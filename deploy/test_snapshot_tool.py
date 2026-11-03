#!/usr/bin/env python3
"""Tests for deploy/snapshot_tool.py (T-199, D-070). Stdlib unittest; run: python3 -B deploy/test_snapshot_tool.py

Everything is planted in a temporary tree with a SYNTHETIC patterns file (fake values below); no real private value is read or
written. The shared finalize rules (evals/finalize_prompt_log.py) read the same file through $SNAPSHOT_PATTERNS.
"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "snapshot_tool.py"
sys.dont_write_bytecode = True

OUTSIDE, THIRD, TERM = "zzoutsideproj", "zzthirdparty.example", "zzquux-secret-term.example"
_TMP = tempfile.TemporaryDirectory()
PAT = Path(_TMP.name) / "patterns"
PAT.write_text(f"# synthetic\nterm\t{TERM}\n#@outside\t{OUTSIDE}\n#@third\t{THIRD}\n#@personal\tzzpersonal_file\n")
os.environ["SNAPSHOT_PATTERNS"] = str(PAT)
sys.path[:0] = [str(HERE.parent / "tools"), str(HERE.parent / "evals")]
import finalize_prompt_log as fpl  # noqa: E402


def split(v, n=None):
    n = n or len(v) // 2
    return v[:n], v[n:]


class Snap(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "tree"
        (self.root / "tools").mkdir(parents=True)
        (self.root / "tools" / "check_secrets.py").write_text((HERE.parent / "tools" / "check_secrets.py").read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def run_tool(self, cmd, pat=PAT, extra_env=None):
        env = dict(os.environ, SNAPSHOT_PATTERNS=str(pat), **(extra_env or {}))
        return subprocess.run([sys.executable, "-B", "-I", str(TOOL), cmd, str(self.root)], capture_output=True, text=True, env=env)

    def put(self, name, text):
        (self.root / name).write_text(text)

    def planted(self):
        a, b = split(OUTSIDE)
        t1, t2 = split(TERM, 10)
        h1, h2 = split(THIRD)
        self.put("planted_name.py", f'X = "{a}" + "{b}"\n')
        self.put("planted_name2.txt", f"{a}'  '{b}\n")
        self.put("planted_name3.md", f'{a}" "{b}\n')
        self.put("planted_term.py", f'Y = "{t1}" + "{t2}"\n')
        self.put("planted_term2.txt", f"{t1}\\{t2} and {TERM[:6]}[.]{TERM[-7:]}\n")
        self.put("planted_third.py", f"Z = '{h1}' + '{h2}'\n")
        self.put("planted_wild.txt", f"{OUTSIDE[:5]}?{OUTSIDE[6:]}\n")  # one-letter wildcard spelling

    FILES = ("planted_name.py", "planted_name2.txt", "planted_name3.md", "planted_term.py", "planted_term2.txt", "planted_third.py",
             "planted_wild.txt")

    def test_clean_tree_passes(self):
        self.put("ok.txt", "nothing private here, 'abc' + 'def'\n")
        r = self.run_tool("scan")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_scan_fails_on_split_fragments(self):
        self.planted()
        r = self.run_tool("scan")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        for f in self.FILES:
            self.assertIn(f"HIT {f}:", r.stdout, f)
        self.assertIn("normalized", r.stdout)
        out = (r.stdout + r.stderr).lower()
        for v in (OUTSIDE, THIRD, TERM):
            self.assertNotIn(v, out)  # the report names the file and the rule, never the value

    def test_redact_removes_split_fragments_then_scan_passes(self):
        self.planted()
        r = self.run_tool("redact")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r2 = self.run_tool("scan")
        self.assertEqual(r2.returncode, 0, r2.stdout + r2.stderr)
        self.assertIn("<outside project>", (self.root / "planted_name.py").read_text())

    def test_no_outside_line_fails_closed(self):
        noline = Path(self.tmp.name) / "noline"
        noline.write_text(f"term\t{TERM}\n")
        for cmd in ("scan", "redact"):
            r = self.run_tool(cmd, pat=noline)
            self.assertEqual(r.returncode, 2, cmd + r.stdout + r.stderr)
            self.assertIn("#@outside", r.stderr)

    def test_switch_off_lets_the_name_through(self):
        # the shared switch is evals/finalize_prompt_log.REDACT_OUTSIDE_PROJECT_NAME; flipped in a child process only
        self.put("name.txt", f"{OUTSIDE}\n")
        code = ("import sys,runpy;sys.path[:0]=[%r,%r,%r];import finalize_prompt_log as f;f.REDACT_OUTSIDE_PROJECT_NAME=False;"
                "sys.argv=['x','scan',%r];runpy.run_path(%r,run_name='__main__')"
                % (str(HERE.parent / "tools"), str(HERE.parent / "evals"), str(HERE), str(self.root), str(TOOL)))
        r = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True, env=dict(os.environ))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        on = self.run_tool("scan")  # switch on (default): the same tree fails
        self.assertEqual(on.returncode, 1, on.stdout + on.stderr)

    def test_allow_list_final_and_demo_video_but_nothing_else(self):
        png = b"\x89PNG\r\n\x1a\n" + b"\0" * 32
        (self.root / "artifacts" / "screenshots" / "final").mkdir(parents=True)
        (self.root / "artifacts" / "screenshots" / "other").mkdir(parents=True)
        (self.root / "artifacts" / "demo.webm").write_bytes(b"\x1a\x45\xdf\xa3" + b"\0" * 32)
        (self.root / "artifacts" / "screenshots" / "final" / "a.png").write_bytes(png)
        (self.root / "app" / "frontend" / "guided").mkdir(parents=True)
        (self.root / "app" / "frontend" / "guided" / "ladder.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>")
        r = self.run_tool("scan")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        (self.root / "artifacts" / "screenshots" / "other" / "b.png").write_bytes(png)
        (self.root / "artifacts" / "other.webm").write_bytes(b"\x1a\x45\xdf\xa3" + b"\0" * 32)
        r = self.run_tool("scan")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("screenshots/other/b.png", r.stdout + r.stderr)
        self.assertIn("artifacts/other.webm", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
