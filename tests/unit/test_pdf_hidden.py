"""T-087: text in the text layer that is not visible when the page is rendered is flagged per page and kept out of the case text
until the paralegal confirms it. Synthetic PDFs are generated here (tests/unit/_pdf_raw.py)."""
import pathlib

import pytest

from app.backend import pdf_checks, pdf_hidden, pdf_text
from tests.unit._pdf_raw import build, build_pages, text_page
from tests.unit.spawn_audit import audit, spawn_keys

pytest.importorskip("pypdfium2")

VISIBLE = "SYNTHETIC visit 03/04/2023 Dr. Rao: neck pain 6/10, ibuprofen prescribed."
HIDDEN = {
    "white": (b"BT /F1 12 Tf 1 1 1 rg 50 650 Td (PLANTED white text: patient was symptom free.) Tj ET", "blends_with_background"),
    "offpage": (b"BT /F1 12 Tf 0 g 900 650 Td (PLANTED off page text.) Tj ET", "off_page"),
    "tiny": (b"BT /F1 1 Tf 0 g 50 600 Td (PLANTED tiny text.) Tj ET", "tiny_font"),
    "invisible": (b"BT /F1 12 Tf 3 Tr 0 g 50 550 Td (PLANTED invisible mode text.) Tj ET 0 Tr", "invisible_render_mode"),
    "scaled_tiny": (b"q 0.1 0 0 0.1 0 0 cm BT /F1 20 Tf 0 g 500 5000 Td (PLANTED scaled tiny text.) Tj ET Q", "tiny_font"),
    "covered": (b"BT /F1 12 Tf 0 g 50 500 Td (PLANTED covered text.) Tj ET\n1 1 1 rg 40 490 300 40 re f", "blends_with_background"),
    "near_white": (b"BT /F1 12 Tf 0.97 g 50 450 Td (PLANTED nearly white text.) Tj ET", "blends_with_background"),
}


def pdf_with(*keys, page_text=VISIBLE):
    return build(text_page([page_text]) + b"\n" + b"\n".join(HIDDEN[k][0] for k in keys))


@pytest.mark.parametrize("key", sorted(HIDDEN))
def test_each_kind_of_hidden_text_is_flagged_with_its_reason(key):
    scanned = pdf_hidden.scan(pdf_with(key))
    hidden = scanned["pages"][1]["hidden"]
    assert len(hidden) == 1 and "PLANTED" in hidden[0]["text"]
    assert HIDDEN[key][1] in hidden[0]["reasons"]


def test_visible_text_is_never_flagged():
    scanned = pdf_hidden.scan(build(text_page([VISIBLE, "Second visible line: ROM limited."])))
    assert scanned["pages"][1]["hidden"] == [] and scanned["pages"][1]["text_objects"] >= 1


def test_small_but_legible_and_coloured_text_is_visible():
    c = text_page([VISIBLE]) + b"\nBT /F1 7 Tf 0 0 0.6 rg 50 600 Td (Footnote in small blue type.) Tj ET\nBT /F1 12 Tf 0.5 g 50 560 Td (Grey stamp.) Tj ET"
    assert pdf_hidden.scan(build(c))["pages"][1]["hidden"] == []


def test_white_text_on_a_dark_box_is_visible():
    c = b"0 g 40 600 300 40 re f\nBT /F1 14 Tf 1 g 50 612 Td (White on black label.) Tj ET"
    assert pdf_hidden.scan(build(c))["pages"][1]["hidden"] == []


def test_hidden_text_is_excluded_from_the_case_text_and_reported_per_page():
    got = pdf_checks.extract(pdf_with("white", "offpage", "tiny"))
    assert "PLANTED" not in got["text"] and VISIBLE in got["text"]
    ht = got["pdf_checks"]["hidden_text"]
    assert ht["checked"] and ht["excluded_until_confirmed"] and [p["page"] for p in ht["pages"]] == [1]
    page = ht["pages"][0]
    assert page["count"] == 3 and page["excluded"] and not page["confirmed"]
    assert {r for it in page["items"] for r in it["reasons"]} == {"blends_with_background", "off_page", "tiny_font"}
    assert all(it["why"] for it in page["items"])


def test_paralegal_confirmation_includes_the_hidden_text_for_that_page_only():
    two = build(text_page([VISIBLE]) + b"\n" + HIDDEN["white"][0])
    got = pdf_checks.extract(two, include_hidden="1")
    assert "PLANTED white text" in got["text"]
    page = got["pdf_checks"]["hidden_text"]["pages"][0]
    assert page["confirmed"] and not page["excluded"]
    assert got["pages"][0]["hidden_text_included"] is True
    assert "PLANTED" not in pdf_checks.extract(two, include_hidden="2")["text"]


def test_pdf_text_extract_applies_the_check_by_default():
    assert "PLANTED" not in pdf_text.extract(pdf_with("white"))["text"]


def test_a_pdf_whose_only_text_is_hidden_is_refused_with_the_hidden_pages_named():
    with pytest.raises(pdf_text.PdfError) as e:
        pdf_checks.extract(build(HIDDEN["white"][0] + b"\n" + HIDDEN["offpage"][0]))
    assert e.value.code == "pdf_only_hidden_text" and e.value.detail["hidden_text_pages"] == [1]


def test_removal_falls_back_to_the_visible_objects_when_the_strings_cannot_be_matched():
    out = pdf_hidden.remove_from_text("Visible A\nsomething the extractor spelled differently",
                                      [{"text": "PLANTED", "reasons": []}], "Visible A")
    assert out == "Visible A"


def test_removal_takes_a_whole_hidden_line_with_its_line_break():
    assert pdf_hidden.remove_from_text("line one\nHIDDEN words\nline three", [{"text": "HIDDEN words", "reasons": []}], "") == "line one\nline three"


def test_two_page_pdf_reports_only_the_page_with_hidden_text():
    two = build_pages([text_page([VISIBLE]), text_page(["Page two visible line."]) + b"\n" + HIDDEN["white"][0]])
    got = pdf_checks.extract(two)
    assert [p["page"] for p in got["pdf_checks"]["hidden_text"]["pages"]] == [2]
    assert "Page two visible line." in got["text"] and "PLANTED" not in got["text"]
    assert "PLANTED" not in pdf_checks.extract(two, include_hidden="1")["text"]       # confirming page 1 does not include page 2
    assert "PLANTED" in pdf_checks.extract(two, include_hidden="1,2")["text"]
    assert "PLANTED" in pdf_checks.extract(two, include_hidden="all")["text"]


def test_pdf_hidden_only_starts_local_children():
    """pdf_hidden.py starts local children and never an LLM (T-087). The AST audit in spawn_audit.py enforces it: no claude,
    anthropic or app.llm import, name or string; every spawn starts `ps` (RSS probe) or this interpreter running its own module."""
    src = pathlib.Path(pdf_hidden.__file__).read_text()
    assert audit(src, "pdf_hidden") == []
    assert spawn_keys(src) == ["lit:ps", "expr:sys.executable"]


# Each snippet is appended to the real module; the audit must report it. Every one of these passed the old regex allow-list.
BYPASSES = {
    "from_import_alias": "from subprocess import run as _sp_run\n_sp_run(['/usr/bin/curl', 'https://example.invalid'])\n",
    "module_alias": "import subprocess as sp\nsp.run(['/usr/bin/curl', 'https://example.invalid'])\n",
    "uncalled_attribute": "import subprocess\n_f = subprocess.run\n_f(['/usr/bin/curl', 'x'])\n",
    "getattr_lookup": "import subprocess\ngetattr(subprocess, 'run')(['/usr/bin/curl', 'x'])\n",
    "argv_in_variable": "import subprocess\n_argv = ['/usr/bin/curl', 'x']\nsubprocess.run(_argv)\n",
    "starred_argv": "import subprocess\nsubprocess.run(*[['/usr/bin/curl', 'x']])\n",
    "shell_true": "import subprocess\nsubprocess.run(['ps'], shell=True)\n",
    "rebind_subprocess": "subprocess = None\n",
    "claude_program": "import subprocess\nsubprocess.run(['claude', '-p', 'hi'], capture_output=True)\n",
    "claude_absolute_path": "import subprocess\nsubprocess.run(['/usr/local/bin/claude', '-p'])\n",
    "interpreter_runs_code": "import subprocess, sys\nsubprocess.run([sys.executable, '-c', 'import os; os.system(\"curl x\")'])\n",
    "interpreter_other_module": "import subprocess, sys\nsubprocess.run([sys.executable, '-m', 'app.llm.backends.claude_cli'])\n",
    "dunder_import": "__import__('subprocess').run(['/usr/bin/curl', 'x'])\n",
    "exec_string": "exec('import anthropic')\n",
    "os_system": "import os\nos.system('curl https://example.invalid')\n",
    "os_popen": "import os\nos.popen('curl https://example.invalid')\n",
    "anthropic_import": "import anthropic\n",
    "llm_package_import": "from app import llm\n",
    "llm_relative_import": "from ..llm import backends\n",
    "claude_string": "_NAME = 'claude'\n",
    "claude_identifier": "def _call_claude():\n    return None\n",
}


@pytest.mark.parametrize("snippet", list(BYPASSES.values()), ids=list(BYPASSES))
def test_pdf_hidden_audit_rejects_bypass(snippet):
    src = pathlib.Path(pdf_hidden.__file__).read_text() + "\n" + snippet
    assert audit(src, "pdf_hidden"), "the audit let this through"


def test_pdf_hidden_audit_rejects_a_spawn_that_is_not_the_probe_or_interpreter_module():
    src = pathlib.Path(pdf_hidden.__file__).read_text() + "\nimport subprocess\nsubprocess.run(['/usr/bin/curl', 'x'])\n"
    assert any("curl" in v for v in audit(src, "pdf_hidden"))
