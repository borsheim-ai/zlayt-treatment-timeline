"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
T-136 round 2: compare-export-note (D-058: a note on an accepted, compared quote-only edit under the AI's summary whose second AI check has no answer: the server's blocker sentence; holds btn-write-summary 'Write the summary', which opens the edit box; NO rerun button), data-blocker-code (the reason code on a gate-blocker row, e.g. JUDGE_NOT_RUN), btn-gate-write-summary (the same action on that item's JUDGE_NOT_RUN gate-blocker row); the row's entry-state chip of a compared edit reads
  'Compared by you' (not 'Needs review') with entry-reasons 'Compared by you with the quote; the second AI check ...'; edited-note of a quote-only edit reads 'Quote changed by you' and shows the original excerpt.
T-142: conflict-empty (the Conflicts group's empty state: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.'), conflict-coverage (details in the Conflicts group: open when empty, collapsed when conflicts are listed; words from GET case `checks`
  {conflict_types, labels, not_checked}, a fixed fallback without it) holding conflict-checked-item, conflict-not-checked-item and, in the fallback only, conflict-coverage-note.
T-149 (multi-case, tests/e2e/test_multicase.py): cases-overview (the home section, local mode only), cases-row (one per case, data-token), cases-open (the link that opens it), cases-title, cases-dates (<time> elements), cases-stage, cases-progress-<kind> (a <progress>, kind = entries | flags | amounts)
  with cases-progress-text-<kind> ('2 of 5'), call-out chips cases-chip-needs-review, cases-chip-edits, cases-chip-tray, cases-chip-blocked ('Export blocked (n)') with cases-blocker-reason (one per distinct reason, first two), cases-chip-ready; cases-filter-all / cases-filter-attention / cases-filter-ready (aria-pressed),
  cases-sort (select: attention, recent, least_done, title), cases-count, cases-empty. Detail: case-overview (first block of the timeline), co-progress-<kind> / co-progress-text-<kind>, co-chip-needs-review / co-chip-edits / co-chip-tray / co-chip-blocked / co-chip-ready, co-blocker-reason,
  co-gate-steps (<details>) with co-gate-toggle (its summary), co-gate-verdict, co-gate-step (one per step of GET trace; data-step-id, data-step-status) holding co-gate-word and co-gate-why; btn-all-cases (header: back to the overview).
  Literal forms used by specs: cases-progress-entries, cases-progress-<seq>, cases-progress-text-entries, cases-progress-text-<seq>, co-progress-entries, co-progress-<seq>, co-progress-text-entries, co-progress-text-<seq> (<seq> = flags | amounts).
T-149 round 2 (tests/e2e/test_multicase.py): the overview block is ONE block: it holds todo-strip and checks-card (case-stepper, judge-panel) in its .co-slot; co-gate-* are gone (the Case checks rail is the one place for the steps). need-review-count is now the block's
  needs-review chip (open items only), co-chip-edits, co-chip-tray (quiet), cases-chip-can-export and co-chip-can-export ('Can export \u2014 N not reviewed (they stay out of the letter)', amber), co-chip-ready ('Everything decided', green, only when nothing is undecided), co-chip-blocked; the same chip ids with the cases- prefix on a row.
  Row: cases-decided ('n of N decided'), cases-next (the one call-out of a not-analyzed or failed row), cases-search (title), cases-list (data-ready="true" after the first settled paint), cases-loading, cases-load-error with cases-retry, cases-open-error, filter cases-filter-ready is now 'Ready to send'.
  Detail: case-heading (the h2, tabindex -1, focused when a case opens from the list, aria-label names the case), do-first with btn-do-first (one line from next_action {item_id, kind, reason}), btn-rename-case, case-rename-input, btn-save-rename, case-rename-error, todo-more (phone: the jump list behind one line),
  data-do-first (attribute on the overview block while the line is shown), LiveRerun and JudgeNotRun (stubs that make GET case say rerun_available true), rerun-unavailable (the sentence that replaces the rerun button when no item says rerun_available), input-title (the case name field beside Analyze).
T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
T-136 r3 (tests/e2e/test_held_quote_gate.py): btn-write-summary-case ('Write the summary' on the case-level places: the 'Ready to export?' and 'Second AI check' steps of the case rail and the 'How the AI was checked' rows; opens the entry's summary box like the blocker row's btn-gate-write-summary). A held re-picked quote offers btn-rerun-judge only until a rerun gave no answer (the blocker's rerun_no_answer).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
  edit-check-hint (a reworded entry that is still marked Needs review: its btn-accept reads 'I compared it with the quote'; the row carries data-edit-check; it counts as open in the header, todo-list ('1 edit to check') and the copy-confirm),
  letter-style (fieldset in the export panel) with letter-style-standard / letter-style-oneline radios (T-121: ?style=oneline), tray-filtered (collapsed <details> 'Filtered by rule (n)', D-057) with tray-filtered-summary,
  tray-filtered-rule (one per rule, data-rule) and tray-filtered-item; data-group = the list a row sits in (flag kind on the flag sections, 'charges' / 'unclear-amounts' on the amount tables): a / d move only inside it.
  T-136: btn-edit-excerpt ('Change quote' on an entry row; opens excerpt-editor), btn-copy-cancel ('Go back' in copy-confirm), edit-compare-prompt (a visible line under the edit-check hint after the a key was pressed on an edit that still waits for her comparison: 'Not recorded yet ...'; a never records it, the btn-accept 'I compared it with the quote' does),
  dismissed-group-flags / dismissed-group-amounts (a <details> at the end of the Flags / Charges panel, 'Dismissed (n)', rows keep Undo; opens for the item just dismissed) with dismissed-summary-flags / dismissed-summary-amounts, dismissed-flags (rows) and dismissed-amounts (table).
  A dismissed flag / amount / entry has NO btn-accept and no btn-edit (state word 'Dismissed' + btn-reset 'Undo'); entry-date is a <time datetime="YYYY-MM-DD"> showing the long date.
T-144: uncovered-summary (a link 'Not in an entry (n)' in an entry row's link bar; aria-expanded), uncovered-list (the list 'Also in this record, not in an entry (n)', hidden until opened; data-record-count), uncovered-heading (its full wording), uncovered-item (one <li> per sentence, data-record-id), uncovered-text (the verbatim sentence, read-only), btn-uncovered-jump ('Show in record': opens the source record with that sentence highlighted). Never in the letter, the notes or the copy text. data-entry-id = the entry id on an entry row (specs find a row by it); data-flag = the flag key (likely_duplicate | likely_total) on charge-flag; T-144's data-record-count is the number of sentences in uncovered-list.
T-172 (D-064, tests/e2e/test_count_charge.py): not-counted-reason (the code's plain sentence 'Not counted: ...' in the Status cell of every amount that is not a charge), btn-count-charge ('Count this charge'; only on a countable row), count-confirm (the confirm <dialog>; Cancel has focus), count-confirm-amount, count-confirm-reason, btn-count-confirm (named: 'I checked this is a separate charge for a service'), btn-count-cancel, count-error (the server's refusal, under the Count button). T-172 r2 (tests/e2e/test_count_duplicate.py, real server, no stub): a countable line whose case view carries count_confirm shows charge-flag in its row before any click; Count this charge opens charge-confirm (flag by name) FIRST, then count-confirm; one POST carries confirm_flag.
  T-154 (tests/e2e/test_charge_confirm.py): charge-flag (the flag name + the server's sentence in a charge row's Status cell), charge-confirm (the confirm <dialog> before a flagged charge is accepted; role dialog, Cancel focused), charge-confirm-flag (the flag's name inside it), charge-confirm-msg (the server's sentence), btn-charge-confirm ('Confirm <flag> and accept'), btn-charge-cancel, batch-charges-note (batch bar: 'Charges are accepted one at a time').
T-162 (tests/e2e/test_rerun_note.py): rerun-note (the server's `rerun_note` sentence on a decided item whose re-run disagreed or failed; in the item's controls and at the top of its 'How this was checked' dialog). T-162 r2: rerun-marker (a span in a collapsed Dismissed group's summary: 'N has a re-run note.' / 'N have re-run notes.'; absent when none).
T-154 r2: trace-charge-flag (inside the 'How this was checked' dialog: the code's flag and whether she has confirmed it; absent when the trace carries its own charge_flag step) and audit-charge-flag (the same line in the item's Audit drawer; the accept event there reads 'accept, confirmed <flag>'). Both carry data-flag and data-confirmed. Also used there, already rendered by audit.js and review.js: btn-audit (the row's Audit button), audit-drawer (the dialog), audit-event (one <li> per decision).
  T-149 r3 (declared with T-166): btn-new-case (primary 'New case' button in the Cases card header; scrolls to and focuses the case-name field), cases-keys (the j / k / Enter hint line under the case list), do-first-item (the item named in 'Do this first' in the case overview), panel-error (the notice a side panel shows when it threw; ZL.panelFailed).
  T-166 (MVP polish): dismiss-ghost (the placeholder a dismissed row leaves in its slot for 6 s, carries data-ghost-for = the item id; contains 'Dismissed: <label>' and btn-undo-dismiss 'Undo'), btn-show-excerpt ('Show full excerpt' directly
  under the quote of a DECIDED row; an undecided row shows its whole quote and the button is hidden), btn-save-accept ('Save and accept' beside btn-save-edit in an entry's edit form), discard-confirm (inline 'Undo will throw away your wording' with
  btn-discard-edit and btn-keep-edit; Keep has focus), btn-more (the 'More' button of a flag card or a charge row; an entry row's is entry-toggle) with panels entry-more-panel, flag-more-panel, charge-more-panel holding Why this status, Audit,
  Change quote and Dismiss with reason; calibration-tech (a Technical detail toggle holding the evals report's own sentence; the visible counts read 'In testing on 10 synthetic cases, 84 of 85 verified items matched the record.'), charge-quote (the sentence of the record that holds the amount, never clipped). #progress-text is short ('4 of 23 decided \u00b7 3 to review'; data-edits and data-needs carry the counts, its title is the full sentence).
  Keys: n = first open item, x = Export (both only while an item row has focus). Visible controls per undecided row or card: at most five (Accept, Edit or Edit note, Dismiss, Open record, More).
  T-174 (MVP finish, tests/e2e/test_mvp_finish.py): section-nav (a sticky bar under the case header with nav-overview, nav-timeline, nav-flags, nav-charges, nav-export; each shows what is still open in its section and the current one carries aria-current=location), btn-back-to-review (the first control in the Export view; closes Export and returns focus to the row she left), btn-error-action (the one action button inside an input error box `error`: Try again, Use the sample case, Edit the text, Choose a .txt file), charge-detail (the code's detail of a not-counted amount, inside the row's More panel). The skip link and n go to case.next_action.item_id: the case overview box carries it as data-do-first-item (the item named in do-first-item). cases-status-error and cases-status-retry (T-175 r2: the message and the Try again button on a case-list row with status_error; no counts, bar or Can export on it), case-switcher (the 'Add a synthetic case' card under the case list; shown on the overview only).
  T-174 r2 (refused paste and counted line, tests/e2e/test_mvp_finish.py): btn-error-library ('Choose a library case' in the input error box for a paste the demo does not run), error-live-note (the one line on how to run live locally, ENABLE_LIVE=1), library-list (the 'Add a synthetic case' group's list of library cases), counted-by-you (the single 'Counted by you' line on a charge she confirmed with Count this charge).
  T-177 (D-065, honest demo provenance): tag-prepared ('Prepared answer' tag on an entry whose summary is a hand-checked demo answer; never 'AI draft'), tag-ai-draft (the 'draft' tag with the AI glyph on a recorded or live answer), audit-prepared (chip on an Audit call row for a prepared answer). T-177 r2: audit-call (one Audit drawer call row), why-ladder and why-generator (the Recorded ladder list in the Why dialog and its 'Drafted by' / 'Prepared by' value). The #badge text says whose answers the demo replays.
  T-045 (tests/e2e/test_journey_modes.py, test_adversarial_ui.py, test_letter_matrix.py, test_two_cases_side_by_side.py): no new test ids.
  T-204 r3 (guided shell and step 1, tests/e2e/test_prepared_first_paint.py): brand (the header's product-name link to home), footer-note (the one footer sentence: neutral until /api/health answers, then the demo's provenance line), demo-badge (the header pill with the demo's provenance label; absent until health answers), btn-draft (step 1's 'Draft the timeline' button), draft-done (step 1's 'Records added' panel shown when the draft finishes).
"""
import json, os, urllib.request, urllib.error
import pytest

SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
import sys
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)                 # tray_entry_for_record imports the app's own placeholder builder
_PRIVATE = {}


def pytest_configure(config):
    """T-136 r2 (staff review F1): a plain `pytest tests/e2e` must RUN the specs that write to the server's SQLite file (ZLAYT_DB: test_edit_to_check, test_code_check_refusal, test_change_the_quote,
    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
    global BASE, SERVER
    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
        return
    import atexit, shutil, socket, subprocess, sys, tempfile, time
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"

    def fail(why):
        """T-136 r3 (staff review r2 major 2): a private server that does not start must stop the run with its own log, never fall through to whatever answers on :7860 (the shared app, with its data)."""
        if proc.poll() is None:
            proc.kill()
        log.close()
        try:
            tail = open(os.path.join(tmp, "server.log")).read()[-2000:]
        except OSError:
            tail = ""
        pytest.exit(f"e2e: the private test server {why} (port {port}). Nothing was run, and nothing was sent to :7860.\n--- server.log (tail) ---\n{tail}", returncode=2)

    for _ in range(80):
        try:
            urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
        except Exception:
            if proc.poll() is not None:
                fail(f"exited with code {proc.returncode} before it answered")
            time.sleep(0.5)
    else:
        fail("did not answer /api/health within 40 seconds")
    if proc.poll() is not None:
        fail(f"exited with code {proc.returncode} right after it answered")
    _PRIVATE.update(proc=proc, tmp=tmp)
    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; SERVER = base; BASE = base + "/classic"
    def stop():
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close(); shutil.rmtree(tmp, ignore_errors=True)
    atexit.register(stop)


def needs_db():
    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
    one fails instead of skipping, so a run can say '0 skipped'."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
        if os.environ.get("E2E_REQUIRE_DB") == "1":
            pytest.fail(msg)
        pytest.skip(msg)
    return path

def _up():
    try:
        urllib.request.urlopen(SERVER + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {SERVER} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(SERVER + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

def tray_entry_for_record(tok, record_id):
    """T-173 (T-168): put one record's entry into the could-not-verify tray the way the pipeline does when the extract step has no answer for it (FIXTURE_MISS). T-168 recorded lib01
    record 3's extract answer, so no library case has an entry tray item any more; the specs that need one overwrite that entry's stored row (needs_db, like the T-136 store writes)
    with the pipeline's own placeholder: generator.failure_entry(record, group, 'FIXTURE_MISS') (no summary, no quote, ladder.failure set, no generator or judge), written through
    pipeline._row, the same row builder the pipeline persists with, and the ladder's backend name kept. The tray is then read from the real backend view and DOM. Returns the item id."""
    import time
    path = needs_db()
    c = api("GET", f"/api/cases/{tok}")[1]
    e = next((x for x in c["entries"] if x["record_ids"] == [record_id]), None)
    if e is None:
        pytest.fail(f"tray_entry_for_record: case {tok} has no entry for record {record_id}; entries: {[x['record_ids'] for x in c['entries']]}")
    from app.db import db as DB
    from app.backend import generator, pipeline as PL, store
    conn = DB.connect(path)
    try:
        case = DB.get_case(conn, tok)
        recs = store.load_records(conn, tok, case["raw_text"])
        rec = next(r for r in recs if f"r{r['n']}" == record_id)
        f = generator.failure_entry(rec, [rec["n"]], "FIXTURE_MISS")
        assert f["id"] == e["id"], (f["id"], e["id"])
        old = DB.get_item(conn, e["id"], tok)
        f["ladder"]["backend"] = (old.get("ladder") or {}).get("backend")      # the pipeline stamps P.backend_name() on every item it stores
        DB.update_item(conn, e["id"], now=time.time(), case=tok, **PL._row("entry", PL._clean(f)))
    finally:
        conn.close()
    t = next((x for x in api("GET", f"/api/cases/{tok}")[1]["tray"] if x["id"] == e["id"]), None)       # what the paralegal gets: a placeholder, no attempt to show
    assert t and t["kind"] == "entry" and t["reasons"] == ["FIXTURE_MISS"] and t["attempt"] == {"summary": None, "excerpt": None}, t
    return e["id"]

@pytest.fixture
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)

def reveal(loc):
    """T-166 F11: Why this status, Change quote and Audit wait behind a row's More button. Opens it when the control is hidden, and returns the control."""
    if not loc.first.is_visible():
        loc.first.locator("xpath=ancestor::*[@data-item-id][1]").locator("[data-testid=entry-toggle], [data-testid=btn-more]").first.click()
    return loc




class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."

    def __init__(self, page, token, ids):
        self.page, self.token, self.ids = page, token, list(ids)
        self.base = {i: self._summary(i) for i in self.ids}
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
            page.route(self._re.compile(pat), fn)

    def _summary(self, i):
        c = api("GET", f"/api/cases/{self.token}")[1]
        e = next((x for x in c["entries"] + c["undated_entries"] if x["id"] == i), None)
        return e and (e["summary"], e["review_status"])

    def active(self):
        return [i for i in self.ids if (cur := self._summary(i)) and cur[1] in ("accepted", "edited") and cur[0] == self.base[i][0]]

    def _na(self, i):
        return {"code": "EDIT_SUMMARY", "text": self.FIX, "target": {"item_id": i}}

    def blockers(self):
        return [{"item_id": i, "kind": "entry", "reason_code": "SUMMARY_DROPS_QUALIFIER", "step_id": "summary_qualifier", "failed_steps": ["summary_qualifier"], "why": self.WHY, "next_action": self._na(i)} for i in self.active()]

    def _case_trace(self, route):
        d = route.fetch().json(); act = self.blockers()
        if act:
            g = next(x for x in d["steps"] if x["id"] == "export_gate")
            g["blockers"] = [b for b in g["blockers"] if b["reason_code"] != "NOTHING_ACCEPTED"] + act
            g.update(status="fail", ready=False, reason_code="SUMMARY_DROPS_QUALIFIER", why=self.WHY, next_action=act[0]["next_action"])
            g["counts"].update(blocking=len(g["blockers"]), code_check_failed=len(act))
            d["verdict"] = {"code": "needs_attention", "label": f"{len(act)} summar{'ies fail' if len(act) != 1 else 'y fails'} a check"}   # the backend's wording (T-098 r2)
        route.fulfill(json=d)

    def _item_trace(self, route):
        d = route.fetch().json()
        if d["item_id"] in self.active():
            for st in d["steps"]:
                if st["id"] == "summary_qualifier":
                    st.update(status="fail", blocks_export=True, why=st["why"] if st["status"] == "fail" else "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
                              reason_code="SUMMARY_DROPS_QUALIFIER", next_action=self._na(d["item_id"]))
            d["verdict"] = {"code": "needs_attention", "label": "Needs your attention: a check on your wording fails", "blocks_export": True}
            d["next_action"] = self._na(d["item_id"])
        route.fulfill(json=d)

    def _export(self, route):
        act = self.blockers()
        if not act:
            return route.continue_()
        route.fulfill(status=422, json={"error": {"code": "export_blocked", "message": act[0]["why"] + " The export is blocked.", "detail": {"blockers": act}}})


class LiveRerun:
    """T-157: item.rerun_available is false on every item with the fixture backend (no live model can answer), so the page offers no rerun. This stub plays a live backend for specs that
    press the rerun: GET .../cases/<token> says rerun_available true on every item until a POST .../rejudge has gone through; after it the server would say false (the rerun got no answer)
    and so does the stub. Registered after another stub, it wins (route.fetch() goes to the server, not through the other routes)."""
    import re as _re

    def __init__(self, page):
        self.answered = False
        page.route(self._re.compile(r"/api/cases/[^/?]+$"), self._case)
        page.route(self._re.compile(r"/api/cases/[^/]+/rejudge$"), self._rejudge)

    def _case(self, route):
        if route.request.method != "GET":
            return route.continue_()
        d = route.fetch().json()
        for k in ("entries", "undated_entries", "flags", "amounts"):
            for i in d.get(k) or []:
                i["rerun_available"] = not self.answered
        route.fulfill(json=d)

    def _rejudge(self, route):
        r = route.fetch(); self.answered = True
        route.fulfill(response=r)


class JudgeNotRun:
    """Route-rewriting stub that puts accepted items into the D-044 state 'the second AI check never ran' (the fixture backend cannot produce it for a recorded case).
    It rewrites GET .../trace, .../items/<id>/trace, .../judges and .../export, and answers POST .../rejudge. The items it hits are the ids that are accepted or edited in
    the real case right now (so dismissing one removes it, like the real gate). hold=True keeps the rejudge request open until release() so a test can see the busy state.
    mode 'clears': the rejudge answers for every item and the stub stops rewriting; mode 'still': nothing answers.
    exempt=[ids] (T-097, D-045 b): items the paralegal edited. /judges lists them as unresolved ('unavailable') but the gate does NOT list them as blockers, so a panel that
    follows the gate must call them 'Edited by you, not AI-checked' and offer no rerun for them."""
    import re as _re
    WHY = "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it."

    def __init__(self, page, token, ids, mode="clears", hold=False, exempt=()):
        self.page, self.token, self.ids, self.mode, self.hold = page, token, list(ids), mode, hold
        self.exempt = list(exempt)
        self.cleared = False; self.posts = 0; self._held = None
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/judges$", self._judges),
                        (r"/api/cases/[^/]+/export$", self._export), (r"/api/cases/[^/]+/rejudge$", self._rejudge), (r"/api/cases/[^/]+$", self._case)):
            page.route(self._re.compile(pat), fn)

    def active(self):
        if self.cleared:
            return []
        c = api("GET", f"/api/cases/{self.token}")[1]
        if not c or "entries" not in c:
            return []
        st = {e["id"]: e["review_status"] for e in c["entries"] + c["undated_entries"]}
        return [i for i in self.ids if st.get(i) in ("accepted", "edited")]

    def _case(self, route):
        """T-157: the fixture backend says rerun_available false on every item (no live model can answer); this stub plays a live backend, so the rerun offer is drawn."""
        if route.request.method != "GET":
            return route.continue_()
        d = route.fetch().json()
        for k in ("entries", "undated_entries", "flags", "amounts"):
            for i in d.get(k) or []:
                i["rerun_available"] = True
        route.fulfill(json=d)

    def _na(self, i):
        return {"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": i, "judge": "j1"}}

    def _blockers(self):
        return [{"item_id": i, "kind": "entry", "reason_code": "JUDGE_NOT_RUN", "why": self.WHY, "next_action": self._na(i)} for i in self.active()]

    def _case_trace(self, route):
        d = route.fetch().json(); act = self._blockers()
        if act:
            n = len(act); g = next(x for x in d["steps"] if x["id"] == "export_gate"); j = next(x for x in d["steps"] if x["id"] == "judges")
            g["blockers"] = [b for b in g["blockers"] if b["reason_code"] != "NOTHING_ACCEPTED"] + act
            g.update(status="fail", ready=False, reason_code="JUDGE_NOT_RUN", why=f"{n} accepted items have not been double-checked by the second AI check, so the export is blocked. Run the second check again.",
                     next_action={"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"view": "judges"}})
            g["counts"].update(blocking=len(g["blockers"]), judge_not_run=n)
            j.update(status="fail", reason_code="JUDGE_UNAVAILABLE", next_action={"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"view": "judges"}})
            j["counts"]["unavailable"] = n
            d["verdict"] = {"code": "needs_attention", "label": f"{n} accepted items not double-checked"}
        route.fulfill(json=d)

    def _item_trace(self, route):
        d = route.fetch().json()
        if d["item_id"] in self.active():
            for st in d["steps"]:
                if st["id"].startswith("judge_"):
                    st.update(status="skipped", reason_code="JUDGE_UNAVAILABLE", why="The second AI check never gave an answer for this item.", next_action=self._na(d["item_id"]))
        route.fulfill(json=d)

    def _judges(self, route):
        d = route.fetch().json(); act = self.active()
        for i in act:
            d["unresolved"].append({"item_id": i, "kind": "entry", "judge": "j1", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5",
                                    "prompt_version": "judge_faithfulness_v1", "call_id": None, "review_status": "accepted"})
        for i in self.exempt:
            if not self.cleared:
                d["unresolved"].append({"item_id": i, "kind": "entry", "judge": "j1", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5",
                                        "prompt_version": "judge_faithfulness_v1", "call_id": None, "review_status": "edited"})
        d["totals"]["unavailable"] += len(act)
        route.fulfill(json=d)

    def _export(self, route):
        act = self.active()
        if not act:
            return route.continue_()
        route.fulfill(status=422, json={"error": {"code": "judge_not_run", "message": f"{len(act)} accepted items have not had the second AI check, so the export is blocked. Run the second check again.",
                                                  "detail": {"blockers": self._blockers()}}})

    def _rejudge(self, route):
        self.posts += 1
        if self.hold:
            self._held = route; return
        self._answer(route)

    def release(self):
        r, self._held = self._held, None
        self._answer(r)

    def _answer(self, route):
        act = self.active(); self.cleared = self.mode == "clears"
        ok = self.mode == "clears"
        route.fulfill(json={"token": self.token, "asked": len(act),
                            "rejudged": [{"item_id": i, "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "supported", "state": "verified", "state_reasons": []} for i in act] if ok else [],
                            "still_unavailable": [] if ok else [{"item_id": i, "kind": "entry", "judge": "j1", "review_status": "accepted", "verdict": "unavailable"} for i in act],
                            "export_gate": {"ready": ok, "status": "pass" if ok else "fail", "blockers": [] if ok else self._blockers()}})
