"""T-132 (T-120 r3 paralegal blocker + staff minors 1 and 2): when the unit a history word flags is ATTRIBUTION ONLY ('Hx obtained via patient's son;'),
the flag's quote extends to the next clause of the same sentence so the condition is shown; 'Hx per MS history' keeps its flag (MS is not Ms.);
the history-word gate in scan() is pinned. Deterministic code, no model."""
import pytest

from app.backend import flags as FL, lexicon_scan as LS


def _prior(text):
    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]


def _quotes(text):
    return sorted({text[h["unit_start"]:h["unit_end"]] for h in _prior(text)})


# 1. the quote carries the condition ------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text,quote", [
    ("Hx obtained via patient's son; neck pain and headaches.", "Hx obtained via patient's son; neck pain and headaches."),         # S6, the r3 blocker
    ("Hx via interpreter, who interpreted; prior neck injury.", "Hx via interpreter, who interpreted; prior neck injury."),          # S8
    ("Hx obtained from patient's husband; prior cervical strain.", "Hx obtained from patient's husband; prior cervical strain."),   # N2
    ("Pain 7/10. Hx per EMS; lumbar strain 2019. Left wrist swollen.", "Hx per EMS; lumbar strain 2019."),                            # only the same sentence
    ("Hx per interpreter; neck pain; headaches.", "Hx per interpreter; neck pain;"),                                                  # ONE following clause
    ("Hx per interpreter\nLumbar strain 2019", "Hx per interpreter\nLumbar strain 2019"),                                           # a newline does not end the sentence here
])
def test_an_attribution_only_unit_extends_to_the_following_clause(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


def test_the_extended_quote_is_one_flag_that_shows_the_condition_and_keeps_both_lexicon_ids():
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": "Hx obtained from patient's husband; prior cervical strain."}
    pre = [f for f in FL.lexicon_flags(r) if f["type"] == "pre_existing"]
    assert len(pre) == 1 and "prior cervical strain" in pre[0]["excerpt"] and pre[0]["excerpt"].startswith("Hx obtained from")
    assert len(pre[0]["lexicon_ids"]) >= 2                                      # the history word and the condition phrase are one flag (no duplicate fragment)


@pytest.mark.parametrize("text", [
    "Hx obtained via patient's son, who reports neck pain; denies fever.",   # the unit already names the condition: unchanged
    "Hx of lumbar strain; denies fever.",
    "Hx: lumbar strain 2019; other.",
])
def test_a_unit_that_names_the_condition_is_not_extended(text):
    (q,) = _quotes(text)
    assert q == text[:text.index(";") + 1]


def test_nothing_to_extend_to_at_the_end_of_the_text_or_the_sentence():
    assert _prior("Hx obtained via patient's son; ") == []                      # attribution and nothing after it: no condition, no flag
    assert _quotes("Hx obtained via patient's son; neck pain. Left wrist swollen.") == ["Hx obtained via patient's son; neck pain."]


@pytest.mark.parametrize("text", ["Hx obtained via patient's son, who interpreted.", "Hx via interpreter."])
def test_attribution_only_sentences_still_raise_nothing(text):
    assert _prior(text) == []


# 2. MS is not Ms. ---------------------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text", ["Hx per MS history.", "Hx per patient, MS diagnosis.", "Hx via MS clinic note.", "PHx obtained from MS society records."])
def test_ms_the_diagnosis_is_not_a_person_title(text):
    assert any(h["text"].lower() in ("hx", "phx") for h in _prior(text)), text


@pytest.mark.parametrize("text", ["Hx obtained from Dr. Lee.", "Hx per Ms. Alvarez, the patient's wife.", "Hx per Dr Lee.", "Hx obtained via Mrs. Jones.", "Hx per Mr Smith, who interpreted."])
def test_a_titled_person_is_still_a_source(text):
    assert _prior(text) == [], text


# 3. the history-word gate (T-120 r3 staff minor 2, mutant F) --------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text", ["Degenerative per patient's son.", "Chronic per EMS.", "Pre-existing per interpreter.", "Previous knee surgery per patient."])
def test_a_condition_word_before_an_attribution_phrase_is_not_skipped_as_a_history_source(text):
    assert _prior(text), text


def test_only_hits_of_the_same_flag_type_join_the_extended_quote():
    t = "Hx per EMS; patient states symptoms began after the collision."
    hits = LS.scan(t)
    kinds = {h["flag_type"] for h in hits}
    assert "pre_existing" in kinds
    other = [h for h in hits if h["flag_type"] != "pre_existing"]
    assert other and all(t[h["unit_start"]:h["unit_end"]] == "patient states symptoms began after the collision." for h in other), other


# ---- round 2 (reviews/T-132-staff-engineer.md) -----------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("text,quote", [      # a soft line wrap inside the attribution phrase is part of the unit (finding 1)
    ("Hx obtained\nvia patient's son; neck pain and headaches.", "Hx obtained\nvia patient's son; neck pain and headaches."),
    ("Hx obtained via\npatient's son; neck pain and headaches.", "Hx obtained via\npatient's son; neck pain and headaches."),
    ("Hx obtained via patient's\nson; neck pain and headaches.", "Hx obtained via patient's\nson; neck pain and headaches."),
    ("Hx\nper EMS; neck pain.", "Hx\nper EMS; neck pain."),
    ("Hx obtained\nvia patient's son, who reports neck pain.", "Hx obtained\nvia patient's son, who reports neck pain."),   # the condition is already in the unit: still never 'Hx obtained'
])
def test_a_wrapped_attribution_phrase_is_never_a_fragment_quote(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


def test_a_wrapped_attribution_with_nothing_after_it_still_raises_nothing():
    assert _prior("Hx obtained\nvia patient's son.") == []


@pytest.mark.parametrize("text,quote", [      # chained attribution clauses: ONE flag, the condition in it (finding 2)
    ("Hx per EMS; Hx per son; neck pain.", "Hx per EMS; Hx per son; neck pain."),
    ("Hx per EMS; who interpreted; prior neck injury.", "Hx per EMS; who interpreted; prior neck injury."),
    ("Hx per EMS; Hx per son; who interpreted; prior neck injury.", "Hx per EMS; Hx per son; who interpreted; prior neck injury."),
])
def test_chained_attribution_clauses_give_one_flag_with_the_condition(text, quote):
    assert _quotes(text) == [quote], _quotes(text)
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": text}
    pre = [f for f in FL.lexicon_flags(r) if f["type"] == "pre_existing"]
    spans = sorted(f["_span"] for f in pre)
    assert all(a2 >= b1 for (a1, b1), (a2, b2) in zip(spans, spans[1:])), spans           # no two pre_existing flags overlap


@pytest.mark.parametrize("text,quote", [      # the extension never crosses a blank line or a section header (finding 3)
    ("Hx per EMS\n\nPLAN: follow up in 2 weeks.", "Hx per EMS"),
    ("Hx per interpreter\nMEDICATIONS: ibuprofen 400 mg", "Hx per interpreter"),
    ("Hx per EMS;\n\nneck pain.", "Hx per EMS;"),
    ("Hx per EMS; PLAN: follow up.", "Hx per EMS;"),
    ("Hx per EMS\nCHIEF COMPLAINT: neck pain", "Hx per EMS"),
    ("Hx per EMS;\n\n  \nneck pain", "Hx per EMS;"),
])
def test_the_extension_stops_at_a_blank_line_or_a_section_header(text, quote):
    got = _quotes(text)
    assert got == [quote] and all("PLAN" not in q and "MEDICATIONS" not in q and "\n\n" not in q for q in got), got


def test_a_wrap_that_would_swallow_a_blank_line_is_not_bridged():
    assert all("\n\n" not in q for q in _quotes("Hx obtained\n\nvia patient's son; neck pain."))


# ---- mutants M8, M9, M10 of the round-1 review --------------------------------------------------------------------------------------------------------------------
def test_m8_a_condition_word_is_never_extended_only_the_history_word_is():
    assert _quotes("Chronic per EMS; headaches.") == ["Chronic per EMS;"]


def test_m9_the_next_clause_may_start_right_after_the_semicolon():
    assert _quotes("Hx per EMS;neck pain.") == ["Hx per EMS;neck pain."]


def test_the_extension_never_runs_into_the_next_sentence():
    assert _quotes("Hx per EMS; Hx per son. Prior neck injury.") == ["Hx per EMS; Hx per son.", "Prior neck injury."]


# ---- round 3 (reviews/T-132-staff-engineer-r2.md): soft wraps are spaces, chains have no cap, 'for the patient', short labels --------------------------------------
def _flags_no_overlap(text):
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": text}
    spans = sorted(f["_span"] for f in FL.lexicon_flags(r) if f["type"] == "pre_existing")
    assert all(a2 >= b1 for (a1, b1), (a2, b2) in zip(spans, spans[1:])), spans
    for a, b in spans:
        assert text[a:b] in text                                                                       # contiguous slice of the original
    return spans


@pytest.mark.parametrize("text", [                    # C1-C4, B31: a wrap inside a CHAINED clause (finding 1)
    "Hx per EMS; Hx obtained\nvia son; neck pain.",                   # C1
    "Hx per EMS; Hx per\nson; neck pain.",                            # C2
    "Hx per EMS; who\ninterpreted; neck pain.",                       # C3: the condition used to be in no flag
    "Hx per EMS; who\ninterpreted\nfor the\npatient; neck pain.",     # C4: several wraps
    "Hx per EMS; who\ninterpreted; prior neck injury.",               # B31
    "Hx per EMS;\nwho interpreted;\nHx\nper son;\nneck pain.",
])
def test_a_wrap_inside_a_chained_attribution_clause_gives_one_flag_with_the_condition(text):
    assert _quotes(text) == [text], _quotes(text)
    assert len(_flags_no_overlap(text)) == 1


def test_the_quote_is_cut_from_the_original_text_never_from_the_normalised_copy():
    t = "Hx per EMS; Hx\nper son; neck pain."
    h = _prior(t)[0]
    assert "\n" in t[h["unit_start"]:h["unit_end"]]                                                  # the wrap is still there in the quote
    assert LS._soft_wraps(t) != t and len(LS._soft_wraps(t)) == len(t)


@pytest.mark.parametrize("text,quote", [              # no cap on the chain, and 'who interpreted for the patient' is attribution (finding 2)
    ("Hx per EMS; Hx per son; Hx per wife; Hx per aunt; Hx per uncle; neck pain.", "Hx per EMS; Hx per son; Hx per wife; Hx per aunt; Hx per uncle; neck pain."),
    ("Hx per EMS; Hx per son; Hx per wife; Hx per husband; Hx per nurse; Hx per staff; Hx per chart; neck pain.",
     "Hx per EMS; Hx per son; Hx per wife; Hx per husband; Hx per nurse; Hx per staff; Hx per chart; neck pain."),
    ("Hx per EMS; who interpreted for the patient; cervical strain; headaches.", "Hx per EMS; who interpreted for the patient; cervical strain;"),
    ("Hx per EMS; who interpreted for her; Hx per son; cervical strain.", "Hx per EMS; who interpreted for her; Hx per son; cervical strain."),
])
def test_chains_have_no_cap_and_who_interpreted_for_the_patient_is_attribution(text, quote):
    assert _quotes(text) == [quote], _quotes(text)
    assert len(_flags_no_overlap(text)) == 1


@pytest.mark.parametrize("text,quote", [              # a short vitals / exam label ends the extension (finding 3)
    ("Hx per EMS;\nBP: 120/80", "Hx per EMS;"),
    ("Hx per EMS; BP: 120/80.", "Hx per EMS;"),
    ("Hx per EMS;\nHR: 88, BP: 120/80", "Hx per EMS;"),
    ("Hx per EMS;\nRR: 16, HR: 88", "Hx per EMS;"),
    ("Hx per EMS;\nPE: normal.", "Hx per EMS;"),
    ("Hx per EMS;\nTYLENOL #3: prn", "Hx per EMS;"),
    ("Hx per EMS; Hx per son;\nBP: 120/80", "Hx per EMS; Hx per son;"),
    ("Hx per EMS;\nA: neck pain.", "Hx per EMS;"),                                   # r4: a label at a line start (SOAP letters too) ends it; see test_item2_*
    ("Hx per EMS;\nPlan: follow up in 2 weeks.", "Hx per EMS;"),                    # r5: 'Plan' is on the closed section-label list
    ("Hx per EMS; Neck pain: onset 2019.", "Hx per EMS; Neck pain: onset 2019."),
])
def test_a_short_vitals_or_exam_label_ends_the_extension(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


# ---- the surviving mutants C6, C7, S6 (and S3 above) ---------------------------------------------------------------------------------------------------------
def test_c6_a_chained_history_clause_that_names_a_condition_ends_the_walk():
    assert _quotes("Hx per EMS; Hx per son: lumbar strain 2019; headaches.") == ["Hx per EMS; Hx per son: lumbar strain 2019;"]


def test_c7_a_who_clause_that_names_something_ends_the_walk():
    assert _quotes("Hx per EMS; who interpreted for the patient; cervical strain; headaches.") == ["Hx per EMS; who interpreted for the patient; cervical strain;"]
    assert _quotes("Hx per EMS; who interpreted and reports neck pain; headaches.") == ["Hx per EMS; who interpreted and reports neck pain;"]


@pytest.mark.parametrize("text", ["Hx per EMS;\n \nneck pain.", "Hx per EMS;\n\t\nneck pain.", "Hx per EMS;\r\n\r\nneck pain.", "Hx per EMS;\r\n \r\nneck pain."])
def test_s6_a_blank_line_with_spaces_or_crlf_ends_the_extension(text):
    assert _quotes(text) == ["Hx per EMS;"]


def test_a_newline_after_a_sentence_end_is_not_a_soft_wrap():
    assert _quotes("Hx per EMS; Hx per son.\nneck pain.") == ["Hx per EMS; Hx per son."]
    assert _quotes("Hx per EMS; Hx per son.\n\nneck pain.") == ["Hx per EMS; Hx per son."]


def test_soft_wraps_keep_hard_breaks_and_offsets():
    t = "a\nb\n\nc\n d\nPLAN: e\nBP: 1\nf. \ng"
    assert LS._soft_wraps(t) == "a b\n\nc  d\nPLAN: e\nBP: 1 f. \ng"       # soft: a-b, c-d, 1-f; hard: blank line, before PLAN:, before BP:, after 'f.'


@pytest.mark.parametrize("text", ["Hx obtained\n \nvia patient's son; neck pain.", "Hx obtained\r\n\r\nvia patient's son; neck pain.", "Hx obtained\n\t\nvia patient's son; neck pain."])
def test_a_phrase_is_not_bridged_over_a_blank_line_with_spaces_or_crlf(text):
    assert all("\n \n" not in q and "\r\n\r\n" not in q and "\n\t\n" not in q for q in _quotes(text)), _quotes(text)


def test_a_newline_after_a_sentence_end_and_a_closing_quote_or_bracket_is_hard():
    assert _quotes('Hx per EMS; Hx per son."\nneck pain.') == ['Hx per EMS; Hx per son."']
    assert _quotes("Hx per EMS; (Hx per son.)\nneck pain.") == ["Hx per EMS; (Hx per son.)"]


# ---- round 4 fix-up (reviews/T-132-staff-engineer-r3.md; orchestrator note of 2026-11-02T12:54:30Z, §7.4) ------------------------------------------------------
def _one_flag_with(text, *condition):
    spans = _flags_no_overlap(text)
    assert len(spans) == 1, spans
    q = text[spans[0][0]:spans[0][1]]
    assert all(c in q for c in condition), q
    return q


@pytest.mark.parametrize("text,condition", [         # item 1: two attribution lines in a row, the first without ';' (V1, V3-V7, V9, V10) -> ONE flag that shows the condition
    ("Hx per EMS\nHx via son; neck pain.", "neck pain"),                                                                                                  # V1
    ("Hx obtained via patient's son\nHx obtained via EMS; prior neck injury.", "prior neck injury"),                                                      # V3
    ("Hx per EMS\nHx per son\nHx per wife; prior neck injury.", "prior neck injury"),                                                                      # V4
    ("Hx per EMS\nHx per son; Hx per wife; prior neck injury.", "prior neck injury"),                                                                      # V5
    ("Hx per EMS\n  Hx per son, who interpreted for the patient; prior neck injury.", "prior neck injury"),                                                # V6
    ("Hx per EMS; Hx per son\nHx per wife; prior neck injury.", "prior neck injury"),                                                                      # V7
    ("Pain 7/10. Hx per EMS\nHx obtained from patient's husband; prior cervical strain. Left wrist swollen.", "prior cervical strain"),                    # V9
    ("Hx per EMS\nwho interpreted for the patient\nHx per son; prior neck injury.", "prior neck injury"),                                                  # V10
])
def test_item1_overlapping_attribution_lines_are_one_flag_whose_quote_contains_the_condition(text, condition):
    q = _one_flag_with(text, condition)
    assert q.startswith("Hx") and q in text


def test_item1_pins_which_hit_gets_the_merged_unit_both_lexicon_ids_stay_on_the_one_flag():
    t = "Hx per EMS\nHx via son; neck pain."
    r = {"n": 1, "id": "r1", "source": "Clinic", "date_iso": "2026-01-09", "excerpt": t}
    (f,) = [f for f in FL.lexicon_flags(r) if f["type"] == "pre_existing"]
    assert f["excerpt"] == t and len(f["lexicon_ids"]) >= 2
    hs = _prior(t)
    assert len({(h["unit_start"], h["unit_end"]) for h in hs}) == 1


def test_item1_fuzz_two_to_four_attribution_lines_then_a_condition_is_one_flag():
    import random
    rnd = random.Random(132)
    hx = ["Hx per EMS", "Hx obtained via patient's son", "Hx obtained from the patient's wife", "Hx per aunt", "Hx per Dr. Smith"]
    who = "who interpreted for the patient"                      # one who-clause per clause: two in a row is a clause with content (the phrase allows one)
    sep = ["\n", "; ", ";\n", ", ", "\n  "]
    for _ in range(300):
        parts, seps = [rnd.choice(hx)], []
        for _ in range(rnd.randint(1, 3)):
            s_ = rnd.choice(sep)
            seps.append(s_)
            parts.append(who if s_ != ", " and parts[-1] != who and rnd.random() < 0.3 else rnd.choice(hx))
        text = "".join(p + s_ for p, s_ in zip(parts, seps)) + parts[-1] + rnd.choice(["; neck pain.", "\nprior cervical strain.", "; lumbar strain 2019."])
        _one_flag_with(text, text.split()[-1].rstrip("."))


def test_item1_non_overlapping_flags_of_the_same_type_stay_separate():
    t = "Hx per EMS; neck pain.\n\nPrior knee surgery per patient."
    spans = _flags_no_overlap(t)
    assert len(spans) == 2


# item 2: any 'Label:' line and the start of a bullet list end the extension -----------------------------------------------------------------------------------------
@pytest.mark.parametrize("text,quote", [
    ("Hx per EMS;\nPlan: follow up in 2 weeks.", "Hx per EMS;"),
    ("Hx obtained via patient's son;\nPlan: MRI cervical spine, ibuprofen 600 mg TID, PT referral.", "Hx obtained via patient's son;"),
    ("Hx per EMS\nMedications: ibuprofen 400 mg", "Hx per EMS"),
    ("Hx per EMS\nDx: sprain.", "Hx per EMS"),
    ("Hx per EMS;\nA: neck pain.", "Hx per EMS;"),                                  # SOAP letters are labels at a line start
    ("Hx per EMS; Hx per son;\nAssessment: cervical strain", "Hx per EMS; Hx per son;"),
])
def test_item2_a_label_line_ends_the_extension_closed_list_or_capitals(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


@pytest.mark.parametrize("text,quotes", [             # the labels and the text after them are never inside the quote of the history flag
    ("Hx per EMS\nRx: cyclobenzaprine 10 mg\nPrior neck injury.", ["Hx per EMS", "Prior neck injury."]),
    ("Hx per EMS\nAllergies: NKDA\nMeds: none\nprior neck injury", ["Hx per EMS", "prior neck injury"]),
])
def test_item2_text_after_a_label_line_is_not_in_the_history_quote(text, quotes):
    assert _quotes(text) == quotes, _quotes(text)


@pytest.mark.parametrize("text,quote", [
    ("Hx per EMS\n- ibuprofen 600 mg\n- PT referral\n- follow up 2 weeks.", "Hx per EMS"),
    ("Hx per EMS;\n* ibuprofen 600 mg", "Hx per EMS;"),
    ("Hx per EMS\n• ibuprofen 600 mg", "Hx per EMS"),
    ("Hx per EMS\n1. ibuprofen 600 mg", "Hx per EMS"),
    ("Hx per EMS\n2) PT referral", "Hx per EMS"),
])
def test_item2_the_start_of_a_bullet_list_ends_the_extension(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


@pytest.mark.parametrize("text", [                    # not a label and not a bullet: the extension continues
    "Hx per EMS; Neck pain: onset 2019.",             # a label inside a line is a condition's word
    "Hx per EMS\nSeen at 10:30 for neck pain.",       # a time is not a label
    "Hx per EMS\nneck pain: onset 2019.",             # lower-case start is a wrapped clause
    "Hx per EMS\n-5 mm lumbar curve loss.",           # a minus sign is not a bullet
    "Hx per EMS\n2019 lumbar strain.",                # a year is not a numbered item
    "Hx obtained via patient's son;\nLeft wrist swollen: since Monday.",   # r5: a clinical phrase ending in a colon is the condition, never a label
    "Hx per EMS;\nNeck pain: onset 2019.",
    "Hx per EMS;\nDischarge instructions: rest, ice.",   # not on the closed list
    "Hx per EMS\nPlanning: knee surgery 2019.",       # 'Plan' only as a whole word
    "Hx per EMS\nTemperature sensitivity: since 2018.",
])
def test_item2_ordinary_continuation_lines_still_extend(text):
    assert _quotes(text) == [text], _quotes(text)


def test_item2_soft_wraps_keeps_labels_and_bullets_hard():
    assert LS._soft_wraps("a\nPlan: b\nc\n- d\ne\n1. f\ng\nSeen 10:30") == "a\nPlan: b c\n- d e\n1. f g Seen 10:30"
    assert LS._soft_wraps("a\nLeft wrist swollen: b\nNeck pain: c") == "a Left wrist swollen: b Neck pain: c"      # r5: not a closed-list label


@pytest.mark.parametrize("label", ["S", "O", "A", "P", "Subjective", "Objective", "Assessment", "Plan", "Impression", "Diagnosis", "Dx", "Rx", "Meds", "Medications", "Allergies",
                                   "BP", "HR", "RR", "Temp", "SpO2", "Pulse", "Weight", "PLAN", "plan", "Medications"])
def test_r5_every_closed_list_label_followed_by_a_colon_ends_the_extension(label):
    text = f"Hx per EMS;\n{label}: neck pain 2019."
    assert _quotes(text) == ["Hx per EMS;"], _quotes(text)


# item 3: the chain walk is linear ---------------------------------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("unit", ["Hx per EMS; ", "Hx per EMS\n"])
def test_item3_a_24k_character_chain_scans_in_linear_time(unit):
    text = unit * 2000 + "neck pain."
    assert len(text) >= 22000
    hits = [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]
    assert {(h["unit_start"], h["unit_end"]) for h in hits} == {(0, len(text))}, sorted({(h["unit_start"], h["unit_end"]) for h in hits})[:3]
    # no wall-clock bound (r5): the call-count test below is the exact linearity check


def test_item3_each_clause_is_classified_a_bounded_number_of_times(monkeypatch):
    calls = []
    real = LS._attribution_only
    monkeypatch.setattr(LS, "_attribution_only", lambda norm, unit: calls.append(1) or real(norm, unit))
    n = 600
    LS.scan("Hx per EMS; " * n + "neck pain.")
    assert len(calls) <= 3 * n, len(calls)                      # quadratic would be ~n*n/2


def test_item3_a_long_chain_still_gives_the_same_flag_as_a_short_one():
    for n in (3, 40, 400):
        t = "Hx per EMS; " * n + "neck pain."
        assert _one_flag_with(t, "neck pain") == t


# item 4: every family noun as it is written in the code ------------------------------------------------------------------------------------------------------------
_FAMILY_NOUNS = ["son", "daughter", "husband", "wife", "spouse", "mother", "father", "brother", "sister", "sibling", "aunt", "uncle", "cousin", "grandmother", "grandfather",
                 "niece", "nephew", "family", "friend", "caregiver", "relative", "guardian", "parent", "neighbor"]


def test_item4_the_noun_list_below_is_the_one_in_the_code():
    written = LS._PERSON.split("|")
    assert written[:len(_FAMILY_NOUNS)] == _FAMILY_NOUNS, written[:len(_FAMILY_NOUNS) + 2]


@pytest.mark.parametrize("noun", _FAMILY_NOUNS)
def test_item4_a_family_source_alone_raises_nothing_and_with_a_condition_the_quote_carries_it(noun):
    assert _prior(f"Hx obtained from patient's {noun}.") == [], noun
    assert _prior(f"Hx per {noun}.") == [], noun
    assert _quotes(f"Hx obtained from the {noun}; prior neck injury.") == [f"Hx obtained from the {noun}; prior neck injury."], noun


# item 5: a wrap right after Dr. / Mr. / Mrs. / Ms. / an initial is not a sentence end ---------------------------------------------------------------------------------
@pytest.mark.parametrize("text", [
    "Hx obtained via Dr.\nSmith; prior neck injury.",
    "Hx per EMS; Hx obtained via Dr.\nSmith; prior neck injury.",
    "Hx per EMS; Hx obtained via Mrs.\nJones; prior neck injury.",
    "Hx per EMS; Hx per Dr.\nSmith, who interpreted; prior neck injury.",
    "Hx per EMS; Hx per Ms.\nLee; prior neck injury.",
    "Hx per EMS; Hx per Mr.\nBrown; prior neck injury.",
    "Hx per Dr.\nSmith; Hx per EMS; prior neck injury.",
])
def test_item5_a_wrap_after_a_title_is_one_flag_with_the_condition(text):
    _one_flag_with(text, "prior neck injury")


def test_item5_a_wrap_after_a_title_never_changes_the_flags_against_the_same_text_on_one_line():
    for t in ["Hx per EMS; who interpreted for Dr.\nSmith; prior neck injury.", "Hx per EMS; Hx per J.\nSmith; prior neck injury.", "Hx per EMS; who interpreted for Mrs.\nSmith; neck pain."]:
        assert _flags_no_overlap(t) == _flags_no_overlap(t.replace("\n", " ")), t          # same spans, so no 'Dr.' fragment quote


def test_item5_a_real_sentence_end_before_a_newline_is_still_hard():
    assert _quotes("Hx per EMS; seen at clinic.\nPrior neck injury.") == ["Hx per EMS; seen at clinic.", "Prior neck injury."]
    assert LS._soft_wraps("a Dr.\nb. \nc E.\nd.\ne") == "a Dr. b. \nc E. d.\ne"      # initials and titles soft, 'b.' and 'd.' hard


# ---- item 3, the other linear-time pieces: the helpers that used to rescan from 0 / to the end of the sentence for every hit give the same answers as the plain scans ----------------
def _bounds_reference(text, start, end):
    s = 0
    for m in LS.SENT_END.finditer(text, 0, start):
        s = m.end()
    m = LS.SENT_END.search(text, end)
    return s, (m.start() if m else len(text))


def _source_sentence_reference(text, end):
    import re
    m = LS._HISTORY_SOURCE.match(text, end) or LS._HISTORY_VIA.match(text, end)
    if not m:
        return False
    s = LS._SENT_END.search(text, m.end())
    return not re.search(r"\w", text[m.end():s.start() if s else len(text)])


def test_item3_sentence_bounds_and_source_sentence_equal_the_plain_scans_on_random_text():
    import random
    rnd = random.Random(1320)
    alpha = ["Hx", "per", "EMS", "son", "via", "neck", "pain", ".", ".", "!", "?", ";", ",", "\n", "\n", " ", " ", "  ", "Dr.", "2019", ":", "a.b", ".x"]
    for _ in range(1500):
        text = "".join(rnd.choice(alpha) + rnd.choice([" ", "", " "]) for _ in range(rnd.randint(1, 30)))
        for start in range(0, len(text) + 1, 3):
            end = min(len(text), start + rnd.randint(0, 4))
            assert LS._sentence_bounds(text, start, end) == _bounds_reference(text, start, end), (text, start, end)
        for end in range(len(text) + 1):
            assert LS._is_source_sentence(text, end) == _source_sentence_reference(text, end), (text, end)


def test_item3_negation_reads_only_the_clause_after_the_last_semicolon_and_the_first_tokens_after_the_hit():
    neg = __import__("app.backend.lexicon", fromlist=["load"]).load()["negation"]
    pad = "Hx per EMS; " * 300
    assert LS.negated(pad + "no neck pain.", len(pad + "no "), len(pad + "no neck pain"), neg)                    # pre-cue in the same clause
    assert not LS.negated(pad + "neck pain.", len(pad), len(pad + "neck pain"), neg)
    assert LS.negated(pad + "neck pain: none", len(pad), len(pad + "neck pain"), neg)                             # field answer
    assert not LS.negated("no cough; neck pain.", len("no cough; "), len("no cough; neck pain"), neg)            # the cue is before the ';'


# ---- mutant-killing rows for the r4 code (section header at a line start, long prefix before a title, colon without space, touching units) -------------------------------------------
@pytest.mark.parametrize("text,quote", [
    ("Hx per EMS\nTYLENOL #3: prn", "Hx per EMS"),                                            # '#' and digits: the caps header rule, not the 'Label:' rule
    ("Hx per EMS\nBP: 120/80", "Hx per EMS"),
    ("Hx per EMS\nNeck:pain, onset 2019.", "Hx per EMS\nNeck:pain, onset 2019."),             # a colon with no space after it is not a label
    ("Hx per EMS\nRe:neck pain.", "Hx per EMS\nRe:neck pain."),
])
def test_r4_header_and_label_edges(text, quote):
    assert _quotes(text) == [quote], _quotes(text)


def test_r4_a_title_wrap_far_from_the_start_of_the_text_is_still_not_a_sentence_end():
    t = "Seen at the clinic yesterday afternoon. Pain 7/10. Hx per EMS; Hx obtained via Dr.\nSmith; prior neck injury."
    assert any(q.endswith("prior neck injury.") and "Dr.\nSmith" in q for q in _quotes(t)), _quotes(t)
    assert LS._soft_wraps("x" * 80 + " Dr.\nSmith") == "x" * 80 + " Dr. Smith"
    assert LS._soft_wraps("x" * 80 + " end.\nSmith") == "x" * 80 + " end.\nSmith"
    assert LS._soft_wraps("x" * 80 + " approx.\n2 yrs ago") == "x" * 80 + " approx. 2 yrs ago"        # a longer abbreviation: the whole token is read


def test_r4_units_that_touch_but_do_not_overlap_stay_two_flags():
    t = "Hx of neck strain;Hx of back strain."
    assert len(_flags_no_overlap(t)) == 2 and len(_quotes(t)) == 2, _quotes(t)


@pytest.mark.parametrize("text", [                    # r5 (staff r4 minor 3): a titled name after 'who interpreted for' is attribution, so the flag holds the condition
    "Hx per EMS; who interpreted for Dr.\nSmith; prior neck injury.",
    "Hx per EMS; who interpreted for Dr. Smith; prior neck injury.",
    "Hx per EMS; who interpreted for Mrs. Jones; prior neck injury.",
])
def test_r5_a_titled_name_in_the_who_clause_is_attribution(text):
    assert _quotes(text) == [text], _quotes(text)
    assert len(_flags_no_overlap(text)) == 1
