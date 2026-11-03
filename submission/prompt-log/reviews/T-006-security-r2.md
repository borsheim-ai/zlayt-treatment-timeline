# T-006 security review, round 2 (secrets scanner + git hygiene) — verdict: changes

Both round-1 blockers are fixed and proven in a scratch repo: files with spaces, tabs, newlines, emoji and non-ASCII names are scanned; renames (with appended key), new copies and symlink-to-file type changes are scanned; the file-level allowlist is gone; `ANTHROPIC_API_KEY=<value>` is flagged; the extra providers and env-name variants are caught; `.git/hooks/pre-commit` exists, is executable, matches `tools/install_git_hooks.sh`, and a plain `git commit` with a key staged exits 1 (also from a subdirectory). Repo scan: `check_secrets: ok (179 file(s) scanned)`; 29/29 commits are conventional. No blocker remains.

What is left is about the gate as a whole, not the regexes: the Claude-side scan is blind to files added in the same command, the native hook (the only thing that sees them) is a local untracked file that `--no-verify` skips and no document installs, and the scanner flags the most common config idiom while missing UTF-16 files. Evidence: `artifacts/review-evidence/T-006-r2-*`. Scanner sha at review: `c57a65996b21` (only change during review: `from __future__ import annotations`).

```json
{
 "card": "T-006",
 "persona": "security-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "round 2: 9e759a2 + working tree at HEAD eb78e3b; tools/check_secrets.py, tools/install_git_hooks.sh, .git/hooks/pre-commit, .gitignore, tools/tests/test_secrets.py; git log",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -p no:cacheprovider -> 262 passed (includes test_secrets.py)",
  "python3 tools/check_secrets.py (repo scan) -> check_secrets: ok (179 file(s) scanned); .git/hooks/pre-commit run directly in the real repo -> rc 0 (index empty)",
  "T-006-r2-probe.py in scratch repos (never the real index): 10 odd file names with a key inside, 36 env/credential file names, ~65 value patterns (formats, case, splits, encodings, 1 MB line, 200k lines, NUL/CRLF/U+2028), UTF-16 file, rename+append with spaces, copy, symlink->file type change, gitlink, staged delete, partial staging, git-failure modes (bogus GIT_DIR, GIT_INDEX_FILE, unreadable .git, no git on PATH); output T-006-r2-probe.out.txt",
  "T-006-r2-fp-probe.py: 20 ordinary config/doc lines mentioning ANTHROPIC_API_KEY run through --staged in a scratch repo (T-006-r2-fp-probe.out.txt)",
  "T-006-r2-chain-probe.py: piped 'git add X && git commit ...' variants into git-guard.sh (real index empty) (T-006-r2-chain-probe.out.txt)",
  "copied the real .git/hooks/pre-commit into scratch repos: plain commit with key staged (rc 1), --no-verify (rc 0), commit from a subdirectory (rc 1), -c core.hooksPath=/dev/null (rc 0), clean commit (rc 0)",
  "git log --format=%s checked against the conventional-commit prefix list (0 non-conforming of 29); git check-ignore -v on .env, .env.local, .envrc, id_rsa, x.pem, x.key, a.env, .venv, node_modules, artifacts/tmp, agent-memory-local, *.sqlite3; git ls-files for tracked secret-shaped names (none)",
  "grep for install_git_hooks.sh references outside the card: none in RUNBOOK, CLAUDE.md, CONTRACT or any bootstrap",
  "read check_secrets.py, install_git_hooks.sh, .gitignore, .git/config (no core.hooksPath)"
 ],
 "verdict": "changes",
 "scores": {
  "detection_coverage": 4,
  "gate_coverage": 2,
  "fail_closed_behavior": 3,
  "false_positive_rate": 3,
  "git_hygiene": 5
 },
 "findings": [
  {
   "severity": "major",
   "title": "A key added and committed in one command is never scanned by the Claude-side gate, and `git commit --no-verify` defeats the native hook",
   "evidence": "git_guard.py:226-231 + 343-344 (T-003 code): secret_scan() runs check_secrets --staged against the index AT HOOK TIME, before any `git add` in the same command has executed. T-006-r2-chain-probe.out.txt (index empty): ALLOW \"git add notes.env && git commit -m 'chore: notes'\", ALLOW 'git add config/prod.pem && git commit --no-verify -m x', ALLOW 'git add src/key.py; git commit -m x' (only the explicit .env name check, `git add -f .env.local && git commit`, denies). Native hook: scratch repo, key staged, `git commit --no-verify` -> rc 0, commit created ('log: 4e71441 noverify'); `-c core.hooksPath=/dev/null commit` -> rc 0; `git config core.hooksPath` and `rm .git/hooks/pre-commit` are allowed by git-guard (see T-003 findings).",
   "why_it_matters": "'git add f && git commit -m x' is the most common agent commit shape. In that shape the only effective gate is the native hook, and one flag (`--no-verify`, which agents reach for when a hook blocks a false positive, see the false-positive finding) turns it off. CONTRACT invariant 10 'secrets never enter git' is then enforced by luck. Acceptance criterion 1 (staged key blocked) holds only for the pre-staged case.",
   "fix": "In git-guard: deny `git commit` with --no-verify / -n / `-c core.hooksPath=` and `git config core.hooksPath`; when a command contains a `git add <paths>` followed by commit, run check_secrets over the working-tree contents of those paths (or deny chained add+commit); optionally add `check_secrets.py --paths`.",
   "acceptance_test": "With an empty index and a file containing a key-shaped string on disk, git-guard.sh returns deny for \"git add k.txt && git commit -m x\" and for \"git add k.txt && git commit --no-verify -m x\"; \"git commit --no-verify -m x\" alone returns deny; the same commands with a clean file remain allowed."
  },
  {
   "severity": "major",
   "title": "The native pre-commit hook is untracked, local to this clone, and installed by no documented step",
   "evidence": "`grep -rn install_git_hooks` outside the card: only tools/install_git_hooks.sh itself and board/cards/T-006.md; RUNBOOK.md, CLAUDE.md, docs/CONTRACT.md and the bootstrap steps (CONTRACT 'Step 1..' list) never call it. .git/hooks/pre-commit is outside version control by construction. No CI/E2E step runs `python3 tools/check_secrets.py`. Round-1 major asked for runbook/bootstrap wiring and a CI step; only the script was added.",
   "why_it_matters": "CONTRACT line 27 promises 'a pre-commit check blocks key-shaped strings'. On a fresh clone, a second machine, a worktree with its own hooks dir, or after `git init` in Docker, there is no hook; given the chained-commit finding above, there is then no gate at all. The hook also silently depends on `python3` on PATH.",
   "fix": "Add `sh tools/install_git_hooks.sh` to RUNBOOK 'first run' and the session bootstrap, have `board.py validate` (or the SessionStart hook) warn when .git/hooks/pre-commit is missing/not executable/differs from the script, and add `python3 tools/check_secrets.py` to the E2E/release checklist (M5 gate).",
   "acceptance_test": "grep -n install_git_hooks docs/RUNBOOK.md CLAUDE.md returns a hit; deleting .git/hooks/pre-commit makes `python3 tools/board.py validate` (or the SessionStart output) print a warning; `python3 tools/check_secrets.py` is listed in the release checklist."
  },
  {
   "severity": "minor",
   "title": "Text files containing a NUL byte in the first 8000 bytes are skipped as binary, including UTF-16 files",
   "evidence": "check_secrets.py main(): `if b\"\\0\" in data[:8000]: continue  # binary`. T-006-r2-probe.out.txt: a UTF-16 file containing a sk-ant key -> (0, 'check_secrets: ok (1 file(s) scanned staged)'); 'sk-ant NUL first (looks binary)' MISSED; key after a NUL at byte 7999 MISSED.",
   "why_it_matters": "Windows PowerShell redirection writes UTF-16 by default, and a stray NUL turns any file into 'binary'. The module docstring documents 'split across lines or encoded', not this; a skipped file prints 'ok (N file(s) scanned)' as if scanned.",
   "fix": "Do not skip: scan the bytes with byte-pattern regexes as well as the decoded text, and try utf-16 when a BOM or every-other-NUL pattern is present; report 'skipped as binary: <names>' on stdout.",
   "acceptance_test": "A staged UTF-16 (BOM) file and a UTF-8 file with a leading NUL, each containing a key-shaped string -> check_secrets --staged exits 1."
  },
  {
   "severity": "minor",
   "title": "The scanner reports success when git itself fails",
   "evidence": "check_secrets.py git() returns only stdout and ignores the return code. T-006-r2-probe.out.txt: GIT_DIR=/nonexistent -> 'check_secrets: ok (0 file(s) scanned staged)' rc 0; GIT_INDEX_FILE=/nonexistent/idx -> same; .git chmod 000 -> same. (With no git on PATH it crashes with a traceback, rc 1, which is fail-closed.) A failing `git show :<path>` is also swallowed and the file silently counts as scanned (b'' content).",
   "why_it_matters": "Round-1 fix text said to fail the run if `git show` returns non-zero. Today a broken git (dubious-ownership error, permission problem, locked index) yields a green 'ok' from a security gate.",
   "fix": "Check the return code of every git call and exit 2 with the stderr text; for staged files whose `git show` fails (other than gitlinks, mode 160000), fail; print scanned vs listed counts.",
   "acceptance_test": "With GIT_DIR=/nonexistent, `check_secrets.py --staged` exits non-zero; with a gitlink staged it still exits 0."
  },
  {
   "severity": "minor",
   "title": "False positives on the standard config idiom, with no escape hatch",
   "evidence": "T-006-r2-fp-probe.out.txt BLOCKED: 'ANTHROPIC_API_KEY = os.getenv(\"ANTHROPIC_API_KEY\")', 'ANTHROPIC_API_KEY = os.environ[\"ANTHROPIC_API_KEY\"]', 'ANTHROPIC_API_KEY = <redacted>', 'ANTHROPIC_API_KEY=<redacted> (never commit this)', 'ANTHROPIC_API_KEY=\"sk-ant-...\"', 'ANTHROPIC_API_KEY=<redacted>', 'ANTHROPIC_API_KEY=<redacted>'. Regex (check_secrets.py ANTHROPIC_API_KEY pattern): value is any 6+ non-space characters not starting with <, $, your, changeme, xxx, ..., None, null. The allowlist was removed (correctly) but no per-line marker replaced it.",
   "why_it_matters": "The M2+ app config will contain exactly these lines (CONTRACT: key 'from .env only'). A blocked commit sends agents to --no-verify, which the previous finding shows is not blocked.",
   "fix": "Exclude values beginning with os., settings., getenv, environ, process.env, and the word-list REPLACE/PLACEHOLDER/dummy/fake/test/example; support a `# noqa: secrets` (or `// secrets:ignore`) marker on the same line, with a test that the marker works only for the ANTHROPIC_API_KEY-assignment pattern and never for the prefix patterns (sk-ant-, ghp_, PEM).",
   "acceptance_test": "The seven BLOCKED lines above -> exit 0; 'ANTHROPIC_API_KEY=<redacted>' and a real-shaped sk-ant string -> still exit 1, even with the marker on the latter."
  },
  {
   "severity": "minor",
   "title": "Pattern and file-name gaps remain (case, quoted JSON key, common credential shapes and files)",
   "evidence": "T-006-r2-probe.out.txt MISSED: 'SK-ANT-...' uppercase, 'anthropic_api_key=...' lowercase, lowercase PEM header, '\"ANTHROPIC_API_KEY\": \"<20 chars>\"' (the closing quote before ':' defeats `ANTHROPIC_API_KEY\\s*[=:]`; round 1 only caught it through the sk-ant prefix), 'sk-ant-' + 7 chars, Bearer <36>, 'x-api-key: <42>', 'api_key = <hex32>', AWS secret access key, ASIA temp key, Slack webhook URL, Stripe sk_test_, Twilio SK..., JWT. File names not flagged: 'ENV', '.env ' (trailing space), '.env.', credentials.json, secrets.json, service-account.json, .npmrc, .pypirc, .netrc, .aws/credentials, *.p12, *.jks, id_rsa / server.pem / server.key by name (gitignored, but `git add -f` passes the name check; content check still catches PEM bodies).",
   "why_it_matters": "A public-key deployment repo (Dockerfile, deploy/) will carry tokens that are not Anthropic keys; the Anthropic key itself is covered, which is why this is minor.",
   "fix": "Make patterns case-insensitive where the name is a label (env name, PEM), allow an optional closing quote before the separator, add the missing shapes and file names above.",
   "acceptance_test": "Each MISSED line becomes BLOCKED in T-006-r2-probe.py; the repo scan stays clean."
  }
 ],
 "whats_right": [
  "NUL-separated file names with --diff-filter=ACMRT: spaces, tabs, newlines, emoji and non-ASCII names, renames with an appended key, copies and symlink->file type changes are all blocked, and values are redacted in the output.",
  "The native pre-commit hook works as designed on this clone: plain `git commit` with a staged key exits 1 (also from a subdirectory), and `.gitignore` plus the 29/29 conventional commit log are in good shape.",
  "No allowlist and no self-matching patterns: the scanner scans its own source and tests (repo scan: 179 files, clean)."
 ],
 "questions_for_chris": [
  "Is `git commit --no-verify` ever legitimate for the agents? If not, blocking it in git-guard is the simplest closure of the first finding.",
  "Do you want the hook installed via a tracked hooksPath directory (core.hooksPath=tools/githooks, set by bootstrap) instead of a copy into .git/hooks? It survives clones but is itself bypassable by config, so it still needs the git-guard rule."
 ]
}
```
