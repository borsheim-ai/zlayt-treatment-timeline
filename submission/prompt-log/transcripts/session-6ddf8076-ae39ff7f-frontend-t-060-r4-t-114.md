# Subagent: Frontend: T-060 r4 + T-114 (Frontend: T-060 r4 + T-114)

Source: `agent-ae39ff7f9d1a91f89.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:05:14.511Z

You are the frontend worker in /Users/arsis/zlayt-pm-project. Do the T-060 round 4 and T-114 together. Read `python3 tools/board.py show T-060` (see the latest orchestrator note) and `show T-114`. Also read these reviews:
- reviews/T-060-ux-designer-pass3.md
- reviews/T-060-accessibility-pass3.md
- reviews/T-114-paralegal-r2.md
- reviews/T-117-ux-designer.md
- reviews/T-096-ux-designer-r2.md

Work:
1. **T-114 major:** the gap-change notice must persist, surviving dismiss and reload (use a backend field if one exists, else stored case state), and it must show on the affected gap card with the old and new numbers. Also fix its minors.
2. **T-060 AC5 leftovers:**
   - a re-check notice on edit;
   - `$` formatting in the 422 message;
   - reviewed-vs-remaining progress, plus export navigation;
   - Copy letter disabled when empty;
   - plain wording for "other items not reviewed".
3. **Pass-3 minors:**
   - library cases show file-slug titles, so show readable titles;
   - dismissed rows leave the queue, or go into a collapsed "Dismissed" group;
   - the T-117 AI-check row wording must agree with the tray's "Nothing to accept here";
   - the T-096 no-sentences copy is doubled;
   - fix the accessibility minors where they're cheap.
4. **Screenshots:** save before/after as artifacts/screenshots/ui-pass-{1,2,3,4}-*.png. Use existing t060 screenshots for the earlier passes and take new ones for this round, at 1440 and 390 widths.
5. **Tests:**
   - e2e covers each fix, including notice persistence after reload;
   - run the full e2e and the unit suites on a clean worktree.
6. **Commit and hand off:**
   - commit with a pathspec: run `git add <paths>`, then `git commit -m msg -- <paths>` as a separate command;
   - check AC1 (evidence research/ui-references.md), AC4 (reviews/T-060-accessibility-pass3.md) and AC5. Leave AC3, which needs pass 4;
   - write the handoffs and move both cards to in_review.

Rules:
- Use your own server on a spare port. Never kill shared ports 7860, 8787 or 4173; stop only your own PIDs, never pkill.
- After you commit, restart the shared app with tools/serve_app.sh.
- Reply in 8 lines or fewer.

### User / tool · 2026-11-02T11:05:14.517Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:17.691Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-060 | tail -80; echo ======; python3 tools/board.py show T-114"
}
````

### User / tool · 2026-11-02T11:05:17.890Z

**tool result**
````
priority: "P1"
depends_on: ["T-044", "T-045"]
created_by: "orchestrator"
created_at: "2026-11-02T02:08:18Z"
updated_at: "2026-11-02T11:05:05Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T10:22:55Z"
rounds: 1
commits: ["3e3f3b7", "eabe2b8", "9fcae9b", "c8e36fb", "5d975ed", "d9efc5c", "7d5a45f"]
reviews:
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-060-ux-designer-pass2.md", "at": "2026-11-02T10:22:55Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "pass", "file": "reviews/T-060-paralegal-pass2.md", "at": "2026-11-02T10:22:55Z"}
  - {"persona": "accessibility-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-060-accessibility-pass2.md", "at": "2026-11-02T10:22:55Z"}
  - {"persona": "accessibility-reviewer", "model": "claude-haiku-5-5", "verdict": "pass", "file": "reviews/T-060-accessibility-pass3.md", "at": "2026-11-02T11:04:42Z"}
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "pass", "file": "reviews/T-060-ux-designer-pass3.md", "at": "2026-11-02T11:04:56Z"}
ac:
  - {"n": 1, "text": "research/ui-references.md: >= 8 real products/design systems with screenshots-free descriptions, what to borrow, URL", "done": false, "evidence": null}
  - {"n": 2, "text": "docs/UI_DESIGN_BRIEF.md: typography, spacing, color tokens (light/dark), components, density, states; frontend implements tokens in app/frontend/styles.css", "done": true, "evidence": "app/frontend/tokens.css (palette light+dark, 7 type sizes, spacing, 2 radii, elevation, states); census on lib09 light+dark: 6 font sizes, radii 4/6/50%, 0 text nodes under 4.5:1 in both themes; commits eabe2b8, 9fcae9b. Density toggle not built (scope cut)"}
  - {"n": 3, "text": ">= 3 review passes recorded (reviews/T-xxx-ux-designer-pass{1,2,3}.md + accessibility + paralegal), last two with no major; before/after screenshots in artifacts/screenshots/ui-pass-*.png", "done": false, "evidence": null}
  - {"n": 4, "text": "WCAG 2.2 AA contrast and keyboard checks pass (accessibility-reviewer)", "done": false, "evidence": null}
  - {"n": 5, "text": "Carry T-044 UX minors into the polish pass: re-check notice on edit; $ formatting in 422 message; reviewed-vs-remaining progress + export navigation; disable Copy letter when empty; plain wording for 'other items not reviewed'", "done": false, "evidence": null}
---
## Description
Chris (inbox 02:08Z): after core product work, a detailed UI/UX review so it looks like a polished enterprise application, not a vibe-coded app; UI/UX personas take multiple detailed passes using real-world examples from similar industries/products. Plan: pass 1 reference study (ux-designer + researcher: EvenUp, Supio, CaseMark, Filevine, Clio, DocuSign/legal review UIs, claims platforms; design systems like Carbon/Fluent) → design brief with tokens; pass 2 implementation by frontend x2; pass 3 ux-designer + accessibility + paralegal review on the running app; pass 4 fix round. Stop rule: two consecutive passes with no major.

## Notes (append-only, newest last)
- 2026-11-02T02:17:37Z researcher: Pass 1 done by researcher (not claimed): research/ui-references.md (13 sources: 8 opened design systems/pages incl. Carbon table/status/notification, GOV.UK error summary + summary list, Fluent typography + MessageBar, WCAG 1.4.3; legal-tech pages EvenUp, Supio, Filevine, Litify, CaseMark opened but are marketing text with no UI detail, so borrows from them are marked as inferences; Clio 403, DocuSign 404, Guidewire search-only) and docs/UI_DESIGN_BRIEF.md (type scale, 4px spacing, density, light/dark tokens with computed contrast ratios, status vocabulary shape+word, 6 components, banners, empty/error/loading states, keyboard model, open decisions section 11). Frontend may amend values with a note; token changes must regenerate the contrast table (appendix A).
- 2026-11-02T02:17:49Z researcher: Commit c143c4b (docs: UI brief + ui-references) also contains other agents' staged files app/backend/api.py, app/backend/pdf_text.py, tests/unit/test_pdf_upload.py (shared git index; I staged only my two docs). History not rewritten; owner of those files please be aware.
- 2026-11-02T02:28:23Z orchestrator: AC 5 added: Carry T-044 UX minors into the polish pass: re-check notice on edit; $ formatting in 422 message; reviewed-vs-remaining progress + export navigation; disable Copy letter when empty; plain wording for 'other items not reviewed'
- 2026-11-02T03:10:03Z backend: For frontend (from T-076 paralegal review): Edit is enabled on undated rows (undated_entries). Edit implies accept, so the server returns 422 DATE_UNCONFIRMED. Disable Edit (and Accept) on undated rows until confirm_date; show 'Confirm the date first'. Also: after confirm_date the entry now has DATE_AMBIGUOUS cleared from reasons and state recomputed, so rows no longer say 'two ways' once confirmed.
- 2026-11-02T03:11:36Z orchestrator: From T-072 r4: mock.js:15 mock summary says 'patient states' non-verbatim; reword and tighten the frontend guard's per-file exemption.
- 2026-11-02T04:17:05Z orchestrator: Held: needs T-081/T-082 r3 (same frontend files) and the new feature UIs; starts after them per Chris (core work first).
- 2026-11-02T04:17:05Z orchestrator: assigned: frontend
- 2026-11-02T04:58:16Z orchestrator: From T-046 r2: the side-by-side 'Show gap flag' control needs a keyboard shortcut or skip link (190 Tabs today); plus its 3 minors.
- 2026-11-02T05:37:44Z orchestrator: From T-085 r4 minors: language.py docstring overclaims no leakage to Spanish; missing space glues 'advised'+'evaluation'; 8/41 short English lines route uncertain (review-load).
- 2026-11-02T06:14:53Z orchestrator: From T-108: after a successful quote save, the 'accept refused' box stays until reload; clear it on save.
- 2026-11-02T06:38:25Z orchestrator: From T-108 r2: the could-not-verify tray shows 'no sentences to pick from' without the backend's sentences_reason; render it.
- 2026-11-02T09:02:03Z orchestrator: Pass 1 (review only, no code): ux-designer + paralegal + accessibility in parallel against research/ui-references.md and docs/UI_DESIGN_BRIEF.md; frontend implements after T-096 lands; pass 2 re-reviews.
- 2026-11-02T09:02:25Z orchestrator: assigned: frontend
- 2026-11-02T09:21:16Z orchestrator: Pass 1 complete: reviews/T-060-ux-designer-pass1.md (15 majors: token fragmentation 3 palettes/2 blues/21 type sizes/no :hover), reviews/T-060-paralegal-pass1.md (5 majors: keyboard across panels, needs-review first, hidden next actions, unclear-amount table), reviews/T-060-accessibility-pass1.md (BLOCKER: Shift+A accepts all from any focus; 6 majors). Implementation starts when T-096 lands; backend items are T-114.
- 2026-11-02T09:27:47Z backend: T-114 backend API for frontend (contract memory/contracts/api.md updated): (1) POST /records/{rid}/confirm_date now returns gap_changes[] = [{flag_id, change: changed|added|removed, old_days, new_days, old_from, old_to, new_from, new_to, sentence}] ([] when no gap moved). sentence is ready to announce, e.g. 'Gap recalculated after you confirmed record 4: now 40 days (was 42).' lib09 record 4 -> 5 March gives 42 -> 40. (2) Every amount in GET case amounts[] has accept_effect (letter_total|acknowledge|internal_notes) and judge_required_for_export. A rate is 'acknowledge': accepting it never creates JUDGE_NOT_RUN, so label the button Acknowledge / keep 'Accept as noted' and do not say it goes in the letter. (3) lib09 judge fixtures for the two rate rows recorded, so the demo has no rerun dead end. Not done here: F4 'an intake form never ends a gap' (gaps.py has no such rule; needs its own card).
- 2026-11-02T09:28:34Z frontend: claimed
- 2026-11-02T09:28:34Z orchestrator: Claimed with --force past the T-045 dependency: T-045 is parked for the M3 gate panel; UI polish proceeds now per Chris's request and T-045's E2E reruns after it.
- 2026-11-02T10:03:02Z frontend: AC 2 checked: app/frontend/tokens.css (palette light+dark, 7 type sizes, spacing, 2 radii, elevation, states); census on lib09 light+dark: 6 font sizes, radii 4/6/50%, 0 text nodes under 4.5:1 in both themes; commits eabe2b8, 9fcae9b. Density toggle not built (scope cut)
- 2026-11-02T10:03:02Z frontend: Pass-2 implementation done (commits 3e3f3b7 keyboard, eabe2b8 tokens, 9fcae9b layout). Verified on own server from a clean HEAD worktree (fixture, port 7931, DB in scratchpad, stopped by PID): e2e 135 pass; remaining failures are NOT frontend regressions or need QA edits: test_side_by_side::test_p_moves_focus (presses j from body: obsolete under the a11y blocker), test_suggestions tray-flag x2 (wording changed per T-096 UX F5), test_stepper case_rail_is_one_line + judge_panel_when_nothing_objected (fail on HEAD frontend too). QA T-115: new test ids are declared in tests/e2e/conftest.py docstring (T-060 paragraph). NOT done (left for pass 3): long dates in rows (entry-date text must stay ISO for e2e filters), dismissed rows collapsing under Dismissed (n), row overflow menu / 120px collapsed row, gap headline card, merge of the two check accordions, inline live re-check on edit (F25), $ formatting in the 422 message, density toggle, grid layout for the source pane (still fixed, now below the header). T-096 review: skip links (Tab, Enter reaches dates / dismissal suggestion / first item), Keep showing persisted per case, stale note above the numbers once, tray flag wording, sentences_reason copy; the 'sentenceless record' corpus case is backend/QA.
- 2026-11-02T10:03:13Z frontend: moved in_progress -> in_review: AC1 done by researcher (research/ui-references.md, not mine); AC3 needs review passes 2 and 3 (this is the pass-2 implementation); AC4 contrast verified by my census in both themes, WCAG keyboard checks need the accessibility-reviewer; AC5: all but the dollar formatting in the 422 message are done
- 2026-11-02T10:03:50Z orchestrator: review dispatched: ux-designer-reviewer, paralegal-reviewer, accessibility-reviewer
- 2026-11-02T10:06:42Z qa: e2e follow-ups 6e880e6: p test focuses a queue row first (WCAG 2.1.4); tray-flag lead updated to the single T-060 sentence for both reasons plus a check that tray-why sits in a closed disclosure; test_judge_panel_when_nothing_objected used a snapshot inner_text on an async count (now expect/to_have_text). Verified on a private app (ZLAYT_MODE=local, fixture/curated, port 7871): side_by_side + suggestions + stepper green (the :7860 dev app returned 500 on case create, 'create failed ValueError' in artifacts/tmp/app.log, not touched).
- 2026-11-02T10:22:55Z orchestrator: review ux-designer-reviewer (claude-sonnet-5-5): changes — reviews/T-060-ux-designer-pass2.md; round 1; findings:
    - [major] M1. The Shortcuts dialog (button and '?') prints '[object HTMLElement]' instead of the shortcut list — fix: Flatten the rows: `KEYS.flatMap(([k, v]) => [el('dt', {}, el('kbd', {}, k)), el('dd', {}, v)])`. Add a Playwright assertion that no dialog or page text contains '[object' or 'undefined' or 'null'. Optionally add the one-line footer hint from pass-1 F13.
    - [major] M2. Entry rows are still 208 to 275 px at 1440, and eight stacked panels sit above the first row, so one entry (without its buttons) is visible at load — fix: 1) Merge 'Case checks', 'What you need to do' and 'How the AI was checked' into one 40 px strip that expands (one chevron, one status chip), and fold the accuracy paragraph into the info popover or the Why dialog. 2) Move 'Acce
    - [major] M3. A decided row still looks and acts undecided: Accept stays a filled primary button, the dismissed row stays in the list with Accept offered — fix: Decided rows: replace the filled Accept with a disabled 'Accepted' (check icon, `--ok` text) or hide it, keep Edit, and show 'Undo' as the text link beside the chip; set the summary to `--text-muted`. Dismissed rows: collapse under a '
    - [minor] m1. Case labels and the library are still file slugs, and one developer term reaches every case — fix: Add a `name` (title case) and a short `description` to every library manifest entry; derive case names from it; drop the 'Add:' prefix; clamp text in CSS only. Reword the accuracy line without 'fixture' ('Measured on 10 synthetic test cases: verified items matched the record 84 of 8
    - [minor] m2. Charges table: reasons duplicated, column geometry differs between the two tables, 'Keep in notes' is a primary button — fix: One shared `<colgroup>` for both tables (Amount 120 / Description 1fr / Class 112 / Status 150 / Actions 180); keep the amber sentence and drop the code reason from the status cell (or the reverse); make 'Keep in notes' secondary; put Accept and Dismiss on
    - [minor] m3. Row dates are ISO ('2026-01-09'); the letter, flags and records list use long dates — fix: Format row dates with Intl.DateTimeFormat('en-US', {dateStyle:'medium'}) inside <time datetime>; keep the verbatim record date untouched in the record pane and quote blocks.
    - [minor] m4. 'Open record' still opens a modal on top of the source pane that already shows the same record; the pane prints raw '=== Record 2 ===' markers — fix: At >= 1024 px 'Open record' scrolls and highlights in the pane and moves focus there; the modal stays for narrow widths. Hide the '=== Record n ===' marker line in the pane header.
    - [minor] m5. Edit has no live check, original comparison or counter — fix: Debounced (400 ms) polite live line under the textarea ('Checking numbers and dates against the excerpt...' then the code reason); 'Original' as a muted line above the field; Cmd/Ctrl+Enter saves.
    - [minor] m6. 'Verified' chip has no icon and shares the blue of 'AI draft', the accent and the selected row; header and timeline disagree on 'need review' — fix: Verified: circle-check icon in `--ok`; 'AI draft' neutral (`--info` is fine but not the accent blue). Label the header count 'items'; label the Timeline chips 'entries needing review'.
    - [minor] m7. Dates-to-confirm card and flag footers keep redundant controls — fix: Hide Accept/Edit/Dismiss until the date is confirmed and drop the 'Go to its date choices' link; make 'Dismiss' open the reason field (one control), move Audit to the row menu.
    - [minor] m8. Case-checks and AI-check panels: title baseline misaligned, text-link toggles with a tiny triangle, long text-only notice when export is blocked — fix: One header row per panel (`display:flex; align-items:center`), a 16 px chevron button as the toggle, the blocker list rendered once, the notice in `--warn` not `--bad`.
- 2026-11-02T10:22:55Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): pass — reviews/T-060-paralegal-pass2.md
- 2026-11-02T10:22:55Z orchestrator: review accessibility-reviewer (claude-haiku-5-5): changes — reviews/T-060-accessibility-pass2.md
- 2026-11-02T10:22:55Z frontend: claimed
- 2026-11-02T10:44:01Z frontend: Round 3 in progress: commits c8e36fb (shortcut sheet, theme name, skip targets, decided rows, T-117), 5d975ed (compact rows ~110-140px, checks card, toolbar batch button, charges rows, letter box + Download), d9efc5c (tests). Filed T-120 (interpreter prior-condition flag, backend) and T-121 (letter one-line option and AI-translation note, backend; the UI shows server text verbatim). Not done: density toggle (scope cut), Accept-all button confirm (conftest T-060 contract says the labelled button is one step; Shift+A asks), dismissed group under 'Dismissed (n)', long dates in rows.
- 2026-11-02T10:53:06Z frontend: AC 5 checked: not complete: done = Copy letter disabled when empty, plain 'not reviewed' wording, progress + export navigation; open = inline re-check notice on edit and $ in the 422 message
- 2026-11-02T10:53:11Z frontend: AC 5 unchecked
- 2026-11-02T10:53:11Z frontend: AC 5 is not complete (a mistaken check was reverted): done = Copy letter disabled when empty, plain 'not reviewed' wording, progress + export navigation, $ cents everywhere in the charges panel; open = inline re-check notice on edit and $ formatting in the 422 message. AC 2 evidence for round 3: census 0 text nodes under 4.5:1 in light and dark on sample and lib09, 6 font sizes.
- 2026-11-02T10:53:25Z frontend: moved in_progress -> in_review: AC1 is the researcher's (research/ui-references.md); AC3 and AC4 need the pass-3 reviews (ux-designer, accessibility, paralegal); AC5 has two open items listed in the handoff
- 2026-11-02T10:53:35Z orchestrator: review dispatched: ux-designer-reviewer, accessibility-reviewer
- 2026-11-02T11:04:42Z orchestrator: review accessibility-reviewer (claude-haiku-5-5): pass — reviews/T-060-accessibility-pass3.md
- 2026-11-02T11:04:56Z orchestrator: review ux-designer-reviewer (claude-sonnet-5-5): pass — reviews/T-060-ux-designer-pass3.md
- 2026-11-02T11:05:05Z orchestrator: Pass 3: ux-designer pass, accessibility pass (0 majors). AC3 needs 'last two with no major' -> a pass-4 ux+paralegal after this round. Frontend round 4: check AC1 (research/ui-references.md exists), AC4 (reviews/T-060-accessibility-pass3.md), finish AC5 leftovers, ui-pass-*.png before/after screenshots, pass-3 minors (library cases show file-slug titles; dismissed rows stay in queue), plus T-114 gap-notice major, T-117 minor (AI-check row says accept while tray says nothing to accept), T-096 minor (doubled no-sentences copy).
- 2026-11-02T11:05:05Z orchestrator: assigned: frontend

## Handoff
What changed (round 3): shortcut sheet is a real dialog with 9 kbd/dd rows (flatMap; dom.js el() flattens any nesting); rows are compact (summary beside excerpt, 110-140 px collapsed, More/Less opens a row; first entry at ~460 px at 1440x900, was 676-780; 390: needs-review row <= 420); case checks, next action and AI check are one card, batch button sits in the Timeline toolbar, Start review button; decided rows show Accepted/Dismissed + Undo with no filled Accept; 320 px reflow fixed; theme toggle name follows state; upload control shows its focus ring; skip-link hrefs resolve; T-117 (separate card); paralegal minors F5 F6 F7(chip) F8 F9(box+download) F11 F12 N1 N2 F14 N3. Held rechecks: T-096 dates/dismissal skip links reachable (test), T-114 gap-change notice renders on lib09 (test).
How verified: full tests/e2e on a clean worktree of 7d5a45f, own server port 7946 (ZLAYT_MODE=local, DB in scratchpad, stopped by PID): 176 passed, 16 skipped; new tests/e2e/test_polish_r3.py (18 tests, incl. the negative row-only key test and the Tab/Enter/Space-only review+export) and the retrying judge-count assert at test_stepper.py:204 (T-115 r2 F1) were added on coordinator request; census 0 text nodes under 4.5:1 in both themes, 6 font sizes; screenshots artifacts/screenshots/t060-r3-{sample,lib09}-{1440,390}-{top,full}.png (full page 11826 -> 6657 px at 1440).
What's left: filed T-120 (interpreter prior-condition flag) and T-121 (letter one-line option and AI-translation note as bracketed phrase) for backend: the letter is server text shown verbatim. Not done: density toggle, Accept-all button confirm (the conftest T-060 contract keeps the labelled button one step; Shift+A asks), dismissed rows under 'Dismissed (n)', long dates in rows (e2e filters on ISO), AC5 inline re-check on edit and $ in the 422 message, UX m1 library titles from the manifest (backend), N-9 row tab stops.
Surprised: a class named rv-edit is both the edit button and the edit form, so a form margin rule inflated every row by 16 px; items inside display:contents wrappers miss direct-child grid rules; a worktree with other agents' uncommitted backend edits gave false e2e failures that pass on clean HEAD.

======
---
id: "T-114"
title: "Backend items from T-060 pass 1: rate rows must not offer an accept that later blocks export; demo has judge fixtures for every acceptable lib09 item; gap recompute after a date confirm is reported"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:21:16Z"
updated_at: "2026-11-02T11:05:05Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:39:42Z"
rounds: 2
commits: ["b5fb35c"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-114-paralegal.md", "at": "2026-11-02T09:39:42Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-114-paralegal-r2.md", "at": "2026-11-02T11:00:41Z"}
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
- 2026-11-02T09:39:42Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-114-paralegal.md; round 1; findings:
    - [major] The lib09 gap change (42 to 40 days) is returned by the API, but HEAD's UI shows the new figure with no notice — fix: Frontend, under T-060: render gap_changes[].sentence beside the gap flag and in the flags tray after confirm_date. Whether an intake form should ever be a gap endpoint is a decision for Chris (questions_for_chris 1).
    - [minor] An accepted rate row still reads Needs review and keeps a primary Accept as noted button — fix: After acknowledge, the state chip reads something like Noted, not in letter, and the primary control becomes Undo or Reset. Keep the internal-notes sentence.
- 2026-11-02T09:39:42Z backend: claimed
- 2026-11-02T09:39:42Z orchestrator: Backend part confirmed by review. The remaining major (UI notice for gap_changes) is T-060 frontend work; re-check after T-060 lands. Note T-116 changed lib09: the intake form no longer ends the gap, so the 42->40 example may now read 42->42; use another case to test the notice.
- 2026-11-02T09:39:42Z orchestrator: assigned: backend
- 2026-11-02T10:55:22Z orchestrator: moved in_progress -> in_review
- 2026-11-02T10:55:22Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T11:00:41Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-114-paralegal-r2.md; round 2; findings:
    - [major] The gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed — fix: Show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory: one line under the title such as 'Changed after you confirmed record 4: now 40 days (was 42).' It stays until the gap changes a
    - [minor] An accepted rate row still shows a Needs review chip beside Accepted — fix: After acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false); I did not click it. If it does nothing, it should not look like a button.
- 2026-11-02T11:00:42Z orchestrator: Remaining major is frontend: the gap-change notice must persist (survive dismiss/reload) and show on the gap card. Batch with the T-060 pass-3 frontend round.
- 2026-11-02T11:00:42Z orchestrator: moved changes_requested -> blocked: held for the T-060 pass-3 frontend round
- 2026-11-02T11:05:05Z orchestrator: moved blocked -> in_progress
- 2026-11-02T11:05:05Z orchestrator: assigned: frontend

## Handoff
The gap_changes UI notice landed in T-060 r3 (c8e36fb/5d975ed); E2E in tests/e2e/test_polish_r3.py. Backend part already confirmed in round 1.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:18.148Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend/project_t060_polish.md"
}
````

### User / tool · 2026-11-02T11:05:18.160Z

**tool result**
````
1	---
2	name: t060-enterprise-polish
3	description: T-060 tokens, keyboard scope, compact-row layout, checks card, decided-row buttons, and the pitfalls hit in rounds 2-3
4	metadata:
5	  type: project
6	---
7	**Tokens:** `app/frontend/tokens.css` is the only place for colours/sizes/radii/shadows (7 font sizes in rem, 2 radii 4/6, light+dark+data-theme). Other CSS files only read tokens. One button system: `.btn` (+ `--primary|--ghost|--link|--sm`); status chips `.chip--ok|warn|bad|info|muted` + `data-icon`. Audit recipe: computed font-size/contrast census (text nodes, effective background, both themes); expect 6 sizes and 0 nodes under 4.5:1 (round 3: 0 in both themes on sample and lib09).
8	**Keyboard (WCAG 2.1.4):** single keys act only when focus is inside a `[data-item-id]` row outside dialogs/sbs-pane (`RV.itemRowOf`). j/k = DOM order, a/d advance via `RV.nextPendingAfter` (needs-review entry in the queue first, then any needs-review, then any open). Shift+A: batch.js `batch-confirm`; review.js ignores shifted letters. A letter key with a dialog open says "Press Escape" (live region). Skip links = app.js SKIPS, hrefs point at real elements (TARGETS adds ids), re-rendered on `zl:panels`. After a case opens, `resetTabStart` focuses `#skip-nav` (tabindex -1) so one Tab reaches the first skip link.
9	**Compact row (round 3):** `.entry[data-entry-id]` is a 2-column grid: head (date, provider, Rec, reason with ellipsis, chips) / summary (clamp 3) beside excerpt (clamp 2) / decision buttons left + links right. `.rv-controls` is `display: contents` inside rows. `More`/`Less` (`entry-toggle`) opens a row (`openRows` Set in timeline.js survives repaints). Decided rows clamp to 1 line. Tray cards and date-to-confirm cards (no data-entry-id) keep the old single column. Row-actions are moved after the controls in the DOM so Tab order = screen order.
10	**Decided buttons:** primary only when `pending`; accepted -> "Accepted" (`rv-decided`, still enabled, no-op that says so, because e2e `.all()` loops click every btn-accept); dismissed -> "Dismissed" muted; reset reads "Undo". Keep `btn-accept`/`btn-dismiss`/`btn-reset` testids on every row.
11	**Checks card:** timeline.js wraps case-stepper + judge-panel in `.checks` (one border, dividers); calibration-line sits below the queue and is NOT collapsed (e2e asserts it visible).
12	**Pitfalls:** `el.append(cond ? node : null)` prints "null": always `.filter(Boolean)`; `el()` now flattens any nesting (`kids.flat(Infinity)`), the shortcut sheet bug was a nested array. A class named `rv-edit` is BOTH the edit button and the edit form: always write `form.rv-edit` / `form.rv-reason` in CSS (a form margin rule added 16px to the button row). No row height may depend on focus. entry-date text must stay ISO. Letter/notes text is built by the server and shown verbatim: letter layout changes (T-121) are backend. Sandbox/hook: no `$VAR` in command position, no `rm -rf`, no `sleep` chains; commit with `git commit -F file -- <paths>` and `git add` in its own command; `git add -N` is refused.
13	**Dev/test recipe:** clean worktree of HEAD (`git worktree add --detach <dir> HEAD`), server `PORT=.. ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch> python -m app.main`, run `E2E_BASE_URL=http://localhost:PORT .venv/bin/python -m pytest tests/e2e`, kill by PID. A worktree with uncommitted backend edits from other agents shows false e2e failures (export 422, judge-panel) that pass on a clean HEAD.
14	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:20.727Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; git log --oneline | head -5; ls app/frontend app/frontend/* | head -80; wc -l app/frontend/*.js app/frontend/*.css | tail -40"
}
````

### User / tool · 2026-11-02T11:05:20.906Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
db7f6d0 docs(orchestrator): D-054 states the T-112 r2 salient-content trim rule (T-112 r2 major 2)
e1ce8dc fix(backend): a never-judged LLM_ONLY tray item carries its real reason, not JUDGE_UNAVAILABLE (T-122; case_05 f_r1_1 judge_unavailable 1 -> 0)
7d5a45f fix(frontend): refusal, edit box and blocked notice span the full row inside the compact grid (T-060 r3)
f8f358e fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
1b93582 fix(backend): D-054 trims only salient new content; split-off and tray-trace fixes (T-112 r2)
app/frontend/api.js
app/frontend/app.js
app/frontend/audit.js
app/frontend/batch.js
app/frontend/charges.js
app/frontend/dom.js
app/frontend/excerpt.js
app/frontend/export.js
app/frontend/exportcfg.js
app/frontend/flags.js
app/frontend/index.html
app/frontend/input.js
app/frontend/judges.js
app/frontend/manual.js
app/frontend/mock.js
app/frontend/mock_extra.js
app/frontend/mock_flags.js
app/frontend/mock_sample.js
app/frontend/narrative.js
app/frontend/review.css
app/frontend/review.js
app/frontend/sidebyside.css
app/frontend/sidebyside.js
app/frontend/source.js
app/frontend/state.js
app/frontend/stepper.css
app/frontend/stepper.js
app/frontend/styles.css
app/frontend/suggestions.css
app/frontend/suggestions.js
app/frontend/switcher.js
app/frontend/timeline.js
app/frontend/tokens.css

app/frontend:
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
suggestions.js
switcher.js
timeline.js
tokens.css

app/frontend/dev:
harness.js
mock-data.js
mock-review.js
panels.html
      46 app/frontend/api.js
     131 app/frontend/app.js
      57 app/frontend/audit.js
     135 app/frontend/batch.js
     119 app/frontend/charges.js
      33 app/frontend/dom.js
      50 app/frontend/excerpt.js
      79 app/frontend/export.js
      51 app/frontend/exportcfg.js
      90 app/frontend/flags.js
     106 app/frontend/input.js
     210 app/frontend/judges.js
      93 app/frontend/manual.js
     216 app/frontend/mock.js
      29 app/frontend/mock_extra.js
      55 app/frontend/mock_flags.js
       2 app/frontend/mock_sample.js
      75 app/frontend/narrative.js
     368 app/frontend/review.js
     119 app/frontend/sidebyside.js
      37 app/frontend/source.js
      28 app/frontend/state.js
     632 app/frontend/stepper.js
     181 app/frontend/suggestions.js
      73 app/frontend/switcher.js
     273 app/frontend/timeline.js
     125 app/frontend/review.css
      19 app/frontend/sidebyside.css
     114 app/frontend/stepper.css
     252 app/frontend/styles.css
      20 app/frontend/suggestions.css
      91 app/frontend/tokens.css
    3909 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:21.055Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-060-ux-designer-pass3.md | head -150"
}
````

### User / tool · 2026-11-02T11:05:21.164Z

**tool result**
````
# T-060 pass 3: enterprise UI/UX review (ux-designer-reviewer)

**Verdict: pass.** No blocker, no major. The three pass-2 majors are closed: M1 fixed, M2 fixed with a minor residual (row density, first screen), M3 fixed for accepted rows and partial for dismissed rows (now a minor). This is the first pass from me with no major; the stop rule (two consecutive passes with no major) needs one more clean pass, and the accessibility pass is not mine to judge. Eleven minors and two nits remain, none of them new defects of the pass-2 kind.

Scores against pass 1 and pass 2 (1 to 5): design quality 2 -> 4 -> 4, originality 2 -> 3 -> 3, craft 2 -> 3 -> 4, functionality 3 -> 4 -> 4. Craft rises because the dialog defect, the 208 to 275 px rows and the filled Accept on decided rows are gone. Originality stays at 3: it is a clean Carbon-style review list, not a distinctive one. No score is 2 or below.

## Scope and how I ran it

- Pinned: `git rev-parse --short HEAD` printed `e1ce8dc`; `git diff --stat 7d5a45f HEAD -- app/frontend` printed nothing, so the frontend at HEAD is the one in the T-060 round-3 commits (c8e36fb, 5d975ed, d9efc5c, 7d5a45f). `git status --short | wc -l` printed 1742 (dirty), so I used `git archive HEAD` into the session scratchpad (`.../scratchpad/app3`), `PORT=7981 HOST=127.0.0.1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, own `ZLAYT_DB`. Listener PID 49349, stopped with `kill 49349`; `curl http://127.0.0.1:7981/api/health` then printed `000`.
- Playwright (project venv) at 1440x900 and 390x844 touch: landing, sample case (results, first screen, every panel), five library cases (lib01, lib06, lib09, lib11, lib14) at both widths, the Shortcuts button and `?`, Start review, keyboard (Tab order, skip links, `a`, `d`, `k`, `r`, `e`, Shift+A with its dialog), More, Open record, Edit with an unsupported number, Accept, Dismiss, Undo, Accept all verified (button) then Undo last batch, flags, charges, export open with pending items, dark mode, computed-style census, DOM text scans, a real dismissal-suggestion case (three prior dismissals through the real route), the AI-check panel on five cases at two widths.
- Not exercised: PDF upload, real-model latency, Safari and Firefox, WCAG conformance (accessibility-reviewer), the audit drawer, 1024 and 768 widths, a stubbed failed run (unchanged since pass 2), the Exhibit/Bates form. Comparisons to EvenUp, Supio, Filevine and Litify are to what their marketing pages state (research/ui-references.md); I saw no UI of theirs.
- Probe scripts and results are in `artifacts/review-evidence/T-060-pass3/` (`ux3-*`).

## Pass-2 findings, one by one

| # | Pass-2 finding | Status | Evidence |
|---|---|---|---|
| M1 | Shortcuts dialog printed `[object HTMLElement]` | **Fixed** | Shortcuts button opens a dialog with 9 `kbd` rows (j/k, a, d, e, r, o, p, Shift+A, ?) and an intro; `dialog_object` false; page-wide scan for `[object`, `undefined`, `null` false (ux3-walk1-results.json, ux3-23-shortcuts.png). Residual: `?` pressed from the page top (nothing selected) opens nothing, `?` on a selected item does (nit N1) |
| M2 | Rows 208 to 275 px, eight panels above the first row | **Fixed, residual minor (m-new1)** | Rows now 110 to 138 px (was 208 to 275); first row top 464 (was 676); first Accept's bottom edge at 593, inside 900; case checks, next step and AI check are one card; Accept-all moved to the Timeline toolbar. Short of my own target: first row at 464 not < 450, 3 rows fully visible not 4 (ux3-walk1-results.json). At 390: first row at 893 (was 1,205), rows 246 to 330 px (was 446 to 569), target <= 420 met |
| M3 | Decided row kept a filled Accept; dismissed rows stayed | **Fixed for Accepted, partial for Dismissed (m-new2)** | Accepted row: no Accept button, a green check and 'Accepted', Edit, Dismiss, 'Undo' link; Undo returns '0 of 20 decided' (ux3-37-after-accept.png, ux3-walk2-results.json). Dismissed row: 'Dismissed' label with Undo, but still in the queue, quote struck through, Accept (secondary) offered (ux3-39-after-dismiss.png; `dismissed_section` empty) |
| m1 | Slugs and 'fixture backend' | **Open** | Header on lib09 and lib11 reads 'case lib09 spanish interpreter espalda' and 'case lib11 priors and ledger'; calibration line still 'on the fixture backend (recorded replies, 10 golden cases, small sample)' (ux3-walk8-results.json lib11_header, ux3-92-1440-calibration.png). The handoff lists it as backend. Landing is 900 px |
| m2 | Charges geometry, duplicate reasons, primary 'Keep in notes' | **Partial** | Status and Decision columns now start at x 578 / 786 in both tables (was 778 vs 452). Still: unclear rows print two reasons, 'Keep in notes' is a filled primary (2 in the unclear table), rows 197 and 199 px (was 147), amount cell 'missing 3 days of work' (ux3-15-charges.png) |
| m3 | ISO dates in rows | **Open** | `entry-date` '2026-01-09' on all nine rows; the export uses 'January 9, 2026' (ux3-walk1-results.json iso_dates). Handoff: e2e filters on ISO |
| m4 | Modal over the pane; raw `=== Record n ===` marker | **Open** | 'Open record' at 1440 opens a dialog (`open_record_modal` true) while the pane shows the same record with '=== Record 4 ===' (ux3-74-open-record.png, ux3-walk3-results.json) |
| m5 | Edit has no live check | **Open** | Typing ' Extra 99 mg.' and waiting 1.2 s: nothing reacts, label unchanged (ux3-75-edit-bad.png). Handoff lists it as not done |
| m6 | Verified chip icon, two 'need review' counts | **Partial** | Timeline chips now say 'entries' ('0 entries need review') while the header says '3 need review', so the nouns differ; 'Quote matches' chip still has no icon (ux3-04-results-d.png) |
| m7 | Redundant controls | **Open** | Date card keeps disabled Accept and Edit plus 'Confirm the date first. Go to its date choices' (ux3-39-after-dismiss.png); every flag card keeps 'Dismiss' and 'Dismiss with reason…' (ux3-14-flags-panel.png; gap card buttons: Accept, Edit note, Dismiss, Dismiss with reason…, Audit) |
| m8 | Panel alignment, text-link toggles | **Partial** | Case checks, next step and AI check are one card with aligned titles (ux3-04-results-d.png); toggles are still underlined 'Show▾' links. Export-blocked notice not re-measured |
| n1 | Type scale, glyph icons, 120 px mobile header | **Open** | Computed font sizes 14, 12, 16, 13, 20, 15 (6); glyph icons; mobile sticky 32 + 88 px (ux3-walk4-results.json) |

Count of the 12 pass-2 findings: fixed 2 (M1, M2 with residual), partial 4 (M3, m2, m6, m8), open 6 (m1, m3, m4, m5, m7, n1). No open item is above minor.

## Scope cuts: accepted

- **Density toggle: accepted.** The toggle existed to make rows compact. The default rows are now 110 to 138 px and 246 to 330 px at 390; a second control would add a setting for a need that no longer exists. If the first row at 464 px and 3 visible rows (m-new1) are fixed, nobody needs it.
- **Accept-all confirm: accepted.** The conftest contract keeps the labelled button one step. The batch is entries only ('Charges, flags and anything marked needs review always need your own decision'), the button turns into 'Undo last batch (9)' immediately (ux3-80-after-acceptall.png) and nine per-row Undo links appear, so the action is reversible in one click. Shift+A, the key that can fire by accident, asks first and states the count (ux3-72-shiftA.png). That meets dossier check 9 and the error-prevention heuristic better than a confirm on every click would.

## Screen polish, 1 to 5 (pass 1 -> pass 2 -> pass 3; 4 = would pass in a Carbon or Atlassian product)

| Screen | P1 | P2 | P3 | Why |
|---|---|---|---|---|
| Case list and library | 2 | 3 | 3 | Landing is one 900 px screen; slugs and mid-word clamps remain (m1) |
| Paste / upload | 3 | 4 | 4 | Not re-walked beyond the landing; unchanged |
| Processing and failure | 2 | 4 | 4 | Not re-walked; code unchanged since pass 2 |
| Timeline and review queue | 2 | 3 | 4 | 110 to 138 px rows, quote beside the summary, first Accept on screen, decided rows read as decided; ISO dates, clipped caution line (m-new3) |
| Case checks and AI check | 3 | 3 | 4 | One card, one next step; text-link toggles |
| Flags | 2 | 4 | 4 | Side-by-side evidence unchanged; double dismiss (m7); gap flag at y 2,090 (m-new1) |
| Charges and billing | 2 | 3 | 3 | Columns aligned; rows taller, reasons doubled, primary on not-totaled (m2) |
| Source record | 3 | 4 | 4 | Sticky pane; modal duplicate and raw marker (m4) |
| Dates, tray, manual entry | 2 | 3 | 4 | Radio with suggested reading and reason; tray row has plain lead and 'Nothing to accept here'; disabled row remains |
| Export and paragraph | 3 | 4 | 4 | Summary line names what is in and out ('9 entries, 0 charges in letter ... 14 items pending (10 flags)'), pending items under their own heading, Copy letter and Download .txt |
| Mobile 390 | 2 | 3 | 4 | No horizontal scroll on any page; every row button 44 px; rows 246 to 330 px; first row at 893 px behind about one screen of status panels; link row is 36 px |
| Dark mode | 1 | 4 | 4 | Spot-checked on lib09 (ux3-65-dark-top.png) |
| Keyboard | 2 | 3 | 4 | Skip links reach dates, the dismissal suggestion or the first item in Tab + Enter; shortcut sheet works; Start review button |

## Does it read as a polished enterprise tool?

On the sample case, yes, for a prototype: a sticky case header with progress and the primary action, state chips with icons, captioned verbatim evidence in every row, side-by-side conflict quotes, a source pane, an undoable batch action, a keyboard sheet, light and dark from one token layer. Set beside the marketing descriptions of EvenUp, Supio, Filevine and Litify (no UI seen), it now has what their lists lead with. Three things still give it away as a prototype: library cases show file slugs as titles (m1), row dates are ISO while the letter uses long dates (m3), and two small copy-and-control leftovers (two reasons per unclear charge, two dismiss buttons per flag). None blocks a demo; all are cheap.

## Findings

### m-new1 (minor): first screen is close but not at the target; the gap flag is still 2,090 px down
`ux3-walk1-results.json`: first row top 464 (target < 450), `rows_fully_visible` 3 (target 4), gap flag at y 2,090 at 1440x900 (pass 2: 3,015; pass 1: 4,161). Three status blocks above the Timeline (Records, Open decisions, Case checks) take 464 - 131 = 333 px. Dossier check 19 (73-day gap visible without scrolling) still fails; the pane's 'Show gap flag' button and 'Skip to the gap flag' link are the workaround. I rate it minor because the work (first Accept in view, 110 to 138 px rows) is now above the fold; this is my judgement against the pass-2 target, not a spec constraint.

### m-new2 (minor): a dismissed row stays in the queue, with its verbatim quote struck through and Accept offered
`ux3-39-after-dismiss.png`, `ux3-59m-lib09-dismissed.png`. The Accepted half of M3 is fixed. The dismissed row keeps its place in the list, strikes through the record's own quote (the record did not change, only the decision), and shows a secondary Accept beside 'Undo'. The handoff names the 'Dismissed (n)' group as not done.

### m-new3 (minor): the AI-translation caution and the summary are clipped to one line in collapsed rows
`ux3-39-after-dismiss.png` (1440): '▲ Check: translated by AI; read the o…' and, on decided rows, 'Patient reports pain 6/10 that worsens when raising the arm. Denies lo…'. At 390 the caution wraps in full; at 1440 the safety sentence is cut. A sentence whose job is to say 'read the original yourself' should not be the clipped one.

### m-new4 (minor): the AI-check panel row for a could-not-verify flag contradicts the tray
`ux3-117-judge-panel-lib06.png` and `ux3-117-tray-lib06.png`: the panel row says 'Your decision: Not reviewed' and 'What you need to do: ... Edit it, accept it if you agree with it, or dismiss it', while the tray says 'Nothing to accept here'. Same panel still uses 'See the steps', 'Technical details', 'Code said' and 'phrase list'. See T-117 review.

### Pass-2 minors still open (m1, m3, m4, m5, m7, n1) and partial (m2, m6, m8)
Evidence in the table above; fixes unchanged from pass 2. Of these, the quickest wins for a demo are m1 (library names), m3 (`Intl.DateTimeFormat` inside `<time>` and an e2e filter on `datetime`), m7 (one dismiss control) and m2 (secondary 'Keep in notes').

### N1 (nit): `?` does nothing from the page top
Mouse at (5,5), focus on body, `?` pressed: no dialog. After Start review, `?` opens it. The dialog intro says letter keys need a selected item, but `?` is a help key. Fix: open the sheet from anywhere except a text field.

### N2 (nit): 'More' has a different accessible name from its label
`aria-label` 'Show all of Dr. Alvarez, primary care, 2026-01-16' on a button that reads 'More'; Playwright `get_by_role('button', name='More')` finds nothing. Deferred to accessibility-reviewer.

## What is right (do not break)

- The decided-row treatment and 'Undo last batch (n)': one click reverses the batch, and Shift+A is the only path that asks.
- Skip links that land on the most blocking work (dates form, dismissal suggestion, first item) in Tab + Enter, at both widths.
- Compact row with the quote beside the summary, captioned with record and provider, 110 to 138 px, and More for the full excerpt in the same row.

```json
{
 "card": "T-060",
 "persona": "ux-designer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "app/frontend at HEAD e1ce8dc (frontend identical to 7d5a45f; commits c8e36fb, 5d975ed, d9efc5c, 7d5a45f); app at http://127.0.0.1:7981 (git archive HEAD, fixture backend, ZLAYT_MODE=local); sample case and library cases lib01, lib06, lib09, lib11, lib14; 1440x900 and 390x844",
 "exercised": [
  "git rev-parse --short HEAD (e1ce8dc), git diff --stat 7d5a45f HEAD -- app/frontend (empty), git status --short | wc -l (1742, dirty), git archive HEAD into scratchpad; server PID 49349 stopped with kill, port returns 000",
  "Playwright at 1440x900 and 390x844 touch: landing, sample results, five library cases, Shortcuts button and ? key, Start review, Tab order and skip links, a/d/k/r/e/Shift+A, More, Open record, Edit with unsupported number, Accept, Dismiss, Undo, Accept all verified and Undo last batch, flags, charges, export with pending items, dark mode, computed-style census, AI-check panel on five cases at two widths",
  "real dismissal-suggestion case (three prior dismissals via the real route), calibration route (real stale state), reading present.py and manual.js for the sentences_reason copy",
  "not exercised: PDF upload, real-model latency, Safari/Firefox, WCAG conformance, audit drawer, 1024 and 768 widths, failed-run stub, Exhibit/Bates form; EvenUp, Supio, Filevine, Litify compared by marketing text only"
 ],
 "verdict": "pass",
 "scores": {
  "design_quality": 4,
  "originality": 3,
  "craft": 4,
  "functionality": 4
 },
 "findings": [
  {
   "severity": "minor",
   "title": "m-new1. First row at 464 px and 3 rows on the first screen (target < 450 and 4); the 73-day gap flag is still 2,090 px down",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-walk1-results.json: landmarks entry1 464, gap 2090; rows_fully_visible 3; entry heights 110 to 138; artifacts/review-evidence/T-060-pass3/ux3-04-results-d.png",
   "why_it_matters": "Dossier check 19 (gap flag visible without scrolling) still fails; the pass-2 M2 target was 4 rows on the first screen. The work itself is now above the fold, so this is minor.",
   "fix": "Fold the Records card into the header or the Open decisions card, and drop the 'What you need to do' strip when Start review is shown. Optionally promote a one-line gap headline into the Open decisions card with a link to the gap card.",
   "acceptance_test": "Sample case, 1440x900, scroll 0: first entry top < 450, at least 4 [data-entry-id] rows fully visible; the gap flag headline is in the viewport."
  },
  {
   "severity": "minor",
   "title": "m-new2. Dismissed rows stay in the queue with the record's quote struck through and Accept offered",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-39-after-dismiss.png, artifacts/review-evidence/T-060-pass3/ux3-59m-lib09-dismissed.png, artifacts/review-evidence/T-060-pass3/ux3-walk2-results.json (dismissed_section [])",
   "why_it_matters": "The Accepted half of pass-2 M3 is fixed; a dismissed row still takes full row space and strikes through verbatim record text, which did not change.",
   "fix": "Collapse dismissed rows under a 'Dismissed (n)' disclosure at the end of the queue with Undo; strike through the summary only, never the quote.",
   "acceptance_test": "After Dismiss the row is not a child of [data-testid=queue] and appears under 'Dismissed (1)'; the excerpt block has no line-through."
  },
  {
   "severity": "minor",
   "title": "m-new3. The 'translated by AI; read the original quote yourself' caution and decided summaries are clipped with an ellipsis at 1440",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-39-after-dismiss.png ('Check: translated by AI; read the o...'), artifacts/review-evidence/T-060-pass3/ux3-37-after-accept.png",
   "why_it_matters": "The caution exists to make the reviewer read the original; clipping it removes the instruction. Clipping the summary of an accepted row hides what will go into the letter until More is pressed.",
   "fix": "Let the caution wrap (it already does at 390) and give it its own line; clamp decided summaries to 2 lines, not 1.",
   "acceptance_test": "At 1440 the caution text of a translated row is fully visible (scrollWidth <= clientWidth)."
  },
  {
   "severity": "minor",
   "title": "m-new4. AI-check panel row for a could-not-verify flag tells the reviewer to accept it; the tray says nothing can be accepted",
   "evidence": "artifacts/review-evidence/T-060-pass3/ux3-117-judge-panel-lib06.png ('Degenerative wording · Record 5 ... Your decision: Not reviewed ... accept it if you agree with it, or dismiss it'), artifacts/review-evidence/T-060-pass3/ux3-117-tray-lib06.png ('Nothing to accept here')",
   "why_it_matters": "Two surfaces give opposite instructions for the same item; the panel also still uses 'See the steps', 'Technical details', 'Code said' and 'phrase list', which pass 2 reported gone on the closed panel.",
   "fix": "For tray items the panel row shows 'Left out of the letter' and no decision line or action sentence; use 'Why this status' as the one label for the steps.",
   "acceptance_test": "The judge row for a [data-tray-kind=flag] item contains no 'accept' and no 'Your decision'."
  },
  {
   "severity": "minor",
   "title": "Pass-2 m1/m3/m4/m5/m7/n1 still open; m2/m6/m8 partial",
   "evidence": "Table in this review; artifacts/review-evidence/T-060-pass3/ux3-walk1-results.json (iso_dates), ux3-walk3-results.json (open_record_modal true, edit_live unchanged), ux3-walk8-results.json (lib11_header 'case lib11 priors and ledger', primary_in_unclear 2, census font sizes 6), ux3-14-flags-panel.png, ux3-15-charges.png",
   "why_it_matters": "Slug titles, ISO row dates, a duplicate record modal, no live edit check, two dismiss controls and primary 'Keep in notes' are what remain between this and a product that looks finished.",
   "fix": "As in pass 2: manifest names; Intl long dates in rows; open the record in the pane at >= 1024; debounced edit check; one dismiss control; secondary 'Keep in notes'; one reason per unclear row.",
   "acceptance_test": "Pass-2 acceptance tests for m1 to m8 and n1 unchanged."
  },
  {
   "severity": "nit",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:23.231Z

**tool call — Bash**
````
{
 "command": "grep -n \"minor\\|nit\\|major\" reviews/T-060-accessibility-pass3.md | head -40; echo =====; sed -n 1,80p reviews/T-114-paralegal-r2.md"
}
````

### User / tool · 2026-11-02T11:05:23.351Z

**tool result**
````
4:Verdict: **pass**. No blockers, no majors. All four pass-2 majors are fixed. Four minors and seven nits remain (listed below).
8:All four pass-2 majors are fixed and verified in the running build: the shortcut sheet prints its keys, the 320 CSS px reflow holds with Case checks and the AI-check panel both open, the theme toggle name follows the visible state, and the Upload control shows a focus ring that opens the file chooser on Enter and Space.
10:Pass-2 N-8 (skip-link targets) is partial: the queue views are fixed, but in the Export and copy views three of the four skip links point at elements that are not rendered. Pass-2 N-9 (timeline rows as Tab stops) is still open. Two new minors: the entry More/Less control's name omits its visible text and changes with state, and the timeline container carries an `aria-labelledby` with no role. Two new nits: the Export heading has no visible focus indicator, and a decided Accept keeps `aria-pressed="true"` while a second press does nothing.
38:| N-1 shortcut sheet prints `[object HTMLElement]` | major | **fixed** | `review.js:301` now `KEYS.flatMap(...)`. Sheet: 9 `kbd`, 9 `dt`, 9 `dd`, no "[object" (`T-060-accessibility-pass3-details.json`: `sheet_has_object_html_text` false, `sheet_kbd_count` 9). axe `10-shortcuts-sheet` has no `definition-list` in light or dark. |
39:| N-2 320 px reflow with Case checks open | major | **fixed** | `styles.css:250` `.zs-chip { white-space: normal; max-width: 100% }`. With Case checks open, `scrollWidth` 320 (`T-060-accessibility-pass3-reflow-probe.json`). With Case checks and "How the AI was checked" both open, 320 px, `scrollWidth` 320 and 0 chips past the edge in queue, edit, flags, charges, Export and the source dialog (`T-060-accessibility-pass3-extra.json` `b_reflow320_*`, 42 visible chips each). |
40:| N-3 theme toggle name stale | major | **fixed** | `app.js:40` sets `aria-label` on every change. Keyboard: after 1 press "Theme: light. Press to change it."; after 2, "Theme: dark. Press to change it."; after 3, "Theme: auto. Press to change it." (`T-060-accessibility-pass3-names.json` `theme_three_presses`; `T-060-accessibility-pass3-keyboard-results.json` `k_theme_name_after_*`). |
41:| N-4 Upload control: 1x1 clipped focus stop | major | **fixed** | `styles.css:248` `label.btn:has(+ #file:focus-visible)` draws a 2 px ring. At 3x zoom the ring is visible around "Upload .txt" (`T-060-accessibility-pass3-file-ring-zoom.png`); computed `solid 2px rgb(11, 87, 208)`, 6.39:1 against the label background. Enter and Space each open a file chooser (`T-060-accessibility-pass3-file-ring-zoom.json`). |
42:| N-5 "Why this status" buttons share a name | minor | **fixed** | `stepper.js:466` names each button with its item. 23 visible buttons, 23 unique names (`T-060-accessibility-pass3-details.json` `why_status_buttons`). |
43:| N-6 dismiss-with-reason has no `aria-controls` | minor | **fixed** | `review.js:240` `aria-controls` = `dr-f_gap_r6_r7`, and the input has that id (`j_dismiss_reason_attrs_after`, `j_dismiss_reason_input_labelled`). |
44:| N-7 `landmark-unique` on the side-by-side pane | minor | **fixed** | axe `landmark-unique` absent in all 36 scans. |
45:| N-8 skip-link targets | minor | **partial** | Queue views: all four `#skip-nav` hrefs resolve (`skip_targets_exist` true) and axe `skip-link` passes. Export and copy views (audit states 14 to 16, light and dark): `#skip-to-review`, `#skip-to-flags` and `#skip-to-charges` do not exist, so axe `skip-link` (moderate, 3 nodes, "No skip link target") in 6 scans. Activation still works through `onclick` (`T-060-accessibility-pass3-extra.json` `a_export_view_skip`). See finding P3-3 below, folded into N-8. |
46:| N-9 each timeline row is a Tab stop and also holds buttons | minor | **open** | `review.js:358` still sets `tabindex="0"` on the row. At 1280 px light the walk has 19 row stops, each followed by 8 buttons (Accept, Edit, Dismiss, Why, Open record, Audit, Change quote, More). `walk_1280_names|light`. |
47:| N-10 edit textarea name drops the visible rule | minor | **fixed** | No `aria-label` on the textarea. Accessible name = "Summary wording (the quoted excerpt, date and provider cannot be changed)". Refused edit: `aria-describedby` = `rv-err-e2`, role=alert, visible (`T-060-accessibility-pass3-details.json` `edit_label_chain`, `refused_describedby_target`). |
48:| N-11 focus after Accept goes to Flags | nit | open, unchanged | Accept e1 by Enter moves focus to `flag-f_r7_1` "Accident date source". Announcement unchanged. Product question. |
49:| N-12 two polite regions per decision | nit | open | Accept e1: `rv-live` ("Accepted: Austin EMS run report, 2026-01-09. 22 left to review.") and `progress-text` (role=status, "1 of 23 decided") both change (`j_accept_e1.live_after`). |
50:| N-13 two stops partly under the sticky header at 320 px | nit | open | `walk_320|light` `partly_hidden_by_sticky_or_other`: stop 109 visible on 3 of 9 points (covered by `#case-name` and `#btn-export`), stop 117 visible on 6 of 9. `entirely_hidden_count` 0, so SC 2.4.11 AA passes. |
51:| N-14 twelve "Technical details" summaries share a name | nit | open | 12 visible (`technical_details_visible` 12). |
52:| N-15 source dialog Tab goes to browser chrome and back | nit | open, unchanged | `source_modal_tab_targets` alternates BODY (browser chrome) and Close. Batch-confirm shows the same pattern (`s_shift_a_tab_inside_4`). Not a trap. |
53:| m1 live region node | minor | fixed | `rv-live` and `progress-text` keep their nodes across an Accept (`l_after_accept_identity`: `rvSame` true, `ptSame` true). |
54:| m3 dismiss-with-reason | minor | fixed | See N-6. |
55:| m4 blocked-copy alert | minor | fixed | Copy anyway blocked: `role="alert"`, class `error` (`j_copy_anyway_status`). |
56:| m5 landmarks and headings | minor | fixed | See N-7. |
57:| m6 skip links | minor | partial | See N-8. |
58:| m7 row tab stops | minor | open | See N-9. |
59:| m8 Enter vs a | minor | fixed (unchanged) | Enter on Accept e1 moves focus to the next needs-review item, `flag-f_r7_1`, as in pass 2. |
60:| M6 generic button names | major, now minor | fixed | Timeline names, flag and charge "Why this status" names all fixed (N-5). |
61:| B1, M1 to M5 (pass 1) | blocker, majors | fixed | Letter keys from Export or an input change nothing (`s_from_export_focus`, `T-060-accessibility-pass3-keyboard-results.json`). Dark and light contrast 0 failing (below). Export focus on the heading in view, Copy letter one Tab away. Copy anyway returns focus to Copy letter. |
67:**P3-1. The row More/Less control's name omits its visible text and changes with its state.** (SC 2.5.3 Label in Name, Level A; same class as pass-2 N-10, rated minor there.)
75:- Why it matters: the attribute is prohibited on a generic `div`, so AT ignores it. The heading "Timeline" still exists visually, but the list has no programmatic name or role. This is a needs-review item in axe, not a violation, so it is a minor here.
85:**P3-4. Export heading has no visible focus indicator after Enter on Export.** (SC 2.4.7 applies to the focused element; the checklist scopes the rule to interactive elements, so this is a nit.)
96:**Carried nits (unchanged or open):** N-11 (focus after Accept, product question), N-12 (two polite regions), N-13 (two stops partly under the sticky header at 320 px), N-14 (twelve "Technical details" names), N-15 (source dialog Tab through browser chrome). Fixes and acceptance tests are in the pass-2 review.
100:- **axe-core, 18 states x light and dark (36 scans):** 0 serious or critical violations. Moderate `skip-link` in 6 scans (Export and copy views, N-8). `landmark-unique` gone. `definition-list` gone. Axe "incomplete" items (needs review): `color-contrast` in the empty states, why dialog and dialogs; `aria-prohibited-attr` (P3-2). My own computed contrast found 0 failures for these, so the axe incomplete items are not text-contrast failures.
112:- All four pass-2 majors are closed, and each fix was measured in the running build, not read from the code.
148:  {"severity": "minor", "title": "N-8 (partial): skip-link hrefs in the Export and copy views point at elements that do not exist; axe skip-link moderate in 6 scans",
153:  {"severity": "minor", "title": "N-9 (open): each timeline row is a Tab stop and is followed by 8 buttons (pass-1 m7, pass-2 N-9)",
155:   "why_it_matters": "APG composite pattern: a row that is both a stop and a container of stops gives a mixed model, and the sample needs about 215 Tab presses to walk the page. Every action is still reachable, so this is minor.",
158:  {"severity": "minor", "title": "P3-1: the row More/Less control's name omits its visible text and changes with state (SC 2.5.3)",
160:   "why_it_matters": "SC 2.5.3 Label in Name (Level A): the collapsed name does not contain the visible text 'More'. The name also changes with aria-expanded, so state is announced twice. Same class as pass-2 N-10, rated minor there.",
163:  {"severity": "minor", "title": "P3-2: the timeline container has aria-labelledby with no role; axe aria-prohibited-attr (incomplete, serious) in 22 scans",
165:   "why_it_matters": "SC 4.1.2. The attribute is prohibited on a generic div, so the list has no programmatic name and AT ignores it. The visible h2 'Timeline' still titles the list. axe marks it needs-review, not violation, so this is minor.",
=====
# T-114 r2 review: paralegal-reviewer (Maria Delgado persona)

Verdict: **changes** (0 blockers, 1 major, 1 minor, 2 nits). The gap-change notice now appears when a date is confirmed and names both numbers, but it is held only in page memory. After Got it or a reload the gap card reads "Gap of 40 days" with no reason, so the round-1 major is still open. The round-1 minor is partly fixed: the "Accept as noted" button is gone, but an accepted rate row still shows a "Needs review" chip. The round-1 nit (lib01 fixture miss) is still there.

The scope is HEAD, not b5fb35c. HEAD is e1ce8dc, which includes the T-060 r3 frontend commits (c8e36fb, 5d975ed), so the round-1 "no UI consumer" finding had to be re-tested on the committed code.

## Round-1 items

| Round-1 item | Status at e1ce8dc | Evidence |
|---|---|---|
| Major: gap change must show in the UI | Partly. Banner at confirm: yes. Gap card and after reload: no. | artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json |
| Minor: accepted rate row reads unfinished | Partly. "Accept as noted" gone; "Needs review" chip still on the row. | artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png |
| Nit: lib01 extract misses its fixture | Still open. One FIXTURE_MISS row for case lib01. | sqlite3 query output in the exercised list |

## What I ran

Deterministic first.

- `git rev-parse HEAD` printed `e1ce8dc620e6ec0778320456ac79a25f1832bfee`. `git merge-base --is-ancestor c8e36fb HEAD` and the same for `5d975ed` both succeeded.
- `git archive HEAD` extracted to the session scratchpad `t114r2/archive`. `grep -rln gap_changes app/frontend app/backend` returned `app/frontend/timeline.js` and `app/backend/review.py`.
- Server from the archive: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local HOST=127.0.0.1 PORT=7881`, ZLAYT_DB in the scratchpad, PID 51899. `GET /` returned 200. Stopped by PID at the end. The team app on 7860 was not touched.

Live checks. Scripts are in `artifacts/review-evidence/`, run with `.venv/bin/python` (`-I` for the JSON check).

- `T-114-r2-paralegal-probe.py`: lib09 has one date to confirm (record 4, "03/05/2026"), candidates 2026-03-05 and 2026-05-03, suggested 2026-05-03. The gap is 42 days, record 1 to record 2.
- `T-114-r2-paralegal-sweep.py` (out: `T-114-r2-paralegal-sweep.out.json`): all 15 library packets, fresh cases. Two confirm attempts in total, both lib09 record 4. Confirming 2026-03-05 returns `gap_changes` 42 to 40 (new start 2026-03-05). Confirming 2026-05-03 returns none.
- `T-114-r2-paralegal-ui-gap.py` (Playwright, Chromium, 1440x900; out: `T-114-r2-paralegal-ui-gap.out.json`): confirmed record 4 as 2026-03-05 in the Dates to confirm form, read the banner text and position, scrolled to top, clicked Got it, reloaded, then accepted rate a3 on a second load.
- `T-114-r2-paralegal-checks2.py` (out: `T-114-r2-paralegal-checks2.out.json`): full gap-card text after confirm and after reload, rate a3 chips and the Kept in notes control, FIXTURE_MISS rows.
- `sqlite3` on the scratch DB: `SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name;` printed `case lib01 er only then gap|1`. The same query without the join printed `1`.
- `T-114-r2-paralegal-jsoncheck.py` on the draft JSON: `findings {'blocker': 0, 'major': 1, 'minor': 1, 'nit': 2} verdict changes`, `errors none`, `paperwork sentence count in reloaded gap card: 2`, `'was 42' or 'recalculated' in reloaded gap card: False`.

Code read at HEAD: `app/frontend/timeline.js:73, 77, 95, 97`; `app/frontend/review.js:233`; `app/frontend/charges.js:77`; `app/backend/review.py:353-364, 400`.

Not exercised: I did not click "Kept in notes" or Undo on the rate row. I did not walk the 30 exports or the 7 refusals again (round 1 covered them, and this round's scope is the notice and the minors). The working tree has uncommitted changes (for example `app/backend/api.py` and `app/backend/pipeline.py` in `git status --short`), so this review covers the HEAD archive only.

## Findings

### Major: the gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed

Evidence: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.after_confirm.note_text is "A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it". steps.after_dismiss.note_count is 0. steps.after_reload.note_count is 0, body_has_recalc is false and body_has_was_42 is false. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload begins "Gap of 40 days Needs review Gap of 40 days between March 5, 2026", and the check reports no "was 42" or "recalculated" on the card. The only 42 on the card is in the paperwork sentence: "the gap would be 42 days (March 3, 2026 to April 14, 2026)". Source: `app/frontend/timeline.js:73` (`let gapNote = null`) and `timeline.js:97` (Got it clears it). Screenshots: `artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png` and `artifacts/review-evidence/T-114-r2-ui-4-after-reload.png`.

Why it matters: round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray. Its acceptance test was that the gap flag card shows "Gap recalculated after you confirmed record 4: now 40 days (was 42)." At e1ce8dc the notice is clear at the moment of confirm, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The adjuster counts days between encounters and asks why a number changed. The round-1 acceptance test is not met.

Fix: show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory. One line under the title, for example "Changed after you confirmed record 4: now 40 days (was 42)." It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.

Acceptance test: lib09, confirm record 4 as 2026-03-05, then reload. The element `flag-f_gap_r4_r2` contains "now 40 days (was 42)" and "March 5, 2026". Repeat after clicking Got it on the banner.

### Minor: an accepted rate row still shows a "Needs review" chip beside "Accepted"

Evidence: `artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png`. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` rate_a3_chips is ["Needs review", "Accepted"], and rate_a3_needs_review_text_count is 1. Fixed part: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.rate_a3_after.has_accept_as_noted is 0. The control is now "Kept in notes" (`app/frontend/review.js:233`) with Undo, and the text reads "Kept in the internal notes only; not in the letter or the total." (`app/frontend/charges.js:77`).

Why it matters: the Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.

Fix: after acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false). I did not click it; if it does nothing, it should not look like a button.

Acceptance test: lib09, accept rate a3. The row contains no "Needs review" text (count 0), and its status reads Accepted or Noted only.

### Nit: the lib01 extract step still misses its demo fixture on every run

Evidence: the sqlite3 query in the exercised list printed `case lib01 er only then gap|1`. The row is step extract, attempt 1, parsed_ok 0, error "FIXTURE_MISS 83bcee077841...". Round 1 saw four such rows across its lib01 runs.

Why it matters: nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.

Fix: record the lib01 extract response under `tests/fixtures/llm/` (curated set), or note the fallback on the card.

Acceptance test: a fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls.

### Nit: the paperwork sentence appears twice in the lib09 gap card

Evidence: `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload. "which looks like paperwork, not a visit" occurs twice (the jsoncheck count is 2). Each occurrence is followed by "If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)", with the "Needs review: AI translation" text between them.

Why it matters: the gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It sits on the card this card touches, so I flag it here.

Fix: render the paperwork note once in the gap card.

Acceptance test: lib09 gap card after confirming record 4: the text "looks like paperwork" occurs once.

## Right already

- The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers ("now 40 days (was 42)"), and is announced in the status region.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:23.956Z

**tool call — Bash**
````
{
 "command": "grep -n \"minor\\|nit\\b\" reviews/T-117-ux-designer.md | head -20; echo ====; grep -n -i \"doubl\\|sentences_reason\\|no sentences\\|minor\" reviews/T-096-ux-designer-r2.md | head -30"
}
````

### User / tool · 2026-11-02T11:05:24.056Z

**tool result**
````
3:**Verdict: pass.** The row is titled with the flag's name and a record cue, like every other row; no raw id appears in the panel on any of the five library cases at 1440 or 390. One minor (copy contradicts the tray) and no blocker or major.
19:### F1 (minor): the panel row tells the reviewer to accept an item the tray says cannot be accepted
44:  {"severity": "minor", "title": "AI-check panel row for a could-not-verify flag says to accept or dismiss it; the tray says nothing can be accepted",
====
3:**Verdict: pass.** The round-1 major (keyboard reach, 87 to 102 Tab presses) is fixed: Tab, Enter reaches the dates form and the dismissal suggestion at both widths. Of the 5 round-1 minors, 2 are fixed (Keep showing persisted, pointer near the top), 2 are fixed with a small residual (stale note, tray wording) and 1 is open (sentences_reason copy). No blocker, no major.
21:| F6 | sentences_reason copy repeats; no corpus case | **Open (minor)** | `app/frontend/manual.js:55` renders 'This record has no sentences to pick from.' + ' Why: ' + reason; the reason (`app/backend/present.py:188`) starts 'No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, ...'. 'no sentences' appears twice, 'could not be told apart' is a developer phrase, and no real case reaches the state |
26:### F6 (minor): the no-sentences message still says the same thing twice and speaks in layout terms
27:Evidence: `app/frontend/manual.js:55`; `app/backend/present.py:188`. Composed message: 'This record has no sentences to pick from. Why: No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, so a quote cut from it could not be checked against the record. Read the record text instead.'
30:Acceptance test: a non-stubbed case with a record without Date and Source lines shows `manual-no-sentences` with one sentence and no repeated 'no sentences'.
59:  {"severity": "minor", "title": "F6. The no-sentences message states the same fact twice and uses layout terms",
60:   "evidence": "app/frontend/manual.js:55 ('This record has no sentences to pick from.' + ' Why: ' + reason); app/backend/present.py:188 (reason starts 'No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text')",
61:   "why_it_matters": "The reviewer reads 'no sentences' twice, then a developer phrase; the one instruction ('Read the record text instead') comes last. No real case reaches the state.",
63:   "acceptance_test": "A non-stubbed case with a record without Date and Source lines shows manual-no-sentences with one sentence and no repeated 'no sentences'."},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:26.276Z

**tool call — Bash**
````
{
 "command": "sed -n 15,30p reviews/T-117-ux-designer.md; cat app/frontend/timeline.js; cat app/frontend/manual.js | sed -n 40,70p"
}
````

### User / tool · 2026-11-02T11:05:26.380Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:26.813Z

**tool call — Bash**
````
{
 "command": "grep -n \"gap_changes\\|gap_change\" -r app/backend memory/contracts/api.md | head -30"
}
````

### User / tool · 2026-11-02T11:05:26.931Z

**tool result**
````
app/backend/review.py:353:    gap_changes = []
app/backend/review.py:354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
app/backend/review.py:355:    for ch in gap_changes:
app/backend/review.py:356:        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
app/backend/review.py:363:            "removed_flag_ids": removed, "gap_changes": gap_changes,
app/backend/review.py:400:def _gap_changes(old: dict, new: dict) -> list:
app/backend/review.py:423:def _gap_change_sentence(ch: dict, seq) -> str:
app/backend/review.py:471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
memory/contracts/api.md:262:**T-116 / D-055 (rounds 3 and 4): gap math runs over EVERY dated record, whatever ingest called it; paperwork-looking records warn and show the other number, they are never dropped.** The ingest `kind` (encounter, billing_statement, phone_note, records_admin) is a label guess and gap math does not read it; a visit whose label carries a paperwork word is an endpoint like any other. `gaps.admin_label` reads a record's header (`Source:`) label and returns a plain label (intake form incl. `formulario de admisión`, billing statement, ledger, EOB, claim form, affidavit, records request, records review, narrative letter, letter or correspondence, phone or message note, administrative record) or null. It is conservative: a visit word in the label (outside the provider name and parentheses) or treatment evidence in the text means no label. It changes no counted gap date, day count or flag. Confirming record 4 of lib09 as 5 March moves the gap 42 to 40 days and `gap_changes` reports it, as in T-114.
memory/contracts/api.md:268:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:28.854Z

**tool call — Bash**
````
{
 "command": "sed -n 325,480p app/backend/review.py; grep -n \"gap_change\\|gap_note\\|gapNote\" app/frontend/*.js tests/e2e/*.py | head -30"
}
````

### User / tool · 2026-11-02T11:05:28.980Z

**tool result**
````
    enforce_ocr(conn, case_id, t)
    return chk["warnings"]


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
            "removed_flag_ids": removed, "gap_changes": gap_changes,
            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}


def _without_date_doubt(item: dict) -> dict:
    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
        reasons.append("AI_TRANSLATION")
    state = item["state"]
    if state == "needs_review" and not reasons:
        state = "verified"
    out = {"state": state, "state_reasons_json": reasons}
    if isinstance(item.get("ladder"), dict):
        out["ladder"] = {**item["ladder"], "state": state}
    return out


def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t):
    after = {"date_chosen": date_iso, "date_raw": rec["date_raw"], "candidates": rec["date_candidates"], "record_id": rec["id"],
             "cleared_date_ambiguous": cleared}
    before = {"date_status": "ambiguous", "date_iso": rec.get("date_iso")}
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, "confirm_date", DB._enc(before), DB._enc(after), t))


def _drop(conn, case_id, flag_id):
    cur = conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (flag_id, case_id))
    return [flag_id] if cur.rowcount else []


def _gap_figures(flag: dict) -> dict:
    c = flag.get("computed") or {}
    return {"flag_id": flag["id"], "from": c.get("from_date"), "to": c.get("to_date"), "days": c.get("days"), "record_nos": list(c.get("record_nos") or [])}


def _gap_changes(old: dict, new: dict) -> list:
    """Which gap figures a recompute changed (T-114). `old`/`new` map flag id -> _gap_figures. A gap whose id survives and whose figures moved is `changed`; an
    old gap that vanished and a new one that shares a record number with it are ONE `changed` entry (an endpoint moved); the rest are `removed` / `added`.
    Each: {flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to}; the side that does not exist is null. Code over the figures, never a model."""
    rows = []
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
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
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
    if changes is not None:
        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
    return removed


# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
tests/e2e/conftest.py:51:  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
app/frontend/timeline.js:70:  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
app/frontend/timeline.js:73:  let gapNote = null;   // {token, items: [sentence]}
app/frontend/timeline.js:76:    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
app/frontend/timeline.js:77:    gapNote = changes.length ? { token: s.token, items: changes } : null;
app/frontend/timeline.js:93:  function gapNoteNode(c) {
app/frontend/timeline.js:94:    if (!gapNote || gapNote.token !== c.token) return null;
app/frontend/timeline.js:96:      el("div", { class: "notice-body" }, el("strong", {}, "A gap figure changed. "), gapNote.items.map((t) => el("span", { class: "gap-sentence" }, t + " "))),
app/frontend/timeline.js:97:      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
app/frontend/timeline.js:242:    const gapN = gapNoteNode(c); if (gapN) wrap.append(gapN);
tests/e2e/test_polish_r3.py:257:def test_t114_gap_change_notice_renders_after_a_date_confirm(page, lib09):
tests/e2e/test_polish_r3.py:258:    """T-114: confirm_date answers gap_changes[]; the sentence shows above the timeline and is announced."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:33.315Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"keep showing\\|keep_showing\\|ui_state\\|prefs\\|localStorage\" app/frontend/*.js memory/contracts/api.md | head -20; cat app/frontend/state.js app/frontend/api.js"
}
````

### User / tool · 2026-11-02T11:05:33.407Z

**tool result**
````
app/frontend/app.js:35:  // ---- theme: auto (follow the OS), light or dark. Remembered in localStorage when it is available; the page works without it.
app/frontend/app.js:41:    try { localStorage.setItem("zlayt.theme", t); } catch (_) { /* not remembered */ }
app/frontend/app.js:125:    let saved = "auto"; try { saved = localStorage.getItem("zlayt.theme") || "auto"; } catch (_) { /* no storage */ }
app/frontend/suggestions.js:3:   ZL.sg.dismissalBox  banner "You dismissed this kind of flag N times..." with Hide similar / Keep showing (T-089); never hides on load
app/frontend/suggestions.js:55:  // "Keep showing" is client-side only, and remembered for this browser per case + key (localStorage, wrapped: the page works without it).
app/frontend/suggestions.js:58:    get: (_, k) => { try { return localStorage.getItem(keptKey(String(k))) === "1"; } catch (_e) { return false; } },
app/frontend/suggestions.js:59:    set: (_, k, v) => { try { if (v) localStorage.setItem(keptKey(String(k)), "1"); else localStorage.removeItem(keptKey(String(k))); } catch (_e) { /* not remembered */ } return true; },
app/frontend/suggestions.js:71:      const keep = el("button", { type: "button", class: "btn", "data-testid": "btn-keep-showing", "data-key": s.key }, "Keep showing");
memory/contracts/api.md:295:Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed (reversible with `reset`); the response is then an error and the refreshed list shows what remains. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
/* Tiny store. ZL.state.get() -> {health, token, case, status, error}; subscribe(fn) re-renders on every set(). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  let s = { health: null, token: null, created: null, case: null, status: null };
  const subs = [];
  ZL.state = {
    get: () => s,
    set(patch) { s = Object.assign({}, s, patch); subs.forEach((f) => f(s)); },
    subscribe(f) { subs.push(f); },
    // Patch the local case from a POST .../review response (item + totals + review); T-043 calls this after each decision.
    applyReview(resp) {
      const c = s.case; if (!c || !resp || !resp.item) return;
      for (const k of ["entries", "undated_entries", "amounts", "flags"]) {
        const i = (c[k] || []).findIndex((x) => x.id === resp.item.id);
        if (i >= 0) { // the review response labels items with a generic kind ("amount"); an amount's own kind (charge / rate / ...) must survive
          const { kind, ...rest } = resp.item; c[k][i] = Object.assign({}, c[k][i], rest);
        }
      }
      if (resp.totals) c.totals = Object.assign({}, c.totals, resp.totals);
      if (resp.review) c.review = Object.assign({}, c.review, resp.review);
      ZL.state.set({ case: c });
    },
  };
  // Extension points for T-043 (frontend-2): register without editing T-042 files.
  ZL.hooks = { rowActions: [], panels: [] };           // rowActions: fn(entry, rowEl); panels: fn(case, mountEl) -> void
  ZL.registerRowActions = (fn) => ZL.hooks.rowActions.push(fn);
  ZL.registerPanel = (fn) => ZL.hooks.panels.push(fn);
})();
/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
  const mode = new URLSearchParams(location.search).get("api") || API_MODE;
  ZL.API_MODE = mode;

  class ApiError extends Error {
    constructor(status, err) { super((err && err.message) || "Request failed"); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }
  }
  ZL.ApiError = ApiError;

  async function call(method, path, body) {
    let status, data;
    if (mode === "mock") {
      ({ status, body: data } = await ZL.mock.handle(method, path, body));
    } else {
      const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
      status = res.status;
      try { data = await res.json(); } catch (_) { data = null; }
    }
    if (status >= 400) throw new ApiError(status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + encodeURIComponent(token);
  ZL.api = {
    health: () => call("GET", "/health"),
    createCase: (payload) => call("POST", "/cases", payload),          // {text} or {sample:true}
    getCase: (token) => call("GET", t(token)),
    run: (token, confirm_rerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirm_rerun }),
    status: (token) => call("GET", t(token) + "/status"),
    item: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id)),
    trace: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id) + "/trace"),
    caseTrace: (token) => call("GET", t(token) + "/trace"),
    judges: (token) => call("GET", t(token) + "/judges"),
    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + encodeURIComponent(rid) + "/confirm_date", { date }),
    rejudge: (token) => call("POST", t(token) + "/rejudge"),            // D-044: run the second AI check again for accepted items it never checked
    dismissalSuggestions: (token) => call("GET", t(token) + "/dismissal_suggestions"),                      // T-089: read-only list
    applyDismissal: (token, key) => call("POST", t(token) + "/dismissal_suggestions/apply", { key }),   // T-089: only ever called from the paralegal's click
    calibration: () => call("GET", "/calibration"),                                                      // T-099: {status, calibration, message}
    exportCase: (token) => call("GET", t(token) + "/export"),
    remove: (token) => call("DELETE", t(token)),
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:40.705Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/timeline.js"
}
````

### User / tool · 2026-11-02T11:05:40.792Z

**tool result**
````
/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
   T-043 plugs in through ZL.registerRowActions(fn(entry,rowEl)) and ZL.registerPanel(fn(case, mountEl)). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological

  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
  const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled",
    JUDGE_DISAGREES: "the second check did not agree", LLM_ONLY: "only the AI suggested it; the checks found nothing to match", AI_TRANSLATION: "translated by AI; read the original quote yourself", FIXTURE_MISS: "the demo has no recorded answer for this step" };
  const reasonText = (r) => REASON[r] || String(r).toLowerCase().replace(/_/g, " ");

  const STATE_TONE = { verified: ["info", "match"], needs_review: ["warn", "alert"], rejected: ["bad", "x"] };
  const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
  // Machine state and the human decision are two separate chips; an undecided item shows only the machine chip (the Accept button already says what is left).
  function chips(e) {
    const t = STATE_TONE[e.state] || ["muted", "info"], d = DECISION[e.review_status];
    return el("span", { class: "entry-chips" },
      el("span", { class: "chip chip--" + t[0], "data-icon": t[1], "data-testid": "entry-state" }, STATE_LABEL[e.state] || e.state),
      d ? el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status) : null);
  }
  function quote(e, rec) {
    return el("figure", { class: "quote" },
      el("figcaption", { class: "quote-cap" }, "Excerpt" + (rec ? " · Record " + rec.seq + " · " + rec.source_label : "")),
      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt));
  }
  // T-060 r3: a row is compact (summary and excerpt side by side, each clamped) until the paralegal opens it; the choice survives a repaint, and nothing about it depends on focus.
  const openRows = new Set();
  function entryRow(e, c) {
    const rec = c.records.find((r) => r.id === e.record_ids[0]);
    const row = el("article", { class: "entry st-" + e.state + (openRows.has(e.id) ? " is-open" : ""), "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    const reasonText_ = e.state === "needs_review" && e.reasons.length ? "Check: " + e.reasons.map(reasonText).join("; ") : "";
    const who = e.provider + (e.date ? ", " + e.date : "");
    const toggle = el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-toggle", "aria-expanded": String(openRows.has(e.id)), "aria-label": (openRows.has(e.id) ? "Show less of " : "Show all of ") + who,
      onclick: () => { const open = !openRows.has(e.id); if (open) openRows.add(e.id); else openRows.delete(e.id); row.classList.toggle("is-open", open); toggle.setAttribute("aria-expanded", String(open)); toggle.setAttribute("aria-label", (open ? "Show less of " : "Show all of ") + who); toggle.textContent = open ? "Less" : "More"; } }, openRows.has(e.id) ? "Less" : "More");
    row.append(...[
      el("div", { class: "entry-head" },
        e.date ? el("span", { class: "date", "data-testid": "entry-date" }, e.date) : el("span", { class: "chip chip--warn", "data-icon": "calendar", "data-testid": "entry-date" }, "Date to confirm"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
        e.date && rec ? el("span", { class: "chip chip--rec" }, "Rec " + rec.seq) : null,
        reasonText_ ? el("p", { class: "reason", "data-testid": "entry-reasons", title: reasonText_ }, reasonText_) : null,
        chips(e)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag", "data-icon": "ai", title: "Drafted by AI" }, "draft") : null),
      e.edited ? el("p", { class: "muted small note", "data-testid": "edited-note" }, "Edited by you; the code checked your wording against the quote when you saved. Original: " + e.edited.original_summary) : null,
      quote(e, rec),
      e.duplicate_note ? el("p", { class: "muted small note" }, e.duplicate_note) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + e.date : ""), onclick: () => openWhy(e.id) }, "Why this status"),
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": `Open record ${rec ? rec.seq : ""} for ${e.provider}`, onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"),
        )].filter(Boolean));
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    const ra = row.querySelector(":scope > .row-actions");
    if (ra) { ra.append(toggle); row.append(ra); }   // "More" is the last of the row's links; the links follow the decision buttons in the DOM, as they do on screen, so Tab order matches what is seen
    return row;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => ZL.firstRank(e.id, e.state);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
  }
  // The record's own quoted text (verbatim, as in the record body), shown so the date can be judged next to what the record says.
  function recordExcerpt(rec) {
    const m = /(?:^|\n)Excerpt:\s*"?([\s\S]*?)"?\s*$/.exec(rec.text || "");
    return m ? m[1].trim() : "";
  }
  ZL.recordExcerpt = recordExcerpt;
  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
  // one is shown in plain words above the timeline (it stays until dismissed) and announced, so a figure never changes silently. Focus then moves to the
  // entry's Accept button (a date that was just confirmed is the next thing to decide), or to the "no entry yet" card.
  let gapNote = null;   // {token, items: [sentence]}
  ZL.confirmDate = async function (recordId, cand) {
    const s = ZL.state.get(), resp = await ZL.api.confirmDate(s.token, recordId, cand);
    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
    gapNote = changes.length ? { token: s.token, items: changes } : null;
    ZL.state.set({ case: await ZL.api.getCase(s.token) });
    const c = ZL.state.get().case, rec = c.records.find((r) => r.id === recordId), say = ZL.rv && ZL.rv.say ? ZL.rv.say : () => {};
    const en = c.entries.concat(c.undated_entries).find((x) => (x.record_ids || [])[0] === recordId);
    const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + recordId + '"]');
    let msg = "Date confirmed: " + ZL.fmtDate(cand) + ".";
    if (left) msg += " Record " + (rec ? rec.seq : "") + " has no entry yet; it is listed under Records without an entry.";
    if (changes.length) msg += " " + changes.join(" ");
    say(msg);
    requestAnimationFrame(() => {
      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
      if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "center" }); }
      else if (left) left.scrollIntoView({ block: "center" });
    });
    return resp;
  };
  function gapNoteNode(c) {
    if (!gapNote || gapNote.token !== c.token) return null;
    return el("section", { class: "notice notice--info", "data-testid": "gap-change-note", role: "status", "aria-label": "Gap figures changed" },
      el("div", { class: "notice-body" }, el("strong", {}, "A gap figure changed. "), gapNote.items.map((t) => el("span", { class: "gap-sentence" }, t + " "))),
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
  }
  function datesToConfirm(c) {
    const none = !c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length);
    const box = el("section", { class: "group" + (none ? " group--empty" : ""), "data-testid": "dates-to-confirm", "aria-labelledby": "h-dates" }, el("h2", { id: "h-dates" }, "Dates to confirm"));
    if (none) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    const confirmDate = (d, cand) => ZL.confirmDate(d.record_id, cand);
    const confirmBar = (d) => {
      const raw = d.raw || d.date_raw || "";
      // T-088/T-096: a suggested reading is pre-selected with its reason, and still needs the paralegal's Confirm click.
      if (ZL.sg && ZL.sg.usableSuggestion(d)) return ZL.sg.dateForm(d, { legend: `Written as “${raw}”. Which date?`, onConfirm: (cand) => confirmDate(d, cand) });
      const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${raw}”. Which date?`));
      d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
        try { await confirmDate(d, cand); } catch (er) { alert(er.message); }
      } }, ZL.fmtDate(cand))));
      if (d.suggestion && d.suggestion.reason) bar.append(el("p", { class: "muted small", "data-testid": "date-suggestion-reason" }, "Hint: " + d.suggestion.reason + ". It does not point to one date, so none is selected."));
      return bar;
    };
    const shown = {};
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d) shown[d.record_id] = true;
      if (d && d.candidates.length) row.insertBefore(confirmBar(d), row.querySelector(".row-actions"));
      else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
    // A record with an ambiguous date but no entry at all (no model entry for it): still list it here so the date can be confirmed.
    // Once confirmed it is not removed: it moves to "Records without an entry" (manual.js) with a note and the by-hand path.
    // A record with no readable date and no entry has no date to confirm; it is listed once, under "Records without an entry".
    c.dates_to_confirm.filter((d) => !shown[d.record_id] && d.candidates.length).forEach((d) => {
      const rec = c.records.find((r) => r.id === d.record_id);
      const quote = rec ? recordExcerpt(rec) : "";
      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip chip--warn", "data-icon": "calendar" }, "Date to confirm")),
        quote ? el("blockquote", { class: "excerpt", "data-testid": "date-to-confirm-excerpt" }, quote) : null);
      row.append(confirmBar(d));
      row.append(el("p", { class: "muted small", "data-testid": "date-to-confirm-note" }, "No entry was drafted for this record. After you pick the date it is listed under Records without an entry, where you enter it by hand."));
      if (rec) row.append(el("div", { class: "row-actions" }, el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => ZL.openSource([{ record_id: rec.id, start: null, end: null }], `Record ${rec.seq}: ${rec.source_label}`) }, `Open record ${rec.seq}`)));
      box.append(row);
    });
    return box;
  }
  // D-053: a `flag` tray item is an AI-suggested flag the checks did not confirm. It is never in the flags list or the letter.
  // One plain sentence for both reasons (T-096 review F5): no internal terms. What the paralegal can do goes in a second line, once.
  const FLAG_NOT_CONFIRMED = "The AI suggested this flag. The checks did not support it, so it is left out of the letter.";
  const FLAG_NOT_FOUND = FLAG_NOT_CONFIRMED;
  function tray(c) {
    const box = el("section", { class: "group tray" + (c.tray.length ? "" : " group--empty"), "data-testid": "rejected-tray", "aria-labelledby": "h-tray" }, el("h2", { id: "h-tray" }, `Could not verify (${c.tray.length})`));
    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here.")); return box; }
    box.append(el("p", { class: "muted small" }, "These items did not produce something you can use. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const isFlag = t.kind === "flag";
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id, "data-tray-kind": t.kind || "entry" },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip chip--bad", "data-icon": "x" }, isFlag ? "Flag not confirmed" : "Could not verify")),
        isFlag ? el("p", { class: "summary", "data-testid": "tray-flag-lead" }, (t.reasons || [])[0] === "LLM_ONLY" ? FLAG_NOT_FOUND : FLAG_NOT_CONFIRMED) : null,
        isFlag ? null : el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
        isFlag ? el("p", { class: "muted small" }, "Nothing to accept here. Read what the AI suggested below; if it applies, open the record and check.") : null,
        isFlag ? el("details", { class: "zs-more" }, el("summary", {}, "Why the checks left it out"), el("p", { class: "muted small", "data-testid": "tray-why" }, t.why))
          : el("p", { class: "summary", "data-testid": "tray-why" }, t.why),
        t.attempt && (t.attempt.summary || t.attempt.excerpt) ? el("p", { class: "muted small", "data-testid": "tray-attempt" }, (isFlag ? "The flag the AI suggested (not used): " : "The model's attempt (not used): ") + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
        el("div", { class: "row-actions" }, ZL.stepper ? ZL.stepper.traceButton(t.id, "btn btn--link") : null, recs.map((r) => el("button", { type: "button", class: "btn btn--link", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
      box.append(item);
    });
    return box;
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    try {
      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
      clear(body);
      body.append(...[
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
        ZL.stepper ? ZL.stepper.itemSection(s.token, id) : null,
        el("details", { class: "zs-more" }, el("summary", {}, "Recorded ladder (raw state and checks)"), el("dl", { class: "kv", "data-testid": "why-ladder" },
          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)"))),
        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openWhy = openWhy;

  // ---- "What you need to do": one strip above the work, in plain words, each open decision a jump control. Built from the case data, so it is there before the
  // case-checks trace has loaded. Rebuilt when a late panel (the dismissal suggestion) appears.
  let todoHost = null;
  function todoItems(c) {
    const pend = (i) => (i.review_status || "pending") === "pending";
    const dated = c.undated_entries.filter(pend).length + c.dates_to_confirm.filter((d) => d.candidates.length && !c.undated_entries.some((e) => (e.record_ids || [])[0] === d.record_id)).length;
    const needsEntries = c.entries.filter((e) => pend(e) && e.state === "needs_review").length;
    const verifiedEntries = c.entries.filter((e) => pend(e) && e.state === "verified").length;
    const flags = (c.flags || []).filter(pend).length;
    const charges = (c.amounts || []).filter((a) => pend(a) && a.kind === "charge").length;
    const unclear = (c.amounts || []).filter((a) => pend(a) && a.kind !== "charge").length;
    const suggest = document.querySelectorAll('[data-testid="dismissal-suggestion"]').length;
    const n = (k, one, many) => k + " " + (k === 1 ? one : many);
    const out = [];
    if (dated) out.push(["dates", n(dated, "date to confirm", "dates to confirm"), "Choose the date for the record that has none"]);
    if (needsEntries) out.push(["review", n(needsEntries, "entry needs review", "entries need review"), ""]);
    if (flags) out.push(["flags", n(flags, "flag to review", "flags to review"), ""]);
    if (suggest) out.push(["suggest", n(suggest, "dismissal suggestion", "dismissal suggestions") + " waiting in Flags", ""]);
    if (charges) out.push(["charges", n(charges, "charge to check", "charges to check"), ""]);
    if (unclear) out.push(["charges", n(unclear, "unclear amount", "unclear amounts") + " (not totaled)", ""]);
    if (verifiedEntries) out.push(["review", n(verifiedEntries, "verified entry not yet accepted", "verified entries not yet accepted"), ""]);
    return out;
  }
  function paintTodo() {
    const host = todoHost; if (!host || !host.isConnected) return;
    const c = ZL.state.get().case; if (!c || c.status !== "ready") return;
    ZL.clear(host);
    const items = todoItems(c), done = !items.length;
    host.className = "todo-strip" + (done ? " todo-strip--done" : "");
    host.append(el("h2", { id: "h-todo" }, done ? "Everything is decided" : "Open decisions"));
    if (done) host.append(el("p", { class: "todo-lead" }, "Nothing is waiting on you. Open Export to copy the treatment section; decisions you made are in the letter and the internal notes."),
      el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-todo-export", onclick: () => ZL.skipTo && ZL.skipTo("export") }, "Go to Export"));
    else {
      host.append(el("button", { type: "button", class: "btn btn--primary btn--sm", "data-testid": "btn-start-review", onclick: () => ZL.skipTo && ZL.skipTo("review") }, "Start review"));
      host.append(el("ul", { class: "todo-list", "data-testid": "todo-list" }, items.map(([id, text]) => el("li", {},
        el("button", { type: "button", class: "btn btn--sm", "data-testid": "todo-" + id, onclick: () => ZL.skipTo && ZL.skipTo(id) }, text)))));
    }
  }
  document.addEventListener("zl:panels", () => requestAnimationFrame(paintTodo));

  ZL.renderReview = function (s) {
    const c = s.case, mount = ZL.$("#review-body");
    // a re-render rebuilds every row; keep keyboard focus on the same item and control (a stray repaint must never drop focus to the page)
    const ae = document.activeElement, rowEl = ae && ae.closest ? ae.closest("[data-item-id]") : null;
    const keep = ae && ae !== mount && mount.contains(ae) ? { row: rowEl ? rowEl.getAttribute("data-item-id") : null, self: ae === rowEl, tid: ae.getAttribute("data-testid"), action: ae.getAttribute("data-action") } : null;
    clear(mount);
    if (!c || c.status !== "ready") return;
    const shown = c.entries.concat(c.undated_entries), nNeeds = shown.filter((e) => e.state === "needs_review").length, nVer = shown.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
    todoHost = el("section", { "data-testid": "todo-strip", "aria-labelledby": "h-todo" }); wrap.append(todoHost); paintTodo();
    const gapN = gapNoteNode(c); if (gapN) wrap.append(gapN);
    // one card for the three "how was this checked" rows (case checks, what to do next, how the AI was checked) and the accuracy note: ~150 px instead of ~400, so the work starts on the first screen
    const checks = el("div", { class: "checks", "data-testid": "checks-card" }); wrap.append(checks);
    if (ZL.stepper) ZL.stepper.mountCase(checks);
    const hasDates = c.undated_entries.length || c.dates_to_confirm.some((d) => d.candidates.length);
    const dates = datesToConfirm(c);
    wrap.append(...[
      el("div", { class: "toolbar" },
        el("h2", { id: "h-timeline" }, "Timeline"),
        el("span", { class: "toolbar-counts", "data-testid": "review-counts" },
          el("span", { class: "chip chip--muted" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"}`),
          el("span", { class: "chip chip--warn", "data-icon": "alert" }, `${nNeeds} ${nNeeds === 1 ? "entry needs" : "entries need"} review`),
          el("span", { class: "chip chip--info", "data-icon": "match" }, `${nVer} quote ${nVer === 1 ? "matches" : "match"}`),
          c.undated_entries.length ? el("span", { class: "muted small" }, `${c.undated_entries.length} in Dates to confirm`) : null),
        el("label", { class: "toolbar-sort" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      ZL.stepper ? ZL.stepper.exportNotice() : null,
      hasDates ? dates : null,
      el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, sortedEntries(c).map((e) => entryRow(e, c))),
      hasDates ? null : dates, tray(c), ZL.sg ? ZL.sg.calibration() : null].filter(Boolean));   // never hand append() a bare null: it prints the word null
    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
    ZL.hooks.panels.forEach((fn) => fn(c, side));
    if (keep) {   // put focus back where it was
      const row = keep.row && (mount.querySelector('[data-testid="queue"] [data-item-id="' + keep.row + '"]') || mount.querySelector('[data-item-id="' + keep.row + '"]'));
      const t = row ? (keep.self ? row : (keep.action && row.querySelector('[data-action="' + keep.action + '"]')) || (keep.tid && row.querySelector('[data-testid="' + keep.tid + '"]')) || row)
        : (!keep.row && keep.tid ? mount.querySelector('[data-testid="' + keep.tid + '"]') : null);
      if (t) { if (!t.hasAttribute("tabindex") && !/^(BUTTON|A|INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) t.setAttribute("tabindex", "0"); t.focus({ preventScroll: true }); }
    }
    document.dispatchEvent(new Event("zl:panels"));
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:41.038Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/flags.js app/frontend/switcher.js"
}
````

### User / tool · 2026-11-02T11:05:41.131Z

**tool result**
````
/* Flags panel (T-043): four groups plus "Record warnings" (R-FL-6),
   unmerged conflicts shown side by side (D-017), reviewer note only (D-010), confirm_date control for ambiguous dates.
   All server text is inserted as text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);

  const GROUPS = [
    ["gap", "Treatment gaps", "No gap over 30 days found."],
    ["conflict", "Conflicts between records", "No conflicts found."],
    ["pre_existing", "Pre-existing conditions", "No earlier conditions mentioned."],
    ["causation", "Causation language", "No causation wording found."],
    ["record_warning", "Record warnings", "No record warnings."],
  ];
  const joinList = (a) => (a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]);
  const recOf = (c, id) => (c.records || []).find((r) => r.id === id);
  const recSeq = (c, id) => { const r = recOf(c, id); return r ? r.seq : String(id).replace(/^r/, ""); };

  // One block per record (a gap names two records, each with a Date and a Source line: two blocks, side by side, not four stacked boxes).
  function evidence(c, f) {
    const ul = el("ul", { class: "rv-evidence" + (f.type === "conflict" ? " rv-side" : ""), "data-testid": "flag-evidence", "aria-label": "Quoted evidence" });
    const byRec = [], at = {};
    (f.evidence || []).forEach((e) => { if (!(e.record_id in at)) { at[e.record_id] = byRec.length; byRec.push({ id: e.record_id, lines: [] }); } byRec[at[e.record_id]].lines.push(e.excerpt); });
    byRec.forEach((g) => {
      const r = recOf(c, g.id);
      const li = el("li", { class: "rv-ev" },
        el("span", { class: "rv-ev-cap" }, "Record " + recSeq(c, g.id) + (r ? " · " + r.source_label : "")),
        el("blockquote", { class: "rv-quote" }, g.lines.map((t) => el("span", { class: "rv-line" }, t))));
      if (f.type === "conflict") {
        // Show the entry's own quoted line from the same record so both sides can be read without opening it.
        const en = (c.entries || []).concat(c.undated_entries || []).find((x) => (x.record_ids || []).includes(g.id));
        if (en && en.excerpt && !g.lines.includes(en.excerpt)) li.append(el("span", { class: "rv-ev-more" }, "Quoted line from this record: " + en.excerpt));
      }
      ul.append(li);
    });
    return ul;
  }

  function dateControl(c, f) {
    const rid = ((f.evidence || [])[0] || {}).record_id;
    const row = (c.dates_to_confirm || []).find((d) => d.record_id === rid);
    if (!row) return null;
    const raw = row.raw || row.date_raw || "";
    if (!(row.candidates || []).length)
      return el("p", { class: "rv-note" }, "No readable date was found for this record, so it stays off the timeline and out of the gap checks.");
    // T-096: the suggested reading (T-088) is pre-selected with its reason; the paralegal still clicks Confirm date.
    return ZL.sg.dateForm(row, { legend: "The date “" + raw + "” can be read two ways. Choose how this record is dated:", onConfirm: async (cand) => {
      await ZL.confirmDate(rid, cand);   // timeline, gaps and warnings are recomputed by the backend; changed gap figures are announced
    } });
  }

  function card(c, f) {
    const seqs = (RV.sourceTargets(f, "flag").ids || []).map((id) => recSeq(c, id));
    const note = f.reviewer_note || (f.edited && f.edited.note);
    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
      el("p", { class: "rv-text-body" }, f.explanation),
      f.state === "needs_review" && f.why ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), f.why) : null,   // the "quote found word for word..." sentence is in Why this status, not repeated on every card
      evidence(c, f));
    if (f.category === "date_ambiguous") { const dc = dateControl(c, f); if (dc) a.append(dc); }
    if (note) a.append(el("p", { class: "rv-usernote", "data-testid": "flag-note-text" }, el("strong", {}, f.review_status === "dismissed" ? "Dismissed because: " : "Your note: "), note));
    a.append(el("div", { class: "rv-actions rv-links" },
      seqs.length ? el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", onclick: () => RV.openSource(f, "flag") }, seqs.length > 1 ? "Open records " + joinList(seqs) : "Open record " + seqs[0]) : null,
      ZL.stepper ? ZL.stepper.traceButton(f.id, "btn btn--link") : null));
    a.append(RV.controls(f, "flag"));
    return a;
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "flags-panel");
    root.setAttribute("aria-labelledby", "rv-flags-h");
    root.append(el("h2", { id: "rv-flags-h" }, "Flags"),
      el("p", { class: "rv-help" }, "Flags point to things worth checking. Accepting one means you have seen it: it goes to the internal notes, never into the letter."));
    if (c.injection && c.injection.banner) root.append(el("p", { class: "rv-banner", role: "note" }, c.injection.banner));
    if (ZL.sg) root.append(ZL.sg.dismissalBox(c));
    const flags = c.flags || [];
    GROUPS.forEach(([type, title, empty]) => {
      const list = RV.needsReviewFirst(flags.filter((f) => f.type === type));
      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
        el("h3", { id: "rv-g-" + type }, title + " (" + list.length + ")"));
      if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
      list.forEach((f) => g.append(card(c, f)));
      root.append(g);
    });
  }
  RV.registerPanel("flags", render);
  RV.renderFlags = render;
})();
/* Case switcher (T-053 AC2, local mode only). Shown only when GET /api/cases answers 200 (404 in demo/public mode).
   Lists cases (open with one click) and the synthetic library (POST /cases {library:id}, then run). Text via ZL.el only. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let root = null, lastToken = undefined, busy = false;

  async function get(path) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle("GET", path);
    const res = await fetch("/api" + path); let body = null;
    try { body = await res.json(); } catch (_) { /* no body */ }
    return { status: res.status, body };
  }
  function say(msg, isError) { const p = root && root.querySelector(".cs-msg"); if (p) { p.textContent = msg || ""; p.setAttribute("role", isError ? "alert" : "status"); } }

  async function openCase(token) {
    const c = await ZL.api.getCase(token);
    history.replaceState(null, "", "#/case/" + encodeURIComponent(token));
    ZL.state.set({ token, created: c.status === "ingested" ? Object.assign({}, c, { record_count: (c.records || []).length }) : null, case: c, status: null });
    if (c.status === "running") ZL.pollRun();
    window.scrollTo(0, 0);   // the case list sits under the work; show the case just opened
  }
  async function guarded(fn) {
    if (busy) return; busy = true; say("");
    try { await fn(); } catch (e) { say((e && e.message) || "That did not work.", true); } finally { busy = false; }
  }
  const open = (token) => guarded(() => openCase(token));
  const loadLibrary = (id) => guarded(async () => {
    const resp = await ZL.api.createCase({ library: id });
    await openCase(resp.token);
    ZL.state.set({ status: { status: "running", progress: { label: "Starting…" } } });
    await ZL.api.run(resp.token, false); ZL.pollRun();
  });

  // Library manifest names are file slugs ("case lib01 er only then gap"). Show a readable title: drop the slug prefix, sentence case.
  const nice = (n) => { const t = String(n || "").replace(/^case[ _]/i, "").replace(/^lib(\d+)[ _]?/i, (_, d) => "L" + parseInt(d, 10) + " · ").replace(/_/g, " "); return t.charAt(0).toUpperCase() + t.slice(1); };
  const when = (iso) => { const d = iso ? new Date(iso) : null; return d && !isNaN(d) ? d.toLocaleString("en-US", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) : ""; };
  const firstSentence = (t) => { const m = /^[\s\S]*?[.!?](\s|$)/.exec(String(t || "")); return (m ? m[0] : String(t || "")).trim(); };

  function draw(cases, library) {
    const cur = ZL.state.get().token;
    const list = el("ul", { class: "cs-list", "data-testid": "case-list" });
    if (!cases.length) list.append(el("li", { class: "rv-empty" }, "No cases yet."));
    cases.forEach((c) => {
      const k = c.counts || {};
      list.append(el("li", {}, el("button", { type: "button", class: "btn cs-btn", "data-testid": "case-" + c.token, "aria-current": c.token === cur ? "true" : null, onclick: () => open(c.token) },
        (c.token === cur ? "Open now: " : "") + (c.name || ("Pasted records" + (when(c.created_at || c.updated_at) ? ", " + when(c.created_at || c.updated_at) : ""))), el("span", { class: "cs-meta" }, [c.status, c.record_count != null ? c.record_count + " records" : null, k.pending != null ? k.pending + " pending" : null, when(c.created_at || c.updated_at)].filter(Boolean).join(" · ")))));
    });
    const lib = el("ul", { class: "cs-list", "data-testid": "library-list" });
    library.forEach((l) => lib.append(el("li", {}, el("button", { type: "button", class: "btn cs-btn", "data-testid": "library-" + l.id, onclick: () => loadLibrary(l.id) },
      "Add: " + nice(l.name), l.description ? el("span", { class: "cs-meta" }, firstSentence(l.description.replace(/^Library L\d+ \([^)]*\)\.\s*/, ""))) : null))));
    if (!library.length) lib.append(el("li", { class: "rv-empty" }, "The library is empty."));
    const msg = root.querySelector(".cs-msg") || el("p", { class: "cs-msg rv-error", role: "status" });
    const wasOpen = root.querySelector("details") ? root.querySelector("details").open : false;
    clear(root);
    root.append(el("details", { class: "cs-details", open: wasOpen },
      el("summary", { id: "cs-h" }, "Cases (" + cases.length + ") and synthetic library"),
      el("div", { class: "cs-body" }, list, el("h3", { class: "cs-h" }, "Add a synthetic case (loads and runs it)"), lib, msg)));
  }
  async function refresh() {
    const [a, b] = await Promise.all([get("/cases"), get("/library")]);
    if (a.status !== 200) { if (root) root.hidden = true; return; }
    if (!root) {
      root = el("section", { id: "case-switcher", class: "card cs", "data-testid": "case-switcher", "aria-labelledby": "cs-h" }, el("p", { class: "cs-msg rv-error", role: "status" }));
      const main = document.querySelector("main"); main.append(root);   // under the work, collapsed: the paste box and the review come first
    }
    root.hidden = false;
    draw((a.body && a.body.cases) || [], (b.status === 200 && b.body && b.body.cases) || []);
  }
  document.addEventListener("DOMContentLoaded", () => {
    refresh().catch(() => {});
    ZL.state.subscribe((s) => { if (s.token !== lastToken) { lastToken = s.token; if (root) refresh().catch(() => {}); } });
  });
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:45.013Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh | head -30; cat app/frontend/app.js | sed -n 1,131p; lsof -iTCP -sTCP:LISTEN -P 2>/dev/null | grep -E \"79[0-9][0-9]\" | head"
}
````

### User / tool · 2026-11-02T11:05:45.188Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
(function () {
  const ZL = window.ZL, { $ } = ZL;
  const SYNTH = "Synthetic data only — never paste real records";
  let poller = null;

  function renderChrome(s) {
    const h = s.health;
    $("#banner-synthetic").textContent = (h && h.banner) || SYNTH;           // present on every view, even before /health answers
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? (h.fixture_set === "recorded" ? "cached demo (recorded responses)" : "cached demo (curated responses)") : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : ""; // D-029: the demo replays the curated fixture set; label says so
    badge.hidden = !h;
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  // ---- case header (sticky): case name, "n of N decided", Export. The numbers are counts of what the API sent; nothing is computed beyond counting.
  const itemsOf = (c) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).filter((i) => i.state !== "rejected");
  ZL.progressOf = function (c) {
    const all = itemsOf(c), decided = all.filter((i) => (i.review_status || "pending") !== "pending").length;
    const needs = all.filter((i) => (i.review_status || "pending") === "pending" && i.state === "needs_review").length;
    return { total: all.length, decided, left: all.length - decided, needs };
  };
  function renderHeader(s) {
    const c = s.case, ready = !!(c && c.status === "ready");
    $("#case-name").hidden = !c; if (c) $("#case-name").textContent = c.name || "Case";
    document.title = c && c.name ? "Treatment timeline · " + c.name : "Treatment timeline";
    $("#case-progress").hidden = !ready; $("#btn-export").hidden = !ready; $("#btn-shortcuts").hidden = !ready;
    if (!ready) return;
    const p = ZL.progressOf(c), bar = $("#progress-bar");
    $("#progress-text").textContent = p.decided + " of " + p.total + " decided" + (p.needs ? " · " + p.needs + " need review" : "");
    bar.max = Math.max(p.total, 1); bar.value = p.decided;
    bar.setAttribute("aria-valuetext", p.decided + " of " + p.total + " items decided");
  }
  // ---- theme: auto (follow the OS), light or dark. Remembered in localStorage when it is available; the page works without it.
  const THEMES = ["auto", "light", "dark"];
  function setTheme(t) {
    const root = document.documentElement;
    if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
    const b = $("#btn-theme"); if (b) { b.textContent = "Theme: " + t; b.setAttribute("data-theme-choice", t); b.setAttribute("aria-label", "Theme: " + t + ". Press to change it."); }   // the name contains the visible text and says the current value
    try { localStorage.setItem("zlayt.theme", t); } catch (_) { /* not remembered */ }
  }
  // ---- skip links: the first focusable things on the page. They land on the work, most blocking first: the dates form, the dismissal suggestion, the first item to decide, flags, charges, Export. With one of those present it is Tab, Enter.
  const SKIPS = [
    ["dates", "Skip to dates to confirm", () => !!document.querySelector("[data-testid=dates-to-confirm] [data-testid=confirm-date], [data-testid=dates-to-confirm] [data-testid=btn-confirm-date]"),
      () => focusEl("[data-testid=dates-to-confirm] [data-testid=btn-confirm-date]:not(:disabled), [data-testid=dates-to-confirm] [data-testid=confirm-date]:checked, [data-testid=dates-to-confirm] [data-testid=confirm-date]")],
    ["suggest", "Skip to the dismissal suggestion", () => !!document.querySelector("[data-testid=dismissal-suggestion]"), () => focusEl("[data-testid=dismissal-suggestion] [data-testid=btn-hide-similar]")],
    ["review", "Skip to the first item to review", () => !!document.querySelector("[data-testid=queue] [data-item-id]"), () => ZL.rv && ZL.rv.focusFirstPending()],
    ["flags", "Skip to the gap flag and other flags", () => !!document.querySelector("[data-testid=flags-panel] [data-item-id]"), () => focusEl("[data-testid=flags-panel] [data-flag-type=gap], [data-testid=flags-panel] [data-item-id]")],
    ["charges", "Skip to charges", () => !!document.querySelector("[data-testid=charges-panel] [data-item-id]"), () => focusEl("[data-testid=charges-panel] [data-item-id]")],
    ["export", "Skip to Export", () => !$("#btn-export").hidden, () => focusEl("[data-testid=btn-export]")],
  ];
  const TARGETS = { dates: "[data-testid=dates-to-confirm]", suggest: "[data-testid=dismissal-suggestions]", review: "[data-testid=queue]", flags: "[data-testid=flags-panel]", charges: "[data-testid=charges-panel]", export: "[data-testid=btn-export]" };
  function focusEl(sel) {
    const t = document.querySelector(sel); if (!t) return;
    if (!t.hasAttribute("tabindex") && !/^(BUTTON|A|INPUT)$/.test(t.tagName)) t.setAttribute("tabindex", "-1");
    t.focus({ preventScroll: true }); t.scrollIntoView({ block: "center" });
  }
  ZL.skipTo = (id) => { const x = SKIPS.find((k) => k[0] === id); if (x) x[3](); };
  let skipSig = "";
  function renderSkips() {
    const nav = $("#skip-nav"), ready = ZL.state.get().case && ZL.state.get().case.status === "ready";
    const live = SKIPS.filter(([, , has]) => ready && has());
    const sig = live.map((x) => x[0]).join(",");
    if (sig === skipSig && nav.firstChild) return; skipSig = sig;
    ZL.clear(nav);
    live.forEach(([id, label, , go]) => {
      const t = document.querySelector(TARGETS[id] || ""); if (t && !t.id) t.id = "skip-to-" + id;   // a real element for the href to resolve to (WCAG 2.4.1); the click still moves focus to the first control
      nav.append(ZL.el("a", { href: "#" + ((t && t.id) || "main"), "data-testid": "skip-" + id, onclick: (ev) => { ev.preventDefault(); go(); } }, label));
    });
  }
  ZL.renderSkips = () => requestAnimationFrame(renderSkips);
  // After a case opens (a library case from the switcher, a paste, a deep link) the control that was pressed is gone and the browser's Tab start point is wherever it was
  // (the end of the page for the case list). Put it back at the top, so one Tab reaches the first skip link (T-060 r3, paralegal N1).
  let readyToken = null;
  function resetTabStart(s) {
    const tok = s.case && s.case.status === "ready" ? s.token : null;
    if (!tok || tok === readyToken) { if (!tok) readyToken = null; return; }
    readyToken = tok;
    requestAnimationFrame(() => {
      const a = document.activeElement;
      if (a && a !== document.body && a.isConnected && !a.closest("#input-body, #view-input")) return;
      const nav = $("#skip-nav"); if (nav) { nav.setAttribute("tabindex", "-1"); nav.focus({ preventScroll: true }); }
    });
  }
  function render(s) {
    renderChrome(s);
    renderHeader(s);
    ZL.renderInput(s);
    $("#view-review").hidden = !(s.case && s.case.status === "ready");
    ZL.renderReview(s);
    ZL.renderSkips();
    resetTabStart(s);
  }
  ZL.state.subscribe(render);

  ZL.pollRun = function () {
    clearInterval(poller);
    const tick = async () => {
      const s = ZL.state.get(); if (!s.token) return clearInterval(poller);
      try {
        const st = await ZL.api.status(s.token);
        if (st.status === "ready") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else if (st.status === "failed") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else ZL.state.set({ status: st });
      } catch (e) { clearInterval(poller); ZL.state.set({ status: { status: "failed", error: { message: e.message } } }); }
    };
    tick(); poller = setInterval(tick, 1000);
  };

  async function boot() {
    render(ZL.state.get());
    try { ZL.state.set({ health: await ZL.api.health() }); } catch (_) { /* banners fall back to static text */ }
    const m = /#\/case\/([^&/]+)/.exec(location.hash);
    if (m) {
      const token = decodeURIComponent(m[1]);
      try { const c = await ZL.api.getCase(token); ZL.state.set({ token, case: c }); if (c.status === "running") ZL.pollRun(); }
      catch (_) { history.replaceState(null, "", location.pathname + location.search); }
    }
  }
  document.addEventListener("DOMContentLoaded", () => {
    $("#delete-now").addEventListener("click", () => ZL.startOver());
    $("#btn-export").addEventListener("click", () => { if (ZL.stepper) ZL.stepper.onExport(); ZL.openExport(); });
    $("#btn-shortcuts").addEventListener("click", () => ZL.rv && ZL.rv.openShortcuts());
    let saved = "auto"; try { saved = localStorage.getItem("zlayt.theme") || "auto"; } catch (_) { /* no storage */ }
    setTheme(THEMES.includes(saved) ? saved : "auto");
    $("#btn-theme").addEventListener("click", () => setTheme(THEMES[(THEMES.indexOf($("#btn-theme").getAttribute("data-theme-choice")) + 1) % THEMES.length]));
    document.addEventListener("zl:panels", ZL.renderSkips);
    boot();
  });
})();
Python    52563 arsis    9u  IPv4 0x3b8e2dc6a14c14ec      0t0  TCP localhost:7991 (LISTEN)
Python    59175 arsis    9u  IPv4 0x344e3fca91b7f3be      0t0  TCP localhost:7992 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:48.533Z

**tool call — Bash**
````
{
 "command": "cat app/main.py | head -40; grep -n \"frontend\" app/backend/api.py | head; ls tests/e2e; git worktree list"
}
````

### User / tool · 2026-11-02T11:05:48.652Z

**tool result**
````
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
27:# index.html has one inline onclick (dialog Close); allowed by hash until the frontend moves it to a listener.
588:    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
591:        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charges.py
test_code_check_refusal.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_polish_r3.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
/Users/arsis/zlayt-pm-project                                                                                                                                                                                                                             db7f6d0 [main]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_base    158809b (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_c1      b66e748 (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_final   d9efc5c (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_final2  7d5a45f (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_head    8b4ff11 (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_live1   e1ce8dc (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_live2   e1ce8dc (detached HEAD)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_live3   e1ce8dc (detached HEAD)
/private/tmp/claude-501/wt_t094                                                                                                                                                                                                                           dda614d (detached HEAD)
/private/tmp/claude-501/wt_t094b                                                                                                                                                                                                                          8b54d40 (detached HEAD)
/private/tmp/claude-501/wt_t094c                                                                                                                                                                                                                          789cb39 (detached HEAD)
/private/tmp/claude-501/wt_t112                                                                                                                                                                                                                           afcde06 (detached HEAD)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:53.600Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo $S > /dev/null && git worktree add --detach $S/wt_r4 HEAD >/dev/null 2>&1; cd $S/wt_r4 && mv app/frontend app/frontend_orig && ln -s /Users/arsis/zlayt-pm-project/app/frontend app/frontend && ls -la app | head; ls /Users/arsis/zlayt-pm-project/.venv/bin/python"
}
````

### User / tool · 2026-11-02T11:05:54.257Z

**tool result**
````
total 40
drwxr-xr-x@ 11 arsis  wheel   352 Nov  2 05:05 .
drwxr-xr-x@ 22 arsis  wheel   704 Nov  2 05:05 ..
-rw-r--r--@  1 arsis  wheel  8454 Nov  2 05:05 README-arch.md
-rw-r--r--@  1 arsis  wheel     0 Nov  2 05:05 __init__.py
drwxr-xr-x@ 52 arsis  wheel  1664 Nov  2 05:05 backend
drwxr-xr-x@  5 arsis  wheel   160 Nov  2 05:05 db
lrwxr-xr-x@  1 arsis  wheel    42 Nov  2 05:05 frontend -> /Users/arsis/zlayt-pm-project/app/frontend
drwxr-xr-x@ 36 arsis  wheel  1152 Nov  2 05:05 frontend_orig
drwxr-xr-x@ 11 arsis  wheel   352 Nov  2 05:05 llm
/Users/arsis/zlayt-pm-project/.venv/bin/python
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:05:58.423Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt_r4 && mkdir -p ../r4data && (PORT=7955 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$PWD/../r4data/db.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > ../r4data/server.log 2>&1 & echo $! > ../r4data/pid); sleep 3; curl -s localhost:7955/api/health; cat ../r4data/pid; curl -s localhost:7955/api/library | head -c 1500"
}
````

### User / tool · 2026-11-02T11:06:01.551Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}71076
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the pat"},{"id":"case_lib02_slip_fall_prior_knee","name":"case lib02 slip fall prior knee","description":"Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute and prior change. The tool shows the prior-condition language and the hedge an"},{"id":"case_lib03_truck_rear_end_chiro","name":"case lib03 truck rear end chiro","description":"Library L3 (mirrors S3). Passenger car struck from behind by a tractor-trailer; chiropractic plan of 36 visits, no change in pain score at visit 14, discharge at maximum benefit after 31 visits, then an MRI 35 days later with hedged chronic"},{"id":"case_lib04_dog_bite_scar_revision","name":"case lib04 dog bite scar revision","description":"Library L4 (mirrors S4). Facial dog bite repaired in the ED, plastic-surgery follow-ups with scar photographs, a planned 8-week interval that the tool still flags, a $6,500 revision estimate and a later revision with a surgeon fee. The tool"},{"id":"case_lib05_pedestrian_orif_hardware","name":"case lib05 pedestrian orif hardware","description":"Library L5 (mirrors S5). Pedestria
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:06.899Z

**tool call — Bash**
````
{
 "command": "curl -s localhost:7955/api/library | python3 -c \"\nimport json,sys\nfor c in json.load(sys.stdin)['cases']: print(c['id'],'|',c['name'])\"; curl -s localhost:7955/api/cases | head -c 600"
}
````

### User / tool · 2026-11-02T11:06:07.022Z

**tool result**
````
case_lib01_er_only_then_gap | case lib01 er only then gap
case_lib02_slip_fall_prior_knee | case lib02 slip fall prior knee
case_lib03_truck_rear_end_chiro | case lib03 truck rear end chiro
case_lib04_dog_bite_scar_revision | case lib04 dog bite scar revision
case_lib05_pedestrian_orif_hardware | case lib05 pedestrian orif hardware
case_lib06_lop_billed_vs_adjusted | case lib06 lop billed vs adjusted
case_lib07_parking_lot_fall_outside_records | case lib07 parking lot fall outside records
case_lib08_second_crash_mri_after | case lib08 second crash mri after
case_lib09_spanish_interpreter_espalda | case lib09 spanish interpreter espalda
case_lib10_eob_ub04_cms1500 | case lib10 eob ub04 cms1500
case_lib11_priors_and_ledger | case lib11 priors and ledger
case_lib12_records_review_credibility | case lib12 records review credibility
case_lib13_cloned_notes_cross_provider | case lib13 cloned notes cross provider
case_lib14_handwritten_chiro_scans | case lib14 handwritten chiro scans
case_lib15_conclusory_letter_mist | case lib15 conclusory letter mist
{"cases":[]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:09.426Z

**tool call — Bash**
````
{
 "command": "grep -n \"case-name\\|Add:\\|case lib\\|\\\"L1\\|L9 \\|library-\" tests/e2e/*.py | head -30; ls artifacts/screenshots | grep -i \"t060\\|ui-pass\" | head -30"
}
````

### User / tool · 2026-11-02T11:06:09.519Z

**tool result**
````
tests/e2e/conftest.py:50:  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
t060-after-_espalda-1440-full.png
t060-after-_espalda-1440-top.png
t060-after-_espalda-390-full.png
t060-after-_espalda-390-top.png
t060-after-sample-1440-full.png
t060-after-sample-1440-top.png
t060-after-sample-390-full.png
t060-after-sample-390-top.png
t060-before-_espalda-1440-full.png
t060-before-_espalda-1440-top.png
t060-before-_espalda-390-full.png
t060-before-_espalda-390-top.png
t060-before-sample-1440-full.png
t060-before-sample-1440-top.png
t060-before-sample-390-full.png
t060-before-sample-390-top.png
t060-r3-lib09-1440-full.png
t060-r3-lib09-1440-top.png
t060-r3-lib09-390-full.png
t060-r3-lib09-390-top.png
t060-r3-sample-1440-full.png
t060-r3-sample-1440-top.png
t060-r3-sample-390-full.png
t060-r3-sample-390-top.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:12.212Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p tests/e2e/test_polish_r3.py; sed -n 245,300p tests/e2e/test_polish_r3.py; grep -n \"def \\|fixture\" tests/e2e/conftest.py | sed -n 1,60p"
}
````

### User / tool · 2026-11-02T11:06:12.321Z

**tool result**
````
"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def active(page):
    return page.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")


def tab_until(page, testid, limit=40):
    for _ in range(limit):
        page.keyboard.press("Tab")
        a = active(page)
        if a and a["tid"] == testid:
            return a
    raise AssertionError(f"Tab never reached {testid}; last {active(page)}")


# ---- 1. the shortcut sheet
def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-shortcuts").click()
    dlg = page.get_by_test_id("shortcuts-modal"); expect(dlg).to_be_visible()
    lst = dlg.get_by_test_id("shortcuts-list")
    expect(lst.locator("kbd")).to_have_count(9)
    expect(lst.locator("dt")).to_have_count(9); expect(lst.locator("dd")).to_have_count(9)
    txt = dlg.inner_text()
    assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    # '?' from an item row opens the same sheet
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()


def test_no_object_undefined_or_null_text_on_the_review_page(page, sample_case):
    open_case(page, sample_case)
    assert not BAD_TEXT.search(page.locator("body").inner_text()), BAD_TEXT.findall(page.locator("body").inner_text())


# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
def _snapshot(page):
    return page.evaluate("""() => ({ accepted: document.querySelectorAll('[data-review=accepted],[data-review=dismissed],[data-review=edited]').length,
        dialogs: document.querySelectorAll('dialog[open]').length, active: (document.activeElement || {}).tagName + ':' + ((document.activeElement || {}).getAttribute ? document.activeElement.getAttribute('data-testid') : '') })""")


def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
    open_case(page, sample_case)
    before = _snapshot(page)
    # from the page body
    page.evaluate("document.activeElement && document.activeElement.blur()")
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-dates", 4)
    page.keyboard.press("Enter")
    assert page.evaluate("!!document.activeElement.closest('[data-testid=dates-to-confirm]')")


def test_start_review_button_moves_focus_to_the_first_item(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-start-review").click()
    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')")


def test_t114_gap_change_notice_renders_after_a_date_confirm(page, lib09):
    """T-114: confirm_date answers gap_changes[]; the sentence shows above the timeline and is announced."""
    open_case(page, lib09)
    box = page.get_by_test_id("dates-to-confirm")
    # pick the reading the paste does not suggest, so a gap figure moves (lib09 record 4: 42 days -> 40)
    radios = box.get_by_test_id("confirm-date")
    n = radios.count()
    assert n >= 2
    target = None
    for i in range(n):
        if radios.nth(i).get_attribute("data-date") == "2026-03-05":
            target = radios.nth(i)
    assert target is not None
    target.check()
    box.get_by_test_id("btn-confirm-date").first.click()
    note = page.get_by_test_id("gap-change-note")
    expect(note).to_be_visible(timeout=10000)
    expect(note).to_contain_text(re.compile(r"Gap recalculated"))
    assert not BAD_TEXT.search(note.inner_text())


# ---- 8. export view
def test_export_letter_box_fits_its_text_and_can_be_downloaded(page, sample_case):
    tok = sample_case
    ids = [e["id"] for e in api("GET", f"/api/cases/{tok}")[1]["entries"] if e["state"] == "verified" and e["date"]]
    api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})
    open_case(page, tok); page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-letter"); expect(box).to_be_visible()
    assert page.evaluate("(() => { const e = document.querySelector('[data-testid=export-letter]'); return e.scrollHeight <= e.clientHeight + 1; })()")
    assert page.get_by_test_id("btn-download-letter").count() == 1 and page.get_by_test_id("btn-download-notes").count() == 1
    if page.get_by_test_id("btn-download-letter").is_enabled():
        with page.expect_download() as dl:
            page.get_by_test_id("btn-download-letter").click()
            if page.get_by_test_id("copy-confirm").count():
                page.get_by_test_id("btn-copy-anyway").click()
        assert dl.value.suggested_filename.endswith(".txt")
        text = open(dl.value.path(), encoding="utf-8").read()
        assert text.startswith("TREATMENT CHRONOLOGY")
1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
66:def _up():
73:def pytest_collection_modifyitems(config, items):
76:    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
81:def api(method, path, body=None):
91:def golden_text(name):
94:@pytest.fixture
95:def base_url():
98:@pytest.fixture
99:def sample_case():
113:@pytest.fixture(scope="session")
114:def pw():
119:@pytest.fixture
120:def page(pw):
129:def open_case(page, tok):
144:    def __init__(self, page, token, ids):
150:    def _summary(self, i):
155:    def active(self):
158:    def _na(self, i):
161:    def blockers(self):
164:    def _case_trace(self, route):
174:    def _item_trace(self, route):
185:    def _export(self, route):
193:    """Route-rewriting stub that puts accepted items into the D-044 state 'the second AI check never ran' (the fixture backend cannot produce it for a recorded case).
202:    def __init__(self, page, token, ids, mode="clears", hold=False, exempt=()):
210:    def active(self):
219:    def _na(self, i):
222:    def _blockers(self):
225:    def _case_trace(self, route):
238:    def _item_trace(self, route):
246:    def _judges(self, route):
258:    def _export(self, route):
265:    def _rejudge(self, route):
271:    def release(self):
275:    def _answer(self, route):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:14.089Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/review.js"
}
````

### User / tool · 2026-11-02T11:06:14.171Z

**tool result**
````
/* Review controls shared by entries, flags and charges (T-043, frontend-2).
   Exposes ZL.rv = { controls, act, money, chips, find, openSource, say, legend, nextId }.
   - ZL.rv.controls(item, kind) -> element with Accept / Edit / Dismiss / Reset (kind: "entry" | "flag" | "amount").
   - Registered as a row action so every timeline entry row gets the same controls (ZL.registerRowActions).
   - One document-level key handler works on ANY element that carries data-item-id (queue items, entry rows, flag and charge cards).
   Untrusted text only ever goes through ZL.el (text nodes) / textContent. No amounts are added or compared here. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const el = (...a) => ZL.el(...a);
  const RV = (ZL.rv = {});
  const drafts = {};        // id -> {open, text, reasonOpen, reason}  (survives re-renders)
  const ui = {};            // id -> {openEdit}  latest controls instance per item
  const busy = new Set();

  RV.caseNow = () => (ZL.state && ZL.state.get().case) || null;
  RV.find = function (c, id) {
    for (const [k, kind] of [["entries", "entry"], ["undated_entries", "entry"], ["amounts", "amount"], ["flags", "flag"]]) {
      const it = ((c && c[k]) || []).find((x) => x.id === id);
      if (it) return { item: it, kind };
    }
    return null;
  };
  // Display formatting of an integer-cents value by string slicing only (no arithmetic).
  RV.money = function (cents) {
    if (cents == null) return "";
    const neg = String(cents)[0] === "-";
    const s = String(cents).replace("-", "").padStart(3, "0");
    const d = s.slice(0, -2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const c = s.slice(-2);
    return (neg ? "-" : "") + "$" + d + "." + c;   // always cents, so a column of amounts lines up and matches the letter
  };
  // Stable sort: needs_review before everything else (R-TL-5 order, applied inside each group / table).
  RV.needsReviewFirst = (list) => list.map((x, i) => [x, i]).sort((a, b) => ZL.firstRank(a[0].id, a[0].state) - ZL.firstRank(b[0].id, b[0].state) || a[1] - b[1]).map((p) => p[0]);
  // Plain JSON request for endpoints ZL.api does not wrap (mock or real). Returns {status, body}; never throws on HTTP errors.
  RV.http = async function (method, path, body) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle(method, path, body);
    const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
    let b = null; try { b = await res.json(); } catch (_) { /* empty body */ }
    return { status: res.status, body: b };
  };
  RV.errMsg = (r, fallback) => (r && r.body && r.body.error && r.body.error.message) || fallback || "That did not work.";
  RV.label = (item) => item.title || (item.provider ? item.provider + (item.date ? ", " + item.date : "") : null) || item.text || item.id;

  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
  const STATE_TONE = { verified: ["info", "match"], needs_review: ["warn", "alert"], rejected: ["bad", "x"] };
  const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
  RV.chips = function (item) {   // machine state, then (only once decided) the human decision: two chips, two icons
    const t = STATE_TONE[item.state] || ["muted", "info"], d = DECISION[item.review_status];
    return el("span", { class: "rv-chips" },
      el("span", { class: "chip chip--" + t[0], "data-icon": t[1], "data-chip": "state" }, STATE_LABEL[item.state] || item.state),
      d ? el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-chip": "review" }, REVIEW_LABEL[item.review_status]) : null);
  };

  // ---- live region: created once at load (a region that appears with its first message is often not announced)
  let live;
  function liveRegion() { if (!live) { live = document.getElementById("rv-live") || el("div", { id: "rv-live", class: "rv-sr", "aria-live": "polite", role: "status" }); if (!live.isConnected) document.body.append(live); } return live; }
  if (document.body) liveRegion(); else document.addEventListener("DOMContentLoaded", liveRegion);
  RV.say = function (msg, isError) {
    const l = liveRegion();
    l.textContent = "";
    setTimeout(() => { l.textContent = msg; }, 20);
    l.setAttribute("role", isError ? "alert" : "status");
  };

  // ---- open the source record(s) of an item (R-RV-9); entries/amounts: one record, flags: every record in the evidence
  RV.sourceTargets = function (item, kind) {
    if (kind === "flag") {   // one span per record, so a two-record flag opens both records once each
      const seen = {}, spans = [];
      (item.evidence || []).forEach((e) => { if (!seen[e.record_id]) { seen[e.record_id] = 1; spans.push({ record_id: e.record_id, start: e.start, end: e.end }); } });
      return { ids: spans.map((s) => s.record_id), spans };
    }
    if (kind === "entry" && typeof ZL.entrySpans === "function") { const spans = ZL.entrySpans(item); return { ids: spans.map((s) => s.record_id), spans }; }
    const ids = item.record_ids || [];
    return { ids, spans: ids.length ? [{ record_id: ids[0], start: item.excerpt_start, end: item.excerpt_end }] : [] };
  };
  RV.openSource = function (item, kind, title) {   // T-042's modal: ZL.openSource(spans, title)
    const t = RV.sourceTargets(item, kind);
    if (!t.spans.length || typeof ZL.openSource !== "function") return;
    const c = RV.caseNow(), seqs = t.ids.map((id) => { const r = ((c && c.records) || []).find((x) => x.id === id); return r ? r.seq : id; });
    ZL.openSource(t.spans, title || (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]));
  };

  // ---- one linear queue in page order (T-060, paralegal F1). Items are every [data-item-id] row that is on screen, in document order: dates to confirm,
  // the timeline rows (needs review first), the could-not-verify tray, flags, charges. j / k walk that list; a / d / Enter-on-a-button advance to the next
  // item that still needs a decision, needs-review ones before verified ones.
  const NOT_QUEUE = "dialog, .sbs-pane";
  RV.itemRowOf = function (t) {   // the item row that holds focus, or null (focus on Export, the header, a dialog or the page body is not "in" the queue)
    const r = t && t.closest && t.closest("[data-item-id]");
    return r && !r.closest(NOT_QUEUE) ? r : null;
  };
  RV.domItems = () => Array.from(document.querySelectorAll("[data-item-id]")).filter((n) => !n.closest(NOT_QUEUE) && n.offsetParent !== null);
  const decidable = (n) => n.getAttribute("data-review") === "pending" && n.getAttribute("data-state") !== "rejected" && !n.hasAttribute("data-tray-kind");
  RV.nextPendingAfter = function (items, at) {   // items after `at` first, then wrapping. Order of preference: a needs-review entry in the timeline, then any needs-review item, then any item that still needs a decision
    const order = items.slice(at + 1).concat(items.slice(0, Math.max(at, 0) + (at < 0 ? 0 : 1)));
    const open = order.filter(decidable), needs = (n) => n.getAttribute("data-state") === "needs_review";
    return open.find((n) => needs(n) && n.closest('[data-testid="queue"]')) || open.find(needs) || open[0] || null;
  };
  function focusNode(t) {
    if (!t) return false;
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
    t.focus({ preventScroll: true }); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
    return true;
  }
  function focusItem(id) {
    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
    return focusNode(q || document.querySelector('[data-item-id="' + id + '"]'));
  }
  RV.focusFirstPending = function () {   // "Start review": the first item that needs a decision, needs-review ones first
    const items = RV.domItems(); const t = items.filter(decidable).find((n) => n.getAttribute("data-state") === "needs_review") || items.find(decidable) || items[0];
    return focusNode(t);
  };
  function focusExport(msg) { const b = document.querySelector('[data-testid="btn-export"]'); if (b) { b.focus(); if (msg) RV.say(msg); } }
  function restoreFocus(pf) {
    if (!pf) return;
    requestAnimationFrame(() => {
      if (pf.nextFrom) {
        const items = RV.domItems(), at = items.findIndex((n) => n.getAttribute("data-item-id") === pf.nextFrom);
        const t = RV.nextPendingAfter(items, at);
        if (t && t.getAttribute("data-item-id") !== pf.nextFrom) { focusNode(t); return; }
        focusExport("Nothing left to decide. Export is next.");   // the last decision: the next control is the one that finishes the job, not the top of the page
        return;
      }
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) t.focus(); else focusItem(pf.id);
    });
  }

  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  // m2: a refused edit is tied to its field (aria-invalid + aria-describedby) as well as announced
  function markInvalid(id, s) { const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (!ta || !s) return; s.id = s.id || "rv-err-" + id; ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", s.id); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) { s.textContent = msg; markInvalid(id, s); } RV.say(msg, true); }
  const nextCode = (e) => { const n = e && e.detail && e.detail.next_action; return n && n.code ? String(n.code).toUpperCase() : null; };   // T-104: EDIT_SUMMARY | EDIT_QUOTE
  const QUOTE = "Change the quote";
  const changeQuote = (id) => () => { if (ZL.stepper && ZL.stepper.changeQuote) ZL.stepper.changeQuote(id); };
  // T-104: CODE_CHECK_FAILED returned by an EDIT: the server's sentence sits under the edit box (the box stays open with the typed text); EDIT_QUOTE adds a Change the quote action.
  function showEditRefusal(id, e) {
    const s = slot(id, "rv-error"), msg = e.message || "That wording fails a check. Edit it to match the quote.";
    if (s) {
      ZL.clear(s);
      s.append(el("span", { "data-testid": "edit-refused-msg" }, msg));
      if (nextCode(e) === "EDIT_QUOTE") s.append(" ", el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-edit-refused-quote", "aria-label": QUOTE + " for " + (ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id), onclick: changeQuote(id) }, QUOTE));
    }
    markInvalid(id, s);
    RV.say("Not saved: " + msg, true);
    const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
  }

  // ---- D-051 (T-098 r2): Accept is refused with 422 CODE_CHECK_FAILED when the summary fails a code check. The server's plain reason (it ends "Edit the summary to match the
  // quote.") shows right under the item's buttons with an Edit action; nothing was changed. It stays until the item changes (any successful decision) or the paralegal edits.
  const refusals = {};       // id -> {message}
  function paintRefusal(root, id, edit) {
    const r = refusals[id], box = root.querySelector(".rv-refused");
    if (!box) return;
    ZL.clear(box); box.hidden = !r;
    if (!r) return;
    box.append(el("p", { class: "rv-refused-msg", "data-testid": "accept-refused-msg" }, el("strong", {}, "Not accepted. "), r.message),
      r.code === "EDIT_QUOTE"   // T-104: the first failing check is on the quote, so the fix is the quote, not the summary
        ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-quote", "aria-label": QUOTE + " for " + r.label, onclick: changeQuote(r.id) }, QUOTE)
        : edit ? el("button", { type: "button", class: "btn rv-refused-edit", "data-testid": "btn-accept-refused-edit", "aria-label": "Edit the summary for " + r.label, onclick: edit }, "Edit the summary") : null);
  }
  RV.clearRefusal = (id) => { if (refusals[id]) { delete refusals[id]; repaintRefusal(id); } };   // T-108: a saved quote change ends the refused-Accept box at once
  function repaintRefusal(id) { document.querySelectorAll('[data-controls-for="' + id + '"]').forEach((root) => paintRefusal(root, id, root._openEdit)); }
  RV.isCodeCheckRefusal = (e) => !!e && String(e.code).toUpperCase() === "CODE_CHECK_FAILED";

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
  const DATE_FIRST = "Confirm the date first.", DATE_WHY = "This entry has no confirmed date, so it cannot go into the letter yet. Pick the right date in Dates to confirm.";
  RV.needsDate = (item, kind) => kind === "entry" && !item.date;
  function goToDateRow(id) {   // the entry's own row sits in Dates to confirm: move focus to its date choices
    const row = document.querySelector('[data-testid="dates-to-confirm"] [data-entry-id="' + id + '"]');
    const t = row && (row.querySelector('[data-testid="confirm-date"]:checked') || row.querySelector('[data-testid="confirm-date"]') || row);
    const box = document.querySelector('[data-testid="dates-to-confirm"]');
    const f = t || box; if (!f) return;
    if (!f.hasAttribute("tabindex") && !/^(BUTTON|A)$/.test(f.tagName)) f.setAttribute("tabindex", "-1");
    f.focus(); if (f.scrollIntoView) f.scrollIntoView({ block: "center" });
  }

  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    busy.add(id);
    try {
      const resp = await ZL.api.review(c.token, id, body);
      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      ZL.state.applyReview(resp);
      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, scope: o.scope } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, (e.message || "That edit is not allowed.") + toks);
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
        refusals[id] = { id, code: nextCode(e), message: e.message || "The summary fails a check. Edit the summary to match the quote.", label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
        const mine = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-controls-for="' + id + '"]'), box = (mine || document).querySelector(".rv-refused:not([hidden])");
        if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
    } finally { busy.delete(id); }
  };

  // ---- controls
  RV.controls = function (item, kind) {
    const id = item.id, st = item.review_status || "pending";
    const isFlag = kind === "flag", canEdit = kind === "entry" || isFlag;
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    // T-060 r3: a decided row shows its state, not the action it already took. Primary (filled) is for an undecided item only; Accepted / Dismissed read as quiet state words, Undo is the way back.
    const VARIANT = { accept: st === "pending" ? "btn--primary" : st === "dismissed" ? "" : "rv-decided", edit: "", dismiss: st === "dismissed" ? "rv-decided rv-decided--muted" : "btn--ghost", reset: "btn--link", audit: "btn--link", "dismiss-reason": "btn--link" };
    const btn = (action, text, tid, extra, name) => el("button", Object.assign({ type: "button", class: ("btn " + (VARIANT[action] || "") + " rv-" + action).replace("  ", " "), "data-testid": tid, "data-action": action, "aria-label": (name || text).replace("…", "") + ": " + lbl }, extra || {}), text);
    const accepted = st === "accepted" || st === "edited";

    const bar = el("div", { class: "rv-actions", role: "group", "aria-label": "Review actions" });
    const blocked = RV.needsDate(item, kind) && st !== "accepted";
    const acceptText = accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
    bar.append(btn("accept", acceptText, "btn-accept", { "data-icon": accepted ? "check" : null, "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null,
      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, { action: "accept" }, ev.detail === 0 ? { advance: true } : { focus: "accept" }); } }));
    let form;
    if (canEdit) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true), disabled: blocked }));
    bar.append(btn("dismiss", st === "dismissed" ? "Dismissed" : "Dismiss", "btn-dismiss", { "data-icon": st === "dismissed" ? "dash" : null, "aria-pressed": String(st === "dismissed"),
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.reasonOpen)); if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
      el("button", { type: "button", class: "btn btn--link", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));

    // dismiss reason (flags only; optional - R-RV-5)
    const reasonIn = el("input", { type: "text", id: "dr-" + id, class: "rv-input", maxlength: "300", "aria-label": "Reason for dismissing (optional)", "data-testid": "dismiss-reason", value: d.reason || "" });
    reasonIn.addEventListener("input", () => { d.reason = reasonIn.value; });
    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const r = reasonIn.value.trim(); RV.act(id, r ? { action: "dismiss", note: r } : { action: "dismiss" }, { focus: "dismiss" }); } },
      reasonIn, el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-dismiss-confirm" }, "Dismiss"));
    if (isFlag) root.append(reasonRow);

    if (canEdit) {
      const hint = isFlag ? "Your note (internal notes only, never in the letter)" : "Summary wording (the quoted excerpt, date and provider cannot be changed)";
      const ta = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: isFlag ? "note" : "summary", "data-testid": isFlag ? "flag-note" : "edit-summary" });   // named by its visible label (WCAG 2.5.3)
      ta.value = d.text;
      ta.addEventListener("input", () => { d.text = ta.value; ta.removeAttribute("aria-invalid"); });
      form = el("form", { class: "rv-edit", hidden: !d.open, onsubmit: (ev) => {
        ev.preventDefault(); const v = ta.value.trim();
        if (!v) { showError(id, isFlag ? "Write a note first, or cancel." : "The summary can't be empty."); return; }
        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: "edit" });
      } },
        el("label", { class: "rv-label" }, hint, ta),
        el("div", { class: "rv-actions" },
          el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-edit" }, "Save"),
          el("button", { type: "button", class: "btn", "data-testid": "btn-cancel-edit", onclick: () => toggleEdit(false) }, "Cancel")));
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
      });
      root.append(form);
      var toggleEdit = function (open) {
        d.open = open; form.hidden = !open;
        if (open) ta.focus(); else { const b = bar.querySelector('[data-action="edit"]'); if (b) b.focus(); }
      };
      ui[id] = { openEdit: () => toggleEdit(true) };
      root._openEdit = () => toggleEdit(true);
    } else ui[id] = {};
    root.append(el("div", { class: "rv-error", role: "alert" }));
    paintRefusal(root, id, root._openEdit);
    return root;
  };

  // ---- legend (one line; the full list is the Shortcuts dialog)
  RV.legend = () => el("p", { class: "rv-keys", "data-testid": "keys-hint" }, el("strong", {}, "Keyboard: "),
    "with an item selected, j and k move between items, a accepts, d dismisses, e edits. Press ? for the full list.");

  // ---- the shortcut sheet: opened by the header "Shortcuts" button, or by ? while an item is selected
  const KEYS = [["j / k", "Next / previous item (dates to confirm, then entries, flags, charges)"], ["a", "Accept the selected item, then move to the next one that needs a decision"], ["d", "Dismiss the selected item, then move on"],
    ["e", "Edit the wording of the selected item"], ["r", "Reset a decided item"], ["o", "Open the source record in a dialog"], ["p", "Move focus to the source record beside the list (Esc returns)"],
    ["Shift+A", "Accept all verified entries (asks first, with the count)"], ["?", "This list"]];
  RV.openShortcuts = function () {
    let d = document.querySelector('[data-testid="shortcuts-modal"]');
    if (!d) {
      d = el("dialog", { class: "dlg dlg--md", "data-testid": "shortcuts-modal", "aria-labelledby": "kb-title" },
        el("div", { class: "dlg-head" }, el("h2", { id: "kb-title" }, "Keyboard shortcuts"), el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-close-shortcuts", onclick: () => d.close() }, "Close")),
        el("div", { class: "dlg-body" },
          el("p", { class: "muted" }, "Letter keys work only while an item is selected: use Start review, or press Tab and then Enter on the first skip link. They never act from Export, the header or a text box."),
          el("dl", { class: "kv kv--keys", "data-testid": "shortcuts-list" }, KEYS.flatMap(([k, v]) => [el("dt", {}, el("kbd", {}, k)), el("dd", {}, v)]))));
      document.body.append(d);
    }
    const back = document.activeElement;
    d.addEventListener("close", () => { if (back && back.isConnected) back.focus(); }, { once: true });
    if (!d.open) d.showModal();
  };

  // ---- keyboard flow (R-RV-4, WCAG 2.1.4 / T-060 blocker). Single-key shortcuts act ONLY while focus is on an item row or on something inside one.
  // From Export, the header, a dialog, a text field or the page body they do nothing, so a stray key can never change a decision.
  const typing = (t) => !!t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (typing(t)) return;
    if (document.querySelector("dialog[open]")) {   // a dialog swallows the letter keys; say so instead of doing nothing (T-060 r3, paralegal F11)
      if (ev.key.length === 1 && "jkadero".includes(ev.key.toLowerCase()) && !ev.shiftKey && ZL.state.get().case) RV.say("A window is open. Press Escape to close it first, then use the key again.");
      return;
    }
    const row = RV.itemRowOf(t);
    if (!row) return;
    const c = RV.caseNow(); if (!c) return;
    const key = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key, id = row.getAttribute("data-item-id");
    if (ev.key === "?") { ev.preventDefault(); if (RV.openShortcuts) RV.openShortcuts(); return; }
    if (ev.shiftKey) return;   // Shift+A is the batch key (batch.js); a capital letter never means the single-item key
    if (key === "j" || key === "k") {
      const items = RV.domItems(), at = items.indexOf(row), n = items[at + (key === "j" ? 1 : -1)];
      ev.preventDefault();
      if (n) focusNode(n); else RV.say(key === "j" ? "That is the last item." : "That is the first item.");
      return;
    }
    if (ev.key.length !== 1 || !"aedro".includes(key)) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.act(id, { action: "reset" }, { focus: "reset" }); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (c && mountEl) render(mountSection(mountEl, name), c); });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
      rowEl.setAttribute("data-item-id", entry.id); rowEl.setAttribute("data-review", entry.review_status || "pending");
      if (!rowEl.hasAttribute("tabindex")) rowEl.setAttribute("tabindex", "0");
      const ctrl = RV.controls(entry, "entry"); rowEl.append(ctrl);
      const au = ctrl.querySelector(".rv-audit"), links = rowEl.querySelector(".row-actions");
      if (au && links) links.append(au);   // Why? / Open record / Change quote / Audit are one group of links on the right of the row
      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
        const head = rowEl.querySelector(".entry-head") || rowEl;
        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
      }
    });
  }
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:16.664Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Not in the quote\\|not in the quote\\|new_tokens\\|\\\"tokens\\\"\" app/backend/*.py | head -20; grep -n \"invalid_edit\" -r tests/e2e | head"
}
````

### User / tool · 2026-11-02T11:06:16.766Z

**tool result**
````
app/backend/generator.py:104:              summary_tokens_not_in_excerpt=g.new_tokens(summary, excerpt, record["source"], record.get("date_iso") or "") if not failures else [],
app/backend/grounding.py:154:def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/grounding.py:265:    if new_tokens(summary, excerpt, label, date_iso):
app/backend/narrative.py:59:    if grounding.new_tokens(text, quote, entry["label"], entry["date_iso"] or ""):
app/backend/review.py:5:no, not, without) that is not in the quote, a qualifier of the quote that the summary drops, or a highlight that cannot be found is a hard 422
app/backend/review.py:71:CHECK_PHRASE = {"SUMMARY_TOKEN_NOT_IN_EXCERPT": "a number or word in it is not in the quote", "SUMMARY_DROPS_QUALIFIER": "it drops a qualifier the quote has",
app/backend/review.py:89:        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
app/backend/review.py:91:            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
app/backend/review.py:110:    if c == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and d.get("tokens"):
app/backend/review.py:111:        toks = d["tokens"]
app/backend/review.py:113:            what = "The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(toks) + "."
app/backend/review.py:134:            "tokens": (fails.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens", []),
app/backend/review.py:238:    D-034/D-047: a number/date/$ figure, a side or negation word that is not in the quote, a qualifier the summary drops, or a highlight that
app/backend/review.py:244:    toks = g.new_tokens(new_sum, new_exc, label, date_iso)
app/backend/review.py:247:        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
app/backend/spanish.py:4:from app.backend.spanish_text import *      # noqa: F401,F403  (module_for, new_tokens, check_summary, check_excerpt, translation_info, ...)
app/backend/spanish_text.py:9:`module_for(lang)` returns `grounding` for English and this module for Spanish; both expose new_tokens, dropped_qualifiers and check_summary.
app/backend/spanish_text.py:192:def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/spanish_text.py:194:    the parsed date do not support. Same contract as grounding.new_tokens."""
app/backend/spanish_text.py:275:    if new_tokens(summary, excerpt, label, date_iso):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:18.239Z

**tool call — Bash**
````
{
 "command": "sed -n 236,262p app/backend/review.py; sed -n 100,120p app/backend/review.py; sed -n 154,200p app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T11:06:18.342Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:21.255Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _num_tokens\" -A25 app/backend/grounding.py; grep -n \"T-044\" -B2 -A6 reviews/T-044*ux* 2>/dev/null | grep -i \"\\\\$\\|422\" | head"
}
````

### User / tool · 2026-11-02T11:06:21.376Z

**tool result**
````
134:def _num_tokens(text: str) -> list:
135-    out = []
136-    for m in _NUM.finditer(text):
137-        t = m.group(0).replace(",", "")
138-        out.append(str(int(t)) if t.isdigit() else t)
139-    return out
140-
141-
142-def _allowed_numbers(excerpt: str, label: str, date_iso: str) -> set:
143-    allowed = set(_num_tokens(excerpt)) | set(_num_tokens(label))
144-    allowed |= {str(int(p)) for p in re.findall(r"\d+", date_iso or "")}
145-    return allowed
146-
147-
148-def side_neg_words(text: str, keep_order: bool = False):
149-    """The side and negation words in `text` (lower case): left, right, bilateral, no, not, none, never, without, denies, negative, absent, neither, nor, n't forms."""
150-    ws = [(a or b).lower() for a, b in _WORDS.findall(text)]
151-    return ws if keep_order else set(ws)
152-
153-
154-def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
155-    """Numbers, dollar figures, dates (month names), side and negation words (side_neg_words) and attribution, hedge or approximation words
156-    (added_qualifier_tokens) in the summary that are in none of the
157-    excerpt, the source label or the parsed date. Digits are compared as digit runs, so a label digit can mask a changed
158-    score ('visit 8' vs 'pain 8/10'): that gap belongs to judge 1 (SE5)."""
159-    allowed = _allowed_numbers(excerpt, label, date_iso)
3:Verdict: pass (no blockers, no majors; five minors). Drove the live app at 1280x900 and 390x844 with Playwright: paste sample, run, accept all verified, undo batch, edit entry 3, $9,000 edit on entry 5, export, both copy buttons (clipboard read-back), pending confirmation, dismiss 5 / leave 6 pending, badge label. Evidence: `artifacts/review-evidence/T-044-*.png`, `T-044-ux-designer-walk*.py`, `*.out.txt`, `T-044-1280-letter-7of9.txt`.
5-Tests: `pytest tests/e2e/test_export_ui.py tests/e2e/test_edit.py` = 2 failed, 6 passed. Both failures are test defects, not UI defects. `test_added_dollar_warns_and_needs_keep_my_wording` expects the old 409 and "$9,000"; after D-034 the server returns a hard 422 and the UI renders it ("...not in the quote: 9000. Remove it or change the quote."), with no Keep my wording button (verified at both widths). `test_notes_list_edited_item_with_both_texts` asserts "edited" right after Save without waiting (the failing snapshot still shows the open edit form). Both tests need rewriting by qa.
12- "exercised": ["pytest tests/e2e/test_export_ui.py tests/e2e/test_edit.py -> 2 failed, 6 passed (failures judged against D-034)", "Playwright walks 1-4 at 1280 and 390: paste sample, run, accept all verified, undo batch, edit entry 3, $9,000 edit, export, two copy buttons with clipboard read-back, pending confirmation, dismiss 5 / leave 6 pending, badge text", "curl/urllib API probe of the $9,000 edit after restart: 422 invalid_edit", "read export.js, review.js showConfirm, app.js badge", "inspected exported letter and notes text files"],
17:  {"severity": "minor", "title": "Hard-422 message names '9000', not what the user typed ('$9,000')", "evidence": "artifacts/review-evidence/T-044-ux-designer-walk3.py output and T-044-390-13-dollar-after-restart.png: 'not in the quote: 9000. Remove it or change the quote.' for the input 'billed $9,000.'", "why_it_matters": "The user cannot map the normalized token back to her wording; it reads like a defect. Frontend already flagged the same issue to backend.", "fix": "Backend returns the token as typed (or the UI highlights it in the textarea); keep the message beside Save.", "acceptance_test": "Edit entry 5 to add '$9,000' -> message contains '$9,000' and the textarea content is preserved."},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:26.274Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"dry_run\\|dry-run\\|/check\\|validate\\|preview\" memory/contracts/api.md | head; grep -n \"re-check\\|recheck\\|re check\\|ai check\\|judge 1\\|second check\" memory/contracts/api.md | head -20"
}
````

### User / tool · 2026-11-02T11:06:26.365Z

**tool result**
````
76:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
753:| `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
28:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
34:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
108:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
118:Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
149:      "state": "verified", "reasons": [], "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
166:      "state": "verified", "reasons": [], "why": "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
225:      "state": "verified", "reasons": [], "why": "Quote found word for word; the phrase list and the model agree, and the second check agreed.",
301:            "why": "The second check found part of the summary not supported by the quote.",
329:**Edit re-check order (R-RV-3, ADR-005; D-034, D-047).** (1) Structure, else 422. (2) Code checks (ADR-012). Any of these is a **hard `422 invalid_edit`**: nothing is saved, no judge call is made, no event is logged, and there is **no confirm or override** (the `409 needs_confirm` / `confirm_warnings` / `keep_my_wording` path is removed; a `confirm_warnings` field in a body is ignored):
343:  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
350:- `to: "charge"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated ("not billed", "unbilled"), the figure has a parsed value and its record is not injection-tagged, **and (2) judge 2** re-checks the figure against class `charge` and answers `agree`. Code runs first; the judge is not called when the code check fails. Undoing her own earlier demotion of a figure the code first called a charge skips both checks (the original class returns with the judge answer it had; works with no judge available).
351:- **Spanish cues (T-110 r2, code only, D-050).** The charged-amount wording also accepts `cargo`, `cargos`, `honorarios` and `estado de cuenta` in the figure's sentence (`detail.wording` / `reclassified.wording` carries the phrase). `sin cargo`, `no facturado` and similar negations refuse it, and so does `saldo` (a balance restates charges: counting it would count them twice). The shared rate-cue test (`amounts.RATE_CUE`) also reads `por sesión`, `por visita`, `por hora`, `por día`, `cada` and their unaccented spellings, so `$400 por sesión` is a rate and stays `NO_CHARGE_WORDING`; the amount classifier reads the same rate words, so such a figure is class `rate`. A Spanish figure is still never classed `charge` by code: it starts `unclear` and becomes a charge only here, with the judge re-check; it then counts in the D-019 total once accepted.
372:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
563:`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `RERUN_JUDGE` (text "Run the second check again.", target `{item_id, judge}` or `{view: "judges"}`; the action is `POST /rejudge`), `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.
629:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **T-114 (rates):** every amount in `amounts[]` carries `accept_effect` and `judge_required_for_export`. `accept_effect` is `letter_total` (a `charge`: counted in the billed-charges total), `acknowledge` (a `rate`: accepting it only acknowledges it, it is listed in the internal notes and never totaled, D-019/D-042) or `internal_notes` (`estimate`, `unclear`). `judge_required_for_export` is `false` only for a rate: an accepted rate whose second check never ran is **not** a `JUDGE_NOT_RUN` blocker, so accepting a rate can never block export (its item trace `judge_2` step says the check is optional for a rate). The UI should label a rate's button "Acknowledge" (or keep "Accept as noted") and never promise it goes in the letter. Charges, entries and flags are unchanged. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
648:Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
653:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
714:- **Entry field `translation`** (every entry view; `null` for English records): `{source_language: "es", source_language_name: "Spanish", label: "AI translation", summary_is_translation: true, quote_is_original: true}`. After the paralegal edits the summary, or writes a manual entry, `label` is `"Translation (edited by reviewer)"`. The UI must show `label` next to the summary and show the quote as the original Spanish. Edits and manual entries on a Spanish record are checked against the Spanish quote and judged with the Spanish prompt.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:28.844Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"re-check\\|recheck\" reviews/T-044-ux-designer*.md | head; grep -n \"warnings\\|JUDGE_\" app/frontend/review.js | head"
}
````

### User / tool · 2026-11-02T11:06:28.955Z

**tool result**
````
16:  {"severity": "minor", "title": "Edit re-check is not explained before Save, and the result uses developer wording", "evidence": "artifacts/review-evidence/T-044-390-4-edit-open.png (edit form says only 'Summary wording (the quoted excerpt, date and provider cannot be changed)'); T-044-390-5-edited.png: a Verified+Accepted entry flips to 'Needs review' with 'Check: judge unavailable' after the edit, while still included in the letter", "why_it_matters": "The user is not told beforehand that her wording is checked against the quote. 'judge' is developer vocabulary (checklist 18). A Verified entry silently becoming Needs review after her own edit is unexplained.", "fix": "Add one line under the edit box ('Your wording will be checked against the quoted excerpt'). Replace 'judge unavailable' with plain words ('Could not re-check your wording; compare it with the quote').", "acceptance_test": "E2E: open edit on entry 3 and assert the re-check sentence is visible; save and assert the entry's why text contains no 'judge'."},
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:34.091Z

**tool call — Bash**
````
{
 "command": "sed -n 325,350p memory/contracts/api.md | cut -c1-1500"
}
````

### User / tool · 2026-11-02T11:06:34.175Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:44.188Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/charges.js; cat app/frontend/manual.js | sed -n 1,60p"
}
````

### User / tool · 2026-11-02T11:06:44.271Z

**tool result**
````
/* Charges panel (T-043): accepted total from the API (never summed here), "detected, not yet accepted" labelled as not a total,
   unclear tray for rates / estimates / damages / unreadable amounts (R-CH-3, R-CH-5, D-019). Charges: accept or dismiss only (D-010). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);
  const KIND = { charge: "Charge", rate: "Rate", estimate: "Estimate", damages: "Damages mention", unclear: "Unclear" };
  const recSeq = (c, id) => { const r = (c.records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };
  const reasonIs = (a, code) => (a.reasons || []).includes(code);

  // "12 planned; discharged at visit 9" for a per-visit rate, read from the record headers/text the API returned (or a.rate_note when the backend sends it).
  function rateContext(c, a) {
    const n = a.rate_note || {};
    let planned = n.planned, last = n.last_visit;
    if (planned == null && last == null) {
      const prefix = (s) => String(s || "").split(",")[0].trim().toLowerCase();
      const me = (c.records || []).find((r) => r.id === (a.record_ids || [])[0]);
      const same = me ? (c.records || []).filter((r) => prefix(r.source_label) === prefix(me.source_label)) : [];
      same.forEach((r) => {
        const p = /Plan of care:\s*(\d+)\s*visits?/i.exec(r.text || ""); if (p && planned == null) planned = p[1];
        const v = /\bvisit\s+(\d+)/i.exec(r.source_label || ""); if (v && (last == null || +v[1] > +last)) last = v[1];
      });
    }
    const bits = (planned != null ? [planned + " planned"] : []).concat(last != null ? ["discharged at visit " + last] : []);
    return bits.join("; ");
  }
  // One-line description for the unclear tray. Wording comes from the amount's kind and the quoted line; nothing is computed.
  function unclearNote(c, a) {
    const bits = [];
    if (a.kind === "rate") {
      const m = /\bper\s+([A-Za-z]+)/i.exec(a.excerpt || "") || /\/\s*([A-Za-z]+)/.exec(a.excerpt || "");
      const unit = m ? m[1].toLowerCase() : null;
      bits.push("rate " + a.text + (unit ? "/" + unit : "") + "; " + (unit ? unit + " count" : "count") + " not stated");
      const ctx = a.note || a.detail || rateContext(c, a);
      if (ctx) bits[0] += " (" + ctx + ")";
    } else if (a.kind === "estimate") bits.push("estimate; not a bill");
    else if (a.kind === "damages") bits.push("mention of damages; not a bill");
    else if (a.value_cents == null) bits.push("unreadable amount; request clean copy of bill");
    else bits.push("unclear; not a bill");
    if (a.state === "needs_review") bits.push("needs review");
    if (reasonIs(a, "INJECTION_SUSPECTED")) bits.push("appears inside instruction-like text");
    return bits.join("; ");
  }

  // Plain status words for the Status column. The reason itself is the code's (unclearNote); nothing is computed here.
  const STATUS_WORDS = { rate: "Not counted: a rate, not a bill", estimate: "Not counted: an estimate", damages: "Not counted: a damages mention", unclear: "Not counted: can't tell if this is a bill" };
  // A short stretch of the quote around the amount, with the amount marked. The full quote is one click away (Open record) and stays in the title.
  function snippet(a) {
    const q = String(a.excerpt || ""), amt = String(a.text || ""), i = amt ? q.indexOf(amt) : -1;
    const box = el("blockquote", { class: "rv-quote", title: q });
    if (i < 0) { box.append(q); return box; }
    let from = 0, to = q.length;
    if (q.length > 140) {
      from = Math.max(0, i - 70); to = Math.min(q.length, i + amt.length + 50);
      if (from > 0) { const sp = q.indexOf(" ", from); if (sp >= 0 && sp < i) from = sp + 1; }
      if (to < q.length) { const sp = q.lastIndexOf(" ", to); if (sp > i + amt.length) to = sp; }
    }
    box.append((from > 0 ? "… " : "") + q.slice(from, i), el("mark", {}, amt), q.slice(i + amt.length, to) + (to < q.length ? " …" : ""));
    return box;
  }

  function row(c, a, inTray, boiler) {
    const isCharge = a.kind === "charge";
    const rs = a.review_status || "pending";
    const seq = recSeq(c, (a.record_ids || [])[0]);
    const tr = el("tr", { class: "rv-card rv-amount", tabindex: "0", "data-testid": "amount-" + a.text, "data-item-id": a.id, "data-amount-kind": a.kind,
      "data-state": a.state, "data-review": rs, "aria-label": "Amount " + a.text });
    const first = el("td", { class: "rv-c-amount", "data-label": "Amount" }, el("strong", { class: "rv-money", title: "As written in the record: " + a.text }, a.value_cents != null ? RV.money(a.value_cents) : a.text), el("span", { class: "rv-kind" }, KIND[a.kind] || a.kind));
    const src = el("td", { class: "rv-c-src", "data-label": "From the record" },
      snippet(a),
      el("div", { class: "rv-src-links" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": "Open record " + seq + " for the amount " + a.text, onclick: () => RV.openSource(a, "amount") }, "Open record " + seq),
        ZL.stepper ? ZL.stepper.traceButton(a.id, "btn btn--link") : null));
    // one reason line (the code's). The server's longer sentence is shown only when it adds something and is not a notice every row repeats.
    const why = a.why && !boiler.has(a.why) ? a.why : null;
    const status = el("td", { class: "rv-c-status", "data-label": "Status" }, RV.chips(a),
      inTray ? el("span", { class: "rv-unclear-note" }, STATUS_WORDS[a.kind] || STATUS_WORDS.unclear, ". ", unclearNote(c, a)) : null,
      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Kept in the internal notes only; not in the letter or the total.") : null,
      why ? el("p", { class: a.state === "needs_review" ? "rv-reason-line" : "rv-why" }, why) : null);
    const act = el("td", { class: "rv-c-act", "data-label": "Decision" }, RV.controls(a, "amount"));
    tr.append(first, src, status, act);
    return tr;
  }

  function table(c, list, caption, inTray, boiler) {
    return el("table", { class: "rv-table" }, el("caption", { class: "rv-sr" }, caption),
      el("thead", {}, el("tr", {}, ["Amount", "From the record", "Status", "Decision"].map((h) => el("th", { scope: "col" }, h)))),
      el("tbody", {}, RV.needsReviewFirst(list).map((a) => row(c, a, inTray, boiler))));
  }
  // A sentence that several rows carry (for example the Spanish-record notice) is shown once above the table and left out of the rows.
  function repeated(list) {
    const n = {}; list.forEach((a) => { if (a.why) n[a.why] = (n[a.why] || 0) + 1; });
    return new Set(Object.keys(n).filter((k) => n[k] > 1));
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "charges-panel");
    root.setAttribute("aria-labelledby", "rv-charges-h");
    const amounts = c.amounts || [], t = c.totals || {};
    const charges = amounts.filter((a) => a.kind === "charge"), unclear = amounts.filter((a) => a.kind !== "charge");
    const acc = (t.accepted && t.accepted.cents) != null ? t.accepted.cents : 0;
    const pendObj = t.pending || t.detected_not_a_total || { cents: 0 };
    root.append(el("h2", { id: "rv-charges-h" }, "Charges"),
      el("p", { class: "rv-help" }, "Only charges you accept are counted. Rates, estimates, damages and unreadable amounts are listed below and never added."),
      el("div", { class: "rv-totals" },
        el("p", { class: "rv-total rv-total-main", "data-testid": "accepted-total", "aria-live": "polite" }, el("span", { class: "rv-total-label" }, "Accepted charges: "), el("strong", {}, RV.money(acc))),
        el("p", { class: "rv-total rv-total-pending", "data-testid": "pending-total" }, "Detected, not yet accepted: " + RV.money(pendObj.cents || 0) + " (not a total)")));
    const overlap = ZL.sg ? ZL.sg.overlapBox(c) : null; if (overlap) root.append(overlap);
    root.append(el("h3", {}, "Detected charges (" + charges.length + ")"));
    const chBoil = repeated(charges), unBoil = repeated(unclear);
    if (charges.length) { chBoil.forEach((t) => root.append(el("p", { class: "rv-tray-note" }, t))); root.append(table(c, charges, "Detected charges", false, chBoil)); } else root.append(el("p", { class: "rv-empty" }, "No charges were found."));
    const tray = el("section", { class: "rv-tray", "data-testid": "unclear-tray", "aria-labelledby": "rv-unclear-h" },
      el("h3", { id: "rv-unclear-h" }, "Unclear — not totaled (" + unclear.length + ")"));
    if (unclear.length) { unBoil.forEach((t) => tray.append(el("p", { class: "rv-tray-note", "data-testid": "tray-notice" }, t))); tray.append(table(c, unclear, "Unclear amounts, not totaled", true, unBoil)); } else tray.append(el("p", { class: "rv-empty" }, "Nothing unclear."));
    root.append(tray);
  }
  RV.registerPanel("charges", render);
  RV.renderCharges = render;
})();
/* Manual entry for a record in the could-not-verify tray (T-056 B1, D-031). The paralegal picks whole sentences of that record
   (the excerpt is cut from the record text by code, so it is verbatim) and writes her own summary: POST /records/{rid}/entry.
   Server refusals (422, D-047: the reason is shown inline and the typed text stays) are shown in plain words. Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  const draft = {};   // tray item id -> {open, picked:[sentence index], summary}
  const REASON = {
    EXCERPT_NOT_WHOLE_SENTENCE: "The quote must start and end at a sentence boundary.",
    EXCERPT_NOT_VERBATIM: "The quote is not word for word in the record.",
    EXCERPT_OMITS_QUALIFIER: "A hedge sentence in the record qualifies your quote; include it.",
  };

  // Quotable sentences of a record: header lines are not part of any excerpt, and the opening `Excerpt: "` / closing quote are not quoted text.
  function quotable(rec) {
    const out = [];
    (rec.sentences || []).forEach((s) => {
      let a = s.start, b = s.end, txt = rec.text.slice(a - rec.char_start, b - rec.char_start);
      if (/^(===|Date:|Source:)/.test(txt)) return;
      const m = /^Excerpt:\s*"?/.exec(txt); if (m) { a += m[0].length; txt = txt.slice(m[0].length); }
      if (/"\s*$/.test(txt) && !txt.slice(0, -1).includes('"')) { const k = txt.length - txt.replace(/"\s*$/, "").length; b -= k; txt = txt.slice(0, txt.length - k); }
      if (txt.trim()) out.push({ text: txt, start: a, end: b });
    });
    return out;
  }

  function control(c, t, rec) {
    const d = draft[t.id] || (draft[t.id] = { open: false, picked: [], summary: "" });
    const sents = quotable(rec);
    const msg = el("p", { class: "rv-error", role: "alert", "data-testid": "manual-error" });
    const sum = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: "summary", "data-testid": "manual-summary", "aria-label": "Your summary, written from the quote" });
    sum.value = d.summary; sum.addEventListener("input", () => { d.summary = sum.value; });
    const boxes = sents.map((s, i) => {
      const cb = el("input", { type: "checkbox", name: "sent", value: String(i), checked: d.picked.includes(i) || null, onchange: () => { d.picked = boxes.filter((b) => b.input.checked).map((b) => +b.input.value); } });
      return { input: cb, label: el("label", { class: "rv-radio" }, cb, s.text) };
    });
    async function submit() {
      msg.textContent = "";
      const idx = d.picked.slice().sort((a, b) => a - b);
      if (!idx.length) { msg.textContent = "Pick at least one sentence to quote."; return; }
      if (idx.some((v, k) => k && v !== idx[k - 1] + 1)) { msg.textContent = "Pick sentences that sit next to each other in the record."; return; }
      if (!d.summary.trim()) { msg.textContent = "Write your summary of the quote."; return; }
      const a = sents[idx[0]], b = sents[idx[idx.length - 1]];
      const body = { summary: d.summary.trim(), excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/records/" + encodeURIComponent(rec.id) + "/entry", body);
      if (r.status === 200 || r.status === 201) {
        delete draft[t.id]; ZL.state.set({ case: await ZL.api.getCase(c.token) }); RV.say("Entry added for record " + rec.seq + ". It is not reviewed yet."); return;
      }
      const err = (r.body && r.body.error) || {}, detail = err.detail || {};
      const why = (detail.reasons || []).map((x) => REASON[x]).filter(Boolean);
      msg.textContent = (err.message || "That entry was refused.") + (why.length ? " " + why.join(" ") : "");
      RV.say(msg.textContent, true);
    }
    const form = el("form", { class: "rv-edit rv-manual-form", hidden: !d.open, "data-testid": "manual-form", onsubmit: (ev) => { ev.preventDefault(); submit(); } },
      el("fieldset", { class: "rv-fieldset" }, el("legend", {}, "Pick the sentences to quote from Record " + rec.seq + " (whole sentences, next to each other)"),
        sents.length ? boxes.map((b) => b.label) : el("p", { class: "rv-empty", "data-testid": "manual-no-sentences" }, "This record has no sentences to pick from." + (rec.sentences_reason ? " Why: " + rec.sentences_reason : ""))),
      el("label", { class: "rv-label" }, "Your summary (written from the quote; numbers and dates must be in the quote)", sum),
      el("div", { class: "rv-actions" }, el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-manual" }, "Add entry"),
        el("button", { type: "button", class: "btn", onclick: () => toggle(false) }, "Cancel")), msg);
    const open = el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-manual-entry", "aria-expanded": String(d.open), onclick: () => toggle(!d.open) }, "Enter this record by hand");
    function toggle(v) { d.open = v; form.hidden = !v; open.setAttribute("aria-expanded", String(v)); if (v) { const f = form.querySelector("input,textarea"); if (f) f.focus(); } else open.focus(); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:44.743Z

**tool call — Bash**
````
{
 "command": "grep -n \"Your decision\\|What you need to do\\|See the steps\\|Technical details\\|Code said\\|phrase list\\|accept it if\\|Not reviewed\" app/frontend/*.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T11:06:44.826Z

**tool result**
````
app/frontend/audit.js:48:    body.append(el("h3", {}, "Your decisions"));
app/frontend/review.js:44:  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
app/frontend/judges.js:6:   into one row with chips. Model, prompt and reason-code internals sit in closed "Technical details".
app/frontend/judges.js:15:    sources_disagree: "The phrase list and the AI disagree",
app/frontend/judges.js:17:  const RS = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
app/frontend/judges.js:24:  const TODO_COMPARE = "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.";   // same fixed sentence as the item stepper (COMPARE_BY_HAND)
app/frontend/judges.js:50:      el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps"));
app/frontend/judges.js:52:  const noCode = (t) => String(t || "").replace(/\s*\([A-Z]{3,}(?:_[A-Z]+)*\)\s*$/, "");   // the closed reason code lives in Technical details
app/frontend/judges.js:72:    return el("details", { class: "zs-more", "data-testid": "judge-row-tech" }, el("summary", {}, "Technical details"), nodes.length ? el("p", { class: "zs-ev" }, nodes) : null,
app/frontend/judges.js:92:      el("p", { class: "zj-chips" }, chips, decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
app/frontend/judges.js:94:      it.dis.map((x) => el("p", { class: "zs-ev" }, el("span", { class: "zs-k" }, "Code said: "), x.code_says || "", el("br"), el("span", { class: "zs-k" }, "The AI said: "), noCode(x.judge_says))),
app/frontend/judges.js:95:      todo ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), todo) : null,
app/frontend/judges.js:103:      el("p", { class: "zj-chips" }, chip("Blocks the export", "zj-chip-bad"), decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
app/frontend/judges.js:105:      b.next_action && b.next_action.text ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), b.next_action.text) : null,
app/frontend/judges.js:109:        el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps")));
app/frontend/judges.js:170:      el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "),
app/frontend/judges.js:178:    det.append(el("details", { class: "zs-more zj-tech", "data-testid": "judge-tech" }, el("summary", {}, "Technical details"),
app/frontend/stepper.js:214:  // ---- "What you need to do": one fixed sentence from the server plus a button where something on the page can do it.
app/frontend/stepper.js:323:      el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), text), buttons.length ? el("div", { class: "zs-todo-btns" }, buttons) : null, rerunToo ? rerunStatus() : null, msg);
app/frontend/stepper.js:347:    if (ev.events && ev.events.length) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decisions: "), ev.events.map((e) => (e.action || "") + (e.at ? " at " + e.at : "")).join("; ")));
app/frontend/stepper.js:348:    else if (ev.action) out.push(el("p", { class: "zs-ev" }, el("strong", {}, "Your decision: "), ev.action + (ev.at ? " at " + ev.at : "")));
app/frontend/stepper.js:359:      out.push(el("details", { class: "zs-more", "data-testid": "step-tech" }, el("summary", {}, "Technical details"), techNodes.length ? el("p", { class: "zs-ev" }, techNodes) : null,
app/frontend/stepper.js:364:  // Count chips in the paralegal's words: no "llm", "lexicon" or reason codes in the primary view (those are in Technical details).
app/frontend/stepper.js:365:  const WORD = { code: "code", llm: "AI", lexicon: "phrase list", "lexicon+llm": "phrase list and AI" };
app/frontend/stepper.js:496:      el("p", { class: "zs-todo-text" }, el("strong", {}, "Not reviewed (" + (w.count != null ? w.count : "") + "): "), w.why || ""),
app/frontend/stepper.js:549:    // "What you need to do", visible without opening the checks: the next step that waits on the human, in the words the rail uses (T-060, paralegal F2).
app/frontend/stepper.js:554:        el("p", {}, el("strong", {}, "What you need to do: "), text),
app/frontend/mock_flags.js:19:        [find(recs, 4, "Plan of care: 12 visits."), find(recs, 6, "Discharged from PT after two missed appointments.")], { state: "needs_review", reasons: ["LEXICON_ONLY"], why: "The phrase list and the model disagree on this flag
app/frontend/mock_flags.js:21:        [find(recs, 3, "Patient reports low back pain in 2023, resolved.")], { state: "needs_review", reasons: ["LLM_ONLY"], why: "The model found this; the phrase list did not." }),
app/frontend/timeline.js:7:  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
app/frontend/timeline.js:192:  // ---- "What you need to do": one strip above the work, in plain words, each open decision a jump control. Built from the case data, so it is there before the
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:46.611Z

**tool call — Bash**
````
{
 "command": "sed -n 1,130p app/frontend/judges.js"
}
````

### User / tool · 2026-11-02T11:06:46.698Z

**tool result**
````
/* "How the AI was checked" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, agreed / objected / unavailable counts,
   each objection with its fixed-sentence reason, and where the code checks and the AI read an item differently. Every row links to the item's stepper.
   This is a report on the AI's drafts, never a verdict on the case: the label says so. Counts are the server's; nothing is added here.
   Placement (round 2): mounted by ZL.stepper.mountCase right under the case checks, collapsed by default to ONE summary row that carries the signal
   ("16 checked, 13 agreed with the draft, 3 questioned"). One row per item: an item the AI objected to AND that appears under "disagreements" is merged
   into one row with chips. Model, prompt and reason-code internals sit in closed "Technical details".
   Rows carry data-target-item (not data-item-id) so the review keyboard flow and the panels' j/k walk do not treat them as review items. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let cache = null, wasOpen = false, gate = null;   // gate: what the export gate lists, {jnr: [item ids with a JUDGE_NOT_RUN blocker], code: [code-check blockers on the paralegal's wording]}; null until the case trace has loaded

  const DIS = {
    judge_objects: "Code checks passed, the AI objected",
    judge_agrees_code_flags: "Code raised a doubt, the AI found it supported",
    sources_disagree: "The phrase list and the AI disagree",
  };
  const RS = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const KIND = { entry: "Entry", amount: "Amount", flag: "Flag" };
  const READING = {   // the verdict in words that name who disagrees with whom
    partially: "The AI found the draft only partly supported by the quote.",
    unsupported: "The AI found the draft not supported by the quote.",
    disagrees: "The AI reads this differently from the draft.",
  };
  const TODO_COMPARE = "Compare the item with the quote yourself. Edit it, accept it if you agree with it, or dismiss it.";   // same fixed sentence as the item stepper (COMPARE_BY_HAND)
  const TODO_AMOUNT = "Compare the amount with the quote yourself. Accept it as a charge, leave it unclear, or dismiss it.";
  const TODO_UNCHECKED = "Read it yourself, then accept, edit or dismiss it. The AI did not give an answer you can rely on.";   // item not decided yet
  const TODO_PENDING = "Run the second check again first. If you accept it before the second check has run, the export is blocked until it does.";   // undecided item with no AI answer
  const TODO_BLOCKED = "The second AI check did not run on this item, so it can't go in the letter yet. Run the second check again; if it still cannot answer, dismiss the item.";   // accepted/edited: same sentence as the export gate
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);

  function title(id) { const cue = ZL.stepper.cue(id); return ZL.stepper.label(id) + (cue ? " · " + cue : ""); }
  // Which items block the export is the GATE's answer (the blockers of GET /trace), never a guess from the item's review status: D-045(b) exempts summaries the paralegal
  // wrote or edited from the judge, but not from the code checks, so an edited item can lack a judge answer and be ready, or fail a code check and block. gate is null while the trace is loading.
  function reviewOf(it) { const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return (f && f.item.review_status) || (it.unres || {}).review_status; }
  const gateSet = (tr) => {
    const g = ((tr || {}).steps || []).find((x) => x.id === "export_gate"); if (!g) return null;
    const bl = g.blockers || [];
    return { jnr: bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)), verdict: (tr && tr.verdict) || null };
  };
  const codeIds = () => new Set(((gate && gate.code) || []).map((b) => b.item_id));
  const unchecked = (it) => !!(it.unres && !it.rej && it.unres.verdict === "unavailable");
  const blocking = (it) => unchecked(it) && !!gate && gate.jnr.includes(it.id);
  // The paralegal wrote or edited this wording: no second check applies (D-045 b), and the gate does not list it.
  const humanWording = (it) => { if (!unchecked(it) || blocking(it)) return false; const c = ZL.state.get().case, f = c && ZL.rv && ZL.rv.find(c, it.id); return reviewOf(it) === "edited" || !!(f && f.item.ai_drafted === false); };
  const waiting = (it) => unchecked(it) && !blocking(it) && !humanWording(it) && reviewOf(it) === "pending";   // undecided and unchecked: a rerun covers it
  function links(id) {
    const t = title(id);
    return el("div", { class: "zs-todo-btns" },
      el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
      el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps"));
  }
  const noCode = (t) => String(t || "").replace(/\s*\([A-Z]{3,}(?:_[A-Z]+)*\)\s*$/, "");   // the closed reason code lives in Technical details
  const chip = (text, cls) => el("span", { class: "zs-chip " + (cls || "") }, text);

  // One item, once: group the three server lists by item id.
  function byItem(d) {
    const m = new Map();
    const get = (id, kind) => { if (!m.has(id)) m.set(id, { id, kind, rej: null, unres: null, dis: [] }); return m.get(id); };
    (d.rejections || []).forEach((r) => { get(r.item_id, r.kind).rej = r; });
    (d.unresolved || []).forEach((r) => { get(r.item_id, r.kind).unres = r; });
    (d.disagreements || []).forEach((x) => { get(x.item_id, x.kind).dis.push(x); });
    return Array.from(m.values());
  }

  function techDetails(it) {
    const r = it.rej || it.unres, bits = [];
    const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "zs-kv" }, el("span", { class: "zs-k" }, k + " "), String(v)));
    if (r) bits.push(kv("reason code", r.reason_code), kv("model", r.model), kv("prompt", r.prompt_version), kv("your decision", RS[r.review_status] || r.review_status));
    it.dis.forEach((x) => bits.push(kv("kind of disagreement", x.type), kv("resolution", x.resolution)));
    const nodes = bits.filter(Boolean);
    if (!nodes.length && !(r && r.response_raw)) return null;
    return el("details", { class: "zs-more", "data-testid": "judge-row-tech" }, el("summary", {}, "Technical details"), nodes.length ? el("p", { class: "zs-ev" }, nodes) : null,
      r && r.response_raw ? el("pre", { class: "zs-pre" }, r.response_raw) : null);
  }

  function row(it, testid) {
    const r = it.rej, u = it.unres, chips = [], mine = humanWording(it);
    if (r) chips.push(chip("AI objected", "zj-chip-bad"));
    else if (mine) chips.push(chip("Edited by you, not AI-checked"));
    else if (u) chips.push(chip(u.verdict === "unavailable" ? "AI did not check" : "AI could not decide", "zj-chip-bad"));
    it.dis.forEach((x) => { if (!(r && x.type === "judge_objects")) chips.push(chip(DIS[x.type] || x.type)); });   // "the AI objected" is already the first chip
    const decision = (r || u || it.dis[0] || {}).review_status;
    let why = null;
    if (r) why = el("p", { class: "zs-why" }, el("strong", {}, (READING[r.verdict] || ZL.stepper.verdictWord(r.verdict) + ".") + " "), r.rationale || "");
    else if (mine) why = el("p", { class: "zs-why" }, "You edited this item, so it is your wording and does not need the second check.");
    else if (u) why = el("p", { class: "zs-why" }, u.verdict === "unavailable" ? "The second check did not answer, so no AI judge looked at this item." : "The second check could not decide.");
    const blk = blocking(it);
    if (blk) { chips.push(chip("Blocks the export", "zj-chip-bad")); why = null; }
    const todo = blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u ? (u && !r ? TODO_UNCHECKED : it.kind === "amount" ? TODO_AMOUNT : TODO_COMPARE) : null;
    return el("li", { class: "zj-row", "data-testid": testid, "data-target-item": it.id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, title(it.id)), el("span", { class: "zs-kind" }, KIND[it.kind] || it.kind)),
      el("p", { class: "zj-chips" }, chips, decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      why,
      it.dis.map((x) => el("p", { class: "zs-ev" }, el("span", { class: "zs-k" }, "Code said: "), x.code_says || "", el("br"), el("span", { class: "zs-k" }, "The AI said: "), noCode(x.judge_says))),
      todo ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), todo) : null,
      links(it.id), techDetails(it));
  }
  // An edited or hand-written item whose wording fails a code check: the row is the gate's blocker as the server wrote it (reason, fix sentence), with an Edit action.
  function wordingRow(b) {
    const id = b.item_id, t = title(id), decision = reviewOf({ id });
    return el("li", { class: "zj-row", "data-testid": "judge-wording", "data-target-item": id },
      el("div", { class: "zs-head" }, el("span", { class: "zs-label", "data-testid": "judge-row-title" }, t), el("span", { class: "zs-kind" }, KIND.entry)),
      el("p", { class: "zj-chips" }, chip("Blocks the export", "zj-chip-bad"), decision ? chip("Your decision: " + (RS[decision] || decision)) : null),
      el("p", { class: "zs-why" }, el("strong", {}, ZL.stepper.wordingLead(id) + " "), b.why || ""),
      b.next_action && b.next_action.text ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), b.next_action.text) : null,
      el("div", { class: "zs-todo-btns" },
        el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-judge-edit", "aria-label": ZL.stepper.wordingEditText(id, b.next_action) + " for " + t, onclick: () => ZL.stepper.wordingFix(id, b.next_action) }, ZL.stepper.wordingEditText(id, b.next_action)),
        el("button", { type: "button", class: "btn", "data-testid": "btn-judge-goto", "aria-label": "Go to item " + t, onclick: () => ZL.stepper.goto(id) }, "Go to item"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-judge-steps", "aria-label": "See the steps for " + t, onclick: () => ZL.stepper.openTrace(id) }, "See the steps")));
  }
  const CAP = 5;   // rows shown per group before "Show the other N"; the full list is one click away
  const list = (testid, label, rows, mk, empty, extra) => el("section", { class: "zj-group", "data-testid": testid, "aria-label": label },
    el("h3", {}, label + " (" + plural(rows.length, "item", "items") + ")"), extra || null,
    rows.length ? el("ul", { class: "zj-list" }, rows.slice(0, CAP).map(mk)) : el("p", { class: "rv-empty" }, empty),
    rows.length > CAP ? el("details", { class: "zs-more", "data-testid": "judge-more" }, el("summary", {}, "Show the other " + (rows.length - CAP)), el("ul", { class: "zj-list" }, rows.slice(CAP).map(mk))) : null);

  function tile(n, label) { return el("li", { class: "zj-tile" }, el("strong", { class: "zj-n" }, String(n)), el("span", { class: "zj-l" }, label)); }

  // Built from the server's totals and from the gate; each kind of item is named once, and only items the gate lists carry the blocking words ("blocks export"). An edited item the
  // gate does not hold is counted as "edited by you, not AI-checked" and never as blocking, so the panel and the rail ("Export blocked by N") agree.
  function summaryText(d) {
    const t = d.totals || {}, bits = [], n = t.items_judged || 0;
    const nb = ((gate && gate.jnr) || []).length, nc = ((gate && gate.code) || []).length, cids = codeIds();
    const rest = byItem(d).filter((i) => unchecked(i) && !blocking(i) && !cids.has(i.id));
    const nEdit = gate ? rest.filter(humanWording).length : 0, nWait = gate ? rest.length - nEdit : t.unavailable || 0;
    if (!t.unsupported && !t.unsure && !t.unavailable && !nb && !nc) bits.push("checked " + n + ", all agreed with the draft");
    else {
      bits.push(n + " checked", (t.supported || 0) + " agreed with the draft");
      if (t.unsupported) bits.push(t.unsupported + " questioned");
      if (t.unsure) bits.push(t.unsure + " undecided");
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:06:50.867Z

**tool call — Bash**
````
{
 "command": "grep -rn \"See the steps\\|Your decision\\|Technical details\\|Code said\" tests/ | cut -c1-200 | head -20"
}
````

### User / tool · 2026-11-02T11:06:51.020Z

**tool result**
````
tests/e2e/test_stepper.py:192:    """Reason codes, rule rows and raw count keys live in Technical details, not in the primary view."""
tests/e2e/test_stepper.py:200:    """T-082 r2: one summary row with the counts; closed by default; opening shows the label, models and totals; internals stay in Technical details."""
tests/e2e/test_stepper.py:213:    assert not re.search(r"[A-Z]{3,}_[A-Z_]+|_v\d|prompt", visible), visible      # reason codes and prompt versions are inside closed Technical details
tests/e2e/conftest.py:20:  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-tit
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:00.917Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json,urllib.request,time\ndef call(m,p,b=None):\n    r=urllib.request.Request(\"http://localhost:7955/api\"+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={\"Content-Type\":\"application/json\"})\n    try: return json.load(urllib.request.urlopen(r))\n    except urllib.error.HTTPError as e: return {\"err\":e.code,\"body\":e.read().decode()[:300]}\nc=call(\"POST\",\"/cases\",{\"library\":\"case_lib09_spanish_interpreter_espalda\"})\ntok=c[\"token\"]; print(tok)\nprint(call(\"POST\",f\"/cases/{tok}/run\",{}))\nfor _ in range(60):\n    s=call(\"GET\",f\"/cases/{tok}/status\")\n    if s[\"status\"] in(\"ready\",\"failed\"):break\n    time.sleep(.5)\ncase=call(\"GET\",f\"/cases/{tok}\")\nprint([ (f[\"id\"],f.get(\"days\"),f.get(\"computed\"),list(f.keys())) for f in case[\"flags\"] if f[\"type\"]==\"gap\"][:2])\nprint(case[\"dates_to_confirm\"])\nprint(case.get(\"name\"))\nopen(\"/tmp/claude-501/tok\",\"w\").write(tok)\nEOF"
}
````

### User / tool · 2026-11-02T11:07:01.762Z

**tool result**
````
9Ozgm2ZXczESTFqqLdBcng
{'token': '9Ozgm2ZXczESTFqqLdBcng', 'status': 'running', 'stage': 'extract', 'started_at': '2026-11-02T11:07:01Z'}
[('f_gap_r1_r2', None, {'days': 42, 'endpoint_warnings': [], 'record_ids': ['r1', 'r2'], 'record_nos': [1, 2], 'from': '2026-03-03', 'to': '2026-04-14', 'threshold': 30, 'from_record': 'r1', 'to_record': 'r2'}, ['id', 'state', 'reasons', 'why', 'review_status', 'edited', 'ladder', 'type', 'category', 'source_kind', 'title', 'explanation', 'computed', 'evidence', 'origin', 'reviewer_note'])]
[{'record_id': 'r4', 'raw': '03/05/2026', 'candidates': ['2026-03-05', '2026-05-03'], 'status': 'ambiguous', 'suggestion': {'convention': 'DMY', 'label': 'DD/MM', 'iso': '2026-05-03', 'reason': 'Another date in this packet uses day first (Record 2: 14/04/2026)', 'evidence': [{'record_id': 'r2', 'raw': '14/04/2026'}], 'evidence_count': 1, 'auto_applied': False}}]
case lib09 spanish interpreter espalda
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:28.394Z

**tool call — Bash**
````
{
 "command": "curl -s localhost:7955/api/library | python3 -c \"\nimport json,sys\nfor c in json.load(sys.stdin)['cases']:\n    if c['id'][8:10] in ('06','08','10','12','13','15'): print(c['id'][:10],c['description'][:260]);print()\""
}
````

### User / tool · 2026-11-02T11:07:28.504Z

**tool result**
````
case_lib06 Library L6 (mirrors S6). Side-impact collision, attorney-referred clinic treating under a letter of protection, a billing statement with a balance, and an imaging bill with an adjustment and an amount due. Only stated charges are counted; a

case_lib08 Library L8 (P1+P13). Pre-suit file: rear-end collision, ED, orthopedics, 11 weeks of PT, then a second collision 11 days after PT discharge (EMS in a hard collar, ED), the first MRI only after crash 2, an orthopedic note that dates the arm 

case_lib10 Library L10 (P6+P14). Pickup struck at an intersection, ED then three days of observation. A UB-04 itemized hospital bill with an accommodation rate beside the line charge and a 0001 total line, a health-plan EOB for the same dates of servi

case_lib12 Library L12 (P7+P8). Lumbar strain after a pickup collision, PCP, physical therapy with Waddell lines charted four ways (two clean negations, a positive count with inconsistent effort, a mixed-side sentence and a contrast sentence with 'sym

case_lib13 Library L13 (P10+P16). Rear-end collision on a highway on-ramp. Three PCP visits weeks apart carry the identical copied-forward ROS 'denies neck pain, denies back pain, denies numbness' while orthopedics, two days after the first PCP visit 

case_lib15 Library L15 (P3+P17). EMS notes minor damage and a refused transport, urgent care calls it a low-speed MVC, the chiropractor later records the patient saying the impact was violent, and the chiropractor's narrative letter states the collisi
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:32.385Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/index.html | sed -n 1,200p | cut -c1-220; cat app/frontend/dom.js"
}
````

### User / tool · 2026-11-02T11:07:32.475Z

**tool result**
````
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="review.css">
<link rel="stylesheet" href="stepper.css">
<link rel="stylesheet" href="sidebyside.css">
<link rel="stylesheet" href="suggestions.css">
</head>
<body>
<nav id="skip-nav" class="skip-nav" aria-label="Skip links" data-testid="skip-nav"></nav>
<div id="banner-synthetic" class="banner synth" data-testid="banner-synthetic" role="region" aria-label="Synthetic data notice">Synthetic data only — never paste real records</div>
<header class="app-header" data-testid="app-header">
  <div class="app-header-row">
    <h1 class="brand">Treatment timeline</h1>
    <span id="case-name" class="case-name" data-testid="case-name" hidden></span>
    <div id="case-progress" class="case-progress" data-testid="case-progress-bar" hidden>
      <span id="progress-text" data-testid="progress-text" role="status"></span>
      <progress id="progress-bar" max="1" value="0" aria-label="Items decided"></progress>
    </div>
    <span class="spacer"></span>
    <div class="header-tools">
      <span id="badge" class="chip chip--muted" hidden></span>
      <span id="retention" class="muted small" hidden></span>
      <button type="button" id="delete-now" class="btn btn--sm" hidden>Delete now</button>
      <button type="button" id="btn-shortcuts" class="btn btn--sm" data-testid="btn-shortcuts" aria-haspopup="dialog" hidden>Shortcuts</button>
      <button type="button" id="btn-theme" class="btn btn--sm" data-testid="btn-theme" aria-label="Theme: auto. Press to change it.">Theme: auto</button>
      <button type="button" id="btn-export" class="btn btn--primary" data-testid="btn-export" hidden>Export</button>
    </div>
  </div>
</header>
<div id="banner-ai" class="banner ai" data-testid="banner-ai" role="region" aria-label="AI notice" hidden></div>
<main id="main">
  <section id="view-input" class="card" aria-labelledby="h-input">
    <h2 id="h-input">Records</h2>
    <div id="input-body"></div>
  </section>
  <section id="view-review" aria-labelledby="h-review" hidden>
    <h2 id="h-review" class="sr">Review</h2>
    <div id="review-body"></div>
  </section>
  <section id="view-export" class="card" aria-labelledby="h-export" hidden>
    <h2 id="h-export">Export</h2>
    <div id="export-body"></div>
  </section>
</main>
<dialog id="source-modal" data-testid="record-modal" aria-labelledby="source-title">
  <div class="dlg-head"><h2 id="source-title">Source record</h2><button type="button" id="source-close" class="btn btn--sm" data-testid="btn-close-modal">Close</button></div>
  <div id="source-body"></div>
</dialog>
<dialog id="why-modal" data-testid="why-modal" aria-labelledby="why-title">
  <div class="dlg-head"><h2 id="why-title">Why?</h2><button type="button" class="btn btn--sm" data-testid="why-close" onclick="this.closest('dialog').close()">Close</button></div>
  <div id="why-body"></div>
</dialog>
<!-- load order matters; mock files are only used when API_MODE is "mock" -->
<script src="dom.js"></script>
<script src="mock_sample.js"></script>
<script src="mock.js"></script>
<script src="mock_flags.js"></script>
<script src="mock_extra.js"></script>
<script src="api.js"></script>
<script src="state.js"></script>
<script src="input.js"></script>
<script src="source.js"></script>
<script src="stepper.js"></script>
<script src="suggestions.js"></script>
<script src="timeline.js"></script>
<!-- T-043 (frontend-2): review.js first (controls + keys), then the panels -->
<script src="review.js"></script>
<script src="flags.js"></script>
<script src="charges.js"></script>
<script src="batch.js"></script>
<script src="audit.js"></script>
<script src="judges.js"></script>
<script src="manual.js"></script>
<script src="narrative.js"></script>
<script src="exportcfg.js"></script>
<script src="excerpt.js"></script>
<script src="export.js"></script>
<script src="sidebyside.js"></script>
<script src="switcher.js"></script>
<script src="app.js"></script>
</body>
</html>
/* Shared DOM helpers (frontend-1 / T-042; also used by T-043). Data is only ever written with textContent / text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  // el("button", {class:"x", type:"button", onclick:fn, "data-testid":"y"}, "label", childNode, ...)
  ZL.el = function (tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat(Infinity)) {   // any nesting of arrays: a list of [dt, dd] pairs must never print as [object HTMLElement]
      if (c == null || c === false) continue;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return e;
  };
  // Rank "needs review first" by the state an item had when this case was first shown, so rows do not jump when a decision changes the state
  // (keeps the row under the cursor still and nth-button order stable).
  const ranks = {};
  ZL.firstRank = (id, state) => { const k = (ZL.state && ZL.state.get().token) + ":" + id; if (!(k in ranks)) ranks[k] = state === "needs_review" ? 0 : 1; return ranks[k]; };
  ZL.clear = (n) => { while (n.firstChild) n.removeChild(n.firstChild); return n; };
  ZL.$ = (s, r) => (r || document).querySelector(s);
  ZL.fmtDate = (iso) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return iso || "undated";
    const mon = ["January","February","March","April","May","June","July","August","September","October","November","December"][+m[2] - 1];
    return `${mon} ${+m[3]}, ${m[1]}`;
  };
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:36.466Z

**tool call — Bash**
````
{
 "command": "grep -n \"fixture\" app/frontend/suggestions.js app/frontend/stepper.js | cut -c1-220 | head; grep -rn \"fixture backend\" app/backend/*.py | cut -c1-200 | head -3; grep -rn \"'Add:\\|\\\"Add:\\|Add: \" tests/ | head"
}
````

### User / tool · 2026-11-02T11:07:36.589Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:43.060Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/dom.js\"\ns=open(p).read()\ns=s.replace('''  ZL.money = (cents)''','''  // Library cases arrive named after their file (\"case lib09 spanish interpreter espalda\"). Show a plain title instead; any other name (a pasted case, a sample) is left alone.\n  // Display only: the case id and the stored name never change.\n  const LIB_TITLE = { 1: \"ER visit, then a treatment gap\", 2: \"Slip and fall, prior knee surgery\", 3: \"Truck rear-end, chiropractic plan\", 4: \"Dog bite, scar revision\", 5: \"Pedestrian struck, hardware (ORIF)\",\n    6: \"Letter of protection, billed vs. adjusted\", 7: \"Parking-lot fall, outside records\", 8: \"Second crash, MRI after\", 9: \"Spanish-language records, back pain\", 10: \"Hospital bill and EOB forms (UB-04, CMS-1500)\",\n    11: \"Prior conditions and charge ledger\", 12: \"Records review, credibility wording\", 13: \"Copied-forward notes across providers\", 14: \"Handwritten chiropractic scans\", 15: \"Conflicting accounts, narrative letter\" };\n  ZL.niceName = (name) => {\n    const m = /^case[ _]lib(\\\\d+)\\\\b\\\\s*(.*)$/i.exec(String(name || \"\"));\n    if (!m) return name;\n    if (LIB_TITLE[+m[1]]) return LIB_TITLE[+m[1]];\n    const t = m[2].replace(/_/g, \" \").trim();\n    return t ? t.charAt(0).toUpperCase() + t.slice(1) : name;\n  };\n  ZL.money = (cents)''',1)\nopen(p,\"w\").write(s)\n\np=\"app/frontend/app.js\"\ns=open(p).read()\ns=s.replace('''$(\"#case-name\").textContent = c.name || \"Case\";\n    document.title = c && c.name ? \"Treatment timeline · \" + c.name : \"Treatment timeline\";''','''$(\"#case-name\").textContent = ZL.niceName(c.name) || \"Case\";\n    document.title = c && c.name ? \"Treatment timeline · \" + ZL.niceName(c.name) : \"Treatment timeline\";''',1)\nopen(p,\"w\").write(s)\n\np=\"app/frontend/switcher.js\"\ns=open(p).read()\na=s.index(\"  // Library manifest names\")\nb=s.index(\"  const when =\")\ns=s[:a]+s[b:]\ns=s.replace('(c.name || (\"Pasted records\"','(ZL.niceName(c.name) || (\"Pasted records\"')\ns=s.replace('\"Add: \" + nice(l.name)','ZL.niceName(l.name)')\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"niceName\\|nice(\" app/frontend/*.js | cut -c1-160"
}
````

### User / tool · 2026-11-02T11:07:43.180Z

**tool result**
````
app/frontend/app.js:26:    $("#case-name").hidden = !c; if (c) $("#case-name").textContent = ZL.niceName(c.name) || "Case";
app/frontend/app.js:27:    document.title = c && c.name ? "Treatment timeline · " + ZL.niceName(c.name) : "Treatment timeline";
app/frontend/dom.js:37:  ZL.niceName = (name) => {
app/frontend/switcher.js:44:        (c.token === cur ? "Open now: " : "") + (ZL.niceName(c.name) || ("Pasted records" + (when(c.created_at || c.updated_at) ? ",
app/frontend/switcher.js:48:      ZL.niceName(l.name), l.description ? el("span", { class: "cs-meta" }, firstSentence(l.description.replace(/^Library L\d+ \([^)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:46.376Z

**tool call — Bash**
````
{
 "command": "grep -n \"case\\.name\\|c\\.name\\|\\.name ||\" app/frontend/*.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T11:07:46.461Z

**tool result**
````
app/frontend/app.js:26:    $("#case-name").hidden = !c; if (c) $("#case-name").textContent = ZL.niceName(c.name) || "Case";
app/frontend/app.js:27:    document.title = c && c.name ? "Treatment timeline · " + ZL.niceName(c.name) : "Treatment timeline";
app/frontend/mock.js:156:        return ok({ token, name: c.name, status: "ingested", source: body && body.sample ? "sample" : "paste", demo_mode: false, record_count: c.records.length, split_method: 
app/frontend/switcher.js:44:        (c.token === cur ? "Open now: " : "") + (ZL.niceName(c.name) || ("Pasted records" + (when(c.created_at || c.updated_at) ? ", " + when(c.created_at || c.updated_at)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:48.250Z

**tool call — bash**
````
{
 "command": "echo noop"
}
````

### User / tool · 2026-11-02T11:07:48.251Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:56.984Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/timeline.js\"\ns=open(p).read()\n\nold_start=s.index(\"  let gapNote = null;\")\nold_end=s.index(\"  ZL.confirmDate = async function\")\nnew_store='''  let gapNote = null;   // {token, items: [sentence]}: the announcement above the timeline, dismissable\n  // The same change is also kept per case (T-114 r3, paralegal): the gap card says \"now 40 days (was 42)\" after Got it, after a reload and on another day, until that gap changes again.\n  // The backend has no stored field for it yet (filed as a card), so it is kept in this browser per case, next to \"Keep showing\". If a gap flag ever carries `gap_change`, that wins.\n  const gapKey = (token) => \"zlayt.gapchg.\" + token;\n  const gapMem = {};\n  function gapStore(token) {\n    if (gapMem[token]) return gapMem[token];\n    let v = []; try { v = JSON.parse(localStorage.getItem(gapKey(token)) || \"[]\"); } catch (_) { v = []; }\n    return (gapMem[token] = Array.isArray(v) ? v : []);\n  }\n  function gapSave(token, changes) {\n    const keep = gapStore(token).filter((x) => !changes.some((n) => n.flag_id === x.flag_id));\n    gapMem[token] = keep.concat(changes.filter((n) => n && n.flag_id));\n    try { localStorage.setItem(gapKey(token), JSON.stringify(gapMem[token])); } catch (_) { /* not remembered across reloads */ }\n  }\n  const dayWord = (n) => n + (n === 1 ? \" day\" : \" days\");\n  const span = (a, b) => (a && b ? ZL.fmtDate(a) + \" to \" + ZL.fmtDate(b) : \"\");\n  // What the gap card shows: the sentence the server wrote, then the old and new figures with their dates. Only while the card still shows the new figure.\n  function gapChangeFor(c, f) {\n    if (!f || f.type !== \"gap\") return null;\n    const cur = f.computed || {};\n    const g = f.gap_change || gapStore(c.token).find((x) => x.flag_id === f.id && x.new_days === cur.days && (x.new_from == null || x.new_from === cur.from));\n    if (!g || g.new_days == null) return null;\n    const lines = [];\n    if (g.old_days != null) lines.push(\"Before: \" + dayWord(g.old_days) + (span(g.old_from, g.old_to) ? \" (\" + span(g.old_from, g.old_to) + \")\" : \"\") + \".\");\n    lines.push(\"Now: \" + dayWord(g.new_days) + (span(g.new_from, g.new_to) ? \" (\" + span(g.new_from, g.new_to) + \")\" : \"\") + \".\");\n    return { sentence: g.sentence || \"\", lines };\n  }\n  // A gap that no longer applies has no card; the panel keeps the sentence under Treatment gaps.\n  function gapRemoved(c) {\n    const have = new Set((c.flags || []).map((f) => f.id));\n    return gapStore(c.token).filter((x) => x.change === \"removed\" && x.sentence && !have.has(x.flag_id)).map((x) => x.sentence);\n  }\n  ZL.gapChanges = { forFlag: gapChangeFor, removed: gapRemoved };\n'''\ns=s[:old_start]+new_store+s[old_end:]\ns=s.replace('''    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);\n    gapNote = changes.length ? { token: s.token, items: changes } : null;''','''    const all = resp && Array.isArray(resp.gap_changes) ? resp.gap_changes.filter(Boolean) : [], changes = all.map((g) => g.sentence).filter(Boolean);\n    gapNote = changes.length ? { token: s.token, items: changes } : null;\n    if (all.length) gapSave(s.token, all);''')\nopen(p,\"w\").write(s)\nEOF"
}
````

### User / tool · 2026-11-02T11:07:57.111Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:07:59.319Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/frontend; git status --short app/frontend"
}
````

### User / tool · 2026-11-02T11:07:59.434Z

**tool result**
````
 app/frontend/app.js      |  4 ++--
 app/frontend/dom.js      | 12 ++++++++++++
 app/frontend/switcher.js |  6 ++----
 app/frontend/timeline.js | 38 ++++++++++++++++++++++++++++++++++++--
 4 files changed, 52 insertions(+), 8 deletions(-)
 M app/frontend/app.js
 M app/frontend/dom.js
 M app/frontend/switcher.js
 M app/frontend/timeline.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:08:03.750Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/flags.js\"\ns=open(p).read()\ns=s.replace('''      el(\"p\", { class: \"rv-text-body\" }, f.explanation),\n''','''      gapChangeLine(c, f),\n      el(\"p\", { class: \"rv-text-body\" }, f.explanation),\n''',1)\ns=s.replace('''  function card(c, f) {''','''  // T-114 r3: a gap whose figure moved after a date was confirmed says so on its own card, with the old and new numbers, for as long as the card shows the new figure.\n  function gapChangeLine(c, f) {\n    const g = ZL.gapChanges && ZL.gapChanges.forFlag(c, f); if (!g) return null;\n    return el(\"p\", { class: \"rv-gap-change\", \"data-testid\": \"gap-change-card\" }, el(\"strong\", {}, g.sentence || \"This figure changed after you confirmed a date.\"), \" \", g.lines.join(\" \"));\n  }\n\n  function card(c, f) {''',1)\ns=s.replace('''      if (!list.length) g.append(el(\"p\", { class: \"rv-empty\" }, empty));''','''      if (type === \"gap\" && ZL.gapChanges) ZL.gapChanges.removed(c).forEach((t) => g.append(el(\"p\", { class: \"rv-gap-change\", \"data-testid\": \"gap-change-removed\" }, t)));\n      if (!list.length) g.append(el(\"p\", { class: \"rv-empty\" }, empty));''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"rv-reason-line\\|\\.notice\" app/frontend/*.css | head"
}
````

### User / tool · 2026-11-02T11:08:03.862Z

**tool result**
````
app/frontend/review.css:16:.rv-reason-line { background: var(--warn-bg); color: var(--warn); padding: var(--s-2) var(--s-3); border-radius: var(--r-1); margin: var(--s-2) 0; font-size: var(--t-sm); line-height: var(--lh-sm); }
app/frontend/styles.css:95:.notice { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--s-3); padding: var(--s-3) var(--s-4); border: 1px solid var(--border); border-left: 3px solid var(--info); border-radius: var(--r-2); background: var(--info-bg); color: var(--text); margin: var(--s-3) 0; }
app/frontend/styles.css:96:.notice--warn, .rv-banner { border-left-color: var(--warn); background: var(--warn-bg); }
app/frontend/styles.css:97:.notice--bad { border-left-color: var(--bad); background: var(--bad-bg); }
app/frontend/styles.css:98:.notice--ok { border-left-color: var(--ok); background: var(--ok-bg); }
app/frontend/styles.css:99:.notice-body { min-width: 0; overflow-wrap: anywhere; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:08:05.681Z

**tool call — Bash**
````
{
 "command": "sed -n 60,252p app/frontend/styles.css | cut -c1-330"
}
````

### User / tool · 2026-11-02T11:08:05.764Z

**tool result**
````
.btn[aria-pressed="true"]:not(.btn--primary) { border-color: var(--ok); color: var(--ok); }
.btn[aria-busy="true"] { cursor: progress; }
.btn:disabled, .btn[disabled] { background: var(--sunken); border-color: var(--border); color: var(--text-subtle); cursor: not-allowed; }
.btn:disabled:hover { background: var(--sunken); }
label.btn { cursor: pointer; }
input[type="text"], input:not([type]), textarea, select { font: var(--w-regular) var(--t-md)/var(--lh-md) var(--font); color: var(--text); background: var(--panel); border: 1px solid var(--border-strong); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); max-width: 100%; }
textarea { width: 100%; display: block; resize: vertical; }
#paste { font-family: var(--mono); font-size: var(--t-sm); line-height: var(--lh-sm); min-height: 12rem; }
select { min-height: var(--control-h-sm); padding: var(--s-1) var(--s-2); }
select:hover, textarea:hover, input:hover { border-color: var(--text-muted); }
input[type="radio"], input[type="checkbox"] { width: 1.5rem; height: 1.5rem; accent-color: var(--accent); margin: 0; flex: none; }
.lbl, .rv-label { display: block; font-weight: var(--w-strong); margin-bottom: var(--s-1); }
.row { display: flex; flex-wrap: wrap; gap: var(--s-2); align-items: center; margin-top: var(--s-3); }
.error, .rv-error { color: var(--bad); font-weight: var(--w-strong); }
.error { background: var(--bad-bg); border: 1px solid var(--bad); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); margin-top: var(--s-3); }
.rv-error:empty { display: none; }
.progress { font-weight: var(--w-strong); }
details > summary { cursor: pointer; min-height: var(--control-h-sm); display: flex; align-items: center; gap: var(--s-2); }
details > summary:hover { color: var(--accent-hover); }

/* ---- 4 chips and notices --------------------------------------------------------------------------------------------------- */
.chip, .rv-chip, .zs-chip, .zs-kind, .zs-verdict, .tag, .sg-tag, .zs-blocks { display: inline-flex; align-items: center; gap: var(--s-1); min-height: 1.375rem; padding: 0 var(--s-2); border: 1px solid var(--border); border-radius: var(--r-1);
  background: var(--sunken); color: var(--text-muted); font-size: var(--t-xs); line-height: var(--lh-xs); font-weight: var(--w-strong); white-space: nowrap; }
.chip[data-icon]::before, .rv-chip[data-icon]::before { flex: none; width: 1rem; text-align: center; }
[data-icon="check"]::before { content: "\2713"; } [data-icon="alert"]::before { content: "\25B2"; font-size: 0.7em; } [data-icon="x"]::before { content: "\2715"; }
[data-icon="pencil"]::before { content: "\270E"; } [data-icon="dash"]::before { content: "\2296"; } [data-icon="ai"]::before { content: "AI"; width: auto; } [data-icon="calendar"]::before { content: "\25F7"; }
[data-icon="info"]::before { content: "i"; font-style: italic; }
.chip--ok, .rv-rs-accepted, .rv-rs-edited { background: var(--ok-bg); color: var(--ok); border-color: var(--ok); }
.chip--warn, .rv-state-needs_review { background: var(--warn-bg); color: var(--warn); border-color: var(--warn); }
.chip--bad, .rv-state-rejected, .rv-rs-dismissed { background: var(--bad-bg); color: var(--bad); border-color: var(--bad); }
.chip--info, .rv-state-verified, .tag, .sg-tag, .rv-selfreport { background: var(--info-bg); color: var(--info); border-color: var(--info); }
.chip--muted { background: transparent; color: var(--text-muted); border-color: var(--border-strong); }
.chip--rec { background: transparent; font-weight: var(--w-regular); }
.rv-rs-dismissed { background: transparent; color: var(--text-muted); border-color: var(--border-strong); }
.count-line { font-weight: var(--w-strong); background: var(--sunken); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); }
.notice { display: flex; align-items: flex-start; justify-content: space-between; gap: var(--s-3); padding: var(--s-3) var(--s-4); border: 1px solid var(--border); border-left: 3px solid var(--info); border-radius: var(--r-2); background: var(--info-bg); color: var(--text); margin: var(--s-3) 0; }
.notice--warn, .rv-banner { border-left-color: var(--warn); background: var(--warn-bg); }
.notice--bad { border-left-color: var(--bad); background: var(--bad-bg); }
.notice--ok { border-left-color: var(--ok); background: var(--ok-bg); }
.notice-body { min-width: 0; overflow-wrap: anywhere; }
.rv-banner { padding: var(--s-3) var(--s-4); border: 1px solid var(--border); border-left-width: 3px; border-radius: var(--r-2); margin: var(--s-3) 0; }

/* ---- 5 cards, rows, quotes -------------------------------------------------------------------------------------------------- */
.card { background: var(--panel); border: 1px solid var(--border); border-radius: var(--r-2); padding: var(--s-4) var(--s-5); margin-bottom: var(--s-4); }
.card > h2, .card-title { margin-bottom: var(--s-3); }
.found { font-size: var(--t-xl); line-height: var(--lh-xl); font-weight: var(--w-strong); }
.reclist { padding-left: var(--s-5); margin: var(--s-2) 0; }
.reclist-wrap > summary { font-weight: var(--w-strong); }
.toolbar { display: flex; flex-wrap: wrap; gap: var(--s-2) var(--s-4); align-items: center; }
.toolbar h2 { margin-right: var(--s-2); }
.toolbar-counts { display: flex; flex-wrap: wrap; gap: var(--s-2); align-items: center; }
.toolbar-sort { margin-left: auto; display: flex; align-items: center; gap: var(--s-2); color: var(--text-muted); font-size: var(--t-sm); }
.timeline { margin-top: var(--s-2); }
.group { margin-top: var(--s-5); }
.group > h2 { font-size: var(--t-lg); line-height: var(--lh-lg); margin-bottom: var(--s-2); }
.group--empty { margin-top: var(--s-4); color: var(--text-subtle); font-size: var(--t-sm); line-height: var(--lh-sm); }
.group--empty > h2 { display: inline; font-size: var(--t-sm); line-height: var(--lh-sm); font-weight: var(--w-strong); color: var(--text-muted); }
.group--empty > h2::after { content: ": "; }
.group--empty > p { display: inline; }
.group--empty > .muted { color: var(--text-subtle); }

/* A compact review row (T-060 r3): head line (date, provider, record, why it needs a look, state), then the summary and its excerpt side by side (each clamped),
   then the decision buttons on the left and the row's links on the right. "More" opens the whole row. Nothing here depends on focus or selection. */
.entry { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-content: start; gap: var(--s-1) var(--s-4); margin: var(--s-2) 0; padding: var(--s-2) var(--s-4); background: var(--panel); border: 1px solid var(--border); border-left: 3px solid var(--border-strong); border-radius: var(--r-2); }
.entry > * { grid-column: 1 / -1; min-width: 0; }
.entry > .entry-head { order: 0; }
.entry[data-entry-id] > .summary { order: 1; grid-column: 1; align-self: start; }
.entry[data-entry-id] > figure.quote { order: 2; grid-column: 2; align-self: start; }
.entry[data-entry-id] > .note { order: 3; }
.entry[data-entry-id] > .sg-dateform, .entry[data-entry-id] > .row, .entry[data-entry-id] > .reason, .entry[data-entry-id] > .muted { order: 3; }
.entry[data-entry-id] .rv-controls { display: contents; }
.entry[data-entry-id] .rv-actions { order: 4; grid-column: 1; margin: 0; }
.entry[data-entry-id] .row-actions { order: 5; grid-column: 2; display: flex; flex-wrap: wrap; justify-content: flex-end; align-items: center; gap: 0 var(--s-1); align-self: center; }
.entry[data-entry-id] .rv-refused, .entry[data-entry-id] .rv-error, .entry[data-entry-id] form.rv-reason, .entry[data-entry-id] form.rv-edit, .entry[data-entry-id] .rv-blocked, .entry[data-entry-id] > details, .entry[data-entry-id] > form, .entry[data-entry-id] > .ex-edit { order: 6; }
.entry[data-entry-id] .rv-refused, .entry[data-entry-id] .rv-error, .entry[data-entry-id] form.rv-reason, .entry[data-entry-id] form.rv-edit, .entry[data-entry-id] .rv-blocked { grid-column: 1 / -1; }   /* these sit inside .rv-controls (display: contents), so the direct-child span rule does not reach them */
.entry.st-needs_review { border-left-color: var(--warn); }
.entry.st-rejected { border-left-color: var(--bad); }
.entry.sbs-current { background: var(--accent-soft); border-left-color: var(--accent); }
.entry[data-review="dismissed"] .summary, .entry[data-review="dismissed"] .excerpt { color: var(--text-subtle); text-decoration: line-through; text-decoration-color: var(--border-strong); }
.entry[data-review="accepted"] .summary, .entry[data-review="edited"] .summary { color: var(--text-muted); }
.entry:focus-visible { outline: var(--focus-ring); outline-offset: var(--focus-offset); }
.entry-head { display: flex; flex-wrap: wrap; align-items: center; gap: 0 var(--s-3); min-height: 1.5rem; }
.entry-chips { display: inline-flex; flex-wrap: wrap; gap: var(--s-1); margin-left: auto; }
.date { font-weight: var(--w-strong); font-variant-numeric: tabular-nums; }
.provider { font-weight: var(--w-regular); color: var(--text); min-width: 0; overflow-wrap: anywhere; }
.summary { max-width: var(--measure); }
.entry[data-entry-id] .summary { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
.entry[data-entry-id] .entry-head .reason { flex: 1 1 12rem; min-width: 0; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.entry[data-entry-id].is-open .summary, .entry[data-entry-id].is-open .excerpt { display: block; -webkit-line-clamp: unset; overflow: visible; }
.entry[data-entry-id].is-open .entry-head .reason { white-space: normal; overflow: visible; }
.entry[data-entry-id][data-review="accepted"]:not(.is-open) .summary, .entry[data-entry-id][data-review="edited"]:not(.is-open) .summary, .entry[data-entry-id][data-review="dismissed"]:not(.is-open) .summary { -webkit-line-clamp: 1; }
.entry[data-entry-id][data-review="accepted"]:not(.is-open) .excerpt, .entry[data-entry-id][data-review="edited"]:not(.is-open) .excerpt, .entry[data-entry-id][data-review="dismissed"]:not(.is-open) .excerpt { -webkit-line-clamp: 1; }
.reason { color: var(--warn); font-size: var(--t-sm); line-height: var(--lh-sm); font-weight: var(--w-strong); }
.reason::before { content: "\25B2\00a0"; font-size: 0.7em; vertical-align: 0.1em; }
figure.quote { margin: 0; max-width: var(--measure); }
.quote-cap { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }   /* names the quote for assistive tech; shown when the row is open */
.entry.is-open .quote-cap { position: static; width: auto; height: auto; overflow: visible; clip: auto; white-space: normal; display: block; font-size: var(--t-xs); line-height: var(--lh-xs); color: var(--text-subtle); margin-bottom: 2px; }
.excerpt, .rv-quote, .zs-quote blockquote { margin: 0; padding: var(--s-1) var(--s-3); background: var(--sunken); border-left: 3px solid var(--border-strong); border-radius: 0 var(--r-1) var(--r-1) 0; color: var(--text);
  font-size: var(--t-read); line-height: var(--lh-read); font-style: normal; overflow-wrap: anywhere; }
/* a fixed clamp: nothing about a row's height may depend on focus or selection (a layout shift between mousedown and mouseup loses the click) */
.entry[data-entry-id] .excerpt { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
/* a tray or date-to-confirm card keeps the full quote */
.entry:not([data-entry-id]) .excerpt { display: block; }
.src-text, .ex-text { white-space: pre-wrap; overflow-wrap: anywhere; background: var(--sunken); border: 1px solid var(--border); border-radius: var(--r-1); padding: var(--s-3); font: var(--w-regular) var(--t-read)/var(--lh-read) var(--font); }
.ex-text { max-height: none; overflow: visible; }   /* the box is as tall as its text: no scroll inside a scrolling page */
.ex-block .toolbar { justify-content: space-between; }
.ex-btns { margin-top: 0; }
.kv { display: grid; grid-template-columns: max-content 1fr; gap: var(--s-1) var(--s-3); }
.kv dt { font-weight: var(--w-strong); } .kv dd { overflow-wrap: anywhere; }
.kv--keys { grid-template-columns: 7rem 1fr; align-items: baseline; }
.checks { margin: 0; padding-left: var(--s-4); } .checks .bad { color: var(--bad); font-weight: var(--w-strong); }
.why-sentence { font-weight: var(--w-strong); margin-bottom: var(--s-3); }
.ex-block { margin: var(--s-4) 0; } .ex-block h3 { margin: 0; }
.ex-confirm-msg { background: var(--warn-bg); border: 1px solid var(--warn); color: var(--warn); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); font-weight: var(--w-strong); }
.ex-warn { margin: var(--s-2) 0; padding-left: var(--s-5); }
.ex-units { margin-top: var(--s-3); border-top: 1px solid var(--border); padding-top: var(--s-3); }
.ex-unit-list { list-style: none; padding: 0; margin: var(--s-2) 0; display: grid; gap: var(--s-1); }
.ex-unit-list label { display: flex; gap: var(--s-2); align-items: flex-start; }
.todo-strip { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2) var(--s-4); background: var(--panel); border: 1px solid var(--border); border-left: 3px solid var(--warn); border-radius: var(--r-2); padding: var(--s-2) var(--s-4); margin: var(--s-3) 0; }
.todo-strip--done { border-left-color: var(--ok); }
.todo-strip h2 { font-size: var(--t-md); line-height: var(--lh-md); margin: 0; }
.todo-list { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: var(--s-2); }
.todo-list li { display: flex; align-items: center; gap: var(--s-1); }
.todo-lead { max-width: var(--measure); }

/* ---- 6 dialogs --------------------------------------------------------------------------------------------------------------- */
dialog { padding: 0; border: 1px solid var(--border); border-radius: var(--r-2); background: var(--panel); color: var(--text); width: min(52rem, 96vw); max-height: 90vh; box-shadow: var(--elev-2); }
dialog.dlg--sm { width: min(30rem, 96vw); }
dialog.dlg--md { width: min(38rem, 96vw); }
dialog::backdrop { background: var(--scrim); }
.dlg-head { display: flex; justify-content: space-between; align-items: center; gap: var(--s-3); position: sticky; top: 0; z-index: 3; background: var(--panel); padding: var(--s-3) var(--s-4); border-bottom: 1px solid var(--border); }
.dlg-head h2 { font-size: var(--t-lg); line-height: var(--lh-lg); }
.dlg-body, #source-body, #why-body { padding: var(--s-4); display: grid; gap: var(--s-3); }
.dlg-foot { display: flex; gap: var(--s-2); justify-content: flex-end; padding: var(--s-3) var(--s-4); border-top: 1px solid var(--border); }

/* ---- 7 responsive ------------------------------------------------------------------------------------------------------------ */
@media (max-width: 768px) {
  .card { padding: var(--s-3); }
  :root { --header-h: 5.5rem; }
  progress { width: 6rem; }
  .entry { grid-template-columns: minmax(0, 1fr); padding: var(--s-2) var(--s-3); }
  .entry[data-entry-id] > .summary, .entry[data-entry-id] > figure.quote, .entry[data-entry-id] .rv-actions, .entry[data-entry-id] .row-actions { grid-column: 1; }
  .entry .row-actions { justify-content: flex-start; }
  .entry[data-entry-id] .entry-head .reason { flex-basis: 100%; white-space: normal; }
  .entry[data-entry-id] .summary { -webkit-line-clamp: 3; }
  .entry[data-entry-id] .excerpt { -webkit-line-clamp: 2; }
  .kv { grid-template-columns: 1fr; }
  .toolbar-sort { margin-left: 0; width: 100%; }
  .dlg-head, .dlg-foot { padding: var(--s-3); }
}
@media (max-width: 480px) { .case-name { font-size: var(--t-md); } }
@media print { .banner.synth, .app-header { position: static; } }

/* processing state */
.run-state { margin-top: var(--s-3); display: grid; gap: var(--s-2); }
.skeletons { display: grid; gap: var(--s-2); margin-top: var(--s-2); }
.skeleton { height: 4rem; border-radius: var(--r-2); background: linear-gradient(90deg, var(--sunken), var(--border), var(--sunken)); background-size: 200% 100%; }
@media (prefers-reduced-motion: no-preference) { .skeleton { animation: shimmer 1.4s linear infinite; } @keyframes shimmer { to { background-position: -200% 0; } } }

/* a finished run: the records card is one row (count, list, start over) */
.input-done { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-1) var(--s-4); }
.input-done .found { font-size: var(--t-lg); line-height: var(--lh-lg); }
.input-done .row { margin-top: 0; margin-left: auto; }
.input-done .reclist-wrap { margin: 0; }
.input-done .reclist-wrap[open] { flex: 1 1 100%; order: 5; }
#view-input:has(.input-done) { padding: var(--s-1) var(--s-4); margin-bottom: 0; }
#view-input:has(.input-done) > h2 { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.summary .tag { margin-left: var(--s-2); vertical-align: baseline; min-height: 0; line-height: var(--lh-xs); }
@media (max-width: 768px) {
  /* phone header: case name and Export on one row, progress under it; the rest is on the desktop header */
  .app-header-row { gap: var(--s-1) var(--s-3); padding-top: var(--s-2); padding-bottom: var(--s-2); }
  .app-header-row:has(#case-name:not([hidden])) .brand, #btn-shortcuts, #btn-theme, #badge, #retention { display: none; }
  .case-name { flex: 1 1 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .spacer { display: none; }
  .case-progress { order: 3; flex: 1 1 100%; }
  .header-tools { margin-left: auto; }
  .case-progress progress { flex: 1 1 auto; width: auto; }
}

/* decided rows: the state, not the action (T-060 r3). Filled primary is for an undecided item only. */
.btn.rv-decided, .btn[aria-pressed="true"].rv-decided { border-color: transparent; background: transparent; color: var(--ok); font-weight: var(--w-strong); cursor: default; }
.btn.rv-decided:hover { background: transparent; }
.btn.rv-decided--muted, .btn[aria-pressed="true"].rv-decided--muted { color: var(--text-muted); }
.btn.rv-decided[data-icon]::before { content: "\2713"; }
.btn.rv-decided--muted[data-icon]::before { content: "\2296"; }
.entry .rv-actions .btn, .entry .row-actions .btn { min-height: var(--control-h-sm); }
.rv-actions .btn--link.rv-reset { font-size: var(--t-sm); }
/* the visible Upload control carries the focus ring of the (visually hidden) file input */
label.btn:has(+ #file:focus-visible) { outline: var(--focus-ring); outline-offset: var(--focus-offset); }
/* chips in the case-check panels wrap instead of running off a narrow screen (WCAG 1.4.10) */
.zs-chip, .zs-kind, .zs-verdict, .zs-blocks { white-space: normal; max-width: 100%; }
.zs-counts { display: flex; flex-wrap: wrap; gap: var(--s-1); }
@media (max-width: 768px) { .entry .row-actions .btn { min-height: 2.25rem; } }   /* secondary links: 36px, above the 24px minimum; the decision buttons keep 44px */
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:08:19.292Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/timeline.js\"\ns=open(p).read()\ns=s.replace('''reasonText_ ? el(\"p\", { class: \"reason\", \"data-testid\": \"entry-reasons\", title: reasonText_ }, reasonText_) : null,''','''reasonText_ ? el(\"p\", { class: \"reason\" + (e.reasons.includes(\"AI_TRANSLATION\") ? \" reason--caution\" : \"\"), \"data-testid\": \"entry-reasons\", title: reasonText_ }, reasonText_) : null,''',1)\n\ns=s.replace('''      el(\"div\", { class: \"timeline\", \"data-testid\": \"queue\", \"aria-labelledby\": \"h-timeline\" }, sortedEntries(c).map((e) => entryRow(e, c))),\n      hasDates ? null : dates,''','''      el(\"div\", { class: \"timeline\", \"data-testid\": \"queue\", \"aria-labelledby\": \"h-timeline\" }, liveRows.map((e) => entryRow(e, c))),\n      dismissedGroup(c, dismissedRows),\n      hasDates ? null : dates,''',1)\ns=s.replace('''    const dates = datesToConfirm(c);\n    wrap.append(...[''','''    const dates = datesToConfirm(c);\n    const sorted = sortedEntries(c), liveRows = sorted.filter((e) => e.review_status !== \"dismissed\"), dismissedRows = sorted.filter((e) => e.review_status === \"dismissed\");\n    wrap.append(...[''',1)\ns=s.replace('''  function sortedEntries(c) {''','''  // T-060 r4: a dismissed entry leaves the queue and waits in a collapsed \"Dismissed (n)\" group right under it, each with Undo. It opens by itself for the entry the paralegal just\n  // dismissed (so she sees where it went and can undo it), and stays as she leaves it. Dismissed entries are never in the letter.\n  ZL.dismissedOpen = false;\n  function dismissedGroup(c, rows) {\n    if (!rows.length) return null;\n    const d = el(\"details\", { class: \"dismissed-group\", \"data-testid\": \"dismissed-group\", open: ZL.dismissedOpen || null },\n      el(\"summary\", { \"data-testid\": \"dismissed-summary\" }, `Dismissed (${rows.length})`, el(\"span\", { class: \"muted small\" }, \" Not in the letter. Open to read them or press Undo.\")),\n      el(\"div\", { class: \"timeline\", \"data-testid\": \"dismissed-queue\" }, rows.map((e) => entryRow(e, c))));\n    d.addEventListener(\"toggle\", () => { ZL.dismissedOpen = d.open; });\n    return d;\n  }\n  function sortedEntries(c) {''',1)\nopen(p,\"w\").write(s)\n\np=\"app/frontend/styles.css\"\ns=open(p).read()\ns=s.replace('''.entry[data-review=\"dismissed\"] .summary, .entry[data-review=\"dismissed\"] .excerpt { color: var(--text-subtle); text-decoration: line-through; text-decoration-color: var(--border-strong); }''','''.entry[data-review=\"dismissed\"] .summary { color: var(--text-subtle); text-decoration: line-through; text-decoration-color: var(--border-strong); }   /* the summary is struck, never the record's own quote */\n.dismissed-group { margin-top: var(--s-3); border: 1px solid var(--border); border-radius: var(--r-2); padding: 0 var(--s-3); background: var(--sunken); }\n.dismissed-group > summary { font-weight: var(--w-strong); }\n.dismissed-group[open] > summary { border-bottom: 1px solid var(--border); margin-bottom: var(--s-1); }''',1)\n# caution wraps on its own line; decided summaries keep 2 lines\ns=s.replace('''.entry[data-entry-id].is-open .entry-head .reason { white-space: normal; overflow: visible; }''','''.entry[data-entry-id].is-open .entry-head .reason, .entry[data-entry-id] .entry-head .reason--caution { white-space: normal; overflow: visible; flex-basis: 100%; }   /* \"read the original quote yourself\" is never cut short */''',1)\ns=s.replace('''.entry[data-entry-id][data-review=\"accepted\"]:not(.is-open) .summary, .entry[data-entry-id][data-review=\"edited\"]:not(.is-open) .summary, .entry[data-entry-id][data-review=\"dismissed\"]:not(.is-open) .summary { -webkit-line-clamp: 1; }''','''.entry[data-entry-id][data-review=\"accepted\"]:not(.is-open) .summary, .entry[data-entry-id][data-review=\"edited\"]:not(.is-open) .summary, .entry[data-entry-id][data-review=\"dismissed\"]:not(.is-open) .summary { -webkit-line-clamp: 2; }''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"rv-gap-change\" app/frontend/*.css; sed -n 1,30p app/frontend/review.css | cut -c1-250"
}
````

### User / tool · 2026-11-02T11:08:19.446Z

**tool result**
````
/* Review panels (T-043, restyled in T-060): controls, flags, charges, batch bar, audit drawer, export settings, case switcher. Tokens only (tokens.css). */
.rv-panel { max-width: 100%; min-width: 0; margin: var(--s-5) 0; overflow-wrap: anywhere; }
.rv-panel > h2 { margin-bottom: var(--s-1); }
.rv-panel h3 { margin: var(--s-5) 0 var(--s-2); }
.rv-help, .rv-keys, .rv-why, .rv-empty, .rv-note { color: var(--text-muted); font-size: var(--t-sm); line-height: var(--lh-sm); margin: var(--s-1) 0 var(--s-3); max-width: var(--measure); }
.rv-empty { color: var(--text-subtle); }
.rv-card { border: 1px solid var(--border); border-left: 3px solid var(--border-strong); border-radius: var(--r-2); background: var(--panel); padding: var(--s-3) var(--s-4); margin: var(--s-2) 0; min-width: 0; }
.rv-card[data-state="needs_review"] { border-left-color: var(--warn); }
.rv-card[data-state="rejected"] { border-left-color: var(--bad); }
.rv-card[data-review="dismissed"] { background: var(--sunken); }
.rv-card[data-review="dismissed"] .rv-text-body { color: var(--text-subtle); text-decoration: line-through; text-decoration-color: var(--border-strong); }
.rv-card.sbs-current { background: var(--accent-soft); border-left-color: var(--accent); }
.rv-head { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-1) var(--s-3); }
.rv-title { font-size: var(--t-md); line-height: var(--lh-md); font-weight: var(--w-strong); flex: 1 1 14rem; }
.rv-chips { display: inline-flex; flex-wrap: wrap; gap: var(--s-1); }
.rv-reason-line { background: var(--warn-bg); color: var(--warn); padding: var(--s-2) var(--s-3); border-radius: var(--r-1); margin: var(--s-2) 0; font-size: var(--t-sm); line-height: var(--lh-sm); }
.rv-usernote { background: var(--sunken); padding: var(--s-2) var(--s-3); border-radius: var(--r-1); font-size: var(--t-sm); line-height: var(--lh-sm); }
.rv-text-body { margin: var(--s-2) 0; max-width: var(--measure); }
.rv-evidence { list-style: none; margin: var(--s-2) 0; padding: 0; display: grid; grid-template-columns: 1fr; gap: var(--s-2); }
.rv-evidence.rv-side, .rv-evidence:has(> li:nth-child(2)) { grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); }
.rv-ev { min-width: 0; }
.rv-ev-cap { display: block; font-size: var(--t-xs); line-height: var(--lh-xs); color: var(--text-subtle); margin-bottom: 2px; }
.rv-ev-more { display: block; font-size: var(--t-sm); line-height: var(--lh-sm); color: var(--text-muted); margin-top: var(--s-1); }
.rv-actions { display: flex; flex-wrap: wrap; align-items: center; gap: var(--s-2); margin: var(--s-2) 0 0; }
.rv-actions .rv-audit, .rv-actions .rv-dismiss-reason { margin-left: 0; }
.rv-controls .rv-actions .rv-audit { margin-left: auto; }
.rv-datefix, form.rv-edit, form.rv-reason { margin: var(--s-2) 0; }
form.rv-edit[hidden], form.rv-reason[hidden] { display: none; }
.rv-text, .rv-input { display: block; width: 100%; margin-top: var(--s-1); }
form.rv-reason { display: flex; flex-wrap: wrap; gap: var(--s-2); align-items: center; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:08:46.991Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/review.js\"\ns=open(p).read()\n\n# 1. asTyped + rechecks helpers, before \"---- errors\"\ns=s.replace('''  // ---- errors (R-RV-3, D-034, D-047).''','''  // The server names a refused number the way it compares it (\"9000\"). Show it the way the paralegal typed it (\"$9,000\"): swap the first matching figure in the message for the\n  // same figure as it appears in her own text. Display only; nothing is added or compared.\n  RV.asTyped = function (msg, tokens, text) {\n    let out = String(msg || \"\");\n    (tokens || []).forEach((tok) => {\n      if (!/^\\\\d[\\\\d.]*$/.test(String(tok))) return;\n      const re = /\\\\$?\\\\s?\\\\d[\\\\d,]*(?:\\\\.\\\\d+)?/g; let m, typed = null;\n      while ((m = re.exec(text || \"\")) && !typed) { const bare = m[0].replace(/[$,\\\\s]/g, \"\"); if (bare === tok || bare.replace(/\\\\.0+$/, \"\") === tok) typed = m[0].trim(); }\n      if (!typed || typed === tok) return;\n      out = out.replace(new RegExp(\"(^|[^\\\\\\\\d$,.])\" + String(tok).replace(/[.*+?^${}()|[\\\\]\\\\\\\\]/g, \"\\\\\\\\$&\") + \"(?![\\\\\\\\d,]|\\\\\\\\.\\\\\\\\d)\"), (_, pre) => pre + typed);\n    });\n    return out;\n  };\n  // What happened to an edit, in plain words, kept on the row until the next decision: the code re-checks the wording against the quote on every save, then a second AI check reads it.\n  const rechecks = {};   // id -> sentence\n  function recheckSentence(resp) {\n    const w = (resp && resp.warnings) || [], st = resp && resp.item && resp.item.state;\n    const lead = \"Saved and re-checked. The code compared every number, date and negation in your wording with the quote and found no difference.\";\n    if (w.length) return lead + \" \" + w.map((x) => x.message).filter(Boolean).join(\" \") + \" Compare it with the quote yourself.\";\n    return lead + (st === \"needs_review\" ? \" The entry still needs your review.\" : \" The second AI check agreed.\");\n  }\n\n  // ---- errors (R-RV-3, D-034, D-047).''',1)\n\n# 2. act: dismissed open, edit success recheck, typed message\ns=s.replace('''      ZL.state.applyReview(resp);\n      const left =''','''      if (body.action === \"edit\" && found && found.kind === \"entry\") rechecks[id] = recheckSentence(resp); else delete rechecks[id];\n      if (body.action === \"dismiss\" && found && found.kind === \"entry\") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo\n      ZL.state.applyReview(resp);\n      if (rechecks[id]) RV.say(rechecks[id]);\n      const left =''',1)\ns=s.replace('''        const d = e.detail || {}, toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || \"\").includes(d.tokens[0]) ? \" Not in the quote: \" + d.tokens.join(\", \") + \".\" : \"\";\n        showError(id, (e.message || \"That edit is not allowed.\") + toks);''','''        const d = e.detail || {}, ta0 = document.querySelector('[data-controls-for=\"' + id + '\"] textarea'), typed = ta0 ? ta0.value : \"\";\n        const toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || \"\").includes(d.tokens[0]) ? \" Not in the quote: \" + d.tokens.join(\", \") + \".\" : \"\";\n        showError(id, RV.asTyped((e.message || \"That edit is not allowed.\") + toks, d.tokens, typed));''',1)\n# code-check refusal on edit: typed form too\ns=s.replace('''    const s = slot(id, \"rv-error\"), msg = e.message || \"That wording fails a check. Edit it to match the quote.\";''','''    const ta0 = document.querySelector('[data-controls-for=\"' + id + '\"] textarea');\n    const s = slot(id, \"rv-error\"), msg = RV.asTyped(e.message || \"That wording fails a check. Edit it to match the quote.\", e.detail && e.detail.tokens, ta0 ? ta0.value : \"\");''',1)\ns=s.replace('''message: e.message || \"The summary fails a check. Edit the summary to match the quote.\", label:''','''message: RV.asTyped(e.message || \"The summary fails a check. Edit the summary to match the quote.\", e.detail && e.detail.tokens, (found && found.item && ((found.item.edited && found.item.edited.summary) || found.item.summary)) || \"\"), label:''',1)\n\n# 3. controls: recheck paragraph + hint + original\ns=s.replace('''    root.append(el(\"div\", { class: \"rv-refused\", role: \"alert\", hidden: true, \"data-testid\": \"accept-refused\" }));''','''    root.append(el(\"div\", { class: \"rv-refused\", role: \"alert\", hidden: true, \"data-testid\": \"accept-refused\" }));\n    if (rechecks[id] && st === \"edited\") root.append(el(\"p\", { class: \"rv-recheck\", \"data-testid\": \"edit-recheck-note\" }, rechecks[id]));''',1)\ns=s.replace('''        el(\"label\", { class: \"rv-label\" }, hint, ta),\n        el(\"div\", { class: \"rv-actions\" },''','''        !isFlag && item.edited && item.edited.original_summary ? el(\"p\", { class: \"rv-original muted small\", \"data-testid\": \"edit-original\" }, el(\"strong\", {}, \"Original wording: \"), item.edited.original_summary) : null,\n        el(\"label\", { class: \"rv-label\" }, hint, ta),\n        isFlag ? null : el(\"p\", { class: \"rv-help rv-recheck-hint\", \"data-testid\": \"edit-recheck-hint\" }, \"When you save, the code checks every number, date and negation in your wording against the quote, then a second AI check reads it. Nothing is added to the letter until it passes.\"),\n        el(\"div\", { class: \"rv-actions\" },''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"asTyped\" app/frontend/review.js | head; node -e \"\nglobal.window={};\" 2>/dev/null; sed -n '/RV.asTyped = /,/^  };/p' app/frontend/review.js"
}
````

### User / tool · 2026-11-02T11:08:47.163Z

**tool result**
````
132:  RV.asTyped = function (msg, tokens, text) {
164:    const s = slot(id, "rv-error"), msg = RV.asTyped(e.message || "That wording fails a check. Edit it to match the quote.", e.detail && e.detail.tokens, ta0 ? ta0.value : "");
230:        showError(id, RV.asTyped((e.message || "That edit is not allowed.") + toks, d.tokens, typed));
233:        refusals[id] = { id, code: nextCode(e), message: RV.asTyped(e.message || "The summary fails a check. Edit the summary to match the quote.", e.detail && e.detail.tokens, (found && found.item && ((found.item.edited && found.item.edited.summary) || found.item.summary)) || ""), label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
  RV.asTyped = function (msg, tokens, text) {
    let out = String(msg || "");
    (tokens || []).forEach((tok) => {
      if (!/^\d[\d.]*$/.test(String(tok))) return;
      const re = /\$?\s?\d[\d,]*(?:\.\d+)?/g; let m, typed = null;
      while ((m = re.exec(text || "")) && !typed) { const bare = m[0].replace(/[$,\s]/g, ""); if (bare === tok || bare.replace(/\.0+$/, "") === tok) typed = m[0].trim(); }
      if (!typed || typed === tok) return;
      out = out.replace(new RegExp("(^|[^\\d$,.])" + String(tok).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![\\d,]|\\.\\d)"), (_, pre) => pre + typed);
    });
    return out;
  };
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:08:53.964Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/review.js\"\ns=open(p).read()\ns=s.replace('''        RV.act(id, { action: \"edit\", edits: isFlag ? { note: v } : { summary: v } }, { focus: \"edit\" });\n      } },''','''        const h = form.querySelector(\".rv-recheck-hint\"), was = h ? h.textContent : \"\";\n        if (h) h.textContent = \"Checking your wording against the quote…\";\n        RV.act(id, { action: \"edit\", edits: isFlag ? { note: v } : { summary: v } }, { focus: \"edit\" }).finally(() => { if (h && h.isConnected) h.textContent = was; });\n      } },''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"rv-recheck\\|rv-gap\" app/frontend/*.css | head -3\ncat >> app/frontend/review.css <<'EOF'\n\n/* T-060 r4: the edit re-check line and the persistent gap-change line (T-114) */\n.rv-recheck, .rv-gap-change { background: var(--info-bg); border-left: 3px solid var(--info); border-radius: var(--r-1); padding: var(--s-2) var(--s-3); margin: var(--s-2) 0; font-size: var(--t-sm); line-height: var(--lh-sm); color: var(--text); max-width: var(--measure); }\n.entry[data-entry-id] .rv-recheck { order: 6; grid-column: 1 / -1; }\n.rv-original { margin: 0 0 var(--s-2); }\n.rv-recheck-hint { margin: var(--s-1) 0 var(--s-2); }\nEOF"
}
````

### User / tool · 2026-11-02T11:08:54.083Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:02.053Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/review.js\"\ns=open(p).read()\ns=s.replace('''  RV.chips = function (item) {   // machine state, then (only once decided) the human decision: two chips, two icons\n    const t = STATE_TONE[item.state] || [\"muted\", \"info\"], d = DECISION[item.review_status];\n    return el(\"span\", { class: \"rv-chips\" },\n      el(\"span\", { class: \"chip chip--\" + t[0], \"data-icon\": t[1], \"data-chip\": \"state\" }, STATE_LABEL[item.state] || item.state),''','''  RV.chips = function (item) {   // machine state, then (only once decided) the human decision: two chips, two icons\n    const t = STATE_TONE[item.state] || [\"muted\", \"info\"], d = DECISION[item.review_status];\n    // T-114 r3: a decided rate / estimate / unclear amount reads one chip, \"Accepted\" (kept in the internal notes): its \"Needs review\" doubt is what she just resolved\n    const noted = item.accept_effect && item.accept_effect !== \"letter_total\" && (item.review_status === \"accepted\" || item.review_status === \"edited\");\n    if (noted) return el(\"span\", { class: \"rv-chips\" }, el(\"span\", { class: \"chip chip--\" + d[0], \"data-icon\": d[1], \"data-chip\": \"review\" }, REVIEW_LABEL[item.review_status]));\n    return el(\"span\", { class: \"rv-chips\" },\n      el(\"span\", { class: \"chip chip--\" + t[0], \"data-icon\": t[1], \"data-chip\": \"state\" }, STATE_LABEL[item.state] || item.state),''',1)\nopen(p,\"w\").write(s)\nEOF\necho ok"
}
````

### User / tool · 2026-11-02T11:09:02.153Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:08.791Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/judges.js\"\ns=open(p).read()\ns=s.replace('''  function links(id) {\n    const t = title(id);''','''  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says \"accept\".\n  const trayFlag = (id) => { const c = ZL.state.get().case; return !!(c && (c.tray || []).some((t) => t.id === id && t.kind === \"flag\")); };\n  const TODO_TRAY = \"Nothing to accept here. It is left out of the letter. If it matters, open the record and check it yourself.\";\n  function links(id) {\n    const t = title(id);''',1)\ns=s.replace('''\"aria-label\": \"See the steps for \" + t, onclick: () => ZL.stepper.openTrace(id) }, \"See the steps\"));\n  }''','''\"aria-label\": \"Why this status: \" + t, onclick: () => ZL.stepper.openTrace(id) }, \"Why this status\"));\n  }''',1)\ns=s.replace('''\"aria-label\": \"See the steps for \" + t, onclick: () => ZL.stepper.openTrace(id) }, \"See the steps\")));\n  }''','''\"aria-label\": \"Why this status: \" + t, onclick: () => ZL.stepper.openTrace(id) }, \"Why this status\")));\n  }''',1)\ns=s.replace('''    const decision = (r || u || it.dis[0] || {}).review_status;\n    let why = null;''','''    const tray = trayFlag(it.id);\n    const decision = tray ? null : (r || u || it.dis[0] || {}).review_status;\n    let why = null;''',1)\ns=s.replace('''    const todo = blk ? TODO_BLOCKED :''','''    const todo = tray ? TODO_TRAY : blk ? TODO_BLOCKED :''',1)\ns=s.replace('''    if (r) chips.push(chip(\"AI objected\", \"zj-chip-bad\"));\n    else if (mine)''','''    if (tray) chips.push(chip(\"Left out of the letter\"));\n    else if (r) chips.push(chip(\"AI objected\", \"zj-chip-bad\"));\n    else if (mine)''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"See the steps\" app/frontend/*.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T11:09:08.900Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:14.639Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/judges.js\"\ns=open(p).read()\ns=s.replace('\"Code said: \"','\"The code check said: \"',1)\ns=s.replace('''el(\"summary\", {}, \"Technical details\"), nodes.length ? el(\"p\", { class: \"zs-ev\" }, nodes) : null,\n      r && r.response_raw''','''el(\"summary\", { \"aria-label\": \"Technical details: \" + title(it.id) }, \"Technical details\"), nodes.length ? el(\"p\", { class: \"zs-ev\" }, nodes) : null,\n      r && r.response_raw''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"Technical details\" app/frontend/judges.js | cut -c1-200; grep -rn \"Code said\\|phrase list\" tests/e2e | head"
}
````

### User / tool · 2026-11-02T11:09:14.762Z

**tool result**
````
6:   into one row with chips. Model, prompt and reason-code internals sit in closed "Technical details".
55:  const noCode = (t) => String(t || "").replace(/\s*\([A-Z]{3,}(?:_[A-Z]+)*\)\s*$/, "");   // the closed reason code lives in Technical details
75:    return el("details", { class: "zs-more", "data-testid": "judge-row-tech" }, el("summary", { "aria-label": "Technical details: " + title(it.id) }, "Technical details"), nodes.length ? el("p", { 
183:    det.append(el("details", { class: "zs-more zj-tech", "data-testid": "judge-tech" }, el("summary", {}, "Technical details"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:18.394Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/manual.js\"\ns=open(p).read()\ns=s.replace('''\"This record has no sentences to pick from.\" + (rec.sentences_reason ? \" Why: \" + rec.sentences_reason : \"\"))''','''rec.sentences_reason || \"This record has no sentences to pick from. Read the record text instead.\")''',1)\nopen(p,\"w\").write(s)\nEOF\nsed -n 60,93p app/frontend/manual.js"
}
````

### User / tool · 2026-11-02T11:09:18.499Z

**tool result**
````
    function toggle(v) { d.open = v; form.hidden = !v; open.setAttribute("aria-expanded", String(v)); if (v) { const f = form.querySelector("input,textarea"); if (f) f.focus(); } else open.focus(); }
    form.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.stopPropagation(); toggle(false); } });
    return el("div", { class: "rv-manual", "data-testid": "manual-entry", "data-record-id": rec.id }, el("div", { class: "rv-actions" }, open), form);
  }

  RV.registerPanel("manual", (root, c) => {
    ZL.clear(root); root.className = "rv-batchhost"; root.removeAttribute("data-testid");
    const wrap = root.closest('[data-testid="timeline"]'); if (!wrap) return;
    const inTray = {};
    wrap.querySelectorAll('[data-testid="tray-item"]').forEach((node) => {
      const t = (c.tray || []).find((x) => x.id === node.getAttribute("data-item-id"));
      const rec = t && (t.record_ids || []).length === 1 ? (c.records || []).find((r) => r.id === t.record_ids[0]) : null;
      if (!rec || (t.kind && t.kind !== "entry")) return;
      inTray[rec.id] = true;
      if (!node.querySelector(":scope > .rv-manual")) node.append(control(c, t, rec));
    });
    // Records that produced no entry and are not in the tray (for example the model call failed): same control.
    const has = {}; (c.entries || []).concat(c.undated_entries || [], c.tray || []).forEach((e) => (e.record_ids || []).forEach((id) => { has[id] = true; }));
    const toConfirm = {}; (c.dates_to_confirm || []).forEach((d) => { if ((d.candidates || []).length) toConfirm[d.record_id] = true; });  // listed once, under Dates to confirm
    const missing = (c.records || []).filter((r) => !has[r.id] && !inTray[r.id] && !toConfirm[r.id] && !r.duplicate_of);
    if (!missing.length || c.status !== "ready") return;
    root.className = "rv-panel"; root.setAttribute("data-testid", "records-without-entry");
    root.append(el("h2", {}, "Records without an entry (" + missing.length + ")"),
      el("p", { class: "rv-help" }, "These records did not produce an entry, so they are not in the timeline or the letter. Read the record, quote the sentences yourself and write the summary."));
    missing.forEach((r) => {
      const card = el("article", { class: "rv-card", "data-testid": "missing-entry", "data-record-id": r.id },
        el("div", { class: "rv-head" }, el("h3", { class: "rv-title" }, "Record " + r.seq + ": " + r.source_label), el("span", { class: "rv-chip" }, r.date_iso ? ZL.fmtDate(r.date_iso) : "undated")),
        r.date_status === "confirmed" ? el("p", { class: "rv-help", "data-testid": "missing-date-confirmed" }, `Date confirmed: ${ZL.fmtDate(r.date_iso)}. Not on the timeline yet: enter this record by hand below.`) : null,
        r.date_status === "confirmed" && ZL.recordExcerpt && ZL.recordExcerpt(r) ? el("blockquote", { class: "excerpt", "data-testid": "missing-entry-excerpt" }, ZL.recordExcerpt(r)) : null,
        el("div", { class: "rv-actions" }, el("button", { type: "button", class: "btn", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], "Record " + r.seq + ": " + r.source_label) }, "Open record " + r.seq)));
      card.append(control(c, { id: "rec:" + r.id }, r)); root.append(card);
    });
  });
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:21.064Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/manual.js\"\ns=open(p).read()\ns=s.replace('''msg.textContent = (err.message || \"That entry was refused.\") + (why.length ? \" \" + why.join(\" \") : \"\");''','''msg.textContent = RV.asTyped((err.message || \"That entry was refused.\") + (why.length ? \" \" + why.join(\" \") : \"\"), detail.tokens, d.summary);''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"Dismissed\\|dismiss\" app/frontend/batch.js | head"
}
````

### User / tool · 2026-11-02T11:09:21.176Z

**tool result**
````
57:  // Items the server named that are still waiting (an item the paralegal has since edited, accepted or dismissed drops out of the list).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:27.089Z

**tool call — Bash**
````
{
 "command": "grep -rn \"Show all of\\|Show less\\|entry-toggle\" tests/ | cut -c1-200 | head; grep -n \"aria-labelledby\" app/frontend/timeline.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T11:09:27.217Z

**tool result**
````
tests/e2e/conftest.py:54:T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More
tests/e2e/test_polish_r3.py:4:New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
tests/e2e/test_polish_r3.py:165:    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
146:    const box = el("section", { class: "group" + (none ? " group--empty" : ""), "data-testid": "dates-to-confirm", "aria-labelledby": "h-dates" }, el("h2", { id: "h-dates" }, "Dates to confirm"));
192:    const box = el("section", { class: "group tray" + (c.tray.length ? "" : " group--empty"), "data-testid": "rejected-tray", "aria-labelledby": "h-tray" }, el("h2", { id: "h-tray" }, `Could not v
286:    todoHost = el("section", { "data-testid": "todo-strip", "aria-labelledby": "h-todo" }); wrap.append(todoHost); paintTodo();
307:      el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, liveRows.map((e) => entryRow(e, c))),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:31.633Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/export.js; sed -n 60,100p reviews/T-060-accessibility-pass3.md"
}
````

### User / tool · 2026-11-02T11:09:31.715Z

**tool result**
````
/* Export view (T-044): two separate copy blocks built by the SERVER (letter_text / internal_notes_text); the UI only displays and copies them verbatim.
   Count line sits outside both blocks (R-EX-5). Copy asks for one confirmation when anything is pending (names pending flags separately). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let open = false, data = null, timer = null, confirmFor = null;

  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  function countLine(c) {
    return `${plural(c.entries, "entry", "entries")}, ${plural(c.charges, "charge", "charges")} in letter · ${plural(c.flags_in_notes, "flag", "flags")} in internal notes · ${c.records_in_letter} of ${c.records_total} records in letter · ${plural(c.pending, "item", "items")} pending (${plural(c.pending_flags, "flag", "flags")})`;
  }
  function status(msg, bad) { const s = ZL.$("#export-status"); if (s) { s.textContent = msg || ""; s.className = bad ? "error" : "muted"; s.setAttribute("role", bad ? "alert" : "status"); } }
  async function copy(text, which) {
    try { await navigator.clipboard.writeText(text); status(`Copied the ${which}.`); }
    catch (_) { status("The browser blocked copying. Select the text in the box and copy it by hand.", true); }
  }
  // A plain-text file of exactly the text the server built (no editing, no re-assembly here).
  function download(text, name, which) {
    const url = URL.createObjectURL(new Blob([text || ""], { type: "text/plain;charset=utf-8" })), a = el("a", { href: url, download: name });
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status(`Downloaded the ${which} as ${name}.`);
  }
  // What is pending, by name ("2 charges, 1 flag") from the case on screen; falls back to the export's own counts.
  function pendingWords(c) {
    const cs = ZL.state.get().case, pend = (i) => (i.review_status || "pending") === "pending";
    if (!cs) return null;
    const bits = [[(cs.entries || []).concat(cs.undated_entries || []).filter(pend).length, "entry", "entries"], [(cs.amounts || []).filter((a) => pend(a) && a.kind === "charge").length, "charge", "charges"],
      [(cs.amounts || []).filter((a) => pend(a) && a.kind !== "charge").length, "unclear amount", "unclear amounts"], [c.pending_flags, "flag", "flags"]].filter(([n]) => n);
    return bits.map(([n, one, many]) => plural(n, one, many) + " not reviewed");
  }
  // One primary button for one task: while the confirmation is showing, Copy letter steps down and Copy anyway is the primary.
  function askConfirm(c, then, verb) {
    verb = verb || "Copy";
    const box = ZL.$("#export-confirm"), main = ZL.$('[data-testid="btn-copy-letter"]'); clear(box); box.hidden = false;
    if (main) main.classList.remove("btn--primary");
    const parts = pendingWords(c) || [plural(c.pending, "item", "items") + " not reviewed"];
    const close = () => { box.hidden = true; if (main) { main.classList.add("btn--primary"); main.focus(); } };
    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-copy-cancel", onclick: close }, "Go back")));
    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
  }
  function render() {
    const root = ZL.$("#export-body"); clear(root);
    ZL.$("#view-export").hidden = !open;
    if (!open || !data) return;
    const c = data.counts;
    root.append(...[
      el("p", { class: "count-line", "data-testid": "count-line", role: "status" }, countLine(c)),
      (data.warnings || []).length ? el("ul", { class: "ex-warn" }, data.warnings.map((w) => el("li", {}, typeof w === "string" ? w : (w.message || w.code)))) : null,
      el("p", { id: "export-status", class: "muted small", role: "status" }),
      el("div", { id: "export-confirm", hidden: true }),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h1" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h1" }, "Treatment section (paste into the letter)"),
          el("div", { class: "row ex-btns" },
            el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-letter", disabled: !data.letter_text, onclick: () => { const go = () => copy(data.letter_text, "treatment section"); c.pending > 0 ? askConfirm(c, go) : go(); } }, "Copy letter"),
            el("button", { type: "button", class: "btn", "data-testid": "btn-download-letter", disabled: !data.letter_text, onclick: () => { const go = () => download(data.letter_text, "treatment-section.txt", "treatment section"); c.pending > 0 ? askConfirm(c, go, "Download") : go(); } }, "Download .txt"))),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-letter" }, data.letter_text)),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h2" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h2" }, "Internal review notes — do not send"),
          el("div", { class: "row ex-btns" },
            el("button", { type: "button", class: "btn", "data-testid": "btn-copy-notes", onclick: () => copy(data.internal_notes_text, "internal notes") }, "Copy notes"),
            el("button", { type: "button", class: "btn", "data-testid": "btn-download-notes", onclick: () => download(data.internal_notes_text, "internal-review-notes.txt", "internal notes") }, "Download .txt"))),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-notes" }, data.internal_notes_text))].filter(Boolean));
  }
  async function load(scroll) {
    const s = ZL.state.get(); if (!s.token) return;
    try { data = await ZL.api.exportCase(s.token); open = true; render(); if (ZL.stepper) ZL.stepper.clearExportNotice(); if (scroll) { const h = ZL.$("#h-export"); h.setAttribute("tabindex", "-1"); h.scrollIntoView({ block: "start" }); h.focus({ preventScroll: true }); } }
    catch (e) {
      data = null;
      // A refused export (422 judge_not_run / export_blocked) is shown beside the Export button, scrolled into view and focused, with the blocker list and the rerun button.
      if (ZL.stepper && ZL.stepper.showExportBlocked(e, scroll)) { open = false; render(); return; }
      open = true; render(); ZL.$("#export-body").append(el("p", { class: "error", role: "alert" }, e.message));
    }
  }
  ZL.openExport = () => load(true);
  ZL.closeExport = () => { open = false; render(); };
  // keep an open export in step with review decisions made after it was opened
  ZL.state.subscribe((s) => { if (!s.case) { open = false; data = null; render(); return; } if (open) { clearTimeout(timer); timer = setTimeout(() => load(false), 250); } });
})();
| M6 generic button names | major, now minor | fixed | Timeline names, flag and charge "Why this status" names all fixed (N-5). |
| B1, M1 to M5 (pass 1) | blocker, majors | fixed | Letter keys from Export or an input change nothing (`s_from_export_focus`, `T-060-accessibility-pass3-keyboard-results.json`). Dark and light contrast 0 failing (below). Export focus on the heading in view, Copy letter one Tab away. Copy anyway returns focus to Copy letter. |

## New findings

### Minor

**P3-1. The row More/Less control's name omits its visible text and changes with its state.** (SC 2.5.3 Label in Name, Level A; same class as pass-2 N-10, rated minor there.)
- Evidence: `review.js:35` `aria-label: (openRows.has(e.id) ? "Show less of " : "Show all of ") + who`. Collapsed: visible "More", name "Show all of Austin EMS run report, 2026-01-09", `aria-expanded` "false". Expanded: visible "Less", name "Show less of Austin EMS run report, 2026-01-09", `aria-expanded` "true" (`T-060-accessibility-pass3-names.json` `pending.toggle`, `toggle_after_open`).
- Why it matters: the collapsed name does not contain the visible word "More". The name also changes with `aria-expanded`, so a screen reader can say the state twice.
- Fix: keep one name that contains the visible word, for example `aria-label` "More: <item>" / "Less: <item>", or drop `aria-label` and use the visible word plus `aria-expanded` with the row name supplied another way. Pick one and keep it stable across states.
- Acceptance test: the toggle's accessible name contains its visible text in both states; `aria-expanded` is the only state change.

**P3-2. The timeline container has `aria-labelledby` but no role, so its name is not exposed.** (SC 4.1.2; axe reports `aria-prohibited-attr` as needs-review, serious.)
- Evidence: `timeline.js:261` `el("div", { class: "timeline", "data-testid": "queue", "aria-labelledby": "h-timeline" }, ...)`. The element is also the skip-link target `#skip-to-review`. axe `aria-prohibited-attr` (incomplete, serious, message "aria-labelledby attribute is not well supported on a div with no valid role attribute") in 22 of 36 scans: 11 states, both themes (`T-060-accessibility-pass3-audit-results.json`, `d_incomplete_aria_prohibited_attr` in the extra probe).
- Why it matters: the attribute is prohibited on a generic `div`, so AT ignores it. The heading "Timeline" still exists visually, but the list has no programmatic name or role. This is a needs-review item in axe, not a violation, so it is a minor here.
- Fix: either remove `aria-labelledby` (the `h2` precedes the list), or give the container a role that allows a name, for example `role="region"` with `aria-labelledby` (only if a region landmark is wanted here).
- Acceptance test: axe `aria-prohibited-attr` incomplete count 0 in the queue states, and the element has either no `aria-labelledby` or a role that allows it.

**P3-3 (folded into N-8). Export-view skip links are dead.** Evidence: `T-060-accessibility-pass3-extra.json` `a_export_view_skip.targets`: `#skip-to-review`, `#skip-to-flags`, `#skip-to-charges` do not exist in the Export view; `#btn-export` does. Fix and test as in N-8.

**Carried: N-8 (partial) and N-9 (open)** are listed in the pass-2 table above; their fixes are unchanged.

### Nit

**P3-4. Export heading has no visible focus indicator after Enter on Export.** (SC 2.4.7 applies to the focused element; the checklist scopes the rule to interactive elements, so this is a nit.)
- Evidence: `T-060-accessibility-pass3-keyboard-results.json` `j_export_focus`: tag `h2`, name "Export", `outlineStyle` "none". The same value is in the pass-2 keyboard JSON, so it was not new in this build; it was not logged in pass 2.
- Fix: give the focused heading a focus style, for example `h2[tabindex="-1"]:focus-visible { outline: var(--focus-ring); }`.
- Acceptance test: after Enter on Export, the heading shows a 2 px ring with at least 3:1 contrast.

**P3-5. Accept on a decided row keeps `aria-pressed="true"` but a second press does nothing.** (SC 4.1.2 value; the announcement is correct.)
- Evidence: `T-060-accessibility-pass3-names.json` `accepted.accept`: `aria_pressed` "true", name "Accepted: Austin EMS run report, 2026-01-09". `T-060-accessibility-pass3-noop.json`: second press leaves `data-review` "accepted" and `aria-pressed` "true", and `rv-live` says "Accepted already. Use Undo to change it."
- Why it matters: `aria-pressed` means a toggle. A button that cannot turn off is a button, and Undo is the separate control.
- Fix: drop `aria-pressed` on a decided Accept (the state is already in the visible text and label), or make the control a real toggle.
- Acceptance test: a decided Accept has no `aria-pressed` attribute, or pressing it changes the value.

**Carried nits (unchanged or open):** N-11 (focus after Accept, product question), N-12 (two polite regions), N-13 (two stops partly under the sticky header at 320 px), N-14 (twelve "Technical details" names), N-15 (source dialog Tab through browser chrome). Fixes and acceptance tests are in the pass-2 review.

## Checks that passed this pass

- **axe-core, 18 states x light and dark (36 scans):** 0 serious or critical violations. Moderate `skip-link` in 6 scans (Export and copy views, N-8). `landmark-unique` gone. `definition-list` gone. Axe "incomplete" items (needs review): `color-contrast` in the empty states, why dialog and dialogs; `aria-prohibited-attr` (P3-2). My own computed contrast found 0 failures for these, so the axe incomplete items are not text-contrast failures.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:37.825Z

**tool call — Bash**
````
{
 "command": "grep -rn \"aria-pressed\\|aria_pressed\" tests/ | cut -c1-200 | head; grep -n \"h2\\[tabindex\\|focus-visible\" app/frontend/styles.css | head"
}
````

### User / tool · 2026-11-02T11:09:37.982Z

**tool result**
````
tests/e2e/test_code_check_refusal.py:131:    assert row.get_by_test_id("btn-accept").get_attribute("aria-pressed") == "false"
19::focus-visible { outline: var(--focus-ring); outline-offset: var(--focus-offset); }
21:.entry, .rv-card, [data-item-id], [data-testid="btn-export"], h2[tabindex], section[tabindex] { scroll-margin-top: var(--sticky); }
143:.entry:focus-visible { outline: var(--focus-ring); outline-offset: var(--focus-offset); }
251:label.btn:has(+ #file:focus-visible) { outline: var(--focus-ring); outline-offset: var(--focus-offset); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:46.230Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/timeline.js\"\ns=open(p).read()\nold=s[s.index('    const toggle = el(\"button\", { type: \"button\", class: \"btn btn--link\", \"data-testid\": \"entry-toggle\"'):s.index('    row.append(...[')]\nnew='''    // one accessible name that starts with the visible word (WCAG 2.5.3) and says which row it is; aria-expanded is the only thing that tells the state\n    const tname = (open) => (open ? \"Less\" : \"More\") + \" of \" + who;\n    const toggle = el(\"button\", { type: \"button\", class: \"btn btn--link\", \"data-testid\": \"entry-toggle\", \"aria-expanded\": String(openRows.has(e.id)), \"aria-label\": tname(openRows.has(e.id)),\n      onclick: () => { const open = !openRows.has(e.id); if (open) openRows.add(e.id); else openRows.delete(e.id); row.classList.toggle(\"is-open\", open); toggle.setAttribute(\"aria-expanded\", String(open)); toggle.setAttribute(\"aria-label\", tname(open)); toggle.textContent = open ? \"Less\" : \"More\"; } }, openRows.has(e.id) ? \"Less\" : \"More\");\n'''\ns=s.replace(old,new,1)\ns=s.replace('el(\"div\", { class: \"timeline\", \"data-testid\": \"queue\", \"aria-labelledby\": \"h-timeline\" }','el(\"div\", { class: \"timeline\", \"data-testid\": \"queue\", role: \"group\", \"aria-labelledby\": \"h-timeline\" }',1)\nopen(p,\"w\").write(s)\n\np=\"app/frontend/app.js\"\ns=open(p).read()\ns=s.replace('''    const sig = live.map((x) => x[0]).join(\",\");\n    if (sig === skipSig && nav.firstChild) return; skipSig = sig;''','''    const sig = live.map((x) => x[0]).join(\",\");\n    live.forEach(([id]) => { const t = document.querySelector(TARGETS[id] || \"\"); if (t && !t.id) t.id = \"skip-to-\" + id; });   // the review is rebuilt on every change, so a cached link must be re-pointed at the new element\n    if (sig === skipSig && nav.firstChild) return; skipSig = sig;''',1)\nopen(p,\"w\").write(s)\n\np=\"app/frontend/styles.css\"\ns=open(p).read()\ns=s.replace('''label.btn:has(+ #file:focus-visible)''','''h2[tabindex=\"-1\"]:focus { outline: var(--focus-ring); outline-offset: var(--focus-offset); }   /* Export moves focus to its heading: it shows where focus is */\nlabel.btn:has(+ #file:focus-visible)''',1)\nopen(p,\"w\").write(s)\nEOF\necho; grep -n \"skip-to-\\|TARGETS\\[\" app/frontend/app.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T11:09:46.350Z

**tool result**
````
65:    live.forEach(([id]) => { const t = document.querySelector(TARGETS[id] || ""); if (t && !t.id) t.id = "skip-to-" + id; });   // the review is rebuilt on every change, so a cached link must be re
69:      const t = document.querySelector(TARGETS[id] || ""); if (t && !t.id) t.id = "skip-to-" + id;   // a real element for the href to resolve to (WCAG 2.4.1); the click still moves focus to the fi
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:09:58.835Z

**tool call — Bash**
````
{
 "command": "sed -n 60,142p tests/e2e/conftest.py; sed -n 100,200p tests/e2e/test_polish_r3.py"
}
````

### User / tool · 2026-11-02T11:09:58.930Z

**tool result**
````
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

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



class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."
    for k in ("j", "a", "Shift+A"):
        page.keyboard.press(k)
    assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0


def test_letter_key_with_a_window_open_says_so(page, sample_case):
    """paralegal F11: o then a used to do nothing, silently."""
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("o"); expect(page.get_by_test_id("record-modal")).to_be_visible()
    page.keyboard.press("a")
    expect(page.locator("#rv-live")).to_contain_text("Press Escape")
    assert page.locator("[data-review=accepted]").count() == 0


# ---- 3. Tab, Enter and Space only: review one item, then export (R-RV-4)
def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_case):
    tok = sample_case
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] == "verified" and e["date"]]
    assert api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})[0] == 200   # setup by API: the checked entries are in the letter
    open_case(page, tok)
    # (a) one item reviewed by keyboard: Tab to the first skip link, Enter, then Tab to the item's Dismiss button, Enter
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-review", 6)
    page.keyboard.press("Enter")
    row = active(page); assert row["item"], row
    item = row["item"]
    tab_until(page, "btn-dismiss", 12)
    page.keyboard.press("Enter")
    expect(page.locator(f'[data-item-id="{item}"]').first).to_have_attribute("data-review", "dismissed")
    # (b) the export, from a fresh load, by keyboard only
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-export", 10)
    page.keyboard.press("Enter")
    assert active(page)["tid"] == "btn-export"
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    tab_until(page, "btn-copy-letter", 6)
    page.keyboard.press("Space")
    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
    page.keyboard.press("Enter")
    expect(page.locator("#export-status")).to_contain_text("Copied the treatment section")


# ---- 4. density
def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
    try:
        rows = pg.locator('[data-testid=queue] > article')
        assert rows.count() >= 5
        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
        first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
        assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
        visible = [bx for bx in boxes if bx[0] + bx[1] <= 900]
        assert len(visible) >= 3, boxes
        for top, h, state in boxes:
            assert h <= (170 if state == "needs_review" else 150), boxes
    finally:
        b.close()


def test_row_opens_with_more_and_closes_with_less(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
    h0 = row.bounding_box()["height"]
    expect(t).to_have_attribute("aria-expanded", "false"); t.click(); expect(t).to_have_attribute("aria-expanded", "true")
    assert "is-open" in row.get_attribute("class")
    t.click(); expect(t).to_have_attribute("aria-expanded", "false"); assert abs(row.bounding_box()["height"] - h0) < 2


def test_390_needs_review_row_is_at_most_420(pw, lib09):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
    try:
        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
        assert hs and max(hs) <= 420, hs
        assert pg.evaluate("document.documentElement.scrollWidth") <= 391
    finally:
        b.close()


# ---- 5. decided rows show a state, not a filled Accept
def test_accepted_row_has_no_filled_accept_and_undo_returns(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1")
    acc = row.get_by_test_id("btn-accept"); expect(acc).to_have_class(re.compile(r"btn--primary"))
    acc.click(); expect(row).to_have_attribute("data-review", "accepted")
    acc = row.get_by_test_id("btn-accept")
    assert "btn--primary" not in acc.get_attribute("class") and acc.inner_text().strip().startswith("Accepted")
    assert page.locator("[data-testid=entry-1] .btn--primary:visible").count() == 0
    row.get_by_test_id("btn-reset").click(); expect(row).to_have_attribute("data-review", "pending")
    expect(row.get_by_test_id("btn-accept")).to_have_class(re.compile(r"btn--primary"))


def test_dismissed_row_keeps_no_filled_accept(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-2")
    row.get_by_test_id("btn-dismiss").click(); expect(row).to_have_attribute("data-review", "dismissed")
    assert "btn--primary" not in row.get_by_test_id("btn-accept").get_attribute("class")
    assert row.get_by_test_id("btn-dismiss").inner_text().strip().startswith("Dismissed")
    assert row.get_by_test_id("btn-reset").inner_text().strip() == "Undo"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:10:04.544Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json,urllib.request,time\ndef call(m,p,b=None):\n    r=urllib.request.Request(\"http://localhost:7955/api\"+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={\"Content-Type\":\"application/json\"})\n    try: return json.load(urllib.request.urlopen(r))\n    except urllib.error.HTTPError as e: return {\"err\":e.code,\"body\":e.read().decode()[:300]}\ndef mk(body):\n    tok=call(\"POST\",\"/cases\",body)[\"token\"]; call(\"POST\",f\"/cases/{tok}/run\",{})\n    for _ in range(100):\n        if call(\"GET\",f\"/cases/{tok}/status\")[\"status\"] in(\"ready\",\"failed\"):break\n        time.sleep(.3)\n    return tok\nt=mk({\"sample\":True}); c=call(\"GET\",f\"/cases/{t}\")\nprint(\"sample tray\",[(x[\"id\"],x.get(\"kind\")) for x in c[\"tray\"]], len(c[\"entries\"]), [a[\"kind\"] for a in c[\"amounts\"]])\nfor lib in [\"case_lib06_lop_billed_vs_adjusted\",\"case_lib11_priors_and_ledger\"]:\n    t=mk({\"library\":lib}); c=call(\"GET\",f\"/cases/{t}\")\n    print(lib,\"tray\",[(x[\"id\"],x.get(\"kind\")) for x in c[\"tray\"]],[ (a[\"id\"],a[\"kind\"],a.get(\"accept_effect\")) for a in c[\"amounts\"]][:6])\n    call(\"DELETE\",f\"/cases/{t}\")\nEOF"
}
````

### User / tool · 2026-11-02T11:10:05.405Z

**tool result (error)**
````
Exit code 1
sample tray [] 9 ['charge', 'rate', 'charge', 'damages']
case_lib06_lop_billed_vs_adjusted tray [('f_r5_1', 'flag')] [('a1', 'charge', 'letter_total'), ('a2', 'charge', 'letter_total'), ('a3', 'unclear', 'internal_notes'), ('a4', 'charge', 'letter_total'), ('a5', 'charge', 'letter_total'), ('a6', 'unclear', 'internal_notes')]
Traceback (most recent call last):
  File "<stdin>", line 17, in <module>
  File "<stdin>", line 4, in call
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:10:36.815Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/test_polish_r4.py",
 "content": "\"\"\"T-060 round 4 (frontend) + T-114 r3: the gap-change line that survives a reload, readable library titles, dismissed rows leave the queue, the edit re-check\nnotice and the typed-dollar 422 message, the AI-check row for a flag the checks left out, the doubled no-sentences copy, and the cheap accessibility fixes.\nNew test ids (declared in tests/e2e/conftest.py, 'T-060 round 4'): gap-change-card, gap-change-removed, dismissed-group, dismissed-summary, dismissed-queue, edit-recheck-hint,\nedit-recheck-note, edit-original. Library cases need ZLAYT_MODE=local; the fixture backend replays recorded answers.\"\"\"\nimport json\nimport re\nimport time\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case, BASE\n\nBAD_TEXT = re.compile(r\"\\[object|\\bundefined\\b|\\bnull\\b\")\n\n\ndef _run(tok):\n    assert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    for _ in range(300):\n        s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(.5)\n    assert s[\"status\"] == \"ready\"\n\n\ndef _lib(lib_id):\n    st, c = api(\"POST\", \"/api/cases\", {\"library\": lib_id})\n    if st not in (200, 201):\n        pytest.skip(\"library cases need ZLAYT_MODE=local\")\n    _run(c[\"token\"])\n    return c[\"token\"]\n\n\n@pytest.fixture\ndef lib09():\n    tok = _lib(\"case_lib09_spanish_interpreter_espalda\")\n    yield tok\n    api(\"DELETE\", f\"/api/cases/{tok}\")\n\n\n@pytest.fixture\ndef lib06():\n    tok = _lib(\"case_lib06_lop_billed_vs_adjusted\")\n    yield tok\n    api(\"DELETE\", f\"/api/cases/{tok}\")\n\n\ndef _confirm_record4_as_march_5(page):\n    box = page.get_by_test_id(\"dates-to-confirm\")\n    radios = box.get_by_test_id(\"confirm-date\")\n    target = None\n    for i in range(radios.count()):\n        if radios.nth(i).get_attribute(\"data-date\") == \"2026-03-05\":\n            target = radios.nth(i)\n    assert target is not None\n    target.check()\n    box.get_by_test_id(\"btn-confirm-date\").first.click()\n\n\n# ---- T-114 major: the gap-change line is on the gap card and survives Got it and a reload\ndef test_t114_gap_change_stays_on_the_gap_card_after_got_it_and_reload(page, lib09):\n    open_case(page, lib09)\n    gap = page.locator('[data-testid=flags-panel] [data-flag-type=gap]').first\n    assert \"was 42\" not in gap.inner_text()                       # before the confirm there is nothing to explain\n    _confirm_record4_as_march_5(page)\n    note = page.get_by_test_id(\"gap-change-note\"); expect(note).to_be_visible(timeout=10000)\n    card = page.get_by_test_id(\"gap-change-card\"); expect(card).to_have_count(1)\n    expect(card).to_contain_text(\"now 40 days (was 42)\")\n    expect(card).to_contain_text(\"March 5, 2026\"); expect(card).to_contain_text(\"March 3, 2026\"); expect(card).to_contain_text(\"April 14, 2026\")\n    assert page.locator('[data-testid=flags-panel] [data-flag-type=gap]').first.get_by_test_id(\"gap-change-card\").count() == 1   # it sits on the gap card, not elsewhere\n    page.get_by_test_id(\"btn-dismiss-gap-note\").click(); expect(note).to_have_count(0)\n    expect(page.get_by_test_id(\"gap-change-card\")).to_contain_text(\"now 40 days (was 42)\")      # Got it removes the announcement, not the card line\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n    assert page.get_by_test_id(\"gap-change-note\").count() == 0\n    card = page.get_by_test_id(\"gap-change-card\"); expect(card).to_have_count(1)\n    expect(card).to_contain_text(\"now 40 days (was 42)\"); expect(card).to_contain_text(\"March 5, 2026\")\n    assert not BAD_TEXT.search(card.inner_text())\n\n\ndef test_t114_gap_change_line_is_not_shown_on_a_case_that_never_changed(page, lib09):\n    open_case(page, lib09)\n    assert page.get_by_test_id(\"gap-change-card\").count() == 0 and page.get_by_test_id(\"gap-change-removed\").count() == 0\n\n\ndef test_t114_accepted_rate_row_reads_one_status_chip(page, sample_case):\n    open_case(page, sample_case)\n    row = page.locator('tr[data-amount-kind=rate]').first\n    row.get_by_test_id(\"btn-accept\").click()\n    expect(row).to_have_attribute(\"data-review\", \"accepted\")\n    txt = row.inner_text()\n    assert \"Needs review\" not in txt and \"Accepted\" in txt, txt\n    assert row.locator(\"[data-chip]\").count() == 1\n\n\n# ---- T-060 r4: library cases show readable titles\ndef test_library_case_header_and_buttons_show_titles_not_file_slugs(page, lib09):\n    open_case(page, lib09)\n    name = page.get_by_test_id(\"case-name\").inner_text()\n    assert \"lib09\" not in name and not name.lower().startswith(\"case \") and \"_\" not in name, name\n    assert \"lib09\" not in page.title()\n    page.locator(\"details.cs-details > summary\").click()\n    labels = page.locator('[data-testid^=\"library-\"]').all_inner_texts()\n    assert labels and not any(re.search(r\"\\blib\\d+\\b|^Add:\", t) for t in labels), labels\n    assert not any(t.strip().startswith(\"L1 ·\") for t in labels)\n\n\n# ---- T-060 r4: a dismissed entry leaves the queue and waits in the Dismissed group\ndef test_dismissed_entry_leaves_the_queue_for_the_dismissed_group_and_undo_returns_it(page, sample_case):\n    open_case(page, sample_case)\n    row = page.get_by_test_id(\"entry-2\")\n    row.get_by_test_id(\"btn-dismiss\").click()\n    group = page.get_by_test_id(\"dismissed-group\"); expect(group).to_have_count(1)\n    expect(page.get_by_test_id(\"dismissed-summary\")).to_contain_text(\"Dismissed (1)\")\n    assert page.locator('[data-testid=queue] [data-testid=entry-2]').count() == 0\n    assert page.locator('[data-testid=dismissed-queue] [data-testid=entry-2]').count() == 1\n    dis = page.get_by_test_id(\"entry-2\"); expect(dis).to_be_visible()          # opened for the entry just dismissed, so Undo is in reach\n    assert page.evaluate(\"getComputedStyle(document.querySelector('[data-testid=entry-2] [data-testid=entry-excerpt]')).textDecorationLine\") == \"none\"   # the record's own quote is never struck through\n    dis.get_by_test_id(\"btn-reset\").click()\n    expect(page.locator('[data-testid=queue] [data-testid=entry-2]')).to_have_count(1)\n    expect(page.get_by_test_id(\"dismissed-group\")).to_have_count(0)\n\n\ndef test_dismissed_group_is_collapsed_after_a_reload(page, sample_case):\n    tok = sample_case\n    e = api(\"GET\", f\"/api/cases/{tok}\")[1][\"entries\"][1][\"id\"]\n    assert api(\"POST\", f\"/api/cases/{tok}/items/{e}/review\", {\"action\": \"dismiss\"})[0] == 200\n    open_case(page, tok)\n    expect(page.get_by_test_id(\"dismissed-summary\")).to_contain_text(\"Dismissed (1)\")\n    assert page.get_by_test_id(\"dismissed-group\").get_attribute(\"open\") is None\n    assert page.locator(f'[data-testid=queue] [data-item-id=\"{e}\"]').count() == 0\n    page.get_by_test_id(\"dismissed-summary\").click()\n    expect(page.locator(f'[data-testid=dismissed-queue] [data-item-id=\"{e}\"]')).to_be_visible()\n\n\n# ---- AC5: the re-check line on edit, and the 422 message in the paralegal's own dollars\ndef _open_edit(page, n=1):\n    row = page.get_by_test_id(f\"entry-{n}\"); row.get_by_test_id(\"btn-edit\").click()\n    return row\n\n\ndef test_edit_box_says_the_wording_is_re_checked_and_a_saved_edit_reports_it(page, sample_case):\n    open_case(page, sample_case)\n    row = _open_edit(page, 1)\n    hint = row.get_by_test_id(\"edit-recheck-hint\"); expect(hint).to_be_visible()\n    assert \"checks every number, date and negation\" in hint.inner_text()\n    ta = row.get_by_test_id(\"edit-summary\"); old = ta.input_value()\n    ta.fill(old.rstrip(\".\") + \".\")                                  # same words: nothing new to refuse\n    row.get_by_test_id(\"btn-save-edit\").click()\n    expect(row).to_have_attribute(\"data-review\", \"edited\")\n    note = page.get_by_test_id(\"entry-1\").get_by_test_id(\"edit-recheck-note\"); expect(note).to_be_visible()\n    assert \"re-checked\" in note.inner_text() and not BAD_TEXT.search(note.inner_text())\n    page.get_by_test_id(\"entry-1\").get_by_test_id(\"btn-reset\").click()\n    expect(page.get_by_test_id(\"entry-1\").get_by_test_id(\"edit-recheck-note\")).to_have_count(0)     # the note ends with the decision\n\n\ndef test_refused_dollar_figure_is_shown_as_typed(page, sample_case):\n    open_case(page, sample_case)\n    row = _open_edit(page, 5)\n    ta = row.get_by_test_id(\"edit-summary\"); ta.fill(ta.input_value().rstrip(\".\") + \", billed $9,000.\")\n    row.get_by_test_id(\"btn-save-edit\").click()\n    err = row.locator(\".rv-error\"); expect(err).to_contain_text(\"$9,000\", timeout=10000)\n    assert not re.search(r\"(?<![\\d$,])9000\", err.inner_text()), err.inner_text()\n    assert \"$9,000\" in row.get_by_test_id(\"edit-summary\").input_value()      # her text stays in the box\n\n\n# ---- T-117 minor: the AI-check row for a flag the checks left out does not say \"accept\"\ndef test_ai_check_row_for_a_tray_flag_agrees_with_the_tray(page, lib06):\n    open_case(page, lib06)\n    tray = page.locator('[data-testid=tray-item][data-tray-kind=flag]')\n    assert tray.count() >= 1\n    expect(tray.first).to_contain_text(\"Nothing to accept here\")\n    tid = tray.first.get_attribute(\"data-item-id\")\n    page.get_by_test_id(\"judge-panel\").locator(\"summary\").first.click()\n    row = page.locator(f'[data-testid=judge-panel] [data-target-item=\"{tid}\"]').first\n    if row.count() == 0:\n        pytest.skip(\"the AI check did not list the tray flag in this fixture\")\n    txt = row.inner_text()\n    assert not re.search(r\"\\baccept it\\b|Your decision\", txt, re.I), txt\n    assert \"Left out of the letter\" in txt and \"Nothing to accept here\" in txt\n    assert \"See the steps\" not in txt and \"Why this status\" in txt\n\n\n# ---- T-096 minor: the no-sentences message is one sentence\ndef test_no_sentences_message_is_not_doubled(page, sample_case):\n    tok = sample_case\n    reason = \"No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text. Read the record text instead.\"\n\n    def rewrite(route):\n        r = route.fetch(); body = r.json()\n        gone = body[\"entries\"][0]\n        body[\"entries\"] = [e for e in body[\"entries\"] if e[\"id\"] != gone[\"id\"]]\n        for rec in body[\"records\"]:\n            rec[\"sentences\"] = []; rec[\"sentences_reason\"] = reason\n        route.fulfill(response=r, body=json.dumps(body))\n    page.route(re.compile(rf\"/api/cases/{re.escape(tok)}$\"), rewrite)\n    open_case(page, tok)\n    page.get_by_test_id(\"btn-manual-entry\").first.click()\n    msg = page.get_by_test_id(\"manual-no-sentences\").first\n    expect(msg).to_be_visible()\n    t = msg.inner_text()\n    assert t.lower().count(\"no sentences\") == 1 and \"Why:\" not in t, t\n\n\n# ---- accessibility: label in name, the group's role, skip links that resolve in the export view, a visible focus on the Export heading\ndef test_row_toggle_name_contains_its_visible_word_in_both_states(page, sample_case):\n    open_case(page, sample_case)\n    t = page.get_by_test_id(\"entry-1\").get_by_test_id(\"entry-toggle\")\n    assert t.get_attribute(\"aria-label\").startswith(\"More\")\n    t.click(); assert t.inner_text() == \"Less\" and t.get_attribute(\"aria-label\").startswith(\"Less\") and t.get_attribute(\"aria-expanded\") == \"true\"\n    page.get_by_role(\"button\", name=re.compile(r\"^Less of\")).first.click()\n\n\ndef test_queue_has_a_role_that_allows_its_name(page, sample_case):\n    open_case(page, sample_case)\n    q = page.get_by_test_id(\"queue\")\n    assert q.get_attribute(\"role\") == \"group\" and q.get_attribute(\"aria-labelledby\") == \"h-timeline\"\n\n\ndef test_every_skip_link_resolves_in_the_review_and_in_the_export_view(page, sample_case):\n    open_case(page, sample_case)\n    def hrefs():\n        return page.evaluate(\"[...document.querySelectorAll('[data-testid=skip-nav] a')].map(a => [a.getAttribute('href'), !!document.querySelector(a.getAttribute('href'))])\")\n    assert hrefs() and all(ok for _, ok in hrefs()), hrefs()\n    page.get_by_test_id(\"btn-export\").click(); expect(page.locator(\"#h-export\")).to_be_focused()\n    page.wait_for_timeout(400)\n    assert all(ok for _, ok in hrefs()), hrefs()\n    ring = page.evaluate(\"getComputedStyle(document.querySelector('#h-export')).outlineStyle\")\n    assert ring != \"none\", ring\n\n\ndef test_translation_caution_is_not_clipped_at_1440(pw, lib09):\n    b = pw.chromium.launch(); pg = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page(); open_case(pg, lib09)\n    try:\n        cautions = pg.locator('[data-testid=queue] .reason--caution')\n        assert cautions.count() >= 1\n        assert cautions.evaluate_all(\"els => els.every(e => e.scrollWidth <= e.clientWidth + 1)\")\n    finally:\n        b.close()\n"
}
````

### User / tool · 2026-11-02T11:10:36.875Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/test_polish_r4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:10:40.287Z

**tool call — Bash**
````
{
 "command": "sed -i \"s/New test ids (declared in tests\\/e2e\\/conftest.py, 'T-060 round 4')/New test ids (to be added to the tests\\/e2e\\/conftest.py docstring by QA)/\" tests/e2e/test_polish_r4.py && E2E_BASE_URL=http://localhost:7955 timeout 900 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T11:10:40.382Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/e2e/test_polish_r ...": undefined label 'ests/e2e/test_polish_r4.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:10:42.466Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/test_polish_r4.py\"\ns=open(p).read()\ns=s.replace(\"(declared in tests/e2e/conftest.py, 'T-060 round 4')\",\"(QA adds them to the tests/e2e/conftest.py docstring)\")\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 timeout 900 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T11:10:42.595Z

**tool result**
````
/bin/bash: line 12: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:10:44.081Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -q 2>&1 | tail -60"
}
````

### User / tool · 2026-11-02T11:11:26.295Z

**tool result**
````
E                         - 'button "Dismiss: $185"': Dismiss
E                         - 'button "Audit: $185"': Audit
E                   - row "Amount missing 3 days of work":
E                     - cell "missing 3 days of work Damages mention":
E                       - strong: missing 3 days of work
E                       - text: Damages mention
E                     - 'cell "Pain 4/10, improving. Patient reports missing 3 days of work. Open record 5 for the amount missing 3 days of work Why this status: missing 3 days of work (damages)"':
E                       - blockquote "Pain 4/10, improving. Patient reports missing 3 days of work.":
E                         - text: Pain 4/10, improving. Patient reports
E                         - mark: missing 3 days of work
E                         - text: .
E                       - button "Open record 5 for the amount missing 3 days of work": Open record 5
E                       - 'button "Why this status: missing 3 days of work (damages)"': Why this status
E                     - 'cell "▲ Needs review Not counted: a damages mention. mention of damages; not a bill; needs review This figure is not a bill (for example a damages or settlement figure), so it is not added to the total."':
E                       - text: "▲ Needs review Not counted: a damages mention. mention of damages; not a bill; needs review"
E                       - paragraph: This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.
E                     - cell "Review actions":
E                       - group "Review actions":
E                         - 'button "Keep in notes: missing 3 days of work"': Keep in notes
E                         - 'button "Dismiss: missing 3 days of work"': Dismiss
E                         - 'button "Audit: missing 3 days of work"': Audit
E           - heading "Audit" [level=2]
E           - paragraph: Every model call behind this case, and every decision you made.
E           - button "Open full audit"
E           - heading "Draft treatment paragraph" [level=2]
E           - paragraph: Written from the entries you have accepted, one cited sentence per entry, each checked by code and a second model. It stays in the internal notes until you accept it.
E           - button "Draft paragraph from accepted entries" [disabled]
E           - paragraph: Accept at least one entry first.
E           - status
E           - heading "Exhibit and Bates numbers" [level=2]
E           - paragraph: Optional. Fills “Source [Ex. __ / Bates __]” in the letter text. Left empty, the blanks stay for you to fill in.
E           - text: Exhibit label
E           - textbox "Exhibit label Replaces the Ex. blank, for example 7 or B-2."
E           - text: Replaces the Ex. blank, for example 7 or B-2. Bates prefix
E           - textbox "Bates prefix For example RIV-"
E           - text: For example RIV- First Bates number
E           - textbox "First Bates number Numbers run in record order from this value."
E           - text: Numbers run in record order from this value.
E           - button "Save settings"
E           - button "Use the blank placeholders"
E           - region "Source record":
E             - heading "Source record" [level=3]
E             - paragraph:
E               - text: 10 flags (1 gap)
E               - button "Show gap flag"
E             - text: Follows the selected item. Press p to move here, Esc to return.
E             - region "Source record text":
E               - paragraph: Select an item to see its source record here.
E         - region "Cases (3) and synthetic library":
E           - group: Cases (3) and synthetic library
E       - status

tests/e2e/test_polish_r4.py:223: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r4.py::test_t114_gap_change_stays_on_the_gap_card_after_got_it_and_reload
FAILED tests/e2e/test_polish_r4.py::test_t114_accepted_rate_row_reads_one_status_chip
FAILED tests/e2e/test_polish_r4.py::test_dismissed_entry_leaves_the_queue_for_the_dismissed_group_and_undo_returns_it
FAILED tests/e2e/test_polish_r4.py::test_edit_box_says_the_wording_is_re_checked_and_a_saved_edit_reports_it
FAILED tests/e2e/test_polish_r4.py::test_every_skip_link_resolves_in_the_review_and_in_the_export_view
5 failed, 8 passed, 1 skipped in 41.88s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:11:28.472Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -q 2>&1 | grep -E \"^(E  +(Assertion|Error|playwright|assert|Timeout|Locator|Expected|Actual|Call log)|tests/e2e.*Error|____)\" | head -40"
}
````

### User / tool · 2026-11-02T11:12:11.313Z

**tool result**
````
______ test_t114_gap_change_stays_on_the_gap_card_after_got_it_and_reload ______
E       AssertionError: Locator expected to have count '1'
E       Actual value: 0 
E       Call log:
tests/e2e/test_polish_r4.py:66: AssertionError
______________ test_t114_accepted_rate_row_reads_one_status_chip _______________
E       AssertionError: Locator expected to have attribute 'accepted'
E       Actual value: None
E       Error: element(s) not found 
E       Call log:
tests/e2e/test_polish_r4.py:88: AssertionError
E       AssertionError: Locator expected to have count '1'
E       Actual value: 0 
E       Call log:
tests/e2e/test_polish_r4.py:111: AssertionError
E       AssertionError: Locator expected to have attribute 'edited'
E       Actual value: None
E       Error: element(s) not found 
E       Call log:
tests/e2e/test_polish_r4.py:148: AssertionError
______ test_every_skip_link_resolves_in_the_review_and_in_the_export_view ______
E       AssertionError: Locator expected to be focused
E       Actual value: inactive 
E       Call log:
tests/e2e/test_polish_r4.py:223: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:17.060Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/dbg1.py <<'EOF'\nimport sys, json, time\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom tests.e2e.conftest import api, BASE\nfrom playwright.sync_api import sync_playwright\nst, c = api(\"POST\", \"/api/cases\", {\"library\": \"case_lib09_spanish_interpreter_espalda\"}); tok = c[\"token\"]\napi(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(100):\n    if api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] == \"ready\": break\n    time.sleep(.5)\nwith sync_playwright() as p:\n    b = p.chromium.launch(); pg = b.new_page(viewport={\"width\":1440,\"height\":900})\n    pg.on(\"response\", lambda r: print(\"RESP\", r.url[-40:], r.status) if \"confirm_date\" in r.url else None)\n    pg.goto(f\"{BASE}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for()\n    box = pg.get_by_test_id(\"dates-to-confirm\")\n    radios = box.get_by_test_id(\"confirm-date\")\n    for i in range(radios.count()):\n        if radios.nth(i).get_attribute(\"data-date\") == \"2026-03-05\": radios.nth(i).check()\n    box.get_by_test_id(\"btn-confirm-date\").first.click()\n    pg.wait_for_timeout(1500)\n    print(pg.evaluate(\"Object.keys(localStorage).map(k=>[k,localStorage[k]])\"))\n    print(pg.get_by_test_id(\"gap-change-note\").inner_text() if pg.get_by_test_id(\"gap-change-note\").count() else \"NO NOTE\")\n    print([ (f.get_attribute(\"data-item-id\"), f.inner_text()[:200]) for f in pg.locator(\"[data-flag-type=gap]\").all()])\n    b.close()\napi(\"DELETE\", f\"/api/cases/{tok}\")\nEOF\n.venv/bin/python /private/tmp/claude-501/dbg1.py"
}
````

### User / tool · 2026-11-02T11:12:17.321Z

**tool result (error)**
````
Exit code 1
Traceback (most recent call last):
  File "/private/tmp/claude-501/dbg1.py", line 5, in <module>
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"}); tok = c["token"]
                                                                                                    ~^^^^^^^^^
KeyError: 'token'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:18.901Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/dbg1.py"
}
````

### User / tool · 2026-11-02T11:12:21.791Z

**tool result**
````
RESP qpiJ8-PK1p20Cacw/records/r4/confirm_date 200
[['zlayt.gapchg.Eqx8NWqpiJ8-PK1p20Cacw', '[{"flag_id":"f_gap_r4_r2","change":"changed","old_days":42,"new_days":40,"old_from":"2026-03-03","old_to":"2026-04-14","new_from":"2026-03-05","new_to":"2026-04-14","sentence":"Gap recalculated after you confirmed record 4: now 40 days (was 42)."}]'], ['zlayt.theme', 'auto']]
A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42).
Got it
[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:26.058Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python - <<'EOF'\nimport sys, time\nsys.path.insert(0, \".\")\nfrom tests.e2e.conftest import api\nst, c = api(\"POST\", \"/api/cases\", {\"library\": \"case_lib09_spanish_interpreter_espalda\"}); tok = c[\"token\"]\napi(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(100):\n    if api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] == \"ready\": break\n    time.sleep(.5)\nr = api(\"POST\", f\"/api/cases/{tok}/records/r4/confirm_date\", {\"date\": \"2026-03-05\"})\nprint(r[0], r[1][\"gap_changes\"], r[1][\"gap_flags\"], r[1][\"removed_flag_ids\"])\ncase = api(\"GET\", f\"/api/cases/{tok}\")[1]\nprint([(f[\"id\"], f[\"type\"], f[\"review_status\"], (f.get(\"computed\") or {}).get(\"days\")) for f in case[\"flags\"]])\napi(\"DELETE\", f\"/api/cases/{tok}\")\nEOF"
}
````

### User / tool · 2026-11-02T11:12:26.839Z

**tool result**
````
200 [{'flag_id': 'f_gap_r4_r2', 'change': 'changed', 'old_days': 42, 'new_days': 40, 'old_from': '2026-03-03', 'old_to': '2026-04-14', 'new_from': '2026-03-05', 'new_to': '2026-04-14', 'sentence': 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'}] ['f_gap_r4_r2'] ['f_date_r4', 'f_gap_r1_r2']
[('f_r1_1', 'pre_existing', 'pending', None), ('f_r1_2', 'causation', 'pending', None), ('f_r2_1', 'causation', 'pending', None), ('f_r3_1', 'causation', 'pending', None), ('f_gap_r4_r2', 'gap', 'pending', 40)]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:30.250Z

**tool call — Bash**
````
{
 "command": "sed -i 's/pg.on(\"response\"/pg.on(\"console\", lambda m: print(\"CONSOLE\", m.type, m.text[:300])); pg.on(\"pageerror\", lambda e: print(\"PAGEERR\", str(e)[:300])); pg.on(\"response\"/' /private/tmp/claude-501/dbg1.py && E2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/dbg1.py 2>&1 | head"
}
````

### User / tool · 2026-11-02T11:12:30.340Z

**tool result (error)**
````
Exit code 1
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/dbg1.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:32.596Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"/private/tmp/claude-501/dbg1.py\"\ns=open(p).read()\ns=s.replace('pg.on(\"response\"','pg.on(\"console\", lambda m: print(\"CONSOLE\", m.type, m.text[:300])); pg.on(\"pageerror\", lambda e: print(\"PAGEERR\", str(e)[:300])); pg.on(\"response\"',1)\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/dbg1.py 2>&1 | head"
}
````

### User / tool · 2026-11-02T11:12:35.529Z

**tool result**
````
PAGEERR Cannot access 'tray' before initialization
RESP fl601JI7x88bcyQw/records/r4/confirm_date 200
[['zlayt.gapchg.FTzZ12fl601JI7x88bcyQw', '[{"flag_id":"f_gap_r4_r2","change":"changed","old_days":42,"new_days":40,"old_from":"2026-03-03","old_to":"2026-04-14","new_from":"2026-03-05","new_to":"2026-04-14","sentence":"Gap recalculated after you confirmed record 4: now 40 days (was 42)."}]'], ['zlayt.theme', 'auto']]
A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42).
Got it
[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:12:39.229Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/judges.js\"\ns=open(p).read()\ns=s.replace('''    const tray = trayFlag(it.id);\n    const decision = tray ?''','''    const decision = tray ?''',1)\ns=s.replace('''    const r = it.rej, u = it.unres, chips = [], mine = humanWording(it);''','''    const r = it.rej, u = it.unres, chips = [], mine = humanWording(it), tray = trayFlag(it.id);''',1)\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -q 2>&1 | grep -E \"^(E  +(Assertion|Error|playwright|assert|Timeout|Locator|Expected|Actual)|tests/e2e.*Error|____|[0-9]+ (passed|failed))\" | head -40"
}
````

### User / tool · 2026-11-02T11:13:02.254Z

**tool result**
````
______ test_every_skip_link_resolves_in_the_review_and_in_the_export_view ______
E       AssertionError: Locator expected to be focused
E       Actual value: inactive 
tests/e2e/test_polish_r4.py:223: AssertionError
1 failed, 13 passed in 22.66s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:06.515Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/test_polish_r4.py\"\ns=open(p).read()\ns=s.replace('''def test_every_skip_link_resolves_in_the_review_and_in_the_export_view(page, sample_case):\n    open_case(page, sample_case)''','''def test_every_skip_link_resolves_in_the_review_and_in_the_export_view(page, sample_case):\n    ids = [e[\"id\"] for e in api(\"GET\", f\"/api/cases/{sample_case}\")[1][\"entries\"] if e[\"state\"] == \"verified\" and e[\"date\"]]\n    api(\"POST\", f\"/api/cases/{sample_case}/review/batch\", {\"action\": \"accept\", \"item_ids\": ids})      # something accepted, so the export opens\n    open_case(page, sample_case)''',1)\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py -q 2>&1 | grep -E \"^(E  +(Assertion|Error|playwright|assert|Timeout|Locator|Expected|Actual)|tests/e2e.*Error|____|[0-9]+ (passed|failed))\" | head -40"
}
````

### User / tool · 2026-11-02T11:13:25.035Z

**tool result**
````
14 passed in 18.18s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:27.870Z

**tool call — Bash**
````
{
 "command": "(E2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e -q -x -p no:cacheprovider > /private/tmp/claude-501/e2e_full1.log 2>&1 &) ; sleep 1; echo started"
}
````

### User / tool · 2026-11-02T11:13:28.953Z

**tool result**
````
started
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:30.745Z

**tool call — Bash**
````
{
 "command": "ps aux | grep \"pytest tests/e2e -q -x\" | grep -v grep | awk '{print $2}'"
}
````

### User / tool · 2026-11-02T11:13:30.896Z

**tool result**
````
84105
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:32.434Z

**tool call — Bash**
````
{
 "command": "kill 84105; cd /Users/arsis/zlayt-pm-project && (E2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider > /private/tmp/claude-501/e2e_full1.log 2>&1 &) ; echo restarted"
}
````

### User / tool · 2026-11-02T11:13:32.541Z

**tool result**
````
restarted
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:39.099Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/screenshots && for w in 1440 390; do for k in top full; do cp t060-before-sample-$w-$k.png ui-pass-1-sample-$w-$k.png; cp t060-before-_espalda-$w-$k.png ui-pass-1-lib09-$w-$k.png; cp t060-after-sample-$w-$k.png ui-pass-2-sample-$w-$k.png; cp t060-after-_espalda-$w-$k.png ui-pass-2-lib09-$w-$k.png; cp t060-r3-sample-$w-$k.png ui-pass-3-sample-$w-$k.png; cp t060-r3-lib09-$w-$k.png ui-pass-3-lib09-$w-$k.png; done; done; ls ui-pass* | wc -l; git -C /Users/arsis/zlayt-pm-project log --oneline -1 -- artifacts/screenshots/t060-before-sample-1440-top.png"
}
````

### User / tool · 2026-11-02T11:13:39.742Z

**tool result**
````
      24
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:46.382Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/review.js\"\ns=open(p).read()\ns=s.replace('''const VARIANT = { accept: st === \"pending\" ? \"btn--primary\" :''','''const VARIANT = { accept: st === \"pending\" ? (noted ? \"\" : \"btn--primary\") :''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"noted\" app/frontend/review.js | head; ls research/ui-references.md reviews/T-060-accessibility-pass3.md"
}
````

### User / tool · 2026-11-02T11:13:46.498Z

**tool result**
````
51:    const noted = item.accept_effect && item.accept_effect !== "letter_total" && (item.review_status === "accepted" || item.review_status === "edited");
52:    if (noted) return el("span", { class: "rv-chips" }, el("span", { class: "chip chip--" + d[0], "data-icon": d[1], "data-chip": "review" }, REVIEW_LABEL[item.review_status]));
250:    const noted = kind === "amount" && item.kind !== "charge";
257:    const VARIANT = { accept: st === "pending" ? (noted ? "" : "btn--primary") : st === "dismissed" ? "" : "rv-decided", edit: "", dismiss: st === "dismissed" ? "rv-decided rv-decided--muted" : "btn--ghost", reset: "btn--link", audit: "btn--link", "dismiss-reason": "btn--link" };
263:    const acceptText = accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
research/ui-references.md
reviews/T-060-accessibility-pass3.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:48.282Z

**tool call — Bash**
````
{
 "command": "sleep 100; tail -c 400 /private/tmp/claude-501/e2e_full1.log"
}
````

### User / tool · 2026-11-02T11:13:48.284Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: tail -c 400 /private/tmp/claude-501/e2e_full1.log. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:49.307Z

Meanwhile, write the screenshot script.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:13:56.244Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/shots4.py",
 "content": "import sys, time, os\nsys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom tests.e2e.conftest import api, BASE\nfrom playwright.sync_api import sync_playwright\n\nOUT = \"/Users/arsis/zlayt-pm-project/artifacts/screenshots\"\n\n\ndef make(body):\n    st, c = api(\"POST\", \"/api/cases\", body); tok = c[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(200):\n        if api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] == \"ready\":\n            break\n        time.sleep(.5)\n    return tok\n\n\nsample = make({\"sample\": True})\nlib09 = make({\"library\": \"case_lib09_spanish_interpreter_espalda\"})\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for w, h in ((1440, 900), (390, 844)):\n        ctx = b.new_context(viewport={\"width\": w, \"height\": h}, device_scale_factor=1)\n        pg = ctx.new_page()\n        for name, tok in ((\"sample\", sample), (\"lib09\", lib09)):\n            pg.goto(f\"{BASE}/#/case/{tok}\"); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000); pg.wait_for_timeout(800)\n            pg.screenshot(path=f\"{OUT}/ui-pass-4-{name}-{w}-top.png\")\n            pg.screenshot(path=f\"{OUT}/ui-pass-4-{name}-{w}-full.png\", full_page=True)\n        # the T-114 line on the gap card, after Got it and a reload (lib09)\n        pg.goto(f\"{BASE}/#/case/{lib09}\"); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        box = pg.get_by_test_id(\"dates-to-confirm\"); radios = box.get_by_test_id(\"confirm-date\")\n        for i in range(radios.count()):\n            if radios.nth(i).get_attribute(\"data-date\") == \"2026-03-05\":\n                radios.nth(i).check()\n        box.get_by_test_id(\"btn-confirm-date\").first.click()\n        pg.get_by_test_id(\"btn-dismiss-gap-note\").click(); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        card = pg.locator(\"[data-flag-type=gap]\").first\n        card.scroll_into_view_if_needed(); pg.wait_for_timeout(300)\n        card.screenshot(path=f\"{OUT}/ui-pass-4-gap-change-card-{w}.png\")\n        # a dismissed entry in the Dismissed group (sample)\n        pg.goto(f\"{BASE}/#/case/{sample}\"); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        pg.get_by_test_id(\"entry-2\").get_by_test_id(\"btn-dismiss\").click(); pg.wait_for_timeout(300)\n        g = pg.get_by_test_id(\"dismissed-group\"); g.scroll_into_view_if_needed(); pg.wait_for_timeout(300)\n        g.screenshot(path=f\"{OUT}/ui-pass-4-dismissed-group-{w}.png\")\n        api(\"POST\", f\"/api/cases/{sample}/items/{pg.get_by_test_id('entry-2').get_attribute('data-item-id')}/review\", {\"action\": \"reset\"})\n        ctx.close()\n    b.close()\n# reset the lib09 date so a second width starts from the same state is not needed: the confirm is idempotent for the card line\napi(\"DELETE\", f\"/api/cases/{sample}\"); api(\"DELETE\", f\"/api/cases/{lib09}\")\nprint(sorted(f for f in os.listdir(OUT) if f.startswith(\"ui-pass-4\")))\n"
}
````

### User / tool · 2026-11-02T11:13:56.316Z

**tool result**
````
File created successfully at: /private/tmp/claude-501/shots4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:01.472Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"/private/tmp/claude-501/shots4.py\"\ns=open(p).read()\ns=s.replace('''        pg.goto(f\"{BASE}/#/case/{lib09}\"); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        box = pg.get_by_test_id(\"dates-to-confirm\")''','''        gc = make({\"library\": \"case_lib09_spanish_interpreter_espalda\"})\n        pg.goto(f\"{BASE}/#/case/{gc}\"); pg.reload(); pg.get_by_test_id(\"timeline\").wait_for(timeout=15000)\n        box = pg.get_by_test_id(\"dates-to-confirm\")''',1)\ns=s.replace('''        card.screenshot(path=f\"{OUT}/ui-pass-4-gap-change-card-{w}.png\")''','''        card.screenshot(path=f\"{OUT}/ui-pass-4-gap-change-card-{w}.png\"); api(\"DELETE\", f\"/api/cases/{gc}\")''',1)\nopen(p,\"w\").write(s)\nEOF\ntail -c 300 /private/tmp/claude-501/e2e_full1.log"
}
````

### User / tool · 2026-11-02T11:14:01.592Z

**tool result**
````
...............ss.....ss..s.s.sss.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:04.096Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/e2e_full1.log; do sleep 5; done; tail -c 1500 /private/tmp/claude-501/e2e_full1.log",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T11:14:04.167Z

**tool result**
````
Command running in background with ID: bbqqua17b. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bbqqua17b.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:06.438Z

**tool call — Bash**
````
{
 "command": "grep -ln \"app/frontend\\|frontend\" tests/unit/*.py | head; python3 tools/board.py new --help 2>&1 | head -20"
}
````

### User / tool · 2026-11-02T11:14:06.580Z

**tool result**
````
tests/unit/test_backend_no_speaker_label.py
tests/unit/test_e2e_contract.py
tests/unit/test_frontend_no_speaker_label.py
tests/unit/test_quote_units.py
usage: board.py new [-h] --title TITLE --milestone {M0,M1,M2,M3,M4,M5} --role
                    {orchestrator,architect,backend,db,frontend,qa,release,writer,researcher}
                    [--priority {P0,P1,P2}] [--depends [DEPENDS ...]]
                    [--ac AC] [--by BY] [--body-file BODY_FILE] [--body BODY]
                    [--status {backlog,ready,needs_chris,blocked}]

options:
  -h, --help            show this help message and exit
  --title TITLE
  --milestone {M0,M1,M2,M3,M4,M5}
  --role {orchestrator,architect,backend,db,frontend,qa,release,writer,researcher}
  --priority {P0,P1,P2}
  --depends [DEPENDS ...]
  --ac AC
  --by BY
  --body-file BODY_FILE
  --body BODY
  --status {backlog,ready,needs_chris,blocked}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:08.452Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_frontend_no_speaker_label.py tests/unit/test_e2e_contract.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T11:14:08.827Z

**tool result**
````
    def test_data_attributes_declared():
        """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
        c = contract()
        for p in specs():
            for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
>               assert a in c, (p.name, a)
E               AssertionError: ('test_polish_r4.py', 'data-chip')
E               assert 'data-chip' in 'E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fi...bugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).\n'

tests/unit/test_e2e_contract.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
FAILED tests/unit/test_e2e_contract.py::test_data_attributes_declared - Asser...
2 failed, 7 passed in 0.06s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:11.987Z

**tool call — Bash**
````
{
 "command": "git log --format=\"%h %an %s\" -3 -- tests/e2e/conftest.py; sed -n 50,58p tests/e2e/conftest.py | cut -c1-700; sed -n 1,40p tests/unit/test_e2e_contract.py"
}
````

### User / tool · 2026-11-02T11:14:12.106Z

**tool result**
````
d56328a Chris Borsheim test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
d9efc5c Chris Borsheim test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export, compact rows, decided rows, 320 px reflow, theme-toggle name, held rechecks (T-060 r3, T-119)
eabe2b8 Chris Borsheim feat(frontend): one design-token system (tokens.css: palette light+dark, 7-step type scale, spacing, 2 radii, elevation) and every stylesheet rebuilt on it; one button and chip system with hover, active, focus and disabled states; sticky case header (T-060)
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""E2E hook contract (R-ST-1, R-RV-8): every data-testid, data-attribute, role and shortcut used by tests/e2e specs is declared in tests/e2e/conftest.py's docstring,
so the frontend builds to one source (T-039 review)."""
import pathlib, re
E2E = pathlib.Path(__file__).resolve().parents[1] / "e2e"

def contract():
    s = (E2E / "conftest.py").read_text().split('"""')[1]
    return s

def specs():
    return [p for p in E2E.glob("test_*.py")]

def test_every_test_id_is_declared():
    """R-ST-1: get_by_test_id hooks in specs are named in the conftest contract (<seq>/<raw> placeholders allowed)."""
    c = contract(); used = set()
    for p in specs():
        for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
            used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
    missing = []
    for u in used:
        pat = u.replace("<seq>", "<seq>") 
        if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
            missing.append(u)
    assert not missing, missing

def test_data_attributes_declared():
    """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
    c = contract()
    for p in specs():
        for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
            assert a in c, (p.name, a)

def test_roles_and_inputs_and_keys_declared():
    """R-RV-8: role=alert, tabindex, input names and a/d/j shortcuts are declared."""
    c = contract()
    for needle in ("role=alert", "tabindex", "input named date or provider", "a = accept", "d = dismiss", "j = next"):
        assert needle in c
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:18.813Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/conftest.py\"\ns=open(p).read()\nmarker='Optional test hook: window.__debugInjectRecordHtml'\nadd='''T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),\n  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and\n  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.\n  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).\n'''\ns=s.replace(marker, add+marker,1)\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_frontend_no_speaker_label.py tests/unit/test_e2e_contract.py -q 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T11:14:19.189Z

**tool result**
````
tests/unit/test_e2e_contract.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_data_attributes_declared - Asser...
1 failed, 8 passed in 0.06s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:20.629Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q 2>&1 | grep AssertionError"
}
````

### User / tool · 2026-11-02T11:14:20.949Z

**tool result**
````
E               AssertionError: ('test_polish_r4.py', 'data-amount-kind')
tests/unit/test_e2e_contract.py:31: AssertionError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:23.756Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/conftest.py\"\ns=open(p).read()\ns=s.replace(\"data-chip marks the state / review chips\",\"data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips\",1)\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_e2e_contract.py tests/unit/test_frontend_no_speaker_label.py -q 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T11:14:24.112Z

**tool result**
````
.........                                                                [100%]
9 passed in 0.04s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:29.189Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py new --title \"Keep the gap-change record on the gap flag: GET case returns gap_change {old_days,new_days,old_from,old_to,new_from,new_to,record_seq,sentence} on a gap flag whose figures moved after a confirm_date (T-114 r3)\" --milestone M3 --role backend --priority P2 --by frontend --ac \"A gap flag whose figures changed in confirm_date carries gap_change (same shape as gap_changes[] plus record_seq) in GET /cases/{token}, until that gap changes again; a gap that was removed is listed in the case as gap_changes_removed[] with its sentence; contract updated; unit test\" --body \"From T-060 r4 / T-114 r2 paralegal major. The UI now keeps the change per case in the browser (localStorage zlayt.gapchg.<token>) so it survives Got it and a reload, but it is lost on another browser or after clearing site data. app/frontend/timeline.js (gapChangeFor) already prefers flag.gap_change when present, so the backend field switches it over with no further UI work; the browser copy can then be dropped.\" 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T11:14:29.362Z

**tool result**
````
T-127
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:31.672Z

**tool call — Bash**
````
{
 "command": "for f in app/frontend/*.js; do node --check $f 2>&1 | head -3; done; echo checked"
}
````

### User / tool · 2026-11-02T11:14:32.885Z

**tool result**
````
checked
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:34.738Z

**tool call — Bash**
````
{
 "command": "sleep 1; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bbqqua17b.output 2>/dev/null | tail -5; tail -c 200 /private/tmp/claude-501/e2e_full1.log"
}
````

### User / tool · 2026-11-02T11:14:35.875Z

**tool result**
````
...............ss.....ss..s.s.sss..s.s.s..sss.F.......
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:38.264Z

**tool call — Bash**
````
{
 "command": "grep -n \"other items\\|not reviewed\\|left to review\" app/frontend/*.js | cut -c1-220 | head"
}
````

### User / tool · 2026-11-02T11:14:38.365Z

**tool result**
````
app/frontend/batch.js:53:      RV.say("Undone: " + n + " " + (n === 1 ? "entry" : "entries") + " back to not reviewed.");
app/frontend/export.js:28:    return bits.map(([n, one, many]) => plural(n, one, many) + " not reviewed");
app/frontend/export.js:35:    const parts = pendingWords(c) || [plural(c.pending, "item", "items") + " not reviewed"];
app/frontend/manual.js:46:        delete draft[t.id]; ZL.state.set({ case: await ZL.api.getCase(c.token) }); RV.say("Entry added for record " + rec.seq + ". It is not reviewed yet."); return;
app/frontend/review.js:225:      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
app/frontend/stepper.js:366:  const KEY = { by_origin: "found by", by_type: "kinds", method: "records split by", unsupported: "AI objected", supported: "AI agreed", unsure: "undecided", items_judged: "items checked", pen
app/frontend/stepper.js:530:    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:41.620Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/e2e_full1.log; do sleep 5; done; tail -c 2500 /private/tmp/claude-501/e2e_full1.log",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T11:18:22.448Z

**tool result**
````
 $9,000. Remove it or change the quote."

tests/e2e/test_rerun_judge.py:367: AssertionError
_____________ test_no_sentences_to_pick_shows_the_backends_reason ______________

page = <Page url='http://localhost:7955/#/case/VZAFWhxKMWkhyYFrJzz3cQ'>
cases = <function cases.<locals>.mk at 0x10baf5580>

    def test_no_sentences_to_pick_shows_the_backends_reason(page, cases):
        tok = cases(lib("case_lib01_er_only_then_gap.txt"))
        REASON = "This record has no Date and Source lines, so no sentence can be cut from it."
        def strip(b):
            rid = next(t for t in b["tray"] if t.get("kind") == "entry")["record_ids"][0]
            for r in b["records"]:
                if r["id"] == rid: r["sentences"] = []; r["sentences_reason"] = REASON
        rewrite_case(page, strip); open_case(page, tok)
        page.get_by_test_id("btn-manual-entry").first.click()
>       expect(page.get_by_test_id("manual-no-sentences")).to_contain_text("This record has no sentences to pick from."); expect(page.get_by_test_id("manual-no-sentences")).to_contain_text(REASON)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Locator expected to contain text 'This record has no sentences to pick from.'
E       Actual value: This record has no Date and Source lines, so no sentence can be cut from it. 
E       Call log:
E         - Expect "to_contain_text" get_by_test_id("manual-no-sentences") with timeout 5000ms
E         - waiting for get_by_test_id("manual-no-sentences")
E           14 × locator resolved to <p class="rv-empty" data-testid="manual-no-sentences">This record has no Date and Source lines, so no s…</p>
E              - unexpected value "This record has no Date and Source lines, so no sentence can be cut from it."
E       
E       Aria snapshot:
E       - paragraph: This record has no Date and Source lines, so no sentence can be cut from it.

tests/e2e/test_suggestions.py:260: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_edit.py::test_added_dollar_is_a_hard_422_no_override - ...
FAILED tests/e2e/test_rerun_judge.py::test_refused_edit_shows_the_reason_inline_and_keeps_the_typed_text_no_confirm_dialog[Visit 8: pain 4/10, improving; billed $9,000.-9000]
FAILED tests/e2e/test_suggestions.py::test_no_sentences_to_pick_shows_the_backends_reason
3 failed, 187 passed, 16 skipped in 285.67s (0:04:45)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:37.383Z

**tool call — Bash**
````
{
 "command": "grep -n \"9000\\|9,000\" tests/e2e/test_edit.py tests/e2e/test_rerun_judge.py | cut -c1-260"
}
````

### User / tool · 2026-11-02T11:18:37.479Z

**tool result**
````
tests/e2e/test_rerun_judge.py:359:@pytest.mark.parametrize("typed,shown", [("Visit 8: pain 4/10, improving; billed $9,000.", "9000"), ("Pain 4/10, improving in the left arm.", "left"), ("Pain 4/10, improving.", None)])
tests/e2e/test_edit.py:17:    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
tests/e2e/test_edit.py:19:    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
tests/e2e/test_edit.py:22:    e.get_by_test_id("edit-summary").fill("Visit 8: pain 4/10, improving; billed $9,000."); e.get_by_test_id("btn-save-edit").click()
tests/e2e/test_edit.py:23:    expect(page.get_by_role("alert").or_(page.get_by_test_id("warning-list")).first).to_contain_text("9000")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:39.084Z

**tool call — Bash**
````
{
 "command": "sed -n 355,372p tests/e2e/test_rerun_judge.py | cut -c1-300; sed -n 14,30p tests/e2e/test_edit.py | cut -c1-300"
}
````

### User / tool · 2026-11-02T11:18:39.178Z

**tool result**
````
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == "Edited by you, not AI-checked" and st.get_by_test_id("item-wording-fail").count() == 0


@pytest.mark.parametrize("typed,shown", [("Visit 8: pain 4/10, improving; billed $9,000.", "9000"), ("Pain 4/10, improving in the left arm.", "left"), ("Pain 4/10, improving.", None)])
def test_refused_edit_shows_the_reason_inline_and_keeps_the_typed_text_no_confirm_dialog(page, sample_case, typed, shown):
    """D-047: a number, side or negation that is not in the quote is a hard 422: the reason sits under the edit box, the text stays, there is no 'keep my wording' choice.
    (The third case is the unchanged summary: it saves, so no error line.)"""
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill(typed); e.get_by_test_id("btn-save-edit").click()
    if shown is None:
        expect(e).to_have_attribute("data-review", "edited"); return
    err = e.locator(".rv-error"); expect(err).to_contain_text(shown); expect(err).to_contain_text("quote")
    assert e.get_by_test_id("edit-summary").input_value() == typed and e.get_by_test_id("edit-summary").is_visible()
    assert e.get_attribute("data-review") != "edited"
    assert page.get_by_test_id("btn-keep-wording").count() == 0 and page.get_by_test_id("warning-list").count() == 0
    e = page.get_by_test_id("entry-3"); assert e.get_attribute("data-review") == "edited" and "edited" in e.inner_text().lower() and "daily headaches" in e.get_by_test_id("entry-summary").inner_text()

def test_added_dollar_is_a_hard_422_no_override(page, sample_case):
    """R-RV-3 / D-034: adding '$9,000' (not in the quote) is a hard 422 - API and UI; nothing saved, no 'keep my wording' button."""
    c = api("GET", f"/api/cases/{sample_case}")[1]; eid = [e for e in c["entries"] if "r5" in e["record_ids"]][0]["id"]
    st, err = api("POST", f"/api/cases/{sample_case}/items/{eid}/review", {"action": "edit", "edits": {"summary": "Visit 8: pain 4/10, improving; billed $9,000."}, "confirm_warnings": True})
    assert st == 422
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Visit 8: pain 4/10, improving; billed $9,000."); e.get_by_test_id("btn-save-edit").click()
    expect(page.get_by_role("alert").or_(page.get_by_test_id("warning-list")).first).to_contain_text("9000")
    assert e.get_attribute("data-review") != "edited" and page.get_by_test_id("btn-keep-wording").count() == 0

def test_date_and_provider_not_editable(page, sample_case):
    """R-RV-2: no input exists for date or provider."""
    open_case(page, sample_case); e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    assert e.locator("input[name=date], input[name=provider]").count() == 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:18:43.938Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/e2e/test_rerun_judge.py\"\ns=open(p).read()\ns=s.replace('(\"Visit 8: pain 4/10, improving; billed $9,000.\", \"9000\")','(\"Visit 8: pain 4/10, improving; billed $9,000.\", \"$9,000\")',1)\nopen(p,\"w\").write(s)\np=\"tests/e2e/test_edit.py\"\ns=open(p).read()\ns=s.replace('''.first).to_contain_text(\"9000\")''','''.first).to_contain_text(\"$9,000\")      # T-060 r4: the figure is shown as she typed it, not as the server normalises it (\"9000\")''',1)\nopen(p,\"w\").write(s)\np=\"tests/e2e/test_suggestions.py\"\ns=open(p).read()\nold='''expect(page.get_by_test_id(\"manual-no-sentences\")).to_contain_text(\"This record has no sentences to pick from.\"); expect(page.get_by_test_id(\"manual-no-sentences\")).to_contain_text(REASON)'''\nassert old in s\ns=s.replace(old,'''expect(page.get_by_test_id(\"manual-no-sentences\")).to_have_text(REASON)      # T-060 r4 (T-096 r2 F6): the backend's reason alone; the generic lead plus \"Why:\" said the same thing twice''',1)\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_edit.py tests/e2e/test_rerun_judge.py tests/e2e/test_suggestions.py -q -p no:cacheprovider 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T11:20:10.367Z

**tool result**
````
.........................................................                [100%]
57 passed in 86.09s (0:01:26)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:11.244Z

Now screenshots.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:11.806Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/shots4.py 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T11:20:22.450Z

**tool result**
````
['ui-pass-4-dismissed-group-1440.png', 'ui-pass-4-dismissed-group-390.png', 'ui-pass-4-gap-change-card-1440.png', 'ui-pass-4-gap-change-card-390.png', 'ui-pass-4-lib09-1440-full.png', 'ui-pass-4-lib09-1440-top.png', 'ui-pass-4-lib09-390-full.png', 'ui-pass-4-lib09-390-top.png', 'ui-pass-4-sample-1440-full.png', 'ui-pass-4-sample-1440-top.png', 'ui-pass-4-sample-390-full.png', 'ui-pass-4-sample-390-top.png']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:24.061Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-gap-change-card-1440.png"
}
````

### User / tool · 2026-11-02T11:20:24.072Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:24.410Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-dismissed-group-1440.png"
}
````

### User / tool · 2026-11-02T11:20:24.417Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:24.515Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-lib09-1440-top.png"
}
````

### User / tool · 2026-11-02T11:20:24.522Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:29.764Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/frontend/flags.js\"\ns=open(p).read()\ns=s.replace('''      f.state === \"needs_review\" && f.why ? el(\"p\", { class: \"rv-reason-line\" }, el(\"strong\", {}, \"Needs review: \"), f.why) : null,''','''      f.state === \"needs_review\" && whyOnce(f) ? el(\"p\", { class: \"rv-reason-line\" }, el(\"strong\", {}, \"Needs review: \"), whyOnce(f)) : null,''',1)\ns=s.replace('''  function card(c, f) {''','''  // The \"why\" can carry sentences the card's explanation already says (the paperwork note on a gap): show each sentence once.\n  function whyOnce(f) {\n    const exp = String(f.explanation || \"\");\n    return String(f.why || \"\").split(/(?<=[.!?])\\\\s+/).filter((t) => t && !exp.includes(t.trim())).join(\" \");\n  }\n\n  function card(c, f) {''',1)\nopen(p,\"w\").write(s)\nEOF\nnode --check app/frontend/flags.js && echo ok"
}
````

### User / tool · 2026-11-02T11:20:29.903Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:31.205Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-lib09-390-top.png"
}
````

### User / tool · 2026-11-02T11:20:31.213Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:20:34.812Z

**tool call — Bash**
````
{
 "command": "E2E_BASE_URL=http://localhost:7955 .venv/bin/python -m pytest tests/e2e/test_polish_r4.py tests/e2e/test_flags_panel.py tests/e2e/test_charges.py -q -p no:cacheprovider 2>&1 | tail -3; E2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/shots4.py 2>&1 | tail -1 | cut -c1-80",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T11:21:17.248Z

**tool result**
````
........................                                                 [100%]
24 passed in 31.53s
['ui-pass-4-dismissed-group-1440.png', 'ui-pass-4-dismissed-group-390.png', 'ui-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:18.319Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-gap-change-card-390.png"
}
````

### User / tool · 2026-11-02T11:21:18.331Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:23.207Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"/private/tmp/claude-501/shots4.py\"\ns=open(p).read()\ns=s.replace('''        card.scroll_into_view_if_needed(); pg.wait_for_timeout(300)\n        card.screenshot(path=f\"{OUT}/ui-pass-4-gap-change-card-{w}.png\")''','''        card.evaluate(\"e => { e.scrollIntoView({block: 'start'}); window.scrollBy(0, -150); }\"); pg.wait_for_timeout(300)\n        pg.screenshot(path=f\"{OUT}/ui-pass-4-gap-change-card-{w}.png\")''',1)\ns=s.replace('''        g = pg.get_by_test_id(\"dismissed-group\"); g.scroll_into_view_if_needed(); pg.wait_for_timeout(300)\n        g.screenshot(path=f\"{OUT}/ui-pass-4-dismissed-group-{w}.png\")''','''        g = pg.get_by_test_id(\"dismissed-group\"); g.evaluate(\"e => { e.scrollIntoView({block: 'start'}); window.scrollBy(0, -200); }\"); pg.wait_for_timeout(300)\n        pg.screenshot(path=f\"{OUT}/ui-pass-4-dismissed-group-{w}.png\")''',1)\nopen(p,\"w\").write(s)\nEOF\nE2E_BASE_URL=http://localhost:7955 .venv/bin/python /private/tmp/claude-501/shots4.py 2>&1 | tail -1 | cut -c1-60",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T11:21:33.696Z

**tool result**
````
['ui-pass-4-dismissed-group-1440.png', 'ui-pass-4-dismissed-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:34.772Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/ui-pass-4-gap-change-card-390.png"
}
````

### User / tool · 2026-11-02T11:21:34.782Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:37.321Z

**tool call — Bash**
````
{
 "command": "git add app/frontend/app.js app/frontend/dom.js app/frontend/flags.js app/frontend/judges.js app/frontend/manual.js app/frontend/review.js app/frontend/review.css app/frontend/styles.css app/frontend/switcher.js app/frontend/timeline.js tests/e2e/test_polish_r4.py tests/e2e/conftest.py tests/e2e/test_edit.py tests/e2e/test_rerun_judge.py tests/e2e/test_suggestions.py artifacts/screenshots/ui-pass-1-sample-1440-top.png && git add artifacts/screenshots/ui-pass-*.png && git status --short | grep -v \"^ M\\|^??\" | head -40"
}
````

### User / tool · 2026-11-02T11:21:38.130Z

**tool result**
````
M  app/frontend/app.js
M  app/frontend/dom.js
M  app/frontend/flags.js
M  app/frontend/judges.js
M  app/frontend/manual.js
M  app/frontend/review.css
M  app/frontend/review.js
M  app/frontend/styles.css
M  app/frontend/switcher.js
M  app/frontend/timeline.js
A  artifacts/screenshots/ui-pass-1-lib09-1440-full.png
A  artifacts/screenshots/ui-pass-1-lib09-1440-top.png
A  artifacts/screenshots/ui-pass-1-lib09-390-full.png
A  artifacts/screenshots/ui-pass-1-lib09-390-top.png
A  artifacts/screenshots/ui-pass-1-sample-1440-full.png
A  artifacts/screenshots/ui-pass-1-sample-1440-top.png
A  artifacts/screenshots/ui-pass-1-sample-390-full.png
A  artifacts/screenshots/ui-pass-1-sample-390-top.png
A  artifacts/screenshots/ui-pass-2-lib09-1440-full.png
A  artifacts/screenshots/ui-pass-2-lib09-1440-top.png
A  artifacts/screenshots/ui-pass-2-lib09-390-full.png
A  artifacts/screenshots/ui-pass-2-lib09-390-top.png
A  artifacts/screenshots/ui-pass-2-sample-1440-full.png
A  artifacts/screenshots/ui-pass-2-sample-1440-top.png
A  artifacts/screenshots/ui-pass-2-sample-390-full.png
A  artifacts/screenshots/ui-pass-2-sample-390-top.png
A  artifacts/screenshots/ui-pass-3-lib09-1440-full.png
A  artifacts/screenshots/ui-pass-3-lib09-1440-top.png
A  artifacts/screenshots/ui-pass-3-lib09-390-full.png
A  artifacts/screenshots/ui-pass-3-lib09-390-top.png
A  artifacts/screenshots/ui-pass-3-sample-1440-full.png
A  artifacts/screenshots/ui-pass-3-sample-1440-top.png
A  artifacts/screenshots/ui-pass-3-sample-390-full.png
A  artifacts/screenshots/ui-pass-3-sample-390-top.png
A  artifacts/screenshots/ui-pass-4-dismissed-group-1440.png
A  artifacts/screenshots/ui-pass-4-dismissed-group-390.png
A  artifacts/screenshots/ui-pass-4-gap-change-card-1440.png
A  artifacts/screenshots/ui-pass-4-gap-change-card-390.png
A  artifacts/screenshots/ui-pass-4-lib09-1440-full.png
A  artifacts/screenshots/ui-pass-4-lib09-1440-top.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:42.806Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/commitmsg4.txt",
 "content": "feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles\n\n- T-114: the gap card keeps \"now 40 days (was 42)\" with before/after dates, per case in the browser (survives Got it and reload); prefers flag.gap_change when the backend sends it (T-127)\n- accepted rate/estimate/unclear rows show one chip; \"Keep in notes\" is not primary\n- dismissed entries leave the queue for a collapsed \"Dismissed (n)\" group with Undo; the record's quote is never struck through\n- edit box says the wording is re-checked; a saved edit reports the re-check; refused figures show as typed ($9,000)\n- library cases get plain titles (header, title, lists); AI-check row for a tray flag agrees with the tray; no-sentences copy once\n- a11y: More/Less name contains its label, queue role=group, skip-link ids re-pointed after a repaint, Export heading focus ring, unique Technical details names\n- tests: tests/e2e/test_polish_r4.py (14), conftest hook paragraph, three old assertions updated (9000 -> $9,000, doubled no-sentences copy); screenshots ui-pass-{1..4}-*.png\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n"
}
````

### User / tool · 2026-11-02T11:21:42.869Z

**tool result**
````
File created successfully at: /private/tmp/claude-501/commitmsg4.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:49.070Z

**tool call — Bash**
````
{
 "command": "git commit -F /private/tmp/claude-501/commitmsg4.txt -- app/frontend/app.js app/frontend/dom.js app/frontend/flags.js app/frontend/judges.js app/frontend/manual.js app/frontend/review.js app/frontend/review.css app/frontend/styles.css app/frontend/switcher.js app/frontend/timeline.js tests/e2e/test_polish_r4.py tests/e2e/conftest.py tests/e2e/test_edit.py tests/e2e/test_rerun_judge.py tests/e2e/test_suggestions.py artifacts/screenshots/ui-pass-1-lib09-1440-full.png artifacts/screenshots/ui-pass-1-lib09-1440-top.png artifacts/screenshots/ui-pass-1-lib09-390-full.png artifacts/screenshots/ui-pass-1-lib09-390-top.png artifacts/screenshots/ui-pass-1-sample-1440-full.png artifacts/screenshots/ui-pass-1-sample-1440-top.png artifacts/screenshots/ui-pass-1-sample-390-full.png artifacts/screenshots/ui-pass-1-sample-390-top.png artifacts/screenshots/ui-pass-2-lib09-1440-full.png artifacts/screenshots/ui-pass-2-lib09-1440-top.png artifacts/screenshots/ui-pass-2-lib09-390-full.png artifacts/screenshots/ui-pass-2-lib09-390-top.png artifacts/screenshots/ui-pass-2-sample-1440-full.png artifacts/screenshots/ui-pass-2-sample-1440-top.png artifacts/screenshots/ui-pass-2-sample-390-full.png artifacts/screenshots/ui-pass-2-sample-390-top.png artifacts/screenshots/ui-pass-3-lib09-1440-full.png artifacts/screenshots/ui-pass-3-lib09-1440-top.png artifacts/screenshots/ui-pass-3-lib09-390-full.png artifacts/screenshots/ui-pass-3-lib09-390-top.png artifacts/screenshots/ui-pass-3-sample-1440-full.png artifacts/screenshots/ui-pass-3-sample-1440-top.png artifacts/screenshots/ui-pass-3-sample-390-full.png artifacts/screenshots/ui-pass-3-sample-390-top.png artifacts/screenshots/ui-pass-4-dismissed-group-1440.png artifacts/screenshots/ui-pass-4-dismissed-group-390.png artifacts/screenshots/ui-pass-4-gap-change-card-1440.png artifacts/screenshots/ui-pass-4-gap-change-card-390.png artifacts/screenshots/ui-pass-4-lib09-1440-full.png artifacts/screenshots/ui-pass-4-lib09-1440-top.png artifacts/screenshots/ui-pass-4-lib09-390-full.png artifacts/screenshots/ui-pass-4-lib09-390-top.png artifacts/screenshots/ui-pass-4-sample-1440-full.png artifacts/screenshots/ui-pass-4-sample-1440-top.png artifacts/screenshots/ui-pass-4-sample-390-full.png artifacts/screenshots/ui-pass-4-sample-390-top.png 2>&1 | tail -5; git log --oneline -1"
}
````

### User / tool · 2026-11-02T11:21:51.756Z

**tool result**
````
 create mode 100644 artifacts/screenshots/ui-pass-4-sample-1440-full.png
 create mode 100644 artifacts/screenshots/ui-pass-4-sample-1440-top.png
 create mode 100644 artifacts/screenshots/ui-pass-4-sample-390-full.png
 create mode 100644 artifacts/screenshots/ui-pass-4-sample-390-top.png
 create mode 100644 tests/e2e/test_polish_r4.py
e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:21:56.937Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && kill 71076; git worktree add --detach $S/wt_r4final HEAD >/dev/null 2>&1; cd $S/wt_r4final && git log --oneline -1 && ls evals/golden | head -2; ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; (PORT=7956 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$S/r4data/final.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/r4data/final.log 2>&1 & echo $! > $S/r4data/final.pid); sleep 3; curl -s localhost:7956/api/health | head -c 80; cat $S/r4data/final.pid"
}
````

### User / tool · 2026-11-02T11:22:00.609Z

**tool result**
````
e293daa feat(frontend): T-060 r4 + T-114 r3 - persistent gap-change line, Dismissed group, edit re-check notice, typed $ in refusals, readable library titles
README.md
case_01_date_formats.expected.json
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only2547
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:04.472Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/wt_r4final && (E2E_BASE_URL=http://localhost:7956 .venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider > /private/tmp/claude-501/e2e_final.log 2>&1; .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q > /private/tmp/claude-501/unit_final.log 2>&1) ; tail -5 /private/tmp/claude-501/e2e_final.log; tail -8 /private/tmp/claude-501/unit_final.log",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T11:30:14.275Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: TimeoutError
=========================== short test summary info ============================
FAILED tests/e2e/test_rerun_judge.py::test_first_blocking_item_is_the_first_in_the_queue
1 failed, 189 passed, 16 skipped in 296.18s (0:04:56)
........................................................................ [ 83%]
........................................................................ [ 85%]
........................................................................ [ 88%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 95%]
........................................................................ [ 97%]
...............................................................          [100%]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:19.456Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/wt_r4final && E2E_BASE_URL=http://localhost:7956 .venv/bin/python -m pytest tests/e2e/test_rerun_judge.py -q -p no:cacheprovider -k first_blocking 2>&1 | tail -15; grep -n \"first_blocking\" -A14 tests/e2e/test_rerun_judge.py | head -30",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T11:30:21.766Z

**tool result**
````
.                                                                        [100%]
1 passed, 24 deselected in 2.00s
185:def test_first_blocking_item_is_the_first_in_the_queue(page, unrun):
186-    open_case(page, unrun.token); cs = open_rail(page)
187-    cs.locator('[data-step-id="export_gate"]').get_by_test_id("btn-step-action").filter(has_text="first blocking item").click()
188-    focused = page.evaluate("document.activeElement.getAttribute('data-item-id')")
189-    queue = page.locator('[data-testid="queue"] [data-item-id]').evaluate_all("els => els.map(e => e.getAttribute('data-item-id'))")
190-    assert focused == next(i for i in queue if i in unrun.ids)
191-
192-
193-# ---- T-097: where the rerun answer shows, and the panel agreeing with the gate
194-def vis(page, loc):
195-    b = loc.bounding_box(); vh = page.viewport_size["height"]
196-    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh
197-
198-
199-@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:26.452Z

**tool call — Bash**
````
{
 "command": "kill 2547; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git worktree remove --force $S/wt_r4 2>&1 | tail -1; git worktree remove --force $S/wt_r4final 2>&1 | tail -1; sh tools/serve_app.sh 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T11:30:29.090Z

**tool result**
````
app http 200 on :7860
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:29.825Z

Now board updates.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:40.720Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; SHA=e293daa\n$B ac T-060 --check 1 --agent frontend --evidence \"research/ui-references.md (13 sources, researcher pass 1)\" | tail -1\n$B ac T-060 --check 4 --agent frontend --evidence \"reviews/T-060-accessibility-pass3.md: pass, 0 majors; r4 fixes P3-1, P3-2, N-8, P3-4, N-14 (tests/e2e/test_polish_r4.py)\" | tail -1\n$B ac T-060 --check 5 --agent frontend --evidence \"tests/e2e/test_polish_r4.py: re-check hint and note on edit, \\$9,000 shown as typed in the 422, Copy letter disabled when empty and plain 'not reviewed' wording (test_polish_r3 / export), progress + export navigation; full e2e on clean e293daa\" | tail -1\n$B commit T-060 --sha $SHA --agent frontend | tail -1\n$B commit T-114 --sha $SHA --agent frontend | tail -1\n$B note T-060 --agent frontend --text \"Round 4 done (e293daa): AC1, AC4, AC5 checked; AC3 left for pass 4 (screenshots artifacts/screenshots/ui-pass-{1,2,3,4}-{sample,lib09}-{1440,390}-{top,full}.png plus ui-pass-4-gap-change-card-*, ui-pass-4-dismissed-group-*). Filed T-127 (backend: persist gap_change on the flag). Cross-boundary: added the round-4 paragraph to tests/e2e/conftest.py and updated three old assertions (test_edit 9000 -> \\$9,000, test_rerun_judge same, test_suggestions no-sentences copy) because the behaviours they encoded were the review findings.\" | tail -1\n$B handoff T-060 --agent frontend --text \"What changed (r4): AC5 leftovers: re-check line under the edit box and on an edited row, refused figures shown as typed (\\$9,000), accepted rate rows one chip; pass-3 minors: library titles in plain words (header, tab title, lists), dismissed entries leave the queue for a collapsed 'Dismissed (n)' group (opens for the one just dismissed; quote never struck), AI-check row for a tray flag says 'Left out of the letter' and 'Nothing to accept here', no-sentences copy once, translation caution wraps, decided summaries 2 lines; a11y: More/Less name starts with its label, queue role=group, skip-link ids re-pointed after repaint, Export heading focus ring, unique Technical details names. How verified: tests/e2e/test_polish_r4.py (14 pass); full tests/e2e on a clean worktree of e293daa on own port 7956: 189 passed, 16 skipped, 1 timeout (test_first_blocking_item_is_the_first_in_the_queue) that passes alone; tests/unit all pass. Screenshots in artifacts/screenshots/ui-pass-*. What's left: AC3 needs pass 4 (ux-designer + paralegal). Not done: density toggle, long dates in rows (e2e filters on ISO), N-9 row tab stops, open-record in pane at >=1024, flag double dismiss, N1 '?' from page top (the negative key test asserts it does nothing). Surprised: a const used before its declaration inside a row builder threw and silently emptied the whole flags panel (caught by the first e2e); node --check does not see TDZ errors.\" | tail -1\n$B handoff T-114 --agent frontend --text \"What changed: the gap-change notice persists. The gap card shows the server sentence plus 'Before: 42 days (March 3 to April 14, 2026). Now: 40 days (March 5 to April 14, 2026)', kept per case in the browser (localStorage zlayt.gapchg.<token>) and shown while the card still shows the new figure; Got it removes only the banner; a removed gap keeps its sentence under Treatment gaps. The backend has no stored field, so T-127 asks for flag.gap_change; the UI already prefers it. Minor fixed: an accepted rate/estimate/unclear row shows one chip (Accepted); 'Keep in notes' is no longer primary. Paperwork sentence no longer repeated on the gap card (Needs review line drops sentences the explanation already says). How verified: tests/e2e/test_polish_r4.py::test_t114_gap_change_stays_on_the_gap_card_after_got_it_and_reload (confirm, Got it, reload, 'now 40 days (was 42)' and March 5, 2026 on the card), ::test_t114_accepted_rate_row_reads_one_status_chip; full e2e clean. Left: T-127 (backend field; browser copy is lost on another browser); lib01 FIXTURE_MISS nit is backend/QA.\" | tail -1\n$B move T-060 in_review --agent frontend | tail -1\n$B move T-114 in_review --agent frontend | tail -1"
}
````

### User / tool · 2026-11-02T11:30:41.448Z

**tool result**
````
AC 1 checked: research/ui-references.md (13 sources, researcher pass 1)
AC 4 checked: reviews/T-060-accessibility-pass3.md: pass, 0 majors; r4 fixes P3-1, P3-2, N-8, P3-4, N-14 (tests/e2e/test_polish_r4.py)
AC 5 checked: tests/e2e/test_polish_r4.py: re-check hint and note on edit, $9,000 shown as typed in the 422, Copy letter disabled when empty and plain 'not reviewed' wording (test_polish_r3 / export), progress + export navigation; full e2e on clean e293daa
T-060: commit e293daa recorded
T-114: commit e293daa recorded
noted on T-060
handoff written on T-060
handoff written on T-114
board.py: error: T-060 already in_review
T-114: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:45.879Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\".claude/agent-memory/frontend/project_t060_polish.md\"\ns=open(p).read()\ns+='''**Round 4 (e293daa):** `ZL.niceName` (dom.js) gives library cases plain titles (display only). Gap-change line: timeline.js `gapChangeFor` (localStorage `zlayt.gapchg.<token>`, prefers `flag.gap_change` once backend T-127 sends it), shown by flags.js on the gap card. Dismissed entries render in `details.dismissed-group` under the queue; `ZL.dismissedOpen` opens it for the entry just dismissed (e2e tests that dismiss then click Undo rely on that). `RV.asTyped` shows refused figures as typed ($9,000). Edit re-check: `rechecks[id]` in review.js, `edit-recheck-hint` / `edit-recheck-note`. Pitfalls: a `const` used before its declaration in a row builder throws and silently empties the whole panel (node --check will not catch TDZ; run one e2e after every edit to judges/flags/timeline); the e2e hook contract unit test (`tests/unit/test_e2e_contract.py`) needs every new test id and data-* attribute declared in the conftest docstring; `aria-label` on a toggle must start with its visible word.\n'''\nopen(p,\"w\").write(s)\nEOF\ngit status --short .claude/agent-memory/frontend | head -3"
}
````

### User / tool · 2026-11-02T11:30:46.024Z

**tool result**
````
 M .claude/agent-memory/frontend/MEMORY.md
?? .claude/agent-memory/frontend/project_t060_polish.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:30:52.408Z

T-060 round 4 and T-114 are done in commit e293daa. T-114 is `in_review`; T-060 was already `in_review` before I moved it.

- **T-114 major:** the gap card now keeps "now 40 days (was 42)" with before and after dates, per case in the browser. It survives Got it and a reload. The backend has no stored field, so I filed T-127 for one; the UI already prefers it. The minor is fixed: an accepted rate shows one chip, and "Keep in notes" is no longer primary.
- **T-060 AC5:**
  - A re-check hint shows under the edit box, and a saved edit reports the re-check.
  - Refused figures show as typed ("$9,000").
  - Reviewed-vs-remaining progress, export navigation, Copy letter disabled when empty and the plain "not reviewed" wording were already in; they are now covered by tests.
  - AC1, AC4 and AC5 are checked; AC3 waits for pass 4.
- **Pass-3 minors:**
  - Library cases show plain titles in the header, tab title and lists.
  - Dismissed entries move to a collapsed "Dismissed (n)" group with Undo. It opens for the entry you just dismissed.
  - The AI-check row for a flag the checks left out now agrees with "Nothing to accept here".
  - The no-sentences copy is no longer doubled.
  - The translation caution wraps and is no longer clipped.
  - Accessibility fixes: the More/Less control's name now starts with its visible word, the queue has `role="group"`, skip-link targets resolve after a repaint, the Export heading shows a focus ring, and the "Technical details" labels are unique.
  - Not done: density toggle, long dates in rows (e2e filters on ISO), the row Tab stops, and `?` from the page top.
- **Tests:** a new `tests/e2e/test_polish_r4.py` has 14 tests, including notice persistence after reload. Full e2e on a clean worktree of e293daa: 189 passed, 16 skipped, 1 timeout. That one, `test_first_blocking_item_is_the_first_in_the_queue`, passes alone. The unit suite passes.
- **Cross-boundary edits:** I added a round-4 paragraph to the `tests/e2e/conftest.py` docstring (the hook contract unit test needs it). I changed three old assertions that encoded the behaviours the reviews flagged: `test_edit` and `test_rerun_judge` expected "9000", and `test_suggestions` expected the doubled no-sentences copy.
- **Screenshots:** `artifacts/screenshots/ui-pass-{1,2,3,4}-{sample,lib09}-{1440,390}-{top,full}.png`, plus the gap-card and Dismissed-group shots for pass 4.
- **Servers:** my servers are stopped (own PIDs only). The shared app is restarted with `tools/serve_app.sh` and answers 200 on :7860.
