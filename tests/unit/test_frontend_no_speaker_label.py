"""D-040: no user-facing text in app/frontend may say who spoke.

Scanned everywhere in app/frontend: "self-report", "self report", "patient statement", "patient self".
Scanned everywhere except the verbatim-record mock files: "patient states". Appendix A record 9 is quoted
verbatim there ("Patient states symptoms began after the January collision."), and that is record text, not a
label. The mock files are listed in VERBATIM_FIXTURES; any other file that says "patient states" fails.

The internal CSS class `.rv-selfreport` (no hyphen) is allowed; it is not user-facing text.
"""
import re
from pathlib import Path

FRONTEND = Path(__file__).resolve().parents[2] / "app" / "frontend"
BAD = re.compile(r"self[-\s]?report|patient\s+(?:statement|self)", re.I)
PATIENT_STATES = re.compile(r"patient\s+states", re.I)
ALLOWED = {"rv-selfreport"}
VERBATIM_FIXTURES = {"mock.js", "mock_sample.js", "mock_flags.js", "dev/mock-data.js"}
SUFFIXES = {".js", ".html", ".css", ".json", ".md", ".txt"}


def frontend_hits(rel, text):
    """Return 'rel:line: text' for every line of `text` (file `rel`, relative to app/frontend) that names the speaker."""
    hits = []
    check_states = rel not in VERBATIM_FIXTURES
    for n, line in enumerate(text.splitlines(), 1):
        found = False
        for m in BAD.finditer(line):
            if m.group(0).lower() in ALLOWED or "rv-selfreport" in line[max(0, m.start() - 3):m.end()]:
                continue
            found = True
        if not found and check_states and PATIENT_STATES.search(line):
            found = True
        if found:
            hits.append(f"{rel}:{n}: {line.strip()[:100]}")
    return hits


def test_no_speaker_label_in_frontend():
    hits = []
    for p in FRONTEND.rglob("*"):
        if not p.is_file() or p.suffix not in SUFFIXES:
            continue
        rel = p.relative_to(FRONTEND).as_posix()
        hits += frontend_hits(rel, p.read_text(errors="ignore"))
    assert not hits, "D-040 violation:\n" + "\n".join(hits)


def test_planted_self_report_fails_in_user_facing_file():
    assert frontend_hits("review.js", "// PLANT self-reported")
    assert frontend_hits("timeline.js", 'el("p", {}, "Patient self-report")')


def test_planted_patient_statement_fails_even_in_fixture():
    assert frontend_hits("mock_flags.js", '// PLANT a patient statement')
    assert frontend_hits("review.js", '// PLANT a patient statement')


def test_planted_patient_states_fails_in_user_facing_file():
    assert frontend_hits("timeline.js", 'el("p", {}, "an attribution such as patient states")')
    assert frontend_hits("narrative.js", "// PLANT Patient States")


def test_verbatim_record_text_in_mock_fixture_is_allowed():
    line = 'excerpt: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."'
    assert frontend_hits("dev/mock-data.js", line) == []
    assert frontend_hits("mock.js", line) == []


def test_internal_rv_selfreport_class_is_allowed():
    assert frontend_hits("review.css", ".rv-selfreport { background: #e8eefc; }") == []
    assert frontend_hits("review.js", 'el("span", { class: "rv-chip rv-selfreport" })') == []
