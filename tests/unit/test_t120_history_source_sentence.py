"""T-120 (T-060 pass-2 F13): a history-SOURCE sentence ('Hx obtained via patient's son, who interpreted') names who gave the history,
not a prior condition, so the phrase list does not raise 'Mention of a prior or pre-existing condition' on it. A real prior-condition
mention still raises the flag, in the same record and in others. Deterministic code guard in lexicon_scan (the lexicon is researcher-owned)."""
import pathlib

import pytest

from app.backend import flags as FL, ingest as I, lexicon_scan as LS

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ["Hx obtained via patient's son, who interpreted.", "Hx obtained from patient's daughter.", "Hx taken per interpreter.",
          "History obtained via interpreter.", "History provided by patient's husband.", "hx was obtained through a telephone interpreter.",
          "H/o obtained via family member.", "Hx per patient's son, who interpreted.", "Hx via interpreter."]
REAL = ["Hx obtained via interpreter: lumbar strain 2019.", "PHx obtained via patient's son: lumbar strain 2019.", "Hx obtained via interpreter; lumbar strain 2019.",
        "Hx per patient: lumbar strain 2019.", "Hx per patient of lumbar strain", "History per patient: left knee surgery in 2017.",
        "Hx per patient lumbar strain", "Hx via interpreter: prior neck injury 2018.", "Hx obtained from patient: lumbar strain 2019.", "Hx obtained via patient's son of lumbar strain",
        "Hx per patient's son: prior neck injury.", "Hx of lumbar strain.", "Hx: lumbar strain 2019.", "History of migraines.", "Hx neck pain.", "h/o lumbar strain",
        "Prior history of neck pain 2019, resolved."]


def _prior(text):
    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]


@pytest.mark.parametrize("s", SOURCE)
def test_history_source_sentence_raises_no_prior_condition_hit(s):
    assert _prior(s) == []
    assert _prior(s + " Patient states she was struck by a car. Left shoulder pain 7/10.") == []


@pytest.mark.parametrize("s", REAL)
def test_real_prior_condition_mentions_still_hit(s):
    assert _prior(s)


def test_source_sentence_does_not_hide_a_real_prior_condition_next_to_it():
    t = "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. Left shoulder pain 7/10."
    hits = _prior(t)
    assert len(hits) >= 1 and all("lumbar strain" in t[h["unit_start"]:h["unit_end"]] for h in hits)
    t2 = "Hx obtained via patient's son. Prior neck injury in 2018."
    assert _prior(t2)


def test_lib09_record_1_raises_no_prior_condition_flag_and_other_prior_mentions_still_do():
    recs = I.ingest((ROOT / "evals/library/case_lib09_spanish_interpreter_espalda.txt").read_text(encoding="utf-8"))["records"]
    interp = next(r for r in recs if "Hx obtained via" in r["excerpt"])
    assert interp["n"] == 1                                    # the interpreter sentence is in record 1 of lib09 (r1), not record 2
    assert [f for f in FL.lexicon_flags(interp) if f["type"] == "pre_existing"] == []
    real = dict(interp, excerpt="Hx obtained via patient's son, who interpreted. Prior history of left shoulder dislocation 2019. Pain 7/10.")
    pre = [f for f in FL.lexicon_flags(real) if f["type"] == "pre_existing"]
    assert pre and all("Hx obtained via" not in f["excerpt"] for f in pre)


# --- r3: the sentence is judged by what is LEFT after the attribution phrase is stripped, never by a guess about "naming a condition" ---
# Staff r2 probe (32 phrasings). Two staff rows have no lexicon entry at all for the bare word "History" (the parent build did not flag them either), so they are
# not in this list: 'History provided by wife, notable for lumbar strain.' and 'History obtained from patient - lumbar strain.'.
STAFF_NONE = ["Hx per patient's son.", "PHx obtained via patient's son, who interpreted.", "History provided by patient's wife.", "Hx obtained via telephone interpreter.",
              "Hx per EMS.", "Hx per interpreter line.", "History given by the patient's mother.", "Hx relayed through language line interpreter.",
              "PHx gathered from patient's friend.", "History was obtained from patient's caregiver.", "Hx per patient.", "History obtained from chart review.",
              "Hx per medical records.", "Hx obtained from Dr. Lee."]
STAFF_FLAG = ["Hx obtained via interpreter: lumbar strain 2019.", "PHx obtained via patient's son: lumbar strain 2019.", "Hx per patient's son, significant for diabetes.",
              "Hx obtained via interpreter, positive for prior neck injury.", "Hx per patient's son; patient fractured her wrist before.",
              "PHx obtained via interpreter (lumbar strain).", "Hx obtained via interpreter and reports degenerative disc disease.",
              "Hx per patient's son, history of lumbar strain.", "Hx obtained via patient's son who interpreted. Hx of lumbar strain 2019.",
              "Hx obtained via interpreter\nLumbar strain 2019", "Hx per EMS - pt had previous knee surgery", "Hx obtained via interpreter, pre-existing arthritis",
              "Hx per patient's son, who interpreted, a recurring back problem", "PHx obtained via son; previous whiplash", "Hx obtained from Dr. Lee: lumbar strain"]
# Paralegal r2: a condition named with no colon, digit or 'of' after the source phrase (S4, S6, S11, S15) and the r1 forms.
PARALEGAL_FLAG = ["Hx obtained via patient's son, who reports neck pain.", "Hx obtained via patient's son, who reports chronic neck pain.",
                  "Hx obtained via patient's son; neck pain and headaches.", "Hx obtained via EMS crew, who relayed lumbar strain.",
                  "Hx obtained via patient's son, who interpreted, and reports lumbar strain.", "Hx obtained via patient's son, who interpreted, lumbar strain 2019.",
                  "Hx via interpreter, who interpreted; prior neck injury.", "Hx of lumbar strain obtained via patient's son.",
                  "Hx obtained via patient's son, who interpreted. Prior lumbar strain 2019.", "Hx obtained via patient's son, who interpreted, significant for diabetes.",
                  "Hx obtained via patient's son, who interpreted, fractured her wrist."]
PARALEGAL_NONE = ["Hx obtained via patient's son, who interpreted.", "Hx per patient's son, who interpreted.",
                  "Hx obtained via patient's son, who interpreted. Lumbar strain was noted.", "Hx obtained via patient\u2019s son, who interpreted."]
# Parent-build (pre-T-120) flags that r2 lost and r3 must keep: Hx hit itself, five staff forms plus the bare-newline form.
PARENT_REGRESSION = ["Hx per patient's son, significant for diabetes.", "PHx obtained via interpreter (lumbar strain).", "Hx obtained via interpreter\nLumbar strain 2019",
                     "Hx per patient's son, who interpreted, a recurring back problem", "Hx obtained from Dr. Lee: lumbar strain", "Hx obtained via interpreter: lumbar strain."]
# Source and extra shapes that are only attribution.
MORE_NONE = ["Hx obtained from the patient and daughter.", "Hx obtained via patient's son, who interpreted for the patient.", "Hx obtained via a family member, who translated.",
             "Hx obtained via patient's son and telephone interpreter.", "Hx obtained via interpreter\n", "Hx obtained via interpreter,"]


def _hx(t):
    return [h["text"] for h in _prior(t)]


@pytest.mark.parametrize("s", STAFF_NONE + PARALEGAL_NONE + MORE_NONE)
def test_r3_attribution_only_sentence_yields_no_hit(s):
    assert _hx(s) == []


@pytest.mark.parametrize("s", STAFF_FLAG + PARALEGAL_FLAG + PARENT_REGRESSION)
def test_r3_text_left_after_the_attribution_keeps_a_pre_existing_hit(s):
    assert _hx(s)


@pytest.mark.parametrize("s", PARENT_REGRESSION)
def test_r3_the_hit_is_the_history_word_itself(s):
    """Pins which rule fired: the Hx hit (not a separate lexicon phrase like 'prior ... injury') survives for the colon-only, newline and parenthesis forms."""
    assert [h for h in _hx(s) if h.lower() in ("hx", "phx")], s


def test_r3_newline_does_not_end_the_sentence():
    assert _hx("Hx obtained via interpreter\nLumbar strain") == ["Hx"]
    assert _hx("Hx obtained via interpreter.\nLumbar strain") == []          # a period does


def test_r3_colon_after_the_source_keeps_the_hit():
    assert _hx("Hx obtained via interpreter: lumbar strain.") == ["Hx"]
    assert _hx("Hx per patient: lumbar strain") == ["Hx"]


def test_r3_two_sentences_judged_separately():
    t = "Hx obtained via patient's son, who interpreted. Hx per patient: lumbar strain."
    hits = _prior(t)
    assert len(hits) == 1 and t[hits[0]["start"]:hits[0]["end"]] == "Hx" and hits[0]["start"] > t.index(". ")


def test_r3_unknown_source_noun_keeps_the_flag():
    """Not in the closed list of people and channels: nothing is stripped, so the hit stays (safe direction: the paralegal dismisses it)."""
    assert _hx("Hx obtained via the plumber.")


def test_r3_no_condition_guessing_left_in_the_guard():
    src = (ROOT / "app/backend/lexicon_scan.py").read_text(encoding="utf-8")
    body = src[src.index("def _is_source_sentence"):src.index("def _hit_year")]
    assert "\\d" not in body and "\\bof\\b" not in body and '":"' not in body    # the r2 proxy (colon / digit / 'of') is gone
