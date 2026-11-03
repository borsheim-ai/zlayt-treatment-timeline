"""T-105 (T-100 r2 F1-F3): the added-qualifier word lists (attribution, hedge, approximation) are built from ONE place, app/llm/lexicon.yaml
(code_lists.added_qualifier), and read by the English and the Spanish path alike. Misses from the r2 probe are refused; faithful paraphrases are not."""
import pytest

from app.backend import grounding as GR, lexicon, spanish_text as ST

Q = "Pain 4/10, improving."


def _new(summary, quote=Q):
    return GR.new_tokens(summary, quote)


@pytest.mark.parametrize("summary", [
    "Reports pain 4/10, improving.", "Patient describes pain 4/10, improving.", "Patient noted pain 4/10, improving.", "Patient indicates pain 4/10, improving.",
    "Pain 4/10, improving according to the patient.", "Pain 4/10 (self-reported), improving.",
    "Pain 4/10, seems to be improving.", "Pain 4/10, potentially improving.", "Pain 4/10, apparently improving.", "Pain 4/10, suspected improvement.",
    "Pain 4/10, consistent with improvement.", "Pain 4/10, tends to improve.",
    "Pain nearly 4/10, improving.", "Pain almost 4/10, improving.", "Pain close to 4/10, improving.", "Pain circa 4/10, improving.", "Pain ca. 4/10, improving.",
    "Pain about four out of ten, improving."])
def test_r2_misses_are_refused(summary):
    assert _new(summary), summary


@pytest.mark.parametrize("summary,quote", [
    ("Patient describes pain 4/10.", "Patient describes pain 4/10."), ("Seems improved.", "Seems improved."), ("Pain nearly 4/10.", "Pain nearly 4/10."),
    ("Reports pain 4/10.", "Reports pain 4/10."), ("Pain apparently improving.", "Pain apparently improving."), ("Pain circa 4/10.", "Pain about 4/10."),
    ("Pain ca. 4/10.", "Pain ~4/10."), ("Patient indicates pain 4/10.", "Pt states pain 4/10.")])
def test_a_quote_that_carries_the_kind_lets_the_summary_carry_it(summary, quote):
    assert _new(summary, quote) == []


@pytest.mark.parametrize("summary,quote", [
    ("Counseled about 3 home exercises.", "Counseling provided on 3 home exercises."),
    ("Educated around 2 stretching routines.", "Education given on 2 stretching routines."),
    ("Discussed about 3 options.", "3 options reviewed."),
    ("Patient cannot bear weight.", "Unable to bear weight."), ("Patient can't bear weight.", "Unable to bear weight."),
    ("Unable to bear weight.", "Patient cannot bear weight."), ("Patient could not lift the arm.", "Cannot lift the arm."),
    ("Did not tolerate the exercise.", "Didn’t tolerate the exercise."), ("Didn't tolerate the exercise.", "Did not tolerate the exercise."),
    ("Pain not improved.", "Pain isn't improved.")])
def test_faithful_paraphrases_are_not_refused(summary, quote):
    assert GR.new_tokens(summary, quote) == [], (summary, quote, GR.new_tokens(summary, quote))


def test_a_real_approximation_still_refused_after_a_non_preposition_about():
    assert _new("Counseled about 3 exercises; pain about 4/10.", "Counseling provided on 3 exercises. Pain 4/10.")
    assert _new("Pain about 4/10.")
    assert _new("Pain around 4/10.")


def test_cannot_is_still_refused_when_the_quote_has_no_inability_or_hedge():
    assert _new("Patient cannot bear weight.")
    assert _new("Patient cannot bear weight.", "Weight bearing tolerated.")


@pytest.mark.parametrize("summary", ["Improving; absence of numbness.", "Improving; lacks radiation.", "Improving; free of numbness.", "Improving; nothing else.",
                                     "Improving; unremarkable otherwise.", "Improving; didn’t worsen.", "Improving; wasn’t worse."])
def test_negation_words_of_the_spanish_helper_and_curly_apostrophes_are_covered(summary):
    assert _new(summary), summary


def test_curly_apostrophe_contraction_in_the_quote_supports_the_summary():
    assert _new("Patient wasn't worse.", "Patient wasn’t worse.") == []
    assert GR.side_neg_words("didn’t") == GR.side_neg_words("didn't") and GR.side_neg_words("didn’t")


def test_lexicon_examples_behave_as_stated():
    import re
    fam = {e["id"] for e in lexicon.code_list("added_qualifier")}
    assert {"attribution", "attribution_bare_verb", "hedge", "hedge_carried", "approximation", "approximation_preposition_context", "inability", "inability_assertion",
            "side", "negation_word", "negation_extra", "negation_ruled_out", "negation_contraction", "negation_interchangeable"} <= fam
    for e in lexicon.load()["code_lists"]["added_qualifier"]["entries"]:
        rx = re.compile(e["pattern"], re.I)
        for ex in e["examples"]["hit"]:
            assert rx.search(ex), (e["id"], ex)
        for ex in e["examples"]["miss"]:
            assert not rx.search(ex), (e["id"], ex)


# ---- the structural single-source guard (T-105 r2): no word list of the lexicon's vocabulary may be a literal in the two checking modules ----
import ast
import pathlib
import re

# Top-level names that hold a word list on purpose, with the reason. Everything else in grounding.py and spanish_text.py must read the lexicon.
_ALLOWED = {
    "_SIDES": "Spanish -> English translation table: the keys are Spanish; the values are the side words the lexicon's `side` entry matches",
    "_HEDGE_CUES": "Spanish hedge cue words; probable/eventual/eventualmente overlap the English regexes only as cognates",
    "_SELF_CUES": "Spanish attribution cue words (refiere, manifiesta, niega ...); niega/informa overlap English only as cognates",
    "_EN_NOT_RULED_OUT": "phrase matcher for 'cannot be ruled out' semantics of 'No se descarta' (T-085), not a qualifier-kind list",
    "_EN_RULED_OUT": "phrase matcher for the opposite ('ruled out') reading, same Spanish rule",
    "_EN_SAYS_NOT_RULED_OUT": "phrase matcher for 'cannot be excluded' read as a negation, same Spanish rule",
}
_SINGLE_WORD_FAMILIES = ("hedge", "hedge_carried", "attribution_word", "approximation_word", "inability", "side", "negation_word", "negation_extra",
                         "negation_ruled_out", "negation_contraction")


def _is_lexicon_word(token: str) -> bool:
    """True when the lexicon (any single-word family) matches the whole token: the test of 'this is one of the lexicon's words', stems and plurals included."""
    return any(re.fullmatch(e["regex"].pattern, token, re.I) for e in lexicon.code_list("added_qualifier") if e["id"] in _SINGLE_WORD_FAMILIES)


def _vocabulary():
    return _is_lexicon_word


def duplicated_word_lists(source: str, is_word, allowed=()) -> list:
    """(name, line, words) for every literal in `source` that holds 3 or more distinct lexicon words as whole tokens: a regex string, a set, tuple, list
    or dict display, or a split() string. Docstrings are not literals. Top-level names in `allowed` are skipped."""
    tree = ast.parse(source)
    out = []
    for top in tree.body:
        if isinstance(top, ast.Expr) and isinstance(top.value, ast.Constant):
            continue                                        # the module docstring
        name = next((t.id for t in getattr(top, "targets", []) if isinstance(t, ast.Name)), getattr(top, "name", "?"))
        if name in allowed:
            continue
        doc = {id(n.body[0].value) for n in ast.walk(top) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.body
               and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant)}
        for node in ast.walk(top):
            if isinstance(node, (ast.Constant, ast.Set, ast.List, ast.Tuple, ast.Dict)):
                strs = [c.value for c in ast.walk(node) if isinstance(c, ast.Constant) and isinstance(c.value, str) and id(c) not in doc]
                tokens = set(re.findall(r"(?<![\w'])[a-z]+(?:'[a-z]+)?(?![\w'])", " ".join(strs).lower()))
                hits = {t for t in tokens if is_word(t)}
                if len(hits) >= 3:
                    out.append((name, node.lineno, sorted(hits)))
    return out


@pytest.mark.parametrize("module", [GR, ST], ids=["grounding", "spanish_text"])
def test_no_duplicated_word_list_remains_in_code(module):
    src = pathlib.Path(module.__file__).read_text(encoding="utf-8")
    assert duplicated_word_lists(src, _vocabulary(), _ALLOWED) == []


def test_the_guard_catches_a_word_list_added_back():
    vocab = _vocabulary()
    assert all(vocab(w) for w in ("seems", "apparently", "nearly", "absence", "possibly", "potentially", "circa", "cannot", "left"))
    assert duplicated_word_lists('X = re.compile(r"\\b(seems|possibly|apparently)\\b")', vocab)
    assert duplicated_word_lists('X = {"seems", "possibly", "apparently"}', vocab)
    assert duplicated_word_lists('X = frozenset("seems possibly apparently".split())', vocab)
    assert duplicated_word_lists('def f():\n    return w in ("no", "not", "none", "never")', vocab)
    assert duplicated_word_lists('X = {"seems": 1, "possibly": 2, "apparently": 3}', vocab)
    assert duplicated_word_lists('X = re.compile(r"\\b(seems|possibly|apparently)\\b")', vocab, allowed=("X",)) == []     # only a named top-level entry is skipped
    assert duplicated_word_lists('def f():\n    """seems possibly apparently"""\n    return 1', vocab) == []                  # a docstring is not a list
    assert duplicated_word_lists('X = "SUMMARY_TOKEN_NOT_IN_EXCERPT"', vocab) == []


def test_the_allowlist_is_only_the_documented_spanish_tables():
    assert set(_ALLOWED) == {"_SIDES", "_HEDGE_CUES", "_SELF_CUES", "_EN_NOT_RULED_OUT", "_EN_RULED_OUT", "_EN_SAYS_NOT_RULED_OUT"}
    assert all(len(why) > 30 for why in _ALLOWED.values())


def test_one_lexicon_edit_moves_both_directions():
    """A word added to the lexicon's hedge entry is refused when ADDED and reported when DROPPED, because both read the same regex."""
    word = "apparently"
    assert _new(f"Pain {word} 4/10, improving.")
    assert GR.dropped_qualifiers("Pain 4/10, improving.", f"Pain {word} 4/10, improving.") == ["hedge"]
    assert GR.dropped_qualifiers(f"Pain {word} 4/10, improving.", f"Pain {word} 4/10, improving.") == []


@pytest.mark.parametrize("quote,summary,kind", [
    ("Patient describes pain 4/10.", "Pain 4/10.", "self_report"), ("Pain apparently improving.", "Pain improving.", "hedge"),
    ("Pain potentially improving.", "Pain improving.", "hedge"), ("Pain seems to be improving.", "Pain improving.", "hedge"),
    ("Pain nearly 4/10.", "Pain 4/10.", "approx"), ("Pain circa 4/10.", "Pain 4/10.", "approx"), ("Pain close to 4/10.", "Pain 4/10.", "approx"),
    ("Pain reportedly 4/10.", "Pain 4/10.", "self_report"), ("Pain possibly 4/10.", "Pain 4/10.", "hedge"), ("Pain approx. 4/10.", "Pain 4/10.", "approx"),
    ("Pain according to the patient 4/10.", "Pain 4/10.", "self_report"), ("Patient indicates pain 4/10.", "Pain 4/10.", "self_report"),
    ("No numbness.", "Numbness.", "negation"), ("Didn’t tolerate the exercise.", "Tolerated the exercise.", "negation")])
def test_dropped_qualifiers_read_the_same_lexicon(quote, summary, kind):
    assert kind in GR.dropped_qualifiers(summary, quote), (quote, summary)


@pytest.mark.parametrize("quote,summary", [
    ("Patient describes pain 4/10.", "Patient describes pain 4/10."), ("Pain apparently improving.", "Pain apparently improving."),
    ("Pain nearly 4/10.", "Pain approximately 4/10."), ("Didn’t tolerate the exercise.", "Did not tolerate the exercise."),
    ("Counseled about 3 home exercises.", "Counseled on 3 home exercises."), ("Pain 4/10, cannot lift.", "Pain 4/10, unable to lift.")])
def test_a_faithful_summary_drops_nothing(quote, summary):
    assert GR.dropped_qualifiers(summary, quote) == [], (quote, summary)


def test_bare_verb_quote_supports_a_patient_indicates_summary():
    assert _new("Patient indicates pain 4/10.", "Indicates pain 4/10.") == []
    assert _new("Patient indicates pain 4/10.", "Pain 4/10.")


def test_spanish_absence_quote_supports_an_english_absence_summary():
    assert ST.new_tokens("Absence of numbness.", "Ausencia de entumecimiento.") == []
    assert ST.new_tokens("Free of numbness.", "Sin entumecimiento.") == []
    assert ST.new_tokens("Absence of numbness.", "Entumecimiento leve.")


def test_curly_apostrophe_summary_is_normalised_against_the_quote():
    assert _new("Patient can’t lift the arm.", "Patient cannot lift the arm.") == []
    assert _new("Patient can’t lift the arm.", "Lifts the arm.")
    assert GR.side_neg_words("Patient wasn’t worse") == {"wasn't"}


def test_spanish_path_reads_the_same_lists():
    q = "Dolor cervical 6/10, mejorando."
    for s in ("Patient describes neck pain 6/10.", "Neck pain apparently 6/10.", "Neck pain nearly 6/10.", "Neck pain potentially 6/10.", "Patient indicates neck pain 6/10."):
        assert ST.new_tokens(s, q), s
    assert ST.new_tokens("Patient describes neck pain 6/10.", "Refiere dolor cervical 6/10.") == []
    assert ST.new_tokens("Neck pain nearly 6/10.", "Dolor cervical aproximadamente 6/10.") == []
    assert ST.new_tokens("Neck pain apparently 6/10.", "Dolor cervical posible 6/10.") == []


def test_faithful_spanish_paraphrases_are_not_refused():
    assert ST.new_tokens("Counseled about 3 home exercises.", "Se ensenaron 3 ejercicios en casa.") == []


def test_carried_only_hedge_words_count_as_carrying_a_hedge():
    assert GR.dropped_qualifiers("Fracture cannot be excluded.", "Possible fracture.") == []
    assert GR.dropped_qualifiers("Findings suggested a fracture.", "Possible fracture.") == []
    assert GR.dropped_qualifiers("Fracture cannot be determined.", "Possible fracture.") == []
    assert GR.dropped_qualifiers("Fracture.", "Possible fracture.") == ["hedge"]
    assert _new("Fracture cannot be excluded.", "Fracture.")                  # but neither word may be ADDED where the quote has no hedge


def test_no_not_none_never_are_one_negation_when_dropped():
    assert GR.dropped_qualifiers("There was none.", "No numbness.") == []
    assert GR.dropped_qualifiers("Never numb.", "Not numb.") == []
    assert GR.dropped_qualifiers("Without numbness.", "No numbness.") == ["negation"]


def test_spanish_dropped_negation_reads_english_words_of_a_mixed_quote():
    assert "negation" in ST.dropped_qualifiers("Mild pain.", "Unremarkable, dolor leve.")
    assert ST.dropped_qualifiers("Unremarkable; mild pain.", "Unremarkable, dolor leve.") == []
    assert "negation" in ST.dropped_qualifiers("Mild pain.", "Absence of dolor.")
    assert ST.dropped_qualifiers("Fracture possible.", "No se descarta fractura.") == []            # the Spanish 'no' is the cue list's word, not an English negation
