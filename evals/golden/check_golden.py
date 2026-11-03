#!/usr/bin/env python3
"""Deterministic self-check of the golden set (no LLM, no network).

Run:  python3 evals/golden/check_golden.py        (exit 0 = golden set is internally consistent)

Verifies, for every <case>.expected.json:
  * the .txt starts with "SYNTHETIC" and parses into the records the JSON declares (raw date, kind, source);
  * entries: provider == the header source label of the lowest-numbered cited record, exactly as written (D-014, R-TL-9;
    no aliases); must_contain_excerpt (string or list) verbatim in the cited records; required_terms supported by the record;
  * seeded_edits (R-RV-3): an edit expected to go to needs_review really introduces a number absent from the excerpt,
    source label and parsed date; the control edit introduces none;
  * gap_table equals real calendar arithmetic over the parsed dates of *clinical-encounter* records only
    (billing statements, phone notes and ambiguous dates are excluded) and flag == (days > 30);
  * gap flags match flagged gap rows; totals equal the sum of in_total charges; all evidence is verbatim;
  * every must_not has >= 3 bad_examples and >= 3 good_examples; for regex / structural checks BOTH sets are TESTED
    (every bad example must fire, every good example must not); judge examples are counted and checked for overlap
    (the eval runner uses them to calibrate judge #1);
  * every regex must_not does not fire on the case input itself (unless input_exempt), nor on totals.display text;
  * the 10 stress types required by CONTRACT s5 M1 are covered by the synthetic cases;
  * sample.export.expected.txt: every quote is verbatim in the record it is cited to; headings equal the record header label +
    date; summaries satisfy required_terms (summary alone) and keep self-report attribution; numbers in summaries come from the
    excerpt/label/date; the total line is exactly totals.letter_line (D-019); no regex must_not fires on the letter; the
    "flagged language" and "bills to request" sections are re-derived from sample.expected.json and must match; every must flag's
    evidence appears in the notes;
  * flag-matching reference fixtures (overlapping evidence + one-to-one assignment; K4 vs K5);
  * hallucinations.jsonl / hallucinations_controls.jsonl: counts, labels, category coverage, verbatim record_text,
    >= 10 items from synthetic cases, >= 5 paraphrase controls with token overlap < 0.8.
This checks the *golden files*, not the product. The product runner (evals/run.py) consumes them.

Regex semantics (shared with the runner): text is first stripped of double-quoted spans (verbatim excerpts); each match of
`pattern` is ignored when `unless_context` matches the up-to-80 characters immediately BEFORE the match.
"""
import datetime as dt, json, pathlib, re, sys

D = pathlib.Path(__file__).parent
errs = []


def err(case, msg):
    errs.append(f"{case}: {msg}")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def parse_txt(text):
    recs = {}
    for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', text):
        recs[int(m.group(1))] = dict(raw=m.group(2), source=m.group(3), excerpt=m.group(4))
    return recs


def strip_quotes(s):
    return re.sub(r'"[^"]*"', " ", s)


def fires_text(mn, s, strip=True):
    """Return list of non-exempt regex matches of must_not `mn` in tool-authored text `s`."""
    rx = re.compile(mn["pattern"])
    ctx = re.compile(mn["unless_context"]) if mn.get("unless_context") else None
    if strip:
        s = strip_quotes(s)
    hits = []
    for m in rx.finditer(s):
        if ctx and ctx.search(s[max(0, m.start() - 80):m.start()]):
            continue
        hits.append(m.group(0))
    return hits


def fires_struct(mn, fx):
    c = mn["check"]
    if c == "amount_value":
        return fx.get("value") in mn["values"]
    if c == "entry_date":
        return fx.get("date") in mn["dates"]
    if c == "flag_status":
        return fx.get("status") in mn["forbidden"]
    if c == "amount_count_max":
        return fx.get("amount_count", 0) > mn["max"]
    raise ValueError(c)


def span_problems(sp):
    out = []
    if "source_kind" in sp:
        out.append("source_kind not allowed on spans (D-040: no speaker label)")
    if not sp.get("attribution_any"):
        out.append("attribution_any missing")
    if re.search(r"tenderness|\bROM\b|range of motion|\bDx\b|alert and oriented|strain|x-ray|\bMRI\b|splint", sp.get("excerpt", ""), re.I):
        out.append("objective/assessment content")
    return out


def nums(x):
    return {t.replace(",", "").lstrip("$").lstrip("0") or "0" for t in re.findall(r"\$?\d[\d,]*(?:\.\d+)?", x)}


def long_date(iso):
    d = dt.date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def overlap(cand_ex, gold_ex):
    """Candidate excerpt must CONTAIN the golden span, or be a fragment of it covering >= 50% of its length."""
    c, g = norm(cand_ex).lower(), norm(gold_ex).lower()
    return bool(c) and bool(g) and (g in c or (c in g and len(c) >= 0.5 * len(g)))


def flag_matches(g, c):
    """Reference matcher (README 'Flags'): same type; cites; gap dates; and, on every record in cite.all, the candidate's
    evidence must OVERLAP (normalized substring either way) a golden evidence item of field excerpt/source on that record."""
    if g["type"] != c["type"]:
        return False
    recs_c = {e["record_no"] for e in c["evidence"]}
    if not all(r in recs_c for r in g["cite"]["all"]):
        return False
    if g["cite"]["any"] and not any(r in recs_c for r in g["cite"]["any"]):
        return False
    if g["type"] == "gap":
        return (g["from_date"], g["to_date"], g["days"]) == (c.get("from_date"), c.get("to_date"), c.get("days"))
    for r in g["cite"]["all"]:
        gold = [e["excerpt"] for e in g["evidence"] if e["record_no"] == r and e.get("field", "excerpt") in ("excerpt", "source")]
        if gold and not any(overlap(ce["excerpt"], ge) for ce in c["evidence"] if ce["record_no"] == r for ge in gold):
            return False
    return True


def assign(golden, cands):
    """One-to-one assignment (each candidate flag satisfies at most ONE golden flag): maximum bipartite matching."""
    uniq, seen_ = [], set()
    for c in cands:      # identical (type, evidence) candidates collapse into one
        k = (c["type"], tuple(sorted((e["record_no"], norm(e["excerpt"])) for e in c["evidence"])), c.get("from_date"), c.get("to_date"))
        if k not in seen_:
            seen_.add(k); uniq.append(c)
    cands = uniq
    owner = {}

    def try_(gi, seen):
        for ci, c in enumerate(cands):
            if ci in seen or not flag_matches(golden[gi], c):
                continue
            seen.add(ci)
            if ci not in owner or try_(owner[ci], seen):
                owner[ci] = gi
                return True
        return False

    for gi in range(len(golden)):
        try_(gi, set())
    return {golden[gi]["id"] for gi in owner.values()}


ENTRY_KEYS = {"id", "record_nos", "date", "date_status", "encounter", "provider", "must_contain_excerpt", "required_terms",
              "self_report_spans", "note", "needs_review", "date_candidates"}

# a mislabelled span MUST be rejected (proves the span check is live)
if not span_problems(dict(excerpt="Alert and oriented", source_kind="patient_report", attribution_any=["x"])) or \
        not span_problems(dict(excerpt="Tenderness over the anterior shoulder", attribution_any=["x"])) or \
        span_problems(dict(excerpt="C/O neck pain", attribution_any=["C/O"])):
    errs.append("span_problems self-test failed: a mislabelled span was accepted or a good one rejected")

COVER = {
    "date-format variety": "date_format_variety", "29/30/31-day boundaries": "gap_boundary_29_30_31",
    "rate not a charge": "rate_not_charge", "OCR noise": "ocr_noise_amount", "no amounts": "no_amounts",
    "duplicate records": "duplicate_records", "provider-name conflict": "provider_name_conflict",
    "subtle pre-existing": "subtle_pre_existing", "prompt injection": "prompt_injection",
    "diagnosis temptation": "diagnosis_inference_trap", "non-visit record hides gap": "non_encounter_record_hides_gap",
}

cases = sorted(D.glob("*.expected.json"))
synthetic_tags = set()
all_txt = {}
sample_ex = None
for jp in cases:
    cid = jp.name.replace(".expected.json", "")
    ex = json.loads(jp.read_text())
    text = (D / ex["input_file"]).read_text()
    all_txt[cid] = text
    if cid == "sample":
        sample_ex = ex
    if not text.startswith("SYNTHETIC"):
        err(cid, "input text must start with SYNTHETIC")
    if cid.startswith("case_") and not text.startswith("SYNTHETIC — invented for evaluation; not real patient data\n"):
        err(cid, "synthetic case must start with the exact SYNTHETIC label line")
    if ex.get("synthetic") is not True:
        err(cid, "synthetic flag must be true")
    if cid.startswith("case_"):
        synthetic_tags.update(ex["stress_types"])
    recs = parse_txt(text)
    if sorted(recs) != [r["record_no"] for r in ex["records"]]:
        err(cid, f"record numbers differ: txt {sorted(recs)}")
    for r in ex["records"]:
        t = recs.get(r["record_no"])
        if not t:
            continue
        if t["raw"] != r["raw_date"] or t["source"] != r["source"]:
            err(cid, f"record {r['record_no']} raw date/source mismatch")
        if r["kind"] not in ("encounter", "billing_statement", "phone_note"):
            err(cid, f"record {r['record_no']}: bad kind")
        if r["date"]:
            try:
                dt.date.fromisoformat(r["date"])
            except ValueError:
                err(cid, f"bad ISO date {r['date']}")

    def ex_of(n):
        return recs[n]["excerpt"]

    # ---- entries
    for e in ex["entries"]:
        unknown = set(e) - ENTRY_KEYS
        if unknown:
            err(cid, f"{e['id']}: unknown entry keys {sorted(unknown)} (a renamed key would silently disable a check)")
        musts = e["must_contain_excerpt"] if isinstance(e["must_contain_excerpt"], list) else [e["must_contain_excerpt"]]
        for m in musts:
            if not any(m in ex_of(n) for n in e["record_nos"]):
                err(cid, f"{e['id']}: must_contain_excerpt not verbatim in records {e['record_nos']}: {m[:40]}")
        hay = norm(" ".join(ex_of(n) + " " + recs[n]["source"] for n in e["record_nos"])).lower()
        for term in e["required_terms"]:   # D-022: checked against the SUMMARY alone; here: must be grounded in the record
            alts = term if isinstance(term, list) else [term]
            if not any(norm(a).lower() in hay for a in alts):
                err(cid, f"{e['id']}: required_term {term} not supported by cited records (would be an invented requirement)")
        for sp in e.get("self_report_spans", []):
            if not any(sp["excerpt"] in ex_of(n) for n in e["record_nos"]):
                err(cid, f"{e['id']}: self_report span not verbatim: {sp['excerpt'][:40]}")
            for pr in span_problems(sp):
                err(cid, f"{e['id']}: self_report span: {pr}: {sp['excerpt'][:50]}")
        if "source_kind" in e:
            err(cid, f"{e['id']}: entry-level source_kind removed (D-022); tag spans")
        rs = [next(r for r in ex["records"] if r["record_no"] == n) for n in e["record_nos"]]
        if "provider_aliases" in e:
            err(cid, f"{e['id']}: provider_aliases are not allowed (D-014); provider is the header label")
        if e["provider"] != rs[0]["source"]:
            err(cid, f"{e['id']}: provider {e['provider']!r} != header label {rs[0]['source']!r}")
        for r_ in rs[1:]:
            if norm(r_["source"]).lower() != norm(rs[0]["source"]).lower():
                err(cid, f"{e['id']}: merged records have different provider labels")
        if len({r["date"] for r in rs}) != 1 or e["date"] != rs[0]["date"]:
            err(cid, f"{e['id']}: merged records disagree on date, or date mismatch")
        if e["encounter"] != (rs[0]["kind"] == "encounter"):
            err(cid, f"{e['id']}: encounter flag disagrees with record kind")
        if e["date_status"] == "parsed" and not e["date"]:
            err(cid, f"{e['id']}: parsed entry without a date")
    if ex["expected_entry_count"] != len(ex["entries"]):
        err(cid, "expected_entry_count != len(entries)")
    if sorted(n for e in ex["entries"] for n in e["record_nos"]) != sorted(recs):
        err(cid, "entries do not cover every input record exactly once")

    # ---- gap table: encounters only
    by = {}
    excluded = []
    for r in ex["records"]:
        if r["date"] and r["kind"] == "encounter":
            by.setdefault(r["date"], []).append(r["record_no"])
        else:
            excluded.append(r["record_no"])
    if sorted(excluded) != sorted(ex["gap_excluded_records"]):
        err(cid, f"gap_excluded_records {ex['gap_excluded_records']} != non-encounter/ambiguous records {sorted(excluded)}")
    ds = sorted(by)
    if len(ex["gap_table"]) != max(len(ds) - 1, 0):
        err(cid, "gap_table length wrong")
    for g, (a, b) in zip(ex["gap_table"], zip(ds, ds[1:])):
        days = (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days
        if (g["from_date"], g["to_date"], g["days"]) != (a, b, days):
            err(cid, f"gap row {a}->{b}: golden {g['days']} vs calendar {days}")
        if g["flag"] != (days > 30):
            err(cid, f"gap row {a}->{b}: flag should be {days > 30}")
        if g["from_records"] != by[a] or g["to_records"] != by[b]:
            err(cid, f"gap row {a}->{b}: record lists wrong")
    flagged = {(g["from_date"], g["to_date"], g["days"]) for g in ex["gap_table"] if g["flag"]}
    gap_flags = {(f["from_date"], f["to_date"], f["days"]) for f in ex["flags"] if f["type"] == "gap"}
    if flagged != gap_flags:
        err(cid, f"gap flags {sorted(gap_flags)} != flagged rows {sorted(flagged)}")

    # ---- amounts + totals
    ids = {a["id"] for a in ex["amounts"]}
    for a in ex["amounts"]:
        if a["excerpt"] not in ex_of(a["record_no"]):
            err(cid, f"{a['id']}: excerpt not verbatim")
        if a["class"] not in ("charge", "rate", "estimate", "unclear", "damages"):
            err(cid, f"{a['id']}: bad class")
        if a["class"] != "charge" and a["in_total"]:
            err(cid, f"{a['id']}: only charges may be in_total")
        if a["class"] in ("unclear", "damages") and a["value"] is not None:
            err(cid, f"{a['id']}: unclear/damages must have value null")
        if a.get("service_date_in_excerpt") and a["service_date_in_excerpt"] not in a["excerpt"]:
            err(cid, f"{a['id']}: service_date_in_excerpt not verbatim in the excerpt")
        if a["class"] != "damages" and a["raw"] not in a["excerpt"]:
            err(cid, f"{a['id']}: raw not inside excerpt")
    t = ex["totals"]
    s = sum(a["value"] for a in ex["amounts"] if a["in_total"])
    if t["explicit_charges_total"] != s:
        err(cid, f"totals {t['explicit_charges_total']} != sum {s}")
    if set(t["counted_amount_ids"]) != {a["id"] for a in ex["amounts"] if a["in_total"]} or not set(t["counted_amount_ids"]) <= ids:
        err(cid, "counted_amount_ids mismatch")
    if "display" in t:
        err(cid, "totals.display removed: use letter_line / ui_line / notes_lines (one canonical string per surface)")
    if t["status"] == "none_found":
        if t["letter_line"] is not None:
            err(cid, "no-charge case must have letter_line null")
    elif t["letter_line"] != f"Billed charges accepted from these records: ${t['explicit_charges_total']:,.2f}":
        err(cid, f"letter_line must be exactly 'Billed charges accepted from these records: $X' (D-019): {t['letter_line']!r}")
    if t["status"] != "none_found" and t["ui_line"] != f"Accepted charges: ${t['explicit_charges_total']:,.2f}":
        err(cid, "ui_line mismatch")
    dollar = [a for a in ex["amounts"] if a["class"] != "damages"]
    if t["amounts_found"] not in (len(dollar), sum(1 for a in dollar if a["required"])):
        err(cid, "amounts_found inconsistent")

    # ---- flags / tolerated / warnings evidence
    for f in ex["flags"] + ex["tolerated"] + ex["record_warnings"]:
        for ev in f.get("evidence", []):
            fld = ev.get("field", "excerpt")
            if fld == "excerpt":
                ok = ev["excerpt"] in ex_of(ev["record_no"])
            elif fld == "source":
                ok = ev["excerpt"] in recs[ev["record_no"]]["source"]
            elif fld == "date":
                ok = ev["excerpt"] == next(r["date"] for r in ex["records"] if r["record_no"] == ev["record_no"])
            else:
                ok = False
            if not ok:
                err(cid, f"{f['id']}: evidence not verbatim ({fld}) in record {ev['record_no']}: {ev['excerpt'][:40]}")
        if "cite" in f:
            for n in f["cite"]["all"] + f["cite"]["any"]:
                if n not in recs:
                    err(cid, f"{f['id']}: cites unknown record {n}")
    for w in ex["record_warnings"]:
        if w.get("type") != "record_warning" or w.get("category") not in ("injection_suspected", "date_ambiguous"):
            err(cid, f"{w['id']}: record_warning vocabulary (ADR-013): type record_warning + category injection_suspected|date_ambiguous")
        hay_w = next(r["raw_date"] for r in ex["records"] if r["record_no"] == w["record_no"]) if w.get("field") == "date" else ex_of(w["record_no"])
        if w["excerpt"] not in hay_w:
            err(cid, f"{w['id']}: warning excerpt not verbatim")
    for f in ex["flags"]:
        if f["type"] not in ("gap", "conflict", "pre_existing", "causation") or f["level"] not in ("must", "should"):
            err(cid, f"{f['id']}: bad type/level")

    # ---- seeded edits
    for se in ex.get("seeded_edits", []):
        rr = next(r for r in ex["records"] if r["record_no"] == se["record_no"])
        allowed = nums(ex_of(se["record_no"]) + " " + rr["source"] + " " + (rr["date"] or "") + " " + rr["raw_date"])
        new = nums(se["new_summary"]) - allowed
        if se["kind"] == "number":
            if not new or not set(se["introduced"]) <= new:
                err(cid, f"{se['id']}: edit does not introduce the declared number(s) {se['introduced']} (introduces {sorted(new)})")
            if se["expected_state"] != "needs_review":
                err(cid, f"{se['id']}: number-adding edit must expect needs_review")
        elif se["kind"] == "control":
            if new:
                err(cid, f"{se['id']}: control edit introduces numbers {sorted(new)}")
        elif se["kind"] == "judge_masked":
            if new or any(w in (ex_of(se["record_no"]) + rr["source"]) for w in se["introduced"]):
                err(cid, f"{se['id']}: masked edit must reuse digits already allowed (code check blind) yet change the value")
        elif se["kind"] == "judge":
            if new or any(w in ex_of(se["record_no"]).lower() for w in se["introduced"]):
                err(cid, f"{se['id']}: judge edit must introduce a term absent from the excerpt and no new number")
    if cid == "sample" and {x["kind"] for x in ex.get("seeded_edits", [])} != {"number", "judge", "judge_masked", "control"}:
        err(cid, "sample needs seeded edits of kinds number, judge, judge_masked and control")

    # ---- must_not: structure + examples tested both ways
    for m in ex["must_not"]:
        mid = f"{cid}/{m['id']}"
        bad, good = m.get("bad_examples", []), m.get("good_examples", [])
        if len(bad) < 3 or len(good) < 3:
            err(cid, f"{m['id']}: needs >= 3 bad_examples and >= 3 good_examples")
            continue
        if m["check"] == "regex":
            try:
                re.compile(m["pattern"])
                if m.get("unless_context"):
                    re.compile(m["unless_context"])
            except re.error as e:
                err(cid, f"{m['id']}: regex does not compile: {e}")
                continue
            for b in bad:
                if not fires_text(m, b):
                    err(cid, f"{m['id']}: bad example NOT caught: {b!r}")
            for g in good:
                h = fires_text(m, g)
                if h:
                    err(cid, f"{m['id']}: good example wrongly fires {h}: {g!r}")
            if not m.get("input_exempt"):
                h = fires_text(m, text, strip=False)
                if h:
                    err(cid, f"{m['id']}: regex fires on the input itself: {h}")
            for surf in [ex["totals"]["letter_line"], ex["totals"]["ui_line"]] + ex["totals"]["notes_lines"]:
                h = fires_text(m, surf) if surf else []
                if h:
                    err(cid, f"{m['id']}: regex fires on golden totals string {surf!r}: {h}")
        elif m["check"] == "judge":
            if set(bad) & set(good):
                err(cid, f"{m['id']}: judge examples overlap")
        elif m["check"] in ("amount_value", "entry_date", "flag_status", "amount_count_max"):
            for b in bad:
                if not fires_struct(m, b):
                    err(cid, f"{m['id']}: bad fixture NOT caught: {b}")
            for g in good:
                if fires_struct(m, g):
                    err(cid, f"{m['id']}: good fixture wrongly fires: {g}")
        else:
            err(cid, f"{m['id']}: unknown check type {m['check']}")

missing = [k for k, tag in COVER.items() if tag not in synthetic_tags]
if missing:
    errs.append(f"stress types not covered by synthetic cases: {missing}")
if len([p for p in cases if p.name.startswith("case_")]) < 6:
    errs.append("need >= 6 synthetic cases")

# ---- flag-matching reference fixtures (README 'Flags': overlapping evidence + one-to-one assignment)
gflags = sample_ex["flags"]
def cand(typ, ev, **kw):
    d = dict(type=typ, evidence=[dict(record_no=r, excerpt=x) for r, x in ev]); d.update(kw); return d
K4c = cand("causation", [(7, "New onset pain")])
K5c = cand("causation", [(7, "Date of accident per intake form: 2026-01-19.")])
FIX = [
    ("one record-7 causation candidate on 'New onset' satisfies K4 only, not K5", [K4c], {"K4"}),
    ("one candidate on the intake-date line satisfies K5 only", [K5c], {"K5"}),
    ("two distinct candidates satisfy both", [K4c, K5c], {"K4", "K5"}),
    ("one candidate carrying both spans can satisfy at most ONE golden flag", [cand("causation", [(7, "New onset pain"), (7, "Date of accident per intake form: 2026-01-19.")])], None),
    ("a gap or conflict flag never satisfies a causation golden flag",
     [cand("gap", [(6, "Discharged from PT after two missed appointments"), (7, "New onset pain")], from_date="2026-03-06", to_date="2026-05-18", days=73),
      cand("conflict", [(7, "Date of accident per intake form: 2026-01-19."), (1, "rear-ended at approx. 35 mph")])], {"G1", "C1"}),
    ("two identical whole-record-7 causation candidates collapse and earn one golden flag, not both",
     [cand("causation", [(7, "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.")])] * 2, None),
    ("a one-word fragment earns nothing", [cand("causation", [(7, "pain")])], set()),
    ("wrong gap dates do not match G1", [cand("gap", [(6, "x"), (7, "y")], from_date="2026-02-20", to_date="2026-03-06", days=14)], set()),
]
for desc, cands_, want in FIX:
    got = assign(gflags, cands_)
    if want is None:
        if len(got) != 1 or not got <= {"K4", "K5"}:
            errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}")
    elif got != want:
        errs.append(f"flag-matching fixture failed ({desc}): got {sorted(got)}, want {sorted(want)}")

# ---- sample.export.expected.txt
ep = D / "sample.export.expected.txt"
etxt = ep.read_text()
m_l, m_n = "=== LETTER_TEXT", "=== INTERNAL_NOTES_TEXT"
if not (etxt.startswith(m_l) and m_n in etxt):
    errs.append("sample.export.expected.txt: missing LETTER_TEXT / INTERNAL_NOTES_TEXT delimiters")
else:
    letter = etxt.split(m_n)[0].split("\n", 1)[1]
    notes = etxt.split(m_n)[1].split("\n", 1)[1]
    srecs = parse_txt(all_txt["sample"])
    srows = {r["record_no"]: r for r in sample_ex["records"]}
    sample_norm = norm(all_txt["sample"])
    # (1) every quoted span in either block is verbatim in the record it is cited to
    for m in re.finditer(r'[Rr]ecord (\d+) \(([^)]*)\)', notes):
        n = int(m.group(1)); r = srows.get(n)
        want = f"{r['source']}, {long_date(r['date'])}" if r else None
        if m.group(2).replace(", dated ", ", ") != want:
            errs.append(f"export notes: 'record {n} ({m.group(2)})' != '{want}'")
        tail = notes[m.end(): m.end() + 6]
        q = re.match(r'[:\s]{0,3}"([^"]+)"', tail)
        if q and norm(q.group(1)) not in norm(srecs[n]["excerpt"]):
            errs.append(f"export notes: quote cited to record {n} is not in record {n}: {q.group(1)[:50]}")
    # (2) letter entries
    lt = letter.split("BILLED CHARGES")
    entry_blocks = [b for b in lt[0].strip().split("\n\n")[1:] if b.strip()]
    letter_quote = {}
    sample_entries = {e["record_nos"][0]: e for e in sample_ex["entries"]}
    for blk in entry_blocks:
        ln = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d{1,2}, \d{4}) — (.+)$", ln[0])
        if not m or len(ln) != 3:
            errs.append(f"export letter: malformed entry block: {blk[:60]}")
            continue
        recno = [n for n, r in srows.items() if r["source"] == m.group(2) and long_date(r["date"]) == m.group(1)]
        if len(recno) != 1:
            errs.append(f"export letter: heading does not match exactly one record header label+date: {ln[0]}")
            continue
        n = recno[0]
        q = re.fullmatch(r'Source \[Ex\. __ / Bates __\]: "(.+)"', ln[2])
        if not q or norm(q.group(1)) not in norm(srecs[n]["excerpt"]):
            errs.append(f"export letter: Source quote for record {n} is not verbatim in record {n}")
            continue
        letter_quote[n] = q.group(1)
        summ = ln[1]
        allowed = nums(q.group(1) + " " + srows[n]["source"] + " " + srows[n]["date"] + " " + long_date(srows[n]["date"]))
        if nums(summ) - allowed:
            errs.append(f"export letter: summary for record {n} has numbers not in excerpt/label/date: {sorted(nums(summ) - allowed)}")
        e = sample_entries[n]
        for term in e["required_terms"]:
            alts = term if isinstance(term, list) else [term]
            if not any(a.lower() in summ.lower() for a in alts):
                errs.append(f"export letter: summary for record {n} fails required_terms {term} (D-022: summary alone)")
        for sp in e.get("self_report_spans", []):
            if not any(a.lower() in summ.lower() for a in sp["attribution_any"]):
                errs.append(f"export letter: summary for record {n} drops the self-report attribution for {sp['excerpt'][:30]!r}")
    if sorted(letter_quote) != sorted(srows):
        errs.append("export letter: entries missing for some records")
    # (3) charges and the total line (D-019)
    tot = sample_ex["totals"]["letter_line"]
    if lt[1].count("Billed charges accepted from these records") != 1 or tot not in lt[1].split("\n"):
        errs.append(f"export letter: total line must be exactly {tot!r} on its own line (D-019)")
    charge_lines = re.findall(r"^(.+?), (?:date of service \[_{10}\] \((?:record|statement) dated )?([A-Z][a-z]+ \d+, \d{4})\)?: \$([\d,]+\.\d{2})\nSource \[Ex\. __ / Bates __\]: \"([^\"]+)\"", lt[1], re.M)
    paid = {a["record_no"]: a for a in sample_ex["amounts"] if a["in_total"]}
    got = set()
    for label, d_, val, q in charge_lines:
        hit = [n for n, r in srows.items() if r["source"] == label and long_date(r["date"]) == d_ and n in paid]
        if len(hit) != 1 or float(val.replace(",", "")) != paid[hit[0]]["value"] or q not in srecs[hit[0]]["excerpt"] or paid[hit[0]]["excerpt"] not in q:
            errs.append(f"export letter: charge line does not match golden amounts: {label} {val}")
        else:
            got.add(hit[0])
    if got != set(paid):
        errs.append("export letter: charge lines do not cover exactly the in_total amounts")
    lq = strip_quotes(letter)
    if ".." in letter:
        errs.append("export letter: contains a '..' run (R-EX-6)")
    for amt in re.findall(r"\$[\d,]+(?:\.\d+)?", lq):
        if not re.fullmatch(r"\$[\d,]+\.\d{2}", amt):
            errs.append(f"export letter: amount {amt} not in $1,234.00 form")
    if re.search(r"visit count|\brate\b|supplemented|excludes", lq, re.I):
        errs.append("export letter: non-charge reason / parenthetical leaked (D-019, R-EX-8)")
    if "FLAGS ACCEPTED" in letter or "INTERNAL REVIEW NOTES" in letter:
        errs.append("export letter: flag text leaked into the letter block")
    for m in sample_ex["must_not"]:
        if m["check"] == "regex" and fires_text(m, letter):
            errs.append(f"export letter fires sample {m['id']}: {fires_text(m, letter)}")
    # (4) derived notes sections: flagged language quoted in the letter, bills to request
    def lab(f):
        if f["type"] == "gap": return "gap"
        if f["type"] == "conflict": return {"accident_date": "conflict, accident date", "treatment_plan": "conflict, pt plan"}[f["subtype"]]
        if f["type"] == "pre_existing": return "prior condition"
        return "causation language"
    derived = {}
    for n, q in letter_quote.items():
        ls = {lab(f) for f in sample_ex["flags"] for ev in f["evidence"]
              if ev["record_no"] == n and ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) in norm(q)}
        if ls:
            derived[n] = ls
    sec = re.search(r"FLAGGED LANGUAGE QUOTED IN THE LETTER[^\n]*\n(.*?)\n\n", notes, re.S)
    exported = {}
    order = []
    for line in (sec.group(1).split("\n") if sec else []):
        m = re.match(r'- Record (\d+) \([^)]*\): "[^"]+" (.+)\.$', line)
        if not m:
            errs.append(f"export notes: malformed flagged-language line: {line[:60]}")
            continue
        order.append(int(m.group(1)))
        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
    if exported != derived or order != sorted(order):
        errs.append(f"export notes: flagged-language section != derived from golden flags (D-012/R-EX-4). derived={derived} exported={exported}")
    head = lambda lbl: lbl.split(",")[0]
    charged = {head(srows[n]["source"]) for n in paid}
    want_bills, seen = [], set()
    for n in sorted(srows):
        h = head(srows[n]["source"])
        if h not in charged and h not in seen:
            seen.add(h); want_bills.append(h)
    nontot = {head(srows[a["record_no"]]["source"]) for a in sample_ex["amounts"] if a["class"] in ("rate", "estimate", "unclear")}
    sb = re.search(r"BILLS TO REQUEST[^\n]*\n- (.+)\.\n", notes)
    got_bills = [re.sub(r" \(itemized ledger\)$", "", x.strip()) for x in sb.group(1).split(";")] if sb else []
    if got_bills != want_bills:
        errs.append(f"export notes: bills to request {got_bills} != derived (label up to first comma, chronological) {want_bills}")
    for h in nontot:
        if f"{h} (itemized ledger)" not in (sb.group(1) if sb else ""):
            errs.append(f"export notes: {h} should carry '(itemized ledger)'")
    # (5) every must flag has its evidence in ITS OWN bullet of FLAGS ACCEPTED (K5 cannot hide inside C1's bullet)
    bullets = {l.split(":")[0].lower(): l for l in notes.split("\n") if l.startswith("- ")}
    def bullet_for(f):
        key = {"gap": "- gap", "pre_existing": "- prior condition", "causation": "- causation language"}.get(f["type"])
        if f["type"] == "conflict":
            key = "- conflict, accident date" if f["subtype"] == "accident_date" else "- conflict, pt plan"
        return bullets.get(key, "")
    for f in sample_ex["flags"]:
        if f["level"] != "must":
            continue
        b = bullet_for(f)
        if not b:
            errs.append(f"export notes: no FLAGS ACCEPTED bullet for {f['id']}")
        elif f["type"] == "gap":
            if f"{f['days']} days" not in b or long_date(f["from_date"]) not in b or long_date(f["to_date"]) not in b:
                errs.append(f"export notes: gap bullet lacks {f['id']} days/dates")
        elif f["type"] in ("causation", "pre_existing") or f.get("subtype") == "treatment_plan":
            for ev in f["evidence"]:
                if ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) not in norm(b):
                    errs.append(f"export notes: must flag {f['id']} evidence missing from its bullet: {ev['excerpt'][:50]}")
        else:   # accident-date conflict (R-FL-2/R-EX-4): BOTH sides quoted, no choice made, no computed delay
            for ev in f["evidence"]:
                if ev.get("field", "excerpt") == "excerpt" and norm(ev["excerpt"]) not in norm(b):
                    errs.append(f"export notes: {f['id']} bullet must quote both sides; missing: {ev['excerpt'][:50]}")
            if "does not choose" not in b or not all(f"ecord {n}" in b for n in (1, 2, 7)):
                errs.append(f"export notes: {f['id']} bullet must cite records 1, 2, 7 and say the tool does not choose between the dates")
            if re.search(r"\bdelay\w*|\d+ days|months? after", b, re.I):
                errs.append(f"export notes: {f['id']} bullet computes a delay (D-017)")
    first = notes.strip().split("\n")
    if first[2] != "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0." or "Pending items" in notes:
        errs.append("export notes: AI-assistance line must be the R-EX-4(1) text with 'Items not reviewed: N.' and no 'Pending items' line")
    if "FLAGS ACCEPTED" not in notes or "AMOUNTS NOT TOTALED" not in notes:
        errs.append("export notes: block incomplete")

# ---- hallucination set
all_excerpts = []
for cid, tx in all_txt.items():
    for n, r in parse_txt(tx).items():
        all_excerpts.append((cid, r["excerpt"]))
items = [json.loads(l) for l in (D / "hallucinations.jsonl").read_text().splitlines() if l.strip()]
if len(items) < 30:
    errs.append(f"hallucinations.jsonl has {len(items)} items, need >= 30 (20 original + >= 10 from synthetic cases)")
REQ_CAT = {"wrong_laterality", "wrong_level", "severity_upgrade", "subjective_as_objective", "negation_flipped", "causation",
           "hedge_removed", "invented_diagnosis", "invented_provider", "merged_dates", "negative_study_flipped",
           "wrong_provider", "recommended_as_performed", "temporal_to_causal", "approximation_dropped", "abbreviation_misexpanded"}
miss = REQ_CAT - {i["category"] for i in items}
if miss:
    errs.append(f"hallucination categories missing: {sorted(miss)}")
synth_items = 0
for it in items:
    for k in ("record_text", "candidate_summary", "why_unsupported", "category"):
        if not it.get(k):
            errs.append(f"hallucination {it.get('id')}: missing {k}")
    if it.get("synthetic") is not True:
        errs.append(f"hallucination {it['id']}: synthetic:true missing")
    if it["candidate_summary"] in it["record_text"]:
        errs.append(f"hallucination {it['id']}: candidate is a verbatim copy of the record")
    srcs = set()
    for line in it["record_text"].split("\n"):
        m = re.match(r'Record \d+ \| [^|]+ \| [^|]+ \| "(.*)"$', line)
        found = [c for c, e in all_excerpts if e == m.group(1)] if m else []
        if not found:
            errs.append(f"hallucination {it['id']}: record_text line not verbatim in a golden .txt")
        srcs.update(found)
    if any(s.startswith("case_") for s in srcs):
        synth_items += 1
if synth_items < 10:
    errs.append(f"only {synth_items} hallucination items come from synthetic cases, need >= 10")
if any(i["id"] == "H12" and i["category"] != "negation_flipped" for i in items):
    errs.append("H12 must be labeled negation_flipped")

ctrls = [json.loads(l) for l in (D / "hallucinations_controls.jsonl").read_text().splitlines() if l.strip()]
para = 0
for c in ctrls:
    if not (c["record_text"] and c["candidate_summary"]) or c.get("synthetic") is not True or c.get("supported") is not True:
        errs.append(f"control {c.get('id')} incomplete")
    if re.search(r"\b(he|she|his|her|him)\b", c["candidate_summary"], re.I) and not re.search(r"\b(he|she|his|her)\b", c["record_text"], re.I):
        errs.append(f"control {c['id']} invents the patient's sex")
    rt = set(re.findall(r"[a-z0-9$%/.,-]+", c["record_text"].lower()))
    ct = re.findall(r"[a-z0-9$%/.,-]+", c["candidate_summary"].lower())
    overlap = sum(1 for w in ct if w in rt) / max(len(ct), 1)
    if overlap < 0.8:
        para += 1
if len(ctrls) < 10 or para < 5:
    errs.append(f"controls: need >= 10 items with >= 5 paraphrases (overlap < 0.8); have {len(ctrls)} / {para}")

if errs:
    print("GOLDEN CHECK FAILED")
    for e in errs:
        print(" -", e)
    sys.exit(1)
n_must = sum(len(json.loads(p.read_text())["must_not"]) for p in cases)
print(f"golden OK: {len(cases)} cases ({len(cases) - 1} synthetic), {n_must} must_nots with tested examples, "
      f"{len(items)} hallucination items ({synth_items} synthetic-sourced), {len(ctrls)} controls ({para} paraphrase), all stress types covered")
