# Subagent: Staff r2: T-128 + T-129 (Staff r2: T-128 + T-129)

Source: `agent-a5c8ca48f3b7c9cf3.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:57:47.928Z

This is the round-2 review of board cards T-128 and T-129 in /Users/arsis/zlayt-pm-project. Read reviews/T-128-staff-engineer.md and reviews/T-129-staff-engineer.md, and both cards (`python3 tools/board.py show T-###`), including the handoffs and orchestrator notes.

On a `git archive HEAD` copy in your scratchpad, check each card:
- **T-128:** the structural no-fragment rule. Only later clauses are removed. If the first clause is unsupported, nothing is trimmed. If the kept prefix has fewer than 2 content words, nothing is trimmed. Re-run your 31 fragment probes and 12 should-trim probes, plus at least 15 fresh ones. Check that the IV/orif/hep/ekg deletion mutants die, and that the negation words now come from the lexicon (no private _NEG).
- **T-129:** preamble and unsplit are served on GET case and match api.md. A case re-run after the change leaves no accepted flag pointing at a shifted record number; test it.

Run the unit suite and mutate the code to test the tests.

Write reviews/T-128-staff-engineer-r2.md and reviews/T-129-staff-engineer-r2.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Stop only your own PIDs. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:50.877Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:57:50.888Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:51.194Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-128-staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:57:51.204Z

**tool result**
````
1	# T-128 review, round 1 - staff-engineer-reviewer
2	
3	Card: summary trim must never leave a fragment (source findings: reviews/T-112-staff-engineer-r3.md finding 2 and 4). Commit 3d53ca5; HEAD at review time is 93de5f2 (`git log --oneline | head -3` shows 93de5f2, 3a74f75, 3d53ca5; `git diff 3d53ca5 HEAD --stat -- app/backend/summary_trim.py` is empty). I worked on `git archive 93de5f2` in my scratchpad (`T128_9_127_r1/repo`, plus a second archive `mut/` for mutants). Probe and mutation scripts are copied to `artifacts/review-evidence/T-128-129-127-r1/`.
4	
5	**Verdict: changes.** One major, two minors. The 7 fragments named in r3 are held and the three r3 mutants are now killed. The guard is still a closed word list, though: 10 of 31 fresh probes still leave a clear fragment and 3 more a borderline one.
6	
7	## 1. Deterministic checks
8	- `tests/unit/test_summary_trim.py` in the archive: 259 passed (matches the handoff). Full `tests/unit` in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed (handoff says 3056 passed; the 4 skips account for the difference).
9	- No model or network is involved: `summary_trim.py` is pure code.
10	
11	## 2. Fresh fragment probes (probe_t128.py, 31 summaries)
12	`.venv/bin/python -I probe_t128.py <archive>`. 19 of 31 trimmed, 12 stayed whole (correct, whole summary goes to judge 1). Of the 19 trimmed outputs, 10 are clear fragments, 3 borderline, 6 fine:
13	- Clear fragments: `Pain in the neck and lower back.` | `Lower back pain.` -> `Lower back.`; `Pain in the neck and right shoulder.` -> `Right shoulder.`; `Wrist fracture and surgery.` | `Surgery.` -> `Surgery.`; `MRI ordered, pending insurance approval.` -> `Pending insurance approval.`; `Knee surgery recommended, requiring six weeks of crutches.` -> `Requiring six weeks of crutches.`; `Ankle sprain, likely from the fall.` -> `Likely from the fall.`; `Back pain, worse with sitting.` -> `Worse with sitting.`; `Epidural injection given, after which pain eased.` -> `After which pain eased.`; `Shoulder surgery performed, leading to a sling.` -> `Leading to a sling.`; `Physical therapy started, plus home exercises.` -> `Plus home exercises.`
14	- Borderline: `Again advised to rest.`, `Treated with ice.`, `No radiation.` (the last is a negation kept over a quote that says radiation to arm; judge 1 still sees it).
15	- The guard works only for words in `_CONNECTOR` (summary_trim.py:389-392), the bare-body-part test (:445-447) and `_LEAD`. `pending`, `requiring`, `likely`, `worse`, `after`, `leading`, `plus`, `again` are not in any list, and a two-word noun phrase (`Lower back`) or a non-body bare noun (`Surgery`) passes the single-body-part test. This is the r3 finding-2 class with a different vocabulary.
16	
17	## 3. Unsupported clauses still trim (probe_t128b.py, 12 pairs)
18	5 of 12 trim as intended (`Neck pain; surgery recommended.` -> `Neck pain.`; `Wrist pain; cast applied; discharged home.` -> `Wrist pain; discharged home.`; also the sling, splint and CT cases). 7 stay whole: 2 are right (`then physical therapy`, `Which was tolerated.` would be cut-loose clauses), 5 are over-guarded: `Neck pain. Surgery recommended. Also reports headaches.`, `Neck pain; MRI ordered. Was prescribed ibuprofen.`, `Back pain; injection given. Is improving.`, `Back pain; ultrasound done. Had a follow-up visit.` (each kept clause is its own sentence), and `Was seen at the ER; surgery recommended.` (nothing was removed before it; the summary opened that way itself). This fails safe (judge 1 sees the unsupported clause) but the brief's "unsupported clauses still trim when no fragment would remain" is not met for these.
19	
20	## 4. Mutation of the tests (mut.py, 14 mutants on summary_trim.py against test_summary_trim.py)
21	Killed (9): connector rule off; drop the after-removed arm; with-join guard off; bare-body-part test off; widen it to any noun; delete `which`, `including`, `was`, `due` from `_CONNECTOR`. Survived (5): drop the "no kept clause before it" arm (259 passed; this arm only fires for the summary's own first clause, which is exactly the over-guard above); drop `len(...) > 1` (equivalent: a one-word summary cannot have had a clause removed); delete `also`, `however`, `consistent` from `_CONNECTOR`.
22	Abbreviation-table sweep (sweep.py: each of the 30 `_ABBR`/`_ABBR_CASE` entries set to a dead word, then test_summary_trim.py): 26 killed, 4 survive: `IV`, `orif`, `hep`, `ekg`. The card's AC says each entry deletion is killed. `IV`, `hep`, `ekg` show no behavioural effect in any pair I tried. `orif` does, in the direction the tests do not cover (section 5).
23	
24	## 5. Reverse-direction abbreviation check (rev.py, 18 pairs: abbreviation in the summary, spelled out in the quote)
25	2 of 18 over-trim to an empty text (to the could-not-verify tray): `ORIF wrist.` | `Open reduction internal fixation of wrist.` -> `''`; `RCR performed.` | `Rotator cuff repair performed.` -> `''`. The `orif` and `rcr` expansions (summary_trim.py:97-98) append the word `surgery`, which the quote does not contain, so the family check sees a new procedure. The other 16 stay whole. Pre-existing T-112 behaviour, not introduced here, but it is why the `orif` survivor matters.
26	
27	```json
28	{"card": "T-128", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
29	 "scope": "git archive of 93de5f2 (summary_trim.py and test_summary_trim.py identical to 3d53ca5) in scratchpad T128_9_127_r1; app/backend/summary_trim.py, tests/unit/test_summary_trim.py, reviews/T-112-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-054; fixture/no backend, no network",
30	 "exercised": [
31	  "python3 tools/board.py show T-128, T-129, T-127; read reviews/T-112-staff-engineer-r3.md in full; git diff 3d53ca5~1 3d53ca5",
32	  ".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed",
33	  "tests/unit/test_summary_trim.py in the archive: 259 passed",
34	  "probe_t128.py: 31 fresh fragment-prone summaries (19 trimmed, 10 clear and 3 borderline fragments among them)",
35	  "probe_t128b.py: 12 positive-control pairs (5 trimmed, 2 rightly held, 5 over-guarded)",
36	  "mut.py: 14 mutants of summary_trim.py (9 killed, 5 survived), 5 of ingest.py and 11 of present.py/review.py run for the sibling cards",
37	  "sweep.py: 30 abbreviation-table entries set dead one at a time (26 killed, 4 survive: IV, orif, hep, ekg)",
38	  "rev.py: 18 reverse-direction abbreviation pairs (2 over-trimmed)",
39	  "grep of docs/LLM_VS_CODE.md and memory/ORCHESTRATOR_DECISIONS.md for 'fragment' and 'not yet committed'"
40	 ],
41	 "verdict": "changes",
42	 "scores": {"deterministic_trim_is_code": 5, "fragment_safety": 2, "unsupported_removal_precision": 3, "faithful_paraphrase_survival": 4, "test_strength": 3, "doc_matches_code": 3},
43	 "findings": [
44	  {"severity": "major",
45	   "title": "The fragment guard is a closed word list: 10 of 31 fresh probes still leave a clear fragment, 3 more a borderline one; D-054 still says 'never leaving a fragment'",
46	   "evidence": "`.venv/bin/python -I artifacts/review-evidence/T-128-129-127-r1/probe_t128.py <archive>` (summary_trim.py:389-392 `_CONNECTOR`, :445-447 bare body part): 'Pain in the neck and lower back.' | 'Lower back pain.' -> 'Lower back.'; 'Pain in the neck and right shoulder.' -> 'Right shoulder.'; 'Wrist fracture and surgery.' | 'Surgery.' -> 'Surgery.'; 'MRI ordered, pending insurance approval.' | 'MRI approved.' -> 'Pending insurance approval.'; 'Knee surgery recommended, requiring six weeks of crutches.' -> 'Requiring six weeks of crutches.'; 'Ankle sprain, likely from the fall.' -> 'Likely from the fall.'; 'Back pain, worse with sitting.' -> 'Worse with sitting.'; 'Epidural injection given, after which pain eased.' -> 'After which pain eased.'; 'Shoulder surgery performed, leading to a sling.' -> 'Leading to a sling.'; 'Physical therapy started, plus home exercises.' -> 'Plus home exercises.'. Borderline: 'Again advised to rest.', 'Treated with ice.', 'No radiation.'. memory/ORCHESTRATOR_DECISIONS.md:62 (D-054) 'never leaving a fragment'.",
47	   "why_it_matters": "This is r3 finding 2 again: the fix adds the r3 examples' words (due, which, including) and one-body-part rule, so the same defect class re-opens with the next connector. A fragment like 'Likely from the fall.' reaches judge 1 and the paralegal as the whole summary after one accept click; nothing is invented and the quote and trace stay, so it is not a blocker, but the card title and D-054 promise 'never' and the 7 tested probes were written from the review's own examples (they pass by construction).",
48	   "fix": "Replace the lexical list with a structural test: after removal, a kept clause that does not contain a finite verb or a content-word head of its own, or whose first word is not a noun/adjective/determiner head of the original summary's subject, keeps the whole summary. Cheap version: when a clause is removed, keep the whole summary unless every kept clause begins with a word that also begins a kept clause in the ORIGINAL summary's first position (i.e. a word that could open a sentence), and extend the bare-noun rule to any single content word or a noun phrase with no verb. Or soften D-054 to name the guarded shapes.",
49	   "acceptance_test": "tests/unit/test_summary_trim.py: the 10 clear fragments above (and the 3 borderline) return changed False; 'Pain in the neck and back.' over 'Neck pain.' still becomes 'Pain in the neck.'; a parametrized sweep takes every trimmed output of 100 recorded generator summaries and asserts each kept clause begins with the summary's own first-clause word class or a verb."},
50	  {"severity": "minor",
51	   "title": "The guard over-fires: 5 of 12 positive controls that should trim stay whole, including a summary whose own first clause opens with a connector word",
52	   "evidence": "`probe_t128b.py`: 'Neck pain; MRI ordered. Was prescribed ibuprofen.' | 'Neck pain. Ibuprofen prescribed.' -> unchanged; 'Neck pain. Surgery recommended. Also reports headaches.' -> unchanged; 'Back pain; injection given. Is improving.' -> unchanged; 'Back pain; ultrasound done. Had a follow-up visit.' -> unchanged; 'Was seen at the ER; surgery recommended.' | 'Seen at ER.' -> unchanged. summary_trim.py:443 `(after_removed or not any(not d for d in drop[:i])) and _connector_led(...)` does not look at the separator, so a new sentence after '.' counts as cut-loose. Mutant 'drop the no-kept-before arm' -> 259 passed.",
53	   "why_it_matters": "I would have done it differently, not a spec violation: the failure is in the safe direction (judge 1 still sees the unsupported clause). But AC 1 says the trim 'still trims when no fragment would remain', and the handoff's own surprise ('a blanket rule broke Pain.') shows the guard was tuned by hand.",
54	   "fix": "Apply the connector test only when the removed clause was joined to the kept one by ',' ';' or a conjunction, not when a '.' ends the removed clause; and drop the leading arm (a summary's own first clause is the model's wording, not something this trim cut loose).",
55	   "acceptance_test": "The 4 two-sentence pairs and the 'Was seen at the ER' pair above trim (changed True, kept clause intact); 'Knee surgery recommended, due to torn meniscus.' over 'Torn meniscus.' still stays whole."},
56	  {"severity": "minor",
57	   "title": "Mutant-killing tests are incomplete: 3 connector entries, the leading arm and 4 abbreviation entries (IV, orif, hep, ekg) survive; the orif entry shows a faithful over-trim in the reverse direction",
58	   "evidence": "mut.py: deleting 'also', 'however' or 'consistent' from `_CONNECTOR` -> 259 passed each; dropping the leading arm -> 259 passed. sweep.py: 4 of 30 table entries survive (IV, orif, hep, ekg); AC 1 evidence names only tha/acdf/lle/rle/bue/rue/lue/u/s/UE. rev.py: 'ORIF wrist.' | 'Open reduction internal fixation of wrist.' -> '' and 'RCR performed.' | 'Rotator cuff repair performed.' -> '' (expansions at summary_trim.py:97-98 append 'surgery').",
59	   "why_it_matters": "The card's second half is 'kill the surviving mutants'; 26 of 30 table deletions are killed, not all. The two reverse-direction over-trims send faithful entries to the tray, the T-112 r1/r2/r3 failure class (accepted as debt after round 3).",
60	   "fix": "Add one test per surviving connector (also, however, consistent) and a faithful pair for orif/rcr in both directions; drop 'surgery' from the orif/rcr expansions or let a procedure word be covered by the abbreviation that produced it. Mark IV/hep/ekg as dead entries (remove or document).",
61	   "acceptance_test": "The sweep.py run prints 'survivors: []' or lists only entries documented as inert; 'ORIF wrist.' over the spelled-out quote returns changed False."}
62	 ],
63	 "whats_right": [
64	  "The 7 fragments from the T-112 r3 review are held whole and the three r3 mutants (us/im case, label body vouch, quote negation) are now killed by named tests.",
65	  "Trimming stays pure code with the original output kept: unsupported clauses with no fragment risk still trim to a whole clause ('Neck pain; surgery recommended.' -> 'Neck pain.').",
66	  "Test file is deterministic and fast (259 tests in about 1 s), with a monkeypatch-based entry-deletion check built into the suite."
67	 ],
68	 "questions_for_chris": []}
69	```
70	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:51.563Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-129-staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:57:51.571Z

**tool result**
````
1	# T-129 review, round 1 - staff-engineer-reviewer
2	
3	Card: a non-library preamble must not become record 1 (reviews/T-123-paralegal.md minor; D-027: nothing is dropped). Commit 3a74f75; HEAD at review time is 93de5f2 (`git diff 3a74f75 HEAD --stat -- app/backend/ingest.py` is empty). I worked on `git archive 93de5f2` (`repo/`) and on `git archive 3a74f75~1` (`parent/`) in scratchpad `T128_9_127_r1`. Scripts are in `artifacts/review-evidence/T-128-129-127-r1/`.
4	
5	**Verdict: changes.** One major, one minor. Numbering is stable and nothing is dropped, and all 5 ingest mutants I ran are killed. But the contract line that says the preamble "has `preamble: true`" is not true of what the API serves, so the card's second option ("shown as a preamble") is unreachable and the preamble is still counted and displayed as an unlabelled record 3.
6	
7	## 1. Deterministic checks
8	- `tests/unit/test_ingest.py` is part of the full unit run in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed.
9	- Old/new comparison over every `.txt` input under evals/, tests/, spec/, app/ (27 files, `cmp_ingest.py` loads the parent and HEAD `ingest.py` side by side): record numbers, sources and `unsplit` flags are identical for all 27. Golden and library packets and `unsplit_paste.txt` do not shift. The recorded-fixture suite passes, so no recorded call is keyed to a moved number.
10	- Record numbering of the 9 shapes in `ab.py` (HEAD vs parent): with a preamble above (`---` separated, blank-line separated, no separator, `=== Record N ===` style, "Re: Date:" text, two preambles), real records are r1, r2 and the preamble(s) are r3 (r4), `unsplit: true`, `preamble: true`. A note between records and trailing text are numbered after the real records, `preamble: false`. Parent numbered the preamble r1 in all of those. `ov129.py`: no overlapping record spans in 6 shapes.
11	
12	## 2. What the API serves (api129.py, via `pipeline.ingest_case` and `present.record_view`)
13	`record_view` keys: char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text. No `unsplit`, no `preamble`. HEAD: `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')` (unsplit and preamble print None). `GET /api/cases/{token}` returns `"warnings": []` (present.py case_view), so `UNSPLIT_TEXT` is only in the POST response. `grep -n "UNSPLIT\|unsplit\|preamble" app/frontend/*.js app/frontend/*.html` prints nothing. memory/contracts/api.md:76 says an unsplit record has `unsplit: true` and the one above the first real record `preamble: true`.
14	
15	## 3. Upgrade behaviour (upg129.py)
16	A case created under the parent with a cover sheet, whose gap flag the paralegal accepted, then re-ingested by HEAD code on the same DB file:
17	`old: [('f_gap_r2_r3', 'accepted', 70), ('f_date_r1', 'pending', None)]` then `new: records r1 2026-01-09, r2 2026-03-20, r3 None; flags [('f_gap_r2_r3', 'accepted', 70, ['r2','r3']), ('f_gap_r1_r2', 'pending', 70, ['r1','r2']), ('f_date_r3', 'pending', None, ['r3'])]`. `_persist` (pipeline.py:186-208) keeps the accepted row by id, and it now cites r3 = the cover sheet.
18	
19	```json
20	{"card": "T-129", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
21	 "scope": "git archive of 93de5f2 (ingest.py identical to 3a74f75) and 3a74f75~1 in scratchpad T128_9_127_r1; app/backend/ingest.py, tests/unit/test_ingest.py, app/backend/present.py record_view, app/backend/pipeline.py _store_records/_persist, memory/contracts/api.md:76; fixture/no backend, no network",
22	 "exercised": [
23	  "python3 tools/board.py show T-129; git diff 3a74f75~1 3a74f75; read app/backend/ingest.py in full",
24	  ".venv/bin/python -m pytest tests/unit -q in the archive: 3057 collected, 3053 passed, 4 skipped, 0 failed",
25	  "cmp_ingest.py: parent vs HEAD ingest over 27 .txt inputs under evals/, tests/, spec/, app/ (0 differ in record numbers/sources/unsplit)",
26	  "ab.py: 9 input shapes through parent and HEAD ingest (preamble with ---, blank line, no separator, header style; mid-note; trailing note; date-like preamble)",
27	  "ov129.py: 6 preamble shapes checked for overlapping record spans (none)",
28	  "api129.py: pipeline.ingest_case + present.record_view keys for a preamble case and a mid-note case (parent and HEAD)",
29	  "upg129.py: case created and gap flag accepted under the parent, re-ingested under HEAD on the same sqlite file",
30	  "mut.py: 5 mutants of ingest.py against tests/unit/test_ingest.py (sort off, preamble flag never set, preamble always true, first = block start, drop leftovers): all 5 killed",
31	  "grep of app/frontend for UNSPLIT/unsplit/preamble; grep of callers of ingest/split_records/_store_records"
32	 ],
33	 "verdict": "changes",
34	 "scores": {"numbering_stability": 5, "nothing_dropped_D027": 5, "api_exposes_preamble": 2, "contract_matches_code": 2, "test_strength": 4, "upgrade_safety": 3},
35	 "findings": [
36	  {"severity": "major",
37	   "title": "The preamble is still a counted record 3 and nothing the API serves says it is a preamble: api.md:76 promises `unsplit`/`preamble` fields on the record that GET case and POST case do not return",
38	   "evidence": "api129.py on HEAD: `record_view` keys are char_end, char_start, date_candidates, date_iso, date_raw, date_status, duplicate_of, encounter, id, injection_tag, language, seq, source_label, text; the cover sheet prints `('r3', 3, 0, None, None, 'FAX COVER SHEET|To')`. present.py case_view returns `\"warnings\": []`; `grep -rn \"UNSPLIT\\|unsplit\\|preamble\" app/frontend` prints nothing. memory/contracts/api.md:76: 'text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: ... the one above the first real record also has `preamble: true`'. Card AC 1: 'is not counted as a record (or is shown as a preamble, not a record)'. Handoff: 'Left: frontend may label preamble records.'",
39	   "why_it_matters": "The harm the paralegal reported (a cover sheet shifting 'record 1') is fixed. But AC 1 asks for one of two outcomes: the cover sheet is not counted (it is, as record 3, so a 2-record packet reports 3), or it is shown as a preamble (the UI cannot tell: the flag lives only in the in-memory ingest dict, which `_store_records` (pipeline.py:158) does not persist and `record_view` does not emit). The contract text is wrong for GET case, so a frontend following it finds no field. The stated 'frontend may label' follow-up cannot be built without a backend change.",
40	   "fix": "Persist `unsplit` and `preamble` on the records row (or derive them in `record_view` from `source_label == '' and date_raw == ''` plus position) and add both to `record_view`; carry the `UNSPLIT_TEXT` warning into GET case or document that it is POST-only. Then update api.md:76 to say which responses carry the fields. Frontend card to label it 'cover text, not a record'.",
41	   "acceptance_test": "tests/unit: create a case from a cover-sheet paste, then `GET /api/cases/{token}`: records[2] has `preamble: true` and `unsplit: true`, records[0..1] have both false, and a library packet (golden case_01) has all records false."},
42	  {"severity": "minor",
43	   "title": "A case stored before this commit and re-ingested after it keeps its accepted review on the old record numbers, so the accepted gap flag now cites the cover sheet",
44	   "evidence": "upg129.py: old (parent) `('f_gap_r2_r3', 'accepted', 70)`; after HEAD re-ingest on the same DB: `('f_gap_r2_r3', 'accepted', 70, ['r2','r3'])` alongside a new pending `('f_gap_r1_r2', 'pending', 70, ['r1','r2'])`, with r3 now the cover sheet. pipeline.py:150-166 (`_store_records` deletes and re-stores) and :186-208 (`_persist` keeps the old row's review_status by id; stale rows are removed only if pending).",
45	   "why_it_matters": "A reviewed item stays bound to a number that now means a different record; the accepted gap would still be listed for export. Exposure is bounded (cases purge after 24 h, `DB.RETENTION_SECONDS`, and only pastes with unsplit text are affected), so it is minor, but it is the numbering-stability question the brief asked and the card has no note, no migration and no test.",
46	   "fix": "Either re-run is allowed to drop a reviewed item whose record_ids no longer match the stored records, with a visible reset, or document in the card/DECISIONS that numbering changed and in-flight cases with unsplit text must be re-created (retention makes this a one-line note).",
47	   "acceptance_test": "Unit test: store a case with a preamble using the old numbering (records r1 preamble, r2, r3, accepted f_gap_r2_r3), re-run ingest_case with the new code, assert no accepted flag cites a record whose date differs from the one it was computed on, or that the item is reset to pending."}
48	 ],
49	 "whats_right": [
50	  "Numbering is stable on real data: 27 golden/library/spec inputs produce identical record numbers before and after, and the preamble cases keep r1, r2 for the real records in 6 shapes.",
51	  "D-027 is honoured: the preamble is kept verbatim as its own unsplit record, `UNSPLIT_TEXT` is raised for it, and no span overlaps another.",
52	  "The tests pin the behaviour (6 parametrized preambles plus 2 more): all 5 mutants I ran against ingest.py (sort, flag, first-field, always-preamble, dropped leftovers) fail at least one test."
53	 ],
54	 "questions_for_chris": []}
55	```
56	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:51.930Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t128_t129_t127_patterns.md"
}
````

### User / tool · 2026-11-02T11:57:51.939Z

**tool result**
````
1	---
2	name: project_t128_t129_t127_patterns
3	description: r1 at HEAD 93de5f2 - T-128 changes (fragment guard still a closed word list, over-guard, 4 table survivors), T-129 changes (preamble flag not served by API, pre-upgrade accepted flag mis-bound), T-127 pass
4	metadata:
5	  type: project
6	---
7	
8	- T-128 3d53ca5 (changes: 1 major, 2 minor): fragment guard `_CONNECTOR` + bare-body-part rule is a closed list; 31 fresh probes left 10 clear fragments (pending/requiring/likely/worse/after which/leading/plus, 'Lower back.', 'Surgery.'). Over-guard: connector test ignores the '.' separator and the summary's own first clause (5/12 positives stay whole). Abbreviation sweep: 26/30 killed, survivors IV/orif/hep/ekg; orif/rcr expansions append 'surgery' so the abbreviation-in-summary direction over-trims.
9	- T-129 3a74f75 (changes: 1 major, 1 minor): numbering stable on 27 inputs, 5/5 ingest mutants killed, but `unsplit`/`preamble` never reach record_view, GET case warnings is [] and the frontend never reads them, so api.md:76 is false for GET; pre-upgrade case re-ingest keeps an accepted gap flag bound to the old number (`_persist` keeps review_status by id).
10	- T-127 93de5f2 (pass: 2 minor, 1 nit): from/to comparison in gap_change_index unpinned (equal days, shifted dates); removed path tested only on hand-built events.
11	
12	**Why:** the same classes recur: a closed-vocabulary guard re-opens with the next word; a field that exists in an in-memory dict is documented as API but never persisted or serialised.
13	**How to apply:** on any "contract says field X" card, call present.record_view / the real route and list the keys, do not trust the ingest dict; on guard cards write 30 fresh probes from the guard's complement, not the review's examples; for the old/new comparison load parent and HEAD ingest side by side (scripts in artifacts/review-evidence/T-128-129-127-r1/).
14	
15	Related: [[project_t112_trim_patterns]], [[project_wiring_review_patterns]].
16	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:52.678Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-128; python3 tools/board.py show T-129; git log --oneline | head -5; git status --short | head -20"
}
````

### User / tool · 2026-11-02T11:57:52.912Z

**tool result**
````
---
id: "T-128"
title: "Summary trim: never leave a fragment (Back. / Due to torn meniscus. / Including a sling.) and kill T-112 r3 surviving mutants"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:24:58Z"
updated_at: "2026-11-02T11:57:43Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:49:15Z"
rounds: 1
commits: ["3d53ca5", "180138c"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-128-staff-engineer.md", "at": "2026-11-02T11:49:09Z"}
ac:
  - {"n": 1, "text": "the 5 fragments from reviews/T-112-staff-engineer-r3.md are not produced (trim skipped, whole summary goes to judge); tests kill the us/im case, label body-part vouch and quote-negation mutants and each abbreviation-table entry deletion", "done": true, "evidence": "tests/unit/test_summary_trim.py: 7 fragment probes stay whole; 3 injected mutants (us/im case, label body vouch, quote negation) each fail the suite; per-entry deletion test for tha/acdf/lle/rle/bue/rue/lue/u/s/UE; full unit 3056 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:26:09Z orchestrator: assigned: backend
- 2026-11-02T11:26:18Z backend: claimed
- 2026-11-02T11:37:46Z backend: AC 1 checked: tests/unit/test_summary_trim.py: 7 fragment probes stay whole; 3 injected mutants (us/im case, label body vouch, quote negation) each fail the suite; per-entry deletion test for tha/acdf/lle/rle/bue/rue/lue/u/s/UE; full unit 3056 passed
- 2026-11-02T11:37:46Z backend: moved in_progress -> in_review
- 2026-11-02T11:37:56Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T11:49:09Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-128-staff-engineer.md; round 1; findings:
    - [major] The fragment guard is a closed word list: 10 of 31 fresh probes still leave a clear fragment, 3 more a borderline one; D-054 still says 'never leaving a fragment' — fix: Replace the lexical list with a structural test: after removal, a kept clause that does not contain a finite verb or a content-word head of its own, or whose first word is not a noun/adjective/determiner head of the 
    - [minor] The guard over-fires: 5 of 12 positive controls that should trim stay whole, including a summary whose own first clause opens with a connector word — fix: Apply the connector test only when the removed clause was joined to the kept one by ',' ';' or a conjunction, not when a '.' ends the removed clause; and drop the leading arm (a summary's own first clause is the model's wording, no
    - [minor] Mutant-killing tests are incomplete: 3 connector entries, the leading arm and 4 abbreviation entries (IV, orif, hep, ekg) survive; the orif entry shows a faithful over-trim in the reverse direction — fix: Add one test per surviving connector (also, however, consistent) and a faithful pair for orif/rcr in both directions; drop 'surgery' from the orif/rcr expansions or let a procedure
- 2026-11-02T11:49:09Z orchestrator: Round 2 direction: replace the fragment word list with a structural rule. Never remove the first clause; only later clauses may be removed. If the first clause itself is unsupported, do not trim (send the whole summary to the judge / tray as today). If the kept prefix has fewer than 2 content words, do not trim. That makes fragments like 'Likely from the fall.' / 'Lower back.' impossible by construction. Re-run the reviewer's 31 fragment probes and 12 should-trim probes; kill the IV/orif/hep/ekg deletion mutants.
- 2026-11-02T11:49:10Z orchestrator: assigned: backend
- 2026-11-02T11:49:15Z backend: claimed
- 2026-11-02T11:56:40Z orchestrator: Also (T-105 r2 leftover): summary_trim.py keeps private _NEG/_NEG_WORDS lists; read negation words from the lexicon via grounding.view() like the other checks.
- 2026-11-02T11:57:33Z backend: moved in_progress -> in_review
- 2026-11-02T11:57:43Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Round 2. Replaced the fragment word lists (_CONNECTOR, _LEAD, bare-body-part) with the structural rule: first clause never removed (unsupported first clause = whole summary to judge; all clauses unsupported still = tray), kept prefix (clauses before the first removal) needs >= 2 content words, a clause joined to a removed one by comma / and / with is not left behind (';' or a sentence end may stand alone). Reviewer probes: the fragment set (7 + 19 fresh) all stay whole, 8 positive controls trim incl. the two-sentence and 'Was seen at the ER' cases; reverse ORIF/RCR over-trim fixed with quote-side surgery words; inert IV/hep/ekg entries removed; per-entry tests now put the term in a later clause. Verified: test_summary_trim 285 pass, rule mutants (prefix <1/<3, no comma/and/with, last-removal prefix, qx off) each fail; full unit 3189 pass; evals metrics unchanged. Left: rule 1 is equivalent to rule 2 (empty prefix) so its mutant cannot differ; kept explicit. Surprised: 'Pain; X' and 'Pain 6/10; X' no longer trim (1 content word): fail-safe, judge sees them.

---
id: "T-129"
title: "Ingest: a non-library preamble counts as a phantom record 1"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:25:56Z"
updated_at: "2026-11-02T11:57:43Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:49:15Z"
rounds: 1
commits: ["3a74f75", "1f0a164"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-129-staff-engineer.md", "at": "2026-11-02T11:49:09Z"}
ac:
  - {"n": 1, "text": "a pasted preamble with no record header/date is not counted as a record (or is shown as a preamble, not a record); unit test; reviews/T-123-paralegal.md minor", "done": true, "evidence": "tests/unit/test_ingest.py::test_a_preamble_does_not_shift_the_record_numbers (3 preambles x 2 separators): real records stay r1,r2; preamble kept (D-027) as unsplit preamble:true, numbered last"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:26:09Z orchestrator: assigned: backend
- 2026-11-02T11:26:18Z backend: claimed
- 2026-11-02T11:37:46Z backend: AC 1 checked: tests/unit/test_ingest.py::test_a_preamble_does_not_shift_the_record_numbers (3 preambles x 2 separators): real records stay r1,r2; preamble kept (D-027) as unsplit preamble:true, numbered last
- 2026-11-02T11:37:46Z backend: moved in_progress -> in_review
- 2026-11-02T11:37:56Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T11:49:09Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-129-staff-engineer.md; round 1; findings:
    - [major] The preamble is still a counted record 3 and nothing the API serves says it is a preamble: api.md:76 promises `unsplit`/`preamble` fields on the record that GET case and POST case do not return — fix: Persist `unsplit` and `preamble` on the records row (or derive them in `record_view` from `source_label == '' and date_raw == ''` plus position) and add both to `record_view`; carry the
    - [minor] A case stored before this commit and re-ingested after it keeps its accepted review on the old record numbers, so the accepted gap flag now cites the cover sheet — fix: Either re-run is allowed to drop a reviewed item whose record_ids no longer match the stored records, with a visible reset, or document in the card/DECISIONS that numbering changed and in-flight cases with unsplit tex
- 2026-11-02T11:49:09Z orchestrator: Round 2: serve unsplit/preamble on GET case (or correct api.md:76); a case re-run after this commit must re-key or invalidate decisions whose record_seq shifted (no accepted flag may point at the wrong record) - test it.
- 2026-11-02T11:49:10Z orchestrator: assigned: backend
- 2026-11-02T11:49:15Z backend: claimed
- 2026-11-02T11:57:33Z backend: moved in_progress -> in_review
- 2026-11-02T11:57:43Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Round 2. GET case now serves unsplit and preamble on every record (marks stored in cases.config_json by pipeline._store_record_marks, no schema change; present._recs_by_id/record_view). A re-run in which a record id now names different text (span changed or gone) resets the paralegal's decisions on items citing it to pending, event log keeps them, stale rows are removed by _persist. api.md updated (fields in both examples, UNSPLIT_TEXT is POST-only, reset rule). Verified: 3 new tests in test_ingest.py (served fields, old-numbering upgrade case with an accepted gap, same-numbering keeps decisions); 6 mutants each fail; full unit 3189 pass. Left: frontend label for preamble. Note: the pipeline.py commit also carries another worker's pure reorder of final_amounts_out (same file, uncommitted by them).

1f0a164 fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
882d4ee chore(evals): regenerate calibration.json from a clean worktree of 97b59a6 (fixture; lexicon.yaml T-105 r2)
97b59a6 fix(backend): T-105 r2 lexicon.yaml is the single source: dropped_qualifiers, quote-side checks, negation/side words and the Spanish helper read it through grounding views; structural no-duplicate-list guard
a44dced fix(backend): T-126 r2 every tray flag stays out of export counts and notes, merge trace, one filtered helper
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:57:59.916Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -3; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; ls $S | head; ls artifacts/review-evidence/T-128-129-127-r1/; H=$(git rev-parse HEAD); echo $H; mkdir -p $S/T128_9_r2/repo && git archive HEAD | tar -x -C $S/T128_9_r2/repo && ls $S/T128_9_r2/repo | head -30; git diff 3d53ca5 HEAD --stat -- app/ tests/ memory/contracts | tail -15"
}
````

### User / tool · 2026-11-02T11:58:00.666Z

**tool result**
````
1f0a164 fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
882d4ee chore(evals): regenerate calibration.json from a clean worktree of 97b59a6 (fixture; lexicon.yaml T-105 r2)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
641ed.bak
M1
M1_nocombine
M2
M2_find0
M3
M4
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
ab.py
api129.py
cmp_ingest.py
idx.py
mut.py
ov129.py
probe127.py
probe127b.py
probe_t128.py
probe_t128b.py
rev.py
sweep.py
upg129.py
1f0a164eebb5ed508adea86497e0141bb67fcd95
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
 app/backend/present.py                          |  59 +++++++++-
 app/backend/review.py                           |   7 +-
 app/backend/spanish_text.py                     |  42 +++----
 app/backend/store.py                            |   2 +-
 app/backend/summary_trim.py                     |  57 +++------
 app/backend/trace.py                            |  19 ++-
 app/llm/lexicon.yaml                            |  41 ++++++-
 memory/contracts/api.md                         |  19 ++-
 tests/unit/test_ingest.py                       |  82 +++++++++++++
 tests/unit/test_summary_trim.py                 | 115 ++++++++++++------
 tests/unit/test_t105_added_qualifier_lexicon.py | 149 ++++++++++++++++++++++--
 tests/unit/test_t120_history_source_sentence.py |  77 ++++++++++++
 tests/unit/test_t126_filtered_by_rule.py        | 101 +++++++++++++++-
 tests/unit/test_t127_gap_change_kept.py         |  66 +++++++++++
 20 files changed, 871 insertions(+), 204 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:58:04.298Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; ls -a .venv >/dev/null && echo venv; cd $R && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -5; cat app/backend/summary_trim.py | sed -n 330,520p",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T12:01:08.606Z

**tool result**
````
venv
........................................................................ [ 94%]
........................................................................ [ 97%]
........................................................................ [ 99%]
......................                                                   [100%]
3186 passed, 4 skipped in 182.89s (0:03:02)
    the quote's own topic with a changed value ('Pain 3/10' over 'Pain 4/10') stays, because the D-034/D-047 code checks flag it needs_review and the paralegal sees the conflict."""
    out, loose = [], []
    nums = grounding._num_tokens(clause)
    loose += [n for n in nums if n not in quote["nums"]]
    low = clause.lower()
    for m in grounding._MONTH_RX.findall(clause):
        if m.lower() not in quote["low"] and m.lower() != quote["month"] and str(_MONTHS.index(m.lower()) + 1) not in quote["nums"]:
            out.append(m.lower())
    sw = grounding.side_neg_words(clause, keep_order=True)
    for w in dict.fromkeys(sw):
        if w in _SIDE_WORDS:
            ok = w in quote["sides"] or (w.startswith("bilateral") and (quote["both"] or {"left", "right"} <= quote["sides"]))
            if not ok:
                loose.append(w)
        elif w.endswith("n't") or w in _NEG_WORDS:
            if not quote["neg"]:
                loose.append(w)
    toks = re.findall(r"[A-Za-z0-9]+", clause)
    proper = {t.lower() for i, t in enumerate(toks) if i and len(t) > 2 and t[0].isupper() and t[1:].islower()}      # 'Fennimoor Spine Clinic', 'Capital Imaging': a name, not a body part
    hits = _family_hits([w for w in _words(clause) if w not in proper])
    for name, (kind, w) in hits.items():
        cov = next(c for _k, n, _r, c, _q in _FAM if n == name)
        if name not in quote["fams"] and not (set(cov) & quote["fams"]):
            out.append(w)
    if loose and not any(_supported(w, quote["forms"]) for w in content_words(clause)):
        out += loose
    return list(dict.fromkeys(out))


# The record's source label ('Valley Imaging, cervical MRI') is part of what the quote sits in: it vouches for body parts, sides and imaging modality,
# never for treatment, drug or diagnosis words (a label that says 'orthopedic surgery' does not support 'surgery recommended').
_LABEL_FAMILIES = frozenset({"mri", "ct", "xray", "ultrasound", "emg", "imaging"})


def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
    ex = excerpt or ""
    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if w in _SIDE_WORDS}
    if _QUOTE_LEFT.search(ex + " " + (label or "")):
        sides.add("left")
    if _QUOTE_RIGHT.search(ex + " " + (label or "")):
        sides.add("right")
    month = ""
    m = re.match(r"\d{4}-(\d{2})", date_iso or "")
    if m:
        month = _MONTHS[int(m.group(1)) - 1]
    low = (ex + " " + (label or "")).lower()
    neg = bool(_NEG.search(ex) or _QUOTE_NEG.search(ex))
    return {"nums": _number_set(ex, label or "", date_iso or ""), "low": low, "month": month, "sides": sides, "both": bool(_QUOTE_BOTH.search(ex) or _QUOTE_BOTH.search(_prep(ex))), "neg": neg,
            "forms": _quote_forms(ex + " " + (label or "")), "fams": _quote_families(_words(ex)) | {f for f in _quote_families(_words(label or "")) if f in _LABEL_FAMILIES or f in _BODY}}


_PARTICIPLE = re.compile(r"^(?:[a-z]+(?:ed|ing)|given|consistent|due|secondary|related|compatible|suggestive|positive)$")


def _single_word(piece: str) -> str:
    w = _WORD.findall(piece.lower())
    return w[0] if len(w) == 1 else ""


def _joined_by_with(sep: str) -> bool:
    return sep.strip().lower() == "with"


def trim(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> dict:
    """See the module docstring. Never edits a kept clause's words; only whole clauses are dropped, or nothing is."""
    clauses = split_clauses(summary or "")
    quote = _quote_profile(excerpt, label, date_iso)
    why_removed = [new_salient(text, quote) for text, _ in clauses]
    drop = [bool(w) for w in why_removed]
    unchanged = {"text": summary, "removed": [], "kept": [c[0] for c in clauses], "supported": bool(summary), "notes": [], "changed": False}
    if not any(drop):
        return unchanged
    # 'diagnosed with diabetes': the lone participle left of a removed ' with ' clause is its head word, not a clause of its own: it goes with it (one removal, one note).
    merged = {}
    for i in range(len(clauses) - 1):
        if not drop[i] and drop[i + 1] and _joined_by_with(clauses[i][1]) and _PARTICIPLE.match(_single_word(clauses[i][0])):
            drop[i] = True
            merged[i] = i + 1
    removed = []
    for i, (c, d) in enumerate(zip(clauses, drop)):
        if not d or i - 1 in merged:
            continue
        text = c[0].rstrip(" .;,")
        removed.append(f"{text} with {clauses[i + 1][0].rstrip(' .;,')}" if i in merged else text)
    notes = [NOTE.format(r) for r in removed]
    left = [c[0] for c, d in zip(clauses, drop) if not d]
    if not left or not any(content_words(c) for c in left):
        return {"text": "", "removed": removed, "kept": [], "supported": False, "notes": notes, "changed": True}
    # T-128 r2 (D-054 'never leave a fragment'), structural, no word list:
    if drop[0]:                                      # (1) the first clause is never removed: an unsupported first clause means the whole summary goes to judge 1
        return unchanged
    first_cut = drop.index(True)
    if len(content_words(" ".join(c[0] for c in clauses[:first_cut]))) < 2:       # (2) the kept prefix must carry at least 2 content words ('Pain.' alone is not a summary)
        return unchanged
    for i in range(1, len(clauses)):                 # (3) a clause joined to a removed one by ',' ' and ' or ' with ' only made sense after it ('..., due to ...', '... and was advised ...')
        if not drop[i] and drop[i - 1] and clauses[i - 1][1].strip().lower() in (",", "and", "with"):
            return unchanged
    out, last_kept = "", None
    for i, ((text, sep), d) in enumerate(zip(clauses, drop)):
        if d:
            continue
        piece = text.rstrip(" .;,")
        if last_kept is None:
            out = piece
        else:
            prev_sep = clauses[last_kept][1]
            use = prev_sep if i - 1 == last_kept else max((clauses[j][1] for j in range(last_kept, i)), key=_strength)
            out = _join(out, use, piece)
        last_kept = i
    out = out[:1].upper() + out[1:]
    if summary.rstrip().endswith("."):
        out += "."
    return {"text": out, "removed": removed, "kept": left, "supported": True, "notes": notes, "changed": True}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:14.930Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-127-r1 && sed -n 1,80p probe_t128.py; echo ======; sed -n 1,40p probe_t128b.py; echo =====; sed -n 1,40p sweep.py; sed -n 1,40p rev.py"
}
````

### User / tool · 2026-11-02T12:01:15.025Z

**tool result**
````
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import summary_trim as T
# (summary, excerpt, label) fragment-prone: a clause is unsupported and removal could leave a stub
P = [
 # noun-phrase stubs
 ("Pain in the neck and lower back.", "Lower back pain."),
 ("Pain in the neck and right shoulder.", "Right shoulder pain."),
 ("Pain in the neck, back and shoulder.", "Shoulder pain."),
 ("Wrist fracture and surgery.", "Surgery."),
 ("Wrist fracture, then splint.", "Splint applied."),
 ("Neck pain and numbness in the hand.", "Hand numbness."),
 ("Laceration repaired with sutures and a dressing.", "Dressing applied."),
 # connector-led stubs, words outside the list
 ("MRI ordered, pending insurance approval.", "MRI approved."),
 ("Knee surgery recommended, requiring six weeks of crutches.", "Crutches issued."),
 ("Neck pain with spasm, prompting a collar.", "Collar given."),
 ("Brace applied, despite swelling.", "Brace applied."),
 ("Ankle sprain, likely from the fall.", "Fall at home."),
 ("Back pain, worse with sitting.", "Sitting tolerance reduced."),
 ("Epidural injection given, after which pain eased.", "Pain eased."),
 ("Wrist cast placed, along with a sling.", "Sling provided."),
 ("Shoulder surgery performed, leading to a sling.", "Sling provided."),
 ("Fracture seen on X-ray, suggesting an old injury.", "Old injury."),
 ("Physical therapy started, plus home exercises.", "Exercises given."),
 ("Neck collar fitted; again advised to rest.", "Advised to rest."),
 ("MRI done; mild disc bulge noted at L4.", "MRI done."),
 ("Sutured laceration, remains tender to touch.", "Sutured laceration."),
 ("Hand numbness; resolved after splinting.", "Numbness."),
 ("Wrist pain, with swelling noted over the scaphoid.", "Wrist pain."),
 ("Patient reports headache and was prescribed ibuprofen.", "Ibuprofen prescribed."),
 ("Rear-ended at a stoplight, now has neck pain.", "Neck pain."),
 ("Neck sprain diagnosed, treated with ice.", "Ice applied."),
 ("Ankle X-ray negative, however pain persists.", "X-ray negative."),
 ("Back pain; also referred to orthopedics.", "Referred to orthopedics."),
 ("Knee brace issued, not weight bearing.", "Brace issued."),
 ("Fracture of the left wrist, cast applied, not yet healed.", "Cast applied."),
 ("Neck pain, no radiation.", "Radiation to arm."),
]
n=0; frag=0
def looks_frag(t):
    import re
    w = re.findall(r"[A-Za-z']+", t.lower())
    return bool(w) and (len(w)==1 or w[0] in T._LEAD or w[0] in T._CONNECTOR)
for s, e in P:
    r = T.trim(s, e)
    n+=1
    flag = r["changed"] and r["text"] and looks_frag(r["text"])
    frag += bool(flag)
    print(("CHANGED " if r["changed"] else "whole   ") + ("FRAG? " if flag else "      ") + repr(s), "|", repr(e), "->", repr(r["text"]) if r["changed"] else "", r["removed"] if r["changed"] else "")
print(n, "probes; changed:", sum(T.trim(s,e)["changed"] for s,e in P))
======
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import summary_trim as T
POS = [   # an unsupported clause exists and a whole supported clause stays: trim SHOULD fire
 ("Neck pain. Surgery recommended. Also reports headaches.", "Neck pain. Headaches reported."),
 ("Was seen at the ER; surgery recommended.", "Seen at ER."),
 ("Neck pain; MRI ordered. Was prescribed ibuprofen.", "Neck pain. Ibuprofen prescribed."),
 ("Back pain; injection given. Is improving.", "Back pain. Improving."),
 ("Neck pain; surgery recommended.", "Neck pain."),
 ("Wrist pain; cast applied; discharged home.", "Wrist pain. Discharged home."),
 ("Knee pain, MRI ordered; then physical therapy.", "Knee pain. Physical therapy."),
 ("Back pain; ultrasound done. Had a follow-up visit.", "Back pain. Follow-up visit."),
 ("Neck pain; epidural given. Which was tolerated.", "Neck pain. Tolerated."),
 ("Shoulder pain; sling provided; pain 7/10.", "Shoulder pain 7/10."),
 ("Ankle sprain; splint applied; follow-up in two weeks.", "Ankle sprain. Follow-up in two weeks."),
 ("Headache; CT scan ordered; ibuprofen advised.", "Headache. Ibuprofen advised."),
]
for s,e in POS:
    r=T.trim(s,e)
    print(("CHANGED " if r["changed"] else "WHOLE   "), repr(s),"|",repr(e),"->",repr(r["text"]) if r["changed"] else "", r["removed"])
=====
import sys, os, re, subprocess, json
root = sys.argv[1]
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
sys.path.insert(0, root); os.chdir(root)
import app.backend.summary_trim as T
keys = [("c", k) for k in T._ABBR_CASE] + [("l", k) for k in T._ABBR]
print(len(keys), "entries")
if len(sys.argv) > 2:
    kind, key = sys.argv[2], sys.argv[3]
    import pytest
    if kind == "c":
        T._ABBR_CASE[key] = "zzqx"
        T._ABBR_CASE_RX = re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(T._ABBR_CASE) + r")(?![A-Za-z0-9/])")
    else:
        T._ABBR[key] = "zzqx"
    sys.exit(pytest.main(["tests/unit/test_summary_trim.py", "-q", "-x", "-p", "no:cacheprovider", "--no-header"]))
surv = []
for kind, key in keys:
    r = subprocess.run([PY, "-I", sys.argv[0], root, kind, key], capture_output=True, text=True, cwd=root)
    if r.returncode == 0:
        surv.append(key)
print("survivors:", surv)
import sys; sys.path.insert(0, sys.argv[1])
import app.backend.summary_trim as T
P = [("ORIF wrist.","Open reduction internal fixation of wrist."),("THA performed.","Total hip arthroplasty performed."),("TKA performed.","Total knee arthroplasty performed."),
 ("RCR performed.","Rotator cuff repair performed."),("ACDF done.","Anterior cervical discectomy and fusion done."),("TPI given.","Trigger point injection given."),
 ("ESI given.","Epidural steroid injection given."),("LLE pain.","Left lower extremity pain."),("BUE numbness.","Bilateral upper extremity numbness."),
 ("DJD noted.","Degenerative joint disease noted."),("CXR negative.","Chest x-ray negative."),("Lac repaired.","Laceration repaired."),
 ("APAP given.","Acetaminophen given."),("CP reported.","Chest pain reported."),("OA noted.","Osteoarthritis noted."),("RA noted.","Rheumatoid arthritis noted."),
 ("IM injection given.","Intramuscular injection given."),("US performed.","Ultrasound performed.")]
for s,e in P:
    r=T.trim(s,e); print("OVERTRIM" if r["changed"] else "ok      ", repr(s),"|",repr(e),"->",repr(r["text"]) if r["changed"] else "")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:16.951Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; sed -n 1,60p $R/app/backend/summary_trim.py; grep -n \"_NEG\\b\\|_NEG_WORDS\\|_NEG =\\|neg_words\\|def split_clauses\\|_SEP\" $R/app/backend/summary_trim.py | head -40"
}
````

### User / tool · 2026-11-02T12:01:17.049Z

**tool result**
````
"""D-054: code removes the clauses of an AI summary that add salient content its own quote lacks, before the judge sees the summary. CODE ONLY (no LLM, no network).

    trim(summary, excerpt, label="", date_iso="") -> {"text", "removed", "kept", "supported", "notes", "changed"}

Why: the generator sometimes summarizes beyond its own excerpt ('Initial consult; left wrist pain 6/10; splint fitted.' over the pain sentence only).
Judge 1 rightly objects, and a ship bar that depends on the model's luck flaps. Trimming by code is deterministic and keeps 'every statement traces to a quote'.

Rule (T-112 r2: remove only what is demonstrably NEW, never a faithful paraphrase; the judge still checks everything that stays):
 1. Split the summary into clauses at ';' ',' sentence-ending '.' and the joins ' and ' / ' with ' (no split inside '1,200', '6.5', 'Dr.', 'approx.', 'e.g.').
 2. A clause is REMOVED only when it carries salient new content, i.e. at least one of these is not in the quote (the record's source label and parsed date also count
    as present, as in grounding.new_tokens):
      a. a number or a month name (D-034; 'six', 'twice', 'x2' in the quote count as 2, 6 ...);   b. a side (left / right / bilateral; 'L', 'lt', 'both' in the quote count);
      c. a negation (no, not, denies ...; any negation-like quote word - normal, unremarkable, unchanged, unable - counts as present);
      d. a procedure, treatment, device or drug term (splint, cast, MRI, injection, surgery, referred, prescribed, ordered, hospitalized, Tylenol ...);
      e. a body part (wrist, neck, lumbar ...);   f. a diagnosis noun (fracture, sprain, concussion, radiculopathy ...).
    a-c count only for a clause that shares no content word with the quote ('for 4 weeks'); a clause on the quote's own topic with a changed value ('Pain 3/10' over
    'Pain 4/10') stays, because the D-034/D-047 code checks flag a number or side the quote lacks and the paralegal sees the conflict. A NEGATION on the quote's own
    topic also stays but is only guaranteed to reach judge 1 and the human: when the quote has the same negation word elsewhere, grounding.new_tokens does not flag it
    ('No cervical strain.' over 'X-ray: no acute fracture. Cervical strain.'). d-f always count.
    A capitalized word inside a clause is a name ('Fennimoor Spine Clinic'), not a body part.
    Clinical abbreviations are spelled out on both sides first (expand_abbreviations: lac, DJD, ESI, BLE, US, IM, C-collar ...), so 'Chin lac.' supports 'Laceration to the chin'.
    Terms (d-f) are matched by word FAMILY (lexicon below): the quote supports a term when it has a word of the same family (Tylenol~acetaminophen, cervical~neck,
    fingers~digits, prescription~prescribed) or of a family that covers it (a bare 'scan' is covered by MRI or CT; 'spine' by neck or back).
 3. A clause with no salient new content STAYS, whatever its other words ('Dizziness reported.' over 'Pt dizzy since crash.'; 'Walks with a cane' over 'Patient ambulating
    with cane'); the judge checks it. Whole clauses only: a kept clause is never edited. Fragments are impossible by CONSTRUCTION, with no word list (T-128 r2, D-054):
      (1) the FIRST clause is never removed: when it is unsupported nothing is trimmed and the whole summary goes to judge 1 (unless every clause is unsupported: rule 4);
      (2) the kept prefix (the clauses before the first removal) has at least 2 content words;
      (3) a clause that was joined to a removed one by ',' ' and ' or ' with ' is not left behind ('..., due to X', '... and was advised to rest'); only ';' or a
          sentence end lets a clause stand alone.
    When a rule says no, the summary is returned unchanged. A lone participle before a removed ' with ' clause ('diagnosed' in 'diagnosed with diabetes') is that clause's
    head word and is removed with it.
 4. If every clause is removed, or the clauses left have no content word at all (stopwords and numbers only), `text` is '' and the caller sends the item to the
    could-not-verify tray (D-053/D-054). A summary with no removal is returned unchanged, byte for byte."""
import re

from app.backend import grounding

NOTE = "removed from the summary: not in the quote: '{}'"

_STOP = frozenset("""
a an the and or but nor of in on at to for from by with without within into onto over under about around per via as is are was were be been being am do does did
has have had having it its this that these those there here then than so such very also too only just not no yes if when while after before during since until
he she they them his her their him we us you your i me my our who whom whose which what where why how can could would should may might will shall must
patient patients pt pts client reports report reported reporting states stated state notes noted note record records documented documents document describes
described describe says said stating denies denied deny negative none never neither absent left right bilateral bilaterally
possible possibly probable probably likely unlikely suspected suspect appears appear appeared apparently approximately approx roughly estimated
one two three four five six seven eight nine ten
now currently today still already again later earlier recently rated rating score scored seen presented presents presenting came
""".split())
_ABBR_BEFORE_PERIOD = frozenset({"dr", "mr", "mrs", "ms", "st", "jr", "sr", "vs", "approx", "e.g", "i.e", "etc", "no", "dept", "inc", "ref", "fig", "cf", "est"})
# Abbreviation and synonym groups: a word in a group is supported by any other word of the group. Deliberately generous (a wrong match only keeps a clause
# the judge then checks; a missed match would remove a faithful clause).
_GROUPS = [
    {"pt", "physical", "therapy", "therapist", "rehab", "rehabilitation"},
    {"hx", "history"}, {"dx", "diagnosis", "diagnosed", "diagnostic", "impression"}, {"tx", "treatment", "treated", "treat", "treating", "therapy"},
    {"rx", "prescription", "prescribed", "medication", "medications", "meds", "med"}, {"sx", "symptom", "symptoms"}, {"fx", "fracture", "fractured"},
    {"ha", "headache", "headaches"}, {"lbp", "low", "back", "pain"}, {"mva", "mvc", "collision", "accident", "crash", "wreck", "vehicle"},
    {"er", "ed", "emergency", "ems", "ambulance"}, {"ortho", "orthopedic", "orthopaedic", "orthopedics", "orthopedist", "orthopedics"},
    {"neuro", "neurology", "neurologic", "neurological", "neurologist"}, {"xray", "radiograph", "radiographs", "radiography", "imaging", "film", "films"},
    {"mri", "imaging", "scan"}, {"ct", "imaging", "scan", "tomography"},
81:_NEG = re.compile(r"\b(?:no|not|none|never|without|denies|denied|deny|negative|neither|nor|absent)\b|n't\b", re.IGNORECASE)
176:def split_clauses(summary: str) -> list:
270:_NEG_WORDS = frozenset({"no", "not", "none", "never", "without", "denies", "denied", "negative", "neither", "nor", "absent"})
273:_QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
338:    sw = grounding.side_neg_words(clause, keep_order=True)
344:        elif w.endswith("n't") or w in _NEG_WORDS:
366:    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if w in _SIDE_WORDS}
376:    neg = bool(_NEG.search(ex) or _QUOTE_NEG.search(ex))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:25.296Z

**tool call — Bash**
````
{
 "command": "git status --short app/ tests/ memory/contracts | head; git diff HEAD --stat -- app/backend/summary_trim.py app/backend/pipeline.py app/backend/present.py; grep -n \"_NEG\\b\\|_NEG_WORDS\\|_QUOTE_NEG\" app/backend/summary_trim.py | head; git log --oneline -3 -- app/backend/summary_trim.py; grep -n \"negation\\|neg\" app/llm/lexicon.yaml | head -20; grep -n \"def view\\|def side_neg_words\\|NEG\" app/backend/grounding.py | head -20"
}
````

### User / tool · 2026-11-02T12:01:25.493Z

**tool result**
````
 M app/backend/api.py
 M app/backend/lexicon_scan.py
 M app/backend/summary_trim.py
 M app/frontend/app.js
 M app/frontend/dom.js
 M app/frontend/review.js
 M tests/unit/test_summary_trim.py
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
 app/backend/summary_trim.py | 12 +++++-------
 1 file changed, 5 insertions(+), 7 deletions(-)
271:_QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
374:    neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
22:#   prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context,
29:# - `negatable: true` → apply the negation guard below. A negated hit is suppressed and logged in the audit.
37:# - examples.hit must fire; examples.miss must not fire; examples.negated must match the regex but be suppressed
46:negation:
48:  # The reference implementation is research/lexicon_selfcheck.py:negated().
50:  pre_cues: ['no', 'not', 'denies', 'denied', 'deny', 'negative for', 'no history of', 'no prior', 'no previous',
60:  # Exception for coordinated negation lists. A comma does NOT end the scope when (1) the hit's own comma-segment
63:  # change." and "ROS: Denies fever, chills, …, or prior neck injury." negated, while
69:  # Field-style answers: a hit followed by ":" (up to three words later) or directly by "-", then a negative
70:  # answer, is negated ("Prior injuries: No.", "Previous accidents: none.", "Pre-existing conditions: none.").
71:  field_answer: '^\s*(?:(?:[\w/''-]+\s*){0,3}?[:?]|-)\s*(?:no|none|n|neg|negative|denies|denied|n/a|nil|0|absent)\b'
72:  pseudo_negations: ['no increase', 'no change', 'not only', 'not necessarily', 'no significant change',
79:    Pseudo-negations contain a negation word but do not negate a finding ("not sure whether she had a prior neck
106:  negatable: false
118:    negated: ['Headache 2026, resolved.']
127:  negatable: true
130:  false_positive: '"No history of neck injury" and "denies history of" are negated. "History of present illness" is a section header, excluded. "Family history of" is excluded (not the patient). "History of" an unrelated disease (asthma) still fires at medium; the LLM judges relevance.'
135:    negated: ['Patient has no history of neck injury.', 'Denies history of back pain.', 'No history of neck or back problems.']
144:  negatable: true
147:  false_positive: '"No hx of trauma" is negated. "HPI" is not matched. "Hx: none" is negated by the field-answer rule.'
148:def side_neg_words(text: str, keep_order: bool = False):
245:def view(*names: str):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:29.270Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- app/backend/summary_trim.py; git diff HEAD --stat -- tests/unit/test_summary_trim.py; date -u; ls -l --time-style=full-iso app/backend/summary_trim.py 2>/dev/null || stat -f \"%Sm\" app/backend/summary_trim.py; git log -1 --format=%cd"
}
````

### User / tool · 2026-11-02T12:01:29.416Z

**tool result**
````
diff --git a/app/backend/summary_trim.py b/app/backend/summary_trim.py
index ce53078..f3dc83b 100644
--- a/app/backend/summary_trim.py
+++ b/app/backend/summary_trim.py
@@ -78,7 +78,6 @@ for _g in _GROUPS:
         _GROUP_OF.setdefault(_w, set()).update(_g)
 
 _WORD = re.compile(r"[a-z]+")
-_NEG = re.compile(r"\b(?:no|not|none|never|without|denies|denied|deny|negative|neither|nor|absent)\b|n't\b", re.IGNORECASE)
 _SUFFIXES = ("ations", "ation", "ments", "ment", "ness", "ings", "ing", "ied", "ies", "ed", "es", "s", "ly", "al")
 _SPLIT = re.compile(r";|,(?!\d)|(?<!\d),|\s+(?:and|with)\s+|\.(?=\s|$)", re.IGNORECASE)
 _STRENGTH = {";": 2, ",": 1, ".": 3}
@@ -267,8 +266,7 @@ _FAMILIES = [
 ]
 _FAM = [(k, n, re.compile(rx), cov, re.compile(qx) if qx else None) for k, n, rx, cov, qx in _FAMILIES]
 _BODY = frozenset(n for k, n, *_ in _FAMILIES if k == "body")
-_NEG_WORDS = frozenset({"no", "not", "none", "never", "without", "denies", "denied", "negative", "neither", "nor", "absent"})
-_SIDE_WORDS = frozenset({"left", "right", "bilateral", "bilaterally"})
+# Negation and side words are the lexicon's (code_lists.added_qualifier through grounding.view / aq), not lists of this module (T-105 r2, T-128 r2).
 # Quote words that already carry a negation or a negative finding: a summary negation is then not NEW content (the judge decides if it is the right one).
 _QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
                         r"nad|nkda|nonspecific)\b|\w+n't\b|\bw/o\b", re.IGNORECASE)
@@ -337,11 +335,11 @@ def new_salient(clause: str, quote: dict) -> list:
             out.append(m.lower())
     sw = grounding.side_neg_words(clause, keep_order=True)
     for w in dict.fromkeys(sw):
-        if w in _SIDE_WORDS:
+        if grounding.aq("side").fullmatch(w):
             ok = w in quote["sides"] or (w.startswith("bilateral") and (quote["both"] or {"left", "right"} <= quote["sides"]))
             if not ok:
                 loose.append(w)
-        elif w.endswith("n't") or w in _NEG_WORDS:
+        elif w.endswith("n't") or grounding.is_negation_word(w):
             if not quote["neg"]:
                 loose.append(w)
     toks = re.findall(r"[A-Za-z0-9]+", clause)
@@ -363,7 +361,7 @@ _LABEL_FAMILIES = frozenset({"mri", "ct", "xray", "ultrasound", "emg", "imaging"
 
 def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
     ex = excerpt or ""
-    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if w in _SIDE_WORDS}
+    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if grounding.aq("side").fullmatch(w)}
     if _QUOTE_LEFT.search(ex + " " + (label or "")):
         sides.add("left")
     if _QUOTE_RIGHT.search(ex + " " + (label or "")):
@@ -373,7 +371,7 @@ def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
     if m:
         month = _MONTHS[int(m.group(1)) - 1]
     low = (ex + " " + (label or "")).lower()
-    neg = bool(_NEG.search(ex) or _QUOTE_NEG.search(ex))
+    neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))
     return {"nums": _number_set(ex, label or "", date_iso or ""), "low": low, "month": month, "sides": sides, "both": bool(_QUOTE_BOTH.search(ex) or _QUOTE_BOTH.search(_prep(ex))), "neg": neg,
             "forms": _quote_forms(ex + " " + (label or "")), "fams": _quote_families(_words(ex)) | {f for f in _quote_families(_words(label or "")) if f in _LABEL_FAMILIES or f in _BODY}}
 
 tests/unit/test_summary_trim.py | 18 ++++++++++++++++++
 1 file changed, 18 insertions(+)
Mon Nov  2 12:01:29 UTC 2026
Nov  2 06:00:45 2026
Mon Nov 2 05:57:25 2026 -0600
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:38.410Z

**tool call — Bash**
````
{
 "command": "grep -n \"def has_negation\\|def is_negation_word\\|def aq\\b\\|def aq(\" app/backend/grounding.py; git diff HEAD --stat | grep -v agent-memory | head -20; git diff HEAD -- tests/unit/test_summary_trim.py"
}
````

### User / tool · 2026-11-02T12:01:38.609Z

**tool result**
````
217:def has_negation(text: str, *, extra: bool = False, ignore: tuple = ()) -> bool:
224:def is_negation_word(w: str) -> bool:
240:def aq(name: str):
 .../backend/project_backend_conventions.md         |    2 +
 .../backend/project_t110_overlap_tray.md           |    6 +
 .../claims-adjuster-reviewer/MEMORY.md             |    9 +
 .../feedback_lexicon_review_method.md              |    5 +
 .../feedback_reviews_write_once.md                 |    9 +
 .../feedback_reviewer_tooling_quirks.md            |   50 +
 .../paralegal-reviewer/library-review-patterns.md  |   16 +
 .../reviewer-hook-constraints.md                   |    1 +
 .../project_pdf_upload_review_patterns.md          |    7 +
 .../project_e2e_contract_review_patterns.md        |    9 +-
 .../project_harness_review_patterns.md             |   17 +
 .../project_split_llm_review_patterns.md           |   12 +
 app/backend/api.py                                 |    4 +-
 app/backend/lexicon_scan.py                        |   21 +-
 app/backend/summary_trim.py                        |   12 +-
 app/frontend/app.js                                |    9 +-
 app/frontend/dom.js                                |    8 +
 app/frontend/review.js                             |   56 +-
 app/frontend/timeline.js                           |   13 +-
 board/activity.jsonl                               | 1641 ++++++++++++++++++++
/bin/bash: child setpgid (85524 to 85524): Operation not permitted
diff --git a/tests/unit/test_summary_trim.py b/tests/unit/test_summary_trim.py
index 9098f12..0d6ebb7 100644
--- a/tests/unit/test_summary_trim.py
+++ b/tests/unit/test_summary_trim.py
@@ -695,3 +695,21 @@ def test_without_its_table_entry_the_pair_is_trimmed(entry, summary, excerpt, mo
         monkeypatch.setattr(T, "_ABBR_CASE_RX", re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(T._ABBR_CASE) + r")(?![A-Za-z0-9/])"))
     r = T.trim(summary, excerpt)
     assert r["changed"], (entry, r)
+
+
+# ---- T-128 r2 / T-105 r2 leftover: negation and side words come from the lexicon (grounding.view), not from private lists in summary_trim ----------------------------
+def test_negation_words_are_the_lexicons_not_a_private_list():
+    import pathlib
+    src = pathlib.Path(T.__file__).read_text()
+    import re
+    assert not re.search(r"^(?:_NEG|_NEG_WORDS|_SIDE_WORDS)\s*=", src, re.M)
+    # 'absence of' / 'lacks' / 'free of' are lexicon negation words (negation_extra): a summary clause that adds one the quote does not have is new content
+    for s in ("Neck pain; absence of numbness.", "Neck pain; lacks radiation.", "Neck pain; free of numbness."):
+        r = T.trim(s, "Neck pain.")
+        assert r["changed"] and r["text"] == "Neck pain.", (s, r)
+    assert not T.trim("Neck pain; absence of numbness.", "Neck pain. Exam unremarkable.")["changed"]        # the quote has a negative finding
+    assert not T.trim("Neck pain; absence of numbness.", "Neck pain. No numbness.")["changed"]
+    assert not T.trim("Neck pain; denies fever.", "Neck pain. Absence of radiation.")["changed"]       # the quote's own 'absence of' is a lexicon negation word
+    assert T.trim("Neck pain; denies fever.", "Neck pain. Radiation to the arm.")["changed"]
+    # a side word comes from the lexicon too
+    assert T.trim("Neck pain; bilaterally tender.", "Neck pain.")["changed"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:01:45.700Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-128-129-r2 && mkdir -p $E && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo\nO=artifacts/review-evidence/T-128-129-127-r1\nsed 's/w\\[0\\] in T._LEAD or w\\[0\\] in T._CONNECTOR/False/' $O/probe_t128.py > $E/probe_t128_r2.py\ncp $O/probe_t128b.py $E/probe_t128b_r2.py; cp $O/sweep.py $E/sweep_r2.py; cp $O/rev.py $E/rev_r2.py\n.venv/bin/python -I $E/probe_t128_r2.py $R | cut -c1-200; echo; .venv/bin/python -I $E/probe_t128b_r2.py $R; echo; .venv/bin/python -I $E/rev_r2.py $R | grep -c OVERTRIM"
}
````

### User / tool · 2026-11-02T12:01:46.165Z

**tool result**
````
/bin/bash: child setpgid (85744 to 85744): Operation not permitted
whole         'Pain in the neck and lower back.' | 'Lower back pain.' ->  
whole         'Pain in the neck and right shoulder.' | 'Right shoulder pain.' ->  
whole         'Pain in the neck, back and shoulder.' | 'Shoulder pain.' ->  
whole         'Wrist fracture and surgery.' | 'Surgery.' ->  
whole         'Wrist fracture, then splint.' | 'Splint applied.' ->  
whole         'Neck pain and numbness in the hand.' | 'Hand numbness.' ->  
whole         'Laceration repaired with sutures and a dressing.' | 'Dressing applied.' ->  
whole         'MRI ordered, pending insurance approval.' | 'MRI approved.' ->  
whole         'Knee surgery recommended, requiring six weeks of crutches.' | 'Crutches issued.' ->  
whole         'Neck pain with spasm, prompting a collar.' | 'Collar given.' ->  
whole         'Brace applied, despite swelling.' | 'Brace applied.' ->  
whole         'Ankle sprain, likely from the fall.' | 'Fall at home.' ->  
whole         'Back pain, worse with sitting.' | 'Sitting tolerance reduced.' ->  
whole         'Epidural injection given, after which pain eased.' | 'Pain eased.' ->  
whole         'Wrist cast placed, along with a sling.' | 'Sling provided.' ->  
whole         'Shoulder surgery performed, leading to a sling.' | 'Sling provided.' ->  
CHANGED       'Fracture seen on X-ray, suggesting an old injury.' | 'Old injury.' -> '' ['Fracture seen on X-ray', 'suggesting an old injury']
whole         'Physical therapy started, plus home exercises.' | 'Exercises given.' ->  
whole         'Neck collar fitted; again advised to rest.' | 'Advised to rest.' ->  
CHANGED       'MRI done; mild disc bulge noted at L4.' | 'MRI done.' -> 'MRI done.' ['mild disc bulge noted at L4']
whole         'Sutured laceration, remains tender to touch.' | 'Sutured laceration.' ->  
CHANGED       'Hand numbness; resolved after splinting.' | 'Numbness.' -> '' ['Hand numbness', 'resolved after splinting']
whole         'Wrist pain, with swelling noted over the scaphoid.' | 'Wrist pain.' ->  
whole         'Patient reports headache and was prescribed ibuprofen.' | 'Ibuprofen prescribed.' ->  
whole         'Rear-ended at a stoplight, now has neck pain.' | 'Neck pain.' ->  
whole         'Neck sprain diagnosed, treated with ice.' | 'Ice applied.' ->  
whole         'Ankle X-ray negative, however pain persists.' | 'X-ray negative.' ->  
whole         'Back pain; also referred to orthopedics.' | 'Referred to orthopedics.' ->  
CHANGED       'Knee brace issued, not weight bearing.' | 'Brace issued.' -> '' ['Knee brace issued', 'not weight bearing']
whole         'Fracture of the left wrist, cast applied, not yet healed.' | 'Cast applied.' ->  
whole         'Neck pain, no radiation.' | 'Radiation to arm.' ->  
31 probes; changed: 4

CHANGED  'Neck pain. Surgery recommended. Also reports headaches.' | 'Neck pain. Headaches reported.' -> 'Neck pain. Also reports headaches.' ['Surgery recommended']
WHOLE    'Was seen at the ER; surgery recommended.' | 'Seen at ER.' ->  []
CHANGED  'Neck pain; MRI ordered. Was prescribed ibuprofen.' | 'Neck pain. Ibuprofen prescribed.' -> 'Neck pain. Was prescribed ibuprofen.' ['MRI ordered']
CHANGED  'Back pain; injection given. Is improving.' | 'Back pain. Improving.' -> 'Back pain. Is improving.' ['injection given']
CHANGED  'Neck pain; surgery recommended.' | 'Neck pain.' -> 'Neck pain.' ['surgery recommended']
CHANGED  'Wrist pain; cast applied; discharged home.' | 'Wrist pain. Discharged home.' -> 'Wrist pain; discharged home.' ['cast applied']
CHANGED  'Knee pain, MRI ordered; then physical therapy.' | 'Knee pain. Physical therapy.' -> 'Knee pain; then physical therapy.' ['MRI ordered']
CHANGED  'Back pain; ultrasound done. Had a follow-up visit.' | 'Back pain. Follow-up visit.' -> 'Back pain. Had a follow-up visit.' ['ultrasound done']
CHANGED  'Neck pain; epidural given. Which was tolerated.' | 'Neck pain. Tolerated.' -> 'Neck pain. Which was tolerated.' ['epidural given']
CHANGED  'Shoulder pain; sling provided; pain 7/10.' | 'Shoulder pain 7/10.' -> 'Shoulder pain; pain 7/10.' ['sling provided']
CHANGED  'Ankle sprain; splint applied; follow-up in two weeks.' | 'Ankle sprain. Follow-up in two weeks.' -> 'Ankle sprain; follow-up in two weeks.' ['splint applied']
WHOLE    'Headache; CT scan ordered; ibuprofen advised.' | 'Headache. Ibuprofen advised.' ->  []

0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:02:22.983Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-128-129-r2 && cat > $E/fresh_t128_r2.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import summary_trim as T\n# (summary, excerpt, expect) expect: W = whole summary stays (no change), T = trims to a whole-clause result, F = a kept later clause must not be a dependent fragment\nP = [\n (\"Neck pain with stiffness; surgery recommended.\", \"Neck pain with stiffness.\", \"T\"),\n (\"Low back pain after the crash; physical therapy prescribed; follow-up in 2 weeks.\", \"Low back pain after the crash. Follow-up in 2 weeks.\", \"T\"),\n (\"Seen at ER for neck pain; CT scan ordered.\", \"Seen at ER for neck pain.\", \"T\"),\n (\"Neck pain; injection given; resulting in relief.\", \"Neck pain. Relief reported.\", \"F\"),\n (\"Wrist pain; splint applied; which helped.\", \"Wrist pain. Helped.\", \"F\"),\n (\"Knee pain; MRI ordered. Pending results.\", \"Knee pain. Results pending.\", \"F\"),\n (\"Neck pain; cast applied; however, improving.\", \"Neck pain. Improving.\", \"F\"),\n (\"Shoulder pain; surgery performed; due to torn labrum.\", \"Shoulder pain. Torn labrum.\", \"F\"),\n (\"Ankle pain; X-ray taken; no fracture.\", \"Ankle pain. No fracture.\", \"T\"),\n (\"Neck pain, injection given, relief noted.\", \"Neck pain. Relief noted.\", \"W\"),\n (\"Pain; MRI ordered; follow-up in 2 weeks.\", \"Pain. Follow-up in 2 weeks.\", \"W\"),\n (\"Neck pain, and surgery recommended.\", \"Neck pain.\", \"T\"),\n (\"Neck pain, MRI ordered and follow-up in two weeks.\", \"Neck pain. Follow-up in two weeks.\", \"W\"),\n (\"Neck pain. Surgery recommended; follow-up in two weeks.\", \"Neck pain. Follow-up in two weeks.\", \"T\"),\n (\"Surgery recommended; neck pain.\", \"Neck pain.\", \"W\"),\n (\"Neck pain; steroid injection given; and physical therapy started.\", \"Neck pain. Physical therapy started.\", \"F\"),\n (\"Back pain; ultrasound done; thereafter, improvement.\", \"Back pain. Improvement.\", \"F\"),\n (\"Back pain; epidural given; as a result, less pain.\", \"Back pain. Less pain.\", \"F\"),\n (\"Wrist fracture; cast applied; including follow-up.\", \"Wrist fracture. Follow-up.\", \"F\"),\n (\"Head injury; CT ordered; negative.\", \"Head injury. Negative.\", \"F\"),\n (\"Neck pain; ibuprofen prescribed; 3 times daily.\", \"Neck pain. Three times daily.\", \"F\"),\n (\"Neck pain; physical therapy started; for six weeks.\", \"Neck pain. Six weeks.\", \"F\"),\n (\"Hip pain; X-ray taken; unremarkable.\", \"Hip pain. Unremarkable.\", \"F\"),\n (\"Neck sprain. MRI ordered. Resolved.\", \"Neck sprain. Resolved.\", \"F\"),\n (\"Whiplash; collar fitted; worn daily.\", \"Whiplash. Worn daily.\", \"F\"),\n (\"Knee pain; brace issued; as needed.\", \"Knee pain. As needed.\", \"F\"),\n]\nfor s,e,x in P:\n    r=T.trim(s,e)\n    print(x, (\"CHANGED\" if r[\"changed\"] else \"whole  \"), repr(s), \"->\", repr(r[\"text\"]) if r[\"changed\"] else \"\", r[\"removed\"] if r[\"changed\"] else \"\")\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo\n.venv/bin/python -I $E/fresh_t128_r2.py $R 2>&1 | grep -v setpgid"
}
````

### User / tool · 2026-11-02T12:02:23.187Z

**tool result**
````
T CHANGED 'Neck pain with stiffness; surgery recommended.' -> 'Neck pain with stiffness.' ['surgery recommended']
T CHANGED 'Low back pain after the crash; physical therapy prescribed; follow-up in 2 weeks.' -> 'Low back pain after the crash; follow-up in 2 weeks.' ['physical therapy prescribed']
T CHANGED 'Seen at ER for neck pain; CT scan ordered.' -> 'Seen at ER for neck pain.' ['CT scan ordered']
F CHANGED 'Neck pain; injection given; resulting in relief.' -> 'Neck pain; resulting in relief.' ['injection given']
F CHANGED 'Wrist pain; splint applied; which helped.' -> 'Wrist pain; which helped.' ['splint applied']
F CHANGED 'Knee pain; MRI ordered. Pending results.' -> 'Knee pain. Pending results.' ['MRI ordered']
F CHANGED 'Neck pain; cast applied; however, improving.' -> 'Neck pain; however, improving.' ['cast applied']
F CHANGED 'Shoulder pain; surgery performed; due to torn labrum.' -> 'Shoulder pain; due to torn labrum.' ['surgery performed']
T CHANGED 'Ankle pain; X-ray taken; no fracture.' -> 'Ankle pain; no fracture.' ['X-ray taken']
W whole   'Neck pain, injection given, relief noted.' ->  
W whole   'Pain; MRI ordered; follow-up in 2 weeks.' ->  
T CHANGED 'Neck pain, and surgery recommended.' -> 'Neck pain.' ['surgery recommended']
W whole   'Neck pain, MRI ordered and follow-up in two weeks.' ->  
T CHANGED 'Neck pain. Surgery recommended; follow-up in two weeks.' -> 'Neck pain. Follow-up in two weeks.' ['Surgery recommended']
W whole   'Surgery recommended; neck pain.' ->  
F CHANGED 'Neck pain; steroid injection given; and physical therapy started.' -> 'Neck pain; physical therapy started.' ['steroid injection given']
F CHANGED 'Back pain; ultrasound done; thereafter, improvement.' -> 'Back pain; thereafter, improvement.' ['ultrasound done']
F CHANGED 'Back pain; epidural given; as a result, less pain.' -> 'Back pain; as a result, less pain.' ['epidural given']
F CHANGED 'Wrist fracture; cast applied; including follow-up.' -> 'Wrist fracture; including follow-up.' ['cast applied']
F CHANGED 'Head injury; CT ordered; negative.' -> 'Head injury; negative.' ['CT ordered']
F CHANGED 'Neck pain; ibuprofen prescribed; 3 times daily.' -> 'Neck pain; 3 times daily.' ['ibuprofen prescribed']
F CHANGED 'Neck pain; physical therapy started; for six weeks.' -> 'Neck pain; for six weeks.' ['physical therapy started']
F CHANGED 'Hip pain; X-ray taken; unremarkable.' -> 'Hip pain; unremarkable.' ['X-ray taken']
F CHANGED 'Neck sprain. MRI ordered. Resolved.' -> 'Neck sprain. Resolved.' ['MRI ordered']
F whole   'Whiplash; collar fitted; worn daily.' ->  
F CHANGED 'Knee pain; brace issued; as needed.' -> 'Knee pain; as needed.' ['brace issued']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:02:43.381Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; grep -n \"Was seen at the ER\\|seen at the ER\\|Seen at\" $R/tests/unit/test_summary_trim.py | head; cd $R && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF' 2>&1 | grep -v setpgid\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import summary_trim as T\nfor s,e in [(\"Was seen at the ER; surgery recommended.\",\"Seen at the ER.\"),(\"Was seen at the ER; surgery recommended.\",\"Seen at ER.\"),(\"Seen at the ER; surgery recommended.\",\"Seen at ER.\")]:\n    r=T.trim(s,e); print(repr(s),repr(e),r[\"changed\"],r[\"text\"], T.content_words(\"Was seen at the ER\"))\nEOF"
}
````

### User / tool · 2026-11-02T12:02:43.576Z

**tool result**
````
614:    r = T.trim("Was seen at the ER; surgery recommended.", "Seen at ER.")
'Was seen at the ER; surgery recommended.' 'Seen at the ER.' False Was seen at the ER; surgery recommended. ['er']
'Was seen at the ER; surgery recommended.' 'Seen at ER.' False Was seen at the ER; surgery recommended. ['er']
'Seen at the ER; surgery recommended.' 'Seen at ER.' False Seen at the ER; surgery recommended. ['er']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:02:47.183Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; sed -n 600,630p $R/tests/unit/test_summary_trim.py"
}
````

### User / tool · 2026-11-02T12:02:47.266Z

**tool result**
````
    ("Wrist pain; cast applied; discharged home.", "Wrist pain. Discharged home.", "Wrist pain; discharged home."),
    ("Neck pain; MRI ordered. Was prescribed ibuprofen.", "Neck pain. Ibuprofen prescribed.", "Neck pain. Was prescribed ibuprofen."),
    ("Neck pain. Surgery recommended. Also reports headaches.", "Neck pain. Headaches.", "Neck pain. Also reports headaches."),
    ("Back pain; injection given. Is improving.", "Back pain. Improving.", "Back pain. Is improving."),
    ("Back pain; ultrasound done. Had a follow-up visit.", "Back pain. Follow-up visit.", "Back pain. Had a follow-up visit."),
    ("Pain in the neck and back.", "Neck pain.", "Pain in the neck."),
    ("Initial consult; left wrist pain 6/10; splint fitted.", "Patient reports left wrist pain 6/10.", "Initial consult; left wrist pain 6/10."),
])
def test_unsupported_later_clauses_still_trim_when_a_whole_clause_is_left(summary, excerpt, want):
    r = T.trim(summary, excerpt)
    assert r["changed"] and r["text"] == want, r


def test_the_first_clause_is_never_removed():
    r = T.trim("Was seen at the ER; surgery recommended.", "Seen at ER.")
    assert not r["changed"]                                                                  # nothing is removed before the first clause stands
    r = T.trim("Surgery recommended; neck pain.", "Neck pain.")
    assert not r["changed"] and r["removed"] == []                                           # an unsupported FIRST clause: whole summary to the judge
    r = T.trim("Splint fitted.", PAIN)
    assert r["text"] == "" and r["removed"] == ["Splint fitted"]                             # nothing at all supported: the tray, as before
    r = T.trim("Splint fitted; cast applied.", PAIN)
    assert r["text"] == "" and not r["supported"]


def test_a_kept_prefix_with_fewer_than_two_content_words_is_not_trimmed():
    assert not T.trim("Pain; splint fitted.", "Fell on back. Pain.")["changed"]
    assert not T.trim("Headache; knee brace given.", "Headache daily.")["changed"]
    assert not T.trim("Pain with radiculopathy.", "Pain 5/10.")["changed"]
    assert T.trim("Back pain with radiculopathy.", "Back pain 5/10.")["text"] == "Back pain."      # two content words: fine
    assert not T.trim("Pain; splint fitted; swelling noted; cast applied.", "Pain. Swelling noted.")["changed"]          # the prefix is what comes before the FIRST removal, not the last
    assert T.trim("Pain; swelling noted; splint fitted.", "Pain. Swelling noted.")["text"] == "Pain; swelling noted."    # 'Pain; swelling noted' is two content words before the first removal
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:02:54.681Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; time .venv/bin/python -I $E/sweep_r2.py $R 2>&1 | grep -v setpgid; grep -n \"orif\\|'iv'\\|\\\"iv\\\"\\|hep\\b\\|ekg\\|\\\"IV\\\"\" $R/app/backend/summary_trim.py | head",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T12:02:55.567Z

**tool result**
````
27 entries
survivors: []

real	0m0.714s
user	0m0.436s
sys	0m0.185s
101:         "rcr": "rotator cuff repair surgery", "tka": "total knee arthroplasty surgery", "tha": "total hip arthroplasty surgery", "orif": "open reduction internal fixation surgery",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:03:00.387Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; .venv/bin/python -I $E/sweep_r2.py $R l hep 2>&1 | tail -8; pwd"
}
````

### User / tool · 2026-11-02T12:03:02.231Z

**tool result**
````
27 entries
........................................................................ [ 25%]
........................................................................ [ 50%]
........................................................................ [ 75%]
.....................................................................    [100%]
285 passed in 1.50s
/Users/arsis/zlayt-pm-project
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:03:07.922Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; time .venv/bin/python -I $E/sweep_r2.py $R 2>&1 | grep -v setpgid; echo; .venv/bin/python -I $E/rev_r2.py $R | grep -v setpgid | grep -c OVERTRIM",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T12:03:27.429Z

**tool result**
````
27 entries
survivors: []

real	0m19.303s
user	0m16.530s
sys	0m2.609s

0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:03:44.181Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; cat > $E/mut_t128_r2.py <<'EOF'\nimport sys, subprocess, pathlib\nroot = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nf = root/\"app/backend/summary_trim.py\"; orig = f.read_text()\nM = [\n (\"prefix<2 -> <1\", \"content_words(\\\" \\\".join(c[0] for c in clauses[:first_cut]))) < 2\", \"content_words(\\\" \\\".join(c[0] for c in clauses[:first_cut]))) < 1\"),\n (\"prefix<2 -> <3\", \"content_words(\\\" \\\".join(c[0] for c in clauses[:first_cut]))) < 2\", \"content_words(\\\" \\\".join(c[0] for c in clauses[:first_cut]))) < 3\"),\n (\"prefix up to LAST cut\", \"first_cut = drop.index(True)\", \"first_cut = len(drop) - 1 - drop[::-1].index(True)\"),\n (\"rule3 off\", \"(\\\",\\\", \\\"and\\\", \\\"with\\\"):\\n            return unchanged\", \"(\\\"zz\\\",):\\n            return unchanged\"),\n (\"rule3 no comma\", \"in (\\\",\\\", \\\"and\\\", \\\"with\\\")\", \"in (\\\"and\\\", \\\"with\\\")\"),\n (\"rule3 no and\", \"in (\\\",\\\", \\\"and\\\", \\\"with\\\")\", \"in (\\\",\\\", \\\"with\\\")\"),\n (\"rule3 no with\", \"in (\\\",\\\", \\\"and\\\", \\\"with\\\")\", \"in (\\\",\\\", \\\"and\\\")\"),\n (\"rule3 ignores prev removed\", \"if not drop[i] and drop[i - 1] and clauses[i - 1][1]\", \"if not drop[i] and clauses[i - 1][1]\"),\n (\"rule1 off\", \"if drop[0]:\", \"if False:\"),\n (\"tray: no-content-left off\", \"if not left or not any(content_words(c) for c in left):\", \"if not left:\"),\n (\"participle merge off\", \"and _PARTICIPLE.match(_single_word(clauses[i][0])):\", \"and False:\"),\n (\"join keeps weakest sep\", \"key=_strength)\", \"key=lambda s: -_strength(s))\"),\n (\"capitalise off\", \"out = out[:1].upper() + out[1:]\", \"pass\"),\n (\"final period dropped\", \"if summary.rstrip().endswith(\\\".\\\"):\\n        out += \\\".\\\"\", \"pass\"),\n (\"no-removal returns changed\", \"if not any(drop):\\n        return unchanged\", \"if not any(drop):\\n        return dict(unchanged, changed=True)\"),\n (\"qx (quote negation) off\", \"neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))\", \"neg = bool(grounding.has_negation(ex, extra=True))\"),\n]\nM[-1] = (\"quote-neg regex off (HEAD form)\", \"neg = bool(_NEG.search(ex) or _QUOTE_NEG.search(ex))\", \"neg = bool(_NEG.search(ex))\")\nsurv = []\nfor name, a, b in M:\n    if orig.count(a) < 1:\n        print(\"NOT FOUND\", name); continue\n    f.write_text(orig.replace(a, b, 1))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", \"tests/unit/test_summary_trim.py\", \"-q\", \"-x\", \"-p\", \"no:cacheprovider\", \"--no-header\"], cwd=root, capture_output=True, text=True)\n    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-100:]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", tail)\n    if not r.returncode: surv.append(name)\nf.write_text(orig)\nprint(\"survivors:\", surv)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; .venv/bin/python -I $E/mut_t128_r2.py $R 2>&1 | grep -v setpgid; diff <(git -C /Users/arsis/zlayt-pm-project show HEAD:app/backend/summary_trim.py) $R/app/backend/summary_trim.py && echo restored",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T12:03:57.163Z

**tool result**
````
KILLED   prefix<2 -> <1 | 1 failed, 211 passed in 0.37s
KILLED   prefix<2 -> <3 | 1 failed, 211 passed in 0.36s
KILLED   prefix up to LAST cut | 1 failed, 249 passed in 0.87s
KILLED   rule3 off | 1 failed, 91 passed in 0.32s
KILLED   rule3 no comma | 1 failed, 250 passed in 1.05s
KILLED   rule3 no and | 1 failed, 91 passed in 0.32s
KILLED   rule3 no with | 1 failed, 250 passed in 0.84s
KILLED   rule3 ignores prev removed | 1 failed, 92 passed in 0.33s
SURVIVED rule1 off | 285 passed in 0.88s
KILLED   tray: no-content-left off | 1 failed, 79 passed in 0.25s
KILLED   participle merge off | 1 failed, 211 passed in 0.37s
KILLED   join keeps weakest sep | 1 failed, 91 passed in 0.32s
SURVIVED capitalise off | 285 passed in 1.02s
KILLED   final period dropped | 1 failed in 0.22s
KILLED   no-removal returns changed | 1 failed, 2 passed in 0.21s
KILLED   quote-neg regex off (HEAD form) | 1 failed, 253 passed in 1.42s
survivors: ['rule1 off', 'capitalise off']
restored
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:01.538Z

**tool call — Bash**
````
{
 "command": "git show 1f0a164 --stat | head -20; git show 1f0a164 -- app/backend/pipeline.py app/backend/present.py memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T12:04:01.665Z

**tool result**
````
commit 1f0a164eebb5ed508adea86497e0141bb67fcd95
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:57:25 2026 -0600

    fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/pipeline.py   | 40 +++++++++++++++++++++++++++++++----
 app/backend/present.py    | 12 +++++++++--
 memory/contracts/api.md   |  8 +++----
 tests/unit/test_ingest.py | 54 +++++++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 104 insertions(+), 10 deletions(-)
commit 1f0a164eebb5ed508adea86497e0141bb67fcd95
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:57:25 2026 -0600

    fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index a504bf9..d317e06 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -143,13 +143,45 @@ def _store_split_failure(conn, cid: str, reason) -> None:
     DB.update_case(conn, cid, config_json=cfg or None)
 
 
-def _store_records(conn, cid: str, ing: dict) -> None:
+def _store_record_marks(conn, cid: str, ing: dict) -> None:
+    """T-129: which stored records are unsplit text (D-027) and which of those is a preamble, kept in the case config so GET case serves them (record_view)."""
+    marks = {"unsplit_records": [r["id"] for r in ing["records"] if r.get("unsplit")], "preamble_records": [r["id"] for r in ing["records"] if r.get("preamble")]}
+    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
+    if all(cfg.get(k, []) == v for k, v in marks.items()):
+        return
+    for k, v in marks.items():
+        if v:
+            cfg[k] = v
+        else:
+            cfg.pop(k, None)
+    DB.update_case(conn, cid, config_json=cfg or None)
+
+
+def _item_record_ids(item: dict) -> list:
+    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
+
+
+def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
+    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
+    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
+    if not moved:
+        return
+    for kind in ("entry", "amount", "flag"):
+        for it in DB.list_items(conn, cid, kind):
+            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
+                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
+
+
+def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
     """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
     or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
     before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
+    _store_record_marks(conn, cid, ing)
     stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
     if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
         return
+    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
+    _reset_reviewed_on(conn, cid, {i for i, a, b in stored if new_spans.get(i) != (a, b)}, now)
     conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
     try:
         conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
@@ -215,7 +247,7 @@ def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
 def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
     """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
     ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
-    _store_records(conn, cid, ing)
+    _store_records(conn, cid, ing, now)
     _persist(conn, cid, "flag", ing["flags"], now)
     _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
     DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
@@ -284,7 +316,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     _store_split_failure(conn, cid, ing.get("split_failure"))
     if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
         errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
-    _store_records(conn, cid, ing)
+    _store_records(conn, cid, ing, clock())
     dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
     entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
     code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
@@ -365,9 +397,9 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
     final_amounts = [_clean(a) for a in final_amounts]
     damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
+    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
     PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
-    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
     now_t = clock()
     _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
     _persist(conn, cid, "amount", final_amounts, now_t)
diff --git a/app/backend/present.py b/app/backend/present.py
index 70858c1..ada5b21 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -143,7 +143,14 @@ _ID_KIND = {"e": "entry", "a": "amount", "f": "flag"}
 
 
 def _recs_by_id(conn, case_id):
-    return {r["id"]: r for r in (DB._decode(x) for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)))}
+    cfg = (DB.get_case(conn, case_id) or {}).get("config") or {}
+    unsplit, pre = set(cfg.get("unsplit_records") or []), set(cfg.get("preamble_records") or [])      # T-129: stored by pipeline._store_record_marks
+    out = {}
+    for x in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
+        r = DB._decode(x)
+        r["unsplit"], r["preamble"] = r["id"] in unsplit, r["id"] in pre
+        out[r["id"]] = r
+    return out
 
 
 def item_view(conn, case_id, item_id):
@@ -210,7 +217,8 @@ def record_view(r, raw, with_sentences=True, pages=None):
     v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
          "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
          "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
-         "char_end": r["char_end"], "text": block, "language": language.block_lang(block)}
+         "char_end": r["char_end"], "text": block, "language": language.block_lang(block),
+         "unsplit": bool(r.get("unsplit")), "preamble": bool(r.get("preamble"))}      # T-129: text outside any recognised record (D-027); a preamble sits above the first real record
     if pages:                                    # PDF source (D-031): the page where the record starts
         v["page"] = pdf_text.page_for(pages, r["char_start"])
         from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index eee97ce..e5c532b 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -66,14 +66,14 @@ Request text is normalised first (CRLF and CR become LF; leading/trailing whites
   "demo_mode": true, "record_count": 9, "split_method": "code",
   "records": [
     { "id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09",
-      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true,
+      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false,
       "char_start": 106, "char_end": 313,
       "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"" } ],
   "dates_to_confirm": [],
   "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
   "warnings": [] }
 ```
-(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
+(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
 
 ## POST /api/cases/pdf (D-031)
 Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
@@ -135,7 +135,7 @@ Read once, then patch local state from review responses. `entries` are **chronol
   "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
   "records": [
     { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
-      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
+      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
       "sentences": [ {"text": "Dx: cervical strain;", "start": 396, "end": 416}, {"text": "concussion without loss of consciousness.", "start": 417, "end": 458}, {"text": "CT head negative.", "start": 459, "end": 476},
                      {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
   "undated_entries": [],
@@ -729,7 +729,7 @@ Languages: English and Spanish. Code detects the language of every record (`app/
 - **Not covered:** amounts in Spanish records are classified by the English billing phrases, so a Spanish charge or rate is usually `unclear` and goes to the paralegal (T-084 reclassify); Latin-American `$1.250,00` figures are read as `$1.250` with no value (`unclear`), never as a wrong number.
 
 ## Summary clause trimming (T-112, D-054)
-Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the joins ` and ` / ` with `) and removes a clause only when it adds salient content its own quote lacks (T-112 r2): a procedure/treatment/device/drug term, a body part, or a diagnosis noun that the quote (and, for body part, side and imaging modality, the record's source label) does not have, matched by word family (Tylenol~acetaminophen, cervical~neck, fingers~digits). A number, month, side or negation the quote lacks counts only for a clause that shares no content word with the quote. A changed number or side on the quote's own topic stays and is flagged `needs_review` by the D-034/D-047 code checks (which look for the word anywhere in the quote); a negation on the quote's own topic also stays but is only guaranteed to reach judge 1 and the paralegal: if the quote has the same negation word elsewhere (`No cervical strain.` over `X-ray: no acute fracture. Cervical strain.`), the token check does not flag it. Clinical abbreviations are spelled out on both sides before matching (lac, DJD, OA, RA, ESI, TPI, BLE/LLE/RLE/LE, BUE/LUE/RUE/UE, US, IM, C-collar, APAP, CP, ORIF, TKA and similar), so a faithful expansion is not trimmed. A clause with no such content stays even if none of its words appear in the quote ("Dizziness reported." over "Pt dizzy since crash."): judge 1 still checks it. Whole clauses only; if removing would leave a fragment (a clause starting with an article or preposition, or a lone noun left after a removed ` with ` clause: `Laceration repaired with sutures.` never becomes `Sutures.`), nothing is trimmed; a lone participle before a removed ` with ` clause goes with it (`diagnosed with diabetes` is one removal). Nothing else changes: the model's original output stays in `ladder.generator.output`, and `ladder.summary_trim = {rule, original_summary, removed[], notes[], kept_summary}` records what code removed (`notes[i]` = "removed from the summary: not in the quote: '<clause>'"). The entry's `summary` is the kept text; judge 1 and every later check see it. If every clause is removed (or what is left has no content word), no entry is made: the record gets a could-not-verify tray placeholder with reason `SUMMARY_NOT_IN_QUOTE` (state `rejected`, `ladder.failure`, not an error in `errors[]`). Human-written summaries (edit, manual entry) are never trimmed (D-047 refuses an unsupported one), and neither are summaries of Spanish or uncertain-language records (D-050 makes those needs_review anyway). Frontend: show the `summary_trimmed` trace step when present; a tray item with reason `SUMMARY_NOT_IN_QUOTE` uses the same wording as other placeholders (the `why` sentence names the cause).
+Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the joins ` and ` / ` with `) and removes a clause only when it adds salient content its own quote lacks (T-112 r2): a procedure/treatment/device/drug term, a body part, or a diagnosis noun that the quote (and, for body part, side and imaging modality, the record's source label) does not have, matched by word family (Tylenol~acetaminophen, cervical~neck, fingers~digits). A number, month, side or negation the quote lacks counts only for a clause that shares no content word with the quote. A changed number or side on the quote's own topic stays and is flagged `needs_review` by the D-034/D-047 code checks (which look for the word anywhere in the quote); a negation on the quote's own topic also stays but is only guaranteed to reach judge 1 and the paralegal: if the quote has the same negation word elsewhere (`No cervical strain.` over `X-ray: no acute fracture. Cervical strain.`), the token check does not flag it. Clinical abbreviations are spelled out on both sides before matching (lac, DJD, OA, RA, ESI, TPI, BLE/LLE/RLE/LE, BUE/LUE/RUE/UE, US, IM, C-collar, APAP, CP, ORIF, TKA and similar), so a faithful expansion is not trimmed. A clause with no such content stays even if none of its words appear in the quote ("Dizziness reported." over "Pt dizzy since crash."): judge 1 still checks it. Whole clauses only, and fragments are impossible by construction (T-128 r2, no word list): the FIRST clause is never removed (an unsupported first clause means nothing is trimmed and the whole summary goes to judge 1; a summary with every clause unsupported still goes to the tray), the kept prefix (the clauses before the first removal) must have at least 2 content words, and a clause joined to a removed one by `,` ` and ` or ` with ` is not left behind (only `;` or a sentence end lets a clause stand alone: `Laceration repaired with sutures.` never becomes `Sutures.`); when a rule says no, nothing is trimmed; a lone participle before a removed ` with ` clause goes with it (`diagnosed with diabetes` is one removal). Nothing else changes: the model's original output stays in `ladder.generator.output`, and `ladder.summary_trim = {rule, original_summary, removed[], notes[], kept_summary}` records what code removed (`notes[i]` = "removed from the summary: not in the quote: '<clause>'"). The entry's `summary` is the kept text; judge 1 and every later check see it. If every clause is removed (or what is left has no content word), no entry is made: the record gets a could-not-verify tray placeholder with reason `SUMMARY_NOT_IN_QUOTE` (state `rejected`, `ladder.failure`, not an error in `errors[]`). Human-written summaries (edit, manual entry) are never trimmed (D-047 refuses an unsupported one), and neither are summaries of Spanish or uncertain-language records (D-050 makes those needs_review anyway). Frontend: show the `summary_trimmed` trace step when present; a tray item with reason `SUMMARY_NOT_IN_QUOTE` uses the same wording as other placeholders (the `why` sentence names the cause).
 
 ## DELETE /api/cases/{token}
 `204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:13.733Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-128-129-127-r1/upg129.py; cat artifacts/review-evidence/T-128-129-127-r1/api129.py | head -40; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S/T128_9_127_r1/; git show 1f0a164 -- tests/unit/test_ingest.py"
}
````

### User / tool · 2026-11-02T12:04:13.839Z

**tool result**
````
import sys, os
root, db, step = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root); os.chdir(root)
os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
from app.db import db as DB
from app.backend import pipeline, present, review
def rec(date, src, ex): return f'Date: {date}\nSource: {src}\nExcerpt: "{ex}"'
text = "FAX COVER SHEET\nTo: Dr X\n---\n" + "\n---\n".join([rec("2026-01-09","Lakeside Clinic, intake","Intake done."), rec("2026-03-20","Lakeside Clinic, follow-up","Neck pain improving.")])
conn = DB.connect(db)
if step == "old":
    cid = DB.create_case(conn, text, now=1.0, name="x", source="paste", backend="fixture", demo_mode=0)
    pipeline.ingest_case(conn, cid, text, 1.0)
    gap = [f for f in DB.list_items(conn, cid, "flag") if f["type"]=="gap"][0]
    review.apply_review(conn, cid, gap["id"], {"action": "accept"}, now=2.0)
    print("old:", cid, [(r["id"], r["date_iso"]) for r in present._recs_by_id(conn, cid).values()], [(f["id"], f["review_status"], f["computed"].get("days")) for f in DB.list_items(conn, cid, "flag")])
    open(db + ".cid", "w").write(cid)
else:
    cid = open(db + ".cid").read()
    pipeline.ingest_case(conn, cid, text, 3.0)
    print("new:", [(r["id"], r["date_iso"]) for r in present._recs_by_id(conn, cid).values()], [(f["id"], f["review_status"], f["computed"].get("days"), f["computed"].get("record_ids") or f.get("record_ids")) for f in DB.list_items(conn, cid, "flag")])
import sys, os, tempfile, json
root, label = sys.argv[1], sys.argv[2]
sys.path.insert(0, root); os.chdir(root)
os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
for k in ("ENABLE_LIVE","ANTHROPIC_API_KEY"): os.environ.pop(k, None)
from app.db import db as DB
from app.backend import pipeline, present
d = tempfile.mkdtemp(); path = d + "/t.sqlite"
conn = DB.connect(path)
R1='Date: 2026-01-09\nSource: Lakeside Clinic, intake form\nExcerpt: "Patient completed intake paperwork."'
R2='Date: 2026-01-16\nSource: Lakeside Clinic, initial evaluation\nExcerpt: "Seen for neck pain."'
for name, text in {"preamble": "FAX COVER SHEET\nTo: Dr X\n---\n"+R1+"\n---\n"+R2, "midnote": R1+"\n---\nfree text between\n---\n"+R2}.items():
    cid = DB.create_case(conn, text, now=1.0, name=name, source="paste", backend="fixture", demo_mode=0)
    ing = pipeline.ingest_case(conn, cid, text, 1.0)
    recs = [present.record_view(r, text, with_sentences=False) for r in present._recs_by_id(conn, cid).values()]
    print(label, name, "record_view keys:", sorted(recs[0].keys()))
    print(label, name, [(r["id"], r["seq"], r["char_start"], r.get("unsplit"), r.get("preamble"), r["text"][:18].replace("\n","|")) for r in sorted(recs, key=lambda r: r["seq"])])
    print(label, name, "flags:", [(f["id"], f["category"], f["record_ids"]) for f in DB.list_items(conn, cid, "flag")])
mut
parent
repo
scripts
unit_full.txt
upg
commit 1f0a164eebb5ed508adea86497e0141bb67fcd95
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:57:25 2026 -0600

    fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_ingest.py b/tests/unit/test_ingest.py
index d9d7bba..6dbdb15 100644
--- a/tests/unit/test_ingest.py
+++ b/tests/unit/test_ingest.py
@@ -168,3 +168,57 @@ def test_no_preamble_means_no_extra_record_and_the_library_wording_is_set_aside(
 def test_text_between_records_is_numbered_after_the_real_records_and_is_not_a_preamble():
     out = I.ingest(_REC1 + "\n---\nfree text between separators\n---\n" + _REC2)
     assert [(r["n"], r["unsplit"], r["preamble"]) for r in out["records"]] == [(1, False, False), (2, False, False), (3, True, False)]
+
+
+# ---- T-129 round 2 (reviews/T-129-staff-engineer.md): GET case serves unsplit/preamble; a re-run never leaves a decision on a shifted record number -----------------
+from app.backend import pipeline as _PL  # noqa: E402
+from app.db import db as _DB  # noqa: E402
+
+_COVER = "FAX COVER SHEET\nTo: Dr X\nPages: 3"
+
+
+def test_get_case_serves_unsplit_and_preamble_on_every_record(tmp_path):
+    """present.case_view is exactly what GET /api/cases/{token} returns."""
+    from app.backend import present
+    conn = _DB.connect(str(tmp_path / "t129.sqlite"))
+
+    def served(text):
+        cid = _DB.create_case(conn, text, now=1.0)
+        _PL.ingest_case(conn, cid, text, 1.0)
+        return present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["records"]
+    recs = served(_COVER + "\n---\n" + _REC1 + "\n---\n" + _REC2)
+    assert [(r["id"], r["unsplit"], r["preamble"]) for r in recs] == [("r1", False, False), ("r2", False, False), ("r3", True, True)]
+    assert "FAX COVER SHEET" in recs[2]["text"]
+    assert [(r["unsplit"], r["preamble"]) for r in served(_REC1 + "\n---\nfree note\n---\n" + _REC2)] == [(False, False), (False, False), (True, False)]
+    assert not any(r["unsplit"] or r["preamble"] for r in served(_REC1 + "\n---\n" + _REC2))
+
+
+def test_a_rerun_after_the_numbering_changed_resets_decisions_made_on_shifted_records(tmp_path):
+    """Stored under the OLD numbering (a dated 'cover' record 1, the two visits r2 and r3, the gap between r2 and r3 accepted); the new code numbers the same paste
+    r1, r2 and the cover text r3. The accepted gap must not stay on r2/r3: it goes back to pending (the event log keeps the accept) and the stale row is gone."""
+    conn = _DB.connect(str(tmp_path / "up.sqlite"))
+    old_text = 'Date: 2025-12-01\nSource: Cover\nExcerpt: "Fax cover sheet."\n---\n' + _REC1 + "\n---\n" + _REC2.replace("2026-01-16", "2026-03-20")
+    cid = _DB.create_case(conn, old_text, now=1.0)
+    _PL.ingest_case(conn, cid, old_text, 1.0)
+    gap = next(f for f in _DB.list_items(conn, cid, "flag") if f["type"] == "gap" and f["id"] == "f_gap_r2_r3")
+    _DB.apply_review(conn, gap["id"], "accept", now=2.0, case=cid)
+    assert _DB.get_item(conn, gap["id"], cid)["review_status"] == "accepted"
+    new_text = _COVER + "\n---\n" + _REC1 + "\n---\n" + _REC2.replace("2026-01-16", "2026-03-20")
+    _PL.ingest_case(conn, cid, new_text, 3.0)
+    flags = {f["id"]: f for f in _DB.list_items(conn, cid, "flag") if f["type"] == "gap"}
+    assert "f_gap_r2_r3" not in flags, "the stale row (decided on other records) is gone"
+    assert flags["f_gap_r1_r2"]["review_status"] == "pending"
+    assert [e["action"] for e in _DB.list_events(conn, cid, "f_gap_r2_r3")] == ["accept", "reset"]
+    for f in _DB.list_items(conn, cid, "flag"):                       # no decided flag points at a record that is not what it was decided on
+        assert f["review_status"] == "pending"
+
+
+def test_a_rerun_with_the_same_numbering_keeps_decisions(tmp_path):
+    conn = _DB.connect(str(tmp_path / "same.sqlite"))
+    text = _REC1 + "\n---\n" + _REC2.replace("2026-01-16", "2026-03-20")
+    cid = _DB.create_case(conn, text, now=1.0)
+    _PL.ingest_case(conn, cid, text, 1.0)
+    gap = next(f for f in _DB.list_items(conn, cid, "flag") if f["type"] == "gap")
+    _DB.apply_review(conn, gap["id"], "accept", now=2.0, case=cid)
+    _PL.ingest_case(conn, cid, text, 3.0)
+    assert _DB.get_item(conn, gap["id"], cid)["review_status"] == "accepted"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:20.907Z

**tool call — Bash**
````
{
 "command": "grep -n \"ZLAYT_DB\\|PORT\\|def main\\|__main__\\|ZLAYT_MODE\" app/backend/api.py | head -20; cat run.sh 2>/dev/null | head -20; grep -n \"ZLAYT_DB\\|ZLAYT_PORT\" -r app/config.py app/db/db.py 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T12:04:21.003Z

**tool result**
````
80:    return os.environ.get("ZLAYT_MODE") == "local"
94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
550:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
584:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:22.451Z

**tool call — Bash**
````
{
 "command": "sed -n 85,130p app/backend/api.py; cat tools/serve_app.sh | head -30; grep -rn \"create_app\\|TestClient\\|test_client\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T12:04:22.555Z

**tool result**
````
    host = request.client.host if request.client else None
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
tests/unit/test_api.py:5:from fastapi.testclient import TestClient
tests/unit/test_api.py:14:    return TestClient(app)
tests/unit/test_api_routes.py:7:from fastapi.testclient import TestClient
tests/unit/test_api_routes.py:9:from app.backend.api import create_app
tests/unit/test_api_routes.py:21:    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:28.920Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_api_routes.py; grep -n \"def post_case\\|/api/cases\\\"\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-02T12:04:29.021Z

**tool result**
````
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
218:    @app.get("/api/cases")
234:    @app.post("/api/cases", status_code=201)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:40.894Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2/repo; sed -n 150,260p $R/app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T12:04:40.993Z

**tool result**
````
    if all(cfg.get(k, []) == v for k, v in marks.items()):
        return
    for k, v in marks.items():
        if v:
            cfg[k] = v
        else:
            cfg.pop(k, None)
    DB.update_case(conn, cid, config_json=cfg or None)


def _item_record_ids(item: dict) -> list:
    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])


def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
    if not moved:
        return
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, cid, kind):
            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)


def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
    _store_record_marks(conn, cid, ing)
    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
        return
    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
    _reset_reviewed_on(conn, cid, {i for i, a, b in stored if new_spans.get(i) != (a, b)}, now)
    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
    try:
        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
        for r in ing["records"]:
            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
                          encounter=int(r["encounter"]))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _row(kind: str, it: dict) -> dict:
    ladder = _clean(it.get("ladder") or {})
    if kind == "entry":
        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    if kind == "amount":
        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "endpoint_warnings", "conditional") if k in it}
    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}


def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    for it in items:
        old = existing.get(it["id"])
        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        row = _row(kind, it)
        if old is None:
            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
            continue
        DB.update_item(conn, it["id"], now=now, case=cid, **row)
        if kind == "flag" and old["review_status"] != "pending":
            oc = old.get("computed") or {}
            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing, now)
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:04:46.706Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -4; git status --short app/backend/summary_trim.py tests/unit/test_summary_trim.py; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/T128_9_r2b/repo && git archive HEAD | tar -x -C $S/T128_9_r2b/repo && cd $S/T128_9_r2b/repo && git -C /Users/arsis/zlayt-pm-project rev-parse HEAD; grep -n \"_NEG\\b\\|_NEG_WORDS\\|_SIDE_WORDS\\|has_negation\\|is_negation_word\\|aq(\" app/backend/summary_trim.py; sed -n 205,260p app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T12:04:47.356Z

**tool result**
````
2790918 refactor(backend): summary_trim reads negation and side words from the lexicon (T-105 r2 leftover)
f4d68bb fix(backend): T-132 attribution-only history unit extends to the next clause; MS is not Ms.; pin the history-word gate
1f0a164 fix(backend): T-129 r2 serve unsplit and preamble on GET case; a re-run resets decisions on shifted record numbers
180138c fix(backend): T-128 r2 structural no-fragment rule (first clause kept, 2-word prefix, no dangling joins), inert abbreviations removed
27909187c2c6585d2128fc7d6d543d60dacee3f2
271:_QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
338:        if grounding.aq("side").fullmatch(w):
342:        elif w.endswith("n't") or grounding.is_negation_word(w):
364:    sides = {w for w in grounding.side_neg_words(ex + " " + (label or "")) if grounding.aq("side").fullmatch(w)}
374:    neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))
        if w.split()[0] in ("about", "around") and aq("approximation_preposition_context").search(text[max(0, m.start() - 40):m.start()]):
            continue
        out.append(w)
    return out


def negation_words(text: str) -> list:
    """The negation words in the text (lower case, in order); every contraction is the word 'not'."""
    return ["not" if w.endswith("n't") else w for w in (re.sub(r"\s+", " ", m.group(0)).lower() for m in
                                                        view("negation_word", "negation_contraction").finditer(text.replace("\u2019", "'")))]


def has_negation(text: str, *, extra: bool = False, ignore: tuple = ()) -> bool:
    """Any negation wording; extra=True also accepts the looser words (absence of, lacks, free of, nothing, unremarkable, ruled out).
    `ignore` lists words that do not count (the Spanish helper ignores 'no': in a Spanish quote it is the Spanish cue list's word)."""
    names = ("negation_word", "negation_contraction") + (("negation_extra", "negation_ruled_out") if extra else ())
    return any(m.group(0).lower() not in ignore for m in view(*names).finditer(text.replace("\u2019", "'")))


def is_negation_word(w: str) -> bool:
    return bool(view("negation_word", "negation_extra").fullmatch(w))


def lateral_words(text: str) -> set:
    return {m.group(0).lower() for m in aq("side").finditer(text)}


@functools.lru_cache(maxsize=1)
def _aq() -> dict:
    """The added-qualifier families from app/llm/lexicon.yaml code_lists.added_qualifier (T-105): the one source of the attribution, hedge,
    approximation and inability word lists, for this module and for spanish_text."""
    from app.backend import lexicon
    return {e["id"]: e["regex"] for e in lexicon.code_list("added_qualifier")}


def aq(name: str):
    return _aq()[name]


@functools.lru_cache(maxsize=None)
def view(*names: str):
    """One compiled regex over several lexicon families (alternation); a view of the lexicon, never a word list of its own."""
    return re.compile("|".join(f"(?:{aq(n).pattern})" for n in names), re.IGNORECASE)


def _clean(m) -> str:
    return re.sub(r"\s+", " ", m.group(0)).strip(" .;:\n").lower()


def added_qualifier_tokens(summary: str, excerpt: str, *, quote_has: dict = None) -> list:
    """Qualifier words the summary carries but the quote has no qualifier of that kind for (D-047, the reverse of dropped_qualifiers):
    an attribution (who said it), a hedge (how sure) or an approximation (how exact). The word lists are the lexicon's added_qualifier family (T-105). `quote_has` lets the Spanish
    path say that its own cue lists found a kind in the quote ({'attribution'|'hedge'|'approximation': bool}). Returns the summary's own words, lower
    case, in order; [] when the quote carries the kind. 'cannot' and 'unable to' are one statement; 'about' before a verb-object ('counseled about 3
    exercises') is a preposition, not an approximation."""
    qh = quote_has or {}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:04.209Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R1=$S/T128_9_r2/repo; R2=$S/T128_9_r2b/repo\ncat > $E/neg_diff_t128_r2.py <<'EOF'\nimport sys, subprocess, json\nPY=\"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n# each pair: summary, quote\nP = [\n (\"Neck pain; denies fever.\", \"Neck pain.\"),\n (\"Neck pain; denied fever.\", \"Neck pain.\"),\n (\"Neck pain; deny any numbness.\", \"Neck pain.\"),\n (\"Neck pain; denying numbness.\", \"Neck pain.\"),\n (\"Neck pain; denies numbness.\", \"Neck pain. Denies numbness.\"),\n (\"Neck pain; denies numbness.\", \"Neck pain. Patient will deny numbness.\"),\n (\"Neck pain; absence of numbness.\", \"Neck pain.\"),\n (\"Neck pain; lacks radiation.\", \"Neck pain.\"),\n (\"Neck pain; free of numbness.\", \"Neck pain.\"),\n (\"Neck pain; nothing abnormal found.\", \"Neck pain.\"),\n (\"Neck pain; no numbness.\", \"Neck pain.\"),\n (\"Neck pain; without numbness.\", \"Neck pain.\"),\n (\"Neck pain; never numbness.\", \"Neck pain.\"),\n (\"Neck pain; neither numbness.\", \"Neck pain.\"),\n (\"Neck pain; absent reflexes.\", \"Neck pain.\"),\n (\"Neck pain; negative for fracture.\", \"Neck pain.\"),\n (\"Neck pain; did not miss work.\", \"Neck pain.\"),\n (\"Neck pain; couldn't sleep.\", \"Neck pain.\"),\n (\"Neck pain; w/o radiation.\", \"Neck pain.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Denies radiation.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Deny radiation.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Absence of radiation.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Lacks radiation.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Free of radiation.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Nothing radiating.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Radiation absent.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Neuro exam negative.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Radiation to the arm.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Radiation ruled out.\"),\n (\"Neck pain; no radiation.\", \"Neck pain. Exam unremarkable.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Denies fracture.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Deny fracture history.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. No acute fracture.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Fracture not seen.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Fracture can't be excluded.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. W/O fracture.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Nor fracture.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Never fractured.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Neither fracture nor dislocation.\"),\n (\"Neck pain; no fracture.\", \"Neck pain. Without fracture.\"),\n]\nif len(sys.argv) > 2:\n    sys.path.insert(0, sys.argv[1])\n    from app.backend import summary_trim as T\n    out = []\n    for s, q in P:\n        r = T.trim(s, q); out.append([r[\"changed\"], r[\"text\"]])\n    print(json.dumps(out)); sys.exit()\nres = {}\nfor lab, root in ((\"old\", sys.argv[1]), (\"new\", sys.argv[2])):\n    r = subprocess.run([PY, \"-I\", __file__, root, \"x\"], capture_output=True, text=True, cwd=root)\n    res[lab] = json.loads(r.stdout.strip().splitlines()[-1])\nfor (s, q), a, b in zip(P, res[\"old\"], res[\"new\"]):\n    print((\"DIFF \" if a != b else \"same \"), repr(s), \"|\", repr(q), \"| old:\", a, \"| new:\", b)\nEOF\n.venv/bin/python -I $E/neg_diff_t128_r2.py $R1 $R2 2>&1 | grep -v setpgid"
}
````

### User / tool · 2026-11-02T12:05:04.436Z

**tool result**
````
[[true, "Neck pain."], [true, "Neck pain."], [false, "Neck pain; deny any numbness."], [false, "Neck pain; denying numbness."], [false, "Neck pain; denies numbness."], [false, "Neck pain; denies numbness."], [false, "Neck pain; absence of numbness."], [false, "Neck pain; lacks radiation."], [false, "Neck pain; free of numbness."], [false, "Neck pain; nothing abnormal found."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [true, "Neck pain."], [false, "Neck pain; w/o radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no radiation."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."], [false, "Neck pain; no fracture."]]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:10.470Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R1=$S/T128_9_r2/repo; R2=$S/T128_9_r2b/repo\nsed -i 's/if len(sys.argv) > 2:/if len(sys.argv) > 3:/; s/\"-I\", __file__, root, \"x\"/\"-I\", __file__, root, \"x\", \"y\"/' $E/neg_diff_t128_r2.py\n.venv/bin/python -I $E/neg_diff_t128_r2.py $R1 $R2 2>&1 | grep -v setpgid | sed 's/ | old:/\\n     old:/; s/ | new:/ new:/'"
}
````

### User / tool · 2026-11-02T12:05:10.526Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  2:/if len(sys.argv) > 3:/; s/"-I", __file__, root, "x"/"-I", __file__, root, "x", "y"/)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:14.135Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2/neg_diff_t128_r2.py",
 "old_string": "if len(sys.argv) > 2:",
 "new_string": "if len(sys.argv) >= 4:"
}
````

### User / tool · 2026-11-02T12:05:14.234Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2/neg_diff_t128_r2.py has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:14.580Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2/neg_diff_t128_r2.py",
 "old_string": "\"-I\", __file__, root, \"x\"]",
 "new_string": "\"-I\", __file__, root, \"x\", \"y\"]"
}
````

### User / tool · 2026-11-02T12:05:14.674Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2/neg_diff_t128_r2.py has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:18.322Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R1=$S/T128_9_r2/repo; R2=$S/T128_9_r2b/repo\n.venv/bin/python -I $E/neg_diff_t128_r2.py $R1 $R2 2>&1 | grep -v setpgid"
}
````

### User / tool · 2026-11-02T12:05:18.677Z

**tool result**
````
same  'Neck pain; denies fever.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; denied fever.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; deny any numbness.' | 'Neck pain.' | old: [False, 'Neck pain; deny any numbness.'] | new: [False, 'Neck pain; deny any numbness.']
same  'Neck pain; denying numbness.' | 'Neck pain.' | old: [False, 'Neck pain; denying numbness.'] | new: [False, 'Neck pain; denying numbness.']
same  'Neck pain; denies numbness.' | 'Neck pain. Denies numbness.' | old: [False, 'Neck pain; denies numbness.'] | new: [False, 'Neck pain; denies numbness.']
same  'Neck pain; denies numbness.' | 'Neck pain. Patient will deny numbness.' | old: [False, 'Neck pain; denies numbness.'] | new: [False, 'Neck pain; denies numbness.']
DIFF  'Neck pain; absence of numbness.' | 'Neck pain.' | old: [False, 'Neck pain; absence of numbness.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; lacks radiation.' | 'Neck pain.' | old: [False, 'Neck pain; lacks radiation.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; free of numbness.' | 'Neck pain.' | old: [False, 'Neck pain; free of numbness.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; nothing abnormal found.' | 'Neck pain.' | old: [False, 'Neck pain; nothing abnormal found.'] | new: [True, 'Neck pain.']
same  'Neck pain; no numbness.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; without numbness.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; never numbness.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; neither numbness.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; absent reflexes.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; negative for fracture.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; did not miss work.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  "Neck pain; couldn't sleep." | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; w/o radiation.' | 'Neck pain.' | old: [False, 'Neck pain; w/o radiation.'] | new: [False, 'Neck pain; w/o radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Denies radiation.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Deny radiation.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Absence of radiation.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Lacks radiation.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Free of radiation.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Nothing radiating.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Radiation absent.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Neuro exam negative.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Radiation to the arm.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Radiation ruled out.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no radiation.' | 'Neck pain. Exam unremarkable.' | old: [False, 'Neck pain; no radiation.'] | new: [False, 'Neck pain; no radiation.']
same  'Neck pain; no fracture.' | 'Neck pain. Denies fracture.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Deny fracture history.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. No acute fracture.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Fracture not seen.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | "Neck pain. Fracture can't be excluded." | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. W/O fracture.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Nor fracture.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Never fractured.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Neither fracture nor dislocation.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
same  'Neck pain; no fracture.' | 'Neck pain. Without fracture.' | old: [False, 'Neck pain; no fracture.'] | new: [False, 'Neck pain; no fracture.']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:42.105Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; python3 - <<'EOF'\nimport re,pathlib\np=pathlib.Path(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2\")\nsrc=(p/\"neg_diff_t128_r2.py\").read_text()\nnew='''P = [\n (\"Neck pain; no nausea.\", \"Neck pain. Deny N/V.\"),\n (\"Neck pain; no fever.\", \"Neck pain. Denying chills.\"),\n (\"Neck pain; denies dizziness.\", \"Neck pain. Deny vertigo.\"),\n (\"Neck pain; no loss of consciousness.\", \"Neck pain. Denial of LOC.\"),\n (\"Neck pain; no vomiting.\", \"Neck pain. Pt denies nausea.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Nothing else reported.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Lacks sensation changes.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Absence of tingling.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Free of tingling.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Denies tingling.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Deny tingling.\"),\n (\"Neck pain; no numbness.\", \"Neck pain. Radiation to arm.\"),\n (\"Neck pain; absence of fever.\", \"Neck pain. Denies chills.\"),\n (\"Neck pain; lacks balance.\", \"Neck pain. Denies chills.\"),\n (\"Neck pain; nothing broken.\", \"Neck pain.\"),\n (\"Neck pain; nothing broken.\", \"Neck pain. No fracture.\"),\n (\"Neck pain; free of fracture.\", \"Neck pain. No fracture.\"),\n]\n'''\ni=src.index(\"P = [\"); j=src.index(\"]\\nif len(sys.argv)\")+2\n(p/\"neg_diff2_t128_r2.py\").write_text(src[:i]+new+src[j:])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I $E/neg_diff2_t128_r2.py $S/T128_9_r2/repo $S/T128_9_r2b/repo 2>&1 | grep -v setpgid; grep -n \"negation_word\\|negation_extra\\|negation_contraction\" -A4 app/llm/lexicon.yaml | grep -i \"regex\" | head"
}
````

### User / tool · 2026-11-02T12:05:42.497Z

**tool result**
````
same  'Neck pain; no nausea.' | 'Neck pain. Deny N/V.' | old: [False, 'Neck pain; no nausea.'] | new: [False, 'Neck pain; no nausea.']
same  'Neck pain; no fever.' | 'Neck pain. Denying chills.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; denies dizziness.' | 'Neck pain. Deny vertigo.' | old: [False, 'Neck pain; denies dizziness.'] | new: [False, 'Neck pain; denies dizziness.']
same  'Neck pain; no loss of consciousness.' | 'Neck pain. Denial of LOC.' | old: [False, 'Neck pain; no loss of consciousness.'] | new: [False, 'Neck pain; no loss of consciousness.']
same  'Neck pain; no vomiting.' | 'Neck pain. Pt denies nausea.' | old: [False, 'Neck pain; no vomiting.'] | new: [False, 'Neck pain; no vomiting.']
DIFF  'Neck pain; no numbness.' | 'Neck pain. Nothing else reported.' | old: [True, 'Neck pain.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Lacks sensation changes.' | old: [False, 'Neck pain; no numbness.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Absence of tingling.' | old: [False, 'Neck pain; no numbness.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Free of tingling.' | old: [False, 'Neck pain; no numbness.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Denies tingling.' | old: [False, 'Neck pain; no numbness.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Deny tingling.' | old: [False, 'Neck pain; no numbness.'] | new: [False, 'Neck pain; no numbness.']
same  'Neck pain; no numbness.' | 'Neck pain. Radiation to arm.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; absence of fever.' | 'Neck pain. Denies chills.' | old: [False, 'Neck pain; absence of fever.'] | new: [False, 'Neck pain; absence of fever.']
same  'Neck pain; lacks balance.' | 'Neck pain. Denies chills.' | old: [False, 'Neck pain; lacks balance.'] | new: [False, 'Neck pain; lacks balance.']
same  'Neck pain; nothing broken.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; nothing broken.' | 'Neck pain. No fracture.' | old: [False, 'Neck pain; nothing broken.'] | new: [False, 'Neck pain; nothing broken.']
same  'Neck pain; free of fracture.' | 'Neck pain. No fracture.' | old: [False, 'Neck pain; free of fracture.'] | new: [False, 'Neck pain; free of fracture.']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:05:51.087Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/T128_9_r2b/repo && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF' 2>&1 | grep -v setpgid\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import grounding as G, summary_trim as T\nfor t in [\"Deny N/V.\",\"Deny tingling.\",\"Denies tingling.\",\"Denying chills.\",\"Denial of LOC.\",\"Pt deny chest pain\"]:\n    print(repr(t), G.has_negation(t, extra=True), bool(T._QUOTE_NEG.search(t)), G.negation_words(t), T._quote_profile(t,\"\",\"\")[\"neg\"])\nprint(G.is_negation_word(\"deny\"), G.is_negation_word(\"denies\"))\nprint(T.new_salient(\"no nausea\", T._quote_profile(\"Neck pain. Deny N/V.\",\"\",\"\")))\nprint(T.new_salient(\"no numbness\", T._quote_profile(\"Neck pain. Deny tingling.\",\"\",\"\")))\nEOF\ngrep -n \"negation_word\" -B1 -A6 app/llm/lexicon.yaml | head -40"
}
````

### User / tool · 2026-11-02T12:05:51.282Z

**tool result**
````
'Deny N/V.' False False [] False
'Deny tingling.' False False [] False
'Denies tingling.' True False ['denies'] True
'Denying chills.' False False [] False
'Denial of LOC.' False False [] False
'Pt deny chest pain' False False [] False
False True
[]
[]
1410-          miss: ['Pain 4/10.']
1411:      - id: negation_word
1412-        pattern: '\b(?:no|not|none|never|without|denies|denied|negative|neither|nor|absent)\b'
1413-        examples:
1414-          hit: ['No numbness.', 'Pain not worse.', 'Denied weakness.', 'Negative for fracture.']
1415-          miss: ['Pain 4/10.', 'Nothing else.']
1416-      - id: negation_interchangeable
1417-        pattern: '\b(?:no|not|none|never)\b'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:06:04.338Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2\")\nsrc=(p/\"neg_diff2_t128_r2.py\").read_text()\nnew='''P = [\n (\"Neck pain; no shortness of breath.\", \"Neck pain. Deny SOB.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Deny dyspnea.\"),\n (\"Neck pain; no loss of consciousness.\", \"Neck pain. Deny syncope.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Deny tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Denies tingling.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denies dyspnea.\"),\n (\"Neck pain; no shortness of breath.\", \"Neck pain. Denies SOB.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denying dyspnea.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denial of dyspnea.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Nothing about dyspnea.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Nothing else.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Absence of tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Lacks tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Free of tingling.\"),\n (\"Neck pain; absence of weakness.\", \"Neck pain.\"),\n (\"Neck pain; lacks coordination.\", \"Neck pain.\"),\n (\"Neck pain; free of weakness.\", \"Neck pain.\"),\n (\"Neck pain; nothing abnormal on x-ray.\", \"Neck pain.\"),\n]\n'''\ni=src.index(\"P = [\"); j=src.index(\"]\\\\nif len(sys.argv)\")+2\n(p/\"neg_diff3_t128_r2.py\").write_text(src[:i]+new+src[j:])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I $E/neg_diff3_t128_r2.py $S/T128_9_r2/repo $S/T128_9_r2b/repo 2>&1 | grep -v setpgid"
}
````

### User / tool · 2026-11-02T12:06:04.478Z

**tool result**
````
Traceback (most recent call last):
  File "<stdin>", line 25, in <module>
ValueError: substring not found
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python: can't open file '/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2/neg_diff3_t128_r2.py': [Errno 2] No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:06:12.794Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2\")\nsrc=(p/\"neg_diff2_t128_r2.py\").read_text()\nnew='''P = [\n (\"Neck pain; no shortness of breath.\", \"Neck pain. Deny SOB.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Deny dyspnea.\"),\n (\"Neck pain; no loss of consciousness.\", \"Neck pain. Deny syncope.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Deny tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Denies tingling.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denies dyspnea.\"),\n (\"Neck pain; no shortness of breath.\", \"Neck pain. Denies SOB.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denying dyspnea.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Denial of dyspnea.\"),\n (\"Neck pain; no trouble breathing.\", \"Neck pain. Nothing about dyspnea.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Nothing else.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Absence of tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Lacks tingling.\"),\n (\"Neck pain; no weakness.\", \"Neck pain. Free of tingling.\"),\n (\"Neck pain; absence of weakness.\", \"Neck pain.\"),\n (\"Neck pain; lacks coordination.\", \"Neck pain.\"),\n (\"Neck pain; free of weakness.\", \"Neck pain.\"),\n (\"Neck pain; nothing abnormal on x-ray.\", \"Neck pain.\"),\n]\n'''\ni=src.index(\"P = [\"); j=src.index(\"]\\nif len(sys.argv)\")+2\n(p/\"neg_diff3_t128_r2.py\").write_text(src[:i]+new+src[j:])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I $E/neg_diff3_t128_r2.py $S/T128_9_r2/repo $S/T128_9_r2b/repo 2>&1 | grep -v setpgid"
}
````

### User / tool · 2026-11-02T12:06:13.191Z

**tool result**
````
same  'Neck pain; no shortness of breath.' | 'Neck pain. Deny SOB.' | old: [False, 'Neck pain; no shortness of breath.'] | new: [False, 'Neck pain; no shortness of breath.']
DIFF  'Neck pain; no trouble breathing.' | 'Neck pain. Deny dyspnea.' | old: [False, 'Neck pain; no trouble breathing.'] | new: [True, 'Neck pain.']
same  'Neck pain; no loss of consciousness.' | 'Neck pain. Deny syncope.' | old: [False, 'Neck pain; no loss of consciousness.'] | new: [False, 'Neck pain; no loss of consciousness.']
DIFF  'Neck pain; no weakness.' | 'Neck pain. Deny tingling.' | old: [False, 'Neck pain; no weakness.'] | new: [True, 'Neck pain.']
same  'Neck pain; no weakness.' | 'Neck pain. Denies tingling.' | old: [False, 'Neck pain; no weakness.'] | new: [False, 'Neck pain; no weakness.']
same  'Neck pain; no trouble breathing.' | 'Neck pain. Denies dyspnea.' | old: [False, 'Neck pain; no trouble breathing.'] | new: [False, 'Neck pain; no trouble breathing.']
same  'Neck pain; no shortness of breath.' | 'Neck pain. Denies SOB.' | old: [False, 'Neck pain; no shortness of breath.'] | new: [False, 'Neck pain; no shortness of breath.']
same  'Neck pain; no trouble breathing.' | 'Neck pain. Denying dyspnea.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
same  'Neck pain; no trouble breathing.' | 'Neck pain. Denial of dyspnea.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; no trouble breathing.' | 'Neck pain. Nothing about dyspnea.' | old: [True, 'Neck pain.'] | new: [False, 'Neck pain; no trouble breathing.']
DIFF  'Neck pain; no weakness.' | 'Neck pain. Nothing else.' | old: [True, 'Neck pain.'] | new: [False, 'Neck pain; no weakness.']
DIFF  'Neck pain; no weakness.' | 'Neck pain. Absence of tingling.' | old: [True, 'Neck pain.'] | new: [False, 'Neck pain; no weakness.']
same  'Neck pain; no weakness.' | 'Neck pain. Lacks tingling.' | old: [False, 'Neck pain; no weakness.'] | new: [False, 'Neck pain; no weakness.']
same  'Neck pain; no weakness.' | 'Neck pain. Free of tingling.' | old: [False, 'Neck pain; no weakness.'] | new: [False, 'Neck pain; no weakness.']
DIFF  'Neck pain; absence of weakness.' | 'Neck pain.' | old: [False, 'Neck pain; absence of weakness.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; lacks coordination.' | 'Neck pain.' | old: [False, 'Neck pain; lacks coordination.'] | new: [True, 'Neck pain.']
DIFF  'Neck pain; free of weakness.' | 'Neck pain.' | old: [False, 'Neck pain; free of weakness.'] | new: [True, 'Neck pain.']
same  'Neck pain; nothing abnormal on x-ray.' | 'Neck pain.' | old: [True, 'Neck pain.'] | new: [True, 'Neck pain.']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:06:24.911Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R2=$S/T128_9_r2b/repo\npython3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-128-129-r2\")\ns=(p/\"mut_t128_r2.py\").read_text()\ni=s.index(\"M = [\"); j=s.index(\"surv = []\")\nnew='''M = [\n (\"quote negation: extra=False\", \"grounding.has_negation(ex, extra=True)\", \"grounding.has_negation(ex, extra=False)\"),\n (\"quote negation: always False\", \"grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex)\", \"_QUOTE_NEG.search(ex)\"),\n (\"clause negation: only 'no'\", \"grounding.is_negation_word(w)\", \"(w == 'no')\"),\n (\"clause negation: never\", \"grounding.is_negation_word(w)\", \"False\"),\n (\"clause side words: never\", \"if grounding.aq(\\\\\"side\\\\\").fullmatch(w):\\\\n            ok\", \"if False:\\\\n            ok\"),\n (\"quote sides ignored\", \"if grounding.aq(\\\\\"side\\\\\").fullmatch(w)}\", \"if False}\"),\n (\"contraction branch off\", \"w.endswith(\\\\\"n't\\\\\") or grounding.is_negation_word(w)\", \"grounding.is_negation_word(w)\"),\n (\"prefix<2 -> <1\", \"content_words(\\\\\" \\\\\".join(c[0] for c in clauses[:first_cut]))) < 2\", \"content_words(\\\\\" \\\\\".join(c[0] for c in clauses[:first_cut]))) < 1\"),\n]\n'''\n(p/\"mut2_t128_r2.py\").write_text(s[:i]+new+s[j:])\nEOF\n.venv/bin/python -I $E/mut2_t128_r2.py $R2 2>&1 | grep -v setpgid; cd $R2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_summary_trim.py -q -p no:cacheprovider 2>&1 | tail -2",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T12:06:35.892Z

**tool result**
````
KILLED   quote negation: extra=False | 1 failed, 285 passed in 1.61s
KILLED   quote negation: always False | 1 failed, 89 passed in 0.34s
KILLED   clause negation: only 'no' | 1 failed, 253 passed in 0.89s
KILLED   clause negation: never | 1 failed, 253 passed in 0.93s
KILLED   clause side words: never | 1 failed, 285 passed in 1.39s
SURVIVED quote sides ignored | 286 passed in 0.87s
SURVIVED contraction branch off | 286 passed in 0.84s
KILLED   prefix<2 -> <1 | 1 failed, 211 passed in 0.43s
survivors: ['quote sides ignored', 'contraction branch off']
......................................................................   [100%]
286 passed in 1.06s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:06:43.912Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/T128_9_r2b/repo && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF' 2>&1 | grep -v setpgid\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import grounding as G, summary_trim as T\nprint(G.side_neg_words(\"Pt can't sleep, didn't eat, bilateral wrist, left knee\", keep_order=True))\nprint(T._quote_profile(\"Bilateral wrist pain.\",\"\",\"\")[\"sides\"], T._quote_profile(\"Left knee pain, bilaterally.\",\"\",\"\")[\"sides\"])\nprint(T.trim(\"Neck pain; bilateral wrist pain.\",\"Neck pain. Wrist pain, both sides.\"))\nprint(T.trim(\"Neck pain; bilateral wrist swelling.\",\"Neck pain. Wrist swelling bilaterally.\"))\nEOF"
}
````

### User / tool · 2026-11-02T12:06:44.104Z

**tool result**
````
["can't", "didn't", 'bilateral', 'left']
{'bilateral'} {'left', 'bilaterally'}
{'text': 'Neck pain; bilateral wrist pain.', 'removed': [], 'kept': ['Neck pain', 'bilateral wrist pain'], 'supported': True, 'notes': [], 'changed': False}
{'text': 'Neck pain; bilateral wrist swelling.', 'removed': [], 'kept': ['Neck pain', 'bilateral wrist swelling'], 'supported': True, 'notes': [], 'changed': False}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:06:53.823Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/m3 && mkdir -p $S/m3 && cp -r $S/T128_9_r2b/repo $S/m3/repo && cd $S/m3/repo && python3 - <<'EOF'\nimport pathlib\nf=pathlib.Path(\"app/backend/summary_trim.py\"); s=f.read_text()\na='w.endswith(\"n\\'t\") or grounding.is_negation_word(w)'\nassert a in s\nf.write_text(s.replace(a,'grounding.is_negation_word(w)',1))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF' 2>&1 | grep -v setpgid\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import summary_trim as T\nfor s in [\"Neck pain; couldn't sleep.\",\"Neck pain; didn't miss work.\",\"Neck pain; can't lift.\"]:\n    print(s, T.trim(s,\"Neck pain.\")[\"changed\"])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_summary_trim.py -q -p no:cacheprovider 2>&1 | tail -1"
}
````

### User / tool · 2026-11-02T12:06:56.637Z

**tool result**
````
Neck pain; couldn't sleep. False
Neck pain; didn't miss work. False
Neck pain; can't lift. False
286 passed in 1.03s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:07:01.227Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/T128_9_r2b/repo && (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > $S/unit_r2b.txt 2>&1 &) ; echo started"
}
````

### User / tool · 2026-11-02T12:07:01.324Z

**tool result**
````
started
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:07:12.494Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2b/repo; grep -n \"manual\" $R/app/backend/review.py | head -12; grep -n \"def apply_review\" -A30 $R/app/db/db.py | grep -n \"reset\\|manual\" | head"
}
````

### User / tool · 2026-11-02T12:07:12.594Z

**tool result**
````
203:    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
237:    """Code checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
270:                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
476:# ---------------------------------------------------------------- manual entry (D-031, T-056)
477:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
517:    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
9:223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:07:19.082Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T128_9_r2b/repo; sed -n 476,530p $R/app/backend/review.py; grep -n \"manual_entry\\|\\\"reset\\\"\" $R/app/db/db.py | head"
}
````

### User / tool · 2026-11-02T12:07:19.176Z

**tool result**
````
# ---------------------------------------------------------------- manual entry (D-031, T-056)
def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
    t = _now(now)
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    rec = next((r for r in recs if r["id"] == record_id), None)
    if rec is None:
        raise ReviewError(404, "not_found", message="No such record.")
    if rec.get("duplicate_of"):
        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
    if live:
        raise _bad("This record already has an entry; edit that entry instead.")
    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
        raise _bad("Provide a summary and the quoted sentences.")
    summary, excerpt = summary.strip(), excerpt.strip()
    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
    if problems:
        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], excerpt)
    eid = f"e{rec['seq']}_m"
    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
                         ocr_derived=record_id in ocr_record_ids(conn, case_id))
    base = generator.body_offset(rec)
    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
                              "date_provider_from_header": True},
              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
    DB.add_item(conn, case_id, "entry", {
        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}


# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
    `not_duplicate` event on the original entry."""
    from app.backend import pipeline as PL
    from app.llm import provider as P
19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
21:           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
33:SCHEMA_VERSION = 4          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062); 4 = += reclassify, rejudge (T-095; v3 -> v4 is an in-place migration)
223:    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
253:    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:07:39.901Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; cat > $E/t129_r2.py <<'EOF'\nimport sys, os, tempfile, json\nroot = sys.argv[1]\nsys.path.insert(0, root); os.chdir(root)\nos.environ.update(LLM_BACKEND=\"claude-cli\", ENABLE_LIVE=\"1\", ZLAYT_MODE=\"local\")   # POST /api/cases is code-only; /run is never called\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.backend import pipeline as PL, present\nfrom app.db import db as DB\nd = tempfile.mkdtemp(); path = d + \"/t.sqlite\"\nc = TestClient(create_app(path, static_dir=d), client=(\"127.0.0.1\", 50000))\ndef rec(date, src, ex): return f'Date: {date}\\nSource: {src}\\nExcerpt: \"{ex}\"'\nR1 = rec(\"2026-01-09\", \"Lakeside Clinic, intake\", \"Intake done. ER charges: $6,240.\")\nR2 = rec(\"2026-03-20\", \"Lakeside Clinic, follow-up\", \"Neck pain improving. Charge per visit $185.\")\nCOVER = \"FAX COVER SHEET\\nTo: Dr X\\nPages: 3\"\nprint(\"== A. real routes: POST then GET, record flags\")\nfor name, text in ((\"preamble\", COVER + \"\\n---\\n\" + R1 + \"\\n---\\n\" + R2), (\"plain\", R1 + \"\\n---\\n\" + R2), (\"midnote\", R1 + \"\\n---\\nfree note\\n---\\n\" + R2)):\n    r = c.post(\"/api/cases\", json={\"text\": text}); assert r.status_code == 201, r.text\n    tok = r.json()[\"token\"]\n    post = [(x[\"id\"], x[\"unsplit\"], x[\"preamble\"]) for x in r.json()[\"records\"]]\n    g = c.get(f\"/api/cases/{tok}\")\n    get = [(x[\"id\"], x[\"unsplit\"], x[\"preamble\"]) for x in g.json()[\"records\"]]\n    print(name, \"POST\", post, \"GET\", get, \"same:\", post == get, \"GET warnings:\", g.json().get(\"warnings\"), \"POST warnings:\", [w if isinstance(w, str) else w.get(\"code\") for w in r.json()[\"warnings\"]])\nprint(\"== B. upgrade: store under old numbering (dated cover r1), accept gap + accept amount + dismiss amount, re-ingest with real preamble\")\nconn = DB.connect(path)\nold = 'Date: 2025-12-01\\nSource: Cover\\nExcerpt: \"Fax cover sheet.\"\\n---\\n' + R1 + \"\\n---\\n\" + R2\ncid = DB.create_case(conn, old, now=1.0, name=\"up\", source=\"paste\", backend=\"fixture\", demo_mode=0)\nPL.ingest_case(conn, cid, old, 1.0)\nfor kind in (\"flag\", \"amount\"):\n    for it in DB.list_items(conn, cid, kind):\n        print(\" old\", kind, it[\"id\"], it[\"review_status\"], it.get(\"record_ids\") or (it.get(\"computed\") or {}).get(\"record_ids\"), it.get(\"text\"))\ngap = next(f for f in DB.list_items(conn, cid, \"flag\") if f[\"type\"] == \"gap\")\nDB.apply_review(conn, gap[\"id\"], \"accept\", now=2.0, case=cid)\nam = DB.list_items(conn, cid, \"amount\")\nDB.apply_review(conn, am[0][\"id\"], \"accept\", now=2.0, case=cid)\nif len(am) > 1: DB.apply_review(conn, am[1][\"id\"], \"dismiss\", now=2.0, case=cid)\nnew = COVER + \"\\n---\\n\" + R1 + \"\\n---\\n\" + R2\nPL.ingest_case(conn, cid, new, 3.0)\nrecs = {r[\"id\"]: r[\"date_iso\"] for r in present._recs_by_id(conn, cid).values()}\nprint(\" new records\", recs)\nfor kind in (\"flag\", \"amount\"):\n    for it in DB.list_items(conn, cid, kind):\n        ids = it.get(\"record_ids\") or (it.get(\"computed\") or {}).get(\"record_ids\")\n        print(\" new\", kind, it[\"id\"], it[\"review_status\"], ids, it.get(\"text\"))\nbad = [(k, it[\"id\"]) for k in (\"flag\", \"amount\") for it in DB.list_items(conn, cid, k) if it[\"review_status\"] != \"pending\"]\nprint(\" decided items left after shift:\", bad)\nprint(\" events:\", [(e[\"item_id\"] if \"item_id\" in e else e.get(\"item\"), e[\"action\"]) for e in DB.list_events(conn, cid)] if hasattr(DB, \"list_events\") else None)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I $E/t129_r2.py $S/T128_9_r2b/repo 2>&1 | grep -v setpgid | cut -c1-330",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T12:07:40.658Z

**tool result**
````
== A. real routes: POST then GET, record flags
preamble POST [('r1', False, False), ('r2', False, False), ('r3', True, True)] GET [('r1', False, False), ('r2', False, False), ('r3', True, True)] same: True GET warnings: [] POST warnings: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
plain POST [('r1', False, False), ('r2', False, False)] GET [('r1', False, False), ('r2', False, False)] same: True GET warnings: [] POST warnings: []
midnote POST [('r1', False, False), ('r2', False, False), ('r3', True, False)] GET [('r1', False, False), ('r2', False, False), ('r3', True, False)] same: True GET warnings: [] POST warnings: ['SPLIT_AMBIGUOUS', 'SPLIT_REJECTED', 'UNSPLIT_TEXT', 'DATE_EXCLUDED_FROM_GAPS']
== B. upgrade: store under old numbering (dated cover r1), accept gap + accept amount + dismiss amount, re-ingest with real preamble
 old flag f_gap_r1_r2 pending ['r1', 'r2'] None
 old flag f_gap_r2_r3 pending ['r2', 'r3'] None
 old amount a1 pending ['r2'] $6,240
 old amount a2 pending ['r3'] $185
 new records {'r1': '2026-01-09', 'r2': '2026-03-20', 'r3': None}
 new flag f_gap_r1_r2 pending ['r1', 'r2'] None
 new flag f_date_r3 pending ['r3'] None
 new amount a1 pending ['r1'] $6,240
 new amount a2 pending ['r2'] $185
 decided items left after shift: []
 events: [('f_gap_r1_r2', 'accept'), ('a1', 'accept'), ('a2', 'dismiss'), ('a1', 'reset'), ('a2', 'reset'), ('f_gap_r1_r2', 'reset')]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:07:57.746Z

**tool call — Bash**
````
{
 "command": "E=$PWD/artifacts/review-evidence/T-128-129-r2; cat > $E/mut_t129_r2.py <<'EOF'\nimport sys, subprocess, pathlib\nroot = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nfiles = {\"pl\": root/\"app/backend/pipeline.py\", \"pr\": root/\"app/backend/present.py\"}\norig = {k: v.read_text() for k, v in files.items()}\nM = [\n (\"pl\", \"marks never stored\", '    marks = {\"unsplit_records\"', '    return\\n    marks = {\"unsplit_records\"'),\n (\"pr\", \"record_view unsplit always False\", '\"unsplit\": bool(r.get(\"unsplit\"))', '\"unsplit\": False'),\n (\"pr\", \"record_view preamble always False\", '\"preamble\": bool(r.get(\"preamble\"))', '\"preamble\": False'),\n (\"pr\", \"_recs_by_id preamble never set\", 'r[\"id\"] in pre', 'False'),\n (\"pl\", \"reset no-op\", \"    if not moved:\\n        return\\n    for kind\", \"    return\\n    for kind\"),\n (\"pl\", \"moved: only vanished ids\", \"new_spans.get(i) != (a, b)\", \"i not in new_spans\"),\n (\"pl\", \"reset flags only\", 'for kind in (\"entry\", \"amount\", \"flag\"):', 'for kind in (\"flag\",):'),\n (\"pl\", \"reset amounts skipped\", 'for kind in (\"entry\", \"amount\", \"flag\"):', 'for kind in (\"entry\", \"flag\"):'),\n (\"pl\", \"reset accepted only\", 'it[\"review_status\"] != \"pending\" and moved', 'it[\"review_status\"] == \"accepted\" and moved'),\n (\"pl\", \"no computed.record_ids fallback\", \"or (item.get(\\\"computed\\\") or {}).get(\\\"record_ids\\\")\", \"\"),\n (\"pl\", \"no evidence fallback\", \" or [e.get(\\\"record_id\\\") for e in item.get(\\\"evidence\\\") or []]\", \"\"),\n (\"pl\", \"run_pipeline passes now=0.0\", \"_store_records(conn, cid, ing, clock())\", \"_store_records(conn, cid, ing)\"),\n (\"pl\", \"ingest_case passes no now\", \"_store_records(conn, cid, ing, now)\", \"_store_records(conn, cid, ing)\"),\n (\"pl\", \"marks early-return inverted\", \"if all(cfg.get(k, []) == v for k, v in marks.items()):\\n        return\", \"if not all(cfg.get(k, []) == v for k, v in marks.items()):\\n        return\"),\n]\nsurv = []\nfor k, name, a, b in M:\n    if orig[k].count(a) < 1: print(\"NOT FOUND\", name); continue\n    files[k].write_text(orig[k].replace(a, b, 1))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", \"tests/unit/test_ingest.py\", \"tests/unit/test_api_routes.py\", \"tests/unit/test_pipeline.py\", \"-q\", \"-x\", \"-p\", \"no:cacheprovider\", \"--no-header\"], cwd=root, capture_output=True, text=True)\n    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-120:]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), name, \"|\", tail)\n    if not r.returncode: surv.append(name)\n    files[k].write_text(orig[k])\nprint(\"survivors:\", surv)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S/m3 >/dev/null; rm -rf $S/m4 && mkdir -p $S/m4 && cp -r $S/T128_9_r2b/repo $S/m4/repo; ls $S/m4/repo/tests/unit | grep -c \"test_pipeline.py\"; .venv/bin/python -I $E/mut_t129_r2.py $S/m4/repo 2>&1 | grep -v setpgid",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T12:08:44.353Z

**tool result**
````
1
KILLED   marks never stored | 1 failed, 56 passed in 0.65s
KILLED   record_view unsplit always False | 1 failed, 56 passed in 0.60s
KILLED   record_view preamble always False | 1 failed, 56 passed in 0.42s
KILLED   _recs_by_id preamble never set | 1 failed, 56 passed in 0.42s
KILLED   reset no-op | 1 failed, 57 passed in 0.45s
KILLED   moved: only vanished ids | 1 failed, 57 passed in 0.45s
SURVIVED reset flags only | 123 passed in 7.61s
SURVIVED reset amounts skipped | 123 passed in 7.04s
SURVIVED reset accepted only | 123 passed in 7.44s
KILLED   no computed.record_ids fallback | 1 failed, 57 passed in 0.46s
SURVIVED no evidence fallback | 123 passed in 7.22s
SURVIVED run_pipeline passes now=0.0 | 123 passed in 7.89s
KILLED   ingest_case passes no now | 1 failed, 57 passed in 0.52s
KILLED   marks early-return inverted | 1 failed, 56 passed in 0.44s
survivors: ['reset flags only', 'reset amounts skipped', 'reset accepted only', 'no evidence fallback', 'run_pipeline passes now=0.0']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:08:57.474Z

**tool call — Bash**
````
{
 "command": "sleep 100; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -3 $S/unit_r2b.txt; cd /Users/arsis/zlayt-pm-project && git log --oneline | head -3",
 "timeout": 130000
}
````

### User / tool · 2026-11-02T12:08:57.476Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad tail -3 $S/unit_r2b.txt cd /Users/arsis/zlayt-pm-project git log --oneline head -3. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:09:02.145Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; timeout 150 bash -c \"until grep -qE 'passed|failed' $S/unit_r2b.txt; do sleep 3; done\"; tail -3 $S/unit_r2b.txt; cd /Users/arsis/zlayt-pm-project && git log --oneline | head -3",
 "timeout": 170000
}
````

### User / tool · 2026-11-02T12:09:02.273Z

**tool result**
````
/bin/bash: timeout: command not found
........................................................................ [ 46%]
........................................................................ [ 49%]
.......................................................................5dfba88 test(qa): T-113/T-112 three consecutive live 3-runs from clean 63e18ed, ship_bar_met x3
2790918 refactor(backend): summary_trim reads negation and side words from the lexicon (T-105 r2 leftover)
f4d68bb fix(backend): T-132 attribution-only history unit extends to the next clause; MS is not Ms.; pin the history-word gate
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:09:08.070Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; n=0; until grep -qE ' passed| failed' $S/unit_r2b.txt || [ $n -gt 55 ]; do sleep 3; n=$((n+1)); done; tail -2 $S/unit_r2b.txt; cd /Users/arsis/zlayt-pm-project && git diff 2790918 HEAD --stat -- app tests/unit memory/contracts | tail -3",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T12:10:05.458Z

**tool result**
````
..................................................                       [100%]
3214 passed, 4 skipped in 182.56s (0:03:02)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:11:09.964Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-128-staff-engineer-r2.md",
 "content": "# T-128 review, round 2 - staff-engineer-reviewer\n\nCard: summary trim must never leave a fragment, kill the T-112 r3 surviving mutants, and (orchestrator note) read negation words from the lexicon. Commits 180138c (structural rule) and 2790918 (lexicon negation). I worked on `git archive` copies in my scratchpad: `T128_9_r2/repo` is 1f0a164 (the code of 180138c), `T128_9_r2b/repo` is 2790918. After the second archive HEAD moved to 5dfba88; `git diff 2790918 HEAD --stat -- app tests/unit memory/contracts` is empty, so the code I reviewed is HEAD's. Scripts are in `artifacts/review-evidence/T-128-129-r2/`.\n\n**Verdict: changes.** One major, three minors, one nit. The rule is implemented as the orchestrator specified and it holds every probe from round 1. But the claim \"fragments are impossible by construction\" (module docstring, api.md, handoff) is false: the rule guards the start of the summary and `,` / `and` / `with` joins, and does not guard a kept later clause that is itself dependent. 12 of 17 fresh probes of that shape leave a fragment or a mis-attached result.\n\n## 1. Deterministic checks\n- `tests/unit` at 1f0a164: 3186 passed, 4 skipped, 0 failed (the handoff says 3189; the working tree had more tests than HEAD). At 2790918: 3214 passed, 4 skipped, 0 failed. `tests/unit/test_summary_trim.py` at 2790918: 286 passed.\n- No model or network: `summary_trim.py` is pure code.\n\n## 2. Round-1 probes re-run (probe_t128_r2.py, probe_t128b_r2.py)\n- 31 fragment probes: 27 stay whole, 3 go to the tray (`''`, every clause unsupported), 1 trims to a whole clause (`MRI done; mild disc bulge noted at L4.` -> `MRI done.`). None leaves a fragment. The 10 clear fragments of round 1 now stay whole.\n- 12 should-trim probes: 10 trim to whole clauses (the four two-sentence pairs that the round-1 guard blocked now trim). 2 stay whole: `Was seen at the ER; surgery recommended.` (prefix has one content word, `ER`) and `Headache; CT scan ordered; ibuprofen advised.` (one content word). Both fail safe, the judge sees them. The handoff says `Was seen at the ER` trims; the test (test_summary_trim.py:613-615) asserts it does not.\n\n## 3. Fresh probes (fresh_t128_r2.py, 26 pairs): the claim \"impossible by construction\" fails\nClean results: `Neck pain with stiffness; surgery recommended.` -> `Neck pain with stiffness.`, `Ankle pain; X-ray taken; no fracture.` -> `Ankle pain; no fracture.`, `Neck pain, injection given, relief noted.` stays whole (comma join), `Pain; MRI ordered; ...` stays whole (one-word prefix), `Surgery recommended; neck pain.` stays whole. Then the kept-later-clause shape, where the clause before it is removed and the separator is `;` or `.`:\n- `Neck pain; injection given; resulting in relief.` -> `Neck pain; resulting in relief.`\n- `Wrist pain; splint applied; which helped.` -> `Wrist pain; which helped.`\n- `Neck pain; cast applied; however, improving.` -> `Neck pain; however, improving.`\n- `Shoulder pain; surgery performed; due to torn labrum.` -> `Shoulder pain; due to torn labrum.` (the card title's own example, `Due to torn meniscus.`, with `;` instead of `,`)\n- `Back pain; ultrasound done; thereafter, improvement.` -> `Back pain; thereafter, improvement.`\n- `Back pain; epidural given; as a result, less pain.` -> `Back pain; as a result, less pain.`\n- `Wrist fracture; cast applied; including follow-up.` -> `Wrist fracture; including follow-up.`\n- `Neck pain; ibuprofen prescribed; 3 times daily.` -> `Neck pain; 3 times daily.`; `Neck pain; physical therapy started; for six weeks.` -> `Neck pain; for six weeks.`; `Knee pain; brace issued; as needed.` -> `Knee pain; as needed.`\n- Mis-attached result: `Head injury; CT ordered; negative.` -> `Head injury; negative.`; `Hip pain; X-ray taken; unremarkable.` -> `Hip pain; unremarkable.` (the imaging result now reads as the finding on the injury).\nThat is 10 dependent fragments and 2 mis-attached results of 17 probes of this shape. Rule 3 (summary_trim.py, the loop over `clauses[i - 1][1]`) only looks at `,` `and` `with`; the docstring says \"only ';' or a sentence end lets a clause stand alone\", which is true of the grammar only for independent clauses.\n\n## 4. Mutation of the tests (mut_t128_r2.py on 1f0a164; mut2_t128_r2.py on 2790918)\n- Rule mutants, 16 on 1f0a164: 14 killed (prefix <1, <3, prefix to the LAST cut, rule 3 off, rule 3 without `,`, without `and`, without `with`, rule 3 ignoring the previous removal, tray condition, participle merge off, join strength reversed, final period dropped, no-removal marks changed, quote negation off). Survived 2: \"rule 1 off\" (equivalent: an empty prefix has 0 content words, rule 2 fires; the handoff says so) and \"capitalise off\" (dead code since the first kept clause is always clause 0).\n- Abbreviation sweep (sweep_r2.py, absolute script path): 27 entries, each set to a dead word, `survivors: []`. IV, hep, ekg were deleted from the table as inert rather than tested; orif is now killed. Reverse-direction pairs (rev_r2.py): 0 of 18 over-trim, including `ORIF wrist.` and `RCR performed.` that over-trimmed in round 1.\n- Lexicon mutants on 2790918 (8): 6 killed (quote extra=False, quote negation off, clause negation only `no`, never, clause side words never, prefix <1). Survived 2: the `n't` contraction branch (`Neck pain; couldn't sleep.` over `Neck pain.` stays whole under the mutant and 286 tests pass) and `quote sides ignored` (not shown to be equivalent).\n\n## 5. Negation moved to the lexicon (commit 2790918): behaviour change\nChecked: no `_NEG`, `_NEG_WORDS` or `_SIDE_WORDS` assignment remains (`grep -n` of summary_trim.py at 2790918 shows `grounding.aq(\"side\")`, `grounding.is_negation_word`, `grounding.has_negation(ex, extra=True)`), and a test pins that. Old (1f0a164) against new, same pairs (neg_diff_t128_r2.py, neg_diff2, neg_diff3: 75 pairs):\n- Summary side, now trimmed (was kept, correct): `absence of numbness`, `lacks radiation`, `free of numbness`, `nothing abnormal found`, `absence of weakness`, `lacks coordination`, `free of weakness`, each over `Neck pain.` -> `Neck pain.` These were under-trims.\n- Quote side, a negation word now vouches (was trimmed): `Neck pain; no numbness.` over `Neck pain. Nothing else reported.` and over `Neck pain. Absence of tingling.` now stay whole (judge sees them). Looser, in the safe direction; same lenient design as `unremarkable`.\n- `deny`: `Neck pain; no trouble breathing.` over `Neck pain. Deny dyspnea.` changes from kept to trimmed (`Neck pain.`), a faithful paraphrase over-trimmed because the quote's only negation is the bare word `deny`. Pairs that share a word with the quote (`no nausea` over `Deny N/V`, `no loss of consciousness` over `Deny syncope`) stay whole. `Denying` and `Denial of` were never recognised by either version (`no trouble breathing` over `Denying dyspnea.` trims in both).\n- `denies fever` as a summary clause trims in both. Under-trim: none found beyond the unrecognised deny forms.\n\n```json\n{\"card\": \"T-128\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 1f0a164 (180138c code) and 2790918 in scratchpad T128_9_r2 / T128_9_r2b; HEAD at end of review 5dfba88 (app/tests/contract unchanged since 2790918); app/backend/summary_trim.py, tests/unit/test_summary_trim.py, app/backend/grounding.py has_negation/is_negation_word, memory/contracts/api.md summary-trim section; fixture/no backend, no network\",\n \"exercised\": [\n  \"python3 tools/board.py show T-128, T-129; read reviews/T-128-staff-engineer.md and T-129-staff-engineer.md; git show 1f0a164; git diff HEAD on the working tree\",\n  \".venv/bin/python -m pytest tests/unit -q in the 1f0a164 archive: 3186 passed, 4 skipped; in the 2790918 archive: 3214 passed, 4 skipped; test_summary_trim.py: 286 passed\",\n  \"probe_t128_r2.py (the 31 round-1 fragment probes) and probe_t128b_r2.py (the 12 should-trim pairs) against 1f0a164\",\n  \"fresh_t128_r2.py: 26 new pairs (9 should-trim or should-hold, 17 kept-later-clause fragment shapes)\",\n  \"mut_t128_r2.py: 16 rule mutants on summary_trim.py; mut2_t128_r2.py: 8 lexicon mutants on 2790918\",\n  \"sweep_r2.py: 27 abbreviation entries set dead one at a time (survivors: none); rev_r2.py: 18 reverse-direction pairs (0 over-trim)\",\n  \"neg_diff_t128_r2.py, neg_diff2_t128_r2.py, neg_diff3_t128_r2.py: 75 negation pairs, old (1f0a164) against new (2790918) in separate processes\",\n  \"manual mutant: n't branch removed from new_salient on a copy of 2790918 -> 286 passed and three contraction clauses stay whole\",\n  \"grep of summary_trim.py for _NEG, _NEG_WORDS, _SIDE_WORDS, has_negation, is_negation_word\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"deterministic_trim_is_code\": 5, \"fragment_safety\": 3, \"unsupported_removal_precision\": 4, \"faithful_paraphrase_survival\": 4, \"test_strength\": 4, \"lexicon_single_source\": 5, \"doc_matches_code\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"'Fragments are impossible by construction' is false: a kept later clause that depends on a removed one survives when the separator is ';' or '.' (12 of 17 fresh probes)\",\n   \"evidence\": \"`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/fresh_t128_r2.py <archive>`: 'Shoulder pain; surgery performed; due to torn labrum.' -> 'Shoulder pain; due to torn labrum.'; 'Neck pain; injection given; resulting in relief.' -> 'Neck pain; resulting in relief.'; 'Wrist pain; splint applied; which helped.' -> 'Wrist pain; which helped.'; 'Neck pain; cast applied; however, improving.' -> 'Neck pain; however, improving.'; 'Back pain; epidural given; as a result, less pain.' -> 'Back pain; as a result, less pain.'; 'Wrist fracture; cast applied; including follow-up.' -> 'Wrist fracture; including follow-up.'; 'Neck pain; physical therapy started; for six weeks.' -> 'Neck pain; for six weeks.'; 'Head injury; CT ordered; negative.' -> 'Head injury; negative.'; 'Hip pain; X-ray taken; unremarkable.' -> 'Hip pain; unremarkable.'. summary_trim.py trim(), rule (3) checks only clauses[i - 1][1] in (',', 'and', 'with'). Docstring: 'Fragments are impossible by CONSTRUCTION'; api.md summary-trim section says the same; D-054 'never leaving a fragment'.\",\n   \"why_it_matters\": \"This is the round-1 finding (fragment class) with a different separator, and the card title names 'Due to torn meniscus.' as the thing that must not happen. The word list is gone but the guarantee is not delivered: the first clause and the prefix are safe, the tail is not. Nothing is invented, the quote and trace stay and judge 1 sees the text, so it is not a blocker, but 'Head injury; negative.' attaches an imaging result to the wrong finding and the docs promise it cannot happen.\",\n   \"fix\": \"Keep the structural approach and extend it to the tail: either (a) allow a removal only when every clause after the first removal is also removed (suffix cut; otherwise the whole summary goes to judge 1), or (b) require a kept clause that follows a removed one to start with a content word that is not in _STOP and not a participle (reuse _STOP and _PARTICIPLE, no new list) and to carry its own head noun. Or soften the docstring, api.md and D-054 to name exactly what is guaranteed (first clause, 2-word prefix, no comma/and/with orphan).\",\n   \"acceptance_test\": \"tests/unit/test_summary_trim.py: the 12 summaries above return changed False (or, for option b, none of them yields a kept clause starting with resulting/which/however/due/as/including/for/negative/unremarkable); 'Ankle pain; X-ray taken; no fracture.' still trims to 'Ankle pain; no fracture.' and 'Neck pain. Surgery recommended; follow-up in two weeks.' still trims.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The lexicon move makes bare 'deny' count as no negation: a faithful paraphrase is now trimmed ('no trouble breathing' over 'Deny dyspnea.')\",\n   \"evidence\": \"`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/neg_diff3_t128_r2.py <1f0a164 archive> <2790918 archive>`: DIFF 'Neck pain; no trouble breathing.' | 'Neck pain. Deny dyspnea.' | old: [False, 'Neck pain; no trouble breathing.'] | new: [True, 'Neck pain.']. grounding.has_negation('Deny N/V.', extra=True) is False; lexicon.yaml:1412 negation_word is '\\\\b(?:no|not|none|never|without|denies|denied|negative|neither|nor|absent)\\\\b' (no deny, denying, denial).\",\n   \"why_it_matters\": \"A clause is removed (and in a one-clause summary the entry goes to the could-not-verify tray) when the summary says 'no X' and the quote's only negation is 'deny' with a different noun. Fail-direction is visible (the paralegal sees the trim note), and the orchestrator already queued a researcher card for the lexicon, so this is minor. The same gap hides 'denying' and 'denial of' in both old and new code.\",\n   \"fix\": \"Researcher card: add deny, denying, denial of to negation_word (and a hit/miss example) in app/llm/lexicon.yaml; add the pair above as a test in test_summary_trim.py so it goes red until then.\",\n   \"acceptance_test\": \"T.trim('Neck pain; no trouble breathing.', 'Neck pain. Deny dyspnea.')['changed'] is False and the same for 'Denying dyspnea.' and 'Denial of dyspnea.'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Test gap: the n't contraction branch of new_salient is untested; removing it leaves 286 tests green and contraction clauses unsupported-but-kept\",\n   \"evidence\": \"Copy of 2790918 with `w.endswith(\\\"n't\\\") or grounding.is_negation_word(w)` changed to `grounding.is_negation_word(w)`: `pytest tests/unit/test_summary_trim.py` -> 286 passed; T.trim(\\\"Neck pain; couldn't sleep.\\\", 'Neck pain.')['changed'] False, same for \\\"didn't miss work\\\" and \\\"can't lift\\\" (the unmutated code trims all three). Also 'quote sides ignored' (mut2_t128_r2.py) survives.\",\n   \"why_it_matters\": \"The card's second half is 'kill the surviving mutants'; this refactor opened a new one in code it rewrote, and a regression there would silently stop trimming negated clauses with contractions.\",\n   \"fix\": \"Add a parametrized test over couldn't / didn't / can't clauses with a quote that has no negation (trimmed) and one that has (kept); add one quote-side test where the quote says 'bilateral' only.\",\n   \"acceptance_test\": \"The contraction-branch mutant and the quote-sides mutant in mut2_t128_r2.py print KILLED.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Handoff says 'Was seen at the ER' trims; the test asserts it does not; two dead lines remain\",\n   \"evidence\": \"Handoff: '8 positive controls trim incl. the two-sentence and Was seen at the ER cases'. tests/unit/test_summary_trim.py:613-615 test_the_first_clause_is_never_removed: `assert not r['changed']` for that pair. summary_trim.py `if drop[0]: return unchanged` is equivalent to rule 2 (the handoff says so) and `out = out[:1].upper() + out[1:]` survives deletion (the first kept clause is always clause 0).\",\n   \"why_it_matters\": \"Handoff accuracy and dead code only; behaviour is the safe one.\",\n   \"fix\": \"Correct the handoff wording; delete or comment the capitalise line.\",\n   \"acceptance_test\": \"none needed\"}\n ],\n \"whats_right\": [\n  \"All 31 round-1 fragment probes now stay whole or go to the tray, and the 4 two-sentence should-trim pairs that the old guard blocked trim again; prefix and first-clause rules are each killed by a named test.\",\n  \"Abbreviation table sweep is clean (27 entries, no survivors) and the reverse ORIF/RCR over-trim is gone (0 of 18).\",\n  \"Negation and side words come from the lexicon through grounding (no private lists), with a source-level guard test; the move closes under-trims for absence of, lacks, free of and nothing.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T12:11:10.113Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-128-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:11:21.391Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-128-129-r2; for f in neg_diff_t128_r2 neg_diff2_t128_r2 neg_diff3_t128_r2; do grep -c '^ (\"' $E/$f.py; done; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/T128_9_r2b/repo && /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF' 2>&1 | grep -v setpgid\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import summary_trim as T\nfor s in [\"Neck pain; couldn't sleep.\",\"Neck pain; didn't miss work.\",\"Neck pain; can't lift.\"]:\n    print(s, T.trim(s,\"Neck pain.\")[\"changed\"])\nEOF"
}
````

### User / tool · 2026-11-02T12:11:21.605Z

**tool result**
````
40
17
18
Neck pain; couldn't sleep. True
Neck pain; didn't miss work. True
Neck pain; can't lift. True
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:11:49.538Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-129-staff-engineer-r2.md",
 "content": "# T-129 review, round 2 - staff-engineer-reviewer\n\nCard: a non-library preamble must not become record 1; round 2 asks that GET case serves `unsplit` / `preamble` (matching api.md) and that a re-run after the numbering changed leaves no decided item on a shifted record number. Commit 1f0a164. I worked on a `git archive` of 2790918 in my scratchpad (`T128_9_r2b/repo`, with `m4/repo` as a mutation copy); `git diff 2790918 HEAD --stat -- app tests/unit memory/contracts` is empty at the end of the review (HEAD 5dfba88), so the code is HEAD's. Scripts are in `artifacts/review-evidence/T-128-129-r2/` (`t129_r2.py`, `mut_t129_r2.py`).\n\n**Verdict: pass.** Both round-1 findings are fixed and verified through the real routes and the real re-ingest path. Two minors remain (tests narrower than the code; one ordering nit), neither changes behaviour today.\n\n## 1. Deterministic checks\n- `tests/unit` in the 2790918 archive: 3214 passed, 4 skipped, 0 failed. The three new tests in `tests/unit/test_ingest.py` pass.\n\n## 2. GET case serves the fields (t129_r2.py part A, FastAPI TestClient on the real app, loopback peer)\n`POST /api/cases` and `GET /api/cases/{token}` for three pastes return identical `(id, unsplit, preamble)` per record:\n- cover sheet above two records: `[('r1', False, False), ('r2', False, False), ('r3', True, True)]` on both.\n- two records only: `[('r1', False, False), ('r2', False, False)]`.\n- a free note between two records: `[... ('r3', True, False)]`.\nGET `warnings` is `[]` and POST has `UNSPLIT_TEXT`, which is what api.md now says (the warning is POST-only). The fields are in both api.md examples (memory/contracts/api.md, the POST and GET record examples) and the text at the `UNSPLIT_TEXT` warning code names both responses. `grep -rn \"unsplit\\|preamble\" app/frontend` still prints nothing, so no label is shown yet; the handoff lists that as left, and it is a frontend card, not this one.\n\n## 3. Re-run after the numbering changed (t129_r2.py part B, same sqlite file, ingest_case twice)\nStored under the old numbering (a dated cover as r1, visits r2 and r3), then I accepted the gap `f_gap_r1_r2`, accepted amount `a1` ($6,240, then on r2) and dismissed `a2` ($185). Re-ingest of the same paste with an undated cover sheet on top:\n- records after: `r1 2026-01-09, r2 2026-03-20, r3 None`.\n- every item that cites a record whose span changed is back to `pending`; `decided items left after shift: []`. Events keep the history: `a1 accept, a2 dismiss, f_gap_r1_r2 accept, a1 reset, a2 reset, f_gap_r1_r2 reset`.\n- the stale `f_gap_r2_r3` row is gone, `f_date_r3` is new and pending.\nSo no accepted or dismissed item (flag or amount) points at a shifted number. The unit test covers only the flag; see finding 1.\n\n## 4. Mutation of the tests (mut_t129_r2.py: 14 mutants of pipeline.py / present.py against test_ingest.py + test_api_routes.py + test_pipeline.py)\nKilled (9): marks never stored; `unsplit` always False; `preamble` always False; `_recs_by_id` never sets preamble; reset is a no-op; moved set limited to vanished ids; no `computed.record_ids` fallback; `ingest_case` passes no `now`; marks early-return inverted.\nSurvived (5): reset only flags; reset skips amounts; reset only accepted items (dismissed and edited stay bound to the old number); no evidence-record fallback; `run_pipeline` passes the default `now` to `_store_records` (reset events then carry time 0.0).\n\n```json\n{\"card\": \"T-129\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive of 2790918 (HEAD 5dfba88, app/tests/contract identical) in scratchpad T128_9_r2b and m4; app/backend/pipeline.py _store_record_marks/_reset_reviewed_on/_store_records/_persist, app/backend/present.py _recs_by_id/record_view, tests/unit/test_ingest.py, memory/contracts/api.md; fixture/no model call, no network\",\n \"exercised\": [\n  \"python3 tools/board.py show T-129; read reviews/T-129-staff-engineer.md; git show 1f0a164 (pipeline.py, present.py, api.md, test_ingest.py)\",\n  \".venv/bin/python -m pytest tests/unit -q in the 2790918 archive: 3214 passed, 4 skipped, 0 failed\",\n  \"t129_r2.py part A: FastAPI TestClient on create_app (loopback peer), POST /api/cases then GET /api/cases/{token} for a cover-sheet paste, a plain paste and a mid-note paste; compared record fields and warnings\",\n  \"t129_r2.py part B: case stored under the old numbering, gap accepted, amount accepted, amount dismissed, re-ingested on the same sqlite file with the cover sheet on top; listed item statuses, cited records and the event log\",\n  \"mut_t129_r2.py: 14 mutants of pipeline.py / present.py against test_ingest.py, test_api_routes.py, test_pipeline.py (9 killed, 5 survived)\",\n  \"grep of app/frontend for unsplit / preamble; read pipeline.py _store_records lines 150-215 including the BEGIN/COMMIT block and _persist\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"numbering_stability\": 5, \"nothing_dropped_D027\": 5, \"api_exposes_preamble\": 4, \"contract_matches_code\": 5, \"test_strength\": 3, \"upgrade_safety\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"The reset on a shifted record number is pinned for accepted flags only; amounts, entries, dismissed and edited decisions and the run_pipeline path have no test\",\n   \"evidence\": \"`.venv/bin/python -I artifacts/review-evidence/T-128-129-r2/mut_t129_r2.py <archive>`: 'reset flags only' (pipeline.py _reset_reviewed_on `for kind in (\\\"entry\\\", \\\"amount\\\", \\\"flag\\\")` -> `(\\\"flag\\\",)`), 'reset amounts skipped', 'reset accepted only' (`it[\\\"review_status\\\"] != \\\"pending\\\"` -> `== \\\"accepted\\\"`), 'no evidence fallback' (_item_record_ids) and 'run_pipeline passes now=0.0' each leave 123 tests passed. tests/unit/test_ingest.py test_a_rerun_after_the_numbering_changed_resets_decisions_made_on_shifted_records accepts one gap flag and asserts flags only.\",\n   \"why_it_matters\": \"The code is right today (part B shows an accepted amount and a dismissed amount reset), but an accepted amount or an edited entry bound to the wrong record is the export-relevant case and the one a later edit to this helper would break unnoticed. The card AC and the orchestrator's note name the accepted flag, which is why this is minor and not major.\",\n   \"fix\": \"Extend the test: accept a gap flag, accept an amount and dismiss another, re-ingest with the cover on top, assert all three are pending and that the event log has the reset; add one run_pipeline-path assertion that the reset event has a non-zero timestamp.\",\n   \"acceptance_test\": \"The five mutants above print KILLED in mut_t129_r2.py.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"_reset_reviewed_on commits its resets before the records transaction begins\",\n   \"evidence\": \"app/backend/pipeline.py _store_records: `_reset_reviewed_on(conn, cid, {...}, now)` runs before `conn.execute(\\\"BEGIN\\\")`; if the DELETE/INSERT block raises and rolls back, the decisions were already reset while the records stay on the old numbering.\",\n   \"why_it_matters\": \"Fails in the safe direction (items pending, exception propagates, event log intact) and needs a DB error to trigger, so it is only an ordering note.\",\n   \"fix\": \"Move the reset inside the same transaction, or comment that reset-then-fail is intended.\",\n   \"acceptance_test\": \"none needed\"}\n ],\n \"whats_right\": [\n  \"GET case and POST case serve the same unsplit and preamble per record, and api.md names which response carries the UNSPLIT_TEXT warning (POST only).\",\n  \"A re-ingest after the numbering changed resets every decided item that cites a moved record (flags and amounts), keeps the events, removes the stale row, and leaves an unchanged case alone (same-numbering test).\",\n  \"Marks are stored in cases.config_json with no schema change and refreshed before the early return, so a model split that moves records updates them too (the inverted-early-return mutant is killed).\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T12:11:49.690Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-129-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:11:52.470Z

**tool call — Bash**
````
{
 "command": "for f in T-128 T-129; do python3 - $f <<'EOF'\nimport re,json,sys\nt=open(f\"reviews/{sys.argv[1]}-staff-engineer-r2.md\").read()\nm=re.findall(r\"```json\\n(.*?)```\",t,re.S); assert len(m)==1\nd=json.loads(m[0]); print(d[\"card\"],d[\"verdict\"],[f[\"severity\"] for f in d[\"findings\"]])\nEOF\ndone; python3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T12:11:52.654Z

**tool result**
````
T-128 changes ['major', 'minor', 'minor', 'nit']
T-129 pass ['minor', 'nit']
ok (134 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:11:58.794Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t128_t129_r2_patterns.md",
 "content": "---\nname: project_t128_t129_r2_patterns\ndescription: r2 at 1f0a164/2790918 - T-128 changes (structural rule leaves dependent kept tail clauses after ';' or '.'; deny not in lexicon), T-129 pass (GET serves fields, shifted-record reset verified; tests flag-only)\nmetadata:\n  type: project\n---\n\n- T-128 r2 (180138c + 2790918, changes: 1 major, 2 minor, 1 nit): first-clause/2-word-prefix/comma-and-with rule holds all 31 r1 probes, sweep 27/27 killed, 0/18 reverse over-trim. But \"impossible by construction\" is false: a kept later clause after a removed one joined by ';' or '.' stays ('Shoulder pain; due to torn labrum.', 'Head injury; negative.' = CT result re-attached). 12 of 17 fresh probes. Lexicon move: bare 'deny' no longer a negation (one faithful paraphrase over-trims), contraction branch of new_salient untested.\n- T-129 r2 (1f0a164, pass: 1 minor, 1 nit): GET/POST serve unsplit+preamble identically; accepted gap, accepted amount and dismissed amount all reset after a numbering shift. Tests only assert the accepted flag; 5 of 14 mutants survive (flags-only, amounts skipped, accepted-only, evidence fallback, now=0.0).\n\n**Why:** a structural rule fixed the word-list problem for the start of the summary but the same fragment class moved to the tail; a fix verified on one item kind (flag) leaves the sibling kinds unpinned.\n**How to apply:** for \"by construction\" claims, enumerate where the construction does not reach (tail, other separators) and probe those; for reset/migration cards, mutate the item-kind and status filters, then check each kind through the real re-ingest. Sweep scripts must be given absolute paths (subprocess cwd changes, a relative script path made every mutant look killed in 0.7 s); a guard hook blocks `sed -i` and any `>` in a shell command on reviewer paths, use the Edit tool.\n\nRelated: [[project_t128_t129_t127_patterns]], [[project_t112_trim_patterns]].\n"
}
````

### User / tool · 2026-11-02T12:11:58.886Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t128_t129_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:12:02.388Z

**tool call — Bash**
````
{
 "command": "echo '- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — T-128 r2 changes: structural rule leaves dependent tail clauses, deny gap; T-129 r2 pass: tests flag-only, relative sweep path false-kills' >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md; tail -2 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md | cut -c1-120"
}
````

### User / tool · 2026-11-02T12:12:02.471Z

**tool result**
````
- [T-120 r3 patterns](project_t120_r3_patterns.md) — f7829c1 pass: strip-then-scan verified, MS honorific collision, u
- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — T-128 r2 changes: structural rule leaves dependent tai
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:12:06.480Z

T-128 r2 is `changes` with one major: "fragments are impossible by construction" is false, because a kept later clause that depends on a removed one survives after `;` or `.` (12 of 17 fresh probes). Examples are `Shoulder pain; due to torn labrum.` and `Head injury; negative.`. Minors: bare `deny` no longer counts as negation after 2790918 (one faithful paraphrase now over-trims), and the `n't` contraction branch is untested.

T-129 r2 is `pass`, with only a minor and a nit. GET case serves `unsplit` and `preamble` identically to POST, and a re-run after a numbering shift resets decided flags and amounts. The tests pin only the accepted flag, and 5 of 14 mutants survive. Both reviews are in `/Users/arsis/zlayt-pm-project/reviews/` as `T-128-staff-engineer-r2.md` and `T-129-staff-engineer-r2.md`.
