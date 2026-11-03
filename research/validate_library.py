#!/usr/bin/env python3
"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).

check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
doctors named in opinions, study authors, firms, counties, cities and highways. Matching is case-insensitive and
accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.

Self-test checks the v2 doc mechanically: every surname written before author initials or 'et al' (e.g. 'Fraser S.G.'), every
bare surname in a parenthesised list inside a paragraph that cites earlier sources (e.g. 'Brinjikji, Nakashima'), and every
'X v. Y' / 'In re X' caption name must be on the denylist, and each one planted in a packet must fail the scan. A newly cited
name therefore fails the self-test until it is added to DENYLIST_V2 and the doc's 'Denylist additions' block.

Run:        python3 research/validate_library.py
Self-test:  python3 research/validate_library.py --self-test
"""
import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIB = ROOT / "evals" / "library"
V2_DOC = ROOT / "research" / "case-library-sources-v2.md"

# v1 sources (research/case-library-sources.md). States are listed because v1 sources named them; packets use the
# two-letter abbreviation (e.g. "TX") where a state must appear.
DENYLIST_V1 = ["Nichols", "Duke Linden", "Haygood", "Escabedo", "K & L", "K&L", "Auto Crushers", "Alexandria", "Puerto Rico",
               "Rissman", "Colossus", "Manitoba", "Verisk", "Medicare", "Tennessee", "Nebraska", "New Jersey", "Virginia",
               "Oklahoma", "Texas", "Florida", "California", "Illinois", "Michigan", "Kelly", "Cutch"]
# v2 sources (research/case-library-sources-v2.md, "Denylist additions" block). Keep the two lists in sync; --self-test checks.
DENYLIST_V2 = [
    # P1 JLG Trucking v. Garza
    "JLG", "Garza", "Pechero", "Zapata",
    # P2 Guevara v. Ferrer
    "Guevara", "Ferrer",
    # P3 Hills v. Donis (parties, the doctor named in the opinion, the author justice, the highway)
    "Donis", "Matamoros", "Castellanos", "Morehouse", "Reuben", "Rueben", "Poissant", "I-45",
    # P4 Chiv v. Figueroa
    "Chiv", "Figueroa",
    # P5 In re Central Oregon Truck Co.
    "Central Oregon", "Oregon", "Broussard",
    # P6 Gunn v. McCoy
    "Gunn", "McCoy",
    # P7 Rodriguez v. Wal-Mart Stores
    "Rodriguez", "Wal-Mart", "Walmart",
    # P16 defense-firm write-up
    "Lewis Brisbois", "Brisbois", "Harris County",
    # P17 Hampton v. Miskell (dropped as a source, names still banned) and Castro et al.
    "Hampton", "Miskell", "Baratta", "I-635", "Castro", "Schilgen",
    # Study authors cited in v2 (author initials or 'et al' in source lines; bare names in the opening citation list)
    "Steinkamp", "Kantrowitz", "Airan-Javia", "ElGhrably", "Fishbain", "Powell", "Anderson",
    "Fraser", "Brinjikji", "Nakashima", "Vera", "Rodríguez-Vera",
    # Firm website slugs in cited URLs (not people; a slug never occurs as ordinary packet text)
    "mdjwlaw", "painterfirm",
    # Cities and counties named in v2 citations; insurer named in a v1 caption that v2 mentions
    "Houston", "Dallas", "Allstate",
]
# Real names that are also ordinary lowercase words: banned only when capitalised (Title or UPPER), so "rolling hills" or
# "flores" (Spanish for flowers) in a packet still passes while "Hills" / "FLORES" as a name fails.
DENY_CAPITALISED = ["Hills", "Flores", "Bai", "FAIR Health"]
# Eponymous clinical terms that share a name with a cited author and are allowed in packets on purpose.
ALLOWED_EPONYMS = ["Waddell"]
DENYLIST = DENYLIST_V1 + DENYLIST_V2
BANNER = "SYNTHETIC — invented for evaluation; not real patient data\n"


def fold(s):
    """Strip accents so 'Rodríguez' matches 'Rodriguez'."""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


_ANY = [(w, re.compile(r"(?<!\w)" + re.escape(fold(w)) + r"(?!\w)", re.I)) for w in DENYLIST]
_CAP = [(w, re.compile(r"(?<!\w)(?:" + re.escape(w) + "|" + re.escape(w.upper()) + r")(?!\w)")) for w in DENY_CAPITALISED]


def scan_text(text):
    """Return the denylist terms found in text (case- and accent-insensitive; capitalised-only terms need a capital)."""
    t = fold(text)
    return [w for w, rx in _ANY if rx.search(t)] + [w for w, rx in _CAP if rx.search(t)]


def doc_denylist_block(doc_text):
    """Terms listed in the v2 doc's fenced 'Denylist additions' block (one per line, '#' comments allowed)."""
    m = re.search(r"## Denylist additions.*?```text\n(.*?)```", doc_text, re.S)
    if not m:
        return None
    return [ln.split("#")[0].strip() for ln in m.group(1).splitlines() if ln.split("#")[0].strip()]


_GENERIC = {"In", "re", "Inc", "Inc.", "LLC", "LLC,", "Co", "Co.", "Stores", "Stores,", "Truck", "Trucking", "Trucking,", "The",
            "of", "and", "Tex", "Tex.", "App", "App.", "No", "No."}


def doc_caption_names(doc_text):
    """Capitalised name tokens from every 'X v. Y' and 'In re X' caption in the v2 doc."""
    names = set()
    for a, b in re.findall(r"([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*) v\. ([A-Z][\w.'&-]*(?:,? [A-Z][\w.'&-]*)*)", doc_text):
        for side in (a, b):
            for tok in re.split(r"[ ,]+", side):
                if len(tok) > 1 and tok not in _GENERIC and tok[0].isupper() and not any(c.isdigit() for c in tok):
                    names.add(tok.rstrip(".,"))
    for x in re.findall(r"In re ([A-Z][\w'-]*(?: [A-Z][\w'-]*)*)", doc_text):
        toks = [t for t in x.split() if t not in _GENERIC]
        if toks:
            names.add(" ".join(toks[:2]))
    return names


# A surname is a capitalised word directly before author initials ('Fraser S.G.', 'Steinkamp J.', 'Rodríguez-Vera F.J.')
# or before 'et al' ('Fishbain et al.'). Initials are capital letters only, so 'Co.', 'Inc.' and 'No.' never match.
_AUTHOR_RX = re.compile(r"(?<![\w'’-])([A-Z][\w'’-]*)(?=,? [A-Z]\.(?:[A-Z]\.)*(?!\w)|\s+et al\b)")


def doc_author_names(doc_text):
    """Surnames written before author initials or 'et al' anywhere in the v2 doc."""
    return {m.group(1) for m in _AUTHOR_RX.finditer(doc_text)}


def doc_listed_citation_names(doc_text):
    """Bare surnames in parenthesised lists inside paragraphs that cite earlier sources (the 'already cited' sentence).

    Only single capitalised words with lowercase letters count, so acronyms (MIST), IDs (D-043) and tool names are skipped
    by shape, and multi-word items such as 'In re Allstate' or 'K&L Auto Crushers' are left to the denylist entries.
    """
    names = set()
    for para in re.split(r"\n\s*\n", doc_text):
        if "cited" not in para:
            continue
        flat = " ".join(para.split())
        for group in re.findall(r"\(([^()]*)\)", flat):
            for item in re.split(r"[,;]", group):
                item = item.strip()
                if re.fullmatch(r"[A-Z][a-z][\w'’-]*", item):
                    names.add(item)
    return names


def doc_citation_names(doc_text):
    """Every name the v2 doc cites: author surnames, bare names in citation lists, and caption names."""
    return doc_author_names(doc_text) | doc_listed_citation_names(doc_text) | doc_caption_names(doc_text)


def _covered(name, listed):
    """A cited name is covered when the name, one of its words, or one of its hyphen parts is listed (case/accent-insensitive)."""
    return any(fold(p).lower() in listed for p in [name] + name.split() + re.split(r"-", name))


def self_test(doc_text=None):
    """Run the self-test. doc_text overrides the v2 doc (used to prove a newly cited name fails the test)."""
    fails = []
    for w in DENYLIST:
        for variant in {w, w.lower(), w.upper(), w.swapcase(), w.title()}:
            if w not in scan_text(f"Seen by Dr. {variant} at the clinic."):
                fails.append(f"planted {variant!r} not caught")
    for w in DENY_CAPITALISED:
        for variant in (w, w.upper()):
            if w not in scan_text(f"Referred by {variant} Family Clinic."):
                fails.append(f"planted {variant!r} not caught")
        if scan_text(f"walked up the {w.lower()} near home"):
            fails.append(f"lowercase common word {w.lower()!r} wrongly flagged")
    if not scan_text("Patient: Ana Rodríguez (SYNTHETIC)"):
        fails.append("accented Rodríguez not caught")
    for w in ALLOWED_EPONYMS:
        if scan_text(f"{w} signs 0/5 today."):
            fails.append(f"eponym {w!r} wrongly flagged")
    doc = V2_DOC.read_text() if doc_text is None else doc_text
    block = doc_denylist_block(doc)
    listed = {fold(w).lower() for w in DENYLIST + DENY_CAPITALISED + ALLOWED_EPONYMS}
    if block is None:
        fails.append("v2 doc has no '## Denylist additions' ```text block")
    else:
        for w in block:
            if fold(w).lower() not in listed:
                fails.append(f"v2 doc denylist term {w!r} missing from validate_library.py")
        for w in DENYLIST_V2 + DENY_CAPITALISED:
            if w not in block:
                fails.append(f"validate_library.py term {w!r} missing from the v2 doc block")
    authors = doc_author_names(doc)
    cite_lists = doc_listed_citation_names(doc)
    captions = doc_caption_names(doc)
    for name in sorted(authors | cite_lists | captions):
        if not _covered(name, listed):
            kind = "author" if name in authors else "citation-list" if name in cite_lists else "caption"
            fails.append(f"v2 doc cites {kind} name {name!r} but it is not on the denylist (add it to DENYLIST_V2 and the doc block)")
    with tempfile.TemporaryDirectory() as tmp:
        # Every cited author or citation-list surname, planted in a packet, must make the library scan fail.
        for i, name in enumerate(sorted(authors | cite_lists)):
            p = pathlib.Path(tmp) / f"case_planted_author_{i}.txt"
            p.write_text(BANNER + f"Seen by {name} S.G. at the clinic on 03/06/2026.\n")
            if not scan_library([p]):
                fails.append(f"planted author/citation surname {name!r} passed the library scan")
        # End-to-end: a planted packet must make the library scan fail.
        p = pathlib.Path(tmp) / "case_planted.txt"
        p.write_text(BANNER + "Patient seen by DR. GARZA after the crash on i-45.\n")
        if not scan_library([p]):
            fails.append("planted packet passed the library scan")
    for f in fails:
        print("SELF-TEST FAIL:", f)
    n = len(DENYLIST) * 5 + len(DENY_CAPITALISED) * 3 + len(authors | cite_lists)
    print("self-test:", "FAIL" if fails else
          f"ok ({n} planted variants caught; {len(authors | cite_lists | captions)} cited names covered: "
          f"{len(authors)} author, {len(cite_lists)} citation-list, {len(captions)} caption)")
    return 1 if fails else 0


def scan_library(files):
    bad = []
    for f in files:
        t = f.read_text()
        for w in scan_text(t):
            bad.append(f"{f.name}: contains real identifier {w!r}")
        if f.suffix == ".txt" and not t.startswith(BANNER):
            bad.append(f"{f.name}: missing SYNTHETIC header")
    return bad


def main():
    if "--self-test" in sys.argv:
        return self_test()
    cases = sorted(LIB.glob("case_*.expected.json"))
    if len(cases) < 6:
        print(f"FAIL: need >= 6 library cases, found {len(cases)}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / "golden"
        shutil.copytree(ROOT / "evals" / "golden", d)
        for f in LIB.glob("case_*"):
            shutil.copy(f, d / f.name)
        r = subprocess.run([sys.executable, str(d / "check_golden.py")], capture_output=True, text=True, cwd=d)
    print(r.stdout.strip()[-1500:] or r.stderr.strip()[-1500:])
    bad = scan_library(sorted(LIB.glob("case_*")))
    for b in bad:
        print("IDENTIFIER CHECK FAIL:", b)
    terms = len(DENYLIST) + len(DENY_CAPITALISED)
    print("identifier check:", "FAIL" if bad else f"ok ({len(cases)} packets, {terms} denylist terms, case-insensitive)")
    return 1 if (r.returncode or bad) else 0


if __name__ == "__main__":
    sys.exit(main())
