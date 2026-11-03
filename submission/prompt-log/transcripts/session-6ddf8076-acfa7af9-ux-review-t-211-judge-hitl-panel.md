# Subagent: UX review: T-211 judge/HITL panel (UX review: T-211 judge/HITL panel)

Source: `agent-acfa7af956f46cf9f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T13:13:17.081Z

Review T-211 in /Users/arsis/zlayt-pm-project as the UX designer, starting from a fresh context. The commits are 82217e5 and 4e4ff36; read D-074 in memory/ORCHESTRATOR_DECISIONS.md and the handoff.

Chris hands Zlayt only the demo and the repo, so a first-time viewer must see and understand that each answer passes a code check, then an independent second AI check (the LLM judge), then the human decides.

Extract a fresh `git archive HEAD` and run demo mode on your own port; stop your PID afterward. At 1440x900 and 390x844, judge:
- the "How this was checked" panel on Step 2 and Step 3 items. It folds to chips when space is short; is it still discoverable?
- the "How each answer is checked" page linked from the header;
- clarity of the explanation, honesty per D-065 for prepared answers, and no regressions to the guided flow.

Put screenshots in artifacts/review-evidence/T-211-ux/. Write reviews/T-211-ux-designer.md in D.2 format, applying the verdict rule. Reply in 2 lines.

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:18.583Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/ux-designer.md"
}
````

### User / tool · 2026-11-03T13:13:18.595Z

**tool result**
````
1	# Persona dossier — ux-designer-reviewer
2	
3	## 1. Identity
4	**Priya Raman (fictional), Principal UX Designer, enterprise workflow software — 12 years, last 4 on human-in-the-loop AI review tools (document review, claims triage).**
5	She has watched expert users abandon AI tools that hid where an answer came from, and others that made correcting the AI slower than doing the work by hand. Her incentive: the reviewer must finish faster *and* trust the result, so she grades the cost of verifying and correcting, not the beauty of the first screen.
6	
7	## 2. Day-to-day context
8	- Tools: Figma, Playwright scripts for walkthroughs, screen recordings, heuristic-evaluation sheets.
9	- Pressures: expert users with high volume who live on the keyboard; buyers who judge in a 3-minute demo.
10	- A bad day: usability sessions where every participant re-opens the source PDF because the tool's excerpt is hidden two clicks away.
11	
12	## 3. Goals and success criteria for this artifact
13	- The paralegal can see, for any entry, flag, or dollar amount, the exact source excerpt without leaving the screen.
14	- State is always visible: what is verified, what needs review and why, what has been accepted/edited/dismissed, how many remain.
15	- Correction is cheap: accept/edit/dismiss in one action each, keyboard-reachable, undoable.
16	- Errors, empty states, and model failure are designed, not default stack traces.
17	- The export is usable as pasted text in a demand letter.
18	
19	## 4. Review checklist
20	1. Every timeline entry shows date, provider, one-line summary, and the verbatim excerpt (or a one-click/one-key reveal that stays on the same screen).
21	2. `needs_review` items are visually distinct from `verified` and sorted first; the one-sentence reason is visible without hovering.
22	3. `rejected` (could-not-verify) items appear in a visible tray, not silently dropped.
23	4. Flags are grouped by type (gap, conflict, prior condition, causation language) and each shows the evidence excerpt(s); a conflict shows both excerpts side by side.
24	5. The charges table separates totaled charges from "unclear — not totaled" items; the $185/visit rate sits in the unclear group with its reason.
25	6. A progress indicator shows reviewed vs remaining (e.g., "7 of 12 reviewed") at all times during review.
26	7. Accept, edit, dismiss are each one click and have keyboard equivalents; the shortcuts are discoverable on screen.
27	8. Edit happens in place, preserves the original text for comparison, and marks the item as edited.
28	9. Any accept/dismiss can be undone without reloading.
29	10. Export is disabled or clearly warns while items remain unreviewed, and states exactly what will be included.
30	11. The exported text pastes cleanly into a word processor: one line per entry, no HTML artifacts, no UI labels, citations present.
31	12. Empty input, oversized input, and model/LLM failure each show a plain-language message near the input, preserve what the user pasted, and suggest the next step.
32	13. Long-running processing shows status (step names or progress), not a frozen screen.
33	14. The "synthetic data only" banner is persistent and does not obscure content or focused elements.
34	15. The AI's role is explained where it acts (e.g., "Summary drafted by AI, checked against the excerpt") — not a generic disclaimer.
35	16. Confidence is shown only as states that change a decision (verified / needs review / rejected), not as decorative percentages.
36	17. The layout works at 390 px width: no horizontal scroll for the review list; actions remain reachable.
37	18. Terminology matches the user's world (chronology, provider, excerpt, billed charges), not the developer's (chunk, span, token).
38	19. On first load of the sample-case results, the first focusable item in the results region is a `needs_review` item, and the 73-day gap flag is visible without scrolling at 1440x900.
39	20. Nothing in the interface claims more than the record supports (e.g., no "injury caused by accident" headers).
40	
41	## 5. Red flags / dealbreakers
42	Each item here is a **blocker** (rate it so; never major or minor).
43	- The source excerpt is not visible or reachable for an item (breaks "reviews rather than trusts").
44	- Export includes items the user did not accept, or there is no way to see what will be exported.
45	- An error state loses the user's pasted records.
46	- Unverified model output is styled identically to verified output.
47	
48	## 6. Vocabulary
49	visibility of system status, recognition over recall, error prevention, user control and freedom, accelerators, progressive disclosure, empty state, error state, inline validation, provenance / citation affordance, calibrated trust, efficient correction, efficient dismissal, scope of AI explanation, information scent, hierarchy, affordance.
50	
51	## 7. How I review
52	1. Read the brief; open the app at the given URL with Playwright (desktop 1440x900 and mobile 390x844).
53	2. Screenshot every state: empty, input pasted, processing, results, an item expanded, edit mode, flags panel, charges table, export preview, error (submit empty input; submit 500 KB of text), and model-failure if the brief provides a way to force it.
54	3. Complete the sample case end to end using only the keyboard first, then the mouse. Time both.
55	4. Try to export with items unreviewed; try to undo an accept; edit an entry and check the export shows the edit.
56	5. Paste the export into a plain text file and inspect it.
57	6. Score each of the four criteria (design quality, originality, craft, functionality) 1-5; any score ≤ 2 must have a matching major or blocker finding.
58	7. File findings with screenshot paths under `artifacts/review-evidence/`.
59	
60	Hard thresholds: functionality ≤ 2 → at least one blocker; verifying any single item takes more than 2 actions → major.
61	
62	## 8. Calibration
63	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
64	- **blocker — Excerpt hidden from conflict flag.** Evidence: screenshot shows "Conflicting accident dates" with no excerpts. Fix: show both quotes ("...2026-01-09..." EMS, "Date of accident per intake form: 2026-01-19") with record labels. Test: E2E asserts both excerpts visible in the flag card.
65	- **blocker — Error loses pasted input.** Evidence: submitting 600 KB shows "Error 413" and clears the textarea. Fix: inline message "This is over the 200 KB limit. Split the records and try again." with text preserved.
66	- **minor — No progress count.** Evidence: review screen with 12 entries has no remaining count. Fix: sticky "5 of 12 reviewed · 3 need review".
67	
68	## 9. Sources
69	- https://www.nngroup.com/articles/ten-usability-heuristics/ — NN/g: Nielsen's 10 heuristics (system status, user control, error prevention, recognition over recall, flexibility/accelerators, error recovery).
70	- https://www.nngroup.com/articles/error-message-guidelines/ — NN/g (2023): put errors near their source, don't rely on color alone, explain plainly with a fix, preserve user input.
71	- https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ — Amershi et al., CHI 2019: 18 validated guidelines across initial use, during interaction, when wrong, over time.
72	- https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ — Microsoft HAX Toolkit: the same 18 guidelines grouped by stage, including when the AI system is wrong.
73	- https://pair.withgoogle.com/chapter/explainability-trust/ — Google PAIR: calibrate trust, explain data sources, scale detail to stakes, show confidence only when it improves decisions.
74	- Assumption: the "two actions to verify" threshold and the 390 px width are this project's choices, not from a source.
75	
76	## 10. Limits
77	Do not judge clinical correctness, adjuster tactics, legal ethics, or code quality. Accessibility conformance (WCAG) belongs to accessibility-reviewer — note obvious issues but defer severity to them.
78	
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:19.335Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && python3 tools/board.py show T-211",
 "description": "Show recent commits and the T-211 card"
}
````

### User / tool · 2026-11-03T13:13:19.488Z

**tool result**
````
cda2856 feat(qa): T-184 demo assets: 72 final screenshots (1440x900, 390x844) with captions, 167 s Playwright walkthrough video, timed narration; scripts in tests/demo_assets (captured at 4e4ff36)
4e4ff36 chore(frontend): T-211 refresh the ladder picture from submission/validation-ladder.svg
82217e5 feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label
3784bfb docs(writer): T-188 submission checklist, email draft, NEEDS_CHRIS by priority, product note and Part 2 refreshed (T-181, T-179, D-071 to D-073), PDFs
6be191f docs(release): T-212 README as front door: run, 3-minute walk, how the AI is checked, what's where, limits
9655f1d test(backend): T-202 r6 pin the 60-character UB-04 label window in production and the check; drop the unreachable statement-date branches of the check
756546b test(backend): T-202 r6 pin pipe cells, no-date bound, unlocated figure and visit ranges; heading cells gate the From/To pairing alone
3654cf9 test(backend): T-202 r6 sample letter golden chain: spec REQUIREMENTS block 1+2 and the hand-built export case carry the MRI blank and the new notes section
---
id: "T-211"
title: "Guided UI exposes and explains the validation ladder: per-item code check, second AI check (judge) verdict + reason, your decision; a 'How each answer is checked' page from every screen"
milestone: "M4"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T04:33:55Z"
updated_at: "2026-11-03T13:13:03Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T04:34:14Z"
rounds: 0
commits: ["82217e5", "4e4ff36"]
reviews: []
ac:
  - {"n": 1, "text": "on every Step 2/3 item a visible 'How this was checked' section shows the code check result, the judge verdict and its reason (or 'prepared by our team' per D-065 plus the judge result), and the user's decision; a How-it-works page (header link) explains code check -> independent AI judge (different prompt/model) -> you decide, with the validation-ladder graphic; plain words; e2e + 390px; no console errors", "done": true, "evidence": "tests/e2e/guided/test_t211.py 17 pass (1440 and 390, no console errors); full tests/e2e from git archive 6e16e9a, E2E_REQUIRE_DB=1: 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T04:34:14Z frontend: claimed
- 2026-11-03T04:46:55Z frontend: Built: how-checked panel (review.js, trace-fed: code check / second AI check verdict+reason / you; prepared lead per D-065), /how-it-works page + header link on every screen, ladder SVG copy, Step 3 date_label. test_t211.py 17 pass on live server; full e2e from archive running.
- 2026-11-03T05:05:14Z frontend: AC 1 checked: tests/e2e/guided/test_t211.py 17 pass (1440 and 390, no console errors); full tests/e2e from git archive 6e16e9a, E2E_REQUIRE_DB=1: 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone)
- 2026-11-03T05:06:01Z frontend: moved in_progress -> in_review
- 2026-11-03T13:13:03Z orchestrator: review dispatched: ux-designer-reviewer

## Handoff
What changed: every Step 2/3 item has a 'How this was checked' panel (review.js drawHow, fed by GET /items/<id>/trace): Code check (what code verified or what failed, plus 'All N checks'), Second AI check (Agrees / Disputes / Could not check / Not needed + the server's one-line reason and its model; prepared items lead with 'Prepared by our team; the second AI check then checked it against the quote.' per D-065), You (decision or 'Waiting for you'). New page /how-it-works (how.js, how.css, about 150 words, ladder SVG copied from submission/, code vs AI lists, repo doc names) linked from the header on every screen. Step 3 reads service_date.date_label. · Verified: tests/e2e/guided/test_t211.py 17 pass at 1440 and 390 with no console errors; full tests/e2e from git archive (E2E_REQUIRE_DB=1): 598 passed, 1 skipped, 2 failed (test_charge_confirm duplicate-sentence fails at HEAD too, D-073 wording; test_held_quote_gate passes alone). · Left: panel sits under the record on desktop (open when window height >= 840 and no highlighted word would be pushed out, else folds to three chips, one click opens); on a phone it is at the end of the line card, closed with chips. The SVG is a snapshot of submission/: re-copy if the writer changes it. · Surprised: the multi-record warning test forces every highlight into the record window, so the open panel cannot always fit at 1440x900; history.length is 2 on a fresh tab so Back uses G.navigated.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:20.418Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-074\" -A 30 memory/ORCHESTRATOR_DECISIONS.md | head -60; grep -n \"D-065\" -A 15 memory/ORCHESTRATOR_DECISIONS.md | head -25",
 "description": "Read D-074 and D-065 decisions"
}
````

### User / tool · 2026-11-03T13:13:20.510Z

**tool result**
````
102:## D-074 — The deliverable is the demo plus the repo (Chris, 2026-11-03)
103-Chris will hand Zlayt only the running demo and the repo. So: (1) README.md is the front door: what it is, a two-command setup that works from a fresh clone, a 3-minute guided walk of the demo, and where the LLM-as-judge and the human-in-the-loop live (code, prompts, evals, decisions), with the validation-ladder diagram; (2) the app itself exposes and explains the ladder: each item shows its code check, the second AI check (judge) verdict and reason, and the human decision, and a plain "How each answer is checked" page is reachable from every screen; (3) the submission packet (checklist, product note, Part 2, prompt log) stays in submission/ and is linked from the README; (4) after T-184/T-188 an independent reviewer double-checks the assets and the packet.
104-- D-073 fallback applied (T-202 r6 paralegal fail: a visit note lends its date to another visit's charge; a UB-04 period overrides a line's own date). Per the pre-declared rule the MVP letter prints the fillable blank "date of service [__________] (record|statement dated X)" on every charge line; no service date is extracted for the letter. Step 3 shows the same. SCOPE_CUTS 28 covers date extraction.
73:| D-065 | Honest demo provenance (amends D-029; GATE-M3 PM blocker). Curated fixture answers are never presented as model output. Badge: "Demo: sample answers prepared by our team"; tooltip: "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote." (amended T-177 r2: the eval report stores hashes, not answers) A curated item carries a "Prepared answer" tag, never "AI draft"; its trace step reads "Prepared answer (hand-checked by the team for the demo), standing in for the AI draft"; its audit row stores the model as "hand-checked (qa)". Recorded live answers keep their AI labels and model ids. Plain wording (D-063 polish) must stay truthful: removing jargon never removes provenance. | T-167's jargon cleanup dropped the 'curated' disclosure, so prepared answers were labelled as the model's; that is an over-claim. | GATE-M3 product-manager |
74-| D-066 | A summary the second check disputed is not one click from the letter (GATE-M3 PM major). Accepting an item whose judge verdict is disagree/unsupported/partially (or that carries JUDGE_DISAGREES) requires the same explicit "I compared it with the quote" confirm as an unconfirmed edit; the confirm is stored on the review event. Batch accept never includes such items. | The human is the last rung; a disputed summary must get a deliberate human comparison, not a reflex click. | GATE-M3 product-manager |
75-| D-067 | The drafted treatment paragraph is cut from the MVP UI (GATE-M3 PM + paralegal majors). The backend route stays, but the page does not offer it and it never reaches the letter, until it has its own eval and each sentence carries its verbatim quote and the [Ex. __ / Bates __] placeholder (D-002). Recorded as a scope cut. | It went live without an eval and its letter lines lack quotes, which D-002 rules out. | GATE-M3 product-manager, paralegal |
76-| D-068 | Guided UI redesign (Chris, 2026-11-02: "VERY hard to use… so simple someone's grandma can use it"). The app becomes a fixed four-step guide per case: 1 Add records, 2 Check the timeline, 3 Check the bills, 4 Get your letter. Home is "Your cases": one card per case with its step progress and one Continue button. Inside a case the step bar never moves; each step is its own page; review is one item at a time (the highlighted quote beside the AI's line, a plain question, two big answers, Back, "3 of 9"). Flags and could-not-verify items join the same queue as plain questions. Step 4 shows the letter, Copy and Download, or "N items still need a decision — go back". No collapsing groups, no jargon, nothing that reflows on click. The backend, API and every ladder rule are unchanged; the old screen moves to /classic so its e2e suite keeps guarding behaviour while the guided UI gets its own suite. Supersedes T-179's UI scope. | The user's verdict on the current UI; a guide with fixed steps is the simplest model for a non-expert. | Chris chat |
77-
78-## D-069 — T-177 after 3 rounds: replace the swap table with a property test (§7.4)
79:Round 3 fixed the shipped sample but the failure paths (malformed or missing curated answer) still leak model names and "AI" wording through a word-swap table. A fourth round is authorised with a structural change instead of more swaps: (1) when an item or case is prepared, every user-facing string is built from a prepared-specific template keyed by the provenance field, never by rewriting AI text; (2) a malformed curated answer is treated as missing (never falls back to a model label); (3) a property test runs the demo over fault-injected curated sets (valid, malformed, missing, empty) for the sample and two library cases and fails if any API response for a prepared item or case matches /\bAI\b|claude|sonnet|haiku|opus|model/i outside the D-065 tooltip sentence. If round 4 fails, the demo hides failed prepared items behind one plain sentence ("This answer is not available in the demo") and the residual goes to SCOPE_CUTS.
80-
81-## D-070 — One redaction rule set, no private literal in tracked code, applied to every published file
82-T-187 r3: private values survive as quoted fragments joined with '+' (in transcripts and in the redaction source itself), and the snapshot applied only some rules outside the prompt log. Binding: (1) every private term (work email, third-party and personal names, job-application path pieces, tailnet host) lives only in the gitignored deploy/.private_patterns; tracked code holds rule logic, never the values; (2) the snapshot applies the full rule set (prompt-log rules + private terms + home paths + outside project name) to every text file it publishes; (3) the final scan matches on a normalized view of each file (strip quotes, '+', whitespace, backslashes, case) so split or escaped forms fail the build. Same switch semantics for Chris's T-193 answer.
83-
84-## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
85-T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
86-
87-## D-071 amendment — when the service date is not certain, print none and ask the human
88-T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
89-
90-## D-072 — The prompt log is built and privacy-reviewed once, last
91-Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
92-- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93-- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
94-- D-071 amendment 2 (§7.4 after T-202 r3; round 4 authorised, final): (a) a record's own date is a service date only for a positively identified encounter record (visit/ER/clinic/therapy/ambulance-run note); bills, receipts, superbills, charge summaries and unknown types never lend their header date; (b) in prose, only "date of service", "dates of service", "DOS" and "service date" are labels ("visit date", "seen on" and bare "date" are not; they also name next or prior visits); (c) letter_check keeps an independent scanner but reads the same declared encounter-type table (one data file), and anchors the blank; (d) if round 4 fails, the fallback is the most conservative rule: every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:24.107Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer && cat feedback_pin_review_commit.md project_t181_guided_build.md project_t203_375_hint.md reference_sample_load_stall.md feedback_reviewer_bash_parse_guard.md project_t180_guided_mockup.md",
 "description": "Read relevant memory files"
}
````

### User / tool · 2026-11-03T13:13:24.194Z

**tool result**
````
---
name: feedback_pin_review_commit
description: Review the app at the card's commit via git archive, never the repo-root working tree (it carries uncommitted changes and HEAD moves mid-review)
metadata:
  type: feedback
---

Serve the app from `git archive <card-commit> | tar -x -C <scratchpad>/<name>` and run `python -m app.main` from that copy, not from the repo root.

**Why:** On the T-046 review the repo-root tree had 269 uncommitted changes (`git status --short`). A server started there gave a judge-panel test failure that did not reproduce at the card commit 5616dc3. HEAD also moved twice during the review (5616dc3 to e92b6ed to e2b4e3f). Results from the dirty tree were discarded.

T-097 r2 (2026-11-02): the card's latest commit (21b6665) predated the backend tickets the brief depended on (T-100 24c18a7 came after it). When the brief asks for HEAD, archive HEAD, record that SHA, and check ancestry with `git merge-base --is-ancestor` for each ticket commit. HEAD moved again during that review (32f6c9d to f345bc8); diff the two before saying the pinned result still holds.

T-181 r2 (2026-11-02): I extracted the archive into a REUSED directory. A stale narrative.js left there from an older tree gave a false e2e failure, which I filed as a finding and retracted in r3. Always extract into a brand-new empty directory, named with the SHA.

**How to apply:** Before any "at HEAD" run, record `git rev-parse --short HEAD` and `git status --short | wc -l`. Export the card's commit to scratch and start the server from that copy (PORT, HOST=127.0.0.1, separate ZLAYT_DB). Quote the commit in the review scope. Stop the server when done and confirm the port returns 000.
---
name: project-t181-guided-build
description: T-181 guided UI: r1 26287b9 (4 majors), r2 9ab8cae (2 phone majors), r3 2c19817 pass (0 majors; 375x667 tick box under the bar kept as minor, refused-edit editor top under header at 390)
metadata:
  type: project
---

r1 (reviews/T-181-ux-designer.md, 26287b9): changes, 4 majors (M1 Step 3 done overflow at 390, M2 disputed line under the header at 390, M3 garbled qualifier refusal, M4 step toggle navigates).

r2 (reviews/T-181-ux-designer-r2.md, 9ab8cae): changes, 2 majors. The record window hid the highlight when the tick box showed, and the refused-edit message sat behind the action bar.

r3 (reviews/T-181-ux-designer-r3.md, 2c19817, 2026-11-02): **pass**.
- Both majors are fixed at 390x844.
- At 375x667 the mark is fixed, but the line runs under the bar and the box is off-screen, with no reason given for the greyed Yes. Kept as minor (F1), because the project's target is 390 px. A question to Chris asks whether the iPhone SE is in the grandma bar.
- New minor: at 390 after a refusal, only the last line of the editor shows (editor y 419-547 under header bottom 512).
- 139 guided e2e passed on a fresh archive.
- The r2 "133/134" minor was MY false finding: a stale narrative.js in a reused archive dir. Retracted.

Scripts: T-181-ux-r3-lib.py (OUT T-181-ux-r3/, base :7906), -majors.py (creates lib10 on :7907 and measures both majors at 3 phone sizes), -se.py, -walk/-keyboard/-download/-edit/-explore.py.

**Why:** Chris's bar is "grandma-simple". The phone was the last gap.

**How to apply:** If T-181 reopens, re-run -majors.py and -se.py against a NEW empty archive dir. Write r2 acceptance tests only for sizes I'm prepared to grade at major. See [[feedback-pin-review-commit]], [[project-t180-guided-mockup]].
---
name: project-t203-375-hint
description: T-203 r1 38ee0c3 changes (1 major); r2 fa34fe9 pass, 0 majors; open minor: Show box scrolls highlighted words off and clips label
metadata:
  type: project
---

T-203 r1 (reviews/T-203-ux-designer.md, 38ee0c3, 2026-11-02): **changes**, 1 major.
- Major: after Fix the wording at 375x667 the slot showed only "Saved: ... Read it once more", box at y 630-658 behind the bar; drawStatus showed the hint only when no Saved message.
- Minors: "above" wrong at 375x667; ABBR pt->patient treated PT (physical therapy) as patient.

T-203 r2 (reviews/T-203-ux-designer-r2.md, fa34fe9): **pass**, 0 majors, 1 minor, 3 nits. 145 passed (guided + no_console_errors + demo_provenance) on a fresh archive.
- Fixed: "Saved. Tick the box to say you compared them." + "Show box" button (34 px high, 13 px text); Show box puts box at y 441-469 above bar 482 and focuses it; Space then A finishes by keyboard.
- Open minor: Show box scrolls highlighted words off the top and clips the label's second line; nits: PT's/PTs still map to patient, hint 13 px, "Read it once more" only appears after the tick. Step 3 label wrap at 375 still not done.

Scripts: artifacts/review-evidence/T-203-ux-r2-measure.py (ports 7993 demo / 7994 local; makes lib10 and lib11 itself) and -r2-kbd.py. Windows run: window.G.step2.outsideParts is callable live.

**Why:** the 375x667 phone is treated as in scope, so edit-path gaps there were majors.

**How to apply:** if T-203 comes back, re-run r2-measure.py part 1 and check the label clipping after Show box. See [[project-t181-guided-build]].
---
name: reference_sample_load_stall
description: Playwright sample load (btn-sample, btn-analyze, entry-1) sometimes shows no entry-1 for 60 s just after an app server start; the server log stays empty; retry once and log the wait time
metadata:
  type: reference
---

On a freshly started app server (PORT set, fixture backend, empty ZLAYT_DB), the first sample analysis sometimes never shows `entry-1` within 60 s. `/api/health` is 200, the server log is empty, and no LLM failures are logged. A later load on the same server took 1.3 s (`wait_for` visible), and the same sample run succeeded inside 15 s in another run.

**Why:** Seen on T-046 r2 (2026-11-01) on three server starts. I could not isolate a cause from the server side.

**How to apply:** Load the sample once and wait up to 45 s for `entry-1`. On timeout, click `btn-analyze` once more and wait again. Record the wait time in the review's exercised list rather than reporting a stall as a product defect. Do not use a click result from a page where the sample stalled. See [[project_sbs_pane_overlay]] for the r2 walk.
---
name: feedback_reviewer_bash_parse_guard
description: git-guard refuses a reviewer Bash call it cannot parse ("No closing quotation") when one command chains a $(cat ...) assignment, a || fallback and echo strings; split the stop-and-verify steps into separate calls
metadata:
  type: feedback
---

On T-104 r1 (2026-11-02) one Bash call combining `SCR=...; PID=$(cat "$SCR/...")`, `ps -p $PID -o pid=,command=`, `kill`, a `sleep`, `(ps ... || echo "...")` and a `curl -w` failed in the PreToolUse hook: "git-guard: could not parse command safely (No closing quotation)". Nothing ran. The same kind of chained command had passed earlier.

GATE-M3 (2026-11-02): an inline `python -c "..."` with escaped backticks (\`\`\`json regex) was refused with "No escaped character". Same remedy: write the check to a .py file and run it.

**Why:** The hook's shell parser loses track of quotes in long compound lines. The failure costs a call and makes it unclear whether anything ran.

**How to apply:** Keep each Bash call to one purpose. Read the PID file with the Read tool, check the process with `ps -p <pid> -o pid=,command=` alone, then `kill <pid>` alone, then confirm the port in a separate call. Put Python checks in a file under artifacts/review-evidence/ (see [[feedback_reviewer_bash_devnull]]).
---
name: project-t180-guided-mockup
description: T-180 round 1 review of the guided UI spec and static mockup (changes, 4 majors); re-measure list and probe quirks for round 2 and the build card
metadata:
  type: project
---

T-180 r1 (reviews/T-180-ux-designer.md): verdict changes, 0 blockers, 4 majors. Mockup is static `file://` pages in artifacts/mockups/guided (28 pages; every answer is an href, so "nothing moves" is a weak test).

Majors to re-measure: (1) primary button below fold on step1-add (y975), step1-found (y897-953), step4-letter (Copy y1016) at 1440x900 and 1366x768; (2) at 390x844 source card is 122 px (23-38 percent of content), Undo ellipsized in the status slot; (3) paste/upload/Rename/error pages not mocked, demo offers Paste then refuses; (4) jargon on decision screens ("second check", "the model's quote", "checked by code", "itemized service line").

**Why:** Chris's brief is "grandma-simple"; the review pages have a fixed action bar but Step 1 and Step 4 do not.
**How to apply:** for round 2 and the build card, re-run artifacts/review-evidence/T-180-ux-fold.py and T-180-ux-scrollcards.py; also check api.md for `COMPARE_REQUIRED`, `compared`, PDF `title`. Probe quirk: git-guard rejects Bash with `$(...)`/backslash-escaped one-liners; write a script file instead.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:25.058Z

**tool call — Bash**
````
{
 "command": "git diff --stat 4e4ff36 HEAD -- app/ && git show --stat 82217e5 4e4ff36 | head -60",
 "description": "Show T-211 commit file stats and app diff since"
}
````

### User / tool · 2026-11-03T13:13:25.182Z

**tool result**
````
commit 82217e53c8f80b7dcca48c6b45e2c361f0229113
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 23:04:43 2026 -0600

    feat(frontend): T-211 How this was checked on every Step 2/3 item, How each answer is checked page, Step 3 reads date_label
    
    Panel from the item trace: code check, second AI check verdict and reason (prepared answers say so, D-065), your decision. Header link on every screen; ladder picture copied from submission. e2e test_t211.py (17) at 1440 and 390.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/app.js                |   9 +-
 app/frontend/guided/core.js               |   1 +
 app/frontend/guided/how.css               |  75 ++++++++++
 app/frontend/guided/how.js                |  54 +++++++
 app/frontend/guided/index.html            |   2 +
 app/frontend/guided/review.js             | 106 ++++++++++++-
 app/frontend/guided/step2.js              |  17 ++-
 app/frontend/guided/step3.js              |  24 ++-
 app/frontend/guided/validation-ladder.svg | 107 +++++++++++++
 tests/e2e/guided/test_t206.py             |   4 +-
 tests/e2e/guided/test_t211.py             | 241 ++++++++++++++++++++++++++++++
 11 files changed, 621 insertions(+), 19 deletions(-)

commit 4e4ff362b3791b58fca07f1a51a7c696aaec2bf5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 23:05:31 2026 -0600

    chore(frontend): T-211 refresh the ladder picture from submission/validation-ladder.svg
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/validation-ladder.svg | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:27.397Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && grep -n -i \"demo\" docs/RUNBOOK.md | head -30 && ls artifacts/review-evidence | grep -i \"T-211\" ; ls reviews | grep T-211",
 "description": "Record HEAD and find demo mode run instructions"
}
````

### User / tool · 2026-11-03T13:13:27.686Z

**tool result**
````
cda2856
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:29.375Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh; grep -n -i \"demo\\|PORT\\|ZLAYT_DB\" README.md | head -30",
 "description": "Read app serve script and README run instructions"
}
````

### User / tool · 2026-11-03T13:13:29.472Z

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
5:**Synthetic data only.** The app shows a banner and refuses text it has not seen in demo mode. Never paste real patient or client records.
20:Open <http://127.0.0.1:7860>. The first run creates `.venv` and installs `requirements.txt` (the only slow step); later runs start in seconds. Stop it with Ctrl-C. Use another port with `PORT=7870 ./run.sh`.
29:docker build -t zlayt-demo .
30:docker run --rm -p 7860:7860 zlayt-demo        # http://127.0.0.1:7860
40:2. **Step 1 of 4, "We found 9 records".** The nine synthetic records are listed with the dates the code read from them. Click **Draft the timeline**. When it finishes you should see "19 timeline items and 4 bill amounts are ready for you to check." (The badge "Prepared by our team" is demo mode; see below.) Click **Go to step 2: Check the timeline**.
49:Language and judgment (a one-line summary, "is this supported by the quote?", "do these two records conflict?") are model steps. Dates, gap arithmetic, quote matching, currency totals, sorting, de-duplication, schema checks and export assembly are plain code, never a model. Every model output then passes three rungs in order, and nothing a model produced reaches the letter without all three:
53:1. **Code check.** The excerpt must appear word for word in the record, every number, date and dollar figure in a summary must appear in the excerpt, the provider comes from the record's own source line. A failure is shown and never repaired; a rejected item cannot be exported. Code: [`app/backend/grounding.py`](app/backend/grounding.py), checks wired in [`app/backend/generator.py`](app/backend/generator.py) and [`app/backend/pipeline.py`](app/backend/pipeline.py), state rules in [`app/backend/confidence.py`](app/backend/confidence.py).
57:**Prompts.** Generator (does the drafting): [`extract_v1.md`](app/llm/prompts/extract_v1.md) (Spanish: [`extract_es_v1.md`](app/llm/prompts/extract_es_v1.md)), [`flags_v1.md`](app/llm/prompts/flags_v1.md), [`narrative_v1.md`](app/llm/prompts/narrative_v1.md), [`split_v1.md`](app/llm/prompts/split_v1.md). Judge (checks the drafting, different text): [`judge_faithfulness_v1.md`](app/llm/prompts/judge_faithfulness_v1.md) (J1), [`judge_amount_class_v1.md`](app/llm/prompts/judge_amount_class_v1.md) (J2), [`judge_conflict_v6.md`](app/llm/prompts/judge_conflict_v6.md) (J3), [`judge_flag_v3.md`](app/llm/prompts/judge_flag_v3.md) (J4). Older versions stay in [`app/llm/prompts/`](app/llm/prompts/) so changes are visible; each report records the prompt hashes it was run with.
61:- [`evals/`](evals/): the golden set (`evals/golden/`, expected outputs written by hand before the product code), seeded-error controls for the judges (`evals/golden/judge_controls*.jsonl`), 40 seeded hallucinations the checks must catch, the runner `evals/run.py`, and the reports.
62:- [`evals/reports/calibration.json`](evals/reports/calibration.json): measured calibration (how often each confidence state matched the hand-written expectation); the app serves it at `/api/calibration` and quotes it on the review screen.
63:- [`evals/reports/latest.json`](evals/reports/latest.json) and the dated `evals/reports/*.md`: the ship-bar report from live runs. Judge controls: [`evals/reports/controls-20261102T123937Z.md`](evals/reports/controls-20261102T123937Z.md) (every deliberately wrong answer caught, no false agreement).
66:**Demo mode and live mode.** Demo mode is the default and needs nothing. In demo mode no model is called and none can be: the backend is `fixture` and replays stored answers from [`tests/fixtures/llm/`](tests/fixtures/llm/). The sample's summaries and flags are **prepared answers** written and hand-checked by the team and labelled "Prepared by our team", never "AI draft" (decision D-065). The second check's verdicts are different: they are real recorded outputs of the judge model, never scripted (D-056), and the code checks run for real on every item. Live mode is opt-in and runs the real generator and judge on any pasted text.
68:| | Demo mode (default) | Live mode (opt-in) |
72:| Accepted input | the sample and the committed golden/library cases only (others get `409 demo_mode_unsupported_input`) | any pasted text or PDF, within size limits |
75:Demo wins whatever else is set: without `ENABLE_LIVE=1` the backend is `fixture` even if `LLM_BACKEND` or a key is present. Live `anthropic-api` also needs `PROVIDER_CAP_CONFIRMED=1` (you set a provider-side spend limit first) or the server refuses to start. The backends are in [`app/llm/backends/`](app/llm/backends/) and are chosen in [`app/llm/provider.py`](app/llm/provider.py); the resolved mode is in [`app/config.py`](app/config.py).
88:| Eval reports | [`evals/reports/latest.json`](evals/reports/latest.json) (current ship-bar numbers), [`evals/reports/`](evals/reports/) (dated reports, judge controls, calibration) |
97:What was deliberately left out, why, and what adding it would cost: [`memory/SCOPE_CUTS.md`](memory/SCOPE_CUTS.md). In short: no accounts or sharing, no real-data (PHI) handling, no medical or legal judgment (the tool points at the record's own words; diagnosis, severity and causation stay with the paralegal and attorney), no demand-letter prose in a firm's voice. The demo accepts only the sample and the committed cases; the Docker image is unverified; and the ship-bar result (3-run determinism, the judge's seeded-error controls) comes from live model runs, not from anything you can reproduce offline.
102:- `make evals` scores the golden set on the **fixture backend** and writes `data/evals/<timestamp>.md` (git-ignored; the committed `evals/reports/` are left alone). **It fails on a clean clone, and that is expected, not a defect** (the runner exits 1, so `make` prints `Error 1` and exits 2; the last lines name three `blocker:` items): the ship bar includes metrics that need live model runs (3-run determinism, the judge's seeded-error controls), and a fixture run cannot measure them, so the report says `ship_bar_met=False` and lists those as blockers by design. The Makefile prints a line saying so. Read the report's table for the numbers the fixture run can check (dates, gaps, totals, grounding); the ship-bar result comes from a live run, recorded in `evals/reports/latest.json`.
107:- **Port already in use**: `./run.sh` prints `error: port 7860 ... is already in use` and exits 3. Pick another: `PORT=7870 ./run.sh`.
110:- **Live mode exits with `error: ...`**: the message names the missing variable; see "Demo mode and live mode" above.
114:- Hugging Face Spaces (primary, Docker SDK, port 7860, secrets in Space settings): [`deploy/HUGGINGFACE.md`](deploy/HUGGINGFACE.md), one command `deploy/hf_push.sh <user>/<space>`.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:35.558Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T211-cda2856 && cd /Users/arsis/zlayt-pm-project && git archive cda2856 | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T211-cda2856 && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T211-cda2856",
 "description": "Extract HEAD archive into a new empty scratch dir"
}
````

### User / tool · 2026-11-03T13:13:37.242Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:44.238Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T211-cda2856 && PORT=7931 HOST=127.0.0.1 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t211.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t211-app.log 2>&1",
 "description": "Start demo-mode app server on port 7931 from archive",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T13:13:44.308Z

**tool result**
````
Command running in background with ID: bsb36ms5h. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bsb36ms5h.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:45.024Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p app/frontend/guided/review.js | grep -n \"how\\|How\" | head -60",
 "description": "Find how-checked panel code in review.js"
}
````

### User / tool · 2026-11-03T13:13:45.106Z

**tool result**
````
26:      .replace(/\b([Tt])he quote (does not|is not|is|has|says|contains|states|shows|carries|gives|labels)\b/g, (m, t, v) => `${t}he highlighted words ${v === "is" ? "are" : v === "has" ? "have" : v === "carries" ? "carry" : v === "gives" ? "give" : v === "labels" ? "label" : v === "does not" ? "do not" : v === "is not" ? "are not" : v === "says" ? "say" : v === "contains" ? "contain" : v === "states" ? "state" : "show"}`)
37:    hedge: { re: /\b(?:may|might|possibly|possible|probable|probably|likely|appears?|suspected|suggests?|suggestive of|consistent with|cannot be excluded|rule out|r\/o)\b/gi, because: "which shows it is not certain" },
40:    approx: { re: /\b(?:approx\.?|approximately|about|around|roughly|estimated)\b/gi, because: "which shows the figure is only close" },
42:  const FALLBACK_WORDS = { self_report: "a phrase that says whose account this is", hedge: "a word that shows it is not certain", negation: "a word that says something is not there", laterality: "the side (left or right)", approx: "a word that shows the figure is only close" };
90:  /* ---------- T-211 (D-074): "How this was checked" on every item: three rows in plain words, from the item's own check trace (GET .../items/<id>/trace; metadata only, no prompts).
96:  const CODE_PHRASE = [          // [trace step id, what passing it means], in the order they are said; two are shown
104:  R.howCode = function (tr) {
115:  R.howJudge = function (tr, item) {
126:  R.howYou = function (S, item) {
137:  R.howOpen = null;      // null until she toggles the panel; then it stays as she left it for the rest of the visit
145:    const full = text.length, win = opt.win && opt.win[0] > 0 || opt.win && opt.win[1] < full ? opt.win : null;       // opt.win = [from, to] in the record's own offsets: show only that part (several records in one warning)
199:        const it = S.cur(); if (it) S.forceCompare.set(it.id, (e.detail && e.detail.verdict) || "disagrees");       // the page did not know: show the compare box (the server's reason is in it), never a raw error
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:46.602Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/review.js",
 "offset": 88,
 "limit": 55
}
````

### User / tool · 2026-11-03T13:13:46.614Z

**tool result**
````
88	  };
89	
90	  /* ---------- T-211 (D-074): "How this was checked" on every item: three rows in plain words, from the item's own check trace (GET .../items/<id>/trace; metadata only, no prompts).
91	     1 Code check   what code verified (the passed steps with kind "code"), or what did not pass.
92	     2 Second AI check   a different model with a different prompt: verdict (agrees / disputes / could not check) and the fixed one-line reason the server wrote for its reason code.
93	                         A prepared demo answer (D-065) says so first: the team prepared it, then the second AI check read it against the quote.
94	     3 You   her decision, or "Waiting for you".
95	     The code and AI rows come from the trace (fetched once per item version); the You row is drawn at once from the item. A trace that cannot be read says so in the row, never a guess. ---------- */
96	  const CODE_PHRASE = [          // [trace step id, what passing it means], in the order they are said; two are shown
97	    ["excerpt_verbatim", "the highlighted words are in the record word for word"], ["summary_tokens", "the line's numbers and dates are in them"],
98	    ["found_in_text", "the amount appears in the record"], ["amount_class", "a rule sorted what kind of figure it is"],
99	    ["computed", "the dates and the number of days were worked out by code"], ["spans_match", "the words it points to are in the record"],
100	    ["record_warning_check", "the wording was found in the record by code"], ["date_confirmed", "the date comes from the record"],
101	  ];
102	  const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
103	  const isCodeStep = (x) => x.kind === "code" && (x.status === "pass" || x.status === "fail");
104	  R.howCode = function (tr) {
105	    const codes = ((tr && tr.steps) || []).filter(isCodeStep), bad = codes.filter((x) => x.status === "fail");
106	    if (!codes.length) return { state: "none", chip: "Code: none", text: "No code check applies to this item.", list: [] };
107	    const list = codes.map((x) => ({ ok: x.status === "pass", label: R.plain(x.label) }));
108	    if (bad.length) return { state: "bad", chip: "Code: not passed", text: "Did not pass: " + R.plain(bad[0].why || bad[0].label) + (bad.length > 1 ? ` (and ${bad.length - 1} more)` : ""), list };
109	    const ok = new Set(codes.map((x) => x.id)), say = CODE_PHRASE.filter(([id]) => ok.has(id)).slice(0, 2).map(([, t]) => t);
110	    return { state: "ok", chip: "Code: passed", text: "Passed: " + (say.length ? say.join(", and ") : `${codes.length} check${codes.length === 1 ? "" : "s"} by code`) + ".", list };
111	  };
112	  const VERDICT = { supported: ["Agrees", "ok", "AI: agrees"], agree: ["Agrees", "ok", "AI: agrees"], agrees: ["Agrees", "ok", "AI: agrees"],
113	    partially: ["Disputes", "bad", "AI: disputes"], unsupported: ["Disputes", "bad", "AI: disputes"], disagrees: ["Disputes", "bad", "AI: disputes"], disagree: ["Disputes", "bad", "AI: disputes"],
114	    unsure: ["Could not check", "warn", "AI: could not check"], unavailable: ["Could not check", "warn", "AI: could not check"] };
115	  R.howJudge = function (tr, item) {
116	    const steps = (tr && tr.steps) || [], st = steps.find((x) => x.kind === "llm" && x.evidence && x.evidence.model && x.evidence.model.role === "judge") || steps.find((x) => /^judge/.test(x.id));
117	    const prep = !!(item && item.prepared), lead = prep ? "Prepared by our team; the second AI check then checked it against the quote." : "";
118	    if (!st) return { state: "none", word: "Not run", chip: "AI: not run", lead, text: "No second AI check applies to this item.", model: "" };
119	    const ev = st.evidence || {}, m = ev.model && ev.model.id && !ev.model.prepared ? ev.model.id + (ev.prompt_version ? ` · prompt ${ev.prompt_version}` : "") : "";
120	    const text = cap(R.plain(ev.rationale || st.why || "").replace(/^A second AI check (?:also )?/, ""));          // the row is already headed "Second AI check"
121	    if (st.status === "skipped" && !ev.judge_verdict) return { state: "none", word: "Not needed", chip: "AI: not needed", lead, text: cap(text.replace(/^Not needed: /, "")), model: "" };
122	    if (st.status === "pending") return { state: "warn", word: "Not run yet", chip: "AI: not run yet", lead, text, model: m };
123	    const v = VERDICT[ev.judge_verdict] || (st.status === "fail" ? VERDICT.disagrees : VERDICT.supported);
124	    return { state: v[1], word: v[0], chip: v[2], lead, text, model: m };
125	  };
126	  R.howYou = function (S, item) {
127	    const t = S.cfg.youText && S.cfg.youText(S, item);
128	    if (t) return { state: "ok", chip: "You: decided", text: t };
129	    return { state: "wait", chip: "You: waiting", text: item.edit_to_check ? "You changed the wording. Waiting for you to compare it with the highlighted words." : "Waiting for you." };
130	  };
131	  const TRACES = new Map();      // token|item|version -> Promise<trace>. A write changes the version, so the next look asks again. A failed read is forgotten.
132	  R.traceOf = function (S, item) {
133	    const key = S.token + "|" + item.id + "|" + item.version;
134	    if (!TRACES.has(key)) TRACES.set(key, G.api.itemTrace(S.token, item.id).catch((e) => { TRACES.delete(key); throw e; }));
135	    return TRACES.get(key);
136	  };
137	  R.howOpen = null;      // null until she toggles the panel; then it stays as she left it for the rest of the visit
138	
139	  /* ---------- the record, with the highlighted words marked, or its sentences tappable ---------- */
140	  R.recBlock = function (rec, opt) {
141	    opt = opt || {};
142	    let text = rec.text || "", base = rec.char_start || 0;
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:47.379Z

**tool call — Bash**
````
{
 "command": "grep -n \"drawHow\\|howOpen\\|how-\" app/frontend/guided/review.js | head -40; cat app/frontend/guided/how.js",
 "description": "Find drawHow and read how.js page"
}
````

### User / tool · 2026-11-03T13:13:47.466Z

**tool result**
````
137:  R.howOpen = null;      // null until she toggles the panel; then it stays as she left it for the rest of the visit
248:    E.how = h("details", { class: "how", "data-testid": "how-checked", hidden: true });
258:    E.showBox = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-show-box", hidden: true }, "Show box");
347:      drawHow(item, sc);
361:    function drawHow(item, sc) {
366:      const row = (key, label, sub) => { const v = h("div", { class: "how-v", "data-testid": "how-" + key + "-text" }, "Checking…"), s = sub ? h("span", { class: "how-sub", "data-testid": "how-" + key + "-sub" }, sub) : null, r = h("div", { class: "how-r", "data-testid": "how-" + key }, h("div", { class: "how-l" }, h("b", {}, label), s), v); return [r, v, s]; };
369:      const chip = (key, text, state) => h("span", { class: "hchip " + (state || ""), "data-testid": "how-chip-" + key }, text);
371:      const sum = h("summary", { "data-testid": "how-summary" }, h("span", { class: "how-t" }, "How this was checked"), h("span", { class: "how-chips" }, cCode, cAi, cYou));
372:      E.how.replaceChildren(sum, h("div", { class: "how-rows" }, rCode, rAi, rYou));
374:      const want = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;
376:      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };
381:        const ul = h("ul", { class: "how-all", "data-testid": "how-all-list", hidden: true }, c.list.map((x) => h("li", { class: x.ok ? "ok" : "bad" }, h("span", { "aria-hidden": "true" }, x.ok ? "✓ " : "✗ "), h("span", { class: "sr" }, x.ok ? "Passed: " : "Did not pass: "), x.label)));
382:        const more = c.list.length ? h("button", { type: "button", class: "how-more", "data-testid": "how-all-checks", "aria-expanded": "false", onclick: () => { ul.hidden = !ul.hidden; more.setAttribute("aria-expanded", ul.hidden ? "false" : "true"); } }, `All ${c.list.length} check${c.list.length === 1 ? "" : "s"}`) : null;
385:        vAi.replaceChildren(...[j.lead ? h("p", { class: "how-lead", "data-testid": "how-prepared" }, j.lead) : null, h("p", {}, h("b", { class: "how-verdict " + j.state, "data-testid": "how-verdict" }, j.word), j.text ? ". " + j.text : ""),
399:      if (!E.how.open || R.howOpen != null || E.how.parentNode !== E.srcCard) { if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark(); return; }
/* "How each answer is checked" (/how-it-works). T-211, D-074. Reachable from the header on every screen (app.js draws the link).
   A plain explanation of the validation ladder for a first-time reader: draft (AI, or prepared answers in the demo) -> code checks -> an independent second AI check -> you decide. What is code and what is AI, with the repo's doc names in text.
   The wording about who drafted follows the same provenance rule as the rest of the app (G.provenance, D-065): a prepared demo never says an AI wrote the answers.
   Page contract: G.pages.how = async (ctx) => cleanup. Text only (textContent); no inline style attributes. Test ids: how-page, how-steps, how-step-1..4, how-ladder-img, how-ladder-open, how-code-vs-ai, how-repo, how-back. */
(function () {
  const G = window.G, { h } = G;

  const code = (t) => h("code", {}, t);

  G.pages.how = async function (ctx) {
    await G.healthNow(ctx.signal);
    const p = G.provenance();
    const draft = p.kind === "prepared"
      ? ["Prepared by our team. ", "In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from."]
      : p.kind === "recorded"
        ? ["Drafted by an AI model. ", "An AI model drafted a one-line summary of each record and picked the exact words it came from. In this demo those answers were recorded earlier."]
        : ["Drafted by an AI model. ", "An AI model reads each record, drafts a one-line summary and picks the exact words it came from."];
    const back = h("button", { type: "button", class: "btn", "data-testid": "how-back", onclick: () => { if (G.navigated) history.back(); else ctx.go("/"); } }, "‹ Back");      // by a link inside the app: back to where she was; opened directly (history.length also counts the blank tab): to the cases
    const step = (n, head, body) => h("li", { "data-testid": "how-step-" + n }, h("span", { class: "how-n", "aria-hidden": "true" }, String(n)), h("div", {}, h("b", {}, head), " ", body));

    ctx.view.append(h("main", { class: "wrap how-page", id: "main", "data-testid": "how-page" },
      h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("h1", { "data-testid": "page-title" }, "How each answer is checked"),
        h("p", {}, "Nothing reaches your letter until code has checked it, a second AI has checked it, and you have said yes.")), back),
      h("div", { class: "panel" },
        h("ol", { class: "how-steps", "data-testid": "how-steps" },
          step(1, draft[0], draft[1]),
          step(2, "Code checks it.", "Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone."),
          step(3, "A second AI checks it.", "A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote."),
          step(4, "You decide.", "You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.")),
        h("p", { class: "muted how-note" }, "Each item in steps 2 and 3 shows these three checks under “How this was checked”. The second AI can be wrong too, which is why the last word is yours.")),
      h("div", { class: "panel" }, h("h2", {}, "The checks, as a picture"),
        h("div", { class: "how-fig", tabindex: "0", role: "group", "aria-label": "The validation ladder picture. It scrolls sideways on a narrow screen." },
          h("img", { src: "/validation-ladder.svg", width: "820", height: "600", alt: "Validation ladder. A record goes to a draft. Rung 1, code, checks the quote word for word and every number. Rung 2, a second AI with a different prompt, agrees, disputes or could not check. Rung 3, you accept, edit or dismiss. Code builds the export from accepted items only. Items that fail a check go to a could-not-verify list and never reach the letter.", "data-testid": "how-ladder-img" })),
        h("p", { class: "muted how-note" }, h("a", { href: "/validation-ladder.svg", target: "_blank", rel: "noopener", "data-testid": "how-ladder-open" }, "Open the picture full size"), " (it opens in a new tab).")),
      h("div", { class: "panel", "data-testid": "how-code-vs-ai" }, h("h2", {}, "What is code and what is AI"),
        h("div", { class: "how-cols" },
          h("div", {}, h("h3", {}, "Code only, never AI"),
            h("ul", {}, h("li", {}, "Splitting the pasted text into records"), h("li", {}, "Reading dates, and the days between visits"), h("li", {}, "Finding every dollar amount, saying what kind it is, and adding up the total"),
              h("li", {}, "Checking that a quote is in the record word for word, and that its numbers are in the quote"), h("li", {}, "The wording of each warning, sorting, and building the letter"))),
          h("div", {}, h("h3", {}, "AI, always checked"),
            h("ul", {}, h("li", {}, "Drafting a one-line summary and picking the quote" + (p.kind === "prepared" ? " (prepared by our team in this demo)" : "")), h("li", {}, "The second check that reads each answer against the record"),
              h("li", {}, "Spotting wording the other side could use, which code then checks and you decide"))))),
      h("div", { class: "panel", "data-testid": "how-repo" }, h("h2", {}, "Where to read more in the repo"),
        h("ul", { class: "how-repo" },
          h("li", {}, code("docs/LLM_VS_CODE.md"), ": every step, whether it is code or AI, and how it is checked."),
          h("li", {}, code("app/llm/prompts/"), ": the second check's prompts, for example ", code("judge_faithfulness_v1.md"), " and ", code("judge_amount_class_v1.md"), "."),
          h("li", {}, code("app/backend/grounding.py"), ": the word-for-word and number checks. ", code("app/backend/judges.py"), ": how the second AI's answer becomes a verdict."),
          h("li", {}, code("evals/"), ": the golden cases and reports that measure both checks."),
          h("li", {}, code("memory/ORCHESTRATOR_DECISIONS.md"), ": D-065 (prepared answers are never called AI output) and D-066 (a disputed line needs your comparison).")),
        h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: "/", "data-testid": "how-home" }, "Back to your cases")))));
    ctx.setTitle("How each answer is checked");
    return undefined;
  };
})();
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:50.552Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/frontend/guided/review.js",
 "offset": 240,
 "limit": 175
}
````

### User / tool · 2026-11-03T13:13:50.560Z

**tool result**
````
240	    E.srcBody = h("div", { class: "card-b", "data-testid": "card-source", tabindex: "0", "aria-label": "The record" });
241	    E.lineHead = h("div", { class: "card-h", "data-testid": "line-head" });
242	    E.lineBody = h("div", { class: "card-b", "data-testid": "line-body" });
243	    E.foot = h("div", { class: "card-f plain", "data-testid": "card-foot", tabindex: "-1" });
244	    E.lineCard = h("section", { class: "card card-line", "aria-label": "To check", "data-testid": "card-line" }, E.lineHead, E.lineBody, E.foot);
245	    E.srcCard = h("section", { class: "card card-src", "aria-label": "From the record", "data-testid": "card-src" }, h("div", { class: "card-h" }, h("span", { class: "ch-title" }, "From the record"), E.srcHead), E.srcBody);
246	    E.work = h("main", { class: "work", id: "main", "data-testid": "work" }, E.srcCard, E.lineCard);
247	    /* T-211: "How this was checked" sits under the quote in the record card on a wide screen (it never takes room from the line), and at the end of the line card on a phone (that card scrolls as one box; the footer with its tick box stays beside the line) */
248	    E.how = h("details", { class: "how", "data-testid": "how-checked", hidden: true });
249	    const narrowMQ = matchMedia("(max-width: 760px)");
250	    const placeHow = () => { const into = narrowMQ.matches ? E.lineCard : E.srcCard; if (E.how.parentNode !== into) into.append(E.how); };
251	    narrowMQ.addEventListener("change", placeHow); placeHow();
252	    const btn = (cls, tid, key) => h("button", { type: "button", class: "btn " + cls, "data-testid": tid, "aria-keyshortcuts": key || null });
253	    E.question = h("p", { class: "question", id: "q", "data-testid": "question" });
254	    E.yes = btn("answer primary", "answer-yes", "a"); E.no = btn("answer", "answer-no", "d");
255	    E.yes.setAttribute("data-autofocus", "");
256	    E.back = btn("quiet", "btn-back", "ArrowLeft"); E.third = btn("quiet", "btn-third", "e"); E.later = btn("quiet", "btn-later", "ArrowRight");
257	    E.statusText = h("span", { class: "st-msg", "data-testid": "status-text" }); E.undo = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-undo", hidden: true }, "Undo");
258	    E.showBox = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-show-box", hidden: true }, "Show box");
259	    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo, E.showBox);
260	    E.actions = h("div", { class: "actions", "data-testid": "actions" }, h("div", { class: "actions-in" }, E.question,
261	      h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
262	    E.back.textContent = "‹ Back"; E.later.textContent = "Decide later";
263	    E.back.onclick = () => back();
264	    E.later.onclick = () => { const l = S.screen && S.screen.later; if (l === false) return; if (l && l.run) l.run(); else S.skip(); };
265	    ctx.view.replaceChildren(E.titlebar, E.work, E.actions);
266	    ctx.layout("frame");
267	
268	    function toggleSteps(force) {
269	      const open = force != null ? force : !body.classList.contains("steps-open");
270	      body.classList.toggle("steps-open", open); E.toggle.setAttribute("aria-expanded", open ? "true" : "false");
271	    }
272	    const onDocClick = (e) => { if (body.classList.contains("steps-open") && !e.target.closest("#step-bar") && !e.target.closest("[data-testid=btn-steps]")) toggleSteps(false); };
273	
274	    function drawStatus() {
275	      const s = S.said;
276	      const box = E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
277	      const tick = box ? (box.dataset.testid === "check-compare" ? "Tick the box to say you compared them." : "Tick the box first.") : "";      // no direction word: the box can be above the bar or below the screen
278	      const saved = s && !s.undo && /^Saved/.test(s.text);      // a "Saved" note must not hide the reason Yes is greyed: both stay until she ticks
279	      const why = box && (!s || saved);
280	      E.statusText.textContent = why ? (saved ? "Saved. " : "") + tick : s ? s.text : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
281	      E.status.classList.toggle("hint", !s && !why);
282	      E.status.dataset.why = why ? "tick" : "";
283	      E.undo.hidden = !(s && s.undo);
284	      E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;
285	      const hidden = !!why && boxHidden(box);      // the box is under the bar or below the screen: one tap brings it into view
286	      E.showBox.hidden = !hidden;
287	      E.showBox.onclick = hidden ? () => revealBox(box) : null;
288	    }
289	    function boxHidden(box) {
290	      const r = box.getBoundingClientRect(), bar = E.actions.getBoundingClientRect();
291	      return r.bottom > bar.top - 4 || r.top < 0;
292	    }
293	    function revealBox(box) {
294	      const bar = E.actions.getBoundingClientRect();
295	      box.style.scrollMarginBottom = Math.ceil(window.innerHeight - bar.top + 12) + "px";
296	      try { box.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* nothing to scroll */ }
297	      box.focus({ preventScroll: true }); drawStatus();
298	    }
299	
300	    function updateTitlebar() {
301	      const items = S.counted(), left = S.left().length, total = items.length, done = total - left;
302	      const q = S.queue[S.idx], n = q && !q.optional ? S.numberOf(q.id) : null;
303	      E.count.textContent = S.screen && S.screen.counter ? S.screen.counter : n ? `${cfg.unit} ${n} of ${total}` : q && q.optional ? "Optional" : `${total} ${cfg.unit.toLowerCase()}s`;
304	      E.prog.textContent = `${done} answered · ${left} to go`;
305	      const pct = total ? Math.round((done / total) * 100) : 100;
306	      E.fill.style.width = pct + "%"; E.bar.setAttribute("aria-valuenow", String(pct));
307	      if (cfg.chip) E.total.textContent = R.money(((S.c.totals || {}).accepted || {}).cents || 0);
308	    }
309	
310	    /* ---- render one screen ---- */
311	    function fillTag(tag, extra) { return tag ? h("span", { class: "tag " + tag.cls, title: tag.title || null, "data-testid": extra || "line-tag" }, tag.text) : null; }
312	    function syncButtons() {
313	      const sc = S.screen; if (!sc) return;
314	      const set = (el, def) => {                                    // an absent answer keeps its place (invisible), so nothing else moves
315	        if (!def) { el.style.visibility = "hidden"; el.disabled = true; el.setAttribute("aria-hidden", "true"); el.tabIndex = -1; return; }
316	        el.disabled = S.busy || (typeof def.disabled === "function" ? def.disabled() : !!def.disabled);
317	        el.style.visibility = ""; el.removeAttribute("aria-hidden"); el.removeAttribute("tabindex");
318	      };
319	      set(E.yes, sc.yes); set(E.no, sc.no); set(E.third, sc.third);
320	      E.back.disabled = S.busy || sc.back === false; E.later.disabled = S.busy;
321	      E.later.style.visibility = sc.later === false ? "hidden" : ""; E.later.tabIndex = sc.later === false ? -1 : 0;
322	      E.third.classList.toggle("hint", !!(sc.third && sc.third.hint));
323	      E.undo.disabled = S.busy;
324	    }
325	    function drawBtn(el, def, keep) {
326	      if (!def) { el.replaceChildren(keep || ""); el.classList.remove("two"); el.onclick = null; return; }
327	      el.replaceChildren(...[def.label, def.sub ? h("span", { class: "sub" }, def.sub) : null].filter(Boolean));
328	      el.classList.toggle("two", !!def.sub); el.onclick = () => def.run();
329	      if (el === E.yes) el.classList.toggle("primary", !def.plain);
330	    }
331	    function render(keepScroll) {
332	      const item = S.cur(), q = S.queue[S.idx];
333	      if (!item) return finish();
334	      const sc = (S.screen = cfg.present(S, item, q));
335	      E.lineCard.dataset.itemId = item.id; E.lineCard.dataset.kind = item.kind || ""; E.lineCard.dataset.mode = S.ui.mode || "view";
336	      const head = [fillTag(sc.tag), fillTag(sc.tag2, "line-tag2"), sc.sub ? h("span", { class: "ch-sub", "data-testid": "line-sub" }, sc.sub) : null];
337	      E.lineHead.replaceChildren(...head.filter(Boolean));
338	      const bodyScroll = E.lineBody.scrollTop;
339	      E.lineBody.replaceChildren(...[].concat(sc.body || []).filter(Boolean));
340	      E.lineBody.scrollTop = keepScroll ? bodyScroll : 0;
341	      if (!keepScroll) E.lineCard.scrollTop = 0;
342	      const err = S.err ? { cls: "bad", nodes: [h("strong", {}, "Not saved. "), S.err.text] } : null;
343	      const foot = err || sc.foot || { cls: "plain", nodes: [] };
344	      E.foot.className = "card-f " + (foot.cls || "plain"); E.foot.replaceChildren(...[].concat(foot.nodes || []).filter(Boolean));
345	      if (err) E.foot.setAttribute("role", "alert"); else E.foot.removeAttribute("role");
346	      E.question.textContent = sc.question || "";
347	      drawHow(item, sc);
348	      drawBtn(E.yes, sc.yes, "Yes"); drawBtn(E.no, sc.no, "No"); drawBtn(E.third, sc.third, "Fix the wording");
349	      E.later.textContent = sc.later && sc.later.label ? sc.later.label : "Decide later";
350	      // a phone: when any item of this step needs a tick box the line card gets the room for the whole visit (so nothing moves between items), and the line and its box are on screen together
351	      S.sticky = S.sticky || S.queue.some((q) => { const it = S.item(q.id); return !!it && (!!R.dispute(it) || !!it.edit_to_check || (it.countable && it.kind !== "charge") || (it.flag && it.confirm_required)); }) || !!E.foot.querySelector("input[type=checkbox]");
352	      E.work.classList.toggle("needs-check", !!S.sticky);      // before the record is drawn: the window is its final size when the highlight is scrolled into it
353	      renderSource(false);
354	      fitHow();
355	      updateTitlebar(); syncButtons(); drawStatus();
356	      if (err) showRefusal();
357	      if (!keepScroll) focusFirst(sc);
358	    }
359	    /* ---- T-211: the three rows ---- */
360	    let howTicket = 0;
361	    function drawHow(item, sc) {
362	      const mine = ++howTicket;
363	      if (sc.how === false) { E.how.hidden = true; E.how.replaceChildren(); return; }
364	      E.how.hidden = false;
365	      const you = R.howYou(S, item);
366	      const row = (key, label, sub) => { const v = h("div", { class: "how-v", "data-testid": "how-" + key + "-text" }, "Checking…"), s = sub ? h("span", { class: "how-sub", "data-testid": "how-" + key + "-sub" }, sub) : null, r = h("div", { class: "how-r", "data-testid": "how-" + key }, h("div", { class: "how-l" }, h("b", {}, label), s), v); return [r, v, s]; };
367	      const [rCode, vCode] = row("code", "Code check", "no AI"), [rAi, vAi, sAi] = row("ai", "Second AI check", "own model and prompt"), [rYou, vYou] = row("you", "You");
368	      vYou.textContent = you.text; rYou.dataset.state = you.state;
369	      const chip = (key, text, state) => h("span", { class: "hchip " + (state || ""), "data-testid": "how-chip-" + key }, text);
370	      const cCode = chip("code", "Code: …"), cAi = chip("ai", "AI: …"), cYou = chip("you", you.chip, you.state);
371	      const sum = h("summary", { "data-testid": "how-summary" }, h("span", { class: "how-t" }, "How this was checked"), h("span", { class: "how-chips" }, cCode, cAi, cYou));
372	      E.how.replaceChildren(sum, h("div", { class: "how-rows" }, rCode, rAi, rYou));
373	      E.how.dataset.item = item.id; E.how.setAttribute("aria-busy", "true");
374	      const want = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;
375	      if (want !== E.how.open) { E.how._auto = true; E.how.open = want; }          // a change the page made is not her choice (the toggle event says which)          // closed (chips only) on a phone and on a short window until she opens it
376	      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };
377	      R.traceOf(S, item).then((tr) => {
378	        if (mine !== howTicket || !S.alive) return;
379	        const c = R.howCode(tr), j = R.howJudge(tr, item);
380	        rCode.dataset.state = c.state; cCode.textContent = c.chip; cCode.className = "hchip " + c.state;
381	        const ul = h("ul", { class: "how-all", "data-testid": "how-all-list", hidden: true }, c.list.map((x) => h("li", { class: x.ok ? "ok" : "bad" }, h("span", { "aria-hidden": "true" }, x.ok ? "✓ " : "✗ "), h("span", { class: "sr" }, x.ok ? "Passed: " : "Did not pass: "), x.label)));
382	        const more = c.list.length ? h("button", { type: "button", class: "how-more", "data-testid": "how-all-checks", "aria-expanded": "false", onclick: () => { ul.hidden = !ul.hidden; more.setAttribute("aria-expanded", ul.hidden ? "false" : "true"); } }, `All ${c.list.length} check${c.list.length === 1 ? "" : "s"}`) : null;
383	        vCode.replaceChildren(...[c.text, " ", more, ul].filter(Boolean));
384	        rAi.dataset.state = j.state; cAi.textContent = j.chip; cAi.className = "hchip " + j.state;
385	        vAi.replaceChildren(...[j.lead ? h("p", { class: "how-lead", "data-testid": "how-prepared" }, j.lead) : null, h("p", {}, h("b", { class: "how-verdict " + j.state, "data-testid": "how-verdict" }, j.word), j.text ? ". " + j.text : ""),
386	          ].filter(Boolean));
387	        if (j.model) { sAi.textContent = j.model.split(" · ")[0]; sAi.title = "Model and prompt: " + j.model; sAi.dataset.model = j.model; }
388	        E.how.removeAttribute("aria-busy");
389	        fitHow();
390	      }).catch((e) => {
391	        if (mine !== howTicket || !S.alive || (e && e.name === "AbortError")) return;
392	        for (const [v, c, k] of [[vCode, cCode, "Code"], [vAi, cAi, "AI"]]) { v.textContent = "We couldn't load this just now."; c.textContent = k + ": –"; }
393	        E.how.removeAttribute("aria-busy");
394	      });
395	    }
396	    /* The highlighted words come first: when the open panel would push any of them out of the record window (several records in one warning, a long quote), and she has not chosen to keep it open,
397	       it folds to its one-line chips. She can open it; her choice then stays for the rest of the visit. */
398	    function fitHow() {
399	      if (!E.how.open || R.howOpen != null || E.how.parentNode !== E.srcCard) { if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark(); return; }
400	      const box = E.srcBody.getBoundingClientRect(), cut = [...E.srcBody.querySelectorAll("mark")].some((m) => { const r = m.getBoundingClientRect(); return r.bottom > box.bottom + 1; });
401	      if (cut) { E.how._auto = true; E.how.open = false; if (S.alignMark) S.alignMark(); } else if (S.alignMark) S.alignMark();
402	    }
403	    function renderSource(keep) {
404	      const sc = S.screen; if (!sc || !sc.src) { E.srcHead.textContent = ""; E.srcBody.replaceChildren(); return; }
405	      const top = E.srcBody.scrollTop;
406	      E.srcHead.textContent = sc.src.head || ""; E.srcBody.replaceChildren(...sc.src.nodes().filter(Boolean));
407	      if (keep) E.srcBody.scrollTop = top;
408	      else alignMark();
409	    }
410	    /* the first highlighted word is in the record window: top-aligned with one line of the record above it on a phone (the window is small), a third down on a wide screen. Measured with rects, not offsetTop (the window is not the mark's offset parent). */
411	    function alignMark() {
412	      const box = E.srcBody, m = box.querySelector("mark, .sent.on");
413	      if (!m) { box.scrollTop = 0; return; }
414	      const narrow = matchMedia("(max-width: 760px)").matches, lead = narrow ? Math.min(30, box.clientHeight / 4) : box.clientHeight / 3;
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:53.037Z

**tool call — Bash**
````
{
 "command": "curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7931/ ; curl -s http://127.0.0.1:7931/api/health",
 "description": "Check demo server on port 7931 is up"
}
````

### User / tool · 2026-11-03T13:13:53.154Z

**tool result**
````
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":false,"answers":"recorded","live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5","generator_prepared":false},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:13:56.263Z

**tool call — Bash**
````
{
 "command": "grep -n \"provenance\" app/frontend/guided/core.js | head; grep -rn \"FIXTURE_SET\" app/config.py run.sh Dockerfile tests/e2e/conftest.py | head",
 "description": "Check provenance logic and FIXTURE_SET defaults"
}
````

### User / tool · 2026-11-03T13:13:56.353Z

**tool result**
````
tests/e2e/conftest.py:128:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
run.sh:36:    export LLM_BACKEND="${LLM_BACKEND:-fixture}" FIXTURE_SET="${FIXTURE_SET:-curated}" HOST="${HOST:-127.0.0.1}" PORT="${PORT:-7860}"
app/config.py:12:DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}
app/config.py:31:        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
Dockerfile:23:ENV HOST=0.0.0.0 PORT=7860 LLM_BACKEND=fixture FIXTURE_SET=curated DATA_DIR=/home/user/data
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:00.117Z

**tool call — Bash**
````
{
 "command": "cat run.sh; grep -rn \"FIXTURE_SET\\|generator_prepared\" app/backend/*.py app/main.py app/llm/provider.py | head",
 "description": "Read run.sh and where FIXTURE_SET is read"
}
````

### User / tool · 2026-11-03T13:14:00.212Z

**tool result**
````
#!/bin/sh
# One command from a fresh clone to the guided UI in demo mode (no key, no network after the one-time install).
#   ./run.sh                 demo mode on http://127.0.0.1:7860   (PORT=7870 ./run.sh to change the port)
#   ./run.sh setup           create .venv and install requirements only
#   ./run.sh test            run the unit tests (installs requirements-dev.txt first)
# Live mode is opt-in: see README.md and .env.example. This script never reads or prints .env.
set -eu
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null; then
  echo "Python 3.12+ is required (found: $("$PY" --version 2>&1)). Install it, or set PYTHON=/path/to/python3.12." >&2
  exit 1
fi

if [ ! -x .venv/bin/python ]; then
  echo "Creating .venv and installing requirements (one time, about a minute)..."
  "$PY" -m venv .venv
fi
# Reinstall only when requirements.txt changed since the last successful install.
if [ ! -f .venv/.installed ] || [ requirements.txt -nt .venv/.installed ]; then
  .venv/bin/pip install --quiet --disable-pip-version-check -r requirements.txt
  touch .venv/.installed
fi

case "${1:-serve}" in
  setup)
    echo "Ready: .venv installed." ;;
  test)
    .venv/bin/pip install --quiet --disable-pip-version-check -r requirements-dev.txt
    exec .venv/bin/python -m pytest tests/unit -q ;;
  serve)
    # Demo defaults; a value you already exported wins.
    # On Replit (REPL_ID is set) the preview/published URL only reaches a process bound to 0.0.0.0.
    if [ -z "${HOST:-}" ] && [ -n "${REPL_ID:-}" ]; then HOST=0.0.0.0; fi
    export LLM_BACKEND="${LLM_BACKEND:-fixture}" FIXTURE_SET="${FIXTURE_SET:-curated}" HOST="${HOST:-127.0.0.1}" PORT="${PORT:-7860}"
    .venv/bin/python -m app.config
    # app.main prints "Serving on ..." once the port is free; a startup error is one line, not a traceback.
    exec .venv/bin/python -m app.main ;;
  *)
    echo "usage: ./run.sh [serve|setup|test]" >&2; exit 2 ;;
esac
app/backend/api.py:144:        return dict(base, generator=present.PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
app/backend/api.py:630:            ex["provenance"] = {"generator_model": mm["generator"], "judge_model": mm["judge"], "generator_prepared": mm["generator_prepared"], "backend": backend(),
app/backend/present.py:283:        self.case_prepared = models_for(conn, case_id, {"generator": "", "judge": ""}, self.calls)["generator_prepared"]
app/backend/present.py:338:    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with any recorded or live answer keeps the configured model; one with no usable answer follows the set in use."""
app/backend/present.py:342:    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
app/backend/store.py:161:    prep = present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"]      # D-069: the case's provenance chooses the wording of the export's notes and labels
app/backend/trace.py:191:        self.prep = bool(self.models.get("generator_prepared"))      # D-069: the case's own provenance; an item's wording is this OR its own first answer's
app/backend/trace.py:1033:    use_voice(present.models_for(conn, case_id, {"generator": "", "judge": ""})["generator_prepared"])
app/backend/trace.py:1173:    prep = bool(cx.models.get("generator_prepared"))      # T-177 r2 / D-065: the case's answers are hand-checked fixtures, so the step must not say an AI drafted them
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:03.609Z

**tool call — Bash**
````
{
 "command": "grep -n '\"answers\"' app/backend/api.py | head -5; grep -n \"def models_for\" -A 12 app/backend/present.py | head -30",
 "description": "Check health answers field and models_for"
}
````

### User / tool · 2026-11-03T13:14:03.702Z

**tool result**
````
266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
336:def models_for(conn, case_id, base, calls=None):
337-    """D-065 (T-177 r2): the {generator, judge} model names a payload shows for THIS case. When every generator answer of the case is a hand-checked fixture, no model drafted it: the generator reads
338-    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with any recorded or live answer keeps the configured model; one with no usable answer follows the set in use."""
339-    calls = DB.list_llm_calls(conn, case_id) if calls is None else calls
340-    gens = [c for c in calls if c["role"] == "generator" and not str(c.get("error") or "").startswith("FIXTURE_MISS")]      # a call that found no answer is no model's work and no fixture's
341-    prepared = all(AU.is_prepared(c.get("recorded_from")) for c in gens) if gens else AU.answers_prepared()      # D-069: no usable answer (malformed, empty or missing counts as none) is decided by the set in use, never by a model label
342-    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
343-
344-
345-def narrative_view(conn, case_id, nar):
346-    """D-065: the draft paragraph's generator answer, marked prepared (and named 'hand-checked (qa)') when it came from a curated fixture."""
347-    if not nar or not isinstance(nar.get("generator"), dict):
348-        return nar
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:06.749Z

**tool call — Bash**
````
{
 "command": "sed -n 1,120p tests/e2e/guided/test_t211.py",
 "description": "Read the T-211 e2e test helpers"
}
````

### User / tool · 2026-11-03T13:14:06.830Z

**tool result**
````
"""T-211 (D-074): the app itself shows and explains the validation ladder. Real browser, fixture backend (curated set), real API; cases are made over the API and deleted afterwards.
Guarded: every Step 2 and Step 3 item shows "How this was checked" with three rows (code check, second AI check with its verdict and reason, you); a prepared answer says it was prepared by our team and then
checked; a disputed or failed check is shown in words (the trace is rewritten the way the server answers for one); the panel never hides the highlighted words or the primary action at 1440x900 and fits at 390px;
the header link on every screen opens "How each answer is checked" (about 150 words, the ladder picture, what is code and what is AI, the repo doc names); no console error anywhere."""
import json
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, sized, case, item, open_item, settle   # noqa: F401  (make and phone are fixtures)

VERDICTS = {"Agrees", "Disputes", "Could not check", "Not needed"}


def rows(page):
    t = lambda k: page.get_by_test_id(k).inner_text()
    return t("how-code-text"), t("how-ai-text"), t("how-you-text")


def wait_loaded(page):
    expect(page.get_by_test_id("how-checked")).not_to_have_attribute("aria-busy", "true", timeout=10000)


def open_panel(page):
    """At 1440x900 the panel folds to its chips when it would push a highlighted word out of the record window; she opens it with one click (and it then stays open)."""
    if not page.get_by_test_id("how-code").is_visible():
        page.get_by_test_id("how-summary").click()
    expect(page.get_by_test_id("how-code")).to_be_visible()


def inside(outer, inner):
    return inner["y"] >= outer["y"] - 1 and inner["y"] + inner["height"] <= outer["y"] + outer["height"] + 1


# ------------------------------------------------------------------------------------------------ the three rows on every item

def test_every_item_of_steps_2_and_3_shows_code_check_second_ai_check_and_you(pw, make):
    tok = make(); c = case(tok)
    b, pg = sized(pw, 1440, 900)
    try:
        seen = watch(pg)
        steps = [("timeline", i["id"]) for g in ("entries", "undated_entries", "flags") for i in c[g]] + [("bills", a["id"]) for a in c["amounts"]]
        assert len(steps) >= 15
        for step, iid in steps:
            open_item(pg, tok, iid, step=step); wait_loaded(pg)
            expect(pg.get_by_test_id("how-summary")).to_be_visible()
            for k in ("how-chip-code", "how-chip-ai", "how-chip-you"):
                assert pg.get_by_test_id(k).count() == 1, (iid, k)
            open_panel(pg)
            code, ai, you = rows(pg)
            assert code.startswith(("Passed:", "Did not pass:", "No code check")), (iid, code)
            assert page_verdict(pg) in VERDICTS, (iid, page_verdict(pg))
            assert ai.strip() and "Checking" not in ai and "Checking" not in code, (iid, ai)
            assert you.strip() == "Waiting for you.", (iid, you)
            for k in ("how-code", "how-ai", "how-you"):
                expect(pg.get_by_test_id(k)).to_be_visible()
            y = pg.get_by_test_id("answer-yes").bounding_box(); assert y["y"] + y["height"] <= 900, f"{iid}: the primary action is below the fold"
            assert pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight"), iid
        assert seen == [], seen
    finally:
        b.close()


def page_verdict(pg):
    return pg.get_by_test_id("how-verdict").inner_text()


def test_a_prepared_answer_says_it_was_prepared_and_then_checked_and_names_the_second_check(page, make):
    seen = watch(page)
    tok = make(); e = item(tok, "e1"); assert e["prepared"] is True
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    expect(page.get_by_test_id("how-prepared")).to_have_text("Prepared by our team; the second AI check then checked it against the quote.")
    code, ai, _ = rows(page)
    assert code.startswith("Passed:") and "word for word" in code, code
    assert page_verdict(page) == "Agrees" and "found every statement" in ai.lower(), ai
    assert page.get_by_test_id("how-ai-sub").inner_text().startswith("claude-haiku"), "the second check names its own model"
    page.get_by_test_id("how-all-checks").click()
    expect(page.get_by_test_id("how-all-list")).to_be_visible()
    assert page.get_by_test_id("how-all-list").locator("li").count() >= 5
    # an amount is code-made: no "prepared" line, but the same second check
    open_item(page, tok, "a1", step="bills"); wait_loaded(page); open_panel(page)
    assert page.get_by_test_id("how-prepared").count() == 0 and "amount appears in the record" in rows(page)[0]
    # a warning made by code needs no second check, and says why
    open_item(page, tok, "f_gap_r6_r7"); wait_loaded(page); open_panel(page)
    assert page_verdict(page) == "Not needed" and "worked out by code" in rows(page)[0]
    assert seen == [], seen


def test_your_decision_shows_in_the_you_row(page, make):
    seen = watch(page)
    tok = make(); open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "Waiting for you."
    page.get_by_test_id("answer-yes").click(); settle(page, 500)
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You kept it in the letter."
    page.get_by_test_id("answer-no").click(); settle(page, 500)
    open_item(page, tok, "e1"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You left it out of the letter."
    open_item(page, tok, "a1", step="bills"); page.get_by_test_id("answer-yes").click(); settle(page, 500)
    open_item(page, tok, "a1", step="bills"); wait_loaded(page); open_panel(page)
    assert rows(page)[2] == "You counted it in the bill total."
    assert seen == [], seen


# ------------------------------------------------------------------------------------------------ a dispute or a failed check is shown in words

def rewrite_trace(page, fn):
    def h(route):
        r = route.fetch(); j = r.json(); fn(j); route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+/items/e2/trace$"), h)


def test_a_disputed_item_shows_disputes_with_the_servers_reason_and_a_failed_code_check_says_what_failed(page, make):
    seen = watch(page)
    tok = make()
    def fn(j):
        for s in j["steps"]:
            if s["id"] == "judge_1":
                s["status"] = "fail"; s["evidence"].update(judge_verdict="partially", judge_reason_code="DROPS_QUALIFIER", rationale="The summary leaves out a qualifier that the quote carries.")
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:09.394Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def make\\|^def case\\|^def item\\|^def open_item\\|^def sized\\|^def settle\\|^def phone\" -A 14 tests/e2e/guided/test_step2.py | head -110",
 "description": "Read step2 test helpers for case creation and navigation"
}
````

### User / tool · 2026-11-03T13:14:09.475Z

**tool result**
````
19:def make():
20-    made = []
21-
22-    def _make(lib=None):
23-        import time
24-        st, c = C.api("POST", "/api/cases", {"sample": True} if lib is None else {"library": lib}); assert st in (200, 201), (st, c)
25-        tok = c["token"]; made.append(tok)
26-        assert C.api("POST", f"/api/cases/{tok}/run", {})[0] == 202
27-        for _ in range(300):
28-            s = C.api("GET", f"/api/cases/{tok}/status")[1]
29-            if s["status"] in ("ready", "failed"):
30-                break
31-            time.sleep(0.5)
32-        assert s["status"] == "ready", s
33-        return tok
--
39:def case(tok):
40-    return C.api("GET", f"/api/cases/{tok}")[1]
41-
42-
43:def item(tok, iid):
44-    c = case(tok)
45-    return next(i for g in ("entries", "undated_entries", "flags", "amounts", "tray") for i in c[g] if i["id"] == iid)
46-
47-
48:def open_item(page, tok, iid=None, step="timeline"):
49-    go(page, f"/case/{tok}/{step}" + (f"?item={iid}" if iid else ""))
50-    page.get_by_test_id("card-line").wait_for()
51-
52-
53-def line_id(page):
54-    return page.get_by_test_id("card-line").get_attribute("data-item-id")
55-
56-
57:def settle(page, ms=350):
58-    page.wait_for_timeout(ms)
59-
60-
61-@pytest.fixture
62:def phone(pw):
63-    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); pg = ctx.new_page()
64-    yield pg
65-    b.close()
66-
67-
68:def sized(pw, w, h):
69-    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}); return b, ctx.new_page()
70-
71-
72-# ------------------------------------------------------------------------------------------------ the screen
73-
74-def test_opens_on_the_first_item_with_the_record_words_beside_it(page, make):
75-    seen = watch(page)
76-    tok = make(); e1 = item(tok, "e1")
77-    go(page, f"/case/{tok}/timeline")
78-    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
79-    assert page.evaluate("location.search") == "?item=e1", "the open item is in the address, so a reload lands on it"
80-    assert page.get_by_test_id("item-count").inner_text() == "Item 1 of 19" and page.get_by_test_id("progress-text").inner_text() == "0 answered · 19 to go"
81-    assert page.get_by_test_id("line-text").inner_text() == e1["summary"]
82-    marks = page.locator("[data-testid=card-source] mark")
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:19.682Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux-probe.py",
 "content": "\"\"\"T-211 UX review probe: create the sample case (and library cases) over the API on the demo server, list every Step 2/3 item's judge verdict from its trace.\nUsage: python T-211-ux-probe.py <base> [lib ...]\"\"\"\nimport json, sys, time, urllib.request\n\nBASE = sys.argv[1]\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=60) as r:\n            return r.status, json.loads(r.read() or b\"{}\")\n    except urllib.error.HTTPError as e:\n        return e.code, json.loads(e.read() or b\"{}\")\n\n\ndef make(body):\n    st, c = api(\"POST\", \"/api/cases\", body)\n    if st not in (200, 201):\n        return None, (st, c)\n    tok = c[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(300):\n        s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s.get(\"status\") in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.5)\n    return tok, s\n\n\ndef summarize(tok):\n    c = api(\"GET\", f\"/api/cases/{tok}\")[1]\n    out = []\n    for g in (\"entries\", \"undated_entries\", \"flags\", \"amounts\", \"tray\"):\n        for i in c.get(g, []):\n            st, tr = api(\"GET\", f\"/api/cases/{tok}/items/{i['id']}/trace\")\n            j = None\n            for s in tr.get(\"steps\", []) if isinstance(tr, dict) else []:\n                ev = s.get(\"evidence\") or {}\n                if s.get(\"kind\") == \"llm\" and (ev.get(\"model\") or {}).get(\"role\") == \"judge\" or str(s.get(\"id\", \"\")).startswith(\"judge\"):\n                    j = (s.get(\"id\"), s.get(\"status\"), ev.get(\"judge_verdict\"), (ev.get(\"model\") or {}).get(\"id\"), (ev.get(\"model\") or {}).get(\"prepared\"), (ev.get(\"rationale\") or s.get(\"why\") or \"\")[:90])\n                    break\n            codes = [(s[\"id\"], s[\"status\"]) for s in (tr.get(\"steps\", []) if isinstance(tr, dict) else []) if s.get(\"kind\") == \"code\" and s.get(\"status\") in (\"pass\", \"fail\")]\n            out.append((g, i[\"id\"], i.get(\"state\"), i.get(\"prepared\"), j, [x for x in codes if x[1] == \"fail\"]))\n    return c, out\n\n\nif __name__ == \"__main__\":\n    targets = [{\"sample\": True}] + [{\"library\": x} for x in sys.argv[2:]]\n    for body in targets:\n        tok, s = make(body)\n        print(\"==\", body, tok, s if tok is None else s.get(\"status\"))\n        if not tok:\n            continue\n        c, out = summarize(tok)\n        print(\"TOKEN\", tok)\n        for row in out:\n            print(row)\n"
}
````

### User / tool · 2026-11-03T13:14:19.785Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:21.070Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7931/api/library | head -c 1500",
 "description": "List library cases available in demo"
}
````

### User / tool · 2026-11-03T13:14:21.157Z

**tool result**
````
{"error":{"code":"not_found","message":"Not found.","detail":{}}}
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:22.348Z

**tool call — Bash**
````
{
 "command": "grep -n \"library\" memory/contracts/api.md | head -12",
 "description": "Find library endpoint in API contract"
}
````

### User / tool · 2026-11-03T13:14:22.434Z

**tool result**
````
41:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
57:`local_mode` (T-197, additive): `true` only on the private local server (`ZLAYT_MODE=local`, same value that gates `GET /api/cases` and `GET /api/library`, which do not exist in public mode, D-008). The guided UI reads it on first paint and never probes those routes when it is `false`, so a public server sees no 404.
419:`POST .../items/{id}/review` with `{"action": "count", "confirm": "separate_charge"}` (an amount only; `400 bad_request` for an entry or flag, `409 item_rejected` for a rejected amount) counts a countable amount: it becomes class `charge` and is `accepted` in one step, so the letter total (R-EX-8) sums it like any accepted charge; no second AI check is asked (it is her decision with a named confirm: `judge_required_for_export: false`, `second_check_pending: false`, the trace's `judge_2` step is `skipped` with "you counted this line ... and confirmed it by name", `why` says so). Response: the review response shape (`item`, `totals`, `review`, `warnings`) plus `amount` (the case-view shape, `kind: "charge"`) and `reclassified: {from, to: "charge", counted: true, confirm: "separate_charge"}`. Errors, all `422` with `detail.reason_code` equal to the code and nothing changed: `NOT_COUNTABLE` (message "This amount cannot be counted. <not_counted_reason>"; `detail.not_counted_reason`; also for an amount that is already a charge: "This amount is already a charge. Accept it to count it."); `CONFIRM_REQUIRED` for a missing or wrong `confirm` (`detail: {flag: "separate_charge", name: "Counted as a separate charge", confirm_with: "separate_charge", message, not_counted_reason}`); `CONFIRM_REQUIRED` naming `likely_duplicate` or `likely_total` (send that flag as `confirm_flag`; `detail.flag`, `detail.confirm_with`, `detail.of` = the other amount's id): `likely_duplicate` when ANOTHER live amount of the case (any record, the same record too) that is an accepted or pending charge, or is itself countable, has the same amount and the same service and a compatible date; the service is normalized (round 3): codes meet, or the shorter description's words each have an equivalent in the other (word families and abbreviations: PT / physical therapy, pt / patient, xray / x-ray / radiograph, ther ex / therapeutic exercise, OV / office visit, e-stim, eval / exam), or a CPT code meets its description when the case itself states both on one line; a code the case never describes, against a described line at the same amount, is asked about (candidate, not decided). Over-flagging costs one more named confirm (a date is compared only when both lines state one; a line with no date of service may be the same visit as a dated one). `separate_charge` alone is never enough for a line that matches; both lines of a pair are flagged, and after one is counted the other matches an accepted charge. `likely_total` when the figure equals the sum of at least two other charges of its record. Every amount in `amounts[]` also carries `count_confirm`: `null`, or for a countable amount that would need such a flag `{flag, name, message, confirm_with, of}` (the same object the 422 `detail` carries), so the screen can show the warning before the click. A non-string `confirm` is `422 invalid_edit`. The charge then carries `flag: {flag: "separate_charge", name: "Counted as a separate charge", confirmed_at, ...}` (or the duplicate/total flag it was counted with); after a `reset` the next `accept` needs the flag's `confirm_with` again (`confirm_required: true`), a `dismiss` takes it out of the total, and a rerun keeps it. Audit (`GET .../audit`, also in public mode as metadata): two events for the item, in order: `action: "reclassify"` whose local-mode `after` is `{event: "count", kind: "charge", review_status: "accepted", confirm: {flag: "separate_charge", name, confirmed_at}, not_counted_reason, confirm_flag}` (`before: {kind, review_status, state}`) and, in `events[]`, `confirm: {flag: "separate_charge", name, confirmed_at}`; then the `accept` event, which carries the confirm of the flag the charge holds. `ladder.counted = {confirm, at, by: "reviewer", not_counted_reason}`; `ladder.code_checks.classified_by = "reviewer:counted"`. The internal notes' `AMOUNTS NOT TOTALED` list drops a counted amount. Balance wording (round 2): "Amount unpaid that the provider has a right to be paid: $2,660.00" says Balance (lib15 affidavit), not Payment. Checked on every library case, both by summing every countable amount and by counting each with only the named confirm: never exceeds the case's hand-verified `explicit_charges_total` (lib11: $3,260 + $250 + $180 + $2,310 = $6,000.00) and the adjuster's t140 ledgers (r1 to r3, restating labels) have no countable amount.
714:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
730:**Case titles (T-157).** `title` is what to show and is never "Untitled case": (1) the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped; a typed name keeps its words); (2) when the case has no name, or a name that is empty once cleaned (`case_01_`, `.txt`), the first record header: the provider (its Source line with any tags or angle brackets dropped, at most 60 characters) and that record's date, "Marrowgate General ED, Feb 14, 2026" ("Records from Feb 14, 2026" when the record has no Source line, the bare provider when it has no date); (3) when no record has either, "Records added Nov 2" ("Sample case" for the sample). `name` is the stored value, `null` until someone names the case. `PATCH /api/cases/{token}` with `{"title": "Rivera v. Acme"}` stores the name (same rule as on create: plain text, control characters removed, white space collapsed; a `<` or `>` or more than 120 characters is `422 invalid_title` and the stored name is unchanged) and answers `200 {token, name, title}`; a blank or `null` title clears the name, so the title returns to the derived default; a body without `title`, or a `title` that is neither text nor null, is `400 bad_request`; an unknown token is `404 not_found`. The name goes through the same readable-title step as any other, so underscores or a file extension in a typed title are shown as words. Allowed in public mode too (the token is the capability). A rename is not a review event. **A title is never markup:** a typed title is refused if it contains `<` or `>`, and a title derived from a record's Source line has its tags dropped, so `title` is always plain text and a client may still render it as text only (`textContent`), never as HTML.
732:**`next_action` (T-157).** The single first thing to do in the case, `{item_id, kind, reason}`, or `null` when nothing blocks the export and nothing waits for review. Code only; no model call; the same value in `GET /api/cases` and `GET /api/cases/{token}`. Order: (1) a case only ingested (not run) is `{item_id: null, kind: "run", reason: "Run the case to draft the timeline. ..."}`; (2) else the first export-gate blocker (`hitl.gate_blockers`, in the gate's order): `kind` and `item_id` are the blocker's (`kind: "case"` and `item_id: null` for a run in progress or failed; `entry|flag|amount` for a code-check failure or an accepted item whose second check never answered) and `reason` is its plain `why`; the `NOTHING_ACCEPTED` blocker, which names no item, yields to step 3 whenever an item waits, because deciding that item is what clears it; (3) else the first needs-review item that is still open (`state: needs_review` and `review_status: pending`, or an edit not yet confirmed), in timeline order: by the date of the record it cites (a flag citing several uses the earliest; undated last), then that record's position in the packet, then entry before flag before amount, then id; `kind` is `entry|flag|amount` and `reason` is the item's own `why`; (4) else `NOTHING_ACCEPTED` as a blocker if that is all that is left; (5) else `null`. Items the review counts leave out (a tray placeholder the paralegal answered, a rule-filtered proposal, a rejected item) are never named. After each decision the field moves to the next item. `tests/unit/test_case_list.py` compares it with GET case for every library case and checks the order rules. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `hitl.needs_review_open` (T-157 r3) is the number of items still open in Needs review: `state: needs_review` and (`review_status: pending` or an unconfirmed edit, `edit_to_check`), i.e. exactly the set `next_action` picks from and the items of `GET /api/cases/{token}` that wait for the paralegal; a reworded entry counts, an accepted item that is still `needs_review` does not (so it is at most `needs_review`). `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
733:`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
734:`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).
812:- **Eval.** `python -m evals.letter_check` (also a row and a blocker in `python -m evals.run`): the fixture-backend export of the sample, every golden case and every library packet has 0 currency strings outside BILLED CHARGES, 0 non-accepted amounts inside it, the exact total line, and (all charges dismissed) none anywhere. Round 4: it uses the same `money.py` detector as the hold and the gate, splits the letter by structure (`export.split_letter`), and counts a letter the gate blocks as a violation (`the export gate blocked this letter`).
861:- **T-177 r4 (D-069: templates by provenance, malformed means missing):** every user-facing string of a prepared item or case comes from a prepared-specific template chosen by the item's `prepared` field (or the case's `models.generator_prepared`); no AI sentence is rewritten afterwards. Consequences for payloads: (1) the word "AI" and any model name appear only in the badge tooltip sentence and in structured identity fields of the real second check (`models.judge`, judge call rows, `ladder.judge.model`); every sentence about the second check says "second check" on a prepared item or case (`why`, trace labels such as "Second check: is the summary supported by the quote?", blockers, warnings, 422 messages, the export notes line). (2) The trace step for a prepared answer is labelled "Prepared answer" with `why` "Prepared answer (hand-checked by the team for the demo)"; the D-065 "standing in for the AI draft" tail is gone (only the badge tooltip may say AI). The case-trace `extract` step is labelled "Prepared summaries and quotes for each record". (3) A malformed or empty prepared answer is treated as a missing one: the generator call is not retried, its `llm_calls` row reads `FIXTURE_MISS` with model `hand-checked (qa)`, the item is `rejected` with reason `FIXTURE_MISS` ("The demo has no prepared answer for this step, so this item has not been checked."), and the case's `models.generator` stays `hand-checked (qa)` / `generator_prepared: true` (also when no answer is usable at all, by the fixture set in use). (4) `ladder.translation.label` / `review_label` read "Prepared translation" / "Prepared translation — check against the original" on a prepared item; the export letter's bracketed note reads "[Prepared translation of the Spanish original; check before sending]". (5) `JUDGE_NOT_RUN` blockers carry `prepared: boolean` (the case's provenance) so the 422 headline can say "second check". (6) The export notes disclosure line for a prepared case reads "This chronology was built from answers the team prepared for this demo and checked by a second check; ...". (7) `GET /items/{id}` for a flag whose category is `llm_split` reads "Record boundaries chosen by a prepared answer" when prepared. Guard: tests/unit/test_prepared_property.py (fault-injected curated sets: valid, malformed, empty, missing; the sample and two library cases).
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:26.444Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-211-ux-probe.py http://127.0.0.1:7931",
 "description": "Probe sample case judge verdicts per item"
}
````

### User / tool · 2026-11-03T13:14:27.288Z

**tool result**
````
== {'sample': True} _Ls5whWrpNVOrL4rZvNoag ready
TOKEN _Ls5whWrpNVOrL4rZvNoag
('entries', 'e1', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e2', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e3', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e4', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e5', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e6', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e7', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e8', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e9', 'verified', False, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('flags', 'f_gap_r6_r7', 'verified', False, ('judge_not_needed', 'skipped', None, None, None, 'Not needed: this is arithmetic over dates in the record, which code does exactly.'), [])
('flags', 'f_accident_date_after_treatment_1_2_7', 'verified', False, ('judge_not_needed', 'skipped', None, None, None, 'Not needed: this is arithmetic over dates in the record, which code does exactly.'), [])
('flags', 'f_cx1', 'verified', False, ('judge_3', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the two quotes conflict.'), [])
('flags', 'f_r3_1', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r8_1', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r6_1', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r7_1', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r7_2', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r8_2', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r9_1', 'verified', False, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('amounts', 'a1', 'verified', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a2', 'needs_review', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a4', 'verified', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a3', 'needs_review', False, ('judge_2', 'skipped', None, None, None, 'Damages and other non-bill figures are not sent to the second check.'), [])
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:31.269Z

**tool call — Bash**
````
{
 "command": "lsof -nP -iTCP:7931 -sTCP:LISTEN",
 "description": "Find PID listening on port 7931"
}
````

### User / tool · 2026-11-03T13:14:31.422Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  32837 arsis    9u  IPv4 0x349f7602b0ec9e5e      0t0  TCP 127.0.0.1:7931 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:32.459Z

**tool call — Bash**
````
{
 "command": "kill 32837",
 "description": "Stop the first demo server"
}
````

### User / tool · 2026-11-03T13:14:32.537Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:42.499Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T211-cda2856 && LLM_BACKEND=fixture FIXTURE_SET=curated PORT=7932 HOST=127.0.0.1 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t211b.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t211b-app.log 2>&1",
 "description": "Start demo server as run.sh does on port 7932",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T13:14:42.575Z

**tool result**
````
Command running in background with ID: b20rd4ilg. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b20rd4ilg.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:43.303Z

**tool call — Bash**
````
{
 "command": "grep -n \"main\\|FIXTURE\\|environ\" app/main.py | head -20",
 "description": "Check whether app.main applies config defaults"
}
````

### User / tool · 2026-11-03T13:14:43.383Z

**tool result**
````
1:"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens).
14:    """uvicorn app.main:create --factory"""
23:def main():
25:    host, port = os.environ.get("HOST", "127.0.0.1"), int(os.environ.get("PORT", "7860"))
32:        if os.environ.get("ZLAYT_DEBUG") == "1":
41:if __name__ == "__main__":
42:    main()
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:46.190Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7932/api/health && echo && .venv/bin/python artifacts/review-evidence/T-211-ux-probe.py http://127.0.0.1:7932",
 "description": "Check health and probe sample case on curated demo server"
}
````

### User / tool · 2026-11-03T13:14:47.198Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":false,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
== {'sample': True} Vm6bPPGcHQU_lzc72hIugQ ready
TOKEN Vm6bPPGcHQU_lzc72hIugQ
('entries', 'e1', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e2', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e3', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e4', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e5', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e6', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e7', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e8', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('entries', 'e9', 'verified', True, ('judge_1', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check found every statement in the summary in the quote.'), [])
('flags', 'f_gap_r6_r7', 'verified', False, ('judge_not_needed', 'skipped', None, None, None, 'Not needed: this is arithmetic over dates in the record, which code does exactly.'), [])
('flags', 'f_accident_date_after_treatment_1_2_7', 'verified', False, ('judge_not_needed', 'skipped', None, None, None, 'Not needed: this is arithmetic over dates in the record, which code does exactly.'), [])
('flags', 'f_cx1', 'verified', False, ('judge_3', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the two quotes conflict.'), [])
('flags', 'f_r3_1', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r8_1', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r6_1', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r7_1', 'needs_review', True, ('judge_4', 'skipped', None, None, None, 'Not run: only the phrase list found this flag, so there is no prepared answer to double-ch'), [('agreement', 'fail')])
('flags', 'f_r7_2', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r8_2', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('flags', 'f_r9_1', 'verified', True, ('judge_4', 'pass', 'supported', 'claude-haiku-5-5', False, 'The second check agreed that the flag fits the quote.'), [])
('amounts', 'a1', 'verified', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a2', 'needs_review', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a4', 'verified', False, ('judge_2', 'pass', 'supported', 'claude-haiku-5-5', False, "The second check agreed with the rule's reading of this figure."), [])
('amounts', 'a3', 'needs_review', False, ('judge_2', 'skipped', None, None, None, 'Damages and other non-bill figures are not sent to the second check.'), [])
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:14:52.480Z

**tool call — Bash**
````
{
 "command": "git diff 82217e5~1 82217e5 -- app/frontend/guided/app.js app/frontend/guided/core.js app/frontend/guided/step2.js app/frontend/guided/step3.js app/frontend/guided/index.html",
 "description": "Show T-211 diff for app, core, step2, step3, index"
}
````

### User / tool · 2026-11-03T13:14:52.581Z

**tool result**
````
diff --git a/app/frontend/guided/app.js b/app/frontend/guided/app.js
index 25981a0..af4f2a3 100644
--- a/app/frontend/guided/app.js
+++ b/app/frontend/guided/app.js
@@ -8,6 +8,7 @@
      /case/<token>/timeline    G.pages.timeline  layout frame  (step 2; ?item=<id>; the done screen calls ctx.layout("page"))
      /case/<token>/bills       G.pages.bills     layout frame  (step 3; ?item=<id>; the done screen calls ctx.layout("page"))
      /case/<token>/letter      G.pages.letter    layout page   (step 4)
+     /how-it-works             G.pages.how       layout page   (T-211: "How each answer is checked"; linked from the header on every screen; no step bar)
    PAGE CONTRACT: G.pages.<name> = async (ctx) => optional cleanup function. Render into ctx.view (cleared; its children become children of <body> because .view is display:contents,
    so a frame page appends .titlebar, .work and .actions, a page-layout page appends one <main class="wrap">). Resolve when the first paint is done; the shell then sets data-ready on #view.
    ctx = { route, token, step, query (URLSearchParams), case (GET case JSON, null on home and /new), health, signal (aborts on navigation: pass it to fetch),
@@ -19,7 +20,7 @@
   const root = document.documentElement, body = document.body, view = $("#view"), bar = $("#step-bar"), list = $("#step-list"), headerEl = $("#header");
   const TITLE = "Treatment Timeline";
   const ROUTES = [
-    [/^\/$/, "home", 0], [/^\/new$/, "new", 1],
+    [/^\/$/, "home", 0], [/^\/new$/, "new", 1], [/^\/how-it-works$/, "how", 0],
     [/^\/case\/([^/]+)\/records$/, "records", 1], [/^\/case\/([^/]+)\/timeline$/, "timeline", 2], [/^\/case\/([^/]+)\/bills$/, "bills", 3], [/^\/case\/([^/]+)\/letter$/, "letter", 4],
   ];
   const FRAME = { timeline: true, bills: true };
@@ -63,7 +64,9 @@
       ? h("a", { class: "brand", href: "/", "data-testid": "brand" }, h("span", { class: "brand-mark", "aria-hidden": "true" }, "TT"), h("span", {}, "Treatment Timeline"))
       : [h("a", { class: "back-cases", href: "/", "data-testid": "btn-your-cases" }, h("span", { "aria-hidden": "true" }, "‹"), h("span", { class: "long" }, "Your cases"), h("span", { class: "short" }, "Cases")),
          h("div", { class: "hd-case" }, h("span", { class: "case-title", "data-testid": "case-title", title: t }, t), headerState.sub ? h("span", { class: "case-sub" }, headerState.sub) : null)];
-    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), themeButton());
+    const how = h("a", { class: "how-link", href: "/how-it-works", "data-testid": "link-how", "aria-current": now && now.name === "how" ? "page" : null },
+      h("span", { class: "long" }, "How each answer is checked"), h("span", { class: "short" }, "How it's checked"));      // T-211, D-074: on every screen
+    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), how, themeButton());
     themeLabel();
   }
   G.store.healthP = G.api.health();
@@ -96,7 +99,7 @@
     if (/^\/case\/[^/]+$/.test(path)) return { name: "redirect", token: decodeURIComponent(path.split("/")[2]) };
     return { name: "missing", step: 0, query: new URLSearchParams() };
   }
-  G.go = function (path, opts) { (opts && opts.replace ? history.replaceState : history.pushState).call(history, null, "", path); return render(); };
+  G.go = function (path, opts) { G.navigated = true; (opts && opts.replace ? history.replaceState : history.pushState).call(history, null, "", path); return render(); };
   G.route = () => now;
   function setLayout(mode) { body.classList.toggle("frame", mode === "frame"); body.classList.toggle("page", mode !== "frame"); }
 
diff --git a/app/frontend/guided/core.js b/app/frontend/guided/core.js
index ae5d6cf..b995631 100644
--- a/app/frontend/guided/core.js
+++ b/app/frontend/guided/core.js
@@ -77,6 +77,7 @@
     confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + enc(rid) + "/confirm_date", { date }),
     rejudge: (token) => call("POST", t(token) + "/rejudge"),
     trace: (token, s) => call("GET", t(token) + "/trace", null, s),
+    itemTrace: (token, id, s) => call("GET", t(token) + "/items/" + enc(id) + "/trace", null, s),          // T-211: the per-item check trace ("How this was checked")
     exportCase: (token, s) => call("GET", t(token) + "/export", null, s),
   };
 
diff --git a/app/frontend/guided/index.html b/app/frontend/guided/index.html
index aa91331..a77e78b 100644
--- a/app/frontend/guided/index.html
+++ b/app/frontend/guided/index.html
@@ -12,6 +12,7 @@
 <link rel="stylesheet" href="/step2.css">
 <link rel="stylesheet" href="/step3.css">
 <link rel="stylesheet" href="/step4.css">
+<link rel="stylesheet" href="/how.css">
 </head>
 <body class="page">
 <a class="skip" href="#view" data-testid="skip-main">Skip to the main content</a>
@@ -30,6 +31,7 @@
 <script src="/step2.js"></script>
 <script src="/step3.js"></script>
 <script src="/step4.js"></script>
+<script src="/how.js"></script>
 <script src="/app.js"></script>
 </body>
 </html>
diff --git a/app/frontend/guided/step2.js b/app/frontend/guided/step2.js
index f13e38c..e099851 100644
--- a/app/frontend/guided/step2.js
+++ b/app/frontend/guided/step2.js
@@ -193,7 +193,7 @@
       });
     };
     return {
-      tag: { cls: "you", text: "Your wording" }, sub: lineHead(item, rec), focus: "field",
+      tag: { cls: "you", text: "Your wording" }, sub: lineHead(item, rec), focus: "field", how: false,
       body: [h("p", { class: "muted fix-hint" }, "Change the line so it says only what the highlighted words say. Numbers, left or right, and words like “no” or “possible” must match."), ta],
       foot: { cls: "plain", nodes: [R.plain(item.why)] },
       question: "Change the line, then save it.",
@@ -259,7 +259,7 @@
     if (noteMode) {
       const ta = h("textarea", { class: "edit", "data-testid": "edit-note", "aria-label": "Your note for the attorney", "data-autofocus": "" });
       ta.value = ui.draft != null ? ui.draft : item.reviewer_note || ""; ta.addEventListener("input", () => { ui.draft = ta.value; });
-      return { ...tags, focus: "field", body: [h("p", { class: "warn-title" }, "Add a note for the attorney"), ta],
+      return { ...tags, focus: "field", how: false, body: [h("p", { class: "warn-title" }, "Add a note for the attorney"), ta],
         foot: { cls: "plain", nodes: ["Your note goes in the notes for the attorney, next to this warning. It never goes in the letter."] },
         question: "Write your note, then save it.",
         yes: { label: "Save note", run: () => { const note = (ui.draft != null ? ui.draft : "").trim(); if (!note) { S.err = { text: "Write the note first." }; S.render(true); return undefined; } return S.decide(item, "edit", { edits: { note } }); } },
@@ -300,7 +300,7 @@
           S.render(false);
         });
       };
-      return { tag: { cls: "you", text: "Written by you" }, sub: recLabel(rec), focus: "field",
+      return { tag: { cls: "you", text: "Written by you" }, sub: recLabel(rec), focus: "field", how: false,
         body: [h("label", { class: "sr", for: "mine" }, "Your line for the timeline"), ta],
         foot: { cls: "plain", nodes: ["Use only what the chosen sentences say. Numbers, left or right, and words like “no” or “possible” must match."] },
         question: "Write the line for the timeline, then save it.",
@@ -327,6 +327,15 @@
       src: { head: recs.length ? headFor(recs) : "", nodes: sourceFor(S, recs, [], { uncovered: false }) } };
   }
 
+  /* T-211: the "You" row of "How this was checked": her decision in words (null = no decision yet) */
+  function youText(S, item) {
+    const st = item.review_status, flag = groupOf(S.c, item) === "flag" || item.kind === "flag" || !!item.type, tray = groupOf(S.c, item) === "tray";
+    if (item.edit_to_check || !st || st === "pending") return null;
+    if (st === "dismissed") return tray ? "You skipped it." : flag ? "You said the attorney does not need to be told." : "You left it out of the letter.";
+    if (st === "edited") return flag ? "You added a note. The attorney will be told." : "You wrote your own wording and kept it in the letter.";
+    return flag ? "You said the attorney should be told." : "You kept it in the letter.";
+  }
+
   /* what the Saved line says */
   function statusFor(S, item, resp, action) {
     const q = S.queue.find((x) => x.id === (item && item.id)), flag = !!(item && (item.type || item.kind === "flag"));
@@ -381,7 +390,7 @@
   }
 
   G.pages.timeline = function (ctx) {
-    return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find, present, statusFor, done, empty });
+    return R.run(ctx, { step: 2, title: "Check the timeline", unit: "Item", chip: false, buildQueue, find, present, statusFor, done, empty, youText });
   };
   G.step2 = { buildQueue, find, flagHeading, outsideParts };
 })();
diff --git a/app/frontend/guided/step3.js b/app/frontend/guided/step3.js
index ecea33d..d6259c1 100644
--- a/app/frontend/guided/step3.js
+++ b/app/frontend/guided/step3.js
@@ -21,7 +21,9 @@
   /* T-206: a record's date is shown bare only when it is a certain service date. An amount with no service_date of its own (a ledger line not counted yet, a UB-04 or invoice total) never has one: a bill document's date is its statement's. */
   const BILL_DOC = /\b(ledger|invoice|statement|UB-?04|CMS-?1500|HCFA|EOB|explanation of benefits|itemi[sz]ed|billing|bill)\b/i;
   const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
-  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? "statement dated " + d : d) : "no date"; };
+  /* T-211 (T-202 r6): service_date.date_label says what the record's date is called: "statement" for a bill, "record" for any other record. No service_date (a ledger line not counted yet) is a bill document's: "statement". */
+  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
+  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? st + " dated " + d : d) : "no date"; };      // st: false, or the word "statement" | "record"
   const recLabel = (r, st) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, st)}`;
   const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
   const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
@@ -30,22 +32,22 @@
   /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
   const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
     /^date of service/i.test(sd.text || "") ? null : h("span", { class: "label-cap" }, "Date of service "), h("b", { "data-testid": "service-date-text" }, sd.text || ""),
-    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.statement_date_iso)}`) : null);
+    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
   const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
   /* T-206/T-209 r3: the note above states the specific reason; this sentence is the same for every reason that is not certain, so it can never contradict the note: find the date outside this card's guess, write it in the letter's blank. The card has no control to type a date. */
   const confirmNext = (sd) => {
-    const stmt = /\(statement dated/.test((sd && sd.text) || "") ? " The date in parentheses is the statement date, not the service date." : "";
+    const paren = /\((statement|record) dated/.exec((sd && sd.text) || ""), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : "";
     return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
       " Counting it adds the amount to the bill total.");
   };
 
   function present(S, item) {
     const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
-    const sd = sdOf(item), st = stmtDated(item, sd, rec);
+    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);
     const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
-    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r)) : null }));
+    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r) && dateWord(sd)) : null }));
     const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
-    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
+    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? st + " dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
     const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
     const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
     const flag = item.flag && item.confirm_required ? item.flag : null;
@@ -98,6 +100,14 @@
       no: { label: "No, leave it out", run: () => S.decide(item, "dismiss") }, third: null };
   }
 
+  /* T-211: the "You" row of "How this was checked" (null = no decision yet) */
+  function youText(S, item) {
+    const st = item.review_status, k = kindOf(item);
+    if (!st || st === "pending") return null;
+    if (st === "dismissed") return k === "charge" ? "You chose not to count it." : k === "count" ? "You left it out of the notes." : "You left it out of the notes for the attorney.";
+    return k === "charge" ? "You counted it in the bill total." : k === "count" ? "You did not count it. It is noted for the attorney." : "You listed it in the notes for the attorney. It is never added to the total.";
+  }
+
   function statusFor(S, item, resp, action) {
     const f = item ? figure(item) : "this amount", kind = item ? kindOf(item) : "never";
     if (action === "count") return `${f} counted in the bill total`;
@@ -148,6 +158,6 @@
   }
 
   G.pages.bills = function (ctx) {
-    return R.run(ctx, { step: 3, title: "Check the bills", unit: "Amount", chip: true, buildQueue, find, present, statusFor, done, empty });
+    return R.run(ctx, { step: 3, title: "Check the bills", unit: "Amount", chip: true, buildQueue, find, present, statusFor, done, empty, youText });
   };
 })();
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:15:10.648Z

**tool call — Bash**
````
{
 "command": "cat app/frontend/guided/how.css; grep -n \"how-link\\|\\.short\\|\\.long\" app/frontend/guided/*.css | head -20; grep -n \"def go\\|def watch\" -A 10 tests/e2e/guided/test_shell_smoke.py | head -30",
 "description": "Read how.css, header link CSS and go/watch helpers"
}
````

### User / tool · 2026-11-03T13:15:10.747Z

**tool result**
````
/* T-211 (D-074): the header link, the "How this was checked" panel on Step 2 and 3 items, and the "How each answer is checked" page. OWNER: frontend. Loaded last. Tokens only; no inline styles. */

/* ---------- header link (every screen) ---------- */
.how-link { display: inline-flex; align-items: center; height: 44px; padding: 0 14px; border-radius: 10px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text);
  font: 600 .9375rem var(--font); text-decoration: none; white-space: nowrap; flex: none; }
.how-link:hover { background: var(--sunken); }
.how-link[aria-current="page"] { border-color: var(--accent); background: var(--accent-soft); }
.how-link .short { display: none; }
@media (max-width: 1100px) { .how-link .long { display: none; } .how-link .short { display: inline; } }
@media (max-width: 760px) { .how-link { height: 40px; padding: 0 10px; font-size: .875rem; } }

/* ---------- the panel: three rows ---------- */
.how { flex: none; border-top: 1px solid var(--border); background: var(--sunken); font-size: .875rem; line-height: 1.25rem; color: var(--text); }
.how > summary { list-style: none; cursor: pointer; display: flex; align-items: center; gap: 8px 12px; flex-wrap: wrap; padding: 6px 24px; min-height: 34px; }
.how > summary::-webkit-details-marker { display: none; }
.how > summary::before { content: "\25B8"; color: var(--muted); flex: none; font-size: .875rem; }
.how[open] > summary::before { content: "\25BE"; }
.how-t { font-weight: 700; font-size: .9375rem; }
.how-chips { display: inline-flex; gap: 6px; flex-wrap: wrap; }
.how[open] .how-chips { display: none; }
.hchip { display: inline-flex; align-items: center; height: 24px; padding: 0 10px; border-radius: 999px; font-size: .8125rem; font-weight: 700; white-space: nowrap; background: var(--panel); border: 1px solid var(--border); color: var(--muted); }
.hchip.ok { background: var(--ok-bg); color: var(--ok); border-color: transparent; }
.hchip.bad { background: var(--bad-bg); color: var(--bad); border-color: transparent; }
.hchip.warn, .hchip.wait { background: var(--warn-bg); color: var(--warn); border-color: var(--warn-edge); }
.how-rows { padding: 0 24px 8px; display: grid; gap: 4px; }
.how-r { display: grid; grid-template-columns: 8.5rem minmax(0, 1fr); gap: 4px 14px; align-items: start; }
.how-l b { display: block; font-weight: 700; }
.how-sub { display: block; font-size: .75rem; line-height: 1rem; color: var(--muted); overflow-wrap: anywhere; }
.how-v { color: var(--text); overflow-wrap: anywhere; min-height: 1.25rem; }
@media (min-width: 761px) { .how-r[data-testid="how-code"] .how-v { min-height: 2.5rem; } .how-r[data-testid="how-ai"] .how-v { min-height: 3.75rem; } }      /* the rows keep their height while the trace loads and from item to item */
.how-v p { margin: 0; }
.how-v p + p { margin-top: 2px; }
.how-lead { font-weight: 600; }
.how-verdict { font-weight: 800; }
.how-verdict.ok { color: var(--ok); }
.how-verdict.bad { color: var(--bad); }
.how-verdict.warn { color: var(--warn); }
.how-r[data-state="bad"] > .how-v { color: var(--bad); font-weight: 600; }
.how-more { display: inline; border: 0; background: transparent; padding: 0; color: var(--accent); font: 600 .875rem var(--font); cursor: pointer; text-decoration: underline; }
.how-all { list-style: none; margin: 4px 0 0; padding: 0; font-size: .875rem; line-height: 1.25rem; color: var(--muted); }
.how-all li.ok span:first-child { color: var(--ok); font-weight: 800; }
.how-all li.bad { color: var(--bad); }

@media (max-width: 760px) {
  .how > summary { padding: 6px 14px; min-height: 36px; gap: 4px 8px; }
  .how-t { font-size: .8125rem; }
  .hchip { height: 22px; padding: 0 8px; font-size: .75rem; }
  .how-rows { padding: 0 14px 8px; font-size: .875rem; line-height: 1.25rem; }
  .how-r { grid-template-columns: 5.75rem minmax(0, 1fr); gap: 2px 8px; }
}

/* ---------- the page ---------- */
.how-page .how-steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }
.how-page .how-steps li { display: grid; grid-template-columns: 40px minmax(0, 1fr); gap: 14px; align-items: start; }
.how-n { width: 36px; height: 36px; border-radius: 50%; background: var(--accent); color: var(--on-accent); display: grid; place-items: center; font-weight: 800; }
.how-page .how-note { margin-top: 16px; font-size: 1rem; line-height: 1.5rem; }
.how-fig { overflow-x: auto; border: 1px solid var(--border); border-radius: 12px; background: #fff; margin-top: 8px; }
.how-fig img { display: block; width: 100%; height: auto; min-width: 640px; max-width: 820px; margin: 0 auto; }
.how-cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-top: 8px; }
.how-cols h3 { font-size: 1.0625rem; margin-bottom: 6px; }
.how-cols ul, .how-repo { margin: 0; padding-left: 20px; display: grid; gap: 6px; }
.how-repo code, .how-page code { font: 600 .9375em ui-monospace, SFMono-Regular, Menlo, monospace; background: var(--sunken); padding: 1px 6px; border-radius: 6px; overflow-wrap: anywhere; }
@media (max-width: 760px) {
  .how-cols { grid-template-columns: 1fr; gap: 16px; }
  .how-page .page-h { flex-direction: column; align-items: stretch; }
  .how-page .page-h .btn { align-self: flex-start; }
}

/* the header has one more control now: on a phone the brand name gives way before anything runs past the edge */
@media (max-width: 760px) {
  .header .brand { min-width: 0; flex: 0 1 auto; }
  .header .brand span:last-child { overflow: hidden; text-overflow: ellipsis; }
  .header .how-link { flex: none; }
  .header .case-title { flex: 1 1 0; }
}
app/frontend/guided/how.css:4:.how-link { display: inline-flex; align-items: center; height: 44px; padding: 0 14px; border-radius: 10px; border: 1px solid var(--border-strong); background: var(--panel); color: var(--text);
app/frontend/guided/how.css:6:.how-link:hover { background: var(--sunken); }
app/frontend/guided/how.css:7:.how-link[aria-current="page"] { border-color: var(--accent); background: var(--accent-soft); }
app/frontend/guided/how.css:8:.how-link .short { display: none; }
app/frontend/guided/how.css:9:@media (max-width: 1100px) { .how-link .long { display: none; } .how-link .short { display: inline; } }
app/frontend/guided/how.css:10:@media (max-width: 760px) { .how-link { height: 40px; padding: 0 10px; font-size: .875rem; } }
app/frontend/guided/how.css:73:  .header .how-link { flex: none; }
app/frontend/guided/styles.css:69:.back-cases .short { display: none; }
app/frontend/guided/styles.css:91:.step .st-label .short { display: none; }
app/frontend/guided/styles.css:332:  .back-cases .long { display: none; }
app/frontend/guided/styles.css:333:  .back-cases .short { display: inline; }
app/frontend/guided/styles.css:344:  .step .st-label .long { display: none; }
app/frontend/guided/styles.css:345:  .step .st-label .short { display: inline; }
20:def watch(page, allow_404=()):
21-    """pageerror, console.error, failed requests (an asset 404 counts) and window.onerror / unhandledrejection (a hook that runs before any page script). Returns the list to assert empty."""
22-    seen = []
23-    page.add_init_script(HOOK)
24-    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
25-    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" and not any(a in m.text for a in allow_404) else None)
26-    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url for a in allow_404) else None)
27-    page.on("requestfailed", lambda r: seen.append("requestfailed: " + r.url) if "ERR_ABORTED" not in (r.failure or "") else None)      # a fetch the app aborted on purpose when she moved on is not a failure
28-    return seen
29-
30-
31:def go(page, path="/"):
32-    page.goto(C.SERVER + path)
33-    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)
34-
35-
36-def rect(page, sel):
37-    return page.evaluate("(s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); }", sel)
38-
39-
40-def chrome(page):
41-    return {s: rect(page, s) for s in CHROME}
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:15:36.256Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux-measure.py",
 "content": "\"\"\"T-211 UX review: walk every Step 2/3 item of the sample case at several sizes, measure the \"How this was checked\" panel and screenshot it; then the How page.\nUsage: python T-211-ux-measure.py <base> <outdir>\"\"\"\nimport json, os, sys, time, urllib.request\nfrom playwright.sync_api import sync_playwright\n\nBASE, OUT = sys.argv[1], sys.argv[2]\nos.makedirs(OUT, exist_ok=True)\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None, headers={\"Content-Type\": \"application/json\"})\n    with urllib.request.urlopen(req, timeout=60) as r:\n        return json.loads(r.read() or b\"{}\")\n\n\ndef make():\n    tok = api(\"POST\", \"/api/cases\", {\"sample\": True})[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(300):\n        if api(\"GET\", f\"/api/cases/{tok}/status\").get(\"status\") in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.5)\n    return tok\n\n\ndef go(pg, path):\n    pg.goto(BASE + path)\n    pg.locator(\"[data-testid=view][data-ready]\").wait_for(state=\"attached\", timeout=15000)\n\n\nMEASURE = \"\"\"() => {\n  const q = (t) => document.querySelector(`[data-testid=${t}]`);\n  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); return [Math.round(b.x), Math.round(b.y), Math.round(b.width), Math.round(b.height)]; };\n  const how = q('how-checked'), sum = q('how-summary'), bar = q('actions'), line = q('card-line'), src = q('card-source');\n  const marks = [...document.querySelectorAll('[data-testid=card-source] mark')];\n  const sb = src ? src.getBoundingClientRect() : null;\n  const marksIn = sb ? marks.filter(m => { const b = m.getBoundingClientRect(); return b.top >= sb.top - 1 && b.bottom <= sb.bottom + 1; }).length : 0;\n  const barTop = bar ? bar.getBoundingClientRect().top : innerHeight;\n  const sumR = sum ? sum.getBoundingClientRect() : null;\n  return {\n    item: line && line.dataset.itemId, open: how && how.open, hidden: how && how.hidden, parent: how && how.parentNode && how.parentNode.dataset.testid,\n    how: r(how), summary: r(sum), barTop: Math.round(barTop),\n    summaryInView: !!sumR && sumR.top >= 0 && sumR.bottom <= barTop && sumR.height > 0,\n    chips: [...document.querySelectorAll('[data-testid^=how-chip-]')].map(c => c.textContent),\n    code: (q('how-code-text') || {}).innerText, ai: (q('how-ai-text') || {}).innerText, you: (q('how-you-text') || {}).innerText, aiSub: (q('how-ai-sub') || {}).innerText,\n    marks: marks.length, marksIn, yes: r(q('answer-yes')), lineCard: r(line), lineScrollH: line && line.scrollHeight, lineClientH: line && line.clientHeight,\n    docScroll: document.documentElement.scrollHeight > innerHeight, hScroll: document.documentElement.scrollWidth > innerWidth,\n    tag: (q('line-tag') || {}).innerText, foot: (q('card-foot') || {}).innerText,\n  };\n}\"\"\"\n\n\ndef walk(pw, tok, w, h, label, mobile=False, shots=()):\n    b = pw.chromium.launch()\n    ctx = b.new_context(viewport={\"width\": w, \"height\": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=1)\n    pg = ctx.new_page()\n    errs = []\n    pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n    pg.on(\"console\", lambda m: errs.append(m.text) if m.type == \"error\" else None)\n    c = api(\"GET\", f\"/api/cases/{tok}\")\n    steps = [(\"timeline\", i[\"id\"]) for g in (\"entries\", \"undated_entries\", \"flags\") for i in c[g]] + [(\"bills\", a[\"id\"]) for a in c[\"amounts\"]]\n    rows = []\n    for step, iid in steps:\n        go(pg, f\"/case/{tok}/{step}?item={iid}\")\n        pg.get_by_test_id(\"card-line\").wait_for()\n        try:\n            pg.wait_for_function(\"() => { const e = document.querySelector('[data-testid=how-checked]'); return e && e.getAttribute('aria-busy') !== 'true'; }\", timeout=10000)\n        except Exception as e:\n            errs.append(f\"{iid}: busy {e}\")\n        pg.wait_for_timeout(250)\n        m = pg.evaluate(MEASURE)\n        m[\"step\"] = step\n        rows.append(m)\n        if iid in shots:\n            pg.screenshot(path=f\"{OUT}/{label}-{iid}.png\")\n            if not m[\"open\"]:\n                pg.get_by_test_id(\"how-summary\").click(); pg.wait_for_timeout(300)\n                m2 = pg.evaluate(MEASURE); m2[\"after_open\"] = True; m2[\"step\"] = step; rows.append(m2)\n                pg.screenshot(path=f\"{OUT}/{label}-{iid}-opened.png\")\n                pg.get_by_test_id(\"how-summary\").click(); pg.wait_for_timeout(200)       # put it back so the rest of the walk keeps the default\n    b.close()\n    return rows, errs\n\n\ndef how_page(pw, w, h, label, mobile=False):\n    b = pw.chromium.launch()\n    ctx = b.new_context(viewport={\"width\": w, \"height\": h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=1)\n    pg = ctx.new_page(); errs = []\n    pg.on(\"pageerror\", lambda e: errs.append(str(e)))\n    pg.on(\"console\", lambda m: errs.append(m.text) if m.type == \"error\" else None)\n    go(pg, \"/\")\n    pg.screenshot(path=f\"{OUT}/{label}-home.png\")\n    link = pg.get_by_test_id(\"link-how\")\n    info = {\"link_text\": link.inner_text(), \"link_box\": link.bounding_box()}\n    link.click(); pg.get_by_test_id(\"how-page\").wait_for()\n    pg.screenshot(path=f\"{OUT}/{label}-how-fold.png\")\n    pg.screenshot(path=f\"{OUT}/{label}-how-full.png\", full_page=True)\n    info.update(pg.evaluate(\"\"\"() => { const m = document.querySelector('[data-testid=how-page]'); const t = m.innerText; const words = t.split(/\\\\s+/).filter(Boolean).length;\n      const img = document.querySelector('[data-testid=how-ladder-img]'), fig = img.closest('.how-fig'), ib = img.getBoundingClientRect(), steps = document.querySelector('[data-testid=how-steps]').getBoundingClientRect();\n      return { words, title: document.title, imgW: Math.round(ib.width), figW: fig.clientWidth, figScrollW: fig.scrollWidth, imgTop: Math.round(ib.top), stepsBottom: Math.round(steps.bottom),\n        hScroll: document.documentElement.scrollWidth > innerWidth, docH: document.documentElement.scrollHeight, imgLoaded: img.complete && img.naturalWidth > 0,\n        steps: [...document.querySelectorAll('[data-testid^=how-step-]')].map(s => s.innerText) }; }\"\"\"))\n    pg.get_by_test_id(\"how-back\").click(); pg.wait_for_timeout(500)\n    info[\"back_to\"] = pg.evaluate(\"location.pathname\")\n    b.close()\n    return info, errs\n\n\nif __name__ == \"__main__\":\n    tok = make()\n    res = {\"token\": tok}\n    shots = (\"e1\", \"f_gap_r6_r7\", \"f_cx1\", \"f_r7_1\", \"a2\", \"a3\")\n    with sync_playwright() as pw:\n        for (w, h, mob) in ((1440, 900, False), (390, 844, True), (1366, 768, False)):\n            label = f\"{w}x{h}\"\n            rows, errs = walk(pw, tok, w, h, label, mob, shots)\n            res[label] = {\"rows\": rows, \"errs\": errs}\n            info, e2 = how_page(pw, w, h, label, mob)\n            res[label + \"-how\"] = {\"info\": info, \"errs\": e2}\n    json.dump(res, open(f\"{OUT}/measure.json\", \"w\"), indent=1)\n    for k, v in res.items():\n        if k == \"token\":\n            continue\n        if \"rows\" in v:\n            print(\"==\", k, \"errs\", v[\"errs\"])\n            for m in v[\"rows\"]:\n                print(m[\"step\"], m[\"item\"], \"open\" if m[\"open\"] else \"closed\", \"inview\" if m[\"summaryInView\"] else \"NOT-IN-VIEW\", \"sum\", m[\"summary\"], \"bar\", m[\"barTop\"],\n                      \"marks\", f\"{m['marksIn']}/{m['marks']}\", \"yes\", m[\"yes\"], \"line\", m[\"lineScrollH\"], m[\"lineClientH\"], \"docScroll\" if m[\"docScroll\"] else \"\", \"after\" if m.get(\"after_open\") else \"\")\n        else:\n            print(\"==\", k, v)\n"
}
````

### User / tool · 2026-11-03T13:15:36.347Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux-measure.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:15:37.496Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-211-ux-measure.py http://127.0.0.1:7932 artifacts/review-evidence/T-211-ux",
 "description": "Run measurement walk at three sizes plus How page",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T13:16:12.361Z

**tool result**
````
== 1440x900 errs []
timeline e1 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e2 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e3 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e4 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e5 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e6 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e7 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e8 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline e9 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_gap_r6_r7 closed inview sum [33, 672, 667, 36] bar 729 marks 4/4 yes [32, 782, 270, 56] line 415 415  
timeline f_gap_r6_r7 open inview sum [33, 538, 667, 34] bar 729 marks 2/4 yes [32, 782, 270, 56] line 415 415  after
timeline f_accident_date_after_treatment_1_2_7 closed inview sum [33, 672, 667, 36] bar 729 marks 3/3 yes [32, 782, 270, 56] line 415 415  
timeline f_cx1 closed inview sum [33, 672, 667, 36] bar 729 marks 2/2 yes [32, 782, 270, 56] line 415 415  
timeline f_cx1 open inview sum [33, 538, 667, 34] bar 729 marks 1/2 yes [32, 782, 270, 56] line 415 415  after
timeline f_r3_1 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r8_1 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r6_1 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r7_1 open inview sum [33, 516, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r7_2 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r8_2 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
timeline f_r9_1 open inview sum [33, 536, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
bills a1 open inview sum [33, 538, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
bills a2 open inview sum [33, 538, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
bills a4 open inview sum [33, 538, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
bills a3 open inview sum [33, 538, 667, 34] bar 729 marks 1/1 yes [32, 782, 270, 56] line 415 415  
== 1440x900-how {'info': {'link_text': 'How each answer is checked', 'link_box': {'x': 1017.3125, 'y': 41.5, 'width': 235.6875, 'height': 44}, 'words': 412, 'title': 'How each answer is checked – Treatment Timeline', 'imgW': 820, 'figW': 1056, 'figScrollW': 1056, 'imgTop': 682, 'stepsBottom': 497, 'hScroll': False, 'docH': 2260, 'imgLoaded': True, 'steps': ['1\nPrepared by our team. In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from.', '2\nCode checks it. Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone.', '3\nA second AI checks it. A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote.', '4\nYou decide. You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.'], 'back_to': '/'}, 'errs': []}
== 390x844 errs []
timeline e1 closed NOT-IN-VIEW sum [17, 737, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 362 216  
timeline e1 open inview sum [17, 591, 356, 36] bar 659 marks 1/1 yes [12, 708, 178, 50] line 558 216  after
timeline e2 closed NOT-IN-VIEW sum [17, 761, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 386 216  
timeline e3 closed NOT-IN-VIEW sum [17, 713, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 338 216  
timeline e4 closed NOT-IN-VIEW sum [17, 689, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 314 216  
timeline e5 closed NOT-IN-VIEW sum [17, 665, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 290 216  
timeline e6 closed NOT-IN-VIEW sum [17, 689, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 314 216  
timeline e7 closed NOT-IN-VIEW sum [17, 689, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 314 216  
timeline e8 closed NOT-IN-VIEW sum [17, 737, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 362 216  
timeline e9 closed NOT-IN-VIEW sum [17, 713, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 338 216  
timeline f_gap_r6_r7 closed NOT-IN-VIEW sum [17, 690, 356, 58] bar 659 marks 3/4 yes [12, 708, 178, 50] line 315 216  
timeline f_gap_r6_r7 open inview sum [17, 591, 356, 36] bar 659 marks 3/4 yes [12, 708, 178, 50] line 481 216  after
timeline f_accident_date_after_treatment_1_2_7 closed NOT-IN-VIEW sum [17, 826, 356, 58] bar 659 marks 2/3 yes [12, 708, 178, 50] line 451 216  
timeline f_cx1 closed NOT-IN-VIEW sum [17, 735, 356, 58] bar 659 marks 2/2 yes [12, 708, 178, 50] line 359 216  
timeline f_cx1 open inview sum [17, 592, 356, 36] bar 659 marks 2/2 yes [12, 708, 178, 50] line 485 216  after
timeline f_r3_1 closed NOT-IN-VIEW sum [17, 767, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 391 216  
timeline f_r8_1 closed NOT-IN-VIEW sum [17, 745, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 369 216  
timeline f_r6_1 closed NOT-IN-VIEW sum [17, 767, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 391 216  
timeline f_r7_1 closed NOT-IN-VIEW sum [17, 745, 356, 86] bar 659 marks 1/1 yes [12, 708, 178, 50] line 397 216  
timeline f_r7_1 open inview sum [17, 564, 356, 36] bar 659 marks 1/1 yes [12, 708, 178, 50] line 625 216  after
timeline f_r7_2 closed NOT-IN-VIEW sum [17, 722, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 347 216  
timeline f_r8_2 closed NOT-IN-VIEW sum [17, 722, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 347 216  
timeline f_r9_1 closed NOT-IN-VIEW sum [17, 791, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 415 216  
bills a1 closed NOT-IN-VIEW sum [17, 712, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 336 216  
bills a2 closed NOT-IN-VIEW sum [17, 676, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 300 216  
bills a2 open inview sum [17, 592, 356, 36] bar 659 marks 1/1 yes [12, 708, 178, 50] line 446 216  after
bills a4 closed NOT-IN-VIEW sum [17, 972, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 597 216  
bills a3 closed NOT-IN-VIEW sum [17, 706, 356, 58] bar 659 marks 1/1 yes [12, 708, 178, 50] line 331 216  
bills a3 open inview sum [17, 591, 356, 36] bar 659 marks 1/1 yes [12, 708, 178, 50] line 477 216  after
== 390x844-how {'info': {'link_text': "How it's checked", 'link_box': {'x': 189.75, 'y': 49.5, 'width': 137.375, 'height': 40}, 'words': 412, 'title': 'How each answer is checked – Treatment Timeline', 'imgW': 640, 'figW': 318, 'figScrollW': 640, 'imgTop': 1231, 'stepsBottom': 1018, 'hScroll': False, 'docH': 3248, 'imgLoaded': True, 'steps': ['1\nPrepared by our team. In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from.', '2\nCode checks it. Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone.', '3\nA second AI checks it. A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote.', '4\nYou decide. You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.'], 'back_to': '/'}, 'errs': []}
== 1366x768 errs []
timeline e1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e1 open inview sum [33, 396, 630, 34] bar 609 marks 0/1 yes [32, 656, 270, 56] line 327 327  after
timeline e2 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e3 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e4 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e5 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e6 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e7 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e8 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline e9 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_gap_r6_r7 closed inview sum [33, 552, 630, 36] bar 609 marks 4/4 yes [32, 656, 270, 56] line 327 327  
timeline f_gap_r6_r7 open inview sum [33, 418, 630, 34] bar 609 marks 1/4 yes [32, 656, 270, 56] line 327 327  after
timeline f_accident_date_after_treatment_1_2_7 closed inview sum [33, 552, 630, 36] bar 609 marks 2/3 yes [32, 656, 270, 56] line 327 327  
timeline f_cx1 closed inview sum [33, 552, 630, 36] bar 609 marks 2/2 yes [32, 656, 270, 56] line 327 327  
timeline f_cx1 open inview sum [33, 418, 630, 34] bar 609 marks 0/2 yes [32, 656, 270, 56] line 327 327  after
timeline f_r3_1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r8_1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r6_1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r7_1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r7_1 open inview sum [33, 376, 630, 34] bar 609 marks 0/1 yes [32, 656, 270, 56] line 327 327  after
timeline f_r7_2 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r8_2 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
timeline f_r9_1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
bills a1 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
bills a2 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
bills a2 open inview sum [33, 418, 630, 34] bar 609 marks 0/1 yes [32, 656, 270, 56] line 327 327  after
bills a4 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
bills a3 closed inview sum [33, 552, 630, 36] bar 609 marks 1/1 yes [32, 656, 270, 56] line 327 327  
bills a3 open inview sum [33, 418, 630, 34] bar 609 marks 0/1 yes [32, 656, 270, 56] line 327 327  after
== 1366x768-how {'info': {'link_text': 'How each answer is checked', 'link_box': {'x': 943.3125, 'y': 41.5, 'width': 235.6875, 'height': 44}, 'words': 412, 'title': 'How each answer is checked – Treatment Timeline', 'imgW': 820, 'figW': 1056, 'figScrollW': 1056, 'imgTop': 682, 'stepsBottom': 497, 'hScroll': False, 'docH': 2260, 'imgLoaded': True, 'steps': ['1\nPrepared by our team. In this demo the sample answers were written ahead of time, not by an AI model. A real run has an AI model draft a one-line summary of each record and pick the exact words it came from.', '2\nCode checks it. Plain code, not AI, confirms the quote is in the record word for word and that every date, amount and number in the line is in the quote. Dates, gaps and totals are worked out by code alone.', '3\nA second AI checks it. A different model, with a different prompt, reads the record and the answer. It says it agrees, disputes it or could not check, with a one-line reason. If it disputes, you must confirm you compared the line with the quote.', '4\nYou decide. You accept, edit or dismiss every item. Code builds the letter from what you accepted, and nothing else.'], 'back_to': '/'}, 'errs': []}
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:16.573Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-075\" -A 6 memory/ORCHESTRATOR_DECISIONS.md | head -20",
 "description": "Check whether D-075 is a recorded decision"
}
````

### User / tool · 2026-11-03T13:16:16.655Z

**tool result**
````
106:## D-075 — Ship freeze: how we finish fast (Chris, 2026-11-03: "speed all this work up")
107-Where the time went: serial review→fix rounds per card (T-202 took six), every worker running the full e2e suite (10-20 min each), per-card reviews plus gate panels re-checking the same things, and polish findings reopening cards. Binding until submission:
108-1. Fix only what makes the demo wrong, crash, leak or mislead (fact errors, provenance, privacy, broken setup). Every other finding (major or minor UX/test-rigor/wording) goes straight to SCOPE_CUTS as accepted debt; no new rounds for it.
109-2. No more per-card review rounds. The open cards (T-202 fallback, T-207, T-211, T-213, T-184, T-188, T-212) are reviewed once, together, by ONE combined M3+M4 gate panel on one pinned commit, run in parallel (staff, UX, paralegal, privacy, installer, PM; Sonnet except PM). That panel is also Chris's double-check of the assets and packet. One blockers-only fix round, then gate.
110-3. Workers run targeted tests only; QA runs the full unit + e2e suite once on the gate commit.
111-4. The final prompt-log build and the snapshot build start as soon as the gate commit is pinned, in parallel with the panel, and re-run once (delta only) after the fix round.
112-5. M5 hiring panel runs immediately after, on the final commit.
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:22.884Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux/390x844-e1.png"
}
````

### User / tool · 2026-11-03T13:16:22.892Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:23.350Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux/1440x900-f_r7_1.png"
}
````

### User / tool · 2026-11-03T13:16:23.358Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:32.823Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux/1440x900-f_cx1.png"
}
````

### User / tool · 2026-11-03T13:16:32.835Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:33.329Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-211-ux/1440x900-how-fold.png"
}
````

### User / tool · 2026-11-03T13:16:33.338Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:41.074Z

**tool call — Bash**
````
{
 "command": "lsof -nP -iTCP:7932 -sTCP:LISTEN",
 "description": "Find PID of demo server on 7932"
}
````

### User / tool · 2026-11-03T13:16:41.243Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  35346 arsis    9u  IPv4 0x349f7602b0ec9e5e      0t0  TCP 127.0.0.1:7932 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:42.364Z

**tool call — Bash**
````
{
 "command": "kill 35346",
 "description": "Stop my demo server"
}
````

### User / tool · 2026-11-03T13:16:42.445Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:16:43.720Z

**tool call — Bash**
````
{
 "command": "curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7932/",
 "description": "Confirm port 7932 is closed"
}
````

### User / tool · 2026-11-03T13:16:43.807Z

**tool result (error)**
````
Exit code 7
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:17:36.476Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-211-ux-designer.md",
 "content": "# T-211 — UX designer review (Priya Raman, ux-designer-reviewer)\n\n**Verdict: fail** (1 blocker, 0 majors, 5 minors). Severity follows D-075 (Chris, 2026-11-03), which is binding until submission. Only findings that make the demo wrong or misleading, or that make the judge/HITL explanation false or invisible, are blocker-class. Everything else is minor and goes to SCOPE_CUTS. Minors that my dossier (§8) would rate major are labelled \"(dossier: major)\", so the lower rating is visible.\n\nScope: HEAD cda2856 (`git rev-parse --short HEAD` printed `cda2856`). T-211 commits 82217e5 and 4e4ff36 are its ancestors. `git diff --stat 4e4ff36 HEAD -- app/` printed nothing, so the app is the same as at the card commit. I extracted the commit with `git archive cda2856` into a new empty scratch directory. I served it in demo mode the way run.sh does (LLM_BACKEND=fixture, FIXTURE_SET=curated) on :7932 with its own DB. `/api/health` returned `\"answers\":\"prepared\"`, `\"generator\":\"hand-checked (qa)\"`, `\"judge\":\"claude-haiku-5-5\"`. I stopped the server afterwards, and `curl` on :7932 returned `000`.\n\nWhat works: on desktop the panel is clear and well placed. At 1440x900 it is open on 19 of 23 items and folds to chips on the 4 multi-record warnings. The summary row sits at y 536–706, above the action bar (top 729). Yes stays at y 782 on every item, and there are no console errors. The How page is plain and honest about prepared answers.\n\nThe problem is one sample item. On f_r7_1 the panel says the second AI checked a prepared answer. The same row also says the second AI did not run and that there is no prepared answer. That makes the judge explanation false on a screen the demo shows.\n\n```json\n{\"card\": \"T-211\", \"persona\": \"ux-designer-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"HEAD cda2856 (contains 82217e5, 4e4ff36; no app/ diff since 4e4ff36); git archive into a new empty dir; demo mode (fixture, curated) on http://127.0.0.1:7932; sample case (evals/golden/sample.txt via POST /api/cases {sample:true})\",\n \"exercised\": [\n  \"Read personas/ux-designer.md, D-074, D-065, D-069 note in memory/contracts/api.md, D-075, the T-211 card and handoff, review.js:90-137 and 240-402, how.js, how.css, the T-211 diff of app.js/step2.js/step3.js\",\n  \"artifacts/review-evidence/T-211-ux-probe.py: per-item judge verdicts from GET /items/<id>/trace for all 23 sample items (first on a server started without FIXTURE_SET, which served the 'recorded' set; discarded and rerun on the curated server)\",\n  \"artifacts/review-evidence/T-211-ux-measure.py: opened every Step 2 (19) and Step 3 (4) item at 1440x900, 390x844 (mobile, touch) and 1366x768; measured panel open/closed, summary rect vs action bar, highlights inside the record window, Yes rect, page scroll; opened the folded panel on 6 items and re-measured; console errors collected (none at any size)\",\n  \"How page via the header link at all three sizes: word count, steps text, ladder image size and sideways scroll, Back returns to /\",\n  \"Screenshots in artifacts/review-evidence/T-211-ux/ (measure.json holds every number quoted)\",\n  \"Not exercised (D-075 time box): full e2e, an end-to-end keyboard walk to Step 4, the You row after a decision (covered by test_t211.py, not re-driven live)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"design quality\": 4, \"originality\": 3, \"craft\": 3, \"functionality\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"f_r7_1: the Second AI check row says a prepared answer was checked by the second AI, then says the check did not run and there is no prepared answer\",\n   \"evidence\": \"artifacts/review-evidence/T-211-ux/1440x900-f_r7_1.png (Item 13 of 19, accident-date warning, tag 'Prepared answer'). The Second AI check row reads, verbatim: 'Prepared by our team; the second AI check then checked it against the quote.' then 'Not needed. Not run: only the phrase list found this warning, so there is no prepared answer to double-check; it stays marked for review.' The Code check row reads: 'Did not pass: The phrase list found this warning but the prepared answers did not; check that it applies.' Probe: f_r7_1 prepared=True, judge_4 status 'skipped', judge_verdict None. Cause: app/frontend/guided/review.js:117 sets the prepared lead from item.prepared alone, whatever the judge step did; review.js:121 maps every skipped step without a verdict to the word 'Not needed', even when its reason begins 'Not run'.\",\n   \"why_it_matters\": \"This is the one sample item where the ladder did not run in full, so it is where a first-time viewer learns most about the ladder. The panel tells them a second AI checked a prepared answer. The same row then says neither happened, and it labels a check that did not run as 'Not needed'. D-074 says the app must show the judge's verdict truthfully. D-065 says provenance wording must be truthful. Under D-075 a false judge explanation is blocker-class.\",\n   \"fix\": \"Show the prepared lead only when the judge step actually returned a verdict (status pass or fail with judge_verdict). Show the verdict word 'Not run' (chip 'AI: not run') when the step was skipped and its reason begins 'Not run', and keep 'Not needed' for code-made items such as the gap and accident-date arithmetic. Backend owner: an item that only the phrase list found should not carry the 'Prepared answer' tag or prepared=true. That is a card for backend, not frontend.\",\n   \"acceptance_test\": \"Live sample case, f_r7_1, at 1440x900: how-ai-text does not contain 'then checked it'; how-verdict is 'Not run'; how-chip-ai is 'AI: not run'. f_gap_r6_r7 still reads 'Not needed'. e1 still shows the prepared lead with 'Agrees'.\"},\n  {\"severity\": \"minor\", \"title\": \"(dossier: major) At 390x844 the panel is below the action bar on 23 of 23 items; only a grey edge hints that it exists\",\n   \"evidence\": \"artifacts/review-evidence/T-211-ux/390x844-e1.png. measure.json 390x844: the summary's top edge is between y 665 and 972 on every item, and the action bar's top edge is at y 659. The line card is scrollable (scrollHeight 290-597 vs clientHeight 216). After a tap the panel opens in view (390x844-e1-opened.png). The header link 'How it's checked' is visible at x 190, y 50 (390x844-home.png).\",\n   \"why_it_matters\": \"This answers the brief's question 'is it still discoverable?'. On a phone it is not discoverable without scrolling inside the card. A viewer who never scrolls that inner box never sees the per-item code check, AI check and You rows. I did not rate it blocker because the panel is one scroll away and the header link explains the ladder on every screen.\",\n   \"fix\": \"On a phone, put the chip row (closed summary) directly under the line's tag and date, or in the line card's head, so the three chips show at first paint. Keep the rows folded.\",\n   \"acceptance_test\": \"390x844, every sample item: the how-summary rect is fully above the actions top edge with the line card scrolled to 0.\"},\n  {\"severity\": \"minor\", \"title\": \"(dossier: major) Once opened, the panel hides the highlighted words, and the choice persists for the rest of the visit\",\n   \"evidence\": \"measure.json 1366x768 after opening: e1 shows 0 of 1 marks in the record window, f_cx1 0 of 2, f_r7_1 0 of 1, a2 0 of 1, a3 0 of 1. At 1440x900 after opening, f_gap_r6_r7 shows 2 of 4 and f_cx1 1 of 2. Cause: review.js:399 returns early from fitHow once R.howOpen is set, so after one click every later item keeps the panel open even when it pushes the highlight out. Screenshot: 1366x768-e1-opened.png.\",\n   \"why_it_matters\": \"The quote beside the line is how the paralegal verifies an item. A viewer on a 1366x768 laptop who opens the panel once to learn the ladder then has to scroll the record window to find the quote on every item. The words are still reachable by scrolling, so this is not the §5 blocker.\",\n   \"fix\": \"After the user opens the panel, still scroll the record window so the first mark is in view (alignMark after layout). Or cap the open panel's height with its own scroll, so the window keeps room for the marks.\",\n   \"acceptance_test\": \"1366x768: open the panel on e1, then step through e2..e9 and f_cx1; on each, at least the first mark is inside the card-source rect.\"},\n  {\"severity\": \"minor\", \"title\": \"The demo never shows the second AI disputing anything; the dispute path is covered only by a stubbed e2e\",\n   \"evidence\": \"T-211-ux-probe.py on the curated sample: judge verdicts are 'supported' on 18 items, skipped on 5 (gap, accident-date, f_r7_1, a3) and disputed on 0. tests/e2e/guided/test_t211.py rewrite_trace() forces 'partially' on e2 with page.route.\",\n   \"why_it_matters\": \"D-074 asks a first-time viewer to understand that an independent check can disagree. In the demo every verdict is a green 'AI: agrees', so the judge reads as a rubber stamp. The red 'Disputes' state has never been seen live.\",\n   \"fix\": \"Product decision. Either have the How page show one disputed example as a static picture of the panel, or add a committed demo case whose recorded judge verdict is a real dispute.\",\n   \"acceptance_test\": \"A viewer of the demo can reach one screen showing 'AI: disputes' with the server's reason, without stubbing.\"},\n  {\"severity\": \"minor\", \"title\": \"The How page is 412 words, not 'about 150', and the picture starts below the fold\",\n   \"evidence\": \"measure.json 1440x900-how: words 412, steps end at y 497, ladder image top at y 682. At 1440x900 the fold shows an empty white frame (1440x900-how-fold.png). At 390x844 the image is 640 px wide in a 318 px box and scrolls sideways (390x844-how-full.png).\",\n   \"why_it_matters\": \"The four steps are clear (what's right, below). Below them are three more panels (the picture, the code-vs-AI lists and the repo paths) that repeat the steps. On a phone the picture must be scrolled sideways to read it.\",\n   \"fix\": \"Put the picture directly beside or under the four steps, and fold the repo list under 'For reviewers'. On a phone use a tall version of the SVG.\",\n   \"acceptance_test\": \"1440x900: part of the ladder picture is visible above the fold. 390x844: figure scrollWidth <= clientWidth.\"},\n  {\"severity\": \"minor\", \"title\": \"'Not needed' covers two different situations, and the 'Code: none' / 'AI: not needed' chips show no reason when the panel is folded\",\n   \"evidence\": \"Probe: a3 judge_2 skipped with 'Damages and other non-bill figures are not sent to the second check.'; f_gap_r6_r7 judge_not_needed 'arithmetic over dates'. Both show the chip 'AI: not needed' (390x844-a3.png, 1440x900-f_gap_r6_r7.png).\",\n   \"why_it_matters\": \"For the gap, 'not needed' is accurate: code did the work. For damages, the second check is skipped by policy, so 'Not sent' is the honest word.\",\n   \"fix\": \"Chip 'AI: not sent' for policy skips; keep 'not needed' for code-made items.\",\n   \"acceptance_test\": \"a3 shows 'AI: not sent'; f_gap_r6_r7 shows 'AI: not needed'.\"}],\n \"whats_right\": [\n  \"At 1440x900 the panel is open on 19 of 23 items and folds to chips on the 4 multi-record warnings. The primary action never moves (Yes at y 782 on every item), and there were 0 console errors across 69 item views.\",\n  \"The How page's four steps are honest and plain. Step 1 says the demo answers were 'written ahead of time, not by an AI model' (D-065), and step 3 says the second AI 'can be wrong too, which is why the last word is yours'.\",\n  \"The header link is on every screen and fits at 390 ('How it's checked', 137x40 px), and Back returns to where the user came from.\"],\n \"questions_for_chris\": [\n  \"Should the demo include one real recorded judge dispute (a committed case or a static example on the How page), so viewers see the second check disagree at least once?\"]}\n```\n"
}
````

### User / tool · 2026-11-03T13:17:36.627Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-211-ux-designer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:17:38.008Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5",
 "description": "Validate board including the new review file"
}
````

### User / tool · 2026-11-03T13:17:38.164Z

**tool result**
````
ok (213 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:17:45.758Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_t211_ladder_panel.md",
 "content": "---\nname: project-t211-ladder-panel\ndescription: T-211 r1 cda2856 fail (D-075 severity): f_r7_1 panel says prepared+second AI checked while judge did not run; phone panel below bar; demo server needs FIXTURE_SET=curated\nmetadata:\n  type: project\n---\n\nT-211 r1 (reviews/T-211-ux-designer.md, HEAD cda2856, 2026-11-03): **fail**, 1 blocker, 5 minors.\n- Blocker: on sample item f_r7_1 (the accident-date phrase-list warning) the \"Second AI check\" row shows the prepared lead \"...the second AI check then checked it against the quote.\" next to \"Not needed. Not run: ... no prepared answer\". Cause: review.js:117 (lead set on item.prepared alone) and review.js:121 (any skip maps to \"Not needed\").\n- Minors (several are majors under the dossier, filed minor per D-075): at 390x844 the panel summary is below the action bar on 23 of 23 items; once opened, the panel hides marks at 1366x768 and the choice persists; no live dispute anywhere in the demo; the How page is 412 words with the picture below the fold; \"not needed\" is used for policy skips.\n\nProbe quirk: `python -m app.main` without FIXTURE_SET serves the \"recorded\" set, where items show prepared=false. Start the demo server with LLM_BACKEND=fixture FIXTURE_SET=curated, the same way run.sh does.\n\nScripts: artifacts/review-evidence/T-211-ux-probe.py (per-item judge verdicts from traces) and T-211-ux-measure.py <base> <outdir> (3 sizes, all items, How page).\n\n**Why:** D-075 (ship freeze) makes only \"wrong, misleading, or false or invisible explanation\" findings blocking.\n**How to apply:** at the gate, re-run measure.py and check the f_r7_1 row text and the phone summary position. See [[project-t181-guided-build]].\n"
}
````

### User / tool · 2026-11-03T13:17:45.853Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/project_t211_ladder_panel.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:17:47.544Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer && printf '%s\\n' '- [T-211 ladder panel](project_t211_ladder_panel.md) — cda2856 fail: f_r7_1 false judge row; phone panel below bar; serve demo with FIXTURE_SET=curated' >> MEMORY.md",
 "description": "Add T-211 pointer to memory index"
}
````

### User / tool · 2026-11-03T13:17:47.636Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T13:17:50.458Z

Fail, 1 blocker: on sample item f_r7_1 the "Second AI check" row says the second AI checked a prepared answer, then "Not needed. Not run … no prepared answer" (`review.js:117`, `:121`; `artifacts/review-evidence/T-211-ux/1440x900-f_r7_1.png`).
No majors under D-075; 5 minors, of which two the dossier would rate major: the phone panel sits below the action bar on all 23 items, and opening it hides the highlighted words at 1366x768. Review: `/Users/arsis/zlayt-pm-project/reviews/T-211-ux-designer.md`; my server on :7932 is stopped.
