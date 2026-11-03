# T-212 staff-engineer review, round 2 (staff-engineer-reviewer)

Verdict: **pass**. Scope: HEAD be257c9 (`docs(release): drop OWNER placeholder clone step from README (T-212)`), which changes README.md only (1 insertion, 2 deletions). This round checks the two things the round-1 major asked for: no OWNER clone URL, and every README link to a repo file resolves.

## What I checked at HEAD

1. **No OWNER URL.** `git show HEAD:README.md | grep -n -i owner` prints nothing and exits 1. The HEAD README has no `git clone` line and no github.com URL at all. A repo-wide check, `git grep -n -E "github\.com/OWNER|OWNER/zlayt" HEAD`, prints nothing. The other `OWNER` hits in tracked files are file-ownership comments (for example `app/frontend/guided/review.js:1`) and prompt-log transcripts, not clone URLs. Evidence: `artifacts/review-evidence/T-212-r2/owner_grep_head.out`.
2. **Every README link to a repo file resolves.** I took the markdown link targets and `href`/`src` attributes in the HEAD README (58 in total) and checked each against the tracked files at HEAD (`git ls-tree -r --name-only HEAD`; this list is byte-identical to `git ls-files` for the index at the time of the check). All 58 resolve to a tracked file or directory, 0 are missing, and 0 are external. Bare `<http://127.0.0.1:7860>` and code spans are not links, so they are not counted. Evidence: `artifacts/review-evidence/T-212-r2/readme_links.out` (script `check_readme_links.py` alongside it).
3. **Commands the README names are tracked and executable.** `run.sh` and `deploy/hf_push.sh` are both mode 100755 at HEAD.
4. **The open item in the AC evidence is closed at HEAD.** The AC note said `submission/SUBMISSION_CHECKLIST.md` and `submission/email-draft.md` were linked but untracked. Both are tracked at HEAD (mode 100644).

## Observation outside the HEAD artifact (minor)

While I was reviewing, the shared index and the worktree for README.md were not in agreement with HEAD. `git status --short -- README.md` printed `MM README.md`. The staged blob (9b56421) is the pre-fix README, so `git diff --cached HEAD -- README.md` adds back `+git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt`. The worktree blob (174fc0c) equals HEAD. My first read of the worktree against HEAD was clean, and a second read a few minutes later showed the staged reversal, so someone is staging README.md while this review runs. HEAD is correct and this does not change the verdict. But any commit made from this index without a pathspec would reintroduce the OWNER line and reopen the round-1 major. Evidence: `artifacts/review-evidence/T-212-r2/readme_index_state.out`.

## Not exercised

- No fresh clone was walked by me. That is the installer-reviewer's job, and their pass is in `reviews/T-212-installer-r2.md`.
- No pytest or eval run. The diff is one README paragraph and the brief named no tests. The LLM, grounding and totals checks in my checklist are outside this card's diff.
- No app URL was exercised. The card is documentation only.
- Model id: I am running as claude-haiku-5-5. The persona brief expects claude-sonnet-5-5 and the round-1 record used that id. I record the model I am actually running as; see the question below.

## Verdict rule

No blocker. No major. One minor, which is scoped to the index and not to the commit. Verdict: pass.

```json
{"card": "T-212", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD be257c9 (README.md only, +1/-2); repo-wide git grep at HEAD; reviews/T-212-gate-M3M4.md (round 1 finding); no app URL (docs-only card)",
 "exercised": [
  "read personas/staff-engineer.md in full and the card via python3 tools/board.py show T-212",
  "read reviews/T-212-gate-M3M4.md and reviews/T-212-installer-r2.md",
  "git show --stat HEAD and git show HEAD -- README.md (diff is 1 insertion, 2 deletions)",
  "git show HEAD:README.md | grep -n -i owner, exit=1 with no output (artifacts/review-evidence/T-212-r2/owner_grep_head.out)",
  "git grep -n -E 'github.com/OWNER|OWNER/zlayt' HEAD, no output",
  "python3 -I artifacts/review-evidence/T-212-r2/check_readme_links.py on the HEAD README against git ls-tree -r HEAD: 58 targets, 58 resolve, 0 missing (readme_links.out)",
  "git ls-tree HEAD for run.sh, deploy/hf_push.sh (100755), submission/SUBMISSION_CHECKLIST.md, submission/email-draft.md (100644)",
  "git ls-files -s README.md and git status --short -- README.md: index holds 9b56421, HEAD is 174fc0c, status MM (readme_index_state.out)",
  "git diff --cached HEAD -- README.md: shows the OWNER clone line re-added to the index"
 ],
 "verdict": "pass",
 "scores": {"no_placeholder_url": 5, "link_integrity": 5, "scope_of_change": 5, "index_hygiene": 3},
 "findings": [
  {"severity": "minor",
   "title": "Shared index stages the pre-fix README; a pathspec-less commit from it would reopen the round-1 major (index state, not HEAD)",
   "evidence": "artifacts/review-evidence/T-212-r2/readme_index_state.out: index blob 9b56421b9920bc25236835c2d3f84d1a98f45a5e, HEAD blob 174fc0cc30d1ddc8aa031e7e3a2cd23565c32096, status MM README.md. git diff --cached HEAD -- README.md adds '+git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'.",
   "why_it_matters": "HEAD is correct, so this does not change the verdict. But the index is shared, and a commit that does not name README.md as a pathspec would carry the placeholder back into the repo and reopen the round-1 major. The worktree and index changed between two reads during this review, so the state is not stable.",
   "fix": "Whoever owns the in-flight README edit should decide whether it is intended. If not, restore the index entry to HEAD before any further commit. Commit only with an explicit pathspec, as CLAUDE.md requires.",
   "acceptance_test": "git show HEAD:README.md | grep -c -i owner prints 0; git diff --cached --quiet -- README.md (or the index blob equals git ls-tree HEAD README.md) after the next commit; git grep -n -E 'github.com/OWNER|OWNER/zlayt' HEAD prints nothing."}
 ],
 "whats_right": [
  "The fix is the minimum: HEAD be257c9 changes README.md only, one paragraph and one command line removed.",
  "All 58 relative README targets resolve to tracked files or directories at HEAD, and the two submission files the AC note called untracked are now tracked.",
  "The commands the README names (run.sh, deploy/hf_push.sh) are tracked and executable."
 ],
 "questions_for_chris": [
  "Is someone intentionally re-staging the OWNER clone line in README.md (index 9b56421 against HEAD 174fc0c)? If it is intentional, the r2 verdict covers HEAD only.",
  "Which model id should the reviewer record carry? I am running as claude-haiku-5-5; the persona brief expects claude-sonnet-5-5. I used the model I am running as."
 ]}
```
