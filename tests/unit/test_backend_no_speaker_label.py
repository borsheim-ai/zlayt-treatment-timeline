"""D-040 backend follow-through (T-072 r2/r3): no user-facing backend string may say who spoke.

Sibling of test_frontend_no_speaker_label.py. It parses app/backend/*.py with ast and checks every string
literal that the code can show to a user (dict values, templates, f-string parts, plain assignments). Docstrings
and comments are skipped because they are not rendered. Internal ids such as the `patient_report` category key
do not match the pattern and are not flagged. Text files in app/backend (none today) are scanned as plain text.
"""
import ast
import re
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[2] / "app" / "backend"
BAD = re.compile(r"self[-\s]?report|patient\s+(?:statement|states|self)", re.I)
TEXT_SUFFIXES = {".html", ".json", ".txt", ".yaml", ".yml", ".md"}


def _docstring_ids(tree):
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant):
                if isinstance(body[0].value.value, str):
                    ids.add(id(body[0].value))
    return ids


def speaker_hits(source, name="<src>"):
    """Return 'name:line: text' for every user-facing string literal in `source` that names the speaker."""
    tree = ast.parse(source, name)
    skip = _docstring_ids(tree)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
            if BAD.search(node.value):
                hits.append(f"{name}:{node.lineno}: {node.value.strip()[:100]}")
    return hits


def test_no_speaker_words_in_backend_user_facing_strings():
    hits = []
    for p in sorted(BACKEND.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(BACKEND.parents[1])
        if p.suffix == ".py":
            hits += speaker_hits(p.read_text(encoding="utf-8", errors="ignore"), str(rel))
        elif p.suffix in TEXT_SUFFIXES:
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if BAD.search(line):
                    hits.append(f"{rel}:{n}: {line.strip()[:100]}")
    assert not hits, "D-040 violation in app/backend:\n" + "\n".join(hits)


def test_scanner_flags_a_planted_user_facing_string():
    src = 'REASONS = {"SUMMARY_DROPS_QUALIFIER": "The sentence drops a self-report marker."}\n'
    assert speaker_hits(src, "planted.py")
    assert speaker_hits('X = f"a patient statement {1}"\n', "planted.py")


def test_scanner_flags_planted_patient_states_in_reason_text():
    src = 'WHY = {"SUMMARY_DROPS_QUALIFIER": "an attribution such as patient states, a hedge"}\n'
    assert speaker_hits(src, "planted.py")
    assert speaker_hits('Y = "Patient States"\n', "planted.py")


def test_scanner_ignores_docstrings_comments_and_internal_ids():
    src = (
        '"""Module doc: self-report is discussed here."""\n'
        "# comment: self-report\n"
        "def f():\n"
        '    """Doc with a patient statement."""\n'
        '    return {"category": "patient_report", "title": "Reported onset"}\n'
    )
    assert speaker_hits(src, "clean.py") == []


def test_real_why_and_narrative_strings_name_no_speaker():
    for mod in ("why", "narrative"):
        src = (BACKEND / f"{mod}.py").read_text(encoding="utf-8")
        assert speaker_hits(src, f"{mod}.py") == [], mod
