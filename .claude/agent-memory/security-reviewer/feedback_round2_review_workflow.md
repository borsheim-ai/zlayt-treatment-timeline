---
name: round2-review-workflow
description: Workflow gotchas for round-2 re-reviews (HEAD moves several times per review, pin with git archive, reviewer-write-guard makes the first Write final, board-guard flags > in strings, probes must restore patched socket/SDK functions)
metadata:
  type: feedback
---

Round-2 re-reviews of a card: pin the commit you actually tested. Other agents commit to the same repo during a review. T-034 r2: b1803c0 -> 250e7b6. T-040 r2: 7a450a1 -> 5650eae -> 099732b -> 996f9b4 -> 037cc89. T-053 r2 (2026-11-02): 02f9939 -> dbb2c66 -> 20d866f -> 709397e -> f5444a8 -> e83eb54 -> d796383 -> d0c9cdb -> bee1844, six moves in about 25 minutes. Pin with `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-r2/head_<sha>` and run pytest there with `-p no:cacheprovider`, so the venv is the project one (`/Users/arsis/zlayt-pm-project/.venv/bin/python`) and the copy is the only code on the path. Quote the pinned sha and `git rev-parse --short HEAD` in the same call. Before finishing, check `git diff --quiet <pinned> HEAD -- <gate files>`; if the gate files moved, say so in the review.

The git archive pin has no `.git` and no `.venv`, so `git` and `tools/check_secrets.py` must run on the main repo, and the probes must `chdir` into the archive and put it at `sys.path[0]`. A commit can also fail to import on its own: 02f9939 imports `case_extras` before the module exists (added in dbb2c66). Check collection errors before reading any count.

The reviewer-write-guard makes the first Write to `reviews/<card>-<persona>.md` final: a later Edit to fix a count or a label is denied ("reviews are append-only; write a new file"). Proofread the JSON and every number before the first Write. Confirm numbers with a query or a grep first; I had to leave one wrong count in T-053 r2 for this reason.

The live server on :7860 can predate HEAD. Probes against it are not evidence for HEAD. Other agents also kill listeners between calls, so start probe servers with `subprocess.Popen` inside one Python run and stop them in a `finally`. Check `lsof -iTCP:<port> -sTCP:LISTEN` first, and do not use `timeout` (not installed on macOS). Use `lsof -ti tcp:<port> | xargs kill` for manual cleanup. One Bash call was killed with exit 144 mid-probe; rerun it rather than reading partial output.

The git-guard PreToolUse hook rejects `$(...)` in an echo or similar command position. The board-guard hook reads `>` inside quoted strings as a redirect; `curl -w "... -> %{http_code}"` was blocked. Keep arrows and `>` out of shell strings and put probes in files under artifacts/review-evidence/ (Write tool, then `.venv/bin/python -I <file>`).

Probe gotchas (T-053 r2): (1) do not re-capture a module attribute after patching it, because the module-level `_orig = socket.create_connection` ran after the patch and captured the stub, so every local HTTP call was blocked; capture originals once, before any patch. (2) Patching `subprocess.run` globally breaks the probe's own subprocess calls; save and restore it in a `try/finally`. (3) A UDP `connect()` to 192.0.2.1 picks the outbound interface address without sending a packet, which gives a LAN address for a non-loopback check.

T-055/T-058 (2026-11-01, HEAD moved d796383 -> 08764e7 within an hour): `git archive HEAD` lacks the untracked LLM fixtures the sample case needs, so pinned tests fail unless `tests/fixtures` is copied from the working tree (record that in the review). git-guard blocks `rm` with a variable path ("unresolved expansion"); use literal paths. `timeout` is not installed on macOS. `which gitleaks` returns rc=1 (not installed). pip-audit can be installed into a scratchpad venv (`python3 -m venv <scratch>/pa && <scratch>/pa/bin/pip install pip-audit`) and run with `--no-deps --disable-pip` on a fully pinned requirements file, without touching `.venv`.

T-053 r3 (2026-11-01): HEAD was 08764e7 at the first check, 8ec0b25 at the pin, 38421cc at write time (docs and memory only; gate files unchanged). Pin the commit you test, then re-check drift at write time. Brief says `python3 -m pytest`, but system python3 has no pytest: use `.venv/bin/python -m pytest -p no:cacheprovider`, and do not pipe pytest into tail when you need the exit code (the pipe hides it). After the first Write, a self-found error (I cited api.py:103 for live_enabled, which is at :113) was fixed by appending a correction after the JSON block, not by Edit, because reviews are append-only. Proofread line refs with grep before the first Write, not after.

Persona scope: if a brief asks security-reviewer to write a record under another persona's name, do not write it. Report the facts and say that persona needs its own run.

**Why:** T-034 r2 (first `$()` echo blocked, HEAD changed between pytest and grep). T-040 r2 (four HEAD moves, a live server that predated HEAD, a dirty tree producing a flaky result). T-053 r2 (six HEAD moves, an append-only review file with one wrong count, and a probe bug that made every local request look blocked).
**How to apply:** at the start of each round-2 review, record the HEAD sha and the server start time, pin an archive, probe through a file, and proofread the review before the first Write.
