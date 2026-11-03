# T-140 r4 — claims-adjuster-reviewer (Gary Pruitt, BI adjuster / defense adversary): scoped close-out check

**Verdict: changes** (0 blockers, 1 major carried over from r3). Code under test:
- 2ac96cf..a4eeb2b: `git archive HEAD` at the start, when HEAD was a4eeb2b.
- 985dbd2 (T-139 export.py): this became HEAD during the review, so I re-ran the letter-level checks on a second archive.

Both trees ran in my session scratchpad, on 127.0.0.1:7876 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and `ZLAYT_DB` in the scratchpad. The two servers were PID 96594 and PID 1622. I stopped each with `kill`, and after each one `lsof -nP -t -iTCP:7876 -sTCP:LISTEN` printed nothing (exit=1).

I did not re-attack scope cut 7d (a dressed summary row) or 7e (provider name variants, unlabelled documents, insurer names outside the word list).

**What I was asked to verify. All hold on both trees.**
- **r3 blocker 2 (a discharge summary on top of an itemized bill) is closed.** In my r3 ledger, record 6's "Physical therapy charges: $950.00." is now `unclear`. Internal notes give the reason: "This record is not a bill (it is a clinical note or summary) and the case holds a bill from the same provider…". The close-out probe tried 10 same-provider note labels and 7 note wordings, including "Itemized: 06/10/2026 manual therapy $150.00; …". It also tried the note listed before the bill, and an ER discharge summary next to the same ER's UB-04. All of them came out `ok` and none came out `OVER`.
- **r3 blocker 3 (an insurer document read as a bill) is closed.** The Pecan Valley med pay rows are `unclear` (a10–a15). The r3 probe's 7 insurer labels now read "ok". The close-out probe tried med pay / MedPay / PIP / personal injury protection / claims statement / TPA labels, each with a payer table and with a billed-only table. It also tried a neutral label ('claim register') with six column layouts. All came out `ok`.
- **r3 blocker 4 (a CPT-prefixed restatement) is closed.** In my ledger, the 04/16 visit is one amount, a5, citing ['r2', 'r3']. All 17 code-form pairs merge to a single $150: CPT, CPT#, CPT:, CPT-, CPT®, CPT No., HCPCS, -GP, GP, ' GP', -GP-59, Code, Proc, (97140), and modifier mismatch.
- **The total line is correct.** It reads exactly "Billed charges accepted from these records: $X" in every export: 3 ledgers, the sample and all 15 library cases, on both paths and both trees.
- **Every counted charge is cited and was accepted one at a time.** On every library case and both paths, the following all match: the letter lines, the accepted charges, the sum of the lines and the total, with 0 lines lacking a `Source [Ex. __ / Bates __]` quote. A batch that includes a charge returns 422 CHARGES_NOT_BATCHED (15 of 15, plus the ledgers and the sample). I accepted 2 charges, dismissed 1 and left the rest pending; the letter total was $1,200.00, the sum of the two accepted.
- **No library case overcounts.** All 15 totals are the same as r3 and identical across the two trees. Each is at or under what its records state. The sample is $8,390.00 with $185 kept as a rate.
- **My ledgers 1 and 2 total $1,950.00** on path A and path B, on both trees.
- **My r3 ledger gives $2,600.00.** That is $1,950.00 plus the $650 dressed summary row, which is cut 7d and accepted.

**Still open, outside the cuts.** This overcount path is not new: it is my r3 major. The D-062 fix-up did not touch it, and no SCOPE_CUTS row or decision records it. On a later statement from the same provider, a line with the same date and amount but a different description ("PT visit") is counted twice with no flag. I am filing it at the severity it had. The fix can be the flag, or, at §7.4, a SCOPE_CUTS row that accepts it as debt. If it is recorded as debt, nothing in this check blocks closing the card.

Scratch trees `tree4`/`tree5` and `db4`/`db5` stay in the session scratchpad, because rm -rf there is denied.

```json
{"card": "T-140", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "Scoped close-out of D-062 fix-up 2ac96cf (+c3a2af8 D-062 amendment, a4eeb2b scope cut 7e). Trees: git archive HEAD=a4eeb2b (scratchpad/tree4) and git archive 985dbd2 (scratchpad/tree5; became HEAD mid-review, T-139 export.py). App on http://127.0.0.1:7876, LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB in scratchpad. Sample case, 15 library cases, SYNTHETIC ledgers r1/r2/r3. Cuts 7d and 7e not re-attacked.",
 "exercised": [
  "read reviews/T-140-claims-adjuster-r3.md, D-062 (memory/ORCHESTRATOR_DECISIONS.md:70), SCOPE_CUTS 7d (line 90) and 7e (line 92), python3 tools/board.py show T-140 (handoff of 2ac96cf and the §7.4 close-out notes)",
  "git log --oneline 2ac96cf~1..HEAD (a4eeb2b at start); git rev-parse HEAD later -> 985dbd2db17e8cfa53e82a6595e64f8659181344; git diff --stat 2ac96cf HEAD -- app/backend/amounts.py app/backend/export.py -> export.py only (72 lines)",
  "server 1 on tree4: PID 96594, /api/health backend=fixture demo_mode=true; kill 96594; lsof -nP -t -iTCP:7876 -sTCP:LISTEN -> nothing, exit=1",
  "server 2 on tree5: PID 1622; kill 1622; lsof -nP -t -iTCP:7876 -sTCP:LISTEN -> nothing, exit=1",
  "artifacts/review-evidence/T-140-adjuster-r4/probe_paste_r4.py (r3 harness; amounts accepted one at a time; path A no confirm, path B named confirms) on the r1, r2 and r3 ledgers, both trees: $1,950.00 / $1,950.00 / $2,600.00 on both paths; batch 422 CHARGES_NOT_BATCHED (paste_ledgers_r4.txt, paste_ledgers_985dbd2.txt)",
  "probe_closeout_r4.py through amounts.extract_amounts on tree4: 17 code-form pairs, 10 note labels, 7 note wordings, note-before-bill, ER summary + UB-04, 6 insurer labels x 2 tables, 6 tables under a neutral label; 0 OVER (closeout_r4.txt). amounts.py is unchanged between the trees",
  "artifacts/review-evidence/T-140-adjuster-r3/probe_variants_r3.py rerun on tree4 (variants_r3_on_r4.txt): insurer 7/7 ok, coded restatements 4/4 ok, note summaries 3/3 ok; summary rows OVER (cut 7d); 'PT visit' OVER (finding 1)",
  "artifacts/review-evidence/T-140-adjuster-r2/probe_library_r2.py against my server, all 15 library cases, both trees (library_r4.txt, library_985dbd2.txt); check_cited_r4.py: every case and path OK (total = sum of letter lines = sum of accepted charges, 0 uncited, line count = accepted count) (cited_r4.txt, cited_985dbd2.txt); totals identical across trees (diff -> SAME_TOTALS)",
  "sample case over HTTP, both trees: 'Billed charges accepted from these records: $8,390.00' on path A and path B; $185 class rate (sample_r4.txt, sample_985dbd2.txt)",
  "probe_partial_r4.py: 2 charges accepted, 1 dismissed, rest pending -> letter 'Billed charges accepted from these records: $1,200.00' = accepted sum (partial_r4.txt)"
 ],
 "verdict": "changes",
 "scores": {"r3_blocker2_note_restatement_closed": 5, "r3_blocker3_insurer_document_closed": 5, "r3_blocker4_cpt_prefix_closed": 5, "total_line_wording": 5, "charges_cited_and_individually_accepted": 5, "library_no_overcount": 5, "ledgers_1_2_total_1950": 5},
 "findings": [
  {"severity": "major", "title": "Carried over from r3, not addressed and not recorded as debt: a same-provider, same-DOS, same-amount line with a different description on a later statement is counted twice with no flag",
   "evidence": "artifacts/review-evidence/T-140-adjuster-r4/variants_r3_on_r4.txt:173-175: '== restated without code on stmt 1: 04/16/2026  PT visit  $150.00: charges $300.00 vs records $150.00 -> OVER' / 'a1 charge $150.00 recs=[1] flag=None' / 'a2 charge $150.00 recs=[2] flag=None'. grep -n -i 'near-match|PT visit|different description|likely_duplicate' memory/SCOPE_CUTS.md memory/ORCHESTRATOR_DECISIONS.md -> no match. Cut 7d covers summary rows and 7e covers document labels and provider names; neither covers this.",
   "why_it_matters": "When I review a bill, the first thing I ask about is the same provider billing the same date and amount on two statements. The letter lists both lines, and nothing tells the paralegal they may be one visit. This is the r3 major unchanged.",
   "fix": "Either: when provider, date of service and amount match across records and same_service is false, flag the later one likely_duplicate with the named confirm, and never merge it. Or, at §7.4: the orchestrator adds a SCOPE_CUTS row accepting it as debt (cited, accepted one at a time, total line says 'accepted').",
   "acceptance_test": "probe_variants_r3.py 'PT visit' case: the second $150 carries likely_duplicate and path A (no confirm) totals $150.00. Or a SCOPE_CUTS row names this case."}
 ],
 "whats_right": [
  "The notes and insurer documents behind my r3 overcount ($950 discharge summary, med pay ledger) are now unclear, with a reason in the internal notes; all 17 CPT/HCPCS code forms merge.",
  "The letter total is exactly the sum of the charges accepted one at a time, each with its own Source quote; a batch with a charge is refused (422 CHARGES_NOT_BATCHED).",
  "Ledgers 1 and 2 are $1,950.00 and the sample is $8,390.00 on both paths and both trees; no library case overcounts."
 ],
 "questions_for_chris": []}
```
