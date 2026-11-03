---
name: research-attack-map-gaps
description: Recurring adjuster-attack issues in Zlayt research (omitted attacks in r1; invented Rivera facts in fix rows in r2) and verified source facts
metadata:
  type: project
---

T-008 round 1 (2026-11-01): adjuster-attacks.md A1–A11 omitted delay-to-first-treatment, MIST/transport, attorney/LOP timing,
duration/passive care. Round 2 (568e4b7) added A12–A15 — but the new rows invented Rivera facts: A15 "referral to pain
management" (rec 7 names no referral source) and "Rivera's care is active" (no modality in recs 4-6). Rated blocker + major.

Round 3 (da17ba2): r2 items fixed, but "radicular symptoms" (adjuster-attacks.md notes A4/A5) had survived since r1;
I missed it twice. Rated blocker: golden sample.expected.json must-not lists "Radicular symptoms in right arm." Also overbroad
negatives ("records name no referral source" vs rec 3 "Refer to physical therapy") and "no visit count" (labels say visit 8/9).

Round 4 (654b31c, re-check, claude-haiku-5-5 run): "radicular" gone (grep exit 1), A10 "visit count" gone, line 99 scoped,
CLARA named. But line 34 (A14) kept the same unscoped "no record states a referral source" — the fix scoped one instance of a
repeated phrase and left the other. Left at minor (not re-rated); r4 gate = not pass. Evidence: reviews/T-008-claims-adjuster-r4.md.

**Why:** researchers fill "Rivera records that trigger it" cells from memory of the case, not from sample.txt; fix rounds
are where new invented facts slip in.

**How to apply on fix rounds:** grep the WHOLE file for every phrase a finding named ("no record states", "no referral
source"), not just the cited line; a partial scope fix still leaves the finding open.

**How to apply:** sweep NOTES prose too, not just table cells; grep research for the golden must-not diagnosis regex
(sample.expected.json ~:974: whiplash|radicul|stenosis|sprain|bulg|nerve root|spondyl) and for unscoped negatives. On every re-review, grep each NEW row's Rivera cell against evals/golden/sample.txt (esp. "refer", "active",
"performed", severity words). Correction: Claims Journal src 1 does NOT mention attorney retention/referral/LOP (curl
re-checked r2) — it covers transport, vehicle damage, start/gaps, provider type, active/passive, duration. Verified by curl:
Brinjikji AJNR 2015 = LUMBAR only; Nakashima Spine 2015 PMID 25584950 = cervical, bulging 87.6%, SCC 5.3% (C5-C6 41%);
Herrera v. Madrak >12 missed PT; VLW src 16 "eight days later"; IRMI Stowers ok; Braun src 18 defines MIST; Fletcher v.
Simmons 403. D-017: tool never computes delay — judge research, not code, on that. Use curl (no WebFetch); write curl
output only to a literal artifacts/review-evidence/ path (hook rejects `mkdir $VAR`). Evidence:
artifacts/review-evidence/T-008-adjuster-source-checks.txt, T-008-r2-adjuster.md. Related: [[lexicon-review-method]].
