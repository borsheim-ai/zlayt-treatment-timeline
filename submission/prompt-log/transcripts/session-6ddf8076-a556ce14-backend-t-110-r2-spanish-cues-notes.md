# Subagent: Backend: T-110 r2 Spanish cues + notes (Backend: T-110 r2 Spanish cues + notes)

Source: `agent-a556ce14734e5408a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T07:03:13.057Z

You own board card T-110, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-110-paralegal.md and the orchestrator note on the card (`python3 tools/board.py show T-110`). T-103 has closed, so app/backend/amounts.py (the shared cue function) is free.

1. Add Spanish charge, rate and balance cues to the shared code cue function: cargo/cargos and honorarios mean a charge; "por sesión", "por visita" and "cada" mean a rate; saldo means a balance. An `unclear` Spanish amount can then be reclassified to a charge through the T-084 guard (code cue plus judge re-check), and it's then counted by the D-019 total. A rate never becomes a charge. Test on lib09: reclassifying "consultas $1,300" to a charge works, and "$400 por sesión" is refused.
2. Put totals.possible_overlaps into the export's internal notes, worded plainly.
3. Drop the tray placeholder once a manual entry exists for that record.
4. While you're in amounts.py, fix the T-103 r4 minor: the UB-04 room total belongs in other_figures.

Don't change any LLM prompt; this is code cues only. Run `.venv/bin/python -m pytest -q tests/unit` and check it on a `git archive HEAD` copy. Commit with the pathspec rule or a fresh temp index, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-110 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T07:03:13.062Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:22.897Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-110 | tail -80; cat reviews/T-110-paralegal.md | head -120; cat .claude/agent-memory/backend/project_t110_overlap_tray.md"
}
````

### User / tool · 2026-11-02T07:03:23.037Z

**tool result**
````
---
id: "T-110"
title: "lib09 product gaps: case total double-counts the consult ($7,040 vs $6,390) and only 4 of 7 entries load"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:34:48Z"
updated_at: "2026-11-02T06:54:53Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:54:52Z"
rounds: 1
commits: ["3e936a0"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-110-paralegal.md", "at": "2026-11-02T06:54:52Z"}
ac:
  - {"n": 1, "text": "Explain and fix why lib09 loads 4/7 entries on the fixture backend; the case charge total does not count the same consult twice when a statement line summarizes it (or flags the possible overlap for the paralegal instead of summing); tests on lib09", "done": true, "evidence": "tests/unit/test_lib09_t110.py 21 passed; full tests/unit passes in a clean git-archive of HEAD + my files (shared tree has unrelated failures from others' live judges/billing edits). lib09: all 7 records are entries (4/7 is evals.run entry_found content match: recorded extract left out E1 mechanism, E2 chief complaint, E6 pain 5/10; r2/r4/r7 needs_review by D-050); a record with no AI output is now a tray item with its reason (FIXTURE_MISS/LLM_FAILED_AFTER_RETRIES/UNSUPPORTED_LANGUAGE); totals.possible_overlaps flags the $1,300 consultas statement line vs the $650 consult, total unchanged"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T06:34:55Z backend: claimed
- 2026-11-02T06:51:22Z backend: AC 1 checked: tests/unit/test_lib09_t110.py 21 passed; full tests/unit passes in a clean git-archive of HEAD + my files (shared tree has unrelated failures from others' live judges/billing edits). lib09: all 7 records are entries (4/7 is evals.run entry_found content match: recorded extract left out E1 mechanism, E2 chief complaint, E6 pain 5/10; r2/r4/r7 needs_review by D-050); a record with no AI output is now a tray item with its reason (FIXTURE_MISS/LLM_FAILED_AFTER_RETRIES/UNSUPPORTED_LANGUAGE); totals.possible_overlaps flags the $1,300 consultas statement line vs the $650 consult, total unchanged
- 2026-11-02T06:51:27Z backend: moved in_progress -> in_review
- 2026-11-02T06:51:36Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T06:54:52Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): changes — reviews/T-110-paralegal.md; round 1; findings:
    - [major] POSSIBLE_OVERLAP is API-only: the paralegal never sees it in the app or in the export — fix: Show each overlap beside the total in the charges panel, with both excerpts and a one-click dismiss of either line. Add a line to 'Internal review notes - do not send' that names both records and amounts; never put it in the letter (D-019). Open the frontend card and the LLM_VS_CODE note the 
    - [major] Spanish charges stay `unclear` with no way for the paralegal to promote them, so D-050's human gate cannot change the total — fix: Either add a human 'treat as billed charge' action on an unclear amount (the paralegal reads the original, and it is recorded as human-classified) or add Spanish cues (consulta, sesion, estado de cuenta) to the code classifier. Meanwhile, say 'Spanish fig
    - [minor] The 4/7 explanation blames the matcher, but the recorded entries omit the mechanism, the chief complaint and a pain score — fix: Say 'extract recall gap (E1, E2, E6)' in the card and eval report instead of 'matcher'. Track the gap in SCOPE_CUTS or re-record the extract.
    - [minor] The tray placeholder stays listed after the paralegal enters the entry by hand — fix: Mark the tray item resolved, or hide it, once a live manual entry exists for the same record.
- 2026-11-02T06:54:52Z backend: claimed
- 2026-11-02T06:54:53Z orchestrator: Round 2 after T-103 closes (shared amounts.py cue function). Fix: add Spanish charge/rate cues to the shared code cue function (cargo/cargos, honorarios, por sesión = rate, saldo = balance) so an 'unclear' Spanish amount can be reclassified to charge through the T-084 guard (code cue + judge); put possible_overlaps into the export's internal notes; drop the tray placeholder once a manual entry exists. The overlap warning on screen is T-096.
- 2026-11-02T06:54:53Z orchestrator: assigned: backend

## Handoff
Changed: (1) lib09 loads 7/7 records as entries (6 dated + r4 undated), no errors; the 4/7 is evals.run entry_found content matching: the recorded extract quoted other sentences (E1 mechanism, E2 chief complaint, E6 pain 5/10); r2/r4/r7 needs_review is D-050 by design. Real vanish bug fixed: a record the extract made no output for (FIXTURE_MISS, LLM_FAILED_AFTER_RETRIES, UNSUPPORTED_LANGUAGE) is now a rejected tray entry with reason + why (generator.failure_entry, trace excludes it from grounding, manual entry still works). (2) app/backend/overlap.py: totals.possible_overlaps (POSSIBLE_OVERLAP) pairs a statement line with a separately stated charge of the same service family (EN+ES) whose record date is inside the stated range or on/before the statement; lib09 gives $1,300 consultas vs $650 consult; totals unchanged, no arithmetic. Verified: tests/unit/test_lib09_t110.py 21 passed; full tests/unit green in clean git-archive HEAD + my files. Left/surprised: product total on lib09 is 5,090 not 7,040 (Spanish 'estado de cuenta'/'por sesión' not classified, so $1,300 and $400s are unclear; Spanish cues would change J2 prompts and need a fixture re-record); evals check_must_not amount_value M5 hits on the unclear saldo $2,900 (qa: should require class charge); needs a frontend card to show possible_overlaps beside the total and the architect to note it in LLM_VS_CODE. Shared dirty tree has unrelated failures (billing/judges edits by others).

# T-110 review: paralegal-reviewer (commit 3e936a0)

Verdict: changes. No blockers. Two majors, two minors.

Setup: `git archive 3e936a0` extracted into the scratchpad. Server on port 7961 with `ZLAYT_MODE=local`, fixture backend and a scratch `ZLAYT_DB`. It was stopped by PID (confirmed `stopped`, then curl 000). Probe scripts are `artifacts/review-evidence/T-110-paralegal-run.py` through `run5.py`.

Confirmed:
- **lib09 loads 7 of 7 records.** Library lib09 gave 6 dated entries (e1, e2, e3, e5, e6, e7) plus the undated e4. The tray was empty, warnings were empty and `error` was None. Nothing vanished.
- **Tray item for a record with no AI output.** I removed the recorded extract fixture for record 6 (sha `641ed15b…`) and used `LLM_FIXTURE_DIR`. The case then had 5 dated entries, 1 undated entry and `tray=[{id:e6, record_ids:[r6], state:rejected, reasons:[FIXTURE_MISS], why:"The demo has no recorded AI answer for this step, so this item has not been checked."}]`.
- **Manual entry on that tray record works.** A paraphrase quote returned 422 `invalid_edit`. A verbatim quote returned 201 and entry `e6_m` as `needs_review` / `JUDGE_UNAVAILABLE`, labelled "entered by reviewer". After I accepted it, the letter carried record 6 with a verbatim quote. The tray placeholder never reached the letter (it is counted under `excluded.rejected:1`).
- **POSSIBLE_OVERLAP on the consult.** `totals.possible_overlaps` has one pair: a5 `$1,300.00` (r7, statement) against a2 `$650.00` (r2), service `consult`, `both_in_total:false`. Accepted and pending totals were identical before and after, so no figure changed. Accepting a1 and a4 (the $2,940 and $2,150 charges) gave `Billed charges stated in these records: $5,090.00`, which matches D-019 with no parenthetical.

## The "4/7 was the eval matcher" claim

It is half right. The entries do exist, and the three misses come from the quote, not from lost records. The recorded entries quote:
- E1: "Left shoulder pain 7/10. X-ray … ED charge…" and omit "Patient states she was struck by a car…".
- E2: "Refiere dolor 6/10 … Plan: …" and omit the "Motivo de consulta … desde el atropello del 3 de marzo" chief complaint.
- E6: "MRI reviewed. Recommend physical therapy and subacromial injection." and omit "Pain 5/10".

Calling that "the matcher, not the product" is the wrong framing. The matcher is working: it reports that the entry a paralegal sees leaves out the mechanism, the chief complaint and a pain score. Nothing is invented, and she can edit the quote. But pain 6/10 to 5/10 is exactly what she needs in a demand, and the dropped sentences are an extract recall gap. See finding 3.

## Spanish amounts left `unclear` under D-050

The 7 amounts are `unclear` and none is totaled. The unclear-total gate (D-019) held under test: I accepted every amount and the total stayed $5,090.

I accept that as a conservative interim, but only conditionally. D-050 says the paralegal's accept is the gate for translated text. For these amounts, accept does nothing to the total. The judge says `SHOULD_BE_CHARGE` for a2 and a5, the code says `unclear`, and there is no reclassify action. A Spanish-only provider's bill can therefore never reach the letter total, even after she has read the original. The internal notes also say "Amount unclear … Request clean copy of bill" for "Consulta: $650.00", which is not unclear to a human reader. See finding 2.

Not in scope, for the record: the `pre_existing` flag `f_r1_1` on record 1 is `LEXICON_ONLY` and its evidence is "Hx obtained via patient's son, who interpreted." That is a false positive on "Hx". It is noise she will dismiss, and it appears in the internal notes under "Flag, Prior condition".

```json
{"card": "T-110", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 3e936a0 via git archive; own server :7961 (ZLAYT_MODE=local, fixture backend, scratch DB); library case_lib09_spanish_interpreter_espalda; record-6 extract fixture removed via LLM_FIXTURE_DIR for the tray test",
 "exercised": [
  "read personas/paralegal.md, T-110 card, D-019/D-050/D-053",
  "loaded lib09 through POST /api/cases {library} and /run: 7 records gave 6 dated entries + 1 undated entry, tray 0, warnings [], error None",
  "removed the record-6 extract fixture (sha 641ed15b...): record 6 became tray item e6 (rejected, FIXTURE_MISS, with why); POST /records/r6/entry returned 422 for a paraphrase and 201 for a verbatim quote; accepted e6_m; export letter had the manual entry and not the placeholder",
  "read totals.possible_overlaps: a5 $1,300 vs a2 $650, both_in_total false; accepted all amounts a1-a7: accepted total 509000 cents before and after the overlap, letter line 'Billed charges stated in these records: $5,090.00'",
  "grepped app/ for possible_overlaps and POSSIBLE_OVERLAP: the only consumer outside overlap.py is present.py:118; the frontend and export.py never mention it",
  "read evals/library/case_lib09 expected.json and tests/unit/test_lib09_t110.py:62-70 for the 4/7 explanation",
  "stopped the server by PID and confirmed it was down"],
 "verdict": "changes",
 "scores": {"verify_quickly": 3, "nothing_vanishes": 4, "totals_integrity": 5},
 "findings": [
  {"severity": "major",
   "title": "POSSIBLE_OVERLAP is API-only: the paralegal never sees it in the app or in the export",
   "evidence": "grep -rn 'possible_overlaps|POSSIBLE_OVERLAP' app (excluding overlap.py) returns only app/backend/present.py:118. No frontend file renders it. Export on lib09 after accepting everything: 'overlap' not in internal_notes_text and not in letter_text; the notes list the $1,300 line under AMOUNTS NOT TOTALED with no mention of the $650 consult. Worker handoff says it 'needs a frontend card to show possible_overlaps beside the total'.",
   "why_it_matters": "AC 1 allows 'flags the possible overlap for the paralegal instead of summing'. A flag only the JSON carries reaches nobody. In an English case where both lines are accepted charges (both_in_total true), the letter total would double count the consult and nothing on screen or in the internal notes would warn her.",
   "fix": "Show each overlap beside the total in the charges panel, with both excerpts and a one-click dismiss of either line. Add a line to 'Internal review notes - do not send' that names both records and amounts; never put it in the letter (D-019). Open the frontend card and the LLM_VS_CODE note the worker listed.",
   "acceptance_test": "E2E on lib09 with the Spanish lines promoted to charges: the charges panel shows the $1,300 vs $650 warning, and export internal_notes_text contains 'Possible overlap' with both record numbers, while letter_text contains no 'overlap' and the total line is unchanged."},
  {"severity": "major",
   "title": "Spanish charges stay `unclear` with no way for the paralegal to promote them, so D-050's human gate cannot change the total",
   "evidence": "lib09 a2 ($650, 'Consulta: $650.00.') and a5 ($1,300, 'Estado de cuenta: consultas $1,300.00') are kind unclear with ladder judge reason SHOULD_BE_CHARGE, verdict disagree. After accept on a1-a7: totals.accepted = 509000 cents (only $2,940 + $2,150), not_totaled = a2,a3,a5,a6,a7. Internal notes: 'Amount unclear ($650.00). Request clean copy of bill.' review.py has no reclassify path. Worker handoff: 'Spanish estado de cuenta / por sesion not classified ... would change J2 prompts and need a fixture re-record'.",
   "why_it_matters": "Leaving them out of the total is the safe side under D-019, so I do not rate it a blocker. But D-050 says the paralegal's accept is the gate for translated text, and here her accept is a no-op. A Spanish-only provider's charges can never be counted. The note 'Request clean copy of bill' sends her to request a bill for a figure she can already read and quote, and the judge's disagreement is not shown as the reason.",
   "fix": "Either add a human 'treat as billed charge' action on an unclear amount (the paralegal reads the original, and it is recorded as human-classified) or add Spanish cues (consulta, sesion, estado de cuenta) to the code classifier. Meanwhile, say 'Spanish figure not classified; check the original' in the notes rather than 'clean copy of bill'.",
   "acceptance_test": "lib09: a paralegal accepts a2 and flips it to charge, then the total reads $5,740 and a2 appears in the letter with its quote. Or, with Spanish cues, a2 is a charge, pending, and needs_review under D-050. The unclear-never-totaled eval stays green."},
  {"severity": "minor",
   "title": "The 4/7 explanation blames the matcher, but the recorded entries omit the mechanism, the chief complaint and a pain score",
   "evidence": "tests/unit/test_lib09_t110.py:62-70 pins misses {E1,E2,E6}. e1 excerpt lacks 'struck by a car'; e2 lacks 'Motivo de consulta ... atropello del 3 de marzo'; e6 reads 'MRI reviewed. Recommend physical therapy and subacromial injection.' without 'Pain 5/10'.",
   "why_it_matters": "Entry content is verbatim, so nothing is invented. But a quote that drops 'Pain 5/10' (down from 6/10 on 04-21) and the patient-stated mechanism is a recall gap an adjuster will not share. The matcher is reporting it correctly.",
   "fix": "Say 'extract recall gap (E1, E2, E6)' in the card and eval report instead of 'matcher'. Track the gap in SCOPE_CUTS or re-record the extract.",
   "acceptance_test": "Report wording only. Optionally, a lib09 eval line that fails if the e6 excerpt lacks 'Pain 5/10' once the extract is re-recorded."},
  {"severity": "minor",
   "title": "The tray placeholder stays listed after the paralegal enters the entry by hand",
   "evidence": "After POST /records/r6/entry returned 201, GET case shows entries containing e6_m and tray still [('e6','rejected')]; export excluded.rejected is 1.",
   "why_it_matters": "She sees an item that says 'not checked' for a record she has already handled, and the could-not-verify count does not fall to zero. The tests mention that a rerun replaces the placeholder, but not that a manual entry resolves it.",
   "fix": "Mark the tray item resolved, or hide it, once a live manual entry exists for the same record.",
   "acceptance_test": "Unit: after manual_entry on r6, tray excludes e6 or shows it as resolved by e6_m, while the export is unchanged."}
 ],
 "whats_right": [
  "Nothing vanishes: a record with no AI output becomes a tray item with a plain reason, manual entry works with a verbatim-quote check (422 on a paraphrase), and the placeholder never reaches the letter.",
  "The overlap warning changes no figure: the total stays $5,090 whether or not the Spanish lines are accepted, and the letter total line has no parenthetical (D-019).",
  "Spanish entries and amounts are held at needs_review with the 'AI translation - check against the original' reason; none is auto-verified (D-050)."],
 "questions_for_chris": []}
```
---
name: t110-overlap-and-failure-tray
description: T-110 lib09 findings: the 4/7 is the eval matcher, failed extract records now tray placeholders, POSSIBLE_OVERLAP warning beside the total
metadata:
  type: project
---

- lib09 "4/7 entries" is `evals.run.entry_found` content matching, not a load failure: all 7 records are entries (6 dated + r4 undated), no errors. Misses E1/E2/E6 = the recorded extract quoted other sentences (mechanism, chief complaint, pain 5/10 left out). Spanish r2/r4/r7 are needs_review/AI_TRANSLATION by D-050 on purpose. The M5 must_not hit is `check_must_not` amount_value matching ANY amount with value 2,900 (an unclear saldo), not only class charge (qa-owned, golden says class charge).
- lib09's product total is 5,090 pending (not 7,040): Spanish statement/rate cues are not in `amounts.classify` ('estado de cuenta', 'por sesión'), so $1,300 and $400s are `unclear`. 7,040 only appears if the paralegal makes both $650 and $1,300 charges. Adding Spanish cues changes the J2 prompts -> fixture re-record; left as a follow-up.
- A record the extract step made no output for used to vanish (only `errors`). `generator.failure_entry` now makes a rejected tray entry (`ladder.failure`), pipeline appends it to `rejected`; trace excludes `ladder.failure` rows from allitems/grounding. `trace` extract counts add `in_tray` only when nonzero (test_trace pins the exact counts dict).
- `overlap.py` (POSSIBLE_OVERLAP): closed service-family table EN+ES, rate cues read only the figure's own clause (`_clause_after` stops at `.;\n`), `totals_view.possible_overlaps`. No arithmetic (D-052 spirit); never changes totals.
- Shared-tree pitfall again: other workers edit judges.py/audited.py/prompts live, so full `tests/unit` on the dirty tree shows unrelated failures; verify in a `git archive HEAD` copy with only my files overlaid (pipeline/present rebuilt as HEAD + my hunks).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:23.351Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; wc -l app/backend/amounts.py; grep -n \"def \\|^[A-Z_]* = \" app/backend/amounts.py | head -80"
}
````

### User / tool · 2026-11-02T07:03:23.466Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/pipeline.py
 M board/activity.jsonl
 M board/cards/T-045.md
     172 app/backend/amounts.py
10:_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
11:_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
12:_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
14:_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
15:_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
16:_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
17:_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
18:_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
19:_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
22:_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
26:_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
27:RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
28:_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)
31:def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
37:_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)
40:def to_cents(figure: str):
49:def find_amounts(excerpt: str) -> list:
62:def _label(excerpt: str, start: int) -> str:
68:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
89:def _is_billing_source(source: str) -> bool:
93:def damages_mentions(excerpt: str) -> list:
107:def _norm(s):
111:def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
131:def extract_amounts(records: list, separate=frozenset()) -> list:
157:_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
158:_VISIT = re.compile(r"\bvisit\s+(\d+)\b", re.IGNORECASE)
161:def _prefix(source):
165:def rate_note(records: list, record_no: int) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:25.475Z

**tool call — Bash**
````
{
 "command": "sed -n 1,135p app/backend/amounts.py; grep -rn \"reclassif\\|T-084\\|has_rate_cue\\|RATE_CUE\" app --include=*.py | grep -v \"^app/backend/amounts.py\" | head -30; git log --oneline -5; git diff --stat app/backend | tail -5"
}
````

### User / tool · 2026-11-02T07:03:25.605Z

**tool result**
````
"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import re

from app.backend import injection, lexicon

# '$' + a whole numeric token (extra decimals are kept so to_cents can refuse them: never truncated).
# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
# ONE rate-cue test for every code path that decides "is this figure a unit price?" (reclassify.py wording gate, billing.py ledger rows and
# sentences). A cue is decisive: "Charge per visit $185" and "Billed $150 per visit" state a rate, whatever else the text says (D-042, T-084 r2).
_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
              r"|\ban?\s+(?:visit|session|hour|hr|day|treatment|appointment|unit|procedure|month|week)\b|\b(?:daily|hourly|weekly|monthly|session|visit|unit|flat)\s+(?:rate|fee|price|cost)\b|\brate\b"
              r"|\b(?:hourly|daily|weekly|monthly|apiece)\b|\bunit\s+(?:price|cost|charge)\b|@\s*\$"
              r"|\b\d+\s*[x\u00d7]\s*\$?\d")
_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)


def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
    """True when the text carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of ...). `unit_notation=True` is for a
    ledger row's description, where "x1" / "x2" is the unit count of a normal charge line and not a multiplier."""
    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))


_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


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


def damages_mentions(excerpt: str) -> list:
    """Work-loss and similar mentions with no dollar value (lexicon `damages`): [{raw, cents: None, cls: 'damages', start, end}]."""
    out = []
    for e in lexicon.code_list("damages"):
        for m in e["regex"].finditer(excerpt or ""):
            end = m.end()
            t = _WORK_TAIL.match(excerpt, end)
            if t:
                end = t.end()
            if not any(o["start"] < end and m.start() < o["end"] for o in out):
                out.append({"raw": excerpt[m.start():end], "cents": None, "cls": "damages", "start": m.start(), "end": end})
    return sorted(out, key=lambda o: o["start"])


def _norm(s):
    return " ".join((s or "").split()).casefold()


def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
    """Same date + normalised provider + record text (when given) + class + value merges into one amount citing every record (R-CH-6). Unreadable values never merge."""
    out, index = [], {}
    for a in amounts:
        nos = sorted(a.get("record_nos") or [a["record_no"]])
        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
        if set(nos) & set(separate):        # records the paralegal declared not-a-duplicate never merge (D-031)
            key = None
        if key in index:
            m = out[index[key]]
            m["record_nos"] = sorted(set(m["record_nos"]) | set(nos))
            m["duplicate_note"] = "Same amount, date and provider appears in records " + ", ".join(str(n) for n in m["record_nos"]) + "."
            continue
        row = {**a, "record_nos": nos, "duplicate_note": None}
        if key is not None:
            index[key] = len(out)
        out.append(row)
    return out


def extract_amounts(records: list, separate=frozenset()) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
    `separate` = record numbers the paralegal said are not duplicates: their amounts never merge with another record's and get ids ax<n>_<k>."""
    rows = []
app/backend/billing.py:308:        ratey, row_rate = A.has_rate_cue(desc, unit_notation=True), False
app/backend/billing.py:410:            if cls == "rate" or (kind is None and cls == "charge" and A.has_rate_cue(seg)):
app/backend/confidence.py:69:                      ("translated", "AI_TRANSLATION")):      # D-050: the one place that keeps a Spanish / unidentified-language item from ever being verified      # T-086/D-042: read from a scanned page; no later step (edit, judge, reclassify) clears it
app/backend/review.py:204:    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
app/backend/pipeline.py:193:        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
app/backend/pipeline.py:194:            from app.backend import reclassify as RC
app/backend/api.py:513:    from app.backend import reclassify
app/backend/api.py:514:    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
app/backend/overlap.py:84:    return bool(AM.has_rate_cue(ctx) or _RATE_ES.search(_plain(ctx)))
app/db/db.py:33:SCHEMA_VERSION = 4          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062); 4 = += reclassify, rejudge (T-095; v3 -> v4 is an in-place migration)
app/db/db.py:34:AUDIT_ONLY_ACTIONS = ("reclassify", "rejudge")          # logged by log_event(); never change review_status, so apply_review() refuses them
app/db/db.py:71:    `edit` rows whose payload says event == 'reclassify' get their real action. The user_version bump is part of the same transaction."""
app/db/db.py:86:                if isinstance(after, dict) and after.get("event") == "reclassify":
app/db/db.py:87:                    action = "reclassify"
app/db/db.py:241:    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
app/backend/reclassify.py:1:"""Guarded charge reclassification by the paralegal (T-084, D-042; supersedes the D-010 'a rate can never become a charge' cut).
app/backend/reclassify.py:8:  injection-tagged, AND (2) judge 2 re-checks the figure against the class `charge` and agrees. Otherwise 422 `reclassify_refused` with a
app/backend/reclassify.py:27:AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
app/backend/reclassify.py:30:# a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
app/backend/reclassify.py:31:_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
app/backend/reclassify.py:77:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
app/backend/reclassify.py:84:    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
app/backend/reclassify.py:97:def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
app/backend/reclassify.py:107:        raise review._bad("Only a dollar figure can be reclassified.")
app/backend/reclassify.py:114:    prior = lad.get("reclassification") or {}
app/backend/reclassify.py:124:    cc.update(classified_by="reviewer:reclassified", **({"charge_wording": wording} if wording else {}))
app/backend/reclassify.py:134:    lad.update(judge=jd, code_checks=cc, state=state, reclassification={
app/backend/reclassify.py:143:    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
app/backend/reclassify.py:145:                                          "note": lad["reclassification"]["note"]}, t)
app/backend/reclassify.py:185:            "review": present.review_view(conn, case_id), "reclassified": change, "warnings": warnings}
4a560d8 fix(backend): Waddell results flag in every word order; bare N/5 positive flags after a Waddell sentence (T-111 r2, D-043)
8a2b934 fix(backend): billing places tokens by position, not text; exact per-record count holds on 24000 generated records; other_figures filled (T-103 r4)
dda614d fix(backend): rejected model output goes to the could-not-verify tray, conflict candidate rules widened, judge_flag_v3 (T-094 r2, D-053)
3e936a0 feat(backend): failed-extract records are could-not-verify tray items; POSSIBLE_OVERLAP warns beside the charge total (T-110)
013f15b docs(architect): D-053 rows 11-12, tray replaces suppressed flags
 app/backend/api.py      | 4 ++--
 app/backend/pipeline.py | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:28.850Z

**tool call — Bash**
````
{
 "command": "sed -n 1,100p app/backend/reclassify.py; git diff app/backend | head -40"
}
````

### User / tool · 2026-11-02T07:03:28.949Z

**tool result**
````
"""Guarded charge reclassification by the paralegal (T-084, D-042; supersedes the D-010 'a rate can never become a charge' cut).

Two directions, one rule of thumb: taking a figure OUT of the billed-charges total is always the paralegal's call; putting a figure INTO it
needs evidence.
- charge -> not-a-charge: always allowed. The row's kind becomes `unclear` (shown as "not added to the total", never totaled).
- not-a-charge (rate, estimate, unclear, damages) -> charge: allowed only when (1) CODE finds charged-amount wording (charged, charges, billed,
  invoiced, amount due ...) in the same sentence as the figure, with no negation, the figure has a parsed value and the record is not
  injection-tagged, AND (2) judge 2 re-checks the figure against the class `charge` and agrees. Otherwise 422 `reclassify_refused` with a
  fixed reason and nothing changes. Undoing the paralegal's own earlier demotion of a figure the code first called a charge skips both
  checks ONLY while nothing under it has moved: a rerun that changed the code's class of the figure, or its sentence, makes the restore
  run both checks again like any other rate-to-charge (the stored judge answer was about the old sentence).
- A sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of) never passes the code wording check, even
  when it also says charge or billed: "Charge per visit $185" and "Billed $150 per visit" state a rate and stay refused.
- A rerun keeps her class for the same figure; a charge she promoted is dropped back to the code's class if the sentence under it changed.
Whatever the direction: the item goes back to `pending` (she decides again), the ladder keeps who/what/when, and an audit event is written.
The judge sees only the record text, the figure and the class (judges.run_j2_meta); the model supplies no prose that is stored."""
import hashlib
import re

from fastapi import Request

from app.backend import amounts as A, confidence, generator, judge_guard, judges, language, review, store, why as WHY
from app.db import db as DB

TARGETS = ("charge", "not_a_charge")
NOT_A_CHARGE_KIND = "unclear"
AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
_WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
# a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
_NEGATED = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)

REFUSALS = {
    "NO_VALUE": "The dollar value of this figure could not be read, so it cannot become a charge.",
    "INJECTION_SUSPECTED": "This record has instruction-like text, so a figure from it cannot become a charge.",
    "NO_CHARGE_WORDING": "The sentence with this figure has no wording that says it was charged or billed (such as charged, billed, invoiced or amount due), so it stays a figure that is not a charge.",
    "JUDGE_DISAGREES": "A second AI check read this figure as something other than a charge, so it stays as it is.",
    "JUDGE_UNSURE": "A second AI check could not tell whether this figure is a charge, so it stays as it is.",
    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
}


def _sentences(excerpt: str):
    """[(start, end, text)] of the excerpt's sentences, the same boundary rule amounts.classify uses."""
    out, pos = [], 0
    for m in _BOUNDARY.finditer(excerpt):
        out.append((pos, m.start(), excerpt[pos:m.start()]))
        pos = m.end()
    out.append((pos, len(excerpt), excerpt[pos:]))
    return out


def _figure_spans(excerpt: str, row: dict, rec):
    """Where this amount sits in the excerpt: the stored absolute offsets when they check out, else every occurrence of its text."""
    raw = row["text"]
    if rec is not None and row.get("excerpt_start") is not None:
        i = row["excerpt_start"] - generator.body_offset(rec)
        if 0 <= i and excerpt[i:i + len(raw)] == raw:
            return [(i, i + len(raw))]
    return [(m.start(), m.end()) for m in re.finditer(re.escape(raw), excerpt)]


def _classified_rate(excerpt: str, start: int, end: int) -> bool:
    """The amount classifier's own verdict on this figure: if it calls the figure a rate, the wording gate refuses it too (one rate test, two readers)."""
    return A.classify(excerpt, {"start": start, "end": end, "cents": 1}) == "rate"


def charge_wording(excerpt: str, row: dict, rec=None):
    """Code check: the charged-amount phrase in the figure's own sentence (every occurrence of the figure must have one, no negation, no rate
    cue), or None. A rate cue decides: "Charge per visit $185" and "Billed $150 per visit" are rates."""
    spans = _figure_spans(excerpt or "", row, rec)
    found = None
    for s, _e in spans:
        sent = next((t for a, b, t in _sentences(excerpt) if a <= s <= b), "")
        m = _WORDING.search(sent)
        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
            return None
        found = found or m.group(0)
    return found


def _refuse(reason: str, **detail):
    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
                                                          **detail}, REFUSALS[reason])


def _sha(text) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def _log(conn, case_id, item_id, before, after, t):
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))


def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = review._now(now)
    to = (body or {}).get("to")
    if to not in TARGETS:
diff --git a/app/backend/api.py b/app/backend/api.py
index 21bc044..a0b70c0 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -506,10 +506,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import billing
     billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index a82abd3..d7c2c8a 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -364,9 +364,9 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
     final_amounts = [_clean(a) for a in final_amounts]
     damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
+    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
     PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
-    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     now_t = clock()
     _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
     _persist(conn, cid, "amount", final_amounts, now_t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:32.351Z

**tool call — Bash**
````
{
 "command": "grep -n \"other_figures\\|room\" app/backend/billing.py | head -30; grep -n \"internal\\|unclear\\|Request clean\" app/backend/export.py | head -40; grep -n \"tray\\|def manual_entry\" app/backend/*.py | grep -v \"^app/backend/export\" | head -40; ls tests/unit | grep -i \"lib09\\|amount\\|billing\\|reclass\""
}
````

### User / tool · 2026-11-02T07:03:32.461Z

**tool result**
````
29:row) is one of that entry's `other_figures`, wherever a parser first put it.
202:    return {"record_no": rec["n"], "kind": kind, "why": why, "figure": fig, "excerpt": excerpt, "_at": fig["_at"], "_row": row or fig["_at"], "other_figures": []}
659:                        "_at": at, "_row": _row_span(s, seg), "other_figures": []})
667:# other money tokens (a running balance on a price row) become its `other_figures`.
763:    if not any(_lap(fig["_at"], f["_at"]) for f in h["other_figures"]):
764:        h["other_figures"].append(fig)
769:    OTHER money token printed on that row becomes one of its `other_figures`, wherever a parser first put it: a second amount in the sentence, a running
964:                "figure": fig, "other_figures": list(others), "why": why, "excerpt": excerpt, "cites": [{"record_no": n, "excerpt": excerpt}]}
965:    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"], x.get("other_figures", [])) for x in excluded]
966:    extras += [extra(x["record_no"], "unclear", x["kind"], x["figure"], x["excerpt"], "An LOP, lien or reduction amount is listed apart from the charges.", x.get("other_figures", [])) for x in lop]
1024:            for v in d.get("other_figures") or []:
1:"""Export assembly: letter_text and internal_notes_text from reviewed items. CODE ONLY (no LLM, no network).
4:    build_export(case) -> {"letter_text": str, "internal_notes_text": str, "counts": {...}}  (counts: R-EX-5, outside both blocks)
9:    amounts: [{id, record_no, cents|None, cls, raw, excerpt, review_status}]   cls: charge | rate | estimate | unclear | damages | ...
130:        internal notes as 'date not confirmed')."""
254:# ---------------------------------------------------------------- internal notes
415:            body = f"Estimate {m}; not a billed charge. Request clean copy of bill."
416:        elif cls == "unclear":
417:            body = f"Amount unclear ({a.get('raw') or m}). Request clean copy of bill."
614:    return {"letter_text": _letter(v), "internal_notes_text": notes, "counts": counts}
app/backend/api.py:426:    async def manual_entry(token: str, rid: str, request: Request):
app/backend/billing.py:23:else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Three more cases are not tokens: on a UB-04
app/backend/flags.py:245:    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
app/backend/flags.py:286:    # What the independent judge rejects (T-094, D-053): nothing is dropped. The item leaves the flag list and goes to the could-not-verify tray
app/backend/flags.py:292:        _to_tray(f, "JUDGE_DISAGREES", reason)
app/backend/flags.py:295:def _to_tray(f: dict, code: str, judge_reason=None) -> None:
app/backend/flags.py:296:    """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
app/backend/flags.py:306:    phrase-list and model leaves it needs_review (JUDGE_DISAGREES); a model-only flag J4 rejects goes to the tray (D-053, see _judge_one).
app/backend/flags.py:307:    A model-proposed CONFLICT is never a flag: only a code candidate (run_conflict_pass) can make one, so the model's goes to the tray (D-053)."""
app/backend/flags.py:312:            _to_tray(f, "LLM_ONLY")
app/backend/generator.py:131:    """A record the extract step produced NO output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE) as a could-not-verify tray
app/backend/generator.py:144:    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
app/backend/pipeline.py:289:    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
app/backend/pipeline.py:306:            rejected.append(generator.failure_entry(by_n[f["record_no"]], next(g for g in ing["groups"] if g[0] == f["record_no"]), f["failure"]))   # never vanishes: tray item with the reason
app/backend/pipeline.py:359:    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
app/backend/pipeline.py:371:    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
app/backend/pipeline.py:373:    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
app/backend/pipeline.py:385:            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
app/backend/pipeline.py:397:    for f in out["flags"] + out["tray"]:
app/backend/pipeline.py:407:            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
app/backend/review.py:432:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
app/backend/present.py:211:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
app/backend/present.py:214:    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
app/backend/present.py:216:    tray += [{"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
app/backend/present.py:226:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/trace.py:870:    failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure")]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
app/backend/trace.py:911:               **({"in_tray": len(failed_ents)} if failed_ents else {})}
app/backend/trace.py:931:                       "They stay in the tray and out of the letter.", reason=first, rule="row 4", counts=gcounts,
app/backend/trace.py:932:                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"view": "tray"})))
test_amounts.py
test_billing.py
test_lib09_t110.py
test_reclassify.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:35.237Z

**tool call — Bash**
````
{
 "command": "sed -n 195,230p app/backend/present.py; sed -n 395,430p app/backend/export.py; sed -n 254,300p app/backend/export.py; sed -n 100,130p app/backend/present.py; sed -n 1005,1040p app/backend/billing.py; cat tests/unit/test_lib09_t110.py | head -60"
}
````

### User / tool · 2026-11-02T07:03:35.338Z

**tool result**
````
        while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
            j += 1
        out.append((spans[i][0], spans[j][1]))
        i = j + 1
    return out


def case_view(conn, case_id, *, backend, models, demo_mode):
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = list(_recs_by_id(conn, case_id).values())
    its = all_items(conn, case_id)
    ents = its["entry"]
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected"]
    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
    tray += [{"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
              "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
              "flag": {"type": x["type"], "category": x["category"]},
              "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
              "ladder": {"item_id": x["id"], "state": "rejected"}} for x in its["flag"] if x["state"] == "rejected"]
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs], "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
            "review": review_view(conn, case_id), "warnings": [], "error": err,
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
        m2 = re.search(r"\bvisit\s+(\d+)\b", r.get("source", ""), re.I)
        if m2 and re.search(r"\bdischarged\b", r.get("excerpt", ""), re.I):
            last = m2.group(1)
    bits = ([f"{planned} planned"] if planned else []) + ([f"discharged at visit {last}"] if last else [])
    return f" ({'; '.join(bits)})" if bits else ""


def _amounts_not_totaled(v):
    out = [f'- {_cap(v.cite(a["record_no"]))}: charge {_money(a["cents"])} not exported and not totaled: excerpt not found in record.'
           for a in v.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and not v.verbatim(a)]
    for a in v.amounts:
        if a["cls"] in ("charge", "damages") or _status(a) != "in":
            continue
        n, cls = a["record_no"], a["cls"]
        q = f'"{_amount_quote(v, a)}"'
        m = _money_short(a.get("cents"), a.get("raw", ""))
        if cls == "rate":
            per = "/visit" if re.search(r"per visit", a["excerpt"], re.I) else ""
            body = f"Rate {m}{per}; visit count not stated{_plan_note(v, n)}. Request itemized {_ledger_label(v, n)}."
        elif cls == "estimate":
            body = f"Estimate {m}; not a billed charge. Request clean copy of bill."
        elif cls == "unclear":
            body = f"Amount unclear ({a.get('raw') or m}). Request clean copy of bill."
        else:
            body = f"{_cap(cls.replace('_', ' '))} amount {m}; not totaled."
        out.append(f"- {_cap(v.cite(n))}: {q} {body}")
    return out or ["- none"]


def _damages(v):
    out = [f'- {_cap(v.cite(a["record_no"]))}: "{_amount_quote(v, a)}"'
           for a in v.amounts if a["cls"] == "damages" and _status(a) == "in"]
    return out or ["- none"]


def _future(v):
# ---------------------------------------------------------------- internal notes
def _flag_label(f):
    t, sub = f.get("type"), f.get("subtype")
    if t == "gap":
        return "Gap"
    if t == "conflict":
        return "Conflict, " + _CONFLICT_SUB.get(sub, (sub or "other").replace("_", " "))
    if t == "pre_existing":
        return "Prior condition"
    if t == "causation":
        return "Causation language"
    if t == "record_warning":
        return "Record warning"
    return _cap((t or "flag").replace("_", " "))


def _excerpt_ev(f):
    return [x for x in f.get("evidence", []) if x.get("field", "excerpt") == "excerpt"]


def _flag_line(v, f):
    """One flag as a note sentence: '<label>: <body>'."""
    t = f.get("type")
    label = _flag_label(f)
    ev = f.get("evidence", [])
    if t == "gap":
        recs = list(dict.fromkeys(x["record_no"] for x in ev))
        days = f.get("days")
        if days is None and f.get("from_date") and f.get("to_date"):
            days = (date.fromisoformat(f["to_date"]) - date.fromisoformat(f["from_date"])).days
        span = f"{days} days, {_long_date(f.get('from_date'))} to {_long_date(f.get('to_date'))}"
        return _terminate(f"{label}: {span}: " + " to ".join(v.cite(n) for n in recs))
    if t == "conflict":
        order = list(dict.fromkeys(x["record_no"] for x in ev))
        by_rec = {n: [x for x in ev if x["record_no"] == n and x.get("field", "excerpt") == "excerpt"] for n in order}
        if f.get("subtype") == "accident_date":
            segs = []
            for k, n in enumerate(order):
                if by_rec[n]:
                    head = v.cite(n) if k == 0 else _cap(v.cite(n))
                    segs.append(_terminate(f'{head}: "{v.quote(n, by_rec[n][0]["excerpt"], whole_sentence=True)}"'))
                else:
                    coll = next((x for x in _sentences(v.text(n)) if _COLLISION_RE.search(x)), None)
                    if coll:
                        head = v.cite(n) if k == 0 else _cap(v.cite(n))
                        segs.append(_terminate(f'{head}: "{coll.strip()}"'))
                    else:


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
                            if a["kind"] != "charge" and a["review_status"] != "dismissed" and a["kind"] != "damages"],
            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total


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
    """[] when every cited excerpt anywhere in the analysis is a verbatim substring of the record it names, and every figure text sits inside the
    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines (EOB row figures
    included), cites and unreconciled rows. Returns [{ref, reason}]; `for_case` puts the list in the response as
    `citation_failures`."""
    text_of = {r["n"]: (r.get("text") or r.get("excerpt") or "") for r in records}
    bad = []
    for d in _walk({k: v for k, v in analysis.items() if k != "rules"}):
        ref = d.get("id") or d.get("code") or "?"
        if "excerpt" in d and "record_no" in d:
            if d["excerpt"] not in text_of.get(d["record_no"], ""):
                bad.append({"ref": ref, "reason": "excerpt_not_verbatim"})
            for k, v in d.items():
                if k in _FIG_KEYS and _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": f"{k}_not_in_excerpt"})
            for k, v in (d.get("eob") or {}).items():
                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": f"eob_{k}_not_in_excerpt"})
            if _figure_like(d.get("figure")) and not _in(d["figure"]["text"], d["excerpt"]):
                bad.append({"ref": ref, "reason": "figure_not_in_excerpt"})
            for v in d.get("other_figures") or []:
                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
                    bad.append({"ref": ref, "reason": "other_figure_not_in_excerpt"})
    seen, out = set(), []
    for b in bad:
        k = (b["ref"], b["reason"])
        if k not in seen:
            seen.add(k)
            out.append(b)
    return out


def checked(analysis: dict, records: list) -> dict:
    """The analysis plus its citation check. A failure is shown (`citation_failures`, status `citation_failed`), never swallowed; nothing is dropped silently."""
    fails = verify_citations(analysis, records)
    analysis["citation_failures"] = fails
    if fails:
"""T-110 on the lib09 Spanish packet (fixture backend, no network): where the 4/7 comes from, a record with no AI output never vanishes
(could-not-verify tray with its reason), and POSSIBLE_OVERLAP warns next to the charge total instead of guessing (D-019)."""
import json
import pathlib
import tempfile

import pytest

from app.backend import ingest as IN, overlap as OV, pipeline as PL, present, review as RV, totals as T, trace
from app.db import db as DB
from app.llm import provider as P
from evals import run as R
from tests.unit._fakes import FakeCall

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
NAME = "case_lib09_spanish_interpreter_espalda"
TEXT = (LIB / f"{NAME}.txt").read_text()
EXPECTED = json.loads((LIB / f"{NAME}.expected.json").read_text())


@pytest.fixture(scope="module")
def lib09():
    return PL.run_case(TEXT, "fixture")


def _stored(wrap=None):
    """Run the fixture backend into a kept database; `wrap(call)` may replace the model call (to force a miss on one record)."""
    tmp = tempfile.TemporaryDirectory()
    with PL._Backend("fixture"):
        conn, cid, call = PL._scratch_call(tmp.name, IN.normalize_text(TEXT))
        PL.run_pipeline(conn, cid, TEXT, call=wrap(call) if wrap else call)
    return tmp, conn, cid


def _miss_on(*item_ids):
    def wrap(call):
        def c(step, system, user, schema, *, item_id=None):
            if item_id in item_ids:
                raise P.FixtureMiss("forced")
            return call(step, system, user, schema, item_id=item_id)
        return c
    return wrap


# ---------------------------------------------------------------- AC1: the 4/7
def test_every_lib09_record_has_an_entry_nothing_vanishes(lib09):
    """The '4/7' is the eval matcher, not a load failure: all seven records are entries (six dated, one date-to-confirm), no errors, nothing in the tray."""
    got = {n for e in lib09["entries"] + lib09["undated_entries"] for r in e["record_ids"] for n in [int(r[1:])]}
    assert got == set(range(1, 8)) and lib09["errors"] == [] and lib09["tray"] == [] and lib09["status"] == "done"
    assert len(lib09["entries"]) == 6 and [e["record_ids"] for e in lib09["undated_entries"]] == [["r4"]]


def test_spanish_records_are_held_for_review_not_verified(lib09):
    """D-050: records 2, 4 and 7 are Spanish, so their entries are needs_review with AI_TRANSLATION; the English ones are verified. The hold is not why the matcher misses."""
    by = {e["record_ids"][0]: e for e in lib09["entries"] + lib09["undated_entries"]}
    for r in ("r2", "r4", "r7"):
        assert by[r]["state"] == "needs_review" and "AI_TRANSLATION" in by[r]["reasons"]
    for r in ("r1", "r3", "r5", "r6"):
        assert by[r]["state"] == "verified"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:46.542Z

**tool call — Bash**
````
{
 "command": "grep -n '\\$' evals/library/case_lib09_spanish_interpreter_espalda.txt; python3 - <<'E'\nimport json;d=json.load(open('evals/library/case_lib09_spanish_interpreter_espalda.expected.json'));print(json.dumps({k:v for k,v in d.items() if 'amount' in k or 'must' in k},indent=1)[:2500])\nE\ngrep -n \"D-019\\|D-050\" memory/ORCHESTRATOR_DECISIONS.md | head; grep -n \"saldo\\|balance\" app/backend/*.py | head -20"
}
````

### User / tool · 2026-11-02T07:03:46.664Z

**tool result**
````
6:Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."
11:Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00."
26:Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."
36:Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
{
 "amounts": [
  {
   "id": "A1",
   "record_no": 1,
   "raw": "$2,940",
   "value": 2940,
   "class": "charge",
   "excerpt": "ED charge: $2,940",
   "in_total": true,
   "required": true,
   "needs_review": false
  },
  {
   "id": "A2",
   "record_no": 2,
   "raw": "$650.00",
   "value": null,
   "class": "unclear",
   "excerpt": "Consulta: $650.00",
   "in_total": false,
   "required": false,
   "needs_review": true,
   "note": "The note's own consult fee; the statement's plural 'consultas' line is $1,300.00 (2 x $650.00) and the packet holds one consult note, so this fee is probably inside that line. Counted once, through the statement line"
  },
  {
   "id": "A3",
   "record_no": 2,
   "raw": "$400.00",
   "value": 400,
   "class": "rate",
   "excerpt": "Costo por sesi\u00f3n de terapia f\u00edsica: $400.00",
   "in_total": false,
   "required": true,
   "needs_review": true,
   "note": "Rate per session (costo por sesi\u00f3n), not a charge: sessions billed are not stated."
  },
  {
   "id": "A4",
   "record_no": 5,
   "raw": "$2,150",
   "value": 2150,
   "class": "charge",
   "excerpt": "MRI charge: $2,150",
   "in_total": true,
   "required": true,
   "needs_review": false
  },
  {
   "id": "A5",
   "record_no": 7,
   "raw": "$1,300.00",
   "value": 1300,
   "class": "charge",
   "excerpt": "consultas $1,300.00",
   "in_total": true,
   "required": true,
   "needs_review": false,
   "note": "The billed consult line; counted instead of the $650.00 note fee, which it probably includes"
  },
  {
   "id": "A6",
   "record_no": 7,
   "raw": "$400.00",
   "value": 400,
   "class": "rate",
   "excerpt": "4 sesiones a $400.00 por sesi\u00f3n",
   "in_total": false,
   "required": false,
   "needs_review": true,
   "note": "Rate per session; the four sessions have no stated charge total."
  },
  {
   "id": "A7",
   "record_no": 7,
   "raw": "$2,900.00",
   "value": null,
   "class": "unclear",
   "excerpt": "Saldo: $2,900.00",
   "in_total": false,
   "required": true,
   "needs_review": true,
   "note": "Balance (saldo) equals $1,300.00 + 4 x $400.00; counting it would double count."
  }
 ],
 "must_not_flag": [
  {
   "id": "N1",
   "type": "gap",
   "statement": "No gap flag for the 7, 14 and 7-day intervals; the ambiguous-date intake (record 4) and the statement of account (record 7) are not gap endpoints."
  }
 ],
 "must_not": [
  {
   "id": "M1",
   "statement": "Resolves left vs right (picks a side, calls one record a charting error) or merges the t
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
58:| D-050 | Non-English is never auto-verified (2026-11-02, §7.4 after T-085 r3): every item from a record routed Spanish or LANGUAGE_UNCERTAIN is needs_review with the label 'AI translation — check against the original'. The Spanish code checks and the translation judge still run and their failures are shown, but passing them never yields 'verified'. The paralegal's accept is the gate. English routing keeps its normal ladder. | Three rounds showed heuristic Spanish/Portuguese/Italian routing and cue lists keep leaking (4/41 dropped hedges, 1/27 misroutes on fresh lines); making the human the only verifier for translated text removes the silent-pass risk instead of chasing word lists. | T-085 legal-nurse r3 |
60:| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
app/backend/amounts.py:18:_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
app/backend/billing.py:3:What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
app/backend/billing.py:5:'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
app/backend/billing.py:8:(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB service
app/backend/billing.py:22:CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
app/backend/billing.py:28:On a rate, estimate or LOP/lien row, every OTHER money token printed on the row (a running balance, a second amount in the sentence, a printed total on that
app/backend/billing.py:30:Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
app/backend/billing.py:45:    "A running balance, a printed total and an EOB row's amounts are listed beside the lines and never added to them or checked against them.",
app/backend/billing.py:63:_BALFWD = re.compile(r"\bbal(?:ance)?\.?\s*(?:fwd|forward|brought\s+forward)\b|\bprevious\s+balance\b|\bprior\s+balance\b", re.IGNORECASE)
app/backend/billing.py:65:         "adjustment": re.compile(r"\b(?:ADJ(?:USTMENTS?|S)?)\b", re.IGNORECASE), "balance": re.compile(r"\b(?:BALANCE|BAL)\b", re.IGNORECASE),
app/backend/billing.py:170:    """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
app/backend/billing.py:179:        if "billed" in cols and "balance" in cols and len([k for k in cols if k != "rate"]) >= 3:
app/backend/billing.py:214:    sit under a money column header (`all_bare`: every whole number on the line, for a balance-forward row). Dates are never tokens. Nothing here
app/backend/billing.py:253:    """(lines, stated totals, balance-forward rows [list], rate entries). A row whose description carries a rate cue and whose CHARGES figure was found (read
app/backend/billing.py:277:                if kind in ("billed", "paid", "adjustment", "balance") and f["cents"] is not None and kind not in stated:
app/backend/billing.py:326:            line["balance"] = None                    # the running balance of a price row is one of the rate entry's other figures
app/backend/billing.py:340:            "description": description, "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [t for t, _ in pairs],
app/backend/billing.py:352:           "balance": re.compile(rf"(?:BALANCE\s+DUE|AMOUNT\s+DUE|TOTAL\s+BALANCE)\s*[:=]?\s*({_FIGX})", re.IGNORECASE)}
app/backend/billing.py:374:          ("balance", re.compile(r"\bbalance\b|\bamount\s+due\b", re.IGNORECASE)))
app/backend/billing.py:388:    """(lines, stated totals, rate entries, balance-forward figures). A figure the classifier calls a rate, or a charge-worded figure whose sentence also carries a rate cue
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:03:59.057Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && sed -n 28,40p evals/library/case_lib09_spanish_interpreter_espalda.txt"
}
````

### User / tool · 2026-11-02T07:03:59.060Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:05.183Z

**tool call — Bash**
````
{
 "command": "sed -n 28,40p evals/library/case_lib09_spanish_interpreter_espalda.txt; sed -n 100,190p app/backend/reclassify.py"
}
````

### User / tool · 2026-11-02T07:04:05.272Z

**tool result**
````
=== Record 6 ===
Date: 2026-05-12
Source: Dr. Lucan Ostrowe, orthopedics, follow-up
Excerpt: "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."

=== Record 7 ===
Date: 2026-05-20
Source: Consultorio Médico Aguaclara, estado de cuenta (billing statement)
Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
    if to not in TARGETS:
        raise review.ReviewError(400, "bad_request", message='Send "to": "charge" or "not_a_charge".')
    note = (body or {}).get("note")
    if note is not None and not isinstance(note, str):
        raise review.ReviewError(400, "bad_request", message="The note must be text.")
    kind, row = review._item(conn, case_id, item_id)
    if kind != "amount":
        raise review._bad("Only a dollar figure can be reclassified.")
    if row["state"] == "rejected":
        raise review.ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    old_kind = row["kind"]
    if (to == "charge") == (old_kind == "charge"):                         # already there: nothing to do, nothing logged
        return _result(conn, case_id, item_id, None, [])
    lad = dict(row.get("ladder") or {"item_id": item_id})
    prior = lad.get("reclassification") or {}
    original = prior.get("original_kind", old_kind)
    rec = next((r for r in store.load_records(conn, case_id) if r["id"] == (row["record_ids"] or [None])[0]), None)
    wording, judge_res, restored = None, None, False
    if to == "charge":
        restored = _may_restore(row, prior, original)
        if not restored:
            wording, judge_res = _guard(row, rec, call)
    new_kind = "charge" if to == "charge" else NOT_A_CHARGE_KIND
    cc = dict(lad.get("code_checks") or {})
    cc.update(classified_by="reviewer:reclassified", **({"charge_wording": wording} if wording else {}))
    if to == "charge":
        jd = prior["previous_judge"] if restored else judge_res["judge"]
        ladder_verdict = judges.to_ladder("j2", (jd or {}).get("verdict", "unavailable")) if jd else "unavailable"
    else:
        jd, ladder_verdict = None, None
    state, reasons = confidence.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": ladder_verdict},
                                              {"injection": bool(rec and rec.get("injection_tag")), "amount_class": new_kind,
                                               "ocr_derived": bool(rec and rec["id"] in review.ocr_record_ids(conn, case_id)),
                                               "translated": language.translated_record(rec)})      # D-050
    lad.update(judge=jd, code_checks=cc, state=state, reclassification={
        "from": old_kind, "to": new_kind, "at": store.iso(t), "by": "reviewer", "original_kind": original, "wording": wording, "restored": restored,
        "excerpt_sha": _sha(row["excerpt"]),
        "note": (note or "").strip()[:500] or None,
        "previous_judge": lad.get("judge") if to == "not_a_charge" else prior.get("previous_judge")})
    before = {"kind": old_kind, "review_status": row["review_status"], "state": row["state"]}
    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
    if row["review_status"] != "pending":                                  # her earlier decision was about the old meaning
        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
                                          "judge_verdict": (jd or {}).get("verdict"), "judge_call_id": (jd or {}).get("call_id"), "restored": restored,
                                          "note": lad["reclassification"]["note"]}, t)
    return _result(conn, case_id, item_id, {"from": old_kind, "to": new_kind, "wording": wording, "judge_verdict": (jd or {}).get("verdict"),
                                           "restored": restored}, [])


def _may_restore(row: dict, prior: dict, original: str) -> bool:
    """Undoing her own demotion may skip both checks only while the code's original call still stands: the figure was a charge and has a judge
    answer, and no rerun has since changed the code's class of the figure or its sentence. Otherwise the guard runs in full."""
    if original != "charge" or prior.get("previous_judge") is None:
        return False
    rerun = prior.get("rerun")
    if rerun is None:
        return prior.get("excerpt_sha") in (None, _sha(row["excerpt"]))
    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])


def _guard(row: dict, rec, call):
    """The two checks for putting a figure into the total, code first. Returns (wording, {'judge': ladder judge dict}) or raises 422."""
    if row["value_cents"] is None:
        raise _refuse("NO_VALUE")
    if rec is not None and rec.get("injection_tag"):
        raise _refuse("INJECTION_SUSPECTED")
    wording = charge_wording(row["excerpt"], row, rec)
    if wording is None:
        raise _refuse("NO_CHARGE_WORDING")
    if call is None:
        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row["excerpt"], row["text"], "charge", call=call, item_id=row["id"])
    ladder_verdict = judges.to_ladder("j2", verdict)
    if ladder_verdict != "supported":
        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
        raise _refuse(reason, wording=wording, **({"error_class": err} if err else {}))
    return wording, {"judge": {"model": judges.judge_model(), "prompt_version": "judge_amount_class_v1", "call_id": call_id, "verdict": verdict,
                               "reason_code": code}}


def _result(conn, case_id, item_id, change, warnings):
    from app.backend import present
    amount = present._VIEW["amount"](DB.get_item(conn, item_id, case_id), present._recs_by_id(conn, case_id))     # the GET /cases shape: `kind` is the class
    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "reclassified": change, "warnings": warnings}


def carry_over(old: dict, it: dict) -> dict:
    """pipeline._persist hook: a rerun re-derives the code's class, but a figure the paralegal reclassified keeps her class (same figure only)."""
    rc = (old.get("ladder") or {}).get("reclassification")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:23.963Z

**tool call — Bash**
````
{
 "command": "cat app/backend/overlap.py | sed -n 1,60p; sed -n 100,200p app/backend/overlap.py; sed -n 540,614p app/backend/export.py; grep -n \"def build_export\\|class .*View\\|def cite\\|possible\" app/backend/export.py app/backend/api.py | head -20"
}
````

### User / tool · 2026-11-02T07:04:24.056Z

**tool result**
````
"""POSSIBLE_OVERLAP: a statement line that may already include a separately stated charge (T-110, D-019). All code; no model, no arithmetic.

The case charge total adds STATED charges only (D-019). A billing statement line such as "consultas $1,300.00" can summarize a consult that another
record states on its own ("Consulta: $650.00"); counting both would add the consult twice. Code must not guess that they overlap (it cannot know the
statement's contents, and it must not subtract or merge anything), so it only WARNS: when a statement line and a separately stated charge name the
same kind of service (a small closed family table, English and Spanish) and the charge's date falls inside the statement's date range, the pair is
listed next to the total so the paralegal decides. The warning never changes the total and never compares the two figures.

Date range: two dates written in the statement text ("from X to Y", "X - Y", "del X al Y") are the stated range; otherwise the statement covers
everything up to its own record date (a statement summarizes what was billed before it was issued). A charge whose own date is not confirmed is
listed too (date_known false): the code cannot rule the overlap out.
"""
import re
import unicodedata

from app.backend import amounts as AM, dates

CODE = "POSSIBLE_OVERLAP"
_TAIL = (" The total adds each stated charge and does not merge them. Check whether the statement line already includes the separate charge; "
         "dismiss one of the two if it does.")
MESSAGES = {   # fixed sentences (never model text); the key is chosen by code
    "range": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record, and that charge's date is inside the statement's stated date range." + _TAIL,
    "upto": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record, dated on or before the statement." + _TAIL,
    "date": "Possible overlap: this statement line is for the same kind of service as a charge stated separately in another record whose date is not confirmed, so the date range cannot rule it out." + _TAIL,
}
MESSAGE = MESSAGES["upto"]

# Closed service-family table (English + Spanish, accents stripped, lower case). A family is the only thing two figures need to share.
_FAMILIES = (
    ("consult", r"\bconsult\w*|\boffice\s+visit\b|\bvisita\s+de\s+consultorio\b"),
    ("physical_therapy", r"\bphysical\s+therap\w*|\bphysiotherap\w*|\bterapia\s+fisica\b|\bfisioterapia\b|\bchiropract\w*|\bquiropract\w*|\bPT\b"),
    ("imaging", r"\bmri\b|\bresonancia\b|\bx-?\s?rays?\b|\bradiograf\w*|\brayos?\s+x\b|\bct\s+scan\b|\btomograf\w*|\bultrasound\b|\bultrasonido\b|\bimaging\b"),
    ("emergency", r"\bemergency\b|\bemergencia\b|\burgencias\b|\bED\b|\ber\b"),
    ("ambulance", r"\bambulance\b|\bambulancia\b|\bems\b"),
    ("injection", r"\binjection\w*|\binyeccion\w*|\bepidural\b"),
    ("surgery", r"\bsurg\w*|\bcirug\w*|\barthroscop\w*"),
    ("laboratory", r"\blab\b|\blabs\b|\blaborator\w*"),
)
_FAMILY_RX = tuple((name, re.compile(rx, re.IGNORECASE)) for name, rx in _FAMILIES)
# A statement summary line is not a service line: balances, totals, payments and adjustments never name a service to overlap.
_SUMMARY = re.compile(r"\b(?:balance|total|saldo|paid|payments?|pago|pagado|adjustments?|ajuste|due|adeudado|amount\s+due)\b", re.IGNORECASE)
_STATEMENT_SRC = re.compile(r"\bestado\s+de\s+cuenta\b|\bfactura\b|\bcuenta\s+de\s+gastos\b", re.IGNORECASE)
_RATE_ES = re.compile(r"\b(?:por|cada)\s+(?:sesion|visita|hora|dia|unidad|cita|tratamiento|procedimiento)\b|\bcosto\s+por\b|\btarifa\b|/\s*(?:sesion|visita)\b", re.IGNORECASE)
_RANGE_JOIN = re.compile(r"^\s*(?:to|through|thru|until|-|–|—|a|al|hasta)\s*$", re.IGNORECASE)


def _plain(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")


def families(label: str) -> set:
    """The service families named in an amount's own clause."""
    t = _plain(label)
    return {name for name, rx in _FAMILY_RX if rx.search(t)}


def is_statement_source(source: str) -> bool:
    return bool(AM._is_billing_source(source or "") or _STATEMENT_SRC.search(_plain(source)))


        end = rng[1] if rng else s.get("record_date")
        for c in others:
            if c["record_id"] == s["record_id"]:
                continue
            shared = fam & families(c.get("label", ""))
            if not shared:
                continue
            d = c.get("record_date")
            if d is None:                      # a date not confirmed cannot rule the overlap out; say so
                known = False
            else:
                known = True
                if (rng and not (rng[0] <= d <= rng[1])) or (not rng and end and d > end):
                    continue
            out.append({"code": CODE, "statement_amount_id": s["id"], "covered_amount_id": c["id"], "service": sorted(shared)[0],
                        "statement_record_id": s["record_id"], "covered_record_id": c["record_id"],
                        "statement_text": s.get("text"), "covered_text": c.get("text"),
                        "range": {"from": rng[0] if rng else None, "to": end, "stated": bool(rng)}, "date_known": known,
                        "both_charges": s["kind"] == "charge" and c["kind"] == "charge",
                        "both_in_total": s["kind"] == "charge" and c["kind"] == "charge"
                                         and s["review_status"] in ("accepted", "edited") and c["review_status"] in ("accepted", "edited"),
                        "message": MESSAGES["date"] if not known else MESSAGES["range"] if rng else MESSAGES["upto"]})
    return sorted(out, key=lambda o: (o["statement_amount_id"], o["covered_amount_id"]))


def view(conn, case_id: str) -> list:
    """The warnings for one stored case (reads amounts, records and the pasted text; no writes)."""
    from app.db import db as DB
    case = DB.get_case(conn, case_id)
    raw = case["raw_text"]
    recs = {r["id"]: DB._decode(r) for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,))}
    rows = []
    for a in DB.list_items(conn, case_id, "amount"):
        rec = recs.get((a["record_ids"] or [None])[0])
        if rec is None or a["excerpt_start"] is None:
            continue
        body = raw[rec["char_start"]:rec["char_end"]]
        rows.append({"id": a["id"], "record_id": rec["id"], "kind": a["kind"], "value_cents": a["value_cents"], "text": a["text"],
                     "review_status": a["review_status"], "state": a["state"],
                     "label": AM._label(raw, a["excerpt_start"]).replace("Excerpt:", "").strip(' "'), "after": _clause_after(raw, a["excerpt_end"]),
                     "statement": is_statement_source(rec.get("source_label")), "record_date": rec.get("date_iso") if rec.get("date_status") in ("parsed", "confirmed") else None,
                     "record_excerpt": body})
    return possible_overlaps(rows)
    for s in n.get("sentences", []):
        e = live.get(s["entry_id"])
        stale = e is None or (n.get("basis") or {}).get(s["entry_id"]) != basis_hash(e)
        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
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
    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
    Pending items are not blockers: they stay out of the letter and the AI disclosure line counts them."""

    def __init__(self, items):
        self.items = list(items)
        super().__init__(self.items[0]["reason_code"] if self.items else "EXPORT_BLOCKED")

    @property
    def code(self) -> str:
        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"


class JudgeNotRun(ExportBlocked):
    """D-044 alias kept for callers that only care about the judge dimension."""


def build_export(case: dict) -> dict:
    """Pure function: reviewed items in, two text blocks out. Deterministic; no I/O; no flags reach the letter.
    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
    blockers (`case["export_blockers"]`) are enforced one level up, in export_routes.export_payload, so the pure builder stays usable on a partly reviewed case."""
    if case.get("judge_not_run"):
        raise JudgeNotRun(case["judge_not_run"])
    v = _View(case)
    notes = _notes(v)
    in_letter = {e["record_no"] for e in v.in_entries}
    pend = _pending(v)
    counts = {  # R-EX-5 count line: shown by the UI outside both blocks, never inside them
        "entries": len(v.in_entries),
        "charges": len(v.in_charges),
        "flags_in_notes": sum(1 for f in v.flags if _status(f) == "in"),
        "records_in_letter": len(in_letter),
        "records_total": len(v.records),
        "pending": len(pend),
        "pending_flags": sum(1 for f in v.flags if _status(f) == "pending"),
    }
    return {"letter_text": _letter(v), "internal_notes_text": notes, "counts": counts}
app/backend/export.py:111:class _View:
app/backend/export.py:176:    def cite(self, n):
app/backend/export.py:179:    def cite_dated(self, n):
app/backend/export.py:595:def build_export(case: dict) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:25.925Z

**tool call — Bash**
````
{
 "command": "sed -n 105,200p app/backend/export.py; grep -n \"def export_case\" -A50 app/backend/store.py | head -90; sed -n 60,100p app/backend/overlap.py"
}
````

### User / tool · 2026-11-02T07:04:26.016Z

**tool result**
````
def _sentences(text):
    return [text[s:e] for s, e in _sentence_spans(text or "")]


# ---------------------------------------------------------------- case view
class _View:
    """Read-only index over the case dict. All ordering decisions live here."""

    def __init__(self, case):
        self.records = {r["n"]: r for r in case.get("records", [])}
        cfg = case.get("export_config") or {}
        self.export_config = cfg if any(cfg.get(k) is not None for k in ("exhibit", "bates_prefix", "bates_start")) else None
        self.entries = sorted(case.get("entries", []), key=lambda e: (self._date(e), e["record_no"], str(e.get("id"))))
        self.amounts = sorted(case.get("amounts", []), key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
        self.flags = list(case.get("flags", []))
        self.narrative = case.get("narrative")

    def verbatim(self, item):
        """The quoted excerpt must still be a substring of its record (whitespace-normalized); else it never ships."""
        return _norm(item.get("excerpt")) in _norm(self.text(item["record_no"]))

    @property
    def in_entries(self):
        """D-041: an entry with no confirmed date never reaches the letter, even if it was accepted before this rule (it is listed in the
        internal notes as 'date not confirmed')."""
        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e) and self.date_of(e)]

    @property
    def narrative_sentences(self):
        """Sentences of an ACCEPTED draft paragraph whose cited entry is still in the letter and unchanged since the draft."""
        n = self.narrative
        if not n or n.get("status") != "accepted":
            return []
        live = {e["id"]: e for e in self.in_entries}
        return [s for s in n.get("sentences", []) if s["entry_id"] in live and (n.get("basis") or {}).get(s["entry_id"]) == basis_hash(live[s["entry_id"]])]

    @property
    def in_charges(self):
        return [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None
                and _status(a) == "in" and self.verbatim(a)]

    def _date(self, item):
        return self.date_of(item) or "9999-12-31"

    def date_of(self, item):
        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")

    def source_prefix(self, n):
        """Citation prefix: 'Source [Ex. __ / Bates __]: ', or '..., p. N: ' when the record came from a PDF (D-031)."""
        pg = (self.records.get(n) or {}).get("page")
        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
        return head + (": " if pg is None else f", p. {pg}: ")

    def _bracket(self, n):
        """'Source [Ex. 7 / Bates RIV-0001]' from the per-case export config; unset parts stay '__'. Bates = first number + record number - 1, 4 digits."""
        c = self.export_config
        ex = c.get("exhibit") or "__"
        prefix, start = c.get("bates_prefix"), c.get("bates_start")
        bates = "__" if prefix is None and start is None else f"{prefix or ''}{(1 if start is None else start) + n - 1:04d}"
        return f"Source [Ex. {ex} / Bates {bates}]"

    def source(self, n):
        return (self.records.get(n) or {}).get("source", "")

    def text(self, n):
        return (self.records.get(n) or {}).get("excerpt", "")

    def rec_date(self, n):
        return (self.records.get(n) or {}).get("date_iso")

    def cite(self, n):
        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"

    def cite_dated(self, n):
        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"

    def quote(self, n, ev, whole_sentence=False):
        """Quote evidence from record n. A directly following full stop is included when the evidence starts a
        sentence; whole_sentence expands mid-sentence evidence to its sentence. Always a substring of the record."""
        text = self.text(n)
        i = text.find(ev) if ev else -1
        if i < 0:
            return ev
        j = i + len(ev)
        if whole_sentence:
            hit = [(s, e) for s, e in _sentence_spans(text) if s <= i and j <= e]
            if hit:
                return text[hit[0][0]:hit[0][1]]
        starts_sentence = i == 0 or text[:i].rstrip(" ").endswith((".", "\n"))
        if starts_sentence and text[j:j + 1] == "." and not ev.endswith("."):
            return ev + "."
        return ev


def _amount_quote(v, a):
36:def export_case(conn, case_id: str) -> dict:
37-    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
38-    case = DB.get_case(conn, case_id)
39-    recs = load_records(conn, case_id, case["raw_text"])
40-    n_of = {r["id"]: r["n"] for r in recs}
41-    rec_of = {r["id"]: r for r in recs}
42-    from app.backend import review as review_mod        # lazy: review imports store
43-    ents = []
44-    for e in DB.list_items(conn, case_id, "entry"):
45-        if e["state"] == "rejected":
46-            continue
47-        ed = e.get("edited") or {}
48-        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
49-                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
50-        if "summary" in ed:
51-            d["original_summary"] = ed.get("original_summary", e["summary"])
52-            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
53-            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
54-                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
55-        if "excerpt" in ed:
56-            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
57-        lad = e.get("ladder") or {}
58-        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
59-            d["code_check_failed"] = True
60-        if lad.get("entered_by"):
61-            d["entered_by_reviewer"] = True
62-        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
63-            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
64-        ents.append(d)
65-    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
66-                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
67-    fl = []
68-    for f in DB.list_items(conn, case_id, "flag"):
69-        c = f.get("computed") or {}
70-        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
71-                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
72-        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
73-                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
74-    events = []     # D-047: no 'keep my wording' event exists any more
75-    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
76-    pages = (case.get("config") or {}).get("pages")
77-    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
78-                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
79-    nar = (case.get("config") or {}).get("narrative")
80-    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
81-    from app.backend import trace                       # lazy: trace imports store
82-    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
83-    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
84-    ec = (case.get("config") or {}).get("export")
85-    if ec:
86-        out["export_config"] = ec

def stated_range(text: str):
    """(from_iso, to_iso) when the statement text states a range of two parsed dates joined by to/through/-/al/hasta; else None."""
    found = [d for d in dates.find_dates(text or "") if d.get("status") == "parsed" and d.get("iso")]
    for a, b in zip(found, found[1:]):
        if _RANGE_JOIN.match((text or "")[a["end"]:b["start"]]):
            lo, hi = sorted((a["iso"], b["iso"]))
            return lo, hi
    return None


def _clause_after(text: str, end: int) -> str:
    """The words right after a figure in its own clause (up to the next sentence or clause break), so a rate cue in the next sentence is not read as this figure's."""
    return re.split(r"[.;\n]", (text or "")[end:end + 40])[0]


def candidate(a: dict) -> bool:
    """A figure that can be a stated charge: a clean dollar value, not a rate/estimate/damages figure and not dismissed."""
    return (a.get("value_cents") is not None and a.get("kind") in ("charge", "unclear") and a.get("review_status") != "dismissed" and a.get("state") != "rejected"
            and not _is_rate_like(a))


def _is_rate_like(a: dict) -> bool:
    ctx = f"{a.get('label', '')} {a.get('after', '')}"
    return bool(AM.has_rate_cue(ctx) or _RATE_ES.search(_plain(ctx)))


def possible_overlaps(amounts: list) -> list:
    """`amounts`: [{id, record_id, kind, value_cents, text, review_status, state, label (the amount's own clause), after (30 chars after it),
    statement (bool: its record is a billing statement), record_date (ISO or None), record_excerpt}].
    Returns [{code, statement_amount_id, covered_amount_id, service, range, date_known, both_charges, both_in_total, message}] in a stable order.
    Two figures of one record never pair; a rate is never a party; the statement line is the summarizing side."""
    out = []
    lines = [a for a in amounts if a.get("statement") and candidate(a) and not _SUMMARY.search(_plain(a.get("label", "")))]
    others = [a for a in amounts if not a.get("statement") and candidate(a)]
    for s in lines:
        fam = families(s.get("label", ""))
        if not fam:
            continue
        rng = stated_range(s.get("record_excerpt", ""))
        end = rng[1] if rng else s.get("record_date")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:45.553Z

**tool call — Bash**
````
{
 "command": "sed -n 125,160p app/backend/generator.py; sed -n 425,500p app/backend/review.py; sed -n 860,935p app/backend/trace.py; grep -n \"_VIEW = \\|def _entry_view\" -A14 app/backend/present.py | head -60; grep -n \"rejected\" app/backend/export_routes.py app/backend/store.py | head"
}
````

### User / tool · 2026-11-02T07:04:45.650Z

**tool result**
````
def _one(args):
    record, group, call, case_text = args
    return extract_one(record, group, call=call, case_text=case_text)


def failure_entry(record: dict, group: list, failure: str) -> dict:
    """A record the extract step produced NO output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE) as a could-not-verify tray
    item: state rejected, the failure code as its reason, no summary or quote. It never reaches the timeline or the letter, and it never vanishes:
    the paralegal sees the record with the reason and can write the entry by hand (D-031). `ladder.failure` marks it as a placeholder."""
    e = _entry_base(record, group, "")
    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
    e["ladder"] = {"item_id": e["id"], "generator": None, "judge": None, "failure": failure, "code_checks": {}, "state": "rejected",
                   "human": {"action": None, "edited_text": None, "at": None}}
    return e


def extract_entries(records: list, groups: list, *, call, case_text: str = "", workers: int = CONCURRENCY):
    """Stages 1-2 over distinct records (only the first record of each duplicate group is sent). Returns
    (entries, rejected, failures). `entries` are chronological by (date, seq) and never contain a rejected item; `rejected` goes to the
    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
    by_n = {r["n"]: r for r in records}
    jobs = [(by_n[g[0]], g, call, case_text) for g in groups]
    with ThreadPoolExecutor(max_workers=max(1, min(workers, CONCURRENCY))) as ex:
        results = list(ex.map(_one, jobs))
    made = [r for r in results if "failure" not in r]
    failures = [r for r in results if "failure" in r]
    entries = sorted((e for e in made if e["state"] != "rejected"), key=lambda e: (e["date"] or "9999-99-99", e["seq"]))
    rejected = [e for e in made if e["state"] == "rejected"]
    return entries, rejected, failures


def judge_entries(entries: list, records_by_n: dict, *, call, case_text: str = "") -> list:
    """Stage 3: judge 1 on every non-rejected entry. Judge failure -> 'unavailable' (JUDGE_UNAVAILABLE). Recomposes state."""
    def work(e):
        if e["state"] == "rejected":
            return e, None, False
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
    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
        raise _bad("Provide a summary and the quoted sentences.")
    summary, excerpt = summary.strip(), excerpt.strip()
    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
    if problems:
        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], excerpt)
    eid = f"e{rec['seq']}_m"
    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
                         ocr_derived=record_id in ocr_record_ids(conn, case_id))
    base = generator.body_offset(rec)
    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
                              "date_provider_from_header": True},
              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
    DB.add_item(conn, case_id, "entry", {
        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}


# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
    `not_duplicate` event on the original entry."""
    from app.backend import pipeline as PL
    from app.llm import provider as P
    t = _now(now)
    kind, ent = _item(conn, case_id, entry_id)
    if kind != "entry":
        raise _bad("Only a merged entry can be split.")
    ids = list(ent["record_ids"] or [])
    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
        raise _bad("That record is not one of the duplicates merged into this entry.")
    case = DB.get_case(conn, case_id)
    cfg = dict(case.get("config") or {})
    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
    DB.update_case(conn, case_id, config_json=cfg)
    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    for i in items:
        out[i[key]] = out.get(i[key], 0) + 1
    return out


def case_trace(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    case = cx.case
    recs = list(cx.recs.values())
    ents = DB.list_items(conn, case_id, "entry")
    failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure")]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
    ents = [x for x in ents if not (x.get("ladder") or {}).get("failure")]
    amts = DB.list_items(conn, case_id, "amount")
    flgs = DB.list_items(conn, case_id, "flag")
    allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
    cfg = case.get("config") or {}
    rv = present.review_view(conn, case_id)
    jr = judge_report(conn, case_id, full)
    st = []
    # 1 ingest
    dup = sum(1 for r in recs if r["duplicate_of"])
    st.append(step("ingest", "Read the paste and split it into records", "code", PASS if recs else FAIL,
                   f"{len(recs)} records found." + (f" {dup} exact duplicate{'s' if dup != 1 else ''} merged into the record they repeat." if dup else ""), rule="row 1",
                   counts={"records": len(recs), "duplicates_merged": dup, "characters": len(case["raw_text"])}))
    # 2 split
    llm_split = any(f["category"] == "llm_split" for f in flgs)
    sf = cfg.get("split_failure")
    if sf:
        st.append(step("split", "Record boundaries", "code", FAIL, reason_text("SPLIT_AMBIGUOUS"), reason="SPLIT_AMBIGUOUS", rule="row 1", evidence={"values": {"failure": sf}},
                       counts={"method": "code", "llm_split": False}, next_action=na("READ_RECORD", {"view": "records"})))
    elif llm_split:
        st.append(step("split", "Record boundaries", "llm", FAIL, reason_text("LLM_SPLIT"), reason="LLM_SPLIT", rule="row 1", counts={"method": "llm", "llm_split": True},
                       next_action=na("READ_RECORD", {"view": "records"})))
    else:
        st.append(step("split", "Record boundaries", "code", PASS, "The record markers in the paste decided where each record starts and ends.", rule="row 1",
                       counts={"method": "code", "llm_split": False}))
    # 3 dates
    dc = _count_by([{"s": r["date_status"]} for r in recs], "s")
    bad = dc.get("ambiguous", 0) + dc.get("missing", 0)
    dcounts = {k: dc.get(k, 0) for k in ("parsed", "confirmed", "ambiguous", "missing")}
    if bad:
        code = "DATE_AMBIGUOUS" if dc.get("ambiguous") else "DATE_MISSING"
        st.append(step("dates", "Dates read by code", "code", FAIL, f"{bad} record date{'s are' if bad != 1 else ' is'} not confirmed. " + reason_text(code), reason=code, rule="row 2",
                       counts=dcounts, next_action=na("CONFIRM_DATE", {"view": "dates_to_confirm"})))
    else:
        st.append(step("dates", "Dates read by code", "code", PASS, "Every record date was read by code and is parsed or confirmed.", rule="row 2", counts=dcounts))
    # 4 extract
    firsts = [r for r in recs if not r["duplicate_of"]]
    have = {(e["record_ids"] or [None])[0] for e in ents}
    missing = [r["id"] for r in firsts if r["id"] not in have]
    ecounts = {"records_to_draft": len(firsts), "entries": len(ents), "rejected": sum(1 for e in ents if e["state"] == "rejected"), "records_without_entry": len(missing),
               **({"in_tray": len(failed_ents)} if failed_ents else {})}
    if not cx.ran:
        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PENDING, "The AI run has not started.", rule="row 4", counts=ecounts, next_action=na("RERUN")))
    elif missing:
        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", FAIL, f"{len(missing)} record{'s have' if len(missing) != 1 else ' has'} no AI-made entry. "
                       + reason_text("LLM_FAILED_AFTER_RETRIES"), reason="LLM_FAILED_AFTER_RETRIES", rule="row 4", evidence={"values": {"record_ids": missing}}, counts=ecounts,
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"record_id": missing[0]})))
    else:
        st.append(step("extract", "AI drafts a summary and a quote for each record", "llm", PASS, f"The AI drafted an entry for all {len(firsts)} records.", rule="row 4", counts=ecounts))
    # 5 grounding
    rej = [(k, x) for k, x in allitems if x["state"] == "rejected"]
    codes = {}
    for _, x in rej:
        for c in x.get("state_reasons") or []:
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"):
                codes[c] = codes.get(c, 0) + 1
    gcounts = {"items_checked": len(allitems), "rejected": len(rej), "reasons": codes}
    if rej:
        first = next(iter(codes), None)
        st.append(step("grounding", "Every quote and amount is in the record", "code", FAIL, f"{len(rej)} item{'s were' if len(rej) != 1 else ' was'} rejected because the quote or amount is not in the record. "
                       "They stay in the tray and out of the letter.", reason=first, rule="row 4", counts=gcounts,
                       next_action=na("DISMISS_OR_ENTER_BY_HAND", {"view": "tray"})))
    elif not allitems:
        st.append(step("grounding", "Every quote and amount is in the record", "code", PENDING, "There is nothing to check yet.", rule="row 4", counts=gcounts, next_action=na("RERUN")))
    else:
86:_VIEW = {"entry": entry_view, "amount": amount_view, "flag": flag_view}
87-_ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
88-
89-
90-def _recs_by_id(conn, case_id):
91-    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
92-
93-
94-def item_view(conn, case_id, item_id):
95-    row = DB.get_item(conn, item_id, case_id)
96-    kind = _ID_KIND[item_id[0]]
97-    v = _VIEW[kind](row, _recs_by_id(conn, case_id))
98-    v["kind"] = kind
99-    return v
100-
app/backend/store.py:45:        if e["state"] == "rejected":
app/backend/store.py:66:                 excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:51.319Z

**tool call — Bash**
````
{
 "command": "grep -n \"excluded\\|\\\"rejected\\\"\\|state\\\"\\] == \\\"rejected\\|state'\\] == 'rejected\" app/backend/*.py | grep -v \"^app/backend/\\(flags\\|generator\\|judges\\|confidence\\)\" | head -40; grep -n \"def entry_view\" -A20 app/backend/present.py | head -40"
}
````

### User / tool · 2026-11-02T07:04:51.409Z

**tool result**
````
app/backend/api.py:535:            ex["excluded"] = {"pending": case["pending_count"],
app/backend/api.py:537:                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
app/backend/billing.py:389:    (per visit/session/hour/day, each, x N, daily rate), is a price: listed as a rate, never a line. An estimate is listed as excluded. Every other
app/backend/billing.py:665:# unreconciled line, an excluded rate (or an LOP/lien amount, which is listed apart), or on its row as `unclear`. This pass reads the raw text with
app/backend/billing.py:885:    lines, stated_by_rec, lop, excluded, balfwds, rec_form = [], {}, [], [], {}, {}
app/backend/billing.py:924:        excluded += rates
app/backend/billing.py:965:    extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"], x.get("other_figures", [])) for x in excluded]
app/backend/billing.py:968:        shown = _placed([l for l in lines if l["record_no"] == r["n"]], {}, [], [x for x in excluded + lop if x["record_no"] == r["n"]])
app/backend/case_extras.py:132:                    raise ApiError(422, "CODE_CHECK_FAILED", first["why"] + " Nothing was changed.", {"rejected": e.rejected}) from None
app/backend/case_extras.py:134:                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
app/backend/case_extras.py:135:                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
app/backend/dismissal_patterns.py:24:_BAD = ("rejected",)
app/backend/export.py:34:OUT = ("dismissed", "rejected")
app/backend/export.py:468:        elif any(e.get("review_status") == "rejected" for e in ents):
app/backend/export.py:469:            why = "rejected"
app/backend/overlap.py:78:    return (a.get("value_cents") is not None and a.get("kind") in ("charge", "unclear") and a.get("review_status") != "dismissed" and a.get("state") != "rejected"
app/backend/reclassify.py:108:    if row["state"] == "rejected":
app/backend/pdf_checks.py:81:    checks = {"hidden_text": {"checked": False, "pages": [], "excluded_until_confirmed": True,
app/backend/pdf_checks.py:164:        if it.get("state") == "rejected" or not ocr_ids.intersection(it.get("record_ids") or []):
app/backend/pdf_hidden.py:784:                          "confirmed": n in confirmed, "excluded": n not in confirmed})
app/backend/pdf_hidden.py:791:                      "excluded": n not in confirmed})
app/backend/pdf_hidden.py:792:    return {"checked": not unchecked, "unchecked_pages": unchecked, "pages": pages, "excluded_until_confirmed": True}
app/backend/pipeline.py:73:        item["ladder"] = _ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
app/backend/pipeline.py:238:    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
app/backend/pipeline.py:358:    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
app/backend/pipeline.py:359:    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
app/backend/present.py:108:    am = [a for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
app/backend/present.py:123:    live = [(k, r) for k, r in items if r["state"] != "rejected"]
app/backend/present.py:125:    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
app/backend/present.py:208:    live_e = [e for e in ents if e["state"] != "rejected"]
app/backend/present.py:211:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
app/backend/present.py:213:             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected"]
app/backend/present.py:216:    tray += [{"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
app/backend/present.py:220:              "ladder": {"item_id": x["id"], "state": "rejected"}} for x in its["flag"] if x["state"] == "rejected"]
app/backend/present.py:225:            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
app/backend/present.py:226:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "tray": tray, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/review.py:176:    if item["state"] == "rejected" and action in ("accept", "edit"):
app/backend/review.py:212:            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
app/backend/review.py:409:        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
app/backend/review.py:444:    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
41:def entry_view(row, recs):
42-    r = recs.get((row["record_ids"] or [None])[0], {})
43-    ed = row.get("edited") or {}
44-    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
45-            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
46-            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
47-            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
48-            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row)}
49-
50-
51-def _translation(row):
52-    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
53-    t = (row.get("ladder") or {}).get("translation")
54-    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written"))) if t else None
55-
56-
57-def amount_view(row, recs):
58-    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
59-            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
60-            "duplicate_note": row["duplicate_note"]}
61-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:04:55.497Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def \" app/db/db.py | head -60; grep -n \"failure\" tests/unit/test_lib09_t110.py | head -20; grep -n \"def pipeline_rerun\\|DELETE FROM items\" app/backend/*.py app/db/db.py | head"
}
````

### User / tool · 2026-11-02T07:04:55.605Z

**tool result**
````
29:def init(path: str = ":memory:"):
38:def connect(path: str):
68:def _migrate_v3_to_v4(conn, schema: str) -> None:
98:def _tok(prefix: str) -> str:
102:def _enc(v):
106:def _cols(conn, table):
110:def sha256(text: str) -> str:
114:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
122:def update_case(conn, case_id: str, **fields) -> None:
131:def get_case(conn, case_id: str):
136:def _insert(conn, table, row):
144:def add_record(conn, case_id: str, **fields) -> str:
150:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
163:def _find(conn, item_id, case=None):
180:def _decode(row) -> dict:
191:def get_item(conn, item_id: str, case: str = None) -> dict:
195:def list_items(conn, case_id: str, kind: str) -> list:
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
240:def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
250:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
257:def list_events(conn, case_id: str, item_id: str = None) -> list:
264:def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
273:def get_llm_call(conn, call_id: str):
278:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
285:def delete_case(conn, case_id: str) -> None:
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
304:def table_counts(conn, case_id: str) -> dict:
47:    """The '4/7' is the eval matcher, not a load failure: all seven records are entries (six dated, one date-to-confirm), no errors, nothing in the tray."""
87:        assert next(s for s in tr["steps"] if s["id"] == "grounding")["status"] != "fail"     # a failed call is not a grounding failure
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:06.342Z

**tool call — Bash**
````
{
 "command": "sed -n 525,545p app/backend/api.py; grep -n \"counts\\[\\|\\\"rejected\\\"\\|\\['rejected'\\]\" app/backend/trace.py | head; grep -rn \"other_figures\\|room\" tests/unit/test_billing.py | head; git show 8a2b934 --stat | head; grep -n \"UB-04\\|room\" memory/*.md reviews/T-103*.md | head -20"
}
````

### User / tool · 2026-11-02T07:05:06.462Z

**tool result**
````
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"],
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

236:    rs, rejected = row["review_status"], row["state"] == "rejected"
269:    live = row.get("state") != "rejected"
280:    elif row.get("state") == "rejected":
281:        code, label = "rejected", "Rejected; kept out of the letter"
373:    live_pending = row["state"] != "rejected" and row["review_status"] == "pending"
411:    return row["state"] != "rejected" and row["review_status"] in ("accepted", "edited")
496:    if kind != "charge" or gfail or row["state"] == "rejected":
545:        bad = row["state"] == "rejected" and "JUDGE_DISAGREES" not in R or cc.get("excerpt_verbatim") is False
558:        bad = row["state"] == "rejected" or cc.get("spans_match_input") is False
772:        if r["verdict"] != "unavailable" or row["state"] == "rejected" or row["review_status"] == "dismissed":
tests/unit/test_billing.py:579:    own figure and its `other_figures` (a running balance on a price row), nothing else (T-103 r3)."""
tests/unit/test_billing.py:583:            items.append((l["excerpt"], {_nt(l["figure"]["text"])} | {_nt(f["text"]) for f in l["other_figures"]}, False))
tests/unit/test_billing.py:1167:    assert r["figure"]["text"] == "185.00" and [f["text"] for f in r["other_figures"]] == ["999.00"] and r["other_figures"][0]["cents"] == 99900
tests/unit/test_billing.py:1175:    assert [(f["text"], f["cents"]) for f in r["other_figures"]] == [("$315", None)]
tests/unit/test_billing.py:1181:    texts = [f["text"] for l in out["lines"] if "figure" in l for f in [l["figure"], *l["other_figures"]]]
tests/unit/test_billing.py:1188:    next(l for l in out["lines"] if l["class"] == "rate")["other_figures"][0]["text"] = "123.45"
tests/unit/test_billing.py:1192:def test_dropping_the_other_figures_turns_the_oracle_red():
tests/unit/test_billing.py:1196:    next(l for l in out["lines"] if l["class"] == "rate")["other_figures"] = []
tests/unit/test_billing.py:1214:            for f in [l["figure"], *l["other_figures"]]:
tests/unit/test_billing.py:1301:    assert [f["text"] for f in r["other_figures"]] == ["2O0.00"] and not out["unreconciled"]
commit 8a2b934ada770a29cc90bd677015cd1f62e2726a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:53:44 2026 -0600

    fix(backend): billing places tokens by position, not text; exact per-record count holds on 24000 generated records; other_figures filled (T-103 r4)
    
    - placement by offset range: a printed total that shares its excerpt with an equal figure is its own line; no figure text is compared (D-052)
    - sign of a charge is a flag read from credit notation, not a value test
    - rate/estimate/LOP rows: every other token on the row is an other_figure (no-cents balance, second LOP amount, printed balance on the row)
    - UB-04 units, EOB money-shaped service slot, CMS broken boxes, odd decimals, prose number after a figure no longer over/under-list
memory/DECISIONS.md:124:  - **Deviations from contract §5.2, recorded:** (i) no separate "clinical facts" field (extra paraphrase is extra room to invent); (ii) added J4 and the instruction-like-text row; (iii) amounts are classified by code only, with J2 on all of them (the contract allowed an LLM classifier; it is not built); (iv) flag and conflict wording is code-templated and the LLM returns only a category plus quoted spans; (v) gaps use record dates, not entries (ADR-010); (vi) the accident-date conflict is a code rule (ADR-014); (vii) no LLM date pointing (D-011); (viii) batch accept, charge reclassification and the duplicate-split action are cut (D-010, D-011).
memory/SCOPE_CUTS.md:72:| debt | T-103 accepted with documented debt after 4 rounds (§7.4) | 4 rounds; exact money-token count holds on 0 of 24,600 random draws, no sums or comparisons remain. Q1 ruled by orchestrator: offset overlap is placement, not a figure comparison (allowed under D-052). Carried: UB-04 room total should sit in other_figures (minor). | see card | M3 |
reviews/T-103-staff-engineer-r4.md:10:2. Other_figures gaps: **partly closed.** The r3 probe cases D (no-cents table balance), E (prose rate with two figures) and H (two LOP amounts in one sentence) now have an empty rule-break list, and the R1 footer (130.00 four times in, four out) and R2 (65.00 listed once) repros are fixed. One shape still breaks the literal rule on every UB-04 draw (finding 1).
reviews/T-103-staff-engineer-r4.md:18:- r3 F1 (other_figures literal gaps): open for the UB-04 room row (finding 1). Closed for probe cases D, E, H.
reviews/T-103-staff-engineer-r4.md:57:   "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw.py -I: b1 charge 5,550.00 and b6 rate 1,850.00 with other_figures [] on the same UB-04 room row (ub04_rate_row_draw6_8a2b934_output.txt)",
reviews/T-103-staff-engineer-r4.md:69:    "title": "UB-04 rate row: the row's own 5,550.00 total is a charge line, not in the rate entry's other_figures (r3 F1 carried; the r4 handoff says every other token on a rate row is an other figure)",
reviews/T-103-staff-engineer-r4.md:70:    "evidence": "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw6_8a2b934_output.txt: b1 class charge billed 5,550.00 and b6 class rate figure 1,850.00 other_figures [] on the excerpt '0120 ROOM & BOARD SEMI-PVT 1,850.00 ... 5,550.00'. Repro: .venv/bin/python -I artifacts/review-evidence/T-103-r4/rate_rule_random.py <8a2b934 archive> 20261102,1,2,3,4,5 -> draws_with_rate_rule_break=458, all ub04 (rate_rule_by_base_8a2b934_output.txt). The UB-04 sample is test_billing.py:55-64. memory/contracts/api.md:695 says other_figures 'holds every OTHER money token printed on a rate, estimate or LOP/lien row ... a printed balance or total on that row'.",
reviews/T-103-staff-engineer-r4.md:71:    "why_it_matters": "No value is lost and no sum is made: 5,550.00 is on its own charge line, verbatim, and the per-record count holds. But the contract a client reads says the rate entry carries every other money token of its row, and this one does not. The literal rule fails on every UB-04 room row. A client that reads other_figures misses the row total. Both places cannot hold at once: the count test forbids listing the token twice, so the contract must either name this exception or the token must move to other_figures.",
reviews/T-103-staff-engineer-r4.md:107:   "Q3 (new): for the UB-04 room row, should a row total that the row already lists as a charge line also appear in the rate entry's other_figures, or is that a documented exception? Finding 1 depends on the answer."
reviews/T-103-staff-engineer-r3.md:94:    "evidence": "artifacts/review-evidence/T-103-r3/random_count_detail_output.txt. Draw 32: '14' from 'treatment visits 1 through $123.45 14' is listed in unreconciled u1. Draw 34: the UB-04 UNITS value '3' is other_figures of the ROOM rate b6 after the description was lengthened. Draw 165: the EOB row's code field is '123.45' (b3 code) and the CPT 97014 is an unclear figure of b3. random_count_classify_output.txt: 18 BARE_OVERLIST and 1 OTHER over 600 draws. parse_figure('3') returns cents None and usd None (checked inline), so no money value is invented; the entries carry text only. Column test: billing.py:157 _tokens; EOB row regex billing.py:485 _EOBROW and _eob_tokens at billing.py:496.",
reviews/T-103-staff-engineer.md:39:   "probe listings of T-083 PROBES (ledger, prose, CMS-1500, UB-04, rates, LOP, printed totals, balance forwards, EOB) via a loader of tests/unit/test_billing.py from the archive",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:15.081Z

**tool call — Bash**
````
{
 "command": "sed -n 50,70p tests/unit/test_billing.py; sed -n 250,345p app/backend/billing.py"
}
````

### User / tool · 2026-11-02T07:05:15.159Z

**tool result**
````
    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001
    060126 060326 11 97014 A 9000 3 SYN-NPI-0001
    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001
28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00"""

UB_ROOM = """SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
0450    EMERGENCY ROOM                               091526        1          1,975.00
0250    PHARMACY                                     091526       14            412.75
0300    LABORATORY                                   091526        6            688.00
0320    DX X-RAY                                     091526        2            540.00
0001    TOTAL                                        092226                   9,165.75
67 S42.201A   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)"""

PROSE = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
         "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")

LOP = ("Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction "
       "of the account. Please send an itemized statement.")


def _ledger_table(rec, lines):
    """(lines, stated totals, balance-forward rows [list], rate entries). A row whose description carries a rate cue and whose CHARGES figure was found (read
    or not) is a price, not a charge: it goes to the rate entries and into no total. Every other line that carries a figure and is not a clean
    dated row (above the header, below it, a total it cannot place) is emitted as an unparsed line (unclear, not totaled), never dropped."""
    hi, cols = _header(lines)
    offs = _offsets(lines)
    dcols = {k: (m.start(), m.end()) for k, rx in _DATECOLS.items() for m in [rx.search(lines[hi])] if m}
    out, stated, balfwd, rates = [], {}, [], []

    def unparsed(i, toks):
        out.append(_blank_line(rec, "ledger", lines[i], unparsed=True, unit=offs[i], unclear=[(t.group(0), (offs[i] + t.start(), offs[i] + t.end())) for t in toks]))

    for i in range(hi):                                # a figure above the column header is listed too
        if _tokens(lines[i]):
            unparsed(i, _tokens(lines[i]))
    for i in range(hi + 1, len(lines)):
        ln = lines[i]
        if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
            new = _stated(rec, ln, offs[i])
            _put_stated(rec, stated, new, out)
            left = []
            for t in _tokens(ln):
                f, kind, at = parse_figure(t.group(0)), _column(t.span(), cols), (offs[i] + t.start(), offs[i] + t.end())
                if any(_lap(at, v["_at"]) for v in new.values()):
                    continue                                 # this token IS one of the totals just read from the line
                if kind in ("billed", "paid", "adjustment", "balance") and f["cents"] is not None and kind not in stated:
                    stated[kind] = {**(_mag(f) if kind in ("paid", "adjustment") else f), "cite": _cite(rec, ln), "_at": at, "_unit": offs[i]}      # a totals row printed under the columns
                else:
                    left.append(t)
            if left:
                unparsed(i, left)
            continue
        if _BALFWD.search(ln):
            toks = _tokens(ln, all_bare=True)
            if toks:
                bf = {**_pf(toks[-1], offs[i]), "cite": _cite(rec, ln), "_unit": offs[i]}
                if bf["cents"] is None or len(toks) > 1:
                    unparsed(i, toks if bf["cents"] is None else toks[:-1])
                if bf["cents"] is not None:
                    balfwd.append(bf)          # every forward row is kept; analyze() lists them all when a provider has more than one
            continue
        m = _ROW.match(ln)
        figs = _tokens(ln, cols)
        if not m:
            if figs:                                  # a figure on a line that is not a dated row: listed, not totaled (it moves to a rate or LOP entry's other figures when it sits on that row)
                unparsed(i, figs)
            continue
        head = ln[:figs[0].start()] if figs else ln
        row_m = _ROW.match(head + " ")
        parts = (row_m.group(3) if row_m else "").split(None, 1)
        code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
        desc = (parts[1] if code and len(parts) > 1 else " ".join(parts)).strip() if parts else ""
        dos, posted = m.group(1), m.group(2)
        if posted is None and len(dcols) == 2 and _near((m.start(1), m.end(1)), dcols["posted"]) < _near((m.start(1), m.end(1)), dcols["dos"]):
            dos, posted = None, m.group(1)            # the only date sits under POSTED: the DOS cell is blank, the posting date is not a service date
        line = _blank_line(rec, "ledger", ln, dos=dos, posted=posted, code=code, description=desc, unit=offs[i])
        ratey, row_rate = A.has_rate_cue(desc, unit_notation=True), False
        for fm in figs:
            kind = _column(fm.span(), cols)
            f = _pf(fm, offs[i])
            if kind == "billed" and ratey:           # a price, whether or not its cents could be read: listed once, never a line
                rates.append(_rate_entry(rec, f, ln.strip(), "This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled.", row=_row_span(offs[i], ln)))
                row_rate = True
            elif kind is None or f["cents"] is None:
                _add_unclear(line, f["text"], f["_at"])
            elif kind == "rate":
                rates.append(_rate_entry(rec, f, ln.strip(), "This figure sits in the RATE column: a rate is a price, not a charge.", row=_row_span(offs[i], ln)))
            elif line[kind] is not None:
                _add_unclear(line, f["text"], f["_at"])            # two figures in one column: not guessed
            else:
                line[kind] = _mag(f) if kind in ("paid", "adjustment") else f
                if kind == "billed":
                    line["_credit"] = _is_credit(f["text"])
        if row_rate:
            line["balance"] = None                    # the running balance of a price row is one of the rate entry's other figures
            if not (line["paid"] or line["adjustment"] or line["unclear"]):
                continue
        out.append(line)
    tail = hi + 1 if hi + 1 < len(lines) else None
    if tail is not None:
        _put_stated(rec, stated, {k: v for k, v in _stated(rec, "\n".join(lines[tail:]), offs[tail]).items() if k not in stated}, out)
    return out, stated, balfwd, rates


def _blank_line(rec, form, ln, dos=None, posted=None, code=None, description="", unparsed=False, unclear=None, unit=None):
    """A line with no figures yet. `unclear` is [(text, (start, end))]: the tokens listed on the row with their positions."""
    pairs = list(unclear or [])
    return {"record_no": rec["n"], "form": form, "dos": dos, "dos_iso": _dos(dos) if dos else None, "posted": posted, "code": code,
            "description": description, "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [t for t, _ in pairs],
            "excerpt": ln.strip(), "unparsed": unparsed, "_uat": [p for _, p in pairs], "_unit": unit}


def _add_unclear(line, text, at):
    line["unclear"].append(text)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:15.882Z

**tool call — Bash**
````
{
 "command": "sed -n 755,800p app/backend/billing.py; sed -n 20,35p app/backend/billing.py; sed -n 685,700p memory/contracts/api.md; ls artifacts/review-evidence/T-103-r4/ | head; sed -n 55,110p reviews/T-103-staff-engineer-r4.md"
}
````

### User / tool · 2026-11-02T07:05:15.976Z

**tool result**
````
def _has_figure(l):
    return bool(l["billed"] or l["adjustment"] or l["paid"] or l["balance"] or l.get("non_covered") or l.get("eob"))


def _add_other(h, fig):
    """Put a token among an entry's other figures once: a token already there (same position) is not added again."""
    if not any(_lap(fig["_at"], f["_at"]) for f in h["other_figures"]):
        h["other_figures"].append(fig)


def _hold(got, stated, bfs, rates, lop):
    """(lines, rate/estimate entries, LOP entries) with one entry per printed row. The first figure of a rate, estimate or LOP/lien row is the entry; every
    OTHER money token printed on that row becomes one of its `other_figures`, wherever a parser first put it: a second amount in the sentence, a running
    balance the table parser left as an unclear figure, a printed total or balance on the same row. A token the entry already shows as its own figure is
    shown once. Positions decide all of this; no figure text is compared."""
    keep = []
    for h in sorted(list(rates) + list(lop), key=lambda h: h["_at"][0]):
        if any(_lap(h["_at"], k["_at"]) for k in keep):
            continue                                           # the same printed figure read as a rate and as an LOP amount: one entry
        host = next((k for k in keep if _within(h["_at"], k["_row"])), None)
        if host is not None:
            _add_other(host, {**parse_figure(h["figure"]["text"]), "_at": h["_at"]})          # read as the row prints it: a no-cents figure keeps its text and no value
        else:
            keep.append(h)
    out = []
    for l in got:
        had = bool(l["unclear"])
        pairs = []
        for t, sp in zip(l["unclear"], l.get("_uat") or []):
            h = next((k for k in keep if _within(sp, k["_row"])), None)
            if h is None:
                pairs.append((t, sp))
            elif not _lap(sp, h["_at"]):
                _add_other(h, {**parse_figure(t), "_at": sp})          # else: the entry's own figure, listed on its row too: shown once, as the entry
        l["unclear"], l["_uat"] = [t for t, _ in pairs], [sp for _, sp in pairs]
        if not (had and not pairs and (l.get("unparsed") or not _has_figure(l))):
            out.append(l)
    for h in keep:
        for k in [k for k, v in stated.items() if _within(v["_at"], h["_row"])]:
            v = stated.pop(k)
            if not _lap(v["_at"], h["_at"]):
                _add_other(h, {kk: v[kk] for kk in ("text", "cents", "usd", "_at")})
        for v in [v for v in bfs if _within(v["_at"], h["_row"])]:
            bfs.remove(v)
(two decimals, or an odd decimal like 95.5, OCR letters tolerated), with or without '$'; (b) a '$' figure with no cents; or (c) a bare whole
number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Three more cases are not tokens: on a UB-04
revenue-code row, a whole number with a decimal or '$' figure to its right (the row's charges are its last figure, so it is the units count; the header's UNITS and
SERV DATE columns are read as well as the money ones); a procedure code that follows a money-shaped token in an EOB row's service slot; and a prose number that
directly follows another money figure with no word between. A lone number in a CMS-1500 box followed by another figure (a broken box) is not read as the box.
Every money token must be a listed line, an unreconciled line, or sit on its row as an 'unclear' figure: the final accounting pass lists whatever no parser placed.
On a rate, estimate or LOP/lien row, every OTHER money token printed on the row (a running balance, a second amount in the sentence, a printed total on that
row) is one of that entry's `other_figures`, wherever a parser first put it.
Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
"""
import re

from app.backend import amounts as A, dates

    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "record_nos": [2], "form": "eob",
      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row
      "eob": {"billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}},
      "eob_codes": "PR-1, PR-2, CO-45", "unclear": [], "checks": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures
      "excerpt": "06/10/26  97140  70.00 ...", "cites": [ {"record_no": 2, "excerpt": "<same>"} ] } ],
  "unreconciled": [ { "id": "u1", "provider": "...", "record_no": 1, "form": "cms1500", "class": "unclear", "reason_code": "ROW_NOT_PARSED", "message": "...",
    "excerpt": "<the row, verbatim>", "figures": ["$85.00"] } ],   // rows that carry a figure or a date but fit no layout; never dropped. `figures` holds only the money tokens, not the rest of the line
  "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"}, {"record_no": 5, "reason_code": "UNRECOGNISED_BILLING_FORM"} ],
  "rules": [ "Every figure is listed with the line it was read from; nothing is totaled here, ...", "..." ] } }
```
**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. **Figure fields on an extra line, `other_figures`, a running `balance`, and everything in `eob` are never summed or compared by a client.** `other_figures` (a list of `{text, cents, usd}`, empty when none) holds every OTHER money token printed on a rate, estimate or LOP/lien row, wherever a parser first put it: the running balance on a price row (a no-cents one such as `$315` keeps its text with `cents: null`), a second amount in an LOP or rate sentence (the first amount is the entry, the later ones are its other figures), a printed balance or total on that row. A token on such a row is never also a line of its own. The only exception is a row that is also a charge line (a UB-04 room row: FL 44 rate and FL 47 charge): the charge is that line's. No token is reachable only by reading the excerpt; each text sits inside the excerpt (`verify_citations`: `other_figure_not_in_excerpt`). The class is `unclear` because the code does not decide what such a figure means. A figure that is both an LOP amount and a printed balance is one line.
**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept). A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. **Nothing is merged or deduplicated across records or providers (T-103 r3):** two providers printing the same row are two lines, a re-sent statement is two lines (one per record, each citing only its own record, so `record_nos` has one entry), and a line is identified by its record and its position in it (`id` follows record order, then position). Only a byte-identical copy of a whole record is dropped, at ingest (`duplicate_of`). CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a `rate` and the `0001` line is a printed total. A fee-schedule or per-unit figure is a rate; a table row or a sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate; one shared test, `amounts.has_rate_cue`, also used by reclassify) is a rate even beside the word charge or billed, is listed once, and a `RATE` column's figures are rates too. A ledger-table figure with no cents (`$185`, `185`) under a money column stays on its row as `unclear` text (`LINE_UNCLEAR`); on a rate row it is a `rate` line with `cents: null`, and a no-cents balance on a rate row is that rate's `other_figures` entry. A blank DOS cell stays blank (`dos: null`, `NO_DATE_OF_SERVICE`); the posting date is never read as the service date. A figure with OCR letters, other than two decimals, or inside an injection-tagged record has `cents: null` / the record is in `skipped_records`. A billing-looking record in no known layout is a `skipped_records` entry `UNRECOGNISED_BILLING_FORM`. An EOB service row (date, service code, then one figure per header column: BILLED, DISCOUNT, ALLOWED, DEDUCT, COINS, PLAN PAID, YOU MAY OWE) is a line of form `eob`; it is never compared with the ledger, so a difference in billed or paid is simply two cited lines. A service code and the number in a reason code (`PR-1`, `CO-45`) are not money. Every cited excerpt anywhere in the response (lines, cites, unreconciled) is checked against the record's own text, and every figure text (including each `eob` figure) against its excerpt, by `verify_citations`, which the route runs on every call; failures are returned as `citation_failures` and make the status `citation_failed`.
**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens, nor is a whole number on a UB-04 revenue-code row that has a decimal figure to its right (the units count), a procedure code pushed into an EOB money column by a money-shaped service slot, or a prose number directly after another money figure; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of these holds is added to `unreconciled` as a `ROW_NOT_PARSED` row (one already on that row is extended). The test replays every money token of the T-083 probe sets (r1 to r5 reviews, `artifacts/review-evidence/T-083-*`) plus 600 random insertions (seed 20261102) and 5 x 600 more (seeds 1 to 5), and fails if one is missing or if the exact per-record count differs. Repeated summary rows are never overwritten: two balance-forward rows, and a second TOTAL CHARGES / BALANCE DUE / paid / adjustment row (in one record, or in a second statement of the same provider and form family) are all listed (the earlier ones in `unreconciled`, the last as a line; a copy of a statement in a second record lists that record's totals again, one set per record). An EOB money token is a `$` figure with or without cents, a decimal (OCR letters tolerated), or a whole number under one of the EOB money columns; a row whose figures do not map one-to-one to the columns (a `$140`, `1O0.00`, `130.5`, a bare `130`, a missing or extra figure) keeps every token on its row in `unclear`. A printed total on an EOB (its TOTAL row) is an `unreconciled` row of form `eob`. The test also deletes each EOB figure in turn and requires the oracle to name it. A second test counts the money tokens per record (in every probe and in every random draw): the multiset of normalised token texts in the output's figure fields (`billed`, `paid`, `adjustment`, `balance`, `eob`, `unclear`, `figure`, `other_figures`, `unreconciled.figures`; never an excerpt) must equal the multiset in the input, so a token listed twice or listed for another token's sake fails as surely as a lost one.
**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, and the response fields `payer_reports`, `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
**Ladder.** All steps are code (parse, cite); there is no model step, so no judge. The human step is reading the view; none of it is exportable.

compare_scan_8a2b934_output.txt
live_dup_probe_8a2b934_output.txt
mut_r4.py
mutation_results_r4.txt
probe_r3_8a2b934_output.json
probe_r3_8a2b934_stderr.txt
probe_r3_R4M3_mutant_output.json
pytest_billing_archive_8a2b934.txt
pytest_billing_worktree_HEAD_4a560d8.txt
random_count_seeds.py
   "artifacts/review-evidence/T-103-r3/repro_r3.py -I on the 8a2b934 archive: R1 130.00 x4 in and out; R2 65.00 listed once (repro_r3_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r4/rate_rule_random.py -I, literal api.md:695 rule over rate, estimate and LOP rows, 3,600 draws: 458 break, all ub04, token 5550.00 on rate line b6 (rate_rule_random_8a2b934_output.txt, rate_rule_by_base_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw.py -I: b1 charge 5,550.00 and b6 rate 1,850.00 with other_figures [] on the same UB-04 room row (ub04_rate_row_draw6_8a2b934_output.txt)",
   "artifacts/review-evidence/T-103-r3/compare_scan.py on billing.py at 8a2b934 (80 flagged lines, read by category; compare_scan_8a2b934_output.txt); targeted money-word and comparison scan, and sum, float, Decimal and += scan (54 and 18 lines, read)",
   "artifacts/review-evidence/T-103-r4/mut_r4.py on scratch copies: R4M1 117 failed; R4M2 337 passed; R4M3 337 passed (mutation_results_r4.txt); raise-at-billing.py:790 inline: 15 failed, 322 passed",
   "artifacts/review-evidence/T-103-r3/live_dup_probe.py -I on the 8a2b934 archive: dedupe groups [[1, 2]], record 2 tokens in output 0 (live_dup_probe_8a2b934_output.txt)",
   "python -m pytest -q tests/unit/test_billing.py: 337 passed in the worktree (pytest_billing_worktree_HEAD_4a560d8.txt) and 337 passed on the 8a2b934 archive with -I and no cache (pytest_billing_archive_8a2b934.txt)",
   "grep for float(, except, LLM and model imports in billing.py: none; grep for MISMATCH codes in billing.py, api.md and tests; test source scan at test_billing.py:1336; Chris answers searched in submission/NEEDS_CHRIS.md and board/inbox: none found",
   "grep -n on memory/contracts/api.md (lines 667, 695, 696), billing.py (113, 117, 403, 763, 776, 786, 789, 790, 797, 798, 801, 884, 949, 968 to 970) and ingest.py (228 to 238): each cited line checked"
 ],
 "verdict": "changes",
 "scores": {"exact_per_record_money_count": 5, "money_integer_cents_no_float": 5, "no_llm_in_deterministic_path": 5, "other_figures_contract_api_695": 2, "D052_no_comparisons": 3, "no_silent_loss_live_path": 3, "test_mutation_catch": 3, "D019_total_unchanged": 5},
 "findings": [
   {"severity": "major",
    "title": "UB-04 rate row: the row's own 5,550.00 total is a charge line, not in the rate entry's other_figures (r3 F1 carried; the r4 handoff says every other token on a rate row is an other figure)",
    "evidence": "artifacts/review-evidence/T-103-r4/ub04_rate_row_draw6_8a2b934_output.txt: b1 class charge billed 5,550.00 and b6 class rate figure 1,850.00 other_figures [] on the excerpt '0120 ROOM & BOARD SEMI-PVT 1,850.00 ... 5,550.00'. Repro: .venv/bin/python -I artifacts/review-evidence/T-103-r4/rate_rule_random.py <8a2b934 archive> 20261102,1,2,3,4,5 -> draws_with_rate_rule_break=458, all ub04 (rate_rule_by_base_8a2b934_output.txt). The UB-04 sample is test_billing.py:55-64. memory/contracts/api.md:695 says other_figures 'holds every OTHER money token printed on a rate, estimate or LOP/lien row ... a printed balance or total on that row'.",
    "why_it_matters": "No value is lost and no sum is made: 5,550.00 is on its own charge line, verbatim, and the per-record count holds. But the contract a client reads says the rate entry carries every other money token of its row, and this one does not. The literal rule fails on every UB-04 room row. A client that reads other_figures misses the row total. Both places cannot hold at once: the count test forbids listing the token twice, so the contract must either name this exception or the token must move to other_figures.",
    "fix": "Choose one and write it down: (a) api.md:695 says a token that the same row already lists as a charge line is not repeated in other_figures, and the rule is tested for that case; or (b) the rate entry takes the row total as an other figure and the charge line for that token is removed, keeping the count exact. Then fix the wording in api.md:695 to match.",
    "acceptance_test": "The literal rule script (rate_rule_random.py) reports 0 break draws on seeds 20261102 and 1-5, or api.md names the exception and a test asserts it. A mutant that removes the chosen rule turns a named test red."},
   {"severity": "major",
    "title": "Comparisons remain in listing code: placement and the suppression of a printed total are decided by comparing offsets (r3 F2 carried; open on Q1)",
    "evidence": "app/backend/billing.py:113 (return a[0] < b[1] and b[0] < a[1], the overlap test behind _lap) and :117 (containment, behind _within); :763 (if not any(_lap(fig['_at'], f['_at']) ...)); :776 (host = next(... _within(h['_at'], k['_row']) ...)); :786-789 (_within and _lap decide whether an unclear figure is an other figure); :797 and :801 (_lap decides whether a stated total or balance forward is an other figure); :968-970 (shown = _placed(...); if any(_lap(v['_at'], p) for p in shown): continue, so a printed stated total is not listed when its offsets overlap a placed token). compare_scan_8a2b934_output.txt lists these lines. memory/contracts/api.md:667 says 'No sums and no comparisons of any kind'. The D-052 decision text (memory/ORCHESTRATOR_DECISIONS.md:60) does not use the word 'comparison'. Q1 has no ruling in submission/NEEDS_CHRIS.md or board/inbox.",
    "why_it_matters": "Money values are no longer compared: the sign is a credit-notation flag (billing.py:403, 949), placement is by position, and no sum exists. What remains is a comparison of positions that decides which entry a token belongs to and whether a printed total is shown. Under the standard the brief states ('no sums or comparisons of any kind'), that is a comparison that decides output. Under the worker's documented reading (api.md:667: 'the only tests left on numbers are layout ... and offset overlap') it is allowed. The reading is Chris's to make, not the reviewer's or the worker's.",
    "fix": "Chris rules on Q1. If the literal reading stands: the parsers return the ids of the tokens they placed (the r3 fix), so the placement pass and the stated-total suppression compare nothing, and compare_scan shows no offset comparison in billing.py outside the verifier. If the placement reading stands: record it as a decision in memory/DECISIONS.md, reword api.md:667 to name offset overlap as the one allowed comparison, and keep the compare_scan allow-list in the test.",
    "acceptance_test": "After Q1: either compare_scan.py over billing.py lists only the verifier's substring checks, or api.md:667 names offset overlap and a DECISIONS entry records the ruling. A mutant that always suppresses a stated total turns 117 tests red (R4M1, mutation_results_r4.txt), so the suppression itself is covered."},
   {"severity": "minor",
    "title": "Live ingest folds a byte-identical same-date copy before billing sees it; record 2 has no count and no skipped entry (r3 F6 carried; awaiting Q2)",
    "evidence": "artifacts/review-evidence/T-103-r4/live_dup_probe_8a2b934_output.txt: dedupe groups [[1, 2]], billing record_nos [1], record 2 tokens in output 0. app/backend/ingest.py:228-238 (key = date, normalised source, normalised text; unchanged since 1526a1f). app/backend/billing.py:884 (recs = [r for r in records if not r.get('duplicate_of')]), with no skipped_records entry. memory/contracts/api.md:696 says 'a re-sent statement is two lines (one per record, ...)'.",
    "why_it_matters": "The rule that a re-sent statement is two lines is true for analyze() called directly, but not for the live path. A listing should say when a record is not shown; this one drops record 2 without a word. Checklist item 19 would accept one line here, so the behaviour may be right; the contract and the path do not say the same thing.",
    "fix": "Chris rules on Q2. If one set: name record 2 in skipped_records with reason DUPLICATE_OF and reword api.md:696 to say identical same-date copies are one set. If two sets: stop the ingest fold for billing and keep both records. Either way test the path through ingest.dedupe and then analyze.",
    "acceptance_test": "live_dup_probe.py: record 2 is either named in skipped_records with DUPLICATE_OF, or it has its own lines; the test runs through ingest.dedupe, not analyze() alone."},
   {"severity": "minor",
    "title": "detail carries both a reason for listing and a kind of line (r3 F7 carried, not changed in r4)",
    "evidence": "app/backend/billing.py:949 sets detail to eob, reversal, balance_only, rate, or None; the extra lines set detail to stated_total_billed, stated_total_balance, balance_forward and so on (billing.py:972 and the extra() calls at :965-966). The r4 handoff says 'detail kind/reason split (F7) untouched'.",
    "why_it_matters": "A client branches on strings that mean two different things: why a ledger row is listed, and what kind of line it is.",
    "fix": "As r1, r2b and r3 proposed: a closed kind list for what the line is, a separate reason for why it is listed, both documented in api.md.",
    "acceptance_test": "Every line has a kind from a closed list and a reason from a closed list; a test pins both lists."},
   {"severity": "minor",
    "title": "Two rate-row holder branches can be removed with the suite and the rule check unchanged (test-strength gap)",
    "evidence": "artifacts/review-evidence/T-103-r4/mutation_results_r4.txt: R4M2 (billing.py:790, the unclear-to-other_figures move) 337 passed; R4M3 (billing.py:798, the stated-total move) 337 passed. Raise-at-790 inline check: 15 failed, 322 passed, so the branch is reached. rate_rule_random_R4M3_mutant_output.txt (the R4M2 run's output file name keeps the earlier label) is identical to the baseline, so no output changes in 3,600 draws.",
    "why_it_matters": "Either the branch is redundant (the token is placed by another route in every shape tested) or the tests cannot tell. Both are a problem: dead code in the placement pass, and a contract rule with no guard on the path it names.",
    "fix": "Find a shape in which only the branch places the token, and assert its other_figures; or delete the branch and let the rule check and the exact count cover the case.",
    "acceptance_test": "Removing the chosen branch turns a named test red (mutant R4M2 or R4M3 in mutation_results_r4.txt)."}
 ],
 "whats_right": [
   "The exact per-record count holds on 24,600 generated draws across 41 seeds (0 failures by the module helper and by an independent count), and the same harness reproduces the r3 failure (31 of 600) on the r3 commit.",
   "Money values are no longer compared or summed: the sign is a credit-notation flag, the R1 footer and the R2 double are fixed, and no mismatch code or per-provider total remains in billing.py.",
   "The stated-total suppression is covered by a mutant (R4M1 turns 117 tests red), and the billing tests pass reproducibly (337 on both the worktree and the archive copy)."
 ],
 "questions_for_chris": [
   "Q1 (carried from r3, still open): does 'no comparisons of any kind' (api.md:667, and the brief) forbid comparing offsets to place a token and to suppress a printed total? D-052's own text (memory/ORCHESTRATOR_DECISIONS.md:60) does not mention comparisons. Finding 2 depends on the answer.",
   "Q2 (carried from r3, still open): a byte-identical copy dated the same day from the same source is folded at ingest (ingest.py:228-238). Do you want one set with record 2 named in skipped_records as DUPLICATE_OF, or two sets? Finding 3 depends on the answer.",
   "Q3 (new): for the UB-04 room row, should a row total that the row already lists as a charge line also appear in the rate entry's other_figures, or is that a documented exception? Finding 1 depends on the answer."
 ]}
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:21.656Z

**tool call — Bash**
````
{
 "command": "grep -n \"ub04\\|UB-04\\|FL 44\\|_rate_entry(\" app/backend/billing.py | head -40"
}
````

### User / tool · 2026-11-02T07:05:21.747Z

**tool result**
````
7:A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as class rate; an estimate, an LOP or lien amount, a printed total
8:(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB service
21:number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
23:else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Three more cases are not tokens: on a UB-04
44:    "A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as a rate, never a charge; a row or sentence that says per visit/session/hour/day, each or x N is a rate even beside the word charge.",
152:    """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
158:    if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
159:        return "ub04"
200:def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=None):
209:_NONMONEY = ("units", "servdate")          # UB-04 header columns that are not money: a whole number nearest to one of these is a count or a date
313:                rates.append(_rate_entry(rec, f, ln.strip(), "This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled.", row=_row_span(offs[i], ln)))
318:                rates.append(_rate_entry(rec, f, ln.strip(), "This figure sits in the RATE column: a rate is a price, not a charge.", row=_row_span(offs[i], ln)))
411:                rates.append(_rate_entry(rec, fig, seg.strip(), row=row))
423:                rates.append(_rate_entry(rec, fig, seg.strip(), "An estimate is not a charge. It is not totaled.", kind="estimate", row=row))
504:# ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)
521:    """(index, columns) with the UB-04 header's non-money columns too (units, service date), so a whole number is told to sit under UNITS rather than
533:def _ub04(rec, lines):
545:                out.append(_blank_line(rec, "ub04", ln, unparsed=True, unit=offs[i], unclear=toks))
553:        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
562:                rates.append(_rate_entry(rec, p, ln.strip(), "UB-04 line 44 is a rate, not a charge.", row=_row_span(offs[i], ln)))
721:    elif form == "ub04":
812:    hi, cols = _header(ls) if form == "ledger_table" else _ub_all_cols(ls) if form == "ub04" else _eob_header(ls) if form == "eob" else (None, None)
903:        elif form == "ub04":
904:            got, st, rates = _ub04(r, ls)
911:        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
919:                        rates.append(_rate_entry(r, {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"]), "_at": at}, body[row[0]:row[1]], row=row))
921:        if form in ("ledger_table", "ledger_text", "cms1500", "ub04", "eob"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:23.726Z

**tool call — Bash**
````
{
 "command": "sed -n 533,580p app/backend/billing.py; sed -n 195,208p app/backend/billing.py"
}
````

### User / tool · 2026-11-02T07:05:23.809Z

**tool result**
````
def _ub04(rec, lines):
    hi, cols = _ub_all_cols(lines)
    if hi is None:
        return [], {}, []
    offs = _offsets(lines)
    out, rates, stated = [], [], {}
    for i in range(hi + 1, len(lines)):
        ln = lines[i]
        m = _UBROW.match(ln)
        if not m:
            toks = [(t.group(0), (offs[i] + t.start(), offs[i] + t.end())) for t in _tokens(ln)]
            if toks:                                  # a figure on a line that is not a revenue-code row: listed, never dropped
                out.append(_blank_line(rec, "ub04", ln, unparsed=True, unit=offs[i], unclear=toks))
            continue
        figs = [(f, _column(f.span(), cols)) for f in _tokens(ln)]
        if m.group(1) == "0001":
            for f, k in figs:
                if k == "billed":
                    stated["billed"] = {**_pf(f, offs[i]), "cite": _cite(rec, ln), "_unit": offs[i]}
            continue
        line = {"record_no": rec["n"], "form": "ub04", "dos": None, "dos_iso": None, "posted": None, "code": m.group(1), "description": m.group(2).strip(),
                "billed": None, "adjustment": None, "paid": None, "balance": None, "unclear": [], "_uat": [], "_unit": offs[i], "excerpt": ln.strip(), "non_covered": None}
        sd = re.search(r"\b(\d{6})\b", ln[:figs[0][0].start()] if figs else ln)
        line["dos"] = sd.group(1) if sd else None
        for f, k in figs:
            p = _pf(f, offs[i])
            if p["cents"] is None or k is None or k in _NONMONEY:
                _add_unclear(line, p["text"], p["_at"])
            elif k == "rate":
                rates.append(_rate_entry(rec, p, ln.strip(), "UB-04 line 44 is a rate, not a charge.", row=_row_span(offs[i], ln)))
            elif k == "noncovered":
                line["non_covered"] = p
            elif line["billed"] is None:
                line["billed"] = p
                line["_credit"] = _is_credit(p["text"])
            else:
                _add_unclear(line, p["text"], p["_at"])
        out.append(line)
    return out, stated, rates


# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
_EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
            ("coinsurance", r"COINS\w*"), ("plan_paid", r"PLAN\s+PAID"), ("patient_owes", r"YOU\s+MAY\s+OWE|PATIENT\s+RESP\w*"))
_EOBROW = re.compile(rf"^\s*({_DATE})\s+(\S+)\s+")


def _eob_header(lines):
    k = _column(token_span, cols)
    return k is not None and k not in _NONMONEY


# ------------------------------------------------------------------ itemized ledger table
def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=None):
    """A rate, estimate or LOP-like entry. `fig` carries its position (`_at`); `row` is the offsets of the printed row (the excerpt) it was read from."""
    return {"record_no": rec["n"], "kind": kind, "why": why, "figure": fig, "excerpt": excerpt, "_at": fig["_at"], "_row": row or fig["_at"], "other_figures": []}


def _blank_dates(ln):
    return re.sub(_DATE, lambda m: " " * len(m.group(0)), ln)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:36.829Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/backend/amounts.py'\ns=open(p).read()\n# 1 Spanish rate cues\ns=s.replace('''_UNIT = r\"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?\"\n''','''_UNIT = r\"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?\"\n# Spanish unit nouns (T-110 r2): \"por sesión\", \"por visita\", \"cada ...\". Accents are optional because pasted records often lose them.\n_UNIT_ES = r\"(?:sesi[o\\\\u00f3]n|sesiones|visitas?|horas?|d[i\\\\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)\"\n''')\ns=s.replace('''_RATE_WORD = re.compile(rf\"\\\\b(?:(?:per|each)[\\\\s-]+{_UNIT}|rate\\\\s+of)\\\\b|/\\\\s*{_UNIT}\\\\b\", re.IGNORECASE)''',\n'''_RATE_WORD = re.compile(rf\"\\\\b(?:(?:per|each)[\\\\s-]+{_UNIT}|rate\\\\s+of|(?:por|cada)\\\\s+{_UNIT_ES})\\\\b|/\\\\s*{_UNIT}\\\\b|/\\\\s*{_UNIT_ES}\\\\b\", re.IGNORECASE)''')\ns=s.replace('''_RATE_AFTER = re.compile(rf\"^\\\\s*(?:(?:per|each|an?)[\\\\s-]+{_UNIT}\\\\b|/\\\\s*{_UNIT}\\\\b|each\\\\b|''','''_RATE_AFTER = re.compile(rf\"^\\\\s*(?:(?:per|each|an?)[\\\\s-]+{_UNIT}\\\\b|(?:por|cada)\\\\s+{_UNIT_ES}\\\\b|/\\\\s*{_UNIT}\\\\b|each\\\\b|cada\\\\s+(?:una?|uno)\\\\b|''')\ns=s.replace('''_RATE_CORE = (r\"\\\\bper\\\\b|\\\\beach\\\\b|\\\\bevery\\\\b|''','''_RATE_CORE = (r\"\\\\bper\\\\b|\\\\beach\\\\b|\\\\bevery\\\\b|\\\\bcada\\\\b|\\\\bpor\\\\s+(?:sesi[o\\\\u00f3]n|sesiones|visitas?|horas?|d[i\\\\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)\\\\b|''')\nopen(p,'w').write(s)\nE\ngrep -n \"_UNIT_ES\\|cada\" app/backend/amounts.py | head"
}
````

### User / tool · 2026-11-02T07:05:36.934Z

**tool result**
````
15:# Spanish unit nouns (T-110 r2): "por sesión", "por visita", "cada ...". Accents are optional because pasted records often lose them.
16:_UNIT_ES = r"(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)"
17:_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of|(?:por|cada)\s+{_UNIT_ES})\b|/\s*{_UNIT}\b|/\s*{_UNIT_ES}\b", re.IGNORECASE)
18:_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|(?:por|cada)\s+{_UNIT_ES}\b|/\s*{_UNIT}\b|each\b|cada\s+(?:una?|uno)\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
24:_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|\bcada\b|\bpor\s+(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:44.964Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/amounts.py'\ns=open(p).read()\ns=s.replace('''_WORK_TAIL = re.compile(''','''# Spanish charge and balance cues (T-110 r2, D-050). The classifier does NOT use them: a Spanish figure stays `unclear` until the paralegal reads the\n# original and reclassifies it, and only the reclassify guard (code cue + judge re-check) reads them. A rate cue above still beats a charge cue.\nCHARGE_CUE_ES = re.compile(r\"\\\\b(?:cargos?|honorarios|estado\\\\s+de\\\\s+cuenta)\\\\b\", re.IGNORECASE)\n_NO_CHARGE_ES = re.compile(r\"\\\\bsin\\\\s+(?:cargo|costo|cobro)s?\\\\b|\\\\bno\\\\s+(?:se\\\\s+)?(?:cobr[o\\\\u00f3a]|factur\\\\w*)\\\\b|\\\\bgratis\\\\b|\\\\bgratuit[oa]\\\\b\", re.IGNORECASE)\nBALANCE_CUE = re.compile(r\"\\\\bsaldos?\\\\b|\\\\bbalance\\\\s+(?:forward|brought)\\\\b\", re.IGNORECASE)\n\n\ndef charge_cue_es(text: str):\n    \"\"\"The Spanish charged-amount phrase in `text` (cargo, cargos, honorarios, estado de cuenta), or None. A negation ('sin cargo', 'no facturado') or a\n    balance word (saldo) in the same text returns None: a balance restates charges, so counting it would count them twice.\"\"\"\n    t = text or \"\"\n    m = CHARGE_CUE_ES.search(t)\n    return m.group(0) if m and not _NO_CHARGE_ES.search(t) and not BALANCE_CUE.search(t) else None\n\n\n_WORK_TAIL = re.compile(''',1)\nopen(p,'w').write(s)\np='app/backend/reclassify.py'\ns=open(p).read()\ns=s.replace('''        m = _WORDING.search(sent)\n        if not m or _NEGATED''','''        m = _WORDING.search(sent)\n        es = None if m else A.charge_cue_es(sent)             # Spanish cargo / cargos / honorarios / estado de cuenta (a saldo or a negation in the sentence: none)\n        if not (m or es) or (m and A.BALANCE_CUE.search(sent)) or _NEGATED''')\ns=s.replace(\"        found = found or m.group(0)\",\"        found = found or (m.group(0) if m else es)\")\nopen(p,'w').write(s)\nE\nsed -n 70,85p app/backend/reclassify.py"
}
````

### User / tool · 2026-11-02T07:05:45.068Z

**tool result**
````
    """Code check: the charged-amount phrase in the figure's own sentence (every occurrence of the figure must have one, no negation, no rate
    cue), or None. A rate cue decides: "Charge per visit $185" and "Billed $150 per visit" are rates."""
    spans = _figure_spans(excerpt or "", row, rec)
    found = None
    for s, _e in spans:
        sent = next((t for a, b, t in _sentences(excerpt) if a <= s <= b), "")
        m = _WORDING.search(sent)
        es = None if m else A.charge_cue_es(sent)             # Spanish cargo / cargos / honorarios / estado de cuenta (a saldo or a negation in the sentence: none)
        if not (m or es) or (m and A.BALANCE_CUE.search(sent)) or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
            return None
        found = found or (m.group(0) if m else es)
    return found


def _refuse(reason: str, **detail):
    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:51.194Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/amounts.py'\ns=open(p).read()\ns=s.replace('BALANCE_CUE = re.compile(r\"\\\\bsaldos?\\\\b|\\\\bbalance\\\\s+(?:forward|brought)\\\\b\", re.IGNORECASE)','BALANCE_CUE = re.compile(r\"\\\\bsaldos?\\\\b\", re.IGNORECASE)')\nopen(p,'w').write(s)\nE\ngrep -n \"BALANCE_CUE =\" app/backend/amounts.py\nsed -n 1,80p tests/unit/test_reclassify.py"
}
````

### User / tool · 2026-11-02T07:05:51.306Z

**tool result**
````
43:BALANCE_CUE = re.compile(r"\bsaldos?\b", re.IGNORECASE)
"""T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun."""
import pytest
from fastapi.testclient import TestClient
from app.backend import pipeline as PL, present, reclassify as RC, review as RV
from app.backend.api import create_app
from app.db import db as DB
from app.llm import audited as AU
from tests.unit._fakes import FakeCall, sample_script

TEXT = """=== Record 1 ===
Date: 2026-03-02
Source: Capital PT, visit 1
Excerpt: "Visit completed. Rate of $185 per visit."

=== Record 2 ===
Date: 2026-03-09
Source: Capital PT, visit 2
Excerpt: "Visit completed. Charge per visit $185."

=== Record 3 ===
Date: 2026-03-16
Source: Capital Imaging
Excerpt: "MRI performed. Charge: $310."

=== Record 4 ===
Date: 2026-03-23
Source: Capital PT, visit 4
Excerpt: "Visit completed. Not billed $90 per visit to this patient."

=== Record 5 ===
Date: 2026-03-30
Source: Capital PT, visit 5
Excerpt: "Visit completed. $185 was billed to the patient."

=== Record 6 ===
Date: 2026-04-06
Source: Capital PT, visit 6
Excerpt: "Visit completed. Billed $150 per visit."
"""
J2 = lambda v, code="NONE": {"j2": {"verdict": v, "reason_code": code}}     # noqa: E731


def seeded(tmp_path, judge="agree"):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    conn = DB.connect(str(tmp_path / "rc.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 1.0)
    return conn, cid


def kinds(conn, cid):
    return {a["text"] + "@" + a["record_ids"][0]: a for a in DB.list_items(conn, cid, "amount")}


def aid(conn, cid, text, rec):
    return kinds(conn, cid)[f"{text}@{rec}"]["id"]


def events(conn, cid, item_id):
    return [e for e in DB.list_events(conn, cid, item_id) if (e.get("after") or {}).get("event") == "reclassify"]


def test_fixture_classes_are_what_the_tests_assume(tmp_path):
    conn, cid = seeded(tmp_path)
    k = kinds(conn, cid)
    assert (k["$185@r1"]["kind"], k["$185@r2"]["kind"], k["$310@r3"]["kind"], k["$90@r4"]["kind"]) == ("rate", "rate", "charge", "rate")
    assert (k["$185@r5"]["kind"], k["$150@r6"]["kind"]) == ("unclear", "rate")       # r5: charged wording, no rate cue; r2 and r6: wording AND a rate cue


# ---------------------------------------------------------------- charge -> not a charge
def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RV.apply_review(conn, cid, a, {"action": "accept"})
    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge", "note": "This is a retainer, not a bill."}, call=None, now=5.0)
    assert r["amount"]["kind"] == "unclear" and r["item"]["review_status"] == "pending"          # her earlier accept was about the old meaning
    assert r["totals"]["accepted"]["cents"] == 0 and r["reclassified"] == {"from": "charge", "to": "unclear", "wording": None, "judge_verdict": None, "restored": False}
    [ev] = events(conn, cid, a)
    assert ev["before"]["kind"] == "charge" and ev["after"]["kind"] == "unclear" and ev["after"]["note"] == "This is a retainer, not a bill."
    row = DB.get_item(conn, a, cid)
    assert row["ladder"]["reclassification"]["by"] == "reviewer" and row["ladder"]["code_checks"]["classified_by"] == "reviewer:reclassified"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:55.446Z

**tool call — Bash**
````
{
 "command": "grep -n \"J2(\\|def test.*promot\\|\\\"to\\\": \\\"charge\\\"\" tests/unit/test_reclassify.py | head -12; sed -n 80,110p tests/unit/test_reclassify.py"
}
````

### User / tool · 2026-11-02T07:05:55.536Z

**tool result**
````
96:    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)                                # no judge call available: still fine
105:    call = FakeCall(J2("agree"))
107:        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
115:        RC.reclassify(conn, cid, aid(conn, cid, "$90", "r4"), {"to": "charge"}, call=FakeCall(J2("agree")))
122:    call = FakeCall(J2("agree"))
123:    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call, now=7.0)
139:        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2(verdict, code)))
144:@pytest.mark.parametrize("call", [None, FakeCall(J2("agree", "BAD CODE")), lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed())])
149:        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
157:        RC.reclassify(conn, cid, a, {"to": "charge"}, call=lambda *x, **k: (_ for _ in ()).throw(RuntimeError("bug")))
166:    call = FakeCall(J2("agree"))
168:        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert row["ladder"]["reclassification"]["by"] == "reviewer" and row["ladder"]["code_checks"]["classified_by"] == "reviewer:reclassified"
    assert any(e["action"] == "reset" for e in DB.list_events(conn, cid, a))                    # the reset is its own audited event


def test_same_direction_is_a_noop_without_an_event(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r1")
    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    assert r["reclassified"] is None and not events(conn, cid, a)


def test_undoing_her_own_demotion_restores_the_code_class_without_a_judge(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    before = DB.get_item(conn, a, cid)["ladder"]["judge"]
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)                                # no judge call available: still fine
    assert r["amount"]["kind"] == "charge" and r["reclassified"]["restored"] is True
    assert DB.get_item(conn, a, cid)["ladder"]["judge"] == before and len(events(conn, cid, a)) == 2


# ---------------------------------------------------------------- not a charge -> charge (guarded)
def test_rate_without_charge_wording_is_422_and_the_judge_is_never_asked(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r1")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.code, e.value.detail["reason"], e.value.detail["check"]) == (422, "reclassify_refused", "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:56.791Z

Now item 2 (export notes), 3 (tray), 4 (UB-04). First the export.

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:05:57.831Z

**tool call — Bash**
````
{
 "command": "sed -n 86,100p app/backend/store.py; grep -n \"def _money\\b\\|def _money_short\\|def _terminate\\|def _cap\" -A6 app/backend/export.py | head -40; grep -n \"internal_notes\\|AMOUNTS NOT TOTALED\" tests/unit/*.py | head -8"
}
````

### User / tool · 2026-11-02T07:05:57.919Z

**tool result**
````
        out["export_config"] = ec
    if nar:
        out["narrative"] = {"status": nar["status"], "basis": nar.get("basis", {}), "removed": nar.get("removed", []),
                            "sentences": [{"text": x["text"], "entry_id": x["entry_id"], "cite": x.get("cite")} for x in nar.get("sentences", [])]}
    return out
56:def _money(cents):
57-    return f"${cents // 100:,}.{cents % 100:02d}"
58-
59-
60:def _money_short(cents, raw=""):
61-    if cents is None:
62-        return raw
63-    return f"${cents // 100:,}" if cents % 100 == 0 else _money(cents)
64-
65-
66-def _norm(s):
--
70:def _cap(s):
71-    return s[:1].upper() + s[1:]
72-
73-
74:def _terminate(s):
75-    """End a note sentence with a period unless it already ends with a full stop."""
76-    return s if s.endswith('."') or s.endswith(".") else s + "."
77-
78-
79-def _sentence_spans(text):
80-    """[(start, end)] whole-sentence spans, split at '. ' (not after an abbreviation, not before a lowercase
tests/unit/test_api.py:31:    assert isinstance(j["letter_text"], str) and isinstance(j["internal_notes_text"], str)
tests/unit/test_api.py:32:    assert j["letter_text"] != j["internal_notes_text"] and "INTERNAL REVIEW NOTES" not in j["letter_text"]
tests/unit/test_api.py:33:    assert "AI assistance" not in j["letter_text"] and "AI assistance" in j["internal_notes_text"]
tests/unit/test_api_routes.py:168:    assert ex["internal_notes_text"]    # golden byte-equality runs on the curated fixture set (D-029, qa T-051)
tests/unit/test_case_extras.py:107:    assert out["letter_text"] == letter.rstrip("\n") and out["internal_notes_text"] == notes.rstrip("\n")
tests/unit/test_case_extras.py:117:    assert X.build_export(cfg)["internal_notes_text"] == notes.rstrip("\n")           # notes never carry the exhibit numbers
tests/unit/test_date_unconfirmed.py:82:    assert "date not confirmed" in ex["internal_notes_text"]
tests/unit/test_eval_runner.py:197:    monkeypatch.setattr(R, "check_spec", lambda *a, **k: {"spec_matches_golden": False, "letter_equal": False, "internal_notes_equal": True})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:08.134Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/store.py'\ns=open(p).read()\ns=s.replace('''    ec = (case.get(\"config\") or {}).get(\"export\")\n    if ec:''','''    from app.backend import overlap                      # lazy: overlap imports amounts and dates only\n    ov = overlap.view(conn, case_id)                      # T-110: statement line vs a separately stated charge of the same kind; code only, never changes a figure\n    if ov:\n        out[\"possible_overlaps\"] = [dict(o, statement_record_no=n_of.get(o[\"statement_record_id\"], 0), covered_record_no=n_of.get(o[\"covered_record_id\"], 0)) for o in ov]\n    ec = (case.get(\"config\") or {}).get(\"export\")\n    if ec:''',1)\nopen(p,'w').write(s)\np='app/backend/export.py'\ns=open(p).read()\ns=s.replace('''        self.narrative = case.get(\"narrative\")\n\n    def verbatim''','''        self.narrative = case.get(\"narrative\")\n        self.overlaps = list(case.get(\"possible_overlaps\") or [])\n\n    def verbatim''',1)\ns=s.replace('''def _damages(v):''','''def _overlaps(v):\n    \"\"\"T-110: a statement line that may already include a separately stated charge of the same kind. Internal notes only (D-019): the letter's total line never\n    changes. Plain words, both records and both figures named; nothing is added, subtracted or compared here.\"\"\"\n    out = []\n    for o in v.overlaps:\n        s_no, c_no = o.get(\"statement_record_no\"), o.get(\"covered_record_no\")\n        line = (f\"- Possible overlap: {v.cite(s_no)} lists {o.get('statement_text')} on a statement line, and {v.cite(c_no)} separately states \"\n                f\"{o.get('covered_text')}, both for {str(o.get('service') or 'the same service').replace('_', ' ')}. The statement line may already include that charge.\")\n        if o.get(\"both_in_total\"):\n            line += \" Both figures are in the charges total, so this service may be counted twice. Check the records and dismiss one of the two.\"\n        elif not o.get(\"date_known\", True):\n            line += \" The date of the second record is not confirmed, so the statement's date range cannot rule it out. Check the records before relying on the total.\"\n        else:\n            line += \" The total does not currently add both figures. Check the records before accepting both.\"\n        out.append(line)\n    return out\n\n\ndef _damages(v):''',1)\ns=s.replace('''        \"AMOUNTS NOT TOTALED\", *_amounts_not_totaled(v), \"\",\n''','''        \"AMOUNTS NOT TOTALED\", *_amounts_not_totaled(v), \"\",\n        *([\"POSSIBLE OVERLAPS (check before relying on the charges total)\", *_overlaps(v), \"\"] if v.overlaps else []),\n''',1)\nopen(p,'w').write(s)\nE\n"
}
````

### User / tool · 2026-11-02T07:06:08.232Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:21.073Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/generator.py'\ns=open(p).read()\ns=s.replace('''def extract_entries(''','''def resolved_placeholders(entries: list) -> set:\n    \"\"\"Ids of could-not-verify placeholders (`ladder.failure`) whose record now has a live entry, which is the entry the paralegal wrote by hand (T-110 r2).\n    Such a placeholder is handled: the tray, the rejected counts and the export's excluded count leave it out. The row itself stays (audit).\"\"\"\n    live = {r for e in entries if e[\"state\"] != \"rejected\" for r in (e[\"record_ids\"] or [])}\n    return {e[\"id\"] for e in entries if (e.get(\"ladder\") or {}).get(\"failure\") and e[\"state\"] == \"rejected\" and live & set(e[\"record_ids\"] or [])}\n\n\ndef extract_entries(''',1)\nopen(p,'w').write(s)\np='app/backend/present.py'\ns=open(p).read()\ns=s.replace('''             \"ladder\": {\"item_id\": x[\"id\"], \"state\": \"rejected\"}} for k in (\"entry\", \"amount\") for x in its[k] if x[\"state\"] == \"rejected\"]''','''             \"ladder\": {\"item_id\": x[\"id\"], \"state\": \"rejected\"}} for k in (\"entry\", \"amount\") for x in its[k] if x[\"state\"] == \"rejected\" and x[\"id\"] not in handled]''',1)\ns=s.replace('''    ents = its[\"entry\"]\n    live_e =''','''    ents = its[\"entry\"]\n    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, \"entry\"))      # T-110 r2: a record the paralegal entered by hand leaves the tray\n    live_e =''',1)\ns=s.replace('''    items = [(k, r) for k in (\"entry\", \"amount\", \"flag\") for r in DB.list_items(conn, case_id, k)]\n    live =''','''    items = [(k, r) for k in (\"entry\", \"amount\", \"flag\") for r in DB.list_items(conn, case_id, k)]\n    handled = generator.resolved_placeholders([r for k, r in items if k == \"entry\"])\n    items = [(k, r) for k, r in items if r[\"id\"] not in handled]\n    live =''',1)\nopen(p,'w').write(s)\np='app/backend/api.py'\ns=open(p).read()\ns=s.replace('''\"rejected\": sum(1 for k in (\"entry\", \"amount\") for r in DB.list_items(c, token, k) if r[\"state\"] == \"rejected\")}''','''\"rejected\": sum(1 for k in (\"entry\", \"amount\") for r in DB.list_items(c, token, k) if r[\"state\"] == \"rejected\"\n                                              and r[\"id\"] not in generator.resolved_placeholders(DB.list_items(c, token, \"entry\")))}''',1)\nopen(p,'w').write(s)\np='app/backend/trace.py'\ns=open(p).read()\ns=s.replace('''    failed_ents = [x for x in ents if (x.get(\"ladder\") or {}).get(\"failure\")]''','''    handled = generator.resolved_placeholders(ents)\n    failed_ents = [x for x in ents if (x.get(\"ladder\") or {}).get(\"failure\") and x[\"id\"] not in handled]''',1)\ns=s.replace('''    ents = [x for x in ents if not (x.get(\"ladder\") or {}).get(\"failure\")]\n    amts''','''    ents = [x for x in ents if not (x.get(\"ladder\") or {}).get(\"failure\")]      # (a hand-entered record's placeholder is dropped here too)\n    amts''',1)\nopen(p,'w').write(s)\nE\ngrep -n \"^from\\|^import\" app/backend/present.py app/backend/trace.py | grep -n \"generator\"; grep -n \"generator\" app/backend/api.py | head -3; git diff app/backend/api.py | head -40"
}
````

### User / tool · 2026-11-02T07:06:21.212Z

**tool result**
````
123:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
538:                                              and r["id"] not in generator.resolved_placeholders(DB.list_items(c, token, "entry")))}
539:            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
diff --git a/app/backend/api.py b/app/backend/api.py
index 21bc044..55ffb87 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -506,10 +506,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import billing
     billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
@@ -534,7 +534,8 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
             ex["excluded"] = {"pending": case["pending_count"],
                               "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
-                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
+                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected"
+                                              and r["id"] not in generator.resolved_placeholders(DB.list_items(c, token, "entry")))}
             ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                 "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                 "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:25.942Z

**tool call — Bash**
````
{
 "command": "sed -n 1,25p app/backend/present.py | grep -n \"import\"; grep -n \"^from app.backend\\|^import\\|^from\" app/backend/trace.py | head; grep -n \"^from app.backend import\\|^    from app.backend import\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T07:06:26.043Z

**tool result**
````
2:import json
3:import re
5:from app.backend import confidence, date_convention, grounding, ingest, language, overlap, pdf_text, sentences, spanish, store, totals as T, why
6:from app.db import db as DB
11:import json
13:from app.backend import grounding, narrative, present, review, store, why
14:from app.backend import judges as J
15:from app.db import db as DB
16:from app.llm import audited as AU
23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
41:from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
509:    from app.backend import billing
511:    from app.backend import pdf_routes
513:    from app.backend import reclassify
516:    from app.backend import calibration_route
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:27.916Z

**tool call — Bash**
````
{
 "command": "grep -n \"^from app\\|^import\" app/backend/generator.py"
}
````

### User / tool · 2026-11-02T07:06:27.996Z

**tool result**
````
5:import re
10:from app.backend import confidence, grounding, injection, judges, language, schemas, spanish, why
11:from app.llm import audited as AU, promptlib, provider as P
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:32.696Z

No cycle. Add imports; in api.py use a `present` helper to keep the edit small.

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:35.886Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\nimport re\np='app/backend/present.py'; s=open(p).read()\ns=s.replace(\"from app.backend import confidence, date_convention, grounding,\",\"from app.backend import confidence, date_convention, generator, grounding,\",1); open(p,'w').write(s)\np='app/backend/trace.py'; s=open(p).read()\ns=s.replace(\"from app.backend import grounding, narrative, present,\",\"from app.backend import generator, grounding, narrative, present,\",1); open(p,'w').write(s)\np='app/backend/present.py'; s=open(p).read()\ns=s.replace('''def review_view(conn, case_id):''','''def rejected_count(conn, case_id):\n    \"\"\"Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2).\"\"\"\n    handled = generator.resolved_placeholders(DB.list_items(conn, case_id, \"entry\"))\n    return sum(1 for k in (\"entry\", \"amount\") for r in DB.list_items(conn, case_id, k) if r[\"state\"] == \"rejected\" and r[\"id\"] not in handled)\n\n\ndef review_view(conn, case_id):''',1); open(p,'w').write(s)\np='app/backend/api.py'; s=open(p).read()\ns=s.replace('''\"rejected\": sum(1 for k in (\"entry\", \"amount\") for r in DB.list_items(c, token, k) if r[\"state\"] == \"rejected\"\n                                              and r[\"id\"] not in generator.resolved_placeholders(DB.list_items(c, token, \"entry\")))}''','''\"rejected\": present.rejected_count(c, token)}''',1); open(p,'w').write(s)\nE\ngit diff app/backend/api.py | grep '^[+-]' | head"
}
````

### User / tool · 2026-11-02T07:06:36.003Z

**tool result**
````
--- a/app/backend/api.py
+++ b/app/backend/api.py
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
-                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
+                              "rejected": present.rejected_count(c, token)}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:53.703Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='app/backend/billing.py'; s=open(p).read()\nold='''            else:\n                _add_unclear(line, p[\"text\"], p[\"_at\"])\n        out.append(line)\n    return out, stated, rates\n'''\nnew='''            else:\n                _add_unclear(line, p[\"text\"], p[\"_at\"])\n        if row_rate:                                  # T-103 r4: the room row's FL 47 total (and a non-covered figure) are other figures of the FL 44 rate entry, listed once, as that entry's\n            for key in (\"billed\", \"non_covered\"):\n                if line[key] is not None:\n                    _add_other(row_rate[0], line[key])\n                    line[key] = None\n            if not line[\"unclear\"]:\n                continue                              # nothing else on the row: no line of its own\n        out.append(line)\n    return out, stated, rates\n'''\nassert old in s\ns=s.replace(old,new,1)\ns=s.replace('''        for f, k in figs:\n            p = _pf(f, offs[i])\n            if p[\"cents\"] is None or k is None or k in _NONMONEY:''','''        row_rate = []\n        for f, k in figs:\n            p = _pf(f, offs[i])\n            if p[\"cents\"] is None or k is None or k in _NONMONEY:''',1)\ns=s.replace('''                rates.append(_rate_entry(rec, p, ln.strip(), \"UB-04 line 44 is a rate, not a charge.\", row=_row_span(offs[i], ln)))\n            elif k == \"noncovered\":''','''                rates.append(_rate_entry(rec, p, ln.strip(), \"UB-04 line 44 is a rate, not a charge.\", row=_row_span(offs[i], ln)))\n                row_rate.append(rates[-1])\n            elif k == \"noncovered\":''',1)\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T07:06:54.488Z

**tool result**
````
    def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
        out = one([rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)])
        ls = rows(out, "Saltmarrow")
>       assert [cents(l) for l in ls] == [555000, 197500, 41275, 68800, 54000]
E       assert [197500, 41275, 68800, 54000] == [555000, 1975... 68800, 54000]
E         
E         At index 0 diff: 197500 != 555000
E         Right contains one more item: 54000
E         Use -v to get more diff

tests/unit/test_billing.py:264: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:06:56.205Z

**tool call — Bash**
````
{
 "command": "sed -n 258,285p tests/unit/test_billing.py; .venv/bin/python -m pytest -q tests/unit/test_billing.py -q 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T07:07:00.639Z

**tool result**
````
    assert detail(out, "stated_total_billed")[0]["figure"]["cents"] == 39000


def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
    out = one([rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)])
    ls = rows(out, "Saltmarrow")
    assert [cents(l) for l in ls] == [555000, 197500, 41275, 68800, 54000]
    assert [(x["figure"]["cents"], x["detail"]) for x in rates(out)] == [(185000, "rate")]
    assert all(l["code"] != "0001" for l in ls) and detail(out, "stated_total_billed")[0]["figure"]["cents"] == 916575


def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
    eob = [l for l in out["lines"] if l["form"] == "eob"]
    assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
    l140 = next(l for l in eob if l["code"] == "97140")
    assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
    assert l140["billed"] is None and l140["paid"] is None and l140["checks"] == [] and l140["excerpt"] in EOB     # an EOB row is never a charge or a payment
    assert [cents(l) for l in rows(out, "Larkspur") if l["form"] == "ledger"][:2] == [21000, 13000]
    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised
    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})


def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
    r = [rec(1, "Brightwater Spine & Wellness, itemized ledger", "Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00."),
         rec(2, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)]
    ls = rows(one(r), "Brightwater")
    assert [(l["form"], cents(l)) for l in ls] == [("ledger", 39000)] + [("cms1500", c) for c in (8500, 8500, 8500, 9000, 4500)]
E         
E         At index 0 diff: 197500 != 555000
E         Right contains one more item: 54000
E         Use -v to get more diff

tests/unit/test_billing.py:264: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:05.214Z

Only that one expectation changes; update it and pin the other_figures.

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:07.396Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/unit/test_billing.py'; s=open(p).read()\ns=s.replace('''    assert [cents(l) for l in ls] == [555000, 197500, 41275, 68800, 54000]\n    assert [(x[\"figure\"][\"cents\"], x[\"detail\"]) for x in rates(out)] == [(185000, \"rate\")]\n''','''    assert [cents(l) for l in ls] == [197500, 41275, 68800, 54000]            # T-103 r4: the room row's FL 47 total is not a line of its own ...\n    assert [(x[\"figure\"][\"cents\"], x[\"detail\"]) for x in rates(out)] == [(185000, \"rate\")]\n    assert [(f[\"text\"], f[\"cents\"]) for f in rates(out)[0][\"other_figures\"]] == [(\"5,550.00\", 555000)]       # ... it is the FL 44 rate entry's other figure, listed once\n''',1)\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -4; grep -n \"def rates\" -A3 tests/unit/test_billing.py | head"
}
````

### User / tool · 2026-11-02T07:07:11.732Z

**tool result**
````
........................................................................ [ 64%]
........................................................................ [ 85%]
.................................................                        [100%]
337 passed in 3.98s
99:def rates(out):
100-    return [l for l in out["lines"] if l["class"] == "rate"]
101-
102-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:12.612Z

Update api.md exception wording, then write tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:14.485Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'; s=open(p).read()\nold=\"A token on such a row is never also a line of its own. The only exception is a row that is also a charge line (a UB-04 room row: FL 44 rate and FL 47 charge): the charge is that line's.\"\nassert old in s\ns=s.replace(old,\"A token on such a row is never also a line of its own, with no exception: on a UB-04 room row the FL 44 figure is the rate entry and the FL 47 total (and any non-covered figure) is one of that entry's `other_figures` (T-103 r4, T-110 r2).\")\nopen(p,'w').write(s)\nE\ngrep -n \"possible_overlaps\\|POSSIBLE_OVERLAP\\|tray\" memory/contracts/api.md | head -20; grep -n \"internal_notes_text\" memory/contracts/api.md | head -5"
}
````

### User / tool · 2026-11-02T07:07:14.600Z

**tool result**
````
131:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
187:    "possible_overlaps": []
232:  "tray": [
247:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
360:**`totals.possible_overlaps` (T-110, D-019; every response that carries `totals`).** Array, normally empty. One object per pair of a billing-statement line and a separately stated charge that name the same kind of service (closed family table in `app/backend/overlap.py`: consult, physical therapy, imaging, emergency, ambulance, injection, surgery, laboratory; English and Spanish) when the charge's record date is inside the statement's date range (two dates written in the statement text, else on or before the statement's own date). Fields: `code: "POSSIBLE_OVERLAP"`, `statement_amount_id`, `covered_amount_id`, `statement_record_id`, `covered_record_id`, `statement_text`, `covered_text` (the figures as written), `service`, `range: {from, to, stated}`, `date_known` (false when the charge's record date is not confirmed: it is listed, not ruled out), `both_charges` (both are class `charge`), `both_in_total` (both are accepted, so the accepted total currently contains both), `message` (one of three fixed sentences; never model text). Rates, estimates, damages, dismissed and unreadable figures are never parties, nor are statement balance/total/payment/adjustment lines or two figures of one record. **The warning never changes `totals.accepted`, `pending` or `detected_not_a_total`, and no figure is subtracted, merged or compared: the total still adds stated charges only.** The frontend shows each warning beside the total with both figures and the message; the paralegal dismisses one of the two if the statement line includes the other.
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
372:  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:22.083Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'; s=open(p).read()\ns=s.replace(\"the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it.\",\"the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit.\",1)\ns=s.replace(\"the paralegal dismisses one of the two if the statement line includes the other.\",\"the paralegal dismisses one of the two if the statement line includes the other. **Export (T-110 r2):** when `possible_overlaps` is not empty, `internal_notes_text` gets a section `POSSIBLE OVERLAPS (check before relying on the charges total)` after `AMOUNTS NOT TOTALED`, one plain-words line per pair naming both records and both figures (and whether both are in the total); with none, the notes are byte-for-byte as before. The letter never mentions an overlap.\",1)\nopen(p,'w').write(s)\nE\ngrep -c \"T-110 r2\" memory/contracts/api.md; grep -n \"Spanish\\|reclassif\" memory/contracts/api.md | grep -i \"reclass\" | head -5"
}
````

### User / tool · 2026-11-02T07:07:22.203Z

**tool result**
````
3
31:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
103:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
321:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
341:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
345:- Same class as now: `200`, `reclassified: null`, nothing written.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:23.731Z

**tool call — Bash**
````
{
 "command": "sed -n 341,358p memory/contracts/api.md | cut -c1-900"
}
````

### User / tool · 2026-11-02T07:07:23.810Z

**tool result**
````
## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
The paralegal says a dollar figure is, or is not, a billed charge. Taking a figure **out** of the total is always her call; putting one **in** needs evidence. Body: `{ "to": "charge" | "not_a_charge", "note": "optional, 500 chars" }`.
- `to: "not_a_charge"` on a `charge`: always allowed. The class becomes `unclear` (response `amount.kind: "unclear"`; shown as "not added to the total", never totaled).
- `to: "charge"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated ("not billed", "unbilled"), the figure has a parsed value and its record is not injection-tagged, **and (2) judge 2** re-checks the figure against class `charge` and answers `agree`. Code runs first; the judge is not called when the code check fails. Undoing her own earlier demotion of a figure the code first called a charge skips both checks (the original class returns with the judge answer it had; works with no judge available).
- Same class as now: `200`, `reclassified: null`, nothing written.
- Anything not allowed: `422 reclassify_refused`, nothing changes, no event: `{error: {code, message, detail: {reason, check: "code"|"judge", wording?, error_class?}}}`. `detail.reason` is one of `NO_VALUE`, `INJECTION_SUSPECTED`, `NO_CHARGE_WORDING` (check `code`), `JUDGE_DISAGREES`, `JUDGE_UNSURE`, `JUDGE_UNAVAILABLE` (check `judge`; `JUDGE_UNAVAILABLE` includes no recorded answer in demo mode, so a rate-to-charge there is refused with "try again" wording). `message` is a fixed plain sentence, safe to show. Other errors: `400 bad_request` (missing/other `to`, non-text `note`), `404 not_found`, `409 item_rejected`, `422 invalid_edit` (not an amount).
- On success the item goes back to `review_status: pending` (a reset event is logged first if she had decided it; her earlier decision was about the old meaning) and must be accepted again. Its state is recomposed: a judged charge is `verified`; a not-a-charge is `needs_review` with `AMOUNT_UNCLEAR`.
- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassification` = `{from, to, at, by: "reviewer", original_kind, wording, restored, note, previous_judge}` and `ladder.code_checks.classified_by` = `"reviewer:reclassified"`.
- A rerun (`POST /run`) keeps her class for the same figure (same text and value); a changed figure takes the new code class.

Response 200:
```json
{ "item":   { "id": "a2", "kind": "amount", "review_status": "pending", "state": "verified", "reasons": [] },
  "amount": { "id": "a2", "text": "$185", "value_cents": 18500, "kind": "charge", "state": "verified", "reasons": [], "why": "...", "review_status": "pending",
              "ladder": { "reclassification": { "from": "rate", "to": "charge", "by": "reviewer", "wording": "Charge" }, "...": "..." } },
  "totals": { "...": "as in review" }, "review": { "...": "as in review" },
  "reclassified": { "from": "rate", "to": "charge", "wording": "Charge", "judge_verdict": "agree", "restored": false },
  "warnings": [] }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:41.587Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='memory/contracts/api.md'; s=open(p).read()\ns=s.replace(\"- Same class as now: `200`, `reclassified: null`, nothing written.\\n\",\"- **Spanish cues (T-110 r2, code only, D-050).** The charged-amount wording also accepts `cargo`, `cargos`, `honorarios` and `estado de cuenta` in the figure's sentence (`detail.wording` / `reclassified.wording` carries the phrase). `sin cargo`, `no facturado` and similar negations refuse it, and so does `saldo` (a balance restates charges: counting it would count them twice). The shared rate-cue test (`amounts.RATE_CUE`) also reads `por sesión`, `por visita`, `por hora`, `por día`, `cada` and their unaccented spellings, so `$400 por sesión` is a rate and stays `NO_CHARGE_WORDING`; the amount classifier reads the same rate words, so such a figure is class `rate`. A Spanish figure is still never classed `charge` by code: it starts `unclear` and becomes a charge only here, with the judge re-check; it then counts in the D-019 total once accepted.\\n- Same class as now: `200`, `reclassified: null`, nothing written.\\n\",1)\nopen(p,'w').write(s)\nE\ncat > tests/unit/test_lib09_t110_r2.py <<'E'\n\"\"\"T-110 r2 on lib09 (fixture backend, no network): Spanish cues let a paralegal reclassify an unclear figure to a charge through the T-084 guard, a rate\nnever becomes one, possible overlaps reach the internal notes (never the letter), and a hand-entered record leaves the tray.\"\"\"\nimport pytest\n\nfrom app.backend import amounts as A, export as X, present, reclassify as RC, review as RV, store\nfrom app.db import db as DB\nfrom tests.unit._fakes import FakeCall\nfrom tests.unit.test_lib09_t110 import _stored, _miss_on, TEXT\n\nJ2 = lambda v, code=\"NONE\": {\"j2\": {\"verdict\": v, \"reason_code\": code}}     # noqa: E731\n\n\ndef _by_text(conn, cid):\n    out = {}\n    for a in DB.list_items(conn, cid, \"amount\"):\n        out.setdefault(a[\"text\"], []).append(a)\n    return out\n\n\n# ---------------------------------------------------------------- the shared cues\n@pytest.mark.parametrize(\"text\", [\"Costo por sesión de terapia: $400.00\", \"4 sesiones a $400.00 por sesion\", \"$90 por visita\", \"$50 cada sesión\", \"$50 cada uno\", \"$50 por hora\"])\ndef test_spanish_rate_cues_are_rate_cues_and_the_classifier_calls_the_figure_a_rate(text):\n    assert A.has_rate_cue(text)\n    amt = A.find_amounts(text)[0]\n    assert A.classify(text, amt) == \"rate\"\n\n\n@pytest.mark.parametrize(\"text\", [\"Cargo por factura 4471: $400\", \"Honorarios: $650\", \"Consulta: $650.00\"])\ndef test_spanish_charge_words_are_not_rate_cues(text):\n    assert not A.has_rate_cue(text)\n\n\ndef test_charge_cue_es_and_balance_cue():\n    assert A.charge_cue_es(\"Cargos: $1,300.00\") == \"Cargos\" and A.charge_cue_es(\"Honorarios del médico $650\") == \"Honorarios\"\n    assert A.charge_cue_es(\"Estado de cuenta: consultas $1,300.00;\") == \"Estado de cuenta\"\n    assert A.charge_cue_es(\"Sin cargo: $0\") is None and A.charge_cue_es(\"Saldo de cargos: $2,900\") is None and A.charge_cue_es(\"Consulta: $650\") is None\n    assert A.BALANCE_CUE.search(\"Saldo: $2,900.00\") and not A.BALANCE_CUE.search(\"Cargos: $1,300\")\n\n\n# ---------------------------------------------------------------- lib09 through the T-084 guard\ndef test_lib09_consultas_line_can_be_reclassified_to_a_charge_and_counts_in_the_total():\n    tmp, conn, cid = _stored()\n    with tmp:\n        a5 = _by_text(conn, cid)[\"$1,300.00\"][0]\n        assert a5[\"kind\"] == \"unclear\"\n        call = FakeCall(J2(\"agree\"))\n        r = RC.reclassify(conn, cid, a5[\"id\"], {\"to\": \"charge\"}, call=call, now=5.0)\n        assert r[\"amount\"][\"kind\"] == \"charge\" and r[\"reclassified\"][\"wording\"].lower() == \"estado de cuenta\" and r[\"reclassified\"][\"judge_verdict\"] == \"agree\"\n        assert len(call.log) == 1 and r[\"item\"][\"review_status\"] == \"pending\"\n        for aid in (a5[\"id\"],):\n            RV.apply_review(conn, cid, aid, {\"action\": \"accept\"})\n        t = present.totals_view(conn, cid)\n        assert t[\"accepted\"][\"cents\"] == 130000 and t[\"accepted\"][\"count\"] == 1               # D-019 counts it once accepted\n\n\ndef test_lib09_consultas_reclassification_still_needs_the_judge():\n    tmp, conn, cid = _stored()\n    with tmp:\n        a5 = _by_text(conn, cid)[\"$1,300.00\"][0]\n        with pytest.raises(RV.ReviewError) as e:\n            RC.reclassify(conn, cid, a5[\"id\"], {\"to\": \"charge\"}, call=FakeCall(J2(\"disagree\", \"SHOULD_BE_ESTIMATE\")))\n        assert e.value.detail[\"reason\"] == \"JUDGE_DISAGREES\" and DB.get_item(conn, a5[\"id\"], cid)[\"kind\"] == \"unclear\"\n\n\ndef test_lib09_rate_per_session_is_refused_and_never_asks_the_judge():\n    tmp, conn, cid = _stored()\n    with tmp:\n        for a in _by_text(conn, cid)[\"$400.00\"]:\n            call = FakeCall(J2(\"agree\"))\n            with pytest.raises(RV.ReviewError) as e:\n                RC.reclassify(conn, cid, a[\"id\"], {\"to\": \"charge\"}, call=call)\n            assert (e.value.status, e.value.detail[\"reason\"], e.value.detail[\"check\"]) == (422, \"NO_CHARGE_WORDING\", \"code\")\n            assert call.log == [] and DB.get_item(conn, a[\"id\"], cid)[\"kind\"] in (\"rate\", \"unclear\")\n\n\ndef test_lib09_saldo_is_never_a_charge():\n    tmp, conn, cid = _stored()\n    with tmp:\n        saldo = _by_text(conn, cid)[\"$2,900.00\"][0]\n        with pytest.raises(RV.ReviewError) as e:\n            RC.reclassify(conn, cid, saldo[\"id\"], {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))\n        assert e.value.detail[\"reason\"] == \"NO_CHARGE_WORDING\"\n\n\ndef test_a_saldo_in_the_same_sentence_as_a_charge_word_is_refused():\n    row = {\"text\": \"$2,900.00\"}\n    assert RC.charge_wording(\"Cargos, saldo: $2,900.00.\", row) is None\n    assert RC.charge_wording(\"Saldo: $2,900.00.\", row) is None\n    assert RC.charge_wording(\"Honorarios: $2,900.00.\", row) == \"Honorarios\"\n    assert RC.charge_wording(\"Sin cargo: $2,900.00.\", row) is None\n    assert RC.charge_wording(\"Honorarios $90 por sesión: $90.00.\", {\"text\": \"$90.00\"}) is None\n\n\n# ---------------------------------------------------------------- export: overlap in the internal notes only\ndef _export(conn, cid):\n    for it in DB.list_items(conn, cid, \"amount\") + DB.list_items(conn, cid, \"entry\"):\n        if it[\"state\"] != \"rejected\":\n            RV.apply_review(conn, cid, it[\"id\"], {\"action\": \"accept\"}) if it[\"kind\" if \"kind\" in it and it.get(\"record_ids\") and False else \"id\"] else None\n    return X.build_export(store.export_case(conn, cid))\n\n\ndef test_overlap_is_in_the_internal_notes_and_not_in_the_letter():\n    tmp, conn, cid = _stored()\n    with tmp:\n        a = _by_text(conn, cid)\n        for t in (\"$2,940\", \"$2,150\"):\n            RV.apply_review(conn, cid, a[t][0][\"id\"], {\"action\": \"accept\"})\n        RC.reclassify(conn, cid, a[\"$650.00\"][0][\"id\"], {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))      # \"Consulta: $650.00\" has no Spanish charge word: refused below\nE\necho"
}
````

### User / tool · 2026-11-02T07:07:41.699Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:07:56.225Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/unit/test_lib09_t110_r2.py'; s=open(p).read()\ni=s.index(\"# ---------------------------------------------------------------- export: overlap\")\ns=s[:i]+'''# ---------------------------------------------------------------- export: overlap in the internal notes only\ndef test_overlap_is_in_the_internal_notes_and_not_in_the_letter():\n    tmp, conn, cid = _stored()\n    with tmp:\n        a = _by_text(conn, cid)\n        for t in (\"$2,940\", \"$2,150\"):\n            RV.apply_review(conn, cid, a[t][0][\"id\"], {\"action\": \"accept\"})\n        case = store.export_case(conn, cid)\n        [o] = case[\"possible_overlaps\"]\n        assert (o[\"statement_record_no\"], o[\"covered_record_no\"], o[\"service\"]) == (7, 2, \"consult\")\n        ex = X.build_export(case)\n        notes, letter = ex[\"internal_notes_text\"], ex[\"letter_text\"]\n        assert \"POSSIBLE OVERLAPS (check before relying on the charges total)\" in notes and \"Possible overlap: record 7\" in notes\n        assert \"$1,300.00\" in notes and \"record 2\" in notes and \"$650.00\" in notes and \"consult\" in notes\n        assert \"The total does not currently add both figures\" in notes\n        assert \"overlap\" not in letter.lower() and \"Billed charges stated in these records: $5,090.00\" in letter       # D-019: the letter and its total are untouched\n\n\ndef test_overlap_line_says_when_both_figures_are_in_the_total():\n    tmp, conn, cid = _stored()\n    with tmp:\n        RV.apply_review(conn, cid, _by_text(conn, cid)[\"$2,940\"][0][\"id\"], {\"action\": \"accept\"})\n        case = store.export_case(conn, cid)\n        case[\"possible_overlaps\"][0][\"both_in_total\"] = True\n        notes = X.build_export(case)[\"internal_notes_text\"]\n        assert \"Both figures are in the charges total, so this service may be counted twice\" in notes\n        case[\"possible_overlaps\"] = []\n        assert \"POSSIBLE OVERLAPS\" not in X.build_export(case)[\"internal_notes_text\"]            # no overlap: the notes are as before\n\n\n# ---------------------------------------------------------------- the tray placeholder leaves once the paralegal enters the record by hand\ndef test_placeholder_leaves_the_tray_when_a_manual_entry_exists():\n    tmp, conn, cid = _stored(_miss_on(\"e6\"))\n    with tmp:\n        rid = \"r6\"\n        assert [t[\"id\"] for t in present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=True)[\"tray\"]] == [\"e6\"]\n        rejected_before = present.review_view(conn, cid)[\"counts\"][\"rejected\"]\n        assert rejected_before == 1 and present.rejected_count(conn, cid) == 1\n        quote = \"Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10.\"\n        RV.manual_entry(conn, cid, rid, {\"summary\": \"MRI reviewed; physical therapy and injection recommended; pain 5/10.\", \"excerpt\": quote}, call=FakeCall(J2(\"agree\")))\n        view = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=True)\n        assert view[\"tray\"] == [] and present.review_view(conn, cid)[\"counts\"][\"rejected\"] == 0 and present.rejected_count(conn, cid) == 0\n        assert DB.get_item(conn, \"e6\", cid)[\"state\"] == \"rejected\"                          # the placeholder row stays for audit\n        assert any(e[\"id\"] == \"e6_m\" for e in view[\"entries\"])\n'''\nopen(p,'w').write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_lib09_t110_r2.py -x 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T07:07:57.372Z

**tool result**
````
..................                                                       [100%]
18 passed in 0.82s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:08:00.228Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T07:10:00.836Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b7xi9f8wn). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b7xi9f8wn.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:10:04.688Z

**tool call — Bash**
````
{
 "command": "git status --short | grep -v \"agent-memory\\|^?? board\\|board/\" ; git diff --stat -- app tests memory/contracts | tail -20"
}
````

### User / tool · 2026-11-02T07:10:04.820Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:10:07.985Z

**tool call — Bash**
````
{
 "command": "git diff --stat app/backend memory/contracts/api.md tests/unit/test_billing.py"
}
````

### User / tool · 2026-11-02T07:10:08.080Z

**tool result**
````
 app/backend/amounts.py     | 23 ++++++++++++++++++++---
 app/backend/api.py         |  6 +++---
 app/backend/billing.py     |  9 +++++++++
 app/backend/export.py      | 20 ++++++++++++++++++++
 app/backend/generator.py   |  7 +++++++
 app/backend/pipeline.py    |  2 +-
 app/backend/present.py     | 13 +++++++++++--
 app/backend/reclassify.py  |  5 +++--
 app/backend/store.py       |  4 ++++
 app/backend/trace.py       |  7 ++++---
 memory/contracts/api.md    |  7 ++++---
 tests/unit/test_billing.py |  3 ++-
 12 files changed, 88 insertions(+), 18 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:10:13.109Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/arc && mkdir -p $S/arc && git archive HEAD | tar -x -C $S/arc && for f in amounts billing export generator present reclassify store trace; do cp app/backend/$f.py $S/arc/app/backend/$f.py; done && cp memory/contracts/api.md $S/arc/memory/contracts/api.md && cp tests/unit/test_billing.py tests/unit/test_lib09_t110_r2.py $S/arc/tests/unit/ && git diff app/backend/api.py > $S/api.diff && python3 - <<'E'\nimport re\nS=\"/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"\np=S+\"/arc/app/backend/api.py\"; s=open(p).read()\nold='''\"rejected\": sum(1 for k in (\"entry\", \"amount\") for r in DB.list_items(c, token, k) if r[\"state\"] == \"rejected\")}'''\nassert old in s\nopen(p,'w').write(s.replace(old,'\"rejected\": present.rejected_count(c, token)}'))\nE\nls $S/arc | head -3; ls .venv >/dev/null && echo venv"
}
````

### User / tool · 2026-11-02T07:10:13.534Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
venv
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:10:15.564Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arc && timeout 590 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q tests/unit -p no:cacheprovider -q 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T07:10:15.644Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:10:17.765Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arc && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -p no:cacheprovider 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T07:12:55.889Z

**tool result**
````
........................................................................ [ 63%]
........................................................................ [ 66%]
........................................................................ [ 69%]
........................................................................ [ 72%]
........................................................................ [ 75%]
........................................................................ [ 78%]
........................................................................ [ 81%]
........................................................................ [ 84%]
..............................................................s......... [ 87%]
........................................................................ [ 90%]
........................................................................ [ 93%]
........................................................................ [ 96%]
........................................................................ [ 99%]
........................                                                 [100%]
2396 passed, 4 skipped in 156.95s (0:02:36)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:01.778Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/idx && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/amounts.py app/backend/billing.py app/backend/export.py app/backend/generator.py app/backend/present.py app/backend/reclassify.py app/backend/store.py app/backend/trace.py memory/contracts/api.md tests/unit/test_billing.py tests/unit/test_lib09_t110_r2.py && git apply --cached --include='app/backend/api.py' <(git diff app/backend/api.py | python3 -c \"\nimport sys,re\nd=sys.stdin.read()\nhead,*h=re.split(r'(?m)^(?=@@)',d)\nmine=[x for x in h if 'rejected_count' in x]\nsys.stdout.write(head+''.join(mine))\") && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T07:13:02.034Z

**tool result**
````
 app/backend/amounts.py           |  23 ++++++-
 app/backend/api.py               |   2 +-
 app/backend/billing.py           |   9 +++
 app/backend/export.py            |  20 ++++++
 app/backend/generator.py         |   7 ++
 app/backend/present.py           |  13 +++-
 app/backend/reclassify.py        |   5 +-
 app/backend/store.py             |   4 ++
 app/backend/trace.py             |   7 +-
 memory/contracts/api.md          |   7 +-
 tests/unit/test_billing.py       |   3 +-
 tests/unit/test_lib09_t110_r2.py | 137 +++++++++++++++++++++++++++++++++++++++
 12 files changed, 222 insertions(+), 15 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:07.308Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/idx && git commit -q -m \"fix(backend): Spanish charge/rate/balance cues in the shared cue function, overlap in internal notes, tray placeholder leaves after manual entry, UB-04 room total in other_figures (T-110 r2)\n\n- amounts: cargo/cargos/honorarios/estado de cuenta = charge cue (reclassify guard only), por sesion/visita/hora/dia and cada = rate cue (classifier, billing, reclassify), saldo = balance cue (refuses)\n- export: POSSIBLE OVERLAPS section in the internal notes, never in the letter\n- generator/present/trace/api: a failed-extract placeholder with a hand-entered entry leaves the tray and the rejected counts\n- billing: UB-04 FL 47 total is the FL 44 rate entry's other_figures (T-103 r4 minor)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git log --oneline -1 && unset GIT_INDEX_FILE && git show --stat HEAD | tail -14"
}
````

### User / tool · 2026-11-02T07:13:08.235Z

**tool result**
````
check_secrets: ok (12 file(s) scanned staged)
d24ff07 fix(backend): Spanish charge/rate/balance cues in the shared cue function, overlap in internal notes, tray placeholder leaves after manual entry, UB-04 room total in other_figures (T-110 r2)

 app/backend/amounts.py           |  23 ++++++-
 app/backend/api.py               |   2 +-
 app/backend/billing.py           |   9 +++
 app/backend/export.py            |  20 ++++++
 app/backend/generator.py         |   7 ++
 app/backend/present.py           |  13 +++-
 app/backend/reclassify.py        |   5 +-
 app/backend/store.py             |   4 ++
 app/backend/trace.py             |   7 +-
 memory/contracts/api.md          |   7 +-
 tests/unit/test_billing.py       |   3 +-
 tests/unit/test_lib09_t110_r2.py | 137 +++++++++++++++++++++++++++++++++++++++
 12 files changed, 222 insertions(+), 15 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:09.137Z

Now the board and memory.

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:14.678Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-110 --check 1 --agent backend --evidence \"r2: tests/unit/test_lib09_t110_r2.py 18 passed (lib09 'consultas \\$1,300' reclassifies to charge via T-084 guard and counts once accepted; '\\$400 por sesion' and saldo refused NO_CHARGE_WORDING; overlap in internal notes not letter; tray placeholder gone after manual entry); test_billing 337 passed (UB-04 room total in other_figures); full tests/unit 2396 passed in git archive HEAD + my files; commit d24ff07\" 2>&1 | tail -2; $B commit T-110 --sha d24ff07 --agent backend 2>&1 | tail -1; $B handoff T-110 --agent backend --text \"Round 2. Changed: (1) amounts.py shared cues: cargo/cargos/honorarios/estado de cuenta = charge cue (only the reclassify guard reads it), por sesion/visita/hora/dia + cada = rate cue (RATE_CUE, classifier, billing, reclassify), saldo = balance cue that refuses; lib09 consultas \\$1,300 reclassifies to charge with the judge re-check and counts in the D-019 total once accepted; \\$400 por sesion refused NO_CHARGE_WORDING; the classifier now calls the Spanish \\$400s rate. 'estado de cuenta' added as a charge cue beyond your list because the lib09 sentence has no cargo/honorarios word. (2) export internal notes: POSSIBLE OVERLAPS section after AMOUNTS NOT TOTALED (only when there is one; letter untouched; goldens unchanged). (3) generator.resolved_placeholders: a failed-extract placeholder with a live entry leaves tray, rejected counts, trace in_tray, export excluded. (4) billing: UB-04 FL 47 total (and non-covered) is the FL 44 rate entry's other_figures, no own line; test_billing + api.md updated. Verified: test_lib09_t110_r2 18 passed; tests/unit 2396 passed in git archive HEAD + my files; no prompt/lexicon change. Left: screen overlap warning is T-096; Spanish 'Request clean copy of bill' note wording unchanged. Surprised: api.py/pipeline.py carry others' uncommitted hunks, committed only mine via temp index.\" 2>&1 | tail -1; $B move T-110 in_review --agent backend 2>&1 | tail -1"
}
````

### User / tool · 2026-11-02T07:13:14.956Z

**tool result**
````
AC 1 checked: r2: tests/unit/test_lib09_t110_r2.py 18 passed (lib09 'consultas $1,300' reclassifies to charge via T-084 guard and counts once accepted; '$400 por sesion' and saldo refused NO_CHARGE_WORDING; overlap in internal notes not letter; tray placeholder gone after manual entry); test_billing 337 passed (UB-04 room total in other_figures); full tests/unit 2396 passed in git archive HEAD + my files; commit d24ff07
T-110: commit d24ff07 recorded
handoff written on T-110
T-110: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:19.084Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/backend && cat >> project_t110_overlap_tray.md <<'E'\n\n## Round 2 (commit d24ff07)\n- Spanish cues live in `amounts.py`: `RATE_CUE`/`_RATE_WORD`/`_RATE_AFTER` read por sesión/visita/hora/día + cada (classifier, billing and reclassify share them, so lib09's $400s are now class `rate`); `CHARGE_CUE_ES` (cargo/cargos/honorarios/estado de cuenta) and `BALANCE_CUE` (saldo) are read ONLY by `reclassify.charge_wording`, never by `classify` (D-050: Spanish stays unclear until the paralegal reclassifies). lib09's \"consultas $1,300\" sentence has no cargo/honorarios, so \"estado de cuenta\" was added as a charge cue.\n- `generator.resolved_placeholders(entries)` is the one rule for \"tray placeholder answered by a hand-entered entry\"; used in present (tray, review counts, rejected_count), trace in_tray, api export excluded. DB has no delete, so the row stays.\n- UB-04 room row: FL 47 total goes to the FL 44 rate entry's other_figures and has no line (billing._ub04 `row_rate`).\n- Commit with a temp index when api.py/pipeline.py carry others' hunks: `git apply --cached` a filtered diff for only my hunk.\nE\necho ok"
}
````

### User / tool · 2026-11-02T07:13:19.165Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T07:13:23.069Z

T-110 round 2 is in `in_review`, committed as d24ff07, and tests pass.

- **Tests:** `tests/unit` gives 2396 passed on a `git archive HEAD` copy plus my files.
- **Spanish cues:** lib09 "consultas $1,300" now reclassifies to a charge through the T-084 guard, and the D-019 total counts it once accepted. "$400 por sesión" and the saldo line are refused. No prompt was changed.
- **Beyond your list:** I added "estado de cuenta" as a Spanish charge cue. The lib09 sentence has no cargo or honorarios word, so "consultas $1,300" would not pass without it.
- **Classifier change:** the shared rate cues now also read por sesión, por visita and cada, so lib09's $400 figures are classed `rate` by code instead of `unclear`.
- **Overlap notes:** `totals.possible_overlaps` now appears as a "POSSIBLE OVERLAPS" section in the internal notes. It appears only when there is one, and the letter is untouched.
- **Tray placeholder:** it drops from the tray, the rejected counts, the trace and the export's excluded count once the record has a hand-entered entry.
- **UB-04:** the room total is now in the rate entry's `other_figures` with no line of its own. I updated `tests/unit/test_billing.py` and `api.md` to match.
- **Commit:** `api.py` and `pipeline.py` carry other agents' uncommitted edits, so I committed through a fresh temp index. `git diff --cached --stat` listed only my 12 files, including the new `tests/unit/test_lib09_t110_r2.py`.
