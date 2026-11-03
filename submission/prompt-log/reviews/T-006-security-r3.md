# T-006 security review, round 3 (final) — secrets scanner and git hygiene

Verdict: **pass** (no blockers or majors; five minors). Both r2 majors are closed to the D-023 standard. Code: `tools/check_secrets.py` md5 `52ea5094...` (unchanged since e3fbb08), native hook `.git/hooks/pre-commit`.

## What I ran
- Re-ran my r2 scratch-repo probes (`T-006-r2-probe.py` -> `T-006-r3-probe.out.txt`): 80 OK; the r2 misses for JWT, Bearer, AWS secret key and UTF-16 are now caught, the `os.getenv`/`os.environ` false positives are gone, and a failing git (bogus GIT_DIR, unreadable .git) now exits 1 with `BLOCKED (git diff --cached failed ...)` instead of reporting ok.
- `T-006-r2-chain-probe.py` against the live git-guard: `git add notes.env && git commit`, `git add src/key.py; git commit`, `git add -f .env.local && git commit` and `--no-verify` all DENY.
- `T-006-r3-commit-paths-probe.py` (new): in a scratch repo a tracked file modified to contain a key and committed with `git commit -m x f.txt` is blocked by the native hook (rc 1); git-guard alone ALLOWs the same command (finding 1).
- Native hook: `ls -la .git/hooks/pre-commit` = `-rwxr-xr-x`, content `exec python3 "$(git rev-parse --show-toplevel)/tools/check_secrets.py" --staged`; in a scratch repo a plain `git commit` with a staged key returns rc 1 (`check_secrets: BLOCKED / a.txt:1: Anthropic key (value redacted)`), a clean commit rc 0, a commit from a subdirectory rc 1. `docs/RUNBOOK.md:26` and `tools/serve_board.sh:4` install it.
- Real repo: `python3 tools/check_secrets.py` -> `check_secrets: ok (185 file(s) scanned)`. gitleaks is not installed; I replayed the scanner's own patterns over every added line of `git log --all -p -U0` (42 commits): 0 hits, and no `.env`-like filename in history. `.gitignore` has `.env`, `.env.*`, `!.env.example`, `*.env`, `.envrc`, `*.pem`, `*.key`, `id_rsa*`, `*.log`, caches. `pytest tools/tests -q`: 304 passed.

## Findings
1. minor `git commit <path>` (and `--only`/`-o`) commits the working-tree content of a tracked file without staging it first; git-guard's `--staged` scan sees an empty index. The native hook catches it (verified), so the exposure is a clone without the hook installed.
2. minor Nothing verifies the native hook stays installed or current: it is created only when `serve_board.sh` runs and `[ -x .git/hooks/pre-commit ]` is false; `board.py validate` and the session bootstrap do not warn.
3. minor False positives with no escape hatch: `ANTHROPIC_API_KEY = <redacted> `=REPLACE_ME`, `=dummy-key-for-tests`, `="sk-ant-..."` and `sk-ant-... (never commit this)` all block. Agents cannot use `--no-verify` (D-023), so they are stuck.
4. minor Files with a NUL byte in the first 8000 bytes are skipped silently and still counted as scanned (`ok (1 file(s) scanned)`).
5. minor Pattern gaps remain (r2 minor, partly fixed).

```json
{"card": "T-006", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "tools/check_secrets.py, .git/hooks/pre-commit, tools/install_git_hooks.sh, tools/serve_board.sh:4, docs/RUNBOOK.md:26, .gitignore, git-guard commit/stage rules; commit e3fbb08 (check_secrets.py unchanged since); scratch repos under /private/tmp/claude-501/t006-r3*; threat model D-023",
 "exercised": [
  "python3 tools/board.py show T-006 (AC + handoff)",
  "artifacts/review-evidence/T-006-r2-probe.py re-run in a scratch repo (T-006-r3-probe.out.txt): 80 OK lines; diff vs r2: Bearer, AWS secret, JWT, UTF-16 key now blocked; os.environ assignment no longer a false positive; bogus GIT_DIR / unreadable .git now exit 1 with a BLOCKED message",
  "artifacts/review-evidence/T-006-r2-chain-probe.py against the live git-guard (T-006-r3-chain-probe.out.txt): add&&commit, add;commit, add -f .env.local&&commit, --no-verify all DENY",
  "artifacts/review-evidence/T-006-r2-fp-probe.py (T-006-r3-fp-probe.out.txt): 15 of 20 benign lines ok; 5 block (finding 3)",
  "artifacts/review-evidence/T-006-r3-commit-paths-probe.py (new): `git commit -m x f.txt` with a modified tracked file containing a key: git-guard ALLOW x4 spellings, native hook rc 1",
  "ls -la .git/hooks/pre-commit and cat of it; scratch-repo commits with the real hook text: staged key rc 1, clean rc 0, subdir rc 1, --no-verify and core.hooksPath bypass rc 0 (humans only; agents are denied by git-guard)",
  "python3 tools/check_secrets.py on the real repo: ok (185 file(s) scanned); regex replay of the scanner patterns over `git log --all -p -U0` (42 commits): 0 hits; gitleaks not installed (which gitleaks printed nothing)",
  "cat .gitignore; grep for pre-commit / install_git_hooks in docs/RUNBOOK.md, tools/serve_board.sh; .venv/bin/python -m pytest tools/tests -q: 304 passed"
 ],
 "verdict": "pass",
 "scores": {"r2_majors_fixed": 4, "scanner_correctness_and_fail_closed": 4, "native_hook_coverage": 3, "pattern_coverage": 3, "false_positive_handling": 3, "git_hygiene_gitignore_history": 5},
 "findings": [
  {"severity": "minor",
   "title": "git commit <path> is invisible to the Claude-side secret scan",
   "evidence": "T-006-r3-commit-paths-probe.out.txt: 'index clean at hook time: \"\"'; 'git-guard: ALLOW | git commit -m x f.txt', 'ALLOW | git commit -m x -- f.txt', 'ALLOW | git commit --only f.txt -m x', 'ALLOW | git commit -o f.txt -m x'; 'native hook, commit <path>: rc 1 check_secrets: BLOCKED f.txt:1: Anthropic key (value redacted)'. git_guard.py only requires add/commit separation; the scan runs `check_secrets.py --staged` before the command executes.",
   "why_it_matters": "`git commit file -m msg` is a common idiom and is the same hole r2 major 1 described (a key committed with no preceding scan of its content). The native hook is the backstop and works, so a key cannot enter history in a clone that has the hook; the Claude-side layer is blind in every clone.",
   "fix": "In git-guard, for `git commit` with path operands (anything non-flag after the message options, or -o/--only/-i/--include), run check_secrets on the working-tree content of those paths (e.g. `check_secrets.py --paths <p> ...`) before allowing, or deny with 'stage with git add, then commit without paths'.",
   "acceptance_test": "pytest: scratch repo with a modified tracked file containing a runtime-built sk-ant key; the git-guard payload `git commit -m x f.txt` denies; with a clean file it allows."},
  {"severity": "minor",
   "title": "Native pre-commit hook is not checked for presence or drift",
   "evidence": "grep -rn 'install_git_hooks' shows tools/serve_board.sh:4 (`[ -x .git/hooks/pre-commit ] || ./tools/install_git_hooks.sh`) and docs/RUNBOOK.md:26 only; board.py validate (`python3 tools/board.py validate` -> 'ok (28 file(s))') and the SessionStart hook (settings.json: `board.py status --brief`) do not look at .git/hooks. The hook is untracked, per clone, and an existing but stale or edited file is never rewritten.",
   "why_it_matters": "r2 major 2 asked for a warning when the hook is missing or different. Auto-install on server start is a real improvement, but a fresh clone that has not started the board server, or a hook that was edited, commits unscanned without any signal. Rated minor because the hook exists and blocks here and git-guard still scans for agents.",
   "fix": "Have `board.py validate` (or the SessionStart hook) warn when .git/hooks/pre-commit is missing, not executable, or differs from the text emitted by tools/install_git_hooks.sh; or move the hook to a tracked hooks/ dir and set core.hooksPath in the bootstrap.",
   "acceptance_test": "pytest: in a temp clone with no pre-commit hook `board.py validate` prints a WARN naming tools/install_git_hooks.sh; after the installer runs it prints none."},
  {"severity": "minor",
   "title": "False positives on placeholder and settings assignments, with no escape hatch",
   "evidence": "T-006-r3-fp-probe.out.txt: 'BLOCKED | ANTHROPIC_API_KEY = <redacted>', 'BLOCKED | ANTHROPIC_API_KEY=<redacted> (never commit this)', 'BLOCKED | ANTHROPIC_API_KEY=\"sk-ant-...\"', 'BLOCKED | ANTHROPIC_API_KEY=<redacted>', 'BLOCKED | ANTHROPIC_API_KEY=<redacted>'. check_secrets.py: the ANTHROPIC_API_KEY pattern negates only `<|$|your|changeme|xxx|...|None|null|os.|getenv|environ`; there is no `noqa` marker. The `os.getenv`/`os.environ` cases now pass (fixed).",
   "why_it_matters": "README and test-fixture lines of this shape are normal in a repo with a deployed key. D-023 makes `--no-verify` illegitimate for agents, so a blocked doc commit has no sanctioned way through and will be handled by rewording until it passes, or escalated.",
   "fix": "Add settings., config., REPLACE, PLACEHOLDER, dummy, fake, test, example and a literal `sk-ant-...` / `sk-ant-xxx` to the negated prefixes (still flag any sk-ant- followed by 8+ key characters via the first pattern), and honour a same-line `# noqa: secrets` marker for the ANTHROPIC_API_KEY-assignment pattern only, with a test that the marker never suppresses the sk-ant- pattern.",
   "acceptance_test": "pytest: the five lines above pass; `ANTHROPIC_API_KEY=` followed by a runtime-built sk-ant key still blocks even with `# noqa: secrets`."},
  {"severity": "minor",
   "title": "Files with a NUL byte in the first 8000 bytes are skipped silently and counted as scanned",
   "evidence": "check_secrets.py: `elif b\"\\0\" in data[:8000]: continue  # binary`; T-006-r3-probe.out.txt: 'MISSED rc=0 | sk-ant NUL first (looks binary) | check_secrets: ok (1 file(s) scanned staged)' and 'sk-ant after NUL at byte 7999'. UTF-16 files with a BOM are now decoded and blocked (fixed).",
   "why_it_matters": "A key in a text-like file that happens to contain a NUL (a log with a stray byte, a dump) passes, and the 'ok (N file(s) scanned)' line overstates coverage. r2 minor, only the UTF-16 half was addressed.",
   "fix": "Run the byte-pattern regexes (compiled as bytes) over every file regardless of NULs, and print 'skipped: <n> binary file(s)' for anything not text-decoded.",
   "acceptance_test": "pytest: a file `b'\\0' + runtime-built sk-ant key` is reported BLOCKED."},
  {"severity": "minor",
   "title": "Pattern and filename gaps (r2 minor, partly fixed)",
   "evidence": "T-006-r3-probe.out.txt MISSED (plausible forms only): 'env lowercase anthropic_api_key' (`anthropic_api_key=abc123xyz789`), 'JSON key (quoted name)' (`\"ANTHROPIC_API_KEY\": \"qqqq...\"`), 'ANTHROPIC_API_KEY_FOO=value', 'sk-ant uppercase', 'PEM lowercase', 'stripe sk_test', 'ASIA temp key', 'slack webhook', 'api_key= hex32', 'x-api-key 42', filenames 'ENV' and '.env ' (trailing space). Residual per handoff: keys split across lines or encoded (base64, hex, reversed, zero-width, unicode hyphen, concatenation) are not detected; those are accepted under D-023.",
   "why_it_matters": "The only real secret in this project is an Anthropic key, and any value starting with sk-ant- is caught wherever it appears, so exposure is small; the lowercase and quoted-JSON forms are the ordinary ways a non-sk value for this variable gets written.",
   "fix": "Make the ANTHROPIC_API_KEY pattern case-insensitive and allow an optional closing quote before the separator; make ENV_NAME case-insensitive (already) and tolerate a trailing space/dot; leave third-party token shapes out unless the project uses them.",
   "acceptance_test": "pytest: `anthropic_api_key=abc123xyz789` and `\"ANTHROPIC_API_KEY\": \"qqqqqqqqqqqqqqqqqqqq\"` are blocked; `ANTHROPIC_API_KEY = os.getenv(\"ANTHROPIC_API_KEY\")` still passes."}
 ],
 "whats_right": [
  "Scanner fails closed: with a bogus GIT_DIR or unreadable .git it exits 1 with 'BLOCKED (git diff --cached failed ...)', NUL-separated names handle spaces and unicode, and renames, type changes and UTF-16 keys are all caught.",
  "Add-and-commit in one command, --no-verify and -n are denied by git-guard (all four chain probes DENY), and the native pre-commit hook blocks a staged key in a scratch repo (rc 1) including from a subdirectory.",
  "Repo hygiene is clean: scanner ok on 185 tracked files, 0 pattern hits across all 42 commits of history, no env-like file names ever committed, .gitignore covers .env*, keys, pem, logs and caches."
 ],
 "questions_for_chris": []}
```
