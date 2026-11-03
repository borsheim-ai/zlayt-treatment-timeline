# Subagent: Backend: T-088/T-089 r2 (Backend: T-088/T-089 r2)

Source: `agent-aca84bf69b92b47c5.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:30:12.712Z

You own board cards T-088 (round 2) and T-089 (round 2), both claimed by "backend", in /Users/arsis/zlayt-pm-project. Read reviews/T-088-staff-engineer.md and reviews/T-089-staff-engineer.md.

**T-088 (failed):**
- The reason says "in this record" for dates that sit in other records of the packet (golden case_01 record 8). Name where the evidence date really is, e.g. "Other records in this packet use month first (Record 3: 03/14/2026)". Test it on case_01.
- AC1 was marked done without the UI or the eval case. The UI is now card T-096 (frontend). Post a board note correcting the AC evidence, and add the eval-style test in tests/unit. Note on the card the exact golden case qa should add.

**T-089 (changes):** add a route-level test that demo or public mode can't reach the local profile store or the suggestions, so a forced-local mutant fails. Fix the minors.

The shared git index had stale staged deletions of your files; I've unstaged them. Commit only with a temp index (`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD`, add your paths, commit), and never leave staged state in the real index. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

Run `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`. Don't touch flags.py or judges.py (T-094). Never pkill. Then `board.py ac`, the handoff, and `move <card> in_review --agent backend`, for each card. Reply in 2 lines.

### User / tool · 2026-11-02T04:30:12.717Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:14.540Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-088-staff-engineer.md | head -120; echo ======; cat reviews/T-089-staff-engineer.md | head -120; python3 tools/board.py show T-088 | head -60"
}
````

### User / tool · 2026-11-02T04:30:14.691Z

**tool result**
````
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
======
# T-089 review: dismissal-pattern suggestions (staff-engineer-reviewer)

**Verdict: changes.** No blocker. The core rules hold: nothing is auto-dismissed, the GET is read-only, bulk-applied flags never feed back into the count, the pipeline does not read the history, and storage adds no identity. Two majors and one minor-level test gap need fixing before the gate. The majors are the demo-isolation test gap (F1) and the shared git index that stages deletion of this card's files (F3). Suggestions only, no auto-dismiss, and no change to pipeline output or golden recall are all verified, not assumed.

Scope: commit f667f08 (`app/backend/dismissal_patterns.py`, `app/backend/api.py:497`, `tests/unit/test_dismissal_patterns.py`, the T-089 contract section in `memory/contracts/api.md`). Checked against D-042 in `memory/ORCHESTRATOR_DECISIONS.md` line 50.

**Checks against your three points**
1. Nothing auto-dismissed: holds. `suggest()` (`dismissal_patterns.py:51-72`) only reads. The GET route (`:92-99`) does not call `apply`. The POST route (`:101-114`) is the only writer, and it needs a key. Mutants 89e (suggest writes) and 89f (GET auto-applies) are both caught.
2. No effect on pipeline output or golden recall: holds. `pipeline.py` does not import `dismissal_patterns`. The golden identity test (`test_dismissal_patterns.py:116-134`) passes, and mutant 89i (history filters pipeline flags) is caught. Sensitivity is limited, see F4.
3. Storage local only, no user identity: holds. The module reads the existing `flags` table with no new column, table, or identity field. `grep -n "user|email|identity|account"` on the module returns only the docstring that says there are no users. Scope is case-only unless `ZLAYT_MODE=local`, mutant 89g is caught.

**Exercised**
- `python3 tools/board.py show T-089`; `git show f667f08` (stat and per-file); `git show f667f08:<path>` for in-scope files; D-042 in `memory/ORCHESTRATOR_DECISIONS.md`.
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: 151 passed, 1106 deselected. `pytest tests/unit/test_dismissal_patterns.py -v`: 17 passed (of 25 across both cards).
- Mutation suite in scratch copy `artifacts/review-evidence/T-088-T-089/mut` (runner `mutate.py`, output `mutation_run.txt`): 89a, 89c, 89e, 89f, 89g, 89i caught; 89b, 89d, 89d2, 89h not caught (see findings).
- `git diff --cached --name-status`; `git cat-file -e HEAD:<path>` (F3).
- `grep -rn dismissal app/frontend`: 0 matches (no banner built yet).

```json
{"card": "T-089", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f667f08: app/backend/dismissal_patterns.py, app/backend/api.py:497 (route registration), tests/unit/test_dismissal_patterns.py, memory/contracts/api.md (T-089 section); golden evals/golden/*.txt via G.case_names(); no live app URL (TestClient in-process)",
 "exercised": ["board.py show T-089 and T-088", "git show f667f08 --stat and per-file diffs", "git show f667f08:<path> for in-scope files", "memory/ORCHESTRATOR_DECISIONS.md D-042", "pytest -q tests/unit -k 'date or dismiss or suggest' (151 passed, 1106 deselected)", "pytest tests/unit/test_dismissal_patterns.py -v (17 passed)", "mutation suite 89a-89i incl. 89d2 in scratch copy (artifacts/review-evidence/T-088-T-089/mutation_run.txt)", "git diff --cached --name-status; git cat-file -e HEAD:<path>", "grep -rn dismissal app/frontend (0)", "grep for pipeline imports of dismissal_patterns (none)"],
 "verdict": "changes",
 "scores": {"never_auto_dismiss": 5, "no_pipeline_or_recall_effect": 4, "local_only_no_identity": 4, "demo_isolation_tested": 2, "tests_fail_on_mutation": 3, "ac_integrity": 3},
 "findings": [
  {"severity": "major",
   "title": "Demo-mode isolation at the route is not tested; forcing local scope in the route passes all 25 tests",
   "evidence": "app/backend/api.py:497 registers the route with local_mode=local_mode. Mutant 89h replaces it with local_mode=lambda: True in the scratch copy: '25 passed' (artifacts/review-evidence/T-088-T-089/mutation_run.txt, line 'MUTANT 89h ... NOT CAUGHT'). tests/unit/test_dismissal_patterns.py:94-113 (test_routes_and_demo_mode_isolation) creates one case only and seeds history in that case, so it cannot tell local from non-local scope. The unit test at :84-91 tests the function with local=True/False, not the route. memory/contracts/api.md (T-089 section) says 'a public/demo token never sees another case's dismissals'; the test named 'demo-mode isolation' does not assert that.",
   "why_it_matters": "The suggestion message counts dismissals in other cases ('all cases on this computer'). If the route's scope regresses, a public demo token would see phrase counts from other cases. The data is synthetic and the counts carry little content, so this is a test-coverage gap, not a live leak; the code today is correct. Depth on exposure belongs to security-reviewer. The card's AC evidence names a demo-isolation test that does not test isolation.",
   "fix": "Add a route test: create case A with 3 dismissals of a phrase and case B with the pending match, run without ZLAYT_MODE, and assert GET /api/cases/B/dismissal_suggestions returns suggestions == []. Then run with ZLAYT_MODE=local and assert the suggestion appears. Rename the test to describe what it asserts.",
   "acceptance_test": "Mutant 89h (local_mode forced True in api.py:497) must fail the new test. The unmodified route must pass it."},
  {"severity": "major",
   "title": "Shared git index stages deletion of this card's files (blast radius: T-088 and T-089)",
   "evidence": "git diff --cached --name-status: 'D app/backend/dismissal_patterns.py' and 'D tests/unit/test_dismissal_patterns.py' (plus the T-088 files and app/llm/prompts/conflicts_v1.md). git cat-file -e HEAD:app/backend/dismissal_patterns.py succeeds and the on-disk file matches HEAD (git show f667f08:<path> | diff: no output).",
   "why_it_matters": "HEAD is intact, so f667f08 itself is fine. The next commit made from this index deletes the T-089 module, its routes' code path and its tests, which is a silent loss of the deliverable.",
   "fix": "Orchestrator restores the index for these paths without touching the working tree, then commits with explicit paths. The reviewer does not run git reset.",
   "acceptance_test": "git diff --cached --name-status -- app/backend/dismissal_patterns.py tests/unit/test_dismissal_patterns.py prints nothing."},
  {"severity": "minor",
   "title": "Eligibility rules are tested only as a conjunction; neither the type rule nor the origin rule is isolated",
   "evidence": "app/backend/dismissal_patterns.py:22 (ELIGIBLE_TYPES) and :28 (origin must contain 'lexicon'). tests/unit/test_dismissal_patterns.py:49-50 builds the gap and record_warning flags with origin='code', so the origin check alone excludes them. Mutant 89d (gap added to ELIGIBLE_TYPES) and mutant 89d2 (origin requirement removed) both give '25 passed' (mutation_run.txt).",
   "why_it_matters": "The AC says 'ineligible types never offered'. Today a lexicon-origin gap flag would be offered for hiding if the type list were widened, and no test would notice.",
   "fix": "Add cases: a gap flag and a record_warning flag with origin 'lexicon+llm' (must not be suggested); a pre_existing flag with origin 'llm' only (must not be suggested).",
   "acceptance_test": "Mutants 89d and 89d2 must each fail a test."},
  {"severity": "minor",
   "title": "Category threshold boundary (CATEGORY_MIN) has no negative test; golden identity test seeds only one category",
   "evidence": "app/backend/dismissal_patterns.py:21 CATEGORY_MIN = 5. The category test (tests/unit/test_dismissal_patterns.py:54-63) only asserts the positive case at 5. Mutant 89b (CATEGORY_MIN = 4) gives '25 passed'. Also tests/unit/test_dismissal_patterns.py:15 defaults the seeded history to category 'new_onset'. Mutant 89i fails only the [sample] parametrization of the golden identity test (mutation_run.txt), so the other nine golden cases are not sensitive to history at all.",
   "why_it_matters": "The AC claim 'pipeline output identical on all golden cases with and without history' is true, but the test can only detect pipeline influence on flags of category new_onset. For the other nine cases it is a vacuous equality. The AC item also says 'eval shows no recall loss', and no eval report path exists; this unit equivalence test is the only evidence.",
   "fix": "Add a 4-dismissal negative case for the category rule. In the golden identity test, seed history with each case's own flag categories and phrases (taken from its pipeline output) so the equality is sensitive per case. Name the unit test as the recall evidence in the card, or add an eval report.",
   "acceptance_test": "Mutants 89b and 89i must each fail on at least one golden case other than sample."},
  {"severity": "minor",
   "title": "AC 'surface as a suggestion' is evidenced only by the API payload; the banner is not built",
   "evidence": "board show T-089, AC 1 done=true. Handoff: 'Left: frontend banner'. grep -rn dismissal app/frontend: 0 matches. The AC text does not name a UI element, so the API payload is the AC's surface.",
   "why_it_matters": "Acceptable for this AC as written, but the card's notes ask the frontend to show a banner with two buttons, and nothing in the card records that as a later AC. The surfacing will be lost unless a follow-up card tracks it.",
   "fix": "Create a follow-up frontend card for the banner, or add the banner to this card's AC before closing it.",
   "acceptance_test": "A UI test shows the banner after three dismissals, and flags stay unchanged until the 'Hide similar' click."},
  {"severity": "nit",
   "title": "apply() is not atomic across flags",
   "evidence": "app/backend/dismissal_patterns.py:86-87: the loop calls review.apply_review once per flag id with no transaction. A failure partway leaves earlier flags dismissed. Not reproduced; the flag ids come from pending flags and no test exercises a mid-loop failure.",
   "why_it_matters": "Low risk because each dismissal is individually logged and reversible with reset. Still a partial write with no explicit response.",
   "fix": "Wrap the loop in one transaction, or document the partial-write behaviour in api.md.",
   "acceptance_test": "A test that forces apply_review to raise on the second flag and asserts the first flag is not dismissed."}
 ],
 "whats_right": [
  "The GET path is read-only (mutant 89e, which writes on read, fails four tests; mutant 89f, which auto-applies on GET, fails the route test).",
  "Bulk-applied flags carry APPLIED_NOTE and are excluded from the count (dismissal_patterns.py:44); mutant 89c, which counts them, fails the self-reinforcement test.",
  "The pipeline does not import the module, and the history can change no pipeline output (mutant 89i is caught by the golden identity test)."
 ],
 "questions_for_chris": ["In local mode the suggestion counts dismissals across every case on the machine. Is that the intended single-profile scope, or should counts stay per case until a profile concept exists?"]}
```
---
id: "T-088"
title: "Date-convention suggestion (pre-select with stated reason, still one confirm)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:30:07Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:30:07Z"
rounds: 1
commits: ["f667f08"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-088-staff-engineer.md", "at": "2026-11-02T04:30:07Z"}
ac:
  - {"n": 1, "text": "For an ambiguous numeric date, the API suggests MM/DD or DD/MM with the reason (other dates in the packet), the UI pre-selects it, and the paralegal still confirms once; never auto-applied; eval case", "done": true, "evidence": "tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:36Z backend: UI needs: dates_to_confirm[].suggestion {convention, label, iso, reason, evidence, auto_applied:false} (contract in api.md). Pre-select the radio for suggestion.iso (when non-null), show reason beneath, still require an explicit confirm click (D-041); never confirm on load. Golden: evals/golden/case_01_date_formats should get a case asserting the 04/05/2026 record's suggestion is MM/DD with 4 evidence dates (qa owns golden; unit test tests/unit/test_date_convention.py covers it on that file today). No db change.
- 2026-11-02T04:21:36Z backend: AC 1 checked: tests/unit/test_date_convention.py (8 tests) pass: month-first/day-first/no-evidence/mixed evidence, golden case_01 suggestion, confirm still required, nothing written. UI pre-select is frontend's (see note)
- 2026-11-02T04:21:37Z backend: moved in_progress -> in_review
- 2026-11-02T04:21:41Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:30:07Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-088-staff-engineer.md; round 1; findings:
    - [blocker] Reason says the evidence dates are 'in this record' when they come from other records in the packet — fix: Build the reason from the evidence's own record ids, e.g. 'Other dates in this packet use month first (02/17/2026, record 2) and (03-17-26, record 6)'. Remove the phrase 'in this record' everywhere. Update the expected strings at test_date_convention.py:32, :46 and :99.
    - [major] AC 1 is marked done=true while two of its required parts are not in the codebase — fix: Set AC 1 back to done=false until (a) the frontend pre-select ships and (b) a golden expected entry for case_01 record 8 asserts the MDY suggestion. Or split those two parts into follow-up cards and close the unit half only.
    - [major] Shared git index stages deletion of this card's files (blast radius: T-088 and T-089) — fix: Orchestrator (not this reviewer) restores the index for the card paths without touching the working tree, then commits with explicit paths. The index then matches HEAD for these four files.
    - [minor] Weak assertion: `and`/`or` precedence lets the two-digit-year test pass with the wrong convention — fix: assert s["convention"] == "MDY" and (s["iso"] is None or s["iso"] in rows[1]["date_candidates"])
- 2026-11-02T04:30:07Z backend: claimed

## Handoff
Changed: new app/backend/date_convention.py (code only); present.dates_to_confirm adds suggestion; contract section in memory/contracts/api.md. Verified: .venv/bin/python -m pytest tests/unit/test_date_convention.py (8 pass); full unit run has 14 failures all in T-094 J3/conflict, reclassify and provider tests, none from this card. Left: frontend pre-select; qa golden case. Surprised: ambiguous dates within the record text also count as evidence, but dates in ISO form do not. Commit f667f08.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:15.094Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/agent-memory/backend/MEMORY.md"
}
````

### User / tool · 2026-11-02T04:30:15.099Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:17.486Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/project_backend_conventions.md; cat app/backend/date_convention.py; sed -n 1,120p tests/unit/test_date_convention.py; git status --short | head -20; git diff --cached --name-status | head"
}
````

### User / tool · 2026-11-02T04:30:17.631Z

**tool result**
````
---
name: backend-conventions
description: Codepaths, conventions and pitfalls for the deterministic backend modules and pipeline (T-032/033/037); read before touching ingest, amounts, gaps, conflicts, pipeline
metadata:
  type: project
---

Codepaths (app/backend): `ingest.py` (split/limits/dedupe/warnings, `ingest()` composite, `evidence_span`), `dates.py` (format list, 2-digit year >40 ambiguous per D-027), `amounts.py` (cents, classify, extract_amounts, rate_note), `totals.py`, `gaps.py`, `conflicts.py`, `flag_templates.py` (render with closed var whitelist + golden-subtype aliases), `lexicon.py` (loads app/llm/lexicon.yaml as data; deterministic modules must not import app.llm), `pipeline.py` (stages 0-7, `run_ingest`, `ingest_case`, `run_pipeline`, `run_case`, `judge_summary`, CLI). `app/pipeline.py` is a shim so `python -m app.pipeline` works (outside owned paths; flagged to orchestrator).

Conventions: money is int cents and amounts.py must not contain `float(`; text outside recognised record blocks becomes an `unsplit` record (never dropped; only exact `ingest.BANNERS` lines are set aside); a figure inside an injection hit has cents None; flag title/explanation only via flag_templates.render; code never sets review_status (pipeline items leave a run `pending`; `_persist` preserves existing review status on rerun).

Pitfalls: (1) the stage-and-commit rule: `git add` and `git commit` must be separate Bash calls (git-guard hook rejects a combined call), and commit with explicit pathspec `git commit -m ... -- <paths>`. (2) One sqlite3 connection shared by worker threads corrupts `PRAGMA table_info` reads; audited.py serialises writes with `_DB_LOCK`; do not use `:memory:` DBs with threads (CLI uses a temp file). (3) Fixture keys hash the full prompt, so any prompt/schema change in app/llm/prompts or judges invalidates tests/fixtures/llm: re-run `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record <golden .txt>` per case and `--judges`. (4) tests/unit/test_pipeline.py SEM script has `record_id` which schemas.FlagOutput forbids: the 3 j3 pipeline tests fail until T-036/qa reconcile.

Review findings to avoid repeating: silent text loss in splitters, silent century guesses, ACs ticked on REPL evidence without a named test.

T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).
"""Date-convention SUGGESTION for ambiguous numeric dates (T-088, D-042; code only, LLM_VS_CODE row 2). Never applied by itself.

An ambiguous record date such as 04/05/2026 has two code-proposed readings (MM/DD and DD/MM). This module looks at the OTHER numeric
dates in the same packet whose order is certain (one number above 12: 03/14/2026 is month first, 14/03/2026 is day first) and, when they
all agree, suggests that order with the reason stated in plain words and the dates it rests on. Mixed evidence or none: no suggestion.
The suggestion is a hint the UI pre-selects; the paralegal still confirms once through confirm_date (D-041), and confirm_date still only
accepts one of the code candidates. Nothing here writes to the database or changes a pipeline result."""
import re

from app.backend import dates

_NUM_DATE = re.compile(r"(?<![\d/.\-])(\d{1,2})([/.\-])(\d{1,2})\2(\d{4}|\d{2})(?![\d/.\-]\d)(?!\d)")
MAX_EVIDENCE = 2
_LABEL = {"MDY": "MM/DD", "DMY": "DD/MM"}


def _order(a: int, b: int):
    """MDY / DMY when the numbers prove the order, else None (both <= 12, or neither a valid month)."""
    if a > 12 and 1 <= b <= 12:
        return "DMY"
    if b > 12 and 1 <= a <= 12:
        return "MDY"
    return None


def _evidence(records, raw_text):
    """Unambiguous numeric dates in the packet, in record order: [{record_id, raw, order}]. Reads each record's date label and its text."""
    out, seen = [], set()
    for r in records:
        block = raw_text[r["char_start"]:r["char_end"]]
        for m in _NUM_DATE.finditer(block):
            order = _order(int(m[1]), int(m[3]))
            key = (r["id"], m[0])
            if order and key not in seen:
                seen.add(key)
                out.append({"record_id": r["id"], "raw": m[0], "order": order})
    return out


def _example(ev):
    return f"({ev['raw']})"


def suggest(rec: dict, records: list, raw_text: str):
    """Suggestion for one ambiguous record, or None. `rec` and `records` are record rows (id, date_raw, date_status, date_candidates,
    char_start, char_end). Returns {convention, label, iso, reason, evidence[]}; `iso` is None when the year is also ambiguous."""
    if rec.get("date_status") != "ambiguous":
        return None
    m = _NUM_DATE.fullmatch(" ".join(str(rec.get("date_raw") or "").split()))
    if not m or _order(int(m[1]), int(m[3])) is not None:
        return None
    ev = _evidence(records, raw_text)
    orders = {e["order"] for e in ev}
    if len(orders) != 1:
        return None                      # no evidence, or the packet mixes both orders: say nothing rather than guess
    order = next(iter(orders))
    a, b = int(m[1]), int(m[3])
    mo, d = (a, b) if order == "MDY" else (b, a)
    cands = [c for c in rec.get("date_candidates") or [] if int(c[5:7]) == mo and int(c[8:10]) == d]
    iso = cands[0] if len(cands) == 1 else None
    shown = ev[:MAX_EVIDENCE]
    n = len(ev)
    first = "month first" if order == "MDY" else "day first"
    reason = (f"Other dates in this record use {first} {_example(shown[0])}" if n == 1 else
              f"{n} other dates in this record use {first} " + " and ".join(_example(e) for e in shown))
    return {"convention": order, "label": _LABEL[order], "iso": iso, "reason": reason,
            "evidence": [{"record_id": e["record_id"], "raw": e["raw"]} for e in shown], "evidence_count": n, "auto_applied": False}
"""T-088: date-convention suggestion. Code only, never auto-applied, still one confirm (D-041/D-042)."""
import pytest
from fastapi.testclient import TestClient

from app.backend import date_convention as DC, present
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import run_case
from tests.unit.test_date_unconfirmed import snapshot


def packet(*dates_text):
    """records built from (date_raw, extra text) pairs; returns (rows, raw)."""
    raw, rows, pos = "", [], 0
    for i, (d, extra) in enumerate(dates_text, 1):
        block = f"Date: {d}\nNote: {extra}\n"
        p = dates.parse_date(d)
        rows.append({"id": f"r{i}", "date_raw": d, "date_status": p["status"], "date_candidates": p["candidates"],
                     "char_start": pos, "char_end": pos + len(block)})
        raw, pos = raw + block, pos + len(block)
    return rows, raw


from app.backend import dates   # noqa: E402


def test_month_first_evidence_suggests_mm_dd_with_reason():
    rows, raw = packet(("03/14/2026", "seen"), ("04/05/2026", "seen again"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "MDY" and s["label"] == "MM/DD" and s["iso"] == "2026-04-05"
    assert s["reason"] == "Other dates in this record use month first (03/14/2026)"
    assert s["evidence"] == [{"record_id": "r1", "raw": "03/14/2026"}] and s["auto_applied"] is False


def test_day_first_evidence_suggests_dd_mm():
    rows, raw = packet(("14/03/2026", "x"), ("04/05/2026", "y"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "DMY" and s["iso"] == "2026-05-04" and "day first (14/03/2026)" in s["reason"]


def test_evidence_inside_record_text_counts_and_is_listed_up_to_two():
    rows, raw = packet(("04/05/2026", "follow up on 06/25/2026 and 07/30/2026 and 08/31/2026"))
    s = DC.suggest(rows[0], rows, raw)
    assert s["convention"] == "MDY" and s["evidence_count"] == 3 and len(s["evidence"]) == 2
    assert s["reason"].startswith("3 other dates in this record use month first (06/25/2026) and (07/30/2026)")


def test_no_suggestion_without_evidence_or_with_mixed_evidence():
    rows, raw = packet(("04/05/2026", "alone"), ("06/07/2026", "also ambiguous"))
    assert DC.suggest(rows[0], rows, raw) is None
    rows, raw = packet(("03/14/2026", "a"), ("25/03/2026", "b"), ("04/05/2026", "c"))
    assert DC.suggest(rows[2], rows, raw) is None


def test_not_ambiguous_or_iso_dates_never_get_or_give_evidence():
    rows, raw = packet(("2026-03-14", "iso is not numeric-order evidence"), ("04/05/2026", "x"))
    assert DC.suggest(rows[1], rows, raw) is None
    assert DC.suggest(rows[0], rows, raw) is None        # a parsed record has no suggestion


def test_two_digit_year_ambiguity_keeps_convention_but_no_iso():
    rows, raw = packet(("03/14/2026", "x"), ("04/05/98", "y"))
    s = DC.suggest(rows[1], rows, raw)
    assert s["convention"] == "MDY" and s["iso"] is None or s["iso"] in rows[1]["date_candidates"]


def test_suggestion_never_writes_and_is_not_a_confirmation(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "x.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)))
    t = run_case(c, G.raw("case_01_date_formats"))
    before = snapshot(db, t)
    g = c.get(f"/api/cases/{t}").json()
    amb = [r for r in g["records"] if r["date_status"] == "ambiguous"]
    assert amb
    for item in g["dates_to_confirm"]:
        s = item.get("suggestion")
        if s:
            assert s["auto_applied"] is False and item["candidates"] and (s["iso"] is None or s["iso"] in item["candidates"])
    assert all(r["date_status"] == "ambiguous" for r in amb)        # nothing was confirmed by the suggestion
    assert snapshot(db, t) == before
    conn = DB.connect(db)
    assert not [e for e in DB.list_events(conn, t) if e["action"] == "confirm_date"]
    conn.close()


def test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "y.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)))
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    item = [d for d in g["dates_to_confirm"] if d["raw"] == "04/05/2026"][0]
    s = item["suggestion"]
    assert s["label"] == "MM/DD" and s["iso"] == "2026-04-05" and s["auto_applied"] is False
    assert s["evidence_count"] == 4 and s["reason"] == "4 other dates in this record use month first (02/17/2026) and (03-17-26)"
    assert item["status"] == "ambiguous"                     # still unconfirmed until the paralegal confirms
    assert c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
    r = c.post(f"/api/cases/{t}/records/{item['record_id']}/confirm_date", json={"date": "2026-04-05"})
    assert r.status_code == 200 and not [d for d in r.json()["dates_to_confirm"] if d["raw"] == "04/05/2026"]
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/confidence.py
 M app/backend/dates.py
 M app/backend/export.py
 M app/backend/flags.py
 M app/backend/generator.py
M	app/backend/present.py
D	app/llm/prompts/conflicts_v1.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:20.653Z

**tool call — Bash**
````
{
 "command": "sed -n 110,140p app/backend/present.py; grep -n \"record_id\\|\\\"id\\\"\\|ordinal\\|seq\" app/backend/ingest.py | head -20; cat evals/golden/case_01_date_formats.txt | head -60; ls evals/golden | head -30; sed -n 1,40p evals/golden/case_01_date_formats.expected.json"
}
````

### User / tool · 2026-11-02T04:30:20.768Z

**tool result**
````
    cnt = lambda sts: sum(1 for a in ch if a["review_status"] in sts)   # noqa: E731
    return {"accepted": {"cents": t["accepted_cents"], "count": cnt(("accepted", "edited")), "label": "Accepted charges"},
            "pending": {"cents": t["detected_pending_cents"], "count": cnt(("pending",)), "label": "Pending review"},
            "detected_not_a_total": {"cents": sum(a["value_cents"] for a in ch if a["review_status"] != "dismissed"),
                                     "count": sum(1 for a in ch if a["review_status"] != "dismissed"), "label": "Detected (not a total)"},
            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"]}


def review_view(conn, case_id):
    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
    live = [(k, r) for k, r in items if r["state"] != "rejected"]
    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
    rank = {"amount": 0, "entry": 1, "flag": 2}
    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
    return {"counts": counts, "queue": [r["id"] for _, r in pend],
            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}


def dates_to_confirm(conn, case_id):
    recs = list(_recs_by_id(conn, case_id).values())
    raw = DB.get_case(conn, case_id)["raw_text"]
    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
            for r in recs if r["date_status"] in ("ambiguous", "missing")]


def record_view(r, raw, with_sentences=True, pages=None):
    block = raw[r["char_start"]:r["char_end"]]
220:            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
319:        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
331:            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
342:        w["id"] = f"f_{ {'injection_suspected': 'inj', 'llm_split': 'split'}.get(w['category'], 'date') }_r{r['n']}"
350:            "injection_records": [r["id"] for r in recs if r["injection_tag"]]}
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-02-03
Source: Quillfeather Urgent Care
Excerpt: "Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care charge: $310.00."

=== Record 2 ===
Date: 02/17/2026
Source: Dr. Orla Pennywhistle, primary care
Excerpt: "Ankle swelling improved. Refer to physical therapy 1x/week for 4 weeks."

=== Record 3 ===
Date: Feb 24, 2026
Source: Pemberwick Physical Therapy, visit 1
Excerpt: "Gait mildly antalgic. Pain 4/10."

=== Record 4 ===
Date: 3 March 2026
Source: Pemberwick Physical Therapy, visit 2
Excerpt: "Pain 3/10. Balance exercises added."

=== Record 5 ===
Date: March 10th, 2026
Source: Pemberwick Physical Therapy, visit 3
Excerpt: "Pain 2/10. Walking without a limp."

=== Record 6 ===
Date: 03-17-26
Source: Pemberwick Physical Therapy, visit 4
Excerpt: "Pain 1/10. Discharged to home exercise program."

=== Record 7 ===
Date: 3/25/26
Source: Dr. Orla Pennywhistle, primary care
Excerpt: "Ankle exam normal. Optional recheck on 04/14/2026 if symptoms return."

=== Record 8 ===
Date: 04/05/2026
Source: Dr. Orla Pennywhistle, phone note
Excerpt: "Patient reports no new symptoms."

README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
{
  "schema_version": "golden/1",
  "case_id": "case_01_date_formats",
  "synthetic": true,
  "input_file": "case_01_date_formats.txt",
  "description": "Seven distinct date formats plus one genuinely ambiguous numeric date (04/05/2026: April 5 or May 4) on a phone note. Ambiguous date must be marked ambiguous, excluded from gap math, and surfaced for review. A future date inside an excerpt (04/14/2026) is not a record date.",
  "stress_types": [
    "date_format_variety",
    "ambiguous_date",
    "date_in_excerpt_trap",
    "no_flags_clean_case",
    "discharge_without_noncompliance"
  ],
  "records": [
    {
      "record_no": 1,
      "raw_date": "2026-02-03",
      "date": "2026-02-03",
      "kind": "encounter",
      "source": "Quillfeather Urgent Care"
    },
    {
      "record_no": 2,
      "raw_date": "02/17/2026",
      "date": "2026-02-17",
      "kind": "encounter",
      "source": "Dr. Orla Pennywhistle, primary care"
    },
    {
      "record_no": 3,
      "raw_date": "Feb 24, 2026",
      "date": "2026-02-24",
      "kind": "encounter",
      "source": "Pemberwick Physical Therapy, visit 1"
    },
    {
      "record_no": 4,
      "raw_date": "3 March 2026",
      "date": "2026-03-03",
      "kind": "encounter",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:23.973Z

**tool call — Bash**
````
{
 "command": "sed -n 312,322p app/backend/ingest.py; grep -n \"def _recs_by_id\" -A6 app/backend/present.py; grep -rn \"confirm_date\\|ZLAYT_MODE\\|local_mode\" app/backend/api.py | head -20; sed -n 85,140p app/backend/dismissal_patterns.py; sed -n 1,30p tests/unit/test_dismissal_patterns.py; sed -n 75,140p tests/unit/test_dismissal_patterns.py"
}
````

### User / tool · 2026-11-02T04:30:24.084Z

**tool result**
````
        warns.append(_warn("PHI_PATTERN", "Text looks like it contains an SSN, phone number or MRN. This tool is for synthetic data only."))
    for r in recs:
        p = dates.parse_date(r["date_raw"])
        kind = record_kind(r["source"], r["excerpt"])
        hits = [{**h, "field": "excerpt"} for h in injection.scan(r["excerpt"])] + \
               [{**h, "field": "source"} for h in injection.scan(r["source"])]
        rid = f"r{r['n']}"
        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
                 injection_tag=bool(hits), injection_hits=hits)
        if llm_split:
89:def _recs_by_id(conn, case_id):
90-    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
91-
92-
93-def item_view(conn, case_id, item_id):
94-    row = DB.get_item(conn, item_id, case_id)
95-    kind = _ID_KIND[item_id[0]]
app/backend/api.py:79:def local_mode() -> bool:
app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:101:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
app/backend/api.py:107:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:179:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
app/backend/api.py:220:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:230:        if not local_mode():
app/backend/api.py:240:            if not local_mode():
app/backend/api.py:411:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/api.py:412:    async def confirm_date(token: str, rid: str, request: Request):
app/backend/api.py:419:            return review.confirm_date(c, token, rid, b["date"])
app/backend/api.py:513:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
app/backend/api.py:544:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
app/backend/api.py:549:                return trace.item_trace(c, token, item_id, full=local_mode())
app/backend/api.py:560:            return trace.case_trace(c, token, full=local_mode())
app/backend/api.py:569:            return trace.judge_report(c, token, full=local_mode())
app/backend/api.py:578:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
        raise KeyError(key)
    for fid in s["flag_ids"]:
        review.apply_review(conn, case_id, fid, {"action": "dismiss", "note": APPLIED_NOTE}, now=now)
    return {"key": key, "dismissed_flag_ids": s["flag_ids"], "suggestions": suggest(conn, case_id, local=local)}


def add_routes(app, *, conn, get_case, body_of, ApiError, now, local_mode):
    @app.get("/api/cases/{token}/dismissal_suggestions")
    def dismissal_suggestions(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"suggestions": suggest(c, token, local=local_mode()), "min_phrase": PHRASE_MIN, "min_category": CATEGORY_MIN}
        finally:
            c.close()

    @app.post("/api/cases/{token}/dismissal_suggestions/apply")
    async def dismissal_suggestions_apply(token: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("key"), str):
            raise ApiError(400, "bad_request", "Send the key of the suggestion to apply.")
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply(c, token, b["key"], local=local_mode(), now=now)
            except KeyError:
                raise ApiError(404, "not_found", "That suggestion no longer applies.") from None
        finally:
            c.close()
"""T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output."""
import pytest
from fastapi.testclient import TestClient

from app.backend import dismissal_patterns as DP, pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record as wr
from tests.unit.test_review_rules import seeded

NEW_ONSET = "New onset pain radiating to right arm with numbness in fingers."


def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
                "evidence_json": [{"record_no": 1, "text": text, "start": 0, "end": len(text)}], "state": "verified", "state_reasons_json": []})
    if status:
        DB.apply_review(conn, fid, status, now=1.0, case=case)


def snapshot(conn, case):
    return [(f["id"], f["review_status"], f["state"]) for f in DB.list_items(conn, case, "flag")]


def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    before = snapshot(conn, cid)
    assert f["review_status"] == "dismissed" and f["reviewer_note"] == DP.APPLIED_NOTE
    assert len(DB.list_events(conn, cid)) == n_events + 1         # one logged dismiss event
    # a bulk-hidden flag is not a new manual dismissal: the count stays 3, not 4
    add_flag(conn, cid, "f_new")
    assert DP.suggest(conn, cid)[0]["dismissed_count"] == 3
    with pytest.raises(KeyError):
        DP.apply(conn, cid, "phrase:nope")


def test_scope_is_this_case_unless_local_profile(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    other = DB.create_case(conn, "x", now=1.0)
    for i in range(3):
        add_flag(conn, other, f"f_o{i}", status="dismiss")
    assert DP.suggest(conn, cid, local=False) == []
    s = DP.suggest(conn, cid, local=True)
    assert len(s) == 1 and s[0]["scope"] == "all cases on this computer"


def test_routes_and_demo_mode_isolation(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ZLAYT_MODE", raising=False)
    from tests.unit.test_api_routes import run_case
    db = str(tmp_path / "r.sqlite")
    c = TestClient(create_app(db, static_dir=str(tmp_path)))
    t = run_case(c)
    conn = DB.connect(db)
    for i in range(3):
        add_flag(conn, t, f"f_old{i}", status="dismiss")
    conn.close()
    r = c.get(f"/api/cases/{t}/dismissal_suggestions")
    assert r.status_code == 200 and r.json()["suggestions"][0]["dismissed_count"] == 3
    assert c.get("/api/cases/nope/dismissal_suggestions").status_code == 404
    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={}).status_code == 400
    assert c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": "phrase:zzz"}).status_code == 404
    key = r.json()["suggestions"][0]["key"]
    a = c.post(f"/api/cases/{t}/dismissal_suggestions/apply", json={"key": key})
    assert a.status_code == 200 and a.json()["dismissed_flag_ids"] and a.json()["suggestions"] == []


@pytest.mark.parametrize("case", G.case_names())
def test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):
    """Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts."""
    def run(seed_history):
        conn = DB.connect(str(tmp_path / f"{case}-{seed_history}.sqlite"))
        if seed_history:
            hist = DB.create_case(conn, "history", now=1.0)
            for i in range(8):
                add_flag(conn, hist, f"f_h{i}", status="dismiss")
        cid = DB.create_case(conn, G.raw(case), now=1.0)
        def extract(u):
            ex = G.record(case, wr(u, case)[0])["excerpt"].split(". ")[0].rstrip(".") + "."
            return dict(summary=ex, excerpt=ex)
        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script() if case == "sample" else sample_script(extract=extract)), now=lambda: 1.0)
        view = {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in ("entry", "amount", "flag")}
        DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either
        assert {k: [(i["id"], i.get("category"), i["state"], i["review_status"]) for i in DB.list_items(conn, cid, k)] for k in view} == view
        return view
    assert run(False) == run(True)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:30.430Z

**tool call — Bash**
````
{
 "command": "sed -n 1,84p app/backend/dismissal_patterns.py; sed -n 30,75p tests/unit/test_dismissal_patterns.py; grep -n \"def run_case\" -A12 tests/unit/test_api_routes.py; python3 tools/board.py show T-089 | sed -n 1,25p; grep -n \"T-089\" -B2 -A25 memory/contracts/api.md | head -60"
}
````

### User / tool · 2026-11-02T04:30:30.581Z

**tool result**
````
"""Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.

The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
the paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside
ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.

When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
may offer "You dismissed this kind of flag 4 times. Hide similar ones in this case?". This module only READS: suggest() never writes and
never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
PENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those
bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.

Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
that code or the model found without a lexicon phrase are never suggested for hiding."""
from fastapi import Request

from app.backend import lexicon_scan, review
from app.db import db as DB

PHRASE_MIN = 3
CATEGORY_MIN = 5
ELIGIBLE_TYPES = ("pre_existing", "causation")
APPLIED_NOTE = "Hidden by dismissal-pattern suggestion (paralegal confirmed)."
_BAD = ("rejected",)


def _eligible(f) -> bool:
    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")


def _phrase(f):
    """(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only."""
    for ev in f.get("evidence") or []:
        hits = [h for h in lexicon_scan.scan(ev.get("text") or "") if h["category"] == f["category"]]
        if hits:
            h = min(hits, key=lambda x: x["start"])
            return h["id"], " ".join(h["text"].lower().split())
    return None, None


def _history(conn, case_id: str, local: bool) -> list:
    """Dismissed, eligible flags that were dismissed by the paralegal one at a time."""
    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
    return [f for f in (DB._decode(r) for r in rows) if _eligible(f) and (f.get("reviewer_note") or "") != APPLIED_NOTE]


def _pending(conn, case_id: str) -> list:
    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]


def suggest(conn, case_id: str, *, local: bool = False) -> list:
    """Read-only. [{key, kind: phrase|category, label, dismissed_count, scope, flag_ids, message}], phrase suggestions first."""
    hist = _history(conn, case_id, local)
    phrase_n, cat_n = {}, {}
    for f in hist:
        pid, _ = _phrase(f)
        if pid:
            phrase_n[pid] = phrase_n.get(pid, 0) + 1
        cat_n[f["category"]] = cat_n.get(f["category"], 0) + 1
    out, covered = [], set()
    pend = [(f, *_phrase(f)) for f in _pending(conn, case_id)]
    scope = "all cases on this computer" if local else "this case"
    for pid in sorted({p for _, p, _ in pend if p and phrase_n.get(p, 0) >= PHRASE_MIN}):
        ids = [f["id"] for f, p, _ in pend if p == pid]
        label = next(t for _, p, t in pend if p == pid)
        out.append(_row(f"phrase:{pid}", "phrase", label, phrase_n[pid], scope, ids))
        covered.update(ids)
    for cat in sorted({f["category"] for f, _, _ in pend if cat_n.get(f["category"], 0) >= CATEGORY_MIN}):
        ids = [f["id"] for f, _, _ in pend if f["category"] == cat and f["id"] not in covered]
        if ids:
            out.append(_row(f"category:{cat}", "category", cat.replace("_", " "), cat_n[cat], scope, ids))
    return out


def _row(key, kind, label, n, scope, ids):
    return {"key": key, "kind": kind, "label": label, "dismissed_count": n, "scope": scope, "flag_ids": ids, "auto_applied": False,
            "message": f"You dismissed this kind of flag {n} times. Hide similar ones in this case?"}


def apply(conn, case_id: str, key: str, *, local: bool = False, now=None) -> dict:
    """The paralegal accepted the suggestion: dismiss the matching pending flags in THIS case through the normal review path.
    Raises KeyError when the key is not a current suggestion (nothing is written)."""
    s = next((x for x in suggest(conn, case_id, local=local) if x["key"] == key), None)
    if s is None:
    before = snapshot(conn, cid)
    s = DP.suggest(conn, cid)
    assert len(s) == 1 and s[0]["kind"] == "phrase" and s[0]["dismissed_count"] == 3 and s[0]["auto_applied"] is False
    assert s[0]["message"] == "You dismissed this kind of flag 3 times. Hide similar ones in this case?"
    assert "f_r7_2" in s[0]["flag_ids"]                           # the sample's pending new_onset flag
    assert snapshot(conn, cid) == before                          # suggest() wrote nothing; the flag is still pending
    assert next(f for f in DB.list_items(conn, cid, "flag") if f["id"] == "f_r7_2")["review_status"] == "pending"


def test_two_dismissals_are_not_enough(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(2):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_ineligible_flags_are_never_suggested(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(6):
        add_flag(conn, cid, f"f_g{i}", category="gap_over_30", type_="gap", origin="code", status="dismiss")
        add_flag(conn, cid, f"f_i{i}", category="injection_suspected", type_="record_warning", origin="code", status="dismiss")
    assert DP.suggest(conn, cid) == []


def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    texts = ["Pain began after the collision.", "Symptoms began after the accident.", "Onset after the fall.", "New onset of numbness.",
             "Developed pain after the accident."]
    for i, t in enumerate(texts):
        add_flag(conn, cid, f"f_c{i}", category="patient_report", text=t, status="dismiss")
    s = DP.suggest(conn, cid)
    cats = [x for x in s if x["kind"] == "category"]
    assert len(cats) == 1 and cats[0]["key"] == "category:patient_report" and cats[0]["dismissed_count"] == 5
    assert cats[0]["flag_ids"] == ["f_r9_1"] and cats[0]["label"] == "patient report"


def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
    conn, cid, _ = seeded(tmp_path)
    for i in range(3):
        add_flag(conn, cid, f"f_old{i}", status="dismiss")
    key = DP.suggest(conn, cid)[0]["key"]
    n_events = len(DB.list_events(conn, cid))
    out = DP.apply(conn, cid, key, now=2.0)
    assert out["dismissed_flag_ids"] == ["f_r7_2"] and out["suggestions"] == []
    f = next(x for x in DB.list_items(conn, cid, "flag") if x["id"] == "f_r7_2")
    assert f["review_status"] == "dismissed" and f["reviewer_note"] == DP.APPLIED_NOTE
34:def run_case(c, text=None):
35-    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
36-    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
37-    wait_ready(c, tok)
38-    return tok
39-
40-
41-def test_health_shape(env):
42-    h = env[1].get("/api/health").json()
43-    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
44-    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)
45-
46-
---
id: "T-089"
title: "Dismissal-pattern suggestions for a single local profile (suggestions only)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:30:07Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:30:07Z"
rounds: 1
commits: ["f667f08"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-089-staff-engineer.md", "at": "2026-11-02T04:30:07Z"}
ac:
  - {"n": 1, "text": "Repeated dismissals of the same flag phrase surface as a suggestion ('You dismissed this 4 times'); never auto-dismisses; per-profile local only; eval shows no recall loss on golden", "done": true, "evidence": "tests/unit/test_dismissal_patterns.py (17 pass): 3 dismissals -> suggestion, 2 -> none, apply only on click via review path, no self-reinforcement, ineligible types never offered, demo-mode isolation, pipeline output identical on all golden cases + sample with/without history (recall unchanged)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
22-| GET | `/api/cases/{token}/status` | stage and progress |
23-| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
24:| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
25:| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
26-| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
27-| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
28-| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
29-| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
30-| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
31-| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
32-| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected` |
33-| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
34-| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
35-| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
36-| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
37-| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
38-| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
39-| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
40-| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
41-
42----
43-
44-## GET /api/health
45-```json
46-{ "ok": true, "version": "0.1.0", "synthetic_only": true,
47-  "banner": "Synthetic data only — never paste real records",
48-  "backend": "fixture", "demo_mode": true, "live_enabled": false,
49-  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
50-  "limits": {"max_chars": 60000, "max_records": 40},
--
269-The suggestion changes nothing: the record stays `ambiguous`, its entry stays in `undated_entries`, and Accept stays blocked (D-041, `DATE_UNCONFIRMED`) until the paralegal confirms through `confirm_date`, which still accepts only a code candidate (`422 date_invalid` otherwise). **UI:** pre-select the radio for `suggestion.iso` (when not null), show `reason` under it, keep the confirm button enabled only on an explicit click, and let the paralegal pick the other reading freely. Do not confirm on load.
270-
271:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
272-Suggestions only (`app/backend/dismissal_patterns.py`). The tool has one local profile and no accounts, so "the profile" is this machine's database: the history is the set of flags the paralegal dismissed one at a time. Under `ZLAYT_MODE=local` it counts every case in the database; otherwise only this case (a public/demo token never sees another case's dismissals). Nothing new is stored. Only lexicon-phrase flags of type `pre_existing` or `causation` can be suggested; gap and conflict flags, injection and date warnings are never offered for hiding.
273-Response 200:
274-```json
275-{ "suggestions": [
276-    { "key": "phrase:new_onset", "kind": "phrase", "label": "new onset", "dismissed_count": 4, "scope": "all cases on this computer",
277-      "flag_ids": ["f_r7_2"], "auto_applied": false,
278-      "message": "You dismissed this kind of flag 4 times. Hide similar ones in this case?" } ],
279-  "min_phrase": 3, "min_category": 5 }
280-```
281-`kind` is `phrase` (same lexicon phrase group dismissed at least `min_phrase` times) or `category` (same category at least `min_category` times, listing only flags a phrase suggestion does not already cover). `flag_ids` are this case's still-**pending** flags that match. The list is empty when nothing qualifies. This GET is read-only and changes no flag, state or pipeline result.
282-
283-### POST /api/cases/{token}/dismissal_suggestions/apply
284-Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
285-
286-## GET /api/cases/{token}/items/{item_id}  — "Why?"
287-Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
288-```json
289-{ "item": { "id": "e4", "kind": "entry", "state": "needs_review", "reasons": ["JUDGE_PARTIAL"],
290-            "why": "The second check found part of the summary not supported by the quote.",
291-            "ladder": {"item_id": "e4", "state": "needs_review"} },
292-  "source": [ { "record_id": "r4", "char_start": 775, "char_end": 952, "highlight_start": 858, "highlight_end": 928 } ],
293-  "calls": [
294-    { "id": "c18", "role": "generator", "step": "extract", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5"},
295-      "model": "claude-sonnet-5-5", "prompt_version": "extract_v1", "prompt_sha256": "9f2c0a77", "attempt": 1,
296-      "latency_ms": 5120, "cost_usd": 0.0041, "tokens_in": 812, "tokens_out": 150, "parsed_ok": true, "verdict": null },
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:43.172Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/date_convention.py'\ns=open(p).read()\ns=s.replace(\"import re\\n\\nfrom app.backend import dates\\n\",\"import re\\n\")\ns=s.replace('''def _example(ev):\n    return f\"({ev['raw']})\"''','''def _example(ev):\n    \"\"\"'(Record 3: 03/14/2026)': names the record the date sits in, so the paralegal looks in the right place.\"\"\"\n    return f\"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})\"''')\ns=s.replace('''    reason = (f\"Other dates in this record use {first} {_example(shown[0])}\" if n == 1 else\n              f\"{n} other dates in this record use {first} \" + \" and \".join(_example(e) for e in shown))''','''    reason = (f\"Another date in this packet uses {first} {_example(shown[0])}\" if n == 1 else\n              f\"{n} other dates in this packet use {first} \" + \" and \".join(_example(e) for e in shown))''')\nopen(p,'w').write(s)\np='tests/unit/test_date_convention.py'\ns=open(p).read()\ns=s.replace('\"Other dates in this record use month first (03/14/2026)\"','\"Another date in this packet uses month first (Record 1: 03/14/2026)\"')\ns=s.replace('\"day first (14/03/2026)\" in s[\"reason\"]','\"day first (Record 1: 14/03/2026)\" in s[\"reason\"]')\ns=s.replace('startswith(\"3 other dates in this record use month first (06/25/2026) and (07/30/2026)\")','startswith(\"3 other dates in this packet use month first (Record 1: 06/25/2026) and (Record 1: 07/30/2026)\")')\ns=s.replace('s[\"convention\"] == \"MDY\" and s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"]','s[\"convention\"] == \"MDY\" and (s[\"iso\"] is None or s[\"iso\"] in rows[1][\"date_candidates\"])')\ns=s.replace('s[\"reason\"] == \"4 other dates in this record use month first (02/17/2026) and (03-17-26)\"','s[\"reason\"] == \"4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)\"')\ns+='''\n\ndef test_reason_names_the_record_each_date_sits_in_never_this_record(tmp_path, monkeypatch):\n    \"\"\"T-088 round 2: evidence dates in other records must not be described as 'in this record' (golden case_01, record 8).\"\"\"\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    c = TestClient(create_app(str(tmp_path / \"z.sqlite\"), static_dir=str(tmp_path)))\n    t = run_case(c, G.raw(\"case_01_date_formats\"))\n    g = c.get(f\"/api/cases/{t}\").json()\n    item = [d for d in g[\"dates_to_confirm\"] if d[\"raw\"] == \"04/05/2026\"][0]\n    s = item[\"suggestion\"]\n    assert item[\"record_id\"] == \"r8\" and \"this record\" not in s[\"reason\"]\n    assert \"other records\" not in s[\"reason\"] or \"Record\" in s[\"reason\"]\n    assert s[\"reason\"].count(\"Record \") == len(s[\"evidence\"]) == 2\n    for e in s[\"evidence\"]:\n        assert e[\"record_id\"] != \"r8\" and f\"(Record {e['record_id'][1:]}: {e['raw']})\" in s[\"reason\"]\n    # packet: month-first date in record 1, ambiguous date in record 2 -> the reason points at record 1\n    rows, raw = packet((\"03/14/2026\", \"seen\"), (\"04/05/2026\", \"seen again\"))\n    r = DC.suggest(rows[1], rows, raw)[\"reason\"]\n    assert \"Record 1\" in r and \"this record\" not in r and \"Record 2\" not in r\n'''\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_date_convention.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:30:44.998Z

**tool result**
````
.........                                                                [100%]
9 passed in 1.38s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:55.516Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_date_convention.py'\ns=open(p).read()\ns=s.replace('    assert \"other records\" not in s[\"reason\"] or \"Record\" in s[\"reason\"]\\n','')\nopen(p,'w').write(s)\n\np='tests/unit/test_dismissal_patterns.py'\ns=open(p).read()\nold_start=s.index(\"def test_routes_and_demo_mode_isolation\")\nold_end=s.index('@pytest.mark.parametrize(\"case\", G.case_names())')\nnew='''def _client(tmp_path, monkeypatch, name, mode=None):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    if mode:\n        monkeypatch.setenv(\"ZLAYT_MODE\", mode)\n    else:\n        monkeypatch.delenv(\"ZLAYT_MODE\", raising=False)\n    db = str(tmp_path / name)\n    return TestClient(create_app(db, static_dir=str(tmp_path))), db\n\n\ndef test_routes_apply_and_errors(tmp_path, monkeypatch):\n    from tests.unit.test_api_routes import run_case\n    c, db = _client(tmp_path, monkeypatch, \"r.sqlite\")\n    t = run_case(c)\n    conn = DB.connect(db)\n    for i in range(3):\n        add_flag(conn, t, f\"f_old{i}\", status=\"dismiss\")\n    conn.close()\n    r = c.get(f\"/api/cases/{t}/dismissal_suggestions\")\n    assert r.status_code == 200 and r.json()[\"suggestions\"][0][\"dismissed_count\"] == 3\n    assert c.get(\"/api/cases/nope/dismissal_suggestions\").status_code == 404\n    assert c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={}).status_code == 400\n    assert c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={\"key\": \"phrase:zzz\"}).status_code == 404\n    key = r.json()[\"suggestions\"][0][\"key\"]\n    a = c.post(f\"/api/cases/{t}/dismissal_suggestions/apply\", json={\"key\": key})\n    assert a.status_code == 200 and a.json()[\"dismissed_flag_ids\"] and a.json()[\"suggestions\"] == []\n\n\ndef _two_cases(c, db):\n    \"\"\"Case A holds three dismissals of a phrase; case B (a different token) holds only the pending match.\"\"\"\n    from tests.unit.test_api_routes import run_case\n    a, b = run_case(c), run_case(c)\n    assert a != b\n    conn = DB.connect(db)\n    for i in range(3):\n        add_flag(conn, a, f\"f_a_old{i}\", status=\"dismiss\")\n    add_flag(conn, b, \"f_b_pending\")\n    conn.close()\n    return a, b\n\n\ndef test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route(tmp_path, monkeypatch):\n    \"\"\"Demo/public mode: case B sees nothing from case A; apply refuses; a forced-local route (mutant) fails this test.\"\"\"\n    c, db = _client(tmp_path, monkeypatch, \"pub.sqlite\")\n    a, b = _two_cases(c, db)\n    assert c.get(f\"/api/cases/{b}/dismissal_suggestions\").json()[\"suggestions\"] == []\n    assert c.post(f\"/api/cases/{b}/dismissal_suggestions/apply\", json={\"key\": \"phrase:new_onset\"}).status_code == 404\n    pend = lambda: [f for f in DB.list_items(DB.connect(db), b, \"flag\") if f[\"id\"] == \"f_b_pending\"][0][\"review_status\"]   # noqa: E731\n    assert pend() == \"pending\"                                       # nothing was hidden in B by A's history\n    # case A's own history is still its own: B's flag is not in A, A has no pending match, so A gets none either\n    assert c.get(f\"/api/cases/{a}/dismissal_suggestions\").json()[\"suggestions\"] == []\n\n\ndef test_local_mode_counts_the_machine_profile_through_the_route(tmp_path, monkeypatch):\n    c, db = _client(tmp_path, monkeypatch, \"loc.sqlite\", mode=\"local\")\n    a, b = _two_cases(c, db)\n    s = c.get(f\"/api/cases/{b}/dismissal_suggestions\", headers={\"host\": \"127.0.0.1\"}).json()[\"suggestions\"]\n    assert len(s) == 1 and s[0][\"scope\"] == \"all cases on this computer\" and s[0][\"dismissed_count\"] == 3 and \"f_b_pending\" in s[0][\"flag_ids\"]\n\n\n'''\ns=s[:old_start]+new+s[old_end:]\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:30:58.733Z

**tool result**
````
           ^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

c = <starlette.testclient.TestClient object at 0x10a044f20>, text = None

    def run_case(c, text=None):
>       tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_api_routes.py:35: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_dismissal_patterns.py::test_public_demo_mode_cannot_reach_other_cases_dismissals_through_the_route
FAILED tests/unit/test_dismissal_patterns.py::test_local_mode_counts_the_machine_profile_through_the_route
2 failed, 17 passed in 2.73s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:01.043Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py -k public 2>&1 | grep -n \"429\\|rate\\|error\" | head; grep -n \"rate\\|RATE\" app/backend/api.py | head -20"
}
````

### User / tool · 2026-11-02T04:31:02.764Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:05.096Z

**tool call — Bash**
````
{
 "command": "cat > /tmp/x.py 2>/dev/null; .venv/bin/python - <<'EOF'\nimport os,tempfile\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ.pop(\"ANTHROPIC_API_KEY\",None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd=tempfile.mkdtemp()\nc=TestClient(create_app(d+\"/a.sqlite\",static_dir=d))\nfor i in range(2):\n    r=c.post(\"/api/cases\",json={\"sample\":True}); print(r.status_code,r.text[:300])\n    t=r.json().get(\"token\")\n    if t: print(c.post(f\"/api/cases/{t}/run\",json={}).status_code)\nEOF"
}
````

### User / tool · 2026-11-02T04:33:05.484Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b3otnolaa). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b3otnolaa.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:08.168Z

**tool call — Bash**
````
{
 "command": "sleep 5; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b3otnolaa.output; rm -f /tmp/x.py; cd /Users/arsis/zlayt-pm-project; grep -n \"429\\|too_many\\|per_ip\\|MAX_CASES\\|case_limit\\|rate_limit\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T04:33:13.280Z

**tool result**
````
app/backend/pdf_checks.py:18:    "ocr_too_many_pages": f"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.",
app/backend/pdf_checks.py:67:                raise PdfError("ocr_too_many_pages", {"scanned_pages": len(scan_pages), "max": pdf_ocr.MAX_OCR_PAGES})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:17.987Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py -k public 2>&1 | grep -n \"Error\\|assert\\|^E\" | head; grep -n \"def create_case\\|\\\"/api/cases\\\"\" -A14 app/backend/api.py | head -50"
}
````

### User / tool · 2026-11-02T04:33:19.600Z

**tool result**
````
12:        assert c.get(f"/api/cases/{b}/dismissal_suggestions").json()["suggestions"] == []
13:        assert c.post(f"/api/cases/{b}/dismissal_suggestions/apply", json={"key": "phrase:new_onset"}).status_code == 404
15:        assert pend() == "pending"                                       # nothing was hidden in B by A's history
17:>       assert c.get(f"/api/cases/{a}/dismissal_suggestions").json()["suggestions"] == []
18:E       AssertionError: assert [{'key': 'phr...unt': 3, ...}] == []
19:E         
20:E         Left contains one more item: {'key': 'phrase:new_onset', 'kind': 'phrase', 'label': 'new onset', 'dismissed_count': 3, ...}
21:E         Use -v to get more diff
23:tests/unit/test_dismissal_patterns.py:145: AssertionError
218:    @app.get("/api/cases")
219-    def list_cases():
220-        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
221-            raise ApiError(404, "not_found", "Not found.")
222-        c = conn()
223-        try:
224-            return {"cases": present.case_list(c)}
225-        finally:
226-            c.close()
227-
228-    @app.get("/api/library")
229-    def library():
230-        if not local_mode():
231-            raise ApiError(404, "not_found", "Not found.")
232-        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
--
234:    @app.post("/api/cases", status_code=201)
235:    async def create_case(request: Request):
236-        b = await body_of(request)
237-        sample = b.get("sample") is True
238-        lib = None
239-        if isinstance(b.get("library"), str):
240-            if not local_mode():
241-                raise ApiError(404, "not_found", "Not found.")
242-            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
243-            if lib is None:
244-                raise ApiError(404, "not_found", "No such library case.")
245-        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
246-        if not isinstance(text, str):
247-            raise ApiError(400, "bad_request", "Provide text or sample: true.")
248-        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
249-
--
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
252-        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
253-        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
254-        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
255-            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
256-        cl = request.headers.get("content-length")
257-        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
258-            raise ApiError(413, "input_too_large", "The PDF is too large.")
259-        data = b""
260-        async for chunk in request.stream():
261-            data += chunk
262-            if len(data) > pdf_text.MAX_PDF_BYTES:
263-                raise ApiError(413, "input_too_large", "The PDF is too large.")
264-        opts = {}
265-        if (ocr or "").lower() in ("1", "true", "yes"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:22.902Z

**tool call — Bash**
````
{
 "command": "grep -rn \"ZLAYT_MODE.*local\" tests/unit/*.py | head -8; grep -n \"client=\\|TestClient(.*client\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T04:33:23.011Z

**tool result**
````
tests/unit/test_api_routes.py:263:    """T-040 AC (T-051 privacy): public/demo audit has no prompt, response, record or edit text; ZLAYT_MODE=local adds them."""
tests/unit/test_api_routes.py:273:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:285:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:298:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:314:    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", host)
tests/unit/test_api_routes.py:335:    monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.setenv("HOST", "127.0.0.1")
tests/unit/test_api_routes.py:342:    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.delenv("HOST", raising=False)
tests/unit/test_billing.py:279:    monkeypatch.setenv("ZLAYT_MODE", "local")
tests/unit/test_api_routes.py:21:    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)
tests/unit/test_api_routes.py:345:        assert TestClient(app, client=(peer, 5000)).get("/api/cases").status_code == 200, peer
tests/unit/test_api_routes.py:347:        r = TestClient(app, client=(peer, 5000)).get("/api/cases")
tests/unit/test_api_routes.py:349:        assert TestClient(app, client=(peer, 5000)).get("/api/health").status_code == 403
tests/unit/test_api_routes.py:351:    assert TestClient(app, client=("192.168.1.5", 5000)).get("/api/health").status_code == 200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:38.585Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_dismissal_patterns.py'\ns=open(p).read()\ns=s.replace('return TestClient(create_app(db, static_dir=str(tmp_path))), db','return TestClient(create_app(db, static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000)), db')\ns=s.replace('''    # case A's own history is still its own: B's flag is not in A, A has no pending match, so A gets none either\n    assert c.get(f\"/api/cases/{a}/dismissal_suggestions\").json()[\"suggestions\"] == []\n''','''    own = c.get(f\"/api/cases/{a}/dismissal_suggestions\").json()[\"suggestions\"]       # A's own history still counts for A, scoped to A\n    assert len(own) == 1 and own[0][\"scope\"] == \"this case\" and \"f_b_pending\" not in own[0][\"flag_ids\"]\n''')\ns=s.replace(', headers={\"host\": \"127.0.0.1\"}','')\n# golden sensitivity\ni=s.index('@pytest.mark.parametrize(\"case\", G.case_names())')\ns=s[:i]+'''@pytest.mark.parametrize(\"case\", G.case_names())\ndef test_suggestions_never_change_pipeline_output_so_golden_recall_is_unchanged(tmp_path, case):\n    \"\"\"Same case through the pipeline with and without a dismissal history in the database: identical flags, entries and amounts.\n    The history is built from the case's OWN flags (same type, category, origin and quoted phrase, 8 dismissals each), so a pipeline that\n    let history filter flags would change this case's output; a case with no eligible flag also gets the generic new_onset history.\"\"\"\n    def run(history_from):\n        conn = DB.connect(str(tmp_path / f\"{case}-{bool(history_from)}.sqlite\"))\n        if history_from is not None:\n            hist = DB.create_case(conn, \"history\", now=1.0)\n            for n, f in enumerate(history_from * 8 or [None]):\n                if f is None:\n                    add_flag(conn, hist, f\"f_h{n}\", status=\"dismiss\")\n                else:\n                    add_flag(conn, hist, f\"f_h{n}\", category=f[\"category\"], text=f[\"evidence\"][0][\"text\"], type_=f[\"type\"], origin=f[\"origin\"], status=\"dismiss\")\n        cid = DB.create_case(conn, G.raw(case), now=1.0)\n        def extract(u):\n            ex = G.record(case, wr(u, case)[0])[\"excerpt\"].split(\". \")[0].rstrip(\".\") + \".\"\n            return dict(summary=ex, excerpt=ex)\n        PL.run_pipeline(conn, cid, G.raw(case), call=FakeCall(sample_script() if case == \"sample\" else sample_script(extract=extract)), now=lambda: 1.0)\n        view = {k: [(i[\"id\"], i.get(\"category\"), i[\"state\"], i[\"review_status\"]) for i in DB.list_items(conn, cid, k)] for k in (\"entry\", \"amount\", \"flag\")}\n        DP.suggest(conn, cid, local=True)                          # computing suggestions after the run must not matter either\n        assert {k: [(i[\"id\"], i.get(\"category\"), i[\"state\"], i[\"review_status\"]) for i in DB.list_items(conn, cid, k)] for k in view} == view\n        flags = [f for f in DB.list_items(conn, cid, \"flag\") if DP._eligible(f) and f.get(\"evidence\")]\n        return view, flags\n    base, flags = run(None)\n    seeded_view, _ = run(flags)\n    assert base == seeded_view\n    assert flags or case in G.case_names()                          # cases without an eligible flag use the generic history below\n    assert base == run([])[0]\n\n\ndef test_eligibility_rules_are_each_enforced_on_their_own(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    for i in range(6):\n        add_flag(conn, cid, f\"f_gl{i}\", category=\"gap_over_30\", type_=\"gap\", origin=\"lexicon+llm\", status=\"dismiss\")      # right origin, wrong type\n        add_flag(conn, cid, f\"f_rw{i}\", category=\"new_onset\", type_=\"record_warning\", origin=\"lexicon+llm\", status=\"dismiss\")\n        add_flag(conn, cid, f\"f_llm{i}\", category=\"new_onset\", type_=\"pre_existing\", origin=\"llm\", status=\"dismiss\")          # right type, no lexicon\n    assert DP.suggest(conn, cid) == []\n    add_flag(conn, cid, \"f_ok\", type_=\"pre_existing\", origin=\"lexicon\", status=None)\n    assert DP.suggest(conn, cid) == []                              # ineligible history never counts toward an eligible pending flag\n\n\ndef test_category_threshold_is_exactly_five(tmp_path):\n    conn, cid, _ = seeded(tmp_path)\n    texts = [\"Pain began after the collision.\", \"Symptoms began after the accident.\", \"Onset after the fall.\", \"New onset of numbness.\"]\n    for i, t in enumerate(texts):\n        add_flag(conn, cid, f\"f_c{i}\", category=\"patient_report\", text=t, status=\"dismiss\")\n    assert [x for x in DP.suggest(conn, cid) if x[\"kind\"] == \"category\"] == []             # 4 is not enough\n    add_flag(conn, cid, \"f_c4\", category=\"patient_report\", text=\"Developed pain after the accident.\", status=\"dismiss\")\n    assert [x[\"dismissed_count\"] for x in DP.suggest(conn, cid) if x[\"kind\"] == \"category\"] == [5]\n'''\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_dismissal_patterns.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:33:42.238Z

**tool result**
````
.....................                                                    [100%]
21 passed in 3.19s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:47.679Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_dismissal_patterns.py'\ns=open(p).read()\ns=s.replace(\"    assert flags or case in G.case_names()                          # cases without an eligible flag use the generic history below\\n\",\"\")\nopen(p,'w').write(s)\nEOF\nmut(){ f=$1; a=$2; b=$3; k=$4; cp $f /tmp/bk_mut; python3 - \"$f\" \"$a\" \"$b\" <<'EOF'\nimport sys\nf,a,b=sys.argv[1:]\ns=open(f).read(); assert a in s; open(f,'w').write(s.replace(a,b,1))\nEOF\nr=$(.venv/bin/python -m pytest -q -x tests/unit/test_dismissal_patterns.py tests/unit/test_date_convention.py 2>&1 | tail -1); cp /tmp/bk_mut $f; echo \"$k: $r\"; }\nmut app/backend/api.py \"local_mode=local_mode)   # T-089\" \"local_mode=lambda: True)   # T-089\" forced_local\nmut app/backend/dismissal_patterns.py \"CATEGORY_MIN = 5\" \"CATEGORY_MIN = 4\" cat4\nmut app/backend/dismissal_patterns.py 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\")' 'ELIGIBLE_TYPES = (\"pre_existing\", \"causation\", \"gap\", \"record_warning\")' types\nmut app/backend/dismissal_patterns.py \"and \\\"lexicon\\\" in (f.get(\\\"origin\\\") or \\\"\\\")\" \"\" origin\nmut app/backend/date_convention.py \"(Record {str(ev['record_id']).lstrip('r')}: {ev['raw']})\" \"({ev['raw']})\" reason_old\nrm -f /tmp/bk_mut; git diff --stat app/backend/api.py | tail -1\n.venv/bin/python -m pytest -q tests/unit -k \"date or dismiss or suggest\" 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:34:13.922Z

**tool result**
````
forced_local: 1 failed, 7 passed in 2.02s
cat4: 1 failed, 20 passed in 2.95s
types: 1 failed, 19 passed in 3.40s
origin: 1 failed, 19 passed in 3.33s
reason_old: 1 failed, 21 passed in 3.57s
 1 file changed, 25 insertions(+), 11 deletions(-)
........................................................................ [ 90%]
................                                                         [100%]
160 passed, 1210 deselected in 8.50s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:16.761Z

**tool call — Bash**
````
{
 "command": "grep -n \"in this record\\|other dates\" memory/contracts/api.md app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T04:34:16.855Z

**tool result**
````
memory/contracts/api.md:264:                  "reason": "Other dates in this record use month first (03/14/2026)",
memory/contracts/api.md:267:`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Other dates in this record use month first (03/14/2026)"; several read "4 other dates in this record use month first (02/17/2026) and (03-17-26)" (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
app/backend/date_convention.py:64:              f"{n} other dates in this packet use {first} " + " and ".join(_example(e) for e in shown))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:21.180Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\ns=s.replace('\"reason\": \"Other dates in this record use month first (03/14/2026)\"','\"reason\": \"Another date in this packet uses month first (Record 1: 03/14/2026)\"')\ns=s.replace('one date reads \"Other dates in this record use month first (03/14/2026)\"; several read \"4 other dates in this record use month first (02/17/2026) and (03-17-26)\"','one date reads \"Another date in this packet uses month first (Record 1: 03/14/2026)\"; several read \"4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)\" (each example names the record the date sits in; the evidence dates come from the packet, never described as \"in this record\")')\ns=s.replace(\"Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.\",\"Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed (reversible with `reset`); the response is then an error and the refreshed list shows what remains.\")\nopen(p,'w').write(s)\nEOF\ngit add -n app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md; git ls-files app/backend/date_convention.py tests/unit/test_dismissal_patterns.py; git diff --stat HEAD -- memory/contracts/api.md app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py app/backend/dismissal_patterns.py | tail -6"
}
````

### User / tool · 2026-11-02T04:34:21.341Z

**tool result**
````
add 'app/backend/date_convention.py'
add 'memory/contracts/api.md'
add 'tests/unit/test_date_convention.py'
add 'tests/unit/test_dismissal_patterns.py'
app/backend/date_convention.py
tests/unit/test_dismissal_patterns.py
 app/backend/date_convention.py        |  9 ++--
 memory/contracts/api.md               | 13 ++---
 tests/unit/test_date_convention.py    | 29 +++++++++--
 tests/unit/test_dismissal_patterns.py | 93 ++++++++++++++++++++++++++++++-----
 4 files changed, 116 insertions(+), 28 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:25.287Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- memory/contracts/api.md | grep '^[+-]' | cut -c1-140"
}
````

### User / tool · 2026-11-02T04:34:25.392Z

**tool result**
````
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
+| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), tota
-## POST /api/cases/{token}/review/batch (D-031)
+## POST /api/cases/{token}/review/batch (D-031)
-                  "reason": "Other dates in this record use month first (03/14/2026)",
+                  "reason": "Another date in this packet uses month first (Record 1: 03/14/2026)",
-`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambi
+`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambi
-Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in 
+Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in 
-## DELETE /api/cases/{token}
+## DELETE /api/cases/{token}
-| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
+| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:29.204Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u) && git read-tree HEAD && git add app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md && git diff --cached --name-status && git commit -q -m \"fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log -1 --format=%h; unset GIT_INDEX_FILE; git diff --cached --name-status | head -5"
}
````

### User / tool · 2026-11-02T04:34:29.295Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u) && git read-tree HEAD && git add app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md && g
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:31.304Z

**tool call — Bash**
````
{
 "command": "IDX=$(mktemp -u /private/tmp/claude-501/idx.XXXXXX); echo $IDX > /private/tmp/claude-501/idxpath; GIT_INDEX_FILE=$IDX git read-tree HEAD && GIT_INDEX_FILE=$IDX git add app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md && GIT_INDEX_FILE=$IDX git diff --cached --name-status"
}
````

### User / tool · 2026-11-02T04:34:31.455Z

**tool result**
````
M	app/backend/date_convention.py
M	memory/contracts/api.md
M	tests/unit/test_date_convention.py
M	tests/unit/test_dismissal_patterns.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:33.320Z

**tool call — Bash**
````
{
 "command": "IDX=$(cat /private/tmp/claude-501/idxpath); GIT_INDEX_FILE=$IDX git commit -q -m \"fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"; git log -1 --format=%h; rm -f $IDX; git diff --cached --name-status | head"
}
````

### User / tool · 2026-11-02T04:34:33.392Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion ($) is blocked | command: IDX=$(cat /private/tmp/claude-501/idxpath); GIT_INDEX_FILE=$IDX git commit -q -m "fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility 
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:35.161Z

**tool call — Bash**
````
{
 "command": "IDX=$(cat /private/tmp/claude-501/idxpath); GIT_INDEX_FILE=$IDX git commit -q -m \"fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"; git log -1 --format='%h %s'; git diff --cached --name-status | head"
}
````

### User / tool · 2026-11-02T04:34:35.557Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
55300e9 fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
M	app/backend/api.py
M	app/backend/confidence.py
M	app/backend/date_convention.py
M	app/backend/dates.py
M	app/backend/export.py
M	app/backend/generator.py
D	app/backend/language.py
M	app/backend/narrative.py
D	app/backend/pdf_checks.py
D	app/backend/pdf_hidden.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:44.152Z

**tool call — Bash**
````
{
 "command": "git restore --staged app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py memory/contracts/api.md app/backend/dismissal_patterns.py 2>&1 | tail -2; git diff --cached --name-only -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit memory/contracts/api.md\nB=\"python3 tools/board.py\"\n$B note T-088 --agent backend --text \"Round 2 (commit 55300e9): reason now names where each evidence date sits, e.g. golden case_01 record 8: '4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)'; 'in this record' removed everywhere; and/or precedence fixed; unused import removed. Tests: tests/unit/test_date_convention.py (9 pass; reason-names-record test is mutation-checked: old wording fails it). AC1 CORRECTION: the earlier AC1 evidence overstated. Only the API/unit half is done. NOT done: (a) UI pre-select, now card T-096 (frontend); (b) eval case. For qa: add to evals/golden/case_01_date_formats.expected.json an assertion that the dates_to_confirm item for record r8 (raw 04/05/2026) has suggestion.convention=MDY, label 'MM/DD', iso '2026-04-05', evidence_count 4, evidence record_ids [r2, r6], auto_applied false, and status stays 'ambiguous' until confirm_date. Until qa adds it, tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required is the stand-in.\"\n$B ac T-088 --check 1 --agent backend --evidence \"PARTIAL, corrected: backend half only. tests/unit/test_date_convention.py (9 pass) incl. golden case_01 reason naming Record 2 and Record 6. NOT done: UI pre-select (T-096, frontend) and the golden expected.json eval entry (qa; exact assertion in the note above)\" 2>&1 | tail -2\n$B handoff T-088 --agent backend --text \"Changed: reason names the record of each evidence date (Record N: raw), never 'in this record'; test precedence fix; unused import; api.md updated. Verified: .venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass); mutants restoring old wording fail. Left: UI pre-select (T-096), golden expected entry (qa, see note). Surprised: the earlier AC1 tick overstated; corrected in the note. Commit 55300e9.\"\n$B commit T-088 --sha 55300e9 --agent backend 2>&1 | tail -1\n$B move T-088 in_review --agent backend 2>&1 | tail -1"
}
````

### User / tool · 2026-11-02T04:34:44.213Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not checkout/restore board/ or memory/ files
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:45.920Z

**tool call — Bash**
````
{
 "command": "git restore --staged app/backend/date_convention.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py app/backend/dismissal_patterns.py 2>&1 | tail -2; git diff --cached --name-only | grep -c \"date_convention\\|dismissal\\|api.md\""
}
````

### User / tool · 2026-11-02T04:34:46.054Z

**tool result**
````
1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:55.433Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B note T-088 --agent backend --text \"Round 2 (commit 55300e9): reason now names where each evidence date sits, e.g. golden case_01 record 8: '4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)'; 'in this record' removed everywhere; and/or precedence fixed; unused import removed. Tests: tests/unit/test_date_convention.py (9 pass; reason-names-record test mutation-checked: old wording fails it). AC1 CORRECTION: the earlier AC1 evidence overstated. Only the API/unit half is done. NOT done: (a) UI pre-select, now card T-096 (frontend); (b) eval case. For qa: add to evals/golden/case_01_date_formats.expected.json an assertion that the dates_to_confirm item for record r8 (raw 04/05/2026) has suggestion.convention=MDY, label 'MM/DD', iso '2026-04-05', evidence_count 4, evidence record_ids [r2, r6], auto_applied false, and status stays 'ambiguous' until confirm_date. Until qa adds it, tests/unit/test_date_convention.py::test_golden_case_01_gets_month_first_suggestion_and_confirm_still_required is the stand-in.\" 2>&1 | tail -1\n$B ac T-088 --check 1 --agent backend --evidence \"PARTIAL, corrected: backend half only. tests/unit/test_date_convention.py (9 pass) incl. golden case_01 reason naming Record 2 and Record 6. NOT done: UI pre-select (T-096, frontend) and golden expected.json eval entry (qa; exact assertion in the note)\" 2>&1 | tail -1\n$B handoff T-088 --agent backend --text \"Changed: reason names the record of each evidence date (Record N: raw), never 'in this record'; test precedence fix; unused import; api.md updated. Verified: .venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass); mutant restoring old wording fails. Left: UI pre-select (T-096), golden expected entry (qa, see note). Surprised: earlier AC1 tick overstated; corrected in note. Commit 55300e9.\" 2>&1 | tail -1\n$B commit T-088 --sha 55300e9 --agent backend 2>&1 | tail -1\n$B move T-088 in_review --agent backend 2>&1 | tail -1\n$B note T-089 --agent backend --text \"Round 2 (commit 55300e9): added route-level demo-isolation tests (public mode: case B gets no suggestions from case A's dismissals, apply 404, B's flag stays pending; local mode: counts the machine profile). Mutants verified failing: route forced local (89h), CATEGORY_MIN=4 (89b), gap/record_warning eligible (89d), lexicon-origin requirement removed (89d2). Golden identity test now seeds each case's own flags as history (sensitive per case). Apply non-atomicity documented in api.md. Frontend banner: no follow-up card is mine to create; orchestrator/frontend to track (api.md has the UI notes).\" 2>&1 | tail -1\n$B ac T-089 --check 1 --agent backend --evidence \"tests/unit/test_dismissal_patterns.py (21 pass): suggestion thresholds incl. category 4 vs 5, each eligibility rule alone, route-level public-mode isolation (forced-local mutant fails), local-mode profile, apply via review path, golden identity with per-case history. Recall evidence is this unit equivalence test (no eval report). Banner UI not built (frontend)\" 2>&1 | tail -1\n$B handoff T-089 --agent backend --text \"Changed: route-level demo/public isolation test + local-mode route test; isolated eligibility (type, origin) and category-threshold tests; golden identity test seeds each case's own flags; apply partial-write documented. Verified: pytest -k 'date or dismiss or suggest' (160 pass); mutants 89b/89d/89d2/89h now fail. Left: frontend banner card. Surprised: sample case has its own pending match so case A gets a suggestion scoped to itself. Commit 55300e9.\" 2>&1 | tail -1\n$B commit T-089 --sha 55300e9 --agent backend 2>&1 | tail -1\n$B move T-089 in_review --agent backend 2>&1 | tail -1"
}
````

### User / tool · 2026-11-02T04:34:56.045Z

**tool result**
````
noted on T-088
AC 1 checked: PARTIAL, corrected: backend half only. tests/unit/test_date_convention.py (9 pass) incl. golden case_01 reason naming Record 2 and Record 6. NOT done: UI pre-select (T-096, frontend) and golden expected.json eval entry (qa; exact assertion in the note)
handoff written on T-088
T-088: commit 55300e9 recorded
T-088: in_progress -> in_review
noted on T-089
AC 1 checked: tests/unit/test_dismissal_patterns.py (21 pass): suggestion thresholds incl. category 4 vs 5, each eligibility rule alone, route-level public-mode isolation (forced-local mutant fails), local-mode profile, apply via review path, golden identity with per-case history. Recall evidence is this unit equivalence test (no eval report). Banner UI not built (frontend)
handoff written on T-089
T-089: commit 55300e9 recorded
T-089: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:59.354Z

T-088 and T-089 are both in `in_review`, committed as 55300e9. `pytest -k "date or dismiss or suggest"` passes (160).

- **T-088:** the reason now reads "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)" on golden case_01 record 8, and a new test covers that case. I posted an AC1 correction, saying only the backend half is done. I also noted the exact golden assertion for qa to add and pointed the UI half at T-096. I fixed the other review minors too.
- **T-089:** new route-level tests show a public-mode case sees nothing from another case's dismissals, and a forced-local route fails them. I also fixed the review's minors (eligibility, category threshold, golden-history sensitivity).

The shared index still has stale staged entries from other agents, including `memory/contracts/api.md`. The board-guard hook blocked me from unstaging that file, so please unstage it.
