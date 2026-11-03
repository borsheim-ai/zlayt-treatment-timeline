"""T-085 round 2 (legal-nurse review): language detection fails safe, 'No se descarta' keeps its meaning, the Spanish cue lists are complete,
and the Spanish token checks and judge have a measured set (tests/unit/spanish_translation_pairs.jsonl; opt-in live judge eval below).
Fake model calls only except the opt-in live eval; no key, no network by default."""
import json
import os
import pathlib
import subprocess
import sys

import pytest

from app.backend import generator, ingest, language, spanish, spanish_text as ST
from app.llm import audited as AU
from tests.unit._fakes import FakeCall

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAIRS = [json.loads(line) for line in (ROOT / "tests/unit/spanish_translation_pairs.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]

# held-out short Spanish one-liners: every one resolves to es, none to en
SPANISH_SHORT = [
    "RM cervical: protrusión discal C5-C6, posible estenosis foraminal derecha.",
    "Cervicalgia postraumática, espasmo paravertebral, ROM reducido aprox. 40%.",
    "Dolor lumbar 7/10.", "Niega pérdida de conocimiento.", "Posible desgarro del menisco izquierdo.", "Rx rodilla derecha: sin fractura.",
    "Aqueja mareo al levantarse.", "Lumbalgia mecánica.", "Fisioterapia 2 veces por semana.", "Paciente refiere cefalea.",
    "Hernia discal L4-L5, no se descarta radiculopatía.", "Se indica reposo relativo por 5 días.", "Tomografía de cráneo normal.",
    "Contusión en hombro derecho, sin limitación.", "Alta médica. Control en 4 semanas.", "Esguince cervical grado II.",
    "Cita de control: 12/05/2026.", "Quizás exista lesión meniscal.", "Tal vez haya fractura.", "Impresiona como hernia discal.",
    "Consulta: $650.00",
]
FRENCH = ["Douleur cervicale 7/10, pas de perte de conscience.", "La patiente se plaint de douleur à l'épaule droite depuis trois jours.",
          "Radiographie du genou: pas de fracture.", "Le patient nie toute douleur.", "Douleur lombaire depuis deux semaines.",
          "IRM cervicale: hernie discale C5-C6."]
PORTUGUESE = ["Dor cervical 7/10. Nega perda de consciência. Fisioterapia.", "Paciente refere dor no ombro direito.",
              "Ressonância magnética: sem fratura.", "Dor lombar há duas semanas.", "Joelho esquerdo com dor."]
ITALIAN = ["Dolore alla spalla destra da tre giorni.", "Il paziente non ha perso conoscenza."]
GERMAN = ["Schmerzen im rechten Knie seit drei Tagen.", "Der Patient hat keine Schmerzen."]
ENGLISH_SHORT = ["Cervical MRI: disc protrusion at C5-C6 with foraminal stenosis.", "Left knee pain 6/10.", "Patient denies loss of consciousness.",
                 "CT head negative.", "Rx cyclobenzaprine 10 mg qhs. RTC 2 wks.", "Follow-up in 4 weeks.", "Physical therapy 2x/week.",
                 "Balance due $450.00", "No fracture.", "Possible meniscal tear.", "X-ray right shoulder: no fracture.",
                 "Plan: continue PT, pain control, follow up in 6 weeks.", "Pt c/o neck pain.", "MRI lumbar spine: L4-L5 disc bulge."]


# ---------------------------------------------------------------- blocker 1: the CLI
def _cli(tmp_path, name, text):
    f = tmp_path / name
    f.write_text(text, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "LLM_BACKEND", "ENABLE_LIVE")}
    return subprocess.run([sys.executable, "-m", "app.pipeline", str(f)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)


def _packet(*bodies):
    return "\n".join(f"=== Record {i} ===\nDate: 2026-03-0{i}\nSource: Quillmere Regional ED\nExcerpt: \"{b}\"\n" for i, b in enumerate(bodies, 1))


def test_cli_refuses_a_french_file_with_the_named_language_and_no_traceback(tmp_path):
    p = _cli(tmp_path, "fr.txt", _packet(FRENCH[1], FRENCH[0]))
    assert p.returncode == 1 and "refused: unsupported_language (French)" in p.stderr and "Traceback" not in p.stderr


def test_cli_runs_a_spanish_file_on_the_fixture_backend(tmp_path):
    p = _cli(tmp_path, "es.txt", _packet("Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento.", "Dolor lumbar 7/10."))
    assert p.returncode == 0 and "Traceback" not in p.stderr and "UnboundLocalError" not in p.stderr


def test_cli_runs_an_english_file(tmp_path):
    p = _cli(tmp_path, "en.txt", _packet("Patient states she was struck by a car while walking. Left shoulder pain 7/10.", "Left knee pain 6/10."))
    assert p.returncode == 0 and "Traceback" not in p.stderr


# ---------------------------------------------------------------- blockers 2 and 3: language detection on short lines
@pytest.mark.parametrize("line", SPANISH_SHORT)
def test_short_spanish_clinical_lines_are_spanish_never_english(line):
    got = language.detect(line)["lang"]
    assert got == "es" or (got == "uncertain" and line == "Consulta: $650.00")       # D-048: 'Consulta' is Spanish and Portuguese
    assert language.record_lang({"excerpt": line}) in ("es", "uncertain")


@pytest.mark.parametrize("name,lines", [("French", FRENCH), ("Portuguese", PORTUGUESE), ("Italian", ITALIAN), ("German", GERMAN)])
def test_short_lines_in_unsupported_languages_are_never_english_and_never_spanish(name, lines):
    for ln in lines:
        d = language.detect(ln)
        assert d["lang"] in ("other", "uncertain"), (ln, d)
        assert d["lang"] != "other" or d["name"] == name, (ln, d)
        assert language.record_lang({"excerpt": ln}) in ("other", "uncertain")


@pytest.mark.parametrize("line", FRENCH[:5] + PORTUGUESE[:4])
def test_clear_french_and_portuguese_lines_are_refused_by_name(line):
    d = language.detect(line)
    assert d["lang"] == "other" and d["name"] in ("French", "Portuguese")


@pytest.mark.parametrize("line", ENGLISH_SHORT)
def test_short_english_lines_stay_english(line):
    assert language.record_lang({"excerpt": line}) == "en"


def test_accented_text_with_no_resolved_language_is_uncertain_not_english():
    d = language.detect("Café, señal ü.")
    assert d["lang"] in ("uncertain", "es") and d["lang"] != "unknown"
    assert language.record_lang({"excerpt": "Zyxwv ñandú."}) in ("es", "uncertain")


def _uncertain_record():
    rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": "Kein Bewusstseinsverlust.", "date_iso": "2026-03-03", "date_status": "parsed"}
    rec["lang"] = "uncertain"
    rec["lang_reason"] = "test"
    return rec


def test_uncertain_record_goes_the_translation_path_is_never_verified_and_never_gets_english_checks():
    rec = _uncertain_record()
    call = FakeCall({"extract_es": lambda u: dict(summary="No loss of consciousness.", excerpt="Kein Bewusstseinsverlust.")})
    e = generator.extract_one(rec, [1], call=call, case_text="x")
    assert call.steps() == ["extract_es"]                       # not the English extract step
    assert e["state"] == "needs_review" and "LANGUAGE_UNCERTAIN" in e["reasons"]
    assert e["ladder"]["translation"]["label"] == "AI translation" and e["ladder"]["translation"]["source_language"] == "uncertain"
    judged = generator.judge_entries([e], {1: rec}, call=FakeCall({"judge_faithfulness_es": dict(verdict="supported", reason_code="NONE")}), case_text="x")
    assert judged[0]["state"] == "needs_review" and "LANGUAGE_UNCERTAIN" in judged[0]["reasons"]     # a supporting judge cannot clear it
    assert judged[0]["ladder"]["judge"]["prompt_version"] == "judge_faithfulness_es_v1"
    assert spanish.module_for("uncertain") is ST and spanish.module_for("en") is not ST


def test_uncertain_record_warns_with_the_reason_and_the_case_is_not_refused():
    recs = language.annotate([{"n": 1, "id": "r1", "excerpt": "Kein Bewusstseinsverlust."}, {"n": 2, "id": "r2", "excerpt": "Left knee pain 6/10."}])
    assert recs[0]["lang"] == "uncertain" and recs[1]["lang"] == "en"
    language.case_check(recs)
    w = [x for x in language.record_warnings(recs) if x["code"] == "LANGUAGE_UNCERTAIN"]
    assert len(w) == 1 and w[0]["record_no"] == 1 and "never marked verified" in w[0]["message"]


def test_a_case_of_only_unsupported_language_short_lines_is_refused():
    recs = language.annotate([{"n": i + 1, "id": f"r{i + 1}", "excerpt": ln} for i, ln in enumerate(FRENCH[:3])])
    with pytest.raises(language.UnsupportedLanguage) as ei:
        language.case_check(recs)
    assert ei.value.names == ["French"]


def test_french_short_line_in_a_packet_is_skipped_not_translated_as_spanish():
    rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": FRENCH[0]}
    language.annotate([rec])
    e = generator.extract_one(rec, [1], call=FakeCall(), case_text="x")
    assert e == {"failure": "UNSUPPORTED_LANGUAGE", "record_no": 1}


# ---------------------------------------------------------------- major: 'No se descarta' and the cue lists
@pytest.mark.parametrize("summary,quote,expected", [
    ("Fracture ruled out.", "No se descarta fractura.", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Fracture excluded.", "No se descarta fractura.", ["SUMMARY_DROPS_QUALIFIER"]),
    ("No fracture.", "No se descarta fractura.", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Fracture ruled out.", "No se puede descartar fractura.", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Fracture.", "No se descarta fractura.", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Fracture cannot be excluded.", "No se descarta fractura.", []),
    ("Fracture cannot be ruled out.", "No se descarta fractura.", []),
    ("Fracture not excluded.", "No se descarta fractura.", []),
    ("Fracture possible.", "No se descarta fractura.", []),
    ("Fracture ruled out.", "Se descarta fractura.", []),
    ("Fracture excluded.", "Fractura descartada.", []),
    ("Fracture cannot be excluded.", "Se descarta fractura.", ["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER"]),     # D-047: the hedge is also one the quote lacks
])
def test_no_se_descarta_keeps_its_meaning_and_ruled_out_fails_it(summary, quote, expected):
    assert ST.check_summary(summary, quote) == expected


@pytest.mark.parametrize("summary,quote,kind", [
    ("Neck pain 7/10.", "Aqueja dolor cervical 7/10.", "self_report"),
    ("Low back pain since the accident.", "Alega dolor lumbar desde el accidente.", "self_report"),
    ("Left knee pain.", "Señala dolor en rodilla izquierda.", "self_report"),
    ("Dizziness on standing.", "Expresa mareo al ponerse de pie.", "self_report"),
    ("Meniscal injury.", "Quizás exista lesión meniscal.", "hedge"),
    ("Meniscal injury.", "Quiza exista lesión meniscal.", "hedge"),
    ("Fracture.", "Tal vez haya fractura.", "hedge"),
    ("Disc herniation.", "Impresiona como hernia discal.", "hedge"),
    ("Radicular compromise.", "Eventual compromiso radicular.", "hedge"),
    ("Knee pain.", "Jamás había tenido dolor de rodilla.", "negation"),
    ("History of lumbar surgery.", "Carece de antecedentes de cirugía lumbar.", "negation"),
    ("Patient has neurological symptoms.", "Paciente libre de síntomas neurológicos.", "negation"),
    ("Fever and chills.", "Ni fiebre ni escalofríos.", "negation"),
    ("Pain when walking.", "Nada de dolor al caminar.", "negation"),
])
def test_each_added_cue_word_is_a_qualifier_the_summary_must_carry(summary, quote, kind):
    assert kind in ST.dropped_qualifiers(summary, quote)
    assert "SUMMARY_DROPS_QUALIFIER" in ST.check_summary(summary, quote)


@pytest.mark.parametrize("summary,quote", [
    ("However, pain persists.", "Sin embargo, el dolor persiste."),
    ("Undoubtedly there is spasm.", "Sin duda hay espasmo."),
    ("Complains of neck pain 7/10.", "Aqueja dolor cervical 7/10."),
    ("Alleges low back pain since the accident.", "Alega dolor lumbar desde el accidente."),
    ("Perhaps a meniscal injury.", "Quizás exista lesión meniscal."),
    ("Appears to be a disc herniation.", "Impresiona como hernia discal."),
    ("Never had knee pain before.", "Jamás había tenido dolor de rodilla."),
    ("Lacks a history of lumbar surgery.", "Carece de antecedentes de cirugía lumbar."),
    ("Patient free of neurological symptoms.", "Paciente libre de síntomas neurológicos."),
])
def test_faithful_translations_with_the_new_cues_pass(summary, quote):
    assert ST.check_summary(summary, quote) == []


def test_a_no_se_descarta_sentence_after_the_quote_must_travel_with_it():
    text = "Hernia discal L4-L5. No se descarta radiculopatía."
    assert ST.is_hedge_unit("No se descarta radiculopatía.")
    assert "EXCERPT_OMITS_QUALIFIER" in ST.check_excerpt(text, "Hernia discal L4-L5.")


# ---------------------------------------------------------------- major: a measured set for the Spanish token checks and judge
def test_the_pair_set_is_big_and_covers_every_kind():
    assert len(PAIRS) >= 40 and len({p["id"] for p in PAIRS}) == len(PAIRS)
    kinds = {p["kind"] for p in PAIRS}
    assert {"control", "negation", "laterality", "hedge", "self_report", "number", "judge_only"} <= kinds
    assert sum(1 for p in PAIRS if not p["faithful"]) >= 30 and sum(1 for p in PAIRS if p["faithful"]) >= 15


def test_code_checks_flag_every_unfaithful_pair_they_should_and_no_faithful_control():
    missed = [p["id"] for p in PAIRS if p["code_flags"] and not ST.check_summary(p["summary"], p["quote"])]
    false_pos = [p["id"] for p in PAIRS if p["faithful"] and ST.check_summary(p["summary"], p["quote"])]
    assert missed == [] and false_pos == []
    # pairs the code layer is not expected to catch (meaning changes with no checked token) are the judge's: they are listed, not hidden
    assert {p["id"] for p in PAIRS if not p["faithful"] and not p["code_flags"]} == {p["id"] for p in PAIRS if p["kind"] == "judge_only"}


@pytest.mark.skipif(os.environ.get("SPANISH_JUDGE_EVAL") != "1" or os.environ.get("ENABLE_LIVE") != "1",
                    reason="live judge eval: run with SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1 LLM_BACKEND=claude-cli (about 55 model calls)")
def test_live_translation_judge_recall_and_false_positive_rate(tmp_path):
    """Measures judge_faithfulness_es_v1 on the pair set: every unfaithful pair must come back not 'supported', no control may come back
    'unsupported'. qa: record fixtures for these calls and add the rates to the library report."""
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / "judge.sqlite"))
    cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
    call = AU.make_call(conn, cid)
    bad_supported, good_unsupported = [], []
    for p in PAIRS:
        verdict, _, _ = spanish.run_j1_meta(p["summary"], p["quote"], "Clinic", call=call, nonce="n" + p["id"], item_id=p["id"], lang="es")
        if not p["faithful"] and verdict == "supported":
            bad_supported.append(p["id"])
        if p["faithful"] and verdict == "unsupported":
            good_unsupported.append(p["id"])
    assert bad_supported == [] and good_unsupported == []
