# T-157 review r3: staff-engineer-reviewer (commit f31b146)

Verdict: **pass** (0 blockers, 0 majors, 0 findings). Verdict rule: no blocker, no major, so pass.

Scope: commit f31b146 (the r3 fix). HEAD at review time was f31b146. Three files changed: app/backend/case_list.py, memory/contracts/api.md, tests/unit/test_case_list.py. Reviewed on a `git archive f31b146` copy with untracked artifacts/review-evidence overlaid (the tests read it). Fixture backend, in-process TestClient, no live app URL, no UI.

Checks from the brief:
- Unconfirmed edit (edit_to_check) is in next_action after blockers and in timeline order. Code: case_list.py:147 keeps `or review.edit_unconfirmed(kind, r)` in the waiting set, and next_action (case_list.py:168-177) takes blockers first, then `waiting[0]`. The dropping mutant (K) turns 4 tests red. Blocker-precedence (H), timeline pick (A), seq/rank swap (C) and undated-first (D) also turn red.
- hitl.needs_review_open is on each case in GET /api/cases (case_list.py:197 via summary(), reached from api.py:218-226 summaries()). It equals the GET case waiting set for every library case (test_case_list.py:95, with an oracle built from GET case items, not from needs_review_order). Mutants K2 (pending-only count), R (count = needs_review) and Q (key removed) all turn the drift test red.
- tests/unit/test_case_list.py passes: 44 passed on the archive.

Closed from r2: finding 1 (major, unconfirmed edit drops out of the waiting set; mutant K survived in r2, is red now); finding 5 (plain_title dropped text after a lone '<'; mutant P is red now); finding 6 (demo gate tested by identity only; mutant M is red now, the absolute-pin test catches it).

Not in scope and not judged: the r2 api.py minors (entity-encoded titles, create with a non-text title, PATCH check order) and the frontend 'Untitled case' nit.

Outside this commit (noted, not a finding): tests/e2e/test_multicase.py:261-264 pops hitl.needs_review_open to exercise the pre-T-157 frontend fallback. The backend now always sends the key, so that e2e path no longer matches the live contract. Frontend lens; outside my review. The card notes also record that a backend worker ran `git checkout` on a shared file and lost another worker's uncommitted edits. The fix is lesson commit 33929ce (a hook against subagent checkout/restore). Process, not this commit.

Mutants (archive copy, one at a time, `.venv/bin/python -I`; baseline 44 passed; output saved to artifacts/review-evidence/T-157-r3-mutants.out):
- killed (red): K drop edit_unconfirmed from waiting (4 failed); K2 open count pending only (2); R open count = needs_review (1); Q open key dropped (2); A waiting[-1] (3); B first=None (2); G NOTHING_ACCEPTED not yielded (2); H blockers lose to waiting (2); C seq/rank swap (1); D undated first (3); P lone '<' drops words (1); M store.live_enabled drops ENABLE_LIVE (1).
- survived: none.

```json
{"card": "T-157", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f31b146 (r3 fix): app/backend/case_list.py, memory/contracts/api.md, tests/unit/test_case_list.py. HEAD at review time was f31b146. Reviewed on a git archive copy of f31b146 (scratchpad T-157-r3-f31b146) with untracked artifacts/review-evidence overlaid (cp -Rn). Fixture backend, in-process TestClient, no app URL, no UI. Cases under test: all library cases (drift test) plus the reworded entry on the shared fixture.",
 "exercised": [
  "read personas/staff-engineer.md in full; reviews/T-157-staff-engineer-r2.md; .claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md and feedback_exact_count_vs_presence.md",
  "python3 tools/board.py show T-157: status in_review, commits [926bf37, 852b060, f31b146], rounds 2, AC 1 done with the r2 evidence text; notes record the r3 request and the lost store.py edits",
  "git rev-parse --short HEAD -> f31b146; git status --short (working tree dirty with other roles' memory and app edits; the archive of the commit is what was reviewed)",
  "git show --stat f31b146 -> 3 files, 78 insertions, 5 deletions; git show f31b146 -- app/backend/case_list.py memory/contracts/api.md tests/unit/test_case_list.py (full diff read)",
  "git archive f31b146 | tar -x into scratchpad T-157-r3-f31b146; cp -Rn artifacts/review-evidence overlay; git show f31b146:<path> | cmp for the three in-scope files: identical",
  ".venv/bin/python -I -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '44 passed in 11.39s' (artifacts/review-evidence/T-157-r3-test_case_list.out)",
  "read on the archive: case_list.py needs_review_order (lines 134-157, incl. the edit_unconfirmed filter at 147), next_action (158-178), summary (181-199); api.py:218-226 GET /api/cases; present.py:311-350 GET case view (rejected items excluded from entries/flags); generator.resolved_placeholders (rejected placeholders only); test_case_list.py helper _waiting (405-407), drift test (around 80-100), tests at 410-430 (blocker first), 499-525 (library-case earliest waiting), and the r3 tests at the end of the file (unconfirmed edit, exact waiting set, demo gate pins, needs_review_open)",
  "grep -rn needs_review_open over the archive: app/backend/case_list.py:197 (the only producer), memory/contracts/api.md:700 and :707 (documented), tests/unit/test_case_list.py:95-96 and :587-594 (drift and direct test), app/frontend/overview.js:62-64 (consumer, read only)",
  "mutant runner scratchpad T-157-r3-mutate.py (python -I, each mutant on its own copy of the archive with review-evidence symlinked; each replacement asserted to match exactly once): output artifacts/review-evidence/T-157-r3-mutants.out. Baseline 44 passed; 12 mutants all red: K 4 failed, K2 2, R 1, Q 2, A 3, B 2, G 2, H 2, C 1, D 3, P 1, M 1",
  "first mutant run was stopped after it stalled copying the 1.5G review-evidence tree per mutant (process kill of my own PID 19447, verified by ps command line); the rerun with the symlink is the recorded result"
 ],
 "verdict": "pass",
 "scores": {"card_acs_implemented": 5, "tests_prove_acs": 5, "next_action_determinism": 5, "needs_review_open_contract": 5, "contract_consistency": 4, "title_plain_text": 4, "honest_failure": 4},
 "findings": [],
 "whats_right": [
  "The next_action pick is pinned by a reworded-entry scenario that makes the edit the earliest waiting item, and by an oracle built from GET case JSON (_waiting); dropping edit_unconfirmed from the waiting set now turns 4 tests red (mutant K).",
  "hitl.needs_review_open comes from the same needs_review_order that next_action reads, and the drift test checks it against the GET case waiting set for every library case; the three count mutants (K2, R, Q) all go red.",
  "The demo gate is pinned to absolute values (key alone is demo; ENABLE_LIVE=1 with claude-cli is live), and plain_title keeps the words after a lone '<' (mutants M and P both red)."
 ],
 "questions_for_chris": []}
```
