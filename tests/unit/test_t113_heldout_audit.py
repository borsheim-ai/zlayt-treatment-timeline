"""Held-out status is derived, not asserted (T-113 r2, staff-engineer F1): a control committed together with the prompt that names its words is not held out."""
import json
import pathlib
import re

import pytest

from evals import heldout_audit as A
from evals import j3_controls as J
from tests.unit._githist import REASON, single_commit

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ORDER = {c: i for i, c in enumerate(["c1", "c2", "c3", "c4", "c5"])}


def test_a_control_committed_with_the_prompt_is_refused():
    st, why = A.classify("c3", None, {"c3"}, ["teammate"], "a roommate or a coworker", ORDER)
    assert st == A.WITH_PROMPT and "c3" in why


def test_a_control_whose_word_is_in_the_prompt_is_refused_even_when_it_came_first():
    st, why = A.classify("c1", None, {"c3"}, ["smoking"], "Quitting smoking is not the course of care ending.", ORDER)
    assert st == A.TERM and "smoking" in why


def test_a_control_run_before_a_later_prompt_version_is_seen_not_clean():
    st, _ = A.classify("c1", "c2", {"c3"}, ["naproxen"], "a drug discontinued", ORDER)
    assert st == A.SEEN


def test_a_control_written_after_the_prompt_and_not_yet_run_is_clean_for_it():
    assert A.classify("c4", None, {"c3"}, ["naproxen"], "a drug discontinued", ORDER)[0] == A.CLEAN
    assert A.classify("c4", "c5", {"c3"}, ["naproxen"], "a drug discontinued", ORDER)[0] == A.CLEAN       # run after the last prompt edit: still clean for it


def test_a_control_not_in_git_is_not_clean():
    assert A.classify(None, None, {"c3"}, ["x"], "", ORDER)[0] == A.UNCOMMITTED


def test_the_next_prompt_version_makes_every_control_that_was_run_before_it_seen():
    assert A.classify("c1", "c2", {"c3", "c5"}, ["x"], "", ORDER)[0] == A.SEEN
    assert A.classify("c4", "c4", {"c3", "c5"}, ["x"], "", ORDER)[0] == A.SEEN


# ------------------------------------------------------------------ the committed files
HELD = [json.loads(l) for l in (ROOT / A.HELD_FILE).read_text().splitlines() if l.strip()]
HELD_J3 = [r for r in HELD if r["judge"] == "j3"]
PROMPT = (ROOT / A.PROMPTS / A.current_prompt_name()).read_text().lower()


def test_every_held_out_j3_control_has_distinguishing_words_and_none_is_in_the_current_prompt():
    assert {r["id"] for r in HELD_J3} == set(J.HELD_TERMS)
    for r in HELD_J3:
        terms = J.HELD_TERMS[r["id"]]
        assert terms and all(t == t.lower() for t in terms), r["id"]
        text = (r["excerpt_a"] + " " + r["excerpt_b"]).lower()
        assert all(t in text for t in terms), f"{r['id']}: a term is not in the control's own quotes"
        assert not [t for t in terms if t in PROMPT], f"{r['id']}: {terms} appears in the current judge_conflict prompt, so it is not held out"


def test_the_three_contaminated_controls_are_in_sample_with_their_labels_unchanged():
    ids = {r["id"]: r for r in J.build_rows()}
    for new, was, label in (("J3V17", "H3V16", "wrong"), ("J3V18", "H3V1", "wrong"), ("J3V19", "H3V3", "wrong")):
        assert ids[new]["split"] == "in_sample" and ids[new]["kind"] == label and was in ids[new]["why"]
        assert was not in ids


def test_the_prompt_names_the_words_of_the_three_demoted_controls():
    """Why they moved: the current prompt contains these words (so they could not stay held out)."""
    for w in ("teammate", "smoking", "gym"):
        assert w in PROMPT


@pytest.mark.skipif(single_commit(), reason=REASON)   # T-194: one-commit public snapshot
@pytest.mark.skipif(not A.available(), reason="no git history here (exported tree)")
def test_no_committed_held_out_control_was_written_with_the_prompt_or_names_its_words():
    rows = A.audit()
    assert {r["id"] for r in rows} == set(J.HELD_TERMS)
    bad = [(r["id"], r["status"]) for r in rows if r["status"] in (A.WITH_PROMPT, A.TERM, "no_terms")]
    assert not bad, bad


@pytest.mark.skipif(not A.available(), reason="no git history here (exported tree)")
def test_the_report_lines_state_the_derived_count_not_the_label():
    md = " ".join(A.summary_lines())
    assert "derived from git" in md and re.search(r"Clean held-out J3 controls: \d+ of 17", md)
