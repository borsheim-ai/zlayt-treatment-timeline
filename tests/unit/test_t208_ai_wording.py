"""T-208 (T-201 staff review): the carrier letter never names an AI or a model. evals/letter_check.ai_wording is pure; measure() runs it over every letter of every case."""
import pytest
from evals import letter_check as LC

PLANTED = ["Drafted by an AI model (claude-sonnet-5-5).", "Reviewed by Claude", "Haiku pass", "opus", "the model wrote this", "AI-assisted", "Drafted by AI."]
CLEAN = ["Patient reports lower-back pain; gait not noted.", "Said he had an aim to return; the main plan was PT.", "Chair maintained the modeling clay exhibit.", "Dr. Chaim ordered an MRI."]


@pytest.mark.parametrize("text", PLANTED)
def test_each_ai_or_model_wording_is_found(text):
    assert LC.ai_wording("TREATMENT CHRONOLOGY\n\n" + text + "\n")


@pytest.mark.parametrize("text", CLEAN)
def test_ordinary_words_that_contain_the_letters_are_not_found(text):
    assert LC.ai_wording(text) == []


Q = "Paciente refiere dolor lumbar desde el accidente."
OK = LC.ALLOWED_AI_LABELS[0]
STD = f'April 14, 2026 — Clinic\nPatient reports low back pain.\nFrom Clinic, p. 2: "{Q}"\n{OK}\n'
ONE = f'April 14, 2026 — Clinic, p. 2: "{Q}" [Record 1] — English: Patient reports low back pain. {OK}\n'


def test_the_exact_translation_label_is_allowed_only_with_a_translated_quote():
    assert LC.ai_wording(STD, [Q]) == []                  # standard style: alone under the translated quote
    assert LC.ai_wording(ONE, [Q]) == []                  # one-line style: after the translated quote on the same line
    assert LC.ai_wording(STD.replace("check before sending", "drafted by an AI model"), [Q])
    assert LC.ai_wording(STD.replace(OK, OK + " Drafted by an AI model."), [Q])
    assert LC.ai_wording("[AI translation]", [Q])


def test_mutant_label_on_an_english_letter_fails():
    """T-208 r2: no translated source entry in the case, so the label fails wherever it is printed."""
    english = f'April 14, 2026 — Clinic\nPatient reports low back pain.\nFrom Clinic, p. 2: "Pt reports low back pain."\n{OK}\n'
    assert LC.ai_wording(english, [])
    assert LC.ai_wording(english)                                  # default: nothing is exempt
    assert LC.ai_wording(f"TREATMENT CHRONOLOGY\n\n{OK}\n", [])      # under the heading, as the review mutant placed it
    assert LC.ai_wording(STD)                                      # even the right layout fails without the case's translated quotes
    assert LC.ai_wording(ONE, [])


def test_label_away_from_the_translated_quote_fails():
    """Translated entry exists, but the label is not directly with its quote: under the heading, under another entry's quote, or after a blank line."""
    other = 'April 15, 2026 — Clinic\nPT note.\nFrom Clinic, p. 3: "Pt tolerated PT."\n'
    assert LC.ai_wording(f"TREATMENT CHRONOLOGY\n\n{OK}\n" + STD.replace(OK, ""), [Q])
    assert LC.ai_wording(other + OK + "\n" + STD.replace(OK, ""), [Q])
    assert LC.ai_wording(STD.replace(f'"\n{OK}', f'"\n\n{OK}'), [Q])
    assert LC.ai_wording(STD.replace(OK, "x " + OK), [Q])
    assert len(LC.ai_wording(STD + OK + "\n", [Q])) == 1          # a second copy of the label with no quote of its own: one hit, the first stays allowed


def test_measure_reports_ai_wording_in_every_variant_and_style(monkeypatch):
    bad = "TREATMENT CHRONOLOGY\n\nDrafted by an AI model.\n"
    got = {v: {"letters": {"standard": bad, "oneline": bad}, "notes": "", "charge_cents": [], "refused": [], "records": [], "dismissed_providers": [], "gate": {}}
           for v in ("all_accepted", "charges_dismissed", "counted")}
    monkeypatch.setattr(LC, "letters_for", lambda text, backend="fixture": got)
    monkeypatch.setattr(LC, "violations", lambda *a, **k: [])
    monkeypatch.setattr(LC, "charge_date_violations", lambda *a, **k: [])
    m = LC.measure([("x", "t")])
    hits = [v for v in m["per_case"]["x"] if "names AI or a model" in v]
    assert {h.split(": letter")[0] for h in hits} == {f"{st} ({v})" for st in ("standard", "oneline") for v in ("all_accepted", "charges_dismissed", "counted")}, m      # 3 variants x 2 styles


def test_measure_fails_the_label_on_an_english_case_and_passes_it_on_a_translated_one(monkeypatch):
    def run(quotes):
        got = {v: {"letters": {"standard": STD, "oneline": ONE}, "notes": "", "charge_cents": [], "refused": [], "records": [], "dismissed_providers": [], "gate": {}, "translated_quotes": quotes}
               for v in ("all_accepted", "charges_dismissed", "counted")}
        monkeypatch.setattr(LC, "letters_for", lambda text, backend="fixture": got)
        monkeypatch.setattr(LC, "violations", lambda *a, **k: [])
        monkeypatch.setattr(LC, "charge_date_violations", lambda *a, **k: [])
        return LC.measure([("x", "t")])
    assert run([Q])["value"] == 0
    bad = run([])
    assert bad["value"] == 6 and "x" in bad["per_case"], bad
