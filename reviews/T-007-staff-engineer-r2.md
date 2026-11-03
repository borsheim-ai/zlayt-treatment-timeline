# T-007 round 2 review — staff-engineer-reviewer

**Verdict: pass** (0 blockers, 0 majors, 2 minors, 2 nits).

The orchestrator's rejection of the round-1 major is correct. `sed -n '1,20p' memory/PROGRESS.md` line 10 reads `6. Conventional commits e37efb3, fbe5690; .gitignore complete; tag m0 pending M0 gate.` It has no PASS marker, unlike items 1-5 and 7. The round-1 review quoted a "-> PASS" suffix that is not in the file. `python3 tools/board.py list --milestone M0` shows `T-006 M0 orchestrator in_review P0 AC 3/3`, not READY. `git tag -l` prints nothing, so the tag is genuinely absent, but PROGRESS says so honestly.

Round-1 minors: both are addressed by artifacts/m0-smoke/*.md. agent-load-tests.md has the verbatim native-load error plus both haiku replies, each 5 lines (matches CONTRACT 4.8 item 4). live-feed.md has before/after /api/activity output, and board/activity.jsonl lines 96-97 corroborate the probe event. Neither artifact is cited from PROGRESS yet.

Not verifiable from my seat: heartbeat cron 0174861c (not a finding). Not exercised: the browser UI polling the feed live.

```json
{"card": "T-007", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2; memory/PROGRESS.md entry 2026-11-02T00:20Z; artifacts/m0-smoke/*.md; artifacts/screenshots/*.png; board state for M0; app http://localhost:7777; no sample case (M0)",
 "exercised": [
  "python3 tools/agent_prompt.py staff-engineer-reviewer",
  "python3 tools/board.py show T-007 (Notes triage 00:20:16Z, Handoff)",
  "cat reviews/T-007-staff-engineer.md (round 1)",
  ".venv/bin/python -m pytest tools/tests -q -> '38 passed in 7.80s'",
  "sed -n '1,20p' memory/PROGRESS.md -> line 10: '6. Conventional commits e37efb3, fbe5690; .gitignore complete; tag m0 pending M0 gate.' (no PASS)",
  "python3 tools/board.py list --milestone M0 -> 'T-006 M0 orchestrator in_review P0 AC 3/3' (T-001..T-004, T-006, T-007 in_review; T-005 in_progress)",
  "python3 tools/board.py show T-006 (AC 3 was edited at 00:16:19Z to 'git log shows conventional commits (tag m0 is applied when the M0 gate passes)')",
  "git tag -l -> empty; git log --oneline | head -> 1e9b348, de324d2, 65894f6, fbe5690, e37efb3",
  "curl -s localhost:7777/healthz -> {\"ok\": true}",
  "curl -s 'localhost:7777/api/activity?limit=6' (feed live and newest-first)",
  "file artifacts/screenshots/*.png -> m0-board-mobile.png PNG 390 x 1703; m0-board.png PNG 1440 x 1000",
  "cat artifacts/m0-smoke/agent-load-tests.md and live-feed.md",
  "grep -n m0-smoke memory/PROGRESS.md memory/STATE.md -> no match (rc=1)",
  "grep smoke board/activity.jsonl -> line 97 {event: smoke, text: 'live feed evidence probe', ts 00:20:16Z}",
  "grep compile_agents.py:198 and .claude/agents/paralegal-reviewer.md:18 (model-id follow-up claim holds)",
  "read docs/CONTRACT.md 4.8 items 1-7",
  "python3 tools/board.py validate reviews/T-007-staff-engineer.md -> ok"
 ],
 "verdict": "pass",
 "scores": {"round1_major_rejection_valid": 5, "round1_minors_addressed": 4, "s4_8_checks_recorded_honestly": 4, "evidence_reproducible": 4},
 "findings": [
  {"severity": "minor", "title": "PROGRESS does not cite the new m0-smoke evidence files",
   "evidence": "grep -n m0-smoke memory/PROGRESS.md memory/STATE.md -> no match (rc=1); PROGRESS.md:8 (item 4) and :6 (item 2) still name no evidence path; the round-1 minor fix asked for the paths to be cited in PROGRESS",
   "why_it_matters": "The M0 gate reads PROGRESS. The evidence exists but a reader of the milestone record cannot find it. This is a should-fix, not a spec violation.",
   "fix": "Append a PROGRESS line pointing item 2 at artifacts/m0-smoke/live-feed.md and item 4 at artifacts/m0-smoke/agent-load-tests.md (PROGRESS is append-only).",
   "acceptance_test": "grep -c m0-smoke memory/PROGRESS.md >= 2"},
  {"severity": "minor", "title": "Tag m0 is required by 4.8 item 6 but no card AC now requires it",
   "evidence": "docs/CONTRACT.md 4.8 item 6 ends 'tag m0'; T-006 title still says '... tag m0)' but its AC 3 was rewritten at 00:16:19Z to 'tag m0 is applied when the M0 gate passes'; T-006 is in_review AC 3/3 and `git tag -l` is empty; PROGRESS item 6 says 'pending M0 gate'",
   "why_it_matters": "This is not the round-1 major: the PROGRESS line is honest. The risk is that the tag falls through the cracks once every M0 card is done. This is a label-as-spec-adjacent process point, not a spec violation by this card.",
   "fix": "Make the m0 tag an explicit step of the M0 gate (milestones.md or a gate card) and append a PROGRESS line naming the tag when it is created.",
   "acceptance_test": "board/milestones.md M0 gate checklist lists 'git tag m0'; `git tag -l m0` prints m0 before M0 is marked done"},
  {"severity": "nit", "title": "Test count in PROGRESS is stale",
   "evidence": "PROGRESS.md:7 says '37 total'; `pytest tools/tests -q` now prints '38 passed in 7.80s'",
   "why_it_matters": "Point-in-time figure; harmless, but a reader may think a test was lost.",
   "fix": "Say '37 at the time of writing' or append the new count.",
   "acceptance_test": "PROGRESS count matches pytest output or is dated"},
  {"severity": "nit", "title": "Live-feed evidence exercises the endpoint, not the UI poll",
   "evidence": "artifacts/m0-smoke/live-feed.md: 'The UI polls this endpoint every 5 s (tools/board_ui.html, setInterval refresh)' is asserted by reference; before and after events share ts 2026-11-02T00:20:16Z",
   "why_it_matters": "Item 2 says the feed 'updates live'. The endpoint change is proven; the browser rendering the new row is not. Acceptable for M0.",
   "fix": "Optionally screenshot the feed after a board.py log, or read_page the activity panel.",
   "acceptance_test": "A saved screenshot or DOM dump shows the probe event in the rendered feed"}
 ],
 "whats_right": [
  "The round-1 major rested on a misquote; the orchestrator checked PROGRESS.md:10 and the board before rejecting, and PROGRESS marks item 6 open rather than PASS",
  "agent-load-tests.md records the native-load failure verbatim, uses the contract's fallback, and surfaces the model-id mismatch, which compile_agents.py:198 now handles",
  "38/38 tests pass, healthz is ok, and both screenshots are valid PNGs at 1440x1000 and 390x1703"
 ],
 "questions_for_chris": []}
```
