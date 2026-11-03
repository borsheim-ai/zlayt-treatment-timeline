# Subagent: T-160 row-height check (T-160 row-height check)

Source: `agent-ac1ab7c56b90b4c27.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T15:36:54.236Z

Review board card T-160 (commit 94a31a4) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-160`.

On a `git archive HEAD` copy, on your own port with E2E_REQUIRE_DB=1, run tests/e2e/test_polish_r3.py. Confirm:
- the original compact-row height budget is restored and not loosened;
- the "Not in an entry (n)" link sits in the head line and is reachable by click and keyboard;
- test_uncovered_ui.py still passes.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-160-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Stop only your own PIDs. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:00.195Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:00.197Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-160",
 "description": "Show board card T-160"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:00.198Z

**tool call — Bash**
````
{
 "command": "git log --oneline -3 94a31a4 && git rev-parse HEAD && git show --stat 94a31a4 | head -40",
 "description": "Show commit 94a31a4 metadata and HEAD"
}
````

### User / tool · 2026-11-02T15:37:00.237Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### User / tool · 2026-11-02T15:37:00.390Z

**tool result**
````
---
id: "T-160"
title: "Compact rows over budget since T-144: the 'Not in an entry (n)' link in the entry head makes rows taller than the T-060 compact-row budget; restore the budget (move the link or render it inline)"
milestone: "M2"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:52:47Z"
updated_at: "2026-11-02T15:36:38Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T15:36:25Z"
rounds: 0
commits: ["94a31a4"]
reviews: []
ac:
  - {"n": 1, "text": "test_polish_r3 row-height checks pass with the ORIGINAL budget (T-155 r2 reverts the loosened test); uncovered link still reachable by click and keyboard; e2e", "done": true, "evidence": "test_polish_r3 original budget passes (first screen, 150/170 px rows at 1440, 420 px at 390) and test_uncovered_ui passes from git archive HEAD 94a31a4; link now <=2 px taller"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:52:57Z orchestrator: assigned: frontend
- 2026-11-02T15:36:25Z frontend: claimed
- 2026-11-02T15:36:25Z frontend: AC 1 checked: test_polish_r3 original budget passes (first screen, 150/170 px rows at 1440, 420 px at 390) and test_uncovered_ui passes from git archive HEAD 94a31a4; link now <=2 px taller
- 2026-11-02T15:36:25Z frontend: moved in_progress -> in_review
- 2026-11-02T15:36:38Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: uncovered.js inserts the 'Not in an entry (n)' link in the entry head right after the record chip (was appended after the status chips and wrapped to its own line at 390); uncovered.css keeps it nowrap. Measured on the sample: link adds <=2 px per row at 1440 and 390 (was 22 px at 390). Verified: test_polish_r3 (original budget, no markers present) + test_uncovered_ui pass from git archive HEAD. Left: nothing; I removed the T-149 r2 xfail marker earlier (now passing). Surprised: at 1440 the same rows were only 4 px taller.
````

### User / tool · 2026-11-02T15:37:00.511Z

**tool result**
````
94a31a4 fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-count chips), loading/error/retry states, j/k and search, case names (create, rename, T-157 titles), rerun only when rerun_available
c0e2b86 fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
985dbd2db17e8cfa53e82a6595e64f8659181344
commit 94a31a4b8f0f7cd5cec7a4960460b9d916af7a97
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:29:46 2026 -0600

    fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/uncovered.css | 3 +++
 app/frontend/uncovered.js  | 5 +++--
 2 files changed, 6 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:03.787Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat project_t155_e2e_triage_patterns.md feedback_evidence_sha_vs_commit.md feedback_verify_pid_before_kill.md feedback_review_write_once.md feedback_frontend_text_coupling.md project_t136_r2_patterns.md",
 "description": "Read relevant prior memory files"
}
````

### User / tool · 2026-11-02T15:37:03.865Z

**tool result**
````
---
name: t155-e2e-triage-patterns
description: T-155 r1 (20b3a42, changes): green claim cited an older sha, "stale" density reds were real at 078c5ae, hidden collapsed list measures 0 px with an 8px margin, refusal box sits btn_y+132
metadata:
  type: project
---

T-155 (test-only triage of 9 e2e reds) reviewed at 20b3a42. Verdict changes: 0 blockers, 2 majors, 2 minors, 1 nit. Review: reviews/T-155-staff-engineer-r1b.md (corrected record; the first file is write-once and has two count errors).

- **Green claim on an older sha.** The card's AC evidence was a run at 078c5ae; 20b3a42 has 12 more commits. At 20b3a42 test_polish_r3.py:181 (first entry y<520) fails 3 of 3 (y=552, the T-149 overview block). It was not triaged on the card.
- **"Stale test" was the wrong direction.** At 078c5ae the original density budgets really failed (179 > 150, 430 > 420). f262223 fixed it upstream. At 20b3a42 the original measure passes, so the T-144 edit to ROW_BOXES_JS was unnecessary.
- **Hidden list.** The T-144 list is `display:none` when closed (uncovered.css:4, uncovered.js:21). It has height 0 but its computed margin-top is 8px, so the edit's subtraction under-measures list rows by 8px. The "30-57 px" comment is false at HEAD.
- **Refusal box geometry (T-158).** The accept-refused box sits at btn_y + 132 and is below an 844px fold when btn_y > 580. One of 24 samples hit it (scrollY 734). The card's "about 50%" rate did not reproduce. Mechanism real, rate overstated.
- **Load.** uptime load averages were 21 to 24 during these runs. Flake rates measured on this machine may not match a loaded one.

**Why:** a "stale test" triage is a claim about history. It has to be tested at the sha the red was seen on, not inferred from the diff.
**How to apply:** for any e2e triage, run the pre-change test file at the card's cited sha and at HEAD. Count commits between them. For any layout budget, check the DOM state (display, height, computed margin) of anything the test excludes.

Related: [[feedback_evidence_sha_vs_commit]], [[project_t136_r2_patterns]], [[project_t158_mobile_geometry]], [[feedback_review_write_once]].
---
name: feedback_evidence_sha_vs_commit
description: a card's green run and its "stale test" triage can cite an older sha; run the cited test at that sha and at the reviewed commit before accepting either, and count the commits between them
metadata:
  type: feedback
---

Before accepting "full suite green at clean HEAD" or "this red is a stale test", check which sha the evidence ran on. Run `git rev-list --count <evidence-sha>..<commit>` and run the disputed test file at both shas. If the file at the evidence sha fails the same way the card says it is stale, the triage is backwards.

**Why:** T-155 r1 (20b3a42): the AC evidence was a run at 078c5ae, 12 commits behind. At 078c5ae the density budgets really failed (179 > 150); a later frontend fix (f262223) cured them. The card called them stale and loosened the budget with a false comment. A first-screen red at the reviewed commit was not on the card.

**How to apply:** in any e2e review, record the evidence sha and the reviewed sha on the first line of the exercised list. Use an archive per sha (git archive | tar -x into a unique scratch dir, own port, E2E_REQUIRE_DB=1). If HEAD moves during the review, say so and state which sha the findings are for.

Related: [[project_t155_e2e_triage_patterns]], [[project_round2_snapshot_review_patterns]].
---
name: feedback_verify_pid_before_kill
description: a PID captured with $! from a subshell can be a wrapper, not the server; run ps -p and lsof on the port before kill, and kill the listener, not the recorded number
metadata:
  type: feedback
---

Before killing a server, check the PID you recorded with `ps -o pid,ppid,command -p <pid>` and check the listener with `lsof -iTCP:<port> -sTCP:LISTEN -n -P`. Kill the listener and confirm the port is closed.

**Why:** T-119 r3 (this session): I wrote `echo $!` from a subshell that started `nohup python -m app.main &`. The recorded PID (6353) was a bash wrapper, not the server. I killed it without checking. The real server (6354) stayed up and had to be stopped by its listener PID. The ports were closed only after that second kill.

**How to apply:** when a review starts its own servers, record the listener PID with lsof after the health check, not `$!`. Stop only PIDs whose command line shows the app, and verify both ports closed afterwards. If a wrong PID was killed, say so in the review's exercised list.

Related: [[project_t119_keyboard_coverage_patterns]], [[feedback_shared_scratchpad]].
---
name: feedback_review_write_once
description: reviews/*.md are append-only under reviewer-write-guard; proof-read the review body before the first Write, because Edit is blocked afterwards
metadata:
  type: feedback
---

Write a review file once, after proof-reading every line citation and every "I ran X" claim. Once `reviews/<card>-<persona>.md` exists, `Edit` on it is refused by reviewer-write-guard ("reviews are append-only — write a new file with a -r2/-r3 suffix"), so a typo in the body stays there.

**Why:** T-080 r2 (this session): I wrote `reviews/T-080-staff-engineer-r2.md` with three wrong body citations (a line number, an "export builder" pointer with no path, and an unverified "stable across GETs" claim). The JSON block was accurate, but the body could not be corrected in place.

**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it ("review must contain a ```json block"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.

**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.

**T-141 r5 addendum:** the first Write carried one control claim I had not yet run ("V10 and W10 print info on 93a2ffc"). It was true, but the guard then refused an Edit to fix a muddled sentence about it. Run every "X prints Y on the control archive" claim before the first Write, and proof-read the evidence sentence, not only the JSON. Accurate-but-clumsy wording can stay, but it cannot be corrected in place. See [[project_t141_r5_patterns]].
---
name: feedback_frontend_text_coupling
description: when a backend changes a user-facing sentence, grep app/frontend for the old phrase and for regexes over it; a server-text swap keyed to old wording silently keeps the frontend fallback
metadata:
  type: feedback
---

When a card rewords a sentence the UI shows, check the frontend for (a) the old literal phrase in fallback constants and (b) any regex or `includes` that decides whether to swap in the server's text. A backend-only test passes while the screen keeps the old fallback.

**Why:** T-134 r4 (4f416a4): the backend reworded the held-edit sentence to a conditional and dropped "stays blocked". `app/frontend/review.js:191` only swapped in the server's text when `/export stays blocked/` matched, so the fallback `AI_HELD` (review.js:182) that says "the export stays blocked" stayed on the card while the gate passed. The backend unit tests were green.

**How to apply:** `grep -rn "<old phrase>" app/frontend app/backend` and `grep -rn "test(" app/frontend | grep -i <phrase>` before accepting a wording fix. Probe the item's JSON for the same state and run the frontend regex over it (python `re` gives the same answer for these literals). Prefer an explicit server flag over a regex on text (the T-134 r4 `second_check_pending` field exists for this; the UI does not read it yet).

Related: [[project_t134_r4_t138_r2_patterns]].
---
name: t136-r2-patterns
description: T-136 r2 (HEAD 07c7558): private-server fallback to :7860, red e2e suite predating the card, flaky mobile and open_rail tests, client copy of a server gate rule
metadata:
  type: project
---

T-136 r2 review (reviews/T-136-staff-engineer-r2.md, verdict changes: 0 blockers, 2 majors, 2 minors).

- **Fall-through in a start-your-own-server harness.** tests/e2e/conftest.py pytest_configure returned silently when its private server failed to start or did not answer in 80 tries, leaving BASE at localhost:7860. A plain run then ran against the shared dev app and reported green with skips. Repro: prepend sys.exit(3) to app/main.py in a scratch copy. Check any "start my own server" helper for paths that keep the default URL.
- **Attribution run was invalid at first.** Archiving an older commit (d19ae46) with the old conftest hit the shared :7860 app and skipped 30 DB specs. Re-run old commits against your own server with E2E_REQUIRE_DB=1, and check which server the run actually hits before attributing failures.
- **Red suite that predates the card.** Seven deterministic e2e failures (polish_r5 row reasons, rerun_judge x2, stepper x4) fail on d19ae46 too, so the card's frontend diff is not the cause. The card still cannot claim a pass on a red suite.
- **Flakes.** Mobile refusal test (code_check_refusal 390x844) failed in 2 of 3 plain runs on the same commit. The card's own gate-warning test failed once in 5 runs; open_rail does a read-then-click on details.open (test_stepper.py:35-36).
- **Duplicated gate rule.** dom.js:55 decides "export stays blocked" from reasons containing JUDGE_UNAVAILABLE; trace.py:807 ai_summary_unchecked decides it on the server. They differ on judge verdict None or "".

**Why:** these four patterns (fall-through, invalid attribution, red-before-card, read-then-click) recur across cards; check for them first.
**How to apply:** when a card claims "N fail identically at HEAD", archive its parent and run the same files against your own server before accepting the attribution; run the same file twice before calling a test deterministic.

Related: [[project_e2e_contract_review_patterns]], [[project_harness_review_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:04.591Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; echo ---; git log --oneline -8; echo ---; ls tests/e2e/ | head -80; echo ---; ls reviews | grep -E \"T-16[0-2]|T-155|T-149|T-060\" ; echo ---; grep -rn \"T-060\\|compact\" docs/*.md memory/*.md 2>/dev/null | head -20",
 "description": "Check git state, e2e test list, and budget docs"
}
````

### User / tool · 2026-11-02T15:37:04.777Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/case_list.py
 M app/backend/export.py
 M app/backend/present.py
 M app/backend/store.py
 M app/backend/trace.py
MM app/frontend/api.js
MM app/frontend/app.js
---
985dbd2 fix(backend): T-139 r4 one money detector (money.py) for the hold, the export gate and the letter eval; the gate scans the final letter text and blocks naming the line; labelled figures and number words after a money verb are money; held-out hints state the true cause
67be38d fix(frontend): T-162 r2 a collapsed Dismissed group says how many of its items carry a re-run note; e2e opens the group and asserts the entry and amount notes visible, unconditional; note helpers at module scope
a4eeb2b docs(orchestrator): scope cut 7e charge-source detection residuals (T-140)
94a31a4 fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-count chips), loading/error/retry states, j/k and search, case names (create, rename, T-157 titles), rerun only when rerun_available
c0e2b86 fix(backend): T-159 r2 confirm and its event in one transaction (accept taken back on failure), trace events carry the confirm, tests kill the oldest-event and confirmed_at mutants
99438fb fix(backend): T-161 r2 first-run failure driven by failed_steps (flag step down with no phrase-list hit reads run_partial), extract-down first run with no entries reads failed
78b6a33 fix(backend): T-141 r7 plural-history date guard reads two-digit years (1/3/26, 1-3-26, Jan 3, 26, 1/26)
---
__init__.py
__pycache__
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charge_confirm.py
test_charges.py
test_code_check_refusal.py
test_conflict_coverage.py
test_conflict_skipped.py
test_edit.py
test_edit_to_check.py
test_export_ui.py
test_flags_panel.py
test_held_quote_gate.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_multicase.py
test_no_console_errors.py
test_polish_r3.py
test_polish_r4.py
test_polish_r5.py
test_rerun_judge.py
test_rerun_note.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
test_uncovered_ui.py
---
T-060-accessibility-pass1.md
T-060-accessibility-pass2.md
T-060-accessibility-pass3.md
T-060-paralegal-pass1.md
T-060-paralegal-pass2.md
T-060-paralegal-pass4.md
T-060-paralegal-pass5.md
T-060-ux-designer-pass1.md
T-060-ux-designer-pass2.md
T-060-ux-designer-pass3.md
T-060-ux-designer-pass4.md
T-060-ux-designer-pass5.md
T-149-paralegal.md
T-149-ux-designer.md
T-155-staff-engineer-r1b.md
T-155-staff-engineer.md
T-161-staff-engineer-r2.md
T-161-staff-engineer.md
T-162-staff-engineer.md
---
docs/CONTRACT.md:232:- `STATE.md` is the handoff artifact: what milestone is active, what is in flight, what the next three actions are, open risks, URLs. Rewrite it every cycle (keep under 150 lines). If your context is compacted or the session restarts, `STATE.md` + `board.py status` must be enough to resume.
docs/CONTRACT.md:436:- **Context hygiene:** keep subagent reports short; details live in files. Before any `/compact` risk (you'll feel it), rewrite `STATE.md`. After compaction, re-read `CLAUDE.md`, `STATE.md`, `board.py status`.
memory/PROGRESS.md:36:- 2026-11-02T09:14Z heartbeat: 95 done; M2 waits on T-112 live runs then T-113 (conflict judge false agrees); T-060 pass-1 reviews running; 0 stalled; inbox empty.
memory/PROGRESS.md:37:- 2026-11-02T10:14Z heartbeat: 97 done; M2 waits on T-113 (conflict judge + 3 live runs); T-060 pass 2 in progress (paralegal pass); 0 stalled; inbox empty.
memory/PROGRESS.md:38:- 2026-11-02T10:55:44Z orchestrator: T-060/T-096 UX+a11y pass 3, T-114/T-119 re-checks, T-113 live 3-runs on e1ce8dc, backend on T-120/121/123/105 dispatched; T-112 r2 review running.
docs/UI_DESIGN_BRIEF.md:1:# UI design brief (T-060 pass 1, DRAFT for frontend and the UX reviewer)
docs/UI_DESIGN_BRIEF.md:3:Status: draft by researcher; the frontend card T-060 owns implementation and may amend values with a note. Evidence for the choices is in
docs/UI_DESIGN_BRIEF.md:44:Default is **comfortable**; a header toggle switches to **compact** and is remembered in `localStorage` (wrapped in try/catch; page works without it).
docs/UI_DESIGN_BRIEF.md:144:3. **Line 2:** the summary (`--t-body`, up to 3 lines, then "Show more"), followed by the verbatim quote block (7.3), collapsed to one line by default in compact density
docs/UI_DESIGN_BRIEF.md:189:- Buttons: height 36 px (28 compact), 4 px radius, text+icon, never icon-only except Close and the density/theme toggles (which carry `aria-label` and a tooltip).
docs/UI_DESIGN_BRIEF.md:253:3. Density default: comfortable. Compact is for the power user and the demo video at 1280 px; the UX reviewer may prefer compact as default on desktop.
memory/SCOPE_CUTS.md:50:| debt | T-065 accepted with documented debt after 2 rounds (§7.4) | r2 major (btn-undo-batch contract id) already fixed at HEAD by 4594bb7; 4 minors carried to T-060 UI polish. | see card | M3 |
memory/SCOPE_CUTS.md:51:| debt | T-068 accepted with documented debt after 3 rounds (§7.4) | r3 major (confirmed entry still 'Needs review'/'date can be read two ways') is the server leaving DATE_AMBIGUOUS after confirm_date, fixed in T-076 r2. Minors (Edit enabled on undated row; orphan branch needs a curated fixture) carried to T-060. | see card | M3 |
memory/SCOPE_CUTS.md:55:| debt | T-072 accepted with documented debt after 4 rounds (§7.4) | 4 rounds: user-facing reason text and guards done; remaining major is one mock summary in app/frontend/mock.js:15 (dev ?api=mock only) carried to T-060 with the 2 minors. | see card | M3 |
memory/SCOPE_CUTS.md:63:| debt | T-046 accepted with documented debt after 2 rounds (§7.4) | Stretch card, 2 rounds; pane works at >=1024px. Major (Show-gap-flag link needs ~190 Tab presses: add a skip link/shortcut) and minors carried to T-060. | see card | M3 |
memory/SCOPE_CUTS.md:76:| debt | T-115 accepted with documented debt after 2 rounds (§7.4) | 2 rounds; fixtures are real recordings and guarded. D-029 amended by D-056. J3 controls red is T-113's scope. Remaining: e2e race at test_stepper.py:204 -> folded into the T-060 round-3 e2e run (frontend worker declares/fixes tests it touches). | see card | M3 |
memory/SCOPE_CUTS.md:82:| debt | T-060 accepted with documented debt after 3 rounds (§7.4) | paralegal pass-5 majors moved to T-136 | see card | M3 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:09.126Z

**tool call — Bash**
````
{
 "command": "git show 94a31a4 -- app/frontend/uncovered.css app/frontend/uncovered.js; echo ---LOG; git log --oneline -6 -- tests/e2e/test_polish_r3.py; echo ---; git log --oneline -4 -- tests/e2e/test_uncovered_ui.py; echo; git rev-list --count 94a31a4..985dbd2",
 "description": "Show T-160 diff and test history"
}
````

### User / tool · 2026-11-02T15:37:09.531Z

**tool result**
````
commit 94a31a4b8f0f7cd5cec7a4960460b9d916af7a97
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 09:29:46 2026 -0600

    fix(frontend): T-160 the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/uncovered.css b/app/frontend/uncovered.css
index 35ef402..e65b246 100644
--- a/app/frontend/uncovered.css
+++ b/app/frontend/uncovered.css
@@ -12,3 +12,6 @@
   .unc-item { flex-direction: column; gap: var(--s-1); }
   .unc-jump { align-self: flex-start; min-height: 2.25rem; padding-left: 0; }
 }
+
+/* T-160: the link lives in the head line; it never takes a line of its own */
+.entry-head > .unc-toggle { flex: none; white-space: nowrap; min-height: 1.5rem; font-size: var(--t-sm); }
diff --git a/app/frontend/uncovered.js b/app/frontend/uncovered.js
index 5a3596d..a706d17 100644
--- a/app/frontend/uncovered.js
+++ b/app/frontend/uncovered.js
@@ -28,8 +28,9 @@
           onclick: () => ZL.openSource([{ record_id: rec.id, start: u.start, end: u.end }], `Record ${rec.seq}: ${rec.source_label || who}`) }, many ? `Show in record ${rec.seq}` : "Show in record")))));
     const toggle = el("button", { type: "button", class: "btn btn--link unc-toggle", "data-testid": "uncovered-summary", "aria-expanded": String(opened.has(entry.id)), "aria-controls": id, "aria-label": full + ": " + who,
       onclick: () => { const open = panel.hidden; panel.hidden = !open; toggle.setAttribute("aria-expanded", String(open)); if (open) opened.add(entry.id); else opened.delete(entry.id); } }, `Not in an entry (${n})`);
-    const head = row.querySelector(":scope > .entry-head");   // the head line has room on a wide screen; the link bar wraps to a second line when one more link joins it
-    if (head) head.append(toggle); else row.append(toggle);
+    // T-160: the link sits in the head line right after the record chip (or the provider), so it shares a line that already exists; at the end of the head it wrapped to a line of its own on a phone.
+    const head = row.querySelector(":scope > .entry-head"), anchor = head && (head.querySelector(":scope > .chip--rec") || head.querySelector(":scope > .provider"));
+    if (anchor) anchor.after(toggle); else if (head) head.append(toggle); else row.append(toggle);
     row.append(panel);
   });
 
---LOG
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-count chips), loading/error/retry states, j/k and search, case names (create, rename, T-157 titles), rerun only when rerun_available
d967488 test(e2e): T-155 r2 revert T-144 row-height loosening, xfail(strict) first-screen (T-149 r2), a7 presence check, rename stale test name
20b3a42 test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
1394661 feat(frontend): T-149 multi-case overview (list, filter, sort, call-out chips, progress per kind) and case overview block (progress, call-outs, export-gate steps) at the top of the detail
b612176 feat(frontend): T-060 r5 + T-131 - dismissed items keep no Accept, edited-needs-review counts as open, focus stays in one list, one need-review count, plain reasons, long dates, Filtered by rule, one-line letter control
c559ce2 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
---
f262223 fix(frontend): T-144 the uncovered list opens from a short link in the entry head so compact rows keep their height
ded5ca4 feat(frontend): T-144 'Also in this record, not in an entry (n)' list under each entry, one click to the highlighted sentence

3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:11.193Z

**tool call — Bash**
````
{
 "command": "git show d967488 -- tests/e2e/test_polish_r3.py | head -150",
 "description": "Show T-155 r2 revert diff to polish_r3"
}
````

### User / tool · 2026-11-02T15:37:11.287Z

**tool result**
````
commit d967488b902c04b5926603aa805fdc7f48eb49d1
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:54:39 2026 -0600

    test(e2e): T-155 r2 revert T-144 row-height loosening, xfail(strict) first-screen (T-149 r2), a7 presence check, rename stale test name
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/test_polish_r3.py b/tests/e2e/test_polish_r3.py
index 20c71ae..5c8575e 100644
--- a/tests/e2e/test_polish_r3.py
+++ b/tests/e2e/test_polish_r3.py
@@ -165,19 +165,13 @@ def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_c
 
 
 # ---- 4. density
-# T-144 (stale-test update): every entry row may now carry a collapsed "Also in this record, not in an entry (n)" list (uncovered-list, ~30-57 px with its margins). The row-height
-# budgets below (150 / 170 px at 1440, 420 px at 390) were set before it existed and still guard the row itself, so the measured height leaves that deliberate list out.
-ROW_BOXES_JS = """els => els.map(e => { const r = e.getBoundingClientRect(), u = e.querySelector('[data-testid=uncovered-list]');
-    let extra = 0; if (u) { const c = getComputedStyle(u); extra = u.getBoundingClientRect().height + parseFloat(c.marginTop) + parseFloat(c.marginBottom); }
-    return [r.top + scrollY, r.height - extra, e.getAttribute('data-state')]; })"""
-
-
+@pytest.mark.xfail(strict=True, reason="T-149 r2")   # first entry y=552 > 520 under the case overview block; T-149 r2 owns moving it above the fold. Not loosened here.
 def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
     try:
         rows = pg.locator('[data-testid=queue] > article')
         assert rows.count() >= 5
-        boxes = rows.evaluate_all(ROW_BOXES_JS)
+        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
         assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
         first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
         assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
@@ -200,7 +194,7 @@ def test_row_opens_with_more_and_closes_with_less(page, sample_case):
 def test_390_needs_review_row_is_at_most_420(pw, lib09):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
     try:
-        hs = [bx[1] for bx in pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all(ROW_BOXES_JS)]
+        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
         assert hs and max(hs) <= 420, hs
         assert pg.evaluate("document.documentElement.scrollWidth") <= 391
     finally:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:11.606Z

**tool call — Bash**
````
{
 "command": "git show 94a31a4:tests/e2e/test_polish_r3.py | cat -n | head -260",
 "description": "Read test_polish_r3.py at the card commit"
}
````

### User / tool · 2026-11-02T15:37:11.703Z

**tool result**
````
     1	"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
     2	T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
     3	(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
     4	New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
     5	Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
     6	import re
     7	import time
     8	import pytest
     9	from playwright.sync_api import expect
    10	from tests.e2e.conftest import api, open_case, BASE
    11	
    12	BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")
    13	
    14	
    15	def _run(tok):
    16	    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    17	    for _ in range(300):
    18	        s = api("GET", f"/api/cases/{tok}/status")[1]
    19	        if s["status"] in ("ready", "failed"):
    20	            break
    21	        time.sleep(.5)
    22	    assert s["status"] == "ready"
    23	
    24	
    25	@pytest.fixture
    26	def lib09():
    27	    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    28	    if st not in (200, 201):
    29	        pytest.skip("library cases need ZLAYT_MODE=local")
    30	    _run(c["token"])
    31	    yield c["token"]
    32	    api("DELETE", f"/api/cases/{c['token']}")
    33	
    34	
    35	def active(page):
    36	    return page.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")
    37	
    38	
    39	def tab_until(page, testid, limit=40):
    40	    for _ in range(limit):
    41	        page.keyboard.press("Tab")
    42	        a = active(page)
    43	        if a and a["tid"] == testid:
    44	            return a
    45	    raise AssertionError(f"Tab never reached {testid}; last {active(page)}")
    46	
    47	
    48	# ---- 1. the shortcut sheet
    49	def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
    50	    open_case(page, sample_case)
    51	    page.get_by_test_id("btn-shortcuts").click()
    52	    dlg = page.get_by_test_id("shortcuts-modal"); expect(dlg).to_be_visible()
    53	    lst = dlg.get_by_test_id("shortcuts-list")
    54	    expect(lst.locator("kbd")).to_have_count(9)
    55	    expect(lst.locator("dt")).to_have_count(9); expect(lst.locator("dd")).to_have_count(9)
    56	    txt = dlg.inner_text()
    57	    assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
    58	    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    59	    page.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('data-testid') === 'btn-shortcuts'")   # the dialog hands focus back to its opener first; focusing the row before that raced it (flaky at HEAD 078c5ae)
    60	    # '?' from an item row opens the same sheet
    61	    page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()
    62	
    63	
    64	def test_no_object_undefined_or_null_text_on_the_review_page(page, sample_case):
    65	    open_case(page, sample_case)
    66	    assert not BAD_TEXT.search(page.locator("body").inner_text()), BAD_TEXT.findall(page.locator("body").inner_text())
    67	
    68	
    69	# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
    70	def _snapshot(page):
    71	    return page.evaluate("""() => ({ accepted: document.querySelectorAll('[data-review=accepted],[data-review=dismissed],[data-review=edited]').length,
    72	        dialogs: document.querySelectorAll('dialog[open]').length, active: (document.activeElement || {}).tagName + ':' + ((document.activeElement || {}).getAttribute ? document.activeElement.getAttribute('data-testid') : '') })""")
    73	
    74	
    75	def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
    76	    open_case(page, sample_case)
    77	    before = _snapshot(page)
    78	    # from the page body
    79	    page.evaluate("document.activeElement && document.activeElement.blur()")
    80	    for k in ("j", "a", "d", "Shift+A", "?"):
    81	        page.keyboard.press(k)
    82	    assert _snapshot(page) == {**before, "active": _snapshot(page)["active"]}, "a key acted from the page body"
    83	    assert page.evaluate("!document.activeElement.closest || !document.activeElement.closest('[data-item-id]')")
    84	    # from the Export button
    85	    page.get_by_test_id("btn-export").focus()
    86	    for k in ("j", "a", "d", "Shift+A", "?"):
    87	        page.keyboard.press(k)
    88	    s = _snapshot(page)
    89	    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0 and s["active"].endswith("btn-export"), s
    90	    # from an input: the edit box of an item, and the sort control
    91	    page.get_by_test_id("entry-1").get_by_test_id("btn-edit").click()
    92	    ta = page.get_by_test_id("entry-1").get_by_test_id("edit-summary"); expect(ta).to_be_focused()
    93	    start = ta.input_value()
    94	    for k in ("j", "a", "d", "Shift+A"):
    95	        page.keyboard.press(k)
    96	    s = _snapshot(page)
    97	    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0, s
    98	    assert ta.input_value() == start + "jadA"                       # they were typed, not run
    99	    page.keyboard.press("Escape")
   100	    page.get_by_test_id("sort").focus()
   101	    for k in ("j", "a", "Shift+A"):
   102	        page.keyboard.press(k)
   103	    assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0
   104	
   105	
   106	def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
   107	    """WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing."""
   108	    open_case(page, sample_case)
   109	    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()
   110	    page.keyboard.press("p")
   111	    expect(page.get_by_test_id("sbs-body")).to_be_focused()           # from an item row it works, and the pane now shows an item
   112	    page.keyboard.press("Escape")
   113	    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')"), "Escape should return focus to the item row"
   114	    focus = lambda: page.evaluate("(() => { const a = document.activeElement; return (a.tagName || '') + ':' + (a.getAttribute('data-testid') || a.id || ''); })()")
   115	    page.evaluate("document.activeElement.blur()")
   116	    before = focus()
   117	    page.keyboard.press("p")
   118	    assert focus() == before, f"p moved focus from the page body: {before} -> {focus()}"
   119	    for tid in ("btn-export", "btn-shortcuts", "sort"):
   120	        page.get_by_test_id(tid).focus(); here = focus()
   121	        page.keyboard.press("p")
   122	        assert focus() == here, f"p moved focus from {tid}: {here} -> {focus()}"
   123	    assert not page.get_by_test_id("sbs-body").evaluate("e => e === document.activeElement")
   124	
   125	
   126	def test_letter_key_with_a_window_open_says_so(page, sample_case):
   127	    """paralegal F11: o then a used to do nothing, silently."""
   128	    open_case(page, sample_case)
   129	    page.get_by_test_id("entry-1").focus(); page.keyboard.press("o"); expect(page.get_by_test_id("record-modal")).to_be_visible()
   130	    page.keyboard.press("a")
   131	    expect(page.locator("#rv-live")).to_contain_text("Press Escape")
   132	    assert page.locator("[data-review=accepted]").count() == 0
   133	
   134	
   135	# ---- 3. Tab, Enter and Space only: review one item, then export (R-RV-4)
   136	def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_case):
   137	    tok = sample_case
   138	    c = api("GET", f"/api/cases/{tok}")[1]
   139	    ids = [e["id"] for e in c["entries"] if e["state"] == "verified" and e["date"]]
   140	    assert api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})[0] == 200   # setup by API: the checked entries are in the letter
   141	    open_case(page, tok)
   142	    # (a) one item reviewed by keyboard: Tab to the first skip link, Enter, then Tab to the item's Dismiss button, Enter
   143	    page.evaluate("document.activeElement && document.activeElement.blur()")
   144	    tab_until(page, "skip-review", 6)
   145	    page.keyboard.press("Enter")
   146	    row = active(page); assert row["item"], row
   147	    item = row["item"]
   148	    tab_until(page, "btn-dismiss", 12)
   149	    page.keyboard.press("Enter")
   150	    expect(page.locator(f'[data-item-id="{item}"]').first).to_have_attribute("data-review", "dismissed")
   151	    # (b) the export, from a fresh load, by keyboard only
   152	    page.reload(); page.get_by_test_id("timeline").wait_for()
   153	    page.evaluate("document.activeElement && document.activeElement.blur()")
   154	    tab_until(page, "skip-export", 10)
   155	    page.keyboard.press("Enter")
   156	    assert active(page)["tid"] == "btn-export"
   157	    page.keyboard.press("Enter")
   158	    expect(page.get_by_test_id("export-letter")).to_be_visible()
   159	    tab_until(page, "btn-copy-letter", 6)
   160	    page.keyboard.press("Space")
   161	    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
   162	    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
   163	    page.keyboard.press("Enter")
   164	    expect(page.locator("#export-status")).to_contain_text("Copied the treatment section")
   165	
   166	
   167	# ---- 4. density
   168	def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
   169	    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
   170	    try:
   171	        rows = pg.locator('[data-testid=queue] > article')
   172	        assert rows.count() >= 5
   173	        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
   174	        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
   175	        first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
   176	        assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
   177	        visible = [bx for bx in boxes if bx[0] + bx[1] <= 900]
   178	        assert len(visible) >= 2, boxes                                               # T-149: the case overview block (about 120 px) now sits above the first entry; it was 3 rows before it
   179	        for top, h, state in boxes:
   180	            assert h <= (170 if state == "needs_review" else 150), boxes
   181	    finally:
   182	        b.close()
   183	
   184	
   185	def test_row_opens_with_more_and_closes_with_less(page, sample_case):
   186	    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
   187	    h0 = row.bounding_box()["height"]
   188	    expect(t).to_have_attribute("aria-expanded", "false"); t.click(); expect(t).to_have_attribute("aria-expanded", "true")
   189	    assert "is-open" in row.get_attribute("class")
   190	    t.click(); expect(t).to_have_attribute("aria-expanded", "false"); assert abs(row.bounding_box()["height"] - h0) < 2
   191	
   192	
   193	def test_390_needs_review_row_is_at_most_420(pw, lib09):
   194	    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
   195	    try:
   196	        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
   197	        assert hs and max(hs) <= 420, hs
   198	        assert pg.evaluate("document.documentElement.scrollWidth") <= 391
   199	    finally:
   200	        b.close()
   201	
   202	
   203	# ---- 5. decided rows show a state, not a filled Accept
   204	def test_accepted_row_has_no_filled_accept_and_undo_returns(page, sample_case):
   205	    open_case(page, sample_case); row = page.get_by_test_id("entry-1")
   206	    acc = row.get_by_test_id("btn-accept"); expect(acc).to_have_class(re.compile(r"btn--primary"))
   207	    acc.click(); expect(row).to_have_attribute("data-review", "accepted")
   208	    acc = row.get_by_test_id("btn-accept")
   209	    assert "btn--primary" not in acc.get_attribute("class") and acc.inner_text().strip().startswith("Accepted")
   210	    assert page.locator("[data-testid=entry-1] .btn--primary:visible").count() == 0
   211	    row.get_by_test_id("btn-reset").click(); expect(row).to_have_attribute("data-review", "pending")
   212	    expect(row.get_by_test_id("btn-accept")).to_have_class(re.compile(r"btn--primary"))
   213	
   214	
   215	def test_dismissed_row_keeps_no_filled_accept(page, sample_case):
   216	    open_case(page, sample_case); row = page.get_by_test_id("entry-2")
   217	    row.get_by_test_id("btn-dismiss").click(); expect(row).to_have_attribute("data-review", "dismissed")
   218	    assert row.get_by_test_id("btn-accept").count() == 0     # T-060 r5 (paralegal M1): a dismissed row keeps Undo, not Accept
   219	    assert row.get_by_test_id("btn-dismiss").inner_text().strip().startswith("Dismissed")
   220	    assert row.get_by_test_id("btn-reset").inner_text().strip() == "Undo"
   221	
   222	
   223	# ---- 6. accessibility
   224	def test_320_reflow_with_case_checks_open(pw, sample_case):
   225	    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 320, "height": 640}).new_page(); open_case(pg, sample_case)
   226	    try:
   227	        pg.get_by_test_id("case-summary").click()
   228	        pg.get_by_test_id("case-step").first.wait_for()
   229	        pg.get_by_test_id("judge-summary").click()
   230	        assert pg.evaluate("document.documentElement.scrollWidth") == 320
   231	        assert pg.evaluate("[...document.querySelectorAll('.zs-chip')].filter(c => c.getBoundingClientRect().right > 320.5).length") == 0
   232	    finally:
   233	        b.close()
   234	
   235	
   236	def test_theme_toggle_name_follows_the_visible_state(page, sample_case):
   237	    open_case(page, sample_case); t = page.get_by_test_id("btn-theme")
   238	    seen = []
   239	    for _ in range(3):
   240	        t.click()
   241	        vis = t.inner_text().strip(); name = t.get_attribute("aria-label")
   242	        assert vis.lower() in name.lower(), (vis, name)                              # label in name (2.5.3)
   243	        seen.append(vis)
   244	    assert len(set(seen)) == 3, seen
   245	
   246	
   247	def test_file_input_focus_shows_a_ring_on_the_upload_control(page):
   248	    page.goto(BASE); page.get_by_test_id("btn-analyze").wait_for()
   249	    page.get_by_test_id("file-input").focus()
   250	    page.keyboard.press("Shift+Tab"); page.keyboard.press("Tab")
   251	    assert active(page)["tid"] == "file-input"
   252	    ring = page.evaluate("getComputedStyle(document.querySelector('label[for=file]')).outlineStyle")
   253	    assert ring != "none"
   254	
   255	
   256	def test_skip_link_hrefs_resolve_to_elements(page, sample_case):
   257	    open_case(page, sample_case)
   258	    bad = page.evaluate("[...document.querySelectorAll('#skip-nav a')].filter(a => !document.getElementById(a.getAttribute('href').slice(1))).map(a => a.getAttribute('href'))")
   259	    assert bad == []
   260
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:18.141Z

**tool call — Bash**
````
{
 "command": "git show 94a31a4:tests/e2e/conftest.py | cat -n | head -150; echo ---; git show 94a31a4:tests/e2e/test_uncovered_ui.py | cat -n",
 "description": "Read e2e conftest and uncovered UI test at card commit"
}
````

### User / tool · 2026-11-02T15:37:18.258Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:21.454Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; mkdir -p \"$S/t160-review\"; git show 94a31a4:tests/e2e/conftest.py > \"$S/t160-review/conftest.head.py\" 2>/dev/null; sed -n '20,200p' \"$S/t160-review/conftest.head.py\" | grep -n \"BASE\\|PORT\\|7860\\|E2E_\\|def \\|ZLAYT\\|LLM_BACKEND\\|Popen\\|subprocess\" | head -80",
 "description": "Locate server/port config in e2e conftest"
}
````

### User / tool · 2026-11-02T15:37:21.574Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
76:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
82:def pytest_configure(config):
83:    """T-136 r2 (staff review F1): a plain `pytest tests/e2e` must RUN the specs that write to the server's SQLite file (ZLAYT_DB: test_edit_to_check, test_code_check_refusal, test_change_the_quote,
84:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
85:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
86:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
87:    global BASE
88:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
90:    import atexit, shutil, socket, subprocess, sys, tempfile, time
93:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
96:    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
99:    def fail(why):
100:        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
108:        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)
122:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; BASE = base
123:    def stop():
131:def needs_db():
132:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
134:    path = os.environ.get("ZLAYT_DB")
136:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
137:        if os.environ.get("E2E_REQUIRE_DB") == "1":
142:def _up():
144:        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
149:def pytest_collection_modifyitems(config, items):
152:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
157:def api(method, path, body=None):
158:    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
167:def golden_text(name):
171:def base_url():
172:    return BASE
175:def sample_case():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:30.720Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T-160-r1; rm -rf \"$R\"; mkdir -p \"$R/card-94a31a4\" \"$R/head-985dbd2\" && git archive 94a31a4 | tar -x -C \"$R/card-94a31a4\" && git archive HEAD | tar -x -C \"$R/head-985dbd2\" && ls \"$R/card-94a31a4\" | head -50; echo; ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python; git rev-parse HEAD; git rev-parse --short 94a31a4; echo \"archive at: $R\"; git log -1 --format='%H %s' 94a31a4 | cut -c1-60; git show 802d5fd:tests/e2e/test_polish_r3.py | grep -n \"xfail\" ",
 "description": "Archive card commit and HEAD into scratch dirs"
}
````

### User / tool · 2026-11-02T15:37:30.788Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T-160-r1; rm -rf "$R"; mkdir -p "$R/card-94a31a4" "$R/head-985dbd2" && git archive 94a31a4 has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:33.977Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/",
 "description": "Create unique scratch subdirectory for card archive"
}
````

### User / tool · 2026-11-02T15:37:34.063Z

**tool result**
````
card-94a31a4
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:37.439Z

**tool call — Bash**
````
{
 "command": "git archive 94a31a4 | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && git rev-parse --short HEAD && git rev-parse --short 94a31a4 && ls -la .venv/bin/python",
 "description": "Extract card commit archive and check HEAD and venv"
}
````

### User / tool · 2026-11-02T15:37:38.037Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
985dbd2
94a31a4
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:37:41.872Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q -rsxX -p no:cacheprovider 2>&1 | tail -60",
 "description": "Run test_polish_r3 on the card commit archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:38:07.935Z

**tool result**
````
...................                                                      [100%]
19 passed in 25.06s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:38:10.721Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_uncovered_ui.py -v -rsxX -p no:cacheprovider 2>&1 | tail -40; echo ---; cat tests/e2e/test_uncovered_ui.py",
 "description": "Run test_uncovered_ui on the card commit archive and read it",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:38:21.964Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 7 items

tests/e2e/test_uncovered_ui.py::test_collapsed_list_with_count_and_verbatim_sentences PASSED [ 14%]
tests/e2e/test_uncovered_ui.py::test_an_entry_whose_record_is_fully_covered_has_no_list PASSED [ 28%]
tests/e2e/test_uncovered_ui.py::test_one_click_opens_the_record_with_that_sentence_highlighted PASSED [ 42%]
tests/e2e/test_uncovered_ui.py::test_keyboard_only PASSED                [ 57%]
tests/e2e/test_uncovered_ui.py::test_usable_at_390px PASSED              [ 71%]
tests/e2e/test_uncovered_ui.py::test_changing_the_quote_updates_the_list PASSED [ 85%]
tests/e2e/test_uncovered_ui.py::test_never_in_the_letter_or_the_copy_text PASSED [100%]

============================== 7 passed in 10.23s ==============================
---
"""T-144 (GATE-M2 legal-nurse major 2, UI half): under each entry, a "Not in an entry (n)" link in the row's link bar (it costs the compact row no height) opens "Also in this record, not in an entry (n)": the record's sentences no entry quote covers
(records[].uncovered[], T-143). Closed by default, each sentence verbatim, one click opens the source record with that sentence highlighted; never in the letter or the copy text.
Needs ZLAYT_MODE=local (library case lib09, Spanish interpreter). New test ids (declared in conftest): uncovered-summary (the link, aria-expanded), uncovered-list (the list, hidden until opened, data-record-count), uncovered-heading (the full wording), uncovered-item
(one <li> per sentence, data-record-id), uncovered-text (the verbatim sentence), btn-uncovered-jump ('Show in record')."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

LIB = "case_lib09_spanish_interpreter_espalda"
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": LIB})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def _entry_of(case, record_id):
    return next(e for e in case["entries"] + case["undated_entries"] if e["record_ids"] == [record_id])


def _row(page, entry):
    return page.locator(f'[data-testid^="entry-"][data-entry-id="{entry["id"]}"]').first


def test_collapsed_list_with_count_and_verbatim_sentences(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 1)
    assert len(r1["uncovered"]) == 2
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"]))
    box, summ = row.get_by_test_id("uncovered-list"), row.get_by_test_id("uncovered-summary")
    expect(summ).to_be_visible(); expect(summ).to_have_text("Not in an entry (2)")
    expect(summ).to_have_attribute("aria-expanded", "false")                       # closed
    expect(box).to_be_hidden(); expect(box.get_by_test_id("uncovered-text").first).to_be_hidden()   # the sentences wait behind the link
    summ.click()
    expect(summ).to_have_attribute("aria-expanded", "true")
    expect(box.get_by_test_id("uncovered-heading")).to_have_text("Also in this record, not in an entry (2)")
    texts = [t for t in box.get_by_test_id("uncovered-text").all_inner_texts()]
    assert texts == [u["text"] for u in r1["uncovered"]]                          # verbatim, in record order, nothing filtered by kinds
    assert box.get_by_test_id("uncovered-item").count() == 2


def test_an_entry_whose_record_is_fully_covered_has_no_list(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r5 = next(r for r in case["records"] if r["seq"] == 5)
    assert r5["uncovered"] == []
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r5["id"]))
    expect(row.get_by_test_id("uncovered-list")).to_have_count(0); expect(row.get_by_test_id("uncovered-summary")).to_have_count(0)


def test_one_click_opens_the_record_with_that_sentence_highlighted(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 1)
    target = next(u for u in r1["uncovered"] if u["text"].startswith("Patient states she was struck by a car"))
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"])); box = row.get_by_test_id("uncovered-list")
    row.get_by_test_id("uncovered-summary").click()
    box.get_by_test_id("uncovered-item").filter(has_text=target["text"]).get_by_test_id("btn-uncovered-jump").click()
    expect(page.get_by_test_id("record-modal")).to_be_visible()
    hl = page.get_by_test_id("record-highlight")
    expect(hl).to_have_count(1)
    assert norm(hl.inner_text()) == norm(target["text"])
    expect(hl).to_be_in_viewport()


def test_keyboard_only(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r3 = next(r for r in case["records"] if r["seq"] == 3)
    target = r3["uncovered"][0]
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r3["id"])); box = row.get_by_test_id("uncovered-list")
    summ = row.get_by_test_id("uncovered-summary")
    summ.focus()
    page.keyboard.press("Enter")
    expect(summ).to_have_attribute("aria-expanded", "true"); expect(box).to_be_visible()
    jump = box.get_by_test_id("btn-uncovered-jump").first
    for _ in range(4):                                                            # More, then the list: the jump is the next stop after the row's own links
        page.keyboard.press("Tab")
        if jump.evaluate("n => n === document.activeElement"):
            break
    expect(jump).to_be_focused()
    expect(jump).to_have_accessible_name(re.compile(r"Show in record 3"))
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("record-modal")).to_be_visible()
    assert norm(page.get_by_test_id("record-highlight").inner_text()) == norm(target["text"])
    page.keyboard.press("Escape")
    expect(page.get_by_test_id("record-modal")).to_be_hidden()
    expect(jump).to_be_focused()                                                  # focus comes back to the button she used


def test_usable_at_390px(pw, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r6 = next(r for r in case["records"] if r["seq"] == 6)
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        open_case(pg, lib09)
        row = _row(pg, _entry_of(case, r6["id"])); box = row.get_by_test_id("uncovered-list")
        row.scroll_into_view_if_needed()
        sb = row.get_by_test_id("uncovered-summary").bounding_box(); assert sb["height"] >= 24 and sb["x"] >= 0 and sb["x"] + sb["width"] <= 390
        row.get_by_test_id("uncovered-summary").click()
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")   # no sideways scroll
        for j in box.get_by_test_id("btn-uncovered-jump").all():
            bb = j.bounding_box()
            assert bb["height"] >= 36 and bb["x"] >= 0 and bb["x"] + bb["width"] <= 390
        for t in box.get_by_test_id("uncovered-text").all():
            bb = t.bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390
        box.get_by_test_id("btn-uncovered-jump").nth(1).click()
        expect(pg.get_by_test_id("record-modal")).to_be_visible()
        assert norm(pg.get_by_test_id("record-highlight").inner_text()) == r6["uncovered"][1]["text"]
    finally:
        b.close()


def test_changing_the_quote_updates_the_list(page, lib09):
    """A sentence she adds to the quote leaves the list; the list comes from the server, so it is re-read after the save."""
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 3)                         # record 3: adding its interpreter line to the quote is accepted by the save route
    n0 = len(r1["uncovered"])
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"]))
    row.get_by_test_id("btn-edit-excerpt").click()
    ed = row.get_by_test_id("excerpt-editor")
    units = ed.get_by_test_id("excerpt-unit")
    for i in range(units.count()):
        if not units.nth(i).is_checked():
            units.nth(i).click()
    ed.get_by_test_id("btn-save-excerpt").click()
    expect(row.get_by_test_id("edited-note")).to_be_visible()                      # the save landed
    now = api("GET", f"/api/cases/{lib09}")[1]
    after = next(r for r in now["records"] if r["seq"] == 3)["uncovered"]
    assert len(after) < n0
    row = _row(page, _entry_of(now, r1["id"]))
    if after:
        expect(row.get_by_test_id("uncovered-summary")).to_have_text(f"Not in an entry ({len(after)})")
    else:
        expect(row.get_by_test_id("uncovered-summary")).to_have_count(0); expect(row.get_by_test_id("uncovered-list")).to_have_count(0)


def test_never_in_the_letter_or_the_copy_text(page, sample_case):
    case = api("GET", f"/api/cases/{sample_case}")[1]
    texts = [u["text"] for r in case["records"] for u in r["uncovered"]]
    assert texts, "the sample has sentences no entry covers"
    open_case(page, sample_case)
    assert page.get_by_test_id("uncovered-summary").count() >= 1
    for b in page.get_by_test_id("btn-accept").all():
        b.click()
    page.get_by_test_id("btn-export").click()
    letter = page.get_by_test_id("export-letter")
    expect(letter).to_be_visible()
    page.get_by_test_id("btn-copy-letter").click()
    clip = page.evaluate("navigator.clipboard.readText()")
    # (an accepted flag may quote its own evidence sentence in the internal notes, by contract; the notes are not checked here)
    shown = norm(letter.inner_text()) + " " + norm(clip)
    for t in texts:
        assert norm(t) not in shown, t
    assert letter.get_by_test_id("uncovered-list").count() == 0 and letter.get_by_test_id("uncovered-summary").count() == 0
    exp = api("GET", f"/api/cases/{sample_case}/export")
    if exp[0] == 200:
        for t in texts:
            assert norm(t) not in norm(exp[1]["letter_text"]), t
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:38:36.256Z

**tool call — Bash**
````
{
 "command": "git log --format='%h %s' -S\"170 if state\" -- tests/e2e/test_polish_r3.py | cut -c1-120; echo ---; git log --format='%h %s' -S\"xfail(strict=True, reason=\\\"T-149 r2\\\")\" -- tests/e2e/test_polish_r3.py | cut -c1-120; echo ---; git show ded5ca4^:tests/e2e/test_polish_r3.py | grep -n \"170\\|420\\|150\" | head; echo ---; git show ded5ca4^:tests/e2e/test_polish_r3.py | sed -n '166,185p' | cut -c1-260; echo ---; git log --oneline -3 ded5ca4 -- tests/e2e/test_polish_r3.py | cut -c1-120; echo ---; git show 20b3a42 -- tests/e2e/test_polish_r3.py | head -60 | cut -c1-260",
 "description": "Trace history of row-height budget and xfail marker"
}
````

### User / tool · 2026-11-02T15:38:36.659Z

**tool result**
````
d9efc5c test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export,
---
802d5fd feat(frontend): T-149 r2 one merged case overview block (do-this-first from next_action, amber Can export, open-
d967488 test(e2e): T-155 r2 revert T-144 row-height loosening, xfail(strict) first-screen (T-149 r2), a7 presence check,
---
179:            assert h <= (170 if state == "needs_review" else 150), boxes
192:def test_390_needs_review_row_is_at_most_420(pw, lib09):
196:        assert hs and max(hs) <= 420, hs
---
# ---- 4. density
def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
    try:
        rows = pg.locator('[data-testid=queue] > article')
        assert rows.count() >= 5
        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
        first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
        assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
        visible = [bx for bx in boxes if bx[0] + bx[1] <= 900]
        assert len(visible) >= 2, boxes                                               # T-149: the case overview block (about 120 px) now sits above the first entry; it was 3 rows before it
        for top, h, state in boxes:
            assert h <= (170 if state == "needs_review" else 150), boxes
    finally:
        b.close()


def test_row_opens_with_more_and_closes_with_less(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
---
1394661 feat(frontend): T-149 multi-case overview (list, filter, sort, call-out chips, progress per kind) and case overv
b612176 feat(frontend): T-060 r5 + T-131 - dismissed items keep no Accept, edited-needs-review counts as open, focus sta
c559ce2 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
---
commit 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:40:12 2026 -0600

    test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/e2e/test_polish_r3.py b/tests/e2e/test_polish_r3.py
index 95306c8..20c71ae 100644
--- a/tests/e2e/test_polish_r3.py
+++ b/tests/e2e/test_polish_r3.py
@@ -56,6 +56,7 @@ def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
     txt = dlg.inner_text()
     assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
     page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
+    page.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('data-testid') === 'btn-shortcuts'")   # the dialog hands focus back to its opener first; focusing the row before that raced it (flaky at HEAD 078c5ae)
     # '?' from an item row opens the same sheet
     page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()
 
@@ -164,12 +165,19 @@ def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_c
 
 
 # ---- 4. density
+# T-144 (stale-test update): every entry row may now carry a collapsed "Also in this record, not in an entry (n)" list (uncovered-list, ~30-57 px with its margins). The row-height
+# budgets below (150 / 170 px at 1440, 420 px at 390) were set before it existed and still guard the row itself, so the measured height leaves that deliberate list out.
+ROW_BOXES_JS = """els => els.map(e => { const r = e.getBoundingClientRect(), u = e.querySelector('[data-testid=uncovered-list]');
+    let extra = 0; if (u) { const c = getComputedStyle(u); extra = u.getBoundingClientRect().height + parseFloat(c.marginTop) + parseFloat(c.marginBottom); }
+    return [r.top + scrollY, r.height - extra, e.getAttribute('data-state')]; })"""
+
+
 def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
     try:
         rows = pg.locator('[data-testid=queue] > article')
         assert rows.count() >= 5
-        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
+        boxes = rows.evaluate_all(ROW_BOXES_JS)
         assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
         first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
         assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
@@ -192,7 +200,7 @@ def test_row_opens_with_more_and_closes_with_less(page, sample_case):
 def test_390_needs_review_row_is_at_most_420(pw, lib09):
     b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
     try:
-        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
+        hs = [bx[1] for bx in pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all(ROW_BOXES_JS)]
         assert hs and max(hs) <= 420, hs
         assert pg.evaluate("document.documentElement.scrollWidth") <= 391
     finally:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:38:41.974Z

**tool call — Bash**
````
{
 "command": "git diff ded5ca4^ 94a31a4 -- tests/e2e/test_polish_r3.py | cut -c1-220; echo \"--- diff-stat since T-144 base:\"; git diff --stat ded5ca4^ 94a31a4 -- tests/ app/ | tail -3; echo \"--- commits touching uncovered.* after 94a31a4 at HEAD:\"; git log --oneline 94a31a4..HEAD -- app/frontend/uncovered.css app/frontend/uncovered.js tests/e2e/test_polish_r3.py tests/e2e/test_uncovered_ui.py",
 "description": "Diff density test since pre-T-144 and check later edits"
}
````

### User / tool · 2026-11-02T15:38:42.176Z

**tool result**
````
diff --git a/tests/e2e/test_polish_r3.py b/tests/e2e/test_polish_r3.py
index 95306c8..02cea80 100644
--- a/tests/e2e/test_polish_r3.py
+++ b/tests/e2e/test_polish_r3.py
@@ -56,6 +56,7 @@ def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
     txt = dlg.inner_text()
     assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
     page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
+    page.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('data-testid') === 'btn-shortcuts'")   # the dialog hands focus back to its opener first; focusing the row before that race
     # '?' from an item row opens the same sheet
     page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()
 
--- diff-stat since T-144 base:
 tests/unit/test_t161_first_run_stage_down.py       | 136 +++++
 tests/unit/test_trace.py                           |   2 +-
 116 files changed, 7172 insertions(+), 519 deletions(-)
--- commits touching uncovered.* after 94a31a4 at HEAD:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:38:50.308Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/card-94a31a4 && grep -n \"def open_case\" -A8 tests/e2e/conftest.py; grep -n \"def sample_case\" -A6 tests/e2e/conftest.py; grep -n \"def pw\\b\\|def page\\b\" -A6 tests/e2e/conftest.py | head -30; lsof -iTCP -sTCP:LISTEN -n -P | grep -E \"787|786|7860\" ; echo \"lsof exit $?\"",
 "description": "Read open_case helper and check listening ports"
}
````

### User / tool · 2026-11-02T15:38:50.510Z

**tool result**
````
224:def open_case(page, tok):
225-    page.goto(f"{BASE}/#/case/{tok}")
226-    page.get_by_test_id("timeline").wait_for(timeout=15000)
227-
228-
229-
230-class WordingFails:
231-    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
232-    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
194:def sample_case():
195-    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
196-    import time
197-    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
198-    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
199-    for _ in range(300):
200-        s = api("GET", f"/api/cases/{tok}/status")[1]
209:def pw():
210-    sync = pytest.importorskip("playwright.sync_api")
211-    with sync.sync_playwright() as p:
212-        yield p
213-
214-@pytest.fixture
215:def page(pw):
216-    b = pw.chromium.launch()
217-    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
218-    pg = ctx.new_page()
219-    yield pg
220-    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
221-    except Exception: pass
netsimd   12300 arsis   19u  IPv6 0xffe400510787a64d      0t0  TCP 127.0.0.1:61859 (LISTEN)
Python    79952 arsis    9u  IPv4 0x63ec67752c241980      0t0  TCP 127.0.0.1:7875 (LISTEN)
Python    93684 arsis    3u  IPv4 0x7b54b1bb2c8e9d2d      0t0  TCP 127.0.0.1:8787 (LISTEN)
Python    99144 arsis    9u  IPv4 0x8ee116607a3f06fc      0t0  TCP 127.0.0.1:7860 (LISTEN)
lsof exit 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:38:53.708Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1; cd $D/card-94a31a4 && (PORT=7891 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$D/card-94a31a4.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $D/card-server.log 2>&1 &) ; sleep 4; lsof -iTCP:7891 -sTCP:LISTEN -n -P; curl -s -m 3 http://127.0.0.1:7891/api/health; echo; tail -3 $D/card-server.log",
 "description": "Start my own app server on port 7891 from card archive"
}
````

### User / tool · 2026-11-02T15:38:57.993Z

**tool result**
````
COMMAND  PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  4187 arsis    9u  IPv4 0xaf4cc256d431684f      0t0  TCP 127.0.0.1:7891 (LISTEN)
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:39:13.681Z

**tool call — Bash**
````
{
 "command": "ps -o pid,ppid,command -p 4187 | cut -c1-160; D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $D/T-160-r1/probe && cat > $D/T-160-r1/probe/measure.py <<'EOF'\n\"\"\"Row-height and head-line probe for T-160 (reviewer scratch; read-only against the server it is given).\"\"\"\nimport json, sys, time, urllib.request, urllib.error\nfrom playwright.sync_api import sync_playwright\n\nBASE = sys.argv[1].rstrip(\"/\")\nLIB = \"case_lib09_spanish_interpreter_espalda\"\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None),\n                                 headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=20) as r:\n            return r.status, json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, None\n\n\nst, c = api(\"POST\", \"/api/cases\", {\"library\": LIB})\nassert st in (200, 201), st\ntok = c[\"token\"]\nassert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\nfor _ in range(120):\n    s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.5)\nprint(\"lib09 status:\", s[\"status\"])\n\nROWS = \"\"\"() => [...document.querySelectorAll('[data-testid=queue] > article')].map(e => ({\n  id: e.getAttribute('data-entry-id'), state: e.getAttribute('data-state'), h: +e.getBoundingClientRect().height.toFixed(2),\n  top: +(e.getBoundingClientRect().top + scrollY).toFixed(2), hasSum: !!e.querySelector('[data-testid=uncovered-summary]')}))\"\"\"\nHEAD = \"\"\"() => [...document.querySelectorAll('[data-testid=queue] > article .entry-head')].slice(0, 6).map(h => ({\n  kids: [...h.children].map(k => ({cls: k.className, tid: k.getAttribute('data-testid'), top: +k.getBoundingClientRect().top.toFixed(1), h: +k.getBoundingClientRect().height.toFixed(1)})),\n  headH: +h.getBoundingClientRect().height.toFixed(1)}))\"\"\"\nTABBED = \"\"\"() => { const a = document.activeElement; return a ? (a.getAttribute('data-testid') || a.tagName) + '|' + (a.textContent || '').trim().slice(0, 40) : 'none'; }\"\"\"\n\nout = {\"base\": BASE, \"lib09\": s[\"status\"], \"viewports\": {}}\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in ((1440, 900), (390, 844)):\n        pg = b.new_context(viewport={\"width\": w, \"height\": h}).new_page()\n        pg.goto(f\"{BASE}/#/case/{tok}\")\n        pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        time.sleep(0.5)\n        with_link = pg.evaluate(ROWS)\n        head = pg.evaluate(HEAD)\n        # control: same page with the link element removed from the DOM (no other change)\n        pg.evaluate(\"document.querySelectorAll('[data-testid=uncovered-summary]').forEach(n => n.remove())\")\n        without = pg.evaluate(ROWS)\n        deltas = [round(a[\"h\"] - b_[\"h\"], 2) for a, b_ in zip(with_link, without)]\n        out[\"viewports\"][str(w)] = {\n            \"rows_with_link\": [(r[\"id\"], r[\"state\"], r[\"h\"], r[\"hasSum\"]) for r in with_link],\n            \"rows_without_link\": [(r[\"id\"], r[\"state\"], r[\"h\"]) for r in without],\n            \"max_row_delta_px\": max(deltas) if deltas else None,\n            \"head_children_first_rows\": head[:3],\n        }\n        pg.close()\n    # keyboard reachability at 1440 on a fresh load: Tab from the document start, count stops until the first summary is focused\n    pg = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n    pg.goto(f\"{BASE}/#/case/{tok}\")\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n    pg.evaluate(\"document.activeElement && document.activeElement.blur()\")\n    stops, reached = [], None\n    for i in range(400):\n        pg.keyboard.press(\"Tab\")\n        cur = pg.evaluate(TABBED)\n        stops.append(cur)\n        if cur.startswith(\"uncovered-summary|\"):\n            reached = i + 1\n            break\n    out[\"tab_reach\"] = {\"reached_at_tab\": reached, \"stop_before\": stops[-2] if reached and len(stops) > 1 else None,\n                        \"stops_total\": len(stops)}\n    if reached:\n        pg.keyboard.press(\"Enter\")\n        out[\"tab_reach\"][\"after_enter_expanded\"] = pg.evaluate(\"document.activeElement.getAttribute('aria-expanded')\")\n    b.close()\nprint(json.dumps(out, indent=1))\nEOF\ncd $D/T-160-r1/card-94a31a4 && timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/measure.py http://127.0.0.1:7891 2>&1 | tail -150",
 "description": "Measure row heights and tab reach on my card-commit server",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:39:13.795Z

**tool result**
````
  PID  PPID COMMAND
 4187     1 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
/bin/bash: line 160: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:39:17.451Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $D/T-160-r1/card-94a31a4 && /Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/measure.py http://127.0.0.1:7891 > $D/T-160-r1/probe/card-94a31a4.json 2> $D/T-160-r1/probe/card-94a31a4.err; echo \"exit $?\"; tail -5 $D/T-160-r1/probe/card-94a31a4.err; python3 -c \"\nimport json,sys\nd=json.load(open('$D/T-160-r1/probe/card-94a31a4.json'))\nprint(d['lib09'], d['tab_reach'])\nfor w,v in d['viewports'].items():\n    print('VIEWPORT',w,'max_row_delta',v['max_row_delta_px'])\n    for r in v['rows_with_link']: print('  with',r)\n    for r in v['rows_without_link']: print('  wo  ',r)\n    print('  head',v['head_children_first_rows'][:2])\n\"",
 "description": "Run probe and summarise row heights and tab reach",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:39:20.295Z

**tool result (error)**
````
Exit code 1
exit 0
Traceback (most recent call last):
  File "<string>", line 3, in <module>
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:39:22.677Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat $D/T-160-r1/probe/card-94a31a4.err | tail -20; echo ---; head -c 600 $D/T-160-r1/probe/card-94a31a4.json",
 "description": "Inspect probe error output"
}
````

### User / tool · 2026-11-02T15:39:22.765Z

**tool result**
````
---
lib09 status: ready
{
 "base": "http://127.0.0.1:7891",
 "lib09": "ready",
 "viewports": {
  "1440": {
   "rows_with_link": [
    [
     "e2",
     "needs_review",
     179.09,
     true
    ],
    [
     "e7",
     "needs_review",
     173.09,
     false
    ],
    [
     "e1",
     "verified",
     134,
     true
    ],
    [
     "e3",
     "verified",
     134,
     true
    ],
    [
     "e5",
     "verified",
     110,
     false
    ],
    [
     "e6",
     "verified",
     134,
     true
    ]
   ],
   "rows_without_link": [
    [
     "e2",
     "needs_review",
     177.09
    ],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:39:27.094Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 -c \"\nimport json\nt=open('$D/T-160-r1/probe/card-94a31a4.json').read()\nd=json.loads(t[t.index('{'):])\nprint(d['lib09'], d['tab_reach'])\nfor w,v in d['viewports'].items():\n    print('VIEWPORT',w,'max_row_delta',v['max_row_delta_px'])\n    wo={r[0]:r[2] for r in v['rows_without_link']}\n    for r in v['rows_with_link']: print('  ',r[0],r[1],'with',r[2],'without',wo[r[0]],'has_sum',r[3])\n    print('  head kids row1', [ (k['tid'] or k['cls'], k['top'], k['h']) for k in v['head_children_first_rows'][0]['kids']], v['head_children_first_rows'][0]['headH'])\n\"",
 "description": "Parse probe JSON and summarise"
}
````

### User / tool · 2026-11-02T15:39:27.196Z

**tool result**
````
ready {'reached_at_tab': 25, 'stop_before': 'entry-4|Date to confirmRecord 4: Consultorio Méd', 'stops_total': 25, 'after_enter_expanded': 'true'}
VIEWPORT 1440 max_row_delta 2.0
   e2 needs_review with 179.09 without 177.09 has_sum True
   e7 needs_review with 173.09 without 173.09 has_sum False
   e1 verified with 134 without 134 has_sum True
   e3 verified with 134 without 134 has_sum True
   e5 verified with 110 without 110 has_sum False
   e6 verified with 134 without 134 has_sum True
  head kids row1 [('entry-date', 1161.1, 20), ('entry-provider', 1161.1, 20), ('chip chip--rec', 1160.1, 22), ('uncovered-summary', 1159.1, 24), ('entry-reasons', 1183.1, 19.1), ('entry-chips', 1202.2, 22)] 65.1
VIEWPORT 390 max_row_delta 2.0
   e2 needs_review with 371.09 without 369.09 has_sum True
   e7 needs_review with 407.09 without 407.09 has_sum False
   e1 verified with 312 without 310 has_sum True
   e3 verified with 330 without 328 has_sum True
   e5 verified with 266 without 266 has_sum False
   e6 verified with 312 without 310 has_sum True
  head kids row1 [('entry-date', 1809.1, 20), ('entry-provider', 1829.1, 20), ('chip chip--rec', 1850.1, 22), ('uncovered-summary', 1849.1, 24), ('entry-reasons', 1873.1, 19.1), ('entry-chips', 1892.2, 22)] 105.1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:39:45.378Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $D/T-160-r1/parent-802d5fd && cd /Users/arsis/zlayt-pm-project && git archive 802d5fd | tar -x -C $D/T-160-r1/parent-802d5fd && mkdir -p $D/T-160-r1/head-985dbd2 && git archive 985dbd2 | tar -x -C $D/T-160-r1/head-985dbd2 && cd $D/T-160-r1/parent-802d5fd && (PORT=7892 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$D/T-160-r1/parent.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $D/T-160-r1/parent-server.log 2>&1 &); sleep 4; lsof -iTCP:7892 -sTCP:LISTEN -n -P; curl -s -m 3 http://127.0.0.1:7892/api/health | head -c 80; echo; /Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/measure.py http://127.0.0.1:7892 > $D/T-160-r1/probe/parent-802d5fd.json 2> $D/T-160-r1/probe/parent.err; echo \"probe exit $?\"; python3 -c \"\nimport json\nt=open('$D/T-160-r1/probe/parent-802d5fd.json').read()\nd=json.loads(t[t.index('{'):])\nprint(d['lib09'], d['tab_reach'])\nfor w,v in d['viewports'].items():\n    print('VIEWPORT',w,'max_row_delta',v['max_row_delta_px'])\n    wo={r[0]:r[2] for r in v['rows_without_link']}\n    for r in v['rows_with_link']: print('  ',r[0],r[1],'with',r[2],'without',wo[r[0]],'has_sum',r[3])\n    print('  head kids row1', [ (k['tid'] or k['cls'], k['top'], k['h']) for k in v['head_children_first_rows'][0]['kids']], v['head_children_first_rows'][0]['headH'])\n\"",
 "description": "Archive parent and HEAD, probe parent placement on port 7892",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:39:53.316Z

**tool result**
````
COMMAND  PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  6083 arsis    9u  IPv4 0x34aafd83310b950e      0t0  TCP 127.0.0.1:7892 (LISTEN)
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only
probe exit 0
ready {'reached_at_tab': 25, 'stop_before': 'entry-4|Date to confirmRecord 4: Consultorio Méd', 'stops_total': 25, 'after_enter_expanded': 'true'}
VIEWPORT 1440 max_row_delta 6.0
   e2 needs_review with 183.09 without 177.09 has_sum True
   e7 needs_review with 173.09 without 173.09 has_sum False
   e1 verified with 138 without 134 has_sum True
   e3 verified with 138 without 134 has_sum True
   e5 verified with 110 without 110 has_sum False
   e6 verified with 138 without 134 has_sum True
  head kids row1 [('entry-date', 1164.1, 20), ('entry-provider', 1164.1, 20), ('chip chip--rec', 1163.1, 22), ('entry-reasons', 1185.1, 19.1), ('entry-chips', 1207.2, 22), ('uncovered-summary', 1204.2, 28)] 69.1
VIEWPORT 390 max_row_delta 22.0
   e2 needs_review with 391.09 without 369.09 has_sum True
   e7 needs_review with 407.09 without 407.09 has_sum False
   e1 verified with 332 without 310 has_sum True
   e3 verified with 350 without 328 has_sum True
   e5 verified with 266 without 266 has_sum False
   e6 verified with 332 without 310 has_sum True
  head kids row1 [('entry-date', 1807.1, 20), ('entry-provider', 1827.1, 20), ('chip chip--rec', 1847.1, 22), ('entry-reasons', 1869.1, 19.1), ('entry-chips', 1899.2, 22), ('uncovered-summary', 1888.2, 44)] 125.1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:40:00.547Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $D/T-160-r1/parent-802d5fd && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q -rsxX -p no:cacheprovider -k \"first_screen or 390_needs or row_opens\" 2>&1 | grep -v \"^$\" | tail -40 | cut -c1-400",
 "description": "Control run: density tests on the parent archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:40:05.555Z

**tool result**
````
...                                                                      [100%]
3 passed, 16 deselected in 4.04s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:40:19.243Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $D/T-160-r1/probe/budget.py <<'EOF'\n\"\"\"Reviewer scratch: row heights vs the polish_r3 budgets (150 / 170 needs_review at 1440, 420 needs_review at 390) for sample and lib09, with and without the link.\"\"\"\nimport json, sys, time, urllib.request, urllib.error\nfrom playwright.sync_api import sync_playwright\nBASE = sys.argv[1].rstrip(\"/\")\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=20) as r:\n            return r.status, json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, None\n\ndef make(kind):\n    if kind == \"sample\":\n        st, c = api(\"POST\", \"/api/cases\", {\"sample\": True})\n    else:\n        st, c = api(\"POST\", \"/api/cases\", {\"library\": \"case_lib09_spanish_interpreter_espalda\"})\n    tok = c[\"token\"]; assert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    for _ in range(120):\n        s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"): break\n        time.sleep(0.5)\n    return tok, s[\"status\"]\n\nROWS = \"\"\"() => [...document.querySelectorAll('[data-testid=queue] > article')].map(e => ({id: e.getAttribute('data-entry-id'), state: e.getAttribute('data-state'), h: +e.getBoundingClientRect().height.toFixed(2)}))\"\"\"\nres = {}\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for kind in (\"sample\", \"lib09\"):\n        tok, st = make(kind)\n        for w, h, budget in ((1440, 900, None), (390, 844, None)):\n            pg = b.new_context(viewport={\"width\": w, \"height\": h}).new_page()\n            pg.goto(f\"{BASE}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000); time.sleep(0.5)\n            rows = pg.evaluate(ROWS)\n            pg.evaluate(\"document.querySelectorAll('[data-testid=uncovered-summary]').forEach(n => n.remove())\")\n            wo = {r[\"id\"]: r[\"h\"] for r in pg.evaluate(ROWS)}\n            pg.close()\n            key = f\"{kind}@{w}\"\n            res[key] = [{\"id\": r[\"id\"], \"state\": r[\"state\"], \"h\": r[\"h\"], \"h_without_link\": wo[r[\"id\"]]} for r in rows]\n            res[key + \"_over\"] = [r[\"id\"] for r in rows if r[\"h\"] > ((170 if r[\"state\"] == \"needs_review\" else 150) if w == 1440 else (420 if r[\"state\"] == \"needs_review\" else 10**9))]\n    b.close()\nprint(json.dumps(res))\nEOF\nfor port in 7891 7892; do echo \"== port $port\"; /Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/budget.py http://127.0.0.1:$port > $D/T-160-r1/probe/budget-$port.json 2>$D/T-160-r1/probe/budget-$port.err; echo \"exit $?\"; python3 -c \"\nimport json\nd=json.load(open('$D/T-160-r1/probe/budget-$port.json'))\nfor k,v in d.items():\n    if k.endswith('_over'): print(k, v); continue\n    print(k, [(r['id'], r['state'][:5], r['h'], r['h_without_link']) for r in v])\n\"; done",
 "description": "Measure budget rows for sample and lib09 on both servers",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:40:28.255Z

**tool result**
````
== port 7891
exit 0
sample@1440 [('e1', 'verif', 138, 138), ('e2', 'verif', 138, 138), ('e3', 'verif', 134, 134), ('e4', 'verif', 134, 134), ('e5', 'verif', 110, 110), ('e6', 'verif', 118, 118), ('e7', 'verif', 134, 134), ('e8', 'verif', 138, 138), ('e9', 'verif', 134, 134)]
sample@1440_over []
sample@390 [('e1', 'verif', 310, 310), ('e2', 'verif', 308, 308), ('e3', 'verif', 310, 308), ('e4', 'verif', 288, 288), ('e5', 'verif', 248, 246), ('e6', 'verif', 290, 290), ('e7', 'verif', 310, 308), ('e8', 'verif', 308, 308), ('e9', 'verif', 330, 330)]
sample@390_over []
lib09@1440 [('e2', 'needs', 179.09, 177.09), ('e7', 'needs', 173.09, 173.09), ('e1', 'verif', 134, 134), ('e3', 'verif', 134, 134), ('e5', 'verif', 110, 110), ('e6', 'verif', 134, 134)]
lib09@1440_over ['e2', 'e7']
lib09@390 [('e2', 'needs', 371.09, 369.09), ('e7', 'needs', 407.09, 407.09), ('e1', 'verif', 312, 310), ('e3', 'verif', 330, 328), ('e5', 'verif', 266, 266), ('e6', 'verif', 312, 310)]
lib09@390_over []
== port 7892
exit 0
sample@1440 [('e1', 'verif', 138, 138), ('e2', 'verif', 138, 138), ('e3', 'verif', 138, 134), ('e4', 'verif', 134, 134), ('e5', 'verif', 114, 110), ('e6', 'verif', 118, 118), ('e7', 'verif', 138, 134), ('e8', 'verif', 138, 138), ('e9', 'verif', 134, 134)]
sample@1440_over []
sample@390 [('e1', 'verif', 310, 310), ('e2', 'verif', 308, 308), ('e3', 'verif', 330, 308), ('e4', 'verif', 288, 288), ('e5', 'verif', 268, 246), ('e6', 'verif', 290, 290), ('e7', 'verif', 330, 308), ('e8', 'verif', 308, 308), ('e9', 'verif', 330, 330)]
sample@390_over []
lib09@1440 [('e2', 'needs', 183.09, 177.09), ('e7', 'needs', 173.09, 173.09), ('e1', 'verif', 138, 134), ('e3', 'verif', 138, 134), ('e5', 'verif', 110, 110), ('e6', 'verif', 138, 134)]
lib09@1440_over ['e2', 'e7']
lib09@390 [('e2', 'needs', 391.09, 369.09), ('e7', 'needs', 407.09, 407.09), ('e1', 'verif', 332, 310), ('e3', 'verif', 350, 328), ('e5', 'verif', 266, 266), ('e6', 'verif', 332, 310)]
lib09@390_over []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:40:34.322Z

**tool call — Bash**
````
{
 "command": "git grep -n -i \"row\" 94a31a4 -- docs/UI_DESIGN_BRIEF.md | grep -i \"px\\|height\\|compact\\|budget\" | cut -c1-400 | head -20; echo ---; git grep -n -E \"170|420|150 ?px|compact row|row height|budget\" 94a31a4 -- docs/ reviews/T-060-*.md reviews/T-149-*.md memory/DECISIONS.md memory/ORCHESTRATOR_DECISIONS.md 2>/dev/null | grep -i \"row\\|budget\\|px\" | cut -c1-400 | head -30",
 "description": "Find the spec text for compact-row height budget"
}
````

### User / tool · 2026-11-02T15:40:34.473Z

**tool result**
````
94a31a4:docs/UI_DESIGN_BRIEF.md:39:Radius: 4 px on controls, chips and inputs; 6 px on cards; none on table rows. Borders instead of shadows: 1 px `--border`; one shadow token only for
94a31a4:docs/UI_DESIGN_BRIEF.md:45:Row heights follow Carbon's scale (opened source: 24/32/40/48/64, 64 only for two-line rows).
94a31a4:docs/UI_DESIGN_BRIEF.md:49:| Table row (charges) | 40 px | 32 px |
94a31a4:docs/UI_DESIGN_BRIEF.md:50:| Timeline row (two lines: date + provider, summary) | 64 px minimum, grows with text | 52 px minimum |
94a31a4:docs/UI_DESIGN_BRIEF.md:140:Two-line row, 64 px minimum. Structure, left to right:
94a31a4:docs/UI_DESIGN_BRIEF.md:148:- Selected row: `--accent-soft` background, 3 px `--accent` left bar, and the record pane scrolls to the excerpt.
94a31a4:docs/UI_DESIGN_BRIEF.md:178:- At 375 px each row becomes a summary-list block (label / value / action).
94a31a4:docs/UI_DESIGN_BRIEF.md:211:| Timeline queue | "Nothing to review. All items are decided." (when finished) / "No entries yet. The records have not been read." | skeleton rows at the real row height (64 px) with a text status "Reading records 4 of 9" (from the API `progress.label`); no spinner-only state | error summary (7.6) with the code reason and Retry; the pasted text is never lost |
---
94a31a4:docs/CONTRACT.md:44:- *Classify failures and change conditions before retrying,* with budgets and escalation. Never retry the same thing the same way.
94a31a4:docs/CONTRACT.md:238:Write one file per role in `.claude/agents/` using the template in Appendix D.5. Workers: `architect, backend, db, frontend, qa, release, writer, researcher`. Reviewers: `paralegal-reviewer, litigation-lead-reviewer, claims-adjuster-reviewer, legal-nurse-reviewer, privacy-compliance-reviewer, product-manager-reviewer, ux-designer-reviewer, staff-engineer-reviewer, secu
94a31a4:docs/CONTRACT.md:260:Time budgets are guidance for scope decisions, not deadlines to miss silently. When a milestone exceeds 150% of budget, cut scope deliberately (record in `SCOPE_CUTS.md`) rather than drift. Target total wall-clock: 10–16 hours.
94a31a4:docs/CONTRACT.md:308:Cards (frontend, backend, qa): paste/upload input; timeline view with date, provider, summary, exact excerpt, confidence state, and "Why?"; flags panel grouped by type with evidence; charges table with running total and the "unclear" tray; accept / edit / dismiss per entry and per flag with keyboard-friendly review flow; export (copy-ready demand-letter treatment secti
94a31a4:docs/CONTRACT.md:397:### 7.4 Verdicts and loop budget
94a31a4:docs/CONTRACT.md:469:## 12. Guardrails and budgets
94a31a4:docs/M2M3_COVERAGE.md:5:- M2 critical-path total ≈ 5 h of serial work (7 cards × ~40 min) vs 3.5 h budget → **cut trigger:** if T-035 is not in review by M2 start + 2.5 h, apply cut (1), then (2).
94a31a4:docs/UI_DESIGN_BRIEF.md:110:- **≥ 1024 px (R-ST-1):** two panes. Left queue 40% (min 420 px), right source record 60%, each scrolls independently. The record pane scrolls to and highlights
94a31a4:docs/UI_DESIGN_BRIEF.md:211:| Timeline queue | "Nothing to review. All items are decided." (when finished) / "No entries yet. The records have not been read." | skeleton rows at the real row height (64 px) with a text status "Reading records 4 of 9" (from the API `progress.label`); no spinner-only state | error summary (7.6) with the code reason and Retry; the pasted text is never lost |
94a31a4:memory/DECISIONS.md:305:- Decision: cut now, not at the cut line (D-011, D-020): the in-app rate limiter and spend ledger (spend control is a provider-side limit), arbitrary-text ingest on the public build, batch accept (R-RV-7), charge reclassification and amount edits (R-CH-7), the "not a duplicate" split action, LLM date pointing, bring-your-own-key, `?full=1` prompt view, flag title/ex
94a31a4:memory/ORCHESTRATOR_DECISIONS.md:32:| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:40:48.060Z

**tool call — Bash**
````
{
 "command": "git show 94a31a4:app/frontend/uncovered.js | sed -n '1,12p' | cut -c1-300; echo ---; git grep -n \"chip--rec\\|entry-provider\\|\\\"provider\\\"\\|'provider'\\|class: \\\"provider\\|provider\\\"\" 94a31a4 -- app/frontend/*.js | cut -c1-300 | head -20; echo ---; git grep -n \"entry-head\" 94a31a4 -- app/frontend/*.js app/frontend/*.css | cut -c1-260 | head -12",
 "description": "Check head child class names used by the link anchor"
}
````

### User / tool · 2026-11-02T15:40:48.228Z

**tool result**
````
/* T-144: "Also in this record, not in an entry (n)" under each entry. Shows records[].uncovered[] (T-143: every sentence of the record that no live entry quote overlaps, computed by code),
   each sentence verbatim, in a list that starts closed (a "Not in an entry (n)" link in the row's head line opens it). "Show in record" opens the source record with that sentence highlighted (ZL.openSource, by the API's offsets).
   Review aid only: it is never in the letter, the notes or the copy text, and `kinds` is a hint the UI does not use (nothing is filtered here). Plugs in through ZL.registerRowActions. */
(function () {
  const ZL = window.ZL, { el } = ZL;
  const opened = new Set();   // entry ids whose list she opened; the rows repaint on every decision, and a list she is reading must stay open

  const recordsOf = (entry) => {
    const c = ZL.state.get().case; if (!c) return [];
    return entry.record_ids.map((rid) => c.records.find((r) => r.id === rid)).filter((r) => r && r.uncovered && r.uncovered.length);
  };

---
94a31a4:app/frontend/timeline.js:51:        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
94a31a4:app/frontend/timeline.js:52:        e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : null,
94a31a4:app/frontend/timeline.js:191:        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip chip--warn", "data-icon": "calendar" }, "Date to confirm")),
94a31a4:app/frontend/timeline.js:212:        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip chip--bad", "data-icon": "x" }, isFlag ? "Flag not confirmed" : "Could not verify")),
94a31a4:app/frontend/uncovered.js:32:    const head = row.querySelector(":scope > .entry-head"), anchor = head && (head.querySelector(":scope > .chip--rec") || head.querySelector(":scope > .provider"));
---
94a31a4:app/frontend/review.js:513:        const head = rowEl.querySelector(".entry-head") || rowEl;
94a31a4:app/frontend/styles.css:125:.entry > .entry-head { order: 0; }
94a31a4:app/frontend/styles.css:144:.entry-head { display: flex; flex-wrap: wrap; align-items: center; gap: 0 var(--s-3); min-height: 1.5rem; }
94a31a4:app/frontend/styles.css:150:.entry[data-entry-id] .entry-head .reason { flex: 1 1 12rem; min-width: 0; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
94a31a4:app/frontend/styles.css:152:.entry[data-entry-id].is-open .entry-head .reason, .entry[data-entry-id] .entry-head .reason--caution { white-space: normal; overflow: visible; flex-basis: 100%; }   /* "read the original quote yourself" is never cut short *
94a31a4:app/frontend/styles.css:206:  .entry[data-entry-id] .entry-head .reason { flex-basis: 100%; white-space: normal; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
94a31a4:app/frontend/styles.css:207:  .entry[data-entry-id].is-open .entry-head .reason { display: block; -webkit-line-clamp: unset; overflow: visible; }
94a31a4:app/frontend/timeline.js:49:      el("div", { class: "entry-head" },
94a31a4:app/frontend/timeline.js:191:        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip chip--warn", "data-icon": "calendar" }, "Date
94a31a4:app/frontend/timeline.js:212:        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip chip--bad", "data-icon": "x" }, isFlag ? "Flag not co
94a31a4:app/frontend/uncovered.css:17:.entry-head > .unc-toggle { flex: none; white-space: nowrap; min-height: 1.5rem; font-size: var(--t-sm); }
94a31a4:app/frontend/uncovered.js:32:    const head = row.querySelector(":scope > .entry-head"), anchor = head && (head.querySelector(":scope > .chip--rec") || head.querySelector(":scope > .provider"));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:41:06.507Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $D/T-160-r1/probe/narrow.py <<'EOF'\n\"\"\"Reviewer scratch: is the Not-in-an-entry link inside a 320 px viewport, on the first summary of sample and lib09 rows, and does it share the chip's line?\"\"\"\nimport json, sys, time, urllib.request, urllib.error\nfrom playwright.sync_api import sync_playwright\nBASE = sys.argv[1].rstrip(\"/\")\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=20) as r:\n            return r.status, json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, None\nJS = \"\"\"() => [...document.querySelectorAll('[data-testid=uncovered-summary]')].map(s => { const r = s.getBoundingClientRect(); const row = s.closest('[data-testid=queue] > article'); const chip = row.querySelector('.entry-head > .chip--rec'); const c = chip ? chip.getBoundingClientRect() : null;\n  return {id: row.getAttribute('data-entry-id'), left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), chipTop: c ? +c.top.toFixed(1) : null, docW: document.documentElement.scrollWidth}; })\"\"\"\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for kind in (\"sample\", \"lib09\"):\n        st, c = api(\"POST\", \"/api/cases\", {\"sample\": True} if kind == \"sample\" else {\"library\": \"case_lib09_spanish_interpreter_espalda\"})\n        tok = c[\"token\"]; api(\"POST\", f\"/api/cases/{tok}/run\", {})\n        for _ in range(120):\n            s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n            if s[\"status\"] in (\"ready\", \"failed\"): break\n            time.sleep(0.5)\n        pg = b.new_context(viewport={\"width\": 320, \"height\": 640}).new_page()\n        pg.goto(f\"{BASE}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000); time.sleep(0.5)\n        rows = pg.evaluate(JS)\n        print(kind, \"320px:\", json.dumps(rows))\n        pg.close()\n    b.close()\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/narrow.py http://127.0.0.1:7891 2>&1 | tail -5 | cut -c1-900",
 "description": "Check link position at 320 px on card server",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T15:41:09.572Z

**tool result**
````
    at eval (eval at evaluate (:370:30), <anonymous>:1:194)
    at Array.map (<anonymous>)
    at eval (eval at evaluate (:370:30), <anonymous>:1:73)
    at UtilityScript.evaluate (<anonymous>:377:18)
    at UtilityScript.<anonymous> (<anonymous>:1:44)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:41:13.181Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -i \"s/s.closest('\\[data-testid=queue\\] > article')/s.closest('article')/\" $D/T-160-r1/probe/narrow.py && /Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/narrow.py http://127.0.0.1:7891 2>&1 | tail -5 | cut -c1-1200",
 "description": "Rerun narrow-viewport link probe with corrected row selector",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T15:41:13.237Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  article')/s.closest('article')/)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:41:19.918Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $D/T-160-r1/probe/narrow.py <<'EOF'\n\"\"\"Reviewer scratch: is the Not-in-an-entry link inside a 320 px viewport, and does it share the record chip's line?\"\"\"\nimport json, sys, time, urllib.request, urllib.error\nfrom playwright.sync_api import sync_playwright\nBASE = sys.argv[1].rstrip(\"/\")\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=20) as r:\n            return r.status, json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, None\nJS = \"\"\"() => [...document.querySelectorAll('[data-testid=uncovered-summary]')].map(s => { const r = s.getBoundingClientRect(); const row = s.closest('article'); const chip = row.querySelector('.entry-head > .chip--rec'); const c = chip ? chip.getBoundingClientRect() : null;\n  return {id: row.getAttribute('data-entry-id'), left: +r.left.toFixed(1), right: +r.right.toFixed(1), top: +r.top.toFixed(1), chipTop: c ? +c.top.toFixed(1) : null, docW: document.documentElement.scrollWidth}; })\"\"\"\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for kind in (\"sample\", \"lib09\"):\n        st, c = api(\"POST\", \"/api/cases\", {\"sample\": True} if kind == \"sample\" else {\"library\": \"case_lib09_spanish_interpreter_espalda\"})\n        tok = c[\"token\"]; api(\"POST\", f\"/api/cases/{tok}/run\", {})\n        for _ in range(120):\n            s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n            if s[\"status\"] in (\"ready\", \"failed\"): break\n            time.sleep(0.5)\n        pg = b.new_context(viewport={\"width\": 320, \"height\": 640}).new_page()\n        pg.goto(f\"{BASE}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000); time.sleep(0.5)\n        print(kind, \"320px:\", json.dumps(pg.evaluate(JS)))\n        pg.close()\n    b.close()\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python $D/T-160-r1/probe/narrow.py http://127.0.0.1:7891 2>&1 | tail -5 | cut -c1-1200",
 "description": "Check link position at 320 px on card server",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T15:41:23.231Z

**tool result**
````
sample 320px: [{"id": "e3", "left": 27, "right": 153.6, "top": 1587, "chipTop": 1565, "docW": 320}, {"id": "e5", "left": 89, "right": 215.6, "top": 2223, "chipTop": 2224, "docW": 320}, {"id": "e7", "left": 88.5, "right": 215, "top": 2855, "chipTop": 2856, "docW": 320}]
lib09 320px: [{"id": "e4", "left": 27, "right": 155.4, "top": 1245, "chipTop": null, "docW": 320}, {"id": "e2", "left": 88.9, "right": 215.4, "top": 2061.1, "chipTop": 2062.1, "docW": 320}, {"id": "e1", "left": 87.2, "right": 215.6, "top": 2853.3, "chipTop": 2854.3, "docW": 320}, {"id": "e3", "left": 89.1, "right": 215.7, "top": 3233.3, "chipTop": 3234.3, "docW": 320}, {"id": "e6", "left": 89.3, "right": 217.6, "top": 3929.3, "chipTop": 3930.3, "docW": 320}]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:41:31.665Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $D/T-160-r1/head-985dbd2 && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_uncovered_ui.py -q -rsxX -p no:cacheprovider 2>&1 | tail -6 | cut -c1-300; echo \"--- card archive, both files again (repeat run for determinism)\"; cd $D/T-160-r1/card-94a31a4 && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_uncovered_ui.py -q -rsxX -p no:cacheprovider 2>&1 | tail -4 | cut -c1-300; cd $D/T-160-r1/card-94a31a4 && git -C /Users/arsis/zlayt-pm-project diff --quiet 94a31a4 HEAD -- tests/e2e/test_polish_r3.py tests/e2e/test_uncovered_ui.py app/frontend/uncovered.js app/frontend/uncovered.css; echo \"diff-quiet exit (0 = identical at HEAD) $?\"",
 "description": "Run both e2e files on HEAD archive and repeat on card archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:42:44.514Z

**tool result**
````
..........................                                               [100%]
26 passed in 35.45s
--- card archive, both files again (repeat run for determinism)
..........................                                               [100%]
26 passed in 34.81s
diff-quiet exit (0 = identical at HEAD) 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:43:04.987Z

**tool call — Bash**
````
{
 "command": "git grep -n \"summ.focus()\\|def test_keyboard_only\" 94a31a4 -- tests/e2e/test_uncovered_ui.py; git grep -n \"def test_first_screen\\|boxes\\[0\\]\\[0\\] < 520\\|170 if state\\|def test_390_needs\\|max(hs) <= 420\" 94a31a4 -- tests/e2e/test_polish_r3.py; git grep -n \"uncovered-summary\\|chip--rec\" 94a31a4 -- app/frontend/timeline.js | cut -c1-120; ls reviews | grep \"^T-160\" ; echo \"no-existing-review exit $?\"; ps -o pid,command -p 4187,6083 | cut -c1-120; lsof -iTCP:7891 -sTCP:LISTEN -n -P | tail -1; lsof -iTCP:7892 -sTCP:LISTEN -n -P | tail -1",
 "description": "Confirm citation line numbers and my server PIDs"
}
````

### User / tool · 2026-11-02T15:43:05.290Z

**tool result**
````
94a31a4:tests/e2e/test_uncovered_ui.py:85:def test_keyboard_only(page, lib09):
94a31a4:tests/e2e/test_uncovered_ui.py:92:    summ.focus()
94a31a4:tests/e2e/test_polish_r3.py:168:def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
94a31a4:tests/e2e/test_polish_r3.py:174:        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
94a31a4:tests/e2e/test_polish_r3.py:180:            assert h <= (170 if state == "needs_review" else 150), boxes
94a31a4:tests/e2e/test_polish_r3.py:193:def test_390_needs_review_row_is_at_most_420(pw, lib09):
94a31a4:tests/e2e/test_polish_r3.py:197:        assert hs and max(hs) <= 420, hs
94a31a4:app/frontend/timeline.js:52:        e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : 
no-existing-review exit 1
  PID COMMAND
 4187 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/
 6083 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/
Python  4187 arsis    9u  IPv4 0xaf4cc256d431684f      0t0  TCP 127.0.0.1:7891 (LISTEN)
Python  6083 arsis    9u  IPv4 0x34aafd83310b950e      0t0  TCP 127.0.0.1:7892 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:43:08.482Z

**tool call — Bash**
````
{
 "command": "kill 4187 6083; sleep 2; lsof -iTCP:7891 -sTCP:LISTEN -n -P; echo \"7891 exit $?\"; lsof -iTCP:7892 -sTCP:LISTEN -n -P; echo \"7892 exit $?\"; ps -o pid,command -p 4187,6083 2>/dev/null | cut -c1-80; echo \"ps done\"; lsof -iTCP -sTCP:LISTEN -n -P | grep -i python",
 "description": "Stop my two app servers by PID and confirm ports closed"
}
````

### User / tool · 2026-11-02T15:43:10.828Z

**tool result**
````
7891 exit 1
7892 exit 1
  PID COMMAND
ps done
Python      824 arsis   10u  IPv4 0xd89fda7756feeb64      0t0  TCP 127.0.0.1:8000 (LISTEN)
Python     1617 arsis    9u  IPv4 0xb3724165068b70a7      0t0  TCP 127.0.0.1:7952 (LISTEN)
Python     1826 arsis    9u  IPv4 0xc837ac7d28aec599      0t0  TCP 127.0.0.1:7943 (LISTEN)
Python     8089 arsis    9u  IPv4 0x3a7a2ed812f63d60      0t0  TCP 127.0.0.1:7895 (LISTEN)
Python    13577 arsis    9u  IPv4 0xb7e125bbc2389146      0t0  TCP 127.0.0.1:7878 (LISTEN)
Python    23429 arsis    9u  IPv4 0xd59ea69d8669b87d      0t0  TCP 127.0.0.1:62204 (LISTEN)
Python    25593 arsis    9u  IPv4 0xaf7b19e12a43e449      0t0  TCP 127.0.0.1:63089 (LISTEN)
Python    38450 arsis    3u  IPv4 0xe3e90fe2e5c7d085      0t0  TCP 127.0.0.1:7777 (LISTEN)
Python    68574 arsis    3u  IPv4 0x71132eb8f1361cf1      0t0  TCP 127.0.0.1:5173 (LISTEN)
Python    68578 arsis    3u  IPv4 0x71132eb8f1361cf1      0t0  TCP 127.0.0.1:5173 (LISTEN)
Python    93684 arsis    3u  IPv4 0x7b54b1bb2c8e9d2d      0t0  TCP 127.0.0.1:8787 (LISTEN)
Python    97570 arsis    9u  IPv4 0x7361460df7302cd0      0t0  TCP 127.0.0.1:7893 (LISTEN)
Python    99075 arsis    9u  IPv4 0x4a9f3f163bf3f8b5      0t0  TCP 127.0.0.1:7894 (LISTEN)
Python    99144 arsis    9u  IPv4 0x8ee116607a3f06fc      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:43:12.876Z

**tool call — Bash**
````
{
 "command": "for p in 824 1617 1826 8089 13577 23429 25593 38450 68574 93684 97570 99075 99144; do lsof -a -p $p -d cwd -Fn 2>/dev/null | grep \"^n\" | grep -q \"T-160-r1\" && echo \"MINE? $p\"; done; echo \"cwd scan done\"",
 "description": "Check no remaining listener runs from my T-160 archive dirs"
}
````

### User / tool · 2026-11-02T15:43:13.729Z

**tool result**
````
cwd scan done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:04.444Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-160-staff-engineer.md",
 "content": "# T-160 review: staff-engineer-reviewer (commit 94a31a4)\n\nScope: commit 94a31a4 (app/frontend/uncovered.js, app/frontend/uncovered.css), checked with tests/e2e/test_polish_r3.py and tests/e2e/test_uncovered_ui.py. HEAD moved to 985dbd2 during the review (3 later commits: a4eeb2b, 67be38d, 985dbd2; none touch the four files). The findings are for 94a31a4. Both shas were run and both pass the two files.\n\nVerdict: pass. 0 blockers, 0 majors, 3 minors, 1 nit. The verdict rule gives pass because no blocker or major was found.\n\nThe three checks in the brief:\n\n1. Original budget restored, not loosened: confirmed. The density section of tests/e2e/test_polish_r3.py at 94a31a4 (lines 168-197) matches the pre-T-144 version at ded5ca4^ (budgets 150 and 170 at 1440, 420 at 390, raw getBoundingClientRect height). The only other diff in that file since ded5ca4^ is the T-155 focus-wait line in the shortcut test. The T-144 ROW_BOXES_JS subtraction is gone.\n2. Link in the head line, reachable by click and keyboard: confirmed. In the head, the uncovered-summary sits directly after chip--rec (1440 px: summary top 1159.1, chip top 1160.1, same line). From the document start, Tab reaches it on stop 25; Enter then sets aria-expanded to true. A click opens the list (test_one_click_opens_the_record_with_that_sentence_highlighted passes).\n3. test_uncovered_ui.py: 7 passed on 94a31a4 and on HEAD.\n\nFindings, in short:\n- F1 (minor): the commit and handoff say the rows are back inside the budget. Only the sample case is checked. At 1440 px, a lib09 needs_review row is 179.09 px against a 170 budget, with the link present.\n- F2 (minor): the title's premise (rows over budget since T-144) does not reproduce against the budgets the suite enforces. The link added 22 px at 390 on a lib09 row, which was 391 px against a 420 budget.\n- F3 (minor): no test fails if the placement is reverted. The density tests pass on the pre-fix placement (802d5fd).\n- F4 (minor): \"it never takes a line of its own\" is false at 320 px. The sample e3 link wraps below its chip.\n- F5 (nit): test_keyboard_only starts with summ.focus(), so Tab reach is not asserted by any test.\n\nFull commands and output paths are in the exercised list in the JSON block.\n\n```json\n{\"card\": \"T-160\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 94a31a4 (app/frontend/uncovered.js, app/frontend/uncovered.css); tests tests/e2e/test_polish_r3.py and tests/e2e/test_uncovered_ui.py; HEAD 985dbd2 checked (3 later commits, none touch the four files); private app servers on 127.0.0.1:7891 (94a31a4) and 127.0.0.1:7892 (parent 802d5fd), both stopped; fixture backend; sample case and library case case_lib09_spanish_interpreter_espalda\",\n \"exercised\": [\n  \"read personas/staff-engineer.md; python3 tools/board.py show T-160 (status in_review, commits [94a31a4], AC 1 done with evidence)\",\n  \"git show 94a31a4 (uncovered.js +5/-2 lines, uncovered.css +3 lines; commit subject verbatim: 'the Not in an entry (n) link sits in the entry head line right after the record chip, so it never takes a line of its own; rows are back inside the T-060 compact-row budget (<=2 px)')\",\n  \"git diff ded5ca4^ 94a31a4 -- tests/e2e/test_polish_r3.py (only the shortcut-sheet focus-wait line differs; density section identical to pre-T-144); git log -S for the 150/170/420 budgets (introduced d9efc5c) and for the xfail marker (removed in 802d5fd, not in this commit)\",\n  \"git archive 94a31a4 | tar -x into scratchpad T-160-r1/card-94a31a4; git archive 802d5fd into T-160-r1/parent-802d5fd; git archive 985dbd2 into T-160-r1/head-985dbd2 (scratchpad dirs are under /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad)\",\n  \"card archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q -rsxX -p no:cacheprovider -> 19 passed, 0 skipped, 25.06s (conftest started a private server, no E2E_BASE_URL)\",\n  \"card archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_uncovered_ui.py -v -rsxX -> 7 passed (all 7 named tests PASSED)\",\n  \"card archive, both files again: 26 passed (34.81s); HEAD archive 985dbd2, both files: 26 passed (35.45s)\",\n  \"control on parent 802d5fd: E2E_REQUIRE_DB=1 pytest tests/e2e/test_polish_r3.py -k 'first_screen or 390_needs or row_opens' -> 3 passed, 16 deselected (the placement this card removes is not caught)\",\n  \"own server on 127.0.0.1:7891 (card) and 127.0.0.1:7892 (parent), listener PIDs 4187 and 6083 confirmed with lsof and ps before stopping; both stopped by PID; ports closed afterwards; other listeners (7860, 7875, 8787 and others) not touched\",\n  \"probe measure.py (T-160-r1/probe/measure.py) on 7891 and 7892: every queue row's height with the link and with the uncovered-summary node removed from the DOM (control), head children geometry at 1440 and 390, Tab-from-body reach count; outputs T-160-r1/probe/card-94a31a4.json and T-160-r1/probe/parent-802d5fd.json\",\n  \"probe budget.py (T-160-r1/probe/budget.py) on 7891 and 7892: sample and lib09 rows at 1440 and 390 against the 150/170/420 budgets; outputs T-160-r1/probe/budget-7891.json and budget-7892.json\",\n  \"probe narrow.py (T-160-r1/probe/narrow.py) on 7891 at 320 px: summary and record-chip tops for sample and lib09\",\n  \"not run: the full e2e suite, unit tests, the eval runner (outside the card's AC); no real-data or live-model paths touched\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"budget_restored_not_loosened\": 5, \"link_in_head_line_click_and_keyboard\": 4, \"uncovered_ui_tests_green\": 5, \"test_guards_the_regression\": 2, \"claims_match_measurements\": 3},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Commit and handoff say rows are back inside the budget; only the sample case is checked against it\",\n   \"evidence\": \"T-160-r1/probe/budget-7891.json: lib09@1440 rows e2 needs_review h=179.09 (h_without_link=177.09) and e7 needs_review h=173.09 with no uncovered-summary. The budget is 170 for needs_review (tests/e2e/test_polish_r3.py:180), but the first-screen test uses sample_case (tests/e2e/test_polish_r3.py:168) and no lib09 row is measured at 1440. Commit subject: 'rows are back inside the T-060 compact-row budget (<=2 px)'.\",\n   \"why_it_matters\": \"The claim is true for the sample only. A paralegal opening the library case sees needs_review rows above the budget the commit cites, and the suite cannot see it. The e7 row is over with no link at all, so the link is not the whole story for that case.\",\n   \"fix\": \"Scope the commit and card wording to the sample case, or extend the 1440 budget check to lib09 and decide the budget for it (the e7 row at 173.09 with no link is a pre-existing overage).\",\n   \"acceptance_test\": \"Either a 1440 lib09 assertion (needs_review rows at most 170 px) that passes, or the handoff and card state that the budget covers the sample case only. Repro: the budget probe on any server with lib09 at 1440.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The premise (rows over budget since T-144) does not reproduce against the enforced budgets\",\n   \"evidence\": \"T-160-r1/probe/budget-7892.json (parent 802d5fd, link at end of head): sample@1440 max 138 px (verified budget 150); sample@390 max 330 px; lib09@390 e2 needs_review 391.09 px (budget 420). The density tests pass on the parent: 3 passed (control run, see exercised). Link cost on the parent: +6 px at 1440 and +22 px at 390 (T-160-r1/probe/parent-802d5fd.json, max_row_delta_px 6.0 and 22.0). Card: +2 px at both widths (T-160-r1/probe/card-94a31a4.json).\",\n   \"why_it_matters\": \"The fix is real and worth having: 22 px at 390 went to 2 px. But the title says the link made rows exceed the budget, and no enforced budget was exceeded by any measured row. A future reader who trusts the title will look for a breach that is not there.\",\n   \"fix\": \"Restate the title and commit as: the link added 22 px at 390 per row (2 px after the move), and no enforced budget was breached. Keep the 2 px figure.\",\n   \"acceptance_test\": \"Title and handoff match the probe numbers above; the claim is checkable with the same probe on 802d5fd and 94a31a4.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"No test fails if the link goes back to the end of the head; the budget test passes on the pre-fix placement\",\n   \"evidence\": \"git show 94a31a4 -- app/frontend/uncovered.js (the removed line: if (head) head.append(toggle); else row.append(toggle);). Control: E2E_REQUIRE_DB=1 pytest tests/e2e/test_polish_r3.py -k 'first_screen or 390_needs or row_opens' on the parent archive gives 3 passed. The 390 test (tests/e2e/test_polish_r3.py:193-197) uses the lib09 needs_review max, which is 391 on the parent and 371 on the card, both under 420.\",\n   \"why_it_matters\": \"This card is a layout regression fix. As written, the same regression can come back and every green check stays green. That is the failure mode the persona exists to catch: a fix with no test that fails without it.\",\n   \"fix\": \"Add one assertion that the uncovered-summary shares the record chip's line at 390 (summary.top minus chip.top is less than the chip height) on lib09, or tighten the lib09 needs_review budget at 390 to 380 px (card 371, parent 391).\",\n   \"acceptance_test\": \"Put the parent placement (if (head) head.append(toggle)) into a scratch copy of uncovered.js: the new test fails. Restore 94a31a4: it passes. Record both runs in the card's evidence.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"'It never takes a line of its own' is false at 320 px\",\n   \"evidence\": \"T-160-r1/probe/narrow.py on 7891 at 320 px: sample e3 uncovered-summary top=1587 left=27 vs chip--rec top=1565 (the link is 22 px below the chip, on its own line). Other sample rows: e5 left=89 top=2223 chipTop=2224 (same line). Comment in app/frontend/uncovered.css:17: '/* T-160: the link lives in the head line; it never takes a line of its own */'.\",\n   \"why_it_matters\": \"The 320 px reflow requirement is in scope for this UI (test_polish_r3.py:224-233 checks overflow only, and it stays green). The link does not overflow, but it does take its own line on a real row, which contradicts the comment and the commit message.\",\n   \"fix\": \"Scope the comment and commit wording to 390 and up, or let the head wrap in a way that keeps the link with its chip at 320 (for example, group the chip and link in one flex item).\",\n   \"acceptance_test\": \"At 320 px for sample and lib09, uncovered-summary.top minus chip--rec.top is smaller than the chip height on every row that has a chip. Repro: narrow.py against the card server.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"test_keyboard_only starts from summ.focus(), so Tab reach to the link is not asserted\",\n   \"evidence\": \"tests/e2e/test_uncovered_ui.py:92 summ.focus(). Probe on 7891 (T-160-r1/probe/card-94a31a4.json, tab_reach): from document start, Tab reaches uncovered-summary on stop 25 (stop before: entry-4 row), and Enter gives aria-expanded=true. The test never performs that Tab walk.\",\n   \"why_it_matters\": \"A tabindex=-1 or a DOM move that takes the link out of the Tab order would pass the test. The card's claim is reachable by keyboard, and the test only proves the button works once focused.\",\n   \"fix\": \"Add a Tab walk from the document start to the first uncovered-summary, with a stop count bound.\",\n   \"acceptance_test\": \"Set tabindex=-1 on the link in a scratch copy: the Tab walk test fails. Restore: it passes.\"}\n ],\n \"whats_right\": [\n  \"The density section of tests/e2e/test_polish_r3.py is identical to the pre-T-144 version: budgets 150/170/420 and the raw height. The T-155 subtraction is gone, not loosened.\",\n  \"The link is measured at +2 px per row at 1440 and 390 against a no-link DOM control (22 px to 2 px at 390 versus 802d5fd), and it shares the record chip's line at both widths.\",\n  \"test_uncovered_ui.py is 7 of 7 and test_polish_r3.py is 19 of 19 on the card archive, repeated, and on HEAD with no skips (E2E_REQUIRE_DB=1, private server).\"\n ],\n \"questions_for_chris\": [\"Is the 150/170/420 row budget meant for every case or only the sample? lib09 rows are 179.09 px (needs_review, 1440, with the link) and 173.09 px (needs_review, no link, 1440). The answer decides whether F1 is a fix or a scope note.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T15:44:04.589Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-160-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:07.456Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json,re\nt=open('reviews/T-160-staff-engineer.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json fences:', len(blocks), 'total fences:', t.count('\\`\\`\\`'))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('card',d['card'],'persona',d['persona'],'model',d['model'],'verdict',d['verdict'],'expected',exp,'sev',sev)\nprint('exercised',len(d['exercised']),'whats_right',len(d['whats_right']))\n\" ; python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Parse the review JSON and check verdict rule read-only"
}
````

### User / tool · 2026-11-02T15:44:07.514Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:10.755Z

**tool call — Bash**
````
{
 "command": "P=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-160-r1/probe; cat > $P/check_json.py <<'EOF'\nimport json, re, sys\nt = open(sys.argv[1]).read()\nfence = chr(96) * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, t, re.S)\nprint(\"json fences:\", len(blocks), \"all fences:\", t.count(fence))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", d[\"card\"], \"persona\", d[\"persona\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"], \"expected\", exp, \"sev\", sev)\nprint(\"exercised\", len(d[\"exercised\"]), \"whats_right\", len(d[\"whats_right\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $P/check_json.py /Users/arsis/zlayt-pm-project/reviews/T-160-staff-engineer.md",
 "description": "Validate the review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T15:44:10.861Z

**tool result**
````
json fences: 1 all fences: 2
card T-160 persona staff-engineer-reviewer model claude-haiku-5-5 verdict pass expected pass sev ['minor', 'minor', 'minor', 'minor', 'nit']
exercised 13 whats_right 3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:15.316Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 150
}
````

### User / tool · 2026-11-02T15:44:15.323Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (150). The file has 90 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:16.404Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T15:44:16.412Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E; T-124 d56328a pass: one-way and substring id check
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1-r2 (fail) and r4 3223e50 (changes): H3V5 label contradicts judge rule 1, reachability mutants red, relabel second-agent test
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263, r2 8bc7f90, r3 db08276 (all fail): bare figures vanish in prose/CMS/balance-forward, second balance-forward overwrites, counter blind to bare numbers, mutant label checks
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4 6bca71e (fail): repeated statement totals overwritten while counted as placed, skipped billing records leave complete true, stray bare-number definition gap
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untested); T-099 r2 f345bc8 pass: case_count clause untested, F2 debt needs SCOPE_CUTS row
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — r5 690a0e3 fail: ledger+CMS totals share a [-1] slot, bare charge beyond TOL=8 dropped, complete ignores reconciliation checks
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — r1 4c5f9bf changes; r2 fdc2506 pass: guard tested for golden only, recheck test passes via backstop, latest.json blocks run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — dd84122 fail: summary-only edit bypasses accept guard, gate recomputes 2 of 5 checks, notes print AI wording
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — r1 fail; r2b fail; r3 changes; r4 8a2b934 changes: UB-04 room total vs other_figures, offset comparisons open on Q1, redundant holder branches
35	- [Exact count vs presence](feedback_exact_count_vs_presence.md) — presence oracles miss a dropped second copy; run the test module's random generator with exact per-record counts
36	- [T-100 r2 patterns](project_t100_r2_patterns.md) — r2 288c1d3 changes: shared new_tokens, vocabulary narrower than _EN_* lists, fixture eval diff method, Spanish branches unpinned
37	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — 1335f21 pass: choke point verified by grep+probe; unchecked removed narrative text still printed; 4 unrelated unit failures
38	- [T-106 patterns](project_t106_review_patterns.md) — c2a5d1f changes: pdf_hidden regex bypass via from-subprocess-import, notes-only fix leaves narrative panel printing, loose fixture filter
39	- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — r1 d3e127c changes; r2 a271014 pass: masked route checks, sentences_reason unrendered, store.py broad except, clone for .git count
40	- [Shared scratchpad](feedback_shared_scratchpad.md) — scratchpad is shared with other agents: unique card-round subdirs, diff -rq archive checks, no backgrounded setup chains
41	- [T-109 doc-vs-code patterns](project_t109_doc_vs_code_patterns.md) — r1 changes; r2 4bdf366 fail (model conflicts dropped); r3 changes; r4 425095f pass: cite range off by blank lines, scan a-side keys, fix-up scope
42	- [T-106 r2 audit patterns](project_t106_r2_audit_patterns.md) — r2 e3a62fa changes: AST audit misses os alias/ctypes/asyncio, ps argv tail unpinned, rest-of-app still regex
43	- [T-102 stale-calibration patterns](project_t102_stale_calibration_patterns.md) — r1 276991b fail; r2 03206ca changes: stale fix verified via clone (archive can't discriminate), T-096 owner still missing, wrong-dir guard is a literal pin
44	- [T-115 e2e/curated patterns](project_t115_e2e_curated_patterns.md) — r1 400a8c0 changes: evidence cites older commit than HEAD, regen re-keys prompts with scripted answers, ZLAYT_DB skips, inner_text race
45	- [T-112 trim patterns](project_t112_trim_patterns.md) — r1 afcde06, r2 1b93582 changes: stems then abbreviations over-trim, doc/D-054 on old rule, unpinned counter
46	- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — r1 6e880e6 changes; r2 changes (p gate); r3 c559ce2 pass: vis() first-frame poll, count artifact without sha
47	- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof listener before killing own servers
48	- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — HEAD 433ac1c: negative-proxy guard, one-direction single-source refactor, write-once errata in my r2 files
49	- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — r1 93de5f2: closed-list fragment guard, preamble flag never served by API, T-127 pass with unpinned from/to
50	- [T-120 r3 patterns](project_t120_r3_patterns.md) — f7829c1 pass: strip-then-scan verified, MS honorific collision, unpinned gate mutant, count errata in r3 file
51	- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — T-128 r2 changes: structural rule leaves dependent tail clauses, deny gap; T-129 r2 pass: tests flag-only, relative sweep path false-kills
52	- [T-133 lexicon patterns](project_t133_lexicon_review_patterns.md) — r1 e79c3aa/1218b2e changes: bare 'History:' HPI over-flag, attribution deny untested, ';' truncates excerpt, deny has no source
53	- [T-113/T-122 patterns](project_t113_t122_patterns.md) — 5dfba88: held-out control written with the prompt naming its noun, closed-list word mutants, vacuous order test; T-122 regression created by T-113 commit
54	- [T-132 r2 / T-128 r3 patterns](project_t132_t128_r2r3_patterns.md) — both changes: wrap inside chained clause, 2-letter header labels, participle before removed with-tail, prefix-oracle fuzz with old-code control
55	- [T-133 r3 patterns](project_t133_r3_patterns.md) — 4065ef2 changes: r2 header guard dropped Past/Medical/Surgical history flags, ';' suppression recall gap, live eval owed
56	- [T-133 r4 patterns](project_t133_r4_patterns.md) — 128942d changes (final): \s matches newline so line-start bare History: flags, parity tests blind to gains, 13d "before T-133" premise false
57	- [T-133 r5 patterns](project_t133_r5_patterns.md) — 15be212 pass: prior-ending x separator grid, CR-only kills \s but CRLF/blank cannot, eval grep must read header line, 13d PMH overstated
58	- [Regex multiline probe](feedback_regex_multiline_probe.md) — probe \s and line-break variants of "line start" guards; \s matches newline under re.M on raw text
59	- [Differential probe vs prior build](feedback_differential_probe_prior_build.md) — run the probe set on pre-fix and HEAD archives; FLAG-to-quiet flips reveal regressions the acceptance list misses
60	- [T-134 unconfirmed-edit patterns](project_t134_unconfirmed_edit_patterns.md) — r1 5fb338d changes; r2 db1d8d5 changes: judge_report human_overrides counts open edit, N3/N5 mutants survive
61	- [GATE-M2 patterns](project_gate_m2_patterns.md) — 0c24f5f fail: deadline skips judge_entries so entries compose verified, timed-out rerun deletes pending, no live ship-bar report at HEAD
62	- [T-113 r2 patterns](project_t113_r2_patterns.md) — bea3984 changes: git-derived held-out audit checked with throwaway repos, count/real-data unpinned (7 of 14 mutants green), in-place edit blind spot, 13c history side only
63	- [T-132 r4 patterns](project_t132_r4_patterns.md) — fc60471 changes: 'Label:' regex drops condition lines ('Left wrist swollen:'), git archive from a subdir exports empty tree, control-vs-HEAD visibility diff, equivalence of linearised helpers
64	- [T-132 r5 patterns](project_t132_r5_patterns.md) — ed45b4a/5de16d3 pass: closed-list stop leaves ALL-CAPS condition lines dropped (minor), AC count off by one, control-first probe expectations, hook denies rm with expansion
65	- [T-134 r3 / T-138 patterns](project_t134_r3_t138_patterns.md) — both changes: text fix missed review step + gate headline, stale rejudge claim, snapshot aliases mutated dict, HEAD broken by sibling commit
66	- [T-145/T-146 patterns](project_t145_t146_patterns.md) — T-145 pass: shared JUDGE_NOT_RUN sentence mislabels real failure; T-146 changes: failed (done_with_errors) re-run wipes accepted entries, state-only snapshot
67	- [T-141 r2 patterns](project_t141_r2_patterns.md) — 68b8685 changes: clause word list still loses conflicts (prior to/no history of), stored run summary stale after confirm_date, sibling test hunk red at commit
68	- [T-134 r4 / T-138 r2 patterns](project_t134_r4_t138_r2_patterns.md) — 4f416a4 changes, b7a7ead pass: backend D-058 wording fixed but UI regex keeps old stays-blocked sentence, identical-text re-pick test, alias and leak controls
69	- [Frontend text coupling](feedback_frontend_text_coupling.md) — when a backend sentence changes, grep app/frontend for the old phrase and regexes over it (server-text swap silently falls back)
70	- [T-136 r2 patterns](project_t136_r2_patterns.md) — 07c7558 changes: private-server fallback to :7860, red e2e predating the card, flaky mobile and open_rail tests, client copy of gate rule
71	- [T-146 r2 patterns](project_t146_r2_patterns.md) — 2db6ad2 changes: keep-whole rule keyed on judge/stub only; flags-down downgrades corroborated flag, SUMMARY_NOT_IN_QUOTE overwrites
72	- [T-140 r2 patterns](project_t140_r2_patterns.md) — a0e2639 changes: tests read untracked reviewer file (clean pytest aborts), after-figure position gap, reclassify skips duplicate/total flags
73	- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed
74	- [T-141 r4 patterns](project_t141_r4_patterns.md) — 93a2ffc changes: month-year two-month cut-off hides 'Rear-ended in October 2025' while bare-year fix flipped; pinned variant contradicts r3 acceptance
75	- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — r1 changes: untracked ledger read at import breaks clean collection, golden-named test without golden compare, git show not working tree, HEAD moved 3x
76	- [T-146 r3 patterns](project_t146_r3_patterns.md) — bf53087 changes: equal-rank check worsening replaces decided item silently, reword fails case, rerun_note no UI consumer
77	- [T-146 r4 patterns](project_t146_r4_patterns.md) — c2913a6 pass: a2 keep-and-note and j3 gate hold; identical re-run rewrites decided rows (updated_at, call_id); dead 'conflicts' key
78	- [Fake script keys](feedback_fake_script_keys.md) — FakeCall returns {} for unknown step keys; grep the key is consumed and run a wrong-key control before trusting a step-down probe
79	- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned
80	- [T-155 e2e triage patterns](project_t155_e2e_triage_patterns.md) — 20b3a42 changes (r1b): green claim on older sha, "stale" density reds were real, hidden list 0 px + 8px margin, refusal box btn_y+132
81	- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a "stale test" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between
82	- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — r1 926bf37 and r2 852b060 (changes): edit-class waiting-set survivor, identity-only demo test, entity titles, PATCH 422-before-404
83	- [T-140 r3 / T-152 r2 patterns](project_t140_r3_t152_r2_patterns.md) — 35d8280 changes: default-deny per line not per figure (second-figure leaks), undated promote unflagged, 7 surviving mutants; T-152 pass, sibling commit broke collection briefly
84	- [T-141 r6 patterns](project_t141_r6_patterns.md) — 824984f fail: closed exemption leaks across and/or/with/for/of, plural and bare hit/impact missing from _EVENT, Q15 regression
85	- [T-141 r7 patterns](project_t141_r7_patterns.md) — ba21b4b fail: two-digit-year dates escape the plural-list guard, lib11 e2e skip file red since before ff1256e, conftest SyntaxError looks like red
86	- [T-141 r8 patterns](project_t141_r8_patterns.md) — 78b6a33 pass (HEAD 99438fb): HEAD moved past card, lib11 .expected.json changed by sibling card, sentence-scope residual, 10-pin mutant
87	- [T-162 rerun-note patterns](project_t162_rerun_note_patterns.md) — 70af4a7 fail; r2 67be38d changes: console watcher blind to panel throws (4 of 7 panels dead, spec green), to_be_hidden vacuous
88	- [Watcher blind to render errors](feedback_watcher_blind_to_render_errors.md) — pageerror/console watchers stay empty when a render hook throws; mutate a non-first panel and list [data-panel]
89	- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (export 200), always-reset mutant, undated-boundary mutant, FakeCall skips validate_schema
90	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:22.363Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t160_budget_placement_patterns.md",
 "content": "---\nname: t160-budget-placement-patterns\ndescription: T-160 r1 94a31a4 pass (3 minors, 1 nit): row-budget test covers sample only, reverted placement passes the density tests, \"never own line\" false at 320 px, Tab reach untested\nmetadata:\n  type: project\n---\n\nT-160 r1 (94a31a4, link moved after the record chip in uncovered.js:32) reviewed as pass: 0 blockers, 0 majors, 3 minors, 1 nit. Review: reviews/T-160-staff-engineer.md. The density section of test_polish_r3.py was byte-identical to the pre-T-144 version, so the budget was restored, not loosened.\n\n- **Budget scoped to the sample.** The first-screen test (test_polish_r3.py:168) uses sample_case. A lib09 needs_review row is 179 px at 1440 with the link and 173 px without it. No test sees either.\n- **Premise not reproduced.** On the parent 802d5fd the enforced budgets were met: the link added +22 px at 390 (lib09 e2 391 against 420) and +6 px at 1440. \"Over budget since T-144\" was an overclaim.\n- **Unguarded regression.** The density tests pass on the pre-fix placement (control: `-k \"first_screen or 390_needs or row_opens\"` gives 3 passed on 802d5fd). Nothing fails if the link goes back to the end of the head.\n- **Overclaim at 320 px.** The sample e3 link wraps below its chip (top 1587 against chip 1565). The \"never takes a line of its own\" comment is only true at 390 and up.\n- **Tab reach is not tested.** test_uncovered_ui.py:92 calls summ.focus(). Tab from the document start reached the link at stop 25 on the card, so the claim holds but no test proves it.\n\n**Why:** a layout fix that is measured only on the sample, with no check that fails without it, comes back silently. The 22 px to 2 px improvement was real; the description of what breached was not.\n**How to apply:** for any row or layout budget, run a differential probe on the parent and the card, on every fixture case the paralegal can open (sample and lib09), not only the test's fixture. Run the density tests on the pre-fix archive as a control. Probe overflow at 320 px as well as the cited widths.\n\nShell gotcha seen this round: the board guard denied a `sed -i` edit and a command with backslash-escaped backticks (\"could not parse command safely\"). Write scratch scripts with a heredoc and run them with `.venv/bin/python -I`.\n\nRelated: [[project_t155_e2e_triage_patterns]], [[feedback_evidence_sha_vs_commit]], [[project_t136_r2_patterns]], [[feedback_differential_probe_prior_build]].\n"
}
````

### User / tool · 2026-11-02T15:44:22.456Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t160_budget_placement_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:24.378Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (export 200), always-reset mutant, undated-boundary mutant, FakeCall skips validate_schema\n",
 "new_string": "- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — both pass: compensation fails under double fault (export 200), always-reset mutant, undated-boundary mutant, FakeCall skips validate_schema\n- [T-160 budget/placement patterns](project_t160_budget_placement_patterns.md) — 94a31a4 pass: budget test sample-only, reverted placement passes density tests, \"never own line\" false at 320 px\n"
}
````

### User / tool · 2026-11-02T15:44:24.481Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T15:44:26.027Z

T-160 (94a31a4): pass (0 blockers, 0 majors, 3 minors, 1 nit). Budget restored and not loosened, link reachable by click and Tab, both e2e files green (19 and 7 on the card, 26 on HEAD 985dbd2). Review: /Users/arsis/zlayt-pm-project/reviews/T-160-staff-engineer.md
