"""T-079 pre-build check (from reviews/T-077-paralegal-r3.md): the library identifier denylist is case- and accent-insensitive and
covers the author-year and prose-cited names in research/case-library-sources-v2.md.

research/validate_library.py is researcher-owned; this is the qa-side guard that runs in the unit suite. It does not edit that file.
"""
import importlib.util
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("validate_library", ROOT / "research" / "validate_library.py")
VL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(VL)
DOC = (ROOT / "research" / "case-library-sources-v2.md").read_text()


def test_validator_self_test_passes():
    assert VL.self_test() == 0


def test_every_packet_in_the_library_passes_the_scan():
    files = sorted((ROOT / "evals" / "library").glob("case_*"))
    assert len(files) >= 30          # 15 packets x (txt + expected.json)
    assert VL.scan_library(files) == []


def test_mixed_case_and_accents_are_caught():
    for text in ["Seen by DR. GARZA", "dr. garza", "Dr. gArZa", "Ana RODRÍGUEZ", "ana rodriguez", "see brinjikji 2019", "BROUSSARD",
                 "i-45 southbound", "HOUSTON", "lewis brisbois"]:
        assert VL.scan_text(text), text


def test_author_year_and_prose_cited_names_from_the_v2_doc_are_caught():
    """Names written as 'Surname X.Y.' / 'Surname et al.' and bare names in the 'already cited' prose list, in any case."""
    names = VL.doc_author_names(DOC) | VL.doc_listed_citation_names(DOC)
    assert {"Fishbain", "Steinkamp", "Brinjikji", "Nakashima"} <= names
    for n in sorted(names):
        variants = (n, n.upper()) if n in VL.DENY_CAPITALISED else (n, n.upper(), n.lower(), n.swapcase())   # capitalised-only terms are also ordinary words
        for variant in variants:
            assert VL.scan_text(f"Reviewed by {variant} S.G. in clinic."), (n, variant)


def test_only_the_waddell_eponym_is_exempt():
    assert VL.ALLOWED_EPONYMS == ["Waddell"]
    assert VL.scan_text("0/5 Waddell signs.") == []
    assert VL.scan_text("Dr. Waddell saw her") == []        # exempt by design: the eponym is a clinical term, not a name check
    for org in ("FAIR Health", "Wal-Mart", "Lewis Brisbois", "Allstate"):
        assert VL.scan_text(f"billed by {org.upper()}"), org


def test_capitalised_only_terms_do_not_hit_ordinary_words():
    assert VL.scan_text("walked on the hills near home") == []
    assert VL.scan_text("Seen at HILLS clinic")
    assert re.fullmatch(r"[A-Za-z ]+", "FAIR Health")
