# T-120 paralegal re-check (round 3)

**Verdict: fail.** One blocker. The four r2 blocker shapes now raise the prior flag with the whole sentence as the excerpt, and the interpreter-only sentence stays quiet. But the semicolon form of the same content ("Hx obtained via patient's son; neck pain and headaches.") flags only the source phrase. The condition after the semicolon is in no flag, so the r2 defect (the condition is dropped) is still there for this shape.

Scope: HEAD f7829c1 (the T-120 r3 commit) as a `git archive` copy in the session scratchpad (zlayt-r3/), fixture backend, ZLAYT_MODE=local, port 7896. Listener PID 53182 and launcher PID 53181 were stopped; lsof on 7896 returned nothing and curl returned 000.

Evidence: artifacts/review-evidence/T-120-r3-paralegal-probe.py (probe), artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json (21 sentences, engine), artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json (live), artifacts/review-evidence/T-120-r3-paralegal-jsoncheck.py (this file's shape check).

## Re-test of the r2 blocker sentences and the interpreter-only sentence

Engine probe on lib09 record 1 with the excerpt replaced. The card's "record 2" is record 1. Column "r2 433ac1c" is the r2 run (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json).

| # | Probe sentence (abbreviated) | r2 433ac1c | r3 f7829c1 | Expected | OK |
|---|---|---|---|---|---|
| S1 | PHx obtained via patient's son: lumbar strain 2019. | flag | flag | flag | yes |
| S2 | Hx obtained via patient's son, who interpreted. (interpreter-only) | none | none | none | yes |
| S3 | Hx obtained via interpreter: lumbar strain 2019. | flag | flag | flag | yes |
| S4 | Hx obtained via patient's son, who reports neck pain. (r2 blocker) | none | flag, whole sentence | flag | yes |
| S5 | Hx obtained via patient's son, who reports chronic neck pain. | flag | flag | flag | yes |
| S6 | Hx obtained via patient's son; neck pain and headaches. (r2 blocker) | none | flag, excerpt "Hx obtained via patient's son;" only | flag, condition in the flag | NO (blocker) |
| S7 | Hx per patient's son, who interpreted. | none | none | none | yes |
| S8 | Hx via interpreter, who interpreted; prior neck injury. | flag | flag (2 flags, one on "Hx via interpreter, who interpreted;") | flag | yes (duplicate fragment) |
| S9 | Hx of lumbar strain obtained via patient's son. | flag | flag | flag | yes |
| S10 | Hx obtained via patient's son, who interpreted, lumbar strain 2019. | flag | flag | flag | yes |
| S11 | Hx obtained via EMS crew, who relayed lumbar strain. (r2 blocker) | none | flag, whole sentence | flag | yes |
| S12 | Hx obtained via patient's son, who interpreted. Lumbar strain was noted. | none | none | none | yes |
| S13 | ...who interpreted. Prior lumbar strain 2019. | flag | flag | flag | yes |
| S14 | Hx: lumbar strain 2019. (control) | flag | flag | flag | yes |
| S15 | Hx obtained via patient's son, who interpreted, and reports lumbar strain. (r2 blocker) | none | flag, whole sentence | flag | yes |
| S16 | Hx obtained via patient's son, who interpreted, denies neck pain. | none | flag | none | NO (minor) |
| N1 | Hx obtained via patient's daughter, who reports chronic low back pain since 2019. | not tested | flag, whole sentence | flag | yes |
| N2 | Hx obtained from patient's husband; prior cervical strain. | not tested | flag (2 flags: "Hx obtained from patient's husband;" and "prior cervical strain.") | flag | yes (duplicate fragment) |
| N3 | Hx obtained via EMS crew, who translated. | not tested | none | none | yes |
| N4 | Hx obtained via patient's son, who reports headaches and dizziness. | not tested | flag, whole sentence | flag | yes |
| N5 | Hx per interpreter, who interpreted, and lists prior shoulder surgery. | not tested | flag | flag | yes |

Engine check, S2 and the live lib09 case: S2 gives no flag. In the live lib09 case (ready) the pre_existing list is empty.

Live (HTTP): the paste route returns 409 demo_mode_unsupported_input, as in r2. lib09, lib02, lib11 and the sample all reach ready. Their pre_existing lists are identical to the r2 run on 433ac1c (diffed): lib02 has 5 flags, lib11 has 4, the sample keeps "Patient reports low back pain in 2023, resolved." (r3) and "Findings may represent degenerative change" (r8).

## Findings

1. **blocker: the semicolon form of a condition-naming history line drops the condition from every flag (S6).** The flag's evidence is `["Hx obtained via patient's son;"]`, so "neck pain and headaches" appears in no excerpt and has no flag of its own. Cause: `app/backend/sentences.py:36-37` ends a unit at ";", and `stripped_spans` (sentences.py:69) takes the excerpt from that unit. `app/backend/lexicon_scan.py:28` ends the source-sentence test only at `[.!?]`, so the hit survives on the rest "; neck pain and headaches" (lexicon_scan.py:124). The same content without the semicolon (S4) shows the whole sentence. The pre-T-120 build gave the same cut excerpt (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json, S6). My probe checks only whether a flag was raised, so it marked S6 as a match; the excerpt check is the finding. Fix: keep the source sentence whole through its semicolon, or give that clause its own flag. Acceptance: S6 raises a flag and an excerpt contains "neck pain and headaches"; S2 and S7 stay quiet.

2. **minor: a denial raises the flag (S16).** "denies neck pain" now flags. The r2 build gave none (T-120-r2-engine-HEAD-433ac1c.json, S16). This is an over-flag in the safe direction. Question for Chris below.

3. **minor: attribution fragments that end in ";" still raise a flag (S8, N2).** "Hx via interpreter, who interpreted;" and "Hx obtained from patient's husband;" each get their own flag, while the period form (S2) gets none. The fix belongs with finding 1: decide on the whole source unit.

4. **minor: card AC 1 still says "record 2"** (carried from r1 and r2). `python3 tools/board.py show T-120` prints "...the interpreter-history sentence of record 2". The evidence line now says record 1, but the AC text is still wrong.

## What I exercised

- Read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, and `python3 tools/board.py show T-120`.
- `git rev-parse HEAD` gave f7829c1. `git archive --prefix=zlayt-r3/ f7829c1 | tar -x` into the session scratchpad.
- Started `.venv/bin/python -m app.main` from the archive with ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, HOST=127.0.0.1, PORT=7896. `/api/health` returned 200 with demo_mode true.
- Engine probe (`.venv/bin/python -I`, ARCH=archive) for S1 to S16 and N1 to N5. HTTP probe (ZLAYT_BASE=http://127.0.0.1:7896) for the paste route and the four library cases. Diffed the HTTP output against artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json.
- Read the archive code at sentences.py:30-62 and 69, and lexicon_scan.py:28 and 115-124.
- Stopped the server: `kill 53182 53181`; `lsof -iTCP:7896 -sTCP:LISTEN -nP` returned nothing (exit 1); curl returned 000; ps showed neither PID.
- Not run: pytest (backend and staff reviewer lane). The live LLM merge path (flags.py:249) is not reachable: fixture mode, and the paste route is refused.

## What is right

- The r2 blocker shapes S4, S11 and S15 now raise the flag with the whole sentence as the excerpt.
- The interpreter-only sentence (S2) and its variants S7 and S12 raise nothing, and the live lib09 pre_existing list is empty.
- The live priors (lib02, lib11, sample records 3 and 8) are unchanged from the r2 run, and the new sentences N1, N3, N4 and N5 match their expectations.

## Questions for Chris

- Should a negated condition ("denies neck pain") raise a prior-condition flag? I count it as an over-flag (minor). Your answer decides whether S16 stays a finding.

```json
{"card": "T-120", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD f7829c1 (the T-120 r3 commit; earlier T-120 commits 1cb8707 and 07dbd2b) as a git archive copy in the session scratchpad, zlayt-r3/; app on http://127.0.0.1:7896 (fixture backend, ZLAYT_MODE=local, listener PID 53182, launcher PID 53181, both stopped); engine probes through app.backend.flags.lexicon_flags and lexicon_scan.scan on lib09 record 1 with the excerpt replaced (the card's 'record 2' is record 1); live library cases lib09, lib02, lib11 and the sample evals/golden/sample.txt",
 "exercised": [
  "read personas/paralegal.md in full, reviews/T-120-paralegal-r2.md, python3 tools/board.py show T-120 (status in_review; AC 1 still reads 'of record 2')",
  "git rev-parse HEAD gave f7829c1; git archive --prefix=zlayt-r3/ f7829c1 | tar -x -C <scratchpad> (the session scratchpad)",
  "started .venv/bin/python -m app.main from the archive with PYTHONDONTWRITEBYTECODE=1, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, LLM_BACKEND=fixture, FIXTURE_SET=curated, HOST=127.0.0.1, PORT=7896; lsof gave listener PID 53182; /api/health returned 200 with demo_mode true",
  "engine probe: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py engine > artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json; 21 sentences: S1 to S16 (the r1 and r2 set, same expectations) and N1 to N5 (new)",
  "live probe: ZLAYT_BASE=http://127.0.0.1:7896 .venv/bin/python -I artifacts/review-evidence/T-120-r3-paralegal-probe.py http > artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json; paste POST returned 409 demo_mode_unsupported_input; lib09, lib02, lib11 and sample all reached ready",
  "diffed the live pre_existing lists against the r2 run artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json: equal for lib09, lib02, lib11 and the sample",
  "read the archive code: app/backend/sentences.py:30-62 (unit_spans, ';' ends a unit at line 36-37), sentences.py:69 (stripped_spans), app/backend/lexicon_scan.py:28 (_SENT_END ends only at [.!?]) and lexicon_scan.py:115-124 (_is_source_sentence)",
  "compared against the r2 engine runs artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json (S16 none) and artifacts/review-evidence/T-120-r2-engine-base-0c47356.json (S6 excerpt cut at the semicolon before T-120)",
  "stopped the server: kill 53182 53181; lsof -iTCP:7896 -sTCP:LISTEN returned nothing (exit 1); curl returned 000; ps showed neither PID",
  "not run: pytest (the unit suite is the backend's and staff reviewer's lane) and the live LLM merge path (flags.py:249), which fixture mode and the 409 paste route cannot reach"],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "prior_mentions_flagged": 3, "interpreter_sentence_not_flagged": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Semicolon history line: the prior condition after ';' is in no flag (S6 'Hx obtained via patient's son; neck pain and headaches.' flags only the attribution fragment)",
   "evidence": "artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json probe S6: raised true, pre_existing_flags [\"Hx obtained via patient's son;\"], lexicon_hit_ids [hx_abbrev]. The words 'neck pain and headaches' are in no flag excerpt. Cause: app/backend/sentences.py:36-37 ends a unit at ';', and stripped_spans (sentences.py:69) takes each flag excerpt from that unit. app/backend/lexicon_scan.py:28 ends the source-sentence test only at [.!?], so the hit survives on the rest '; neck pain and headaches' (lexicon_scan.py:124). The same sentence without the semicolon (S4, 'who reports neck pain.') gets the whole sentence as its excerpt. Pre-T-120 build: the same truncated excerpt (artifacts/review-evidence/T-120-r2-engine-base-0c47356.json, S6). HEAD 433ac1c: no flag (artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json, S6).",
   "why_it_matters": "Checklist item 9 and card AC 1: a prior-condition mention in a history line must raise a flag whose excerpt carries the mention. Here the flag sits on the source phrase, and 'neck pain and headaches' (history content) has no flag at all. This is the r2 blocker's defect (the condition is dropped from the flag) for the semicolon shape. A paralegal who dismisses 'Hx obtained via patient's son;' as only the source phrase never sees the condition. The lexicon has no bare 'neck pain' entry, so nothing else catches it. My probe's expect column checks only whether a flag was raised, so it marks S6 as a match; this finding is the excerpt check. Not downgraded to major: the condition is absent from every flag, which is the r2 blocker.",
   "fix": "Keep the Hx source sentence whole through its semicolon, so that its flag excerpt contains the clause after ';' (as S4 does without the semicolon), or give that clause its own flag. The owner picks the rule; do not add condition words to the lexicon just for this case.",
   "acceptance_test": "Engine probe S6 ('Hx obtained via patient's son; neck pain and headaches.'): a pre_existing flag is raised AND one of its evidence excerpts contains 'neck pain and headaches' (checked on the excerpt text, not only on raised). S2 and S7 still raise nothing. Re-run artifacts/review-evidence/T-120-r3-paralegal-probe.py engine on the fixed archive, with the excerpt check added."},
  {"severity": "minor",
   "title": "Denial raises a prior flag: S16 'Hx obtained via patient's son, who interpreted, denies neck pain.' flags again (433ac1c did not)",
   "evidence": "artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S16: raised true, pre_existing_flags [\"Hx obtained via patient's son, who interpreted, denies neck pain.\"], lexicon_hit_ids [hx_abbrev]. artifacts/review-evidence/T-120-r2-engine-HEAD-433ac1c.json S16: pre_existing_flags []. Cause: lexicon_scan.py:124 keeps the hit for any word after the attribution, including 'denies neck pain'.",
   "why_it_matters": "A denial is not a prior-condition mention. The flag adds a review item that the paralegal must dismiss, and the flag text itself says a prior condition is mentioned. The direction is safe (no fact is lost), so this is an over-flag, not a blocker. It is a regression from the r2 build, which handled this sentence correctly.",
   "fix": "The owner decides: either suppress the hit when a negation word follows the source phrase, or record in the card that a denial keeps the flag by design (question_for_chris).",
   "acceptance_test": "Engine probe S16 raises no pre_existing flag, or the card records the decision to keep it. S2, S7, S12 and N3 stay quiet, and the other rows keep their results."},
  {"severity": "minor",
   "title": "Attribution fragments that end in ';' still raise a flag (S8 'Hx via interpreter, who interpreted;' and N2 'Hx obtained from patient's husband;')",
   "evidence": "artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json S8: pre_existing_flags [\"Hx via interpreter, who interpreted;\", \"prior neck injury.\"]. N2: pre_existing_flags [\"Hx obtained from patient's husband;\", \"prior cervical strain.\"]. The same attribution with a period (S2, \"Hx obtained via patient's son, who interpreted.\") raises nothing. Cause: _SENT_END (lexicon_scan.py:28) ends only at [.!?], so the rest of the sentence after ';' keeps the hit, and the excerpt is cut at ';' (sentences.py:36-37).",
   "why_it_matters": "The r3 design is that a sentence which is only attribution yields nothing. With a ';' the attribution is flagged on its own fragment, and the condition after the ';' gets a second flag. The paralegal sees two flags for one line, one of them empty of any condition. This is noise, not a lost fact.",
   "fix": "Make the decision on the whole source unit, through the ';' (see the blocker fix). The attribution-only check then runs on the whole unit, so a unit with nothing but attribution yields nothing and a unit with a condition gets one flag whose excerpt contains the condition.",
   "acceptance_test": "Engine probe: 'Hx obtained via patient's son, who interpreted;' raises no flag. 'Hx obtained from patient's husband; prior cervical strain.' raises one pre_existing flag whose excerpt contains 'prior cervical strain'. S2 is unchanged."},
  {"severity": "minor",
   "title": "Card AC 1 still says the interpreter sentence is in lib09 record 2 (carried from r1 and r2; the evidence string now admits the error, the AC text does not)",
   "evidence": "python3 tools/board.py show T-120, AC 1 text: \"...on the interpreter-history sentence of record 2; ...\"; AC 1 evidence: \"...the sentence is lib09 record 1; AC text says record 2 in error\". artifacts/review-evidence/T-120-r3-engine-HEAD-f7829c1.json: lib09_record_numbers_with_source_sentence [1].",
   "why_it_matters": "Checklist item 3: a reviewer or paralegal who opens record 2 will not find the sentence. The evidence line says so, but the AC text stays wrong.",
   "fix": "Correct AC 1 to 'record 1' through the board (orchestrator route; the AC text cannot be hand-edited).",
   "acceptance_test": "python3 tools/board.py show T-120 shows 'record 1' in AC 1 and no 'record 2'."}
 ],
 "whats_right": [
  "The r2 blocker shapes now flag with the whole sentence as the excerpt: S4 'Hx obtained via patient's son, who reports neck pain.', S11 'Hx obtained via EMS crew, who relayed lumbar strain.' and S15 'Hx obtained via patient's son, who interpreted, and reports lumbar strain.'",
  "The interpreter-only sentence raises no flag: engine S2 'Hx obtained via patient's son, who interpreted.' gives []; live lib09 pre_existing is empty; S7 and S12 are quiet too.",
  "Live priors are unchanged from the r2 run on 433ac1c (lib02 5 flags, lib11 4, sample records 3 'Patient reports low back pain in 2023, resolved.' and 8 'Findings may represent degenerative change'), and all five new sentences N1 to N5 match their expectations (N2 with the duplicate flag in finding 3)."],
 "questions_for_chris": [
  "Should a negated condition ('denies neck pain') raise a prior-condition flag? I count it as an over-flag (minor). Your answer decides whether S16 is a finding."]}
```
