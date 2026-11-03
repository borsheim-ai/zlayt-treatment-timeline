"""T-085 round 3 (D-048): language routing fails safe, and it is MEASURED on a labelled file written before the run.

tests/unit/language_routing_heldout.jsonl: 244 rows (one-liners and short notes; test_the_docstring_row_count_is_right keeps this number true), labelled by hand (es with and without accents, en, mixed en/es,
it, pt, fr, de; short and long). `source`: reviewer_probe = a line the T-085 reviewer used (in-sample for the word lists); authored = written
for this set before the first run; authored_batch2 = a second fresh batch, run once; tuned_after_miss = a batch-2 line the first run got wrong,
after which the lists were extended (in-sample from then on); r4_collision = English rows with stray foreign-list words (son, operation,
plus, solo, eventual, hernia, vertebral...) written for T-085 r4 after the r3 review. `ambiguous` rows are real in both languages (Rotator
cuff tendinitis.) and count for neither the English rate nor a miss. `d050_only` rows (Italian that is word for word Spanish) cannot be routed
by any word list; they are not in the routing gates, and test_d050 shows they are never verified. Print the confusion matrix with:  python -m tests.unit.test_language_routing_heldout

Acceptable routes (D-048): en -> en; es and mixed -> es or uncertain, NEVER en; it/pt/fr/de -> other or uncertain, NEVER en or es.
`uncertain` is a safe answer for a non-English line (translation path, needs_review, labelled); it is a cost, not an error, for an English line.
"""
import collections
import json
import pathlib

import pytest

from app.backend import generator, language, spanish_text as ST
from tests.unit._fakes import FakeCall

HELD = pathlib.Path(__file__).with_name("language_routing_heldout.jsonl")
ALL_ROWS = [json.loads(line) for line in HELD.read_text(encoding="utf-8").splitlines() if line.strip()]
ROWS = [r for r in ALL_ROWS if not r.get("d050_only")]
D050_ONLY = [r for r in ALL_ROWS if r.get("d050_only")]
ACCEPT = {"en": {"en"}, "es": {"es", "uncertain"}, "mixed": {"es", "uncertain"}, "it": {"other", "uncertain"}, "pt": {"other", "uncertain"},
          "fr": {"other", "uncertain"}, "de": {"other", "uncertain"}}
EXACT = {"en": "en", "es": "es", "mixed": "es", "it": "other", "pt": "other", "fr": "other", "de": "other"}


def route(text):
    return language.record_lang({"excerpt": text})


def confusion(rows=ROWS):
    cm = collections.defaultdict(collections.Counter)
    for r in rows:
        cm[r["label"]][route(r["text"])] += 1
    return cm


def report(rows=ROWS):
    cm = confusion(rows)
    cols = ["en", "es", "other", "uncertain"]
    lines = [f"{'label':8}" + "".join(f"{c:>11}" for c in cols) + f"{'n':>6}"]
    for lab in ACCEPT:
        lines.append(f"{lab:8}" + "".join(f"{cm[lab][c]:>11}" for c in cols) + f"{sum(cm[lab].values()):>6}")
    safe = sum(1 for r in rows if route(r["text"]) in ACCEPT[r["label"]]) / len(rows)
    exact = sum(1 for r in rows if route(r["text"]) == EXACT[r["label"]]) / len(rows)
    lines.append(f"safe routing {safe:.1%} · exact routing {exact:.1%} · n={len(rows)}")
    return "\n".join(lines), safe, exact


def test_the_file_is_big_labelled_and_covers_every_kind():
    assert len(ROWS) >= 120
    assert {r["label"] for r in ROWS} == set(ACCEPT)
    assert sum(1 for r in ROWS if r["label"] == "es" and any(ord(c) > 127 for c in r["text"])) >= 10          # Spanish with accents
    assert sum(1 for r in ROWS if r["label"] == "es" and all(ord(c) < 128 for c in r["text"])) >= 30         # Spanish without
    assert sum(1 for r in ROWS if r["label"] == "mixed") >= 12
    assert sum(1 for r in ROWS if len(r["text"]) > 150) >= 10 and sum(1 for r in ROWS if len(r["text"]) < 40) >= 40
    assert {r["source"] for r in ROWS} >= {"reviewer_probe", "authored", "authored_batch2", "r4_collision"}


def test_the_docstring_row_count_is_right():
    assert f"{len(ALL_ROWS)} rows" in __doc__


def test_no_non_english_line_is_routed_as_english():
    bad = [(r["label"], r["text"]) for r in ROWS if r["label"] != "en" and route(r["text"]) == "en"]
    assert bad == []


def test_no_italian_portuguese_french_or_german_line_is_routed_as_spanish():
    bad = [(r["label"], r["text"]) for r in ROWS if r["label"] in ("it", "pt", "fr", "de") and route(r["text"]) == "es"]
    assert bad == []


def test_every_line_takes_an_acceptable_route():
    bad = [(r["label"], route(r["text"]), r["text"]) for r in ROWS if route(r["text"]) not in ACCEPT[r["label"]] and r["label"] != "en"]
    assert bad == []


def test_english_lines_stay_english_with_a_known_cost_for_cognate_only_lines():
    en = [r for r in ROWS if r["label"] == "en"]
    got = [route(r["text"]) for r in en]
    assert all(g in ("en", "uncertain") for g in got)                 # never refused, never Spanish
    assert sum(g == "en" for g in got) / len(en) >= 0.85, [(r["text"], g) for r, g in zip(en, got) if g != "en"]


def test_english_rows_meet_the_r3_gate_60_rows_none_spanish_at_most_5_percent_uncertain():
    en = [r for r in ROWS if r["label"] == "en" and not r.get("ambiguous")]
    got = [route(r["text"]) for r in en]
    assert len(en) >= 60 and sum(r["source"] == "r4_collision" for r in en) >= 30
    assert "es" not in got and "other" not in got
    assert sum(g == "uncertain" for g in got) / len(en) <= 0.05, [(r["text"], g) for r, g in zip(en, got) if g != "en"]
    assert all(route(r["text"]) in ("en", "uncertain") for r in ROWS if r.get("ambiguous"))


R3_ENGLISH = [
    "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. "
    "X-ray left shoulder negative for fracture.",
    "Patient tolerated the operation well and was discharged home.",
    "Pain plus numbness in the right hand. Follow up in four weeks.",
    "MRI: small hernia at L5-S1, mild vertebral body edema, no radicular signs.",
    "Patient was walking solo when struck by a vehicle. Complains of left hip pain.",
    "Radiology: eventual follow-up recommended. Findings: no acute fracture.",
]


@pytest.mark.parametrize("line", R3_ENGLISH)
def test_the_reviewers_english_lines_with_stray_foreign_list_words_stay_english(line):
    assert route(line) == "en"


def test_the_reviewers_er_record_in_library_09_stays_english():
    lib = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library" / "case_lib09_spanish_interpreter_espalda.txt"
    if not lib.exists():
        pytest.skip("library packet 9 not present")
    from app.backend import ingest
    recs = language.annotate(ingest.ingest(lib.read_text())["records"])
    assert {r["n"]: r["lang"] for r in recs}[1] == "en" and {r["n"] for r in recs if r["lang"] == "es"} == {2, 4, 7}


# foreign lines that carry the same collision words must still never become English
FOREIGN_WITH_COLLISION_WORDS = [
    "Paciente camina solo, sin dolor.", "Dolor lumbar plus hernia discal.", "Son dolores en el cuello desde el accidente.",
    "Hernia discal L5-S1, operation programada.", "Suspeita de hernia discal L4-L5.", "Hernia discal L5-S1 com compressao radicular.",
    "Il paziente cammina solo, nessuna frattura.", "Le patient marche solo, pas de fracture, plus de douleur.", "Eventual cirugia programada.",
    "Dolor vertebral con signos radiculares.", "Dolor basal 4/10, sin radiculopatia.",
]


@pytest.mark.parametrize("line", FOREIGN_WITH_COLLISION_WORDS)
def test_collision_words_do_not_turn_a_foreign_line_into_english(line):
    assert route(line) != "en"


@pytest.mark.parametrize("line", ["Suspeita de hernia discal L4-L5.", "Hernia discal L5-S1 com compressao radicular."])
def test_the_reviewers_portuguese_lines_do_not_route_as_spanish(line):
    assert route(line) in ("other", "uncertain")


def test_the_reviewers_italian_line_that_is_word_for_word_spanish_is_held_by_d050_not_by_routing():
    assert [r["text"] for r in D050_ONLY] == ["Cervicalgia post-traumatica."]
    for r in D050_ONLY:
        assert route(r["text"]) in ("es", "uncertain")                 # it cannot be told from Spanish, and it must never be English
        rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": r["text"]}
        call = FakeCall({"extract_es": lambda u, t=r["text"]: dict(summary="Post-traumatic cervicalgia.", excerpt=t),
                         "judge_faithfulness_es": dict(verdict="supported", reason_code="NONE")})
        e = generator.extract_one(rec, [1], call=call, case_text="x")
        e = generator.judge_entries([e], {1: rec}, call=call, case_text="x")[0]
        assert e["state"] == "needs_review" and "AI_TRANSLATION" in e["reasons"] and e["state"] != "verified"


def test_routing_accuracy_is_reported_and_has_a_floor():
    text, safe, exact = report()
    print("\n" + text)
    assert safe >= 0.95 and exact >= 0.6, text      # exact is low by design: a cognate-heavy unaccented Spanish line is 'uncertain' (safe), not 'es'


def test_every_reviewer_probe_in_the_file_is_handled_correctly():
    probes = [r for r in ROWS if r["source"] == "reviewer_probe"]
    assert len(probes) >= 25
    bad = [(r["label"], route(r["text"]), r["text"]) for r in probes if route(r["text"]) not in ACCEPT[r["label"]]]
    assert bad == []


# reviewer r1 and r2 probes that are not (or not only) routing probes
R2_SPANISH = ["Escoliosis leve.", "Artrosis facetaria L4-L5.", "Contractura trapecio.", "Vertigo postural.", "Cirugia programada.", "Ibuprofeno 400 mg.",
              "Hernia L5-S1.", "TAC normal.", "Neumonia basal.", "Reduccion cerrada.", "Velocidad aproximada 35 mph.", "Dudoso edema oseo.",
              "RM cervical: protrusión discal C5-C6, posible estenosis foraminal derecha.", "Cervicalgia postraumática, espasmo paravertebral, ROM reducido aprox. 40%."]
R2_FOREIGN = ["Receita: ibuprofeno 400 mg.", "Cirurgia agendada.", "Nessuna frattura.", "Possibile frattura dello scafoide.", "Ricetta: ibuprofene 400 mg.",
              "Intervento programmato.", "Kontrolle in vier Wochen.", "Rezept: Ibuprofen 400 mg.", "Operation geplant.", "Nessuna frattura alla radiografia.",
              "Dor cervical 7/10. Nega perda de consciência. Fisioterapia.", "Douleur cervicale 7/10, pas de perte de conscience.",
              "La patiente se plaint de douleur à l'épaule droite depuis trois jours."]
R2_MIXED = ["MRI lumbar: protrusión L4-L5, posible compresión radicular.", "Pt refiere neck pain 7/10 desde el accidente.",
            "Patient reports dolor 7/10 en hombro derecho."]


@pytest.mark.parametrize("line", R2_SPANISH + R2_MIXED)
def test_reviewer_spanish_and_mixed_probes_are_es_or_uncertain(line):
    assert route(line) in ("es", "uncertain")


@pytest.mark.parametrize("line", R2_FOREIGN)
def test_reviewer_foreign_probes_are_never_english_and_never_spanish(line):
    assert route(line) in ("other", "uncertain")


@pytest.mark.parametrize("line", R2_SPANISH + R2_MIXED + R2_FOREIGN)
def test_no_reviewer_probe_runs_the_english_extract_step_unlabelled(line):
    rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": line}
    call = FakeCall({"extract_es": lambda u: dict(summary="Summary.", excerpt=line)})
    e = generator.extract_one(rec, [1], call=call, case_text="x")
    if route(line) == "other":
        assert e == {"failure": "UNSUPPORTED_LANGUAGE", "record_no": 1}
    else:
        assert call.steps() == ["extract_es"] and e["ladder"]["translation"]["label"] == "AI translation"
        if route(line) == "uncertain":
            assert e["state"] == "needs_review" and "LANGUAGE_UNCERTAIN" in e["reasons"]


def test_every_non_english_line_in_the_file_skips_the_english_step():
    for r in ROWS:
        if r["label"] == "en":
            continue
        rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": r["text"]}
        call = FakeCall({"extract_es": lambda u, t=r["text"]: dict(summary="Summary.", excerpt=t)})
        generator.extract_one(rec, [1], call=call, case_text="x")
        assert "extract" not in call.steps(), r["text"]


# ---------------------------------------------------------------- union of the English and Spanish checks on mixed quotes
@pytest.mark.parametrize("summary,quote,kind", [
    ("Lumbar MRI: protrusion at L4-L5 with nerve root compression.", "MRI lumbar: protrusión L4-L5, posible compresión radicular.", "hedge"),
    ("Right shoulder pain 7/10.", "Patient reports dolor 7/10 en hombro derecho.", "self_report"),
    ("Neck pain 7/10 since the accident.", "Pt refiere neck pain 7/10 desde el accidente.", "self_report"),
    ("Meniscal finding.", "Hallazgo incierto en menisco.", "hedge"),
    ("Fracture line.", "Dudoso trazo de fractura.", "hedge"),
    ("Bone edema.", "Dudoso edema oseo.", "hedge"),
    ("Traumatic injury.", "Lesion presuntamente traumatica.", "hedge"),
    ("Fell from the stairs.", "A decir del paciente, cayo de la escalera.", "self_report"),
    ("Pain 7/10.", "Calificó el dolor como 7/10.", "self_report"),
    ("Speed 35 mph.", "Velocidad aproximada 35 mph.", "approx"),
    ("Speed 35 mph.", "Velocidad aproximado 35 mph.", "approx"),
    ("Knee MRI without tear.", "Knee MRI: no se descarta tear, possible ACL sprain.", "hedge"),
])
def test_mixed_and_new_cue_quotes_fail_when_the_summary_drops_the_qualifier(summary, quote, kind):
    assert kind in ST.dropped_qualifiers(summary, quote)
    assert "SUMMARY_DROPS_QUALIFIER" in ST.check_summary(summary, quote)


@pytest.mark.parametrize("summary,quote", [
    ("Lumbar MRI: protrusion at L4-L5, possible nerve root compression.", "MRI lumbar: protrusión L4-L5, posible compresión radicular."),
    ("Patient reports pain 7/10 in the right shoulder.", "Patient reports dolor 7/10 en hombro derecho."),
    ("Patient reports neck pain 7/10 since the accident.", "Pt refiere neck pain 7/10 desde el accidente."),
    ("Uncertain meniscal finding.", "Hallazgo incierto en menisco."),
    ("Doubtful fracture line.", "Dudoso trazo de fractura."),
    ("Presumably a traumatic injury.", "Lesion presuntamente traumatica."),
    ("Per the patient, fell from the stairs.", "A decir del paciente, cayo de la escalera."),
    ("Patient rated the pain 7/10.", "Calificó el dolor como 7/10."),
    ("Approximate speed 35 mph.", "Velocidad aproximada 35 mph."),
])
def test_faithful_summaries_of_mixed_and_new_cue_quotes_pass(summary, quote):
    assert ST.check_summary(summary, quote) == []


def test_the_word_lists_do_not_claim_english_words_for_a_foreign_language():
    # an English word in a foreign list would make English text 'non-English evidence'; words shared with English are listed on both sides on purpose
    english_core = language._set("patient the and with pain left right fracture follow mri knee neck back shoulder")
    for code in ("es", "pt", "it", "de"):
        assert not (language._STOP[code] & language._set("the and with pain left right follow mri knee neck back shoulder")), code
    assert not (language._ROMANCE & language._STOP["en"]) and english_core


if __name__ == "__main__":
    print(report()[0])
