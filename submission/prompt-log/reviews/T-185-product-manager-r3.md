# T-185 product note, round 3: product-manager-reviewer (Dana Okafor lens)

**Verdict: pass** (0 blockers, 0 majors, 1 minor carried from r2, 1 new nit).

**What I graded.** `git show HEAD:submission/product-note.md` at HEAD 6d6dc45, which is the fix commit. `git status --short submission/` is empty, so the working tree matches HEAD. The scope is narrow: the r2 major and any new defect in `git diff ddfbf6d 6d6dc45 -- submission/`.

**r2 major (library number not in the committed report): closed.**
- "(0.580 on a later run; report being regenerated)" is gone. Row 2 now reads "entries 0.775, amounts 0.681 [L] (93/120; 47/69)".
- I recomputed from `git show HEAD:evals/reports/library-latest.md` (source commit a74b727, which matches the note's "run at a74b727"). Results: 15 packets, entries 93/120 = 0.775, amounts 47/69 = 0.681, must flags 34/42 = 0.810.
- Every library number in the note (rows 2 and 3 and the bullet on line 24) matches one of those values. `0.580` appears 0 times in the note and 0 times in Part 2.

**r2 minors that the diff touched.**
- "(same review)" now points at GATE-M3-product-manager.md: fixed.
- "Largest misses" now names every packet with entry recall below 0.6 (lib11, lib15, lib13, lib09): fixed.
- NEEDS_CHRIS row 8 now names T-191, but it is still P1 while T-191 is P2: half fixed (minor, carried).

**New in the diff.** The pointer for the 5-of-5 figure is a bare filename, `GATE-M3-product-manager.md`, so the path check reports it as MISS. It says "cited above", and the full path is on line 24, so this is a nit.

**Render.** The rendered HEAD copy is 1 page (`artifacts/review-evidence/T-185-pm/r3/product-note.pdf`).

```json
{"card": "T-185", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/product-note.md and submission/NEEDS_CHRIS.md at HEAD 6d6dc45 (fix commit); diff ddfbf6d..6d6dc45 -- submission/; evals/reports/library-latest.md at HEAD",
 "exercised": [
  "Read reviews/T-185-product-manager-r2.md and my memory note feedback_submission_doc_patterns.md",
  "git log --oneline -10 -> HEAD 6d6dc45; git show --stat 6d6dc45; git diff ddfbf6d 6d6dc45 -- submission/ (read in full); git status --short submission/ -> empty",
  "git log --oneline -3 -- evals/reports/library-latest.md -> last change ce70bd2 (regenerated from clean a74b727); header 'Source commit: a74b727... (tree: clean)'",
  "python3 -I artifacts/review-evidence/T-185-pm/lib_sums_r2.py artifacts/review-evidence/T-185-pm/r3-library-HEAD.md -> '15 packets', 'entries: 93/120 = 0.775', 'amounts: 47/69 = 0.681', 'must flags: 34/42 = 0.810'",
  "grep -niE 'librar|\\[L\\]' on the HEAD note -> lines 11, 16, 17, 24; every number is one of 15 / 0.775 / 0.681 / 93/120 / 47/69 / 34 of 42 / 0.81; grep -c '0\\.580' -> 0 in note and Part 2",
  "Per-packet entry recall from library-latest.md: lib11 4/9, lib15 4/8, lib13 5/9, lib09 4/7 (all <0.6), each in the 'Largest misses' list",
  "python3 -I artifacts/review-evidence/T-185-pm/paths_in_head.py <repo> submission/product-note.md -> all OK except 'MISS GATE-M3-product-manager.md' (bare filename)",
  "board.py show T-191 -> priority P2, status needs_chris; HEAD NEEDS_CHRIS row 8 -> '| 8 | P1 | T-191 |'",
  "Rendered HEAD note with HEAD print.css via pandoc + headless Chrome -> artifacts/review-evidence/T-185-pm/r3/product-note.pdf = 1 page"
 ],
 "verdict": "pass",
 "scores": {"accuracy": 5, "no_invented_chris_facts": 5, "required_contents": 5, "honesty_of_misses": 5, "voice": 4, "length": 5},
 "findings": [
  {"severity": "minor", "title": "Carried from r2: NEEDS_CHRIS row 8 is P1, but its card T-191 is P2",
   "evidence": "HEAD:submission/NEEDS_CHRIS.md row 8 '| 8 | P1 | T-191 | Product note, Cut paragraph ...'; python3 tools/board.py show T-191 -> 'priority: \"P2\"'. The r3 diff changed only the card column ('(card pending)' -> 'T-191').",
   "why_it_matters": "Chris triages from the needs_chris column. When the row and the card disagree, the one placeholder in the graded cut paragraph may be under-prioritized.",
   "fix": "Writer: set row 8 to P2. Or ask the orchestrator to raise T-191 to P1. Either way, make the two agree.",
   "acceptance_test": "For every NEEDS_CHRIS row, the card column names an existing card with the same priority (board.py show)."},
  {"severity": "nit", "title": "New in r3: the source for the 5-of-5 figure is a bare filename, not a repo path",
   "evidence": "HEAD:submission/product-note.md:26 '5 of 5 times in 16 cases (`GATE-M3-product-manager.md`, cited above)'; paths_in_head.py -> 'MISS GATE-M3-product-manager.md'. The full path is on :24.",
   "why_it_matters": "Every other backticked path in the note opens in git as written. This one only resolves if the reader follows 'cited above'.",
   "fix": "Use `submission/prompt-log/reviews/GATE-M3-product-manager.md`, or drop the backticks and keep 'cited above'.",
   "acceptance_test": "paths_in_head.py on product-note.md reports no MISS."}
 ],
 "whats_right": [
  "Row 2 shows the fractions (93/120; 47/69) next to the ratios, so a panelist can check them against [L] in seconds.",
  "The 'Largest misses' list now covers content-type misses (conclusory letters, cloned notes) as well as input formats.",
  "The note is still 1 page, and every r2 honesty fix (row 5, D-068 bullet, in-progress labels) is unchanged."
 ],
 "questions_for_chris": []}
```
