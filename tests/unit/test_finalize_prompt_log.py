"""T-187 r5 / T-198 r3 (D-072): rule tests for evals/finalize_prompt_log.py and evals/privacy_tree_scan.py.

The first group uses a SYNTHETIC patterns file (made-up names, written to a tmp dir and passed via SNAPSHOT_PATTERNS), so it runs
anywhere and holds no private value. The last test runs the privacy reviewer's own checkers against the committed prompt log using the
real local deploy/.private_patterns; it is skipped when that git-ignored file is absent. It prints counts only.
"""
from __future__ import annotations

import collections
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SYN = "\n".join([
    "email\tzorbexcorp.net",
    "email\tpat.quillfeather@zorbexcorp.net",
    "email\tpat.quillfeather",
    "device\tquillphone-lab-3",
    "term\tglimmerbook",
    "<redacted-private>",
    "#@third\tNorthwindsor",
    "#@outside\tGlimmerbook",
    "#@outside\tGLMB",
    "#@outside\tNYSE:GLMB",
    "#@outside\t$GLMB",
    "#@personal\tJobfolders/Offerletters/note.pdf",
    "#@personal\tPatQuillfeather_",
]) + "\n"


def load(tmp_path, monkeypatch, name="fpl_syn"):
    pf = tmp_path / "patterns"
    pf.write_text(SYN, encoding="utf-8")
    monkeypatch.setenv("SNAPSHOT_PATTERNS", str(pf))
    spec = importlib.util.spec_from_file_location(name, ROOT / "evals" / "finalize_prompt_log.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def scrub(mod, text):
    return mod.scrub(text, "t", collections.Counter())


@pytest.fixture()
def fpl(tmp_path, monkeypatch):
    return load(tmp_path, monkeypatch)


def test_derived_terms_and_switch_precedence(fpl):
    assert "quillphone-lab" in fpl.TERMS["device"]                       # stem without the numeric suffix
    assert "Jobfolders" in fpl.TERMS["personal"]                          # top folder of a personal path
    assert "Offerletters" not in fpl.TERMS["personal"]                    # later pieces are often common words
    assert not [v for v in fpl.TERMS["term"] if v.lower() == "glimmerbook"]  # the outside name is not also a term


@pytest.mark.parametrize("text", [
    r'r"(?i)zorbexcorp*\.net"',               # regex quantifier between label and dot
    r"zorbexcorp?.net",
    r'("zorbex","corp.net")',                 # pieces
    "zorbexcorp.net",
    "zorbexcorp[.]net",
    r'x = "zorbex" + "corp" + ".net"',
    r"pat\.quillfeather\@zorbexcorp\.net",
    r'("pat.quill","feather")',               # tuple split of the local part
    r"pat\\*\.quillfeather",
])
def test_work_email_forms(fpl, text):
    out = scrub(fpl, text)
    assert "zorbex" not in out.lower() and "quillfeather" not in out.lower(), out
    assert fpl.M_PRIVATE in out


@pytest.mark.parametrize("text", ["Pat Quillfeather wrote this", "Author: Pat Quillfeather <pat@example.org>", "Pat Quillfeather - Dev", "Pat, Quillfeather"])
def test_public_name_prose_is_not_over_redacted(fpl, text):
    assert scrub(fpl, text) == text


@pytest.mark.parametrize("text", ["**Pat Quillfeather**", "Pat Quillfeather.", "Pat Quillfeather?", "*Pat Quillfeather*", "Pat Quillfeather"])
def test_public_name_with_trailing_wildcard_chars_has_no_hits(fpl, text):
    """Orchestrator T-199 finding: a personal term ending in `_` must not match the public name followed by `.`, `?` or `*`."""
    assert scrub(fpl, text) == text


def test_tree_scan_zero_hits_for_public_name(tmp_path, monkeypatch):
    pf = tmp_path / "patterns"
    pf.write_text(SYN, encoding="utf-8")
    monkeypatch.setenv("SNAPSHOT_PATTERNS", str(pf))
    monkeypatch.syspath_prepend(str(ROOT / "evals"))
    monkeypatch.syspath_prepend(str(ROOT / "tools"))
    for m in ("finalize_prompt_log", "privacy_tree_scan"):
        sys.modules.pop(m, None)
    import privacy_tree_scan as pts
    for text in ("Pat Quillfeather", "**Pat Quillfeather** wrote", "Pat Quillfeather? Pat Quillfeather.", "Pat Quillfeather <pat@example.org>"):
        assert not pts.hits(text, "f.md", pts.rules()), text
    for m in ("finalize_prompt_log", "privacy_tree_scan"):
        sys.modules.pop(m, None)


def test_trailing_separator_value_still_masks_file_names(fpl):
    assert "quillfeather" not in scrub(fpl, "PatQuillfeather_Resume.pdf").lower()
    assert "quillfeather" not in scrub(fpl, "Pat*Quillfeather_x").lower()


@pytest.mark.parametrize("text,expect", [
    ("tailscale status: quillphone-lab  online", "tailscale status: <device>  online"),
    ("tailscale status: quillphone-lab-3  online", "tailscale status: <device>  online"),
    ("Quillphone-Lab", "<device>"),
    ("QUILLPHONE_LAB", "<device>"),
])
def test_phone_stem(fpl, text, expect):
    assert scrub(fpl, text) == expect


@pytest.mark.parametrize("text", ["ls Jobfolders", "<home-path>", "(\"Job\", \"folders\")".replace("\"Job\", \"folders\"", "\"Jobfold\",\"ers\"")])
def test_job_folder_names(fpl, text):
    out = scrub(fpl, text)
    assert "jobfold" not in out.lower(), out


def test_switch_true_masks_as_outside_not_private(fpl):
    fpl.REDACT_OUTSIDE_PROJECT_NAME = True
    c = collections.Counter()
    out = fpl.scrub("We opened the Glimmerbook repo and glimmer_book? no: GLIMMERBOOK", "t", c)
    assert "<outside project>" in out and fpl.M_PRIVATE not in out
    assert {k for (_, k), n in c.items() if n} =={fpl.C_OUTSIDE}


def test_switch_false_leaves_the_name_even_if_listed_as_term(fpl):
    fpl.REDACT_OUTSIDE_PROJECT_NAME = False
    out = scrub(fpl, "We opened the Glimmerbook repo")
    assert out == "We opened the Glimmerbook repo"


@pytest.mark.parametrize("text, expect", [
    ("Work at Glimmerbook (NYSE: GLMB) since 2020", "Work at <outside project> (<outside project>) since 2020"),
    ("shares of $GLMB rose", "shares of <outside project> rose"),
    ("ticker glmb.", "ticker <outside project>."),
    ("the word glmbx and xglmb and GLMBs stay", "the word glmbx and xglmb and GLMBs stay"),   # a short ticker is whole-word only
])
def test_outside_ticker_forms(fpl, text, expect):
    assert scrub(fpl, text) == expect


@pytest.mark.parametrize("text,expect", [
    ("cd glimmerbook-v2/src/app/main.py && ls", "cd <outside project> && ls"),
    ("open glimmerbook/README.md", "open <outside project>"),
    ("<home-path>", "<home-path>"),
    ("<home-path>", "<home-path>"),
    ("path=../../Glimmerbook/docs/a.md;", "path=<outside project>;"),
])
def test_outside_path_tails(fpl, text, expect):
    fpl.REDACT_OUTSIDE_PROJECT_NAME = True
    assert scrub(fpl, text) == expect


@pytest.mark.parametrize("text", [
    r'r"(?i)glimmer\\*book"', '("glimmer","book")', "glimmer, book", "glimmer-book", "g l i m m e r b o o k", "x_glimmerbook_y", "loadGlimmerbookConfig",
    "gli​mmerbook", 'x = "glim" + "merbook"'])
def test_outside_name_forms(fpl, text):
    fpl.REDACT_OUTSIDE_PROJECT_NAME = True
    out = scrub(fpl, text)
    assert re.sub(r"[^a-z]", "", out.lower()).count("glimmer") == 0, out


def test_tree_scan_catches_the_reviewer_forms(tmp_path, monkeypatch):
    pf = tmp_path / "patterns"
    pf.write_text(SYN, encoding="utf-8")
    monkeypatch.setenv("SNAPSHOT_PATTERNS", str(pf))
    monkeypatch.syspath_prepend(str(ROOT / "evals"))
    monkeypatch.syspath_prepend(str(ROOT / "tools"))
    for m in ("finalize_prompt_log", "privacy_tree_scan"):
        sys.modules.pop(m, None)
    import privacy_tree_scan as pts
    rs = pts.rules()
    forms = {
        "gapped domain": r'r"zorbexcorp*\.net"',
        "phone stem": "quillphone-lab  online",
        "job folder": "ls Jobfolders",
        "outside tuple": '("glimmer","book")',
        "outside regex star": r"glimmer\\*book",
    }
    for label, text in forms.items():
        assert pts.hits(text, "f.md", rs), label
    assert not pts.hits("Pat Quillfeather and a glimmering book", "f.md", rs)
    for m in ("finalize_prompt_log", "privacy_tree_scan"):
        sys.modules.pop(m, None)


@pytest.mark.skipif(not (ROOT / "deploy" / ".private_patterns").is_file(), reason="local private patterns file absent")
def test_reviewer_focus_checker_reports_zero_on_committed_prompt_log():
    """T-187-r4-focus.py (the privacy reviewer's own counts) on HEAD's submission/prompt-log: every label must print n=0."""
    script = ROOT / "artifacts" / "review-evidence" / "T-187-r4-focus.py"
    if not script.is_file():
        pytest.skip("reviewer checker absent")
    r = subprocess.run([sys.executable, "-I", str(script), "HEAD"], capture_output=True, text=True, timeout=900)
    rows = [ln for ln in r.stdout.splitlines() if re.match(r"\S+\s+n=\s*\d+", ln)]
    assert rows, "checker printed no count rows"
    bad = [re.match(r"(\S+)\s+n=\s*(\d+)", ln).groups() for ln in rows if not re.match(r"\S+\s+n=\s*0\b", ln)]
    assert not bad, f"non-zero labels (counts only): {bad}"


# --- Chris's own words (only MASTER_PROMPT.md of them may be published) ------------------------------------------------------------
def _chris_fpl(tmp_path, monkeypatch, turns, master=""):
    """Load the module against a fake Claude Code project dir holding the given human turns (synthetic sentences, not real messages)."""
    import json
    proj = tmp_path / "proj"
    proj.mkdir()
    rows = [{"type": "user", "origin": {"kind": "human"}, "message": {"content": t}} for t in turns]
    rows.append({"type": "user", "origin": {"kind": "task-notification"}, "message": {"content": "zebra quokka narwhal wombat otter gecko heron ibis lemur"}})
    (proj / "s1.jsonl").write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    mp = tmp_path / "MASTER_PROMPT.md"
    mp.write_text(master, encoding="utf-8")
    mod = load(tmp_path, monkeypatch, name="fpl_chris")
    monkeypatch.setattr(mod.ex, "PROJ", proj)
    monkeypatch.setattr(mod, "MASTER_PROMPT", mp)
    mod.CHRIS_GRAMS = mod.load_chris_grams()
    mod.CHRIS_FIRST = {g[0] for g in mod.CHRIS_GRAMS}
    return mod


SENT = "please make the sidebar friendlier to blue pelicans and also quieter at night"


def test_chris_span_is_replaced_even_through_json_escapes_and_markup(tmp_path, monkeypatch):
    m = _chris_fpl(tmp_path, monkeypatch, [SENT])
    out, n = m.scrub_chris(f'x "text": "**Please** make the sidebar\\nfriendlier to blue pelicans, and also quieter at night." y')
    assert n == 1 and m.M_CHRIS in out and "pelicans" not in out and out.startswith('x "text": "') and out.endswith('." y')
    # seven words are below the threshold; eight are not
    assert m.scrub_chris("please make the sidebar friendlier to blue")[1] == 0
    assert m.scrub_chris("please make the sidebar friendlier to blue pelicans")[1] == 1


def test_chris_master_prompt_wording_and_other_origins_are_kept(tmp_path, monkeypatch):
    m = _chris_fpl(tmp_path, monkeypatch, [SENT, "the master prompt sentence has plenty of words in it to match"],
                   master="Text: the master prompt sentence has plenty of words in it to match.")
    assert m.scrub_chris("the master prompt sentence has plenty of words in it to match")[1] == 0
    assert m.scrub_chris("zebra quokka narwhal wombat otter gecko heron ibis lemur")[1] == 0   # a task notification is not Chris
    assert m.scrub_chris(SENT)[1] == 1


def test_inbox_event_text_is_omitted_but_acks_are_kept(fpl):
    import json
    line, ch = fpl.omit_inbox_text(json.dumps({"ts": "t", "event": "inbox", "agent": "chris", "card": None, "text": "anything he typed"}))
    assert ch and "anything" not in line and fpl.M_INBOX in line
    ack = json.dumps({"ts": "t", "event": "inbox_ack", "agent": "orchestrator", "card": None, "text": "acknowledged 1"})
    assert fpl.omit_inbox_text(ack) == (ack, False)
    assert fpl.omit_inbox_text(line)[1] is False   # idempotent


def test_session_with_human_turns_is_detected(tmp_path, fpl):
    import json
    a, b = tmp_path / "a.jsonl", tmp_path / "b.jsonl"
    a.write_text(json.dumps({"type": "user", "origin": {"kind": "human"}, "message": {"content": "hi"}}) + "\n")
    b.write_text(json.dumps({"type": "user", "message": {"content": "brief written by the orchestrator"}}) + "\n")
    assert fpl.has_human_turn(a) and not fpl.has_human_turn(b)


def test_snapshot_drop_chris(tmp_path, fpl):
    import json
    sys.path.insert(0, str(ROOT / "deploy"))
    snap = tmp_path / "snap"
    (snap / "board" / "inbox" / "archive").mkdir(parents=True)
    (snap / "board" / "inbox" / "archive" / "n.md").write_text("note")
    (snap / "MASTER_PROMPT.md").write_text("kept")
    (snap / "board" / "activity.jsonl").write_text(json.dumps({"event": "inbox", "agent": "chris", "text": "secret words here"}) + "\n")
    r = subprocess.run([sys.executable, "-B", "-I", str(ROOT / "deploy" / "snapshot_tool.py"), "drop-chris", str(snap)],
                       capture_output=True, text=True, env={**os.environ, "SNAPSHOT_PATTERNS": str(tmp_path / "patterns")})
    assert r.returncode == 0, r.stderr
    assert not (snap / "board" / "inbox").exists() and (snap / "MASTER_PROMPT.md").read_text() == "kept"
    assert "secret words" not in (snap / "board" / "activity.jsonl").read_text()
