"""check_secrets.py regression tests (T-006 round 2). Keys are built by concatenation so this file never matches."""
import shutil, subprocess, sys
from pathlib import Path
import pytest

SRC = Path(__file__).resolve().parents[1] / "check_secrets.py"
KEY = "sk-" + "ant-" + "api03-" + "A" * 40


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "tools").mkdir()
    shutil.copy(SRC, tmp_path / "tools" / "check_secrets.py")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


def scan(repo):
    return subprocess.run([sys.executable, str(repo / "tools/check_secrets.py"), "--staged"], capture_output=True, text=True)


def stage(repo, name, content):
    p = repo / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    subprocess.run(["git", "add", "-f", "--", name], cwd=repo, check=True)


@pytest.mark.parametrize("name", ["my key.txt", "naïve.txt", "a\tb.txt", "dir with space/x.py"])
def test_odd_filenames_scanned(repo, name):
    stage(repo, name, f"k = '{KEY}'\n")
    r = scan(repo)
    assert r.returncode == 1 and KEY not in r.stdout


def test_rename_scanned(repo):
    stage(repo, "old.txt", "clean\n")
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x", "--no-verify"], cwd=repo, check=True)
    subprocess.run(["git", "mv", "old.txt", "new.txt"], cwd=repo, check=True)
    (repo / "new.txt").write_text("clean\n" + KEY + "\n")
    subprocess.run(["git", "add", "new.txt"], cwd=repo, check=True)
    assert scan(repo).returncode == 1


@pytest.mark.parametrize("name", [".env", ".env.local", ".envrc", "prod.env", ".ENV"])
def test_env_files_blocked(repo, name):
    stage(repo, name, "X=1\n")
    assert scan(repo).returncode == 1


def test_env_example_allowed(repo):
    stage(repo, ".env.example", "ANTHROPIC_API_KEY=\n")
    assert scan(repo).returncode == 0


@pytest.mark.parametrize("line", ["ANTHROPIC_API" + "_KEY=abc123xyz789", "ANTHROPIC_API" + "_KEY: 'k3y-value-here'",
                                  "gh" + "p_" + "B" * 36, "github_" + "pat_" + "C" * 50, "xox" + "b-" + "1" * 20,
                                  "AI" + "za" + "D" * 35, "sk" + "_live_" + "E" * 24,
                                  "-----BEGIN PGP PRIVATE KEY" + " BLOCK-----"])
def test_patterns(repo, line):
    stage(repo, "f.txt", line + "\n")
    assert scan(repo).returncode == 1


@pytest.mark.parametrize("line", ["ANTHROPIC_API_KEY=", "ANTHROPIC_API_KEY=<your key>", "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY",
                                  "os.environ.get('ANTHROPIC_API_KEY')", "ANTHROPIC_API" + "_KEY = os.getenv('X')", "pattern = r'sk-ant-[A-Za-z0-9_\\-]{8,}'"])
def test_no_false_positive(repo, line):
    stage(repo, "f.txt", line + "\n")
    assert scan(repo).returncode == 0, scan(repo).stdout


def test_repo_itself_clean():
    r = subprocess.run([sys.executable, str(SRC)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_utf16_scanned(repo):
    p = repo / "u.txt"; p.write_bytes(("k=" + KEY + "\n").encode("utf-16"))
    subprocess.run(["git", "add", "u.txt"], cwd=repo, check=True)
    assert scan(repo).returncode == 1


def test_git_failure_fails_closed(tmp_path):
    (tmp_path / "tools").mkdir(); shutil.copy(SRC, tmp_path / "tools" / "check_secrets.py")  # not a git repo
    r = subprocess.run([sys.executable, str(tmp_path / "tools/check_secrets.py"), "--staged"], capture_output=True, text=True)
    assert r.returncode == 1
