# T-077 round 3: paralegal-reviewer (research/validate_library.py + research/case-library-sources-v2.md, commit 8d7548d)

**Verdict: changes.** The round-2 major is closed for the name shapes the validator parses. Every real person and party name in the v2 doc, study authors included, is on the denylist, and the library scan passes. Two gaps remain. The self-test only extracts names in three shapes (author initials or "et al", the bracketed "already cited" list, and "X v. Y" captions), so a new name cited in author-year form or in prose passes silently. And the capitalised-only matcher misses the title-case "Fair Health", although the doc claims case-insensitive matching. Neither gap is a blocker: no current packet and no current doc name is uncovered.

## Answers to the four checks

1. **Every cited real name is denylisted.** Yes. The self-test extracts 12 author surnames, 15 citation-list names and 16 caption names, and all 43 are covered. My own independent scan of every capitalised token in the doc prose (section B) found no person or party name outside the list. The only uncovered tokens are generic words, journal and publisher titles, agencies, URL fragments and invented names (Marrowgate, Pennywhistle, both v1 examples).
2. **The self-test extracts mechanically and fails on a new name, for some shapes only.** Fails: a new author with initials (M1, `Smithers K.L.`), a new "et al" author (M3), a new caption (M5), and a new name in the bracketed "already cited" list (M6). Passes with exit 0: author-year with no initials (M2, `Smithers 2019`), prose mention (M4, `as Smithers reported`), and comma-year (M7, `Smithers, 2019`). Deleting Fraser or Brinjikji from the validator and the doc block makes the self-test exit 1 (section D), so the list itself is guarded.
3. **Planted names in a scratch packet.** Fraser and Brinjikji planted in a packet in a scratch copy of the library make the real validator entry point exit 1 (`IDENTIFIER CHECK FAIL: ... contains real identifier 'Fraser'`). Title-case `Fair Health` passes (exit 0). An uncited, unlisted `Smithers` passes, as the list-based scan is designed to.
4. **Judgment call on firm and organisation names.** Acceptable for synthetic-data safety with two conditions. A journal, publisher, agency or website domain is not a patient, provider or party identifier, and cannot be mistaken for one in a packet, so leaving those out is defensible. Firm words are different: `Painter` is a plausible invented surname, and the slug `painterfirm` implies a firm named Painter, so slug-only coverage leaves it open. Condition 1: fix the title-case FAIR Health gap (F2). Condition 2: add `Painter` as capitalised-only, as `Hills`, `Flores` and `Bai` are, and state the organisation exemption in the doc (F3).

## Commands run and output

```
$ python3 research/validate_library.py --self-test
self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)     exit 0
$ python3 research/validate_library.py
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 80 denylist terms, case-insensitive)      exit 0
$ python3 artifacts/review-evidence/T-077-paralegal-r3-names.py > artifacts/review-evidence/T-077-paralegal-r3-names.out
```

Full output: `artifacts/review-evidence/T-077-paralegal-r3-names.out`. Sections:
- A: validator extraction, all 43 names covered.
- B: independent token scan, 281 capitalised tokens, 237 not hit by the denylist scan; reviewed by hand, no uncited person or party name.
- C: self-test mutations M1 to M8 (M8 is a control).
- D: deleting `Fraser` or `Brinjikji` from list and doc block, self-test exit 1 both times.
- E: `scan_text` on probes: `'Fair Health' -> []`, `'FAIR Health' -> ['FAIR Health']`, `'Painter Law Firm' -> []`, `'painterfirm' -> ['painterfirm']`.
- F: planted packets in `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r3copy/evals/library/`, run via the real entry point.

Round-2 finding F1 (four real names missing from the list): closed. Brinjikji, Nakashima, Fraser and Vera are now in `DENYLIST_V2` (validate_library.py:53-56 region) and in the doc block (case-library-sources-v2.md:420-424).

## Findings

1. **major: the self-test extracts names only in three shapes, so a new name cited in author-year form or in prose passes.** Evidence: `artifacts/review-evidence/T-077-paralegal-r3-names.out`, section C: `M2 new author-year 'Smithers (2019)' with no initials ... exit=0  self-test: ok`; `M4 new prose mention 'as Smithers reported' ... exit=0`; `M7 new surname in comma-year cite 'Smithers, 2019' ... exit=0`. The extraction is shape-bound: `research/validate_library.py:110` (`_AUTHOR_RX`, initials or "et al" only), `:118-126` (citation list only in paragraphs containing "cited"), `:93` (captions only). The doc's rule text, case-library-sources-v2.md:24-25 ("Every real name in this file is on that denylist") and :26-27 ("--self-test extracts every author surname ..."), reads as a whole-file guarantee, which the self-test does not give. Current state is clean (section B), so this is a guard gap for future edits, not a leak. Why it matters: the next research edit that cites a study as "Smithers (2019)" or "as Smithers reported" would pass the self-test, and a packet built from it would pass the scan. Fix: either require every proper-name token in the doc (outside a fenced allow-list) to be listed or explicitly exempted, or add author-year and prose-name shapes to the extractor and fail on any unlisted capitalised token that is not in a small stop list. Acceptance test: M2, M4 and M7 in section C each exit 1 with the name reported; the baseline still exits 0.

2. **minor: "Fair Health" in title case is not caught.** Evidence: section E `'Fair Health' -> []` and section F `case_planted_fairhealth_titlecase.txt exit=0`. `research/validate_library.py:72` builds the capitalised-only matcher from `w` and `w.upper()` only, and the self-test at :155 checks the same two variants, so the test does not see the gap. The doc says matching is case-insensitive (case-library-sources-v2.md:372) and labels FAIR Health "capitalised only" (:430). Title case is the natural casing for an organisation name, so the intent is to match it. Why it matters: a payer named "Fair Health" in a packet passes the scan. Risk is low (organisation, not a person or patient), but the guard does not do what the doc says. Fix: match title case as well, e.g. `re.compile(..., re.I)` for multi-word capitalised-only terms, or add `w.title()` to the variants at :72 and :155. Acceptance test: the title-case packet in section F exits 1 and the self-test planted-variant check includes `Fair Health`.

3. **minor: firm and organisation exemptions are implicit, and "Painter" is not listed.** Evidence: case-library-sources-v2.md:137 (`painterfirm.com`), section E `'Painter Law Firm' -> []`, and section F `case_planted_painter.txt exit=0`. The doc's rule at :367-368 says the denylist covers "every real person's name and every firm-website slug or organisation name cited in this file's sources", but organisation names cited in the file are not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw, texasworker, hallapproved, natlawreview, statpearls. Slugs are listed (`mdjwlaw`, `painterfirm`), so the firm's own words ("Painter") are not. Why it matters: "Painter" is an ordinary surname that the doc's own rule 2 says to avoid as an invented name (:27-28 bans common surnames). The doc overclaims the rule text, and a reader cannot tell which organisations are exempt or why. Fix: add `Painter` as capitalised-only with the other surname-words, and state in :367-368 that publishers, journals, agencies and website domains are exempt because they are not patient, provider or party identifiers. Acceptance test: a packet with `Painter Medical Group` fails the scan; the doc sentence names the exemption.

## Scores

Not an app run, so `verify_quickly` does not apply. Scores below are for this research card.

## Outside my lens

Whether the cited opinions and studies are good law or accurately summarised. I checked only the names against the list and the validator's behaviour.

```json
{"card": "T-077", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "research/validate_library.py and research/case-library-sources-v2.md at commit 8d7548d (round 3); evals/library (7 packets) and evals/golden; no app run (research card, no sample case)",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-077-paralegal-r2.md, reviews/T-077-paralegal.md (round-1 context), my memory files for T-052 and T-077 r2",
  "git log --oneline -5; git show --stat 8d7548d (2 files: research/case-library-sources-v2.md, research/validate_library.py)",
  "Read research/validate_library.py in full (about 180 lines) and research/case-library-sources-v2.md lines 1-440 with line numbers",
  "python3 research/validate_library.py --self-test -> 'self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)', exit 0",
  "python3 research/validate_library.py -> 'identifier check: ok (7 packets, 80 denylist terms, case-insensitive)', exit 0",
  "artifacts/review-evidence/T-077-paralegal-r3-names.py (+ .out): A) validator extraction, all 43 names covered; B) independent scan of 281 capitalised doc tokens, no uncited person or party name; C) eight self-test mutations (M1-M8): M1, M3, M5, M6 fail as designed; M2, M4, M7 pass (gap); M8 control passes; D) deleting Fraser or Brinjikji from list and doc block -> self-test exit 1; E) scan_text probes; F) planted packets in a scratch copy run through the real validator: Fraser and Brinjikji exit 1, title-case Fair Health exit 0, Painter exit 0, uncited Smithers exit 0",
  "grep -n on case-library-sources-v2.md for painter, fair health, Health Affairs, Pediatrics, 'every real', 'capitalised only', 'case-insensitive'; grep -n on validate_library.py for DENY_CAPITALISED, _CAP, _AUTHOR_RX, the 'cited' paragraph test and the variant loop",
  "Not exercised: a fetch of the cited sources to check whether 'Painter' is the plaintiff firm's name; the packet-level check_golden run in the scratch copy was run only through the validator's main() entry point"],
 "verdict": "changes",
 "scores": {"denylist_covers_cited_names": 4, "self_test_mechanical_extraction": 3, "planted_name_fails_scan": 4, "firm_org_judgment": 3, "synthetic_safety_enforcement": 3},
 "findings": [
  {"severity": "major", "title": "Self-test extracts names in three shapes only; author-year and prose-cited names pass silently",
   "evidence": "artifacts/review-evidence/T-077-paralegal-r3-names.out section C: 'M2 new author-year 'Smithers (2019)' with no initials ... exit=0  self-test: ok'; 'M4 new prose mention 'as Smithers reported' ... exit=0'; 'M7 new surname in comma-year cite 'Smithers, 2019' ... exit=0'. Extraction: research/validate_library.py:110 (_AUTHOR_RX, initials or et al), :118-126 (citation list, only paragraphs containing 'cited'), :93 (captions). Doc rule: research/case-library-sources-v2.md:24-25 'Every real name in this file is on that denylist'; :26-27 '--self-test extracts every author surname ...'.",
   "why_it_matters": "The doc states a whole-file guarantee that the self-test does not enforce. Current state is clean: an independent scan of every capitalised token in the doc prose (section B) finds no cited person or party name outside the list, so no real identifier is in the packets. The exposure is the next research edit that cites a study as 'Smithers (2019)' or names an author in prose, which would pass the self-test and any packet built from it would pass the scan. Synthetic-data safety depends on this guard, so it is a major and not a minor. It is not a blocker because nothing leaks today.",
   "fix": "Either (a) require every proper-name token in the doc prose to be listed or on an explicit exemption list, failing on any unlisted capitalised token not in a short stop list; or (b) add author-year ('Name (2019)', 'Name, 2019') and prose-name shapes to the extractor. State the scope of the self-test in the doc rule text at :24-27.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-077-paralegal-r3-names.py: M2, M4 and M7 each exit 1 and name the surname; baseline self-test still exits 0; the independent scan (section B) still shows no uncovered person or party name."},
  {"severity": "minor", "title": "Title-case 'Fair Health' passes the capitalised-only matcher",
   "evidence": "artifacts/review-evidence/T-077-paralegal-r3-names.out section E: 'Fair Health' -> []; 'FAIR Health' -> ['FAIR Health']; section F: case_planted_fairhealth_titlecase.txt exit=0. research/validate_library.py:72 (_CAP built from w and w.upper() only) and :155 (self-test variants (w, w.upper())). Doc :372 'Matching is case-insensitive'; :430 'FAIR Health  # capitalised only (organisation)'.",
   "why_it_matters": "The doc says matching is case-insensitive and the term is meant to match when capitalised. Title case is the natural casing for an organisation name, so the guard misses the most likely form. The self-test has the same blind spot, so it reports ok. Risk is low (organisation, not a person or patient), but the guard does not do what the doc says.",
   "fix": "Match title case as well as UPPER for capitalised-only terms (add w.title() to the variants at :72 and :155, or match case-insensitively with a word-boundary and a capital first letter).",
   "acceptance_test": "Planting 'Fair Health' in a packet makes the validator exit 1 (section F row fails); the self-test planted-variant check includes w.title()."},
  {"severity": "minor", "title": "Firm and organisation exemptions are implicit; 'Painter' is not listed while its slug is",
   "evidence": "research/case-library-sources-v2.md:137 'painterfirm.com/medmal/...'; :426 'painterfirm' listed; :367-368 'every real person's name and every firm-website slug or organisation name cited in this file's sources'. Organisation names cited but not listed: Health Affairs (:255), Pediatrics and AHRQ (:186), PubMed, Legal500, Casemine, FindLaw (:136 and :283), texasworker (:189), natlawreview (:243). Probes: section E 'Painter Law Firm' -> []; section F case_planted_painter.txt exit=0.",
   "why_it_matters": "Slugs are listed but the firm's own words are not, and the doc's rule text says every organisation name is covered. The judgment call is acceptable for synthetic-data safety: publishers, journals, agencies and website domains are not patient, provider or party identifiers, and a packet is unlikely to carry them as a person. Firm words are a different case, because 'Painter' is an ordinary surname the doc's own rule 2 (:27-28) bans as an invented name. A reader cannot tell which organisations are exempt or why.",
   "fix": "Add 'Painter' as capitalised-only (like Hills, Flores and Bai). Rewrite :367-368 to name the exemption: publishers, journals, agencies and website domains are exempt because they are not patient, provider or party identifiers; firm and payer names are listed.",
   "acceptance_test": "A packet with 'Painter Medical Group' fails the validator; the doc's denylist section states the organisation exemption in one sentence."}
 ],
 "whats_right": [
  "Every author surname the validator extracts (Airan-Javia, Anderson, Bai, Castro, ElGhrably, Fishbain, Flores, Fraser, Kantrowitz, Powell, Rodríguez-Vera, Steinkamp) and the opening-list names (Haygood, Brinjikji, Nakashima) are on DENYLIST_V2 and the doc block; my independent token scan found no uncited person or party name.",
  "Deleting Fraser or Brinjikji from the list and doc block makes the self-test exit 1, and planted Fraser or Brinjikji packets make the real validator exit 1 (artifacts/review-evidence/T-077-paralegal-r3-names.out sections D and F).",
  "The validator's list and the doc's denylist block stay in sync (the self-test fails on drift in either direction), and the validator docstring at :1-11 states the self-test's shapes accurately."],
 "questions_for_chris": [
  "Is 'Waddell' (the eponym in the cited Fishbain title, used in packets as 'Waddell 3/5') an acceptable exception to 'every real person's name' in :367? The validator allows it on purpose (ALLOWED_EPONYMS); I did not object to the choice, I am asking you to confirm it.",
  "Should publisher, journal, agency and website names (Health Affairs, Pediatrics, AHRQ, PubMed, Legal500) be listed or exempt in writing? My recommendation is written exemption (F3)."]}
```
