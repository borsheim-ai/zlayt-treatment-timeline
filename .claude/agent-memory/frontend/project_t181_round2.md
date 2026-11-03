---
name: t181-round2
description: T-181 r2 hooks (outside-word underline, Bates preview, G.healthNow/local_mode, droppedText, phone layout rules) and pitfalls
metadata:
  type: project
---

- **404 on first paint**: public mode answers 404 on GET /api/cases (Home) and /api/library (/new) by design; only `health.local_mode` (T-197) tells the page. Use `G.healthNow(signal)` (shares the shell's health promise); skip the probe when `local_mode === false`. test_round2 starts its own PUBLIC server (module fixture, ZLAYT_MODE unset) and a route-injected health proves the frontend half.
- **Provenance follows the case**: `G.provenance(c)` defaults to `G.store.current`; a case with `models.generator_prepared === false` is "recorded" even when the server's curated set is on. Set in app.js paintCase and on the `case` event.
- **Outside words**: step2.js `outsideParts` underlines words of the line not in the quote (stopwords skipped, 's' stemmed) only on disputed or edited lines; grey box heading is "outside the highlighted words" (backend `uncovered` = sentences no line quotes, NOT sentences no line uses).
- **Refused edit**: server 422 invalid_edit carries `detail.qualifiers` (kinds only); `R.droppedText` finds the words (first in the old summary, else the quote). S.lastEdit is set in step2 save. R.plain fixes "the quote gives/carries" grammar.
- **Phones**: `.work.needs-check` (class set in render when the foot has a checkbox) gives the line card the room; never auto-scroll the line card. Step list overlay leaves a 36px top band so the toggle (z-index 40) stays tappable. Step 3 done tables become cards below 760px (data-label from table()). Multi-record warnings show a window around each highlight (`windowOf`) with a "Show the whole of record N" toggle.
- **Focus pitfall**: when Yes is refused and no checkbox exists, focusFirst puts focus on the card foot (tabindex -1), never on No; pressing A says "not available here".
- Test recipe: tests/e2e/guided/test_round2.py; verify from a git archive made with a temp index (GIT_INDEX_FILE under the scratchpad; the git-guard hook blocks `rm` with an unresolved $ expansion, so use fresh dir names).
