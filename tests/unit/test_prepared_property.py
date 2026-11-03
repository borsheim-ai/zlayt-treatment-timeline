"""T-177 round 4 (D-069): a property test over fault-injected curated sets.

Property: when the answers in use are the team's prepared ones (the fixture set is named `curated`), NO text an API response carries for the case or any of its items
matches /\\bAI\\b|claude|sonnet|haiku|opus|model/i, except the exact D-065 tooltip sentence. The same holds when a prepared answer is malformed, empty or missing: a malformed
or empty answer is treated as missing, never as a model's output.

How the sets are built: run the case once on the recorded set, read which fixture keys its generator steps used, and write a copy of the whole recorded set to
<tmp>/curated/ where each of those generator answers is relabelled `recorded_from.backend = "curated"` (a prepared answer with the same content). Then one fault is injected:
  valid      the answers as they are
  malformed  the answer's required keys are removed (the schema check fails on every attempt)
  empty      the answer is an empty object
  missing    the answer file is not there
  unsupported  a well-formed answer whose summary says something its quote does not (code removes it: SUMMARY_NOT_IN_QUOTE and the skipped steps)
each applied to one answer (the first extract answer) or to every generator answer. The judge answers stay the recorded ones (they are real model answers).
Cases: the sample (shipped curated set too) and two library cases (library routes exist in local mode only).

What is scanned: every string VALUE (never a key) in every response of the case: case, status, trace, judges, audit, narrative, billing, export (before and after accepting),
dismissal suggestions, and each item and its trace. The one structured exception is the identity of the real second-check model: an identifier with no whitespace (a model id,
a backend name, a prompt version) inside a judge context (a `judge` key, a call row with role judge, a judge step). Sentences are never exempt: a sentence that mentions
the second check must say "second check", not "AI".
"""
import json
import os
import re
import shutil
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

FORBIDDEN = re.compile(r"\bAI\b|claude|sonnet|haiku|opus|model", re.I)
TOOLTIP = "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."      # D-065, exact
LIBRARY = ("case_lib09_spanish_interpreter_espalda", "case_lib10_eob_ub04_cms1500")
SRC = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
PREPARED_MODEL = "hand-checked (qa)"
FAULTS = ("valid", "malformed", "empty", "missing", "unsupported")
UNSUPPORTED_SUMMARY = "Patient received a lumbar epidural steroid injection of 4 mL and was diagnosed with a herniated disc at L4-L5."
SCOPES = ("one", "all")


def _client(tmp_path, monkeypatch, *, fixture_dir=None, fixture_set=None, mode="local"):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    if mode:
        monkeypatch.setenv("ZLAYT_MODE", mode)
    else:
        monkeypatch.delenv("ZLAYT_MODE", raising=False)
    for k in ("ANTHROPIC_API_KEY", "ENABLE_LIVE", "LLM_FIXTURE_DIR", "FIXTURE_SET"):
        monkeypatch.delenv(k, raising=False)
    if fixture_set:
        monkeypatch.setenv("FIXTURE_SET", fixture_set)
    if fixture_dir:
        monkeypatch.setenv("LLM_FIXTURE_DIR", str(fixture_dir))
    db = tmp_path / "p.sqlite"
    return TestClient(create_app(str(db), static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), db


def _new_case(c, case):
    r = c.post("/api/cases", json={"sample": True} if case == "sample" else {"library": case})
    assert r.status_code == 201, r.text
    return r.json()["token"]


def _run(c, tok):
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            return s
        time.sleep(0.25)
    raise AssertionError("run did not finish")


def _generator_keys(tmp_path, monkeypatch, case):
    """The fixture keys the case's generator steps asked for on the recorded set, in call order (first attempt of each step)."""
    c, db = _client(tmp_path / "rec", monkeypatch)
    tok = _new_case(c, case)
    _run(c, tok)
    conn = sqlite3.connect(str(db))
    rows = conn.execute("SELECT step, item_id, prompt_sha256, parsed_ok FROM llm_calls WHERE role='generator' ORDER BY item_id, created_at, rowid").fetchall()
    conn.close()
    keys = []
    for step, item_id, key, ok in rows:
        if os.path.isfile(os.path.join(SRC, f"{key}.json")) and (step, key) not in keys:      # every generator answer that was recorded, whether or not it parsed; the first extract is e1's on the sample
            keys.append((step, key))
    return keys


def _break(path, fault):
    if fault == "missing":
        os.unlink(path)
        return
    with open(path) as f:
        d = json.load(f)
    if fault == "empty":
        d["output"] = {}
    elif fault == "unsupported":
        if isinstance(d.get("output"), dict) and "summary" in d["output"]:
            d["output"]["summary"] = UNSUPPORTED_SUMMARY      # well formed, but nothing in the quote supports it
    else:      # malformed: the required keys are gone and an unknown one is added, so the schema check fails every attempt
        d["output"] = {"unexpected": "not the shape the step asks for"}
    with open(path, "w") as f:
        json.dump(d, f)


def build_set(root, keys, fault, scope):
    """<root>/curated/: the recorded set, with the case's generator answers relabelled prepared and the fault injected into the first extract answer or into all."""
    d = os.path.join(root, "curated")
    os.makedirs(d)
    for f in os.listdir(SRC):
        if f.endswith(".json"):
            shutil.copy(os.path.join(SRC, f), d)
    for _, key in keys:
        p = os.path.join(d, f"{key}.json")
        with open(p) as f:
            o = json.load(f)
        o["recorded_from"] = {"backend": "curated", "model": PREPARED_MODEL, "recorded_at": "2026-11-02T00:00:00Z"}
        with open(p, "w") as f:
            json.dump(o, f)
    if fault != "valid":
        targets = [k for s, k in keys if s.startswith("extract")][:1] if scope == "one" else [k for _, k in keys]
        for key in targets:
            _break(os.path.join(d, f"{key}.json"), fault)
    return d


# ------------------------------------------------------------------ scanning
def _is_ident(s):
    return not re.search(r"\s", s)


VERBATIM_KEYS = {"system_text", "user_text", "response_raw", "raw"}      # the prompt a call carried and the answer it returned, stored word for word (local-mode audit): model I/O, not a statement made to the reader
JUDGE_MODELS = {"claude-haiku-5-5"}      # the real second-check model; the case's `models.judge` is added at run time


def strings(o, path="", judge=False):
    """(path, value, in_judge_context) for every string value, never a key. Verbatim model I/O fields are skipped."""
    if isinstance(o, dict):
        is_judge = judge or o.get("role") == "judge" or str(o.get("id", "")).startswith("judge") or str(o.get("step", "")).startswith(("judge", "j1", "j2", "j3", "j4"))
        for k, v in o.items():
            if k in VERBATIM_KEYS:
                continue
            yield from strings(v, f"{path}.{k}", is_judge or str(k).startswith("judge"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f"{path}[{i}]", judge)
    elif isinstance(o, str):
        yield path, o, judge


def offenders(label, payload, judge_models=frozenset(JUDGE_MODELS)):
    """(label, path, matched word, text) for each string that matches FORBIDDEN, minus the D-065 tooltip sentence. Exempt, and only these: an identifier with no whitespace
    (model id, backend name, prompt version) in a judge context, or exactly the real second-check model's id anywhere (e.g. a judge's objection row)."""
    out = []
    for path, s, judge in strings(payload):
        t = s.replace(TOOLTIP, "")
        m = FORBIDDEN.search(t)
        if m and not ((judge and _is_ident(s)) or s in judge_models):
            out.append((label, re.sub(r"\[\d+\]", "[]", path), m.group(0), s[:160]))
    return out


def actions(c, tok, case, res, get):
    """D-069 r5: the paths a reviewer takes that the plain accept pass does not. (1) Edit the quote of the first two prepared entries to their first sentence, then accept them:
    the second check has no recorded answer on the new quote, so the item, trace and export say so in the prepared voice. (2) Accept one entry that still has no second-check answer.
    (3) Write a manual entry for each record that has no live entry (a rejected or failed prepared answer), then read it. Every response, refusals included, is kept."""
    recs = {r["id"]: r for r in case.get("records", [])}
    live = [e for e in case.get("entries", []) if e.get("state") != "rejected"]
    edited = 0
    for e in live:
        rec = recs.get((e.get("record_ids") or [None])[0]) or {}
        sents = [x["text"] for x in rec.get("sentences", [])]
        if len(sents) < 2 or edited >= 2:
            continue
        runs = [" ".join(sents[i:j]) for n in range(len(sents) - 1, 0, -1) for i in range(len(sents) - n + 1) for j in (i + n,)]      # shorter quotes made of whole sentences, longest first
        for k, q in enumerate(runs):
            r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "edit", "edits": {"excerpt": q}})
            res[f"edit{k}:{e['id']}" if r.status_code != 200 else f"edit:{e['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            if r.status_code == 200:
                edited += 1
                break
        get(f"item-edited:{e['id']}", f"/items/{e['id']}")      # edited, not yet accepted: "you changed the quote, the second check has no answer"
        get(f"trace-edited:{e['id']}", f"/items/{e['id']}/trace")
        get(f"trace-edited-case:{e['id']}", "/trace")
        get(f"export-edited:{e['id']}", "/export")
        c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"})      # then accepted: the export names the second check that never ran
        get(f"item-accepted:{e['id']}", f"/items/{e['id']}")
        get(f"trace-accepted:{e['id']}", f"/items/{e['id']}/trace")
    for e in live[2:3]:      # accepted without ever editing: the second check's answer is whatever the set has
        r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"})
        res[f"accept-plain:{e['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    have = {rid for e in live for rid in (e.get("record_ids") or [])}
    for rid, rec in recs.items():
        if rid in have or rec.get("duplicate_of") or not rec.get("sentences"):
            continue
        first = rec["sentences"][0]["text"]
        r = c.post(f"/api/cases/{tok}/records/{rid}/entry", json={"summary": first, "excerpt": first})
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        res[f"manual:{rid}"] = body
        mid = (body.get("item") or body).get("id") if isinstance(body, dict) else None
        if mid:
            get(f"item-manual:{mid}", f"/items/{mid}")
            get(f"trace-manual:{mid}", f"/items/{mid}/trace")
    get("case-actions", "")
    get("export-actions", "/export")
    get("trace-actions", "/trace")
    get("judges-actions", "/judges")
    get("narrative-actions", "/narrative")


def collect(c, tok, do_actions=True):
    """Every response of the case, as {label: json}. Includes refusals (a 422 body is a response too)."""
    res = {}

    def get(label, path):
        r = c.get(f"/api/cases/{tok}{path}")
        try:
            res[label] = r.json()
        except ValueError:
            pass
        return r

    case = get("case", "").json()
    for p in ("/status", "/trace", "/judges", "/audit", "/narrative", "/billing", "/dismissal_suggestions", "/export"):
        get(p, p)
    ids = [x["id"] for k in ("entries", "flags", "amounts") for x in case.get(k, [])] + [x["id"] for x in case.get("tray", []) if isinstance(x, dict) and x.get("id")]
    for iid in ids:
        get(f"item:{iid}", f"/items/{iid}")
        get(f"trace:{iid}", f"/items/{iid}/trace")
    if do_actions:
        actions(c, tok, case, res, get)
    case = get("case-before-accept", "").json()
    for iid in [x["id"] for x in case.get("entries", []) if x.get("review_status") not in ("accepted", "edited")]:      # decide: accept each entry, and dismiss the first flag; then read the case, the export and the first entry again
        r = c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "accept"})
        res[f"accept:{iid}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    for f in case.get("flags", [])[:1]:
        r = c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "dismiss"})
        res[f"dismiss:{f['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    get("case-after", "")
    get("export-after", "/export")
    get("trace-after", "/trace")
    for iid in ids[:3]:
        get(f"trace-after:{iid}", f"/items/{iid}/trace")
    return res


def prepared_items(res):
    return [k for k, v in res.items() if k.startswith("item:") and isinstance(v, dict) and (v.get("item") or {}).get("prepared") is True]


def run_variant(tmp_path, monkeypatch, case, fault, scope, shipped=False, mode="local", do_actions=True):
    if shipped:
        c, _ = _client(tmp_path / "run", monkeypatch, fixture_set="curated", mode=mode)
    else:
        keys = _generator_keys(tmp_path / "keys", monkeypatch, case)
        assert keys, f"no generator fixtures for {case}"
        c, _ = _client(tmp_path / "run", monkeypatch, fixture_dir=build_set(str(tmp_path / "set"), keys, fault, scope), mode=mode)
    tok = _new_case(c, case)
    status = _run(c, tok)
    return c, tok, status, collect(c, tok, do_actions)


def _assert_clean(res, where):
    bad = []
    for label, payload in res.items():
        bad += offenders(label, payload, frozenset(JUDGE_MODELS | {((res.get('case') or {}).get('models') or {}).get('judge')}))
    seen = {}
    for label, path, word, s in bad:
        seen.setdefault((re.sub(r"[:].*", "", label), path, word), s)
    assert not seen, f"{where}: {len(bad)} string(s) for a prepared case match {FORBIDDEN.pattern}:\n" + "\n".join(f"  {k}: {v}" for k, v in sorted(seen.items())[:40])


# ------------------------------------------------------------------ the property
@pytest.fixture(autouse=True)
def _dirs(tmp_path):
    for n in ("rec", "keys", "run", "set"):
        (tmp_path / n).mkdir()


@pytest.mark.parametrize("scope", SCOPES)
@pytest.mark.parametrize("fault", FAULTS)
@pytest.mark.parametrize("case", ("sample",) + LIBRARY)
def test_no_prepared_text_names_an_ai_or_a_model(tmp_path, monkeypatch, case, fault, scope):
    if fault == "valid" and scope == "all":
        pytest.skip("valid has no scope")
    c, tok, status, res = run_variant(tmp_path, monkeypatch, case, fault, scope)
    where = f"{case}/{fault}/{scope}"
    if fault == "valid":
        assert prepared_items(res), f"{where}: no item is marked prepared, so the property would be vacuous"
    cm = res["case"].get("models") or {}
    assert cm.get("generator") == PREPARED_MODEL and cm.get("generator_prepared") is True, (where, cm)      # a broken answer never flips the case back to a model label
    _assert_clean(res, where)


def test_shipped_curated_sample_in_demo_and_local_mode(tmp_path, monkeypatch):
    for mode in (None, "local"):
        sub = tmp_path / (mode or "demo")
        for n in ("rec", "keys", "run", "set"):
            (sub / n).mkdir(parents=True)
        c, tok, status, res = run_variant(sub, monkeypatch, "sample", "valid", "one", shipped=True, mode=mode)
        assert len(prepared_items(res)) >= 15, mode      # T-214: f_r7_1 (phrase list only) is no longer prepared; the 15 others have a curated answer
        _assert_clean(res, f"shipped/{mode}")


@pytest.mark.parametrize("fault", ("malformed", "empty"))
def test_a_malformed_or_empty_answer_reads_exactly_like_a_missing_one(tmp_path, monkeypatch, fault):
    """D-069 (2): malformed means missing. The record's item, its trace and the case trace say the same thing whichever way the answer is unusable."""
    texts = {}
    for f in (fault, "missing"):
        sub = tmp_path / f
        for n in ("rec", "keys", "run", "set"):
            (sub / n).mkdir(parents=True)
        c, tok, status, res = run_variant(sub, monkeypatch, "sample", f, "one")
        it = res["item:e1"]["item"]
        steps = [(s["id"], s["label"], s["status"], s["why"], s["reason_code"]) for s in res["trace:e1"]["steps"]]
        ct = [(s["id"], s["label"], s["status"], s["why"]) for s in res["/trace"]["steps"] if s["id"] in ("extract", "judges")]
        texts[f] = (it["state"], it.get("why"), it.get("explanation"), steps, ct, res["case"]["models"])
    assert texts["missing"][0] == "rejected" and "no prepared answer" in json.dumps(texts["missing"][3]).lower(), "the fault must hit e1, or this test proves nothing"
    assert texts[fault] == texts["missing"], json.dumps({k: v for k, v in texts.items()})[:3000]


def test_a_prepared_answer_carries_no_prompt_version(tmp_path, monkeypatch):
    """T-177 r3 F4 (the round-2 acceptance test that was never written): nothing prompted a hand-written answer, so no audit row, trace step or export field names a generator prompt for it."""
    c, tok, status, res = run_variant(tmp_path, monkeypatch, "sample", "valid", "one", shipped=True, do_actions=False)      # provenance of a clean export: the action pass leaves blockers
    prepared_rows = [x for x in res["/audit"]["calls"] if x.get("prepared")]
    assert len(prepared_rows) >= 16
    assert all(x["prompt_version"] is None for x in prepared_rows), [x["step"] for x in prepared_rows if x["prompt_version"]]
    steps = [s for k, v in res.items() if k.startswith("trace:") for s in v["steps"] if (s.get("evidence") or {}).get("model", {}).get("prepared")]
    assert steps and all(s["evidence"].get("prompt_version") is None for s in steps)
    pv = res["export-after"]["provenance"]["prompt_versions"]
    assert pv and not {"extract_v1", "extract_es_v1", "flags_v1", "conflicts_v1", "split_v1", "narrative_v1"} & set(pv), pv      # only the second check's prompts remain


# ------------------------------------------------------------------ r5: the twins themselves
def test_every_sentence_that_names_an_ai_has_a_prepared_twin_and_no_twin_names_one():
    """T-177 r5 (staff-engineer r4 F1/F5): the lookups are `(TWIN.get(code) if prepared else None) or AI_TEXT`, so a deleted or misspelled twin falls back to the AI sentence without a sound.
    Close that statically: every why / trace-why / next-action sentence that matches FORBIDDEN has a twin under the same code, and no twin matches it."""
    from app.backend import trace, why
    tables = (("why", why._WHY, why._WHY_PREPARED), ("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED), ("next", trace._NEXT, trace._NEXT_PREPARED))
    missing, dirty, orphan = [], [], []
    for name, base, twin in tables:
        missing += [f"{name}.{k}" for k, v in base.items() if FORBIDDEN.search(v) and not twin.get(k)]
        dirty += [f"{name}.{k}" for k, v in twin.items() if FORBIDDEN.search(v)]
        orphan += [f"{name}.{k}" for k in twin if k not in base]
    assert not missing, f"AI wording with no prepared twin: {missing}"
    assert not dirty, f"a prepared twin that names an AI or a model: {dirty}"
    assert not orphan, f"a twin with no sentence to replace (misspelled code?): {orphan}"
    assert why.why("INJECTION_SUSPECTED", prep=True) != why.why("INJECTION_SUSPECTED")


@pytest.mark.parametrize("fault", ("valid", "unsupported"))
def test_the_edit_and_hand_entry_paths_are_reached_and_use_the_prepared_voice(tmp_path, monkeypatch, fault):
    """The action pass is not vacuous. After "edit the quote" and then "accept", responses carry the prepared twins (not just a clean scan): the edit warning, the edited-not-accepted
    trace sentence, the export's "second check never ran" blocker. If a twin is deleted the AI sentence is printed instead and these fail (and the scan above fails too)."""
    from app.backend import trace, why
    c, tok, status, res = run_variant(tmp_path, monkeypatch, "sample", fault, "one")
    assert any(k.startswith("edit:") and res[k].get("item") for k in res), "no edit was accepted, so the edit path was not exercised"
    blob = json.dumps(res, ensure_ascii=False)
    for name, base, twin, code in (("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED, "EDIT_NOT_CONFIRMED_ITEM_AI"), ("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED, "JUDGE_NOT_RUN"),
                                   ("why", why._WHY, why._WHY_PREPARED, "JUDGE_UNAVAILABLE")):
        assert twin[code] in blob, f"{name}.{code}: the prepared twin never appears in any response of the action pass"
        assert base[code] not in blob, f"{name}.{code}: the AI sentence appears in a prepared case"
    assert any(k.startswith("warn") or "warnings" in json.dumps(v) for k, v in res.items() if k.startswith("edit:")), "the edit response carried no second-check warning"
    if fault == "unsupported":
        e1 = json.dumps(res["item:e1"]) + json.dumps(res["trace:e1"])
        assert why._WHY_PREPARED["SUMMARY_NOT_IN_QUOTE"] in e1, "the unsupported summary was not removed by code"
        assert any(k.startswith("manual:") for k in res), "no hand entry was written for the removed entry"
