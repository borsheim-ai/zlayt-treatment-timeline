"""T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct
states; a missing or invalid file gives calibration null and never an invented number. Aggregate counts only, so demo mode is fine.
Fixture backend, no key, SYNTHETIC counts."""
import json
import shutil
import subprocess

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.backend import calibration_route as CR
from app.backend.api import create_app


def make():
    """A valid evals.calibration/1 document (one golden case), built the way evals/run.py builds it."""
    by_type = {
        "entry": {"verified": {"matched": 54, "total": 55, "by_case": {"sample": [54, 55]}},
                  "needs_review": {"matched": 2, "total": 2, "by_case": {"sample": [2, 2]}}},
        "amount": {"verified": {"matched": 9, "total": 9, "by_case": {"sample": [9, 9]}},
                   "needs_review": {"matched": 6, "total": 6, "by_case": {"sample": [6, 6]}}},
        "flag": {"verified": {"matched": 20, "total": 20, "by_case": {"sample": [20, 20]}},
                 "needs_review": {"matched": 2, "total": 2, "by_case": {"sample": [2, 2]}}},
    }
    by_state = {"verified": {"matched": 83, "total": 84, "cases": ["sample"]},
                "needs_review": {"matched": 10, "total": 10, "cases": ["sample"]}}
    return {
        "schema": "evals.calibration/1", "backend": "fixture", "case_count": 1, "small_sample": True,
        "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642", "generated_at": "2026-11-02T04:48:31Z",
        "by_state": by_state, "by_type": by_type, "not_scored": {"entry": 0, "amount": 0, "flag": 0, "total": 0},
        "sentences": {
            "overall": {"verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).",
                        "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample)."},
            "by_type": {t: {"verified": f"Verified {n} matched the record {by_type[t]['verified']['matched']}/{by_type[t]['verified']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).",
                            "needs_review": f"Needs-review {n} matched the record {by_type[t]['needs_review']['matched']}/{by_type[t]['needs_review']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample)."}
                        for t, n in (("entry", "entries"), ("amount", "amounts"), ("flag", "flags"))}},
        # not served: the route keeps to the statement's shape
        "cases": ["sample"], "hashes": {"app/llm/lexicon.yaml": "00"}, "models": {"generator": "x"}, "match_rule": "...", "source": "evals.run",
        "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f", "source_tree_clean": True,
    }


def write(tmp_path, doc, name="calibration.json"):
    p = tmp_path / name
    p.write_text(doc if isinstance(doc, str) else json.dumps(doc, indent=1, sort_keys=True) + "\n")
    return p


def bare_client(path):
    app = FastAPI()
    CR.add_routes(app, path=path)
    return TestClient(app)


# ---- present

def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
    out = CR.load(write(tmp_path, make()))
    assert out["status"] == "ok" and out["message"] is None
    c = out["calibration"]
    assert c["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
    assert c["backend"] == "fixture" and c["case_count"] == 1 and c["small_sample"] is True
    assert c["by_state"]["verified"] == {"matched": 83, "total": 84, "cases": ["sample"]}
    assert c["sentences"]["overall"]["verified"].startswith("Verified items matched the record 83/84 times")


def test_served_object_is_exactly_the_t096_shape_without_hashes_models_or_paths(tmp_path):
    c = CR.load(write(tmp_path, make()))["calibration"]
    assert set(c) == set(CR.SERVED) | {"stale", "stale_reason"}
    assert not {"hashes", "models", "cases", "source", "source_tree", "match_rule"} & set(c)


def test_route_serves_present_file_over_http(tmp_path):
    r = bare_client(write(tmp_path, make())).get("/api/calibration")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["calibration"]["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"


def test_committed_report_is_valid_when_present():
    if not CR.REPORT.exists():
        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
    out = CR.load()
    assert out["status"] == "ok", out


# ---- missing

def test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):
    out = CR.load(tmp_path / "nope.json")
    assert out == {"status": "missing", "calibration": None, "message": CR.MISSING}


def test_route_missing_file_returns_200_empty_state_not_an_error(tmp_path):
    r = bare_client(tmp_path / "nope.json").get("/api/calibration")
    assert r.status_code == 200
    assert r.json() == {"status": "missing", "calibration": None, "message": CR.MISSING}


# ---- invalid

INVALID_CASES = {
    "not_json": "{not json",
    "not_utf8": None,      # written as raw bytes below
    "top_level_list": "[]",
    "wrong_schema": lambda d: d.update(schema="evals.calibration/2"),
    "sum_mismatch_hand_edit": lambda d: d["by_state"]["verified"].update(matched=90),
    "sentence_quotes_other_counts": lambda d: d["sentences"]["overall"].update(verified=d["sentences"]["overall"]["verified"].replace("83/84", "90/91")),
    "matched_above_total": lambda d: d["by_type"]["flag"]["verified"].update(matched=21),
    "negative_count": lambda d: d["by_type"]["amount"]["verified"].update(matched=-1, total=-1),
    "bool_counts": lambda d: d["by_state"]["needs_review"].update(matched=True),
    "missing_key": lambda d: d.pop("sentences"),
    "missing_source_commit": lambda d: d.update(source_commit=""),
    "statement_for_a_type_missing": lambda d: d["sentences"]["by_type"].pop("flag"),
    # T-099 r2 minor: the served labels and sub-counts are checked against each other and against the sentences
    "case_count_not_the_case_list": lambda d: d.update(case_count=500),
    "small_sample_flipped": lambda d: d.update(small_sample=False),
    "by_case_sum_not_the_cell_total": lambda d: d["by_type"]["entry"]["verified"]["by_case"].update(sample=[50, 55]),
    "by_case_matched_above_its_total": lambda d: d["by_type"]["entry"]["verified"]["by_case"].update({"sample": [2, 1], "other": [52, 54]}),
    "backend_label_not_in_statements": lambda d: d.update(backend="claude-sonnet-5-5"),
    "statement_names_other_case_count": lambda d: d.update(case_count=2, cases=["sample", "extra"]),
}


@pytest.mark.parametrize("name", sorted(INVALID_CASES))
def test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):
    spec = INVALID_CASES[name]
    if name == "not_utf8":
        p = tmp_path / "calibration.json"
        p.write_bytes(b"\xff\xfe\x00bad")
    elif isinstance(spec, str):
        p = write(tmp_path, spec)
    else:
        d = make()
        spec(d)
        p = write(tmp_path, d)
    out = CR.load(p)
    assert out == {"status": "invalid", "calibration": None, "message": CR.INVALID}
    assert "83/90" not in json.dumps(out) and "90/91" not in json.dumps(out)


def test_invalid_route_response_does_not_echo_file_contents(tmp_path):
    d = make()
    d["by_state"]["verified"]["matched"] = 90
    r = bare_client(write(tmp_path, d)).get("/api/calibration")
    assert r.status_code == 200
    assert r.json() == {"status": "invalid", "calibration": None, "message": CR.INVALID}


def test_problems_is_empty_for_a_valid_document_and_lists_faults_otherwise():
    assert CR.problems(make()) == []
    d = make()
    d["by_state"]["verified"]["matched"] = 90
    assert CR.problems(d)


def test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total(tmp_path):
    """T-099 r2 major. The state total and its own sentence are edited together, so the statement check passes and only the rule
    'state totals equal the sum over type totals' can reject it. Removing that rule must turn this test red."""
    d = make()
    d["by_state"]["verified"].update(matched=90, total=91)
    d["sentences"]["overall"]["verified"] = d["sentences"]["overall"]["verified"].replace("83/84", "90/91")
    assert CR.load(write(tmp_path, d)) == {"status": "invalid", "calibration": None, "message": CR.INVALID}
    assert any(p.startswith("by_state.verified.matched") for p in CR.problems(d))


# ---- stale (T-102): the recorded prompt hashes against the prompt files on disk (the ones the app loads), committed or not. Each test builds its own throwaway tree.

GIT = ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "-c", "user.name=qa", "-c", "user.email=qa@example.invalid"]


def git(repo, *args):
    subprocess.run([*GIT, "-C", str(repo), *args], check=True, capture_output=True)


def make_repo(tmp_path, prompts=None):
    """A git checkout with two prompts and a lexicon, committed. Hermetic: never touches the project's own repository."""
    repo = tmp_path / "repo"
    (repo / "app" / "llm" / "prompts").mkdir(parents=True)
    for name, text in (prompts or {"extract_v1.md": "extract\n", "judge_flag_v2.md": "flag v2\n"}).items():
        (repo / "app" / "llm" / "prompts" / name).write_text(text)
    (repo / "app" / "llm" / "lexicon.yaml").write_text("terms: []\n")
    git(repo, "init", "-q")
    git(repo, "add", "app")
    git(repo, "commit", "-q", "-m", "prompts")
    return repo


def recorded_for(root):
    """A valid document whose recorded hashes are the prompts under `root`, as a run from that checkout would record them."""
    d = make()
    d["hashes"] = CR.disk_prompt_hashes(root)
    return d


def commit_all_under_app(repo, message):
    git(repo, "add", "-A", "app")
    git(repo, "commit", "-q", "-m", message)


def test_current_when_recorded_hashes_match_the_prompts_on_disk(tmp_path):
    repo = make_repo(tmp_path)
    c = CR.load(write(tmp_path, recorded_for(repo)), root=repo)["calibration"]
    assert c["stale"] is False and c["stale_reason"] is None


def test_edited_and_committed_prompt_is_stale_and_the_reason_names_it(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v2.md").write_text("flag v2, tightened\n")
    commit_all_under_app(repo, "tighten flag prompt")
    out = CR.load(write(tmp_path, doc), root=repo)
    assert out["status"] == "ok"
    c = out["calibration"]
    assert c["stale"] is True
    assert c["stale_reason"] == ("The AI's instructions have changed since these numbers were measured: judge_flag_v2.md changed. "
                                 "The numbers describe an earlier version and may be out of date.")


def test_prompt_added_since_the_run_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v3.md").write_text("flag v3\n")
    commit_all_under_app(repo, "add flag v3")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "judge_flag_v3.md is new" in c["stale_reason"]


def test_prompt_removed_since_the_run_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    git(repo, "rm", "-q", "app/llm/prompts/extract_v1.md")
    git(repo, "commit", "-q", "-m", "retire extract v1")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "extract_v1.md was removed" in c["stale_reason"]


def test_lexicon_change_is_stale_too(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/lexicon.yaml").write_text("terms: [x]\n")
    commit_all_under_app(repo, "lexicon")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "lexicon.yaml changed" in c["stale_reason"]


def test_uncommitted_prompt_edit_is_stale_and_reverting_it_is_current(tmp_path):
    """T-102 review F1: the app loads the prompt files from disk, so an edit that is not committed already changes what runs and must read stale."""
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    path = repo / "app/llm/prompts/judge_flag_v2.md"
    path.write_text("edited, not committed\n")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "judge_flag_v2.md changed" in c["stale_reason"]
    path.write_text("flag v2\n")
    assert CR.load(write(tmp_path, doc), root=repo)["calibration"]["stale"] is False


def test_prompt_edited_in_a_temp_copy_of_the_real_prompts_is_stale(tmp_path):
    """The real prompt files and lexicon, copied: recorded from the copy as it is, then one real prompt is edited in the copy only."""
    real = CR.ROOT
    copy = tmp_path / "copy"
    shutil.copytree(real / "app" / "llm" / "prompts", copy / "app" / "llm" / "prompts")
    shutil.copy(real / "app" / "llm" / "lexicon.yaml", copy / "app" / "llm" / "lexicon.yaml")
    doc = recorded_for(copy)
    assert CR.load(write(tmp_path, doc), root=copy)["calibration"]["stale"] is False
    target = sorted((copy / "app" / "llm" / "prompts").glob("extract_*.md"))[0]
    target.write_text(target.read_text() + "\nAn uncommitted edit.\n")
    out = CR.load(write(tmp_path, doc), root=copy)
    assert out["status"] == "ok" and out["calibration"]["stale"] is True
    assert f"{target.name} changed" in out["calibration"]["stale_reason"]


def test_route_over_http_reports_an_uncommitted_prompt_edit_as_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/extract_v1.md").write_text("extract, edited and not committed\n")
    app = FastAPI()
    CR.add_routes(app, path=write(tmp_path, doc), root=repo)
    body = TestClient(app).get("/api/calibration").json()
    assert body["status"] == "ok" and body["calibration"]["stale"] is True
    assert "extract_v1.md changed" in body["calibration"]["stale_reason"]


def test_an_unreadable_current_prompt_set_is_stale_with_the_unchecked_reason_never_current(tmp_path, monkeypatch):
    """Fail closed: when the current prompts cannot be read the numbers are not shown as current (T-102 review F4, mutant: reason None)."""
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)

    def boom(root=None):
        raise PermissionError("denied")
    monkeypatch.setattr(CR, "disk_prompt_hashes", boom)
    out = CR.load(write(tmp_path, doc), root=repo)
    assert out["status"] == "ok"
    assert out["calibration"]["stale"] is True and out["calibration"]["stale_reason"] == CR.UNCHECKED


def test_a_tree_without_git_is_compared_on_disk_too(tmp_path):
    root = tmp_path / "copy"
    (root / "app" / "llm" / "prompts").mkdir(parents=True)
    (root / "app" / "llm" / "prompts" / "extract_v1.md").write_text("extract\n")
    (root / "app" / "llm" / "lexicon.yaml").write_text("terms: []\n")
    doc = recorded_for(root)
    assert CR.load(write(tmp_path, doc), root=root)["calibration"]["stale"] is False
    (root / "app" / "llm" / "prompts" / "extract_v1.md").write_text("extract, edited on disk\n")
    c = CR.load(write(tmp_path, doc), root=root)["calibration"]
    assert c["stale"] is True and "extract_v1.md changed" in c["stale_reason"]


def test_a_file_that_records_no_hashes_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    doc.pop("hashes")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "does not record which AI instructions" in c["stale_reason"]
    doc["hashes"] = {}
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "does not record which AI instructions" in c["stale_reason"]


def test_stale_reason_names_at_most_eight_files_and_counts_the_rest():
    recorded = {"old.md": "00"}
    current = {f"judge_{i:02d}.md": "11" for i in range(10)}
    reason = CR.stale_reason({"hashes": recorded}, current)
    assert reason.count(" is new") == 8 and "old.md was removed" not in reason
    assert reason.endswith("; and 3 more. The numbers describe an earlier version and may be out of date.")


def test_disk_hashes_are_the_hashes_evals_run_records(tmp_path):
    """The route and the producer (evals/run.py hashes()) must agree on the same files, or every fresh file would read as stale."""
    from evals.run import hashes as run_hashes
    repo = make_repo(tmp_path)
    assert CR.current_prompt_hashes(repo) == run_hashes(repo) == CR.disk_prompt_hashes(repo)


def test_route_serves_the_stale_flag_over_http(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v2.md").write_text("flag v2, tightened\n")
    commit_all_under_app(repo, "tighten flag prompt")
    app = FastAPI()
    CR.add_routes(app, path=write(tmp_path, doc), root=repo)
    body = TestClient(app).get("/api/calibration").json()
    assert body["status"] == "ok" and body["calibration"]["stale"] is True
    assert "judge_flag_v2.md changed" in body["calibration"]["stale_reason"]
    assert "hashes" not in body["calibration"]


# ---- the route on the real app, demo mode, read-only

@pytest.fixture
def app_client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "cal.sqlite"), static_dir=str(tmp_path)))


def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
    r = app_client.get("/api/calibration")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("ok", "missing", "invalid")
    assert ("calibration" in body) and (body["calibration"] is None) == (body["status"] != "ok")


def test_route_carries_no_case_tokens_or_record_text(app_client):
    body = app_client.get("/api/calibration").json()
    text = json.dumps(body)
    assert "token" not in text and "raw_text" not in text and "records" not in text


def test_route_is_read_only(app_client):
    assert app_client.post("/api/calibration", json={}).status_code == 405
    assert app_client.put("/api/calibration", json={}).status_code == 405
    assert app_client.patch("/api/calibration", json={}).status_code == 405
    assert app_client.delete("/api/calibration").status_code == 405
