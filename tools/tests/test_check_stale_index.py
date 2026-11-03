"""check_stale_index: block stale-index reverts, allow partial staging (lessons ec33bf0, 2fca530, 57a08ba, e511778)."""
import shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def g(cwd, *a):
    return subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def repo(tmp_path):
    r = tmp_path / "r"
    (r / "tools").mkdir(parents=True)
    shutil.copy(REPO / "tools" / "check_stale_index.py", r / "tools")
    g(r, "init", "-q"); g(r, "config", "user.email", "t@t"); g(r, "config", "user.name", "t")
    (r / "f").write_text("a\n"); g(r, "add", "f", "tools"); g(r, "commit", "-qm1")
    (r / "f").write_text("a\nb\n"); g(r, "add", "f"); g(r, "commit", "-qm2")
    (r / "f").write_text("a\nb\nc\nd\n")  # another worker's uncommitted edit
    return r


def check(r):
    return subprocess.run([sys.executable, "tools/check_stale_index.py"], cwd=r, capture_output=True, text=True).returncode


def test_partial_stage_is_allowed(tmp_path):
    r = repo(tmp_path)
    (tmp_path / "partial").write_text("a\nb\nc\n")
    sha = g(r, "hash-object", "-w", str(tmp_path / "partial"))
    g(r, "update-index", "--cacheinfo", f"100644,{sha},f")
    assert check(r) == 0


def test_stale_older_version_is_blocked(tmp_path):
    r = repo(tmp_path)
    g(r, "update-index", "--cacheinfo", f"100644,{g(r, 'rev-parse', 'HEAD~1:f')},f")
    assert check(r) == 1


def test_staged_delete_of_file_on_disk_is_blocked(tmp_path):
    r = repo(tmp_path)
    g(r, "rm", "-q", "--cached", "f")
    assert check(r) == 1


def test_clean_index_passes(tmp_path):
    assert check(repo(tmp_path)) == 0
