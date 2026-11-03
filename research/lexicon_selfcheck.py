"""Self-check for app/llm/lexicon.yaml (T-009, round 2). Reference matcher only, not product code.

Run: .venv/bin/python research/lexicon_selfcheck.py [--verbose]
1. Schema per D-018 (flag_type, category, hedge, self_report, strength, negatable; code_lists present).
2. Every regex compiles; every entry's examples behave (hit / miss / negated).
3. The Appendix A sample: hits per record equal each entry's `appendix_c`.
4. Every golden case (evals/golden/*.txt): recall on must/should pre_existing and causation flags (a high/medium
   hit of the same type overlapping the evidence excerpt), must_not_flag checks, code-list scans
   (non_encounter over Source labels, injection, accident_date_phrases).
5. Both reviewer probe sets (artifacts/review-evidence/T-009-nurse-probes.txt and the PROBES list in
   T-009-adjuster-probes.py, read with ast, not executed): false positives and false negatives.
PASS = no schema/example errors, no appendix_c mismatch, 100% recall on golden MUST flags, no must_not
violation, ≤ 2 false positives across both probe sets (bar set by the orchestrator for round 2).

Reference semantics implemented here (the backend may differ but must pass the same vectors):
negation guard (clause-bounded, list exception, field answers), year_filter, suppress_if_followed_by.
`negated(text, start, end, neg)` keeps its round-1 signature so the reviewers' probe scripts still import it.
"""
import ast
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "app" / "llm" / "lexicon.yaml"
GOLDEN = ROOT / "evals" / "golden"
EVID = ROOT / "artifacts" / "review-evidence"
REQUIRED = ("id", "pattern", "flag_type", "category", "hedge", "self_report", "strength", "negatable",
            "rationale", "source", "false_positive", "appendix_c")
RAISES = ("high", "medium")
HELDOUT = ROOT / "evals" / "lexicon_heldout.jsonl"
HELDOUT_BAR = 0.85
# ADR-013 closed category list (memory/DECISIONS.md, api.md "Closed category lists"). Lexicon entries may use only these.
ADR013_LEXICON_CATEGORIES = {
    "pre_existing", "degenerative_language", "prior_surgery",
    "speculative_language", "patient_report", "missed_care", "new_onset", "scene_facts", "alternative_cause",
    "litigation_referral", "objective_negative", "recovery_context", "accident_date_provenance"}
PROBE_ACCIDENT_YEAR = 2026  # probes are written around the 2026 sample case
VERBOSE = "--verbose" in sys.argv

TOKEN = re.compile(r"[\w'/-]+|[;,]")
SENT_END = re.compile(r"[.!?](?=\s|$)|\n")


# ───────────── negation guard ─────────────

def _sentence_bounds(text, start, end):
    s = 0
    for m in SENT_END.finditer(text, 0, start):
        s = m.end()
    m = SENT_END.search(text, end)
    return s, (m.start() if m else len(text))


def _norm(tokens):
    return " " + " ".join(t.lower() for t in tokens if t not in (",", ";")) + " "


def _strip_pseudo(s, pseudo):
    for p in pseudo:
        s = s.replace(" " + p.lower() + " ", " ")
    return s


def _has(s, phrases):
    return any((" " + p.lower() + " ") in s for p in phrases)


def _cut_at_terminator(tokens, terms, from_end=True):
    """Return the part of tokens after the last (from_end) / before the first terminator."""
    low = [t.lower() for t in tokens]
    joined = " " + " ".join(low) + " "
    multi = [t for t in terms if " " in t]
    if from_end:
        for i in range(len(low) - 1, -1, -1):
            if low[i] in terms or any(" ".join(low[i:i + len(m.split())]) == m for m in multi):
                return tokens[i + 1:]
        return tokens
    for i in range(len(low)):
        if low[i] in terms or any(" ".join(low[i:i + len(m.split())]) == m for m in multi):
            return tokens[:i]
    return tokens


def negated(text, start, end, neg):
    """Clause-bounded NegEx-style guard (D-018). True if the hit text[start:end] is negated."""
    s0, s1 = _sentence_bounds(text, start, end)
    after_text = text[end:s1]
    # field-style answer may follow a sentence-ending "?" ("Prior injuries? Denies."), so test the rest of the text
    if neg.get("field_answer") and re.match(neg["field_answer"], text[end:], re.I):
        return True
    terms = [t.lower() for t in neg["clause_terminators"]]
    word_terms = [t for t in terms if t not in (",", ";")]
    pseudo = neg["pseudo_negations"]
    w = neg["window_tokens"]
    before = TOKEN.findall(text[s0:start])

    # split the before-text into comma segments (semicolons always end scope)
    if ";" in before:
        before = before[len(before) - before[::-1].index(";"):]
    segs, cur = [], []
    for t in before:
        if t == ",":
            segs.append(cur)
            cur = []
        else:
            cur.append(t)
    segs.append(cur)  # last = the hit's own segment

    def seg_negates(seg):
        tail = _cut_at_terminator(seg, word_terms)[-w:]
        return _has(_strip_pseudo(_norm(tail), pseudo), neg["pre_cues"])

    if seg_negates(segs[-1]):
        return True
    # list exception: hit segment contains or/nor, earlier segments breaker-free back to the cue
    hit_seg = [t.lower() for t in segs[-1]]
    if len(segs) > 1 and any(c in hit_seg for c in neg["list_coordinators"]):
        breakers = set(b.lower() for b in neg["list_breakers"])
        if not breakers & set(hit_seg):
            for seg in reversed(segs[:-1]):
                low = [t.lower() for t in seg]
                if _has(_strip_pseudo(_norm(seg), pseudo), neg["pre_cues"]):
                    # the cue segment may contain breakers only before the cue (e.g. "ROS: Denies fever")
                    return True
                if breakers & set(low) or any(t in word_terms for t in low):
                    break
    # post-cues within the hit's clause
    after = TOKEN.findall(after_text)
    clause = []
    for t in after:
        if t in (",", ";") or t.lower() in word_terms:
            break
        clause.append(t)
    return _has(_strip_pseudo(_norm(clause[:w]), pseudo), neg["post_cues"])


# ───────────── matcher ─────────────

YEAR = re.compile(r"\b(19|20)\d{2}\b")


def _hit_year(m):
    for g in ("year", "year2"):
        try:
            if m.group(g):
                return int(m.group(g))
        except IndexError:
            pass
    y = YEAR.search(m.group(0))
    return int(y.group(0)) if y else None


def _clause_after(text, end):
    m = re.search(r"[,;.\n]", text[end:])
    return text[end:end + m.start()] if m else text[end:]


def production_chip(text):
    """D-040 (supersedes D-037): ask the PRODUCTION code, not a reference copy. True only if production would put a speaker chip on this
    excerpt: a surviving grounding.has_self_report, or any lexicon flag for the sentence with source_kind 'patient_report'. Expected: never."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from app.backend import flags, grounding
    if hasattr(grounding, "has_self_report"):
        return True
    rec = {"n": 1, "id": "r1", "source": "Clinic", "excerpt": text, "date_iso": "2026-06-01"}
    return any(f.get("source_kind") == "patient_report" for f in flags.lexicon_flags(rec))


# T-061 r3 B1/B2 rows (reviews/T-061-claims-adjuster-r3.md) plus the D-037 keep rows; D-040: no row gets a chip; production is asked every time.
CHIP_NO = ["Patient states pain began after the collision, wife reports headaches.", "Pt reports neck pain, EMS notes headaches.",
           "Patient reports neck pain and his wife says he is in pain.", "Patient reports neck pain, per his wife, headaches began at the scene.",
           "Patient reports neck pain (per wife, headaches since the scene).", "Patient reports pain 4/10, girlfriend says he limps.",
           "Patient reports neck pain, Mrs. Ortiz reports headaches.", "Patient states neck pain; wife thinks he is faking.",
           "Patient reports neck pain, wife thinks he is faking.", "Patient states neck pain; his wife told the ER he was fine.",
           "Patient states neck pain, EMS notes headaches, wife reports nausea.", "Pt c/o neck pain; wife drove him in.", "C/O neck pain 7/10 and headache."]
CHIP_YES = ["Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
            "Pt reports neck pain 7/10.", "Patient complains of lower back pain."]


def hits(entry, text, neg, accident_year):
    """List of (start, end, matched) that FIRE (not negated / filtered / suppressed)."""
    out = []
    for m in entry["_rx"].finditer(text):
        if entry.get("negatable") and negated(text, m.start(), m.end(), neg):
            continue
        if entry.get("year_filter") and accident_year:
            y = _hit_year(m)
            if y and y >= accident_year:
                continue
        sup = entry.get("_sup")
        if sup and sup.search(_clause_after(text, m.end())):
            continue
        out.append((m.start(), m.end(), m.group(0)))
    return out


def fires(entry, rx, text, neg, accident_year=PROBE_ACCIDENT_YEAR):  # round-1 compatible helper
    return bool(hits(entry, text, neg, accident_year))


def scan(entries, text, neg, accident_year):
    res = []
    for e in entries:
        for h in hits(e, text, neg, accident_year):
            res.append((e, h))
    return res


# ───────────── golden parsing ─────────────

REC = re.compile(r"=== Record (\d+) ===\s*\nDate:\s*(.*?)\nSource:\s*(.*?)\nExcerpt:\s*\"(.*?)\"\s*(?:\n|$)", re.S)


def parse_case(path):
    recs = {}
    for n, date, src, exc in REC.findall(path.read_text()):
        recs[int(n)] = {"date": date.strip(), "source": src.strip(), "text": exc}
    years = [int(y.group(0)) for r in recs.values() for y in [re.search(r"\b(?:19|20)\d{2}\b", r["date"])] if y]
    return recs, (min(years) if years else None)


def _overlaps(text, span, excerpt):
    i = text.find(excerpt)
    if i < 0:
        return True  # evidence not found verbatim in the excerpt line (header evidence): any hit in record counts
    return span[0] < i + len(excerpt) and span[1] > i


# ───────────── main ─────────────

def main():
    lex = yaml.safe_load(LEX.read_text())
    neg = lex["negation"]
    entries = lex["entries"]
    types = set(lex["flag_types"])
    errors, ids = [], set()

    for e in entries:
        for f in REQUIRED:
            if f not in e or e[f] is None or (isinstance(e[f], str) and not e[f].strip()):
                errors.append(f"{e.get('id')}: missing {f}")
        if e["id"] in ids:
            errors.append(f"duplicate id {e['id']}")
        ids.add(e["id"])
        if e["flag_type"] not in types or e["flag_type"] == "record_warning":
            errors.append(f"{e['id']}: flag_type {e['flag_type']} not allowed for lexicon entries")
        if e.get("category") not in ADR013_LEXICON_CATEGORIES:
            errors.append(f"{e['id']}: category {e.get('category')!r} not in the ADR-013 closed list")
        if e["strength"] not in ("high", "medium", "low"):
            errors.append(f"{e['id']}: bad strength")
        if not isinstance(e["hedge"], bool) or not isinstance(e["self_report"], bool):
            errors.append(f"{e['id']}: hedge/self_report must be booleans")
        if e["hedge"] and e["self_report"]:
            errors.append(f"{e['id']}: an entry cannot be both hedge and self_report (R-TL-8)")
        try:
            e["_rx"] = re.compile(e["pattern"], re.I | re.M)
            e["_sup"] = re.compile(e["suppress_if_followed_by"], re.I) if e.get("suppress_if_followed_by") else None
        except re.error as exc:
            errors.append(f"{e['id']}: regex error {exc}")
            continue
        ex = e.get("examples", {})
        for s in ex.get("hit", []):
            if not hits(e, s, neg, PROBE_ACCIDENT_YEAR):
                errors.append(f"{e['id']}: should HIT: {s!r}")
        for s in ex.get("miss", []):
            if hits(e, s, neg, PROBE_ACCIDENT_YEAR):
                errors.append(f"{e['id']}: should MISS: {s!r}")
        for s in ex.get("negated", []):
            if not e["_rx"].search(s):
                errors.append(f"{e['id']}: negated example does not match regex: {s!r}")
            elif hits(e, s, neg, PROBE_ACCIDENT_YEAR):
                errors.append(f"{e['id']}: should be NEGATED/filtered: {s!r}")
    for name in ("non_encounter", "accident_date_phrases", "injection", "damages"):
        cl = lex.get("code_lists", {}).get(name)
        if not cl:
            errors.append(f"code_lists.{name} missing")
            continue
        for f in ("consumer", "rationale", "source", "false_positive", "entries", "examples"):
            if f not in cl:
                errors.append(f"code_lists.{name}: missing {f}")
        cl["_rx"] = [re.compile(x["pattern"], re.I | re.M) for x in cl["entries"]]
        for s in cl["examples"].get("hit", []):
            if not any(r.search(s) for r in cl["_rx"]):
                errors.append(f"code_lists.{name}: should HIT: {s!r}")
        for s in cl["examples"].get("miss", []):
            if any(r.search(s) for r in cl["_rx"]):
                errors.append(f"code_lists.{name}: should MISS: {s!r}")
    entries = [e for e in entries if "_rx" in e]
    cls = lex["code_lists"]

    def cl_hit(name, s):
        return any(r.search(s) for r in cls[name]["_rx"])

    print(f"entries: {len(entries)}  by type: " + ", ".join(
        f"{t}={sum(1 for e in entries if e['flag_type'] == t)}" for t in ("pre_existing", "causation"))
        + f"  hedge={sum(e['hedge'] for e in entries)}  self_report={sum(e['self_report'] for e in entries)}"
        + "  code_lists: " + ", ".join(f"{k}={len(v['entries'])}" for k, v in cls.items()))

    # 3. sample appendix_c
    sample, sample_year = parse_case(GOLDEN / "sample.txt")
    mismatch = []
    print(f"\n[sample] hits per record (accident year proxy {sample_year})")
    for n, r in sample.items():
        got = {e["id"] for e, _ in scan(entries, r["text"], neg, sample_year)}
        print(f"  {n}: " + ", ".join(sorted(f"{i}[{next(e['strength'] for e in entries if e['id'] == i)}]" for i in got)))
        for e in entries:
            if (n in (e.get("appendix_c") or [])) != (e["id"] in got):
                mismatch.append(f"record {n}: {e['id']} expected={n in (e.get('appendix_c') or [])} got={e['id'] in got}")

    # 4. golden cases
    print("\n[golden] recall on pre_existing/causation flags (high/medium hit of same type overlapping evidence)")
    must_total = must_hit = should_total = should_hit = 0
    golden_fail, mustnot_fail, cl_report = [], [], []
    for exp_path in sorted(GOLDEN.glob("*.expected.json")):
        exp = json.loads(exp_path.read_text())
        txt = GOLDEN / exp.get("input_file", exp_path.name.replace(".expected.json", ".txt"))
        if not txt.exists():
            txt = GOLDEN / exp_path.name.replace(".expected.json", ".txt")
        recs, ay = parse_case(txt)
        case = exp_path.name.replace(".expected.json", "")
        for fl in exp.get("flags", []):
            if fl["type"] not in ("pre_existing", "causation") or fl.get("level") not in ("must", "should"):
                continue
            ok = True
            for ev in fl["evidence"]:
                r = recs.get(ev["record_no"])
                found = r and any(e["flag_type"] == fl["type"] and e["strength"] in RAISES
                                  and _overlaps(r["text"], (h[0], h[1]), ev["excerpt"])
                                  for e, h in scan(entries, r["text"], neg, ay))
                ok = ok and bool(found)
            if fl["level"] == "must":
                must_total += 1
                must_hit += ok
            else:
                should_total += 1
                should_hit += ok
            line = f"  {case} {fl['id']} {fl['type']} {fl['level']}: {'HIT' if ok else 'MISS'}"
            print(line)
            if not ok and fl["level"] == "must":
                golden_fail.append(line.strip())
        for mn in exp.get("must_not_flag", []):
            if mn.get("type") not in ("pre_existing", "causation"):
                continue
            scope = mn.get("record_nos") or list(recs)
            bad = [(n, e["id"], h[2]) for n in scope for e, h in scan(entries, recs[n]["text"], neg, ay)
                   if e["flag_type"] == mn["type"] and e["strength"] in RAISES]
            status = "OK" if not bad else f"VIOLATED {bad}"
            print(f"  {case} must_not {mn['id']} {mn['type']}: {status}")
            if bad:
                mustnot_fail.append(f"{case} {mn['id']}: {bad}")
        for n, r in recs.items():
            if cl_hit("non_encounter", r["source"]):
                cl_report.append(f"non_encounter: {case} r{n} '{r['source']}'")
            if cl_hit("injection", r["text"]):
                cl_report.append(f"injection: {case} r{n}")
            if cl_hit("accident_date_phrases", r["text"]):
                cl_report.append(f"accident_date_phrases: {case} r{n}")
    print(f"  MUST recall {must_hit}/{must_total}; SHOULD recall {should_hit}/{should_total}")
    print("\n[golden] code-list hits\n  " + "\n  ".join(cl_report))

    # 5. probes
    fp, fn = [], []
    vmap = lex.get("v1_type_map", {})
    nurse = EVID / "T-009-nurse-probes.txt"
    adj = EVID / "T-009-adjuster-probes.py"
    print("\n[probes] nurse (FIRE: high/medium of the mapped type; SUPPRESS/NONE: no high/medium)")
    n_ok = n_tot = 0
    if nurse.exists():
        for line in nurse.read_text().splitlines():
            if line.startswith("#") or not line.strip():
                continue
            cat, exp, s = [x.strip() for x in line.split("|", 2)]
            res = scan(entries, s, neg, PROBE_ACCIDENT_YEAR)
            n_tot += 1
            if exp.startswith("FIRE:"):
                t = vmap.get(exp[5:], exp[5:])
                # low-only hits are NOT flags (T-027): the mapped type must be raised at high/medium
                ok = any(e["flag_type"] == t and (e["strength"] in RAISES or (cat == "SUBJ" and e["self_report"]))
                         for e, _ in res)
                if not ok:
                    fn.append(f"nurse {cat} {exp} | {s}" + (" (low only)" if any(e["flag_type"] == t for e, _ in res) else ""))
            elif exp == "SUPPRESS":
                ok = not any((e["flag_type"] == "pre_existing" or e["id"] == "likely_alternative_cause")
                             and e["strength"] in RAISES for e, _ in res)
                if not ok:
                    fp.append(f"nurse {cat} SUPPRESS | {s} -> {[e['id'] for e, _ in res]}")
            else:
                t = vmap.get(exp[5:], exp[5:])
                ok = not any(e["flag_type"] == t and e["strength"] in RAISES for e, _ in res)
                if not ok:
                    fp.append(f"nurse {cat} {exp} | {s} -> {[e['id'] for e, _ in res if e['flag_type'] == t]}")
            n_ok += ok
            if VERBOSE or not ok:
                print(f"  {'ok ' if ok else 'BAD'} {cat:5} {exp:26} {s}  -> " + ", ".join(f"{e['id']}[{e['strength']}]" for e, _ in res))
        print(f"  nurse: {n_ok}/{n_tot} ok")
    print("\n[probes] claims-adjuster (FLAG: high/medium raised; QUIET: no high/medium)")
    a_ok = a_tot = 0
    if adj.exists():
        tree = ast.parse(adj.read_text())
        probes = next(ast.literal_eval(n.value) for n in tree.body
                      if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "PROBES" for t in n.targets))
        for exp, cat, s in probes:
            res = scan(entries, s, neg, PROBE_ACCIDENT_YEAR)
            raised = [e["id"] for e, _ in res if e["strength"] in RAISES]
            a_tot += 1
            if exp == "FLAG":
                ok = bool(raised)
                if not ok:
                    fn.append(f"adjuster {cat} | {s}" + (" (low only)" if res else ""))
            else:
                ok = not raised
                if not ok:
                    fp.append(f"adjuster QUIET {cat} | {s} -> {raised}")
            a_ok += ok
            if VERBOSE or not ok:
                print(f"  {'ok ' if ok else 'BAD'} {exp:5} {cat:12} {s}  -> " + ", ".join(f"{e['id']}[{e['strength']}]" for e, _ in res))
        print(f"  adjuster: {a_ok}/{a_tot} ok")
    print(f"\n[probes] false positives: {len(fp)} (bar ≤ 2)   false negatives: {len(fn)}")
    for x in fp:
        print("  FP " + x)
    for x in fn:
        print("  FN " + x)


    # 6. held-out probe set (evals/lexicon_heldout.jsonl): never copied into lexicon examples
    ho_ok = ho_tot = 0
    ho_bad, ho_by_group = [], {}
    ex_texts = {x.strip().lower() for e in entries for k in ("hit", "miss", "negated") for x in e.get("examples", {}).get(k, [])}
    leaked = []
    if HELDOUT.exists():
        for line in HELDOUT.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["text"].strip().lower() in ex_texts:
                leaked.append(r["text"])
            res = scan(entries, r["text"], neg, r.get("accident_year", PROBE_ACCIDENT_YEAR))
            raised = [e for e, _ in res if e["strength"] in RAISES]
            x = r["expect"]
            if x == "pre_existing":
                ok = any(e["flag_type"] == "pre_existing" for e in raised)
            elif x == "hedge":
                ok = any(e["hedge"] for e in raised)
            elif x == "attribution":
                ok = any(e["self_report"] and e["flag_type"] == "causation" for e in raised)
            elif x == "self_report_any":
                ok = any(e["self_report"] for e, _ in res)
            elif x == "quiet_pre_existing":
                ok = not any(e["flag_type"] == "pre_existing" for e in raised)
            elif x == "quiet_hedge":
                ok = not any(e["hedge"] for e in raised)
            elif x == "quiet_self_report":
                ok = not production_chip(r["text"])
            else:
                raise SystemExit(f"bad expect {x}")
            ho_tot += 1
            ho_ok += ok
            g = ho_by_group.setdefault(r["group"], [0, 0])
            g[0] += ok
            g[1] += 1
            if not ok:
                ho_bad.append(f"{r['id']} {r['group']} {x} | {r['text']} -> " + ", ".join(f"{e['id']}[{e['strength']}]" for e, _ in res))
        print(f"\n[held-out] {HELDOUT.name}: {ho_ok}/{ho_tot} = {ho_ok / max(ho_tot, 1):.0%} (bar {HELDOUT_BAR:.0%}); "
              + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in ho_by_group.items()))
        for b in ho_bad:
            print("  MISS " + b)
        for t in leaked:
            print("  LEAK (held-out sentence is a lexicon example): " + t)
        if leaked:
            errors.append(f"{len(leaked)} held-out sentences copied into lexicon examples")
    else:
        errors.append("evals/lexicon_heldout.jsonl missing")
    chip_bad = [t for t in CHIP_NO + CHIP_YES if production_chip(t)]   # D-040: the chip is cut, so every former no-chip and chip row must be chip-free
    print(f"\n[production chip] D-040 no speaker chip on {len(CHIP_NO)} former no-chip + {len(CHIP_YES)} former chip rows: {len(CHIP_NO) + len(CHIP_YES) - len(chip_bad)}/{len(CHIP_NO) + len(CHIP_YES)}")
    for t in chip_bad:
        print("  CHIP MISMATCH " + t)
    if chip_bad:
        errors.append(f"{len(chip_bad)} production chip mismatches")
    held_pass = ho_tot >= 40 and ho_ok / max(ho_tot, 1) >= HELDOUT_BAR

    if mismatch:
        print("\nappendix_c mismatches:\n  " + "\n  ".join(mismatch))
    if errors:
        print("\nERRORS:\n  " + "\n  ".join(errors))
    ok = not errors and not mismatch and not golden_fail and not mustnot_fail and len(fp) <= 2 and held_pass
    print(f"\nSUMMARY golden MUST recall {must_hit}/{must_total}, SHOULD {should_hit}/{should_total}; "
          f"must_not violations {len(mustnot_fail)}; probe FP {len(fp)}, FN {len(fn)} of {n_tot + a_tot}; held-out {ho_ok}/{ho_tot}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
