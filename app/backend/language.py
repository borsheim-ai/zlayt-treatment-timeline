"""Record language detection (D-042, D-048, T-085). Deterministic code, no model: a word-list and script scorer over the record body.

FAIL SAFE (D-048). A record runs as English only when it is CONFIDENTLY English: enough English function and clinical words and no
non-English evidence at all (no accented letter, no Spanish/Portuguese/Italian/French/German function word, clinical stem or ending).
Everything else is either confidently Spanish, confidently another language, or `uncertain`. Outcomes:
  `en`         confidently English.
  `es`         confidently Spanish; `mixed` is set when English wording is also present ("Pt refiere neck pain 7/10").
  `other`      confidently something else (a name for the message); the pipeline refuses a case with no supported record and skips (and
               says so about) an unsupported record in a mixed packet. Italian, Portuguese, French and German never route to Spanish.
  `uncertain`  non-English evidence but no confident answer, or no English evidence at all on a line with words the English lists do not
               know (a short, unaccented, cognate-heavy line). The record is still read through the translation path (Spanish prompt, the
               union of English and Spanish token checks, translation judge), is never `verified` (reason LANGUAGE_UNCERTAIN) and carries a
               warning. The English-only token checks never run for it.
  `unknown`    nothing to judge (numbers, codes, abbreviations that are all known English). Treated as English.
Mixed English/Spanish text is supported: it routes `es` with `mixed` set and the Spanish module runs the English cue checks as well.
"""
import re
import unicodedata

SUPPORTED = ("en", "es")
NAMES = {"en": "English", "es": "Spanish", "fr": "French", "de": "German", "pt": "Portuguese", "it": "Italian",
         "uncertain": "an unidentified language"}
MIXED_SCORE = 0.12
FOREIGN_MARGIN = 1.5         # an unsupported language needs this factor over the best competitor to be named
ES_VS_UNSUPPORTED = 1.6      # Spanish must beat French/Portuguese/Italian/German by this factor on the word evidence, else uncertain
ES_SHARE_SHORT = 0.6        # on a short line, this share of its words of 4+ letters must be words the Spanish, Romance or English lists know
ES_SHARE_LONG = 0.5
EN_CONFIDENT = 1.0           # English-only evidence needed (a single English-only word) when there is no non-English evidence

_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)


def _fold(w: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", w.lower()) if unicodedata.category(c) != "Mn")


def _set(s: str) -> frozenset:
    return frozenset(_fold(w) for w in s.split())


_STOP = {
    "en": _set("the and of to in is was were with for on at by from patient pain has had have he she her his their reports states "
               "reported stated denies visit follow up notes note plan exam examination history chief complaint diagnosis treatment "
               "referred shoulder back neck left right which this that are be been will daily twice weeks days week months month year years "
               "recommend recommended continue continued physical therapy ordered review reviewed charge fee balance statement no not or an as it its "
               "low spine knee mri x-ray findings mild moderate severe injury accident since after before pt "
               # added D-048: function words, common clinical words and abbreviations that are English and not another listed language
               "if when while during into over under about because than then there they them we our you your my do does did can could would "
               "should may might must also one two three four five six seven eight nine ten only other more some any all each both per via head chest pelvis hip ankle foot wrist elbow hand arm "
               "leg fracture fractures tear sprain strain disc negative positive denied complains complaining c/o rx rtc qhs wks wk prn bid tid "
               "hx dx tx fx s/p ct emg ncv er due total paid amount date source excerpt record records seen saw presented presents arrived "
               "released discharged discharge home work return returned symptoms symptom swelling bruising tenderness range motion limited "
               "stiffness numbness tingling headache headaches dizziness nausea fever chills worse worsened improved improving better "
               "medication medications dose tablets tablet capsule pill surgery surgical procedure procedures scheduled recommended referral "
               "small noted intact tolerated reflexes strength symmetric advised"
               "evaluation evaluated consult consultation appointment clinic hospital emergency department imaging radiograph scan "),
    "es": _set("de la el los las un una unos unas del al y en con por para sin sobre entre desde hasta que se su sus es son fue fueron "
               "esta estan ha han hay pero como mas muy tambien este estos estas ese esa paciente dolor refiere niega acude "
               "evolucion dias anos ano consulta fecha motivo exploracion diagnostico tratamiento hombro espalda derecho derecha "
               "izquierdo izquierda cuello cabeza rodilla terapia fisica sesion sesiones saldo cuenta estado antecedentes semanas semana "
               "mes meses presenta signos vitales cita atropello choque fractura medicamento receta dosis horas vez "
               "le lo les nos mi tiene tuvo recomienda indica solicita solicitada ingreso formulario firma accidentes anteriores "
               # clinical one-liners and abbreviations
               "rm resonancia magnetica radiografia ecografia tomografia columna posible posibles discal estenosis cervicalgia lumbalgia "
               "dorsalgia postraumatica postraumatico espasmo reducido reducida aprox aproximadamente movilidad rango limitacion limitado "
               "molestia hormigueo entumecimiento mareo cefalea nauseas esguince luxacion desgarro cicatriz fisioterapia "
               "hallazgos evaluacion alta ingresa niegan negativo negativa sospecha sospechoso impresion concluyente reposo cuadro "
               # qualifier cue words that mark clinical Spanish
               "aqueja alega quiza quizas impresiona jamas carece libre nada ni tal senala expresa eventual sugestivo sugiere puede podria "
               "probablemente actualmente refirio manifiesta relata dolores "
               # D-048: more Spanish function words and clinical words, accented or not
               "no donde cuando mientras durante hacia segun tras ante bajo otro otra otros otras todo toda todos todas cada solo "
               "sido sera seran habia hubo cual cuales quien porque aun ya mejor peor tras asi "
               "escoliosis artrosis facetaria trapecio neumonia reduccion cerrada velocidad cirugia programada vertebral lumbares cervicales "
               "incierto incierta dudoso dudosa presunto presunta presuntamente indeterminado indeterminada califico califica aproximado "
               "aproximada aproximados aproximadas decir rotura oseo radicular derrame "
               "conocimiento perdida mecanica exista existe haya hayan traumatica traumatico tobillo muneca codo cadera pierna brazo pie mano pecho pelvis hombros rodillas "
               "medico medica medicos exploracion caida escalera golpe golpeo cayo cayeron choco impacto ambulancia urgencias urgencia radiologia"),
    "fr": _set("le la les des du de est dans avec sans qui pas une aux cette sont ete etre tres ont elle il ils patiente douleur douleurs "
               "depuis apres avant pour sur par que ne mais ou donc aussi plus ces mon son sa ses leur vous nous je tu et au "
               "cervicale lombaire epaule droite droit gauche genou dos tete cou jours jour semaines mois trois deux perte conscience "
               "connaissance plaint plainte plaintes traitement radiographie irm ordonnance suivi nie aucun aucune jamais "
               "avait etait resultats ni "
               # D-048
               "patient fracture suspectee consultation controle examen chute accident blessure entorse hematome oedeme ordonnance "
               "quatre cinq mise placee prescrit prescrite apparition anterieur anterieure sortie hospitalisation urgences"),
    "de": _set("der die das und ist nicht mit von zu den dem ein eine auf fur im bei nach auch sich schmerzen patient patientin seit wurde "
               "wurden sind wird oder ohne aber noch nur wie dass am zum zur einer einem einen des nacken schulter rechts links knie ruecken "
               "kein keine verlust bewusstsein tagen wochen "
               # D-048
               "in kontrolle rezept operation geplant vier drei zwei fuenf sechs tage woche monate untersuchung behandlung verletzung bruch "
               "roentgen aufnahme entlassung sturz unfall krankenhaus befund arzt aerztin vorstellung beschwerden bestehen besteht"),
    "pt": _set("o os as um uma de do da dos das no na nos nas em com para sem seu sua foi sao nao tambem mais muito paciente dor refere nega "
               "anos dias semana semanas ate tem ha ao aos pelo pela pelos pelas apos desde sobre entre perda consciencia fisioterapia "
               "ombro direito direita esquerdo esquerda joelho coluna ressonancia queixa relata dores tinha nega "
               # D-048
               "receita agendada agendado cirurgia fratura exame consulta queda acidente lesao entorse inchaco dois tres quatro "
               "cinco seis duas vezes encaminhado suspeita suspeito suspeitas compressao sinais encaminhada internado internada alta retorno semanais medico medica exames pedido solicitado"),
    "it": _set("il lo gli le un uno una di del della dei delle e non con per su da che sono ha hanno paziente dolore nel nella dal dalla "
               "anche piu molto senza questo questa questi queste lei lui spalla destra sinistra ginocchio schiena collo giorni settimane "
               "perdita coscienza "
               # D-048
               "nessun nessuna nessuno possibile frattura dello alla allo agli alle ricetta intervento programmato programmata scafoide "
               "controllo visita esame radiografia risonanza magnetica caduta incidente distorsione contusione tre quattro cinque "
               "sei dimesso dimessa ricovero ospedale pronto soccorso terapia prescritta prescritto sospetta sospetto referto"),
}
# Romance stems and words that are clearly not English but belong to Spanish, Portuguese and Italian (and sometimes French) alike.
# They count as non-English evidence (so the line is never confidently English) but never as evidence FOR Spanish by themselves.
_ROMANCE = _set("hernia ibuprofeno naproxeno tac contractura vertigo leve programado cerrado cerrada abierta abierto basal neumonia "
                "lesiones luxacion artrosi scoliosi contrattura trapezio trapecio osteoartrosis ligamento "
                "tendinopatia radiculopatia radiculitis neuralgia cefalea migrana mialgia fibromialgia analgesico antiinflamatorio "
                "miorrelajante infiltracion bloqueo cirurgia cirugia ortopedista ortopedico traumatologia traumatologo fisioterapeuta "
                "menisco quiropractico quiropraxia vendaje inmovilizacion yeso ferula collarin muletas")
_ALL = {c: s for c, s in _STOP.items()}
_UNIQUE = {c: frozenset(w for w in s if not any(w in o for k, o in _ALL.items() if k != c)) for c, s in _ALL.items()}
_FOREIGN = ("es", "fr", "de", "pt", "it")
_FOREIGN_WORDS = frozenset().union(*(_STOP[c] for c in _FOREIGN))
_BONUS = {"es": re.compile(r"[ñ¿¡]"), "pt": re.compile(r"[ãõ]"), "de": re.compile(r"[ßäö]"), "fr": re.compile(r"[èêâîôûœëïç]"),
          "it": re.compile(r"[ìò]")}
_MARKS = re.compile(r"[áéíóúàèìòùâêîôûäöüëïçãõñœß¿¡]", re.IGNORECASE)      # a letter or mark outside the English alphabet
# word endings (on folded words of 6+ letters) that mark one language and are not English
_MORPH = {"it": re.compile(r"(ione|ioni)$"), "de": re.compile(r"(ung|ungen|keit|heit|lich|isch|ische|ischen|schen)$"),
          "pt": re.compile(r"(cao|coes)$"), "es": re.compile(r"(ciones|dad|dades)$"), "fr": re.compile(r"(eux|euse|euses)$")}
# Words a record may use without any English function word and still be English (abbreviations, drug names, cognates shared with English).
_ENGLISH_OK = frozenset(_STOP["en"]) | _set("normal cervical lumbar thoracic sacral vertigo hernia ibuprofen naproxen cyclobenzaprine tramadol "
                                            "acetaminophen meloxicam gabapentin methocarbamol prednisone hydrocodone oxycodone lidocaine "
                                            "tylenol motrin flexeril xray ray scan stable unremarkable intact mild bilateral control lesion contusion protrusion compresion "
                                            "compression hospital edema meniscal radicular performed injection overweight rotator cuff "
                                            "chiropractic orthopedic neurology radiology hypertension corticosteroid neurologically")

# D-050 / T-085 r3 major 2: words that sit in a foreign list (or the Romance stems) but are ordinary English words or English clinical cognates
# ("the patient's son", "the operation", "pain plus numbness", "walking solo", "eventual follow-up", "hernia", "vertebral", "radicular").
# They are not evidence of a foreign language on their own: when nothing else is foreign and English clearly leads, the line is English.
# Deliberately short and conservative; words that are mainly Spanish/Portuguese (dolor, paciente, sin) are never here.
_EN_COLLISIONS = _set("son operation plus solo eventual hernia vertebral radicular basal discal vertigo neuralgia radiculitis par")
EN_DOMINANT = 3.0            # English-only words needed to call a line English when its only foreign evidence is a collision word

# Scripts that are not Latin: a record mostly in one of these is unsupported whatever the stop words say.
_SCRIPTS = (("Chinese", 0x4E00, 0x9FFF), ("Japanese", 0x3040, 0x30FF), ("Korean", 0xAC00, 0xD7AF), ("Cyrillic", 0x0400, 0x04FF),
            ("Arabic", 0x0600, 0x06FF), ("Hebrew", 0x0590, 0x05FF), ("Devanagari", 0x0900, 0x097F), ("Thai", 0x0E00, 0x0E7F),
            ("Greek", 0x0370, 0x03FF))


def _script_of(ch: str):
    o = ord(ch)
    for name, lo, hi in _SCRIPTS:
        if lo <= o <= hi:
            return name
    return None


def _result(lang, **kw):
    return {"lang": lang, "name": None, "code": None, "mixed": False, "words": 0, "scores": {}, "reason": "", **kw}


def detect(text: str) -> dict:
    """{'lang': 'en'|'es'|'other'|'uncertain'|'unknown', 'name': str|None, 'code': ISO code of an unsupported language or None,
    'mixed': bool, 'words': int, 'scores': {code: float}, 'reason': str}. Pure function of the text. Fails safe (D-048)."""
    text = text or ""
    letters = [c for c in text if c.isalpha()]
    out = _result("unknown")
    if not letters:
        return out
    counts = {}
    for c in letters:
        s = _script_of(c)
        if s:
            counts[s] = counts.get(s, 0) + 1
    if counts:
        name, n = max(counts.items(), key=lambda kv: kv[1])
        if n / len(letters) >= 0.3:
            return _result("other", name=name, words=len(letters), reason=f"{name} script")
    words = [_fold(w) for w in _WORD.findall(re.sub(r"\bnon-(?=[a-z])", "", text, flags=re.IGNORECASE))]   # "non-weight-bearing" is English
    out["words"] = len(words)
    low = text.lower()
    n = max(len(words), 1)
    hits = {}                                     # evidence per language: a word only one list owns counts 1, a shared word 0.5
    for code, stop in _STOP.items():
        h = sum(1.0 if w in _UNIQUE[code] else 0.5 for w in words if w in stop and (len(w) >= 2 or w in ("y", "a")))
        h += len(_BONUS[code].findall(low)) if code in _BONUS else 0
        h += sum(0.75 for w in words if len(w) >= 6 and code in _MORPH and _MORPH[code].search(w))
        hits[code] = h
    out["scores"] = {c: round(h / n, 4) for c, h in hits.items()}
    e, s = hits["en"], hits["es"]
    f_code = max(("fr", "de", "pt", "it"), key=lambda c: hits[c])
    f = hits[f_code]
    # evidence that is NOT shared with English: a foreign list word English does not own, a mark, an ending, a Romance stem
    marks = len(_MARKS.findall(low))
    foreign_only = sum(1.0 for w in words if (w in _FOREIGN_WORDS or w in _ROMANCE) and w not in _STOP["en"] and len(w) >= 2)
    foreign_only += marks + sum(0.75 for w in words if len(w) >= 6 and any(rx.search(w) for rx in _MORPH.values()))
    english_only = sum(1.0 if w not in _FOREIGN_WORDS else 0.5 for w in words if w in _STOP["en"])
    foreign_core = marks + sum(1.0 for w in words if (w in _FOREIGN_WORDS or w in _ROMANCE) and w not in _STOP["en"] and w not in _EN_COLLISIONS and len(w) >= 2) \
        + sum(0.75 for w in words if len(w) >= 6 and w not in _EN_COLLISIONS and any(rx.search(w) for rx in _MORPH.values()))

    def uncertain(why):
        return {**out, "lang": "uncertain", "name": NAMES["uncertain"], "reason": why}

    if foreign_only > 0 and foreign_core == 0 and english_only >= EN_DOMINANT:      # only English look-alikes and clearly English wording
        out["lang"] = "en"
        return out
    if foreign_only == 0:                         # nothing says non-English
        if english_only >= EN_CONFIDENT:
            out["lang"] = "en"
            return out
        unknown_words = [w for w in words if len(w) >= 4 and w not in _ENGLISH_OK]
        if unknown_words:                         # no English words and words the English lists do not know: not confidently English
            return uncertain("no recognisable English wording on a line with words the English lists do not know: " + ", ".join(unknown_words[:3]))
        return out
    # some non-English evidence is present
    rest = max(s, e, *(hits[c] for c in ("fr", "de", "pt", "it") if c != f_code))
    if f >= 2 and f >= FOREIGN_MARGIN * rest and f > s:
        return {**out, "lang": "other", "name": NAMES[f_code], "code": f_code, "reason": f"{NAMES[f_code]} wording"}
    content = [w for w in words if len(w) >= 4]
    explained = sum(1 for w in content if w in _STOP["es"] or w in _ROMANCE or w in _ENGLISH_OK)
    share = (explained / len(content)) if content else 1.0
    if s >= 1.0 and s >= ES_VS_UNSUPPORTED * f and share >= (ES_SHARE_SHORT if len(content) <= 6 else ES_SHARE_LONG):
        out["lang"] = "es"
        out["mixed"] = english_only >= EN_CONFIDENT
        return out
    if f > 0 and s > 0:
        return uncertain(f"could be Spanish or {NAMES[f_code]}")
    if f > 0:
        return uncertain(f"could be {NAMES[f_code]} or another language")
    return uncertain("non-English wording or letters, but too little to tell which language")


def record_body(rec: dict) -> str:
    """The text the record's language is judged on: the excerpt (the record's own words), never the Date/Source header lines."""
    return rec.get("excerpt") or ""


def record_lang(rec: dict) -> str:
    """'en' | 'es' | 'other' | 'uncertain' for a record dict. Uses the value ingest/pipeline already set, else detects.
    Text with no evidence for any language (numbers, codes) counts as English; anything with some foreign evidence never does."""
    got = rec.get("lang")
    if got in ("en", "es", "other", "uncertain"):
        return got
    d = detect(record_body(rec))
    return "en" if d["lang"] == "unknown" else d["lang"]


def is_translated(lang: str) -> bool:
    """True when the record goes through the translation path (Spanish prompt, Spanish token checks, translation judge, label):
    Spanish, and a record whose language is uncertain. The English token checks never run for either."""
    return lang in ("es", "uncertain")


def translated_record(rec) -> bool:
    """D-050: True when an item made from this record (dict) must carry AI_TRANSLATION and can never be `verified`."""
    return bool(rec) and is_translated(record_lang(rec))


def annotate(records: list) -> list:
    """Set r['lang'] ('en'|'es'|'other'|'uncertain'), r['lang_name'] (display name, None for en/es), r['lang_reason'] (uncertain only)
    and r['lang_mixed'] on every record. Returns the list."""
    for r in records:
        d = detect(record_body(r))
        r["lang"] = "en" if d["lang"] == "unknown" else d["lang"]
        r["lang_name"] = d["name"] if d["lang"] == "other" else None
        r["lang_reason"] = d["reason"] if d["lang"] == "uncertain" else ""
        r["lang_mixed"] = bool(d["mixed"])
    return records


class UnsupportedLanguage(ValueError):
    """Raised by the pipeline's ingest when no record of the case is in a supported language. Subclasses ValueError, not IngestError,
    so callers that only know IngestError do not mislabel it; `code` is the API error code."""
    code = "unsupported_language"

    def __init__(self, names):
        self.names = sorted({n for n in names if n})
        super().__init__("unsupported_language")


def case_check(records: list) -> None:
    """Refuse a case whose recognisable records are all unsupported. A record that is merely unknown or short does not rescue a case
    (a case of numbers and codes is English by default), but at least one supported record must have been recognised or be unknown."""
    langs = [r.get("lang") or record_lang(r) for r in records]
    if langs and all(lg == "other" for lg in langs):
        raise UnsupportedLanguage(r.get("lang_name") for r in records)


MESSAGE = ("This tool reads English and Spanish records. The text looks like {names}, which is not supported, so nothing was run. "
           "Paste records in English or Spanish.")


def api_fields(exc) -> tuple:
    """(message, detail) for the API error of an UnsupportedLanguage; ('', {}) for anything else."""
    if not isinstance(exc, UnsupportedLanguage):
        return "", {}
    names = ", ".join(exc.names) or "another language"
    return MESSAGE.format(names=names), {"languages": exc.names, "supported": [NAMES[c] for c in SUPPORTED]}


def record_warnings(records: list, prep: bool = False) -> list:
    """Pipeline warnings (api.md `warnings`) for records in an unsupported language (skipped), of uncertain language (needs review) and Spanish records (translated)."""
    out = []
    for r in records:
        lg = r.get("lang")
        if lg == "other":
            out.append({"code": "UNSUPPORTED_LANGUAGE", "record_no": r["n"], "item_id": r["id"],
                        "message": f"Record {r['n']} looks like {r.get('lang_name') or 'another language'}, which is not supported; "
                                   "it was not summarised and is left out of the timeline. Read it yourself."})
    for r in records:
        if r.get("lang") == "uncertain":
            out.append({"code": "LANGUAGE_UNCERTAIN", "record_no": r["n"], "item_id": r["id"],
                        "message": f"Record {r['n']}: the language could not be identified with confidence ({r.get('lang_reason') or 'too little text'}). "
                                   "It is read as a translation, is never marked verified, and needs your review against the original."})
    es = [r for r in records if r.get("lang") == "es"]
    if es:
        out.append({"code": "SPANISH_RECORDS", "record_nos": [r["n"] for r in es], "record_no": es[0]["n"], "item_id": es[0]["id"],
                    "message": f"Spanish records: the quote is always the original Spanish; the summary is {'a prepared' if prep else 'an AI'} translation and is labelled. "
                               "The phrase lists for pre-existing conditions and causation wording are English only, so for Spanish records "
                               f"those flags come from the {'prepared answers' if prep else 'AI check'} alone. Read the Spanish quote yourself."})
    return out


def block_lang(block: str) -> str:
    """'en' | 'es' | 'other' for the raw text of one stored record block (what the API record view has)."""
    from app.backend import ingest
    try:
        body = ingest.split_records(block)[0]["excerpt"]
    except Exception:
        body = block
    return record_lang({"excerpt": body})
