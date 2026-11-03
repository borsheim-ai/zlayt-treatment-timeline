# T-198 review: outside-project-name redaction at commit f5f1be9 (privacy-compliance-reviewer)

**Verdict: changes.** No blocker. One major: the rule does not remove the name in every form the card claims. The committed prompt log still
discloses it through a split string literal in one transcript (two lines). The bare-name checks pass. The switch exists and the README lists the rule.

**Model note.** This review was run as `claude-haiku-5-5`, the model I am actually running as. My dossier expects `claude-opus-5-5` for judgment
reviews. The same mismatch was raised in T-195. The orchestrator should decide whether this counts as the judgment review.

**Scope.** Commit `f5f1be9` only. I read `git show f5f1be9:...` and `git ls-tree`/`git show f5f1be9:<path>` for every check. The working tree is at `9ab8cae`
and was not reviewed. The snapshot side (`deploy/`, `snapshot_tool.py`) is not graded here; it moves to the release card, as briefed.
I did not print or write the outside-project name anywhere in this review. Where a form is quoted, letters are masked.

## Brief checks

| Brief item | Result |
|---|---|
| 1. `submission/prompt-log/` at f5f1be9 has 0 occurrences of the name in any form (case-insensitive, escaped, path) | **FAIL for one form.** Plain, case-insensitive, backslash-escaped and file-name forms: 0. A split string literal (`"<5 letters>" + "<5 letters>"`): 2 lines in 1 file. See F1. |
| 2. Switch `REDACT_OUTSIDE_PROJECT_NAME` exists in `evals/finalize_prompt_log.py` | **PASS.** Line 52 at f5f1be9 is `REDACT_OUTSIDE_PROJECT_NAME = True`. It is read in `scrub()` (line 176), in the README writer (line 240) and in `self_test()` (line 302). |
| 3. README lists the rule | **PASS.** `submission/prompt-log/README.md:16` is item 7, "Outside project name redacted until Chris decides", and names the switch. The top-level `README.md` does not mention it (release-owned; not graded here). |

## What I exercised

Checker: `artifacts/review-evidence/T-198-checks.py` (run with `python3 -I <file> <scratchpad>`). It derives the name from the finalizer's
assembly line at f5f1be9 in memory. It prints counts and labels only, and the self-test output is captured so that no match text can print.
Output (run 2, verbatim):

```
derived name: length=10 (value not printed)
[before-rule] f5f1be9^ submission/prompt-log: tracked files=1128
[before-rule]   plain case-insensitive occurrences=171 in files=82
[after-rule] f5f1be9 submission/prompt-log: tracked files=1159
[after-rule]   plain case-insensitive occurrences=0 in files=0
[after-rule]   broad-form occurrences (separators/escapes/zero-width/%/&#)=2 in files=1
[after-rule]   file names: plain=0 broad=0
[after-rule]   marker '<outside project>' occurrences=342 in files=89
[switch] REDACT_OUTSIDE_PROJECT_NAME at f5f1be9 = True
[self-test] finalizer self_test() at f5f1be9 on the extracted committed prompt log: failures=0
[scrub]   plain: survives=False
[scrub]   lower-case: survives=False
[scrub]   upper-case: survives=False
[scrub]   backslash inside: survives=False
[scrub]   json unicode escape of first letter: survives=True
[scrub]   percent-encoded first letter: survives=True
[scrub]   hyphen inside (slug): survives=True
[scrub]   underscore inside (snake): survives=True
[scrub]   space inside (prose): survives=True
[scrub]   zero-width space inside: survives=True
[scrub]   html numeric entity of first letter: survives=True
[scrub]   split into two string literals (source assembly): survives=True
[switch-off] plain form survives with switch False: True
[switch-off] self_test() with switch False: failures=0 (no exception)
[readme] switch name occurrences in README at f5f1be9: 1
[readme] item-7 heading present: True
[readme] 'any form' wording present: True
[readme] top-level README.md at f5f1be9 mentions switch: False
```

Other commands:
- `git show f5f1be9:evals/finalize_prompt_log.py` lines 47-55 and 176-178, 240, 302 (read).
- `git show f5f1be9:submission/prompt-log/README.md` lines 8 and 16 (read). Item 7 says "replaced wherever it appears, in any letter case and any form: a path segment, a file-name slug, prose, or a JSON or regex-escaped spelling".
- Locate of the one normalised-only hit (`T-198-locate.py`, scratchpad, letters masked): `submission/prompt-log/transcripts/session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md` lines 548 and 556. Line 556 has the shape `53:_······· = "·····" + "·····"  # ...` (the finalizer's assembly line, reproduced verbatim).
- Marker count excluding the README: 341 occurrences in 88 files, which matches the README's "341 occurrences in 88 files" (the README itself is excluded by the edit's scope).
- `python3 tools/board.py validate` (read-only): `ok (200 file(s))`.
- `git ls-tree -r f5f1be9 -- submission/prompt-log`: file names checked for the name in plain and broad form: 0.

## Findings

**F1 (major): split string literal discloses the name in the committed transcript; the rule and self-test cannot see it.**
- Evidence: `submission/prompt-log/transcripts/session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md` lines 548 and 556 at f5f1be9. Line 556 is the finalizer's own assembly line (`evals/finalize_prompt_log.py:53` at f5f1be9), reproduced verbatim. The name is written as two 5-letter string literals joined by ` + `. Checker row "split into two string literals" reports `survives=True`. The after-rule broad-form count is 2 in 1 file.
- Why it matters: the rule is meant to remove the name "in any form" (README item 7). The split form lets a reader rebuild the name with one concatenation, so the committed prompt log still discloses it. The card's literal grep (`grep -ri` = 0) passes, so the acceptance test as written does not catch it. The self-test also misses it: `scrub()` strips only backslashes (`sub_normalized`), and `self_test()` checks the plain pattern after backslash removal. The next rebuild will not catch it either. The assembly trick in `evals/finalize_prompt_log.py:53` only hides the name in the source file; it does not stop the transcript from quoting that line.
- Severity basis: the material is the name of one other project, plus a source line from this repo. It is not PHI or client data on the evidence available, and it is the same category as T-195 F1, which I rated major. It would become a blocker if Chris's answer or the source shows client or employer-confidential material.
- Fix: (a) make the redaction normalise before matching, as the checker does: strip quotes, `+`, whitespace, separators, backslashes and zero-width characters, and decode `\uXXXX`, `%XX` and `&#N;`. Use that in `scrub()` and in `self_test()`. (b) Rebuild the prompt log so the two literal lines in the T-198 transcript become `<outside project>`. (c) Do not put the name, or its pieces, in any new text, including the fix text and the self-test.
- Acceptance test: `python3 -I artifacts/review-evidence/T-198-checks.py <scratchpad>` at the fix commit shows `[after-rule] broad-form occurrences ... =0 in files=0`, and the row "split into two string literals" shows `survives=False`.

**F2 (minor): "any form" is wider than what the rule removes.**
- Evidence: `submission/prompt-log/README.md:16` says "in any letter case and any form: a path segment, a file-name slug, prose, or a JSON or regex-escaped spelling"; `evals/finalize_prompt_log.py:48-49` (f5f1be9) says "any case, any form (path segment, prose, JSON/regex-escaped)". Checker rows with `survives=True` at f5f1be9: JSON `\uXXXX` escape, `%XX` percent-encoding, HTML numeric entity, hyphen, underscore, space and zero-width insertion.
- Why it matters: the README is what Chris reads to decide the T-193 switch. It says more than the code does. Today the folder has no such forms apart from F1, so the impact is latent: a later rebuild that quotes a JSON-escaped spelling would pass both the rule and the self-test.
- Fix: use the same normaliser as F1 in `scrub()` and `self_test()`, so the claim holds. Otherwise narrow the README and the comment to "any letter case, and backslash escapes".
- Acceptance test: every row of the checker's form table shows `survives=False`, or the README text matches the rows that do.

**F3 (nit): bare substring also redacts an ordinary English word.**
- Evidence: `evals/finalize_prompt_log.py:54` (f5f1be9) `OUTSIDE_RX = re.compile(_OUTSIDE, re.I)` with no word boundaries, by design ("matches inside paths, slugs, snake/kebab/camel forms"). The name is also a common word, so prose in transcripts is altered.
- Why it matters: over-redaction of ordinary prose is a fidelity cost, not a leak. Chris should know it when he answers T-193.
- Fix: none required. Note it in the T-193 answer.

## What is right

1. The switch is one line (`evals/finalize_prompt_log.py:52`). Flipping it to `False` makes the plain form pass through (`switch-off ... survives: True`) and `self_test()` still returns 0 failures without an exception.
2. Plain, case-insensitive, backslash-escaped and file-name forms are 0 across the 1159 tracked files under `submission/prompt-log/` at f5f1be9 (171 occurrences in 82 files before the rule).
3. The README's marker count is right: 341 occurrences in 88 files, excluding the README itself.

## Questions for Chris

- Is the name of the outside project itself confidential (third-party or employer), or only the excerpts it came from? If the excerpts are client material, F1 becomes a blocker under dossier §5.
- The dossier expects `claude-opus-5-5` for judgment reviews. This run was `claude-haiku-5-5`. Does the orchestrator need an Opus rerun of T-198?

```json
{"card": "T-198", "persona": "privacy-compliance-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f5f1be9 only: submission/prompt-log/ (1159 tracked files), evals/finalize_prompt_log.py (REDACT_OUTSIDE_PROJECT_NAME, scrub, self_test), submission/prompt-log/README.md item 7. Snapshot side not graded (release card). Working tree at 9ab8cae not reviewed.",
 "exercised": [
  "git show f5f1be9:evals/finalize_prompt_log.py (lines 1-55, 136-182, 291-332 read; saved to scratchpad) and git archive f5f1be9 evals tools submission/prompt-log extracted to scratchpad for the self-test",
  "git show f5f1be9:submission/prompt-log/README.md lines 8 and 16; grep of README for the switch name (1 occurrence) and for 'any form' wording",
  "git ls-tree -r --name-only f5f1be9 -- submission/prompt-log (1159 files); file names checked for the name in plain and broad form: 0",
  "python3 -I artifacts/review-evidence/T-198-checks.py <scratchpad> (counts, switch value, self_test at f5f1be9 = 0 failures, scrub() on 12 forms of the name, switch-off run, README checks); output in the review body",
  "python3 -I <scratchpad>/T198-locate.py (letters masked): locates the one normalised-only hit at submission/prompt-log/transcripts/session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md lines 548 and 556",
  "marker count excluding README: 341 occurrences in 88 files (matches README item 7)",
  "python3 tools/board.py validate (read-only): ok (200 file(s))",
  "board card T-198 via python3 tools/board.py show T-198 and git show f5f1be9 (commit stat)",
  "reviewer memory (MEMORY.md, prompt-log-review.md, recurring-findings.md) and personas/privacy-compliance.md read in full"
 ],
 "verdict": "changes",
 "scores": {"prompt_log_no_name_any_form": 2, "switch_exists_and_flips": 5, "readme_lists_rule": 4, "rule_covers_stated_forms": 2, "self_test_catches_name_forms": 2},
 "findings": [
  {"severity": "major",
   "title": "Split string literal discloses the outside-project name in a committed transcript; the rule and self-test do not catch it",
   "evidence": "submission/prompt-log/transcripts/session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md:548 and :556 at f5f1be9 (line 556 shape with letters masked: `53:_······· = \"·····\" + \"·····\"`, a verbatim copy of evals/finalize_prompt_log.py:53 at f5f1be9). checker: after-rule plain=0 files=0; broad-form=2 files=1; split-literal row survives=True. self_test() at f5f1be9 = 0 failures (plain pattern only).",
   "why_it_matters": "README item 7 says the name is replaced in any form. A split literal lets a reader rebuild the name with one concatenation, so the committed prompt log still discloses it. The literal grep (= 0) passes, so the card's acceptance test cannot see it, and the self-test cannot catch it on the next rebuild. Not PHI or client data on current evidence; same category as T-195 F1 (major). Becomes a blocker if the material is client or employer-confidential (Chris to confirm).",
   "fix": "(a) In evals/finalize_prompt_log.py, normalise before matching in scrub() and self_test(): strip quotes, '+', whitespace, separators, backslashes and zero-width characters; decode \\uXXXX, %XX and &#N;. (b) Rebuild the prompt log so the two literal lines in the T-198 transcript become <outside project>. (c) Put neither the name nor its pieces in any new text.",
   "acceptance_test": "python3 -I artifacts/review-evidence/T-198-checks.py <scratchpad> at the fix commit: '[after-rule] broad-form occurrences ... =0 in files=0'; row 'split into two string literals' shows survives=False."},
  {"severity": "minor",
   "title": "'Any form' is wider than what the rule removes (JSON/percent/entity escapes, separators, zero-width)",
   "evidence": "submission/prompt-log/README.md:16 (f5f1be9): 'replaced wherever it appears, in any letter case and any form: a path segment, a file-name slug, prose, or a JSON or regex-escaped spelling'. evals/finalize_prompt_log.py:48-49 (f5f1be9): 'any case, any form (path segment, prose, JSON/regex-escaped)'. checker scrub() rows with survives=True: JSON \\uXXXX, %XX, HTML numeric entity, hyphen, underscore, space, zero-width insertion.",
   "why_it_matters": "The README is what Chris reads to decide the T-193 switch, and it says more than the code does. No such form is present in the folder apart from F1, so the impact is latent; a later rebuild that quotes a JSON-escaped spelling would pass both the rule and the self-test.",
   "fix": "Use the F1 normaliser in scrub() and self_test(), so the claim holds; or narrow README item 7 and the finalizer comment to 'any letter case, and backslash escapes'.",
   "acceptance_test": "Every row of the checker's form table shows survives=False, or the README text matches the rows that do."},
  {"severity": "nit",
   "title": "Bare substring also redacts an ordinary English word",
   "evidence": "evals/finalize_prompt_log.py:54 (f5f1be9): OUTSIDE_RX = re.compile(_OUTSIDE, re.I), no word boundaries (comment: 'matches inside paths, slugs, snake/kebab/camel forms').",
   "why_it_matters": "Over-redaction of ordinary prose is a fidelity cost, not a leak. Chris should know it when he answers T-193.",
   "fix": "None required; note it in the T-193 answer.",
   "acceptance_test": "None."}
 ],
 "whats_right": [
  "The switch is one line (evals/finalize_prompt_log.py:52, = True) and drives scrub(), the README writer and self_test(); with it False, the plain form passes and self_test() runs with 0 failures and no exception.",
  "Plain, case-insensitive, backslash-escaped and file-name forms: 0 across the 1159 tracked files under submission/prompt-log/ at f5f1be9 (171 occurrences in 82 files before the rule).",
  "README item 7 (submission/prompt-log/README.md:16) names the rule and the switch, and its count (341 occurrences in 88 files) matches the folder excluding the README."
 ],
 "questions_for_chris": [
  "Is the outside project's name itself confidential (third-party or employer), or only the excerpts it came from? If the excerpts are client material, F1 becomes a blocker under dossier section 5.",
  "The dossier expects claude-opus-5-5 for judgment reviews; this run was claude-haiku-5-5. Does T-198 need an Opus rerun?"
 ]}
```
