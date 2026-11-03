# T-008 round 4 re-check — claims-adjuster-reviewer

Scope: commit 654b31c (docs(research): T-008 round 4), research/adjuster-attacks.md, checked against the r3 findings in reviews/T-008-claims-adjuster-r3.md. No app (research card). Sample: Jordan Rivera, evals/golden/sample.txt.

**Result against the r3 findings:**

| r3 finding | Status | Evidence |
|---|---|---|
| Blocker: "radicular" symptoms label (research/adjuster-attacks.md:61-62) | Resolved | `grep -rn -i radicular research/` → no output, exit 1. Line 61 now quotes rec 7 verbatim. |
| Minor: A10 "no visit count" (line 30) | Resolved | `grep -n -i "visit count\|no PT charge\|no record states a PT charge"` → only line 30, now "no record states a PT charge → cannot total". The "visit count" wording is gone. |
| Minor: "Rivera's records name no referral source" (line 99) | Resolved at line 99 | Line 99 now reads "Record 7 names no referral source (record 3 says only "Refer to physical therapy")." |
| Minor: same overbroad negative in A14 (line 34) | **Not resolved** | Line 34 still reads "...no record states a referral source or an attorney". Unchanged by 654b31c (the diff touches only lines 30, 99, 20 and 151). r3's acceptance test names line 34 explicitly. |
| Nit: src 20 affiliation (line 151) | Resolved | `grep -n -i CLARA` → line 151 "author works for CLARA Analytics, a claims-analytics vendor to insurers". |

Why line 34 stays open: the r3 evidence quoted that exact sentence, and the r3 fix asked for it to be scoped to rec 7 or to quote rec 3. The 654b31c commit message says "referral scope", but only line 99 was scoped. Rec 3 is "Refer to physical therapy 2x/week for 6 weeks.", so an unscoped "no record states a referral source" is still contradicted by a record. The attorney half of the sentence is accurate: sample.txt has no attorney, counsel or LOP mention. The severity stays minor, as in r3. I did not raise it, because no new evidence supports a higher rating.

Gate: the r3 blocker is resolved, but one r3 minor is still open. The orchestrator's bar is that every r3 finding is resolved, so this re-check does NOT pass. The JSON `verdict` below follows the §7.4 mechanical rule (no blocker, no major → pass). Read it together with this paragraph, not on its own.

Model note: this review was run as claude-haiku-5-5 (the model the environment reports). The dossier's expected id is claude-opus-5-5. The record uses the id I actually ran as.

```json
{"card": "T-008", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 654b31c (research/adjuster-attacks.md, 5 insertions/5 deletions) re-checked against reviews/T-008-claims-adjuster-r3.md; no app (research card); Jordan Rivera sample (evals/golden/sample.txt)",
 "exercised": [
  "Read personas/claims-adjuster.md in full; read reviews/T-008-claims-adjuster-r3.md in full; read memory index and two memory files",
  "cd /Users/arsis/zlayt-pm-project && grep -rn -i radicular research/ -> no output, exit=1",
  "grep -n \"radiating to right arm\" research/adjuster-attacks.md -> line 28 (A8, rec 7 quote) and line 61 (plaintiff quotes rec 7), exit=0",
  "grep -n -i \"visit count\\|no PT charge\\|no record states a PT charge\" research/adjuster-attacks.md -> line 30 only, exit=0",
  "grep -n -i \"referral source\" research/adjuster-attacks.md -> lines 34 (A14, unchanged) and 99 (scoped), exit=0",
  "grep -n -i CLARA research/adjuster-attacks.md -> line 151, exit=0",
  "grep -rn -i radicul research/ (broader acceptance regex from r3) -> no output, exit=1",
  "grep -rn -i -E \"whiplash|radicul|stenosis|sprain|bulg|nerve root|spondyl\" research/ -> hits only literature citations (lines 56-60, 135, 149: Brinjikji, Nakashima); no sample-case diagnosis term, exit=0",
  "grep -n -i \"no record\\|no source\\|names no\" research/adjuster-attacks.md -> lines 30, 34, 97, 99 reviewed; line 34 is the only unscoped negative left",
  "grep -n -i \"refer\\|attorney\\|counsel\\|lawyer\\|LOP\\|letter of protection\" evals/golden/sample.txt -> rec 3 'Refer to physical therapy 2x/week for 6 weeks.'; no attorney/counsel/LOP mention, exit=0",
  "git show --stat --format='%H %s' -s 654b31c -> 654b31c1dca5dd5802b995ab0933fd8539dcd297 docs(research): T-008 round 4 ...",
  "git show --stat --format= 654b31c -> research/adjuster-attacks.md | 10 +++++-----; git show 654b31c -- research/adjuster-attacks.md | grep -n \"^[-+].*referral\" -> line 99 changed, line 34 not changed",
  "sed -n '26,27p;99p' research/adjuster-attacks.md | cut -c1-200 (A6/A7 rows and line 99 read directly)"
 ],
 "verdict": "pass",
 "scores": {"source_quality_and_labeling": 4, "adversarial_coverage": 5, "accuracy_vs_sources": 4, "texas_relevance": 4, "usefulness_to_flags_and_lexicon": 4},
 "findings": [
  {"severity": "minor",
   "title": "A14 still says 'no record states a referral source' (r3 minor, not resolved)",
   "evidence": "research/adjuster-attacks.md:34 'Not in records. Rec 7 is a \"new patient\" visit dated 2026-05-18; no record states a referral source or an attorney'. Rec 3 (evals/golden/sample.txt:16): 'Refer to physical therapy 2x/week for 6 weeks.' Line 99 (scoped, fixed in 654b31c): 'Record 7 names no referral source (record 3 says only \"Refer to physical therapy\").' Commit 654b31c changed lines 30, 99, 20 and 151 only.",
   "why_it_matters": "The unscoped negative is the same paraphrase that r3 flagged. Rec 3 is a stated referral to PT, so 'no record states a referral source' is contradicted by a record. A golden or persona author who copies line 34 gets the overbroad claim. The attorney half is accurate (no attorney or LOP mention in sample.txt), so only the referral half needs fixing. Rated minor, as in r3; not re-rated without new evidence.",
   "fix": "Replace the tail of line 34 with: 'Rec 7 names no referral source; the only stated referral is rec 3 \"Refer to physical therapy\"; no record states an attorney or letter of protection.'",
   "acceptance_test": "grep -n \"no record states a referral source\" research/adjuster-attacks.md returns no line; line 34 either names rec 7 for the referral negative or quotes rec 3."}
 ],
 "whats_right": [
  "'radicular' has zero hits in research/ (grep exit 1), and the golden must-not term sweep finds only literature citations.",
  "Line 99 now scopes the referral negative to rec 7 and quotes rec 3 'Refer to physical therapy'; line 61 quotes rec 7 verbatim.",
  "A10 no longer says 'no visit count' (line 30 now says 'no record states a PT charge → cannot total'); src 20 names the CLARA Analytics affiliation (line 151)."
 ],
 "questions_for_chris": []}
```
