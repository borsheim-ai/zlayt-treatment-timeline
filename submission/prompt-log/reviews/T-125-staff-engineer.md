# T-125 staff-engineer review (commit 4e294d7)

Verdict: pass. The commit adds one fixture file and no code. The fixture is needed, it matches the key the test asks for, and it sits in the recorded set, not the curated set, so D-056 is not breached.

Provenance (D-056), checked on the archive of c26ff04:
- The file is `tests/fixtures/llm/0a68ecb1....json` (key prefix 0a68ecb1; full name in the commit). The same path listed in tests/fixtures/llm/curated: 0 matches. Nothing shadows a recording.
- Its bytes equal `json.dumps(d, indent=1, sort_keys=True)` of its own content, which is what `app/llm/backends/fixture.py:write` produces, so the shape matches the recorder.
- `recorded_from` is claude-cli, claude-haiku-5-5, 2026-11-02T11:06:45Z, the same shape as its neighbours. The recorded time is a few seconds before the board claim (11:06:51Z), which is consistent with work starting before the claim.
- I cannot prove from the file that a live call happened; no tool can. The format, the key match and the absence of a curated copy are what can be checked, and all hold.
- Control: with the file moved aside, `test_t114_rates_and_demo_judges.py` fails 1 of 20 (the lib09 walk) with `llm call failed ... step=j4 ... prompt_hash=0a68ecb1...`. With it back, 26 passed (t114 plus tests/unit/test_curated_fixtures.py).
- Full unit suite on the archive: 2816 passed, 4 skipped.

```json
{"card": "T-125", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive c26ff04: tests/fixtures/llm/<0a68ecb1...>.json (commit 4e294d7), tests/unit/test_t114_rates_and_demo_judges.py, tests/unit/test_curated_fixtures.py",
 "exercised": ["pytest tests/unit -q on archive: 2816 passed, 4 skipped", "pytest test_t114_rates_and_demo_judges.py + test_curated_fixtures.py: 26 passed", "control: fixture moved aside -> t114 lib09 walk fails with J4 prompt_hash 0a68ecb1", "byte-compare of the fixture with the recorder's json.dumps(indent=1, sort_keys=True) output: equal", "ls tests/fixtures/llm/curated for the key: absent", "read fixture.py write() and test_curated_fixtures.py"],
 "verdict": "pass",
 "scores": {"correctness": 5, "determinism": 5, "llm_code_boundary": 5, "test_quality": 4},
 "findings": [],
 "whats_right": ["The fixture is a recorded answer in tests/fixtures/llm, not a curated judge file, and test_curated_fixtures.py passes with an empty allow-list.", "Cause is stated precisely (T-120 renumbered the flag, the J4 prompt carries the item id) and no prompt changed.", "Only the one missing key was added, so no recorded answer was overwritten."],
 "questions_for_chris": []}
```
