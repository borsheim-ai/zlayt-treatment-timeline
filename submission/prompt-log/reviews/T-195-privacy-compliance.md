# T-195 review: NEEDS_CHRIS publish item (privacy-compliance-reviewer)

**Verdict: changes.** Mechanical checks pass for the four points in the brief. One major finding: NEEDS row 11 says the
prompt-log default is "Redacted", but the HEAD prompt log still names a third-party project in 161 places, and the
snapshot scan does not check for it. Row 10's publish steps match `deploy/SNAPSHOT.md`.

**Model note.** This review was run as claude-haiku-5-5 (the model I am actually running as). My dossier expects
claude-opus-5-5 for judgment reviews, so the orchestrator should check whether this run counts as the judgment review.

## Scope and what I exercised

- Commit `dfd9b11` (subject "docs(submission): NEEDS_CHRIS publish-from-snapshot item, T-193, row 8 to P2"). It is an ancestor of HEAD.
  `git diff --stat dfd9b11 HEAD` and `git diff --stat dfd9b11` (working tree) are both empty for `submission/NEEDS_CHRIS.md` and `deploy/SNAPSHOT.md`, so the three sources agree.
- `git show dfd9b11:submission/NEEDS_CHRIS.md` (43 lines), read in full. Row 10 (P0, T-195), row 11 (P1, T-193), row 8 (P2, T-191).
- `deploy/SNAPSHOT.md` (102 lines), read in full. Usage, one-time setup, "To publish" line, exit-code text, run record.
- `git show dfd9b11:deploy/make_public_snapshot.sh`: line 9 (`python3 deploy/snapshot_tool.py init-patterns .`), lines 21-26
  (missing-file exit 2, refusal if tracked), 59 (`init -q -b main`), 17-18 (author name and address), 83 (`SNAPSHOT_PATH=` print).
- `git show dfd9b11:.gitignore`: line 35 is `deploy/.private_patterns`. `git ls-files -- deploy/.private_patterns` returns 0 lines
  (not tracked). `git check-ignore -v deploy/.private_patterns` matches `.gitignore:35`.
- `python3 tools/board.py show T-195` (ACs, status in_review, commits `dfd9b11`) and `python3 tools/board.py show T-193`
  (status needs_chris, P1, AC "default: redacted").
- `artifacts/review-evidence/T-195-checks.py` (run with `python3 -I`). Counts and line numbers only. The local
  `deploy/.private_patterns` was read by kind and count only; no value was printed or written to the review.
- `artifacts/review-evidence/T-195-snapshot-md-checks.py` (run with `python3 -I`). Classification only.
- `git log --all` author and committer counts against the email-kind patterns (count only).
- `git grep` counts for the third-party project name at HEAD; `evals/finalize_prompt_log.py` lines 58-66 and 228-235 read.
- `personas/privacy-compliance.md` and my memory directory (`public-snapshot-review.md`, `recurring-findings.md`, `prompt-log-review.md`).

## Results

**1. Row 10 tells Chris to publish only the snapshot: PASS.** Row 10 says "Never push this repo, its history or any existing
branch", and SNAPSHOT.md says "Publish only from the snapshot this script builds. Never push the working repo or its history."

**2. Row 10 steps match SNAPSHOT.md: PASS, with two nits.**

| Row 10 step | SNAPSHOT.md | Match |
|---|---|---|
| `bash deploy/make_public_snapshot.sh` | Usage: `bash deploy/make_public_snapshot.sh` | yes |
| needs local, gitignored `deploy/.private_patterns`; one-time setup in `deploy/SNAPSHOT.md` | "One-time setup: the local private-patterns file"; exits 2 if missing | yes |
| prints `SNAPSHOT_PATH=<dir>` | "It prints `SNAPSHOT_PATH=<dir>` and exits 0 only if every check passes" | yes |
| new one-commit repo, author cborsheim@gmail.com, passed the scan | step 4 (author and committer) and step 5 (scan) | yes (script: `AUTHOR_EMAIL="cborsheim@gmail.com"`) |
| `cd <dir> && git remote add origin <url> && git push -u origin main` | "To publish: `cd <SNAPSHOT_PATH> && git remote add origin <url> && git push -u origin main`" | yes; the script creates branch `main` (`init -q -b main`), so the push refspec is valid |
| non-zero exit: do not publish | exit 1 on failure with "do NOT publish"; exit 2 for missing patterns | yes |

- nit: row 10 adds "or any existing branch". SNAPSHOT.md does not say that. It is stricter and consistent with the rest, so it is not a conflict.
- nit: row 10 points to the one-time setup but does not spell the init command. SNAPSHOT.md and the script header (line 9) both have it.
- The "29 commits authored with the work email" claim is correct: 29 commits in `git log --all` have an author matching an email pattern (count only).

**3. Row 11 lists T-193 with its default (redacted): listed PASS; the default is not implemented (see finding F1).**
Row 11 and the T-193 card both state the default as "redacted", but HEAD does not match it.

**4. No private value in the file: PASS.** Output of `T-195-checks.py` against `dfd9b11:submission/NEEDS_CHRIS.md`:
- tailnet-shaped (tail+hex, <redacted-private>): 0 lines
- <redacted-private>/10-shaped IPv4: 0 lines
- any IPv4-shaped: 0 lines
- non-user email-shaped strings: 0
- private-pattern kinds (device 2 patterns, email 3, term 1): 0 matching lines for each kind
- the same result for the working-tree copy

For context, `deploy/SNAPSHOT.md` has 3 lines with 100.x-shaped strings. All three are the documented exempt test peer and CIDR text (`<redacted-private>`, `<redacted-private>/10`), and the one non-user email-shaped string is a placeholder. No private pattern matches in either file.

## Findings

**F1 (major): row 11 states a redacted default that the HEAD prompt log does not implement, and the publish scan does not catch it.**
- Count: `git grep -h -o` for the third-party project name at HEAD gives 161 occurrences in 82 files under `submission/prompt-log/`; 89 files in total.
  The same name appears in `submission/NEEDS_CHRIS.md`, `board/` cards, `memory/`, `MASTER_PROMPT.md`, and `app/frontend/stepper.js`.
- `evals/finalize_prompt_log.py:63` redacts only path forms (job-search and project-folder paths). No rule redacts the bare name.
- `evals/finalize_prompt_log.py:233` describes the prompt log as containing "excerpts from Chris's other local projects (for example the
  [third-party] project) and directory listings of his job-search folders".
- `deploy/.private_patterns` has 1 term-kind pattern, and it does not contain the name (boolean check).
- So the snapshot's text scan and redaction do not cover it. Row 10 says the snapshot "passed the scan", which is true for the scan's
  patterns but can be read as a clean bill for this content.
- Row 11 verbatim: "Redacted (the default); the prompt-log export follows your answer."

Why it matters: the snapshot publishes whatever is in HEAD. "Default redacted" describes a rule the exporter does not have, so Chris
could approve publishing on a false premise. The content is third-party project material and personal job-search detail, not Zlayt
data, so I rate it major on current evidence. If Chris confirms the excerpts are verbatim material from a real third-party or client
matter, §5 of my dossier applies and this becomes a blocker.

Fix: either (a) QA adds a bare-name rule to the finalizer and the exporter is re-run before publish, or (b) row 11 says what is true
today ("not redacted at HEAD: 161 occurrences in 82 prompt-log files; publish is held until you answer"), and row 10 adds "the scan
does not check third-party project names or job-search folder names". Do not add the name to the public tree as a fix.

Acceptance test: after the chosen fix, `git grep -c -i <name> <snapshot>` returns 0 (or Chris's recorded answer in the Inbox is
`show` and the row says so). Row 11 text matches the exporter's actual output.

**F2 (nit): row 10 wording differs from SNAPSHOT.md.** Add "or any existing branch" to SNAPSHOT.md, or leave it as a stricter
instruction. Either is acceptable.

**F3 (nit): row 10 does not spell the one-time setup command.** Optionally add `python3 deploy/snapshot_tool.py init-patterns .`.

## What is right

1. Row 10's push command matches `deploy/SNAPSHOT.md` exactly, and the script's `init -q -b main` makes the `main` refspec valid.
2. `submission/NEEDS_CHRIS.md` at `dfd9b11` has no tailnet-shaped string, no <redacted-private>/10 address, no non-user email, and no
   private-pattern match.
3. Row 11 matches the T-193 card (P1, needs_chris, default redacted). The "29 commits" claim checks out.

## Questions for Chris

- Are the excerpts behind F1 verbatim material from a real third-party project, or from a client matter? If so, F1 becomes a blocker under §5.
- Should the prompt-log default be "redact" for the third-party project name as well as for paths? That is the T-193 decision.

```json
{"card": "T-195", "persona": "privacy-compliance-reviewer", "model": "claude-haiku-5-5",
 "scope": "submission/NEEDS_CHRIS.md at commit dfd9b11 (row 10, row 11, row 8); deploy/SNAPSHOT.md (dfd9b11, HEAD and working tree identical); deploy/make_public_snapshot.sh and deploy/snapshot_tool.py at dfd9b11; .gitignore at dfd9b11; board cards T-195 and T-193; HEAD prompt log and finalizer (read-only, counts only)",
 "exercised": [
  "git show dfd9b11:submission/NEEDS_CHRIS.md (read in full, 43 lines)",
  "git show HEAD:deploy/SNAPSHOT.md and working-tree deploy/SNAPSHOT.md (read in full, 102 lines); git diff --stat dfd9b11 HEAD and dfd9b11 working tree: empty for both files",
  "git merge-base --is-ancestor dfd9b11 HEAD: yes",
  "git show dfd9b11:deploy/make_public_snapshot.sh and snapshot_tool.py: grep of usage, exit codes, author, init -q -b main, SNAPSHOT_PATH print",
  "git show dfd9b11:.gitignore | grep private_patterns: line 35; git ls-files deploy/.private_patterns: 0; git check-ignore -v: matched .gitignore:35",
  "python3 tools/board.py show T-195 and show T-193 (read-only)",
  "python3 -I artifacts/review-evidence/T-195-checks.py: tailnet/100.x/IPv4/email shapes and private-pattern kinds, counts only (dfd9b11 and working tree)",
  "python3 -I artifacts/review-evidence/T-195-snapshot-md-checks.py: classification of SNAPSHOT.md 100.x and email strings (documented-exempt; placeholder)",
  "git log --all author and committer counts against email-kind patterns: 29 commits with a matching author",
  "git grep -l / -h -o for the third-party project name at HEAD (89 files; 161 occurrences in 82 prompt-log files); evals/finalize_prompt_log.py lines 58-66 and 228-235 read; deploy/.private_patterns term kind (boolean, no match)",
  "personas/privacy-compliance.md read in full; reviewer memory (public-snapshot-review.md, recurring-findings.md, MEMORY.md index)"
 ],
 "verdict": "changes",
 "scores": {"publish_only_from_snapshot": 5, "row10_steps_match_SNAPSHOT_md": 4, "no_private_values_in_NEEDS": 5, "row11_T193_listed_and_default_stated": 3, "row11_default_implemented_at_HEAD": 2, "scan_coverage_of_third_party_names": 2},
 "findings": [
  {"severity": "major",
   "title": "Row 11 states a redacted default that HEAD does not implement; the publish scan does not cover the third-party project name",
   "evidence": "submission/NEEDS_CHRIS.md row 11 verbatim: 'Redacted (the default); the prompt-log export follows your answer.' git grep at HEAD: third-party project name in 161 occurrences across 82 files under submission/prompt-log/ (89 files total). evals/finalize_prompt_log.py:63 redacts only path forms; evals/finalize_prompt_log.py:233 describes excerpts from other local projects and job-search folder listings in the prompt log. deploy/.private_patterns term kind: 1 pattern, does not contain the name (boolean check). Row 10 says 'that passed the scan'.",
   "why_it_matters": "Chris could approve publishing from the snapshot on the premise that the default redacts the name, but HEAD and the scan do not implement that. The content is third-party project material and personal job-search detail; it is not Zlayt data, so this is major on current evidence. It becomes a blocker under dossier section 5 if the excerpts are verbatim real third-party or client material.",
   "fix": "Either (a) QA adds a bare-name rule to evals/finalize_prompt_log.py, the exporter is re-run, and the snapshot is re-checked before publish; or (b) row 11 states the true current state ('not redacted at HEAD: 161 occurrences in 82 prompt-log files; publish held until you answer') and row 10 adds that the scan does not check third-party project or job-search folder names. Do not publish the name as a workaround.",
   "acceptance_test": "After the fix, git grep -c -i with the name over the snapshot tree returns 0, or Chris's Inbox answer is 'show' and row 11 says so. Row 11 text matches the exporter's actual output on the same HEAD."},
  {"severity": "nit",
   "title": "Row 10 adds 'or any existing branch', which SNAPSHOT.md does not say",
   "evidence": "submission/NEEDS_CHRIS.md row 10: 'Never push this repo, its history or any existing branch.' deploy/SNAPSHOT.md: 'Never push the working repo or its history.'",
   "why_it_matters": "The added text is stricter and consistent with the rest of the file, so it does not conflict; the wording just differs from the source.",
   "fix": "Either add 'or any existing branch' to SNAPSHOT.md, or leave it as is.",
   "acceptance_test": "Both files carry the same prohibition wording, or the difference is accepted in the card note."},
  {"severity": "nit",
   "title": "Row 10 points to the one-time setup but does not spell the init command",
   "evidence": "submission/NEEDS_CHRIS.md row 10: 'one-time setup in deploy/SNAPSHOT.md'. deploy/SNAPSHOT.md 'One-time setup' section and make_public_snapshot.sh line 9 both give: python3 deploy/snapshot_tool.py init-patterns .",
   "why_it_matters": "The pointer is accurate. Chris has to open a second file to get the command.",
   "fix": "Optionally add the command to row 10.",
   "acceptance_test": "Row 10 names the command or the card note records that the pointer is accepted."}
 ],
 "whats_right": [
  "Row 10's push command matches deploy/SNAPSHOT.md verbatim, and the script's init -q -b main makes the main refspec valid.",
  "submission/NEEDS_CHRIS.md at dfd9b11 has no tailnet-shaped string, no <redacted-private>/10 address, no non-user email, and no private-pattern match (counts only).",
  "Row 11 matches the T-193 card (P1, needs_chris, default redacted), and the 29-commit work-email claim checks out."
 ],
 "questions_for_chris": [
  "Are the excerpts behind F1 verbatim material from a real third-party project or from a client matter? If yes, F1 becomes a blocker under dossier section 5.",
  "Should the prompt-log default redact the third-party project name as well as the paths? That is the T-193 decision."
 ]}
```
