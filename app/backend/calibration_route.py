"""GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).

Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
from those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.

Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
- "ok": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the
  served subset (SERVED below) plus two flags (T-102):
    stale        true when the prompt or lexicon hashes recorded in the file differ from the files on disk that the running app loads
                 (added, removed or edited since the run, committed or not); the counts then describe older prompts. A file that
                 records no hashes is stale too, and so is a state where the current files cannot be read (never shown as current).
    stale_reason a plain sentence naming the files that differ, or null when `stale` is false.
  The hashes themselves are not served.
- "missing": no file. `calibration` is null. Nothing is invented.
- "invalid": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other
  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.
The UI hides the accuracy line when `calibration` is null (T-096) and shows "numbers from an older version" when `stale` is true.
This module reads one fixed path and the prompt files on disk; it never writes.
"""
import hashlib
import json
import logging
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "evals" / "reports" / "calibration.json"
SCHEMA = "evals.calibration/1"
TYPES = ("entry", "amount", "flag")
STATES = ("verified", "needs_review")
SMALL_N = 30  # evals/run.py CAL_SMALL_N: fewer cases, or items in a state, than this is a small sample
SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
PROMPT_DIR = "app/llm/prompts"  # the same inputs evals/run.py hashes(): every prompt *.md and the lexicon
LEXICON = "app/llm/lexicon.yaml"
MISSING = "No calibration has been measured yet, so no accuracy line is shown."
INVALID = "The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run."
UNCHECKED = "The current prompts could not be read, so these numbers cannot be checked against them."
log = logging.getLogger("zlayt.calibration")


def _count(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def _cell_ok(c) -> bool:
    return isinstance(c, dict) and _count(c.get("matched")) and _count(c.get("total")) and c["matched"] <= c["total"]


def _by_case_ok(cell) -> bool:
    """Each case's [matched, total] has matched <= total, and the cases add up to the cell's own counts."""
    bc = cell["by_case"]
    if not all(isinstance(v, list) and len(v) == 2 and _count(v[0]) and _count(v[1]) and v[0] <= v[1] for v in bc.values()):
        return False
    return sum(v[0] for v in bc.values()) == cell["matched"] and sum(v[1] for v in bc.values()) == cell["total"]


def _statement_ok(text, cell, backend, case_count) -> bool:
    """A statement is a non-empty string that names the backend. When its cell has items it must also quote that cell's own m/t and the
    case count, as calibration_sentences in evals/run.py builds them. A hand-edited number or label fails here."""
    if not isinstance(text, str) or not text or f" on the {backend} backend" not in text:
        return False
    if cell["total"] == 0:
        return True
    return f"{cell['matched']}/{cell['total']} times" in text and f"{case_count} golden cases" in text


def problems(c) -> list:
    """Why `c` is not a valid calibration document. Empty list when it is. Checks the shape, the count ranges, that the state totals add up
    to the type totals, and that each statement quotes its own counts."""
    if not isinstance(c, dict):
        return ["not an object"]
    bad = []
    if c.get("schema") != SCHEMA:
        bad.append("schema")
    if not (isinstance(c.get("backend"), str) and c["backend"]):
        bad.append("backend")
    if not _count(c.get("case_count")):
        bad.append("case_count")
    if not isinstance(c.get("small_sample"), bool):
        bad.append("small_sample")
    if not (isinstance(c.get("source_commit"), str) and c["source_commit"]):
        bad.append("source_commit")
    if not isinstance(c.get("generated_at"), str):
        bad.append("generated_at")
    ns = c.get("not_scored")
    if not (isinstance(ns, dict) and all(_count(ns.get(k)) for k in TYPES + ("total",)) and ns["total"] == sum(ns[t] for t in TYPES)):
        bad.append("not_scored")
    bs, bt, se = c.get("by_state"), c.get("by_type"), c.get("sentences")
    if not (isinstance(bs, dict) and isinstance(bt, dict) and all(isinstance(bt.get(t), dict) for t in TYPES)):
        return bad + ["by_state or by_type"]
    for s in STATES:
        if not (_cell_ok(bs.get(s)) and isinstance(bs[s].get("cases"), list) and all(isinstance(x, str) for x in bs[s]["cases"])):
            bad.append(f"by_state.{s}")
            continue
        for k in ("matched", "total"):
            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
                bad.append(f"by_state.{s}.{k} is not the sum over by_type (hand-edited count)")
    for t in TYPES:
        for s in STATES:
            cell = (bt.get(t) or {}).get(s)
            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
                bad.append(f"by_type.{t}.{s}")
            elif not _by_case_ok(cell):
                bad.append(f"by_type.{t}.{s}.by_case does not add up to its cell")
    if bad:
        return bad
    cases = c.get("cases")
    if not (isinstance(cases, list) and all(isinstance(x, str) for x in cases) and len(cases) == c["case_count"]):
        bad.append("case_count is not the number of cases")
    if c["small_sample"] != (c["case_count"] < SMALL_N or any(bs[s]["total"] < SMALL_N for s in STATES)):
        bad.append("small_sample is not the sample-size rule")
    if not (isinstance(se, dict) and isinstance(se.get("overall"), dict) and isinstance(se.get("by_type"), dict)):
        return bad + ["sentences"]
    for s in STATES:
        if not _statement_ok(se["overall"].get(s), bs[s], c["backend"], c["case_count"]):
            bad.append(f"sentences.overall.{s} does not quote its counts")
    for t in TYPES:
        for s in STATES:
            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s], c["backend"], c["case_count"]):
                bad.append(f"sentences.by_type.{t}.{s} does not quote its counts")
    return bad


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def disk_prompt_hashes(root=ROOT) -> dict:
    """The prompt and lexicon hashes read from the working tree: the set evals/run.py hashes() records. The route compares against these, not HEAD."""
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / PROMPT_DIR).glob("*.md")):
        out[p.relative_to(root).as_posix()] = _sha256(p.read_bytes())
    if (root / LEXICON).exists():
        out[LEXICON] = _sha256((root / LEXICON).read_bytes())
    return out


def current_prompt_hashes(root=ROOT) -> dict:
    """What the prompts are now: the files on disk under `root`, which are the files the running app loads (app/llm/promptlib.py reads them
    from disk). Deliberately not HEAD: a prompt edited and not yet committed already changes what the pipeline runs, so it must read as stale."""
    return disk_prompt_hashes(root)


def stale_reason(doc, current):
    """Why the measurement in `doc` no longer matches the prompts in `current`, or None. Compared name by name: a prompt added, removed or
    edited since the run means the counts describe other prompts. A file that records no hashes cannot be shown current."""
    recorded = doc.get("hashes")
    if not isinstance(recorded, dict) or not recorded:
        return "This measurement does not record which AI instructions it used, so it cannot be checked against the current ones."
    changed = sorted(k for k in set(recorded) | set(current) if recorded.get(k) != current.get(k))
    if not changed:
        return None

    def describe(k):
        name = pathlib.PurePosixPath(k).name
        if k not in recorded:
            return f"{name} is new"
        if k not in current:
            return f"{name} was removed"
        return f"{name} changed"
    shown = "; ".join(describe(k) for k in changed[:8])
    more = f"; and {len(changed) - 8} more" if len(changed) > 8 else ""
    return f"The AI's instructions have changed since these numbers were measured: {shown}{more}. The numbers describe an earlier version and may be out of date."


def _envelope(status, calibration=None, message=None) -> dict:
    return {"status": status, "calibration": calibration, "message": message}


def load(path=REPORT, root=ROOT) -> dict:
    """The envelope for the file at `path`: ok with the served subset and the stale flags, missing, or invalid. Read-only; never raises.
    `root` is the tree whose prompt files (on disk) the file is compared with."""
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _envelope("missing", message=MISSING)
    except (OSError, UnicodeDecodeError):
        log.warning("calibration file could not be read: %s", p.name)
        return _envelope("invalid", message=INVALID)
    try:
        doc = json.loads(raw)
    except ValueError:
        log.warning("calibration file is not JSON: %s", p.name)
        return _envelope("invalid", message=INVALID)
    bad = problems(doc)
    if bad:
        log.warning("calibration file rejected: %s", "; ".join(bad))
        return _envelope("invalid", message=INVALID)
    try:
        why = stale_reason(doc, current_prompt_hashes(root))
    except OSError:
        log.warning("current prompt files could not be read under %s", pathlib.Path(root).name)
        why = UNCHECKED
    served = {k: doc[k] for k in SERVED}
    served.update(stale=why is not None, stale_reason=why)
    return _envelope("ok", served)


def add_routes(app, *, path=REPORT, root=ROOT):
    @app.get("/api/calibration")
    def calibration():
        return load(path, root)
