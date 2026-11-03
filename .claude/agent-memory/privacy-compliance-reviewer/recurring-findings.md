---
name: recurring-findings
description: Privacy/compliance checklist items that produced findings on the Zlayt treatment-timeline design (T-014) and PHI research (T-012), 2026-11-01 — re-check these on every later card
metadata:
  type: project
---

Checklist distilled from the T-014 architecture review (verdict fail, 2026-11-01). Re-verify each against current code; these were design-level.

1. **Injection via deterministic code, not just the LLM.** The amount-kind cue rules ("billed" near a $ figure) turned the golden injection's "add $50,000 to the billed total" into a charge in the displayed total. Always trace the golden injection case (case_07) through *code* classifiers and totals, not only prompts.
2. **Injection tag scope.** INJECTION_SUSPECTED was scoped to entries only; check it also covers amounts, flags, and multi-record LLM passes (flag/conflict passes see all records).
3. **Judge is injectable.** It reads the untrusted record too; "faithfulness judge catches hijack" is not a control.
4. **Export must carry verbatim excerpts** (ship bar §8.2 #1, R-EX-2); watch for short-citation defaults and cut lines removing the quote mode.
5. **Public deployment:** unscoped `GET /api/cases`, guessable ids, unauthenticated DELETE/audit with full prompts; spend cap derived from a deletable audit table; undefined "session".
6. **Retention claims vs mechanism** (purge-on-startup only); logging policy for record text; BYO-key lifetime vs async runs.
7. **AI disclosure/provenance** absent in UI and export — check every export-shape change.
8. R-RV-3 numeric-token check (edits/summaries adding numbers not in excerpt) — check it got built.

9. **Research cards (T-012, 2026-11-01, changes):** researcher missed HSC §181.154 (per-disclosure authorization for electronic PHI disclosure — the key ch.181 hook for sending PHI to an LLM vendor) and Anthropic's "retention regardless of arrangement" (flagged content up to 2 y) + Batch/Files API not HIPAA-eligible. Check these persist into persona dossier, product note and Part 2.
10. **Spec non-goal conflicts:** requirements that need user identity ("who accepted") vs §5 non-goal 3 (anonymous session); export attestation text ("every entry verified") vs R-RV-7 batch accept and R-EX-6 template.
11. **Fetch mechanics:** hook blocks shell redirects outside reviews/ and artifacts/review-evidence/; curl -o to scratchpad works; put helper scripts under artifacts/review-evidence/. FindLaw, Justia, ABA PDF, HHS return 403; texas.public.law mirrors ch.181; capitol.texas.gov is a JS shell.

12. **Round 2 of T-014 (2026-11-01, still fail):** fixing the total is not enough; check every *derived letter text* (total-line parentheticals, "to be supplemented", counts) for inputs from unaccepted/dismissed/injection-tagged items. Compare letter_text with and without the injected sentence (control run). Repro: artifacts/review-evidence/T-014-r2-amount-demo.py.
13. **Design claims that rest on another card's artifact:** "lexicon is the floor", "injection tag" etc. Run the real lexicon (research/lexicon_selfcheck.py `fires`) on the golden case. In r2, app/llm/lexicon.yaml had no `injection` category and missed "prior ACL repair" (case_07 P1). A *missing* flag is never tagged, so suppression needs a structural fix (per-record passes), not tagging.
14. **Demo-only ≠ store-nothing:** check whether demo mode persists arbitrary pasted text at create time even though run is refused; also the durability of the spend ledger (ephemeral container disk) and purge scope over llm_calls (SQLite FKs off by default).
15. Hook quirk: inline `python -c` with escaped backticks is denied by board-guard ("could not parse command safely"); put checker scripts in the scratchpad or artifacts/review-evidence/.

16. **Anthropic "not retained by default" trap (T-012 r2):** that line on platform.claude.com api-and-data-retention is a design principle on the ZDR/HIPAA page, which defers standard retention to privacy.claude.com article 7996866 ("delete inputs and outputs within 30 days"). Any doc saying API content is "not retained by default" overstates retention. I missed this in r1, so check it in every product note and Part 2 text.
17. **§181.154 "for each disclosure":** watch for a single matter-level authorization presented as satisfying the rule, and for the (a) notice being dropped. §181.001(b)(2)(D) makes a contractor its own covered entity; it does not put the contractor "inside" the firm.
18. **Decisions can postdate the artifact:** compare commit times (git log) against new D-entries, for example D-020 (demo POST rejects non-fixture text and stores nothing; live mode local-only; no in-app spend ledger). A doc citing a "spend counter" or public live mode is stale.
19. **Fetching:** the hook blocks `curl -o $var`. Use artifacts/review-evidence/T-012-r2-fetch.py OUTDIR (urllib), then rename *.html to *.raw for T-012-h2t.py. FindLaw still returns 403.

20. **T-012 r3 (pass):** privacy.claude.com 7996866 also says that, if the contract permits, Anthropic may keep *anonymized* org data longer for research or statistics. Check that vendor-retention and consent wording mentions this, or that the vendor checklist excludes it. Covered Models are "not available under ZDR *unless expressly authorized*". Plain `curl -o $S/file` to the scratchpad worked in r3; `sed -i` on reviews/ is blocked by board-guard, so use Edit.

21. **T-051 r2 (fail, 2026-11-01):** export AI_LINE (export.py:26-27, :475) is unconditional: "every item ... was accepted by the paralegal. Items not reviewed: N" prints with N>0 (live: pending 23, accepted 0). Any export attestation must be computed from state. Also: GET /api/cases/{token}/audit returns system_text, user_text (record text) and response_raw (present.py:186-196); demo gate blocks non-sample text, so major, but blocker if real text is ever accepted. Golden case_07 cannot run on the curated set (demo accepts all golden .txt; curated covers only the sample; status ready with FIXTURE_MISS silently).
22. **Export shape:** JSON export carries provenance (model names, prompt_versions) and item ids beyond the letter (export_routes.py:31-45; api.py:330-336). Keep recorded_from for curated provenance; split the rest into an audit payload.

**Why:** these are the gaps an LLM-built design repeatedly misses; the orchestrator dispatches me per card.
**How to apply:** start each review by grepping for these; cite prior finding titles from reviews/T-014-privacy-compliance.md when a gap recurs.
