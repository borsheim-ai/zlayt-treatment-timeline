"""T-121 (T-060 pass-2 F9): optional one-line letter style, and the translation note as a bracketed, removable phrase at the end of the entry.
All code (export.py); the default letter for an English case is unchanged and still equals the golden."""
import pytest

from app.backend import export as X
from tests.unit import _golden as G
from tests.unit.test_export import build_case
from tests.unit.test_spanish_records import ES_QUOTE, ES_SUMMARY, MIXED, _wait, api   # noqa: F401  (api is a fixture)

NOTE = "[AI translation of the Spanish original; check before sending]"
NOTE_EDITED = "[Translation of the Spanish original, edited by reviewer; check before sending]"


def _case(label=None, extra=None):
    case = build_case()
    if label:
        e = next(e for e in case["entries"] if e["record_no"] == 1)
        e["translation_label"] = label
        e["summary"] = "Restrained driver rear-ended."
    return case


def test_default_letter_still_equals_the_golden_and_style_standard_is_the_same():
    letter, _ = G.export_blocks()
    case = build_case()
    assert X.build_export(case)["letter_text"] == letter.rstrip("\n")
    assert X.build_export(case, style="standard")["letter_text"] == letter.rstrip("\n")
    assert X.build_export(case, style=None)["letter_text"] == letter.rstrip("\n")


def test_oneline_gives_one_line_per_entry_built_from_the_same_items():
    case = build_case()
    out = X.build_export(case, style="oneline")["letter_text"]
    lines = out.split("\n")
    n_entries = len([e for e in case["entries"] if e["review_status"] == "accepted"])
    entry_lines = [l for l in lines if " — " in l and l.rstrip().endswith("]") and '"' in l]
    assert len(entry_lines) == n_entries
    first = entry_lines[0]
    assert first.startswith('January 9, 2026 — Austin EMS run report: "41M restrained driver, rear-ended at approx. 35 mph.')
    assert first.endswith('Transported to Central ER." [Ex. __ / Bates __]')
    assert "Source [" not in "\n".join(entry_lines)
    assert out.startswith("TREATMENT CHRONOLOGY\n\n")
    assert "Billed charges accepted from these records: $8,390.00" in out            # charges section unchanged
    assert out.count("BILLED CHARGES") == 1


def test_oneline_quote_is_still_a_substring_of_the_record_and_has_no_newline():
    case = build_case()
    out = X.build_export(case, style="oneline")["letter_text"]
    for e in case["entries"]:
        assert e["excerpt"] in out


def test_oneline_uses_the_export_config_and_the_pdf_page():
    case = build_case()
    case["export_config"] = {"exhibit": "7", "bates_prefix": "RIV-", "bates_start": 1}
    out = X.build_export(case, style="oneline")["letter_text"]
    assert '" [Ex. 7 / Bates RIV-0001]' in out
    case["export_config"] = None
    case["records"][0]["page"] = 3
    assert '" [Ex. __ / Bates __, p. 3]' in X.build_export(case, style="oneline")["letter_text"]


def test_oneline_is_deterministic_and_leaves_flags_out_of_the_letter():
    case = build_case()
    a = X.build_export(case, style="oneline")
    assert a == X.build_export(case, style="oneline")
    for bad in ("73 days", "Conflict", "REVIEWER NOTE", "INTERNAL"):
        assert bad not in a["letter_text"]


def test_unknown_style_is_refused():
    with pytest.raises(ValueError):
        X.build_export(build_case(), style="fancy")


@pytest.mark.parametrize("label,note", [("AI translation", NOTE), ("Translation (edited by reviewer)", NOTE_EDITED)])
def test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles(label, note):
    case = _case(label)
    std = X.build_export(case)["letter_text"]
    one = X.build_export(case, style="oneline")["letter_text"]
    for out in (std, one):
        assert "AI translation:" not in out and "Translation (edited by reviewer):" not in out
        assert not any(l.startswith(("AI translation", "Translation (edited")) for l in out.split("\n"))
        assert out.count(note) == 1
        line = next(l for l in out.split("\n") if note in l)
        assert line.endswith(note)
    assert "Restrained driver rear-ended.\n" in std                              # the summary line carries no label prefix
    lines = std.split("\n")
    i = lines.index(note)                                                          # standard style: its own bracket line, last line of the entry
    assert lines[i - 1].startswith("Source [Ex. __ / Bates __]: ") and note not in lines[i - 1] and (i + 1 == len(lines) or lines[i + 1] == "")
    assert next(l for l in one.split("\n") if note in l).startswith("January 9, 2026 — Austin EMS run report: ")


def test_english_entries_never_carry_the_note():
    assert "check before sending" not in X.build_export(build_case(), style="oneline")["letter_text"]


def test_api_style_param_and_unknown_style(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    for e in c.get(f"/api/cases/{tok}").json()["entries"]:
        assert c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"}).status_code == 200
    std = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    assert NOTE in std and "AI translation:" not in std and ES_SUMMARY in std
    one = c.get(f"/api/cases/{tok}/export?style=oneline")
    assert one.status_code == 200
    lt = one.json()["letter_text"]
    assert f'"{ES_QUOTE}"' in lt and lt.count(NOTE) == 1 and "Source [" not in lt
    assert c.get(f"/api/cases/{tok}/export?style=standard").json()["letter_text"] == std
    bad = c.get(f"/api/cases/{tok}/export?style=fancy")
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_style"


@pytest.mark.parametrize("label,note", [("AI translation", NOTE), ("Translation (edited by reviewer)", NOTE_EDITED)])
def test_oneline_translated_entry_carries_its_summary_on_the_same_line_as_the_note(label, note):
    case = _case(label)
    case["entries"][0]["summary"] = "Restrained driver rear-ended; neck pain 7/10."
    line = next(l for l in X.build_export(case, style="oneline")["letter_text"].split("\n") if note in l)
    assert " — English: Restrained driver rear-ended; neck pain 7/10. " + note in line
    assert line.index('"41M restrained') < line.index("English:") < line.index(note)
    assert "English:" not in "\n".join(l for l in X.build_export(build_case(), style="oneline")["letter_text"].split("\n"))     # English entries carry no such tail


def test_oneline_collapses_whitespace_only_and_keeps_one_line():
    case = build_case()
    e = case["entries"][0]
    case["records"][0]["excerpt"] = "Line one.\n  Line   two.\tEnd."
    e["excerpt"] = "Line one.\n  Line   two.\tEnd."
    out = X.build_export(case, style="oneline")["letter_text"]
    assert '"Line one. Line two. End." [Ex. __ / Bates __]' in out
    entry_line = next(l for l in out.split("\n") if l.startswith("January 9, 2026 — Austin EMS run report"))
    assert "\t" not in entry_line and "  " not in entry_line
    std = X.build_export(case)["letter_text"]
    assert '"Line one.\n  Line   two.\tEnd."' in std                # the standard style keeps the quote exactly


def test_oneline_translated_entry_with_a_multi_line_summary_stays_one_line():
    case = _case("AI translation")
    case["entries"][0]["summary"] = "Restrained driver\nrear-ended."
    line = next(l for l in X.build_export(case, style="oneline")["letter_text"].split("\n") if NOTE in l)
    assert "English: Restrained driver rear-ended." in line
