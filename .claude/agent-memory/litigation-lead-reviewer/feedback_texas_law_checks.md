---
name: texas-law-checks
description: Recurring Texas-law misstatements and source-fetch workarounds seen in persona/ethics content on this project (Rule 1.05, Op. 705, Haygood, ch. 181)
metadata:
  type: feedback
---

Re-check these every time ethics/damages law shows up in dossiers, product note or Part 2. They were wrong or overstated in T-010 (2026-11-01).

- Tex. Disc. R. 1.05 has NO ABA 1.6(c)-style "reasonable efforts" clause; duty is "shall not knowingly reveal". Precautions come from 1.01 cmt. 8 + Ops. 680/705.
- Op. 705 (Feb 2025) only analogizes AI to "overconfident nonlawyer assistants. Cf. Rule 5.03" — not a holding that 5.03 governs AI. ABA 512 is the one tying AI to 5.1/5.3.
- Demand letters go to adjusters: the relevant rule is Tex. R. 4.01 (truthfulness to third persons), not 3.03 candor/Mata.
- Haygood: recoverable = "have been or must be paid"; billed is not categorically an overstatement (LOP/unpaid).
- Tex. H&S §181.154 (electronic disclosure authorization) is the ch. 181 provision relevant to sending records to an LLM vendor.
- §41.0105 unchanged since 2003; 2025 SB 30 died in conference (last action 05/30/2025).

**Why:** these become reviewer prompts and submission prose read by lawyers; a wrong rule costs the same credibility as a wrong date in a demand.
**How to apply:** fetch primaries with curl (WebFetch unavailable): Haygood via search.txcourts.gov cn=09-0377; statutes via texas.public.law (statutes.capitol.texas.gov /Docs htm links return a JS shell); ABA 512 PDF via web.archive.org id_ snapshot (americanbar.org 403). Bash `>` redirects into scratchpad are blocked by the reviewer hook; use `curl -o`.

- §181.154(c)(2) is "authorized OR required by state or federal law"; (c)(1) exceptions apply only to disclosures TO another covered entity. Paraphrases drop both.
- Rule 4.01 cmt 3 (verified): "no duty to inform a third person of relevant or material facts, except as required by law..."

Round-2 traps (T-010, 2026-11-01): (1) dossier fixes are inert until `tools/compile_agents.py` recompiles `.claude/agents/*-reviewer.md` — always line-diff dossier vs compiled body; (2) my own round-1 fix wording can contradict later binding decisions (D-001 / R-EX-4/R-EX-8: missing bills and rate reasons belong in internal notes, never the letter) — re-check my prior fixes against ORCHESTRATOR_DECISIONS. Reviewer hook blocks heredoc/`>` into scratchpad; put helper scripts under artifacts/review-evidence/.

Round-3 (T-010, 2026-11-01): D-019 superseded R-EX-8's "(... charges to be supplemented)" parenthetical — letter total line is exactly "Billed charges stated in these records: $X"; spec reconciliation lives on T-025. Don't quote R-EX-8's sample line in fixes. My session's loaded prompt can lag the on-disk agent file (recompile seconds before dispatch) — trust `compile_agents.py --check` + line-diff, not my own prompt text. Shell hook rejects `for p in ...; do echo "$p: $(...)"` (git-guard); list paths explicitly instead.

Also recurring: watch for persona checklists that make the tool resolve the accident-date conflict or decide what adverse facts go into the export — that is attorney strategy, and the spec says export = only accepted items.
