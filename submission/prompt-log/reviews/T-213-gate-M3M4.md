# T-213 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **pass**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

Office tab removed from the board UI. Verified at HEAD by grep and by the board server tests. No blocker or major. One minor on the tools/tests run and an observation on the in-flight prompt-log rebuild.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **minor** tools/tests is red in the dirty working tree because the in-flight prompt-log rebuild (T-187) re-introduced key-shaped test strings; HEAD is clean. Evidence: pytest tools/tests/test_secrets.py::test_repo_itself_clean -> 'check_secrets: BLOCKED ... session-6ddf8076-acdc9f4a-m0-review-security.md:695: OpenAI-style key (value redacted)' and 22 more lines; HEAD copy of the same file has 0 pattern hits; git status shows ' M submission/prompt-log/transcripts/session-6ddf8076-acdc9f4a-m0-review-security.md'.
2. **minor** tools/tests shows 6 (clone) to 11 (plain archive) failures when the repo sits under /tmp (staff panel minor 4, environmental). Evidence: GATE-M3M4-staff-engineer.md finding 4: .claude/hooks/board_guard.py:38 treats /tmp and /private/tmp as writable, so test_board_guard/test_git_guard expectations break; passes 339/339 in the real repo at f6d5c19.

```json
{
 "card": "T-213",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git show HEAD:tools/board_ui.html, tools/board_server.py; tools/tests in the main repo",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "git show HEAD:tools/board_server.py | grep -c -i office = 0; git show HEAD:tools/board_ui.html | grep -c -i office = 0",
  "staff panel: board_server.py from an archive on 7791/7792: / 200, /api/office 404, Playwright over six tabs, only console error is favicon 404",
  "pytest tools/tests -q -p no:cacheprovider in the main repo: 338 passed, 1 failed (test_secrets.py::test_repo_itself_clean)",
  "that failure: check_secrets scans the working-tree copy of submission/prompt-log/transcripts/session-6ddf8076-acdc9f4a-m0-review-security.md (23 key-shaped hits, values masked); I matched check_secrets.PATTERNS against git show HEAD: of the same file = 0 hits, against the working copy = 23",
  "git diff HEAD on that file: the in-flight prompt-log rebuild changed the redaction ('<redacted>' became 'sk-ant ...' in scanner-test lines); the file is the M0 security reviewer's transcript and the masked lines are its scanner-test commands (they appear to be synthetic test keys; I did not print or verify the values)"
 ],
 "verdict": "pass",
 "scores": {
  "ac_met_at_head": 5,
  "tests_green_at_head": 4
 },
 "findings": [
  {
   "severity": "minor",
   "title": "tools/tests is red in the dirty working tree because the in-flight prompt-log rebuild (T-187) re-introduced key-shaped test strings; HEAD is clean",
   "evidence": "pytest tools/tests/test_secrets.py::test_repo_itself_clean -> 'check_secrets: BLOCKED ... session-6ddf8076-acdc9f4a-m0-review-security.md:695: OpenAI-style key (value redacted)' and 22 more lines; HEAD copy of the same file has 0 pattern hits; git status shows ' M submission/prompt-log/transcripts/session-6ddf8076-acdc9f4a-m0-review-security.md'.",
   "why_it_matters": "Not a defect of T-213 and not in the gated commit. It would block the T-187 commit through git-guard (--staged), but a red secret scan on the tree that gets published is the thing to catch before T-194.",
   "fix": "Re-run the prompt-log redaction so scanner-test strings are redacted, then rerun tools/check_secrets.py before staging.",
   "acceptance_test": "python3 tools/check_secrets.py exits 0 on the working tree before T-187 is committed."
  },
  {
   "severity": "minor",
   "title": "tools/tests shows 6 (clone) to 11 (plain archive) failures when the repo sits under /tmp (staff panel minor 4, environmental)",
   "evidence": "GATE-M3M4-staff-engineer.md finding 4: .claude/hooks/board_guard.py:38 treats /tmp and /private/tmp as writable, so test_board_guard/test_git_guard expectations break; passes 339/339 in the real repo at f6d5c19.",
   "why_it_matters": "A QA run from a /tmp archive shows red that is not a product defect.",
   "fix": "Run the tools suite from the real checkout.",
   "acceptance_test": "pytest tools/tests passes from a clone outside /tmp."
  }
 ],
 "whats_right": [
  "No 'office' string remains in board_ui.html or board_server.py at HEAD, and /api/office returns 404.",
  "The board UI still loads all six tabs with no console errors beyond the favicon."
 ],
 "questions_for_chris": []
}
```
