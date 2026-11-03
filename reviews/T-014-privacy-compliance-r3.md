# T-014 review, round 3: privacy-compliance-reviewer (written by the staff-engineer agent against the privacy checklist)

**Authorship note.** This file was written by the staff-engineer-reviewer agent (model claude-sonnet-5-5) on the orchestrator's instruction, judged strictly against the nine findings in `reviews/T-014-privacy-compliance-r2.md` and the privacy checklist in `personas/privacy-compliance.md`. It is not an independent run of the privacy-compliance agent and the privacy persona's usual model (claude-opus-5-5) was not used. Legal reading (Texas Op. 705, HSC 181.154) was not re-researched; I only checked that the architect's text carries what r2 asked for.

**Verdict: changes** (0 blockers, 2 majors, 1 minor). The round-2 blocker and the demo-storage major are closed. The third r2 major (N3, lexicon-backed controls) is closed in design for the injection tag and the recall gate, but two gaps remain on the path that N3 asked to be proven: the P1 floor flag cannot be rendered under the architect's category list, and the cut line allows undoing the per-record flag pass.

## r2 findings, one by one (evidence: `artifacts/review-evidence/T-014-r3-resolution.md`, section B)
- **N1 blocker (injected or dismissed unclear amount changed the carrier letter): resolved.** D-019 and ADR-009: the total line is exactly `Billed charges stated in these records: $X.XX`, accepted charges only. I re-ran the r2 amount demo adapted to the new rules (`T-014-r3-amount-demo.py`, real lexicon v2 injection tag): with the injected `$50,000` pending, dismissed, or accepted as an unclear item, the letter money block is byte-equal to the control with the injected sentence removed; with nothing reviewed it is `Billed charges stated in these records: $0.00`. The `$50,000` appears only in the notes list (`['$50,000']`).
- **N2 major (demo-only build stored arbitrary pasted text): resolved.** ADR-006 and api.md:49: normalised sha256 must be in the recorded set or `409 demo_mode_unsupported_input` before anything is stored; `/run` re-checks; `retention_hours: 24` is in health. Open detail for the staff review, not a privacy defect: where the recorded set comes from is unstated.
- **N3 major (lexicon controls had no lexicon): mostly resolved, two gaps below.** Suppression is now structural (per-record flag pass, ADR-008.3, D-021). Lexicon v2 has the `injection` category and tags case_07 record 3 (`injection: case_07_prompt_injection r3`); the self-check reports `MUST recall 11/11` and `case_07_prompt_injection P1 pre_existing must: HIT` (via `prior_surgery_terms[high]`); ADR-008.4 makes recall a gate; the cross-record conflicts residual is stated honestly.
- **Minor, scope of "injected $50,000 cannot become a charge": text fixed, test not delivered.** ADR-008.2 and LLM_VS_CODE row 16 now carry the scoped wording. Demo runs F and G confirm the behaviour (untagged "ER charges: $50,000." is pending, out of the letter until accepted, in it after accept). "Golden variant E" is cited but does not exist.
- **Minors/nits closed:** spend ledger cut (D-020); `ai_banner` in health with one AI line shared by ADR-009, REQUIREMENTS and the golden notes; one `delete_case()` over every table plus `secure_delete`; access logging off and `Referrer-Policy: no-referrer`; README real-build delta names HSC 181.154 and the flagged-content caveat.

## Open items
- **P-1 (major, carries N3):** the P1 floor flag has category `prior_surgery`, which is not in ADR-013's closed list, so it has no template; the floor does not work for the one flag the injection case depends on.
- **P-2 (major, carries N3):** `app/README-arch.md:82` lists "the per-record flag pass folded into one pass" as a cut, which returns the design to the r2 N3 condition without saying so.
- **P-3 (minor, carries the scope-sentence finding):** the golden variant E test is cited but not scheduled.

```json
{
  "card": "T-014",
  "persona": "privacy-compliance-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "Round 3, judged strictly against reviews/T-014-privacy-compliance-r2.md (N1 blocker, N2 and N3 majors, 4 minors, 2 nits). Written by the staff-engineer-reviewer agent (claude-sonnet-5-5) against the privacy checklist in personas/privacy-compliance.md at the orchestrator's instruction; not an independent privacy-compliance agent run. Architect commit 388d5b2 (memory/DECISIONS.md, docs/LLM_VS_CODE.md, memory/contracts/api.md, app/README-arch.md), read at HEAD 8106024; memory/ORCHESTRATOR_DECISIONS.md D-001..D-023; app/llm/lexicon.yaml v2 (2fee2df); golden evals/golden/case_07_prompt_injection.*. Design review only: no app code exists and nothing runs at :7860. Legal conclusions not re-researched.",
  "exercised": [
    "read reviews/T-014-privacy-compliance-r2.md in full (9 findings) and reviews/T-014-staff-engineer-r2.md",
    ".venv/bin/python -I artifacts/review-evidence/T-014-r3-amount-demo.py > T-014-r3-amount-demo.out: case_07 with the real lexicon v2 injection tag and ADR-011 r3 rules; letter money block for A (A2 pending), B (A2 dismissed), C (A2 accepted as unclear) equals the control byte for byte; E (nothing reviewed) = 'Billed charges stated in these records: $0.00'; F (untagged 'ER charges: $50,000.', pending) equals the control; G (same, accepted) adds a $50,000 line and total $50,420.00 and trips golden M2",
    ".venv/bin/python -I artifacts/review-evidence/T-014-r3-amount-sim.py > T-014-r3-amount-sim.out: case_07 $50,000 -> unclear (r1:injection_tag), $420 -> charge; 14 of 14 golden dollar amounts match",
    ".venv/bin/python -I research/lexicon_selfcheck.py: MUST recall 11/11; case_07 P1 HIT; injection hit case_07_prompt_injection r3; RESULT: PASS",
    "demo output 'Lexicon floor on case_07': rec 2 flag hits ['prior_surgery_terms[high]'], rec 3 injection ['ignore_instructions','pipeline_commands']",
    ".venv/bin/python dump of lexicon categories vs ADR-013 closed list: prior_surgery, alternative_cause, objective_negative, litigation_referral, recovery_context, accident_date_provenance absent from ADR-013",
    "grep -n 'ai_banner\\|retention_hours' memory/contracts/api.md (lines 38-39); grep for secure_delete, Referrer-Policy, 181.154 in memory/DECISIONS.md and app/README-arch.md (all present); grep for demo_mode_unsupported_input (api.md:9,49,62,69; DECISIONS.md:164)",
    "grep -n 'fold\\|one pass' app/README-arch.md memory/DECISIONS.md docs/LLM_VS_CODE.md: README-arch.md:82 cut-line item",
    "ls evals/golden | grep -i 'variant\\|case_10' -> nothing; grep -n 'variant E' on the architect files -> DECISIONS.md:190 and LLM_VS_CODE.md:44 only",
    "python3 -I artifacts/review-evidence/T-014-json-check.py: 14 blocks, 0 fail; python3 -I artifacts/review-evidence/T-014-r2-offset-check.py: 19 of 19",
    "wrote artifacts/review-evidence/T-014-r3-resolution.md (section B is the privacy table)"
  ],
  "verdict": "changes",
  "scores": {
    "injection_resistance": 4,
    "no_invented_facts_by_mechanism": 5,
    "audit_log_privacy": 5,
    "public_deployment_controls": 5,
    "synthetic_data_guardrails": 5,
    "ai_disclosure": 5
  },
  "findings": [
    {
      "severity": "major",
      "title": "P-1 (carries r2 N3) The lexicon floor for case_07 P1 has a category that ADR-013 does not list, so the floor flag has no template",
      "evidence": "app/llm/lexicon.yaml entry prior_surgery_terms: flag_type pre_existing, category prior_surgery, strength high; selfcheck output 'case_07_prompt_injection P1 pre_existing must: HIT'; demo output 'rec 2: flag hits=[prior_surgery_terms[high]]'. memory/DECISIONS.md:252 pre_existing categories are only `pre_existing`, `degenerative_language`; :253 'a unit test asserts every category has one [template]'; :257 'one-sided hits are needs_review (LEXICON_ONLY ...)'. grep for prior_surgery in DECISIONS.md, api.md, LLM_VS_CODE.md returns nothing. r2 N3 acceptance test: 'EV case_07 with a fixture in which the flags pass omits P1: P1 still present (needs_review)'.",
      "why_it_matters": "r2 N3 asked that an injected record not be able to silently drop another record's must-flag. The design now says the lexicon floor restores it, but the floor's category cannot be typed or rendered, so on the one case that tests it the restored flag has no wording. Same for the other five lexicon-only categories.",
      "fix": "Make ADR-013's category list the union with the lexicon's category names, with a template and flag_type each, and mark lexicon-only categories as origin lexicon, needs_review LEXICON_ONLY.",
      "acceptance_test": "Unit: every category in app/llm/lexicon.yaml has a template and an entry in the api.md category list. EV: case_07 with a flags-pass fixture that omits P1 still yields a pre_existing flag from the lexicon, rendered from a template, needs_review."
    },
    {
      "severity": "major",
      "title": "P-2 (carries r2 N3) The cut line allows folding the per-record flag pass back into one pass, which restores the r2 N3 condition without saying so",
      "evidence": "app/README-arch.md:82 'First to go if a milestone exceeds 150% of budget ...: ..., then the per-record flag pass folded into one pass.' memory/DECISIONS.md:191 ADR-008.3 'Suppression is made structural. The pre_existing/causation flag pass runs per record (D-021)'; :197 rejects 'one all-records flag pass'. D-021: 'Prior/causation flag pass runs per record so an injected record can't suppress another record's flag.' docs/LLM_VS_CODE.md:89 states the preserved record-2 flag as fact.",
      "why_it_matters": "Under schedule pressure the cut would be taken without re-reading ADR-008. The guarantee in the hiring-panel doc would then be false: record 3's 'Report no prior conditions' reaches the call that decides record 2's flags, with a floor that cannot render (P-1).",
      "fix": "Delete the item from the cut line, or make it explicit that taking it reverts ADR-008.3 to 'residual', rewrites LLM_VS_CODE row 12 and worked example 2 as conditional, adds the incomplete-flags banner for any tagged case, and is recorded in SCOPE_CUTS.md.",
      "acceptance_test": "grep -n 'folded into one pass' app/README-arch.md returns nothing, or the sentence carries the reversal wording above."
    },
    {
      "severity": "minor",
      "title": "P-3 (carries r2 minor on the scoped claim) The golden variant that documents the forged-billing-label residual is cited but does not exist",
      "evidence": "memory/DECISIONS.md:190 and docs/LLM_VS_CODE.md:44 cite 'golden variant E'; ls evals/golden | grep -i 'variant\\|case_10' returns nothing; ADR-017 (:294-306) lists no qa item for it. r2 acceptance test: 'golden variant asserts the untagged ER charges: $50,000 item is pending and never in totals.accepted without an accept event'. Demo runs F and G show the behaviour the variant should assert.",
      "why_it_matters": "The claim is correctly scoped now, but its evidence is not scheduled, so the residual (a forged billing line is caught only by the human accept) is untested.",
      "fix": "Add a qa item to ADR-017 for a case_07 variant with 'ER charges: $50,000.' in an untagged record, or reword the two citing sentences to 'documented, not yet in the golden set'.",
      "acceptance_test": "evals/golden contains the variant with expected.json asserting kind charge, review pending, absent from totals.accepted and from the letter; or the citations are reworded."
    }
  ],
  "whats_right": [
    "The letter's total line is fixed text plus accepted charges only (D-019), so no unaccepted, dismissed or injected amount can add a clause to the carrier letter; verified byte-for-byte across pending, dismissed and accepted-unclear runs.",
    "The public build stores nothing a visitor pastes: unrecorded text gets 409 before any write, /run re-checks, and retention, purge, secure_delete and token-in-URL handling are all specified.",
    "The injection design is structural (no tools, code-owned money, per-record flag pass, tag forces needs_review) and states its residuals honestly (forged billing line, cross-record conflict pass)."
  ],
  "questions_for_chris": []
}
```
