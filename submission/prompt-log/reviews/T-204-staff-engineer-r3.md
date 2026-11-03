# T-204 review — staff-engineer-reviewer (round 3), commit 68f67cc

Verdict: pass (no blocker, no major; two minors and one nit remain). Both r2 findings that gated the card are fixed and verified on a fresh `git archive 68f67cc`:

1. The r2 blocker (AI-check panel says "The AI said:" about the prepared answers on the plain sample) is gone. The panel now reads "Where code and the prepared answers read an item differently (1 item)", the chip "The phrase list and the prepared answers disagree", and "The prepared answers said: The prepared answers did not include it." My r2 probe P1 passes. The Technical-detail line is keyed the same way.
2. The r2 major (guided footer says "drafted by AI" until /api/health answers) is gone. With health held the footer reads "Checked by code; you decide every item."; with health failing (500) it stays neutral and no walked page paints "drafted by AI"; after health it reads the prepared sentence. A live-looking health (demo_mode false) still says "drafted by AI" (control), so the live sentence is not lost.
3. Allow-list: the open verb list is gone; `_leaks("The AI said: The prepared answers did not include it.")`, "The AI found it.", "the AI disagrees with ...", and a non-measured backend name all return a leak. Residual looseness is a nit.
4. Mutants: the guided footer mutant (F) fails the guided test, as asked. 12 of 13 mutants die; the one survivor (E, classic banner falls back to the server's string) is equivalent because the server sends the same sentence (api.py:39 equals app.js:5).
5. Full tests/e2e from a fresh archive, E2E_REQUIRE_DB=1: 570 passed, 1 skipped, 0 failed (817 s), matching the card.

```json
{"card": "T-204", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 68f67cc (parent fc37fbc, ancestor of HEAD 88c73dd): app/frontend/judges.js, app/frontend/guided/app.js, tests/e2e/test_prepared_first_paint.py; fresh git archive 68f67cc with private fixture-backend servers (curated set, ZLAYT_MODE=local, LLM_BACKEND=fixture); classic UI at /classic and guided UI at /; prepared sample case",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-204-staff-engineer-r2.md, the card and handoff (board.py show T-204), my memory file project_t204_prepared_wording_patterns.md",
  "git show 68f67cc (3 files, 117 insertions, 8 deletions) in full; git merge-base --is-ancestor 68f67cc HEAD: ancestor; git log 68f67cc^..68f67cc: one commit",
  "git archive 68f67cc into a scratch dir; r2 probes copied in: artifacts/review-evidence/T204_r2_probe_narrow.py (P1 plain-sample AI-check panel, P2 guided footer with health held) and T204_probe_rail.py: 3 passed; P1 output 'Where code and the prepared answers read an item differently (1 item)'; P2 before health 'Checked by code; you decide every item.', after health 'Demo: sample answers prepared by our team. Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.'",
  "T204_r2_probe_guided.py (document-wide observer plus 30 ms scan; guided home, step 1 done screen, step 2, 3, 4 with the held accepted item; classic rail, AI-check panel, Why/trace/audit, export): 2 passed; read every listed text: guided 5 texts with AI/model words (all second-check or 'not written by an AI model' or the step 1 banner), classic 37 (all second-check wording, the judge's model id, 'records split by code (not AI)', the calibration sentence 82/83 and 11/11 on the claude-cli backend (10 golden cases, small sample), the rail legend 'checked by a second AI model'); no 'The AI said', 'the AI disagree', 'drafted by AI' or 'kept the AI's summary'",
  "New probes artifacts/review-evidence/T204_r3_probe_fresh.py: F1 guided with /api/health 500 (footer 'Checked by code; you decide every item.', 142 texts, no drafted-by-AI, no leaks), F3 plain sample with the flag item dismissed, reset, accepted then the AI-check panel with every details open (706 texts, 0 leaks, panel lines say 'prepared answers'), F4 guided with health faked live (footer 'Summaries and warnings are drafted by AI and checked by code' kept: control), F2 classic with health held (page never paints a case before health: timeline wait timed out, so there is no pre-health window to scan)",
  "Called the test's _leaks() directly (python -I, scratch T204_r3/leakcheck.py) on 13 phrases: 'The AI said: The prepared answers...', 'The AI wrote this summary', 'AI-drafted summary', 'The AI found it.', 'Drafted by the model', 'the AI disagrees with the prepared answers' and a claude-api backend sentence are leaks; 'The AI check wrote the summary' is not (nit)",
  "13 mutants in separate archive copies (artifacts/review-evidence/T204_r3_mutate.py --all, runner T204_r3_run_mutants.py, each grep-confirmed single match): A rail held words, B rerun label, D judges loading prepared=false, F guided footer default back to 'drafted by AI' (required), G row label back to 'The AI said: ', H technical-detail label back to 'the AI said', I chip back to DIS, J group heading back to 'the AI', K DIS_PREP off, L classic PREPARED_BANNER constant to the live sentence, M guided step 1 banner hard-coded live sentence, N preparedFor case-level fallback removed: all KILLED; E classic banner fallback to server string: SURVIVED (equivalent)",
  "tests/e2e/test_prepared_first_paint.py on the clean archive: 8 passed (12 s); grep of the new tests for sleep/wait_for_timeout/except/skip: none",
  "Full tests/e2e from a clean git archive 68f67cc, E2E_REQUIRE_DB=1: 570 passed, 1 skipped in 817 s; log artifacts/review-evidence/T204_r3_full_e2e_68f67cc.log (the skip's reason not looked up)",
  "git diff --cached --name-status in the shared repo: M guided/app.js, judges.js, tests/e2e/test_prepared_first_paint.py still staged (finding 2)"
 ],
 "verdict": "pass",
 "scores": {"AC 1: no AI wording for a prepared case, every screen": 4, "r2 blocker fixed (AI-check panel on the plain sample)": 5, "r2 major fixed (guided footer before health)": 5, "test strength (mutation)": 4, "allow-list precision": 4, "commit hygiene": 3},
 "findings": [
  {"severity": "minor",
   "title": "Guided step 1 banner is still the server's global string, not keyed to the open case; the prepared sentence is still copied in two places with no test tying them",
   "evidence": "app/frontend/guided/step1.js:272 `hl.ai_banner ? h(\"p\", ..., hl.ai_banner)` prints the health string for every case, while G.provenance() (guided/app.js:45-50) keys on the open case's models.generator_prepared. app/frontend/app.js:5 PREPARED_BANNER duplicates app/backend/api.py:39; `grep -rl PREPARED_BANNER tests app` finds only those two files. Mutant E (app.js:11 fallback to the server's string) survives all 8 tests because the strings are equal. This is the r2 minor 4, which the handoff says was left for a later round; I did not build a case with generator_prepared=false on a prepared server.",
   "why_it_matters": "A string copied by hand drifts; a test that cannot tell the copy from the server's text means a later edit to one side passes silently. On a prepared server, a case written by a model would still read 'prepared by our team' on step 1.",
   "fix": "Drop the client copy (use h.ai_banner) or add a test that GET /api/health ai_banner equals the classic constant; derive the step 1 sentence from G.provenance() of the open case.",
   "acceptance_test": "A test fails when app.js:5 and api.py:39 differ; a case stub with models.generator_prepared=false on a prepared server prints no 'prepared by our team' on step 1."},
  {"severity": "minor",
   "title": "Shared index again stages the pre-68f67cc state of the card's three files",
   "evidence": "git diff --cached --name-status: M app/frontend/guided/app.js, M app/frontend/judges.js, M tests/e2e/test_prepared_first_paint.py. git diff --cached --stat: 8 insertions, 117 deletions across those paths, i.e. the reverse of the commit (third round this hazard shows up).",
   "why_it_matters": "A commit made without a pathspec would silently revert T-204 r3.",
   "fix": "Orchestrator: git reset -q -- those 3 paths after confirming nobody has real staged work there; commit by pathspec only.",
   "acceptance_test": "git diff --cached --name-only prints none of the 3 paths."},
  {"severity": "nit",
   "title": "Allow-list still forgives any sentence containing 'AI check'; judge_objects branches for a prepared item are not reachable by the fixture and so untested",
   "evidence": "tests/e2e/test_prepared_first_paint.py SECOND_CHECK includes r\"AI[- ]?checks?\\b\"; leakcheck: _leaks(['The AI check wrote the summary']) is False. DIS_PREP.judge_objects, the second-AI-check branch of whoSaid (judges.js:25) and the 'the answers' mixed heading (judges.js dWho) are not exercised: the curated fixture produces only sources_disagree for the plain sample.",
   "why_it_matters": "Closed-list lesson from r1 and r2: the next AI-attributing sentence that happens to contain 'AI check' passes. The unreached branches are about the real judge, so the wording is accurate either way; the risk is drift.",
   "fix": "Pin the AI-check phrases to the existing labels; stub /judges with a judge_objects disagreement on a prepared item and assert 'the second AI check said'.",
   "acceptance_test": "_leaks(['The AI check wrote the summary']) returns a leak; a stubbed judge_objects disagreement on a prepared item reads 'The second AI check said:'."}
 ],
 "whats_right": [
  "The disagreement wording is keyed per item by who answered (prepared answers vs second AI check vs live AI) in the chip, row, Technical detail and group heading, and all five keyed spots have a mutant that dies.",
  "G.provenance() makes no claim until health answers and stays neutral when health fails, while a live health still says 'drafted by AI'.",
  "The allow-list is narrowed to whole sentences and the calibration regex is pinned to the measured claude-cli sentence; no fixed sleeps; the rerun label now has a route-stub test."
 ],
 "questions_for_chris": []}
```
