---
name: flag-source-kind-and-run-signal
description: source_kind history for self-report labels: T-036 r2/r3 (word filter, spec unamended) then T-061 r0 (dd545e3) narrowed the lexicon but left flags/grounding wiring (AC2) undone and the exclusion regex over-broad
metadata:
  type: project
---

Round 2 (cd4bc60) fixed the intake-date mislabel by deleting the lexicon `self_report` contribution from `grounding._self_report` for every entry. Spec (memory/DECISIONS.md:286) says source_kind is set by code from the lexicon self_report entries. Blocker, r2.

Round 3 (3f37141) restored the lexicon contribution, but behind a word filter: `_PATIENT_WORDS` (grounding.py:177) must find patient|pt|he|she|client|c/o|complain|subjective|patient-reported in the matched text, and `intake_form_accident_date` is skipped by name (grounding.py:175). Result on the commit:
- Still wrong: "S: neck pain 7/10." and "Self-reported neck pain 7/10." (lexicon.yaml:744 matches; code says record). Blocker, r3.
- Over-attributed: "EMS / Witness / Wife / Family complains of ..." give patient_report, because `complain` is in `_SELF` (grounding.py:167) and `_PATIENT_WORDS`. Major, r3.
- Spec not amended: DECISIONS.md:286 and lexicon.yaml:25-26 unchanged in the commit. Major, r3.

T-061 r0 (dd545e3, "narrow lexicon self_report to explicit patient attribution"), verdict fail:
- D-033 (ORCHESTRATOR_DECISIONS.md:41) now decides EMS/witness/spouse/family and bare S:/Subjective: headers are not patient self-report. Lexicon side is right: scope-aware lexicon gives the brief's sentences the right label.
- AC2 not done: no app/backend file in the commit. Production (flags.py:46, :125 -> grounding.has_self_report) still labels "EMS/Witness/Wife/Family complains of neck pain 7/10." patient_report. Blocker, because D-033 makes it a spec violation (r3 rated the same thing major before D-033 existed).
- The commit leaves test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution red (passes at parent 099732b). Its yes-list still asserts "Subjective:" is patient. Major. The card evidence cited selfcheck/golden only.
- exclude_sentence (lexicon.yaml:89) is not sentence-subject anchored: "Patient states EMS noted a laceration." and "Patient reports his wife said he was fine." come out record. Latent until AC2 wires it. Major. Held-out set has no patient-subject + family/EMS-word probe.
- Spec text (DECISIONS.md:286, lexicon.yaml:25-26) still states the superseded rule. Minor.
- Evidence: artifacts/review-evidence/T-061-probe.py and T-061-probe.txt; T-061-base-failed.txt vs T-061-head-failed.txt.

**Why:** each round narrows a classifier to fix the named example, then the narrowing misses an adjacent form or a neighbouring subject. Round r0 of T-061 narrowed the lexicon but not the code path that reads it, and the worker's own probes contained no patient-subject sentence with a family word, so the over-broad exclusion passed.

**How to apply:** when source_kind or any self-report label is touched, (1) diff the commit for app/backend files, not just the lexicon; (2) run the parent-vs-HEAD FAILED list, since a lexicon change flips tested behaviour; (3) probe patient-subject sentences that contain EMS/wife/witness/family words; (4) check whether DECISIONS.md:286 and the lexicon header were amended. Related: [[feedback_lexicon_review_method]], [[project_flag_pass_review_patterns]], [[feedback_review_commit_not_worktree]].
