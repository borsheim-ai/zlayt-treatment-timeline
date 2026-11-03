"""T-167 (MVP UX audit F4/F7): no developer codes and no test-mode wording in anything the paralegal reads, or in the exported internal notes.
Reason codes stay in the API fields (`reasons`, `reason_code`, `code`); only the displayed sentences change.
The demo-mode edit message says plainly that the AI second check is not available in the demo and what she can do instead."""
import re
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.backend import calibration_route, export, narrative, reclassify, trace, why as WHY
from app.backend.api import create_app
from tests.unit.test_api_routes import run_case

# A reason code is SHOUTING_SNAKE (two or more words); ordinary capitals (PT, MRI, OCR, AI) are not.
CODE = re.compile(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b")
# Test-mode and developer wording that must never be shown to a paralegal.
BANNED = ("fixture", "curated", "older version", "server answered", "recorded replies", "golden case", "the server", "request failed", "http 5")
EDIT = "Persistent neck pain 6/10 with daily headaches noted."


def assert_plain(text, where=""):
    assert not CODE.search(text), f"raw reason code in {where}: {CODE.search(text).group(0)!r} in {text[:200]!r}"
    low = text.lower()
    for b in BANNED:
        assert b not in low, f"test/developer wording {b!r} in {where}: {text[:200]!r}"


# ---------------------------------------------------------------- why.py: every fixed sentence, with every judge shape
JUDGES = [None, {}, {"verdict": "unavailable", "reason_code": "JUDGE_NOT_RUN"},
          {"verdict": "unavailable", "reason_code": "NONE", "error_class": "LLMFailedFixtureMiss"},
          {"verdict": "unavailable", "reason_code": "NONE", "error_class": "LLMFailedTimeout"},
          {"verdict": "unavailable", "reason_code": "NONE"}]


@pytest.mark.parametrize("code", WHY.all_codes())
@pytest.mark.parametrize("judge", JUDGES, ids=lambda j: str(j and j.get("error_class") or j and j.get("reason_code")))
def test_every_why_sentence_is_plain(code, judge):
    assert_plain(WHY.why(code, judge), f"why({code})")


def test_judge_detail_and_models_sentences_are_plain():
    for c in ("ADDS_DIAGNOSIS", "SHOULD_BE_CHARGE", "TEXT_AMBIGUOUS", "WRONG_TYPE", "NOT_SUPPORTED_BY_QUOTE", "FACT_MISMATCH"):
        assert_plain(WHY.judge_detail(c), f"judge_detail({c})")
    assert_plain(WHY.MODEL_CONFLICT, "MODEL_CONFLICT")


def test_not_run_sentence_has_no_internal_code_prefix():
    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("The second AI check did not run or did not finish")
    assert not WHY.why("JUDGE_UNAVAILABLE", {"verdict": "unavailable", "reason_code": "JUDGE_NOT_RUN"}).startswith("JUDGE_NOT_RUN")


def test_demo_second_check_sentence_says_plainly_what_it_is_and_what_to_do():
    s = WHY.why("JUDGE_UNAVAILABLE", {"verdict": "unavailable", "reason_code": "NONE", "error_class": "LLMFailedFixtureMiss"})
    low = s.lower()
    assert "second check is not available in this demo" in low and "ai" in low
    assert "compare" in low and "quote" in low and "accept" in low         # what she can do instead
    assert "failed" not in low and "gave no usable answer" not in low         # not framed as a failure she caused


def test_live_failed_second_check_sentence_says_what_to_do():
    s = WHY.why("JUDGE_UNAVAILABLE", {"verdict": "unavailable", "reason_code": "NONE", "error_class": "LLMFailedTimeout"})
    low = s.lower()
    assert "second check is not available right now" in low and "compare" in low and "quote" in low and "accept" in low
    assert "failed" not in low and "gave no usable answer" not in low


def test_other_message_strings_are_plain():
    for k, s in narrative.REASONS.items():
        assert_plain(s, f"narrative.REASONS[{k}]")
    for k, s in trace.TRACE_WHY.items():
        assert_plain(s, f"trace.TRACE_WHY[{k}]")
    for k, s in reclassify.REFUSALS.items():
        assert_plain(s, f"reclassify.REFUSALS[{k}]")
    stale = calibration_route.stale_reason({"hashes": {"app/llm/prompts/a.md": "x"}}, {"app/llm/prompts/a.md": "y"})
    assert_plain(stale, "calibration stale reason")
    assert_plain(calibration_route.stale_reason({}, {}), "calibration stale reason (no hashes)")


# ---------------------------------------------------------------- the exported notes
def test_edit_reason_phrases_in_the_notes_carry_no_code():
    for c, s in export._EDIT_REASON_PHRASE.items():
        assert_plain(s, f"_EDIT_REASON_PHRASE[{c}]")
    for codes in (["JUDGE_UNAVAILABLE"], ["FIXTURE_MISS"], ["SOMETHING_NEW"], ["JUDGE_PARTIAL", "JUDGE_UNSURE"], []):
        assert_plain(export._edit_unconfirmed_why({"edit_state_reasons": codes}), f"_edit_unconfirmed_why({codes})")


def test_removed_narrative_lines_in_the_notes_carry_no_code():
    n = {"status": "pending", "sentences": [], "basis": {}, "removed": [
        {"text": "x", "entry_id": "e1", "reason": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": narrative.REASONS["SUMMARY_TOKEN_NOT_IN_EXCERPT"]},
        {"text": "y", "entry_id": "e2", "reason": "NOT_AN_ACCEPTED_ENTRY", "message": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"]},
        {"text": "Second check said no.", "entry_id": "e3", "reason": "JUDGE_UNSUPPORTED", "message": narrative.REASONS["JUDGE_UNSUPPORTED"]},
        {"text": "z", "entry_id": "e4", "reason": "JUDGE_UNAVAILABLE", "message": narrative.REASONS["JUDGE_UNAVAILABLE"]}]}
    lines = export._draft_paragraph(SimpleNamespace(narrative=n, in_entries=[]))
    text = "\n".join(lines)
    assert_plain(text, "draft-paragraph notes")
    assert "AI wording removed (failed a check: The sentence has a number" in text
    assert 'Removed: "Second check said no."' in text and "not supported by the cited quote" in text
    assert "Sentence removed (cites an entry that is not accepted)" in text


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)          # no live model: this is the demo
    d = str(tmp_path / "t167.sqlite")
    return TestClient(create_app(d, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def test_demo_edit_message_and_notes_are_plain_end_to_end(env):
    c = env
    tok = run_case(c)
    assert c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200
    j = r.json()
    # the codes stay in the API fields
    assert j["item"]["reasons"] == ["JUDGE_UNAVAILABLE"] and [w["code"] for w in j["warnings"]] == ["JUDGE_UNAVAILABLE"]
    # the displayed text is plain, says the check is not available in the demo and what she can do
    msg = j["warnings"][0]["message"]
    for text in (msg, j["item"]["why"]):
        assert_plain(text, "demo edit message")
        low = text.lower()
        assert "not available in this demo" in low and "compare" in low and "quote" in low and "accept" in low
    notes = c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
    assert_plain(notes, "internal notes")
    assert "edited; second check not available" in notes and "not yet confirmed" in notes
    # accept it after comparing: the other notes line (edited item accepted) is plain too
    assert c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "accept"}).status_code == 200
    notes = c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
    assert_plain(notes, "internal notes after accept")
    assert "after comparing it with the quote; second check not available" in notes


def test_sample_golden_notes_still_match_and_are_plain():
    from tests.unit._golden import export_blocks
    _, notes = export_blocks()
    assert_plain(notes, "golden internal notes")
