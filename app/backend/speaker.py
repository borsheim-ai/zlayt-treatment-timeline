"""Speaker attribution v2 (T-091, D-040 / D-042): who is the speaker of an excerpt? Deterministic, local, no model, no network.

STATUS: DISABLED. D-040 stays in force; nothing in the UI, flags or export imports this module. `ENABLED` is the
switch and it is False. See the T-091 handoff for the score on evals/adversarial/speaker_attribution.jsonl.

Contract
    attribute(text) -> Attribution(label, speakers, reasons)
    label is one of:
      "patient"  every statement in the excerpt is attributed to the patient by an explicit head ("Patient states ...",
                 "Pt c/o ...", "Per patient, ...", "paciente refiere ..."), and nothing else appears in it.
      "other"    every statement is attributed to a named non-patient source (EMS, wife, witness, nurse, ...), and no
                 patient statement is nested inside (that would be hearsay of a patient statement: "unknown").
      "unknown"  anything else: mixed speakers, no speaker, pronoun-only speaker ("He states"), bare "C/O", titles or
                 names, uppercase "PT" (physical therapy or patient), a word the grammar does not know.
    A wrong "patient" is a credibility error; "unknown" is always safe. Every rule below therefore fails toward unknown.

Mechanism (no dependency parser: spaCy is not installed in .venv and its model cannot be fetched offline, and a
statistical parse would be the wrong tool for a fail-closed gate anyway)
    1. Normalise (NFKC, strip invisible format chars, fold quotes, lowercase; uppercase "PT" is kept as ambiguous).
    2. Split into sentences, then into clause segments at punctuation and at a CLOSED set of connector words.
    3. A segment is a HEAD only if it starts with a recognised speaker + speech verb ("wife reports"), a "per X" /
       "according to X" phrase, or a "X:" label for a listed non-patient source. Everything else is a continuation.
    4. A continuation (or a head's complement) may contain only words from a CLOSED vocabulary (symptom, body, time,
       function words). An unknown word, a second speaker, a speech verb or a pronoun head all fall outside it, so the
       result is unknown. There is no deny-list of speakers or verbs on the patient path: that is what let four review
       rounds find another hole. Words are added to the vocabulary, never to a block list.
    5. The one allowed embedding is hearsay inside a patient statement in the past tense, directly after the verb:
       "Patient states EMS noted a laceration." / "... his wife drove him to the ER." The patient is still the speaker.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

ENABLED = False   # D-040: the chip stays off. Flip only after the adversarial gate is 100% AND T-091 wiring is reviewed.

LABELS = ("patient", "other", "unknown")


@dataclass(frozen=True)
class Attribution:
    label: str
    speakers: tuple = ()
    reasons: tuple = field(default_factory=tuple)


def chip_label(text: str):
    """What the UI would ask for. None while ENABLED is False (D-040) and for every non-patient result."""
    if not ENABLED:
        return None
    return "patient" if attribute(text).label == "patient" else None


# --------------------------------------------------------------------------------------------------- vocabulary

def _w(s: str) -> frozenset:
    return frozenset(s.split())


_PATIENT_SUBJ = _w("patient pt paciente paciente")
_DET = _w("the this his her their its a an patient's pt's paciente's el la los las su sus")
_MOD = _w("triage charge er ed emergency ambulance ems scene responding on-scene police treating referring attending resident "
          "nursing ward floor other family insurance claims adjuster rn lpn")

# non-patient sources (English + Spanish). 'pt' is deliberately absent; 'pt' is a patient subject.
_SRC = _w("""ems emt emts paramedic paramedics medic medics ambulance crew wife husband spouse mother father mom dad parent parents
son daughter sister brother grandmother grandfather aunt uncle cousin girlfriend boyfriend fiance fiancee partner friend
family relative relatives caregiver neighbor neighbour coworker co-worker colleague boss employer supervisor witness
witnesses passenger driver bystander officer police trooper deputy adjuster attorney lawyer nurse rn lpn cna triage
doctor physician md provider pa np therapist chiropractor technician tech radiologist clerk receptionist
esposa esposo marido madre padre hermano hermana hijo hija familiar testigo paramedico paramédico paramédicos paramedicos
enfermera enfermero médico medico doctora policía policia oficial pasajero conductor amigo amiga novia novio""")

# speech / documentation verbs. Used ONLY to recognise a head ("<speaker> <verb>"); never as a deny-list.
_SAY = _w("""states stated state reports reported report says said say tells told tell notes noted note denies denied deny
complains complained complain c_o endorses endorsed describes described relates related indicates indicated admits admitted
acknowledges acknowledged claims claimed believes believed thinks thought recalls recalled remembers remembered rates rated
mentions mentioned expresses expressed voices voiced volunteers volunteered reiterates confirms confirmed advises advised
informs informed relays relayed attributes attributed links linked associates associated blames blamed alleges alleged
contends maintains insists asserts declares answers responds agrees observed observes found saw documented documents
recorded records witnessed heard suspects feels felt gives gave
refiere refirió refirio dice dijo manifiesta manifestó manifesto indica indicó indico niega negó nego reporta reportó reporto
informa informó informo relata relató relato menciona mencionó menciono afirma afirmó afirmo señala señaló expresa declara
declaró comenta comentó describe describió acusa""")
_SAY_PATIENT = _SAY - _w("observed observes found saw witnessed heard suspects feels felt gives gave")

_EMBED_VERB = _w("noted said told stated reported documented drove took brought found saw called helped gave transported "
                 "picked arrived asked advised")

# connector words that open a new segment (dropped). 'per' / 'according to' / 'segun' are kept as the segment's first word.
_SPLIT = _w("and but while whereas although though however plus as then so because y e pero mientras sino pues or o")
_KEEP_SPLIT = _w("per según segun")

_SECTION = frozenset({"s", "subjective", "hpi", "history of present illness", "cc", "chief complaint", "hx", "history",
                      "interval history", "subjective complaints", "complaints", "complaint", "comment", "comments", "note",
                      "notes", "narrative", "reason for visit", "motivo de consulta", "subjetivo", "historia"})
_PREFIX = _w("at on during today the visit intake exam appointment follow up followup initial evaluation consult consultation "
             "office hoy en la el consulta cita")

_COMMON = """
a an the of in on at to for from with without into onto over under up down out off through during after before since until till
about around across near between within against along both each all any some no not none never nor neither only just still very
quite more most less much many few little too even already again ever once twice than like such same another is are was were be
been being am do does did done has have had having can could would should might must it its this that these those there
here when where how what if which he she him her his hers they them their theirs we us our i me my mine you your
at all so as well
"""

_BODY = """
neck back head shoulder shoulders arm arms elbow elbows wrist wrists hand hands finger fingers thumb hip hips leg legs knee knees
ankle ankles foot feet toe toes chest rib ribs abdomen abdominal stomach belly groin jaw face eye eyes ear ears nose mouth teeth
tooth spine cervical thoracic lumbar sacral coccyx tailbone skull scalp forehead temple temples throat trapezius upper lower mid
left right l r lt rt bilateral bilaterally bilat side sides front rear base area areas joint joints muscle muscles
"""

_SYMPTOM = """
pain pains ache aches aching soreness sore stiffness stiff tenderness tender numbness numb tingling weakness weak swelling swollen
bruising bruise bruised spasm spasms headache headaches migraine migraines dizziness dizzy lightheaded nausea nauseous vomiting
fatigue tired anxiety anxious depression insomnia fever chills cough rash laceration cut cuts abrasion abrasions contusion fracture
sprain strain strained bleeding discomfort burning pressure cramping cramps limp limping radiating radiates radiated radiculopathy
sharp dull constant constantly intermittent intermittently mild moderate severe worse worsen worsens worsened worsening better
improved improving improves resolved resolving persistent persists persisted continues continued continue shooting stabbing
throbbing occasional occasionally frequent frequently daily nightly worst unbearable intense terrible bad good fine ok okay normal
normally unable able difficulty trouble hard easy limited limitation restriction restricted flare flares flared
loss consciousness conscious unconscious lost blackout blacked passed alert awake oriented ambulatory stable confused confusion
irritable irritability moody mood sleep sleeping slept sleeps rest resting memory concentrating concentration vision blurry blurred
ringing hearing balance gait walking walk walked walks standing stand stood sitting sit sat bending bend lifting lift lifted
reaching carrying driving drive driven working work worked running climbing stairs prolonged long short
hurts hurt hurting felt feel feels feeling seems seemed began begin begins start started starts onset woke wake waking happened
occurred occur occurs went go going came come taking take taken took got get getting gets became become becoming hit struck
rear-ended rearended slammed jolted jerked thrown twisted fell fall fallen slipped slip trip tripped
"""

_EVENT = """
accident accidents collision crash crashed vehicle car truck motorcycle bike bicycle pedestrian airbag airbags seatbelt seat belt
belts impact windshield steering wheel dashboard door light lights intersection road highway street lot parking fall slip work job
home house stairs steps ladder ground floor ice wet scene incident injury injuries injured event er ed emergency room hospital clinic
office urgent care sleep night
"""

_TREAT = """
ibuprofen tylenol acetaminophen naproxen medication medications meds pills pill relief relieves helps helped ice heat rest therapy
treatment physical chiropractic massage injection injections surgery surgeries
"""

_TIME = """
today yesterday tonight now currently ago last first second third prior previous following later early late lately recently
morning evening afternoon night nights day days week weeks month months year years hour hours minute minutes moment time times
one two three four five six seven eight nine ten zero half several couple
"""

_SPANISH = """
dolor dolores cuello cabeza espalda hombro hombros brazo brazos mano manos pierna piernas rodilla rodillas pie pies tobillo pecho
cadera desde el la los las un una de del en con sin por a al que se me mi mis su sus es está esta estoy tiene tengo hace días dias
semana semanas mes meses año años hoy ayer anoche noche mañana tarde accidente choque colisión colision golpe golpeó golpeo
después despues antes durante cuando constante intermitente leve moderado moderada severo severa fuerte intenso intensa mareo
mareos náusea nausea náuseas nauseas vómito vomito fiebre hormigueo entumecimiento debilidad inflamación inflamacion hinchazón
hinchazon rigidez molestia molestias lesión lesion caída caida cayó cayo no nada ninguno más mas menos muy todo todos todo
lumbar cervical lado izquierdo derecho izquierda derecha ambos ambas """

_EXTRA = """
also ran run runs limps sleeps poorly low deployed steady gait damage minimal distress intake stop stopped red green traffic whiplash
fault slowly suddenly sudden behind ahead speed speeding mph hit-and-run turn turning merging merged
prior surgeries arthroscopy fusion discectomy laminectomy replacement problem problems symptom symptoms caused cause causes due
missing missed duty closed clinic appointment could earlier violent brief thrown against struck by cannot cant couldn't didn't
wasn't hadn't haven't isn't doesn't don't won't wouldn't another state
pérdida perdida conciencia comenzó comenzo empezó empezo duerme mal vehículo vehiculo detuvo dolía dolia ha
"""
_BASE = _w(_COMMON + _BODY + _SYMPTOM + _EVENT + _TREAT + _TIME + _SPANISH + _EXTRA)
_NUMERIC = re.compile(r"^[\d#:.,%+~<>=-]*\d[\d#:.,%+~<>=a-z-]*$")   # 7#10, 2026, 3d, 10mg ('/' between digits is folded to '#')

# What a continuation / complement may contain, by current speaker.
_VOCAB_PATIENT = _BASE
_VOCAB_OTHER = _BASE | _w("patient pt paciente")

# --------------------------------------------------------------------------------------------------- normalise

_ABBR = re.compile(r"\b(pt|dr|mr|mrs|ms|sr|sra|st|vs|approx|no|hx|dx|rx|tx|w|c|s|e\.g|i\.e)\.", re.IGNORECASE)


def _normalise(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "")
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Cf")           # zero-width and bidi controls
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("«", '"'), ("»", '"')):
        t = t.replace(a, b)
    # uppercase PT is physical therapy or patient: mark it so it can never become a patient subject
    t = re.sub(r"\bPT\b\.?", " pt_ambiguous ", t)
    t = t.lower()
    t = re.sub(r"\b(patient|pt)[- ]reported\b(?!\s+(?:by|that|he|she|his|her)\b)", r"\1 reports", t)   # "Patient-reported neck pain"
    t = re.sub(r"\bc\s*/\s*o\b", "c_o", t)
    t = re.sub(r"\bs\s*/\s*p\b", "s_p", t)
    t = re.sub(r"\bw\s*/\s*o\b", "w_o", t)
    t = re.sub(r"\bw\s*/", "w_ ", t)
    t = re.sub(r"(?<=\d)\s*/\s*(?=\d)", "#", t)
    t = re.sub(r"(?<=\d)\.(?=\d)", "#", t)                                   # 7.5
    t = _ABBR.sub(lambda m: m.group(1), t)                                   # pt. -> pt, mrs. -> mrs
    t = re.sub(r"(?:as\s+)?(?:reported|stated|described|relayed|noted|documented|per)\s+by\s+", " per ", t)
    t = re.sub(r"\b(?:as\s+per|according\s+to|de\s+acuerdo\s+con)\b", " per ", t)
    t = re.sub(r"\bpor\s+(?=(?:el|la)?\s*(?:paciente|esposa|esposo)\b)", " según ", t)
    # appositive name or title right after a source noun: "wife (mrs. ortiz) reports"
    t = re.sub(r"(\b(?:" + "|".join(sorted(_SRC, key=len, reverse=True)) + r")\b)\s*\(\s*(?:mrs?|ms|miss|mr|dr|sra?|señora?)\.?\s+[a-záéíóúñ]+\s*\)", r"\1", t)
    t = re.sub(r"(?m)^\s*(?:[-*•·]|\d+[.)])\s+", "", t)                      # bullets and numbering
    return t


# ------------------------------------------------------------------------------------------------------ segmenting

def _tokens(s: str) -> list:
    return re.findall(r"[\w'#]+(?:-[\w'#]+)*", s, re.UNICODE)


def _sentences(t: str) -> list:
    out = []
    for block in re.split(r"(?<=[.!?])\s+|[.!?]+$|\n{2,}", t):
        if block and block.strip():
            out.append(block.strip(" .!?"))
    return out


_PUNCT_SPLIT = re.compile(r"\s*([,;:—–()\[\]\"/&]|\s-\s|\n)\s*")


def _split_segments(sentence: str) -> list:
    """-> list of (token_list, sep_after). Connector words open a new segment; 'per' keeps its place as first word."""
    parts = _PUNCT_SPLIT.split(sentence)
    raw = []   # (text, sep_after)
    for i in range(0, len(parts), 2):
        txt = parts[i]
        sep = parts[i + 1].strip() if i + 1 < len(parts) and parts[i + 1] is not None else ""
        raw.append((txt, sep or ("\n" if "\n" in (parts[i + 1] if i + 1 < len(parts) else "") else "")))
    segs = []
    for txt, sep in raw:
        toks = _tokens(txt)
        cur = []
        out = []
        for tok in toks:
            if tok in _SPLIT or tok in _KEEP_SPLIT:
                if cur:
                    out.append((cur, ""))
                cur = [] if tok in _SPLIT else [tok]
            else:
                cur.append(tok)
        if cur:
            out.append((cur, ""))
        if out:
            out[-1] = (out[-1][0], sep)
            segs.extend(out)
        elif segs and sep:
            segs[-1] = (segs[-1][0], segs[-1][1] or sep)
    return [(t, s) for t, s in segs if t]


# --------------------------------------------------------------------------------------------------- head detection

def _skip_det(toks, i):
    while i < len(toks) and toks[i] in _DET:
        i += 1
    return i


def _src_phrase(toks, i):
    """Return index after a source phrase starting at i (modifiers + a source noun), or None."""
    j = i
    while j < len(toks) and toks[j] in _MOD and toks[j] not in _SRC:
        j += 1
    if j < len(toks) and toks[j] in _SRC:
        j += 1
        # "family member", "ambulance crew", "ems crew", "triage nurse"
        while j < len(toks) and toks[j] in _SRC | _w("member members"):
            j += 1
        return j
    return None


def _patient_phrase(toks, i):
    j = _skip_det(toks, i)
    if j < len(toks) and toks[j] in _PATIENT_SUBJ:
        return j + 1
    return None


def _head(toks, sep):
    """Classify one segment. -> (speaker, complement_tokens, kind) or None.
    speaker: 'patient' | 'other'; kind: 'verb' | 'per' | 'label'."""
    if not toks:
        return None
    # per / segun
    if toks[0] in _KEEP_SPLIT:
        j = _patient_phrase(toks, 1)
        if j is not None:
            return "patient", toks[j:], "per"
        j = _src_phrase(toks, _skip_det(toks, 1))
        if j is not None:
            return "other", toks[j:], "per"
        return None
    # patient + verb
    j = _patient_phrase(toks, 0)
    if j is not None:
        k = j
        if k < len(toks) and toks[k] in _w("also now currently further today then again"):
            k += 1
        if k < len(toks) and toks[k] in _SAY_PATIENT:
            k += 1
            if k < len(toks) and toks[k] == "of" and toks[k - 1] in _w("complains complained complain"):
                k += 1
            return "patient", toks[k:], "verb"
        return None
    # source + verb, or source label
    j = _src_phrase(toks, _skip_det(toks, 0))
    if j is not None:
        if j < len(toks) and toks[j] in _SAY:
            k = j + 1
            if k < len(toks) and toks[k] == "of" and toks[k - 1] in _w("complains complained complain"):
                k += 1
            return "other", toks[k:], "verb"
        if j == len(toks) and sep in (":", "—", "–", "-"):
            return "other", [], "label"
    return None


def _complement_ok(comp, speaker, allow_embed):
    """comp must be inside the closed vocabulary; a leading hearsay embedding is allowed after a patient verb."""
    vocab = _VOCAB_PATIENT if speaker == "patient" else _VOCAB_OTHER
    toks = list(comp)
    if allow_embed and toks:
        i = 1 if toks[0] == "that" else 0
        i = _skip_det(toks, i) if toks[i:i + 1] and toks[i] in _DET else i
        j = _src_phrase(toks, i)
        if j is not None and j < len(toks) and toks[j] in _EMBED_VERB:
            toks = toks[j + 1:]
    for t in toks:
        if t in vocab or _NUMERIC.match(t):
            continue
        return False
    return True


# ------------------------------------------------------------------------------------------------------- sentence

def _classify_sentence(sentence: str):
    segs = _split_segments(sentence)
    if segs and len(segs[0][0]) > 1 and _NUMERIC.match(segs[0][0][0]):      # "2026-04-05 Patient reports ..."
        segs[0] = (segs[0][0][1:], segs[0][1])
    reasons = []
    speakers = set()
    # drop section labels and lead-in phrases before the first head
    cleaned = []
    seen_head = False
    for toks, sep in segs:
        if not seen_head:
            joined = " ".join(toks)
            if joined in _SECTION or (all(t in _PREFIX or _NUMERIC.match(t) for t in toks)):
                continue
        if _head(toks, sep) is not None:
            seen_head = True
        cleaned.append((toks, sep))
    cur = None
    pre = []        # unattributed lead-in tokens, only valid when a trailing "per X" head claims them
    first_head = True
    for toks, sep in cleaned:
        h = _head(toks, sep)
        if h is None:
            if cur is None:
                pre.append(toks)
                continue
            if not _complement_ok(toks, cur, False):
                return None, speakers, ["unrecognised words or a pronoun/second speaker in: " + " ".join(toks)]
            continue
        speaker, comp, kind = h
        if pre:
            if kind != "per" or any(not _complement_ok(p, speaker, False) for p in pre):
                return None, speakers, ["unattributed text before the first speaker"]
            pre = []
        if not _complement_ok(comp, speaker, allow_embed=(speaker == "patient" and kind == "verb")):
            return None, speakers, ["unrecognised words in the statement: " + " ".join(comp)]
        cur = speaker
        speakers.add(speaker)
        first_head = False
    if pre or not speakers:
        return None, speakers, ["no explicit speaker"]
    return speakers, speakers, reasons


def attribute(text: str) -> Attribution:
    """Label who is speaking in `text`. Deterministic. See the module docstring for the rules."""
    t = _normalise(text)
    # a newline starts a new segment only when the next line begins with a speaker head; otherwise it is a soft wrap
    lines = [ln for ln in t.split("\n")]
    joined = lines[0] if lines else ""
    for prev, nxt in zip(lines, lines[1:]):
        nseg = _split_segments(nxt.strip())
        starts_head = bool(nseg) and _head(nseg[0][0], nseg[0][1]) is not None
        if not prev.strip():
            joined += " "
        elif re.search(r"[.!?]\s*$", prev) or starts_head:
            joined += " ; " if not re.search(r"[.!?]\s*$", prev) else " "
        else:
            joined += " "
        joined += nxt
    sentences = _sentences(joined)
    if not sentences:
        return Attribution("unknown", (), ("empty",))
    allspk = set()
    reasons = []
    for s in sentences:
        spk, seen, why = _classify_sentence(s)
        allspk |= set(seen or ())
        if spk is None:
            return Attribution("unknown", tuple(sorted(allspk)), tuple(why))
        reasons.extend(why)
    if allspk == {"patient"}:
        return Attribution("patient", ("patient",), ())
    if allspk == {"other"}:
        return Attribution("other", ("other",), ())
    return Attribution("unknown", tuple(sorted(allspk)), ("mixed speakers",))
