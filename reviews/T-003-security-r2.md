# T-003 security review, round 2 (hooks + settings) — verdict: fail

Round 2 is a real improvement: of the 345 round-1 probes, 141 that were ALLOW are now DENY, all 35 commit-with-staged-secret spellings from round 1 now deny, and malformed input in git-guard/board-guard denies instead of passing. But the rewrite introduced a regression that makes the headline AC3 commands bypassable by a plain multi-line command: `segments()` does not treat a newline as a command separator, so `git status` followed by a new line `git add -A` is ALLOW (round 1 denied `cd /tmp` + newline + `git add -A`). `git push origin HEAD:+main` (force via refspec) is also still ALLOW. The 262 passing tests do not cover these shapes. Probe corpora and outputs are under `artifacts/review-evidence/T-003-r2-*`.

State caveat: the working tree moved while I reviewed. The fail-closed `.sh` wrappers and `from __future__ import annotations` lines are uncommitted edits (HEAD eb78e3b); `board_guard.py` changed at 18:44:50 (md5 850962e6...). Findings below are against that snapshot; git_guard.py md5 9abac86f... was stable throughout.

Regressions vs round 1 (DENY then, ALLOW now): `cd /tmp<NL>git add -A`, the three heredoc-then-command cases, `{ git add -A; }`, `echo git add -A | bash`, `git push origin main $(echo --force)`, `git push origin main \`echo -f\``, and (board-guard, working tree) `cp tools/board.py x && python3 x move T-003 done`. Residuals the handoff already documents (not findings): inherited env vars, `python -c` / `node -e` / perl code.

```json
{
 "card": "T-003",
 "persona": "security-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "round 2: 9e759a2 plus working tree at HEAD eb78e3b (uncommitted fail-closed .sh wrappers, board_guard.py md5 850962e6); .claude/hooks/*, .claude/settings.json; no app yet",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -p no:cacheprovider -> 262 passed",
  "re-ran all 345 round-1 git-guard probes with cwd set (artifacts/review-evidence/T-003-r2-git-guard-results.txt is the new corpus run; round-1 list diffed: 10 DENY->ALLOW regressions, 141 ALLOW->DENY fixes)",
  "ran ~540 new git-guard probes (T-003-r2-probe-corpus.txt -> T-003-r2-git-guard-results.txt: 285 DENY / 253 ALLOW) covering newline/brace/keyword/IFS/alias/xargs/exec/nohup/refspec/homoglyph/glob/protected-path rm and find forms",
  "ran direct probes with real newlines, line continuations, 200 KB commands, 400-deep parens, 6-deep nested bash -c, NUL and unbalanced quotes, and malformed hook JSON (T-003-r2-probe-direct.py -> .out.txt)",
  "re-ran the 35-case commit-with-staged-secret probe in a scratch repo (T-003-r2-commit-secret-probe.py): all real commit spellings now DENY",
  "ran ~230 board-guard probes as a native reviewer (agent_type security-reviewer + agent_id): legit-work misfires, write bypasses, board.py self-approval bypasses, BOARD_ROOT, agent_type variants (T-003-r2-probe-direct.out.txt, T-003-r2-probe-board2.py -> .out.txt)",
  "piped malformed and edge input into reviewer-write-guard.sh before and after the wrapper change",
  "ran every hook with PATH=/usr/bin:/bin (system python 3.9): git_guard.py and board_guard.py crashed with TypeError (list[str] | None) and exit 1 = non-blocking; re-ran after the working-tree wrapper/__future__ edits: now deny",
  "read git_guard.py, board_guard.py, reviewer_write_guard.py, the three .sh wrappers, teammate_idle.py, board_validate.py, settings.json, git diff HEAD",
  "live observation: the real board-guard hook denied several of my own legitimate Bash calls (see finding on misfires)"
 ],
 "verdict": "fail",
 "scores": {
  "git_guard_coverage": 2,
  "secret_commit_block": 4,
  "fail_closed_behavior": 4,
  "reviewer_write_guard": 3,
  "false_positive_rate": 3,
  "tests_vs_reality": 2
 },
 "findings": [
  {
   "severity": "blocker",
   "title": "Newline-separated commands are not split: anything after a benign first line bypasses every git-guard rule (regression)",
   "evidence": "git_guard.py:90-109 segments(): shlex.shlex(..., punctuation_chars=';&|()') with whitespace_split=True; newline is whitespace, so 'git status\\ngit add -A' becomes one segment [git,status,git,add,-A] and check_git sees sub=status. Probe T-003-r2-probe-direct.out.txt: ALLOW for 'git status\\ngit add -A', 'echo hi\\ngit push --force origin main', 'git log -1\\nrm -rf board', 'ls\\ngit reset --hard HEAD~3', '# note\\ngit add -A', 'git status\\r\\ngit add -A', 'git add \\\\\\n.' (backslash-newline continuation of 'git add .'), 'echo <200KB>\\ngit add -A'. Round-1 file T-003-git-guard-probe.txt line 71 'cd /tmp\\ngit add -A' was DENY; now ALLOW. Also line 287-289 heredoc-then-command cases DENY then, ALLOW now (strip_heredocs rejoins with \\n, then segments() collapses it). Also check_segment's 'cd' branch (git_guard.py:307-309) does 'continue', silently dropping the rest of that collapsed segment.",
   "why_it_matters": "Violates AC3 ('git-guard denies git add -A, reset --hard, force push'). Multi-line Bash commands are the normal shape of agent scripts, so this is not an exotic evasion: the first line only has to be something other than git. It also silently disables rm -rf protection and the commit secret scan for the same reason.",
   "fix": "Split the command on unquoted newlines (and \\r) before shlex, e.g. tokenise per line after heredoc stripping, or map unquoted newlines to ';' in a quote-aware pass; handle backslash-newline by joining lines first. Never `continue` past the remainder of a segment after cd.",
   "acceptance_test": "test_git_guard_denies gains: 'git status\\ngit add -A', 'echo hi\\r\\ngit push -f origin main', 'cd /tmp\\ngit add -A', 'ls\\nrm -rf board', 'git add \\\\\\n.', 'cat <<EOF\\nx\\nEOF\\ngit reset --hard' -> all DENY; and 'git status\\ngit log' remains ALLOW."
  },
  {
   "severity": "blocker",
   "title": "Force push via a colon refspec ('HEAD:+main') is still allowed",
   "evidence": "git_guard.py:199: `any(t.startswith(\"+\") or (t.startswith(\":\") and len(t) > 1) for t in paths)` only catches a LEADING '+'. T-003-r2-probe-direct.out.txt: ALLOW 'git push origin HEAD:+main' and 'git push origin HEAD:+refs/heads/main'; DENY only 'git push origin +main'. Round-1 blocker #3 named '+main' refspec forms; the fix covered one spelling.",
   "why_it_matters": "Violates AC3 ('denies ... force push'). 'HEAD:+main' / 'src:+dst' is the second most common way to force-push and is what an agent uses when pushing a local branch to a differently named remote branch.",
   "fix": "Treat any refspec token (not starting with '-') that has '+' at the start or immediately after ':' as a force push; keep the rule that simple (whether a push is fast-forward is not decidable in a hook).",
   "acceptance_test": "'git push origin HEAD:+main', 'git push origin +HEAD:main', 'git push origin HEAD:+refs/heads/main', \"git push origin 'a:+b'\" -> DENY; 'git push origin main', 'git push -u origin feature:feature' -> ALLOW."
  },
  {
   "severity": "major",
   "title": "Command-position parsing misses shell keywords, brace groups, xargs and wrappers that take arguments",
   "evidence": "git_guard.py:237-250 check_segment strips only names in WRAPPERS and then only flags starting with '-'. Probes ALLOW (T-003-r2-probe-direct.out.txt): '{ git add -A; }', '{ git push -f; }', 'if true; then git add -A; fi', 'for i in 1; do git add -A; done', '! git add -A', 'git status && { git add -A; }', 'f() { git add -A; }; f', 'xargs -n1 git push -f' (literal -f; xargs is not a wrapper), 'xargs git add < list', 'env -u X git add -A' (the X operand is left as the command), 'nice -n 5 git add -A', 'sudo -u root git add -A', 'timeout -s KILL 5 git add -A', 'setsid git add -A', plus ionice/taskset/caffeinate/arch/xcrun/watch/script. '{ git add -A; }' was DENY in round 1 (accidentally, by the old regex).",
   "why_it_matters": "These are ordinary shell spellings (loops over repos, `if` blocks, `sudo -u`, `nice -n`) that carry the same blocked git operations; the handoff claims 'wrapper stripping' covers this.",
   "fix": "Strip leading shell reserved words ({ } ! if then else elif fi do done while until case esac function) and 'name()' definitions; treat xargs/setsid/ionice/taskset/arch/xcrun/caffeinate/watch/script as wrappers; when a wrapper's option takes an argument (-u, -n, -s, -c, -g) consume it; and add a generic fallback: if the segment's first token is unknown but any later token is exactly 'git', analyse from that token (deny-biased).",
   "acceptance_test": "Each probe in the evidence list above -> DENY; 'for f in a b; do git add \"$f\"; done' stays ALLOW."
  },
  {
   "severity": "major",
   "title": "Unquoted pipe into a shell is no longer analysed (regression); other shell re-entry forms also pass",
   "evidence": "git_guard.py:294-302: the exec_like branch only analyses QUOTED strings and $(...)/backticks. ALLOW: 'echo git add -A | bash', 'echo git add -A | sh', '... | zsh', '... | /bin/sh', 'sh <<< git\\\\ add\\\\ -A', 'source /dev/stdin <<EOF ... EOF' (strip_heredocs feeds_shell only knows SHELLS/eval/xargs, git_guard.py:68-69), 'bash <(echo git add -A)', \"trap 'git add -A' EXIT\". Round-1 line 67 'echo git add -A | bash' was DENY; the handoff states 'pipes into a shell' are analysed.",
   "why_it_matters": "Piping a command string into sh is the standard way to run a generated command line; the claimed coverage is only true when the payload is quoted.",
   "fix": "When any segment's program is a shell (or source/. /eval) and it has no -c/script operand, analyse the previous pipeline stage's literal arguments (echo/printf/cat) as a command string; handle <(...) process substitution, here-strings with escapes, 'source/.' heredocs, and `trap '<cmd>'`.",
   "acceptance_test": "'echo git add -A | bash', 'printf \"git push -f\\n\" | sh', 'bash <(echo git add -A)', \"trap 'git add -A' EXIT\", 'source /dev/stdin <<EOF\\ngit add -A\\nEOF' -> DENY."
  },
  {
   "severity": "major",
   "title": "Unresolved expansions in git/rm arguments are allowed: $(…), glob ./*, ${IFS}, brace expansion",
   "evidence": "T-003-r2-probe-direct.out.txt ALLOW: 'git add $(pwd)', 'git add $(ls)', 'git add `pwd`', 'git add $(git rev-parse --show-toplevel)', 'git add ./*' and 'git add .*' (while 'git add *' is denied), 'git${IFS}add${IFS}-A', '{git,add,-A}', 'git push origin main $(echo --force)', 'git reset --$(echo hard)', 'git push ${F:---force}', 'rm -rf $(pwd)', 'rm -rf `pwd`', 'rm -rf $OLDPWD'. The $(...) body is analysed (git_guard.py:303-304) but its OUTPUT is never substituted back; expand_vars (75-87) ignores ${VAR:-x}. 'git push origin main $(echo --force)' and the backtick twin were DENY in round 1.",
   "why_it_matters": "'git add $(pwd)' and 'git add ./*' are add-all by another name (the round-1 recommendation was to deny any unexpanded $VAR/$(...)/glob as a git or rm operand). The handoff only documents 'variables inherited from the environment' as residual, not command substitution, IFS or brace expansion.",
   "fix": "For add/push/reset/clean/checkout/restore/rm/find/mv: if any operand still contains $, backtick, an unescaped glob (* ? [ {) or a brace list after expansion, deny with 'use literal paths'. Treat ./*, .*, ./. like * in broad().",
   "acceptance_test": "Every probe listed -> DENY; 'git add app/main.py tests/test_a.py' and 'git add -- \"app/my file.py\"' stay ALLOW."
  },
  {
   "severity": "major",
   "title": "git -c / git config can inject aliases and command-running config keys in the same command",
   "evidence": "git_guard.py:152-156 skips the value of -c without inspecting it; alias resolution (140-146) reads only the on-disk config. ALLOW: \"git -c alias.x='!git add -A' x\", \"git -c alias.x='add -A' x\", \"git config alias.zz 'add -A' && git zz\", \"git config alias.zz '!git add -A' && git zz\", \"git -c core.pager='git add -A' log\", \"git -c core.fsmonitor='git add -A' status\", \"git -c core.editor='git add -A' commit\" (the last also reaches scan_flag but the index is empty at hook time).",
   "why_it_matters": "These are exactly the alias bypasses round 1 reported (probe lines 68, 320-324); only the 'alias already exists on disk' case is fixed. core.pager/fsmonitor/editor/sshCommand execute arbitrary commands.",
   "fix": "Deny `-c`/`--config-env` whose key is alias.*, core.pager, core.editor, core.fsmonitor, core.sshCommand, core.hooksPath, core.askPass, credential.helper, or any value beginning with '!'; deny `git config` writes to alias.*, core.hooksPath and the same keys.",
   "acceptance_test": "All seven probes -> DENY; 'git -c user.name=x -c user.email=y commit -m z' (with a clean index) stays ALLOW."
  },
  {
   "severity": "major",
   "title": "rm/find protection covers only the protected directories themselves, not their contents, globs or the guard's own files",
   "evidence": "git_guard.py:121-122 is_protected() is true for the path itself or an ANCESTOR of a protected path, never a descendant; line 274 special-cases only p == ROOT/.git. ALLOW: 'rm -rf board/*', 'rm -rf memory/*', 'rm -rf reviews/*', 'rm -rf board/cards/*', 'rm -rf .git/objects', 'rm -rf .git/*', 'rm -rf .git/hooks/pre-commit', 'rm .git/hooks/pre-commit', 'rm -rf .gi?', 'rm -rf .g*', 'rm -rf .{git,claude}', 'find -delete' (no operand = cwd; git_guard.py:280-285 loop breaks at first '-' and checks nothing), 'find board -exec rm -rf {} +', 'rm -rf .claude/hooks', 'rm -f .claude/settings.json', 'rm -rf tools', 'mv x board/cards/T-001.md' (PROTECTED lists board/cards, handoff lists .git, board, memory, reviews). 'rm -rf board/*' etc. were ALLOW in round 1 too.",
   "why_it_matters": "The handoff presents these paths as protected; wiping their contents, the git object store, the native pre-commit hook or the hooks themselves is one glob away. Removing the pre-commit hook silently disables the secret gate (see T-006).",
   "fix": "Resolve each operand; treat descendants of .git, .claude, tools, board, memory, reviews as protected for any recursive rm or for rm of .git/hooks/*, .claude/settings.json and .claude/hooks/*; expand/deny glob metacharacters (* ? [ {) in rm operands under the project root; default `find` start path to '.' and apply the same checks to -exec rm/-delete.",
   "acceptance_test": "'rm -rf board/*', 'rm -rf .git/objects', 'rm .git/hooks/pre-commit', 'rm -rf .gi?', 'find -delete', 'find board -exec rm -rf {} +', 'rm -rf .claude/hooks' -> DENY; 'rm -rf app/__pycache__' and 'rm -f artifacts/tmp/x.png' -> ALLOW."
  },
  {
   "severity": "major",
   "title": "Reviewer write enforcement (board-guard) is a denylist with holes in ordinary spellings",
   "evidence": "board_guard.py:113-165 (redirect regex at ~88-96, WRITE_CMDS at 33, sed handling at ~141). As a native reviewer (agent_type security-reviewer + agent_id), ALLOW: 'echo x >& app/x' (the `&` branch `continue`s), 'sed -Ei s/a/b/ app/x', 'sed -ni p app/x', 'sed --in-place=.b ...' (only args starting with -i are matched), \"perl -pi -e 's/a/b/' app/x\", 'ruby -i', 'unlink app/x', 'shred -u app/x', 'chown arsis app/x', 'curl https://x -oapp/x', 'curl ... --output=app/x', 'curl -sSo app/x ...', 'curl -sO ...', 'wget https://x' (writes cwd), 'wget -P app ...', 'unzip a.zip -d app', 'pip install -t app x', 'git clone https://x app/r', 'git diff --output=app/x', 'git format-patch -o app', 'git bundle create app/x.bundle', 'git archive -o app/x.tar', and non-listed mutating git: update-ref, symbolic-ref, hash-object -w, write-tree, read-tree, update-index, gc, notes, fetch, submodule update (MUTATING_GIT, board_guard.py:~30). Output: T-003-r2-probe-direct.out.txt and T-003-r2-probe-board2.out.txt. The handoff documents only interpreter-written files as residual.",
   "why_it_matters": "'Reviewers are read-only on product code: a hook enforces this' is a stated invariant; `sed -Ei` and `>&` are accidental-use spellings, not exotic ones.",
   "fix": "Invert for reviewers: allow an explicit set of read-only programs (cat ls grep rg sed-without--i head tail wc diff jq git read-only subcommands python3 -m pytest curl-without-output etc.) and deny the rest, or at minimum add the spellings above (>&, -[a-zA-Z]*i clusters, --in-place*, curl -o/--output/-O/-o<attached>/combined short flags, wget, unzip, pip -t, git clone/update-ref/symbolic-ref/hash-object/read-tree/update-index/gc/notes/fetch and --output/-o options). Document 'python -c' as the known residual.",
   "acceptance_test": "Each probe -> DENY for a reviewer identity; the 'legit' set (git log/diff/show, sed -n, curl -s URL -o artifacts/review-evidence/x, pytest) -> ALLOW."
  },
  {
   "severity": "major",
   "title": "board.py self-approval guard (no reviewer/worker moves a card to done or records a review) is evaded by wrappers and flags; the latest edit made it weaker",
   "evidence": "board_guard.py working tree (18:44:50) board_args(): only seg[i]=='board.py' or python[3[.x]] [-flags] board.py counts. T-003-r2-probe-board2.out.txt ALLOW as a reviewer: 'env python3 tools/board.py move T-003 done', 'env -i python3 tools/board.py ...', 'nice python3 ...', 'time python3 ...', 'arch -arm64 python3 ...', 'python3 -W ignore tools/board.py ...', 'python3 -X dev tools/board.py ...', 'cp tools/board.py /private/tmp/.../b.py && python3 /private/tmp/.../b.py move T-003 done', 'python3 -m tools.board move T-003 done'. 'cp ... b.py && python3 b.py move T-003 done' was DENY before this edit (first run vs second run of T-003-r2-probe-direct.py: diff line 241). BOARD_ROOT=<allowed scratch path> exempts the whole command (board_root_outside), which is intended, but relies on allowed_write's realpath of a path that does not yet exist.",
   "why_it_matters": "'No self-approval' (only the orchestrator moves to done / records reviews) is a core harness rule; the hook is the only identity-aware check because board.py trusts a self-declared --agent.",
   "fix": "Run the segment through the same wrapper/flag stripping as git_guard.check_segment before looking for board.py; additionally deny, for any non-orchestrator identity, any command string containing 'board.py' or 'tools.board' or `import board` outside the READONLY_BOARD whitelist; longer term make board.py require a per-session orchestrator token the hook injects (hooks can rewrite the command via updatedInput).",
   "acceptance_test": "The eight listed probes -> DENY for agent_type backend and security-reviewer; 'python3 tools/board.py show T-003' -> ALLOW."
  },
  {
   "severity": "minor",
   "title": "Hooks misfire on legitimate reviewer work (hit live while writing this review)",
   "evidence": "Live: 'cd <scratchpad> && cat > probe2.py <<EOF' denied ('redirect to probe2.py': the redirect check runs on the pre-cd cwd, board_guard.py ~88-96); 'cat > $SP/probe2.py' denied (variables are not expanded for redirect targets); 'git config --get ...' denied ('reviewers may not run git config'); a valid command containing \"$(head ... | sed 's/.*reason\": \"//')\" denied by git-guard ('could not parse command safely (No closing quotation)', flat shlex cannot parse nested quotes inside $() in double quotes); Write to the scratchpad is denied by reviewer-write-guard although the persona says to use it and board-guard allows it for Bash. Probe T-003-r2-probe-direct.out.txt / board2.out.txt: DENY for 'git branch --list', 'git stash list', 'git tag -l', 'git worktree list', 'git init /private/tmp/.../repo2', 'git -C <scratch repo> add/commit', 'cd <scratch repo> && git add x' (scratch-repo probing, which security review needs, is impossible without a python subprocess that evades the guard), \"grep -rln 'git add' docs | xargs wc -l\", \"awk '$1 > 5 {print}' f | xargs echo\" and 'echo \"bash -c '\\''git add -A'\\'' is bypassed\" > reviews/x.md' (new quoted-string recursion treats quoted prose/awk as commands whenever xargs, $( or backtick appears), and a commit message like \"note: use bash -c 'git add -A' never\".",
   "why_it_matters": "False positives push reviewers (and workers) toward python/subprocess workarounds that the guards cannot see, and erode trust in the hooks.",
   "fix": "Track `cd` for the redirect check; expand simple VAR=value before the redirect regex; allow read-only forms (branch --list, config --get, stash list, tag -l, worktree list) and mutating git when -C/cwd resolves under /tmp or the scratchpad; make the scratchpad writable for the Write tool; for quoted-string recursion only treat a quoted string as a command when it is the operand of sh -c/eval/xargs sh or a pipe-to-shell stage.",
   "acceptance_test": "All the quoted legit commands above -> ALLOW for a reviewer identity; the corresponding bypass probes remain DENY."
  },
  {
   "severity": "minor",
   "title": "reviewer-write-guard still fails open on non-JSON and unknown keys; crash handling only exists as uncommitted wrapper edits",
   "evidence": "reviewer_write_guard.py main() uses _common.read_input(), which swallows parse errors: '{{{' and empty stdin -> exit 0 with no output; {\"tool_input\":{\"filepath\":\"<ROOT>/app/x.py\"}} -> allowed (path key not recognised). Non-object / int / NUL path inputs crash with a traceback (exit 1, non-blocking) in the committed code; in the working tree the new .sh wrapper turns those into deny (verified). git_guard and board_guard deny on non-JSON ('guard error (JSONDecodeError...)'). settings/hook wrappers (git-guard.sh etc.) are uncommitted: before them, PATH=/usr/bin (python 3.9) made git-guard and board-guard crash with `TypeError: unsupported operand type(s) for |` and exit 1 = fail open; /opt/homebrew/bin/python3 is hard-coded in the wrapper.",
   "why_it_matters": "Round-1 major 'guards fail open on internal errors and malformed input' is closed for git/board guards and, via the wrapper, for crashes, but the reviewer write guard still allows on unparseable input; the fix is not yet in a commit and has no test.",
   "fix": "Make reviewer_write_guard emit deny on any parse failure or when no path key is found for Edit|Write|NotebookEdit; commit the wrappers; add tests that run each .sh with a crashing python and with system python 3.9; replace the hard-coded homebrew path with a lookup order (python3.12, python3.11, python3).",
   "acceptance_test": "Piping '{{{' and '{\"tool_input\":{\"filepath\":\"x\"}}' into reviewer-write-guard.sh -> deny JSON; test_hooks gains a crash-wrapper test; `git status` shows the wrappers committed."
  },
  {
   "severity": "minor",
   "title": "History-moving and gate-tag operations remain allowed",
   "evidence": "ALLOW (T-003-r2-git-guard-results.txt): 'git tag -f m0' and 'git tag --force m0' (tag -d is denied), 'git branch -f main HEAD~5', 'git branch -M main', 'git checkout -B main HEAD~3', 'git update-ref refs/heads/main HEAD~1', 'git reset main' / 'git reset origin/main' (git_guard.py:205 regex only matches HEAD, ~ ^ @ or hex), 'git fetch -f origin +refs/heads/*:refs/heads/*', 'git pull --force', 'git remote remove origin', 'git config core.hooksPath /dev/null', 'git read-tree --reset -u HEAD', 'git checkout-index -a -f', 'git submodule foreach git add -A'.",
   "why_it_matters": "CONTRACT 'never rewrite history' and the m0 gate tag are integrity rules; moving the m0 tag or main is as destructive as the blocked forms.",
   "fix": "Deny tag -f/--force, branch -f/-M/-m on existing branches, checkout/switch -B/-C, update-ref/symbolic-ref, fetch/pull -f and '+' refspecs, read-tree --reset, checkout-index -f, and `git config` writes to core.hooksPath; resolve any `reset <non-flag>` operand that is not a path after `--` as a revision.",
   "acceptance_test": "Each probe -> DENY; 'git tag -a m0 -m gate' and 'git checkout -b feature' -> ALLOW."
  },
  {
   "severity": "minor",
   "title": "TeammateIdle still logs raw hook input unredacted; hook key log is unbounded",
   "evidence": "teammate_idle.py:15-16 writes json.dumps(raw, indent=1) to board/.hook_debug.log (gitignored). My probe of the hook created it: 'TeammateIdle raw input: { \"tool_input\": { \"command\": \"git add -A\", ...' (cat board/.hook_debug.log). git_guard.py:329-334 appends one line per Bash call to board/.hook_input_keys.log (2031 lines / 251 KB at review time, no rotation).",
   "why_it_matters": "Round-1 minor (log only key names) is unchanged; raw input can contain prompts or secrets typed into commands. Disclosure: this review's probes created board/.hook_debug.log and added lines to .hook_input_keys.log (both gitignored).",
   "fix": "Log key names and agent_type only (as the other hook does), delete the file once the field mapping is confirmed, cap the keys log.",
   "acceptance_test": "After running teammate-idle with a crafted input containing 'sk-ant-TEST', grep -c 'sk-ant' board/.hook_debug.log -> 0."
  }
 ],
 "whats_right": [
  "Fail-closed in git-guard and board-guard is real: non-JSON, non-object, non-string command, cwd of the wrong type, unterminated quotes, nesting >4 and secret-scan timeout all produce a deny, and a crashing python is now denied by the .sh wrappers (working tree).",
  "Global-option, abbreviation and alias handling works for the spellings the tests target: git -C/-c/--no-pager, --forc, -fu clusters, \\git, /usr/bin/git, sh -c / eval / quoted strings up to depth 4 (141 of the 345 round-1 probes flipped to DENY).",
  "Commit-time secret scan now runs for every commit spelling, including git -c ... commit, quoted git/commit and unknown aliases: every real commit spelling in the 35 round-1 variants (and the alias/commit-tree ones) denies when a key is staged."
 ],
 "questions_for_chris": [
  "Threat model for the guards: only accidents by well-meaning agents, or a hostile/prompt-injected agent? If the latter, string-matching hooks are the wrong layer and a sandboxed shell or an allow-list of commands is needed; the findings above are rated for the accident-plus-lazy-evasion model.",
  "Should reviewers be allowed mutating git inside a scratch repo under /tmp (needed to exercise check_secrets and similar), with the same rule enforced by resolving -C/cwd?"
 ]
}
```
