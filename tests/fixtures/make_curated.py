"""Builds tests/fixtures/llm/curated/ (D-029, T-051): HAND-CHECKED generator/judge responses that reproduce the golden summaries and
excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a model.
Run:  .venv/bin/python tests/fixtures/make_curated.py [--check]
Judge answers (any schema with a "verdict") are NEVER scripted (T-115 r2, D-029): the build replays the real recorded model answer from
tests/fixtures/llm/<key>.json and, on a miss, records one live (ENABLE_LIVE=1 LLM_BACKEND=claude-cli, at most 3 attempts). No curated
judge file is written, so a curated answer can never shadow a recording; the check replays curated first, then the recorded set.
The script runs the real pipeline on evals/golden/sample.txt with the provider patched to these scripted answers, writes one
<sha256>.json per distinct prompt (key = provider.prompt_hash), each with a top-level "CURATED" header, then replays the set through the
real fixture backend and checks the export against evals/golden/sample.export.expected.txt.
"""
import json, os, pathlib, sys, tempfile, time
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("LLM_BACKEND", "fixture")
OUT = ROOT / "tests" / "fixtures" / "llm" / "curated"
MAX_LIVE_ATTEMPTS = 3
import threading
_LIVE_LOCK = threading.Lock()
HEADER = ("CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from "
          "sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).")

from tests.unit import _golden as G
from app.backend import ingest
from tests.unit._fakes import golden_summaries, which_record
from app.llm import provider as P
from app.llm._types import LLMResult

SUMS = golden_summaries()
GOLD = G.expected("sample")
# per-record LLM flags (type, category, verbatim span) taken from sample.expected.json evidence
FLAGS = {
    3: [("pre_existing", "pre_existing", "Patient reports low back pain in 2023, resolved.")],
    6: [("causation", "missed_care", "Discharged from PT after two missed appointments.")],
    7: [("causation", "new_onset", "New onset pain")],
    8: [("pre_existing", "degenerative_language", "Findings may represent degenerative change"),
        ("causation", "speculative_language", "may represent degenerative change; correlate clinically")],
    9: [("causation", "patient_report", "Patient states symptoms began after the January collision.")],
}
CONFLICT = dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.",
                excerpt_b="Discharged from PT after two missed appointments.")

NARR_OVERRIDE = {6: "Discharged from PT after two missed appointments; pain 3/10."}

def answer(system, user, schema):
    props = set(schema.get("properties", {}))
    if "sentences" in props:                      # narrative paragraph (T-059): one firm-voice sentence per accepted entry, from the golden summary
        import re
        # entry 6: the golden summary says "physical therapy" while the quote says "PT", which the code check reads as new adverse wording
        sents = [dict(entry_id=m.group(1), text=f"On {m.group(3)}, {m.group(4)}: " + NARR_OVERRIDE.get(int(m.group(2)), SUMS[int(m.group(2))][0]))
                 for m in re.finditer(r"^ENTRY (e(\d+)) \| (.*?) \| (.*)$", user, re.M)]
        return dict(sentences=sents)
    if {"summary", "excerpt"} <= props:
        n = which_record(user)[0]
        return dict(summary=SUMS[n][0], excerpt=SUMS[n][1])
    if "verdict" in props:
        enum = schema["properties"]["verdict"].get("enum") or []
        v = {"supported": "supported", "agree": "agree", "conflict": "conflict"}
        pick = next((x for x in ("supported", "agree", "conflict") if x in enum), enum[0])
        return dict(verdict=pick, reason_code="NONE")
    if "flags" in props:
        recs = which_record(user)
        if len(recs) > 1:                     # cross-record conflicts pass
            return dict(flags=[CONFLICT])
        out = [dict(type=t, category=c, excerpt=x, excerpt_b=None) for t, c, x in FLAGS.get(recs[0], [])] if recs else []
        return dict(flags=out)
    raise SystemExit(f"unknown schema for curated answer: {sorted(props)}")

def accept_all(conn, cid, out, call):
    from app.backend import review
    for kind in ("entries", "amounts", "flags"):
        for it in out[kind]:
            if it.get("state") != "rejected":
                try:
                    review.apply_review(conn, cid, it["id"], {"action": "accept"}, call=call)
                except Exception as e:
                    print("accept failed", it["id"], getattr(e, "code", e))


def build():
    from app.db import db as DB
    from app.backend import pipeline as PL
    from app.llm import audited as AU
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.json"):
        f.unlink()
    written = {}
    def judge(model, system, user, schema):
        """Real model answer for a judge prompt: recorded if present, else live (<= 3 attempts) and recorded to the default dir."""
        key = P.prompt_hash(model, system, user, schema)
        try:
            return P._fixture.call(model, system, user, schema, key=key)
        except P.FixtureMiss:
            pass
        if P.backend_name() == "fixture":
            raise SystemExit(f"no recorded judge answer for {key[:12]} and no live backend: rerun with ENABLE_LIVE=1 LLM_BACKEND=claude-cli")
        want = next((x for x in ("supported", "agree", "conflict") if x in (schema["properties"]["verdict"].get("enum") or [])), None)
        with _LIVE_LOCK:                                      # judges run in threads; record_context and the env flag are process-global
            try:
                return P._fixture.call(model, system, user, schema, key=key)     # another thread recorded it meanwhile
            except P.FixtureMiss:
                pass
            os.environ["RECORD_FIXTURES"] = "1"
            try:
                for attempt in range(1, MAX_LIVE_ATTEMPTS + 1):
                    try:
                        with P.record_context(G.raw("sample")):
                            res = real(model, system, user, schema)
                    except Exception as e:                   # backend error / invalid JSON: counts as an attempt
                        print(f"judge {key[:8]} attempt {attempt}: {type(e).__name__} {e}")
                        continue
                    print(f"judge {key[:8]} attempt {attempt}: {res.output['verdict']} {res.output.get('reason_code')} (golden path expects {want})")
                    if res.output["verdict"] == want:
                        return res
                raise SystemExit(f"judge {key[:8]}: no accepted answer in {MAX_LIVE_ATTEMPTS} attempts; last recorded answer stays in tests/fixtures/llm")
            finally:
                os.environ.pop("RECORD_FIXTURES", None)

    def fake(model, system, user, schema):
        if "verdict" in schema.get("properties", {}):
            return judge(model, system, user, schema)
        key = P.prompt_hash(model, system, user, schema)
        out = answer(system, user, schema)
        written[key] = dict(CURATED=HEADER, output=out,
                            recorded_from=dict(backend="curated", model="hand-checked (qa)", recorded_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
        return LLMResult(output=out, backend="fixture", model_resolved=model, recorded_from=written[key]["recorded_from"])
    real = P.complete_with_meta
    P.complete_with_meta = fake
    try:
        tmp = tempfile.mkdtemp()
        conn = DB.connect(os.path.join(tmp, "c.sqlite")); cid = DB.create_case(conn, ingest.normalize_text(G.raw("sample")), now=1.0)   # the API stores normalised text; the narrative nonce hashes it
        call = AU.make_call(conn, cid)
        out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
        accept_all(conn, cid, out, call)
        from app.backend import narrative
        narrative.draft(conn, cid, call=call, now=1.0)
    finally:
        P.complete_with_meta = real
    for k, v in written.items():
        (OUT / f"{k}.json").write_text(json.dumps(v, indent=1, sort_keys=True))
    return len(written)

def check():
    """Replays through the REAL fixture backend; accepts everything; compares letter_text with the golden file."""
    os.environ.pop("LLM_FIXTURE_DIR", None)
    os.environ["FIXTURE_SET"] = "curated"        # curated first, then the recorded set (judge answers are recordings only)
    os.environ["LLM_BACKEND"] = "fixture"
    from app.db import db as DB
    from app.backend import pipeline as PL, store, export, review
    from app.llm import audited as AU
    tmp = tempfile.mkdtemp()
    conn = DB.connect(os.path.join(tmp, "r.sqlite")); cid = DB.create_case(conn, ingest.normalize_text(G.raw("sample")), now=1.0)
    call = AU.make_call(conn, cid)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    bad = [(e["id"], e["state"], e["reasons"]) for e in out["entries"] if e["state"] != "verified"]
    print("entries:", len(out["entries"]), "non-verified:", bad)
    from app.db import db as DB2
    for kind in ("entry", "amount", "flag"):
        for it in DB2.list_items(conn, cid, kind):
            if it["review_status"] == "pending" and it["state"] != "rejected":
                try:
                    review.apply_review(conn, cid, it["id"], {"action": "accept"}, call=call)
                except Exception as e:
                    print("accept failed", it["id"], it.get("text") or it.get("summary"), getattr(e, "code", e))
    ex = export.build_export(store.export_case(conn, cid))
    from app.backend import narrative
    nar = narrative.draft(conn, cid, call=call, now=1.0)
    print("narrative:", nar.get("error") or f"{len(nar['sentences'])} sentences, removed: {[(r['entry_id'], r['reason']) for r in nar['removed']]}")
    g = (G.G / "sample.export.expected.txt").read_text()
    gl = g.split("=== INTERNAL_NOTES_TEXT")[0].split("\n", 1)[1].rstrip("\n")
    gn = g.split("=== INTERNAL_NOTES_TEXT")[1].split("\n", 1)[1].rstrip("\n")
    notes = ex["internal_notes_text"].replace(export.AI_LINE_PREPARED.split("{n}")[0], export.AI_LINE.split("{n}")[0])      # D-069: the golden predates the prepared disclosure line; every other byte must match
    print("letter equal:", ex["letter_text"] == gl, "| notes equal:", notes == gn)
    if ex["letter_text"] != gl:
        import difflib
        print("\n".join(list(difflib.unified_diff(gl.split("\n"), ex["letter_text"].split("\n"), "golden", "got", lineterm=""))[:30]))
    return ex["letter_text"] == gl

if __name__ == "__main__":
    if "--check" not in sys.argv:
        print("curated files written:", build())
    sys.exit(0 if check() else 1)
