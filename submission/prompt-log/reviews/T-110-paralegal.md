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
