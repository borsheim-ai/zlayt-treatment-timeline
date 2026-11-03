# T-219 — litigation-lead review (Part 2 rewrite, commit 7544137)

Reviewer: litigation-lead-reviewer (Bob Kessler, fictional plaintiff PI partner who signs the demands), fresh context, model claude-opus-5-5.

**Verdict: fail.** The voice is right, the questions to me are good ones, and the go/no-go shows real understanding of what a wrong line costs with an adjuster. Three things would still stop me trusting this PM with my matters.

1. The paralegal sessions have a paralegal pick a former client's file and show it to an outside PM, and the PM brings a chronology "from a closed matter" that his tool produced. All of this happens before anyone at the firm approves it, and "I won't copy or record anything" is offered as the confidentiality safeguard. Texas Rule 1.05(b)(1) applies to former clients too and has no "nothing was copied" exception.
2. The go/no-go says my reading the internal notes "is the verification Texas Opinion 705 expects." That is narrower than what 705 says.
3. The go/no-go asks for live matters but reports only the good numbers. It leaves out library recall (entries 0.775, amounts 0.681), which is the same figure the product note gives as the reason not to go live.

**What I exercised (commands run and their output):**
- `git log --oneline -5` → HEAD `7544137 docs(writer): T-219 Part 2 in Chris's voice ...`; `git diff --stat 7544137 HEAD -- submission/part2-process.md` → empty (the file under review matches HEAD).
- `git show 7544137:submission/part2-process.md | cat -n`: read all 190 lines as the lawyer receiving these messages.
- `python3 tools/board.py show T-219`: AC, handoff, writer notes.
- `submission/product-note.md` (to check consistency with the ship call); `evals/reports/library-latest.md` (library recall per packet, plus 7 amount-type must_not hits at a74b727, pre-billing redesign); `evals/library/*.expected.json` (what each must_not hit was: all `amount_value`, none diagnosis or causation).
- Primary sources fetched with curl into `artifacts/review-evidence/T-219-op705.html` and `T-219-r105.html`: Texas Op. 705 ("a lawyer should always verify the accuracy of any responses received from a generative AI tool"; "Cf. Rule 5.03"; Op. 680 precautions including reviewing "terms of service"; "may need to secure client consent") and Texas Rule 1.05(b)(1) ("Reveal confidential information of a client or a former client to ... anyone else, other than the client, the clients representatives, or the members, associates, or employees of the lawyers law firm"), (c)(1)–(2).
- `personas/litigation-lead.md` (checklist items 13, 14, 15, 20) and my memory file `feedback_texas_law_checks.md`.

**Out of my lens:** page count and PDF layout, PM-craft structure, and the engineering sections (area 8), except where they make a claim to a lawyer.

```json
{"card": "T-219", "persona": "litigation-lead-reviewer", "model": "claude-opus-5-5",
 "scope": "submission/part2-process.md at commit 7544137 (identical to HEAD); cross-checked against submission/product-note.md and evals/reports/library-latest.md; no app run (document review)",
 "exercised": [
   "git log --oneline -5 -> 7544137 at HEAD; git diff --stat 7544137 HEAD -- submission/part2-process.md -> no diff",
   "git show 7544137:submission/part2-process.md | cat -n (full read, 190 lines)",
   "python3 tools/board.py show T-219 (AC, handoff)",
   "read submission/product-note.md lines 1-45 (ship call: shadow, not live matters, until library recall meets bar)",
   "read evals/reports/library-latest.md and evals/library/*.expected.json (7 must_not hits, all amount_value)",
   "curl Texas Op. 705 -> artifacts/review-evidence/T-219-op705.html; curl Texas Rule 1.05 -> artifacts/review-evidence/T-219-r105.html; extracted verify / Cf. 5.03 / terms of service / client consent / 1.05(b)(1),(c) text",
   "grep of part2 at 7544137 for closed matter, client data, Opinion 705, 0.775, 0.681, 4.01, Stowers"
 ],
 "verdict": "fail",
 "scores": {"kickoff_and_questions_for_lead": 4, "go_no_go_supervision_and_ethics": 2, "paralegal_engagement": 4, "client_data_protection": 1, "tone": 5, "trust_with_my_matters": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Paralegal sessions expose former-client files to an outside PM without attorney approval; 'I won't copy anything' is offered as the safeguard, and the tool has already run on a closed matter",
   "evidence": "part2-process.md:37 heading '**Watching real work without client data.**' followed by 'She works on her own machine on a closed matter. I watch, copy nothing, record nothing. If the firm wants more distance, she redoes a closed matter from a redacted copy'; :145 to a paralegal: 'Pick a closed matter and build it the way you normally do while I watch. I won't copy or record anything.'; :149 'This one's from a closed matter. I planted five mistakes in it, mixed in with whatever the tool got wrong on its own.'; :151 'that no client data leaves your machine'. Compare :73, where the test set requires 'the attorney approves them', and :131, which asks whether the tool may run on closed matters at all. Texas R. 1.05(b)(1): a lawyer shall not knowingly 'Reveal confidential information of a client or a former client to ... anyone else, other than the client, the clients representatives, or the members, associates, or employees of the lawyers law firm' (artifacts/review-evidence/T-219-r105.html).",
   "why_it_matters": "A closed file is still a former client's confidential information. Showing it on screen to someone outside the firm is a disclosure whether or not anything is copied. The paralegal message lets my nonlawyer staff decide that disclosure, and the find-the-error printout means a former client's records went through the tool, and onto paper the PM carries, before the founder question at :131 was even asked. A partner who reads this asks who approved it. The doc's own heading ('without client data') contradicts its content. This misstates the confidentiality duty and the supervision duty, which makes it a blocker under this brief.",
   "fix": "Default to de-identified or synthetic records for observation and for the find-the-error exercise. A real closed matter is used only after the responsible attorney picks and approves it, the observer is under a written confidentiality agreement with the firm, and client consent is obtained where the attorney decides 1.05(c) requires it. Have the paralegal message say 'the matter [attorney] cleared for this' instead of 'Pick a closed matter'. Have :149 say the chronology came from a de-identified or synthetic packet, or from the attorney-approved shadow set after :131 is answered. Retitle :37 to something true, e.g. 'Watching real work, with the attorney's sign-off'.",
   "acceptance_test": "grep of part2 shows no instruction to a paralegal to choose a client matter. Every use of a real closed matter names attorney approval and the confidentiality agreement. No tool output from a real matter appears before the step that approves running the tool on real matters. The heading at :37 does not say 'without client data' while the text describes viewing a client file."},
  {"severity": "blocker",
   "title": "Go/no-go equates 'you read the internal notes' with 'the verification Texas Opinion 705 expects'",
   "evidence": "part2-process.md:106 'You read those notes before any letter it helped with goes out, as you'd check a new paralegal's work; that's the verification Texas Opinion 705 expects.' Op. 705 (artifacts/review-evidence/T-219-op705.html): 'a lawyer should always verify the accuracy of any responses received from a generative AI tool ... lawyers are responsible for the work product they submit regardless of who (or what) does the original research and drafting.'",
   "why_it_matters": "This is the message that tells me what I am agreeing to supervise, and it shrinks my duty to reading the warnings list. Op. 705 expects me to verify the accuracy of AI output in work product I send. My paralegals' per-line accepts are part of that under my supervision (the opinion's 'Cf. Rule 5.03' analogy), but reading the notes is not verifying the letter lines I sign. A PM who tells a signing attorney that the opinion is satisfied by less than it says loses the attorney, and it is a misstatement of the ethics duty.",
   "fix": "Describe the actual supervision and stop labeling it as compliance. For example: 'Before any letter it helped with goes out, you read the internal notes and check the letter lines against their quotes, all of them at first and then a sample we agree on, the way you would check a new paralegal's work. Op. 705 says you must verify AI output, not rely on it blindly. This is how we make that practical; you decide whether it's enough.'",
   "acceptance_test": "Line :106 no longer says reading the notes is 'the verification Op. 705 expects'. It names the attorney checking letter lines against source quotes, and it frames Op. 705 as 'verify, don't rely blindly', matching the fetched text."},
  {"severity": "blocker",
   "title": "Go/no-go and ship-bar table report only favorable numbers; omit the below-bar library recall that the product note says blocks live use",
   "evidence": "part2-process.md:101-103 lists grounding 242/242, 40/40 caught, 0 diagnosis/cause statements and 'The weak spot: on 15 unfamiliar packets it raised 34 of 42 warnings'. It does not mention entry recall 0.775 or amount recall 0.681 on the same 15 packets. :82 ship-bar row 'Recall | 95% of golden entries and amounts | 0.982 and 1.000' gives golden only, while the Flags row (:83) does show the library 0.81. submission/product-note.md:21: 'Meets the bar on golden, below it on the library (0.775, 0.681, 0.81). So: stage-0 shadow ... not live matters, until library recall meets the bar.' evals/reports/library-latest.md: amounts 2/3, 3/7, 2/5, 5/9, 4/8, 3/5, 4/7 on seven packets.",
   "why_it_matters": "A go/no-go to the signing attorney has to give me the number that would make me say no. On unfamiliar records the tool found about two-thirds of the charges. That is an under-demand risk on every matter where a paralegal trusts it. The message names one weak spot and leaves out the bigger one, and it asks for live matters on numbers that the PM's own product note says do not support live matters. If I found that out after saying yes, I would not take another go/no-go from this PM at face value. It is the same reason an adjuster discounts a chronology that hides the gap.",
   "fix": "Add one bullet to :101-104, e.g. 'On unfamiliar packets it found 78% of treatment entries and 68% of charges, so she still reads every bill and the notes list bills to request.' Make the stand-in numbers either meet the bar or state that with Part 1's numbers the answer would be no-go. Add the library recall to the :82 row the same way :83 does for flags.",
   "acceptance_test": "The go/no-go message contains every ship-bar metric that misses its bar (entries, amounts, flags on library). Row :82 shows golden and library recall. The message's ask is consistent with product-note.md:21."},
  {"severity": "major",
   "title": "Kill threshold tolerates one unsupported fact reaching a carrier",
   "evidence": "part2-process.md:114 Output quality, Kill if: 'two unsupported facts reach a carrier'; compare :106 'One unsupported fact in a draft you review, and we pause.'",
   "why_it_matters": "A statement in a demand that no record supports is the bad day this whole project exists to prevent: a Rule 4.01 exposure if it is knowing, and a credibility hit that the adjuster remembers on the next file. The table reads as if the first one that reaches a carrier is tolerated. Pausing at one in a draft and killing at two at the carrier leaves the one-at-the-carrier case undefined.",
   "fix": "Kill if: 'one unsupported fact reaches a carrier'. Also state the response: stop the pilot, notify the signing attorney the same day, and the attorney decides whether and how to correct it with the carrier.",
   "acceptance_test": "Row :114 kill threshold is one fact reaching a carrier, and the doc names the same-day attorney notification."},
  {"severity": "major",
   "title": "Confidentiality controls for live matters and the real-work test set are incomplete; client-data decisions sit with founders, not the responsible attorney",
   "evidence": ":73 test set controls are 'the attorney approves them; they never leave Zinda's environment; access is logged', with nothing about the model vendor's terms (no training, retention), de-identification where practical, or client consent. :106 'What you're agreeing to supervise' has no word on where live client records go or on vendor terms. :125 'A founder decides: ... any real client data in any environment'. Op. 705 precautions (T-219-op705.html): 'reviewing and potentially renegotiating the \"terms of service\"', 'may need to secure client consent'.",
   "why_it_matters": "Stage 1 sends live client medical records to an LLM. The signing attorney is the one who has to decide that this is a permitted use of confidential information (Op. 705 / ABA 512: vendor terms, data security, consent). The go/no-go never asks him to. The decision table also routes 'real client data' to the founders. Persona checklist 14 lists these controls as the condition for an acceptable real-work test set.",
   "fix": "Add to :73 'model vendor terms reviewed (no training on our data, retention limits), de-identified where practical, client consent where the attorney decides it's required'. Add one line to the go/no-go: 'Live records go to [vendor] under terms you've reviewed: no training, [N]-day retention. Your call whether our engagement letters cover this.' In :125, make real client data a joint decision of the responsible attorney and a founder.",
   "acceptance_test": "Test-set paragraph names vendor terms, de-identification, and consent. The go/no-go names where live data goes and asks the attorney to approve it. The :125 table gives the attorney the client-data decision."},
  {"severity": "minor",
   "title": "No tie to Rule 4.01 or Stowers deadlines (checklist 20)",
   "evidence": "grep of part2 at 7544137 for '4.01' and 'Stowers': no matches. The carrier/adjuster framing is present (:15, :127, :171).",
   "why_it_matters": "The no-invention rule matters to me because these are statements to a third person (Rule 4.01) and because a time-limited demand has to be right before its deadline. Blank service dates (D-073) add paralegal time exactly when a Stowers clock is running. A PM who names that understands my calendar.",
   "fix": "One clause in area 2 or 5, e.g. 'A demand is a statement to the carrier, and on a Stowers deadline there's no second draft, so a blank beats a wrong date.' Add Stowers-deadline matters to the stage-1 watch list.",
   "acceptance_test": "Part 2 mentions statements to the carrier/Rule 4.01 and Stowers or time-limited demands at least once, accurately."},
  {"severity": "nit",
   "title": "'she' in the go/no-go is ambiguous with two paralegals",
   "evidence": ":103 'so she still reads the records'; :104 'for her to fill'; stage 1 is 'two paralegals' (:99, :106).",
   "why_it_matters": "In a message asking me to approve two people, 'she' reads as one unnamed paralegal.",
   "fix": "Use 'they' or 'each paralegal'.",
   "acceptance_test": "The go/no-go uses no unexplained 'she'."}
 ],
 "whats_right": [
  "The three questions for the lead (:31-33) are ones I'd answer, especially 'what did it cost? Days, or dollars off the offer?' and 'What will you never let software write in a letter?'",
  "Blank service dates over wrong ones, and 'warnings stay in internal notes, never with the carrier': this PM understands a wrong date costs every other line.",
  "Tone is right for a partner: short, direct, a clear ask with a deadline ('Yes, no, or \"yes, but\" by Thursday?'), and honest about the persona-only 4/5 (:87)."
 ],
 "questions_for_chris": [
  "Is Zlayt's PM treated as part of Zinda Law Group (an affiliate or retained vendor under the firm's confidentiality agreement)? If so, say it once in area 1. It changes how a lawyer reads the observation sessions, though attorney approval is still needed."
 ]}
```
