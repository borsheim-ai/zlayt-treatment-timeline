# T-185 product note, round 2: product-manager-reviewer (Dana Okafor lens)

**Verdict: changes** (0 blockers, 1 major, 3 minors, 2 nits).

Graded at `git show HEAD:submission/product-note.md`. HEAD is 2e58e18, and the note is byte-identical to ddfbf6d (`git diff ddfbf6d HEAD --stat -- submission/` is empty). The working tree is not graded.

**Round-1 findings: 9 of 10 closed.**
- **Both blockers are fixed.**
  - Row 5 now reads "Not met on the screen I rejected".
  - The first "What testing found" bullet tells the D-068 story plainly.
  - T-181 and T-179 are marked "In progress, not yet in the app".
  - The failure table says D-066 "will need ... (in progress)".
- **Unit count is fixed.** 5,795 at 33e88c6 is in the HEAD tree (`artifacts/unit-count-33e88c6.txt`).
- **Stretch is fixed.** The note names all three items, gives the D-042 reason (verified verbatim against the decision) and states the cost.
- **Every cited path exists in HEAD** (script output below).
- **All three minors and the nit are fixed:** the $10,906 claim is dropped, the LLM_SPLIT fallback is listed, the metrics name their sources, and "Score 5" is gone.

**Still open (major).** Library recall in row 2 is partly fixed. Entries 0.775 and amounts 0.681 match the committed `evals/reports/library-latest.md` (93/120, 47/69, 34/42). But the row adds "(0.580 on a later run; report being regenerated)". 0.580 is in no committed report, and no card regenerates the report.

**Placeholders (brief item 2): acceptable, not a defect.**
- D-031 and D-042 are Chris's own calls (decision log: "Chris, inbox 02:05Z" and "Chris, chat"), so his motive is a fact only he has. The note already states what was decided and what it cost, so it reads complete without him. T-191 tracks the placeholder.
- One flaw: NEEDS_CHRIS row 8 is P1 and says "(card pending)", while T-191 is P2.

Page count: 1. Rendered from HEAD with the committed `submission/print.css` (8.7pt), output in `artifacts/review-evidence/T-185-pm/r2/product-note.pdf`.

```json
{"card": "T-185", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/product-note.md at HEAD 2e58e18 (identical to fix commit ddfbf6d); cited evidence at HEAD: evals/reports/library-latest.md, evals/reports/20261102T164038Z.md, evals/reports/m3-sensors.md, artifacts/unit-count-33e88c6.txt, submission/prompt-log/reviews/{GATE-M3-paralegal,GATE-M3-product-manager,T-140-claims-adjuster}.md, memory/ORCHESTRATOR_DECISIONS.md, submission/NEEDS_CHRIS.md; app code at HEAD (app/backend/api.py, app/frontend/guided/); running app http://localhost:7860",
 "exercised": [
  "Read personas/product-manager.md, my round-1 review reviews/T-185-product-manager.md, board.py show T-185/T-191/T-192, board.py list (T-177, T-179, T-181 in_progress; no library-regeneration card)",
  "git log --oneline -8; git show --stat ddfbf6d; git diff ddfbf6d HEAD --stat -- submission/ -> empty (note unchanged since the fix commit)",
  "git show HEAD:submission/product-note.md read end to end twice; rendered HEAD copy with committed print.css via pandoc + headless Chrome -> artifacts/review-evidence/T-185-pm/r2/product-note.pdf = 1 page",
  "git show HEAD:evals/reports/library-latest.md -> python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py artifacts/review-evidence/T-185-pm/library-HEAD.md -> '15 packets', 'entries: 93/120 = 0.775', 'amounts: 47/69 = 0.681', 'must flags: 34/42 = 0.810'",
  "git grep -n '0\\.580' HEAD -- evals/reports/ -> no match; only hits are the note itself, writer memory, the prompt-log copy of my r1 review and transcripts",
  "python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py <repo> submission/product-note.md -> 11 of 11 backticked paths OK in HEAD tree",
  "git ls-tree HEAD artifacts/unit-count-33e88c6.txt -> blob b7958bd; file tail '5795 passed, 8 skipped in 356.75s'; git status --short on it -> 'D ' staged and '??' (staged deletion in the shared index)",
  "git show HEAD:evals/reports/m3-sensors.md:7-8 -> E2E '412 passed' at d7ea327 (matches note)",
  "git show HEAD:evals/reports/20261102T164038Z.md -> models generator claude-sonnet-5-5 / judge claude-haiku-5-5; 'Clean held-out J3 controls: 5 of 17' (:115); J3 20/20, J4 12/12",
  ".venv/bin/python -m evals.run --check-fresh -> exit=0; git log 312efe6..HEAD -- app/llm/prompts app/llm/lexicon.yaml -> empty",
  "git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md:10 -> '$16,147.00 ... The records state $8,123.50'; GATE-M3-product-manager.md:46 -> 'Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click'",
  "memory/ORCHESTRATOR_DECISIONS.md at HEAD: D-031 'Scope reinstated (Chris, inbox 02:05Z)', D-042 'Second scope reinstatement (Chris, chat) ... every remaining cut that needs neither a paid third-party integration nor auth/multi-user'; D-059 first commit 07c7558, git merge-base --is-ancestor a74b727 07c7558 -> true ('before the billing redesign' holds)",
  "git show HEAD:submission/NEEDS_CHRIS.md rows 8-9 vs board.py show T-191 (P2) / T-192 (P2)",
  "git show HEAD:app/backend/api.py:699-712 and HEAD:app/frontend/guided/{review,step2}.js; curl http://localhost:7860/ (old UI, older server), /classic -> 404, /api/health -> demo_mode true"
 ],
 "verdict": "changes",
 "scores": {"accuracy": 4, "no_invented_chris_facts": 5, "required_contents": 5, "honesty_of_misses": 5, "voice": 4, "length": 5},
 "findings": [
  {"severity": "major", "title": "Row 2 cites a library amount recall (0.580) that no committed report contains, plus a regeneration that no card owns",
   "evidence": "HEAD:submission/product-note.md:16 '**Library: entries 0.775, amounts 0.681 [L]** (0.580 on a later run; report being regenerated)'. lib_sums_r2.py on HEAD:evals/reports/library-latest.md -> 'amounts: 47/69 = 0.681'. git grep -n '0\\.580' HEAD -- evals/reports/ -> no match. The 0.580 came from my untracked r1 evidence (artifacts/review-evidence/GATE-M3-pm/library-d0b04bc.md; git ls-files --error-unmatch -> 'did not match any file(s) known to git'). board.py list | grep -i library -> only done cards (T-052, T-053, T-077, T-079, T-129); no open card regenerates library-latest.md. The orchestrator's T-185 note at 21:27:58Z: 'drop the 0.580 mention unless a committed report shows it.'",
   "why_it_matters": "The brief and AC 1 require every number to trace to a committed report. A panelist who opens [L] finds 0.681 and no trace of 0.580. 'Report being regenerated' promises work that nobody is doing. The note's credibility rests on its numbers opening to their source.",
   "fix": "Delete '(0.580 on a later run; report being regenerated)'. Or have qa regenerate evals/reports/library-latest.md at the submission commit under a card, commit it, and cite that single report's numbers.",
   "acceptance_test": "Every library number in product-note.md row 2 equals a value computed from git show HEAD:evals/reports/library-latest.md, and the note contains no '0.580' unless that report shows it."},
  {"severity": "minor", "title": "'(same review)' points at the wrong source: the nearest citation is the T-140 adjuster review, but the 5 of 5 / 16 cases figure is from GATE-M3-product-manager",
   "evidence": "HEAD:submission/product-note.md:25 cites 'submission/prompt-log/reviews/T-140-claims-adjuster.md'; :26 'One click accepted a disputed summary, 5 of 5 times in 16 cases (same review)'. The figure is at GATE-M3-product-manager.md:46 'Across 16 cases, 5 of 5 judge-disputed entries were accepted with a single click'. git show HEAD:submission/prompt-log/reviews/T-140-claims-adjuster.md | grep -E '5 of 5|16 cases' -> no match.",
   "why_it_matters": "A panelist following 'same review' opens the billing review and does not find the number. It is a small break in traceability on the note's key honesty bullet.",
   "fix": "Replace '(same review)' with '(`submission/prompt-log/reviews/GATE-M3-product-manager.md`)', or move the bullet next to the GATE-M3 citation.",
   "acceptance_test": "The source named next to '5 of 5 times in 16 cases' contains that figure (grep)."},
  {"severity": "minor", "title": "'Misses cluster in ledgers, EOBs, scans, Spanish' leaves out two of the four worst library packets",
   "evidence": "HEAD:evals/reports/library-latest.md entries column: lib11 priors_and_ledger 4/9, lib15 conclusory_letter_mist 4/8, lib13 cloned_notes_cross_provider 5/9, lib09 spanish 4/7, lib10 eob 6/9, lib14 scans 6/8. The named categories (lib09, lib10, lib11, lib14) account for 13 of the 27 missed entries. The unnamed cloned-notes (lib13) and conclusory-letter (lib15) packets account for 8.",
   "why_it_matters": "Error analysis is the point of the library run. Naming only the input-format causes (ledger, EOB, scan, language) hides the content-type misses (cloned notes, conclusory letters) that a paralegal would hit on ordinary records.",
   "fix": "'Largest misses: ledgers, conclusory letters, cloned notes, Spanish, EOBs' (or list the packets by recall), still followed by 'real misses vs stale expected files not yet separated'.",
   "acceptance_test": "Each packet with entry recall below 0.6 in library-latest.md falls in a category the row names."},
  {"severity": "minor", "title": "NEEDS_CHRIS row 8 (the stretch reason) is P1 and says '(card pending)', while its card T-191 exists at P2",
   "evidence": "HEAD:submission/NEEDS_CHRIS.md:22 '| 8 | P1 | (card pending) | Product note, Cut paragraph: why you reinstated cuts ...'. board.py show T-191 -> 'priority: \"P2\"', title 'Chris: stretch-item reasons in the product note (NEEDS_CHRIS #8)'.",
   "why_it_matters": "Chris works from the needs_chris column on his phone. If the row and the card disagree on priority, he may under-prioritize the one placeholder that sits in the note's graded 'cut scope on purpose' paragraph. A stale '(card pending)' also shows the parity check was not re-run.",
   "fix": "Set row 8's card column to T-191 and make the priorities agree (P1 on both, since the placeholder is visible in the one-page note).",
   "acceptance_test": "For every NEEDS_CHRIS row, the card column names an existing card with the same priority (board.py show)."},
  {"severity": "nit", "title": "Outside the verdict per brief item 4, but a release risk: at HEAD the public/demo front door is the empty T-181 scaffold, so 'not yet in the app' is already untrue and 'What I built' is not reachable in demo mode",
   "evidence": "HEAD:app/backend/api.py:700 'in demo or public mode it sends the visitor to the guided UI at /'; HEAD:app/frontend/guided/review.js 'Empty on purpose (T-181 scaffold)'; step2.js 'PLACEHOLDER from the T-181 scaffold: it only draws the empty frame'. product-note.md:7 'Each timeline entry shows the AI's summary beside the verbatim quote; she accepts, edits or dismisses it ... In progress, not yet in the app: a guided four-step screen'.",
   "why_it_matters": "If the submission is tagged before T-181 is done, the panel's prototype link shows empty steps. The note would then describe a review screen they cannot reach.",
   "fix": "Orchestrator: do not tag a submission commit while / serves the scaffold in demo mode. Refresh line 7 when T-181 lands, as already planned.",
   "acceptance_test": "At the submission commit, in demo mode, every action in 'What I built' can be done from /."},
  {"severity": "nit", "title": "The cited unit-count file is staged for deletion in the shared index",
   "evidence": "git status --short artifacts/unit-count-33e88c6.txt -> 'D ' plus '??'; git ls-files --error-unmatch -> not known; git ls-tree HEAD -> present (blob b7958bd).",
   "why_it_matters": "A path-limited commit that sweeps this path would remove the note's test-count evidence from git.",
   "fix": "Orchestrator: git restore --staged artifacts/unit-count-33e88c6.txt (non-destructive) before the next commit.",
   "acceptance_test": "git ls-files --error-unmatch artifacts/unit-count-33e88c6.txt succeeds."}
 ],
 "whats_right": [
  "Row 5 'Not met on the screen I rejected' and the first testing bullet turn the D-068 human verdict into the note's clearest AI-judgment lesson. Keep that order.",
  "Present tense is used only for what HEAD ships. T-181 and T-179 are labeled in progress in the build paragraph, the failure table and the M3 bullet.",
  "Stretch paragraph names all three items, gives the verifiable D-042 rule, states the cost and leaves only Chris's motive as a tracked placeholder."
 ],
 "questions_for_chris": []}
```
