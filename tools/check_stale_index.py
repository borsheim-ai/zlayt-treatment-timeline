#!/usr/bin/env python3
"""Pre-commit guard against stale-index reverts (lessons: ec33bf0, 2fca530, 57a08ba).

Several workers share one checkout. A commit built from an index that predates other workers' commits
silently reverts their files. The signature: a staged path whose staged blob matches neither HEAD nor
the working tree (an old version), or a staged deletion of a file that still exists on disk.
Exit 1 with the offending paths; 0 otherwise. Works with GIT_INDEX_FILE temp indexes too.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"check_stale_index: BLOCKED (git {args[0]} failed: {r.stderr.strip()[:200]})")
        sys.exit(1)
    return r.stdout


def blob(spec: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", spec], capture_output=True, text=True)
    return r.stdout.strip() or None


def older_versions(path: str, depth: int = 200) -> set[str]:
    """Blob ids this path had in the last `depth` commits that touched it."""
    out = git("log", f"-{depth}", "--format=%H", "--", path).split()
    return {b for c in out[1:] if (b := blob(f"{c}:{path}"))}


def main() -> int:
    if not blob("HEAD"):
        return 0  # first commit
    hits = []
    raw =git("diff", "--cached", "--name-status", "--no-renames", "-z").split("\0")
    pairs = [(raw[i], raw[i + 1]) for i in range(0, len(raw) - 1, 2) if raw[i]]
    for status, path in pairs:
        on_disk = (ROOT / path).is_file()
        if status == "D":
            if on_disk:
                hits.append(f"{path}: staged as deleted but still on disk (stale index?)")
            continue
        staged = blob(f":{path}")
        head = blob(f"HEAD:{path}")
        work = git("hash-object", "--", path).strip() if on_disk else None
        # a partial stage (git add -p) is a new blob; a stale-index revert re-stages an *older committed* version
        if staged and staged != head and staged != work and staged in older_versions(path):
            hits.append(f"{path}: staged version is an older committed version (stale index would revert it)")
    if hits:
        print("check_stale_index: BLOCKED — this commit would revert work that is not yours.\n"
              "Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD\n"
              + "\n".join(hits))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
