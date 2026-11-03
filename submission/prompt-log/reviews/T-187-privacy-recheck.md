# T-187: D-072 final privacy re-check, outside-project ticker fix (card T-187; same review as reviews/FINAL-privacy-recheck.md)

Reviewer: privacy-compliance-reviewer (Nadia Farouk persona), fresh context, 2026-11-03. HEAD `fcf0e0d` (rule code) over `d8126e2`
(rebuilt prompt log). Model actually run: `claude-sonnet-5-5`, not the dossier's expected `claude-opus-5-5` (flagged to the orchestrator).
This file holds no private value, no ticker and no fragment of either. Every number comes from a script that prints counts, kinds,
lengths and paths only. The ticker is derived at run time from the old build (`e0d721d`) inside the scripts.

**Verdict: pass (0 blockers, 0 majors, 2 minors, 1 nit).** The major from `reviews/FINAL-privacy-sweep.md` is fixed. At HEAD the
ticker next to the outside-project marker is gone from the prompt log (0 of 1,347 files) and from a freshly built snapshot (0 of
3,942 text files and 3,623 git blobs). I found no private value in any form. The remaining findings are hardening gaps in the new rule
and one tool hazard that I tripped over myself (disclosed below).

## Before / after (same script, same ticker)
| Check | e0d721d prompt log (old) | HEAD prompt log | Fresh snapshot at HEAD |
|---|---|---|---|
| `FINAL-privacy-ticker.py` marker + ticker | 16 in 9 files (the old finding) | 0 (`distinct tickers next to the marker: 0`) | 0 |
| whole word, any case (`FINAL-recheck-tickercount.py`) | 19 in 9 files | 0 | 0 |
| `EXCH:TICKER` / `$TICKER` | 15 / 0 | 0 / 0 | 0 / 0 |
| decoded, letter-spaced, reversed, hex, base64 (`FINAL-recheck-tickerforms.py`, control 12/12 forms) | 19 whole-word, rest 0 | 0 | 0 |
| marker followed by any `EXCH:SYMBOL` | 14 in 7 files | 0 | 0 |

The bio line now reads with two adjacent markers and no exchange or symbol (`<outside project> (<outside project>)`).

## What I ran
1. **My checker at HEAD and at the old commit**: `FINAL-privacy-ticker.py --commit HEAD submission/prompt-log`: 1,347 texts, 0 tickers. The same script on `e0d721d` is the positive control (old finding reproduced).
2. **Sweep scripts on the prompt log at HEAD** (`FINAL-privacy-plant.py` control 17 values x 18 forms; `FINAL-privacy-sweep.py --commit HEAD --paths submission/prompt-log`, 1,347 files, 169 MB). Result: **the same 39 kind/method pairs as the previous sweep of `e0d721d`**, all in the known false-positive classes (public author name, a hardware-model phrase, possessive of the public first name, ordinary words, a synthetic one-letter-user path). The outside-name key has 0 hits. The sweep drops values of 4 characters or fewer, so the ticker is checked by the dedicated scripts below (`FINAL-recheck-tickerterm.py` confirms the ticker is an `#@outside` line in the local patterns file).
3. **Fresh snapshot**: `SNAPSHOT_DIR=<new scratch dir> bash deploy/make_public_snapshot.sh`, exit 0. Log: "prune: removed 185 ... kept 114"; "redact: 106 replacement(s) in 29 file(s)"; "finalize rules: outside project name ...: 13"; "scan: ok (0 hits)"; "privacy_tree_scan: 4433 text file(s) checked, 0 with hits"; "history: 1 commit ... remotes: 0"; "check_secrets: ok (3942 file(s) scanned)".
4. **Snapshot text and git**: `FINAL-privacy-ticker.py`, `-tickercount`, `-tickerforms`, `-markerwin` (what sits within 40 characters of each of 622 markers in 133 files: 0 URLs, 0 handles, 0 exchange labels except the synthetic test fixtures, 1 "previously"-type word in a transcript that is not a company), `-adjcap` (15 capitalised neighbours, none related to any private key). `FINAL-privacy-sweep.py --dir <snapshot>` over 11,377 blobs (files plus every git object, 661 MB): **the same 39 kind/method pairs as the prior snapshot sweep, 0 outside-name hits**.
5. **Chance byte hits in binaries, judged by pixels** (the three letters occur inside compressed image and video bytes): `FINAL-recheck-gitobjs2.py` shows 7 whole-word byte hits in exactly 3 blobs: `artifacts/demo.webm` (5) and 2 PNGs (1 each); printable-ASCII ratio around the match 0.41 to 0.59 and NUL bytes present, so not text. Judged as asked:
   - **109 snapshot PNGs, 436 OCR passes** (psm 3 and 11, 1x and 2x) with `FINAL-recheck-tickerocr.py`: 0 ticker tokens, 0 near-misses, 0 exchange labels. The positive control (ticker drawn at two sizes, `FINAL-recheck-ocrctl.py`) fired 14 times.
   - **175 frames of `demo.webm`** at 1 fps (Playwright's ffmpeg-mac; the file is byte-identical to HEAD): 700 OCR passes, 0 hits.
   - **The 2 PDFs changed since the last sweep** (`product-note.pdf`, `part2-process.pdf`): `FINAL-privacy-binx.py` (pdftotext, pdfinfo, 49 inflated streams) then ticker scripts: 0 whole-word. One letter-spaced match appears inside an inflated font stream (NUL-separated glyph-id bytes next to `ÿ` padding, `FINAL-recheck-spacedctx.py`); it is font data, not text. The 5 rendered pages (OCR, 20 passes): 0 hits.
   - `FINAL-privacy-ocr.py` (all other private terms) on the 109 snapshot images: NO HITS.
6. **Rule code and tests** (`fcf0e0d`): read the diff of `evals/finalize_prompt_log.py`, `evals/privacy_tree_scan.py`, `deploy/snapshot_tool.py`, `tests/unit/test_finalize_prompt_log.py`. `.venv/bin/python -m pytest tests/unit/test_finalize_prompt_log.py deploy/test_snapshot_tool.py -q`: **56 passed**. In-process probe of `scrub()` with 16 disguised ticker forms (`FINAL-recheck-scrubprobe.py`): see finding 1.
7. **README count**: marker count at HEAD excluding the README's own mention is 586 in 116 files, matching README edit 7.

## Process disclosure: I started a rebuild of the prompt log by accident
While looking for the rule's options I ran `.venv/bin/python evals/finalize_prompt_log.py --help`. That script has no argument parsing (`evals/finalize_prompt_log.py:503`, `__main__` calls the full build), so it ran the **full rebuild into `submission/prompt-log/`** (about 10 minutes, `ps` showed the `--help` command line) until I killed it. Effects, from `git status --short submission/prompt-log` afterwards: 6 tracked files modified (README.md, REDACTIONS.md, board-activity.jsonl, transcripts/INDEX.md, the QA ticker-rebuild transcript, the orchestrator transcript; all growth since `d8126e2`, 874 insertions, 10 deletions) and 1 new untracked transcript (this review session). I ran the ticker scripts on that working-tree folder: 0 hits in every form (1,348 files). Nothing was committed, and **everything in this review used `git show HEAD:` or the `git archive HEAD` snapshot**, so my numbers are unaffected. The orchestrator should discard or re-run that rebuild deliberately (`git restore` is not available to me). This is also finding 2.

## Findings in short
- **minor:** the new ticker rule matches only the plain whole word on raw text; 8 disguised forms of it survive `scrub()` that the name rule would catch.
- **minor:** `evals/finalize_prompt_log.py` has no argument handling, so `--help` or any flag silently runs a 10-minute rebuild that overwrites the published folder.
- **nit:** the prompt-log README (edit 7) and SNAPSHOT.md do not say that the exchange ticker is also masked, nor the new rule's limits.

```json
{"card": "T-187", "persona": "privacy-compliance-reviewer", "model": "claude-sonnet-5-5",
 "scope": "HEAD fcf0e0d (rule code) over d8126e2 (prompt log rebuilt, 773 transcripts); submission/prompt-log at HEAD (1,347 files); fresh public snapshot built from HEAD by deploy/make_public_snapshot.sh (3,942 text files, 3,623 git blobs, 109 PNGs, 2 PDFs, demo.webm); prior finding: reviews/FINAL-privacy-sweep.md major; cards T-187, T-194, T-195, T-198, T-199, T-217",
 "exercised": [
  "FINAL-privacy-ticker.py --commit HEAD submission/prompt-log (0) and on e0d721d as positive control (16 in 9 files)",
  "FINAL-recheck-tickerterm.py: the ticker is loaded as an #@outside line of deploy/.private_patterns (kind and length only)",
  "FINAL-recheck-tickercount.py / -tickerforms.py (control 12/12 disguised forms) on HEAD prompt log, e0d721d prompt log, snapshot files, working-tree prompt-log folder, extracted PDF text",
  "FINAL-privacy-plant.py (17 values x 18 forms) + FINAL-privacy-sweep.py --commit HEAD --paths submission/prompt-log: 1,347 files, same 39 kind/method pairs as the e0d721d sweep, outside-name key 0 hits",
  "bash deploy/make_public_snapshot.sh into a fresh dir: exit 0, scan ok 0 hits, privacy_tree_scan 4433 files 0 hits, 1 commit, 0 remotes, check_secrets ok 3942 files",
  "FINAL-privacy-sweep.py --dir <snapshot>: 11,377 blobs (files + every git object), same 39 kind/method pairs as the prior snapshot sweep, 0 outside-name hits",
  "FINAL-privacy-markerctx.py / FINAL-recheck-markerwin.py / FINAL-recheck-adjcap.py: window around 622 markers in 133 files; 0 URLs, 0 handles, 0 exchange labels outside synthetic fixtures",
  "FINAL-recheck-gitobjs.py / -gitobjs2.py: 3,623 git blobs, 7 chance byte hits in 3 binary blobs (demo.webm, 2 PNGs)",
  "FINAL-recheck-tickerocr.py on 109 snapshot PNGs (436 passes), 175 demo.webm frames (700 passes), 5 rendered PDF pages (20 passes); positive control FINAL-recheck-ocrctl.py fired 14 times; FINAL-privacy-ocr.py (all other terms) NO HITS",
  "FINAL-privacy-binx.py on the snapshot (2 PDFs, 49 streams, 109 PNG chunks, webm metadata) then ticker scripts; FINAL-recheck-spacedctx.py on the one letter-spaced font-stream match",
  "FINAL-recheck-othersym.py / -symdist.py: the non-outside EXCH:SYMBOL strings are synthetic placeholders in test fixtures and QA transcripts (edit distance 3 to 4 from the ticker)",
  "FINAL-recheck-scrubprobe.py: in-process scrub() on 16 disguised ticker forms (read-only)",
  "pytest tests/unit/test_finalize_prompt_log.py deploy/test_snapshot_tool.py: 56 passed",
  "Read: personas/privacy-compliance.md, reviews/FINAL-privacy-sweep.md, git show fcf0e0d (4 files), evals/finalize_prompt_log.py docstring and __main__, submission/prompt-log/README.md edit 7, memory files"
 ],
 "verdict": "pass",
 "scores": {"ticker next to marker removed (log and snapshot)": 5, "no private value in any form": 5, "images, PDFs and video by pixels": 5, "ticker rule robustness vs name rule": 3, "tool safety (finalize CLI)": 2, "README/SNAPSHOT disclosure of the ticker rule": 3},
 "findings": [
  {"severity": "minor",
   "title": "The ticker rule matches only the plain whole word; disguised spellings of the ticker survive scrub()",
   "evidence": "FINAL-recheck-scrubprobe.py (in-process scrub() on evals/finalize_prompt_log.py at HEAD, OUTSIDE_WORD_RX active): masked = plain, lower-case, $TICKER, (EXCH: TICKER), EXCH:TICKER, possessive, underscore-adjacent (7 of 16). Unchanged = quote-split with +, tuple, JSON \\uXXXX, letter-spaced, regex-dotted, %XX, &#N;, comma-quoted letters (8 of 16), plus the ticker followed by a digit (correctly a different token). evals/finalize_prompt_log.py:196-202 builds OUTSIDE_WORD_RX as a raw-text whole-word regex; evals/privacy_tree_scan.py (fcf0e0d) and deploy/snapshot_tool.py use the same regex. tests/unit/test_finalize_prompt_log.py::test_outside_ticker_forms covers 4 plain cases only. Today's output has 0 of these forms (FINAL-recheck-tickerforms.py: 0 on the prompt log and the snapshot), so nothing leaks now.",
   "why_it_matters": "The name has the normalised, gapped matcher; the ticker, which identifies the same company one-to-one, has only the plain one. The project has met split literals in redaction source repeatedly (T-187 r2 to r4, T-198), and any worker or reviewer transcript that spells the ticker in a regex or in pieces would pass the scrub, the tree scan and the snapshot certificate alike. The README admits that escapes are not decoded for the name, but not that the ticker is weaker.",
   "fix": "For short outside values add a second matcher on the raw text: the value's characters separated by 0 to 3 non-alphanumeric characters, with a non-alphanumeric (or edge) on both outer sides, applied after a decode pass for \\uXXXX, %XX and &#N;. Use it in scrub(), privacy_tree_scan.py and the snapshot rules. Keep the whole-word boundary so ordinary words stay untouched.",
   "acceptance_test": "Extend test_outside_ticker_forms with a synthetic ticker in the 8 surviving forms (quote-split, tuple, \\u escapes, letter-spaced, dotted, %XX, &#N;, comma-quoted) and assert each becomes the marker, while 'glmbx', 'xglmb' and 'GLMBs' (synthetic) stay. FINAL-recheck-scrubprobe.py prints ticker_still_whole_word=False and spaced_form_remains=False for every form."},
  {"severity": "minor",
   "title": "evals/finalize_prompt_log.py has no argument handling: --help (or any flag) runs the full 10-minute rebuild into submission/prompt-log/",
   "evidence": "Running `.venv/bin/python evals/finalize_prompt_log.py --help` started the build (`ps -o etime,command` showed the --help command line at 10:36 elapsed with 100% CPU); git status afterwards: 6 tracked files modified and 1 untracked transcript under submission/prompt-log/, 802 files with a fresh mtime. evals/finalize_prompt_log.py:503 `if __name__ == \"__main__\":` calls the build directly; the module docstring shows `python3 evals/finalize_prompt_log.py` as the only usage.",
   "why_it_matters": "The script overwrites the published folder and includes the current session's own transcript. A reviewer or worker who only wants the usage text can rewrite the artifact that is about to be published, and a killed run can leave README/REDACTIONS rewritten but the self-test (step 5) never run.",
   "fix": "Add argparse with --help, and require an explicit flag (for example --build) to write. Exit with usage on any unknown argument.",
   "acceptance_test": "A unit test runs `python3 evals/finalize_prompt_log.py --help` in a temp copy and asserts exit 0, usage text, and no change under submission/prompt-log/."},
  {"severity": "nit",
   "title": "README edit 7 and deploy/SNAPSHOT.md do not mention that the exchange ticker is also masked, or the new rule's limits",
   "evidence": "grep -n -i -E 'ticker|short value|stock' over submission/prompt-log/README.md, REDACTIONS.md, deploy/SNAPSHOT.md and submission/NEEDS_CHRIS.md finds no line describing it; README line 16 lists the forms for the name only. REDACTIONS.md counts the ticker under the existing outside-name class.",
   "why_it_matters": "The README says what edits were made. A reader who sees only the name described will not know that bare, EXCH:TICKER and $TICKER forms are masked too, or that those short values are whole-word matches without the name's split-literal handling.",
   "fix": "Add one sentence to README edit 7 (generated block in evals/finalize_prompt_log.py) and to SNAPSHOT.md: the company's exchange ticker is masked the same way (whole word, bare, EXCH:TICKER and $TICKER), and its escaped or split spellings are not decoded.",
   "acceptance_test": "grep -n -i 'ticker' submission/prompt-log/README.md shows the sentence after a rebuild."}
 ],
 "whats_right": [
  "The ticker is gone next to the marker in the prompt log and the snapshot (0 in every form I tried), and the bio line now holds two adjacent markers with no symbol",
  "One shared regex drives finalize, the tree scan and the snapshot rules, with a unit test for the plain forms and the word-boundary cases (56 tests pass)",
  "Snapshot images, PDFs and video are clean by pixels and text layers, with positive OCR controls that fire"
 ],
 "questions_for_chris": [
  "T-193 is still open: may the published repo name your employer? If yes, flip REDACT_OUTSIDE_PROJECT_NAME and the ticker findings above become moot; if no, the snapshot as built at HEAD is safe on this point.",
  "The working-tree prompt-log folder was partly rewritten by my accidental run (6 modified files, 1 new transcript). Do you want it discarded (restore to HEAD) or committed as a deliberate rebuild?"
 ]}
```
