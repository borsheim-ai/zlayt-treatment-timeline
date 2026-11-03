"""Tests that audit provenance need the repository's real history; a one-commit public snapshot (deploy/make_public_snapshot.sh, T-194) has none."""
import pathlib
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
REASON = "requires_git_history: this repository has a single commit (public snapshot), so the commits this test cites are not present"


def commit_count(root=ROOT):
    """Number of commits reachable from HEAD, or None when there is no usable git repository."""
    if shutil.which("git") is None:
        return None
    r = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root, capture_output=True, text=True)
    return int(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip().isdigit() else None


def single_commit(root=ROOT):
    """True only for a real repository with exactly one commit. No repo at all is a different case, handled by each test's own skip."""
    return commit_count(root) == 1
