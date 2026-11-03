# Subagent: T-066 review (haiku staff) (T-066 review (haiku staff))

Source: `agent-a44ad7a2d4a4b0880.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:39:29.899Z

Review board card T-066 in /Users/arsis/zlayt-pm-project (commit e7c1912, app/backend/ingest.py plus tests/unit/test_split_llm.py). When no model or fixture is available for an unsplit paste, the pipeline must emit SPLIT_REJECTED (reason NO_MODEL) and never pass silently. Confirm the behaviour; confirm the test fails when the emission is removed in a scratch copy; confirm the fix doesn't break the commit 8bf99fb re-run consistency path. Run `python3 -m pytest -q tests/unit/test_split_llm.py`, using .venv/bin/python if needed.

Write reviews/T-066-staff-engineer.md with a ```json block containing card, persona, verdict and findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:30.931Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:39:30.940Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:31.180Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:39:31.186Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r2, T-059 r1: stale-on-failed-rerun, untracked replacement fixture, any-reason seeded tests
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — "code only" docs that call models, D-033 regex labels family speech, fixture deleted at sha, reviews append-only
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:31.820Z

**tool call — Bash**
````
{
 "command": "git show --stat e7c1912 2>&1 | head -40; echo ---; git log --oneline -8 2>&1; echo ---; ls -la .venv/bin/python 2>&1; echo ---; python3 tools/board.py show T-066 2>&1 | head -80",
 "description": "Inspect commit, git log, venv, and T-066 card"
}
````

### User / tool · 2026-11-02T02:39:31.999Z

**tool result**
````
commit e7c1912621e023082e5e8ec55a4442b5162d0c20
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:39:18 2026 -0600

    fix(backend): emit SPLIT_REJECTED (NO_MODEL) for an unsplit paste with no splitter (T-066)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/ingest.py        |  7 +++++--
 tests/unit/test_split_llm.py | 11 +++++++++++
 2 files changed, 16 insertions(+), 2 deletions(-)
---
7986d22 feat(frontend): /api/office exposes orchestrator.acted (recent dispatch/review cards + owner) for T-064
e7c1912 fix(backend): emit SPLIT_REJECTED (NO_MODEL) for an unsplit paste with no splitter (T-066)
1855b76 docs(architect): align LLM_VS_CODE and DECISIONS with code at HEAD (T-063 r1)
5900040 fix(frontend): batch accept shows an error and accepts nothing on 404/405 (T-065)
b614b40 board: sync cards, reviews, lessons, agent memory; append-only review guard; pathspec commit rule
8bf99fb fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
670ed09 test(backend): batch accept refuses needs_review and rejected entries (T-055 F1/F2)
991dac4 fix(backend): patient_report chip only on a whole-excerpt patient clause (T-061 r4, D-037)
---
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
---
---
id: "T-066"
title: "Emit SPLIT_REJECTED when no model is available for an unsplit paste"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:38:13Z"
updated_at: "2026-11-02T02:39:26Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:38:23Z"
rounds: 0
commits: ["e7c1912"]
reviews: []
ac:
  - {"n": 1, "text": "With no model/fixture available, an unsplit paste yields a SPLIT_REJECTED warning, covered by a unit test (reviews/T-063-staff-engineer.md major 2)", "done": true, "evidence": "tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model passes; tests/unit: 923 pass, 5 unrelated fail (narrative x3, t037 case_02 j1 fixture miss, e2e_contract passes alone)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:38:23Z backend: claimed
- 2026-11-02T02:39:21Z backend: AC 1 checked: tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model passes; tests/unit: 923 pass, 5 unrelated fail (narrative x3, t037 case_02 j1 fixture miss, e2e_contract passes alone)
- 2026-11-02T02:39:21Z backend: moved in_progress -> in_review
- 2026-11-02T02:39:26Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: ingest.py sets split_failure=NO_MODEL when an ambiguous single unsplit/incomplete block has no splitter, so SPLIT_REJECTED is emitted with a 'No model was available' message. Verified: 2 new tests in test_split_llm.py; full unit run 923 pass, 5 fail in files not touched (test_narrative x3, t037 case_02 j1 fixture miss, e2e_contract passes alone). Left: nothing. Surprised: system python lacks pytest, use .venv.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:35.693Z

**tool call — Bash**
````
{
 "command": "git show e7c1912 -- app/backend/ingest.py tests/unit/test_split_llm.py",
 "description": "Show full diff of commit e7c1912"
}
````

### User / tool · 2026-11-02T02:39:35.792Z

**tool result**
````
commit e7c1912621e023082e5e8ec55a4442b5162d0c20
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:39:18 2026 -0600

    fix(backend): emit SPLIT_REJECTED (NO_MODEL) for an unsplit paste with no splitter (T-066)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/ingest.py b/app/backend/ingest.py
index 14928ba..5ee0ee5 100644
--- a/app/backend/ingest.py
+++ b/app/backend/ingest.py
@@ -259,7 +259,10 @@ def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_REC
     text = check_limits(raw_text, max_chars)
     recs, method = _split(text)
     llm_split, split_failure, split_call_id = False, None, None
-    if splitter and method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"])):
+    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
+    if eligible and not splitter:
+        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
+    if splitter and eligible:
         try:
             got = splitter(text)
         except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
@@ -290,7 +293,7 @@ def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_REC
     elif method == "ambiguous":
         warns.append(_warn("SPLIT_AMBIGUOUS", "Record boundaries could not be found with confidence; check the split."))
         if split_failure:
-            warns.append(_warn("SPLIT_REJECTED", "The AI's proposed record boundaries were not used (" + split_failure + "); the paste stays one record."))
+            warns.append(_warn("SPLIT_REJECTED", ("No model was available to propose record boundaries" if split_failure == "NO_MODEL" else "The AI's proposed record boundaries were not used (" + split_failure + ")") + "; the paste stays one record."))
     if any(len(g) > 1 for g in groups):
         warns.append(_warn("DUPLICATE_MERGED", "Identical records were merged into one entry that cites all of them."))
     if any(p.search(text) for p in _PHI):
diff --git a/tests/unit/test_split_llm.py b/tests/unit/test_split_llm.py
index 2a6286d..72168a3 100644
--- a/tests/unit/test_split_llm.py
+++ b/tests/unit/test_split_llm.py
@@ -14,6 +14,17 @@ def test_code_split_finds_one_unsplit_block_without_a_splitter():
     assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and not any(w["code"] == "LLM_SPLIT" for w in r["warnings"])
 
 
+def test_no_model_for_unsplit_paste_emits_split_rejected_no_model():
+    w = {x["code"]: x for x in IN.ingest(TEXT)["warnings"]}
+    assert "SPLIT_AMBIGUOUS" in w
+    assert "SPLIT_REJECTED" in w and "No model" in w["SPLIT_REJECTED"]["message"]
+
+
+def test_confident_code_split_without_model_has_no_split_rejected():
+    codes = [x["code"] for x in IN.ingest("Date: 2026-03-03\nSource: Clinic\nExcerpt: Neck pain.")["warnings"]]
+    assert "SPLIT_REJECTED" not in codes
+
+
 def test_valid_llm_split_makes_two_records_each_flagged():
     r = IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
     assert [x["char_start"] for x in r["records"]] == [0, SECOND] and r["split_method"] == "llm"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:36.231Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_split_llm.py 2>&1 | tail -30; echo \"exit=$?\"; echo ---; python3 -m pytest -q tests/unit/test_split_llm.py 2>&1 | tail -5",
 "description": "Run split LLM unit tests with venv and system python"
}
````

### User / tool · 2026-11-02T02:39:37.171Z

**tool result**
````
...............................                                          [100%]
31 passed in 0.56s
exit=0
---
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:38.913Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/ingest.py && sed -n 1,60p app/backend/ingest.py",
 "description": "Read top of ingest.py"
}
````

### User / tool · 2026-11-02T02:39:39.002Z

**tool result**
````
     356 app/backend/ingest.py
"""Stage 0 ingest (all code): split, header date/source, kind, duplicate merge, limits, injection tag, warnings.
R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
import re

from app.backend import dates, flag_templates, injection, lexicon

MAX_CHARS = 60000
MAX_RECORDS = 40

# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")

_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
_SEP = re.compile(r"^[ \t]*---+[ \t]*$", re.MULTILINE)
_DATE_LINE = re.compile(r"^Date:", re.MULTILINE)
_F_DATE = re.compile(r"^Date:[ \t]*(.*)$", re.MULTILINE)
_F_SRC = re.compile(r"^Source:[ \t]*(.*)$", re.MULTILINE)
_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)


class IngestError(ValueError):
    """Input refused before any processing; str(e) is the API error code ('bad_request' | 'input_too_large')."""

    @property
    def code(self) -> str:
        return str(self)


def normalize_text(raw: str) -> str:
    """CRLF and CR become LF; leading and trailing whitespace trimmed (api.md POST /api/cases)."""
    return (raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
    t = normalize_text(text)
    if not t:
        raise IngestError("bad_request")
    if len(t) > max_chars:
        raise IngestError("input_too_large")
    return t


def _spans(text: str):
    """Candidate block (start, end) spans and the method that found them; None when nothing is confident."""
    heads = [m.start() for m in _HEADER.finditer(text)]
    if heads:
        return list(zip(heads, heads[1:] + [len(text)]))
    if _SEP.search(text):
        cuts = [0] + [x for m in _SEP.finditer(text) for x in (m.start(), m.end())] + [len(text)]
        return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2)]
    starts = [m.start() for m in _DATE_LINE.finditer(text)]
    if starts and (_F_SRC.search(text) or _F_EXC.search(text)):
        return list(zip(starts, starts[1:] + [len(text)]))
    return None


def _excerpt_extent(rest: str):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:39.567Z

**tool call — Bash**
````
{
 "command": "sed -n 230,320p app/backend/ingest.py | cat -n | sed 's/^ *\\([0-9]*\\)/L\\1+229/' | head -100",
 "description": "Read the ingest() function body with line numbers"
}
````

### User / tool · 2026-11-02T02:39:39.653Z

**tool result**
````
L1+229	    for r in records:
L2+229	        p = dates.parse_date(r["date_raw"])
L3+229	        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
L4+229	        if key not in groups:
L5+229	            groups[key] = []
L6+229	            order.append(key)
L7+229	        groups[key].append(r["n"])
L8+229	    return [sorted(groups[k]) for k in order]
L9+229	
L10+229	
L11+229	_PHI = [re.compile(p, re.IGNORECASE) for p in (
L12+229	    r"\b\d{3}-\d{2}-\d{4}\b",                                  # SSN
L13+229	    r"(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b",  # phone
L14+229	    r"\bMRN\s*[:#]?\s*[A-Z0-9-]{5,}")]                         # MRN
L15+229	
L16+229	
L17+229	def _warn(code: str, message: str, item_id=None) -> dict:
L18+229	    return {"code": code, "message": message, "item_id": item_id}
L19+229	
L20+229	
L21+229	def warnings(raw_text: str) -> list:
L22+229	    return ingest(raw_text)["warnings"]
L23+229	
L24+229	
L25+229	def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS, splitter=None, not_duplicates=()) -> dict:
L26+229	    """Everything stage 0 knows. Zero model calls unless `splitter(text) -> [(start, end)] | None` is given AND the code split found one
L27+229	    unsplit block (D-031); its answer is accepted only if validate_split passes, else the single record stays.
L28+229	    `not_duplicates`: record ids ('r2') the paralegal said are NOT duplicates of the record they matched; they stay separate (D-031).
L29+229	    Raises IngestError('bad_request'|'input_too_large') first."""
L30+229	    text = check_limits(raw_text, max_chars)
L31+229	    recs, method = _split(text)
L32+229	    llm_split, split_failure, split_call_id = False, None, None
L33+229	    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
L34+229	    if eligible and not splitter:
L35+229	        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
L36+229	    if splitter and eligible:
L37+229	        try:
L38+229	            got = splitter(text)
L39+229	        except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
L40+229	            got, split_failure = None, e.code
L41+229	        if got is not None:
L42+229	            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
L43+229	            try:
L44+229	                checked = validate_split(text, spans or [], max_records)
L45+229	            except ValueError as e:        # the code check refused the proposal: keep the one record, with the reason code
L46+229	                split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
L47+229	            else:
L48+229	                recs, method, llm_split = _llm_records(text, checked), "llm", True
L49+229	    if len(recs) > max_records:
L50+229	        raise IngestError("input_too_large")
L51+229	    groups = dedupe(recs)
L52+229	    if not_duplicates:
L53+229	        nd = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
L54+229	        out = []
L55+229	        for grp in groups:
L56+229	            out.append([grp[0]] + [n for n in grp[1:] if n not in nd])
L57+229	            out += [[n] for n in grp[1:] if n in nd]
L58+229	        groups = out
L59+229	        groups.sort(key=lambda g: g[0])
L60+229	    first_of = {n: g[0] for g in groups for n in g}
L61+229	    warns, to_confirm, record_warnings = [], [], []
L62+229	    if llm_split:
L63+229	        warns.append(_warn("LLM_SPLIT", "The pasted text had no recognisable record markers; the AI proposed the record boundaries and code checked them. Check the split."))
L64+229	    elif method == "ambiguous":
L65+229	        warns.append(_warn("SPLIT_AMBIGUOUS", "Record boundaries could not be found with confidence; check the split."))
L66+229	        if split_failure:
L67+229	            warns.append(_warn("SPLIT_REJECTED", ("No model was available to propose record boundaries" if split_failure == "NO_MODEL" else "The AI's proposed record boundaries were not used (" + split_failure + ")") + "; the paste stays one record."))
L68+229	    if any(len(g) > 1 for g in groups):
L69+229	        warns.append(_warn("DUPLICATE_MERGED", "Identical records were merged into one entry that cites all of them."))
L70+229	    if any(p.search(text) for p in _PHI):
L71+229	        warns.append(_warn("PHI_PATTERN", "Text looks like it contains an SSN, phone number or MRN. This tool is for synthetic data only."))
L72+229	    for r in recs:
L73+229	        p = dates.parse_date(r["date_raw"])
L74+229	        kind = record_kind(r["source"], r["excerpt"])
L75+229	        hits = [{**h, "field": "excerpt"} for h in injection.scan(r["excerpt"])] + \
L76+229	               [{**h, "field": "source"} for h in injection.scan(r["source"])]
L77+229	        rid = f"r{r['n']}"
L78+229	        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
L79+229	                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
L80+229	                 injection_tag=bool(hits), injection_hits=hits)
L81+229	        if llm_split:
L82+229	            line = r["excerpt"].split("\n", 1)[0][:160]
L83+229	            at = r["text"].find(line)
L84+229	            record_warnings.append({"type": "record_warning", "category": "llm_split", "record_no": r["n"], "call_id": split_call_id,
L85+229	                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
L86+229	                                                  "end": r["char_start"] + at + len(line) if at >= 0 else None}]})
L87+229	        if r["unsplit"]:
L88+229	            warns.append(_warn("UNSPLIT_TEXT", "Text outside any recognised record was kept as its own record; check it and add separators if it belongs to one.", rid))
L89+229	        if p["status"] != "parsed":
L90+229	            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
L91+229	            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:41.281Z

**tool call — Bash**
````
{
 "command": "sed -n 60,230p app/backend/ingest.py",
 "description": "Read middle of ingest.py (split, validate_split, SplitFailed)"
}
````

### User / tool · 2026-11-02T02:39:41.369Z

**tool result**
````
def _excerpt_extent(rest: str):
    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
    if rest.startswith('"'):
        i = 0
        while True:
            j = rest.find("\n", i)
            seg = rest[i:len(rest) if j < 0 else j].rstrip()
            if seg.endswith('"') and i + len(seg) > 1:
                return rest[1:i + len(seg) - 1], i + len(seg)
            if j < 0:
                break
            i = j + 1
    return rest.strip(), len(rest.rstrip())


def _scan_block(text: str, a: int, b: int):
    """Parse one block. Returns (fields | None, covered spans). Covered spans are absolute; whatever lies outside them is leftover."""
    block = text[a:b]
    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
    h = _HEADER.match(block)
    if h:
        cov.append((a, a + h.end()))
    found = 0
    for key, pat in (("date_raw", _F_DATE), ("source", _F_SRC)):
        m = pat.search(block)
        if m:
            f[key] = m.group(1).strip()
            cov.append((a + m.start(), a + m.end()))
            found += 1
    e = _F_EXC.search(block)
    if e:
        exc, used = _excerpt_extent(block[e.end():])
        f["excerpt"] = exc
        cov.append((a + e.start(), a + e.end() + used))
        found += 1
    f["complete"] = found == 3
    return (f if found else None), cov


def _leftovers(text: str, cov: list):
    """Non-blank segments of `text` not inside any covered span, as (start, end); an exact golden banner line (BANNERS) on line 1 is exempt."""
    out, pos = [], 0
    for s, e in sorted(cov) + [(len(text), len(text))]:
        if s > pos:
            seg = text[pos:s]
            if seg.strip():
                lead = len(seg) - len(seg.lstrip())
                out.append((pos + lead, pos + len(seg.rstrip())))
        pos = max(pos, e)
    return [(s, e) for s, e in out if not (s == 0 and text[s:e] in BANNERS)]


def _split(text: str):
    """(records, method). Every non-blank character of the input ends up inside some record; text outside a recognised block becomes
    an `unsplit` record (D-027) and the split is reported ambiguous."""
    spans = _spans(text)
    if not spans:
        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
    items, method = [], "code"
    cov_all = [] if _HEADER.search(text) else [(m.start(), m.end()) for m in _SEP.finditer(text)]   # separator lines carry no content
    for a, b in spans:
        f, cov = _scan_block(text, a, b)
        cov_all += cov
        if f is None:
            continue
        if not f["complete"]:
            method = "ambiguous"
        end = max(e for _, e in cov)
        items.append((a, end, f))
    for s, e in _leftovers(text, cov_all):
        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
        method = "ambiguous"
    items.sort(key=lambda t: t[0])
    return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method


def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}


class SplitFailed(Exception):
    """The model could not give a split (call failed, no recorded answer, unusable output). `code` is a reason code; never model text."""
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def validate_split(text: str, spans, max_records: int = None) -> list:
    """Code check on the model's record boundaries (D-031). `spans` = [(start, end)]. Valid only if they cover `text` exactly
    (first start 0, each end == next start, last end == len(text)), every start falls on a line start, and there are at least two.
    Returns the list of (start, end) or raises ValueError; the caller then keeps the single unsplit record."""
    sp = [(int(a), int(b)) for a, b in spans]
    if max_records is not None and len(sp) > max_records:
        raise ValueError("SPLIT_TOO_MANY")
    if len(sp) < 2 or sp[0][0] != 0 or sp[-1][1] != len(text):
        raise ValueError("SPLIT_NOT_COVERING")
    for i, (a, b) in enumerate(sp):
        if not a < b or (i and a != sp[i - 1][1]):
            raise ValueError("SPLIT_NOT_CONTIGUOUS")
        if a and text[a - 1] != "\n":
            raise ValueError("SPLIT_NOT_ON_LINE_START")
        if not text[a:b].strip():
            raise ValueError("SPLIT_EMPTY_RECORD")
    return sp


def numbered(text: str) -> str:
    """The text with an '@OFFSET| ' label on every line, so the model can name boundaries without counting characters."""
    out, pos = [], 0
    for line in text.split("\n"):
        out.append(f"@{pos}| {line}")
        pos += len(line) + 1
    return "\n".join(out)


def _llm_records(text: str, spans: list) -> list:
    """Records from validated spans. Fields come from code only (labelled lines, or a first line that parses as a date)."""
    out = []
    for a, b in spans:
        s0 = a + (len(text[a:b]) - len(text[a:b].lstrip()))
        first_line = text[s0:b].split("\n", 1)[0].rstrip()
        if s0 == 0 and first_line in BANNERS:       # the golden banner line belongs to no record
            s0 += len(first_line)
            s0 += len(text[s0:b]) - len(text[s0:b].lstrip())
        e0 = a + len(text[a:b].rstrip())
        if s0 >= e0:
            continue
        f, _cov = _scan_block(text, s0, e0)
        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
        if not f["excerpt"]:
            f["excerpt"] = text[s0:e0].strip()
        if not f["date_raw"]:
            first = text[s0:e0].split("\n", 1)[0].strip()
            left, _, right = re.split(r"(\s+[\u2014\u2013|-]\s+)", first, maxsplit=1)[:3] if re.search(r"\s+[\u2014\u2013|-]\s+", first) else (first, "", "")
            if dates.parse_date(left.strip())["status"] == "parsed":     # 'May 4, 2026 - Pottsworth Emergency Department' or a bare date line
                f["date_raw"] = left.strip()
                if right.strip() and not f["source"]:
                    f["source"] = right.strip()
                    f["excerpt"] = text[s0:e0].split("\n", 1)[1].strip() if "\n" in text[s0:e0] else f["excerpt"]
        out.append(_record(len(out) + 1, text[s0:e0], s0, e0, f))
    return out


def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
    text = check_limits(raw_text, max_chars)
    recs, _ = _split(text)
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    return recs


def record_kind(source: str, excerpt: str = "") -> str:
    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
    if not (source or "").strip():
        return "unsplit_text"
    for e in lexicon.code_list("non_encounter"):
        if e["regex"].search(source or ""):
            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
    return "encounter"


def _norm(s: str) -> str:
    return " ".join((s or "").split()).casefold()


def dedupe(records: list) -> list:
    """Groups of record numbers (in file order): same date + same normalised provider label + same normalised text merge (R-TL-7)."""
    groups, order = {}, []
    for r in records:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:42.145Z

**tool call — Bash**
````
{
 "command": "sed -n 320,356p app/backend/ingest.py; echo ----; git show 8bf99fb --stat; echo ----; grep -rn \"split_failure\\|NO_MODEL\\|SPLIT_REJECTED\\|splitter\" app/ tests/ evals/ --include=*.py | grep -v \"^app/backend/ingest.py:2[5-9][0-9]\\|^app/backend/ingest.py:3[0-2][0-9]\"",
 "description": "Read rest of ingest.py and grep callers of splitter and NO_MODEL"
}
````

### User / tool · 2026-11-02T02:39:42.261Z

**tool result**
````
            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
            record_warnings.append({"type": "record_warning", "category": "date_ambiguous", "record_no": r["n"],
                                    "evidence": [{"field": "date", "text": r["date_raw"]}]})
        if hits:   # one flag per tagged record; evidence = every matched phrase (offsets into the excerpt)
            record_warnings.append({"type": "record_warning", "category": "injection_suspected", "record_no": r["n"],
                                    "evidence": [{"field": h["field"], "text": h["phrase"], "start": h["start"], "end": h["end"]} for h in hits]})
    by_n = {r["n"]: r for r in recs}
    for w in record_warnings:       # title/explanation come from flag_templates only (R-FL-8)
        r = by_n[w["record_no"]]
        ev = w["evidence"][0]["text"]
        w["id"] = f"f_{ {'injection_suspected': 'inj', 'llm_split': 'split'}.get(w['category'], 'date') }_r{r['n']}"
        w["title"], w["explanation"] = flag_templates.render("record_warning", w["category"], provider=r["source"] or None,
                                                             date=r["date_iso"], quote=ev if w["category"] == "injection_suspected" else None,
                                                             raw=r["date_raw"] if w["category"] == "date_ambiguous" else None)
        w["reasons"] = {"injection_suspected": ["INJECTION_SUSPECTED"], "llm_split": ["LLM_SPLIT"]}.get(w["category"], [])
    first = text.split("\n", 1)[0].rstrip()
    return {"banner": first if first in BANNERS else None, "records": recs, "groups": groups, "split_method": method if method in ("code", "llm") else "ambiguous", "split_failure": split_failure, "warnings": warns,
            "dates_to_confirm": to_confirm, "record_warnings": record_warnings,
            "injection_records": [r["id"] for r in recs if r["injection_tag"]]}


def evidence_span(rec: dict, field: str, needle: str = None) -> dict:
    """Evidence item for a record: field 'date' | 'source' (the header line) or 'excerpt' (`needle`, a verbatim substring of the record).
    Offsets are absolute in the normalised input when the record carries `text` and `char_start`; otherwise they are None."""
    text, base = rec.get("text"), rec.get("char_start")
    out = {"record_no": rec["n"], "field": field, "text": needle, "start": None, "end": None}
    if field in ("date", "source"):
        pat = _F_DATE if field == "date" else _F_SRC
        m = pat.search(text) if text else None
        out["text"] = m.group(0) if m else (rec.get("date_iso") if field == "date" else rec.get("source"))
        if m and base is not None:
            out["start"], out["end"] = base + m.start(), base + m.end()
    elif text and base is not None and needle:
        i = text.find(needle)
        if i >= 0:
            out["start"], out["end"] = base + i, base + i + len(needle)
    return out
----
commit 8bf99fb5ff76026aaac7d30b7288b901a4e0f725
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:37:20 2026 -0600

    fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
    
    Stored records now follow the run's records on every run (delete + re-store in one transaction when ids/spans differ);
    ingest narrows the except to validate_split only.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/ingest.py        | 14 +++++++++-----
 app/backend/pipeline.py      | 31 +++++++++++++++++++------------
 tests/unit/test_split_llm.py | 42 ++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 70 insertions(+), 17 deletions(-)
----
app/backend/ingest.py:2:R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
app/backend/ingest.py:336:    return {"banner": first if first in BANNERS else None, "records": recs, "groups": groups, "split_method": method if method in ("code", "llm") else "ambiguous", "split_failure": split_failure, "warnings": warns,
app/backend/sentences.py:1:"""Sentence units (R-TL-2, D-012/D-021, ADR-016). One splitter shared by the excerpt check, flag evidence and the edit UI.
app/backend/split_llm.py:13:def make_splitter(call):
app/backend/pipeline.py:51:    ing = IN.ingest(raw_text, splitter=split_llm.make_splitter(call) if call else None, not_duplicates=not_duplicates)
app/backend/pipeline.py:95:    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "banner": ing["banner"],
app/backend/pipeline.py:242:    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
app/backend/pipeline.py:243:        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
tests/unit/test_sentences.py:1:"""Sentence units. R-TL-2 (D-012/D-021 splitter), LLM_VS_CODE row 4 rung 1."""
tests/unit/test_sentences.py:31:    ("Rx cyclobenzaprine 10 mg. Follow up in 1 week.", "Rx cyclobenzaprine 10 mg."),   # 'mg.' before a capitalised sentence IS a terminator (backend splitter; REQ R-TL-2 abbreviation list to be corrected)
tests/unit/test_split_llm.py:12:def test_code_split_finds_one_unsplit_block_without_a_splitter():
tests/unit/test_split_llm.py:20:    assert "SPLIT_REJECTED" in w and "No model" in w["SPLIT_REJECTED"]["message"]
tests/unit/test_split_llm.py:25:    assert "SPLIT_REJECTED" not in codes
tests/unit/test_split_llm.py:29:    r = IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
tests/unit/test_split_llm.py:49:    r = IN.ingest(TEXT, splitter=lambda t: bad)
tests/unit/test_split_llm.py:55:def test_splitter_failure_keeps_one_record_with_a_reason():
tests/unit/test_split_llm.py:58:    r = IN.ingest(TEXT, splitter=boom)
tests/unit/test_split_llm.py:59:    assert len(r["records"]) == 1 and r["split_failure"] == "LLM_FAILED_AFTER_RETRIES" and r["split_method"] == "ambiguous"
tests/unit/test_split_llm.py:60:    assert any(w["code"] == "SPLIT_AMBIGUOUS" for w in r["warnings"]) and any(w["code"] == "SPLIT_REJECTED" for w in r["warnings"])
tests/unit/test_split_llm.py:63:def test_unexpected_splitter_errors_propagate():
tests/unit/test_split_llm.py:67:        IN.ingest(TEXT, splitter=boom)
tests/unit/test_split_llm.py:70:def test_splitter_not_called_when_code_split_is_confident():
tests/unit/test_split_llm.py:73:    r = IN.ingest(G.raw("sample"), splitter=lambda t: called.append(1))
tests/unit/test_split_llm.py:82:def test_make_splitter_sends_numbered_nonce_wrapped_text_and_returns_spans():
tests/unit/test_split_llm.py:87:    spans = split_llm.make_splitter(call)(T)
tests/unit/test_split_llm.py:158:    assert len(IN.ingest(T3, splitter=lambda t: spans)["records"]) == 1
tests/unit/test_split_llm.py:166:    r = IN.ingest(t, splitter=lambda x: spans)
tests/unit/test_split_llm.py:167:    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and r["split_failure"] == "SPLIT_TOO_MANY"
tests/unit/test_split_llm.py:171:    r = IN.ingest(TEXT, splitter=lambda t: ([(0, SECOND), (SECOND, len(t))], "c42"))
tests/unit/test_split_llm.py:183:    r = IN.ingest(raw, splitter=lambda x: [(0, i), (i, len(x))])
tests/unit/test_split_llm.py:263:        IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:51.933Z

**tool call — Bash**
````
{
 "command": "sed -n 1,130p app/backend/pipeline.py",
 "description": "Read pipeline.py top section with split wiring"
}
````

### User / tool · 2026-11-02T02:39:52.016Z

**tool result**
````
"""Pipeline stages 0-7 (app/README-arch.md; ADR-007, ADR-010, ADR-011, ADR-013, ADR-014). `python -m app.pipeline <file>` prints the result.

0 ingest (code, sync)  1 extract (LLM)  2 verify (code)  3 judge_entries (J1)  4 amounts (J2 on every amount)
5 conflicts (one LLM pair pass + J3)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
No code path here sets review_status: every item leaves a run `pending`. A model failure loses only that item and is reported in `errors`.
`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is the audited wrapper bound to a case (or a test fake)."""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
                         judges, split_llm, totals as TT, why as WHY)
from app.db import db as DB
from app.llm import audited as AU, provider as P

STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
DEADLINE_S = 480
CONCURRENCY = 3
_ORIGIN = {"both": "lexicon+llm"}


def _clean(d: dict) -> dict:
    """Drop private '_' keys before an item is stored or returned."""
    return {k: v for k, v in d.items() if not k.startswith("_")}


def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
            "human": {"action": None, "edited_text": None, "at": None}, "state": state}


def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons}
    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
        ctx["date_status"] = "ambiguous"
    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
                                     "code_reasons": []}, ctx)


# ------------------------------------------------------------------ stage 0
def run_ingest(raw_text: str, call=None, not_duplicates=()) -> dict:
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    ing = IN.ingest(raw_text, splitter=split_llm.make_splitter(call) if call else None, not_duplicates=not_duplicates)
    text = IN.normalize_text(raw_text)
    recs = ing["records"]
    by_n = {r["n"]: r for r in recs}
    backend = P.backend_name()
    flags = []
    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
    for f in code:
        nos = f["record_nos"]
        ev = f["evidence"]
        reasons = list(f.get("reasons") or [])
        state, why_codes = _compose_code(by_n, nos, reasons, ev, text)
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
                "Computed by code from the record dates and text; every cited span matches the input."}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = _ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        flags.append(item)
    for w in ing["record_warnings"]:
        r = by_n[w["record_no"]]
        inj = w["category"] == "injection_suspected"
        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
                      "explanation": w["explanation"], "evidence": [{"record_no": w["record_no"], **e} for e in w["evidence"]],
                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
                      "ladder": _ladder(w["id"], backend, {"computed_by": "code"}, state)})
        if w["category"] == "llm_split":      # trace the flag to the audited split call (prompt version, model, call id)
            flags[-1]["ladder"]["generator"] = {"model": judges.generator_model(), "prompt_version": "split_v1", "call_id": w.get("call_id")}
    amounts, damages = [], []
    sep = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
    for a in AM.extract_amounts(recs, separate=sep):
        item = amount_item(a, by_n[a["record_no"]])
        (damages if a["cls"] == "damages" else amounts).append(item)
    warnings = list(ing["warnings"])
    for r in recs:
        if r["injection_tag"]:
            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
                             "message": "This record contains instruction-like text; it is shown unchanged and everything from it needs review."})
    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "banner": ing["banner"],
            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
            "injection_records": ing["injection_records"]}


def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
    """The pipeline's amount item from an amounts.extract_amounts row and its record."""
    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
            "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}


def _not_duplicates(conn, cid: str) -> list:
    return list(((DB.get_case(conn, cid) or {}).get("config") or {}).get("not_duplicates", []))


def _store_records(conn, cid: str, ing: dict) -> None:
    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
        return
    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
    try:
        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
        for r in ing["records"]:
            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
                          encounter=int(r["encounter"]))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:52.477Z

**tool call — Bash**
````
{
 "command": "sed -n 215,275p app/backend/pipeline.py; echo ----SPLIT_LLM; cat -n app/backend/split_llm.py | head -80",
 "description": "Read pipeline errors section and split_llm module"
}
````

### User / tool · 2026-11-02T02:39:52.562Z

**tool result**
````
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso") and r["kind"] == "encounter")
    return int(ds[0][:4]) if ds else None


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = call or AU.make_call(conn, cid, now=clock)
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid))
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing)
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
    status = "done"
    timed_out = False

    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            errors.append(_err("LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"], "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
----SPLIT_LLM
     1	"""LLM split fallback (D-031): ask the model for record-boundary character offsets when the code split found one unsplit block.
     2	
     3	The model only points: it returns {records: [{start, end}]}. ingest.validate_split then checks by code that the spans cover the
     4	text exactly and start on line starts; anything else keeps the single record. Every record made this way carries the
     5	record_warning LLM_SPLIT (ingest.ingest). Fields (date, source, excerpt) never come from the model.
     6	"""
     7	from pydantic import ValidationError
     8	
     9	from app.backend import ingest, injection, schemas
    10	from app.llm import audited as AU, promptlib, provider as P
    11	
    12	
    13	def make_splitter(call):
    14	    """call(step, system, user, schema, *, item_id=None) -> (output, call_id): the audited wrapper bound to the case."""
    15	    def split(text: str):
    16	        prompt = promptlib.load("split_v1")
    17	        nonce = promptlib.nonce(text, "split", "all")
    18	        user = injection.wrap(ingest.numbered(text), nonce) + f"\nTOTAL: {len(text)}\nReturn the JSON object."
    19	        try:
    20	            out, call_id = call("split", prompt.text, user, schemas.SplitOutput.model_json_schema(), item_id="split")
    21	        except P.FixtureMiss:
    22	            raise ingest.SplitFailed("FIXTURE_MISS") from None
    23	        except AU.LLMFailed:
    24	            raise ingest.SplitFailed("LLM_FAILED_AFTER_RETRIES") from None
    25	        try:
    26	            spans = [(s.start, s.end) for s in schemas.SplitOutput.model_validate(out).records]
    27	        except (ValidationError, TypeError, ValueError):
    28	            raise ingest.SplitFailed("SCHEMA_INVALID") from None
    29	        return spans, call_id
    30	    return split
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:58.956Z

**tool call — Bash**
````
{
 "command": "cat -n tests/unit/test_split_llm.py",
 "description": "Read full split LLM unit test file"
}
````

### User / tool · 2026-11-02T02:39:59.031Z

**tool result**
````
     1	"""D-031 LLM split fallback (T-057): code validates the model's boundaries; LLM_SPLIT on every LLM-split record; failure keeps one record."""
     2	import pytest
     3	from app.backend import ingest as IN, split_llm, pipeline as PL
     4	from app.backend import flag_templates as FT
     5	
     6	TEXT = ("March 3, 2026\nDr. Rowan Pell, orthopedics. Right wrist swelling after a fall. X-ray shows a distal radius fracture.\n\n"
     7	        "March 17, 2026\nDr. Rowan Pell, orthopedics. Splint removed. Pain 2/10.\n")
     8	T = IN.normalize_text(TEXT)
     9	SECOND = T.index("March 17")
    10	
    11	
    12	def test_code_split_finds_one_unsplit_block_without_a_splitter():
    13	    r = IN.ingest(TEXT)
    14	    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and not any(w["code"] == "LLM_SPLIT" for w in r["warnings"])
    15	
    16	
    17	def test_no_model_for_unsplit_paste_emits_split_rejected_no_model():
    18	    w = {x["code"]: x for x in IN.ingest(TEXT)["warnings"]}
    19	    assert "SPLIT_AMBIGUOUS" in w
    20	    assert "SPLIT_REJECTED" in w and "No model" in w["SPLIT_REJECTED"]["message"]
    21	
    22	
    23	def test_confident_code_split_without_model_has_no_split_rejected():
    24	    codes = [x["code"] for x in IN.ingest("Date: 2026-03-03\nSource: Clinic\nExcerpt: Neck pain.")["warnings"]]
    25	    assert "SPLIT_REJECTED" not in codes
    26	
    27	
    28	def test_valid_llm_split_makes_two_records_each_flagged():
    29	    r = IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
    30	    assert [x["char_start"] for x in r["records"]] == [0, SECOND] and r["split_method"] == "llm"
    31	    assert r["records"][0]["date_raw"] == "March 3, 2026" and r["records"][1]["date_iso"] == "2026-03-17"
    32	    assert [w["category"] for w in r["record_warnings"]] == ["llm_split", "llm_split"]
    33	    assert all(w["reasons"] == ["LLM_SPLIT"] and w["title"] for w in r["record_warnings"])
    34	    assert any(w["code"] == "LLM_SPLIT" for w in r["warnings"])
    35	    for x in r["records"]:                      # every record text is a verbatim slice of the input
    36	        assert T[x["char_start"]:x["char_end"]] == x["text"]
    37	
    38	
    39	@pytest.mark.parametrize("bad", [
    40	    [(0, SECOND + 3), (SECOND + 3, None)],            # not on a line start
    41	    [(0, SECOND), (SECOND, 5)],                        # does not reach the end
    42	    [(1, SECOND), (SECOND, 10 ** 6)],                  # does not start at 0 / overruns
    43	    [(0, SECOND), (SECOND + 1, len(T))],               # gap
    44	    [(0, len(T))],                                     # one span: nothing to split
    45	    [(0, SECOND), (SECOND - 5, len(T))],               # overlap
    46	])
    47	def test_invalid_boundaries_keep_one_record(bad):
    48	    bad = [(a, len(T) if b is None else b) for a, b in bad]
    49	    r = IN.ingest(TEXT, splitter=lambda t: bad)
    50	    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and not any(w["category"] == "llm_split" for w in r["record_warnings"])
    51	    with pytest.raises(ValueError):
    52	        IN.validate_split(T, bad)
    53	
    54	
    55	def test_splitter_failure_keeps_one_record_with_a_reason():
    56	    def boom(t):
    57	        raise IN.SplitFailed("LLM_FAILED_AFTER_RETRIES")
    58	    r = IN.ingest(TEXT, splitter=boom)
    59	    assert len(r["records"]) == 1 and r["split_failure"] == "LLM_FAILED_AFTER_RETRIES" and r["split_method"] == "ambiguous"
    60	    assert any(w["code"] == "SPLIT_AMBIGUOUS" for w in r["warnings"]) and any(w["code"] == "SPLIT_REJECTED" for w in r["warnings"])
    61	
    62	
    63	def test_unexpected_splitter_errors_propagate():
    64	    def boom(t):
    65	        raise RuntimeError("down")
    66	    with pytest.raises(RuntimeError):
    67	        IN.ingest(TEXT, splitter=boom)
    68	
    69	
    70	def test_splitter_not_called_when_code_split_is_confident():
    71	    from tests.unit import _golden as G
    72	    called = []
    73	    r = IN.ingest(G.raw("sample"), splitter=lambda t: called.append(1))
    74	    assert not called and r["split_method"] == "code" and len(r["records"]) == 9
    75	
    76	
    77	def test_numbered_labels_every_line_with_its_offset():
    78	    n = IN.numbered(T)
    79	    assert f"@{SECOND}| March 17, 2026" in n and n.startswith("@0| March 3, 2026")
    80	
    81	
    82	def test_make_splitter_sends_numbered_nonce_wrapped_text_and_returns_spans():
    83	    seen = {}
    84	    def call(step, system, user, schema, *, item_id=None):
    85	        seen.update(step=step, user=user, schema=schema, item_id=item_id)
    86	        return {"records": [{"start": 0, "end": SECOND}, {"start": SECOND, "end": len(T)}]}, "c1"
    87	    spans = split_llm.make_splitter(call)(T)
    88	    assert spans == ([(0, SECOND), (SECOND, len(T))], "c1") and seen["step"] == "split"
    89	    assert f"@{SECOND}|" in seen["user"] and "<record-" in seen["user"] and f"TOTAL: {len(T)}" in seen["user"]
    90	
    91	
    92	def test_template_renders_for_llm_split():
    93	    title, expl = FT.render("record_warning", "llm_split")
    94	    assert "AI" in title and "AI" in expl
    95	
    96	
    97	# ---- recorded fixture replay (python -m app.llm.record evals/golden/unsplit_paste.txt, LLM_FIXTURE_DIR=tests/fixtures/llm/split)
    98	import json, os, pathlib
    99	ROOT = pathlib.Path(__file__).resolve().parents[2]
   100	EXP = json.loads((ROOT / "evals" / "golden" / "unsplit_paste.split.json").read_text())
   101	
   102	
   103	@pytest.fixture
   104	def replay(monkeypatch, tmp_path):
   105	    monkeypatch.setenv("LLM_BACKEND", "fixture")
   106	    monkeypatch.setenv("LLM_FIXTURE_DIR", str(ROOT / "tests" / "fixtures" / "llm" / "split"))
   107	    from app.db import db as DB
   108	    from app.llm import audited as AU
   109	    raw = (ROOT / "evals" / "golden" / EXP["input_file"]).read_text()
   110	    conn = DB.connect(str(tmp_path / "s.sqlite"))
   111	    cid = DB.create_case(conn, raw, now=1.0)
   112	    return conn, cid, raw, AU.make_call(conn, cid)
   113	
   114	
   115	def test_golden_unsplit_paste_code_split_is_one_block():
   116	    raw = (ROOT / "evals" / "golden" / EXP["input_file"]).read_text()
   117	    r = IN.ingest(raw)
   118	    assert len(r["records"]) == EXP["code_split"]["record_count"] and r["split_method"] == EXP["code_split"]["split_method"]
   119	
   120	
   121	def test_golden_unsplit_paste_replays_recorded_split_through_audited(replay):
   122	    from app.db import db as DB
   123	    conn, cid, raw, call = replay
   124	    ing = PL.run_ingest(raw, call=call)
   125	    assert ing["split_method"] == EXP["llm_split"]["split_method"]
   126	    got = [(r["n"], r["date_iso"], r["source"], r["text"].startswith(e["starts_with"])) for r, e in zip(ing["records"], EXP["records"])]
   127	    assert got == [(e["record_no"], e["date"], e["source"], True) for e in EXP["records"]] and len(ing["records"]) == len(EXP["records"])
   128	    warns = [f for f in ing["flags"] if f["type"] == "record_warning" and f["category"] == EXP["llm_split"]["record_warning_category"]]
   129	    assert sorted(f["record_nos"][0] for f in warns) == [1, 2, 3] and all(f["reasons"] == ["LLM_SPLIT"] and f["state"] == "needs_review" for f in warns)
   130	    assert any(w["code"] == "LLM_SPLIT" for w in ing["warnings"])
   131	    rows = [c for c in DB.list_llm_calls(conn, cid) if c["step"] == "split"]          # the ladder record: one audited row, parsed
   132	    assert len(rows) == 1 and rows[0]["parsed_ok"] == 1 and rows[0]["role"] == "generator"
   133	
   134	
   135	def test_run_pipeline_replaces_the_single_stored_record(replay):
   136	    """The case is created with the one unsplit record (code only); the run replaces it with the three LLM-split records."""
   137	    from app.db import db as DB
   138	    conn, cid, raw, call = replay
   139	    PL.ingest_case(conn, cid, raw, 1.0)
   140	    assert DB.table_counts(conn, cid)["records"] == 1
   141	    PL.run_pipeline(conn, cid, raw, call=call, now=2.0)         # the other steps have no fixtures: they fail visibly, the split does not
   142	    assert DB.table_counts(conn, cid)["records"] == 3
   143	
   144	
   145	# ---- T-057 r1: each AC1 clause pinned on its own (line starts are valid in these, only the named defect is present)
   146	T3 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
   147	L2, L3 = T3.index("May 11"), T3.index("May 25")
   148	
   149	
   150	@pytest.mark.parametrize("spans,code", [
   151	    ([(0, L2), (L2, L3)], "SPLIT_NOT_COVERING"),                 # all starts on line starts, but the last record's text is dropped
   152	    ([(0, L2), (L3, len(T3))], "SPLIT_NOT_CONTIGUOUS"),          # all starts on line starts, but the middle text is dropped
   153	    ([(0, L3), (L2, len(T3))], "SPLIT_NOT_CONTIGUOUS"),          # overlap on line starts
   154	])
   155	def test_coverage_and_contiguity_are_checked_independently_of_line_starts(spans, code):
   156	    with pytest.raises(ValueError, match=code):
   157	        IN.validate_split(T3, spans)
   158	    assert len(IN.ingest(T3, splitter=lambda t: spans)["records"]) == 1
   159	
   160	
   161	def test_too_many_records_falls_back_to_one_record_not_input_too_large():
   162	    lines = "".join(f"May {1 + i % 28}, 2026\nNote {i}.\n" for i in range(45))
   163	    t = IN.normalize_text(lines)
   164	    starts = [0] + [t.index(f"Note {i}.") - len(f"May {1 + i % 28}, 2026\n") for i in range(1, 45)]
   165	    spans = list(zip(starts, starts[1:] + [len(t)]))
   166	    r = IN.ingest(t, splitter=lambda x: spans)
   167	    assert len(r["records"]) == 1 and r["split_method"] == "ambiguous" and r["split_failure"] == "SPLIT_TOO_MANY"
   168	
   169	
   170	def test_llm_split_flag_span_is_absolute_and_carries_the_call_id():
   171	    r = IN.ingest(TEXT, splitter=lambda t: ([(0, SECOND), (SECOND, len(t))], "c42"))
   172	    for w in r["record_warnings"]:
   173	        ev, rec = w["evidence"][0], next(x for x in r["records"] if x["n"] == w["record_no"])
   174	        assert T[ev["start"]:ev["end"]] == ev["text"] and rec["char_start"] <= ev["start"] and ev["end"] <= rec["char_end"]
   175	        assert w["call_id"] == "c42"
   176	
   177	
   178	def test_banner_is_in_no_record_prompt_and_code_agree():
   179	    from tests.unit import _golden as G
   180	    raw = (ROOT / "evals" / "golden" / "unsplit_paste.txt").read_text()
   181	    t = IN.normalize_text(raw)
   182	    i = t.index("May 11, 2026")
   183	    r = IN.ingest(raw, splitter=lambda x: [(0, i), (i, len(x))])
   184	    assert r["records"][0]["char_start"] == t.index("May 4, 2026") and "SYNTHETIC" not in r["records"][0]["text"]
   185	    from app.llm import promptlib
   186	    assert "leaves a leading banner line out" in promptlib.load("split_v1").text
   187	
   188	
   189	def _extract(u):
   190	    import re
   191	    body = re.search(r"RECORD TEXT:\n<record-\w+>\n(.*?)\n</record-", u, re.S).group(1)
   192	    s = body.split(". ")[0].rstrip(".") + "."
   193	    return dict(summary=s, excerpt=s)
   194	
   195	
   196	def _stub_call(spans_by_run):
   197	    """Fake audited call: extract returns the record's first sentence; the split step returns the next scripted boundary list."""
   198	    from tests.unit._fakes import FakeCall, sample_script
   199	    runs = iter(spans_by_run)
   200	    extract = _extract
   201	    return FakeCall(sample_script(extract=extract, split=lambda u: {"records": [{"start": a, "end": b} for a, b in next(runs)]}))
   202	
   203	
   204	def test_rerun_with_different_boundaries_replaces_the_stored_records(tmp_path):
   205	    """T-057 r1 blocker: same record count, different spans -> the records table follows the latest accepted split."""
   206	    from app.db import db as DB
   207	    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
   208	    a2, a3 = T4.index("May 11"), T4.index("May 25")
   209	    b2 = T4.index("Dr. A, ortho. Pain")                                         # a different, still line-start-valid, boundary
   210	    A = [(0, a2), (a2, a3), (a3, len(T4))]
   211	    B = [(0, b2), (b2, a3), (a3, len(T4))]
   212	    call = _stub_call([A, B])
   213	    conn = DB.connect(str(tmp_path / "s.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
   214	    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
   215	    starts = lambda: [r[0] for r in conn.execute("SELECT char_start FROM records WHERE case_id=? ORDER BY seq", (cid,))]
   216	    assert starts() == [a for a, _ in A]
   217	    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
   218	    assert starts() == [a for a, _ in B] and starts() != [a for a, _ in A]
   219	    for e in DB.list_items(conn, cid, "entry"):
   220	        rec = next(r for r in conn.execute("SELECT char_start, char_end FROM records WHERE case_id=? AND id=?", (cid, e["record_ids"][0])))
   221	        assert e["excerpt"] in T4[rec[0]:rec[1]]
   222	
   223	
   224	@pytest.mark.parametrize("second", ["call_fails", "invalid_spans"])
   225	def test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent(tmp_path, second):
   226	    """T-057 r2 blocker (probe_rerun_fail2): run 1 model-split into 3 records; run 2's split fails / is rejected -> one record. Stored
   227	    records must equal run 2's records and every entry excerpt must be a substring of its own stored record."""
   228	    from app.db import db as DB
   229	    from app.llm import audited as AU
   230	    from tests.unit._fakes import FakeCall, sample_script
   231	    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
   232	    a2, a3 = T4.index("May 11"), T4.index("May 25")
   233	    A = [(0, a2), (a2, a3), (a3, len(T4))]
   234	    runs = iter([A, second])
   235	
   236	    def split(u):
   237	        v = next(runs)
   238	        if v == "call_fails":
   239	            raise AU.LLMFailed("down")
   240	        if v == "invalid_spans":
   241	            return {"records": [{"start": 0, "end": 10}, {"start": 10, "end": 20}]}      # does not cover the text
   242	        return {"records": [{"start": a, "end": b} for a, b in v]}
   243	    call = FakeCall(sample_script(extract=_extract, split=split))
   244	    conn = DB.connect(str(tmp_path / "c.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
   245	    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
   246	    assert DB.table_counts(conn, cid)["records"] == 3
   247	    out = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
   248	    stored = [tuple(r) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
   249	    assert stored == [(r["id"], r["char_start"], r["char_end"]) for r in out["records"]] and len(stored) == 1
   250	    spans = {r[0]: (r[1], r[2]) for r in stored}
   251	    entries = DB.list_items(conn, cid, "entry")
   252	    assert entries
   253	    for e in entries:
   254	        a, b = spans[e["record_ids"][0]]
   255	        assert e["excerpt"] in T4[a:b], e["id"]
   256	
   257	
   258	def test_value_error_outside_validate_split_is_not_reported_as_a_rejected_split(monkeypatch):
   259	    def boom(text, spans):
   260	        raise ValueError("programming error")
   261	    monkeypatch.setattr(IN, "_llm_records", boom)
   262	    with pytest.raises(ValueError, match="programming error"):
   263	        IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
   264	
   265	
   266	def test_split_call_failure_reaches_the_run_errors_and_is_audited_with_prompt_version(tmp_path):
   267	    from app.db import db as DB
   268	    from app.llm import audited as AU
   269	    from tests.unit._fakes import FakeCall, sample_script
   270	    conn = DB.connect(str(tmp_path / "f.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
   271	    out = PL.run_pipeline(conn, cid, TEXT, call=FakeCall(sample_script(extract=_extract, split=AU.LLMFailed("down"))), now=lambda: 1.0)
   272	    assert {"code": "LLM_FAILED_AFTER_RETRIES", "stage": "split"} == {k: v for k, v in next(e for e in out["errors"] if e["stage"] == "split").items() if k in ("code", "stage")}
   273	    assert DB.table_counts(conn, cid)["records"] == 1
   274	
   275	
   276	def test_split_audit_row_has_prompt_version_and_flag_resolves_to_call(replay):
   277	    from app.db import db as DB
   278	    conn, cid, raw, call = replay
   279	    ing = PL.run_ingest(raw, call=call)
   280	    row = next(c for c in DB.list_llm_calls(conn, cid) if c["step"] == "split")
   281	    assert row["prompt_version"] == "split_v1"
   282	    flags = [f for f in ing["flags"] if f.get("category") == "llm_split"]
   283	    assert flags and all(f["ladder"]["generator"]["call_id"] == row["id"] and f["ladder"]["generator"]["prompt_version"] == "split_v1" for f in flags)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:59.616Z

**tool call — Bash**
````
{
 "command": "grep -n \"def make_call\\|FixtureMiss\\|LLMFailed\\|def backend_name\\|NO_MODEL\\|no model\\|No model\\|class .*Error\\|class .*Miss\\|LLM_BACKEND\" app/llm/*.py app/backend/*.py app/*.py 2>/dev/null | head -60",
 "description": "Locate model-availability and fixture-miss code paths"
}
````

### User / tool · 2026-11-02T02:39:59.704Z

**tool result**
````
app/llm/promptlib.py:1:"""Versioned prompt files (app/llm/prompts/<name>_v<N>.md) and nonce helper. Prompt text is data; no model call here."""
app/llm/audited.py:27:class LLMFailed(Exception):
app/llm/audited.py:31:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
app/llm/audited.py:32:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:35:        P.FixtureMissing.__init__(self, prompt_hash)
app/llm/audited.py:68:        except P.FixtureMissing as e:
app/llm/audited.py:89:            raise LLMFailedFixtureMiss(h)
app/llm/audited.py:92:    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed")
app/llm/audited.py:104:def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
app/llm/_types.py:7:class LLMError(Exception):
app/llm/_types.py:11:class FixtureMissing(LLMError):
app/llm/_types.py:19:FixtureMiss = FixtureMissing   # old spelling, kept as an alias
app/llm/provider.py:3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
app/llm/provider.py:15:from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
app/llm/provider.py:23:def backend_name() -> str:
app/llm/provider.py:25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
app/backend/api.py:46:class ApiError(Exception):
app/backend/api.py:102:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/backend/api.py:111:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
app/backend/api.py:125:    def make_call(c, cid):
app/llm/record.py:1:"""Fixture recorder: LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record evals/golden/<case>.txt
app/llm/record.py:22:        raise ValueError("record mode needs a live LLM_BACKEND (claude-cli or anthropic-api)")
app/llm/record.py:82:            print("refused: needs a live LLM_BACKEND and RECORD_FIXTURES=1", file=sys.stderr)
app/backend/generator.py:50:    except P.FixtureMiss:
app/backend/generator.py:52:    except AU.LLMFailed:
app/backend/generator.py:145:        except P.FixtureMiss:
app/backend/judges.py:33:    except AU.LLMFailed:
app/backend/judges.py:100:    Returns {id: {'verdict', 'ladder', 'call_id', 'reason_code', 'fixture_miss', 'model', 'prompt_version'}}. FixtureMiss -> ladder 'unavailable' + fixture_miss True."""
app/backend/judges.py:108:        except _P.FixtureMiss:
app/backend/flags.py:28:    except KeyError:    # a category outside the closed list: ground() rejects it; no model text is used as a title
app/backend/flags.py:189:    except P.FixtureMiss:
app/backend/flags.py:191:    except AU.LLMFailed:
app/backend/flags.py:220:    except P.FixtureMiss:
app/backend/flags.py:222:    except (AU.LLMFailed, ValidationError, TypeError, ValueError):
app/backend/flags.py:278:        except P.FixtureMiss:
app/backend/pdf_text.py:23:class PdfError(ValueError):
app/backend/pipeline.py:178:    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
app/backend/pipeline.py:380:        self.old = os.environ.get("LLM_BACKEND")
app/backend/pipeline.py:382:            os.environ["LLM_BACKEND"] = self.name
app/backend/pipeline.py:387:            os.environ.pop("LLM_BACKEND", None)
app/backend/pipeline.py:389:            os.environ["LLM_BACKEND"] = self.old
app/backend/ingest.py:2:R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
app/backend/ingest.py:23:class IngestError(ValueError):
app/backend/ingest.py:264:        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
app/backend/ingest.py:296:            warns.append(_warn("SPLIT_REJECTED", ("No model was available to propose record boundaries" if split_failure == "NO_MODEL" else "The AI's proposed record boundaries were not used (" + split_failure + ")") + "; the paste stays one record."))
app/backend/lexicon_scan.py:2:field answers, year_filter, suppress_if_followed_by. Pure; no model. Hits with strength high/medium raise flags; low is context only."""
app/backend/narrative.py:91:    except (AU.LLMFailed, P.FixtureMiss, ValidationError, TypeError, ValueError):
app/backend/review.py:18:class ReviewError(Exception):
app/backend/split_llm.py:21:        except P.FixtureMiss:
app/backend/split_llm.py:23:        except AU.LLMFailed:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:02.718Z

**tool call — Bash**
````
{
 "command": "sed -n 175,200p app/backend/pipeline.py; echo ----; grep -n \"run_ingest\\|ingest_case\\|run_pipeline\\|split_records\" app/backend/*.py app/*.py tools/*.py tests/unit/*.py tests/e2e/*.py 2>/dev/null | grep -v \"def \" | head -40; echo ----; sed -n 95,135p app/backend/api.py",
 "description": "Find callers of ingest_case, run_ingest, run_pipeline and api model wiring"
}
````

### User / tool · 2026-11-02T02:40:02.823Z

**tool result**
````
def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing)
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"]})
    a["state"], a["reasons"] = state, reasons
    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
----
app/backend/api.py:285:                ing = pipeline_mod().ingest_case(c, cid, text, now)
app/backend/api.py:326:            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
app/backend/pipeline.py:179:    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
app/backend/pipeline.py:239:    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid))
app/backend/pipeline.py:406:            out = run_pipeline(conn, cid, text, call=call)
app/backend/pipeline.py:468:        out = run_pipeline(conn, cid, raw)
app/backend/store.py:23:            body = ingest.split_records(block)[0]["excerpt"]
tests/unit/_fakes.py:62:    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call
tests/unit/test_amounts.py:81:    recs = I.split_records(base + "\n" + block)
tests/unit/test_narrative.py:11:    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
tests/unit/test_narrative.py:148:    PL.run_pipeline(conn, cid, G.raw("sample"), call=AU.make_call(conn, cid), now=lambda: 1.0)
tests/unit/test_manual_and_split.py:20:    PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
tests/unit/test_manual_and_split.py:97:    PL.run_pipeline(conn, cid, G.raw(CASE), call=call, now=lambda: 1.0)
tests/unit/test_manual_and_split.py:117:    PL.run_pipeline(conn, cid, G.raw(CASE), call=call, now=lambda: 2.0)
tests/unit/test_manual_and_split.py:159:    PL.run_pipeline(conn, cid, TWO, call=call, now=lambda: 1.0)
tests/unit/test_manual_and_split.py:177:    PL.run_pipeline(conn, cid, TWO, call=call, now=lambda: 2.0)                       # rerun keeps both, with their review status
tests/unit/test_pipeline.py:19:    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
tests/unit/test_pipeline.py:28:    out = PL.run_ingest(G.raw("sample"))
tests/unit/test_pipeline.py:121:    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script()), now=lambda: float(next(t)), deadline_s=480)
tests/unit/test_pipeline.py:126:    out = PL.run_ingest(G.raw("case_07_prompt_injection"))
tests/unit/test_pipeline.py:136:    PL.run_pipeline(conn, cid, G.raw("case_04_duplicates_no_amounts"), call=c, now=lambda: 1.0)
tests/unit/test_split_llm.py:124:    ing = PL.run_ingest(raw, call=call)
tests/unit/test_split_llm.py:139:    PL.ingest_case(conn, cid, raw, 1.0)
tests/unit/test_split_llm.py:141:    PL.run_pipeline(conn, cid, raw, call=call, now=2.0)         # the other steps have no fixtures: they fail visibly, the split does not
tests/unit/test_split_llm.py:214:    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
tests/unit/test_split_llm.py:217:    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
tests/unit/test_split_llm.py:245:    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
tests/unit/test_split_llm.py:247:    out = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
tests/unit/test_split_llm.py:271:    out = PL.run_pipeline(conn, cid, TEXT, call=FakeCall(sample_script(extract=_extract, split=AU.LLMFailed("down"))), now=lambda: 1.0)
tests/unit/test_split_llm.py:279:    ing = PL.run_ingest(raw, call=call)
tests/unit/test_ingest.py:8:    """R-IN-1 / row 1: split_records returns every golden record with its raw date, source label and excerpt."""
tests/unit/test_ingest.py:9:    got = I.split_records(G.raw(case))
tests/unit/test_ingest.py:22:    recs = I.split_records(G.raw("case_04_duplicates_no_amounts"))
tests/unit/test_ingest.py:28:    assert I.dedupe(I.split_records(G.raw("sample"))) == [[i] for i in range(1, 10)]
tests/unit/test_ingest.py:32:    recs = I.split_records(G.raw("case_04_duplicates_no_amounts"))
tests/unit/test_ingest.py:38:    assert [r["source"] for r in I.split_records(t)] == ["A Clinic", "B Clinic"]
tests/unit/test_ingest.py:43:    assert len(I.split_records(t)) == 1
tests/unit/test_ingest.py:49:    assert all(r["excerpt"] in raw for r in I.split_records(raw))
tests/unit/test_ingest.py:58:        I.split_records("x" * 2_000_000)
tests/unit/test_review_rules.py:20:    out = PL.run_pipeline(conn, cid, G.raw(case), call=call, now=lambda: 1.0)
----
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:15.585Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i \"T-063\\|T-057\\|T-066\" ; echo ----; grep -n -A12 \"major\" reviews/T-063-staff-engineer.md 2>/dev/null | head -60; echo ----; grep -rn \"NO_MODEL\\|SPLIT_REJECTED\\|FIXTURE_MISS\" docs/ spec/ memory/ reviews/ --include=*.md 2>/dev/null | head -40",
 "description": "Find T-063 review major 2 and spec references to split codes"
}
````

### User / tool · 2026-11-02T02:40:15.694Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:16.282Z

**tool call — Bash**
````
{
 "command": "sed -n 270,300p app/backend/api.py; echo ----; sed -n 395,410p app/backend/pipeline.py; echo ----; sed -n 462,470p app/backend/pipeline.py; echo ----; grep -n \"warnings\" app/backend/pipeline.py | head -20",
 "description": "Check API case creation, CLI paths, and warnings propagation"
}
````

### User / tool · 2026-11-02T02:40:16.388Z

**tool result**
````
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            name = name if isinstance(name, str) else ("Sample case" if sample else None)
            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, ingest.IngestError):
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
                    "record_warning_flags": [f["id"] for f in flags if f["type"] == "record_warning"],
                    "warnings": ing["warnings"]}
        finally:
----
    cid = DB.create_case(conn, text, now=0.0)
    return conn, cid, AU.make_call(conn, cid)


def run_case(text: str, backend: str = None) -> dict:
    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
        conn.close()
        return view

----
        return 1
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:          # a file, not :memory: (worker threads share the connection)
        conn = DB.connect(a.db or os.path.join(d, "cli.sqlite"))
        cid = DB.create_case(conn, IN.normalize_text(raw), now=time.time())
        out = run_pipeline(conn, cid, raw)
        conn.close()
    print(json.dumps(out, indent=1, default=str) if a.json else format_report(out))
----
5:Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
73:    for w in ing["record_warnings"]:
90:    warnings = list(ing["warnings"])
93:            warnings.append({"code": "INJECTION_SUSPECTED", "record_no": r["n"], "item_id": r["id"],
96:            "dates_to_confirm": ing["dates_to_confirm"], "flags": flags, "amounts": amounts, "damages": damages, "warnings": warnings,
288:                ing["warnings"].append({"code": f["pipeline_warning"], "stage": "conflicts", "item_id": f["id"],
345:            "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
367:            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:18.197Z

**tool call — Bash**
````
{
 "command": "grep -n \"SPLIT\\|NO_MODEL\\|Major 2\\|^- \\*\\*major\\|^### \\|major 2\\|2\\. \\*\\*\" reviews/T-063-staff-engineer.md | head -40; echo ----; sed -n 25,32p docs/LLM_VS_CODE.md",
 "description": "Find split references in T-063 review and LLM_VS_CODE row 1"
}
````

### User / tool · 2026-11-02T02:40:18.284Z

**tool result**
````
11:1. Row 1 (docs/LLM_VS_CODE.md:29) against `ingest.validate_split` (app/backend/ingest.py:149-165), the split trigger (ingest.py:262-270), the SPLIT_* warnings (ingest.py:284-289), split_llm.py, and the schema (schemas.py:59-66). Result: validator clauses match the doc; the SPLIT_REJECTED claim and the "one unsplit block" trigger do not.
20:- `git grep` at 473ac2a for validate_split, LLM_SPLIT, SPLIT_REJECTED, SPLIT_AMBIGUOUS, D-031 to D-035.
35:split_method ambiguous split_failure None codes ['SPLIT_AMBIGUOUS', 'DATE_EXCLUDED_FROM_GAPS']
36:invalid proposal: split_failure SPLIT_NOT_COVERING codes ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'DATE_EXCLUDED_FROM_GAPS']
71:**M1 (major) SPLIT_REJECTED with no model.** Doc row 1 (docs/LLM_VS_CODE.md:29) says: "If validation fails, or no model is available, the whole paste is one record flagged SPLIT_AMBIGUOUS with a SPLIT_REJECTED reason." ADR-018 (memory/DECISIONS.md:341) says "(SPLIT_REJECTED otherwise)". Code emits SPLIT_REJECTED only when `split_failure` is set (ingest.py:288-289), which needs a splitter that ran. `ingest_case` passes no call (pipeline.py:166-168), so the creation path emits SPLIT_AMBIGUOUS only. Reproduce: probe section 1, first line. Fix: emit SPLIT_REJECTED with reason NO_MODEL when an ambiguous single block is not sent to a model, or correct the doc. Acceptance test: `IN.ingest(TEXT)` contains a SPLIT_REJECTED warning whose message names the reason.
110:  "git grep at 473ac2a: validate_split, LLM_SPLIT, SPLIT_REJECTED, SPLIT_AMBIGUOUS, D-031..D-035",
127:  {"severity": "major", "title": "SPLIT_REJECTED is not emitted when no model is available",
128:   "evidence": "docs/LLM_VS_CODE.md:29 ('If validation fails, or no model is available, ... with a SPLIT_REJECTED reason'); memory/DECISIONS.md:341 ('SPLIT_REJECTED otherwise'); app/backend/ingest.py:286-289 (SPLIT_REJECTED only when split_failure is set); app/backend/pipeline.py:166-168 (ingest_case passes no call). Repro: probe section 1: codes ['SPLIT_AMBIGUOUS', 'DATE_EXCLUDED_FROM_GAPS'] with no splitter.",
130:   "fix": "Emit SPLIT_REJECTED with a reason code (for example NO_MODEL) when an ambiguous single block is not sent to a model, or correct the doc and ADR-018.",
131:   "acceptance_test": "IN.ingest(TEXT) with no splitter returns a SPLIT_REJECTED warning carrying a reason; a test in tests/unit/test_split_llm.py asserts it."},
----
"Code" is ordinary deterministic code with unit tests. "LLM" is a model call. Where both appear, the second column says who is the source of truth.

| # | Pipeline step | Code or LLM | Why we drew the line here | How it is checked |
|---|---|---|---|---|
| 1 | Split pasted text into records; merge exact duplicates | **Code first**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + text merges into one entry that cites every source record. Only when the code split finds **a single record that is unsplit, or lacks a date or a source label**, may a model be asked (a single record with both labels, such as a one-visit paste, is not sent), and it returns **character offsets only** (never text). Code validates the offsets (`ingest.validate_split`): the pieces must cover the whole text, be contiguous, start at line starts, and give a sensible record count. If validation fails, or the model call fails, the whole paste is **one** record flagged `SPLIT_AMBIGUOUS` plus `SPLIT_REJECTED` carrying the reason code. When no model is wired in at all (the case-creation path today), only `SPLIT_AMBIGUOUS` is emitted and the reason is not shown; that gap is card T-066, so read this row as the intended behaviour once T-066 lands. Every record cut by the model carries `LLM_SPLIT` and is `needs_review`. | Splitting is pattern matching. A model that rewrites or reorders text would alter the source, so it may only point at where to cut and code does the cutting. | The UI shows "N records found" before any pipeline model call. Unit tests: pieces concatenated equal the input; duplicates merge; `tests/unit/test_split_llm.py` covers accepted and rejected model splits. The call is audited as step `split`. A reviewer can mark one record of a merged entry "not a duplicate"; this is **not code only**: code undoes the merge and logs it, then the generator drafts that record's entry, judge 1 checks it, and the amount judge checks its amounts (see the second-wave section). |
| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. | The spec says date arithmetic is a decision. A model states a wrong date confidently. We prefer to ask. | Unit tests per format and per ambiguous case. Ambiguous or missing dates are excluded from gap math and listed under "Dates to confirm". |
| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initial evaluation"). The model is not asked for either. | A model told to "find the date" can pick the wrong one, and an adjuster cross-checks provider names against the record. The header is unambiguous. | Unit tests: the entry's date and provider equal the header values. An ambiguous date moves the entry to a "Dates to confirm" group after the timeline until the paralegal picks one of the readings the code proposed. |
| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the backend allows | Reading prose and condensing it is what models do well. | **Rung 1, code:** the excerpt is a contiguous run of whole sentences, word for word in the record; every number, date and dollar figure in the summary appears in the excerpt or source line, and every qualifier in the excerpt (hedge, "patient states", "without", left/right, "approx.") appears in the summary; if a chosen sentence is qualified by a hedge ("may represent", "correlate clinically") in the same or the next sentence, that hedge is included. **Rung 2, judge 1 (faithfulness):** "is every clause supported by this excerpt?" returns `supported`, `partially` or `unsupported`. **Rung 3:** human. |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:32.461Z

**tool call — Bash**
````
{
 "command": "ls -a; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md; echo ----; cat .claude/agent-memory/staff-engineer-reviewer/feedback_severity_vs_brief.md | head -30; echo ----; git status --short | head -20",
 "description": "List repo top level, read split-LLM memory, check git status"
}
````

### User / tool · 2026-11-02T02:40:32.586Z

**tool result**
````
.
..
.claude
.env
.git
.gitignore
.pytest_cache
.venv
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
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
----
---
name: split-llm-review-patterns
description: T-057 r1 (LLM split fallback, commit 099732b): eval report hash vs committed prompt, same-count re-run leaves stale records, surviving mutants masked by a sibling check, audited prompt_version dropped
metadata:
  type: project
---

Recurring patterns from the T-057 round-1 review (2026-11-01, reviews/T-057-staff-engineer.md, verdict fail: 2 blockers, 4 majors).

- **Eval report can attest to a different prompt.** The card's report (evals/reports/20261102T021046Z.md:44) listed split_v1.md at sha 579868d5..., but the committed file was 8e872bc4.... The report was also never committed (git log -- report prints nothing). **Why:** CONTRACT 8.3 says re-run evals before in_review; an uncommitted report that hashes an older prompt is not evidence. **How to apply:** for any prompt/model/schema change, compare `git show <sha>:<prompt> | shasum -a 256` with the hash in the report and check `git log -- <report>`.
- **Same-count re-run keeps stale rows.** pipeline.py replaced stored records only when the count differed, and _store_records returns early when rows exist. A second run with different boundaries of the same count leaves run-1 spans while entries use run-2 spans. Reachable via POST /api/cases/{token}/run (api.py:312). A deterministic fixture hides it; use a stub split. **How to apply:** for any "replace on change" guard, test a re-run where the count is equal and the content differs.
- **Mutant survives because a sibling check catches the same case.** Dropping the line-start check fails tests, but dropping coverage or contiguity leaves 33/33 green. The "gap" and "overlap" cases start mid-line, so the line-start check rejects them first. **How to apply:** for every validator clause, build a case where only that clause fails (line-start-aligned) and mutate each clause alone.
- **audited make_call drops prompt_version for every step.** audited.py:106 never passes prompt_version, so llm_calls.prompt_version is NULL for all steps, including the new split. Caller also discarded the call_id (split_llm.py:17 `_call_id`). **How to apply:** after any new LLM step, query llm_calls for the step and check prompt_version and that the output links to a call_id.
- **Bare except in the fallback path.** `except Exception: pass` around a splitter swallowed LLMFailed; the run showed only SPLIT_AMBIGUOUS and no errors[] entry. **How to apply:** grep `except Exception` in every fallback; the test asserted only the record count.
- **Evidence span relative to the wrong base.** LLM_SPLIT evidence used start 0 / end len of the excerpt, which selects the banner in the paste. **How to apply:** check T[start:end] == evidence text for every new flag.

Harness and environment gotchas seen in this review (also relevant to other reviewers):
- reviewer-write-guard blocks Write to the scratchpad path; write evidence scripts under artifacts/review-evidence/<card>-staff-engineer/ instead.
- git-guard blocks `rm` with an unresolved shell expansion; use fresh directory names instead of deleting.
- board-guard treats a `>` inside a grep pattern as a redirect and blocks the command; avoid `>` in patterns (use grep -e).
- `git archive <sha>` excludes untracked fixtures. At any T-057-era commit the judge replay tests (test_t037_backend.py) fail with FIXTURE_MISS even after `cp -n` from the working tree, and the same 3 fail at the parent commit, so there is no clean full-suite control. Report the split subset as the control, and say so.
- HEAD moved (099732b -> 996f9b4) and the working tree had 145 dirty files during the review. Pin by full sha.

See also [[project_eval_runner_review_patterns]], [[project_backend_llm_review_patterns]], [[project_llm_stage_review_patterns]], [[project_harness_review_patterns]].

## Round 2 additions (T-057 r2 b365af3, T-059 20d866f; 2026-11-01)
- **Replace-on-change fixes cover only the success path.** r1 fix deleted stored records when split_method == 'llm'; a re-run whose split FAILS or is rejected skips the delete, so run-1 records stay while run-2 entries cite the unsplit block (repro: artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py). **How to apply:** for any "replace stored state" fix, test success->failure and success->success re-runs.
- **Fix commit deletes a tracked fixture and leaves its replacement untracked** (prompt hash change re-keys the fixture). Always `git archive <sha>` + pytest -k <card> as the clean control; check `git status --short tests/fixtures`.
- **Seeded-hallucination tests that accept any reason code** let a whole check be mutated away (T-059 N3 D-006 token check, N11 basis-hash staleness both survived 17 passed). Incidental checks (dropped 'C/O' qualifier) catch every row for a self-report quote; use a clean quote (e5 'Pain 4/10, improving.') to isolate checks.
- Mutant scripts: write with the Write tool under artifacts/review-evidence/<card>-staff-engineer/; a `>` or `<` inside a bash heredoc/sed string trips board-guard.

## Round 3 additions (T-057 r3, fix 8bf99fb; 2026-11-01)
- **Replace-on-change fixes must also reconcile decided items.** 8bf99fb makes pending items consistent on failed and successful re-splits, but `_persist` only deletes pending rows, so ACCEPTED entries keep record ids that no longer exist (probe_accepted_orphan.py). why_view silently drops them (present.py:170-177). **How to apply:** for any "replace stored state" fix, add a test where the paralegal has accepted items before the re-run.
- **Pending-only tests hide accepted-item state.** The round-3 tests never accept anything, so they pass while the decided-item path is broken. **How to apply:** check whether the new test's fixtures include a decision step.
- **Board validator rejects placeholder JSON.** `<dummy>` values fail the verdict enum and severity check in board-validate.sh (PostToolUse). Ask before writing placeholders into a review record.
- **Brief command may not run.** System python3 has no pytest; use .venv/bin/python -m pytest and say so in the review.
----
---
name: severity-vs-brief
description: When the dispatch brief sets a default severity that conflicts with CONTRACT D.2 (for example "list mismatches as major"), rate per D.2 and state the deviation in the review
metadata:
  type: feedback
---

When the brief says to file a class of finding as a major, but the finding violates a spec constraint, rate it a blocker per CONTRACT D.2 (persona section 8) and say so in the review summary and in why_it_matters.

**Why:** T-063 brief said "list any mismatch as a major". The D-033 mismatch labelled a family member's statement as the patient's own self-report, which D-033 explicitly forbids. D.2 defines a spec-constraint violation as a blocker. I rated it a blocker, stated the deviation at the top of the review, and left the override to the orchestrator.

**How to apply:** for each finding, check the D.2 definition first; a brief's default is a starting point, not a cap. Put any deviation in the review's first paragraph so the orchestrator sees it without reading the JSON. Do not downgrade a finding to match a brief.

See also [[project_t063_doc_vs_code_review_patterns]].
----
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/llm/backends/fixture.py
 M board/activity.jsonl
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M evals/reports/latest.json
 M memory/SCOPE_CUTS.md
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
 M tests/fixtures/llm/067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
 M tests/fixtures/llm/128383b890348cd75ed0f2eb15f8516ffb0e90785d18225192c7a1b405bcf58d.json
 M tests/fixtures/llm/12c7d9209cd3664ab6d186c3019b41db44960c32d1e3116c3cab75b6940d40d1.json
 M tests/fixtures/llm/15676bbd3a5dfcc0ea008d7ce5df7d39df233a249a11548075e4595d1556399c.json
 M tests/fixtures/llm/15bbdc084a71365c8cbeb7dcce6bb8aa8661e71cdff83f73c613fea855ed21a2.json
 M tests/fixtures/llm/17ba1e45346d1f4b42edcc19e3012b72cdf6c0e95181231310148679957b4320.json
 M tests/fixtures/llm/1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:41.041Z

**tool call — Bash**
````
{
 "command": "git diff --stat e7c1912 HEAD -- app/backend/ingest.py tests/unit/test_split_llm.py app/backend/pipeline.py; echo \"scope-dirty:\"; git status --short -- app/backend/ingest.py tests/unit/test_split_llm.py app/backend/pipeline.py app/backend/split_llm.py tests/fixtures/llm/split; echo ----; ls tests/fixtures/llm/split 2>&1 | head; echo ----; git ls-files tests/fixtures/llm/split | head; echo ----; git cat-file -t e7c1912; git rev-parse --short HEAD",
 "description": "Check scope files for drift from pinned commit and fixture state"
}
````

### User / tool · 2026-11-02T02:40:41.216Z

**tool result**
````
scope-dirty:
----
d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
----
tests/fixtures/llm/split/d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
----
commit
373f8b1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:43.911Z

**tool call — Bash**
````
{
 "command": "D=artifacts/review-evidence/T-066-staff-engineer && mkdir -p $D/pinned-e7c1912 && git archive e7c1912 | tar -x -C $D/pinned-e7c1912 && cd $D/pinned-e7c1912 && ls && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -3; echo \"--- rerun (determinism)\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -1; echo \"--- targeted\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider -k \"no_model or confident_code\" -v 2>&1 | tail -6",
 "description": "Pin e7c1912 via git archive and run split tests twice"
}
````

### User / tool · 2026-11-02T02:40:46.245Z

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
...............................                                          [100%]
31 passed in 0.53s
--- rerun (determinism)
31 passed in 0.55s
--- targeted
plugins: anyio-4.16.0
collected 31 items / 29 deselected / 2 selected

tests/unit/test_split_llm.py ..                                          [100%]

======================= 2 passed, 29 deselected in 0.19s =======================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:52.753Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/mutate.py",
 "content": "\"\"\"Mutation spot-check for T-066 (commit e7c1912). Each mutant is a fresh copy of the pinned archive; the repo itself is never edited.\nRun: /Users/arsis/zlayt-pm-project/.venv/bin/python mutate.py <pinned_dir> <out_dir>\n\"\"\"\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\npinned = pathlib.Path(sys.argv[1])\nout = pathlib.Path(sys.argv[2])\nINGEST = \"app/backend/ingest.py\"\n\nMUTANTS = {\n    # M1: the one-line emission that sets the reason on an unsplit paste with no splitter is removed\n    \"M1_no_NO_MODEL_assignment\": (\n        '        split_failure = \"NO_MODEL\"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently\\n',\n        \"        pass\\n\"),\n    # M2: the SPLIT_REJECTED warning is suppressed for the NO_MODEL reason (assignment kept)\n    \"M2_no_SPLIT_REJECTED_for_NO_MODEL\": (\n        '        if split_failure:\\n            warns.append(_warn(\"SPLIT_REJECTED\"',\n        '        if split_failure and split_failure != \"NO_MODEL\":\\n            warns.append(_warn(\"SPLIT_REJECTED\"'),\n    # M3: the whole eligibility gate is dropped for the no-splitter branch (NO_MODEL set on any ambiguous paste, not just eligible ones)\n    \"M3_NO_MODEL_on_any_ambiguous\": (\n        '    if eligible and not splitter:\\n',\n        '    if method == \"ambiguous\" and not splitter:\\n'),\n}\n\nresults = {}\nfor name, (old, new) in MUTANTS.items():\n    dst = out / name\n    if dst.exists():\n        shutil.rmtree(dst)\n    shutil.copytree(pinned, dst, symlinks=True)\n    p = dst / INGEST\n    src = p.read_text()\n    n = src.count(old)\n    if n != 1:\n        results[name] = f\"MUTATION NOT APPLIED (matches={n})\"\n        continue\n    p.write_text(src.replace(old, new))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"tests/unit/test_split_llm.py\", \"-p\", \"no:cacheprovider\"],\n                       cwd=dst, capture_output=True, text=True)\n    failed = [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n    results[name] = {\"exit\": r.returncode, \"summary\": r.stdout.strip().splitlines()[-1], \"failed\": failed}\n\nfor k, v in results.items():\n    print(k, v)\n"
}
````

### User / tool · 2026-11-02T02:40:52.851Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/mutate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:54.792Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer && mkdir -p mutants && /Users/arsis/zlayt-pm-project/.venv/bin/python mutate.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/mutants 2>&1 | tail -20",
 "description": "Run three mutants of the NO_MODEL emission in scratch copies"
}
````

### User / tool · 2026-11-02T02:40:58.001Z

**tool result**
````
M1_no_NO_MODEL_assignment {'exit': 1, 'summary': '1 failed, 30 passed in 0.57s', 'failed': ['FAILED tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model']}
M2_no_SPLIT_REJECTED_for_NO_MODEL {'exit': 1, 'summary': '1 failed, 30 passed in 0.53s', 'failed': ['FAILED tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model']}
M3_NO_MODEL_on_any_ambiguous {'exit': 0, 'summary': '31 passed in 0.52s', 'failed': []}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:11.806Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/repro_paths.py",
 "content": "\"\"\"T-066 repro on the pinned tree (e7c1912). Run from the pinned copy root:\n  cd <pinned> && LLM_FIXTURE_DIR=<empty dir> /Users/arsis/zlayt-pm-project/.venv/bin/python <this file>\nPrints the warning codes/messages produced on (A) case creation (no model call), (B) a run with the fixture backend and no split fixture,\n(C) a multi-record paste with one trailing unsplit block (case creation), (D) re-run consistency: create -> good split -> failing split.\n\"\"\"\nimport os\nimport sys\nimport tempfile\n\nROOT = os.getcwd()\nsys.path.insert(0, ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.setdefault(\"LLM_FIXTURE_DIR\", tempfile.mkdtemp(prefix=\"empty-fixtures-\"))\n\nfrom app.backend import ingest as IN, pipeline as PL  # noqa: E402\nfrom app.db import db as DB  # noqa: E402\nfrom app.llm import audited as AU  # noqa: E402\nfrom tests.unit._fakes import FakeCall, sample_script  # noqa: E402\nfrom tests.unit.test_split_llm import TEXT, _extract, T  # noqa: E402\n\nTWO_PLUS_TAIL = \"Date: 2026-03-03\\nSource: Clinic A\\nExcerpt: Neck pain.\\n\\nDate: 2026-03-10\\nSource: Clinic A\\nExcerpt: Follow up.\\n\\nFree text with no label at all.\\n\"\n\n\ndef codes(ws):\n    return [(w[\"code\"], w[\"message\"]) for w in ws if w[\"code\"].startswith(\"SPLIT\")]\n\n\nprint(\"== A. case creation, unsplit paste, no splitter (POST /api/cases path)\")\ning = PL.ingest_case(DB.connect(os.path.join(tempfile.mkdtemp(), \"a.sqlite\")), DB.create_case(DB.connect(os.path.join(tempfile.mkdtemp(), \"x.sqlite\")), TEXT, now=1.0), TEXT, 1.0) if False else IN.ingest(TEXT)\nprint(\"split_failure:\", ing[\"split_failure\"], \"| split_method:\", ing[\"split_method\"])\nfor c in codes(ing[\"warnings\"]):\n    print(\"  \", c)\n\nprint(\"== B. run, fixture backend, no split fixture (api.py run path, call always set)\")\nconn = DB.connect(os.path.join(tempfile.mkdtemp(), \"b.sqlite\"))\ncid = DB.create_case(conn, TEXT, now=1.0)\nout = PL.run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid), now=lambda: 1.0)\nprint(\"split_failure:\", out.get(\"split_failure\"), \"| split_method:\", out.get(\"split_method\"))\nfor c in codes(out[\"warnings\"]):\n    print(\"  \", c)\nprint(\"  errors:\", [(e[\"code\"], e.get(\"stage\")) for e in out[\"errors\"] if e.get(\"stage\") == \"split\"])\n\nprint(\"== C. multi-record paste with one trailing unsplit block, case creation\")\ning = IN.ingest(TWO_PLUS_TAIL)\nprint(\"records:\", len(ing[\"records\"]), \"split_method:\", ing[\"split_method\"], \"split_failure:\", ing[\"split_failure\"])\nfor c in codes(ing[\"warnings\"]):\n    print(\"  \", c)\n\nprint(\"== D. re-run consistency: create (no model) -> run with good split -> run with failing split\")\nA = [(0, T.index(\"May 11\")), (T.index(\"May 11\"), T.index(\"May 25\")), (T.index(\"May 25\"), len(T))]\nT4 = IN.normalize_text(\"May 4, 2026\\nDr. A, ortho. Fall. Wrist swelling.\\nMay 11, 2026\\nDr. A, ortho. Pain 5/10.\\nMay 25, 2026\\nDr. A, ortho. Splint removed.\\n\")\na2, a3 = T4.index(\"May 11\"), T4.index(\"May 25\")\nA = [(0, a2), (a2, a3), (a3, len(T4))]\nruns = iter([A, \"call_fails\"])\n\n\ndef split(u):\n    v = next(runs)\n    if v == \"call_fails\":\n        raise AU.LLMFailed(\"down\")\n    return {\"records\": [{\"start\": a, \"end\": b} for a, b in v]}\n\n\nconn = DB.connect(os.path.join(tempfile.mkdtemp(), \"d.sqlite\"))\ncid = DB.create_case(conn, T4, now=1.0)\ncreated = PL.ingest_case(conn, cid, T4, 1.0)\nprint(\"after create: records stored =\", DB.table_counts(conn, cid)[\"records\"], \"| create codes:\", [c[0] for c in codes(created[\"warnings\"])])\ncall = FakeCall(sample_script(extract=_extract, split=split))\nout1 = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)\nprint(\"after run 1 (good split): stored =\", DB.table_counts(conn, cid)[\"records\"], \"| run records =\", len(out1[\"records\"]))\nout2 = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)\nstored = [tuple(r) for r in conn.execute(\"SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq\", (cid,))]\nprint(\"after run 2 (call fails): stored =\", len(stored), \"| run records =\", len(out2[\"records\"]), \"| consistent:\",\n      stored == [(r[\"id\"], r[\"char_start\"], r[\"char_end\"]) for r in out2[\"records\"]])\nprint(\"  run 2 split codes:\", [c[0] for c in codes(out2[\"warnings\"])], \"| split_failure:\", out2.get(\"split_failure\"))\n"
}
````

### User / tool · 2026-11-02T02:41:11.901Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/repro_paths.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:14.213Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/repro_paths.py",
 "old_string": "ing = PL.ingest_case(DB.connect(os.path.join(tempfile.mkdtemp(), \"a.sqlite\")), DB.create_case(DB.connect(os.path.join(tempfile.mkdtemp(), \"x.sqlite\")), TEXT, now=1.0), TEXT, 1.0) if False else IN.ingest(TEXT)",
 "new_string": "ing = PL.run_ingest(TEXT)   # exactly what ingest_case calls (no call= argument, so no splitter)"
}
````

### User / tool · 2026-11-02T02:41:14.329Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/repro_paths.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:15.858Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912 && E=$(mktemp -d /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/empty-fixtures.XXXX) && LLM_FIXTURE_DIR=$E /Users/arsis/zlayt-pm-project/.venv/bin/python ../repro_paths.py 2>&1 | tail -40",
 "description": "Run repro script for creation, run, multi-record and re-run paths"
}
````

### User / tool · 2026-11-02T02:41:16.249Z

**tool result**
````
llm call failed call_id=c0f14a195e291 step=split attempt=1 prompt_hash=04b22883aea55288aae152c4bab8882c055c1247c21e0299101f7618c8293692
llm call failed call_id=c94fe671d54f7 step=extract attempt=1 prompt_hash=095cf5dc7e22b80ae0bef91157762f6b77942388f160d16e8e7bde10addf589a
llm call failed call_id=ca99342b40a87 step=conflicts attempt=1 prompt_hash=ed1d2e84170fc8485050275fba202202e369964238d7a440a5bd689417ac5b6d
llm call failed call_id=c7730a9761fb9 step=flags attempt=1 prompt_hash=2745f46ef6c78f64d6307e31ed4941f72670246b06c57447266e4feb1f6c8190
== A. case creation, unsplit paste, no splitter (POST /api/cases path)
split_failure: NO_MODEL | split_method: ambiguous
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', 'No model was available to propose record boundaries; the paste stays one record.')
== B. run, fixture backend, no split fixture (api.py run path, call always set)
split_failure: None | split_method: None
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', "The AI's proposed record boundaries were not used (FIXTURE_MISS); the paste stays one record.")
  errors: [('LLM_FAILED_AFTER_RETRIES', 'split')]
== C. multi-record paste with one trailing unsplit block, case creation
records: 2 split_method: code split_failure: None
== D. re-run consistency: create (no model) -> run with good split -> run with failing split
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912/../repro_paths.py", line 50, in <module>
    A = [(0, T.index("May 11")), (T.index("May 11"), T.index("May 25")), (T.index("May 25"), len(T))]
             ^^^^^^^^^^^^^^^^^
ValueError: substring not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:22.237Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer && /usr/bin/perl -0pi -e 's/A = \\[\\(0, T\\.index\\(\"May 11\"\\)\\), \\(T\\.index\\(\"May 11\"\\), T\\.index\\(\"May 25\"\\)\\), \\(T\\.index\\(\"May 25\"\\), len\\(T\\)\\)\\]\\n//; s/TWO_PLUS_TAIL = .*\\n/TWO_PLUS_TAIL = \"Date: 2026-03-03\\\\nSource: Clinic A\\\\nExcerpt: Neck pain.\\\\n---\\\\nDate: 2026-03-10\\\\nSource: Clinic A\\\\nExcerpt: Follow up.\\\\n---\\\\nFree text with no label at all.\\\\n\"\\n/' repro_paths.py && grep -n \"TWO_PLUS_TAIL =\\|^A = \" repro_paths.py && cd pinned-e7c1912 && E=$(mktemp -d /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/empty-fixtures.XXXX) && LLM_FIXTURE_DIR=$E /Users/arsis/zlayt-pm-project/.venv/bin/python ../repro_paths.py 2>/dev/null | tail -30",
 "description": "Fix repro script section D and C, rerun on pinned copy"
}
````

### User / tool · 2026-11-02T02:41:22.863Z

**tool result**
````
21:TWO_PLUS_TAIL = "Date: 2026-03-03\nSource: Clinic A\nExcerpt: Neck pain.\n---\nDate: 2026-03-10\nSource: Clinic A\nExcerpt: Follow up.\n---\nFree text with no label at all.\n"
52:A = [(0, a2), (a2, a3), (a3, len(T4))]
== A. case creation, unsplit paste, no splitter (POST /api/cases path)
split_failure: NO_MODEL | split_method: ambiguous
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', 'No model was available to propose record boundaries; the paste stays one record.')
== B. run, fixture backend, no split fixture (api.py run path, call always set)
split_failure: None | split_method: None
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', "The AI's proposed record boundaries were not used (FIXTURE_MISS); the paste stays one record.")
  errors: [('LLM_FAILED_AFTER_RETRIES', 'split')]
== C. multi-record paste with one trailing unsplit block, case creation
records: 3 split_method: ambiguous split_failure: None
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
== D. re-run consistency: create (no model) -> run with good split -> run with failing split
after create: records stored = 1 | create codes: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED']
after run 1 (good split): stored = 3 | run records = 3
after run 2 (call fails): stored = 1 | run records = 1 | consistent: True
  run 2 split codes: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED'] | split_failure: None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:41.085Z

**tool call — Bash**
````
{
 "command": "git status --short -- tests/unit/test_split_llm.py app/backend/ingest.py; echo \"---diff vs e7c1912 (working tree):\"; git diff --stat e7c1912 -- tests/unit/test_split_llm.py app/backend/ingest.py; echo \"---sha256 pinned vs working:\"; shasum -a 256 artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912/tests/unit/test_split_llm.py tests/unit/test_split_llm.py app/backend/ingest.py artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912/app/backend/ingest.py; echo ---; git log --oneline -3",
 "description": "Check whether working-tree split test and ingest differ from pinned commit"
}
````

### User / tool · 2026-11-02T02:41:41.295Z

**tool result**
````
 M tests/unit/test_split_llm.py
---diff vs e7c1912 (working tree):
 tests/unit/test_split_llm.py | 57 ++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 57 insertions(+)
---sha256 pinned vs working:
87ce167add53cdebd9b40d630e7949ec31b08a79a424cb8449590395519a776e  artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912/tests/unit/test_split_llm.py
d1803c7c22d0b8e475ea567ad655c49a8f77fde60c765d08c278b1b4eb40d096  tests/unit/test_split_llm.py
cfdc2fa734deaf4ab1664fa0c582ca6bda4623d7b80f8afa26b1342e8573e9d6  app/backend/ingest.py
cfdc2fa734deaf4ab1664fa0c582ca6bda4623d7b80f8afa26b1342e8573e9d6  artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912/app/backend/ingest.py
---
8b2001e docs: D-040 cut the patient self-report chip (§7.4 after 4 rounds)
373f8b1 docs: D-039 freeze records once items are decided; redact dummy key in lessons; board sync
06eb84b fix(backend): narrative keeps a stored paragraph on failure, adds severity check, pins every check with tests (T-059 r1)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:44.191Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -3; echo \"--- added test names in uncommitted working-tree file (not in pinned sha):\"; git diff e7c1912 -- tests/unit/test_split_llm.py | grep \"^+def \\|^+@pytest\" | head -20",
 "description": "Run split tests on working tree and list uncommitted added tests"
}
````

### User / tool · 2026-11-02T02:41:45.161Z

**tool result**
````
..................................                                       [100%]
34 passed in 0.58s
--- added test names in uncommitted working-tree file (not in pinned sha):
+@pytest.mark.parametrize("second", ["call_fails", "different_bounds"])
+def test_rerun_after_decisions_reuses_stored_records_and_never_resplits(tmp_path, second):
+def test_resplit_stays_allowed_while_every_entry_is_pending(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:41:48.966Z

**tool call — Bash**
````
{
 "command": "git show e7c1912:app/backend/pipeline.py | grep -n -A4 'conn.execute(\"ROLLBACK\")'; echo ---; git show e7c1912:app/backend/pipeline.py | sed -n 130,140p | head -3",
 "description": "Check whether _store_records rollback re-raises the exception"
}
````

### User / tool · 2026-11-02T02:41:49.088Z

**tool result**
````
130:        conn.execute("ROLLBACK")
131-        raise
132-
133-
134-def _row(kind: str, it: dict) -> dict:
---
        conn.execute("ROLLBACK")
        raise
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:42:05.989Z

**tool call — Bash**
````
{
 "command": "grep -o '\"persona\": *\"[^\"]*\"' reviews/T-063-staff-engineer.md reviews/T-057-staff-engineer-r3.md | head -3; echo ---; grep -n \"\\\"split_method\\\"\\|split_failure\" <(git show e7c1912:app/backend/pipeline.py) | head; echo ---; python3 tools/board.py --help 2>&1 | grep -i \"validate\" | head -3; echo ---; grep -n \"def cmd_validate\\|validate\" tools/board.py | head -8",
 "description": "Check persona key convention, run-output keys, and validator availability"
}
````

### User / tool · 2026-11-02T02:42:06.180Z

**tool result**
````
reviews/T-063-staff-engineer.md:"persona": "staff-engineer-reviewer"
reviews/T-057-staff-engineer-r3.md:"persona": "staff-engineer-reviewer"
---
95:    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "banner": ing["banner"],
242:    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
243:        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
---
                {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
  {init,new,claim,move,note,handoff,ac,review,assign,dispatch,commit,update,next,status,validate,milestone,gate,lesson,inbox,log,show,list}
---
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:42:12.751Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912 && grep -n 'eligible = \\|if eligible and not splitter\\|split_failure = \"NO_MODEL\"\\|warns.append(_warn(\"SPLIT_REJECTED\"\\|if splitter and eligible' app/backend/ingest.py; grep -n 'call = call or AU.make_call\\|if ing.get(\"split_failure\") in\\|def run_pipeline\\|\"warnings\": ing\\[\"warnings\"\\]' app/backend/pipeline.py; grep -n \"def test_\" tests/unit/test_split_llm.py | sed -n 1,6p; grep -n \"run_ingest(raw_text, not_duplicates\\|def ingest_case\" app/backend/pipeline.py; grep -n 'raise ingest.SplitFailed(\"FIXTURE_MISS\")' app/backend/split_llm.py",
 "description": "Pin exact line numbers in the e7c1912 archive for evidence"
}
````

### User / tool · 2026-11-02T02:42:12.877Z

**tool result**
````
262:    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
263:    if eligible and not splitter:
264:        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
265:    if splitter and eligible:
296:            warns.append(_warn("SPLIT_REJECTED", ("No model was available to propose record boundaries" if split_failure == "NO_MODEL" else "The AI's proposed record boundaries were not used (" + split_failure + ")") + "; the paste stays one record."))
224:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
227:    call = call or AU.make_call(conn, cid, now=clock)
242:    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
345:            "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
12:def test_code_split_finds_one_unsplit_block_without_a_splitter():
17:def test_no_model_for_unsplit_paste_emits_split_rejected_no_model():
23:def test_confident_code_split_without_model_has_no_split_rejected():
28:def test_valid_llm_split_makes_two_records_each_flagged():
47:def test_invalid_boundaries_keep_one_record(bad):
55:def test_splitter_failure_keeps_one_record_with_a_reason():
177:def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
179:    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
22:            raise ingest.SplitFailed("FIXTURE_MISS") from None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:42:30.609Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer && /Users/arsis/zlayt-pm-project/.venv/bin/python mutate.py $PWD/pinned-e7c1912 $PWD/mutants > mutation_output.txt 2>&1; cat mutation_output.txt; cd pinned-e7c1912 && E=$(mktemp -d $PWD/../empty-fixtures.XXXX) && LLM_FIXTURE_DIR=$E /Users/arsis/zlayt-pm-project/.venv/bin/python ../repro_paths.py 2>/dev/null > ../repro_output.txt; cat ../repro_output.txt; cd .. && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>/dev/null | tail -1 >/dev/null; (cd pinned-e7c1912 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider) > pinned_pytest_output.txt 2>&1; tail -1 pinned_pytest_output.txt",
 "description": "Save mutation, repro and pinned pytest outputs as evidence files"
}
````

### User / tool · 2026-11-02T02:42:35.820Z

**tool result**
````
M1_no_NO_MODEL_assignment {'exit': 1, 'summary': '1 failed, 30 passed in 0.56s', 'failed': ['FAILED tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model']}
M2_no_SPLIT_REJECTED_for_NO_MODEL {'exit': 1, 'summary': '1 failed, 30 passed in 0.57s', 'failed': ['FAILED tests/unit/test_split_llm.py::test_no_model_for_unsplit_paste_emits_split_rejected_no_model']}
M3_NO_MODEL_on_any_ambiguous {'exit': 0, 'summary': '31 passed in 0.53s', 'failed': []}
== A. case creation, unsplit paste, no splitter (POST /api/cases path)
split_failure: NO_MODEL | split_method: ambiguous
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', 'No model was available to propose record boundaries; the paste stays one record.')
== B. run, fixture backend, no split fixture (api.py run path, call always set)
split_failure: None | split_method: None
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
   ('SPLIT_REJECTED', "The AI's proposed record boundaries were not used (FIXTURE_MISS); the paste stays one record.")
  errors: [('LLM_FAILED_AFTER_RETRIES', 'split')]
== C. multi-record paste with one trailing unsplit block, case creation
records: 3 split_method: ambiguous split_failure: None
   ('SPLIT_AMBIGUOUS', 'Record boundaries could not be found with confidence; check the split.')
== D. re-run consistency: create (no model) -> run with good split -> run with failing split
after create: records stored = 1 | create codes: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED']
after run 1 (good split): stored = 3 | run records = 3
after run 2 (call fails): stored = 1 | run records = 1 | consistent: True
  run 2 split codes: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED'] | split_failure: None
31 passed in 0.55s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:42:59.445Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-066-staff-engineer.md",
 "content": "# T-066 review (staff-engineer-reviewer), commit e7c1912\n\n**Verdict: changes.** No blockers. Two majors, two minors.\n\nConfirmed: on the case-creation path (`ingest_case`, no model call), an unsplit paste yields `SPLIT_REJECTED` with reason NO_MODEL, and removing that emission fails the new test in a scratch copy. The re-run path from 8bf99fb stays consistent with the change.\n\nNot confirmed as the brief states it: on the run path (`run_pipeline`, which always has a call), a paste with no split fixture reports reason `FIXTURE_MISS`, not NO_MODEL. I rated this major, not blocker: nothing is silent, and LLM_VS_CODE row 1 accepts a reason code on a failed call. The brief's wording is the reason for the escalation to \"reason NO_MODEL\".\n\nSecond major: a multi-record paste with one trailing unsplit block still gets `SPLIT_AMBIGUOUS` with no reason. LLM_VS_CODE row 1 names T-066 as the card that closes this gap. The `len(recs) == 1` gate that decides it is not pinned by any test (mutant M3 survives 31/31).\n\nModel note: this review ran as claude-haiku-5-5. CLAUDE.md §6 assigns engineering reviewers to Sonnet. See questions_for_chris.\n\n## Exercised\n- `git show --stat e7c1912` and `git show e7c1912 -- app/backend/ingest.py tests/unit/test_split_llm.py` (full diff read).\n- `git diff --stat e7c1912 HEAD -- app/backend/ingest.py tests/unit/test_split_llm.py app/backend/pipeline.py` (empty: scope files unchanged since the commit).\n- Pinned copy: `git archive e7c1912 | tar -x` into `artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912`, then `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider` run twice: `31 passed in 0.55s` and `31 passed in 0.55s` (output in `pinned_pytest_output.txt`). The brief's `python3 -m pytest` fails on system python: `No module named pytest`.\n- Working tree (not the pinned sha): `34 passed`. The extra 3 tests come from an uncommitted +57-line edit to `tests/unit/test_split_llm.py` that is not in e7c1912. Not reviewed.\n- Mutation spot-check, `artifacts/review-evidence/T-066-staff-engineer/mutate.py` (output in `mutation_output.txt`), each mutant in a fresh copy of the pinned tree:\n  - M1, remove the `split_failure = \"NO_MODEL\"` line (pinned ingest.py:264): `1 failed, 30 passed`. The failing test is `test_no_model_for_unsplit_paste_emits_split_rejected_no_model`.\n  - M2, suppress the SPLIT_REJECTED warning when reason is NO_MODEL (ingest.py:295): `1 failed, 30 passed`. Same test.\n  - M3, set NO_MODEL for any ambiguous paste, dropping the single-record gate (ingest.py:263): `31 passed`. Survivor.\n- Repro script `repro_paths.py` (output in `repro_output.txt`), run from the pinned copy with an empty `LLM_FIXTURE_DIR`:\n  - A (case creation, `PL.run_ingest(TEXT)`, the same call `ingest_case` makes at pipeline.py:179): `split_failure: NO_MODEL`, warning \"No model was available to propose record boundaries\".\n  - B (run, `run_pipeline` with `AU.make_call`): warning reason `FIXTURE_MISS`, errors `LLM_FAILED_AFTER_RETRIES` at stage split.\n  - C (multi-record paste with a trailing unsplit block, case creation): 3 records, `split_method: ambiguous`, only `SPLIT_AMBIGUOUS`.\n  - D (re-run consistency, create then good split then failing split): stored records equal run records (`consistent: True`).\n- Read: `docs/LLM_VS_CODE.md:29` (row 1), `reviews/T-063-staff-engineer.md` M1, `app/backend/split_llm.py:13-30`, `app/backend/pipeline.py:177-179, 224-227, 242-243, 345`, `app/backend/api.py:285, 326`, `personas/staff-engineer.md`.\n- Grep for bare or swallowed exceptions in the scope: ingest.py catches only `SplitFailed` and `ValueError` (narrow). `pipeline.py` `_store_records` re-raises after ROLLBACK.\n- Not run: full `tests/unit` suite (brief scoped to the split file), E2E, CLI on the sample case. No app URL exercised.\n\n## Findings\n\n### F1 (major): the run path reports FIXTURE_MISS, not NO_MODEL\n- Evidence: `artifacts/review-evidence/T-066-staff-engineer/repro_output.txt` section B: `('SPLIT_REJECTED', \"The AI's proposed record boundaries were not used (FIXTURE_MISS); the paste stays one record.\")`. Cause: `pipeline.py:227` `call = call or AU.make_call(conn, cid, now=clock)` means `run_pipeline` always passes a splitter, so the `if eligible and not splitter` branch (`ingest.py:263`) is reached only from `ingest_case` (`pipeline.py:179`). The splitter's fixture miss is `split_llm.py:22`, which raises `SplitFailed(\"FIXTURE_MISS\")`.\n- Why it matters: the brief requires reason NO_MODEL when \"no model or fixture\" is available. The same unsplit paste shows \"No model was available\" at creation and \"FIXTURE_MISS\" at run. Nothing is silent, and the doc accepts a reason code on a failed call, so this is not a blocker. It is still a visible divergence from the stated requirement, and the NO_MODEL reason is unreachable on every path that runs the pipeline.\n- Fix: the orchestrator picks one reason vocabulary and records it in `memory/ORCHESTRATOR_DECISIONS.md`. Option A: `split_llm.py:21-22` maps `FixtureMiss` to `SplitFailed(\"NO_MODEL\")`, and `pipeline.py:242-243` keeps the FIXTURE_MISS detail in the error entry. Option B: amend the brief and ADR-018 (`memory/DECISIONS.md:341`) to accept FIXTURE_MISS on the run path.\n- Acceptance test: `run_pipeline(conn, cid, TEXT, call=AU.make_call(conn, cid))` with an empty `LLM_FIXTURE_DIR` yields a SPLIT_REJECTED warning whose message names the chosen code, plus one `errors` entry for stage split. Reverting the fix must fail this test.\n\n### F2 (major): multi-record paste with an unsplit tail gets no reason\n- Evidence: `repro_output.txt` section C: 3 records, `split_method: ambiguous`, warnings `['SPLIT_AMBIGUOUS']` only. Gate: `ingest.py:262` `len(recs) == 1`. Doc: `docs/LLM_VS_CODE.md:29` says \"When no model is wired in at all (the case-creation path today), only `SPLIT_AMBIGUOUS` is emitted and the reason is not shown; that gap is card T-066, so read this row as the intended behaviour once T-066 lands.\" Survivor: mutant M3 (`mutate.py`, `31 passed in 0.53s`). No test feeds a multi-record paste with a leftover block.\n- Why it matters: the graded table says T-066 closes this gap, and this class of paste still shows no reason. The eligibility gate decides which pastes get a reason at all, and no test pins it. A future change to the gate would pass the suite.\n- Fix: either (a) emit SPLIT_REJECTED with a reason code for every ambiguous paste that is not sent to a model, which the orchestrator must name; or (b) amend LLM_VS_CODE row 1 and ADR-018 so the reason applies only to single-block pastes, with that scope written in the row. Either way, add a test for the multi-record tail.\n- Acceptance test: `IN.ingest(\"Date: 2026-03-03\\nSource: Clinic A\\nExcerpt: Neck pain.\\n---\\nDate: 2026-03-10\\nSource: Clinic A\\nExcerpt: Follow up.\\n---\\nFree text with no label at all.\\n\")` yields a SPLIT_REJECTED warning with a reason code. Mutant M3 must fail the suite.\n\n### F3 (minor): the named test checks ingest(), not the pipeline, and no reason text is pinned\n- Evidence: `tests/unit/test_split_llm.py:17-20` calls `IN.ingest(TEXT)` only and asserts `\"No model\" in message`. `tests/unit/test_split_llm.py:55-60` asserts only that SPLIT_REJECTED is present for `LLM_FAILED_AFTER_RETRIES`, not its reason. No test covers the run-path reason.\n- Why it matters: the AC and brief say \"the pipeline must emit\". Without a run-path test, F1 can regress silently.\n- Fix: add a `run_pipeline` test with the fixture backend and an empty fixture dir that asserts the reason code.\n- Acceptance test: that test fails when F1's fix is reverted.\n\n### F4 (minor): run output drops split_method and split_failure at top level\n- Evidence: `pipeline.py:95` (`run_ingest`) returns `split_failure`. The `run_pipeline` return at `pipeline.py:345` has no `split_method` or `split_failure` key. `repro_output.txt` section B prints `split_failure: None | split_method: None`.\n- Why it matters: the reason is only in message text, so the UI and evals cannot assert it without string matching.\n- Fix: include `split_method` and `split_failure` (reason code as a field) in the `run_pipeline` return.\n- Acceptance test: `run_pipeline(...)[\"split_failure\"] == \"FIXTURE_MISS\"` (or the code chosen under F1).\n\n## What is right\n- The NO_MODEL assignment is code-only and sits before the splitter branch (`ingest.py:262-265`). No model call, and the confident-split negative test passes (`test_split_llm.py:23-25`).\n- M1 and M2 are both killed by the new test. Errors are not swallowed: `SplitFailed` reasons reach warnings, and unexpected exceptions still propagate (`test_split_llm.py:63-67`).\n- The 8bf99fb re-run path is consistent with the change: create, good split, failing split leaves stored records equal to run records (`repro_output.txt` section D). The diff touches no record-storage code.\n\n```json\n{\"card\": \"T-066\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit e7c1912 (app/backend/ingest.py, tests/unit/test_split_llm.py), pinned via git archive to artifacts/review-evidence/T-066-staff-engineer/pinned-e7c1912; HEAD at review time 8b2001e; no app URL exercised; sample: evals/golden/unsplit_paste.txt via the test replay\",\n \"exercised\": [\n   \"git show --stat / git show e7c1912 (full diff read)\",\n   \"git diff --stat e7c1912 HEAD -- ingest.py test_split_llm.py pipeline.py (empty)\",\n   \"git archive e7c1912 -> pinned-e7c1912; .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider x2: 31 passed, 31 passed\",\n   \"system python3 -m pytest: No module named pytest (brief command not runnable on system python)\",\n   \"working tree test_split_llm.py (uncommitted +57 lines, not in e7c1912): 34 passed (not reviewed)\",\n   \"mutate.py on pinned copy: M1 remove NO_MODEL assignment -> 1 failed; M2 suppress NO_MODEL warning -> 1 failed; M3 drop single-record gate -> 31 passed (survivor)\",\n   \"repro_paths.py sections A-D on pinned copy (repro_output.txt): A NO_MODEL at creation; B FIXTURE_MISS on run; C multi-record tail gives SPLIT_AMBIGUOUS only; D re-run consistent True\",\n   \"read docs/LLM_VS_CODE.md:29, reviews/T-063-staff-engineer.md M1, split_llm.py:13-30, pipeline.py:177-179 / 224-227 / 242-243 / 345, api.py:285 / 326, personas/staff-engineer.md\",\n   \"grep bare/swallowed exceptions in scope; _store_records re-raises after ROLLBACK\"],\n \"verdict\": \"changes\",\n \"scores\": {\"contract_match_llm_vs_code_row1\": 3, \"failure_visibility\": 4, \"test_strength\": 3, \"rerun_consistency_8bf99fb\": 5, \"llm_free_deterministic_path\": 5},\n \"findings\": [\n   {\"severity\": \"major\", \"title\": \"Run path reports FIXTURE_MISS, not NO_MODEL; NO_MODEL unreachable on any path that runs the pipeline\",\n    \"evidence\": \"artifacts/review-evidence/T-066-staff-engineer/repro_output.txt section B: (\\\"SPLIT_REJECTED\\\", \\\"The AI's proposed record boundaries were not used (FIXTURE_MISS)...\\\"); pipeline.py:227 call always set; ingest.py:263 branch reached only from pipeline.py:179; split_llm.py:22 raise SplitFailed(\\\"FIXTURE_MISS\\\")\",\n    \"why_it_matters\": \"Brief requires reason NO_MODEL for no model or fixture. Same paste shows NO_MODEL at creation and FIXTURE_MISS at run. Not silent and accepted by LLM_VS_CODE row 1, so major not blocker.\",\n    \"fix\": \"Orchestrator picks one reason vocabulary and records it in memory/ORCHESTRATOR_DECISIONS.md. A: split_llm.py:21-22 maps FixtureMiss to SplitFailed(\\\"NO_MODEL\\\"), pipeline.py:242-243 keeps FIXTURE_MISS detail in errors. B: amend brief and ADR-018 (memory/DECISIONS.md:341).\",\n    \"acceptance_test\": \"run_pipeline(conn,cid,TEXT,call=AU.make_call(conn,cid)) with empty LLM_FIXTURE_DIR yields SPLIT_REJECTED naming the chosen code plus one errors entry stage=split; reverting the fix fails it.\"},\n   {\"severity\": \"major\", \"title\": \"Multi-record paste with an unsplit tail gets SPLIT_AMBIGUOUS with no reason; eligibility gate untested\",\n    \"evidence\": \"repro_output.txt section C: 3 records, split_method ambiguous, warnings ['SPLIT_AMBIGUOUS'] only; ingest.py:262 len(recs)==1 gate; docs/LLM_VS_CODE.md:29 names T-066 as the card closing this gap; mutate.py M3 -> 31 passed\",\n    \"why_it_matters\": \"The graded table says T-066 closes this gap and this class still shows no reason. The gate decides which pastes get a reason and no test pins it; a change to the gate passes the suite.\",\n    \"fix\": \"Either (a) SPLIT_REJECTED with a reason code for every ambiguous paste not sent to a model (orchestrator names the code), or (b) amend LLM_VS_CODE row 1 and ADR-018 to limit the reason to single-block pastes and say so in the row. Add a multi-record tail test either way.\",\n    \"acceptance_test\": \"IN.ingest('Date: 2026-03-03\\\\nSource: Clinic A\\\\nExcerpt: Neck pain.\\\\n---\\\\nDate: 2026-03-10\\\\nSource: Clinic A\\\\nExcerpt: Follow up.\\\\n---\\\\nFree text with no label at all.\\\\n') yields a SPLIT_REJECTED warning with a reason code; mutant M3 fails the suite.\"},\n   {\"severity\": \"minor\", \"title\": \"Named test exercises ingest(), not the pipeline; reason text unpinned\",\n    \"evidence\": \"tests/unit/test_split_llm.py:17-20 IN.ingest(TEXT) only; tests/unit/test_split_llm.py:55-60 asserts SPLIT_REJECTED presence only\",\n    \"why_it_matters\": \"AC and brief say the pipeline must emit it. Without a run-path test, F1 can regress silently.\",\n    \"fix\": \"Add a run_pipeline test with fixture backend and empty fixture dir asserting the reason code.\",\n    \"acceptance_test\": \"Test fails when the F1 fix is reverted.\"},\n   {\"severity\": \"minor\", \"title\": \"run_pipeline output drops split_method and split_failure at top level\",\n    \"evidence\": \"app/backend/pipeline.py:95 run_ingest returns split_failure; run_pipeline return pipeline.py:345 has no split_method/split_failure; repro_output.txt section B prints None for both\",\n    \"why_it_matters\": \"Reason exists only in message text; UI and evals cannot assert it without string matching.\",\n    \"fix\": \"Add split_method and split_failure (reason code as a field) to the run_pipeline return.\",\n    \"acceptance_test\": \"run_pipeline(...)['split_failure'] equals the code chosen under F1 on the fixture-miss run.\"}\n ],\n \"whats_right\": [\n   \"NO_MODEL assignment is code-only, before the splitter branch (ingest.py:262-265); no model call; confident-split negative test passes (test_split_llm.py:23-25).\",\n   \"Mutants M1 and M2 are both killed by the new test; SplitFailed reasons reach warnings and unexpected exceptions still propagate (test_split_llm.py:63-67).\",\n   \"8bf99fb re-run path stays consistent: create, good split, failing split leaves stored records equal to run records (repro_output.txt section D); no record-storage code touched.\"\n ],\n \"questions_for_chris\": [\n   \"Model policy: CLAUDE.md §6 assigns engineering reviewers to Sonnet; this review ran as claude-haiku-5-5. Should T-066 be re-reviewed on Sonnet before the record counts?\",\n   \"F2: should a multi-record paste with an unsplit tail show a reason at all? The answer changes LLM_VS_CODE row 1 and ADR-018.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:42:59.629Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-066-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:02.038Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json,re\nt=open('reviews/T-066-staff-engineer.md').read()\nm=re.search(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nd=json.loads(m.group(1)); print('json ok', d['verdict'], [f['severity'] for f in d['findings']])\n\" ; git rev-parse --short HEAD; python3 tools/board.py validate reviews/T-066-staff-engineer.md 2>&1 | tail -5; echo \"exit=$?\"",
 "description": "Parse the review JSON and run board validator on the file"
}
````

### User / tool · 2026-11-02T02:43:02.097Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:04.507Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/check_json.py",
 "content": "\"\"\"Parse the single fenced json block in reviews/T-066-staff-engineer.md and print its verdict and finding severities.\"\"\"\nimport json\nimport pathlib\nimport re\n\ntext = pathlib.Path(\"/Users/arsis/zlayt-pm-project/reviews/T-066-staff-engineer.md\").read_text()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"card\", d[\"card\"], \"persona\", d[\"persona\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"])\nprint(\"severities\", [f[\"severity\"] for f in d[\"findings\"]])\n"
}
````

### User / tool · 2026-11-02T02:43:04.617Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/check_json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:06.662Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-066-staff-engineer/check_json.py; git rev-parse --short HEAD; python3 tools/board.py validate reviews/T-066-staff-engineer.md 2>&1 | tail -5",
 "description": "Parse review JSON block and run board validator"
}
````

### User / tool · 2026-11-02T02:43:06.955Z

**tool result**
````
json blocks: 1
card T-066 persona staff-engineer-reviewer model claude-haiku-5-5 verdict changes
severities ['major', 'major', 'minor', 'minor']
f201e3b
ok (1 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:13.818Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t066_no_model_reason_patterns.md",
 "content": "---\nname: t066-no-model-reason-patterns\ndescription: T-066 r1 (commit e7c1912, SPLIT_REJECTED NO_MODEL): reason code unreachable on the run path, eligibility gate survives mutation, brief command not runnable on system python\nmetadata:\n  type: project\n---\n\nRecurring patterns from the T-066 round-1 review (2026-11-02, reviews/T-066-staff-engineer.md, verdict changes: 0 blockers, 2 majors, 2 minors).\n\n- **A new \"no splitter\" branch is dead on the run path.** `run_pipeline` sets `call = call or AU.make_call(...)` (pipeline.py:227), so every pipeline run passes a splitter and the `if eligible and not splitter` branch (ingest.py:263) only runs from `ingest_case` (creation). On a run with no fixture the reason is FIXTURE_MISS, not NO_MODEL. **How to apply:** for any branch keyed on `splitter is None` / `call is None`, grep every caller and run the producer through `run_pipeline` (not `ingest()`), then check the reason it actually emits.\n- **Gate mutants survive when the test only covers the positive case.** Dropping the single-record gate (`len(recs) == 1`) left 31/31 green; the only negative test is a confident split. **How to apply:** for every eligibility gate, add a case where gate-on and gate-off differ in output; mutate the gate alone.\n- **Doc row can name the card as the fix.** LLM_VS_CODE row 1 said \"that gap is card T-066, so read this row as the intended behaviour once T-066 lands\", so the review checks the doc's stated scope, not only the card AC wording (\"an unsplit paste\").\n- **Brief command fails on system python.** `python3 -m pytest` returns `No module named pytest`; use `.venv/bin/python -m pytest -p no:cacheprovider`. Same gotcha as [[project_split_llm_review_patterns]].\n- **Working tree moves during review.** Another agent appended 57 uncommitted lines to the split test file mid-review (34 passed vs 31 at the pinned sha). Pin with `git archive <sha>` into review-evidence and report the working-tree count separately.\n- **Harness: board-guard denies `python -c` with escaped backticks.** A `\\`\\`\\`json` regex inside `python3 -c` returned \"could not parse command safely\". Put the check in a file under artifacts/review-evidence and run that.\n\nSee also [[project_llm_stage_review_patterns]], [[project_harness_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T02:43:13.927Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t066_no_model_reason_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:15.695Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)",
 "new_string": "- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)\n- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — T-066 r1: splitter-None branch dead on run path (FIXTURE_MISS), gate mutant survives, system python lacks pytest"
}
````

### User / tool · 2026-11-02T02:43:15.808Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:43:17.705Z

Verdict: changes (0 blockers, 2 majors, 2 minors). NO_MODEL works on case creation and the 8bf99fb re-run stays consistent, but on the run path a missing fixture reports FIXTURE_MISS, and a multi-record paste with an unsplit tail still gets no reason.
Review: /Users/arsis/zlayt-pm-project/reviews/T-066-staff-engineer.md (board validate: ok); evidence under /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-066-staff-engineer/. Pinned 31/31 at e7c1912; `python3 -m pytest` fails on system python, so I used .venv.
