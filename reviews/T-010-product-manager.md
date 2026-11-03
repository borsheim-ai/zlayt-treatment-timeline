# T-010 review — product-manager-reviewer

**Verdict: changes** (0 blockers, 1 major, 3 minors).

The five domain dossiers meet the §6.3 structure and the count requirements, and they are the strongest part of M1 so far. Every checklist is tied to sample-case facts I checked against `spec/SAMPLE_CASE_TRUTHS.md`: the 73-day and 28-day intervals, 01-09 vs 01-19, $8,390, the $185 rate, the LOC qualifier and the ESI recommendation. All 5 sampled sources say what their one-line takeaways claim.

The card does not pass because of the calibration sections. These sections are compiled verbatim into the reviewer prompts, and they teach the reviewers to under-grade lost or invented facts. Legal-nurse rates a dropped "without loss of consciousness" as **major**, although its own §5 lists that as a dealbreaker and Appendix C lists it as a "must not". Legal-nurse also rates "MRI performed" for a record that only says "MRI ordered" as **minor**. Claims-adjuster rates an ESI that was only recommended but shows up as completed as **minor**, and a missed-appointment flag that never appears as **major**. Under CONTRACT.md:676, any finding that "invents or loses facts" is a blocker. A reviewer that follows these anchors will pass a card that should fail. This is the lenient-reviewer failure mode, built into the prompt.

Exercised: `python3 tools/board.py show T-010` (status in_review, commit 34e9398, 3 AC checked); `git show --stat 34e9398` (5 files, 381 insertions; no later changes to personas/); I scripted a §6.3 section, source and checklist count (`artifacts/review-evidence/T-010-011-sections.txt`), which found all 5 files with sections 1-10, unique URLs 8/8/10/9/12 (≥5), checklist items 23/18/18/19/18 (12-25), and 3 calibration examples each. I read all 5 dossiers line by line against spec/SPEC.md Appendix A records 1-9 and SAMPLE_CASE_TRUTHS. I curl-fetched 5 cited sources from these dossiers (Texas Op. 705, HHS minimum-necessary via the archive, privacy.claude.com retention, PubMed 32813098, Claims Journal 2013) and all 5 were supported (`artifacts/review-evidence/T-010-011-source-check.md`). I grepped for AI-filler vocabulary (no hits in T-010 files) and cross-checked each §5 red flag against the §8 calibration severities.

```json
{"card": "T-010", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 34e9398: personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md; no app (M1 research card); sample case = spec/SPEC.md Appendix A records 1-9 + spec/SAMPLE_CASE_TRUTHS.md",
 "exercised": [
  "python3 tools/board.py show T-010 -> status in_review, commits [34e9398], AC 1-3 done:true",
  "git show --stat 34e9398 -> 5 persona files, 381 insertions; git diff 0a10094 HEAD --stat -- personas/ -> empty (no drift)",
  "scripted section/source/checklist/calibration count -> artifacts/review-evidence/T-010-011-sections.txt: all 5 have sections [1..10]; unique URLs paralegal 8, litigation-lead 8, claims-adjuster 10, legal-nurse 9, privacy-compliance 12; checklist 23/18/18/19/18; calibration 3 each (blocker/major/minor)",
  "read all 5 dossiers in full; checked every sample-case fact they cite against spec/SPEC.md:57-65 and spec/SAMPLE_CASE_TRUTHS.md (gaps 73/28, dates 01-09/01-19, $6,240+$2,150=$8,390, $185 rate, 'Recommend' ESI, 'MRI ordered') -> all correct",
  "curl spot-check of 5 cited URLs from these dossiers (privacy.claude.com retention, legalethicstexas Op 705, HHS minimum-necessary via web.archive.org, PubMed 32813098, claimsjournal 2013) -> 5/5 supported; see artifacts/review-evidence/T-010-011-source-check.md",
  "grep for AI-filler terms (seamless|robust|leverag|pivotal|delve|not just|...) -> 0 hits in T-010 files",
  "cross-check of each dossier's section 5 red flags against its section 8 calibration severities and against docs/CONTRACT.md:676 severity definitions"
 ],
 "verdict": "changes",
 "scores": {"structure_6_3": 5, "source_grounding": 5, "checklist_concreteness": 5, "calibration_severity": 2, "lane_discipline": 4},
 "findings": [
  {"severity": "major",
   "title": "Calibration grades fact-losing and fact-inventing outputs below blocker, which contradicts the dossiers' own dealbreakers and the severity definition",
   "evidence": "personas/legal-nurse.md:58 '**major — LOC qualifier dropped.** ... \"Dx: cervical strain; concussion.\"' vs legal-nurse.md:43 red flag '\"Without loss of consciousness\" dropped from the concussion diagnosis' and SAMPLE_CASE_TRUTHS 'must not ... treat \"concussion without loss of consciousness\" as anything other than what it says'; legal-nurse.md:59 '**minor — Order reads as result.** ... record 7 summary \"MRI performed.\"' (record 7 only says 'MRI ordered'; this is an invented event); claims-adjuster.md:58 '**minor — Recommended treatment reads as completed.** ... export \"2026-06-12 — cervical epidural steroid injection.\"' vs claims-adjuster.md:38 red flag 'A single invented fact or overstated finding'; claims-adjuster.md:57 '**major — Missed appointments not flagged.**' vs claims-adjuster.md:41 red flag 'A hidden gap, prior condition, or missed-appointment note ... the chronology omitted'; docs/CONTRACT.md:676 'blocker = violates a spec constraint, invents or loses facts'; SPEC.md:48 'Do not let the tool invent medical facts.'",
   "why_it_matters": "Section 8 is compiled into the reviewer prompt as the severity anchor. A legal-nurse or claims-adjuster reviewer that copies these anchors will file a dropped LOC qualifier as 'changes' and an invented procedure as 'should fix'. The card would then pass a milestone gate with an invented medical fact in the export, which is the single thing Appendix A forbids outright. This is the 'talks itself into it not being a big deal' failure, written into the prompt.",
   "fix": "Re-grade legal-nurse #2 and #3 and claims-adjuster #2 and #3 to blocker, or replace them with genuinely major/minor examples, such as a correct but non-verbatim provider label for major or an un-expanded unambiguous abbreviation for minor. Add one line to each section 5: 'Anything in this list is a blocker.'",
   "acceptance_test": "For each of the 5 dossiers, no section 8 example rated major or minor describes an output that adds, drops or changes a fact relative to the record, or matches a section 5 red flag. Re-run the red-flag/calibration cross-check in artifacts/review-evidence/T-010-011-sections.txt and confirm it shows no contradiction."},
  {"severity": "minor",
   "title": "Section 5 'dealbreakers' carry no severity, so the dossiers contradict themselves (privacy-compliance)",
   "evidence": "personas/privacy-compliance.md:44 red flag 'Full record text or completions written to server logs on the public deployment.' vs privacy-compliance.md:59 '**major — Completions in server logs.**'",
   "why_it_matters": "A reviewer faced with a dealbreaker that its own calibration rates as major will pick the softer grade. Severity should come from one place.",
   "fix": "Either rate the logging example as a blocker, or reword the red flag so it is narrower than the calibration example (for example, 'logs record text and the deployment is public without a synthetic-data banner').",
   "acceptance_test": "Every section 5 bullet in privacy-compliance.md either has no matching section 8 example or matches one rated blocker."},
  {"severity": "minor",
   "title": "Some checklist items ask for features beyond Appendix A without a severity cap, which invites scope creep from reviewers",
   "evidence": "personas/claims-adjuster.md:19 '2. Delay to first treatment is computed from the accident date (here: same day, EMS) and shown' (not a must-have, and it assumes 01-09 is the accident date, which conflicts with item 1 at line 18 'the tool ... chose one silently'); personas/litigation-lead.md:30 '12. An audit trail exists showing who accepted/edited each item' (a single-user prototype has no 'who')",
   "why_it_matters": "Reviewers will file these as majors against a time-boxed prototype. Appendix A grades 'cut scope on purpose', and the reviewer prompts should not push the other way.",
   "fix": "Mark items that go beyond the must-haves as '(nice-to-have; minor at most)'. Reword claims-adjuster #2 as 'if the tool shows delay to first treatment, it shows it against both conflicting accident dates or not at all'. Reword litigation-lead #12 to 'what the model produced vs what the human changed'.",
   "acceptance_test": "Each checklist item either traces to an Appendix A must-have, constraint or Appendix C truth, or carries an explicit '(minor at most)' tag."},
  {"severity": "minor",
   "title": "privacy-compliance checklist reaches into security-reviewer's lane without deferring",
   "evidence": "personas/privacy-compliance.md:29 '10. API keys are server-side only and never appear in client code, logs, fixtures, or the repo.'; privacy-compliance.md:37 '18. Demo mode serves cached synthetic results and cannot be used to submit arbitrary text to the LLM without the server's rate limit and spend cap.'; Limits at privacy-compliance.md:78 do not defer either item; personas/security.md:28-29 and :20-22 own the same checks",
   "why_it_matters": "Two reviewers filing the same finding at different severities creates triage noise and lets the softer grade win.",
   "fix": "Drop #10 and #18, or prefix them with 'note and defer to security-reviewer'. Add 'secrets, rate limits and spend caps belong to security-reviewer' to Limits.",
   "acceptance_test": "grep -n 'spend cap\\|API keys' personas/privacy-compliance.md matches only lines that say 'defer to security-reviewer'."}
 ],
 "whats_right": [
  "Every checklist is anchored to exact sample-case truths (73/28 days, 01-09 vs 01-19, $8,390, '$185 per visit' as rate, 'Recommend' ESI), and I verified each one against SPEC.md:57-65.",
  "Sources are honest about their bias (vendor and plaintiff/defense advocacy labeled) and about fetch failures (ABA 512/477R marked secondary); 5/5 spot-checked takeaways are accurate.",
  "Limits sections name the persona that owns each adjacent concern (paralegal defers strategy to litigation-lead and clinical reading to legal-nurse), which keeps reviewers in their lane."
 ],
 "questions_for_chris": []}
```
