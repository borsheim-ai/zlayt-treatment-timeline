# T-198 round 2 — privacy-compliance-reviewer (Nadia Farouk)

Scope: the outside-project-name rule and switch in `evals/finalize_prompt_log.py` and the rebuilt `submission/prompt-log/`, both at 8f78874 (reviewed together with T-187 r4). The snapshot half of the AC ("the snapshot built by deploy/make_public_snapshot.sh greps 0") belongs to T-199, which is `in_progress` with uncommitted `deploy/` edits. I noted it and did not grade it. The name is never written here; I refer to it as `<redacted>`.

**Verdict: changes (2 major, 1 nit).**

- **F1, the name survives in two published transcripts.** In `session-6ddf8076-a29d1318-privacy-review-t-187-r3.md:1606` it appears as two halves joined by a regex `\\*`. In `session-6ddf8076-a2cabe7e-privacy-check-t-198.md:980`, the T-198 round-1 review session, it appears as a two-element tuple `("<half>","<half>")`. The D-070 view removes quotes, `+`, whitespace and backslashes, but not `*` or `,`, so both stay readable. The finalize self-test and `privacy_tree_scan.py` report 0. The transcript the brief names, `session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md`, is clean. Its only near-hits are Chris's public name and the public gmail.
- **F2, the switch is not the single switch.** The local `deploy/.private_patterns` also lists the name as a `term` line. The T-198 card note says it was added so the snapshot greps 0. Finalize loads `term` into `PRIVATE_TERM_RX`, which runs before the path rules and before `OUTSIDE_RX`. As a result:
  - every replacement of the name is `<redacted-private>`, counted as "private network detail" (REDACTIONS.md has no outside class);
  - `REDACT_OUTSIDE_PROJECT_NAME = False` still masks every plain form;
  - 44 home paths into the outside project keep their sub-folder, file and call-prep suffix, because `HOME_RXS`/`PERSONAL_RXS` cannot match after the name is already a marker.

  The README/self-test half of the switch works: with the switch False, the README says "six", item 7 disappears, and the self-test group is dropped.
- **Nit:** the README item 7 "any form ... JSON or regex-escaped" overclaim from round 1 is still in 8f78874. a44cfa7 narrows it (diff read), so check it at the next build.

```json
{"card": "T-198", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "evals/finalize_prompt_log.py (REDACT_OUTSIDE_PROJECT_NAME, OUTSIDE_RX, term loading, rule order) and submission/prompt-log/ at 8f78874; a44cfa7 README wording noted; snapshot half (T-199, in_progress) noted, not graded",
 "exercised": [
  "python3 tools/board.py show T-198 / T-187 / T-199; read reviews/T-198-privacy-compliance.md, reviews/T-187-privacy-compliance-r3.md, D-070, both handoffs",
  "python3 -I artifacts/review-evidence/T-198-r2-switch.py 8f78874: loads finalize from the commit in-process with the switch True and False and scrubs 17 synthetic spellings of the name built at run time. True: prose/lower/upper/snake/kebab/camel/plus-split/backslash/spaced -> markers ['<redacted-private>'] class 'private network detail'; regex-star, tuple-split, comma-space, hyphen-split, zero-width -> name left; \\u/%/&# -> unchanged (not decoded). False: identical scrub results; README block 'six', item 7 absent; self-test outside group off. 'outside name also listed as kind term (normalized): True'",
  "python3 -I artifacts/review-evidence/T-187-r4-focus.py 8f78874: outside-plain n=0; outside-gapped n=2 files=2 (a29d1318:1606, a2cabe7e:980)",
  "python3 -I artifacts/review-evidence/T-187-r4-sweep.py 8f78874 --shapes over the whole folder: term exact-A hits only in those two files (shapes '<5 letters>\\\\*<5 letters>' and '<5 letters>\",\"<5 letters>'); every other term-kind near-hit is an English dictionary word (T-187-r4-fpwords.py)",
  "python3 -I artifacts/review-evidence/T-187-r4-sweep.py 8f78874 --ctx all on transcripts/session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md: no outside-name hit in any view; email-kind hits are the public name and public gmail only",
  "git show 8f78874:submission/prompt-log/REDACTIONS.md: no outside-name class row; header 'edit classes 1 to 6'",
  "python3 evals/privacy_tree_scan.py --dir submission/prompt-log -> '1175 text file(s) checked, 0 with hits'",
  "git diff 8f78874 a44cfa7 -- submission/prompt-log/README.md evals/finalize_prompt_log.py: item 7 wording narrowed to 'in these forms ... Unicode, percent or entity escapes and zero-width characters are not decoded'"
 ],
 "verdict": "changes",
 "scores": {"name redacted in every form in the prompt log": 2, "one switch flips it (AC)": 1, "README item 7 accuracy": 2, "rule code holds no name or fragment": 5},
 "findings": [
  {"severity": "major",
   "title": "Outside project name still readable in two published transcripts (regex-quantifier join and tuple split); self-test and tree scan report 0",
   "evidence": "T-187-r4-focus.py 8f78874: outside-gapped n=2: submission/prompt-log/transcripts/session-6ddf8076-a29d1318-privacy-review-t-187-r3.md:1606 (two halves joined by a regex backslash-star) and session-6ddf8076-a2cabe7e-privacy-check-t-198.md:980 (tuple of two quoted halves separated by a comma). T-198-r2-switch.py reproduces both forms as 'name_left=True' with the switch on. 'python3 evals/privacy_tree_scan.py --dir submission/prompt-log' -> 0 with hits.",
   "why_it_matters": "The AC says 'case-insensitive, all forms' and 'greps 0'. A reader recovers the name at a glance from either line. This is the same failure class as round 1 (split literal in a review session's own transcript), now through '*' and ',' instead of '+'. Until Chris answers T-193 the default is that the name is not published.",
   "fix": "Match the name, like every term of 8+ alphanumerics, on an alphanumeric-only casefolded view, so that any run of non-alphanumerics inside it is ignored. Map spans back. Use the same view in self_test and privacy_tree_scan.py. Rebuild after this review, because this session also carries split forms in its tool calls.",
   "acceptance_test": "T-187-r4-focus.py on the rebuilt folder: outside-gapped n=0 and outside-plain n=0. T-198-r2-switch.py with the switch True: regex-star, tuple-split, comma-space, hyphen-split and zero-width all name_left=False."},
  {"severity": "major",
   "title": "REDACT_OUTSIDE_PROJECT_NAME is not the single switch: the name is also a 'term' in the local patterns file, so it is masked as <redacted-private> under either setting and path rules are bypassed",
   "evidence": "T-198-r2-switch.py 8f78874: 'outside name also listed as kind term (normalized): True'. With REDACT_OUTSIDE_PROJECT_NAME=False, prose/case/snake/kebab/camel/plus/backslash forms still give markers=['<redacted-private>'] (class 'private network detail ...'). REDACTIONS.md at 8f78874 has no outside-name class, so all replacements fall under private network. finalize_prompt_log.py:131 PRIVATE_TERM_RX = term_rx(TERMS['email'] + TERMS['term']) runs in scrub() before PERSONAL_RXS/HOME_RXS/OUTSIDE_RX. Result: 44 occurrences in 10 files of '/Users/<name>/<redacted-private>/<sub-folder>/<file>' and '~/<redacted-private>-<suffix>' (e.g. board-activity.jsonl:1820-1821) where README edit 3 promises <home-path>/<personal file>. T-198 card note: the term line was added to the local file so the snapshot greps 0.",
   "why_it_matters": "AC: 'the rule is one switch so Chris's show answer flips it'. If Chris says 'show', flipping the tracked switch silently changes nothing in the content and the README then says six kinds of edit while the name is still masked under a mislabelled class. Meanwhile the rule order publishes the outside project's sub-folder and file names and the call-prep suffix that edits 3/4 say are masked.",
   "fix": "In finalize, subtract every '#@outside' value (normalized) from the 'term' list before building PRIVATE_TERM_RX, so the name is handled only by OUTSIDE_RX, which runs after the path rules. Have T-199 give the snapshot an 'outside' kind tied to the same switch and stop adding the name as a 'term'. Add a test that runs scrub() with the switch False on a run-time-built sentence and asserts the name is present, and with True asserts '<outside project>'.",
   "acceptance_test": "T-198-r2-switch.py on the new commit: switch True gives markers=['<outside project>'] for plain forms, and switch False gives name_left=True for prose. After rebuild, REDACTIONS.md has an outside-name class with count > 0, and grep -rcE '(/Users/[a-z]+/|~/)<redacted-private>' submission/prompt-log totals 0."},
  {"severity": "nit",
   "title": "README item 7 'any form ... JSON or regex-escaped' overclaim (round-1 minor) still in 8f78874; narrowed in a44cfa7",
   "evidence": "git show 8f78874:submission/prompt-log/README.md item 7: 'in any letter case and any form: a path segment, a file-name slug, prose, or a JSON or regex-escaped spelling'; T-198-r2-switch.py: \\u, %XX and &#N; forms are not replaced. git diff 8f78874 a44cfa7 narrows the sentence and says these are not decoded.",
   "why_it_matters": "The wording now matches the code at a44cfa7. After the F1 fix it must also stop listing 'quoted pieces joined with +' as the only split form, or list what the new view folds.",
   "fix": "Regenerate item 7 from the F1 rule when it lands.",
   "acceptance_test": "The README item 7 sentence lists exactly the forms that T-198-r2-switch.py shows as name_left=False."}
 ],
 "whats_right": [
  "The rule code holds no name or fragment; the name is read at run time from the git-ignored file, and plain, case, snake/kebab/camel, quote-plus-split and backslash forms are 0 in the folder.",
  "Flipping the switch correctly regenerates the README (seven to six kinds, item 7 removed) and drops the self-test group.",
  "The QA transcript named in the brief (session-6ddf8076-a8986e29-qa-t-198-outside-name-redaction.md) is clean under every view I ran, including its former split-literal lines."
 ],
 "questions_for_chris": []}
```
