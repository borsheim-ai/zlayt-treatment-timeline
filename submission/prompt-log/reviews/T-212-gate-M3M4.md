# T-212 review, combined M3+M4 gate (D-075), staff-engineer-reviewer

Verdict: **changes**. HEAD a932fc9dcd627e0e5f92a234add6fc41b835a4f1.

README front door. The install and the walk work on a fresh clone (installer and verify pass), the `make evals` blocker is fixed, and all 58 README links resolve. The installer panel's major is still open at HEAD: the first command is a placeholder. The README discloses it and gives a zip path, and it cannot be closed until the repo is published, but it is open, so the verdict is changes.

Panel evidence used: reviews/GATE-M3M4-staff-engineer.md (f6d5c19), reviews/GATE-M3M4-verify-staff.md (43ce6eb), artifacts/gate-M3M4-suite-final.txt (43ce6eb: unit 5945 passed 0 failed, e2e 614 passed 0 failed, letter_check 0, spec check all true).

## Findings
1. **major** The first README command cannot run as written: it clones https://github.com/OWNER/zlayt.git. Evidence: README.md:13 'The repo URL below does not exist yet ... OWNER is a placeholder'; README.md:16 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'. GATE-M3M4-installer.md major 1: 'First README command is a placeholder that fails'. verify-staff did not re-rate it; row 29 of SCOPE_CUTS accepts it as debt.
2. **minor** Docker build and run were never executed and the README says so (accepted, NEEDS_CHRIS). Evidence: GATE-M3M4-installer.md 'Not exercised': docker build, docker run, make test, deploy/; SCOPE_CUTS debt row for T-182.

```json
{
 "card": "T-212",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git archive a932fc9: README.md, run.sh, Makefile; installer panel at f6d5c19; verify pass at 43ce6eb",
 "exercised": [
  "git rev-parse HEAD = a932fc9 (docs-only on top of c2dd104); git diff --stat 43ce6eb a932fc9 -- app tests/e2e is empty, so the 43ce6eb unit/e2e runs still describe the app at HEAD",
  "python3 tools/board.py show <card> for the AC of this card",
  "read reviews/GATE-M3M4-{staff-engineer,ux-designer,paralegal,privacy-compliance,installer,product-manager}.md, GATE-M3M4-verify-staff.md, GATE-M3M4-verify-pm-r2.md and artifacts/gate-M3M4-suite-final.txt",
  "git archive a932fc9 into a scratchpad dir (arcC) for every check below, so the dirty main working tree was not read for product claims",
  "grep -n OWNER README.md at a932fc9: line 13 explains the placeholder, line 16 is 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'",
  "link checker: README.md 58 relative links, 0 dead",
  "verify-staff: fresh clone under env -i, ./run.sh healthy, Playwright walk of README steps 1-5 reaches $8,390.00 and a letter, zero page errors; make evals exits 2 and names exactly three blocker lines",
  "grep -n -i 'date of service' README.md: line 43 now describes the blank (installer minor fixed)",
  "git show HEAD:memory/SCOPE_CUTS.md row 29 lists 'Installer: README OWNER placeholder until Chris publishes' as accepted debt",
  "git show HEAD:submission/NEEDS_CHRIS.md rows 2-4: publish only the snapshot (T-195), byline and links (T-190), demo link (T-022); grep OWNER in NEEDS_CHRIS.md finds nothing, so no row says to replace the README placeholder"
 ],
 "verdict": "changes",
 "scores": {
  "fresh_clone_path_works": 5,
  "claims_true": 5,
  "first_command_runs_as_written": 2
 },
 "findings": [
  {
   "severity": "major",
   "title": "The first README command cannot run as written: it clones https://github.com/OWNER/zlayt.git",
   "evidence": "README.md:13 'The repo URL below does not exist yet ... OWNER is a placeholder'; README.md:16 'git clone https://github.com/OWNER/zlayt.git zlayt && cd zlayt'. GATE-M3M4-installer.md major 1: 'First README command is a placeholder that fails'. verify-staff did not re-rate it; row 29 of SCOPE_CUTS accepts it as debt.",
   "why_it_matters": "The T-212 AC is 'a fresh-clone reader following only README reaches the sample case and the letter'. Today that works only through the zip path the README mentions in one sentence. The placeholder is disclosed, so it does not mislead, but a reviewer who copies the first command gets 'repository not found'.",
   "fix": "At publish time (T-194/T-195) replace OWNER with the real account in the snapshot's README, or name the actual path in the first code block (unzip, then ./run.sh) until a URL exists. This needs Chris's account name, so it is a publish-step item, not a worker fix today.",
   "acceptance_test": "grep -c OWNER README.md in the published snapshot returns 0 and `git clone <that url>` works from an empty directory; or the first code block is the zip path and runs."
  },
  {
   "severity": "minor",
   "title": "Docker build and run were never executed and the README says so (accepted, NEEDS_CHRIS)",
   "evidence": "GATE-M3M4-installer.md 'Not exercised': docker build, docker run, make test, deploy/; SCOPE_CUTS debt row for T-182.",
   "why_it_matters": "Reader-facing Docker instructions are unproven; the README does not hide that.",
   "fix": "Chris runs `make docker docker-run` once with Docker Desktop.",
   "acceptance_test": "a note on NEEDS_CHRIS says it ran."
  }
 ],
 "whats_right": [
  "A fresh clone under env -i reaches a healthy server, the sample case and a downloadable letter with zero page errors.",
  "The 'make evals' description now matches reality (three blocker lines, exit 2) and the README names the date blank in the walk."
 ],
 "questions_for_chris": [
  "Which GitHub account and repo name will host the public snapshot, so README.md:16 can be filled in at publish (T-194/T-195)?"
 ]
}
```
