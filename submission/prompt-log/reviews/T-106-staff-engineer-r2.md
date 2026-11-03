# T-106 round 2 review: staff-engineer-reviewer (commit e3a62fa)

**Verdict: changes** (0 blockers, 1 major, 3 minor). Scope is the round-2 change only: pdf_hidden/pdf_ocr allow-list moved from a regex to an AST audit in `tests/unit/spawn_audit.py`. The narrative-panel item is not re-raised, per the orchestrator decision in the card notes (2026-11-02T06:20:44Z).

Answers to the three checks:

1. **Round-1 bypass rejected: yes.** The from-import alias (`from subprocess import run as _sp_run`) fails the audit at HEAD (`line 798: from subprocess import ...`). A scratch copy with that snippet appended to `app/backend/pdf_hidden.py` fails `test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children` and `test_provider.py::test_single_call_path` (2 failed). All 21 pdf_hidden and 6 pdf_ocr bypass snippets listed on the card are parametrized tests and pass (31 passed in the bypass/allow-list selection).
2. **ps RSS probe: narrow enough and acceptable as written.** The argv is a literal five-item list (`pdf_hidden.py:514`), shell is off, `timeout=2`, and the only dynamic item is `str(pid)`, an int from our own `Popen` (`pdf_hidden.py:559`). No user text reaches it. But the audit pins only argv[0] (`spawn_audit.py:132-134`), so the narrowness is a property of the code, not of the test. See F2.
3. **Clean-HEAD suite: fully green.** `pytest -q tests/unit` on a no-`.git` archive of e3a62fa gave `2184 passed, 4 skipped`, exit 0, on two runs. The 4 skips are the three no-git and env-gated tests (see Deterministic checks).

The gap that matters: the audit still walks only the `subprocess` name and `os.<attr>` on a literal `os` base. Process starts through an `os` alias, `from os import system`, `ctypes` libc calls, `asyncio`, or `_posixsubprocess` pass the audit and the real tests. That is F1 (major). Current `pdf_hidden.py` does not do any of these, so there is no present violation.

## Deterministic checks

- Archive: `git archive e3a62fa | tar -x -C <scratchpad>/T106_r2_archive`, then `git rev-parse --git-dir` gave `fatal: not a git repository`. Hashes match HEAD: `tests/unit/spawn_audit.py` sha256 `27837c64...5cf0` (same in the scratch copy), `app/backend/pdf_hidden.py` sha256 `9449758f...01cb5` (same as `git show e3a62fa:app/backend/pdf_hidden.py`).
- `cd <archive> && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit`, run 1: `2184 passed, 4 skipped in 157.89s (0:02:37)`, exit 0. Run 2 with `-rs`: `2184 passed, 4 skipped in 161.76s (0:02:41)`, exit 0. Skips: `test_eval_runner.py:794` (x2) and `:819` ("no git repository here"), `test_spanish_failsafe.py:223` (live judge eval, env-gated).
- Audit probe at HEAD, run with `python -I` from a heredoc (no file written; the audit module is a byte-identical copy in the probe dir), verbatim output:

```
HEAD pdf_hidden audit: []
HEAD pdf_hidden spawn keys: ['lit:ps', 'expr:sys.executable']
HEAD pdf_ocr audit: []
HEAD pdf_ocr spawn keys: ['expr:exe', 'expr:exe', 'expr:_which()']
REJECTED r1_from_import_alias -> line 798: from subprocess import ...
PASSED   x_os_module_alias -> no violation
PASSED   x_from_os_import_system -> no violation
PASSED   x_from_os_import_popen -> no violation
PASSED   x_ctypes_libc_system -> no violation
PASSED   x_asyncio_exec -> no violation
PASSED   x_posixsubprocess -> no violation
PASSED   x_ps_argv_tail_user_value -> no violation
PASSED   x_ps_plus_tail -> no violation
ocr_x_os_module_alias: PASSED; ocr_x_asyncio_exec: PASSED (against pdf_ocr.py)
```

- Scratch mutants (copies of the archive, never the project tree), each run with `.venv/bin/python -m pytest -q <node ids>`:
  - `mut_a` (round-1 from-import appended to pdf_hidden.py): **2 failed**. Both allow-list tests fail on `backend/pdf_hidden.py: line 798: from subprocess import ...`. Round 1 bypass is killed.
  - `mut_b` (`import os as o` / `o.system("curl https://example.invalid")` appended to pdf_hidden.py): **2 passed**.
  - `mut_c` (`import ctypes` / `ctypes.CDLL(None).system(b"curl ...")` appended to pdf_hidden.py): **2 passed**.
  - `mut_d` (`__import__("subprocess").run(["/usr/bin/curl", ...])` appended to app/backend/export.py): `test_provider.py::test_single_call_path` **1 passed**.
- Grep for `except`, `float(`, `sleep(`, `retry` in the added lines: not repeated here; the diff is 234 insertions, which I read in full for the audit and the three test files.

## Findings

**F1 (major): the AST audit still lets process starts through when they avoid the `subprocess` name.** `spawn_audit.py:14` `BANNED_MODULES` has no `asyncio`, `_posixsubprocess` or `ctypes`. The `os` check only fires on a literal `os` base (`spawn_audit.py:115` `if base == "os" and BANNED_OS_ATTR.match(attr)`), so `import os as o; o.system(...)` passes. `ImportFrom` (`spawn_audit.py:92-98`) checks only `subprocess`, banned modules and names matching `claude|anthropic|llm`, so `from os import system` passes. The probe and mutants above reproduce all five shapes, in pdf_hidden and in pdf_ocr. `pdf_hidden.py:38` imports `ctypes` today (used for PDFium buffers at lines 122-128, 225, 311, no libc call), which is why the audit cannot simply ban it.
- Why it matters: the audit is now the only enforcement that pdf_hidden and pdf_ocr start no unlisted program. The module docstring (`spawn_audit.py:5-6`) claims alias and lookup tricks are caught because "every check here walks the parsed tree". These are alias tricks the docstring names. Not a blocker: no such call exists in either module today (`pdf_hidden.py` has plain `import os`, no `os.system`/`popen`), so this is a weak guard, not a present violation.
- Fix: (a) flag any `Attribute` whose attr matches `BANNED_OS_ATTR`, whatever the base; (b) flag `from os import` of a name matching `BANNED_OS_ATTR`; (c) add `asyncio` and `_posixsubprocess` to `BANNED_MODULES`; (d) for `ctypes`, flag attributes and names `CDLL`, `PyDLL`, `cdll`, `pydll`, `LoadLibrary`, `system`, `popen` (the buffer and type uses stay allowed); (e) add the five shapes to `BYPASSES` in `tests/unit/test_pdf_hidden.py:112` and `OCR_BYPASSES` in `tests/unit/test_pdf_ocr.py:138`.
- Acceptance test: each new snippet appended to a copy of `app/backend/pdf_hidden.py` makes `test_pdf_hidden_audit_rejects_bypass[*]` fail. Mutant `mut_b`-style (`import os as o` + `o.system`) must fail `test_pdf_hidden_only_starts_local_children`. The same for pdf_ocr.

**F2 (minor): the audit does not pin the ps probe's argv tail.** `spawn_audit.py:132-134` checks argv[0] only. `subprocess.run(["ps", "-o", "rss=", "-p", "1", "/usr/bin/curl"])` passes (`x_ps_argv_tail_user_value`, `x_ps_plus_tail` above). The shipped probe (`pdf_hidden.py:514`) is fixed and acceptable, so this is a guard-strength issue, not a present violation.
- Fix: for `ps`, require `len(argv.elts) == 5` and literal `["-o", "rss=", "-p"]` at elts[1:4]; the fifth element may only be the pid expression used today.
- Acceptance test: appending the `x_ps_plus_tail` snippet to `pdf_hidden.py` fails `test_pdf_hidden_audit_rejects_bypass`.

**F3 (minor): the rest-of-app guard is still a line-start regex.** `tests/unit/test_provider.py:132` `elif re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M)` is the only check on the other app modules. `mut_d` (`__import__("subprocess")` in `app/backend/export.py`) passes `test_provider.py::test_single_call_path`. The card's AC names this test. The regex is pre-existing, but the round-2 commit kept it for every module except the two allow-listed ones.
- Fix: run `audit(src, <empty policy>)` on every module outside `app/llm/backends` (a policy with no allowed spawns and the same banned names), instead of the regex.
- Acceptance test: `mut_d`-style append to `app/backend/export.py` makes `test_single_call_path` fail.

**F4 (minor, pre-existing, not in e3a62fa, read from code, not exercised): the RSS probe swallows its failure and returns "no memory".** `app/backend/pdf_hidden.py:514-517`:
```
out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
return int(out.split()[0]) * 1024 if out else 0
except (OSError, ValueError, IndexError, subprocess.SubprocessError):
    return 0
```
On macOS, `RLIMIT_AS` is refused (`pdf_hidden.py:677`), so the 1 GiB parent-side ceiling (`pdf_hidden.py:66`, polled through this probe) is the only memory cap there. A `ps` timeout or error under memory pressure, which is when the cap matters, silently returns 0 and the ceiling does not fire for that poll. The wall-clock deadline still bounds the child, so this is bounded in time, not unbounded.
- Fix: count consecutive probe failures and raise `HiddenScanUnavailable("memory_unknown")` after N, or log the failure; do not return 0.
- Acceptance test: a test that makes `ps` raise `TimeoutExpired` and asserts the scan is refused or killed with a visible reason, not a clean result.

## Right

- Round-1 from-import bypass is killed: mutant `mut_a` fails two allow-list tests at HEAD's audit.
- The ps probe is narrow in code: a five-item literal argv, shell off, `timeout=2`, pid is an int from our own `Popen`.
- The clean-HEAD suite reproduces twice: `2184 passed, 4 skipped, 0 failed`, exit 0.

## Not exercised

- The UI and the app URL: not in scope for this round; no app was run.
- The sample case and the eval runner: no prompt, model, lexicon or schema change in e3a62fa.
- Security depth on `PATH` resolution of `ps`: outside my lens; deferred to security-reviewer.

```json
{"card": "T-106", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e3a62fa (HEAD, round 2); git archive copy with no .git at /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T106_r2_archive; files tests/unit/spawn_audit.py, tests/unit/test_pdf_hidden.py, tests/unit/test_pdf_ocr.py, tests/unit/test_provider.py, app/backend/pdf_hidden.py, app/backend/pdf_ocr.py; no app URL; no sample-case run (no prompt, model, lexicon or schema change)",
 "exercised": [
   "read personas/staff-engineer.md, board show T-106 (status in_review, rounds 1, notes incl. decision 2026-11-02T06:20:44Z), reviews/T-106-staff-engineer.md (round 1), .claude/agent-memory project_t106_review_patterns",
   "git show --stat e3a62fa (6 files, 234+/30-); git show e3a62fa -- app (pdf_hidden.py: signal import, __import__ removed)",
   "git archive e3a62fa | tar -x into a new empty scratch dir; git rev-parse --git-dir -> fatal: not a git repository; sha256 of spawn_audit.py and pdf_hidden.py match HEAD",
   ".venv/bin/python -m pytest -q tests/unit on the archive, two runs: 2184 passed, 4 skipped, 0 failed (exit 0; run 2 with -rs; skips test_eval_runner.py:794 x2, :819, test_spanish_failsafe.py:223)",
   ".venv/bin/python -m pytest -q -k 'bypass or only_starts or only_runs or single_call' on pdf_hidden, pdf_ocr, provider and provider_backends tests: 31 passed, 61 deselected",
   "python3 -I heredoc probe of spawn_audit.py (copy at HEAD) against pdf_hidden.py and pdf_ocr.py: round-1 from-import REJECTED; os module alias, from os import system/popen, ctypes libc system, asyncio.create_subprocess_exec, _posixsubprocess, ps argv tail PASSED (pdf_hidden); os alias and asyncio PASSED (pdf_ocr)",
   "scratch mutant copies (never the project tree): mut_a round-1 from-import appended to pdf_hidden.py -> 2 failed (test_pdf_hidden_only_starts_local_children, test_provider single_call_path); mut_b os alias -> 2 passed; mut_c ctypes CDLL.system -> 2 passed; mut_d __import__ subprocess in export.py -> test_single_call_path 1 passed",
   "read spawn_audit.py in full (147 lines); pdf_hidden.py:38, 66, 122-128, 225, 311, 514-517, 559-560, 677; pdf_ocr.py:58-64, 167; test_pdf_hidden.py:103-145; test_pdf_ocr.py:131-151; test_provider.py:115-134",
   "git status --short -- reviews/ (T-106 r2 file absent before this write)"
 ],
 "verdict": "changes",
 "scores": {"round1_bypass_rejected": 5, "ps_probe_narrow": 3, "audit_covers_process_start_routes": 2, "rest_of_app_guard_ast": 2, "clean_head_suite_green": 5, "no_swallowed_error_on_guard_path": 3},
 "findings": [
   {"severity": "major", "title": "AST audit still passes process starts that avoid the subprocess name (os alias, from os import, ctypes libc, asyncio, _posixsubprocess) in pdf_hidden and pdf_ocr",
    "evidence": "tests/unit/spawn_audit.py:14 BANNED_MODULES lacks asyncio/_posixsubprocess/ctypes; spawn_audit.py:115 `if base == \"os\" and BANNED_OS_ATTR.match(attr)` only fires on a literal os base; spawn_audit.py:92-98 ImportFrom checks no os names. Probe (python3 -I heredoc, audit at HEAD): PASSED x_os_module_alias 'import os as o\\no.system(...)', x_from_os_import_system, x_from_os_import_popen, x_ctypes_libc_system, x_asyncio_exec, x_posixsubprocess; ocr_x_os_module_alias and ocr_x_asyncio_exec PASSED against pdf_ocr.py. Mutants: mut_b (os alias appended to pdf_hidden.py) -> test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children 2 passed; mut_c (ctypes CDLL.system) -> 2 passed.",
    "why_it_matters": "The audit is now the only enforcement that pdf_hidden and pdf_ocr start no unlisted program, and its docstring (spawn_audit.py:5-6) says alias and lookup tricks are caught. These are alias tricks it names. Not a blocker: no such call exists in either module today (pdf_hidden.py imports os plainly; ctypes at pdf_hidden.py:122-128, 225, 311 is buffers only), so the guard is weak but nothing violates the constraint.",
    "fix": "(a) flag any Attribute whose attr matches BANNED_OS_ATTR regardless of base; (b) flag from-os imports of names matching BANNED_OS_ATTR; (c) add asyncio and _posixsubprocess to BANNED_MODULES; (d) for ctypes flag attributes/names CDLL, PyDLL, cdll, pydll, LoadLibrary, system, popen while keeping the buffer/type uses; (e) add the five shapes to BYPASSES (tests/unit/test_pdf_hidden.py:112) and OCR_BYPASSES (tests/unit/test_pdf_ocr.py:138).",
    "acceptance_test": "Each new snippet appended to a copy of app/backend/pdf_hidden.py makes test_pdf_hidden_audit_rejects_bypass[*] fail; the os-alias snippet appended to pdf_hidden.py makes test_pdf_hidden_only_starts_local_children fail; the same for pdf_ocr.py via test_pdf_ocr_audit_rejects_bypass[*]."},
   {"severity": "minor", "title": "ps probe argv tail is not pinned by the audit",
    "evidence": "tests/unit/spawn_audit.py:132-134 checks argv.elts[0] only. Probe: PASSED x_ps_argv_tail_user_value `subprocess.run(['ps', '-o', 'rss=', '-p', '1', '/usr/bin/curl'])` and x_ps_plus_tail `subprocess.run(['ps'] + ['/usr/bin/curl'])`. Shipped probe app/backend/pdf_hidden.py:514 is a fixed five-item literal list with pid = str(int from our own Popen).",
    "why_it_matters": "The ps exception is acceptable as written (fixed argv, shell off, timeout=2, no user text), so this is a guard-strength gap: the narrowness the card claims lives only in the code and not in the test that is supposed to enforce it.",
    "fix": "For ps: require len(argv.elts) == 5 and literal -o, rss=, -p at elts[1:4]; the fifth element may only be the pid expression used today.",
    "acceptance_test": "Appending the x_ps_plus_tail snippet to a copy of app/backend/pdf_hidden.py makes test_pdf_hidden_audit_rejects_bypass fail."},
   {"severity": "minor", "title": "Rest-of-app guard is still a line-start regex; a __import__ subprocess spawn passes test_single_call_path",
    "evidence": "tests/unit/test_provider.py:132 `elif re.search(r\"^\\s*(import|from)\\s+(anthropic|subprocess)\\b\", src, re.M)`. Mutant mut_d: `__import__(\"subprocess\").run([\"/usr/bin/curl\", \"https://example.invalid\"])` appended to app/backend/export.py -> `.venv/bin/python -m pytest -q tests/unit/test_provider.py::test_single_call_path` 1 passed.",
    "why_it_matters": "test_single_call_path is named in the card AC. The regex is pre-existing, but this commit kept it for every module except the two allow-listed ones, so the single-call-path invariant still rests on a line-start regex outside pdf_hidden and pdf_ocr.",
    "fix": "Run audit(src, <policy with no allowed spawns>) on every module outside app/llm/backends instead of the regex.",
    "acceptance_test": "The mut_d-style append to app/backend/export.py makes test_provider.py::test_single_call_path fail."},
   {"severity": "minor", "title": "RSS probe swallows its failure and returns 0 (no memory cap) on the one platform where it is the only cap",
    "evidence": "app/backend/pdf_hidden.py:514-517 `out = subprocess.run([\"ps\", \"-o\", \"rss=\", \"-p\", str(pid)], ..., timeout=2)...` / `except (OSError, ValueError, IndexError, subprocess.SubprocessError): return 0`. pdf_hidden.py:66 CHILD_RSS_BYTES = 1 GiB; pdf_hidden.py:677 comment: macOS refuses RLIMIT_AS. Read from code; pre-existing, not in e3a62fa; not exercised.",
    "why_it_matters": "On macOS the parent-side RSS poll is the only memory ceiling. A ps timeout or error under memory pressure, when the ceiling matters, silently reads as 0 and the ceiling does not fire for that poll. The wall-clock deadline still bounds the child, so the exposure is bounded in time.",
    "fix": "Count consecutive probe failures and raise HiddenScanUnavailable('memory_unknown') after N, or log the failure; do not return 0 on error.",
    "acceptance_test": "A test that makes ps raise subprocess.TimeoutExpired and asserts the scan is refused or killed with a visible reason, not a clean result."}
 ],
 "whats_right": [
   "The round-1 from-import bypass is killed: a scratch copy with it appended fails test_pdf_hidden_only_starts_local_children and test_provider single_call_path at HEAD.",
   "The ps RSS probe is narrow in code: a five-item literal argv, shell off, timeout=2, and its only dynamic item is an int pid from our own Popen.",
   "The clean-HEAD suite reproduces twice: 2184 passed, 4 skipped, 0 failed, exit 0."
 ],
 "questions_for_chris": []}
```
