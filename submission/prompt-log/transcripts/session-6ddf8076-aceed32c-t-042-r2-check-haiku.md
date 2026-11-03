# Subagent: T-042 r2 check (haiku) (T-042 r2 check (haiku))

Source: `agent-aceed32c50cb5230a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:57:46.437Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-042 (commit 348cd0b) vs reviews/T-042-ux-designer.md (major: timeline counts don't reconcile; minor: false red error from could-not-verify tray). Re-run the reviewer's walk script artifacts/review-evidence/T-042-*.py if present (else serve app/frontend on :7867 with ?api=mock and check with Playwright): header shows entries-only counts that match the rows; opening a tray record shows no role=alert. Quote outputs. Write reviews/T-042-ux-designer-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:57:47.534Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/ux-designer.md"
}
````

### User / tool · 2026-11-02T01:57:47.546Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:57:48.287Z

**tool call — Bash**
````
{
 "command": "ls reviews/ artifacts/review-evidence/ 2>&1; ls .claude/agent-memory/ux-designer-reviewer/ 2>&1; git -C /Users/arsis/zlayt-pm-project log --oneline -3 2>&1; git -C /Users/arsis/zlayt-pm-project show --stat 348cd0b 2>&1 | head -30",
 "description": "List reviews, evidence, memory dir, and commit 348cd0b"
}
````

### User / tool · 2026-11-02T01:57:48.404Z

**tool result**
````
artifacts/review-evidence/:
M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-001-r2-readonly-repros.txt
T-001-r3-repro.out.txt
T-001-r3-repro.sh
T-002-curl.txt
T-002-r2-activity-390.png
T-002-r2-board-390.png
T-002-r2-csrf-curl.txt
T-002-r2-inbox-390.png
T-002-r2-milestones-390.png
T-002-r2-personas-390.png
T-002-r2-state-390.png
T-002-r2-xss.json
T-002-r3-404.py
T-002-r3-activity-390.png
T-002-r3-board-390.png
T-002-r3-inbox-390.png
T-002-r3-milestones-390.png
T-002-r3-personas-390.png
T-002-r3-probe.out.txt
T-002-r3-probe.py
T-002-r3-state-390.png
T-002-r3-ui.out.txt
T-002-r3-ui.py
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-r2-commit-secret-probe.out.txt
T-003-r2-commit-secret-probe.py
T-003-r2-git-guard-results.txt
T-003-r2-probe-board2.out.txt
T-003-r2-probe-board2.py
T-003-r2-probe-corpus.txt
T-003-r2-probe-direct.out.txt
T-003-r2-probe-direct.out2.txt
T-003-r2-probe-direct.py
T-003-r3-probe-board2.out.txt
T-003-r3-probe-corpus.out.txt
T-003-r3-probe-corpus.py
T-003-r3-probe-direct.out.txt
T-003-r3-probe-legit.out.txt
T-003-r3-probe-legit.py
T-003-r3-probe-pwd.out.txt
T-003-r3-probe-pwd.py
T-003-r3-probe-rwg.out.txt
T-003-r3-probe-rwg.py
T-003-r3-probe-targeted.out.txt
T-003-r3-probe-targeted.py
T-003-r3-probe-targeted2.out.txt
T-003-r3-probe-targeted2.py
T-003-reviewer-write-guard-probe.txt
T-004-agent-check.txt
T-004-r2-agent-sync.txt
T-004-r2-board-guard-probe.py
T-004-r2-board-guard-probe.txt
T-004-r2-shell-write-probe.txt
T-004-r3-board-guard-probe.out.txt
T-004-r3-board-guard-probe.py
T-005-r2-pathcheck.py
T-006-check-secrets-probe.txt
T-006-r2-chain-probe.out.txt
T-006-r2-chain-probe.py
T-006-r2-fp-probe.out.txt
T-006-r2-fp-probe.py
T-006-r2-probe.out.txt
T-006-r2-probe.py
T-006-r3-chain-probe.out.txt
T-006-r3-commit-paths-probe.out.txt
T-006-r3-commit-paths-probe.py
T-006-r3-fp-probe.out.txt
T-006-r3-probe.out.txt
T-006-rename-probe.txt
T-008-adjuster-source-checks.txt
T-008-r2-adjuster.md
T-008-r2-src
T-008-r3-adjuster-greps.txt
T-008-r3-adjuster-hits.md
T-008-r3-insurancejournal-854959.html
T-008-r3-insurancejournal-checks.txt
T-009-adjuster-probes.py
T-009-adjuster-probes.txt
T-009-nurse-golden-scan.txt
T-009-nurse-probe-output.txt
T-009-nurse-probe.py
T-009-nurse-probes.txt
T-009-r2-nurse-probe-output.txt
T-009-r2-nurse-probe.py
T-009-r2-nurse-variants-output.txt
T-009-r2-nurse-variants.py
T-009-r2-resolution.md
T-010-011-sections.txt
T-010-011-source-check.md
T-010-litlead-source-check.md
T-010-r2-count.py
T-010-r2-resolution.md
T-010-r2-srch.py
T-010-r3-check.py
T-010-r3-resolution.md
T-011-r2-check.py
T-012-h2t.py
T-012-r2-fetch.py
T-012-r2-resolution.md
T-012-source-check.md
T-013-paralegal-walkthrough.md
T-013-r2-paralegal-jsoncheck.py
T-013-r2-paralegal-walk.out.txt
T-013-r2-paralegal-walk.py
T-013-r2-resolution.md
T-013-r3-paralegal-golden-cmp.out.txt
T-013-r3-paralegal-golden-cmp.py
T-013-r3-paralegal-jsoncheck.py
T-013-r3-paralegal-walk.out.txt
T-013-r3-paralegal-walk.py
T-013-r3-resolution.md
T-013-r3check.py
T-013-trace.md
T-014-amount-cue-demo.py
T-014-injection-trace.md
T-014-json-check.out
T-014-json-check.py
T-014-r2-amount-demo.py
T-014-r2-amount-sim.out
T-014-r2-amount-sim.py
T-014-r2-json-check.out
T-014-r2-offset-check.out
T-014-r2-offset-check.py
T-014-r2-privacy-resolution.md
T-014-r2-staff-resolution.md
T-014-r3-amount-demo.out
T-014-r3-amount-demo.py
T-014-r3-amount-sim.out
T-014-r3-amount-sim.py
T-014-r3-resolution.md
T-014-walkthrough.md
T-015-legal-nurse-items.md
T-015-paralegal-blind.md
T-015-paralegal-regex-probe.out.txt
T-015-paralegal-regex-probe.py
T-015-r2-nurse-probe.out.txt
T-015-r2-nurse-probe.py
T-015-r2-nurse.md
T-015-r2-paralegal-jsoncheck.py
T-015-r2-paralegal-probe.out.txt
T-015-r2-paralegal-probe.py
T-015-r2-paralegal.md
T-015-r3-paralegal-entries.out.txt
T-015-r3-paralegal-entries.py
T-015-r3-paralegal-jsoncheck.py
T-015-r3-paralegal-mutation.out.txt
T-015-r3-paralegal-mutation.py
T-015-r3-paralegal-probe.out.txt
T-015-r3-paralegal-probe.py
T-015-r3-paralegal-rerun-of-r2-probe.out.txt
T-015-r3-paralegal-s6diff.out.txt
T-015-r3-paralegal-s6diff.py
T-015-r3-rerun-of-r2-nurse-probe.out.txt
T-015-r4-paralegal-jsoncheck.out.txt
T-015-r4-paralegal-jsoncheck.py
T-015-r4-paralegal-recheck.out.txt
T-015-r4-paralegal-recheck.py
T-017-r3-owner-probe.out.txt
T-017-r3-owner-probe.py
T-018-contract-probe.out.txt
T-018-contract-probe.py
T-018-r2-applied-check.out.txt
T-018-r2-applied-check.py
T-018-r3-applied-check.out.txt
T-025-pm-probe.out.txt
T-025-pm-probe.py
T-025-pm-r2-probe.out.txt
T-025-pm-r2-probe.py
T-026-desktop-dialog.png
T-026-desktop-office.png
T-026-mobile-dialog.png
T-026-mobile-office.png
T-026-ux-designer-office.py
T-027-nurse-fresh-probe.py
T-027-nurse-fresh.txt
T-028-r2-checks.py
T-028-r2-json-check.py
T-028-review-checks.py
T-028-review-json-check.py
T-030-exercise.py
T-031-ac_check.out
T-031-ac_check.py
T-031-mutation.out
T-031-mutation.py
T-031-r2-check.out
T-031-r2-check.py
T-031-r2-verdict-check.py
T-032-ingest.py
T-033-golden.out.txt
T-033-golden.py
T-033-mutations.txt
T-033-r2-golden.out.txt
T-036-adjuster-probe.py
T-036-adjuster-probe2.py
T-036-case07-pipeline.txt
T-036-cases-probe.txt
T-036-probe2.txt
T-036-probe3.py
T-036-probe3.txt
T-036-sample-probe.txt
T-039-r2-checks.py
T-039-r2-checks.txt
T-039-r2-letter-stub.py
T-039-r2-letter-stub.txt
T-039-r2-mutation.py
T-039-r2-mutation.txt
T-041-cnp.py
T-041-export-all-accepted.txt
T-041-export-case07.txt
T-041-export-dismiss5-pending6.txt
T-041-export.py
T-041-r2-mutation.py
T-042-1280-01-empty.png
T-042-1280-02-empty-error.png
T-042-1280-03-oversize.png
T-042-1280-04-pdf.png
T-042-1280-05-found.png
T-042-1280-06-processing.png
T-042-1280-07-results.png
T-042-1280-07b-results-full.png
T-042-1280-08-entry7.png
T-042-1280-09-why7.png
T-042-1280-10-source8.png
T-042-1280-11-fail4.png
T-042-1280-12-dates-to-confirm.png
T-042-1280-13-kbd.png
T-042-1280-14-tray-open-record.png
T-042-375-01-empty.png
T-042-375-02-empty-error.png
T-042-375-03-oversize.png
T-042-375-04-pdf.png
T-042-375-05-found.png
T-042-375-06-processing.png
T-042-375-07-results.png
T-042-375-07b-results-full.png
T-042-375-08-entry7.png
T-042-375-09-why7.png
T-042-375-10-source8.png
T-042-375-11-fail4.png
T-042-ux-designer-walk.py
T-043-1280-01-flags-top.png
T-043-1280-02-conflict.png
T-043-1280-03-charges.png
T-043-1280-04-after-dismiss-er.png
T-043-1280-05-gap-modal.png
T-043-1280-06-keyboard.png
T-043-1280-07-1200-accepted.png
T-043-1280-08-injection.png
T-043-1280-09-integrated.png
T-043-1280-10-conflict-card.png
T-043-375-01-flags-top.png
T-043-375-02-conflict.png
T-043-375-03-charges.png
T-043-375-04-after-dismiss-er.png
T-043-375-05-gap-modal.png
T-043-375-06-keyboard.png
T-043-375-09-integrated.png
T-043-paralegal-probe.py
T-043-paralegal-probe2.py
T-047-desktop-1440-dialog.png
T-047-desktop-1440-forced-reviewing.png
T-047-desktop-1440.png
T-047-mobile-390-dialog.png
T-047-mobile-390-full.png
T-047-mobile-390-nav-onload.png
T-047-mobile-390.png
T-047-ux-designer-ac2-forced.py
T-047-ux-designer-check.py
T-047-ux-designer-nav-keyboard.py
T-049-served-index.html
T-049-ux-designer-01-board-390.png
T-049-ux-designer-02-office-390.png
T-049-ux-designer-03-fullscreen-390.png
T-049-ux-designer-04-view-office-390.png
T-049-ux-designer-check.out.json
T-049-ux-designer-check.py
__pycache__
tmp13651ilh
tmp_7ds_ih3
tmpexbqevaz
tmpq8_383ll

reviews/:
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security-r3.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
T-026-ux-designer.md
T-027-legal-nurse.md
T-028-staff-engineer-r2.md
T-028-staff-engineer.md
T-029-staff-engineer-r2.md
T-029-staff-engineer.md
T-030-staff-engineer-r2.md
T-030-staff-engineer-r3.md
T-030-staff-engineer.md
T-031-staff-engineer-r2.md
T-031-staff-engineer.md
T-032-staff-engineer-r2.md
T-032-staff-engineer.md
T-033-staff-engineer.md
T-034-security-r2.md
T-034-security.md
T-035-staff-engineer-r2.md
T-035-staff-engineer.md
T-039-staff-engineer.md
T-041-paralegal-r2.md
T-041-paralegal.md
T-042-ux-designer.md
T-047-ux-designer.md
T-048-staff-engineer.md
T-049-ux-designer.md
348cd0b fix(frontend): entries-only count line, no false tray error, UX minors (T-042 r2)
ad4803a fix(backend): T-033 r2 - unit-rate-only rate cue, no decimal truncation, conflict over-firing test
d67a82d feat(backend): pipeline stages 0-7, persistence, CLI (T-037 part 1)
commit 348cd0b46c0aecfab926d8ee48c7e553b6ccadfa
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:57:39 2026 -0600

    fix(frontend): entries-only count line, no false tray error, UX minors (T-042 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/input.js    |  6 ++++--
 app/frontend/source.js   |  9 +++++----
 app/frontend/styles.css  |  3 +++
 app/frontend/timeline.js | 20 +++++++++++---------
 4 files changed, 23 insertions(+), 15 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:57:50.477Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-042-ux-designer.md; echo ----; cat artifacts/review-evidence/T-042-ux-designer-walk.py",
 "description": "Read round 1 review and existing walk script"
}
````

### User / tool · 2026-11-02T01:57:50.560Z

**tool result**
````
# T-042 UX review (ux-designer-reviewer)

Verdict: changes. No blockers. Every T-042 AC behaves as written against the mock API. One major (status count contradicts the visible list) plus minors. Real backend (:7860) was not up, so this is mock-only (`?api=mock`); the real e2e specs were not run. T-043 code (Accept/Edit/Dismiss, flags, charges) was loading in index.html while I reviewed; I did not grade it.

AC check (served `.venv/bin/python -m http.server 7865 --directory app/frontend`, Playwright 1280x900 and 375x812, script `artifacts/review-evidence/T-042-ux-designer-walk.py`):
1. "9 records found" shown before Analyze with text "Read by code only. No model has been called yet." PASS. .pdf refused: "PDF files can't be read here. Save the records as plain text (.txt) or paste them." role=alert, pasted text kept. Empty: "There is no text to read. Paste records or choose a .txt file." Oversize (600,017 chars): "That is 600,017 characters; the limit is 60,000. Nothing was sent." Textarea preserved at full length. PASS.
2. needs_review (entry-3) first, then verified by date; "Dates to confirm" after the queue (pasted case_01 shows the undated row); "Could not verify" tray after that. PASS.
3. Why? on entry 7: state, backend, generator, code checks, judge verdict. PASS.
4. Entry 8 highlight text == excerpt (True at both widths). PASS.
5. Synthetic banner visible on empty, found, processing, results and modals at both widths; AI banner on review; `grep -c innerHTML app/frontend/*.js` = 0 for all 12 files. PASS.
6. `?fail=4`: record 4 in tray with "could not process" + reason. PASS.
No horizontal scroll at 375. No console or page errors.

Screenshots: artifacts/review-evidence/T-042-{1280,375}-01..11*.png, T-042-1280-12-dates-to-confirm.png, -13-kbd.png, -14-tray-open-record.png.

```json
{"card": "T-042", "persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/frontend (index.html, input.js, timeline.js, source.js, app.js, mock.js) served statically on :7865 with ?api=mock; sample case + case_01 paste + ?fail=4; 1280x900 and 375x812. Real backend not exercised.",
 "exercised": ["Read personas/ux-designer.md, `python3 tools/board.py show T-042`, tests/e2e/conftest.py contract, test_input/test_timeline/test_source_record",
   "`grep -c innerHTML app/frontend/*.js` -> 0 for all 12 files",
   "Playwright 1280 and 375: empty submit, 600 KB submit, .pdf upload, sample load, Analyze/processing, results, entry-7 Why?, entry-8 Open record, ?fail=4 tray, tray Open record, case_01 paste (Dates to confirm), Tab order",
   "Measured data-state order, tabindex on queue rows, first focusable in results, horizontal scroll, y-offsets of first needs_review row"],
 "verdict": "changes",
 "scores": {"design_quality": 3, "originality": 3, "craft": 3, "functionality": 4},
 "findings": [
  {"severity": "major", "title": "Status count line contradicts the list on screen", "evidence": "artifacts/review-evidence/T-042-1280-07-results.png: toolbar reads 'Timeline (9 entries)' and 'testid=review-counts' = '2 need review · 11 verified', but the queue has 9 rows and exactly 1 needs_review (entry-3). With ?fail=4: '1 need review · 10 verified' next to 'Timeline (8 entries)'. Source: timeline.js renderReview uses c.review.counts (mock.js:131 counts entries + amounts + flags).", "why_it_matters": "This is the only status/progress line on the review screen. A paralegal counts one amber row and reads two, or 11 verified of 9 entries, and stops trusting the tool. Visibility of system status and calibrated trust.", "fix": "Show entry-only counts beside the entry list (e.g. '1 of 9 needs review'), or label the number as covering entries, amounts and flags. Do not print a number that cannot be reconciled with visible rows.", "acceptance_test": "E2E: text of review-counts needs_review count equals queue rows with data-state=needs_review, and verified+needs_review equals the entry count."},
  {"severity": "minor", "title": "Tray 'Open record' shows a false red error", "evidence": "artifacts/review-evidence/T-042-1280-14-tray-open-record.png: opening record 4 from the tray renders role=alert 'The exact position of this quote could not be found in the record, so nothing is highlighted.' source.js:11-14 treats start==null as a failure. Tray items have no quote.", "why_it_matters": "The expected path for a could-not-verify item reads as a fault, and an alert is announced to screen readers. It undermines the tray's purpose (read it yourself).", "fix": "When no span is requested, render the record plainly with no alert; keep the alert only when a span was requested but offsets are invalid.", "acceptance_test": "Open record from the tray: record-modal has no role=alert; open an entry with bad offsets: alert appears."},
  {"severity": "minor", "title": "Record list pushes the timeline down; first focusable item in results is the sort menu", "evidence": "At 375 the first needs_review row starts at y=955 (below the 812 fold); at 1280 it starts at y=624; the 9-line records list sits above the timeline after the run (T-042-375-07-results.png). Tab order after load: Start over, sort select, then entry-3 (T-042-1280-13-kbd.png). Checklist 19 wants the first focusable item to be needs_review. The gap flag is at y=3108 (1280) and 4760 (375); that flag belongs to T-043.", "why_it_matters": "On a returning visit or after Analyze, the reviewer must scroll past input echoes to reach the work. Keyboard users hit a sort control before the first item.", "fix": "Collapse the records list to a one-line summary ('9 records read') once the case is ready; move the sort control after the queue in DOM order or make the first needs_review row the first tab stop; focus it or scroll to the timeline when the run completes.", "acceptance_test": "After sample run at 1280x900, entry-3 top < 450 px and is the first focusable element inside the review region."},
  {"severity": "minor", "title": "Two state chips per row use ambiguous words", "evidence": "T-042-1280-10-source8.png: rows read 'Verified' + 'pending'. entry head text: '2026-01-09 | Austin EMS run report | Verified | pending'.", "why_it_matters": "'Verified' (machine check) next to 'pending' (human review) reads as a contradiction; the paralegal cannot tell which one means she still has work.", "fix": "Label the second chip by what the user owes: 'Not reviewed yet' / 'Accepted' / 'Edited' / 'Dismissed', and label the first 'Machine check: verified'.", "acceptance_test": "No row shows the bare word 'pending'; both chips carry a noun or prefix that names what they describe."},
  {"severity": "minor", "title": "Why? panel uses developer vocabulary and an internal id", "evidence": "T-042-1280-09-why7.png: title 'Why? e7'; rows 'Generator', 'Generator output', 'summary tokens not in excerpt: none', 'judge_faithfulness_v1', 'Backend fixture'.", "why_it_matters": "The first line is plain ('Quote found word for word...'), but the rest is for engineers. AC requires checks, verdict, state and backend, so keep them, in the user's words.", "fix": "Title it with the entry (e.g. 'Why? 2026-05-18 Hill Country Pain Management'); rename to 'Draft written by', 'Numbers in summary not in the quote', 'Second check (AI reviewer)'; put model and prompt versions in the collapsed Model calls details.", "acceptance_test": "why-modal text contains none of: 'e7', 'tokens', 'prompt_version', 'extract_v1' outside the collapsed details."},
  {"severity": "minor", "title": "Analyze stays clickable during a run; progress is text only", "evidence": "T-042-1280-06-processing.png: 'Analyze' button still shown and enabled under 'Checking summaries 0 of 9'; no bar. input.js:57 renders Analyze when status==='ingested' and the poll status lags.", "why_it_matters": "A second click returns an error (409 in the mock) that surfaces as a red alert in the middle of a normal run. The stage text does keep the screen from looking frozen, which is right.", "fix": "Disable or hide Analyze while status is running and add a progress element (role=progressbar or a simple bar).", "acceptance_test": "During a run btn-analyze is absent or disabled, and a progress element reports done/total."},
  {"severity": "minor", "title": "Sticky synthetic banner can cover focused elements", "evidence": "styles.css .banner.synth{position:sticky;top:0;z-index:5}; at 375 the banner wraps to two lines (~60 px) and overlays scrolled content (T-042-375-11-fail4.png). No scroll-margin-top on [tabindex] rows or buttons.", "why_it_matters": "Checklist 14: the banner must stay persistent without obscuring a focused control; Tab/scrollIntoView can park the focus under it. Defer severity to accessibility-reviewer.", "fix": "Add scroll-padding-top equal to the banner height on html, or shorten the mobile text.", "acceptance_test": "At 375, Tab through 10 controls: each focused element's top >= banner bottom."},
  {"severity": "nit", "title": "Duplicated modal heading", "evidence": "T-042-1280-10-source8.png: 'Record 8: Austin Imaging, cervical MRI' appears in the dialog title and again above the record text.", "why_it_matters": "Wasted vertical space on a 375 px screen.", "fix": "Drop the inner h3 when it equals the dialog title.", "acceptance_test": "Single heading per record in the modal."}
 ],
 "whats_right": ["Input errors sit under the buttons in plain language, keep the pasted text, and the oversize message says 'Nothing was sent'.",
   "Source modal highlights by API offsets and equals the entry excerpt at both widths; excerpt is on every row without an extra click.",
   "Needs-review rows carry amber with a text chip and a visible 'Check: ...' reason; the could-not-verify tray explains it is not in the letter."],
 "questions_for_chris": ["Is 'N need review' in the toolbar meant to count entries only, or entries plus amounts and flags? If the latter it needs its own label."]}
```
----
import re, json, tempfile, os
from playwright.sync_api import sync_playwright
U="http://localhost:7865/index.html?api=mock"
OUT="artifacts/review-evidence/T-042-"
log=[]
def L(k,v): log.append((k,v)); print(k,"=>",v)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H,tag in ((1280,900,"1280"),(375,812,"375")):
        ctx=b.new_context(viewport={"width":W,"height":H}); pg=ctx.new_page()
        errs=[]; pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.on("dialog",lambda d:(errs.append("DIALOG "+d.message), d.dismiss()))
        pg.goto(U); pg.wait_for_timeout(500)
        pg.screenshot(path=f"{OUT}{tag}-01-empty.png")
        L(tag+" banner",pg.get_by_test_id("banner-synthetic").inner_text())
        # empty
        pg.get_by_test_id("btn-analyze").click(); pg.wait_for_timeout(200)
        L(tag+" empty alert",pg.get_by_role("alert").first.inner_text())
        pg.screenshot(path=f"{OUT}{tag}-02-empty-error.png")
        # oversize
        big="=== Record 1 ===\n"+("x"*600000)
        pg.get_by_test_id("input-text").fill(big); pg.get_by_test_id("btn-analyze").click(); pg.wait_for_timeout(300)
        L(tag+" oversize alert",pg.get_by_role("alert").first.inner_text()); L(tag+" textarea preserved len",len(pg.get_by_test_id("input-text").input_value()))
        pg.screenshot(path=f"{OUT}{tag}-03-oversize.png")
        # pdf
        d=tempfile.mkdtemp(); f=os.path.join(d,"x.pdf"); open(f,"wb").write(b"%PDF-1.4")
        pg.get_by_test_id("input-text").fill("my pasted text keep me")
        pg.get_by_test_id("file-input").set_input_files(f); pg.wait_for_timeout(200)
        L(tag+" pdf alert",pg.get_by_role("alert").first.inner_text()); L(tag+" paste kept after pdf",pg.get_by_test_id("input-text").input_value())
        pg.screenshot(path=f"{OUT}{tag}-04-pdf.png")
        # sample
        pg.get_by_test_id("btn-sample").click(); pg.get_by_test_id("record-count").wait_for()
        L(tag+" count",pg.get_by_test_id("record-count").inner_text())
        pg.screenshot(path=f"{OUT}{tag}-05-found.png")
        pg.get_by_test_id("btn-analyze").click(); pg.wait_for_timeout(700)
        L(tag+" progress",pg.get_by_test_id("status-stage").inner_text() if pg.get_by_test_id("status-stage").count() else "none")
        pg.screenshot(path=f"{OUT}{tag}-06-processing.png")
        pg.get_by_test_id("timeline").wait_for(timeout=15000)
        pg.screenshot(path=f"{OUT}{tag}-07-results.png")
        pg.screenshot(path=f"{OUT}{tag}-07b-results-full.png",full_page=True)
        L(tag+" ai banner vis",pg.get_by_test_id("banner-ai").is_visible()); L(tag+" synth vis",pg.get_by_test_id("banner-synthetic").is_visible())
        rows=pg.get_by_test_id("queue").locator("[data-state]").all()
        L(tag+" queue states",[r.get_attribute("data-state") for r in rows])
        L(tag+" queue ids",[r.get_attribute("data-testid") for r in rows])
        L(tag+" first focusable in results", pg.evaluate("()=>{const m=document.querySelector('#view-review');const f=m.querySelector('a[href],button,select,input,textarea,[tabindex]:not([tabindex=\"-1\"])');const r=f.closest('[data-state]');return f.outerHTML.slice(0,90)+' | row state='+(r?r.dataset.state:null)}"))
        L(tag+" queue rows tabindex",pg.evaluate("()=>[...document.querySelectorAll('[data-testid=queue] [data-state]')].map(e=>e.getAttribute('tabindex'))"))
        L(tag+" horiz scroll",pg.evaluate("()=>document.documentElement.scrollWidth>document.documentElement.clientWidth"))
        L(tag+" review-counts",pg.get_by_test_id("review-counts").inner_text() if pg.get_by_test_id("review-counts").count() else None)
        L(tag+" dates-to-confirm",pg.get_by_test_id("dates-to-confirm").inner_text()[:200])
        L(tag+" tray",pg.get_by_test_id("rejected-tray").inner_text()[:300])
        # ordering of sections
        L(tag+" section order",pg.evaluate("()=>[...document.querySelectorAll('[data-testid=timeline] > *')].map(e=>e.dataset.testid||e.className)"))
        e7=pg.get_by_test_id("entry-7"); e7.scroll_into_view_if_needed(); pg.screenshot(path=f"{OUT}{tag}-08-entry7.png")
        e7.get_by_test_id("entry-why").click(); pg.wait_for_timeout(400)
        L(tag+" why",pg.get_by_test_id("why-modal").inner_text())
        pg.screenshot(path=f"{OUT}{tag}-09-why7.png")
        pg.get_by_test_id("why-close").click()
        e8=pg.get_by_test_id("entry-8"); ex=e8.get_by_test_id("entry-excerpt").inner_text()
        e8.get_by_test_id("btn-source").click(); pg.wait_for_timeout(300)
        hl=pg.get_by_test_id("record-highlight").inner_text()
        L(tag+" e8 highlight==excerpt",re.sub(r"\s+"," ",hl).strip()==re.sub(r"\s+"," ",ex).strip()); L(tag+" e8 excerpt",ex[:100]); L(tag+" hl",hl[:100])
        pg.screenshot(path=f"{OUT}{tag}-10-source8.png")
        pg.get_by_test_id("btn-close-modal").click()
        # keyboard: tab order first 6
        L(tag+" errs",errs)
        ctx.close()
        # fail=4
        ctx=b.new_context(viewport={"width":W,"height":H}); pg=ctx.new_page()
        pg.goto(U+"&fail=4"); pg.get_by_test_id("btn-sample").click(); pg.get_by_test_id("record-count").wait_for(); pg.get_by_test_id("btn-analyze").click(); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        L(tag+" fail4 tray",pg.get_by_test_id("rejected-tray").inner_text()); pg.get_by_test_id("rejected-tray").scroll_into_view_if_needed()
        pg.screenshot(path=f"{OUT}{tag}-11-fail4.png")
        ctx.close()
    # dates to confirm via paste of case_01
    ctx=b.new_context(viewport={"width":1280,"height":900}); pg=ctx.new_page(); pg.goto(U)
    pg.get_by_test_id("input-text").fill(open("evals/golden/case_01_date_formats.txt").read()); pg.get_by_test_id("btn-analyze").click()
    pg.get_by_test_id("timeline").wait_for(timeout=15000)
    L("case01 dates-to-confirm",pg.get_by_test_id("dates-to-confirm").inner_text()[:500])
    pg.get_by_test_id("dates-to-confirm").scroll_into_view_if_needed(); pg.screenshot(path=OUT+"1280-12-dates-to-confirm.png")
    ctx.close()
    # keyboard walk on sample
    ctx=b.new_context(viewport={"width":1280,"height":900}); pg=ctx.new_page(); pg.goto(U); pg.get_by_test_id("btn-sample").click(); pg.get_by_test_id("record-count").wait_for(); pg.get_by_test_id("btn-analyze").click(); pg.get_by_test_id("timeline").wait_for(timeout=15000)
    seq=[]
    for i in range(8):
        pg.keyboard.press("Tab"); seq.append(pg.evaluate("()=>{const a=document.activeElement;return (a.dataset.testid||a.tagName)+':'+(a.textContent||'').trim().slice(0,20)}"))
    L("kbd tab order after load",seq)
    L("queue rows tabindex",pg.evaluate("()=>[...document.querySelectorAll('[data-testid=queue] [data-state]')].map(e=>e.getAttribute('tabindex'))"))
    r=pg.locator("[data-testid=queue] [data-state]").first; L("first row review attr",r.get_attribute("data-review")); 
    pg.screenshot(path=OUT+"1280-13-kbd.png")
    ctx.close()
    b.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:57:50.783Z

**tool call — Bash**
````
{
 "command": "git show 348cd0b -- app/frontend/ | head -250",
 "description": "Show the round-2 frontend diff"
}
````

### User / tool · 2026-11-02T01:57:50.877Z

**tool result**
````
commit 348cd0b46c0aecfab926d8ee48c7e553b6ccadfa
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:57:39 2026 -0600

    fix(frontend): entries-only count line, no false tray error, UX minors (T-042 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/input.js b/app/frontend/input.js
index 75cf094..f68f53d 100644
--- a/app/frontend/input.js
+++ b/app/frontend/input.js
@@ -37,6 +37,7 @@
     rd.readAsText(f);
   }
 
+  const recList = (c) => el("ul", { class: "reclist", "data-testid": "record-list" }, c.records.map((r) => el("li", {}, `Record ${r.seq}: ${r.source_label} — ${r.date_status === "parsed" || r.date_status === "confirmed" ? ZL.fmtDate(r.date_iso) : r.date_status === "ambiguous" ? "date to confirm" : "no readable date"}`)));
   ZL.renderInput = function (s) {
     const root = ZL.$("#input-body");
     const c = s.case, h = s.health;
@@ -62,9 +63,9 @@
     root.append(...[
       el("p", { class: "found", "data-testid": "record-count", role: "status" }, `${n} ${n === 1 ? "record" : "records"} found`),
       el("p", { class: "muted small" }, "Read by code only. No model has been called yet."),
-      el("ul", { class: "reclist", "data-testid": "record-list" }, c.records.map((r) => el("li", {}, `Record ${r.seq}: ${r.source_label} — ${r.date_status === "parsed" || r.date_status === "confirmed" ? ZL.fmtDate(r.date_iso) : r.date_status === "ambiguous" ? "date to confirm" : "no readable date"}`))),
+      c.status === "ready" ? el("details", { class: "reclist-wrap" }, el("summary", {}, `Records (${n})`), recList(c)) : recList(c),
       el("div", { class: "row" },
-        c.status === "ingested" ? el("button", { type: "button", class: "btn primary", "data-testid": "btn-analyze", onclick: startRun }, "Analyze") : null,
+        c.status === "ingested" && !(s.status && s.status.status === "running") ? el("button", { type: "button", class: "btn primary", "data-testid": "btn-analyze", onclick: startRun }, "Analyze") : null,
         el("button", { type: "button", class: "btn", "data-testid": "start-over", onclick: startOver }, "Start over")),
       running || (s.status && s.status.status === "running") ? el("p", { class: "progress", "data-testid": "status-stage", role: "status" }, (s.status && s.status.progress && s.status.progress.label) || "Working…") : null,
       s.status && s.status.status === "failed" ? el("p", { class: "error", role: "alert", "data-testid": "run-error" }, (s.status.error && s.status.error.message) || "The run failed. Finished items are kept.") : null,
@@ -72,6 +73,7 @@
   };
   async function startRun() {
     const s = ZL.state.get(); showError("");
+    ZL.state.set({ status: { status: "running", progress: { label: "Starting…" } } });
     try { await ZL.api.run(s.token, false); ZL.pollRun(); } catch (e) { showError(e.message); }
   }
   async function startOver() {
diff --git a/app/frontend/source.js b/app/frontend/source.js
index e013427..a5bfbe2 100644
--- a/app/frontend/source.js
+++ b/app/frontend/source.js
@@ -2,12 +2,13 @@
    (ABSOLUTE character offsets from the API, never computed from the model) highlighted. Used by entries here and by flags/charges in T-043. */
 (function () {
   const ZL = window.ZL, { el, clear } = ZL;
-  function recordView(rec, span, label) {
+  function recordView(rec, span, label, omitHead) {
     const box = el("section", { class: "src-rec", "data-testid": "record-section", "data-record-id": rec.id });
-    box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
+    if (!omitHead) box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
     const pre = el("pre", { class: "src-text" });
     const rs = span.start - rec.char_start, re = span.end - rec.char_start;
-    if (span.start == null || rs < 0 || re > rec.text.length || re <= rs) {
+    if (span.start == null) { pre.append(document.createTextNode(rec.text)); box.append(pre); return { box, mark: null }; } // whole-record view (no quote to highlight)
+    if (rs < 0 || re > rec.text.length || re <= rs) {
       pre.append(document.createTextNode(rec.text));
       box.append(pre, el("p", { class: "error", role: "alert", "data-testid": "highlight-missing" }, "The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record."));
       return { box, mark: null };
@@ -24,7 +25,7 @@
     let first = null;
     spans.forEach((sp) => {
       const rec = c.records.find((r) => r.id === sp.record_id); if (!rec) return;
-      const v = recordView(rec, sp); body.append(v.box); first = first || v.mark;
+      const v = recordView(rec, sp, null, spans.length === 1 && title && title.startsWith(`Record ${rec.seq}`)); body.append(v.box); first = first || v.mark;
     });
     if (!dlg.open) dlg.showModal();
     if (first) first.scrollIntoView({ block: "center" });
diff --git a/app/frontend/styles.css b/app/frontend/styles.css
index 4ca6dd8..856b8ef 100644
--- a/app/frontend/styles.css
+++ b/app/frontend/styles.css
@@ -52,3 +52,6 @@ mark{background:var(--mark);color:inherit;padding:0 1px;border-radius:2px}
 .checks{margin:0;padding-left:18px}.checks .bad{color:var(--bad);font-weight:700}
 .why-sentence{font-weight:600}
 @media (max-width:480px){.kv{grid-template-columns:1fr}.btn{min-height:44px}main{padding:0 8px 60px}}
+
+.btn[disabled]{opacity:.5;cursor:not-allowed}.entry,[tabindex],.btn{scroll-margin-top:90px}
+details.reclist-wrap summary{cursor:pointer;font-weight:600;min-height:36px}
diff --git a/app/frontend/timeline.js b/app/frontend/timeline.js
index d35ce74..f8f2a23 100644
--- a/app/frontend/timeline.js
+++ b/app/frontend/timeline.js
@@ -4,6 +4,7 @@
   const ZL = window.ZL, { el, clear } = ZL;
   let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological
 
+  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
   const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
   const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
     LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled" };
@@ -20,7 +21,7 @@
         el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
         el("span", { class: "provider", "data-testid": "entry-provider" }, e.provider),
         stateChip(e),
-        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, e.review_status)),
+        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status)),
       el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag" }, "AI-drafted") : null),
       e.edited ? el("p", { class: "muted small", "data-testid": "edited-note" }, "Edited by you. Original: " + e.edited.original_summary) : null,
       el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt),
@@ -79,7 +80,8 @@
   const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
   async function openWhy(id) {
     const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
-    ZL.$("#why-title").textContent = "Why? " + id;
+    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
+    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
     body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
     try {
       const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
@@ -89,10 +91,10 @@
         el("dl", { class: "kv", "data-testid": "why-ladder" },
           el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
           el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
-          lad.generator ? [el("dt", {}, "Generator"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
-            el("dt", {}, "Generator output"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
-          el("dt", {}, "Code checks"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
-          el("dt", {}, "Second check (judge)"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
+          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
+            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
+          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
+          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
         r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
     } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
   }
@@ -101,12 +103,12 @@
   ZL.renderReview = function (s) {
     const c = s.case, mount = ZL.$("#review-body"); clear(mount);
     if (!c || c.status !== "ready") return;
-    const counts = c.review && c.review.counts;
+    const nNeeds = c.entries.filter((e) => e.state === "needs_review").length, nVer = c.entries.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
     const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
     wrap.append(
       el("div", { class: "toolbar" },
-        el("h2", {}, `Timeline (${c.entries.length} entries)`),
-        counts ? el("span", { class: "muted small", "data-testid": "review-counts" }, `${counts.needs_review} need review · ${counts.verified} verified`) : null,
+        el("h2", {}, "Timeline"),
+        el("span", { class: "muted", "data-testid": "review-counts" }, `${c.entries.length} ${c.entries.length === 1 ? "entry" : "entries"} · ${nNeeds} needs review · ${nVer} verified`),
         el("label", { class: "muted small" }, "Order ",
           el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
             el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:57:54.305Z

**tool call — Bash**
````
{
 "command": "(lsof -nP -iTCP:7865 -iTCP:7867 -sTCP:LISTEN 2>&1 || true); ls app/frontend/; ls -la .venv/bin/python 2>&1; .venv/bin/python -c \"import playwright; print('playwright ok')\" 2>&1; python3 tools/board.py show T-042 2>&1 | head -40",
 "description": "Check ports, frontend files, venv Playwright, board card T-042"
}
````

### User / tool · 2026-11-02T01:57:54.542Z

**tool result**
````
api.js
app.js
charges.js
dev
dom.js
flags.js
index.html
input.js
mock.js
mock_sample.js
review.css
review.js
source.js
state.js
styles.css
timeline.js
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
playwright ok
---
id: "T-042"
title: "Frontend: input, banners, timeline, Why?, rejected tray, source-record modal"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: ["T-039"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:10Z"
updated_at: "2026-11-02T01:57:47Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T01:57:37Z"
rounds: 1
commits: ["117f2ec", "1da399d", "348cd0b"]
reviews:
  - {"persona": "ux-designer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-042-ux-designer.md", "at": "2026-11-02T01:56:55Z"}
ac:
  - {"n": 1, "text": "paste and .txt upload show '9 records found' before any model call; .pdf refused with a plain message; empty/oversize shows an error state (R-IN-1, R-IN-2, R-IN-4); proved by tests/e2e/test_input.py", "done": true, "evidence": "paste/.txt/sample -> record-count '9 records found' before run; .pdf -> role=alert plain msg; empty/oversize -> alert; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 2, "text": "timeline rows show date, provider, summary, excerpt, state; needs_review above verified; 'Dates to confirm' group after the timeline; rejected items in a 'could not verify' tray (R-TL-1, R-TL-5, R-IN-5); proved by test_timeline.py", "done": true, "evidence": "rows date/provider/summary/excerpt/state in queue (needs_review first), dates-to-confirm after timeline, rejected-tray; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 3, "text": "Why? on entry 7 shows check results, judge verdict, state and backend (R-TL-6); proved by test_timeline.py::test_why_entry7", "done": true, "evidence": "entry-why on entry 7: checks, judge, state, backend shown (why-modal); mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 4, "text": "opening entry 8's record highlights a span equal to the excerpt using API offsets (R-RV-9); proved by test_source_record.py::test_entry_highlight", "done": true, "evidence": "btn-source on entry 8: record-highlight text == entry-excerpt using excerpt_start/end - record.char_start; mock-API Playwright run /private/tmp/claude-501/fe_t042.py (29 checks, all pass, served with ?api=mock); real backend (:7860) not up yet, so e2e specs not run against it"}
  - {"n": 5, "text": "banner 'Synthetic data only — never paste real records' on every view and the AI banner on review (R-CO-5); `grep -c innerHTML app/frontend/*.js` is 0 (textContent only)", "done": true, "evidence": "banner-synthetic static in index.html (every view), banner-ai on review; grep -c innerHTML app/frontend/*.js = 0 for every file"}
  - {"n": 6, "text": "Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 \"could not process\" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason \"could not process\"'.", "done": true, "evidence": "mock ?fail=4: record 4 appears in rejected-tray with 'could not process' + reason (AC6 part for T-042)"}
  - {"n": 7, "text": "Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.", "done": true, "evidence": "bookkeeping item (depends_on edits) - not a frontend change; T-042 depends_on already T-039"}
---
## Description
Input and read-only timeline against the api.md examples (R-IN-1, R-IN-2, R-IN-4, R-IN-5, R-TL-1, R-TL-5, R-TL-6, R-RV-9, R-CO-5). Can start now from the API draft; integrates with the real API when m3-be-api-review lands.

Plan key: m3-fe-input-timeline (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 40 min.

## Notes (append-only, newest last)
- 2026-11-02T01:22:46Z orchestrator: AC 6 added: Contract review (T-018): T-042 AC2 append: 'with the stub backend failing every call for record 4, the UI shows record 4 "could not process" with the reason in the could-not-verify tray'. T-041 AC3 append: 'record 4 is listed under RECORDS NOT IN THE TREATMENT SECTION with reason "could not process"'.
- 2026-11-02T01:22:46Z orchestrator: AC 7 added: Contract review (T-018): T-031 depends_on += T-029. T-042 depends_on += T-039. T-043 depends_on += T-039, T-040. Or split T-043 AC3 into a mock-API AC and move the reload proof to T-045.
- 2026-11-02T01:22:47Z orchestrator: updated depends_on=['T-039']
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-042.md
- 2026-11-02T01:47:05Z frontend: claimed
- 2026-11-02T01:47:05Z frontend: Claimed with --force (T-039 in progress; building against api.md + mock layer). Shared module layout proposed for frontend-2/T-043: app/frontend/{index.html,styles.css,api.js (API_MODE const mock|real, fetch + mock),state.js (store+subscribe),dom.js (el() helper, textContent only),input.js,timeline.js,source.js,app.js (T-042 owned); flags.js,charges.js,review.js (T-043 owned)}. Hooks: window.ZL.state, ZL.api, ZL.dom.el, ZL.openSource(recordId, spans), ZL.registerPanel(name, renderFn) for T-043 panels, mount point <div id=side-panels>.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:00.258Z

**tool call — Bash**
````
{
 "command": "nohup .venv/bin/python -m http.server 7867 --directory app/frontend > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/server7867.log 2>&1 &\nsleep 2; curl -s -o /dev/null -w \"%{http_code}\\n\" \"http://localhost:7867/index.html?api=mock\"; grep -n \"review-counts\\|counts\\|needs_review\\|verified\" app/frontend/mock.js | head -40",
 "description": "Serve frontend on port 7867 and check mock counts source"
}
````

### User / tool · 2026-11-02T01:58:02.374Z

**tool result**
````
200
88:      const needs = sample && r.seq === 3; const state = needs ? "needs_review" : "verified";
94:      else { e.state = "needs_review"; e.reasons = ["DATE_AMBIGUOUS"]; e.why = "The date can be read two ways; confirm which one is right."; undated.push(e);
101:          excerpt: sent.text, excerpt_start: sent.start, excerpt_end: sent.end, state: rate ? "needs_review" : "verified", reasons: rate ? ["AMOUNT_RATE_NOT_TOTALED"] : [],
103:          review_status: "pending", edited: null, duplicate_note: null, ladder: { item_id: "a" + (amounts.length + 1), state: rate ? "needs_review" : "verified", backend: "fixture", generator: null,
114:        origin: "code", reviewer_note: null, state: "verified", reasons: [], why: "Calculated by code from two dates read from the record headers.", review_status: "pending", edited: null,
115:        ladder: { item_id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, state: "verified", backend: "fixture", generator: null, code_checks: { dates_parsed: true, days, threshold: 30 }, judge: null, human: { action: null } } });
117:    const queue = [...undated, ...entries].filter((e) => e.state === "needs_review").map((e) => e.id).concat(entries.filter((e) => e.state !== "needs_review").map((e) => e.id));
131:    c.review = { queue: c._queue, counts: { pending: n((i) => i.review_status === "pending"), accepted: n((i) => i.review_status === "accepted"), edited: n((i) => i.review_status === "edited"),
132:      dismissed: n((i) => i.review_status === "dismissed"), needs_review: n((i) => i.state === "needs_review"), verified: n((i) => i.state === "verified"), rejected: c.tray.length }, ready_to_export: false };
172:          progress: { done: Math.round(frac * total), total, label: `Checking summaries ${Math.round(frac * total)} of ${total}` }, counts: { entries: c.entries.length, amounts: c.amounts.length, flags: c.flags.length }, error: null, elapsed_ms: Date.now() - c._run });
199:        const e = c.undated_entries.splice(i, 1)[0]; e.date = d; e.date_status = "confirmed"; e.state = "verified"; e.reasons = []; c.entries.push(e);
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:08.357Z

**tool call — Bash**
````
{
 "command": "cat -n app/frontend/timeline.js | sed -n 1,140p",
 "description": "Read timeline.js renderer"
}
````

### User / tool · 2026-11-02T01:58:08.440Z

**tool result**
````
     1	/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
     2	   T-043 plugs in through ZL.registerRowActions(fn(entry,rowEl)) and ZL.registerPanel(fn(case, mountEl)). */
     3	(function () {
     4	  const ZL = window.ZL, { el, clear } = ZL;
     5	  let sortMode = "review"; // "review" = needs_review first, then by date; "date" = chronological
     6	
     7	  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
     8	  const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
     9	  const REASON = { JUDGE_PARTIAL: "part of the summary isn't fully supported by the quote", JUDGE_UNSUPPORTED: "the summary isn't supported by the quote", DATE_AMBIGUOUS: "the date can be read two ways",
    10	    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled" };
    11	  const reasonText = (r) => REASON[r] || String(r).toLowerCase().replace(/_/g, " ");
    12	
    13	  function stateChip(e) {
    14	    return el("span", { class: "chip st-" + e.state, "data-testid": "entry-state" }, STATE_LABEL[e.state] || e.state);
    15	  }
    16	  function entryRow(e, c) {
    17	    const rec = c.records.find((r) => r.id === e.record_ids[0]);
    18	    const row = el("article", { class: "entry st-" + e.state, "data-testid": "entry-" + e.seq, "data-entry-id": e.id, "data-state": e.state });
    19	    row.append(...[
    20	      el("div", { class: "entry-head" },
    21	        el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
    22	        el("span", { class: "provider", "data-testid": "entry-provider" }, e.provider),
    23	        stateChip(e),
    24	        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status)),
    25	      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag" }, "AI-drafted") : null),
    26	      e.edited ? el("p", { class: "muted small", "data-testid": "edited-note" }, "Edited by you. Original: " + e.edited.original_summary) : null,
    27	      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt),
    28	      e.duplicate_note ? el("p", { class: "muted small" }, e.duplicate_note) : null,
    29	      e.state === "needs_review" && e.reasons.length ? el("p", { class: "reason", "data-testid": "entry-reasons" }, "Check: " + e.reasons.map(reasonText).join("; ")) : null,
    30	      el("div", { class: "row-actions", "data-testid": "row-actions" },
    31	        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
    32	        el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, "Open record"))].filter(Boolean));
    33	    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    34	    return row;
    35	  }
    36	  function sortedEntries(c) {
    37	    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    38	    const list = c.entries.slice().sort(byDate);
    39	    if (sortMode === "date") return list;
    40	    const rank = (e) => (e.state === "needs_review" ? 0 : 1);
    41	    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
    42	  }
    43	  function datesToConfirm(c) {
    44	    const box = el("section", { class: "group", "data-testid": "dates-to-confirm" }, el("h2", {}, "Dates to confirm"));
    45	    if (!c.undated_entries.length && !c.dates_to_confirm.length) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    46	    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    47	    c.undated_entries.forEach((e) => {
    48	      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
    49	      const rec = c.records.find((r) => r.id === e.record_ids[0]);
    50	      const row = entryRow(e, c); row.classList.add("undated");
    51	      if (d && d.candidates.length) {
    52	        const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${d.date_raw}”. Which date?`));
    53	        d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn small", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
    54	          try { await ZL.api.confirmDate(ZL.state.get().token, d.record_id, cand); ZL.state.set({ case: await ZL.api.getCase(ZL.state.get().token) }); } catch (er) { alert(er.message); }
    55	        } }, ZL.fmtDate(cand))));
    56	        row.insertBefore(bar, row.querySelector(".row-actions"));
    57	      } else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
    58	      box.append(row);
    59	    });
    60	    return box;
    61	  }
    62	  function tray(c) {
    63	    const box = el("section", { class: "group tray", "data-testid": "rejected-tray" }, el("h2", {}, `Could not verify (${c.tray.length})`));
    64	    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here. Every record produced an entry that passed the code checks.")); return box; }
    65	    box.append(el("p", { class: "muted small" }, "These records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    66	    c.tray.forEach((t) => {
    67	      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
    68	      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
    69	        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip st-rejected" }, "Could not verify")),
    70	        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
    71	        el("p", { class: "summary" }, t.why),
    72	        t.attempt ? el("p", { class: "muted small" }, "The model's attempt (not used): " + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
    73	        el("div", { class: "row-actions" }, recs.map((r) => el("button", { type: "button", class: "btn small", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
    74	      box.append(item);
    75	    });
    76	    return box;
    77	  }
    78	
    79	  // ---- Why? panel
    80	  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
    81	  async function openWhy(id) {
    82	    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    83	    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
    84	    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
    85	    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    86	    try {
    87	      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
    88	      clear(body);
    89	      body.append(...[
    90	        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
    91	        el("dl", { class: "kv", "data-testid": "why-ladder" },
    92	          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
    93	          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
    94	          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
    95	            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
    96	          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
    97	          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
    98	        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · " + cl.verdict : ""}`)))) : null].filter(Boolean));
    99	    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
   100	  }
   101	  ZL.openWhy = openWhy;
   102	
   103	  ZL.renderReview = function (s) {
   104	    const c = s.case, mount = ZL.$("#review-body"); clear(mount);
   105	    if (!c || c.status !== "ready") return;
   106	    const nNeeds = c.entries.filter((e) => e.state === "needs_review").length, nVer = c.entries.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
   107	    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
   108	    wrap.append(
   109	      el("div", { class: "toolbar" },
   110	        el("h2", {}, "Timeline"),
   111	        el("span", { class: "muted", "data-testid": "review-counts" }, `${c.entries.length} ${c.entries.length === 1 ? "entry" : "entries"} · ${nNeeds} needs review · ${nVer} verified`),
   112	        el("label", { class: "muted small" }, "Order ",
   113	          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
   114	            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
   115	      el("div", { class: "timeline", "data-testid": "queue" }, sortedEntries(c).map((e) => entryRow(e, c))),
   116	      datesToConfirm(c), tray(c));
   117	    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
   118	    ZL.hooks.panels.forEach((fn) => fn(c, side));
   119	  };
   120	})();
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:08.780Z

**tool call — Bash**
````
{
 "command": "cat -n app/frontend/source.js | sed -n 1,45p; echo ----; grep -n \"rejected-tray\\|tray\" app/frontend/*.js | head -30",
 "description": "Read source.js and find tray markup"
}
````

### User / tool · 2026-11-02T01:58:08.867Z

**tool result**
````
     1	/* Source-record modal (R-RV-9). ZL.openSource([{record_id, start, end}]) opens the full record text(s) with the span [start,end)
     2	   (ABSOLUTE character offsets from the API, never computed from the model) highlighted. Used by entries here and by flags/charges in T-043. */
     3	(function () {
     4	  const ZL = window.ZL, { el, clear } = ZL;
     5	  function recordView(rec, span, label, omitHead) {
     6	    const box = el("section", { class: "src-rec", "data-testid": "record-section", "data-record-id": rec.id });
     7	    if (!omitHead) box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
     8	    const pre = el("pre", { class: "src-text" });
     9	    const rs = span.start - rec.char_start, re = span.end - rec.char_start;
    10	    if (span.start == null) { pre.append(document.createTextNode(rec.text)); box.append(pre); return { box, mark: null }; } // whole-record view (no quote to highlight)
    11	    if (rs < 0 || re > rec.text.length || re <= rs) {
    12	      pre.append(document.createTextNode(rec.text));
    13	      box.append(pre, el("p", { class: "error", role: "alert", "data-testid": "highlight-missing" }, "The exact position of this quote could not be found in the record, so nothing is highlighted. Check the whole record."));
    14	      return { box, mark: null };
    15	    }
    16	    const mark = el("mark", { "data-testid": "record-highlight", tabindex: "-1" }, rec.text.slice(rs, re));
    17	    pre.append(document.createTextNode(rec.text.slice(0, rs)), mark, document.createTextNode(rec.text.slice(re)));
    18	    box.append(pre);
    19	    return { box, mark };
    20	  }
    21	  ZL.openSource = function (spans, title) {
    22	    const c = ZL.state.get().case; if (!c) return;
    23	    const dlg = ZL.$("#source-modal"), body = ZL.$("#source-body"); clear(body);
    24	    ZL.$("#source-title").textContent = title || "Source record";
    25	    let first = null;
    26	    spans.forEach((sp) => {
    27	      const rec = c.records.find((r) => r.id === sp.record_id); if (!rec) return;
    28	      const v = recordView(rec, sp, null, spans.length === 1 && title && title.startsWith(`Record ${rec.seq}`)); body.append(v.box); first = first || v.mark;
    29	    });
    30	    if (!dlg.open) dlg.showModal();
    31	    if (first) first.scrollIntoView({ block: "center" });
    32	  };
    33	  ZL.entrySpans = (e) => e.record_ids.map((rid) => ({ record_id: rid, start: e.excerpt_start, end: e.excerpt_end }));
    34	  document.addEventListener("DOMContentLoaded", () => {
    35	    ZL.$("#source-close").addEventListener("click", () => ZL.$("#source-modal").close());
    36	  });
    37	})();
----
app/frontend/charges.js:2:   unclear tray for rates / estimates / damages / unreadable amounts (R-CH-3, R-CH-5, D-019). Charges: accept or dismiss only (D-010). */
app/frontend/charges.js:10:  // One-line description for the unclear tray. Wording comes from the amount's kind and the quoted line; nothing is computed.
app/frontend/charges.js:67:    const tray = el("section", { class: "rv-tray", "data-testid": "unclear-tray", "aria-labelledby": "rv-unclear-h" },
app/frontend/charges.js:69:    if (unclear.length) tray.append(table(c, unclear, "Unclear amounts, not totaled", true)); else tray.append(el("p", { class: "rv-empty" }, "Nothing unclear."));
app/frontend/charges.js:70:    root.append(tray);
app/frontend/mock.js:3:   Mock switches (URL query): ?fail=4 makes the stub backend fail every call for record 4 (tray shows "could not process"). */
app/frontend/mock.js:78:    const records = parseRecords(text); const entries = [], undated = [], tray = [], amounts = [], flags = [], toConfirm = [];
app/frontend/mock.js:82:        tray.push({ id: "e" + r.seq + "x", kind: "entry", record_ids: [r.id], state: "rejected", reasons: ["LLM_CALL_FAILED"],
app/frontend/mock.js:119:      undated_entries: undated, entries, amounts, totals: null, flags, tray, dates_to_confirm: toConfirm, injection: { records: [], banner: null }, review: null, warnings: [], created_at: new Date().toISOString(), updated_at: new Date().toISOString(), _queue: queue, _run: 0 };
app/frontend/mock.js:132:      dismissed: n((i) => i.review_status === "dismissed"), needs_review: n((i) => i.state === "needs_review"), verified: n((i) => i.state === "verified"), rejected: c.tray.length }, ready_to_export: false };
app/frontend/mock.js:138:  const view = (c) => { const v = clone(c); delete v._queue; delete v._run; if (c.status !== "ready") { if (c.status === "ingested") { v.entries = []; v.undated_entries = []; v.amounts = []; v.flags = []; v.tray = []; } } return v; };
app/frontend/mock.js:175:        const id = decodeURIComponent(m[1]); const it = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags, ...c.tray].find((x) => x.id === id);
app/frontend/timeline.js:1:/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
app/frontend/timeline.js:62:  function tray(c) {
app/frontend/timeline.js:63:    const box = el("section", { class: "group tray", "data-testid": "rejected-tray" }, el("h2", {}, `Could not verify (${c.tray.length})`));
app/frontend/timeline.js:64:    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here. Every record produced an entry that passed the code checks.")); return box; }
app/frontend/timeline.js:66:    c.tray.forEach((t) => {
app/frontend/timeline.js:68:      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
app/frontend/timeline.js:70:        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
app/frontend/timeline.js:116:      datesToConfirm(c), tray(c));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:34.158Z

**tool call — Bash**
````
{
 "command": "grep -n \"view-review\\|source-modal\\|why-modal\\|id=\\\"source\\|id=\\\"why\" app/frontend/index.html | head; grep -n \"banner\" app/frontend/styles.css | head -5; sed -n 1,12p app/frontend/mock.js | cut -c1-240",
 "description": "Check view and modal ids in index.html and banner css"
}
````

### User / tool · 2026-11-02T01:58:34.251Z

**tool result**
````
24:  <section id="view-review" class="card" aria-labelledby="h-review" hidden>
29:<dialog id="source-modal" data-testid="record-modal" aria-labelledby="source-title">
30:  <div class="dlg-head"><h2 id="source-title">Source record</h2><button type="button" id="source-close" class="btn small" data-testid="btn-close-modal">Close</button></div>
31:  <div id="source-body"></div>
33:<dialog id="why-modal" data-testid="why-modal" aria-labelledby="why-title">
34:  <div class="dlg-head"><h2 id="why-title">Why?</h2><button type="button" class="btn small" data-testid="why-close" onclick="this.closest('dialog').close()">Close</button></div>
35:  <div id="why-body"></div>
7:.banner{padding:8px 16px;font-weight:600;text-align:center}
8:.banner.synth{background:#b42318;color:#fff;position:sticky;top:0;z-index:5}
9:.banner.ai{background:var(--aibg);border-bottom:1px solid var(--line);font-weight:500}
/* In-memory mock of the api.md contract (shapes copied from memory/contracts/api.md). Dev/test only: used while API_MODE === "mock".
   Parses `=== Record N ===` / Date: / Source: / Excerpt: blocks from the pasted text like the real ingest does (offsets are absolute).
   Mock switches (URL query): ?fail=4 makes the stub backend fail every call for record 4 (tray shows "could not process"). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const SAMPLE_SUMMARIES = {
    1: "Restrained driver rear-ended at approx. 35 mph; reported neck pain 7/10 and headache; transported to Central ER.",
    2: "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
    3: "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.",
    4: "Cervical range of motion reduced approx. 40%; plan of care is 12 visits.",
    5: "Pain 4/10, improving; patient reports missing 3 days of work.",
    6: "Discharged from PT after two missed appointments; pain 3/10.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:50.336Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-walk.py",
 "content": "\"\"\"T-042 round 2 (commit 348cd0b) UX re-check, ux-designer-reviewer.\nServed: python3 -m http.server 7867 --directory app/frontend  (mock API via ?api=mock).\nRun from project root: .venv/bin/python artifacts/review-evidence/T-042-r2-ux-designer-walk.py\nWrites T-042-r2-* screenshots and prints every check as JSON-ish lines.\n\"\"\"\nimport re, json\nfrom playwright.sync_api import sync_playwright\n\nBASE = \"http://localhost:7867/index.html?api=mock\"\nOUT = \"artifacts/review-evidence/T-042-r2-\"\nRES = {}\n\n\ndef rec(k, v):\n    RES[k] = v\n    print(k, \"=>\", json.dumps(v, ensure_ascii=False))\n\n\ndef run_sample(pg, fail=False):\n    pg.goto(BASE + (\"&fail=4\" if fail else \"\"))\n    pg.get_by_test_id(\"btn-sample\").click()\n    pg.get_by_test_id(\"record-count\").wait_for()\n    pg.get_by_test_id(\"btn-analyze\").click()\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n    pg.wait_for_timeout(300)\n\n\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for W, H, tag in ((1280, 900, \"1280\"), (375, 812, \"375\")):\n        # ---------- A. header counts vs rows (round-1 major)\n        ctx = b.new_context(viewport={\"width\": W, \"height\": H}); pg = ctx.new_page()\n        errs = []\n        pg.on(\"pageerror\", lambda e: errs.append(\"PAGEERROR \" + str(e)))\n        pg.on(\"console\", lambda m: errs.append(\"CONSOLE \" + m.text) if m.type == \"error\" else None)\n        run_sample(pg)\n        hdr = pg.get_by_test_id(\"review-counts\").inner_text()\n        rec(f\"{tag} A1 review-counts text\", hdr)\n        rec(f\"{tag} A1 toolbar h2\", pg.locator(\"#review-body .toolbar h2\").first.inner_text())\n        rows = pg.get_by_test_id(\"queue\").locator(\"[data-state]\").all()\n        states = [r.get_attribute(\"data-state\") for r in rows]\n        n_rows = len(rows); n_need = states.count(\"needs_review\"); n_ver = states.count(\"verified\")\n        m = re.search(r\"(\\d+) entr(?:y|ies) · (\\d+) needs review · (\\d+) verified\", hdr)\n        hdr_n = tuple(int(x) for x in m.groups()) if m else None\n        rec(f\"{tag} A2 rows total/needs_review/verified\", [n_rows, n_need, n_ver])\n        rec(f\"{tag} A2 header entries/needs/verified\", hdr_n)\n        rec(f\"{tag} A2 header reconciles with rows\", hdr_n == (n_rows, n_need, n_ver))\n        rec(f\"{tag} A2 review-status chip texts\", sorted(set(pg.locator(\"[data-testid=review-status]\").all_inner_texts())))\n        rec(f\"{tag} A2 state chip texts\", sorted(set(pg.locator(\"[data-testid=entry-state]\").all_inner_texts())))\n        rec(f\"{tag} A3 dates-to-confirm text\", pg.get_by_test_id(\"dates-to-confirm\").inner_text()[:160])\n        rec(f\"{tag} A3 tray heading\", pg.get_by_test_id(\"rejected-tray\").locator(\"h2\").inner_text())\n        pg.get_by_test_id(\"review-counts\").scroll_into_view_if_needed()\n        pg.screenshot(path=f\"{OUT}{tag}-01-results-header.png\")\n        pg.screenshot(path=f\"{OUT}{tag}-02-results-viewport.png\")\n\n        # first needs_review row position and first focusable in review region\n        e3 = pg.locator(\"[data-testid=queue] [data-state=needs_review]\").first\n        rec(f\"{tag} A4 first needs_review row top (px, page coords)\", pg.evaluate(\"(el)=>el.getBoundingClientRect().top+window.scrollY\", e3.element_handle()))\n        rec(f\"{tag} A4 first focusable in #view-review\", pg.evaluate(\n            \"()=>{const f=document.querySelector('#view-review').querySelector('a[href],button,select,input,textarea,[tabindex]:not([tabindex=\\\"-1\\\"])');const r=f.closest('[data-state]');return (f.outerHTML||'').slice(0,80)+' | row state='+(r?r.dataset.state:null)}\"))\n        rec(f\"{tag} A4 records list is collapsed <details>\", pg.evaluate(\"()=>{const d=document.querySelector('details.reclist-wrap');return d?{present:true,open:d.open,summary:d.querySelector('summary').textContent}:{present:false}}\"))\n\n        # ---------- B. why? vocabulary (round-1 minor)\n        pg.get_by_test_id(\"entry-7\").get_by_test_id(\"entry-why\").click(); pg.wait_for_timeout(400)\n        rec(f\"{tag} B1 why-title\", pg.locator(\"#why-title\").inner_text())\n        rec(f\"{tag} B1 why-ladder text\", pg.get_by_test_id(\"why-ladder\").inner_text())\n        rec(f\"{tag} B1 why-text\", pg.get_by_test_id(\"why-text\").inner_text())\n        rec(f\"{tag} B1 why-modal full text\", pg.get_by_test_id(\"why-modal\").inner_text()[:900])\n        pg.screenshot(path=f\"{OUT}{tag}-03-why7.png\")\n        pg.get_by_test_id(\"why-close\").click()\n\n        # ---------- C. source modal from entry 8 (duplicate heading, round-1 nit)\n        e8 = pg.get_by_test_id(\"entry-8\")\n        e8.get_by_test_id(\"btn-source\").click(); pg.wait_for_timeout(300)\n        rec(f\"{tag} C1 entry-8 modal h3 count\", pg.locator(\"#source-body h3\").count())\n        rec(f\"{tag} C1 entry-8 modal title\", pg.locator(\"#source-title\").inner_text())\n        rec(f\"{tag} C1 entry-8 role=alert inside modal\", pg.locator(\"#source-modal [role=alert]\").count())\n        pg.screenshot(path=f\"{OUT}{tag}-04-source8.png\")\n        pg.get_by_test_id(\"btn-close-modal\").click()\n\n        # ---------- D. sticky banner vs focus (round-1 minor; 375 only meaningful)\n        bn = pg.get_by_test_id(\"banner-synthetic\").bounding_box()\n        rec(f\"{tag} D1 synthetic banner box\", {\"top\": bn[\"y\"], \"bottom\": bn[\"y\"] + bn[\"height\"]})\n        rec(f\"{tag} D1 banner position\", pg.evaluate(\"()=>getComputedStyle(document.querySelector('[data-testid=banner-synthetic]')).position\"))\n        obscured = []\n        seq = []\n        for _ in range(12):\n            pg.keyboard.press(\"Tab\")\n            info = pg.evaluate(\"\"\"()=>{const a=document.activeElement;const r=a.getBoundingClientRect();\n              const b=document.querySelector('[data-testid=banner-synthetic]').getBoundingClientRect();\n              return {label:((a.dataset.testid||a.tagName)+':'+(a.textContent||'').trim().slice(0,18)), top:r.top, bottom:r.bottom, bTop:b.top, bBottom:b.bottom}}\"\"\")\n            seq.append(info[\"label\"])\n            if info[\"top\"] < info[\"bBottom\"] and info[\"bottom\"] > info[\"bTop\"] and info[\"label\"].split(\":\")[0] != \"banner-synthetic\":\n                obscured.append(info[\"label\"])\n        rec(f\"{tag} D1 keyboard tab labels (12 Tabs from results-page focus)\", seq)\n        rec(f\"{tag} D1 focused elements overlapped by sticky banner\", obscured)\n        rec(f\"{tag} D2 horizontal scroll\", pg.evaluate(\"()=>document.documentElement.scrollWidth>document.documentElement.clientWidth\"))\n        rec(f\"{tag} console/page errors\", errs)\n        ctx.close()\n\n        # ---------- E. tray record (round-1 minor: false red alert)\n        ctx = b.new_context(viewport={\"width\": W, \"height\": H}); pg = ctx.new_page()\n        run_sample(pg, fail=True)\n        tray_rec = pg.get_by_test_id(\"rejected-tray\").inner_text()\n        rec(f\"{tag} E1 tray text (first 260)\", tray_rec[:260])\n        alerts_before = pg.locator(\"[role=alert]\").count()\n        rec(f\"{tag} E1 role=alert count on page before opening tray record\", alerts_before)\n        pg.get_by_test_id(\"rejected-tray\").get_by_role(\"button\", name=re.compile(\"Open record\")).first.click()\n        pg.wait_for_timeout(400)\n        rec(f\"{tag} E2 source-modal open\", pg.locator(\"#source-modal\").evaluate(\"d=>d.open\"))\n        rec(f\"{tag} E2 role=alert inside record-modal\", pg.locator(\"#source-modal [role=alert]\").count())\n        rec(f\"{tag} E2 highlight-missing testid count\", pg.get_by_test_id(\"highlight-missing\").count())\n        rec(f\"{tag} E2 role=alert on page after opening tray record\", pg.locator(\"[role=alert]\").count())\n        rec(f\"{tag} E2 record-modal text (first 220)\", pg.locator(\"#source-body\").inner_text()[:220])\n        pg.screenshot(path=f\"{OUT}{tag}-05-tray-open-record.png\")\n        pg.get_by_test_id(\"btn-close-modal\").click()\n\n        # control: a real bad span must still raise the alert (fix must not suppress genuine failures)\n        pg.evaluate(\"()=>{const c=ZL.state.get().case; ZL.openSource([{record_id:c.records[0].id,start:-5,end:3}],'control bad span')}\")\n        pg.wait_for_timeout(200)\n        rec(f\"{tag} E3 control bad-offset span: role=alert inside modal\", pg.locator(\"#source-modal [role=alert]\").count())\n        rec(f\"{tag} E3 control bad-offset testid\", pg.get_by_test_id(\"highlight-missing\").count())\n        pg.screenshot(path=f\"{OUT}{tag}-06-control-bad-span.png\")\n        ctx.close()\n\n        # ---------- F. Analyze during run (round-1 minor)\n        ctx = b.new_context(viewport={\"width\": W, \"height\": H}); pg = ctx.new_page()\n        pg.goto(BASE)\n        pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for()\n        pg.get_by_test_id(\"btn-analyze\").click()\n        samples = []\n        for t in (0, 300, 700):\n            pg.wait_for_timeout(0 if t == 0 else 300)\n            samples.append({\"t_ms\": t, \"analyze_buttons\": pg.get_by_test_id(\"btn-analyze\").count(),\n                            \"stage\": pg.get_by_test_id(\"status-stage\").inner_text() if pg.get_by_test_id(\"status-stage\").count() else None})\n        rec(f\"{tag} F1 during run\", samples)\n        if tag == \"1280\":\n            pg.screenshot(path=f\"{OUT}{tag}-07-processing.png\")\n        pg.get_by_test_id(\"timeline\").wait_for(timeout=20000)\n        ctx.close()\n\n    # ---------- G. input-side regressions (empty, oversize, pdf) - quick\n    ctx = b.new_context(viewport={\"width\": 1280, \"height\": 900}); pg = ctx.new_page(); pg.goto(BASE)\n    pg.get_by_test_id(\"btn-analyze\").click() if pg.get_by_test_id(\"btn-analyze\").count() else pg.get_by_test_id(\"input-text\").fill(\"\")\n    pg.evaluate(\"()=>{}\")\n    pg.get_by_test_id(\"input-text\").fill(\"keep me \" + \"x\" * 10)\n    pg.get_by_test_id(\"input-text\").fill(\"=== Record 1 ===\\n\" + \"x\" * 600000)\n    pg.get_by_test_id(\"btn-analyze\").click() if pg.get_by_test_id(\"btn-analyze\").count() else None\n    pg.wait_for_timeout(300)\n    rec(\"G1 oversize alert\", pg.get_by_role(\"alert\").first.inner_text() if pg.get_by_role(\"alert\").count() else None)\n    rec(\"G1 textarea length kept\", len(pg.get_by_test_id(\"input-text\").input_value()))\n    ctx.close()\n    b.close()\n\njson.dump(RES, open(OUT + \"ux-designer-check.out.json\", \"w\"), ensure_ascii=False, indent=1)\nprint(\"WROTE\", OUT + \"ux-designer-check.out.json\")\n"
}
````

### User / tool · 2026-11-02T01:58:50.432Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-walk.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:54.536Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-walk.py",
 "old_string": "    ctx = b.new_context(viewport={\"width\": 1280, \"height\": 900}); pg = ctx.new_page(); pg.goto(BASE)\n    pg.get_by_test_id(\"btn-analyze\").click() if pg.get_by_test_id(\"btn-analyze\").count() else pg.get_by_test_id(\"input-text\").fill(\"\")\n    pg.evaluate(\"()=>{}\")\n    pg.get_by_test_id(\"input-text\").fill(\"keep me \" + \"x\" * 10)\n    pg.get_by_test_id(\"input-text\").fill(\"=== Record 1 ===\\n\" + \"x\" * 600000)\n    pg.get_by_test_id(\"btn-analyze\").click() if pg.get_by_test_id(\"btn-analyze\").count() else None\n    pg.wait_for_timeout(300)\n    rec(\"G1 oversize alert\", pg.get_by_role(\"alert\").first.inner_text() if pg.get_by_role(\"alert\").count() else None)\n    rec(\"G1 textarea length kept\", len(pg.get_by_test_id(\"input-text\").input_value()))\n    ctx.close()",
 "new_string": "    ctx = b.new_context(viewport={\"width\": 1280, \"height\": 900}); pg = ctx.new_page(); pg.goto(BASE)\n    pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(200)\n    rec(\"G0 empty-submit alert\", pg.get_by_role(\"alert\").first.inner_text() if pg.get_by_role(\"alert\").count() else None)\n    pg.get_by_test_id(\"input-text\").fill(\"=== Record 1 ===\\n\" + \"x\" * 600000)\n    pg.get_by_test_id(\"btn-analyze\").click(); pg.wait_for_timeout(300)\n    rec(\"G1 oversize alert\", pg.get_by_role(\"alert\").first.inner_text() if pg.get_by_role(\"alert\").count() else None)\n    rec(\"G1 textarea length kept\", len(pg.get_by_test_id(\"input-text\").input_value()))\n    ctx.close()"
}
````

### User / tool · 2026-11-02T01:58:54.636Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-walk.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:55.899Z

**tool call — Bash**
````
{
 "command": "timeout 400 .venv/bin/python artifacts/review-evidence/T-042-r2-ux-designer-walk.py 2>&1 | tail -150",
 "description": "Run round-2 T-042 Playwright walk against port 7867",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T01:58:55.988Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:58:57.304Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-042-r2-ux-designer-walk.py 2>&1 | tail -150",
 "description": "Run round-2 T-042 Playwright walk against port 7867",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T01:59:18.476Z

**tool result**
````
1280 A1 review-counts text => "9 entries · 1 needs review · 8 verified"
1280 A1 toolbar h2 => "Timeline"
1280 A2 rows total/needs_review/verified => [9, 1, 8]
1280 A2 header entries/needs/verified => [9, 1, 8]
1280 A2 header reconciles with rows => true
1280 A2 review-status chip texts => ["Not reviewed yet"]
1280 A2 state chip texts => ["Needs review", "Verified"]
1280 A3 dates-to-confirm text => "Dates to confirm\n\nNone. Every record has a readable date."
1280 A3 tray heading => "Could not verify (0)"
1280 A4 first needs_review row top (px, page coords) => 444.5
1280 A4 first focusable in #view-review => "<select data-testid=\"sort\"><option value=\"review\" selected=\"\">Needs review first | row state=null"
1280 A4 records list is collapsed <details> => {"present": true, "open": false, "summary": "Records (9)"}
1280 B1 why-title => "Why? Hill Country Pain Management, new patient, 2026-05-18"
1280 B1 why-ladder text => "State\nverified\nBackend\nfixture\nDrafted by\nclaude-sonnet-5-5 · extract_v1\nAI draft\nSummary: New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered. Excerpt: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.\nChecks run by code\nexcerpt verbatim: passed\nexcerpt whole sentence: passed\nqualifier carried: passed\ndate provider from header: passed\nsummary tokens not in excerpt: none\nhighlight found: passed\nSecond check by another model\nsupported · claude-haiku-5-5 · judge_faithfulness_v1"
1280 B1 why-text => "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
1280 B1 why-modal full text => "Why? Hill Country Pain Management, new patient, 2026-05-18\nClose\n\nQuote found word for word, every number in the summary is in the quote, and the second check agreed.\n\nState\nverified\nBackend\nfixture\nDrafted by\nclaude-sonnet-5-5 · extract_v1\nAI draft\nSummary: New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered. Excerpt: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.\nChecks run by code\nexcerpt verbatim: passed\nexcerpt whole sentence: passed\nqualifier carried: passed\ndate provider from header: passed\nsummary tokens not in excerpt: none\nhighlight found: passed\nSecond check by another model\nsupported · claude-haiku-5-5 · judge_faithfulness_v1\nModel calls (2)"
1280 C1 entry-8 modal h3 count => 0
1280 C1 entry-8 modal title => "Record 8: Austin Imaging, cervical MRI"
1280 C1 entry-8 role=alert inside modal => 0
1280 D1 synthetic banner box => {"top": 0, "bottom": 40}
1280 D1 banner position => "sticky"
1280 D1 keyboard tab labels (12 Tabs from results-page focus) => ["btn-accept:Accept", "btn-edit:Edit", "btn-dismiss:Dismiss", "entry-9:2026-06-12Hill Cou", "entry-why:Why?", "btn-source:Open record", "btn-accept:Accept", "btn-edit:Edit", "btn-dismiss:Dismiss", "flag-f_gap_r6_r7:Gap of 73 daysVeri", "btn-source:Open records 6 and", "btn-accept:Accept"]
1280 D1 focused elements overlapped by sticky banner => []
1280 D2 horizontal scroll => false
1280 console/page errors => []
1280 E1 tray text (first 260) => "Could not verify (1)\n\nThese records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself.\n\nRecord 4: Capital PT, initial evaluation\nCould not verify\n\ncould not process\n\nCould not proces"
1280 E1 role=alert count on page before opening tray record => 12
1280 E2 source-modal open => true
1280 E2 role=alert inside record-modal => 0
1280 E2 highlight-missing testid count => 0
1280 E2 role=alert on page after opening tray record => 12
1280 E2 record-modal text (first 220) => "=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\""
1280 E3 control bad-offset span: role=alert inside modal => 1
1280 E3 control bad-offset testid => 1
1280 F1 during run => [{"t_ms": 0, "analyze_buttons": 0, "stage": "Starting…"}, {"t_ms": 300, "analyze_buttons": 0, "stage": "Checking summaries 0 of 9"}, {"t_ms": 700, "analyze_buttons": 0, "stage": "Checking summaries 0 of 9"}]
375 A1 review-counts text => "9 entries · 1 needs review · 8 verified"
375 A1 toolbar h2 => "Timeline"
375 A2 rows total/needs_review/verified => [9, 1, 8]
375 A2 header entries/needs/verified => [9, 1, 8]
375 A2 header reconciles with rows => true
375 A2 review-status chip texts => ["Not reviewed yet"]
375 A2 state chip texts => ["Needs review", "Verified"]
375 A3 dates-to-confirm text => "Dates to confirm\n\nNone. Every record has a readable date."
375 A3 tray heading => "Could not verify (0)"
375 A4 first needs_review row top (px, page coords) => 563.5
375 A4 first focusable in #view-review => "<select data-testid=\"sort\"><option value=\"review\" selected=\"\">Needs review first | row state=null"
375 A4 records list is collapsed <details> => {"present": true, "open": false, "summary": "Records (9)"}
375 B1 why-title => "Why? Hill Country Pain Management, new patient, 2026-05-18"
375 B1 why-ladder text => "State\nverified\nBackend\nfixture\nDrafted by\nclaude-sonnet-5-5 · extract_v1\nAI draft\nSummary: New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered. Excerpt: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.\nChecks run by code\nexcerpt verbatim: passed\nexcerpt whole sentence: passed\nqualifier carried: passed\ndate provider from header: passed\nsummary tokens not in excerpt: none\nhighlight found: passed\nSecond check by another model\nsupported · claude-haiku-5-5 · judge_faithfulness_v1"
375 B1 why-text => "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
375 B1 why-modal full text => "Why? Hill Country Pain Management, new patient, 2026-05-18\nClose\n\nQuote found word for word, every number in the summary is in the quote, and the second check agreed.\n\nState\nverified\nBackend\nfixture\nDrafted by\nclaude-sonnet-5-5 · extract_v1\nAI draft\nSummary: New onset pain radiating to right arm with numbness in fingers; pain 7/10; MRI ordered. Excerpt: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.\nChecks run by code\nexcerpt verbatim: passed\nexcerpt whole sentence: passed\nqualifier carried: passed\ndate provider from header: passed\nsummary tokens not in excerpt: none\nhighlight found: passed\nSecond check by another model\nsupported · claude-haiku-5-5 · judge_faithfulness_v1\nModel calls (2)"
375 C1 entry-8 modal h3 count => 0
375 C1 entry-8 modal title => "Record 8: Austin Imaging, cervical MRI"
375 C1 entry-8 role=alert inside modal => 0
375 D1 synthetic banner box => {"top": 0, "bottom": 64}
375 D1 banner position => "sticky"
375 D1 keyboard tab labels (12 Tabs from results-page focus) => ["btn-accept:Accept", "btn-edit:Edit", "btn-dismiss:Dismiss", "entry-9:2026-06-12Hill Cou", "entry-why:Why?", "btn-source:Open record", "btn-accept:Accept", "btn-edit:Edit", "btn-dismiss:Dismiss", "flag-f_gap_r6_r7:Gap of 73 daysVeri", "btn-source:Open records 6 and", "btn-accept:Accept"]
375 D1 focused elements overlapped by sticky banner => []
375 D2 horizontal scroll => false
375 console/page errors => []
375 E1 tray text (first 260) => "Could not verify (1)\n\nThese records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself.\n\nRecord 4: Capital PT, initial evaluation\nCould not verify\n\ncould not process\n\nCould not proces"
375 E1 role=alert count on page before opening tray record => 12
375 E2 source-modal open => true
375 E2 role=alert inside record-modal => 0
375 E2 highlight-missing testid count => 0
375 E2 role=alert on page after opening tray record => 12
375 E2 record-modal text (first 220) => "=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\""
375 E3 control bad-offset span: role=alert inside modal => 1
375 E3 control bad-offset testid => 1
375 F1 during run => [{"t_ms": 0, "analyze_buttons": 0, "stage": "Starting…"}, {"t_ms": 300, "analyze_buttons": 0, "stage": "Checking summaries 0 of 9"}, {"t_ms": 700, "analyze_buttons": 0, "stage": "Checking summaries 0 of 9"}]
G0 empty-submit alert => "There is no text to read. Paste records or choose a .txt file."
G1 oversize alert => "That is 600,017 characters; the limit is 60,000. Nothing was sent."
G1 textarea length kept => 600017
WROTE artifacts/review-evidence/T-042-r2-ux-designer-check.out.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:59:44.822Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-kbd.py",
 "content": "\"\"\"T-042 round 2 follow-up checks (ux-designer-reviewer): clean keyboard path, visible alerts, case_01 counts.\nServed: python3 -m http.server 7867 --directory app/frontend (?api=mock). Run from project root:\n.venv/bin/python artifacts/review-evidence/T-042-r2-ux-designer-kbd.py\n\"\"\"\nimport re, json\nfrom playwright.sync_api import sync_playwright\n\nBASE = \"http://localhost:7867/index.html?api=mock\"\nOUT = \"artifacts/review-evidence/T-042-r2-\"\nLABEL = \"\"\"()=>{const a=document.activeElement;if(!a||a===document.body)return 'BODY';\n  const r=a.closest('[data-state]');return (a.dataset.testid||a.tagName)+(r&&r.dataset.testid===a.dataset.testid?'[row]':'')+':'+(a.textContent||'').trim().slice(0,22)}\"\"\"\n\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    # 1. Keyboard-only path from page top to the first needs_review row (1280x900)\n    ctx = b.new_context(viewport={\"width\": 1280, \"height\": 900}); pg = ctx.new_page(); pg.goto(BASE)\n    pg.get_by_test_id(\"btn-sample\").focus(); pg.keyboard.press(\"Enter\"); pg.get_by_test_id(\"record-count\").wait_for()\n    pg.get_by_test_id(\"btn-analyze\").focus(); pg.keyboard.press(\"Enter\")\n    pg.get_by_test_id(\"timeline\").wait_for(timeout=20000); pg.wait_for_timeout(300)\n    pg.evaluate(\"()=>{document.activeElement&&document.activeElement.blur();window.scrollTo(0,0)}\")\n    path = []\n    target_hit = None\n    for i in range(1, 41):\n        pg.keyboard.press(\"Tab\")\n        lab = pg.evaluate(LABEL); path.append(lab)\n        if pg.evaluate(\"()=>{const a=document.activeElement;return !!a.closest('[data-testid=queue] [data-state=needs_review]')}\"):\n            target_hit = i; break\n    print(\"KBD tabs to first needs_review focus:\", target_hit)\n    print(\"KBD path:\", json.dumps(path, ensure_ascii=False))\n    pg.screenshot(path=OUT + \"1280-08-kbd-first-needs-review.png\")\n    ctx.close()\n\n    # 2. Visible role=alert count on the results page, before and after opening a tray record (fail=4)\n    for W, H, tag in ((1280, 900, \"1280\"), (375, 812, \"375\")):\n        ctx = b.new_context(viewport={\"width\": W, \"height\": H}); pg = ctx.new_page(); pg.goto(BASE + \"&fail=4\")\n        pg.get_by_test_id(\"btn-sample\").click(); pg.get_by_test_id(\"record-count\").wait_for()\n        pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for(timeout=20000); pg.wait_for_timeout(300)\n        vis = lambda: pg.evaluate(\"()=>[...document.querySelectorAll('[role=alert]')].filter(e=>e.offsetParent!==null||getComputedStyle(e).position==='fixed').map(e=>(e.dataset.testid||'')+'|'+e.textContent.trim().slice(0,60))\")\n        before = vis()\n        pg.get_by_test_id(\"rejected-tray\").get_by_role(\"button\", name=re.compile(\"Open record\")).first.click(); pg.wait_for_timeout(300)\n        after = pg.evaluate(\"()=>[...document.querySelectorAll('[role=alert]')].filter(e=>e.offsetParent!==null).map(e=>(e.dataset.testid||'')+'|'+e.textContent.trim().slice(0,60))\")\n        print(tag, \"VISIBLE role=alert before tray open:\", json.dumps(before, ensure_ascii=False))\n        print(tag, \"VISIBLE role=alert after tray open:\", json.dumps(after, ensure_ascii=False))\n        print(tag, \"source-modal text (first 160):\", json.dumps(pg.locator(\"#source-body\").inner_text()[:160], ensure_ascii=False))\n        if tag == \"1280\":\n            pg.screenshot(path=OUT + \"1280-09-tray-open-record-r2.png\")\n        ctx.close()\n\n    # 3. case_01 paste: does the header count (entries only) still agree with rows and the dates-to-confirm group?\n    ctx = b.new_context(viewport={\"width\": 1280, \"height\": 900}); pg = ctx.new_page(); pg.goto(BASE)\n    pg.get_by_test_id(\"input-text\").fill(open(\"evals/golden/case_01_date_formats.txt\").read())\n    pg.get_by_test_id(\"btn-analyze\").click(); pg.get_by_test_id(\"timeline\").wait_for(timeout=20000); pg.wait_for_timeout(300)\n    print(\"CASE01 review-counts:\", pg.get_by_test_id(\"review-counts\").inner_text())\n    rows = pg.get_by_test_id(\"queue\").locator(\"[data-state]\").all()\n    print(\"CASE01 queue rows:\", len(rows), [r.get_attribute(\"data-state\") for r in rows])\n    print(\"CASE01 dates-to-confirm:\", json.dumps(pg.get_by_test_id(\"dates-to-confirm\").inner_text()[:400], ensure_ascii=False))\n    print(\"CASE01 undated rows (data-state):\", pg.locator(\"[data-testid=dates-to-confirm] [data-state]\").evaluate_all(\"els=>els.map(e=>e.dataset.state)\"))\n    pg.get_by_test_id(\"dates-to-confirm\").scroll_into_view_if_needed(); pg.screenshot(path=OUT + \"1280-10-case01-counts.png\")\n    ctx.close()\n    b.close()\n"
}
````

### User / tool · 2026-11-02T01:59:44.924Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-ux-designer-kbd.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:59:46.448Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-042-r2-ux-designer-kbd.py 2>&1 | tail -40",
 "description": "Run keyboard path, visible alert, and case_01 count checks",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T01:59:58.866Z

**tool result**
````
KBD tabs to first needs_review focus: 4
KBD path: ["SUMMARY:Records (9)", "start-over:Start over", "sort:Needs review firstBy d", "entry-3[row]:2026-01-16Dr. Alvarez,"]
1280 VISIBLE role=alert before tray open: []
1280 VISIBLE role=alert after tray open: []
1280 source-modal text (first 160): "=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge"
375 VISIBLE role=alert before tray open: []
375 VISIBLE role=alert after tray open: []
375 source-modal text (first 160): "=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge"
CASE01 review-counts: 2 entries · 0 needs review · 2 verified
CASE01 queue rows: 2 ['verified', 'verified']
CASE01 dates-to-confirm: "Dates to confirm\n\nThese records are left off the timeline and the gap check until you pick the right date. The tool never guesses.\n\nundated\nPemberwick Physical Therapy, visit 1\nNeeds review\nNot reviewed yet\n\nAI summary (mock): Gait mildly antalgic.AI-drafted\n\nGait mildly antalgic. Pain 4/10.\n\nCheck: the date can be read two ways\n\nNo readable date in this record header; it stays off the timeline.\n\n"
CASE01 undated rows (data-state): ['needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:00:13.673Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-1280-10-case01-counts.png"
}
````

### User / tool · 2026-11-02T02:00:13.682Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:00:13.866Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-042-r2-1280-01-results-header.png"
}
````

### User / tool · 2026-11-02T02:00:13.874Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:00:31.806Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | grep \"^T-042-r2\" ; echo ---; ls -la .claude/agent-memory/ux-designer-reviewer/ 2>&1 | head -20; echo ---; grep -n \"validate\\|def main\\|argv\" tools/board.py | head -20",
 "description": "List round-2 evidence files, memory dir, and board validate usage"
}
````

### User / tool · 2026-11-02T02:00:31.910Z

**tool result**
````
T-042-r2-1280-01-results-header.png
T-042-r2-1280-02-results-viewport.png
T-042-r2-1280-03-why7.png
T-042-r2-1280-04-source8.png
T-042-r2-1280-05-tray-open-record.png
T-042-r2-1280-06-control-bad-span.png
T-042-r2-1280-07-processing.png
T-042-r2-1280-08-kbd-first-needs-review.png
T-042-r2-1280-09-tray-open-record-r2.png
T-042-r2-1280-10-case01-counts.png
T-042-r2-375-01-results-header.png
T-042-r2-375-02-results-viewport.png
T-042-r2-375-03-why7.png
T-042-r2-375-04-source8.png
T-042-r2-375-05-tray-open-record.png
T-042-r2-375-06-control-bad-span.png
T-042-r2-ux-designer-check.out.json
T-042-r2-ux-designer-kbd.py
T-042-r2-ux-designer-walk.py
---
total 0
drwxr-xr-x@  2 arsis  staff   64 Nov  1 19:03 .
drwxr-xr-x@ 16 arsis  staff  512 Nov  1 19:47 ..
---
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
1145:def main(argv=None) -> int:
1146:    args = build_parser().parse_args(argv)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:00:56.796Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-042-ux-designer-r2.md",
 "content": "# T-042 round 2 UX review (ux-designer-reviewer)\n\nVerdict: changes. No blockers. The two round-1 items are handled as follows. The false red alert on tray records is fixed. The count line reconciles on the sample case, but it still contradicts the screen on case_01 (new major, same finding class). Four other round-1 minors were fixed and three are partly open, carried as minors.\n\nScope: commit 348cd0b (app/frontend: input.js, source.js, styles.css, timeline.js), served with `.venv/bin/python -m http.server 7867 --directory app/frontend`, `?api=mock`, sample case plus `evals/golden/case_01_date_formats.txt`, 1280x900 and 375x812. Real backend not exercised.\n\nRound-1 status:\n- Major, counts do not reconcile: sample case FIXED; case_01 NOT FIXED, reopened as the new major below.\n- Minor, false red alert from tray: FIXED.\n- Minor, record list pushes timeline down / first focusable is the sort menu: PARTLY (list collapsed; sort select still first).\n- Minor, two state chips ambiguous: FIXED (\"Not reviewed yet\" chip).\n- Minor, Analyze clickable during run: FIXED (hidden while running).\n- Minor, sticky banner covers focus: FIXED at 375 (64 px banner, 90 px scroll margin, no overlapped focus stop).\n- Minor, Why? developer vocabulary: PARTLY (title and labels renamed; prompt versions and \"tokens\" still in the main list).\n- Nit, duplicated modal heading: FIXED.\n\nKey outputs (full output: artifacts/review-evidence/T-042-r2-ux-designer-check.out.json and the console of the kbd script):\n\n```\n1280 A1 review-counts text => \"9 entries · 1 needs review · 8 verified\"\n1280 A2 rows total/needs_review/verified => [9, 1, 8]\n1280 A2 header reconciles with rows => true\n1280 E2 role=alert inside record-modal => 0\n1280 E2 role=alert on page after opening tray record => 12   (hidden nodes; see next line)\nVISIBLE role=alert before tray open: []   VISIBLE role=alert after tray open: []   (1280 and 375)\n1280 E3 control bad-offset span: role=alert inside modal => 1   (real failure still alerts)\nCASE01 review-counts: 2 entries · 0 needs review · 2 verified\nCASE01 undated rows (data-state): ['needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review', 'needs_review']\nKBD path: [\"SUMMARY:Records (9)\", \"start-over:Start over\", \"sort:Needs review firstBy d\", \"entry-3[row]:2026-01-16Dr. Alvarez,\"]\n1280 A4 first needs_review row top => 444.5   (round 1: 624)\n375  A4 first needs_review row top => 563.5   (round 1: 955)\n1280 F1 during run => analyze_buttons 0 at t=0, 300, 700 ms; stage \"Checking summaries 0 of 9\"\n375 D1 banner box => bottom 64; focused elements overlapped by sticky banner => []\n```\n\nFindings are below. Screenshots: artifacts/review-evidence/T-042-r2-{1280,375}-*.png.\n\n```json\n{\"card\": \"T-042\", \"persona\": \"ux-designer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 348cd0b (app/frontend/input.js, source.js, styles.css, timeline.js); app served on http://localhost:7867/index.html?api=mock (mock API, not the real backend on :7860); sample case (evals/golden/sample.txt) and evals/golden/case_01_date_formats.txt; 1280x900 and 375x812\",\n \"exercised\": [\n  \"Read personas/ux-designer.md, reviews/T-042-ux-designer.md (round 1), artifacts/review-evidence/T-042-ux-designer-walk.py (hardcodes :7865 and overwrites T-042-* evidence, so not re-run; replaced by T-042-r2-ux-designer-walk.py and T-042-r2-ux-designer-kbd.py)\",\n  \"git show 348cd0b --stat (4 files, 23 insertions, 15 deletions) and git show 348cd0b -- app/frontend/ diff\",\n  \"python3 tools/board.py show T-042: status in_review, commits include 348cd0b\",\n  \"curl http://localhost:7867/index.html?api=mock -> 200; python3 -m http.server 7867 --directory app/frontend\",\n  \"Playwright 1280x900 and 375x812, sample case: review-counts text vs queue rows (data-state), review-status and state chip texts, dates-to-confirm and tray text, first focusable in #view-review, records details collapsed state, first needs_review row y-position, horizontal scroll, console errors\",\n  \"Playwright: Why? on entry 7 (title, ladder text, modal text), entry 8 Open record (h3 count, role=alert count), 12 Tab stops with sticky-banner overlap check\",\n  \"Playwright: ?fail=4 tray 'Open record 4' (modal open, role=alert inside and on page, visible role=alert before/after), control span with start=-5 to confirm the real alert still fires\",\n  \"Playwright: Analyze button count and stage text at 0, 300, 700 ms during a run\",\n  \"Playwright: keyboard-only Tab path from page top to first needs_review row (1280)\",\n  \"Playwright: case_01 paste, review-counts, queue rows, dates-to-confirm rows and states\",\n  \"Playwright: empty submit and 600 KB submit (input-side regression; alert text and textarea length 600017 kept)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"design_quality\": 3, \"originality\": 3, \"craft\": 4, \"functionality\": 4},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Count line reconciles on the sample case but not on case_01: header says 0 need review while six Needs review items sit below it\",\n   \"evidence\": \"CASE01 review-counts: '2 entries · 0 needs review · 2 verified'; CASE01 undated rows (data-state): ['needs_review' x6]; dates-to-confirm chips read 'Needs review' / 'Not reviewed yet' (artifacts/review-evidence/T-042-r2-1280-10-case01-counts.png). Sample case is fine: '9 entries · 1 needs review · 8 verified' vs rows [9, 1, 8] (T-042-r2-1280-01-results-header.png).\",\n   \"why_it_matters\": \"The round-1 major was a count that cannot be reconciled with what is on screen. The round-2 fix counts timeline entries only, which is correct for the sample, but the only status line still says zero need review on a screen that shows six items marked Needs review. Checklist 6 and 'how many remain' are misstated for the paste path that produces Dates to confirm. Visibility of system status; calibrated trust.\",\n   \"fix\": \"Include the Dates to confirm items in the same line, e.g. '2 entries · 0 need review · 6 dates to confirm', or add 'Dates to confirm: 6 need review' to the same toolbar. Keep the sample case output unchanged.\",\n   \"acceptance_test\": \"E2E with case_01 paste: needs-review number in review-counts (plus any dates-to-confirm count) equals the number of [data-state=needs_review] rows on screen across timeline and Dates to confirm (6 in this case). E2E with sample: 1 equals the one needs_review row.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The Order select is still the first focusable control in the review region (round-1 minor, partly fixed)\",\n   \"evidence\": \"A4 first focusable in #view-review => '<select data-testid=\\\"sort\\\">...'; KBD path from page top: ['SUMMARY:Records (9)', 'start-over:Start over', 'sort:Needs review firstBy d', 'entry-3[row]:2026-01-16Dr. Alvarez,'] (4 Tabs). First needs_review row top: 444.5 px at 1280 (round 1: 624), 563.5 px at 375 (round 1: 955). Collapsing the records list is confirmed: details.reclist-wrap open=false.\",\n   \"why_it_matters\": \"The collapse fixes the scroll position. Keyboard users still reach a sort control before the first item that needs them, which is checklist 19's first-focusable rule.\",\n   \"fix\": \"Move the Order select after the queue, or make the first needs_review row the first tab stop inside #view-review.\",\n   \"acceptance_test\": \"Sample run at 1280x900: first focusable element inside #view-review has data-state=needs_review; first needs_review row top < 450 px (already 444.5).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Why? panel still puts prompt versions and internal wording in the main list (round-1 minor, partly fixed)\",\n   \"evidence\": \"1280 B1 why-ladder text => '...Drafted by / claude-sonnet-5-5 · extract_v1 ... Checks run by code / ... summary tokens not in excerpt: none ... Second check by another model / supported · claude-haiku-5-5 · judge_faithfulness_v1'. Title now 'Why? Hill Country Pain Management, new patient, 2026-05-18' (fixed); 'Model calls (2)' is collapsed (fine).\",\n   \"why_it_matters\": \"The renamed labels help. The main view still carries prompt identifiers and the word 'tokens', which mean nothing to a paralegal and belong in Model calls. Not a spec violation; a should-fix.\",\n   \"fix\": \"Move model and prompt_version lines under the collapsed Model calls details. Reword 'summary tokens not in excerpt' in plain words that match what the check does.\",\n   \"acceptance_test\": \"why-ladder inner text (outside details) contains none of 'extract_v1', 'judge_faithfulness_v1', 'tokens'.\"}\n ],\n \"whats_right\": [\n  \"Tray 'Open record 4' opens the whole record with no role=alert (E2: 0 inside record-modal; 0 visible alerts before or after), and a real bad span still alerts (E3: 1), so the fix did not suppress genuine failures.\",\n  \"Count line matches the rows on the sample case (9 entries, 1 needs review, 8 verified) and the Needs review rows carry a visible 'Check:' reason.\",\n  \"Analyze is removed while a run is in progress and the stage text shows from the first poll ('Starting…', then 'Checking summaries 0 of 9'); the 375 sticky banner no longer covers any of 12 Tab stops.\"],\n \"questions_for_chris\": [\"Should the review header's needs-review number include the Dates to confirm items (6 on case_01), or should that group keep its own labelled count? The fix for the major depends on this product call.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T02:00:56.939Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-042-ux-designer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:03.481Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-042-ux-designer-r2.md",
 "old_string": "Verdict: changes. No blockers. The two round-1 items are handled as follows. The false red alert on tray records is fixed. The count line reconciles on the sample case, but it still contradicts the screen on case_01 (new major, same finding class). Four other round-1 minors were fixed and three are partly open, carried as minors.",
 "new_string": "Verdict: changes. No blockers. The round-1 major is only partly fixed: the count line reconciles on the sample case but still contradicts the screen on case_01, so it is re-filed as a major below. Of the round-1 minors, the false red alert on tray records is fixed, as are the chip labels, Analyze-during-run, and the sticky-banner overlap; the record-list focus order and the Why? vocabulary are partly fixed and carried as minors. The round-1 nit (duplicate heading) is fixed."
}
````

### User / tool · 2026-11-02T02:01:03.628Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-042-ux-designer-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:03.970Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-042-ux-designer-r2.md 2>&1 | head -20; echo \"exit=$?\"",
 "description": "Validate the round-2 review file with the board validator"
}
````

### User / tool · 2026-11-02T02:01:04.096Z

**tool result**
````
ok (1 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:09.655Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_recheck_all_paths.md",
 "content": "---\nname: recheck-all-data-paths\ndescription: When re-checking a fix for a count/status line, reconcile it on every data path (sample case AND paste variants), not just the sample case\nmetadata:\n  type: feedback\n---\n\nWhen verifying a round-N fix for a count or status line, reconcile the number against visible rows on every input path that renders it, not only the sample case. T-042 r2 (2026-11-01): the header count reconciled on the sample case (9/1/8) but read \"0 needs review\" on the case_01 paste while six \"Needs review\" items sat in the Dates to confirm group below it.\n\n**Why:** The sample case is the path the implementer tests. Paste variants render extra groups (undated items, tray, flags) that the count can silently skip.\n\n**How to apply:** For any count line, run the sample plus at least one golden case with undated or tray items (`evals/golden/case_01_date_formats.txt` has undated items). Compare the header number to `[data-state]` rows across every section on screen.\n\nAlso: `app/frontend/` review walk scripts hardcode their port and overwrite the round-1 `T-042-*` evidence. Write a new round-N script with its own output prefix instead of re-running the old one.\n"
}
````

### User / tool · 2026-11-02T02:01:09.759Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/feedback_recheck_all_paths.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:10.347Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/MEMORY.md",
 "content": "- [Recheck all data paths](feedback_recheck_all_paths.md) — reconcile count lines on sample AND paste variants; new round script per prefix, don't rerun old hardcoded-port walks\n"
}
````

### User / tool · 2026-11-02T02:01:10.450Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/ux-designer-reviewer/MEMORY.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:11.744Z

**tool call — Bash**
````
{
 "command": "for pid in $(lsof -t -nP -iTCP:7867 -sTCP:LISTEN 2>/dev/null); do kill $pid; done; sleep 1; (lsof -nP -iTCP:7867 -sTCP:LISTEN 2>&1 || echo \"7867 closed\")",
 "description": "Stop the port 7867 static server started for this review"
}
````

### User / tool · 2026-11-02T02:01:12.973Z

**tool result**
````
7867 closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:01:13.951Z

T-042 r2 verdict: changes. The tray false alert is fixed and the sample-case counts reconcile, but on the case_01 paste the header says "0 needs review" beside six "Needs review" items (major). Review: reviews/T-042-ux-designer-r2.md (validates ok).
