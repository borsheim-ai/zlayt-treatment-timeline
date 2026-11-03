# T-133 r3 review (staff-engineer-reviewer), lexicon deny forms and history_significant_for

Pinned to HEAD 4065ef2 (f939ccb: T-133 r2 lexicon fix; 4065ef2: calibration regenerated from a clean worktree of f939ccb). Reviewed from `git archive 4065ef2`, extracted to the scratchpad directory T-133-r3-archive-4065ef2 (lexicon.yaml sha256 25920bf6..., equal to HEAD). The pre-r2 comparison uses the r1 archive of 1218b2e (lexicon sha256 30f5c65f..., equal to `git show 1218b2e:app/llm/lexicon.yaml`). The main tree was not edited.

Verdict: **changes** (no blocker; one major, two minors, one design minor).

The r2 F1 request is met for the forms it named: the four named sentences and 15 HPI or header sentences are quiet, and the positives still flag. F2, F4 and F6 are closed. The r2 fix, however, introduced a regression. "Past history:", "Medical history:", "Surgical history:" and "Past medical history: significant for X" lost the prior-condition flag they raised before f939ccb. Nothing in the unit tests or the golden set pins them. The F3 fix suppresses the flag instead of showing the condition, which leaves a recall gap on a semicolon form. F5 (live eval evidence) is still open.

## Status of the r2 items

| r2 item | Status at 4065ef2 | Evidence |
|---|---|---|
| F1 major, HPI narratives flag | Fixed for the named forms. The fix caused a regression (new F1). | probe_r3 output: 4 named sentences and HPI01 to HPI15 quiet on HEAD (flagged on 1218b2e) |
| F2 minor, attribution deny untested | Closed | mutant A (drop deny, denying from attribution_word): 1 failed |
| F3 minor, excerpt with no condition | Resolved by suppression, not extension. Recall gap (new F2). | probe: 'History reviewed; significant for diabetes.' quiet on HEAD, FLAG 'History reviewed;' on 1218b2e |
| F4 minor, deny has no source | Closed | NegEx genConText/negex_triggers.txt lines 24-26 (denied, denies, denying [PREN]); pyConText KB lexical_kb_05042016.yml lines 658-676 (Lex: deny, denies, denied, denying); both URLs in lexicon.yaml:51-52 |
| F5 minor, fixture-only eval | Open | evals/reports/20261102T123428Z.md:3 'backend fixture'; no claude-cli report newer than the lexicon change |
| F6 nit, unit count | Closed | f939ccb collects 3316 tests = the card's 3315 passed + 1 skipped (I did not run the f939ccb suite) |

## Checks against the brief

1. **Bare History and HPI narratives do not flag pre_existing.** Pass for every form I probed on HEAD (see Exercised). The four named sentences from r2 F1 and HPI01 to HPI15 are quiet. Two attributed forms still flag (see F4).
2. **Hits still flag.** Pass. These flag on HEAD: "History provided by wife, notable for lumbar strain." (quote is the full sentence), "History significant for diabetes.", "History is significant for prior assault.", "History is notable for a 2019 lumbar strain.", "Medical history remarkable for prior neck surgery.", "History provided by husband; notable for cervical strain.", "History obtained via interpreter, significant for chronic low back pain.". "History provided by wife." (attribution only) is quiet.
3. **Deny forms count as negation.** Pass. `is_negation_word` is True for deny, denies, denied and denying, and False for declined and declines. `dropped_qualifiers('Numbness.', 'Patient and wife deny numbness.')` returns ['negation']. "Patient and wife deny history significant for neck injury.", "Denying history significant for neck injury." and "Patient denies history significant for neck injury." are quiet.
4. **r1 minors.** See the status table above.
5. **Unit suite.** Pass. `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider` on the HEAD archive: `3318 passed, 4 skipped in 181.87s (0:03:01)`, exit 0. HEAD includes 5fb338d (T-134), which adds tests; the T-133 count is the f939ccb count above.

## Mutation spot-checks (scratch copies of the HEAD archive, not committed)

| Mutant | Result on tests/unit/test_t133_lexicon.py |
|---|---|
| A: drop deny and denying from attribution_word (lexicon.yaml:1404) | 1 failed (test_a_deny_summary_carries_the_quotes_attribution). F2 closed. |
| B: drop the header look-ahead after the history word (lexicon.yaml:185) | 4 failed |
| C: drop deny from negation_word (lexicon.yaml:1445) | 2 failed |
| D: drop denying from negation.pre_cues (lexicon.yaml:55) | 2 failed |

## Findings

**F1 (major). Past, Medical and Surgical history headers, and "Past medical history: significant for X", lost the prior-condition flag in f939ccb.**
Repro (both archives, same probe script, `flags.lexicon_flags`):
- "Past history: significant for lumbar strain." 1218b2e: pre_existing flag, excerpt the full sentence. HEAD: no flag.
- "Medical history: significant for diabetes." 1218b2e: flag. HEAD: no flag.
- "Surgical history: notable for L4-5 laminectomy." 1218b2e: flag. HEAD: no flag.
- "Past medical history: significant for diabetes." 1218b2e: flag (history_significant_for). HEAD: no flag.
Cause: the look-ahead `(?!\s*[:\-])` at app/llm/lexicon.yaml:185 applies to every history word, not only a bare "History:" header, so it also excludes "history:" after "Past", "Medical" and "Surgical". The rationale at app/llm/lexicon.yaml:181 says past history "has its own header entries, pmh_psh_section and hx_abbrev". That is not true for these forms. pmh_psh_section (lexicon.yaml:202-208) matches "Past medical history:" with the regex but is strength low, and app/backend/lexicon_scan.py:11 and :196 drop anything below medium, so it raises no flag. hx_abbrev (lexicon.yaml:142-143) covers Hx, h/o and PHx only. Nothing else raises a flag for these forms. No test covers them: `grep -n -i "past history\|medical history:\|surgical history" tests/unit/test_t133_lexicon.py` finds only a section comment (line 145). The golden sample and spec text contain none of these headers, so the eval does not catch it either.
Why it matters: the entry exists to flag prior conditions in chart history, and the r2 fix removed the flag from a standard PMH idiom that the pre-r2 build raised. The lexicon is the floor (app/backend/flags.py:243: "A failed or missed model call leaves the lexicon flags in place"), so when the model also misses, the adjuster gets no flag. Rated major, not blocker: the record text is unchanged, the model pass may still flag the sentence, and I did not test that path.
Fix: scope the header exclusion to a bare "History" by adding look-behinds for past, medical and surgical before the history word, for example `(?<!past\s)(?<!medical\s)(?<!surgical\s)`, and keep the header look-ahead for a bare "History:". Add these four forms to the hit list in tests/unit/test_t133_lexicon.py.
Acceptance test: lexicon_scan.scan and flags.lexicon_flags return a pre_existing flag whose excerpt is the full sentence for "Past history: significant for lumbar strain.", "Medical history: significant for diabetes.", "Surgical history: notable for L4-5 laminectomy." and "Past medical history: significant for diabetes."; the four r2 F1 sentences and HPI01 to HPI15 stay quiet; a test fails if the past, medical or surgical look-behind is removed.

**F2 (minor). A semicolon after a bare history word now suppresses the flag, which drops a true prior condition.**
Evidence: HEAD `flags.lexicon_flags` on "History reviewed; significant for diabetes." returns [] (the 1218b2e build returned a flag whose excerpt was "History reviewed;"). "Pain 6/10. History reviewed; notable for pain on cough." returns [] on HEAD. The lexicon comment at app/llm/lexicon.yaml:184 and the test at tests/unit/test_t133_lexicon.py:193-196 pin the suppression. The r1 F3 acceptance test asked for an excerpt that contains the condition, which is not what this build returns.
Why it matters: the no-conditionless-quote goal is met, but the trade is a silent miss on a semicolon form that can carry a true prior condition. The yaml comment discloses the choice, but the card does not record it as a scope cut for Chris.
Fix: either extend the flag unit to the condition clause after a non-attribution semicolon, as the r1 fix proposed, or record a SCOPE_CUTS row for the lost form and get Chris's decision.
Acceptance test: flags.lexicon_flags on "History reviewed; significant for diabetes." returns one pre_existing flag whose excerpt contains "significant for diabetes", or a SCOPE_CUTS row names the form and the test pins that decision.

**F3 (minor). Eval evidence for the lexicon change is still fixture-only (r2 F5, open).**
Evidence: evals/reports/20261102T123428Z.md:3 reads "backend `fixture`", and line 6 says determinism_3run and unsupported_count_3run need a live backend. The newer evals/reports/20261102T123652Z.md is also fixture and dirty. The claude-cli reports in evals/reports (controls-20261102T063331Z.md, controls-20261102T075238Z.md, determinism-diagnosis.md) predate the lexicon change.
Why it matters: criterion 18 needs a re-run eval report for a lexicon change. The path exists, but the live determinism and unsupported-count numbers are not measured.
Fix: run the live claude-cli eval on the T-133 commit and cite its report on the card before the M3 gate.
Acceptance test: a report under evals/reports/ has backend `claude-cli`, numeric determinism_3run and unsupported_count_3run, and a source commit at or after f939ccb, and the card cites it.

**F4 (minor, design; not a spec violation). Bare History narratives with the patient as the source still flag.**
Evidence: HEAD `flags.lexicon_flags` returns a pre_existing flag for "History obtained from patient, notable for neck pain.", "History per patient: significant for neck pain." and "History (per patient): notable for neck pain.". Each hit is history_significant_for. The r2 fix quiets the same sentence only when an index cue follows ("since the crash").
Why it matters: these are HPI-shaped sentences, and the brief asks for HPI narratives not to flag. The AC's own example "History provided by wife, notable for lumbar strain" flags by the same rule, so the two are consistent. Whether the patient as source should be excluded is a product decision, not a reviewer call.
Fix: Chris decides. If the patient is excluded, add a suppressor for patient or pt as the source when no past-history cue is present. If not, say so in the entry rationale.
Acceptance test: whichever decision is taken is pinned by a test next to the existing wife-source test in tests/unit/test_t133_lexicon.py.

## Probe output (verbatim, HEAD 4065ef2 archive; pre-r2 1218b2e in parentheses where it differs)

- `[F1-a] scan=quiet ... <= 'History: 45-year-old male, significant for neck pain.'` (1218b2e: FLAG)
- `[F1-c] scan=quiet ... <= 'Chief complaint and history: notable for neck pain.'` (1218b2e: FLAG)
- `[HPI06] scan=quiet ... <= 'History reviewed; notable for pain on cough.'` (1218b2e: FLAG 'History reviewed;')
- `[HPI15] scan=quiet ... <= 'History: 37-year-old woman, notable for lumbar pain after a fall at work.'` (1218b2e: FLAG)
- `[POS-wife] scan=FLAG ids=['history_significant_for'] unit=['History provided by wife, notable for lumbar strain.']`
- `[CTL-wife-only] scan=quiet ... <= 'History provided by wife.'`
- `[REG-past-hdr] scan=quiet ... <= 'Past history: significant for lumbar strain.'` (1218b2e: FLAG)
- `Past medical history: significant for diabetes.` HEAD `[]`; 1218b2e `[('pre_existing', 'pre_existing', 'Past medical history: significant for diabetes.')]`
- `is_negation_word deny True / denies True / denied True / denying True / declined False / declines False`
- `dropped deny->none: ['negation']`; `negation_words: ['deny', 'denying']`
- `History obtained from patient, notable for neck pain.` HEAD `history_significant_for` FLAG (F4)

## Exercised

- `python3 tools/board.py show T-133` (card, notes and handoff read)
- `git log --oneline -6`, `git show 4065ef2 --stat`, `git diff e79c3aa^ HEAD -- app/llm/lexicon.yaml`, `git show 4065ef2:tests/unit/test_t133_lexicon.py` (read in full)
- `git archive 4065ef2 | tar -x` to scratchpad T-133-r3-archive-4065ef2; sha256 of lexicon.yaml equals `git show 4065ef2:app/llm/lexicon.yaml`
- `git archive f939ccb | tar -x` to scratchpad T-133-r3-archive-f939ccb; `pytest tests/unit --collect-only -q`: 3316 tests collected (f939ccb), 3322 (HEAD)
- `.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider` on the HEAD archive: 3318 passed, 4 skipped in 181.87s, exit 0
- Probe scripts probe_r3.py and probe_flags.py and scan_all.py (scratchpad T-133-r3-scripts) run on the HEAD archive and the 1218b2e archive (T-133-r1-archive, lexicon sha verified). 15 HPI and header sentences, 4 named sentences, 8 positives and controls, 7 header variants, 5 negation probes, and 10 more HPI variants (em dash, per patient, taken from patient, reviewed with period, Hx, history of, unremarkable, index cue after the condition)
- Mutants A to D built from the HEAD archive with exact-count assertions (scratchpad T-133-r3-mutA to mutD); `.venv/bin/python -I -m pytest tests/unit/test_t133_lexicon.py -q` on each
- `research/lexicon_selfcheck.py` on the HEAD archive: `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115`, `RESULT: PASS`
- `python -I -c` runpy of `app.pipeline evals/golden/sample.txt` with LLM_BACKEND=fixture, twice on HEAD (identical) and once on 1218b2e (identical to HEAD): `Status: done backend: fixture records: 9 entries: 9 flags: 10 amounts: 3`
- `curl` of raw.githubusercontent.com chapmanbe/negex genConText/negex_triggers.txt and chapmanbe/pyConTextNLP KB/lexical_kb_05042016.yml (both HTTP 200); grep of deny lines (NegEx 24-26; pyConText 658-676)
- `head -4` of evals/reports/20261102T123428Z.md and 20261102T123652Z.md; `git log -- evals/reports/20261102T123428Z.md`; grep of evals/reports for claude-cli
- grep of tests/unit/test_t133_lexicon.py and evals/golden, spec for past, medical and surgical history headers (no matches in tests or golden or spec)
- Not run: the live claude-cli backend (no network LLM calls from the reviewer); the f939ccb unit suite (count via collection only). Outside my lens: whether a pre_existing flag is clinically right, and whether the model pass recovers the F1 forms.

## Right

- The r2 named HPI forms, 15 further HPI and header sentences, and the four named sentences stay quiet on HEAD, and the wife, diabetes, prior-assault and 2019 forms still flag.
- Deny is a negation everywhere it is read (negation_word, pre_cues, field_answer, attribution_word, is_negation_word), and each form now has an opened source with its URL in the yaml.
- Sample case output is identical between the pre-r2 and HEAD builds, across two runs, and the lexicon selfcheck is PASS 115/115.

## Machine-readable record

```json
{"card": "T-133", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD 4065ef2 (f939ccb lexicon r2 fix; 4065ef2 calibration), archive extracted to scratchpad; app/llm/lexicon.yaml, tests/unit/test_t133_lexicon.py, evals/reports/20261102T123428Z.md; lexicon-only, no app URL (no server run); HEAD also contains 5fb338d (T-134, out of scope); pre-r2 comparison 1218b2e archive",
 "exercised": ["board.py show T-133 with handoff", "git log and git show --stat on 4065ef2; git diff e79c3aa^..HEAD on lexicon.yaml; read tests/unit/test_t133_lexicon.py at 4065ef2", "git archive 4065ef2 extracted; lexicon sha256 equals HEAD", "git archive f939ccb extracted; pytest --collect-only: 3316 (f939ccb), 3322 (HEAD)", "pytest tests/unit -q on HEAD archive: 3318 passed, 4 skipped, exit 0", "probe_r3.py: 4 named sentences, 15 HPI and header sentences, 8 positives and controls, 7 header variants, 5 negation probes on HEAD and 1218b2e", "probe_flags.py and scan_all.py: flags.lexicon_flags and lexicon_scan.scan on the same sentences, HEAD and 1218b2e", "10 extra HPI variants on HEAD", "mutants A to D (attribution_word deny, header look-ahead, negation_word deny, pre_cues denying) on HEAD archive; tests/unit/test_t133_lexicon.py on each", "research/lexicon_selfcheck.py on HEAD archive: PASS, held-out 115/115", "app.pipeline evals/golden/sample.txt via runpy with LLM_BACKEND=fixture, twice on HEAD and once on 1218b2e: identical", "curl NegEx and pyConText KB (HTTP 200); grep deny lines", "head of evals/reports/20261102T123428Z.md and 20261102T123652Z.md; grep evals/reports for claude-cli; grep tests, golden and spec for past, medical and surgical history headers"],
 "verdict": "changes",
 "scores": {"deterministic_no_llm": 5, "deny_forms_grounded_and_sourced": 5, "history_entry_hits_and_controls": 3, "over_flag_control_on_hpi_text": 4, "no_regression_outside_card_scope": 2, "mutation_killability": 5, "flag_excerpt_visibility": 3, "eval_evidence_criterion_18": 3},
 "findings": [
  {"severity": "major", "title": "Past, Medical and Surgical history headers and Past medical history: significant for X lost the prior-condition flag in f939ccb",
   "evidence": "Repro on the HEAD archive and the 1218b2e archive with flags.lexicon_flags: 'Past history: significant for lumbar strain.' 1218b2e pre_existing flag, HEAD none; 'Medical history: significant for diabetes.' 1218b2e flag, HEAD none; 'Surgical history: notable for L4-5 laminectomy.' 1218b2e flag, HEAD none; 'Past medical history: significant for diabetes.' 1218b2e flag via history_significant_for, HEAD none. Cause: header look-ahead at app/llm/lexicon.yaml:185 applies to every history word. Rationale at app/llm/lexicon.yaml:181 says past history has pmh_psh_section and hx_abbrev; pmh_psh_section (lexicon.yaml:202-208) is strength low and dropped by app/backend/lexicon_scan.py:11 and :196; hx_abbrev (lexicon.yaml:142-143) covers Hx, h/o, PHx only. grep of tests/unit/test_t133_lexicon.py finds no past, medical or surgical header test (only the comment at line 145).",
   "why_it_matters": "The entry exists to flag prior conditions in chart history. The r2 fix removed the flag from a standard PMH idiom that the pre-r2 build raised. The lexicon is the floor (app/backend/flags.py:243: a failed or missed model call leaves the lexicon flags in place), so when the model also misses, no flag is raised. Major, not blocker: the record text is unchanged and the model pass may still flag; that path was not tested.",
   "fix": "Scope the header exclusion to a bare History: add look-behinds for past, medical and surgical before the history word, for example (?<!past\\s)(?<!medical\\s)(?<!surgical\\s), and keep the header look-ahead for a bare History:. Add the four forms to the hit list in tests/unit/test_t133_lexicon.py.",
   "acceptance_test": "lexicon_scan.scan and flags.lexicon_flags return a pre_existing flag whose excerpt is the full sentence for 'Past history: significant for lumbar strain.', 'Medical history: significant for diabetes.', 'Surgical history: notable for L4-5 laminectomy.' and 'Past medical history: significant for diabetes.'; the four r2 F1 sentences and HPI01 to HPI15 stay quiet; a test fails if a past, medical or surgical look-behind is removed."},
  {"severity": "minor", "title": "A semicolon after a bare history word now suppresses the flag, dropping a true prior condition",
   "evidence": "HEAD flags.lexicon_flags on 'History reviewed; significant for diabetes.' returns [] (1218b2e returned a flag with excerpt 'History reviewed;'). 'Pain 6/10. History reviewed; notable for pain on cough.' returns [] on HEAD. Suppression pinned at tests/unit/test_t133_lexicon.py:193-196; design comment at app/llm/lexicon.yaml:184. The r1 F3 acceptance asked for an excerpt containing the condition.",
   "why_it_matters": "No conditionless quote now appears, but the trade is a silent miss on a semicolon form that can carry a true prior condition. The comment discloses it; the card does not record it as a scope cut for Chris.",
   "fix": "Either extend the unit to the condition clause after a non-attribution semicolon, as the r1 fix proposed, or record a SCOPE_CUTS row for the lost form and get Chris's decision.",
   "acceptance_test": "flags.lexicon_flags on 'History reviewed; significant for diabetes.' returns one pre_existing flag whose excerpt contains 'significant for diabetes', or a SCOPE_CUTS row names the form and a test pins that decision."},
  {"severity": "minor", "title": "Eval evidence for the lexicon change is still fixture-only (r2 F5, open)",
   "evidence": "evals/reports/20261102T123428Z.md:3 'backend fixture'; line 6: determinism_3run and unsupported_count_3run need a live backend. evals/reports/20261102T123652Z.md is fixture and dirty. The claude-cli reports (controls-20261102T063331Z.md, controls-20261102T075238Z.md, determinism-diagnosis.md) predate the change.",
   "why_it_matters": "Criterion 18 needs a re-run eval report for a lexicon change. The path exists, but live determinism and unsupported-count numbers are not measured.",
   "fix": "Run the live claude-cli eval on the T-133 commit and cite its report path on the card before the M3 gate.",
   "acceptance_test": "A report under evals/reports/ has backend claude-cli, numeric determinism_3run and unsupported_count_3run, and a source commit at or after f939ccb, and the card cites it."},
  {"severity": "minor", "title": "Design: bare History narratives with the patient as source still flag pre_existing",
   "evidence": "HEAD flags.lexicon_flags returns a pre_existing flag, via history_significant_for, for 'History obtained from patient, notable for neck pain.', 'History per patient: significant for neck pain.' and 'History (per patient): notable for neck pain.'. The r2 fix quiets the same sentence only when an index cue follows ('since the crash').",
   "why_it_matters": "These are HPI-shaped and the brief asks for HPI narratives not to flag. The AC's wife-source example flags by the same rule, so the rule is consistent. Whether patient-as-source should be excluded is a product decision, not a reviewer call; not a spec violation.",
   "fix": "Chris decides. If excluded, add a suppressor for patient or pt as the source when no past-history cue is present. If not, state that in the entry rationale.",
   "acceptance_test": "Whichever decision is taken is pinned by a test next to the existing wife-source test in tests/unit/test_t133_lexicon.py."}
 ],
 "whats_right": ["The four named r2 F1 sentences and HPI01 to HPI15 stay quiet on HEAD, and the wife, diabetes, prior-assault and 2019 forms still flag.", "Deny is a negation everywhere it is read (negation_word, pre_cues, field_answer, attribution_word, is_negation_word), and each form now has an opened source with its URL in the yaml.", "Sample case output is identical between the pre-r2 and HEAD builds across two runs, and lexicon_selfcheck is PASS 115/115."],
 "questions_for_chris": ["Should bare History narratives whose source is the patient ('History obtained from patient, notable for neck pain.', 'History per patient: notable for neck pain.') raise pre_existing, as the wife-source AC example does, or be quiet like the index-cue form?", "Is the semicolon suppression of 'History reviewed; notable for X' (recall loss) acceptable as a recorded scope cut, or should the flag show the condition as r1 proposed?"]}
```
