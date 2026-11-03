# Subagent: Backend: T-214 phrase-list flag label (Backend: T-214 phrase-list flag label)

Source: `agent-af80ea6427ab7028f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T13:23:57.547Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim the newest backend card, "Flags found only by the phrase list…" (find it with `python3 tools/board.py list --role backend`). Speed rule D-075 applies: targeted tests only.

On the sample, flag f_r7_1 carries prepared=true and a "Prepared answer" tag, but only the code phrase list found it. Under D-065 that misstates its origin. Set prepared=false for items whose only source is code, and give them an origin such as "Found by code (phrase list)". Keep prepared=true only for items with a curated answer.

Run the prepared-property test, the provenance tests and the sample tests from a `git archive` copy. Another backend worker may be editing export.py and service_date.py (T-202), so stay out of those files. Commit with a temp index and `git commit`, move the card to in_review, and reply in 1 line.

### User / tool · 2026-11-03T13:23:57.553Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:00.455Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list --role backend | tail -15; cat .claude/agent-memory/backend/project_t177_r5_twin_guard.md | head -30"
}
````

### User / tool · 2026-11-03T13:24:00.602Z

**tool result**
````
T-167	M3	backend    	cancelled        	P0	AC 1/1	MVP backend wording (T-166 audit F4/F7): no developer codes or test-mode wording in paralegal-facing text or the exported notes (JUDGE_UNAVAILABLE, fixture backend, curated responses, 'server answered 500'); demo-mode edit wording is plain
T-168	M2	backend    	done             	P0	AC 1/1	Demo: lib01 reads 'failed' since T-165 because record 3 has no recorded extract answer; record that one answer live (claude-cli, D-056) so the demo case runs clean
T-170	M3	backend    	cancelled        	P1	AC 0/1	Internal notes accuracy (GATE-M2 r2 adjuster majors): lib15 a 12-visit future-care estimate is labelled 'Rate $1,800/visit'; the accident-date line can call a pre-accident visit the 'First recorded treatment'
T-171	M2	backend    	done             	P0	AC 1/1	D-064: the review screen says why an amount is not counted in plain words, and a line not counted only for a missing detail (no date of service / no bill header) can be counted with a named confirm (lib11 $250/$180/$2,310)
T-175	M3	backend    	done             	P0	AC 1/1	Intermittent HTTP 500 on GET /api/cases (case overview) seen during e2e (T-173 review); find the race and fix it
T-176	M3	backend    	cancelled        	P2	AC 0/1	Undo on a counted line should restore it to Unclear (kind unclear, Count this charge button), not leave a pending Charge
T-177	M3	backend    	done             	P0	AC 1/1	GATE-M3 blocker (D-065): curated demo answers must never be labelled as AI output - badge, 'Prepared answer' tags, trace step and audit model 'hand-checked (qa)'; recorded answers keep AI labels
T-178	M3	backend    	done             	P0	AC 1/1	GATE-M3 chaos blocker+majors: a run interrupted by a server restart stays 'running' forever (no export, no re-run); a stale second tab silently overrides a dismissal; zero-width-only paste passes the empty check and spends model calls; a lone surrogate in a paste returns 500
T-183	M4	backend    	done             	P0	AC 1/1	M4 hardening check: server-side key never exposed, per-session rate limit and spend cap on live calls, demo mode serves the prepared sample answers with no key, optional bring-your-own-key, input size limits, error states; fill only real gaps
T-196	M3	backend    	done             	P1	AC 1/1	api.md: D-066 compare stamp wording matches behaviour (not atomic; taken back on failure)
T-197	M3	backend    	done             	P0	AC 1/1	GET /api/health reports local_mode so the guided UI never probes /api/cases or /api/library in public mode (T-181 r2 first-paint 404)
T-200	M3	backend    	done             	P0	AC 1/1	Letter: counted undated ledger lines must not print the statement date as a service date (lib11 'itemized ledger, June 15, 2026')
T-201	M3	backend    	done             	P0	AC 1/1	Fix 2 e2e failures at HEAD after T-177 r5 wording (test_edit_to_check re-picked quote; test_letter_matrix no AI text in letter, sample)
T-202	M3	backend    	in_progress      	P0	AC 1/1	D-071: letter charge lines print the bill's service date or period, not the statement date (case_09, lib14, lib10)
T-214	M3	backend    	ready            	P0	AC 0/1	Flags found only by the phrase list (code) are not labelled 'Prepared answer' (sample f_r7_1): prepared=false, tag says found by code
---
name: t177-r5-twin-guard
description: T-177 r5 - what the "AI summary leak" actually was, the property-test action pass, static twin test, mutant recipe on a git archive
metadata:
  type: project
---

At HEAD the "AI summary" strings in trace.py:348 / why.py were already the prepared twins; the r4 reviewer's B2/B4/C5 were mutants, not live leaks. The real live leak found in r5 was `review._check_summary`: the edit/manual-entry JUDGE_UNAVAILABLE warning called `why.unavailable_sentence(...)` without `prep` ("The AI second check is not available in this demo"). Fixed by passing `prep` (edit: `present.Prov(conn, case_id).prepared(item)`; manual: `AU.answers_prepared()`).

**Why:** the lookups are `(TWIN.get(code) if prep else None) or AI_TEXT`, so a missing twin or a missing `prep` argument falls back to AI wording silently.
**How to apply:** any new sentence that names an AI/model needs a twin under the same code AND a call path that passes `prep`. tests/unit/test_prepared_property.py guards both: static twin completeness (`why._WHY`/`trace.TRACE_WHY`/`trace._NEXT` vs their `_PREPARED`), the `unsupported` fault, and `actions()` (edit quote -> read -> accept -> read, plain accept, hand entry for records with no live entry). `collect(..., do_actions=False)` for tests that need a clean export.

Pitfalls: edit of a prepared entry's quote is refused (422) if the summary keeps a number the shorter quote lacks, so the action pass tries whole-sentence runs longest first. Mutant recipe: `git archive <sha> | tar -x -C dir`, exact-string replace + restore bytes, run property file only (~55 s each). Main index may carry other workers' staged changes (even a staged `D` of my test file): commit with `GIT_INDEX_FILE=<fixed path>`, `read-tree HEAD`, `git add <3 paths>`, `git commit -- <paths>`, never touch the real index.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:02.661Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-214 --agent backend; $B show T-214; grep -rn \"Prepared answer\\|\\\"prepared\\\"\\|prepared=\" app/backend app/llm --include=*.py | grep -v \"^app/backend/export.py\\|service_date\" | head -60"
}
````

### User / tool · 2026-11-03T13:24:02.838Z

**tool result**
````
T-214 claimed by backend
---
id: "T-214"
title: "Flags found only by the phrase list (code) are not labelled 'Prepared answer' (sample f_r7_1): prepared=false, tag says found by code"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T13:23:54Z"
updated_at: "2026-11-03T13:24:02Z"
claimed_by: "backend"
claimed_at: "2026-11-03T13:24:02Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "an item whose only source is the code phrase list has prepared=false and a 'Found by code' origin; prepared stays true only for curated answers; unit test over the sample and the curated set; property test still green", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T13:24:02Z backend: claimed

## Handoff (filled when moving to in_review)

app/backend/store.py:215:    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events, prepared=prep)
app/backend/trace.py:216:PREPARED_LABEL = "Prepared answer"      # D-069: the D-065 wording minus its "standing in for the AI draft" tail (only the badge tooltip may say AI)
app/backend/trace.py:217:PREPARED_WHY = "Prepared answer (hand-checked by the team for the demo)"
app/backend/trace.py:221:PREPARED_FLAGS_LABEL = "Prepared answers did not include this flag"
app/backend/trace.py:251:                    "prepared": bool(call) and AU.is_prepared(call.get("recorded_from"))}}      # D-065: a hand-checked fixture answer, not model output
app/backend/trace.py:252:    ev["prompt_version"] = None if ev["model"]["prepared"] else ((call or {}).get("prompt_version") or prompt_version)      # a prepared answer was prompted by nothing (T-177 r3)
app/backend/trace.py:471:        prep = ev["model"]["prepared"] or (not (call and call.get("recorded_from")) and cx.answers_prepared)      # D-065 (T-177 r3): a failed or missing prepared answer is still a prepared answer, never "AI drafted"
app/backend/trace.py:472:        if prep and not ev["model"]["prepared"]:
app/backend/trace.py:491:            if ev["model"]["prepared"]:
app/backend/trace.py:774:        if ev["model"]["prepared"]:
app/backend/trace.py:850:    if ev["model"]["prepared"]:
app/backend/trace.py:1042:            "rerun_no_answer": tried, "prepared": _PREP.get(), "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}
app/backend/trace.py:1175:    xev = {"evidence": {"model": {"id": present.PREPARED_MODEL, "role": "generator", "independent_of_generator": None, "prepared": True}}} if prep else {}
app/backend/present.py:310:        v["prepared"] = prepared
app/backend/present.py:312:            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
app/backend/present.py:342:    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
app/backend/present.py:351:    return {**nar, "prepared": prepared, "generator": {**nar["generator"], "prepared": prepared, **({"model": call["model"]} if prepared else {})}}
app/backend/present.py:552:         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"], "prepared": prep}      # D-065: a hand-checked fixture answer, not model output
app/backend/api.py:135:        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
app/backend/api.py:143:        prepared = answers() == "prepared"
app/backend/api.py:144:        return dict(base, generator=present.PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
app/backend/api.py:268:                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
app/backend/export_routes.py:59:        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items), all(i.get("prepared") for i in e.items))      # D-069: the blockers carry the case's provenance
app/llm/audited.py:78:    return P.backend_name() == "fixture" and fixture.answer_source() == "prepared"
app/llm/backends/fixture.py:50:    return "prepared" if fixture_dir().name == "curated" else "recorded"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:05.728Z

**tool call — Bash**
````
{
 "command": "sed -n 285,360p app/backend/present.py; grep -n \"class Prov\" -A60 app/backend/present.py | head -120; ls tests/unit | grep -i \"prepar\\|proven\""
}
````

### User / tool · 2026-11-03T13:24:05.823Z

**tool result**
````
    def first_call(self, row):
        """The generator call behind the item: its ladder's call, else the item's last generator call, else (a flag) its record's flag call."""
        gen = (row.get("ladder") or {}).get("generator")
        call = self.by_id.get((gen or {}).get("call_id")) or next(iter(reversed(self.by_item.get(row["id"], []))), None)
        if call is None and str(row["id"]).startswith("f_") and row.get("origin") in FLAG_AI_ORIGINS:
            call = flag_generator_call(self.calls, row["id"], row.get("type"))      # T-177 r3: a flag's generator answer is its record's flag call (the ladder does not record it)
        return call

    def item_prepared(self, row) -> bool:
        call = self.first_call(row)
        return bool(call) and AU.is_prepared(call.get("recorded_from"))

    def prepared(self, row) -> bool:
        return self.case_prepared or self.item_prepared(row)


def with_provenance(conn, case_id, views, prov=None):
    """D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name
    ('hand-checked (qa)') on its ladder's generator, so no screen or payload names a model for an answer no model gave. Others get prepared false and keep their model id.
    D-069: sets only the provenance fields; every sentence was already built from the prepared templates (view_of), none is rewritten here."""
    prov = prov if prov is not None else Prov(conn, case_id)
    for v in views:
        gen = (v.get("ladder") or {}).get("generator")
        call = prov.first_call(v)      # a view carries the same id / ladder / type / origin the call lookup reads
        prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
        v["prepared"] = prepared
        if gen is not None:
            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
            if prepared:
                gen["model"] = call["model"]


FLAG_AI_ORIGINS = ("llm", "lexicon+llm", "lexicon")      # the record's flag call ran for these (the phrase-list-only ones too: the call found nothing for them)


def flag_generator_call(calls, item_id, ftype=None):
    """The generator call behind a flag that does not record one: the flags (or, for a conflict, conflicts) call made for its record (item f_r3_1 -> call item f_r3). Without a call of
    its own, the case's last such call when every one of them is the same kind; else None. A call that found no recorded answer is not an answer."""
    step = "conflicts" if ftype == "conflict" else "flags"
    gens = [c for c in calls if c["role"] == "generator" and c["step"] == step and not str(c.get("error") or "").startswith("FIXTURE_MISS")]
    base = re.sub(r"_\d+$", "", str(item_id))
    own = [c for c in gens if c.get("item_id") in (item_id, base)]
    if own:
        return own[-1]
    kinds = {AU.is_prepared(c.get("recorded_from")) for c in gens}
    return gens[-1] if gens and len(kinds) == 1 else None


PREPARED_MODEL = AU.PREPARED_MODEL      # what a prepared (curated) answer names as its maker; the same text the audit rows carry


def models_for(conn, case_id, base, calls=None):
    """D-065 (T-177 r2): the {generator, judge} model names a payload shows for THIS case. When every generator answer of the case is a hand-checked fixture, no model drafted it: the generator reads
    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with any recorded or live answer keeps the configured model; one with no usable answer follows the set in use."""
    calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
    gens = [c for c in calls if c["role"] == "generator" and not str(c.get("error") or "").startswith("FIXTURE_MISS")]      # a call that found no answer is no model's work and no fixture's
    prepared = all(AU.is_prepared(c.get("recorded_from")) for c in gens) if gens else AU.answers_prepared()      # D-069: no usable answer (malformed, empty or missing counts as none) is decided by the set in use, never by a model label
    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)


def narrative_view(conn, case_id, nar):
    """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
    if not nar or not isinstance(nar.get("generator"), dict):
        return nar
    call = next((c for c in DB.list_llm_calls(conn, case_id) if c["id"] == nar["generator"].get("call_id")), None)
    prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
    return {**nar, "prepared": prepared, "generator": {**nar["generator"], "prepared": prepared, **({"model": call["model"]} if prepared else {})}}


def second_check_pending_ids(conn, case_id) -> set:
    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
    acknowledges it, no check needed). Lazy import: trace imports this module."""
    from app.backend import trace
    return {u["item_id"] for u in trace.unjudged_items(conn, case_id) if not trace.acknowledge_only(u["kind"], u["row"])}


272:class Prov:
273-    """D-069: the provenance of the answers behind one case's items, read once. `prepared(row)` is the field every user-facing sentence about the item is keyed by: the item's first
274-    answer is a hand-checked fixture, or the case's answers are the prepared ones (so even a code-made item talks about 'the second check', never 'the second AI check')."""
275-
276-    def __init__(self, conn, case_id, calls=None):
277-        self.calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
278-        self.by_id = {c["id"]: c for c in self.calls}
279-        self.by_item = {}
280-        for c in self.calls:
281-            if c["role"] == "generator" and c.get("item_id"):
282-                self.by_item.setdefault(c["item_id"], []).append(c)
283-        self.case_prepared = models_for(conn, case_id, {"generator": "", "judge": ""}, self.calls)["generator_prepared"]
284-
285-    def first_call(self, row):
286-        """The generator call behind the item: its ladder's call, else the item's last generator call, else (a flag) its record's flag call."""
287-        gen = (row.get("ladder") or {}).get("generator")
288-        call = self.by_id.get((gen or {}).get("call_id")) or next(iter(reversed(self.by_item.get(row["id"], []))), None)
289-        if call is None and str(row["id"]).startswith("f_") and row.get("origin") in FLAG_AI_ORIGINS:
290-            call = flag_generator_call(self.calls, row["id"], row.get("type"))      # T-177 r3: a flag's generator answer is its record's flag call (the ladder does not record it)
291-        return call
292-
293-    def item_prepared(self, row) -> bool:
294-        call = self.first_call(row)
295-        return bool(call) and AU.is_prepared(call.get("recorded_from"))
296-
297-    def prepared(self, row) -> bool:
298-        return self.case_prepared or self.item_prepared(row)
299-
300-
301-def with_provenance(conn, case_id, views, prov=None):
302-    """D-065: mark every item whose generator answer is a hand-checked fixture (the call's recorded_from.backend is 'curated') `prepared: true` and put the fixture's own model name
303-    ('hand-checked (qa)') on its ladder's generator, so no screen or payload names a model for an answer no model gave. Others get prepared false and keep their model id.
304-    D-069: sets only the provenance fields; every sentence was already built from the prepared templates (view_of), none is rewritten here."""
305-    prov = prov if prov is not None else Prov(conn, case_id)
306-    for v in views:
307-        gen = (v.get("ladder") or {}).get("generator")
308-        call = prov.first_call(v)      # a view carries the same id / ladder / type / origin the call lookup reads
309-        prepared = bool(call) and AU.is_prepared(call.get("recorded_from"))
310-        v["prepared"] = prepared
311-        if gen is not None:
312-            gen = v["ladder"]["generator"] = dict(gen, prepared=prepared)      # a copy: the stored row is never touched
313-            if prepared:
314-                gen["model"] = call["model"]
315-
316-
317-FLAG_AI_ORIGINS = ("llm", "lexicon+llm", "lexicon")      # the record's flag call ran for these (the phrase-list-only ones too: the call found nothing for them)
318-
319-
320-def flag_generator_call(calls, item_id, ftype=None):
321-    """The generator call behind a flag that does not record one: the flags (or, for a conflict, conflicts) call made for its record (item f_r3_1 -> call item f_r3). Without a call of
322-    its own, the case's last such call when every one of them is the same kind; else None. A call that found no recorded answer is not an answer."""
323-    step = "conflicts" if ftype == "conflict" else "flags"
324-    gens = [c for c in calls if c["role"] == "generator" and c["step"] == step and not str(c.get("error") or "").startswith("FIXTURE_MISS")]
325-    base = re.sub(r"_\d+$", "", str(item_id))
326-    own = [c for c in gens if c.get("item_id") in (item_id, base)]
327-    if own:
328-        return own[-1]
329-    kinds = {AU.is_prepared(c.get("recorded_from")) for c in gens}
330-    return gens[-1] if gens and len(kinds) == 1 else None
331-
332-
test_prepared_property.py
test_prepared_provenance.py
test_prepared_provenance_r3.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:06.246Z

**tool call — Bash**
````
{
 "command": "grep -rn \"f_r7_1\\|phrase list\\|Found by code\\|origin\" app/backend/*.py | grep -v service_date | head -40"
}
````

### User / tool · 2026-11-03T13:24:06.334Z

**tool result**
````
app/backend/api.py:196:                log.warning("existence probe for a failed request itself failed (%s); answering the original error", type(probe_err).__name__)
app/backend/billing.py:40:    "ROW_NOT_PARSED": "This row carries a figure or a date but did not fit the form's layout, so it was not read into any column. It is listed here, not totaled; check the original.",
app/backend/amounts.py:57:# original and reclassifies it, and only the reclassify guard (code cue + judge re-check) reads them. A rate cue above still beats a charge cue.
app/backend/conflicts.py:176:    return [{"subtype": "accident_date", "category": category, "type": "conflict", "origin": "code", "title": title, "explanation": expl,
app/backend/conflicts.py:237:        out.append({"subtype": "provider_name", "category": "provider_name_variant", "type": "conflict", "origin": "code", "title": title,
app/backend/count_charge.py:75:               reclassification={"from": row["kind"], "to": "charge", "at": store.iso(t), "by": "reviewer", "original_kind": prior.get("original_kind", row["kind"]),
app/backend/conflict_candidates.py:10:  the phrase list fires on as a prior condition or surgery, or that names an earlier accident or claim.
app/backend/conflict_candidates.py:57:# a prior event the phrase list does not cover (an earlier accident or claim). A sentence that is itself a denial never counts.
app/backend/conflict_candidates.py:207:                for ou in _units(o):                                  # an earlier accident or claim, which the phrase list does not cover
app/backend/dismissal_patterns.py:28:    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")
app/backend/export.py:8:    entries: [{id, record_no, summary, excerpt, review_status, [translation_label], [date_iso], [original_summary], [original_excerpt]}]
app/backend/export.py:47:TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
app/backend/export.py:48:                    "Prepared translation": "[Prepared translation of the Spanish original; check before sending]",
app/backend/export.py:49:                    "Translation (edited by reviewer)": "[Translation of the Spanish original, edited by reviewer; check before sending]"}
app/backend/export.py:524:            body = f"Not classified as a charge ({a.get('raw') or m}); check the original quote."
app/backend/export.py:657:    so edited-ness is the status OR a stored original that differs from the exported text. Out-of-letter entries are not listed."""
app/backend/export.py:662:    return ((e.get("original_summary") is not None and e["original_summary"] != e["summary"])
app/backend/export.py:663:            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))
app/backend/export.py:690:        if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
app/backend/export.py:691:            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
app/backend/export.py:692:                bits.append(f'summary was {"prepared" if v.prepared else "AI"} wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
app/backend/export.py:694:                bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
app/backend/export.py:695:        if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
app/backend/export.py:696:            bits.append(f'excerpt was "{e["original_excerpt"]}", now "{e["excerpt"]}"')
app/backend/flags.py:45:    f["why"] = why.join(f["reasons"], (f.get("ladder") or {}).get("judge")) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
app/backend/flags.py:49:def _flag(record: dict, ftype: str, category: str, excerpt: str, origin: str, span, tagged: bool, agreement) -> dict:
app/backend/flags.py:51:    f = {"type": ftype, "category": category, "excerpt": excerpt, "origin": origin, "record_no": record["n"],
app/backend/flags.py:59:                    "judge": "unavailable" if origin != "lexicon" else None}}
app/backend/flags.py:81:    """Flags from the phrase list alone: excerpt = the whole sentence unit that contains the hit; one flag per (unit, type)."""
app/backend/flags.py:121:    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
app/backend/flags.py:148:            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
app/backend/flags.py:163:            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
app/backend/flags.py:218:        elif f["origin"] == "llm" and FT.TYPE_OF.get(f["category"]) != f["type"]:
app/backend/flags.py:233:            "origin": "code", "title": title, "explanation": expl, "review_status": "pending", "state": "needs_review",
app/backend/flags.py:286:    f = {"id": fid, "type": "conflict", "category": c["category"], "excerpt": qa, "excerpt_b": qb, "origin": "code", "title": title, "explanation": expl,
app/backend/flags.py:334:        elif f["origin"] in ("llm", "both"):
app/backend/flags.py:350:    if f["state"] != "rejected" and ((step == "j3" and v == "benign" and f.get("origin") == "code") or
app/backend/flags.py:351:                                      (step == "j4" and v == "disagree" and f.get("origin") == "llm")):
app/backend/flags.py:383:        if f["type"] == "conflict" and f.get("origin") == "llm":
app/backend/generator.py:63:    if language.is_translated(lang):                      # the quote stays in the original language; the summary is a labelled AI translation (D-042)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:10.965Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/unit/test_prepared_provenance_r3.py; grep -n \"PREPARED_LABEL\\|origin_label\\|ORIGIN_LABEL\" app/backend/*.py | head -30; sed -n 140,170p app/backend/flags.py"
}
````

### User / tool · 2026-11-03T13:24:11.075Z

**tool result**
````
"""T-177 round 3 (D-065, final): every backend-generated text for a PREPARED item says it is a prepared answer. Never 'AI drafted', 'AI found it', 'the AI's summary' or a model name.
Covers flag items (trace step + why + origin), failed prepared items (SUMMARY_NOT_IN_QUOTE, SCHEMA_INVALID), a missing curated answer (no model step), and /classic routing (D-068).
The recorded set keeps its AI wording."""
import json
import re
import shutil
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

PREPARED_MODEL = "hand-checked (qa)"
ALLOWED = "\x00"       # D-069: nothing is allowed any more (the "standing in for the AI draft" tail was dropped); tests/unit/test_prepared_property.py is the full guard
AI_WORDS = re.compile(r"AI draft|AI found|AI proposed|AI-made|AI read|AI wrote|the AI's|the AI did not|claude-sonnet", re.I)
E1_KEY = "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7"      # e1's curated generator answer


def _client(tmp_path, monkeypatch, fixture_set=None, fixture_dir=None, mode="local", static=None):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    if mode:
        monkeypatch.setenv("ZLAYT_MODE", mode)
    else:
        monkeypatch.delenv("ZLAYT_MODE", raising=False)
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        monkeypatch.delenv(k, raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    if fixture_dir:
        monkeypatch.setenv("LLM_FIXTURE_DIR", str(fixture_dir))
    return TestClient(create_app(str(tmp_path / "p.sqlite"), static_dir=str(static or tmp_path)), client=("127.0.0.1", 50000))


def _run(c, partial=False):
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (partial and (s.get("error") or {}).get("code") == "run_partial"), json.dumps(s)[:1500]      # a record with no usable answer is a partial run, kept
    return tok


@pytest.fixture
def curated(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch, "curated")
    return c, _run(c)


@pytest.fixture
def recorded(tmp_path, monkeypatch):
    c = _client(tmp_path, monkeypatch)
    return c, _run(c)


def _ids(c, tok):
    case = c.get(f"/api/cases/{tok}").json()
    return [x["id"] for k in ("entries", "flags", "amounts") for x in case.get(k, [])] + [x["id"] for x in case.get("tray", []) if isinstance(x, dict) and x.get("id")]


def _hits(text):
    return AI_WORDS.findall(text.replace(ALLOWED, ""))


def _mutated_set(tmp_path, mode):
    """Copy the curated set (+ recorded fallback, as fixture.call does) into tmp/curated; break e1's generator answer."""
    import os
    root = tmp_path / "mut"
    d = root / "curated"
    d.mkdir(parents=True)
    src = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
    for f in os.listdir(src):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, f), d)
    for f in os.listdir(os.path.join(src, "curated")):
        if f.endswith(".json"):
            shutil.copy(os.path.join(src, "curated", f), d)
app/backend/trace.py:216:PREPARED_LABEL = "Prepared answer"      # D-069: the D-065 wording minus its "standing in for the AI draft" tail (only the badge tooltip may say AI)
app/backend/trace.py:218:CASE_PREPARED_LABEL = "Prepared summaries and quotes for each record"
app/backend/trace.py:474:        xlabel = PREPARED_LABEL if prep else "AI drafted a summary and picked a quote"      # `prep` here is the item's own first answer; `voice` is the item's or the case's
app/backend/trace.py:492:                st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
app/backend/trace.py:775:            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
app/backend/trace.py:851:        st.append(step("extracted", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
app/backend/trace.py:1174:    xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"
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
            _note_merged(lx, uniq[match])
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:16.530Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe.py <<'EOF'\nimport sys, json, tempfile, os\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project/tests/unit\")\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ[\"ZLAYT_MODE\"]=\"local\"; os.environ[\"FIXTURE_SET\"]=\"curated\"\nimport test_prepared_provenance_r3 as t\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd=tempfile.mkdtemp()\nc=TestClient(create_app(d+\"/p.sqlite\", static_dir=d), client=(\"127.0.0.1\",50000))\ntok=t._run(c)\ncase=c.get(f\"/api/cases/{tok}\").json()\nfor f in case[\"flags\"]:\n    print(f[\"id\"], f.get(\"origin\"), f.get(\"prepared\"), f.get(\"type\"), f.get(\"origin_label\"))\nf=[x for x in case[\"flags\"] if x[\"id\"]==\"f_r7_1\"][0]\nprint(json.dumps({k:v for k,v in f.items() if k not in(\"evidence\",)}, indent=1)[:3000])\nprint(json.dumps(c.get(f\"/api/cases/{tok}/items/f_r7_1/trace\").json(), indent=1)[:3500] if False else \"\")\nEOF\npython3 /private/tmp/claude-501/*/*/scratchpad/probe.py 2>&1 | tail -80"
}
````

### User / tool · 2026-11-03T13:24:16.893Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe.py", line 5, in <module>
    import test_prepared_provenance_r3 as t
  File "/Users/arsis/zlayt-pm-project/tests/unit/test_prepared_provenance_r3.py", line 9, in <module>
    import pytest
ModuleNotFoundError: No module named 'pytest'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:19.283Z

**tool call — Bash**
````
{
 "command": "ls -a | head -30; which -a python python3 pytest; ls .venv 2>/dev/null"
}
````

### User / tool · 2026-11-03T13:24:19.369Z

**tool result**
````
.
..
.claude
.dockerignore
.env
.env.example
.git
.gitignore
.pytest_cache
.scratch
.venv
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
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
run.sh
/opt/homebrew/bin/python3
/usr/bin/python3
bin
include
lib
pyvenv.cfg
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:20.638Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python /private/tmp/claude-501/*/*/scratchpad/probe.py 2>&1 | tail -80"
}
````

### User / tool · 2026-11-03T13:24:21.616Z

**tool result**
````
f_gap_r6_r7 code False gap None
f_accident_date_after_treatment_1_2_7 code False conflict None
f_cx1 code False conflict None
f_r3_1 lexicon+llm True pre_existing None
f_r8_1 lexicon+llm True pre_existing None
f_r6_1 lexicon+llm True causation None
f_r7_1 lexicon True causation None
f_r7_2 lexicon+llm True causation None
f_r8_2 lexicon+llm True causation None
f_r9_1 lexicon+llm True causation None
{
 "id": "f_r7_1",
 "state": "needs_review",
 "reasons": [
  "LEXICON_ONLY"
 ],
 "why": "The phrase list found this flag but the prepared answers did not; check that it applies.",
 "review_status": "pending",
 "version": 1793712261.315045,
 "edited": null,
 "ladder": {
  "backend": "fixture",
  "code_checks": {
   "classified_by": "lexicon+llm",
   "excerpt_verbatim": true,
   "highlight_found": true
  },
  "generator": null,
  "item_id": "f_r7_1",
  "judge": null,
  "state": "needs_review",
  "human": {
   "action": null,
   "edited_text": null,
   "at": null
  }
 },
 "rerun_note": null,
 "rerun_available": false,
 "type": "causation",
 "category": "accident_date_provenance",
 "source_kind": "record",
 "title": "Accident date source",
 "explanation": "Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): \u201cDate of accident per intake form: 2026-01-19.\u201d",
 "computed": {
  "excerpt": "Date of accident per intake form: 2026-01-19.",
  "lexicon_ids": [
   "intake_form_accident_date"
  ],
  "record_ids": [
   "r7"
  ],
  "record_nos": [
   7
  ]
 },
 "origin": "lexicon",
 "reviewer_note": null,
 "prepared": true,
 "second_check_pending": false
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:25.884Z

**tool call — Bash**
````
{
 "command": "grep -rn \"origin\" memory/contracts/api.md | head -20; grep -rn \"Prepared answer\\|\\.prepared\" app/frontend --include=*.js --include=*.html -l | head; sed -n 740,800p app/backend/trace.py"
}
````

### User / tool · 2026-11-03T13:24:25.979Z

**tool result**
````
memory/contracts/api.md:143:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
memory/contracts/api.md:213:      "origin": "code", "reviewer_note": null,
memory/contracts/api.md:227:      "origin": "code", "reviewer_note": null,
memory/contracts/api.md:238:      "origin": "lexicon+llm", "reviewer_note": null,
memory/contracts/api.md:351:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
memory/contracts/api.md:364:            "edited": {"summary": "...", "original_summary": "...", "at": "2026-11-02T01:06:00Z", "kept_my_wording": false} },
memory/contracts/api.md:399:- `to: "charge"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated ("not billed", "unbilled"), the figure has a parsed value and its record is not injection-tagged, **and (2) judge 2** re-checks the figure against class `charge` and answers `agree`. Code runs first; the judge is not called when the code check fails. Undoing her own earlier demotion of a figure the code first called a charge skips both checks (the original class returns with the judge answer it had; works with no judge available).
memory/contracts/api.md:404:- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassification` = `{from, to, at, by: "reviewer", original_kind, wording, restored, note, previous_judge}` and `ladder.code_checks.classified_by` = `"reviewer:reclassified"`.
memory/contracts/api.md:647:- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `summary_trimmed` (code, D-054, present only when code removed summary clauses the quote does not support: `why` lists each as "removed from the summary: not in the quote: '<clause>'"; `evidence.removed`, `evidence.original_summary`, `evidence.kept_summary`; the second AI check saw `kept_summary`), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. **T-139 r3 (code changed the AI's text because it states an amount; internal, never in the letter):** `excerpt_narrowed` (code, rule `T-139`, status `pass`, present only when code dropped the quote's end sentence(s) that state an amount; right after `extracted`/`summary_trimmed`; `why` says what was removed, that amounts go only in Billed charges and the internal notes, and that the second check saw the shortened quote; `evidence = {removed[] (the dropped sentences, verbatim), quote_before, quote_after, summary_before, summary_after}`) and `charge_clause_removed` (code, rule `T-139`, status `pass`, present when code removed the trailing summary clause(s) that state an amount, either at generation time after narrowing or in the quote-picker `edit` that removed the amount from the quote; `evidence = {removed[] (verbatim clauses), summary_before, summary_after, quote_before, quote_after}`). The same generation-time record is in `GET /items/{id}` `item.ladder.excerpt_narrowed = {rule, original_excerpt, dropped[], summary_removed[], original_summary, summary_before_charge_trim}`; the edit-time record is internal (`edited.code_trim`), shown only through the step, and cleared by the next edit or by `reset`. The steps are never in `letter_text`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
memory/contracts/api.md:672:    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
memory/contracts/api.md:785:- **Quote.** For a Spanish record the entry `excerpt` is always the original Spanish, checked word for word against the record text (accents included). A model quote that is a translation is `rejected` (`GROUNDING_EXCERPT_NOT_VERBATIM`). Offsets point into the original text.
memory/contracts/api.md:787:- **Entry field `translation`** (every entry view; `null` for English records): `{source_language: "es", source_language_name: "Spanish", label: "AI translation", summary_is_translation: true, quote_is_original: true}`. After the paralegal edits the summary, or writes a manual entry, `label` is `"Translation (edited by reviewer)"`. The UI must show `label` next to the summary and show the quote as the original Spanish. Edits and manual entries on a Spanish record are checked against the Spanish quote and judged with the Spanish prompt.
memory/contracts/api.md:788:- **Never auto-verified (D-050).** Every item (entry, amount, flag) made from a record routed `es` or `uncertain` is `needs_review` with reason `AI_TRANSLATION` ("AI translation — check against the original"), whatever the Spanish code checks and the translation judge said. Their failures still show in the trace; passing them never yields `verified`. Enforced once, in `confidence.compose_state` (ctx `translated`), and every path that rewrites a state passes it: pipeline, rerun, rejudge, edit and manual entry, date confirmation, reclassify, flags. The entry `translation` block also carries `review_label: "AI translation — check against the original"`. Batch accept refuses such an item (`not_verified`); the paralegal's single accept is the gate and still works, and export needs nothing more than that accept.
memory/contracts/api.md:791:- **Export.** In the letter, a translated entry ends with a bracketed, removable note on its own line under the quote (T-121): `[AI translation of the Spanish original; check before sending]` (or `[Translation of the Spanish original, edited by reviewer; check before sending]`), (in the one-line style, at the end of the entry's line); no line starts with `AI translation:`. The quote is the original Spanish. The AI-drafted treatment paragraph (`/narrative`) is English-only and skips translated entries.
memory/contracts/api.md:798:Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the join ` and `; ` with ` is not a boundary, so `Neck pain consistent with sprain.` is one clause) and removes a clause only when it adds salient content its own quote lacks (T-112 r2): a procedure/treatment/device/drug term, a body part, or a diagnosis noun that the quote (and, for body part, side and imaging modality, the record's source label) does not have, matched by word family (Tylenol~acetaminophen, cervical~neck, fingers~digits). A number, month, side or negation the quote lacks counts only for a clause that shares no content word with the quote. A changed number or side on the quote's own topic stays and is flagged `needs_review` by the D-034/D-047 code checks (which look for the word anywhere in the quote); a negation on the quote's own topic also stays but is only guaranteed to reach judge 1 and the paralegal: if the quote has the same negation word elsewhere (`No cervical strain.` over `X-ray: no acute fracture. Cervical strain.`), the token check does not flag it. Clinical abbreviations are spelled out on both sides before matching (lac, DJD, OA, RA, ESI, TPI, BLE/LLE/RLE/LE, BUE/LUE/RUE/UE, US, IM, C-collar, APAP, CP, ORIF, TKA and similar), so a faithful expansion is not trimmed. A clause with no such content stays even if none of its words appear in the quote ("Dizziness reported." over "Pt dizzy since crash."): judge 1 still checks it. Whole clauses only. Code does not promise that the kept text reads as a finished sentence (a clause is never edited; the judge and the human check the wording); what it does guarantee, with no word list (T-128 r3): code trims only a SUFFIX, so the kept text is always a prefix of whole clauses and a clause is removed only when every clause after it is removed too (nothing kept can depend on something removed; `Shoulder pain; surgery performed; due to torn labrum.` keeps both or drops the tail), the FIRST clause is never removed (an unsupported first clause means nothing is trimmed and the whole summary goes to judge 1; a summary with every clause unsupported still goes to the tray), and the kept prefix has at least 2 content words; when a rule says no, nothing is trimmed; a with-phrase is removed with its head or kept with it (`Neck pain; diagnosed with diabetes.` removes the whole clause `diagnosed with diabetes`; a summary that is one unsupported clause, such as `Neck pain consistent with sprain.` over `Neck pain.`, goes to the could-not-verify tray). Nothing else changes: the model's original output stays in `ladder.generator.output`, and `ladder.summary_trim = {rule, original_summary, removed[], notes[], kept_summary}` records what code removed (`notes[i]` = "removed from the summary: not in the quote: '<clause>'"). The entry's `summary` is the kept text; judge 1 and every later check see it. If every clause is removed (or what is left has no content word), no entry is made: the record gets a could-not-verify tray placeholder with reason `SUMMARY_NOT_IN_QUOTE` (state `rejected`, `ladder.failure`, not an error in `errors[]`). Human-written summaries (edit, manual entry) are never trimmed (D-047 refuses an unsupported one), and neither are summaries of Spanish or uncertain-language records (D-050 makes those needs_review anyway). Frontend: show the `summary_trimmed` trace step when present; a tray item with reason `SUMMARY_NOT_IN_QUOTE` uses the same wording as other placeholders (the `why` sentence names the cause).
memory/contracts/api.md:803:- **Narrowing first (T-139 follow-up, code only).** Before the hold-out, when the quote has several sentences and its currency-bearing sentence(s) sit at the START or END, code drops them (`charge_text.narrow_excerpt`): the narrowed quote is a contiguous run of whole, verbatim sentences (a substring of the model's quote; an amount in the MIDDLE, a single-sentence quote, a quote that is all amounts, or fewer than 2 content words left means no narrowing). The summary is then trimmed against the narrowed quote (D-054, then the trailing-amount-clause rule above). Every rung-1 check re-runs on the narrowed pair (`generator.verify`); it is kept only if the pair states no amount, some summary is left, and no check raises a reason the original pair did not already raise; otherwise the entry keeps its quote and is held as above. Judge 1 runs on the narrowed pair (D-044/D-058), so no answer given for the longer quote is reused; with no answer the entry is `needs_review` with `JUDGE_UNAVAILABLE` (JUDGE_NOT_RUN). The entry's `quote`/`excerpt` and offsets are the narrowed text. `ladder.excerpt_narrowed = {rule: "T-139", original_excerpt, dropped[], summary_removed[], original_summary}` records what code dropped; `ladder.generator.output` keeps the model's own output. Frontend: when `ladder.excerpt_narrowed` is present, say "charge sentence not quoted" next to the quote; the paralegal can still re-pick a longer quote, but a quote with an amount is refused as above. Over the 25 recorded cases, 51 entries stated an amount; 42 are narrowed (39 verified by judge 1, 3 need review for other reasons) and 9 remain held (single-sentence billing statements).
memory/contracts/api.md:806:- **Edit.** `edits.excerpt` (the quote picker) with a quote that has no amount: if the summary still states one and the AI wrote that summary (she has not edited it), code removes the trailing clause(s) that state an amount under the D-054 suffix rule (only a run of clauses at the end, never the first clause, the kept prefix keeps at least 2 content words; otherwise nothing is trimmed) and the edit saves with the trimmed summary (`edited.summary`, the original is kept; the internal notes' EDITED ITEMS line shows both). The response `warnings[]` gains `{code: "CHARGE_CLAUSE_REMOVED", item_id, removed: [clause...], message}`. If code cannot trim, the edit is `422 invalid_edit` (`detail.reason "CHARGE_TEXT_IN_ENTRY"`); the paralegal edits the summary. A quote is never rewritten by code.
memory/contracts/api.md:844:| `AI_TRANSLATION` | needs_review | the item comes from a record routed Spanish or LANGUAGE_UNCERTAIN (D-050); "AI translation — check against the original"; never verified by any check, only the paralegal's accept |
memory/contracts/api.md:861:- **T-177 r4 (D-069: templates by provenance, malformed means missing):** every user-facing string of a prepared item or case comes from a prepared-specific template chosen by the item's `prepared` field (or the case's `models.generator_prepared`); no AI sentence is rewritten afterwards. Consequences for payloads: (1) the word "AI" and any model name appear only in the badge tooltip sentence and in structured identity fields of the real second check (`models.judge`, judge call rows, `ladder.judge.model`); every sentence about the second check says "second check" on a prepared item or case (`why`, trace labels such as "Second check: is the summary supported by the quote?", blockers, warnings, 422 messages, the export notes line). (2) The trace step for a prepared answer is labelled "Prepared answer" with `why` "Prepared answer (hand-checked by the team for the demo)"; the D-065 "standing in for the AI draft" tail is gone (only the badge tooltip may say AI). The case-trace `extract` step is labelled "Prepared summaries and quotes for each record". (3) A malformed or empty prepared answer is treated as a missing one: the generator call is not retried, its `llm_calls` row reads `FIXTURE_MISS` with model `hand-checked (qa)`, the item is `rejected` with reason `FIXTURE_MISS` ("The demo has no prepared answer for this step, so this item has not been checked."), and the case's `models.generator` stays `hand-checked (qa)` / `generator_prepared: true` (also when no answer is usable at all, by the fixture set in use). (4) `ladder.translation.label` / `review_label` read "Prepared translation" / "Prepared translation — check against the original" on a prepared item; the export letter's bracketed note reads "[Prepared translation of the Spanish original; check before sending]". (5) `JUDGE_NOT_RUN` blockers carry `prepared: boolean` (the case's provenance) so the 422 headline can say "second check". (6) The export notes disclosure line for a prepared case reads "This chronology was built from answers the team prepared for this demo and checked by a second check; ...". (7) `GET /items/{id}` for a flag whose category is `llm_split` reads "Record boundaries chosen by a prepared answer" when prepared. Guard: tests/unit/test_prepared_property.py (fault-injected curated sets: valid, malformed, empty, missing; the sample and two library cases).
app/frontend/review.js
app/frontend/timeline.js
app/frontend/stepper.js
app/frontend/audit.js
app/frontend/judges.js
app/frontend/guided/step2.js
app/frontend/guided/review.js
        return st
    if origin == "code":
        comp = present._computed(row.get("computed"))
        vals = {k: comp[k] for k in ("from", "to", "days", "threshold", "stated_dates", "body_date", "first_treatment_date", "names", "subtype") if k in comp}
        st.append(step("computed", "Dates compared by code" if ftype == "gap" else "Stated and recorded dates compared by code", "code", PASS,
                       row["explanation"] or "Computed by code from the record dates.", rule="row 9" if ftype == "gap" else "row 10", evidence={"values": vals, "spans": spans}))
        bad = row["state"] == "rejected" or cc.get("spans_match_input") is False
        st.append(step("spans_match", "Cited text matches the record", "code", FAIL if bad else PASS,
                       reason_text("GROUNDING_EXCERPT_NOT_VERBATIM") if bad else "Every cited date line is in the record, character for character.",
                       reason="GROUNDING_EXCERPT_NOT_VERBATIM" if bad else None, rule="row 10", evidence={"spans": spans},
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"]) if bad else None))
        if "ENDPOINT_NOT_VERIFIED" in R:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", FAIL, reason_text("ENDPOINT_NOT_VERIFIED"), reason="ENDPOINT_NOT_VERIFIED", rule="row 9",
                           next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
        else:
            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", PASS, "Both dates are parsed or confirmed.", rule="row 9"))
        st.append(inj())
        st += _ocr_steps(R, rid0)
        st.append(step("judge_not_needed", second_check(""), "llm", SKIPPED, "Not needed: this is arithmetic over dates in the record, which code does exactly.", rule="row 9"))
        st.append(_human_step(cx, row, "flag"))
        return st
    has_llm, has_lex = origin in ("llm", "lexicon+llm"), origin in ("lexicon", "lexicon+llm")
    if ftype == "conflict":
        pass                                  # a conflict is the AI's pair proposal (row 11): no phrase list, so no agreement step
    elif has_lex:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", PASS, "The researched phrase list found this wording in the record.", rule="row 12", evidence={"spans": spans}))
    else:
        st.append(step("proposed_by_phrase_list", "Phrase list found it", "code", SKIPPED, reason_text("LLM_ONLY"), reason="LLM_ONLY", rule="row 12"))
    prep = prepared_item(cx, row, "flag")      # D-065 (T-177 r3): the flag's first answer is its record's flag call, which a curated set makes a prepared answer
    if has_llm:
        gen = lad.get("generator") or {}
        step_name = "conflicts" if ftype == "conflict" else "flags"
        call = _first_call(cx, row, "flag")
        ev = _llm_evidence(cx, "generator", gen.get("model") or cx.models["generator"], gen.get("prompt_version") or AU.PROMPT_OF_STEP.get(step_name), call)
        if ev["model"]["prepared"]:
            st.append(step("proposed_by_ai", PREPARED_LABEL, "llm", PASS, PREPARED_WHY, rule="D-065", evidence=ev))
        elif prep:      # no usable prepared answer for this record's flags: no model is named
            st.append(step("proposed_by_ai", PREPARED_FLAGS_LABEL, "llm", SKIPPED, PREPARED_FLAGS_MISSING, reason="FIXTURE_MISS", rule="D-065"))
        else:
            st.append(step("proposed_by_ai", "AI found it", "llm", PASS, "The AI proposed this flag as a category and a quote; it wrote no explanation.", rule="row 12", evidence=ev))
    elif prep:
        st.append(step("proposed_by_ai", PREPARED_FLAGS_LABEL, "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="D-065"))
    else:
        st.append(step("proposed_by_ai", "AI found it", "llm", SKIPPED, reason_text("LEXICON_ONLY"), reason="LEXICON_ONLY", rule="row 12"))
    if ftype == "conflict":
        pass
    elif has_llm and has_lex:
        st.append(step("agreement", _AGREE[1 if prep else 0], "code", PASS, pick("Both the phrase list and the AI found this flag.", "Both the phrase list and the prepared answers include this flag."), rule="row 12"))
    else:
        code = "LEXICON_ONLY" if origin == "lexicon" else "LLM_ONLY"
        if code in R:
            st.append(step("agreement", _AGREE[1 if prep else 0], "code", FAIL, reason_text(code), reason=code, rule="row 12", next_action=na("COMPARE_BY_HAND", {"item_id": row["id"]})))
        else:
            other = next((c for c in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS") if c in R), None)
            st.append(step("agreement", _AGREE[1 if prep else 0], "code", SKIPPED, reason_text(other) if other else "Only one source looked at this record, so there is nothing to compare.",
                           reason=other, rule="row 12"))
    if cat == "credibility_language":
        st.append(step("credibility_wording", "Credibility wording is not a clean negation", "code", PASS,
                       "The sentence uses a credibility term and is not a plain negation such as 'No Waddell signs', so it is flagged for you to see first.", rule="D-043"))
    vfail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or "SCHEMA_INVALID" in R or cc.get("excerpt_verbatim") is False
    if vfail:
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:34.700Z

**tool call — Bash**
````
{
 "command": "grep -rn \"get(\\\"prepared\\\")\\|\\[\\\"prepared\\\"\\]\\|item_prepared\\|\\.prepared(\" app/backend app/llm | grep -v \"^app/backend/export.py\" | head -30; grep -n \"prepared\" app/frontend/review.js | head -20; grep -n \"FLAG_AI_ORIGINS\" -r app | head; grep -n \"origin_label\\|\\\"origin\\\"\" app/backend/present.py | head"
}
````

### User / tool · 2026-11-03T13:24:34.826Z

**tool result**
````
app/backend/trace.py:252:    ev["prompt_version"] = None if ev["model"]["prepared"] else ((call or {}).get("prompt_version") or prompt_version)      # a prepared answer was prompted by nothing (T-177 r3)
app/backend/trace.py:471:        prep = ev["model"]["prepared"] or (not (call and call.get("recorded_from")) and cx.answers_prepared)      # D-065 (T-177 r3): a failed or missing prepared answer is still a prepared answer, never "AI drafted"
app/backend/trace.py:472:        if prep and not ev["model"]["prepared"]:
app/backend/trace.py:491:            if ev["model"]["prepared"]:
app/backend/trace.py:774:        if ev["model"]["prepared"]:
app/backend/trace.py:850:    if ev["model"]["prepared"]:
app/backend/present.py:250:    prep = prov.prepared(row)
app/backend/present.py:293:    def item_prepared(self, row) -> bool:
app/backend/present.py:298:        return self.case_prepared or self.item_prepared(row)
app/backend/present.py:310:        v["prepared"] = prepared
app/backend/review.py:334:        prep = present.Prov(conn, case_id).prepared(item)      # D-069: the sentence follows the item's provenance
app/backend/review.py:512:    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, prep=present.Prov(conn, case_id).prepared(item),      # D-069 r5: the warning follows the item's provenance
app/backend/export_routes.py:59:        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items), all(i.get("prepared") for i in e.items))      # D-069: the blockers carry the case's provenance
278:  // T-204 / D-065 / D-069: for a prepared answer (item.prepared, or the case's models.generator_prepared) the fallback is the prepared twin of the sentence (the same words as the server's TRACE_WHY_PREPARED),
279:  // never the AI-worded one, so the first paint and the swap both say "prepared wording". Keyed by the item, not by rewriting the AI text.
280:  const PREPARED_HELD = "You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers or you edit the summary in your own words.";
282:  const isPrepared = (item) => { const c = ZL.state.get().case; return !!(item && item.prepared) || !!(c && c.models && c.models.generator_prepared); };
app/backend/trace.py:233:    if kind == "flag" and row.get("origin") in present.FLAG_AI_ORIGINS:
app/backend/trace.py:242:    if kind not in ("entry", "flag") or (kind == "flag" and row.get("origin") not in present.FLAG_AI_ORIGINS):
app/backend/present.py:289:        if call is None and str(row["id"]).startswith("f_") and row.get("origin") in FLAG_AI_ORIGINS:
app/backend/present.py:317:FLAG_AI_ORIGINS = ("llm", "lexicon+llm", "lexicon")      # the record's flag call ran for these (the phrase-list-only ones too: the call found nothing for them)
193:            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
289:        if call is None and str(row["id"]).startswith("f_") and row.get("origin") in FLAG_AI_ORIGINS:
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:36.748Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Prepared answer\" app/frontend | head; sed -n 180,200p app/backend/present.py; sed -n 225,250p app/backend/trace.py; grep -rn \"T-214\\|f_r7_1\" tests | head"
}
````

### User / tool · 2026-11-03T13:24:36.861Z

**tool result**
````
app/frontend/stepper.js:41:    if (m && m.prepared) return "Prepared answer";         // D-065: a hand-checked demo answer is not an AI draft
app/frontend/stepper.js:585:      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet, or waiting for you. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “You” steps are your decisions, and " + (S.preparedFor(null) ? "“Prepared answer” steps are our team\u2019s wording for this demo, checked by a second AI model." : "“AI” steps are done by a model.")));
app/frontend/timeline.js:23:  // D-065: a hand-checked demo answer is a "Prepared answer", never an AI draft; recorded and live answers keep the AI label.
app/frontend/timeline.js:25:    ? el("span", { class: "tag", "data-testid": "tag-prepared", title: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." }, "Prepared answer")
app/frontend/timeline.js:276:            el("dt", {}, lad.generator.prepared ? "Prepared answer" : "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
app/frontend/audit.js:23:      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.prepared ? el("span", { class: "rv-chip", "data-testid": "audit-prepared" }, "Prepared answer") : null, c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
app/frontend/guided/step2.js:378:        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. " + (G.provenance().kind === "prepared" ? "" : "“AI draft” means an AI wrote it. ") + "“Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
app/frontend/guided/review.js:61:  /* ---------- provenance tags (D-065): a prepared answer says "Prepared answer", never "AI" ---------- */
app/frontend/guided/review.js:65:    if (item.prepared) return { cls: "prep", text: "Prepared answer", title: p.note };
    if row["type"] != "gap" or not ex:
        return base
    return " ".join(([] if base == OK_WHY else [base]) + ex)


def flag_view(row, recs, prep=False):
    c = _common(row, prep)
    c["why"] = _gap_why(row, c["why"])
    title, expl = FT.PREPARED_TEXT.get(row["category"]) if prep and row["category"] in FT.PREPARED_TEXT else (row["title"], row["explanation"])      # D-069
    if prep and (title, expl) == FT.UNRECOGNISED:
        title, expl = FT.UNRECOGNISED_PREPARED
    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": title,
            "explanation": expl, "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}


def gap_change_index(events, current: dict):
    """T-127: which gap figures a confirm_date moved, kept with the case. `events` are the case's review events (oldest first); each `confirm_date` event's `after.gap_changes`
    holds what confirm_date reported (with record_seq and sentence). `current` maps gap flag id -> {days, from, to}. Returns ({flag_id: change} for gaps whose CURRENT figures
    are the ones that change produced, [removed changes whose gap is still gone]). A later change to the same gap replaces the earlier one; once the figures differ from the
    ones the change produced, nothing is claimed. Code over stored figures, never a model."""
_WHY_CODES = set(why.all_codes())


def _first_call(cx, row, kind):
    """The generator call behind an item (entry: its extract call; flag: its record's flags/conflicts call), or None."""
    lad = row.get("ladder") or {}
    if kind == "entry":
        return cx.call((lad.get("generator") or {}).get("call_id"), row["id"], "extract")
    if kind == "flag" and row.get("origin") in present.FLAG_AI_ORIGINS:
        return cx.call((lad.get("generator") or {}).get("call_id")) or present.flag_generator_call(list(cx.call_by_id.values()), row["id"], row.get("type"))
    return None


def prepared_item(cx, row, kind) -> bool:
    """D-065: the item's first answer is a hand-checked fixture, or it has none and the set in use is the curated one. Then no sentence about it may say an AI drafted or found it."""
    if kind == "entry" and (row.get("ladder") or {}).get("entered_by"):
        return False
    if kind not in ("entry", "flag") or (kind == "flag" and row.get("origin") not in present.FLAG_AI_ORIGINS):
        return False
    call = _first_call(cx, row, kind)
    return AU.is_prepared(call.get("recorded_from")) if call and call.get("recorded_from") else cx.answers_prepared      # a call that gave no answer has no provenance: the set in use decides


def _llm_evidence(cx, role, model, prompt_version, call):
    ev = {"model": {"id": (call or {}).get("model") or model, "role": role,
                    "independent_of_generator": None if role == "generator" else ((call or {}).get("model") or model) != cx.models["generator"],
tests/e2e/guided/test_t211.py:170:    for iid in ("e1", "f_r7_1"):
tests/e2e/guided/test_t211.py:230:def test_f_r7_1_says_the_second_check_did_not_run_and_never_says_it_checked_a_prepared_answer(page, make):
tests/e2e/guided/test_t211.py:232:    tok = make(); open_item(page, tok, "f_r7_1"); wait_loaded(page); open_panel(page)
tests/e2e/guided/test_step2.py:265:    tok = make(LIB03); f = item(tok, "f_r7_1")
tests/e2e/guided/test_step2.py:267:    open_item(page, tok, "f_r7_1")
tests/e2e/guided/test_step2.py:269:    assert item(tok, "f_r7_1")["review_status"] == "accepted"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:46.598Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"app/backend/present.py\"\ns=open(p).read()\nold='''        prepared = bool(call) and AU.is_prepared(call.get(\"recorded_from\"))\n        v[\"prepared\"] = prepared\n        if gen is not None:'''\nnew='''        prepared = bool(call) and AU.is_prepared(call.get(\"recorded_from\"))\n        if str(v.get(\"id\", \"\")).startswith(\"f_\") and v.get(\"origin\") in CODE_ONLY_FLAG_ORIGINS:\n            prepared = False      # T-214: found only by code (the phrase list; the model's answer had nothing for it), so no curated answer is behind it\n            v[\"origin_label\"] = CODE_ONLY_FLAG_ORIGINS[v[\"origin\"]]\n        v[\"prepared\"] = prepared\n        if gen is not None:'''\nassert old in s\ns=s.replace(old,new)\ns=s.replace('''FLAG_AI_ORIGINS = (''','''CODE_ONLY_FLAG_ORIGINS = {\"lexicon\": \"Found by code (phrase list)\", \"code\": \"Found by code\"}      # T-214 (D-065): a flag whose only source is code is never a \"prepared answer\"\nFLAG_AI_ORIGINS = (''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"gen is not None\" -B3 app/backend/present.py | head; ls tests/unit | grep -i sample"
}
````

### User / tool · 2026-11-03T13:24:46.707Z

**tool result**
````
311-            prepared = False      # T-214: found only by code (the phrase list; the model's answer had nothing for it), so no curated answer is behind it
312-            v["origin_label"] = CODE_ONLY_FLAG_ORIGINS[v["origin"]]
313-        v["prepared"] = prepared
314:        if gen is not None:
test_flags_sample.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:24:53.705Z

**tool call — Bash**
````
{
 "command": "grep -n \"items/\" tests/unit/test_prepared_provenance_r3.py | head -3; cat > tests/unit/test_flag_origin_t214.py <<'EOF'\n\"\"\"T-214 (D-065): a flag whose only source is code (the phrase list, or a computed gap/conflict) is never a \"Prepared answer\". prepared is true only when a curated answer is behind the item.\"\"\"\nfrom tests.unit.test_prepared_provenance_r3 import _client, _run\n\n\ndef _flags(c, tok):\n    return c.get(f\"/api/cases/{tok}\").json()[\"flags\"]\n\n\ndef test_code_only_flags_are_not_prepared_on_the_curated_sample(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch, \"curated\")\n    tok = _run(c)\n    fl = _flags(c, tok)\n    by_id = {f[\"id\"]: f for f in fl}\n    assert by_id[\"f_r7_1\"][\"origin\"] == \"lexicon\"\n    assert by_id[\"f_r7_1\"][\"prepared\"] is False and by_id[\"f_r7_1\"][\"origin_label\"] == \"Found by code (phrase list)\"\n    for f in fl:\n        if f[\"origin\"] == \"lexicon\":\n            assert f[\"prepared\"] is False and f[\"origin_label\"] == \"Found by code (phrase list)\", f[\"id\"]\n        elif f[\"origin\"] == \"code\":\n            assert f[\"prepared\"] is False and f[\"origin_label\"] == \"Found by code\", f[\"id\"]\n        else:\n            assert f[\"prepared\"] is True and f.get(\"origin_label\") is None, f[\"id\"]      # a curated answer is behind it\n    item = c.get(f\"/api/cases/{tok}/items/f_r7_1\").json()[\"item\"]\n    assert item[\"prepared\"] is False and item[\"origin_label\"] == \"Found by code (phrase list)\"\n\n\ndef test_recorded_set_flags_are_never_prepared(tmp_path, monkeypatch):\n    c = _client(tmp_path, monkeypatch)\n    tok = _run(c)\n    fl = _flags(c, tok)\n    assert fl and all(f[\"prepared\"] is False for f in fl)\n    assert all(f.get(\"origin_label\") for f in fl if f[\"origin\"] in (\"lexicon\", \"code\"))\nEOF\n.venv/bin/python -m pytest tests/unit/test_flag_origin_t214.py -q -x 2>&1 | tail -15"
}
````

### User / tool · 2026-11-03T13:24:55.397Z

**tool result**
````
101:        item = c.get(f"/api/cases/{tok}/items/{f['id']}").json()["item"]
103:        st = next(s for s in c.get(f"/api/cases/{tok}/items/{f['id']}/trace").json()["steps"] if s["id"] == "proposed_by_ai")
117:            r = c.get(f"/api/cases/{tok}/items/{iid}{suffix}")
..                                                                       [100%]
2 passed in 1.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:25:01.399Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/arc && mkdir $S/arc && git archive HEAD | tar -x -C $S/arc && cp app/backend/present.py $S/arc/app/backend/ && cp tests/unit/test_flag_origin_t214.py $S/arc/tests/unit/ && cd $S/arc && ln -s /Users/arsis/zlayt-pm-project/.venv .venv && (time .venv/bin/python -m pytest tests/unit/test_flag_origin_t214.py tests/unit/test_prepared_property.py tests/unit/test_prepared_provenance.py tests/unit/test_prepared_provenance_r3.py tests/unit/test_flags_sample.py -q -x -p no:cacheprovider 2>&1 | tail -15)"
}
````

### User / tool · 2026-11-03T13:25:47.741Z

**tool result**
````
MM .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
D  .claude/agent-memory/backend/project_t202_r5_d073.md
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
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
            c, tok, status, res = run_variant(sub, monkeypatch, "sample", "valid", "one", shipped=True, mode=mode)
>           assert len(prepared_items(res)) >= 16, mode
E           AssertionError: None
E           assert 15 >= 16
E            +  where 15 = len(['item:e1', 'item:e2', 'item:e3', 'item:e4', 'item:e5', 'item:e6', ...])
E            +    where ['item:e1', 'item:e2', 'item:e3', 'item:e4', 'item:e5', 'item:e6', ...] = prepared_items({'case': {'token': '4BMFp3UpWCR62Y5QLxrhXg', 'name': 'Sample case', 'status': 'ready', 'demo_mode': True, ...}, '/stat...: 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}, 'independent_models': True, ...}, ...})

tests/unit/test_prepared_property.py:303: AssertionError
------------------------------ Captured log call -------------------------------
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c91d74e829788 step=j1 attempt=1 prompt_hash=6ef69725d811139b8fec56b34c8886858b627c3c98269e686c98de41ad841dff
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c12c54b44f52b step=j1 attempt=1 prompt_hash=d625988273a9c816758784ab6214e0ef9d483848cb415dd32c903bc64879a89a
=========================== short test summary info ============================
FAILED tests/unit/test_prepared_property.py::test_shipped_curated_sample_in_demo_and_local_mode
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 29 passed, 3 skipped in 44.05s

real	0m44.463s
user	0m21.339s
sys	0m10.576s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:25:50.239Z

**tool call — Bash**
````
{
 "command": "sed -n 296,306p tests/unit/test_prepared_property.py; git diff --stat HEAD -- tests/unit/test_prepared_property.py"
}
````

### User / tool · 2026-11-03T13:25:50.342Z

**tool result**
````
def test_shipped_curated_sample_in_demo_and_local_mode(tmp_path, monkeypatch):
    for mode in (None, "local"):
        sub = tmp_path / (mode or "demo")
        for n in ("rec", "keys", "run", "set"):
            (sub / n).mkdir(parents=True)
        c, tok, status, res = run_variant(sub, monkeypatch, "sample", "valid", "one", shipped=True, mode=mode)
        assert len(prepared_items(res)) >= 16, mode
        _assert_clean(res, f"shipped/{mode}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:25:56.184Z

**tool call — Bash**
````
{
 "command": "sed -i '303s/.*/        assert len(prepared_items(res)) >= 15, mode      # T-214: f_r7_1 (phrase list only) is no longer a prepared item; the 15 others have a curated answer/' tests/unit/test_prepared_property.py && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp tests/unit/test_prepared_property.py $S/arc/tests/unit/ && cd $S/arc && .venv/bin/python -m pytest tests/unit/test_prepared_property.py tests/unit/test_prepared_provenance.py tests/unit/test_prepared_provenance_r3.py tests/unit/test_flags_sample.py tests/unit/test_flag_origin_t214.py -q -p no:cacheprovider 2>&1 | tail -8"
}
````

### User / tool · 2026-11-03T13:25:56.269Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/unit/test_prepare ...": undefined label 'ests/unit/test_prepared_property.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:26:03.728Z

**tool call — Bash**
````
{
 "command": "sed -i '' '303s/.*/        assert len(prepared_items(res)) >= 15, mode      # T-214: f_r7_1 (phrase list only) is no longer prepared; the 15 others have a curated answer/' tests/unit/test_prepared_property.py && sed -n 303p tests/unit/test_prepared_property.py && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp tests/unit/test_prepared_property.py $S/arc/tests/unit/ && cd $S/arc && .venv/bin/python -m pytest tests/unit/test_prepared_property.py tests/unit/test_prepared_provenance.py tests/unit/test_prepared_provenance_r3.py tests/unit/test_flags_sample.py tests/unit/test_flag_origin_t214.py -q -p no:cacheprovider 2>&1 | tail -8"
}
````

### User / tool · 2026-11-03T13:27:02.819Z

**tool result**
````
        assert len(prepared_items(res)) >= 15, mode      # T-214: f_r7_1 (phrase list only) is no longer prepared; the 15 others have a curated answer
.s.........s.........s.................................................. [ 97%]
..                                                                       [100%]
71 passed, 3 skipped in 58.50s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:05.693Z

Now api.md note, board, commit.

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:10.966Z

**tool call — Bash**
````
{
 "command": "git diff --stat HEAD -- memory/contracts/api.md | tail -1; cat >> memory/contracts/api.md <<'EOF'\n- **T-214 (D-065, flag provenance):** a flag whose only source is code (`origin` `lexicon`, the phrase list found it and the answers did not, or `code`, a computed gap/conflict) has `prepared: false` and `origin_label` `\"Found by code (phrase list)\"` / `\"Found by code\"` (null for `llm` and `lexicon+llm`). `prepared: true` stays only for an item with a curated answer behind it. On the sample, `f_r7_1` no longer carries the \"Prepared answer\" tag. The wording of its sentences still follows the case (prepared templates in a prepared case). Frontend: show `origin_label` where the tag would be.\nEOF\nB=\"python3 tools/board.py\"; $B ac T-214 --check 1 --agent backend --evidence \"tests/unit/test_flag_origin_t214.py (curated sample + recorded set + item detail), test_prepared_property.py, test_prepared_provenance*.py, test_flags_sample.py: 71 passed from git archive copy\"\n$B handoff T-214 --agent backend --text \"What changed: present.with_provenance sets prepared=false and origin_label ('Found by code (phrase list)' / 'Found by code') for flags with origin lexicon/code (CODE_ONLY_FLAG_ORIGINS); api.md note; property floor 16->15. Verified: 71 passed from git archive overlay (no export.py/service_date.py). Left: frontend can show origin_label. Surprised: only f_r7_1 on the sample was affected.\"\n$B move T-214 in_review --agent backend\nexport GIT_INDEX_FILE=/Users/arsis/zlayt-pm-project/.scratch/t214.idx; git read-tree HEAD && git add app/backend/present.py tests/unit/test_flag_origin_t214.py tests/unit/test_prepared_property.py memory/contracts/api.md && git commit -q -m \"fix(backend): flags found only by code are not prepared answers (T-214)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- app/backend/present.py tests/unit/test_flag_origin_t214.py tests/unit/test_prepared_property.py memory/contracts/api.md && SHA=$(git rev-parse HEAD) && unset GIT_INDEX_FILE && $B commit T-214 --sha $SHA --agent backend; git show --stat --oneline $SHA | tail -6"
}
````

### User / tool · 2026-11-03T13:27:11.068Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: git diff --stat HEAD -- memory/contracts/api.md | tail -1; cat >> memory/contracts/api.md <<'EOF'
- **T-214 (D-065, flag provenance):** a flag whose only source is code (`origin` `lexicon`, the phrase
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:15.316Z

**tool call — Bash**
````
{
 "command": "cat >> memory/contracts/api.md <<'EOF'\n- **T-214 (D-065, flag provenance):** a flag whose only source is code (`origin` `lexicon`, the phrase list found it and the answers did not, or `code`, a computed gap/conflict) has `prepared: false` and `origin_label` `\"Found by code (phrase list)\"` / `\"Found by code\"` (null for `llm` and `lexicon+llm`). `prepared: true` stays only for an item with a curated answer behind it. On the sample, `f_r7_1` no longer carries the \"Prepared answer\" tag. The wording of its sentences still follows the case (prepared templates in a prepared case). Frontend: show `origin_label` where the tag would be.\nEOF\nB=\"python3 tools/board.py\"; $B ac T-214 --check 1 --agent backend --evidence \"tests/unit/test_flag_origin_t214.py (curated sample + recorded set + item detail), test_prepared_property.py, test_prepared_provenance*.py, test_flags_sample.py: 71 passed from git archive copy\"\n$B handoff T-214 --agent backend --text \"What changed: present.with_provenance sets prepared=false and origin_label ('Found by code (phrase list)' / 'Found by code') for flags with origin lexicon/code (CODE_ONLY_FLAG_ORIGINS); api.md note; property floor 16->15. Verified: 71 passed from git archive overlay (no export.py/service_date.py). Left: frontend can show origin_label. Surprised: only f_r7_1 on the sample was affected.\"\n$B move T-214 in_review --agent backend"
}
````

### User / tool · 2026-11-03T13:27:15.554Z

**tool result**
````
AC 1 checked: tests/unit/test_flag_origin_t214.py (curated sample + recorded set + item detail), test_prepared_property.py, test_prepared_provenance*.py, test_flags_sample.py: 71 passed from git archive copy
handoff written on T-214
T-214: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:16.211Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/Users/arsis/zlayt-pm-project/.scratch/t214.idx; rm -f $GIT_INDEX_FILE; git read-tree HEAD && git add app/backend/present.py tests/unit/test_flag_origin_t214.py tests/unit/test_prepared_property.py memory/contracts/api.md && git diff --cached --stat | tail -6"
}
````

### User / tool · 2026-11-03T13:27:17.049Z

**tool result**
````
 app/backend/present.py               |  4 ++++
 memory/contracts/api.md              |  1 +
 tests/unit/test_flag_origin_t214.py  | 32 ++++++++++++++++++++++++++++++++
 tests/unit/test_prepared_property.py |  2 +-
 4 files changed, 38 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:21.046Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/Users/arsis/zlayt-pm-project/.scratch/t214.idx; git commit -q -m \"fix(backend): flags found only by code are not prepared answers (T-214)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- app/backend/present.py tests/unit/test_flag_origin_t214.py tests/unit/test_prepared_property.py memory/contracts/api.md; SHA=$(git rev-parse HEAD); unset GIT_INDEX_FILE; python3 tools/board.py commit T-214 --sha $SHA --agent backend; git show --stat --oneline $SHA | tail -6"
}
````

### User / tool · 2026-11-03T13:27:25.880Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
T-214: commit d15c9ab3fd18bd7759d7a44cf190115163aec4d5 recorded
d15c9ab fix(backend): flags found only by code are not prepared answers (T-214)
 app/backend/present.py               |  4 ++++
 memory/contracts/api.md              |  1 +
 tests/unit/test_flag_origin_t214.py  | 32 ++++++++++++++++++++++++++++++++
 tests/unit/test_prepared_property.py |  2 +-
 4 files changed, 38 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T13:27:31.298Z

T-214 is in review as commit d15c9ab. On the sample, f_r7_1 now has `prepared=false` and `origin_label` "Found by code (phrase list)". Flags with code origin get "Found by code". The 71 targeted tests pass from a `git archive` copy, covering the prepared-property, provenance and sample tests plus a new `tests/unit/test_flag_origin_t214.py`.

The property test's floor of prepared items on the sample dropped from 16 to 15, since f_r7_1 was the one that no longer counts. The change is in `app/backend/present.py`, with a note in `memory/contracts/api.md`; `export.py` and `service_date.py` were untouched. The frontend still needs to show `origin_label` where the tag was.
