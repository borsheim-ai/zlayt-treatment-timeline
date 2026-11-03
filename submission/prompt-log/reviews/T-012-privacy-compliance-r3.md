# T-012 privacy-compliance review, round 3 (final, §7.4) — research/phi-and-ai-supervision.md (commit cf009d2)

**Verdict: pass.** All 3 round-2 majors are resolved, and so are all 4 minors and the nit. I re-fetched the new
commercial-retention source (src 19) and the API data-retention page (src 9). The 30-day and 2-year wording in §1.4
matches them verbatim, and the "not retained by default" line is now marked as not the standard default. PR-1, PR-1a
and §3.1.4 match D-020 and the spec (R-CO-4, README-arch:63). The §181.154 "for each disclosure" question is routed
to counsel, and the (a) notice and (d) AG form are back. I re-checked the §521.053(a) and (c) quotes against the
statute text.

Round-2 resolution:

| r2 finding | Status | Evidence (cf009d2) |
|---|---|---|
| M1 retention "not retained by default" | resolved | :111-120 quotes src 19 "within 30 days of receipt or generation" (priv.txt:18) and its exceptions (priv.txt:19-22, 31); :117 says it "must not be quoted as the standard API default"; :121-122 marks HIPAA-org-without-ZDR retention as unknown and to be confirmed in the BAA; consent wording at :127-129 rewritten; src 19 added at :271 |
| M2 §181.154 per-disclosure + (a) notice | resolved | :57-65, PR-2a :160, §3.2 :203, §3.3 :220-221, A-P6 :244-249: "for each disclosure" is an open question for counsel; the (a) notice and the (d) form are named |
| M3 D-020 conflict | resolved | PR-1 :156 "rejected and not stored", with a row-count-unchanged test and a log-grep test; PR-1a :157 local-only, provider-side spend limit; :195 "no in-app spend ledger, D-020"; grep for spend counter / public live / opt-in finds nothing |
| m (2)(D) misread | resolved | :52-53 "a covered entity in its own right. It does not place the vendor inside the firm" |
| m screen share | resolved | :183-188 treated as a disclosure, with conditions; in-person preferred |
| m Appendix A provenance | resolved | :192 "the same approach as Appendix A's fictional sample" |
| m §521.053 trigger/vendor duty | resolved | :225-230 quotes (a) verbatim, including the good-faith carve-out (s521.txt:16); (c) at :229 (s521.txt:19); PR-2 :159 |
| nit PR-9 tags | resolved | :168 names `instruction_like_text` and `record_warning` |

Remaining (no blockers, no majors):
- **minor:** §1.4 and the prescribed consent wording omit src 19's contract-gated clause that anonymized data may be
  kept longer.
- **nit:** "not available under ZDR" drops "unless expressly authorized by Anthropic".
- **nit:** the header still says Round 2 and doesn't list D-020 among the binding decisions.

**Product note implications.** Use the :127-129 sentence. It is accurate apart from the anonymization caveat, which
belongs in the vendor review.

**Part 2 implications.** PR-2a gives the right structure for the engagement packet. Counsel decides per-run versus
per-matter authorization, and that decision is on file before the first call. The (a) notice is posted in the office
and on the website.

```json
{"card": "T-012", "persona": "privacy-compliance-reviewer", "model": "claude-opus-5-5",
 "scope": "research/phi-and-ai-supervision.md at cf009d2 (git diff 4924221..cf009d2); decisions D-008, D-009, D-020, D-023 in memory/ORCHESTRATOR_DECISIONS.md; spec/REQUIREMENTS.md R-CO-4; app/README-arch.md:63; no app URL (research card)",
 "exercised": [
  "python3 tools/board.py show T-012 -> status in_review, rounds 2, commits [8a22a5c, 4924221, cf009d2]",
  "git log --date=iso -6 -> cf009d2 2026-11-01 18:58:55 (after D-020/D-023 commits); git diff 4924221..cf009d2 -- research/phi-and-ai-supervision.md (read in full)",
  "curl privacy.claude.com/en/articles/7996866 -> 200 107447 bytes; text-extracted with artifacts/review-evidence/T-012-h2t.py; priv.txt:18 'within 30 days of receipt or generation, except:'; :19-22 Files API / ZDR agreement / Usage Policy / law; :31 'up to 2 years ... classification scores for up to 7 years'; :32 anonymization clause; no HIPAA/BAA mention",
  "curl platform.claude.com/docs/en/manage-claude/api-and-data-retention -> 200; anth.txt:35 defers standard retention to the commercial policy; :39 'not retained by default'; :55/:110 Covered Models 'not available under ZDR unless expressly authorized by Anthropic'; :349 2-year flagged clause",
  "curl texas.public.law §521.053 and §181.154 -> 200/200; s521.txt:16 (a) incl. good-faith carve-out, :19 (c) 'immediately after discovering the breach'; s154.txt:16-20 (a) notice and (b) 'for each disclosure', :28 (d) AG form",
  "grep -n -i of the research doc for: not retained, spend counter, ledger, public live, live mode, falls inside, how Appendix A, for each disclosure, (a) notice, 521.053, opt-in, compliant, anonymi",
  "grep of memory/contracts/api.md, app/README-arch.md and spec/REQUIREMENTS.md for llm_calls / review_events / 'not stored' (PR-1's table names and D-020 wording are consistent)",
  "python3 tools/check_secrets.py -> 'check_secrets: ok (185 file(s) scanned)'",
  "read personas/privacy-compliance.md (live dossier), my memory recurring-findings.md and reviews/T-012-privacy-compliance-r2.md"
 ],
 "verdict": "pass",
 "scores": {"source_accuracy": 5, "coverage_of_texas_and_vendor_law": 5, "requirements_testable_for_this_prototype": 5, "usefulness_for_product_note_and_part2": 4},
 "findings": [
  {"severity": "minor",
   "title": "§1.4 exception list and the prescribed consent wording omit src 19's contract-gated anonymized-data retention",
   "evidence": "privacy.claude.com 7996866, priv.txt:32: \"If permitted in your contract with us, we may anonymize your organization's data for research or statistical purposes, in which case we may retain this information for longer.\" research/phi-and-ai-supervision.md:112-116 lists the Files API, ZDR, Usage Policy, law and flagged exceptions but not this one; :127-129 consent wording: \"deletes inputs and outputs within 30 days unless a zero-retention agreement applies, and may keep them up to 2 years if flagged ... or longer where required by law\".",
   "why_it_matters": "Checklist item 9 says vendor handling must be stated accurately. The doc presents :127-129 as the complete text for client consent. Vendor 'anonymization' is not HIPAA Safe Harbor or Expert Determination de-identification, and Op. 705 requires the lawyer to review the tool's terms. This is a vendor-review item, not a defect in the prototype.",
   "fix": "Add to the §1.4 exceptions: 'longer for data anonymized for research or statistics, if the contract permits (src 19)'. Add to the PR-2 vendor checklist: 'confirm the contract or BAA does not permit anonymized retention, or disclose it'.",
   "acceptance_test": "grep -n -i anonymi research/phi-and-ai-supervision.md returns a line in §1.4 or PR-2."},
  {"severity": "nit",
   "title": "Covered Models 'not available under ZDR' drops the source's 'unless expressly authorized by Anthropic'",
   "evidence": "research/phi-and-ai-supervision.md:119-120 \"require 30-day retention and are not available under ZDR (src 9)\"; anth.txt:55 \"not available under ZDR unless expressly authorized by Anthropic\".",
   "why_it_matters": "This is a small overstatement in a vendor summary that may be copied into Part 2.",
   "fix": "Append 'unless expressly authorized by Anthropic'.",
   "acceptance_test": "§1.4 Covered Models line carries the qualifier."},
  {"severity": "nit",
   "title": "Header is stale: says Round 2 and omits D-020 from the binding decisions, though PR-1/PR-1a/§3.1 rely on it",
   "evidence": "research/phi-and-ai-supervision.md:3 \"Round 2 (2026-11-02), revised after reviews/T-012-privacy-compliance.md\"; :6 lists D-001, D-005, D-008, D-009, D-011 only.",
   "why_it_matters": "Readers use the header to see which decisions bind the requirements.",
   "fix": "Update to Round 3 and add D-020 (demo POST rejects and stores nothing; live mode local-only).",
   "acceptance_test": "Header names Round 3 and D-020."}
 ],
 "whats_right": [
  "§1.4 now quotes the commercial 30-day default verbatim and explicitly fences off the 'not retained by default' line. Keep the 'must not be quoted as the standard API default' warning.",
  "PR-1's control (row counts unchanged across five tables plus a log grep for a unique token) is the right store-nothing test for D-020. Keep it as the E2E.",
  "§181.154 is handled as the persona requires: the doc asks rather than decides. Counsel's written answer on per-run versus per-matter authorization must be on file before the first call, and the (a) notice is named."
 ],
 "questions_for_chris": []}
```
