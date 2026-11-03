# T-005 round 3 (final): product-manager-reviewer

**Verdict: changes.** 0 blockers, 1 major, 2 minors, 2 nits.

All seven r2 findings are resolved:
- NEEDS_CHRIS now has 3 rows and 3 `needs_chris` cards, with matching priorities.
- Every row is a genuine Chris ask with an exact expected answer. Team calls moved to an FYI list.
- ADR-000e matches `tailscale serve status`.
- The RUNBOOK Terminal restart now carries `--remote-control`.
- CLAUDE.md, STATE and ADR-000d all say native agents with a fallback.
- The release row has its (M4) marker.

One new major: the working-tree `memory/STATE.md` heartbeat line is now garbled. RUNBOOK Restart step 4 tells the restarted session to recreate the cron from "text in memory/STATE.md", and that text is gone.

```json
{"card": "T-005", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "Round 3. Working tree 2026-11-02 ~01:00Z: CLAUDE.md, docs/RUNBOOK.md, memory/{STATE,LESSONS,DECISIONS ADR-000d/e,ORCHESTRATOR_DECISIONS}.md, submission/NEEDS_CHRIS.md, needs_chris/cancelled/done cards T-019..T-024. Board https://<redacted-private>:7777. No sample case (M0).",
 "exercised": [
  "python3 tools/board.py show T-005 -> rounds 2, in_review, AC 1-3 checked",
  "python3 tools/board.py list --status needs_chris -> T-019 P1 (#1), T-022 P1 (#2), T-023 P2 (#3); NEEDS_CHRIS.md table rows #1 P1 T-019, #2 P1 T-022, #3 P2 T-023 -> 3/3 parity, priorities match",
  "board.py list --status cancelled -> T-020, T-021; --status done -> T-024 (email, answered)",
  "python3 tools/board.py validate -> 'ok (27 file(s))'; grep NEEDS_CHRIS tools/board.py .claude/hooks/*.py -> only board.py:310 and :408 (no row/card parity check)",
  "tailscale serve status -> :10000 and :8443 -> 8787, 443 -> 4173, :7777 -> 7777; curl https://<redacted-private>:7777/healthz -> 200; curl http://localhost:7777/healthz -> 200",
  "read ADR-000e (DECISIONS.md:46-51): https serve on :7777/:7860, never overwrite existing mappings; plain http listed under Alternatives",
  "read docs/RUNBOOK.md in full; claude --help -> -c/--continue, --dangerously-skip-permissions and --remote-control [name] all exist",
  "wc -l CLAUDE.md -> 86; python3 -I artifacts/review-evidence/T-005-r2-pathcheck.py <repo> -> the release row now reads '(all M4)'; the remaining hits are false positives on relative names",
  "grep spawn/native in CLAUDE.md:54, STATE.md:26, ADR-000d:39-44 -> all say native, with agent_prompt.py as fallback",
  "git diff HEAD -- memory/STATE.md -> heartbeat prompt line replaced (uncommitted); read D-024 (ORCHESTRATOR_DECISIONS.md:32)",
  "grep -rn 'NEEDS_CHRIS #[0-9]' memory/ docs/ CLAUDE.md -> ORCHESTRATOR_DECISIONS.md:17 'NEEDS_CHRIS #8', LESSONS.md:11 '#2 withdrawn'",
  "wc -l evals/golden/hallucinations.jsonl -> 40"
 ],
 "verdict": "changes",
 "scores": {"map_completeness_for_fresh_agent": 4, "runbook_operable_by_chris": 4, "restart_readiness": 3, "needs_chris_quality": 4, "decisions_under_ambiguity_legibility": 4},
 "findings": [
  {"severity": "major",
   "title": "STATE.md heartbeat line is garbled, so Restart step 4 can't recreate the heartbeat",
   "evidence": "git diff HEAD -- memory/STATE.md: removed '-Heartbeat cron 0174861c at :07/:27/:47 — prompt: \"HEARTBEAT (zlayt-pm-project orchestrator, §9): run board status --brief and inbox; nudge stalled (45 min) owners; dispatch pending reviews; append one line to PROGRESS.\" Recreate after restart.' and added '+Heartbeat cron 0174861c at :07/:27/:47 — prompt: \"Heartbeat: hourly cron at :13 (D-024); recreate after restart.' The new line gives two schedules, leaves the quote unclosed and has no prompt body. RUNBOOK.md Restart step 4: 'recreate the heartbeat cron (text in memory/STATE.md)'.",
   "why_it_matters": "The heartbeat is what nudges stalled owners and dispatches pending reviews while Chris is away. After a reboot the resumed orchestrator has no prompt to recreate and two conflicting schedules to pick from. My r1 major was exactly this: a restart that doesn't resume the autonomous run.",
   "fix": "STATE.md: one schedule that matches D-024(6) (hourly at :13), plus the full heartbeat prompt text in a closed quote. Drop the old cron id or mark it 'session-only'.",
   "acceptance_test": "grep -n 'Heartbeat' memory/STATE.md shows one schedule and a complete quoted prompt that includes 'board status --brief', 'inbox' and 'dispatch pending reviews'."},
  {"severity": "minor",
   "title": "Stale cross-references after the NEEDS_CHRIS rebuild",
   "evidence": "ORCHESTRATOR_DECISIONS.md:17 D-009 '... NEEDS_CHRIS #8.' There is no row #8 now; it is an FYI line. NEEDS_CHRIS.md row 3 says '20 hallucination probes', but wc -l evals/golden/hallucinations.jsonl gives 40, and ship bar 4 is now a rate. RUNBOOK Restart step 4 calls general-purpose plus agent_prompt.py the default ('unless native agent types are available'), while CLAUDE.md:54 says native is the default. LESSONS.md:11 says native types appeared at 00:22:43Z; ADR-000d:41 says 'about 00:40Z'.",
   "why_it_matters": "Row 3 is a spend ask, and Chris sizes his answer from the call count it states, which is now about half the real eval load. The other mismatches are small, but they are the kind a hiring-panel reader notices in a decision log.",
   "fix": "D-009: point to the FYI list. Row 3: 'every item in hallucinations.jsonl (40 today)', with the call estimate updated. RUNBOOK step 4: 'native agent types; fallback agent_prompt.py'. Align the LESSONS/ADR timestamp.",
   "acceptance_test": "grep -rn 'NEEDS_CHRIS #[0-9]' memory/ returns only LESSONS history lines. NEEDS_CHRIS row 3's probe count equals wc -l of hallucinations.jsonl."},
  {"severity": "minor",
   "title": "Row-to-card parity is still kept by hand; it broke in r1 and r2",
   "evidence": "grep NEEDS_CHRIS tools/board.py .claude/hooks/*.py finds only board.py:310 (close-on-answer) and :408 (file list). board.py validate passes with no parity check. The r2 fix offered a validator or a stop-guard check.",
   "why_it_matters": "The needs_chris column is Chris's view from his phone. The process that adds rows during triage skipped the card step twice already.",
   "fix": "Under D-024(7) no harness round is left, so log this as debt in LESSONS.md and add a line to the orchestrator triage checklist: 'NEEDS_CHRIS row → board.py new --status needs_chris \"(NEEDS_CHRIS #n)\" same priority'.",
   "acceptance_test": "LESSONS.md or the orchestrator checklist names the rule; the M1 gate re-runs the 3/3 parity check."},
  {"severity": "nit",
   "title": "ADR-000e context and the NEEDS_CHRIS FYI omit the :10000 mapping",
   "evidence": "tailscale serve status: ':10000 ... proxy http://127.0.0.1:8787'. ADR-000e:48 lists only 443 and 8443. The FYI line says 'your existing 443/8443 mappings untouched'. RUNBOOK.md:11 does list 8443/10000.",
   "why_it_matters": "The tear-down list at the end has to match what's live.",
   "fix": "Add ':10000 → 8787' to ADR-000e's context and the FYI line.",
   "acceptance_test": "Every serve port in `tailscale serve status` that isn't ours is named in ADR-000e."},
  {"severity": "nit",
   "title": "T-019 (API key) is P1, but it is only needed if Chris answers 'live' to T-022",
   "evidence": "NEEDS_CHRIS row 1: 'Only needed if you answer \"live\" to #2.' The default is demo-only (D-008, D-020).",
   "why_it_matters": "Two P1s on Chris's phone where one depends on the other overstates what's urgent.",
   "fix": "Make T-019 P2, or add depends_on T-022.",
   "acceptance_test": "board.py show T-019 shows P2 or depends_on T-022."}
 ],
 "whats_right": [
  "NEEDS_CHRIS holds 3 genuine Chris asks, each with a card, the same priority, an exact expected answer and the team's default meanwhile; team calls sit in an FYI list Chris can overrule.",
  "ADR-000e now records what was built (https serve on :7777/:7860, never overwrite existing mappings), and its URL returns 200.",
  "The RUNBOOK Terminal restart line has --continue --dangerously-skip-permissions --remote-control, all confirmed in claude --help."
 ],
 "questions_for_chris": []}
```
