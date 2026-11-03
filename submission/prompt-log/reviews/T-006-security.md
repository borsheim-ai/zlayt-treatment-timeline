# T-006 security review (Secrets scanner + git hygiene) — verdict: fail

Deterministic checks: 37 tests pass but none cover the scanner. `.env` is ignored and clean in history (value grepped, 0 hits). `check_secrets.py` itself fails open: files with spaces or non-ASCII names and renamed files are never scanned yet the run reports `ok`. Blockers: 2. Majors: 4. AC3 (tag m0) unmet at review time. Evidence: artifacts/review-evidence/T-006-*.txt.

```json
{
 "card": "T-006",
 "persona": "security-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "commit range e37efb3..fbe5690 (+ working tree state at review): tools/check_secrets.py, .gitignore, git log/tags; contract \u00a71.10, \u00a74.3, \u00a712",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 37 passed (none of them is a check_secrets test: tools/tests has only test_board.py and test_hooks.py)",
  "read tools/check_secrets.py and .gitignore in full",
  "ran `python3 tools/check_secrets.py` (default mode) on the real repo -> ok, 74 files",
  "staged 63 crafted contents/filenames in a scratch git repo via git update-index and ran `check_secrets.py --staged` on each (artifacts/review-evidence/T-006-check-secrets-probe.txt)",
  "rename-plus-edit probe (artifacts/review-evidence/T-006-rename-probe.txt)",
  "git check-ignore -v on .env, .env.local, .env.example, foo/.env and 30 other secret/cache paths; git ls-files for tracked env files; git status --ignored",
  "history: `git log -p --all | grep -c sk-ant` = 4 (CONTRACT/MASTER_PROMPT prose, the check_secrets.py pattern line, one test_hooks.py line that builds the key by concatenation; zero key material). The .env value (not printed) was grepped with -F across `git log -p --all`, all blobs, and the working tree: 0 hits. The value is placeholder-length, so this proves only that this string never entered git.",
  "git tag (empty), git log (conventional-commit subjects), ls .git/hooks (samples only), git config user.email"
 ],
 "verdict": "fail",
 "scores": {
  "scanner_coverage": 2,
  "fail_closed_behavior": 1,
  "gitignore_hygiene": 4,
  "history_cleanliness": 5,
  "acceptance_criteria_met": 2
 },
 "findings": [
  {
   "severity": "blocker",
   "title": "Files whose names contain spaces, tabs or non-ASCII characters are silently never scanned",
   "evidence": "check_secrets.py:25 `git(...).split()` splits on whitespace and git C-quotes non-ASCII/tab names. Probe (artifacts/review-evidence/T-006-check-secrets-probe.txt, 'file/path shapes'): staged `my key.txt`, `caf\u00e9.txt`, `tab<TAB>name.txt`, each containing a full sk-ant-api03-... key -> MISSED rc=0; the same content in `tools/other.py` -> CAUGHT rc=1. `git show :{f}` on the mangled token returns '' (line 34), so no error is raised.",
   "why_it_matters": "\u00a71.10/\u00a74.3: key-shaped strings staged must block the commit. Any file with a space in its name (very common for exports and screenshots) bypasses the gate with a clean 'ok' exit, and the same applies to `.env` files in such paths. The scanner fails open and reports success.",
   "fix": "Use `git diff --cached --name-only -z` / `git ls-files -z` and split on NUL; fail the run (exit 2) if `git show` for any listed path returns a non-zero code; print the count of files scanned vs listed.",
   "acceptance_test": "tools/tests/test_secrets.py: key in `my key.txt` and `caf\u00e9.txt` -> exit 1; `git show` failure -> exit 2."
  },
  {
   "severity": "blocker",
   "title": "Renamed or type-changed files are excluded from --staged, so a key added in a rename commit is not scanned",
   "evidence": "check_secrets.py:25 `--diff-filter=ACM`. Probe artifacts/review-evidence/T-006-rename-probe.txt: `git mv old.txt new.txt` + append sk-ant key + stage -> status `R  old.txt -> new.txt`; `check_secrets: ok (0 file(s) scanned staged)`, rc=0. Control: same key appended in place -> BLOCKED rc=1.",
   "why_it_matters": "Same requirement as above; renames are routine in refactors, and a staged `git mv x .env` also evades the .env-name rule.",
   "fix": "Use `--diff-filter=ACMRT` (and -M off via `--no-renames` so renames appear as A) with -z.",
   "acceptance_test": "Rename+append test above returns exit 1; `git mv config .env` staged returns exit 1."
  },
  {
   "severity": "major",
   "title": "`ANTHROPIC_API_KEY=` is not flagged unless the value starts with `sk-`; CONTRACT \u00a74.3 names that string as a marker",
   "evidence": "check_secrets.py:10 `ANTHROPIC_API_KEY\\s*=\\s*['\\\"]?sk-`. Probe: `ANTHROPIC_API_KEY=<redacted> and the quoted form -> MISSED rc=0. (`ANTHROPIC_API_KEY=<redacted> is CAUGHT; empty `ANTHROPIC_API_KEY=` in .env.example correctly passes.) Related misses: `sk-ant-abcdefg` (7 chars after prefix, below the {8,} floor), upper-case `SK-ANT-`, OpenAI `sk-<48 alnum>`, bare `Authorization: Bearer <36>`.",
   "why_it_matters": "The contract's marker is the assignment, not the value shape. A key written as a non-sk- value (a proxy token, a rotated format, a truncated paste) in an `ANTHROPIC_API_KEY=` line gets through. I label this major rather than blocker because every real Anthropic key starts `sk-ant-` and is caught; the spec text is ambiguous on whether the bare assignment must trip.",
   "fix": "Flag `ANTHROPIC_API_KEY\\s*[:=]\\s*['\\\"]?[^\\s'\\\"$<{]{8,}` (non-empty, not an obvious placeholder/variable reference) and make the sk-ant pattern case-insensitive with {4,}.",
   "acceptance_test": "Probe lines above -> exit 1; `.env.example` with empty value, `ANTHROPIC_API_KEY=${...}` and `os.environ['ANTHROPIC_API_KEY']` -> exit 0."
  },
  {
   "severity": "major",
   "title": "Allowlist exempts three files wholesale, one of which does not exist and one of which contains no patterns",
   "evidence": "check_secrets.py:16 `ALLOW_FILES = {tools/check_secrets.py, tools/tests/test_secrets.py, .claude/hooks/git_guard.py}`; `ls tools/tests` -> test_board.py, test_hooks.py only. Probe: a full sk-ant key staged into each of the three allowlisted paths -> MISSED rc=0. git_guard.py:1-76 contains no key pattern; the file that does (tools/tests/test_hooks.py, line with `\"sk-ant-\" + ...`) is not allowlisted and only passes because the key is built by concatenation.",
   "why_it_matters": "Anyone (or any agent) pasting a real key into the scanner's own files, which agents edit, commits it with a green check. Whole-file exemptions defeat the control for the files most likely to be touched by 'fix the secrets scanner' tasks. Also AC1 has no test: T-006 claims the scanner blocks a staged key but nothing in tools/tests exercises it.",
   "fix": "Remove ALLOW_FILES. Keep fixtures safe by constructing fake keys at runtime (as test_hooks.py does) and, for the pattern definitions, allow only lines that contain a `# noqa: secrets` marker or match a documented dummy value (e.g. sk-ant-DUMMY...). Add tools/tests/test_secrets.py.",
   "acceptance_test": "Real-shaped key in any file including check_secrets.py -> exit 1; the suite still passes with the dummy-marker convention."
  },
  {
   "severity": "major",
   "title": "No native git pre-commit hook; the only gate is a regex on the Claude Bash command string",
   "evidence": "`ls .git/hooks` -> only *.sample files; `git config core.hooksPath` -> empty. Enforcement is git_guard.py:67-71, which T-003 review shows is skipped for `git -c ... commit`, `git --no-pager commit`, quoted `\"git\" commit`, aliases (artifacts/review-evidence/T-003-git-guard-commit-secret-probe.txt).",
   "why_it_matters": "\u00a71.10 says 'a pre-commit check blocks key-shaped strings'. \u00a712 says it runs 'via git-guard.sh', so this is spec-conformant on paper, but with the hook bypassable and no second layer, a `git commit` from a human terminal, an IDE, or any non-Bash tool is wholly unguarded.",
   "fix": "Add tools/install_hooks.sh (or set core.hooksPath to a tracked hooks/ dir) installing a pre-commit that runs `python3 tools/check_secrets.py --staged`; call it from the runbook/bootstrap; add a CI/E2E step running `check_secrets.py` on the tree.",
   "acceptance_test": "In a clean clone after the install step, `git commit` with a staged sk-ant key exits non-zero without any Claude hook involved."
  },
  {
   "severity": "major",
   "title": "AC3 not met at review time: tag m0 does not exist; card has no AC evidence",
   "evidence": "`git tag` -> (empty). Card T-006: status in_progress at first read, all three ac entries `done:false, evidence:null`, handoff empty. Commits are conventional (`chore:`, `feat(harness):`, `docs(spec):`, `chore(orchestrator):`).",
   "why_it_matters": "The card cannot close with an unmet acceptance criterion; the review was requested before the card's own evidence existed, so the verdict is on the code as committed.",
   "fix": "Tag m0 at the M0 gate after the above fixes (`git tag -a m0`), attach evidence to AC1-3.",
   "acceptance_test": "`git tag -l m0` returns m0; `board.py show T-006` shows all AC done with evidence."
  },
  {
   "severity": "minor",
   "title": "Pattern and filename coverage is narrow for a repo that will hold a deployed public key",
   "evidence": "Probe MISSED: `github_pat_...`, Slack `xoxb-`, Google `AIza...`, Stripe `sk_live_`, AWS secret access key line, `-----BEGIN PGP/DSA/ENCRYPTED PRIVATE KEY`, `sk-ant-` split across two lines, `.envrc`, `prod.env`, `config.env`, `.ENV`, `.claude/settings.local.json` with a key under env, base64/hex-encoded key. check_secrets.py:29 name test is case-sensitive and only `.env`/`.env.*`.",
   "why_it_matters": "Lens item 'abuse of a public key': M4 deployment will introduce more credentials (hosting, Space tokens). Cheap to cover now.",
   "fix": "Add the patterns above, make filename test case-insensitive and cover `*.env`, `.envrc`, `*.pem`, `*.key`, `id_rsa*`, `credentials*.json`; scan joined line pairs for the `sk-ant-` prefix split case.",
   "acceptance_test": "Each MISSED probe line returns exit 1."
  },
  {
   "severity": "minor",
   "title": ".gitignore misses common secret-bearing and runtime paths",
   "evidence": "`git check-ignore` -> NOT ignored: .envrc, *.env (config.env, prod.env), *.pem, *.key, id_rsa, credentials.json, .ruff_cache/, .mypy_cache/, .coverage, htmlcov/, *.log, .vscode/, app/db/*.db, board/.state.json (currently untracked in `git status`). Covered correctly: .env, .env.local, .env.production, foo/.env, node_modules/, __pycache__/, .pytest_cache/, .claude/agent-memory-local/, artifacts/tmp/, *.sqlite3; .env.example is un-ignored as intended.",
   "why_it_matters": "AC2 is satisfied for the five named items; the gaps are the next most likely accidental commits.",
   "fix": "Append: .envrc, *.env, *.pem, *.key, id_rsa*, credentials*.json, .ruff_cache/, .mypy_cache/, .coverage, htmlcov/, *.log, .vscode/, .idea/, app/db/*.db; decide whether board/.state.json is tracked or ignored.",
   "acceptance_test": "`git check-ignore -q` succeeds for each listed path."
  }
 ],
 "whats_right": [
  ".env is ignored (`.gitignore:1`), not tracked, and its value appears nowhere in history, blobs or working tree; .env.example is correctly un-ignored",
  "check_secrets never prints the matched value (`value redacted`), scans staged blobs via `git show :path` rather than the working tree, and catches .env/.env.*/sub/.env by name",
  "Commit history uses conventional commit subjects throughout"
 ],
 "questions_for_chris": [
  "Commits are authored as <redacted-private> (git config user.email) while your account email is cborsheim@gmail.com; if the repo is published for Zlayt, is the <redacted-private> address one you want visible in history? (Not rewriting history is a contract rule, so decide before first push.)"
 ]
}
```
