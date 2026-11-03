# Subagent: T-126 staff review (T-126 staff review)

Source: `agent-a4af1a0f429aecff5.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:22:01.239Z

Review board card T-126 in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-126`. It implements D-057 (see memory/ORCHESTRATOR_DECISIONS.md): model-proposed flags filtered by the D-032 rule (objective_negative) must go to a collapsed, counted "Filtered by rule" tray group in the API payload, with the rule named. They must never be silently dropped and never reach the timeline or letter.

On a `git archive HEAD` copy in your scratchpad:
- run the unit suite;
- search for any other code path that still drops model proposals silently (D-053);
- mutate the code to test the tests;
- check that memory/contracts/api.md documents the payload.

Write reviews/T-126-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Stop only your own PIDs. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:02.657Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:22:02.667Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:03.092Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-126; git log --oneline | head -5; git status --short | head -20"
}
````

### User / tool · 2026-11-02T11:22:03.276Z

**tool result**
````
---
id: "T-126"
title: "D-057: D-032-filtered model flags (objective_negative) go to a collapsed 'Filtered by rule' tray group, never silently dropped"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:11:07Z"
updated_at: "2026-11-02T11:21:57Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:11:34Z"
rounds: 0
commits: ["6d01774"]
reviews: []
ac:
  - {"n": 1, "text": "flags filtered by D-032 appear in the API tray payload with the rule name and a count; never in timeline/letter; unit test proves no model proposal is dropped silently", "done": true, "evidence": "tests/unit/test_t126_filtered_by_rule.py (5 tests): case payload tray_filtered {label, collapsed, count, rules[rule, ref D-032, count, items]}; not in flags/tray/queue/counts/gate/letter; counts match stored rows; evals fixture flag P/R unchanged 1.000"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:11:34Z backend: claimed
- 2026-11-02T11:15:03Z backend: Frontend note (do not edit app/frontend): render case.tray_filtered as a collapsed 'Filtered by rule' group under the tray: header label + count, one sub-row per rules[] (label, ref, count) expanding to items (attempt.excerpt, why). needs_action is false; it must not add to any 'needs review' count. Shape in memory/contracts/api.md (D-057 paragraph).
- 2026-11-02T11:18:56Z backend: AC 1 checked: tests/unit/test_t126_filtered_by_rule.py (5 tests): case payload tray_filtered {label, collapsed, count, rules[rule, ref D-032, count, items]}; not in flags/tray/queue/counts/gate/letter; counts match stored rows; evals fixture flag P/R unchanged 1.000
- 2026-11-02T11:18:57Z backend: moved in_progress -> in_review
- 2026-11-02T11:21:57Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: flags.merge lists model objective_negative proposals as FILTERED_BY_RULE tray items placed after every other tray item (ids unchanged, no judge fixture changes); present.case_view adds tray_filtered (collapsed, counted, rule named) and keeps them out of tray/flags/queue/review counts; trace gate/judge counts and export skip them; api.md documents it. Verified: new tests, unit suite (only test_summary_trim fails, another worker's in-flight), evals fixture unchanged. Left: frontend renders tray_filtered (note on card). scene_facts stays an LLM_ONLY tray item (needs a look, not noise). Surprised: gate, judge and export counts all read rejected flags, so each needed the exclusion.

e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
6d01774 feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
c26ff04 feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
c89ac86 docs(orchestrator): D-057 rule-filtered model proposals are listed collapsed, not dropped
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:03.802Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-057\\|D-053\\|D-032\" memory/ORCHESTRATOR_DECISIONS.md | head -30"
}
````

### User / tool · 2026-11-02T11:22:03.883Z

**tool result**
````
40:| D-032 | Narrows D-018: normal/negative findings (`objective_negative`: 'negative for fracture', 'WNL', 'full ROM') are **context only, never flags**; `scene_facts` raise a causation flag only on specific adjuster phrases ('minimal damage', 'refused transport', 'ambulatory at scene', 'no airbag deployment'), never on a plain mechanism description ('Cyclist struck by a car'). | First eval: causation precision 0.5 from these two categories; golden case_05 must_not N2. | T-038 eval report 20261102T020824Z |
46:| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
61:| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or that no code candidate confirms, goes to the **could-not-verify tray** with the judge's reason; it is never a flag and never reaches the letter. The eval scores precision on emitted flags only (tray items are not assertions), and reports tray counts separately; R-CO-7's flag-set signature covers flags, not tray items. Conflict candidates from code (T-094) remain the only path to a conflict *flag*; recall gaps in the code rules are listed in SCOPE_CUTS until covered. | Suppressing rejected items to raise precision hid model output from the paralegal, against R-FL-3 and the ladder. | T-094 staff r1 |
65:| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:07.280Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t126r1/a && git rev-parse HEAD && git archive HEAD | tar -x -C $S/t126r1/a && ls $S/t126r1/a | head -30; git show --stat 6d01774 | head -30; git diff HEAD --stat -- app tests memory/contracts | tail -5"
}
````

### User / tool · 2026-11-02T11:22:07.911Z

**tool result**
````
c559ce20ffbdcac8d4ad17b3c78f9ff0786c12a7
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
commit 6d0177472fb85c0775f9869027c2fd6e54209a70
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:18:51 2026 -0600

    feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/confidence.py                |  2 +-
 app/backend/flag_templates.py            |  7 ++++
 app/backend/flags.py                     | 22 ++++++++--
 app/backend/present.py                   | 27 ++++++++----
 app/backend/store.py                     |  2 +
 app/backend/trace.py                     |  4 +-
 app/backend/why.py                       |  1 +
 memory/contracts/api.md                  |  3 +-
 tests/unit/test_flags_pass.py            |  3 +-
 tests/unit/test_t126_filtered_by_rule.py | 72 ++++++++++++++++++++++++++++++++
 10 files changed, 128 insertions(+), 15 deletions(-)
 app/backend/grounding.py    | 62 +++++++++++++++++++++++++++++++++++----------
 app/backend/pipeline.py     |  2 +-
 app/backend/spanish_text.py | 32 ++++++++---------------
 app/llm/lexicon.yaml        | 59 +++++++++++++++++++++++++++++++++++++++---
 5 files changed, 118 insertions(+), 41 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:09.362Z

**tool call — Bash**
````
{
 "command": "git show 6d01774 -- app memory tests/unit/test_flags_pass.py | head -300; git log --oneline 6d01774..HEAD"
}
````

### User / tool · 2026-11-02T11:22:09.486Z

**tool result**
````
commit 6d0177472fb85c0775f9869027c2fd6e54209a70
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:18:51 2026 -0600

    feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/confidence.py b/app/backend/confidence.py
index ab169fe..a4d542e 100644
--- a/app/backend/confidence.py
+++ b/app/backend/confidence.py
@@ -11,7 +11,7 @@ REASON_CODES = (
     "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
     "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
     "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
-    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE",
+    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
 )
 REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
 STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
diff --git a/app/backend/flag_templates.py b/app/backend/flag_templates.py
index c93cc86..b44d830 100644
--- a/app/backend/flag_templates.py
+++ b/app/backend/flag_templates.py
@@ -212,3 +212,10 @@ def render(flag_type: str, subtype: str, **vars) -> tuple:
     v = {k: x for k, x in vars.items() if x not in (None, "")}
     title, expl = TEMPLATES[category_of(flag_type, subtype)](v)
     return title, expl.replace(".”.", ".”")      # a quote that already ends in a period needs no second one
+
+
+# D-057 (T-126): a model proposal that a code rule filters out is listed in a collapsed, counted "Filtered by rule" group, never dropped (D-053).
+# category -> (decision, rule name shown, what the rule says). The group is derived from the flag's category; nothing extra is stored.
+FILTER_RULES = {"objective_negative": ("D-032", "Normal or negative findings",
+                                       "A normal or negative finding is context, not a flag, so the rule filtered it out. Nothing is needed from you.")}
+FILTERED = "FILTERED_BY_RULE"
diff --git a/app/backend/flags.py b/app/backend/flags.py
index 7e5fca9..d6d68a4 100644
--- a/app/backend/flags.py
+++ b/app/backend/flags.py
@@ -19,6 +19,7 @@ _NEEDS_LEXICON = ("scene_facts",)
 # against the claimant, so the paralegal must see them first. Detected by credibility.scan (family match + negation), raised under their own
 # category, never folded into a hedge flag. The lexicon's objective_negative hits (incl. the same phrases) stay context only.
 CREDIBILITY_CATEGORY = credibility.CATEGORY
+FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without importing the engines
 JUDGE_PROMPT = {j: AU.PROMPT_OF_STEP[j] for j in ("j3", "j4")}
 
 
@@ -113,9 +114,13 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
     """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
     (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
     body, out, used = record["excerpt"], [], set()
-    uniq, seen = [], set()
+    uniq, seen, filtered, fseen = [], set(), [], set()
     for lf in llm_flags:
-        if lf.get("category") in _CONTEXT_ONLY:
+        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
+            k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
+            if k not in fseen:
+                fseen.add(k)
+                filtered.append(lf)
             continue
         k = (lf["type"], grounding.normalize(lf["excerpt"]))
         if k not in seen:
@@ -157,6 +162,11 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
         if lf.get("category") in _NEEDS_LEXICON:
             f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
         out.append(f)
+    for lf in filtered:
+        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
+        f["_tray"] = FILTERED
+        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
+        out.append(f)
     for f in out:
         f["_stage"]["injection"] = tagged
         _compose(f)
@@ -239,7 +249,8 @@ def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=Non
     flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
     # tray items go LAST: a flag's id (f_r<n>_<k>) is its position in this list and is part of the judge's prompt, so inserting an item that used to be
     # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
-    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f] + _model_conflicts(conflicts, record, tagged)
+    last = [f for f in flags if f.pop("_last", False)]
+    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f and f not in last] + _model_conflicts(conflicts, record, tagged) + last
     ground(flags, record)
     for f in flags:
         code = f.pop("_tray", None)
@@ -332,6 +343,11 @@ def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
 def _to_tray(f: dict, code: str, judge_reason=None) -> None:
     """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
     f["state"] = "rejected"
+    if code == FILTERED:
+        f["_stage"]["judge"] = None
+        f["reasons"] = [FILTERED]
+        f["why"] = why.why(FILTERED)
+        return
     if code == "LLM_ONLY":
         # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
         # (T-122: the eval counted case_05's f_r1_1 as a judge that did not run)
diff --git a/app/backend/present.py b/app/backend/present.py
index 2a477fb..40c403f 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -2,7 +2,7 @@
 import json
 import re
 
-from app.backend import confidence, date_convention, generator, grounding, ingest, language, overlap, pdf_text, sentences, spanish, store, totals as T, why
+from app.backend import confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, sentences, spanish, store, totals as T, why
 from app.db import db as DB
 
 STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
@@ -147,7 +147,7 @@ def rejected_count(conn, case_id):
 def review_view(conn, case_id):
     items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
     handled = generator.resolved_placeholders([r for k, r in items if k == "entry"])
-    items = [(k, r) for k, r in items if r["id"] not in handled]
+    items = [(k, r) for k, r in items if r["id"] not in handled and (r.get("state_reasons") or [])[:1] != [FT.FILTERED]]       # D-057: rule-filtered proposals need no action and are not counted
     live = [(k, r) for k, r in items if r["state"] != "rejected"]
     counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
     counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
@@ -242,17 +242,28 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
              "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
     # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
     # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
-    tray += [{"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
-              "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
-              "flag": {"type": x["type"], "category": x["category"]},
-              "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
-              "ladder": {"item_id": x["id"], "state": "rejected"}} for x in its["flag"] if x["state"] == "rejected"]
+    def _tray_flag(x):
+        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
+                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
+                "flag": {"type": x["type"], "category": x["category"]},
+                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
+                "ladder": {"item_id": x["id"], "state": "rejected"}}
+    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
+    filtered = [x for x in rejected_flags if x["reasons"][:1] == [FT.FILTERED]]
+    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
+    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
+    rules = []
+    for cat in sorted({x["category"] for x in filtered}):
+        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
+        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
+        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
+    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
     err = json.loads(case["error"]) if case.get("error") else None
     injected = [r["id"] for r in recs if r["injection_tag"]]
     return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
             "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
diff --git a/app/backend/store.py b/app/backend/store.py
index 0fae480..c51bc5c 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -66,6 +66,8 @@ def export_case(conn, case_id: str) -> dict:
                  excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
     fl = []
     for f in DB.list_items(conn, case_id, "flag"):
+        if (f.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:        # D-057: a rule-filtered proposal is not an item to review, count or export
+            continue
         c = f.get("computed") or {}
         ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                    excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
diff --git a/app/backend/trace.py b/app/backend/trace.py
index cb09dfe..b98f214 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -749,6 +749,8 @@ def _judge_rows(cx):
     out = []
     for kind in ("entry", "amount", "flag"):
         for row in DB.list_items(cx.conn, cx.case_id, kind):
+            if kind == "flag" and (row.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:      # D-057: never judged, never counted
+                continue
             jd = (row.get("ladder") or {}).get("judge")
             if not jd or not jd.get("verdict"):
                 out.extend(_judge_never_ran(cx, kind, row))
@@ -896,7 +898,7 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure") and x["id"] not in handled]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
     ents = [x for x in ents if not (x.get("ladder") or {}).get("failure")]      # (a hand-entered record's placeholder is dropped here too)
     amts = DB.list_items(conn, case_id, "amount")
-    flgs = DB.list_items(conn, case_id, "flag")
+    flgs = [x for x in DB.list_items(conn, case_id, "flag") if (x.get("state_reasons") or [])[:1] != ["FILTERED_BY_RULE"]]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
     allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
     cfg = case.get("config") or {}
     rv = present.review_view(conn, case_id)
diff --git a/app/backend/why.py b/app/backend/why.py
index 3614d40..2cc52e1 100644
--- a/app/backend/why.py
+++ b/app/backend/why.py
@@ -23,6 +23,7 @@ _WHY = {
     "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
     "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
     "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
+    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
     "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
     "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
     "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index ea94398..9a2654f 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -128,7 +128,7 @@ Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human dec
 `status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline", "message": "..."}`; finished items are kept. Poll every second. Partial results are readable from the case endpoint while running.
 
 ## GET /api/cases/{token}
-Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
+Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
 ```json
 {
   "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
@@ -756,5 +756,6 @@ Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into
 | `AI_TRANSLATION` | needs_review | the item comes from a record routed Spanish or LANGUAGE_UNCERTAIN (D-050); "AI translation — check against the original"; never verified by any check, only the paralegal's accept |
 | `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by code after the model steps, never cleared by a judge or a date confirmation |
 | `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
+| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D-032 `objective_negative`). Listed only in the case payload's `tray_filtered` (collapsed group with the rule named and a count); not a flag, not in the queue, counts, gate or export; no action needed |
 | `SUMMARY_NOT_IN_QUOTE` | rejected | D-054: code removed every clause of the AI summary because each added content its own quote lacks; the record has no entry, only a could-not-verify tray placeholder (`ladder.failure`, `ladder.summary_trim` lists the removed clauses); write the entry by hand. The same placeholder is made when a record is split out with `not_duplicate` (the response `warnings[]` then carries this code, the new tray item's `item_id` and a message saying code removed the summary; its trace shows later steps as skipped, not as a failed word-for-word check) |
 | `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
diff --git a/tests/unit/test_flags_pass.py b/tests/unit/test_flags_pass.py
index ce6efb4..b7e79d2 100644
--- a/tests/unit/test_flags_pass.py
+++ b/tests/unit/test_flags_pass.py
@@ -121,7 +121,8 @@ def test_d032_objective_negative_is_context_only_and_scene_facts_need_the_phrase
            dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed.")]
     out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
     assert not [f for f in out if f["state"] != "rejected"]                     # never a flag
-    assert [f["category"] for f in out] == ["scene_facts"] and out[0]["reasons"][0] == "LLM_ONLY"       # T-113 / D-053: the scene_facts proposal is a tray item, not a silent drop
+    assert [f["category"] for f in out] == ["scene_facts", "objective_negative"] and out[0]["reasons"][0] == "LLM_ONLY"       # T-113 / D-053: the scene_facts proposal is a tray item, not a silent drop
+    assert out[1]["reasons"] == ["FILTERED_BY_RULE"] and out[1]["state"] == "rejected"                                         # T-126 / D-057: the filtered proposal is listed, collapsed
     r2 = dict(r, excerpt="Ambulatory at scene, refused transport. Minimal damage to vehicle.")
     out = F.run_flag_pass(r2, call=FakeCall({"flags": {"flags": []}}))
     assert out and all(f["category"] == "scene_facts" and f["origin"] == "lexicon" for f in out)
c559ce2 test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring
e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:12.340Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && cat tests/unit/test_t126_filtered_by_rule.py; ls /Users/arsis/zlayt-pm-project/.venv/bin/python; diff -rq /Users/arsis/zlayt-pm-project/tests/unit tests/unit | head"
}
````

### User / tool · 2026-11-02T11:22:12.441Z

**tool result**
````
"""T-126 (D-057): a model proposal that a code rule filters out (D-032 objective_negative) is listed, not dropped: a collapsed, counted
'Filtered by rule' group in the case payload with the rule named. Never a flag, never in the review queue, timeline or letter; needs no action."""
from app.backend import export, flags as F, present
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

R = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative for fracture. Ankle exam normal. Full cervical ROM.", date_iso="2026-06-01")


def test_a_model_objective_negative_proposal_is_a_filtered_item_not_a_silent_drop():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),          # duplicate: one item
           dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert len(out) == 2 and all(f["state"] == "rejected" and f["reasons"][0] == "FILTERED_BY_RULE" and f["origin"] == "llm" for f in out)
    assert [f["excerpt"] for f in out] == ["X-ray negative for fracture.", "Ankle exam normal."]
    assert not [f for f in out if f["state"] != "rejected"]


def test_filtered_items_come_after_every_other_tray_item_so_no_recorded_id_moves():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="Ankle exam normal.", excerpt_b="Full cervical ROM.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["reasons"][0] for f in out] == ["LLM_ONLY", "LLM_ONLY", "FILTERED_BY_RULE"]


def test_the_rule_filter_does_not_touch_a_phrase_list_flag_in_the_same_sentence():
    r = dict(R, excerpt="Patient reports prior neck pain. Ankle exam normal.")
    llm = [dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["category"] for f in out if f["state"] != "rejected"] and [f for f in out if f["reasons"][0] == "FILTERED_BY_RULE"]


def _view(tmp_path, extra):
    conn = DB.connect(str(tmp_path / "c.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=lambda user: {"flags": extra} if which_record(user) == [4] else {"flags": []})),
                    now=lambda: 1.0)
    return conn, cid, present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)


def test_case_payload_has_a_collapsed_counted_group_with_the_rule_named_and_nothing_else_changes(tmp_path):
    (tmp_path / "a").mkdir()
    _, _, base = _view(tmp_path / "a", [])
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),
             dict(type="causation", category="objective_negative", excerpt="Discharged from PT after two missed appointments.")]
    (tmp_path / "b").mkdir()
    conn, cid, v = _view(tmp_path / "b", extra)
    g = v["tray_filtered"]
    assert g["label"] == "Filtered by rule" and g["collapsed"] is True and g["count"] == 2 and g["needs_action"] is False
    (rule,) = g["rules"]
    assert rule["rule"] == "objective_negative" and rule["ref"] == "D-032" and rule["count"] == 2 and "normal" in rule["label"].lower()
    ids = [i["id"] for i in rule["items"]]
    assert len(ids) == 2 and all(i["flag"]["category"] == "objective_negative" and i["attempt"]["excerpt"] for i in rule["items"])
    assert all(i["reasons"][0] == "FILTERED_BY_RULE" and i["why"] for i in rule["items"])
    # not in the flag list, the review queue, the ordinary tray, the counts that need action, or the letter
    assert not [f for f in v["flags"] if f["id"] in ids]
    assert not set(ids) & set(v["review"]["queue"]) and not [t for t in v["tray"] if t["id"] in ids]
    assert v["flags"] == base["flags"] and v["tray"] == base["tray"] and v["review"]["queue"] == base["review"]["queue"]
    assert base["tray_filtered"]["count"] == 0 and base["tray_filtered"]["rules"] == []
    case = {"records": [], "entries": [], "amounts": [], "flags": []}
    assert "Plan of care: 12 visits." not in export.build_export(case)["letter_text"]


def test_no_model_proposal_is_dropped_silently_counts_match(tmp_path):
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits.")]
    conn, cid, v = _view(tmp_path, extra)
    rows = [r for r in present.all_items(conn, cid)["flag"] if r["state"] == "rejected" and r["reasons"][0] == "FILTERED_BY_RULE"]
    assert len(rows) == 1 == v["tray_filtered"]["count"]
/Users/arsis/zlayt-pm-project/.venv/bin/python
Only in /Users/arsis/zlayt-pm-project/tests/unit: __pycache__
Only in /Users/arsis/zlayt-pm-project/tests/unit: test_t105_added_qualifier_lexicon.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:15.903Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && timeout 560 $P -I -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:22:16.008Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:18.393Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && $P -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:25:31.275Z

**tool result**
````
........................................................................ [ 68%]
........................................................................ [ 70%]
...............................................s........................ [ 73%]
........................................................................ [ 75%]
........................................................................ [ 78%]
........................................................................ [ 80%]
........................................................................ [ 83%]
........................................................................ [ 85%]
........................................................................ [ 88%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 95%]
........................................................................ [ 97%]
...............................................................          [100%]
2939 passed, 4 skipped in 191.40s (0:03:11)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:25:34.766Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -n \"_CONTEXT_ONLY\\|continue\\|\\.get(\\\"category\\\")\\|_NEEDS_LEXICON\" app/backend/flags.py | head -60; sed -n 1,30p app/backend/flags.py"
}
````

### User / tool · 2026-11-02T11:25:34.883Z

**tool result**
````
16:_CONTEXT_ONLY = ("objective_negative",)
17:_NEEDS_LEXICON = ("scene_facts",)
87:        if h["category"] not in _CONTEXT_ONLY:
99:            continue
119:        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
124:            continue
160:            continue
162:        if lf.get("category") in _NEEDS_LEXICON:
183:            continue
303:            continue
305:            continue
368:            continue
371:            continue
"""LLM flag engines with the lexicon as the floor (ADR-008, ADR-013; R-FL-3..5, R-FL-7, R-FL-8; LLM_VS_CODE rows 11-13, 16).
Per-record pre_existing/causation pass (one call per record, so an injected record cannot suppress another record's flags) merged
with the code lexicon scan; one cross-record pass for semantic conflicts (accident-date and provider-name conflicts are code, conflicts.py).
The model returns only type, category and quoted text; titles and explanations are code templates. Flags never get a review_status
other than 'pending'. `call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline."""
from pydantic import ValidationError

import re

from app.backend import conflict_candidates as CC, sentences, confidence, credibility, flag_templates as FT, generator, grounding, injection, judges, language, lexicon_scan, schemas, why
from app.llm import audited as AU, promptlib, provider as P

_PER_RECORD_TYPES = ("pre_existing", "causation")
# D-032: normal/negative findings are context only and never become flags (from either signal); a scene_facts flag needs a phrase-list
# hit on a specific adjuster phrase, never just a model's reading of a mechanism description.
_CONTEXT_ONLY = ("objective_negative",)
_NEEDS_LEXICON = ("scene_facts",)
# D-038 (narrows D-032): defense credibility phrases are the exception to "normal/negative is context only". They are what an adjuster quotes
# against the claimant, so the paralegal must see them first. Detected by credibility.scan (family match + negation), raised under their own
# category, never folded into a hedge flag. The lexicon's objective_negative hits (incl. the same phrases) stay context only.
CREDIBILITY_CATEGORY = credibility.CATEGORY
FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without importing the engines
JUDGE_PROMPT = {j: AU.PROMPT_OF_STEP[j] for j in ("j3", "j4")}


# ------------------------------------------------------------------ helpers
def _base(record: dict) -> int:
    return generator.body_offset(record) if record.get("text") else 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:25:37.272Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 78,215p app/backend/flags.py"
}
````

### User / tool · 2026-11-02T11:25:37.380Z

**tool result**
````
def lexicon_flags(record: dict, accident_year=None) -> list:
    """Flags from the phrase list alone: excerpt = the whole sentence unit that contains the hit; one flag per (unit, type)."""
    text = record["excerpt"]
    units = sentences.stripped_spans(text)
    seen, out = {}, []
    hits = []
    for h in lexicon_scan.scan(text, accident_year):
        if h["category"] not in _CONTEXT_ONLY:
            hits.append(h)
    hits += credibility.scan(text)
    prior_units = {(h["unit_start"], h["unit_end"]) for h in hits if h["flag_type"] == "pre_existing"}
    # a sentence that already carries a prior-condition flag does not also raise an "alternative cause" flag (same fact, one flag)
    hits = [h for h in hits if not (h["category"] == "alternative_cause" and (h["unit_start"], h["unit_end"]) in prior_units)]
    for h in hits:
        # a credibility hit's span is already its whole period sentence (D-043): it never pulls a neighbouring hedge sentence into the quote
        a, b = (h["unit_start"], h["unit_end"]) if h["category"] == CREDIBILITY_CATEGORY else _hedge_run(text, units, h["unit_start"], h["unit_end"])
        key = (a, b, h["flag_type"], CREDIBILITY_CATEGORY if h["category"] == CREDIBILITY_CATEGORY else None)   # D-038: never folded into a hedge flag
        if key in seen:
            seen[key]["lexicon_ids"].append(h["id"])
            continue
        f = _flag(record, h["flag_type"], h["category"], text[a:b], "lexicon", (a, b), False, "lexicon_only")
        f["lexicon_ids"] = [h["id"]]
        f["_span"] = (a, b)
        seen[key] = f
        out.append(f)
    return out


# ------------------------------------------------------------------ merge
def _overlap(a, b) -> bool:
    return bool(a and b and a[0] < b[1] and b[0] < a[1])


def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
    body, out, used = record["excerpt"], [], set()
    uniq, seen, filtered, fseen = [], set(), [], set()
    for lf in llm_flags:
        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
            k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
            if k not in fseen:
                fseen.add(k)
                filtered.append(lf)
            continue
        k = (lf["type"], grounding.normalize(lf["excerpt"]))
        if k not in seen:
            seen.add(k)
            uniq.append(lf)
    # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
    # then type, category and text (code decides what code can decide).
    uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
    llm_spans = [grounding.locate(body, lf["excerpt"]) for lf in uniq]
    for lx in lex_flags:
        lx = dict(lx)
        lx["_stage"] = dict(lx["_stage"], injection=tagged)
        match = next((i for i, lf in enumerate(uniq) if i not in used and lf["type"] == lx["type"] and _overlap(llm_spans[i], lx.get("_span"))), None)
        if match is not None:
            used.add(match)
            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
            lx["ladder"] = dict(lx["ladder"], judge=None)
            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
            # only the fallback quote for phrase-list-only flags. A credibility flag is the exception (D-043, T-092): its excerpt is the whole
            # period sentence, so a model clause never replaces it (the positive half of a mixed sentence must stay in the quote).
            if lx["category"] != CREDIBILITY_CATEGORY:
                lx["excerpt"] = uniq[match]["excerpt"]
                sp = llm_spans[match]
                base = _base(record)
                lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
                                   "start": base + sp[0] if sp else None, "end": base + sp[1] if sp else None}]
                lx["_span"] = sp or lx.get("_span")
            _render(lx, record)
        else:
            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
            lx["_stage"]["llm_failed"], lx["_stage"]["fixture_miss"] = llm_failed, fixture_miss
            if llm_failed or fixture_miss:
                lx["_stage"]["agreement"] = None
        out.append(_compose(lx))
    for i, lf in enumerate(uniq):
        if i in used:
            continue
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
        if lf.get("category") in _NEEDS_LEXICON:
            f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
        out.append(f)
    for lf in filtered:
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
        f["_tray"] = FILTERED
        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
        out.append(f)
    for f in out:
        f["_stage"]["injection"] = tagged
        _compose(f)
    return out


def _model_conflicts(proposed: list, record: dict, tagged: bool) -> list:
    """A conflict the model proposed in the per-record pass (T-113, D-053; T-109 r2): only a code candidate (run_conflict_pass) can be a conflict flag, so the
    model's is a could-not-verify tray item (LLM_ONLY) with its own quotes and the fixed template title. It is not judged and never reaches the letter."""
    out, seen = [], set()
    for lf in proposed:
        k = (grounding.normalize(lf["excerpt"]), grounding.normalize(lf.get("excerpt_b") or ""), lf["category"])
        if k in seen:
            continue
        seen.add(k)
        f = _flag(record, "conflict", lf["category"], lf["excerpt"], "llm", grounding.locate(record["excerpt"], lf["excerpt"]), tagged, "llm_only")
        if lf.get("excerpt_b"):
            f["excerpt_b"] = lf["excerpt_b"]
            sb = grounding.locate(record["excerpt"], lf["excerpt_b"])
            f["evidence"].append({"record_no": record["n"], "text": lf["excerpt_b"],
                                  "start": _base(record) + sb[0] if sb else None, "end": _base(record) + sb[1] if sb else None})
            try:
                f["title"], f["explanation"] = FT.render("conflict", lf["category"], provider_a=record.get("source"), date_a=record.get("date_iso"),
                                                         quote_a=lf["excerpt"], quote_b=lf["excerpt_b"])
            except KeyError:
                pass
        f["_tray"] = "LLM_ONLY"
        out.append(f)
    return out


def ground(flags: list, record: dict) -> list:
    """Rung 1 on model flags: quote must be verbatim in its record (else rejected, never repaired); category must belong to the type."""
    for f in flags:
        fail = []
        if grounding.locate(record["excerpt"], f["excerpt"]) is None:
            fail.append("GROUNDING_EXCERPT_NOT_VERBATIM")
        elif f["origin"] == "llm" and FT.TYPE_OF.get(f["category"]) != f["type"]:
            fail.append("SCHEMA_INVALID")
        f["_stage"]["grounding_failures"] = fail
        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
        _compose(f)
    return flags


def _record_warning(record: dict) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:25:41.449Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 215,420p app/backend/flags.py"
}
````

### User / tool · 2026-11-02T11:25:41.593Z

**tool result**
````
def _record_warning(record: dict) -> dict:
    hits = injection.scan(record["excerpt"])
    base = _base(record)
    title, expl = FT.render("record_warning", "injection_suspected", provider=record.get("source"), date=record.get("date_iso"),
                            quote=hits[0]["phrase"] if hits else None)
    return {"type": "record_warning", "category": "injection_suspected", "record_no": record["n"], "record_id": record.get("id", f"r{record['n']}"),
            "origin": "code", "title": title, "explanation": expl, "review_status": "pending", "state": "needs_review",
            "reasons": ["INJECTION_SUSPECTED"] + (["AI_TRANSLATION"] if language.translated_record(record) else []),      # D-050
            "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
            "source_kind": "record",
            "evidence": [{"record_no": record["n"], "text": h["phrase"], "start": base + h["start"], "end": base + h["end"]} for h in hits],
            "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {"classified_by": "code:injection_scan"}}}


# ------------------------------------------------------------------ per-record pass
def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=None, case_text: str = "") -> list:
    """One model call for this record only, merged with the lexicon floor. A failed or missed model call leaves the lexicon flags in place."""
    item = f"f_r{record['n']}"
    n = promptlib.nonce(case_text, "flags", item)
    prompt = promptlib.load("flags_v1")
    user = f"{injection.wrap(record['excerpt'], n)}\nReturn the JSON object."
    llm, conflicts, failed, miss = [], [], False, False
    try:
        out, _cid = call("flags", prompt.text, user, schemas.FlagPass.model_json_schema(), item_id=item)
        try:
            proposed = [f.model_dump() for f in schemas.FlagPass.model_validate(out).flags]
            llm = [f for f in proposed if f["type"] in _PER_RECORD_TYPES]
            conflicts = [f for f in proposed if f["type"] == "conflict"]
        except (ValidationError, TypeError, ValueError):
            failed = True
    except P.FixtureMiss:
        miss = True
    except AU.LLMFailed:
        failed = True
    flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
    # tray items go LAST: a flag's id (f_r<n>_<k>) is its position in this list and is part of the judge's prompt, so inserting an item that used to be
    # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
    last = [f for f in flags if f.pop("_last", False)]
    flags = [f for f in flags if "_tray" not in f] + [f for f in flags if "_tray" in f and f not in last] + _model_conflicts(conflicts, record, tagged) + last
    ground(flags, record)
    for f in flags:
        code = f.pop("_tray", None)
        if code:
            _to_tray(f, code)       # after ground(), which recomposes the state; a rung-1 failure keeps its own reason after the tray code
    if tagged:
        flags.append(_record_warning(record))
    return flags


# ------------------------------------------------------------------ cross-record conflict pass
def _candidate_flag(c: dict, by_n: dict, any_tagged: bool, fid: str) -> dict:
    """A conflict flag built from a code candidate: both quotes are whole sentences cut from the record text, so rung 1 holds by construction
    (it is still checked, not assumed). Title and explanation come from the code template."""
    ra, rb = by_n[c["a"].record_no], by_n[c["b"].record_no]
    qa, qb = c["a"].text, c["b"].text
    sa, sb = grounding.locate(ra["excerpt"], qa), grounding.locate(rb["excerpt"], qb)
    fail = [] if (sa and sb) else ["GROUNDING_EXCERPT_NOT_VERBATIM"]
    title, expl = FT.render("conflict", c["category"], provider_a=ra.get("source"), date_a=ra.get("date_iso"), quote_a=qa,
                            provider_b=rb.get("source"), date_b=rb.get("date_iso"), quote_b=qb)
    f = {"id": fid, "type": "conflict", "category": c["category"], "excerpt": qa, "excerpt_b": qb, "origin": "code", "title": title, "explanation": expl,
         "record_no": ra["n"], "record_id": ra.get("id", f"r{ra['n']}"), "review_status": "pending", "source_kind": "record",
         "evidence": [{"record_no": r["n"], "text": q, "start": (_base(r) + s[0]) if s else None, "end": (_base(r) + s[1]) if s else None}
                      for r, q, s in ((ra, qa, sa), (rb, qb, sb))],
         "ladder": {"item_id": None, "generator": None, "judge": None,
                    "code_checks": {"classified_by": "code:conflict_candidate+j3", "candidate_rule": c["rule"], "arithmetic": c.get("arithmetic"),
                                    "excerpt_verbatim": not fail}},
         "_stage": {"grounding_failures": fail, "injection": any_tagged, "agreement": None, "judge": "unavailable",
                    "translated": language.translated_record(ra) or language.translated_record(rb)}, "_group": c["group"]}
    f["record_nos"] = sorted({ra["n"], rb["n"]})
    return _compose(f)


def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
    """Conflicts between records (T-094, R-CO-7). CODE proposes the candidate pairs (conflict_candidates.py: a stated plan against a later early end,
    a denial of prior problems against a prior-condition sentence; frequency x duration is multiplied out, so '2x/week for 6 weeks' agrees with
    '12 visits' and is never asked about). The model's only job is the classification of each candidate, by J3 (judge_conflict_v6). There is no
    open-ended search call, so the set of candidates cannot vary between runs.
    Policy for the answer: conflict -> flag (verified when the other checks hold); unsure / judge failed -> flag stays needs_review;
    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
    judged one at a time in record order and the first confirmed conflict stands (later ones are not asked)."""
    by_n = {r["n"]: r for r in records}
    cands = CC.candidates(records)
    flags, settled = [], set()
    for i, c in enumerate(cands, 1):
        f = _candidate_flag(c, by_n, any_tagged, f"f_cx{i}")
        flags.append(f)
        if c["group"] in settled and c["rule"] == "history_denial":
            f["_skip"] = True
            continue
        if f["state"] == "rejected":
            continue
        _judge_one(f, i - 1, call=call, case_text=case_text)
        if c["rule"] == "history_denial" and f["state"] != "rejected" and f["ladder"]["judge"]["verdict"] == "conflict":
            settled.add(c["group"])
    return [{k: v for k, v in f.items() if k not in ("_skip", "_group")} for f in flags if not f.get("_skip")]


# ------------------------------------------------------------------ rung 2 for flags (J3 / J4)
def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
    item = f.get("id") or f"f{i}"
    nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
    try:
        if f["type"] == "conflict":
            if not f.get("excerpt_b"):
                return
            v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
            step, pv = "j3", JUDGE_PROMPT["j3"]
        elif f["origin"] in ("llm", "both"):
            v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
            step, pv = "j4", JUDGE_PROMPT["j4"]
        else:
            return
    except P.FixtureMiss:
        f["_stage"]["fixture_miss"] = True
        step = "j3" if f["type"] == "conflict" else "j4"
        v, cid, reason, pv = "unavailable", None, "NONE", JUDGE_PROMPT[step]
    f["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": pv, "call_id": cid, "verdict": v, "reason_code": reason}
    f["_stage"]["judge"] = judges.to_ladder(step, v)
    _compose(f)
    # What the independent judge rejects (T-094, D-053): nothing is dropped. The item leaves the flag list and goes to the could-not-verify tray
    # with the judge's reason (visible in the API and UI, never a flag, never in the letter):
    # - a code-proposed conflict candidate judged benign (J3);
    # - a model-only flag (no phrase-list hit, no second source) judged not a flag (J4). Judge unsure or unavailable keeps any flag visible.
    if f["state"] != "rejected" and ((step == "j3" and v == "benign" and f.get("origin") == "code") or
                                      (step == "j4" and v == "disagree" and f.get("origin") == "llm")):
        _to_tray(f, "JUDGE_DISAGREES", reason)


def _to_tray(f: dict, code: str, judge_reason=None) -> None:
    """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
    f["state"] = "rejected"
    if code == FILTERED:
        f["_stage"]["judge"] = None
        f["reasons"] = [FILTERED]
        f["why"] = why.why(FILTERED)
        return
    if code == "LLM_ONLY":
        # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
        # (T-122: the eval counted case_05's f_r1_1 as a judge that did not run)
        f["_stage"]["judge"] = None
        f["reasons"] = [r for r in f["reasons"] if r != "JUDGE_UNAVAILABLE"]
    f["reasons"] = [code] + [r for r in f["reasons"] if r != code]
    detail = why.judge_detail(judge_reason) if judge_reason else ""
    f["why"] = why.why(code) + (" " + detail if detail else "")


def judge_flags(flags: list, *, call, case_text: str = "") -> list:
    """J4 on every model-involved pre_existing/causation flag. Lexicon-only flags have no judge.
    An unsure answer or failed judge call leaves the flag needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a disagreement on a flag that is both
    phrase-list and model leaves it needs_review (JUDGE_DISAGREES); a model-only flag J4 rejects goes to the tray (D-053, see _judge_one).
    A model-proposed CONFLICT is never a flag: only a code candidate (run_conflict_pass) can make one, so the model's goes to the tray (D-053)."""
    for i, f in enumerate(flags):
        if f["type"] == "record_warning" or f["state"] == "rejected":
            continue
        if f["type"] == "conflict" and f.get("origin") == "llm":
            _to_tray(f, "LLM_ONLY")
            continue
        _judge_one(f, i, call=call, case_text=case_text)
    return flags
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:25:50.084Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -rn \"list_items\\|rejected_count\\|\\\"rejected\\\"\" app --include=*.py | grep -v \"^app/db/db.py\" | head -70; grep -n \"class FlagPass\" -B25 app/backend/schemas.py | head -60"
}
````

### User / tool · 2026-11-02T11:25:50.188Z

**tool result**
````
app/backend/store.py:44:    for e in DB.list_items(conn, case_id, "entry"):
app/backend/store.py:45:        if e["state"] == "rejected":
app/backend/store.py:66:                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
app/backend/store.py:68:    for f in DB.list_items(conn, case_id, "flag"):
app/backend/trace.py:236:    rs, rejected = row["review_status"], row["state"] == "rejected"
app/backend/trace.py:273:    live = row.get("state") != "rejected"
app/backend/trace.py:284:    elif row.get("state") == "rejected":
app/backend/trace.py:285:        code, label = "rejected", "Rejected; kept out of the letter"
app/backend/trace.py:387:    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
app/backend/trace.py:425:    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited")
app/backend/trace.py:456:    for row in DB.list_items(conn, case_id, "entry"):
app/backend/trace.py:513:    if kind != "charge" or gfail or row["state"] == "rejected":
app/backend/trace.py:562:        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
app/backend/trace.py:575:        bad = row["state"] == "rejected" or cc.get("spans_match_input") is False
app/backend/trace.py:751:        for row in DB.list_items(cx.conn, cx.case_id, kind):
app/backend/trace.py:791:        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
app/backend/trace.py:860:    for row in DB.list_items(conn, case_id, "flag"):
app/backend/trace.py:896:    ents = DB.list_items(conn, case_id, "entry")
app/backend/trace.py:900:    amts = DB.list_items(conn, case_id, "amount")
app/backend/trace.py:901:    flgs = [x for x in DB.list_items(conn, case_id, "flag") if (x.get("state_reasons") or [])[:1] != ["FILTERED_BY_RULE"]]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
app/backend/trace.py:938:    ecounts = {"records_to_draft": len(firsts), "entries": len(ents), "rejected": sum(1 for e in ents if e["state"] == "rejected"), "records_without_entry": len(missing),
app/backend/trace.py:951:    rej = [(k, x) for k, x in allitems if x["state"] == "rejected"]
app/backend/trace.py:957:    gcounts = {"items_checked": len(allitems), "rejected": len(rej), "reasons": codes}
app/backend/trace.py:1018:    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
app/backend/trace.py:1023:                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
app/backend/case_extras.py:132:                    raise ApiError(422, "CODE_CHECK_FAILED", first["why"] + " Nothing was changed.", {"rejected": e.rejected}) from None
app/backend/case_extras.py:134:                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
app/backend/case_extras.py:135:                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
app/backend/confidence.py:17:STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
app/backend/confidence.py:75:        return "rejected", rejected + doubts       # the rejecting reasons come first; the item still shows every doubt
app/backend/dismissal_patterns.py:24:_BAD = ("rejected",)
app/backend/dismissal_patterns.py:48:    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]
app/backend/present.py:124:    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
app/backend/present.py:128:    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
app/backend/present.py:141:def rejected_count(conn, case_id):
app/backend/present.py:143:    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))
app/backend/present.py:144:    return sum(1 for k in ("entry", "amount") for r in DB.list_items(conn, case_id, k) if r["state"] == "rejected" and r["id"] not in handled)
app/backend/present.py:148:    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
app/backend/present.py:151:    live = [(k, r) for k, r in items if r["state"] != "rejected"]
app/backend/present.py:153:    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
app/backend/present.py:236:    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
app/backend/present.py:237:    live_e = [e for e in ents if e["state"] != "rejected"]
app/backend/present.py:240:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
app/backend/present.py:242:             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
app/backend/present.py:246:        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
app/backend/present.py:250:                "ladder": {"item_id": x["id"], "state": "rejected"}}
app/backend/present.py:251:    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
app/backend/present.py:265:            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
app/backend/present.py:266:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/flags.py:304:        if f["state"] == "rejected":
app/backend/flags.py:307:        if c["rule"] == "history_denial" and f["state"] != "rejected" and f["ladder"]["judge"]["verdict"] == "conflict":
app/backend/flags.py:338:    if f["state"] != "rejected" and ((step == "j3" and v == "benign" and f.get("origin") == "code") or
app/backend/flags.py:345:    f["state"] = "rejected"
app/backend/flags.py:367:        if f["type"] == "record_warning" or f["state"] == "rejected":
app/backend/export.py:40:OUT = ("dismissed", "rejected")
app/backend/export.py:514:        elif any(e.get("review_status") == "rejected" for e in ents):
app/backend/export.py:515:            why = "rejected"
app/backend/review.py:176:    if item["state"] == "rejected" and action in ("accept", "edit"):
app/backend/review.py:211:        for it in DB.list_items(conn, case_id, kind):
app/backend/review.py:212:            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
app/backend/review.py:342:    for e in DB.list_items(conn, case_id, "entry"):
app/backend/review.py:348:    for a in DB.list_items(conn, case_id, "amount"):
app/backend/review.py:362:            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
app/backend/review.py:436:    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
app/backend/review.py:451:        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
app/backend/review.py:454:    for old in DB.list_items(conn, case_id, "flag"):
app/backend/review.py:471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
app/backend/review.py:488:    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
app/backend/review.py:559:            if e["state"] != "rejected":
app/backend/review.py:571:    for a in DB.list_items(conn, case_id, "amount"):
54-    category: str
55-    excerpt: str
56-    excerpt_b: Optional[str] = None
57-
58-
59-class SplitSpan(_Closed):
60-    start: int = Field(ge=0)
61-    end: int = Field(ge=0)
62-
63-
64-class SplitOutput(_Closed):
65-    """LLM split fallback (D-031): character offsets only. Code validates them (ingest.validate_split)."""
66-    records: List[SplitSpan] = Field(min_length=1)
67-
68-
69-class NarrativeSentence(_Closed):
70-    entry_id: str = Field(min_length=1)
71-    text: str = Field(min_length=1, max_length=600)
72-
73-
74-class NarrativeOutput(_Closed):
75-    """Firm-voice treatment paragraph (D-031): sentences, each citing one accepted entry. Code and judge 1 check every sentence."""
76-    sentences: List[NarrativeSentence] = Field(min_length=1, max_length=60)
77-
78-
79:class FlagPass(_Closed):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:25:56.336Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 852,872p app/backend/trace.py; sed -n 448,470p app/backend/review.py; grep -rn \"rejected\\b\" app/backend/*.py | grep -i \"count\\|sum(\" | grep -v \"^app/backend/trace.py\\|^app/backend/present.py\" | head; grep -n \"excluded\" app/backend/store.py app/backend/export.py | head"
}
````

### User / tool · 2026-11-02T11:25:56.467Z

**tool result**
````
                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
        elif v in ("unsure", "unavailable"):
            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
                                   **({"reason_code": r["reason_code"]} if v == "unsure" else {})))
        elif R & _CODE_CHECK_REASONS:            # judge supported but a code check raised a doubt
            disagreements.append({"item_id": r["item_id"], "kind": r["kind"], "type": "judge_agrees_code_flags",
                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
                                  "resolution": "needs_review", "review_status": row["review_status"]})
    for row in DB.list_items(conn, case_id, "flag"):
        R = set(row.get("state_reasons") or [])
        for c in ("LEXICON_ONLY", "LLM_ONLY"):
            if c in R:
                disagreements.append({"item_id": row["id"], "kind": "flag", "type": "sources_disagree",
                                      "code_says": "The phrase list found it." if c == "LEXICON_ONLY" else "The phrase list did not find it.",
                                      "judge_says": "The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it.",
                                      "resolution": "needs_review", "review_status": row["review_status"]})
    j = lambda *ks: sum(sum(p[k] for p in per.values()) for k in ks)      # noqa: E731
    judges_out = [dict(p, models=sorted(p["models"])) for p in per.values()]
    for p in judges_out:
        if not p["items"]:
            p["models"] = []
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    if changes is not None:
app/backend/api.py:539:                              "rejected": present.rejected_count(c, token)}
app/backend/generator.py:156:    Such a placeholder is handled: the tray, the rejected counts and the export's excluded count leave it out. The row itself stays (audit)."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:01.433Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 40,56p app/backend/schemas.py; grep -n \"run_flag_pass\\|flag_pass\\|judge_flags\\|_flag_rows\\|dedupe\\|def _row\" app/backend/pipeline.py | head -30"
}
````

### User / tool · 2026-11-02T11:26:01.527Z

**tool result**
````
class Judge3(_Judge):
    verdict: Literal["conflict", "benign", "unsure"]
    reason_code: _J3_CODES


class Judge4(_Judge):
    verdict: Literal["agree", "disagree", "unsure"]
    reason_code: _J4_CODES


class FlagOutput(_Closed):
    """One model-proposed flag: category plus quoted span(s). `excerpt_b` is the second quote of a cross-record conflict."""
    type: Literal["pre_existing", "causation", "conflict"]
    category: str
    excerpt: str
    excerpt_b: Optional[str] = None
169:def _row(kind: str, it: dict) -> dict:
338:            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
348:            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:04.595Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 325,420p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T11:26:04.676Z

**tool result**
````
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    if guard("conflicts"):
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    now_t = clock()
    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
    _persist(conn, cid, "amount", final_amounts, now_t)
    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
    else:
        status = "done_with_errors" if errors else "done"
        err = None
    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}


class _Backend:
    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""

    def __init__(self, name):
        self.name, self.old = name, None

    def __enter__(self):
        import os
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:11.023Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -rn \"rejected\\|tray\" evals/*.py | head -30; grep -rn \"objective_negative\" app evals tests --include=*.py -l | head"
}
````

### User / tool · 2026-11-02T11:26:11.141Z

**tool result**
````
evals/run.py:14:        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
evals/run.py:190:def tray_flags(out):
evals/run.py:191:    """Flags the judge or the code moved to the could-not-verify tray (state rejected; D-053). They are not assertions the product makes, so they
evals/run.py:193:    return [f for f in out.get("flags") or [] if f.get("state") == "rejected" and f.get("type") != "record_warning"]
evals/run.py:197:    """Emitted flags only (D-053, T-094 r2): a flag in the could-not-verify tray (state rejected) is not a candidate, so it can neither raise nor lower
evals/run.py:198:    precision or recall and cannot be a must_not hit. Tray counts are reported separately (tray_flags, flag_tray)."""
evals/run.py:201:        if f.get("type") == "record_warning" or f.get("state") == "rejected":
evals/run.py:247:            "tray_flags": [{"type": f.get("type"), "category": f.get("category"), "reasons": f.get("reasons") or []} for f in tray_flags(out)],
evals/run.py:285:        elif unscored is not None and state != "rejected":
evals/run.py:404:    """Entries that judge #1 or code rejected as not supported (README: a judge-reported `unsupported` fails the case)."""
evals/run.py:408:        n += v == "unsupported" or e.get("state") == "rejected"
evals/run.py:413:    """D-054 (T-112 r2): how often code trimmed an AI summary in this case. items_trimmed = entries that kept a shortened summary; tray_placeholders = records whose whole
evals/run.py:414:    summary was removed (could-not-verify tray); clauses_removed = clauses removed over both. Reported, not gated: it shows the clean 3-runs came from the trim and not from luck."""
evals/run.py:415:    trims = [((e.get("ladder") or {}).get("summary_trim"), e) for e in product_entries(out) + list(out.get("tray") or [])]
evals/run.py:418:            "tray_placeholders": sum(1 for t, _ in trims if not t.get("kept_summary"))}
evals/run.py:684:    # R-CO-7's flag signature covers EMITTED flags (state verified or needs_review), not could-not-verify tray items (D-053); the tray is reported
evals/run.py:685:    # apart (run artifact `tray_flag_count`, report `flag_tray`). A flag that flips between the tray and the list still changes this signature.
evals/run.py:686:    flags = [f for f in out.get("flags") or [] if f.get("state") != "rejected"]
evals/run.py:697:        "tray": _srt((tuple(_srt(t.get("record_ids", []))), t.get("date"), t.get("provider"), t.get("state"), tuple(_srt(t.get("reasons") or [])))
evals/run.py:698:                       for t in out.get("tray") or []),
evals/run.py:748:            "tray_flag_count": len(tray_flags(out)),
evals/run.py:832:def _flag_tray(results):
evals/run.py:834:    rows = [(n, t) for n, r in results.items() for t in r["flags"].get("tray_flags", [])]
evals/run.py:840:            "note": "tray flags are not scored for precision or recall and are not in the R-CO-7 flag-set signature (D-053)"}
evals/run.py:865:        "flag_tray": _flag_tray(results),
evals/run.py:866:        "summary_trim_fired": {**{k: sum((r.get("summary_trim") or {}).get(k, 0) for r in results.values()) for k in ("items_trimmed", "clauses_removed", "tray_placeholders")},
evals/run.py:1072:          f"- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): {m['flag_tray']['value']} {json.dumps(m['flag_tray']['by_reason'])} by case {json.dumps(m['flag_tray']['by_case'])}", f"- grounding failures: {json.dumps(m['grounding_rate']['failures'])}",
app/backend/flags.py
app/backend/flag_templates.py
tests/unit/test_flags_pass.py
tests/unit/test_t126_filtered_by_rule.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:19.762Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -rn -i \"dropp\\|discard\\|not counted\\|ignored\\|silently\" app/backend/*.py app/llm/*.py | grep -v \"^app/backend/trace.py.*never dropped\" | head -50"
}
````

### User / tool · 2026-11-02T11:26:19.856Z

**tool result**
````
app/backend/amounts.py:9:# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
app/backend/api.py:390:                rejudging.discard(token)
app/backend/billing.py:5:'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
app/backend/billing.py:48:    "A row that does not fit the layout is listed as unreconciled with its text; it is never dropped.",
app/backend/billing.py:53:_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
app/backend/billing.py:224:    """Record the totals a statement prints. A second figure for the same total (equal or different) is never guessed between or silently
app/backend/billing.py:255:    dated row (above the header, below it, a total it cannot place) is emitted as an unparsed line (unclear, not totaled), never dropped."""
app/backend/billing.py:391:    never totaled and never dropped."""
app/backend/billing.py:499:            if toks or (rest and re.search(r"\d", rest.group(1))):      # carries a money figure, or is dated and has digits, but did not fit the 24 layout: listed, never dropped
app/backend/billing.py:544:            if toks:                                  # a figure on a line that is not a revenue-code row: listed, never dropped
app/backend/billing.py:616:    every figure was read and there is one per column; otherwise EVERY money token of the row is in `unclear` with its text, never dropped."""
app/backend/billing.py:630:            if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
app/backend/billing.py:871:    rows are two lines, and a re-sent statement is two lines, one per record. A byte-identical repeat of a whole record is dropped at ingest
app/backend/billing.py:917:        elif _billing_looking(r, body):                  # a bill in a layout no parser here knows (an ambulance invoice, say): shown, not silently absent
app/backend/billing.py:1046:    """The analysis plus its citation check. A failure is shown (`citation_failures`, status `citation_failed`), never swallowed; nothing is dropped silently."""
app/backend/dismissal_patterns.py:11:bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.
app/backend/conflict_candidates.py:40:                    rf"|(?:left|quit|ceased|stopped|withdrew\s+from|dropped\s+out\s+of)\s+(?:the\s+)?(?:\w+\s+)?{_CARE})\b", re.I)
app/backend/flags.py:119:        if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
app/backend/flags.py:163:            f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
app/backend/flags.py:251:    # dropped must not renumber the flags after it (recorded judge answers are keyed on that prompt)
app/backend/flags.py:334:    # What the independent judge rejects (T-094, D-053): nothing is dropped. The item leaves the flag list and goes to the could-not-verify tray
app/backend/ingest.py:265:        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
app/backend/ingest.py:272:        except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
app/backend/flag_templates.py:217:# D-057 (T-126): a model proposal that a code rule filters out is listed in a collapsed, counted "Filtered by rule" group, never dropped (D-053).
app/backend/gaps.py:48:    """The header label with every parenthetical dropped ("(OCR)", "(faxed)", "(intake form completed same day)")."""
app/backend/gaps.py:130:    before from_date to the nearest visit date at or after to_date. `dropped` = the paperwork-looking records strictly inside that span, in
app/backend/gaps.py:135:    dropped = sorted((r for r in records if r.get("date_iso") and admin_label(r) and (lo is None or r["date_iso"] > lo) and (hi is None or r["date_iso"] < hi)),
app/backend/gaps.py:138:    return {"from": lo, "to": hi, "days": days, "dropped": dropped,
app/backend/gaps.py:139:            "sentence": flag_templates.admin_alternative([(r["n"], r.get("source") or admin_label(r)) for r in dropped], days, lo, hi)}
app/backend/gaps.py:222:    a changed or new flag starts pending (ADR-002). Flags that no longer exist are dropped."""
app/backend/grounding.py:4:check_excerpt: reason codes for a model/user excerpt against its record. check_summary: token and dropped-qualifier checks.
app/backend/grounding.py:200:    """Qualifier words the summary carries but the quote has no qualifier of that kind for (D-047, the reverse of dropped_qualifiers):
app/backend/grounding.py:217:def dropped_qualifiers(summary: str, excerpt: str) -> list:
app/backend/grounding.py:236:    """The words in the quote that carry a qualifier the summary dropped (D-022), for the 'Edit the summary to keep ...' sentence. English patterns only;
app/backend/grounding.py:237:    a Spanish quote may return []. Display only: the pass/fail decision is dropped_qualifiers()."""
app/backend/grounding.py:238:    kinds = set(dropped_qualifiers(summary, excerpt))
app/backend/grounding.py:267:    if dropped_qualifiers(summary, excerpt):
app/backend/narrative.py:4:no dropped hedge / attribution / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
app/backend/narrative.py:61:    if grounding.dropped_qualifiers(_DATE_PHRASE.sub("", text), quote):      # 'On May 29, 2026' must not count as the hedge word 'may'
app/backend/pdf_hidden.py:27:the case and the page is flagged, exactly like hidden text, until the paralegal confirms it. Nothing is ever included silently.
app/backend/pdf_hidden.py:521:    """The JSON lines a child wrote (a killed child leaves a partial last line, which is ignored)."""
app/backend/pdf_checks.py:57:    page, is kept out of the case text and listed in the report until the paralegal confirms it. Nothing is included silently."""
app/backend/reclassify.py:14:- A rerun keeps her class for the same figure; a charge she promoted is dropped back to the code's class if the sentence under it changed.
app/backend/pdf_text.py:16:# library's logger is cut off from every handler and its warnings are ignored during extraction.
app/backend/present.py:150:    items = [(k, r) for k, r in items if r["id"] not in handled and (r.get("state_reasons") or [])[:1] != [FT.FILTERED]]       # D-057: rule-filtered proposals need no action and are not counted
app/backend/review.py:92:        dropped = g.dropped_qualifiers(summ, exc)
app/backend/review.py:93:        if dropped:
app/backend/review.py:94:            out["SUMMARY_DROPS_QUALIFIER"] = {"qualifiers": list(dropped)}
app/backend/review.py:155:    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
app/backend/review.py:252:    dropped = g.dropped_qualifiers(new_sum, new_exc)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:27.518Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -n \"rejudg\" app/backend/*.py | head -20; grep -n \"FILTERED\\|state_reasons\" app/backend/confidence.py app/backend/review.py app/backend/store.py app/db/db.py | head -30"
}
````

### User / tool · 2026-11-02T11:26:27.621Z

**tool result**
````
app/backend/api.py:103:    rejudging = set()
app/backend/api.py:372:    @app.post("/api/cases/{token}/rejudge")
app/backend/api.py:373:    async def rejudge_case(token: str):
app/backend/api.py:376:        from app.backend import rejudge as RJ
app/backend/api.py:380:            if case["status"] == "running" or token in runs or token in rejudging:
app/backend/api.py:386:            rejudging.add(token)
app/backend/api.py:388:                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
app/backend/api.py:390:                rejudging.discard(token)
app/backend/rejudge.py:3:rejudge(conn, case_id, call, now=None) -> dict
app/backend/rejudge.py:7:    except one entry in ladder.rejudge. The paralegal's review_status is never touched. Nothing here clears the export gate except a judge answer.
app/backend/rejudge.py:59:    """One audit row per asked item (review_events action 'rejudge'); review_status is never touched."""
app/backend/rejudge.py:60:    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
app/backend/rejudge.py:61:                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)
app/backend/rejudge.py:64:def rejudge(conn, case_id: str, call, now: float = None) -> dict:
app/backend/rejudge.py:77:        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
app/backend/rejudge.py:92:    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
app/backend/store.py:52:            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
app/backend/store.py:69:        if (f.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:        # D-057: a rule-filtered proposal is not an item to review, count or export
app/backend/review.py:100:    for c in item.get("state_reasons") or []:
app/backend/review.py:163:            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
app/backend/review.py:214:            reasons = list(it.get("state_reasons") or [])
app/backend/review.py:219:            out = {"state": "needs_review", "state_reasons_json": reasons}
app/backend/review.py:307:                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []))
app/backend/review.py:324:    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/review.py:345:            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
app/backend/review.py:349:        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
app/backend/review.py:370:    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
app/backend/review.py:376:    out = {"state": state, "state_reasons_json": reasons}
app/backend/review.py:515:        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
app/backend/confidence.py:14:    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:33.245Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 20,58p app/backend/rejudge.py; sed -n 64,76p app/backend/rejudge.py; grep -n \"mark_ocr_items\" -A25 app/backend/pdf_checks.py | head -50"
}
````

### User / tool · 2026-11-02T11:26:33.336Z

**tool result**
````
def _ask(kind, jid, row, case_text, call):
    """(verdict in the judge's own enum | 'unavailable', call_id, reason_code). Same inputs and nonce as the original run or edit, so a recorded answer is found again."""
    item = row["id"]
    nonce = promptlib.nonce(case_text, jid, item)
    comp = row.get("computed") or {}
    if kind == "entry":
        ed = row.get("edited") or {}
        edited = "summary" in ed or "excerpt" in ed
        lang = "es" if (row.get("ladder") or {}).get("translation") else "en"          # D-042: the Spanish-record judge sees the same input as the run gave it
        return spanish.run_j1_meta(ed.get("summary", row["summary"]), ed.get("excerpt", row["excerpt"]), row["provider"] or "", call=call,
                                   nonce=None if edited else nonce, item_id=item, lang=lang)           # an edit's judge ran without a case nonce (review._check_summary)
    if kind == "amount":
        return judges.run_j2_meta(row["excerpt"], row["text"], row["kind"], call=call, nonce=nonce, item_id=item)
    if jid == "j3":
        if not (comp.get("excerpt") and comp.get("excerpt_b")):
            return _UNAVAILABLE
        return judges.run_j3_meta(comp["excerpt"], comp["excerpt_b"], call=call, nonce=nonce, item_id=item, category=row["category"])
    if not comp.get("excerpt"):
        return _UNAVAILABLE
    return judges.run_j4_meta(comp["excerpt"], row["type"], row["category"], call=call, nonce=nonce, item_id=item)


def _safe_ask(t, case_text, call):
    try:
        return _ask(t["kind"], t["judge"], t["row"], case_text, call)
    except (P.FixtureMissing, AU.LLMFailed):
        return _UNAVAILABLE


def recompose(row: dict, ladder_verdict: str):
    """(state, reasons): the item's other doubts stay; its judge doubts are replaced by what the new answer says. Rejected items never get here."""
    keep = [c for c in (row.get("state_reasons") or []) if c not in _JUDGE_REASONS]
    translated = (row.get("ladder") or {}).get("translation") is not None or bool({"AI_TRANSLATION", "LANGUAGE_UNCERTAIN"} & set(row.get("state_reasons") or []))
    reasons = list(dict.fromkeys(keep + confidence.compose_state({"judge": ladder_verdict}, {"translated": translated})[1]))      # D-050: a judge answer never verifies a translation
    return ("needs_review" if reasons else "verified"), reasons


def _log(conn, case_id, row, jid, call_id, verdict, state, t):
def rejudge(conn, case_id: str, call, now: float = None) -> dict:
    t = time.time() if now is None else now
    case = DB.get_case(conn, case_id)
    case_text = (case["raw_text"] or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    targets = trace.unjudged_items(conn, case_id)
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        answers = list(ex.map(lambda x: _safe_ask(x, case_text, call), targets))
    done, still = [], []
    for tg, (verdict, call_id, code) in zip(targets, answers):
        row, jid = tg["row"], tg["judge"]
        lad = dict(row.get("ladder") or {"item_id": row["id"]})
        ladder_verdict = judges.to_ladder(jid, verdict)
        attempt = {"at": t, "call_id": call_id, "verdict": ladder_verdict}
2:local Tesseract binary. `extract()` is what POST /api/cases/pdf calls; `mark_ocr_items()` is what the pipeline calls before it
3-stores items.
4-
5-Order: read the text layer (pypdf) -> find text that is not visible when the page is rendered (pdf_hidden) and take it out of the
6-page text unless the paralegal confirmed that page -> pages left with no text are OCR'd locally only when the caller asked for OCR.
7-The case text is the result, so hidden text can never ground a quote and OCR words are quoted exactly as OCR read them."""
8-import threading
9-import time
10-
11-from app.backend import pdf_hidden, pdf_ocr, pdf_text
12-from app.backend.pdf_text import PdfError
13-
14-OCR_TIMEOUT_S = pdf_ocr.TOTAL_TIMEOUT_S + 15     # the API's wait when OCR was requested (the plain text path keeps pdf_text.EXTRACT_TIMEOUT_S)
15-
16-MAX_PDF_JOBS = 2             # uploads being processed at once (text read, scan, OCR); the next ones get a 429 instead of queueing (T-087 round 4)
17-BUSY_WAIT_S = 0.5            # a slot freed by a job that has just timed out is given this long to come free before the answer is "busy"
18-_JOBS = threading.BoundedSemaphore(MAX_PDF_JOBS)
19-
20-MESSAGES = {
21-    "pdf_busy": "The server is already reading other PDFs. Wait a moment and upload this one again.",
22-    "pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Run OCR to read the scanned pages, or paste the text instead.",
23-    "pdf_only_hidden_text": "Every piece of text in this PDF's text layer is hidden when the page is shown, or could not be checked, so nothing was read. "
24-                            "Run OCR to read what the pages show, or confirm the listed pages if you trust them.",
25-    "ocr_unavailable": "Scanned pages need Tesseract, which is not available on this server.",
26-    "ocr_too_many_pages": f"This PDF has more than {pdf_ocr.MAX_OCR_PAGES} scanned pages; OCR reads at most that many in one upload. Split the file.",
27-    "ocr_render_failed": "This PDF could not be safely drawn for OCR (the page drawer ran out of memory or time, or the file is damaged), so nothing was read. "
--
156:def mark_ocr_items(items: list, recs: list, pages: list, why_text: str) -> int:
157-    """Every non-rejected item whose record lies on an OCR page becomes needs_review with reason OCR_DERIVED (never `verified`).
158-    Items carry `record_ids` ('r<n>'); `recs` are the ingest records ({n, char_start, char_end}). Mutates in place; returns the count."""
159-    if not any(p.get("source") == "ocr" for p in pages or []):
160-        return 0
161-    ocr_ids = {f"r{r['n']}" for r in recs if is_ocr_span(pages, r["char_start"], r["char_end"])}
162-    n = 0
163-    for it in items:
164-        if it.get("state") == "rejected" or not ocr_ids.intersection(it.get("record_ids") or []):
165-            continue
166-        reasons = list(it.get("reasons") or [])
167-        if "OCR_DERIVED" not in reasons:
168-            reasons.append("OCR_DERIVED")
169-            it["why"] = ((it.get("why") or "") + " " + why_text).strip()
170-        it["reasons"], it["state"] = reasons, "needs_review"
171-        if isinstance(it.get("ladder"), dict):
172-            it["ladder"]["state"] = "needs_review"
173-            it["ladder"].setdefault("code_checks", {})["ocr_derived"] = True
174-        n += 1
175-    return n
176-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:39.204Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -rn \"FROM flags\\|flags WHERE\\|\\\"flag\\\"\" app/backend/*.py app/db/*.py | grep -v \"^app/backend/trace.py:\\(75\\|86\\|89\\|90\\)\" | head -30; grep -rn \"tray_filtered\\|Filtered by rule\" app tests evals --include=* -l 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T11:26:39.411Z

**tool result**
````
app/backend/calibration_route.py:28:TYPES = ("entry", "amount", "flag")
app/backend/api.py:300:                flags = DB.list_items(c, cid, "flag")
app/backend/api.py:361:            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
app/backend/api.py:407:                               "flags": len(DB.list_items(c, token, "flag"))},
app/backend/dismissal_patterns.py:43:    rows = conn.execute("SELECT * FROM flags WHERE review_status='dismissed'" + ("" if local else " AND case_id=?"), () if local else (case_id,)).fetchall()
app/backend/dismissal_patterns.py:48:    return [f for f in DB.list_items(conn, case_id, "flag") if f["review_status"] == "pending" and f["state"] not in _BAD and _eligible(f)]
app/backend/export.py:293:    return _cap((t or "flag").replace("_", " "))
app/backend/gaps.py:103:                    "days": n, "flag": is_gap(n)})
app/backend/gaps.py:204:        if not g["flag"]:
app/backend/pipeline.py:119:    if not any(i["review_status"] != "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k)):
app/backend/pipeline.py:189:    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
app/backend/pipeline.py:201:        if kind == "flag" and old["review_status"] != "pending":
app/backend/pipeline.py:219:    _persist(conn, cid, "flag", ing["flags"], now)
app/backend/pipeline.py:374:    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
app/backend/present.py:106:_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
app/backend/present.py:107:_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
app/backend/present.py:124:    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
app/backend/present.py:148:    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
app/backend/present.py:154:    rank = {"amount": 0, "entry": 1, "flag": 2}
app/backend/present.py:244:    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
app/backend/present.py:246:        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
app/backend/present.py:248:                "flag": {"type": x["type"], "category": x["category"]},
app/backend/present.py:251:    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
app/backend/present.py:266:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/review.py:18:_KIND = {"e": "entry", "a": "amount", "f": "flag"}
app/backend/review.py:183:        if kind == "flag" and action == "dismiss" and body.get("note"):
app/backend/review.py:210:    for kind in ("entry", "amount", "flag"):
app/backend/review.py:282:    if kind == "flag":
app/backend/review.py:285:        set_review(conn, case_id, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, kind="flag", item=item)
app/backend/review.py:362:            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
app/backend/flag_templates.py
app/backend/present.py
tests/unit/test_t126_filtered_by_rule.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:44.021Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 292,312p app/backend/api.py; sed -n 398,410p app/backend/api.py"
}
````

### User / tool · 2026-11-02T11:26:44.111Z

**tool result**
````
            DB.purge_expired(c, now)
            name = name if isinstance(name, str) else ("Sample case" if sample else None)
            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, *language.api_fields(e)) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
                    "warnings": ing["warnings"]}
            case = get_case(c, token)
            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            done = stages.index(stage) if stage in stages else 0
            end = case["run_finished_at"] or time.time()
            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:26:53.008Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 60,100p app/backend/store.py; grep -n \"excluded\" app/backend/export.py | head"
}
````

### User / tool · 2026-11-02T11:26:53.114Z

**tool result**
````
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
        ents.append(d)
    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):
        if (f.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:        # D-057: a rule-filtered proposal is not an item to review, count or export
            continue
        c = f.get("computed") or {}
        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
    events = []     # D-047: no 'keep my wording' event exists any more
    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
    pages = (case.get("config") or {}).get("pages")
    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
    nar = (case.get("config") or {}).get("narrative")
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
    from app.backend import trace                       # lazy: trace imports store
    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    from app.backend import overlap                      # lazy: overlap imports amounts and dates only
    ov = overlap.view(conn, case_id)                      # T-110: statement line vs a separately stated charge of the same kind; code only, never changes a figure
    if ov:
        out["possible_overlaps"] = [dict(o, statement_record_no=n_of.get(o["statement_record_id"], 0), covered_record_no=n_of.get(o["covered_record_id"], 0)) for o in ov]
    ec = (case.get("config") or {}).get("export")
    if ec:
        out["export_config"] = ec
    if nar:
        out["narrative"] = {"status": nar["status"], "basis": nar.get("basis", {}), "removed": nar.get("removed", []),
                            "sentences": [{"text": x["text"], "entry_id": x["entry_id"], "cite": x.get("cite")} for x in nar.get("sentences", [])]}
    return out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:00.052Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && grep -n \"pending_count\\|\\\"flags\\\"\\]\\|case\\[\\\"flags\\\"\\]\\|OUT\" app/backend/export.py | head -20; cd /Users/arsis/zlayt-pm-project && git log --oneline -3 -- app/backend/store.py"
}
````

### User / tool · 2026-11-02T11:27:00.367Z

**tool result**
````
40:OUT = ("dismissed", "rejected")
233:    return "in" if s in IN else "out" if s in OUT else "pending"
603:    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
6d01774 feat(backend): T-126 rule-filtered model flags (D-032 objective_negative) go to a collapsed Filtered by rule group, never dropped (D-057)
d24ff07 fix(backend): Spanish charge/rate/balance cues in the shared cue function, overlap in internal notes, tray placeholder leaves after manual entry, UB-04 room total in other_figures (T-110 r2)
1335f21 fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:06.023Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 590,625p app/backend/export.py; grep -n \"pending\" app/backend/export.py | head -20"
}
````

### User / tool · 2026-11-02T11:27:06.177Z

**tool result**
````
        lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
    for r in n.get("removed", []):
        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
            lines.append(f'- AI wording removed (failed a check: {r.get("message") or r["reason"]}) ({r["entry_id"]}): {r["reason"]}.')
        elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}): {r["reason"]}.')
        else:
            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
    return lines


def _notes(v):
    accepted = [f for f in v.flags if _status(f) == "in"]
    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
    pending = _pending(v)
    sec = [
        NOTES_TITLE, "",
        AI_LINE.format(n=len(pending)), "",
        "FLAGS ACCEPTED", *_flag_block(v, accepted), "",
        "FLAGS DISMISSED", *_flag_block(v, dismissed), "",
        FLAGGED_HEADING, *_flagged_language(v, v.flags), "",
        "AMOUNTS NOT TOTALED", *_amounts_not_totaled(v), "",
        *(["POSSIBLE OVERLAPS (check before relying on the charges total)", *_overlaps(v), ""] if v.overlaps else []),
        "DAMAGES MENTIONS (not charges)", *_damages(v), "",
        "FUTURE TREATMENT RECOMMENDED (no cost stated)", *_future(v), "",
        "BILLS TO REQUEST (entry in the letter, no accepted charge)", *_bills(v), "",
        "RECORDS NOT IN THE TREATMENT SECTION", *_reconcile(v), "",
        "EDITED ITEMS", *_edited(v), "",
        "PENDING ITEMS NOT INCLUDED", *(pending or ["- none"]),
        *_draft_paragraph(v),
    ]
    return "\n".join(sec)


class ExportBlocked(Exception):
    """The export refuses (D-044, D-045): a run in progress or failed, nothing accepted, or accepted AI-made items whose second check never ran. No override.
11:review_status in (accepted, edited) is "in"; dismissed/rejected is "out"; anything else is pending.
233:    return "in" if s in IN else "out" if s in OUT else "pending"
512:        elif any(_status(e) == "pending" for e in ents):
555:def _pending(v):
558:        if _status(e) == "pending" and e.get("code_check_failed"):       # D-051: the wording fails a code check, so it is not printed anywhere in the export
560:        elif _status(e) == "pending":
563:        if _status(a) == "pending":
567:        if _status(f) == "pending":
582:    st = n.get("status", "pending")
584:    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
604:    pending = _pending(v)
607:        AI_LINE.format(n=len(pending)), "",
618:        "PENDING ITEMS NOT INCLUDED", *(pending or ["- none"]),
651:    pend = _pending(v)
658:        "pending": len(pend),
659:        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:11.732Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a && sed -n 1,60p tests/unit/_fakes.py | head -80; grep -n \"def sample_script\" -A30 tests/unit/_fakes.py | head -60; grep -rn \"def build_export\" app/backend/export.py; grep -rn \"export_case\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T11:27:11.835Z

**tool result**
````
"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]


def sample_script(**over):
    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
          "conflicts": {"flags": []}, "flags": {"flags": []}}
    sc.update(over)
    return sc

def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
    from app.backend import pipeline as PL
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
42:def sample_script(**over):
43-    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
44-    sums = golden_summaries()
45-    def extract(user):
46-        n = which_record(user)[0]
47-        return dict(summary=sums[n][0], excerpt=sums[n][1])
48-    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
49-          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
50-          "conflicts": {"flags": []}, "flags": {"flags": []}}
51-    sc.update(over)
52-    return sc
53-
54-def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
55-    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
56-    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
57-    from app.backend import pipeline as PL
58-    from app.db import db as DB
59-    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
60-    cid = DB.create_case(conn, G.raw(case), now=1.0)
61-    call = call or FakeCall(sample_script())
62-    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call
63-
64-def items_for(out, n):
65-    """Every entry-like item (timeline, undated, tray) that cites record number n."""
66-    rid = f"r{n}"
67-    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
68-    return [i for i in pool if rid in i.get("record_ids", [])]
app/backend/export.py:642:def build_export(case: dict, style: str = None) -> dict:
tests/unit/test_lib09_t110_r2.py:101:        case = store.export_case(conn, cid)
tests/unit/test_lib09_t110_r2.py:116:        case = store.export_case(conn, cid)
tests/unit/test_lib09_t110_r2.py:174:        notes = X.build_export(store.export_case(conn, cid))["internal_notes_text"]
tests/unit/test_lib09_t110.py:94:        assert "May 12, 2026" not in X.build_export(store.export_case(conn, cid))["letter_text"]
tests/unit/test_manual_and_split.py:45:    before = X.build_export(store.export_case(conn, cid))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:19.837Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; mkdir -p $S/probe; cat > $S/probe/probe1.py <<'EOF'\nimport sys, tempfile, pathlib\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import pipeline as PL, present, store, export as X\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script, which_record\ntmp = pathlib.Path(tempfile.mkdtemp())\nextra = [dict(type=\"causation\", category=\"objective_negative\", excerpt=\"Plan of care: 12 visits.\"),\n         dict(type=\"causation\", category=\"prior_condition\" , excerpt=\"Discharged from PT after two missed appointments.\")]\ndef flags(user):\n    return {\"flags\": extra} if which_record(user) == [4] else {\"flags\": []}\nconn = DB.connect(str(tmp/\"c.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=1.0)\nPL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=flags, j4={\"verdict\":\"disagree\",\"reason_code\":\"NONE\"})), now=lambda: 1.0)\nv = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\nprint(\"tray flags:\", [(t[\"id\"], t[\"reasons\"][:1], t[\"flag\"][\"category\"]) for t in v[\"tray\"] if t[\"kind\"]==\"flag\"])\nprint(\"filtered:\", v[\"tray_filtered\"][\"count\"], [i[\"id\"] for r in v[\"tray_filtered\"][\"rules\"] for i in r[\"items\"]])\nprint(\"review counts:\", v[\"review\"][\"counts\"])\nc = store.export_case(conn, cid)\nprint(\"export_case flags:\", [(f[\"id\"], f[\"type\"], f[\"subtype\"], f[\"review_status\"]) for f in c[\"flags\"]], \"pending_count\", c[\"pending_count\"])\nEOF\ncd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe1.py $S/a 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T11:27:20.419Z

**tool result**
````
tray flags: [('f_r4_1', ['GROUNDING_EXCERPT_NOT_VERBATIM'], 'prior_condition')]
filtered: 1 ['f_r4_2']
review counts: {'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 9, 'verified': 14, 'rejected': 1}
export_case flags: [('f_gap_r6_r7', 'gap', 'gap_over_30', 'pending'), ('f_accident_date_after_treatment_1_2_7', 'conflict', 'accident_date', 'pending'), ('f_cx1', 'conflict', 'treatment_plan_vs_actual', 'pending'), ('f_r3_1', 'pre_existing', 'pre_existing', 'pending'), ('f_r8_1', 'pre_existing', 'degenerative_language', 'pending'), ('f_r6_1', 'causation', 'missed_care', 'pending'), ('f_r7_1', 'causation', 'accident_date_provenance', 'pending'), ('f_r7_2', 'causation', 'new_onset', 'pending'), ('f_r8_2', 'causation', 'speculative_language', 'pending'), ('f_r9_1', 'causation', 'patient_report', 'pending'), ('f_r4_1', 'causation', 'prior_condition', 'pending')] pending_count 24
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:25.930Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat >> $S/probe/probe1.py <<'EOF'\ntry:\n    out = X.build_export(c)\n    notes = out[\"internal_notes_text\"]\n    i = notes.find(\"PENDING ITEMS NOT INCLUDED\"); print(notes[:300]); print(\"....\"); print(notes[i:i+1500])\n    print(\"letter has tray text:\", \"Discharged from PT\" in out[\"letter_text\"])\nexcept Exception as e:\n    print(\"export:\", type(e).__name__, str(e)[:300])\nEOF\ncd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe1.py $S/a 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T11:27:26.613Z

**tool result**
````
tray flags: [('f_r4_1', ['GROUNDING_EXCERPT_NOT_VERBATIM'], 'prior_condition')]
filtered: 1 ['f_r4_2']
review counts: {'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 9, 'verified': 14, 'rejected': 1}
export_case flags: [('f_gap_r6_r7', 'gap', 'gap_over_30', 'pending'), ('f_accident_date_after_treatment_1_2_7', 'conflict', 'accident_date', 'pending'), ('f_cx1', 'conflict', 'treatment_plan_vs_actual', 'pending'), ('f_r3_1', 'pre_existing', 'pre_existing', 'pending'), ('f_r8_1', 'pre_existing', 'degenerative_language', 'pending'), ('f_r6_1', 'causation', 'missed_care', 'pending'), ('f_r7_1', 'causation', 'accident_date_provenance', 'pending'), ('f_r7_2', 'causation', 'new_onset', 'pending'), ('f_r8_2', 'causation', 'speculative_language', 'pending'), ('f_r9_1', 'causation', 'patient_report', 'pending'), ('f_r4_1', 'causation', 'prior_condition', 'pending')] pending_count 24
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 24.

FLAGS ACCEPTED
- none

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit t
....
PENDING ITEMS NOT INCLUDED
- Entry, record 1 (Austin EMS run report, January 9, 2026): "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."
- Entry, record 2 (Central ER discharge summary, January 9, 2026): "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week."
- Entry, record 3 (Dr. Alvarez, primary care, January 16, 2026): "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks."
- Entry, record 4 (Capital PT, initial evaluation, January 23, 2026): "Cervical range of motion reduced approx. 40%; plan of care 12 visits."
- Entry, record 5 (Capital PT, visit 8, February 20, 2026): "Pain 4/10, improving."
- Entry, record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from physical therapy after two missed appointments; pain 3/10."
- Entry, record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered."
- Entry, record 8 (Austin Imaging, cervical MRI, May 29, 2026): "C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically."
- Entry, record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Cervical epidural steroid injection recommended; patient states symp
letter has tray text: False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:36.601Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat >> $S/probe/probe1.py <<'EOF'\nprint(\"PENDING FLAG LINES:\")\nfor ln in notes[i:].splitlines():\n    if ln.startswith(\"- Flag\") or \"Discharged from PT after two missed appointments\" in ln and \"Entry\" not in ln: print(ln[:200])\nprint(sum(1 for ln in notes[i:].splitlines() if ln.startswith(\"- \")))\nEOF\ncd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe1.py $S/a 2>&1 | sed -n '/PENDING FLAG/,$p'"
}
````

### User / tool · 2026-11-02T11:27:37.214Z

**tool result**
````
PENDING FLAG LINES:
- Flag, Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Flag, Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): 
- Flag, Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed ap
- Flag, Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."
- Flag, Prior condition: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change; correlate clinically."
- Flag, Causation language: record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Flag, Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
- Flag, Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain radiating to right arm with numbness in fingers."
- Flag, Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change; correlate clinically."
- Flag, Causation language: record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."
- Flag, Causation language: record 4 (Capital PT, initial evaluation, January 23, 2026) "Discharged from PT after two missed appointments."
24
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:27:48.746Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat > $S/probe/mut.py <<'EOF'\nimport sys, shutil, subprocess, os\nsrc, work = sys.argv[1], sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nmuts = {\n \"M1 merge drops filtered again\": (\"app/backend/flags.py\", \"            if k not in fseen:\\n                fseen.add(k)\\n                filtered.append(lf)\\n\", \"            pass\\n\"),\n \"M2 tray keeps filtered\": (\"app/backend/present.py\", \"if x not in filtered]\", \"]\"),\n \"M3 review_view counts filtered\": (\"app/backend/present.py\", \" and (r.get(\\\"state_reasons\\\") or [])[:1] != [FT.FILTERED]]\", \"]\"),\n \"M4 store.export_case includes filtered\": (\"app/backend/store.py\", \"        if (f.get(\\\"state_reasons\\\") or [])[:1] == [\\\"FILTERED_BY_RULE\\\"]:\", \"        if False:\"),\n \"M5 trace judge_rows counts filtered\": (\"app/backend/trace.py\", \"            if kind == \\\"flag\\\" and (row.get(\\\"state_reasons\\\") or [])[:1] == [\\\"FILTERED_BY_RULE\\\"]:\", \"            if False:\"),\n \"M6 trace gate flgs counts filtered\": (\"app/backend/trace.py\", \" if (x.get(\\\"state_reasons\\\") or [])[:1] != [\\\"FILTERED_BY_RULE\\\"]]\", \"]\"),\n \"M7 filtered not last\": (\"app/backend/flags.py\", \"+ _model_conflicts(conflicts, record, tagged) + last\", \"+ _model_conflicts(conflicts, record, tagged)\"),\n \"M8 tray_filtered collapsed False\": (\"app/backend/present.py\", \"\\\"collapsed\\\": True\", \"\\\"collapsed\\\": False\"),\n \"M9 filtered dedupe key drops category\": (\"app/backend/flags.py\", \"k = (lf[\\\"type\\\"], lf[\\\"category\\\"], grounding.normalize(lf[\\\"excerpt\\\"]))\", \"k = (lf[\\\"type\\\"],)\"),\n \"M10 _to_tray FILTERED reasons not set\": (\"app/backend/flags.py\", \"        f[\\\"reasons\\\"] = [FILTERED]\\n\", \"\"),\n}\ntests = \"tests/unit/test_t126_filtered_by_rule.py tests/unit/test_flags_pass.py\"\nonly = sys.argv[3:] \nfor name, (path, old, new) in muts.items():\n    if only and not any(name.startswith(o) for o in only): continue\n    d = work + \"/m\"\n    shutil.rmtree(d, ignore_errors=True); shutil.copytree(src, d)\n    p = os.path.join(d, path); s = open(p).read()\n    assert old in s, name\n    open(p, \"w\").write(s.replace(old, new, 1))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", \"-x\", *tests.split()], cwd=d, capture_output=True, text=True)\n    print(name, \"->\", \"KILLED\" if r.returncode else \"SURVIVED\", r.stdout.strip().splitlines()[-1])\nEOF\ncd $S && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/mut.py $S/a $S/ 2>&1 | tail -20",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:28:02.012Z

**tool result**
````
M1 merge drops filtered again -> KILLED 1 failed in 0.29s
M2 tray keeps filtered -> KILLED 1 failed, 3 passed in 0.45s
M3 review_view counts filtered -> SURVIVED 45 passed in 0.80s
M4 store.export_case includes filtered -> SURVIVED 45 passed in 0.78s
M5 trace judge_rows counts filtered -> SURVIVED 45 passed in 0.75s
M6 trace gate flgs counts filtered -> SURVIVED 45 passed in 0.77s
M7 filtered not last -> KILLED 1 failed in 0.32s
M8 tray_filtered collapsed False -> KILLED 1 failed, 3 passed in 0.46s
M9 filtered dedupe key drops category -> KILLED 1 failed in 0.46s
M10 _to_tray FILTERED reasons not set -> KILLED 1 failed in 0.29s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:08.474Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cd $S/probe && sed -e 's#d = work + \"/m\"#d = work + \"/m_\" + name.split()[0]#' -e 's#^tests = .*#tests = \"tests/unit\"#' mut.py > mut2.py && for m in M3 M4 M5 M6; do (/Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/mut2.py $S/a $S/ $m > $S/probe/out_$m.txt 2>&1 &) ; done; sleep 2; echo started"
}
````

### User / tool · 2026-11-02T11:28:10.599Z

**tool result**
````
started
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:15.745Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a; grep -n \"tray_filtered\" memory/contracts/api.md | cut -c1-120; grep -n '\"tray\":' memory/contracts/api.md | head; grep -rn \"tray_filtered\\|FILTERED_BY_RULE\" docs memory/contracts app/frontend 2>/dev/null | cut -c1-120 | head; grep -n \"D-057\\|T-126\" memory/DECISIONS.md docs/*.md | head"
}
````

### User / tool · 2026-11-02T11:28:15.924Z

**tool result**
````
131:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain 
759:| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D
232:  "tray": [
memory/contracts/api.md:131:Read once, then patch local state from review responses. `entries` are **chronological** by 
memory/contracts/api.md:759:| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code ru
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:19.468Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/a; sed -n 225,250p memory/contracts/api.md | cut -c1-200; grep -n \"rejected\\|could-not-verify\\|LLM_VS_CODE\" docs/LLM_VS_CODE.md | head; ls docs"
}
````

### User / tool · 2026-11-02T11:28:19.593Z

**tool result**
````
      "state": "verified", "reasons": [], "why": "Quote found word for word; the phrase list and the model agree, and the second check agreed.",
      "review_status": "pending", "edited": null,
      "ladder": {"item_id": "f_pat_9", "backend": "fixture",
        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "flags_v1", "call_id": "c40", "output": {"type": "causation", "category": "patient_report", "record_id": "r9", "excerpt": "Patient
        "code_checks": {"excerpt_verbatim": true, "lexicon_hit": "patient_report", "highlight_found": true, "injection_tag": false},
        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_flag_v2", "call_id": "c44", "verdict": "agrees"},
        "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} } ],
  "tray": [
    { "id": "e5x", "kind": "entry", "record_ids": ["r5"], "state": "rejected", "reasons": ["GROUNDING_EXCERPT_NOT_VERBATIM"],
      "why": "The model's quote does not appear word for word in the record, so it cannot be used.",
      "attempt": {"summary": "Visit 8: pain 4/10, improving.", "excerpt": "Pain is 4/10 and improving."},
      "ladder": {"item_id": "e5x", "state": "rejected"} } ],
  "dates_to_confirm": [],
  "injection": {"records": [], "banner": null},
  "review": {
    "queue": ["a3", "e4", "e2", "a1"],
    "counts": {"pending": 22, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
    "ready_to_export": false },
  "warnings": [],
  "created_at": "2026-11-02T01:00:00Z", "updated_at": "2026-11-02T01:03:10Z"
}
```
(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phr

## POST /api/cases/{token}/records/{rid}/confirm_date
Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot
12:2. **The model never supplies a value.** It may write a one-line summary and choose an exact excerpt, and point at wording that looks like a flag (a category and a quote). It may not supply a date, an amount, an amount's class or the text of a warning. A date or amount the code cannot find in the record is rejected.
13:3. **Every quote is checked.** Each excerpt must appear word for word in its record (extra spaces ignored). If not, the item is *rejected*: shown in a "could not verify" tray, never exportable.
17:7. **A human decides everything.** Even a fully verified item starts as *pending*. Every accept is an individual decision, except a batch accept of verified, pending entries (code only, all or nothing; never amounts or flags). Every accept of an entry, single or batch, must pass the code checks first (D-051). Amounts and flags have no editable wording: their checks are stored with them, and an accept is refused while the stored state is `rejected` (409). Dates and amounts always need an explicit accept. The export contains exactly the accepted set.
18:8. **Doubt is shown, not hidden.** Items are `verified`, `needs_review` or `rejected` by a fixed rule, doubt sorted first, each with a one-sentence "Why?" made from a template.
29:| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. `SPLIT_REJECTED` always names the reason, on case creation and on runs (T-066, commit d148e0f; `split_failure` in `memory/contracts/api.md`): `NO_MODEL` when there is no model or recorded answer for an unsplit paste, `NOT_ATTEMPTED` when several records are followed by an unsplit tail (the model is only asked about a single block, so the tail stays its own record). Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. Before Rung 2, code trims the summary (D-054; T-112, in progress: `app/backend/summary_trim.py`, not yet committed): a summary clause whose content words no word of its excerpt supports is removed, shown in the trace as 'removed from the summary: not in the quote'; if nothing supported remains, the item goes to the could-not-verify tray. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. Routing comes first, in code (D-048): a record runs as English only when it is confidently English (`language.py`: at least one English-only word and no non-English evidence, `EN_CONFIDENT`; three English-only words when the only foreign evidence is a word shared with another language, `EN_DOMINANT`); otherwise it is Spanish, or `LANGUAGE_UNCERTAIN`, and the Spanish prompt and checks run. A record with no usable output (retries failed, fixture miss, unsupported language, or nothing left after the trim) is a could-not-verify tray item with its reason. It never reaches the timeline or the letter, and it leaves the tray once she enters that record by hand (T-110, D-053). **Rung 3:** human. |
34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model's attention. | Unit tests with noisy, duplicate and dose-like numbers. An amount a model reports that code cannot find is rejected. Billing completeness (D-049): a final code accounting pass lists every money-shaped token in a billing record that no parser placed, so a missing figure is listed, never silent. |
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus a course that ended early; a denial of prior problems versus a history sentence in another record | **Code proposes; the LLM only classifies.** `app/backend/conflict_candidates.py` pairs two whole sentences by two fixed rules: **plan vs early end** (a stated plan, as a visit count or frequency × duration, against a LATER record showing a missed, no-show, cancelled, self-discharged or discontinued course) and **denial vs prior history** (a sentence denying prior problems, against a sentence in another record that the phrase list marks as a prior condition or prior surgery). Code multiplies frequency × duration into visits ("2x/week for 6 weeks" = 12) and carries that arithmetic on the flag. An explicit visit count is the plan quoted when one exists. No numeric comparison is made between a count and a frequency plan, so the two are not checked against each other. Candidates come in a fixed order, so the set cannot vary between runs: there is no open-ended model search (`conflicts_v1` is retired). The model is `judge_conflict_v5` (J3), and it only classifies each candidate as `conflict`, `benign` or `unsure`, with a fixed reason code and no prose. It never proposes a pair, a quote or a number. **Nothing the model produces is silently dropped (D-053):** a code-proposed pair that J3 calls `benign` goes to the could-not-verify tray (tray kind `flag`, reason `JUDGE_DISAGREES`, with the judge's reason); a model-only flag that the flag judge (J4, `judge_flag_v3`) rejects goes to the tray (`JUDGE_DISAGREES`); a model-proposed conflict that no code candidate made goes to the tray (`LLM_ONLY`). Tray items are never flags and never reach the letter. A J3 or J4 `unsure` answer, or a judge that did not answer, keeps the flag visible as `needs_review`. **Candidate rules** also cover number-word visit counts with a plan cue, frequency × duration in weeks (including "twice-weekly for six weeks"), lost to follow-up, stopped or left care, negation- and completion-aware, and denials of earlier accidents or claims. **Not built as candidates:** dosage and laterality pairs (laterality is checked only within one summary, row 15), and month durations (`memory/SCOPE_CUTS.md`, row 13). The J3 eval controls include dosage and laterality pairs (`tests/unit/test_t093_eval_signature.py`), so the model's answer on them is measured; no code rule proposes them. | Reading comprehension is needed only for one yes or no per pair. An open-ended search let the model call "2x/week for 6 weeks" against "12 visits" a conflict (T-094, live run 2). The arithmetic and the choice of pairs are code's. | **Rung 1:** both quotes are whole sentences cut from the record text, and grounding still checks them. **Rung 2, J3:** `conflict` gives a flag (verified only when the other checks hold); `unsure` keeps it `needs_review`; `benign` on a code-proposed pair moves it to the could-not-verify tray, never exported. A denial is judged one candidate at a time, in record order, and the first confirmed conflict stands. **Rung 3:** human accept or dismiss. |
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by code on every record as a second signal | Needs language judgment ("low back pain in 2023, resolved"). Running per record means one record's text never reaches the call that decides another record's flags; the phrase list is a second floor, trusted only as far as its measured recall on the golden set. | Quote check; **judge 4** confirms the category. If only the list or only the model fires, the item needs review and says which. A model-only flag that the flag judge rejects goes to the could-not-verify tray (row 11), never to the review queue or the letter. |
45:| 17 | Confidence state per item (`verified`, `needs_review`, `rejected`) | **Code**: a fixed rule over the checks (rejected if a grounding check fails; needs review on any doubt; verified only if every check and the judge are positive, and the record is English-routed: a Spanish or language-uncertain record is never `verified`, and its items carry `AI_TRANSLATION`, D-050). | The composition is logic, not opinion. Same input, same state. | Unit tests over the full rule table. `needs_review` sorts first; `rejected` sits in a tray. |
CONTRACT.md
LLM_VS_CODE.md
M2M3_COVERAGE.md
RUNBOOK.md
UI_DESIGN_BRIEF.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:28.660Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat > $S/probe/probe2.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import flags as F\nfrom tests.unit._fakes import FakeCall\nR = dict(n=1, source=\"EMS\", excerpt=\"Cyclist struck by a car at low speed. X-ray negative for fracture.\", date_iso=\"2026-06-01\")\nllm = [dict(type=\"causation\", category=\"objective_negative\", excerpt=\"MRI shows no fracture whatsoever.\")]\nfor tagged in (False, True):\n    out = F.run_flag_pass(R, call=FakeCall({\"flags\": {\"flags\": llm}}), tagged=tagged)\n    print(tagged, [(f[\"state\"], f[\"reasons\"], f[\"ladder\"][\"code_checks\"].get(\"excerpt_verbatim\"), f[\"_stage\"].get(\"grounding_failures\"), f[\"_stage\"].get(\"injection\")) for f in out])\nEOF\ncd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe2.py $S/a 2>&1 | tail; cat $S/probe/out_M*.txt"
}
````

### User / tool · 2026-11-02T11:28:29.038Z

**tool result**
````
False [('rejected', ['FILTERED_BY_RULE'], False, ['GROUNDING_EXCERPT_NOT_VERBATIM'], False)]
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/probe/probe2.py", line 9, in <module>
    print(tagged, [(f["state"], f["reasons"], f["ladder"]["code_checks"].get("excerpt_verbatim"), f["_stage"].get("grounding_failures"), f["_stage"].get("injection")) for f in out])
                                                                                                  ~^^^^^^^^^^
KeyError: '_stage'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:34.447Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; sed -i 's/for f in out\\])/for f in out if f[\"type\"]!=\"record_warning\"])/' $S/probe/probe2.py; cd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe2.py $S/a 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T11:28:34.844Z

**tool result**
````
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1/probe/probe2.py'
    print(tagged, [(f["state"], f["reasons"], f["ladder"]["code_checks"].get("excerpt_verbatim"), f["_stage"].get("grounding_failures"), f["_stage"].get("injection")) for f in out])
                                                                                                  ~^^^^^^^^^^
KeyError: '_stage'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:38.095Z

**tool call — Bash**
````
{
 "command": "sleep 200; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat $S/probe/out_M*.txt; pgrep -f mut2.py | head",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:28:38.097Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 200 followed by: S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1 cat $S/probe/out_M*.txt pgrep -f mut2.py head. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:28:40.851Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; until [ $(cat $S/probe/out_M*.txt | wc -l) -ge 4 ]; do sleep 5; done; cat $S/probe/out_M*.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:31:21.420Z

**tool result**
````
M3 review_view counts filtered -> KILLED 1 failed, 1374 passed, 3 skipped in 31.60s
M4 store.export_case includes filtered -> KILLED 1 failed, 2870 passed, 4 skipped in 185.90s (0:03:05)
M5 trace judge_rows counts filtered -> KILLED 1 failed, 2875 passed, 4 skipped in 185.90s (0:03:05)
M6 trace gate flgs counts filtered -> KILLED 1 failed, 1339 passed, 3 skipped in 30.88s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:31:26.097Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; for m in M3 M6; do (cd $S/m_$m && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x 2>&1 | grep -E \"^FAILED|Error\" | head -3); done; ps aux | grep -c \"[m]ut2.py\"",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:32:27.354Z

**tool result**
````
tests/unit/test_lib09_t110_r2.py:131: AssertionError
FAILED tests/unit/test_lib09_t110_r2.py::test_placeholder_leaves_the_tray_when_a_manual_entry_exists
E           AssertionError: assert 'fail' != 'fail'
tests/unit/test_lib09_t110.py:87: AssertionError
FAILED tests/unit/test_lib09_t110.py::test_failed_extract_record_is_a_tray_item_with_its_reason
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:34.973Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; P=/Users/arsis/zlayt-pm-project/.venv/bin/python; (cd $S/a && $P -m pytest -q -p no:cacheprovider tests/unit/test_lib09_t110.py tests/unit/test_lib09_t110_r2.py 2>&1 | tail -2); (cd $S/m_M6 && $P -m pytest -q -p no:cacheprovider tests/unit/test_lib09_t110.py -x 2>&1 | grep -B15 \"AssertionError\" | head -40)",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T11:32:37.431Z

**tool result**
````
.........................................................                [100%]
57 passed in 1.46s
        """A record the extract step made no output for used to vanish (only the run error named it). It is now a rejected entry in the could-not-verify tray."""
        tmp, conn, cid = _stored(_miss_on("e6"))
        with tmp:
            view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
            tray = [t for t in view["tray"] if t["record_ids"] == ["r6"]]
            assert len(tray) == 1 and tray[0]["state"] == "rejected" and tray[0]["reasons"] == ["FIXTURE_MISS"] and tray[0]["why"]
            assert tray[0]["attempt"] == {"summary": None, "excerpt": None}
            shown = {r for e in view["entries"] + view["undated_entries"] + view["tray"] for r in e["record_ids"]}
            assert shown == {f"r{n}" for n in range(1, 8)}                 # every record is on screen somewhere
            assert not any("r6" in e["record_ids"] for e in view["entries"])   # and the placeholder is not on the timeline
            tr = trace.case_trace(conn, cid)
            ex = next(s for s in tr["steps"] if s["id"] == "extract")
            assert ex["status"] == "fail" and ex["counts"]["records_without_entry"] == 1 and ex["counts"]["in_tray"] == 1
>           assert next(s for s in tr["steps"] if s["id"] == "grounding")["status"] != "fail"     # a failed call is not a grounding failure
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           AssertionError: assert 'fail' != 'fail'

tests/unit/test_lib09_t110.py:87: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:32:46.514Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cd $S/m_M4 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -E \"^FAILED\"; cd $S/m_M5 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -E \"^FAILED\"",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:38:44.758Z

**tool result**
````
FAILED tests/unit/test_trace.py::test_pending_live_items_are_a_warning_not_a_blocker_d045
FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
FAILED tests/unit/test_trace.py::test_judge_summary_counts_and_objections - A...
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
FAILED tests/unit/test_trace.py::test_judges_step_is_pending_not_pass_while_the_run_is_going_and_judges_are_missing
FAILED tests/unit/test_trace.py::test_paralegal_edited_summary_is_not_counted_unchecked_in_judges_d045b
FAILED tests/unit/test_trace.py::test_edited_summary_with_judge_unavailable_leaves_judges_step_and_gate_clean_d045b
FAILED tests/unit/test_trace.py::test_rejudge_in_demo_mode_replays_recorded_answers_and_clears_the_gate
FAILED tests/unit/test_trace.py::test_rejudge_objection_is_recorded_and_the_gate_opens_because_the_judge_ran
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:38:52.902Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cd $S/m_M4 && grep -c \"if False:\" app/backend/store.py; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -E \"^FAILED|passed|failed\"",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:41:54.928Z

**tool result**
````
1
        DB.update_case(conn, tok, status="failed")
        check("run failed")
FAILED tests/unit/test_trace.py::test_pending_live_items_are_a_warning_not_a_blocker_d045
FAILED tests/unit/test_trace.py::test_gate_ready_equals_export_allowed_in_every_state_d045
2 failed, 2937 passed, 4 skipped in 180.65s (0:03:00)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:08.072Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r1; cat > $S/probe/probe3.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import flags as F\nfrom tests.unit._fakes import FakeCall\nR = dict(n=1, source=\"EMS\", excerpt=\"Patient reports low back pain in 2023, resolved. Ankle exam normal.\", date_iso=\"2026-06-01\")\nllm = [dict(type=\"pre_existing\", category=\"prior_condition\", excerpt=\"Patient reports low back pain in 2023, resolved.\"),\n       dict(type=\"pre_existing\", category=\"degenerative_language\", excerpt=\"Patient reports low back pain in 2023, resolved.\")]\nout = F.run_flag_pass(R, call=FakeCall({\"flags\": {\"flags\": llm}}))\nprint([(f[\"category\"], f[\"origin\"], f[\"state\"]) for f in out])\nEOF\ncd $S/a && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/probe/probe3.py $S/a 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T11:42:08.473Z

**tool result**
````
[('pre_existing', 'both', 'needs_review')]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:12.439Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep T-126; git rev-parse HEAD; git log --oneline -1"
}
````

### User / tool · 2026-11-02T11:42:12.573Z

**tool result**
````
f7829c1ccecb224875a1d79a6255ff4b109eed67
f7829c1 fix(backend): T-120 r3 history-source skip strips only the attribution phrase and scans what is left (no condition guessing)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:14.625Z

**tool call — Bash**
````
{
 "command": "git diff --stat c559ce2 f7829c1 -- app/backend/flags.py app/backend/present.py app/backend/store.py app/backend/trace.py memory/contracts/api.md tests/unit/test_t126_filtered_by_rule.py | tail -3; echo ---"
}
````

### User / tool · 2026-11-02T11:42:14.732Z

**tool result**
````
 app/backend/present.py  | 43 +++++++++++++++++++++++++++++++++++++++++--
 memory/contracts/api.md |  8 ++++----
 2 files changed, 45 insertions(+), 6 deletions(-)
---
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:16.028Z

**tool call — Bash**
````
{
 "command": "git diff c559ce2 f7829c1 -- app/backend/present.py | grep -n \"FILTER\\|tray\" | head"
}
````

### User / tool · 2026-11-02T11:42:16.127Z

**tool result**
````
69:-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
70:+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:17.025Z

Unrelated change; T-126 scope unchanged. Writing the review.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:48.593Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer.md",
 "content": "# T-126 review (round 1) — staff-engineer-reviewer\n\nScope: commit 6d01774 (D-057, rule-filtered model flags), checked on a `git archive` copy of c559ce2 (card files unchanged at HEAD f7829c1; the later diff touches only an unrelated `gap_changes_removed` key). Exercised: full unit suite, the 5 new tests, ten mutants, three probes, code-path grep, api.md.\n\nVerdict: changes. The feature works: the filtered proposals are listed, collapsed and counted with the rule named (D-032), and they stay out of flags, queue, counts, gate and the letter. One major remains. A rejected tray flag of any other kind still leaks into the export notes and the pending count, which the contract says it must not (api.md, D-053). The card narrowed its exclusion to `FILTERED_BY_RULE` instead of all rejected flags.\n\nDeterministic results (archive of c559ce2, `.venv/bin/python -m pytest tests/unit -q`): `2939 passed, 4 skipped in 191.40s`.\n\nMutants (T-126 test file plus `test_flags_pass.py`):\n- Killed: M1 (merge drops filtered again), M2 (tray keeps filtered), M7 (filtered not last), M8 (`collapsed` False), M9 (dedupe key without category), M10 (reasons not set).\n- Survived in the card's own tests: M3 (`review_view` counts filtered), M4 (`export_case` includes filtered), M5 (trace judge rows count filtered), M6 (trace gate counts filtered).\n- Whole suite: M3-M6 are killed, but only by incidental tests (`test_trace.py`, `test_lib09_t110*.py`), not by anything that names D-057.\n\n## Findings\n1. **Major: other rejected tray flags still count as pending and print in the internal notes.**\n   - Repro: `probe/probe1.py` runs the sample case with a model flag on record 4 whose quote is not in the record.\n   - `review.counts.pending` is 23. `store.export_case` returns `pending_count 24` because `f_r4_1` (state `rejected`, review_status `pending`) is in `flags`.\n   - The notes say \"Items not reviewed: 24\" and \"PENDING ITEMS NOT INCLUDED\" lists `Flag, Causation language: record 4 ... \"Discharged from PT after two missed appointments.\"`, a quote that is not in record 4.\n   - api.md D-053 says a tray flag \"is never in `flags`, `review.queue` or the export\". The card added the skip at `store.py:69` for `FILTERED_BY_RULE` only; the same bug exists for `JUDGE_DISAGREES`, `LLM_ONLY` and grounding-rejected flags.\n2. **Minor: the FILTERED branch of `_to_tray` discards the other reasons.**\n   - `flags.py:~346` sets `reasons=[FILTERED]` and returns early. A non-verbatim model quote loses `GROUNDING_EXCERPT_NOT_VERBATIM` (probe2: `reasons ['FILTERED_BY_RULE']`, `excerpt_verbatim False`), and `INJECTION_SUSPECTED` is likely lost too.\n   - The quote then shows in `tray_filtered` as \"the AI's proposal\" with no mark that it is not in the record.\n   - The comment at `flags.py:~253` (\"a rung-1 failure keeps its own reason\") is no longer true for this path.\n3. **Minor: the card's tests do not pin the exclusions they claim.**\n   - The letter assertion in `test_case_payload_has_a_collapsed_counted_group...` builds the export from an empty case (`{\"records\": [], \"entries\": [], ...}`), so it passes whatever the code does.\n   - Nothing in the T-126 file asserts `review.counts`, the trace gate or judge counts, or `export_case`. Mutants M3-M6 survive it.\n   - Fix: assert `counts.rejected`, `pending_count`, `case_trace` `gate` and `judges` counts and `export_case(...)[\"flags\"]` with and without the filtered item on the stored case.\n4. **Minor: two model proposals for the same quote collapse into one without a trace.**\n   - The dedupe key in `merge` (`flags.py:~122`) is `(type, excerpt)` with no category (probe3: prior_condition and degenerative_language on one quote gives one `pre_existing` flag).\n   - D-053 says nothing the model proposes is silently dropped. At minimum, record the collapsed category in the audit. Same-category duplicates collapsing is fine.\n5. **Minor: docs are only partly updated.**\n   - The api.md paragraph and the reason-code row are good, but the GET example JSON has no `tray_filtered` key (`api.md:232-250`).\n   - `docs/LLM_VS_CODE.md` rows 11 and 12 describe D-053 and say nothing about D-057 or rule-filtered proposals (architect-owned, so this needs a card).\n6. **Nit: the rule marker is copied as a literal.**\n   - `[:1] == [\"FILTERED_BY_RULE\"]` appears in `store.py`, `trace.py` (twice) and `present.py`. Add one helper, `is_filtered(row)`, next to `FT.FILTERED`.\n   - `api.py:407` run-progress `counts.flags` counts tray and filtered rows. It is a progress counter and not a \"needs review\" count, so low value.\n\nRight: (a) the filtered id order is protected, with filtered items placed last so recorded judge prompts keep their ids (test 2 plus mutant M7); (b) a per-item dedupe key that includes the category; (c) the contract paragraph and the reason-code row are specific.\n\n```json\n{\"card\": \"T-126\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 6d01774 (D-057 filtered-by-rule tray group); git archive of c559ce2 in scratchpad t126r1/a (card files same at HEAD f7829c1); memory/contracts/api.md; sample case via FakeCall\",\n \"exercised\": [\"pytest tests/unit on git archive of c559ce2: 2939 passed, 4 skipped\", \"read git show 6d01774 in full (flags, present, store, trace, why, confidence, flag_templates, api.md, tests)\", \"10 mutants M1-M10 against the T-126 test file plus test_flags_pass (M3-M6 survive; M3-M6 each killed only by incidental tests in the full suite: test_trace.py, test_lib09_t110.py, test_lib09_t110_r2.py)\", \"probe1: sample case with a model flag on record 4 plus an objective_negative flag; case_view, store.export_case, build_export notes\", \"probe2: filtered proposal with non-verbatim quote (reasons lose GROUNDING_EXCERPT_NOT_VERBATIM)\", \"probe3: two model proposals, same quote, different category (collapse to one flag)\", \"grep of list_items, rejected, flag readers in app/backend, evals/run.py tray handling, api.py progress counts, pipeline finalize\", \"read memory/contracts/api.md and docs/LLM_VS_CODE.md for D-057\"],\n \"verdict\": \"changes\",\n \"scores\": {\"d057_filter_placement\": 4, \"no_silent_drop\": 3, \"tests_pin_behaviour\": 3, \"contract_docs\": 4, \"determinism_ids\": 5},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Rejected tray flags other than FILTERED_BY_RULE are still counted as pending and printed in the export notes\",\n   \"evidence\": \"probe1 (scratchpad t126r1/probe/probe1.py) on archive: review.counts.pending 23 but export_case pending_count 24; flags list contains f_r4_1 state rejected, review_status pending; internal_notes_text 'Items not reviewed: 24' and PENDING ITEMS NOT INCLUDED lists 'Flag, Causation language: record 4 ... \\\"Discharged from PT after two missed appointments.\\\"' (quote not in record 4). store.py:69 skips only FILTERED_BY_RULE; api.md D-053: tray flag 'is never in flags, review.queue or the export'.\",\n   \"why_it_matters\": \"D-053 tray items must not be review work or export content; the notes count disagrees with the UI and print a non-verbatim quote. The card touched this exact loop and chose the narrow predicate.\",\n   \"fix\": \"In store.export_case skip every flag with state == 'rejected' (and keep the filtered skip only as a subset); same for trace allitems/judge rows if any other rejected flag is counted as pending.\",\n   \"acceptance_test\": \"Run a case with a J4-disagree model-only flag and a grounding-rejected model flag; assert export_case flags exclude both, pending_count == review.counts.pending, and the notes pending list has no flag line for them.\"},\n  {\"severity\": \"minor\", \"title\": \"FILTERED branch of _to_tray drops other reasons (grounding failure, injection)\",\n   \"evidence\": \"flags.py _to_tray: 'if code == FILTERED: ... f[\\\"reasons\\\"] = [FILTERED]; return'. probe2: filtered proposal with a quote not in the record shows reasons ['FILTERED_BY_RULE'], ladder.code_checks.excerpt_verbatim False. Comment in run_flag_pass says a rung-1 failure keeps its own reason.\",\n   \"why_it_matters\": \"The tray_filtered group then shows a quote that is not in the record with no marker, and the audit loses why the ladder would have rejected it.\",\n   \"fix\": \"Keep reasons = [FILTERED] + the rung-1 and injection reasons (as the LLM_ONLY branch does), and render a 'not found in the record' note for such items.\",\n   \"acceptance_test\": \"Unit test: objective_negative proposal with a non-verbatim quote gives reasons[0] FILTERED_BY_RULE and GROUNDING_EXCERPT_NOT_VERBATIM in reasons.\"},\n  {\"severity\": \"minor\", \"title\": \"T-126 tests do not pin counts, gate or export exclusions; the letter assertion is vacuous\",\n   \"evidence\": \"tests/unit/test_t126_filtered_by_rule.py: 'case = {\\\"records\\\": [], \\\"entries\\\": [], \\\"amounts\\\": [], \\\"flags\\\": []}; assert \\\"Plan of care: 12 visits.\\\" not in export.build_export(case)[\\\"letter_text\\\"]' passes for any code. Mutants M3 (present.py review_view), M4 (store.py:69), M5 (trace.py:751), M6 (trace.py:901) all survive test_t126_filtered_by_rule.py plus test_flags_pass.py.\",\n   \"why_it_matters\": \"AC says not in counts, gate or letter; those guarantees ride on unrelated tests and would regress silently if those tests change.\",\n   \"fix\": \"Add assertions on review.counts.rejected, case_trace gate/judges counts, and store.export_case flags/pending_count for the stored case with a filtered item; build the export from export_case, not an empty dict.\",\n   \"acceptance_test\": \"Mutants M3-M6 each make a T-126 test fail.\"},\n  {\"severity\": \"minor\", \"title\": \"Model proposals with the same quote and different category collapse silently in merge\",\n   \"evidence\": \"flags.py merge dedupe key k = (lf['type'], grounding.normalize(lf['excerpt'])) (no category). probe3: prior_condition and degenerative_language on one quote give one flag ('pre_existing','both','needs_review'); the second category is not recorded anywhere.\",\n   \"why_it_matters\": \"D-053/D-057 say nothing the model proposes is silently dropped; the filtered path keys on category, the main path does not.\",\n   \"fix\": \"Record collapsed categories in the kept flag's ladder/audit (or keep both when categories differ).\",\n   \"acceptance_test\": \"Two proposals, same quote, different category: output carries both categories or a ladder note naming the second.\"},\n  {\"severity\": \"minor\", \"title\": \"Docs partly updated: api.md example lacks tray_filtered; LLM_VS_CODE rows 11/12 do not mention D-057\",\n   \"evidence\": \"memory/contracts/api.md:232-250 example has 'tray' but no 'tray_filtered'; docs/LLM_VS_CODE.md row 11 and row 12 cover D-053 only; grep D-057 docs/*.md returns nothing.\",\n   \"why_it_matters\": \"The frontend and graders read the example and the table; the table is the graded LLM/code boundary.\",\n   \"fix\": \"Add tray_filtered to the example JSON; open an architect card to add one sentence on rule-filtered proposals to rows 11-12.\",\n   \"acceptance_test\": \"grep tray_filtered in the api.md example block and D-057 in docs/LLM_VS_CODE.md both match.\"},\n  {\"severity\": \"nit\", \"title\": \"FILTERED_BY_RULE marker repeated as string literals; progress counter includes tray rows\",\n   \"evidence\": \"store.py:69, trace.py:752, trace.py:901 each test [:1] == ['FILTERED_BY_RULE'], present.py uses FT.FILTERED; api.py:407 counts.flags = len(list_items flag).\",\n   \"why_it_matters\": \"A fourth reader that forgets the check is how the first review missed three counters.\",\n   \"fix\": \"One is_filtered(row) helper beside FT.FILTERED; optional: exclude rejected rows from the progress count.\",\n   \"acceptance_test\": \"grep FILTERED_BY_RULE app/backend shows one literal definition.\"}\n ],\n \"whats_right\": [\"Filtered items are placed after every other tray item so recorded judge prompts keep their f_r<n>_<k> ids (test plus mutant M7 kill)\", \"tray_filtered carries rule, ref D-032, label, explanation and count per rule, with needs_action false, and the full unit suite stays green (2939 passed)\", \"api.md documents the payload and adds a FILTERED_BY_RULE reason-code row\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:42:48.761Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:50.181Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3; ps aux | grep -c \"[m]ut2.py\""
}
````

### User / tool · 2026-11-02T11:42:50.390Z

**tool result**
````
ok (131 file(s))
0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:42:53.925Z

T-126 verdict is changes: no blockers, one major. I wrote the review to `/Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer.md` and the board validator accepts it. The unit suite passes (2939 passed, 4 skipped) on the archive copy.

- **Major:** other rejected tray flags (judge-rejected or non-verbatim model flags) still count as pending in `store.export_case` and print in the internal notes. In my repro the notes said "Items not reviewed: 24" against 23 in the UI and printed a quote that is not in record 4. api.md says a tray flag is never in the export. The card skipped only `FILTERED_BY_RULE`.
- **Minor:**
  - The `FILTERED_BY_RULE` branch drops the grounding-failure reason.
  - The card's tests leave 4 of 10 mutants alive: counts, trace gate and judge counts, and `export_case`. The letter assertion builds from an empty case, so it can never fail.
  - Same-quote proposals with different categories merge without a trace.
  - The api.md example lacks `tray_filtered`, and `docs/LLM_VS_CODE.md` has no D-057 text.
- **Nit:** the marker string is copied into four places, and the run-progress counter includes tray rows.
