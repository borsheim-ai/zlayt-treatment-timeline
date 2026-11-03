# Subagent: Researcher: T-077 r3 denylist (Researcher: T-077 r3 denylist)

Source: `agent-a7e2441a9a8b89b8e.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:50:45.158Z

You own board card T-077, round 3 (claimed by "researcher") in /Users/arsis/zlayt-pm-project. Read reviews/T-077-paralegal-r2.md.

Every real person's name cited anywhere in research/case-library-sources-v2.md must be on the denylist in research/validate_library.py, including study authors (Brinjikji, Nakashima, Fraser, Vera) and not just case captions. Do it mechanically:
1. Extract every capitalised surname appearing in citations or source lines of the doc into the denylist.
2. Make the self-test check that every name in the doc's citations is on the denylist, so a newly cited name fails the test until it's added.
3. Plant a study-author name in a scratch packet and show that validation fails.

Run the self-test and `python3 research/validate_library.py` against evals/library. Commit with `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `python3 tools/board.py ac`, the handoff, and `move T-077 in_review --agent researcher`. Reply in 1 line.

### User / tool · 2026-11-02T03:50:45.161Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:48.617Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Read card T-077, review r2, and agent memory",
   "status": "in_progress"
  },
  {
   "content": "Extract name list from case-library-sources-v2.md into denylist",
   "status": "pending"
  },
  {
   "content": "Add self-test that fails on uncited-denylist names",
   "status": "pending"
  },
  {
   "content": "Plant study-author name in scratch packet, confirm failure",
   "status": "pending"
  },
  {
   "content": "Run self-test and validate_library against evals/library",
   "status": "pending"
  },
  {
   "content": "Commit, ac, handoff, move in_review",
   "status": "pending"
  }
 ],
 "scope": "first_task"
}
````

### User / tool · 2026-11-02T03:50:48.620Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:49.344Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-077 && echo ---- && cat reviews/T-077-paralegal-r2.md && echo ---- && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/research-workflow-pitfalls.md && echo ---- && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/record-formats-key-traps.md",
 "description": "Show card, review, and agent memory notes"
}
````

### User / tool · 2026-11-02T03:50:49.488Z

**tool result**
````
---
id: "T-077"
title: "Research: real-world PI case patterns for the multi-case library (v2)"
milestone: "M3"
role: "researcher"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:04Z"
updated_at: "2026-11-02T03:50:41Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T03:50:41Z"
rounds: 2
commits: ["bb26bf0", "5c2cb2f"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-077-paralegal.md", "at": "2026-11-02T03:27:07Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-077-paralegal-r2.md", "at": "2026-11-02T03:50:41Z"}
ac:
  - {"n": 1, "text": "research/case-library-sources-v2.md lists >= 12 case patterns from public real-world sources (court opinions, verdict reports, bar/CLE materials, published studies) with URL, date and the record features each implies (gaps, priors, causation language, billing shape, language)", "done": true, "evidence": "r2 (5c2cb2f): 17 patterns; every Record-features line tagged (from source)/(our inference); Hills v. Donis re-cited to the 2021-02-11 substitute mem. op. (read in full via search.txcourts.gov docket), pet. denied 2021-07-23; P17 source replaced by Castro 1997 PMID 9455663 (Hampton not retrievable); P4/P17 marked theme-only; P5 items 1-4,6 vs 5; P6 case type; statute currency line"}
  - {"n": 2, "text": "Each pattern names which product feature it exercises (D-042 list) and is marked synthetic-safe (no real names, dates shifted)", "done": true, "evidence": "r2 (5c2cb2f): Denylist additions block (46 terms) mirrored in research/validate_library.py DENYLIST_V2/DENY_CAPITALISED, case+accent-insensitive; 'python3 research/validate_library.py --self-test' -> ok (354 planted variants caught, 16 caption names covered); negative test (Garza removed) fails; library scan ok (7 packets, 72 terms); packet table has stage/entry, must-contain and record-formats § columns for lib08-lib15"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T03:11:11Z researcher: claimed
- 2026-11-02T03:15:00Z researcher: Searched/opened ~18 public sources (TX Sup Ct JLG 2015 + Central Oregon 2022 full text; NJ Rodriguez v Wal-Mart 2019 syllabus; Hills v Donis, Chiv v Figueroa, Gunn v McCoy, Steinkamp 2022, Flores 2003, Powell 2008, ElGhrably 2008, Rodriguez-Vera 2002, Bai&Anderson 2015, Fishbain 2003, FAIR Health, defense verdict 2024). Writing research/case-library-sources-v2.md.
- 2026-11-02T03:16:57Z researcher: AC 1 checked: research/case-library-sources-v2.md: 17 patterns (P1-P17), each with URL, source date, read depth, 2-3 line summary and record features; none reuses v1 scenarios or sources (commit bb26bf0)
- 2026-11-02T03:16:57Z researcher: AC 2 checked: Each pattern has a 'D-042 / flags' line and a 'Synthetic-safety' line; global rules section (no real names, dates shifted to 2025-2027, facts recombined) + coverage map + 8 recombined packet proposals (lib08-lib15)
- 2026-11-02T03:16:57Z researcher: moved in_progress -> in_review
- 2026-11-02T03:17:12Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T03:17:12Z orchestrator: Review batched with T-078 once it lands.
- 2026-11-02T03:27:07Z orchestrator: review paralegal-reviewer (claude-sonnet-5-5): changes — reviews/T-077-paralegal.md; round 1; findings:
    - [major] Denylist for v2 real names is not in place, and the doc's list is incomplete and unsafe as written — fix: Researcher adds an explicit 'Denylist additions' block to the v2 doc and updates validate_library.py (case-insensitive) before T-079 starts. Include distinctive tokens: JLG, Pechero, Zapata, Guevara, Ferrer, Donis, Chiv, Figueroa, Broussard, 'Central Oregon', McCoy, Miskell, Wal-
    - [minor] 'Record features' mix source-derived and inferred content, and two sources do not support the record shape at all — fix: Tag each Record-features line 'from source' or 'our inference'. Give Hampton a full citation (court, district, docket or WL cite) or replace it with a retrievable source. Say plainly that P4 and P17 support only the scenario theme.
    - [minor] Hills v. Donis 'withdrawn and substituted 2021-02-11' is not supported by the cited page — fix: Either cite the substituted opinion with its own date and URL, or delete the sentence. Re-read the opinion itself, since the doc admits it was not opened.
    - [minor] P7/lib12 (defense IME) and P16 assume documents a demand-stage packet usually does not contain — fix: Label lib12 as litigation-stage, or recast it as a carrier records-review/peer-review letter or a treating-provider FCE note. Say in lib13 that the PCP note arrived from a records request.
    - [minor] P5 claim that provider ledgers 'match the six categories exactly' overstates the opinion — fix: Reword to 'ledger columns derived from items 1-4 and 6; item 5 (carrier contracts) is a separate document the packet may reference but not reproduce'.
    - [minor] Three D-042 features are credited to packets whose premises do not carry them — fix: Add a 'must contain' column to the packet table, e.g. lib09: one form dated 03/06/2026 day-first plus 14/05/2026; lib12: at least 4 credibility sentences (2 clean, 2 mixed) across 3 dates; lib13: a surgical estimate line.
- 2026-11-02T03:27:07Z researcher: claimed
- 2026-11-02T03:29:33Z researcher: Round 2 started: denylist (case-insensitive + self-test), record-feature tags, Hills/Hampton citations, stage + must-contain + formats columns, P5/P6 rewording.
- 2026-11-02T03:42:48Z researcher: AC 1 checked: r2 (5c2cb2f): 17 patterns; every Record-features line tagged (from source)/(our inference); Hills v. Donis re-cited to the 2021-02-11 substitute mem. op. (read in full via search.txcourts.gov docket), pet. denied 2021-07-23; P17 source replaced by Castro 1997 PMID 9455663 (Hampton not retrievable); P4/P17 marked theme-only; P5 items 1-4,6 vs 5; P6 case type; statute currency line
- 2026-11-02T03:42:48Z researcher: AC 2 checked: r2 (5c2cb2f): Denylist additions block (46 terms) mirrored in research/validate_library.py DENYLIST_V2/DENY_CAPITALISED, case+accent-insensitive; 'python3 research/validate_library.py --self-test' -> ok (354 planted variants caught, 16 caption names covered); negative test (Garza removed) fails; library scan ok (7 packets, 72 terms); packet table has stage/entry, must-contain and record-formats § columns for lib08-lib15
- 2026-11-02T03:43:00Z researcher: moved in_progress -> in_review
- 2026-11-02T03:43:08Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T03:50:41Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-077-paralegal-r2.md; round 2; findings:
    - [major] Denylist still omits four real names the v2 file cites; self-test checks only caption names — fix: Add Brinjikji, Nakashima, Fraser and Vera (and Rodriguez-Vera as a unit) to DENYLIST_V2 and to the 'Denylist additions' block. Extend self_test so that author names in the doc's citations are checked against the list, not only X v. Y captions. Correct the validate_library.py docstring t
    - [minor] Hills v. Donis: the newsbrief is described as saying 'withdrawn', which it does not say — fix: Cite the docket page for the withdrawal and the substitution. Change the newsbrief sentence to 'describes the 2020 opinion (2020 WL 206187) and does not mention withdrawal'. Add the substitute opinion's own PDF link from the docket, or say it is not linked.
    - [minor] Firm and organisation names in cited URLs and text are not on the denylist — fix: Add mdjwlaw, Painter and FAIR Health to the denylist, or state in the doc that organisation and website names are exempt and why.
- 2026-11-02T03:50:41Z researcher: claimed

## Handoff
What changed (r2, 5c2cb2f): research/validate_library.py denylist now holds every real v2 name (case- and accent-insensitive; Hills/Flores/Bai capitalised-only; Waddell allowed as eponym) plus --self-test; v2 doc gains a Denylist additions block, tagged Record features, Hills v. Donis re-cited to the 2021 substitute opinion, P17 source swapped to Castro 1997 (Hampton had no retrievable cite), P5/P6 rewording, stage/entry + must-contain + formats columns; lib12 recast as a pre-suit carrier records review (renamed lib12_records_review_credibility; TRCP 204 exam as litigation variant). · How verified: python3 research/validate_library.py --self-test -> ok (354 planted variants, 16 caption names); negative test with Garza removed fails; python3 research/validate_library.py -> ok (7 packets, 72 terms). · What's left: T-079 should use the new lib12 id and the must-contain table; state names stay banned, so packets write TX. · What surprised me: the 2020 Hills opinion the firm write-up described was withdrawn; the 2021 substitute affirmed one plaintiff's ankle award on lay testimony.

----
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
----
---
name: research-workflow-pitfalls
description: Researcher tooling pitfalls in this repo: git-guard needs add/commit as separate commands; PDFs via curl+pdftotext; Texas court/statute retrieval; denylist + self-check rule; source-marking convention
metadata:
  type: feedback
---

Stage and commit in **separate Bash calls** (`git add <path>` then `git commit -m ... -- <path>`); git-guard blocks a combined command so the secret scan sees the staged set.
**Why:** hook rejected `git add && git commit` on T-078.
**How to apply:** every commit of research/ or personas/.

WebFetch returns "binary PDF" for PDF URLs but saves the file under the tool-results dir; copy it into a fresh scratchpad subdir and run `pdftotext -layout` (at /opt/homebrew/bin) to read official manuals (NUCC 1500, Medicaid UB-04 guides worked this way).
**Why:** primary-source manuals (NUCC, NUBC, CMS) are PDFs; the search summary alone is weaker evidence.
**How to apply:** prefer extracting the primary PDF over citing a search snippet.

Source convention in research/*.md (since T-052, kept in T-078): each source line says **opened** vs "search summary" vs "not opened", and facts from prior knowledge are listed under Assumptions. Specimens use invented names, `SYN-` identifiers, 555-01xx phones, and a SYNTHETIC header. See [[record-formats-key-traps]].

Texas sources: opinion PDFs come from the docket page `https://search.txcourts.gov/Case.aspx?cn=<No>&coa=coa<NN>` (WebFetch lists event links; `curl -L` the SearchMedia URL, then pdftotext). It shows withdrawn/substitute opinions a firm write-up hides (Hills v. Donis: 2020 op withdrawn, 2021-02-11 substitute). statutes.capitol.texas.gov is a JS app: use the texas.public.law mirror (fetch tool caps quotes at 125 chars). CourtListener API needs auth. git-guard also rejects Bash commands containing backslash-escaped backticks: write a script file instead.
**Why:** T-077/T-078 round 2 lost time on 403s and a superseded opinion.
**How to apply:** verify every case date/history on the docket before citing; give court, district and docket/reporter in every caption or drop the source.

Any real name cited in research/case-library-sources*.md must be on the DENYLIST in research/validate_library.py in the same commit, and the doc carries a "## Denylist additions" text block that `--self-test` cross-checks (planted mixed-case names must fail; every "X v. Y" caption token must be listed). Specimens in record-formats.md must pass scan_text too (state written as "TX").
**Why:** T-077 review major: doc said "add names before packets are built" but nothing enforced it.
**How to apply:** run `python3 research/validate_library.py --self-test` and `python3 research/record_formats_check.py` before handing off research cards.
----
---
name: record-formats-key-traps
description: Highest-value extraction traps found in T-078 record-format research (CMS-1500 implied decimal, UB-04 0001 total and FL44 rate, non-service dates) for packet generation and lexicon work
metadata:
  type: project
---

research/record-formats.md (T-078, 2026-11-02) is the reference for synthetic packet formats under D-042. Traps worth reusing in evals/reviews:
- CMS-1500 24F/28 amounts print with no decimal point (`150 | 00`), so OCR gives 15000; 24A From/To + 24G units = several days on one line; Item 14 = injury date, Item 31 = signature date.
- UB-04: line 23 rev code 0001 is the total (do not sum it); FL 44 holds a per-day rate on room lines next to the FL 47 charge (D-042 rate-vs-charge guard).
- One ED visit = facility UB-04 + ED physician 1500 + radiologist 1500 (not duplicates); EOB "amount billed" restates the bill (double count risk).
- Spanish notes: day-first dates; `ago` = agosto; `refiere`/`niega` carry voice/negation.
**Why:** these drive realistic adversarial packets and reviewer checks.
- Round 2 (2026-11-02) added §15-20 (EMS report, ambulance invoice with fractional mileage x rate, CPRC 18.001 affidavit + cover page, narrative letter, office note, records-review/IME), a decimal-less OCR 1500, an inpatient UB-04 room-rate line, §22 cross-specimen table (fixed vs DELIBERATE), and research/record_formats_check.py.
- Occurrence codes 01-06 are all accident codes (not just 01); 1500 grouping only on consecutive days with days = units; PT units must follow a stated 8-minute method.
**How to apply:** when building library cases, lexicon entries, or reviewing billing/OCR cards, start from §1, §21 and §22 of that file. Unverified items are in §23.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:53.979Z

**tool call — Bash**
````
{
 "command": "cat -n research/validate_library.py && echo ---- && git status --short research/ evals/library 2>/dev/null | head -30 && echo ---- && git log --oneline -5 -- research/ && ls evals/library 2>/dev/null | head -50",
 "description": "Read validator script and check git and library state"
}
````

### User / tool · 2026-11-02T03:50:54.120Z

**tool result**
````
     1	#!/usr/bin/env python3
     2	"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).
     3	
     4	check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
     5	runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
     6	cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
     7	doctors named in opinions, firms, counties, cities, highways and study authors. Matching is case-insensitive and
     8	accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.
     9	
    10	Run:        python3 research/validate_library.py
    11	Self-test:  python3 research/validate_library.py --self-test   (planted names must fail; v2 doc names must all be listed)
    12	"""
    13	import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata
    14	
    15	ROOT = pathlib.Path(__file__).resolve().parents[1]
    16	LIB = ROOT / "evals" / "library"
    17	V2_DOC = ROOT / "research" / "case-library-sources-v2.md"
    18	
    19	# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the
    20	# two-letter abbreviation (e.g. "TX") where a state must appear.
    21	DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
    22	               "Rissman", "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia",
    23	               "Oklahoma", "Texas", "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]
    24	# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
    25	DENYLIST_V2 = [
    26	    # P1 JLG Trucking v. Garza
    27	    "JLG", "Garza", "Pechero", "Zapata",
    28	    # P2 Guevara v. Ferrer
    29	    "Guevara", "Ferrer",
    30	    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)
    31	    "Donis", "Matamoros", "Castellanos", "Morehouse", "Reuben", "Rueben", "Poissant", "I-45",
    32	    # P4 Chiv v. Figueroa
    33	    "Chiv", "Figueroa",
    34	    # P5 In re Central Oregon Truck Co.
    35	    "Central Oregon", "Oregon", "Broussard",
    36	    # P6 Gunn v. McCoy
    37	    "Gunn", "McCoy",
    38	    # P7 Rodriguez v. Wal-Mart Stores
    39	    "Rodriguez", "Wal-Mart", "Walmart",
    40	    # P16 defense-firm write-up
    41	    "Lewis Brisbois", "Brisbois", "Harris County",
    42	    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.
    43	    "Hampton", "Miskell", "Baratta", "I-635", "Castro", "Schilgen",
    44	    # Study authors cited in v2
    45	    "Steinkamp", "Kantrowitz", "Airan-Javia", "ElGhrably", "Fishbain", "Powell", "Anderson",
    46	    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions
    47	    "Houston", "Dallas", "Allstate",
    48	]
    49	# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so "rolling hills" or
    50	# "flores" (Spanish for flowers) in a packet still passes while "Hills" / "FLORES" as a name fails.
    51	DENY_CAPITALISED = ["Hills", "Flores", "Bai"]
    52	# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.
    53	ALLOWED_EPONYMS = ["Waddell"]
    54	DENYLIST = DENYLIST_V1 + DENYLIST_V2
    55	BANNER = "SYNTHETIC — invented for evaluation; not real patient data\n"
    56	
    57	
    58	def fold(s):
    59	    """Strip accents so 'Rodríguez' matches 'Rodriguez'."""
    60	    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    61	
    62	
    63	_ANY = [(w, re.compile(r"(?<!\w)" + re.escape(fold(w)) + r"(?!\w)", re.I)) for w in DENYLIST]
    64	_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]
    65	
    66	
    67	def scan_text(text):
    68	    """Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital)."""
    69	    t = fold(text)
    70	    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]
    71	
    72	
    73	def doc_denylist_block(doc_text):
    74	    """Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed)."""
    75	    m = re.search(r"## Denylist additions.*?```text\n(.*?)```", doc_text, re.S)
    76	    if not m:
    77	        return None
    78	    return [ln.split("#")[0].strip() for ln in m.group(1).splitlines() if ln.split("#")[0].strip()]
    79	
    80	
    81	_GENERIC = {"In", "re", "Inc", "Inc.", "LLC", "LLC,", "Co", "Co.", "Stores", "Stores,", "Truck", "Trucking", "Trucking,", "The",
    82	            "of", "and", "Tex", "Tex.", "App", "App.", "No", "No."}
    83	
    84	
    85	def doc_caption_names(doc_text):
    86	    """Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc."""
    87	    names = set()
    88	    for a, b in re.findall(r"([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*) v\. ([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*)", doc_text):
    89	        for side in (a, b):
    90	            for tok in re.split(r"[ ,]+", side):
    91	                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):
    92	                    names.add(tok.rstrip(".,"))
    93	    for x in re.findall(r"In re ([A-Z][\w'-]*(?: [A-Z][\w'-]*)*)", doc_text):
    94	        toks = [t for t in x.split() if t not in _GENERIC]
    95	        if toks:
    96	            names.add(" ".join(toks[:2]))
    97	    return names
    98	
    99	
   100	def self_test():
   101	    fails = []
   102	    for w in DENYLIST:
   103	        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:
   104	            if w not in scan_text(f"Seen by Dr. {variant} at the clinic."):
   105	                fails.append(f"planted {variant!r} not caught")
   106	    for w in DENY_CAPITALISED:
   107	        for variant in (w, w.upper()):
   108	            if w not in scan_text(f"Referred by {variant} Family Clinic."):
   109	                fails.append(f"planted {variant!r} not caught")
   110	        if scan_text(f"walked up the {w.lower()} near home"):
   111	            fails.append(f"lowercase common word {w.lower()!r} wrongly flagged")
   112	    if not scan_text("Patient: Ana Rodríguez (SYNTHETIC)"):
   113	        fails.append("accented Rodríguez not caught")
   114	    for w in ALLOWED_EPONYMS:
   115	        if scan_text(f"{w} signs 0/5 today."):
   116	            fails.append(f"eponym {w!r} wrongly flagged")
   117	    doc = V2_DOC.read_text()
   118	    block = doc_denylist_block(doc)
   119	    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}
   120	    if block is None:
   121	        fails.append("v2 doc has no '## Denylist additions' ```text block")
   122	    else:
   123	        for w in block:
   124	            if fold(w).lower() not in listed:
   125	                fails.append(f"v2 doc denylist term {w!r} missing from validate_library.py")
   126	        for w in DENYLIST_V2 + DENY_CAPITALISED:
   127	            if w not in block:
   128	                fails.append(f"validate_library.py term {w!r} missing from the v2 doc block")
   129	    for name in sorted(doc_caption_names(doc)):
   130	        if not any(fold(part).lower() in listed for part in [name] + name.split()):
   131	            fails.append(f"v2 caption name {name!r} not on the denylist")
   132	    # End-to-end: a planted packet must make the library scan fail.
   133	    with tempfile.TemporaryDirectory() as tmp:
   134	        p = pathlib.Path(tmp) / "case_planted.txt"
   135	        p.write_text(BANNER + "Patient seen by DR. GARZA after the crash on i-45.\n")
   136	        if not scan_library([p]):
   137	            fails.append("planted packet passed the library scan")
   138	    for f in fails:
   139	        print("SELF-TEST FAIL:", f)
   140	    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3
   141	    print("self-test:", "FAIL" if fails else f"ok ({n} planted variants caught, {len(doc_caption_names(doc))} caption names covered)")
   142	    return 1 if fails else 0
   143	
   144	
   145	def scan_library(files):
   146	    bad = []
   147	    for f in files:
   148	        t = f.read_text()
   149	        for w in scan_text(t):
   150	            bad.append(f"{f.name}: contains real identifier {w!r}")
   151	        if f.suffix == ".txt" and not t.startswith(BANNER):
   152	            bad.append(f"{f.name}: missing SYNTHETIC header")
   153	    return bad
   154	
   155	
   156	def main():
   157	    if "--self-test" in sys.argv:
   158	        return self_test()
   159	    cases = sorted(LIB.glob("case_*.expected.json"))
   160	    if len(cases) < 6:
   161	        print(f"FAIL: need >= 6 library cases, found {len(cases)}")
   162	        return 1
   163	    with tempfile.TemporaryDirectory() as tmp:
   164	        d = pathlib.Path(tmp) / "golden"
   165	        shutil.copytree(ROOT / "evals" / "golden", d)
   166	        for f in LIB.glob("case_*"):
   167	            shutil.copy(f, d / f.name)
   168	        r = subprocess.run([sys.executable, str(d / "check_golden.py")], capture_output=True, text=True, cwd=d)
   169	    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])
   170	    bad = scan_library(sorted(LIB.glob("case_*")))
   171	    for b in bad:
   172	        print("IDENTIFIER CHECK FAIL:", b)
   173	    terms = len(DENYLIST) + len(DENY_CAPITALISED)
   174	    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)")
   175	    return 1 if (r.returncode or bad) else 0
   176	
   177	
   178	if __name__ == "__main__":
   179	    sys.exit(main())
----
----
327ce46 fix(research): record formats r2 - NUCC-consistent 1500, OCR and room-rate specimens, six new formats (T-078 r2)
5c2cb2f fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
1193f8a docs(research): record and billing document formats for synthetic packets (T-078)
bb26bf0 docs(research): case library v2 real-world PI patterns (T-077)
9d6756e fix(evals): drop patient_report source_kind from golden checker, goldens and library builder (D-040, T-071 r2)
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:56.291Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '1,120p'",
 "description": "Read first 120 lines of v2 source doc"
}
````

### User / tool · 2026-11-02T03:50:56.375Z

**tool result**
````
     1	# Case library sources v2 (T-077)
     2	
     3	Seventeen real-world personal-injury record patterns from public sources, for the next round of fully synthetic packets in
     4	`evals/library/` (after `case_lib01`–`case_lib07`, see `research/case-library-sources.md`). Researched 2026-11-01/02 by the
     5	researcher agent. Feature names follow D-042 (`memory/ORCHESTRATOR_DECISIONS.md`) plus the base flag types (D-013) and the
     6	credibility rule (D-043).
     7	
     8	**No duplication with v1.** v1 covered: ER visit then a long gap; slip-and-fall onto a previously operated knee; chiropractic
     9	volume on a truck rear-end; facial dog bite and scar revision; pedestrian ORIF and hardware removal; LOP billed-vs-adjusted
    10	(Haygood line); missing out-of-state records. None of the patterns below reuses those scenarios or v1's sources. Sources
    11	already cited in `research/texas-pi-notes.md` and `research/adjuster-attacks.md` (Haygood, In re Allstate, K&L Auto Crushers,
    12	Brinjikji, Nakashima) are not used as primary sources here.
    13	
    14	**Read depth (stated honestly).** "Full text" means the opinion or abstract itself was fetched and read. "Summary" means only
    15	a secondary write-up or search excerpt was seen. Verify a summary-level source against the original before quoting it
    16	outside this repo. Court opinions are authority for what the court said; firm write-ups and press are one side's account.
    17	Medical studies describe record quality in general, not PI records specifically; the PI framing is ours.
    18	
    19	## Synthetic-safety rules (apply to every pattern)
    20	
    21	1. **Pattern, not facts.** We take the shape of the record (what kind of page, which wording, which billing columns, where
    22	   the gap falls) and nothing else. No party, provider, clinic, county, road, date, amount or diagnosis code is copied.
    23	2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
    24	   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
    25	   that denylist (see "Denylist additions" below; matching is case- and accent-insensitive), and
    26	   `python3 research/validate_library.py --self-test` proves a planted name fails. Common surnames that appear here
    27	   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
    28	   including in the Spanish-language packets: pick distinctive invented surnames instead.
    29	3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. "second event
    30	   about 12 weeks after the first"). Real dates in this file are citation dates for the source, not record dates.
    31	4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.
    32	5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.
    33	6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose
    34	   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.
    35	
    36	## Patterns
    37	
    38	### P1. Intervening second accident between first care and the key imaging
    39	- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
    40	  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).
    41	- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a
    42	  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after
    43	  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its
    44	  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.
    45	- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance
    46	  transport in a hard collar after event 2; first MRI dated after event 2; a treating note whose history omits event 2;
    47	  multi-year span ending in fusion.
    48	- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with
    49	  neck complaints; a surgeon's narrative "history" that attributes everything to event 1.
    50	- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/
    51	  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show "two incidents found: human
    52	  decides relevance" as a HITL step. The tool never apportions.
    53	- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region
    54	  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.
    55	
    56	### P2. Immediate care is common-knowledge; later complex care needs an expert
    57	- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —
    58	  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary
    59	  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view
    60	  (summary only).
    61	- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.
    62	  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but
    63	  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each
    64	  was caused by the accident.
    65	- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total
    66	  expenses in an elderly patient.
    67	- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes
    68	  with no causation statement; one itemized hospital bill spanning both phases; comorbidities in the problem list.
    69	- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as "no causation
    70	  language found", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited
    71	  per line); calibrated confidence must not imply causation strength.
    72	- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.
    73	
    74	### P3. Billing affidavits and records are not causation; conclusory physician letter
    75	- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute
    76	  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full
    77	  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11
    78	  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
    79	  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief
    80	  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.
    81	- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards
    82	  for three plaintiffs were reversed and rendered: §18.001 affidavits prove reasonableness of charges, not causation, and
    83	  a treating doctor's letters (and causation statements inside billing records) were conclusory because they gave no
    84	  explanation of how and why the crash caused the diagnoses. The award for a fourth plaintiff's ankle injury, and her
    85	  child's single visit, was affirmed on lay testimony and temporal proximity (Guevara).
    86	- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;
    87	  causation statements embedded in billing records; long diagnosis lists (radiculitis, disc displacement, discogenic pain)
    88	  on the bills; one plaintiff's single-visit bill (evaluation plus hot/cold pack).
    89	- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;
    90	  the same diagnosis lines repeated on every bill.
    91	- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);
    92	  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must
    93	  reject any summary that turns "the accident caused" into a fact; record_warning for non-clinical pages.
    94	- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused; no
    95	  highway, county or party name from the opinion.
    96	
    97	### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight
    98	- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —
    99	  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).
   100	- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified
   101	  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the
   102	  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.
   103	- **Scope of support:** this source supports only the scenario theme (Spanish-speaking party, translation and
   104	  counteraffidavit disputes). The opinion says nothing about how records are charted.
   105	- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line
   106	  such as "history via interpreter" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.
   107	- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled
   108	  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not
   109	  resolved).
   110	- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.
   111	
   112	### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request
   113	- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —
   114	  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).
   115	- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two
   116	  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems
   117	  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to
   118	  proportionality). The billing discovery listed six items: (1) total billed charges, (2) adjustments or write-offs,
   119	  (3) amount paid to the provider and by whom, (4) outstanding balances, (5) copies of contracts with the health-insurance
   120	  carrier, (6) any letters of protection, contracts, liens or other guarantees.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:57.768Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '120,280p'",
 "description": "Read lines 120-280 of v2 source doc"
}
````

### User / tool · 2026-11-02T03:50:57.854Z

**tool result**
````
   120	  carrier, (6) any letters of protection, contracts, liens or other guarantees.
   121	- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;
   122	  the six billing-discovery items above.
   123	- **Record features (our inference):** intake forms answering "prior accidents: none" vs older notes that mention them; a
   124	  neuro or neuropsych note with memory complaints; ledger columns derived from items 1-4 and 6 (billed, adjusted, paid,
   125	  payer, balance, LOP/lien). Item 5 (carrier contracts) is a separate document a packet may reference but never reproduce
   126	  as a ledger column.
   127	- **D-042 / flags:** billing analysis (ledger columns from items 1-4 and 6, each cited; totals by code); pre_existing (prior accidents); conflict
   128	  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
   129	- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment
   130	  facts omitted; ledger numbers invented.
   131	
   132	### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share
   133	- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the
   134	  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
   135	  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
   136	- **Summary:** In a health care liability claim (medical malpractice, not a crash case), the plaintiff replaced provider
   137	  billing affidavits with affidavits from health insurers' subrogation agents stating amounts actually paid; the court held
   138	  §18.001 does not limit affiants to providers or their custodians.
   139	- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.
   140	- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
   141	  "not covered" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;
   142	  the affidavit page itself.
   143	- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and
   144	  flags mismatches); charge reclassification guard (an "allowed amount" is not a charge); dedupe of the same service across
   145	  two documents.
   146	- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.
   147	
   148	### P7. Pain out of proportion, "somatization", "symptom magnification" in the exam note
   149	- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —
   150	  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).
   151	- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain
   152	  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used
   153	  "somatization" and "symptom magnification". The court held such terms are admissible case by case, distinguished them from
   154	  "malingering", and upheld admission of unrelated past medical history.
   155	- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs
   156	  none when a companion touched the arm), no objective findings, "somatization" and "symptom magnification"; unrelated past
   157	  medical history.
   158	- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.
   159	- **Case stage:** a defense medical exam is a post-suit event (in Texas, TRCP 204 needs a motion and court order). For a
   160	  pre-suit demand packet use the same wording in a carrier records-review (peer-review) letter instead (see lib12).
   161	- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);
   162	  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool
   163	  never concludes malingering.
   164	- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;
   165	  no psychiatric details beyond a generic history line.
   166	
   167	### P8. Waddell signs charted as a score
   168	- **Source:** Fishbain et al., "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell
   169	  Signs", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —
   170	  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).
   171	- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably
   172	  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.
   173	- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,
   174	  distraction, regional disturbance, overreaction) charted as a count.
   175	- **Record features (our inference):** "Waddell 3/5 positive", "distraction SLR negative"; clean negations ("0/5 Waddell
   176	  signs") on other dates; FCE "effort inconsistent" lines. "Waddell" is an eponymous clinical term and is allowed in
   177	  packets (it is on the validator's eponym allow-list, not the denylist).
   178	- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);
   179	  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).
   180	- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.
   181	
   182	### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history
   183	- **Source:** Flores G. et al., "Errors in medical interpretation and their potential clinical consequences in pediatric
   184	  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
   185	  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).
   186	  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice
   187	  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https://texasworker.com/?p=38127.
   188	- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
   189	  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall
   190	  into a reported assault.
   191	- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation
   192	  (fall reported as assault); "espalda" word choice (DWC excerpt only).
   193	- **Record features (our inference):** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two
   194	  records; a Spanish intake form beside an English provider note; DD/MM/YYYY dates on a form from a clinic across the
   195	  border.
   196	- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code
   197	  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.
   198	- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.
   199	
   200	### P10. Copy-forward (cloned) notes that contradict the visit
   201	- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., "Prevalence and Sources of Duplicate Information in the
   202	  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).
   203	- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier
   204	  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.
   205	- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.
   206	- **Record features (our inference):** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
   207	  follow-up); "pain 6/10" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.
   208	- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just
   209	  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);
   210	  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows "near-duplicate text
   211	  across N visits".
   212	- **Synthetic-safety:** template text invented; invented clinic.
   213	
   214	### P11. Left/right transposition across records
   215	- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
   216	  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).
   217	- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32
   218	  sets; 19 were later corrected; three consent forms named the wrong eye.
   219	- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms
   220	  naming the wrong side.
   221	- **Record features (our inference):** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
   222	  the other; a radiculopathy side that flips; a correction addendum.
   223	- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the
   224	  LLM); judge must reject a summary that silently picks a side; HITL step "confirm side".
   225	- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.
   226	
   227	### P12. Handwritten, scanned pages with illegible entries
   228	- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
   229	  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).
   230	- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.
   231	- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.
   232	- **Record features (our inference):** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
   233	  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.
   234	- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-
   235	  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned
   236	  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).
   237	- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.
   238	
   239	### P13. Concussion not diagnosed in the ER; LOC history changes later
   240	- **Source:** Powell J.M. et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis", Arch Phys Med Rehabil 89(8):1550–1555
   241	  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).
   242	- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the
   243	  ED record; ED care focused on ruling out severe injury.
   244	- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.
   245	- **Record features (our inference):** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
   246	  patient", headaches, word-finding complaints; a neuropsych page weeks later.
   247	- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after
   248	  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.
   249	- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.
   250	
   251	### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)
   252	- **Source:** Bai G., Anderson G.F., "Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios",
   253	  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
   254	  (press release; paper not opened).
   255	- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50
   256	  highest-markup hospitals charged roughly ten times, 49 of them for-profit.
   257	- **Record features (from source):** hospital charges several times cost.
   258	- **Record features (our inference):** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
   259	  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.
   260	- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a
   261	  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);
   262	  totals in code only.
   263	- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.
   264	
   265	### P15. Ambulance bill: base rate plus per-mile mileage
   266	- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
   267	  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf
   268	  (search excerpt only).
   269	- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines
   270	  were out of network (63.7% in 2018, 59.4% in 2022).
   271	- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing
   272	  rules confirm two lines per trip and loaded miles rounded up to the tenth (see research/record-formats.md §16).
   273	- **Record features (our inference):** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
   274	  "mileage 14 mi @ $X/mi" and a line total; a balance-bill page.
   275	- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);
   276	  billing analysis (lien/balance columns); code checks miles × rate = stated line.
   277	- **Synthetic-safety:** invented EMS agency, mileage and rates.
   278	
   279	### P16. Same-week symptom contradiction across two providers
   280	- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:50:59.068Z

**tool call — Bash**
````
{
 "command": "cat -n research/case-library-sources-v2.md | sed -n '280,440p'",
 "description": "Read lines 280-440 of v2 source doc"
}
````

### User / tool · 2026-11-02T03:50:59.173Z

**tool result**
````
   280	- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
   281	  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
   282	  (fetched; defense-side account).
   283	- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
   284	  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a
   285	  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.
   286	- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care
   287	  doctor; a recommended discectomy; photos of minor impact.
   288	- **Case stage and entry:** in the source the PCP records came in by defense subpoena (post-suit). In a pre-suit demand
   289	  packet the PCP note arrives from the paralegal's own records request after the client lists the PCP on intake (lib13).
   290	- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
   291	  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but
   292	  not in the file.
   293	- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);
   294	  vertical stepper HITL "two providers disagree; paralegal decides which to cite".
   295	- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.
   296	
   297	### P17. Minimal property damage, low-speed impact (MIST) language in records
   298	- **Source:** Castro W.H. et al., "Do 'whiplash injuries' occur in low-speed rear impacts?", Eur Spine J 6(6):366–375
   299	  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via PubMed). This replaces the round-1
   300	  source (a Texas appellate summary on a reconstructionist's five-mph opinion) because no court, district, docket or
   301	  reporter cite could be found for it and its page returned 403; its names stay on the denylist.
   302	- **Summary:** Nineteen volunteers in staged rear impacts (velocity change about 9-14 km/h) showed no injury signs on exam,
   303	  motion analysis or MRI, with one minor exception. The study is the kind of biomechanical evidence the defense cites for
   304	  "minor impact, soft tissue" arguments.
   305	- **Scope of support:** this source supports only the scenario theme (low-speed impacts are argued to be non-injurious).
   306	  It says nothing about EMS or ER wording.
   307	- **Record features (our inference):** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER
   308	  "low-speed MVC"; later treater notes that describe the crash as "violent" or "high impact" (patient-reported).
   309	- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both
   310	  attributed); speaker attribution.
   311	- **Synthetic-safety:** invented crash; no speeds or vehicles from the source; no study data reproduced in a packet.
   312	
   313	## Coverage map: pattern x D-042 feature
   314	
   315	| Feature (D-042 / base flags) | Patterns |
   316	|---|---|
   317	| Charge reclassification guard (rate vs charge) | P6, P14, P15 |
   318	| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |
   319	| Spanish-language records | P4, P9 |
   320	| Local OCR, scanned/handwritten pages | P12 |
   321	| PDF hidden-text detection | P12 (assumption-based, no public source) |
   322	| Date-convention suggestion | P9 (assumption), P12 |
   323	| Dismissal-pattern learning (eval guard) | P8 |
   324	| Calibrated confidence | P2, P5 |
   325	| Speaker attribution v2 | P4, P7, P9, P13, P17 |
   326	| LLM-as-judge visible | P3, P7, P10, P11 |
   327	| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |
   328	| Credibility flags (D-043) | P7, P8 |
   329	| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |
   330	| Pre-existing | P2, P5 |
   331	| Causation language | P1, P2, P3, P13, P17 |
   332	| Gap | P1, P13 |
   333	
   334	## Suggested v2 packets (each recombines two or more patterns)
   335	
   336	Stage: every packet simulates a **pre-suit demand file** unless marked otherwise. "Entry" says how each cross-provider record
   337	reached the paralegal. Format sections refer to `research/record-formats.md`.
   338	
   339	| Proposed id | Combines | One-line synthetic premise | Stage / entry |
   340	|---|---|---|---|
   341	| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 | Pre-suit; all records from the firm's requests to each provider |
   342	| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; "espalda" ambiguity; side flips between ER and ortho | Pre-suit; Spanish clinic note supplied by the client |
   343	| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS | Pre-suit; EOBs from the client's health plan |
   344	| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; ledgers; older patient comorbidities | Pre-suit; older notes from a records request to the PCP |
   345	| lib12_records_review_credibility | P7 + P8 | Carrier records-review (peer-review) letter with symptom-magnification wording; PT/FCE notes with clean and mixed Waddell lines | Pre-suit; review letter came with the carrier's response to the demand. Litigation-stage variant: TRCP 204 exam report |
   346	| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week | Pre-suit; PCP note from the firm's records request after the client listed the PCP |
   347	| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer | Pre-suit; chiro records faxed by the provider |
   348	| lib15_conclusory_letter_mist | P3 + P17 | "Accident caused all" letter; EMS minor-damage and refused-transport wording | Pre-suit; affidavits obtained from providers for later service, not yet served |
   349	
   350	**Must contain** (the builder's checklist; each packet's expected JSON asserts these) and **formats used**:
   351	
   352	| Proposed id | Must contain (D-042 features and flags) | Formats (record-formats.md §) |
   353	|---|---|---|
   354	| lib08 | Two incident dates in the chart (conflict); ED "denies LOC" vs neuro "brief LOC per patient" (conflict, speaker); first MRI dated after event 2; gap between PT discharge and the neuro visit; stepper HITL step "two incidents found" | EMS PCR §15, ED §2, PT §3, radiology §5, office/specialist note §19, ambulance invoice §16 |
   355	| lib09 | One date `03/06/2026` day-first (truth 3 June 2026) and one `14/05/2026`; "Hx via son (interpreter)"; "espalda" with no level; right vs left shoulder across ER and ortho (conflict, HITL confirm side); translation labeled as LLM output | Spanish note §13, ED §2, office/specialist note §19, scanned intake §14 |
   356	| lib10 | Same DOS on a provider bill and an EOB with different numbers (dedupe + mismatch flag); one UB-04 room line where FL44 rate × FL46 days = FL47 charge (rate-vs-charge guard); a 0001 total line; one CMS-1500 amount OCR'd without a separator with its truth stated | UB-04 §9, ledger §10, EOB §11, CMS-1500 §8 |
   357	| lib11 | Intake "prior accidents: none" vs an older note naming two prior crashes (conflict, pre_existing); ledger with billed, adjustment, payment + payer, balance and LOP columns (items 1-4 and 6, no contract column); comorbidity problem list; calibrated confidence on pre-existing | scanned intake §14, office/specialist note §19, ledger §10, LOP §12 |
   358	| lib12 | At least 4 credibility sentences across 3 dates: 2 clean negations ("0/5 Waddell signs") that must not flag, 2 mixed sentences ("Waddell 3/5; effort inconsistent") that must flag (D-043); at least 3 dismissable non-credibility flags so the dismissal-pattern guard is exercised | records-review/IME report §20, PT §3 |
   359	| lib13 | PCP ROS "denies back pain" copied across 3 visits, and an ortho note "low back pain 8/10" in the same week (conflict, cloned text, no merge); a surgical cost estimate line (D-019: not a charge); HITL "two providers disagree" | office/specialist note §19 (PCP and ortho), ED §2 |
   360	| lib14 | Scanned travel card with checkmarks; one handwritten date with no year; a CMS-1500 grouped line where days = units; an ambulance invoice where miles × per-mile rate = line total; a page whose hidden text layer differs from the image | chiro §4, scanned intake §14, CMS-1500 §8, EMS PCR §15, ambulance invoice §16 |
   361	| lib15 | EMS "refused transport" and "minor damage" (causation lexicon, speaker); ER "low-speed MVC" vs later "violent impact" per patient (conflict); a narrative letter "caused all treatment" shown verbatim, never upgraded (judge rejects any summary that states it as fact); an 18.001 affidavit whose attached bill duplicates a bill already in the packet (dedupe) | EMS PCR §15, ED §2, chiro §4, narrative letter §18, 18.001 affidavit §17 |
   362	
   363	## Denylist additions
   364	
   365	Every real proper noun in this file's sources. The same list is in `DENYLIST_V2` / `DENY_CAPITALISED` of
   366	`research/validate_library.py`; `python3 research/validate_library.py --self-test` fails if the two drift apart, if any
   367	"X v. Y" caption name here is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
   368	accent-insensitive; the three capitalised-only terms are also ordinary lowercase words. Allowed on purpose: "Waddell"
   369	(clinical eponym).
   370	
   371	```text
   372	JLG
   373	Garza
   374	Pechero
   375	Zapata
   376	Guevara
   377	Ferrer
   378	Donis
   379	Matamoros
   380	Castellanos
   381	Morehouse
   382	Reuben
   383	Rueben
   384	Poissant
   385	I-45
   386	Chiv
   387	Figueroa
   388	Central Oregon
   389	Oregon
   390	Broussard
   391	Gunn
   392	McCoy
   393	Rodriguez
   394	Wal-Mart
   395	Walmart
   396	Lewis Brisbois
   397	Brisbois
   398	Harris County
   399	Hampton
   400	Miskell
   401	Baratta
   402	I-635
   403	Castro
   404	Schilgen
   405	Steinkamp
   406	Kantrowitz
   407	Airan-Javia
   408	ElGhrably
   409	Fishbain
   410	Powell
   411	Anderson
   412	Houston
   413	Dallas
   414	Allstate
   415	Hills        # capitalised only
   416	Flores       # capitalised only
   417	Bai          # capitalised only
   418	```
   419	
   420	## Assumptions and limits
   421	
   422	- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source
   423	  documented them. They are included because D-042 reinstated those features and they need test cases.
   424	- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was
   425	  dropped as P17's source in round 2: no court, district or docket could be found and its page returned 403.
   426	- P4 (Chiv v. Figueroa) and P17 (Castro et al.) support only the scenario theme, not any record wording.
   427	- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.public.law mirror (amended through
   428	  Acts 2019, 86th Leg., H.B. 1693; §18.001(b) now says the affidavit is not evidence of causation). The official
   429	  statutes.capitol.texas.gov page is a JavaScript app that did not render for the fetch tool. Opinions are cited for
   430	  scenario shape, not as current law.
   431	- Medical studies (P8–P14, P17) describe general record quality or biomechanics, not PI files; every "Record features"
   432	  line is tagged "(from source)" or "(our inference)".
   433	- Defense-firm (P16) and plaintiff-side write-ups are advocacy; used for scenario shape only.
   434	- Search also surfaced Texas Lawbook (2023-05-16) on a verdict where LOP provider entities were shown to the jury; it is
   435	  paywalled and was not used.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:52:16.569Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/validate_library.py",
 "offset": 1,
 "limit": 15
}
````

### User / tool · 2026-11-02T03:52:16.582Z

**tool result**
````
1	#!/usr/bin/env python3
2	"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).
3	
4	check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
5	runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
6	cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
7	doctors named in opinions, firms, counties, cities, highways and study authors. Matching is case-insensitive and
8	accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.
9	
10	Run:        python3 research/validate_library.py
11	Self-test:  python3 research/validate_library.py --self-test   (planted names must fail; v2 doc names must all be listed)
12	"""
13	import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata
14	
15	ROOT = pathlib.Path(__file__).resolve().parents[1]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:52:16.874Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "offset": 76,
 "limit": 6
}
````

### User / tool · 2026-11-02T03:52:16.881Z

**tool result**
````
76	  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full
77	  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11
78	  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
79	  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief
80	  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.
81	- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:52:22.434Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077r3 && cat > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077r3/probe.py <<'EOF'\nimport re, pathlib\ndoc = pathlib.Path(\"/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md\").read_text()\nAUTH = re.compile(r\"(?<![\\w'’-])([A-Z][\\w'’-]*)(?=,? [A-Z]\\.(?:[A-Z]\\.)*(?!\\w)|\\s+et al\\b)\")\nprint(\"AUTHOR-style:\", sorted({m.group(1) for m in AUTH.finditer(doc)}))\nparas = re.split(r\"\\n\\s*\\n\", doc)\nparen = set()\nfor p in paras:\n    if \"cited\" in p or \"Source\" in p or \"Corroborating\" in p:\n        flat = \" \".join(p.split())\n        for g in re.findall(r\"\\(([^()]*)\\)\", flat):\n            for item in re.split(r\"[,;]\", g):\n                item = item.strip()\n                if re.fullmatch(r\"[A-Z][\\w'’-]*\", item):\n                    paren.add(item)\nprint(\"PAREN-list:\", sorted(paren))\nEOF\npython3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077r3/probe.py",
 "description": "Probe author and citation-list name extraction on v2 doc"
}
````

### User / tool · 2026-11-02T03:52:22.555Z

**tool result**
````
AUTHOR-style: ['Airan-Javia', 'Anderson', 'Bai', 'Castro', 'ElGhrably', 'Fishbain', 'Flores', 'Fraser', 'Kantrowitz', 'Powell', 'Rodríguez-Vera', 'Steinkamp']
PAREN-list: ['Brinjikji', 'D-019', 'D-043', 'Guevara', 'Haygood', 'MIST', 'Nakashima', 'P16', 'P17', 'P9', 'Tesseract']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:52:53.721Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/validate_library.py"
}
````

### User / tool · 2026-11-02T03:52:53.736Z

**tool result**
````
1	#!/usr/bin/env python3
2	"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).
3	
4	check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
5	runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
6	cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
7	doctors named in opinions, firms, counties, cities, highways and study authors. Matching is case-insensitive and
8	accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.
9	
10	Run:        python3 research/validate_library.py
11	Self-test:  python3 research/validate_library.py --self-test   (planted names must fail; v2 doc names must all be listed)
12	"""
13	import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata
14	
15	ROOT = pathlib.Path(__file__).resolve().parents[1]
16	LIB = ROOT / "evals" / "library"
17	V2_DOC = ROOT / "research" / "case-library-sources-v2.md"
18	
19	# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the
20	# two-letter abbreviation (e.g. "TX") where a state must appear.
21	DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
22	               "Rissman", "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia",
23	               "Oklahoma", "Texas", "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]
24	# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
25	DENYLIST_V2 = [
26	    # P1 JLG Trucking v. Garza
27	    "JLG", "Garza", "Pechero", "Zapata",
28	    # P2 Guevara v. Ferrer
29	    "Guevara", "Ferrer",
30	    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)
31	    "Donis", "Matamoros", "Castellanos", "Morehouse", "Reuben", "Rueben", "Poissant", "I-45",
32	    # P4 Chiv v. Figueroa
33	    "Chiv", "Figueroa",
34	    # P5 In re Central Oregon Truck Co.
35	    "Central Oregon", "Oregon", "Broussard",
36	    # P6 Gunn v. McCoy
37	    "Gunn", "McCoy",
38	    # P7 Rodriguez v. Wal-Mart Stores
39	    "Rodriguez", "Wal-Mart", "Walmart",
40	    # P16 defense-firm write-up
41	    "Lewis Brisbois", "Brisbois", "Harris County",
42	    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.
43	    "Hampton", "Miskell", "Baratta", "I-635", "Castro", "Schilgen",
44	    # Study authors cited in v2
45	    "Steinkamp", "Kantrowitz", "Airan-Javia", "ElGhrably", "Fishbain", "Powell", "Anderson",
46	    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions
47	    "Houston", "Dallas", "Allstate",
48	]
49	# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so "rolling hills" or
50	# "flores" (Spanish for flowers) in a packet still passes while "Hills" / "FLORES" as a name fails.
51	DENY_CAPITALISED = ["Hills", "Flores", "Bai"]
52	# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.
53	ALLOWED_EPONYMS = ["Waddell"]
54	DENYLIST = DENYLIST_V1 + DENYLIST_V2
55	BANNER = "SYNTHETIC — invented for evaluation; not real patient data\n"
56	
57	
58	def fold(s):
59	    """Strip accents so 'Rodríguez' matches 'Rodriguez'."""
60	    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
61	
62	
63	_ANY = [(w, re.compile(r"(?<!\w)" + re.escape(fold(w)) + r"(?!\w)", re.I)) for w in DENYLIST]
64	_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]
65	
66	
67	def scan_text(text):
68	    """Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital)."""
69	    t = fold(text)
70	    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]
71	
72	
73	def doc_denylist_block(doc_text):
74	    """Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed)."""
75	    m = re.search(r"## Denylist additions.*?```text\n(.*?)```", doc_text, re.S)
76	    if not m:
77	        return None
78	    return [ln.split("#")[0].strip() for ln in m.group(1).splitlines() if ln.split("#")[0].strip()]
79	
80	
81	_GENERIC = {"In", "re", "Inc", "Inc.", "LLC", "LLC,", "Co", "Co.", "Stores", "Stores,", "Truck", "Trucking", "Trucking,", "The",
82	            "of", "and", "Tex", "Tex.", "App", "App.", "No", "No."}
83	
84	
85	def doc_caption_names(doc_text):
86	    """Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc."""
87	    names = set()
88	    for a, b in re.findall(r"([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*) v\. ([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*)", doc_text):
89	        for side in (a, b):
90	            for tok in re.split(r"[ ,]+", side):
91	                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):
92	                    names.add(tok.rstrip(".,"))
93	    for x in re.findall(r"In re ([A-Z][\w'-]*(?: [A-Z][\w'-]*)*)", doc_text):
94	        toks = [t for t in x.split() if t not in _GENERIC]
95	        if toks:
96	            names.add(" ".join(toks[:2]))
97	    return names
98	
99	
100	def self_test():
101	    fails = []
102	    for w in DENYLIST:
103	        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:
104	            if w not in scan_text(f"Seen by Dr. {variant} at the clinic."):
105	                fails.append(f"planted {variant!r} not caught")
106	    for w in DENY_CAPITALISED:
107	        for variant in (w, w.upper()):
108	            if w not in scan_text(f"Referred by {variant} Family Clinic."):
109	                fails.append(f"planted {variant!r} not caught")
110	        if scan_text(f"walked up the {w.lower()} near home"):
111	            fails.append(f"lowercase common word {w.lower()!r} wrongly flagged")
112	    if not scan_text("Patient: Ana Rodríguez (SYNTHETIC)"):
113	        fails.append("accented Rodríguez not caught")
114	    for w in ALLOWED_EPONYMS:
115	        if scan_text(f"{w} signs 0/5 today."):
116	            fails.append(f"eponym {w!r} wrongly flagged")
117	    doc = V2_DOC.read_text()
118	    block = doc_denylist_block(doc)
119	    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}
120	    if block is None:
121	        fails.append("v2 doc has no '## Denylist additions' ```text block")
122	    else:
123	        for w in block:
124	            if fold(w).lower() not in listed:
125	                fails.append(f"v2 doc denylist term {w!r} missing from validate_library.py")
126	        for w in DENYLIST_V2 + DENY_CAPITALISED:
127	            if w not in block:
128	                fails.append(f"validate_library.py term {w!r} missing from the v2 doc block")
129	    for name in sorted(doc_caption_names(doc)):
130	        if not any(fold(part).lower() in listed for part in [name] + name.split()):
131	            fails.append(f"v2 caption name {name!r} not on the denylist")
132	    # End-to-end: a planted packet must make the library scan fail.
133	    with tempfile.TemporaryDirectory() as tmp:
134	        p = pathlib.Path(tmp) / "case_planted.txt"
135	        p.write_text(BANNER + "Patient seen by DR. GARZA after the crash on i-45.\n")
136	        if not scan_library([p]):
137	            fails.append("planted packet passed the library scan")
138	    for f in fails:
139	        print("SELF-TEST FAIL:", f)
140	    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3
141	    print("self-test:", "FAIL" if fails else f"ok ({n} planted variants caught, {len(doc_caption_names(doc))} caption names covered)")
142	    return 1 if fails else 0
143	
144	
145	def scan_library(files):
146	    bad = []
147	    for f in files:
148	        t = f.read_text()
149	        for w in scan_text(t):
150	            bad.append(f"{f.name}: contains real identifier {w!r}")
151	        if f.suffix == ".txt" and not t.startswith(BANNER):
152	            bad.append(f"{f.name}: missing SYNTHETIC header")
153	    return bad
154	
155	
156	def main():
157	    if "--self-test" in sys.argv:
158	        return self_test()
159	    cases = sorted(LIB.glob("case_*.expected.json"))
160	    if len(cases) < 6:
161	        print(f"FAIL: need >= 6 library cases, found {len(cases)}")
162	        return 1
163	    with tempfile.TemporaryDirectory() as tmp:
164	        d = pathlib.Path(tmp) / "golden"
165	        shutil.copytree(ROOT / "evals" / "golden", d)
166	        for f in LIB.glob("case_*"):
167	            shutil.copy(f, d / f.name)
168	        r = subprocess.run([sys.executable, str(d / "check_golden.py")], capture_output=True, text=True, cwd=d)
169	    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])
170	    bad = scan_library(sorted(LIB.glob("case_*")))
171	    for b in bad:
172	        print("IDENTIFIER CHECK FAIL:", b)
173	    terms = len(DENYLIST) + len(DENY_CAPITALISED)
174	    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)")
175	    return 1 if (r.returncode or bad) else 0
176	
177	
178	if __name__ == "__main__":
179	    sys.exit(main())
180	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:22.248Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/validate_library.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).\n\ncheck_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,\nruns the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the\ncited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,\ndoctors named in opinions, study authors, firms, counties, cities and highways. Matching is case-insensitive and\naccent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.\n\nSelf-test checks the v2 doc mechanically: every surname written before author initials or 'et al' (e.g. 'Fraser S.G.'), every\nbare surname in a parenthesised list inside a paragraph that cites earlier sources (e.g. 'Brinjikji, Nakashima'), and every\n'X v. Y' / 'In re X' caption name must be on the denylist, and each one planted in a packet must fail the scan. A newly cited\nname therefore fails the self-test until it is added to DENYLIST_V2 and the doc's 'Denylist additions' block.\n\nRun:        python3 research/validate_library.py\nSelf-test:  python3 research/validate_library.py --self-test\n\"\"\"\nimport pathlib, re, shutil, subprocess, sys, tempfile, unicodedata\n\nROOT = pathlib.Path(__file__).resolve().parents[1]\nLIB = ROOT / \"evals\" / \"library\"\nV2_DOC = ROOT / \"research\" / \"case-library-sources-v2.md\"\n\n# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the\n# two-letter abbreviation (e.g. \"TX\") where a state must appear.\nDENYLIST_V1 = [\"Nichols\", \"Duke Linden\", \"Haygood\", \"Escabedo\", \"K & L\", \"K&L\", \"Auto Crushers\", \"Alexandria\", \"Puerto Rico\",\n               \"Rissman\", \"Colossus\", \"Manitoba\", \"Verisk\", \"Medicare\", \"Tennessee\", \"Nebraska\", \"New Jersey\", \"Virginia\",\n               \"Oklahoma\", \"Texas\", \"Florida\", \"California\", \"Illinois\", \"Michigan\", \"Kelly\", \"Cutch\"]\n# v2 sources (research/case-library-sources-v2.md, \"Denylist additions\" block). Keep the two lists in sync; --self-test checks.\nDENYLIST_V2 = [\n    # P1 JLG Trucking v. Garza\n    \"JLG\", \"Garza\", \"Pechero\", \"Zapata\",\n    # P2 Guevara v. Ferrer\n    \"Guevara\", \"Ferrer\",\n    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)\n    \"Donis\", \"Matamoros\", \"Castellanos\", \"Morehouse\", \"Reuben\", \"Rueben\", \"Poissant\", \"I-45\",\n    # P4 Chiv v. Figueroa\n    \"Chiv\", \"Figueroa\",\n    # P5 In re Central Oregon Truck Co.\n    \"Central Oregon\", \"Oregon\", \"Broussard\",\n    # P6 Gunn v. McCoy\n    \"Gunn\", \"McCoy\",\n    # P7 Rodriguez v. Wal-Mart Stores\n    \"Rodriguez\", \"Wal-Mart\", \"Walmart\",\n    # P16 defense-firm write-up\n    \"Lewis Brisbois\", \"Brisbois\", \"Harris County\",\n    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.\n    \"Hampton\", \"Miskell\", \"Baratta\", \"I-635\", \"Castro\", \"Schilgen\",\n    # Study authors cited in v2 (author initials or 'et al' in source lines; bare names in the opening citation list)\n    \"Steinkamp\", \"Kantrowitz\", \"Airan-Javia\", \"ElGhrably\", \"Fishbain\", \"Powell\", \"Anderson\",\n    \"Fraser\", \"Brinjikji\", \"Nakashima\", \"Vera\", \"Rodríguez-Vera\",\n    # Firm website slugs in cited URLs (not people; a slug never occurs as ordinary packet text)\n    \"mdjwlaw\", \"painterfirm\",\n    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions\n    \"Houston\", \"Dallas\", \"Allstate\",\n]\n# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so \"rolling hills\" or\n# \"flores\" (Spanish for flowers) in a packet still passes while \"Hills\" / \"FLORES\" as a name fails.\nDENY_CAPITALISED = [\"Hills\", \"Flores\", \"Bai\", \"FAIR Health\"]\n# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.\nALLOWED_EPONYMS = [\"Waddell\"]\nDENYLIST = DENYLIST_V1 + DENYLIST_V2\nBANNER = \"SYNTHETIC — invented for evaluation; not real patient data\\n\"\n\n\ndef fold(s):\n    \"\"\"Strip accents so 'Rodríguez' matches 'Rodriguez'.\"\"\"\n    return \"\".join(c for c in unicodedata.normalize(\"NFKD\", s) if not unicodedata.combining(c))\n\n\n_ANY = [(w, re.compile(r\"(?<!\\w)\" + re.escape(fold(w)) + r\"(?!\\w)\", re.I)) for w in DENYLIST]\n_CAP = [(w, re.compile(r\"(?<!\\w)(?:\" + re.escape(w) + \"|\" + re.escape(w.upper()) + r\")(?!\\w)\")) for w in DENY_CAPITALISED]\n\n\ndef scan_text(text):\n    \"\"\"Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital).\"\"\"\n    t = fold(text)\n    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]\n\n\ndef doc_denylist_block(doc_text):\n    \"\"\"Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed).\"\"\"\n    m = re.search(r\"## Denylist additions.*?```text\\n(.*?)```\", doc_text, re.S)\n    if not m:\n        return None\n    return [ln.split(\"#\")[0].strip() for ln in m.group(1).splitlines() if ln.split(\"#\")[0].strip()]\n\n\n_GENERIC = {\"In\", \"re\", \"Inc\", \"Inc.\", \"LLC\", \"LLC,\", \"Co\", \"Co.\", \"Stores\", \"Stores,\", \"Truck\", \"Trucking\", \"Trucking,\", \"The\",\n            \"of\", \"and\", \"Tex\", \"Tex.\", \"App\", \"App.\", \"No\", \"No.\"}\n\n\ndef doc_caption_names(doc_text):\n    \"\"\"Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc.\"\"\"\n    names = set()\n    for a, b in re.findall(r\"([A-Z][\\w.'&-]*(?:,? [A-Z][\\w.'&-]*)*) v\\. ([A-Z][\\w.'&-]*(?:,? [A-Z][\\w.'&-]*)*)\", doc_text):\n        for side in (a, b):\n            for tok in re.split(r\"[ ,]+\", side):\n                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):\n                    names.add(tok.rstrip(\".,\"))\n    for x in re.findall(r\"In re ([A-Z][\\w'-]*(?: [A-Z][\\w'-]*)*)\", doc_text):\n        toks = [t for t in x.split() if t not in _GENERIC]\n        if toks:\n            names.add(\" \".join(toks[:2]))\n    return names\n\n\n# A surname is a capitalised word directly before author initials ('Fraser S.G.', 'Steinkamp J.', 'Rodríguez-Vera F.J.')\n# or before 'et al' ('Fishbain et al.'). Initials are capital letters only, so 'Co.', 'Inc.' and 'No.' never match.\n_AUTHOR_RX = re.compile(r\"(?<![\\w'’-])([A-Z][\\w'’-]*)(?=,? [A-Z]\\.(?:[A-Z]\\.)*(?!\\w)|\\s+et al\\b)\")\n\n\ndef doc_author_names(doc_text):\n    \"\"\"Surnames written before author initials or 'et al' anywhere in the v2 doc.\"\"\"\n    return {m.group(1) for m in _AUTHOR_RX.finditer(doc_text)}\n\n\ndef doc_listed_citation_names(doc_text):\n    \"\"\"Bare surnames in parenthesised lists inside paragraphs that cite earlier sources (the 'already cited' sentence).\n\n    Only single capitalised words with lowercase letters count, so acronyms (MIST), IDs (D-043) and tool names are skipped\n    by shape, and multi-word items such as 'In re Allstate' or 'K&L Auto Crushers' are left to the denylist entries.\n    \"\"\"\n    names = set()\n    for para in re.split(r\"\\n\\s*\\n\", doc_text):\n        if \"cited\" not in para:\n            continue\n        flat = \" \".join(para.split())\n        for group in re.findall(r\"\\(([^()]*)\\)\", flat):\n            for item in re.split(r\"[,;]\", group):\n                item = item.strip()\n                if re.fullmatch(r\"[A-Z][a-z][\\w'’-]*\", item):\n                    names.add(item)\n    return names\n\n\ndef doc_citation_names(doc_text):\n    \"\"\"Every name the v2 doc cites: author surnames, bare names in citation lists, and caption names.\"\"\"\n    return doc_author_names(doc_text) | doc_listed_citation_names(doc_text) | doc_caption_names(doc_text)\n\n\ndef _covered(name, listed):\n    \"\"\"A cited name is covered when the name, one of its words, or one of its hyphen parts is listed (case/accent-insensitive).\"\"\"\n    return any(fold(p).lower() in listed for p in [name] + name.split() + re.split(r\"-\", name))\n\n\ndef self_test(doc_text=None):\n    \"\"\"Run the self-test. doc_text overrides the v2 doc (used to prove a newly cited name fails the test).\"\"\"\n    fails = []\n    for w in DENYLIST:\n        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:\n            if w not in scan_text(f\"Seen by Dr. {variant} at the clinic.\"):\n                fails.append(f\"planted {variant!r} not caught\")\n    for w in DENY_CAPITALISED:\n        for variant in (w, w.upper()):\n            if w not in scan_text(f\"Referred by {variant} Family Clinic.\"):\n                fails.append(f\"planted {variant!r} not caught\")\n        if scan_text(f\"walked up the {w.lower()} near home\"):\n            fails.append(f\"lowercase common word {w.lower()!r} wrongly flagged\")\n    if not scan_text(\"Patient: Ana Rodríguez (SYNTHETIC)\"):\n        fails.append(\"accented Rodríguez not caught\")\n    for w in ALLOWED_EPONYMS:\n        if scan_text(f\"{w} signs 0/5 today.\"):\n            fails.append(f\"eponym {w!r} wrongly flagged\")\n    doc = V2_DOC.read_text() if doc_text is None else doc_text\n    block = doc_denylist_block(doc)\n    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}\n    if block is None:\n        fails.append(\"v2 doc has no '## Denylist additions' ```text block\")\n    else:\n        for w in block:\n            if fold(w).lower() not in listed:\n                fails.append(f\"v2 doc denylist term {w!r} missing from validate_library.py\")\n        for w in DENYLIST_V2 + DENY_CAPITALISED:\n            if w not in block:\n                fails.append(f\"validate_library.py term {w!r} missing from the v2 doc block\")\n    authors = doc_author_names(doc)\n    cite_lists = doc_listed_citation_names(doc)\n    captions = doc_caption_names(doc)\n    for name in sorted(authors | cite_lists | captions):\n        if not _covered(name, listed):\n            kind = \"author\" if name in authors else \"citation-list\" if name in cite_lists else \"caption\"\n            fails.append(f\"v2 doc cites {kind} name {name!r} but it is not on the denylist (add it to DENYLIST_V2 and the doc block)\")\n    with tempfile.TemporaryDirectory() as tmp:\n        # Every cited author or citation-list surname, planted in a packet, must make the library scan fail.\n        for i, name in enumerate(sorted(authors | cite_lists)):\n            p = pathlib.Path(tmp) / f\"case_planted_author_{i}.txt\"\n            p.write_text(BANNER + f\"Seen by {name} S.G. at the clinic on 03/06/2026.\\n\")\n            if not scan_library([p]):\n                fails.append(f\"planted author/citation surname {name!r} passed the library scan\")\n        # End-to-end: a planted packet must make the library scan fail.\n        p = pathlib.Path(tmp) / \"case_planted.txt\"\n        p.write_text(BANNER + \"Patient seen by DR. GARZA after the crash on i-45.\\n\")\n        if not scan_library([p]):\n            fails.append(\"planted packet passed the library scan\")\n    for f in fails:\n        print(\"SELF-TEST FAIL:\", f)\n    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3 + len(authors | cite_lists)\n    print(\"self-test:\", \"FAIL\" if fails else\n          f\"ok ({n} planted variants caught; {len(authors | cite_lists | captions)} cited names covered: \"\n          f\"{len(authors)} author, {len(cite_lists)} citation-list, {len(captions)} caption)\")\n    return 1 if fails else 0\n\n\ndef scan_library(files):\n    bad = []\n    for f in files:\n        t = f.read_text()\n        for w in scan_text(t):\n            bad.append(f\"{f.name}: contains real identifier {w!r}\")\n        if f.suffix == \".txt\" and not t.startswith(BANNER):\n            bad.append(f\"{f.name}: missing SYNTHETIC header\")\n    return bad\n\n\ndef main():\n    if \"--self-test\" in sys.argv:\n        return self_test()\n    cases = sorted(LIB.glob(\"case_*.expected.json\"))\n    if len(cases) < 6:\n        print(f\"FAIL: need >= 6 library cases, found {len(cases)}\")\n        return 1\n    with tempfile.TemporaryDirectory() as tmp:\n        d = pathlib.Path(tmp) / \"golden\"\n        shutil.copytree(ROOT / \"evals\" / \"golden\", d)\n        for f in LIB.glob(\"case_*\"):\n            shutil.copy(f, d / f.name)\n        r = subprocess.run([sys.executable, str(d / \"check_golden.py\")], capture_output=True, text=True, cwd=d)\n    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])\n    bad = scan_library(sorted(LIB.glob(\"case_*\")))\n    for b in bad:\n        print(\"IDENTIFIER CHECK FAIL:\", b)\n    terms = len(DENYLIST) + len(DENY_CAPITALISED)\n    print(\"identifier check:\", \"FAIL\" if bad else f\"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)\")\n    return 1 if (r.returncode or bad) else 0\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
}
````

### User / tool · 2026-11-02T03:53:22.308Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/validate_library.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:24.650Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport sys; sys.path.insert(0,'research')\nimport validate_library as v\nd=v.V2_DOC.read_text()\nprint('authors', sorted(v.doc_author_names(d)))\nprint('cite-lists', sorted(v.doc_listed_citation_names(d)))\nprint('captions', sorted(v.doc_caption_names(d)))\n\" ; python3 research/validate_library.py --self-test; echo \"exit=$?\"",
 "description": "Print extracted citation names and run self-test before doc update"
}
````

### User / tool · 2026-11-02T03:53:24.836Z

**tool result**
````
authors ['Airan-Javia', 'Anderson', 'Bai', 'Castro', 'ElGhrably', 'Fishbain', 'Flores', 'Fraser', 'Kantrowitz', 'Powell', 'Rodríguez-Vera', 'Steinkamp']
cite-lists ['Brinjikji', 'Guevara', 'Haygood', 'Nakashima']
captions ['Allstate', 'Central Oregon', 'Chiv', 'Donis', 'Ferrer', 'Figueroa', 'Garza', 'Guevara', 'Gunn', 'Hampton', 'Hills', 'JLG', 'McCoy', 'Miskell', 'Rodriguez', 'Wal-Mart']
SELF-TEST FAIL: validate_library.py term 'Fraser' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'Brinjikji' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'Nakashima' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'Vera' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'Rodríguez-Vera' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'mdjwlaw' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'painterfirm' missing from the v2 doc block
SELF-TEST FAIL: validate_library.py term 'FAIR Health' missing from the v2 doc block
self-test: FAIL
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:26.853Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "offset": 23,
 "limit": 6
}
````

### User / tool · 2026-11-02T03:53:26.862Z

**tool result**
````
23	2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
24	   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
25	   that denylist (see "Denylist additions" below; matching is case- and accent-insensitive), and
26	   `python3 research/validate_library.py --self-test` proves a planted name fails. Common surnames that appear here
27	   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
28	   including in the Spanish-language packets: pick distinctive invented surnames instead.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:27.289Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "offset": 363,
 "limit": 58
}
````

### User / tool · 2026-11-02T03:53:27.301Z

**tool result**
````
363	## Denylist additions
364	
365	Every real proper noun in this file's sources. The same list is in `DENYLIST_V2` / `DENY_CAPITALISED` of
366	`research/validate_library.py`; `python3 research/validate_library.py --self-test` fails if the two drift apart, if any
367	"X v. Y" caption name here is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
368	accent-insensitive; the three capitalised-only terms are also ordinary lowercase words. Allowed on purpose: "Waddell"
369	(clinical eponym).
370	
371	```text
372	JLG
373	Garza
374	Pechero
375	Zapata
376	Guevara
377	Ferrer
378	Donis
379	Matamoros
380	Castellanos
381	Morehouse
382	Reuben
383	Rueben
384	Poissant
385	I-45
386	Chiv
387	Figueroa
388	Central Oregon
389	Oregon
390	Broussard
391	Gunn
392	McCoy
393	Rodriguez
394	Wal-Mart
395	Walmart
396	Lewis Brisbois
397	Brisbois
398	Harris County
399	Hampton
400	Miskell
401	Baratta
402	I-635
403	Castro
404	Schilgen
405	Steinkamp
406	Kantrowitz
407	Airan-Javia
408	ElGhrably
409	Fishbain
410	Powell
411	Anderson
412	Houston
413	Dallas
414	Allstate
415	Hills        # capitalised only
416	Flores       # capitalised only
417	Bai          # capitalised only
418	```
419	
420	## Assumptions and limits
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:29.143Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "old_string": "   that denylist (see \"Denylist additions\" below; matching is case- and accent-insensitive), and\n   `python3 research/validate_library.py --self-test` proves a planted name fails. Common surnames that appear here",
 "new_string": "   that denylist (see \"Denylist additions\" below; matching is case- and accent-insensitive). `--self-test` extracts every\n   author surname, every bare name in the opening citation list and every caption name from this file, fails if any is not\n   listed, and fails if a planted packet containing one passes the scan. Common surnames that appear here"
}
````

### User / tool · 2026-11-02T03:53:29.196Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:31.562Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "old_string": "Every real proper noun in this file's sources. The same list is in `DENYLIST_V2` / `DENY_CAPITALISED` of\n`research/validate_library.py`; `python3 research/validate_library.py --self-test` fails if the two drift apart, if any\n\"X v. Y\" caption name here is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and\naccent-insensitive; the three capitalised-only terms are also ordinary lowercase words. Allowed on purpose: \"Waddell\"\n(clinical eponym).",
 "new_string": "Every real person's name and every firm-website slug or organisation name cited in this file's sources, including the\nstudy authors (Steinkamp, Kantrowitz, Airan-Javia, ElGhrably, Fishbain, Powell, Anderson, Fraser, Brinjikji, Nakashima,\nRodríguez-Vera, Flores, Bai) and the bare-name citation list in the opening paragraph (Brinjikji, Nakashima). The same list is\nin `DENYLIST_V2` / `DENY_CAPITALISED` of `research/validate_library.py`. `python3 research/validate_library.py --self-test`\nfails if the two drift apart, if any surname it extracts from this file (author initials or 'et al', citation list, or\n\"X v. Y\" caption) is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and\naccent-insensitive; the four capitalised-only terms are also ordinary lowercase words or phrases. Allowed on purpose:\n\"Waddell\" (clinical eponym)."
}
````

### User / tool · 2026-11-02T03:53:31.620Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:32.350Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "old_string": "Allstate\nHills        # capitalised only\nFlores       # capitalised only\nBai          # capitalised only\n```",
 "new_string": "Allstate\nFraser\nBrinjikji\nNakashima\nVera\nRodríguez-Vera\nmdjwlaw\npainterfirm\nHills        # capitalised only\nFlores       # capitalised only\nBai          # capitalised only\nFAIR Health  # capitalised only (organisation)\n```"
}
````

### User / tool · 2026-11-02T03:53:32.410Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:36.364Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "old_string": "  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the withdrawn 2020 opinion only.",
 "new_string": "  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the 2020 opinion (2020 WL 206187) and does not mention\n  the withdrawal; the withdrawal and substitution are shown only on the docket page above (the substitute opinion is not linked)."
}
````

### User / tool · 2026-11-02T03:53:36.423Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:37.650Z

**tool call — Bash**
````
{
 "command": "python3 research/validate_library.py --self-test; echo \"self-test exit=$?\"; python3 research/validate_library.py; echo \"validate exit=$?\"",
 "description": "Run self-test and library validation after doc update"
}
````

### User / tool · 2026-11-02T03:53:38.031Z

**tool result**
````
self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)
self-test exit=0
golden OK: 17 cases (16 synthetic), 85 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (7 packets, 80 denylist terms, case-insensitive)
validate exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:48.705Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t077r3\ncat > $S/negtest.py <<'EOF'\nimport importlib.util, pathlib, shutil, tempfile, io, contextlib, sys\nREPO = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\nSRC = (REPO / \"research\" / \"validate_library.py\").read_text()\nDOC = REPO / \"research\" / \"case-library-sources-v2.md\"\n\ndef load(path, name):\n    spec = importlib.util.spec_from_file_location(name, path)\n    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n    m.V2_DOC = DOC  # point the copy at the real doc\n    return m\n\ndef run(fn):\n    buf = io.StringIO()\n    with contextlib.redirect_stdout(buf):\n        rc = fn()\n    return rc, buf.getvalue().strip()\n\n# 1. Real module: must pass.\nmod = load(REPO / \"research\" / \"validate_library.py\", \"vl_real\")\nprint(\"[1] real:\", run(mod.self_test))\n\n# 2. Newly cited author added to the doc without a denylist entry: must fail.\ndoc_text = DOC.read_text()\nnew_doc = doc_text.replace(\"## Assumptions and limits\",\n    \"Planted check: Zorbell K., Quintana M. et al. (2024) cited for a test only.\\n\\n## Assumptions and limits\", 1)\nprint(\"[2] new author uncovered:\", run(lambda: mod.self_test(doc_text=new_doc)))\n\n# 3. Study author removed from the list (Fraser): must fail.\ns3 = SRC.replace('\"Fraser\", \"Brinjikji\"', '\"Brinjikji\"', 1)\nassert s3 != SRC\np3 = pathlib.Path(tempfile.mkdtemp()) / \"vl_no_fraser.py\"; p3.write_text(s3)\nm3 = load(p3, \"vl_no_fraser\")\nprint(\"[3] Fraser dropped:\", run(m3.self_test))\n\n# 4. Planted study-author packet through the full validate_library.py path: must exit 1.\nwork = pathlib.Path(tempfile.mkdtemp())\nlib = work / \"library\"; shutil.copytree(REPO / \"evals\" / \"library\", lib)\n(lib / \"case_planted_author.txt\").write_text(mod.BANNER + \"Seen by Dr. Pennywhistle. Ref: ElGhrably I., Fraser S.G. (2008).\\n\")\nshutil.copy(REPO / \"evals\" / \"library\" / \"case_lib01_er_only_then_gap.expected.json\", lib / \"case_planted_author.expected.json\")\nmod.LIB = lib\nrc, out = run(mod.main)\nprint(\"[4] planted packet via main():\", \"exit\", rc)\nprint(\"\\n\".join(l for l in out.splitlines() if \"IDENTIFIER\" in l or \"identifier check\" in l))\nEOF\ncd /Users/arsis/zlayt-pm-project && python3 -I $S/negtest.py",
 "description": "Run negative tests: new citation, dropped author, planted packet"
}
````

### User / tool · 2026-11-02T03:53:49.172Z

**tool result**
````
[1] real: (0, 'self-test: ok (408 planted variants caught; 31 cited names covered: 12 author, 15 citation-list, 16 caption)')
[2] new author uncovered: (1, "SELF-TEST FAIL: v2 doc cites author name 'Quintana' but it is not on the denylist (add it to DENYLIST_V2 and the doc block)\nSELF-TEST FAIL: v2 doc cites author name 'Zorbell' but it is not on the denylist (add it to DENYLIST_V2 and the doc block)\nSELF-TEST FAIL: planted author/citation surname 'Quintana' passed the library scan\nSELF-TEST FAIL: planted author/citation surname 'Zorbell' passed the library scan\nself-test: FAIL")
[3] Fraser dropped: (1, "SELF-TEST FAIL: v2 doc denylist term 'Fraser' missing from validate_library.py\nSELF-TEST FAIL: v2 doc cites author name 'Fraser' but it is not on the denylist (add it to DENYLIST_V2 and the doc block)\nSELF-TEST FAIL: planted author/citation surname 'Fraser' passed the library scan\nself-test: FAIL")
[4] planted packet via main(): exit 1
IDENTIFIER CHECK FAIL: case_planted_author.txt: contains real identifier 'ElGhrably'
IDENTIFIER CHECK FAIL: case_planted_author.txt: contains real identifier 'Fraser'
identifier check: FAIL
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:53.041Z

**tool call — Bash**
````
{
 "command": "git status --short -- research/case-library-sources-v2.md research/validate_library.py && git diff --stat -- research/case-library-sources-v2.md research/validate_library.py && git log -3 --format='%h %s%n%b---' -- research/validate_library.py | head -30 && git diff --cached --stat | tail -1",
 "description": "Check git status and recent commit trailer convention"
}
````

### User / tool · 2026-11-02T03:53:53.284Z

**tool result**
````
 M research/case-library-sources-v2.md
 M research/validate_library.py
 research/case-library-sources-v2.md | 29 +++++++++----
 research/validate_library.py        | 84 +++++++++++++++++++++++++++++++------
 2 files changed, 93 insertions(+), 20 deletions(-)
5c2cb2f fix(research): v2 case-library denylist enforced with self-test, tagged record features, verified citations (T-077 r2)
- validate_library.py: v2 real names added (case- and accent-insensitive), capitalised-only terms for
  common words, Waddell eponym allowed, --self-test plants mixed-case names and cross-checks the doc's
  Denylist additions block and every X v. Y caption
- v2 doc: Record features tagged from source / our inference; Hills v. Donis re-cited to the 2021
  substitute opinion (read in full); P17 source replaced (Hampton not retrievable); P5 six items
  reworded; P6 case type; stage/entry, must-contain and formats columns for lib08-lib15

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
---
a010dd4 feat(research): synthetic case library, 7 packets with sources and validator (T-052)
Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:55.353Z

**tool call — Bash**
````
{
 "command": "git add research/case-library-sources-v2.md research/validate_library.py && git status --short -- research/case-library-sources-v2.md research/validate_library.py",
 "description": "Stage the two research files explicitly"
}
````

### User / tool · 2026-11-02T03:53:55.470Z

**tool result**
````
M  research/case-library-sources-v2.md
M  research/validate_library.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:53:56.861Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)\n\n- validate_library.py: DENYLIST_V2 adds Fraser, Brinjikji, Nakashima, Vera, Rodriguez-Vera (study authors and the bare\n  citation list), plus mdjwlaw, painterfirm and FAIR Health (cited firm/organisation tokens)\n- self-test extracts every author surname (before initials or et al), every bare name in the 'already cited' list and\n  every X v. Y caption; each must be listed, and each planted in a packet must fail the scan\n- v2 doc: denylist block and rule 2 updated; Hills v. Donis newsbrief sentence no longer says it mentions withdrawal\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- research/case-library-sources-v2.md research/validate_library.py",
 "description": "Commit the two research files with the T-077 r3 message"
}
````

### User / tool · 2026-11-02T03:53:57.142Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main 8d7548d] fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
 2 files changed, 93 insertions(+), 20 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:01.445Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-077 --agent researcher --text \"Round 3 (8d7548d): extractor added to validate_library.py (author initials/et al, 'already cited' list, X v. Y captions); 4 study authors + Vera/Rodriguez-Vera + firm slugs + FAIR Health on denylist; negative tests: dropped Fraser fails, newly cited Zorbell/Quintana fails, planted ElGhrably/Fraser packet fails main() exit 1\" && python3 tools/board.py ac T-077 --check 2 --agent researcher --evidence \"research/validate_library.py --self-test -> ok (408 planted variants; 31 cited names: 12 author, 15 citation-list, 16 caption); python3 research/validate_library.py -> identifier check ok (7 packets, 80 terms); planted scratch packet with ElGhrably + Fraser S.G. -> exit 1 (scratchpad negtest.py, commit 8d7548d)\"",
 "description": "Add board note and AC check 2 evidence"
}
````

### User / tool · 2026-11-02T03:54:01.653Z

**tool result**
````
noted on T-077
AC 2 checked: research/validate_library.py --self-test -> ok (408 planted variants; 31 cited names: 12 author, 15 citation-list, 16 caption); python3 research/validate_library.py -> identifier check ok (7 packets, 80 terms); planted scratch packet with ElGhrably + Fraser S.G. -> exit 1 (scratchpad negtest.py, commit 8d7548d)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:04.874Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py handoff T-077 --agent researcher --text \"What changed (r3, 8d7548d): validate_library.py extracts every author surname (before initials or et al), every bare name in the 'already cited' list, and every X v. Y caption; all must be on DENYLIST_V2 (added Fraser, Brinjikji, Nakashima, Vera, Rodriguez-Vera, mdjwlaw, painterfirm; FAIR Health caps-only). Doc block and rule 2 updated; Hills newsbrief sentence fixed. · How verified: python3 research/validate_library.py --self-test -> ok (408 planted, 31 cited names); python3 research/validate_library.py -> ok (7 packets, 80 terms). Negative tests (scratchpad negtest.py): new uncited author Zorbell/Quintana -> self-test FAIL; Fraser dropped -> FAIL; planted packet with ElGhrably + Fraser S.G. via main() -> exit 1. · What's left: firm-name exemption is a judgment (only URL slugs and FAIR Health listed; 'Painter' not listed because it is an ordinary word); v1 doc not re-checked. · What surprised me: the 'already cited' sentence hid two real names (Brinjikji, Nakashima) with no initials, so an initials-only extractor would have missed them; the paren-list rule is scoped to paragraphs containing 'cited'.\" && python3 tools/board.py move T-077 in_review --agent researcher",
 "description": "Write handoff and move card to in_review"
}
````

### User / tool · 2026-11-02T03:54:05.075Z

**tool result**
````
handoff written on T-077
T-077: in_progress -> in_review
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:07.992Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py lesson --agent researcher --text \"Denylist self-tests must extract names mechanically from the doc (author initials or et al, citation-list parens, captions); checking only X v. Y captions let study authors (Brinjikji, Fraser) pass in r2. Planting each extracted name in a packet proves the scan catches it.\" && python3 -c \"print('ok')\"",
 "description": "Record a lesson on denylist self-test coverage"
}
````

### User / tool · 2026-11-02T03:54:08.145Z

**tool result**
````
lesson recorded
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:10.647Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/research-workflow-pitfalls.md",
 "old_string": "Any real name cited in research/case-library-sources*.md must be on the DENYLIST in research/validate_library.py in the same commit, and the doc carries a \"## Denylist additions\" text block that `--self-test` cross-checks (planted mixed-case names must fail; every \"X v. Y\" caption token must be listed). Specimens in record-formats.md must pass scan_text too (state written as \"TX\").\n**Why:** T-077 review major: doc said \"add names before packets are built\" but nothing enforced it.\n**How to apply:** run `python3 research/validate_library.py --self-test` and `python3 research/record_formats_check.py` before handing off research cards.",
 "new_string": "Any real name cited in research/case-library-sources*.md must be on the DENYLIST in research/validate_library.py in the same commit, and the doc carries a \"## Denylist additions\" text block that `--self-test` cross-checks. The self-test extracts author surnames (word before initials or \"et al\"), bare names in the \"already cited\" parenthetical list, and \"X v. Y\" caption tokens; each must be listed, and each planted in a packet must fail the scan (planted mixed-case names must fail). Specimens in record-formats.md must pass scan_text too (state written as \"TX\").\n**Why:** T-077 r1 major: doc said \"add names before packets are built\" but nothing enforced it. T-077 r2 major: caption-only check let study authors (Brinjikji, Nakashima, Fraser, Vera) pass; Brinjikji/Nakashima had no initials, so only the citation-list rule sees them.\n**How to apply:** when adding a source, cite authors with initials or \"et al\" so the extractor sees them; run `python3 research/validate_library.py --self-test` and `python3 research/record_formats_check.py` before handing off research cards. Firm website slugs are listed by hand; ordinary-word firm names (Painter) are not listed."
}
````

### User / tool · 2026-11-02T03:54:10.709Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/research-workflow-pitfalls.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:11.417Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/MEMORY.md",
 "old_string": "- [Research workflow pitfalls](research-workflow-pitfalls.md) — separate git add/commit; pdftotext; TX docket/statute retrieval; denylist self-test rule",
 "new_string": "- [Research workflow pitfalls](research-workflow-pitfalls.md) — separate git add/commit; pdftotext; TX docket/statute retrieval; denylist self-test (author/citation-list/caption extraction)"
}
````

### User / tool · 2026-11-02T03:54:11.483Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:54:12.937Z

T-077 round 3 is in_review at commit 8d7548d: the denylist now covers every cited author surname, and the self-test extracts and checks them mechanically. Self-test and `validate_library.py` both pass, and planting `ElGhrably` and `Fraser S.G.` in a scratch packet makes the library scan exit 1. Firm-name coverage is limited to URL slugs and FAIR Health, a judgment call noted in the handoff.
