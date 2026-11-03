# T-088 review: date-convention suggestion (staff-engineer-reviewer)

**Verdict: fail.** One blocker: the suggestion's `reason` says the evidence dates are "in this record" when they sit in other records of the packet. I rated it a blocker, not a major, under CONTRACT D.2 and CLAUDE.md non-negotiable 5 (every statement traces to the input). The code-only, never-applied and D-041 parts hold.

Scope: commit f667f08 (`app/backend/date_convention.py`, `app/backend/present.py:122-135`, `tests/unit/test_date_convention.py`, the T-088 contract section in `memory/contracts/api.md`). Cross-checked against D-041 and D-042 in `memory/ORCHESTRATOR_DECISIONS.md` (lines 49-50) and the golden sample `evals/golden/case_01_date_formats.txt`.

**Checks against your four points**
1. Code only: holds. `date_convention.py` imports only `re` and `dates`, with no LLM or call path. Mutation 88e (a DB write that auto-confirms the ISO reading) is caught by 2 tests.
2. Never auto-applied, one confirm still required: holds. No server path reads `suggestion` except `present.py:129`, which only builds it. `review.confirm_date` (`review.py:172-181`) still takes the client's date and checks it against the candidates. The D-041 block reads `records.date_status`, not the suggestion (`review.py:45-50`).
3. Reason quotes a real date from the packet: the quoted dates are real (`02/17/2026`, `03-17-26`), but the scope is wrong. See F1.
4. Mixed or contradictory packets: `date_convention.py:54-55` returns `None` when the orders disagree or there is no evidence. Mutant 88a (mixed packets allowed through) is caught.

**Exercised**
- `python3 tools/board.py show T-088` and `show T-089`; `git show f667f08 --stat` and per-file diffs; `git show f667f08:<path>` for every file in scope; D-041/D-042 lines in `memory/ORCHESTRATOR_DECISIONS.md`.
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: 151 passed, 1106 deselected. `pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py -v`: 25 passed.
- Mutation suite in a scratch copy (`artifacts/review-evidence/T-088-T-089/mut`, runner `mutate.py`, output `mutation_run.txt`). Core rules 88a/88b/88c/88d/88e are all caught.
- Probe on golden case_01 through FastAPI `TestClient` (no live server, no network, `LLM_BACKEND=fixture`): output in `artifacts/review-evidence/T-088-T-089/probe_t088_output.txt`.
- `git diff --cached --name-status` and `git cat-file -e HEAD:<path>` (index state, see F3).
- `grep -rn suggestion app/frontend` returned 0 matches. `grep -c "suggestion\|dismissal" evals/golden/case_01_date_formats.expected.json` returned 0.

```json
{"card": "T-088", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f667f08: app/backend/date_convention.py, app/backend/present.py (dates_to_confirm), memory/contracts/api.md (T-088 section), tests/unit/test_date_convention.py; golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process)",
 "exercised": ["board.py show T-088 and T-089", "git show f667f08 --stat and per-file diffs", "git show f667f08:<path> for in-scope files", "memory/ORCHESTRATOR_DECISIONS.md D-041, D-042", "pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)", "pytest tests/unit/test_date_convention.py -v (8 passed)", "mutation suite 88a-88e in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)", "probe on golden case_01 via TestClient (artifacts/review-evidence/T-088-T-089/probe_t088_output.txt)", "git diff --cached --name-status; git cat-file -e HEAD:<path>", "grep suggestion app/frontend (0); golden case_01 expected.json (0)"],
 "verdict": "fail",
 "scores": {"code_only_no_llm": 5, "never_auto_applied_d041": 5, "reason_grounded_in_packet": 2, "mixed_packet_handling": 4, "tests_fail_on_mutation": 4, "ac_integrity": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Reason says the evidence dates are 'in this record' when they come from other records in the packet",
   "evidence": "app/backend/date_convention.py:64-65 builds 'Other dates in this record use ...' while `_evidence(records, raw_text)` (line 52) scans every packet record. Golden repro (probe_t088_output.txt): the 04/05/2026 suggestion on record r8 returns reason '4 other dates in this record use month first (02/17/2026) and (03-17-26)', with evidence record ids r2 and r6 (the other two counted dates, 3/25/26 in r7 and 04/14/2026 in r7's excerpt, are also outside r8). evals/golden/case_01_date_formats.txt: record 8 (lines 39-41) contains only 'Patient reports no new symptoms.' and no other date. The false wording is pinned by tests/unit/test_date_convention.py:32, :46 and :99 (line 99 asserts the exact golden reason). The T-088 AC text (board show T-088) says 'the reason (other dates in the packet)'.",
   "why_it_matters": "The paralegal reads a provenance claim about the record in front of them that is false for every golden case of this kind. The D-041 gate still stops an unconfirmed date from reaching the letter, so no wrong date is exported, but the stated reason sends the paralegal to look in the wrong record. CLAUDE.md non-negotiable 5 says every statement must trace to the input, and this one does not. Rated blocker per CONTRACT D.2 (invented fact), not major. The date strings quoted are real.",
   "fix": "Build the reason from the evidence's own record ids, e.g. 'Other dates in this packet use month first (02/17/2026, record 2) and (03-17-26, record 6)'. Remove the phrase 'in this record' everywhere. Update the expected strings at test_date_convention.py:32, :46 and :99.",
   "acceptance_test": "tests/unit/test_date_convention.py: (a) golden case_01 reason names the record of each quoted date and does not contain 'this record'; (b) packet r1 '03/14/2026' with ambiguous r2 '04/05/2026' yields a reason that names record 1. Mutation: restore the old wording, and tests (a) and (b) must fail."},
  {"severity": "major",
   "title": "AC 1 is marked done=true while two of its required parts are not in the codebase",
   "evidence": "board show T-088, AC 1: \"done\": true, evidence \"... UI pre-select is frontend's (see note)\". The AC text includes 'the UI pre-selects it' and 'eval case'. Handoff: 'Left: frontend pre-select; qa golden case.' grep -rn suggestion app/frontend: 0 matches. grep -c 'suggestion|dismissal' evals/golden/case_01_date_formats.expected.json: 0.",
   "why_it_matters": "The card says the AC is done, but the paralegal-facing behaviour (radio pre-selected with the reason, confirm on click only) does not exist, and the eval case the AC names does not exist either. Only the unit-level half is shipped. A required AC item that is present but incomplete is major under the persona calibration.",
   "fix": "Set AC 1 back to done=false until (a) the frontend pre-select ships and (b) a golden expected entry for case_01 record 8 asserts the MDY suggestion. Or split those two parts into follow-up cards and close the unit half only.",
   "acceptance_test": "grep -n suggestion evals/golden/case_01_date_formats.expected.json shows the MDY assertion. A frontend or E2E test shows the 04/05/2026 radio pre-selected with its reason, no confirm request is sent on load, and Accept stays blocked (422 DATE_UNCONFIRMED) until a click on Confirm."},
  {"severity": "major",
   "title": "Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)",
   "evidence": "git diff --cached --name-status: 'D app/backend/date_convention.py', 'D app/backend/dismissal_patterns.py', 'D tests/unit/test_date_convention.py', 'D tests/unit/test_dismissal_patterns.py' (also 'D app/llm/prompts/conflicts_v1.md'). git cat-file -e HEAD:app/backend/date_convention.py succeeds, and the on-disk files match HEAD byte for byte (checked with git show f667f08:<path> | diff). git status shows them as '??' untracked.",
   "why_it_matters": "The committed artifact at HEAD is intact, so this is not a defect in f667f08 itself. But the next commit made from this index deletes the T-088 and T-089 code and tests from the repository. That is a silent loss of both cards' deliverables.",
   "fix": "Orchestrator (not this reviewer) restores the index for the card paths without touching the working tree, then commits with explicit paths. The index then matches HEAD for these four files.",
   "acceptance_test": "git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py prints nothing, and git ls-files app/backend/date_convention.py lists the file."},
  {"severity": "minor",
   "title": "Weak assertion: `and`/`or` precedence lets the two-digit-year test pass with the wrong convention",
   "evidence": "tests/unit/test_date_convention.py:65: assert s[\"convention\"] == \"MDY\" and s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"]. Python parses this as (A and B) or C. When iso is not None and is in the candidates, C is True whatever the convention. In this packet iso is None, so the convention is pinned today; the defect is latent.",
   "why_it_matters": "A later change that makes iso non-null for this case could pass with the convention wrong, which is exactly the regression this test exists to catch.",
   "fix": "assert s[\"convention\"] == \"MDY\" and (s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"])",
   "acceptance_test": "Mutant: swap _LABEL so MDY reports DD/MM while iso is non-null for a two-digit-year packet. The fixed assertion must fail."},
  {"severity": "nit",
   "title": "Unused import",
   "evidence": "app/backend/date_convention.py:10: from app.backend import dates (no reference to dates in the module).",
   "why_it_matters": "Dead import; harmless.",
   "fix": "Delete the line.",
   "acceptance_test": "python -m pyflakes app/backend/date_convention.py (or a grep for 'dates\\.') reports nothing."}
 ],
 "whats_right": [
  "No server path reads the suggestion: present.py:129 only builds it, confirm_date (review.py:172-181) still takes the client's date and checks it against the candidates, and the D-041 block reads records.date_status (review.py:45-50).",
  "Mixed-order and no-evidence packets return None (date_convention.py:54-55); mutant 88a, which lets mixed packets through, fails test_no_suggestion_without_evidence_or_with_mixed_evidence.",
  "Code only with no LLM path, and the auto-confirm mutant 88e is caught by two tests (the write-check and the golden confirm test)."
 ],
 "questions_for_chris": ["For a packet whose dates disagree on order, should the paralegal see a short note that the packet is mixed, or is silence (no suggestion) the intended behaviour? The AC allows either."]
}
```
