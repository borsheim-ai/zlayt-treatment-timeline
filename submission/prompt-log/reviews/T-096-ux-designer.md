# T-096 review: UI for suggestions and confidence (ux-designer-reviewer)

Verdict: **changes**. No blocker. One major (keyboard reach), five minors, one nit. Run as claude-haiku-5-5 (the model this session runs as); the dossier's expected id (claude-opus-5-5) does not apply to this run.

## Scope and pin
- Card commit 36ceb38 (`git cat-file -t 36ceb38` gave a commit; `git log -1` shows "feat(frontend): T-096 pre-selected date suggestion, dismissal banner, measured precision (with stale note), overlap warning, flag tray wording").
- Repo root at review time: `git rev-parse --short HEAD` gave 36ceb38; `git status --short | wc -l` gave 1473 (dirty), so I did not use the repo-root tree. I ran `git archive 36ceb38` into the scratchpad copy `t096-ux-36ceb38`.
- Server: `PORT=7898 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratchpad>/t096-ux.sqlite3`, started from the archive copy. Listener PID 29480 (wrapper 29479). Both stopped; `curl -s -o /dev/null -w "%{http_code}"` on 7898 returned 000.
- Scratch-only setup, disclosed: the archive has no .git, so `evals.run` recorded `source_commit: null`, which the calibration route rejects (status invalid). I ran `python -m evals.run --out <scratch>` (fixture backend), copied the scratch `calibration.json` into the archive's `evals/reports/`, and set `source_commit` to "36ceb38". After that the route returned status ok. No product file was changed. The prompt-stale probe edited `app/llm/prompts/judge_flag_v3.md` in the archive copy and restored the original bytes (`prompt_restored_bytes_equal: true`).

## What I exercised
- API probes (`artifacts/review-evidence/T-096-ux-api-probe.py`, `T-096-ux-sentences-probe.py`): case_01 suggestion fields, case_lib01 and case_lib06 tray items, and a sweep of 24 library/golden files for records without sentences (none found).
- Playwright walk (`artifacts/review-evidence/T-096-ux-designer-walk.py`) at 1440x900 and 390x844: date suggestion before and after one click, dismissal banner (real route, three setup dismissals kept alive), idle wait, Hide similar and Keep showing, reload, measured-precision line, stale line (real route after a prompt edit), overlap warning, tray flag wording, manual-entry no-sentences state, horizontal overflow on each page, and Tab counts to the new controls.
- `tests/e2e/test_suggestions.py` against port 7898: 23 passed in 33.64 s.
- Export: `GET /api/cases/<tok>/export` on case_lib06 returned 422 while items were unreviewed. The "not in the letter" tray claim is therefore code-supported (present.py:222-225, D-053 comment; the `flags` list filters rejected items at present.py:237), not confirmed in an export run.
- Route stubs, disclosed: (a) sentences_reason: the real backend produced no record without sentences in any of the 24 files, so the manual-entry state was reached by rewriting GET /api/cases/<tok>. (b) LLM_ONLY tray reason: rewritten the same way. Both are the same stub approach as tests/e2e/test_suggestions.py.

## Card checks
1. Date suggestion pre-selected with reason, one confirm: PASS. 1440 and 390 both show 2026-04-05 checked, "Suggested · MM/DD", the reason, and Confirm enabled. The 2026-04-05 entry was absent from the queue before the click (0) and present after one click (1). Keyboard reach is the problem (F1).
2. Dismissal banner hides only on click: PASS. Visible on load, still visible after 3 s idle, flag still pending. Hide similar (1440) removed the banner and dismissed the flag, with the live message "Hid 1 similar flag. It stays under Dismissed and you can reset it." Keep showing (390) hid it for the session only, and a reload brought it back (F2).
3. Measured precision: PASS. Line reads "Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)." Small-sample note present. innerText has no "%". Stale path: with a prompt edit, data-stale is "true" and the note shows (F4 on copy).
4. Overlap warning beside the total: PASS. Overlap box sits 87 px below "Accepted charges: $0" inside charges-panel at 1440 (accepted total y 7999, overlap y 8086). No overflow at 390.
5. Could-not-verify wording for flags: substance right, wording not (F5).
6. sentences_reason: shows when there are no sentences, but only through the stub, and the copy repeats itself (F6).

## Findings

### F1 (major): keyboard path to Confirm date and Hide similar is 87 to 102 Tab presses
Measured from document start (blur, scroll to top, press Tab until the target's data-testid matches): btn-confirm-date 87 presses at 1440 and 88 at 390; btn-hide-similar 101 at 1440 and 102 at 390. Pointer path is one click for each. Source of the numbers: the walk output, `artifacts/review-evidence/T-096-ux-designer-walk.py` (keys date_tab_presses_to_confirm, tab_presses_to_hide_similar).
Why it matters: the paralegal is a keyboard-first expert. The dossier's threshold is more than two actions per verification, which makes this a major. Same pattern as the T-046 r2 finding.
Fix: give the dates-to-confirm form and the dismissal banner keyboard entry within two actions, for example a shortcut shown in the Keyboard line, or a skip link placed before the queue, and keep the controls in document order.
Acceptance test: from page load, the focused element is btn-confirm-date (and btn-hide-similar) within 2 key actions, asserted in tests/e2e/test_suggestions.py.

### F2 (minor): Keep showing is not remembered across a reload
At 390, after Keep showing, the banner count was 0. After page.reload() it was 1 (`after_keep_then_reload_banner_count`). The e2e test covers only the in-session repaint. The copy does not say the choice resets.
Fix: persist Keep showing per case (localStorage keyed by case token, or a server flag), or say on the banner that the choice lasts for this visit only.
Acceptance test: click Keep showing, reload, assert dismissal-suggestion count is 0.

### F3 (minor): banner sits far below the fold
Sample case, first load: the dismissal box's top is at y 4778 px at 1440x900 and y 8185 px at 390 (`banner_box_top_vs_flags_top`), inside the flags panel. A paralegal who does not scroll to Flags never sees it. Same fold problem as the gap flag already recorded in memory (project_sample_case_gap_flag_fold).
Fix: a one-line pointer near the top of the review (for example beside the progress count) saying a dismissal suggestion is waiting in Flags, or the count of suggestions.
Acceptance test: on first load at 1440x900 of the sample case, a visible pointer to the suggestion exists without scrolling.

### F4 (minor): stale note repeats itself, shows a file name, and follows the number
Verbatim `stale_note_text`: "These numbers come from an older version of the AI prompts. The prompts have changed since these numbers were measured: judge_flag_v3.md changed. The numbers describe an older version of the prompts." The phrase "older version" appears twice. "judge_flag_v3.md" is developer vocabulary, not the paralegal's. The note also sits under the 84/85 sentence, so the number is read before the warning. The copy comes from app/backend/calibration_route.py (stale_reason), which the frontend renders verbatim.
Fix: say it once, drop the file name (for example "The detection prompt changed after these numbers were measured"), and place the note above the counts.
Acceptance test: with stale true, the note precedes calibration-verified in DOM order, contains no ".md", and contains "older version" once.

### F5 (minor): could-not-verify flag wording uses internal terms and restates itself
Real lead (case_lib06, JUDGE_DISAGREES): "AI suggested a flag that the second check did not confirm; it is not in the letter." Real why: "A second AI check disagreed with the first result for this item. The AI found this flag but the phrase list did not; check that it applies. The second check does not find this flag supported by the quote." Under the LLM_ONLY reason (route stub) the lead says "the code check did not find". "Phrase list" and "code check" are internal terms, and the why repeats the lead three times. The item also does not say what the paralegal can do with it.
The lead's claim "it is not in the letter" is code-supported (present.py:222-225, D-053) but not confirmed by an export run (see Scope).
Fix: one plain sentence per reason, for example "The AI suggested this flag. The checks did not support it, so it is left out of the letter." Replace "code check" and "phrase list" with paralegal terms, and say once what to do (nothing to accept; read the attempt).
Acceptance test: tray flag lead and why contain none of "code check", "phrase list", "second AI check"; e2e updated to the new fixed sentence.

### F6 (minor): sentences_reason copy repeats, and the real path is not reached by any corpus case
Measured (stub): "This record has no sentences to pick from. This record has no Date and Source lines, so no sentence can be cut from it." The sentence "This record has no" appears twice. Across 24 library and golden files the backend produced zero records without sentences, so this state is reachable only through the stub.
Fix: one sentence, for example "No sentence can be picked from this record: it has no Date and Source lines." Add a corpus case or a fixture that produces a record without sentences, so the real path is tested.
Acceptance test: a real (non-stubbed) case with a sentenceless record shows manual-no-sentences with the backend reason.

### F7 (nit): measured-precision line is below the first screen
calibration-line top is y 2098 px at 1440x900 and y 3665 px at 390. Not a card requirement; mentioned so the precision line is not forgotten on the first screen. Optional.

## Whats right
- The date suggestion is pre-selected and reasoned, and it still needs one Confirm click. The 2026-04-05 entry was not in the queue before the click.
- The dismissal banner never hid on load or after 3 s idle, and Hide similar acted only on click, with a clear live message.
- The overlap warning sits directly under the accepted total, names both figures and both records, and adds no number of its own.

## Scores
design quality 4, originality 3, craft 3, functionality 4. No score at or below 2, so no blocker is required by the scoring rule.

```json
{"card": "T-096", "persona": "ux-designer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 36ceb38 via git archive into scratchpad t096-ux-36ceb38; local server 127.0.0.1:7898 (fixture backend, ZLAYT_MODE=local, scratch DB), stopped by PID; sample case, case_01_date_formats, case_lib06, case_lib01, case_lib09; calibration.json scratch copy with source_commit set to 36ceb38 (archive has no .git); route stubs for sentences_reason and LLM_ONLY tray reason",
 "exercised": [
  "git cat-file -t 36ceb38; git log -1 36ceb38 (commit confirmed); git rev-parse --short HEAD (36ceb38); git status --short | wc -l (1473, dirty, so git archive used)",
  "git archive 36ceb38 into scratchpad; server started from the archive copy with PORT=7898, HOST=127.0.0.1, LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local; stopped by PID 29480 (wrapper 29479); port 7898 returns 000 after stop",
  "evals.run --out scratch (fixture); calibration.json copied into archive evals/reports; source_commit set to 36ceb38; GET /api/calibration status ok, stale false, then stale true after prompt edit, then false after restore",
  "artifacts/review-evidence/T-096-ux-api-probe.py and T-096-ux-sentences-probe.py (suggestion fields, tray items, 24 files swept for sentenceless records: none)",
  "artifacts/review-evidence/T-096-ux-designer-walk.py at 1440x900 and 390x844: date suggestion before and after one click; dismissal banner on load, after 3 s idle, Hide similar (1440), Keep showing and reload (390); Tab counts to btn-confirm-date (87/88) and btn-hide-similar (101/102); calibration line text, small-sample note, no percent; stale line; overlap warning and bounding boxes; tray flag lead and why; manual-no-sentences state (stub); horizontal overflow on every page (none)",
  "GET /api/cases/<tok>/export on case_lib06: 422 while items unreviewed (tray claim not verified end to end); present.py:222-225 and :237 read for the tray-flag exclusion",
  "tests/e2e/test_suggestions.py against E2E_BASE_URL=http://127.0.0.1:7898: 23 passed in 33.64 s",
  "screenshots: artifacts/review-evidence/T-096-ux-1440-dates-preselected.png, T-096-ux-390-dates-preselected.png, T-096-ux-1440-dismissal-banner.png, T-096-ux-390-dismissal-banner.png, T-096-ux-1440-calibration-stale.png, T-096-ux-*-overlap-warning.png, T-096-ux-*-tray-flag-real.png, T-096-ux-*-manual-no-sentences.png"
 ],
 "verdict": "changes",
 "scores": {"design quality": 4, "originality": 3, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major", "title": "Keyboard path to Confirm date and Hide similar is 87 to 102 Tab presses from document start",
   "evidence": "T-096-ux-designer-walk.py output: date_tab_presses_to_confirm 87 (1440) and 88 (390); tab_presses_to_hide_similar 101 (1440) and 102 (390); pointer path is one click each",
   "why_it_matters": "The paralegal is keyboard-first; the dossier threshold is more than two actions per verification. Same pattern as the T-046 r2 finding.",
   "fix": "Give the dates-to-confirm form and the dismissal banner keyboard entry within two actions (shortcut shown in the Keyboard line, or a skip link before the queue), keeping document order.",
   "acceptance_test": "From page load, focus reaches btn-confirm-date and btn-hide-similar within 2 key actions; asserted in tests/e2e/test_suggestions.py"},
  {"severity": "minor", "title": "Keep showing is not remembered across a reload",
   "evidence": "walk output at 390: after_keep_banner_count 0, after_keep_then_reload_banner_count 1",
   "why_it_matters": "The banner returns on every visit to the case after the paralegal said keep showing; the copy does not say the choice is temporary.",
   "fix": "Persist Keep showing per case (localStorage keyed by case token, or a server flag), or state on the banner that the choice lasts for this visit.",
   "acceptance_test": "Click Keep showing, reload, assert dismissal-suggestion count is 0"},
  {"severity": "minor", "title": "Dismissal banner is far below the fold",
   "evidence": "walk output: banner_box_top_vs_flags_top y 4778 px at 1440x900 and y 8185 px at 390; memory project_sample_case_gap_flag_fold documents the same fold for the gap flag",
   "why_it_matters": "A paralegal who does not scroll to Flags never sees the suggestion.",
   "fix": "Add a one-line pointer near the top of the review (for example beside the progress count) that says a dismissal suggestion is waiting in Flags.",
   "acceptance_test": "First load of the sample case at 1440x900 shows a visible pointer to the suggestion without scrolling"},
  {"severity": "minor", "title": "Stale note repeats itself, shows a file name, and sits after the number",
   "evidence": "walk output stale_note_text: \"These numbers come from an older version of the AI prompts. The prompts have changed since these numbers were measured: judge_flag_v3.md changed. The numbers describe an older version of the prompts.\" Source: app/backend/calibration_route.py stale_reason",
   "why_it_matters": "Developer vocabulary (a file name) and a duplicated phrase in a trust-critical note; the 84/85 count is read before the warning.",
   "fix": "Say it once, drop the file name (for example 'The detection prompt changed after these numbers were measured'), and place the note above the counts.",
   "acceptance_test": "With stale true, the note precedes calibration-verified in DOM order, contains no '.md', and contains 'older version' once"},
  {"severity": "minor", "title": "Could-not-verify flag wording uses internal terms and restates itself",
   "evidence": "case_lib06 real tray: lead 'AI suggested a flag that the second check did not confirm; it is not in the letter.'; why 'A second AI check disagreed with the first result for this item. The AI found this flag but the phrase list did not; check that it applies. The second check does not find this flag supported by the quote.'; LLM_ONLY stub lead 'the code check did not find'",
   "why_it_matters": "'Phrase list' and 'code check' are internal; the why repeats the lead three times and does not say what the paralegal can do. The 'not in the letter' claim is code-supported (present.py:222-225, D-053) but not confirmed by an export run (export returns 422 while items are unreviewed).",
   "fix": "One plain sentence per reason, e.g. 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' Replace internal terms; say once what to do.",
   "acceptance_test": "Tray flag lead and why contain none of 'code check', 'phrase list', 'second AI check'; e2e fixed sentence updated to match"},
  {"severity": "minor", "title": "sentences_reason copy repeats, and no corpus case reaches it",
   "evidence": "walk output manual_no_sentences_text (route stub): 'This record has no sentences to pick from. This record has no Date and Source lines, so no sentence can be cut from it.'; sentences probe: 0 records without sentences across 24 library and golden files",
   "why_it_matters": "Repeated opening words in a short message; the real path is untested outside a stub.",
   "fix": "Use one sentence, e.g. 'No sentence can be picked from this record: it has no Date and Source lines.' Add a fixture that produces a sentenceless record.",
   "acceptance_test": "A non-stubbed case with a sentenceless record shows manual-no-sentences with the backend reason"},
  {"severity": "nit", "title": "Measured-precision line sits below the first screen",
   "evidence": "walk output cal_box y 2098 px at 1440x900; y 3665 px at 390",
   "why_it_matters": "Not a card requirement; the trust line is not on the first screen.",
   "fix": "Optional: place the line nearer the progress count.",
   "acceptance_test": "Optional"}
 ],
 "whats_right": [
  "The date suggestion is pre-selected with its reason and still needs one Confirm click; the 2026-04-05 entry was absent from the queue before the click (0) and present after (1)",
  "The dismissal banner never hid on load or after 3 s idle; Hide similar acted only on click, with a clear live message",
  "The overlap warning sits directly under the accepted total, names both figures and both records, and adds no number of its own"
 ],
 "questions_for_chris": ["Should the dismissal suggestion surface at the top of the review rather than inside Flags?"]}
```
