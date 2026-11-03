# T-067 round 4 claims-adjuster review (commit 8634bfe, D-043)

Reviewer: claims-adjuster-reviewer (Gary Pruitt persona), model claude-haiku-5-5 (the model I am running as; the dossier's expected id differs, so the actual id is recorded).
Binding rule: D-043 (memory/ORCHESTRATOR_DECISIONS.md:51), not the clause-scoped rules of r1 to r3. Bare "pain behavior(s)" flagging accepted under D-043.
Scope: commit 8634bfe, extracted with `git archive` into the session scratchpad. The live tree has an uncommitted app/backend/flags.py edit that is not part of this card; `git diff 8634bfe -- app/backend/credibility.py` is empty, so the live credibility code equals the commit. The probe ran on the archive.

## Summary

**Verdict: fail.** One blocker, one major, one minor, and one minor that is a question for Chris.

The D-043 gate works for the forms it names. Mixed-side and positive-first sentences flag in every comma, "but", "and" and "or" form. "Not consistent" and the other named families flag. The clean allow-list forms stay silent. One structural bypass remains: the allow-list test runs on the sentence unit, and the unit splitter ends a unit at a semicolon and at a line break. A clean-looking term clause after a semicolon is therefore silent, although D-043 says a second clause flags.

Carry-over from r1 to r3:
- r1 negation and named-family blockers: hold (N01 to N16, R01 to R14).
- r2 mixed-result blocker (positive side dropped): closed for comma, "but" and "and" forms; the semicolon form is new finding F1.
- r3 blocker 1 (positive named before the term is silent): closed (P01 to P06 flag).
- r3 blocker 2 ("not consistent" silent): closed (X01 flags).
- r3 major 1 ("Negative Waddell signs." and "no positive findings"): X14 flags; C08 is silent (F3, minor).
- r3 major 2 ("negative or equivocal"): closed (X04 flags).
- r3 major 3 (bare "pain behaviors"): flags (E13, V07), accepted under D-043.
- r3 minor 2 (excerpt cut at a semicolon): still open, escalated to major (F2).

Accepted under D-043, not findings (fail toward flagging): plain denials and normal-result negatives that D-043 does not list still flag, for example "No evidence of symptom magnification." (N02), "Waddell signs were not present." (N05), "Malingering ruled out." (C09), "Waddell signs were normal." (C07).

## Exercised

- `git show --stat 8634bfe`; `git show 8634bfe -- tests/unit/test_flags_pass.py` (full test diff read).
- `git archive 8634bfe | tar -x -C <scratchpad>/t067r4`; read `app/backend/credibility.py` (60 lines, cat -n), `app/backend/sentences.py` 1-80, `app/backend/flags.py` 15-100, `app/backend/flag_templates.py` 125-140, `memory/ORCHESTRATOR_DECISIONS.md` D-038 (line 46) and D-043 (line 51), `app/llm/lexicon.yaml` 1159-1169.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider` on the live tree: `29 passed in 0.51s`. Same command on the archive: `29 passed in 0.40s`.
- Archive: `pytest -q tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py tests/unit/test_flag_templates.py -p no:cacheprovider`: `68 passed in 0.45s`.
- Wrote `artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py` and ran `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py <archive>`: `rows=139 mismatches=3 ['O01', 'O03', 'O04']`. Output saved to `artifacts/review-evidence/T-067-claims-adjuster-r4-probe.out.txt`.
- The probe covers every attack string from the r1 probe (E01 to E14, N01 to N15, and the multi-sentence M01 as N16), the r1 recall probe (R01 to R14), the r2 brief and own strings (B01 to B18), the r3 probe (M01 to M12, D01 to D08, C01 to C11, V01 to V09, X01 to X14, P01 to P06), and 17 own rows (O01 to O17). Each row is judged against D-043.
- Root-cause run, `.venv/bin/python -I` on the archive: `sentences.stripped_spans` and `credibility.scan` on the bypass strings (output quoted in F1).
- Not exercised: the sample case in the app and the eval harness (this card is a function change).

## Findings

Details in the JSON block. Verdict by rule: one blocker, so `fail`.

- **blocker F1**: a clean-looking term clause after a semicolon or a line break is silent (O01, O03, O04), though D-043 says a second clause flags.
- **major F2**: the flag excerpt is cut at a semicolon and drops the clause that carries the positive result (O13, M07 and five others). This is r3 minor 2, escalated.
- **minor F3**: the code's allow-list is wider than the six forms D-043 lists, and D-043 does not record the difference.
- **question**: whether a semicolon or a line break makes a second clause under D-043 (decides F1's severity).

```json
{"card": "T-067", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 8634bfe (D-043), via git archive into the session scratchpad; live tree has an uncommitted app/backend/flags.py edit not in this card, and credibility.py is identical to the commit; no app URL and no sample case run (function-level probes through credibility.scan and flags.run_flag_pass with FakeCall)",
 "exercised": [
   "git show --stat 8634bfe; git show 8634bfe -- tests/unit/test_flags_pass.py (full diff)",
   "git archive 8634bfe | tar -x -C <scratchpad>/t067r4; cat -n app/backend/credibility.py (60 lines); sentences.py 1-80; flags.py 15-100; flag_templates.py 125-140; lexicon.yaml 1159-1169; ORCHESTRATOR_DECISIONS.md D-038 (line 46) and D-043 (line 51)",
   "git diff 8634bfe -- app/backend/credibility.py on the live tree -> empty (identical)",
   "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider on the live tree -> 29 passed in 0.51s; on the archive -> 29 passed in 0.40s",
   "archive: pytest -q tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py tests/unit/test_flag_templates.py -p no:cacheprovider -> 68 passed in 0.45s",
   ".venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py <archive> -> rows=139 mismatches=3 ['O01','O03','O04']; output in artifacts/review-evidence/T-067-claims-adjuster-r4-probe.out.txt",
   "root-cause run (.venv/bin/python -I on the archive): sentences.stripped_spans and credibility.scan on 'Straight leg raise positive; Waddell signs negative.', 'Positive on the right; no Waddell signs.', a line-break variant, a comma variant and 'Waddell signs negative; straight leg raise positive.'",
   "r1, r2 and r3 attack strings re-run (r1 probe 30+1, r1 recall 14, r2 brief and own 18, r3 probe 60, own 17); every row judged against D-043, not the earlier clause-scoped rules"
 ],
 "verdict": "fail",
 "scores": {"d043_allow_list_gate": 2, "d043_second_clause_flags": 2, "mixed_and_positive_first_recall": 5, "not_consistent_and_family_variants": 5, "excerpt_is_whole_sentence": 3, "allow_list_matches_d043_text": 3, "commit_suite_green": 5, "template_neutral_and_verbatim": 5},
 "findings": [
  {"severity": "blocker",
   "title": "A clean-looking term clause after a semicolon or line break is silent; D-043 says a second clause flags",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-r4-probe.out.txt: 'O01 want=flag got=silent n=0 MISMATCH :: Straight leg raise positive; Waddell signs negative.'; 'O03 want=flag got=silent n=0 MISMATCH :: Positive on the right; no Waddell signs.'; 'O04 want=flag got=silent n=0 MISMATCH :: Straight leg raise positive; Waddell testing was not done.'. Same clauses joined by a comma flag: 'Straight leg raise positive, Waddell signs negative.' -> scan returns 'Waddell signs'. Root cause at 8634bfe: sentences.py:35 (';' ends a unit) and sentences.py:37 (line break ends a unit); credibility.py:54-55 runs _clean_negation on that unit only. Root-cause output: 'Straight leg raise positive; Waddell signs negative.' units -> ['Straight leg raise positive;', 'Waddell signs negative.'] scan -> []. Line-break variant O02 'Straight leg raise positive<line break>Waddell signs negative.' is also silent (judged, not counted). No other flag category fires on O01, O03 or O04 (probe prints none). Test gap: tests/unit/test_flags_pass.py:270 comment covers only the first-half direction ('Waddell signs negative; ...'); no test pins a clean clause after a semicolon.",
   "why_it_matters": "D-043 (memory/ORCHESTRATOR_DECISIONS.md:51) says 'Anything with a second clause, contrast word or side qualifier flags'. The code's own docstring (credibility.py:3-4) says 'A comma, semicolon, contrast word, side qualifier or any extra words means it flags'. The sentence 'Straight leg raise positive; Waddell signs negative.' is two clauses, so D-043 requires a flag, and the code is silent. The same two clauses flag when joined by a comma (M-series and P-series show it), so the result depends on punctuation. Honest harm: in O01, O03 and O04 the silenced clause is not a credibility term, so no credibility term is hidden; but 'Positive on the right; no Waddell signs.' gives the paralegal nothing, and 'Positive on the right' may be the other side of the Waddell result. The rule is violated structurally: any clean-looking term clause after a semicolon is silent. If Chris rules that a semicolon does not make a second clause, this downgrades to minor and D-043 must say so.",
   "fix": "Run the allow-list test (_clean_negation) on the whole sentence, split only at . ? ! and the sentence-ending rule, not at ';' or a line break. Any second clause, including one after a semicolon, then flags, as D-043 requires. Keep the excerpt rule separate (F2). Add to test_d038_everything_else_with_a_credibility_term_flags (tests/unit/test_flags_pass.py:216): 'Straight leg raise positive; Waddell signs negative.', 'Positive on the right; no Waddell signs.', 'Straight leg raise positive; Waddell testing was not done.'. Add the line-break form too if Chris rules a line break is a second clause.",
   "acceptance_test": "Run .venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-r4-probe.py on the fixed commit tree: O01, O03 and O04 print flag with the whole sentence as excerpt (O04 included); O05 and O13 still flag; O10 'Waddell signs negative!' and O16 'Straight leg raise positive. Waddell signs negative.' stay silent; mismatches=0. tests/unit/test_flags_pass.py has one assertion per O01, O03, O04 sentence and passes."},
  {"severity": "major",
   "title": "The flag excerpt is cut at a semicolon and drops the clause that carries the positive result (r3 minor 2, escalated)",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-r4-probe.out.txt: 'O13 ... :: Waddell testing was not done; positive on the right.' then 'excerpt=Waddell testing was not done; whole=False'; 'M07 ... excerpt=Waddell signs positive on the right; whole=False' (the negative clause is dropped); 'X13 ... excerpt=Subjective complaints out of proportion to exam findings; whole=False'; 'P03 ... excerpt=Positive Waddell signs on the left; whole=False'; 'O08 ... excerpt=No Waddell signs; whole=False'; 'O15 ... excerpt=Straight leg raise positive, no symptom magnification. whole=False'. Seven rows in total (M07, X13, P03, O05, O08, O13, O15). Cause: app/backend/flags.py:80-98 (lexicon_flags sets excerpt = text[a:b], the unit span) and app/backend/sentences.py:35.",
   "why_it_matters": "D-043 makes a sentence with a second clause flag so the paralegal sees the whole credibility sentence. The quoted excerpt now drops the second clause. O13's flag reads 'Waddell testing was not done;', which looks like a clean not-done; the positive side is in the text the flag does not quote. The quote is verbatim, so nothing is invented, and the flag exists, so this is not a blocker. The persona treats a softened weakness as a finding (dossier section 3). Escalated from r3 minor 2 because D-043 changed what a semicolon sentence means for the flag: the excerpt must now carry the whole sentence it flagged.",
   "fix": "Make the credibility flag excerpt the whole sentence, with the same sentence boundary as F1 (. ? ! and the sentence end). If Chris keeps the clause excerpt, record that choice and its reason in D-043 and add a SCOPE_CUTS row.",
   "acceptance_test": "Probe rows O13, M07, X13, P03, O08 and O15 print whole=True with the full sentence as excerpt, or D-043 names the clause excerpt as a scope cut. 'Waddell testing was not done; positive on the right.' is the excerpt for O13."},
  {"severity": "minor",
   "title": "The code's allow-list is wider than the six forms D-043 lists, and D-043 does not record the difference",
   "evidence": "Probe rows silent but not named in D-043: 'B05 want=silent-superset got=silent :: No symptom magnification.'; 'B03 0/5 Waddell' and 'C02 0/5 Waddell.' (D-043 names '0/5 Waddell signs.'); 'C08 Negative Waddell signs.' (reverse form). The code allow-list (credibility.py:29-38) also silences 'Waddell signs were negative', 'Waddell signs: negative', 'Waddell testing: not performed' and 'Waddell testing not done', which tests/unit/test_flags_pass.py:206-215 pins. D-043 (ORCHESTRATOR_DECISIONS.md:51) lists six forms in quotes.",
   "why_it_matters": "Each silent superset form is a single clause with no second clause, so no credibility fact is hidden here. The harm is that the written rule does not match the code, and D-043 says 'only allow-list sentences are silent'. An adjuster reading D-043 cannot tell which forms the paralegal will see. Minor because the silenced forms are clean negations.",
   "fix": "Chris records the full allow-list in D-043 (or narrows credibility.py:29-38 to the six named forms). No code change is needed if the list is recorded.",
   "acceptance_test": "D-043 names every form pinned in test_d038_only_allow_listed_clean_negations_are_silent (tests/unit/test_flags_pass.py:206), including 'No symptom magnification.' and 'Negative Waddell signs.', or the code narrows to the named six; probe rows B03, B05, C02 and C08 cite the recorded list."}
 ],
 "whats_right": [
  "Mixed-side and positive-first Waddell sentences flag in every comma, 'but', 'and' and 'or' form (M01 to M12, P01 to P06, X10 to X12), and the r2 and r3 positive-first blockers are closed for those forms.",
  "The D-043 allow-list silences the named clean negations as whole sentences: 'No Waddell signs.', 'Waddell signs negative.', 'Waddell testing was not done.' and 'Waddell testing was not performed.' (B01, B02, B12, B13, C01, C05, D01, D02); a clean sentence followed by a non-term sentence stays silent (C11, O16).",
  "The commit suite is green: tests/unit/test_flags_pass.py 29 passed on the live tree and on the archive; with test_flags_sample.py and test_flag_templates.py, 68 passed. The credibility template stays neutral, and every excerpt printed in the 139-row probe is a verbatim substring of its input."
 ],
 "questions_for_chris": [
  "Does a semicolon make a second clause under D-043? I read 'Anything with a second clause ... flags' and the code docstring (credibility.py:3-4) as yes. If no, F1 downgrades to minor and D-043 must say so.",
  "Is a line break a sentence boundary for the allow-list? The line-break variant (O02) is silent; the splitter treats a line break as a terminator (sentences.py:37).",
  "Should the credibility flag quote the whole sentence (F2), or the clause that matched?",
  "Should D-043 list every form the code silences, including 'No symptom magnification.' and 'Negative Waddell signs.' (F3)?"
 ]}
```
