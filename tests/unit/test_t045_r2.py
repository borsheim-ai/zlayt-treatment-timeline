"""T-045 r2: (1) a rejected item can only be dismissed or reset (ADR-005, review.py item_rejected guard); (2) `evals.run --record-latest` points latest.json at an existing
report with provenance, and a fixture run never replaces a live latest.json."""
import json, pathlib, shutil
import pytest
from app.backend import review as RV
from app.db import db as DB
from evals import run as R
from tests.unit.test_review_rules import seeded, ent, judge, amt

REPORTS = pathlib.Path(R.REPORTS)
LIVE_MD = REPORTS / "20261102T164038Z.md"


# ---- (1) rejected items
def _rejected(tmp_path):
    conn, cid, out = seeded(tmp_path)
    e = ent(out, 5)
    DB.update_item(conn, e, now=2.0, case=cid, state="rejected")
    return conn, cid, e


@pytest.mark.parametrize("body", [dict(action="accept"), dict(action="edit", edits={"summary": "Visit completed."})])
def test_rejected_item_cannot_be_accepted_or_edited(tmp_path, body):
    """ADR-005: accept and edit on a rejected item are 409 item_rejected, and nothing is written (the item stays pending, no event)."""
    conn, cid, e = _rejected(tmp_path)
    before = DB.get_item(conn, e, cid)["review_status"]
    n_events = len(DB.list_events(conn, cid, e))
    with pytest.raises(RV.ReviewError) as x:
        RV.apply_review(conn, cid, e, body, call=judge("supported"))
    assert (x.value.status, x.value.code) == (409, "item_rejected")
    assert DB.get_item(conn, e, cid)["review_status"] == before == "pending"
    assert len(DB.list_events(conn, cid, e)) == n_events


def test_rejected_item_can_still_be_dismissed_and_reset(tmp_path):
    """The other half of the rule: dismiss and reset are the two ways out for a rejected item; neither is blocked by the guard."""
    conn, cid, e = _rejected(tmp_path)
    assert RV.apply_review(conn, cid, e, dict(action="dismiss"))["item"]["review_status"] == "dismissed"
    assert RV.apply_review(conn, cid, e, dict(action="reset"))["item"]["review_status"] == "pending"
    with pytest.raises(RV.ReviewError) as x:
        RV.apply_review(conn, cid, e, dict(action="accept"))
    assert x.value.code == "item_rejected"


# ---- (2) latest.json pointer
def _copy_report(tmp_path):
    shutil.copy(LIVE_MD, tmp_path / LIVE_MD.name)
    return tmp_path / LIVE_MD.name


def test_record_latest_parses_every_value_from_the_report(tmp_path):
    md = _copy_report(tmp_path)
    assert R.main(["--record-latest", str(md), "--out", str(tmp_path)]) == 0
    d = json.loads((tmp_path / "latest.json").read_text())
    assert d["ship_bar_met"] is True and d["backend"] == "claude-cli" and d["models"]["judge"] == "claude-haiku-5-5"
    assert d["generated_at"] == "2026-11-02T16:40:38Z" and d["source"] == {"commit": "312efe663327539df1b712832e23bf1d2c495d42", "clean": True}
    assert d["recorded_from"]["report"] == md.name and d["recorded_from"]["sha256"] == R.sha256_file(md) and len(d["hashes"]) == 17
    assert R.parse_report_md(md.read_text())["hashes"] == d["hashes"]


def test_record_latest_refuses_a_header_that_disagrees_in_either_direction(tmp_path, capsys):
    """Nothing is typed in: a live report whose header says False but whose body meets the bar is refused too (the header is never the source)."""
    md = _copy_report(tmp_path); md.write_text(md.read_text().replace("**ship_bar_met: True**", "**ship_bar_met: False**", 1))
    assert R.main(["--record-latest", str(md), "--out", str(tmp_path)]) == 2 and not (tmp_path / "latest.json").exists()
    assert "header says ship_bar_met False" in capsys.readouterr().err


def test_record_latest_refuses_a_non_report_and_a_report_outside_out(tmp_path):
    bad = tmp_path / "x.md"; bad.write_text("not a report")
    assert R.main(["--record-latest", str(bad), "--out", str(tmp_path)]) == 2 and not (tmp_path / "latest.json").exists()
    other = tmp_path / "elsewhere"; other.mkdir(); md = _copy_report(other)
    assert R.main(["--record-latest", str(md), "--out", str(tmp_path / "out")]) == 2 and not (tmp_path / "out" / "latest.json").exists()


def test_check_fresh_notices_a_report_changed_after_it_was_recorded(tmp_path):
    md = _copy_report(tmp_path)
    (tmp_path / "app" / "llm" / "prompts").mkdir(parents=True)
    R.main(["--record-latest", str(md), "--out", str(tmp_path)])
    d = json.loads((tmp_path / "latest.json").read_text()); d["hashes"] = R.hashes(tmp_path)       # make the prompt hashes equal the (empty) tree
    (tmp_path / "latest.json").write_text(json.dumps(d))
    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 0
    md.write_text(md.read_text() + "\nedited by hand\n")
    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 1


def test_a_fixture_run_does_not_replace_a_live_latest_json(tmp_path):
    from tests.unit.test_eval_runner import report
    md = _copy_report(tmp_path); R.main(["--record-latest", str(md), "--out", str(tmp_path)])
    before = (tmp_path / "latest.json").read_text()
    R.write_report(report(backend="fixture"), tmp_path)
    assert (tmp_path / "latest.json").read_text() == before and (tmp_path / "latest.fixture.json").exists()
    R.write_report(report(backend="claude-cli"), tmp_path)                    # a live run replaces it, as before
    assert json.loads((tmp_path / "latest.json").read_text()).get("recorded_from") is None


def test_a_fixture_run_still_writes_latest_json_when_none_is_live(tmp_path):
    from tests.unit.test_eval_runner import report
    R.write_report(report(backend="fixture"), tmp_path)
    assert json.loads((tmp_path / "latest.json").read_text())["backend"] == "fixture" and not (tmp_path / "latest.fixture.json").exists()


# ---- (3) round 3: --record-latest recomputes the ship bar; the header line is never trusted

def _fixture_like(tmp_path):
    """A fixture-backend report as the runner writes it (render_md), with its header hand-flipped to True."""
    from tests.unit.test_eval_runner import report
    r = report(backend="fixture")
    assert r["ship_bar_met"] is False
    md = tmp_path / "20261102T203245Z.md"
    md.write_text(R.render_md(r))
    md.write_text(md.read_text().replace("**ship_bar_met: False**", "**ship_bar_met: True**", 1))
    assert "**ship_bar_met: True**" in md.read_text()
    return md


def _refused(tmp_path, md, capsys, root=R.ROOT):
    assert R.record_latest(md, tmp_path, root) == 2
    assert not (tmp_path / "latest.json").exists()
    return capsys.readouterr().err


def test_record_latest_refuses_a_hand_flipped_fixture_report(tmp_path, capsys):
    md = _fixture_like(tmp_path)
    assert "not a live backend" in _refused(tmp_path, md, capsys)


def test_record_latest_refuses_a_fixture_report_relabelled_as_live(tmp_path, capsys):
    """Header edited twice (backend and bar): the body still says determinism was not measured and names no per-run directory."""
    md = _fixture_like(tmp_path)
    md.write_text(md.read_text().replace("backend `fixture`", "backend `claude-cli`", 1))
    assert R.record_latest(md, tmp_path) == 2 and not (tmp_path / "latest.json").exists()


def test_record_latest_refuses_a_flipped_live_report_whose_metrics_fail_the_bar(tmp_path, capsys):
    md = _copy_report(tmp_path)
    txt = md.read_text()
    assert "| entry_recall | 0.982 |" in txt
    md.write_text(txt.replace("| entry_recall | 0.982 |", "| entry_recall | 0.500 |", 1))        # the body now fails bar 2; the header still says True
    err = _refused(tmp_path, md, capsys)
    assert "header says ship_bar_met True" in err and "is False (failing: 2_recall)" in err


def test_record_latest_refuses_a_live_report_failing_other_bars(tmp_path, capsys):
    """Each edit below fails a different bar while the header says True; every one is refused."""
    for old, new in [("| grounding_rate | 1.000 (242 checked)", "| grounding_rate | 0.990 (242 checked)"),
                     ("| unsupported_count_3run | 0 |", "| unsupported_count_3run | 1 |"),
                     ("| golden_must_not_hits | 0 |", "| golden_must_not_hits | 2 |"),
                     ("| case_07_total_420 | True |", "| case_07_total_420 | False |")]:
        md = _copy_report(tmp_path)
        txt = md.read_text()
        assert old in txt, old
        md.write_text(txt.replace(old, new, 1))
        assert R.record_latest(md, tmp_path) == 2, old
        assert not (tmp_path / "latest.json").exists()
        capsys.readouterr()


def test_record_latest_takes_determinism_from_the_run_directory_not_the_table(tmp_path, capsys):
    """The table says 1.0; the three run files in a copy of the run directory differ, so the recomputed value is below the bar."""
    root = tmp_path / "repo"
    src = R.ROOT / "evals" / "reports" / "runs" / "20261102T161327Z"
    dst = root / "evals" / "reports" / "runs" / "20261102T161327Z"
    shutil.copytree(src, dst)
    out = tmp_path / "reports"; out.mkdir()
    md = out / LIVE_MD.name; shutil.copy(LIVE_MD, md)
    (root / "app" / "llm" / "prompts").mkdir(parents=True)
    r2 = json.loads((dst / "run2.json").read_text()); r2["signature_parts"]["entry_ids"] = r2["signature_parts"]["entry_ids"][:-1]
    (dst / "run2.json").write_text(json.dumps(r2))
    assert R.record_latest(md, out, root) == 2
    assert "is False" in capsys.readouterr().err and not (out / "latest.json").exists()


def test_record_latest_refuses_when_the_per_run_directory_is_missing(tmp_path, capsys):
    md = _copy_report(tmp_path)
    empty_root = tmp_path / "elsewhere"; empty_root.mkdir()
    assert "per-run directory" in _refused(tmp_path, md, capsys, root=empty_root)


def test_record_latest_accepts_the_real_live_report_and_records_provenance(tmp_path):
    md = _copy_report(tmp_path)
    assert R.record_latest(md, tmp_path) == 0
    d = json.loads((tmp_path / "latest.json").read_text())
    assert d["ship_bar_met"] is True and d["backend"] == "claude-cli"
    rf = d["recorded_from"]
    assert rf["sha256"] == R.sha256_file(md) and rf["source_commit"] == "312efe663327539df1b712832e23bf1d2c495d42"
    assert rf["run_artifacts"] == "evals/reports/runs/20261102T161327Z" and rf["ship_bar_recomputed"] is True


def test_the_committed_latest_json_still_matches_what_record_latest_would_write(tmp_path):
    md = _copy_report(tmp_path); R.record_latest(md, tmp_path)
    want = json.loads((tmp_path / "latest.json").read_text())
    have = json.loads((REPORTS / "latest.json").read_text())
    for d in (want, have):
        d["recorded_from"].pop("recorded_at")
    assert have == want


def test_report_body_parse_matches_the_runner_on_a_rendered_report():
    """The recompute reads the rendered body: for a report the runner just built, it must reach the runner's own answer."""
    from tests.unit.test_eval_runner import report
    r = report(backend="claude-cli")
    r["run_artifacts"] = None
    txt = R.render_md(r)
    m, a, spec = R.metrics_from_report_md(txt)
    assert spec is r["spec_matches_golden"] and a == r["assertions"]
    for k in ("grounding_rate", "entry_recall", "amount_recall"):
        assert m[k]["value"] == r["metrics"][k]["value"]
    for t in R.FLAG_TYPES:
        assert (m["flag_precision"][t], m["flag_recall"][t]) == (r["metrics"]["flag_precision"][t], r["metrics"]["flag_recall"][t])


def test_the_fixture_bar_4_blocker_names_its_live_only_clauses():
    from tests.unit.test_eval_runner import report
    r = report(backend="fixture")
    assert "4_no_invented_facts" in r["blockers"]
    assert any("determinism_3run" in b and "4_no_invented_facts" in b for b in r["blockers"])
