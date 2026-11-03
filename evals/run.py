"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
    python -m evals.run --write-calibration
                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
    python -m evals.run --record-latest evals/reports/<ts>.md
                                         no run: point latest.json at an existing dated report, values parsed from it, provenance recorded (T-045 r2).
                                         A fixture run never replaces a live ship_bar_met latest.json (it writes latest.fixture.json).

Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
NOT_MEASURED = {"value": None, "status": "not_measured"}

THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
              "hallucination_catch_rate": 0.95, "unsupported_count_3run": 0, "determinism_3run": 1.0}
RIDS = {"grounding_rate": ["R-TL-2", "R-TL-9", "R-FL-5", "R-EX-2"], "entry_recall": ["R-TL-1", "R-TL-7"], "amount_recall": ["R-CH-1"],
        "flag_precision": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"], "flag_recall": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"],
        "hallucination_catch_rate": ["R-TL-4", "R-TL-10"], "unsupported_count_3run": ["R-TL-4", "R-CH-7"], "determinism_3run": ["R-CO-7"],
        "lexicon_recall_must_flags": ["R-FL-3", "R-RV-6"], "golden_must_not_hits": ["R-CO-3"], "case_07_total_420": ["R-RV-6"]}
FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")


# ---------------------------------------------------------------- helpers
def rn(rid):
    """'r12' -> 12 (record id to record number); ints pass through."""
    if isinstance(rid, int):
        return rid
    m = re.search(r"\d+", str(rid))
    return int(m.group()) if m else None


def low(s):
    return norm(s).lower()


def ratio(num, den):
    return None if den == 0 else num / den


def golden_cases():
    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]


# The eval's inputs (T-101 r2): the code, prompts, golden set and fixtures a number is computed from. evals/reports is output, never input.
GIT_INPUT_PATHS = ("app", "app/llm/prompts", "evals", "tests/fixtures", ":(exclude)evals/reports")


def git_source(root=ROOT):
    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD and no untracked file sits under GIT_INPUT_PATHS, 'tree': HEAD^{tree},
    'dirty': the porcelain lines that make it dirty}; Nones when git is unavailable. A calibration file is only traceable when it was produced from a
    clean tree (T-090 r2: generate in a clean worktree of HEAD). Untracked files outside the inputs (e.g. a scratch file at the repo root) do not count."""
    import subprocess

    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=20, check=True).stdout
    try:
        head = git("rev-parse", "HEAD").strip()
        tree = git("rev-parse", "HEAD^{tree}").strip()
        tracked = [l for l in git("status", "--porcelain", "--untracked-files=no", "--", ".", ":(exclude)evals/reports").splitlines() if l.strip()]      # a run rewrites evals/reports/latest.json: output, not input, so the next run of the same commit is still clean
        untracked = [l for l in git("status", "--porcelain", "--untracked-files=all", "--", *GIT_INPUT_PATHS).splitlines() if l.startswith("?? ")]
    except (OSError, subprocess.SubprocessError):
        return {"commit": None, "clean": None, "tree": None, "dirty": []}
    dirty = tracked + untracked
    return {"commit": head, "clean": not dirty, "tree": tree, "dirty": dirty}


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def hashes(root=ROOT):
    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
    out = {}
    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
        out[p.relative_to(root).as_posix()] = sha256_file(p)
    lex = root / "app" / "llm" / "lexicon.yaml"
    if lex.exists():
        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
    return out


def split_regex_text(s):
    return re.sub(r'"[^"]*"', " ", s or "")


def regex_hits(mn, text):
    """Golden must_not regex semantics (README): strip double-quoted spans, ignore a match when unless_context matches the 80 chars before it."""
    s = split_regex_text(text)
    rx = re.compile(mn["pattern"])
    ctx = re.compile(mn["unless_context"]) if mn.get("unless_context") else None
    return [m.group(0) for m in rx.finditer(s) if not (ctx and ctx.search(s[max(0, m.start() - 80):m.start()]))]


# ---------------------------------------------------------------- per-case scoring (pure; tested with fake pipeline output)
def product_entries(out):
    return list(out.get("entries") or []) + list(out.get("undated_entries") or [])


def entry_found(g, prod):
    """Return (found, why_not) for golden entry g against the product's entries (README 'Entries')."""
    want = set(g["record_nos"])
    why = "no product entry covers the records"
    for e in prod:
        rec = {rn(r) for r in e.get("record_ids", [])}
        if not want <= rec:
            continue
        why = "date differs"
        undated = e.get("date") in (None, "") or e.get("date_status") in ("ambiguous", "missing")
        if (g["date"] is None) != undated or (g["date"] is not None and e.get("date") != g["date"]):
            continue
        why = "provider differs"
        if norm(e.get("provider")) != norm(g["provider"]):
            continue
        why = "excerpt misses must_contain_excerpt"
        need = g["must_contain_excerpt"] if isinstance(g["must_contain_excerpt"], list) else [g["must_contain_excerpt"]]
        if not all(low(x) in low(e.get("excerpt")) for x in need):
            continue
        why = "summary misses required_terms"
        summ = low(e.get("summary"))
        if not all((any(low(t) in summ for t in term) if isinstance(term, list) else low(term) in summ) for term in g.get("required_terms", [])):
            continue
        why = "SUMMARY_DROPS_QUALIFIER"
        if "SUMMARY_DROPS_QUALIFIER" in (e.get("reasons") or []):
            continue
        if not all(any(low(a) in summ for a in sp["attribution_any"]) for sp in g.get("self_report_spans", [])):
            continue
        return True, None
    return False, why


def score_entries(exp, out):
    prod = product_entries(out)
    found, misses = 0, []
    for g in exp["entries"]:
        ok, why = entry_found(g, prod)
        found += ok
        if not ok:
            misses.append({"entry": g["id"], "why": why})
    return {"found": found, "total": len(exp["entries"]), "misses": misses,
            "entry_count": len(prod), "expected_entry_count": exp["expected_entry_count"],
            "dedupe_ok": len(prod) <= exp["expected_entry_count"]}


def score_amounts(exp, out):
    prod = out.get("amounts") or []
    req = [a for a in exp["amounts"] if a.get("required")]
    found, misses = 0, []
    for g in req:
        cents = None if g["value"] is None else round(g["value"] * 100)
        ok = any(f"r{g['record_no']}" in [str(r) for r in a.get("record_ids", [])] and a.get("text") == g["raw"]
                 and a.get("kind") == g["class"] and a.get("value_cents") == cents for a in prod)
        found += ok
        if not ok:
            misses.append(g["id"])
    gold_cents = round(exp["totals"]["explicit_charges_total"] * 100)
    charge_sum = sum(a.get("value_cents") or 0 for a in prod if a.get("kind") == "charge")
    t = out.get("totals") or {}
    shown = (t.get("detected_not_a_total") or {}).get("cents", charge_sum)
    return {"found": found, "total": len(req), "misses": misses, "charge_sum_cents": charge_sum, "golden_total_cents": gold_cents,
            "total_ok": charge_sum == gold_cents and shown == gold_cents}


def tray_flags(out):
    """Flags the judge or the code moved to the could-not-verify tray (state rejected; D-053). They are not assertions the product makes, so they
    are not scored for precision or recall and are reported apart."""
    return [f for f in out.get("flags") or [] if f.get("state") == "rejected" and f.get("type") != "record_warning"]


def to_candidates(out):
    """Emitted flags only (D-053, T-094 r2): a flag in the could-not-verify tray (state rejected) is not a candidate, so it can neither raise nor lower
    precision or recall and cannot be a must_not hit. Tray counts are reported separately (tray_flags, flag_tray)."""
    cands = []
    for f in out.get("flags") or []:
        if f.get("type") == "record_warning" or f.get("state") == "rejected":
            continue
        c = {"type": f["type"], "state": f.get("state"), "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
                                             for e in f.get("evidence", [])]}
        comp = f.get("computed") or {}
        c.update(from_date=f.get("from_date", comp.get("from")), to_date=f.get("to_date", comp.get("to")), days=f.get("days", comp.get("days")))
        cands.append(c)
    return cands


def tolerated_match(t, c):
    recs = {e["record_no"] for e in c["evidence"]}
    return t["type"] == c["type"] and set(t["cite"]["all"]) <= recs and (not t["cite"]["any"] or bool(set(t["cite"]["any"]) & recs))


def score_flags(exp, out):
    cands = to_candidates(out)
    golden = exp["flags"]
    matched_ids, uniq, owned = assign_detail(golden, cands)
    per = {t: {"must": 0, "must_found": 0, "cands": 0, "cands_ok": 0} for t in FLAG_TYPES}
    for g in golden:
        if g["level"] == "must" and g["type"] in per:
            per[g["type"]]["must"] += 1
            per[g["type"]]["must_found"] += g["id"] in matched_ids
    for i, c in enumerate(uniq):
        if c["type"] not in per:
            continue
        per[c["type"]]["cands"] += 1
        per[c["type"]]["cands_ok"] += i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", []))
    hits = []
    for mn in exp.get("must_not_flag", []):
        for i, c in enumerate(uniq):
            if c["type"] != mn["type"]:
                continue
            if mn.get("from_date") or mn.get("to_date"):
                hit = (c.get("from_date"), c.get("to_date")) == (mn.get("from_date"), mn.get("to_date"))
            elif mn.get("record_nos"):
                hit = set(mn["record_nos"]) <= {e["record_no"] for e in c["evidence"]}
            else:
                hit = i not in owned and not any(tolerated_match(t, c) for t in exp.get("tolerated", []))
            if hit:
                hits.append({"must_not_flag": mn["id"], "candidate_type": c["type"]})
    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
    return {"per_type": per, "missed_must": [g["id"] for g in golden if g["level"] == "must" and g["id"] not in matched_ids],
            "must_not_flag_hits": hits,
            "tray_flags": [{"type": f.get("type"), "category": f.get("category"), "reasons": f.get("reasons") or []} for f in tray_flags(out)],
            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}


def score_record_warnings(exp, out):
    miss = []
    for w in exp.get("record_warnings", []):
        if w["level"] != "must":
            continue
        flagged = any(f.get("type") == "record_warning" and any(rn(e.get("record_id", e.get("record_no"))) == w["record_no"] for e in f.get("evidence", []))
                      for f in out.get("flags") or [])
        review = any(w["record_no"] in {rn(r) for r in e.get("record_ids", [])} and e.get("state") == "needs_review" for e in product_entries(out))
        if not (flagged and review):
            miss.append(w["id"])
    return miss


# ---------------------------------------------------------------- calibrated confidence (T-090, D-042)
CAL_STATES = ("verified", "needs_review")
CAL_TYPES = ("entry", "amount", "flag")
CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate


def score_calibration(exp, out, unscored=None):
    """Per product item that is live (verified or needs_review): did it match the golden answer?  Returns
    {item type: {state: [matched, total]}}.  Same match rules as the recall/precision metrics (no new notion of 'correct'):
    entry = some golden entry is found in it (entry_found); amount = a golden amount with the same record, raw text, class and value;
    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored on purpose.
    `unscored` (optional dict) is filled with {item type: n} for produced items that carry no usable state (missing or unknown) or that
    were dropped as duplicates of an earlier flag, so the denominator never silently shrinks (T-090 r2)."""
    tally = {t: {s: [0, 0] for s in CAL_STATES} for t in CAL_TYPES}
    if unscored is not None:
        unscored.update({t: 0 for t in CAL_TYPES})

    def add(kind, state, ok):
        if state in CAL_STATES:
            tally[kind][state][1] += 1
            tally[kind][state][0] += bool(ok)
        elif unscored is not None and state != "rejected":
            unscored[kind] += 1

    for e in product_entries(out):
        add("entry", e.get("state"), any(entry_found(g, [e])[0] for g in exp["entries"]))
    for a in out.get("amounts") or []:
        ok = False
        for g in exp["amounts"]:
            cents = None if g["value"] is None else round(g["value"] * 100)
            if (f"r{g['record_no']}" in [str(r) for r in a.get("record_ids", [])] and a.get("text") == g["raw"]
                    and a.get("kind") == g["class"] and a.get("value_cents") == cents):
                ok = True
                break
        add("amount", a.get("state"), ok)
    cands = to_candidates(out)                    # each candidate carries its own state; record_warning flags are not candidates
    _, uniq, owned = assign_detail(exp["flags"], cands)
    for i, c in enumerate(uniq):
        if c["type"] in FLAG_TYPES:
            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
    if unscored is not None:
        unscored["flag"] += sum(1 for c in cands if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES) - \
            sum(1 for c in uniq if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES)       # duplicates of an earlier flag
    return tally


def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
    def caveat(total):
        """Names the backend and what was run, so the sentence cannot be read as live-model precision when it is a replay (T-090 r2)."""
        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
        if small_cases:
            parts.append("small sample")
        elif total < CAL_SMALL_N:
            parts.append(f"small sample: {total} items")
        return f" on the {backend} backend ({', '.join(parts)})"

    label = {"verified": "Verified items matched the record {m}/{t} times in testing",
             "needs_review": "Items marked needs review matched the record {m}/{t} times in testing"}
    sentences = {"overall": {}, "by_type": {}}
    for s in CAL_STATES:
        b = by_state[s]
        sentences["overall"][s] = ((label[s].format(m=b["matched"], t=b["total"]) + caveat(b["total"]) + ".") if b["total"]
                                   else f"No {s.replace('_', ' ')} items were seen in testing on the {backend} backend.")
        if b["total"] and not_scored["total"]:
            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
    noun = {"entry": "entries", "amount": "amounts", "flag": "flags"}
    for t in CAL_TYPES:
        sentences["by_type"][t] = {}
        for s in CAL_STATES:
            c = cells[t][s]
            sentences["by_type"][t][s] = (f"{('Verified' if s == 'verified' else 'Needs-review')} {noun[t]} matched the record {c['matched']}/{c['total']} "
                                          f"times in testing{caveat(c['total'])}." if c["total"] else
                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
    return sentences


def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
    names = list(results)
    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
    for n, r in results.items():
        for t in CAL_TYPES:
            for s in CAL_STATES:
                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
                c = cells[t][s]
                c["matched"] += m
                c["total"] += tot
                if tot:
                    c["by_case"][n] = [m, tot]
    by_state = {}
    for s in CAL_STATES:
        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
        by_state[s] = {"matched": m, "total": tot, "cases": cs}
    small_cases = len(names) < CAL_SMALL_N
    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)

    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
            "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
            "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
                          "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
            "not_scored": not_scored,
            "cases": names, "case_count": len(names), "small_sample": small_cases or any(by_state[s]["total"] < CAL_SMALL_N for s in CAL_STATES),
            "by_state": by_state, "by_type": cells, "sentences": sentences}


def check_must_not(exp, out):
    """Deterministic must_not checks (regex + structural); judge-type ones are covered by judge #1 over every summary."""
    tool_text = "\n".join([e.get("summary", "") for e in product_entries(out)] + [out.get("letter_text", "") or ""] +
                          [str(v) for v in (out.get("totals") or {}).get("lines", [])])
    amounts = out.get("amounts") or []
    hits = []
    for mn in exp.get("must_not", []):
        c = mn["check"]
        if c == "regex":
            h = regex_hits(mn, tool_text)
        elif c == "amount_value":
            # T-140: the statement is about COUNTING a figure as a charge (every bad_example has class charge), so only an amount whose class is charge can hit.
            h = [a for a in amounts if a.get("kind", "charge") == "charge" and (a.get("value_cents") is not None and a["value_cents"] % 100 == 0 and a["value_cents"] // 100 in mn["values"]
                 or (a.get("value_cents") is not None and a["value_cents"] / 100 in mn["values"]))]
        elif c == "entry_date":
            h = [e for e in product_entries(out) if e.get("date") in mn["dates"]]
        elif c == "flag_status":
            h = [f for f in out.get("flags") or [] if f.get("review_status", "pending") in mn["forbidden"]]
        elif c == "amount_count_max":
            h = [1] if len(amounts) > mn["max"] else []
        else:
            continue
        if h:
            hits.append(mn["id"])
    return hits


def unsupported_summaries(out):
    """Entries that judge #1 or code rejected as not supported (README: a judge-reported `unsupported` fails the case)."""
    n = 0
    for e in product_entries(out):
        v = ((e.get("ladder") or {}).get("judge") or {}).get("verdict")
        n += v == "unsupported" or e.get("state") == "rejected"
    return n


def summary_trim_counts(out):
    """D-054 (T-112 r2): how often code trimmed an AI summary in this case. items_trimmed = entries that kept a shortened summary; tray_placeholders = records whose whole
    summary was removed (could-not-verify tray); clauses_removed = clauses removed over both. Reported, not gated: it shows the clean 3-runs came from the trim and not from luck."""
    trims = [((e.get("ladder") or {}).get("summary_trim"), e) for e in product_entries(out) + list(out.get("tray") or [])]
    trims = [(t, e) for t, e in trims if t and t.get("removed")]
    return {"items_trimmed": sum(1 for t, _ in trims if t.get("kept_summary")), "clauses_removed": sum(len(t["removed"]) for t, _ in trims),
            "tray_placeholders": sum(1 for t, _ in trims if not t.get("kept_summary"))}


def judge_unavailable_in(out):
    """Items whose judge did not answer (JUDGE_UNAVAILABLE): entries, amounts and flags. Their ladder is incomplete, so no metric built on them is trustworthy."""
    items = product_entries(out) + list(out.get("amounts") or []) + list(out.get("flags") or [])
    return sum("JUDGE_UNAVAILABLE" in (i.get("reasons") or []) or ((i.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" for i in items)


def grounding(text, out):
    """R-TL-2, R-TL-9, R-FL-5, R-EX-2: every product excerpt, amount and flag span is verbatim in the input; provider/date equal the record header."""
    ntext = norm(text)
    recs = {rn(r.get("id", r.get("seq"))): r for r in out.get("records") or []}   # run_case record keys: id, seq, n, source, date_iso, date_status
    checked, bad = 0, []

    def chk(label, ok):
        nonlocal checked
        checked += 1
        if not ok:
            bad.append(label)

    for e in product_entries(out):
        chk(f"entry {e.get('id')} excerpt", norm(e.get("excerpt")) in ntext)
        first = recs.get(min((rn(r) for r in e.get("record_ids", [])), default=None))
        if first is not None:
            chk(f"entry {e.get('id')} provider", norm(e.get("provider")) == norm(first["source"]))
            if first.get("date_status") == "parsed":
                chk(f"entry {e.get('id')} date", e.get("date") == first.get("date_iso"))
    for a in out.get("amounts") or []:
        chk(f"amount {a.get('id')}", norm(a.get("text")) in ntext and norm(a.get("excerpt")) in ntext)
    for f in out.get("flags") or []:
        for ev in f.get("evidence", []):
            chk(f"flag {f.get('id')} evidence", norm(ev.get("excerpt")) in ntext)
    return {"checked": checked, "failures": bad}


def score_unsplit(pipeline, backend):
    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
    them and parses every field. Expected: 3 records with the golden date and source (from code), each carrying exactly one LLM_SPLIT record_warning.
    On the fixture backend the recorded split reply lives in tests/fixtures/llm/split and every other call replays from the default recorded dir;
    a missing split dir or any fixture miss makes the row false, so the row cannot be green on a case that was not replayed."""
    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
    text = (GOLD / "unsplit_paste.txt").read_text()
    saved = {k: os.environ.get(k) for k in ("LLM_FIXTURE_DIR", "FIXTURE_SET")}
    misses, replay_misses, orig = [], [], None
    if backend == "fixture":
        # FIXTURE_SET=split looks in tests/fixtures/llm/split first and then in the recorded default dir. LLM_FIXTURE_DIR must NOT be set:
        # fixture.call then skips the default-dir fallback and every other LLM call of this case (extract, flags) misses (T-102 review F3).
        from app.llm.backends import fixture as FX
        os.environ.pop("LLM_FIXTURE_DIR", None)
        os.environ["FIXTURE_SET"] = "split"
        if not any((FX.DEFAULT_DIR / "split").glob("*.json")):
            misses.append("the recorded split fixture dir is missing or empty")
        orig = FX.call

        def spy(*a, **kw):
            try:
                return orig(*a, **kw)
            except FX.FixtureMiss as e:
                replay_misses.append(str(e))
                raise
        FX.call = spy
    try:
        out = pipeline.run_case(text, backend)
    finally:
        if orig is not None:
            FX.call = orig
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    if replay_misses:
        misses.append(f"{len(replay_misses)} LLM call(s) had no recorded fixture (the case was not fully replayed)")
    recs = {rn(r.get("n", r.get("id"))): r for r in out.get("records") or []}
    if len(recs) != len(exp["records"]):
        misses.append(f"record count {len(recs)} != {len(exp['records'])}")
    warn = {}
    for f in out.get("flags") or []:
        if f.get("type") == "record_warning" and f.get("category") == "llm_split":
            for e in f.get("evidence", [])[:1]:
                warn[rn(e.get("record_id", e.get("record_no")))] = warn.get(rn(e.get("record_id", e.get("record_no"))), 0) + 1
    for g in exp["records"]:
        r = recs.get(g["record_no"])
        if r is None:
            misses.append(f"record {g['record_no']} missing")
            continue
        if r.get("date_iso") != g["date"]:
            misses.append(f"record {g['record_no']} date {r.get('date_iso')} != {g['date']}")
        if norm(r.get("source")) != norm(g["source"]):
            misses.append(f"record {g['record_no']} source differs")
        if warn.get(g["record_no"], 0) != 1:
            misses.append(f"record {g['record_no']} has {warn.get(g['record_no'], 0)} LLM_SPLIT warnings, want 1")
    return {"value": not misses, "misses": misses, "records": len(recs), "r_ids": ["R-IN-1", "R-RV-6"]}


def run_cases(pipeline, backend, cases=None, runs_dir=None):
    """Score every golden case. Returns per-case dicts plus the raw outputs for the live-only checks.
    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
    results, outs = {}, {}
    for name, text, exp in (cases or golden_cases()):
        out = pipeline.run_case(text, backend)
        unscored = {}
        outs[name] = out
        write_run_artifact(runs_dir, name, out, name)
        results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
                         "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
                         "unsupported_summaries": unsupported_summaries(out), "judge_unavailable": judge_unavailable_in(out), "grounding": grounding(text, out),
                         "summary_trim": summary_trim_counts(out),
                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
    return results, outs


# ---------------------------------------------------------------- hallucinations (rung 1 code + rung 2 judge)
def parse_record_text(rt):
    """'Record 8 | 2026-05-29 | Austin Imaging, cervical MRI | "excerpt"' -> (label, date, excerpt)."""
    m = re.match(r'Record \d+ \| ([^|]*) \| (.*?) \| "(.*)"\s*$', rt, re.S)
    if not m:
        return "", "", rt
    return m.group(2).strip(), m.group(1).strip(), m.group(3)


def judge_item(item, judge, check_summary):
    label, date, excerpt = parse_record_text(item["record_text"])
    code = list(check_summary(item["candidate_summary"], excerpt, label, date)) if check_summary else []   # a crash propagates: no silent code-rung loss
    verdict = judge(item["candidate_summary"], excerpt, label)
    return {"id": item["id"], "code_reasons": code, "verdict": verdict}


def hallucination_metrics(items, controls, judge, check_summary=None):
    """catch = code check raised a reason OR judge said partially/unsupported/unavailable-is-NOT-a-catch. Rate over EVERY seeded line."""
    rows = [judge_item(i, judge, check_summary) for i in items]
    caught = [r for r in rows if r["code_reasons"] or r["verdict"] in ("partially", "unsupported")]
    crows = [judge_item(c, judge, check_summary) for c in controls]
    unavailable = [r["id"] for r in rows + crows if r["verdict"] == "unavailable"]
    return {"total": len(items), "caught": len(caught), "judge_unavailable_count": len(unavailable), "judge_unavailable_ids": unavailable,
            "status": "not_measured" if unavailable else "measured", "value": ratio(len(caught), len(items)),
            "missed": [r["id"] for r in rows if r not in caught],
            "caught_by_code": sum(1 for r in rows if r["code_reasons"]), "caught_by_judge_only": sum(1 for r in caught if not r["code_reasons"]),
            "controls_total": len(controls), "controls_unsupported": [r["id"] for r in crows if r["verdict"] == "unsupported"],
            "controls_flagged_by_code": [r["id"] for r in crows if r["code_reasons"]],
            "controls_partially": [r["id"] for r in crows if r["verdict"] == "partially"]}


def load_jsonl(p):
    return [json.loads(l) for l in pathlib.Path(p).read_text().splitlines() if l.strip()]


# ---------------------------------------------------------------- J3 / J4 seeded controls (rung 2 for flags; T-093, D-046)
POSITIVE = {"j3": "conflict", "j4": "agree"}
CONTROL_FILES = (("judge_controls.jsonl", "in_sample"), ("judge_controls_heldout.jsonl", "held_out"))
CONTROL_REPEATS = 3          # live: every control item is judged on the same three runs as R-CO-7, and the gate needs all three to agree


def control_prompt(j):
    """Prompt id the judge currently calls (read from app/backend/judges.py, so the report names the version actually measured)."""
    m = re.search(r'"(judge_conflict_v\d+)"' if j == "j3" else r'"(judge_flag_v\d+)"', (ROOT / "app" / "backend" / "judges.py").read_text())
    return m.group(1) if m else "unknown"


def load_controls(gold=None):
    """In-sample controls (they share authors and rules with the prompts they test) and the held-out file (separately authored; its status is derived by evals/heldout_audit.py)."""
    gold = pathlib.Path(gold or GOLD)
    rows = []
    for name, split in CONTROL_FILES:
        if (gold / name).exists():
            rows += [{"split": split, **r} for r in load_jsonl(gold / name)]
    return rows


def judge_controls_metrics(items, judge_control, repeats=1, workers=1):
    """Seeded wrong and correct items for J4 (judge_flag_v2) and J3 (the judge_conflict version judges.py names). judge_control(item) -> (verdict, reason_code), called `repeats` times per item.
    catch = a WRONG item that never got the positive verdict (J4 'agree', J3 'conflict') in any repeat; false_agree = a wrong item that got it in any repeat.
    A repeat that answers 'unavailable' is not a catch and makes the metric not_measured. An item whose repeats disagree is listed under `unstable`.
    correct_accepted counts correct items the judge confirmed on every repeat. It is REPORTED, NOT GATED: D-046 gates catches and false agrees only, and an
    over-rejecting judge costs flag recall (bar 3) on a live run, so a second threshold here would be a spec change that needs its own ADR (T-093 r2, F4).
    Metrics are also split into in_sample and held_out controls (T-093 r2, F6)."""
    def one(i):
        return i, [judge_control(i) for _ in range(repeats)]
    if workers > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=workers) as ex:
            done = list(ex.map(one, items))
    else:
        done = [one(i) for i in items]
    out, rows = {}, []
    for j in ("j3", "j4"):
        res = []
        for i, calls in done:
            if i["judge"] != j:
                continue
            verdicts = [v for v, _ in calls]
            if POSITIVE[j] in verdicts:
                verdict = POSITIVE[j]
            elif "unavailable" in verdicts:
                verdict = "unavailable"
            else:
                verdict = verdicts[0]
            res.append({"id": i["id"], "judge": j, "kind": i["kind"], "split": i.get("split", "in_sample"), "pair": i.get("pair"), "origin": i.get("origin"), "expected": i["expected"],
                        "verdict": verdict, "verdicts": verdicts, "stable": len(set(verdicts)) == 1, "reason_codes": [c for _, c in calls],
                        "reason_code": calls[0][1]})
        rows += res

        def stats(sel):
            wrong, right = [r for r in sel if r["kind"] == "wrong"], [r for r in sel if r["kind"] == "correct"]
            caught = [r for r in wrong if r["verdict"] not in (POSITIVE[j], "unavailable")]
            return {"wrong_total": len(wrong), "wrong_caught": len(caught), "catch_rate": ratio(len(caught), len(wrong)),
                    "false_agree": [r["id"] for r in wrong if r["verdict"] == POSITIVE[j]],
                    "correct_total": len(right), "correct_accepted": sum(1 for r in right if r["verdict"] == POSITIVE[j] and all(v == POSITIVE[j] for v in r["verdicts"]))}
        out[j] = {**stats(res), "judge_unavailable_ids": [r["id"] for r in res if r["verdict"] == "unavailable"],
                  "unstable": [r["id"] for r in res if not r["stable"]], "repeats": repeats,
                  "by_split": {sp: stats([r for r in res if r["split"] == sp]) for sp in ("in_sample", "held_out") if any(r["split"] == sp for r in res)},
                  "prompt": control_prompt(j)}
    unavailable = [i for j in ("j3", "j4") for i in out[j]["judge_unavailable_ids"]]
    out.update(status="not_measured" if unavailable else "measured", rows=rows, r_ids=["R-CO-2", "R-CO-3"], repeats=repeats,
               value=None if unavailable else min((out[j]["catch_rate"] if out[j]["catch_rate"] is not None else 0.0) for j in ("j3", "j4")))
    return out


def default_judge_control(backend):
    """judge_control for a real run: one J3/J4 call on a scratch database under the requested backend. A missing fixture or failed call is 'unavailable'."""
    import tempfile
    from app.backend import judges, pipeline as BP
    from app.llm import provider as P

    def run(item):
        text = item.get("excerpt") or item["excerpt_a"]
        with BP._Backend(backend), tempfile.TemporaryDirectory() as tmp:
            conn, cid, call = BP._scratch_call(tmp, text)
            try:
                if item["judge"] == "j4":
                    v, _, code = judges.run_j4_meta(item["excerpt"], item["flag_type"], item["category"], call=call, item_id=item["id"])
                else:
                    v, _, code = judges.run_j3_meta(item["excerpt_a"], item["excerpt_b"], call=call, item_id=item["id"], category=item["category"])
            except P.FixtureMiss:
                v, code = "unavailable", "NONE"
            finally:
                conn.close()
        return v, code
    return run


# ---------------------------------------------------------------- live-only: 3 runs on the sample
def _ids(f):
    """Set of record ids a flag cites: its own record_ids plus every evidence record_id (R-CO-7: flags are compared by cited record IDs)."""
    ids = {str(x) for x in f.get("record_ids") or []}
    ids |= {str(e.get("record_id")) for e in f.get("evidence") or [] if e.get("record_id") is not None}
    return sorted(ids)


def _h(s):
    return hashlib.sha256(norm(s).encode()).hexdigest()[:16]


def _srt(rows):
    """Sort rows that may hold None next to str (undated, missing) without a TypeError: by their JSON text."""
    return sorted(rows, key=lambda r: json.dumps(r, sort_keys=True, default=str))


def signature_parts(out):
    """Every R-CO-7 field, by name. Code outputs (record split, parsed dates, entry-ID set, gap flags, amount list and classes, totals) must be identical
    across runs; LLM-derived states (every entry, amount and flag) must match; flags are compared by (type, set of cited record IDs, evidence excerpt)
    plus category and state. Summary wording is NOT in here: it may differ but must be supported in every run (judged by unsupported_count_3run)."""
    recs = _srt((str(r.get("id") or r.get("n") or r.get("seq")), r.get("source"), _h(r.get("excerpt") or ""), r.get("date_iso"), r.get("date_status"))
                  for r in out.get("records") or [])
    ents = product_entries(out)
    # R-CO-7's flag signature covers EMITTED flags (state verified or needs_review), not could-not-verify tray items (D-053); the tray is reported
    # apart (run artifact `tray_flag_count`, report `flag_tray`). A flag that flips between the tray and the list still changes this signature.
    flags = [f for f in out.get("flags") or [] if f.get("state") != "rejected"]
    return {
        "record_split": recs,
        "parsed_dates": _srt((str(r.get("id") or r.get("n") or r.get("seq")), r.get("date_iso"), r.get("date_status")) for r in out.get("records") or []),
        "entry_ids": _srt(str(e.get("id")) for e in ents),
        "entries": _srt((tuple(_srt(e.get("record_ids", []))), e.get("date"), e.get("date_status"), e.get("provider"), e.get("state"),
                           tuple(_srt(e.get("reasons") or []))) for e in ents),
        "gap_flags": _srt((tuple(_ids(f)), (f.get("computed") or {}).get("from"), (f.get("computed") or {}).get("to"), (f.get("computed") or {}).get("days"),
                             f.get("state")) for f in flags if f.get("type") == "gap"),
        "amounts": _srt((a.get("text"), a.get("value_cents"), a.get("kind"), a.get("state"), tuple(_srt(a.get("record_ids", [])))) for a in out.get("amounts") or []),
        "totals": out.get("totals") or {},
        "tray": _srt((tuple(_srt(t.get("record_ids", []))), t.get("date"), t.get("provider"), t.get("state"), tuple(_srt(t.get("reasons") or [])))
                       for t in out.get("tray") or []),
        "flags": _srt((f.get("type"), f.get("category"), tuple(_ids(f)), tuple(_srt(norm(e.get("excerpt")) for e in f.get("evidence", []))), f.get("state"))
                        for f in flags),
    }


def signature(out):
    return json.dumps(signature_parts(out), sort_keys=True, default=str)


def diff_parts(a, b):
    """Name every R-CO-7 field that differs between two runs and the items present in only one of them (so a determinism failure is diagnosable)."""
    d = {}
    for k in sorted(set(a) | set(b)):
        if a.get(k) == b.get(k):
            continue
        if isinstance(a.get(k), list) and isinstance(b.get(k), list):
            ja, jb = [json.dumps(x, sort_keys=True, default=str) for x in a[k]], [json.dumps(x, sort_keys=True, default=str) for x in b[k]]
            d[k] = {"only_in_first": [x for x in ja if x not in jb][:20], "only_in_other": [x for x in jb if x not in ja][:20]}
        else:
            d[k] = {"first": json.dumps(a.get(k), sort_keys=True, default=str)[:500], "other": json.dumps(b.get(k), sort_keys=True, default=str)[:500]}
    return d


_SECRET = re.compile(r"sk-[A-Za-z0-9_-]{16,}|ANTHROPIC_API_KEY|-----BEGIN [A-Z ]*PRIVATE KEY")


def _judge(x):
    j = ((x.get("ladder") or {}).get("judge")) or {}
    return {"verdict": j.get("verdict"), "reason_code": j.get("reason_code"), "prompt_version": j.get("prompt_version"), "model": j.get("model")}


def run_artifact(out, name=None, run=None):
    """Per-run record for diagnosis: items and their states, judge verdicts and reason codes, prompt versions, error codes and the signature parts.
    Deliberately NO prompts, no model output text, no summaries (a hash only), no environment: nothing secret can get in."""
    def item(x, kind):
        gen = ((x.get("ladder") or {}).get("generator")) or {}
        row = {"id": x.get("id"), "kind": kind, "record_ids": x.get("record_ids"), "state": x.get("state"), "reasons": x.get("reasons"), "judge": _judge(x),
               "generator_prompt_version": gen.get("prompt_version")}
        if kind in ("entry", "undated_entry"):
            row.update(date=x.get("date"), date_status=x.get("date_status"), provider=x.get("provider"), summary_sha=_h(x.get("summary") or ""))
        elif kind == "amount":
            row.update(text=x.get("text"), value_cents=x.get("value_cents"), cls=x.get("kind"))
        else:
            row.update(type=x.get("type"), category=x.get("category"), origin=x.get("origin"), computed=x.get("computed"),
                       evidence=[{"record_id": e.get("record_id"), "excerpt": e.get("excerpt")} for e in x.get("evidence") or []])
        return row
    items = [item(e, "entry") for e in out.get("entries") or []] + [item(e, "undated_entry") for e in out.get("undated_entries") or []] + \
            [item(a, "amount") for a in out.get("amounts") or []] + [item(f, "flag") for f in out.get("flags") or []]
    return {"schema": "evals.run.artifact/1", "case": name, "run": run, "backend": out.get("backend"), "models": out.get("models"), "status": out.get("status"),
            "tray_flag_count": len(tray_flags(out)),
            "errors": [{"code": e.get("code"), "stage": e.get("stage"), "record_no": e.get("record_no")} for e in out.get("errors") or []],
            "warning_codes": sorted({w.get("code") for w in out.get("warnings") or [] if isinstance(w, dict)} - {None}),
            "items": items, "signature_parts": signature_parts(out)}


def write_run_artifact(runs_dir, fname, out, name=None, run=None):
    """Write evals/reports/runs/<ts>/<fname>.json. Refuses (raises) if anything secret-looking would be written."""
    if runs_dir is None:
        return None
    body = json.dumps(run_artifact(out, name, run), indent=1, sort_keys=True, default=str) + "\n"
    if _SECRET.search(body):
        raise ValueError(f"refusing to write {fname}: secret-looking content")
    d = pathlib.Path(runs_dir)
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{fname}.json").write_text(body)
    return d / f"{fname}.json"


def live_metrics(pipeline, backend, text, runs=3, runs_dir=None):
    """Exactly 3 runs are required (R-CO-7). Any other count is recorded as not_measured with the reason and can never satisfy the bar.
    With runs_dir each run's artifact (run1.json ..) is written there, and a mismatch lists the differing fields and items."""
    if runs != 3:
        why = f"runs={runs}; exactly 3 live runs are required"
        return {"determinism_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["determinism_3run"]),
                "unsupported_count_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["unsupported_count_3run"])}
    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
    for i, o in enumerate(outs, 1):
        write_run_artifact(runs_dir, f"run{i}", o, "sample", i)
    parts = [signature_parts(o) for o in outs]
    sigs = [signature(o) for o in outs]
    unsupported = [unsupported_summaries(o) + len(grounding(text, o)["failures"]) for o in outs]
    det = {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"],
           "fields": list(parts[0])}
    if det["value"] != 1.0:
        det["differences"] = {f"run1_vs_run{i + 1}": diff_parts(parts[0], parts[i]) for i in range(1, runs) if sigs[i] != sigs[0]}
    return {"determinism_3run": det,
            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}


# ---------------------------------------------------------------- lexicon recall (reported, not gated: D-026)
def lexicon_recall(lexicon_flags, cases=None):
    """Recall of golden `must` pre_existing + causation flags by the lexicon floor alone, per case and pooled. lexicon_flags(record)->flags."""
    per, tot, found = {}, 0, 0
    for name, text, exp in (cases or golden_cases()):
        gold = [f for f in exp["flags"] if f["type"] in ("pre_existing", "causation") and f["level"] == "must"]
        if not gold:
            continue
        cands = []
        recs = {r["record_no"]: r for r in exp["records"]}
        for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', text):
            n = int(m.group(1))
            rec = {"n": n, "source": m.group(3), "excerpt": m.group(4), "date_iso": (recs.get(n) or {}).get("date")}
            for f in lexicon_flags(rec):
                cands.append({"type": f["type"], "evidence": [{"record_no": n, "excerpt": f["excerpt"]}]})
        ids, _, _ = assign_detail(gold, cands)
        per[name] = {"found": len(ids), "total": len(gold), "recall": len(ids) / len(gold), "missed": sorted(g["id"] for g in gold if g["id"] not in ids)}
        tot += len(gold)
        found += len(ids)
    return {"value": ratio(found, tot), "found": found, "total": tot, "per_case": per, "gated": False, "r_ids": RIDS["lexicon_recall_must_flags"]}


# ---------------------------------------------------------------- spec vs golden (REQUIREMENTS section 6)
def spec_blocks(req_text):
    sec = req_text.split("## 6. Export template", 1)[1].split("\n## ", 1)[0]
    blocks = re.findall(r"```\n(.*?)\n```", sec, re.S)
    return blocks[0], blocks[1]


def golden_blocks(export_text):
    head2 = re.search(r"^=== INTERNAL_NOTES_TEXT.*===\s*$", export_text, re.M)
    head1 = re.search(r"^=== LETTER_TEXT.*===\s*$", export_text, re.M)
    letter = export_text[head1.end():head2.start()].strip("\n")
    notes = export_text[head2.end():].strip("\n")
    return letter, notes


def check_spec(req_path=REQUIREMENTS, golden_path=GOLD / "sample.export.expected.txt"):
    b1, b2 = spec_blocks(pathlib.Path(req_path).read_text())
    g1, g2 = golden_blocks(pathlib.Path(golden_path).read_text())
    return {"spec_matches_golden": b1 == g1 and b2 == g2, "letter_equal": b1 == g1, "internal_notes_equal": b2 == g2}


# ---------------------------------------------------------------- aggregate + ship bar
def _flag_tray(results):
    """Could-not-verify flag counts (D-053), reported and never gated: precision above is over emitted flags only."""
    rows = [(n, t) for n, r in results.items() for t in r["flags"].get("tray_flags", [])]
    by_reason = {}
    for _, t in rows:
        k = (t["reasons"] or ["NONE"])[0]
        by_reason[k] = by_reason.get(k, 0) + 1
    return {"value": len(rows), "by_reason": by_reason, "by_case": {n: sum(1 for m, _ in rows if m == n) for n in sorted({n for n, _ in rows})},
            "note": "tray flags are not scored for precision or recall and are not in the R-CO-7 flag-set signature (D-053)"}


def aggregate(results):
    ent = [r["entries"] for r in results.values()]
    amt = [r["amounts"] for r in results.values()]
    fl = [r["flags"]["per_type"] for r in results.values()]
    fprec, frec = {}, {}
    for t in FLAG_TYPES:
        c = sum(p[t]["cands"] for p in fl); ok = sum(p[t]["cands_ok"] for p in fl)
        m = sum(p[t]["must"] for p in fl); mf = sum(p[t]["must_found"] for p in fl)
        fprec[t], frec[t] = ratio(ok, c), ratio(mf, m)
    gr = [r["grounding"] for r in results.values()]
    checked = sum(g["checked"] for g in gr)
    return {
        "grounding_rate": {"value": ratio(checked - sum(len(g["failures"]) for g in gr), checked), "checked": checked,
                           "failures": [f for g in gr for f in g["failures"]], "r_ids": RIDS["grounding_rate"]},
        "entry_recall": {"value": ratio(sum(e["found"] for e in ent), sum(e["total"] for e in ent)),
                         "misses": {n: r["entries"]["misses"] for n, r in results.items() if r["entries"]["misses"]},
                         "dedupe_failures": [n for n, r in results.items() if not r["entries"]["dedupe_ok"]], "r_ids": RIDS["entry_recall"]},
        "amount_recall": {"value": ratio(sum(a["found"] for a in amt), sum(a["total"] for a in amt)),
                          "total_mismatch": [n for n, r in results.items() if not r["amounts"]["total_ok"]], "r_ids": RIDS["amount_recall"]},
        "flag_precision": {**fprec, "r_ids": RIDS["flag_precision"]},
        "flag_recall": {**frec, "r_ids": RIDS["flag_recall"],
                        "missed_must": {n: r["flags"]["missed_must"] for n, r in results.items() if r["flags"]["missed_must"]}},
        "flag_tray": _flag_tray(results),
        "summary_trim_fired": {**{k: sum((r.get("summary_trim") or {}).get(k, 0) for r in results.values()) for k in ("items_trimmed", "clauses_removed", "tray_placeholders")},
                               "per_case": {n: r["summary_trim"] for n, r in results.items() if (r.get("summary_trim") or {}).get("clauses_removed")}},
        "judge_unavailable_in_cases": {"value": sum(r["judge_unavailable"] for r in results.values()),
                                       "per_case": {n: r["judge_unavailable"] for n, r in results.items() if r["judge_unavailable"]}},
        "golden_must_not_hits": {"value": sum(len(r["must_not_hits"]) + len(r["flags"]["must_not_flag_hits"]) + r["unsupported_summaries"] +
                                              len(r["record_warning_misses"]) for r in results.values()),
                                 "detail": {n: {"must_not": r["must_not_hits"], "must_not_flag": r["flags"]["must_not_flag_hits"],
                                                "unsupported_summaries": r["unsupported_summaries"], "record_warning_misses": r["record_warning_misses"]}
                                            for n, r in results.items() if r["must_not_hits"] or r["flags"]["must_not_flag_hits"] or
                                            r["unsupported_summaries"] or r["record_warning_misses"]}, "r_ids": RIDS["golden_must_not_hits"]},
    }


def assertions(results):
    s = results.get("sample", {}).get("flags")
    c6 = results.get("case_06_subtle_pre_existing", {}).get("flags")
    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
    g73 = s is not None and ("2026-03-06", "2026-05-18", 73) not in [tuple(x) for x in s["gap_rows_wrong"]]
    n28 = s is not None and ("2026-01-23", "2026-02-20", 28) not in [tuple(x) for x in s["gap_rows_wrong"]] and \
        (c6 is None or ("2026-10-19", "2026-11-16", 28) not in [tuple(x) for x in c6["gap_rows_wrong"]])
    return {"gap_28_not_flagged": n28, "gap_73_flagged": g73, "all_gap_rows_correct": not any(wrong.values())}


def case_07_total(results, outs):
    out = outs.get("case_07_prompt_injection")
    if out is None:
        return {"value": False, "status": "not_run"}
    ok = results["case_07_prompt_injection"]["amounts"]["total_ok"] and results["case_07_prompt_injection"]["amounts"]["charge_sum_cents"] == 42000
    return {"value": bool(ok), "r_ids": RIDS["case_07_total_420"]}


def controls_ok(jc):
    """D-046 / spec section 7 row 4: J3 and J4 each catch EVERY seeded wrong item (wrong_caught == wrong_total, so a rate of 1.0, not the 0.95 hallucination bar)
    with no false agree, measured with no judge unavailable. Pinned by tests/unit/test_t093_eval_signature.py (T-093 r3)."""
    if not jc or jc.get("status") != "measured":
        return False
    return all(jc[j]["wrong_total"] > 0 and jc[j]["wrong_caught"] == jc[j]["wrong_total"] and not jc[j]["false_agree"] for j in ("j3", "j4"))


def ge_(x, t):
    return x is not None and x >= t


def ship_bar(m, a, backend, spec_ok):
    """Four automated bars (row 5, reviewability, is persona + E2E and is not computed here). Missing/unmeasured => bar fails."""
    th = THRESHOLDS
    def ge(x, t):
        return x is not None and x >= t
    b = {
        "1_grounding": ge(m["grounding_rate"]["value"], th["grounding_rate"]),
        "2_recall": ge(m["entry_recall"]["value"], th["entry_recall"]) and ge(m["amount_recall"]["value"], th["amount_recall"]),
        "3_flags": all(ge(m["flag_precision"][t], th["flag_precision"]) and ge(m["flag_recall"][t], th["flag_recall"]) for t in FLAG_TYPES)
                   and a["gap_28_not_flagged"] and a["gap_73_flagged"],
        "4_no_invented_facts": m["hallucination_catch_rate"].get("judge_unavailable_count", 0) == 0 and m["judge_unavailable_in_cases"]["value"] == 0
                               and ge(m["hallucination_catch_rate"]["value"], th["hallucination_catch_rate"]) and not m["hallucination_catch_rate"]["controls_unsupported"]
                               and m["golden_must_not_hits"]["value"] == 0 and m["unsplit_paste"]["value"] is True and m["case_07_total_420"]["value"] is True
                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3
                               and controls_ok(m.get("judge_controls")),
    }
    blockers = [k for k, v in b.items() if not v]
    for k in ("determinism_3run", "unsupported_count_3run"):
        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
            blockers.append(f"{k}: {m[k].get('reason') or 'not measured over exactly 3 live runs'}")
    if backend not in LIVE_BACKENDS:
        why4 = "; this is why 4_no_invented_facts fails here (its determinism_3run and unsupported_count_3run clauses cannot be measured)" if "4_no_invented_facts" in blockers else ""
        blockers.append(f"backend={backend}: determinism_3run and unsupported_count_3run need a live backend (R-CO-7){why4}")
    if m["hallucination_catch_rate"].get("judge_unavailable_count", 0):
        blockers.append(f"hallucination_catch_rate not_measured: judge unavailable on {m['hallucination_catch_rate']['judge_unavailable_count']} line(s) (stale or missing judge fixtures?)")
    if m["judge_unavailable_in_cases"]["value"]:
        blockers.append(f"judge unavailable on {m['judge_unavailable_in_cases']['value']} item(s) in the golden cases: {m['judge_unavailable_in_cases']['per_case']}")
    if m["amount_recall"]["total_mismatch"]:
        blockers.append("charge total differs from golden in " + ", ".join(m["amount_recall"]["total_mismatch"]))
    if m["entry_recall"]["dedupe_failures"]:
        blockers.append("dedupe failures in " + ", ".join(m["entry_recall"]["dedupe_failures"]))
    jc = m.get("judge_controls")
    if not controls_ok(jc):
        blockers.append("judge_controls (J3/J4 seeded wrong items): " + ("not measured" if not jc or jc.get("status") != "measured" else
                        "; ".join(f"{j} caught {jc[j]['wrong_caught']}/{jc[j]['wrong_total']}, false agree {jc[j]['false_agree']}" for j in ("j3", "j4"))))
    lc = m.get("letter_currency_outside_charges") or {}
    if lc.get("value"):       # measured and non-zero (not_measured only occurs with an injected fake pipeline)
        blockers.append(f"letter states a dollar amount outside the charges section ({lc['value']} in {', '.join(lc.get('per_case') or [])})")
    if not spec_ok:
        blockers.append("spec_matches_golden is false")
    return b, blockers


def evaluate_report(report):
    """Recompute ship_bar_met from a report's own numbers (used by the tampered-report test and the runner)."""
    b, blockers = ship_bar(report["metrics"], report["assertions"], report["backend"], report["spec_matches_golden"])
    return not blockers, b, blockers


def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None, letters=None):
    cases = cases or golden_cases()
    results, outs = run_cases(pipeline, backend, cases, runs_dir)
    m = aggregate(results)
    items, controls = load_jsonl(GOLD / "hallucinations.jsonl"), load_jsonl(GOLD / "hallucinations_controls.jsonl")
    if check_summary is None:
        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
        check_summary = GR.check_summary
    check = check_summary
    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
    m["case_07_total_420"] = case_07_total(results, outs)
    m["unsplit_paste"] = score_unsplit(pipeline, backend)
    sample = next(t for n, t, _ in cases if n == "sample")
    if backend in LIVE_BACKENDS:
        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
    else:
        m["determinism_3run"] = dict(NOT_MEASURED, r_ids=RIDS["determinism_3run"])
        m["unsupported_count_3run"] = dict(NOT_MEASURED, r_ids=RIDS["unsupported_count_3run"])
    if lexicon_flags is None:
        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
        lexicon_flags = FL.lexicon_flags
    m["lexicon_recall_must_flags"] = lexicon_recall(lexicon_flags, cases)
    if judge_control is None:
        m["judge_controls"] = {"status": "not_measured", "value": None, "reason": "no judge_control supplied", "r_ids": ["R-CO-2", "R-CO-3"]}
    else:
        m["judge_controls"] = judge_controls_metrics(load_controls(), judge_control, repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1)
    # T-139 (D-019, R-CH-7, R-EX-8): the letter itself, exported on the FIXTURE backend for every golden and library case, states no dollar amount outside the charges section
    m["letter_currency_outside_charges"] = letters() if letters is not None else {"status": "not_measured", "value": None, "reason": "no letters check supplied", "r_ids": ["R-CH-7", "R-EX-8"]}
    a = assertions(results)
    spec = check_spec(req_path)
    sample_out = outs.get("sample", {})
    source = git_source()
    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
              "source": {"commit": source["commit"], "tree": source["tree"], "clean": source["clean"], "dirty": source["dirty"]},
              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
              "thresholds": THRESHOLDS, "cases": list(results)}
    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
    if runs_dir is not None:
        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
    met, bars, blockers = evaluate_report(report)
    report.update(ship_bar_met=met, bars=bars, blockers=blockers)
    return report


# ---------------------------------------------------------------- output
def pct(x):
    return "n/a" if x is None else f"{x:.3f}"


def render_controls(jc):
    if not jc or "j3" not in jc:
        return ["| judge_controls (J3/J4 seeded) | not_measured | catch every wrong item on every repeat, 0 false agree | R-CO-2 |"]
    L = []
    for j in ("j3", "j4"):
        x = jc[j]
        sp = "; ".join(f"{k.replace('_', '-')} {v['wrong_caught']}/{v['wrong_total']}" for k, v in x.get("by_split", {}).items())
        L.append(f"| {j.upper()} {x['prompt']} seeded catch rate | {pct(x['catch_rate'])} ({x['wrong_caught']}/{x['wrong_total']} wrong caught x{x.get('repeats', 1)} runs; {sp}; "
                 f"false agree {len(x['false_agree'])} {x['false_agree']}; correct accepted {x['correct_accepted']}/{x['correct_total']}; "
                 f"unstable {x.get('unstable', [])}; unavailable {len(x['judge_unavailable_ids'])}) | all wrong caught, 0 false agree | R-CO-2 |")
    return L


def render_control_items(jc):
    """Per-item verdict on every repeat. in-sample controls share authors and rules with the prompts (not independent evidence); a held-out row is separately authored
    and its status is derived from git (evals/heldout_audit.py), never taken from the label."""
    if not jc or "rows" not in jc:
        return []
    L = ["", "## Judge controls, per item", "", "In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says "
         "whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate "
         "from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).", "", "| id | judge | split | kind | pair | origin | expected | verdict per run | ok |", "|---|---|---|---|---|---|---|---|---|"]
    for r in jc["rows"]:
        ok = (r["verdict"] not in (POSITIVE[r["judge"]], "unavailable")) if r["kind"] == "wrong" else all(v == POSITIVE[r["judge"]] for v in r["verdicts"])
        L.append(f"| {r['id']} | {r['judge']} | {r['split'].replace('_', '-')} | {r['kind']} | {(r.get('pair') or '').replace('|', '/')} | {r.get('origin') or ''} | {r['expected']} | {' / '.join(r['verdicts'])} | {'yes' if ok else 'NO'} |")
    try:
        from evals import heldout_audit
        L += ["", *heldout_audit.summary_lines()]
    except Exception as e:      # the audit is information about the evidence, never a reason to lose the report
        L += ["", f"Held-out status could not be computed ({type(e).__name__}); the `held-out` label alone is a claim, not a check."]
    return L + [""]


def render_calibration(c):
    """Calibrated confidence (T-090): counts per state and per type, backend named, no percentages."""
    if not c:
        return []
    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases, source commit `{(c.get('source_commit') or 'unknown')[:10]}`)", ""]
    L += [f"- {c['sentences']['overall'][s]}" for s in CAL_STATES]
    L += ["", "| Item type | Verified (matched/seen) | Needs review (matched/seen) |", "|---|---|---|"]
    for t in CAL_TYPES:
        v, n = c["by_type"][t]["verified"], c["by_type"][t]["needs_review"]
        L.append(f"| {t} | {v['matched']}/{v['total']} | {n['matched']}/{n['total']} |")
    return L + [""]


def render_md(r):
    m = r["metrics"]
    src = r.get("source") or {}
    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`",
         f"Source commit `{src.get('commit') or 'unknown'}`, tree {'clean' if src.get('clean') else 'DIRTY, not reproducible from the commit' if src.get('clean') is False else 'unknown'}.", ""]
    if r["blockers"]:
        L += ["Blockers: " + "; ".join(r["blockers"]), ""]
    L += ["| Metric | Value | Bar | R-IDs |", "|---|---|---|---|"]
    L += [f"| grounding_rate | {pct(m['grounding_rate']['value'])} ({m['grounding_rate']['checked']} checked) | 1.0 | {', '.join(RIDS['grounding_rate'])} |",
          f"| entry_recall | {pct(m['entry_recall']['value'])} | >= 0.95 | {', '.join(RIDS['entry_recall'])} |",
          f"| amount_recall | {pct(m['amount_recall']['value'])} | >= 0.95 | R-CH-1 |"]
    for t in FLAG_TYPES:
        L.append(f"| flag_precision[{t}] / flag_recall[{t}] | {pct(m['flag_precision'][t])} / {pct(m['flag_recall'][t])} | >= 0.9 each | R-FL-1..4 |")
    h = m["hallucination_catch_rate"]
    L += [f"| hallucination_catch_rate | {pct(h['value'])} ({h['caught']}/{h['total']}; {h['status']}; judge unavailable {h['judge_unavailable_count']}) | >= 0.95 | R-TL-4, R-TL-10 |",
          f"| controls judged unsupported | {len(h['controls_unsupported'])} of {h['controls_total']} | 0 | R-TL-4 |",
          f"| unsupported_count_3run | {m['unsupported_count_3run'].get('value', 'not_measured')} | 0 | R-TL-4 |",
          f"| determinism_3run | {m['determinism_3run'].get('value', 'not_measured')} | 1.0 | R-CO-7 |",
          *render_controls(m.get("judge_controls")),
          f"| golden_must_not_hits | {m['golden_must_not_hits']['value']} | 0 | R-CO-3 |",
          f"| unsplit_paste (LLM split, D-031) | {m['unsplit_paste']['value']} {m['unsplit_paste']['misses']} | true | R-IN-1 |",
          f"| case_07_total_420 | {m['case_07_total_420']['value']} | true | R-RV-6 |",
          *( [f"| letter_currency_outside_charges (fixture export, {m['letter_currency_outside_charges'].get('cases', 0)} cases; {m['letter_currency_outside_charges'].get('held_out_entries', 0)} entries held out) | "
              f"{m['letter_currency_outside_charges'].get('value', 'not_measured')} | 0 | R-CH-7, R-EX-8 |"] if "letter_currency_outside_charges" in m else [] ),
          f"| lexicon_recall_must_flags (reported, not gated) | {pct(m['lexicon_recall_must_flags'].get('value'))} | none (D-026) | R-FL-3, R-RV-6 |", ""]
    L += render_calibration(r.get("calibration"))
    L += render_control_items(m.get("judge_controls"))
    L += [f"Assertions: {json.dumps(r['assertions'])}", f"spec_matches_golden: {r['spec_matches_golden']}", "",
          "## Misses (report what was found)", "", f"- entry misses: {json.dumps(m['entry_recall']['misses'])}",
          f"- missed must flags: {json.dumps(m['flag_recall']['missed_must'])}",
          f"- summary clauses removed by code (D-054, reported not gated): {json.dumps(m['summary_trim_fired'])}",
          f"- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): {m['flag_tray']['value']} {json.dumps(m['flag_tray']['by_reason'])} by case {json.dumps(m['flag_tray']['by_case'])}", f"- grounding failures: {json.dumps(m['grounding_rate']['failures'])}",
          f"- seeded hallucinations not caught: {h['missed']}", f"- must_not detail: {json.dumps(m['golden_must_not_hits']['detail'])}", "",
          *( [f"- per-run artifacts: `{r['run_artifacts']}`"] if r.get("run_artifacts") else [] ),
          *( ["- determinism differences: " + json.dumps(m["determinism_3run"]["differences"])] if m["determinism_3run"].get("differences") else [] ),
          "", "## Prompt and lexicon hashes", ""] + [f"- `{k}` {v}" for k, v in r["hashes"].items()]
    return "\n".join(L) + "\n"


class CalibrationRefused(RuntimeError):
    """T-101 r2: write_report(write_calibration=True) was asked to write the committed calibration.json from a header that is not a clean commit."""


def write_calibration_refusal(src):
    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tree at a commit: no tracked
    file differs from HEAD and no untracked file sits under the eval's inputs (T-090 r2: the header must name the code that produced the counts)."""
    if src.get("commit") is None or src.get("clean") is None:
        return "no git repository or HEAD commit is available to name as the source"
    if not src["clean"]:
        paths = [p.rstrip() for p in (src.get("dirty") or [])]
        shown = "; ".join(paths[:10]) or "paths not listed"
        more = f"; and {len(paths) - 10} more" if len(paths) > 10 else ""
        return (f"the tree has uncommitted changes or untracked files under the eval inputs ({shown}{more}); "
                "commit, stash or remove them, or run from a clean worktree of HEAD")
    return None


def write_report(r, outdir=REPORTS, write_calibration=False, scratch_ts=None):
    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
    copy under outdir/runs/<scratch_ts or ts>/ so a plain run never touches the file the app serves (T-101).
    write_calibration is judged here as well as in main(), so every caller that reaches the committed file meets the same clean-HEAD rule (T-101 r2)."""
    if write_calibration:                         # checked before anything is written: a refused call leaves the directory as it was
        cal = r.get("calibration") or {}
        why = "the report has no calibration" if not cal else write_calibration_refusal(
            {"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"), "dirty": []})
        if why:
            raise CalibrationRefused(why)
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = r["generated_at"].replace(":", "").replace("-", "")
    (outdir / f"{ts}.md").write_text(render_md(r))
    body = json.dumps(r, indent=1, sort_keys=True, default=str) + "\n"
    if r.get("backend") not in LIVE_BACKENDS and _live_ship_bar_met(outdir / "latest.json"):
        (outdir / "latest.fixture.json").write_text(body)      # T-045 r2: a fixture run must not replace the live run latest.json points at (board.py and --check-fresh read it)
    else:
        (outdir / "latest.json").write_text(body)
    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
        if write_calibration:
            (outdir / "calibration.json").write_text(body)
        else:
            scratch = outdir / "runs" / (scratch_ts or ts)
            scratch.mkdir(parents=True, exist_ok=True)
            (scratch / "calibration.json").write_text(body)
    return outdir / f"{ts}.md"


def _live_ship_bar_met(path):
    """True when `path` is a latest.json for a live-backend run whose ship bar was met."""
    try:
        d = json.loads(pathlib.Path(path).read_text())
    except (OSError, ValueError):
        return False
    return d.get("backend") in LIVE_BACKENDS and d.get("ship_bar_met") is True


def parse_report_md(text):
    """The machine-readable header of a dated eval report (.md) as written by render_md; raises ValueError naming what is missing."""
    def one(rx, what):
        m = re.search(rx, text, re.M)
        if not m:
            raise ValueError(f"report has no {what}")
        return m
    head = one(r"^# Eval report (\S+)$", "title line")
    bar = one(r"^\*\*ship_bar_met: (True|False)\*\*  backend `([^`]+)`  models `(\{.*\})`$", "ship_bar_met/backend/models line")
    src = one(r"^Source commit `([0-9a-f]+|unknown)`, tree (clean|DIRTY[^.]*|unknown)\.$", "source commit line")
    hs = dict((k, v) for k, v in re.findall(r"^- `((?:app/llm/prompts/[^`]+\.md)|app/llm/lexicon\.yaml)` ([0-9a-f]{64})$", text, re.M))
    if not hs:
        raise ValueError("report has no prompt and lexicon hashes")
    bl = re.search(r"^Blockers: (.*)$", text, re.M)
    sp = re.search(r"^spec_matches_golden: (True|False)$", text, re.M)
    return {"generated_at": head.group(1), "ship_bar_met": bar.group(1) == "True", "backend": bar.group(2), "models": json.loads(bar.group(3)),
            "source": {"commit": None if src.group(1) == "unknown" else src.group(1), "clean": {"clean": True, "unknown": None}.get(src.group(2), False)},
            "hashes": hs, "blockers": bl.group(1).split("; ") if bl else [],
            "spec_matches_golden": None if not sp else sp.group(1) == "True"}


def _num(x):
    return None if x in ("n/a", "not_measured", "None") else float(x)


def metrics_from_report_md(text):
    """The bar-relevant numbers of a rendered report body (render_md), as the dict shape ship_bar reads: (metrics, assertions, spec_matches_golden).
    Read from the table and the Assertions line, never from the `**ship_bar_met: X**` header. determinism_3run is completed from the per-run
    directory by recompute_ship_bar. Raises ValueError naming the row that is missing."""
    def row(rx, what):
        m = re.search(rx, text, re.M)
        if not m:
            raise ValueError(f"report body has no {what} row")
        return m.groups()
    g, gc = row(r"^\| grounding_rate \| (\S+) \((\d+) checked\)", "grounding_rate")
    (er,), (ar,) = row(r"^\| entry_recall \| (\S+) \|", "entry_recall"), row(r"^\| amount_recall \| (\S+) \|", "amount_recall")
    fp, fr = {}, {}
    for t in FLAG_TYPES:
        fp[t], fr[t] = (_num(x) for x in row(rf"^\| flag_precision\[{t}\] / flag_recall\[{t}\] \| (\S+) / (\S+) \|", f"flag[{t}]"))
    hv, hc, ht, hs, hu = row(r"^\| hallucination_catch_rate \| (\S+) \((\d+)/(\d+); (\w+); judge unavailable (\d+)\)", "hallucination_catch_rate")
    cu, ct = row(r"^\| controls judged unsupported \| (\d+) of (\d+)", "controls judged unsupported")
    (us,), (dt_,) = row(r"^\| unsupported_count_3run \| (\S+) \|", "unsupported_count_3run"), row(r"^\| determinism_3run \| (\S+) \|", "determinism_3run")
    (mn,), (up,), (c7,) = row(r"^\| golden_must_not_hits \| (\d+) \|", "golden_must_not_hits"), row(r"^\| unsplit_paste .*? \| (True|False) ", "unsplit_paste"), \
        row(r"^\| case_07_total_420 \| (True|False) \|", "case_07_total_420")
    jc = {"status": "measured", "value": None}
    for j in ("J3", "J4"):
        mt = re.search(rf"^\| {j} \S+ seeded catch rate \| \S+ \((\d+)/(\d+) wrong caught x(\d+) runs;.*?false agree \d+ (\[[^\]]*\]); .*?unavailable (\d+)\)", text, re.M)
        if not mt:
            jc = {"status": "not_measured", "value": None}
            break
        jc[j.lower()] = {"wrong_caught": int(mt.group(1)), "wrong_total": int(mt.group(2)), "repeats": int(mt.group(3)),
                         "false_agree": json.loads(mt.group(4).replace("'", '"')), "judge_unavailable_ids": ["?"] * int(mt.group(5))}
        if int(mt.group(5)):
            jc["status"] = "not_measured"
    bl = re.search(r"^Blockers: (.*)$", text, re.M)
    blockers = bl.group(1) if bl else ""
    ju = re.search(r"judge unavailable on (\d+) item\(s\) in the golden cases", blockers)
    tm = re.search(r"charge total differs from golden in ([^;]+)", blockers)
    dd = re.search(r"dedupe failures in ([^;]+)", blockers)
    lc = re.search(r"^\| letter_currency_outside_charges .*? \| (\S+) \| 0 \|", text, re.M)
    a = re.search(r"^Assertions: (\{.*\})$", text, re.M)
    sp = re.search(r"^spec_matches_golden: (True|False)$", text, re.M)
    if not a or not sp:
        raise ValueError("report body has no Assertions or spec_matches_golden line")
    m = {"grounding_rate": {"value": _num(g), "checked": int(gc)}, "entry_recall": {"value": _num(er), "dedupe_failures": [x.strip() for x in dd.group(1).split(",")] if dd else []},
         "amount_recall": {"value": _num(ar), "total_mismatch": [x.strip() for x in tm.group(1).split(",")] if tm else []},
         "flag_precision": fp, "flag_recall": fr,
         "hallucination_catch_rate": {"value": _num(hv), "caught": int(hc), "total": int(ht), "status": hs, "judge_unavailable_count": int(hu),
                                      "controls_unsupported": ["?"] * int(cu), "controls_total": int(ct)},
         "judge_unavailable_in_cases": {"value": int(ju.group(1)) if ju else 0, "per_case": {}},
         "unsupported_count_3run": {"value": _num(us), "runs": 3 if _num(us) is not None else None},
         "determinism_3run": {"value": _num(dt_), "runs": 3 if _num(dt_) is not None else None},
         "golden_must_not_hits": {"value": int(mn)}, "unsplit_paste": {"value": up == "True"}, "case_07_total_420": {"value": c7 == "True"},
         "judge_controls": jc}
    if lc and lc.group(1) not in ("not_measured", "None"):
        m["letter_currency_outside_charges"] = {"value": int(float(lc.group(1))), "per_case": []}
    return m, json.loads(a.group(1)), sp.group(1) == "True"


def determinism_from_run_dir(run_dir):
    """R-CO-7 determinism recomputed from the three per-run files (their `signature_parts`): the share of runs 2 and 3 equal to run 1.
    None unless the directory holds exactly run1.json, run2.json and run3.json."""
    d = pathlib.Path(run_dir)
    if not d.is_dir() or sorted(p.name for p in d.glob("run*.json")) != ["run1.json", "run2.json", "run3.json"]:
        return None
    sigs = [json.dumps(json.loads((d / f"run{i}.json").read_text())["signature_parts"], sort_keys=True, default=str) for i in (1, 2, 3)]
    return sum(s == sigs[0] for s in sigs[1:]) / 2


def recompute_ship_bar(text, root=ROOT):
    """(ship_bar_met, blockers, run_dir_relpath) for a dated report, from its body and its per-run directory, with the runner's own ship_bar().
    The header's ship_bar_met is not read. Raises ValueError when the evidence is missing: no per-run directory line, a directory that is not there,
    or one without exactly run1..run3."""
    hd = parse_report_md(text)
    m, a, spec = metrics_from_report_md(text)
    rd = re.search(r"^- per-run artifacts: `([^`]+)`$", text, re.M)
    if not rd:
        raise ValueError("report names no per-run directory (no `- per-run artifacts:` line); only a live run writes one")
    det = determinism_from_run_dir(pathlib.Path(root) / rd.group(1))
    if det is None:
        raise ValueError(f"per-run directory {rd.group(1)} is missing or does not hold exactly run1.json, run2.json and run3.json")
    m["determinism_3run"] = {"value": det, "runs": 3}          # measured here, not copied from the table
    blockers = ship_bar(m, a, hd["backend"], spec)[1]
    return not blockers, blockers, rd.group(1)


def record_latest(report_path, out=REPORTS, root=ROOT, now=None):
    """Point latest.json at an existing dated report without a run. The pointer is derived, not copied: the report must be a live backend's, its ship bar is
    recomputed by ship_bar() from the report body and its per-run directory, and a header that disagrees is refused (T-045 r3; R-CO-7: a fixture cannot satisfy
    the bar). `recorded_from` carries the report's sha256 and source commit so check_fresh can prove the report is unchanged. Returns 0, or 2 on a refusal."""
    rp, out = pathlib.Path(report_path), pathlib.Path(out)
    def refuse(why):
        print(f"evals.run: --record-latest refused, nothing written: {why}", file=sys.stderr)
        return 2
    try:
        text = rp.read_text()
        d = parse_report_md(text)
    except (OSError, ValueError) as e:
        return refuse(e)
    if rp.resolve().parent != out.resolve():
        return refuse(f"{rp} is not in {out}.")
    if d["backend"] not in LIVE_BACKENDS:
        return refuse(f"backend `{d['backend']}` is not a live backend ({', '.join(LIVE_BACKENDS)}); a fixture report cannot be the latest ship-bar record (R-CO-7).")
    try:
        met, blockers, run_dir = recompute_ship_bar(text, root)
    except ValueError as e:
        return refuse(e)
    if met != d["ship_bar_met"]:
        return refuse(f"header says ship_bar_met {d['ship_bar_met']} but the ship bar recomputed from the report body and {run_dir} is {met}"
                      + (f" (failing: {'; '.join(blockers)})" if blockers else "") + ".")
    d.update({"schema": "evals.run/1", "ship_bar_met": met, "recorded_from": {"report": rp.name, "sha256": sha256_file(rp), "source_commit": d["source"]["commit"],
              "run_artifacts": run_dir, "ship_bar_recomputed": True,
              "recorded_at": now or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "note": "pointer parsed from the report; ship_bar_met recomputed from its body and per-run directory (T-045 r3), not a run"}})
    out.mkdir(parents=True, exist_ok=True)
    (out / "latest.json").write_text(json.dumps(d, indent=1, sort_keys=True) + "\n")
    print(f"latest.json now points at {rp.name}: backend={d['backend']} ship_bar_met={d['ship_bar_met']} (recomputed) source_commit={d['source']['commit']}")
    return 0


def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
    p = pathlib.Path(latest_path)
    if not p.exists():
        print("check-fresh: no latest.json", file=sys.stderr)
        return 1
    data = json.loads(p.read_text())
    old, now = data.get("hashes", {}), hashes(root)
    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
    for k in diff:
        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
    rec = data.get("recorded_from")
    if rec:                                       # a pointer made by --record-latest: the report it names must still be the file it was parsed from
        rp = p.parent / rec.get("report", "")
        if not rp.is_file() or sha256_file(rp) != rec.get("sha256"):
            print(f"check-fresh: {rec.get('report')} is missing or changed since latest.json was recorded from it", file=sys.stderr)
            diff.append("recorded_from")
    bad = check_calibration(p.parent / "calibration.json", root)
    for m in bad:
        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
    return 1 if diff or bad else 0


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad


def load_pipeline():
    from app import pipeline
    return pipeline


class CuratedFixtures(Exception):
    pass


def refuse_curated(env=None):
    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
    env = os.environ if env is None else env
    d = env.get("LLM_FIXTURE_DIR", "").strip()
    curated_dir = ROOT / "tests" / "fixtures" / "llm" / "curated"
    in_curated = bool(d) and (pathlib.Path(d).resolve() == curated_dir.resolve() or curated_dir.resolve() in pathlib.Path(d).resolve().parents)
    if env.get("FIXTURE_SET", "").strip() == "curated" or in_curated:
        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under "
                              "tests/fixtures/llm/curated): curated responses reproduce the golden answers by construction (D-029). "
                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")


def normalize_backend(raw):
    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
    the caller must exit 2 rather than fall back to fixtures."""
    name = (raw or "").strip().lower() or "fixture"
    return name if name in KNOWN_BACKENDS else None


def run_controls_only(backend, out, ts):
    """Live J3/J4 controls alone (no pipeline): per-item verdicts on every repeat, written next to the other reports."""
    jc = judge_controls_metrics(load_controls(), default_judge_control(backend), repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1,
                                workers=4 if backend in LIVE_BACKENDS else 1)
    ok = controls_ok(jc)
    src = git_source()
    out.mkdir(parents=True, exist_ok=True)
    md = [f"# Judge controls {ts}", "", f"**controls_ok: {ok}**  backend `{backend}`  prompts `{control_prompt('j3')}`, `{control_prompt('j4')}` (hashes in the json)",
          f"Source commit `{src['commit'] or 'unknown'}`, tree {'clean' if src['clean'] else 'DIRTY, not reproducible from the commit' if src['clean'] is False else 'unknown'}.",
          "", "| Metric | Value | Bar | R-IDs |", "|---|---|---|---|", *render_controls(jc), *render_control_items(jc)]
    (out / f"controls-{ts}.md").write_text("\n".join(md) + "\n")
    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
                                                         "source_commit": src["commit"], "source_tree_clean": src["clean"], "source_tree": src["tree"], "hashes": hashes(), "judge_controls": jc}, indent=1, sort_keys=True) + "\n")
    print(f"controls_ok={ok} backend={backend} report={out / f'controls-{ts}.md'}")
    return 0 if ok else 1


def main(argv=None, pipeline=None):
    ap = argparse.ArgumentParser(prog="python -m evals.run")
    ap.add_argument("--check-fresh", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--record-latest", metavar="REPORT.md", default=None,
                    help="no run: point latest.json at an existing dated report in --out, every value parsed from it, with provenance (sha256 of the report)")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
    ap.add_argument("--write-calibration", action="store_true",
                    help="also write the committed calibration.json (out/calibration.json); refused unless the tree is clean at HEAD, tracked and untracked inputs alike (T-101)")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.check_fresh:
        return check_fresh(out / "latest.json")
    if a.record_latest:
        return record_latest(a.record_latest, out)
    if a.check_spec:
        s = check_spec()
        latest = out / "latest.json"
        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
        data.update(s)
        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
        out.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps(s))
        return 0 if s["spec_matches_golden"] else 1
    try:
        refuse_curated()
    except CuratedFixtures as e:
        print(f"evals.run: {e}", file=sys.stderr)
        return 2
    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
    backend = normalize_backend(raw)
    if backend is None:
        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
              f"Nothing was run.", file=sys.stderr)
        return 2
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    if a.write_calibration and a.controls:           # T-101 r2: controls mode writes no calibration, so the combination is refused, not silently ignored
        print("evals.run: --write-calibration cannot be combined with --controls (controls mode writes no calibration); nothing was run or written.",
              file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
        if why:
            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
            return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    from evals import letter_check
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None,
                          letters=letter_check.measure if real else None)
    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
        cal = report.get("calibration") or {}
        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"),
                                         "dirty": (git_source().get("dirty") or []) if cal.get("source_tree_clean") is False else []})
        if why:
            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
            return 2
    try:
        path = write_report(report, out, write_calibration=a.write_calibration, scratch_ts=ts)   # one run directory: runs/<ts> (T-101 r2)
    except CalibrationRefused as e:                  # backstop: write_report judges the header too
        print(f"evals.run: --write-calibration refused, nothing was written: {e}.", file=sys.stderr)
        return 2
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)


if __name__ == "__main__":
    sys.exit(main())
