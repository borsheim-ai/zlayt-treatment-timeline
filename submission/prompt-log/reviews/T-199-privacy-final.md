# T-199: D-072 final privacy sweep (one review covering T-187, T-194, T-195, T-198, T-199, T-217)

Reviewer: privacy-compliance-reviewer (Nadia Farouk persona), claude-opus-5-5, fresh context, 2026-11-03. HEAD `e0d721d`.
I read `deploy/.private_patterns` only to load the terms at run time. This file holds no private value, and no fragment or
ticker of one; every count below was produced by a script that prints kinds, lengths, shapes and paths only.

**Verdict: changes (0 blockers, 1 major).** I found no private value, in any form, in the snapshot text (files plus every git
object), the two PDFs, the 109 published images, the video, or the prompt log at HEAD. The git identity is clean, and the
README walk works from a clone of the snapshot. The major finding is that the **outside-project-name default ("Redacted") is
defeated in 9 published files**. In each, the marker sits directly before the company's stock-exchange ticker, and a ticker
names exactly one company.

## What I ran (all evidence under `artifacts/review-evidence/FINAL-privacy-*`)
1. **Snapshot build:** `SNAPSHOT_DIR=<scratchpad>/FINALpriv-snap-1793720320 bash deploy/make_public_snapshot.sh`, exit 0. Its log
   says: "prune: removed 185 … kept 114 allow-listed"; "redact: 104 replacement(s) in 29 file(s); 112 binary/utf-16 file(s) not
   rewritten"; "scan: ok (0 hits)"; "privacy_tree_scan: 4418 text file(s) checked, 0 with hits"; "history: 1 commit … remotes: 0";
   "check_secrets: ok (3926 file(s) scanned)". (My first attempt into `<scratchpad>/snap` was refused: "snapshot dir is not
   empty". That directory came from another agent, so I used a new one.)
2. **My own normalizer** (`FINAL-privacy-sweep.py`, independent of `snapshot_tool.py` and `privacy_tree_scan.py`).
   - Terms: all 14 pattern lines, including the `#@` kinds, plus the non-gmail git author addresses and their parts, giving
     17 keys.
   - Decodings: utf-8, utf-16le/be and latin-1, then `\uXXXX`, `\xXX`, `%XX` and HTML entities (two rounds), NFKC, zero-width
     removal and char-code lists.
   - Views: alnum-only casefold, plus the same with spelled "dot"/"at" removed.
   - Checks: exact; 1-edit for keys of 8+; gapped; reversed; base64 and hex; long fragments inside a single token; generic
     tailnet/CGNAT/home-path shapes.
   - **Planted control** (`FINAL-privacy-plant.py`): all 14 values in 18 disguises (plain, `+`-split, tuple, regex-escaped,
     regex-quantifier gap, `\u`, `%`, `&#N;`, spelled dot/at, letter-spaced, zero-width, upper-kebab, reversed, base64, hex,
     char codes, one typo, UTF-16LE). **18/18 detected.**
3. **Snapshot text:** 11,329 blobs, 657 MB. That is the 3,926 working files, every loose object inflated, and every object via
   `git cat-file`.
4. **Prompt log at HEAD:** `--commit e0d721d --paths submission/prompt-log`, 1,331 files, 168 MB.
5. **Triage of every raw hit class** (`FINAL-privacy-triage.py`, `-fragtriage.py`, `-devdist.py`; shapes, word classes and
   edit distances only). Each class turned out to be a false positive:
   - One `email` term **normalizes to the public git author name**: ~2,700 snapshot hits, 888 in the prompt log.
     The 12-character fragments of the full work address are that same public-name part.
   - One `email` term matched across `word <word`, where both words are dictionary words (1 file).
   - Two device terms give 1-edit and fragment hits only on generic hardware-model words. The one
     exact hit (`transcripts/session-6ddf8076-orchestrator.md`) is the model phrase followed by a digit on the next line. With
     the preceding word included, its edit distance to every device term is 7 or more.
   - One short device-name part matches the possessive of the public first name.
   - The longest device term (the one with no generic part) has **0 hits** in any form.
   - The personal and outside-name parts hit only ordinary words or a common path word (classified as dictionary words,
     dictionary words plus a suffix, or dictionary compounds; the words are not printed).
   - The `home-other` hits are a synthetic one-letter-user path in `tests/unit/test_t183_hardening.py:223` and its transcripts.
   - Third-party name: 0 hits.
6. **Binaries** (`FINAL-privacy-binx.py`):
   - 2 PDFs: `pdftotext` layout and raw, `pdfinfo` metadata, and 49 FlateDecode streams inflated.
   - 109 PNGs: text chunks (none present).
   - webm: container metadata.
   - Swept: 0 hits. The one hit was ffmpeg echoing my own scratch path.
7. **OCR** (`FINAL-privacy-ocr.py`, tesseract psm 3 and 11 at 1x and 2x, terms exact and 1-edit, plus tailnet/CGNAT/URL/`/Users/`
   shapes):
   - **109 snapshot images, 436 passes: NO HITS.**
   - Positive control on the pruned `artifacts/screenshots/m0-board*.png`: device, term and tailnet shapes all fired.
8. **Video:** Playwright's `ffmpeg-mac` (VP9 decode works) sampled `artifacts/demo.webm` at 1 fps. That webm is byte-identical
   to HEAD (`git diff --quiet`). **175 frames, 700 OCR passes: NO HITS.**
9. **Git** (`FINAL-privacy-gitcheck.py`):
   - 1 commit (`db7c2477a1`); author = committer = the public name with the gmail address.
   - Refs: `refs/heads/main` only. 0 remotes, 1 reflog entry, no non-sample hooks.
   - Objects: 3,607 blobs, 82 trees, 1 commit; 0 unreachable.
   - 0 non-gmail identities.
10. **Snapshot vs HEAD** (`FINAL-privacy-mdiff.py`):
    - 29 files changed. All six changed `.py` files pass `py_compile`; `app/frontend/stepper.js` passes `node --check`.
    - No `submission/prompt-log/` file changed, so HEAD's prompt log is already the redacted form.
11. **Run check:** `git clone` of the snapshot, then `PORT=7897 ./run.sh`:
    - `/api/health` returned 200 after 6 s, with `synthetic_only: true`, the banner text, `demo_mode: true` and `backend: fixture`.
    - API walk: sample → 201 with 9 records; run → `ready` with entries 9, amounts 4, flags 10 (the README's "19 timeline items
      and 4 bill amounts").
    - Export before answers → 422.
    - A novel paste → **409 `demo_mode_unsupported_input`**.
    - `/audit` is metadata only; `GET /api/cases` → 404; DELETE → 204. The banner is in `index.html`.
    - I killed my PID 65157; port 7897 is free afterwards.
12. **NEEDS_CHRIS** (`FINAL-needs-chris-check.py`):
    - Row 2 says to publish only the snapshot. Its count "29 commits authored with the work email" is correct (29 non-gmail of
      650).
    - Row 5's default ("Redacted") matches `REDACT_OUTSIDE_PROJECT_NAME = True` (`evals/finalize_prompt_log.py:71`).
    - Row 5 spells the outside name in the working repo. The snapshot masks it.

## Findings in short
- **major:** an exchange ticker next to the outside-name marker identifies the outside company in 9 published files.
- **minor:** NEEDS_CHRIS row 5 does not say what a "show" answer would take now that the final build exists.
- **minor:** the prompt-log README does not list the D-072 omitted transcript.
- **minor:** the snapshot's own scan does not read PDF text or video pixels, and its rewritten-code list leaves out `.js`.
- **nit:** a stale "Known limits" bullet in SNAPSHOT.md.

```json
{"card": "T-199", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "HEAD e0d721d: public snapshot <scratchpad>/FINALpriv-snap-1793720320 (deploy/make_public_snapshot.sh, 3,926 files + 3,690 git objects, demo.webm, 2 PDFs, 109 PNGs); submission/prompt-log/ at e0d721d (1,331 files); submission/NEEDS_CHRIS.md; snapshot clone run on 127.0.0.1:7897; cards T-187, T-194, T-195, T-198, T-199, T-217",
 "exercised": [
  "bash deploy/make_public_snapshot.sh into a fresh dir (exit 0; scan ok, privacy_tree_scan 0, 1 commit, check_secrets ok)",
  "FINAL-privacy-plant.py + FINAL-privacy-sweep.py planted control: 18/18 disguised forms of all 14 values detected",
  "FINAL-privacy-sweep.py --dir on the snapshot: 11,329 blobs (files + inflated loose objects + cat-file of every object), 657 MB",
  "FINAL-privacy-sweep.py --commit e0d721d --paths submission/prompt-log: 1,331 files, 168 MB",
  "FINAL-privacy-triage.py / -fragtriage.py / -devdist.py on every raw hit class (shapes, word classes, edit distances; no values)",
  "FINAL-privacy-binx.py: pdftotext + pdfinfo + 49 inflated PDF streams, PNG text chunks, webm metadata; swept, 0 hits",
  "FINAL-privacy-ocr.py on 109 snapshot images (436 passes): no hits; positive control on pruned m0-board screenshots fired",
  "Playwright ffmpeg-mac: demo.webm (identical to HEAD) at 1 fps = 175 frames, OCR 700 passes: no hits",
  "FINAL-privacy-gitcheck.py: 1 commit, public name + gmail, 1 ref, 0 remotes, 0 unreachable objects, 0 non-gmail identities",
  "FINAL-privacy-mdiff.py: 29 changed files vs HEAD, markers introduced per file; py_compile 6/6 ok, node --check stepper.js ok",
  "FINAL-privacy-ticker.py and FINAL-privacy-markerctx.py on the snapshot (outside-name marker followed by a ticker)",
  "FINAL-needs-chris-check.py: term kinds per NEEDS_CHRIS line; commit counts by author class (29 non-gmail / 650)",
  "git clone of the snapshot; PORT=7897 ./run.sh; /api/health 200 in 6 s; sample create/run/status/export/audit/list/delete; novel paste 409; banner in index.html; killed own PID 65157",
  "Read: personas/privacy-compliance.md, deploy/make_public_snapshot.sh, deploy/SNAPSHOT.md, deploy/snapshot_tool.py (grep), evals/finalize_prompt_log.py (docstring, switch, omission), submission/NEEDS_CHRIS.md, submission/prompt-log/README.md at e0d721d, ORCHESTRATOR_DECISIONS D-070..D-075"
 ],
 "verdict": "changes",
 "scores": {"no private value in published text, any form": 5, "outside-name default effective": 2, "images, PDFs and video": 5, "git identity and history": 5, "NEEDS_CHRIS accuracy": 4, "README walk from the snapshot": 5, "scan certificate coverage": 3},
 "findings": [
  {"severity": "major",
   "title": "The outside-project default ('Redacted') is defeated: the company's exchange ticker sits right after the marker in 9 published files",
   "evidence": "FINAL-privacy-ticker.py on the snapshot: 'distinct tickers next to the marker: 1', 'marker+ticker: n=16 files=9' (MASTER_PROMPT.md, docs/CONTRACT.md, submission/prompt-log/CONTRACT.md, and 6 transcripts: privacy-review-t-187-r3, privacy-review-t-194-snapshot, writer-t-188-submission-package, pm-re-review-t-185-t-186-r2, gate-panel-pm-double-check, +1). FINAL-privacy-markerctx.py: docs/CONTRACT.md:601 and MASTER_PROMPT.md:601 read 'Internal platform/applied-AI product work at <outside project> (<exchange>: <redacted ticker>)'. Other snapshot lines tie the app's stepper UI to that company's internal tool: app/frontend/stepper.js:2 'Pattern: <outside project> flow rail', memory/ORCHESTRATOR_DECISIONS.md:50 'following the <outside project> vendor-triage flow-rail pattern', memory/contracts/api.md:600, board/cards/T-081.md:22.",
   "why_it_matters": "T-193 is open. NEEDS_CHRIS row 5, prompt-log README edit 7 and T-199 promise that the name stays masked until Chris decides. A ticker is a one-to-one identifier, so anyone reading the published repo learns the employer, and with the flow-rail lines also learns that the app reuses a pattern from that employer's internal vendor-triage tool. That inference is exactly what T-193 asks Chris about. Publishing is irreversible, so shipping this decides T-193 for him.",
   "fix": "Add the ticker as one more git-ignored '#@outside' value in deploy/.private_patterns, so no value enters tracked code (D-070). Alternatively, extend OUTSIDE_RX in evals/finalize_prompt_log.py so that an '(<EXCHANGE>: <TICKER>)' parenthetical right after the outside name becomes part of the same '<outside project>' span. Rebuild the prompt log and the snapshot. Or get the T-193 answer from Chris first.",
   "acceptance_test": "On a fresh snapshot, FINAL-privacy-ticker.py prints 'marker+ticker: n=0', and FINAL-privacy-sweep.py with the ticker loaded as a term reports 0 text-file hits outside binaries. Do the same for submission/prompt-log/ after the rebuild. Add a unit case to tests/unit/test_finalize_prompt_log.py with a synthetic name followed by a synthetic '(EXCH: XYZ)' parenthetical."},
  {"severity": "minor",
   "title": "NEEDS_CHRIS row 5 does not say what a 'show' answer would take now that the final build exists",
   "evidence": "submission/NEEDS_CHRIS.md:17 says 'The final prompt-log build (T-187) follows your answer.' However, HEAD e0d721d is 'feat(qa): T-187 final prompt-log build (D-072/D-075)', built under the default. In evals/finalize_prompt_log.py only the bare name has a switch (REDACT_OUTSIDE_PROJECT_NAME, line 71). The third-party name and personal file names are always masked (THIRD_RX, PERSONAL rules), and outside-repo tool results are always omitted (_render, lines 263-275). The row asks one show/redact question about all three classes.",
   "why_it_matters": "Chris may answer 'show' expecting the quotes and file names to appear, or expecting that nothing else needs to happen. In fact, 'show' needs the switch flipped and both the prompt log and the snapshot rebuilt and re-swept, and the quotes cannot be shown without a code change. The default itself ('Redacted') is stated accurately.",
   "fix": "Reword row 5. State the default per class (outside name: switch, default on; third-party name and personal file names: always masked; outside-repo quotes: always omitted). Say that 'show' means flipping the switch at evals/finalize_prompt_log.py:71, then rebuilding the prompt log and the snapshot, then re-running the privacy sweep before publishing.",
   "acceptance_test": "Row 5 names the switch, the per-class defaults and the rebuild-then-re-sweep step. It no longer says the final build is waiting for the answer."},
  {"severity": "minor",
   "title": "The prompt-log README does not list the transcript D-072 excludes",
   "evidence": "D-072(2) (memory/ORCHESTRATOR_DECISIONS.md:91): '... its own transcript is excluded from the published set (listed in the README as the one omitted file)'. Grepping README.md, TOOLS.md and transcripts/INDEX.md at e0d721d for 'sweep|excluded|omitted file|D-072' finds no such line. README line 19 says 'the card that built it, T-187, is the last transcript'.",
   "why_it_matters": "The README says seven kinds of edit were made 'and nothing else'. A reader comparing it against the board will find the final privacy-sweep session (this one) and the sessions after T-187 missing, with no explanation. That is a disclosure gap in a graded artifact, not a leak.",
   "fix": "Add one line under the EDITS block. The transcript of the D-072 final privacy sweep is deliberately not included (D-072), and sessions after the T-187 build are not in this folder.",
   "acceptance_test": "grep -n 'D-072' submission/prompt-log/README.md shows the omission line; finalize_prompt_log.py keeps it on rebuild."},
  {"severity": "minor",
   "title": "The snapshot's 'passed the scan' does not cover PDF text or video pixels, and its rewritten-code list leaves out .js",
   "evidence": "deploy/snapshot_tool.py:41-51 treats .pdf and .webm as allow-listed media. The build log reads '112 binary/utf-16 file(s) not rewritten' and '109 allow-listed raster image(s) OCR-checked', so the 2 PDFs (FlateDecode text) and demo.webm are not read. deploy/SNAPSHOT.md:33 discloses the video only ('no ffmpeg; look at it by eye'), but Playwright's ffmpeg-mac on this Mac decodes VP9 and I used it to sample 175 frames. NEEDS_CHRIS row 3 asks Chris to re-render the PDFs after editing. The log lists 'rewritten code/test files (6)', all .py, while FINAL-privacy-mdiff.py shows app/frontend/stepper.js was also rewritten (a comment; node --check ok).",
   "why_it_matters": "PDFs and the video are clean today; I checked them by hand. A PDF re-rendered by Chris, or a re-recorded video, would ship under a certificate that never read it. An unlisted rewrite of frontend code is how a redaction could silently change product behaviour.",
   "fix": "In scan: run pdftotext and inflate PDF streams, then apply the same term and shape rules. Sample the video with an ffmpeg if one is found (Playwright's build qualifies), else fail with a message. List every rewritten file whose extension is not .md/.txt/.jsonl.",
   "acceptance_test": "deploy/test_snapshot_tool.py plants a synthetic term in a generated PDF and the scan fails. The build log's rewritten-code list includes app/frontend/stepper.js when it changes."},
  {"severity": "nit",
   "title": "SNAPSHOT.md 'Known limits' says the script does not touch home paths, but it does",
   "evidence": "deploy/SNAPSHOT.md:107 says home paths under the user directory, 'and the content reached through them ... are not touched by this script'. The build log reports 'finalize rules: home-directory path outside this repo: 9', and deploy/snapshot_tool.py:347 applies fpl.scrub (the full rule set, including HOME_RXS, line 237).",
   "why_it_matters": "This understates the protection Chris gets, and it contradicts D-070(2).",
   "fix": "Replace the bullet. Home paths outside the repo are masked as <home-path> (D-070), and outside-repo tool results are omitted only inside the prompt log.",
   "acceptance_test": "The bullet matches the redact log classes."}
 ],
 "whats_right": [
  "No private value in any form across 11,329 snapshot blobs, 1,331 prompt-log files, 2 PDFs, 109 images (OCR) and 175 video frames (OCR); planted control 18/18",
  "Snapshot git is exactly 1 commit by the public name with the gmail address, with no remote and no unreachable objects; NEEDS_CHRIS row 2 says to publish only that",
  "The README walk works from a clone of the snapshot (/api/health 200 in 6 s), with the synthetic banner on and a novel paste refused 409 before storage"
 ],
 "questions_for_chris": [
  "T-193: may the published repo name your employer (it is the outside project, and your bio in docs/CONTRACT.md names it via its ticker)? If yes, flip the switch and drop the major finding; if no, the ticker must be masked too before you push."
 ]}
```
