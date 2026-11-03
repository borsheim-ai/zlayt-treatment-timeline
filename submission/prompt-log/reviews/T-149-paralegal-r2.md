# T-149 round 2 paralegal review (paralegal-reviewer, Maria Delgado persona)

Verdict: **changes** (0 blockers, 1 major, 4 minors, 2 nits). Two of my three round-1 majors are fixed; the third (a "Do this first" line that names the item) is only half fixed.

I ran `git archive 802d5fd` into the scratchpad (`r2-802d5fd`). HEAD was 95ffe36 by the end; `git diff --stat 802d5fd 985dbd2 -- app/frontend` touched only review.js, timeline.js, uncovered.css and uncovered.js, so the overview and detail code under review is the same. I served it on 127.0.0.1:7943 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. I created 9 cases: 6 seeded by API paste (3 unnamed, 2 named, 1 never analyzed), 2 pasted through the home screen (one named, one unnamed then renamed), and 1 accidental duplicate. The server (PID 1826) was stopped by PID: `lsof -iTCP:7943 -sTCP:LISTEN` exit 1, curl 000. Port 7860 was not touched. Scripts and outputs are in `artifacts/review-evidence/T-149-paralegal-r2/`.

## Round-1 majors

**F-1 case names: fixed.** The home screen has a "Client or matter" field (`p1.out.txt`: `input-title`). A named paste shows its name in the header ("Nguyen - dog bite"). An unnamed paste gets the provider and date of record 1 ("Brightwater EMS run report, Jan 22, 2026"), never "Untitled case" (`p16.out.txt`: "Untitled anywhere: False"). Rename in the detail header ("Park - pedestrian ORIF") survived a reload and showed in the overview. Rename is only in the detail header, not on the row; that is fine.

**F-2 export green while items are unreviewed: fixed.** With 1 of 14 items decided the row and the block read the amber "Can export — 13 not reviewed (they stay out of the letter)" (`p5.out.txt`). The green "Everything decided" appeared only at 14 of 14 (`p14.out.txt`), and the filters then read "Needs attention (5)", "Ready to send (1)". A partly reviewed case (2 accepted, 1 dismissed, 8 not reviewed) showed amber, and its export summary says "8 items pending (2 flags)". The letter held exactly the two accepted entries; the dismissed one and the unreviewed ones were absent (`p20.out.txt`, `export-nguyen-partial.txt`). The two cases I worked to the end exported with only accepted items and cited quotes; the sample total reads $8,390.00 (`export-sample.txt`; line wording follows D-062).

**F-3 one "Do this first" line that names the item and links to it: half fixed (F-A below).** There is one line per block and the button lands on the item the server named. It does not name the item, and two buttons still disagree.

## Can I tell at a glance which case needs me, and why?

Partly. The rows show "n of N decided", per-kind bars, "n need review" and, with 9 cases, the "Needs attention first" sort puts the untouched cases with the most items left on top (`p19.out.txt`). But six of the seven untouched rows carry the same sentence, "Nothing is accepted or edited yet, so the letter would be empty." and none says what kind of item waits (date conflict, gap, prior condition), so I cannot rank by what the adjuster will attack. Never-analyzed cases now say "Not analyzed: open the case and press Analyze." (fixed since round 1). Working two cases from the overview to export (Delgado, 14 items, and the Rivera sample, 23 items, the latter in 62 seconds of keyboard work including waits) went smoothly: j/k and Enter on the overview, "Go to it", then `a`, `d`, `e` and Enter on the compare button.

## Findings

**F-A (major). "Do this first" does not name the item, and the block still holds two blue buttons with different first steps.** On the Rivera sample the line reads "Do this first: This figure is a rate, not a charge, so it is not added to the total." No record, provider or amount is named (`p2.out.txt`); "Go to it" lands on amount `$185` (a2). The primary "Start review" button directly under it lands on flag `f_r7_1`, the accident-date source (`p3.out.txt`: "Start review -> flag-f_r7_1", "Go to it -> amount-$185"). On lib02 "Go to it" lands on flag f_r2_1 and "Start review" on entry e4 (`p3.out.txt`). The same sentence is shown for different items: "A second AI check disagreed with the first result for this item." was the line for f_r7_1, then for f_r7_2, then f_r7_3 as I decided them (`p10.out.txt`, `p11.out.txt`, `p12.out.txt` steps 1 and 2), so I could not tell the line had moved on. Expanding "Case checks" gives a third answer, "What you need to do: This item cannot be used. Dismiss it, or write the entry by hand from the record." (`p3.out.txt`, lib02), again naming nothing. The card's own test stubs a `next_action` reason and never asserts that the line names a record or provider (`tests/e2e/test_multicase.py:514-529` in the archive). That is the round-1 acceptance test "its text names a record or provider; Start review never names a different target", still unmet. Fix: build the line as "Do this first: Record 4, Capital PT: <reason>" (or "$185.00 rate, record 4") from `next_action.item_id`; make "Start review" go to the same item as "Go to it", or show only one of them. Acceptance test: on the Rivera sample and lib02 the do-first text contains the record number or provider of the item at `next_action.item_id`, and the focus after "Go to it" and after "Start review" is the same `data-item-id`.

**F-B (minor). The line disappears while items are still pending.** With 3 items left (1 gap flag, 2 charges) the server's `next_action` was null and the block showed no "Do this first" line, only "Start review" and the case-checks bar (`p12.out.txt`: "!! no do-first button with pending (3, 0, 5, True, None)"). On the Rivera sample, from step 5 to 23 (18 items down to 1 pending) every step went through "Start review (no do-first line)" (`p18.out.txt`). The block never says what comes next once the AI-flagged items are done. Fix: when `next_action` is null and items are pending, show "Do this first: Review the remaining n items" with the same target as "Start review". Test: a case with pending items always has one do-first line.

**F-C (minor). The overview row overstates "need review" against the detail.** After I decided some flags, the Delgado row read "5 need review" while the opened case read "3 items need review" (`p8.out.txt` row, `p9.out.txt` block), and "5 need review" again against "2 items need" (`p12.out.txt` start). The server's `hitl.needs_review` stays at 5 (second value of the tuple in `p12.out.txt` is pending, third is `needs_review`: "(5, 0, 5, True, 'f_r7_2')"). The handoff says the backend field `needs_review_open` is still to come. It errs on the safe side, but the row and the detail disagree about the same case. Fix: the backend returns the open count; the row uses it. Test: row count equals the detail header count after decisions.

**F-D (minor). The case checks contradict the new wording and go stale.** The block chip says "Can export — 13 not reviewed", while the Case checks line says "Ready to export, 13 not reviewed" (`p5.out.txt` step 1). When everything is decided the expanded checks still carry "What you need to do: Review the 2 items the AI objected to" (`p14.out.txt`). Fix: use one phrase ("Can export, n not reviewed") in both places, and clear the step text when nothing is pending.

**F-E (minor, carried from round 1 F-5). The row says how many but not why.** Six rows repeat the same blocker sentence and the "n need review" chip has no kind (`p19.out.txt`). The handoff lists the "why" line as skipped. On the sample the first do-first items are the $185 rate, a $ figure that is not a bill, and a phrase-list flag; the accident-date conflict was only reached in step 14 (`p18.out.txt`). Fix: one line under the chips from the server's kinds ("1 date conflict, 1 gap, 2 prior conditions"), and rank date conflicts and gaps ahead of rate notes in `next_action`.

**F-F (nit). Identical derived titles for identical records.** Pasting the same records twice gives two rows "Austin EMS run report, Jan 9, 2026" (`p19.out.txt`). Say so on the row ("same title as another case") or add the created minute.

**F-G (nit). Test count does not match the card.** The card says "36 pass"; plain pytest from the archive gave "35 passed, 1 skipped" (`pytest-multicase.out.txt`). The skipped one is the screenshot test (needs `ZLAYT_SCREENSHOTS=1`). The round-1 keyboard failure did not recur.

## What I exercised

1. `git archive 802d5fd`, server on 7943 (PID 1826, stopped); `setup_r2.py` seeded 6 cases and read GET /api/cases (`setup.out.txt`).
2. `p1_overview.py`: row text, sorts, filters, home inputs. `p2_detail.py`, `p3_targets.py`: do-first, Start review and case-next-action on four cases.
3. `p4_shortcuts.py`: j/k/Enter on the overview. `p5` to `p14`: Delgado edited (Rec 3), compared, a flag dismissed, all 14 items decided with the keyboard; row and filters after each stage.
4. `p15_export.py` on both worked cases; `p18_work_B.py` on the Rivera sample; `p16_paste_ui.py` (named paste, unnamed paste, rename, reload); `p17_titles.py`; `p20_partial.py` (partly reviewed case and its export panel).
5. `tests/e2e/test_multicase.py` from the archive with plain pytest.

```json
{"card": "T-149", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 802d5fd (frontend identical to HEAD at review start 985dbd2 apart from review.js, timeline.js, uncovered.css/js) served on http://127.0.0.1:7943 (PID 1826, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; 9 cases (6 API-pasted, 2 pasted in the UI, 1 duplicate); two cases worked from the overview to export (Delgado v. Hartwell truck rear-end, Rivera sample); live dev app 7860 not touched",
 "exercised": [
  "git archive 802d5fd into the scratchpad; server on 7943 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 1826 (lsof exit 1, curl 000)",
  "seeded 6 cases through POST /api/cases (3 unnamed, 2 named, 1 left unanalyzed) and read GET /api/cases (setup_r2.py)",
  "overview in the browser: row text, filters, sorts, home inputs, j/k/Enter (p1_overview.py, p4_shortcuts.py)",
  "detail of four cases: do-first line, Go to it and Start review focus targets, case-next-action text (p2_detail.py, p3_targets.py)",
  "pasted two cases through the home screen (one with a name, one without), renamed one in the detail header, reloaded, read the overview titles (p16_paste_ui.py)",
  "worked Delgado v. Hartwell from the overview to export with the keyboard: renamed, edited Rec 3, compared, dismissed a flag, accepted the rest; read the row and filters at 1 of 14, 12 of 14 and 14 of 14 (p5 to p14)",
  "worked the Rivera sample from the overview to export: edited Rec 3, dismissed the rate and a flag, accepted the rest, 62 seconds (p18_work_B.py)",
  "exported both cases and a partly reviewed third case; read the letter text and the export summary and internal notes block (p15_export.py, p20_partial.py)",
  "tests/e2e/test_multicase.py from the archive with plain pytest: 35 passed, 1 skipped"
 ],
 "verdict": "changes",
 "scores": {"verify_quickly": 4, "overview_triage": 3, "ready_to_send_signal": 4, "detail_first_action": 3, "identify_case": 4},
 "findings": [
  {"severity": "major", "title": "'Do this first' does not name the item, and 'Start review' goes to a different item than 'Go to it'",
   "evidence": "artifacts/review-evidence/T-149-paralegal-r2/p2.out.txt sample: 'Do this first: This figure is a rate, not a charge, so it is not added to the total.' (no record, provider or amount); p3.out.txt: sample 'Start review -> flag-f_r7_1' vs 'Go to it -> amount-$185', lib02 'Start review -> entry-4' vs 'Go to it -> flag-f_r2_1'; p10/p11/p12 out: the identical sentence 'A second AI check disagreed with the first result for this item.' shown for f_r7_1, f_r7_2, f_r7_3; p3.out.txt lib02 case-next-action 'This item cannot be used. Dismiss it, or write the entry by hand from the record.'; tests/e2e/test_multicase.py:514-529 stubs a reason and never asserts a named record",
   "why_it_matters": "She asked 'what do I do first' and still gets two primary buttons with different targets and a sentence that names no record; with the same sentence for three flags she cannot tell the line moved. This was my round-1 major F-3.",
   "fix": "Build the line from next_action.item_id with the record number and provider or the amount ('Do this first: Record 4, Capital PT: ...'); make Start review go to the same item as Go to it, or show only one of them.",
   "acceptance_test": "e2e on the Rivera sample and lib02: the do-first text contains the record number or provider of the item at next_action.item_id; focus after 'Go to it' and after 'Start review' is the same data-item-id."},
  {"severity": "minor", "title": "The do-first line disappears while items are still pending",
   "evidence": "p12.out.txt: '!! no do-first button with pending (3, 0, 5, True, None)'; p18.out.txt steps 5 to 23 all 'via Start review (no do-first line)' with 18 down to 1 pending",
   "why_it_matters": "Once the AI-flagged items are done the block gives no sentence about what comes next, so the line she was told to rely on is absent for most of a review.",
   "fix": "When next_action is null and items are pending show 'Do this first: Review the remaining n items' with the same target as Start review.",
   "acceptance_test": "e2e: a case with at least one pending item has exactly one do-first line."},
  {"severity": "minor", "title": "Overview row 'need review' count is higher than the detail's for the same case",
   "evidence": "p8.out.txt row 'Delgado v. Hartwell - truck rear-end ... 5 need review | Can export - 6 not reviewed' vs p9.out.txt opened block '3 need review' and header '3 items need review'; p12.out.txt start row '5 need review' vs detail header '2 items need'; server tuple (pending, edits, needs_review, ready, next) = (5, 0, 5, True, 'f_r7_2')",
   "why_it_matters": "The same case reads 5 on the overview and 2 in the detail; the number she uses to choose a case is not the number she meets (the error is on the safe side).",
   "fix": "Backend returns the open needs-review count (the handoff names hitl.needs_review_open) and the row uses it.",
   "acceptance_test": "e2e: after deciding some flagged items, the overview row count equals the count in the opened case's header."},
  {"severity": "minor", "title": "Case checks say 'Ready to export, n not reviewed' beside the amber 'Can export'; stale step text after everything is decided",
   "evidence": "p5.out.txt step 1: chip 'Can export - 13 not reviewed (they stay out of the letter)' and 'Case checks | 7/10 checks passed | 3 need you | Ready to export, 13 not reviewed'; p14.out.txt at 14 of 14: 'Everything decided ... Case checks ... Ready to export | Show | What you need to do: Review the 2 items the AI objected to.'",
   "why_it_matters": "'Ready to export' beside unreviewed items is the wording round 1 asked to remove, and a leftover instruction after the case is done makes her doubt the green state.",
   "fix": "One phrase in both places ('Can export, n not reviewed'); clear the step's next-action text when nothing is pending.",
   "acceptance_test": "e2e: with pending items the page has no 'Ready to export' text; at 0 pending no 'What you need to do' text is visible."},
  {"severity": "minor", "title": "Row says how many need review but not why; the first do-first items on the sample are a rate and a non-bill, not the accident-date conflict",
   "evidence": "p19.out.txt: six untouched rows repeat 'Nothing is accepted or edited yet, so the letter would be empty.' with no kind; p18.out.txt steps 2 to 4 (a2 rate, a3 not a bill, f_r7_1) and f_accident_date_after_treatment_1_2_7 only at step 14; handoff lists the why line as skipped",
   "why_it_matters": "Checklist 16: items needing review say why in one sentence, and she cannot rank cases by what the adjuster will attack.",
   "fix": "One line under the chips from the server's kinds ('1 date conflict, 1 gap, 2 prior conditions'); rank conflicts and gaps ahead of rate notes in next_action.",
   "acceptance_test": "e2e: the Rivera sample row contains 'conflict' and 'gap' counts equal to the flags of those kinds from GET /api/cases/{token}; its first do-first item is a conflict or gap flag."},
  {"severity": "nit", "title": "Identical derived titles for the same records pasted twice",
   "evidence": "p19.out.txt: two rows titled 'Austin EMS run report, Jan 9, 2026'",
   "why_it_matters": "Two rows she cannot tell apart until she opens them.",
   "fix": "Add the created minute to the title or a 'same title as another case' hint.",
   "acceptance_test": "e2e: paste the same text twice; the two overview titles differ."},
  {"severity": "nit", "title": "Card evidence '36 pass' does not match plain pytest: 35 passed, 1 skipped",
   "evidence": "artifacts/review-evidence/T-149-paralegal-r2/pytest-multicase.out.txt: '35 passed, 1 skipped in 20.99s' (skip = the screenshot test needing ZLAYT_SCREENSHOTS=1)",
   "why_it_matters": "Evidence should reproduce as written.",
   "fix": "State '35 pass, 1 skipped (screenshots)' in the card.",
   "acceptance_test": "pytest tests/e2e/test_multicase.py in a clean archive prints no failures."}
 ],
 "whats_right": [
  "Cases get real names: a name field at create, a rename that survives reload, and a default from record 1's provider and date; 'Untitled case' never appeared.",
  "Green appears only at 'Everything decided'; any unreviewed item gives amber 'Can export - n not reviewed (they stay out of the letter)', the Ready to send filter matches, and the letters held only accepted items with cited quotes.",
  "Keyboard flow from the overview (j/k, Enter, Go to it, a, d, e, compare button) took a 23-item case from open to export in 62 seconds."
 ],
 "questions_for_chris": []}
```
