# T-012 privacy-compliance review, round 2 — research/phi-and-ai-supervision.md (commit 4924221)

**Verdict: changes.** All 7 round-1 majors were addressed, and 6 are fully resolved. I re-fetched the sources and the
new statutory text is quoted accurately: §181.154 (a)-(d), §181.101(d) six-year attestations, the §181.201 penalty
tiers and $1.5M cap, and §521.053 (individuals within 60 days; AG within 30 days for 250 or more residents, via the
online form, per S.B. 768). The Anthropic 2-year flagged-content clause, the list of ineligible features, the
inline-PDF rule and the 24 h schema cache are verbatim correct. The per-finding table is in
`artifacts/review-evidence/T-012-r2-resolution.md`.

Three new majors remain:
1. **§1.4 still overstates default retention.** "Not retained by default" is a design principle on the ZDR/HIPAA
   page. That page itself defers standard retention to the commercial policy, which says API inputs and outputs are
   deleted "within 30 days". The doc then prescribes this wording for client consent. I missed this in round 1.
2. **The §181.154 fallback doesn't match the text it quotes.** The statute requires a "separate authorization ...
   for **each** disclosure". PR-2a proposes one matter-level authorization "before the first LLM call" and does not
   flag that gap. PR-2a also drops the (a) notice.
3. **PR-1, PR-1a and §3.1 predate D-020 and now conflict with it.** Demo POST must reject non-fixture text and
   **not store** it. Live mode is local-only. There is no in-app spend ledger, yet the PR-1 control and §3.1 rely on
   one.

Minors:
- A-P6 misreads §181.001(b)(2)(D).
- Remote screen share is itself an electronic disclosure of PHI.
- The provenance claim about Appendix A is unsupported.
- The breach runbook omits the §521.053 trigger and the vendor duty in (c).

**Product note implications.** The vendor-retention sentence must read: "deleted within 30 days by default; longer
under the Usage Policy or for flagged content (up to 2 years); zero retention only by org agreement".

**Part 2 implications.** The consent and authorization packet needs counsel's answer on how §181.154's "each
disclosure" applies to repeated API calls and eval runs. It also needs the (a) notice.

```json
{"card": "T-012", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "research/phi-and-ai-supervision.md at 4924221 (diff since 8a22a5c); decisions D-001..D-022 in memory/ORCHESTRATOR_DECISIONS.md; spec/SPEC.md Part 2 Areas 1 and 4; evals/golden/case_07; no app URL (research card)",
 "exercised": [
  "python3 tools/board.py show T-012 (status in_review, rounds 1, commits [8a22a5c, 4924221])",
  "git diff --stat 8a22a5c -- research/phi-and-ai-supervision.md -> '1 file changed, 219 insertions(+), 99 deletions(-)'; git log dates: 4924221 18:40:21, a399a4c (D-019..D-022) 18:51:24",
  "python3 -I artifacts/review-evidence/T-012-r2-fetch.py <scratchpad>: s154 200, s101 200, s201 200, s001 200, s521 200, Anthropic API & data retention 200, Cornell 164.508 200, Tex. Rule 4.01 200, Ezel 512 200, JD Supra 200, FindLaw 181.001 403",
  "curl privacy.claude.com/en/articles/7996866 (200) and texas.public.law §521.002 (200); text-extracted with artifacts/review-evidence/T-012-h2t.py",
  "grep of the research doc for 181.154 / retain / compliant / 30 days; grep of the repo for INJECTION_SUSPECTED vs instruction_like_text",
  "python3 tools/check_secrets.py -> 'check_secrets: ok (181 file(s) scanned)'",
  "read spec/SPEC.md:17,53,81,84; evals/golden/case_07_prompt_injection.expected.json:6,235-238; decisions D-001,D-005,D-008,D-009,D-011,D-016,D-020",
  "wrote artifacts/review-evidence/T-012-r2-resolution.md (round-1 resolution table with source line refs)"
 ],
 "verdict": "changes",
 "scores": {"source_accuracy": 4, "coverage_of_texas_and_vendor_law": 4, "requirements_testable_for_this_prototype": 4, "usefulness_for_product_note_and_part2": 4},
 "findings": [
  {"severity": "major",
   "title": "§1.4 'Defaults: not retained by default' contradicts Anthropic's commercial API retention policy (30 days), and the doc prescribes it as client-consent wording",
   "evidence": "research/phi-and-ai-supervision.md:103 \"Defaults. Conversation content (prompts and outputs) 'is not retained by default'\"; :110 consent and vendor review \"must say 'not retained by default, with retention of up to 2 years ...'\". The source page, anth.txt:35, says: \"Anthropic offers two data handling arrangements ... ZDR and HIPAA readiness ... For Anthropic's standard retention policies outside these arrangements, see the commercial data retention policy\". The quoted line (anth.txt:39) sits under 'How Anthropic approaches data retention'. privacy.claude.com/en/articles/7996866, priv.txt:18: \"For Anthropic API users, we automatically delete inputs and outputs on our backend within 30 days of receipt or generation, except: ... Files API ... zero data retention agreement ... to enforce our Usage Policy\".",
   "why_it_matters": "Checklist item 9 says to state vendor retention accurately and make no stronger claim. This sentence will go into client consent (PR-2, §3.3) and the product note. For a standard org, such as Chris's key in local live mode, or a HIPAA org without ZDR, it understates retention. Op. 705 requires the lawyer to understand the vendor's terms. I missed this in round 1, when I asked only for the 2-year caveat.",
   "fix": "Rewrite §1.4 'Defaults': 'Standard commercial API: inputs and outputs deleted within 30 days (src: privacy.claude.com 7996866), longer for the Files API, under Usage Policy enforcement, or legal hold; flagged content up to 2 years; zero retention only under an org-level ZDR agreement; Covered Models require 30 days.' State what retention a HIPAA-enabled org without ZDR gets, or mark it as unknown and to be confirmed in the BAA. Change the prescribed consent wording at :110 to match, and add the commercial-retention article as a source.",
   "acceptance_test": "grep -n 'not retained by default' research/phi-and-ai-supervision.md returns no line presented as the standard API default; §1.4 cites the 30-day commercial default and its source."},
  {"severity": "major",
   "title": "The §181.154 fallback (one matter-level authorization) doesn't address the statute's 'separate authorization ... for each disclosure', and PR-2a drops the (a) notice",
   "evidence": "s154.txt:20 (b): \"may not electronically disclose ... without a separate authorization from the individual ... for each disclosure\"; s154.txt:16 (a) notice by posting at the place of business or on the website. research/phi-and-ai-supervision.md:54-56 A-P6: \"get the client's written authorization naming electronic disclosure to the AI vendor ... keep it on file\"; :142 PR-2a control: \"authorization on file before the first LLM call for the matter\"; §3.2:180-181 eval runs rely on the same authorization. Neither PR-2a nor §3.3 mentions the (a) notice.",
   "why_it_matters": "Each extraction run, re-run and eval run sends PHI to the vendor. Whether one signed authorization can cover a defined series of disclosures is exactly what counsel must decide. As written, Part 2 will present a single engagement-packet form as satisfying a per-disclosure rule. That is a compliance claim the quoted text does not support. The persona asks; it does not decide (dossier §9). The research has to surface the question, not silently answer it.",
   "fix": "In A-P6 and PR-2a, state the open question: does one authorization that names the vendor, purpose and duration, covering all disclosures for this matter, satisfy 'for each disclosure', or is per-run authorization needed? Note the AG standard form in (d). Add the (a) notice (website or office posting) to PR-2a and §3.3. Say whether eval use on closed matters (§3.2) needs a separate authorization.",
   "acceptance_test": "A-P6 or PR-2a contains the phrase 'for each disclosure' with the open question routed to counsel; PR-2a or §3.3 names the §181.154(a) notice."},
  {"severity": "major",
   "title": "PR-1, PR-1a and §3.1.4 conflict with D-020: public live mode, a spend-counter control that no longer exists, and no 'reject and do not store' requirement",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:28 D-020: \"POST /api/cases in demo mode accepts only text whose normalized hash ... equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter\". research/phi-and-ai-supervision.md:138 PR-1 control \"paste text -> no LLM call (audit/spend counter unchanged)\"; :139 PR-1a \"If live mode is ever enabled\" (public); :174 \"D-008 already separates the spend counter\". `git log`: 4924221 at 18:40:21, a399a4c (D-019..D-022) at 18:51:24.",
   "why_it_matters": "D-020 binds. Refusing the LLM run is not enough if the pasted text is still persisted at create time (recurring finding: demo-only is not store-nothing). PR-1's control would pass while a stranger's pasted records sit in the Space's DB. A PR-1a reader could also build public live mode, which D-020 forbids.",
   "fix": "PR-1: 'demo POST accepts only fixture-hash text; anything else returns an error and writes nothing (no case, record, audit or log row)'. Control: E2E posts non-fixture text, then asserts the DB row counts are unchanged and no record text appears in logs. PR-1a: re-scope to local live mode only and drop the public live mode case. Replace the spend-counter references with 'provider-side spend limit (README)'.",
   "acceptance_test": "PR-1 names 'not stored' and a row-count-unchanged test; no PR or §3 line mentions an in-app spend counter or public live mode."},
  {"severity": "minor",
   "title": "A-P6 argument (i) misreads §181.001(b)(2)(D): it makes a contractor a covered entity in its own right; it does not put the contractor inside the firm",
   "evidence": "s001.txt:23 (D): a covered entity includes any person who \"is an employee, agent, or contractor of a person described by Paragraph (A), (B), or (C) insofar as ... \"; s001.txt:24 (2-a): \"outside the entity holding the information\". research/phi-and-ai-supervision.md:52-53: \"The vendor is the firm's contractor or agent, so it falls inside the covered entity ... then no disclosure 'outside the entity' happens.\" (My round-1 fix invited this argument without stating it precisely.)",
   "why_it_matters": "The argument is presented as one of two outs from per-disclosure authorization. On the text, it is weak: the vendor becomes a ch. 181 covered entity of its own, and (c)(1) lets one covered entity disclose to another only for treatment, payment or operations.",
   "fix": "Restate (i) accurately: '(2)(D) makes the vendor itself a covered entity; whether a transfer to one's own contractor is a disclosure \"outside the entity holding the information\" is unresolved.' Keep it as an open question for counsel.",
   "acceptance_test": "The A-P6 text no longer says the vendor 'falls inside the covered entity'."},
  {"severity": "minor",
   "title": "§3.1 option 2 (remote screen share) is itself an electronic disclosure of PHI to a non-employee through a conferencing vendor; hiding name, DOB and claim number is not de-identification",
   "evidence": "research/phi-and-ai-supervision.md:165-167 \"Screen share with redaction ... client name, DOB and claim number hidden ... The PM sees structure ... not identities.\" The research's own A-P1/A-P6 (:48-53, :216) treats any electronic transfer of PHI outside the firm as a §181.154 disclosure. Safe Harbor (src 11) also removes all date elements and provider-identifying detail, which remain visible.",
   "why_it_matters": "Area 1 asks how to watch work 'without exposing client data'. This option exposes it, through a third-party video platform, to someone outside the firm, and the doc doesn't say so.",
   "fix": "Either drop option 2 or condition it: firm-controlled conferencing under the firm's vendor terms, the PM under A-P7, and a note that it counts as a disclosure under the research's own A-P6 analysis. Prefer in-person option 1.",
   "acceptance_test": "§3.1 option 2 names its disclosure status and conditions, or is removed."},
  {"severity": "minor",
   "title": "Unsupported provenance claim: 'This is how Appendix A's case was built'",
   "evidence": "research/phi-and-ai-supervision.md:171. spec/SPEC.md:53 says only \"Fictional case: Jordan Rivera ... intentionally imperfect, like real ones\". No source says the case was replicated from a real matter.",
   "why_it_matters": "It is an invented fact in a research doc. It also implies the repo fixture derives from real client records, which is the one thing this repo must never suggest.",
   "fix": "Replace it with 'the same approach as Appendix A's fictional sample' or delete the sentence.",
   "acceptance_test": "grep -n \"how Appendix A\" research/phi-and-ai-supervision.md returns nothing."},
  {"severity": "minor",
   "title": "Breach runbook omits the §521.053 trigger (unauthorized acquisition) and the vendor's duty in (c) to notify the owner",
   "evidence": "s521.txt (a): \"'breach of system security' means unauthorized acquisition of computerized data ...\"; (c): a person maintaining data it does not own \"shall notify the owner ... immediately after discovering the breach\". research/phi-and-ai-supervision.md:201-203 treats 'PHI goes to ... a non-HIPAA org or a log aggregator' as going straight to notice.",
   "why_it_matters": "Area 8's incident plan needs the assessment step: does a misdirected send count as 'acquisition by an unauthorized person'? It also needs the vendor's contractual duty to notify the firm in the vendor review.",
   "fix": "Add the (a) definition as the assessment test and 'vendor must notify the firm immediately (§521.053(c)); put it in the BAA or vendor terms review' to §3.3 and PR-2.",
   "acceptance_test": "§3.3 cites §521.053(a) and (c)."},
  {"severity": "nit",
   "title": "PR-9 tag vocabulary and test naming",
   "evidence": "research/phi-and-ai-supervision.md:150 uses `INJECTION_SUSPECTED` and 'plus an amount-injection case'. evals/golden/case_07_prompt_injection.expected.json:235 uses warning type `instruction_like_text`, and :6 already covers '$50,000 out of every total'.",
   "why_it_matters": "A tester grepping for PR-9's tag will not find it in the golden.",
   "fix": "Name both tags (REQUIREMENTS / lexicon `INJECTION_SUSPECTED`, golden `instruction_like_text`; D-013 `record_warning`) or point to case_07 as the amount case.",
   "acceptance_test": "PR-9's control names case_07's warning type."}
 ],
 "whats_right": [
  "The scope column and the PR-7a/7b and PR-1b 'notice, not a control' split make every PR row testable or explicitly production-only. Keep that structure.",
  "PR-9 and PR-11 now match D-005, D-001 and D-009 exactly: LLM and code paths, all four effects, and an audit-derived internal-notes line that never says 'verified'.",
  "The new statutory text (§181.154, §181.101(d), §181.201, §521.053 after S.B. 768) is quoted accurately, and the stale 60-day AG figure in src 10 is correctly overridden."
 ],
 "questions_for_chris": []}
```
