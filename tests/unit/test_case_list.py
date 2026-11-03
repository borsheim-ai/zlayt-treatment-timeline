"""T-148: GET /api/cases summary list. Every field is compared with the route that owns it (GET case, /status, /trace, /export) for every library
case, so the overview can never say something the case screen does not. Fixture backend, no network; local mode only."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import case_list
from app.backend.api import create_app

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
LIB_IDS = sorted(p.stem for p in LIB.glob("*.txt"))


@pytest.fixture(scope="module")
def local(tmp_path_factory):
    import os
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    d = tmp_path_factory.mktemp("cl")
    c = TestClient(create_app(str(d / "t.sqlite"), static_dir=str(d)), client=("127.0.0.1", 50000))
    yield c
    for k, v in old.items():
        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def _wait(c, tok):
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            return s
        time.sleep(0.25)
    raise AssertionError(s)


@pytest.fixture(scope="module")
def cases(local):
    """Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss)."""
    toks = {}
    for lid in LIB_IDS:
        r = local.post("/api/cases", json={"library": lid})
        assert r.status_code == 201, r.text
        toks[lid] = r.json()["token"]
        assert local.post(f"/api/cases/{toks[lid]}/run", json={}).status_code == 202
    for t in toks.values():
        _wait(local, t)
    first = toks[LIB_IDS[0]]
    items = [i for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{first}").json()[k]]
    for n, it in enumerate(items[:6]):
        local.post(f"/api/cases/{first}/items/{it['id']}/review", json={"action": ["accept", "dismiss"][n % 2]})
    second = local.get(f"/api/cases/{toks[LIB_IDS[1]]}").json()["entries"][0]          # a reworded entry: saved, but the second check cannot confirm the new wording
    local.post(f"/api/cases/{toks[LIB_IDS[1]]}/items/{second['id']}/review", json={"action": "edit", "edits": {"summary": second["summary"].rstrip(".") + " (reworded)."}})
    third = toks[LIB_IDS[2]]                                                                  # accept whatever the code checks allow: a case whose export gate opens
    for k in ("entries", "flags", "amounts"):
        for it in local.get(f"/api/cases/{third}").json()[k]:
            local.post(f"/api/cases/{third}/items/{it['id']}/review", json={"action": "accept"})
    text = (LIB / f"{LIB_IDS[-1]}.txt").read_text()               # an allowed (recorded) text, pasted under a file-slug name and never run
    toks["_ingested"] = local.post("/api/cases", json={"text": text, "name": "smith_records-2024.txt"}).json()["token"]
    return toks


def _by_token(local):
    r = local.get("/api/cases")
    assert r.status_code == 200
    return {x["token"]: x for x in r.json()["cases"]}


def test_list_covers_every_case_newest_first(local, cases):
    got = local.get("/api/cases").json()["cases"]
    assert {x["token"] for x in got} == set(cases.values()) and len(got) == len(LIB_IDS) + 1
    assert got[0]["token"] == cases["_ingested"] and [x["created_at"] for x in got] == sorted((x["created_at"] for x in got), reverse=True)


def test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):
    listed = _by_token(local)
    for lid, tok in cases.items():
        s, case = listed[tok], local.get(f"/api/cases/{tok}").json()
        st = local.get(f"/api/cases/{tok}/status").json()
        tr = local.get(f"/api/cases/{tok}/trace").json()
        gate = next(x for x in tr["steps"] if x["id"] == "export_gate")
        # identity and times: the case screen's own values
        assert s["name"] == case["name"] and s["status"] == case["status"] and s["created_at"] == case["created_at"] and s["updated_at"] == case["updated_at"], lid
        assert s["record_count"] == len(case["records"]) and s["last_activity_at"] >= s["updated_at"], lid
        # run stage: the status route
        assert s["run"]["stage"] == st["stage"] and s["run"]["steps_done"] == st["progress"]["done"] and s["run"]["steps_total"] == st["progress"]["total"], lid
        assert s["run"]["running"] == (case["status"] == "running"), lid
        # review counts and the could-not-verify tray: the case screen
        rc = case["review"]["counts"]
        h = s["hitl"]
        assert h["needs_review"] == rc["needs_review"] and h["edits_to_check"] == rc["edit_to_check"] and h["pending"] == rc["pending"], lid
        assert h["could_not_verify"] == len(case["tray"]), lid
        assert h["needs_review_open"] == len(_waiting(case)) == len([1 for _, i in _waiting(case) if i["state"] == "needs_review"]), lid          # T-157 r3: open = needs review and (pending or unconfirmed edit), from the GET case items
        assert h["needs_review_open"] <= h["needs_review"], lid
        assert s["counts"] == {k: rc[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")}, lid
        # progress per kind: totals are the live items GET case lists, decided never exceeds total, and the kinds add up to the review counts
        live = {"entries": [e for e in case["entries"] + case["undated_entries"]], "flags": case["flags"], "amounts": case["amounts"]}
        for kind, rows in live.items():
            p = s["progress"][kind]
            assert p["total"] == len(rows), (lid, kind)
            assert p["decided"] == sum(1 for r in rows if r["review_status"] in ("accepted", "dismissed", "edited")) - (rc["edit_to_check"] if kind == "entries" else 0), (lid, kind)
        tot = sum(v["total"] for v in s["progress"].values())
        dec = sum(v["decided"] for v in s["progress"].values())
        assert tot - dec == rc["pending"] + rc["edit_to_check"], lid
        # gate: blockers and warnings with their plain reasons, and export_ready is what GET /export allows
        assert s["export_ready"] is gate["ready"] is (local.get(f"/api/cases/{tok}/export").status_code == 200), lid
        assert [(b["reason_code"], b["why"]) for b in h["gate_blockers"]] == [(b["reason_code"], b["why"]) for b in gate["blockers"]], lid
        assert [(w["reason_code"], w["count"], w["why"]) for w in h["gate_warnings"]] == [(w["reason_code"], w["count"], w["why"]) for w in gate["warnings"]], lid
        assert all(b["why"] for b in h["gate_blockers"]) and all(w["why"] for w in h["gate_warnings"]), lid
        # T-157: title and next_action are the same on GET case; no item says rerun is available in fixture mode
        assert s["title"] == case["title"] and "Untitled" not in s["title"], lid
        assert s["next_action"] == case["next_action"], lid
        for k in ("entries", "flags", "amounts"):
            assert all(i["rerun_available"] is False for i in case[k]), (lid, k)


def test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):
    s = _by_token(local)
    first = s[cases[LIB_IDS[0]]]
    assert sum(v["decided"] for v in first["progress"].values()) >= 1 and first["last_activity_at"] > first["updated_at"] or first["last_activity_at"] >= first["updated_at"]
    ing = s[cases["_ingested"]]
    assert ing["status"] == "ingested" and ing["run"]["stage"] == "ingest" and ing["export_ready"] is False
    assert [b["reason_code"] for b in ing["hitl"]["gate_blockers"]] == ["NOTHING_ACCEPTED"]


def test_decided_cases_cover_ready_and_edit_to_check(local, cases):
    s = _by_token(local)
    third = s[cases[LIB_IDS[2]]]
    assert third["export_ready"] is True and third["hitl"]["gate_blockers"] == [] and sum(v["decided"] for v in third["progress"].values()) > 0
    second = s[cases[LIB_IDS[1]]]
    assert second["hitl"]["edits_to_check"] == 1 and second["progress"]["entries"]["decided"] == 0          # a reworded entry is saved but not decided
    assert "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in second["hitl"]["gate_warnings"]]


def test_title_is_readable_not_a_file_slug(local, cases):
    s = _by_token(local)
    assert s[cases["_ingested"]]["title"] == "Smith records 2024"
    for lid in LIB_IDS:
        t = s[cases[lid]]["title"]
        assert t and "_" not in t and not t.endswith((".txt", ".pdf")) and not t.lower().startswith(("case ", "lib")), t
    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"
    assert case_list.readable_title("case_01_date_formats", "paste", 0) == "Date formats"
    assert case_list.readable_title("records_final-v2.pdf", "paste", 0) == "Records final v2"
    assert case_list.readable_title("Smith v. Jones intake", "paste", 0) == "Smith v. Jones intake"
    assert case_list.readable_title(None, "paste", 1762000000) == "Records added Nov 1"          # T-157: never "Untitled case"
    assert case_list.readable_title("", "sample", 0) == "Sample case"


def test_list_is_code_only_no_text_no_model_calls(local, cases):
    import json
    listed = local.get("/api/cases").json()["cases"]
    raw = json.dumps(listed)
    assert "Excerpt:" not in raw and "raw_text" not in raw
    before = {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in list(cases.values())[:3]}
    local.get("/api/cases")
    assert before == {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in before}


def test_list_is_404_outside_local_mode(local, monkeypatch):
    monkeypatch.delenv("ZLAYT_MODE")
    assert local.get("/api/cases").status_code == 404


# ---------------------------------------------------------------- T-157
def test_default_title_comes_from_the_first_record_header(local, cases):
    s = _by_token(local)
    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"                     # a library case keeps its name
    text = (LIB / f"{LIB_IDS[0]}.txt").read_text()
    tok = local.post("/api/cases", json={"text": text}).json()["token"]                    # pasted, no name: provider and first date of record 1
    assert local.get(f"/api/cases/{tok}").json()["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026"
    assert _by_token(local)[tok]["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026" and _by_token(local)[tok]["name"] is None


def test_title_on_create_and_patch(local, cases):
    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
    r = local.post("/api/cases", json={"text": text, "title": "  Rivera   v. Acme \n intake "})
    assert r.status_code == 201 and r.json()["title"] == "Rivera v. Acme intake"
    tok = r.json()["token"]
    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera v. Acme intake" and _by_token(local)[tok]["title"] == "Rivera v. Acme intake"
    p = local.patch(f"/api/cases/{tok}", json={"title": "Rivera, final"})
    assert p.status_code == 200 and p.json()["title"] == "Rivera, final" and p.json()["token"] == tok
    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera, final" and _by_token(local)[tok]["title"] == "Rivera, final"
    assert local.patch(f"/api/cases/{tok}", json={"title": "   "}).json()["title"] != "Rivera, final"          # blank returns to the derived default
    assert "Untitled" not in local.get(f"/api/cases/{tok}").json()["title"]
    long = local.patch(f"/api/cases/{tok}", json={"title": "x" * 120})
    assert long.status_code == 200 and len(long.json()["title"]) == 120
    over = local.patch(f"/api/cases/{tok}", json={"title": "x" * 121})          # over the cap: refused, the stored title is unchanged
    assert over.status_code == 422 and over.json()["error"]["code"] == "invalid_title" and "120" in over.json()["error"]["message"]
    assert local.get(f"/api/cases/{tok}").json()["title"] == "x" * 120
    for bad in ({"title": 5}, {"title": None, "x": 1}, {}, {"name": "a"}):
        got = local.patch(f"/api/cases/{tok}", json=bad)
        if bad == {"title": None, "x": 1}:
            assert got.status_code == 200          # null clears the name like a blank title
        else:
            assert got.status_code == 400 and got.json()["error"]["code"] == "bad_request", bad
    assert local.patch("/api/cases/nope", json={"title": "a"}).status_code == 404


def test_titles_are_never_untitled(local, cases):
    for x in local.get("/api/cases").json()["cases"]:
        assert x["title"] and "untitled" not in x["title"].lower()
    tok = local.post("/api/cases", json={"text": (LIB / f"{LIB_IDS[2]}.txt").read_text(), "name": "  "}).json()["token"]
    assert "untitled" not in local.get(f"/api/cases/{tok}").json()["title"].lower()


def test_rerun_available_follows_live_mode_and_the_last_rerun(local, cases, monkeypatch):
    from app.db import db as DB
    tok = cases[LIB_IDS[0]]
    item = local.get(f"/api/cases/{tok}").json()["entries"][0]
    assert item["rerun_available"] is False                                          # fixture / demo mode: nothing can answer
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    got = local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]
    assert got["rerun_available"] is True                                            # live and no rerun yet
    assert all(i["rerun_available"] is True for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{tok}").json()[k])
    c = DB.connect(local.app.state.db_path)
    try:
        row = DB.get_item(c, item["id"], tok)
        lad = dict(row["ladder"] or {})
        lad["rejudge"] = [{"verdict": "unavailable"}]
        DB.update_item(c, item["id"], case=tok, ladder=lad)
    finally:
        c.close()
    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False          # the last rerun got no answer
    monkeypatch.setenv("ENABLE_LIVE", "0")
    assert local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"] is False
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    case = local.get(f"/api/cases/{tok}").json()
    named = case["entries"][0]["id"]                                                  # a named item, asserted without an if-guard
    assert local.get(f"/api/cases/{tok}/items/{named}").json()["item"]["rerun_available"] is False          # no key, no live answer
    assert case["flags"] + case["amounts"], "the library case must carry a flag or an amount for this check"
    assert all(i["rerun_available"] is False for i in case["flags"] + case["amounts"])


def test_next_action_blockers_first_then_needs_review_in_timeline_order(local, cases):
    s = _by_token(local)
    ing = s[cases["_ingested"]]["next_action"]
    assert ing["kind"] == "run" and ing["item_id"] is None and ing["reason"]          # ingested: nothing to decide before the run
    for lid, tok in cases.items():
        if lid == "_ingested":
            continue
        na = s[tok]["next_action"]
        case = local.get(f"/api/cases/{tok}").json()
        blockers = s[tok]["hitl"]["gate_blockers"]
        if na is None:
            waiting = [i for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
                       if i["state"] == "needs_review" and (i["review_status"] == "pending" or i.get("edit_to_check"))]
            assert not blockers and not waiting, lid          # nothing blocks the export and nothing needs review: nothing to point at
            continue
        assert set(na) == {"item_id", "kind", "reason"} and na["reason"], lid
        item_blockers = [b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"]
        if item_blockers:                                                              # a gate blocker is the first thing, in gate order
            assert (na["item_id"], na["kind"], na["reason"]) == (item_blockers[0].get("item_id"), item_blockers[0]["kind"], item_blockers[0]["why"]), lid
            continue
        every = {i["id"]: (k, i) for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])}
        assert na["item_id"] in every, lid
        kind, it = every[na["item_id"]]
        assert it["state"] == "needs_review" and (it["review_status"] == "pending" or it["edit_to_check"]), lid
        assert na["kind"] == {"entries": "entry", "flags": "flag", "amounts": "amount"}[kind] and na["reason"] == it["why"], lid
    # accepting the item next_action names moves it on (or, when it was the last, clears it)
    fresh = local.post("/api/cases", json={"library": LIB_IDS[3]}).json()["token"]
    local.post(f"/api/cases/{fresh}/run", json={})
    _wait(local, fresh)
    seen = []
    for _ in range(60):
        na = local.get(f"/api/cases/{fresh}").json()["next_action"]
        assert na == _by_token(local)[fresh]["next_action"]
        if na is None or na["item_id"] is None or na["item_id"] in seen:
            break
        seen.append(na["item_id"])
        local.post(f"/api/cases/{fresh}/items/{na['item_id']}/review", json={"action": "dismiss"})
    assert len(seen) == len(set(seen))


def test_next_action_orders_by_record_date_not_by_kind_or_id(local, cases):
    from app.backend import case_list
    from app.db import db as DB
    c = DB.connect(local.app.state.db_path)
    try:
        checked = 0
        for tok in cases.values():
            order = case_list.needs_review_order(c, tok)
            assert order == sorted(order, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))
            dated = [x["date"] for x in order if x["date"]]
            assert dated == sorted(dated)                                             # timeline order
            assert all(x["row"]["state"] == "needs_review" and x["row"]["review_status"] in ("pending", "edited") for x in order)
            checked += len(order)
        assert checked > 5                                                            # the library really has needs-review work to order
    finally:
        c.close()


# ---------------------------------------------------------------- T-157 r2: title validation
_ONERROR = "<img src=x onerror=alert(1)>Rivera"


def test_markup_in_a_title_is_refused_with_a_plain_message_and_nothing_is_stored(local, cases):
    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
    for bad in (_ONERROR, "<script>x</script>", "a > b", "Rivera <b>", "<!-- c -->"):
        r = local.post("/api/cases", json={"text": text, "title": bad})
        assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_title", bad
        msg = r.json()["error"]["message"]
        assert msg and "<" not in msg and ">" not in msg and "onerror" not in msg          # the message never echoes the markup
    before = len(local.get("/api/cases").json()["cases"])
    assert local.post("/api/cases", json={"text": text, "name": _ONERROR}).status_code == 422          # the older `name` field is held to the same rule
    assert len(local.get("/api/cases").json()["cases"]) == before          # a refused create leaves no case behind
    tok = local.post("/api/cases", json={"text": text, "title": "Rivera"}).json()["token"]
    for bad in (_ONERROR, "<script>x</script>\u0007Acme"):
        r = local.patch(f"/api/cases/{tok}", json={"title": bad})
        assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_title", bad
    assert local.get(f"/api/cases/{tok}").json()["title"] == "Rivera" and _by_token(local)[tok]["title"] == "Rivera"          # rename refused: unchanged


def test_an_img_onerror_title_is_never_returned_as_markup_anywhere(local, cases):
    """The stored value and every response that carries a title: inert text only. Rejected on input, and the same rule on the derived default."""
    import json
    text = (LIB / f"{LIB_IDS[1]}.txt").read_text()
    assert local.post("/api/cases", json={"text": text, "title": _ONERROR}).status_code == 422
    # a record whose Source header is markup: the derived title is plain text (tags dropped), not the header verbatim
    from app.db import db as DB
    tok = local.post("/api/cases", json={"text": text}).json()["token"]
    c = DB.connect(local.app.state.db_path)
    try:
        c.execute("UPDATE records SET source_label=? WHERE case_id=? AND seq=(SELECT min(seq) FROM records WHERE case_id=?)", ("<img src=x onerror=alert(1)>Marrowgate ED", tok, tok))
        c.commit()
    finally:
        c.close()
    for body in (local.get(f"/api/cases/{tok}").json(), _by_token(local)[tok]):
        assert "<" not in body["title"] and ">" not in body["title"] and body["title"].startswith("Marrowgate ED"), body["title"]
    assert "<img" not in json.dumps({x["token"]: x["title"] for x in local.get("/api/cases").json()["cases"]})


def test_control_characters_are_stripped_and_white_space_collapsed(local, cases):
    from app.backend import case_list
    assert case_list.validate_title("A\x07cme\x00 v.\u202e Smith") == "Acme v. Smith"          # bell, NUL and bidi override: removed, not turned into gaps
    assert case_list.validate_title("  Rivera \t v.\n Acme  ") == "Rivera v. Acme"
    assert case_list.validate_title("\x07\x00") == "" and case_list.validate_title(None) == ""
    assert case_list.validate_title("x" * 120) == "x" * 120
    for bad in ("x" * 121, "<b>", "5 > 3"):
        with pytest.raises(case_list.TitleError) as e:
            case_list.validate_title(bad)
        assert "<" not in str(e.value) and ">" not in str(e.value)
    assert case_list.plain_title("<b>Clinic</b> & Co <") == "Clinic & Co"          # derived text: tags dropped, stray angle brackets removed
    assert case_list.plain_title("St. Mary's <3 Clinic") == "St. Mary's 3 Clinic"          # a lone < drops only itself, never the words after it
    assert case_list.plain_title("Marrowgate > ED") == "Marrowgate ED"


def test_a_name_that_is_empty_after_cleanup_falls_through_to_the_record_header(local, cases):
    text = (LIB / f"{LIB_IDS[0]}.txt").read_text()
    tok = local.post("/api/cases", json={"text": text, "name": "case_01_"}).json()["token"]
    assert local.get(f"/api/cases/{tok}").json()["title"] == "Dunmarrow Fire-Rescue run report, Feb 14, 2026"          # not "Records added Nov 1"


def test_pdf_title_query_parameter_names_the_case(local, cases, monkeypatch):
    from tests.unit import _golden as G
    from tests.unit._pdf import sample_pdf
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")          # local live mode: demo mode refuses an extracted PDF (409); this test never runs the pipeline
    monkeypatch.setenv("ENABLE_LIVE", "1")
    data, hdr = sample_pdf(G.raw("sample")), {"content-type": "application/pdf"}
    r = local.post("/api/cases/pdf?title=Rivera%20intake", content=data, headers=hdr)
    assert r.status_code == 201, r.text
    assert r.json()["title"] == "Rivera intake" and local.get(f"/api/cases/{r.json()['token']}").json()["title"] == "Rivera intake"
    n = len(local.get("/api/cases").json()["cases"])
    bad = local.post("/api/cases/pdf?title=%3Cb%3Ex", content=data, headers=hdr)
    assert bad.status_code == 422 and bad.json()["error"]["code"] == "invalid_title"
    assert len(local.get("/api/cases").json()["cases"]) == n          # refused before anything is stored


@pytest.mark.parametrize("backend", ["fixture", "claude-cli", "anthropic-api"])
@pytest.mark.parametrize("enable", [None, "0", "1"])
@pytest.mark.parametrize("key", [None, "k"])
def test_rerun_available_is_false_whenever_the_app_is_in_demo_mode(local, cases, monkeypatch, backend, enable, key):
    """One definition of `live` (store.live_enabled): api.demo_mode is its negation and rerun_available can only be true inside it."""
    from app.backend import store
    monkeypatch.setenv("LLM_BACKEND", backend)
    for name, val in (("ENABLE_LIVE", enable), ("ANTHROPIC_API_KEY", key)):
        monkeypatch.delenv(name, raising=False) if val is None else monkeypatch.setenv(name, val)
    tok = cases[LIB_IDS[3]]          # untouched by the other tests (no rerun recorded on its items)
    item = local.get(f"/api/cases/{tok}").json()["entries"][0]
    demo = local.get("/api/health").json()["demo_mode"]
    assert demo is (not store.live_enabled())
    got = local.get(f"/api/cases/{tok}/items/{item['id']}").json()["item"]["rerun_available"]
    if demo:
        assert got is False
    assert got is (store.live_model_available() and not demo)


# ---------------------------------------------------------------- T-157 r2: next_action ordering is pinned
def _fresh(local, lib_id):
    tok = local.post("/api/cases", json={"library": lib_id}).json()["token"]
    assert local.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    _wait(local, tok)
    from tests.unit._hand_entry import enter_failed_records_by_hand
    enter_failed_records_by_hand(local, tok)      # T-165: lib01's record 3 has no recorded extract answer; the paralegal enters it by hand
    return tok


def _db(local):
    from app.db import db as DB
    return DB, DB.connect(local.app.state.db_path)


def _waiting(case):
    return [(k, i) for k in ("entries", "flags", "amounts") for i in case[k] + (case["undated_entries"] if k == "entries" else [])
            if i["state"] == "needs_review" and (i["review_status"] == "pending" or i.get("edit_to_check"))]


def test_a_blocker_comes_before_a_waiting_item_whatever_the_timeline_says(local, cases):
    """Blockers first. Built, not skipped: the case has needs-review items waiting AND an accepted AI-made entry whose second check never answered (JUDGE_NOT_RUN)."""
    DB, c = _db(local)
    tok = _fresh(local, LIB_IDS[0])
    try:
        case = local.get(f"/api/cases/{tok}").json()
        waiting = _waiting(case)
        assert waiting, "scenario not built: no needs-review item is waiting"
        target = next(i for i in case["entries"] if i["state"] != "needs_review" and i["review_status"] == "pending" and not i["edit_to_check"])
        row = DB.get_item(c, target["id"], tok)
        lad = dict(row["ladder"] or {})
        lad["judge"] = {**(lad.get("judge") or {}), "verdict": "unavailable"}
        DB.update_item(c, target["id"], case=tok, ladder=lad)
    finally:
        c.close()
    assert local.post(f"/api/cases/{tok}/items/{target['id']}/review", json={"action": "accept"}).status_code == 200
    s = _by_token(local)[tok]
    blockers = [b for b in s["hitl"]["gate_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    assert blockers and blockers[0]["item_id"] == target["id"], "scenario not built: the accepted entry did not block the export"
    still = _waiting(local.get(f"/api/cases/{tok}").json())
    assert still, "scenario not built: nothing is waiting any more"
    na = s["next_action"]
    assert na == {"item_id": target["id"], "kind": "entry", "reason": blockers[0]["why"]}          # the blocker, not a waiting item
    assert na["item_id"] not in {i["id"] for _, i in still}
    assert local.get(f"/api/cases/{tok}").json()["next_action"] == na


def test_a_failed_run_is_the_first_thing_even_with_items_waiting(local, cases):
    DB, c = _db(local)
    tok = _fresh(local, LIB_IDS[0])
    try:
        assert _waiting(local.get(f"/api/cases/{tok}").json()), "scenario not built"
        DB.update_case(c, tok, status="failed")
        c.commit()
    finally:
        c.close()
    na = _by_token(local)[tok]["next_action"]
    assert na["kind"] == "case" and na["item_id"] is None and "stopped before it finished" in na["reason"]


def test_the_first_waiting_item_is_the_earliest_by_record_date_even_when_kind_and_id_say_otherwise(local, cases):
    """Timeline pick, with date order forced to disagree with seq, kind and id: the date wins; ties fall to record position, then kind, then id."""
    DB, c = _db(local)
    probe = DB.connect(local.app.state.db_path)
    try:
        richest = max((t for k, t in cases.items() if k != "_ingested"), key=lambda t: len({o["seq"] for o in case_list.needs_review_order(probe, t)}))
        lid = next(k for k, t in cases.items() if t == richest)
    finally:
        probe.close()
    tok = _fresh(local, lid)
    try:
        order = case_list.needs_review_order(c, tok)
        recs = [(r["id"], r["seq"]) for r in c.execute("SELECT id, seq FROM records WHERE case_id=? ORDER BY seq", (tok,))]
        assert len(order) >= 2 and len({o["seq"] for o in order}) >= 2, "scenario not built: need waiting items on two or more records"
        # give the record of the LAST waiting item the earliest date, and every other record a later one
        last = order[-1]
        last_rec = next(rid for rid, seq in recs if seq == last["seq"])
        for n, (rid, _) in enumerate(recs):
            day = "2020-01-01" if rid == last_rec else f"2021-0{1 + min(n, 8)}-01"
            c.execute("UPDATE records SET date_iso=? WHERE id=? AND case_id=?", (day, rid, tok))
        c.commit()
        reordered = case_list.needs_review_order(c, tok)
        assert reordered[0]["id"] != order[0]["id"], "scenario not built: the dates did not change the order"
        expect = min((o for o in reordered if o["date"]), key=lambda o: (o["date"], o["seq"] or 0, o["rank"], o["id"]))
        assert reordered[0]["id"] == expect["id"] and reordered[0]["date"] == "2020-01-01"
        na = case_list.next_action(c, tok, blockers=[])
        assert na["item_id"] == reordered[0]["id"] and na["kind"] == reordered[0]["kind"]
        assert na["item_id"] not in (order[0]["id"],) or last["id"] == order[0]["id"]
        # same date everywhere: record position decides, then kind. Swap the positions of the records behind an entry and an amount (both cite records by id) so position and kind disagree
        c.execute("UPDATE records SET date_iso='2022-02-02' WHERE case_id=?", (tok,))
        c.commit()
        ties = case_list.needs_review_order(c, tok)
        assert [(o["seq"], o["rank"], o["id"]) for o in ties] == sorted((o["seq"], o["rank"], o["id"]) for o in ties)
        entry = next(o for o in ties if o["kind"] == "entry")
        amount = next((o for o in ties if o["kind"] == "amount" and o["seq"] > entry["seq"]), None)
        assert amount, "scenario not built: need an entry on an earlier record than an amount"
        swap = {entry["seq"]: amount["seq"], amount["seq"]: entry["seq"]}
        for old in swap:
            c.execute("UPDATE records SET seq=seq+1000 WHERE case_id=? AND seq=?", (tok, old))
        for old, new in swap.items():
            c.execute("UPDATE records SET seq=? WHERE case_id=? AND seq=?", (new, tok, old + 1000))
        c.commit()
        swapped = case_list.needs_review_order(c, tok)
        pos = {o["id"]: n for n, o in enumerate(swapped)}
        assert pos[amount["id"]] < pos[entry["id"]], "position beats kind when the date ties"
        assert case_list.next_action(c, tok, blockers=[])["item_id"] == swapped[0]["id"]
        # an undated item goes last: strip the date from the earliest item's record
        c.execute("UPDATE records SET date_iso=NULL WHERE id=? AND case_id=?", (last_rec, tok))
        c.commit()
        final = case_list.needs_review_order(c, tok)
        assert final[-1]["date"] is None and final[0]["date"] is not None          # undated work sorts after every dated item
    finally:
        c.close()


def test_every_library_case_names_the_earliest_waiting_item_when_nothing_blocks(local, cases):
    """The pick is needs_review_order()[0], and that item's cited record date is the earliest of the waiting set."""
    DB, c = _db(local)
    checked = 0
    try:
        for lid, tok in cases.items():
            if lid == "_ingested":
                continue
            s = _by_token(local)[tok]
            if any(b["reason_code"] != "NOTHING_ACCEPTED" for b in s["hitl"]["gate_blockers"]):
                continue
            order = case_list.needs_review_order(c, tok)
            if not order:
                continue
            assert s["next_action"]["item_id"] == order[0]["id"], lid
            dated = [o["date"] for o in order if o["date"]]
            assert order[0]["date"] == (min(dated) if dated else None), lid
            checked += 1
    finally:
        c.close()
    assert checked >= 3


def test_an_unconfirmed_edit_is_a_needs_review_item_and_next_action_can_name_it(local, cases):
    """An entry the paralegal reworded (edit_to_check) is still waiting for her. Built, not skipped: the reworded entry is made the earliest waiting item by record date, with other
    items still waiting behind it, so next_action naming anything else (or the edit dropping out of the waiting set) fails here."""
    DB, c = _db(local)
    tok = _fresh(local, next(k for k in LIB_IDS if "slip_fall" in k))          # the way the shared fixture builds an unconfirmed edit: reword the first entry
    try:
        case = local.get(f"/api/cases/{tok}").json()
        before = {o["id"] for o in case_list.needs_review_order(c, tok)}
        first = case["entries"][0]
        assert first["id"] not in before and before, "scenario not built: the first entry is decided and other items are waiting"
        r = local.post(f"/api/cases/{tok}/items/{first['id']}/review", json={"action": "edit", "edits": {"summary": first["summary"].rstrip(".") + " (reworded)."}})
        assert r.status_code == 200, r.text
        edited = next(i for i in local.get(f"/api/cases/{tok}").json()["entries"] if i["id"] == first["id"])
        assert edited["edit_to_check"] and edited["state"] == "needs_review", "scenario not built: the edit did not stay unconfirmed"
        target = next(o for o in case_list.needs_review_order(c, tok) if o["id"] == first["id"])          # the edit is in the waiting set
        assert target["kind"] == "entry"
        recs = [(r_["id"], r_["seq"]) for r_ in c.execute("SELECT id, seq FROM records WHERE case_id=? ORDER BY seq", (tok,))]
        for n, (rid, seq) in enumerate(recs):                                      # the edited entry's record is the earliest; every other record is later
            c.execute("UPDATE records SET date_iso=? WHERE id=? AND case_id=?", ("2000-01-01" if seq == target["seq"] else f"2021-0{1 + min(n, 8)}-01", rid, tok))
        c.commit()
        order = case_list.needs_review_order(c, tok)
        assert target["id"] in [o["id"] for o in order], "an unconfirmed edit must stay in the needs-review set"
        assert len(order) >= 2 and order[0]["id"] == target["id"] and {o["id"] for o in order} >= before
        na = case_list.next_action(c, tok, blockers=[])
        assert na["item_id"] == target["id"] and na["kind"] == "entry" and na["reason"]
    finally:
        c.close()


def test_the_set_next_action_chooses_from_is_exactly_the_pending_plus_unconfirmed_edit_items(local, cases):
    """Computed from the GET case JSON, not from needs_review_order: pending-or-edit_to_check items in state needs_review. Includes the reworded entry from the shared fixture."""
    DB, c = _db(local)
    edits = 0
    try:
        for lid, tok in cases.items():
            if lid == "_ingested":
                continue
            case = local.get(f"/api/cases/{tok}").json()
            expect = {i["id"] for _, i in _waiting(case)}
            edits += sum(1 for _, i in _waiting(case) if i.get("edit_to_check"))
            assert {o["id"] for o in case_list.needs_review_order(c, tok)} == expect, lid
    finally:
        c.close()
    assert edits, "scenario not built: no library case carries an unconfirmed edit"


def test_the_demo_gate_is_pinned_to_absolute_values(local, cases, monkeypatch):
    """Not compared with the store: a key alone is demo mode; live needs ENABLE_LIVE=1 and a live backend."""
    monkeypatch.setenv("LLM_BACKEND", "anthropic-api")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    assert local.get("/api/health").json()["demo_mode"] is True
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    assert local.get("/api/health").json()["demo_mode"] is False
    monkeypatch.setenv("ENABLE_LIVE", "0")
    assert local.get("/api/health").json()["demo_mode"] is True


def test_needs_review_open_counts_an_unconfirmed_edit(local, cases):
    """The reworded entry from the shared fixture is open: it is in needs_review_open (and in GET case's waiting set), so the overview chip cannot read zero while it waits."""
    tok = cases[LIB_IDS[1]]
    case = local.get(f"/api/cases/{tok}").json()
    assert any(i.get("edit_to_check") for i in case["entries"]), "scenario not built: no reworded entry"
    h = _by_token(local)[tok]["hitl"]
    assert h["needs_review_open"] == len(_waiting(case)) and h["edits_to_check"] >= 1
    assert h["needs_review_open"] >= h["edits_to_check"]
