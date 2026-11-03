"""Spanish-language records (T-085, D-042): language detection, grounding on the original Spanish, a labelled and judged English translation,
the D-034 token checks across the language gap, and a clear failure for unsupported languages. Fake model calls only; no key, no network."""
import ast
import json
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import dates, generator, grounding, ingest, language, pipeline as PL, sentences, spanish, spanish_text as ST
from app.backend.api import create_app
from app.db import db as DB
from app.llm import audited as AU, promptlib
from tests.unit._fakes import FakeCall

ROOT = pathlib.Path(__file__).resolve().parents[2]

ES_NOTE = ("Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al "
           "levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. "
           "Posible desgarro del manguito rotador. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00.")
ES_QUOTE = "Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento."
ES_SUMMARY = "Patient reports pain 6/10, worse when raising the arm. Denies loss of consciousness."
FR_NOTE = ("La patiente se plaint de douleur à l'épaule droite depuis trois jours. Elle n'a pas de perte de conscience et prend du "
           "paracétamol pour la douleur.")
EN_NOTE = "Patient states she was struck by a car while walking. Left shoulder pain 7/10. X-ray left shoulder negative for fracture."


def packet(*recs):
    out = ["SYNTHETIC — invented for evaluation; not real patient data", ""]
    for i, (date, src, exc) in enumerate(recs, 1):
        out += [f"=== Record {i} ===", f"Date: {date}", f"Source: {src}", f'Excerpt: "{exc}"', ""]
    return "\n".join(out).strip()


MIXED = packet(("2026-03-03", "Quillmere Regional ED", EN_NOTE),
               ("14/04/2026", "Consultorio Médico Aguaclara, nota de consulta", ES_NOTE))


# ---------------------------------------------------------------- language detection (code)
SPANISH = [
    "Paciente femenina de 35 años que acude por dolor cervical de 3 días de evolución posterior a choque vehicular por alcance.",
    "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00.",
    "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible.",
    ES_NOTE,
]
UNSUPPORTED = {
    "French": FR_NOTE,
    "German": "Der Patient klagt über Schmerzen in der rechten Schulter seit drei Tagen. Es besteht keine Bewusstlosigkeit und er nimmt Paracetamol.",
    "Portuguese": "O paciente refere dor no ombro direito há três dias. Nega perda de consciência e não tem outras queixas. A terapia é feita duas vezes por semana.",
    "Italian": "Il paziente riferisce dolore alla spalla destra da tre giorni. Non ha perso conoscenza e non assume altri farmaci per il dolore.",
    "Chinese": "患者右肩疼痛三天，无意识丧失。",
    "Cyrillic": "Пациент жалуется на боль в правом плече в течение трех дней.",
}


@pytest.mark.parametrize("text", SPANISH)
def test_spanish_text_is_detected(text):
    assert language.detect(text)["lang"] == "es"


@pytest.mark.parametrize("name,text", sorted(UNSUPPORTED.items()))
def test_other_languages_are_named_and_unsupported(name, text):
    d = language.detect(text)
    assert d["lang"] == "other" and d["name"] == name


def test_english_and_short_text_stay_supported():
    assert language.detect(EN_NOTE)["lang"] == "en"
    for short in ("03/05/2026 $650.00 12 3", "Rx cyclobenzaprine 10 mg qhs. RTC 2 wks.", "CT head negative.", ""):
        assert language.detect(short)["lang"] in ("unknown", "en")          # no evidence for any language: never 'other', never refused
    assert language.record_lang({"excerpt": "03/05/2026 $650.00"}) == "en"
    assert language.record_lang({"excerpt": "Consulta: $650.00"}) in ("es", "uncertain")      # one Spanish/Portuguese word and nothing else: never English (D-048)


def test_mixed_english_spanish_record_is_supported_not_refused():
    d = language.detect("Patient reports dolor de low back; MRI solicitada. Follow up in 2 weeks.")
    assert d["lang"] in ("en", "es") and d["mixed"] is True


def test_every_golden_and_library_record_keeps_its_language():
    """Only the three Spanish records of library packet 9 are Spanish; no English record is ever 'other' (that would skip it)."""
    seen = {}
    for p in sorted((ROOT / "evals" / "golden").glob("*.txt")) + sorted((ROOT / "evals" / "library").glob("*.txt")):
        try:
            recs = language.annotate(ingest.ingest(p.read_text())["records"])
        except ingest.IngestError:
            continue
        seen[p.name] = {r["lang"] for r in recs}
    assert all("other" not in v for v in seen.values()), seen
    assert {n for n, v in seen.items() if "es" in v} <= {n for n in seen if "spanish" in n}


def test_case_check_refuses_only_when_nothing_is_readable():
    es, en, fr = (dict(n=i, id=f"r{i}", lang=lg, lang_name="French" if lg == "other" else None) for i, lg in ((1, "es"), (2, "en"), (3, "other")))
    language.case_check([es, en, fr])                       # one unsupported record in a mixed packet is skipped, not refused
    language.case_check([])
    with pytest.raises(language.UnsupportedLanguage) as e:
        language.case_check([fr, dict(fr, n=4)])
    assert e.value.code == "unsupported_language" and e.value.names == ["French"]


# ---------------------------------------------------------------- the D-034 checks across the language gap
CHECKS = [
    # (summary, quote, label, date_iso, expected reasons)
    (ES_SUMMARY, ES_QUOTE, "", "", []),
    ("Patient reports pain 7/10, worse when raising the arm. Denies loss of consciousness.", ES_QUOTE, "", "", ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]),
    ("Patient reports pain 6/10, worse when raising the arm.", ES_QUOTE, "", "", ["SUMMARY_DROPS_QUALIFIER"]),                # niega dropped
    ("Pain 6/10, worse when raising the arm. No loss of consciousness.", ES_QUOTE, "", "", ["SUMMARY_DROPS_QUALIFIER"]),       # refiere dropped
    ("Patient reports pain 6/10, worse when raising the arm. Has loss of consciousness.", ES_QUOTE, "", "", ["SUMMARY_DROPS_QUALIFIER"]),   # niega lost
    ("Right shoulder pain. Patient reports it is worse when raising the arm.", "Refiere dolor en el hombro derecho que empeora al levantar el brazo.", "", "", []),
    ("Left shoulder pain. Patient reports it is worse when raising the arm.", "Refiere dolor en el hombro derecho que empeora al levantar el brazo.", "", "",
     ["SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER"]),                                                                # wrong side and the right side lost
    ("Patient reports shoulder pain.", "Refiere dolor en el hombro izquierdo.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),           # side lost
    ("Possible rotator cuff tear.", "Posible desgarro del manguito rotador.", "", "", []),
    ("Rotator cuff tear.", "Posible desgarro del manguito rotador.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),                         # hedge lost
    ("Findings consistent with muscle spasm.", "Hallazgos compatible con contractura muscular.", "", "", []),
    ("Muscle spasm.", "Hallazgos compatible con contractura muscular.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Consultation fee $1,250.00.", "Consulta: $1.250,00.", "", "", []),                                                          # Spanish number format
    ("Consultation fee $1,250.00.", "Consulta: $1,250.00.", "", "", []),
    ("Consultation fee $1,520.00.", "Consulta: $1.250,00.", "", "", ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]),
    ("Temperature 37.5.", "Temperatura 37,5 grados.", "", "", []),
    ("Pain for 3 days.", "Dolor de tres días de evolución.", "", "", []),                                                         # number words
    ("Pain for 4 days.", "Dolor de tres días de evolución.", "", "", ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]),
    ("Seen on May 14, 2026.", "Acude a consulta el 14 de mayo de 2026.", "", "", []),                                              # written month
    ("Seen on June 14, 2026.", "Acude a consulta el 14 de mayo de 2026.", "", "", ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]),
    ("Seen on June 3, 2026.", "Acude a consulta el 03/06/2026.", "", "", []),                                                      # numeric date read day first
    ("Seen on March 6, 2026.", "Acude a consulta el 03/06/2026.", "", "", ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]),
    ("No fracture seen.", "No se observa fractura.", "", "", []),
    ("Fracture seen.", "No se observa fractura.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Without fracture.", "Sin fractura.", "", "", []),
    ("No fracture.", "Sin fractura.", "", "", []),
    ("Pain approx. 20 minutes.", "Dolor aproximadamente 20 minutos.", "", "", []),
    ("Pain 20 minutes.", "Dolor aproximadamente 20 minutos.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),
    ("Suggests a sprain.", "Sugiere esguince cervical.", "", "", []),
    ("A sprain.", "Sugiere esguince cervical.", "", "", ["SUMMARY_DROPS_QUALIFIER"]),
]


@pytest.mark.parametrize("summary,quote,label,date_iso,expected", CHECKS)
def test_summary_checks_across_the_language_gap(summary, quote, label, date_iso, expected):
    assert ST.check_summary(summary, quote, label, date_iso) == expected


def test_english_checks_are_unchanged_for_english_records():
    assert ST.module_for("en") is grounding and ST.module_for("es") is ST
    assert grounding.check_summary("Pain 7/10.", "Pain 6/10.") == ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]


def test_spanish_hedge_sentence_after_the_quote_must_travel_with_it():
    text = "Contractura paravertebral cervical. Compatible con esguince. Plan: reposo."
    assert ST.check_excerpt(text, "Contractura paravertebral cervical.") == ["EXCERPT_OMITS_QUALIFIER"]
    assert ST.check_excerpt(text, "Contractura paravertebral cervical. Compatible con esguince.") == []
    assert grounding.check_excerpt(text, "Contractura paravertebral cervical.") == []          # the English lexicon alone misses it
    assert ST.check_excerpt(text, "Contractura cervical.") == ["GROUNDING_EXCERPT_NOT_VERBATIM"]


def test_quote_matching_is_verbatim_on_the_spanish_text_including_accents():
    assert grounding.locate(ES_NOTE, ES_QUOTE) is not None
    assert grounding.locate(ES_NOTE, ES_QUOTE.replace("é", "e")) is None             # an unaccented 'repair' is not verbatim


def test_spanish_titles_do_not_end_a_sentence_and_dates_parse():
    assert len(sentences.units("Evaluada por la Dra. García hoy. Niega fiebre.")) == 2
    assert dates.parse_date("14 de mayo de 2026")["iso"] == "2026-05-14"
    assert dates.parse_date("jueves 14 de mayo de 2026")["iso"] == "2026-05-14"
    assert dates.parse_date("14-ago-2026")["iso"] == "2026-08-14"
    assert dates.parse_date("14/05/2026")["status"] == "parsed" and dates.parse_date("03/06/2026")["status"] == "ambiguous"
    assert dates.parse_date("31 de abril de 2026")["status"] == "missing" and dates.parse_date("14 de mayo de 99")["status"] == "missing"


# ---------------------------------------------------------------- generator: extract -> verify -> judge
def _record(text=MIXED, n=2):
    return next(r for r in language.annotate(ingest.ingest(text)["records"]) if r["n"] == n)


def _es_script(summary=ES_SUMMARY, excerpt=ES_QUOTE, verdict=("supported", "NONE")):
    return {"extract_es": lambda u: dict(summary=summary, excerpt=excerpt),
            "judge_faithfulness_es": dict(verdict=verdict[0], reason_code=verdict[1])}


def test_spanish_record_uses_the_spanish_prompt_and_step_and_keeps_the_quote_verbatim():
    rec = _record()
    call = FakeCall(_es_script())
    e = generator.extract_one(rec, [2], call=call, case_text=MIXED)
    assert call.steps() == ["extract_es"]
    assert call.log[0]["system"] == promptlib.load("extract_es_v1").text
    assert e["excerpt"] == ES_QUOTE and e["summary"] == ES_SUMMARY and e["state"] == "needs_review" and e["reasons"] == ["AI_TRANSLATION"]        # D-050: code checks pass, still never verified
    assert MIXED[e["excerpt_start"]:e["excerpt_end"]] == ES_QUOTE                     # offsets point into the original Spanish text
    assert e["ladder"]["generator"]["prompt_version"] == "extract_es_v1"
    assert e["ladder"]["translation"]["label"] == "AI translation" and e["ladder"]["translation"]["source_language"] == "es"
    assert e["ladder"]["code_checks"]["summary_tokens_not_in_excerpt"] == [] and e["ladder"]["code_checks"]["excerpt_verbatim"] is True


def test_a_translated_quote_is_rejected_the_excerpt_is_always_the_original():
    rec = _record()
    e = generator.extract_one(rec, [2], call=FakeCall(_es_script(excerpt="Patient reports pain 6/10, worse when raising the arm.")), case_text=MIXED)
    assert e["state"] == "rejected" and "GROUNDING_EXCERPT_NOT_VERBATIM" in e["reasons"]


def test_english_record_still_uses_the_english_prompt():
    rec = _record(n=1)
    call = FakeCall({"extract": dict(summary="Left shoulder pain 7/10.", excerpt="Left shoulder pain 7/10.")})
    e = generator.extract_one(rec, [1], call=call, case_text=MIXED)
    assert call.steps() == ["extract"] and call.log[0]["system"] == promptlib.load("extract_v1").text and "translation" not in e["ladder"]


@pytest.mark.parametrize("bad_summary,reason", [
    ("Patient reports pain 9/10, worse when raising the arm. Denies loss of consciousness.", "SUMMARY_TOKEN_NOT_IN_EXCERPT"),
    ("Patient reports pain 6/10, worse when raising the arm.", "SUMMARY_DROPS_QUALIFIER"),
    ("Patient reports pain 6/10 in the left arm. Denies loss of consciousness.", "SUMMARY_TOKEN_NOT_IN_EXCERPT"),
])
def test_a_bad_translation_goes_to_review_with_the_d034_reason(bad_summary, reason):
    e = generator.extract_one(_record(), [2], call=FakeCall(_es_script(summary=bad_summary)), case_text=MIXED)
    assert e["state"] == "needs_review" and reason in e["reasons"]


def test_translation_judge_runs_with_its_own_prompt_and_its_verdict_sets_the_state():
    rec = _record()
    for verdict, code, state, reason in (("supported", "NONE", "needs_review", "AI_TRANSLATION"), ("partially", "DROPS_QUALIFIER", "needs_review", "JUDGE_PARTIAL"),
                                         ("unsupported", "OTHER_UNSUPPORTED", "needs_review", "JUDGE_UNSUPPORTED")):
        call = FakeCall(_es_script(verdict=(verdict, code)))
        e = generator.extract_one(rec, [2], call=call, case_text=MIXED)
        ents = generator.judge_entries([e], {2: rec}, call=call, case_text=MIXED)
        assert call.steps() == ["extract_es", "judge_faithfulness_es"]
        assert call.log[1]["system"] == promptlib.load("judge_faithfulness_es_v1").text
        assert ES_QUOTE in call.log[1]["user"] and ES_SUMMARY in call.log[1]["user"]
        assert ents[0]["state"] == state and (reason is None or reason in ents[0]["reasons"])
        assert ents[0]["ladder"]["judge"]["prompt_version"] == "judge_faithfulness_es_v1"


def test_unavailable_translation_judge_never_verifies():
    call = FakeCall({**_es_script(), "judge_faithfulness_es": AU.LLMFailed("x")})
    rec = _record()
    e = generator.extract_one(rec, [2], call=call, case_text=MIXED)
    ents = generator.judge_entries([e], {2: rec}, call=call, case_text=MIXED)
    assert ents[0]["state"] != "verified"


def test_unsupported_language_record_is_not_sent_to_a_model():
    text = packet(("2026-03-03", "Quillmere Regional ED", EN_NOTE), ("2026-03-10", "Clinique du Parc", FR_NOTE))
    recs = language.annotate(ingest.ingest(text)["records"])
    assert [r["lang"] for r in recs] == ["en", "other"]
    call = FakeCall({"extract": dict(summary="Left shoulder pain 7/10.", excerpt="Left shoulder pain 7/10.")})
    ents, rej, fails = generator.extract_entries(recs, ingest.ingest(text)["groups"], call=call, case_text=text)
    assert [f["failure"] for f in fails] == ["UNSUPPORTED_LANGUAGE"] and fails[0]["record_no"] == 2
    assert call.steps() == ["extract"] and len(ents) == 1


# ---------------------------------------------------------------- pipeline and API
def _script():
    return {"extract": lambda u: dict(summary="Left shoulder pain 7/10.", excerpt="Left shoulder pain 7/10."),
            "extract_es": lambda u: dict(summary=ES_SUMMARY, excerpt=ES_QUOTE),
            "j1": dict(verdict="supported", reason_code="NONE"), "judge_faithfulness_es": dict(verdict="supported", reason_code="NONE"),
            "j2": dict(verdict="agree", reason_code="NONE"), "j3": dict(verdict="benign", reason_code="NONE"),
            "j4": dict(verdict="agree", reason_code="NONE"), "conflicts": {"flags": []}, "flags": {"flags": []}}


def test_pipeline_runs_a_mixed_packet_and_warns_that_spanish_flags_come_from_the_ai_check_only(tmp_path):
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, ingest.normalize_text(MIXED), now=1.0)
    call = FakeCall(_script())
    out = PL.run_pipeline(conn, cid, MIXED, call=call, now=lambda: 1.0)
    assert out["status"] == "done" and not out["errors"]
    by = {e["seq"]: e for e in out["entries"]}
    assert "translation" not in by[1]["ladder"] and by[2]["ladder"]["translation"]["label"] == "AI translation"
    assert by[2]["excerpt"] == ES_QUOTE and by[2]["state"] == "needs_review" and "AI_TRANSLATION" in by[2]["reasons"]
    assert {r["n"]: r["lang"] for r in out["records"]} == {1: "en", 2: "es"}
    w = next(x for x in out["warnings"] if x["code"] == "SPANISH_RECORDS")
    assert w["record_nos"] == [2] and "English only" in w["message"]
    assert call.steps().count("extract_es") == 1 and call.steps().count("judge_faithfulness_es") == 1


def test_pipeline_skips_an_unsupported_record_with_a_warning_and_an_error(tmp_path):
    text = packet(("2026-03-03", "Quillmere Regional ED", EN_NOTE), ("2026-03-10", "Clinique du Parc", FR_NOTE))
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, ingest.normalize_text(text), now=1.0)
    call = FakeCall(_script())
    out = PL.run_pipeline(conn, cid, text, call=call, now=lambda: 1.0)
    assert out["status"] == "done_with_errors"
    assert [e["code"] for e in out["errors"]] == ["UNSUPPORTED_LANGUAGE"] and out["errors"][0]["record_no"] == 2
    w = next(x for x in out["warnings"] if x["code"] == "UNSUPPORTED_LANGUAGE")
    assert w["record_no"] == 2 and "French" in w["message"]
    assert [e["seq"] for e in out["entries"]] == [1]
    assert not any("douleur" in l["user"] for l in call.log)                    # the French text never reached a model


def test_pipeline_refuses_a_case_with_nothing_readable_and_leaves_no_running_case(tmp_path):
    text = packet(("2026-03-10", "Clinique du Parc", FR_NOTE))
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, ingest.normalize_text(text), now=1.0)
    with pytest.raises(language.UnsupportedLanguage):
        PL.run_pipeline(conn, cid, text, call=FakeCall(_script()), now=lambda: 1.0)
    c = DB.get_case(conn, cid)
    assert c["status"] == "failed" and json.loads(c["error"])["code"] == "unsupported_language"


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")                     # leaves demo mode; the fake call factory means no model is ever started
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    seen = []

    def factory(conn, cid):
        script = _script()

        def call(step, system, user, schema, *, item_id=None, validate=None):
            seen.append((step, item_id))
            v = script[step](user) if callable(script[step]) else script[step]
            return v, None
        return call
    app = create_app(str(tmp_path / "api.sqlite"), call_factory=factory, static_dir=str(tmp_path))
    return TestClient(app, client=("127.0.0.1", 50000)), seen, tmp_path


def _wait(c, tok):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            return s
        time.sleep(0.1)
    raise AssertionError(s)


def test_api_refuses_an_unsupported_language_case_clearly_and_stores_nothing(api):
    c, seen, tmp = api
    r = c.post("/api/cases", json={"text": packet(("2026-03-10", "Clinique du Parc", FR_NOTE))})
    e = r.json()["error"]
    assert r.status_code == 400 and e["code"] == "unsupported_language"
    assert "English and Spanish" in e["message"] and "French" in e["message"]
    assert e["detail"] == {"languages": ["French"], "supported": ["English", "Spanish"]}
    assert DB.connect(str(tmp / "api.sqlite")).execute("SELECT count(*) FROM cases").fetchone()[0] == 0
    assert seen == []
    z = c.post("/api/cases", json={"text": packet(("2026-03-10", "X", UNSUPPORTED["Chinese"]))})
    assert z.status_code == 400 and z.json()["error"]["detail"]["languages"] == ["Chinese"]
    assert c.post("/api/cases", json={"text": MIXED}).status_code == 201                      # Spanish is supported


def test_api_spanish_case_end_to_end_label_edit_export(api):
    c, seen, _ = api
    made = c.post("/api/cases", json={"text": MIXED}).json()
    tok = made["token"]
    assert [r["language"] for r in made["records"]] == ["en", "es"]
    assert any(w["code"] == "SPANISH_RECORDS" for w in made["warnings"])
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    assert _wait(c, tok)["status"] == "ready"
    case = c.get(f"/api/cases/{tok}").json()
    es = next(e for e in case["entries"] if "r2" in e["record_ids"])
    en = next(e for e in case["entries"] if "r1" in e["record_ids"])
    assert es["translation"]["label"] == "AI translation" and es["translation"]["quote_is_original"] is True
    assert en["translation"] is None
    assert es["excerpt"] == ES_QUOTE and es["state"] == "needs_review" and "AI_TRANSLATION" in es["reasons"] and es["ladder"]["judge"]["prompt_version"] == "judge_faithfulness_es_v1"
    # the paralegal edits the English summary: code checks against the Spanish quote, the translation judge runs, the label changes
    bad = c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "edit", "edits": {"summary": "Patient reports pain 9/10."}})
    assert bad.status_code == 422 or bad.status_code == 400
    ok = c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "edit", "edits": {"summary": "Patient reports pain 6/10; denies loss of consciousness."}})
    assert ok.status_code == 200, ok.text
    assert ok.json()["item"]["translation"]["label"] == "Translation (edited by reviewer)"
    assert ("judge_faithfulness_es", es["id"]) in seen
    c.post(f"/api/cases/{tok}/items/{en['id']}/review", json={"action": "accept"})
    assert ok.json()["item"]["state"] == "needs_review" and ok.json()["item"]["edit_to_check"] is True          # T-134/D-050: the edit is open until she accepts it
    assert "Patient reports pain 6/10" not in c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    assert c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "accept"}).status_code == 200      # her explicit accept after comparing it with the quote
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200
    letter = ex.json()["letter_text"]
    assert "Patient reports pain 6/10; denies loss of consciousness." in letter and "[Translation of the Spanish original, edited by reviewer; check before sending]" in letter and "Translation (edited by reviewer):" not in letter
    assert f'"{ES_QUOTE}"' in letter
    assert "Left shoulder pain 7/10." in letter and "AI translation: Left" not in letter


def test_api_unedited_spanish_entry_carries_the_ai_translation_label_in_the_letter(api):
    c, _, _ = api
    tok = c.post("/api/cases", json={"text": MIXED}).json()["token"]
    c.post(f"/api/cases/{tok}/run", json={})
    _wait(c, tok)
    es = next(e for e in c.get(f"/api/cases/{tok}").json()["entries"] if "r2" in e["record_ids"])
    assert c.post(f"/api/cases/{tok}/items/{es['id']}/review", json={"action": "accept"}).status_code == 200
    letter = c.get(f"/api/cases/{tok}/export").json()["letter_text"]
    assert ES_SUMMARY in letter and "AI translation:" not in letter and f'"{ES_QUOTE}"' in letter and letter.count("[AI translation of the Spanish original; check before sending]") == 1
    # the firm-voice paragraph is English-only: a translated entry is not fed to it
    r = c.post(f"/api/cases/{tok}/narrative")
    assert r.status_code == 400


# ---------------------------------------------------------------- boundary and prompt files
def test_code_half_imports_no_llm_client():
    for mod in ("spanish_text", "language"):
        tree = ast.parse((ROOT / "app" / "backend" / f"{mod}.py").read_text())
        names = {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module} | \
                {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        assert not any(x.startswith(("app.llm", "anthropic", "subprocess", "httpx", "requests")) for x in names), (mod, names)
        assert not {n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module == "app.backend"
                    for a in n.names if a.name in ("judges", "flags", "pipeline", "audited")}, mod


def test_prompts_are_versioned_and_say_what_they_must():
    ex, jd = promptlib.load("extract_es_v1"), promptlib.load("judge_faithfulness_es_v1")
    assert ex.name == "extract_es_v1" and "character for character" in ex.text and "never translated" in ex.text
    assert "03/06/2026" in ex.text and "derecho" in ex.text and "niega" in ex.text.lower()
    assert jd.name == "judge_faithfulness_es_v1" and "translation" in jd.text and "Spanish" in jd.text
    for name in ("extract_es_v1", "judge_faithfulness_es_v1"):
        assert "changelog: v1" in (ROOT / "app" / "llm" / "prompts" / f"{name}.md").read_text()
    from app.llm import audited as AU
    assert AU.PROMPT_OF_STEP["extract_es"] == "extract_es_v1" and AU.role_for("judge_faithfulness_es") == "judge"


# ---------------------------------------------------------------- recorded fixtures: library packet 9 (Spanish clinic note, intake form, statement)
def test_recorded_spanish_packet_replays_with_verbatim_spanish_quotes_and_labelled_translations(monkeypatch):
    path = ROOT / "evals" / "library" / "case_lib09_spanish_interpreter_espalda.txt"
    if not path.exists():
        pytest.skip("library packet 9 not present")
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("FIXTURE_SET", raising=False)
    text = path.read_text()
    view = PL.run_case(text)
    recs = {r["n"]: r for r in view["records"]}
    assert [n for n, r in recs.items() if r["lang"] == "es"] == [2, 4, 7]
    spanish_entries = [e for e in view["entries"] + view["undated_entries"] if e["ladder"].get("translation")]
    assert {e["seq"] for e in spanish_entries} == {2, 4, 7}, view["errors"]
    for e in spanish_entries:
        assert e["excerpt"] in text and e["ladder"]["translation"]["label"] == "AI translation"
        assert e["ladder"]["generator"]["prompt_version"] == "extract_es_v1" and e["ladder"]["judge"]["prompt_version"] == "judge_faithfulness_es_v1"
        assert e["ladder"]["judge"]["verdict"] == "supported" and e["ladder"]["code_checks"]["summary_tokens_not_in_excerpt"] == []
