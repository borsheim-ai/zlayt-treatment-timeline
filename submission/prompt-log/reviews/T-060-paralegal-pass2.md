# T-060 pass 2 — paralegal-reviewer (Maria Delgado persona)

Verdict: **pass** (0 blockers, 0 majors, 9 minors, 1 nit). All five pass-1 majors are fixed or reduced to minors. I can now review both cases in page order from the keyboard, with no re-positioning clicks. On lib09 I decided all 19 items one by one and reached "Ready to export" first try, where pass 1 needed a forced dismiss. Information density and letter format are the weak parts; the letter text is still not paste-ready (F9).

## What I ran
App: `git archive HEAD` copy, commit `b89b9d9` (`git rev-parse --short HEAD`), in my scratchpad. `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, port 7881, own SQLite file. Playwright, Chromium, 1440x900. The server was stopped by PID (79883 and its parent 79882); `curl` to port 7881 then printed `000`. Scripts `q0` to `q13` and screenshots are in `artifacts/review-evidence/T-060-pass2/` (the `ux2-*` files there belong to the ux-designer). All timings are script times: they include a 350 ms wait after every key press (about 6 s of the 10 s in task 1), so they are not a human reading time.

## Task 1: case_01 (evals/golden/case_01_date_formats.txt), paste to clipboard
| | Pass 1 | Pass 2 |
|---|---|---|
| Route | 1 paste, 3 clicks, 6 keys; `Shift+A` accepted 8 rows with no row read | 1 paste, 1 click (Analyze), 18 keys; every decision made one by one |
| Keys | `j`, `Tab`, `Enter`, `Shift+A`, `j`, `a`; then Export and Copy by click | Tab x3, Enter (jumps to the date choice), Tab, Enter (confirm), `a` x9, Enter on Export, Tab, Enter on Copy |
| Script time | 9.2 s | 10.2 s |
| In-order accept by keyboard | impossible (focus jumped from row 1 to row 8) | works: `a` moves to the next undecided item; after the 9th `a` focus lands on Export (`04-all-decided.png`) |
| Clipboard | 1,732 chars, plain text | 1,732 chars, no HTML, no markdown (`task1-clipboard.txt`) |

Focus after the date confirm now goes to that entry's Accept button (pass 1: `<body>`). The date step is reachable from three Tabs because the "Open decisions" strip has a "1 date to confirm" button. The header shows "9 of 9 decided" and a focused Export button when I finish.

## Task 2: library lib09 (Spanish), load to clipboard
| | Pass 1 | Pass 2 |
|---|---|---|
| Clicks | 10 (6 were re-positioning), plus 1 load | 3: open "Cases and synthetic library", load lib09, click the "1 date to confirm" chip |
| Keys | 17 | 24 (Tab, Enter, 19 `a`/`d` decisions, Enter on Export, Tab, Enter on Copy) |
| Script time | 19.5 s | 15.2 s |
| Items individually decided | 15 of 19 (4 came from `Shift+A`) | 19 of 19 (`q9-lib09-full.py` output) |
| Export | blocked once; I had to dismiss 2 accepted rows | "9/10 checks passed · 1 need you · Ready to export" at the first attempt (`12e-ready.png`) |
| Page height | 11,133 px | 8,582 px |

`j` now walks one list in page order across panels: e4, e2, e7, e1, e3, e5, e6, then six flags, then seven charges (`q11-jwalk.py`). It stops at the last charge. Letter and notes: `task2-export-letter.txt`, `task2-export-notes.txt`; total reads "Billed charges stated in these records: $5,090.00", unclear amounts and the two $400 rates appear only under AMOUNTS NOT TOTALED in the notes.

## Pass-1 findings, status
| # | Pass-1 finding | Status | Evidence |
|---|---|---|---|
| F1 | Keyboard review breaks across panels | **Fixed** (two small residuals, N1 and N2 below) | `q8` log: `a` visits every item with focus on the next one; `q11` j-walk; shortcuts only act from an item row (`review.js:304-331`) |
| F2 | Needs-review not first; hand-off hidden | **Fixed**, residual minor (F14 below) | `01-after-analyze.png`: "Open decisions" strip with jump buttons, "What you need to do" bar visible at the top; queue sorts needs-review first (lib09: e2, e7 ahead of verified); stepper decision row shows "Needs your decision" with a "Go to Dates to confirm" button (`21-stepper-open.png`) |
| F3 | Accept blocks export; dead-end recovery | **Fixed** | the two "$400 Rate" rows and the unclear rows now offer "Keep in notes" (`12-unclear-tray.png`); accepting every item ends in "Ready to export" |
| F4 | Gap moved 42 to 40 after date confirm | **Fixed** | `q9` output: "GAP BEFORE: Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026" and "GAP AFTER" is identical; the letter notes say the same |
| F5 | Charges and unclear rows too tall | **Partial** | tray 870 px for 5 rows (was 1,958), rows 133 px (target about 56), amount highlighted, 8-word snippet; boilerplate sits once in the tray header; the "Decision" column still stacks three controls (`12-unclear-tray.png`) |
| F6 | Timeline row density | **Partial** | rows 208 px (252 to 275 for rows with a reason bar); about 3.5 rows per 900 px screen, was 2; accepted rows keep a full-blue enabled "Accept" (`04-all-decided.png`), 11 buttons or links per row |
| F7 | "Verified" chip and Accept-all invite trust | **Partial** | `Shift+A` now asks first: "you have not decided on them one by one" with the count (`05b-shiftA.png`); chip still "Verified"; button still "Accept all verified entries (7)"; a mouse click on it accepts with no question (`q13` output: dialog None, "7 of 10 decided") |
| F8 | Export placement and finish | **Partial** (mostly fixed) | sticky header counter and Export; focus lands on Export after the last decision; Bates fields are now above the letter (tops 4,542 vs 5,128 px); "Ready to export, 3 not reviewed" cue; still: letter box 416 px high with 984 px of text, no download control, early-export message repeats itself (`20-early-export.png`) |
| F9 | Letter repeats summary and quote; "AI translation:" prefix | **Open** | `task2-export-letter.txt` lines for April 14, May 3 and May 20 start with "AI translation:"; every entry is summary line then `Source [Ex. __ / Bates __]: "quote"` |
| F10 | Dev panel in local mode | **Mostly fixed** | library collapsed into one "Cases (N) and synthetic library" line (`00-landing.png`); view starts at the top after a library load (scrollY 0); labels read "Open now: case lib09 spanish..." and "Untitled case ready · 8 records"; reload still returns to scrollY 0 (`23-after-reload.png`) though state was kept |
| F11 | `o` modal swallows the next key | **Open** | `q10`: `o` opens the dialog, `a` leaves e2 "pending" and nothing is said; `review.js:310` returns when a dialog is open |
| F12 | Formats and repeated messages | **Partial** | Edit now disabled on the undated row, message appears once (`q10`: e4 count 1); still `$2,940` next to `$650.00` in one panel (`12b-charges.png`), "Accepted charges: $5,090" vs letter "$5,090.00", ISO dates in rows vs long dates in flags |
| F13 | Prior-condition flag on an interpreter sentence | **Open** | `12c-flags.png`: "Hx obtained via patient's son, who interpreted." still raised; the card now says "The phrase list found this flag but the AI did not; check that it applies." which is honest, and the dismissal is listed in the notes under FLAGS DISMISSED |

## Remaining findings
All are minor or nit; none blocks the export or loses a fact. "Spec constraint" or "preference" is marked on each.

**F9 (minor, spec D-002 preference).** Letter lines print a summary line plus a `Source [Ex. __ / Bates __]: "quote"` line, and Spanish entries carry the literal prefix "AI translation:" in the letter. Checklist 19 asks for one line `date — provider: "quote" [Ex. __ / Bates __]`; all four parts are present, so this is length and cleanup, not missing content. Fix: option for the one-line form; make the translation note a bracketed removable phrase. Test: letter option exists that gives one line per entry; no line starts with "AI translation:" in the default letter.

**F13 (minor).** An interpreter note raises "Mention of a prior or pre-existing condition". The tool says so itself, but I still have to read and dismiss it, and it is the first flag I see in lib09's pre-existing panel. Fix: backend skips "Hx obtained via ..." for this flag. Test: lib09 raises no prior-condition flag.

**F5 (minor).** Unclear and charge rows are 133 px, the tray is 870 px. Fix: put amount, provider and date, snippet, status and one button on one 56 px row; secondary links behind a menu. Test: lib09 unclear tray under 700 px.

**F6 (minor).** Accepted rows should look settled: "Accept" stays blue and enabled. Fix: after accept, show a quiet "Accepted" state with Reset, drop the primary style, and fold the quote to one line. Test: after `a`, the row has no `btn--primary` and is under 110 px.

**F7 (minor).** "Verified" means checked by a person to me, and the export rules say no such labels in the letter. The mouse batch button skips the confirmation that `Shift+A` shows. Fix: chip text "Quote matches record"; the same confirm for the button. Test: no chip reads "Verified"; clicking "Accept all..." asks first.

**F8 (minor).** No file download; the letter sits in a scroll box inside a scrolling page; early export prints "The export is blocked. ... Blocking the export (1): Whole case ..." with the same sentence twice. Fix: box sized to its text, `.txt`/`.docx` download, one sentence. Test: letter box height equals scrollHeight; a download control exists.

**F11 (minor).** `o` then `a` does nothing, silently. Fix: `o` moves focus to the source pane, or show "Close the record first (Esc)". Test: `o` then `a` accepts or shows a message.

**F12 (minor).** Mixed currency formats (cents and no cents in one panel) and mixed date styles (ISO in rows, long in flags and letter). Fix: always cents, US long dates in the UI. Test: no `$\d+` without cents in the charges panel.

**N1 (minor, new). Keyboard entry after loading a library case.** After a mouse load of lib09 the page shows the top, but the first `Tab` jumps to the "Cases (9) and synthetic library" line at scrollY 7,348 (`q8-lib09-walk.py`: "first Tab after load -> SUMMARY ... y=7348"). Landing on the "1 date to confirm" chip by clicking it puts focus on a radio button, where `j` and `k` are ignored without a message (`q10` j-walk stayed on e4 for 30 presses). The shortcuts sheet says "use Start review", but no control carries that name; the skip link reads "Skip to the first item to review" and shows only on focus (`app.js:48`, `review.js:295`). Fix: after a case loads, move focus to the "Open decisions" heading (tabindex -1); rename the skip link to match the sheet; `j` from a radio moves to the next row. Test: after a library load, one `Tab` lands on the first button of Open decisions.

**N2 (minor, new). Needs-review entry left to the end.** On lib09, `a` on e7 sent focus to the flags and charges, and e2 (a needs-review entry) came last, after the charges (`q8` log: "a on a7 ... -> e2"). This matches the rule "items after the current one first, then wrap" (`review.js:94-98`), but it is not the order I read the page. Fix: when choosing the next item, prefer the nearest needs-review entry in the timeline panel before moving to flags. Test: on lib09 the 3 entries that need review are visited before the first flag.

**F14 (minor, new). Case-check bar wording.** The bar reads "9/10 checks passed · 1 need you · Ready to export" at the end, which contradicts itself. The stepper marks the date decision as an amber circled "✕" (`21-stepper-open.png`, markers `✓ ✓ ✕ ...`). Fix: "all decided; 1 check was not run" in plain words; use a "your call" icon, not a cross. Test: with everything decided, the bar shows no "need you" count.

**N3 (nit, new).** The pasted case is listed in the case list as "Untitled case ready · 8 records" six times after six runs. Fix: show the first record's date range or the paste time.

## Enterprise or prototype?
Closer to enterprise than before. The queue, hand-off strip, sticky counter and export focus behave like a review tool I would use. The first screen still has 5 stacked panels before the first record (records found, Open decisions, Case checks, What you need to do, How the AI was checked, accuracy note) and the rows are tall, so a 7-row case needs two screens. Information density is the main gap left.

## Prioritized remaining list
1. F9 one-line letter option and no "AI translation:" in the default text (the paste step).
2. F13 no prior-condition flag on "Hx obtained via ...".
3. F5 one-line unclear and charge rows under 700 px.
4. F6 settled look for accepted rows.
5. F7 "Quote matches record"; same confirm for the mouse batch button.
6. N1 entry focus after load; `j` from a radio.
7. F8 letter box sizing and `.txt`/`.docx` download.
8. F11 `o` then `a`.
9. F12 currency and date formats.
10. F14, N2, N3.

## Right already
- One linear queue: `j`/`k`/`a`/`d` cross panels in page order and the last `a` lands on Export.
- Unclear and rate rows say "Keep in notes" instead of "Accept", and the gap stays at 42 days after the intake date is confirmed.
- Shift+A asks first with the count; edit keeps "Original: ..." and decisions survive a reload.

```json
{"card": "T-060", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive HEAD b89b9d9 (frontend commits 3e3f3b7, eabe2b8, 9fcae9b) in scratchpad; app http://127.0.0.1:7881 (fixture, curated, ZLAYT_MODE=local); case_01_date_formats.txt pasted, library lib09; 1440x900; pass 2, review only",
 "exercised": ["case_01 paste to clipboard by keyboard (1 paste, 1 click, 18 keys, 10.2 s scripted, 9 of 9 decided individually)", "lib09 load to clipboard (3 clicks, 24 keys, 15.2 s scripted, 19 of 19 decided individually, Ready to export first try)", "j/k walk across panels on lib09 (28 presses)", "Shift+A confirm dialog and mouse batch click", "gap flag before and after date confirm", "unclear tray, charges and flags geometry and screenshots", "Edit by keyboard with original shown, reload mid-review, early export, stepper expanded", "o then a with the record dialog open", "export letter and notes text for both cases, clipboard length check", "read review.js lines 60-131 and 285-331"],
 "verdict": "pass",
 "scores": {"verify_quickly": 4, "keyboard_flow": 4, "handoff_clarity": 4, "information_density": 3, "export_fit": 4, "trust_cues": 4},
 "findings": [
  {"severity": "minor", "title": "Letter prints a summary line plus a Source line per entry and an 'AI translation:' prefix", "evidence": "artifacts/review-evidence/T-060-pass2/task2-export-letter.txt (April 14, May 3, May 20 entries start 'AI translation:'); task1-export-letter.txt", "why_it_matters": "Longer text to edit before it goes to an adjuster; a UI-style label would be sent unless I notice it", "fix": "Option for the one-line form per D-002; make the translation note a bracketed removable phrase", "acceptance_test": "A letter option gives one line per entry; no line in the default letter starts with 'AI translation:'"},
  {"severity": "minor", "title": "Prior-condition flag still raised on an interpreter sentence", "evidence": "artifacts/review-evidence/T-060-pass2/12c-flags.png ('Hx obtained via patient's son, who interpreted.'); task2-export-notes.txt FLAGS DISMISSED", "why_it_matters": "Noise in the adjuster-facing flag list; I dismiss it every time", "fix": "Backend: no prior-condition flag on 'Hx obtained via ...'", "acceptance_test": "lib09 raises no prior-condition flag"},
  {"severity": "minor", "title": "Charges and unclear rows still 133 px each; unclear tray 870 px", "evidence": "artifacts/review-evidence/T-060-pass2/12-unclear-tray.png; q9-lib09-full.py output 'unclear tray h 870', 'charge row heights ... 133'", "why_it_matters": "Reconciling charges is slower than it should be; pass-1 target was under 700 px", "fix": "One 56 px row: amount, provider and date, snippet, status, one button; secondary links in a menu", "acceptance_test": "lib09 unclear tray height under 700 px"},
  {"severity": "minor", "title": "Timeline rows are about 3.5 per screen; accepted rows keep a blue enabled Accept", "evidence": "artifacts/review-evidence/T-060-pass2/04-all-decided.png; q5-density-shiftA.py row heights [252,208,...]; q13-geom.py 'btn btn--primary rv-accept disabled=false' on an accepted row", "why_it_matters": "A 7-row case needs two screens and an accepted row looks undecided", "fix": "Quiet 'Accepted' state with Reset, one-line quote, fewer visible controls", "acceptance_test": "After accept the row has no btn--primary and is under 110 px; 6 rows fit in 900 px"},
  {"severity": "minor", "title": "'Verified' chip and the mouse batch button; Shift+A asks but the button does not", "evidence": "artifacts/review-evidence/T-060-pass2/05b-shiftA.png; q13-geom.py output 'dialog after batch click: None' and 'progress after: 7 of 10 decided'", "why_it_matters": "Verified reads as human-checked; one mouse click accepts 7 unopened rows", "fix": "Chip 'Quote matches record'; same confirm for the button", "acceptance_test": "No chip reads 'Verified'; clicking Accept all asks with the count"},
  {"severity": "minor", "title": "Export: letter in a 416 px scroll box, no download, early-export message repeats", "evidence": "artifacts/review-evidence/T-060-pass2/04b-export.png; q4-task1.py 'letter box rect [4318.5, 416, 984]'; 20-early-export.png; q13-geom.py 'download controls: []'", "why_it_matters": "The last step of the demand workflow is still copy-only and scroll-in-scroll", "fix": "Box sized to its text; .txt and .docx download; one sentence per message", "acceptance_test": "Letter box height equals scrollHeight; a download control exists"},
  {"severity": "minor", "title": "o opens a dialog that swallows the next key without a message", "evidence": "q10-jk-o-edit.py output 'dialog open after o: True', e2 still pending after a; app/frontend/review.js:310", "why_it_matters": "A keyboard reader loses a keystroke and does not know why", "fix": "o focuses the source pane, or say 'Close the record first (Esc)'", "acceptance_test": "o then a accepts or shows a message"},
  {"severity": "minor", "title": "Mixed currency and date formats", "evidence": "artifacts/review-evidence/T-060-pass2/12b-charges.png ('$2,940' rows, '$650.00' rows, 'Accepted charges: $5,090'); 12c-flags.png (long dates) vs 04-all-decided.png (ISO dates)", "why_it_matters": "Looks unfinished and slows reconciliation against the letter", "fix": "Always cents; US long dates in the UI", "acceptance_test": "No dollar amount without cents in the charges panel"},
  {"severity": "minor", "title": "Keyboard entry after a library load lands at the page bottom; j is ignored on a radio; 'Start review' has no control", "evidence": "q8-lib09-walk.py 'first Tab after load -> SUMMARY ... y=7348'; q10-jk-o-edit.py j-walk stuck on e4; app/frontend/app.js:48; review.js:295", "why_it_matters": "After loading a case the first keystroke sends the view away from the work", "fix": "Focus the Open decisions heading after a load; name the skip link 'Start review'; j from a radio moves to the next row", "acceptance_test": "After a library load one Tab lands on the first button of Open decisions"},
  {"severity": "minor", "title": "Needs-review entry e2 is visited after the flags and charges", "evidence": "q8-lib09-walk.py log 'a on a7 (needs_review) -> ARTICLE entry-2'; app/frontend/review.js:94-98", "why_it_matters": "The advance order is not the order the page reads", "fix": "Prefer the nearest needs-review entry in the timeline before moving to flags", "acceptance_test": "On lib09 the 3 needs-review entries are visited before the first flag"},
  {"severity": "minor", "title": "Case-check bar contradicts itself at the end; decision step shown with a cross", "evidence": "artifacts/review-evidence/T-060-pass2/12e-ready.png / q8 output 'Case checks | 9/10 checks passed | 1 need you | Ready to export'; 21-stepper-open.png (markers includes a cross on the date step)", "why_it_matters": "I cannot tell whether anything still needs me", "fix": "Plain 'all decided; 1 check not run'; 'your call' icon instead of a cross", "acceptance_test": "With every item decided the bar shows no 'need you' count"},
  {"severity": "nit", "title": "Case list shows 'Untitled case' for every pasted case", "evidence": "q8-lib09-walk.py Tab output (case buttons 'Untitled case ready · 8 reco')", "why_it_matters": "Cannot tell my earlier paste runs apart", "fix": "Show the first record date range or the paste time", "acceptance_test": "Two pasted cases have different labels"}
 ],
 "whats_right": ["One linear queue: j/k/a/d cross panels in page order and the last a lands on Export", "Unclear and rate rows say 'Keep in notes' instead of Accept, and the gap stays 42 days after the intake date is confirmed", "Shift+A asks first with the count; Edit keeps the original and decisions survive a reload"],
 "questions_for_chris": ["Should the mouse 'Accept all verified' button ask the same question as Shift+A?"]}
```
