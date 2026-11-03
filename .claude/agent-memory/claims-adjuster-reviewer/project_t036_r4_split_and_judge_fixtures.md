---
name: t036-r4-split-and-judge-fixtures
description: T-036 r4 (HEAD 5650eae): self-report blocker/majors split to T-061 per 7.4; in-scope verdict changes on committed judge fixtures not replaying (JUDGE_UNAVAILABLE on sample), run status silent on judge outage
metadata:
  type: project
---

On 2026-11-02 the orchestrator split the r3 self-report blocker and majors (labelling precision; lexicon/DECISIONS narrowing) into card T-061 (M2, last card) and asked for an in-scope re-judge of T-036 as reviews/T-036-claims-adjuster-r4.md. Verdict r4: changes (0 blocker, 1 major, 1 minor).

**Why:** the split is a scope decision under 7.4. The carried items still reproduce at HEAD (S: and Self-reported give has_self_report False; "Wife complains of" True), so they must not be read as closed. Do not score them in T-036 r4 and do not drop them from T-061.

**How to apply:**
- A clean HEAD can differ from the live tree when fixtures are re-recorded but uncommitted (44 tests/fixtures/llm/*.json at r4). The sample run on committed HEAD then shows JUDGE_UNAVAILABLE on every model flag (20 failed judge calls) and three test_t037_backend.py replay tests fail. Always replay the committed commit (git archive) before scoring judge-dependent behaviour.
- Judge outages are item-level only; run status stays done (minor). Conflict-pass failure is run-level since 81df4e0.
- Evidence for r4: artifacts/review-evidence/T-036-r4-probe.py and .txt, and T-036-r4-cli-sample*.json/.err.

Related: [[project_flag_source_kind_and_run_signal]], [[feedback_review_commit_not_worktree]].
