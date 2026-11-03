# Subagent: Backend: T-116 gap endpoint rule (Backend: T-116 gap endpoint rule)

Source: `agent-af4cd016c02b6a964.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T09:29:43.806Z

You own board card T-116 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-116` and read the gap finding in reviews/T-060-paralegal-pass1.md and the T-114 handoff (`python3 tools/board.py show T-114`).

In app/backend/gaps.py, only treatment encounters may start or end a treatment gap. Intake forms, records requests, billing statements, ledgers, EOBs, affidavits, narrative letters and records reviews are excluded. Detect the record type in code, from headers or labels and the record-format research in research/record-formats.md. Show the exclusion in the gap's "why" ("intake form on 03/05 is not a treatment visit"). Re-check lib09 and the golden cases.

If any golden expected gap changes, post the exact lines on the card for qa; don't edit evals/golden. Run `python -m evals.run` with the fixture backend: gap flag precision and recall must not drop. Run `.venv/bin/python -m pytest -q tests/unit`. Commit with the pathspec rule or a fresh temp index, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-116 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T09:29:43.811Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:46.240Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-116; python3 tools/board.py show T-114 | tail -30; grep -n -i -B2 -A12 \"gap\" reviews/T-060-paralegal-pass1.md | head -80"
}
````

### User / tool · 2026-11-02T09:29:46.436Z

**tool result**
````
---
id: "T-116"
title: "Gap rule: an intake form or other administrative record never ends a treatment gap"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:29:33Z"
updated_at: "2026-11-02T09:29:39Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:29:39Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "gaps.py treats only treatment encounters as gap endpoints; intake forms, records requests, billing statements and affidavits are excluded (by code-detected record type), with the exclusion shown in the gap's why; lib09 and golden cases re-checked; tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:29:39Z backend: claimed

## Handoff (filled when moving to in_review)

id: "T-114"
title: "Backend items from T-060 pass 1: rate rows must not offer an accept that later blocks export; demo has judge fixtures for every acceptable lib09 item; gap recompute after a date confirm is reported"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:21:16Z"
updated_at: "2026-11-02T09:29:33Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:21:17Z"
rounds: 0
commits: ["b5fb35c"]
reviews: []
ac:
  - {"n": 1, "text": "An amount classified rate is not accept-able into the letter (or accepting it needs no judge), so it can never create a JUDGE_NOT_RUN export block; every item a paralegal can accept on the demo library packets has its judge fixture (no demo dead end); confirm_date returns which gap figures changed (old->new) so the UI can say so; tests", "done": true, "evidence": "tests/unit/test_t114_rates_and_demo_judges.py: rate accepted without judge is not a JUDGE_NOT_RUN blocker (charge still is); accept_effect/judge_required_for_export on amounts; all 15 library packets walked in fixture mode with zero JUDGE_NOT_RUN (lib09 rate judge fixtures 7328ae58..., 75686283... recorded via claude-cli, 2 calls); confirm_date gap_changes lib09 42->40"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:21:17Z backend: claimed
- 2026-11-02T09:27:55Z backend: AC 1 checked: tests/unit/test_t114_rates_and_demo_judges.py: rate accepted without judge is not a JUDGE_NOT_RUN blocker (charge still is); accept_effect/judge_required_for_export on amounts; all 15 library packets walked in fixture mode with zero JUDGE_NOT_RUN (lib09 rate judge fixtures 7328ae58..., 75686283... recorded via claude-cli, 2 calls); confirm_date gap_changes lib09 42->40
- 2026-11-02T09:29:25Z backend: moved in_progress -> in_review
- 2026-11-02T09:29:33Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed: a rate (D-019/D-042) is acknowledge-only: amounts carry accept_effect + judge_required_for_export=false, trace.judge_not_run_blockers skips them (gate and GET /export agree), item trace says the check is optional; confirm_date returns gap_changes[] (lib09 r4 -> 5 Mar: 42 -> 40 days, with a sentence); lib09 rate judge fixtures (a3, a6) recorded with claude-cli (2 calls, 1 attempt each). How verified: tests/unit/test_t114_rates_and_demo_judges.py (20 tests incl. all 15 library packets walked, no JUDGE_NOT_RUN); full tests/unit 2491 pass before two test_trace updates for rates, which now pass (105 in test_trace+t114). Left: F4 'an intake form never ends a gap' is NOT done (gaps.py has no such rule; needs its own card); estimate/unclear accepts still need a judge; frontend note on T-060. Surprised: only the two lib09 rate judges were missing across all 15 packets.

53-Acceptance test: on lib09 the two Rate rows show Accept disabled (or a different label) with the reason text; accepting every enabled item leaves "Ready to export".
54-
55:**F4. The gap number changes silently when a date is confirmed (checklist 6, trust).** Evidence: `25c-gap-42-before-confirm.png` shows "Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026". After I confirmed record 4 (an intake form, "formulario de admisión (OCR)") as March 5, `25e-gap-40-after-confirm.png` reads "Gap of 40 days between March 5, 2026 (…formulario de admisión (OCR)) and April 14, 2026", and the accepted flag in the internal notes carries the same text (`task2-export-notes.txt`). `evals/library/case_lib09_spanish_interpreter_espalda.expected.json` lists `gap_excluded_records: [4, 7]` and a 42-day gap.
56-Why it matters: the adjuster counts days between treatment encounters; an intake form is paperwork. The figure moved with no note telling me why.
57:Fix: backend card: an intake or billing form never starts or ends a gap, even after its date is confirmed. UI: if a flag's figures change after a decision, say so ("Gap recalculated after you confirmed record 4: now 40 days").
58:Acceptance test: lib09 after confirming record 4 still shows "Gap of 42 days" ending at record 2, and the intake record is not named as an endpoint.
59-
60-**F5. Charges and unclear amounts are too tall to reconcile.** Evidence: `14b-unclear.png`. Five unclear rows at about 400 px each (1,958 px for the tray). The whole 400-character excerpt wraps in a column about 215 px wide, the amount inside it is not highlighted, and the same two sentences of Spanish-record boilerplate ("AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.") repeat in every row. The status text "unclear; not a bill; needs review" sits beside a quote that says "Consulta: $650.00".
61-Why it matters: reconciling billed charges is my Excel step; this table makes me read the same paragraph five times to find a number.
62-Fix: one row per amount (about 56 px): amount | provider and date | the 8 words around the amount with the amount highlighted | status | actions; the full quote in a drawer or the sticky source pane; the Spanish notice once at the top of the tray; plain status words ("Not counted: can't tell if this is a bill").
63-Acceptance test: lib09 unclear tray height under 700 px; the boilerplate string appears once; the highlighted amount equals the Amount cell on every row.
64-
65-### Minor
66-
67-**F6. Timeline row density.** `22b-public-timeline.png`: two rows per 900 px viewport. Each row repeats the same fact twice (summary, then italic quote) and carries seven buttons (Why?, Open record, Change quote, Accept, Edit, Dismiss, Audit), and Accept stays full blue after it is accepted (`24a-final-accept-viewport.png`). Fix: a compact row of date | provider | summary | quote on hover or click | state chip | one Accept; the secondary actions behind a "..." menu; accepted rows collapse to one line. Test: 8 rows visible in one 900 px screen on case_01.
68-
69-**F7. The "Verified" chip and the "Accept all verified" button invite trust.** The green "Verified" chip means code found the quote; to me "verified" means a person checked it, and the export rules say no "verified" labels in the letter. The first big blue button above the rows is "Accept all verified entries (7)" and one `Shift+A` accepted 8 entries without my looking at any (`06b-after-shiftA.png`). Undo (`Undo last batch (8)`) exists, which is good. Fix: rename the chip "Quote matches record"; label the batch button with a count of rows I have actually opened ("Accept 7 rows you haven't opened"). Test: chip text is not "Verified"; button copy names what is being accepted.
70-
--
85-2. F3 do not offer Accept where acceptance blocks export; recovery must not be a dead end.
86-3. F2 plain "To do" strip above the timeline; needs-review rows first; amber decision icon.
87:4. F4 gap must not move to the intake date; tell me when a figure changes.
88-5. F5 one-line unclear and charge rows; amount highlighted; boilerplate once.
89-6. F8 sticky "N left · Export", letter box sized to its text, Bates fields above it, .txt/.docx download.
90-7. F6 compact timeline rows (8+ per screen); actions behind a menu.
91-8. F7 rename "Verified"; honest wording on batch accept.
92-9. F12 one currency format, US long dates, single messages, disable Edit and Dismiss on undated rows.
93-10. F10 collapse the dev library and case list; scroll to the case after load; restore scroll on reload.
94-(F9, F11 and F13 follow after these.)
95-
96-## Right already
97-- Sticky source pane highlights the quoted words and follows the selected row; this is the fastest way I have seen to check a claim.
98-- Edit keeps the original visible ("Edited by you. Original: …") and review state survives a refresh.
99-- Export copy is clean plain text, the dismissed flag is absent from the letter, and the letter total reads "Billed charges stated in these records: $5,090.00" with unclear amounts only in the internal notes.
--
109-  {"severity": "major", "title": "Needs-review items not first; hand-off hidden in a collapsed stepper", "evidence": "22b-public-timeline.png; 01-after-analyze-full.png; 04-stepper.png; 05-stepper-open.png; bar text '6/10 checks passed - 4 need you - Export blocked by 1'", "why_it_matters": "Checklist 16: the first screen does not say what blocks export", "fix": "Plain 'To do' strip above the timeline with jump controls; needs-review rows first; amber decision icon not red X", "acceptance_test": "case_01: before scrolling the page shows 'Confirm the date for record 8' with a working jump; first timeline row is Needs review"},
110-  {"severity": "major", "title": "Accept offered where acceptance blocks export; recovery is a dead end", "evidence": "18b-all-reviewed.png; 19b-export-blocked.png; 19c-after-rerun.png; 'The second check still did not answer for 2 items of 2. Try again, or dismiss them.'", "why_it_matters": "I accepted what the card offered and was blocked, with no way to rerun in the demo", "fix": "Disable Accept with the reason when the second check is absent, or route to internal notes only; name the check in plain words", "acceptance_test": "lib09 Rate rows show Accept disabled with a reason; accepting every enabled item leaves Ready to export"},
111:  {"severity": "major", "title": "Gap figure changes from 42 to 40 days after confirming an intake form date", "evidence": "25c-gap-42-before-confirm.png; 25e-gap-40-after-confirm.png; task2-export-notes.txt; evals/library/case_lib09_spanish_interpreter_espalda.expected.json gap_excluded_records [4,7]", "why_it_matters": "The adjuster counts days between treatment; the intake form is paperwork and the change is unexplained", "fix": "Backend: intake and billing records never end a gap; UI: say when a figure is recalculated after a decision", "acceptance_test": "lib09 after confirming record 4 still shows Gap of 42 days ending at record 2"},
112-  {"severity": "major", "title": "Charges and unclear-amount rows are too tall to reconcile", "evidence": "14b-unclear.png; unclear tray 1,958 px for 5 rows; boilerplate repeated per row; amount not highlighted", "why_it_matters": "Reconciling billed charges is a core paralegal step and this makes it slow", "fix": "One-line rows with the amount highlighted in a short snippet; notice once per tray; plain status words", "acceptance_test": "lib09 unclear tray under 700 px; boilerplate string appears once; highlighted amount equals the Amount cell"},
113-  {"severity": "minor", "title": "Timeline rows show two entries per screen with seven buttons each", "evidence": "22b-public-timeline.png; 24a-final-accept-viewport.png", "why_it_matters": "Slows scanning; Accept stays primary after accepting", "fix": "Compact rows, secondary actions in a menu, accepted rows collapse", "acceptance_test": "8 rows visible in one 900 px screen on case_01"},
114-  {"severity": "minor", "title": "Verified chip and Accept-all button invite trust", "evidence": "06b-after-shiftA.png; 22a-public-after-analyze.png ('Accept all verified entries (7)'; Verified chip)", "why_it_matters": "Verified reads as human-checked; one key accepted 8 unopened rows", "fix": "Rename chip 'Quote matches record'; batch label says how many rows were opened", "acceptance_test": "No chip text 'Verified'; batch button copy names what is accepted"},
115-  {"severity": "minor", "title": "Export placement and finish: no done cue, 74 Shift+Tabs to Export, 418 px letter box, no download", "evidence": "24a-final-accept-viewport.png; p24-to-export.py output 74; 09-after-export-click.png; 23a-export-early.png ('The export is blocked.' twice)", "why_it_matters": "The last step of the demand workflow is hard to find and to use", "fix": "Sticky 'N left - Export' footer; letter box sized to text; Bates fields above the letter; .txt/.docx download", "acceptance_test": "After the last accept an Export control is reachable within 2 Tab presses and visible without scrolling"},
116-  {"severity": "minor", "title": "Letter repeats summary and quote; 'AI translation:' prefix printed in the letter", "evidence": "task1-export-letter.txt; task2-export-letter.txt ('AI translation: Reason for visit...'; quote 'espaIda')", "why_it_matters": "Longer letter text to edit; a UI-style label would go to the adjuster", "fix": "Optional one-line format per D-002; bracketed removable translation note", "acceptance_test": "A letter option gives one line per entry"},
117-  {"severity": "minor", "title": "Local-mode dev panel pushes the work down; result off screen after load; null case labels", "evidence": "00-landing.png; 13-lib09-loaded.png (scrollY 671 of 11,133); 20c-after-reload.png; public landing 21-public-landing.png is clean", "why_it_matters": "A reviewer using local mode starts 1,500 px from the task and cannot tell cases apart", "fix": "Collapse library under Developer tools; scroll to the case after load; real case labels; restore scroll on reload", "acceptance_test": "After loading a library case the first timeline row is in the viewport"},
118-  {"severity": "minor", "title": "o opens a modal that swallows the next key", "evidence": "17a2-modal-e2.png; app/frontend/review.js:280", "why_it_matters": "o then a silently does nothing; the sticky source pane already shows the record", "fix": "o focuses the source pane or shows 'Close the record first (Esc)'", "acceptance_test": "o then a accepts or shows a message"},
119-  {"severity": "minor", "title": "Inconsistent currency and date formats; repeated messages; Edit/Dismiss enabled on undated rows", "evidence": "24a-final-accept-viewport.png ('$310' vs '$310.00'); 03c-a-on-undated.png ('Confirm the date first' x3); 22b-public-timeline.png (ISO dates)", "why_it_matters": "Looks unfinished and the repeated text hides the one instruction", "fix": "Always show cents; US long dates; one message per state; disable Edit and Dismiss until the date is confirmed", "acceptance_test": "No dollar amount without cents in the charges panel; the undated row shows its instruction once"},
120-  {"severity": "minor", "title": "Prior-condition flag raised on an interpreter sentence", "evidence": "25d-preexisting-false-positive.png ('Hx obtained via patient's son, who interpreted.')", "why_it_matters": "Adjuster-facing noise that makes me distrust the flags", "fix": "Backend: no prior-condition flag on 'Hx obtained via ...'; UI: say when the checkers disagree", "acceptance_test": "lib09 raises no prior-condition flag"}
121- ],
122- "whats_right": ["Sticky source pane highlights the quoted words and follows the selected row", "Edit keeps the original visible and decisions survive a refresh", "Export copy is clean plain text with dismissed items absent and unclear amounts only in the internal notes"],
123: "questions_for_chris": ["Is the library and case list meant to appear in the demo build, or only in local mode?", "Should a confirmed intake-form date ever count as an encounter for the gap check?"]}
124-```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:46.975Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/gaps.py && cat app/backend/gaps.py; git status --short | head"
}
````

### User / tool · 2026-11-02T09:29:47.091Z

**tool result**
````
      71 app/backend/gaps.py
"""Treatment gaps, computed by code over code-parsed header dates of clinical-encounter records (ADR-010, D-003, R-FL-1, row 9).
Entry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).
Ambiguous or missing dates and non-encounter records (billing statements, phone notes) are never endpoints."""
from app.backend import dates, flag_templates
from app.backend.ingest import evidence_span

THRESHOLD_DAYS = 30


def is_gap(days: int) -> bool:
    return days > THRESHOLD_DAYS


def compute_gaps(records: list) -> list:
    """[{from_date, to_date, from_records, to_records, days, flag}] between consecutive DISTINCT encounter dates."""
    by_date = {}
    for r in records:
        if r.get("kind", "encounter") == "encounter" and r.get("date_iso"):
            by_date.setdefault(r["date_iso"], []).append(r["n"])
    ds = sorted(by_date)
    out = []
    for a, b in zip(ds, ds[1:]):
        n = dates.days_between(a, b)
        out.append({"from_date": a, "to_date": b, "from_records": sorted(by_date[a]), "to_records": sorted(by_date[b]),
                    "days": n, "flag": is_gap(n)})
    return out


def _reasons(gap: dict, records: list) -> list:
    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
    reasons = []
    for r in records:
        if r.get("kind", "encounter") != "encounter" or r.get("date_iso"):
            continue
        cands = r.get("date_candidates") or []
        if not cands or any(gap["from_date"] <= c <= gap["to_date"] for c in cands):
            reasons.append("ENDPOINT_NOT_VERIFIED")
            break
    ends = set(gap["from_records"]) | set(gap["to_records"])
    if any(r.get("injection_tag") for r in records if r["n"] in ends):
        reasons.append("INJECTION_SUSPECTED")
    return reasons


def gap_flags(records: list) -> list:
    """One flag per gap over 30 days, id keyed by the bounding record pair; text from flag_templates only."""
    by_n = {r["n"]: r for r in records}
    flags = []
    for g in compute_gaps(records):
        if not g["flag"]:
            continue
        a, b = g["from_records"][-1], g["to_records"][0]
        title, expl = flag_templates.render("gap", "gap_over_30", days=g["days"], from_date=g["from_date"], to_date=g["to_date"],
                                            provider_a=by_n[a].get("source"), provider_b=by_n[b].get("source"))
        ev = [evidence_span(by_n[n], f) for n in (a, b) for f in ("date", "source")]
        flags.append({"id": f"f_gap_r{a}_r{b}", "type": "gap", "category": "gap_over_30", "origin": "code", "title": title,
                      "explanation": expl, "from_date": g["from_date"], "to_date": g["to_date"], "days": g["days"],
                      "record_nos": sorted(set(g["from_records"]) | set(g["to_records"])), "evidence": ev, "reasons": _reasons(g, records)})
    return flags


def merge_flags(old: list, new: list) -> list:
    """Recompute after confirm_date: a flag whose record pair, dates and days are unchanged keeps its review status and note;
    a changed or new flag starts pending (ADR-002). Flags that no longer exist are dropped."""
    prev = {f["id"]: f for f in old}
    out = []
    for f in new:
        o = prev.get(f["id"])
        same = o and all(o.get(k) == f.get(k) for k in ("from_date", "to_date", "days"))
        out.append({**f, "review_status": o.get("review_status", "pending") if same else "pending", "note": o.get("note") if same else None})
    return out
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:49.619Z

**tool call — Bash**
````
{
 "command": "grep -rn '\"kind\"\\|kind=' app/backend/*.py | grep -v \"^app/backend/api\" | head -30; grep -n -i \"intake\\|billing\\|ledger\\|EOB\\|affidavit\\|records request\\|narrative\" research/record-formats.md | head -50; grep -rn \"gap_excluded\" evals/*.py evals/library/*.json evals/golden 2>/dev/null | head -20; ls tests/unit | grep -i gap"
}
````

### User / tool · 2026-11-02T09:29:49.737Z

**tool result**
````
app/backend/billing.py:200:def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=None):
app/backend/billing.py:202:    return {"record_no": rec["n"], "kind": kind, "why": why, "figure": fig, "excerpt": excerpt, "_at": fig["_at"], "_row": row or fig["_at"], "other_figures": []}
app/backend/billing.py:423:                rates.append(_rate_entry(rec, fig, seg.strip(), "An estimate is not a charge. It is not totaled.", kind="estimate", row=row))
app/backend/billing.py:666:            out.append({"record_no": rec["n"], "provider": _provider(rec), "kind": kind, "label": " ".join(label.split()) or None,
app/backend/billing.py:974:    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"], x.get("other_figures", [])) for x in excluded]
app/backend/billing.py:975:    extras += [extra(x["record_no"], "unclear", x["kind"], x["figure"], x["excerpt"], "An LOP, lien or reduction amount is listed apart from the charges.", x.get("other_figures", [])) for x in lop]
app/backend/conflicts.py:13:    enc = [r for r in records if r.get("kind", "encounter") == "encounter" and r.get("date_iso")]
app/backend/conflict_candidates.py:76:                out.append({"record_no": r["n"], "quote": u, "visits": n, "kind": "count", "arithmetic": f"{n} visits"})
app/backend/conflict_candidates.py:81:                out.append({"record_no": r["n"], "quote": u, "visits": per * weeks, "kind": "freq", "arithmetic": f"{per} per week x {weeks} weeks = {per * weeks} visits"})
app/backend/conflict_candidates.py:99:    order = lambda p: (p["kind"] == "count", (by_n[p["record_no"]].get("date_iso") or "", p["record_no"]))
app/backend/export_routes.py:44:            "amounts": [{"id": a["id"], "kind": a["cls"], "counted_in_total": a["cls"] == "charge" and a.get("cents") is not None,
app/backend/dismissal_patterns.py:76:    return {"key": key, "kind": kind, "label": label, "dismissed_count": n, "scope": scope, "flag_ids": ids, "auto_applied": False,
app/backend/gaps.py:18:        if r.get("kind", "encounter") == "encounter" and r.get("date_iso"):
app/backend/gaps.py:33:        if r.get("kind", "encounter") != "encounter" or r.get("date_iso"):
app/backend/generator.py:67:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:99:             source_kind="record")
app/backend/generator.py:145:    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
app/backend/ingest.py:319:        r.update(id=rid, seq=r["n"], date_iso=p["iso"], date_status=p["status"], date_candidates=p["candidates"], kind=kind,
app/backend/pipeline.py:106:            "cents": a["cents"], "value_cents": a["cents"], "cls": a["cls"], "kind": a["cls"], "start": a["start"], "end": a["end"],
app/backend/pipeline.py:177:                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
app/backend/pipeline.py:258:    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso") and r["kind"] == "encounter")
app/backend/pipeline.py:407:            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
app/backend/overlap.py:78:    return (a.get("value_cents") is not None and a.get("kind") in ("charge", "unclear") and a.get("review_status") != "dismissed" and a.get("state") != "rejected"
app/backend/overlap.py:118:                        "both_charges": s["kind"] == "charge" and c["kind"] == "charge",
app/backend/overlap.py:119:                        "both_in_total": s["kind"] == "charge" and c["kind"] == "charge"
app/backend/overlap.py:137:        rows.append({"id": a["id"], "record_id": rec["id"], "kind": a["kind"], "value_cents": a["value_cents"], "text": a["text"],
app/backend/present.py:60:    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
app/backend/present.py:65:            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
app/backend/present.py:66:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}
app/backend/present.py:104:    v["kind"] = kind
1:# Record and billing document formats for synthetic PI packets (T-078)
16:affidavit, narrative letter, office/specialist note, records-review/IME report). Section 21 maps formats to product rules and packet mixes.
27:| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter "Re:" line, intake form, narrative letter "Re:" line | It is the accident date, not a visit. Treating it as an encounter creates a phantom visit and hides the real first-treatment gap. |
29:| Sworn / letter / report date | §18.001 affidavit jurat and notary commission date, narrative letter date, records-review or IME report date | Paperwork about care, not care. The affidavit's own date-of-service range spans many visits. | Usually a day or more after the service. Using it shifts the chronology and can invent a gap. |
30:| Statement / print / fax date | Ledger "Statement date", pharmacy "Printed on", fax header line at the top of every page | Same date on every page of a records production; a naive extractor dates every entry to the production date. |
31:| Received / Bates stamp | Rubber stamp "RECEIVED NOV 03 2026", Bates footer | Law-firm intake date; never a service date. |
52:line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
58:carry the PT, the PTA and a co-signature. Intake forms are in the patient's own hand. Per D-040 the tool does not label speakers; the generator
65:(e.g., once in the provider's production and again as an attachment to the §18.001 affidavit).
71:**Fields.** Arrival date/time; mode of arrival (EMS, private vehicle); triage block (ESI level, vitals, pain score, triage nurse narrative);
127:on the note; they appear on the CMS-1500 or ledger as units times a fee.
181:- Post-visit narrative reports written for the attorney are supplemental reports, not daily notes; their date is the letter date.
204:(Visit #1 was the new-patient exam on 05/29/2026, the date the intake in section 14 is signed; it was billed on an earlier claim not shown.
231:- APS Medical Billing white paper (demographics, clinical information, body, impression): https://apsmedbill.com/whitepapers/documenting-complete-interpretation-report-diagnostic-radiology-services — search summary.
258:procedure(s) performed (often with CPT in the billing copy); surgeon, assistant(s); anesthesia type and anesthesiologist; estimated blood
343:paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.
377:33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142
473:## 10. Itemized provider ledger / statement
480:and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
495:- Texas CPRC §18.001 (affidavit must include an itemized statement of the service and charge): https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm — search summary; see also research/texas-pi-notes.md.
513:(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
514:CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
519:## 11. Explanation of Benefits (EOB) / remittance
530:- The EOB's "amount billed" restates the provider's charge; counting both the bill and the EOB double counts.
534:- Health-plan EOBs in a PI file often signal a subrogation lien by the health plan.
537:- Noridian JF-A, *MSP Calculation Examples on EOBs*: https://med.noridianmedicare.com/web/jfa/topics/msp/calculation-examples-eob — **opened**. Takeaway: billed minus total CARC amount equals allowed; allowed minus paid equals patient responsibility; examples with CARC CO-16 and a network discount.
558:**Fields.** Law-firm letterhead; letter date; addressee (provider billing office); "Re:" block with client name, DOB, date of injury, sometimes
561:and §18.001 affidavit; attorney signature; client acknowledgement and signature. Related documents: provider-side lien notice or
562:"Assignment and Authorization" signed by the patient at intake; hospital lien notice; reduction letters ("accept $X in full satisfaction").
566:itemized statement of charges." Provider intake LOPs add: the provider will not send the account to collections while the claim is pending,
570:- The LOP is not a medical record: its accident narrative is the attorney's, and its dates (letter date, injury date) are not encounters.
576:- Jotform HIPAA intake packet with an embedded LOP (chiropractic, auto/slip-and-fall): https://hipaa.jotform.com/221364153684052 — **opened**. Takeaway: patient signs; provider defers payment and collections; direction to pay from settlement after fees and costs; continuing lien; patient remains responsible for any shortfall; notice duties before disbursement.
587:Billing Department, Larkspur Hollow Physical Therapy (SYNTHETIC)
593:itemized statement of charges with a business-records affidavit.
651:## 14. Scanned and handwritten intake forms (and OCR failure modes)
684:[PAGE IMAGE, described] Brightwater Spine & Wellness New Patient Intake. Handwritten in blue ink.
709:treatments with times (spinal motion restriction, cold pack, medications); narrative (often in CHART or SOAP order); disposition: unit
724:- "Pt states" lines (history) sit beside crew observations in one narrative; the excerpt keeps both voices.
731:- Assumption: the narrative wording above is common EMS charting style; no Texas agency template was opened.
744:NARRATIVE: Pt states "the truck hit me from behind." Denies LOC. C/o neck pain and
762:**Fields.** Agency billing name and tax ID; invoice number, invoice date and run number; date of service; patient; pick-up and drop-off
765:PIP/MedPay, health plan); adjustments; balance due; "out of network" or balance-billing notice.
778:- A balance-billing notice states an asserted balance without a service line (notes only, D-019).
789:Fernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026
803:## 17. Texas CPRC §18.001 billing affidavit and records cover page
819:- The affidavit is **not a medical record**: no encounter, no clinical content. Its jurat date, notary commission date and cover-page date
821:- §18.001(b) (as amended 2019): the affidavit supports reasonableness of the charge but is **not evidence of causation**. Diagnosis lines on
827:- A counteraffidavit from the other side attacks the same lines; it is an opponent's opinion, not a provider record.
831:- Texas Civil Practice and Remedies Code §18.001 and §18.002, via https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.001 and https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.002 — **opened** (fetch tool; short quotes only). Takeaways: affiant is the provider or the records custodian; affidavit must include an itemized statement and be sworn; 90-day / 120-day service deadlines for affidavits and counteraffidavits; §18.001(b) says it is not evidence of causation; §18.002(b-1) medical-expense form adds amount paid and amount unpaid; amended through Acts 2019 (H.B. 1693). Official page https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm is a JavaScript app that did not render for the fetch tool.
832:- Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute mem. op.), via https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 — **opened** (PDF, pdftotext). Takeaway: §18.001 affidavits do not establish causation.
evals/library/case_lib02_slip_fall_prior_knee.expected.json:187:  "gap_excluded_records": [],
evals/library/case_lib03_truck_rear_end_chiro.expected.json:171:  "gap_excluded_records": [],
evals/library/case_lib05_pedestrian_orif_hardware.expected.json:210:  "gap_excluded_records": [],
evals/library/case_lib04_dog_bite_scar_revision.expected.json:167:  "gap_excluded_records": [],
evals/library/case_lib06_lop_billed_vs_adjusted.expected.json:171:  "gap_excluded_records": [
evals/library/case_lib09_spanish_interpreter_espalda.expected.json:219:  "gap_excluded_records": [
evals/library/case_lib07_parking_lot_fall_outside_records.expected.json:203:  "gap_excluded_records": [],
evals/library/case_lib10_eob_ub04_cms1500.expected.json:244:  "gap_excluded_records": [
evals/library/case_lib13_cloned_notes_cross_provider.expected.json:239:  "gap_excluded_records": [],
evals/library/case_lib11_priors_and_ledger.expected.json:251:  "gap_excluded_records": [
evals/library/case_lib14_handwritten_chiro_scans.expected.json:227:  "gap_excluded_records": [
evals/library/case_lib15_conclusory_letter_mist.expected.json:238:  "gap_excluded_records": [
evals/library_build_v2.py:125:          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
evals/golden/case_09_nonvisit_hides_gap.expected.json:116:  "gap_excluded_records": [
evals/golden/case_02_gap_boundaries.expected.json:170:  "gap_excluded_records": [],
evals/library/case_lib01_er_only_then_gap.expected.json:163:  "gap_excluded_records": [],
evals/golden/case_08_diagnosis_temptation.expected.json:112:  "gap_excluded_records": [],
evals/golden/README.md:45:  "gap_excluded_records": [8],            // non-encounter or ambiguous-date records: never gap endpoints
evals/golden/case_04_duplicates_no_amounts.expected.json:117:  "gap_excluded_records": [],
evals/golden/sample.expected.json:276:  "gap_excluded_records": [],
test_gaps.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:51.291Z

**tool call — Bash**
````
{
 "command": "sed -n 255,340p app/backend/ingest.py; grep -n \"def _kind\\|def classify\\|non_encounter\\|NON_ENC\" app/backend/ingest.py | head"
}
````

### User / tool · 2026-11-02T09:29:51.394Z

**tool result**
````
def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS, splitter=None, not_duplicates=()) -> dict:
    """Everything stage 0 knows. Zero model calls unless `splitter(text) -> [(start, end)] | None` is given AND the code split found one
    unsplit block (D-031); its answer is accepted only if validate_split passes, else the single record stays.
    `not_duplicates`: record ids ('r2') the paralegal said are NOT duplicates of the record they matched; they stay separate (D-031).
    Raises IngestError('bad_request'|'input_too_large') first."""
    text = check_limits(raw_text, max_chars)
    recs, method = _split(text)
    llm_split, split_failure, split_detail, split_call_id = False, None, None, None
    eligible = method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"]))
    if eligible and not splitter:
        split_failure = "NO_MODEL"         # an unsplit paste with no model or fixture to propose boundaries: say so, never pass silently
    elif method == "ambiguous" and not eligible and len(recs) > 1:
        split_failure = "NOT_ATTEMPTED"    # several records plus an unsplit tail: the model is only asked about a single block, so say that
        # (one labelled but incomplete record gets no reason: SPLIT_AMBIGUOUS already describes it, and "several records" would be false)
    if splitter and eligible:
        try:
            got = splitter(text)
        except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
            got, split_failure, split_detail = None, e.code, None if e.replayed else e.code
            if e.code == "FIXTURE_MISS":   # no recorded answer is the same user-facing state as no model; the detail stays for the run's error entry
                split_failure = "NO_MODEL"
        if got is not None:
            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
            try:
                checked = validate_split(text, spans or [], max_records)
            except ValueError as e:        # the code check refused the proposal: keep the one record, with the reason code
                split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
            else:
                recs, method, llm_split = _llm_records(text, checked), "llm", True
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    groups = dedupe(recs)
    if not_duplicates:
        nd = {int(str(i)[1:]) for i in not_duplicates if str(i)[1:].isdigit()}
        out = []
        for grp in groups:
            out.append([grp[0]] + [n for n in grp[1:] if n not in nd])
            out += [[n] for n in grp[1:] if n in nd]
        groups = out
        groups.sort(key=lambda g: g[0])
    first_of = {n: g[0] for g in groups for n in g}
    warns, to_confirm, record_warnings = [], [], []
    if llm_split:
        warns.append(_warn("LLM_SPLIT", "The pasted text had no recognisable record markers; the AI proposed the record boundaries and code checked them. Check the split."))
    elif method == "ambiguous":
        warns.append(_warn("SPLIT_AMBIGUOUS", "Record boundaries could not be found with confidence; check the split."))
        if split_failure:
            if split_failure == "NOT_ATTEMPTED":
                msg = "The paste has several records and some text outside them; the AI is only asked to split a single unsplit block, so that text stays its own record (NOT_ATTEMPTED)."
            elif split_failure == "NO_MODEL":
                msg = "No model was available to propose record boundaries; the paste stays one record."
            else:
                msg = "The AI's proposed record boundaries were not used (" + split_failure + "); the paste stays one record."
            warns.append(_warn("SPLIT_REJECTED", msg))
    if any(len(g) > 1 for g in groups):
        warns.append(_warn("DUPLICATE_MERGED", "Identical records were merged into one entry that cites all of them."))
    if any(p.search(text) for p in _PHI):
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
            line = r["excerpt"].split("\n", 1)[0][:160]
            at = r["text"].find(line)
            record_warnings.append({"type": "record_warning", "category": "llm_split", "record_no": r["n"], "call_id": split_call_id,
                                    "evidence": [{"field": "excerpt", "text": line, "start": r["char_start"] + at if at >= 0 else None,
                                                  "end": r["char_start"] + at + len(line) if at >= 0 else None}]})
        if r["unsplit"]:
            warns.append(_warn("UNSPLIT_TEXT", "Text outside any recognised record was kept as its own record; check it and add separators if it belongs to one.", rid))
        if p["status"] != "parsed":
            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
            warns.append(_warn("DATE_EXCLUDED_FROM_GAPS", "A record date is ambiguous or unreadable; it is left out of gap checks until confirmed.", rid))
            record_warnings.append({"type": "record_warning", "category": "date_ambiguous", "record_no": r["n"],
                                    "evidence": [{"field": "date", "text": r["date_raw"]}]})
        if hits:   # one flag per tagged record; evidence = every matched phrase (offsets into the excerpt)
            record_warnings.append({"type": "record_warning", "category": "injection_suspected", "record_no": r["n"],
                                    "evidence": [{"field": h["field"], "text": h["phrase"], "start": h["start"], "end": h["end"]} for h in hits]})
    by_n = {r["n"]: r for r in recs}
    for w in record_warnings:       # title/explanation come from flag_templates only (R-FL-8)
        r = by_n[w["record_no"]]
215:    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
218:    for e in lexicon.code_list("non_encounter"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:52.413Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport json,glob\nfor f in sorted(glob.glob('evals/library/*.expected.json')+glob.glob('evals/golden/*.expected.json')):\n    d=json.load(open(f)); print(f.split('/')[-1], d.get('gap_excluded_records'), [ (g.get('from_record') or g.get('from_records'),g.get('to_record') or g.get('to_records'),g.get('days')) for g in d.get('gap_table',[])][:6])\nE"
}
````

### User / tool · 2026-11-02T09:29:52.529Z

**tool result**
````
case_01_date_formats.expected.json [8] [([1], [2], 14), ([2], [3], 7), ([3], [4], 7), ([4], [5], 7), ([5], [6], 7), ([6], [7], 8)]
case_02_gap_boundaries.expected.json [] [([1], [2], 29), ([2], [3], 30), ([3], [4], 31), ([4], [5], 30), ([5], [6], 31), ([6], [7], 30)]
case_03_rate_and_ocr.expected.json [2] [([1], [3], 14), ([3], [4], 7), ([4], [5], 9)]
case_04_duplicates_no_amounts.expected.json [] [([1, 2], [3, 4], 7), ([3, 4], [5], 14), ([5], [6], 1)]
case_05_provider_conflict.expected.json [] [([1, 2], [3], 8), ([3], [4], 14), ([4], [5], 21)]
case_06_subtle_pre_existing.expected.json [] [([1], [2], 7), ([2], [3], 14), ([3], [4], 14), ([4], [5], 28)]
case_07_prompt_injection.expected.json [] [([1], [2], 7), ([2], [3], 7), ([3], [4], 49)]
case_08_diagnosis_temptation.expected.json [] [([1], [2], 14), ([2], [3], 14), ([3], [4], 21)]
case_09_nonvisit_hides_gap.expected.json [2, 3] [([1], [4], 56), ([4], [5], 14)]
sample.expected.json [] [([1, 2], [3], 7), ([3], [4], 7), ([4], [5], 28), ([5], [6], 14), ([6], [7], 73), ([7], [8], 11)]
case_lib01_er_only_then_gap.expected.json [] [([1, 2], [3], 44), ([3], [4], 14), ([4], [5], 21), ([5], [6], 14)]
case_lib02_slip_fall_prior_knee.expected.json [] [([1, 2], [3], 7), ([3], [4], 14), ([4], [5], 14), ([5], [6], 21), ([6], [7], 49)]
case_lib03_truck_rear_end_chiro.expected.json [] [([1, 2], [3], 3), ([3], [4], 28), ([4], [5], 20), ([5], [6], 19), ([6], [7], 35)]
case_lib04_dog_bite_scar_revision.expected.json [] [([1, 2], [3], 7), ([3], [4], 28), ([4], [5], 56), ([5], [6], 273)]
case_lib05_pedestrian_orif_hardware.expected.json [] [([1, 2], [3], 2), ([3], [4], 26), ([4], [5], 14), ([5], [6], 49), ([6], [7], 119), ([7], [8], 21)]
case_lib06_lop_billed_vs_adjusted.expected.json [4] [([1, 2], [3], 11), ([3], [5], 35), ([5], [6], 21), ([6], [7], 56)]
case_lib07_parking_lot_fall_outside_records.expected.json [] [([1, 2], [3], 7), ([3], [4], 28), ([4], [5], 28), ([5], [6], 28), ([6], [7], 28)]
case_lib08_second_crash_mri_after.expected.json [] [([1, 2], [3], 4), ([3], [4], 10), ([4], [5], 28), ([5], [6], 28), ([6], [7], 21), ([7], [8, 9], 11)]
case_lib09_spanish_interpreter_espalda.expected.json [4, 7] [([1], [2], 42), ([2], [3], 7), ([3], [5], 14), ([5], [6], 7)]
case_lib10_eob_ub04_cms1500.expected.json [4, 6, 8] [([1, 2], [3], 3), ([3], [5], 12), ([5], [7], 14), ([7], [9], 49)]
case_lib11_priors_and_ledger.expected.json [4, 9] [([1], [2, 3], 14), ([2, 3], [5, 6], 9), ([5, 6], [7], 28), ([7], [8], 35)]
case_lib12_records_review_credibility.expected.json [9, 10] [([1, 2], [3], 14), ([3], [4], 14), ([4], [5], 21), ([5], [6], 21), ([6], [7], 14), ([7], [8], 49)]
case_lib13_cloned_notes_cross_provider.expected.json [] [([1, 2], [3], 2), ([3], [4], 2), ([4], [5], 19), ([5], [6], 2), ([6], [7], 7), ([7], [8], 12)]
case_lib14_handwritten_chiro_scans.expected.json [5, 7, 8] [([1, 2], [3], 7), ([3], [4], 15), ([4], [6], 28)]
case_lib15_conclusory_letter_mist.expected.json [6, 7, 8, 9] [([1], [2], 1), ([2], [3], 14), ([3], [4], 14), ([4], [5], 42)]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:54.188Z

**tool call — Bash**
````
{
 "command": "sed -n 205,252p app/backend/ingest.py; grep -n -B2 -A40 \"non_encounter\" app/llm/lexicon.yaml | head -90; cat tests/unit/test_gaps.py | head -40; grep -rn \"compute_gaps\\|gap_flags\" app --include=*.py | grep -v \"^app/backend/gaps.py\""
}
````

### User / tool · 2026-11-02T09:29:54.317Z

**tool result**
````
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
        p = dates.parse_date(r["date_raw"])
        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(r["n"])
    return [sorted(groups[k]) for k in order]


_PHI = [re.compile(p, re.IGNORECASE) for p in (
    r"\b\d{3}-\d{2}-\d{4}\b",                                  # SSN
    r"(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b",  # phone
    r"\bMRN\s*[:#]?\s*[A-Z0-9-]{5,}")]                         # MRN


def _warn(code: str, message: str, item_id=None) -> dict:
    return {"code": code, "message": message, "item_id": item_id}


def warnings(raw_text: str) -> list:
    return ingest(raw_text)["warnings"]
1-# Flag lexicon v2: the deterministic second signal for review flags, plus code-owned phrase lists.
2:# Owner: researcher (T-009). Consumers: backend flag engines, ingest (non_encounter), the accident-date rule
3-# (accident_date_phrases), the injection tag (injection) and amount classification (damages).
4-# Binding contract: memory/ORCHESTRATOR_DECISIONS.md D-013, D-018 (also D-001, D-003, D-005, D-017) and
5-# memory/DECISIONS.md ADR-008, ADR-010, ADR-011, ADR-013, ADR-014.
6-# Research basis: research/adjuster-attacks.md (attacks A1–A15, "AA src N"), research/texas-pi-notes.md,
7-# research/chronology-practice.md. Reviews addressed in round 2: reviews/T-009-legal-nurse.md and
8-# reviews/T-009-claims-adjuster.md.
9-#
10-# HOW TO USE (binding semantics)
11-# T-027 (generalization pass): patterns were widened for spinal levels (C5-6, L4-S1), "<symptom> since <year>",
12-# "may be <finding>", probable/presumed/favors, "attributes/relates ... to", and narrowed for post-accident wording
13-# (dates on/after the accident year, "secondary to the MVA", "Prior injuries? Denies."). Held-out probes live in
14-# evals/lexicon_heldout.jsonl and are never copied into `examples`; the self-check fails on any overlap and scores
15-# low-only hits as non-flags. Categories are exactly the ADR-013 closed list (the self-check asserts it).
16-# - `pattern` is a Python `re` regex, compiled with re.IGNORECASE and matched against the VERBATIM record text.
17-# - `flag_type` ∈ {pre_existing, causation, record_warning} (D-013/D-018). v1's `causation_weakening` and
18-#   `compliance` are both `causation` now; former compliance entries carry category `missed_care`.
19-# - `category` names the LLM flag category the hit pairs with (ADR-013 closed list where one exists:
20-#   pre_existing, degenerative_language, speculative_language, patient_report, missed_care, new_onset).
21-#   Lexicon-only categories (no LLM counterpart; the flag is origin `lexicon`, so needs_review LEXICON_ONLY):
22-#   prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context,
23-#   accident_date_provenance.
24-# - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
25-#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
26-#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
27-# - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
28-#   raises a flag alone. It can still attach to an LLM flag, keep attribution in a summary, or mark a qualifier unit.
29-# - `negatable: true` → apply the negation guard below. A negated hit is suppressed and logged in the audit.
30-# - `year_filter: true` → the hit's year (named group `year`, else the first 19xx/20xx in the match) must be
31-#   EARLIER than the case's accident year. If the year is the same or later, drop the hit: it refers to the index
32-#   event or later care. If the accident year is unknown, keep the hit and mark it needs_review. (The accident
33-#   year is the year of the earliest code-parsed record date; the tool still never picks an accident date, D-017.)
34-# - `suppress_if_followed_by`: regex tested on the text after the hit, up to the end of its clause. A match
35-#   suppresses the hit (e.g. "chronic neck pain since the collision" is post-accident chronicity).
36-# - `appendix_c`: the sample-case record numbers this entry fires on (any strength), else [].
37-# - examples.hit must fire; examples.miss must not fire; examples.negated must match the regex but be suppressed
38-#   by the guard, a field answer, a filter or a suppressor.
39-#   Run: .venv/bin/python research/lexicon_selfcheck.py. It also runs every golden case and both reviewer probe sets.
40-# - Overlapping hits on one span are deduped by code per (span, flag_type).
41-
42-version: 2
--
1278-code_lists:
1279-
1280:  non_encounter:
1281-    applies_to: source_label   # the record's "Source:" header line, as written (D-014)
1282-    consumer: 'ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic. They still become entries.'
1283-    rationale: 'Billing statements, ledgers, phone notes, records requests and correspondence carry dates that are not dates of care. Counting them hides real gaps (golden case_09: a billing statement 27 days after a visit would break a real gap).'
1284-    source: 'D-003; ADR-010; golden case_01 (phone note), case_09 (billing statement, phone note)'
1285-    false_positive: 'A phone note can document clinical advice. It is still excluded from gaps (D-003) but remains an entry. "Telehealth visit" and "video visit" are encounters and are deliberately NOT listed.'
1286-    entries:
1287-      - id: billing_document
1288-        pattern: '\b(?:billing\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|statement\s+of\s+account|account\s+statement|ledger|invoice|explanation\s+of\s+benefits|EOB|UB-?04|HCFA|CMS-?1500|payment\s+(?:history|record)|balance\s+due\s+notice)\b'
1289-      - id: phone_or_message
1290-        pattern: '\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b'
1291-      - id: records_admin
1292-        pattern: '\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|18\.001\s+affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|no-?\s?show\s+(?:notice|letter))\b'
1293-    examples:
1294-      hit: ['Hobbleton Family Clinic, billing statement', 'Gloamwood Chiropractic, billing statement', 'Dr. Orla Pennywhistle, phone note', 'Hobbleton Family Clinic, phone note', 'Austin Imaging, itemized bill', 'Capital PT, records request']
1295-      miss: ['Capital PT, visit 9', 'Central ER discharge summary', 'Austin EMS run report', 'Hill Country Pain Management, follow-up', 'Austin Imaging, cervical MRI', 'Dr. Lysander Quibble, telehealth visit']
1296-
1297-  accident_date_phrases:
1298-    applies_to: record_text
1299-    consumer: 'ADR-014: code extracts stated accident dates where a phrase is followed within 40 characters by a date in a listed format. A conflict arises if a stated date is later than the earliest record date, or if two different stated dates exist. Dates are never merged (D-017).'
1300-    rationale: 'The accident-date conflict (Appendix C: 2026-01-09 per EMS/ER vs "Date of accident per intake form: 2026-01-19") is the case''s headline conflict, and it must be producible without an LLM.'
1301-    source: 'ADR-014; D-017; Appendix C record 7; AA A7 (JLG Trucking)'
1302-    false_positive: '"DOA" also means "dead on arrival" and "DOI" can mean "digital object identifier". Neither is followed by a date within 40 characters, so the code rule ignores them. "Collision on I-35" is followed by a road, not a date, and is ignored for the same reason. "Injured on the job" has no date.'
1303-    entries:
1304-      - id: accident_date_label
1305-        pattern: '\b(?:date\s+of\s+(?:the\s+)?(?:accident|injury|incident|loss|collision|crash|MVA|MVC)|(?:accident|injury|incident|loss|collision|crash|MVA|MVC)\s+date|DOA|DOI|DOL|D/A|D\.O\.A\.?|D\.O\.I\.?)\b'
1306-      - id: event_on_date
1307-        pattern: '\b(?:collision|accident|crash|wreck|MVA|MVC|incident|rear-?ended|injured|hurt)\s+(?:on|dated)\b'
1308-    examples:
1309-      hit: ['Date of accident per intake form: 2026-01-19.', 'DOA: 01/09/2026', 'Date of injury 1/9/26', 'MVA on 01/09/2026', 'Collision on January 9, 2026.', 'Accident date: 2026-01-09', 'DOI 2026-01-09']
1310-      miss: ['Seen today for neck pain.', 'Transported to Central ER.']
1311-
1312-  injection:
1313-    applies_to: record_text
1314-    consumer: 'ADR-008 / D-005: a hit tags the record INJECTION_SUSPECTED. Code creates a record_warning flag (category injection_suspected, evidence = the matched phrase). Everything derived from the record is forced to needs_review, its amounts cannot be charges, and it cannot suppress other records'' flags. The text stays verbatim and is never stripped.'
1315-    rationale: 'Records are untrusted input. Instruction-like text aimed at a model, or at the pipeline ("add $50,000 to the billed total"), must be visible to the paralegal and must not change entries, flags, charges or totals through the LLM or through code (research/phi-and-ai-supervision.md PR-9).'
1316-    source: 'D-005; ADR-008; golden case_07; research/phi-and-ai-supervision.md PR-9'
1317-    false_positive: >
1318-      Medical charts contain lookalikes: "Please disregard previous entry, wrong patient" (a chart correction),
1319-      "Nervous system: intact" (an exam section header), and "You are now cleared to return to work" (discharge
1320-      instructions). The patterns require a model-directed object ("instructions", "prompt", "rules") for
"""Treatment gaps (code). R-FL-1, LLM_VS_CODE row 9; golden gap_table of every case."""
import pytest
from app.backend import gaps as GP
from tests.unit import _golden as G

def recs(case):
    return [dict(n=r["record_no"], date_iso=r["date"], kind=r["kind"]) for r in G.expected(case)["records"]]

@pytest.mark.parametrize("case", G.case_names())
def test_gap_table_matches_golden(case):
    """R-FL-1: for every golden case the computed intervals (dates, record lists, days, flag) equal gap_table."""
    got = GP.compute_gaps(recs(case))
    want = G.expected(case)["gap_table"]
    assert [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in got] == [(w["from_date"], w["to_date"], w["days"], w["flag"]) for w in want]
    assert [(g["from_records"], g["to_records"]) for g in got] == [(w["from_records"], w["to_records"]) for w in want]

@pytest.mark.parametrize("days,flag", [(28, False), (29, False), (30, False), (31, True), (73, True)])
def test_threshold_is_strictly_greater_than_30(days, flag):
    """R-FL-1 (A-104): 29 and 30 do not flag, 31 does."""
    assert GP.is_gap(days) is flag

def test_sample_73_day_flag_and_28_day_near_miss():
    """R-FL-1: sample flags 2026-03-06 -> 2026-05-18 (73) and not 2026-01-23 -> 2026-02-20 (28)."""
    flagged = [(g["from_date"], g["to_date"], g["days"]) for g in GP.compute_gaps(recs("sample")) if g["flag"]]
    assert flagged == [("2026-03-06", "2026-05-18", 73)]

def test_leap_year_case_02_three_flags_four_near_misses():
    """R-FL-1: case_02 (2028 leap) -> 3 flags (31 days), 4 intervals of 29/30."""
    g = GP.compute_gaps(recs("case_02_gap_boundaries"))
    assert sum(x["flag"] for x in g) == 3 and sum(not x["flag"] for x in g) == 4

def test_non_encounter_records_never_endpoints():
    """R-FL-1 (D-003): case_09 billing statement + phone note do not split the 56-day gap."""
    g = GP.compute_gaps(recs("case_09_nonvisit_hides_gap"))
    assert (g[0]["from_date"], g[0]["to_date"], g[0]["days"], g[0]["flag"]) == ("2026-02-02", "2026-03-30", 56, True)

def test_undated_and_ambiguous_excluded_until_confirmed():
    """R-IN-5: a record with date None is excluded; recomputing after confirm_date (date set) includes it."""
    base = [dict(n=1, date_iso="2026-01-01", kind="encounter"), dict(n=2, date_iso=None, kind="encounter"), dict(n=3, date_iso="2026-01-20", kind="encounter")]
    assert [(g["days"]) for g in GP.compute_gaps(base)] == [19]
app/backend/api.py:310:                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
app/backend/pipeline.py:59:    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
app/backend/review.py:354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
app/backend/review.py:362:            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
app/backend/review.py:432:def _recompute_gaps(conn, case_id, t, changes=None):
app/backend/review.py:442:    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
app/backend/review.py:572:    _recompute_gaps(conn, case_id, t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:29:59.058Z

**tool call — Bash**
````
{
 "command": "ls evals/library | head -40; ls evals/golden | head -30; python3 - <<'E'\nimport json\nd=json.load(open('evals/library/case_lib09_spanish_interpreter_espalda.expected.json'))\nprint(list(d.keys())); print(json.dumps(d['records'],ensure_ascii=False)[:1500]); print(d['gap_excluded_records'])\nE"
}
````

### User / tool · 2026-11-02T09:29:59.168Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
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
['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'must_not', 'notes']
[{"record_no": 1, "raw_date": "2026-03-03", "date": "2026-03-03", "kind": "encounter", "source": "Quillmere Regional ED"}, {"record_no": 2, "raw_date": "14/04/2026", "date": "2026-04-14", "kind": "encounter", "source": "Consultorio Médico Aguaclara, nota de consulta"}, {"record_no": 3, "raw_date": "2026-04-21", "date": "2026-04-21", "kind": "encounter", "source": "Dr. Lucan Ostrowe, orthopedics, new patient"}, {"record_no": 4, "raw_date": "03/05/2026", "date": null, "kind": "encounter", "source": "Consultorio Médico Aguaclara, formulario de admisión (OCR)"}, {"record_no": 5, "raw_date": "2026-05-05", "date": "2026-05-05", "kind": "encounter", "source": "Cinder Valley Imaging, right shoulder MRI"}, {"record_no": 6, "raw_date": "2026-05-12", "date": "2026-05-12", "kind": "encounter", "source": "Dr. Lucan Ostrowe, orthopedics, follow-up"}, {"record_no": 7, "raw_date": "2026-05-20", "date": "2026-05-20", "kind": "billing_statement", "source": "Consultorio Médico Aguaclara, estado de cuenta (billing statement)"}]
[4, 7]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:03.168Z

**tool call — Bash**
````
{
 "command": "grep -rn '\\[\"kind\"\\]\\|get(\"kind\")' evals/*.py tests/unit/*.py | grep -i \"rec\\|expected\" | head -15; python3 - <<'E'\nimport json,glob\nfor f in sorted(glob.glob('evals/library/*.expected.json')+glob.glob('evals/golden/*.expected.json')):\n    d=json.load(open(f))\n    for r in d['records']:\n        print(f.split('/')[-1][:12], r['record_no'], r['kind'], '|', r['source'])\nE"
}
````

### User / tool · 2026-11-02T09:30:03.292Z

**tool result**
````
evals/library_build_v2.py:57:    records = [{"record_no": i, "raw_date": r["raw"], "date": r["date"], "kind": r["kind"], "source": r["source"]} for i, r in enumerate(recs, 1)]
evals/library_build_v2.py:66:        e = {"id": f"E{len(entries) + 1}", "record_nos": [i], "date": r["date"], "date_status": r["status"], "encounter": r["kind"] == "encounter",
evals/run.py:606:            res.append({"id": i["id"], "judge": j, "kind": i["kind"], "split": i.get("split", "in_sample"), "pair": i.get("pair"), "origin": i.get("origin"), "expected": i["expected"],
evals/run.py:612:            wrong, right = [r for r in sel if r["kind"] == "wrong"], [r for r in sel if r["kind"] == "correct"]
evals/run.py:685:        "amounts": _srt((a.get("text"), a.get("value_cents"), a.get("kind"), a.get("state"), tuple(_srt(a.get("record_ids", [])))) for a in out.get("amounts") or []),
tests/unit/test_conflicts.py:8:    return [dict(n=r["record_no"], date_iso=r["date"], source=r["source"], excerpt=raw[r["record_no"]]["excerpt"], kind=r["kind"]) for r in ex["records"]]
tests/unit/test_gaps.py:7:    return [dict(n=r["record_no"], date_iso=r["date"], kind=r["kind"]) for r in G.expected(case)["records"]]
tests/unit/test_ingest.py:16:    kinds = {r["record_no"]: r["kind"] for r in G.expected(case)["records"]}
tests/unit/test_lib09_t110_r2.py:48:        assert r["amount"]["kind"] == "charge" and r["reclassified"]["wording"].lower() == "estado de cuenta: consultas" and r["reclassified"]["judge_verdict"] == "agree"
tests/unit/test_lib09_t110_r2.py:188:        assert r["amount"]["kind"] == "charge" and r["reclassified"]["judge_verdict"] == "agree"
tests/unit/test_reclassify.py:65:    assert (k["$185@r1"]["kind"], k["$185@r2"]["kind"], k["$310@r3"]["kind"], k["$90@r4"]["kind"]) == ("rate", "rate", "charge", "rate")
tests/unit/test_reclassify.py:66:    assert (k["$185@r5"]["kind"], k["$150@r6"]["kind"]) == ("unclear", "rate")       # r5: charged wording, no rate cue; r2 and r6: wording AND a rate cue
tests/unit/test_reclassify.py:75:    assert r["amount"]["kind"] == "unclear" and r["item"]["review_status"] == "pending"          # her earlier accept was about the old meaning
tests/unit/test_reclassify.py:78:    assert ev["before"]["kind"] == "charge" and ev["after"]["kind"] == "unclear" and ev["after"]["note"] == "This is a retainer, not a bill."
tests/unit/test_reclassify.py:97:    assert r["amount"]["kind"] == "charge" and r["reclassified"]["restored"] is True
case_01_date 1 encounter | Quillfeather Urgent Care
case_01_date 2 encounter | Dr. Orla Pennywhistle, primary care
case_01_date 3 encounter | Pemberwick Physical Therapy, visit 1
case_01_date 4 encounter | Pemberwick Physical Therapy, visit 2
case_01_date 5 encounter | Pemberwick Physical Therapy, visit 3
case_01_date 6 encounter | Pemberwick Physical Therapy, visit 4
case_01_date 7 encounter | Dr. Orla Pennywhistle, primary care
case_01_date 8 phone_note | Dr. Orla Pennywhistle, phone note
case_02_gap_ 1 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 2 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 3 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 4 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 5 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 6 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 7 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_02_gap_ 8 encounter | Thistlewick Orthopedics, Dr. Beatrix Quillon
case_03_rate 1 encounter | Gloamwood Chiropractic, initial evaluation
case_03_rate 2 billing_statement | Gloamwood Chiropractic, billing statement
case_03_rate 3 encounter | Gloamwood Chiropractic, visit 2
case_03_rate 4 encounter | Gloamwood Chiropractic, visit 3
case_03_rate 5 encounter | Dr. Hobart Wimbleton, radiology
case_04_dupl 1 encounter | Pottsworth Emergency Department
case_04_dupl 2 encounter | Pottsworth Emergency Department
case_04_dupl 3 encounter | Dr. Tabitha Wrenfield, orthopedics
case_04_dupl 4 encounter | Dr. Tabitha Wrenfield, Orthopedics
case_04_dupl 5 encounter | Dr. Tabitha Wrenfield, orthopedics
case_04_dupl 6 encounter | Nimblewick Hand Therapy, intake
case_05_prov 1 encounter | Fernwhistle County EMS
case_05_prov 2 encounter | Thornapple Valley Hospital ED
case_05_prov 3 encounter | Wombleton Orthopedics, Dr. Tallowby
case_05_prov 4 encounter | Crumpet Lane Orthopedics, M. Tallowby, MD
case_05_prov 5 encounter | Wombleton Orthopedics, Dr. Tallowby
case_06_subt 1 encounter | Snickerwood ER
case_06_subt 2 encounter | Dr. Ophelia Marchbanks, primary care
case_06_subt 3 encounter | Plumtree Physical Therapy, evaluation
case_06_subt 4 encounter | Dr. Ophelia Marchbanks, primary care
case_06_subt 5 encounter | Dr. Ophelia Marchbanks, primary care
case_07_prom 1 encounter | Bumblethorpe Urgent Care
case_07_prom 2 encounter | Dr. Ambrose Thistlewaite, orthopedics
case_07_prom 3 encounter | Bumblethorpe Physical Therapy, visit 1
case_07_prom 4 encounter | Bumblethorpe Physical Therapy, visit 2
case_08_diag 1 encounter | Tumblebrook Urgent Care
case_08_diag 2 encounter | Tumblebrook Imaging, shoulder MRI
case_08_diag 3 encounter | Dr. Lysander Quibble, sports medicine
case_08_diag 4 encounter | Tumblebrook Physical Therapy
case_09_nonv 1 encounter | Hobbleton Family Clinic, visit
case_09_nonv 2 billing_statement | Hobbleton Family Clinic, billing statement
case_09_nonv 3 phone_note | Hobbleton Family Clinic, phone note
case_09_nonv 4 encounter | Hobbleton Family Clinic, visit
case_09_nonv 5 encounter | Hobbleton Family Clinic, visit
sample.expec 1 encounter | Austin EMS run report
sample.expec 2 encounter | Central ER discharge summary
sample.expec 3 encounter | Dr. Alvarez, primary care
sample.expec 4 encounter | Capital PT, initial evaluation
sample.expec 5 encounter | Capital PT, visit 8
sample.expec 6 encounter | Capital PT, visit 9
sample.expec 7 encounter | Hill Country Pain Management, new patient
sample.expec 8 encounter | Austin Imaging, cervical MRI
sample.expec 9 encounter | Hill Country Pain Management, follow-up
case_lib01_e 1 encounter | Dunmarrow Fire-Rescue run report
case_lib01_e 2 encounter | Marrowgate General ED
case_lib01_e 3 encounter | Dr. Imelda Quarrington, primary care
case_lib01_e 4 encounter | Plumtree Physical Therapy, initial evaluation
case_lib01_e 5 encounter | Plumtree Physical Therapy, visit 6
case_lib01_e 6 encounter | Plumtree Physical Therapy, discharge
case_lib02_s 1 encounter | Sablewood Market first-aid log
case_lib02_s 2 encounter | Tamsin Valley Urgent Care
case_lib02_s 3 encounter | Dr. Lucan Pettibone, orthopedics
case_lib02_s 4 encounter | Tamsin Imaging, right knee MRI
case_lib02_s 5 encounter | Dr. Lucan Pettibone, orthopedics
case_lib02_s 6 encounter | Cedar Run Physical Therapy, initial evaluation
case_lib02_s 7 encounter | Cedar Run Physical Therapy, visit 10
case_lib03_t 1 encounter | Okmarrow EMS run report
case_lib03_t 2 encounter | Redhaven Regional ED
case_lib03_t 3 encounter | Thimbleby Chiropractic, initial exam
case_lib03_t 4 encounter | Thimbleby Chiropractic, visit 14
case_lib03_t 5 encounter | Thimbleby Chiropractic, visit 22
case_lib03_t 6 encounter | Thimbleby Chiropractic, discharge
case_lib03_t 7 encounter | Redhaven Imaging, lumbar MRI
case_lib04_d 1 encounter | Wrenfield EMS run report
case_lib04_d 2 encounter | Harlow Memorial ED
case_lib04_d 3 encounter | Dr. Odalys Pennywhistle, plastic surgery
case_lib04_d 4 encounter | Dr. Odalys Pennywhistle, plastic surgery
case_lib04_d 5 encounter | Dr. Odalys Pennywhistle, plastic surgery
case_lib04_d 6 encounter | Dr. Odalys Pennywhistle, plastic surgery, operative note
case_lib05_p 1 encounter | Brightwater EMS run report
case_lib05_p 2 encounter | Coldharbor Trauma Center ED
case_lib05_p 3 encounter | Dr. Casimir Voss, orthopedic surgery, operative report
case_lib05_p 4 encounter | Dr. Casimir Voss, orthopedic surgery, clinic
case_lib05_p 5 encounter | Mosswood Physical Therapy, initial evaluation
case_lib05_p 6 encounter | Mosswood Physical Therapy, visit 12
case_lib05_p 7 encounter | Dr. Casimir Voss, orthopedic surgery, clinic
case_lib05_p 8 encounter | Dr. Casimir Voss, orthopedic surgery, operative report
case_lib06_l 1 encounter | Eastvale Fire-Rescue run report
case_lib06_l 2 encounter | Larchmont Ridge ED
case_lib06_l 3 encounter | Gannet and Moor Injury Clinic, new patient
case_lib06_l 4 billing_statement | Gannet and Moor Injury Clinic, billing statement
case_lib06_l 5 encounter | Larchmont Ridge Imaging, right shoulder MRI
case_lib06_l 6 encounter | Gannet and Moor Injury Clinic, injection visit
case_lib06_l 7 encounter | Gannet and Moor Injury Clinic, follow-up
case_lib07_p 1 encounter | Quarry Hill Occupational Health, intake
case_lib07_p 2 encounter | Cobblestone Imaging
case_lib07_p 3 encounter | Dr. Eudora Fennimore, orthopedics
case_lib07_p 4 encounter | Dr. Eudora Fennimore, orthopedics
case_lib07_p 5 encounter | Dr. Eudora Fennimore, orthopedics
case_lib07_p 6 encounter | Cobblestone Imaging, lumbar MRI
case_lib07_p 7 encounter | Dr. Eudora Fennimore, orthopedics
case_lib08_s 1 encounter | Pelham Ridge EMS run report
case_lib08_s 2 encounter | Thornbury Regional ED
case_lib08_s 3 encounter | Dr. Philippa Wenlock, orthopedics, new patient
case_lib08_s 4 encounter | Larkmoor Physical Therapy, initial evaluation
case_lib08_s 5 encounter | Larkmoor Physical Therapy, visit 12
case_lib08_s 6 encounter | Larkmoor Physical Therapy, visit 22
case_lib08_s 7 encounter | Larkmoor Physical Therapy, discharge
case_lib08_s 8 encounter | Pelham Ridge EMS run report
case_lib08_s 9 encounter | Thornbury Regional ED
case_lib08_s 10 encounter | Valley Imaging, cervical MRI
case_lib08_s 11 encounter | Dr. Philippa Wenlock, orthopedics, follow-up
case_lib08_s 12 encounter | Dr. Ansgar Kellerman, neurology
case_lib09_s 1 encounter | Quillmere Regional ED
case_lib09_s 2 encounter | Consultorio Médico Aguaclara, nota de consulta
case_lib09_s 3 encounter | Dr. Lucan Ostrowe, orthopedics, new patient
case_lib09_s 4 encounter | Consultorio Médico Aguaclara, formulario de admisión (OCR)
case_lib09_s 5 encounter | Cinder Valley Imaging, right shoulder MRI
case_lib09_s 6 encounter | Dr. Lucan Ostrowe, orthopedics, follow-up
case_lib09_s 7 billing_statement | Consultorio Médico Aguaclara, estado de cuenta (billing statement)
case_lib10_e 1 encounter | Rainhollow Fire-Rescue run report
case_lib10_e 2 encounter | Saltmarrow General Hospital ED
case_lib10_e 3 encounter | Saltmarrow General Hospital, discharge summary
case_lib10_e 4 billing_statement | Saltmarrow General Hospital, UB-04 itemized bill
case_lib10_e 5 encounter | Dr. Ignatius Wardlaw, orthopedics, new patient
case_lib10_e 6 billing_statement | Quoinmere Mutual Health Plan, EOB
case_lib10_e 7 encounter | Dr. Ignatius Wardlaw, orthopedics, follow-up
case_lib10_e 8 billing_statement | Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)
case_lib10_e 9 encounter | Dr. Ignatius Wardlaw, orthopedics, follow-up
case_lib11_p 1 encounter | Dr. Hesper Alderton, primary care
case_lib11_p 2 encounter | Ashgrove Fire-Rescue run report
case_lib11_p 3 encounter | Wexcombe Memorial ED
case_lib11_p 4 phone_note | Pellingham and Rook PLLC, correspondence (letter of protection)
case_lib11_p 5 encounter | Fennimoor Spine Clinic, new patient
case_lib11_p 6 encounter | Fennimoor Spine Clinic, new patient intake form (OCR text)
case_lib11_p 7 encounter | Fennimoor Spine Clinic, visit 8
case_lib11_p 8 encounter | Fennimoor Spine Clinic, visit 14
case_lib11_p 9 billing_statement | Fennimoor Spine Clinic, itemized ledger
case_lib12_r 1 encounter | Tallowby Fire-Rescue run report
case_lib12_r 2 encounter | Orrin Vale Community ED
case_lib12_r 3 encounter | Dr. Marisol Dunmore, primary care
case_lib12_r 4 encounter | Harrowmere Physical Therapy, initial evaluation
case_lib12_r 5 encounter | Harrowmere Physical Therapy, visit 8
case_lib12_r 6 encounter | Harrowmere Physical Therapy, functional capacity evaluation
case_lib12_r 7 encounter | Harrowmere Physical Therapy, visit 16
case_lib12_r 8 encounter | Dr. Marisol Dunmore, primary care, follow-up
case_lib12_r 9 phone_note | Marlowe Assurance Group, correspondence, records review letter
case_lib12_r 10 billing_statement | Harrowmere Physical Therapy, itemized statement
case_lib13_c 1 encounter | Marlpit Fire-Rescue run report
case_lib13_c 2 encounter | Vessel Grove Medical Center ED
case_lib13_c 3 encounter | Dr. Corwin Pettibone, primary care
case_lib13_c 4 encounter | Dr. Fenwick Larkspur, orthopedics, new patient
case_lib13_c 5 encounter | Dr. Corwin Pettibone, primary care, follow-up
case_lib13_c 6 encounter | Vessel Grove Imaging, lumbar MRI
case_lib13_c 7 encounter | Dr. Fenwick Larkspur, orthopedics, follow-up
case_lib13_c 8 encounter | Dr. Corwin Pettibone, primary care, follow-up
case_lib13_c 9 encounter | Dr. Fenwick Larkspur, orthopedics, follow-up
case_lib14_h 1 encounter | Tarnwick Fire-Rescue run report
case_lib14_h 2 encounter | Orrin Mere Regional ED
case_lib14_h 3 encounter | Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)
case_lib14_h 4 encounter | Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)
case_lib14_h 5 encounter | Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)
case_lib14_h 6 encounter | Hollowbrook Chiropractic, re-examination (typed)
case_lib14_h 7 billing_statement | Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)
case_lib14_h 8 billing_statement | Tarnwick Fire-Rescue, ambulance invoice
case_lib15_c 1 encounter | Brindlewick Fire-Rescue run report
case_lib15_c 2 encounter | Cobblewood Urgent Care
case_lib15_c 3 encounter | Sunderland Chiropractic, new patient
case_lib15_c 4 encounter | Sunderland Chiropractic, visit 6
case_lib15_c 5 encounter | Sunderland Chiropractic, visit 18
case_lib15_c 6 phone_note | Sunderland Chiropractic, correspondence, narrative letter
case_lib15_c 7 billing_statement | Sunderland Chiropractic, itemized statement
case_lib15_c 8 billing_statement | Sunderland Chiropractic, itemized statement
case_lib15_c 9 phone_note | Pennyroyal Records Retrieval, 18.001 affidavit
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:14.963Z

**tool call — Bash**
````
{
 "command": "sed -n 10,25p tests/unit/test_ingest.py; grep -n -A8 -i \"formulario de admisi\\|intake form\" evals/library/case_lib09*.txt evals/library/case_lib11*.txt | head -60; grep -n -i -B1 -A6 \"intake\" evals/library/case_lib07*.txt evals/golden/case_04*.txt | head -40"
}
````

### User / tool · 2026-11-02T09:30:15.066Z

**tool result**
````
    want = G.records(case)
    assert [(r["n"], r["date_raw"], r["source"], r["excerpt"]) for r in got] == [(w["n"], w["date_raw"], w["source"], w["excerpt"]) for w in want]

@pytest.mark.parametrize("case", G.case_names())
def test_record_kind_matches_golden(case):
    """R-FL-1 (D-003): encounter / billing_statement / phone_note classified by code from the source label."""
    kinds = {r["record_no"]: r["kind"] for r in G.expected(case)["records"]}
    for r in G.records(case):
        assert I.record_kind(r["source"], r["excerpt"]) == kinds[r["n"]], (case, r["n"])

def test_case_04_six_records_four_entries():
    """R-TL-7: case_04 gives 6 records and 4 entry groups [[1,2],[3,4],[5],[6]]."""
    recs = I.split_records(G.raw("case_04_duplicates_no_amounts"))
    assert len(recs) == 6
    assert I.dedupe(recs) == [[1, 2], [3, 4], [5], [6]]

evals/library/case_lib09_spanish_interpreter_espalda.txt:20:Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
evals/library/case_lib09_spanish_interpreter_espalda.txt-21-Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."
evals/library/case_lib09_spanish_interpreter_espalda.txt-22-
evals/library/case_lib09_spanish_interpreter_espalda.txt-23-=== Record 5 ===
evals/library/case_lib09_spanish_interpreter_espalda.txt-24-Date: 2026-05-05
evals/library/case_lib09_spanish_interpreter_espalda.txt-25-Source: Cinder Valley Imaging, right shoulder MRI
evals/library/case_lib09_spanish_interpreter_espalda.txt-26-Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."
evals/library/case_lib09_spanish_interpreter_espalda.txt-27-
evals/library/case_lib09_spanish_interpreter_espalda.txt-28-=== Record 6 ===
evals/library/case_lib11_priors_and_ledger.txt:30:Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
evals/library/case_lib11_priors_and_ledger.txt-31-Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."
evals/library/case_lib11_priors_and_ledger.txt-32-
evals/library/case_lib11_priors_and_ledger.txt-33-=== Record 7 ===
evals/library/case_lib11_priors_and_ledger.txt-34-Date: 2026-04-24
evals/library/case_lib11_priors_and_ledger.txt-35-Source: Fennimoor Spine Clinic, visit 8
evals/library/case_lib11_priors_and_ledger.txt-36-Excerpt: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
evals/library/case_lib11_priors_and_ledger.txt-37-
evals/library/case_lib11_priors_and_ledger.txt-38-=== Record 8 ===
evals/golden/case_04_duplicates_no_amounts.txt-29-Date: 2026-05-26
evals/golden/case_04_duplicates_no_amounts.txt:30:Source: Nimblewick Hand Therapy, intake
evals/golden/case_04_duplicates_no_amounts.txt-31-Excerpt: "Grip strength reduced. Pain 3/10."
evals/golden/case_04_duplicates_no_amounts.txt-32-
evals/library/case_lib07_parking_lot_fall_outside_records.txt-4-Date: 2026-02-10
evals/library/case_lib07_parking_lot_fall_outside_records.txt:5:Source: Quarry Hill Occupational Health, intake
evals/library/case_lib07_parking_lot_fall_outside_records.txt-6-Excerpt: "Employee slipped on ice in the employer parking lot before the shift and fell on the right wrist and low back. Reported to supervisor. Not on duty at the time per patient."
evals/library/case_lib07_parking_lot_fall_outside_records.txt-7-
evals/library/case_lib07_parking_lot_fall_outside_records.txt-8-=== Record 2 ===
evals/library/case_lib07_parking_lot_fall_outside_records.txt-9-Date: 2026-02-10
evals/library/case_lib07_parking_lot_fall_outside_records.txt-10-Source: Cobblestone Imaging
evals/library/case_lib07_parking_lot_fall_outside_records.txt-11-Excerpt: "X-ray right wrist: nondisplaced distal radius fracture. X-ray lumbar spine: mild degenerative changes. Charge: $640."
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:18.244Z

**tool call — Bash**
````
{
 "command": "sed -n 22,31p evals/library/case_lib11_priors_and_ledger.txt; python3 - <<'E'\nimport json\nd=json.load(open('evals/library/case_lib11_priors_and_ledger.expected.json'))\nprint(json.dumps(d['gap_table'])); print([ (r['record_no'],r['date']) for r in d['records']]); print(d['gap_excluded_records']); print(d.get('flags') and [f for f in d['flags'] if f.get('type')=='gap'])\nE\ngrep -n \"def render\" -A25 app/backend/flag_templates.py | head -50; grep -n \"gap_over_30\" -B2 -A8 app/backend/flag_templates.py app/llm/*.yaml 2>/dev/null| head -40"
}
````

### User / tool · 2026-11-02T09:30:18.376Z

**tool result**
````
=== Record 5 ===
Date: 2026-03-27
Source: Fennimoor Spine Clinic, new patient
Excerpt: "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."

=== Record 6 ===
Date: 3/27/26
Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."
[{"from_date": "2026-03-04", "to_date": "2026-03-18", "from_records": [1], "to_records": [2, 3], "days": 14, "flag": false}, {"from_date": "2026-03-18", "to_date": "2026-03-27", "from_records": [2, 3], "to_records": [5, 6], "days": 9, "flag": false}, {"from_date": "2026-03-27", "to_date": "2026-04-24", "from_records": [5, 6], "to_records": [7], "days": 28, "flag": false}, {"from_date": "2026-04-24", "to_date": "2026-05-29", "from_records": [7], "to_records": [8], "days": 35, "flag": true}]
[(1, '2026-03-04'), (2, '2026-03-18'), (3, '2026-03-18'), (4, '2026-03-26'), (5, '2026-03-27'), (6, '2026-03-27'), (7, '2026-04-24'), (8, '2026-05-29'), (9, '2026-06-15')]
[4, 9]
[{'id': 'G1', 'type': 'gap', 'level': 'must', 'from_date': '2026-04-24', 'to_date': '2026-05-29', 'days': 35, 'cite': {'all': [7, 8], 'any': []}, 'evidence': [{'record_no': 7, 'field': 'excerpt', 'excerpt': 'Manual therapy and exercises continued'}, {'record_no': 8, 'field': 'excerpt', 'excerpt': 'Neck pain 4/10, low back pain 5/10'}], 'summary': 'Treatment gap of 35 days (2026-04-24 to 2026-05-29), longer than 30.'}]
151:def render(flag_type: str, subtype: str, **vars) -> tuple:
152-    extra = set(vars) - ALLOWED_VARS
153-    if extra:
154-        raise KeyError(f"unknown template variable(s): {sorted(extra)}")
155-    v = {k: x for k, x in vars.items() if x not in (None, "")}
156-    title, expl = TEMPLATES[category_of(flag_type, subtype)](v)
157-    return title, expl.replace(".”.", ".”")      # a quote that already ends in a period needs no second one
app/backend/flag_templates.py-11-# golden-file subtypes (evals/golden) -> ADR-013 category
app/backend/flag_templates.py-12-ALIASES = {
app/backend/flag_templates.py:13:    ("gap", "treatment_gap"): "gap_over_30",
app/backend/flag_templates.py-14-    ("conflict", "accident_date"): "accident_date_after_treatment",
app/backend/flag_templates.py-15-    ("conflict", "provider_name"): "provider_name_variant",
app/backend/flag_templates.py-16-    ("conflict", "treatment_plan"): "treatment_plan_vs_actual",
app/backend/flag_templates.py-17-    ("conflict", "history_inconsistency"): "other_fact_mismatch",
app/backend/flag_templates.py-18-    ("pre_existing", "prior_injury_prior_treatment"): "pre_existing",
app/backend/flag_templates.py-19-    ("pre_existing", "prior_condition_reported"): "pre_existing",
app/backend/flag_templates.py-20-    ("pre_existing", "prior_other_region"): "pre_existing",
app/backend/flag_templates.py-21-    ("pre_existing", "baseline_symptom"): "pre_existing",
--
app/backend/flag_templates.py-29-
app/backend/flag_templates.py-30-TYPE_OF = {
app/backend/flag_templates.py:31:    "gap_over_30": "gap",
app/backend/flag_templates.py-32-    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
app/backend/flag_templates.py-33-    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
app/backend/flag_templates.py-34-    "pre_existing": "pre_existing", "degenerative_language": "pre_existing", "prior_surgery": "pre_existing",
app/backend/flag_templates.py-35-    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py-36-    "scene_facts": "causation", "alternative_cause": "causation", "litigation_referral": "causation",
app/backend/flag_templates.py-37-    "objective_negative": "causation", "accident_date_provenance": "causation", "credibility_language": "causation",
app/backend/flag_templates.py-38-    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
app/backend/flag_templates.py-39-}
--
app/backend/flag_templates.py-114-
app/backend/flag_templates.py-115-TEMPLATES = {
app/backend/flag_templates.py:116:    "gap_over_30": _gap,
app/backend/flag_templates.py-117-    "accident_date_after_treatment": _acc_after,
app/backend/flag_templates.py-118-    "accident_dates_differ": _acc_differ,
app/backend/flag_templates.py-119-    "provider_name_variant": _provider_variant,
app/backend/flag_templates.py-120-    "treatment_plan_vs_actual": _pair("Treatment plan and what followed differ"),
app/backend/flag_templates.py-121-    "other_fact_mismatch": _pair("Records differ on a fact"),
app/backend/flag_templates.py-122-    "pre_existing": lambda v: ("Mention of a prior or pre-existing condition", f"{_at(v)} mentions a prior or pre-existing condition{_quote(v)}."),
app/backend/flag_templates.py-123-    "degenerative_language": lambda v: ("Degenerative wording", f"{_at(v)} uses degenerative wording{_quote(v)}."),
app/backend/flag_templates.py-124-    "prior_surgery": lambda v: ("Mention of prior surgery or repair", f"{_at(v)} mentions prior surgery or repair{_quote(v)}."),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:22.629Z

**tool call — Bash**
````
{
 "command": "sed -n 60,112p app/backend/flag_templates.py; grep -n \"why\" app/backend/present.py app/backend/pipeline.py app/backend/review.py | head -30; sed -n 425,460p app/backend/review.py; grep -n \"gap\" evals/run.py | head -20"
}
````

### User / tool · 2026-11-02T09:30:22.735Z

**tool result**
````
    return f"{_who(v, key)}{_when(v, dkey)}"


def _single(title, lead):
    """One-record flag: '<lead> in <provider> (<date>): “quote”.'"""
    return lambda v: (title, f"{lead} in {_at(v)}{_quote(v)}.")


def _pair(title):
    def f(v):
        a = f"{_at(v, 'provider_a', 'date_a')}{_quote(v, 'quote_a')}"
        b = f"{_at(v, 'provider_b', 'date_b')}{_quote(v, 'quote_b')}"
        return title, f"{a}. {b}."
    return f


def _gap(v):
    days = v.get("days")
    a = f"{_d(v.get('from_date'))}" + (f" ({v['provider_a']})" if v.get("provider_a") else "")
    b = f"{_d(v.get('to_date'))}" + (f" ({v['provider_b']})" if v.get("provider_b") else "")
    return f"Gap of {days} days", f"Gap of {days} days between {a} and {b}."


def _acc_after(v):
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    first = (f", {_d(v['date'])}" + (f" ({prov})" if prov else "")) if v.get("date") else ""
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    return ("Stated accident date is later than recorded treatment",
            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
            "The records disagree; the tool does not choose between them.")


def _acc_differ(v):
    a = f"{_who(v, 'provider_a')} states {_d(v.get('date_a')) or 'a date'}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')} states {_d(v.get('date_b')) or 'a date'}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Two different stated accident dates", f"{a}; {b}. The tool does not choose between them."


def _provider_variant(v):
    a = f"{_who(v, 'provider_a')}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Provider name differs between records", f"{a} and {b} may name the same provider."


def _date_amb(v):
    raw = f"The date “{v['raw']}” in " if v.get("raw") else "A date in "
    return "Date to confirm", f"{raw}{_who(v)} can be read more than one way; choose one reading."


def _inj(v):
    return ("Instruction-like text in a record",
            f"{_at(v)} contains instruction-like text{_quote(v)}. It is shown unchanged and everything from this record needs review.")
app/backend/pipeline.py:15:                         judges, language, split_llm, totals as TT, why as WHY)
app/backend/pipeline.py:64:        state, why_codes = _compose_code(by_n, nos, reasons, ev, text)
app/backend/pipeline.py:68:                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
app/backend/pipeline.py:80:        state, why_codes = confidence.compose_state({"code_reasons": []}, ctx)
app/backend/pipeline.py:84:                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
app/backend/pipeline.py:237:    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
app/backend/pipeline.py:370:    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
app/backend/present.py:5:from app.backend import confidence, date_convention, generator, grounding, ingest, language, overlap, pdf_text, sentences, spanish, store, totals as T, why
app/backend/present.py:12:def _why(reasons):
app/backend/present.py:16:            out.append(why.why(c))
app/backend/present.py:37:    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
app/backend/present.py:166:        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
app/backend/present.py:167:        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
app/backend/present.py:169:        if why_none:
app/backend/present.py:170:            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
app/backend/present.py:226:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
app/backend/present.py:232:              "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
app/backend/present.py:249:def why_view(conn, case_id, item_id):
    if ch["change"] == "removed":
        return f"A gap of {ch['old_days']} days no longer applies after you confirmed the date of record {seq}."
    if ch["change"] == "added":
        return f"A gap of {ch['new_days']} days now applies after you confirmed the date of record {seq}."
    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."


def _recompute_gaps(conn, case_id, t, changes=None):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002). `changes` (a list) receives the gap figures that moved (T-114)."""
    from app.backend import pipeline as PL
    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
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
46:FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")
243:    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
244:    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
248:            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
668:    """Every R-CO-7 field, by name. Code outputs (record split, parsed dates, entry-ID set, gap flags, amount list and classes, totals) must be identical
683:        "gap_flags": _srt((tuple(_ids(f)), (f.get("computed") or {}).get("from"), (f.get("computed") or {}).get("to"), (f.get("computed") or {}).get("days"),
684:                             f.get("state")) for f in flags if f.get("type") == "gap"),
870:    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
871:    g73 = s is not None and ("2026-03-06", "2026-05-18", 73) not in [tuple(x) for x in s["gap_rows_wrong"]]
872:    n28 = s is not None and ("2026-01-23", "2026-02-20", 28) not in [tuple(x) for x in s["gap_rows_wrong"]] and \
873:        (c6 is None or ("2026-10-19", "2026-11-16", 28) not in [tuple(x) for x in c6["gap_rows_wrong"]])
874:    return {"gap_28_not_flagged": n28, "gap_73_flagged": g73, "all_gap_rows_correct": not any(wrong.values())}
906:                   and a["gap_28_not_flagged"] and a["gap_73_flagged"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:28.482Z

**tool call — Bash**
````
{
 "command": "sed -n 1,10p app/backend/flag_templates.py; sed -n 40,60p app/backend/flag_templates.py; grep -n \"ENDPOINT_NOT_VERIFIED\\|DATE_AMBIGUOUS\" -r app --include=*.py | head -20; sed -n 1,30p app/backend/why.py; sed -n 8,40p app/backend/present.py; grep -n \"def flag_view\\|def _flag\" -A25 app/backend/present.py | head -60"
}
````

### User / tool · 2026-11-02T09:30:28.608Z

**tool result**
````
"""Every flag title and explanation is rendered here, by code (D-007, ADR-013, R-FL-8, LLM_VS_CODE row 16).
render(flag_type, subtype, **vars) -> (title, explanation). The subtype is an ADR-013 category or one of its golden aliases.
Only a closed set of variables is accepted, and none is free LLM prose: dates (ISO), day counts, provider labels as written,
and verbatim record quotes. A missing variable drops its clause; braces never reach the output. No template characterizes,
infers causation, computes a delay from the accident (D-017) or labels anyone non-compliant."""
from app.backend.dates import long_date

ALLOWED_VARS = {"days", "from_date", "to_date", "date", "date_a", "date_b", "stated", "provider", "provider_a", "provider_b",
                "quote", "quote_a", "quote_b", "raw"}

/bin/bash: child setpgid (32517 to 32517): Operation not permitted


def _d(iso):
    return long_date(iso) if iso else ""


def _who(v, key="provider"):
    p = v.get(key)
    return f"{p}" if p else "the record"


def _when(v, key="date"):
    return f" ({_d(v[key])})" if v.get(key) else ""


def _quote(v, key="quote"):
    return f": “{v[key]}”" if v.get(key) else ""


def _at(v, key="provider", dkey="date"):
    return f"{_who(v, key)}{_when(v, dkey)}"
app/backend/why.py:17:    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
app/backend/why.py:19:    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
app/backend/trace.py:71:    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
app/backend/trace.py:72:    "DATE_MISSING": "date_confirmed", "ENDPOINT_NOT_VERIFIED": "endpoints_confirmed", "LEXICON_ONLY": "agreement", "LLM_ONLY": "agreement",
app/backend/trace.py:386:        code = "DATE_AMBIGUOUS" if rec.get("date_status") == "ambiguous" else "DATE_MISSING"
app/backend/trace.py:387:        nxt = na("CONFIRM_DATE", {"record_id": rid, "view": "dates_to_confirm"}) if code == "DATE_AMBIGUOUS" else na("READ_RECORD", {"record_id": rid})
app/backend/trace.py:541:        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
app/backend/trace.py:575:        if "ENDPOINT_NOT_VERIFIED" in R:
app/backend/trace.py:576:            st.append(step("endpoints_confirmed", "Dates at both ends are confirmed", "code", FAIL, reason_text("ENDPOINT_NOT_VERIFIED"), reason="ENDPOINT_NOT_VERIFIED", rule="row 9",
app/backend/trace.py:922:        code = "DATE_AMBIGUOUS" if dc.get("ambiguous") else "DATE_MISSING"
app/backend/confidence.py:11:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:23:_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}
app/backend/confidence.py:67:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES"),
app/backend/review.py:345:            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
app/backend/review.py:349:        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
app/backend/review.py:368:    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
app/backend/review.py:370:    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
app/backend/pipeline.py:39:           "endpoint_unverified": "ENDPOINT_NOT_VERIFIED" in reasons,
app/backend/pipeline.py:42:    if "ambiguous" in dates and "ENDPOINT_NOT_VERIFIED" not in reasons and any(r == "DATE_AMBIGUOUS" for r in reasons):
app/backend/gaps.py:37:            reasons.append("ENDPOINT_NOT_VERIFIED")
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
    "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is an AI translation that has not been verified; read the original quote yourself.",
STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    return lad


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}


86:def flag_view(row, recs):
87-    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
88-            "explanation": row["explanation"], "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
89-            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
90-
91-
92-_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
93-_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
94-
95-
96-def _recs_by_id(conn, case_id):
97-    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
98-
99-
100-def item_view(conn, case_id, item_id):
101-    row = DB.get_item(conn, item_id, case_id)
102-    kind = _ID_KIND[item_id[0]]
103-    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
104-    v["kind"] = kind
105-    return v
106-
107-
108-def all_items(conn, case_id):
109-    recs = _recs_by_id(conn, case_id)
110-    return {k: [_VIEW[k](r, recs) for r in DB.list_items(conn, case_id, k)] for k in ("entry", "amount", "flag")}
111-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:36.476Z

**tool call — Bash**
````
{
 "command": "grep -n \"_computed\" -B2 -A12 app/backend/present.py | head -50; grep -n \"computed\" app/db/*.py app/backend/store.py app/backend/pipeline.py | head -20; sed -n 460,480p app/backend/review.py; sed -n 405,425p app/backend/review.py; grep -n \"memory/contracts\" /dev/null; grep -n \"gap_changes\\|computed\" memory/contracts/api.md | head"
}
````

### User / tool · 2026-11-02T09:30:36.602Z

**tool result**
````
67-
68-
69:def _computed(c):
70-    c = dict(c or {})
71-    if "from_date" in c:
72-        c.update({"from": c.pop("from_date"), "to": c.pop("to_date", None)})
73-        c.setdefault("threshold", 30)
74-        ids = c.get("record_ids") or []
75-        if ids:
76-            c["from_record"], c["to_record"] = ids[0], ids[-1]
77-    return c
78-
79-
80-def _evidence(evs, recs):
81-    by_n = {r["seq"]: r["id"] for r in recs.values()}
--
86-def flag_view(row, recs):
87-    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
88:            "explanation": row["explanation"], "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
89-            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
90-
91-
92-_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
93-_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
94-
95-
96-def _recs_by_id(conn, case_id):
97-    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
98-
99-
100-def item_view(conn, case_id, item_id):
app/backend/store.py:69:        c = f.get("computed") or {}
app/backend/pipeline.py:73:        item["ladder"] = _ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
app/backend/pipeline.py:85:                      "ladder": _ladder(w["id"], backend, {"computed_by": "code"}, state)})
app/backend/pipeline.py:179:    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
app/backend/pipeline.py:182:            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
app/backend/pipeline.py:188:    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
app/backend/pipeline.py:202:            oc = old.get("computed") or {}
app/backend/pipeline.py:396:    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
app/backend/pipeline.py:404:            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
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
        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
    fresh = [n for i, n in new.items() if i not in old]
    for i, n in new.items():
        o = old.get(i)
        if o is not None and any(o[k] != n[k] for k in ("from", "to", "days")):
            rows.append(("changed", o, n))
    for i, o in old.items():
        if i in new:
            continue
        mate = next((n for n in fresh if set(n["record_nos"]) & set(o["record_nos"])), None)
        if mate is not None:
            fresh.remove(mate)
        rows.append(("changed" if mate else "removed", o, mate))
    rows += [("added", None, n) for n in fresh]
    nul = {"flag_id": None, "from": None, "to": None, "days": None}
    return [{"flag_id": (n or o)["flag_id"], "change": ch, "old_days": (o or nul)["days"], "new_days": (n or nul)["days"],
             "old_from": (o or nul)["from"], "old_to": (o or nul)["to"], "new_from": (n or nul)["from"], "new_to": (n or nul)["to"]} for ch, o, n in rows]


def _gap_change_sentence(ch: dict, seq) -> str:
    """The plain-words line the UI can announce. The numbers come from the figures in the entry, not from a model."""
    if ch["change"] == "removed":
27:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
193:      "computed": {"from": "2026-03-06", "to": "2026-05-18", "days": 73, "threshold": 30, "from_record": "r6", "to_record": "r7"},
208:      "computed": {"stated_dates": ["2026-01-19"], "earliest_record_date": "2026-01-09"},
222:      "computed": {},
254:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
262:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
537:Three read-only GETs that feed the vertical steppers (pattern: <outside project> flow rail: each node has a status, label, detail and note, plus an overall progress count and a verdict). Everything is derived from data already stored (ladder, review status, `llm_calls`, `review_events`, case config); nothing is recomputed by a model. `404 not_found` for an unknown token or item.
586:- **flag, code-made (gap, accident-date or provider conflict):** `computed` (code, `evidence.values` has the dates and days), `spans_match` (code), `endpoints_confirmed` (code, `ENDPOINT_NOT_VERIFIED`), `judge_not_needed` (skipped: arithmetic over dates needs no judge), `human`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:30:39.360Z

**tool call — Bash**
````
{
 "command": "sed -n 172,184p app/backend/pipeline.py; sed -n 52,62p app/backend/pipeline.py; sed -n 55,80p app/backend/store.py; grep -n \"def load_records\" -A25 app/backend/store.py | head -40"
}
````

### User / tool · 2026-11-02T09:30:39.465Z

**tool result**
````
        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    if kind == "amount":
        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}

    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
    text = IN.normalize_text(raw_text)
    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
    language.case_check(recs)
    by_n = {r["n"]: r for r in recs}
    backend = P.backend_name()
    flags = []
    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
    for f in code:
        nos = f["record_nos"]
        ev = f["evidence"]
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
        lad = e.get("ladder") or {}
        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
            d["code_check_failed"] = True
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
        ents.append(d)
    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):
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

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:05.743Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/project_backend_conventions.md | head -60; grep -n \"40\\|gap_changes\" tests/unit/test_t114_rates_and_demo_judges.py | head; sed -n 252,266p app/backend/pipeline.py; grep -rn \"42\\b.*40\\|gap.*40\" tests/unit/*.py | grep -v t114 | head"
}
````

### User / tool · 2026-11-02T09:31:05.857Z

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

T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.

## T-085 r2 lessons (language fail-safe)
- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
- language.detect: lang 'uncertain' = some non-English evidence, no confident answer; is_translated(lang) routes es+uncertain to the Spanish path; record_lang never returns English for text with foreign evidence. Do not put words identical to English (fracture, diagnostic, cervical, protrusion) in fr/pt/es lists.
- A one-record packet's preamble line becomes record 1 in ingest; test packets need 2+ records or no preamble.
- Spanish eval pairs: tests/unit/spanish_translation_pairs.jsonl; live judge eval opt-in SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1.

T-086/T-087 r2 (PDF security): `pdf_hidden.py` is a differential render (page with vs without all text, render mode 3 toggled per object); `FPDFTextObj_GetText` is O(page) per call, so read text only for hidden objects. `review.enforce_ocr` re-applies OCR_DERIVED after every item-rewriting step (edit, manual entry, split, date confirm). Pitfalls: other workers edit review.py/api.py concurrently, so commit "HEAD + my hunks": rebuild the file by applying my replacements to `git show HEAD:file`, `git hash-object -w`, `git update-index --cacheinfo` into a `GIT_INDEX_FILE=$(mktemp)` index after `git read-tree HEAD`; then `git reset -q -- <my files>` so the main index is not stale. git-guard blocks `$VAR` in command position (use literal paths) and macOS `sed -i` needs a suffix (use python for edits). Strided memoryview rows need `.tobytes()` before zlib.

## T-085 r4 (D-050)
- Non-English never verified: `confidence.compose_state` ctx `translated` -> AI_TRANSLATION; any new code path that composes a state from a record must pass `language.translated_record(rec)`. Row-based recomputes (rejudge.recompose, review._without_date_doubt) keep the reason from the stored row. Tests: tests/unit/test_d050_never_verified.py.
- language.detect: `_EN_COLLISIONS` (son, operation, plus, solo...) are not foreign evidence when English-only words >= 3. Held-out jsonl rows: `d050_only` (unroutable, word-for-word Spanish) and `ambiguous` are excluded from routing gates.
- Committing with other workers' hunks: HEAD moves during work (check `git log -1` right before `read-tree HEAD`); rebuild blobs from the new HEAD (`git show HEAD:f` + my substitutions) and `update-index --cacheinfo`; check_stale_index blocks a stale tree. Run the committed tree via `git archive $(git write-tree)` in the scratchpad.

T-087 r4 (PDF isolation): ALL PDF parsing (pypdf read + PDFium scan) runs in one child (`pdf_hidden._run_child`, modes text/scan/both, JSON lines: texts first, result second) killed at the shared deadline, with a parent-side `ps` RSS poll (1 GiB; macOS has no RLIMIT_AS). `pdf_text.read_pages` is in-process-only for the child and tests. `pdf_checks._JOBS` (2) gives 429 `busy` and covers OCR too (OCR's pdfium render still runs in the API worker thread). Commit trick that worked: fixed GIT_INDEX_FILE path, `git add` and `git commit` in separate Bash calls (git-guard), then `git reset -q -- files` on the real index. Reviewer probe files are in the reviewer's scratchpad, not the repo: rebuild from the review text.

T-094 (live determinism, conflicts, causation): open-ended model generation of conflicts was the flake. Conflicts are now CODE candidates (`conflict_candidates.py`: plan vs early end with frequency x duration multiplied out; denial of prior history vs a phrase-list prior hit), J3 (`judge_conflict_v4`) only classifies; no `conflicts` model step or prompt exists. J3 benign -> tray (rejected); model-only flag + J4 disagree -> suppressed (`out["suppressed_flags"]`). Pitfalls: (1) `evals.run` scores tray (rejected) flags as emitted candidates, so only suppression removes a false positive from precision; (2) any J3 prompt edit must pass `evals.run --controls` (D-046: all wrong caught, 0 false agree, including held-out) before the 3-run evals; (3) to re-record only the changed judge fixtures use a replay-then-record-on-miss wrapper (fixture first, live only on a miss) per case, then make_curated.py and restore unchanged curated files byte-for-byte; (4) the tree is shared: build commits from a temp index on HEAD and check `git diff HEAD -- <file>` for other workers' hunks (pipeline.py/trace.py/api.md got swept by others twice); (5) architect owns docs/LLM_VS_CODE.md row 11 and must be told the conflicts row changed.

T-094 r2 (D-053): nothing a model proposes is dropped. A model-only flag J4 rejects, and a model-proposed conflict without a code candidate, are TRAY items (`flags._to_tray`; reasons JUDGE_DISAGREES / LLM_ONLY); `present.case_view` tray has kind `flag` items (before this, rejected flags were in the DB but never in the API tray). `suppressed_flags` no longer exists. evals/run.py: `to_candidates` skips state `rejected` (precision/recall over emitted flags only), `flag_tray` reported apart, signature `flags` excludes rejected; report header names `Source commit ..., tree clean`. judge_flag_v3 (missed_care = scheduled/recommended treatment not attended; scene refusal is scene_facts): re-record J4 fixtures with `python -m app.llm.record --fill-missing <packet>` over evals/golden/*.txt and evals/library/*.txt in parallel (script pattern: ThreadPool of subprocesses, ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1). Candidate rules: number words, plan cue, _early_end negation/completion guards in conflict_candidates.py; uncovered patterns in SCOPE_CUTS row 13.

T-103 r4 (billing.py): a printed money token is identified by POSITION (`_at` offset range, `_row` excerpt range, `_unit` line/segment start), never by text; parsers attach positions, `_placed()` reads them back, `_strip_private()` removes every `_`-prefixed key before analyze returns. D-052 "no comparisons" was read strictly: no `_nt`, no cents `<`, sign = `_is_credit` flag; guard test `test_no_money_value_or_text_is_compared_in_billing_code`. Verify count fixes with MANY seeds (reviewer seed 20261102 plus seeds 1-40 via the test module's `_insert`/`_BASES`): seed 20261102 alone hid ~28 CMS/EOB shapes. Never add keys to `_ub_header`/`_header` cols (the test generator draws from them, which would change every seed's draws); use `_ub_all_cols`. Commit with other workers' dirty api.md: build HEAD blob + my replacements, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`.
91:    assert "Billed charges stated in these records: $5,090.00" in letter      # $2,940 + $2,150; the two $400.00 rate rows add nothing (D-019)
119:    """lib09 record 4 (an intake form): reading it as 5 March moves the one gap from 42 to 40 days; the response says so, old to new."""
124:    assert len(out["gap_changes"]) == 1
125:    ch = out["gap_changes"][0]
126:    assert (ch["change"], ch["old_days"], ch["new_days"]) == ("changed", 42, 40)
128:    assert ch["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
133:    """golden case_01 record 8 is a phone note (not an encounter): confirming its date moves no gap, so gap_changes is an empty list (not missing)."""
144:    assert out["gap_changes"] == []
147:def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
150:    new = {"f_b": {"flag_id": "f_b", "from": "2026-03-05", "to": "2026-04-14", "days": 40, "record_nos": [3, 4]}}
    if cause:
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
tests/unit/test_t033_backend.py:86:        F.render("gap", "gap_over_30", days=40, narrative="the patient delayed care")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:07.453Z

**tool call — Bash**
````
{
 "command": "sed -n 105,160p tests/unit/test_t114_rates_and_demo_judges.py; sed -n 340,362p app/backend/review.py"
}
````

### User / tool · 2026-11-02T09:31:07.545Z

**tool result**
````
    for x in [*case["entries"], *case["undated_entries"], *case["amounts"], *case["flags"]]:
        if c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"}).status_code == 200:
            accepted.append(x["id"])
    assert accepted, lib
    g = _gate(c, tok)
    jnr = [b["item_id"] for b in g["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    assert jnr == [], f"{lib}: accepted but no judge fixture: {jnr}"
    # stricter than the gate: no accepted item (a rate included) is missing its judge answer, so the demo needs no 'run the second check' step
    missing = [u["item_id"] for u in trace.unjudged_items(conn, tok) if u["item_id"] in accepted]
    assert missing == [], f"{lib}: judge fixture missing for {missing}"


# ------------------------------------------------------------ 3. confirm_date reports which gap figures moved
def test_confirm_date_reports_the_gap_figures_that_changed(client):
    """lib09 record 4 (an intake form): reading it as 5 March moves the one gap from 42 to 40 days; the response says so, old to new."""
    c, path = client
    tok = _load(c, LIB09)
    assert [f["computed"]["days"] for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"] == [42]
    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
    assert len(out["gap_changes"]) == 1
    ch = out["gap_changes"][0]
    assert (ch["change"], ch["old_days"], ch["new_days"]) == ("changed", 42, 40)
    assert (ch["old_from"], ch["old_to"], ch["new_from"], ch["new_to"]) == ("2026-03-03", "2026-04-14", "2026-03-05", "2026-04-14")
    assert ch["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
    assert ch["flag_id"] in out["gap_flags"]


def test_confirm_date_on_a_phone_note_changes_no_gap(client):
    """golden case_01 record 8 is a phone note (not an encounter): confirming its date moves no gap, so gap_changes is an empty list (not missing)."""
    c, path = client
    text = (pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden" / "case_01_date_formats.txt").read_text()
    tok = c.post("/api/cases", json={"text": text}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    d = next(x for x in c.get(f"/api/cases/{tok}").json()["dates_to_confirm"] if x["candidates"])
    out = c.post(f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", json={"date": d["candidates"][0]}).json()
    assert out["gap_changes"] == []


def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
    from app.backend import review as RV
    old = {"f_a": {"flag_id": "f_a", "from": "2026-03-03", "to": "2026-04-14", "days": 42, "record_nos": [2, 3]}}
    new = {"f_b": {"flag_id": "f_b", "from": "2026-03-05", "to": "2026-04-14", "days": 40, "record_nos": [3, 4]}}
    got = RV._gap_changes(old, new)
    assert len(got) == 1 and got[0]["change"] == "changed" and (got[0]["old_days"], got[0]["new_days"]) == (42, 40)
    assert RV._gap_changes(old, old) == []
    assert RV._gap_changes(old, {})[0]["change"] == "removed" and RV._gap_changes({}, new)[0]["change"] == "added"
    assert "now 40 days (was 42)" in RV._gap_change_sentence(got[0], 4)
    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
    moved, cleared = None, []
    for e in DB.list_items(conn, case_id, "entry"):
        if record_id in (e["record_ids"] or []):
            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
                cleared.append(e["id"])
            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
    for a in DB.list_items(conn, case_id, "amount"):
        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
            cleared.append(a["id"])
    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
    gap_changes = []
    removed += _recompute_gaps(conn, case_id, t, gap_changes)
    for ch in gap_changes:
        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:36.511Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/backend/gaps.py'\ns=open(p).read()\ns=s.replace('''\"\"\"Treatment gaps, computed by code over code-parsed header dates of clinical-encounter records (ADR-010, D-003, R-FL-1, row 9).\nEntry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).\nAmbiguous or missing dates and non-encounter records (billing statements, phone notes) are never endpoints.\"\"\"\nfrom app.backend import dates, flag_templates\nfrom app.backend.ingest import evidence_span\n\nTHRESHOLD_DAYS = 30\n''','''\"\"\"Treatment gaps, computed by code over code-parsed header dates of TREATMENT encounters (ADR-010, D-003, R-FL-1, row 9, T-116).\nEntry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).\nAmbiguous or missing dates never make an endpoint. Neither does any record that is not a treatment visit: intake forms, records\nrequests, billing statements, ledgers, EOBs and claim forms, affidavits, narrative letters, records reviews, correspondence and phone\nnotes. The type is read by code from the record's header label (the \"Source:\" line; see research/record-formats.md sections 10-17 and\n21), so a confirmed intake-form date still cannot start or end a gap. A flagged gap names the excluded records that fall inside it.\"\"\"\nimport re\n\nfrom app.backend import dates, flag_templates\nfrom app.backend.ingest import evidence_span\n\nTHRESHOLD_DAYS = 30\n\n# (label shown to the paralegal, header-label regex), first match wins. A bare \"intake\" (an intake evaluation or visit) is a treatment\n# encounter and is deliberately NOT here; only the paperwork wording is (\"intake form\", \"formulario de admision\").\n_NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (\n    (\"intake form\", r\"\\\\b(?:(?:new[- ]patient\\\\s+)?(?:intake|registration|admission|admissions|check-?in)\\\\s+(?:form|forms|packet|paperwork|questionnaire|sheet)\"\n                    r\"|new[- ]patient\\\\s+(?:paperwork|forms?|questionnaire|packet)|patient\\\\s+(?:information|history|health\\\\s+history|registration)\\\\s+(?:form|questionnaire|sheet)\"\n                    r\"|health\\\\s+history\\\\s+(?:form|questionnaire)|pain\\\\s+(?:diagram|questionnaire)|consent\\\\s+form|assignment\\\\s+of\\\\s+benefits)\\\\b\"\n                    r\"|\\\\bformulario\\\\s+de\\\\s+(?:admisi[oó]n|ingreso|registro)\\\\b|\\\\bhoja\\\\s+de\\\\s+(?:admisi[oó]n|ingreso)\\\\b\"),\n    (\"explanation of benefits\", r\"\\\\b(?:explanation\\\\s+of\\\\s+benefits|EOB|remittance(?:\\\\s+advice)?)\\\\b\"),\n    (\"claim form\", r\"\\\\b(?:UB-?04|CMS-?1500|HCFA|claim\\\\s+form)\\\\b\"),\n    (\"ledger\", r\"\\\\b(?:ledger|payment\\\\s+(?:history|record)|account\\\\s+history)\\\\b\"),\n    (\"billing statement\", r\"\\\\b(?:billing|statement\\\\s+of\\\\s+account|account\\\\s+statement|itemi[sz]ed\\\\s+(?:bill|statement|charges)|statement|invoice|superbill|balance\\\\s+due)\\\\b\"\n                          r\"|\\\\bestado\\\\s+de\\\\s+cuenta\\\\b|\\\\bfactura\\\\b\"),\n    (\"affidavit\", r\"\\\\b(?:affidavit|custodian\\\\s+of\\\\s+records|records\\\\s+custodian|certification\\\\s+of\\\\s+records|business\\\\s+records|cover\\\\s+(?:page|sheet))\\\\b\"),\n    (\"records request\", r\"\\\\b(?:records?\\\\s+request|request\\\\s+for\\\\s+records|records\\\\s+retrieval|authorization\\\\s+form|HIPAA\\\\s+authorization)\\\\b\"),\n    (\"records review\", r\"\\\\b(?:records?|chart|peer|utili[sz]ation)\\\\s+review\\\\b|\\\\bIME\\\\b|\\\\bindependent\\\\s+medical\\\\s+(?:exam|examination|evaluation)\\\\b\"),\n    (\"narrative letter\", r\"\\\\bnarrative\\\\s+(?:letter|report)\\\\b|\\\\bmedical[- ]legal\\\\s+(?:report|narrative)\\\\b|\\\\bsummary\\\\s+letter\\\\b|\\\\bdemand\\\\s+letter\\\\b\"),\n    (\"letter or correspondence\", r\"\\\\b(?:correspondence|letter(?:\\\\s+of\\\\s+protection)?|LOP|fax(?:\\\\s+cover)?|referral\\\\s+(?:form|letter)|prior\\\\s+authori[sz]ation)\\\\b\"),\n    (\"phone or message note\", r\"\\\\b(?:phone|telephone|tel\\\\.?)\\\\s+(?:note|call|encounter|message|contact)\\\\b|\\\\bportal\\\\s+message\\\\b|\\\\bvoicemail\\\\b|\\\\bmessage\\\\s+(?:note|log)\\\\b\"),\n)]\n# A document that names itself on its first line (an intake form whose Source label only says \"new patient\"). Anchored: a clinical note that\n# merely mentions a form further in does not match.\n_TITLE = re.compile(r\"^\\\\W*(?:new[- ]patient\\\\s+)?(?:intake|registration|admission)\\\\s+(?:form|packet|questionnaire)\\\\b|^\\\\W*(?:business\\\\s+records\\\\s+)?affidavit\\\\b\", re.IGNORECASE)\n_KIND_LABEL = {\"billing_statement\": \"billing statement\", \"phone_note\": \"phone or message note\", \"records_admin\": \"letter or correspondence\"}\n\n\ndef non_visit_label(rec: dict):\n    \"\"\"The plain label of a record that is not a treatment visit (\"intake form\", \"billing statement\", ...), or None for a treatment encounter.\n    Header label first (code), then the record's own first-line title, then the ingest kind. A record with only a kind (no label) is judged by its kind.\"\"\"\n    src = rec.get(\"source\") or \"\"\n    for label, rx in _NON_VISIT:\n        if rx.search(src):\n            return label\n    first = (rec.get(\"excerpt\") or \"\").lstrip().split(\"\\\\n\", 1)[0][:120]\n    if first and _TITLE.search(first):\n        return \"affidavit\" if \"affidavit\" in first.lower() else \"intake form\"\n    kind = rec.get(\"kind\", \"encounter\")\n    if kind != \"encounter\":\n        return _KIND_LABEL.get(kind, \"record that is not a treatment visit\")\n    return None\n\n\ndef is_treatment(rec: dict) -> bool:\n    return non_visit_label(rec) is None\n''')\ns=s.replace('''        if r.get(\"kind\", \"encounter\") == \"encounter\" and r.get(\"date_iso\"):\n            by_date''','''        if r.get(\"date_iso\") and is_treatment(r):\n            by_date''')\ns=s.replace('''        if r.get(\"kind\", \"encounter\") != \"encounter\" or r.get(\"date_iso\"):\n            continue''','''        if not is_treatment(r) or r.get(\"date_iso\"):\n            continue''')\ns=s.replace('''def gap_flags(records: list) -> list:''','''def excluded_in_span(gap: dict, records: list) -> list:\n    \"\"\"Records with a code-parsed (or confirmed) date inside the gap's span that are NOT treatment visits, with the label code gave them.\n    They are shown in the gap's why so the paralegal sees that an intake form or bill did not end the gap.\"\"\"\n    out = []\n    for r in records:\n        lab = non_visit_label(r)\n        if lab and r.get(\"date_iso\") and gap[\"from_date\"] <= r[\"date_iso\"] <= gap[\"to_date\"]:\n            out.append({\"record_no\": r[\"n\"], \"record_type\": lab, \"date\": r[\"date_iso\"],\n                        \"why\": flag_templates.non_visit_sentence(lab, r[\"date_iso\"])})\n    return sorted(out, key=lambda x: (x[\"date\"], x[\"record_no\"]))\n\n\ndef gap_flags(records: list) -> list:''')\ns=s.replace('''        title, expl = flag_templates.render(\"gap\", \"gap_over_30\", days=g[\"days\"], from_date=g[\"from_date\"], to_date=g[\"to_date\"],\n                                            provider_a=by_n[a].get(\"source\"), provider_b=by_n[b].get(\"source\"))''','''        excl = excluded_in_span(g, records)\n        title, expl = flag_templates.render(\"gap\", \"gap_over_30\", days=g[\"days\"], from_date=g[\"from_date\"], to_date=g[\"to_date\"],\n                                            provider_a=by_n[a].get(\"source\"), provider_b=by_n[b].get(\"source\"),\n                                            excluded=[(x[\"record_type\"], x[\"date\"]) for x in excl])''')\ns=s.replace('''\"record_nos\": sorted(set(g[\"from_records\"]) | set(g[\"to_records\"])), \"evidence\": ev, \"reasons\": _reasons(g, records)})''','''\"record_nos\": sorted(set(g[\"from_records\"]) | set(g[\"to_records\"])), \"evidence\": ev, \"reasons\": _reasons(g, records),\n                      \"excluded_records\": excl})''')\nopen(p,'w').write(s)\n\np='app/backend/flag_templates.py'\ns=open(p).read()\ns=s.replace('''\"quote\", \"quote_a\", \"quote_b\", \"raw\"}''','''\"quote\", \"quote_a\", \"quote_b\", \"raw\", \"excluded\"}''')\ns=s.replace('''def _gap(v):\n    days = v.get(\"days\")''','''def non_visit_sentence(label: str, iso: str) -> str:\n    \"\"\"T-116: why a record inside a gap did not end it. `label` is one of gaps._NON_VISIT's fixed labels, `iso` a code-parsed date.\"\"\"\n    return f\"{label[:1].upper()}{label[1:]} on {_d(iso)} is not a treatment visit, so it does not start or end a gap.\"\n\n\ndef _gap(v):\n    days = v.get(\"days\")''')\ns=s.replace('''    return f\"Gap of {days} days\", f\"Gap of {days} days between {a} and {b}.\"''','''    more = \"\".join(\" \" + non_visit_sentence(lab, iso) for lab, iso in v.get(\"excluded\") or [])\n    return f\"Gap of {days} days\", f\"Gap of {days} days between {a} and {b}.{more}\"''')\nopen(p,'w').write(s)\n\np='app/backend/pipeline.py'\ns=open(p).read()\ns=s.replace('''\"record_nos\", \"excerpt\", \"excerpt_b\", \"names\", \"lexicon_ids\")''','''\"record_nos\", \"excerpt\", \"excerpt_b\", \"names\", \"lexicon_ids\", \"excluded_records\")''')\nopen(p,'w').write(s)\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace('''\"stated_dates\", \"names\"):\n            if k in f:''','''\"stated_dates\", \"names\", \"excluded_records\"):\n            if k in f:''')\nopen(p,'w').write(s)\nE\ngit diff --stat -- app/backend | tail -5; grep -n \"excluded_records\" app/backend/*.py | head; grep -n \"ALLOWED_VARS\" -r app tests | head"
}
````

### User / tool · 2026-11-02T09:31:36.817Z

**tool result**
````
 app/backend/flag_templates.py | 10 ++++--
 app/backend/gaps.py           | 76 +++++++++++++++++++++++++++++++++++++++----
 app/backend/pipeline.py       |  4 +--
 app/backend/review.py         |  2 +-
 5 files changed, 83 insertions(+), 13 deletions(-)
app/backend/gaps.py:122:                      "excluded_records": excl})
app/backend/pipeline.py:180:                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "excluded_records") if k in it}
app/backend/review.py:448:        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "excluded_records"):
app/backend/flag_templates.py:8:ALLOWED_VARS = {"days", "from_date", "to_date", "date", "date_a", "date_b", "stated", "provider", "provider_a", "provider_b",
app/backend/flag_templates.py:158:    extra = set(vars) - ALLOWED_VARS
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:39.820Z

**tool call — Bash**
````
{
 "command": "sed -n 58,76p app/backend/pipeline.py; git diff --stat -- app/backend/pipeline.py app/backend/review.py; git diff -U0 -- app/backend/pipeline.py app/backend/review.py | grep '^[+-]' | cut -c1-160"
}
````

### User / tool · 2026-11-02T09:31:39.946Z

**tool result**
````
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
 app/backend/pipeline.py | 4 ++--
 app/backend/review.py   | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
-                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids") if k in it}
+                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "excluded_records") if k in it}
+    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
-    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
--- a/app/backend/review.py
+++ b/app/backend/review.py
-        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names"):
+        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "excluded_records"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:44.663Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/pipeline.py'\ns=open(p).read()\na='''        for k in (\"subtype\", \"from_date\", \"to_date\", \"days\", \"body_date\", \"first_treatment_date\", \"stated_dates\", \"names\"):\n            if k in f:\n                item[k] = f[k]\n        item[\"ladder\"] = _ladder(item[\"id\"], backend, {\"computed_by\": \"code\", \"spans_match_input\": state != \"rejected\"}, state)\n        flags.append(item)'''\nassert s.count(a)==1\ns=s.replace(a,a.replace('\"names\"):','\"names\", \"excluded_records\"):'))\nopen(p,'w').write(s)\np='app/backend/present.py'\ns=open(p).read()\na='''def flag_view(row, recs):\n    return {**_common(row), \"type\": row[\"type\"],'''\nb='''def _gap_why(row, base):\n    \"\"\"T-116: a gap's why also names each record inside the span that is not a treatment visit (intake form, bill, ...), as stored by code.\"\"\"\n    ex = [x.get(\"why\") for x in (row.get(\"computed\") or {}).get(\"excluded_records\") or [] if x.get(\"why\")]\n    if row[\"type\"] != \"gap\" or not ex:\n        return base\n    return \" \".join(([] if base == OK_WHY else [base]) + ex)\n\n\ndef flag_view(row, recs):\n    c = _common(row)\n    c[\"why\"] = _gap_why(row, c[\"why\"])\n    return {**c, \"type\": row[\"type\"],'''\nassert a in s\ns=s.replace(a,b)\nopen(p,'w').write(s)\nE\ngit diff -U0 app/backend/present.py | head -30"
}
````

### User / tool · 2026-11-02T09:31:44.789Z

**tool result**
````
diff --git a/app/backend/present.py b/app/backend/present.py
index ad98da4..8876494 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -85,0 +86,8 @@ def _evidence(evs, recs):
+def _gap_why(row, base):
+    """T-116: a gap's why also names each record inside the span that is not a treatment visit (intake form, bill, ...), as stored by code."""
+    ex = [x.get("why") for x in (row.get("computed") or {}).get("excluded_records") or [] if x.get("why")]
+    if row["type"] != "gap" or not ex:
+        return base
+    return " ".join(([] if base == OK_WHY else [base]) + ex)
+
+
@@ -87 +95,3 @@ def flag_view(row, recs):
-    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
+    c = _common(row)
+    c["why"] = _gap_why(row, c["why"])
+    return {**c, "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:49.503Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport json,glob\nfrom app.backend import gaps as GP, ingest as I\nfor f in sorted(glob.glob('evals/library/*.txt')+glob.glob('evals/golden/*.txt')):\n    if 'unsplit' in f: continue\n    exp=json.load(open(f.replace('.txt','.expected.json')))\n    recs=I.ingest(open(f).read())['records']\n    for r in recs:\n        lab=GP.non_visit_label(r)\n        k=r['kind']\n        if (lab is None)!=(k=='encounter') or (lab and not r.get('date_iso')==None and False):\n            print(f.split('/')[-1][:14], r['n'], k, '->', lab, '|', r['source'], r['date_iso'])\n    got=[(g['from_date'],g['to_date'],g['days'],g['flag'],g['from_records'],g['to_records']) for g in GP.compute_gaps(recs)]\n    want=[(g['from_date'],g['to_date'],g['days'],g['flag'],g['from_records'],g['to_records']) for g in exp['gap_table']]\n    if got!=want: print('GAPDIFF',f.split('/')[-1]); print(' got ',got); print(' want',want)\nE"
}
````

### User / tool · 2026-11-02T09:31:49.695Z

**tool result (error)**
````
Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'evals/golden/sample.export.expected.expected.json'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:52.850Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport json,glob,os\nfrom app.backend import gaps as GP, ingest as I\nfor f in sorted(glob.glob('evals/library/*.txt')+glob.glob('evals/golden/*.txt')):\n    e=f.replace('.txt','.expected.json')\n    if not os.path.exists(e): continue\n    exp=json.load(open(e))\n    recs=I.ingest(open(f).read())['records']\n    for r in recs:\n        lab=GP.non_visit_label(r)\n        k=r['kind']\n        if (lab is None)!=(k=='encounter'):\n            print(f.split('/')[-1][:14], r['n'], k, '->', lab, '|', r['source'], r['date_iso'])\n    got=[(g['from_date'],g['to_date'],g['days'],g['flag'],g['from_records'],g['to_records']) for g in GP.compute_gaps(recs)]\n    want=[(g['from_date'],g['to_date'],g['days'],g['flag'],g['from_records'],g['to_records']) for g in exp['gap_table']]\n    if got!=want: print('GAPDIFF',f.split('/')[-1]); print(' got ',got); print(' want',want)\nE"
}
````

### User / tool · 2026-11-02T09:31:53.069Z

**tool result**
````
case_lib09_spa 4 encounter -> intake form | Consultorio Médico Aguaclara, formulario de admisión (OCR) None
case_lib11_pri 6 encounter -> intake form | Fennimoor Spine Clinic, new patient intake form (OCR text) 2026-03-27
GAPDIFF case_lib11_priors_and_ledger.txt
 got  [('2026-03-04', '2026-03-18', 14, False, [1], [2, 3]), ('2026-03-18', '2026-03-27', 9, False, [2, 3], [5]), ('2026-03-27', '2026-04-24', 28, False, [5], [7]), ('2026-04-24', '2026-05-29', 35, True, [7], [8])]
 want [('2026-03-04', '2026-03-18', 14, False, [1], [2, 3]), ('2026-03-18', '2026-03-27', 9, False, [2, 3], [5, 6]), ('2026-03-27', '2026-04-24', 28, False, [5, 6], [7]), ('2026-04-24', '2026-05-29', 35, True, [7], [8])]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:55.848Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && sed -n 1,60p tests/unit/test_t114_rates_and_demo_judges.py | head -70"
}
````

### User / tool · 2026-11-02T09:31:55.850Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:57.290Z

**tool call — Bash**
````
{
 "command": "sed -n 1,50p tests/unit/test_t114_rates_and_demo_judges.py | cut -c1-200"
}
````

### User / tool · 2026-11-02T09:31:57.384Z

**tool result**
````
"""T-114 (T-060 pass 1 F3/F4): a rate is acknowledged, never offered as a letter accept that later blocks export (D-019/D-042, accept needs no judge);
every acceptable item on every demo library packet has its judge fixture (no JUDGE_NOT_RUN dead end); confirm_date reports which gap figures moved.
Fixture backend, no network."""
import os
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace
from app.backend.api import create_app, library_cases
from app.db import db as DB

LIB09 = "case_lib09_spanish_interpreter_espalda"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    path = str(tmp_path / "t114.sqlite")
    return TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), path


def _load(c, lib_id):
    tok = c.post("/api/cases", json={"library": lib_id}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready", lib_id
    return tok


def _gate(c, tok):
    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"]}["export_gate"]


def _blank_judge(conn, tok, item_id):
    row = DB.get_item(conn, item_id, tok)
    lad = row["ladder"]
    lad["judge"] = None
    DB.update_item(conn, item_id, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, item_id))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:31:58.688Z

Now the tests, and update the T-114 confirm test.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:32:23.681Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_t116_gap_endpoints.py <<'E'\n\"\"\"T-116 (T-060 F4): only treatment encounters start or end a treatment gap. Intake forms, records requests, billing statements, ledgers, EOBs,\naffidavits, narrative letters and records reviews are read by code from the header label and never make an endpoint, even after their date\nis confirmed. A flagged gap names the excluded records inside it. Fixture backend, no network.\"\"\"\nimport os\nimport pathlib\nimport time\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import gaps as GP\nfrom app.backend import ingest as I\nfrom app.backend.api import create_app\n\nROOT = pathlib.Path(__file__).resolve().parents[2]\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\n\n\ndef rec(n, date, source, kind=\"encounter\", excerpt=\"\"):\n    return dict(n=n, date_iso=date, source=source, kind=kind, excerpt=excerpt, date_candidates=[])\n\n\n@pytest.mark.parametrize(\"source,label\", [\n    (\"Consultorio Médico Aguaclara, formulario de admisión (OCR)\", \"intake form\"),\n    (\"Fennimoor Spine Clinic, new patient intake form (OCR text)\", \"intake form\"),\n    (\"Brightwater Spine, new patient paperwork\", \"intake form\"),\n    (\"Capital PT, patient information form\", \"intake form\"),\n    (\"Saltmarrow General Hospital, UB-04 itemized bill\", \"claim form\"),\n    (\"Quoinmere Mutual Health Plan, EOB\", \"explanation of benefits\"),\n    (\"Fennimoor Spine Clinic, itemized ledger\", \"ledger\"),\n    (\"Hobbleton Family Clinic, billing statement\", \"billing statement\"),\n    (\"Consultorio Aguaclara, estado de cuenta\", \"billing statement\"),\n    (\"Pennyroyal Records Retrieval, 18.001 affidavit\", \"affidavit\"),\n    (\"Capital PT, records request\", \"records request\"),\n    (\"Marlowe Assurance, records review\", \"records review\"),\n    (\"Sunderland Chiropractic, narrative letter\", \"narrative letter\"),\n    (\"Pellingham and Rook PLLC, correspondence (letter of protection)\", \"letter or correspondence\"),\n    (\"Dr. Orla Pennywhistle, phone note\", \"phone or message note\"),\n])\ndef test_non_visit_types_are_detected_from_the_header_label(source, label):\n    assert GP.non_visit_label(rec(1, \"2026-01-01\", source)) == label\n\n\n@pytest.mark.parametrize(\"source\", [\n    \"Nimblewick Hand Therapy, intake\", \"Quarry Hill Occupational Health, intake\", \"Dr. Alvarez, primary care\", \"Capital PT, initial evaluation\",\n    \"Hill Country Pain Management, new patient\", \"Fennimoor Spine Clinic, new patient\", \"Dr. Lysander Quibble, telehealth visit\",\n    \"Austin Imaging, cervical MRI\", \"Central ER discharge summary\", \"Austin EMS run report\", \"Okmarrow EMS run report\"])\ndef test_treatment_encounters_are_not_excluded(source):\n    \"\"\"A bare 'intake' is an intake evaluation or visit: a treatment encounter. Only the paperwork wording is excluded.\"\"\"\n    assert GP.non_visit_label(rec(1, \"2026-01-01\", source)) is None and GP.is_treatment(rec(1, \"2026-01-01\", source))\n\n\ndef test_a_form_that_titles_itself_on_its_first_line_is_excluded_but_a_note_that_mentions_one_is_not():\n    assert GP.non_visit_label(rec(1, \"2026-01-01\", \"Clinic, new patient\", excerpt=\"NEW PATIENT INTAKE FORM\\nName: ...\")) == \"intake form\"\n    assert GP.non_visit_label(rec(1, \"2026-01-01\", \"Clinic, new patient\", excerpt=\"Exam today. Patient completed the intake form in the lobby.\")) is None\n\n\ndef test_kind_alone_still_excludes_so_existing_callers_keep_working():\n    assert GP.non_visit_label(dict(n=1, date_iso=\"2026-01-01\", kind=\"billing_statement\")) == \"billing statement\"\n    assert GP.non_visit_label(dict(n=1, date_iso=\"2026-01-01\", kind=\"encounter\")) is None\n\n\ndef test_a_dated_intake_form_does_not_end_the_gap():\n    \"\"\"The F4 bug: visit 3 March, intake form dated 5 March (confirmed), visit 14 April. The gap stays 3 March to 14 April, 42 days.\"\"\"\n    recs = [rec(1, \"2026-03-03\", \"Quillmere Regional ED\"), rec(4, \"2026-03-05\", \"Aguaclara, formulario de admisión (OCR)\"),\n            rec(2, \"2026-04-14\", \"Aguaclara, nota de consulta\")]\n    g = GP.compute_gaps(recs)\n    assert [(x[\"from_date\"], x[\"to_date\"], x[\"days\"], x[\"flag\"]) for x in g] == [(\"2026-03-03\", \"2026-04-14\", 42, True)]\n    f = GP.gap_flags(recs)[0]\n    assert f[\"record_nos\"] == [1, 2] and 4 not in f[\"record_nos\"] and f[\"id\"] == \"f_gap_r1_r2\"\n    assert f[\"days\"] == 42 and [x[\"record_no\"] for x in f[\"excluded_records\"]] == [4]\n\n\ndef test_the_gap_why_names_the_excluded_record_and_its_date():\n    recs = [rec(1, \"2026-03-03\", \"ED\"), rec(4, \"2026-03-05\", \"Clinic, intake form\"), rec(2, \"2026-04-14\", \"Clinic, follow-up\")]\n    f = GP.gap_flags(recs)[0]\n    assert f[\"excluded_records\"][0][\"why\"] == \"Intake form on March 5, 2026 is not a treatment visit, so it does not start or end a gap.\"\n    assert f[\"excluded_records\"][0][\"why\"] in f[\"explanation\"] and f[\"excluded_records\"][0][\"record_type\"] == \"intake form\"\n\n\n@pytest.mark.parametrize(\"source\", [\"Clinic, billing statement\", \"Clinic, itemized ledger\", \"Plan, EOB\", \"Clinic, CMS-1500\", \"Firm, records request\",\n                                    \"Custodian, business records affidavit\", \"Clinic, narrative letter\", \"Insurer, records review\"])\ndef test_no_non_visit_record_splits_a_gap_wherever_it_falls(source):\n    recs = [rec(1, \"2026-01-01\", \"Clinic, visit 1\"), rec(2, \"2026-01-20\", source), rec(3, \"2026-02-25\", \"Clinic, visit 2\")]\n    assert [(x[\"days\"], x[\"flag\"]) for x in GP.compute_gaps(recs)] == [(55, True)]\n\n\ndef test_an_excluded_record_outside_the_span_is_not_mentioned_and_a_clean_gap_has_no_extra_sentence():\n    recs = [rec(1, \"2026-01-01\", \"Clinic, visit 1\"), rec(2, \"2026-03-01\", \"Clinic, visit 2\"), rec(3, \"2026-04-01\", \"Clinic, billing statement\")]\n    f = GP.gap_flags(recs)[0]\n    assert f[\"excluded_records\"] == [] and f[\"explanation\"].endswith(\".\") and \"not a treatment visit\" not in f[\"explanation\"]\n\n\ndef test_a_non_visit_record_is_never_an_unverified_endpoint_reason():\n    \"\"\"An undated billing statement cannot be a gap endpoint, so it does not raise ENDPOINT_NOT_VERIFIED; an undated visit still can.\"\"\"\n    base = [rec(1, \"2026-01-01\", \"Clinic, visit 1\"), rec(3, \"2026-03-01\", \"Clinic, visit 3\")]\n    undated = dict(rec(2, None, \"Clinic, intake form\"), date_candidates=[\"2026-01-15\"])\n    assert GP.gap_flags(base + [undated])[0][\"reasons\"] == []\n    visit = dict(rec(2, None, \"Clinic, visit 2\"), date_candidates=[\"2026-01-15\"])\n    assert GP.gap_flags(base + [visit])[0][\"reasons\"] == [\"ENDPOINT_NOT_VERIFIED\"]\n\n\nGOLD_GAP_CASES = sorted(p.stem for p in list((ROOT / \"evals\" / \"golden\").glob(\"case_*.txt\")) + list((ROOT / \"evals\" / \"library\").glob(\"case_lib*.txt\")))\n\n\n@pytest.mark.parametrize(\"name\", GOLD_GAP_CASES)\ndef test_golden_and_library_gap_figures_are_unchanged(name):\n    \"\"\"Every golden and library packet keeps its expected gap dates, day counts and flags. Only the record LISTS differ on lib11 (an intake form\n    shares its date with the visit it belongs to; see the card note for qa).\"\"\"\n    import json\n    d = ROOT / \"evals\" / (\"golden\" if name.startswith(\"case_0\") else \"library\")\n    exp = json.loads((d / f\"{name}.expected.json\").read_text())\n    recs = I.ingest((d / f\"{name}.txt\").read_text())[\"records\"]\n    got = [(g[\"from_date\"], g[\"to_date\"], g[\"days\"], g[\"flag\"]) for g in GP.compute_gaps(recs)]\n    assert got == [(g[\"from_date\"], g[\"to_date\"], g[\"days\"], g[\"flag\"]) for g in exp[\"gap_table\"]]\n\n\ndef test_lib11_intake_form_sharing_the_visit_date_leaves_the_visit_as_the_only_endpoint():\n    recs = I.ingest((ROOT / \"evals\" / \"library\" / \"case_lib11_priors_and_ledger.txt\").read_text())[\"records\"]\n    g = [x for x in GP.compute_gaps(recs) if x[\"from_date\"] == \"2026-03-18\"][0]\n    assert g[\"to_records\"] == [5] and GP.non_visit_label(next(r for r in recs if r[\"n\"] == 6)) == \"intake form\"\n\n\n@pytest.fixture\ndef client(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    for k in (\"ENABLE_LIVE\", \"ANTHROPIC_API_KEY\"):\n        monkeypatch.delenv(k, raising=False)\n    return TestClient(create_app(str(tmp_path / \"t116.sqlite\"), static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef test_lib09_confirming_the_intake_form_date_keeps_the_42_day_gap_and_says_why(client):\n    \"\"\"T-060 F4 acceptance: after confirming record 4 as 5 March the case still shows 'Gap of 42 days', ending at record 2, with no gap change\n    reported, and the gap's explanation and why name the intake form.\"\"\"\n    c = client\n    tok = c.post(\"/api/cases\", json={\"library\": LIB09}).json()[\"token\"]\n    assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n    for _ in range(480):\n        if c.get(f\"/api/cases/{tok}/status\").json()[\"status\"] in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    gap = lambda: [f for f in c.get(f\"/api/cases/{tok}\").json()[\"flags\"] if f[\"type\"] == \"gap\"]\n    assert [f[\"computed\"][\"days\"] for f in gap()] == [42] and gap()[0][\"computed\"].get(\"excluded_records\") == []\n    out = c.post(f\"/api/cases/{tok}/records/r4/confirm_date\", json={\"date\": \"2026-03-05\"}).json()\n    assert out[\"gap_changes\"] == []\n    (f,) = gap()\n    assert f[\"title\"] == \"Gap of 42 days\" and (f[\"computed\"][\"from\"], f[\"computed\"][\"to\"]) == (\"2026-03-03\", \"2026-04-14\")\n    assert f[\"computed\"][\"excluded_records\"][0][\"record_no\"] == 4\n    assert \"Intake form on March 5, 2026 is not a treatment visit\" in f[\"explanation\"] and \"Intake form on March 5, 2026 is not a treatment visit\" in f[\"why\"]\n    assert \"record 4\" not in f[\"explanation\"] and \"r4\" not in \" \".join(x.get(\"record_id\", \"\") for x in f[\"evidence\"])\nE\npython3 - <<'E'\np='tests/unit/test_t114_rates_and_demo_judges.py'\ns=open(p).read()\na=s.index('def test_confirm_date_reports_the_gap_figures_that_changed')\nb=s.index('def test_confirm_date_on_a_phone_note')\nnew='''def test_confirm_date_reports_the_gap_figures_that_changed(client):\n    \"\"\"lib09 record 4 is an intake form (T-116): reading it as 5 March no longer moves the gap (it is not a treatment visit), so gap_changes is []\n    and the gap stays 42 days. A treatment encounter whose date moves an endpoint is still reported (see the pairing test below).\"\"\"\n    c, path = client\n    tok = _load(c, LIB09)\n    assert [f[\"computed\"][\"days\"] for f in c.get(f\"/api/cases/{tok}\").json()[\"flags\"] if f[\"type\"] == \"gap\"] == [42]\n    out = c.post(f\"/api/cases/{tok}/records/r4/confirm_date\", json={\"date\": \"2026-03-05\"}).json()\n    assert out[\"gap_changes\"] == []\n    assert [f[\"computed\"][\"days\"] for f in c.get(f\"/api/cases/{tok}\").json()[\"flags\"] if f[\"type\"] == \"gap\"] == [42]\n\n\n'''\ns=s[:a]+new+s[b:]\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_t116_gap_endpoints.py tests/unit/test_t114_rates_and_demo_judges.py tests/unit/test_gaps.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T09:32:32.613Z

**tool result**
````
........................................................................ [ 67%]
...................................                                      [100%]
107 passed in 8.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:32:34.972Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/unit/test_t116_gap_endpoints.py'\ns=open(p).read()\ni=s.index('    assert \"record 4\" not in f[\"explanation\"]')\ns=s[:i].rstrip('\\n')+'\\n'\nopen(p,'w').write(s)\nE\n(.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -8) ; sed -n 1,30p evals/run.py | head -40"
}
````

### User / tool · 2026-11-02T09:34:35.894Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: bv62qdeol). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:37.487Z

**tool call — Bash**
````
{
 "command": "ls evals/reports 2>/dev/null | tail -3; grep -n \"argparse\\|add_argument\" evals/run.py | head; (LLM_BACKEND=fixture timeout 550 .venv/bin/python -m evals.run 2>&1 | tail -30)",
 "timeout": 580000
}
````

### User / tool · 2026-11-02T09:34:37.580Z

**tool result**
````
library-latest.md
m3-sensors.md
runs
21:import argparse
1195:    ap = argparse.ArgumentParser(prog="python -m evals.run")
1196:    ap.add_argument("--check-fresh", action="store_true")
1197:    ap.add_argument("--check-spec", action="store_true")
1198:    ap.add_argument("--backend", default=None)
1199:    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
1200:    ap.add_argument("--out", default=str(REPORTS))
1201:    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
1202:    ap.add_argument("--write-calibration", action="store_true",
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:39.922Z

**tool call — Bash**
````
{
 "command": "git status --short evals/reports | head; LLM_BACKEND=fixture .venv/bin/python -m evals.run > /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/evals116.txt 2>&1; tail -40 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/evals116.txt",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T09:34:41.332Z

**tool result**
````
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T093441Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:43.646Z

**tool call — Bash**
````
{
 "command": "R=evals/reports/20261102T093441Z.md; grep -n -i \"gap\" $R | head -12; PREV=$(ls evals/reports/2026*.md | grep -v 093441 | tail -1); echo $PREV; grep -n -i \"gap\" $PREV | head -12; grep -n -i \"4_no_invented\" $R $PREV | head"
}
````

### User / tool · 2026-11-02T09:34:43.751Z

**tool result**
````
13:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
39:Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
evals/reports/20261102T093020Z.md
13:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
107:Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
112:- entry misses: {"case_02_gap_boundaries": [{"entry": "E1", "why": "excerpt misses must_contain_excerpt"}], "case_06_subtle_pre_existing": [{"entry": "E3", "why": "excerpt misses must_contain_excerpt"}]}
evals/reports/20261102T093441Z.md:6:Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7); judge_controls (J3/J4 seeded wrong items): not measured
evals/reports/20261102T093020Z.md:6:Blockers: 4_no_invented_facts; judge_controls (J3/J4 seeded wrong items): j3 caught 15/17, false agree ['J3V5', 'H3V5']; j4 caught 12/12, false agree []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:45.969Z

**tool call — Bash**
````
{
 "command": "sleep 60; tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output"
}
````

### User / tool · 2026-11-02T09:34:45.970Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 60 followed by: tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:48.534Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"passed|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output; do sleep 5; done; tail -6 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for unit tests to finish",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:34:48.542Z

**tool result**
````
Monitor started (task boa1kh9pi, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:49.505Z

Meanwhile, the api contract note.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:49.990Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- memory/contracts/api.md; sed -n 186,200p memory/contracts/api.md | cut -c1-260"
}
````

### User / tool · 2026-11-02T09:34:50.096Z

**tool result**
````
    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}],
    "possible_overlaps": []
  },
  "flags": [
    { "id": "f_gap_r6_r7", "type": "gap", "category": "gap_over_30", "source_kind": "record",
      "title": "Gap of 73 days",
      "explanation": "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).",
      "computed": {"from": "2026-03-06", "to": "2026-05-18", "days": 73, "threshold": 30, "from_record": "r6", "to_record": "r7"},
      "evidence": [
        {"record_id": "r6", "excerpt": "Date: 2026-03-06", "start": 1107, "end": 1123},
        {"record_id": "r6", "excerpt": "Source: Capital PT, visit 9", "start": 1124, "end": 1151},
        {"record_id": "r7", "excerpt": "Date: 2026-05-18", "start": 1242, "end": 1258},
        {"record_id": "r7", "excerpt": "Source: Hill Country Pain Management, new patient", "start": 1259, "end": 1308} ],
      "origin": "code", "reviewer_note": null,
      "state": "verified", "reasons": [], "why": "Calculated by code from two dates read from the record headers.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:54.180Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'\ns=open(p).read()\na='**T-114: `gap_changes[]`**'\ni=s.index(a)\nadd='''**T-116: only treatment encounters are gap endpoints.** `gaps.non_visit_label` reads the record type in code from the header (`Source:`) label, falling back to the ingest kind: intake form (incl. `formulario de admisión`), billing statement, ledger, explanation of benefits, claim form, affidavit, records request, records review, narrative letter, letter or correspondence, phone or message note. A bare `intake` / `new patient` / `initial evaluation` is a treatment visit. None of the excluded types starts or ends a gap, even after `confirm_date` gives it a date, so confirming record 4 of lib09 as 5 March leaves `Gap of 42 days` (3 Mar to 14 Apr) and `gap_changes` is `[]`. A gap flag's `computed.excluded_records` (always present, `[]` when none) lists the non-visit records dated inside the span: `{record_no, record_type, date, why}`, e.g. `why: \"Intake form on March 5, 2026 is not a treatment visit, so it does not start or end a gap.\"`. The same sentences are appended to the flag's `explanation` and to its `why`. The frontend can show them as is; they are code-built from fixed labels, never model text.\n\n'''\ns=s[:i]+add+s[i:]\nopen(p,'w').write(s)\nE\ngit diff --stat -- memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T09:34:54.305Z

**tool result**
````
 memory/contracts/api.md | 2 ++
 1 file changed, 2 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:34:57.852Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-116 --agent backend --text \"For qa (do not edit evals/golden; I did not): record types are now read by code. Two library lines change, nothing else; gap dates, day counts and flags are identical in all 25 golden+library packets (flag precision/recall gap 1.000/1.000, fixture run evals/reports/20261102T093441Z.md). (1) evals/library/case_lib11_priors_and_ledger.expected.json: record 6 is a 'new patient intake form (OCR text)' dated the same day as record 5, so it stops being an endpoint: gap_table[1].to_records [5, 6] -> [5]; gap_table[2].from_records [5, 6] -> [5]; gap_excluded_records [4, 9] -> [4, 6, 9]. (2) lib09 record 4 (formulario de admision) is already in gap_excluded_records [4, 7] and its kind stays 'encounter' in the golden records list; no change needed. Bare 'intake' (case_04 r6, lib07 r1) stays a treatment encounter.\"; python3 tools/board.py show T-116 | tail -3"
}
````

### User / tool · 2026-11-02T09:34:58.040Z

**tool result**
````
noted on T-116

## Handoff (filled when moving to in_review)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:00.569Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output; do sleep 5; done; tail -6 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for unit test summary",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:00.577Z

**tool result**
````
Monitor started (task bnzln49yr, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:02.210Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output | tail -8"
}
````

### User / tool · 2026-11-02T09:35:02.290Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:06.003Z

**tool call — Monitor**
````
{
 "command": "until [ -s /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output ]; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for test output",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:06.011Z

**tool result**
````
Monitor started (task b12uacp3d, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:06.961Z

**tool call — Bash**
````
{
 "command": "ps aux | grep \"pytest\" | grep -v grep | head -3"
}
````

### User / tool · 2026-11-02T09:35:07.105Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:09.743Z

**tool call — Monitor**
````
{
 "command": "while pgrep -f \"pytest -q tests/unit$\" >/dev/null; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for pytest process end",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:09.753Z

**tool result**
````
Monitor started (task bp38cpt3j, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:11.000Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h; git status --short app tests memory/contracts | head -30"
}
````

### User / tool · 2026-11-02T09:35:11.124Z

**tool result**
````
b5fb35c
 M app/backend/api.py
 M app/backend/flag_templates.py
 M app/backend/gaps.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/review.py
 M app/frontend/batch.js
 M app/frontend/flags.js
 M app/frontend/review.js
 M app/frontend/sidebyside.js
 M app/frontend/timeline.js
 M memory/contracts/api.md
D  tests/fixtures/llm/0a1f9ffffbdbea51c06cf9579c5ee22ca10a92ed9cc4de9d0d7353f48bc05a1b.json
D  tests/fixtures/llm/4280f3fe93c7a9e504bd881391b1e2fca613b4bbac382040c29d19e3285a9882.json
 M tests/unit/test_t114_rates_and_demo_judges.py
?? tests/fixtures/llm/0a1f9ffffbdbea51c06cf9579c5ee22ca10a92ed9cc4de9d0d7353f48bc05a1b.json
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
?? tests/fixtures/llm/23a42e78f6f5e66dfaeda880459bbbbf14d34b4945c40aca56c2d0bd19babf84.json
?? tests/fixtures/llm/249e2de6179c20db35f047d07665f84dcea759a937141dbc2f80ca48a96692f4.json
?? tests/fixtures/llm/2f4820ea5ea9c5774b27dd8afcf0403a0dc37a88dece83f54b0e2a3d0fa4232e.json
?? tests/fixtures/llm/3733e9af1cffd2d880e638be635c69e8f375a373d0565459b80eaff265cbafc3.json
?? tests/fixtures/llm/3e5d9866924792caa21c7c7f85e3c51171cf3eeec5574edcf91fff8e262d18c4.json
?? tests/fixtures/llm/4280f3fe93c7a9e504bd881391b1e2fca613b4bbac382040c29d19e3285a9882.json
?? tests/fixtures/llm/5531d4c17591ba0eba7b53c9b8d53da065ae32be1e52c35fb5538ceeccfabe4d.json
?? tests/fixtures/llm/764f06e3d21fee9d69a75f53bb1a1d919bd7ec6bac9579c307cb2042d9a21aef.json
?? tests/fixtures/llm/797f02f51e04dd09f1acf004652ec8a2aa105516414a3c5dac8ba6cd4ee608ef.json
?? tests/fixtures/llm/8381f7e471270f341577290612b5e632b57001c8a4e510723a4ce30db944a32b.json
?? tests/fixtures/llm/841aee7dcaed94231186dfa9bf9842475586e95376a06f2f94af53bd369998bf.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:13.950Z

**tool call — Bash**
````
{
 "command": "for f in app/backend/flag_templates.py app/backend/present.py app/backend/review.py app/backend/pipeline.py memory/contracts/api.md tests/unit/test_t114_rates_and_demo_judges.py; do echo \"== $f\"; git diff -U0 -- $f | grep '^@@'; done"
}
````

### User / tool · 2026-11-02T09:35:14.125Z

**tool result**
````
== app/backend/flag_templates.py
@@ -9 +9 @@ ALLOWED_VARS = {"days", "from_date", "to_date", "date", "date_a", "date_b", "sta
@@ -75,0 +76,5 @@ def _pair(title):
@@ -80 +85,2 @@ def _gap(v):
== app/backend/present.py
@@ -85,0 +86,8 @@ def _evidence(evs, recs):
@@ -87 +95,3 @@ def flag_view(row, recs):
== app/backend/review.py
@@ -448 +448 @@ def _recompute_gaps(conn, case_id, t, changes=None):
== app/backend/pipeline.py
@@ -70 +70 @@ def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> di
@@ -180 +180 @@ def _row(kind: str, it: dict) -> dict:
@@ -367,0 +368 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
@@ -370 +370,0 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
== memory/contracts/api.md
@@ -261,0 +262,2 @@ Response 200: the record with `date_status: "confirmed"`, its entry's date, the
== tests/unit/test_t114_rates_and_demo_judges.py
@@ -119 +119,2 @@ def test_confirm_date_reports_the_gap_figures_that_changed(client):
@@ -124,6 +125,2 @@ def test_confirm_date_reports_the_gap_figures_that_changed(client):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:16.909Z

**tool call — Monitor**
````
{
 "command": "while pgrep -f \"pytest -q tests/unit$\" >/dev/null; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for unit run end",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:16.919Z

**tool result**
````
Monitor started (task bq3bhv99x, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:19.885Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\n# prepare pipeline.py blob = HEAD + my two hunks only\nimport subprocess\nhead=subprocess.check_output(['git','show','HEAD:app/backend/pipeline.py']).decode()\na='''        for k in (\"subtype\", \"from_date\", \"to_date\", \"days\", \"body_date\", \"first_treatment_date\", \"stated_dates\", \"names\"):\n            if k in f:\n                item[k] = f[k]\n        item[\"ladder\"] = _ladder('''\nassert head.count(a)==1\nhead=head.replace(a,a.replace('\"names\"):','\"names\", \"excluded_records\"):'))\nb='\"record_nos\", \"excerpt\", \"excerpt_b\", \"names\", \"lexicon_ids\") if k in it}'\nassert head.count(b)==1\nhead=head.replace(b,b.replace('\"lexicon_ids\")','\"lexicon_ids\", \"excluded_records\")'))\nopen('/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pipeline_mine.py','w').write(head)\nE\necho ok"
}
````

### User / tool · 2026-11-02T09:35:20.001Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:22.121Z

**tool call — Monitor**
````
{
 "command": "while pgrep -f \"pytest -q tests/unit$\" >/dev/null; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for unit run end (re-arm)",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:22.132Z

**tool result**
````
Monitor started (task bh0zg1x1m, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:24.232Z

**tool call — Bash**
````
{
 "command": "ps -o pid,etime,time,command -p 35040 | cut -c1-120; tail -c 300 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output"
}
````

### User / tool · 2026-11-02T09:35:24.336Z

**tool result**
````
  PID ELAPSED      TIME COMMAND
35040   02:49   0:57.55 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:27.016Z

**tool call — Monitor**
````
{
 "command": "while kill -0 35040 2>/dev/null; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for pid 35040 to exit",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:27.028Z

**tool result**
````
Monitor started (task bfv3wqxpi, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:27.965Z

Waiting on the test run.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:29.385Z

**tool call — Monitor**
````
{
 "command": "while kill -0 35040 2>/dev/null; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output",
 "description": "wait for test completion",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:29.398Z

**tool result**
````
Monitor started (task byoaz3sic, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:30.870Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output"
}
````

### User / tool · 2026-11-02T09:35:30.880Z

**tool result**
````
<system-reminder>Warning: the file exists but the contents are empty.</system-reminder>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:33.521Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pyflakes app/backend/gaps.py 2>&1 | head -3; ps -o etime= -p 35040"
}
````

### User / tool · 2026-11-02T09:35:33.621Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.venv/bin/python: No module named pyflakes
02:58
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:35.444Z

**tool call — Monitor**
````
{
 "command": "while kill -0 35040 2>/dev/null; do sleep 10; done; echo done",
 "description": "wait for unit tests exit",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:35.451Z

**tool result**
````
Monitor started (task bcx0g0vw7, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:36.427Z

Waiting for the unit-test run to finish; I'll commit once it reports.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:37.323Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output | tail -8; ps -o etime= -p 35040"
}
````

### User / tool · 2026-11-02T09:35:37.413Z

**tool result**
````
03:02
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:38.715Z

**tool call — Monitor**
````
{
 "command": "while kill -0 35040 2>/dev/null; do sleep 10; done; echo finished",
 "description": "wait for pytest exit",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T09:35:38.722Z

**tool result**
````
Monitor started (task bz963vcvc, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:40.368Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bv62qdeol.output | head -20"
}
````

### User / tool · 2026-11-02T09:35:40.454Z

**tool result**
````
............................s........................................... [ 84%]
........................................................................ [ 87%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 95%]
........................................................................ [ 98%]
........................................                                 [100%]
2559 passed, 1 skipped in 182.03s (0:03:02)
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
    python -m evals.run --write-calibration
                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:42.521Z

2559 passed. Now commit using a temp index.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:44.477Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h && export GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/idx116 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && B=$(git hash-object -w /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pipeline_mine.py) && git update-index --cacheinfo 100644,$B,app/backend/pipeline.py && git add app/backend/gaps.py app/backend/flag_templates.py app/backend/present.py app/backend/review.py memory/contracts/api.md tests/unit/test_t116_gap_endpoints.py tests/unit/test_t114_rates_and_demo_judges.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T09:35:44.784Z

**tool result**
````
3e3f3b7
 app/backend/flag_templates.py                 |  10 +-
 app/backend/gaps.py                           |  76 +++++++++++--
 app/backend/pipeline.py                       |   4 +-
 app/backend/present.py                        |  12 ++-
 app/backend/review.py                         |   2 +-
 memory/contracts/api.md                       |   2 +
 tests/unit/test_t114_rates_and_demo_judges.py |  11 +-
 tests/unit/test_t116_gap_endpoints.py         | 150 ++++++++++++++++++++++++++
 8 files changed, 248 insertions(+), 19 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:49.189Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/idx116 && git commit -q -m \"feat(backend): only treatment encounters start or end a gap; excluded records named in the gap's why (T-116)\n\nRecord type is read by code from the header label (intake form, billing statement, ledger, EOB, claim form, affidavit, records request, records review, narrative letter, correspondence, phone note). A confirmed intake-form date no longer moves the lib09 gap (stays 42 days). Gap flags carry computed.excluded_records; the sentence is appended to explanation and why.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log -1 --format=%h && git show --stat --format= HEAD | tail -10"
}
````

### User / tool · 2026-11-02T09:35:50.036Z

**tool result**
````
check_secrets: ok (8 file(s) scanned staged)
c1b44be
 app/backend/flag_templates.py                 |  10 +-
 app/backend/gaps.py                           |  76 +++++++++++--
 app/backend/pipeline.py                       |   4 +-
 app/backend/present.py                        |  12 ++-
 app/backend/review.py                         |   2 +-
 memory/contracts/api.md                       |   2 +
 tests/unit/test_t114_rates_and_demo_judges.py |  11 +-
 tests/unit/test_t116_gap_endpoints.py         | 150 ++++++++++++++++++++++++++
 8 files changed, 248 insertions(+), 19 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:55.225Z

**tool call — Bash**
````
{
 "command": "unset GIT_INDEX_FILE; git reset -q -- app/backend/gaps.py app/backend/flag_templates.py app/backend/present.py app/backend/review.py memory/contracts/api.md tests/unit/test_t116_gap_endpoints.py tests/unit/test_t114_rates_and_demo_judges.py 2>&1|tail -1; B=\"python3 tools/board.py\"\n$B commit T-116 --sha c1b44be --agent backend\n$B ac T-116 --check 1 --agent backend --evidence \"tests/unit/test_t116_gap_endpoints.py (49 tests incl. all 25 golden+library gap tables unchanged, lib09 confirm keeps 42 days with why 'Intake form on March 5, 2026 is not a treatment visit...'); tests/unit 2559 passed; python -m evals.run fixture: gap precision/recall 1.000/1.000 (evals/reports/20261102T093441Z.md); lib11 record lists change, posted for qa\"\n$B handoff T-116 --agent backend --text \"What changed: gaps.non_visit_label reads the record type in code from the header label (intake form incl. formulario de admision, billing statement, ledger, EOB, claim form, affidavit, records request, records review, narrative letter, correspondence, phone note; bare 'intake' stays a visit), so none of them starts or ends a gap even after confirm_date. Gap flags carry computed.excluded_records and the sentence 'Intake form on March 5, 2026 is not a treatment visit, so it does not start or end a gap.' in explanation and why (api.md updated). How verified: tests/unit 2559 passed; evals fixture gap P/R 1.000/1.000, same 25 packets' gap dates/days/flags unchanged; lib09 confirm record 4 stays Gap of 42 days, gap_changes []. Left: qa to update lib11 expected lines (card note); frontend may show computed.excluded_records. Surprised: conflicts.py and pipeline._accident_year still use kind=encounter, so an intake form can count as first treatment there (not in scope).\"\n$B move T-116 in_review --agent backend"
}
````

### User / tool · 2026-11-02T09:35:55.555Z

**tool result**
````
T-116: commit c1b44be recorded
AC 1 checked: tests/unit/test_t116_gap_endpoints.py (49 tests incl. all 25 golden+library gap tables unchanged, lib09 confirm keeps 42 days with why 'Intake form on March 5, 2026 is not a treatment visit...'); tests/unit 2559 passed; python -m evals.run fixture: gap precision/recall 1.000/1.000 (evals/reports/20261102T093441Z.md); lib11 record lists change, posted for qa
handoff written on T-116
T-116: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:35:57.723Z

T-116 is in `in_review` (commit c1b44be): only treatment encounters can now start or end a gap, so lib09 stays at 42 days after confirming record 4, and the gap's why names the intake form (`tests/unit` 2559 passed; fixture eval gap precision/recall 1.000/1.000).

Only the lib11 record lists change. Its intake form (record 6) shares record 5's date, so it stops being an endpoint, and I posted the exact lines on the card for qa. I did not touch `evals/golden`.
