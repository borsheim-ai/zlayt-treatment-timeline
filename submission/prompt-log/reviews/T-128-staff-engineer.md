# T-128 review, round 1 - staff-engineer-reviewer

Card: summary trim must never leave a fragment (source findings: reviews/T-112-staff-engineer-r3.md finding 2 and 4). Commit 3d53ca5; HEAD at review time is 93de5f2 (`git log --oneline | head -3` shows 93de5f2, 3a74f75, 3d53ca5; `git diff 3d53ca5 HEAD --stat -- app/backend/summary_trim.py` is empty). I worked on `git archive 93de5f2` in my scratchpad (`T128_9_127_r1/repo`, plus a second archive `mut/` for mutants). Probe and mutation scripts are copied to `artifacts/review-evidence/T-128-129-127-r1/`.

**Verdict: changes.** One major, two minors. The 7 fragments named in r3 are held and the three r3 mutants are now killed. The guard is still a closed word list, though: 10 of 31 fresh probes still leave a clear fragment and 3 more a borderline one.

## 1. Deterministic checks
- `tests/unit/test_summary_trim.py` in the archive: 259 passed (matches the handoff). Full `tests/unit` in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed (handoff says 3056 passed; the 4 skips account for the difference).
- No model or network is involved: `summary_trim.py` is pure code.

## 2. Fresh fragment probes (probe_t128.py, 31 summaries)
`.venv/bin/python -I probe_t128.py <archive>`. 19 of 31 trimmed, 12 stayed whole (correct, whole summary goes to judge 1). Of the 19 trimmed outputs, 10 are clear fragments, 3 borderline, 6 fine:
- Clear fragments: `Pain in the neck and lower back.` | `Lower back pain.` -> `Lower back.`; `Pain in the neck and right shoulder.` -> `Right shoulder.`; `Wrist fracture and surgery.` | `Surgery.` -> `Surgery.`; `MRI ordered, pending insurance approval.` -> `Pending insurance approval.`; `Knee surgery recommended, requiring six weeks of crutches.` -> `Requiring six weeks of crutches.`; `Ankle sprain, likely from the fall.` -> `Likely from the fall.`; `Back pain, worse with sitting.` -> `Worse with sitting.`; `Epidural injection given, after which pain eased.` -> `After which pain eased.`; `Shoulder surgery performed, leading to a sling.` -> `Leading to a sling.`; `Physical therapy started, plus home exercises.` -> `Plus home exercises.`
- Borderline: `Again advised to rest.`, `Treated with ice.`, `No radiation.` (the last is a negation kept over a quote that says radiation to arm; judge 1 still sees it).
- The guard works only for words in `_CONNECTOR` (summary_trim.py:389-392), the bare-body-part test (:445-447) and `_LEAD`. `pending`, `requiring`, `likely`, `worse`, `after`, `leading`, `plus`, `again` are not in any list, and a two-word noun phrase (`Lower back`) or a non-body bare noun (`Surgery`) passes the single-body-part test. This is the r3 finding-2 class with a different vocabulary.

## 3. Unsupported clauses still trim (probe_t128b.py, 12 pairs)
5 of 12 trim as intended (`Neck pain; surgery recommended.` -> `Neck pain.`; `Wrist pain; cast applied; discharged home.` -> `Wrist pain; discharged home.`; also the sling, splint and CT cases). 7 stay whole: 2 are right (`then physical therapy`, `Which was tolerated.` would be cut-loose clauses), 5 are over-guarded: `Neck pain. Surgery recommended. Also reports headaches.`, `Neck pain; MRI ordered. Was prescribed ibuprofen.`, `Back pain; injection given. Is improving.`, `Back pain; ultrasound done. Had a follow-up visit.` (each kept clause is its own sentence), and `Was seen at the ER; surgery recommended.` (nothing was removed before it; the summary opened that way itself). This fails safe (judge 1 sees the unsupported clause) but the brief's "unsupported clauses still trim when no fragment would remain" is not met for these.

## 4. Mutation of the tests (mut.py, 14 mutants on summary_trim.py against test_summary_trim.py)
Killed (9): connector rule off; drop the after-removed arm; with-join guard off; bare-body-part test off; widen it to any noun; delete `which`, `including`, `was`, `due` from `_CONNECTOR`. Survived (5): drop the "no kept clause before it" arm (259 passed; this arm only fires for the summary's own first clause, which is exactly the over-guard above); drop `len(...) > 1` (equivalent: a one-word summary cannot have had a clause removed); delete `also`, `however`, `consistent` from `_CONNECTOR`.
Abbreviation-table sweep (sweep.py: each of the 30 `_ABBR`/`_ABBR_CASE` entries set to a dead word, then test_summary_trim.py): 26 killed, 4 survive: `IV`, `orif`, `hep`, `ekg`. The card's AC says each entry deletion is killed. `IV`, `hep`, `ekg` show no behavioural effect in any pair I tried. `orif` does, in the direction the tests do not cover (section 5).

## 5. Reverse-direction abbreviation check (rev.py, 18 pairs: abbreviation in the summary, spelled out in the quote)
2 of 18 over-trim to an empty text (to the could-not-verify tray): `ORIF wrist.` | `Open reduction internal fixation of wrist.` -> `''`; `RCR performed.` | `Rotator cuff repair performed.` -> `''`. The `orif` and `rcr` expansions (summary_trim.py:97-98) append the word `surgery`, which the quote does not contain, so the family check sees a new procedure. The other 16 stay whole. Pre-existing T-112 behaviour, not introduced here, but it is why the `orif` survivor matters.

```json
{"card": "T-128", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive of 93de5f2 (summary_trim.py and test_summary_trim.py identical to 3d53ca5) in scratchpad T128_9_127_r1; app/backend/summary_trim.py, tests/unit/test_summary_trim.py, reviews/T-112-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-054; fixture/no backend, no network",
 "exercised": [
  "python3 tools/board.py show T-128, T-129, T-127; read reviews/T-112-staff-engineer-r3.md in full; git diff 3d53ca5~1 3d53ca5",
  ".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed",
  "tests/unit/test_summary_trim.py in the archive: 259 passed",
  "probe_t128.py: 31 fresh fragment-prone summaries (19 trimmed, 10 clear and 3 borderline fragments among them)",
  "probe_t128b.py: 12 positive-control pairs (5 trimmed, 2 rightly held, 5 over-guarded)",
  "mut.py: 14 mutants of summary_trim.py (9 killed, 5 survived), 5 of ingest.py and 11 of present.py/review.py run for the sibling cards",
  "sweep.py: 30 abbreviation-table entries set dead one at a time (26 killed, 4 survive: IV, orif, hep, ekg)",
  "rev.py: 18 reverse-direction abbreviation pairs (2 over-trimmed)",
  "grep of docs/LLM_VS_CODE.md and memory/ORCHESTRATOR_DECISIONS.md for 'fragment' and 'not yet committed'"
 ],
 "verdict": "changes",
 "scores": {"deterministic_trim_is_code": 5, "fragment_safety": 2, "unsupported_removal_precision": 3, "faithful_paraphrase_survival": 4, "test_strength": 3, "doc_matches_code": 3},
 "findings": [
  {"severity": "major",
   "title": "The fragment guard is a closed word list: 10 of 31 fresh probes still leave a clear fragment, 3 more a borderline one; D-054 still says 'never leaving a fragment'",
   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-128-129-127-r1/probe_t128.py <archive>` (summary_trim.py:389-392 `_CONNECTOR`, :445-447 bare body part): 'Pain in the neck and lower back.' | 'Lower back pain.' -> 'Lower back.'; 'Pain in the neck and right shoulder.' -> 'Right shoulder.'; 'Wrist fracture and surgery.' | 'Surgery.' -> 'Surgery.'; 'MRI ordered, pending insurance approval.' | 'MRI approved.' -> 'Pending insurance approval.'; 'Knee surgery recommended, requiring six weeks of crutches.' -> 'Requiring six weeks of crutches.'; 'Ankle sprain, likely from the fall.' -> 'Likely from the fall.'; 'Back pain, worse with sitting.' -> 'Worse with sitting.'; 'Epidural injection given, after which pain eased.' -> 'After which pain eased.'; 'Shoulder surgery performed, leading to a sling.' -> 'Leading to a sling.'; 'Physical therapy started, plus home exercises.' -> 'Plus home exercises.'. Borderline: 'Again advised to rest.', 'Treated with ice.', 'No radiation.'. memory/ORCHESTRATOR_DECISIONS.md:62 (D-054) 'never leaving a fragment'.",
   "why_it_matters": "This is r3 finding 2 again: the fix adds the r3 examples' words (due, which, including) and one-body-part rule, so the same defect class re-opens with the next connector. A fragment like 'Likely from the fall.' reaches judge 1 and the paralegal as the whole summary after one accept click; nothing is invented and the quote and trace stay, so it is not a blocker, but the card title and D-054 promise 'never' and the 7 tested probes were written from the review's own examples (they pass by construction).",
   "fix": "Replace the lexical list with a structural test: after removal, a kept clause that does not contain a finite verb or a content-word head of its own, or whose first word is not a noun/adjective/determiner head of the original summary's subject, keeps the whole summary. Cheap version: when a clause is removed, keep the whole summary unless every kept clause begins with a word that also begins a kept clause in the ORIGINAL summary's first position (i.e. a word that could open a sentence), and extend the bare-noun rule to any single content word or a noun phrase with no verb. Or soften D-054 to name the guarded shapes.",
   "acceptance_test": "tests/unit/test_summary_trim.py: the 10 clear fragments above (and the 3 borderline) return changed False; 'Pain in the neck and back.' over 'Neck pain.' still becomes 'Pain in the neck.'; a parametrized sweep takes every trimmed output of 100 recorded generator summaries and asserts each kept clause begins with the summary's own first-clause word class or a verb."},
  {"severity": "minor",
   "title": "The guard over-fires: 5 of 12 positive controls that should trim stay whole, including a summary whose own first clause opens with a connector word",
   "evidence": "`probe_t128b.py`: 'Neck pain; MRI ordered. Was prescribed ibuprofen.' | 'Neck pain. Ibuprofen prescribed.' -> unchanged; 'Neck pain. Surgery recommended. Also reports headaches.' -> unchanged; 'Back pain; injection given. Is improving.' -> unchanged; 'Back pain; ultrasound done. Had a follow-up visit.' -> unchanged; 'Was seen at the ER; surgery recommended.' | 'Seen at ER.' -> unchanged. summary_trim.py:443 `(after_removed or not any(not d for d in drop[:i])) and _connector_led(...)` does not look at the separator, so a new sentence after '.' counts as cut-loose. Mutant 'drop the no-kept-before arm' -> 259 passed.",
   "why_it_matters": "I would have done it differently, not a spec violation: the failure is in the safe direction (judge 1 still sees the unsupported clause). But AC 1 says the trim 'still trims when no fragment would remain', and the handoff's own surprise ('a blanket rule broke Pain.') shows the guard was tuned by hand.",
   "fix": "Apply the connector test only when the removed clause was joined to the kept one by ',' ';' or a conjunction, not when a '.' ends the removed clause; and drop the leading arm (a summary's own first clause is the model's wording, not something this trim cut loose).",
   "acceptance_test": "The 4 two-sentence pairs and the 'Was seen at the ER' pair above trim (changed True, kept clause intact); 'Knee surgery recommended, due to torn meniscus.' over 'Torn meniscus.' still stays whole."},
  {"severity": "minor",
   "title": "Mutant-killing tests are incomplete: 3 connector entries, the leading arm and 4 abbreviation entries (IV, orif, hep, ekg) survive; the orif entry shows a faithful over-trim in the reverse direction",
   "evidence": "mut.py: deleting 'also', 'however' or 'consistent' from `_CONNECTOR` -> 259 passed each; dropping the leading arm -> 259 passed. sweep.py: 4 of 30 table entries survive (IV, orif, hep, ekg); AC 1 evidence names only tha/acdf/lle/rle/bue/rue/lue/u/s/UE. rev.py: 'ORIF wrist.' | 'Open reduction internal fixation of wrist.' -> '' and 'RCR performed.' | 'Rotator cuff repair performed.' -> '' (expansions at summary_trim.py:97-98 append 'surgery').",
   "why_it_matters": "The card's second half is 'kill the surviving mutants'; 26 of 30 table deletions are killed, not all. The two reverse-direction over-trims send faithful entries to the tray, the T-112 r1/r2/r3 failure class (accepted as debt after round 3).",
   "fix": "Add one test per surviving connector (also, however, consistent) and a faithful pair for orif/rcr in both directions; drop 'surgery' from the orif/rcr expansions or let a procedure word be covered by the abbreviation that produced it. Mark IV/hep/ekg as dead entries (remove or document).",
   "acceptance_test": "The sweep.py run prints 'survivors: []' or lists only entries documented as inert; 'ORIF wrist.' over the spelled-out quote returns changed False."}
 ],
 "whats_right": [
  "The 7 fragments from the T-112 r3 review are held whole and the three r3 mutants (us/im case, label body vouch, quote negation) are now killed by named tests.",
  "Trimming stays pure code with the original output kept: unsupported clauses with no fragment risk still trim to a whole clause ('Neck pain; surgery recommended.' -> 'Neck pain.').",
  "Test file is deterministic and fast (259 tests in about 1 s), with a monkeypatch-based entry-deletion check built into the suite."
 ],
 "questions_for_chris": []}
```
