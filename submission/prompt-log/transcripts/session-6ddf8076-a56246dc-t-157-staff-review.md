# Subagent: T-157 staff review (T-157 staff review)

Source: `agent-a56246dcea22b2326.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:47:14.792Z

Review board card T-157 (commit 926bf37) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-157` and memory/contracts/api.md.

On a `git archive HEAD` copy:
- **Case names.** Check title on create, PATCH rename, and a default title derived from the first record header that is never "Untitled case". Check that titles are validated for length and HTML, and are local-only.
- **rerun_available.** It must be false in demo or fixture mode and after a rerun that got no answer.
- **next_action.** It must be deterministic: gate blockers first, then needs-review items in timeline order.
- **case_list.** The drift test must cover the new fields.

Run tests/unit/test_case_list.py and the unit suite.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-157-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:16.181Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T14:47:16.203Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:16.761Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-157 && echo ---- && cat memory/contracts/api.md && echo ---- && git log --oneline -3 && git cat-file -t 926bf37",
 "description": "Show card T-157, API contract, recent git log"
}
````

### User / tool · 2026-11-02T14:47:16.961Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:19.983Z

**tool call — Bash**
````
{
 "command": "git rev-parse --show-toplevel && git rev-parse HEAD && git log --oneline -3 && git cat-file -t 926bf37 && git show --stat 926bf37 | head -40",
 "description": "Check git HEAD and commit 926bf37 contents"
}
````

### User / tool · 2026-11-02T14:47:20.276Z

**tool result**
````
/Users/arsis/zlayt-pm-project
926bf375bf2c1a0272d6db466f1e3c18798bf90d
926bf37 feat(backend): T-157 case titles (title on create, PATCH rename, default from first record header), item.rerun_available, next_action on case list and GET case
52ac285 fix(backend): T-141 r5 date distance never exempts a mechanism word; injury prevention is not an event
20b3a42 test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
commit
commit 926bf375bf2c1a0272d6db466f1e3c18798bf90d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:46:52 2026 -0600

    feat(backend): T-157 case titles (title on create, PATCH rename, default from first record header), item.rerun_available, next_action on case list and GET case
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py           |  29 ++++++++--
 app/backend/case_list.py     |  91 +++++++++++++++++++++++++++--
 app/backend/present.py       |   7 +++
 app/backend/store.py         |  10 ++++
 memory/contracts/api.md      |  12 +++-
 tests/unit/test_case_list.py | 133 ++++++++++++++++++++++++++++++++++++++++++-
 6 files changed, 268 insertions(+), 14 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:20.314Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/bo6johie8.txt"
}
````

### User / tool · 2026-11-02T14:47:20.507Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:26.249Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; echo \"---\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; mkdir -p \"$S/t157-r1/archive\" && git archive 926bf37 | tar -x -C \"$S/t157-r1/archive\" && ls \"$S/t157-r1/archive\" | head -50; echo \"---\"; git show 926bf37 -- app/backend/api.py app/backend/case_list.py app/backend/present.py app/backend/store.py",
 "description": "Check working tree status, archive HEAD into scratch, show backend diff"
}
````

### User / tool · 2026-11-02T14:47:27.315Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
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
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
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
---
commit 926bf375bf2c1a0272d6db466f1e3c18798bf90d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:46:52 2026 -0600

    feat(backend): T-157 case titles (title on create, PATCH rename, default from first record header), item.rerun_available, next_action on case list and GET case
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index c48b2a6..ca1e6ea 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -245,10 +245,11 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
         if not isinstance(text, str):
             raise ApiError(400, "bad_request", "Provide text or sample: true.")
-        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
+        given = b.get("title") if isinstance(b.get("title"), str) else b.get("name")          # T-157: `title` is the name a paralegal types; `name` stays accepted
+        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample)
 
     @app.post("/api/cases/pdf", status_code=201)
-    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
+    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
         """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
         refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
         if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
@@ -275,7 +276,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
                 raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
             raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                            (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
-        out = make_case(got["text"], name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
+        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
         out["pdf_checks"] = got.get("pdf_checks")
         return out
 
@@ -291,7 +292,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             now = time.time()
             DB.purge_expired(c, now)
             name = name if isinstance(name, str) else ("Sample case" if sample else None)
-            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
+            cid = DB.create_case(c, text, now=now, name=case_list.clean_title(name) or None,
                                  source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                  **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
             try:
@@ -304,7 +305,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
                     raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, *language.api_fields(e)) from None
                 log.error("create failed %s", type(e).__name__)
                 raise ApiError(500, "internal", "Something went wrong.") from None
-            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
+            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
                     "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                     "dates_to_confirm": present.dates_to_confirm(c, cid),
                     "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
@@ -316,9 +317,25 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     @app.get("/api/cases/{token}")
     def get_case_view(token: str):
         c = conn()
+        try:
+            case = get_case(c, token)
+            v = present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
+            return {**v, "title": case_list.case_title(c, case), "next_action": case_list.next_action(c, token, case)}          # T-157
+        finally:
+            c.close()
+
+    @app.patch("/api/cases/{token}")
+    async def rename_case(token: str, request: Request):
+        """T-157: body {title}. A blank or null title clears the name: the title goes back to the one derived from the first record header."""
+        b = await body_of(request)
+        if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
+            raise ApiError(400, "bad_request", "Send {\"title\": text}.")
+        c = conn()
         try:
             get_case(c, token)
-            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
+            DB.update_case(c, token, name=case_list.clean_title(b["title"]) or None)
+            case = DB.get_case(c, token)
+            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
         finally:
             c.close()
 
diff --git a/app/backend/case_list.py b/app/backend/case_list.py
index 34df4f1..9e27bba 100644
--- a/app/backend/case_list.py
+++ b/app/backend/case_list.py
@@ -20,8 +20,34 @@ _LIB_PREFIX = re.compile(r"^case[ _](?:lib)?\d+[ _]", re.IGNORECASE)      # eval
 _EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)
 
 
+MAX_TITLE = 120
+_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u2028\u2029]")
+
+
+def clean_title(value) -> str:
+    """T-157: a case name as typed: control characters and line breaks become spaces, runs of white space collapse, at most 120 characters. '' when nothing is left."""
+    return re.sub(r"\s+", " ", _CTRL.sub(" ", value if isinstance(value, str) else "")).strip()[:MAX_TITLE].strip()
+
+
+def derived_title(conn, case_id) -> str:
+    """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
+    None when no record has either."""
+    for r in conn.execute("SELECT source_label, date_iso FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
+        label = clean_title(r["source_label"])[:60].strip()
+        try:
+            day = datetime.date.fromisoformat(r["date_iso"]).strftime("%b %-d, %Y") if r["date_iso"] else None
+        except ValueError:
+            day = None
+        if label:
+            return f"{label}, {day}" if day else label
+        if day:
+            return f"Records from {day}"
+    return None
+
+
 def readable_title(name, source, created_at) -> str:
-    """A name a paralegal would recognise. A file name or slug ("smith_records-2024.pdf") becomes words; no name at all becomes "Untitled case" with its date."""
+    """A name a paralegal would recognise. A file name or slug ("smith_records-2024.pdf") becomes words; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case";
+    `case_title` prefers the first record header over this fallback)."""
     n = _LIB_PREFIX.sub("", (name or "").strip())
     if n and (_SLUG.match(n) or n != (name or "").strip()) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
         n = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", _EXT.sub("", n))).strip()
@@ -29,7 +55,14 @@ def readable_title(name, source, created_at) -> str:
     if n:
         return n
     day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
-    return ("Sample case" if source == "sample" else "Untitled case") + (f", {day}" if source != "sample" else "")
+    return "Sample case" if source == "sample" else f"Records added {day}"
+
+
+def case_title(conn, case: dict) -> str:
+    """What to show for a case: its name made readable; else the first record header (provider and date); else the date it was added. Never "Untitled case"."""
+    if (case["name"] or "").strip():
+        return readable_title(case["name"], case["source"], case["created_at"])
+    return derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])
 
 
 def run_progress(case: dict, stages) -> tuple:
@@ -57,6 +90,56 @@ def _gate(conn, case_id) -> dict:
             "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}
 
 
+_RANK = {"entry": 0, "flag": 1, "amount": 2}
+
+
+def needs_review_order(conn, case_id) -> list:
+    """T-157: the live items that still wait for the paralegal and that the AI could not verify (state needs_review; pending, or an edit not yet confirmed), in timeline order:
+    the date of the record each item cites (earliest, for a flag that cites several), then that record's position, then entry before flag before amount, then id. Undated last.
+    [{id, kind, date, seq, rank, row}]. Same item filter as `_progress`."""
+    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
+    by_seq = {seq: rid for rid, (_, seq) in recs.items()}
+    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
+    handled = generator.resolved_placeholders(items["entry"])
+    out = []
+    for kind, rows in items.items():
+        for r in rows:
+            if r["id"] in handled or FT.is_filtered(r.get("state_reasons")) or r["state"] != "needs_review":
+                continue
+            if not (r["review_status"] == "pending" or review.edit_unconfirmed(kind, r)):
+                continue
+            ids = list(r.get("record_ids") or []) if kind != "flag" else \
+                [e.get("record_id") or by_seq.get(e.get("record_no")) for e in r.get("evidence") or []] or list((r.get("computed") or {}).get("record_ids") or [])
+            known = sorted((recs[i] for i in ids if i in recs), key=lambda x: (x[0] is None, x[0] or "", x[1] or 0))
+            date, seq = known[0] if known else (None, None)
+            date = date or (r.get("date_iso") if kind == "entry" else None)
+            out.append({"id": r["id"], "kind": kind, "date": date, "seq": seq, "rank": _RANK[kind], "row": r})
+    return sorted(out, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
+
+
+def next_action(conn, case_id, case: dict = None, blockers: list = None):
+    """T-157: the single first thing to do in a case, {item_id, kind, reason}, or None when nothing is waiting. Code only, deterministic:
+      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
+         blocker's (`case` for a blocker that names no item, `item_id` null) and `reason` its plain `why`. NOTHING_ACCEPTED yields to step 2 when an item waits (deciding it clears it);
+      2. else the first needs-review item in timeline order (`needs_review_order`): `kind` entry | flag | amount, `reason` the item's own plain `why`;
+      3. else NOTHING_ACCEPTED when nothing is accepted; else None.
+    A case that was only ingested has no items yet: {item_id: null, kind: "run"}. `blockers` may be passed when the caller already read the gate."""
+    case = case or DB.get_case(conn, case_id)
+    if case["status"] == "ingested":
+        return {"item_id": None, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."}
+    blockers = _gate(conn, case_id)["blockers"] if blockers is None else blockers
+    first = next((b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"), None)
+    if first:
+        return {"item_id": first.get("item_id"), "kind": first["kind"], "reason": first["why"]}
+    waiting = needs_review_order(conn, case_id)
+    if waiting:
+        w = waiting[0]
+        return {"item_id": w["id"], "kind": w["kind"], "reason": present.item_view(conn, case_id, w["id"])["why"]}
+    if blockers:
+        return {"item_id": blockers[0].get("item_id"), "kind": blockers[0]["kind"], "reason": blockers[0]["why"]}
+    return None
+
+
 def summary(conn, case_id: str, stages) -> dict:
     case = DB.get_case(conn, case_id)
     rv = present.review_view(conn, case_id)
@@ -65,7 +148,7 @@ def summary(conn, case_id: str, stages) -> dict:
     gate = _gate(conn, case_id)
     last = conn.execute("SELECT max(at) FROM review_events WHERE case_id=?", (case_id,)).fetchone()[0]
     updated = case.get("run_finished_at") or case["created_at"]            # the same value GET case calls updated_at
-    return {"token": case_id, "title": readable_title(case["name"], case["source"], case["created_at"]), "name": case["name"],
+    return {"token": case_id, "title": case_title(conn, case), "name": case["name"],
             "source": case["source"], "status": case["status"],
             "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (case_id,)).fetchone()[0],
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(max(updated, last or 0)),
@@ -75,7 +158,7 @@ def summary(conn, case_id: str, stages) -> dict:
             "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},      # kept from the first version of this route
             "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "edits_to_check": counts["edit_to_check"],
                      "could_not_verify": counts["rejected"], "gate_blockers": gate["blockers"], "gate_warnings": gate["warnings"]},
-            "export_ready": gate["ready"]}
+            "export_ready": gate["ready"], "next_action": next_action(conn, case_id, case, gate["blockers"])}
 
 
 def summaries(conn, stages) -> list:
diff --git a/app/backend/present.py b/app/backend/present.py
index 60bad2f..b09f43b 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -34,9 +34,16 @@ def _ladder(row):
     return lad
 
 
+def rerun_available(row) -> bool:
+    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
+    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
+    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")
+
+
 def _common(row):
     return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
             "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
+            "rerun_available": rerun_available(row),
             "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message")}      # T-146 r3: set when a re-run disagreed with or failed on this decided item
 
 
diff --git a/app/backend/store.py b/app/backend/store.py
index 56d56c9..6d5048a 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -2,10 +2,20 @@
 
 Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
 """
+import os
+
 from app.backend import ingest, pdf_text, spanish
 from app.db import db as DB
 
 
+def live_model_available() -> bool:
+    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with.
+    Read per call, like api.live_enabled, so a test can change the environment."""
+    from app.llm import provider
+    name = provider.backend_name()
+    return name != "fixture" and os.environ.get("ENABLE_LIVE") == "1" and (name == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
+
+
 def iso(t) -> str:
     import datetime
     return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:47.490Z

**tool call — Bash**
````
{
 "command": "git show 926bf37 -- memory/contracts/api.md tests/unit/test_case_list.py",
 "description": "Show api.md and test diff for commit 926bf37"
}
````

### User / tool · 2026-11-02T14:47:47.599Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:48.891Z

**tool call — Bash**
````
{
 "command": "S=$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad 2>/dev/null | head -1); A=\"$S/t157-r1/archive\"; cd \"$A\" && grep -n \"def demo_mode\\|def live_enabled\\|def body_of\\|def backend\\b\\|def backend(\" app/backend/*.py | head; echo ---; grep -n \"def update_case\\|def create_case\" app/db/db.py; echo ---; grep -n \"def backend_name\" -A12 app/llm/provider.py; echo ---; grep -rn \"Untitled\" app tests tools evals 2>/dev/null | head -20; echo ---; grep -n \"Case titles\\|next_action\\|rerun_available\" memory/contracts/api.md | head -30",
 "description": "Locate demo/live helpers, DB update, backend name, and api.md references in archive"
}
````

### User / tool · 2026-11-02T14:47:49.154Z

**tool result**
````
app/backend/api.py:112:    def backend():
app/backend/api.py:116:    def live_enabled():
app/backend/api.py:119:    def demo_mode():
app/backend/api.py:192:    async def body_of(request: Request) -> dict:
app/backend/generator.py:18:def body_offset(record: dict) -> int:
---
114:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
122:def update_case(conn, case_id: str, **fields) -> None:
---
23:def backend_name() -> str:
24-    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
25-    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
26-    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
27-    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
28-    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
29-        return "fixture"
30-    return name
31-
32-
33-def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
34-    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
35-    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
---
app/frontend/overview.js:51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
app/backend/case_list.py:49:    """A name a paralegal would recognise. A file name or slug ("smith_records-2024.pdf") becomes words; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case";
app/backend/case_list.py:62:    """What to show for a case: its name made readable; else the first record header (provider and date); else the date it was added. Never "Untitled case"."""
tests/unit/test_case_list.py:111:        assert s["title"] == case["title"] and "Untitled" not in s["title"], lid
tests/unit/test_case_list.py:145:    assert case_list.readable_title(None, "paste", 1762000000) == "Records added Nov 1"          # T-157: never "Untitled case"
tests/unit/test_case_list.py:184:    assert "Untitled" not in local.get(f"/api/cases/{tok}").json()["title"]
---
33:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
60:Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`. Optional `title` (T-157: the case's name, as typed; `name` is still accepted as the same thing, and `title` wins when both are sent; `POST /api/cases/pdf` takes a `title` query parameter beside `name`). Control characters and line breaks become spaces, runs of white space collapse, at most 120 characters; blank means no name. The response carries `title` (what to show; see "Case titles" under `GET /api/cases`).
108:**D-051:** accept also refuses (all or nothing) any entry whose current summary fails a code check: `422 CODE_CHECK_FAILED`, message = the plain reason + "Nothing was changed.", `detail.rejected` has `{id, reason: "code_check_failed", reason_code, why, next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}`.
132:**T-157, `title` and `next_action` (GET case, top level):** `title` is the same string `GET /api/cases` shows (see "Case titles" there; never "Untitled case"). `next_action` is `{item_id, kind, reason}` or `null`: the single first thing to do, the same value `GET /api/cases` carries (code only, deterministic; rules under "`next_action`" there). **`rerun_available` (bool, every entry, amount and flag view in this payload, in `GET .../items/{item_id}` `item` and in every review response `item`; not on `tray` items):** whether "Run the second check again" (`POST .../rejudge`) can get an answer for this item now. False in demo mode and with the fixture backend (no live model can answer: `ENABLE_LIVE` is not `1`, `LLM_BACKEND` is `fixture`, or `anthropic-api` has no key), and false after a rerun that got no answer (the last `ladder.rejudge` attempt is `unavailable`; it turns true again only when the item's wording or quote changes and drops those attempts). True otherwise. It says nothing about whether the check is needed: use `second_check_pending` for that. Show the rerun button only when both are true; when `second_check_pending` is true and `rerun_available` is false, say the check cannot run here.
368:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
370:- Item trace (`GET /items/{id}/trace`, the "Why this status" row; T-134 r2): while `edit_to_check` is true the `human` step is `pending` (reason `EDIT_NOT_CONFIRMED`, `blocks_export` false, `next_action` DECIDE) with "You edited this item; it is not accepted until you compare it with the quote and accept it, so it stays out of the letter.", and the item `verdict` is `{code: "edit_to_check", label: "Edited; waiting for your check"}` (new `verdict.code` value; a failing code check still wins: `needs_attention`). After her accept it is `accepted` / "Accepted by you". A verified edit (state not `needs_review`) still reads "You edited this item and accepted it.". The case `/judges` totals and the `judges` step no longer count a human-edited entry whose re-check had no answer (D-045b).
397:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while it is `pending`. `likely_duplicate`: same service date, description and amount as an earlier charge of another record (`of` = that amount's id; not set for records the paralegal declared not-a-duplicate). `likely_total`: equals the sum of the other charges of its record (at least two others; it can be a coincidence). Both stay `kind: "charge"`. `POST .../items/{id}/review` with `{"action": "accept"}` on such a charge is `422 CONFIRM_REQUIRED` (`detail: {item_id, reason_code, flag, name, confirm_with, of, next_action}`, message = the flag's plain sentence + "It is not counted unless you confirm that flag by name (<flag>)."); to count it send `{"action": "accept", "confirm": "<confirm_with>"}`. A wrong or missing `confirm` is the same 422; dismiss and reset need none; after a reset the next accept needs the confirm again; a confirmed accept stamps `flag.confirmed_at`. `totals.flagged_charges` lists `[{id, flag}]` of flagged charges still waiting. The letter total (R-EX-8) sums exactly the accepted charges. **Reclassify (D-042) cannot promote a figure a D-059 rule made unclear:** `422 reclassify_refused`, `detail.reason: "NOT_A_CHARGE_BY_RULE"`, `detail.check: "code"`, `detail.rule_reason` (plain words; also appended to the message); no judge call is made.
404:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. An edit still marked `needs_review` is open and out of the letter, so it does not stop the export either (T-134, see the edit section). Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
591:  "next_action": null }                 // object when status is "fail" or "pending", else null
595:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the action is `POST /rejudge`), `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.
606:  "next_action": { "code": "COMPARE_BY_HAND", "text": "...", "target": {"item_id": "e4"} },
612:                    "latency_ms": 5120, "parsed_ok": true, "excerpt": {"record_id": "r4", "start": 858, "end": 928, "text": "..."} }, "next_action": null },
619:      "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
639:      "counts": {"records": 9, "duplicates_merged": 0, "characters": 4120}, "evidence": {}, "next_action": null },
643:      "next_action": {"code": "CONFIRM_DATE", "text": "...", "target": {"view": "dates_to_confirm"}} },
653:      "blockers": [ { "item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "...", "next_action": {"code": "DECIDE", "text": "..."} } ],
654:      "warnings": [ { "reason_code": "ITEMS_NOT_REVIEWED", "count": 21, "why": "21 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", "next_action": {"code": "DECIDE", "text": "...", "target": {"view": "queue"}} } ],
655:      "next_action": {"code": "DECIDE", "text": "..."} } ] }
661:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **T-114 (rates):** every amount in `amounts[]` carries `accept_effect` and `judge_required_for_export`. `accept_effect` is `letter_total` (a `charge`: counted in the billed-charges total), `acknowledge` (a `rate`: accepting it only acknowledges it, it is listed in the internal notes and never totaled, D-019/D-042) or `internal_notes` (`estimate`, `unclear`). `judge_required_for_export` is `false` only for a rate: an accepted rate whose second check never ran is **not** a `JUDGE_NOT_RUN` blocker, so accepting a rate can never block export (its item trace `judge_2` step says the check is optional for a rate). The UI should label a rate's button "Acknowledge" (or keep "Accept as noted") and never promise it goes in the letter. Charges, entries and flags are unchanged. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
677:`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
685:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
701:  "next_action": { "item_id": "f_r3_1" | null, "kind": "entry|flag|amount|case|run", "reason": "plain sentence" } | null }
703:**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, the first record header: the provider (its Source line, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same cleaning as on create: line breaks and control characters become spaces, white space collapses, 120 characters at most) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event.
705:**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
777:- **Accept (single, batch, and `edit`, D-051 choke point).** Refused `422 CODE_CHECK_FAILED` with `detail = {item_id, reason_code: "CHARGE_TEXT_IN_ENTRY", step_id: "charge_text", failed_steps: ["charge_text"], tokens: [], amounts: [...], next_action: {code: "EDIT_QUOTE" | "EDIT_SUMMARY", text, target}}`; `EDIT_QUOTE` when the quote states the amount (the quote picker), else `EDIT_SUMMARY`. Same shape as the D-051 code checks.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:55.664Z

**tool call — Bash**
````
{
 "command": "cd \"$(ls -d /private/tmp/claude-501/*/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad)/t157-r1/archive\" && sed -n 105,125p app/backend/api.py; echo ----; grep -rn \"rejudge\" app/backend/*.py | grep -v \"^.*#\" | head -30; echo ----; grep -n \"def _gate\" -A22 app/backend/case_list.py",
 "description": "Inspect demo/live helpers, rejudge storage, and gate construction in archive"
}
````

### User / tool · 2026-11-02T14:47:55.782Z

**tool result**
````
/bin/bash: line 0: cd: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive: No such file or directory
----
app/backend/api.py:389:    @app.post("/api/cases/{token}/rejudge")
app/backend/api.py:390:    async def rejudge_case(token: str):
app/backend/api.py:393:        from app.backend import rejudge as RJ
app/backend/api.py:405:                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
app/backend/present.py:39:    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
app/backend/review.py:410:        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
app/backend/review.py:430:    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
app/backend/review.py:442:    if snap.get("rejudge"):
app/backend/review.py:443:        lad["rejudge"] = snap["rejudge"]
app/backend/review.py:445:        lad.pop("rejudge", None)
app/backend/rejudge.py:3:rejudge(conn, case_id, call, now=None) -> dict
app/backend/rejudge.py:7:    except one entry in ladder.rejudge. The paralegal's review_status is never touched. Nothing here clears the export gate except a judge answer.
app/backend/rejudge.py:59:    """One audit row per asked item (review_events action 'rejudge'); review_status is never touched."""
app/backend/rejudge.py:60:    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
app/backend/rejudge.py:61:                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)
app/backend/rejudge.py:64:def rejudge(conn, case_id: str, call, now: float = None) -> dict:
app/backend/rejudge.py:77:        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
app/backend/rejudge.py:92:    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
app/backend/trace.py:858:    """The last rerun of the second check (ladder.rejudge) came back unavailable."""
app/backend/trace.py:859:    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
----
86:def _gate(conn, case_id) -> dict:
87-    step = next(s for s in trace.case_trace(conn, case_id, full=False)["steps"] if s["id"] == "export_gate")
88-    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731
89-    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
90-            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}
91-
92-
93-_RANK = {"entry": 0, "flag": 1, "amount": 2}
94-
95-
96-def needs_review_order(conn, case_id) -> list:
97-    """T-157: the live items that still wait for the paralegal and that the AI could not verify (state needs_review; pending, or an edit not yet confirmed), in timeline order:
98-    the date of the record each item cites (earliest, for a flag that cites several), then that record's position, then entry before flag before amount, then id. Undated last.
99-    [{id, kind, date, seq, rank, row}]. Same item filter as `_progress`."""
100-    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
101-    by_seq = {seq: rid for rid, (_, seq) in recs.items()}
102-    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
103-    handled = generator.resolved_placeholders(items["entry"])
104-    out = []
105-    for kind, rows in items.items():
106-        for r in rows:
107-            if r["id"] in handled or FT.is_filtered(r.get("state_reasons")) or r["state"] != "needs_review":
108-                continue
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:47:56.933Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive/tests/unit/test_case_list.py"
}
````

### User / tool · 2026-11-02T14:47:56.943Z

**tool result**
````
1	"""T-148: GET /api/cases summary list. Every field is compared with the route that owns it (GET case, /status, /trace, /export) for every library
2	case, so the overview can never say something the case screen does not. Fixture backend, no network; local mode only."""
3	import pathlib
4	import time
5	
6	import pytest
7	from fastapi.testclient import TestClient
8	
9	from app.backend import case_list
10	from app.backend.api import create_app
11	
12	LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
13	LIB_IDS = sorted(p.stem for p in LIB.glob("*.txt"))
14	
15	
16	@pytest.fixture(scope="module")
17	def local(tmp_path_factory):
18	    import os
19	    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
20	    os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
21	    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
22	        os.environ.pop(k, None)
23	    d = tmp_path_factory.mktemp("cl")
24	    c = TestClient(create_app(str(d / "t.sqlite"), static_dir=str(d)), client=("127.0.0.1", 50000))
25	    yield c
26	    for k, v in old.items():
27	        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
28	
29	
30	def _wait(c, tok):
31	    for _ in range(240):
32	        s = c.get(f"/api/cases/{tok}/status").json()
33	        if s["status"] in ("ready", "failed"):
34	            return s
35	        time.sleep(0.25)
36	    raise AssertionError(s)
37	
38	
39	@pytest.fixture(scope="module")
40	def cases(local):
41	    """Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss)."""
42	    toks = {}
43	    for lid in LIB_IDS:
44	        r = local.post("/api/cases", json={"library": lid})
45	        assert r.status_code == 201, r.text
46	        toks[lid] = r.json()["token"]
47	        assert local.post(f"/api/cases/{toks[lid]}/run", json={}).status_code == 202
48	    for t in toks.values():
49	        _wait(local, t)
50	    first = toks[LIB_IDS[0]]
51	    items = [i for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{first}").json()[k]]
52	    for n, it in enumerate(items[:6]):
53	        local.post(f"/api/cases/{first}/items/{it['id']}/review", json={"action": ["accept", "dismiss"][n % 2]})
54	    second = local.get(f"/api/cases/{toks[LIB_IDS[1]]}").json()["entries"][0]          # a reworded entry: saved, but the second check cannot confirm the new wording
55	    local.post(f"/api/cases/{toks[LIB_IDS[1]]}/items/{second['id']}/review", json={"action": "edit", "edits": {"summary": second["summary"].rstrip(".") + " (reworded)."}})
56	    third = toks[LIB_IDS[2]]                                                                  # accept whatever the code checks allow: a case whose export gate opens
57	    for k in ("entries", "flags", "amounts"):
58	        for it in local.get(f"/api/cases/{third}").json()[k]:
59	            local.post(f"/api/cases/{third}/items/{it['id']}/review", json={"action": "accept"})
60	    text = (LIB / f"{LIB_IDS[-1]}.txt").read_text()               # an allowed (recorded) text, pasted under a file-slug name and never run
61	    toks["_ingested"] = local.post("/api/cases", json={"text": text, "name": "smith_records-2024.txt"}).json()["token"]
62	    return toks
63	
64	
65	def _by_token(local):
66	    r = local.get("/api/cases")
67	    assert r.status_code == 200
68	    return {x["token"]: x for x in r.json()["cases"]}
69	
70	
71	def test_list_covers_every_case_newest_first(local, cases):
72	    got = local.get("/api/cases").json()["cases"]
73	    assert {x["token"] for x in got} == set(cases.values()) and len(got) == len(LIB_IDS) + 1
74	    assert got[0]["token"] == cases["_ingested"] and [x["created_at"] for x in got] == sorted((x["created_at"] for x in got), reverse=True)
75	
76	
77	def test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):
78	    listed = _by_token(local)
79	    for lid, tok in cases.items():
80	        s, case = listed[tok], local.get(f"/api/cases/{tok}").json()
81	        st = local.get(f"/api/cases/{tok}/status").json()
82	        tr = local.get(f"/api/cases/{tok}/trace").json()
83	        gate = next(x for x in tr["steps"] if x["id"] == "export_gate")
84	        # identity and times: the case screen's own values
85	        assert s["name"] == case["name"] and s["status"] == case["status"] and s["created_at"] == case["created_at"] and s["updated_at"] == case["updated_at"], lid
86	        assert s["record_count"] == len(case["records"]) and s["last_activity_at"] >= s["updated_at"], lid
87	        # run stage: the status route
88	        assert s["run"]["stage"] == st["stage"] and s["run"]["steps_done"] == st["progress"]["done"] and s["run"]["steps_total"] == st["progress"]["total"], lid
89	        assert s["run"]["running"] == (case["status"] == "running"), lid
90	        # review counts and the could-not-verify tray: the case screen
91	        rc = case["review"]["counts"]
92	        h = s["hitl"]
93	        assert h["needs_review"] == rc["needs_review"] and h["edits_to_check"] == rc["edit_to_check"] and h["pending"] == rc["pending"], lid
94	        assert h["could_not_verify"] == len(case["tray"]), lid
95	        assert s["counts"] == {k: rc[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")}, lid
96	        # progress per kind: totals are the live items GET case lists, decided never exceeds total, and the kinds add up to the review counts
97	        live = {"entries": [e for e in case["entries"] + case["undated_entries"]], "flags": case["flags"], "amounts": case["amounts"]}
98	        for kind, rows in live.items():
99	            p = s["progress"][kind]
100	            assert p["total"] == len(rows), (lid, kind)
101	            assert p["decided"] == sum(1 for r in rows if r["review_status"] in ("accepted", "dismissed", "edited")) - (rc["edit_to_check"] if kind == "entries" else 0), (lid, kind)
102	        tot = sum(v["total"] for v in s["progress"].values())
103	        dec = sum(v["decided"] for v in s["progress"].values())
104	        assert tot - dec == rc["pending"] + rc["edit_to_check"], lid
105	        # gate: blockers and warnings with their plain reasons, and export_ready is what GET /export allows
106	        assert s["export_ready"] is gate["ready"] is (local.get(f"/api/cases/{tok}/export").status_code == 200), lid
107	        assert [(b["reason_code"], b["why"]) for b in h["gate_blockers"]] == [(b["reason_code"], b["why"]) for b in gate["blockers"]], lid
108	        assert [(w["reason_code"], w["count"], w["why"]) for w in h["gate_warnings"]] == [(w["reason_code"], w["count"], w["why"]) for w in gate["warnings"]], lid
109	        assert all(b["why"] for b in h["gate_blockers"]) and all(w["why"] for w in h["gate_warnings"]), lid
110	        # T-157: title and next_action are the same on GET case; no item says rerun is available in fixture mode
111	        assert s["title"] == case["title"] and "Untitled" not in s["title"], lid
112	        assert s["next_action"] == case["next_action"], lid
113	        for k in ("entries", "flags", "amounts"):
114	            assert all(i["rerun_available"] is False for i in case[k]), (lid, k)
115	
116	
117	def test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):
118	    s = _by_token(local)
119	    first = s[cases[LIB_IDS[0]]]
120	    assert sum(v["decided"] for v in first["progress"].values()) >= 1 and first["last_activity_at"] > first["updated_at"] or first["last_activity_at"] >= first["updated_at"]
121	    ing = s[cases["_ingested"]]
122	    assert ing["status"] == "ingested" and ing["run"]["stage"] == "ingest" and ing["export_ready"] is False
123	    assert [b["reason_code"] for b in ing["hitl"]["gate_blockers"]] == ["NOTHING_ACCEPTED"]
124	
125	
126	def test_decided_cases_cover_ready_and_edit_to_check(local, cases):
127	    s = _by_token(local)
128	    third = s[cases[LIB_IDS[2]]]
129	    assert third["export_ready"] is True and third["hitl"]["gate_blockers"] == [] and sum(v["decided"] for v in third["progress"].values()) > 0
130	    second = s[cases[LIB_IDS[1]]]
131	    assert second["hitl"]["edits_to_check"] == 1 and second["progress"]["entries"]["decided"] == 0          # a reworded entry is saved but not decided
132	    assert "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in second["hitl"]["gate_warnings"]]
133	
134	
135	def test_title_is_readable_not_a_file_slug(local, cases):
136	    s = _by_token(local)
137	    assert s[cases["_ingested"]]["title"] == "Smith records 2024"
138	    for lid in LIB_IDS:
139	        t = s[cases[lid]]["title"]
140	        assert t and "_" not in t and not t.endswith((".txt", ".pdf")) and not t.lower().startswith(("case ", "lib")), t
141	    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"
142	    assert case_list.readable_title("case_01_date_formats", "paste", 0) == "Date formats"
143	    assert case_list.readable_title("records_final-v2.pdf", "paste", 0) == "Records final v2"
144	    assert case_list.readable_title("Smith v. Jones intake", "paste", 0) == "Smith v. Jones intake"
145	    assert case_list.readable_title(None, "paste", 1762000000) == "Records added Nov 1"          # T-157: never "Untitled case"
146	    assert case_list.readable_title("", "sample", 0) == "Sample case"
147	
148	
149	def test_list_is_code_only_no_text_no_model_calls(local, cases):
150	    import json
151	    listed = local.get("/api/cases").json()["cases"]
152	    raw = json.dumps(listed)
153	    assert "Excerpt:" not in raw and "raw_text" not in raw
154	    before = {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in list(cases.values())[:3]}
155	    local.get("/api/cases")
156	    assert before == {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in before}
157	
158	
159	def test_list_is_404_outside_local_mode(local, monkeypatch):
160	    monkeypatch.delenv("ZLAYT_MODE")
161	    assert local.get("/api/cases").status_code == 404
162	
163	
164	# ---------------------------------------------------------------- T-157
165	def test_default_title_comes_from_the_first_record_header(local, cases):
166	    s = _by_token(local)
167	    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"                     # a library case keeps its name
168	    text = (LIB / f"{LIB_IDS[0]}.txt").read_text()
169	    tok = local.post("/api/cases", json={"text": text}).json()["token"]                    # pasted, no name: provider and first date of record 1
170	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026"
171	    assert _by_token(local)[tok]["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026" and _by_token(local)[tok]["name"] is None
172	
173	
174	def test_title_on_create_and_patch(local, cases):
175	    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
176	    r = local.post("/api/cases", json={"text": text, "title": "  Rivera   v. Acme \n intake "})
177	    assert r.status_code == 201 and r.json()["title"] == "Rivera v. Acme intake"
178	    tok = r.json()["token"]
179	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera v. Acme intake" and _by_token(local)[tok]["title"] == "Rivera v. Acme intake"
180	    p = local.patch(f"/api/cases/{tok}", json={"title": "Rivera, final"})
181	    assert p.status_code == 200 and p.json()["title"] == "Rivera, final" and p.json()["token"] == tok
182	    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera, final" and _by_token(local)[tok]["title"] == "Rivera, final"
183	    assert local.patch(f"/api/cases/{tok}", json={"title": "   "}).json()["title"] != "Rivera, final"          # blank returns to the derived default
184	    assert "Untitled" not in local.get(f"/api/cases/{tok}").json()["title"]
185	    long = local.patch(f"/api/cases/{tok}", json={"title": "x" * 200}).json()["title"]
186	    assert len(long) == 120
187	    for bad in ({"title": 5}, {"title": None, "x": 1}, {}, {"name": "a"}):
188	        got = local.patch(f"/api/cases/{tok}", json=bad)
189	        if bad == {"title": None, "x": 1}:
190	            assert got.status_code == 200          # null clears the name like a blank title
191	        else:
192	            assert got.status_code == 400 and got.json()["error"]["code"] == "bad_request", bad
193	    assert local.patch("/api/cases/nope", json={"title": "a"}).status_code == 404
194	
195	
196	def test_titles_are_never_untitled(local, cases):
197	    for x in local.get("/api/cases").json()["cases"]:
198	        assert x["title"] and "untitled" not in x["title"].lower()
199	    tok = local.post("/api/cases", json={"text": (LIB / f"{LIB_IDS[2]}.txt").read_text(), "name": "  "}).json()["token"]
200	    assert "untitled" not in local.get(f"/api/cases/{tok}").json()["title"].lower()
201	
202	
203	def test_rerun_available_follows_live_mode_and_the_last_rerun(local, cases, monkeypatch):
204	    from app.db import db as DB
205	    tok = cases[LIB_IDS[0]]
206	    item = local.get(f"/api/cases/{tok}").json()["entries"][0]
207	    assert item["rerun_available"] is False                                          # fixture / demo mode: nothing can answer
208	    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
209	    monkeypatch.setenv("ENABLE_LIVE", "1")
210	    got = local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]
211	    assert got["rerun_available"] is True                                            # live and no rerun yet
212	    assert all(i["rerun_available"] is True for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{tok}").json()[k])
213	    c = DB.connect(local.app.state.db_path)
214	    try:
215	        row = DB.get_item(c, item["id"], tok)
216	        lad = dict(row["ladder"] or {})
217	        lad["rejudge"] = [{"verdict": "unavailable"}]
218	        DB.update_item(c, item["id"], case=tok, ladder=lad)
219	    finally:
220	        c.close()
221	    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False          # the last rerun got no answer
222	    monkeypatch.setenv("ENABLE_LIVE", "0")
223	    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False
224	    monkeypatch.setenv("ENABLE_LIVE", "1")
225	    monkeypatch.setenv("LLM_BACKEND", "anthropic-api")
226	    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
227	    other = [i for i in local.get(f"/api/cases/{tok}").json()["flags"] + local.get(f"/api/cases/{tok}").json()["amounts"]][:1]
228	    if other:
229	        assert other[0]["rerun_available"] is False                                   # no key, no live answer
230	
231	
232	def test_next_action_blockers_first_then_needs_review_in_timeline_order(local, cases):
233	    s = _by_token(local)
234	    ing = s[cases["_ingested"]]["next_action"]
235	    assert ing["kind"] == "run" and ing["item_id"] is None and ing["reason"]          # ingested: nothing to decide before the run
236	    for lid, tok in cases.items():
237	        if lid == "_ingested":
238	            continue
239	        na = s[tok]["next_action"]
240	        case = local.get(f"/api/cases/{tok}").json()
241	        blockers = s[tok]["hitl"]["gate_blockers"]
242	        if na is None:
243	            waiting = [i for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
244	                       if i["state"] == "needs_review" and (i["review_status"] == "pending" or i.get("edit_to_check"))]
245	            assert not blockers and not waiting, lid          # nothing blocks the export and nothing needs review: nothing to point at
246	            continue
247	        assert set(na) == {"item_id", "kind", "reason"} and na["reason"], lid
248	        item_blockers = [b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"]
249	        if item_blockers:                                                              # a gate blocker is the first thing, in gate order
250	            assert (na["item_id"], na["kind"], na["reason"]) == (item_blockers[0].get("item_id"), item_blockers[0]["kind"], item_blockers[0]["why"]), lid
251	            continue
252	        every = {i["id"]: (k, i) for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])}
253	        assert na["item_id"] in every, lid
254	        kind, it = every[na["item_id"]]
255	        assert it["state"] == "needs_review" and (it["review_status"] == "pending" or it["edit_to_check"]), lid
256	        assert na["kind"] == {"entries": "entry", "flags": "flag", "amounts": "amount"}[kind] and na["reason"] == it["why"], lid
257	    # accepting the item next_action names moves it on (or, when it was the last, clears it)
258	    fresh = local.post("/api/cases", json={"library": LIB_IDS[3]}).json()["token"]
259	    local.post(f"/api/cases/{fresh}/run", json={})
260	    _wait(local, fresh)
261	    seen = []
262	    for _ in range(60):
263	        na = local.get(f"/api/cases/{fresh}").json()["next_action"]
264	        assert na == _by_token(local)[fresh]["next_action"]
265	        if na is None or na["item_id"] is None or na["item_id"] in seen:
266	            break
267	        seen.append(na["item_id"])
268	        local.post(f"/api/cases/{fresh}/items/{na['item_id']}/review", json={"action": "dismiss"})
269	    assert len(seen) == len(set(seen))
270	
271	
272	def test_next_action_orders_by_record_date_not_by_kind_or_id(local, cases):
273	    from app.backend import case_list
274	    from app.db import db as DB
275	    c = DB.connect(local.app.state.db_path)
276	    try:
277	        checked = 0
278	        for tok in cases.values():
279	            order = case_list.needs_review_order(c, tok)
280	            assert order == sorted(order, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
281	            dated = [x["date"] for x in order if x["date"]]
282	            assert dated == sorted(dated)                                             # timeline order
283	            assert all(x["row"]["state"] == "needs_review" and x["row"]["review_status"] in ("pending", "edited") for x in order)
284	            checked += len(order)
285	        assert checked > 5                                                            # the library really has needs-review work to order
286	    finally:
287	        c.close()
288	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:12.186Z

**tool call — Bash**
````
{
 "command": "ls -la .venv/bin/python 2>&1 | head -2; A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; ls \"$A/evals/library\" | head -3; echo ---; sed -n 105,125p \"$A/app/backend/api.py\"; echo ---; sed -n 60,80p \"$A/app/backend/rejudge.py\"; echo ---; grep -n \"rerun_available\\|_common(\" \"$A/app/backend/present.py\" | head -30",
 "description": "Check venv, library fixtures, demo/live helpers, rejudge attempt shape, rerun_available call sites"
}
````

### User / tool · 2026-11-02T14:48:12.324Z

**tool result**
````
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
---
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
---
    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)


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
        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
        if ladder_verdict == "unavailable":
            DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
---
37:def rerun_available(row) -> bool:
43:def _common(row):
46:            "rerun_available": rerun_available(row),
53:    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
81:    return {**_common(row), "flag": flag, "confirm_required": needs, "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
116:    c = _common(row)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:20.800Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; echo \"== name/title readers\"; grep -rn \"\\[\\\"name\\\"\\]\\|\\['name'\\]\\|\\\"title\\\"\\]\\|case_title\\|\\.get(\\\"name\\\")\" app --include=*.py | grep -v \"^app/backend/case_list.py:.*def \" | head -40; echo \"== edit path rejudge handling\"; grep -n \"rejudge\\|def set_review\\|def _edit\\|edit_unconfirmed\" app/backend/review.py | head -40; echo \"== frontend title sinks\"; grep -rn \"title\" app/frontend --include=*.js | grep -i \"innerHTML\\|insertAdjacentHTML\\|outerHTML\" | head; grep -rn \"\\.title\\b\" app/frontend --include=*.js | head -20",
 "description": "Trace title and name readers, edit-path rejudge handling, frontend title sinks"
}
````

### User / tool · 2026-11-02T14:48:20.948Z

**tool result**
````
== name/title readers
app/backend/ingest.py:351:        w["title"], w["explanation"] = flag_templates.render("record_warning", w["category"], provider=r["source"] or None,
app/backend/flags.py:33:        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
app/backend/flags.py:36:        f["title"], f["explanation"] = "Unrecognised flag category", "The model proposed a category that is not on the closed list."
app/backend/flags.py:203:                f["title"], f["explanation"] = FT.render("conflict", lf["category"], provider_a=record.get("source"), date_a=record.get("date_iso"),
app/backend/api.py:75:        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
app/backend/api.py:248:        given = b.get("title") if isinstance(b.get("title"), str) else b.get("name")          # T-157: `title` is the name a paralegal types; `name` stays accepted
app/backend/api.py:249:        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample)
app/backend/api.py:308:            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
app/backend/api.py:323:            return {**v, "title": case_list.case_title(c, case), "next_action": case_list.next_action(c, token, case)}          # T-157
app/backend/api.py:331:        if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
app/backend/api.py:336:            DB.update_case(c, token, name=case_list.clean_title(b["title"]) or None)
app/backend/api.py:338:            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
app/backend/review.py:183:    detail = {"item_id": item_id, "reason_code": "CONFIRM_REQUIRED", "flag": f["flag"], "name": f["name"], "confirm_with": f["confirm_with"], "of": f.get("of"),
app/backend/review.py:186:    return ReviewError(422, "CONFIRM_REQUIRED", detail, f"{f['name']}: {f['message']} It is not counted unless you confirm that flag by name ({f['confirm_with']}).{wrong}")
app/backend/review.py:548:                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
app/backend/language.py:259:        r["lang_name"] = d["name"] if d["lang"] == "other" else None
app/backend/present.py:118:    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
app/backend/present.py:343:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
app/backend/present.py:402:        out.append({"token": cid, "name": case["name"], "status": case["status"], "source": case["source"],
app/db/db.py:107:    return {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
app/backend/pipeline.py:66:                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
app/backend/pipeline.py:81:        flags.append({"id": w["id"], "type": "record_warning", "category": w["category"], "origin": "code", "title": w["title"],
app/backend/pipeline.py:222:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
app/backend/case_list.py:50:    `case_title` prefers the first record header over this fallback)."""
app/backend/case_list.py:63:    if (case["name"] or "").strip():
app/backend/case_list.py:64:        return readable_title(case["name"], case["source"], case["created_at"])
app/backend/case_list.py:151:    return {"token": case_id, "title": case_title(conn, case), "name": case["name"],
== edit path rejudge handling
82:def edit_unconfirmed(kind: str, item: dict) -> bool:
195:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
334:def _edit(conn, case_id, kind, item, body, call, t):
383:        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
385:    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
403:    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
415:    if snap.get("rejudge"):
416:        lad["rejudge"] = snap["rejudge"]
418:        lad.pop("rejudge", None)
== frontend title sinks
app/frontend/flags.js:67:    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
app/frontend/flags.js:69:      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
app/frontend/review.js:42:  RV.label = (item) => item.title || (item.provider ? item.provider + (item.date ? ", " + item.date : "") : null) || item.text || item.id;
app/frontend/stepper.js:65:    return it.title || it.id;
app/frontend/overview.js:51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
app/frontend/app.js:29:    document.title = c && c.name ? "Treatment timeline · " + nameOf(s) : "Treatment timeline";
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:37.393Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; echo \"== spec mentions of title/HTML/markup\"; grep -rn -i \"html\\|markup\\|case name\\|title\" spec docs memory/ORCHESTRATOR_DECISIONS.md 2>/dev/null | grep -i \"case\\|html\\|markup\\|escape\\|untitled\" | head -20; echo \"== frontend el helper\"; grep -rn \"const el = \\|function el(\\|el = (\" app/frontend/*.js | head -3; echo \"== overview title sink\"; grep -n \"titleOf\" app/frontend/overview.js | head; echo \"== library title-length / HTML tests\"; grep -rln \"<script\\|onerror\\|&lt;\" tests/unit | head",
 "description": "Search spec and frontend for title HTML rules and render sinks"
}
````

### User / tool · 2026-11-02T14:48:37.589Z

**tool result**
````
== spec mentions of title/HTML/markup
spec/REQUIREMENTS.md:93:| R-RV-2 | **What each action does (D-010, D-012).** See the table below the requirements. Originals are kept. "Edited" shows in the review UI and in the internal notes, never in the letter text. | UT, each → 422 `invalid_edit`: edit an entry's date or provider; edit a flag's evidence, type or title; edit a charge's amount or class; any other key. `confirm_date` (`POST /records/{rid}/confirm_date`): a date that is not one of the code-proposed readings → 422 `date_invalid`; a record with no readable date (no readings) cannot be confirmed. Also → 422 `invalid_edit`: an excerpt edit that is not a contiguous run of whole sentence units of the same record; an excerpt edit that drops a hedge-set unit (R-TL-8). `confirm_date` on `case_01` record 8 with 2026-05-04 → 200, a review event is logged, the entry joins the timeline. E2E: edit entry 3's summary → "edited" label in the UI; the letter shows the new summary with its citation and no "edited" mark; the notes list the original and the new text. | UT + E2E |
spec/REQUIREMENTS.md:207:17. **Smaller cuts (D-011; SCOPE_CUTS 17).** LLM date pointing, bring-your-own-key, the full-prompt audit view, edits to flag titles or explanations, a case list.
memory/ORCHESTRATOR_DECISIONS.md:19:| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
docs/UI_DESIGN_BRIEF.md:31:| `--t-page` | 24 / 32 | 600 | case title only |
docs/UI_DESIGN_BRIEF.md:116:- **Persistent header strip:** case name, progress ("12 of 20 reviewed", with a text count, not just a bar), density toggle, theme toggle, Export.
docs/CONTRACT.md:217:**Web UI (`tools/board_server.py`, port 7777, one Python file + one HTML/JS file, no build step, mobile-first, dark/light):**
docs/CONTRACT.md:324:- `submission/SUBMISSION_CHECKLIST.md` mirroring Appendix A's checklist with links; `submission/email-draft.md`; `submission/NEEDS_CHRIS.md` (final, prioritized, each item with the exact action and where to put the answer); PDF exports via `pandoc` if available (else HTML).
== frontend el helper
app/frontend/charges.js:5:  const RV = ZL.rv, el = (...a) => ZL.el(...a);
app/frontend/flags.js:6:  const RV = ZL.rv, el = (...a) => ZL.el(...a);
app/frontend/state.js:27:  ZL.registerPanel = (fn) => ZL.hooks.panels.push(fn);
== overview title sink
51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
64:    title: ["Title A to Z", (a, b) => { const x = titleOf(a).toLowerCase(), y = titleOf(b).toLowerCase(); return x < y ? -1 : x > y ? 1 : 0; }],
77:    const h = hitl(s), title = titleOf(s);
== library title-length / HTML tests
tests/unit/test_provider_backends.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:40.742Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; grep -rn \"ZL.el = \\|\\.el = function\\|ZL\\.el=\" app/frontend/*.js | head -3; grep -rn \"textContent\\|innerHTML\" app/frontend/core*.js app/frontend/util*.js 2>/dev/null | head -5; echo ---; sed -n 76,84p app/frontend/overview.js",
 "description": "Check frontend el helper text sink and overview title render"
}
````

### User / tool · 2026-11-02T14:48:40.901Z

**tool result**
````
app/frontend/dom.js:5:  ZL.el = function (tag, attrs, ...kids) {
---
  function rowNode(s) {
    const h = hitl(s), title = titleOf(s);
    ZL.caseTitles[s.token] = title;
    const a = el("a", { class: "cv-open", href: "#/case/" + encodeURIComponent(s.token), "data-testid": "cases-open", onclick: (ev) => {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button) return;
      ev.preventDefault(); ev.stopPropagation(); openCase(s.token, true);
    } }, title);
    return el("li", { class: "cv-row", "data-testid": "cases-row", "data-token": s.token, onclick: (ev) => { if (!ev.target.closest("a, button, select, input, summary")) openCase(s.token, true); } },
      el("div", { class: "cv-main" },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:43.362Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; sed -n 1,20p app/frontend/dom.js",
 "description": "Read frontend el helper to confirm text insertion"
}
````

### User / tool · 2026-11-02T14:48:43.498Z

**tool result**
````
/* Shared DOM helpers (frontend-1 / T-042; also used by T-043). Data is only ever written with textContent / text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  // el("button", {class:"x", type:"button", onclick:fn, "data-testid":"y"}, "label", childNode, ...)
  ZL.el = function (tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat(Infinity)) {   // any nesting of arrays: a list of [dt, dd] pairs must never print as [object HTMLElement]
      if (c == null || c === false) continue;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return e;
  };
  // Rank "needs review first" by the state an item had when this case was first shown, so rows do not jump when a decision changes the state
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:48:49.873Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\" && env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -30",
 "description": "Run test_case_list.py on the archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:48:58.367Z

**tool result**
````
.............                                                            [100%]
13 passed in 8.00s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:02.014Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\" && env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" timeout 580 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -25",
 "description": "Run full unit suite on the archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:49:02.147Z

**tool result**
````
env: timeout: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:04.796Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\" && env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -25",
 "description": "Run full unit suite on the archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:49:09.232Z

**tool result**
````
==================================== ERRORS ====================================
_____________ ERROR collecting tests/unit/test_amounts_d059_api.py _____________
tests/unit/test_amounts_d059_api.py:11: in <module>
    LEDGER = (ROOT / "artifacts" / "review-evidence" / "T-140-adjuster" / "synthetic_ledger.txt").read_text()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1027: in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive/artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt'
=========================== short test summary info ============================
ERROR tests/unit/test_amounts_d059_api.py - FileNotFoundError: [Errno 2] No s...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 3.81s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:14.358Z

**tool call — Bash**
````
{
 "command": "git status --short -- app tests evals tools docs spec memory/contracts artifacts/review-evidence | head; echo \"--- untracked product-ish paths:\"; git ls-files --others --exclude-standard -- app tests evals tools artifacts | head -20; echo \"--- review-evidence dirs referenced by tests:\"; grep -rln \"review-evidence\" tests | head; ls artifacts/review-evidence | wc -l; git check-ignore -v artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt",
 "description": "Check working tree divergence and untracked fixtures the tests read"
}
````

### User / tool · 2026-11-02T14:49:16.794Z

**tool result (error)**
````
Exit code 1
 M app/backend/charge_text.py
MM app/backend/conflict_candidates.py
 M app/backend/generator.py
 M app/backend/present.py
 M app/backend/review.py
 M app/backend/trace.py
 M app/backend/why.py
 M app/frontend/api.js
 M app/frontend/audit.js
 M app/frontend/charges.js
--- untracked product-ish paths:
artifacts/review-evidence/GATE-M2-paralegal/draft.md
artifacts/review-evidence/GATE-M2-paralegal/g1-analyzed-full.png
artifacts/review-evidence/GATE-M2-paralegal/g1-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g1-landing.png
artifacts/review-evidence/GATE-M2-paralegal/g1.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g1.py
artifacts/review-evidence/GATE-M2-paralegal/g2-shortcuts.png
artifacts/review-evidence/GATE-M2-paralegal/g2.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g2.py
artifacts/review-evidence/GATE-M2-paralegal/g3-after-entries.png
artifacts/review-evidence/GATE-M2-paralegal/g3-body.txt
artifacts/review-evidence/GATE-M2-paralegal/g3-edit-open.png
artifacts/review-evidence/GATE-M2-paralegal/g3-edit-saved.png
artifacts/review-evidence/GATE-M2-paralegal/g3-start.png
artifacts/review-evidence/GATE-M2-paralegal/g3.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g3.py
artifacts/review-evidence/GATE-M2-paralegal/g4.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g4.py
artifacts/review-evidence/GATE-M2-paralegal/g4b.out.txt
artifacts/review-evidence/GATE-M2-paralegal/g5-change-quote-e3.png
--- review-evidence dirs referenced by tests:
tests/unit/test_t116_gap_endpoints.py
tests/unit/test_billing.py
tests/unit/test_amounts_d059.py
tests/unit/test_pdf_hidden_r2.py
tests/unit/_pdf_probe.py
tests/unit/test_lib09_t110_r2.py
tests/unit/test_pdf_hidden_r3.py
tests/unit/test_t139_letter_eval.py
tests/unit/test_t116_r4_all_dated_records.py
tests/unit/test_t116_r5_header_only_warning.py
    1576
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:49:22.396Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; mkdir -p \"$A/artifacts/review-evidence\" && cp -Rn /Users/arsis/zlayt-pm-project/artifacts/review-evidence/. \"$A/artifacts/review-evidence/\" && cd \"$A\" && env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -25",
 "description": "Overlay untracked review-evidence fixtures into archive and run full unit suite",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:50:51.892Z

**tool result (error)**
````
Exit code 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:50:55.744Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; ls \"$A/artifacts/review-evidence\" | wc -l; ls \"$A/artifacts/review-evidence/T-140-adjuster\" 2>&1 | head -3; cd \"$A\" && env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > \"$(dirname \"$A\")/full-unit.out\" 2>&1; echo \"exit=$?\"; tail -25 \"$(dirname \"$A\")/full-unit.out\"",
 "description": "Verify overlay and run full unit suite, capturing output to a file",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:55:33.117Z

**tool result**
````
    1576
library_accept_all.txt
probe_library.py
probe_paste.py
exit=0
........................................................................ [ 62%]
........................................................................ [ 63%]
........................................................................ [ 65%]
........................................................................ [ 67%]
........................................................................ [ 68%]
................................................................ss...... [ 70%]
........................................................................ [ 72%]
........................................................................ [ 73%]
........................................................................ [ 75%]
........................................................................ [ 77%]
........................................................................ [ 78%]
........................................................................ [ 80%]
........................................................................ [ 82%]
........................................................................ [ 83%]
.............................................ss......................... [ 85%]
........................................................................ [ 87%]
........................................................................ [ 88%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
........................................................................ [ 97%]
........................................................................ [ 98%]
..............................................                           [100%]
4286 passed, 8 skipped in 275.41s (0:04:35)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:55:43.748Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project; A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\" && export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\"; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nrun(){ env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE $PY -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -4; }\necho \"== MUT A: next_action picks last needs-review item instead of first\"\nsed -i '' 's/        w = waiting\\[0\\]/        w = waiting[-1]/' app/backend/case_list.py && grep -n \"w = waiting\" app/backend/case_list.py && run; git -C $R show 926bf37:app/backend/case_list.py > app/backend/case_list.py\necho \"== MUT B: next_action skips gate blockers entirely\"\nsed -i '' 's/    first = next((b for b in blockers if b\\[\"reason_code\"\\] != \"NOTHING_ACCEPTED\"), None)/    first = None/' app/backend/case_list.py && grep -n \"first = None\" app/backend/case_list.py && run; git -C $R show 926bf37:app/backend/case_list.py > app/backend/case_list.py\necho \"== MUT C: needs-review sorted by rank (entry/flag/amount) before date\"\nsed -i '' 's/    return sorted(out, key=lambda x: (x\\[\"date\"\\] is None, x\\[\"date\"\\] or \"\", x\\[\"seq\"\\] or 0, x\\[\"rank\"\\], x\\[\"id\"\\]))/    return sorted(out, key=lambda x: (x[\"rank\"], x[\"date\"] is None, x[\"date\"] or \"\", x[\"seq\"] or 0, x[\"id\"]))/' app/backend/case_list.py && grep -n 'x\\[\"rank\"\\], x\\[\"id\"\\]\\|\"rank\"\\], x' app/backend/case_list.py; run; git -C $R show 926bf37:app/backend/case_list.py > app/backend/case_list.py\necho \"== restored check\"; diff <(git -C $R show 926bf37:app/backend/case_list.py) app/backend/case_list.py && echo identical",
 "description": "Run three mutants on the archive copy of case_list.py and restore",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:56:04.923Z

**tool result**
````
== MUT A: next_action picks last needs-review item instead of first
136:        w = waiting[-1]
.............                                                            [100%]
13 passed in 6.33s
== MUT B: next_action skips gate blockers entirely
131:    first = None
.............                                                            [100%]
13 passed in 7.64s
== MUT C: needs-review sorted by rank (entry/flag/amount) before date
117:    return sorted(out, key=lambda x: (x["rank"], x["date"] is None, x["date"] or "", x["seq"] or 0, x["id"]))
tests/unit/test_case_list.py:280: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_case_list.py::test_next_action_orders_by_record_date_not_by_kind_or_id
1 failed, 12 passed in 6.08s
== restored check
identical
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:56:21.873Z

**tool call — Bash**
````
{
 "command": "R=/Users/arsis/zlayt-pm-project; A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; S=\"$(dirname \"$A\")\"; cd \"$A\" && export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\"; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\necho \"== MUT D: rerun_available ignores the no-answer rerun\"\nsed -i '' 's/    return store.live_model_available() and not (last and last.get(\"verdict\") == \"unavailable\")/    return store.live_model_available()/' app/backend/present.py && grep -n \"return store.live_model_available()$\" app/backend/present.py; env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE $PY -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -3; git -C $R show 926bf37:app/backend/present.py > app/backend/present.py\necho \"== MUT E: title cut at 200 instead of 120\"\nsed -i '' 's/^MAX_TITLE = 120/MAX_TITLE = 200/' app/backend/case_list.py && grep -n \"^MAX_TITLE\" app/backend/case_list.py; env -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE $PY -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -2; git -C $R show 926bf37:app/backend/case_list.py > app/backend/case_list.py\necho \"== restored\"; diff -q <(git -C $R show 926bf37:app/backend/present.py) app/backend/present.py && diff -q <(git -C $R show 926bf37:app/backend/case_list.py) app/backend/case_list.py && echo restored-identical\necho \"== HTML probe (library create with HTML title, PATCH with HTML title)\"\ncat > \"$S/t157-html-probe.py\" <<'EOF'\nimport os, sys, tempfile\nA = sys.argv[1]; sys.path.insert(0, A)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp()\nc = TestClient(create_app(os.path.join(d, \"t.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\nlib = sorted(os.listdir(os.path.join(A, \"evals\", \"library\")))\nlid = [x for x in lib if x.endswith(\".txt\")][0][:-4]\nr = c.post(\"/api/cases\", json={\"library\": lid, \"title\": \"<img src=x onerror=alert(1)>Rivera\"})\nprint(\"create\", r.status_code, repr(r.json().get(\"title\")))\ntok = r.json()[\"token\"]\np = c.patch(f\"/api/cases/{tok}\", json={\"title\": \"<script>x</script>\\u0007Acme\"})\nprint(\"patch\", p.status_code, repr(p.json().get(\"title\")))\nprint(\"get\", repr(c.get(f\"/api/cases/{tok}\").json()[\"title\"]))\nEOF\nenv -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE $PY -I \"$S/t157-html-probe.py\" \"$A\" 2>&1 | tail -6",
 "description": "Run two more mutants, restore, and probe title HTML handling",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:56:35.559Z

**tool result**
````
== MUT D: rerun_available ignores the no-answer rerun
40:    return store.live_model_available()
=========================== short test summary info ============================
FAILED tests/unit/test_case_list.py::test_rerun_available_follows_live_mode_and_the_last_rerun
1 failed, 12 passed in 6.64s
== MUT E: title cut at 200 instead of 120
23:MAX_TITLE = 200
FAILED tests/unit/test_case_list.py::test_title_on_create_and_patch - Asserti...
1 failed, 12 passed in 5.65s
== restored
restored-identical
== HTML probe (library create with HTML title, PATCH with HTML title)
create 201 '<img src=x onerror=alert(1)>Rivera'
patch 200 '<script>x</script> Acme'
get '<script>x</script> Acme'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:56:48.570Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; sed -n 112,120p app/backend/present.py; echo ---; sed -n 192,200p app/backend/api.py; echo ---; grep -n \"def tray\\|tray\\b\" app/backend/present.py | head -8; echo ---; grep -n \"def item_view\" -A8 app/backend/present.py | head -14; echo ---; grep -n \"def review_view\\|rerun\" app/backend/review.py | head",
 "description": "Read tray/item view builders and body parsing in archive"
}
````

### User / tool · 2026-11-02T14:56:48.725Z

**tool result**
````
    return " ".join(([] if base == OK_WHY else [base]) + ex)


def flag_view(row, recs):
    c = _common(row)
    c["why"] = _gap_why(row, c["why"])
    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
            "explanation": row["explanation"], "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
---
    async def body_of(request: Request) -> dict:
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > MAX_BODY_BYTES:
            raise ApiError(413, "input_too_large", "Input is too large.")
        raw = b""
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > MAX_BODY_BYTES:
                raise ApiError(413, "input_too_large", "Input is too large.")
---
218:    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
314:    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, "entry"))      # T-110 r2: a record the paralegal entered by hand leaves the tray
318:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
321:    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
331:    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
332:    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
346:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
---
173:def item_view(conn, case_id, item_id):
174-    row = DB.get_item(conn, item_id, case_id)
175-    kind = _ID_KIND[item_id[0]]
176-    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
177-    v["kind"] = kind
178-    v["second_check_pending"] = item_id in second_check_pending_ids(conn, case_id)
179-    if kind == "flag":
180-        _with_gap_changes(conn, case_id, [v])
181-    return v
---
385:    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
628:    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:56:56.016Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; S=\"$(dirname \"$A\")\"; cd \"$A\"; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\ncat > \"$S/t157-probe2.py\" <<'EOF'\nimport os, sys, tempfile, time\nA = sys.argv[1]; sys.path.insert(0, A)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp()\nc = TestClient(create_app(os.path.join(d, \"t.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 50000))\nlid = sorted(x for x in os.listdir(os.path.join(A, \"evals\", \"library\")) if x.endswith(\".txt\"))[0][:-4]\ntok = c.post(\"/api/cases\", json={\"library\": lid}).json()[\"token\"]\nc.post(f\"/api/cases/{tok}/run\", json={})\nfor _ in range(240):\n    if c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] in (\"ready\", \"failed\"): break\n    time.sleep(0.25)\nfor body in ('\"title\"', '[\"title\"]', '{\"title\": 5}'):\n    r = c.patch(f\"/api/cases/{tok}\", content=body, headers={\"content-type\": \"application/json\"})\n    print(\"PATCH\", body, r.status_code, r.text[:90])\ncase = c.get(f\"/api/cases/{tok}\").json()\nit = case[\"entries\"][0]\nr = c.post(f\"/api/cases/{tok}/items/{it['id']}/review\", json={\"action\": \"dismiss\"})\nprint(\"review response item keys has rerun_available:\", \"rerun_available\" in r.json().get(\"item\", {}), r.json().get(\"item\", {}).get(\"rerun_available\"))\nprint(\"tray item has rerun_available key:\", [(\"rerun_available\" in t) for t in case.get(\"tray\", [])][:3], \"tray count\", len(case.get(\"tray\", [])))\nprint(\"next_action on GET case:\", case[\"next_action\"])\nEOF\nenv -u LLM_BACKEND -u ENABLE_LIVE -u ANTHROPIC_API_KEY -u ZLAYT_MODE $PY -I \"$S/t157-probe2.py\" \"$A\" 2>&1 | tail -12",
 "description": "Probe PATCH body edge cases and review-response rerun_available key",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:56:57.022Z

**tool result**
````
llm call failed call_id=c2a54532ac152 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
PATCH "title" 400 {"error":{"code":"bad_request","message":"Request body must be a JSON object.","detail":{}
PATCH ["title"] 400 {"error":{"code":"bad_request","message":"Request body must be a JSON object.","detail":{}
PATCH {"title": 5} 400 {"error":{"code":"bad_request","message":"Send {\"title\": text}.","detail":{}}}
review response item keys has rerun_available: True False
tray item has rerun_available key: [False] tray count 1
next_action on GET case: {'item_id': 'f_r3_1', 'kind': 'flag', 'reason': 'The AI found this flag but the phrase list did not; check that it applies.'}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:57:25.610Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nfrom app.backend import case_list as C\nfor n in ['case_01_', '.txt', 'case_lib01_', '  ']:\n    print(repr(n), '->', repr(C.readable_title(n, 'paste', 1762000000)))\n\"; echo \"--- review-evidence overlay vs HEAD tracked count:\"; git -C /Users/arsis/zlayt-pm-project ls-files artifacts/review-evidence | wc -l; echo \"--- e2e contract test location:\"; ls /Users/arsis/zlayt-pm-project/tests/unit | grep -i e2e_contract; ls /Users/arsis/zlayt-pm-project/tests | head; echo \"--- unit-suite test count fields in card vs run\"; grep -n \"4387\" /Users/arsis/zlayt-pm-project/board/cards/T-157.md | head -2",
 "description": "Probe readable_title edge names and locate e2e contract test for count reconciliation",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T14:57:25.793Z

**tool result**
````
Traceback (most recent call last):
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'app'
--- review-evidence overlay vs HEAD tracked count:
       1
--- e2e contract test location:
test_e2e_contract.py
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
--- unit-suite test count fields in card vs run
18:  - {"n": 1, "text": "title create/PATCH/default with tests; rerun_available per item with tests; next_action deterministic (blockers first, then needs-review in timeline order); api.md; case_list stays consistent with GET case (existing drift test extended)", "done": true, "evidence": "tests/unit/test_case_list.py (13 tests: title create/PATCH/default/never Untitled, rerun_available fixture/live/no-answer, next_action order + drift vs GET case for every library case) pass; full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend); api.md updated; commit 926bf37"}
27:- 2026-11-02T14:47:03Z backend: AC 1 checked: tests/unit/test_case_list.py (13 tests: title create/PATCH/default/never Untitled, rerun_available fixture/live/no-answer, next_action order + drift vs GET case for every library case) pass; full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend); api.md updated; commit 926bf37
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:57:30.607Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nfrom app.backend import case_list as C\nfor n in ['case_01_', '.txt', 'case_lib01_', '  ']:\n    print(repr(n), '->', repr(C.readable_title(n, 'paste', 1762000000)))\n\"; echo \"--- e2e test counts\"; cd \"$A\" && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=\"$A\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/test_e2e_contract.py -q -p no:cacheprovider --co 2>&1 | tail -2",
 "description": "Check readable_title edge names and collect e2e contract tests",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T14:57:31.083Z

**tool result**
````
'case_01_' -> 'Records added Nov 1'
'.txt' -> 'Records added Nov 1'
'case_lib01_' -> 'Records added Nov 1'
'  ' -> 'Records added Nov 1'
--- e2e test counts

no tests collected in 0.00s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:57:53.594Z

**tool call — Bash**
````
{
 "command": "A=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-r1/archive\"; cd \"$A\"; grep -n \"^MAX_TITLE\\|^def clean_title\\|^def derived_title\\|^def case_title\\|^def next_action\\|first = next(\\|w = waiting\\[0\\]\\|^def needs_review_order\\|return sorted(out\" app/backend/case_list.py; grep -n \"^def rerun_available\\|return store.live_model_available\" app/backend/present.py; grep -n \"def live_model_available\" app/backend/store.py; grep -n \"def rename_case\\|DB.update_case(c, token, name=\\|given = b.get\\|title: str = None\" app/backend/api.py; grep -n \"def test_\" tests/unit/test_case_list.py | sed -n 1,20p; grep -n \"if other:\" tests/unit/test_case_list.py; grep -n \"if item_blockers:\" tests/unit/test_case_list.py; grep -n \"dates_to_confirm\\|innerHTML\" app/frontend/dom.js | head -2; grep -n \"ZL.el = function\" app/frontend/dom.js; grep -n \"Untitled\" app/frontend/overview.js; ls /Users/arsis/zlayt-pm-project/reviews | grep \"T-157\" ; echo \"exists-check done\"",
 "description": "Collect exact line numbers for citations and check for existing T-157 review"
}
````

### User / tool · 2026-11-02T14:57:53.832Z

**tool result**
````
23:MAX_TITLE = 120
27:def clean_title(value) -> str:
32:def derived_title(conn, case_id) -> str:
61:def case_title(conn, case: dict) -> str:
96:def needs_review_order(conn, case_id) -> list:
117:    return sorted(out, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
120:def next_action(conn, case_id, case: dict = None, blockers: list = None):
131:    first = next((b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"), None)
136:        w = waiting[0]
37:def rerun_available(row) -> bool:
40:    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")
11:def live_model_available() -> bool:
248:        given = b.get("title") if isinstance(b.get("title"), str) else b.get("name")          # T-157: `title` is the name a paralegal types; `name` stays accepted
252:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
328:    async def rename_case(token: str, request: Request):
336:            DB.update_case(c, token, name=case_list.clean_title(b["title"]) or None)
71:def test_list_covers_every_case_newest_first(local, cases):
77:def test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):
117:def test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):
126:def test_decided_cases_cover_ready_and_edit_to_check(local, cases):
135:def test_title_is_readable_not_a_file_slug(local, cases):
149:def test_list_is_code_only_no_text_no_model_calls(local, cases):
159:def test_list_is_404_outside_local_mode(local, monkeypatch):
165:def test_default_title_comes_from_the_first_record_header(local, cases):
174:def test_title_on_create_and_patch(local, cases):
196:def test_titles_are_never_untitled(local, cases):
203:def test_rerun_available_follows_live_mode_and_the_last_rerun(local, cases, monkeypatch):
232:def test_next_action_blockers_first_then_needs_review_in_timeline_order(local, cases):
272:def test_next_action_orders_by_record_date_not_by_kind_or_id(local, cases):
228:    if other:
249:        if item_blockers:                                                              # a gate blocker is the first thing, in gate order
5:  ZL.el = function (tag, attrs, ...kids) {
51:  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
exists-check done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:58:46.338Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer.md",
 "content": "# T-157 review: staff-engineer-reviewer (commit 926bf37)\n\nVerdict: **changes** (0 blockers, 3 majors, 3 minors, 2 nits). Verdict rule: no blocker, so not fail; majors present, so changes.\n\nScope: commit 926bf37 (HEAD at review time). Reviewed on a `git archive 926bf37` copy in my scratchpad. Untracked `artifacts/review-evidence` (1576 files) was overlaid with no-clobber because `tests/unit` reads it. Fixture backend, in-process TestClient, no live app URL.\n\nWhat holds: the code implements the four brief items. Title create, PATCH rename and the derived default work, and the default is never \"Untitled case\". `rerun_available` is false in demo/fixture mode and after a no-answer rerun. `next_action` is code-only, with blockers ahead of needs-review items and a total sort key that ends in the item id. The 13 `test_case_list.py` tests pass, and the full `tests/unit` run has no failures on this copy.\n\nWhat does not hold: the brief asks for HTML validation of titles, and there is none. Two `next_action` rules (blockers first, first-in-timeline pick) have no test that fails when they break. Two mutants survive, so the tests do not prove the AC.\n\nFindings (detail in the JSON block):\n1. major: titles are stored and returned with markup unchanged. Not exploitable in the shipped UI, because the frontend writes text nodes.\n2. major: blockers-first rule is untested. Mutant `first = None` leaves all 13 tests green.\n3. major: first-in-timeline pick is untested. Mutant `waiting[-1]` leaves all 13 tests green.\n4. minor: the card's full-suite evidence (4387 passed, 2 failed) does not reproduce at 926bf37. My run gave 4286 passed, 8 skipped, 0 failed.\n\n```json\n{\"card\": \"T-157\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 926bf37 (HEAD at review time): app/backend/api.py, case_list.py, present.py, store.py, memory/contracts/api.md, tests/unit/test_case_list.py. Reviewed on a git archive copy of 926bf37 with untracked artifacts/review-evidence overlaid (tests read it). Fixture backend, in-process TestClient, no app URL. Case under test: evals/library case_lib01_er_only_then_gap (plus a pasted-and-named case and a library-created title case).\",\n \"exercised\": [\n  \"python3 tools/board.py show T-157 (card AC, handoff, rounds 0, commits 926bf37)\",\n  \"cat memory/contracts/api.md; sections read: conventions line 46 (untrusted strings are plain text), POST /api/cases (line 60, title), PATCH row (line 54), GET case rerun_available (line 132), next_action (line 705), Case titles (line 703)\",\n  \"git show --stat 926bf37; git show 926bf37 -- app/backend/api.py app/backend/case_list.py app/backend/present.py app/backend/store.py memory/contracts/api.md tests/unit/test_case_list.py (full diff read)\",\n  \"git archive 926bf37 | tar -x into the scratchpad archive dir; overlaid artifacts/review-evidence with cp -Rn (1576 untracked files)\",\n  \".venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '13 passed in 8.00s'\",\n  \".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider on the archive: '4286 passed, 8 skipped in 275.41s (0:04:35)', 0 failed (full output at the scratchpad full-unit.out file)\",\n  \"mutant A: case_list.py:136 'w = waiting[0]' -> 'waiting[-1]'; pytest test_case_list.py: '13 passed in 6.33s' (survived)\",\n  \"mutant B: case_list.py:131 'first = next(...)' -> 'first = None'; pytest test_case_list.py: '13 passed in 7.64s' (survived)\",\n  \"mutant C: case_list.py:117 sort key with rank before date; pytest: '1 failed, 12 passed' (killed by test_next_action_orders_by_record_date_not_by_kind_or_id)\",\n  \"mutant D: present.py:40 drops the no-answer clause; pytest: '1 failed, 12 passed' (killed by test_rerun_available_follows_live_mode_and_the_last_rerun)\",\n  \"mutant E: case_list.py:23 MAX_TITLE 120 -> 200; pytest: '1 failed, 12 passed' (killed by test_title_on_create_and_patch)\",\n  \"every mutant file restored from 'git show 926bf37:<path>' and confirmed identical with diff -q\",\n  \"HTML probe (scratchpad t157-html-probe.py, run with python -I, fixture env): POST /api/cases library + title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH title '<script>x</script>\\\\u0007Acme' -> 200 title '<script>x</script> Acme'; GET case returns the same string\",\n  \"PATCH body probe (scratchpad t157-probe2.py): body JSON string '\\\"title\\\"' -> 400 bad_request; body '[\\\"title\\\"]' -> 400 bad_request; {\\\"title\\\": 5} -> 400 bad_request\",\n  \"review response for a dismiss carries item.rerun_available = false (fixture); GET case tray item has no rerun_available key\",\n  \"readable_title probe: 'case_01_' -> 'Records added Nov 1'; '.txt' -> same; 'case_lib01_' -> same; '  ' -> same\",\n  \"read app/backend/api.py:116-119 (live_enabled, demo_mode = not live_enabled) against app/backend/store.py:11-16 (live_model_available)\",\n  \"read app/backend/rejudge.py:64-80 and review.py:385 (rejudge attempts stored with verdict; edit pops ladder.rejudge)\",\n  \"grep for 'Untitled' in app tests tools evals; grep for case name/title readers in app (none reach a prompt, the letter or the export)\",\n  \"frontend sinks: app/frontend/dom.js:5-17 (ZL.el writes text nodes), app/frontend/overview.js:51 and 76-84 (title passed to el as text); grep for innerHTML on title paths (none)\",\n  \"grep for bare except / except: pass in the diff (none added; only try/finally in get_case_view)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"card_acs_implemented\": 4, \"tests_prove_acs\": 2, \"title_input_validation\": 2, \"rerun_available_correct\": 4, \"next_action_determinism\": 4, \"contract_consistency\": 3, \"honest_failure\": 4},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Case titles are not validated for HTML (brief check fails); markup is stored and returned verbatim\",\n   \"evidence\": \"Probe output (scratchpad t157-html-probe.py, python -I): create with title '<img src=x onerror=alert(1)>Rivera' -> 201 title '<img src=x onerror=alert(1)>Rivera'; PATCH '<script>x</script>\\\\u0007Acme' -> 200 '<script>x</script> Acme'; GET case same. Code: app/backend/case_list.py:23-29 clean_title only maps control characters and collapses whitespace, then truncates to 120; no markup check. Derived default copies record text: case_list.py:32-47 derived_title uses clean_title(r['source_label']) on the Source header of a record, which api.md line 46 treats as untrusted. The contract's plain-text rule (api.md:46) lists record text, excerpts and summaries but not titles.\",\n   \"why_it_matters\": \"The brief requires titles validated for length and HTML. Length is validated (120, test_case_list.py:185-186); HTML is not. Not a live XSS today: app/frontend/dom.js:5-17 writes text nodes and overview.js:76-84 passes the title to el() as text. But the value is untrusted record text in a field the contract does not cover, so the first innerHTML sink added later becomes stored XSS. Rated major (not blocker) because no current sink renders markup; this is a missed required check, not an unsafe shipped path.\",\n   \"fix\": \"Decide the rule and enforce it in clean_title. Either reject typed titles containing < or > with 400 bad_request (detail.reason 'title_markup'), and strip tags from derived titles (source label becomes plain text), or document titles as plain text in api.md line 46 and keep the derived text escaped. Add both to the api.md title paragraph (line 703).\",\n   \"acceptance_test\": \"Unit: clean_title('<img src=x onerror=alert(1)>Rivera') contains no '<' (or the typed path returns 400 bad_request). Integration: POST /api/cases with title '<script>x</script>' returns 400 bad_request, and PATCH with the same returns 400 and leaves the stored name unchanged. Derived title for a record with Source '<b>Clinic</b>' contains no '<'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"next_action blockers-first rule has no test that fails when it breaks (mutant survives)\",\n   \"evidence\": \"app/backend/case_list.py:131 'first = next((b for b in blockers if b[\\\"reason_code\\\"] != \\\"NOTHING_ACCEPTED\\\"), None)' mutated to 'first = None' (scratch archive only). '.venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider' -> '13 passed in 7.64s'. The only blocker assertion is tests/unit/test_case_list.py:248-251 and it runs only for a library case that has an item blocker; under the mutant that assertion would fail, so no case in the suite reaches it. api.md:705 says 'tests/unit/test_case_list.py ... checks the order rules'.\",\n   \"why_it_matters\": \"T-157 AC says next_action must be blockers first. A regression that surfaces a waiting item ahead of an export blocker (for example a JUDGE_NOT_RUN accept) would pass CI, and the paralegal would be sent to the wrong item. This is the determinism rule the card exists for.\",\n   \"fix\": \"Add a case where an accepted AI-made item has no second-check answer (JUDGE_NOT_RUN) or a code-check failure on an accepted edit, while other items still wait. Assert next_action equals the blocker, and assert the scenario was actually built (no silent skip). Also add an assertion that next_action is None-free when a blocker exists.\",\n   \"acceptance_test\": \"Scratch mutant 'first = None' in case_list.py:131 must turn the new test red. Test asserts next_action == {item_id, kind, reason} of the export-gate blocker, with a needs-review item present in the same case.\"},\n  {\"severity\": \"major\",\n   \"title\": \"next_action timeline pick is untested (mutant survives); test only checks the sort of its own helper\",\n   \"evidence\": \"app/backend/case_list.py:136 'w = waiting[0]' mutated to 'w = waiting[-1]' (scratch archive only); pytest tests/unit/test_case_list.py -> '13 passed in 6.33s'. tests/unit/test_case_list.py:253-256 only asserts that next_action names some needs-review item. tests/unit/test_case_list.py:272-283 asserts that needs_review_order's own output is sorted by the same key the code uses (order == sorted(order, key=...)), which does not test the pick.\",\n   \"why_it_matters\": \"The AC says the single first thing is the first needs-review item in timeline order. Nothing proves the field is that item, so a change to the index or to the review order would pass. The api.md line 703 claim that the tests 'check the order rules' overstates the coverage.\",\n   \"fix\": \"For each library case with a waiting item and no blocker, assert next_action['item_id'] == case_list.needs_review_order(conn, tok)[0]['id'], and assert the chosen item's cited record date is the earliest of the waiting set. Include a case where kind order and date order disagree, so the test cannot pass on id or kind alone.\",\n   \"acceptance_test\": \"Scratch mutant 'waiting[-1]' at case_list.py:136 must turn the test red. Test: for every library case with waiting items and no blocker, next_action.item_id equals the earliest-dated waiting item.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Card evidence for the full unit suite does not reproduce at 926bf37\",\n   \"evidence\": \"board/cards/T-157.md AC evidence: 'full tests/unit 4387 passed, 2 failed (test_e2e_contract ids declared by frontend, not backend)'. My run on the 926bf37 archive (with review-evidence overlay): '4286 passed, 8 skipped in 275.41s', 0 failed. .venv/bin/python -m pytest tests/test_e2e_contract.py --co reports 'no tests collected', and the file is not under tests/unit.\",\n   \"why_it_matters\": \"Evidence that cannot be reproduced cannot support the verdict. The worker may have run a dirty working tree (git status shows uncommitted product files from other cards). Not a code defect in T-157, but the card cites a file outside the suite it names.\",\n   \"fix\": \"Rerun 'python3 -m pytest tests/unit -q' from a clean archive of the commit, paste the exact command and tail into the card AC evidence, and drop the test_e2e_contract line unless it is reproduced in tests/unit.\",\n   \"acceptance_test\": \"Card AC evidence includes the command and the pytest summary line, and it matches a fresh git archive run.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"rerun_available re-derives the demo/live rule instead of using the one that defines demo mode\",\n   \"evidence\": \"app/backend/store.py:11-16 live_model_available() = name != 'fixture' and ENABLE_LIVE == '1' and (claude-cli or ANTHROPIC_API_KEY). app/backend/api.py:116-119 live_enabled() = ENABLE_LIVE == '1' and (backend() == 'claude-cli' or key); demo_mode() = not live_enabled(). The two agree by reading today, but two definitions of 'live' can drift, and the spec says demo mode is the gate.\",\n   \"why_it_matters\": \"If the two drift, the item could say a rerun can answer in demo mode, which is the failure the AC forbids. Nothing in the suite asserts they agree.\",\n   \"fix\": \"Have present.rerun_available use the same demo_mode/live function as the API (move the definition to one module), and add a parametrized test over LLM_BACKEND, ENABLE_LIVE and ANTHROPIC_API_KEY asserting rerun_available is False whenever demo_mode() is True.\",\n   \"acceptance_test\": \"Parametrized test: for each env combination, rerun_available == (not demo_mode()) for a fixture item.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The anthropic-api-without-key assertion is conditional and can pass without checking anything\",\n   \"evidence\": \"tests/unit/test_case_list.py:227-229: 'other = [...][:1]' then 'if other: assert other[0][\\\"rerun_available\\\"] is False'.\",\n   \"why_it_matters\": \"If the library case has no flags or amounts, the no-key branch asserts nothing, and a regression would pass silently.\",\n   \"fix\": \"Name a specific item id from the case and assert on it unconditionally.\",\n   \"acceptance_test\": \"Test asserts rerun_available is False for a named flag or amount with LLM_BACKEND=anthropic-api and no key, without an if-guard.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"PDF title query parameter is untested\",\n   \"evidence\": \"app/backend/api.py:252 create_case_from_pdf(..., title: str = None) and the make_case call passing 'title if title is not None else name'. No test in tests/unit/test_case_list.py posts to /api/cases/pdf with title. api.md line 60 documents the parameter.\",\n   \"why_it_matters\": \"A documented input path with no test can regress (for example the name would be dropped), and nothing would fail.\",\n   \"fix\": \"Add one test posting an existing synthetic PDF fixture with ?title= and asserting the returned title and GET case title.\",\n   \"acceptance_test\": \"POST /api/cases/pdf?title=Rivera%20intake returns 201 and title 'Rivera intake'. (Not run by me.)\"},\n  {\"severity\": \"nit\",\n   \"title\": \"A stored name that is empty after cleanup skips the record-header default\",\n   \"evidence\": \"Probe: readable_title('case_01_', 'paste', ...) -> 'Records added Nov 1'; '.txt' and 'case_lib01_' give the same. app/backend/case_list.py:61-65 case_title uses readable_title whenever name is non-blank, so the header default (api.md:703 rule 2) is never reached for such names.\",\n   \"why_it_matters\": \"Still never 'Untitled case', so no contract breach. The title is less useful than the first record header and differs from the documented order.\",\n   \"fix\": \"Treat an empty readable name as no name and fall through to derived_title.\",\n   \"acceptance_test\": \"case_title for a case named 'case_01_' returns the derived header title when a record has a Source line.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Frontend still carries an Untitled case fallback (outside this commit)\",\n   \"evidence\": \"app/frontend/overview.js:51 titleOf: '... || \\\"Untitled case\\\"'. Unreachable today because the backend always sends a non-empty title.\",\n   \"why_it_matters\": \"Dead text, but it is the string the AC bans, and a future backend null would show it.\",\n   \"fix\": \"Route to the frontend card: drop the fallback and fall back to the backend title only.\",\n   \"acceptance_test\": \"grep -rn 'Untitled case' app/frontend returns nothing.\"}\n ],\n \"whats_right\": [\n  \"next_action and needs_review_order are code-only and deterministic: the sort key ends in the item id (case_list.py:117) and the no-model-call test passes.\",\n  \"rerun_available is false in fixture/demo mode and after a no-answer rerun; the review response carries it and tray items omit it, as api.md requires (mutant D killed).\",\n  \"PATCH rejects non-object bodies, non-text titles and unknown tokens with explicit 400/404, and the 120-character cap is enforced by test (mutant E killed).\"\n ],\n \"questions_for_chris\": [\n  \"For typed titles that contain < or >, do you want a 400 (reject) or stored-as-text with escaping at the sink? The answer decides the fix for finding 1.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T14:58:46.546Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:58:52.161Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,re\nt=open('reviews/T-157-staff-engineer.md').read()\nm=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(m))\nd=json.loads(m[0])\nprint(d['card'], d['persona'], d['model'], d['verdict'])\nfrom collections import Counter\nprint(Counter(f['severity'] for f in d['findings']))\nsev=[f['severity'] for f in d['findings']]\nmx='blocker' if 'blocker' in sev else 'major' if 'major' in sev else 'pass'\nexp={'blocker':'fail','major':'changes','pass':'pass'}[mx]\nprint('verdict rule expects', exp, 'got', d['verdict'], 'OK' if exp==d['verdict'] else 'MISMATCH')\n\"",
 "description": "Validate the review JSON block parses and matches the verdict rule"
}
````

### User / tool · 2026-11-02T14:58:52.217Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:58:57.065Z

**tool call — Bash**
````
{
 "command": "cat > \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-check-json.py\" <<'EOF'\nimport json, re, sys\nfrom collections import Counter\nt = open(sys.argv[1]).read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(d[\"card\"], d[\"persona\"], d[\"model\"], d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(Counter(sev))\nmx = \"blocker\" if \"blocker\" in sev else \"major\" if \"major\" in sev else \"pass\"\nexp = {\"blocker\": \"fail\", \"major\": \"changes\", \"pass\": \"pass\"}[mx]\nprint(\"verdict rule expects\", exp, \"got\", d[\"verdict\"], \"OK\" if exp == d[\"verdict\"] else \"MISMATCH\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t157-check-json.py\" /Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer.md",
 "description": "Validate review JSON block with a scratch script and check verdict rule"
}
````

### User / tool · 2026-11-02T14:58:57.168Z

**tool result**
````
json blocks: 1
T-157 staff-engineer-reviewer claude-haiku-5-5 changes
Counter({'minor': 4, 'major': 3, 'nit': 2})
verdict rule expects changes got changes OK
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:58:59.450Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-157-staff-engineer.md",
 "old_string": "Verdict: **changes** (0 blockers, 3 majors, 3 minors, 2 nits).",
 "new_string": "Verdict: **changes** (0 blockers, 3 majors, 4 minors, 2 nits)."
}
````

### User / tool · 2026-11-02T14:58:59.496Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-157-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:59:08.580Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md",
 "content": "---\nname: t157-case-title-next-action-patterns\ndescription: T-157 r1 926bf37 (changes): next_action blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card full-suite counts do not reproduce, archive needs review-evidence overlay\nmetadata:\n  type: project\n---\n\nT-157 r1 at 926bf37 was verdict changes (3 majors, 4 minors, 2 nits). Reviewer file reviews/T-157-staff-engineer.md is write-once.\n\n- **Survivors in a new ordering feature.** Mutants that break the blockers-first rule (`first = None`) and the timeline pick (`waiting[-1]`) both left all 13 tests green. The tests asserted membership and the helper's own sort, not the chosen item. Lesson: for any \"single first item\" field, mutate the selection index and the precedence branch, not only the sort key.\n- **Titles.** Length cap (120) was tested, HTML was not. Record text (Source header) flows into the derived default title. The frontend writes text nodes, so it is not exploitable today; rate major, not blocker, and escalate if an innerHTML sink appears.\n- **Evidence numbers.** The card claimed 4387 passed / 2 failed in tests/unit; the same commit gave 4286 passed, 8 skipped, 0 failed. Its failing file (test_e2e_contract) is not under tests/unit. Check card evidence against a clean archive run.\n- **Archive needs untracked fixtures.** `git archive` omits artifacts/review-evidence (untracked), so tests/unit collection fails with FileNotFoundError until it is overlaid with `cp -Rn` from the working tree. Same root as [[project_round2_snapshot_review_patterns]].\n- **Working tree is dirty with other cards.** `git status` showed uncommitted app/ changes from other workers; always review the archive of the commit, never the working tree.\n- **Reviewer write guard.** After the first Write, an Edit to the same reviews file is denied (append-only). A count typo in the summary could not be corrected; get the markdown summary right before the first Write.\n\n**Why:** the card AC said \"blockers first, then timeline order\", and the suite could not tell a correct next_action from a wrong one.\n**How to apply:** on any future \"next item\" or \"single first thing\" field, run mutants on the selection index and each precedence branch; expect red. See [[project_gate_m2_patterns]] for gate blocker ordering.\n"
}
````

### User / tool · 2026-11-02T14:59:08.696Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:59:11.697Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 120
}
````

### User / tool · 2026-11-02T14:59:11.710Z

**tool result**
````
<system-reminder>Warning: the file exists but is shorter than the provided offset (120). The file has 80 lines.</system-reminder>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:59:13.125Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "offset": 75,
 "limit": 6
}
````

### User / tool · 2026-11-02T14:59:13.131Z

**tool result**
````
75	- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — r1 changes: untracked ledger read at import breaks clean collection, golden-named test without golden compare, git show not working tree, HEAD moved 3x
76	- [T-146 r3 patterns](project_t146_r3_patterns.md) — bf53087 changes: equal-rank check worsening replaces decided item silently, reword fails case, rerun_note no UI consumer
77	- [T-141 r5 patterns](project_t141_r5_patterns.md) — 52ac285 changes: verb-only mechanism gate; noun forms, injury words and 'last year' stay info in-window; relative return precedes gate; gate mutant pinned
78	- [T-155 e2e triage patterns](project_t155_e2e_triage_patterns.md) — 20b3a42 changes (r1b): green claim on older sha, "stale" density reds were real, hidden list 0 px + 8px margin, refusal box btn_y+132
79	- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a "stale test" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between
80	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:59:15.344Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a \"stale test\" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between\n",
 "new_string": "- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — before accepting a green run or a \"stale test\" triage, run the cited test at the evidence sha and at the reviewed commit; count commits between\n- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — 926bf37 changes: blockers-first and timeline-pick mutants survive, titles unvalidated for markup, card counts not reproduced, archive needs review-evidence overlay\n"
}
````

### User / tool · 2026-11-02T14:59:15.452Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:59:17.159Z

T-157 (926bf37): changes, 0 blockers, 3 majors (title HTML unvalidated; blockers-first and timeline-pick untested, mutants survive); `reviews/T-157-staff-engineer.md` written, JSON valid. Its summary line says "3 minors" but there are 4; the write guard blocked the fix.
