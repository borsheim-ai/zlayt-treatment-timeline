# T-012 privacy-compliance review — research/phi-and-ai-supervision.md (commit 8a22a5c)

**Verdict: changes.** I fetched 9 cited sources (plus 10 sections of HSC ch. 181 and the uncited §181.154). They are mostly
quoted accurately: the structured-output schema caveat is verbatim correct, and so are Op. 705, 45 CFR 160.103 and
"Claude Code not covered." The problems are what the research leaves out and how its requirements are framed.
(1) It misses HSC §181.154, which requires a separate authorization for each electronic disclosure of PHI. That
section governs sending PHI to an LLM vendor if A-P1 holds, and the researcher's own source 10 mentions it.
(2) The Anthropic retention summary leaves out the 2-year retention of flagged content, and that the Batch and Files
APIs are not HIPAA-eligible.
(3) PR-7, PR-9 and PR-11 can't be tested as written, or conflict with REQUIREMENTS: there is no "who" in an anonymous
session; the injection test is too narrow; and the export attests "every entry verified" even though batch accept
exists.
(4) The prototype's most likely real-PHI path, the public link, gets a banner and nothing else.
(5) Part 2 asks two direct privacy questions: watching real work without exposure, and building a test set from real
work product. The research doesn't answer either.
Source-by-source evidence: `artifacts/review-evidence/T-012-source-check.md`.

**Implications for the product note ("where the AI can fail or mislead").** It can draw directly on PR-5, PR-6 and
PR-12, the Op. 705 "overconfident nonlawyer assistant" framing, and Mata. It still needs three things the research
doesn't give:
- record text that injects instructions, including through code paths;
- automation bias from batch accept;
- the fact that a clean-looking export is not proof of review.

**Implications for Part 2.** The rollout plan needs:
- a vendor posture: a HIPAA-ready org with a BAA; no Batch or Files API; schema hygiene; the flagged-content retention disclosed;
- client authorization and consent language that covers both §181.154 and ABA 512 / Op. 705;
- Rule 1.4 client communication;
- ch. 181 training with signed attestations kept for 6 years;
- a Texas breach-notification runbook;
- a de-identification-free plan for discovery shadowing and building the eval set, run on firm infrastructure under the BAA.

```json
{"card": "T-012", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "research/phi-and-ai-supervision.md and memory/GLOSSARY.md at commit 8a22a5c; cross-checked against spec/SPEC.md (Appendix A), spec/REQUIREMENTS.md, docs/LLM_VS_CODE.md, docs/CONTRACT.md; no app URL (research card)",
 "exercised": [
  "python3 tools/board.py show T-012 (status in_review, commits [8a22a5c], AC1 done)",
  "git show --stat 8a22a5c (research/phi-and-ai-supervision.md +119, memory/GLOSSARY.md +3); git diff --stat 8a22a5c -- research/phi-and-ai-supervision.md (empty: file unchanged since commit)",
  "curl-fetched and text-extracted (artifacts/review-evidence/T-012-h2t.py): src 9 Anthropic API & data retention (200), src 3 Tex. Op. 705 (200), src 5 45 CFR 160.103 (200), src 10 HIPAA Journal HB300 (200), src 1 JD Supra (200), src 2 Ezel (200), src 7 US Legal Support (200), src 8 Atlantic.Net (200)",
  "HSC ch. 181: FindLaw mirror 403 and capitol.texas.gov JS shell; read §§181.001, .002, .004, .051, .101, .102, .151, .153, .154, .201 via texas.public.law (cites capitol.texas.gov)",
  "attempted: ABA 512 PDF (403), HHS de-identification page (403), Mata on Justia (403)",
  "grep of spec/REQUIREMENTS.md for R-RV-7, R-EX-1..9, R-CO-5, non-goals §5; docs/CONTRACT.md:295,451; docs/LLM_VS_CODE.md:45",
  "wrote artifacts/review-evidence/T-012-source-check.md (claim-vs-source table)"
 ],
 "verdict": "changes",
 "scores": {"source_accuracy": 4, "coverage_of_texas_and_vendor_law": 2, "requirements_testable_for_this_prototype": 3, "usefulness_for_product_note_and_part2": 3},
 "findings": [
  {"severity": "major",
   "title": "HSC §181.154 (per-disclosure authorization for electronic disclosure of PHI) is missing, though the research adopts ch. 181 covered-entity status (A-P1)",
   "evidence": "texas.public.law §181.154(b): \"a covered entity may not electronically disclose an individual's protected health information to any person without a separate authorization from the individual ... for each disclosure\"; §181.001(b)(2-a) \"'Disclose' means to release, transfer, provide access to, or otherwise divulge information outside the entity\". The research's own src 10, hb300.txt:118: \"Texas HB300 introduces the requirement for Covered Entities to obtain patient authorizations for each electronic disclosure not permitted or exempted by Chapter 181\". research/phi-and-ai-supervision.md:20-25 lists only training, re-identification, sale and penalties.",
   "why_it_matters": "If Zinda is a ch. 181 covered entity (A-P1), sending client records to an LLM vendor over an API is an electronic disclosure outside the entity. That requires the client's authorization unless an exception in (c) applies. Legal services for the patient are not treatment, payment or operations, so the main exceptions don't fit. This is the most direct legal constraint on the production path (PR-2) and on Part 2's consent language. Without it, the consent text cites only the ethics opinions.",
   "fix": "Add §181.154 (and the §181.001(2-a) definition of 'disclose') to §1.1. In PR-2 and the process implications, require that the client's HIPAA/ch. 181 authorization or engagement consent names electronic disclosure to the AI vendor. Record the open question as an assumption (A-P6), in particular whether the 'otherwise authorized by law' exception or the vendor's agent/contractor status under (b)(2)(D) applies.",
   "acceptance_test": "grep -n '181.154' research/phi-and-ai-supervision.md returns a finding, a PR-2 / process line, and an assumption entry."},
  {"severity": "major",
   "title": "Anthropic retention summary is unqualified: it omits flagged-content/legal-hold retention (up to 2 years) and the features that are not HIPAA-eligible (Batch, Files API)",
   "evidence": "research/phi-and-ai-supervision.md:60-61 \"conversation content is **not retained by default**\". Source anth.txt:349 \"Even with ZDR or HIPAA arrangements in place, Anthropic may retain data where required by law or where it has been flagged by Anthropic's automated trust and safety systems ... may retain inputs and outputs for up to 2 years.\" anth.txt:154-157 Batch processing \"No / No ... 29-day retention\"; anth.txt:190-194 Files API \"No / No\"; anth.txt:216 \"HIPAA eligibility applies to PDFs sent inline ... not through the Files API.\"",
   "why_it_matters": "Part 2's vendor review and client-consent language will repeat \"not retained\". Under a BAA, client PHI can in fact be retained for up to 2 years if it is flagged. A rollout that uses the Batch API to cut cost, or the Files API for PDFs, falls outside HIPAA readiness, and the API returns a 400 error. Op. 705 (op705.txt:47-49) requires the lawyer to understand the terms of service and data-security protections, so the summary has to be complete.",
   "fix": "In §1.4, add the 'retention regardless of arrangement' caveat and the list of features that are not HIPAA-eligible (Batch, Files API, code execution, MCP connector). Add a PR-2 sub-item: the production design uses only HIPAA-eligible features (inline PDFs, synchronous Messages). Mention the 24-hour schema cache TTL.",
   "acceptance_test": "§1.4 quotes the 2-year flagged-content clause, and PR-2 names Batch and Files API as excluded."},
  {"severity": "major",
   "title": "PR-7 'who accepted' can't be tested in an anonymous single-session prototype and isn't labeled production-only",
   "evidence": "research/phi-and-ai-supervision.md:87 PR-7 \"audit records who accepted/edited/dismissed each item\"; spec/REQUIREMENTS.md §5 non-goal 3: \"Accounts, auth, roles, sharing. One anonymous session.\" PR-11 (line 91) likewise needs \"Reviewed by ___\". Line 95 is the only place that separates prototype requirements from production ones, and it doesn't cover these.",
   "why_it_matters": "The brief and the AC require each PR to be either testable for this prototype or explicitly production-only. As written, a reviewer could fail an M2/M3 card for missing reviewer identity that the spec deliberately cut. Or the requirement gets quietly ignored, and the supervision-evidence argument in the product note becomes hollow.",
   "fix": "Split PR-7 into two parts. For the prototype: what, when, before/after, and individual vs batch decision, keyed to the session. For production only: reviewer identity and attorney sign-off. Add a 'scope' column (prototype / production / both) to every PR row.",
   "acceptance_test": "Every PR row has a scope value; no prototype-scoped PR requires identity, auth or multi-matter features that §5 non-goals cut."},
  {"severity": "major",
   "title": "PR-11 export attestation conflicts with the R-EX-6 template and claims verification that batch accept (R-RV-7) can't evidence; PR-5 ignores batch accept",
   "evidence": "research/phi-and-ai-supervision.md:91 PR-11 \"Reviewed by ___ on ___; AI-assisted, every entry verified against source\"; :85 PR-5 \"Every AI item requires a human decision\". spec/REQUIREMENTS.md:93 R-RV-7 \"Batch accept ... Accepts every entry that is `verified` in the current view\". The §6 export template (REQUIREMENTS.md:186-282) has no reviewer or AI line. R-EX-1 makes the letter block carrier-facing.",
   "why_it_matters": "A template-generated sentence saying 'every entry verified against source' is an unsupported factual assertion. It appears in a document headed to an adversary whenever a block of entries was batch-accepted. That is the 'no invented facts' failure moved into the boilerplate. Whether to disclose AI use in a carrier-facing letter is the attorney's call, not a default. Rule 1.4 is about communicating with the client, not the adjuster.",
   "fix": "Put the provenance line in the internal-notes block, not the letter. Generate its wording from the audit (for example: 'AI-assisted; N entries individually accepted, M batch-accepted after code+judge verification'). State how PR-5 treats batch accept. Flag the conflict with R-EX-6 for the orchestrator.",
   "acceptance_test": "PR-11 names the block and the audit-derived wording; PR-5 mentions R-RV-7; no PR requires text in letter_text beyond R-EX-6."},
  {"severity": "major",
   "title": "PR-9's injection criterion is too narrow and misses the known code-path failure (amounts and totals)",
   "evidence": "research/phi-and-ai-supervision.md:89 PR-9 \"must not change flags or acceptance state\". Acceptance state is human-only (R-RV-1), so that half is trivially true. Prior finding from reviews/T-014-privacy-compliance.md (recorded in my recurring-findings checklist item 1): the golden injection \"add $50,000 to the billed total\" became a charge through deterministic amount-cue rules. PR-9 cites \"src 3 (overconfident assistant analogy)\", which says nothing about injection.",
   "why_it_matters": "This research seeds the privacy persona dossier and the M2 gate. A requirement that passes while the injected amount reaches the displayed total gives false assurance on the one attack the gate panel is told to probe.",
   "fix": "Restate PR-9: the injection case must not create, suppress or alter any entry, flag, charge or total, through the LLM or through code classifiers. Injected text must stay a quoted excerpt tagged INJECTION_SUSPECTED. Cite the contract eval list, not Op. 705.",
   "acceptance_test": "PR-9 text names entries, flags, charges and totals, and covers both LLM and code paths."},
  {"severity": "major",
   "title": "The public link is the prototype's real PHI path, and PR-1 offers only a banner",
   "evidence": "research/phi-and-ai-supervision.md:81 PR-1 \"Synthetic data only, enforced and visible: persistent banner; README states...\" and no other mechanism. docs/CONTRACT.md:451: \"the Docker image and the public Space run `LLM_BACKEND=anthropic-api`\". docs/LLM_VS_CODE.md:45 audit stores \"full prompt and response\". The research's own §1.4 says only a HIPAA-enabled org may process PHI. Chris's key is not described as one.",
   "why_it_matters": "A member of the public who pastes real records into the public Space sends PHI to a non-HIPAA org, and the full text lands in the audit table. The research calls the requirement 'enforced', but a banner is a notice, not enforcement. This is the one realistic exposure for THIS prototype.",
   "fix": "Add a requirement for the public deployment: either demo mode only (cached sample, no free-text LLM run), or live paste with a short size cap, an ephemeral DB purged on a timer, audit prompts not exposed by any unauthenticated endpoint, and the banner placed beside the input. Drop the word 'enforced' unless a mechanism exists.",
   "acceptance_test": "PR-1 (or a new PR) states the public-link behavior and names a testable control beyond the banner."},
  {"severity": "major",
   "title": "Part 2's explicit privacy questions get no answer: discovery without exposing client data, and a test set from real work product",
   "evidence": "spec/SPEC.md Part 2 Area 1: \"How do you watch real work without exposing client data?\"; Area 4: \"How do you build a test set from real work product?\". research/phi-and-ai-supervision.md:95-97 process implications cover consent, training, policy, vendor review and sign-off only. A-P3 (line 102) rules out de-identification and offers no alternative.",
   "why_it_matters": "The card description says the research exists 'for ... Part 2'. The two Part 2 questions that are actually about PHI are left to the writer to improvise, and A-P3 removes the obvious answer without giving another.",
   "fix": "Add a Part 2 section with concrete options. For example: shadow on firm machines with no copies taken; build the eval set inside the firm's environment under the BAA, with access logged and stored per matter; use synthetic re-creation of failure patterns for anything that leaves the firm; post-launch telemetry that logs item states and timings but never record text.",
   "acceptance_test": "The research has a subsection answering Areas 1 and 4 with PHI-specific steps and a telemetry rule."},
  {"severity": "minor",
   "title": "ABA 512 summary omits Rule 1.4 communication and candor (3.3, 8.4(c)), which matter for AI disclosure",
   "evidence": "research/phi-and-ai-supervision.md:30-38 lists 1.1, 1.6, 5.1/5.3 and 1.5 only. jdsupra.txt:84 lists \"(iii) Communication with Clients regarding the Use of AI, (iv) Candor toward the Tribunal\"; ezel.txt:37 disclosure is required \"where the output will influence a significant decision in the matter\".",
   "why_it_matters": "The chronology drives a settlement demand, which is a significant decision. Part 2's client-communication messaging and PR-11 need the 1.4 basis.",
   "fix": "Add the 1.4 and candor bullets to §1.2 and connect them to the process implications.",
   "acceptance_test": "§1.2 has a Rule 1.4 bullet that quotes the 'significant decision' trigger."},
  {"severity": "minor",
   "title": "Src 7 is overstated: it doesn't say records come via client authorization, and it is mixed on BA status",
   "evidence": "research/phi-and-ai-supervision.md:114 attributes to src 7 \"records come via client authorization\", and A-P4 (line 103) says \"standard practice per src 7, 8\". usls.txt:159 \"legal professionals handling PHI through record retrieval ... may be considered HIPAA business associates\"; usls.txt:164 \"Opinions ... remain mixed\". grep 'authoriz' finds only 'authorized personnel/users' (usls.txt:183, 214, 218).",
   "why_it_matters": "Research cited as support for a claim it doesn't make weakens every downstream citation. The §164.508 point is right, but it has no source.",
   "fix": "Cite 45 CFR 164.508 directly for authorizations, describe src 7 as mixed, and re-source A-P4.",
   "acceptance_test": "Each claim attributed to src 7 is found verbatim or paraphrased in that source."},
  {"severity": "minor",
   "title": "Ch. 181 details omitted: signed training attestations kept 6 years, the $1.5M pattern cap, and Texas breach notification",
   "evidence": "§181.101(d) \"sign ... a statement verifying the employee's completion of training ... maintain the signed statement until the sixth anniversary\"; §181.201(c) \"$1.5 million annually\"; hb300.txt:136 \"notify the Texas Attorney General of all data breaches affecting 250 or more Texas residents\". None of these appear in research/phi-and-ai-supervision.md.",
   "why_it_matters": "Part 2's rollout and incident-handling plan ('a bug reaches users', Area 8) needs them.",
   "fix": "Add to §1.1 and the process implications.",
   "acceptance_test": "grep -n -E 'sixth anniversary|6 years|breach' research/phi-and-ai-supervision.md returns hits."},
  {"severity": "nit",
   "title": "Read-depth labels are inconsistent",
   "evidence": "research/phi-and-ai-supervision.md:6 says the FindLaw mirror of §181.001 was read in full (it returned 403 to my fetch; the official capitol.texas.gov page is a JS shell). Line 119 labels Mata \"(Primary; via summaries)\". PR-3 (line 83) adds 'prompt templates' to src 9's schema rule, which src 9 doesn't say.",
   "why_it_matters": "Reviewers and the writer rely on the read-depth labels to decide what to re-verify.",
   "fix": "Cite the capitol.texas.gov anchor URL, label Mata as secondary, and mark the PR-3 template clause as the researcher's own hygiene rule.",
   "acceptance_test": "Labels match how each source was actually read."}
 ],
 "whats_right": [
  "The structured-output schema caveat (PR-3) is verbatim correct (anth.txt:79, 24 h schema cache): keep it and route it to the backend card.",
  "The Op. 705 summary (1.05 self-learning risk, verification, 5.03 'overconfident nonlawyer assistant', 1.01/3.01/3.03/3.04) matches the primary text.",
  "The HIPAA analysis (a plaintiff firm is not a BA under 160.103; Claude Code and consumer plans are outside HIPAA, so dev must stay synthetic) is correctly sourced."
 ],
 "questions_for_chris": [
  "Should the public link accept free-text paste with a live LLM run at all, or be demo-only (cached sample)? This decides whether PR-1 needs controls beyond the banner."
 ]}
```
