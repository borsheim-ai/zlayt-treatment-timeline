# T-069 review: EDITED ITEMS lists edited-then-accepted entries, commit 59c7edb (claims-adjuster lens)

Reviewer: claims-adjuster-reviewer, model claude-haiku-5-5.

**Persona scope.** The request was to file this as persona paralegal-reviewer at `reviews/T-069-paralegal.md`. I did not write it under that name, because a review filed under another persona is a misattribution. This file is my claims-adjuster review of the edit audit trail (D-010) and the letter's freedom from edit markers. The paralegal review for T-069 is still outstanding and needs a paralegal-reviewer pass in a fresh context.

**Commit-level note (not a T-069 finding).** Commit 59c7edb also leaves 4 flag unit tests red (see `reviews/T-067-claims-adjuster.md`, major). T-069's own scope is green; the commit as a whole is not.

## Summary

The change does what the card says. An entry edited and then accepted now appears in EDITED ITEMS with its original and its new summary. An entry edited and then dismissed does not appear, and it is absent from the letter. The letter carries the new text with no edit marker, and the original survives only in internal notes (D-001, D-010).

One minor finding, which predates this commit: a paralegal edit can add a word the record does not say ("severe") and no code check covers it. The audit trail records it, so the trail itself works.

## Exercised

- `git show 59c7edb -- app/backend/export.py tests/unit/test_export.py tests/e2e/test_edit.py` (full diff read).
- Read the data path on the 59c7edb tree: `app/backend/store.py:45-49` (edited payload carries originals into the export view), `app/backend/review.py:98` and `:136` (an edit keeps the first original), `app/backend/export.py:474-491` (`_was_edited` and `_edited`), `app/backend/export_routes.py:50` (route).
- Extracted 59c7edb with `git archive` to the session scratchpad. `.venv/bin/python -m pytest tests/unit/test_export.py -p no:cacheprovider -q` from inside that tree gives `21 passed`.
- Started my own server from that tree on a spare port: `HOST=127.0.0.1 PORT=7871 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratchpad>/app-7871.sqlite3 .venv/bin/python -m app.main`. Health check returned `"ok":true`. Chris's app on 127.0.0.1:7860 was not used; I made one read-only GET to its root to confirm it was still up.
- `E2E_BASE_URL=http://127.0.0.1:7871 .venv/bin/python -m pytest tests/e2e/test_edit.py -p no:cacheprovider -v -rA` from the tree gives `6 passed` (including `test_notes_list_edited_item_with_both_texts` at `tests/e2e/test_edit.py:31`, whose xfail the commit removed).
- `.venv/bin/python -I artifacts/review-evidence/T-069-claims-adjuster-probe.py http://127.0.0.1:7871`, real API calls (sample case, entry 3):
  - A, edit then accept: EDITED ITEMS shows `summary was "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.", now "Persistent severe neck pain 6/10 and daily headaches; ..."`. Letter contains the new text. Letter contains no "edited" and no "was".
  - B, edit then dismiss: EDITED ITEMS is `- none`. Letter contains neither the original nor the edit.
  - C, edit, accept, then reset: EDITED ITEMS is `- none`. Letter contains neither text.
- Stopped my server (PID 20790, `python -m app.main` on 7871). Confirmed 7871 is down and 7860 still answers.
- `grep -rn -i severe evals/golden/`: the sample record 3 text is "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved." It contains no severity word (source: `evals/golden/hallucinations_controls.jsonl:2`).

## Findings

One minor finding (in JSON below). No blockers, no majors within T-069's scope, so `pass`.

```json
{"card": "T-069", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 59c7edb (git archive, scratchpad tree); export.py _was_edited/_edited; tests/unit/test_export.py; tests/e2e/test_edit.py via a spare server at 127.0.0.1:7871; real API probe. Paralegal persona review still outstanding.",
 "exercised": ["git show 59c7edb -- app/backend/export.py tests/unit/test_export.py tests/e2e/test_edit.py",
   "read store.py:45-49, review.py:98-136, export.py:474-491, export_routes.py:50 on the commit tree",
   ".venv/bin/python -m pytest tests/unit/test_export.py -p no:cacheprovider -q -> 21 passed",
   "own server from the commit tree on 127.0.0.1:7871 (health ok); E2E_BASE_URL=http://127.0.0.1:7871 .venv/bin/python -m pytest tests/e2e/test_edit.py -p no:cacheprovider -v -rA -> 6 passed; server stopped (PID 20790)",
   "artifacts/review-evidence/T-069-claims-adjuster-probe.py against 127.0.0.1:7871: case A edit+accept lists both texts and the letter has no edit marker; case B edit+dismiss lists none; case C edit+accept+reset lists none",
   "grep -rn -i severe evals/golden/ (record 3 text has no severity word)"],
 "verdict": "pass",
 "scores": {"edited_then_accepted_listed": 5, "dismissed_edit_not_listed": 5, "original_and_new_text_kept": 5, "letter_has_no_edit_marker": 5, "added_words_checked": 2},
 "findings": [
  {"severity": "minor",
   "title": "A paralegal edit can add a severity word the record does not say; no check covers added words, and the letter receives it",
   "evidence": "artifacts/review-evidence/T-069-claims-adjuster-probe.py case A: original summary 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.' edited to 'Persistent severe neck pain 6/10 ...' and accepted. Letter contains 'Persistent severe neck pain 6/10'. Record 3 text in evals/golden/hallucinations_controls.jsonl:2 has no 'severe'. The code check in D-006/D-034 (memory/ORCHESTRATOR_DECISIONS.md:14 and :44) covers numbers, dates and dollars only.",
   "why_it_matters": "Persona section 4 item 18 bars severity adjectives unless verbatim in a record, and item 6 asks that edits be auditable. The audit trail works: EDITED ITEMS records the original and the new text. The gap is that nothing marks an added severity word as absent from the excerpt, so the letter can carry an invented severity with only the notes as a trace. This path predates 59c7edb (the edit was always possible), so it is not a regression of this card. Minor because the paralegal made the edit and it is recorded.",
   "fix": "Decision for Chris: either (a) add a needs_review reason or a notes line 'added words not in excerpt' when an edit adds a word absent from the excerpt, or (b) keep it as paralegal judgment and record that in D-010 so the gap is a decision, not an oversight.",
   "acceptance_test": "Edit adding 'severe' to entry 3 is either returned needs_review with a reason, or listed in internal notes as an added word not in the excerpt, per the chosen option; the choice is recorded in D-010."}
 ],
 "whats_right": [
  "Edited then accepted: EDITED ITEMS shows the original and the new summary, and the letter carries the new text with no 'edited' marker (probe case A; test_edit.py:31 passes).",
  "Edited then dismissed, or edited, accepted and reset: nothing listed and the entry is absent from the letter (probe cases B and C; test_accepted_unedited_and_dismissed_edited_not_listed passes).",
  "The xfail is removed and tests/e2e/test_edit.py passes 6/6 on a live server, not only on the unit fixture."
 ],
 "questions_for_chris": [
  "Should an edit that adds a word absent from the excerpt (e.g. 'severe') get a needs_review reason or a notes line? (minor finding)",
  "The card was requested as a paralegal-reviewer pass. Who runs the paralegal review of T-069, and in a fresh context?"
 ]}
```
