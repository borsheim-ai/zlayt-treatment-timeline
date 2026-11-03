#!/usr/bin/env python3
"""Library report (T-079): scores every evals/library packet with evals.run's scoring functions. REPORTED, NOT GATED (D-031): no exit code
depends on a score; the ship bar (evals.run) still measures only evals/golden. It only exits non-zero when a packet cannot be run at all.

Run:  .venv/bin/python -m evals.library_report [--out evals/reports/library-latest.md]     (fixture backend; no network)
Honest failures are shown, not hidden: a record whose extract call has no recorded fixture shows as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS),
the same rule as lib01.
"""
import argparse
import json
import pathlib
import subprocess
import sys

from evals import run as R

LIB = R.ROOT / "evals" / "library"


def expected_accept_all_cents(exp):
    """The total the letter should print when every acceptable line is accepted one at a time (D-059): `totals.accept_all_total` when the packet records one
    (with its written reason), else the hand-verified `explicit_charges_total`."""
    t = exp["totals"]
    return round(t.get("accept_all_total", t["explicit_charges_total"]) * 100)


def accept_all_total_cents(out):
    """T-140 / D-059: the total the letter would print if the paralegal accepted every amount the tool found (charges, unclear, rate, estimate) ONE AT A TIME,
    through the real export builder (export.build_export), not a sum of charge-class figures. A charge carrying a likely-duplicate or likely-total flag cannot
    be accepted without a named confirm, so it is not accepted here. Items rejected by the code check are not offered for review and are left out.
    None when the letter has no total line (no accepted charge)."""
    from app.backend import export
    case = dict(records=[dict(n=r["n"], source=r.get("source"), date_iso=r.get("date_iso"), excerpt=r["excerpt"], text=r.get("text") or r["excerpt"]) for r in out["records"]],
                entries=[], flags=[], pending_count=0, events=[],
                amounts=[dict(id=a["id"], record_no=a["record_nos"][0], cents=a["cents"], cls=a["kind"], raw=a["raw"], excerpt=a["excerpt"], review_status="accepted")
                         for a in out.get("amounts") or [] if a.get("state") != "rejected" and not a.get("confirm") and not (a.get("ladder") or {}).get("confirm")])
    for line in export.build_export(case)["letter_text"].splitlines():
        if line.startswith("Billed charges accepted from these records: $"):
            return round(float(line.rsplit("$", 1)[1].replace(",", "")) * 100)
    return None


def score(name, text, exp, pipeline):
    out = pipeline.run_case(text, "fixture")
    want = expected_accept_all_cents(exp)
    got = accept_all_total_cents(out)
    accept_all = "ok" if (got or 0) == want else f"WRONG {export_usd(got)} vs {export_usd(want)}"
    e, a, f = R.score_entries(exp, out), R.score_amounts(exp, out), R.score_flags(exp, out)
    errs = [(x.get("code"), x.get("record_no"), x.get("cause")) for x in out.get("errors") or []]
    must = sum(v["must"] for v in f["per_type"].values())
    found = sum(v["must_found"] for v in f["per_type"].values())
    return {"case": name, "accept_all": accept_all, "accept_all_ok": accept_all == "ok", "entries": f"{e['found']}/{e['total']}", "amounts": f"{a['found']}/{a['total']}", "total_ok": a["total_ok"],
            "must_flags": f"{found}/{must}", "must_not_flag_hits": len(f["must_not_flag_hits"]), "must_not_hits": R.check_must_not(exp, out),
            "gap_rows_wrong": len(f["gap_rows_wrong"]), "errors": errs, "status": out.get("status")}


def export_usd(cents):
    return "none" if cents is None else f"${cents // 100:,}.{cents % 100:02d}"


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=R.ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:   # noqa: BLE001 - provenance is best effort; the report still prints
        return ""


def provenance():
    """Source commit and dirty state of the tree the report ran in (a report is only reproducible from a clean tree)."""
    sha = _git("rev-parse", "HEAD") or "unknown"
    dirty = [l for l in _git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
    return sha, ("clean" if not dirty and sha != "unknown" else f"DIRTY ({len(dirty)} tracked paths differ)" if dirty else "unknown")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
    a = ap.parse_args(argv)
    pipeline = R.load_pipeline()
    rows = []
    for p in sorted(LIB.glob("case_*.txt")):
        rows.append(score(p.stem, p.read_text(), json.loads(p.with_name(p.stem + ".expected.json").read_text()), pipeline))
    sha, state = provenance()
    lines = ["# Library report (reported, not gated)", "", f"Source commit: {sha} (tree: {state}). Regenerate from a clean worktree of the commit you cite.", "",
             "Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.", "",
             "| packet | status | entries | amounts | total ok | accept-all total | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['status']} | {r['entries']} | {r['amounts']} | {r['total_ok']} | {r['accept_all']} | {r['must_flags']} | {r['must_not_flag_hits']} | "
                     f"{', '.join(r['must_not_hits']) or '-'} | {r['gap_rows_wrong']} | {'; '.join(f'{c} r{n} {k}' for c, n, k in r['errors']) or '-'} |")
    lines += ["", "## Known honest failures (generated from the run above)", ""]
    fails = [(r["case"], c, n, k) for r in rows for c, n, k in r["errors"]]
    if fails:
        lines += ["| packet | record | code | cause |", "|---|---|---|---|"] + [f"| {p} | r{n} | {c} | {k or 'not captured'} |" for p, c, n, k in fails]
    else:
        lines += ["None at this commit: every record of every packet replays from a recorded fixture on the fixture backend."]
    lines += ["", "History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt "
              "in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract "
              "(T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call)."]
    pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
