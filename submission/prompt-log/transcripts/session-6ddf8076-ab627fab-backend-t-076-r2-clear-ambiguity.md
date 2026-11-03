# Subagent: Backend: T-076 r2 clear ambiguity (Backend: T-076 r2 clear ambiguity)

Source: `agent-ab627fabe04f1bb5f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:08:19.971Z

You own board card T-076, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-076-paralegal.md and reviews/T-068-paralegal-r3.md.

- **Major:** confirm_date leaves DATE_AMBIGUOUS on the entry, so after confirmation it still reads "Needs review" and "the date can be read two ways". When the paralegal confirms a date, clear the date-ambiguity reason and status on that entry and its record, and keep an audit event recording which date was chosen. The entry should then be reviewable like any other dated entry.
- **Minor:** api.md says "no bulk accept"; fix it.
- **UI follow-up:** Edit is enabled on undated rows. Since edit implies accept, the server already 422s it. Post a note on T-060 for the frontend rather than editing app/frontend.

Add unit tests. Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec or temp-index rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-076 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T03:08:19.975Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:22.273Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-076-paralegal.md | head -80; grep -rn \"confirm_date\\|DATE_AMBIGUOUS\" app/backend app/llm memory/contracts/api.md | head -40; grep -n \"bulk\" memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T03:08:22.373Z

**tool result**
````
# T-076 review: paralegal-reviewer (Maria Delgado persona)

Scope: commit 88a3393 (app/backend/review.py, case_extras.py, export.py; memory/contracts/api.md; tests/unit/test_date_unconfirmed.py), exercised through the running app on a `git archive HEAD` snapshot (HEAD = 5f71a65, which contains 88a3393) at http://127.0.0.1:7880 with LLM_BACKEND=fixture FIXTURE_SET=curated and a scratch DATA_DIR. Sample case: evals/golden/case_01_date_formats.txt. The server is stopped (port closed).

## Summary

The server gate does what the card says. Every single, edit and batch accept on the undated record 8 entry is refused with 422 DATE_UNCONFIRMED and nothing changes. The manual-entry path cannot bypass it. After confirm_date the entry accepts and its letter line is correct. One defect is on the server side: confirm_date clears the record warning but leaves the entry's DATE_AMBIGUOUS reason, so the confirmed entry still reads as unresolved.

## What I checked

- Before confirm (curl against the running app): POST items/e8/review accept, edit; POST review/batch accept with ["e8"]. Responses 422 DATE_UNCONFIRMED; batch detail.rejected [{id e8, reason date_unconfirmed}]. Case JSON before and after identical except updated_at; audit event count 7 before and after.
- Manual entry on the undated record: POST records/r8/entry returns 422 invalid_edit "This record already has an entry; edit that entry instead." (no bypass).
- Confirm and accept (Playwright flow artifacts/review-evidence/T-068-paralegal-r3-flow.py, S3 and S4 steps): confirm April 5, 2026 moved the entry onto the timeline with date 2026-04-05; accept returned review_status accepted; reload kept it.
- Export before confirm: no Pennywhistle line in the letter, no "date not stated" in the letter. Internal notes list the record as "date not stated" and "not reviewed" (internal block only).
- Export after confirm and accept: artifacts/review-evidence/T-068-r3/export-letter-after-confirm-accept.txt contains "April 5, 2026 — Dr. Orla Pennywhistle, phone note" with the verbatim quote "Patient reports no new symptoms." and "Source [Ex. __ / Bates __]".
- `.venv/bin/python -m pytest -q tests/unit -k "date or accept"` at the HEAD snapshot: 115 passed, 873 deselected in 4.72s.
- Not exercised: the export path "date not confirmed, not exported" (export.py _reconcile). No API path I could find puts an accepted entry back to an undated state, so I could not reach it.

## Findings

**F1 (major) confirm_date leaves the entry's DATE_AMBIGUOUS reason; the confirmed, accepted entry still reads as unresolved.**
Evidence: GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date(April 5, 2026) and accept: `"state": "needs_review", "reasons": ["DATE_AMBIGUOUS"], "why": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.", "review_status": "accepted"`. The record r8 is `date_status: confirmed`, `date_iso: 2026-04-05`, and the record_warning flags are empty (case JSON: record_warning flags []). The UI row shows "Needs review" and "Check: the date can be read two ways" (artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json, S4_entry_after_confirm_text; screenshot artifacts/review-evidence/T-068-r3/S4b-accepted.png).
Why it matters: the paralegal confirmed the date and the entry still says the date is unresolved. The adjuster-facing letter is not affected. I rate this major, not blocker, because nothing invented reaches the letter; it is a stale statement in the app and a state the persona cannot read as settled.
Fix: confirm_date removes DATE_AMBIGUOUS from the entry's reasons and recomputes its state, the same way it already clears the record warning and recomputes gap flags (api.md, confirm_date section).
Acceptance test: case_01, confirm April 5, 2026. GET items/e8 has no DATE_AMBIGUOUS in reasons, its why text does not contain 'two ways', and state is not needs_review once accepted.

**F2 (minor) memory/contracts/api.md contradicts itself on bulk accept.**
Evidence: memory/contracts/api.md line 74 documents batch accept ("Request: {"action": "accept" | "reset", "item_ids": [...]} ... D-041: ... DATE_UNCONFIRMED"), and line 259 says "There is no bulk accept." The batch endpoint is live (curl POST /review/batch returned 422 DATE_UNCONFIRMED).
Why it matters: the contract is what the frontend and the next reviewer read. A sentence saying there is no bulk accept, next to a documented batch endpoint, invites a wrong test.
Fix: delete "There is no bulk accept." from line 259 (the D-041 text in that paragraph is otherwise correct).
Acceptance test: grep -n "no bulk accept" memory/contracts/api.md returns nothing.

## Verdict

changes: 0 blockers, 1 major (F1), 1 minor (F2). The D-041 server gate itself passes every check I ran. verify_quickly is 3, below the ship bar of 4, because the confirmed entry still reads as unresolved and the paralegal cannot tell from the row that the confirm settled the date.

## Questions for Chris

1. Does confirm_date need to clear the entry's needs_review state, or should an accepted entry keep needs_review as a historical flag? I assume the former.
2. The export reason "date not confirmed, not exported" has no reachable path I could find. Is there a path (for example a re-run that keeps an accepted entry with a re-ambiguous date) that should be tested?

```json
{"card": "T-076", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 88a3393 (app/backend/review.py, case_extras.py, export.py; memory/contracts/api.md; tests/unit/test_date_unconfirmed.py), run through a git archive HEAD (5f71a65) snapshot at http://127.0.0.1:7880 (LLM_BACKEND=fixture FIXTURE_SET=curated, scratch DATA_DIR); sample case evals/golden/case_01_date_formats.txt",
 "exercised": [
   "read personas/paralegal.md, docs/RUNBOOK.md, memory/ORCHESTRATOR_DECISIONS.md D-041, board show T-076, git show 88a3393 diff",
   "git archive HEAD into the scratchpad; started the app from the snapshot on :7880; GET /api/health 200; stopped it afterwards",
   "curl: create case_01, run to ready; POST items/e8/review accept and edit before confirm (422 DATE_UNCONFIRMED); POST review/batch accept ['e8'] (422 DATE_UNCONFIRMED, detail.rejected); GET case before and after (identical apart from updated_at); audit event count before and after (7, 7)",
   "curl: POST records/r8/entry manual entry on the undated record (422 invalid_edit, already has an entry)",
   "Playwright artifacts/review-evidence/T-068-paralegal-r3-flow.py: forced POST accept/edit/batch in the browser session, export before confirm, confirm April 5, 2026, accept, reload, export after confirm",
   "GET items/e8 after confirm and accept (reasons still DATE_AMBIGUOUS)",
   "read artifacts/review-evidence/T-068-r3/export-letter-after-confirm-accept.txt and export-notes-after-confirm-accept.txt",
   "grep -n 'bulk accept' memory/contracts/api.md (lines 74 and 259)",
   ".venv/bin/python -m pytest -q tests/unit -k 'date or accept' at the HEAD snapshot: 115 passed, 873 deselected"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "server_gate_undated_accept_edit_batch": 5, "nothing_changed_on_refusal": 5, "manual_entry_bypass_blocked": 5, "confirm_then_accept_then_export": 4, "confirmed_entry_state_matches_record": 2, "contract_doc_consistent": 3},
 "findings": [
   {"severity": "major", "title": "confirm_date leaves DATE_AMBIGUOUS on the entry; confirmed and accepted entry still reads as unresolved",
    "evidence": "GET /api/cases/3xQA67xxiHA55dJbhknRNQ/items/e8 after confirm_date(2026-04-05) and accept: state needs_review, reasons [DATE_AMBIGUOUS], why 'The date can be read two ways; confirm which one is right. It is left out of gap checks until then.', review_status accepted. Record r8: date_status confirmed, date_iso 2026-04-05, record_warning flags []. UI row: artifacts/review-evidence/T-068-r3/T-068-r3-flow-dump.json S4_entry_after_confirm_text; screenshot artifacts/review-evidence/T-068-r3/S4b-accepted.png",
    "why_it_matters": "The paralegal confirmed the date, and the entry still says the date is unresolved, so the state does not read as settled. The letter line is correct, so this is not a blocker: nothing invented reaches the letter.",
    "fix": "confirm_date removes DATE_AMBIGUOUS from the entry's reasons and recomputes its state, as it already does for the record warning and gap flags.",
    "acceptance_test": "case_01: confirm 2026-04-05, then accept. GET items/e8 has no DATE_AMBIGUOUS reason, its why text does not say 'two ways', and state is not needs_review once accepted."},
   {"severity": "minor", "title": "api.md says there is no bulk accept, one section after documenting it",
    "evidence": "memory/contracts/api.md:74 documents POST review/batch accept (item_ids, DATE_UNCONFIRMED); memory/contracts/api.md:259 reads 'There is no bulk accept.' The batch endpoint is live: POST /review/batch with ['e8'] returns 422 DATE_UNCONFIRMED.",
    "why_it_matters": "The contract is what the frontend and later reviewers read; the contradiction invites a wrong test.",
    "fix": "Delete 'There is no bulk accept.' from api.md line 259.",
    "acceptance_test": "grep -n 'no bulk accept' memory/contracts/api.md returns no match."}
 ],
 "whats_right": [
   "Accept, edit and batch accept on the undated record 8 entry all return 422 DATE_UNCONFIRMED before any write; the case JSON is unchanged apart from updated_at and the audit event count is unchanged (7 before, 7 after).",
   "Manual entry on the undated record is refused (422 invalid_edit, 'This record already has an entry'), so the date gate cannot be bypassed that way.",
   "After confirm_date the entry accepts and the letter line reads 'April 5, 2026 — Dr. Orla Pennywhistle, phone note' with the verbatim quote and [Ex. __ / Bates __]; no 'date not stated' appears in the letter."
 ],
 "questions_for_chris": [
   "F1: should confirm_date clear the entry's needs_review state as well as the record warning? I assume yes.",
   "The export reason 'date not confirmed, not exported' had no reachable path I could find. Should a test reach it (for example a re-run that re-marks an accepted entry as ambiguous)?"
 ]}
```
app/backend/why.py:17:    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:20:_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
app/backend/review.py:172:# ---------------------------------------------------------------- confirm_date
app/backend/review.py:173:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
app/backend/review.py:193:        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
app/backend/api.py:378:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/api.py:379:    async def confirm_date(token: str, rid: str, request: Request):
app/backend/api.py:386:            return review.confirm_date(c, token, rid, b["date"])
app/backend/dates.py:77:    """confirm_date hook (R-IN-5): the paralegal may only choose one of the code-proposed readings. Returns the confirmed date dict."""
app/backend/pipeline.py:41:    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
app/backend/gaps.py:63:    """Recompute after confirm_date: a flag whose record pair, dates and days are unchanged keeps its review status and note;
memory/contracts/api.md:9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
memory/contracts/api.md:23:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
memory/contracts/api.md:29:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected` |
memory/contracts/api.md:74:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
memory/contracts/api.md:97:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`.
memory/contracts/api.md:212:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
memory/contracts/api.md:214:## POST /api/cases/{token}/records/{rid}/confirm_date
memory/contracts/api.md:227:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
memory/contracts/api.md:259:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported". There is no bulk accept.
memory/contracts/api.md:477:| `DATE_AMBIGUOUS` / `DATE_MISSING` | needs_review | date has two readings or is absent; excluded from gap math until confirmed |
74:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
259:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported". There is no bulk accept.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:24.619Z

**tool call — Bash**
````
{
 "command": "sed -n 165,260p app/backend/review.py; sed -n 25,70p app/backend/pipeline.py; cat tests/unit/test_date_unconfirmed.py | head -80; sed -n 210,230p memory/contracts/api.md; git status --short | head -20"
}
````

### User / tool · 2026-11-02T03:08:24.748Z

**tool result**
````
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    return [{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": item["id"]}] \
        if ladder_verdict == "unavailable" else []


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
    if row is None:
        raise ReviewError(404, "not_found", message="No such record.")
    rec = DB._decode(row)
    if rec["date_status"] != "ambiguous":
        raise _bad("Only a record whose date can be read two ways can be confirmed.")
    if date_iso not in (rec["date_candidates"] or []):
        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved = None
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso)
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    log_id = moved["id"] if moved else None
    if log_id:
        DB.apply_review(conn, log_id, "confirm_date", now=t, case=case_id)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _recompute_gaps(conn, case_id, t):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002)."""
    from app.backend import pipeline as PL
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
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
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == record_id), None)
    if rec is None:
        raise ReviewError(404, "not_found", message="No such record.")
    if rec.get("duplicate_of"):
        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
    if live:
        raise _bad("This record already has an entry; edit that entry instead.")
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
def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
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
"""D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'."""
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import run_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def undated_case(c):
    t = run_case(c, G.raw("case_01_date_formats"))
    g = c.get(f"/api/cases/{t}").json()
    rec = [r for r in g["records"] if r["date_status"] == "ambiguous"][0]
    und = [e for e in g["undated_entries"] if rec["id"] in e["record_ids"]]
    assert und, "case_01 must have an undated entry for the ambiguous record"
    return t, g, rec, und[0]


def snapshot(db, t):
    conn = DB.connect(db)
    out = {k: [(i["id"], i["review_status"]) for i in DB.list_items(conn, t, k)] for k in ("entry", "amount", "flag")}
    n = len(DB.list_events(conn, t))
    conn.close()
    return out, n


def test_single_accept_and_edit_on_undated_entry_is_422_and_changes_nothing(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    before = snapshot(db, t)
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "edit", "edits": {"summary": e["summary"] + " "}})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    assert snapshot(db, t) == before
    # dismiss and reset stay available: the entry can be moved out of the letter
    assert c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "dismiss"}).status_code == 200


def test_batch_with_one_undated_entry_is_422_and_applies_nothing(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    dated_ok = [x["id"] for x in g["entries"] if x["state"] == "verified" and x["review_status"] == "pending"][:2]
    assert dated_ok
    before = snapshot(db, t)
    r = c.post(f"/api/cases/{t}/review/batch", json={"action": "accept", "item_ids": dated_ok + [e["id"]]})
    assert r.status_code == 422 and r.json()["error"]["code"] == "DATE_UNCONFIRMED"
    assert {"id": e["id"], "reason": "date_unconfirmed"} in r.json()["error"]["detail"]["rejected"]
    assert snapshot(db, t) == before


def test_accept_works_after_confirm_date_and_letter_has_no_date_not_stated(env):
    db, c = env
    t, g, rec, e = undated_case(c)
    assert c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"}).status_code == 422
    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 200
    r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "accepted"
    letter = c.get(f"/api/cases/{t}/export").json()["letter_text"]
    assert "date not stated" not in letter.lower()


def test_export_never_puts_an_undated_accepted_entry_in_the_letter(env):
    """Defence in depth: an entry accepted before D-041 (or by a direct DB write) still stays out of the treatment section."""
    db, c = env
    t, g, rec, e = undated_case(c)
    conn = DB.connect(db)
    DB.apply_review(conn, e["id"], "accept", now=1.0, case=t)        # bypasses the HTTP rule on purpose
    conn.close()
    ex = c.get(f"/api/cases/{t}/export").json()
}
```
(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.

## POST /api/cases/{token}/records/{rid}/confirm_date
Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot be confirmed; it stays excluded and flagged. Request:
```json
{ "date": "2026-05-04" }
```
Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
```json
{ "record": {"id": "r8", "date_iso": "2026-05-04", "date_status": "confirmed", "date_raw": "04/05/2026"},
  "entry": {"id": "e8", "date": "2026-05-04", "moved_from": "undated_entries"},
  "gap_flags": [],
  "removed_flag_ids": ["f_warn_date_r8"],
  "dates_to_confirm": [], "warnings": [] }
```
`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.

## GET /api/cases/{token}/items/{item_id}  — "Why?"
Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
 M board/cards/T-065.md
 M board/cards/T-066.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:27.565Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p app/backend/confidence.py; grep -n \"def apply_review\" -A40 app/db/db.py | head -80; grep -n \"def update_item\" -A25 app/db/db.py; grep -n \"def add_event\\|def log_event\\|review_events\" app/db/db.py | head"
}
````

### User / tool · 2026-11-02T03:08:27.674Z

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


def compose_state(ladder: dict, context: dict = None):
    ctx = context or {}
    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
    if bad:      # a misspelled key must not fail open to 'verified'
        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
    rejected, doubts = [], []
    for c in ladder.get("grounding_failures", []) or []:
        rejected.append(_known(c))
    if ladder.get("schema_valid", True) is False:
        rejected.append("SCHEMA_INVALID")
    for c in ladder.get("code_reasons", []) or []:
        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
    doubts.append(_lookup(_AGREE, ctx.get("agreement"), none_ok=("both",)))
    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
        if ctx.get(key):
            doubts.append(code)
    rejected = list(dict.fromkeys(rejected))
    doubts = list(dict.fromkeys(d for d in doubts if d))
    if rejected:
        return "rejected", rejected + doubts       # the rejecting reasons come first; the item still shows every doubt
    return ("needs_review", doubts) if doubts else ("verified", [])
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
180-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
181-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
182-    if action not in ACTIONS:
183-        raise ValueError(f"invalid review action {action!r}")
184-    table, row = _find(conn, item_id, case)
185-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
186-    status = ACTIONS[action] or row["review_status"]
187-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
188-    if action == "edit" and not new_edited:
189-        raise ValueError("edit requires a non-empty edited payload")
190-    after = {"review_status": status, "edited": new_edited}
191-    conn.execute("BEGIN")
192-    try:
193-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
194-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
195-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
196-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
197-        conn.execute("COMMIT")
198-    except Exception:
199-        conn.execute("ROLLBACK")
200-        raise
201-    return get_item(conn, item_id, row["case_id"])
202-
203-
204-def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
205-    if status not in REVIEW_STATUSES:
206-        raise ValueError(f"invalid review_status {status!r}")
207-    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
208-    apply_review(conn, item_id, action, edited=edited, now=now, case=case)
209-
210-
211-def list_events(conn, case_id: str, item_id: str = None) -> list:
212-    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
213-    if item_id:
214-        q, a = q + " AND item_id=?", a + [item_id]
215-    return [_decode(r) for r in conn.execute(q + " ORDER BY at, rowid", a)]
216-
217-
218-def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
219-    """One row per attempt. `prompt` is the user text; prompt_sha256 covers system+user unless supplied."""
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
177-
178-
179-def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
180-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
181-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
182-    if action not in ACTIONS:
183-        raise ValueError(f"invalid review action {action!r}")
184-    table, row = _find(conn, item_id, case)
185-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
186-    status = ACTIONS[action] or row["review_status"]
187-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
188-    if action == "edit" and not new_edited:
189-        raise ValueError("edit requires a non-empty edited payload")
5:- review_status is written ONLY by apply_review() (which logs before/after to review_events); set_review_status() wraps it.
24:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
32:SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
180:    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
195:        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
212:    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:27.957Z

**tool call — Bash**
````
{
 "command": "grep -n \"state_reasons\\|\\\"reasons\\\"\\|'reasons'\\|why\" app/backend/present.py | head -30"
}
````

### User / tool · 2026-11-02T03:08:28.047Z

**tool result**
````
4:from app.backend import confidence, grounding, pdf_text, sentences, store, totals as T, why
11:def _why(reasons):
15:            out.append(why.why(c))
36:    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
152:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
166:def why_view(conn, case_id, item_id):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:31.160Z

**tool call — Bash**
````
{
 "command": "grep -n \"ACTIONS\" app/db/db.py | head -3; grep -n \"review_events\" -B1 -A12 app/db/schema.sql | head -40; grep -n \"state_reasons\" app/db/db.py | head; grep -n \"confirm_date\" tests/unit/*.py | head"
}
````

### User / tool · 2026-11-02T03:08:31.269Z

**tool result**
````
18:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
182:    if action not in ACTIONS:
186:    status = ACTIONS[action] or row["review_status"]
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
tests/unit/test_api_routes.py:1:"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
tests/unit/test_api_routes.py:142:def test_confirm_date_case_01(env):
tests/unit/test_api_routes.py:148:    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": "2026-06-06"}).status_code == 422
tests/unit/test_api_routes.py:149:    r = c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]})
tests/unit/test_api_routes.py:155:    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 422
tests/unit/test_api_routes.py:156:    assert any(e["action"] == "confirm_date" for e in c.get(f"/api/cases/{t}/audit").json()["events"])
tests/unit/test_date_unconfirmed.py:1:"""D-041 (T-076): an entry with no confirmed date cannot be accepted (single, edit, batch) until confirm_date; the letter never says 'date not stated'."""
tests/unit/test_date_unconfirmed.py:62:def test_accept_works_after_confirm_date_and_letter_has_no_date_not_stated(env):
tests/unit/test_date_unconfirmed.py:66:    assert c.post(f"/api/cases/{t}/records/{rec['id']}/confirm_date", json={"date": rec["date_candidates"][0]}).status_code == 200
tests/unit/test_date_unconfirmed.py:85:def test_confirm_date_then_batch_accepts(env):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:33.775Z

**tool call — Bash**
````
{
 "command": "grep -n \"INSERT INTO review_events\\|add_event\\|'not_duplicate'\\|\\\"not_duplicate\\\"\\|keep_my_wording\" app/backend/*.py app/db/db.py | head; sed -n 15,22p app/db/db.py; sed -n 1,16p app/backend/review.py"
}
````

### User / tool · 2026-11-02T03:08:33.870Z

**tool result**
````
app/backend/export.py:121:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
app/backend/review.py:3:Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
app/backend/review.py:5:and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
app/backend/review.py:161:        DB.apply_review(conn, item["id"], "keep_my_wording", now=t, case=case_id)
app/backend/review.py:286:        DB.apply_review(conn, eid, "keep_my_wording", now=t, case=case_id)
app/backend/review.py:344:    DB.apply_review(conn, entry_id, "not_duplicate", now=t, case=case_id)
app/backend/store.py:70:    events = [dict(type=ev["action"], item_id=ev["item_id"]) for ev in DB.list_events(conn, case_id) if ev["action"] == "keep_my_wording"]
app/db/db.py:19:           "confirm_date": None, "keep_my_wording": None,
app/db/db.py:20:           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
app/db/db.py:195:        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",

RETENTION_SECONDS = 24 * 3600
REVIEW_STATUSES = ("pending", "accepted", "edited", "dismissed")
ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
           "confirm_date": None, "keep_my_wording": None,
           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
"""Human review decisions and edit re-check (R-RV-2, R-RV-3, R-CH-5, R-CH-7, R-IN-5; D-010, D-011, D-012; ADR-005).

Only DB.apply_review writes review_status (accept, edit, dismiss, reset, confirm_date, keep_my_wording events). There is no bulk accept.
Edit order: (1) structure, else 422 invalid_edit; (2) code token check; (3) judge 1 re-run. A token/judge objection saves nothing
and returns 409 needs_confirm unless `confirm_warnings` is true (then it is saved and a keep_my_wording event is logged). A judge
that cannot answer never blocks: the edit is saved as needs_review with JUDGE_UNAVAILABLE.
"""
import time

from app.backend import amounts as AM, conflicts, confidence, gaps, generator, grounding, judges, store
from app.db import db as DB

ACTIONS = ("accept", "dismiss", "reset", "edit")
_NUMERIC_TOKEN = __import__("re").compile(r"\d|^(?:january|february|march|april|may|june|july|august|september|october|november|december)$", __import__("re").IGNORECASE)
_KIND = {"e": "entry", "a": "amount", "f": "flag"}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:41.010Z

**tool call — Bash**
````
{
 "command": "sed -n 1,54p app/db/schema.sql; grep -n \"DATE_AMBIGUOUS\\|date_status\" app/backend/pipeline.py app/backend/store.py app/backend/amounts.py | head -20"
}
````

### User / tool · 2026-11-02T03:08:41.114Z

**tool result**
````
-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
-- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
-- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
  raw_text TEXT NOT NULL, text_sha256 TEXT,
  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
);
CREATE TABLE IF NOT EXISTS records (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
  date_header_start INTEGER, date_header_end INTEGER, source_header_start INTEGER, source_header_end INTEGER,
  source_label TEXT, date_raw TEXT, date_iso TEXT,
  date_status TEXT CHECK (date_status IN ('parsed','ambiguous','missing','confirmed')),
  date_candidates_json TEXT, duplicate_of TEXT, injection_tag INTEGER DEFAULT 0, encounter INTEGER DEFAULT 1,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS entries (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
  provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS amounts (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
  text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS flags (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
-- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
CREATE TABLE IF NOT EXISTS llm_calls (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
  parsed_ok INTEGER, verdict TEXT, attempt INTEGER DEFAULT 1, latency_ms INTEGER, cost_usd REAL,
  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
);
app/backend/pipeline.py:40:    dates = {rec_by_n[n].get("date_status") for n in nos if n in rec_by_n}
app/backend/pipeline.py:41:    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
app/backend/pipeline.py:42:        ctx["date_status"] = "ambiguous"
app/backend/pipeline.py:76:        ctx = {"llm_split": True} if w["category"] == "llm_split" else {"injection": inj, "date_status": None if inj else "ambiguous"}
app/backend/pipeline.py:157:                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
app/backend/pipeline.py:278:    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:44.750Z

**tool call — bash_placeholder**
````
{}
````

### User / tool · 2026-11-02T03:08:44.752Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash_placeholder</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:08:52.941Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\nold=s[s.index(\"    conn.execute(\\\"UPDATE records SET date_iso=?, date_status='confirmed'\"):s.index(\"    from app.backend import present\\n    return {\\\"record\\\": {\\\"id\\\": record_id, \\\"date_iso\\\": date_iso, \\\"date_status\\\": \\\"confirmed\\\"\")]\nnew='''    conn.execute(\"UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?\", (date_iso, record_id, case_id))\n    moved, cleared = None, []\n    for e in DB.list_items(conn, case_id, \"entry\"):\n        if record_id in (e[\"record_ids\"] or []):\n            DB.update_item(conn, e[\"id\"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))\n            if \"DATE_AMBIGUOUS\" in (e.get(\"state_reasons\") or []):\n                cleared.append(e[\"id\"])\n            moved = {\"id\": e[\"id\"], \"date\": date_iso, \"moved_from\": \"undated_entries\"}\n    for a in DB.list_items(conn, case_id, \"amount\"):\n        if record_id in (a[\"record_ids\"] or []) and \"DATE_AMBIGUOUS\" in (a.get(\"state_reasons\") or []):\n            DB.update_item(conn, a[\"id\"], now=t, case=case_id, **_without_date_doubt(a))\n            cleared.append(a[\"id\"])\n    removed = _drop(conn, case_id, f\"f_date_r{rec['seq']}\")\n    removed += _recompute_gaps(conn, case_id, t)\n    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.\n    _log_confirm_date(conn, case_id, moved[\"id\"] if moved else record_id, rec, date_iso, cleared, t)\n'''\ns=s.replace(old,new)\ns=s.replace('''def _drop(conn, case_id, flag_id):''','''def _without_date_doubt(item: dict) -> dict:\n    \"\"\"The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)\n    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected.\"\"\"\n    reasons = [c for c in (item.get(\"state_reasons\") or []) if c != \"DATE_AMBIGUOUS\"]\n    state = item[\"state\"]\n    if state == \"needs_review\" and not reasons:\n        state = \"verified\"\n    return {\"state\": state, \"state_reasons_json\": reasons}\n\n\ndef _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):\n    after = {\"date_chosen\": date_iso, \"date_raw\": rec[\"date_raw\"], \"candidates\": rec[\"date_candidates\"], \"record_id\": rec[\"id\"],\n             \"cleared_date_ambiguous\": cleared}\n    before = {\"date_status\": \"ambiguous\", \"date_iso\": rec.get(\"date_iso\")}\n    conn.execute(\"INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)\",\n                 (DB._tok(\"v\"), case_id, item_id, \"confirm_date\", DB._enc(before), DB._enc(after), t))\n\n\ndef _drop(conn, case_id, flag_id):''',1)\ns=s.replace(\"There is no bulk accept.\",\"Batch accept (verified, dated, pending entries only) goes through `batch_review`, which also uses apply_review.\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"def batch\\|^def \" app/backend/review.py | head -30; grep -n \"def _tok\\|def _enc\" app/db/db.py; sed -n 195,215p app/backend/review.py"
}
````

### User / tool · 2026-11-02T03:08:53.091Z

**tool result**
````
24:def _now(now):
28:def _item(conn, case_id, item_id):
38:def _bad(msg, **detail):
42:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
54:def _date_unconfirmed_error():
59:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
81:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, body):
117:def _edit(conn, case_id, kind, item, body, call, t):
173:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
205:def _without_date_doubt(item: dict) -> dict:
215:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
223:def _drop(conn, case_id, flag_id):
228:def _recompute_gaps(conn, case_id, t):
269:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
318:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
374:def _upsert(conn, case_id, kind, item, t):
384:def judges_for(dollars, call, case_text):
390:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
62:def _tok(prefix: str) -> str:
66:def _enc(v):
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    removed += _recompute_gaps(conn, case_id, t)
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
            "removed_flag_ids": removed, "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    return {"state": state, "state_reasons_json": reasons}


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:04.497Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace(\"Batch accept (verified, dated, pending entries only) goes through `batch_review`, which also uses apply_review.\",\"Batch accept (verified, dated, pending entries only) writes through apply_review too.\")\ns=s.replace('''    return {\"state\": state, \"state_reasons_json\": reasons}''','''    out = {\"state\": state, \"state_reasons_json\": reasons}\n    if isinstance(item.get(\"ladder\"), dict):\n        out[\"ladder\"] = {**item[\"ladder\"], \"state\": state}\n    return out''')\nopen(p,'w').write(s)\np='memory/contracts/api.md'\ns=open(p).read()\ns=s.replace(\" There is no bulk accept.\",\"\",1)\ns=s.replace(\"Logged as a `confirm_date` event.\",\"Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally.\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"bulk accept\" memory/contracts/api.md; cat >> tests/unit/test_date_unconfirmed.py <<'EOF'\n\n\ndef test_confirm_date_clears_date_ambiguous_on_entry_and_logs_chosen_date(env):\n    \"\"\"T-076 r2 (paralegal F1): after confirm the entry no longer says 'two ways' / needs_review, and the audit names the chosen date.\"\"\"\n    db, c = env\n    t, g, rec, e = undated_case(c)\n    assert \"DATE_AMBIGUOUS\" in e[\"reasons\"] and e[\"state\"] == \"needs_review\"\n    chosen = rec[\"date_candidates\"][0]\n    assert c.post(f\"/api/cases/{t}/records/{rec['id']}/confirm_date\", json={\"date\": chosen}).status_code == 200\n    item = c.get(f\"/api/cases/{t}/items/{e['id']}\").json()\n    grid = c.get(f\"/api/cases/{t}\").json()\n    ent = next(x for x in grid[\"entries\"] if x[\"id\"] == e[\"id\"])\n    assert \"DATE_AMBIGUOUS\" not in ent[\"reasons\"] and \"two ways\" not in ent[\"why\"]\n    assert ent[\"state\"] != \"needs_review\" or ent[\"reasons\"]          # needs_review only if another doubt remains\n    assert not any(x[\"id\"] == e[\"id\"] for x in grid[\"undated_entries\"])\n    assert next(r for r in grid[\"records\"] if r[\"id\"] == rec[\"id\"])[\"date_status\"] == \"confirmed\"\n    assert item is not None\n    r = c.post(f\"/api/cases/{t}/items/{e['id']}/review\", json={\"action\": \"accept\"})\n    assert r.status_code == 200\n    ent = next(x for x in c.get(f\"/api/cases/{t}\").json()[\"entries\"] if x[\"id\"] == e[\"id\"])\n    assert ent[\"review_status\"] == \"accepted\" and \"DATE_AMBIGUOUS\" not in ent[\"reasons\"] and \"two ways\" not in ent[\"why\"]\n    ev = [x for x in c.get(f\"/api/cases/{t}/audit\").json()[\"events\"] if x[\"action\"] == \"confirm_date\"]\n    assert len(ev) == 1 and ev[0][\"after\"][\"date_chosen\"] == chosen and ev[0][\"after\"][\"cleared_date_ambiguous\"] == [e[\"id\"]]\n\n\ndef test_confirm_date_keeps_other_doubts_and_rejected_state():\n    from app.backend.review import _without_date_doubt as w\n    assert w({\"state\": \"needs_review\", \"state_reasons\": [\"DATE_AMBIGUOUS\"]}) == {\"state\": \"verified\", \"state_reasons_json\": []}\n    assert w({\"state\": \"needs_review\", \"state_reasons\": [\"DATE_AMBIGUOUS\", \"JUDGE_UNSURE\"]}) == {\"state\": \"needs_review\", \"state_reasons_json\": [\"JUDGE_UNSURE\"]}\n    assert w({\"state\": \"rejected\", \"state_reasons\": [\"SCHEMA_INVALID\", \"DATE_AMBIGUOUS\"]}) == {\"state\": \"rejected\", \"state_reasons_json\": [\"SCHEMA_INVALID\"]}\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:09:26.971Z

**tool result**
````
        assert next(r for r in grid["records"] if r["id"] == rec["id"])["date_status"] == "confirmed"
        assert item is not None
        r = c.post(f"/api/cases/{t}/items/{e['id']}/review", json={"action": "accept"})
        assert r.status_code == 200
        ent = next(x for x in c.get(f"/api/cases/{t}").json()["entries"] if x["id"] == e["id"])
        assert ent["review_status"] == "accepted" and "DATE_AMBIGUOUS" not in ent["reasons"] and "two ways" not in ent["why"]
        ev = [x for x in c.get(f"/api/cases/{t}/audit").json()["events"] if x["action"] == "confirm_date"]
>       assert len(ev) == 1 and ev[0]["after"]["date_chosen"] == chosen and ev[0]["after"]["cleared_date_ambiguous"] == [e["id"]]
                                ^^^^^^^^^^^^^^
E       KeyError: 'after'

tests/unit/test_date_unconfirmed.py:116: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_date_unconfirmed.py::test_confirm_date_clears_date_ambiguous_on_entry_and_logs_chosen_date
1 failed, 997 passed in 21.57s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:29.195Z

**tool call — Bash**
````
{
 "command": "grep -n \"events\" app/backend/api.py | head; .venv/bin/python - <<'EOF'\nEOF\ngrep -n \"def _decode\" -A12 app/db/db.py | head -20"
}
````

### User / tool · 2026-11-02T03:09:29.311Z

**tool result**
````
144:def _decode(row) -> dict:
145-    out = {}
146-    for k in row.keys():
147-        v = row[k]
148-        if k.endswith("_json"):
149-            out[k[:-5]] = json.loads(v) if v else None
150-        else:
151-            out[k] = v
152-    return out
153-
154-
155-def get_item(conn, item_id: str, case: str = None) -> dict:
156-    return _decode(_find(conn, item_id, case)[1])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:30.323Z

Keys are `before`/`after`... the error says `after` missing; check the audit shape.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:30.904Z

**tool call — Bash**
````
{
 "command": "grep -rn \"\\\"events\\\"\" app/backend/*.py | head -5; grep -n \"events\" memory/contracts/api.md | head -5"
}
````

### User / tool · 2026-11-02T03:09:30.996Z

**tool result**
````
app/backend/export.py:121:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
app/backend/present.py:179:    return {"item": item, "source": src, "calls": calls, "events": events}
app/backend/present.py:200:            "events": [{"id": e["id"], "item_id": e["item_id"], "action": e["action"], "at": store.iso(e["at"]),
20:| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
31:| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
74:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
84:Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
243:  "events": [ {"action": "accept", "at": "2026-11-02T01:05:00Z"} ] }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:32.262Z

**tool call — Bash**
````
{
 "command": "sed -n 195,206p app/backend/present.py"
}
````

### User / tool · 2026-11-02T03:09:32.362Z

**tool result**
````
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:09:35.192Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_date_unconfirmed.py'\ns=open(p).read()\ns=s.replace('''    ev = [x for x in c.get(f\"/api/cases/{t}/audit\").json()[\"events\"] if x[\"action\"] == \"confirm_date\"]\n    assert len(ev)''','''    conn = DB.connect(db)\n    ev = [x for x in DB.list_events(conn, t) if x[\"action\"] == \"confirm_date\"]\n    conn.close()\n    assert len(ev)''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -4\nB=\"python3 tools/board.py\"; $B show T-060 | head -5; git status --short app/backend memory/contracts tests/unit | head"
}
````

### User / tool · 2026-11-02T03:09:57.110Z

**tool result**
````
........................................................................ [ 86%]
........................................................................ [ 93%]
..............................................................           [100%]
998 passed in 21.09s
---
id: "T-060"
title: "Enterprise UI/UX polish: multi-pass review against real-world legal/claims products (Chris request)"
milestone: "M3"
role: "frontend"
 M app/backend/review.py
 M memory/contracts/api.md
 M tests/unit/test_date_unconfirmed.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:10:02.798Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"\ngit commit -q -m \"fix(backend): confirm_date clears DATE_AMBIGUOUS on the entry, logs chosen date; api.md bulk-accept wording (T-076 r2)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/review.py memory/contracts/api.md tests/unit/test_date_unconfirmed.py && SHA=$(git rev-parse --short HEAD) && echo $SHA\n$B commit T-076 --sha $SHA --agent backend\n$B note T-060 --agent backend --text \"For frontend (from T-076 paralegal review): Edit is enabled on undated rows (undated_entries). Edit implies accept, so the server returns 422 DATE_UNCONFIRMED. Disable Edit (and Accept) on undated rows until confirm_date; show 'Confirm the date first'. Also: after confirm_date the entry now has DATE_AMBIGUOUS cleared from reasons and state recomputed, so rows no longer say 'two ways' once confirmed.\"\n$B ac T-076 --check 1 --agent backend --evidence \"tests/unit/test_date_unconfirmed.py::test_confirm_date_clears_date_ambiguous_on_entry_and_logs_chosen_date passes; full tests/unit 998 passed\" 2>&1 | tail -2\n$B handoff T-076 --agent backend --text \"Round 2. What changed: confirm_date now removes DATE_AMBIGUOUS from the entry's (and any amount's) reasons, recomputes state (verified unless another doubt remains; rejected stays), and writes a confirm_date review event whose after_json has date_chosen, date_raw, candidates, cleared ids; api.md 'no bulk accept' removed and confirm_date section updated. Verified: .venv/bin/python -m pytest -q tests/unit -> 998 passed. Left: frontend note posted on T-060 (Edit enabled on undated rows). Surprise: audit endpoint shows before/after only in local mode, so the test reads DB.list_events.\"\n$B move T-076 in_review --agent backend"
}
````

### User / tool · 2026-11-02T03:10:03.351Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
f4ef2ea
T-076: commit f4ef2ea recorded
noted on T-060
AC 1 checked: tests/unit/test_date_unconfirmed.py::test_confirm_date_clears_date_ambiguous_on_entry_and_logs_chosen_date passes; full tests/unit 998 passed
handoff written on T-076
T-076: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:10:08.302Z

T-076 round 2 is fixed and in review (commit f4ef2ea): `confirm_date` now clears DATE_AMBIGUOUS from the entry and recomputes its state, so after confirming it no longer reads "Needs review" or "two ways". It also logs a `confirm_date` event holding the chosen date. The api.md "no bulk accept" sentence is gone, and the Edit-on-undated-rows note for the frontend is posted on T-060. `tests/unit` passes (998 tests).

One thing you might trip over: the audit endpoint only shows an event's chosen date in local mode, so the new test reads the events from the database directly.
