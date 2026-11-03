---
name: t061-speaker-scope-closed-list
description: T-061 r2 (e1400d4): patient_report exclusion is a closed speaker word list with a 3-word window and sentence split; colon labels, Mrs. split, mixed sentences still leak
metadata:
  type: project
---

The self-report exclusion (`self_report_scope.exclude_sentence`, app/llm/lexicon.yaml:89) only recognises a short closed list of
non-patient speakers, requires whitespace right after the speaker word, allows at most 3 words before the speech verb, and is applied to
the sentence found by grounding `_SENT_END` (which splits at "Mrs.", "Dr.", "Pt."). Round 2 (e1400d4) still labels as patient_report:
"EMS: pt c/o neck pain.", "Family: neck pain 7/10, C/O headache.", "Wife (Mrs. Ortiz) reports he complains of neck pain.", "C/O neck pain;
wife reports headaches.", plus unlisted speakers "Girlfriend reports he complains...", "Co-worker reports patient c/o...".
It also drops the patient clause in "EMS reports neck pain, patient states headaches." (record).

**Why:** D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) binds: spouse/family/EMS/witness statements are not patient self-report. The
round-1 blocker was the EMS/wife mislabel; its acceptance list only covered no-colon phrasings, so the class leaked in other forms.

**How to apply:** when re-reviewing T-061 or any attribution/label fix, do not stop at the phrasings the card's acceptance test lists.
Generate variants (speaker-label colon, abbreviation before the subject, descriptor before the verb, mixed clause in one sentence,
unlisted noun) and run them through the production constructor (flags._flag -> grounding.has_self_report). Probe script:
artifacts/review-evidence/T-061-r2-probe.py (run against a `git archive` of the commit). Still open at last review: findings 1-6 in
reviews/T-061-claims-adjuster-r2.md; check whether a later round closed them before reusing this.
