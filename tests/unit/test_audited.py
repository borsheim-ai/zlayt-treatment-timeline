"""Audited call wrapper: retries and audit rows. ADR-003.7, ADR-004, privacy invariants (never log record text); fixture/fake backend only."""
import pytest
from app.llm import audited as AU, provider as P
from app.db import db as DB

MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss   # T-034 AC8 name is FixtureMissing; test_provider pins that the name exists
SCHEMA = {"type": "object", "properties": {"v": {"type": "string"}}, "required": ["v"]}

@pytest.fixture
def env(tmp_path):
    conn = DB.connect(str(tmp_path / "a.sqlite"))
    return conn, DB.create_case(conn, "SYNTHETIC text", now=1.0)

def seq(*outs):
    """complete_with_meta fake: each item is an output dict or an Exception; records the user prompts."""
    state = dict(i=0, users=[])
    def f(model, system, user, schema):
        state["users"].append(user)
        o = outs[min(state["i"], len(outs) - 1)]; state["i"] += 1
        if isinstance(o, Exception):
            raise o
        return P.LLMResult(output=o, backend="fixture", model_resolved=model)
    f.state = state
    return f

def ac(conn, cid, *a, **kw):
    """audited_call; retries are immediate (no backoff, so no sleep hook is needed - if backend adds one, patch it here)."""
    return AU.audited_call(conn, cid, *a, **kw)

def rows(conn, cid):
    return DB.table_counts(conn, cid).get("llm_calls", 0)

def test_first_success_writes_one_row_and_returns_call_id(env):
    """ADR-004: returns (output, call_id); one llm_calls row per attempt."""
    conn, cid = env
    out, call_id = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=seq({"v": "x"}))
    assert out == {"v": "x"} and call_id and rows(conn, cid) == 1

def test_retries_up_to_two_then_succeeds(env):
    """ADR-003.7: 1 + 2 retries; third attempt succeeds -> 3 rows."""
    conn, cid = env
    f = seq(P.LLMError("timeout"), P.LLMError("bad json"), {"v": "ok"})
    out, _ = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert out == {"v": "ok"} and rows(conn, cid) == 3

def test_three_failures_raise_llm_failed_after_retries(env):
    """ADR-003.7 / LLM_FAILED_AFTER_RETRIES: exactly 3 attempts, then a visible failure; no fourth call."""
    conn, cid = env
    f = seq(P.LLMError("x"))
    with pytest.raises(AU.LLMFailed) as e:
        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 3 and rows(conn, cid) == 3

def test_retries_change_something(env):
    """ADR-003.7: a retry is never an identical request - the user prompt carries a stricter-format request."""
    conn, cid = env
    f = seq(P.LLMError("x"), {"v": "ok"})
    ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert f.state["users"][0] != f.state["users"][1]

def test_fixture_missing_is_one_attempt_and_becomes_llm_failed(env):
    """T-034 AC8 / T-037 AC7 / FIXTURE_MISS: a miss is final (one attempt, one row); the wrapper turns it into LLMFailed(LLM_FAILED_AFTER_RETRIES) and the row logs the prompt hash."""
    conn, cid = env
    f = seq(MISS("abc123hash"))
    with pytest.raises(AU.LLMFailed) as e:
        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 1
    (row,) = DB.list_llm_calls(conn, cid)
    assert "abc123hash" in (row["error"] or "")

def test_audit_rows_record_model_backend_attempt_and_error_code(env):
    """Checklist 9 / ADR-004: one row per attempt with the pinned model, backend, attempt index and a failure code; no prompt text in the error column."""
    conn, cid = env
    f = seq(P.LLMError("TIMEOUT"), P.LLMError("INVALID_JSON"), {"v": "ok"})
    ac(conn, cid, "extract", "model-x", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=f)
    rs = sorted(DB.list_llm_calls(conn, cid), key=lambda r: r["attempt"])
    assert [r["attempt"] for r in rs] == [1, 2, 3]
    assert all(r["model"] == "model-x" and r["backend"] == "fixture" and r["step"] == "extract" for r in rs)
    assert rs[0]["error"] and rs[1]["error"] and not rs[2]["error"]
    assert all("SECRET RECORD TEXT" not in (r["error"] or "") for r in rs)

def test_schema_invalid_output_counts_as_failed_attempt(env):
    """ADR-005 SCHEMA_INVALID: output failing `validate` is retried; after 3 -> LLMFailed."""
    conn, cid = env
    def validate(o):
        if "v" not in o:
            raise ValueError("missing v")
    f = seq({"zzz": 1})
    with pytest.raises(AU.LLMFailed):
        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
    assert len(f.state["users"]) == 3

def test_prompts_stored_so_delete_case_removes_them(env):
    """ADR-006: prompts live in llm_calls, which delete_case empties."""
    conn, cid = env
    ac(conn, cid, "extract", "m", "s", "RECORD TEXT HERE", SCHEMA, complete_with_meta=seq({"v": "x"}))
    DB.delete_case(conn, cid)
    assert rows(conn, cid) == 0

def test_never_prints_record_text(env, capsys, caplog):
    """Arch invariant: never log record text, prompts or responses (errors log call_id only)."""
    conn, cid = env
    with pytest.raises(AU.LLMFailed):
        ac(conn, cid, "extract", "m", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=seq(P.LLMError("SECRET RECORD TEXT in error")))
    out = capsys.readouterr()
    assert "SECRET RECORD TEXT" not in out.out + out.err + caplog.text


# ---------------------------------------------------------------- T-073 r2: retry provider and transport errors only; bugs propagate
@pytest.mark.parametrize("bug", [RuntimeError("programmer bug in provider adapter"), TypeError("x"), KeyError("k"), AttributeError("a"), ZeroDivisionError()])
def test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates(env, bug):
    conn, cid = env
    f = seq(bug)
    with pytest.raises(type(bug)):
        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert len(f.state["users"]) == 1                                                      # one attempt, not three
    (row,) = DB.list_llm_calls(conn, cid)                                                  # and the bug is on the audit trail by class name only
    assert row["error"] == type(bug).__name__ and not row["parsed_ok"]


def test_a_type_error_inside_validate_is_a_bug_and_propagates(env):
    conn, cid = env
    def validate(o):
        return o["v"] + 1                                                                  # TypeError: our code, not the model's output
    f = seq({"v": "x"})
    with pytest.raises(TypeError):
        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
    assert len(f.state["users"]) == 1 and rows(conn, cid) == 1


@pytest.mark.parametrize("transport", [TimeoutError("t"), ConnectionError("c"), ConnectionResetError("r")])
def test_transport_errors_are_retried(env, transport):
    conn, cid = env
    f = seq(transport, {"v": "ok"})
    out, _ = ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f)
    assert out == {"v": "ok"} and rows(conn, cid) == 2


def test_llm_failed_names_the_last_failure_code(env):
    conn, cid = env
    with pytest.raises(AU.LLMFailed) as e:
        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=seq(P.LLMError("TIMEOUT claude-cli")))
    assert e.value.last_error == "TIMEOUT"
    with pytest.raises(AU.LLMFailed) as e:
        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=seq(MISS("abc")))
    assert e.value.last_error == "FIXTURE_MISS"
