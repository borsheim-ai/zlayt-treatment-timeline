# Subagent: T-062 review (haiku) (T-062 review (haiku))

Source: `agent-a495b96df21f6be99.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:14:51.201Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-062 (AC: `python3 tools/board.py show T-062`). Run `.venv/bin/python -m pytest tests/unit/test_db.py -q 2>&1 | tail -2`. Check the new log-only review actions (not_duplicate, manual_entry) write an events row with before/after and never set review_status to accepted; the AST guard test still passes. Write reviews/T-062-staff-engineer.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:52.336Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:14:52.343Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:52.669Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-062",
 "description": "Show board card T-062"
}
````

### User / tool · 2026-11-02T02:14:52.800Z

**tool result**
````
---
id: "T-062"
title: "db: log-only review actions not_duplicate and manual_entry (for T-056)"
milestone: "M3"
role: "db"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:14:27Z"
updated_at: "2026-11-02T02:14:52Z"
claimed_by: "db"
claimed_at: "2026-11-02T02:14:35Z"
rounds: 0
commits: ["5f8858f"]
reviews: []
ac:
  - {"n": 1, "text": "app/db/db.py ACTIONS gains 'not_duplicate' and 'manual_entry' (None = logged only, status unchanged); schema.sql review_events CHECK accepts them; schema version bumped so old files rebuild; a test in tests/unit/test_db.py logs one of each and reads it back with before/after JSON", "done": true, "evidence": "tests/unit/test_db.py::test_log_only_actions_not_duplicate_and_manual_entry, test_old_schema_file_is_rebuilt; 23 passed; SCHEMA_VERSION=2 via PRAGMA user_version"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:14:35Z db: claimed
- 2026-11-02T02:14:45Z db: AC 1 checked: tests/unit/test_db.py::test_log_only_actions_not_duplicate_and_manual_entry, test_old_schema_file_is_rebuilt; 23 passed; SCHEMA_VERSION=2 via PRAGMA user_version
- 2026-11-02T02:14:45Z db: moved in_progress -> in_review
- 2026-11-02T02:14:52Z orchestrator: review dispatched: staff (haiku)

## Handoff
ACTIONS + review_events CHECK gain not_duplicate/manual_entry (log-only). SCHEMA_VERSION=2 (PRAGMA user_version); older files dropped+rebuilt in connect(). 2 tests added; 23 passed. Left: nothing.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:52.974Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_db.py -q 2>&1 | tail -2",
 "description": "Run DB unit tests and show summary"
}
````

### User / tool · 2026-11-02T02:14:53.564Z

**tool result**
````
.......................                                                  [100%]
23 passed in 0.27s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:56.363Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_db_review_patterns.md"
}
````

### User / tool · 2026-11-02T02:14:56.369Z

**tool result**
````
1	---
2	name: db-review-patterns
3	description: T-031 (app/db) round-1/round-2 review patterns - partial re-fixes, regex guard blind spots, scratch-copy mutation method, hook gotchas for reviewers
4	metadata:
5	  type: project
6	---
7	
8	Recurring patterns from the T-031 review (app/db/db.py, tests/unit/test_db.py; reviews reviews/T-031-staff-engineer.md and -r2.md).
9	
10	- **A re-fix closes the named entry point, not the write class.** Round 2 locked `update_item` (db.py:137) but left `add_item` (db.py:90-101) accepting `edited_json` with no review event. When a finding says "X can be written with no event", grep every helper that reaches the same column (`grep -rn edited_json app`), not just the one named.
11	- **Source-regex guard tests have blind spots.** test_review_status_only_via_apply_review matches `review_status=?`, `SET review_status`, `review_status='...'`. It misses a multi-column `SET edited_json=?, review_status=:s`, and the test still passes while its docstring says the property holds. Probe such guards with an appended rogue line in a scratch copy before accepting them as proof.
12	- **"Raises on no payload" was true only for the fresh item.** `(edited or before["edited"])` lets a re-edit with no payload succeed and log an event. When a fix says "raises when X", probe the state variants (fresh, already-edited).
13	- **Mutation method that works:** copy app/ and tests/ to the scratchpad, `sed -i.bak` one guard, run `pytest tests/unit/test_db.py -q`, restore from .bak. Do not touch repo files.
14	
15	Reviewer environment gotchas (seen on this card):
16	- The Bash git-guard hook denies commands containing backticks inside a `python -c "..."` string ("could not parse command safely"). Put scripts in a file and run the file.
17	- reviewer-write-guard blocks Write to the scratchpad. Scripts and probes must go under artifacts/review-evidence/.
18	
19	Related: [[project_harness_review_patterns]], [[project_design_review_patterns]].
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:57.011Z

**tool call — Bash**
````
{
 "command": "ls app/db/ tests/unit/ && git -C /Users/arsis/zlayt-pm-project show --stat 5f8858f 2>&1 | head -30; git -C /Users/arsis/zlayt-pm-project log --oneline -5 2>&1",
 "description": "List DB files, commit stat, recent log"
}
````

### User / tool · 2026-11-02T02:14:57.148Z

**tool result**
````
app/db/:
__init__.py
__pycache__
db.py
schema.sql

tests/unit/:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_boundaries.py
test_confidence.py
test_conflicts.py
test_dates.py
test_db.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_gaps.py
test_generator.py
test_grounding.py
test_ingest.py
test_injection.py
test_judges.py
test_multicase.py
test_pdf_upload.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_split_llm.py
test_t033_backend.py
test_t037_backend.py
test_totals.py
commit 5f8858f493a45ec59d5bdc3305afb466792ffb27
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:14:46 2026 -0600

    feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/db/db.py          |  8 +++++++-
 app/db/schema.sql     |  2 +-
 tests/unit/test_db.py | 20 ++++++++++++++++++++
 3 files changed, 28 insertions(+), 2 deletions(-)
5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
099732b feat(backend): LLM split fallback for unsplit pastes, validated by code, flagged LLM_SPLIT (T-057, D-031)
a010dd4 feat(research): synthetic case library, 7 packets with sources and validator (T-052)
2c2eb1f feat(backend): local-mode case list, library loader; api.md audit shapes (T-053)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:58.355Z

**tool call — Bash**
````
{
 "command": "git show 5f8858f -- app/db/db.py app/db/schema.sql tests/unit/test_db.py",
 "description": "Show the T-062 commit diff"
}
````

### User / tool · 2026-11-02T02:14:58.451Z

**tool result**
````
commit 5f8858f493a45ec59d5bdc3305afb466792ffb27
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:14:46 2026 -0600

    feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/db/db.py b/app/db/db.py
index 4213a63..929fc9c 100644
--- a/app/db/db.py
+++ b/app/db/db.py
@@ -16,11 +16,13 @@ import time
 RETENTION_SECONDS = 24 * 3600
 REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
 ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
-           "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
+           "confirm_date": None, "keep_my_wording": None,
+           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
 _ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
 _ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
 _PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
 _CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
+SCHEMA_VERSION = 2   # bump on any schema.sql change; an older file is dropped and rebuilt (data is ephemeral, 24 h)
 _SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
 
 
@@ -53,6 +55,10 @@ def connect(path: str):
     conn.row_factory = sqlite3.Row
     conn.execute("PRAGMA secure_delete=ON")
     conn.execute("PRAGMA foreign_keys=ON")
+    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
+        for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','index') AND name NOT LIKE 'sqlite_%'").fetchall():
+            if r["name"] and not r["name"].startswith("ix_"):
+                conn.execute(f"DROP TABLE IF EXISTS {r['name']}")
     with open(_SCHEMA, encoding="utf-8") as f:
         conn.executescript(f.read())
     conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
diff --git a/app/db/schema.sql b/app/db/schema.sql
index 7e97b6f..5037c31 100644
--- a/app/db/schema.sql
+++ b/app/db/schema.sql
@@ -54,7 +54,7 @@ CREATE TABLE IF NOT EXISTS llm_calls (
 );
 CREATE TABLE IF NOT EXISTS review_events (
   id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording')),
+  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
   before_json TEXT, after_json TEXT, at REAL
 );
 CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
diff --git a/tests/unit/test_db.py b/tests/unit/test_db.py
index 580404f..e1ce833 100644
--- a/tests/unit/test_db.py
+++ b/tests/unit/test_db.py
@@ -173,3 +173,23 @@ def test_add_item_rejects_edits_and_status(conn):
             DB.add_item(conn, cid, "entry", bad)
     assert DB.table_counts(conn, cid)["entries"] == before
     assert DB.get_item(conn, _entry(conn, cid))["edited"] is None
+
+
+def test_log_only_actions_not_duplicate_and_manual_entry(conn):
+    """T-062: logged with before/after, status unchanged."""
+    cid = seed(conn); iid = _entry(conn, cid)
+    DB.apply_review(conn, iid, "not_duplicate", now=7)
+    DB.apply_review(conn, iid, "manual_entry", now=8)
+    ev = DB.list_events(conn, cid, iid)
+    assert [e["action"] for e in ev] == ["not_duplicate", "manual_entry"]
+    assert all(e["before"] == e["after"] == {"review_status": "pending", "edited": None} for e in ev)
+    assert DB.get_item(conn, iid)["review_status"] == "pending"
+
+def test_old_schema_file_is_rebuilt(tmp_path):
+    import sqlite3
+    path = str(tmp_path / "old.sqlite")
+    old = sqlite3.connect(path)
+    old.execute("CREATE TABLE review_events (id TEXT, action TEXT CHECK (action IN ('accept')))"); old.commit(); old.close()
+    c = DB.connect(path)
+    cid = DB.create_case(c, "t", now=1); iid = _entry(c, cid)
+    DB.apply_review(c, iid, "manual_entry", now=2)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:58.669Z

**tool call — Bash**
````
{
 "command": "cat -n app/db/db.py",
 "description": "Read full app/db/db.py with line numbers"
}
````

### User / tool · 2026-11-02T02:14:58.748Z

**tool result**
````
     1	"""SQLite persistence (ADR-002, ADR-006). Owner: db.
     2	
     3	- Times are epoch seconds passed in by the caller (`now=`); nothing here reads the clock, so tests inject a fake one.
     4	- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
     5	- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
     6	- delete_case() is the one deletion path; purge_expired() calls it. Never log record text or prompts.
     7	"""
     8	import hashlib
     9	import json
    10	import logging
    11	import os
    12	import secrets
    13	import sqlite3
    14	import time
    15	
    16	RETENTION_SECONDS = 24 * 3600
    17	REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
    18	ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
    19	           "confirm_date": None, "keep_my_wording": None,
    20	           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
    21	_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
    22	_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
    23	_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
    24	_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
    25	SCHEMA_VERSION = 2   # bump on any schema.sql change; an older file is dropped and rebuilt (data is ephemeral, 24 h)
    26	_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
    27	
    28	
    29	def init(path: str = ":memory:"):
    30	    return connect(path)
    31	
    32	
    33	SCHEMA_VERSION = 2          # 1 = global ids (pre T-050); 2 = (case_id, id) keys
    34	log = logging.getLogger("zlayt.db")
    35	
    36	
    37	def connect(path: str):
    38	    """Open (and create) the database. A file written by an older schema version is moved aside to <path>.old-<ts> and rebuilt
    39	    (one log line, no data text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys."""
    40	    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
    41	        probe = sqlite3.connect(path)
    42	        try:
    43	            version = probe.execute("PRAGMA user_version").fetchone()[0]
    44	            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
    45	        finally:
    46	            probe.close()
    47	        if has_tables and version != SCHEMA_VERSION:
    48	            moved = f"{path}.old-{int(time.time())}"
    49	            os.replace(path, moved)
    50	            for ext in ("-wal", "-shm"):
    51	                if os.path.exists(path + ext):
    52	                    os.replace(path + ext, moved + ext)
    53	            log.warning("database schema version %s != %s: moved %s aside and rebuilt", version, SCHEMA_VERSION, os.path.basename(moved))
    54	    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
    55	    conn.row_factory = sqlite3.Row
    56	    conn.execute("PRAGMA secure_delete=ON")
    57	    conn.execute("PRAGMA foreign_keys=ON")
    58	    if conn.execute("PRAGMA user_version").fetchone()[0] != SCHEMA_VERSION:
    59	        for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','index') AND name NOT LIKE 'sqlite_%'").fetchall():
    60	            if r["name"] and not r["name"].startswith("ix_"):
    61	                conn.execute(f"DROP TABLE IF EXISTS {r['name']}")
    62	    with open(_SCHEMA, encoding="utf-8") as f:
    63	        conn.executescript(f.read())
    64	    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
    65	    return conn
    66	
    67	
    68	def _tok(prefix: str) -> str:
    69	    return prefix + secrets.token_hex(6)
    70	
    71	
    72	def _enc(v):
    73	    return json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v
    74	
    75	
    76	def _cols(conn, table):
    77	    return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
    78	
    79	
    80	def sha256(text: str) -> str:
    81	    return hashlib.sha256(text.encode("utf-8")).hexdigest()
    82	
    83	
    84	def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
    85	    cid = fields.pop("id", None) or secrets.token_urlsafe(16)
    86	    row = {"id": cid, "name": name, "source": source, "raw_text": raw_text, "text_sha256": sha256(raw_text),
    87	           "created_at": now, **fields}
    88	    _insert(conn, "cases", row)
    89	    return cid
    90	
    91	
    92	def update_case(conn, case_id: str, **fields) -> None:
    93	    ok = _cols(conn, "cases") - {"id", "created_at", "raw_text"}
    94	    bad = set(fields) - ok
    95	    if bad:
    96	        raise ValueError(f"unknown case fields {sorted(bad)}")
    97	    sets = ", ".join(f"{k}=?" for k in fields)
    98	    conn.execute(f"UPDATE cases SET {sets} WHERE id=?", [_enc(v) for v in fields.values()] + [case_id])
    99	
   100	
   101	def get_case(conn, case_id: str):
   102	    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
   103	    return _decode(r) if r else None
   104	
   105	
   106	def _insert(conn, table, row):
   107	    bad = set(row) - _cols(conn, table)
   108	    if bad:
   109	        raise ValueError(f"unknown {table} fields {sorted(bad)}")
   110	    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
   111	                 [_enc(v) for v in row.values()])
   112	
   113	
   114	def add_record(conn, case_id: str, **fields) -> str:
   115	    rid = fields.pop("id", None) or _tok("r")
   116	    _insert(conn, "records", {"id": rid, "case_id": case_id, **fields})
   117	    return rid
   118	
   119	
   120	def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
   121	    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
   122	    if kind not in _ITEM_TABLES:
   123	        raise ValueError(f"unknown item kind {kind!r}")
   124	    table, prefix = _ITEM_TABLES[kind]
   125	    p = dict(payload)
   126	    if {"review_status", "edited_json", "edited"} & set(p):
   127	        raise ValueError("review_status and edits are written only by apply_review (with an event row)")
   128	    iid = p.pop("id", None) or _tok(prefix)
   129	    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
   130	    return iid
   131	
   132	
   133	def _find(conn, item_id, case=None):
   134	    """Item ids are unique per case (T-050). Pass `case` (the case id) whenever more than one case can share the file."""
   135	    kind = _PREFIX_KIND.get(item_id[:1])
   136	    if kind is None:
   137	        raise KeyError(item_id)
   138	    table = _ITEM_TABLE_OF[kind]
   139	    q, a = f"SELECT * FROM {table} WHERE id=?", [item_id]
   140	    if case is not None:
   141	        q, a = q + " AND case_id=?", a + [case]
   142	    rows = conn.execute(q, a).fetchall()
   143	    if not rows:
   144	        raise KeyError(item_id)
   145	    if len(rows) > 1:
   146	        raise ValueError(f"item id {item_id!r} exists in several cases; pass case=")
   147	    return table, rows[0]
   148	
   149	
   150	def _decode(row) -> dict:
   151	    out = {}
   152	    for k in row.keys():
   153	        v = row[k]
   154	        if k.endswith("_json"):
   155	            out[k[:-5]] = json.loads(v) if v else None
   156	        else:
   157	            out[k] = v
   158	    return out
   159	
   160	
   161	def get_item(conn, item_id: str, case: str = None) -> dict:
   162	    return _decode(_find(conn, item_id, case)[1])
   163	
   164	
   165	def list_items(conn, case_id: str, kind: str) -> list:
   166	    table = _ITEM_TABLES[kind][0]
   167	    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
   168	
   169	
   170	def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
   171	    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
   172	    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
   173	    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
   174	    if locked & set(fields):
   175	        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
   176	    table, found = _find(conn, item_id, case)
   177	    bad = set(fields) - _cols(conn, table)
   178	    if bad:
   179	        raise ValueError(f"unknown {table} fields {sorted(bad)}")
   180	    fields["updated_at"] = now
   181	    sets = ", ".join(f"{k}=?" for k in fields)
   182	    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
   183	
   184	
   185	def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
   186	    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
   187	    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
   188	    if action not in ACTIONS:
   189	        raise ValueError(f"invalid review action {action!r}")
   190	    table, row = _find(conn, item_id, case)
   191	    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
   192	    status = ACTIONS[action] or row["review_status"]
   193	    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
   194	    if action == "edit" and not new_edited:
   195	        raise ValueError("edit requires a non-empty edited payload")
   196	    after = {"review_status": status, "edited": new_edited}
   197	    conn.execute("BEGIN")
   198	    try:
   199	        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
   200	                     (status, _enc(new_edited), now, item_id, row["case_id"]))
   201	        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
   202	                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
   203	        conn.execute("COMMIT")
   204	    except Exception:
   205	        conn.execute("ROLLBACK")
   206	        raise
   207	    return get_item(conn, item_id, row["case_id"])
   208	
   209	
   210	def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
   211	    if status not in REVIEW_STATUSES:
   212	        raise ValueError(f"invalid review_status {status!r}")
   213	    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
   214	    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
   215	
   216	
   217	def list_events(conn, case_id: str, item_id: str = None) -> list:
   218	    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
   219	    if item_id:
   220	        q, a = q + " AND item_id=?", a + [item_id]
   221	    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
   222	
   223	
   224	def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
   225	    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
   226	    cid = fields.pop("id", None) or _tok("c")
   227	    row = {"id": cid, "case_id": case_id, "system_text": system, "user_text": prompt, "response_raw": response,
   228	           "prompt_sha256": sha256((system or "") + "\n" + prompt), "created_at": now, **fields}
   229	    _insert(conn, "llm_calls", row)
   230	    return cid
   231	
   232	
   233	def get_llm_call(conn, call_id: str):
   234	    r = conn.execute("SELECT * FROM llm_calls WHERE id=?", (call_id,)).fetchone()
   235	    return _decode(r) if r else None
   236	
   237	
   238	def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
   239	    q, a = "SELECT * FROM llm_calls WHERE case_id=?", [case_id]
   240	    if item_id:
   241	        q, a = q + " AND item_id=?", a + [item_id]
   242	    return [_decode(r) for r in conn.execute(q + " ORDER BY created_at, rowid", a)]
   243	
   244	
   245	def delete_case(conn, case_id: str) -> None:
   246	    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
   247	    conn.execute("BEGIN")
   248	    try:
   249	        for t in _CASE_TABLES:
   250	            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
   251	        conn.execute("COMMIT")
   252	    except Exception:
   253	        conn.execute("ROLLBACK")
   254	        raise
   255	
   256	
   257	def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
   258	    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
   259	    for cid in ids:
   260	        delete_case(conn, cid)
   261	    return len(ids)
   262	
   263	
   264	def table_counts(conn, case_id: str) -> dict:
   265	    return {t: conn.execute(f"SELECT COUNT(*) FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,)).fetchone()[0]
   266	            for t in _CASE_TABLES}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:59.005Z

**tool call — Bash**
````
{
 "command": "cat -n app/db/schema.sql && echo ---- && cat -n tests/unit/test_db.py",
 "description": "Read schema.sql and test_db.py with line numbers"
}
````

### User / tool · 2026-11-02T02:14:59.087Z

**tool result**
````
     1	-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
     2	-- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
     3	-- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
     4	CREATE TABLE IF NOT EXISTS cases (
     5	  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
     6	  raw_text TEXT NOT NULL, text_sha256 TEXT,
     7	  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
     8	  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
     9	  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
    10	);
    11	CREATE TABLE IF NOT EXISTS records (
    12	  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
    13	  date_header_start INTEGER, date_header_end INTEGER, source_header_start INTEGER, source_header_end INTEGER,
    14	  source_label TEXT, date_raw TEXT, date_iso TEXT,
    15	  date_status TEXT CHECK (date_status IN ('parsed','ambiguous','missing','confirmed')),
    16	  date_candidates_json TEXT, duplicate_of TEXT, injection_tag INTEGER DEFAULT 0, encounter INTEGER DEFAULT 1,
    17	  PRIMARY KEY (case_id, id)
    18	);
    19	CREATE TABLE IF NOT EXISTS entries (
    20	  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
    21	  provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
    22	  state TEXT, state_reasons_json TEXT,
    23	  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
    24	  edited_json TEXT, ladder_json TEXT, updated_at REAL,
    25	  PRIMARY KEY (case_id, id)
    26	);
    27	CREATE TABLE IF NOT EXISTS amounts (
    28	  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
    29	  text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
    30	  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
    31	  state TEXT, state_reasons_json TEXT,
    32	  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
    33	  edited_json TEXT, ladder_json TEXT, updated_at REAL,
    34	  PRIMARY KEY (case_id, id)
    35	);
    36	CREATE TABLE IF NOT EXISTS flags (
    37	  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
    38	  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
    39	  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
    40	  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
    41	  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
    42	  state TEXT, state_reasons_json TEXT,
    43	  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
    44	  edited_json TEXT, ladder_json TEXT, updated_at REAL,
    45	  PRIMARY KEY (case_id, id)
    46	);
    47	-- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
    48	CREATE TABLE IF NOT EXISTS llm_calls (
    49	  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
    50	  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
    51	  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
    52	  parsed_ok INTEGER, verdict TEXT, attempt INTEGER DEFAULT 1, latency_ms INTEGER, cost_usd REAL,
    53	  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
    54	);
    55	CREATE TABLE IF NOT EXISTS review_events (
    56	  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
    57	  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
    58	  before_json TEXT, after_json TEXT, at REAL
    59	);
    60	CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
    61	CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
    62	CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
    63	CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
    64	CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
    65	CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
----
     1	"""Persistence, deletion, purge. ADR-006, R-PR-* privacy (delete_case = purge function), R-RV-5; db worker owns app/db."""
     2	import pytest
     3	from app.db import db as DB
     4	
     5	H24 = 24 * 3600
     6	
     7	@pytest.fixture
     8	def conn(tmp_path):
     9	    return DB.connect(str(tmp_path / "t.sqlite"))
    10	
    11	def seed(conn, now=1000.0):
    12	    cid = DB.create_case(conn, "SYNTHETIC raw text", now=now)
    13	    DB.add_item(conn, cid, "entry", {"summary": "x"}, now=now)
    14	    DB.add_llm_call(conn, cid, prompt="PROMPT with record text", response="RESPONSE", now=now)
    15	    return cid
    16	
    17	def test_delete_case_empties_every_table_including_prompts(conn):
    18	    """ADR-006 / privacy: delete_case removes the case from EVERY table (cases, records, items, llm_calls prompts, events)."""
    19	    cid = seed(conn)
    20	    other = seed(conn)
    21	    assert sum(DB.table_counts(conn, cid).values()) > 0
    22	    DB.delete_case(conn, cid)
    23	    assert sum(DB.table_counts(conn, cid).values()) == 0
    24	    assert sum(DB.table_counts(conn, other).values()) > 0      # other cases untouched
    25	
    26	def test_llm_calls_table_is_among_the_deleted(conn):
    27	    """ADR-006: stored prompts live in llm_calls and are covered by delete_case."""
    28	    cid = seed(conn)
    29	    assert DB.table_counts(conn, cid).get("llm_calls", 0) >= 1
    30	    DB.delete_case(conn, cid)
    31	    assert DB.table_counts(conn, cid).get("llm_calls", 0) == 0
    32	
    33	def test_purge_after_24h_with_injectable_now(conn):
    34	    """ADR-006: cases older than 24 h are purged lazily; `now` is injectable (no sleeping)."""
    35	    cid = seed(conn, now=1000.0)
    36	    assert DB.purge_expired(conn, now=1000.0 + H24 - 1) == 0
    37	    assert sum(DB.table_counts(conn, cid).values()) > 0
    38	    assert DB.purge_expired(conn, now=1000.0 + H24 + 1) == 1
    39	    assert sum(DB.table_counts(conn, cid).values()) == 0
    40	
    41	def test_purge_uses_the_same_deletion_path(conn):
    42	    """ADR-006: purge and DELETE are one function - a purged case leaves no row in any table (prompts included)."""
    43	    cid = seed(conn)
    44	    DB.purge_expired(conn, now=1000.0 + H24 + 1)
    45	    assert all(v == 0 for v in DB.table_counts(conn, cid).values())
    46	
    47	@pytest.mark.parametrize("status", ["pending", "accepted", "edited", "dismissed"])
    48	def test_review_status_round_trip(conn, status):
    49	    """R-RV-5 / ADR-005: review_status persists and reads back; new items start pending."""
    50	    cid = seed(conn)
    51	    iid = DB.add_item(conn, cid, "entry", {"summary": "y"})
    52	    assert DB.get_item(conn, iid)["review_status"] == "pending"
    53	    DB.set_review_status(conn, iid, status, edited={"summary": "z"} if status == "edited" else None)  # T-031 r2: edit needs a payload
    54	    assert DB.get_item(conn, iid)["review_status"] == status
    55	
    56	def test_invalid_review_status_rejected(conn):
    57	    """ADR-005: only pending|accepted|edited|dismissed are valid; nothing else is stored."""
    58	    cid = seed(conn); iid = DB.add_item(conn, cid, "entry", {})
    59	    with pytest.raises(ValueError):
    60	        DB.set_review_status(conn, iid, "auto_accepted")
    61	
    62	
    63	# --- added by db worker for T-031 round 2 (staff-engineer findings); qa may fold into its own layout ---
    64	import pathlib, re
    65	
    66	def _entry(conn, cid, **p):
    67	    return DB.add_item(conn, cid, "entry", {"summary": "orig", **p})
    68	
    69	def test_review_status_round_trip_new_connection(tmp_path):
    70	    """R-RV-8: status and the edit persist on a second connection; the original stays in its own column."""
    71	    path = str(tmp_path / "p.sqlite")
    72	    c1 = DB.connect(path); cid = DB.create_case(c1, "t", now=1); iid = _entry(c1, cid)
    73	    DB.apply_review(c1, iid, "edit", edited={"summary": "new"}, now=2); c1.close()
    74	    got = DB.get_item(DB.connect(path), iid)
    75	    assert got["review_status"] == "edited" and got["edited"] == {"summary": "new"} and got["summary"] == "orig"
    76	
    77	def test_ladder_roundtrip(tmp_path):
    78	    """AC2: D.4 ladder + backend, call ids and a recorded llm_calls row survive a new connection."""
    79	    path = str(tmp_path / "l.sqlite")
    80	    c1 = DB.connect(path); cid = DB.create_case(c1, "t", now=1)
    81	    call = DB.add_llm_call(c1, cid, prompt="u", response="r", now=2, system="s", role="judge", step="judge_entries",
    82	                           backend="fixture", model="m", prompt_version="judge_faithfulness_v1", verdict="supported",
    83	                           latency_ms=5, cost_usd=0.0, attempt=1)
    84	    ladder = {"item_id": "e1", "backend": "fixture", "generator": {"model": "g", "prompt_version": "extract_v1", "call_id": "c0"},
    85	              "code_checks": {"excerpt_verbatim": True}, "judge": {"verdict": "supported", "call_id": call},
    86	              "state": "verified", "human": {"action": None, "edited_text": None, "at": None}}
    87	    iid = _entry(c1, cid, ladder_json=ladder); c1.close()
    88	    c2 = DB.connect(path)
    89	    assert DB.get_item(c2, iid)["ladder"] == ladder
    90	    row = DB.get_llm_call(c2, call)
    91	    assert (row["backend"], row["model"], row["prompt_version"], row["verdict"], row["latency_ms"]) == ("fixture", "m", "judge_faithfulness_v1", "supported", 5)
    92	    assert len(row["prompt_sha256"]) == 64 and row["user_text"] == "u" and row["response_raw"] == "r"
    93	
    94	def test_apply_review_logs_before_after_and_keeps_original(conn):
    95	    cid = seed(conn); iid = _entry(conn, cid)
    96	    DB.apply_review(conn, iid, "edit", edited={"summary": "new"}, now=5)
    97	    DB.apply_review(conn, iid, "accept", now=6)
    98	    ev = DB.list_events(conn, cid, iid)
    99	    assert [e["action"] for e in ev] == ["edit", "accept"]
   100	    assert ev[0]["before"] == {"review_status": "pending", "edited": None}
   101	    assert ev[0]["after"] == {"review_status": "edited", "edited": {"summary": "new"}}
   102	    assert ev[1]["before"]["review_status"] == "edited" and ev[1]["after"]["review_status"] == "accepted"
   103	    assert DB.get_item(conn, iid)["summary"] == "orig"
   104	
   105	def test_edit_without_payload_raises(conn):
   106	    cid = seed(conn); iid = _entry(conn, cid)
   107	    for call in (lambda: DB.apply_review(conn, iid, "edit"), lambda: DB.set_review_status(conn, iid, "edited")):
   108	        with pytest.raises(ValueError):
   109	            call()
   110	    assert DB.get_item(conn, iid)["review_status"] == "pending" and DB.list_events(conn, cid) == []
   111	
   112	def test_update_item_cannot_write_edits_status_or_ids(conn):
   113	    cid = seed(conn); iid = _entry(conn, cid)
   114	    for bad in ({"edited_json": {"summary": "X"}}, {"edited": {"summary": "X"}}, {"id": "e999"}, {"review_status": "accepted"}, {"case_id": "z"}):
   115	        with pytest.raises(ValueError):
   116	            DB.update_item(conn, iid, **bad)
   117	    DB.update_item(conn, iid, state="verified", ladder={"backend": "fixture"}, now=3)       # allowed fields still work
   118	    assert DB.get_item(conn, iid)["ladder"] == {"backend": "fixture"} and DB.list_events(conn, cid) == []
   119	
   120	def test_secure_delete_is_on(conn):
   121	    assert conn.execute("PRAGMA secure_delete").fetchone()[0] == 1
   122	
   123	import ast
   124	
   125	_WRITE_RE = re.compile(r"\b(UPDATE|INSERT|REPLACE)\b.*\b(review_status|edited_json)\b", re.I | re.S)
   126	
   127	def _writer_sites(source: str):
   128	    """(function, sql) for every string literal / f-string in `source` that is an UPDATE/INSERT touching review_status or edited_json."""
   129	    out = []
   130	    tree = ast.parse(source)
   131	    docstrings = {id(n.body[0].value) for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.Module, ast.ClassDef))
   132	                  and n.body and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
   133	    def walk(node, fn):
   134	        if id(node) in docstrings:
   135	            return
   136	        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
   137	            fn = node.name
   138	        if isinstance(node, ast.JoinedStr):
   139	            sql = "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in node.values)
   140	            if _WRITE_RE.search(sql): out.append((fn, sql))
   141	            return
   142	        if isinstance(node, ast.Constant) and isinstance(node.value, str) and _WRITE_RE.search(node.value):
   143	            out.append((fn, node.value))
   144	        for ch in ast.iter_child_nodes(node):
   145	            walk(ch, fn)
   146	    walk(tree, None)
   147	    return out
   148	
   149	def test_review_status_only_via_apply_review():
   150	    """AC5: every SQL statement under app/ that writes review_status or edited_json (any position in SET, named or
   151	    positional params, f-strings) sits inside apply_review. AST scan, not a line grep."""
   152	    sites = []
   153	    for f in pathlib.Path("app").rglob("*.py"):
   154	        sites += [(str(f), fn) for fn, _ in _writer_sites(f.read_text())]
   155	    assert sites and all(f == "app/db/db.py" and fn == "apply_review" for f, fn in sites), sites
   156	
   157	@pytest.mark.parametrize("rogue", [
   158	    'conn.execute("UPDATE entries SET review_status=? WHERE id=?", (a, b))',
   159	    'conn.execute("UPDATE entries SET edited_json=?, review_status=:s WHERE id=:i", (a, b))',
   160	    'conn.execute(f"UPDATE {t} SET state=?, edited_json=? WHERE id=?", (a, b, c))',
   161	    'conn.execute("INSERT INTO entries (id, review_status) VALUES (?, ?)", (a, b))',
   162	])
   163	def test_writer_guard_catches_rogue_forms(rogue):
   164	    """The guard itself must not weaken: each rogue writer outside apply_review is detected."""
   165	    src = "def apply_review(): pass\ndef sneaky(conn):\n    " + rogue + "\n"
   166	    assert [fn for fn, _ in _writer_sites(src)] == ["sneaky"]
   167	
   168	def test_add_item_rejects_edits_and_status(conn):
   169	    cid = seed(conn)
   170	    before = DB.table_counts(conn, cid)["entries"]
   171	    for bad in ({"edited_json": {"summary": "X"}}, {"review_status": "accepted"}):
   172	        with pytest.raises(ValueError):
   173	            DB.add_item(conn, cid, "entry", bad)
   174	    assert DB.table_counts(conn, cid)["entries"] == before
   175	    assert DB.get_item(conn, _entry(conn, cid))["edited"] is None
   176	
   177	
   178	def test_log_only_actions_not_duplicate_and_manual_entry(conn):
   179	    """T-062: logged with before/after, status unchanged."""
   180	    cid = seed(conn); iid = _entry(conn, cid)
   181	    DB.apply_review(conn, iid, "not_duplicate", now=7)
   182	    DB.apply_review(conn, iid, "manual_entry", now=8)
   183	    ev = DB.list_events(conn, cid, iid)
   184	    assert [e["action"] for e in ev] == ["not_duplicate", "manual_entry"]
   185	    assert all(e["before"] == e["after"] == {"review_status": "pending", "edited": None} for e in ev)
   186	    assert DB.get_item(conn, iid)["review_status"] == "pending"
   187	
   188	def test_old_schema_file_is_rebuilt(tmp_path):
   189	    import sqlite3
   190	    path = str(tmp_path / "old.sqlite")
   191	    old = sqlite3.connect(path)
   192	    old.execute("CREATE TABLE review_events (id TEXT, action TEXT CHECK (action IN ('accept')))"); old.commit(); old.close()
   193	    c = DB.connect(path)
   194	    cid = DB.create_case(c, "t", now=1); iid = _entry(c, cid)
   195	    DB.apply_review(c, iid, "manual_entry", now=2)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:16.206Z

**tool call — Bash**
````
{
 "command": "echo \"== parent SCHEMA_VERSION lines\" && git show 5f8858f^:app/db/db.py | grep -n \"SCHEMA_VERSION\\|user_version\" && echo \"== parent schema.sql CHECK\" && git show 5f8858f^:app/db/schema.sql | grep -n \"review_events\" -A2 && echo \"== grep other action lists\" && grep -rn \"keep_my_wording\\|manual_entry\\|not_duplicate\" --include=*.py --include=*.md --include=*.js --include=*.ts --include=*.html . 2>/dev/null | grep -v \"\\.venv\\|node_modules\" | head -40",
 "description": "Check parent schema version and other action-name references"
}
````

### User / tool · 2026-11-02T02:15:16.390Z

**tool result**
````
== parent SCHEMA_VERSION lines
31:SCHEMA_VERSION = 2          # 1 = global ids (pre T-050); 2 = (case_id, id) keys
41:            version = probe.execute("PRAGMA user_version").fetchone()[0]
45:        if has_tables and version != SCHEMA_VERSION:
51:            log.warning("database schema version %s != %s: moved %s aside and rebuilt", version, SCHEMA_VERSION, os.path.basename(moved))
58:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
== parent schema.sql CHECK
55:CREATE TABLE IF NOT EXISTS review_events (
56-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
57-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording')),
--
65:CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
== grep other action lists
artifacts/review-evidence/T-014-r2-privacy-resolution.md:15:| M3 | No code check on numbers in summaries/edits (major) | ADR-012:236; LLM_VS_CODE row 15; api.md:242-249 `409 needs_confirm` + `warnings[]`, `keep_my_wording` event. | **Resolved** |
artifacts/review-evidence/T-040-r2/head_5650eae/evals/golden/README.md:63:                    "expected_state": "needs_review|no_new_warning","expected_reason","accept_requires_keep_my_wording_confirm"}],
artifacts/review-evidence/T-040-r2/head_5650eae/app/backend/export.py:118:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
artifacts/review-evidence/T-040-r2/head_5650eae/app/backend/store.py:64:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
artifacts/review-evidence/T-040-r2/head_5650eae/app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
artifacts/review-evidence/T-040-r2/head_5650eae/app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
artifacts/review-evidence/T-040-r2/head_5650eae/app/backend/review.py:128:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
artifacts/review-evidence/T-040-r2/head_5650eae/app/db/db.py:19:           "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
artifacts/review-evidence/T-040-r2/head_5650eae/memory/DECISIONS.md:94:review_events id, case_id, item_id, action('accept'|'edit'|'dismiss'|'reset'|'confirm_date'|'keep_my_wording'),
artifacts/review-evidence/T-040-r2/head_5650eae/memory/DECISIONS.md:153:  - **Edit re-check order (R-RV-3, D-006):** (1) structure, else 422. (2) Code token check (ADR-012). If it finds tokens not in the quote: `409 needs_confirm` with the warnings; nothing is saved; the client resends with `confirm_warnings: true`, which saves and logs `keep_my_wording`. (3) Judge 1 re-runs against the edited text. If it objects (`partially`/`unsupported`): the same `409 needs_confirm`. If the judge fails (error, timeout) or there is no recorded fixture for the edit (always the case in demo mode): the edit is saved and the item becomes `needs_review` with `JUDGE_UNAVAILABLE`, shown to her; the code check already passed. The judge never blocks the edit and never lets an unchecked edit look verified.
artifacts/review-evidence/T-040-r2/head_5650eae/memory/contracts/api.md:257:The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.
artifacts/review-evidence/T-040-r2/head_5650eae/board/cards/T-041.md:41:- 2026-11-02T01:51:48Z backend: Interface assumptions: case dict per tests/unit/test_export.build_case (records n/source/date_iso/excerpt; entries; amounts cents/cls; flags evidence/subtype); records may carry could_not_process|status=failed|reason; keep-my-wording read from case['events'] type keep_my_wording; build_export also returns counts (R-EX-5). pending_count key ignored (computed from items). Router app/backend/export_routes.py: set_case_loader(fn(token)->case|None); T-040 must register + provide the DB->case adapter. test_api::test_export_endpoint not present yet.
artifacts/review-evidence/T-040-r2/head_5650eae/tests/unit/test_review_rules.py:102:def test_keep_my_wording_resend_saves_and_logs(tmp_path):
artifacts/review-evidence/T-040-r2/head_5650eae/tests/unit/test_review_rules.py:103:    """R-RV-3: resend with confirm_warnings=true saves (review_status edited) and logs a keep_my_wording event."""
artifacts/review-evidence/T-040-r2/head_5650eae/tests/unit/test_export.py:161:    c["events"] = [dict(type="keep_my_wording", item_id="e3")]
artifacts/review-evidence/T-040-r2/head_5650eae/tests/e2e/test_edit.py:14:def test_added_dollar_warns_and_needs_keep_my_wording(page, sample_case):
artifacts/review-evidence/T-040-r2/head_099732b/evals/golden/README.md:63:                    "expected_state": "needs_review|no_new_warning","expected_reason","accept_requires_keep_my_wording_confirm"}],
artifacts/review-evidence/T-040-r2/head_099732b/app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
artifacts/review-evidence/T-040-r2/head_099732b/app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
artifacts/review-evidence/T-040-r2/head_099732b/app/backend/review.py:128:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
artifacts/review-evidence/T-040-r2/head_099732b/app/backend/export.py:118:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
artifacts/review-evidence/T-040-r2/head_099732b/app/db/db.py:19:           "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
artifacts/review-evidence/T-040-r2/head_099732b/app/backend/store.py:64:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
artifacts/review-evidence/T-040-r2/head_099732b/memory/contracts/api.md:258:The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.
artifacts/review-evidence/T-040-r2/head_099732b/memory/DECISIONS.md:94:review_events id, case_id, item_id, action('accept'|'edit'|'dismiss'|'reset'|'confirm_date'|'keep_my_wording'),
artifacts/review-evidence/T-040-r2/head_099732b/memory/DECISIONS.md:153:  - **Edit re-check order (R-RV-3, D-006):** (1) structure, else 422. (2) Code token check (ADR-012). If it finds tokens not in the quote: `409 needs_confirm` with the warnings; nothing is saved; the client resends with `confirm_warnings: true`, which saves and logs `keep_my_wording`. (3) Judge 1 re-runs against the edited text. If it objects (`partially`/`unsupported`): the same `409 needs_confirm`. If the judge fails (error, timeout) or there is no recorded fixture for the edit (always the case in demo mode): the edit is saved and the item becomes `needs_review` with `JUDGE_UNAVAILABLE`, shown to her; the code check already passed. The judge never blocks the edit and never lets an unchecked edit look verified.
artifacts/review-evidence/T-040-r2/head_099732b/board/cards/T-041.md:41:- 2026-11-02T01:51:48Z backend: Interface assumptions: case dict per tests/unit/test_export.build_case (records n/source/date_iso/excerpt; entries; amounts cents/cls; flags evidence/subtype); records may carry could_not_process|status=failed|reason; keep-my-wording read from case['events'] type keep_my_wording; build_export also returns counts (R-EX-5). pending_count key ignored (computed from items). Router app/backend/export_routes.py: set_case_loader(fn(token)->case|None); T-040 must register + provide the DB->case adapter. test_api::test_export_endpoint not present yet.
artifacts/review-evidence/T-040-r2/head_099732b/tests/unit/test_review_rules.py:102:def test_keep_my_wording_resend_saves_and_logs(tmp_path):
artifacts/review-evidence/T-040-r2/head_099732b/tests/unit/test_review_rules.py:103:    """R-RV-3: resend with confirm_warnings=true saves (review_status edited) and logs a keep_my_wording event."""
artifacts/review-evidence/T-040-r2/head_099732b/tests/unit/test_export.py:161:    c["events"] = [dict(type="keep_my_wording", item_id="e3")]
artifacts/review-evidence/T-040-r2/head_099732b/tests/e2e/test_edit.py:14:def test_added_dollar_warns_and_needs_keep_my_wording(page, sample_case):
artifacts/review-evidence/T-050/h1_head_plus_fixtures/evals/golden/README.md:63:                    "expected_state": "needs_review|no_new_warning","expected_reason","accept_requires_keep_my_wording_confirm"}],
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/backend/store.py:64:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/backend/export.py:112:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/backend/review.py:128:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
artifacts/review-evidence/T-050/h1_head_plus_fixtures/app/db/db.py:17:           "confirm_date": None, "keep_my_wording": None}          # None = logged only, status unchanged
artifacts/review-evidence/T-050/h1_head_plus_fixtures/memory/contracts/api.md:253:The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.
artifacts/review-evidence/T-050/h1_head_plus_fixtures/memory/DECISIONS.md:94:review_events id, case_id, item_id, action('accept'|'edit'|'dismiss'|'reset'|'confirm_date'|'keep_my_wording'),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:32.048Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-062/parent && git archive 5f8858f^ app tests | tar -x -C artifacts/review-evidence/T-062/parent && ls artifacts/review-evidence/T-062/parent && ls -a | grep -i \"conftest\\|pytest.ini\\|pyproject\\|setup.cfg\"; echo \"--- guard: rogue-writer scan on current app/\"; .venv/bin/python -m pytest tests/unit/test_db.py -v 2>&1 | grep -E \"log_only|old_schema|review_status_only|writer_guard|PASS|FAIL\" | head -30",
 "description": "Extract parent commit tree and run DB tests verbosely"
}
````

### User / tool · 2026-11-02T02:15:32.927Z

**tool result**
````
/bin/bash: child setpgid (54849 to 54849): Operation not permitted
app
tests
--- guard: rogue-writer scan on current app/
tests/unit/test_db.py::test_delete_case_empties_every_table_including_prompts PASSED [  4%]
tests/unit/test_db.py::test_llm_calls_table_is_among_the_deleted PASSED  [  8%]
tests/unit/test_db.py::test_purge_after_24h_with_injectable_now PASSED   [ 13%]
tests/unit/test_db.py::test_purge_uses_the_same_deletion_path PASSED     [ 17%]
tests/unit/test_db.py::test_review_status_round_trip[pending] PASSED     [ 21%]
tests/unit/test_db.py::test_review_status_round_trip[accepted] PASSED    [ 26%]
tests/unit/test_db.py::test_review_status_round_trip[edited] PASSED      [ 30%]
tests/unit/test_db.py::test_review_status_round_trip[dismissed] PASSED   [ 34%]
tests/unit/test_db.py::test_invalid_review_status_rejected PASSED        [ 39%]
tests/unit/test_db.py::test_review_status_round_trip_new_connection PASSED [ 43%]
tests/unit/test_db.py::test_ladder_roundtrip PASSED                      [ 47%]
tests/unit/test_db.py::test_apply_review_logs_before_after_and_keeps_original PASSED [ 52%]
tests/unit/test_db.py::test_edit_without_payload_raises PASSED           [ 56%]
tests/unit/test_db.py::test_update_item_cannot_write_edits_status_or_ids PASSED [ 60%]
tests/unit/test_db.py::test_secure_delete_is_on PASSED                   [ 65%]
tests/unit/test_db.py::test_review_status_only_via_apply_review PASSED   [ 69%]
tests/unit/test_db.py::test_writer_guard_catches_rogue_forms[conn.execute("UPDATE entries SET review_status=? WHERE id=?", (a, b))] PASSED [ 73%]
tests/unit/test_db.py::test_writer_guard_catches_rogue_forms[conn.execute("UPDATE entries SET edited_json=?, review_status=:s WHERE id=:i", (a, b))] PASSED [ 78%]
tests/unit/test_db.py::test_writer_guard_catches_rogue_forms[conn.execute(f"UPDATE {t} SET state=?, edited_json=? WHERE id=?", (a, b, c))] PASSED [ 82%]
tests/unit/test_db.py::test_writer_guard_catches_rogue_forms[conn.execute("INSERT INTO entries (id, review_status) VALUES (?, ?)", (a, b))] PASSED [ 86%]
tests/unit/test_db.py::test_add_item_rejects_edits_and_status PASSED     [ 91%]
tests/unit/test_db.py::test_log_only_actions_not_duplicate_and_manual_entry PASSED [ 95%]
tests/unit/test_db.py::test_old_schema_file_is_rebuilt PASSED            [100%]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:38.158Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-062/repro_stale_schema.py",
 "content": "\"\"\"T-062 reviewer probe: a DB file written by pre-T-062 code (user_version=2, old review_events CHECK)\nopened by post-T-062 code. Usage:\n  python repro_stale_schema.py <code_root> old <db_path>   # write a file with the parent code\n  python repro_stale_schema.py <code_root> new <db_path>   # open it with the new code, apply manual_entry\n\"\"\"\nimport sys\n\nroot, stage, path = sys.argv[1], sys.argv[2], sys.argv[3]\nsys.path.insert(0, root)\nfrom app.db import db as DB  # noqa: E402\n\nif stage == \"old\":\n    c = DB.connect(path)\n    cid = DB.create_case(c, \"SYNTHETIC\", now=1)\n    iid = DB.add_item(c, cid, \"entry\", {\"summary\": \"orig\"})\n    DB.apply_review(c, iid, \"accept\", now=2)\n    print(\"old: user_version =\", c.execute(\"PRAGMA user_version\").fetchone()[0])\n    print(\"old: SCHEMA_VERSION in code =\", DB.SCHEMA_VERSION)\n    print(\"old: review_events CHECK has manual_entry:\",\n          \"manual_entry\" in (c.execute(\"SELECT sql FROM sqlite_master WHERE name='review_events'\").fetchone()[0]))\n    c.close()\nelse:\n    c = DB.connect(path)\n    print(\"new: user_version =\", c.execute(\"PRAGMA user_version\").fetchone()[0])\n    print(\"new: review_events CHECK has manual_entry:\",\n          \"manual_entry\" in (c.execute(\"SELECT sql FROM sqlite_master WHERE name='review_events'\").fetchone()[0]))\n    iid = c.execute(\"SELECT id FROM entries LIMIT 1\").fetchone()[0]\n    try:\n        DB.apply_review(c, iid, \"manual_entry\", now=3)\n        print(\"new: manual_entry OK; events:\", [e[\"action\"] for e in DB.list_events(c, c.execute(\"SELECT case_id FROM entries LIMIT 1\").fetchone()[0])])\n    except Exception as e:  # probe only: show what the caller would see\n        print(\"new: manual_entry RAISED\", type(e).__name__, \"-\", e)\n"
}
````

### User / tool · 2026-11-02T02:15:38.252Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-062/repro_stale_schema.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:39.539Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-062 && rm -f $R/stale.sqlite* && echo \"== stage old (parent code 5f8858f^)\" && .venv/bin/python $R/repro_stale_schema.py $PWD/$R/parent old $PWD/$R/stale.sqlite && echo \"== stage new (current HEAD code)\" && .venv/bin/python $R/repro_stale_schema.py $PWD $R/../../../$R/stale.sqlite new 2>&1; echo \"exit=$?\"; echo \"== fresh-file sanity: new code, no old file\" && rm -f $R/fresh.sqlite && .venv/bin/python $R/repro_stale_schema.py $PWD new $PWD/$R/fresh.sqlite 2>&1 | tail -3",
 "description": "Reproduce stale version-2 file against new code"
}
````

### User / tool · 2026-11-02T02:15:39.771Z

**tool result**
````
== stage old (parent code 5f8858f^)
old: user_version = 2
old: SCHEMA_VERSION in code = 2
old: review_events CHECK has manual_entry: False
== stage new (current HEAD code)
new: user_version = 2
new: review_events CHECK has manual_entry: True
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-062/repro_stale_schema.py", line 27, in <module>
    iid = c.execute("SELECT id FROM entries LIMIT 1").fetchone()[0]
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
TypeError: 'NoneType' object is not subscriptable
exit=1
== fresh-file sanity: new code, no old file
    iid = c.execute("SELECT id FROM entries LIMIT 1").fetchone()[0]
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
TypeError: 'NoneType' object is not subscriptable
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:47.884Z

**tool call — Bash**
````
{
 "command": "ls -la | grep -E \" new| new\\b|\\.old-\" ; git status --short | head -20; git check-ignore -v new 2>/dev/null; echo \"tracked? $(git ls-files --error-unmatch new 2>/dev/null || echo no)\"",
 "description": "Find stray database file created by mis-ordered probe args"
}
````

### User / tool · 2026-11-02T02:15:48.050Z

**tool result**
````
-rw-r--r--@   1 arsis  staff  94208 Nov  1 20:15 new
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M app/backend/ingest.py
 M app/backend/pipeline.py
tracked? no
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:51.374Z

**tool call — Bash**
````
{
 "command": "rm -f /Users/arsis/zlayt-pm-project/new && ls -la /Users/arsis/zlayt-pm-project | grep -c \" new$\"; echo \"== uncommitted changes in T-062 files:\"; git diff --stat HEAD -- app/db tests/unit/test_db.py; echo \"(end)\"; git status --short -- app/db tests/unit/test_db.py; echo \"(end status)\"; git rev-parse --short HEAD",
 "description": "Remove stray probe file and confirm T-062 files match HEAD"
}
````

### User / tool · 2026-11-02T02:15:51.434Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (rm /Users/arsis/zlayt-pm-project/new)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:55.815Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-062 && A=/Users/arsis/zlayt-pm-project && rm -f $R/stale.sqlite* $R/control.sqlite* && echo \"== 1. write stale file with parent code (5f8858f^), user_version=2 but old CHECK\" && .venv/bin/python $R/repro_stale_schema.py $A/$R/parent old $A/$R/stale.sqlite && echo \"== 2. open that stale file with HEAD code, apply manual_entry\" && .venv/bin/python $R/repro_stale_schema.py $A new $A/$R/stale.sqlite; echo \"exit=$?\"; echo \"== 3. control: file written by HEAD code, then manual_entry\" && .venv/bin/python $R/repro_stale_schema.py $A old $A/$R/control.sqlite && .venv/bin/python $R/repro_stale_schema.py $A new $A/$R/control.sqlite; echo \"exit=$?\"",
 "description": "Rerun stale-schema probe with correct argument order and control"
}
````

### User / tool · 2026-11-02T02:15:56.115Z

**tool result**
````
== 1. write stale file with parent code (5f8858f^), user_version=2 but old CHECK
old: user_version = 2
old: SCHEMA_VERSION in code = 2
old: review_events CHECK has manual_entry: False
== 2. open that stale file with HEAD code, apply manual_entry
new: user_version = 2
new: review_events CHECK has manual_entry: False
new: manual_entry RAISED IntegrityError - CHECK constraint failed: action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording')
exit=0
== 3. control: file written by HEAD code, then manual_entry
old: user_version = 2
old: SCHEMA_VERSION in code = 2
old: review_events CHECK has manual_entry: True
new: user_version = 2
new: review_events CHECK has manual_entry: True
new: manual_entry OK; events: ['accept', 'manual_entry']
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:04.873Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-062/mutate.py",
 "content": "\"\"\"T-062 reviewer mutation probe. Copies app/ and tests/ into scratch dirs under this folder, applies one\nmutation per dir, runs tests/unit/test_db.py there with the repo venv, and prints the pass/fail summary.\nRepo files are never modified.\"\"\"\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nREPO = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nOUT = REPO / \"artifacts/review-evidence/T-062/mut\"\nPY = str(REPO / \".venv/bin/python\")\n\nMUTANTS = {\n    # M1: drop the new DROP-TABLE loop in connect(); if the test still passes, it does not prove the T-062 change.\n    \"m1_no_drop_loop\": (\n        \"app/db/db.py\",\n        \"    if conn.execute(\\\"PRAGMA user_version\\\").fetchone()[0] != SCHEMA_VERSION:\\n\"\n        \"        for r in conn.execute(\\\"SELECT name FROM sqlite_master WHERE type IN ('table','index') AND name NOT LIKE 'sqlite_%'\\\").fetchall():\\n\"\n        \"            if r[\\\"name\\\"] and not r[\\\"name\\\"].startswith(\\\"ix_\\\"):\\n\"\n        \"                conn.execute(f\\\"DROP TABLE IF EXISTS {r['name']}\\\")\\n\",\n        \"\",\n    ),\n    # M2: manual_entry sets review_status to accepted; log-only invariant must fail a test.\n    \"m2_manual_entry_accepts\": (\n        \"app/db/db.py\",\n        \"\\\"not_duplicate\\\": None, \\\"manual_entry\\\": None}\",\n        \"\\\"not_duplicate\\\": None, \\\"manual_entry\\\": \\\"accepted\\\"}\",\n    ),\n    # M3: not_duplicate sets review_status to dismissed.\n    \"m3_not_duplicate_dismisses\": (\n        \"app/db/db.py\",\n        \"\\\"not_duplicate\\\": None, \\\"manual_entry\\\": None}\",\n        \"\\\"not_duplicate\\\": \\\"dismissed\\\", \\\"manual_entry\\\": None}\",\n    ),\n    # M4: remove the new actions from the schema CHECK (the AC's CHECK requirement).\n    \"m4_schema_check_missing\": (\n        \"app/db/schema.sql\",\n        \",'not_duplicate','manual_entry')\",\n        \")\",\n    ),\n    # M5: log-only action writes no event row.\n    \"m5_no_event_for_manual_entry\": (\n        \"app/db/db.py\",\n        \"    conn.execute(\\\"BEGIN\\\")\\n    try:\\n        conn.execute(f\\\"UPDATE {table} SET review_status=?\",\n        \"    if action == 'manual_entry':\\n        return get_item(conn, item_id, row['case_id'])\\n    conn.execute(\\\"BEGIN\\\")\\n    try:\\n        conn.execute(f\\\"UPDATE {table} SET review_status=?\",\n    ),\n}\n\nfor name, (rel, old, new) in MUTANTS.items():\n    d = OUT / name\n    if d.exists():\n        shutil.rmtree(d)\n    d.mkdir(parents=True)\n    for sub in (\"app\", \"tests\"):\n        shutil.copytree(REPO / sub, d / sub, ignore=shutil.ignore_patterns(\"__pycache__\"))\n    target = d / rel\n    src = target.read_text(encoding=\"utf-8\")\n    n = src.count(old)\n    if n != 1:\n        print(f\"{name}: SKIPPED, anchor found {n} times\")\n        continue\n    target.write_text(src.replace(old, new), encoding=\"utf-8\")\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"tests/unit/test_db.py\", \"-q\", \"-p\", \"no:cacheprovider\"],\n                       cwd=str(d), capture_output=True, text=True)\n    summary = (r.stdout.strip().splitlines() or [\"<no output>\"])[-1]\n    failed = [l.split(\"::\", 1)[1].split(\" \")[0] for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n    print(f\"{name}: {summary}\")\n    for f in failed:\n        print(f\"    FAILED {f}\")\n"
}
````

### User / tool · 2026-11-02T02:16:04.996Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-062/mutate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:06.106Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-062/mutate.py 2>&1 | tail -40",
 "description": "Run mutation probes on scratch copies of db.py and schema"
}
````

### User / tool · 2026-11-02T02:16:09.778Z

**tool result**
````
m1_no_drop_loop: 23 passed in 0.31s
m2_manual_entry_accepts: 1 failed, 22 passed in 0.31s
    FAILED test_log_only_actions_not_duplicate_and_manual_entry
m3_not_duplicate_dismisses: 1 failed, 22 passed in 0.32s
    FAILED test_log_only_actions_not_duplicate_and_manual_entry
m4_schema_check_missing: 2 failed, 21 passed in 0.40s
    FAILED test_log_only_actions_not_duplicate_and_manual_entry
    FAILED test_old_schema_file_is_rebuilt
m5_no_event_for_manual_entry: 1 failed, 22 passed in 0.33s
    FAILED test_log_only_actions_not_duplicate_and_manual_entry
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:20.474Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i \"T-031\\|T-061\\|T-048\" ; echo \"== persona field in an existing staff review:\"; f=$(ls reviews/*staff* 2>/dev/null | head -1); echo \"$f\"; grep -o '\"persona\": \"[^\"]*\"' \"$f\" | head -1; grep -o '\"model\": \"[^\"]*\"' \"$f\" | head -1; echo \"== docs mentions of schema version / user_version / log-only:\"; grep -rn \"user_version\\|SCHEMA_VERSION\\|schema version\\|log-only\\|log only\" docs/ memory/ 2>/dev/null | head -12",
 "description": "Check existing review format and docs on schema versioning"
}
````

### User / tool · 2026-11-02T02:16:20.602Z

**tool result**
````
T-031-staff-engineer-r2.md
T-031-staff-engineer.md
T-048-staff-engineer-r2.md
T-048-staff-engineer.md
== persona field in an existing staff review:
reviews/CONTRACT-M2M3-staff-engineer.md
"persona": "staff-engineer-reviewer"
"model": "claude-opus-5-5"
== docs mentions of schema version / user_version / log-only:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:09.556Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-062-staff-engineer.md",
 "content": "# T-062 staff-engineer review\n\nScope: commit 5f8858f (parent 5f8858f^) touching app/db/db.py, app/db/schema.sql, tests/unit/test_db.py. DB-only card, no app URL, no sample case.\n\nVerdict: **fail**. AC 1 says \"schema version bumped so old files rebuild\". The version was not bumped (it is still 2), so a review_events file written before this commit keeps the old CHECK and rejects the two new actions with an IntegrityError. The AC test passes without the rebuild code it names, so it does not prove the claim.\n\nWhat holds: the log-only actions write one event row with before/after and never change review_status. The AST writer guard is unchanged and passes.\n\nProbe housekeeping (not a finding on the artifact): one probe run with swapped arguments created an untracked SQLite file at `/Users/arsis/zlayt-pm-project/new` (94208 bytes, 20:15). The board-guard hook blocked my `rm` of it, so I did not remove it. It needs deleting by the orchestrator or Chris. It is not part of the commit.\n\nEvidence files (under the allowed path): `artifacts/review-evidence/T-062/repro_stale_schema.py`, `artifacts/review-evidence/T-062/mutate.py`, `artifacts/review-evidence/T-062/parent/` (git archive of 5f8858f^ app and tests), `artifacts/review-evidence/T-062/mut/`.\n\n```json\n{\"card\": \"T-062\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 5f8858f (parent 5f8858f^); app/db/db.py, app/db/schema.sql, tests/unit/test_db.py; no app URL (DB-only card); no sample case\",\n \"exercised\": [\n   \"python3 tools/board.py show T-062 -> status in_review; AC 1 done=true, evidence cites 23 passed and SCHEMA_VERSION=2\",\n   \".venv/bin/python -m pytest tests/unit/test_db.py -q 2>&1 | tail -2 -> '23 passed in 0.27s'\",\n   \".venv/bin/python -m pytest tests/unit/test_db.py -v -> PASSED for test_log_only_actions_not_duplicate_and_manual_entry, test_old_schema_file_is_rebuilt, test_review_status_only_via_apply_review, and all 4 test_writer_guard_catches_rogue_forms params\",\n   \"git show 5f8858f -- app/db/db.py app/db/schema.sql tests/unit/test_db.py (full diff read)\",\n   \"git show 5f8858f^:app/db/db.py | grep -n 'SCHEMA_VERSION\\\\|user_version' -> 31:SCHEMA_VERSION = 2 ; 58:PRAGMA user_version (version was already 2 before the commit)\",\n   \"git archive 5f8858f^ app tests | tar -x -C artifacts/review-evidence/T-062/parent (parent tree for stale-file probe)\",\n   \"artifacts/review-evidence/T-062/repro_stale_schema.py: old stage on parent -> 'user_version = 2', 'CHECK has manual_entry: False'; new stage on the stale file -> 'manual_entry RAISED IntegrityError - CHECK constraint failed: action IN (accept,edit,dismiss,reset,confirm_date,keep_my_wording)'; control (file written by HEAD) -> 'manual_entry OK; events: [accept, manual_entry]'\",\n   \"artifacts/review-evidence/T-062/mutate.py (scratch copies, repo unmodified): m1 delete DROP loop db.py:58-61 -> 23 passed; m2 manual_entry->accepted -> 1 failed (log_only test); m3 not_duplicate->dismissed -> 1 failed; m4 schema CHECK without new actions -> 2 failed (log_only, old_schema_rebuilt); m5 no event row for manual_entry -> 1 failed\",\n   \"grep for SCHEMA_VERSION, user_version, schema version, log-only in docs/ and memory/ -> no matches (no doc states the bump rule)\",\n   \"Read app/db/db.py, app/db/schema.sql, tests/unit/test_db.py in full with line numbers\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"ac1_schema_bump_and_rebuild\": 1, \"log_only_events_before_after\": 5, \"log_only_status_never_accepted\": 5, \"ast_writer_guard_intact\": 5, \"tests_prove_ac1_claim\": 2},\n \"findings\": [\n   {\"severity\": \"blocker\",\n    \"title\": \"AC 1 'schema version bumped so old files rebuild' is not met; version-2 files keep the old CHECK and reject the new actions\",\n    \"evidence\": \"app/db/db.py:25 and app/db/db.py:33 both read 'SCHEMA_VERSION = 2'; git show 5f8858f^:app/db/db.py shows 'SCHEMA_VERSION = 2' already at line 31, so the value did not change. app/db/schema.sql:57 adds 'not_duplicate','manual_entry' to the review_events CHECK with no version bump. Repro (from repo root): .venv/bin/python artifacts/review-evidence/T-062/repro_stale_schema.py $PWD/artifacts/review-evidence/T-062/parent old $PWD/artifacts/review-evidence/T-062/stale.sqlite, then .venv/bin/python artifacts/review-evidence/T-062/repro_stale_schema.py $PWD new $PWD/artifacts/review-evidence/T-062/stale.sqlite prints 'new: user_version = 2', 'new: review_events CHECK has manual_entry: False', 'new: manual_entry RAISED IntegrityError - CHECK constraint failed: action IN (...)'. Control: a file written by HEAD code accepts manual_entry.\",\n    \"why_it_matters\": \"The AC names the bump as the mechanism that makes old files rebuild. Without it, connect() (db.py:47 and db.py:58) treats a pre-T-062 file as current and does not move it aside. Any review action of the new kind on that file raises IntegrityError. The failure is loud and the UPDATE and INSERT share one transaction (db.py:197-206), so nothing is half-written, but the AC is not met and the card evidence ('SCHEMA_VERSION=2 via PRAGMA user_version') describes an unchanged value. The schema.sql comment at db.py:25 says 'bump on any schema.sql change', which this commit breaks.\",\n    \"fix\": \"Set the one SCHEMA_VERSION to 3 (see finding 3 for the duplicate). The existing move-aside at db.py:47-53 then rebuilds any version-2 file.\",\n    \"acceptance_test\": \"New test: write a file with PRAGMA user_version=2 and the pre-T-062 review_events CHECK (literal CREATE TABLE is enough), call DB.connect(path), assert a '<path>.old-*' sibling exists and DB.apply_review(conn, iid, 'manual_entry', now=2) succeeds with events ['manual_entry']. Red on 5f8858f, green after the bump. Re-run repro_stale_schema.py new step: must print 'manual_entry OK'.\"},\n   {\"severity\": \"major\",\n    \"title\": \"test_old_schema_file_is_rebuilt does not exercise the T-062 rebuild code; the AC test passes without it\",\n    \"evidence\": \"tests/unit/test_db.py:188-195 creates a file with no user_version (0), so the pre-existing move-aside at app/db/db.py:47-53 handles it and the new DROP loop at db.py:58-61 is never the cause. Mutant m1 (DROP loop deleted, scratch copy artifacts/review-evidence/T-062/mut/m1_no_drop_loop) gives '.venv/bin/python -m pytest tests/unit/test_db.py -q' -> '23 passed in 0.31s'. Repro: .venv/bin/python artifacts/review-evidence/T-062/mutate.py prints 'm1_no_drop_loop: 23 passed in 0.31s'.\",\n    \"why_it_matters\": \"The AC 1 evidence is the only proof of the rebuild claim, and it passes with the code it names removed. Per persona 13 and section 7.3, a test that cannot fail on the claimed behaviour does not prove it.\",\n    \"fix\": \"Make the test use a version-2 file with the old CHECK (see finding 1) so the version comparison is what is under test. Assert the move-aside sibling exists.\",\n    \"acceptance_test\": \"Mutant A: SCHEMA_VERSION reverted to 2 -> the new test fails. Mutant B: the bump is kept but db.py:47-53 deleted -> the new test fails. Run via artifacts/review-evidence/T-062/mutate.py with those two mutants added.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"Duplicate SCHEMA_VERSION definition and an effectively dead DROP loop\",\n    \"evidence\": \"app/db/db.py:25 'SCHEMA_VERSION = 2   # bump on any schema.sql change; ...' (added by this commit) and app/db/db.py:33 'SCHEMA_VERSION = 2  # 1 = global ids (pre T-050); 2 = (case_id, id) keys' (pre-existing). The DROP loop at db.py:58-61 runs only when user_version != 2. Any file that has tables and a mismatched version is already moved aside at db.py:47-53, so the loop sees an empty file. I could not find an input where it drops anything the move-aside has not already moved.\",\n    \"why_it_matters\": \"Two constants with one name invite a half-edit: bump one and the other wins at import. The dead loop reads like a second rebuild mechanism and is part of why the missing bump in finding 1 was not noticed.\",\n    \"fix\": \"Keep one SCHEMA_VERSION definition. Delete the DROP loop (db.py:58-61), since the move-aside already covers the case.\",\n    \"acceptance_test\": \"grep -c '^SCHEMA_VERSION' app/db/db.py prints 1. The finding 2 test stays red when the version is reverted.\"}\n ],\n \"whats_right\": [\n   \"Log-only actions map to None in ACTIONS (db.py:18-20) and apply_review keeps the current status (db.py:192); mutants m2 and m3 that change the status are caught by test_log_only_actions_not_duplicate_and_manual_entry.\",\n   \"Each log-only action writes a review_events row with before and after in the same transaction (db.py:197-203); test_db.py:178-186 asserts the pair, and mutant m5 that drops the row is caught.\",\n   \"The AST writer guard (test_db.py:123-166) is unchanged and passes, and the new SQL added by this commit (DROP TABLE, PRAGMA) does not match its regex.\"\n ],\n \"questions_for_chris\": [\"Do any review databases survive a deploy on the demo or dev machine (retention is 24 h, db.py:16)? This affects how urgent finding 1 is, not whether it violates AC 1.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T02:17:09.799Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-062-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:12.868Z

**tool call — Bash**
````
{
 "command": "awk '/^```json/{f=1;next}/^```/{f=0}f' reviews/T-062-staff-engineer.md | python3 -c \"import json,sys; d=json.load(sys.stdin); print('json ok; verdict', d['verdict'], '; blockers', sum(f['severity']=='blocker' for f in d['findings']), '; majors', sum(f['severity']=='major' for f in d['findings']))\"; python3 tools/board.py validate 2>&1 | grep -i \"T-062\\|error\\|ok\\|pass\" | head -10",
 "description": "Parse review JSON and run board validator read-only"
}
````

### User / tool · 2026-11-02T02:17:13.041Z

**tool result**
````
json ok; verdict fail ; blockers 1 ; majors 1
ok (62 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:16.104Z

T-062 verdict is fail (1 blocker, 1 major): the schema version was never bumped, so pre-T-062 DB files reject the new actions with IntegrityError; review at /Users/arsis/zlayt-pm-project/reviews/T-062-staff-engineer.md. I also left a stray untracked SQLite file at /Users/arsis/zlayt-pm-project/new from a mis-ordered probe argument, and the board-guard blocked my rm, so please delete it.
