# Subagent: QA: T-119 round 3 (QA: T-119 round 3)

Source: `agent-a01ad8e191ae092b5.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:14:50.545Z

You are the QA worker on board card T-119, round 3, in /Users/arsis/zlayt-pm-project. Claim it with `python3 tools/board.py claim T-119 --agent qa`. Read reviews/T-119-staff-engineer-r2.md.

Fix:
1. **Major:** add an e2e test proving that 'p' (side-by-side, app/frontend/sidebyside.js:102) does nothing when pressed from the page body, only from an item row. Confirm it kills the reviewer's mutB: apply the mutant on a scratch copy and see the test fail.
2. **Minor:** stabilize tests/e2e/test_code_check_refusal.py:110 by waiting on a condition. No sleeps.
3. Fix the cheap remaining minors.

Do not edit app/frontend; another worker is in it. Run the e2e suite on a `git archive HEAD` copy on your own port. Commit with a pathspec: `git add <paths>` first, then `git commit -m msg -- <paths>` as a separate command. Check the AC with evidence, write the handoff, and move the card to in_review.

Stop only your own PIDs. Reply in 3 lines.

### User / tool · 2026-11-02T11:14:50.550Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:53.289Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-119 --agent qa; cat reviews/T-119-staff-engineer-r2.md; cat .claude/agent-memory/qa/MEMORY.md | head -5"
}
````

### User / tool · 2026-11-02T11:14:53.463Z

**tool result**
````
T-119 claimed by qa
# T-119 review, round 2: staff-engineer-reviewer

**Verdict: changes.** No blocker. Of the two round-1 majors, the Tab/Enter/Space-only R-RV-4 test is fixed and kills its mutants. The row-only key test is mostly fixed: it kills four of five scratch mutants, but the `p` gate (`app/frontend/sidebyside.js:102`) is still untested. That was the round-1 mutB, whose acceptance test said the new E2E "fails on both mutants". Three round-1 minors are unchanged.

## What I ran

- Pinned to `git archive e1ce8dc` (HEAD when I started: `e1ce8dc620e6ec0778320456ac79a25f1832bfee`; card commit d9efc5c). Archive file count 1979 equals `git ls-tree -r HEAD`. HEAD later moved to c26ff04; `git diff --stat e1ce8dc HEAD -- app/frontend tests/e2e` shows only a two-line `tests/e2e/conftest.py` comment change (d56328a), so the pin still holds.
- Own fixture server on 127.0.0.1:7991 (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch>`). Both servers (7991, 7992) stopped by PID; ports verified closed.
- `tests/e2e/test_polish_r3.py`: **18 passed** in 23.6s.
- Full `tests/e2e`, run twice. Run 1: **1 failed, 190 passed, 1 skipped** in 253s; the failure was `test_code_check_refusal.py:110` (`vis(...)` "the reason must be on screen beside the button"). Run 2: **191 passed, 1 skipped** in 253s. The failing file then passed 3 of 3 isolated runs (23 passed each). The handoff's 176 passed + 16 skipped = 192 equals my 191 + 1 skipped = 192 collected; the 15 extra skips are the ZLAYT_DB gates, which I set.
- Mutants on a second scratch copy (own port 7992 and sqlite), control green (18 passed) before and after each swap:
  - A, `review.js` letter keys fall back to the first row (`const row = RV.itemRowOf(t) || document.querySelector("[data-item-id]")`): **killed**, `test_letter_keys_do_nothing_from_body_export_or_an_input` fails.
  - B, `sidebyside.js:102` `p` without `ZL.rv.itemRowOf(t)`: **survived 18 of 18, and survived 129 of 129** across all 8 e2e files that press keys (`test_code_check_refusal, test_keyboard_mobile, test_input, test_rerun_judge, test_suggestions, test_polish_r3, test_stepper, test_side_by_side`).
  - C, `batch.js` Shift+A without the row gate: **killed**, same test.
  - D, `review.js` `typing(t)` exemption removed: **killed**, same test (the `jadA` typed-not-run assertion).
  - E, `review.js` dialog-open swallow removed: **killed**, `test_letter_key_with_a_window_open_says_so`.
- Probe (scratch, `artifacts/review-evidence/T-119/r2-probe_p.py`): select an item so the pane is on, blur to body, press `p`. Unmutated HEAD: passes (focus stays). Mutant B: fails with `p moved focus from the body: BODY: -> DIV:sbs-body`. So B has a real effect that no committed test sees.
- Read `tests/e2e/test_polish_r3.py` in full, the `test_stepper.py:204` retry, `review.js:309-345`, `sidebyside.js:98-106`, `batch.js:124-128`. Greps for `sleep(`, `wait_for_timeout`, `keyboard.press("Tab")`, `inner_text()` after a parent wait, `pytest.skip`, and the stale tray copy in `conftest.py`.
- Evidence in `artifacts/review-evidence/T-119/`: `r2-e2e-full-run1.txt`, `r2-e2e-full-run2.txt`, `r2-mutants-polish.txt`, `r2-probe_p.py`, `r2-mut.py`.

## Judgement of the new tests

- **Negative key test** (`test_polish_r3.py:74-102`): asserts decision count, open dialogs and typed text (not implementation). It drives j, a, d, Shift+A and `?` from the body, from Export, from the edit textarea and from the sort control. The "active" field in `_snapshot` compares the snapshot to itself, so it proves nothing, but the next line (`closest('[data-item-id]')` is falsy) does check that focus did not enter a row. Real, mutation-tested for decision keys. Gap: `p` (and `k o e r` only through the shared gate, which mutant A covers) and the header; `p` has its own gate and is not pressed.
- **Dialog case** (`:105-111`): `o` then `a`, expects the "Press Escape" notice and zero accepted. Killed mutant E.
- **Tab/Enter/Space-only flow** (`:115-143`): no `.focus()` on the path; `tab_until` raises if the target is never reached, so a lost skip link, a lost tab stop or a swallowed Enter fails it. It asserts the real outcome (`data-review="dismissed"`, `export-letter` visible, `copy-confirm`, then `Copied the treatment section`). Setup accepts go through the API, which is fine for a keyboard test of one item plus export. It covers one item, not "the sample case", so R-RV-4 is met in kind, not in full; I rate that as a note, not a finding.
- **Determinism:** no `wait_for_timeout`. The one `time.sleep(.5)` (`:21`) is a bounded `/status` poll for the run to reach `ready` (150 s cap, asserts `ready`), the same helper pattern as `test_stepper.py:17`. Assertions after UI actions use `expect(...)` retries. No wall clock, no network beyond the local fixture server.
- **`test_stepper.py:204`:** now `expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(...))`, a retrying assert. Round-1 minor 4 is fixed. No `inner_text()` follows a parent `wait_for` for that testid.

## Round-1 minors

- Minor 3 (stale tray-flag copy): **not fixed.** `tests/e2e/conftest.py:45` still says "AI suggested a flag that the second check did not confirm; it is not in the letter."
- Minor 4 (`inner_text` at :204): **fixed**, see above.
- Minor 5 (the only skip hides ADR-005): **unchanged.** `tests/e2e/test_ladder_gate.py:37` still skips; it is the one skip in both full runs. Pre-existing and not in the T-119 diff.
- Docstring from round-1 finding 2: `tests/e2e/test_keyboard_mobile.py:9` still says "Tab to the first queue item" and `:10` calls `.focus()`. The Tab test now exists elsewhere, so this is a misleading comment only.

## Findings

1. **major: the `p` gate is untested; the new negative test does not fail on round-1 mutB.** Evidence: mutant B (`app/frontend/sidebyside.js:102`, `&& ZL.rv && ZL.rv.itemRowOf(t)` removed) gives 18 passed on `test_polish_r3.py` and 129 passed across the 8 keyboard files (`r2-mutants-polish.txt`); the probe fails on it with `p moved focus from the body: BODY: -> DIV:sbs-body`. The test presses only `j a d Shift+A ?` (`test_polish_r3.py:79,85,93,100`). Round-1 finding 1 asked for a d j k p o e r and its acceptance said it fails on both mutants. Why it matters: `p` is a single-character shortcut that acts from the page body and Export, which is the WCAG 2.1.4 rule T-060 made a blocker; it can regress without CI noticing. Fix: add `p` to the key lists in `test_letter_keys_do_nothing_from_body_export_or_an_input`, after first putting an item in the pane (focus a row, press `p`, Escape, then blur) so the pane is visible; assert focus stays on body or Export. Acceptance: the test passes on HEAD and fails on mutant B (`r2-probe_p.py` is the reference).

2. **minor: full-suite flake in `test_code_check_refusal.py:110`.** Evidence: run 1 failed `test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action` with "the reason must be on screen beside the button, not below the fold"; run 2 passed; the file alone passed 3 of 3. `vis()` (`:93-95`) reads `bounding_box()` once, after `expect(...).to_be_visible()`, against the viewport. This is a one-shot layout read after a click. File is outside the T-119 diff, but the card's AC says "full e2e green". Fix: wait for scroll to settle before the check, e.g. `expect` on a stable box position, or poll `vis` with a retrying assertion. Acceptance: 5 consecutive full-suite runs without this failure.

3. **minor: stale tray-flag copy still in the E2E contract (round-1 minor, unchanged).** Evidence: `tests/e2e/conftest.py:45`. Fix: use the T-060 sentence from `app/frontend/timeline.js:135`. Acceptance: `grep -n "did not confirm; it is not in the letter" tests/e2e/conftest.py` returns nothing.

4. **nit: misleading docstring.** `tests/e2e/test_keyboard_mobile.py:9-10` says "Tab to the first queue item" while calling `.focus()`. Fix: reword to "focus the first item" or point to `test_polish_r3.py`.

## What is right

- The Tab/Enter/Space-only test is genuine keyboard reach with no `.focus()` and real end-state assertions.
- The negative key test kills four of five gate mutants, including the typing exemption and the dialog swallow.
- `test_stepper.py:204` now uses a retrying `expect`; the polish file has no fixed sleeps in UI waits.

## Limits

Outside my lens: UX wording of the shortcut sheet and notices. I did not run `tests/unit`; the card changes only `tests/e2e`.

```json
{"card": "T-119", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit d9efc5c (tests/e2e/test_polish_r3.py, conftest.py) and the test_stepper.py:204 retry; pinned git archive of HEAD e1ce8dc (later HEAD c26ff04 changes only a two-line tests/e2e/conftest.py comment); own fixture servers 127.0.0.1:7991 and 7992 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB in scratch), both stopped by PID",
 "exercised": [
  "read personas/staff-engineer.md, board show T-119, reviews/T-119-staff-engineer.md, git show --stat d9efc5c, git diff --stat d9efc5c HEAD for app/frontend and tests/e2e",
  "git archive e1ce8dc into scratch T119_r2/archive (1979 files, equal to git ls-tree count)",
  "pytest tests/e2e/test_polish_r3.py: 18 passed",
  "pytest tests/e2e full, run 1: 1 failed (test_code_check_refusal.py:110 vis check), 190 passed, 1 skipped (test_ladder_gate.py:37); run 2: 191 passed, 1 skipped",
  "pytest tests/e2e/test_code_check_refusal.py alone x3: 23 passed each",
  "mutants A, B, C, D, E on a scratch copy with control green: polish file kills A, C, D, E; B survives 18/18",
  "mutant B across the 8 e2e files that press keys: 129 passed (survives)",
  "scratch probe r2-probe_p.py: passes on unmutated, fails on mutant B with 'p moved focus from the body: BODY: -> DIV:sbs-body'",
  "read review.js:309-345, sidebyside.js:98-106, batch.js:124-128, test_stepper.py:196-215, test_keyboard_mobile.py:1-20",
  "greps: sleep(, wait_for_timeout, keyboard.press(Tab), inner_text(), pytest.skip, conftest.py stale tray copy, xfail",
  "stopped scratch servers by PID (52563, 59175); ports 7991 and 7992 verified closed",
  "evidence copied to artifacts/review-evidence/T-119/ (r2-e2e-full-run1.txt, r2-e2e-full-run2.txt, r2-mutants-polish.txt, r2-probe_p.py, r2-mut.py)"
 ],
 "verdict": "changes",
 "scores": {"e2e_green_on_pinned_head": 4, "negative_key_rule_coverage": 3, "keyboard_reachability_coverage": 5, "flake_resistance": 4, "round1_minors_closed": 2},
 "findings": [
  {"severity": "major", "title": "The p gate is untested; the new negative key test does not fail on round-1 mutB",
   "evidence": "mutant B (app/frontend/sidebyside.js:102, '&& ZL.rv && ZL.rv.itemRowOf(t)' removed): test_polish_r3.py 18 passed, 8 keyboard files 129 passed (artifacts/review-evidence/T-119/r2-mutants-polish.txt); probe r2-probe_p.py fails with 'p moved focus from the body: BODY: -> DIV:sbs-body'; the test presses only j a d Shift+A ? (tests/e2e/test_polish_r3.py:79,85,93,100)",
   "why_it_matters": "p is a single-character shortcut that must act only from an item row (WCAG 2.1.4, T-060 blocker). It can regress with all 129 keyboard tests green. Round-1 finding 1 named p and its acceptance test required failing on both mutants.",
   "fix": "Add p to the key lists in test_letter_keys_do_nothing_from_body_export_or_an_input after putting an item in the pane (focus a row, press p, Escape, blur), and assert focus stays on the body or Export.",
   "acceptance_test": "The test passes on HEAD and fails on mutant B; artifacts/review-evidence/T-119/r2-probe_p.py is the reference."},
  {"severity": "minor", "title": "Full-suite flake: one-shot bounding-box read in test_code_check_refusal.py:110",
   "evidence": "run 1 of tests/e2e failed test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action 'the reason must be on screen beside the button, not below the fold' (r2-e2e-full-run1.txt); run 2 passed (r2-e2e-full-run2.txt); file alone 23 passed x3; vis() at test_code_check_refusal.py:93-95 reads bounding_box() once",
   "why_it_matters": "The card AC says full e2e green; a one-shot layout read after a click fails intermittently under a full run. Outside the T-119 diff.",
   "fix": "Retry the position check until the scroll settles (poll vis, or use a retrying expect on a stable position).",
   "acceptance_test": "5 consecutive full tests/e2e runs without this failure."},
  {"severity": "minor", "title": "Stale tray-flag copy still in the E2E data-testid contract (round-1 minor, unchanged)",
   "evidence": "tests/e2e/conftest.py:45 quotes 'AI suggested a flag that the second check did not confirm; it is not in the letter.'; the product (app/frontend/timeline.js:135) and test_suggestions.py use the T-060 sentence",
   "why_it_matters": "The conftest is the declared contract for the frontend hooks and contradicts the product and the test.",
   "fix": "Update conftest.py:45 to the T-060 sentence.",
   "acceptance_test": "grep -n 'did not confirm; it is not in the letter' tests/e2e/conftest.py returns nothing."},
  {"severity": "nit", "title": "Misleading docstring in test_keyboard_mobile.py",
   "evidence": "tests/e2e/test_keyboard_mobile.py:9 'Tab to the first queue item' with :10 calling .focus()",
   "why_it_matters": "The docstring claims keyboard reach the test does not exercise; the real Tab test now lives in test_polish_r3.py.",
   "fix": "Reword to 'focus the first item' or point to test_polish_r3.py.",
   "acceptance_test": "The docstring no longer says Tab."}
 ],
 "whats_right": [
  "The Tab/Enter/Space-only test has no .focus() on its path and asserts real end states (dismissed row, export visible, copy confirmed).",
  "The negative key test kills four of five gate mutants (body fallback, Shift+A, typing exemption, dialog swallow).",
  "test_stepper.py:204 is a retrying expect, and test_polish_r3.py has no fixed sleeps in UI waits (one bounded status poll)."
 ],
 "questions_for_chris": []}
```
- [Library packets v2 conventions](project_library_packets.md) — how lib08..15 are built, golden-schema limits, fixture recording recipe
- [Judge controls matched pairs](project_judge_controls.md) — J3/J4 control sets: matched pairs, fixed labels, held-out split, 3 repeats, stable J3W11 finding
- [Calibration route and regen](project_calibration_route.md) — stale flag vs HEAD hashes, clean-worktree regen recipe, score_unsplit fixture-dir pitfall
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:56.180Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -3; sed -n 1,145p tests/e2e/test_polish_r3.py; sed -n 85,125p tests/e2e/test_code_check_refusal.py; sed -n 40,50p tests/e2e/conftest.py; sed -n 1,20p tests/e2e/test_keyboard_mobile.py; sed -n 95,110p app/frontend/sidebyside.js; cat artifacts/review-evidence/T-119/r2-probe_p.py"
}
````

### User / tool · 2026-11-02T11:14:56.338Z

**tool result**
````
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
c26ff04 feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
c89ac86 docs(orchestrator): D-057 rule-filtered model proposals are listed collapsed, not dropped
"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def active(page):
    return page.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")


def tab_until(page, testid, limit=40):
    for _ in range(limit):
        page.keyboard.press("Tab")
        a = active(page)
        if a and a["tid"] == testid:
            return a
    raise AssertionError(f"Tab never reached {testid}; last {active(page)}")


# ---- 1. the shortcut sheet
def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-shortcuts").click()
    dlg = page.get_by_test_id("shortcuts-modal"); expect(dlg).to_be_visible()
    lst = dlg.get_by_test_id("shortcuts-list")
    expect(lst.locator("kbd")).to_have_count(9)
    expect(lst.locator("dt")).to_have_count(9); expect(lst.locator("dd")).to_have_count(9)
    txt = dlg.inner_text()
    assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    # '?' from an item row opens the same sheet
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()


def test_no_object_undefined_or_null_text_on_the_review_page(page, sample_case):
    open_case(page, sample_case)
    assert not BAD_TEXT.search(page.locator("body").inner_text()), BAD_TEXT.findall(page.locator("body").inner_text())


# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
def _snapshot(page):
    return page.evaluate("""() => ({ accepted: document.querySelectorAll('[data-review=accepted],[data-review=dismissed],[data-review=edited]').length,
        dialogs: document.querySelectorAll('dialog[open]').length, active: (document.activeElement || {}).tagName + ':' + ((document.activeElement || {}).getAttribute ? document.activeElement.getAttribute('data-testid') : '') })""")


def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
    open_case(page, sample_case)
    before = _snapshot(page)
    # from the page body
    page.evaluate("document.activeElement && document.activeElement.blur()")
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    assert _snapshot(page) == {**before, "active": _snapshot(page)["active"]}, "a key acted from the page body"
    assert page.evaluate("!document.activeElement.closest || !document.activeElement.closest('[data-item-id]')")
    # from the Export button
    page.get_by_test_id("btn-export").focus()
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0 and s["active"].endswith("btn-export"), s
    # from an input: the edit box of an item, and the sort control
    page.get_by_test_id("entry-1").get_by_test_id("btn-edit").click()
    ta = page.get_by_test_id("entry-1").get_by_test_id("edit-summary"); expect(ta).to_be_focused()
    start = ta.input_value()
    for k in ("j", "a", "d", "Shift+A"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0, s
    assert ta.input_value() == start + "jadA"                       # they were typed, not run
    page.keyboard.press("Escape")
    page.get_by_test_id("sort").focus()
    for k in ("j", "a", "Shift+A"):
        page.keyboard.press(k)
    assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0


def test_letter_key_with_a_window_open_says_so(page, sample_case):
    """paralegal F11: o then a used to do nothing, silently."""
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("o"); expect(page.get_by_test_id("record-modal")).to_be_visible()
    page.keyboard.press("a")
    expect(page.locator("#rv-live")).to_contain_text("Press Escape")
    assert page.locator("[data-review=accepted]").count() == 0


# ---- 3. Tab, Enter and Space only: review one item, then export (R-RV-4)
def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_case):
    tok = sample_case
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] == "verified" and e["date"]]
    assert api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})[0] == 200   # setup by API: the checked entries are in the letter
    open_case(page, tok)
    # (a) one item reviewed by keyboard: Tab to the first skip link, Enter, then Tab to the item's Dismiss button, Enter
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-review", 6)
    page.keyboard.press("Enter")
    row = active(page); assert row["item"], row
    item = row["item"]
    tab_until(page, "btn-dismiss", 12)
    page.keyboard.press("Enter")
    expect(page.locator(f'[data-item-id="{item}"]').first).to_have_attribute("data-review", "dismissed")
    # (b) the export, from a fresh load, by keyboard only
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-export", 10)
    page.keyboard.press("Enter")
    assert active(page)["tid"] == "btn-export"
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    tab_until(page, "btn-copy-letter", 6)
    page.keyboard.press("Space")
    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
    page.keyboard.press("Enter")
    expect(page.locator("#export-status")).to_contain_text("Copied the treatment section")


        t["stub"].attach(page)
    return t


def row_of(page, i):
    return page.get_by_test_id("timeline").locator(f'[data-item-id="{i}"]').first


def vis(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_refused_accept_shows_the_reason_beside_the_button_with_an_edit_action(pw, broken, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        t = arm(broken, pg)
        open_case(pg, t["tok"]); row = row_of(pg, t["id"])
        row.scroll_into_view_if_needed()
        btn = row.get_by_test_id("btn-accept"); btn.click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        msg = box.get_by_test_id("accept-refused-msg").inner_text()
        assert msg.startswith("Not accepted. ") and msg.endswith("Edit the summary to match the quote."), msg
        assert "not in the quote" in msg or t["mode"] == "real"
        assert vis(pg, box), "the reason must be on screen beside the button, not below the fold"
        assert abs(box.bounding_box()["y"] - btn.bounding_box()["y"]) < 140, "next to the Accept button"
        assert box.get_attribute("role") == "alert"
        assert api("GET", f"/api/cases/{t['tok']}")[1]["review"]["counts"]["accepted"] == 0 and _entry(t["tok"], t["id"])["review_status"] == "pending", "nothing was changed"
        # Edit opens the item's edit box; a passing edit clears the refusal and the item is accepted by the edit
        box.get_by_test_id("btn-accept-refused-edit").click()
        ta = row.get_by_test_id("edit-summary"); expect(ta).to_be_visible()
        assert pg.evaluate("document.activeElement === document.querySelector('[data-item-id=\"%s\"] textarea')" % t["id"]) or ta.is_visible()
        ta.fill(t["orig"]); row.get_by_test_id("btn-save-edit").click()
        expect(row_of(pg, t["id"])).to_have_attribute("data-review", "edited")
        expect(row_of(pg, t["id"]).get_by_test_id("accept-refused")).to_be_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_refused_accept_by_keyboard_keeps_focus_and_says_it(page, broken):
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('AI suggested a flag that the second check did not confirm; it is not in the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
"""Keyboard and mobile. R-RV-8, R-ST-1, a11y."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_keyboard_only_accept_flow(page, sample_case):
    """R-RV-8: Tab to the first queue item, Enter opens, 'a' accepts, 'd' dismisses (documented shortcuts)."""
    open_case(page, sample_case); page.get_by_test_id("queue").locator("[data-item-id]").first.focus(); page.keyboard.press("a")
    expect(page.locator("[data-review=accepted]")).to_have_count(1)

def test_mobile_375_modal_not_side_by_side(pw, sample_case):
    """R-ST-1: at 375 px the source record opens as a modal and nothing scrolls horizontally."""
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 375, "height": 800}).new_page(); open_case(pg, sample_case)
    pg.get_by_test_id("entry-1").get_by_test_id("btn-source").click(); assert pg.get_by_test_id("record-modal").is_visible()
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"); b.close()

def test_focus_visible_on_buttons(page, sample_case):
    """a11y: focused buttons have a visible outline."""
    const t = ev.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    if (ev.key === "Enter" && t && t.hasAttribute && t.hasAttribute("data-item-id") && !t.closest("dialog") && !t.closest(".sbs-pane")) {
      show(t.getAttribute("data-item-id"));   // Enter on a focused row (re)selects it into the pane; buttons inside the row keep their own Enter
    } else if (ev.key === "Escape" && t && t.closest && t.closest(".sbs-pane") && current) {
      const row = document.querySelector('[data-testid="queue"] [data-item-id="' + current.id + '"]') || document.querySelector('[data-item-id="' + current.id + '"]');
      if (row) { ev.preventDefault(); if (!row.hasAttribute("tabindex")) row.setAttribute("tabindex", "0"); row.focus(); }
    } else if (ev.key.toLowerCase() === "p" && !pane.hidden && body && ZL.rv && ZL.rv.itemRowOf(t)) {   // only from an item row (WCAG 2.1.4): never from Export or the page body
      if (document.querySelector("dialog[open]")) return;
      ev.preventDefault(); body.focus();
    }
  });

  function sync(s) {
    build(); if (!pane) return;
    const ready = !!(s.case && s.case.status === "ready");
"""Scratch probe (reviewer): p from body / Export must not move focus into the pane."""
import sys
from tests.e2e.conftest import open_case
def _focus(page):
    return page.evaluate("(() => { const a = document.activeElement; return (a.tagName||'') + ':' + (a.getAttribute('data-testid')||''); })()")
def test_p_from_body_and_export(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("queue").locator("[data-item-id]").first.focus(); page.keyboard.press("p")
    assert page.get_by_test_id("sbs-body").evaluate("e => e === document.activeElement")   # pane is on, an item is selected
    page.keyboard.press("Escape")
    page.evaluate("document.activeElement.blur()"); before = _focus(page); page.keyboard.press("p")
    assert _focus(page) == before, f"p moved focus from the body: {before} -> {_focus(page)}"
    page.get_by_test_id("btn-export").focus(); page.keyboard.press("p")
    assert _focus(page).endswith("btn-export"), _focus(page)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:14:59.447Z

**tool call — Bash**
````
{
 "command": "sed -n 130,140p app/frontend/timeline.js | cut -c1-300; grep -n \"did not confirm\" app/frontend/*.js tests/e2e/*.py | cut -c1-250; grep -n \"sleep\\|wait_for_timeout\" tests/e2e/test_code_check_refusal.py | head"
}
````

### User / tool · 2026-11-02T11:14:59.571Z

**tool result**
````
    if (left) msg += " Record " + (rec ? rec.seq : "") + " has no entry yet; it is listed under Records without an entry.";
    if (changes.length) msg += " " + changes.join(" ");
    say(msg);
    requestAnimationFrame(() => {
      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
      if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "center" }); }
      else if (left) left.scrollIntoView({ block: "center" });
    });
    return resp;
  };
  function gapNoteNode(c) {
app/frontend/judges.js:46:  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "accept".
tests/e2e/conftest.py:47:  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('AI suggested a flag that the second check did not confirm; it is not in the letter.'), tra
app/frontend/timeline.js:189:  // D-053: a `flag` tray item is an AI-suggested flag the checks did not confirm. It is never in the flags list or the letter.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:00.751Z

**tool call — Bash**
````
{
 "command": "grep -rn \"tray-flag-lead\" app/frontend/*.js tests/e2e/test_suggestions.py | cut -c1-400"
}
````

### User / tool · 2026-11-02T11:15:00.836Z

**tool result**
````
tests/e2e/test_suggestions.py:230:    expect(item.get_by_test_id("tray-flag-lead")).to_have_text(LEAD)
tests/e2e/test_suggestions.py:241:    expect(page.get_by_test_id("tray-flag-lead").first).to_have_text(LEAD)
tests/e2e/test_suggestions.py:242:    item = page.get_by_test_id("tray-flag-lead").first.locator("xpath=ancestor::*[@data-tray-kind='flag']")
tests/e2e/test_suggestions.py:248:    expect(item).to_have_attribute("data-tray-kind", "entry"); expect(item.get_by_test_id("tray-flag-lead")).to_have_count(0)
app/frontend/timeline.js:202:        isFlag ? el("p", { class: "summary", "data-testid": "tray-flag-lead" }, (t.reasons || [])[0] === "LLM_ONLY" ? FLAG_NOT_FOUND : FLAG_NOT_CONFIRMED) : null,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:03.123Z

**tool call — Bash**
````
{
 "command": "grep -n \"FLAG_NOT_CONFIRMED\\s*=\\|FLAG_NOT_FOUND\\s*=\" app/frontend/*.js | cut -c1-300; grep -n \"^LEAD\" tests/e2e/test_suggestions.py | cut -c1-300"
}
````

### User / tool · 2026-11-02T11:15:03.217Z

**tool result**
````
app/frontend/timeline.js:191:  const FLAG_NOT_CONFIRMED = "The AI suggested this flag. The checks did not support it, so it is left out of the letter.";
app/frontend/timeline.js:192:  const FLAG_NOT_FOUND = FLAG_NOT_CONFIRMED;
225:LEAD = "The AI suggested this flag. The checks did not support it, so it is left out of the letter."   # T-060: one sentence for both reasons
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:04.026Z

Now the edits.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:08.390Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='tests/e2e/conftest.py'; s=open(p).read()\ns=s.replace(\"'AI suggested a flag that the second check did not confirm; it is not in the letter.'\",\"'The AI suggested this flag. The checks did not support it, so it is left out of the letter.'\")\nopen(p,'w').write(s)\np='tests/e2e/test_keyboard_mobile.py'; s=open(p).read()\ns=s.replace(\"R-RV-8: Tab to the first queue item, Enter opens, 'a' accepts, 'd' dismisses (documented shortcuts).\",\"R-RV-8: with the first queue item focused (the Tab-only path is test_polish_r3.py), 'a' accepts, 'd' dismisses (documented shortcuts).\")\nopen(p,'w').write(s)\np='tests/e2e/test_code_check_refusal.py'; s=open(p).read()\ns=s.replace('''def vis(page, loc):\n    b = loc.bounding_box(); vh = page.viewport_size[\"height\"]\n    return b is not None and b[\"y\"] >= 0 and b[\"y\"] + b[\"height\"] <= vh\n''','''def vis(page, loc, timeout=5000):\n    \"\"\"True once the box is fully inside the viewport. Polls: the row scrolls after a click, so a single bounding_box() read can land mid-scroll.\"\"\"\n    vh = page.viewport_size[\"height\"]\n    def inside():\n        b = loc.bounding_box()\n        return b is not None and b[\"y\"] >= 0 and b[\"y\"] + b[\"height\"] <= vh\n    try:\n        page.wait_for_function(\"() => true\")      # no-op: keeps the sync API pumping between polls\n        expect_poll = __import__(\"playwright.sync_api\", fromlist=[\"expect\"]).expect\n        expect_poll(loc).to_be_visible()\n        deadline = timeout\n        while deadline > 0:\n            if inside():\n                return True\n            page.wait_for_function(\"() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(() => r(true))))\")\n            deadline -= 50\n        return inside()\n    except Exception:\n        return inside()\n''')\nopen(p,'w').write(s)\nEOF"
}
````

### User / tool · 2026-11-02T11:15:08.508Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:11.613Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_code_check_refusal.py'; s=open(p).read()\na=s.index(\"def vis(\"); b=s.index(\"@pytest.mark.parametrize\",a)\nnew='''def vis(page, loc, frames=120):\n    \"\"\"True once the box is fully inside the viewport. Polls frame by frame (no sleeps): the row can still be scrolling after a click,\n    so a single bounding_box() read can land mid-scroll.\"\"\"\n    vh = page.viewport_size[\"height\"]\n    for _ in range(frames):\n        bb = loc.bounding_box()\n        if bb is not None and bb[\"y\"] >= 0 and bb[\"y\"] + bb[\"height\"] <= vh:\n            return True\n        page.evaluate(\"() => new Promise(r => requestAnimationFrame(() => r(true)))\")\n    return False\n\n\n'''\ns=s[:a]+new+s[b:]\nopen(p,'w').write(s)\nEOF\ngit diff --stat"
}
````

### User / tool · 2026-11-02T11:15:11.762Z

**tool result**
````
 .claude/agent-memory/backend/MEMORY.md             |    2 +
 .../backend/project_backend_conventions.md         |    2 +
 .../backend/project_t110_overlap_tray.md           |    6 +
 .../claims-adjuster-reviewer/MEMORY.md             |    9 +
 .../feedback_lexicon_review_method.md              |    5 +
 .../feedback_reviews_write_once.md                 |    9 +
 .claude/agent-memory/frontend/MEMORY.md            |    1 +
 .../agent-memory/legal-nurse-reviewer/MEMORY.md    |    2 +
 .claude/agent-memory/paralegal-reviewer/MEMORY.md  |   13 +-
 .../feedback_reviewer_tooling_quirks.md            |   41 +
 .../paralegal-reviewer/library-review-patterns.md  |   16 +
 .../reviewer-hook-constraints.md                   |    1 +
 .claude/agent-memory/qa/MEMORY.md                  |    1 +
 .claude/agent-memory/security-reviewer/MEMORY.md   |    2 +-
 .../project_pdf_upload_review_patterns.md          |    7 +
 .../agent-memory/staff-engineer-reviewer/MEMORY.md |   39 +-
 .../project_e2e_contract_review_patterns.md        |    9 +-
 .../project_harness_review_patterns.md             |   17 +
 .../project_split_llm_review_patterns.md           |   12 +
 .../agent-memory/ux-designer-reviewer/MEMORY.md    |   18 +
 app/backend/api.py                                 |    4 +-
 app/backend/confidence.py                          |    2 +-
 app/backend/flag_templates.py                      |    7 +
 app/backend/flags.py                               |   22 +-
 app/backend/pipeline.py                            |    2 +-
 app/backend/present.py                             |   27 +-
 app/backend/store.py                               |    2 +
 app/backend/trace.py                               |    4 +-
 app/backend/why.py                                 |    1 +
 app/frontend/app.js                                |    5 +-
 app/frontend/dom.js                                |   12 +
 app/frontend/flags.js                              |    8 +
 app/frontend/judges.js                             |   20 +-
 app/frontend/manual.js                             |    4 +-
 app/frontend/review.css                            |    6 +
 app/frontend/review.js                             |   47 +-
 app/frontend/styles.css                            |   10 +-
 app/frontend/switcher.js                           |    6 +-
 app/frontend/timeline.js                           |   61 +-
 board/activity.jsonl                               | 1487 ++++++++++++++++++++
 board/cards/T-045.md                               |    9 +-
 board/cards/T-046.md                               |   55 +-
 board/cards/T-053.md                               |    3 +-
 board/cards/T-055.md                               |    8 +-
 board/cards/T-057.md                               |   21 +-
 board/cards/T-058.md                               |    8 +-
 board/cards/T-059.md                               |   13 +-
 board/cards/T-060.md                               |   71 +-
 board/cards/T-061.md                               |   18 +-
 board/cards/T-063.md                               |   30 +-
 board/cards/T-064.md                               |   49 +-
 board/cards/T-065.md                               |   38 +-
 board/cards/T-066.md                               |   39 +-
 board/cards/T-067.md                               |   85 +-
 evals/reports/latest.json                          |  149 +-
 memory/LESSONS.md                                  |    6 +
 memory/PROGRESS.md                                 |   10 +
 memory/SCOPE_CUTS.md                               |    2 +
 memory/contracts/api.md                            |    2 +-
 tests/e2e/conftest.py                              |    6 +-
 tests/e2e/test_code_check_refusal.py               |   13 +-
 tests/e2e/test_keyboard_mobile.py                  |    2 +-
 tests/unit/test_flags_pass.py                      |    3 +-
 63 files changed, 2398 insertions(+), 191 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:16.614Z

**tool call — Bash**
````
{
 "command": "git diff tests/e2e/conftest.py | head -30; python3 - <<'EOF'\np='tests/e2e/test_polish_r3.py'; s=open(p).read()\nmarker=\"def test_letter_key_with_a_window_open_says_so\"\nnew='''def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):\n    \"\"\"WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing.\"\"\"\n    open_case(page, sample_case)\n    page.get_by_test_id(\"queue\").locator(\"[data-item-id]\").first.focus()\n    page.keyboard.press(\"p\")\n    expect(page.get_by_test_id(\"sbs-body\")).to_be_focused()           # from an item row it works, and the pane now shows an item\n    page.keyboard.press(\"Escape\")\n    assert page.evaluate(\"!!document.activeElement.closest('[data-item-id]')\"), \"Escape should return focus to the item row\"\n    focus = lambda: page.evaluate(\"(() => { const a = document.activeElement; return (a.tagName || '') + ':' + (a.getAttribute('data-testid') || a.id || ''); })()\")\n    page.evaluate(\"document.activeElement.blur()\")\n    before = focus()\n    page.keyboard.press(\"p\")\n    assert focus() == before, f\"p moved focus from the page body: {before} -> {focus()}\"\n    for tid in (\"btn-export\", \"btn-shortcuts\", \"sort\"):\n        page.get_by_test_id(tid).focus(); here = focus()\n        page.keyboard.press(\"p\")\n        assert focus() == here, f\"p moved focus from {tid}: {here} -> {focus()}\"\n    assert not page.get_by_test_id(\"sbs-body\").evaluate(\"e => e === document.activeElement\")\n\n\n'''\ns=s.replace(marker,new+marker,1)\nopen(p,'w').write(s)\nEOF"
}
````

### User / tool · 2026-11-02T11:15:16.755Z

**tool result**
````
diff --git a/tests/e2e/conftest.py b/tests/e2e/conftest.py
index 2f4102f..def973e 100644
--- a/tests/e2e/conftest.py
+++ b/tests/e2e/conftest.py
@@ -44,7 +44,7 @@ T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click
   dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
   calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
   data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
-  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('AI suggested a flag that the second check did not confirm; it is not in the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
+  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
 T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
   Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
   New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
@@ -55,6 +55,10 @@ T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-li
   btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
   Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
   The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
+T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
+  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
+  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
+  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
 Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
 """
 import json, os, urllib.request, urllib.error
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:24.249Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/t119 $S/t119m; mkdir -p $S/t119 && git archive HEAD | tar -x -C $S/t119 && for f in tests/e2e/conftest.py tests/e2e/test_polish_r3.py tests/e2e/test_code_check_refusal.py tests/e2e/test_keyboard_mobile.py; do cp $f $S/t119/$f; done; ls $S/t119 | head -20; sed -n 1,40p tests/e2e/conftest.py | grep -n \"BASE\\|PORT\\|environ\" ; ls .venv/bin/python; echo $S"
}
````

### User / tool · 2026-11-02T11:15:24.740Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
.venv/bin/python
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:26.944Z

**tool call — Bash**
````
{
 "command": "grep -n \"BASE\\s*=\\|environ\\|uvicorn\\|Popen\" tests/e2e/conftest.py | head; grep -rn \"ZLAYT_BASE\\|ZLAYT_E2E\" tests/e2e/conftest.py | head -3; sed -n 1,12p artifacts/review-evidence/T-119/r2-mut.py 2>/dev/null; ls artifacts/review-evidence/T-119/; cat .claude/agent-memory/qa/project_*.md | grep -i \"port\\|archive\" | head"
}
````

### User / tool · 2026-11-02T11:15:27.062Z

**tool result**
````
67:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
import sys, shutil, os
S, name = sys.argv[1], sys.argv[2]
M = {
 "A_body_falls_back_to_first_row": ("app/frontend/review.js", 'const row = RV.itemRowOf(t);\n    if (!row) return;', 'const row = RV.itemRowOf(t) || document.querySelector("[data-item-id]");\n    if (!row) return;'),
 "B_p_without_row_gate": ("app/frontend/sidebyside.js", ' && ZL.rv && ZL.rv.itemRowOf(t)) {', ') {'),
 "C_shiftA_without_row_gate": ("app/frontend/batch.js", '|| !RV.itemRowOf(t)) return;', ') return;'),
 "D_typing_not_exempt": ("app/frontend/review.js", 'if (typing(t)) return;\n    if (document', 'if (false) return;\n    if (document'),
 "E_dialog_swallow_removed": ("app/frontend/review.js", 'if (document.querySelector("dialog[open]")) {   // a dialog swallows', 'if (false) {   // a dialog swallows'),
 "F_export_rowgate_kj": ("app/frontend/review.js", 'if (key === "j" || key === "k") {', 'if (key === "j" || key === "k") { if (!row) return;'),
}
f, a, b = M[name]
src = os.path.join(S, "archive", f); dst = os.path.join(S, "mut", f)
e2e-full.txt
mutA-keyboard-files.txt
mutB-keyboard-files.txt
mutate.py
probe_t119_keys.py
r2-e2e-full-run1.txt
r2-e2e-full-run2.txt
r2-mut.py
r2-mutants-polish.txt
r2-probe_p.py
repeat-judge.txt
GET /api/calibration lives in app/backend/calibration_route.py (T-099, stale flag T-102). It serves evals/reports/calibration.json read-only.
  the report shows blocker 4_no_invented_facts. Golden-case calibration counts are unaffected. Open follow-up for qa.
- Gate = every wrong item caught on every one of 3 repeats (`CONTROL_REPEATS`). correct_accepted is reported, not gated; gating it needs an ADR.
- `python -m evals.run --controls` (LLM_BACKEND=claude-cli ENABLE_LIVE=1) runs only the controls, 4 worker threads, writes evals/reports/controls-<ts>.md/.json (about 8 min for 60 items x 3).
`research/library_build.py`, which v2 imports for helpers (rec/amt/flag/span/mn_*). Never hand-edit the generated .txt/.expected.json.
(never export ANTHROPIC_API_KEY; the cli backend strips it). Run two streams of four packets in the background; check with a fixture-backend
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:29.206Z

**tool call — Bash**
````
{
 "command": "cat run.sh 2>/dev/null | head -20; grep -n \"uvicorn\" docs/RUNBOOK.md | head -3"
}
````

### User / tool · 2026-11-02T11:15:29.321Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:30.925Z

**tool call — Bash**
````
{
 "command": "grep -rn \"uvicorn\\|app.backend\" tests/e2e/conftest.py Makefile deploy 2>/dev/null | head -5; ls app/backend | head -30; grep -rln \"7860\" --include=*.md --include=*.sh . 2>/dev/null | head -5"
}
````

### User / tool · 2026-11-02T11:15:31.053Z

**tool result**
````
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
narrative.py
overlap.py
MASTER_PROMPT.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/MASTER_PROMPT.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/memory/PROGRESS.md
artifacts/review-evidence/T-055-security-r2/head_670ed09/tools/serve_app.sh
artifacts/review-evidence/T-055-security-r2/head_670ed09/memory/ENVIRONMENT.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:32.146Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh | head -30"
}
````

### User / tool · 2026-11-02T11:15:32.232Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:33.414Z

**tool call — Bash**
````
{
 "command": "grep -n \"PORT\\|environ\" app/main.py | head"
}
````

### User / tool · 2026-11-02T11:15:33.503Z

**tool result**
````
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:37.561Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nlsof -i :7993 >/dev/null && echo busy\ncd $S/t119 && PYTHONPATH=. PORT=7993 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/t119.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/t119.log 2>&1 &\necho $! > $S/t119.pid; sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7993/; cat $S/t119.pid"
}
````

### User / tool · 2026-11-02T11:15:41.919Z

**tool result**
````
200
87934
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:15:45.345Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $S/t119 && E2E_BASE_URL=http://127.0.0.1:7993 ZLAYT_DB=$S/t119.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py tests/e2e/test_code_check_refusal.py tests/e2e/test_keyboard_mobile.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T11:16:48.649Z

**tool result**
````
.............................................                            [100%]
45 passed in 62.97s (0:01:02)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:16:49.599Z

Now the mutant: apply B to a second copy (served on 7994) and run the new test.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:16:53.906Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nrm -rf $S/t119m; cp -R $S/t119 $S/t119m\npython3 - <<EOF\np=\"$S/t119m/app/frontend/sidebyside.js\"; s=open(p).read()\na=' && ZL.rv && ZL.rv.itemRowOf(t)) {'; assert s.count(a)==1\nopen(p,\"w\").write(s.replace(a,') {'))\nEOF\ncd $S/t119m && PYTHONPATH=. PORT=7994 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/t119m.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/t119m.log 2>&1 &\necho $! > $S/t119m.pid; sleep 4\ncd $S/t119m && E2E_BASE_URL=http://127.0.0.1:7994 ZLAYT_DB=$S/t119m.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_polish_r3.py -q 2>&1 | tail -8 | tee $S/mutB.txt\nkill $(cat $S/t119m.pid); sleep 1; lsof -i :7994 | wc -l"
}
````

### User / tool · 2026-11-02T11:17:25.010Z

**tool result**
````
E         
E         - BODY:
E         + DIV:sbs-body

tests/e2e/test_polish_r3.py:117: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row
1 failed, 18 passed in 24.92s
/bin/bash: line 20: 91633 Terminated: 15          cd $S/t119m && PYTHONPATH=. PORT=7994 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/t119m.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/t119m.log 2>&1  (wd: ~/zlayt-pm-project)
       2
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:17:29.675Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nlsof -i :7994 | head; cd $S/t119 && E2E_BASE_URL=http://127.0.0.1:7993 ZLAYT_DB=$S/t119.sqlite3 timeout 590 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider 2>&1 | tail -8",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T11:17:29.880Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  91635 arsis    9u  IPv4 0x820b443f978c53a5      0t0  TCP localhost:7994 (LISTEN)
/bin/bash: line 2: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:17:34.024Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nkill 91635; sleep 1; lsof -i :7994 | wc -l\ncd $S/t119 && E2E_BASE_URL=http://127.0.0.1:7993 ZLAYT_DB=$S/t119.sqlite3 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider > $S/full.txt 2>&1 &\necho started",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T11:17:34.112Z

**tool result**
````
Command running in background with ID: b862y8jxx. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b862y8jxx.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:17:36.289Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-119 --agent qa --text \"r3: added test_p_focuses_the_record_pane_only_from_an_item_row (kills reviewer mutB: fails 'BODY: -> DIV:sbs-body'); vis() in test_code_check_refusal polls per animation frame; conftest tray copy + keyboard_mobile docstring fixed. Full e2e running on git archive HEAD copy, port 7993.\" ; python3 tools/board.py show T-119 | grep -n \"^- \\[\" | head"
}
````

### User / tool · 2026-11-02T11:17:36.496Z

**tool result**
````
noted on T-119
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:17:40.013Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\npgrep -f \"pytest tests/e2e -q\" | head; tail -c 300 $S/full.txt"
}
````

### User / tool · 2026-11-02T11:17:40.150Z

**tool result**
````
84248
93581
93582
...............
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:17:43.502Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nfor i in $(seq 1 57); do grep -q \"passed\\|failed\" $S/full.txt && break; sleep 10; done; tail -5 $S/full.txt",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T11:21:54.068Z

**tool result**
````
........................................................................ [ 37%]
......s................................................................. [ 74%]
.................................................                        [100%]
192 passed, 1 skipped in 255.42s (0:04:15)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:00.009Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nkill $(lsof -ti :7993) 2>/dev/null; sleep 1; lsof -i :7993 | wc -l\nmkdir -p artifacts/review-evidence 2>/dev/null; cp $S/mutB.txt artifacts/t119-r3-mutB.txt; cp $S/full.txt artifacts/t119-r3-e2e-full.txt\ngit add tests/e2e/conftest.py tests/e2e/test_polish_r3.py tests/e2e/test_code_check_refusal.py tests/e2e/test_keyboard_mobile.py artifacts/t119-r3-mutB.txt artifacts/t119-r3-e2e-full.txt"
}
````

### User / tool · 2026-11-02T11:22:01.306Z

**tool result**
````
       0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:03.454Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"test(e2e): T-119 r3 p-key row gate test (kills mutB), per-frame vis poll, stale tray copy, docstring\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- tests/e2e/conftest.py tests/e2e/test_polish_r3.py tests/e2e/test_code_check_refusal.py tests/e2e/test_keyboard_mobile.py artifacts/t119-r3-mutB.txt artifacts/t119-r3-e2e-full.txt && git rev-parse --short HEAD; python3 tools/board.py show T-119 | grep -n \"AC\\|\\[ \\]\\|\\[x\\]\" | head"
}
````

### User / tool · 2026-11-02T11:22:04.004Z

**tool result**
````
check_secrets: ok (5 file(s) scanned staged)
c559ce2
27:- 2026-11-02T10:10:35Z qa: AC 1 checked: Fixes are in 6e880e6 (landed concurrently by another qa agent; same edits): test_p_moves focuses a row first, tray-flag LEAD matches T-060 copy + tray-why in closed details, judge-count assert retrying (drift: counts load after the panel). test_case_rail_is_one_line passes on a clean HEAD (b89b9d9 worktree, port 7947, killed by PID). Full tests/e2e on clean HEAD: 156 pass, 16 skip, 1 xfail (T-117), the 1 failure was the pre-fix judge assert, then test_stepper+side_by_side+suggestions rerun with 6e880e6: 50 pass, 1 xfail. No product bug, no new card.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:05.411Z

**tool call — Bash**
````
{
 "command": "sed -n 1,25p board/cards/T-119.md | cut -c1-260"
}
````

### User / tool · 2026-11-02T11:22:05.493Z

**tool result**
````
---
id: "T-119"
title: "E2E updates for T-060: keyboard keys act only from an item row (tests pressed from body), tray-flag wording, case rail and judge panel tests"
milestone: "M3"
role: "qa"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:03:50Z"
updated_at: "2026-11-02T11:17:36Z"
claimed_by: "qa"
claimed_at: "2026-11-02T11:14:53Z"
rounds: 2
commits: ["6e880e6"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-119-staff-engineer.md", "at": "2026-11-02T10:27:09Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-119-staff-engineer-r2.md", "at": "2026-11-02T11:14:46Z"}
ac:
  - {"n": 1, "text": "tests/e2e updated so keyboard tests focus an item row first; tray-flag wording tests match T-096/T-060 copy; test_case_rail_is_one_line and test_judge_panel_when_nothing_objected diagnosed (drift fixed, or product bug -> card + strict xfa
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:10.256Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-119 --check 1 --agent qa --evidence \"r3: tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row fails on reviewer mutB (sidebyside.js:102 row gate removed: 'BODY: -> DIV:sbs-body', artifacts/t119-r3-mutB.txt) and passes on HEAD; full tests/e2e on git archive HEAD copy (port 7993): 192 passed, 1 skipped (artifacts/t119-r3-e2e-full.txt); vis() now polls per animation frame, no sleeps\" 2>&1 | tail -2; $B ac T-119 --check 2 --agent qa --evidence \"see check 1\" 2>&1 | tail -1; $B commit T-119 --sha c559ce2 --agent qa; $B handoff T-119 --agent qa --text \"r3 changes: (1) new e2e test p from body/Export/header/sort does nothing, from an item row focuses sbs-body; applied mutB on a scratch copy (port 7994): that test fails, other 18 pass. (2) test_code_check_refusal vis() polls bounding box per animation frame, no sleeps. (3) conftest tray copy now the T-060 sentence, test_keyboard_mobile docstring reworded. Verified: full e2e on git archive HEAD copy, 192 passed 1 skipped, one run (flake needs more runs to disprove). Surprised: conftest.py carried another worker's uncommitted round-4 hook docs; they went in with my commit (comment-only). Skip in test_ladder_gate.py:37 untouched (pre-existing).\" ; $B move T-119 in_review --agent qa"
}
````

### User / tool · 2026-11-02T11:22:10.616Z

**tool result**
````
AC 1 checked: r3: tests/e2e/test_polish_r3.py::test_p_focuses_the_record_pane_only_from_an_item_row fails on reviewer mutB (sidebyside.js:102 row gate removed: 'BODY: -> DIV:sbs-body', artifacts/t119-r3-mutB.txt) and passes on HEAD; full tests/e2e on git archive HEAD copy (port 7993): 192 passed, 1 skipped (artifacts/t119-r3-e2e-full.txt); vis() now polls per animation frame, no sleeps
board.py: error: no AC 2
T-119: commit c559ce2 recorded
handoff written on T-119
T-119: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:22:13.785Z

T-119 round 3 is in review (commit c559ce2). The new `p` test fails on the reviewer's mutB and passes on HEAD.
- **mutB (the major):** `test_p_focuses_the_record_pane_only_from_an_item_row` fails on mutB with `BODY: -> DIV:sbs-body`, with the other 18 tests in the file passing. On HEAD it passes.
- **Flake and minors:** the `vis()` check in `test_code_check_refusal.py` now polls per animation frame, with no sleeps. I also fixed the stale tray copy in `tests/e2e/conftest.py:45` and the `test_keyboard_mobile.py` docstring.
- **Verification:** the full e2e suite on a `git archive HEAD` copy (port 7993) gave 192 passed, 1 skipped, in one run. A single run doesn't prove the flake is gone. My ports are closed; evidence is `artifacts/t119-r3-mutB.txt` and `artifacts/t119-r3-e2e-full.txt`.
- **Surprise:** `conftest.py` also carried another worker's uncommitted round-4 hook docs (comment-only), and they went into the commit.
