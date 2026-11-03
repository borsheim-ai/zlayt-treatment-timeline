"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]


def sample_script(**over):
    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
          "conflicts": {"flags": []}, "flags": {"flags": []}}
    sc.update(over)
    return sc

def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
    from app.backend import pipeline as PL
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
    call = call or FakeCall(sample_script())
    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call

def items_for(out, n):
    """Every entry-like item (timeline, undated, tray) that cites record number n."""
    rid = f"r{n}"
    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
    return [i for i in pool if rid in i.get("record_ids", [])]
