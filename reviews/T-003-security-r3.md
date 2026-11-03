# T-003 security review, round 3 (final) — hooks and .claude/settings.json

Verdict: **changes** (no blockers; two majors). Graded against D-023 (accidents and lazy evasion; deliberate obfuscation is residual).

Code under test: commit e3fbb08 plus a later uncommitted working-tree edit (one added line in `git_guard.py`, one changed line in `board_guard.py`). The probe results were identical before and after that edit. md5 at review end: git_guard.py `dd4568a8...`, board_guard.py `cecfed4a...`, reviewer_write_guard.py `f64320be...`, check_secrets.py `52ea5094...`. `.git/hooks/pre-commit` exists, is executable and blocks (see T-006 r3).

## What I ran (all with `cwd` in the JSON, nothing destructive executed)
- Replayed the r2 corpus (538 commands) through `git-guard.sh`. r2: 285 DENY / 253 ALLOW. r3: 345 DENY / 193 ALLOW. Of 63 commands that moved ALLOW to DENY, none are false positives; 3 moved DENY to ALLOW (finding 3). Per category (DENY/ALLOW): separators 18/1, aliases/config 7/1, xargs/dynamic 24/18, exec wrappers 28/12, IFS 0/9 (residual, D-023), push 21/7, reset/clean/checkout 114/60, rm/mv 132/85. Output: `artifacts/review-evidence/T-003-r3-probe-corpus.out.txt`.
- Re-ran my r2 direct probes (git 45 DENY / 24 ALLOW vs 9/60 in r2; reviewer board-guard 81/64 vs 76/69; board2 set 37/29 vs 21/45). Both r2 blockers are fixed: newline, CR and backslash-newline now separate commands (10/10 deny), and `HEAD:+main`, `+main`, `HEAD:+refs/heads/main` are denied.
- New targeted sets (`T-003-r3-probe-targeted.py`, `-targeted2.py`, `-legit.py`, `-rwg.py`): about 330 plausible spellings plus 61 legitimate commands. Legitimate-command regression: multi-line python heredocs (quoted and unquoted tag, quotes inside), `git log/diff/show/blame`, `board.py note` with quotes and newlines, commit messages with quotes and `$(cat <<'EOF')`, `rm board/STOP`, `rm -f board/.locks/*`, for/if/while loops all ALLOW; 5 of 61 wrongly denied (finding 6).
- reviewer-write-guard: 29 crafted payloads; crash simulation with each guard's python replaced by `exit 1` (all three wrappers deny). Ran `.venv/bin/python -m pytest tools/tests -q`: 304 passed (handoff says 307).

## Findings (summary; full evidence in JSON)
1. **major** `git add` of a computed or glob-broad path set passes: `git add ./*`, `git add .*`, `git add $(git diff --name-only)`, ``git add `git ls-files -m` ``, `git ls-files -m | xargs git add`. These are the lazy spelling of `-A`/`-u`, and the handoff does not list them as residual.
2. **major** Reviewer redirect detection is token-based and misses `echo x>app/x` and `python3 t.py>app/out.txt` (no space), `echo x >& app/x` (the handoff says `>&` is handled) and `echo x >| app/x` (denied in r2, allowed now: shlex splits `|` as a separator).
3. minor Regression: the wrapper option table is global, so `sudo -n/-E`, `command -p` and `time -p` swallow `git` (all DENY in r2, ALLOW now).
4. minor `.claude/settings.json`, `.claude/` and `tools/check_secrets.py` are removable (`rm -rf .claude` is allowed); deleting settings.json disables every hook.
5. minor History-moving commands are still allowed: `checkout -B`, `switch -C`, `branch -m`, `reset origin/main`, `symbolic-ref`, `fetch -f`, `pull --force`, `read-tree --reset`. D-023 relies on append-only history.
6. minor False positives on legitimate work (full list in JSON); one was hit live during this review (`git config --get core.hooksPath`).
7. minor reviewer-write-guard still allows when `tool_input` has no path or an unknown key.
8. minor Reviewer write spellings not in the handoff's residual list pass (`unlink`, `shred`, `chown`, `git archive -o`, `git bundle`, `git format-patch -o`, `find -exec touch`, `xargs touch/rm`, `awk print >`, `ruby -i`, `ex`).
9. minor `$PWD` expands to the hook process's cwd, not the payload `cwd`.
10. minor `board/.hook_input_keys.log` is appended on every Bash call and is unbounded (676 KB now).
11. nit Docstring cites LESSONS.md for residual risk (D-023 holds it); handoff test count 307 vs 304.

```json
{"card": "T-003", "persona": "security-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git diff 9e759a2..e3fbb08 -- .claude tools plus working tree at review time (uncommitted: git_guard.py +1 line expand_vars in analyse(), board_guard.py 1 line); hooks run via .claude/hooks/*.sh with crafted JSON on stdin; threat model D-023; sample case n/a",
 "exercised": [
  "python3 tools/board.py show T-003 / show T-006; git status/diff e3fbb08 (hooks + check_secrets drift check, md5 stamped)",
  "artifacts/review-evidence/T-003-r3-probe-corpus.py: r2 corpus of 538 commands through git-guard.sh: 345 DENY / 193 ALLOW (r2: 285/253); 63 ALLOW->DENY, 3 DENY->ALLOW",
  "artifacts/review-evidence/T-003-r2-probe-direct.py re-run (out: T-003-r3-probe-direct.out.txt): git 45 DENY/24 ALLOW (r2 9/60), reviewer board-guard 81/64 (r2 76/69), malformed-input matrix for git-guard and board-guard",
  "artifacts/review-evidence/T-003-r2-probe-board2.py re-run: 37 DENY / 29 ALLOW (r2 21/45)",
  "T-003-r3-probe-targeted.py (git-guard main session 99 deny / 7 pass of 106 deny-expected, 1 'FP' of 62 allow-expected which was my own test bug: backticks inside double quotes really execute; reviewer board-guard 24/3 of 27, 8 FP of 45), T-003-r3-probe-targeted2.py, T-003-r3-probe-legit.py (61 legitimate commands, 5 wrongly denied), T-003-r3-probe-rwg.py (29 reviewer-write-guard payloads + crash simulation of all three wrappers)",
  "python3 -m pytest tools/tests -q via .venv/bin/python: 304 passed",
  "read .claude/hooks/git_guard.py, board_guard.py, reviewer_write_guard.py, _common.py, teammate_idle.py, git-guard.sh, .claude/settings.json hooks block",
  "ls -la .git/hooks/pre-commit and scratch-repo commit (see T-006 review); board/.hook_input_keys.log size check; live hook misfire observed on 'git config --get core.hooksPath'"
 ],
 "verdict": "changes",
 "scores": {"r2_blockers_fixed": 5, "command_position_and_separators": 4, "dynamic_arguments_and_globs": 2, "rm_mv_find_protection": 3, "reviewer_write_enforcement": 3, "fail_closed_behaviour": 5, "false_positive_rate": 3, "threat_model_alignment_and_docs": 3},
 "findings": [
  {"severity": "major",
   "title": "git add of a computed or glob-broad path set passes: ./*, .*, $(...), backticks, xargs",
   "evidence": "T-003-r3-probe-targeted.out.txt: 'ALLOW | add ./*  <-- PASSES', 'add .*', 'add $(ls)'. T-003-r3-probe-targeted2.out.txt: ALLOW for `git add $(git diff --name-only)`, ``git add `git ls-files -m` ``, `git ls-files -m | xargs git add`, `git diff --name-only | xargs git add`, `git status -s | awk '{print $2}' | xargs git add`, `git add -- $(git ls-files -o --exclude-standard)`. git_guard.py broad() (line ~165) matches only '.', './', '*', ':/', '(./)+.?', so './*' and '.*' are not covered; no rule looks at '$'/backtick/glob operands for add. Handoff lists only rm/rmdir/unlink as denying $(...) and does not list these as residual.",
   "why_it_matters": "'git add ./*', '.*' and 'git add $(git diff --name-only)' are the lazy spelling of the denied 'git add -A / -u / .': they stage every agent's in-flight files, which is the exact accident the 'explicit paths you own' rule exists to stop. Under D-023 a plausible accidental spelling that passes is a bug at full severity. (Rated major, not blocker: AC3 holds for every spelling of -A/--all/. and '*'; these forms stage a computed set and still go through the secret scan.)",
   "fix": "In check_git for add (and for xargs-fed add): deny any operand that still contains '$', a backtick, or an unescaped glob '* ? [' whose parent directory is '.', the root, or empty; treat './*', '.*', './.*', '..' and '~+' like '*'. When a segment is 'xargs git add' (or xargs with a wrapper that resolves to git add) deny unless the previous stage is a literal echo/printf of paths. Add the tests below to test_git_guard.py.",
   "acceptance_test": "pytest: for cmd in ['git add ./*','git add .*','git add $(git diff --name-only)','git add `git ls-files -m`','git ls-files -m | xargs git add','git diff --name-only | xargs git add'] git-guard denies; 'git add tools/*.py' and 'git add tools/board.py reviews/x.md' still allow."},
  {"severity": "major",
   "title": "Reviewer shell-write guard misses no-space redirects, >& and >| (handoff claims >& is handled; >| regressed)",
   "evidence": "board_guard.py redirect loop matches whole tokens with re.fullmatch(r\"(?:\\d|&)?>>?&?\\|?(.*)\", t). Probes (REV identity, T-003-r3-probe-targeted2.out.txt): 'ALLOW | redir no space x>file' = `echo x>app/x`; 'ALLOW | redir cmd>file' = `python3 t.py>app/out.txt`; 'ALLOW | redir >&' = `echo x >& app/x`; 'ALLOW | redir >|' = `echo x >| app/x`. In r2 (T-003-r2-probe-direct.out2.txt line 142) `echo x >| app/x` was DENY; shlex punctuation_chars now splits the '|' so the redirect has no target. Same file: `echo x >app/x`, `ls 2>app/x`, `echo x &> app/x` are DENY. Handoff: 'Reviewer guard: per-segment redirects with cd tracking, >&, ...'.",
   "why_it_matters": "'cmd>file' without spaces is an ordinary way to type a redirect, and a reviewer (read-only on product code) writing app/ files by accident is exactly what this guard exists to stop; >| is a regression from r2 and >& is claimed as handled in the handoff but is not. Plausible accidental spelling, so full severity under D-023.",
   "fix": "Find redirects with a regex over the quote-stripped segment text (e.g. r'(?<![<>\\w])(\\d|&)?>{1,2}[&|]?\\s*([^\\s;&|<>()]+)') instead of whole-token matching, applied before shlex splitting on '|' and '&'; handle '>&' and '>|' explicitly and ignore '2>&1', '&>/dev/null' and targets that are fd numbers.",
   "acceptance_test": "pytest with a reviewer identity: 'echo x>app/x', 'python3 t.py>app/out.txt', 'echo x >& app/x', 'echo x >| app/x', 'echo x &>> app/x' are denied; 'ls > /dev/null 2>&1', 'echo x>reviews/a.md', 'echo x>/tmp/a' and 'cmd 2>&1 | tee artifacts/review-evidence/a' are allowed."},
  {"severity": "minor",
   "title": "Regression: the global wrapper option table swallows git after sudo -n/-E, command -p, time -p",
   "evidence": "git_guard.py WRAPPER_OPTS_WITH_ARG = {'-u','-n','-s','-g','-k','-C','-p','-I','-L','-P','-E',...} is applied to every wrapper in strip_wrappers(). T-003-r3-probe-corpus.out.txt 'DENY->ALLOW': 'sudo -E git add -A', 'command -p git add -A', 'time -p git add -A' (all DENY in r2); T-003-r3-probe-targeted.out.txt: 'sudo -n', 'sudo -E', 'command -p', 'time -p' all '<-- PASSES'. `nice -n 5`, `env -u X`, `sudo -u root`, `timeout -s KILL 5` do deny.",
   "why_it_matters": "A fix for option-with-argument wrappers (r2 major) introduced new false negatives for flag-only options of the same wrappers. These are unlikely accidents (nobody types sudo before git add), hence minor, but it is a regression that the tests did not catch.",
   "fix": "Make the table per wrapper: sudo {-u,-g,-C,-h,-p,-r,-t,-U}, env {-u,-C,-S}, nice {-n}, timeout {-s,-k}, xargs {-I,-n,-P,-L,-s,-d,-E}, time {} (-p takes no argument), command {} (-p/-v/-V take none), exec {-a}.",
   "acceptance_test": "pytest: 'sudo -n git add -A', 'sudo -E git add -A', 'command -p git add -A', 'time -p git add -A', 'xargs -p git add -A' deny along with the existing nice/env/sudo -u/timeout cases."},
  {"severity": "minor",
   "title": "Harness control files outside .claude/hooks are removable: .claude/settings.json, .claude/, tools/check_secrets.py, tools/",
   "evidence": "T-003-r3-probe-targeted.out.txt (informational): 'ALLOW | rm settings.json' = `rm .claude/settings.json`, 'ALLOW | rm -rf .claude', 'ALLOW | rm check_secrets' = `rm tools/check_secrets.py`; corpus: 'rm -rf tools' ALLOW, 'find -delete' (no operand) ALLOW, 'git mv .git x' ALLOW. PROTECTED_TREES in git_guard.py = .git, board, memory, reviews, .claude/hooks.",
   "why_it_matters": "Removing settings.json switches off every hook and removing check_secrets.py makes the native pre-commit hook fail. r2 asked for .claude/settings.json and the scanner to be protected; only .claude/hooks was added. Low accident probability, hence minor.",
   "fix": "Add ROOT/.claude/settings.json, ROOT/.claude (itself), ROOT/tools/check_secrets.py and ROOT/tools to the rm/mv/find protection (not to the write protection); deny 'find' with -delete and no start operand.",
   "acceptance_test": "pytest: 'rm .claude/settings.json', 'rm -rf .claude', 'rm tools/check_secrets.py', 'rm -rf tools', 'mv .claude x' deny; 'rm tools/__pycache__/x.pyc' allows."},
  {"severity": "minor",
   "title": "History-moving and ref-moving git commands are still allowed although D-023 depends on append-only history",
   "evidence": "T-003-r3-probe-corpus.out.txt still ALLOW: 'git checkout -B main HEAD~3', 'git branch -m main old', 'git symbolic-ref HEAD refs/heads/x', 'git reset origin/main', 'git reset main', 'git fetch -f origin +refs/heads/*:refs/heads/*', 'git pull --force', 'git pull -f', 'git read-tree --reset -u HEAD', 'git checkout-index -a -f'. 'git tag -f' and 'git branch -f' now deny (handoff). Handoff residual list does not mention these.",
   "why_it_matters": "D-023 says history is covered by detection because it is append-only; `checkout -B main HEAD~3` and `reset origin/main` move the branch backwards and `pull -f` / `fetch -f` overwrite local refs without any of the denied flags. r2 minor, unchanged.",
   "fix": "Deny checkout/switch with -B/-C, branch -m/-M on an existing branch, symbolic-ref, update-index --assume-unchanged, read-tree --reset, checkout-index -f, fetch/pull with -f/--force or a '+' refspec; for 'git reset <rev>' deny unless the rev is HEAD with a path operand.",
   "acceptance_test": "pytest: the ten commands above deny; 'git checkout -b x', 'git checkout main', 'git pull --ff-only', 'git fetch origin' allow."},
  {"severity": "minor",
   "title": "False positives on legitimate work (friction; one hit live during this review)",
   "evidence": "T-003-r3-probe-legit.out.txt (git-guard, main session): DENY for `find . -name '*.pyc' -delete`, `find . -name __pycache__ -type d -prune -exec rm -rf {} +` (find under ROOT counts as protected), `mv reviews/a.md reviews/b.md`, `git reset HEAD tools/board.py` (classic unstage idiom; message suggests `git reset -- <path>`), `git config --get core.hooksPath` (read-only; denied by the config rule; hit live: 'PreToolUse:Bash hook error: git-guard: setting git aliases/core command hooks is blocked'). T-003-r3-probe-targeted2.out.txt: `git commit -m \"fix: bash -c 'git add -A' is analysed\"`, `board.py note T-003 'xargs git add -A is denied now'` and `board.py note ... \"verified bash -c 'git add -A' denied\"` DENY (quoted-string pass triggered by the words bash/xargs). board-guard (reviewer): `git branch --list`, `git branch`, `git branch --show-current`, `git tag -l`, `git stash list/show`, `git worktree list`, `git init /private/tmp/.../r1`, `grep -rln 'git add' docs | xargs wc -l`, `echo \"bash -c 'git add -A' is bypassed\" > reviews/x.md`, and macOS `sed -i '' 's/a/b/' /private/tmp/.../cs.py` (empty suffix argument is taken as the script, so the real script becomes a 'file') DENY.",
   "why_it_matters": "Each is a safe, ordinary command. The guards fail toward deny, so the cost is friction and workarounds, not exposure, but the reviewer ones are the same r2 minor that was only partly fixed.",
   "fix": "Allow read-only forms (config --get/--list, branch with no args or --list/--show-current/-a/-v, tag -l/--list, stash list/show, worktree list); apply the quoted-string heuristic only to quoted strings that are the argument of sh -c / eval / bash -c, not to any quote in a command that merely contains the word; let find under ROOT with -name/-type/-prune and -delete/-exec rm pass unless the start path is a protected tree or ROOT with no -name/-path filter; skip the empty-string argument after sed -i; allow `git reset HEAD -- <path>` and `git reset HEAD <file>` when every operand after HEAD is an existing path.",
   "acceptance_test": "pytest: the listed commands allow; `rm -rf board`, `find board -delete`, `git reset HEAD~1`, `git reset --hard` still deny."},
  {"severity": "minor",
   "title": "reviewer-write-guard still allows an Edit|Write payload that has no recognised path",
   "evidence": "reviewer_write_guard.py: `path = ti.get('file_path') or ti.get('notebook_path') or ti.get('path'); if not path: return 0`. T-003-r3-probe-rwg.out.txt: 'ALLOW | malformed: tool_input null <-- PASSES', 'ALLOW | malformed: tool_input missing path <-- PASSES', 'ALLOW | alt key filePath (camel) <-- PASSES', 'ALLOW | alt key file <-- PASSES'. Non-JSON, arrays, tool_input as string, non-string paths all deny; crash simulation denies for all three wrappers.",
   "why_it_matters": "r2 minor: the guard fails open on an unknown key. The current key names are right, so this only matters if the host renames the field, but a write guard should fail closed.",
   "fix": "If tool_name is Edit, Write, MultiEdit or NotebookEdit and no path key is found, deny.",
   "acceptance_test": "pytest: {'tool_name':'Write','tool_input':{'content':'x'}} and {'tool_name':'Write','tool_input':null} deny; {'tool_name':'Read','tool_input':{}} allows."},
  {"severity": "minor",
   "title": "Reviewer write spellings not in the residual list still pass",
   "evidence": "T-003-r3-probe-targeted2.out.txt (reviewer identity) ALLOW: `unlink app/x`, `shred -u app/x`, `chown arsis app/x`, `git archive -o app/x.tar HEAD`, `git bundle create app/x HEAD`, `git format-patch -o app HEAD~1`, `find . -fprint app/x`, `find app -exec touch {} +`, `echo app/x | xargs touch`, `ls app | xargs rm`, `awk 'BEGIN{print 1 > \"app/x\"}'`, `ruby -i -pe 1 app/x`, `ex -sc '%s/a/b/|x' tools/board.py`. WRITE_CMDS in board_guard.py = cp mv install ln touch mkdir rm rmdir chmod truncate tee rsync. D-023 residual list names only IFS, brace expansion, copies of board.py, interpreter one-liners.",
   "why_it_matters": "Not all are deliberate obfuscation (`unlink`, `shred`, `git format-patch -o`, `git archive -o` are the same class as the denied `curl -o`/`git diff --output`); the rest should be written down as residual so the next reviewer does not rediscover them.",
   "fix": "Add unlink, shred, chown, chgrp, git archive/bundle/format-patch -o/--output to the checked set; list find -exec/-fprint, xargs-fed writers, awk/ex/ruby in the D-023 residual list.",
   "acceptance_test": "pytest with reviewer identity: `unlink app/x`, `shred -u app/x`, `git archive -o app/x.tar HEAD`, `git format-patch -o app HEAD~1` deny; the same targets under artifacts/review-evidence allow."},
  {"severity": "minor",
   "title": "$PWD expands to the hook process's working directory, not the payload cwd",
   "evidence": "git_guard.py expand_vars(): assigns.setdefault('PWD', os.getcwd()). Repro (hook process cwd varied, payload cwd = project root): process cwd ROOT -> `git add $PWD`, `rm -rf $PWD/board`, `rm -rf $PWD` DENY; process cwd ROOT/tools -> all three ALLOW (artifacts/review-evidence/T-003-r3-probe-pwd.py, output T-003-r3-probe-pwd.out.txt; also seen as DENY->ALLOW in the corpus when run from artifacts/review-evidence).",
   "why_it_matters": "If the host's hook cwd differs from the Bash tool's cwd (after `cd` in an earlier call), `$PWD` points somewhere harmless and the guard approves a command that acts on the project root.",
   "fix": "Seed PWD from the payload cwd (pass cwd into expand_vars), or deny any remaining $PWD/${PWD} in a git add/rm/mv/find operand.",
   "acceptance_test": "pytest: payload cwd=ROOT with the process started in ROOT/tools: `git add $PWD` and `rm -rf $PWD/board` deny."},
  {"severity": "minor",
   "title": "Hook key log is appended on every Bash call and never capped",
   "evidence": "git_guard.py main(): opens board/.hook_input_keys.log in append mode before the command check. `wc -c board/.hook_input_keys.log` = 676375 bytes at review time; the file is gitignored (*.log) but grows for the life of the clone. r2 minor 'cap the keys log' is unchanged; TeammateIdle now logs key names only (fixed).",
   "why_it_matters": "Unbounded disk growth in a hook that runs on every command; the data (key names, agent_type) is already confirmed in the card notes, so the log has served its purpose.",
   "fix": "Delete the logging now that the identity fields are confirmed, or write only when the key set differs from the last line and cap the file at ~64 KB.",
   "acceptance_test": "pytest: 1000 hook invocations leave board/.hook_input_keys.log under 64 KB (or absent)."},
  {"severity": "nit",
   "title": "Docstring points to LESSONS.md for residual risk; handoff test count is off",
   "evidence": "git_guard.py docstring: 'Residual risk (documented in memory/LESSONS.md)'; `grep -n -i 'IFS\\|brace' memory/LESSONS.md` finds nothing; the residual list is in memory/ORCHESTRATOR_DECISIONS.md D-023. Handoff says '307 total'; `.venv/bin/python -m pytest tools/tests -q` prints '304 passed'.",
   "why_it_matters": "A reader looking for the residual list is sent to the wrong file; the evidence count does not match the run.",
   "fix": "Point the docstring at D-023 and quote the pytest output in the next handoff.",
   "acceptance_test": "grep -n 'D-023' .claude/hooks/git_guard.py returns the docstring line."}
 ],
 "whats_right": [
  "Both r2 blockers are closed with no regressions: unquoted newline, CR and backslash-newline separate commands and every '+' refspec form is denied (10/10 newline, CR and continuation probes; 3/3 '+' refspec probes).",
  "Fail-closed plumbing holds: with each guard's python replaced by 'exit 1' all three .sh wrappers deny, and non-JSON, array, null and non-string command payloads deny.",
  "Legitimate work mostly flows: multi-line python heredocs, git log/diff/show, notes with quotes and newlines, rm board/STOP and board/.locks/* all allow (56 of 61 legitimate commands)."
 ],
 "questions_for_chris": []}
```
