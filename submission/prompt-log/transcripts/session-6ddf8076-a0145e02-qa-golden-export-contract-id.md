# Subagent: QA: golden export + contract id (QA: golden export + contract id)

Source: `agent-a0145e02d7dfd3d58.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:47:22.901Z

Two small qa fixes in /Users/arsis/zlayt-pm-project:

1. **T-072 follow-through** (memory/ORCHESTRATOR_DECISIONS.md D-040): read the card note on T-072 (`python3 tools/board.py show T-072`) and update evals/golden/sample.export.expected.txt lines 58 and 69 exactly as specified there, plus any other golden that still expects "(patient self-report)" or the "Patient self-report" flag title. Then run:
   - `tests/fixtures/make_curated.py --check`;
   - `.venv/bin/python -m pytest -q tests/unit`;
   - `python -m evals.run`.
   Hallucination catch must be 40/40, and the export golden tests must pass.
2. tests/unit/test_e2e_contract fails because the test id `btn-undo-batch`, used in tests/e2e/test_edit.py (T-065), is not declared. Declare it the way the other ids are declared.

Commit with the pathspec rule (`git add <paths>`, then `git commit -m "..." -- <paths>` as separate commands), or with a temp index if another worker has hunks in the same file. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Add a note on T-072 with the commit and test results. Reply in 2 lines.

### User / tool · 2026-11-02T02:47:22.909Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:25.267Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-072 | tail -60; grep -rn \"patient self-report\\|Patient self-report\" evals tests --include=* -il | head -30"
}
````

### User / tool · 2026-11-02T02:47:25.443Z

**tool result**
````
---
id: "T-072"
title: "Neutral title for patient_reported_onset flag; drop '(patient self-report)' from export (D-040 follow-through)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:45:10Z"
updated_at: "2026-11-02T02:47:13Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:45:23Z"
rounds: 0
commits: ["3b6a3fe"]
reviews: []
ac:
  - {"n": 1, "text": "Flag title no longer asserts the speaker (e.g. 'Reported onset'); export no longer appends '(patient self-report)'; flag templates, export tests and golden expectations updated (qa note for golden lines); hallucination catch 40/40", "done": true, "evidence": "commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:45:23Z backend: claimed
- 2026-11-02T02:47:12Z backend: QA ACTION (golden is yours, not edited): evals/golden/sample.export.expected.txt remove the suffix ' (patient self-report)' on line 58 (INTERNAL REVIEW causation entry for record 9: ...January collision." (patient self-report); record 7 -> ...January collision."; record 7) and on line 69 ('Causation language (patient self-report).' -> 'Causation language.'). Until then tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden... and make_curated --check ('notes equal: False', letter equal True) fail. check_golden.py:543 .replace(' (patient self-report)','') is now a harmless no-op, can be dropped. Unrelated pre-existing failure: tests/unit/test_e2e_contract.py::test_every_test_id_is_declared ('btn-undo-batch', frontend). evals.run: hallucination_catch 40/40; blocker 4_no_invented_facts + fixture-determinism were already present in the prior report. Coordinator ask re patient_report template: neutralized (key kept as internal category id; title 'Reported onset', explanation 'Onset wording reported in ...'). Renaming the category id would change prompts/flags_v1.md (hash -> fixture re-record), lexicon.yaml (researcher), curated fixtures, frontend mocks; and flags_v1.md:13 still defines it as 'the patient's own statement' - propose follow-up card if wanted.
- 2026-11-02T02:47:12Z backend: AC 1 checked: commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)
- 2026-11-02T02:47:13Z backend: moved in_progress -> in_review

## Handoff
Changed: patient_report template title -> 'Reported onset' (explanation 'Onset wording reported in ...'); removed both '(patient self-report)' suffixes and _SELF_REPORT_SUBTYPES from export.py; updated export/e2e tests, added neutral-title test. Verified: pytest tests/unit (940 pass; export golden byte-exact tests fail until qa edits sample.export.expected.txt lines 58 and 69, listed in note); evals.run hallucination 40/40. Left: qa golden edit; optional follow-up to rename category id/prompt line (needs fixture re-record). Surprised: category id patient_report is wired through prompt, lexicon, fixtures, so only user-facing text was neutralized.

evals/golden/check_golden.py
evals/golden/sample.export.expected.txt
evals/golden/sample.expected.json
evals/golden/hallucinations.jsonl
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:25.884Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-040\" -A15 memory/ORCHESTRATOR_DECISIONS.md | head -50; git status --short | head -30"
}
````

### User / tool · 2026-11-02T02:47:26.025Z

**tool result**
````
48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/llm/backends/fixture.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
 M board/cards/T-065.md
 M board/cards/T-066.md
 M board/cards/T-067.md
 M evals/reports/latest.json
 M evals/run.py
 M memory/LESSONS.md
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
 M tests/fixtures/llm/067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
 M tests/fixtures/llm/096042ca0286b135b1ff8db5f6d20a32cbf7c3989c5e10fc7ef5bf33da0670c2.json
 M tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
 M tests/fixtures/llm/0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
 M tests/fixtures/llm/11245ae85d4b50423fb2ce331e7adbe7b3436e8dccf11252c833ecfa6e11db67.json
 M tests/fixtures/llm/128383b890348cd75ed0f2eb15f8516ffb0e90785d18225192c7a1b405bcf58d.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:27.995Z

**tool call — Bash**
````
{
 "command": "sed -n '58p;69p' evals/golden/sample.export.expected.txt; grep -n -i \"self-report\" evals/golden/check_golden.py evals/golden/sample.expected.json evals/golden/hallucinations.jsonl | cut -c1-220; grep -rn \"btn-undo-batch\" tests | head; grep -n \"btn-undo\\|btn-\" tests/unit/test_e2e_contract.py | head -20"
}
````

### User / tool · 2026-11-02T02:47:28.173Z

**tool result**
````
- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
evals/golden/check_golden.py:21:    date; summaries satisfy required_terms (summary alone) and keep self-report attribution; numbers in summaries come from the
evals/golden/check_golden.py:491:                errs.append(f"export letter: summary for record {n} drops the self-report attribution for {sp['excerpt'][:30]!r}")
evals/golden/check_golden.py:543:        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
evals/golden/hallucinations.jsonl:10:{"id": "H10", "synthetic": true, "category": "causation", "record_text": "Record 9 | 2026-06-12 | Hill Country Pain Management, follow-up | \"Recommend cervical epidural steroid injec
evals/golden/sample.expected.json:626:      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
evals/golden/sample.expected.json:992:      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
tests/e2e/test_edit.py:60:    expect(page.get_by_test_id("btn-undo-batch")).to_be_visible()
tests/e2e/test_edit.py:66:        page.get_by_test_id("btn-undo-batch").click()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:30.614Z

**tool call — Bash**
````
{
 "command": "sed -i '58s/ (patient self-report)//;69s/Causation language (patient self-report)\\./Causation language./' evals/golden/sample.export.expected.txt && sed -n '58p;69p' evals/golden/sample.export.expected.txt | grep -c \"self-report\"; sed -n 1,60p tests/unit/test_e2e_contract.py; grep -rn \"btn-undo\\|btn-redo\\|undo\" app/frontend --include=* -l | head"
}
````

### User / tool · 2026-11-02T02:47:30.724Z

**tool result**
````
sed: 1: "evals/golden/sample.exp ...": invalid command code e
"""E2E hook contract (R-ST-1, R-RV-8): every data-testid, data-attribute, role and shortcut used by tests/e2e specs is declared in tests/e2e/conftest.py's docstring,
so the frontend builds to one source (T-039 review)."""
import pathlib, re
E2E = pathlib.Path(__file__).resolve().parents[1] / "e2e"

def contract():
    s = (E2E / "conftest.py").read_text().split('"""')[1]
    return s

def specs():
    return [p for p in E2E.glob("test_*.py")]

def test_every_test_id_is_declared():
    """R-ST-1: get_by_test_id hooks in specs are named in the conftest contract (<seq>/<raw> placeholders allowed)."""
    c = contract(); used = set()
    for p in specs():
        for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
            used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
    missing = []
    for u in used:
        pat = u.replace("<seq>", "<seq>") 
        if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
            missing.append(u)
    assert not missing, missing

def test_data_attributes_declared():
    """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
    c = contract()
    for p in specs():
        for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
            assert a in c, (p.name, a)

def test_roles_and_inputs_and_keys_declared():
    """R-RV-8: role=alert, tabindex, input names and a/d/j shortcuts are declared."""
    c = contract()
    for needle in ("role=alert", "tabindex", "input named date or provider", "a = accept", "d = dismiss", "j = next"):
        assert needle in c
app/frontend/batch.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:32.639Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='evals/golden/sample.export.expected.txt'\nL=open(p).read().split('\\n')\nL[57]=L[57].replace(' (patient self-report)','')\nL[68]=L[68].replace('Causation language (patient self-report).','Causation language.')\nopen(p,'w').write('\\n'.join(L))\nE\ngrep -c \"self-report\" evals/golden/sample.export.expected.txt; sed -n 1,50p tests/e2e/conftest.py; grep -n \"undo\" app/frontend/batch.js | head -5; git diff --stat tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T02:47:32.779Z

**tool result**
````
0
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

@pytest.fixture
def base_url():
24:      const u = document.querySelector('[data-testid="btn-undo-batch"]'); if (u) u.focus();
28:  async function undo() {
44:    const undoable = last && last.token === c.token && last.ids.some((id) => { const f = RV.find(c, id); return f && f.item.review_status === "accepted"; });
47:      undoable ? el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-undo-batch", onclick: undo }, "Undo last batch (" + last.ids.length + ")") : null,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:34.909Z

**tool call — Bash**
````
{
 "command": "sed -i 's/btn-accept-verified, btn-dismiss,/btn-accept-verified, btn-undo-batch, btn-dismiss,/' tests/e2e/conftest.py && git diff --stat tests/e2e/conftest.py evals/golden/sample.export.expected.txt; tests/fixtures/make_curated.py --check 2>&1 | tail -5; .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -6; python -m evals.run 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:47:56.717Z

**tool result**
````
sed: 2: "tests/e2e/conftest.py
": undefined label 'ests/e2e/conftest.py'
/bin/bash: tests/fixtures/make_curated.py: Permission denied
FAILED tests/unit/test_eval_runner.py::test_check_spec_recomputes_the_bar_in_a_full_report
FAILED tests/unit/test_eval_runner.py::test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4
FAILED tests/unit/test_eval_spec_check.py::test_real_spec_matches_golden - As...
FAILED tests/unit/test_eval_spec_check.py::test_cli_writes_spec_matches_golden_to_latest_json
FAILED tests/unit/test_narrative.py::test_recorded_sample_paragraph_replays_with_every_sentence_supported
7 failed, 937 passed in 20.97s
/bin/bash: python: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:47:59.322Z

**tool call — Bash**
````
{
 "command": "python3 - <<'E'\np='tests/e2e/conftest.py'\ns=open(p).read()\nassert 'btn-accept-verified, btn-dismiss,' in s\nopen(p,'w').write(s.replace('btn-accept-verified, btn-dismiss,','btn-accept-verified, btn-undo-batch, btn-dismiss,',1))\nE\ngit diff --stat tests/e2e/conftest.py evals/golden/sample.export.expected.txt; .venv/bin/python tests/fixtures/make_curated.py --check 2>&1 | tail -5; .venv/bin/python -m pytest -q tests/unit 2>&1 | grep -E \"FAILED|passed|failed\"; .venv/bin/python -m evals.run 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T02:48:22.385Z

**tool result**
````
 evals/golden/sample.export.expected.txt | 4 ++--
 tests/e2e/conftest.py                   | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
entries: 9 non-verified: []
narrative: 9 sentences, removed: []
letter equal: True | notes equal: True
E       AssertionError: assert (not 'LLM_FAILED_AFTER_RETRIES')
E        +  where 'LLM_FAILED_AFTER_RETRIES' = <built-in method get of dict object at 0x10d334780>('error')
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c5e0cebddc22c step=narrative attempt=1 prompt_hash=e7ed16d363ed2bfc9082eff9545c29396c6639f24cf28336480f09bad13ef6d8
FAILED tests/unit/test_eval_runner.py::test_perfect_run_meets_ship_bar_on_a_live_backend
FAILED tests/unit/test_eval_runner.py::test_check_spec_recomputes_the_bar_in_a_full_report
FAILED tests/unit/test_eval_runner.py::test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4
FAILED tests/unit/test_eval_spec_check.py::test_real_spec_matches_golden - As...
FAILED tests/unit/test_eval_spec_check.py::test_cli_writes_spec_matches_golden_to_latest_json
FAILED tests/unit/test_narrative.py::test_recorded_sample_paragraph_replays_with_every_sentence_supported
6 failed, 938 passed in 20.58s
llm call failed call_id=c24b6f27e3d87 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=cb65d91139600 step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=cdbda0c27b2ae step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c2ab7724eb67d step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=c66f27f719d4c step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
llm call failed call_id=c6587738ccb00 step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
llm call failed call_id=cf9f813d6ae04 step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T024822Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: spec_matches_golden is false
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:24.432Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_eval_spec_check.py::test_real_spec_matches_golden tests/unit/test_narrative.py 2>&1 | grep -E \"^E|Error\" | head -20; git diff --stat app/llm/backends/fixture.py evals/run.py; git log --oneline -3 -- app/llm/backends/fixture.py; grep -n \"hallucination\" evals/reports/latest.json | head -3"
}
````

### User / tool · 2026-11-02T02:48:28.358Z

**tool result**
````
E       AssertionError: assert {'spec_matche...equal': False} == {'spec_matche..._equal': True}
E         
E         Omitting 1 identical items, use -vv to show
E         Differing items:
E         {'internal_notes_equal': False} != {'internal_notes_equal': True}
E         {'spec_matches_golden': False} != {'spec_matches_golden': True}
E         Use -v to get more diff
tests/unit/test_eval_spec_check.py:8: AssertionError
E       AssertionError: assert (not 'LLM_FAILED_AFTER_RETRIES')
E        +  where 'LLM_FAILED_AFTER_RETRIES' = <built-in method get of dict object at 0x109920440>('error')
E        +    where <built-in method get of dict object at 0x109920440> = {'status': 'pending', 'generated_at': '1970-01-01T00:00:02Z', 'sentences': [], 'removed': [], ...}.get
tests/unit/test_narrative.py:154: AssertionError
 app/llm/backends/fixture.py | 2 ++
 evals/run.py                | 6 ++++++
 2 files changed, 8 insertions(+)
c9f272a fix(backend): export maps pipeline output to golden (amount sentence, PT plan label, self-report marker, record-1 quote); FIXTURE_SET support
958c353 feat(backend): LLM provider, claude-cli/anthropic-api/fixture backends, audited retries, recorder (T-034)
127:  "hallucination_catch_rate": {
791:  "hallucination_catch_rate": 0.95,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:30.612Z

**tool call — Bash**
````
{
 "command": "sed -n 1,15p tests/unit/test_eval_spec_check.py; git diff app/llm/backends/fixture.py evals/run.py | head -50; git stash list | head -2; git status --short | grep -v \"tests/fixtures/llm\\|board/\\|agent-memory\""
}
````

### User / tool · 2026-11-02T02:48:30.666Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not run git stash (it rewinds shared board/memory files of other agents)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:31.984Z

**tool call — Bash**
````
{
 "command": "sed -n 1,15p tests/unit/test_eval_spec_check.py; git diff app/llm/backends/fixture.py evals/run.py | head -50; git status --short | grep -v \"tests/fixtures/llm\\|board/\\|agent-memory\""
}
````

### User / tool · 2026-11-02T02:48:32.173Z

**tool result**
````
"""evals.run --check-spec: REQUIREMENTS section 6 blocks vs golden export, byte-equal. T-038 AC2, R-EX-6."""
import json
from evals import run as R

def test_real_spec_matches_golden():
    """AC2: today's REQUIREMENTS section 6 block 1 and 2 equal LETTER_TEXT and INTERNAL_NOTES_TEXT."""
    s = R.check_spec()
    assert s == {"spec_matches_golden": True, "letter_equal": True, "internal_notes_equal": True}

def test_changing_one_character_in_a_temp_copy_makes_it_false(tmp_path):
    """AC2: one changed character in a temp copy of REQUIREMENTS (letter block, then notes block) flips spec_matches_golden to false."""
    text = R.REQUIREMENTS.read_text()
    b1, b2 = R.spec_blocks(text)
    for i, blk, key in ((1, b1, "letter_equal"), (2, b2, "internal_notes_equal")):
        p = tmp_path / f"req{i}.md"
diff --git a/app/llm/backends/fixture.py b/app/llm/backends/fixture.py
index 635f521..db39749 100644
--- a/app/llm/backends/fixture.py
+++ b/app/llm/backends/fixture.py
@@ -20,6 +20,8 @@ def fixture_dir() -> pathlib.Path:
 def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
     p = fixture_dir() / f"{key}.json"
     t0 = time.monotonic()
+    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
+        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
     if not p.is_file():
         raise FixtureMiss(key)
     try:
diff --git a/evals/run.py b/evals/run.py
index e4ef1c3..eb3b0e2 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -677,6 +677,12 @@ def main(argv=None, pipeline=None):
         print(f"evals.run: {e}", file=sys.stderr)
         return 2
     backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
+    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
+        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
+        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
+        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
+              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
+        return 2
     report = build_report(pipeline or load_pipeline(), backend, a.runs)
     path = write_report(report, out)
     print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
 M app/llm/backends/fixture.py
 M evals/golden/sample.export.expected.txt
 M evals/reports/latest.json
 M evals/run.py
 M memory/LESSONS.md
 M tests/e2e/conftest.py
 M tests/fixtures/make_curated.py
 M tests/unit/test_eval_runner.py
 M tools/board_ui.html
 M tools/tests/test_board_server.py
?? artifacts/review-evidence/
?? artifacts/screenshots/office-multilevel-desktop-all.png
?? artifacts/screenshots/office-multilevel-desktop-board.png
?? artifacts/screenshots/office-multilevel-desktop-break.png
?? artifacts/screenshots/office-multilevel-mobile-390-all.png
?? artifacts/screenshots/office-multilevel-mobile-390-board.png
?? artifacts/screenshots/office-multilevel-mobile-390-break.png
?? data/
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
?? evals/reports/20261102T024653Z.md
?? evals/reports/20261102T024822Z.md
?? reviews/T-006-security-r2.md
?? reviews/T-006-security-r3.md
?? reviews/T-006-security.md
?? reviews/T-053-security-r2.md
?? reviews/T-057-staff-engineer-r4.md
?? reviews/T-061-claims-adjuster-r4.md
?? reviews/T-063-staff-engineer-r2.md
?? reviews/T-065-staff-engineer.md
?? reviews/T-066-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:35.410Z

**tool call — Bash**
````
{
 "command": "grep -n \"self-report\" spec/REQUIREMENTS.md | cut -c1-200; .venv/bin/python -m pytest -q tests/unit/test_eval_runner.py 2>&1 | grep -E \"^E \" | head -8; grep -E \"hallucination_catch|blocker\" evals/reports/20261102T024822Z.md | head"
}
````

### User / tool · 2026-11-02T02:48:37.672Z

**tool result**
````
55:| R-TL-8 | **A hedge travels with its finding (D-018, D-021).** The **hedge set** is the lexicon entries with `hedge: true` in `app/llm/lexicon.yaml` (D-018); today `may_represent`, `correlate_clin
57:| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's ex
71:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presente
280:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged fro
291:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
E       AssertionError: assert (['spec_matche...den is false'] == []
E         
E         Left contains one more item: 'spec_matches_golden is false'
E         Use -v to get more diff)
E       assert False is True
E       assert (True is True and False is True)
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:42.630Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B new --title \"Update spec/REQUIREMENTS.md section 6 blocks (lines 280, 291) to match D-040 export golden: drop '(patient self-report)'\" --milestone M3 --role architect --priority P1 --ac \"REQUIREMENTS.md line 280 drops ' (patient self-report)' after the record 9 causation quote; line 291 reads 'Causation language.'; evals.run --check-spec returns spec_matches_golden true; tests/unit/test_eval_spec_check.py and test_eval_runner.py pass\" 2>&1 | tail -2\ngit add evals/golden/sample.export.expected.txt tests/e2e/conftest.py && git commit -m \"fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/golden/sample.export.expected.txt tests/e2e/conftest.py 2>&1 | tail -2; git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T02:48:42.767Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: B="python3 tools/board.py"; $B new --title "Update spec/REQUIREMENTS.md section 6 blocks (lines 280, 291) to match D-040 export golden: drop '(patient self-report)'" --milestone M3 --role architect --
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:44.724Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py new --title \"Update spec/REQUIREMENTS.md section 6 blocks (lines 280, 291) to match D-040 export golden: drop '(patient self-report)'\" --milestone M3 --role architect --priority P1 --ac \"REQUIREMENTS.md line 280 drops ' (patient self-report)' after the record 9 causation quote; line 291 reads 'Causation language.'; evals.run --check-spec returns spec_matches_golden true; tests/unit/test_eval_spec_check.py and test_eval_runner.py pass\" 2>&1 | tail -2; git add evals/golden/sample.export.expected.txt tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T02:48:44.907Z

**tool result**
````
T-074
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:46.455Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/golden/sample.export.expected.txt tests/e2e/conftest.py 2>&1 | tail -2; git log -1 --format=%h"
}
````

### User / tool · 2026-11-02T02:48:46.885Z

**tool result**
````
[main 4594bb7] fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id
 2 files changed, 3 insertions(+), 3 deletions(-)
4594bb7
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:50.139Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-072 --sha 4594bb7 --agent qa | tail -1; python3 tools/board.py note T-072 --agent qa --text \"Golden done in 4594bb7 (lines 58, 69; btn-undo-batch declared in tests/e2e/conftest.py). make_curated --check: letter+notes equal True. unit: 938 pass, 6 fail; export golden tests pass. evals.run hallucination_catch 40/40 (evals/reports/20261102T024822Z.md), ship_bar false only on live-only/spec blockers. REMAINING: spec/REQUIREMENTS.md lines 280 and 291 still carry '(patient self-report)' so check_spec spec_matches_golden=false (fails test_eval_spec_check x2, test_eval_runner x3): not qa-owned, filed T-074 (architect). Separate: test_narrative::test_recorded_sample_paragraph_replays... fails LLM_FAILED_AFTER_RETRIES (fixture miss, not golden-related; fixture.py has uncommitted edits by another worker).\" | tail -1"
}
````

### User / tool · 2026-11-02T02:48:50.500Z

**tool result**
````
T-072: commit 4594bb7 recorded
noted on T-072
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T02:48:52.963Z

Golden lines 58 and 69 are fixed and `btn-undo-batch` is declared in `tests/e2e/conftest.py`. Commit 4594bb7 is recorded on T-072 with a note. Six unit tests still fail: five because `spec/REQUIREMENTS.md` lines 280 and 291 still say "(patient self-report)", so I filed T-074 for architect; the sixth is a fixture-miss failure in `test_narrative`.

`make_curated.py --check` shows letter and notes equal, and the export golden tests pass. `evals.run` hallucination catch is 40/40. Unit tests are 938 passed, 6 failed (`test_eval_spec_check` x2, `test_eval_runner` x3, `test_narrative` x1). The `test_narrative` failure is `LLM_FAILED_AFTER_RETRIES`, which looks unrelated to the golden, and another worker has uncommitted edits in `app/llm/backends/fixture.py`.
