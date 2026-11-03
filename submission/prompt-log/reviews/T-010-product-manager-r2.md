# T-010 review, round 2 — product-manager-reviewer (written by the litigation-lead agent covering the PM's checklist)

**Verdict: pass** (0 blockers, 0 majors, 2 minors).

I judged this strictly against the four round-1 PM findings in `reviews/T-010-product-manager.md`.

- **M1 (calibration severity) is resolved.** Each fact-losing or fact-inventing anchor is now a blocker: legal-nurse "LOC qualifier dropped" and "MRI performed", and claims-adjuster "missed appointments not flagged" and "ESI reads as completed". Every §5 now opens with "Each item here is a **blocker**". Every §8 states the severity rule. None of the remaining major or minor anchors adds or drops a record fact, and none matches a §5 bullet. These changes are compiled into the agent bodies.
- **m2 (privacy logs) is resolved.** The calibration example is now a blocker.
- **m3 (scope caps) is partial.** Adjuster #2 was rewritten under D-017, but lit-lead #12 still asks "who" accepted each item, and no item carries a "(minor at most)" cap.
- **m4 (security lane) is not resolved.** Privacy items 10 and 19 and step 4 still check API keys, rate limits and spend caps, and Limits does not defer to security-reviewer.

Both open items were minor in round 1 and remain minor, so the verdict rule gives pass. Findings outside the PM checklist are in `reviews/T-010-litigation-lead-r2.md`; they include two majors, so the card as a whole is still `changes`. The resolution table is in `artifacts/review-evidence/T-010-r2-resolution.md`, section B.

```json
{"card": "T-010", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "Round 2, written by the litigation-lead-reviewer agent covering the product-manager-reviewer's round-1 checklist (reviews/T-010-product-manager.md), judged strictly against those four findings. git diff 34e9398..6bb13dd -- personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md (commits 6404549, 6bb13dd; working tree = 6bb13dd). No app (documents card).",
 "exercised": [
  "python3 tools/board.py show T-010 (commits 34e9398/6404549/6bb13dd; handoff)",
  "git diff --stat 34e9398..6bb13dd -- personas/ and git diff --stat 6bb13dd -- personas/ (empty)",
  "read all five dossiers at 6bb13dd in full; re-read reviews/T-010-product-manager.md findings and acceptance tests",
  "python3 -I artifacts/review-evidence/T-010-r2-count.py: §5 blocker line present in 5/5; calibration severities paralegal B/M/m, lit-lead B/M/m, adjuster B/B/B/M, nurse B/B/B/M, privacy B/B/m",
  "cross-checked each remaining major/minor calibration example against its own §5 bullets and against 'adds, drops or changes a fact relative to the record' (PM M1 acceptance test)",
  "grep -n -i 'minor at most\\|nice-to-have' and 'defer' over the five dossiers: 0 hits; grep -n -i 'spend cap\\|API keys' personas/privacy-compliance.md: :29, :38 (no deferral)",
  "python line-membership check of personas/<p>.md vs .claude/agents/<p>-reviewer.md: 6404549 severity anchors present in compiled bodies; 6bb13dd lines (incl. adjuster :19) absent",
  "wrote section B of artifacts/review-evidence/T-010-r2-resolution.md"
 ],
 "verdict": "pass",
 "scores": {"structure_6_3": 5, "source_grounding": 5, "checklist_concreteness": 5, "calibration_severity": 5, "lane_discipline": 3},
 "findings": [
  {"severity": "minor",
   "title": "(r1 minor 3, partial) Lit-lead #12 still requires 'who' accepted, and no beyond-must-have item carries a severity cap",
   "evidence": "personas/litigation-lead.md:30 \"12. An audit trail exists showing who accepted/edited each item and what the model originally produced.\" (unchanged from r1); grep -c -i 'minor at most|nice-to-have' across the five dossiers = 0. Resolved part: personas/claims-adjuster.md:19 item 2 now 'first recorded treatment ... never computes a \"delay from the accident\"' (D-017). That line is not yet in .claude/agents/claims-adjuster-reviewer.md.",
   "why_it_matters": "The prototype is single-user (D-010 keeps originals and an 'edited' marker, with no user identity). A litigation-lead reviewer following item 12 could file a major for missing user attribution against a time-boxed prototype that cut that on purpose.",
   "fix": "Item 12: \"An audit trail shows what the model originally produced and what the human accepted or changed (D-010); user identity is a Part 2 rollout item (minor at most here).\" Tag any other item beyond Appendix A/C '(minor at most)'.",
   "acceptance_test": "litigation-lead.md item 12 does not require user identity. Each checklist item traces to an Appendix A must-have, a constraint, an Appendix C truth or a D-decision, or carries '(minor at most)'."},
  {"severity": "minor",
   "title": "(r1 minor 4, not resolved) Privacy checklist still owns secrets, rate limits and spend caps without deferring to security-reviewer",
   "evidence": "personas/privacy-compliance.md:29 \"10. API keys are server-side only and never appear in client code, logs, fixtures, or the repo.\"; :38 \"19. Demo mode ... without the server's rate limit and spend cap.\"; :55 step 4 \"rate limit and spend cap, no key in client\"; :85 Limits has no deferral. grep -n -i defer over the five dossiers: 0 hits. Handoff for 6bb13dd does not mention this finding.",
   "why_it_matters": "Two reviewers filing the same finding at different severities creates triage noise and lets the softer grade win.",
   "fix": "Prefix items 10 and 19 (and step 4's key/spend-cap clause) with 'note and defer to security-reviewer'. Add 'secrets, rate limits and spend caps belong to security-reviewer' to Limits.",
   "acceptance_test": "grep -n 'spend cap\\|API keys' personas/privacy-compliance.md matches only lines that say 'defer to security-reviewer'."}
 ],
 "whats_right": [
  "Every dossier's §5 now says its items are blockers and §8 restates the rule, so the severity comes from one place.",
  "The fact-losing and fact-inventing anchors (LOC dropped, MRI performed, ESI completed, missed appointments hidden, server-log leak) are blockers and are compiled into the agent bodies.",
  "The new major anchors (nurse judge-prompt gap with no wrong output observed; adjuster gap flag missing dates) are true majors that teach the reviewer where the line is."
 ],
 "questions_for_chris": []}
```
