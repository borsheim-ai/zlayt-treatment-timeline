# GATE-M2 round 1 — triage (orchestrator)

Pinned commit 0c24f5f. Panel: staff-engineer, qa, paralegal, legal-nurse, claims-adjuster (Opus), privacy-compliance.
Result: **fail** (3 blockers). Every finding at major or above is mapped to a card; the gate re-runs on the fix commit.

| Severity | Source | Finding | Card |
|---|---|---|---|
| blocker | claims-adjuster | Per-visit rates reach the carrier letter through entry summaries/quotes (lib01 $140, lib03 $120) | T-139 |
| blocker | paralegal | Ledger total and balance-due lines classed as charges; lib11 letter total $10,906 vs $6,000 | T-140 |
| major | claims-adjuster | Dismissed ED charge still quoted in the letter and listed under "Bills to request" | T-139 |
| major | paralegal | lib11 intake "Prior accidents: No" vs PCP 2019/2022 accidents not flagged; false accident-date conflict shown | T-141 |
| major | legal-nurse | "No conflicts found" overclaims; laterality and LOC contradictions not checked | T-142 (+ T-141 API field) |
| major | legal-nurse | Entries drop clinical sentences silently | T-143 (backend) + T-144 (UI) |
| major | qa | Live ship-bar evidence is at 63e18ed; a confirming live 3-run is needed at the tag commit; calibration only fixture-regenerated | orchestrator: confirming live 3-run + live calibration after fixes land |
| blocker | staff-engineer | Deadline-hit run skips judge 1 but entries stay 'verified' and Why says the check agreed; batch accept takes them | T-145 |
| major | staff-engineer | Timed-out re-run deletes previous pending items while the error says they were kept | T-146 |
| major | staff-engineer | No passing ship-bar report at HEAD (--check-fresh exits 1) | same as qa: confirming live 3-run |
| minor | paralegal | "Bills to request" names the plaintiff's law firm | T-139 note |
| minor | privacy | Paste box lacks synthetic warning; injection scan misses "disregard the above" phrasings; JSON export carries provenance ids | to backlog after re-gate |
| question | privacy | Should the letter itself carry an AI marker? | already decided by D-009 (AI statement in UI banner + internal notes, not the letter; listed in NEEDS_CHRIS assumptions) |

In-flight carry-overs that also land before re-gate: T-132, T-133, T-134, T-136, T-138.
