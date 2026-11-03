#!/usr/bin/env python3
"""Pre-commit guard: the tree being committed must import on its own (lessons: 225e666, 2db6ad2).

Several workers share one checkout, so a commit can depend on code that is still uncommitted in the working tree
(present.py called conflict_candidates.checks(); generator.py called why.join). This writes the index (honours
GIT_INDEX_FILE) to a temp dir and imports the app there. Exit 1 with the error; 0 otherwise. Skipped when no app/ file
is staged.
"""
from __future__ import annotations
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = ("app.backend.api",)
# D-068 (T-181): the app has two front ends. /classic is loaded and exercised by test_no_console_errors.py; / (the guided app) and /classic's first paint by the guided shell smoke.
FRONTEND_SMOKE = ("tests/e2e/test_no_console_errors.py", "tests/e2e/guided/test_shell_smoke.py",
                  "tests/e2e/guided/test_golden_path.py")  # T-182 r2 lesson: / must always reach the sample
SMOKE = ("tests/unit/test_api_routes.py::test_create_sample_is_code_only_with_gap_flag",
         "tests/unit/test_api_routes.py::test_whole_case_after_run_matches_contract")


def main() -> int:
    staged = subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--name-only", "--diff-filter=ACM"], capture_output=True, text=True).stdout.split()
    # every staged .py must at least parse (lesson 6379c0b: a conftest.py SyntaxError broke the whole e2e suite)
    for p in staged:
        if p.endswith(".py"):
            src = subprocess.run(["git", "-C", str(ROOT), "show", f":{p}"], capture_output=True, text=True).stdout
            try:
                compile(src, p, "exec")
            except SyntaxError as e:
                print(f"check_index_imports: BLOCKED - {p} does not parse: {e}")
                return 1
    frontend = any(p.startswith("app/frontend/") for p in staged)
    if not frontend and not any(p.startswith("app/") and p.endswith(".py") for p in staged):
        return 0
    py = ROOT / ".venv" / "bin" / "python"
    py = str(py) if py.exists() else sys.executable
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["git", "-C", str(ROOT), "checkout-index", "-a", f"--prefix={tmp}/"], check=True)
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        r = subprocess.run([py, "-I", "-c", "import sys; sys.path.insert(0, '.'); " + "; ".join(f"import {m}" for m in MODULES)],
                           cwd=tmp, capture_output=True, text=True, env=env)
        if r.returncode == 0:
            # An import passes even when a call site names a function that only exists uncommitted (why.join, 2db6ad2),
            # so also create and run the sample case end to end on the fixture backend.
            r = subprocess.run([py, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *SMOKE],
                               cwd=tmp, capture_output=True, text=True, env=env)
            r.stderr = (r.stdout + r.stderr)
        smoke = [f for f in FRONTEND_SMOKE if (Path(tmp) / f).exists()]
        if r.returncode == 0 and frontend and smoke:
            # a frontend change must load a case with no console errors from the committed tree (lesson 6379c0b: a ReferenceError
            # in review.js passed the worker's tests because they ran against the working tree)
            r = subprocess.run([py, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *smoke],
                               cwd=tmp, capture_output=True, text=True, env={**env, "E2E_REQUIRE_DB": "1"})
            r.stderr = (r.stdout + r.stderr)
    if r.returncode != 0:
        print("check_index_imports: BLOCKED - the tree you are committing does not import on its own "
              "(it depends on uncommitted code; stage the missing hunks too):\n" + r.stderr.strip()[-1500:])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
