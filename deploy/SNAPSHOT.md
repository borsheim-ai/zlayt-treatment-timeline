# Public snapshot (T-194)

**Publish only from the snapshot this script builds. Never push the working repo or its history.** The working repo's history has
tailnet hostnames and IPs in older commits and 29 commits authored with a work email; HEAD itself also carried them in tracked files
and screenshots (removed or redacted in the snapshot, not in HEAD).

## One-time setup: the local private-patterns file

The scan has to look for private values (the work email and its domain, the tailnet host name, device names), but a tool that spells
them would publish them. So no private value is written anywhere in `deploy/`. They live in a **local, git-ignored file**,
`deploy/.private_patterns` (one `kind<TAB>value` per line; kinds `email`, `device`, `term`; mode 600; never committed):

```bash
python3 deploy/snapshot_tool.py init-patterns .     # derives it from this repo's history and memory/ENVIRONMENT.md; prints counts only
```

If the file is missing, `make_public_snapshot.sh` stops before building anything, exits 2 and says how to create it. The script also
refuses to run if the file is tracked by git. The file is excluded locally through `.git/info/exclude`; the repo's `.gitignore`
(orchestrator-owned) should list it too. The snapshot never contains it (`git archive` only exports tracked files).

## Usage

```bash
bash deploy/make_public_snapshot.sh              # new temp dir outside the repo
SNAPSHOT_DIR=/path/to/new/empty/dir bash deploy/make_public_snapshot.sh
```

What it does (all on a copy; the real repo, its history and its git config are never touched, nothing is pushed, `.env` is not read):

1. `git archive HEAD` into a new empty directory outside the repo (only committed files; uncommitted work is not included).
2. **Image allow-list** (`snapshot_tool.py prune`): the snapshot may carry images and media (png, jpg, gif, webp, svg, pdf, mp4, mov
   and similar, also when renamed, detected by file signature) only under `artifacts/screenshots/guided/`, `artifacts/screenshots/final/`, `artifacts/mockups/`,
   `submission/`, everything under `app/frontend/` (images the app serves, e.g. the validation-ladder SVG on the How page) and the single file `artifacts/demo.webm` (its pixels are not OCR-checked: no ffmpeg; look at it by eye). Every other image is deleted from the snapshot. Reason: a text scan cannot see pixels, and older board screenshots
   rendered the tailnet URL in their header.
2b. **Chris's own words** (`snapshot_tool.py drop-chris`): `board/inbox/` (his board notes) is deleted from the snapshot and the text of his `inbox` events in
   `board/activity.jsonl` is replaced; `MASTER_PROMPT.md`, the one thing of his own words he authorized, must still be present (the script stops otherwise).
   The redaction step below also replaces any run of 8+ words copied verbatim from one of his messages (read at run time from the local Claude Code
   transcripts, minus the wording that is in `MASTER_PROMPT.md`), and the scans fail if either survives.
3. **Redaction** (`snapshot_tool.py redact`) of every text file: secret patterns from the snapshot's own `tools/check_secrets.py`; the
   generic tailnet shapes (a `tail`+hex label, the tailnet suffix, any <redacted-private>/10 address, in plain, backslash-escaped,
   bracketed-dot, percent-encoded and spelled-out-dot forms); and every value from the local patterns file. Private values become
   `<redacted-private>` and device names become `<device>`. Backslash-escaped spellings (`host\.name`) are caught by running the same
   rules over a backslash-stripped copy and mapping the match back onto the original text. One documentation address, the `<redacted-private>`
   peer in the D-036 test, is exempt in both the redaction and the scan so that test still exercises the tailnet-peer case.
   **Full finalize rule set (T-199, D-070).** `snapshot_tool.py` imports `evals/finalize_prompt_log.py` and calls its `scrub()` on every
   text file, so the snapshot and the prompt log share one rule set, one set of markers and one switch: private terms (work email,
   tailnet host, device names, third-party name, personal job-application names, the outside project name) matched on a normalized
   view, home paths, personal file paths and the generic network shapes. Those terms live only in the git-ignored patterns file:
   kinds `email|device|term` (written by `init-patterns`) and `#@third|outside|personal<TAB>value` lines (entered by hand, kept by
   `init-patterns` when it rewrites the file). With `REDACT_OUTSIDE_PROJECT_NAME` on (the default until Chris answers T-193) the
   `#@outside` line is REQUIRED: no repo data names that project, so it cannot be derived, and without the line `redact` and `scan`
   exit 2 instead of silently publishing the name. Setting that one switch to False in `evals/finalize_prompt_log.py` lets the name
   through in both the prompt log and the snapshot.
4. `git init` and exactly one commit, author and committer `Chris Borsheim <cborsheim@gmail.com>`. The user, system and hook config
   are ignored for that commit (`GIT_CONFIG_GLOBAL=/dev/null`, `core.hooksPath=/dev/null`); no remote is added.
5. `snapshot_tool.py scan`: an independent strict scan of every file's text, its backslash-stripped form, binary files (as latin-1) and
   file names, with the same generic shapes plus the local patterns. It also matches every private term on a **normalized view** of each file (quotes, backticks, `+`, whitespace and backslashes removed, case folded, one-letter wildcards for terms of 8+ characters), so a value split as `'abc' + 'def'` fails the build. `deploy/test_snapshot_tool.py` plants such fragments (synthetic terms) and proves it. It **fails** on any image outside the allow-list, and runs
   `tesseract` over every allow-listed raster image (a hit in the rendered text fails; if `tesseract` is not installed it prints a
   WARNING that those images were not checked, and then each one must be looked at by eye). It also checks the tree matches the
   commit, that there is 1 commit and that every author and committer is the gmail address.
6. `python3 tools/check_secrets.py` run inside the snapshot.

It prints `SNAPSHOT_PATH=<dir>` and exits 0 only if every check passes. On any failure it exits 1, prints `file: category (line)`
(never the value) and keeps the directory with a "do NOT publish" message. Run time is about 80 s.

To publish: `cd <SNAPSHOT_PATH> && git remote add origin <url> && git push -u origin main` (done by Chris, not by the script).

## Edits the snapshot makes to tracked files (HEAD is unchanged)

Redaction also rewrites code that spells the patterns. In the run recorded below these are `evals/finalize_prompt_log.py`,
`tools/board_server.py` and `tools/export_prompt_log.py` (the tailnet-suffix regexes and the default allowed-host list become
`<redacted-private>` / `<device>`). They still parse, but in the snapshot the exporter's private-network regex and the board server's
default tailnet host are not functional; re-run the exporter only from the working repo. The script prints the list of rewritten
`.py` files on every run. Binary files are scanned but not rewritten. A value that is compressed (zip/docx/xlsx) or base64-encoded
would not be seen; the tree has no such file.

## Run recorded for T-194 round 2 (source HEAD 5fa0a75)

```
1/6 git archive HEAD (5fa0a75)
2/6 prune: removed 185 image/media file(s) not on the allow-list; kept 17 allow-listed (16 raster, all under artifacts/screenshots/guided/)
3/6 redact: 129 replacement(s) in 30 file(s); 16 binary/utf-16 file(s) not rewritten (device name: 120; tailnet host / IP / private
      literal: 9; rewritten code: evals/finalize_prompt_log.py, tools/board_server.py, tools/export_prompt_log.py)
4/6 git init + one commit as Chris Borsheim <cborsheim@gmail.com>
5/6 scan: 3429 file(s) checked against 9 pattern(s) (3 generic + 6 private) + the image allow-list; 16 allow-listed raster image(s)
      OCR-checked; scan: ok (0 hits); history: 1 commit, author and committer Chris Borsheim <cborsheim@gmail.com>; remotes: 0
6/6 check_secrets: ok (3429 file(s) scanned)                                                 -> exit 0
```

Negative tests, each exits 1 with the right hit: a text file with the work email written as `local[.]part@domain[.]tld`; the same
with doubled backslashes before the dots; a device name; a PNG outside the allow-list and a PNG renamed to `.txt`; an allow-listed PNG
that renders a `tail`+hex tailnet URL (found by OCR). `<redacted-private>` and the CIDR text `<redacted-private>/10` are not hits. The missing
patterns file case exits 2 with an explanation and builds nothing. `deploy/` itself scans clean against the patterns file.

## `make test` on a clone of the snapshot (source HEAD 5fa0a75)

`git clone <snapshot> x && cd x && make test`: **3 failed, 5827 passed, 3 skipped in 370 s, exit 2.** The README says exit 0 means
all passed; that is **not true for the public clone yet.** The three tests need history that a one-commit repo does not have:

- `tests/unit/test_eval_runner.py::test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head`
- `tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit`
- `tests/unit/test_t113_heldout_audit.py::test_no_committed_held_out_control_was_written_with_the_prompt_or_names_its_words`

They check provenance against commits of the private working history (the calibration's `source_commit`, and which commit wrote each
held-out control). The tests dir belongs to QA: a card note on T-194 asks QA to mark them as needing git history and skip with a stated
reason when the repo has a single commit. Until QA does, treat these 3 as expected failures of the public snapshot; everything else
passes. Provenance claims that cite commits refer to the private working history.

## Known limits and follow-ups

- Home paths such as `<home-path>` and the content reached through them (T-187 r2 major 2, T-193) are not touched by this script;
  that is a separate decision for Chris.
- Screenshots outside the allow-list are dropped from the snapshot, so documents that link to them have dead image links there. Re-take
  board screenshots on localhost and save them under `artifacts/screenshots/guided/` or `artifacts/mockups/` to publish them.
- The NEEDS_CHRIS "publish only from this snapshot" item is writer-owned (T-195); T-194 AC 1 is not complete until it lands.
