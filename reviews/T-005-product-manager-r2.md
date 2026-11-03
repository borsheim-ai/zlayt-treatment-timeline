# T-005 review, round 2 (product-manager-reviewer)

**Verdict: fail.** 1 blocker, 2 majors, 4 minors, 1 nit.

Round 1 had 7 findings. Five are resolved, one is partly resolved, and the blocker is still open in a new form.

| Round-1 finding | Status | Evidence |
|---|---|---|
| B1: restart item missing from NEEDS_CHRIS; no needs_chris cards | **Not resolved (new form).** Withdrawing the restart item was correct: T-020 was cancelled with a reason, and the reviewer write-guard hook fired on this reviewer's own Write, so native definitions and hooks are attached. But NEEDS_CHRIS now has 10 rows and only 2 have cards. | `board.py list --status needs_chris` lists only T-019 (#1) and T-021 (#3). NEEDS_CHRIS.md:9-16 holds rows #4-#11, none with a card. |
| M1: the restart protocol would not resume the run | Resolved. One residual minor: the Terminal path drops Remote Control. | RUNBOOK.md:25 has the `cd`; :29 has the `--dangerously-skip-permissions` flag; :31 has the spawn note; STATE.md:34 holds the heartbeat prompt; STATE.md is now in §4.5 shape |
| M2: CLAUDE.md names paths that don't exist | Mostly resolved. Residual minors: the release row has unmarked future paths, and the spawn line is stale. | CLAUDE.md:7,45,63 are marked; :53-54 list the tools and agent_prompt.py; :26 has `new` |
| M3: ASSUMPTIONS and DECISIONS record conclusions, not reasoning | Format is resolved. **ADR-000e misstates what was built (new major).** | ASSUMPTIONS.md:7-22 has basis, confidence, if-wrong and how-to-check columns; DECISIONS.md:18-51 splits ADR-000 into 000a-e |
| m1: no phone path to resume after STOP | Resolved | RUNBOOK.md:22 |
| m2: app URLs not marked as not live | Resolved | RUNBOOK.md:8-9 |
| m3: SCOPE_CUTS and STATE have no example entries | Resolved | SCOPE_CUTS.md has 13 rows; STATE.md is complete |

**What I exercised:**
- Read the round-1 review, the T-005 card, CLAUDE.md (86 lines), RUNBOOK, NEEDS_CHRIS (re-read after it changed on disk mid-review), STATE, ASSUMPTIONS, ADR-000a-e, SCOPE_CUTS, LESSONS, ENVIRONMENT and CONTRACT §1, §9 and §11.
- Ran `board.py list --status needs_chris` / `--status cancelled` / `status --brief`, and `show` on T-019, T-020 and T-021.
- Ran a path-existence script, saved as `artifacts/review-evidence/T-005-r2-pathcheck.py`.
- Ran `curl` on the healthz endpoint and on the tailnet https and http URLs, plus `tailscale serve status`.
- Ran `claude --help` and checked the restart flags.
- Read stop_guard.py:14 and serve_board.sh.
- Ran `git log --format=%ae`.
- Walked through the RUNBOOK restart and resume-after-STOP steps as Chris, read-only.

```json
{"card": "T-005", "persona": "product-manager-reviewer", "model": "claude-opus-5-5",
 "scope": "Round 2. Working tree 2026-11-02 ~01:30Z: CLAUDE.md, docs/RUNBOOK.md, memory/{STATE,ASSUMPTIONS,DECISIONS(ADR-000a..e),SCOPE_CUTS,LESSONS,ENVIRONMENT}.md, submission/NEEDS_CHRIS.md, needs_chris and cancelled cards T-019..T-021. Board http://localhost:7777 and https://<redacted-private>:7777. No sample case (M0).",
 "exercised": [
  "python3 tools/board.py show T-005: rounds=1, AC 1-3 checked",
  "python3 tools/board.py list --status needs_chris -> 'T-019 ... P2 ... (NEEDS_CHRIS #1)' and 'T-021 ... P2 ... (NEEDS_CHRIS #3)'; nothing else",
  "python3 tools/board.py list --status cancelled -> T-020 (NEEDS_CHRIS #2), with the cancel note 'Resolved without Chris: the Desktop host loaded .claude/agents mid-session'",
  "python3 tools/board.py status --brief -> needs_chris=2",
  "grep -rn 'NEEDS_CHRIS #[4-9]' board/ -> no hits; grep of activity.jsonl -> only the new events for T-019, T-020 and T-021",
  "read submission/NEEDS_CHRIS.md twice. It grew from 9 to 10 rows (#10 and #11 added) during the review.",
  "wc -l CLAUDE.md -> 86. Ran python3 -I artifacts/review-evidence/T-005-r2-pathcheck.py: Dockerfile, Makefile, README.md, run.sh and app/config.py (CLAUDE.md:64) are missing and unmarked; the other hits were false positives on relative names.",
  "curl http://localhost:7777/healthz -> 200; https://<redacted-private>:7777 -> 200; http://<redacted-private>:7777 -> 400; http://localhost:7860 -> 000 (expected, not live)",
  "tailscale serve status: https :7777 -> http://127.0.0.1:7777; 443 -> 4173; 8443 and 10000 -> 8787",
  "claude --help: -c/--continue, --dangerously-skip-permissions and --remote-control [name] all exist",
  "read .claude/hooks/stop_guard.py:14 (the Stop hook allows stopping when board/STOP exists) and tools/serve_board.sh (tmux, then the healthz curl)",
  "ls board/STOP -> absent. Did not create it.",
  "git log --format=%ae | sort | uniq -c -> '16 <redacted-private>'",
  "My own Write to the scratchpad was blocked by reviewer-write-guard, so the hook is attached natively",
  "Walked the RUNBOOK Restart steps 1-5 and the Stop/Resume steps as Chris on the phone and on the Mac, read-only"
 ],
 "verdict": "fail",
 "scores": {"map_completeness_for_fresh_agent": 4, "runbook_operable_by_chris": 4, "restart_readiness": 4, "needs_chris_quality": 2, "decisions_under_ambiguity_legibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "8 of 10 NEEDS_CHRIS items have no needs_chris card, including P1 item #7",
   "evidence": "submission/NEEDS_CHRIS.md:9-16 has rows #4-#11. `python3 tools/board.py list --status needs_chris` lists only T-019 (#1) and T-021 (#3). `grep -rn 'NEEDS_CHRIS #[4-9]' board/` finds nothing. CLAUDE.md:11: 'write submission/NEEDS_CHRIS.md + a needs_chris card'. CONTRACT §1.1: 'create a card in the needs_chris lane'. The handoff says 'submission/NEEDS_CHRIS.md has every item...', but the round-1 acceptance test ('one card per NEEDS_CHRIS row') fails 2/10. Priorities also diverge: row #1 is P1 in the file, but T-019 is P2.",
   "why_it_matters": "This is the same two-part rule that failed in round 1. Chris supervises from the board on his phone (RUNBOOK.md:6), so the needs_chris column is his view. It shows 2 items when there are 10, and the only P1 shown is mislabeled P2. Rows keep being added (#10 and #11 appeared during this review) with no card, so the process that creates rows does not create cards.",
   "fix": "Create one needs_chris card per row #4-#11 (or for each row that survives the §11.5 finding below). Set T-019 to P1. Make it a harness rule, either a board validator or a stop-guard check, that every NEEDS_CHRIS row number has a matching '(NEEDS_CHRIS #n)' card and the same priority.",
   "acceptance_test": "Script: count the row numbers in NEEDS_CHRIS.md and the cards from `board.py list --status needs_chris` whose title has '(NEEDS_CHRIS #n)'. The two sets are equal and the priorities match."},
  {"severity": "major",
   "title": "NEEDS_CHRIS holds items that don't need Chris (§11.5), so the real asks get buried",
   "evidence": "CONTRACT §11.5: 'NEEDS_CHRIS.md contains only items that genuinely require Chris (his story, personal numbers, HF Space name, optional own-voice video, final send)'. Row #4 asks 'How Zinda cites medical records in a demand', and row #5 asks about 'Zinda's treatment section'. Zinda Law Group is the fictional client in the spec scenario (spec/SPEC.md:8), so Chris cannot know this. It is a discovery question (Part 2 area 1), and ASSUMPTIONS A-106 already covers row #4. Row #3 says 'Nothing to do unless you want 443 back', which is an FYI already recorded as ADR-000e. Rows #8, #10 and #11 are product calls the team has already made and recorded as binding (row #10 cites ORCHESTRATOR_DECISIONS D-012).",
   "why_it_matters": "Appendix A grades self-direction and decisions made under ambiguity. A reader of the submitted NEEDS_CHRIS sees the team pass questions about a client's practices and its own product calls to the candidate, which looks like the team waiting on Chris. The asks only Chris can answer (#7 live vs demo, #9 budget, #6 email, #1 key) are mixed in with 6 that need no answer.",
   "fix": "Move rows #4 and #5 to Part 2 discovery questions and ASSUMPTIONS (A-106 already exists). Move #3 to ADR-000e and RUNBOOK only. Keep #8, #10 and #11 as recorded decisions in ORCHESTRATOR_DECISIONS. If you want Chris to see them, put them in one FYI line ('decisions you may want to overrule: D-0xx...') below the table, not as action rows.",
   "acceptance_test": "Every remaining NEEDS_CHRIS row falls under one of §11.5's categories, or needs a credential, account or spend decision only Chris can give. No row's exact action is 'Nothing to do'."},
  {"severity": "major",
   "title": "ADR-000e describes a setup that wasn't built, and its rejected alternative is the one in use",
   "evidence": "memory/DECISIONS.md:50 says 'the phone reaches `http://<node>:7777` and `:7860` (no TLS termination from serve)'. DECISIONS.md:51 rejects 'pick other serve HTTPS ports (extra mapping state...)'. What is live: `tailscale serve status` shows 'https://<redacted-private>:7777 ... proxy http://127.0.0.1:7777', and RUNBOOK.md:6 and :32 use https with `tailscale serve --bg --https=7777`. `curl http://<redacted-private>:7777` returns 400; the https URL returns 200.",
   "why_it_matters": "This is the ADR round 1 asked for, as the plainest example of a decision under ambiguity. As written, the record contradicts the RUNBOOK and the running system. A fresh agent or a hiring-panel reader who follows ADR-000e gets a URL that returns 400. A decision log that misstates the decision fails the 'explained plainly' criterion more than a missing one does.",
   "fix": "Architect: rewrite the ADR-000e Decision and Consequences to match what was built: 'serve --https=7777 and --https=7860, TLS from tailscale serve; never reuse an occupied serve port (run `tailscale serve status` first)'. Move the plain-http option into Alternatives. Mention that 10000 -> 8787 is also Chris's.",
   "acceptance_test": "`grep -n 'http://<node>' memory/DECISIONS.md` returns nothing. ADR-000e's URL matches RUNBOOK.md:6 and returns 200 with curl."},
  {"severity": "minor",
   "title": "The Terminal restart path silently drops Remote Control, and with it the phone steer and resume path",
   "evidence": "RUNBOOK.md:29 `claude --continue --dangerously-skip-permissions` has no `--remote-control`, though `claude --help` lists '--remote-control [name]  Start an interactive session with Remote...'. RUNBOOK.md:16 (direct steer) and :22 ('from the phone, type into this Claude session (Remote Control)') both depend on it. RUNBOOK does not say that a restart needs the Mac.",
   "why_it_matters": "After a reboot, Chris restarts from the Mac and walks away. If he then STOPs from the board, he cannot resume from the phone. The inbox doesn't help either, because a stopped orchestrator doesn't read it.",
   "fix": "Add `--remote-control zlayt` to the Terminal line, or a step 'then run /remote-control and open it on the phone'. Add one line: 'Restart needs the Mac; the phone can only steer once step 3 is done.'",
   "acceptance_test": "RUNBOOK Restart step 3 (Terminal) gives a command that brings back the phone path used in RUNBOOK.md:22."},
  {"severity": "minor",
   "title": "Agent spawning is described two ways: CLAUDE.md and ADR-000d say fallback, STATE says native",
   "evidence": "CLAUDE.md:54: '**how agents are spawned here:** general-purpose subagent ... (host didn't load `.claude/agents` created mid-session)'. ADR-000d (DECISIONS.md:39-44): 'every worker and reviewer is spawned as a general-purpose subagent'. Against that: STATE.md:26 'Reviewers: native agent types (*-reviewer), loaded mid-session', LESSONS.md:11 'Switched reviewers/workers to native types', and T-020 cancelled for that reason.",
   "why_it_matters": "CLAUDE.md is the map a compacted agent reads first. Under the fallback the write-guard hook was 'instruction-only' (LESSONS.md:8), so spawning that way gives a weaker guard.",
   "fix": "CLAUDE.md:54: 'native agent types; fallback `agent_prompt.py` if Agent type not found'. Architect: amend ADR-000d's status to 'superseded in part: native load works; fallback retained'.",
   "acceptance_test": "`grep -n \"didn't load\" CLAUDE.md` returns nothing, and CLAUDE.md, STATE.md and ADR-000d name the same default."},
  {"severity": "minor",
   "title": "CLAUDE.md release ownership row names 5 future files without an (Mx) marker",
   "evidence": "CLAUDE.md:64 lists `Dockerfile`, `README.md`, `Makefile`, `run.sh` and `app/config.py`. All 5 are missing (artifacts/review-evidence/T-005-r2-pathcheck.py output: 'MISSING Dockerfile lines=[64] marked_lines=[]' etc.). Every other future path is now marked (:7, :45, :59, :63).",
   "why_it_matters": "This is the residual from round-1 M2. It is low risk because CLAUDE.md:8 gives the general rule, but it is inconsistent with the rest of the map.",
   "fix": "Append '(M4)' to the release row.",
   "acceptance_test": "The pathcheck script reports no unmarked missing path."},
  {"severity": "minor",
   "title": "Several NEEDS_CHRIS 'exact actions' are 'Reply via inbox.' with no answer format",
   "evidence": "NEEDS_CHRIS.md rows #5, #8, #10 and #11 have the exact action 'Reply via board inbox.' / 'Reply via inbox.'. Rows #4 and #7, by contrast, give the shape of the answer ('\"demo-only\" or \"live with cap $X/day\"').",
   "why_it_matters": "§5 asks for 'each item with the exact action'. A yes/no answer with a stated default is a 10-second tap on a phone; an open question is not. (If the §11.5 finding moves these rows out, this finding goes away.)",
   "fix": "For any row that stays, write the action as 'Reply \"yes\" / \"no\" (default: no)'.",
   "acceptance_test": "Every exact-action cell names the expected reply or a concrete step."},
  {"severity": "nit",
   "title": "The T-020 cancel note gives an event time later than the note itself",
   "evidence": "T-020 note stamped 2026-11-02T00:22:43Z says 'loaded .claude/agents mid-session (~00:30Z...)'.",
   "why_it_matters": "This is a small record-accuracy slip in the audit trail the hiring panel may read.",
   "fix": "Append a corrective note with the right time; don't edit the existing note.",
   "acceptance_test": "T-020 notes give a consistent load time."}
 ],
 "whats_right": [
  "STATE.md is now enough to resume: in-flight cards, next 3 actions, risks, URLs and the full heartbeat prompt (STATE.md:34). Keep it this complete.",
  "ASSUMPTIONS now shows reasoning (basis, confidence, if wrong, how to check), and SCOPE_CUTS has 13 costed rows. This is the 'decisions under ambiguity' evidence Appendix A grades.",
  "Withdrawing the restart ask once native load worked, with a reason on the card, was the right call. The hook firing on this reviewer's own Write confirms it."
 ],
 "questions_for_chris": [
  "NEEDS_CHRIS.md:11 prints your work email (<redacted-private>) inside a file that goes in the submission. `git log` confirms all 16 commits use it. Do you want the address kept out of submission files as well as out of future commits? (Privacy is outside my lens; flagging only.)"
 ]}
```
