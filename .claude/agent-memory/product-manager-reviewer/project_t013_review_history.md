---
name: t013-review-history
description: T-013 REQUIREMENTS review rounds — verdicts, what stayed open after round 3 (as of 2026-11-01)
metadata:
  type: project
---

T-013 (spec/REQUIREMENTS.md) review history:
- **Round 1 (65894f6):** PM changes (5 majors); paralegal fail (flags exported into letter).
- **Round 2 (64f766e):** PM changes (5 majors).
- **Round 3 (b4f3924):** PM changes (2 majors, 4 minors, 1 nit). 4 of the 5 r2 majors are resolved.

Open after round 3. All of it is reconciliation; the content is sound.
1. Ship bar row 4 and R-TL-4 say "19 of 20" seeded hallucinations, but the golden has 34. The fix is to state the threshold as a rate.
2. §8 claims ADR-017 reconciled everything. These still disagree:
   - The api.md export example has dot leaders, different total wording and a different Source line.
   - The notes citation format differs across A-106, R-EX-4 and api.md.
   - confirm_date returns 422 `date_invalid` in api.md and `invalid_edit` in REQ.
   - REQ predates D-018's lexicon `hedge` booleans.
   - The source_kind spelling is `patient_report` in REQ/api and `patient_self_report` in golden.
   - K4/K5 are must in golden and should in REQ.
   - must_not goes to M14 in golden; REQ says M13.

Seeds used for R-ID samples: 13, 1302, 2026. The probe script is at artifacts/review-evidence/T-013-r3check.py.

**T-025 (split from T-013, commit 2e92535, reviewed 2026-11-01): changes, 3 majors.**
- The §8 "Checked and aligned" claims were false. The confirm_date code flipped sides: api.md now says invalid_edit and REQ says date_invalid. A-106 says "not record numbers", but R-EX-4 cites "record N (...)". DECISIONS.md:204 fixes the "single agreed AI line". The api.md confirm_date example adds a gap for a phone note.
- The notes block hand-off is circular: REQ says the golden is the authority, and T-015 r3 says REQ is the file that lags.
- must_not is still the fixed range M1–M14, and the golden is now at M1–M17.
- Probe: artifacts/review-evidence/T-025-pm-probe.py.

**Why:** Artifacts (golden, api.md, ASSUMPTIONS) landed minutes after the REQ commit. Every round's residual has been cross-artifact drift, not REQ content.

**How to apply:** In any round 4 or T-018 contract review, re-run the probe and diff REQ against the current golden and api.md commits. Check the commit timestamps against the REQ commit. Related: [[spec-review-patterns]].

T-025 r2 (changes, 4 majors): writer fixed the authority rule, date_invalid and ship bar 4, but only half-applied "fix every instance". R-FL-4 still said M1-M14 after R-CO-3 was fixed; REQ A-106 row still said "not record numbers" after ASSUMPTIONS.md changed; §8 row 5 owned by a done card; §6 block 2 != golden because qa rewrote the golden after the REQ commit. Probe: artifacts/review-evidence/T-025-pm-r2-probe.py.
**How to apply:** after any "fixed" handoff, grep every occurrence of the old pattern (M1–M14, "today N", "not record numbers"), not just the one the finding cited. Check each §8 owner card's status with board.py show.
