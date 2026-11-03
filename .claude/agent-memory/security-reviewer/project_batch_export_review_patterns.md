---
name: batch-export-review-patterns
description: Recurring weak spots in the T-055 batch accept and T-058 export_config/audit code (regex $ newline, per-case ids, needs_review missing from the sample, untracked LLM fixtures breaking archive pins)
metadata:
  type: project
---

Reviewed T-055 (batch accept, `app/backend/case_extras.py apply_batch`, route POST /api/cases/{token}/review/batch) and T-058 (`validate_config`, export_config routes, `present.audit_view`) on 2026-11-01 at HEAD d796383.

- `_LABEL = re.compile(r"^[A-Za-z0-9 ._-]{1,20}$")` accepts a trailing newline: Python `$` matches before a final `\n`. A PUT of `{"exhibit": "7\n"}` returned 200 and the newline reached the exported letter. Any validator written with `^...$` and `.match` has this bug; use `fullmatch` or `\Z`. A leading newline is refused, which is how to tell it is the trailing `$`.
- Item ids are per case (`e1`..`e9` in every sample case). A batch can carry an id that exists in two cases; the server resolves it inside the caller's case (review.py:33). A test for cross-case isolation needs a second case with ids the first lacks, and the public demo refuses any pasted text unless it is a recorded sample (demo_mode = not live_enabled, api.py:105-106), so a longer paste cannot be made in tests.
- The sample case has only `verified`/`pending` entries. A card test that builds its "bad" list from `state != verified` gets an empty list, so the needs_review branch is never sent. Set the state with `DB.update_item(conn, id, now=0, case=tok, state="needs_review")` and `conn.commit()`.
- `git archive HEAD` omits the untracked LLM fixtures (`tests/fixtures/llm`, 326 tracked of 502 on disk, some tracked files modified in the working tree). Without copying them, sample-case tests fail at HEAD. Copy `tests/fixtures` into the pinned archive and say so in the review.
- Audit: public mode returns metadata only, no prompt, response, error, before or after; the local branch is gated on `ZLAYT_MODE == "local"` (api.py:485-490, present.py:189-190). This was correct at d796383.

**Why:** the T-055/T-058 reviews (2026-11-01). The newline bug is a contract violation found only by probing with a value the spec lists explicitly.
**How to apply:** on any new validator that uses `$`, probe a trailing newline first. On any batch or bulk endpoint, check whether the card's test actually sends each refused kind. Check whether the sample case has the state the AC names before trusting a green test. [[project-pdf-upload-review-patterns]] covers the same archive and fixture gotchas for PDF.
