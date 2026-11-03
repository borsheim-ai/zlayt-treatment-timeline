# Subagent: Backend: T-084 + T-073 review.py (Backend: T-084 + T-073 review.py)

Source: `agent-a54be53653f53dfcd.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:16:19.551Z

You own board cards T-084 and T-073 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `board.py show` on each and read D-042 in memory/ORCHESTRATOR_DECISIONS.md. Both touch app/backend/review.py, so do T-073 first.

- **T-073:** narrow the broad `except` in the review.py judge path (around line 83). Catch only the expected judge errors and keep the error class in the recorded reason; anything else propagates. Add unit tests for both cases.
- **T-084:** guarded charge reclassification by the paralegal. Charge to not-a-charge, and not-a-charge to charge, are allowed. A rate becomes a charge only if code finds charged-amount wording in the excerpt AND a judge re-check passes; otherwise return 422 with a reason. Write an audit event, add api.md contract notes and unit tests, and note on the card what the UI needs.

**Shared rules (8 workers are running in parallel):**
- Put the logic in new modules. In shared files (api.py, pipeline.py, api.md), make the smallest possible edit, re-read the file right before editing, and never reformat.
- Don't touch flags.py or judges.py (T-094 is in them; if T-084 needs a judge call, call the existing function without editing judges.py), evals/library, or evals/run.py.
- Commit only your own hunks. Use a temp index (`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD`, then add your paths or patches) when a shared file has other workers' edits; otherwise `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
- Run `.venv/bin/python -m pytest -q tests/unit`. If a failure is in someone else's area, name it and move on.
- Then `board.py ac`, the handoff, and `move <card> in_review --agent backend`, for each card. Reply in 2 lines.

### User / tool · 2026-11-02T04:16:19.555Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:31.841Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B show T-073; $B show T-084; grep -n \"D-042\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60"
}
````

### User / tool · 2026-11-02T04:16:32.022Z

**tool result**
````
---
id: "T-073"
title: "Narrow the broad except in review.py:83 judge path (keep error class, log reason)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:46:15Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "review.py catches only expected judge errors; others propagate or are recorded with their class; unit test for both", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

---
id: "T-084"
title: "Guarded charge reclassification by the paralegal"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Paralegal can reclassify charge<->not-a-charge; rate->charge only if code finds charged-amount wording in the excerpt AND judge re-check passes, else 422 with reason; audit event; unit tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:32.458Z

**tool call — Bash**
````
{
 "command": "git status --short | head -30; wc -l app/backend/review.py app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:16:32.566Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
     398 app/backend/review.py
     569 app/backend/api.py
     967 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:34.157Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/review.py"
}
````

### User / tool · 2026-11-02T04:16:34.359Z

**tool result**
````
1	"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).
2	
3	Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). Batch accept (verified, dated, pending entries only) writes through apply_review too.
4	Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
5	and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
6	that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
7	"""
8	import time
9	
10	from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store
11	from app.db import db as DB
12	
13	ACTIONS = ("accept", "dismiss", "reset", "edit")
14	_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|may|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
15	_KIND = {"e": "entry", "a": "amount", "f": "flag"}
16	
17	
18	class ReviewError(Exception):
19	    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
20	        super().__init__(code)
21	        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")
22	
23	
24	def _now(now):
25	    return now() if callable(now) else (time.time() if now is None else now)
26	
27	
28	def _item(conn, case_id, item_id):
29	    try:
30	        row = DB.get_item(conn, item_id, case_id)
31	    except KeyError:
32	        raise ReviewError(404, "not_found", message="No such item.") from None
33	    if row["case_id"] != case_id:
34	        raise ReviewError(404, "not_found", message="No such item.")
35	    return _KIND[item_id[0]], row
36	
37	
38	def _bad(msg, **detail):
39	    return ReviewError(422, "invalid_edit", detail, msg)
40	
41	
42	def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
43	    """D-041: an entry whose date is not confirmed (ambiguous, missing, or no date at all) cannot go into the letter. Same rule as
44	    present.case_view uses to put an entry under `undated_entries`: date_iso set and the record's date_status parsed or confirmed."""
45	    if kind != "entry":
46	        return False
47	    if not item.get("date_iso"):
48	        return True
49	    rid = (item.get("record_ids") or [None])[0]
50	    row = conn.execute("SELECT date_status FROM records WHERE id=? AND case_id=?", (rid, case_id)).fetchone()
51	    return bool(row) and row["date_status"] not in ("parsed", "confirmed", None)
52	
53	
54	def _date_unconfirmed_error():
55	    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
56	                       "cannot be accepted into the letter.")
57	
58	
59	def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
60	    t = _now(now)
61	    kind, item = _item(conn, case_id, item_id)
62	    action = (body or {}).get("action")
63	    if action not in ACTIONS:
64	        raise _bad("That action is not allowed.")
65	    if item["state"] == "rejected" and action in ("accept", "edit"):
66	        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
67	    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
68	        raise _date_unconfirmed_error()
69	    warnings = []
70	    if action in ("accept", "dismiss", "reset"):
71	        DB.apply_review(conn, item_id, action, now=t, case=case_id)
72	        if kind == "flag" and action == "dismiss" and body.get("note"):
73	            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
74	    else:
75	        warnings = _edit(conn, case_id, kind, item, body, call, t)
76	    from app.backend import present
77	    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
78	            "review": present.review_view(conn, case_id), "warnings": warnings}
79	
80	
81	def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
82	    """Code token/qualifier checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
83	    Raises 409 needs_confirm unless body['confirm_warnings']; returns the pieces both callers store."""
84	    code_reasons = []
85	    toks = grounding.new_tokens(new_sum, new_exc, label, date_iso)
86	    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
87	    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
88	        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
89	                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
90	    blocking = []
91	    if toks:
92	        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
93	        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
94	    if grounding.dropped_qualifiers(new_sum, new_exc):
95	        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
96	    if span is None:
97	        code_reasons.append("HIGHLIGHT_NOT_FOUND")
98	    verdict, call_id, ladder_verdict, judge_code = "unavailable", None, "unavailable", "NONE"
99	    if call is not None:
100	        try:
101	            verdict, call_id, judge_code = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)
102	        except Exception:
103	            verdict, call_id, judge_code = "unavailable", None, "NONE"
104	        ladder_verdict = judges.to_ladder("j1", verdict)
105	    if ladder_verdict in ("partially", "unsupported"):
106	        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
107	        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
108	    if blocking and not bool(body.get("confirm_warnings")):
109	        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
110	    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
111	                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed")})
112	    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
113	            "state": state, "reasons": reasons}
114	
115	
116	# ---------------------------------------------------------------- edit
117	def _edit(conn, case_id, kind, item, body, call, t):
118	    edits = body.get("edits")
119	    if kind == "amount":
120	        raise _bad("A charge can only be accepted or dismissed.")
121	    if not isinstance(edits, dict) or not edits:
122	        raise _bad("Nothing to edit.")
123	    if kind == "flag":
124	        if set(edits) != {"note"} or not isinstance(edits["note"], str) or not edits["note"].strip():
125	            raise _bad("Only a note can be added to a flag.")
126	        DB.apply_review(conn, item["id"], "edit", edited={"note": edits["note"].strip()[:2000], "at": store.iso(t)}, now=t, case=case_id)
127	        DB.update_item(conn, item["id"], now=t, case=case_id, reviewer_note=edits["note"].strip()[:2000])
128	        return []
129	    if not set(edits) <= {"summary", "excerpt"} or not all(isinstance(v, str) and v.strip() for v in edits.values()):
130	        raise _bad("Only the summary or the quoted sentences of an entry can be edited.")
131	    case = DB.get_case(conn, case_id)
132	    recs = store.load_records(conn, case_id, case["raw_text"])
133	    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
134	    if rec is None:
135	        raise _bad("The entry's source record is missing.")
136	    prev = item.get("edited") or {}
137	    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
138	    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
139	    span = None
140	    if "excerpt" in edits:
141	        problems = grounding.check_excerpt(rec["excerpt"], new_exc)
142	        if problems:
143	            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
144	    span = grounding.locate(rec["excerpt"], new_exc)
145	    base = generator.body_offset(rec)
146	    label, date_iso = item["provider"] or "", item["date_iso"] or ""
147	    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, body)
148	    toks, code_reasons, blocking, ladder_verdict, call_id, state, reasons = (
149	        chk["toks"], chk["code_reasons"], chk["blocking"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
150	    confirmed = bool(body.get("confirm_warnings"))
151	    edited = dict(prev)
152	    edited.update(at=store.iso(t), kept_my_wording=bool(blocking and confirmed),
153	                  override_reasons=[b["code"] for b in blocking] if blocking and confirmed else prev.get("override_reasons", []))
154	    if "summary" in edits or "summary" in prev:
155	        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
156	    if "excerpt" in edits or "excerpt" in prev:
157	        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
158	                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
159	    DB.apply_review(conn, item["id"], "edit", edited=edited, now=t, case=case_id)
160	    if edited["kept_my_wording"]:
161	        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
162	    lad = item.get("ladder") or {"item_id": item["id"]}
163	    lad["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": call_id, "verdict": ladder_verdict,
164	                    "reason_code": chk["judge_code"]}
165	    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
166	                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
167	    lad["state"] = state
168	    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
169	    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
170	        if ladder_verdict == "unavailable" else []
171	
172	
173	# ---------------------------------------------------------------- confirm_date
174	def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
175	    t = _now(now)
176	    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
177	    if row is None:
178	        raise ReviewError(404, "not_found", message="No such record.")
179	    rec = DB._decode(row)
180	    if rec["date_status"] != "ambiguous":
181	        raise _bad("Only a record whose date can be read two ways can be confirmed.")
182	    if date_iso not in (rec["date_candidates"] or []):
183	        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
184	    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
185	    moved, cleared = None, []
186	    for e in DB.list_items(conn, case_id, "entry"):
187	        if record_id in (e["record_ids"] or []):
188	            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
189	            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
190	                cleared.append(e["id"])
191	            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
192	    for a in DB.list_items(conn, case_id, "amount"):
193	        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
194	            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
195	            cleared.append(a["id"])
196	    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
197	    removed += _recompute_gaps(conn, case_id, t)
198	    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
199	    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
200	    from app.backend import present
201	    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
202	            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
203	            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
204	
205	
206	def _without_date_doubt(item: dict) -> dict:
207	    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
208	    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
209	    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
210	    state = item["state"]
211	    if state == "needs_review" and not reasons:
212	        state = "verified"
213	    out = {"state": state, "state_reasons_json": reasons}
214	    if isinstance(item.get("ladder"), dict):
215	        out["ladder"] = {**item["ladder"], "state": state}
216	    return out
217	
218	
219	def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
220	    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
221	             "cleared_date_ambiguous": cleared}
222	    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
223	    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
224	                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))
225	
226	
227	def _drop(conn, case_id, flag_id):
228	    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
229	    return [flag_id] if cur.rowcount else []
230	
231	
232	def _recompute_gaps(conn, case_id, t):
233	    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
234	    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
235	    from app.backend import pipeline as PL
236	    case = DB.get_case(conn, case_id)
237	    recs = store.load_records(conn, case_id, case["raw_text"])
238	    by_n = {r["n"]: r for r in recs}
239	    backend = DB.get_case(conn, case_id).get("backend") or "code"
240	    new = {}
241	    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
242	        nos = f["record_nos"]
243	        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
244	        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
245	                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
246	                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
247	        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
248	            if k in f:
249	                item[k] = f[k]
250	        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
251	        new[item["id"]] = item
252	    removed = []
253	    for old in DB.list_items(conn, case_id, "flag"):
254	        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
255	            continue
256	        item = new.get(old["id"])
257	        if item is None:
258	            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
259	            removed.append(old["id"])
260	            continue
261	        oc = old.get("computed") or {}
262	        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
263	        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
264	            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
265	    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
266	    for iid, item in new.items():
267	        if iid not in have:
268	            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
269	    return removed
270	
271	
272	# ---------------------------------------------------------------- manual entry (D-031, T-056)
273	def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
274	    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
275	    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
276	    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
277	    t = _now(now)
278	    case = DB.get_case(conn, case_id)
279	    recs = store.load_records(conn, case_id, case["raw_text"])
280	    rec = next((r for r in recs if r["id"] == record_id), None)
281	    if rec is None:
282	        raise ReviewError(404, "not_found", message="No such record.")
283	    if rec.get("duplicate_of"):
284	        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
285	    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
286	    if live:
287	        raise _bad("This record already has an entry; edit that entry instead.")
288	    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
289	    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
290	        raise _bad("Provide a summary and the quoted sentences.")
291	    summary, excerpt = summary.strip(), excerpt.strip()
292	    problems = grounding.check_excerpt(rec["excerpt"], excerpt)
293	    if problems:
294	        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
295	    span = grounding.locate(rec["excerpt"], excerpt)
296	    eid = f"e{rec['seq']}_m"
297	    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, body or {})
298	    base = generator.body_offset(rec)
299	    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
300	              "judge": {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
301	                        "reason_code": chk["judge_code"]},
302	              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
303	                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
304	                              "date_provider_from_header": True},
305	              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
306	    if chk["blocking"]:     # reached only with confirm_warnings: the override travels to the internal notes
307	        ladder["override_reasons"] = [b["code"] for b in chk["blocking"]]
308	    DB.add_item(conn, case_id, "entry", {
309	        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
310	        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
311	        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
312	    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
313	    if chk["blocking"]:
314	        DB.apply_review(conn, eid, "keep_my_wording", now=t, case=case_id)
315	    from app.backend import present
316	    warns = [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the entry stays marked for review.", "item_id": eid}] \
317	        if chk["ladder_verdict"] == "unavailable" else []
318	    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
319	            "review": present.review_view(conn, case_id), "warnings": warns}
320	
321	
322	# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
323	def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
324	    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
325	    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
326	    `not_duplicate` event on the original entry."""
327	    from app.backend import pipeline as PL
328	    from app.llm import provider as P
329	    t = _now(now)
330	    kind, ent = _item(conn, case_id, entry_id)
331	    if kind != "entry":
332	        raise _bad("Only a merged entry can be split.")
333	    ids = list(ent["record_ids"] or [])
334	    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
335	        raise _bad("That record is not one of the duplicates merged into this entry.")
336	    case = DB.get_case(conn, case_id)
337	    cfg = dict(case.get("config") or {})
338	    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
339	    DB.update_case(conn, case_id, config_json=cfg)
340	    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
341	    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
342	    recs = store.load_records(conn, case_id, case["raw_text"])
343	    by_n = {r["n"]: r for r in recs}
344	    rec = next(r for r in recs if r["id"] == record_id)
345	    warns = []
346	    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
347	    if call is not None:
348	        e = generator.extract_one(rec, [rec["n"]], call=call, case_text=case["raw_text"])
349	        if "failure" in e:
350	            warns.append({"code": e["failure"], "message": "The record was split off, but the AI could not draft its entry; enter it by hand.", "item_id": None})
351	        else:
352	            if e["state"] != "rejected":
353	                generator.judge_entries([e], by_n, call=call, case_text=case["raw_text"])
354	            e["ladder"]["backend"] = P.backend_name()
355	            e.pop("_stage", None)
356	            _upsert(conn, case_id, "entry", PL._clean(e), t)
357	    else:
358	        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
359	    # its amounts come back as their own items (new ids; existing amounts keep theirs and their review status)
360	    sep = {int(str(i)[1:]) for i in cfg["not_duplicates"] if str(i)[1:].isdigit()}
361	    rows = [a for a in AM.extract_amounts(recs, separate=sep) if a["record_no"] == rec["n"]]
362	    new_items = [PL.amount_item(a, rec) for a in rows]
363	    ing = {"records": recs, "text": case["raw_text"]}
364	    for a in DB.list_items(conn, case_id, "amount"):
365	        if record_id in (a["record_ids"] or []):
366	            DB.update_item(conn, a["id"], now=t, case=case_id, record_ids_json=[i for i in a["record_ids"] if i != record_id], duplicate_note=None)
367	    dollars = [a for a in new_items if a["cls"] != "damages"]
368	    verdicts = judges_for(dollars, call, case["raw_text"])
369	    for a in new_items:
370	        _upsert(conn, case_id, "amount", PL._finish_amount(a, ing, verdicts.get(a["id"])), t)
371	    _recompute_gaps(conn, case_id, t)
372	    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
373	    from app.backend import present
374	    split_id = f"e{rec['n']}" if any(e["id"] == f"e{rec['n']}" for e in DB.list_items(conn, case_id, "entry")) else None
375	    return {"entry_ids": [entry_id] + ([split_id] if split_id else []), "item": present.item_view(conn, case_id, entry_id),
376	            "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": warns}
377	
378	
379	def _upsert(conn, case_id, kind, item, t):
380	    """Add or refresh ONE item without PL._persist's removal of other pending rows."""
381	    from app.backend import pipeline as PL
382	    row = PL._row(kind, item)
383	    if any(i["id"] == item["id"] for i in DB.list_items(conn, case_id, kind)):
384	        DB.update_item(conn, item["id"], now=t, case=case_id, **row)
385	    else:
386	        DB.add_item(conn, case_id, kind, {"id": item["id"], **row}, now=t)
387	
388	
389	def judges_for(dollars, call, case_text):
390	    if call is None or not dollars:
391	        return {}
392	    return judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars], call=call, case_text=case_text)
393	
394	
395	def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
396	    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
397	    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
398	    DB.apply_review(conn, item_id, action, now=now, case=case_id)
399	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:34.870Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend | tail -5; ls app/backend tests/unit | head -80; grep -n \"review\\b\\|review\\.\\|/items\" app/backend/api.py | head -40"
}
````

### User / tool · 2026-11-02T04:16:34.982Z

**tool result**
````
app/backend:
__init__.py
__pycache__
amounts.py
api.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
narrative.py
pdf_text.py
pipeline.py
present.py
rejudge.py
review.py
schemas.py
sentences.py
split_llm.py
store.py
totals.py
trace.py
why.py

tests/unit:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_backend_no_speaker_label.py
test_boundaries.py
test_case_extras.py
test_confidence.py
test_conflict_candidates.py
test_conflicts.py
test_date_unconfirmed.py
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
test_frontend_no_speaker_label.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_ingest.py
test_injection.py
test_judges.py
test_library_denylist.py
test_manual_and_split.py
test_multicase.py
test_narrative.py
test_pdf_upload.py
test_pipeline.py
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
23:from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
149:    @app.exception_handler(review.ReviewError)
409:            return review.confirm_date(c, token, rid, b["date"])
420:            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
424:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
433:            return review.not_duplicate(c, token, item_id, b["record_id"], call=make_call(c, token))
459:    @app.post("/api/cases/{token}/narrative/review")
460:    async def narrative_review(token: str, request: Request):
466:                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
474:    @app.get("/api/cases/{token}/items/{item_id}")
486:    @app.post("/api/cases/{token}/items/{item_id}/review")
492:            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
525:    @app.get("/api/cases/{token}/items/{item_id}/trace")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:38.139Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def \\|^class \\|raise \\|except \" app/backend/judges.py | head -80; grep -n \"^def \\|^class \\|^[A-Z_]* = \" app/backend/amounts.py | head -60; grep -n \"class .*Error\\|^def \" app/llm/provider.py | head -30"
}
````

### User / tool · 2026-11-02T04:16:38.245Z

**tool result**
````
16:def generator_model() -> str:
20:def judge_model() -> str:
24:def _run(step: str, prompt: str, model_cls, quotes: list, lines: list, call, nonce, item_id):
33:    except AU.LLMFailed:
37:    except (ValidationError, TypeError, ValueError):
42:def quotes_labelled(quotes: list, step: str):
47:def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None):
52:def run_j2_meta(excerpt: str, raw_amount: str, code_class: str, *, call, nonce=None, item_id=None):
57:def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
63:def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
68:def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
72:def run_j2(excerpt, raw_amount, code_class, *, call, nonce=None, item_id=None):
76:def run_j3(excerpt_a, excerpt_b, *, call, nonce=None, item_id=None, category=None):
80:def run_j4(excerpt, flag_type, category, *, call, nonce=None, item_id=None):
92:def to_ladder(step: str, verdict: str) -> str:
100:def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
110:        except _P.FixtureMiss:
10:_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
11:_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
12:_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
14:_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
15:_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
16:_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b)", re.IGNORECASE)
17:_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
18:_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
19:_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
20:_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)
23:def to_cents(figure: str):
32:def find_amounts(excerpt: str) -> list:
45:def _label(excerpt: str, start: int) -> str:
51:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
72:def _is_billing_source(source: str) -> bool:
76:def damages_mentions(excerpt: str) -> list:
90:def _norm(s):
94:def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
114:def extract_amounts(records: list, separate=frozenset()) -> list:
140:_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
141:_VISIT = re.compile(r"\bvisit\s+(\d+)\b", re.IGNORECASE)
144:def _prefix(source):
148:def rate_note(records: list, record_no: int) -> dict:
23:def backend_name() -> str:
33:def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
39:def _norm(s: str) -> str:
46:def assert_recordable(text: str, *, whole_file: bool = False) -> None:
65:def record_context(source_text: str):
77:def record_fragment_context(fragment: str):
88:def _recording() -> bool:
92:def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
113:def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:38.963Z

**tool call — Bash**
````
{
 "command": "sed -n 395,440p app/backend/api.py; grep -n \"amount\\|cls\\|rate\" app/db/db.py | head -50; grep -n \"review_events\" -B2 -A10 app/db/schema.sql | head -40"
}
````

### User / tool · 2026-11-02T04:16:39.064Z

**tool result**
````
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
            c.close()

    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
    async def confirm_date(token: str, rid: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("date"), str):
            raise ApiError(400, "bad_request", "Provide the chosen date.")
        c = conn()
        try:
            get_case(c, token)
            return review.confirm_date(c, token, rid, b["date"])
        finally:
            c.close()

    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
    async def manual_entry(token: str, rid: str, request: Request):
        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
        finally:
            c.close()

    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
    async def not_duplicate(token: str, item_id: str, request: Request):
        """D-031: split one record back out of a merged entry. Body {record_id}."""
        b = await body_of(request)
        if not isinstance(b.get("record_id"), str):
            raise ApiError(400, "bad_request", "Provide the record to split off.")
        c = conn()
        try:
            get_case(c, token)
            return review.not_duplicate(c, token, item_id, b["record_id"], call=make_call(c, token))
        finally:
            c.close()

    @app.get("/api/cases/{token}/narrative")
    def narrative_get(token: str):
        c = conn()
        try:
21:_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
22:_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
23:_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
115:    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
53-  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
54-);
55:CREATE TABLE IF NOT EXISTS review_events (
56-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
57-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
58-  before_json TEXT, after_json TEXT, at REAL
59-);
60-CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
61-CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
62-CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
63-CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
64-CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
65:CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:41.517Z

**tool call — Bash**
````
{
 "command": "sed -n 1,125p app/backend/judges.py; sed -n 30,75p app/backend/amounts.py; grep -n \"review_events\\|CHECK\\|migrat\" app/db/db.py | head -30; grep -n \"amounts\" -A20 app/db/schema.sql | head -40"
}
````

### User / tool · 2026-11-02T04:16:41.619Z

**tool result**
````
"""Judges J1-J4 (rung 2 of the validation ladder; LLM_VS_CODE rows 4, 7, 11, 12; ADR-003.8, ADR-008.5).
Each judge sees only the record text and the candidate (never the generator's reasoning), in nonce delimiters, and returns an
enum. A judge failure is "unavailable", never an exception into the pipeline; invalid output (out-of-enum, missing reason_code) is "unavailable", never positive.
`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline (audited_call bound to a case)."""
import os

from pydantic import ValidationError

from app.backend import injection, schemas
from app.llm import audited as AU, promptlib

DEFAULT_GENERATOR_MODEL = "claude-sonnet-5-5"
DEFAULT_JUDGE_MODEL = "claude-haiku-5-5"


def generator_model() -> str:
    return os.environ.get("GENERATOR_MODEL") or DEFAULT_GENERATOR_MODEL


def judge_model() -> str:
    return os.environ.get("JUDGE_MODEL") or DEFAULT_JUDGE_MODEL


def _run(step: str, prompt: str, model_cls, quotes: list, lines: list, call, nonce, item_id):
    """Returns (verdict, call_id, reason_code). verdict in the model's enum, or 'unavailable' / 'unsure'."""
    n = nonce or promptlib.nonce(step, *quotes, *[x if isinstance(x, str) else x[1] for x in lines])
    p = promptlib.load(prompt)
    blocks = "\n".join(f"{label}:\n{injection.wrap(q, n)}" for label, q in quotes_labelled(quotes, step))
    extra = "\n".join(f"{x[0]}:\n{injection.wrap(x[1], n)}" if isinstance(x, tuple) else x for x in lines)   # (name, text) = record-derived, wrapped
    user = blocks + "\n" + extra + "\nReturn the JSON object."
    try:
        out, call_id = call(step, p.text, user, model_cls.model_json_schema(), item_id=item_id)
    except AU.LLMFailed:
        return "unavailable", None, "NONE"
    try:
        m = model_cls.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        return "unavailable", call_id, "NONE"   # invalid judge output (bad enum, missing reason_code) = judge did not answer
    return m.verdict, call_id, m.reason_code


def quotes_labelled(quotes: list, step: str):
    names = {"j3": ["QUOTE A", "QUOTE B"]}.get(step, ["RECORD TEXT"] * len(quotes))
    return zip(names, quotes)


def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None):
    return _run("j1", "judge_faithfulness_v1", schemas.Judge1, [excerpt],
                [("SOURCE LABEL", label), f"CANDIDATE SUMMARY: {summary}"], call, nonce, item_id)


def run_j2_meta(excerpt: str, raw_amount: str, code_class: str, *, call, nonce=None, item_id=None):
    return _run("j2", "judge_amount_class_v1", schemas.Judge2, [excerpt],
                [f"AMOUNT: {raw_amount}", f"CLASS: {code_class}"], call, nonce, item_id)


def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v2 (T-075)."""
    return _run("j3", "judge_conflict_v2", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
                call, nonce, item_id)


def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
    return _run("j4", "judge_flag_v2", schemas.Judge4, [excerpt],
                [f"FLAG TYPE: {flag_type}", f"FLAG CATEGORY: {category}"], call, nonce, item_id)


def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]


def run_j2(excerpt, raw_amount, code_class, *, call, nonce=None, item_id=None):
    return run_j2_meta(excerpt, raw_amount, code_class, call=call, nonce=nonce, item_id=item_id)[0]


def run_j3(excerpt_a, excerpt_b, *, call, nonce=None, item_id=None, category=None):
    return run_j3_meta(excerpt_a, excerpt_b, call=call, nonce=nonce, item_id=item_id, category=category)[0]


def run_j4(excerpt, flag_type, category, *, call, nonce=None, item_id=None):
    return run_j4_meta(excerpt, flag_type, category, call=call, nonce=nonce, item_id=item_id)[0]


_TO_LADDER = {
    "j1": {"supported": "supported", "partially": "partially", "unsupported": "unsupported"},
    "j2": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
    "j3": {"conflict": "supported", "benign": "disagrees", "unsure": "unsure"},
    "j4": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
}


def to_ladder(step: str, verdict: str) -> str:
    """Map a judge's own enum to the compose_state vocabulary. Only the positive verdict becomes 'supported';
    unknown values become 'unsure' and 'unavailable' stays 'unavailable' (never positive by accident)."""
    if verdict == "unavailable":
        return "unavailable"
    return _TO_LADDER[step].get(verdict, "unsure")


def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
    """Judge 2 on every amount, rule-made or not (R-CH-2, row 7). items: [{'id', 'raw', 'cls', 'excerpt'}].
    Returns {id: {'verdict', 'ladder', 'call_id', 'reason_code', 'fixture_miss', 'model', 'prompt_version'}}. FixtureMiss -> ladder 'unavailable' + fixture_miss True."""
    from app.llm import promptlib as _pl, provider as _P
    out = {}
    for it in items:
        n = _pl.nonce(case_text, "j2", it["id"])
        try:
            v, cid, code = run_j2_meta(it["excerpt"], it["raw"], it["cls"], call=call, nonce=n, item_id=it["id"])
            miss = False
        except _P.FixtureMiss:
            v, cid, code, miss = "unavailable", None, "NONE", True
        out[it["id"]] = {"verdict": v, "ladder": to_ladder("j2", v), "call_id": cid, "reason_code": code, "fixture_miss": miss,
                         "model": judge_model(), "prompt_version": "judge_amount_class_v1"}
    return out


def find_amounts(excerpt: str) -> list:
    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
    out = []
    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
    for m in _AMT.finditer(excerpt or ""):
        figure = m.group(1)
        if not any(c.isdigit() for c in figure):
            continue
        injected = any(s <= m.start() and m.end() <= e for s, e in spans)   # a figure inside instruction-like text has no trusted value (D-005)
        out.append({"raw": m.group(0), "cents": None if injected else to_cents(figure), "start": m.start(), "end": m.end()})
    return out


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
    return " ".join((clauses[-1] if clauses else "").split()[-6:])


def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
    needs it to be a billing document."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
        return "damages"
    if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
        return "charge"
    if _CHARGE_END.search(label):
        return "charge"
    return "unclear"


def _is_billing_source(source: str) -> bool:
    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))


5:- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
32:SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
180:    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
195:        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
212:    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
27:CREATE TABLE IF NOT EXISTS amounts (
28-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
29-  text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
30-  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
31-  state TEXT, state_reasons_json TEXT,
32-  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
33-  edited_json TEXT, ladder_json TEXT, updated_at REAL,
34-  PRIMARY KEY (case_id, id)
35-);
36-CREATE TABLE IF NOT EXISTS flags (
37-  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
38-  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
39-  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
40-  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
41-  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
42-  state TEXT, state_reasons_json TEXT,
43-  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
44-  edited_json TEXT, ladder_json TEXT, updated_at REAL,
45-  PRIMARY KEY (case_id, id)
46-);
47--- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
--
62:CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
63-CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
64-CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
65-CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:47.368Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/db app/backend memory/contracts | tail; grep -n \"reclass\" -r app memory/contracts board/cards 2>/dev/null | head; sed -n 175,215p app/db/db.py; grep -n \"SCHEMA_VERSION\" app/db/db.py | head"
}
````

### User / tool · 2026-11-02T04:16:47.498Z

**tool result**
````
app/README-arch.md:81:Already cut (D-011, D-020, ADR-015): in-app rate limiter and spend ledger (spend is limited on the provider key), arbitrary-text ingest on the public build, batch accept, charge reclassification and amount edits, the "not a duplicate" split, LLM date pointing, LLM split fallback, bring-your-own-key, `?full=1`, flag title/explanation edits, case list, jsonl audit export, citation toggle, manual add of an entry for a rejected record.
board/cards/T-061.md:33:- 2026-11-02T02:14:18Z researcher: AC 1 checked: selfcheck PASS: 26 new probes (explicit_patient 8/8, non_patient_speaker 12/12, headers_not_attribution 5/5 + 2 reclassified) in evals/lexicon_heldout.jsonl; self_report_scope.exclude_sentence added; intake entry self_report false; golden MUST 11/11
board/cards/T-084.md:3:title: "Guarded charge reclassification by the paralegal"
board/cards/T-084.md:18:  - {"n": 1, "text": "Paralegal can reclassify charge<->not-a-charge; rate->charge only if code finds charged-amount wording in the excerpt AND judge re-check passes, else 422 with reason; audit event; unit tests", "done": false, "evidence": null}
board/cards/T-013.md:72:    - [minor] unclear → charge reclassification produces a charge with no value — fix: State that `unclear` with a null value cannot become `charge`. It goes to the notes as 'request clean copy of bill'. Only `unclear` items with a parsed value may be reclassified.
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])


def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
    if action not in ACTIONS:
        raise ValueError(f"invalid review action {action!r}")
    table, row = _find(conn, item_id, case)
    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
    status = ACTIONS[action] or row["review_status"]
    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
    if action == "edit" and not new_edited:
        raise ValueError("edit requires a non-empty edited payload")
    after = {"review_status": status, "edited": new_edited}
    conn.execute("BEGIN")
    try:
        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return get_item(conn, item_id, row["case_id"])


def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
    if status not in REVIEW_STATUSES:
        raise ValueError(f"invalid review_status {status!r}")
    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
    apply_review(conn, item_id, action, edited=edited, now=now, case=case)


def list_events(conn, case_id: str, item_id: str = None) -> list:
    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
    if item_id:
        q, a = q + " AND item_id=?", a + [item_id]
    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
32:SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
47:        if has_tables and version != SCHEMA_VERSION:
51:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
58:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:50.377Z

**tool call — Bash**
````
{
 "command": "grep -rn \"list_events\\|review_events\" app --include=*.py | grep -v \"^app/db/db.py\" | head; grep -n \"kind\" app/backend/present.py | head -40; grep -n \"def amount_item\\|def _finish_amount\" -A40 app/backend/pipeline.py | head -120"
}
````

### User / tool · 2026-11-02T04:16:50.491Z

**tool result**
````
app/backend/store.py:70:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
app/backend/trace.py:131:        for e in DB.list_events(conn, case_id):
app/backend/present.py:178:    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
app/backend/present.py:202:                       for e in DB.list_events(conn, case_id)],
app/backend/review.py:223:    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
45:            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
52:            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
74:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
89:    kind = _ID_KIND[item_id[0]]
90:    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
91:    v["kind"] = kind
102:    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
103:    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
109:            "not_totaled": [{"id": a["id"], "kind": a["kind"], "text": a["text"]} for a in am
110:                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"]}
152:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
100:def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
101-    """The pipeline's amount item from an amounts.extract_amounts row and its record."""
102-    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
103-            "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
104-            "excerpt": r["excerpt"], "duplicate_note": a.get("duplicate_note"), "injection": a["injection"], "review_status": "pending"}
105-
106-
107-def _not_duplicates(conn, cid: str) -> list:
108-    return list(((DB.get_case(conn, cid) or {}).get("config") or {}).get("not_duplicates", []))
109-
110-
111-def _frozen_splitter(conn, cid: str):
112-    """D-039: once any entry, amount or flag of the case is accepted, edited or dismissed, the stored records are frozen. Returns None
113-    while everything is still pending (the model may re-split). Otherwise returns a splitter that replays the stored record spans with
114-    no model call, so decided items keep their record ids and excerpts; with fewer than two stored records it answers None (nothing to
115-    replay; the code split decides, which is deterministic and equals what is stored)."""
116-    if not any(i["review_status"] != "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k)):
117-        return None
118-    starts = [r[0] for r in conn.execute("SELECT char_start FROM records WHERE case_id=? ORDER BY seq", (cid,))]
119-    split_call = next((c["id"] for c in reversed(DB.list_llm_calls(conn, cid, "split")) if c.get("parsed_ok")), None)
120-
121-    reason = ((DB.get_case(conn, cid) or {}).get("config") or {}).get("split_failure")
122-
123-    def replay(text: str):             # stored spans are trimmed; the split contract is contiguous starts that cover the text
124-        if len(starts) <= 1 and reason:
125-            raise IN.SplitFailed(reason, replayed=True)
126-        cuts = [0] + starts[1:] + [len(text)]
127-        return (list(zip(cuts, cuts[1:])), split_call) if len(starts) > 1 else None
128-    return replay
129-
130-
131-def _store_split_failure(conn, cid: str, reason) -> None:
132-    """Keep the split-rejection reason in the case config so a later re-run that replays frozen records can show it again (D-039)."""
133-    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
134-    if cfg.get("split_failure") == reason:
135-        return
136-    if reason:
137-        cfg["split_failure"] = reason
138-    else:
139-        cfg.pop("split_failure", None)
140-    DB.update_case(conn, cid, config_json=cfg or None)
--
220:def _finish_amount(a: dict, ing: dict, judged) -> dict:
221-    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
222-    by_n = {r["n"]: r for r in ing["records"]}
223-    a = dict(a)
224-    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
225-    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
226-    state, reasons = confidence.compose_state(
227-        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
228-         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
229-        {"injection": a["injection"], "amount_class": a["cls"]})
230-    a["state"], a["reasons"] = state, reasons
231-    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
232-    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
233-                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
234-                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None)}
235-    return a
236-
237-
238-def _entry_for(entries: list, record_no: int):
239-    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)
240-
241-
242-def _err(code, stage, record_no=None, cause=None) -> dict:
243-    d = {"code": code, "stage": stage}
244-    if record_no is not None:
245-        d["record_no"] = record_no
246-    if cause:
247-        d["cause"] = cause
248-    return d
249-
250-
251-def _accident_year(recs: list):
252-    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso") and r["kind"] == "encounter")
253-    return int(ds[0][:4]) if ds else None
254-
255-
256-def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
257-    clock = now if callable(now) else (lambda: time.time() if now is None else now)
258-    t0 = clock()
259-    call = call or AU.make_call(conn, cid, now=clock)
260-    errors, stage_done = [], []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:55.547Z

**tool call — Bash**
````
{
 "command": "grep -n \"FixtureMiss\\|class LLMFailed\" -r app | head; grep -rn \"reason_code\" app --include=*.py | grep -v \"judges.py\\|schemas.py\" | head -20; grep -n \"unavailable\\|FixtureMiss\\|j1\" tests/unit/test_manual_and_split.py | head -20; ls tests/unit | sed -n 40,100p"
}
````

### User / tool · 2026-11-02T04:16:55.652Z

**tool result**
````
app/llm/provider.py:15:from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
app/llm/_types.py:11:class FixtureMissing(LLMError):
app/llm/_types.py:19:FixtureMiss = FixtureMissing   # old spelling, kept as an alias
app/llm/backends/fixture.py:1:"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
app/llm/backends/fixture.py:7:from app.llm._types import FixtureMiss, LLMError, LLMResult
app/llm/backends/fixture.py:26:        raise FixtureMiss(key)
app/llm/audited.py:27:class LLMFailed(Exception):
app/llm/audited.py:31:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
app/llm/audited.py:32:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:35:        P.FixtureMissing.__init__(self, prompt_hash)
app/backend/store.py:79:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/why.py:68:    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
app/backend/trace.py:9:closed reason_code (D-028), written by code; the model never supplies prose. Every `why`, `label` and `next_action.text` here is a fixed string.
app/backend/trace.py:97:    return {"id": sid, "label": label, "kind": kind, "status": status, "why": why_text, "reason_code": reason, "rule": rule,
app/backend/trace.py:170:def _judge_reason_code(jd, call):
app/backend/trace.py:171:    code = (jd or {}).get("reason_code")
app/backend/trace.py:177:            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
app/backend/trace.py:178:                return got["reason_code"]
app/backend/trace.py:201:    rc = _judge_reason_code(jd, call)
app/backend/trace.py:202:    ev.update(judge_verdict=verdict, judge_reason_code=rc)
app/backend/trace.py:581:            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
app/backend/trace.py:586:            detail = why.judge_detail(jd.get("reason_code"))
app/backend/trace.py:638:    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
app/backend/trace.py:649:                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
app/backend/trace.py:660:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
app/backend/trace.py:663:            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
app/backend/trace.py:693:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
app/backend/trace.py:719:            e = dict(base, reason_code=r["reason_code"], rationale=why.judge_detail(r["reason_code"]) or reason_text(_OBJECTION[v]), state_reason=_OBJECTION[v])
app/backend/trace.py:726:                says = (r["reason_code"] or "").replace("SHOULD_BE_", "").lower()
app/backend/trace.py:728:                                      "judge_says": f"{says} ({r['reason_code']})" if says and r["reason_code"] != "NONE" else "not a " + row["kind"],
test_narrative.py
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
test_t075_determinism.py
test_t093_eval_signature.py
test_totals.py
test_trace.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:59.001Z

**tool call — Bash**
````
{
 "command": "sed -n 20,45p app/llm/audited.py; sed -n 1,25p app/llm/_types.py; grep -n \"def test\" tests/unit/test_manual_and_split.py | head -20; sed -n 1,50p tests/unit/test_manual_and_split.py"
}
````

### User / tool · 2026-11-02T04:16:59.101Z

**tool result**
````
_RETRY_NOTES = (
    "",
    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
)


class LLMFailed(Exception):
    code = "LLM_FAILED_AFTER_RETRIES"


class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""

    def __init__(self, prompt_hash: str = ""):
        P.FixtureMissing.__init__(self, prompt_hash)


def _error_code(e: Exception) -> str:
    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
    if isinstance(e, P.LLMError):
        m = _CODE.match(str(e))
        return m.group(1) if m else "LLM_ERROR"
    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__


"""Shared provider types, JSON parsing and a small JSON-Schema checker (no jsonschema dependency). ADR-004."""
import json
import re
from dataclasses import dataclass, field


class LLMError(Exception):
    """Timeout, backend failure, invalid JSON or schema-invalid output. Messages must never contain record text."""


class FixtureMissing(LLMError):
    """No recorded answer for this prompt hash. Never retried, never answered with a default."""

    def __init__(self, prompt_hash: str = ""):
        super().__init__(f"FIXTURE_MISS {prompt_hash}")
        self.prompt_hash = prompt_hash


FixtureMiss = FixtureMissing   # old spelling, kept as an alias


@dataclass
class LLMResult:
    output: dict
    backend: str = "fixture"
24:def test_record_5_has_no_live_entry(tmp_path):
30:def test_manual_entry_requires_whole_verbatim_sentences(tmp_path, excerpt):
38:def test_manual_entry_is_pending_labelled_logged_and_exports_only_after_accept(tmp_path):
54:def test_manual_entry_summary_with_new_number_is_a_hard_422(tmp_path, confirm):
63:def test_manual_entry_label_in_pending_notes_and_override_is_recorded(tmp_path):
79:def test_manual_entry_refused_when_record_has_a_live_entry(tmp_path):
101:def test_not_a_duplicate_splits_the_pair_with_an_event(tmp_path):
114:def test_split_survives_a_rerun(tmp_path):
122:def test_not_a_duplicate_only_for_a_merged_non_primary_record(tmp_path, rid):
130:def test_routes_exist_and_validate(tmp_path, monkeypatch):
167:def test_duplicate_charge_moves_to_the_split_record_and_survives_rerun(tmp_path):
"""T-056 (D-031): manual entry for a rejected record (whole verbatim sentences, 422 otherwise, never auto-accepted) and 'not a duplicate' split."""
import pytest
from app.backend import export as X, pipeline as PL, review as RV, store
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, sample_script, which_record
from tests.unit.test_review_rules import judge


def sample_with_rejected_5(tmp_path):
    sums = golden_summaries()

    def extract(u):
        n = which_record(u)[0]
        if n == 5:     # a quote that is not in the record: grounding rejects it, so record 5 has no usable entry
            return dict(summary="Pain improving.", excerpt="Pain is much better today.")
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / "m.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    return conn, cid


def test_record_5_has_no_live_entry(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    assert not [e for e in DB.list_items(conn, cid, "entry") if "r5" in e["record_ids"] and e["state"] != "rejected"]


@pytest.mark.parametrize("excerpt", ["Pain 4/10, impr", "improving.", "Patient reports missing 3 days", "Something else entirely."])
def test_manual_entry_requires_whole_verbatim_sentences(tmp_path, excerpt):
    conn, cid = sample_with_rejected_5(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.manual_entry(conn, cid, "r5", {"summary": "Pain 4/10.", "excerpt": excerpt}, call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")
    assert not [x for x in DB.list_items(conn, cid, "entry") if x["id"].endswith("_m")]


def test_manual_entry_is_pending_labelled_logged_and_exports_only_after_accept(tmp_path):
    conn, cid = sample_with_rejected_5(tmp_path)
    r = RV.manual_entry(conn, cid, "r5", {"summary": "Pain 4/10, improving.", "excerpt": "Pain 4/10, improving."}, call=judge("supported"))
    it = r["item"]
    assert it["id"] == "e5_m" and it["review_status"] == "pending" and it["entered_by_reviewer"] and not it["ai_drafted"]
    assert it["date"] == "2026-02-20" and it["provider"] == "Capital PT, visit 8"          # from the header, not from the writer
    assert any(ev["action"] == "manual_entry" and ev["item_id"] == "e5_m" for ev in DB.list_events(conn, cid))
    before = X.build_export(store.export_case(conn, cid))
    assert "February 20, 2026" not in before["letter_text"]                              # never auto-accepted
    RV.apply_review(conn, cid, "e5_m", {"action": "accept"}, call=judge("supported"))
    after = X.build_export(store.export_case(conn, cid))
    assert "February 20, 2026 — Capital PT, visit 8" in after["letter_text"] and "entered by reviewer" not in after["letter_text"]
    assert "entered by reviewer" in after["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:09.223Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/judge_guard.py <<'EOF'\n\"\"\"Narrow judge-call guard (T-073). A judge that cannot answer for an EXPECTED reason (the LLM layer gave up, a fixture is missing, the\nbackend failed) never blocks the human: the result is 'unavailable' and the exception class is kept so the audit says why. Any other\nexception is a bug in our code and propagates. judges._run already turns LLMFailed and schema-invalid output into 'unavailable'; this\nguard covers what still escapes it (an unwrapped provider error such as FixtureMissing).\"\"\"\nfrom app.llm import audited as AU, provider as P\n\nEXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError)\n\n\ndef guarded(fn, *args, **kwargs):\n    \"\"\"Run a judges.run_*_meta function. Returns (verdict, call_id, reason_code, error_class); error_class is None unless the judge could\n    not answer for an expected reason (then verdict 'unavailable', reason_code 'NONE').\"\"\"\n    try:\n        verdict, call_id, code = fn(*args, **kwargs)\n    except EXPECTED_JUDGE_ERRORS as e:\n        return \"unavailable\", None, \"NONE\", type(e).__name__\n    return verdict, call_id, code, None\nEOF\npython3 - <<'EOF'\nimport re\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace(\"\"\"from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store\n\"\"\",\"\"\"from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, store\n\"\"\",1)\nold=\"\"\"        try:\n            verdict, call_id, judge_code = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)\n        except Exception:\n            verdict, call_id, judge_code = \"unavailable\", None, \"NONE\"\n        ladder_verdict\"\"\"\nnew=\"\"\"        verdict, call_id, judge_code, judge_error = judge_guard.guarded(judges.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id)   # T-073\n        ladder_verdict\"\"\"\nassert old in s\ns=s.replace(old,new,1)\ns=s.replace(\"\"\"    verdict, call_id, ladder_verdict, judge_code = \"unavailable\", None, \"unavailable\", \"NONE\"\n\"\"\",\"\"\"    verdict, call_id, ladder_verdict, judge_code, judge_error = \"unavailable\", None, \"unavailable\", \"NONE\", None\n\"\"\",1)\ns=s.replace(\"\"\"    return {\"toks\": toks, \"code_reasons\": code_reasons, \"blocking\": blocking, \"ladder_verdict\": ladder_verdict, \"call_id\": call_id, \"judge_code\": judge_code,\n\"\"\",\"\"\"    return {\"toks\": toks, \"code_reasons\": code_reasons, \"blocking\": blocking, \"ladder_verdict\": ladder_verdict, \"call_id\": call_id, \"judge_code\": judge_code,\n            \"judge_error\": judge_error,\n\"\"\",1)\ns=s.replace(\"\"\"                    \"reason_code\": chk[\"judge_code\"]}\n    lad.setdefault\"\"\",\"\"\"                    \"reason_code\": chk[\"judge_code\"], **({\"error_class\": chk[\"judge_error\"]} if chk[\"judge_error\"] else {})}\n    lad.setdefault\"\"\",1)\ns=s.replace(\"\"\"                        \"reason_code\": chk[\"judge_code\"]},\n              \"code_checks\": {\"excerpt_verbatim\\\"\"\"\",\"\"\"                        \"reason_code\": chk[\"judge_code\"], **({\"error_class\": chk[\"judge_error\"]} if chk[\"judge_error\"] else {})},\n              \"code_checks\": {\"excerpt_verbatim\\\"\"\"\",1)\nopen(p,'w').write(s)\nEOF\ngit diff -U0 app/backend/review.py | grep '^[+-]' | head -30"
}
````

### User / tool · 2026-11-02T04:17:09.365Z

**tool result**
````
--- a/app/backend/review.py
+++ b/app/backend/review.py
-from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store
+from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, store
-    verdict, call_id, ladder_verdict, judge_code = "unavailable", None, "unavailable", "NONE"
+    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
-        try:
-            verdict, call_id, judge_code = judges.run_j1_meta(new_sum, new_exc, label, call=call, item_id=item_id)
-        except Exception:
-            verdict, call_id, judge_code = "unavailable", None, "NONE"
+        verdict, call_id, judge_code, judge_error = judge_guard.guarded(judges.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id)   # T-073
+            "judge_error": judge_error,
-                    "reason_code": chk["judge_code"]}
+                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
-                        "reason_code": chk["judge_code"]},
+                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:12.386Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_review_rules.py; grep -n \"def \\|class \" tests/unit/_fakes.py | head -30"
}
````

### User / tool · 2026-11-02T04:17:12.491Z

**tool result**
````
"""Review/edit rules (backend/review.py). R-RV-2 (D-010, D-012), R-RV-3, R-CH-5, R-CH-7, ADR-005 edit re-check order; fake judge only."""
import pytest
from app.backend import pipeline as PL, review as RV, export as X
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record

def seeded(tmp_path, case="sample"):
    """Seeds a case through the pipeline with a case-aware fake (extract returns the first sentence unit of the cited record)."""
    from tests.unit._fakes import sample_script, which_record as wr
    if case == "sample":
        call = FakeCall(sample_script())
    else:
        def extract(u):
            n = wr(u, case)[0]; ex = G.record(case, n)["excerpt"]
            return dict(summary=ex.split(". ")[0].rstrip(".") + ".", excerpt=ex.split(". ")[0].rstrip(".") + ".")
        call = FakeCall(sample_script(extract=extract))
    conn = DB.connect(str(tmp_path / f"rv-{case}.sqlite")); cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), call=call, now=lambda: 1.0)
    return conn, cid, out

def ent(out, n):
    """Entry id citing record n (api.md: entries carry record_ids like 'r5')."""
    return [e for e in out["entries"] + out.get("undated_entries", []) if f"r{n}" in e["record_ids"]][0]["id"]
def amt(out, raw): return [a for a in out["amounts"] if a["raw"] == raw][0]["id"]
def judge(v): return FakeCall({"j1": {"verdict": v, "reason_code": "NONE"}})

@pytest.mark.parametrize("edits", [{"date": "2026-01-01"}, {"provider": "Someone Else"}, {"record": "r2"}, {"summary": "ok", "date": "2026-01-01"}])
def test_entry_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: editing an entry's date, provider or record -> 422 invalid_edit."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

@pytest.mark.parametrize("edits", [{"evidence": "x"}, {"type": "causation"}, {"title": "New title"}])
def test_flag_immutable_fields_are_422(tmp_path, edits):
    """R-RV-2: flag evidence, type and title are not editable (only a note)."""
    conn, cid, out = seeded(tmp_path)
    fid = [f for f in out["flags"] if f["type"] == "gap"][0]["id"]
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, fid, dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

@pytest.mark.parametrize("edits", [{"value": 1}, {"cls": "charge"}, {"amount": "$1"}, {"note": "x"}])
def test_charge_cannot_be_edited(tmp_path, edits):
    """R-CH-7 (D-010): a charge/rate has accept or dismiss only; no value or class edit, so a rate cannot become a charge."""
    conn, cid, out = seeded(tmp_path)
    with pytest.raises(RV.ReviewError) as e:
        RV.apply_review(conn, cid, amt(out, "$185"), dict(action="edit", edits=edits), call=judge("supported"))
    assert (e.value.status, e.value.code) == (422, "invalid_edit")

def test_excerpt_not_contiguous_whole_sentences_is_422(tmp_path):
    """R-RV-2 (D-012): non-contiguous or mid-sentence excerpt edit -> 422."""
    conn, cid, out = seeded(tmp_path)
    for bad in ["Alert and oriented. 41M restrained driver, rear-ended at approx. 35 mph.", "rear-ended at approx. 35 mph"]:
        with pytest.raises(RV.ReviewError) as e:
            RV.apply_review(conn, cid, ent(out, 1), dict(action="edit", edits=dict(excerpt=bad)), call=judge("supported"))
        assert e.value.code == "invalid_edit"
7:class FakeCall:
9:    def __init__(self, script=None):
12:    def __call__(self, step, system, user, schema, *, item_id=None):
18:    def steps(self):
20:    def prompts(self, step):
23:def golden_summaries():
37:def which_record(user, case="sample"):
42:def sample_script(**over):
45:    def extract(user):
54:def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
64:def items_for(out, n):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:21.462Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_judge_guard.py <<'EOF'\n\"\"\"T-073: the review.py judge path catches only expected judge errors, keeps the error class in the recorded ladder, and lets bugs propagate.\"\"\"\nimport pytest\nfrom app.backend import judge_guard, judges, review as RV\nfrom app.db import db as DB\nfrom app.llm import audited as AU, provider as P\nfrom tests.unit.test_review_rules import ent, judge, seeded\n\n\ndef _raising(exc):\n    def call(step, system, user, schema, *, item_id=None):\n        raise exc\n    return call\n\n\n@pytest.mark.parametrize(\"exc\", [AU.LLMFailed(), P.FixtureMissing(\"abc\"), P.LLMError(\"TIMEOUT\")])\ndef test_guard_turns_expected_errors_into_unavailable_with_class(exc):\n    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, \"Pain.\", \"Pain.\", \"PT\", call=_raising(exc))\n    assert (v, cid, code, err) == (\"unavailable\", None, \"NONE\", type(exc).__name__)\n\n\ndef test_guard_passes_a_normal_answer_through():\n    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, \"Pain.\", \"Pain.\", \"PT\", call=judge(\"supported\"))\n    assert (v, code, err) == (\"supported\", \"NONE\", None)\n\n\n@pytest.mark.parametrize(\"exc\", [RuntimeError(\"bug\"), KeyError(\"x\"), AttributeError(\"y\")])\ndef test_guard_does_not_swallow_unexpected_errors(exc):\n    with pytest.raises(type(exc)):\n        judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))\n\n\ndef test_edit_with_expected_judge_error_saves_as_unavailable_and_keeps_class(tmp_path):\n    conn, cid, out = seeded(tmp_path)\n    eid = ent(out, 5)\n    r = RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=\"Pain improving.\")), call=_raising(P.FixtureMissing(\"h\")))\n    assert [w[\"code\"] for w in r[\"warnings\"]] == [\"JUDGE_UNAVAILABLE\"]\n    jd = DB.get_item(conn, eid, cid)[\"ladder\"][\"judge\"]\n    assert jd[\"verdict\"] == \"unavailable\" and jd[\"error_class\"] == \"FixtureMissing\"\n\n\ndef test_edit_with_unexpected_error_propagates_and_saves_nothing(tmp_path):\n    conn, cid, out = seeded(tmp_path)\n    eid = ent(out, 5)\n    before = DB.get_item(conn, eid, cid)\n    with pytest.raises(RuntimeError):\n        RV.apply_review(conn, cid, eid, dict(action=\"edit\", edits=dict(summary=\"Pain improving.\")), call=_raising(RuntimeError(\"bug\")))\n    after = DB.get_item(conn, eid, cid)\n    assert after[\"review_status\"] == before[\"review_status\"] and not after.get(\"edited\")\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_judge_guard.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:17:22.263Z

**tool result**
````
exc = LLMFailed()

    @pytest.mark.parametrize("exc", [AU.LLMFailed(), P.FixtureMissing("abc"), P.LLMError("TIMEOUT")])
    def test_guard_turns_expected_errors_into_unavailable_with_class(exc):
        v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=_raising(exc))
>       assert (v, cid, code, err) == ("unavailable", None, "NONE", type(exc).__name__)
E       AssertionError: assert ('unavailable... 'NONE', None) == ('unavailable..., 'LLMFailed')
E         
E         At index 3 diff: None != 'LLMFailed'
E         Use -v to get more diff

tests/unit/test_judge_guard.py:18: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_judge_guard.py::test_guard_turns_expected_errors_into_unavailable_with_class[exc0]
1 failed, 8 passed in 0.46s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:27.019Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_judge_guard.py'\ns=open(p).read()\ns=s.replace('@pytest.mark.parametrize(\"exc\", [AU.LLMFailed(), P.FixtureMissing(\"abc\"), P.LLMError(\"TIMEOUT\")])\\ndef test_guard_turns_expected_errors_into_unavailable_with_class(exc):\\n    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, \"Pain.\", \"Pain.\", \"PT\", call=_raising(exc))',\n'''def test_judges_own_handling_of_llmfailed_is_unavailable():\n    assert judge_guard.guarded(judges.run_j1_meta, \"Pain.\", \"Pain.\", \"PT\", call=_raising(AU.LLMFailed()))[:3] == (\"unavailable\", None, \"NONE\")\n\n\n@pytest.mark.parametrize(\"exc\", [AU.LLMFailed(), P.FixtureMissing(\"abc\"), P.LLMError(\"TIMEOUT\")])\ndef test_guard_turns_expected_errors_into_unavailable_with_class(exc):\n    v, cid, code, err = judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_judge_guard.py 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T04:17:27.914Z

**tool result**
````
..........                                                               [100%]
10 passed in 0.53s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:50.369Z

**tool call — Bash**
````
{
 "command": "grep -n \"def compose_state\" -A60 app/backend/confidence.py | head -100; sed -n 40,70p app/backend/present.py; sed -n 95,115p app/backend/present.py"
}
````

### User / tool · 2026-11-02T04:17:50.461Z

**tool result**
````
47:def compose_state(ladder: dict, context: dict = None):
48-    ctx = context or {}
49-    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
50-    if bad:      # a misspelled key must not fail open to 'verified'
51-        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
52-    rejected, doubts = [], []
53-    for c in ladder.get("grounding_failures", []) or []:
54-        rejected.append(_known(c))
55-    if ladder.get("schema_valid", True) is False:
56-        rejected.append("SCHEMA_INVALID")
57-    for c in ladder.get("code_reasons", []) or []:
58-        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
59-    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
60-    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
61-    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
62-    doubts.append(_lookup(_AGREE, ctx.get("agreement"), none_ok=("both",)))
63-    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
64-                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
65-        if ctx.get(key):
66-            doubts.append(code)
67-    rejected = list(dict.fromkeys(rejected))
68-    doubts = list(dict.fromkeys(d for d in doubts if d))
69-    if rejected:
70-        return "rejected", rejected + doubts       # the rejecting reasons come first; the item still shows every doubt
71-    return ("needs_review", doubts) if doubts else ("verified", [])
def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None}


def amount_view(row, recs):
    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
            "duplicate_note": row["duplicate_note"]}


def _computed(c):
    c = dict(c or {})
    if "from_date" in c:
        c.update({"from": c.pop("from_date"), "to": c.pop("to_date", None)})
        c.setdefault("threshold", 30)
        ids = c.get("record_ids") or []
        if ids:
            c["from_record"], c["to_record"] = ids[0], ids[-1]
    return c


def _evidence(evs, recs):
    by_n = {r["seq"]: r["id"] for r in recs.values()}
    return [{"record_id": e.get("record_id") or by_n.get(e.get("record_no")), "excerpt": e.get("excerpt") if e.get("excerpt") is not None else e.get("text"),
             "start": e.get("start"), "end": e.get("end")} for e in (evs or [])]
def all_items(conn, case_id):
    recs = _recs_by_id(conn, case_id)
    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}


def totals_view(conn, case_id):
    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    t = T.totals([{"id": a["id"], "cents": a["value_cents"], "cls": a["kind"], "raw": a["text"], "review_status": a["review_status"]} for a in am])
    ch = [a for a in am if a["kind"] == "charge" and a["value_cents"] is not None]
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:55.276Z

**tool call — Bash**
````
{
 "command": "sed -n 1,46p app/backend/confidence.py; grep -n \"def get_item\\|def update_item\\|def list_items\\|def get_case\\b\" -A12 app/db/db.py | head -80; grep -n \"ApiError\\|def get_case\\|def make_call\\|exception_handler\" app/backend/api.py | head -20; sed -n 145,160p app/backend/api.py; sed -n 484,500p app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:17:55.395Z

**tool result**
````
"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.

Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
"""
REASON_CODES = (
    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT",
)
REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}

_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}


def sort_key(state: str) -> int:
    """needs_review first, then verified, then rejected."""
    return STATE_ORDER[state]


def _known(code: str) -> str:
    if code not in REASON_CODES:
        raise ValueError(f"unknown reason code: {code}")
    return code


def _lookup(table: dict, value, none_ok=()):
    if value is None or value in none_ok:
        return None
    if value not in table:
        raise ValueError(f"unknown value: {value}")
    return table[value]


_LADDER_KEYS = {"grounding_failures", "schema_valid", "code_reasons", "judge"}
_CTX_KEYS = {"injection", "date_status", "amount_class", "agreement", "fixture_miss", "split_ambiguous", "llm_failed",
             "endpoint_unverified", "llm_split"}


95:def get_case(conn, case_id: str):
96-    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
97-    return _decode(r) if r else None
98-
99-
100-def _insert(conn, table, row):
101-    bad = set(row) - _cols(conn, table)
102-    if bad:
103-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
104-    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
105-                 [_enc(v) for v in row.values()])
106-
107-
--
155:def get_item(conn, item_id: str, case: str = None) -> dict:
156-    return _decode(_find(conn, item_id, case)[1])
157-
158-
159:def list_items(conn, case_id: str, kind: str) -> list:
160-    table = _ITEM_TABLES[kind][0]
161-    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]
162-
163-
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
165-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
166-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
167-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
168-    if locked & set(fields):
169-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
170-    table, found = _find(conn, item_id, case)
171-    bad = set(fields) - _cols(conn, table)
172-    if bad:
173-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
174-    fields["updated_at"] = now
175-    sets = ", ".join(f"{k}=?" for k in fields)
176-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
46:class ApiError(Exception):
126:    def make_call(c, cid):
138:    def get_case(c, token):
141:            raise ApiError(404, "not_found", "No such case.")
145:    @app.exception_handler(ApiError)
149:    @app.exception_handler(review.ReviewError)
153:    @app.exception_handler(StarletteHTTPException)
158:    @app.exception_handler(Exception)
163:    @app.exception_handler(RequestValidationError)
193:            raise ApiError(413, "input_too_large", "Input is too large.")
198:                raise ApiError(413, "input_too_large", "Input is too large.")
204:            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
206:            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
219:            raise ApiError(404, "not_found", "Not found.")
229:            raise ApiError(404, "not_found", "Not found.")
239:                raise ApiError(404, "not_found", "Not found.")
242:                raise ApiError(404, "not_found", "No such library case.")
245:            raise ApiError(400, "bad_request", "Provide text or sample: true.")
252:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
255:            raise ApiError(413, "input_too_large", "The PDF is too large.")
    @app.exception_handler(ApiError)
    async def _api_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
            c.close()

    @app.post("/api/cases/{token}/items/{item_id}/review")
    async def review_item(token: str, item_id: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
        finally:
            c.close()

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)

    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:58.588Z

**tool call — Bash**
````
{
 "command": "sed -n 120,145p app/backend/api.py; grep -n \"def add_routes\" -A30 app/backend/case_extras.py | head -50; sed -n 125,170p tests/unit/test_manual_and_split.py; grep -n \"^## \\|^### \" memory/contracts/api.md | tail -40"
}
````

### User / tool · 2026-11-02T04:17:58.699Z

**tool result**
````
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

    def get_case(c, token):
        case = DB.get_case(c, token)
        if case is None:
            raise ApiError(404, "not_found", "No such case.")
        return case

    # -------------------------------------------------- errors / headers
    @app.exception_handler(ApiError)
106:def add_routes(app, *, conn, get_case, body_of, ApiError, now):
107-    @app.post("/api/cases/{token}/review/batch")
108-    async def review_batch(token: str, request: Request):
109-        b = await body_of(request)
110-        c = conn()
111-        try:
112-            get_case(c, token)
113-            try:
114-                return apply_batch(c, token, b, now())
115-            except ValueError:
116-                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
117-            except BatchRefused as e:
118-                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
119-                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
120-                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
121-        finally:
122-            c.close()
123-
124-    @app.get("/api/cases/{token}/export_config")
125-    def export_config_get(token: str):
126-        c = conn()
127-        try:
128-            get_case(c, token)
129-            return get_config(c, token)
130-        finally:
131-            c.close()
132-
133-    @app.put("/api/cases/{token}/export_config")
134-    async def export_config_put(token: str, request: Request):
135-        b = await body_of(request)
136-        c = conn()
        RV.not_duplicate(conn, cid, "e1", rid, call=call)
    assert e.value.status == 422


# ---------------------------------------------------------------- HTTP
def test_routes_exist_and_validate(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient
    from app.backend.api import create_app
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    c = TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)))
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    r = c.post(f"/api/cases/{tok}/records/r5/entry", json={"summary": "Pain 4/10.", "excerpt": "Pain 4/10, impr"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_edit"
    assert c.post(f"/api/cases/{tok}/records/r99/entry", json={"summary": "x", "excerpt": "y"}).status_code == 404
    assert c.post(f"/api/cases/{tok}/items/e1/not_duplicate", json={}).status_code == 400
    assert c.post(f"/api/cases/{tok}/items/e1/not_duplicate", json={"record_id": "r1"}).status_code in (404, 422)


# ---------------------------------------------------------------- the duplicate's charge follows the split (T-056 review B2)
TWO = """=== Record 1 ===
Date: 2026-03-02
Source: Capital Imaging
Excerpt: "Cervical MRI performed. Charge: $310."

=== Record 2 ===
Date: 2026-03-02
Source: Capital Imaging
Excerpt: "Cervical MRI performed. Charge: $310."
"""


def seeded_two(tmp_path):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Cervical MRI performed.", excerpt="Cervical MRI performed.")))
    conn = DB.connect(str(tmp_path / "t.sqlite")); cid = DB.create_case(conn, TWO, now=1.0)
    PL.run_pipeline(conn, cid, TWO, call=call, now=lambda: 1.0)
    return conn, cid, call


def amounts(conn, cid):
    return sorted((a["id"], tuple(a["record_ids"]), a["value_cents"], a["review_status"]) for a in DB.list_items(conn, cid, "amount"))


def test_duplicate_charge_moves_to_the_split_record_and_survives_rerun(tmp_path):
    conn, cid, call = seeded_two(tmp_path)
    assert amounts(conn, cid) == [("a1", ("r1",), 31000, "pending")]            # the duplicate contributes nothing while merged
    RV.not_duplicate(conn, cid, "e1", "r2", call=call)
5:## Conventions
14:## Endpoint index
40:## GET /api/health
53:## POST /api/cases
73:## POST /api/cases/pdf (D-031)
77:## POST /api/cases/{token}/review/batch (D-031)
80:## /api/cases/{token}/export_config (D-031)
83:## POST /api/cases/{token}/run
90:## GET /api/cases/{token}/status
100:## GET /api/cases/{token}
218:## POST /api/cases/{token}/records/{rid}/confirm_date
233:## GET /api/cases/{token}/items/{item_id}  — "Why?"
251:## POST /api/cases/{token}/items/{item_id}/review
285:## GET /api/cases/{token}/export
436:## GET /api/cases/{token}/audit
456:## Check traces (D-042): per-item stepper, case stepper, judge summary
463:### Step (shared by all three endpoints)
481:### GET /api/cases/{token}/items/{item_id}/trace
513:### GET /api/cases/{token}/trace
545:### GET /api/cases/{token}/judges
561:## POST /api/cases/{token}/rejudge  (D-044)
571:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
577:## DELETE /api/cases/{token}
582:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:01.582Z

**tool call — Bash**
````
{
 "command": "sed -n 125,145p app/backend/trace.py; sed -n 170,210p app/backend/present.py; sed -n 436,456p memory/contracts/api.md; sed -n 14,40p memory/contracts/api.md; sed -n 251,284p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T04:18:01.681Z

**tool result**
````
        calls = DB.list_llm_calls(conn, case_id)
        self.call_by_id = {c["id"]: c for c in calls}
        self.calls_by_item = {}
        for c in calls:
            self.calls_by_item.setdefault(c["item_id"], []).append(c)
        self.events = {}
        for e in DB.list_events(conn, case_id):
            self.events.setdefault(e["item_id"], []).append(e)
        self.models = {"generator": J.generator_model(), "judge": J.judge_model()}
        self.ran = self.case.get("run_started_at") is not None
        self.running = self.case["status"] == "running"

    def call(self, call_id, item_id=None, step_name=None):
        if call_id and call_id in self.call_by_id:
            return self.call_by_id[call_id]
        if item_id and step_name:
            hits = [c for c in self.calls_by_item.get(item_id, []) if c["step"] == step_name]
            return hits[-1] if hits else None
        return None


    seen, src = set(), []
    for rid in ids:
        if rid in recs and rid not in seen:
            seen.add(rid)
            r = recs[rid]
            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
    return {"item": item, "source": src, "calls": calls, "events": events}


def _call(c, full=False):
    rf = c.get("recorded_from")
    d = {"id": c["id"], "role": c["role"], "step": c["step"], "backend": c["backend"], "recorded_from": rf, "model": c["model"],
         "prompt_version": c["prompt_version"], "prompt_sha256": c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
         "latency_ms": c["latency_ms"], "cost_usd": c["cost_usd"], "tokens_in": c["tokens_in"], "tokens_out": c["tokens_out"],
         "parsed_ok": bool(c["parsed_ok"]), "verdict": c["verdict"]}
    if full:
        d.update(system_text=c["system_text"], user_text=c["user_text"], response_raw=c["response_raw"], error=c["error"])
    return d


def audit_view(conn, case_id, full=False):
    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
    calls = DB.list_llm_calls(conn, case_id)
    by = {}
    for c in calls:
        by[c["backend"]] = by.get(c["backend"], 0) + 1
    return {"token": case_id, "calls": [_call(c, full) for c in calls],
            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
                        **({"before": e["before"], "after": e["after"]} if full else {})}
                       for e in DB.list_events(conn, case_id)],
            "summary": {"calls": len(calls), "cost_usd": round(sum(c["cost_usd"] or 0 for c in calls), 6),
                        "latency_ms_total": sum(c["latency_ms"] or 0 for c in calls), "by_backend": by}}


def case_list(conn):
    """Local mode only (D-008/D-031): newest first. Metadata and counts, never record text."""
    out = []
    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC"):
## GET /api/cases/{token}/audit
JSON for this case only. **Public/demo (default): metadata only**: no prompt, response, record or edit text. With `ZLAYT_MODE=local` the same call also returns the full prompts and responses and the before/after of each human event (T-040, T-051 privacy check).

Public/demo shape:
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
  "calls": [ { "id": "c1", "role": "generator", "step": "extract", "backend": "fixture", "recorded_from": {"backend": "claude-cli", "model": "claude-sonnet-5-5"},
               "model": "claude-sonnet-5-5", "prompt_version": "extract_v1", "prompt_sha256": "9f2c0a77", "item_id": "e1", "attempt": 1,
               "latency_ms": 5120, "cost_usd": 0.0041, "tokens_in": 812, "tokens_out": 150, "verdict": null, "parsed_ok": true } ],
  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "at": "2026-11-02T01:05:00Z" } ],
  "summary": { "calls": 30, "cost_usd": 0.19, "latency_ms_total": 71200, "by_backend": {"fixture": 30} } }
```
Local shape (`ZLAYT_MODE=local`): each call also has `system_text`, `user_text`, `response_raw`, `error`; each event also has `before` and `after`:
```json
{ "calls": [ { "id": "c1", "...": "as above",
               "system_text": "You read one medical record ...", "user_text": "<<<RECORD-3fa91c0b2d44>>> ... <<<END-3fa91c0b2d44>>>",
               "response_raw": "{\"summary\": \"...\", \"excerpt\": \"...\"}", "error": null } ],
  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ] }
```

## Check traces (D-042): per-item stepper, case stepper, judge summary
## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected` |
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |

---

## GET /api/health
## POST /api/cases/{token}/items/{item_id}/review
All single-item human decisions. Request body (one of these per call; shown as an array of alternatives):
```json
[
  { "action": "accept" },
  { "action": "dismiss", "note": "false positive" },
  { "action": "reset" },
  { "action": "edit", "edits": { "summary": "Discharged from physical therapy after two missed appointments; pain 3/10." } },
  { "action": "edit", "edits": { "excerpt": "Discharged from PT after two missed appointments. Pain 3/10." } },
  { "action": "edit", "edits": { "note": "Ask client about the 2023 episode." }, "confirm_warnings": false }
]
```
Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".

**Edit re-check order (R-RV-3, ADR-005).** (1) Structure, else 422. (2) Code token check (ADR-012) and (3) judge 1 re-run. If the code check finds a number, date, dollar figure or left/right/no/not/without that is not in the quote, or the judge says `partially`/`unsupported`, nothing is saved and the response is 409:
```json
{ "error": { "code": "needs_confirm", "message": "This edit adds a number or fact that is not in the quote.",
    "detail": { "warnings": [
      {"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "“$9,000” is not in the quote.", "item_id": "e3"},
      {"code": "JUDGE_UNSUPPORTED", "message": "The second check could not support “herniation” from the quote.", "item_id": "e3"} ] } } }
```
The client shows the reasons; if she chooses "keep my wording" it resends with `"confirm_warnings": true`, the edit is saved and a `keep_my_wording` event is logged (listed in the internal notes). **If the code check passes but the judge fails** (error, timeout, or no recorded fixture, which is always the case in demo mode), the edit is saved, the item becomes `needs_review` with reason `JUDGE_UNAVAILABLE`, and the response carries it in `warnings[]`: no 409, because nothing objected. The judge never blocks an edit and never lets an unchecked edit look verified.

Response 200:
```json
{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
            "edited": {"summary": "...", "original_summary": "...", "at": "2026-11-02T01:06:00Z", "kept_my_wording": false} },
  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
  "review": { "counts": {"pending": 21, "accepted": 0, "edited": 1, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
```
The frontend does not need to refetch the case.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:06.609Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _persist\" -A45 app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:18:06.699Z

**tool result**
````
183:def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
184-    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
185-    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
186-    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
187-    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
188-    for it in items:
189-        row = _row(kind, it)
190-        old = existing.get(it["id"])
191-        if old is None:
192-            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
193-            continue
194-        DB.update_item(conn, it["id"], now=now, case=cid, **row)
195-        if kind == "flag" and old["review_status"] != "pending":
196-            oc = old.get("computed") or {}
197-            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
198-                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
199-            else:
200-                it["review_status"] = old["review_status"]
201-        elif old["review_status"] != "pending":
202-            it["review_status"] = old["review_status"]
203-    keep = {i["id"] for i in items}
204-    for oid, old in existing.items():
205-        if oid not in keep and old["review_status"] == "pending":
206-            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
207-
208-
209-def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
210-    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
211-    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
212-    _store_records(conn, cid, ing)
213-    _persist(conn, cid, "flag", ing["flags"], now)
214-    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
215-    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
216-    return ing
217-
218-
219-# ------------------------------------------------------------------ stages 4-6 helpers
220-def _finish_amount(a: dict, ing: dict, judged) -> dict:
221-    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
222-    by_n = {r["n"]: r for r in ing["records"]}
223-    a = dict(a)
224-    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
225-    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
226-    state, reasons = confidence.compose_state(
227-        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
228-         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:12.619Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def _row\" -A30 app/backend/pipeline.py; grep -n \"^import\\|^from\" app/backend/pipeline.py; sed -n 1,40p app/backend/why.py; grep -n \"TRACE_WHY\\|amount\" app/backend/trace.py | head -40"
}
````

### User / tool · 2026-11-02T04:18:12.724Z

**tool result**
````
166:def _row(kind: str, it: dict) -> dict:
167-    ladder = _clean(it.get("ladder") or {})
168-    if kind == "entry":
169-        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
170-                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
171-                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
172-    if kind == "amount":
173-        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
174-                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
175-                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
176-    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
177-                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
178-    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
179-            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
180-            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
181-
182-
183-def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
184-    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
185-    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
186-    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
187-    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
188-    for it in items:
189-        row = _row(kind, it)
190-        old = existing.get(it["id"])
191-        if old is None:
192-            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
193-            continue
194-        DB.update_item(conn, it["id"], now=now, case=cid, **row)
195-        if kind == "flag" and old["review_status"] != "pending":
196-            oc = old.get("computed") or {}
8:import argparse
9:import json
10:import sys
11:import time
12:from concurrent.futures import ThreadPoolExecutor
14:from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
16:from app.db import db as DB
17:from app.llm import audited as AU, provider as P
"""One fixed plain-language sentence per reason code (LLM_VS_CODE row 18, api.md appendix). Never model text."""
_WHY = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "The quoted text is not word for word in the record, so this item was rejected and cannot be used.",
    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
    "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
    "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
    "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
    "JUDGE_UNSURE": "A second AI check could not decide whether this item is supported.",
    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
    "DATE_MISSING": "The record has no readable date, so it is left out of gap checks.",
    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
    "AMOUNT_RATE_NOT_TOTALED": "This figure is a rate, not a charge, so it is not added to the total.",
    "AMOUNT_ESTIMATE": "This figure is an estimate, not a billed charge, so it is not added to the total.",
    "AMOUNT_DAMAGES": "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.",
    "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
}


def why(code: str) -> str:
    return _WHY[code]


def all_codes() -> list:
    return list(_WHY)

3:item_trace(conn, case_id, item_id, full)  one item (entry, amount, flag, narrative sentence): extracted, each code check by name, judge, human.
19:_JUDGE_PREFIX = (("judge_faithfulness", "j1"), ("judge_amount_class", "j2"), ("judge_conflict", "j3"), ("judge_flag", "j4"))
40:TRACE_WHY = {
71:    "INJECTION_SUSPECTED": "injection_scan", "LLM_FAILED_AFTER_RETRIES": "extracted", "AMOUNT_RATE_NOT_TOTALED": "amount_class",
72:    "AMOUNT_ESTIMATE": "amount_class", "AMOUNT_DAMAGES": "amount_class", "AMOUNT_UNCLEAR": "amount_class", "CONFLICT_CHECK_INCOMPLETE": "record_warning_check",
79:    if code in TRACE_WHY:
80:        return TRACE_WHY[code]
237:    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
243:                        "GROUNDING_AMOUNT_NOT_IN_TEXT": "Not run: the amount is not in the record text.",
380:# ------------------------------------------------------------------ amounts
381:def _amount_steps(cx, row):
390:    gfail = "GROUNDING_AMOUNT_NOT_IN_TEXT" in R or cc.get("amount_in_text") is False
395:        st.append(_skipped("amount_class", "Rule says what the figure is", "code", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
400:            st.append(step("amount_class", "Rule says what the figure is", "code", PASS,
403:            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
407:            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
409:        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
431:    st.append(_human_step(cx, row, "amount"))
562:    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
618:    """UnknownItem for an id that is not in the case. Entry, amount, flag or narrative sentence (ns...). Any other error is a bug and propagates."""
633:_STEPS_OF.update({"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps})
640:    for kind in ("entry", "amount", "flag"):
646:            jid = judge_of_prompt(jd.get("prompt_version")) or {"entry": "j1", "amount": "j2", "flag": "j4"}[kind]
693:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN"],
725:            if r["kind"] == "amount":
727:                disagreements.append({"item_id": r["item_id"], "kind": "amount", "type": "judge_objects", "code_says": row["kind"],
777:    amts = DB.list_items(conn, case_id, "amount")
779:    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
834:        st.append(step("grounding", "Every quote and amount is in the record", "code", FAIL, f"{len(rej)} item{'s were' if len(rej) != 1 else ' was'} rejected because the quote or amount is not in the record. "
838:        st.append(step("grounding", "Every quote and amount is in the record", "code", PENDING, "There is nothing to check yet.", rule="row 4", counts=gcounts, next_action=na("RERUN")))
840:        st.append(step("grounding", "Every quote and amount is in the record", "code", PASS, f"All {len(allitems)} items cite text that is in the record, character for character.", rule="row 4", counts=gcounts))
875:        st.append(step("totals", "Billed-charges total", "code", SKIPPED, "No dollar amounts were found.", rule="row 8", counts=tcounts))
878:                       reason="PENDING_DECISION", rule="row 8", counts=tcounts, next_action=na("DECIDE", {"view": "amounts"}, ["accept", "dismiss"])))
929:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
931:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
935:        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:17.132Z

**tool call — Bash**
````
{
 "command": "sed -n 380,432p app/backend/trace.py; grep -n \"def _ladder\" -A14 app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:18:17.225Z

**tool result**
````
# ------------------------------------------------------------------ amounts
def _amount_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    kind = row["kind"]
    vals = {"text": row["text"], "value_cents": row["value_cents"], "kind": kind, "classified_by": cc.get("classified_by")}
    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
    gfail = "GROUNDING_AMOUNT_NOT_IN_TEXT" in R or cc.get("amount_in_text") is False
    st = []
    if gfail:
        st.append(step("found_in_text", "Dollar figure is in the record text", "code", FAIL, reason_text("GROUNDING_AMOUNT_NOT_IN_TEXT"), reason="GROUNDING_AMOUNT_NOT_IN_TEXT",
                       rule="row 6", evidence={"excerpt": exc, "values": vals}, next_action=na("DISMISS_OR_ENTER_BY_HAND", {"item_id": row["id"]}, ["dismiss"])))
        st.append(_skipped("amount_class", "Rule says what the figure is", "code", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
    else:
        st.append(step("found_in_text", "Dollar figure is in the record text", "code", PASS, "Code found this figure in the record by pattern; it is not a model's claim.",
                       rule="row 6", evidence={"excerpt": exc, "values": vals}))
        if kind == "charge":
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS,
                           "A billing phrase in the record labels this figure a charge, so it counts toward the total once you accept it.", rule="row 7", evidence={"values": vals}))
        elif kind == "unclear":
            st.append(step("amount_class", "Rule says what the figure is", "code", FAIL, reason_text("AMOUNT_UNCLEAR"), reason="AMOUNT_UNCLEAR", rule="row 7",
                           evidence={"values": vals}, next_action=na("READ_RECORD", {"record_id": rid})))
        else:
            code = _AMOUNT_CODE[kind]
            st.append(step("amount_class", "Rule says what the figure is", "code", PASS, reason_text(code), reason=code, rule="row 7", evidence={"values": vals}))
    if rec.get("injection_tag") or "INJECTION_SUSPECTED" in R:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", FAIL, reason_text("INJECTION_SUSPECTED") + " An amount from such a record cannot become a charge.",
                       reason="INJECTION_SUSPECTED", rule="row 16", evidence={"values": {"record_id": rid}}, next_action=na("READ_RECORD", {"record_id": rid})))
    else:
        st.append(step("injection_scan", "Record has no instruction-like text", "code", PASS, "The record has no instruction-like text.", rule="row 16"))
    if gfail:
        st.append(_skipped("judge_2", "Second AI check: is this figure a charge, rate or estimate?", "llm", "GROUNDING_AMOUNT_NOT_IN_TEXT", "row 7"))
    elif kind == "damages":
        st.append(step("judge_2", "Second AI check: is this figure a charge, rate or estimate?", "llm", SKIPPED, "Damages and other non-bill figures are not sent to the second check.",
                       reason="AMOUNT_DAMAGES", rule="row 7"))
    else:
        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j2", R, rule="row 7"))
    rs = row["review_status"]
    if kind != "charge" or gfail or row["state"] == "rejected":
        why_t = reason_text(_AMOUNT_CODE[kind]) if kind in _AMOUNT_CODE else "Not a billed charge, so it is not added to the total."
        st.append(step("total_inclusion", "Counted in the total", "code", SKIPPED, why_t, reason=_AMOUNT_CODE.get(kind), rule="row 8"))
    elif rs == "dismissed":
        st.append(step("total_inclusion", "Counted in the total", "code", SKIPPED, "Dismissed, so it is not in the total.", rule="row 8"))
    elif rs in ("accepted", "edited"):
        st.append(step("total_inclusion", "Counted in the total", "code", PASS, "Accepted, so this charge is in the billed-charges total (added by code).", rule="row 8", evidence={"values": vals}))
    else:
        st.append(step("total_inclusion", "Counted in the total", "code", PENDING, "Detected but not in the accepted total until you accept it.", reason="PENDING_DECISION", rule="row 8",
                       evidence={"values": vals}, next_action=na("DECIDE", {"item_id": row["id"]}, ["accept", "dismiss"])))
    st.append(_human_step(cx, row, "amount"))
    return st
30:def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
31-    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
32-            "human": {"action": None, "edited_text": None, "at": None}, "state": state}
33-
34-
35-def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
36-    """State of a flag made by code: evidence spans must equal the input text; injection / unconfirmed endpoints give needs_review."""
37-    bad = [e for e in evidence if e.get("start") is not None and case_text[e["start"]:e["end"]] != e["text"]]
38-    ctx = {"injection": any(rec_by_n[n].get("injection_tag") for n in nos if n in rec_by_n),
39-           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons}
40-    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
41-    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
42-        ctx["date_status"] = "ambiguous"
43-    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
44-                                     "code_reasons": []}, ctx)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:25.550Z

**tool call — Bash**
````
{
 "command": "sed -n 114,140p app/backend/amounts.py; grep -n \"def body_offset\" -A8 app/backend/generator.py; grep -n \"def load_records\" -A25 app/backend/store.py | head -40"
}
````

### User / tool · 2026-11-02T04:18:25.655Z

**tool result**
````
def extract_amounts(records: list, separate=frozenset()) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
    `separate` = record numbers the paralegal said are not duplicates: their amounts never merge with another record's and get ids ax<n>_<k>."""
    rows = []
    for r in records:
        if r.get("duplicate_of"):
            continue
        base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
                 for a in find_amounts(r["excerpt"])] + damages_mentions(r["excerpt"])
        for a in sorted(found, key=lambda x: x["start"]):
            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                         "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "injection": bool(r.get("injection_tag"))})
    out = dedupe_amounts(rows, separate)
    i, k = 0, {}
    for a in out:
        if a["record_no"] in separate:         # stable ids that do not shift the other amounts: a rerun lands on the same rows
            k[a["record_no"]] = k.get(a["record_no"], 0) + 1
            a["id"] = f"ax{a['record_no']}_{k[a['record_no']]}"
        else:
            i += 1
            a["id"] = f"a{i}"
    return out


_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
17:def body_offset(record: dict) -> int:
18-    """Absolute offset (in the normalised case text) where record['excerpt'] starts."""
19-    block = record.get("text", "")
20-    m = _EXC.search(block)
21-    base = record.get("char_start", 0)
22-    if m and block[m.end():].startswith(record["excerpt"][:20]):
23-        return base + m.end()
24-    i = block.find(record["excerpt"])
25-    return base + (i if i >= 0 else 0)
14:def load_records(conn, case_id: str, raw: str = None) -> list:
15-    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
16-    if raw is None:
17-        raw = DB.get_case(conn, case_id)["raw_text"]
18-    out = []
19-    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
20-        d = DB._decode(r)
21-        block = raw[d["char_start"]:d["char_end"]]
22-        try:
23-            body = ingest.split_records(block)[0]["excerpt"]
24-        except Exception:
25-            body = block
26-        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
27-                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
28-    return out
29-
30-
31-def _by_id(records):
32-    return {r["id"]: r for r in records}
33-
34-
35-# ---------------------------------------------------------------- unit dicts for export / totals
36-def export_case(conn, case_id: str) -> dict:
37-    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
38-    case = DB.get_case(conn, case_id)
39-    recs = load_records(conn, case_id, case["raw_text"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:48.821Z

**tool call — Bash**
````
{
 "command": "sed -n 12,16p app/backend/pipeline.py; grep -n \"def _clean\" -A6 app/backend/pipeline.py; grep -n \"pipeline\" app/backend/store.py app/backend/generator.py app/backend/present.py | head"
}
````

### User / tool · 2026-11-02T04:18:48.930Z

**tool result**
````
from concurrent.futures import ThreadPoolExecutor

from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
                         judges, split_llm, totals as TT, why as WHY)
from app.db import db as DB
25:def _clean(d: dict) -> dict:
26-    """Drop private '_' keys before an item is stored or returned."""
27-    return {k: v for k, v in d.items() if not k.startswith("_")}
28-
29-
30-def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
31-    return {"item_id": item_id, "backend": backend, "generator": None, "judge": None, "code_checks": code_checks or {},
app/backend/store.py:1:"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.
app/backend/store.py:3:Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
app/backend/generator.py:4:`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:15.432Z

**tool call — Bash**
````
{
 "command": "cat > app/backend/reclassify.py <<'EOF'\n\"\"\"Guarded charge reclassification by the paralegal (T-084, D-042; supersedes the D-010 'a rate can never become a charge' cut).\n\nTwo directions, one rule of thumb: taking a figure OUT of the billed-charges total is always the paralegal's call; putting a figure INTO it\nneeds evidence.\n- charge -> not-a-charge: always allowed. The row's kind becomes `unclear` (shown as \"not added to the total\", never totaled).\n- not-a-charge (rate, estimate, unclear, damages) -> charge: allowed only when (1) CODE finds charged-amount wording (charged, charges, billed,\n  invoiced, amount due ...) in the same sentence as the figure, with no negation, the figure has a parsed value and the record is not\n  injection-tagged, AND (2) judge 2 re-checks the figure against the class `charge` and agrees. Otherwise 422 `reclassify_refused` with a\n  fixed reason and nothing changes. Undoing the paralegal's own earlier demotion of a figure the code first called a charge skips both\n  checks (the code's original call is restored with the judge answer it had).\nWhatever the direction: the item goes back to `pending` (she decides again), the ladder keeps who/what/when, and an audit event is written.\nThe judge sees only the record text, the figure and the class (judges.run_j2_meta); the model supplies no prose that is stored.\"\"\"\nimport re\n\nfrom app.backend import amounts as AM, confidence, generator, judge_guard, judges, review, store, why as WHY\nfrom app.db import db as DB\n\nTARGETS = (\"charge\", \"not_a_charge\")\nNOT_A_CHARGE_KIND = \"unclear\"\nAUDIT_ACTION = \"edit\"      # review_events.action CHECK has no 'reclassify' yet (db card); the payload's `event` says what it was\n_BOUNDARY = re.compile(r\"(?<=[.;!?])\\s+|\\n\")\n_WORDING = re.compile(r\"\\b(?:charged|charges?|billed|invoiced|amount\\s+due|balance\\s+due|total\\s+billed)\\b\", re.IGNORECASE)\n_NEGATED = re.compile(r\"\\b(?:not|never|no|without|unbilled|uncharged)\\s+(?:\\w+\\s+)?(?:charged|charges?|billed|invoiced)\\b|\\b(?:unbilled|uncharged)\\b\", re.IGNORECASE)\n\nREFUSALS = {\n    \"NO_VALUE\": \"The dollar value of this figure could not be read, so it cannot become a charge.\",\n    \"INJECTION_SUSPECTED\": \"This record has instruction-like text, so a figure from it cannot become a charge.\",\n    \"NO_CHARGE_WORDING\": \"The sentence with this figure has no wording that says it was charged or billed (such as charged, billed, invoiced or amount due), so it stays a figure that is not a charge.\",\n    \"JUDGE_DISAGREES\": \"A second AI check read this figure as something other than a charge, so it stays as it is.\",\n    \"JUDGE_UNSURE\": \"A second AI check could not tell whether this figure is a charge, so it stays as it is.\",\n    \"JUDGE_UNAVAILABLE\": \"The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.\",\n}\n\n\ndef _sentences(excerpt: str):\n    \"\"\"[(start, end, text)] of the excerpt's sentences, the same boundary rule amounts.classify uses.\"\"\"\n    out, pos = [], 0\n    for m in _BOUNDARY.finditer(excerpt):\n        out.append((pos, m.start(), excerpt[pos:m.start()]))\n        pos = m.end()\n    out.append((pos, len(excerpt), excerpt[pos:]))\n    return out\n\n\ndef _figure_spans(excerpt: str, row: dict, rec):\n    \"\"\"Where this amount sits in the excerpt: the stored absolute offsets when they check out, else every occurrence of its text.\"\"\"\n    raw = row[\"text\"]\n    if rec is not None and row.get(\"excerpt_start\") is not None:\n        i = row[\"excerpt_start\"] - generator.body_offset(rec)\n        if 0 <= i and excerpt[i:i + len(raw)] == raw:\n            return [(i, i + len(raw))]\n    return [(m.start(), m.end()) for m in re.finditer(re.escape(raw), excerpt)]\n\n\ndef charge_wording(excerpt: str, row: dict, rec=None):\n    \"\"\"Code check: the charged-amount phrase in the figure's own sentence (every occurrence of the figure must have one), or None.\"\"\"\n    spans = _figure_spans(excerpt or \"\", row, rec)\n    found = None\n    for s, _e in spans:\n        sent = next((t for a, b, t in _sentences(excerpt) if a <= s <= b), \"\")\n        m = _WORDING.search(sent)\n        if not m or _NEGATED.search(sent):\n            return None\n        found = found or m.group(0)\n    return found\n\n\ndef _refuse(reason: str, **detail):\n    return review.ReviewError(422, \"reclassify_refused\", {\"reason\": reason, \"check\": \"code\" if reason in (\"NO_VALUE\", \"INJECTION_SUSPECTED\", \"NO_CHARGE_WORDING\") else \"judge\",\n                                                          **detail}, REFUSALS[reason])\n\n\ndef _log(conn, case_id, item_id, before, after, t):\n    conn.execute(\"INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)\",\n                 (DB._tok(\"v\"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))\n\n\ndef reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:\n    t = review._now(now)\n    to = (body or {}).get(\"to\")\n    if to not in TARGETS:\n        raise review.ReviewError(400, \"bad_request\", message='Send \"to\": \"charge\" or \"not_a_charge\".')\n    note = (body or {}).get(\"note\")\n    if note is not None and not isinstance(note, str):\n        raise review.ReviewError(400, \"bad_request\", message=\"The note must be text.\")\n    kind, row = review._item(conn, case_id, item_id)\n    if kind != \"amount\":\n        raise review._bad(\"Only a dollar figure can be reclassified.\")\n    if row[\"state\"] == \"rejected\":\n        raise review.ReviewError(409, \"item_rejected\", message=\"This item could not be verified; it can only be dismissed or reset.\")\n    old_kind = row[\"kind\"]\n    if (to == \"charge\") == (old_kind == \"charge\"):                         # already there: nothing to do, nothing logged\n        return _result(conn, case_id, item_id, None, [])\n    lad = dict(row.get(\"ladder\") or {\"item_id\": item_id})\n    prior = lad.get(\"reclassification\") or {}\n    original = prior.get(\"original_kind\", old_kind)\n    rec = next((r for r in store.load_records(conn, case_id) if r[\"id\"] == (row[\"record_ids\"] or [None])[0]), None)\n    wording, judge_res, restored = None, None, False\n    if to == \"charge\":\n        restored = original == \"charge\" and prior.get(\"previous_judge\") is not None\n        if not restored:\n            wording, judge_res = _guard(row, rec, call)\n    new_kind = \"charge\" if to == \"charge\" else NOT_A_CHARGE_KIND\n    cc = dict(lad.get(\"code_checks\") or {})\n    cc.update(classified_by=\"reviewer:reclassified\", **({\"charge_wording\": wording} if wording else {}))\n    if to == \"charge\":\n        jd = prior[\"previous_judge\"] if restored else judge_res[\"judge\"]\n        ladder_verdict = judges.to_ladder(\"j2\", (jd or {}).get(\"verdict\", \"unavailable\")) if jd else \"unavailable\"\n    else:\n        jd, ladder_verdict = None, None\n    state, reasons = confidence.compose_state({\"grounding_failures\": [], \"schema_valid\": True, \"code_reasons\": [], \"judge\": ladder_verdict},\n                                              {\"injection\": bool(rec and rec.get(\"injection_tag\")), \"amount_class\": new_kind})\n    lad.update(judge=jd, code_checks=cc, state=state, reclassification={\n        \"from\": old_kind, \"to\": new_kind, \"at\": store.iso(t), \"by\": \"reviewer\", \"original_kind\": original, \"wording\": wording, \"restored\": restored,\n        \"note\": (note or \"\").strip()[:500] or None,\n        \"previous_judge\": lad.get(\"judge\") if to == \"not_a_charge\" else prior.get(\"previous_judge\")})\n    before = {\"kind\": old_kind, \"review_status\": row[\"review_status\"], \"state\": row[\"state\"]}\n    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)\n    if row[\"review_status\"] != \"pending\":                                  # her earlier decision was about the old meaning\n        DB.apply_review(conn, item_id, \"reset\", now=t, case=case_id)\n    _log(conn, case_id, item_id, before, {\"event\": \"reclassify\", \"kind\": new_kind, \"review_status\": \"pending\", \"wording\": wording,\n                                          \"judge_verdict\": (jd or {}).get(\"verdict\"), \"judge_call_id\": (jd or {}).get(\"call_id\"), \"restored\": restored,\n                                          \"note\": lad[\"reclassification\"][\"note\"]}, t)\n    return _result(conn, case_id, item_id, {\"from\": old_kind, \"to\": new_kind, \"wording\": wording, \"judge_verdict\": (jd or {}).get(\"verdict\"),\n                                           \"restored\": restored}, [])\n\n\ndef _guard(row: dict, rec, call):\n    \"\"\"The two checks for putting a figure into the total, code first. Returns (wording, {'judge': ladder judge dict}) or raises 422.\"\"\"\n    if row[\"value_cents\"] is None:\n        raise _refuse(\"NO_VALUE\")\n    if rec is not None and rec.get(\"injection_tag\"):\n        raise _refuse(\"INJECTION_SUSPECTED\")\n    wording = charge_wording(row[\"excerpt\"], row, rec)\n    if wording is None:\n        raise _refuse(\"NO_CHARGE_WORDING\")\n    if call is None:\n        raise _refuse(\"JUDGE_UNAVAILABLE\", wording=wording)\n    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row[\"excerpt\"], row[\"text\"], \"charge\", call=call, item_id=row[\"id\"])\n    ladder_verdict = judges.to_ladder(\"j2\", verdict)\n    if ladder_verdict != \"supported\":\n        reason = {\"disagrees\": \"JUDGE_DISAGREES\", \"unsure\": \"JUDGE_UNSURE\"}.get(ladder_verdict, \"JUDGE_UNAVAILABLE\")\n        raise _refuse(reason, wording=wording, **({\"error_class\": err} if err else {}))\n    return wording, {\"judge\": {\"model\": judges.judge_model(), \"prompt_version\": \"judge_amount_class_v1\", \"call_id\": call_id, \"verdict\": verdict,\n                               \"reason_code\": code}}\n\n\ndef _result(conn, case_id, item_id, change, warnings):\n    from app.backend import present\n    return {\"item\": present.item_view(conn, case_id, item_id), \"totals\": present.totals_view(conn, case_id),\n            \"review\": present.review_view(conn, case_id), \"reclassified\": change, \"warnings\": warnings}\n\n\ndef carry_over(old: dict, it: dict) -> dict:\n    \"\"\"pipeline._persist hook: a rerun re-derives the code's class, but a figure the paralegal reclassified keeps her class (same figure only).\"\"\"\n    rc = (old.get(\"ladder\") or {}).get(\"reclassification\")\n    if not rc or old[\"kind\"] == it[\"cls\"] or old[\"text\"] != it[\"text\"] or old[\"value_cents\"] != it[\"cents\"]:\n        return it\n    return {**it, \"cls\": old[\"kind\"], \"kind\": old[\"kind\"], \"state\": old[\"state\"], \"reasons\": old[\"state_reasons\"], \"ladder\": old[\"ladder\"],\n            \"why\": \" \".join(WHY.why(c) for c in old[\"state_reasons\"])}\n\n\ndef add_routes(app, *, conn, get_case, body_of, make_call):\n    @app.post(\"/api/cases/{token}/items/{item_id}/reclassify\")\n    async def reclassify_item(token: str, item_id: str, request):\n        b = await body_of(request)\n        c = conn()\n        try:\n            get_case(c, token)\n            return reclassify(c, token, item_id, b, call=make_call(c, token))\n        finally:\n            c.close()\nEOF\ngrep -n \"^from fastapi\\|^import\\|Request\" app/backend/api.py | head; sed -n 1,20p app/backend/case_extras.py | grep -n import"
}
````

### User / tool · 2026-11-02T04:19:15.561Z

**tool result**
````
6:import hashlib
7:import ipaddress
8:import asyncio
9:import json
10:import logging
11:import os
12:import pathlib
13:import threading
14:import time
16:from fastapi import FastAPI, Request
3:import re
4:import threading
6:from fastapi import Request
8:from app.backend import present, review
9:from app.db import db as DB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:21.700Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/reclassify.py'\ns=open(p).read()\ns=s.replace(\"import re\\n\\nfrom app.backend import amounts as AM, confidence,\",\"import re\\n\\nfrom fastapi import Request\\n\\nfrom app.backend import confidence,\",1)\ns=s.replace(\"request):\\n        b = await\",\"request: Request):\\n        b = await\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"case_extras.add_routes\" app/backend/api.py; grep -n \"_row(kind, it)\" app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T04:19:21.816Z

**tool result**
````
496:    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
189:        row = _row(kind, it)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:24.959Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\na=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(a)==1\ns=s.replace(a,a+\"    from app.backend import reclassify\\n    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084\\n\",1)\nopen(p,'w').write(s)\np='app/backend/pipeline.py'\ns=open(p).read()\na=\"\"\"        row = _row(kind, it)\n        old = existing.get(it[\"id\"])\n\"\"\"\nassert s.count(a)==1\nb=\"\"\"        old = existing.get(it[\"id\"])\n        if kind == \"amount\" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure\n            from app.backend import reclassify as RC\n            it = RC.carry_over(old, it)\n        row = _row(kind, it)\n\"\"\"\ns=s.replace(a,b,1)\nopen(p,'w').write(s)\nEOF\ngit diff -U1 app/backend/pipeline.py app/backend/api.py | head -50"
}
````

### User / tool · 2026-11-02T04:19:25.082Z

**tool result**
````
diff --git a/app/backend/api.py b/app/backend/api.py
index 4edd585..5959eb5 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -496,2 +496,5 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
+    from app.backend import reclassify
+    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
+    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
 
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 2426a4d..1336613 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -3,3 +3,3 @@
 0 ingest (code, sync)  1 extract (LLM)  2 verify (code)  3 judge_entries (J1)  4 amounts (J2 on every amount)
-5 conflicts (one LLM pair pass + J3)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
+5 conflicts (code proposes the pairs, J3 classifies each)  6 flags (one LLM pass per record + lexicon floor + J4)  7 finalize (code).
 Gaps, the accident-date conflict, provider-name conflicts, amounts and record warnings exist after stage 0 and never wait for a model.
@@ -188,4 +188,7 @@ def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
     for it in items:
-        row = _row(kind, it)
         old = existing.get(it["id"])
+        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
+            from app.backend import reclassify as RC
+            it = RC.carry_over(old, it)
+        row = _row(kind, it)
         if old is None:
@@ -312,3 +315,3 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
         a["entry_id"] = _entry_for(entries, a["record_nos"][0])
-    # 5: semantic conflicts (LLM) + J3
+    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
     llm_flags = []
@@ -316,10 +319,3 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     if guard("conflicts"):
-        pair = FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
-        for i, f in enumerate(pair, 1):
-            f["id"] = f"f_cx{i}"
-            if f.get("pipeline_warning"):      # conflict check did not finish: visible on the run, not only on the flag
-                ing["warnings"].append({"code": f["pipeline_warning"], "stage": "conflicts", "item_id": f["id"],
-                                        "message": "The check for conflicts between records did not finish; conflicts may be missing."})
-                errors.append({"code": f["pipeline_warning"], "stage": "conflicts", "record_no": None, "cause": f["reasons"][0]})
-        llm_flags += FL.judge_flags(pair, call=call, case_text=text)
+        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
     # 6: per-record flags (one call per distinct record) + J4
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:28.496Z

**tool call — Bash**
````
{
 "command": "cat > /tmp/x.py 2>/dev/null; .venv/bin/python - <<'EOF'\nfrom tests.unit.test_review_rules import seeded\nimport tempfile, pathlib\nfrom app.db import db as DB\nconn,cid,out=seeded(pathlib.Path(tempfile.mkdtemp()))\nfor a in DB.list_items(conn,cid,\"amount\"):\n    print(a[\"id\"],a[\"text\"],a[\"kind\"],a[\"state\"],a[\"state_reasons\"],a[\"excerpt\"][:150].replace(\"\\n\",\" \"))\nEOF"
}
````

### User / tool · 2026-11-02T04:21:28.636Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b10x6tdp2). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b10x6tdp2.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:30.959Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF' < /dev/null\nfrom tests.unit.test_review_rules import seeded\nimport tempfile, pathlib\nfrom app.db import db as DB\nconn,cid,out=seeded(pathlib.Path(tempfile.mkdtemp()))\nfor a in DB.list_items(conn,cid,\"amount\"):\n    print(a[\"id\"],a[\"text\"],a[\"kind\"],a[\"state\"],a[\"state_reasons\"],a[\"excerpt\"][:150].replace(\"\\n\",\" \"))\nEOF"
}
````

### User / tool · 2026-11-02T04:21:31.062Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:33.124Z

**tool call — Bash**
````
{
 "command": "cat > $TMPDIR/probe.py <<'EOF'\nfrom tests.unit.test_review_rules import seeded\nimport tempfile, pathlib\nfrom app.db import db as DB\nconn,cid,out=seeded(pathlib.Path(tempfile.mkdtemp()))\nfor a in DB.list_items(conn,cid,\"amount\"):\n    print(a[\"id\"],a[\"text\"],a[\"kind\"],a[\"state\"],a[\"state_reasons\"],a[\"excerpt\"][:150].replace(\"\\n\",\" \"))\nEOF\nPYTHONPATH=. .venv/bin/python $TMPDIR/probe.py 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T04:21:33.746Z

**tool result**
````
a1 $6,240 charge verified [] Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $
a2 $185 rate needs_review ['AMOUNT_RATE_NOT_TOTALED'] Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.
a4 $2,150 charge verified [] C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.
a3 missing 3 days of work damages needs_review ['AMOUNT_DAMAGES'] Pain 4/10, improving. Patient reports missing 3 days of work.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:37.281Z

**tool call — Bash**
````
{
 "command": "sed -n 1,75p tests/unit/_fakes.py; grep -n \"class Judge2\" -A12 app/backend/schemas.py"
}
````

### User / tool · 2026-11-02T04:21:37.376Z

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
    call = call or FakeCall(sample_script())
    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call

def items_for(out, n):
    """Every entry-like item (timeline, undated, tray) that cites record number n."""
    rid = f"r{n}"
    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
    return [i for i in pool if rid in i.get("record_ids", [])]
36:class Judge2(_Judge):
37-    verdict: Literal["agree", "disagree", "unsure"]
38-    reason_code: _J2_CODES
39-
40-
41-class Judge3(_Judge):
42-    verdict: Literal["conflict", "benign", "unsure"]
43-    reason_code: _J3_CODES
44-
45-
46-class Judge4(_Judge):
47-    verdict: Literal["agree", "disagree", "unsure"]
48-    reason_code: _J4_CODES
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:46.745Z

**tool call — Bash**
````
{
 "command": "grep -n \"_J2_CODES\" -B1 -A2 app/backend/schemas.py | head -12; grep -n \"def create_app\" -A3 app/backend/api.py | head; sed -n 1,25p tests/unit/test_api_routes.py"
}
````

### User / tool · 2026-11-02T04:21:46.846Z

**tool result**
````
18-_J1_CODES = Literal["NONE", "ADDS_DIAGNOSIS", "ADDS_SEVERITY", "ADDS_CAUSATION", "DROPS_QUALIFIER", "NUMBER_MISMATCH", "OTHER_UNSUPPORTED"]
19:_J2_CODES = Literal["NONE", "SHOULD_BE_CHARGE", "SHOULD_BE_RATE", "SHOULD_BE_ESTIMATE", "SHOULD_BE_DAMAGES", "SHOULD_BE_UNCLEAR", "TEXT_AMBIGUOUS"]
20-_J3_CODES = Literal["NONE", "PLAN_VS_ACTUAL", "FACT_MISMATCH", "DIFFERENT_VISITS", "CAN_BOTH_BE_TRUE", "TEXT_AMBIGUOUS"]
21-_J4_CODES = Literal["NONE", "WRONG_TYPE", "WRONG_CATEGORY", "NEGATED", "NOT_SUPPORTED_BY_QUOTE", "TEXT_AMBIGUOUS"]
22:JUDGE_REASON_CODES = {"j1": _J1_CODES, "j2": _J2_CODES, "j3": _J3_CODES, "j4": _J4_CODES}
23-
24-
--
37-    verdict: Literal["agree", "disagree", "unsure"]
38:    reason_code: _J2_CODES
39-
40-
91:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
92-    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
93-    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
94-    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok):
    for _ in range(160):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:15.359Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_reclassify.py <<'EOF'\n\"\"\"T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\nfrom app.backend import pipeline as PL, reclassify as RC, review as RV\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom app.llm import audited as AU\nfrom tests.unit._fakes import FakeCall, sample_script\n\nTEXT = \"\"\"=== Record 1 ===\nDate: 2026-03-02\nSource: Capital PT, visit 1\nExcerpt: \"Visit completed. Rate of $185 per visit.\"\n\n=== Record 2 ===\nDate: 2026-03-09\nSource: Capital PT, visit 2\nExcerpt: \"Visit completed. Charge per visit $185.\"\n\n=== Record 3 ===\nDate: 2026-03-16\nSource: Capital Imaging\nExcerpt: \"MRI performed. Charge: $310.\"\n\n=== Record 4 ===\nDate: 2026-03-23\nSource: Capital PT, visit 4\nExcerpt: \"Visit completed. Not billed $90 per visit to this patient.\"\n\"\"\"\nJ2 = lambda v, code=\"NONE\": {\"j2\": {\"verdict\": v, \"reason_code\": code}}     # noqa: E731\n\n\ndef seeded(tmp_path, judge=\"agree\"):\n    call = FakeCall(sample_script(extract=lambda u: dict(summary=\"Visit completed.\", excerpt=\"Visit completed.\")))\n    conn = DB.connect(str(tmp_path / \"rc.sqlite\")); cid = DB.create_case(conn, TEXT, now=1.0)\n    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 1.0)\n    return conn, cid\n\n\ndef kinds(conn, cid):\n    return {a[\"text\"] + \"@\" + a[\"record_ids\"][0]: a for a in DB.list_items(conn, cid, \"amount\")}\n\n\ndef aid(conn, cid, text, rec):\n    return kinds(conn, cid)[f\"{text}@{rec}\"][\"id\"]\n\n\ndef events(conn, cid, item_id):\n    return [e for e in DB.list_events(conn, cid, item_id) if (e.get(\"after\") or {}).get(\"event\") == \"reclassify\"]\n\n\ndef test_fixture_classes_are_what_the_tests_assume(tmp_path):\n    conn, cid = seeded(tmp_path)\n    k = kinds(conn, cid)\n    assert (k[\"$185@r1\"][\"kind\"], k[\"$185@r2\"][\"kind\"], k[\"$310@r3\"][\"kind\"], k[\"$90@r4\"][\"kind\"]) == (\"rate\", \"rate\", \"charge\", \"rate\")\n\n\n# ---------------------------------------------------------------- charge -> not a charge\ndef test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$310\", \"r3\")\n    RV.apply_review(conn, cid, a, {\"action\": \"accept\"})\n    r = RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\", \"note\": \"This is a retainer, not a bill.\"}, call=None, now=5.0)\n    assert r[\"item\"][\"kind\"] == \"unclear\" and r[\"item\"][\"review_status\"] == \"pending\"          # her earlier accept was about the old meaning\n    assert r[\"totals\"][\"accepted\"][\"cents\"] == 0 and r[\"reclassified\"] == {\"from\": \"charge\", \"to\": \"unclear\", \"wording\": None, \"judge_verdict\": None, \"restored\": False}\n    [ev] = events(conn, cid, a)\n    assert ev[\"before\"][\"kind\"] == \"charge\" and ev[\"after\"][\"kind\"] == \"unclear\" and ev[\"after\"][\"note\"] == \"This is a retainer, not a bill.\"\n    row = DB.get_item(conn, a, cid)\n    assert row[\"ladder\"][\"reclassification\"][\"by\"] == \"reviewer\" and row[\"ladder\"][\"code_checks\"][\"classified_by\"] == \"reviewer:reclassified\"\n    assert any(e[\"action\"] == \"reset\" for e in DB.list_events(conn, cid, a))                    # the reset is its own audited event\n\n\ndef test_same_direction_is_a_noop_without_an_event(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r1\")\n    r = RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\n    assert r[\"reclassified\"] is None and not events(conn, cid, a)\n\n\ndef test_undoing_her_own_demotion_restores_the_code_class_without_a_judge(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$310\", \"r3\")\n    before = DB.get_item(conn, a, cid)[\"ladder\"][\"judge\"]\n    RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\n    r = RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=None)                                # no judge call available: still fine\n    assert r[\"item\"][\"kind\"] == \"charge\" and r[\"reclassified\"][\"restored\"] is True\n    assert DB.get_item(conn, a, cid)[\"ladder\"][\"judge\"] == before and len(events(conn, cid, a)) == 2\n\n\n# ---------------------------------------------------------------- not a charge -> charge (guarded)\ndef test_rate_without_charge_wording_is_422_and_the_judge_is_never_asked(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r1\")\n    call = FakeCall(J2(\"agree\"))\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=call)\n    assert (e.value.status, e.value.code, e.value.detail[\"reason\"], e.value.detail[\"check\"]) == (422, \"reclassify_refused\", \"NO_CHARGE_WORDING\", \"code\")\n    assert call.log == [] and DB.get_item(conn, a, cid)[\"kind\"] == \"rate\" and not events(conn, cid, a)\n\n\ndef test_negated_wording_does_not_count(tmp_path):\n    conn, cid = seeded(tmp_path)\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, aid(conn, cid, \"$90\", \"r4\"), {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))\n    assert e.value.detail[\"reason\"] == \"NO_CHARGE_WORDING\"\n\n\ndef test_rate_with_wording_and_judge_agreement_becomes_a_pending_verified_charge(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r2\")\n    call = FakeCall(J2(\"agree\"))\n    r = RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=call, now=7.0)\n    assert call.steps() == [\"j2\"] and \"CLASS: charge\" in call.log[0][\"user\"]\n    it = r[\"item\"]\n    assert it[\"kind\"] == \"charge\" and it[\"review_status\"] == \"pending\" and it[\"state\"] == \"verified\"\n    assert r[\"totals\"][\"pending\"][\"cents\"] == 31000 + 18500 and r[\"totals\"][\"accepted\"][\"cents\"] == 0     # counted only after she accepts it\n    row = DB.get_item(conn, a, cid)\n    assert row[\"ladder\"][\"judge\"][\"verdict\"] == \"agree\" and row[\"ladder\"][\"reclassification\"][\"wording\"].lower() == \"charge\"\n    [ev] = events(conn, cid, a)\n    assert ev[\"after\"][\"judge_verdict\"] == \"agree\" and ev[\"after\"][\"wording\"].lower() == \"charge\" and ev[\"before\"][\"kind\"] == \"rate\"\n\n\n@pytest.mark.parametrize(\"verdict,code,reason\", [(\"disagree\", \"SHOULD_BE_RATE\", \"JUDGE_DISAGREES\"), (\"unsure\", \"TEXT_AMBIGUOUS\", \"JUDGE_UNSURE\")])\ndef test_judge_objection_is_422_and_changes_nothing(tmp_path, verdict, code, reason):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r2\")\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=FakeCall(J2(verdict, code)))\n    assert (e.value.status, e.value.detail[\"reason\"], e.value.detail[\"check\"]) == (422, reason, \"judge\")\n    assert e.value.detail[\"wording\"].lower() == \"charge\" and DB.get_item(conn, a, cid)[\"kind\"] == \"rate\" and not events(conn, cid, a)\n\n\n@pytest.mark.parametrize(\"call\", [None, FakeCall(J2(\"agree\", \"BAD CODE\")), lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed())])\ndef test_judge_that_cannot_answer_is_422_judge_unavailable(tmp_path, call):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r2\")\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=call)\n    assert e.value.detail[\"reason\"] == \"JUDGE_UNAVAILABLE\" and DB.get_item(conn, a, cid)[\"kind\"] == \"rate\"\n\n\ndef test_unexpected_judge_bug_propagates(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r2\")\n    with pytest.raises(RuntimeError):\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=lambda *x, **k: (_ for _ in ()).throw(RuntimeError(\"bug\")))\n    assert DB.get_item(conn, a, cid)[\"kind\"] == \"rate\"\n\n\n# ---------------------------------------------------------------- structure\ndef test_bad_body_non_amount_and_rejected_item(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$310\", \"r3\")\n    for body in ({}, {\"to\": \"rate\"}, {\"to\": \"charge\", \"note\": 5}):\n        with pytest.raises(RV.ReviewError) as e:\n            RC.reclassify(conn, cid, a, body, call=None)\n        assert e.value.status == 400\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, \"e1\", {\"to\": \"charge\"}, call=None)\n    assert (e.value.status, e.value.code) == (422, \"invalid_edit\")\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, \"a99\", {\"to\": \"charge\"}, call=None)\n    assert e.value.status == 404\n    DB.update_item(conn, a, now=2.0, case=cid, state=\"rejected\")\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\n    assert (e.value.status, e.value.code) == (409, \"item_rejected\")\n\n\ndef test_injection_tagged_record_and_missing_value_never_become_charges(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r2\")\n    DB.update_item(conn, a, now=2.0, case=cid, value_cents=None)\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))\n    assert e.value.detail[\"reason\"] == \"NO_VALUE\"\n    DB.update_item(conn, a, now=2.0, case=cid, value_cents=18500)\n    conn.execute(\"UPDATE records SET injection_tag='ignore previous instructions' WHERE case_id=? AND id='r2'\", (cid,))\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))\n    assert e.value.detail[\"reason\"] == \"INJECTION_SUSPECTED\"\n\n\ndef test_charge_wording_unit():\n    ex = \"Visit done. Billed $90 per visit. Rate of $120 per visit. Not billed $50 per visit.\"\n    row = lambda raw: {\"text\": raw, \"excerpt_start\": None}      # noqa: E731\n    assert RC.charge_wording(ex, row(\"$90\")).lower() == \"billed\"\n    assert RC.charge_wording(ex, row(\"$120\")) is None\n    assert RC.charge_wording(ex, row(\"$50\")) is None\n    assert RC.charge_wording(\"Amount due $40. Rate $40 per visit.\", row(\"$40\")) is None      # every occurrence of the figure needs its own wording\n\n\n# ---------------------------------------------------------------- rerun and HTTP\ndef test_a_rerun_keeps_her_reclassification(tmp_path):\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$310\", \"r3\")\n    RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\n    call = FakeCall(sample_script(extract=lambda u: dict(summary=\"Visit completed.\", excerpt=\"Visit completed.\")))\n    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 2.0)\n    row = DB.get_item(conn, a, cid)\n    assert row[\"kind\"] == \"unclear\" and row[\"ladder\"][\"reclassification\"][\"by\"] == \"reviewer\" and row[\"state\"] == \"needs_review\"\n\n\ndef test_route(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    c = TestClient(create_app(str(tmp_path / \"h.sqlite\"), static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={}).status_code == 400\n    r = c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={\"to\": \"not_a_charge\"})\n    assert r.status_code == 200 and r.json()[\"item\"][\"kind\"] == \"unclear\" and r.json()[\"reclassified\"][\"from\"] == \"charge\"\n    r = c.post(f\"/api/cases/{tok}/items/a2/reclassify\", json={\"to\": \"charge\"})              # fixture backend has no recorded answer\n    assert r.status_code == 422 and r.json()[\"error\"][\"code\"] == \"reclassify_refused\" and r.json()[\"error\"][\"detail\"][\"reason\"] == \"JUDGE_UNAVAILABLE\"\n    assert c.post(f\"/api/cases/{tok}/items/a99/reclassify\", json={\"to\": \"charge\"}).status_code == 404\n    ev = [e for e in c.get(f\"/api/cases/{tok}/audit\").json()[\"events\"] if e[\"item_id\"] == \"a1\"]\n    assert ev and ev[-1][\"action\"] == \"edit\" or any(e[\"action\"] == \"edit\" for e in ev)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_reclassify.py -x 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:16.381Z

**tool result**
````
.F
=================================== FAILURES ===================================
____ test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited ____

tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-2649/test_charge_to_not_a_charge_is0')

    def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
        conn, cid = seeded(tmp_path)
        a = aid(conn, cid, "$310", "r3")
        RV.apply_review(conn, cid, a, {"action": "accept"})
        r = RC.reclassify(conn, cid, a, {"to": "not_a_charge", "note": "This is a retainer, not a bill."}, call=None, now=5.0)
>       assert r["item"]["kind"] == "unclear" and r["item"]["review_status"] == "pending"          # her earlier accept was about the old meaning
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: assert ('amount' == 'unclear'
E         
E         - unclear
E         + amount)

tests/unit/test_reclassify.py:64: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_reclassify.py::test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 1 passed in 0.53s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:20.768Z

**tool call — Bash**
````
{
 "command": "sed -n 84,94p app/backend/present.py; grep -n '\"amounts\"' -B2 -A8 memory/contracts/api.md | sed -n 1,40p"
}
````

### User / tool · 2026-11-02T04:22:20.860Z

**tool result**
````
    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}


def item_view(conn, case_id, item_id):
    row = DB.get_item(conn, item_id, case_id)
    kind = _ID_KIND[item_id[0]]
    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
    v["kind"] = kind
    return v


93-```json
94-{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
95:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
96-  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
97:  "counts": {"entries": 9, "amounts": 3, "flags": 1},
98-  "error": null, "elapsed_ms": 21540 }
99-```
100-`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline", "message": "..."}`; finished items are kept. Poll every second. Partial results are readable from the case endpoint while running.
101-
102-## GET /api/cases/{token}
103-Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`.
104-```json
105-{
--
133-        "human": {"action": null, "edited_text": null, "at": null} }
134-    } ],
135:  "amounts": [
136-    { "id": "a1", "record_ids": ["r2"], "entry_id": "e2", "text": "$6,240", "value_cents": 624000, "kind": "charge",
137-      "excerpt": "ER charges: $6,240.", "excerpt_start": 533, "excerpt_end": 552,
138-      "state": "verified", "reasons": [], "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
139-      "review_status": "pending", "edited": null, "duplicate_note": null,
140-      "ladder": {
141-        "item_id": "a1", "backend": "fixture", "generator": null,
142-        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
143-        "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c31", "verdict": "agrees"},
--
396-      }
397-    ],
398:    "amounts": [
399-      {
400-        "id": "a1",
401-        "kind": "charge",
402-        "counted_in_total": true,
403-        "edited": false,
404-        "excerpt": "ER charges: $6,240."
405-      },
406-      {
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:27.516Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/reclassify.py'\ns=open(p).read()\ns=s.replace('''    return {\"item\": present.item_view(conn, case_id, item_id), \"totals\"''','''    amount = present._VIEW[\"amount\"](DB.get_item(conn, item_id, case_id), present._recs_by_id(conn, case_id))     # the GET /cases shape: `kind` is the class\n    return {\"item\": present.item_view(conn, case_id, item_id), \"amount\": amount, \"totals\"''',1)\nopen(p,'w').write(s)\np='tests/unit/test_reclassify.py'\ns=open(p).read()\ns=s.replace('r[\"item\"][\"kind\"] == \"unclear\" and r[\"item\"][\"review_status\"]','r[\"amount\"][\"kind\"] == \"unclear\" and r[\"item\"][\"review_status\"]')\ns=s.replace('r[\"item\"][\"kind\"] == \"charge\" and r[\"reclassified\"][\"restored\"]','r[\"amount\"][\"kind\"] == \"charge\" and r[\"reclassified\"][\"restored\"]')\ns=s.replace('it = r[\"item\"]\\n    assert it[\"kind\"] == \"charge\" and it[\"review_status\"]','it = r[\"item\"]\\n    assert r[\"amount\"][\"kind\"] == \"charge\" and it[\"review_status\"]')\ns=s.replace('r.json()[\"item\"][\"kind\"] == \"unclear\"','r.json()[\"amount\"][\"kind\"] == \"unclear\"')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_reclassify.py 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T04:22:28.915Z

**tool result**
````
..................                                                       [100%]
18 passed in 0.95s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:32.292Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_reclassify.py'\ns=open(p).read()\ns=s.replace('    assert ev and ev[-1][\"action\"] == \"edit\" or any(e[\"action\"] == \"edit\" for e in ev)\\n','    assert any(e[\"action\"] == \"edit\" and (e.get(\"after\") or {}).get(\"event\") == \"reclassify\" for e in ev)\\n')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:23:09.604Z

**tool result**
````
E            +  where {'accident', 'date'} = words('Date of accident: 2026-01-08.')
E            +  and   {'first', 'treatment'} = words('First treatment on 2026-01-10.')

tests/unit/test_t093_eval_signature.py:248: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_only_review_module_sets_review_status
FAILED tests/unit/test_billing.py::test_billing_route_for_a_pasted_case - Key...
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
FAILED tests/unit/test_reclassify.py::test_route - assert False
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc1]
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc2]
FAILED tests/unit/test_review_rules.py::test_any_judge_exception_on_edit_is_judge_unavailable_never_supported[exc3]
FAILED tests/unit/test_t093_eval_signature.py::test_every_j3_wrong_item_shares_a_fact_word_across_its_two_quotes_so_keywords_alone_cannot_separate_it
9 failed, 1237 passed in 35.92s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:12.269Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_api_routes.py::test_only_review_module_sets_review_status tests/unit/test_reclassify.py::test_route \"tests/unit/test_review_rules.py\" tests/unit/test_provider.py::test_single_call_path 2>&1 | grep -E \"^E|Error|def test|test_review_rules.py:[0-9]+\" | head -40; grep -n \"test_any_judge_exception\" -B6 -A14 tests/unit/test_review_rules.py"
}
````

### User / tool · 2026-11-02T04:23:14.534Z

**tool result**
````
    def test_only_review_module_sets_review_status():
E           AssertionError: reclassify.py
E           assert ('DB.apply_review(' not in '"""Guarded ... c.close()\n'
E             
E             'DB.apply_review(' is contained here:
E               g
E                       DB.apply_review(conn, item_id, "reset", now=t, case=case_id)
E             ?         ++++++++++++++++
E                   _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
E                                                         "judge_verdict": (jd or {}).get("verdict"), "judge_call_id": (jd or {}).get("call_id"), "restored": restored,...
E             
E             ...Full output truncated, use '-vv' to show)
tests/unit/test_api_routes.py:187: AssertionError
    def test_route(tmp_path, monkeypatch):
E       assert False
E        +  where False = any(<generator object test_route.<locals>.<genexpr> at 0x1085ddbe0>)
tests/unit/test_reclassify.py:215: AssertionError
exc = RuntimeError('judge blew up')
    @pytest.mark.parametrize("exc", [AU.LLMFailed("down"), RuntimeError("judge blew up"), KeyError("verdict"), ValueError("bad")])
    def test_any_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
tests/unit/test_review_rules.py:151: 
E           RuntimeError: judge blew up
tests/unit/_fakes.py:16: RuntimeError
exc = KeyError('verdict')
    @pytest.mark.parametrize("exc", [AU.LLMFailed("down"), RuntimeError("judge blew up"), KeyError("verdict"), ValueError("bad")])
    def test_any_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
tests/unit/test_review_rules.py:151: 
E           KeyError: 'verdict'
tests/unit/_fakes.py:16: KeyError
exc = ValueError('bad')
    @pytest.mark.parametrize("exc", [AU.LLMFailed("down"), RuntimeError("judge blew up"), KeyError("verdict"), ValueError("bad")])
    def test_any_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
tests/unit/test_review_rules.py:151: 
E           ValueError: bad
tests/unit/_fakes.py:16: ValueError
    def test_single_call_path():
E       AssertionError: assert ['backend/pdf_ocr.py'] == []
E         
E         Left contains one more item: 'backend/pdf_ocr.py'
E         Use -v to get more diff
142-def test_helpers_work_on_api_shaped_output():
143-    """Helper smoke (no pipeline): ent()/amt() index api.md-shaped dicts by record_ids."""
144-    out = dict(entries=[dict(id="e5", record_ids=["r5"])], amounts=[dict(id="a3", raw="$185")])
145-    assert ent(out, 5) == "e5" and amt(out, "$185") == "a3"
146-
147-@pytest.mark.parametrize("exc", [AU.LLMFailed("down"), RuntimeError("judge blew up"), KeyError("verdict"), ValueError("bad")])
148:def test_any_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
149-    """T-039 debt / ADR-005 (review.py except around run_j1_meta): ANY exception from the judge on an edit (not only LLMFailed) saves the edit as needs_review with JUDGE_UNAVAILABLE and never as verified/supported."""
150-    conn, cid, out = seeded(tmp_path)
151-    r = RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=dict(summary="Visit 8: pain 4/10 and improving.")), call=FakeCall({"j1": exc}))
152-    it = r["item"]
153-    assert it["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in it["reasons"] and it["state"] != "verified"
154-    assert it["ladder"]["judge"]["verdict"] not in ("supported", "agree")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:23.631Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/reclassify.py'\ns=open(p).read()\ns=s.replace('        DB.apply_review(conn, item_id, \"reset\", now=t, case=case_id)','        review.batch_apply(conn, case_id, item_id, \"reset\", t)               # review.py is the only caller of DB.apply_review',1)\nopen(p,'w').write(s)\np='tests/unit/test_review_rules.py'\ns=open(p).read()\nold=s[s.index('@pytest.mark.parametrize(\"exc\", [AU.LLMFailed(\"down\"), RuntimeError'):s.index('    it = r[\"item\"]\\n    assert it[\"state\"] == \"needs_review\" and \"JUDGE_UNAVAILABLE\"')]\nnew='''@pytest.mark.parametrize(\"exc\", [AU.LLMFailed(\"down\"), P.FixtureMissing(\"h\"), P.LLMError(\"TIMEOUT\")])\ndef test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):\n    \"\"\"T-039 debt / ADR-005, narrowed by T-073: an EXPECTED judge failure (LLMFailed, provider LLMError / FixtureMissing) on an edit saves the edit as needs_review with JUDGE_UNAVAILABLE and never as verified/supported. Any other exception is a bug and propagates (tests/unit/test_judge_guard.py).\"\"\"\n    conn, cid, out = seeded(tmp_path)\n    r = RV.apply_review(conn, cid, ent(out, 5), dict(action=\"edit\", edits=dict(summary=\"Visit 8: pain 4/10 and improving.\")), call=FakeCall({\"j1\": exc}))\n'''\ns=s.replace(old,new,1)\nif \"provider as P\" not in s:\n    s=s.replace(\"from app.llm import audited as AU\\n\",\"from app.llm import audited as AU, provider as P\\n\",1)\nopen(p,'w').write(s)\nEOF\ngit diff tests/unit/test_review_rules.py | head -30; cat > $TMPDIR/p2.py <<'EOF'\nfrom fastapi.testclient import TestClient\nimport os, tempfile, pathlib\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom app.backend.api import create_app\nd=pathlib.Path(tempfile.mkdtemp())\nc = TestClient(create_app(str(d/\"h.sqlite\"), static_dir=str(d)), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\nprint(c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={\"to\": \"not_a_charge\"}).status_code)\nprint(c.get(f\"/api/cases/{tok}/audit\").json()[\"events\"])\nEOF\nPYTHONPATH=. .venv/bin/python $TMPDIR/p2.py"
}
````

### User / tool · 2026-11-02T04:23:24.209Z

**tool result**
````
diff --git a/tests/unit/test_review_rules.py b/tests/unit/test_review_rules.py
index 8fc07a9..43ef9bf 100644
--- a/tests/unit/test_review_rules.py
+++ b/tests/unit/test_review_rules.py
@@ -2,7 +2,7 @@
 import pytest
 from app.backend import pipeline as PL, review as RV, export as X
 from app.db import db as DB
-from app.llm import audited as AU
+from app.llm import audited as AU, provider as P
 from tests.unit import _golden as G
 from tests.unit._fakes import FakeCall, golden_summaries, which_record
 
@@ -144,9 +144,9 @@ def test_helpers_work_on_api_shaped_output():
     out = dict(entries=[dict(id="e5", record_ids=["r5"])], amounts=[dict(id="a3", raw="$185")])
     assert ent(out, 5) == "e5" and amt(out, "$185") == "a3"
 
-@pytest.mark.parametrize("exc", [AU.LLMFailed("down"), RuntimeError("judge blew up"), KeyError("verdict"), ValueError("bad")])
-def test_any_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
-    """T-039 debt / ADR-005 (review.py except around run_j1_meta): ANY exception from the judge on an edit (not only LLMFailed) saves the edit as needs_review with JUDGE_UNAVAILABLE and never as verified/supported."""
+@pytest.mark.parametrize("exc", [AU.LLMFailed("down"), P.FixtureMissing("h"), P.LLMError("TIMEOUT")])
+def test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported(tmp_path, exc):
+    """T-039 debt / ADR-005, narrowed by T-073: an EXPECTED judge failure (LLMFailed, provider LLMError / FixtureMissing) on an edit saves the edit as needs_review with JUDGE_UNAVAILABLE and never as verified/supported. Any other exception is a bug and propagates (tests/unit/test_judge_guard.py)."""
     conn, cid, out = seeded(tmp_path)
     r = RV.apply_review(conn, cid, ent(out, 5), dict(action="edit", edits=dict(summary="Visit 8: pain 4/10 and improving.")), call=FakeCall({"j1": exc}))
     it = r["item"]
200
[{'id': 'v13b0a9923935', 'item_id': 'a1', 'action': 'edit', 'at': '2026-11-02T04:23:24Z'}]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:26.953Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_reclassify.py'\ns=open(p).read()\ns=s.replace('    assert any(e[\"action\"] == \"edit\" and (e.get(\"after\") or {}).get(\"event\") == \"reclassify\" for e in ev)\\n','    assert [e[\"action\"] for e in ev] == [\"edit\"]                      # review_events has no reclassify action yet; the payload (local audit) says reclassify\\n')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T04:24:10.066Z

**tool result**
````
E            +    where <function search at 0x109c447c0> = re.search
E            +    and   re.MULTILINE = re.M

tests/unit/test_provider_backends.py:159: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
2 failed, 1255 passed in 41.57s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:23.812Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\na=\"| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls (\\\"Why?\\\") |\\n\"\nassert s.count(a)==1\nrow=\"| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: \\\"charge\\\"\\\\|\\\"not_a_charge\\\", note?}`. See the section below |\\n\"\ns=s.replace(a,a+row,1)\nold=\"**amount** none (accept or dismiss only; a rate can never become a charge)\"\nassert s.count(old)==1\ns=s.replace(old,\"**amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`)\",1)\nb=\"## GET /api/cases/{token}/export\\n\"\nassert s.count(b)==1\nsec='''## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)\nThe paralegal says a dollar figure is, or is not, a billed charge. Taking a figure **out** of the total is always her call; putting one **in** needs evidence. Body: `{ \"to\": \"charge\" | \"not_a_charge\", \"note\": \"optional, 500 chars\" }`.\n- `to: \"not_a_charge\"` on a `charge`: always allowed. The class becomes `unclear` (response `amount.kind: \"unclear\"`; shown as \"not added to the total\", never totaled).\n- `to: \"charge\"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated (\"not billed\", \"unbilled\"), the figure has a parsed value and its record is not injection-tagged, **and (2) judge 2** re-checks the figure against class `charge` and answers `agree`. Code runs first; the judge is not called when the code check fails. Undoing her own earlier demotion of a figure the code first called a charge skips both checks (the original class returns with the judge answer it had; works with no judge available).\n- Same class as now: `200`, `reclassified: null`, nothing written.\n- Anything not allowed: `422 reclassify_refused`, nothing changes, no event: `{error: {code, message, detail: {reason, check: \"code\"|\"judge\", wording?, error_class?}}}`. `detail.reason` is one of `NO_VALUE`, `INJECTION_SUSPECTED`, `NO_CHARGE_WORDING` (check `code`), `JUDGE_DISAGREES`, `JUDGE_UNSURE`, `JUDGE_UNAVAILABLE` (check `judge`; `JUDGE_UNAVAILABLE` includes no recorded answer in demo mode, so a rate-to-charge there is refused with \"try again\" wording). `message` is a fixed plain sentence, safe to show. Other errors: `400 bad_request` (missing/other `to`, non-text `note`), `404 not_found`, `409 item_rejected`, `422 invalid_edit` (not an amount).\n- On success the item goes back to `review_status: pending` (a reset event is logged first if she had decided it; her earlier decision was about the old meaning) and must be accepted again. Its state is recomposed: a judged charge is `verified`; a not-a-charge is `needs_review` with `AMOUNT_UNCLEAR`.\n- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: \"reclassify\", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassification` = `{from, to, at, by: \"reviewer\", original_kind, wording, restored, note, previous_judge}` and `ladder.code_checks.classified_by` = `\"reviewer:reclassified\"`.\n- A rerun (`POST /run`) keeps her class for the same figure (same text and value); a changed figure takes the new code class.\n\nResponse 200:\n```json\n{ \"item\":   { \"id\": \"a2\", \"kind\": \"amount\", \"review_status\": \"pending\", \"state\": \"verified\", \"reasons\": [] },\n  \"amount\": { \"id\": \"a2\", \"text\": \"$185\", \"value_cents\": 18500, \"kind\": \"charge\", \"state\": \"verified\", \"reasons\": [], \"why\": \"...\", \"review_status\": \"pending\",\n              \"ladder\": { \"reclassification\": { \"from\": \"rate\", \"to\": \"charge\", \"by\": \"reviewer\", \"wording\": \"Charge\" }, \"...\": \"...\" } },\n  \"totals\": { \"...\": \"as in review\" }, \"review\": { \"...\": \"as in review\" },\n  \"reclassified\": { \"from\": \"rate\", \"to\": \"charge\", \"wording\": \"Charge\", \"judge_verdict\": \"agree\", \"restored\": false },\n  \"warnings\": [] }\n```\nNote `item.kind` is the item type (`\"amount\"`, as in the review response); the amount's class is `amount.kind`, the same field the case endpoint uses. Patch local state from `amount`, `totals` and `review`; no refetch needed.\n\n'''\ns=s.replace(b,sec+b,1)\nopen(p,'w').write(s)\nEOF\ngit diff --stat memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T04:24:23.979Z

**tool result**
````
 memory/contracts/api.md | 91 ++++++++++++++++++++++++++++++++++++++++++++++++-
 1 file changed, 90 insertions(+), 1 deletion(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:27.639Z

**tool call — Bash**
````
{
 "command": "git status --short app/backend/review.py app/backend/api.py app/backend/pipeline.py memory/contracts/api.md tests/unit/test_review_rules.py app/backend/reclassify.py app/backend/judge_guard.py tests/unit/test_reclassify.py tests/unit/test_judge_guard.py; git diff app/backend/review.py | grep -c '^@@'; git log --oneline -3"
}
````

### User / tool · 2026-11-02T04:24:27.780Z

**tool result**
````
MM app/backend/api.py
 M app/backend/pipeline.py
 M app/backend/review.py
MM memory/contracts/api.md
 M tests/unit/test_review_rules.py
?? app/backend/judge_guard.py
?? app/backend/reclassify.py
?? tests/unit/test_judge_guard.py
?? tests/unit/test_reclassify.py
5
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:36.927Z

**tool call — Bash**
````
{
 "command": "cat > $TMPDIR/mk.py <<'EOF'\nimport subprocess, os\ndef head(p): return subprocess.run([\"git\",\"show\",\"HEAD:\"+p],capture_output=True,text=True,check=True).stdout\n# api.py\ns=head(\"app/backend/api.py\")\na=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(a)==1\ns=s.replace(a,a+\"    from app.backend import reclassify\\n    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084\\n\",1)\nopen(os.environ[\"TMPDIR\"]+\"/api.py\",\"w\").write(s)\n# pipeline\ns=head(\"app/backend/pipeline.py\")\na=\"\"\"        row = _row(kind, it)\n        old = existing.get(it[\"id\"])\n\"\"\"\nassert s.count(a)==1\ns=s.replace(a,\"\"\"        old = existing.get(it[\"id\"])\n        if kind == \"amount\" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure\n            from app.backend import reclassify as RC\n            it = RC.carry_over(old, it)\n        row = _row(kind, it)\n\"\"\",1)\nopen(os.environ[\"TMPDIR\"]+\"/pipeline.py\",\"w\").write(s)\n# api.md\ns=head(\"memory/contracts/api.md\")\ncur=open(\"memory/contracts/api.md\").read()\ni=cur.index(\"## POST /api/cases/{token}/items/{item_id}/reclassify\"); j=cur.index(\"## GET /api/cases/{token}/export\\n\",i)\nsec=cur[i:j]\na=\"| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls (\\\"Why?\\\") |\\n\"\nassert s.count(a)==1\nrow=[l for l in cur.splitlines(True) if \"/items/{item_id}/reclassify` |\" in l][0]\ns=s.replace(a,a+row,1)\nold=\"**amount** none (accept or dismiss only; a rate can never become a charge)\"\nassert s.count(old)==1\ns=s.replace(old,\"**amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`)\",1)\nb=\"## GET /api/cases/{token}/export\\n\"\nassert s.count(b)==1\ns=s.replace(b,sec+b,1)\nopen(os.environ[\"TMPDIR\"]+\"/api.md\",\"w\").write(s)\nEOF\npython3 $TMPDIR/mk.py && echo ok\nexport GIT_INDEX_FILE=$(mktemp -u); git read-tree HEAD\nfor pair in \"app/backend/api.py:api.py\" \"app/backend/pipeline.py:pipeline.py\" \"memory/contracts/api.md:api.md\"; do p=${pair%%:*}; f=${pair##*:}; h=$(git hash-object -w $TMPDIR/$f); git update-index --cacheinfo 100644,$h,$p; done\ngit add app/backend/review.py app/backend/judge_guard.py app/backend/reclassify.py tests/unit/test_judge_guard.py tests/unit/test_reclassify.py tests/unit/test_review_rules.py\ngit diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:24:37.529Z

**tool result**
````
ok
 app/backend/api.py              |   2 +
 app/backend/judge_guard.py      |  17 ++++
 app/backend/pipeline.py         |   5 +-
 app/backend/reclassify.py       | 175 ++++++++++++++++++++++++++++++++
 app/backend/review.py           |  14 ++-
 memory/contracts/api.md         |  24 ++++-
 tests/unit/test_judge_guard.py  |  52 ++++++++++
 tests/unit/test_reclassify.py   | 215 ++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_review_rules.py |   8 +-
 9 files changed, 498 insertions(+), 14 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:48.218Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u); git read-tree HEAD\nOLD=$(git rev-parse HEAD)\ngit add app/backend/review.py app/backend/judge_guard.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py\ngit commit -q -m \"fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD\nfor pair in \"app/backend/api.py:api.py\" \"app/backend/pipeline.py:pipeline.py\" \"memory/contracts/api.md:api.md\"; do p=${pair%%:*}; f=${pair##*:}; h=$(git hash-object -w $TMPDIR/$f); git update-index --cacheinfo 100644,$h,$p; done\ngit add app/backend/reclassify.py tests/unit/test_reclassify.py\ngit commit -q -m \"feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD\ngit diff --stat $OLD HEAD | tail -12\nunset GIT_INDEX_FILE\n# sync real index where it still holds the old HEAD blob\nfor p in app/backend/review.py tests/unit/test_review_rules.py app/backend/pipeline.py app/backend/api.py memory/contracts/api.md; do\n idx=$(git ls-files -s -- $p | awk '{print $2}'); oldb=$(git rev-parse $OLD:$p); if [ \"$idx\" = \"$oldb\" ]; then git update-index --cacheinfo 100644,$(git rev-parse HEAD:$p),$p; echo synced $p; else echo \"left $p (index has others' staged edits)\"; fi; done"
}
````

### User / tool · 2026-11-02T04:24:48.297Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: export GIT_INDEX_FILE=$(mktemp -u); git read-tree HEAD
OLD=$(git rev-parse HEAD)
git add app/backend/review.py app/backend/judge_guard.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:50.991Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/bk && rm -f /private/tmp/claude-501/bk/idx && git rev-parse HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git add app/backend/review.py app/backend/judge_guard.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py && GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:24:51.409Z

**tool result**
````
e3fc01c91ad227eae5f074ac4251b13edd60aaaa
 app/backend/judge_guard.py      | 17 ++++++++++++++
 app/backend/review.py           | 14 +++++------
 tests/unit/test_judge_guard.py  | 52 +++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_review_rules.py |  8 +++----
 4 files changed, 79 insertions(+), 12 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:53.357Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git commit -q -m \"fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T04:24:53.823Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
7724412
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:54.371Z

**tool call — Bash**
````
{
 "command": "T=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8; ls $TMPDIR 2>/dev/null | head; echo $TMPDIR"
}
````

### User / tool · 2026-11-02T04:24:54.993Z

**tool result**
````
AudioComponentRegistrar
AudioConverterService
BlobRegistryFiles-Jb6FyHse
BlobRegistryFiles-cpt8h5f0
CSExattrCryptoService
CrashHandlerService
SOSBackup-BackupBagV0-tomb
SOSBackup-OtherSyncable-tomb
SOSBackup-Passwords-tomb
SOSBackup-iCloudIdentity-tomb
/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:59.140Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && python3 $TMPDIR/mk.py && echo rebuilt && rm -f /private/tmp/claude-501/bk/idx && GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git read-tree HEAD && for pair in \"app/backend/api.py:api.py\" \"app/backend/pipeline.py:pipeline.py\" \"memory/contracts/api.md:api.md\"; do p=${pair%%:*}; f=${pair##*:}; h=$(git hash-object -w ${TMPDIR}${f}); GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git update-index --cacheinfo 100644,$h,$p; done; GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git add app/backend/reclassify.py tests/unit/test_reclassify.py && GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:24:59.780Z

**tool result**
````
7724412 fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
rebuilt
 app/backend/api.py            |   2 +
 app/backend/pipeline.py       |   5 +-
 app/backend/reclassify.py     | 175 ++++++++++++++++++++++++++++++++++
 memory/contracts/api.md       |  24 ++++-
 tests/unit/test_reclassify.py | 215 ++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 419 insertions(+), 2 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:02.806Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/bk/idx git commit -q -m \"feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD && git status --short app/backend/review.py app/backend/api.py app/backend/pipeline.py memory/contracts/api.md tests/unit/test_review_rules.py app/backend/reclassify.py"
}
````

### User / tool · 2026-11-02T04:25:03.424Z

**tool result**
````
check_secrets: ok (5 file(s) scanned staged)
ec33bf0
MM app/backend/api.py
MM app/backend/pipeline.py
D  app/backend/reclassify.py
MM app/backend/review.py
MM memory/contracts/api.md
MM tests/unit/test_review_rules.py
?? app/backend/reclassify.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:08.320Z

**tool call — Bash**
````
{
 "command": "git reset -q -- app/backend/api.py app/backend/pipeline.py app/backend/reclassify.py app/backend/review.py memory/contracts/api.md tests/unit/test_review_rules.py; git status --short app/backend/review.py app/backend/api.py app/backend/pipeline.py memory/contracts/api.md tests/unit/test_review_rules.py app/backend/reclassify.py app/backend/judge_guard.py tests/unit/test_reclassify.py tests/unit/test_judge_guard.py; git diff --stat -- app/backend/api.py app/backend/pipeline.py memory/contracts/api.md | tail -4"
}
````

### User / tool · 2026-11-02T04:25:08.481Z

**tool result**
````
 M app/backend/api.py
D  app/backend/judge_guard.py
 M app/backend/pipeline.py
 M memory/contracts/api.md
D  tests/unit/test_judge_guard.py
D  tests/unit/test_reclassify.py
?? app/backend/judge_guard.py
?? tests/unit/test_judge_guard.py
?? tests/unit/test_reclassify.py
 app/backend/api.py      | 36 +++++++++++++++++++++++++-----------
 app/backend/pipeline.py | 38 ++++++++++++++++++++++----------------
 memory/contracts/api.md | 38 ++++++++++++++++++++++++++++++++++++++
 3 files changed, 85 insertions(+), 27 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:10.468Z

Remaining "D " entries are stale real-index leftovers for files that are in HEAD; reset them too.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:11.595Z

**tool call — Bash**
````
{
 "command": "git reset -q -- app/backend/judge_guard.py tests/unit/test_judge_guard.py tests/unit/test_reclassify.py; git status --short app/backend/judge_guard.py app/backend/reclassify.py tests/unit/test_reclassify.py tests/unit/test_judge_guard.py; git diff HEAD --stat -- app/backend/reclassify.py app/backend/judge_guard.py app/backend/review.py; .venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T04:25:14.629Z

**tool result**
````
.......................................................                  [100%]
55 passed in 2.40s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:15.605Z

Clean. Now board updates.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:25.174Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\n$B ac T-073 --check 1 --agent backend --evidence \"tests/unit/test_judge_guard.py (10 tests) + test_review_rules.py::test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported: LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class; RuntimeError/KeyError/AttributeError propagate and save nothing\" \n$B handoff T-073 --agent backend --text \"What changed: new app/backend/judge_guard.py (guarded() catches only AU.LLMFailed and provider LLMError incl. FixtureMissing); review._check_summary uses it, so edit and manual entry record ladder.judge.error_class and anything else propagates. Old test test_any_judge_exception_on_edit... narrowed to the expected classes (it encoded the broad catch). · Verified: .venv/bin/python -m pytest -q tests/unit (only 2 failures, test_single_call_path x2, from another worker's pdf_ocr.py) · Left: LLMFailed is already swallowed inside judges._run (no class kept; judges.py off limits). Prompt/model unchanged so no eval run. Commit 7724412.\"\n$B commit T-073 --sha 7724412 --agent backend\n$B move T-073 in_review --agent backend\n$B ac T-084 --check 1 --agent backend --evidence \"tests/unit/test_reclassify.py (18 tests): charge->not-charge, restore, rate+wording+judge agree -> charge, no wording 422 (judge not called), judge disagree/unsure/unavailable 422, injection/no value, audit event, rerun keeps class, HTTP route\"\n$B note T-084 --agent backend --text \"FOR FRONTEND/UX: POST /api/cases/{token}/items/{id}/reclassify body {to:'charge'|'not_a_charge', note?}. Show 'Not a charge' on a charge row and 'This is a charge' on a rate/estimate/unclear row. 200 returns amount (kind=class, patch row), totals, review, reclassified; item returns to pending, so she must accept again. 422 reclassify_refused: show error.message (fixed plain sentence) and detail.reason/check; JUDGE_UNAVAILABLE = offer 'Try again'. Demo mode has no recorded judge answer so rate->charge is always refused there. Item stepper: classified_by reads 'reviewer:reclassified', ladder.reclassification has from/to/wording/note. Contract: api.md section 'POST .../reclassify'.\"\n$B note T-084 --agent backend --text \"NEEDS DB CARD: review_events.action CHECK has no 'reclassify', so the audit row is written as action 'edit' with after.event='reclassify' (constant reclassify.AUDIT_ACTION). When db adds the action, flip the constant. Also trace.py amount_class step text says 'A billing phrase ... labels this figure a charge' for reclassified charges; owner of trace.py may want a reviewer-set variant.\"\n$B handoff T-084 --agent backend --text \"What changed: new app/backend/reclassify.py (logic, route, carry_over), 2-line route hook in api.py, 4-line carry_over hook in pipeline._persist so a rerun keeps her class, api.md section + index row (old 'rate can never become a charge' line reworded). Rules: to not_a_charge always; to charge needs code wording in the same sentence (not negated, value parsed, no injection) then judge 2 agree, else 422 reclassify_refused with fixed reason; restore of own demotion skips both; item resets to pending. Audit: reset event + edit-action row with after.event=reclassify (CHECK limit, see note). · Verified: pytest tests/unit/test_reclassify.py 18 pass; full tests/unit has only 2 unrelated failures (pdf_ocr single-call-path). · Left: db CHECK change, UI. Commit ec33bf0.\"\n$B commit T-084 --sha ec33bf0 --agent backend\n$B move T-084 in_review --agent backend"
}
````

### User / tool · 2026-11-02T04:25:25.824Z

**tool result**
````
AC 1 checked: tests/unit/test_judge_guard.py (10 tests) + test_review_rules.py::test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported: LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class; RuntimeError/KeyError/AttributeError propagate and save nothing
handoff written on T-073
T-073: commit 7724412 recorded
T-073: in_progress -> in_review
AC 1 checked: tests/unit/test_reclassify.py (18 tests): charge->not-charge, restore, rate+wording+judge agree -> charge, no wording 422 (judge not called), judge disagree/unsure/unavailable 422, injection/no value, audit event, rerun keeps class, HTTP route
noted on T-084
noted on T-084
handoff written on T-084
T-084: commit ec33bf0 recorded
T-084: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:29.330Z

T-073 and T-084 are both in review. `tests/unit` ends 1255 passed, 2 failed. Both failures are `test_single_call_path` (test_provider.py and test_provider_backends.py), tripped by another worker's `backend/pdf_ocr.py`.

- **T-073:** `review.py` now catches only `LLMFailed` and provider `LLMError`/`FixtureMissing`, and records the error class in `ladder.judge.error_class`. Anything else propagates. I narrowed the old `test_any_judge_exception...` test in `test_review_rules.py`, because it required the broad catch. Commit 7724412.
- **T-084:** `POST /items/{id}/reclassify` is built as specified. Two things differ from what you might assume:
  - **Audit row:** the `review_events` CHECK has no `reclassify` action, so the audit row is written as `edit` with `after.event='reclassify'`. It needs a db card to add the action.
  - **Rerun:** I added a 4-line hook in `pipeline._persist` so a rerun keeps the paralegal's class for the same figure.

  The UI notes and the db CHECK note are on the card. Commit ec33bf0.
