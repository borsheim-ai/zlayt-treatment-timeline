# T-120 paralegal re-check (round 4, scoped)

**Verdict: pass, for what T-120 changed.** The semicolon drop is pre-existing, not a T-120 regression: the parent 0c47356 gives the same flag and the same excerpt on the brief's sentence. This pass does not clear the r3 blocker. It stays open on HEAD a44dced as a pre-existing defect, owned by T-132 (ready, P1). Until T-132 lands, `verify_quickly` is 3, below the ship bar of 4. Reason: every flag excerpt is a verbatim substring I could find in one step, but on the S6 shape the flag hides the prior condition, so a paralegal must open record 1 to learn what the prior is.

Scope: parent 0c47356 and HEAD a44dced, each run from a fresh `git archive` copy in the session scratchpad (`t120r4/parent/zlayt`, `t120r4/head/zlayt`), fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. The T-120 commit f7829c1 (`t120r4/t120/zlayt`) was also run at engine level. Its range includes T-126 commit 6d01774, which touches flags.py, present.py and others but not lexicon_scan.py or sentences.py. The only sentence-code changes in the range are T-120's (1cb8707, 07dbd2b, f7829c1).

## 1. Regression or pre-existing? Pre-existing.

Case: `artifacts/review-evidence/T-120-r4-case.txt`. Record 1 carries the brief's sentence, "Hx obtained via patient's son; neck pain and headaches."

| Build | Paste (route, pre-approved in launcher) | Prior flag excerpt(s) | "neck pain and headaches" in a flag |
|---|---|---|---|
| parent 0c47356 | 201, run ready | "Hx obtained via patient's son;" (record r1) | no |
| HEAD a44dced | 201, run ready | "Hx obtained via patient's son;" (record r1) | no |

- Evidence: `artifacts/review-evidence/T-120-r4-http-parent-0c47356.json` and `artifacts/review-evidence/T-120-r4-http-head-a44dced.json` (prior flags identical).
- Engine, parent, f7829c1 and HEAD: S6 gives the same excerpt in all three (`artifacts/review-evidence/T-120-r4-compare.txt`, S6 block).
- Why it predates T-120: `app/backend/sentences.py` is byte-identical at 0c47356, a44dced and f7829c1 (sha256 prefix 17c69514a8b56f0b; `artifacts/review-evidence/T-120-r4-archive-check.txt`). The ';' unit cut is at sentences.py:36-37 and the excerpt comes from stripped_spans (sentences.py:69). T-120's skip does not change the excerpt. It only decides whether the hit survives on the rest of the sentence (lexicon_scan.py:115-124).

## 2. What T-120 changed, judged on that alone

Parent to HEAD, 21 engine sentences and 4 library/sample cases:

- Intended and working: an attribution-only history line no longer raises the flag. S2 "Hx obtained via patient's son, who interpreted.", S7, S12 and N3 flag on parent and are quiet on HEAD. lib09 record 1 pre-existing list: parent 1 flag ("Hx obtained via patient's son, who interpreted."), HEAD 0 (`artifacts/review-evidence/T-120-r4-libdiff.txt`).
- Intended and working: S13 "Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019." flags only "Prior lumbar strain 2019." on HEAD; parent flags the attribution sentence as well.
- No loss against parent: every sentence where parent shows a condition in a flag excerpt still does on HEAD. The only probe where the condition is missing is S6, in both builds. The rows that differ from parent are the attribution-only removals (S2, S7, S12, N3) and the attribution half of S13. Library and sample priors match parent exactly: lib02 (5 flags), lib11 (4 flags), sample (2 flags: "Patient reports low back pain in 2023, resolved." and "Findings may represent degenerative change").
- f7829c1 and HEAD (a44dced, which adds T-126 r2) give identical excerpts on all 21 probes, so a44dced changed no excerpt here.

## 3. The r2 blocker forms flag on HEAD, with the whole sentence as the excerpt

- S4 "Hx obtained via patient's son, who reports neck pain." flags; excerpt is the whole sentence. Same as parent.
- S11 "Hx obtained via EMS crew, who relayed lumbar strain." flags; whole sentence. Same as parent.
- S15 "Hx obtained via patient's son, who interpreted, and reports lumbar strain." flags; whole sentence. Same as parent.
- Also re-checked: S5, N1, N4 (who reports headaches and dizziness) and N5 (prior shoulder surgery), all flagged with the condition in the excerpt.

## 4. Pre-existing, same as parent, not counted against T-120

- **S6 semicolon form (r3 blocker): still open on HEAD. Severity stays blocker for the product.** The flag shows only "Hx obtained via patient's son;" and "neck pain and headaches" is in no flag. Parent does the same. T-132 AC 1 names this shape ("the flag's quote extends to the following clause... so the condition is shown"). The M3 gate and T-132 must see it open. This review does not clear it.
- S8 "Hx via interpreter, who interpreted; prior neck injury." and N2 "Hx obtained from patient's husband; prior cervical strain.": two flags each (the ';' fragment, then the condition), same on parent. The period form (S2) is quiet. T-132 AC 1 says "plus T-120 paralegal r3 forms", which should include these; the orchestrator should confirm.
- S16 "Hx obtained via patient's son, who interpreted, denies neck pain.": flags on parent and on HEAD (the r3 minor, "regression" from the r2 build). The r2 build was not the shipping baseline. Not counted here; it is a question for Chris (below).

## 5. Minor, owned by T-120

- Card AC 1 still says the interpreter sentence is in "record 2". The sentence is lib09 record 1 (`evals/library/case_lib09_spanish_interpreter_espalda.txt`, record 1 excerpt). `python3 tools/board.py show T-120` prints it at line 24. Fix through the board: the AC text cannot be hand-edited.

## Method and disclosures

- The stock build refuses custom text: POST /api/cases returns 409 demo_mode_unsupported_input on parent and HEAD (`artifacts/review-evidence/T-120-r4-http-stock-parent-0c47356.json`, `...-stock-head-a44dced.json`). To paste the case through the real route, the launcher (`artifacts/review-evidence/T-120-r4-launch.py`) adds the case's SHA-256 digest to the process's recorded-text set, the same set the stock build fills from evals/golden. Nothing under the archive was edited. Both builds were treated the same way.
- I did not open the browser this round. The flags above come from the JSON of POST /api/cases and GET /api/cases/{token}, not from the rendered page.
- Two earlier server pairs ran from a first extraction, and I could not confirm that copy was intact (the directory no longer held the tree I had extracted). I stopped those servers and cite only the fresh copies under `t120r4`.

## Servers stopped by PID

Final pair: 71020 (parent, 7901) and 71023 (HEAD, 7902). Stock pair: 74738 and 74740. Earlier pairs were also stopped: 67603, 67605, 68554, 68556. After each stop, `lsof -iTCP:7901|7902 -sTCP:LISTEN` returned nothing (exit 1) and `curl` to /api/health returned 000.

## What I exercised

- personas/paralegal.md in full; reviews/T-120-paralegal-r3.md; memory notes on T-120 r2/r3.
- `python3 tools/board.py show T-120` (status blocked; §7.4 triage note 2026-11-02T11:50:07Z; AC 1 says record 2), `show T-132` (ready, P1), `list --status blocked`.
- `git rev-parse` for 0c47356, a44dced and f7829c1; `git log 0c47356..f7829c1 -- app/backend/lexicon_scan.py app/backend/sentences.py app/backend/flags.py` (f7829c1, 07dbd2b, 6d01774, 1cb8707).
- `git archive` into the scratchpad; `artifacts/review-evidence/T-120-r4-archive-check.py` against git objects (file counts 1980/2040/2040; sha match on the three engine files).
- Stock launch on 7901 and 7902 (preapprove 0), POST /api/cases with the case: 409 on both.
- Pre-approved launch, same routes: paste, run, status, GET case. `artifacts/review-evidence/T-120-r4-probe.py paste` on both.
- `artifacts/review-evidence/T-120-r4-probe.py engine` on the three copies (21 sentences, raised and condition-in-excerpt checks); `T-120-r4-compare.py` table.
- `artifacts/review-evidence/T-120-r4-probe.py library` on both servers (lib09, lib02, lib11, sample); `T-120-r4-libdiff.txt`.
- Read app/backend/sentences.py:36-37 and :69; app/backend/lexicon_scan.py:28 and :115-124.
- Not run: browser UI, pytest (backend and staff lane), the live LLM path, and T-132's "Hx per MS history" case.

## Questions for Chris

- Should a negated condition ("denies neck pain") raise a prior-condition flag? The shipping baseline (0c47356) flags it, so it is not a T-120 change. Your answer decides whether it becomes a T-132 item.
- Is it intended that a custom case cannot be pasted in ZLAYT_MODE=local with the fixture backend (409 demo_mode_unsupported_input on both builds)? Outside T-120, but it means a paralegal cannot paste her own case in that mode.

```json
{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "Round-4 scoped check. Parent 0c47356 vs HEAD a44dced (T-120 commit f7829c1 also run at engine level; its range includes T-126 commit 6d01774, which does not touch the sentence code). App on 127.0.0.1:7901 (parent) and 127.0.0.1:7902 (HEAD) from fresh git archive copies in the session scratchpad t120r4/{parent,head,t120}/zlayt; fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. Case artifacts/review-evidence/T-120-r4-case.txt (two synthetic records; record 1 carries 'Hx obtained via patient's son; neck pain and headaches.').",
 "exercised": [
  "read personas/paralegal.md in full, reviews/T-120-paralegal-r3.md, and the T-120 r2/r3 memory notes",
  "python3 tools/board.py show T-120 (status blocked; newest note 2026-11-02T11:50:07Z §7.4 triage; AC 1 still says record 2), show T-132 (ready, P1; AC 1 names the semicolon shape), list --status blocked",
  "git rev-parse 0c47356, a44dced, f7829c1; git log 0c47356..f7829c1 -- app/backend/lexicon_scan.py app/backend/sentences.py app/backend/flags.py gave f7829c1, 07dbd2b, 6d01774, 1cb8707",
  "git archive --prefix=zlayt/ for each commit into the scratchpad t120r4/{parent,head,t120}; artifacts/review-evidence/T-120-r4-archive-check.py compared file counts (1980, 2040, 2040) and sha256 of lexicon_scan.py, sentences.py, flags.py against git objects; output artifacts/review-evidence/T-120-r4-archive-check.txt",
  "launched artifacts/review-evidence/T-120-r4-launch.py with preapprove 0 on 7901 and 7902; POST /api/cases with the case text returned 409 demo_mode_unsupported_input on both (T-120-r4-http-stock-parent-0c47356.json, T-120-r4-http-stock-head-a44dced.json)",
  "launched the same launcher with preapprove 1 (the case digest added to app.state.recorded in-process only; no archive file edited); artifacts/review-evidence/T-120-r4-probe.py paste: POST /api/cases 201, POST run, status ready, GET case; flags in T-120-r4-http-parent-0c47356.json and T-120-r4-http-head-a44dced.json, identical",
  "artifacts/review-evidence/T-120-r4-probe.py engine on the three copies: 21 sentences (S1 to S16, N1 to N5), raised and condition-in-excerpt checks; T-120-r4-engine-parent-0c47356.json, T-120-r4-engine-t120-f7829c1.json, T-120-r4-engine-head-a44dced.json; side-by-side T-120-r4-compare.txt (artifacts/review-evidence/T-120-r4-compare.py)",
  "artifacts/review-evidence/T-120-r4-probe.py library on both servers (lib09, lib02, lib11, sample through the real routes); diff in T-120-r4-libdiff.txt",
  "read app/backend/sentences.py:36-37 and :69, app/backend/lexicon_scan.py:28 and :115-124",
  "stopped every server by PID (final pair 71020 and 71023; stock pair 74738 and 74740; earlier pairs 67603, 67605, 68554, 68556); lsof on 7901 and 7902 returned nothing (exit 1); curl returned 000",
  "not run: browser UI (flag card not seen on screen this round), pytest, live LLM path (fixture only), T-132's 'Hx per MS history' case"],
 "verdict": "pass",
 "scores": {"verify_quickly": 3, "prior_mentions_flagged": 3, "interpreter_sentence_not_flagged": 5, "no_regression_vs_parent": 5},
 "findings": [
  {"severity": "minor",
   "title": "Card AC 1 still says the interpreter sentence is in lib09 record 2",
   "evidence": "python3 tools/board.py show T-120, line 24: AC 1 text '...on the interpreter-history sentence of record 2; ...'. The sentence is lib09 record 1 (evals/library/case_lib09_spanish_interpreter_espalda.txt, record 1 excerpt); the flag in artifacts/review-evidence/T-120-r4-http-head-a44dced.json sits on record r1 of the case.",
   "why_it_matters": "Checklist item 3: a reviewer or paralegal who opens record 2 will not find the sentence. The evidence line says record 1, but the AC text is still wrong.",
   "fix": "Correct AC 1 to 'record 1' through the board (orchestrator route; the AC text cannot be hand-edited).",
   "acceptance_test": "python3 tools/board.py show T-120 prints 'record 1' in AC 1 and no 'record 2'."}
 ],
 "whats_right": [
  "The interpreter-only history line no longer flags on HEAD: lib09 record 1 pre-existing list goes from 1 flag on the parent to 0 on HEAD; engine S2, S7, S12 and N3 are quiet on HEAD and flag on the parent.",
  "The r2 blocker shapes flag on HEAD with the whole sentence as the excerpt, the same as the parent: S4 'who reports neck pain', S11 'EMS crew, who relayed lumbar strain', S15 'who interpreted, and reports lumbar strain'.",
  "Against the parent, no prior-condition excerpt is lost by T-120: all 21 engine rows match except the intended attribution-only removals, and library priors (lib02 5, lib11 4, sample 2) are identical."],
 "questions_for_chris": [
  "Should a negated condition ('denies neck pain') raise a prior-condition flag? The shipping baseline 0c47356 flags it too, so it is not a T-120 change; your answer decides whether it becomes a T-132 item.",
  "Is it intended that a custom case cannot be pasted in ZLAYT_MODE=local with the fixture backend (409 demo_mode_unsupported_input on both builds)? Outside T-120, but a paralegal cannot paste her own case in that mode."]}
```
