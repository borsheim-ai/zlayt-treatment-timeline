# T-077 round 2: paralegal-reviewer (research/case-library-sources-v2.md + research/validate_library.py, commit 5c2cb2f)

**Verdict: changes.** The round-1 major is only partly closed. The denylist mechanism works: the self-test passes, and every planted mixed-case and accented variant of a listed name fails. But four real names the v2 file cites are still not on the list (Brinjikji, Nakashima, Fraser, Vera), so the file's own rule "every real name in this file is on that denylist" is still false. The self-test only checks the "X v. Y" captions, not the prose author names. Nothing in the current packets contains these names (the 7-packet scan is clean), so this is a major and not a blocker. Three round-1 minors are closed. The Hills v. Donis fix is right on the docket but misattributes the withdrawal to the newsbrief.

## Commands run and output

```
$ python3 research/validate_library.py --self-test
self-test: ok (354 planted variants caught, 16 caption names covered)        exit 0
$ python3 research/validate_library.py
identifier check: ok (7 packets, 72 denylist terms, case-insensitive)       exit 0
```

Per-name check (artifacts/review-evidence/T-077-paralegal-r2-denylist.py, output in T-077-paralegal-r2-denylist.out):

```
'Brinjikji' cited at L12   on denylist=False planted-caught=False
'Nakashima' cited at L12   on denylist=False planted-caught=False
'Fraser'    cited at L215  on denylist=False planted-caught=False
'Vera'      cited at L228 (Rodriguez-Vera) on denylist=False planted-caught=False
cited real names NOT on denylist: ['Brinjikji', 'Nakashima', 'Fraser', 'Vera']
caption names checked by self-test: [16 names, all captions only]
```

Round-1 minors:

| Round-1 item | Status | Evidence |
|---|---|---|
| Record features not tagged | Closed | All 17 patterns (P1-P17) carry "(from source)" or "(our inference)"; P4 and P17 say the source supports only the scenario theme (lines 103-104, 305-306). |
| Hills v. Donis "withdrawn and substituted" | Partly closed | Docket supports it (artifacts/review-evidence/T-077-paralegal-r2-docket.out): "Opinion withdrawn 02/11/2021", "Motion for rehearing disposed DENIED 02/11/2021", "Memorandum opinion issued AFFIRMED IN PART AND REVERSED AND RENDERED IN PART [PDF/97 KB]". Supreme Court order list of July 23, 2021 denies 21-0287 (T-077-paralegal-r2-orders.out). But line 80 says the newsbrief "describes the withdrawn 2020 opinion": the fetched page has 0 matches for "withdr" and "substitut". See F2. |
| P7 / lib12 stage not stated | Closed | Case stage line (159-160); stage/entry column (345-348). |
| P5 "six ledger columns" overstated | Closed | Lines 124-126: ledger columns derived from items 1-4 and 6; item 5 is a separate document. |
| D-042 features not in packet rows | Closed | "Must contain" table (350-361) with lib09, lib12, lib13 fixtures. |
| P6 case type, statute currency | Closed | Line 136 "health care liability claim"; statute currency line 427-430. |

## Findings

1. **major, still open: four cited real names are not on the denylist.** Brinjikji and Nakashima (line 12), Fraser (line 215) and Rodriguez-Vera's "Vera" (line 228) are real names in the file and absent from DENYLIST_V2 and the doc block. The self-test checks only caption names (see the output above), though validate_library.py:11 says "v2 doc names must all be listed".
2. **minor: the Hills newsbrief is described as saying what it does not say.** Line 80. Cite the docket for withdrawal and substitution; add the substitute opinion's own PDF link or say it is not linked.
3. **minor: firm and organisation names are not on the list.** mdjwlaw (line 80), painterfirm (line 135), FAIR Health (line 266). The denylist section says it covers "every real proper noun in this file's sources".
4. **nit: provenance dates are after the review date.** Line 4 "Researched 2026-11-01/02", line 427 "checked 2026-11-02". The commit is "Sun Nov 1 21:42:31 2026 -0600", which is 2026-11-02 in UTC, so these are probably UTC. Same pattern in research/record-formats.md lines 9 and 1073. State the timezone.

Outside my lens: whether a Texas statute or case holding is currently good law. I checked only what the doc says the sources say.

```json
{"card": "T-077", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "research/case-library-sources-v2.md and research/validate_library.py at commit 5c2cb2f (round 2); prior review reviews/T-077-paralegal.md; no app run (research card); no sample case",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-077-paralegal.md, git show --stat 5c2cb2f, research/validate_library.py (179 lines), research/case-library-sources-v2.md (435 lines, full)",
  "python3 research/validate_library.py --self-test -> 'self-test: ok (354 planted variants caught, 16 caption names covered)', exit 0",
  "python3 research/validate_library.py -> 'identifier check: ok (7 packets, 72 denylist terms, case-insensitive)', exit 0",
  "artifacts/review-evidence/T-077-paralegal-r2-denylist.py (+ .out): every real name found in the v2 file checked against DENYLIST and a planted sentence; Brinjikji, Nakashima, Fraser, Vera are not on the list and not caught; a planted packet with them passes the library scan",
  "artifacts/review-evidence/T-077-paralegal-r2-docket.out: search.txcourts.gov case 14-18-00566-CV (Opinion withdrawn 02/11/2021; rehearing denied and memorandum opinion issued 02/11/2021)",
  "artifacts/review-evidence/T-077-paralegal-r2-orders.py (+ .out): Texas Supreme Court July 23, 2021 order list denies 21-0287; date mentions in the doc (2026-11-02) checked against the commit date",
  "Fetched mdjwlaw newsbrief TIN-20200211-item1 (HTTP 200, 32,603 bytes): 0 matches for 'withdr' and 'substitut'; cites 2020 WL 206187 only",
  "Counted 'Record features' lines: 17 patterns, each tagged '(from source)' or '(our inference)'",
  "Not exercised: a fresh name-collision search; the round-1 web fetches were not repeated beyond the Hills pages; one fetch dump was written to the session scratchpad (outside the reviewer write paths, not a review artifact)"],
 "verdict": "changes",
 "scores": {"denylist_covers_cited_names": 2, "planted_name_self_test": 4, "round1_minors_closed": 3, "source_fidelity": 4, "synthetic_safety_enforcement": 3},
 "findings": [
  {"severity": "major", "title": "Denylist still omits four real names the v2 file cites; self-test checks only caption names",
   "evidence": "research/case-library-sources-v2.md:12 'Brinjikji, Nakashima'; :215 'ElGhrably I., Fraser S.G.'; :228 'Rodriguez-Vera F.J.'; rule at :24-25 says every real name in the file is on the denylist. research/validate_library.py:25-48 (DENYLIST_V2) has no Brinjikji, Nakashima, Fraser or Vera. artifacts/review-evidence/T-077-paralegal-r2-denylist.out: 'cited real names NOT on denylist: [Brinjikji, Nakashima, Fraser, Vera]'; self-test caption list has 16 names, all 'X v. Y' or 'In re' captions. validate_library.py:11 docstring says 'v2 doc names must all be listed'.",
   "why_it_matters": "The guard fails open for these four names: a packet containing 'Fraser' or 'Brinjikji' passes the identifier check, and the doc says it does not. No current packet contains them (the 7-packet scan is clean), so no real name has leaked; this is why it is a major and not a blocker. It stays open because the round-1 major was exactly this coverage gap.",
   "fix": "Add Brinjikji, Nakashima, Fraser and Vera (and Rodriguez-Vera as a unit) to DENYLIST_V2 and to the 'Denylist additions' block. Extend self_test so that author names in the doc's citations are checked against the list, not only X v. Y captions. Correct the validate_library.py docstring to say what is checked.",
   "acceptance_test": "python3 research/validate_library.py --self-test fails when 'Brinjikji' is removed from DENYLIST_V2 (it passes today); a packet containing 'Fraser S.G.' fails scan_library; the doc-versus-list check covers the prose author names."},
  {"severity": "minor", "title": "Hills v. Donis: the newsbrief is described as saying 'withdrawn', which it does not say",
   "evidence": "research/case-library-sources-v2.md:80 'The firm newsbrief https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.' Fetched page: 0 matches for 'withdr' and 'substitut'; it cites 'Hills v. Donis, No. 14-18-00566-CV, 2020 WL 206187 ... Jan. 14, 2020'. Docket supports the withdrawal (artifacts/review-evidence/T-077-paralegal-r2-docket.out: 'Opinion withdrawn 02/11/2021').",
   "why_it_matters": "This is the sentence round 1 flagged. The conclusion is now right, but a paralegal who opens the newsbrief to check the withdrawal will not find it. The 2021 substitute opinion also has no PDF link in the doc; the docket page is cited instead.",
   "fix": "Cite the docket page for the withdrawal and the substitution. Change the newsbrief sentence to 'describes the 2020 opinion (2020 WL 206187) and does not mention withdrawal'. Add the substitute opinion's own PDF link from the docket, or say it is not linked.",
   "acceptance_test": "In the P3 entry, 'withdrawn' is attributed only to the docket URL; the newsbrief sentence matches the fetched page (no 'withdr' or 'substitut' hits)."},
  {"severity": "minor", "title": "Firm and organisation names in cited URLs and text are not on the denylist",
   "evidence": "research/case-library-sources-v2.md:80 'mdjwlaw.com'; :135 'painterfirm.com/medmal/...'; :266 'FAIR Health, A Window into Utilization and Cost of Ground Ambulance Services'. None appears in DENYLIST_V2 or DENY_CAPITALISED (validate_library.py:21-53). The denylist section (:363-366) says it covers every real proper noun in the file's sources.",
   "why_it_matters": "These are firm and organisation names, not parties, so the risk is lower than for the names in F1. A packet could still carry 'Painter' or 'FAIR Health' with no flag, and the doc's own rule is broader than the list.",
   "fix": "Add mdjwlaw, Painter and FAIR Health to the denylist, or state in the doc that organisation and website names are exempt and why.",
   "acceptance_test": "The denylist block lists every firm or organisation token in the source citations, or the exemption is written in the doc."},
  {"severity": "nit", "title": "Provenance dates are after the review date and do not say which timezone",
   "evidence": "research/case-library-sources-v2.md:4 'Researched 2026-11-01/02'; :427 'CPRC 18.001/18.002 text was checked 2026-11-02'. Commit 5c2cb2f: 'Date: Sun Nov 1 21:42:31 2026 -0600'. The same date appears in research/record-formats.md:9 and :1073.",
   "why_it_matters": "The commit is 2026-11-02 in UTC, so the dates are probably UTC. A reader cannot tell which clock was used, and a statute-currency date should be unambiguous.",
   "fix": "State the timezone, or use the local date.",
   "acceptance_test": "Each date in the doc matches the commit date in the stated timezone."}
 ],
 "whats_right": [
  "All 17 'Record features' lines are tagged '(from source)' or '(our inference)', and P4 and P17 say their sources back only the scenario theme.",
  "The self-test plants 354 mixed-case and accented variants of the listed names and all are caught; lowercase 'hills' is not flagged, and 'Waddell' is allowed as an eponym.",
  "The P5 billing list now matches the opinion: four ledger columns from items 1-4 and 6, with item 5 (carrier contracts) marked as a separate document."],
 "questions_for_chris": [
  "Should cited firm websites and journal names count as 'real names' for the denylist, or only people and places? The doc says 'every real proper noun', and the answer decides F3."]}
```
