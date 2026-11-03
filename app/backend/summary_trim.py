"""D-054: code removes the clauses of an AI summary that add salient content its own quote lacks, before the judge sees the summary. CODE ONLY (no LLM, no network).

    trim(summary, excerpt, label="", date_iso="") -> {"text", "removed", "kept", "supported", "notes", "changed"}

Why: the generator sometimes summarizes beyond its own excerpt ('Initial consult; left wrist pain 6/10; splint fitted.' over the pain sentence only).
Judge 1 rightly objects, and a ship bar that depends on the model's luck flaps. Trimming by code is deterministic and keeps 'every statement traces to a quote'.

Rule (T-112 r2: remove only what is demonstrably NEW, never a faithful paraphrase; the judge still checks everything that stays):
 1. Split the summary into clauses at ';' ',' sentence-ending '.' and the join ' and ' (NOT ' with ': 'Neck pain consistent with sprain.' is ONE clause, so a removed object can never strand its head word) (no split inside '1,200', '6.5', 'Dr.', 'approx.', 'e.g.').
 2. A clause is REMOVED only when it carries salient new content, i.e. at least one of these is not in the quote (the record's source label and parsed date also count
    as present, as in grounding.new_tokens):
      a. a number or a month name (D-034; 'six', 'twice', 'x2' in the quote count as 2, 6 ...);   b. a side (left / right / bilateral; 'L', 'lt', 'both' in the quote count);
      c. a negation (no, not, denies ...; any negation-like quote word - normal, unremarkable, unchanged, unable - counts as present);
      d. a procedure, treatment, device or drug term (splint, cast, MRI, injection, surgery, referred, prescribed, ordered, hospitalized, Tylenol ...);
      e. a body part (wrist, neck, lumbar ...);   f. a diagnosis noun (fracture, sprain, concussion, radiculopathy ...).
    a-c count only for a clause that shares no content word with the quote ('for 4 weeks'); a clause on the quote's own topic with a changed value ('Pain 3/10' over
    'Pain 4/10') stays, because the D-034/D-047 code checks flag a number or side the quote lacks and the paralegal sees the conflict. A NEGATION on the quote's own
    topic also stays but is only guaranteed to reach judge 1 and the human: when the quote has the same negation word elsewhere, grounding.new_tokens does not flag it
    ('No cervical strain.' over 'X-ray: no acute fracture. Cervical strain.'). d-f always count.
    A capitalized word inside a clause is a name ('Fennimoor Spine Clinic'), not a body part.
    Clinical abbreviations are spelled out on both sides first (expand_abbreviations: lac, DJD, ESI, BLE, US, IM, C-collar ...), so 'Chin lac.' supports 'Laceration to the chin'.
    Terms (d-f) are matched by word FAMILY (lexicon below): the quote supports a term when it has a word of the same family (Tylenol~acetaminophen, cervical~neck,
    fingers~digits, prescription~prescribed) or of a family that covers it (a bare 'scan' is covered by MRI or CT; 'spine' by neck or back).
 3. A clause with no salient new content STAYS, whatever its other words ('Dizziness reported.' over 'Pt dizzy since crash.'; 'Walks with a cane' over 'Patient ambulating
    with cane'); the judge checks it. Whole clauses only: a kept clause is never edited. What code guarantees (T-128 r2/r3, D-054), with no word list. It does NOT guarantee that the kept text reads as a finished sentence: a clause is never
    edited, a kept ' and ' clause can still be a short phrase, and the judge and the human check the wording:
      (1) trim only a SUFFIX (T-128 r3): the kept text is always a prefix of whole clauses, and a clause is removed only when every clause after it is removed too,
          so no kept clause can follow (and depend on) a removed one ('Shoulder pain; surgery performed; due to torn labrum.' keeps both or drops the tail);
      (2) the FIRST clause is never removed: when it is unsupported nothing is trimmed and the whole summary goes to judge 1 (unless every clause is unsupported: rule 4);
      (3) the kept prefix has at least 2 content words.
    When a rule says no, the summary is returned unchanged. ' with ' is not a clause boundary, so 'diagnosed with diabetes' is one clause: removed whole or kept whole.
 4. If every clause is removed, or the clauses left have no content word at all (stopwords and numbers only), `text` is '' and the caller sends the item to the
    could-not-verify tray (D-053/D-054). A summary with no removal is returned unchanged, byte for byte."""
import re

from app.backend import grounding

NOTE = "removed from the summary: not in the quote: '{}'"

_STOP = frozenset("""
a an the and or but nor of in on at to for from by with without within into onto over under about around per via as is are was were be been being am do does did
has have had having it its this that these those there here then than so such very also too only just not no yes if when while after before during since until
he she they them his her their him we us you your i me my our who whom whose which what where why how can could would should may might will shall must
patient patients pt pts client reports report reported reporting states stated state notes noted note record records documented documents document describes
described describe says said stating denies denied deny negative none never neither absent left right bilateral bilaterally
possible possibly probable probably likely unlikely suspected suspect appears appear appeared apparently approximately approx roughly estimated
one two three four five six seven eight nine ten
now currently today still already again later earlier recently rated rating score scored seen presented presents presenting came
""".split())
_ABBR_BEFORE_PERIOD = frozenset({"dr", "mr", "mrs", "ms", "st", "jr", "sr", "vs", "approx", "e.g", "i.e", "etc", "no", "dept", "inc", "ref", "fig", "cf", "est"})
# Abbreviation and synonym groups: a word in a group is supported by any other word of the group. Deliberately generous (a wrong match only keeps a clause
# the judge then checks; a missed match would remove a faithful clause).
_GROUPS = [
    {"pt", "physical", "therapy", "therapist", "rehab", "rehabilitation"},
    {"hx", "history"}, {"dx", "diagnosis", "diagnosed", "diagnostic", "impression"}, {"tx", "treatment", "treated", "treat", "treating", "therapy"},
    {"rx", "prescription", "prescribed", "medication", "medications", "meds", "med"}, {"sx", "symptom", "symptoms"}, {"fx", "fracture", "fractured"},
    {"ha", "headache", "headaches"}, {"lbp", "low", "back", "pain"}, {"mva", "mvc", "collision", "accident", "crash", "wreck", "vehicle"},
    {"er", "ed", "emergency", "ems", "ambulance"}, {"ortho", "orthopedic", "orthopaedic", "orthopedics", "orthopedist", "orthopedics"},
    {"neuro", "neurology", "neurologic", "neurological", "neurologist"}, {"xray", "radiograph", "radiographs", "radiography", "imaging", "film", "films"},
    {"mri", "imaging", "scan"}, {"ct", "imaging", "scan", "tomography"},
    {"eval", "evaluation", "assessment", "exam", "examination", "examined", "evaluated", "assessed", "consult", "consultation", "consulted"},
    {"rom", "range", "motion"}, {"fu", "follow", "followup", "followed"}, {"sob", "shortness", "breath"}, {"inj", "injection", "injected"},
    {"surg", "surgery", "surgical", "operation", "operative", "procedure"}, {"abd", "abdomen", "abdominal"}, {"cervical", "neck"},
    {"bp", "blood", "pressure"}, {"hr", "heart", "rate"}, {"gp", "pcp", "physician", "doctor", "provider"},
    {"loc", "loss", "consciousness", "unconscious", "syncope", "blackout"}, {"ams", "altered", "mental", "status", "confusion"}, {"cp", "chest"},
    {"htn", "hypertension", "hypertensive"}, {"dm", "diabetes", "diabetic"}, {"prn", "needed", "necessary"}, {"wnl", "normal", "limits", "unremarkable"},
    {"nad", "distress"}, {"ttp", "tender", "tenderness", "palpation"}, {"sp", "status", "post", "after"}, {"cx", "csp", "cervical", "spine"},
    {"lsp", "lumbar", "spine"}, {"esi", "epidural", "steroid", "injection"}, {"rtw", "return", "work"}, {"nsaid", "nsaids", "ibuprofen", "naproxen", "antiinflammatory"},
    {"ambulat", "ambulate", "ambulates", "ambulating", "ambulation", "ambulatory", "walk", "walks", "walked", "walking", "gait"},
    {"anxious", "anxiety", "nervous"}, {"tearful", "crying", "cried", "cry", "tears"}, {"insomnia", "sleep", "sleeping", "sleepless"},
    {"vomit", "vomited", "vomiting", "emesis", "nausea", "nauseated"}, {"paresthesia", "paresthesias", "numbness", "tingling", "numb"},
    {"dizzy", "dizziness", "vertigo", "lightheaded", "lightheadedness"},
    {"dos", "date", "service"}, {"cc", "chief", "complaint"}, {"hpi", "history", "illness"}, {"ucc", "urgent", "care"}, {"snf", "nursing", "facility"},
]
_GROUP_OF = {}
for _g in _GROUPS:
    for _w in _g:
        _GROUP_OF.setdefault(_w, set()).update(_g)

_WORD = re.compile(r"[a-z]+")
_SUFFIXES = ("ations", "ation", "ments", "ment", "ness", "ings", "ing", "ied", "ies", "ed", "es", "s", "ly", "al")
_SPLIT = re.compile(r";|,(?!\d)|(?<!\d),|\s+and\s+|\.(?=\s|$)", re.IGNORECASE)
_STRENGTH = {";": 2, ",": 1, ".": 3}


def _stem(w: str) -> str:
    """Light stemmer: strips common suffixes and folds a final y to i (dizzy~dizziness, anxious~anxiety is in _GROUPS, bruise~bruising by prefix)."""
    for suf in _SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            w = w[:-len(suf)]
            break
    return w[:-1] + "i" if w.endswith("y") and len(w) > 3 else w


# Clinical abbreviations are expanded to the words (and family words) they stand for, in the quote AND in the summary, so 'Chin lac.' supports 'Laceration to the chin'
# and 'Laceration' supports 'lac' alike. Case-sensitive entries are ordinary English words when lower case (US/us, IM/I'm, OA, RA, LE, UE). Inert entries (IV, HEP, EKG) were removed: they changed no trim (T-128 r2)..
_ABBR_CASE = {"US": "ultrasound", "IM": "intramuscular injection", "OA": "osteoarthritis", "RA": "rheumatoid arthritis", "LE": "lower extremity leg",
              "UE": "upper extremity arm"}
_ABBR = {"lac": "laceration", "lacs": "laceration", "djd": "degenerative joint disease", "esi": "epidural steroid injection", "tpi": "trigger point injection",
         "rcr": "rotator cuff repair surgery", "tka": "total knee arthroplasty surgery", "tha": "total hip arthroplasty surgery", "orif": "open reduction internal fixation surgery",
         "acdf": "anterior cervical discectomy fusion surgery neck", "apap": "acetaminophen", "abx": "antibiotic", "cp": "chest pain", "cxr": "chest xray",
         "ble": "bilateral lower extremity leg", "lle": "left lower extremity leg", "rle": "right lower extremity leg",
         "bue": "bilateral upper extremity arm", "lue": "left upper extremity arm", "rue": "right upper extremity arm", "u/s": "ultrasound"}
_ABBR_RX = re.compile(r"(?<![a-z0-9/])(" + "|".join(sorted((re.escape(k) for k in _ABBR), key=len, reverse=True)) + r")(?![a-z0-9/])")
_ABBR_CASE_RX = re.compile(r"(?<![A-Za-z0-9/])(" + "|".join(_ABBR_CASE) + r")(?![A-Za-z0-9/])")


def expand_abbreviations(text: str) -> str:
    """Lower-cases `text` and spells out clinical abbreviations: 'Chin lac.' -> 'chin laceration.', 'C-collar' -> 'cervical collar', 'upper extremity' -> 'upper extremity arm'."""
    t = _ABBR_CASE_RX.sub(lambda m: _ABBR_CASE[m.group(1)], text)
    t = t.lower()
    t = re.sub(r"\bc[- ]?collar\b", "cervical collar", t)
    t = re.sub(r"\blower\s+extremit\w*", "lower extremity leg", t)
    t = re.sub(r"\bupper\s+extremit\w*", "upper extremity arm", t)
    return _ABBR_RX.sub(lambda m: _ABBR[m.group(1)], t)


def _prep(text: str) -> str:
    t = expand_abbreviations(text)
    t = re.sub(r"x-?\s?rays?", "xray", t)
    t = re.sub(r"\bc/o\b", "complains", t)
    t = re.sub(r"\bf/u\b", "fu", t)
    t = re.sub(r"\bs/p\b", "sp", t)
    t = re.sub(r"\bw/o\b", "without", t)
    t = re.sub(r"\bb/l\b", "bilateral", t)
    t = re.sub(r"\bw/(?=\s)", "with ", t)
    t = re.sub(r"\bn/v\b", "nausea vomiting", t)
    t = re.sub(r"\b\w+n't\b", " not ", t)
    t = t.replace("'", "")
    return t


def content_words(text: str) -> list:
    """The content words of `text` (lower case): no stopwords, no one- or two-letter words unless they are known abbreviations."""
    out = []
    for w in _WORD.findall(_prep(text)):
        if w in _STOP or w.endswith("n't"):
            continue
        if len(w) < 3 and w not in _GROUP_OF:
            continue
        out.append(w)
    return out


def _forms(w: str) -> set:
    base = {w} | _GROUP_OF.get(w, set())
    return {_stem(x) for x in base}


def _match(a: str, b: str) -> bool:
    if a == b:
        return True
    s, l = (a, b) if len(a) <= len(b) else (b, a)
    if len(s) >= 3 and l.startswith(s) and len(l) - len(s) <= 3:
        return True
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n >= 5


def _supported(word: str, quote_forms: set) -> bool:
    return any(_match(f, q) for f in _forms(word) for q in quote_forms)


def _quote_forms(excerpt: str) -> set:
    out = set()
    for w in _WORD.findall(_prep(excerpt)):
        out |= _forms(w)
    return out


def split_clauses(summary: str) -> list:
    """[(clause_text, separator_after)]; the clause text is stripped, the separator is the matched text ('; ', ', ', ' and ', '.' or '')."""
    parts, pos = [], 0
    for m in _SPLIT.finditer(summary):
        if m.group(0) == ".":
            before = re.findall(r"[A-Za-z.]+$", summary[:m.start()])
            tail = before[0].lower() if before else ""
            if tail.strip(".") in _ABBR_BEFORE_PERIOD or len(tail) == 1:
                continue
        seg = summary[pos:m.start()].strip()
        if seg:
            parts.append([seg, m.group(0)])
        elif parts:
            parts[-1][1] = parts[-1][1] if _strength(parts[-1][1]) >= _strength(m.group(0)) else m.group(0)
        pos = m.end()
    tail = summary[pos:].strip()
    if tail:
        parts.append([tail, ""])
    return [(a, b) for a, b in parts]


def _strength(sep: str) -> int:
    return _STRENGTH.get(sep.strip(), 0)


def _join(a: str, sep: str, b: str) -> str:
    s = sep.strip()
    if s == ".":
        return f"{a}. {b[:1].upper()}{b[1:]}"
    if s in (";", ","):
        return f"{a}{s} {b}"
    return f"{a}{sep if sep else ' '}{b}"


# ---------------------------------------------------------------- salient content (T-112 r2)
# (kind, family, word regex, families that also support it, extra regex matched in the QUOTE only)
# A summary word that matches a family is "salient"; it is supported when the quote has a word of that family or of a family in `covered_by`.
_FAMILIES = [
    # procedures, treatment, devices
    ("proc", "splint", r"^splint|^immobili[sz]", (), ""), ("proc", "cast", r"^cast(s|ed|ing)?$", (), ""), ("proc", "brace", r"^brac(e|es|ed|ing)$|^orthotic", (), ""),
    ("proc", "sling", r"^sling", (), ""), ("proc", "collar", r"^collar$|^cervicalcollar", (), ""),
    ("proc", "aid", r"^crutch|^cane(s)?$|^walker|^wheelchair|^boot$", (), ""),
    ("proc", "suture", r"^sutur|^stitch|^staple|^dermabond|^glue$", (), ""), ("proc", "dressing", r"^bandag|^dressing|^gauze", (), ""),
    ("proc", "mri", r"^mri$|^magnetic$", (), ""), ("proc", "ct", r"^ct$|^cat$|^tomograph", (), ""), ("proc", "xray", r"^xray|^radiograph|^xr$|^films?$", (), ""),
    ("proc", "ultrasound", r"^ultrasound|^sonogra", (), ""), ("proc", "emg", r"^emg$|^electromyo|^ncv$|^ncs$|^conduction$", (), ""),
    ("proc", "imaging", r"^imaging$|^scans?$", ("mri", "ct", "xray", "ultrasound"), ""),
    ("proc", "surgery", r"surg|^operat|^arthroscop|^fusion$|ectomy$|plasty$", (), r"^reduction$|^fixation$|^arthroplasty|^repair"),     # quote side: ORIF / RCR spelled out
    ("proc", "injection", r"^inject|^epidural|^esi$|^shots?$|^infusion", (), ""),
    ("proc", "therapy", r"^therap|^physio|^rehab|^chiropract|^acupunct|^massage|^traction$|^manipulat", (), r"^pt$"),
    ("proc", "plan", r"^order|^recommend|^advis|^request|^schedul|^arrang|^authori[sz]|^suggest|^propos", (), ""),
    ("proc", "refer", r"^refer", (), ""), ("proc", "prescribe", r"^prescri|^rx$|^script$|^dispens", (), ""),
    ("proc", "admit", r"^admit|^admission|^hospitali[sz]|^inpatient|^overnight|^icu$", (), ""), ("proc", "discharge", r"^discharg|^released$|^dismissed$", (), ""),
    # drugs (brand and generic names share a family)
    ("drug", "apap", r"^acetaminophen|^tylenol|^paracetamol", (), ""), ("drug", "ibuprofen", r"^ibuprofen|^advil|^motrin", (), ""),
    ("drug", "naproxen", r"^naproxen|^aleve|^naprosyn", (), ""), ("drug", "nsaid", r"^nsaid|^antiinflammatory", ("ibuprofen", "naproxen", "meloxicam", "ketorolac"), ""),
    ("drug", "cyclobenzaprine", r"^cyclobenzaprine|^flexeril", (), ""), ("drug", "tramadol", r"^tramadol|^ultram", (), ""),
    ("drug", "hydrocodone", r"^hydrocodone|^norco|^vicodin|^lortab", (), ""), ("drug", "oxycodone", r"^oxycodone|^percocet|^oxycontin", (), ""),
    ("drug", "gabapentin", r"^gabapentin|^neurontin", (), ""), ("drug", "meloxicam", r"^meloxicam|^mobic", (), ""),
    ("drug", "steroid", r"^prednisone|^medrol|^methylpred|^dexameth|^steroid|^cortisone", (), ""), ("drug", "ketorolac", r"^ketorolac|^toradol", (), ""),
    ("drug", "ondansetron", r"^ondansetron|^zofran", (), ""), ("drug", "benzo", r"^lorazepam|^ativan|^alprazolam|^xanax|^diazepam|^valium", (), ""),
    ("drug", "muscle_relaxant", r"^carisoprodol|^soma$|^methocarbamol|^robaxin|^relaxant", ("cyclobenzaprine",), ""), ("drug", "pregabalin", r"^pregabalin|^lyrica", (), ""),
    ("drug", "opioid", r"^opioid|^narcotic|^morphine|^fentanyl", ("tramadol", "hydrocodone", "oxycodone"), ""), ("drug", "aspirin", r"^aspirin", (), ""), ("drug", "lidocaine", r"^lidocaine|^lidoderm", (), ""),
    ("drug", "antibiotic", r"^antibiotic|^amoxicillin|^augmentin|^keflex|^cephalexin|^cipro", (), ""),
    ("drug", "meds", r"^medicat|^meds$|^medicine|^drug|^pills?$|^analgesic|^painkiller", ("apap", "ibuprofen", "naproxen", "nsaid", "cyclobenzaprine", "tramadol",
     "hydrocodone", "oxycodone", "gabapentin", "meloxicam", "steroid", "ketorolac", "ondansetron", "benzo", "muscle_relaxant", "pregabalin", "opioid", "aspirin",
     "lidocaine", "antibiotic", "prescribe"), ""),
    # body parts
    ("body", "neck", r"^neck|^cervic|^cspine|^c[1-7]$", (), ""), ("body", "back", r"^back$|^lumbar|^lumbosacral|^thoracic|^sacr|^coccyx|^tailbone|^lspine|^tspine|^[lt]\\d+$|^s1$", ("spine",), ""),
    ("body", "spine", r"^spine$|^spinal", ("neck", "back"), ""), ("body", "head", r"^head$|^skull|^scalp|^cranial|^cranium|^brain|^forehead", (), ""),
    ("body", "face", r"^jaw|^tmj|^mandib|^face$|^facial|^cheek|^chin$|^nose$|^nasal|^mouth|^teeth|^tooth|^dental|^lip$", (), ""),
    ("body", "eye", r"^eyes?$|^ocular|^orbital", (), ""), ("body", "ear", r"^ears?$|^auditory", (), ""), ("body", "throat", r"^throat|^larynx", (), ""),
    ("body", "shoulder", r"^shoulder|^clavicle|^collarbone|^rotator|^scapula|^acromi|^supraspinatus|^infraspinatus|^subscapularis|^labr|^glenohumeral|^deltoid", (), ""), ("body", "elbow", r"^elbow", (), ""),
    ("body", "arm", r"^arms?$|^forearm|^humer|^biceps?$|^triceps?$|^radius$|^ulna", (), ""), ("body", "wrist", r"^wrist|^carpal$", (), ""),
    ("body", "hand", r"^hands?$|^palm|^fingers?$|^digits?$|^thumb|^knuckle|^metacarp|^phalan", (), ""),
    ("body", "hip", r"^hips?$|^pelvi|^groin|^sacroiliac|^gluteal|^buttock|^glutes?$", (), ""),
    ("body", "leg", r"^legs?$|^thigh|^femur|^femoral|^shin$|^tibia|^fibula|^calf|^hamstring|^quadricep", (), ""),
    ("body", "knee", r"^knees?$|^patell|^menisc|^cruciate|^collateral|^tricompartmental|^acl$|^mcl$|^pcl$", (), ""), ("body", "ankle", r"^ankles?$|^achilles", (), ""),
    ("body", "foot", r"^foot$|^feet$|^toes?$|^heel$|^plantar|^metatars", (), ""), ("body", "chest", r"^chest|^ribs?$|^sternum|^sternal|^breast", (), ""),
    ("body", "abdomen", r"^abdom|^belly|^stomach|^abd$|^flank|^epigastr|^bowel|^liver|^spleen|^kidney|^bladder", (), ""),
    # diagnosis nouns
    ("dx", "fracture", r"^fractur|^fx$|^broken$", (), ""), ("dx", "sprain", r"^sprain", (), ""), ("dx", "strain", r"^strain", (), ""),
    ("dx", "whiplash", r"^whiplash", (), ""), ("dx", "concussion", r"^concuss|^mtbi$|^tbi$", (), ""),
    ("dx", "herniation", r"^herniat|^hernia$|^bulg|^protrusion|^extrusion|^hnp$", (), ""), ("dx", "tear", r"^tear$|^tears$|^torn$|^rupture|^avuls", (), ""),
    ("dx", "dislocation", r"^dislocat|^subluxat|^luxat", (), ""), ("dx", "contusion", r"^contus|^bruis|^ecchymos|^hematoma", (), ""),
    ("dx", "laceration", r"^lacerat|^abrasion|^gash", (), ""), ("dx", "radiculopathy", r"^radicul|^sciatic|^neuropath|^neuralg|^pinched$", (), ""),
    ("dx", "stenosis", r"^stenosis", (), ""), ("dx", "arthritis", r"^arthrit|^osteoarth|^degenerat|^spondyl|^osteophyt", (), ""),
    ("dx", "tendinitis", r"^tendin|^tendonit|^bursitis", (), ""), ("dx", "fibromyalgia", r"^fibromyalg", (), ""),
    ("dx", "depression", r"^depress", (), ""), ("dx", "anxiety", r"^anxi|^panic", (), ""), ("dx", "ptsd", r"^ptsd$|^posttraumatic", (), ""), ("dx", "insomnia", r"^insomnia", (), ""),
    ("dx", "diabetes", r"^diabet|^dm$", (), ""), ("dx", "hypertension", r"^hypertens|^htn$", (), ""),
    ("dx", "infection", r"^infect|^sepsis|^cellulitis|^abscess", (), ""), ("dx", "cancer", r"^cancer|^tumor|^malignan|^carcinoma", (), ""),
    ("dx", "stroke", r"^stroke|^seizure|^epilep", (), ""), ("dx", "migraine", r"^migraine", (), ""), ("dx", "asthma", r"^asthma|^copd$", (), ""),
]
_FAM = [(k, n, re.compile(rx), cov, re.compile(qx) if qx else None) for k, n, rx, cov, qx in _FAMILIES]
_BODY = frozenset(n for k, n, *_ in _FAMILIES if k == "body")
# Negation and side words are the lexicon's (code_lists.added_qualifier through grounding.view / aq), not lists of this module (T-105 r2, T-128 r2).
# Quote words that already carry a negation or a negative finding: a summary negation is then not NEW content (the judge decides if it is the right one).
_QUOTE_NEG = re.compile(r"\b(?:normal|unremarkable|wnl|nl|clear|intact|resolved|resolving|ruled|r/o|free|unable|cannot|persist\w*|unchanged|fail\w*|lack\w*|neg|non\w+|un[a-z]{4,}|"
                        r"nad|nkda|nonspecific)\b|\w+n't\b|\bw/o\b", re.IGNORECASE)
_QUOTE_LEFT = re.compile(r"(?<![a-z0-9])(?:l|lt|lft)(?![a-z0-9])|\bleft", re.IGNORECASE)
_QUOTE_RIGHT = re.compile(r"(?<![a-z0-9])(?:r|rt|rgt)(?![a-z0-9])|\bright", re.IGNORECASE)
_QUOTE_BOTH = re.compile(r"\bbilat\w*|\bb/l\b|\bboth\b|\beach\b", re.IGNORECASE)
_NUMWORDS = {"zero": 0, "no": None, "one": 1, "once": 1, "single": 1, "two": 2, "twice": 2, "double": 2, "three": 3, "thrice": 3, "four": 4, "five": 5, "six": 6, "seven": 7,
             "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
             "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "dozen": 12}
_MONTHS = grounding._MONTHS


def _family_hits(words) -> dict:
    """{family: word} for the words of a summary clause that name a procedure/device/drug, body part or diagnosis."""
    out = {}
    for w in words:
        for kind, name, rx, _cov, _qx in _FAM:
            if rx.search(w):
                out.setdefault(name, (kind, w))
    return out


def _quote_families(words) -> set:
    out = set()
    for w in words:
        for _k, name, rx, _cov, qx in _FAM:
            if rx.search(w) or (qx is not None and qx.search(w)):
                out.add(name)
    return out


_WORD_NUM = re.compile(r"[a-z]+\d*")


def _words(text: str) -> list:
    return _WORD_NUM.findall(_prep(text))


def _number_set(excerpt: str, label: str, date_iso: str) -> set:
    nums = set(grounding._allowed_numbers(excerpt, label, date_iso))
    for t in list(nums):
        if len(t) == 4 and t.isdigit():
            nums.add(str(int(t[2:])))                                      # 2024 ~ 24
    low = (excerpt + " " + label).lower()
    for w in re.findall(r"[a-z]+", low):
        if _NUMWORDS.get(w) is not None:
            nums.add(str(_NUMWORDS[w]))
    for i, m in enumerate(_MONTHS, 1):
        if m[:3] in low and re.search(r"\b" + m[:3], low):
            nums.add(str(i))
    for m in re.findall(r"\bx\s?(\d+)\b|\b(\d+)\s?x\b", low):
        nums.update(x for x in m if x)
    return nums


def new_salient(clause: str, quote: dict) -> list:
    """The salient items of `clause` that the quote lacks (empty -> the clause stays). Items are short labels for the audit trail.
    Numbers, months, sides and negations count only for a clause that shares no content word with the quote ('4 weeks' over a pain sentence): a clause about
    the quote's own topic with a changed value ('Pain 3/10' over 'Pain 4/10') stays, because the D-034/D-047 code checks flag it needs_review and the paralegal sees the conflict."""
    out, loose = [], []
    nums = grounding._num_tokens(clause)
    loose += [n for n in nums if n not in quote["nums"]]
    low = clause.lower()
    for m in grounding._MONTH_RX.findall(clause):
        if m.lower() not in quote["low"] and m.lower() != quote["month"] and str(_MONTHS.index(m.lower()) + 1) not in quote["nums"]:
            out.append(m.lower())
    sw = grounding.side_neg_words(clause, keep_order=True)
    for w in dict.fromkeys(sw):
        if grounding.aq("side").fullmatch(w):
            ok = w in quote["sides"] or (w.startswith("bilateral") and (quote["both"] or {"left", "right"} <= quote["sides"]))
            if not ok:
                loose.append(w)
        elif w.endswith("n't") or grounding.is_negation_word(w):
            if not quote["neg"]:
                loose.append(w)
    toks = re.findall(r"[A-Za-z0-9]+", clause)
    proper = {t.lower() for i, t in enumerate(toks) if i and len(t) > 2 and t[0].isupper() and t[1:].islower()}      # 'Fennimoor Spine Clinic', 'Capital Imaging': a name, not a body part
    hits = _family_hits([w for w in _words(clause) if w not in proper])
    for name, (kind, w) in hits.items():
        cov = next(c for _k, n, _r, c, _q in _FAM if n == name)
        if name not in quote["fams"] and not (set(cov) & quote["fams"]):
            out.append(w)
    if loose and not any(_supported(w, quote["forms"]) for w in content_words(clause)):
        out += loose
    return list(dict.fromkeys(out))


# The record's source label ('Valley Imaging, cervical MRI') is part of what the quote sits in: it vouches for body parts, sides and imaging modality,
# never for treatment, drug or diagnosis words (a label that says 'orthopedic surgery' does not support 'surgery recommended').
_LABEL_FAMILIES = frozenset({"mri", "ct", "xray", "ultrasound", "emg", "imaging"})


def _quote_profile(excerpt: str, label: str, date_iso: str) -> dict:
    ex = excerpt or ""
    sides = set()          # 'left' / 'right' by the abbreviation-aware patterns below; a quote's 'bilateral' sets "both" (_QUOTE_BOTH), which is how the summary's side is checked
    if _QUOTE_LEFT.search(ex + " " + (label or "")):
        sides.add("left")
    if _QUOTE_RIGHT.search(ex + " " + (label or "")):
        sides.add("right")
    month = ""
    m = re.match(r"\d{4}-(\d{2})", date_iso or "")
    if m:
        month = _MONTHS[int(m.group(1)) - 1]
    low = (ex + " " + (label or "")).lower()
    neg = bool(grounding.has_negation(ex, extra=True) or _QUOTE_NEG.search(ex))
    return {"nums": _number_set(ex, label or "", date_iso or ""), "low": low, "month": month, "sides": sides, "both": bool(_QUOTE_BOTH.search(ex) or _QUOTE_BOTH.search(_prep(ex))), "neg": neg,
            "forms": _quote_forms(ex + " " + (label or "")), "fams": _quote_families(_words(ex)) | {f for f in _quote_families(_words(label or "")) if f in _LABEL_FAMILIES or f in _BODY}}


def trim(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> dict:
    """See the module docstring. Never edits a kept clause's words; only whole clauses are dropped, or nothing is."""
    clauses = split_clauses(summary or "")
    quote = _quote_profile(excerpt, label, date_iso)
    why_removed = [new_salient(text, quote) for text, _ in clauses]
    drop = [bool(w) for w in why_removed]
    unchanged = {"text": summary, "removed": [], "kept": [c[0] for c in clauses], "supported": bool(summary), "notes": [], "changed": False}
    if not any(drop):
        return unchanged
    removed = [c[0].rstrip(" .;,") for c, d in zip(clauses, drop) if d]
    notes = [NOTE.format(r) for r in removed]
    left = [c[0] for c, d in zip(clauses, drop) if not d]
    if not left or not any(content_words(c) for c in left):
        return {"text": "", "removed": removed, "kept": [], "supported": False, "notes": notes, "changed": True}
    # T-128 r2/r3 (D-054 'never leave a fragment'), structural, no word list:
    if drop[0]:                                      # (2) the first clause is never removed: an unsupported first clause means the whole summary goes to judge 1
        return unchanged
    first_cut = drop.index(True)
    if not all(drop[first_cut:]):                    # (1) SUFFIX ONLY (T-128 r3): a clause is removed only when every clause after it is removed too, so no kept clause can depend on a removed one
        return unchanged
    if len(content_words(" ".join(c[0] for c in clauses[:first_cut]))) < 2:       # (3) the kept prefix must carry at least 2 content words ('Pain.' alone is not a summary)
        return unchanged
    out, last_kept = "", None
    for i, ((text, sep), d) in enumerate(zip(clauses, drop)):
        if d:
            continue
        piece = text.rstrip(" .;,")
        if last_kept is None:
            out = piece
        else:
            prev_sep = clauses[last_kept][1]
            use = prev_sep if i - 1 == last_kept else max((clauses[j][1] for j in range(last_kept, i)), key=_strength)
            out = _join(out, use, piece)
        last_kept = i
    out = out[:1].upper() + out[1:]
    if summary.rstrip().endswith("."):
        out += "."
    return {"text": out, "removed": removed, "kept": left, "supported": True, "notes": notes, "changed": True}
