# T-152 review: staff-engineer-reviewer (claude-haiku-5-5)

**Verdict: changes.** 0 blockers, 1 major, 2 minor, 2 nit.

**Claim check.** Confirmed: no golden edit is needed at the pinned HEAD. The accept-all export matches `evals/golden/sample.export.expected.txt` with zero changed lines (after one trailing newline per block). The golden test fails at `ba82071` (stage `extract`) and passes at `2db6ad2`. `generator.py:169` calls `why.join`, and `ba82071:app/backend/why.py` has no `def join`.

**Major (M1): the unit suite cannot be collected from a clean checkout.** `tests/unit/test_amounts_d059_api.py:11` and `tests/unit/test_amounts_d059.py:10,175` read `artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt`, which git does not track. On `25f585c`, `pytest tests/unit` stops with `Interrupted: 1 error during collection`. The card's count describes a working tree with untracked files, not a clean HEAD.

**Minor (m1): the golden-named test does not compare to golden.** `tests/unit/test_api_routes.py:159` is named `..._equals_golden_when_everything_accepted`, but its assertions (lines 170-176) never read `evals/golden`. The real golden checks are `tests/unit/test_export.py:31-36` and `tests/unit/test_curated_fixtures.py:88-94`.

**Minor (m2): the card's count is not reproduced.** The card says `tests/unit 3900 passed 1 skipped` at `2db6ad2`. My clean-archive run gave `3893 passed, 8 skipped, 0 failed`.

**Nit (n1): "byte-equal" is strip-equal.** The app output differs from the golden block by one trailing newline. The repo's own test normalises that way (`test_export.py:35`).

**Nit (n2): card premise.** The title blames T-139 narrowing for golden drift. The verified cause was the broken commit `ba82071`. The title and the "T-139 does not change the golden letter" sentence should say that.

**HEAD moved during review.** The pinned HEAD was `078c5ae`. It later became `25f585c` and then `d34182b`. At `078c5ae`, `test_export_equals_golden_when_everything_accepted` passed, but `test_e2e_contract::test_data_attributes_declared` failed because the committed conftest lacked `data-entry-id`. Commit `e2bb025` fixes that, and the test passes at `25f585c`, so I did not raise it as a finding. The d059 ledger problem is still present at `d34182b`.

Evidence and probe script: `artifacts/review-evidence/T-152-staff-engineer/golden_bytes.py`.

```json
{"card": "T-152", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive of pinned HEAD 078c5aed3abba34393733bffcaabd66859535158 (also archives 2db6ad2, ba82071, 25f585cfd99e910ca6555c773ae7afded2f0238c); HEAD moved to d34182b95bcd502a8a3ae1fe38b67e5b8491945e during review (only docs changed in 25f585c..d34182b); card handoff commits 2db6ad2 and ba82071; sample case evals/golden/sample.txt, curated fixture set, accept-all; no app URL used (e2e harness private server, shared :7860 not used); T-152 made no commit (git log --grep=T-152 is empty)",
 "exercised": [
  "read personas/staff-engineer.md and python3 tools/board.py show T-152 (handoff read)",
  "git rev-parse HEAD, git log, git merge-base --is-ancestor 2db6ad2 HEAD (yes); ba82071 ancestor of 2db6ad2 (yes)",
  "git show ba82071:app/backend/why.py | grep -n 'def join' (exit 1, absent); git show 2db6ad2:app/backend/why.py | grep -n 'def join' (62:def join); ba82071 app/backend/generator.py:169 calls why.join",
  "git archive 078c5aed... / 2db6ad2 / ba82071 / 25f585cf... extracted into scratchpad T-152-r1 dirs (not the working tree)",
  ".venv/bin/python -I -m pytest -p no:cacheprovider tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted -q: 078c5ae 1 passed; 2db6ad2 1 passed; ba82071 1 failed (status failed, stage extract, test_api_routes.py:30)",
  "export tests: pytest tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_api_routes.py -q at 078c5ae: 65 passed; test_api_routes -k export: 1 passed; at 25f585c the golden test + test_export + test_export_edge + test_curated_fixtures::test_make_curated_check_is_current: 33 passed",
  "golden byte probe (artifacts/review-evidence/T-152-staff-engineer/golden_bytes.py) at 078c5ae, FIXTURE_SET=curated, accept all entries+amounts+flags via API: status ready; letter strip-equal True, 0 changed lines; notes strip-equal True, 0 changed lines; byte-equal False (one trailing newline); charges_cents 839000",
  "tests/e2e/test_export_ui.py at 078c5ae and 25f585c with E2E_BASE_URL and ZLAYT_DB unset (private server from the archive): 4 passed, 0 skipped",
  "full tests/unit on archives: 078c5ae 2 failed, 3998 passed, 8 skipped, 1 error (with --continue-on-collection-errors; without it, Interrupted at collection); 2db6ad2 3893 passed, 8 skipped, 0 failed; 25f585c 1 failed, 4156 passed, 8 skipped, 1 error",
  "git ls-files --error-unmatch artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (not tracked); git status --short shows ?? for the directory; git ls-tree at d34182b shows no tracked file there",
  "grep of tests/unit/test_amounts_d059_api.py:11 and test_amounts_d059.py:10,175 for LEDGER read_text; git log --diff-filter=A: test_amounts_d059_api.py added in a0e2639 (after 2db6ad2)",
  "read tests/unit/test_api_routes.py:159-176, tests/unit/test_export.py:1-36, tests/unit/test_curated_fixtures.py:88-94, tests/e2e/test_export_ui.py",
  "python3 tools/board.py show T-152 and git status were read-only; no product or golden file was edited"
 ],
 "verdict": "changes",
 "scores": {"claim_accuracy": 4, "reproducibility": 2, "golden_gate_honesty": 3, "evidence_accuracy": 3},
 "findings": [
  {"severity": "major",
   "title": "Unit suite cannot be collected from a clean checkout: two tests read an untracked artifact",
   "evidence": "tests/unit/test_amounts_d059_api.py:11 LEDGER = (ROOT / 'artifacts' / 'review-evidence' / 'T-140-adjuster' / 'synthetic_ledger.txt'); tests/unit/test_amounts_d059.py:10 and :175 read the same file. git ls-files --error-unmatch artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt -> 'did not match any file(s) known to git'. git status --short shows '?? artifacts/review-evidence/T-140-adjuster/'. Repro: git archive 25f585cfd99e910ca6555c773ae7afded2f0238c | tar -x -C <empty dir>; cd there; .venv/bin/python -I -m pytest tests/unit -q -> 'Interrupted: 1 error during collection' (FileNotFoundError). With --continue-on-collection-errors: '1 failed, 4156 passed, 8 skipped, 1 error'. At 078c5ae: '2 failed, 3998 passed, 8 skipped, 1 error'.",
   "why_it_matters": "A fresh clone of HEAD cannot run the unit gate, so the suite does not pass reproducibly. The card's 'tests/unit ... passed' count only holds in a working tree that has untracked review-evidence files. test_amounts_d059_api.py was added in a0e2639, after the 2db6ad2 evidence commit, so the card's count does not see it.",
   "fix": "Inline the synthetic ledger text in the two test modules (preferred for a gate test), or commit the synthetic ledger under a tracked fixtures path and point both tests at it. Add a clean-archive unit run to the QA checklist.",
   "acceptance_test": "git archive HEAD | tar -x -C <empty dir>; cd <dir>; .venv/bin/python -I -m pytest tests/unit -q exits 0 with no collection errors and no FileNotFoundError."},
  {"severity": "minor",
   "title": "test_export_equals_golden_when_everything_accepted does not compare anything to the golden files",
   "evidence": "tests/unit/test_api_routes.py:159 def test_export_equals_golden_when_everything_accepted(env); assertions at lines 170-176 check '$6,240' absence, 'Billed charges stated in these records: $8,390.00', charges_cents 839000 and non-empty notes; line 175 comment: 'golden byte-equality runs on the curated fixture set (D-029, qa T-051)'. The real golden checks are tests/unit/test_export.py:31-36 (builder fed from golden files) and tests/unit/test_curated_fixtures.py:88-94 (make_curated.py --check replay). Card AC1 cites the misnamed test as the golden gate.",
   "why_it_matters": "A reader of the card will believe the API route output is compared with the golden. It is not. The pipeline-level replay still catches letter drift, so the gap is in naming and evidence, not coverage.",
   "fix": "Rename the test to describe what it asserts (for example test_export_accept_all_api_contract), or add an explicit letter and notes comparison against export_blocks() under FIXTURE_SET=curated. Cite test_curated_fixtures::test_make_curated_check_is_current as the golden gate in the card.",
   "acceptance_test": "Change one letter-visible string in the curated pipeline output in a scratch archive; the test named for the golden contract fails, or the card cites the replay test that does."},
  {"severity": "minor",
   "title": "Card evidence count 3900 passed / 1 skipped is not reproduced at 2db6ad2",
   "evidence": "git archive 2db6ad2 into a scratch dir; .venv/bin/python -I -m pytest -p no:cacheprovider tests/unit -q -> '3893 passed, 8 skipped in 233.83s' (exit 0). Card AC1 evidence: 'tests/unit 3900 passed 1 skipped'.",
   "why_it_matters": "Evidence that cannot be reproduced from the cited commit weakens the card's acceptance record. The difference (7 passes, 7 extra skips) is unexplained and may come from a different environment or a dirty tree.",
   "fix": "Restate AC1 evidence with the exact command, the commit sha, and the counts from a clean archive run.",
   "acceptance_test": "Re-run the command on git archive 2db6ad2; the counts in the card's AC1 evidence equal the output line."},
  {"severity": "nit",
   "title": "'byte-equal' in AC1 evidence is strip-equal (one trailing newline)",
   "evidence": "artifacts/review-evidence/T-152-staff-engineer/golden_bytes.py at 078c5ae, curated, accept-all: 'letter byte-equal: False | strip-equal: True'; tails: app ' these records: $8,390.00' vs golden block 'these records: $8,390.00\\n'. Repo test normalises with letter.rstrip('\\n') at tests/unit/test_export.py:35.",
   "why_it_matters": "The content matches; the word 'byte-equal' overstates what was compared.",
   "fix": "Say 'equal after stripping the trailing newline of the golden block' in AC1 evidence.",
   "acceptance_test": "Card wording matches the probe output."},
  {"severity": "nit",
   "title": "Card title premise (T-139 narrowing caused golden drift) is refuted by the handoff's own finding",
   "evidence": "Card title: 'fails since T-139 narrowing changed sample letter text'. Handoff: 'the earlier failure was at ba82071 ... 2db6ad2 fixed it'. Verified: tests/unit/test_api_routes.py ran at ba82071 -> status failed, stage extract (line 30 assertion); generator.py:169 why.join; ba82071 why.py has no def join; 2db6ad2 why.py:62 def join. Current golden letter is unchanged, so no golden edit is warranted.",
   "why_it_matters": "A card title that names the wrong cause sends the next reader to the golden file instead of the broken commit. The 'T-139 does not change the golden letter' sentence was only checked at HEAD, not before and after T-139.",
   "fix": "Retitle the card to the verified cause (broken commit ba82071 fixed by 2db6ad2) and drop or qualify the T-139 sentence.",
   "acceptance_test": "Card title and handoff name ba82071 and 2db6ad2, and the T-139 claim is either removed or backed by a before/after run."}
 ],
 "whats_right": [
  "The worker did not regenerate the golden: the accept-all export equals sample.export.expected.txt at HEAD with zero changed lines, so no golden edit was needed.",
  "The root cause is right: the golden test fails at ba82071 (stage extract, generator.py:169 calls why.join with no def join) and passes at 2db6ad2.",
  "The export E2E tests ran for real: tests/e2e/test_export_ui.py gave 4 passed and 0 skipped against a private server at both 078c5ae and 25f585c."],
 "questions_for_chris": []}
```
