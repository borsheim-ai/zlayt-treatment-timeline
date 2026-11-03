# Subagent: Frontend: T-136 edit_to_check (Frontend: T-136 edit_to_check)

Source: `agent-a6f5ccf1af4f0a80f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T12:32:07.757Z

You are the frontend worker in /Users/arsis/zlayt-pm-project. Claim T-136 with `python3 tools/board.py claim T-136 --agent frontend`.

T-134 (backend, commit 5fb338d) now exposes `item.edit_to_check`, `review.counts.edit_to_check` and the gate warning EDIT_NOT_CONFIRMED; see memory/contracts/api.md. ZL.editToCheck currently looks only at summary edits. Switch the UI to `item.edit_to_check` so that an excerpt-only edit made with the quote picker shows as open, with the "I compared it with the quote" Accept. The header, strip and copy-confirm counts must use `review.counts.edit_to_check`. Show the gate warning in the export stepper with its plain reason.

Write the e2e tests first. Run e2e on a clean worktree on your own port, then the unit suite. Commit with a pathspec: run `git add <paths>`, then `git commit -m msg -- <paths>` as a separate command. Check the AC, write the handoff, move the card to in_review, and restart the shared app with tools/serve_app.sh.

Never kill ports 7860, 8787 or 4173; stop only your own PIDs. Reply in 3 lines.

### User / tool · 2026-11-02T12:32:07.762Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:15.186Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-136 --agent frontend && python3 tools/board.py show T-136 && cat .claude/agent-memory/frontend/project_t060_polish.md | head -60"
}
````

### User / tool · 2026-11-02T12:32:15.374Z

**tool result**
````
T-136 claimed by frontend
---
id: "T-136"
title: "UI: read item.edit_to_check (not just summary edits) so a quote-picker edit held out of the letter offers 'I compared it with the quote' (T-134 follow-up)"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T12:31:58Z"
updated_at: "2026-11-02T12:32:15Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T12:32:15Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "an excerpt-only edit shows as open with the compare-and-accept control; header/strip counts include review.counts.edit_to_check; e2e test", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T12:32:15Z frontend: claimed

## Handoff (filled when moving to in_review)

---
name: t060-enterprise-polish
description: T-060 tokens, keyboard scope, compact-row layout, checks card, decided-row buttons, and the pitfalls hit in rounds 2-3
metadata:
  type: project
---
**Tokens:** `app/frontend/tokens.css` is the only place for colours/sizes/radii/shadows (7 font sizes in rem, 2 radii 4/6, light+dark+data-theme). Other CSS files only read tokens. One button system: `.btn` (+ `--primary|--ghost|--link|--sm`); status chips `.chip--ok|warn|bad|info|muted` + `data-icon`. Audit recipe: computed font-size/contrast census (text nodes, effective background, both themes); expect 6 sizes and 0 nodes under 4.5:1 (round 3: 0 in both themes on sample and lib09).
**Keyboard (WCAG 2.1.4):** single keys act only when focus is inside a `[data-item-id]` row outside dialogs/sbs-pane (`RV.itemRowOf`). j/k = DOM order, a/d advance via `RV.nextPendingAfter` (needs-review entry in the queue first, then any needs-review, then any open). Shift+A: batch.js `batch-confirm`; review.js ignores shifted letters. A letter key with a dialog open says "Press Escape" (live region). Skip links = app.js SKIPS, hrefs point at real elements (TARGETS adds ids), re-rendered on `zl:panels`. After a case opens, `resetTabStart` focuses `#skip-nav` (tabindex -1) so one Tab reaches the first skip link.
**Compact row (round 3):** `.entry[data-entry-id]` is a 2-column grid: head (date, provider, Rec, reason with ellipsis, chips) / summary (clamp 3) beside excerpt (clamp 2) / decision buttons left + links right. `.rv-controls` is `display: contents` inside rows. `More`/`Less` (`entry-toggle`) opens a row (`openRows` Set in timeline.js survives repaints). Decided rows clamp to 1 line. Tray cards and date-to-confirm cards (no data-entry-id) keep the old single column. Row-actions are moved after the controls in the DOM so Tab order = screen order.
**Decided buttons:** primary only when `pending`; accepted -> "Accepted" (`rv-decided`, still enabled, no-op that says so, because e2e `.all()` loops click every btn-accept); dismissed -> "Dismissed" muted; reset reads "Undo". Keep `btn-accept`/`btn-dismiss`/`btn-reset` testids on every row.
**Checks card:** timeline.js wraps case-stepper + judge-panel in `.checks` (one border, dividers); calibration-line sits below the queue and is NOT collapsed (e2e asserts it visible).
**Pitfalls:** `el.append(cond ? node : null)` prints "null": always `.filter(Boolean)`; `el()` now flattens any nesting (`kids.flat(Infinity)`), the shortcut sheet bug was a nested array. A class named `rv-edit` is BOTH the edit button and the edit form: always write `form.rv-edit` / `form.rv-reason` in CSS (a form margin rule added 16px to the button row). No row height may depend on focus. entry-date text must stay ISO. Letter/notes text is built by the server and shown verbatim: letter layout changes (T-121) are backend. Sandbox/hook: no `$VAR` in command position, no `rm -rf`, no `sleep` chains; commit with `git commit -F file -- <paths>` and `git add` in its own command; `git add -N` is refused.
**Dev/test recipe:** clean worktree of HEAD (`git worktree add --detach <dir> HEAD`), server `PORT=.. ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch> python -m app.main`, run `E2E_BASE_URL=http://localhost:PORT .venv/bin/python -m pytest tests/e2e`, kill by PID. A worktree with uncommitted backend edits from other agents shows false e2e failures (export 422, judge-panel) that pass on a clean HEAD.
**Round 4 (e293daa):** `ZL.niceName` (dom.js) gives library cases plain titles (display only). Gap-change line: timeline.js `gapChangeFor` (localStorage `zlayt.gapchg.<token>`, prefers `flag.gap_change` once backend T-127 sends it), shown by flags.js on the gap card. Dismissed entries render in `details.dismissed-group` under the queue; `ZL.dismissedOpen` opens it for the entry just dismissed (e2e tests that dismiss then click Undo rely on that). `RV.asTyped` shows refused figures as typed ($9,000). Edit re-check: `rechecks[id]` in review.js, `edit-recheck-hint` / `edit-recheck-note`. Pitfalls: a `const` used before its declaration in a row builder throws and silently empties the whole panel (node --check will not catch TDZ; run one e2e after every edit to judges/flags/timeline); the e2e hook contract unit test (`tests/unit/test_e2e_contract.py`) needs every new test id and data-* attribute declared in the conftest docstring; `aria-label` on a toggle must start with its visible word.
**Round 5 (b612176, T-131):** one definition of "open": `ZL.undecided` / `ZL.needsReview` / `ZL.editToCheck` (dom.js); `ZL.progressOf` (app.js) feeds the header, the strip's `need-review-count` and the Timeline chip, so all three are one number. A reworded entry still marked Needs review is open (row has `data-edit-check`, Accept reads "I compared it with the quote" and sends a normal accept); the backend still exports it (D-045b), so the UI names it in copy-confirm and the backend half is card T-134. A dismissed item keeps only Dismissed / Undo / Audit and no state chip; a/d/e say "press r or Undo first". After a/d focus uses `RV.planAdvance` (the list = `[data-group]` flag sections and amount tables, `queue`, `dates-to-confirm`) and never leaves the list; Start review is the only cross-list jump. Rows show `firstSentence(why)` (tooltip = full why), clamped to 2 lines at 390 px or the 420 px row-height test fails. Row dates are `<time datetime>` with `data-testid=entry-date` (tests read `datetime`). `tray_filtered` renders collapsed with no `data-item-id`. Export has a `letter-style` radio group (api.exportCase(token, style)). Test recipe: e2e needs `page.reload()`, not `open_case`, after changing a case over the API (same hash URL does not refetch). Pitfall: `const toCheck` must be declared before `VARIANT` in RV.controls (TDZ).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:16.066Z

**tool call — Bash**
````
{
 "command": "grep -n \"edit_to_check\\|EDIT_NOT_CONFIRMED\" -r memory/contracts/api.md app/frontend | head -50; git status --short | head; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T12:32:16.201Z

**tool result**
````
memory/contracts/api.md:355:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
memory/contracts/api.md:356:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
memory/contracts/api.md:358:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
memory/contracts/api.md:360:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
5fb338d fix(backend): T-134 an edit still Needs review is open: out of the letter, not accepted, gate warns EDIT_NOT_CONFIRMED, notes say second check not available
f939ccb fix(lexicon): T-133 r2 history_significant_for never fires on HPI headers or narratives; deny sourced from pyConText
425095f docs(architect): T-109 r3 ADR-020 item 2 cite _model_conflicts at flags.py:185-209
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:19.507Z

**tool call — Bash**
````
{
 "command": "grep -rn \"editToCheck\\|edit-check\\|edit_to_check\\|editCheck\\|counts.edited\\|edit-recheck\" app/frontend/*.js app/frontend/**/*.js 2>/dev/null | grep -v \"^app/frontend/vendor\" | head -50; ls app/frontend tests/e2e | head -80; sed -n 350,362p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T12:32:19.605Z

**tool result**
````
app/frontend/app.js:23:    return { total: all.length, decided: all.length - open.length, left: open.length, needs: open.filter((i) => i.state === "needs_review").length, edits: all.filter(ZL.editToCheck).length };
app/frontend/export.js:28:    const edits = (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length;   // T-060 r5 (paralegal M2): her reworded entries that are still marked Needs review
app/frontend/export.js:31:  const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length : 0; };
app/frontend/dom.js:47:  ZL.undecided = (i) => { const rs = (i && i.review_status) || "pending"; return rs === "pending" || ZL.editToCheck(i); };
app/frontend/dom.js:49:  ZL.editToCheck = (i) => !!i && i.review_status === "edited" && i.state === "needs_review" && !!i.edited && i.edited.summary != null;   // a reworded entry; a flag's own note is not "wording"
app/frontend/review.js:97:  const decidable = (n) => { const rs = n.getAttribute("data-review"); return (rs === "pending" || (rs === "edited" && n.hasAttribute("data-edit-check"))) && n.getAttribute("data-state") !== "rejected" && !n.hasAttribute("data-tray-kind"); };
app/frontend/review.js:278:    const toCheck = ZL.editToCheck(item);
app/frontend/review.js:299:    if (toCheck && !rechecks[id]) root.append(el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, "Still marked Needs review. Compare your wording with the quote, then press the button to say you did. Until then it counts as open."));
app/frontend/review.js:300:    if (rechecks[id] && st === "edited") root.append(el("p", { class: "rv-recheck", "data-testid": "edit-recheck-note" }, rechecks[id]));
app/frontend/review.js:325:        isFlag ? null : el("p", { class: "rv-help rv-recheck-hint", "data-testid": "edit-recheck-hint" }, "When you save, the code checks every number, date and negation in your wording against the quote, then a second AI check reads it. Nothing is added to the letter until it passes."),
app/frontend/review.js:422:      if (ZL.editToCheck(entry)) rowEl.setAttribute("data-edit-check", ""); else rowEl.removeAttribute("data-edit-check");
app/frontend/timeline.js:264:    const eEntries = c.entries.filter((e) => open(e) && !dateless.has(e.id)), eEdits = eEntries.filter(ZL.editToCheck).length;
app/frontend:
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
suggestions.js
switcher.js
timeline.js
tokens.css

tests/e2e:
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charges.py
test_code_check_refusal.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_polish_r3.py
test_polish_r4.py
test_polish_r5.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
```
The frontend does not need to refetch the case.

**An edit that is still `needs_review` is not decided (T-134; D-045b, D-051; paralegal pass 4 M2).** Saving the edit stays as above (`review_status: "edited"`, `state: "needs_review"`), but until the paralegal says she compared it with the quote it is **open**, one rule in all places:
- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code checks (D-051): if the current wording fails any of them, `422 CODE_CHECK_FAILED` and nothing is written.
- Export: the entry is **not in the letter**, not in `items.entries`, not counted in `counts.entries` or `provenance.edited_count`; it counts in `excluded.pending` and in `excluded.edit_not_confirmed` (subset of pending), and in the notes' "Items not reviewed: N". It does not block export (it is not in the letter, as with a pending item, D-045(a)), unless nothing else is accepted (`NOTHING_ACCEPTED`).
- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
- Internal notes: EDITED ITEMS lists it with "(edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter (accept it to put it there))" (the reason sentence follows the item's reasons: `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, ...), PENDING ITEMS NOT INCLUDED lists it with the same phrase, and RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote". After she accepts, EDITED ITEMS keeps the reason: "(accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE))". The notes never say she accepted an edit she has not accepted.
- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.

## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:22.633Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 10,40p app.js; sed -n 15,60p export.js; sed -n 255,275p timeline.js; sed -n 40,52p dom.js; grep -n \"counts\" *.js | grep -v \"^mock\" | head -30; grep -n \"edit_to_check\\|edit_not_confirmed\\|EDIT_NOT\" mock*.js | head; grep -rn \"JUDGE_NOT_RUN\\|warnings\" stepper.js export.js | head -30"
}
````

### User / tool · 2026-11-02T12:32:22.755Z

**tool result**
````
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? (h.fixture_set === "recorded" ? "cached demo (recorded responses)" : "cached demo (curated responses)") : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : ""; // D-029: the demo replays the curated fixture set; label says so
    badge.hidden = !h;
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  // ---- case header (sticky): case name, "n of N decided", Export. The numbers are counts of what the API sent; nothing is computed beyond counting.
  const itemsOf = (c) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).filter((i) => i.state !== "rejected");
  // T-060 r5: "decided" means she has nothing left to do on the item. A dismissed item is decided. An edited item that is still marked Needs review is NOT: it is counted as an
  // edit to check. One need-review count (`needs`) is used by the header, the Open-decisions strip and the Timeline chip, and it falls when an item is decided or dismissed.
  ZL.progressOf = function (c) {
    const all = itemsOf(c), open = all.filter(ZL.undecided);
    return { total: all.length, decided: all.length - open.length, left: open.length, needs: open.filter((i) => i.state === "needs_review").length, edits: all.filter(ZL.editToCheck).length };
  };
  function renderHeader(s) {
    const c = s.case, ready = !!(c && c.status === "ready");
    $("#case-name").hidden = !c; if (c) $("#case-name").textContent = ZL.niceName(c.name) || "Case";
    document.title = c && c.name ? "Treatment timeline · " + ZL.niceName(c.name) : "Treatment timeline";
    $("#case-progress").hidden = !ready; $("#btn-export").hidden = !ready; $("#btn-shortcuts").hidden = !ready;
    if (!ready) return;
    const p = ZL.progressOf(c), bar = $("#progress-bar");
    $("#progress-text").textContent = p.decided + " of " + p.total + " decided" + (p.needs ? " · " + p.needs + (p.needs === 1 ? " item needs" : " items need") + " review" : "");
    bar.max = Math.max(p.total, 1); bar.value = p.decided;
    bar.setAttribute("aria-valuetext", p.decided + " of " + p.total + " items decided");
  }
  // ---- theme: auto (follow the OS), light or dark. Remembered in localStorage when it is available; the page works without it.
  const THEMES = ["auto", "light", "dark"];
  function setTheme(t) {
    const root = document.documentElement;
    if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t);
  }
  // A plain-text file of exactly the text the server built (no editing, no re-assembly here).
  function download(text, name, which) {
    const url = URL.createObjectURL(new Blob([text || ""], { type: "text/plain;charset=utf-8" })), a = el("a", { href: url, download: name });
    document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    status(`Downloaded the ${which} as ${name}.`);
  }
  // What is pending, by name ("2 charges, 1 flag") from the case on screen; falls back to the export's own counts.
  function pendingWords(c) {
    const cs = ZL.state.get().case, pend = (i) => (i.review_status || "pending") === "pending";
    if (!cs) return null;
    const bits = [[(cs.entries || []).concat(cs.undated_entries || []).filter(pend).length, "entry", "entries"], [(cs.amounts || []).filter((a) => pend(a) && a.kind === "charge").length, "charge", "charges"],
      [(cs.amounts || []).filter((a) => pend(a) && a.kind !== "charge").length, "unclear amount", "unclear amounts"], [c.pending_flags, "flag", "flags"]].filter(([n]) => n);
    const edits = (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length;   // T-060 r5 (paralegal M2): her reworded entries that are still marked Needs review
    return bits.map(([n, one, many]) => plural(n, one, many) + " not reviewed").concat(edits ? [plural(edits, "edited entry", "edited entries") + " still marked Needs review (compare with the quote)"] : []);
  }
  const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length : 0; };
  // One primary button for one task: while the confirmation is showing, Copy letter steps down and Copy anyway is the primary.
  function askConfirm(c, then, verb) {
    verb = verb || "Copy";
    const box = ZL.$("#export-confirm"), main = ZL.$('[data-testid="btn-copy-letter"]'); clear(box); box.hidden = false;
    if (main) main.classList.remove("btn--primary");
    const parts = pendingWords(c) || [plural(c.pending, "item", "items") + " not reviewed"];
    const close = () => { box.hidden = true; if (main) { main.classList.add("btn--primary"); main.focus(); } };
    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. " + verb + " the letter anyway?"),
      el("div", { class: "row" }, el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-anyway", onclick: () => { close(); then(); } }, verb + " anyway"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-copy-cancel", onclick: close }, "Go back")));
    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
  }
  function render() {
    const root = ZL.$("#export-body"); clear(root);
    ZL.$("#view-export").hidden = !open;
    if (!open || !data) return;
    const c = data.counts;
    root.append(...[
      el("p", { class: "count-line", "data-testid": "count-line", role: "status" }, countLine(c)),
      (data.warnings || []).length ? el("ul", { class: "ex-warn" }, data.warnings.map((w) => el("li", {}, typeof w === "string" ? w : (w.message || w.code)))) : null,
      el("fieldset", { class: "ex-style", "data-testid": "letter-style" }, el("legend", {}, "Letter layout"),
        [["standard", "Two lines per entry (summary, then source)"], ["oneline", "One line per entry (date, provider, quote)"]].map(([v, t]) => el("label", { class: "ex-style-opt" },
          el("input", { type: "radio", name: "letter-style", value: v, checked: style === v ? true : null, "data-testid": "letter-style-" + v,
            onchange: () => { style = v; load(false).then(() => { const r = ZL.$('[data-testid="letter-style-' + v + '"]'); if (r) r.focus(); }); } }), " " + t))),
      el("p", { id: "export-status", class: "muted small", role: "status" }),
      el("div", { id: "export-confirm", hidden: true }),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h1" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h1" }, "Treatment section (paste into the letter)"),
          el("div", { class: "row ex-btns" },
  ZL.openWhy = openWhy;

  // ---- "What you need to do": one strip above the work, in plain words, each open decision a jump control. Built from the case data, so it is there before the
  // case-checks trace has loaded. Rebuilt when a late panel (the dismissal suggestion) appears.
  let todoHost = null;
  function todoItems(c) {
    const open = (i) => ZL.undecided(i);
    const dated = c.undated_entries.filter(open).length + c.dates_to_confirm.filter((d) => d.candidates.length && !c.undated_entries.some((e) => (e.record_ids || [])[0] === d.record_id)).length;
    const dateless = new Set(c.undated_entries.map((e) => e.id));
    const eEntries = c.entries.filter((e) => open(e) && !dateless.has(e.id)), eEdits = eEntries.filter(ZL.editToCheck).length;
    const flags = (c.flags || []).filter(open).length;
    const charges = (c.amounts || []).filter((a) => open(a) && a.kind === "charge").length;
    const unclear = (c.amounts || []).filter((a) => open(a) && a.kind !== "charge").length;
    const suggest = document.querySelectorAll('[data-testid="dismissal-suggestion"]').length;
    const n = (k, one, many) => k + " " + (k === 1 ? one : many);
    // each button counts what is left to decide in that list; the ONE "need review" number is the lead line above them (and the header and the Timeline chip say the same number)
    const out = [];
    if (dated) out.push(["dates", n(dated, "date to confirm", "dates to confirm"), "Choose the date for the record that has none"]);
    if (eEntries.length - eEdits) out.push(["review", n(eEntries.length - eEdits, "entry to decide", "entries to decide"), ""]);
    if (eEdits) out.push(["review", n(eEdits, "edit to check", "edits to check"), ""]);
    if (flags) out.push(["flags", n(flags, "flag to review", "flags to review"), ""]);
    if (LIB_TITLE[+m[1]]) return LIB_TITLE[+m[1]];
    const t = m[2].replace(/_/g, " ").trim();
    return t ? t.charAt(0).toUpperCase() + t.slice(1) : name;
  };
  // ---- T-060 r5: ONE definition of "still waiting on the paralegal", used by the header, the Open-decisions strip, the Timeline chip, the keyboard flow and the export question.
  // An item is undecided when it is pending, or when she reworded it and it is still marked Needs review (the second check did not agree or did not run: her wording is in the
  // letter, but she has not yet compared it with the quote). A dismissed item is decided and is never counted as needing review.
  ZL.undecided = (i) => { const rs = (i && i.review_status) || "pending"; return rs === "pending" || ZL.editToCheck(i); };
  ZL.needsReview = (i) => !!i && i.state === "needs_review" && ZL.undecided(i);
  ZL.editToCheck = (i) => !!i && i.review_status === "edited" && i.state === "needs_review" && !!i.edited && i.edited.summary != null;   // a reworded entry; a flag's own note is not "wording"
  // A date for a row: <time datetime="2026-01-09">January 9, 2026</time>. The machine date stays in the attribute (tests and assistive tech read it); the person reads the long form.
  ZL.timeEl = (iso, attrs) => ZL.el("time", Object.assign({ datetime: iso }, attrs || {}), ZL.fmtDate(iso));
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
app.js:17:  // ---- case header (sticky): case name, "n of N decided", Export. The numbers are counts of what the API sent; nothing is computed beyond counting.
dom.js:36:    11: "Prior conditions and charge ledger", 12: "Records review, credibility wording", 13: "Copied-forward notes across providers", 14: "Handwritten chiropractic scans", 15: "Conflicting accounts, narrative letter" };
export.js:22:  // What is pending, by name ("2 charges, 1 flag") from the case on screen; falls back to the export's own counts.
export.js:48:    const c = data.counts;
judges.js:1:/* "How the AI was checked" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, agreed / objected / unavailable counts,
judges.js:151:        el("span", { class: d && ((d.totals || {}).unsupported || (d.totals || {}).unavailable || (d.totals || {}).unsure || (gate && gate.code.length)) ? "zs-sumv zj-sum-bad" : "zs-sumv", "data-testid": "judge-summary-counts" }, d ? summaryText(d) : note || "loading…"), toggle));
review.js:243:      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
review.js:299:    if (toCheck && !rechecks[id]) root.append(el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, "Still marked Needs review. Compare your wording with the quote, then press the button to say you did. Until then it counts as open."));
timeline.js:270:    // each button counts what is left to decide in that list; the ONE "need review" number is the lead line above them (and the header and the Timeline chip say the same number)
timeline.js:320:        el("span", { class: "toolbar-counts", "data-testid": "review-counts" },
stepper.js:4:   except "x of y steps passed" counts of what the server returned. Full-mode-only keys (response_raw, edited_text, events[].before/after) may be absent.
stepper.js:241:  // Case-level steps say what to do with counts ("Review the 3 items the AI objected to"), not the item-level sentence.
stepper.js:243:    const c = st.counts || {};
stepper.js:256:        return { text: "Decide the " + plural(n, "detected charge", "detected charges") + ": accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.", label: "Go to the totals", go: () => gotoPanel("charges") };
stepper.js:299:    if (cc) { text = cc.text; if (cc.rerun) { const n = st.id === "export_gate" ? jnrBlockers(st).length : (st.counts || {}).unavailable || 0; buttons.push(n ? S.rerunButton(groupLabel(n)) : S.rerunButton()); rerunToo = true; } if (cc.go) btn(cc.label, cc.go); }
stepper.js:367:  function fmtCounts(counts) {
stepper.js:369:    Object.entries(counts || {}).forEach(([k, v]) => {
stepper.js:491:  // D-045(a): items nobody has decided yet are a WARNING on the gate, not a blocker: they stay out of the letter and the AI disclosure line counts them.
stepper.js:511:    const bits = fmtCounts(st.counts);
stepper.js:512:    return bits.length ? el("p", { class: "zs-counts", "data-testid": "step-counts" }, bits.map((b) => el("span", { class: "zs-chip" }, b))) : null;
stepper.js:527:    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
suggestions.js:137:        // T-102: the counts were measured with other prompts than the ones the app runs now. Said once, ABOVE the numbers so the warning is read first; the changed-prompt detail sits behind a disclosure.
suggestions.js:142:          "Small sample: " + c.case_count + " synthetic test cases, so these counts are a rough indication, not a promise about your records.") : null,
switcher.js:42:      const k = c.counts || {};
export.js:51:      (data.warnings || []).length ? el("ul", { class: "ex-warn" }, data.warnings.map((w) => el("li", {}, typeof w === "string" ? w : (w.message || w.code)))) : null,
stepper.js:158:  const jnrBlockers = (g) => ((g && g.blockers) || []).filter((b) => b.reason_code === "JUDGE_NOT_RUN");
stepper.js:406:  // and decides nothing: a judge step that never ran is "second check missing" only when the gate lists JUDGE_NOT_RUN for this item, otherwise the wording is the
stepper.js:413:    const gated = !!gate && ((gate.blockers || []).some((b) => b.reason_code === "JUDGE_NOT_RUN" && b.item_id === tr.item_id));
stepper.js:493:    const ws = st.warnings || [];
stepper.js:495:    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
stepper.js:529:    const warned = ((gate && gate.warnings) || []).reduce((t, w) => t + (w.count || 0), 0);
stepper.js:566:    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
stepper.js:571:    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").length))));
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:25.403Z

**tool call — Bash**
````
{
 "command": "sed -n 225,262p app/frontend/review.js; grep -n \"ready_to_export\\|\\\"counts\\\"\\|counts\\.\" memory/contracts/api.md | head -30; sed -n 485,500p app/frontend/stepper.js; grep -n \"edit_to_check\" app/backend/*.py | head -20"
}
````

### User / tool · 2026-11-02T12:32:25.628Z

**tool result**
````
  // ---- the one place a decision is sent (accept / edit / dismiss / reset)
  RV.act = async function (id, body, opts) {
    const o = opts || {}; const c = RV.caseNow();
    if (!c || busy.has(id)) return false;
    const found = RV.find(c, id);
    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
    busy.add(id);
    const plan = o.advance ? RV.planAdvance(id) : null;   // the list she is working in, read before the repaint
    try {
      const resp = await ZL.api.review(c.token, id, body);
      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }
      if (drafts[id] && body.action === "edit") drafts[id].open = false;
      if (drafts[id] && body.action === "dismiss") { drafts[id].reasonOpen = false; drafts[id].reason = ""; }
      if (body.action === "edit" && found && found.kind === "entry") rechecks[id] = recheckSentence(resp); else delete rechecks[id];
      if (body.action === "dismiss" && found && found.kind === "entry") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo
      ZL.state.applyReview(resp);
      if (rechecks[id]) RV.say(rechecks[id]);
      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
      restoreFocus(o.advance ? { nextFrom: id, plan } : o.focus ? { id, action: o.focus } : null);
      return true;
    } catch (e) {
      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
        const d = e.detail || {}, ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea'), typed = ta0 ? ta0.value : "";
        const toks = Array.isArray(d.tokens) && d.tokens.length && !String(e.message || "").includes(d.tokens[0]) ? " Not in the quote: " + d.tokens.join(", ") + "." : "";
        showError(id, RV.asTyped((e.message || "That edit is not allowed.") + toks, d.tokens, typed));
        const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (ta) ta.focus();
      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
        refusals[id] = { id, code: nextCode(e), message: RV.asTyped(e.message || "The summary fails a check. Edit the summary to match the quote.", e.detail && e.detail.tokens, (found && found.item && ((found.item.edited && found.item.edited.summary) || found.item.summary)) || ""), label: ZL.stepper && ZL.stepper.label ? ZL.stepper.label(id) : id };
        repaintRefusal(id); RV.say("Not accepted: " + refusals[id].message, true);
        const mine = document.activeElement && document.activeElement.closest && document.activeElement.closest('[data-controls-for="' + id + '"]'), box = (mine || document).querySelector(".rv-refused:not([hidden])");
        if (box) { const r = box.getBoundingClientRect(); if (r.bottom > window.innerHeight - 16) window.scrollBy(0, r.bottom - window.innerHeight + 16); else if (r.top < 60) window.scrollBy(0, r.top - 60); }   // the answer is on screen beside the pressed button, clear of the sticky banner
      } else if (e && String(e.code).toUpperCase() === "DATE_UNCONFIRMED") showError(id, DATE_FIRST + " " + DATE_WHY);
      else showError(id, (e && e.message) || "That did not work. Try again.");
      return false;
125:  "counts": {"entries": 9, "amounts": 3, "flags": 1},
131:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
248:    "counts": {"pending": 22, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
249:    "ready_to_export": false },
254:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
348:  "review": { "counts": {"pending": 21, "accepted": 0, "edited": 1, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
349:              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
355:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
357:- Export: the entry is **not in the letter**, not in `items.entries`, not counted in `counts.entries` or `provenance.edited_count`; it counts in `excluded.pending` and in `excluded.edit_not_confirmed` (subset of pending), and in the notes' "Items not reviewed: N". It does not block export (it is not in the letter, as with a pending item, D-045(a)), unless nothing else is accepted (`NOTHING_ACCEPTED`).
358:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
505:  "counts": {
622:      "counts": {"records": 9, "duplicates_merged": 0, "characters": 4120}, "evidence": {}, "next_action": null },
623:    { "id": "split", "n": 2, "label": "Record boundaries", "kind": "code", "status": "pass", "counts": {"method": "code", "llm_split": false}, "...": "..." },
625:      "counts": {"parsed": 7, "confirmed": 0, "ambiguous": 1, "missing": 1},
627:    { "id": "extract", "kind": "llm", "counts": {"records_to_draft": 9, "entries": 8, "rejected": 0, "records_without_entry": 1} },
628:    { "id": "grounding", "kind": "code", "counts": {"items_checked": 20, "rejected": 1, "reasons": {"GROUNDING_EXCERPT_NOT_VERBATIM": 1}} },
629:    { "id": "judges", "kind": "llm", "counts": {"items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1} },
630:    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
631:    { "id": "totals", "kind": "code", "counts": {"accepted_cents": 0, "pending_cents": 839000, "pending_charges": 2, "not_totaled": 1} },
632:    { "id": "review", "kind": "human", "counts": {"pending": 21, "accepted": 0, "edited": 0, "dismissed": 0} },
635:      "counts": {"blocking": 1, "pending_items": 21, "date_unconfirmed": 1, "accepted": 0, "dismissed": 0, "rejected_not_blocking": 1, "judge_not_run": 0},
644:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **T-114 (rates):** every amount in `amounts[]` carries `accept_effect` and `judge_required_for_export`. `accept_effect` is `letter_total` (a `charge`: counted in the billed-charges total), `acknowledge` (a `rate`: accepting it only acknowledges it, it is listed in the internal notes and never totaled, D-019/D-042) or `internal_notes` (`estimate`, `unclear`). `judge_required_for_export` is `false` only for a rate: an accepted rate whose second check never ran is **not** a `JUDGE_NOT_RUN` blocker, so accepting a rate can never block export (its item trace `judge_2` step says the check is optional for a rate). The UI should label a rate's button "Acknowledge" (or keep "Accept as noted") and never promise it goes in the letter. Charges, entries and flags are unchanged. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
674:`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
774:| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D-032 `objective_negative`). Listed only in the case payload's `tray_filtered` (collapsed group with the rule named and a count); not a flag, not in the queue, counts, gate or export; no action needed. `reasons[0]` is this code; a grounding or injection reason follows it when it applies (a filtered quote that is not word for word in the record carries `GROUNDING_EXCERPT_NOT_VERBATIM` and its `why` says so; the export never prints it). T-126 r2: **every** tray flag (state `rejected`: judge-rejected, not word for word, rule-filtered) is left out of the export's `flags`, its pending count and its internal notes, so the notes' "Items not reviewed" equals `review.counts.pending`. When the AI proposes one quote under several categories, code keeps one flag and lists the others in `ladder.code_checks.merged_categories` (item trace step `proposals_merged`) |
    const sorted = orderBlockers(bl), first = sorted.slice(0, 6), rest = sorted.slice(6);
    return el("div", { class: "zs-gate", "data-testid": "gate-blockers" },
      el("p", { class: "zs-ev" }, el("strong", {}, (title || "Blocking the export") + " (" + sorted.length + "):")),
      el("ul", { class: "zs-blockers" }, first.map((b) => blockerRow(b, hideWhy))),
      rest.length ? el("details", { class: "zs-more" }, el("summary", {}, "Show the other " + rest.length), el("ul", { class: "zs-blockers" }, rest.map((b) => blockerRow(b, hideWhy)))) : null);
  }
  // D-045(a): items nobody has decided yet are a WARNING on the gate, not a blocker: they stay out of the letter and the AI disclosure line counts them.
  function warningNode(st) {
    const ws = st.warnings || [];
    if (!ws.length) return null;
    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
      el("p", { class: "zs-todo-text" }, el("strong", {}, "Not reviewed (" + (w.count != null ? w.count : "") + "): "), w.why || ""),
      el("p", { class: "zs-ev" }, "This does not block the export."),
      el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn", "data-testid": "btn-gate-warning-jump", onclick: () => gotoFirstPending() }, "Go to the first pending item")))));
  }
  function gateNode(st) {
app/backend/present.py:49:            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter
app/backend/present.py:201:    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
app/backend/present.py:206:            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
app/backend/trace.py:1021:    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
app/backend/trace.py:1025:    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
app/backend/trace.py:1026:        n = rc["edit_to_check"]
app/backend/trace.py:1037:    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
app/backend/trace.py:1090:    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:30.149Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"applyReview\" -A25 state.js | head -60; grep -n \"review_status\\|counts\" mock.js | head -40; grep -n \"Edit_to\\|edit-check\\|edit_check\\|data-edit-check\" ../../tests/e2e/*.py | head -30"
}
````

### User / tool · 2026-11-02T12:32:30.258Z

**tool result**
````
11:    applyReview(resp) {
12-      const c = s.case; if (!c || !resp || !resp.item) return;
13-      for (const k of ["entries", "undated_entries", "amounts", "flags"]) {
14-        const i = (c[k] || []).findIndex((x) => x.id === resp.item.id);
15-        if (i >= 0) { // the review response labels items with a generic kind ("amount"); an amount's own kind (charge / rate / ...) must survive
16-          const { kind, ...rest } = resp.item; c[k][i] = Object.assign({}, c[k][i], rest);
17-        }
18-      }
19-      if (resp.totals) c.totals = Object.assign({}, c.totals, resp.totals);
20-      if (resp.review) c.review = Object.assign({}, c.review, resp.review);
21-      ZL.state.set({ case: c });
22-    },
23-  };
24-  // Extension points for T-043 (frontend-2): register without editing T-042 files.
25-  ZL.hooks = { rowActions: [], panels: [] };           // rowActions: fn(entry, rowEl); panels: fn(case, mountEl) -> void
26-  ZL.registerRowActions = (fn) => ZL.hooks.rowActions.push(fn);
27-  ZL.registerPanel = (fn) => ZL.hooks.panels.push(fn);
28-})();
92:        review_status: "pending", edited: null, duplicate_note: null, ladder: ladder("e" + r.seq, r, ex, state, { summary, verdict: needs ? "partially" : "supported" }) };
103:          review_status: "pending", edited: null, duplicate_note: null, ladder: { item_id: "a" + (amounts.length + 1), state: rate ? "needs_review" : "verified", backend: "fixture", generator: null,
114:        origin: "code", reviewer_note: null, state: "verified", reasons: [], why: "Calculated by code from two dates read from the record headers.", review_status: "pending", edited: null,
123:    const acc = c.amounts.filter((a) => a.kind === "charge" && ["accepted", "edited"].includes(a.review_status));
124:    const pend = c.amounts.filter((a) => a.kind === "charge" && a.review_status === "pending");
125:    const det = c.amounts.filter((a) => a.kind === "charge" && a.review_status !== "dismissed");
131:    c.review = { queue: c._queue, counts: { pending: n((i) => i.review_status === "pending"), accepted: n((i) => i.review_status === "accepted"), edited: n((i) => i.review_status === "edited"),
132:      dismissed: n((i) => i.review_status === "dismissed"), needs_review: n((i) => i.state === "needs_review"), verified: n((i) => i.state === "verified"), rejected: c.tray.length }, ready_to_export: false };
172:          progress: { done: Math.round(frac * total), total, label: `Checking summaries ${Math.round(frac * total)} of ${total}` }, counts: { entries: c.entries.length, amounts: c.amounts.length, flags: c.flags.length }, error: null, elapsed_ms: Date.now() - c._run });
187:        if (a === "accept") it.review_status = "accepted"; else if (a === "dismiss") it.review_status = "dismissed"; else if (a === "reset") { it.review_status = "pending"; it.edited = null; }
188:        else if (a === "edit" && body.edits && typeof body.edits.summary === "string" && id[0] === "e") { it.edited = { summary: body.edits.summary, original_summary: it.summary, at: new Date().toISOString(), kept_my_wording: false }; it.summary = body.edits.summary; it.review_status = "edited"; }
189:        else if (a === "edit" && body.edits && typeof body.edits.note === "string" && id[0] === "f") { it.reviewer_note = body.edits.note; it.review_status = "edited"; }
198:        if (act === "accept") found.forEach((e) => { if (e && (e.state !== "verified" || e.review_status !== "pending")) bad.push({ id: e.id, reason: "only verified, not-yet-reviewed entries can be accepted in a batch" }); });
200:        found.forEach((e) => { if (act === "accept") e.review_status = "accepted"; else { e.review_status = "pending"; e.edited = null; } });
202:        return ok({ items: found.map((e) => ({ id: e.id, review_status: e.review_status })), totals: clone(c.totals), review: clone(c.review), warnings: [] });
../../tests/e2e/conftest.py:64:  edit-check-hint (a reworded entry that is still marked Needs review: its btn-accept reads 'I compared it with the quote'; the row carries data-edit-check; it counts as open in the header, todo-list ('1 edit to check') and the copy-confirm),
../../tests/e2e/test_polish_r5.py:4:T-121 the one-line letter control. New hooks (QA adds them to tests/e2e/conftest.py docstring): need-review-count, edit-check-hint, letter-style, letter-style-standard, letter-style-oneline,
../../tests/e2e/test_polish_r5.py:5:tray-filtered, tray-filtered-summary, tray-filtered-rule, tray-filtered-item; data-edit-check, data-group."""
../../tests/e2e/test_polish_r5.py:95:    assert e.get_attribute("data-edit-check") is not None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:31.991Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p tests/e2e/test_polish_r5.py; sed -n 60,160p tests/e2e/test_polish_r5.py; grep -n \"def \\|^import\\|^from\" tests/e2e/conftest.py | head -50; grep -n \"excerpt\\|sentences\" tests/e2e/test_change_the_quote.py | head -30"
}
````

### User / tool · 2026-11-02T12:32:32.094Z

**tool result**
````
"""T-060 round 5 + T-131 (frontend): HITL correctness and the ux pass-4 minors.
M1 a dismissed flag / amount keeps no Accept and `a` never flips it; M2 a reworded entry still marked Needs review is not decided, is named at export and has a control that clears it;
F3 after a / d focus stays in the same list; F2 one need-review count; F1/F5 plain reason sentences, each reason once; m6 long dates in <time datetime>; D-057 the Filtered-by-rule group;
T-121 the one-line letter control. New hooks (QA adds them to tests/e2e/conftest.py docstring): need-review-count, edit-check-hint, letter-style, letter-style-standard, letter-style-oneline,
tray-filtered, tray-filtered-summary, tray-filtered-rule, tray-filtered-item; data-edit-check, data-group."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case

RAW_CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b|summary token|\btoken\b|\bjudge unavailable\b|\blexicon\b|\bfixture\b", re.I)


def _progress(page):
    t = page.locator("#progress-text").inner_text()
    m = re.match(r"(\d+) of (\d+) decided(?: · (\d+) items? needs? review)?", t)
    assert m, t
    return int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)


def _flag(page, kind="conflict"):
    return page.locator(f'[data-testid=flags-panel] [data-flag-type={kind}]').first


def _edit_entry_3(page):
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    return e
    expect(r).to_have_attribute("data-review", "dismissed"); assert _progress(page) == before


def test_dismissing_a_flag_lowers_the_one_need_review_count(page, sample_case):
    open_case(page, sample_case)
    d0, t0, n0 = _progress(page); assert n0 > 0
    fid = _flag(page).get_attribute("data-item-id"); needs = _flag(page).get_attribute("data-state") == "needs_review"
    _flag(page).get_by_test_id("btn-dismiss").click(); expect(page.locator(f'[data-item-id="{fid}"]')).to_have_attribute("data-review", "dismissed")
    d1, t1, n1 = _progress(page)
    assert d1 == d0 + 1 and n1 == n0 - (1 if needs else 0)


# ---- F2: header, Open-decisions strip and Timeline chip show the same number and move together
def test_one_need_review_count_everywhere(page, sample_case):
    open_case(page, sample_case)
    def counts():
        h = _progress(page)[2]
        strip = int(re.match(r"(\d+)", page.get_by_test_id("need-review-count").inner_text()).group(1))
        chip = int(re.match(r"(\d+)", page.get_by_test_id("review-counts").locator(".chip--warn").inner_text()).group(1))
        return h, strip, chip
    h, s, c = counts(); assert h > 0 and h == s == c, (h, s, c)
    fid = _flag(page).get_attribute("data-item-id")
    _flag(page).get_by_test_id("btn-dismiss").click(); expect(page.locator(f'[data-item-id="{fid}"]')).to_have_attribute("data-review", "dismissed")
    h2, s2, c2 = counts(); assert h2 == s2 == c2, (h2, s2, c2)
    page.get_by_test_id("entry-1").get_by_test_id("btn-dismiss").click()
    h3, s3, c3 = counts(); assert h3 == s3 == c3, (h3, s3, c3)


# ---- M2: a reworded entry that is still marked Needs review is not decided
def test_edited_needs_review_entry_is_open_until_she_says_she_compared_it(page, sample_case):
    open_case(page, sample_case)
    d0, t0, n0 = _progress(page)
    e = _edit_entry_3(page)
    if e.get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit; the case needs the judge to be unavailable (fixture backend)")
    assert e.get_attribute("data-edit-check") is not None
    d1, t1, n1 = _progress(page); assert d1 == d0, "an edit that is still Needs review was counted as decided"
    assert n1 >= 1 and page.get_by_test_id("need-review-count").inner_text().startswith(str(n1))
    ok = e.get_by_test_id("btn-accept"); expect(ok).to_contain_text("I compared it with the quote"); assert "btn--primary" in ok.get_attribute("class")
    expect(page.get_by_test_id("todo-list")).to_contain_text("1 edit to check")
    ok.click(); expect(page.get_by_test_id("entry-3")).to_have_attribute("data-review", "accepted")
    d2, t2, n2 = _progress(page); assert d2 == d0 + 1


def test_edit_to_check_is_named_before_the_letter_is_copied(page, sample_case):
    open_case(page, sample_case)
    if _edit_entry_3(page).get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit")
    page.get_by_test_id("entry-1").get_by_test_id("btn-accept").click()          # something is in the letter
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    expect(page.get_by_test_id("copy-confirm")).to_contain_text("1 edited entry still marked Needs review")


def test_nothing_left_message_does_not_come_while_an_edit_is_open(page, sample_case):
    open_case(page, sample_case)
    if _edit_entry_3(page).get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit")
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for it in c["entries"] + c["amounts"] + c["flags"]:                       # decide everything else over the API
        if it["id"] != [e for e in c["entries"] if "r3" in e["record_ids"]][0]["id"] and it["state"] != "rejected" and it["review_status"] == "pending":
            api("POST", f"/api/cases/{sample_case}/items/{it['id']}/review", {"action": "dismiss"})
    page.reload(); page.get_by_test_id("timeline").wait_for()
    d, t, n = _progress(page); assert d == t - 1, (d, t)
    page.get_by_test_id("entry-3").focus(); page.keyboard.press("a")
    expect(page.locator("#rv-live")).to_contain_text("Nothing left to decide")


# ---- F3: a / d stay inside one list; a second `a` never accepts a flag the reviewer did not choose
def test_second_a_never_accepts_a_conflict_flag(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus()
    page.keyboard.press("a"); page.wait_for_timeout(500)
    in_queue = page.evaluate("!!document.activeElement.closest('[data-testid=queue]')")
    assert in_queue, "focus left the timeline after the first accept"
    page.keyboard.press("a"); page.wait_for_timeout(500)
    assert page.locator("[data-testid=flags-panel] [data-review=accepted]").count() == 0, "a conflict flag was accepted by the second a"
    assert page.evaluate("!!document.activeElement.closest('[data-testid=queue]')")
    assert page.locator("[data-testid=queue] [data-review=accepted]").count() == 2


def test_a_run_down_the_timeline_stays_in_the_timeline(page, sample_case):
    open_case(page, sample_case)
    n = page.locator("[data-testid=queue] [data-item-id]").count()
    page.get_by_test_id("entry-1").focus()
    for _ in range(n + 2):                                                   # more presses than entries
        page.keyboard.press("a"); page.wait_for_timeout(250)
    assert page.locator("[data-testid=flags-panel] [data-review=accepted]").count() == 0
    assert page.locator("[data-testid=charges-panel] [data-review=accepted]").count() == 0
    assert page.locator("[data-testid=queue] [data-review=accepted]").count() == n


def test_flag_decision_moves_to_the_next_flag_of_the_same_kind_only(page, sample_case):
    open_case(page, sample_case)
    kinds = page.locator("[data-testid=flags-panel] [data-group]").evaluate_all("els => els.map(e => [e.getAttribute('data-group'), e.querySelectorAll('[data-item-id]').length])")
    kind = next(k for k, n in kinds if n >= 1)
    grp = page.locator(f'[data-testid=flags-panel] [data-group="{kind}"]'); n = grp.locator("[data-item-id]").count()
    grp.locator("[data-item-id]").first.focus()
    for _ in range(n + 1):
        page.keyboard.press("d"); page.wait_for_timeout(300)
        assert page.evaluate("(k) => { const a = document.activeElement.closest('[data-item-id]'); return !a || !!a.closest('[data-group=\"' + k + '\"]') || !!document.querySelector('#rv-live') }", kind)
    others = page.locator(f'[data-testid=flags-panel] [data-group]:not([data-group="{kind}"]) [data-review=dismissed]').count()
69:import json, os, urllib.request, urllib.error
70:import pytest
75:def _up():
82:def pytest_collection_modifyitems(config, items):
90:def api(method, path, body=None):
100:def golden_text(name):
104:def base_url():
108:def sample_case():
123:def pw():
129:def page(pw):
138:def open_case(page, tok):
153:    def __init__(self, page, token, ids):
159:    def _summary(self, i):
164:    def active(self):
167:    def _na(self, i):
170:    def blockers(self):
173:    def _case_trace(self, route):
183:    def _item_trace(self, route):
194:    def _export(self, route):
211:    def __init__(self, page, token, ids, mode="clears", hold=False, exempt=()):
219:    def active(self):
228:    def _na(self, i):
231:    def _blockers(self):
234:    def _case_trace(self, route):
247:    def _item_trace(self, route):
255:    def _judges(self, route):
267:    def _export(self, route):
274:    def _rejudge(self, route):
280:    def release(self):
284:    def _answer(self, route):
3:lines, so picking whole sentences rebuilds a quote the save route accepts; the refused Accept is lifted by it.
4:No new test ids: btn-accept, accept-refused, btn-accept-refused-quote, excerpt-editor, excerpt-unit, btn-save-excerpt, excerpt-error (all declared in conftest)."""
16:        if e["state"] == "verified" and e["date"] and e["review_status"] == "pending" and len(e["record_ids"]) == 1 and len(r["sentences"]) >= 2:
26:        for s in r["sentences"]:
32:        run = [s for s in r["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
33:        assert run and r["text"][run[0]["start"] - r["char_start"]:run[-1]["end"] - r["char_start"]] == e["excerpt"], "the units rebuild the AI's own quote"
39:    orig = e["excerpt"]
41:    assert _entry(sample_case, e["id"])["excerpt"] != orig
48:        ed = row.get_by_test_id("excerpt-editor"); expect(ed).to_be_visible()
49:        units = ed.get_by_test_id("excerpt-unit")
52:        # pick the sentences that make up the original quote (the picker preselects the stored span; the broken quote started mid-sentence, so it is the whole-sentence run)
53:        want = [s["text"] for s in rec["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
58:        ed.get_by_test_id("btn-save-excerpt").click()
59:        expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()
61:            if _entry(sample_case, e["id"])["excerpt"] == orig:
65:        assert got["excerpt"] == orig and got["review_status"] == "edited", (got["excerpt"], got["review_status"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:35.314Z

**tool call — Bash**
````
{
 "command": "sed -n 1,75p tests/e2e/test_change_the_quote.py; sed -n 104,150p tests/e2e/conftest.py; grep -n \"excerpt_start\\|\\\"excerpt\\\"\" memory/contracts/api.md | head -12; lsof -iTCP -sTCP:LISTEN -P | grep -E \"78|87|41\" | head"
}
````

### User / tool · 2026-11-02T12:32:35.495Z

**tool result**
````
"""T-108: "Change the quote" completes end to end on the sample, against the REAL backend (needs ZLAYT_DB, the SQLite file of the server under test, to put
a bad quote into the store the way a stale or imported state would). The picker's sentence units carry no `Excerpt: "` wrapper, no quote marks and no header
lines, so picking whole sentences rebuilds a quote the save route accepts; the refused Accept is lifted by it.
No new test ids: btn-accept, accept-refused, btn-accept-refused-quote, excerpt-editor, excerpt-unit, btn-save-excerpt, excerpt-error (all declared in conftest)."""
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case
from tests.e2e.test_code_check_refusal import _break_quote, _entry, row_of


def _entry_with_a_picker(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    recs = {r["id"]: r for r in c["records"]}
    for e in c["entries"]:
        r = recs[e["record_ids"][0]]
        if e["state"] == "verified" and e["date"] and e["review_status"] == "pending" and len(e["record_ids"]) == 1 and len(r["sentences"]) >= 2:
            return e, r
    pytest.fail("no entry with a quote picker on the sample")


def test_sample_units_carry_no_wrapper_and_rebuild_every_entry_quote(sample_case):
    c = api("GET", f"/api/cases/{sample_case}")[1]
    recs = {r["id"]: r for r in c["records"]}
    raw_of = lambda r, s: r["text"][s["start"] - r["char_start"]:s["end"] - r["char_start"]]
    for r in c["records"]:
        for s in r["sentences"]:
            assert s["text"] == raw_of(r, s) and not s["text"].startswith(("Excerpt", "Date:", "Source:", "===")) and '"' not in s["text"], s["text"]
    for e in c["entries"] + c["undated_entries"]:
        if len(e["record_ids"]) != 1:
            continue
        r = recs[e["record_ids"][0]]
        run = [s for s in r["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
        assert run and r["text"][run[0]["start"] - r["char_start"]:run[-1]["end"] - r["char_start"]] == e["excerpt"], "the units rebuild the AI's own quote"


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_change_the_quote_saves_and_lifts_the_refusal(pw, sample_case, w, h):
    e, rec = _entry_with_a_picker(sample_case)
    orig = e["excerpt"]
    _break_quote(sample_case, e["id"])
    assert _entry(sample_case, e["id"])["excerpt"] != orig
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        open_case(pg, sample_case); row = row_of(pg, e["id"]); row.scroll_into_view_if_needed()
        row.get_by_test_id("btn-accept").click()
        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
        box.get_by_test_id("btn-accept-refused-quote").click()
        ed = row.get_by_test_id("excerpt-editor"); expect(ed).to_be_visible()
        units = ed.get_by_test_id("excerpt-unit")
        texts = [t.strip() for t in ed.locator("li").all_inner_texts()]
        assert texts and all(not t.startswith(("Excerpt", "Date:", "Source:")) and '"' not in t for t in texts), texts
        # pick the sentences that make up the original quote (the picker preselects the stored span; the broken quote started mid-sentence, so it is the whole-sentence run)
        want = [s["text"] for s in rec["sentences"] if s["start"] >= e["excerpt_start"] and s["end"] <= e["excerpt_end"]]
        for i in range(units.count()):
            on = texts[i] in want
            if units.nth(i).is_checked() != on:
                units.nth(i).click()
        ed.get_by_test_id("btn-save-excerpt").click()
        expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()
        for _ in range(40):
            if _entry(sample_case, e["id"])["excerpt"] == orig:
                break
            pg.wait_for_timeout(250)
        got = _entry(sample_case, e["id"])
        assert got["excerpt"] == orig and got["review_status"] == "edited", (got["excerpt"], got["review_status"])
        # the saved quote passes the code checks again: the item can now be accepted without a CODE_CHECK_FAILED refusal
        st, body = api("POST", f"/api/cases/{sample_case}/items/{e['id']}/review", {"action": "accept"})
        assert st == 200, (st, body)
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)



class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
147:      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
148:      "excerpt_start": 396, "excerpt_end": 532,
155:                      "output": {"summary": "Diagnosed with cervical strain ...", "excerpt": "Dx: cervical strain; ..."}},
165:      "excerpt": "ER charges: $6,240.", "excerpt_start": 533, "excerpt_end": 552,
174:      "excerpt": "Charge per visit $185.", "excerpt_start": 929, "excerpt_end": 951,
195:        {"record_id": "r6", "excerpt": "Date: 2026-03-06", "start": 1107, "end": 1123},
196:        {"record_id": "r6", "excerpt": "Source: Capital PT, visit 9", "start": 1124, "end": 1151},
197:        {"record_id": "r7", "excerpt": "Date: 2026-05-18", "start": 1242, "end": 1258},
198:        {"record_id": "r7", "excerpt": "Source: Hill Country Pain Management, new patient", "start": 1259, "end": 1308} ],
210:        {"record_id": "r7", "excerpt": "Date of accident per intake form: 2026-01-19.", "start": 1407, "end": 1452},
211:        {"record_id": "r1", "excerpt": "Date: 2026-01-09", "start": 123, "end": 139},
212:        {"record_id": "r2", "excerpt": "Date: 2026-01-09", "start": 332, "end": 348} ],
Adobe\x20  1078 arsis   27u  IPv4 0xef02ca575990f956      0t0  TCP localhost:15292 (LISTEN)
qemu-syst 12904 arsis   58u  IPv6 0x73a8419400e2c319      0t0  TCP *:8602 (LISTEN)
Python    14724 arsis    9u  IPv4 0x4eb42ba57b9d54f4      0t0  TCP localhost:7860 (LISTEN)
qemu-syst 15492 arsis   53u  IPv6 0x6a3041bff1bab0ff      0t0  TCP localhost:5613 (LISTEN)
qemu-syst 15492 arsis   55u  IPv6 0x8d8728f4c7baa5fa      0t0  TCP localhost:51128 (LISTEN)
Python    16226 arsis    9u  IPv4 0xd7516849ddec546e      0t0  TCP localhost:7899 (LISTEN)
qemu-syst 20157 arsis    9u  IPv6  0x851a164c24142e4      0t0  TCP localhost:52627 (LISTEN)
qemu-syst 20157 arsis   12u  IPv6 0x2b59415036efe10c      0t0  TCP localhost:52628 (LISTEN)
qemu-syst 20157 arsis   52u  IPv4 0xc37048876dc239ce      0t0  TCP localhost:5609 (LISTEN)
qemu-syst 20157 arsis   53u  IPv6   0x144c7ca5378957      0t0  TCP localhost:5609 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:37.661Z

**tool call — Bash**
````
{
 "command": "git status --short app tests | head; git worktree add --detach /private/tmp/claude-501/wt-t136 HEAD 2>&1 | tail -1; ls .venv/bin/python; cat tools/serve_app.sh | head -30"
}
````

### User / tool · 2026-11-02T12:32:38.238Z

**tool result**
````
 M app/backend/conflict_candidates.py
 M app/backend/flags.py
 M app/backend/lexicon_scan.py
 M app/backend/why.py
 M tests/unit/test_conflict_candidates.py
 M tests/unit/test_flags_pass.py
 M tests/unit/test_t132_attribution_unit.py
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
HEAD is now at 5fb338d fix(backend): T-134 an edit still Needs review is open: out of the letter, not accepted, gate warns EDIT_NOT_CONFIRMED, notes say second check not available
.venv/bin/python
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:42.142Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; mkdir -p /private/tmp/claude-501/t136db && (PORT=7931 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 nohup .venv/bin/python -m app.main > /private/tmp/claude-501/t136db/log 2>&1 & echo $! > /private/tmp/claude-501/t136db/pid); sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7931/; cat /private/tmp/claude-501/t136db/pid; tail -3 /private/tmp/claude-501/t136db/log"
}
````

### User / tool · 2026-11-02T12:32:46.268Z

**tool result**
````
200
39474
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:50.439Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && cat > /private/tmp/claude-501/t136db/probe.py <<'EOF'\nimport json,time,urllib.request\nB=\"http://127.0.0.1:7931\"\ndef api(m,p,b=None):\n    r=urllib.request.Request(B+p,data=json.dumps(b).encode() if b is not None else None,method=m,headers={\"Content-Type\":\"application/json\"})\n    try:\n        with urllib.request.urlopen(r) as x: return x.status,json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or b\"null\")\nst,c=api(\"POST\",\"/api/cases\",{\"sample\":True}); t=c[\"token\"]; api(\"POST\",f\"/api/cases/{t}/run\",{})\nwhile api(\"GET\",f\"/api/cases/{t}/status\")[1][\"status\"] not in(\"ready\",\"failed\"): time.sleep(1)\nc=api(\"GET\",f\"/api/cases/{t}\")[1]\nrecs={r[\"id\"]:r for r in c[\"records\"]}\nfor e in c[\"entries\"]:\n    r=recs[e[\"record_ids\"][0]]\n    print(e[\"id\"],e[\"state\"],e[\"review_status\"],e.get(\"edit_to_check\"),len(r[\"sentences\"]),e[\"excerpt_start\"],e[\"excerpt_end\"],e[\"reasons\"])\nprint(c[\"review\"][\"counts\"])\n# try excerpt-only edit on a needs_review entry\nfor e in c[\"entries\"]:\n    r=recs[e[\"record_ids\"][0]]\n    if e[\"state\"]==\"needs_review\" and len(r[\"sentences\"])>=2:\n        print(\"try\",e[\"id\"],[s[\"text\"] for s in r[\"sentences\"]])\n        break\nprint(t)\nEOF\n.venv/bin/python /private/tmp/claude-501/t136db/probe.py; grep -n \"excerpt\" memory/contracts/api.md | grep -i \"edits\\|edit\" | head -5"
}
````

### User / tool · 2026-11-02T12:32:51.881Z

**tool result**
````
e1 verified pending False 4 180 312 []
e2 verified pending False 6 396 532 []
e3 verified pending False 3 633 723 []
e4 verified pending False 3 858 928 []
e5 verified pending False 2 1026 1047 []
e6 verified pending False 2 1162 1222 []
e7 verified pending False 4 1319 1406 []
e8 verified pending False 2 1536 1660 []
e9 verified pending False 2 1771 1876 []
{'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0, 'edit_to_check': 0}
DGBMzQKHsxUvkCMz4OmLxQ
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
330:  { "action": "edit", "edits": { "excerpt": "Discharged from PT after two missed appointments. Pain 3/10." } },
334:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
355:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
360:- Frontend: an excerpt-only edit (the quote picker) is `edit_to_check` too; use the item's `edit_to_check` instead of the local summary-only test so the row offers the same "I compared it with the quote" Accept.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:55.568Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && grep -n \"_break_quote\" -B3 -A25 tests/e2e/test_code_check_refusal.py | head -80; grep -n \"ZLAYT_DB\\|sqlite\" tests/e2e/*.py | head -20"
}
````

### User / tool · 2026-11-02T12:32:55.658Z

**tool result**
````
183-QUOTE_NEXT = {"code": "EDIT_QUOTE", "text": "Change the quote to whole sentences of the record that keep the hedge sentence"}
184-
185-
186:def _break_quote(tok, eid):
187-    """Real backend: store a quote that starts mid-sentence (first word cut off), like a stale or imported state. The record offsets stay, so the quote picker still preselects the whole sentences."""
188-    path = os.environ.get("ZLAYT_DB")
189-    if not path:
190-        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
191-    sys.path.insert(0, ROOT)
192-    from app.db import db as DB
193-    conn = DB.connect(path)
194-    try:
195-        words = _entry(tok, eid)["excerpt"].split(" ")
196-        DB.update_item(conn, eid, now=9e9, case=tok, excerpt=" ".join(words[1:]))
197-    finally:
198-        conn.close()
199-
200-
201-class RefuseQuote(Refuse):
202-    """Stub: accept (single and batch) and a summary-only edit answer 422 CODE_CHECK_FAILED / EDIT_QUOTE while the item's quote is unchanged; a quote edit goes to the real route and lifts it."""
203-    def __init__(self, tok, eid, edit_code="EDIT_QUOTE"):
204-        super().__init__(tok, eid)
205-        self.base_q = _entry(tok, eid)["excerpt"]
206-        self.edit_code = edit_code
207-
208-    def active(self):
209-        return _entry(self.tok, self.eid)["excerpt"] == self.base_q and _entry(self.tok, self.eid)["review_status"] == "pending"
210-
211-    def _detail(self, code):
--
239-    c = api("GET", f"/api/cases/{sample_case}")[1]
240-    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
241-    if request.param == "real":
242:        _break_quote(sample_case, e["id"]); stub = None
243-    else:
244-        stub = RefuseQuote(sample_case, e["id"])
245-    return {"tok": sample_case, "id": e["id"], "orig": e["summary"], "excerpt": e["excerpt"], "mode": request.param, "stub": stub}
246-
247-
248-def _picker_open(page, t):
249-    """The item's own quote picker is open (its sentences listed, focus on one of them, on screen). Saving a choice is the picker's own job (excerpt.js); the sample record prints
250-    'Excerpt: "..."' around the quote, so its sentence units cannot rebuild the original quote and this spec stops at opening it."""
251-    row = row_of(page, t["id"]); ed = row.get_by_test_id("excerpt-editor")
252-    expect(ed).to_be_visible(); assert ed.get_by_test_id("excerpt-unit").count() >= 2
253-    assert page.evaluate("document.activeElement.getAttribute('data-testid')") == "excerpt-unit", "focus moves into the picker"
254-    assert vis(page, ed.get_by_test_id("btn-save-excerpt")) or vis(page, ed.get_by_test_id("excerpt-unit").first), "the picker is on screen"
255-
256-
257-@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
258-def test_refused_accept_on_a_quote_check_offers_change_the_quote_and_opens_the_picker(pw, broken_quote, w, h):
259-    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
260-    try:
261-        t = arm(broken_quote, pg)
262-        open_case(pg, t["tok"]); row = row_of(pg, t["id"]); row.scroll_into_view_if_needed()
263-        row.get_by_test_id("btn-accept").click()
264-        box = row.get_by_test_id("accept-refused"); expect(box).to_be_visible()
265-        msg = box.get_by_test_id("accept-refused-msg").inner_text()
266-        assert msg.startswith("Not accepted. ") and "whole sentences" in msg, msg
267-        q = box.get_by_test_id("btn-accept-refused-quote")
--
330-def _why_dialog(page, t, rewrite_label=None):
331-    """Accept the item (AI draft), break its quote in the store, open the Why dialog. rewrite_label rewrites the item trace's verdict label (a stub of what the backend sends)."""
332-    assert api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"})[0] == 200
333:    _break_quote(t["tok"], t["id"])
334-    if rewrite_label:
335-        def fn(route):
336-            d = route.fetch().json(); d["verdict"] = dict(d.get("verdict") or {}, label=rewrite_label); route.fulfill(json=d)
337-        page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/trace$"), fn)
338-    open_case(page, t["tok"])
339-    page.locator(f'[data-testid="queue"] [data-item-id="{t["id"]}"], [data-testid="timeline"] [data-item-id="{t["id"]}"]').first.get_by_test_id("entry-why").click()
340-    st = page.get_by_test_id("item-stepper"); st.wait_for()
341-    return st
342-
343-
344-def test_why_dialog_uses_the_backend_verdict_string_for_an_ai_draft_and_offers_change_the_quote(page, sample_case):
345-    c = api("GET", f"/api/cases/{sample_case}")[1]
346-    e = next(x for x in c["entries"] if x["state"] == "verified" and x["date"] and x["review_status"] == "pending")
347-    st = _why_dialog(page, {"tok": sample_case, "id": e["id"]})
348-    assert st.get_by_test_id("item-verdict").inner_text() == "Needs your attention: a check on this summary fails", "the backend's verdict string as sent"
349-    w = st.get_by_test_id("item-wording-fail"); txt = w.inner_text()
tests/e2e/test_change_the_quote.py:1:"""T-108: "Change the quote" completes end to end on the sample, against the REAL backend (needs ZLAYT_DB, the SQLite file of the server under test, to put
tests/e2e/test_code_check_refusal.py:2:with an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server
tests/e2e/test_code_check_refusal.py:24:    path = os.environ.get("ZLAYT_DB")
tests/e2e/test_code_check_refusal.py:26:        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
tests/e2e/test_code_check_refusal.py:181:# inline under the edit box (typed text kept); the Why dialog follows the backend verdict string as sent. Real backend (ZLAYT_DB) and a route stub per case.
tests/e2e/test_code_check_refusal.py:188:    path = os.environ.get("ZLAYT_DB")
tests/e2e/test_code_check_refusal.py:190:        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
tests/e2e/test_local_mode.py:10:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=str(tmp_path_factory.mktemp("loc") / "l.sqlite3"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:57.817Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && grep -n \"def update_item\" -A30 app/db/db.py | head -50"
}
````

### User / tool · 2026-11-02T12:32:57.911Z

**tool result**
````
200:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
201-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
202-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
203-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
204-    if locked & set(fields):
205-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
206-    table, found = _find(conn, item_id, case)
207-    bad = set(fields) - _cols(conn, table)
208-    if bad:
209-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
210-    fields["updated_at"] = now
211-    sets = ", ".join(f"{k}=?" for k in fields)
212-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
213-
214-
215-def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:32:59.058Z

Probe: set an entry to needs_review/JUDGE_UNAVAILABLE in the DB, then edit only the excerpt over the API.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:01.404Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && cat >> /private/tmp/claude-501/t136db/probe.py <<'EOF'\nimport sys; sys.path.insert(0,\".\")\nfrom app.db import db as DB\nconn=DB.connect(\"/private/tmp/claude-501/t136db/app.sqlite3\")\ne=next(x for x in c[\"entries\"] if x[\"id\"]==\"e2\"); r=recs[e[\"record_ids\"][0]]\nDB.update_item(conn,\"e2\",now=9e9,case=t,state=\"needs_review\",reasons=[\"JUDGE_UNAVAILABLE\"]); conn.close()\nc=api(\"GET\",f\"/api/cases/{t}\")[1]; e=next(x for x in c[\"entries\"] if x[\"id\"]==\"e2\"); print(e[\"state\"],e[\"reasons\"])\nsents=[s for s in r[\"sentences\"] if s[\"start\"]>=e[\"excerpt_start\"] and s[\"end\"]<=e[\"excerpt_end\"]]\nprint([s[\"text\"] for s in sents])\nnew=\" \".join(s[\"text\"] for s in sents[:-1]) if len(sents)>1 else None\nprint(api(\"POST\",f\"/api/cases/{t}/items/e2/review\",{\"action\":\"edit\",\"edits\":{\"excerpt\":new}}))\nEOF\n.venv/bin/python /private/tmp/claude-501/t136db/probe.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T12:33:02.599Z

**tool result**
````
x4dDdruLKQFbcwTf3kSSrQ
Traceback (most recent call last):
  File "/private/tmp/claude-501/t136db/probe.py", line 27, in <module>
    DB.update_item(conn,"e2",now=9e9,case=t,state="needs_review",reasons=["JUDGE_UNAVAILABLE"]); conn.close()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/wt-t136/app/db/db.py", line 209, in update_item
    raise ValueError(f"unknown {table} fields {sorted(bad)}")
ValueError: unknown entries fields ['reasons']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:05.066Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && sed -i 's/state=\"needs_review\",reasons=\\[\"JUDGE_UNAVAILABLE\"\\]/state=\"needs_review\"/' /private/tmp/claude-501/t136db/probe.py && .venv/bin/python /private/tmp/claude-501/t136db/probe.py 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T12:33:05.160Z

**tool result (error)**
````
Exit code 1
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/t136db/probe.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:06.584Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && sed -i '' 's/state=\"needs_review\",reasons=\\[\"JUDGE_UNAVAILABLE\"\\]/state=\"needs_review\"/' /private/tmp/claude-501/t136db/probe.py && .venv/bin/python /private/tmp/claude-501/t136db/probe.py 2>&1 | tail -6"
}
````

### User / tool · 2026-11-02T12:33:07.840Z

**tool result**
````
e9 verified pending False 2 1771 1876 []
{'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 3, 'verified': 20, 'rejected': 0, 'edit_to_check': 0}
z05sOSgidho4hBCAm1MjIQ
needs_review []
['Dx: cervical strain;', 'concussion without loss of consciousness.', 'CT head negative.', 'Rx cyclobenzaprine 10 mg.', 'Follow up with PCP in 1 week.']
(200, {'item': {'id': 'e2', 'state': 'needs_review', 'reasons': ['JUDGE_UNAVAILABLE'], 'why': 'The second AI check did not run or did not finish, so this item has not been double-checked.', 'review_status': 'edited', 'edited': {'at': '2026-11-02T12:33:07Z', 'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg.', 'excerpt_end': 502, 'excerpt_start': 396, 'original_excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'}, 'ladder': {'backend': 'fixture', 'code_checks': {'date_provider_from_header': True, 'excerpt_verbatim': True, 'excerpt_whole_sentence': True, 'highlight_found': True, 'qualifier_carried': True, 'summary_tokens_not_in_excerpt': []}, 'generator': {'call_id': 'c2af5041d74f4', 'model': 'claude-sonnet-5-5', 'output': {'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.', 'summary': 'Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.'}, 'prompt_version': 'extract_v1'}, 'human': {'action': 'edit', 'edited_text': None, 'at': '2026-11-02T12:33:07Z'}, 'item_id': 'e2', 'judge': {'call_id': None, 'error_class': 'LLMFailedFixtureMiss', 'model': 'claude-haiku-5-5', 'prompt_version': 'judge_faithfulness_v1', 'reason_code': 'NONE', 'verdict': 'unavailable'}, 'state': 'needs_review'}, 'seq': 2, 'record_ids': ['r2'], 'date': '2026-01-09', 'date_status': 'parsed', 'provider': 'Central ER discharge summary', 'summary': 'Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.', 'ai_drafted': True, 'entered_by_reviewer': False, 'entered_by': None, 'source_kind': 'record', 'excerpt': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg.', 'excerpt_start': 396, 'excerpt_end': 502, 'duplicate_note': None, 'translation': None, 'edit_to_check': True, 'kind': 'entry'}, 'totals': {'accepted': {'cents': 0, 'count': 0, 'label': 'Accepted charges'}, 'pending': {'cents': 839000, 'count': 2, 'label': 'Pending review'}, 'detected_not_a_total': {'cents': 839000, 'count': 2, 'label': 'Detected (not a total)'}, 'not_totaled': [{'id': 'a2', 'kind': 'rate', 'text': '$185'}], 'possible_overlaps': []}, 'review': {'counts': {'pending': 22, 'accepted': 0, 'edited': 1, 'dismissed': 0, 'needs_review': 4, 'verified': 19, 'rejected': 0, 'edit_to_check': 1}, 'queue': ['a2', 'a3', 'f_r7_1', 'a1', 'a4', 'e1', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'f_accident_date_after_treatment_1_2_7', 'f_cx1', 'f_gap_r6_r7', 'f_r3_1', 'f_r6_1', 'f_r7_2', 'f_r8_1', 'f_r8_2', 'f_r9_1'], 'ready_to_export': False}, 'warnings': [{'code': 'JUDGE_UNAVAILABLE', 'message': 'The second check was not available; the item stays marked for review.', 'item_id': 'e2'}]})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:12.964Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"data-testid\" excerpt.js | head -20; grep -n \"btn-change-quote\\|excerpt-editor\\|openPicker\\|ZL.excerpt\" review.js excerpt.js | head -20; sed -n 270,305p review.js"
}
````

### User / tool · 2026-11-02T12:33:13.064Z

**tool result**
````
12:    const f = p.panel.querySelector('[data-testid="excerpt-unit"]'); if (f) f.focus();
25:    const panel = el("form", { class: "ex-units", hidden: true, "data-testid": "excerpt-editor" });
26:    const msg = el("p", { class: "error", role: "alert", hidden: true, "data-testid": "excerpt-error" });
31:          el("input", { type: "checkbox", name: "unit", "data-testid": "excerpt-unit", value: String(i), checked: i >= lo && i <= hi, onchange: () => pick(i) }), " ", u.text)))),
32:        msg, el("div", { class: "row" }, el("button", { type: "submit", class: "btn btn--sm", "data-testid": "btn-save-excerpt" }, "Use these sentences"),
47:    if (bar) bar.append(el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-edit-excerpt", "aria-label": "Change quote: " + entry.provider + (entry.date ? ", " + entry.date : ""), onclick: () => { panel.hidden = !panel.hidden; } }, "Change quote"));
excerpt.js:25:    const panel = el("form", { class: "ex-units", hidden: true, "data-testid": "excerpt-editor" });
    const noted = kind === "amount" && item.kind !== "charge";
    const initial = isFlag ? (item.reviewer_note || (item.edited && item.edited.note) || "") : ((item.edited && item.edited.summary) || item.summary || "");
    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
    if (!d.open) d.text = initial;
    const lbl = RV.label(item);
    const root = el("div", { class: "rv-controls", "data-controls-for": id });
    const dismissed = st === "dismissed";
    // T-060 r5 (paralegal M2): a reworded entry that is still marked Needs review is not settled. Its one next step is to compare it with the quote and say so (an Accept on her own wording).
    const toCheck = ZL.editToCheck(item);
    const accepted = (st === "accepted" || st === "edited") && !toCheck;

    // T-060 r3: a decided row shows its state, not the action it already took. Primary (filled) is for an undecided item only; Accepted / Dismissed read as quiet state words, Undo is the way back.
    const VARIANT = { accept: st === "pending" || toCheck ? (noted ? "" : "btn--primary") : st === "dismissed" ? "" : "rv-decided", edit: "", dismiss: st === "dismissed" ? "rv-decided rv-decided--muted" : "btn--ghost", reset: "btn--link", audit: "btn--link", "dismiss-reason": "btn--link" };
    const btn = (action, text, tid, extra, name) => el("button", Object.assign({ type: "button", class: ("btn " + (VARIANT[action] || "") + " rv-" + action).replace("  ", " "), "data-testid": tid, "data-action": action, "aria-label": (name || text).replace("…", "") + ": " + lbl }, extra || {}), text);
    const bar = el("div", { class: "rv-actions", role: "group", "aria-label": "Review actions" });
    const blocked = RV.needsDate(item, kind) && st !== "accepted";
    const acceptText = toCheck ? "I compared it with the quote" : accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
    // a dismissed item keeps only its state word, Undo and Audit: no Accept, Keep in notes or Edit (the paralegal's M1: one key must not reverse a dismissal)
    if (!dismissed) bar.append(btn("accept", acceptText, "btn-accept", { "data-icon": accepted ? "check" : null, "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null,
      onclick: (ev) => { if (accepted) { RV.say(acceptText + " already. Use Undo to change it."); return; } RV.act(id, { action: "accept" }, ev.detail === 0 ? { advance: true } : { focus: "accept" }); } }));
    let form;
    if (canEdit && !dismissed) bar.append(btn("edit", isFlag ? "Edit note" : "Edit", "btn-edit", { onclick: () => toggleEdit(true), disabled: blocked }));
    bar.append(btn("dismiss", st === "dismissed" ? "Dismissed" : "Dismiss", "btn-dismiss", { "data-icon": st === "dismissed" ? "dash" : null, "aria-pressed": String(st === "dismissed"),
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.reasonOpen)); if (d.reasonOpen) reasonIn.focus(); } }));
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (toCheck && !rechecks[id]) root.append(el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, "Still marked Needs review. Compare your wording with the quote, then press the button to say you did. Until then it counts as open."));
    if (rechecks[id] && st === "edited") root.append(el("p", { class: "rv-recheck", "data-testid": "edit-recheck-note" }, rechecks[id]));
    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
      el("button", { type: "button", class: "btn btn--link", "data-testid": "link-confirm-date", onclick: () => goToDateRow(id) }, "Go to its date choices")));

    // dismiss reason (flags only; optional - R-RV-5)
    const reasonIn = el("input", { type: "text", id: "dr-" + id, class: "rv-input", maxlength: "300", "aria-label": "Reason for dismissing (optional)", "data-testid": "dismiss-reason", value: d.reason || "" });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:16.277Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 1,60p excerpt.js; grep -n \"recheckSentence\" -A12 review.js | head -30"
}
````

### User / tool · 2026-11-02T12:33:16.369Z

**tool result**
````
/* Change the quote of an entry (R-RV-2, D-012): pick a contiguous run of whole sentence units of the SAME record.
   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows the server's reasons. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  // T-104: other places (a refused Accept or edit, the Why dialog, the gate) open this picker for an item by id. Every rendering of the row registers its picker; the first one on the page opens.
  const pickers = {};
  ZL.openQuoteEditor = function (id) {
    const list = (pickers[id] = (pickers[id] || []).filter((p) => p.panel.isConnected));
    const p = list.find((x) => x.row.offsetParent !== null) || list[0];
    if (!p) return false;
    p.panel.hidden = false;
    const f = p.panel.querySelector('[data-testid="excerpt-unit"]'); if (f) f.focus();
    if (p.panel.scrollIntoView) p.panel.scrollIntoView({ block: "nearest" });
    return true;
  };
  ZL.hasQuoteEditor = (id) => !!(pickers[id] || []).some((p) => p.panel.isConnected);
  ZL.registerRowActions((entry, row) => {
    if (entry.state === "rejected") return;
    const rec = ZL.state.get().case.records.find((r) => r.id === entry.record_ids[0]);
    if (!rec || !rec.sentences || rec.sentences.length < 2 || entry.record_ids.length !== 1) return;
    const units = rec.sentences;
    let lo = units.findIndex((u) => u.start >= entry.excerpt_start && u.start < entry.excerpt_end), hi = -1;
    units.forEach((u, i) => { if (u.end > entry.excerpt_start && u.end <= entry.excerpt_end) hi = i; });
    if (lo < 0 || hi < lo) { lo = 0; hi = units.length - 1; }
    const panel = el("form", { class: "ex-units", hidden: true, "data-testid": "excerpt-editor" });
    const msg = el("p", { class: "error", role: "alert", hidden: true, "data-testid": "excerpt-error" });
    function draw() {
      clear(panel);
      panel.append(el("p", { class: "muted small" }, "Choose which sentences of this record the letter quotes. Only whole sentences of this record; a hedge that qualifies a chosen sentence has to stay."),
        el("ul", { class: "ex-unit-list" }, units.map((u, i) => el("li", {}, el("label", {},
          el("input", { type: "checkbox", name: "unit", "data-testid": "excerpt-unit", value: String(i), checked: i >= lo && i <= hi, onchange: () => pick(i) }), " ", u.text)))),
        msg, el("div", { class: "row" }, el("button", { type: "submit", class: "btn btn--sm", "data-testid": "btn-save-excerpt" }, "Use these sentences"),
          el("button", { type: "button", class: "btn btn--sm", onclick: () => { panel.hidden = true; } }, "Cancel")));
    }
    function pick(i) { if (i < lo) lo = i; else if (i > hi) hi = i; else if (i === lo && lo < hi) lo++; else if (i === hi && lo < hi) hi--; else hi = i; draw(); }
    panel.addEventListener("submit", async (ev) => {
      ev.preventDefault(); msg.hidden = true;
      const text = rec.text.slice(units[lo].start - rec.char_start, units[hi].end - rec.char_start);
      try { const resp = await ZL.api.review(ZL.state.get().token, entry.id, { action: "edit", edits: { excerpt: text } }); ZL.state.applyReview(resp); if (ZL.rv && ZL.rv.clearRefusal) ZL.rv.clearRefusal(entry.id); }
      catch (e) {
        msg.textContent = e.message + (e.detail && e.detail.warnings ? " " + e.detail.warnings.map((w) => w.message).join(" ") : ""); msg.hidden = false;
      }
    });
    draw();
    pickers[entry.id] = (pickers[entry.id] || []).filter((p) => p.panel.isConnected); pickers[entry.id].push({ panel, row });
    const bar = row.querySelector(".row-actions");
    if (bar) bar.append(el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-edit-excerpt", "aria-label": "Change quote: " + entry.provider + (entry.date ? ", " + entry.date : ""), onclick: () => { panel.hidden = !panel.hidden; } }, "Change quote"));
    row.append(panel);
  });
})();
167:  function recheckSentence(resp) {
168-    const w = (resp && resp.warnings) || [], st = resp && resp.item && resp.item.state;
169-    const lead = "Saved and re-checked. The code compared every number, date and negation in your wording with the quote and found no difference.";
170-    if (w.length) return lead + " " + w.map((x) => x.message).filter(Boolean).join(" ") + " Compare it with the quote yourself.";
171-    return lead + (st === "needs_review" ? " The entry still needs your review." : " The second AI check agreed.");
172-  }
173-
174-  // ---- errors (R-RV-3, D-034, D-047). A refused edit is a hard 422 whose plain-words reason is shown right under the edit box, which stays open with the typed text.
175-  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
176-  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
177-  // m2: a refused edit is tied to its field (aria-invalid + aria-describedby) as well as announced
178-  function markInvalid(id, s) { const ta = document.querySelector('[data-controls-for="' + id + '"] textarea'); if (!ta || !s) return; s.id = s.id || "rv-err-" + id; ta.setAttribute("aria-invalid", "true"); ta.setAttribute("aria-describedby", s.id); }
179-  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) { s.textContent = msg; markInvalid(id, s); } RV.say(msg, true); }
--
239:      if (body.action === "edit" && found && found.kind === "entry") rechecks[id] = recheckSentence(resp); else delete rechecks[id];
240-      if (body.action === "dismiss" && found && found.kind === "entry") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo
241-      ZL.state.applyReview(resp);
242-      if (rechecks[id]) RV.say(rechecks[id]);
243-      const left = resp.review && resp.review.counts ? resp.review.counts.pending : null;
244-      const verb = { accept: "Accepted", edit: "Saved edit to", dismiss: "Dismissed", reset: "Reset" }[body.action];
245-      RV.say(verb + ": " + (found ? RV.label(found.item) : id) + (left != null ? ". " + left + " left to review." : "."));
246-      restoreFocus(o.advance ? { nextFrom: id, plan } : o.focus ? { id, action: o.focus } : null);
247-      return true;
248-    } catch (e) {
249-      if (RV.isCodeCheckRefusal(e) && body.action === "edit") showEditRefusal(id, e);   // T-104: inline under the edit box, typed text kept, not the generic path
250-      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
251-        const d = e.detail || {}, ta0 = document.querySelector('[data-controls-for="' + id + '"] textarea'), typed = ta0 ? ta0.value : "";
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:30.458Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && sed -n 1030,1060p app/backend/trace.py; grep -n \"gotoFirstPending\" -B2 -A14 app/frontend/stepper.js | head -50; grep -n \"rawcode\\|RAW_CODE\\|REASON_TEXT\\|ITEMS_NOT_REVIEWED\" app/frontend/*.js | head"
}
````

### User / tool · 2026-11-02T12:33:30.677Z

**tool result**
````
    else:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
    # 10 export gate
    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers == []) == export allowed
    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    ccf = [b for b in blockers if b.get("step_id")]             # D-045(b): the paralegal's own wording fails a code check
    live_pending = [(k, x) for k, x in allitems if x["state"] != "rejected" and x["review_status"] == "pending"]
    n_edit = rv["counts"].get("edit_to_check", 0)                # T-134: reworded, still Needs review, not accepted: not in the letter, so it warns like a pending item
    n_pend = len(live_pending)                                  # D-045(a): pending items never reach the letter, so they warn, they do not block
    n_date = sum(1 for k, x in live_pending if review.date_unconfirmed(conn, case_id, k, x))
    ready = not blockers
    gate_counts = {"blocking": len(blockers), "pending_items": n_pend, "date_unconfirmed": n_date, "accepted": rv["counts"]["accepted"] + rv["counts"]["edited"] - n_edit, "edit_not_confirmed": n_edit,
                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
    warnings = [{"reason_code": "ITEMS_NOT_REVIEWED", "count": n_pend, "why": pending_warning(n_pend),
                 "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])}] if n_pend else []
    if n_edit:
        warnings.append({"reason_code": "EDIT_NOT_CONFIRMED", "count": n_edit, "why": edit_warning(n_edit), "next_action": na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])})
    if ready:
        gate = step("export_gate", "Ready to export?", "code", PASS,
                    "At least one item is accepted and every accepted item has its checks, so the export can be built." + (" " + pending_warning(n_pend) if n_pend else "")
                    + (" " + edit_warning(n_edit) if n_edit else ""),
                    rule="row 19", counts=gate_counts)
    else:
        first = blockers[0]
        text = (f"{len(jnr)} accepted item{'s have' if len(jnr) != 1 else ' has'} not been double-checked by the second AI check, so the export is blocked. Run the second check again."
                if jnr and first is jnr[0] else first["why"])
        gate = step("export_gate", "Ready to export?", "code", FAIL, text, reason=first["reason_code"], rule="row 19", counts=gate_counts, next_action=first["next_action"],
                    blocks=True)
    gate.update(ready=ready, blockers=blockers, warnings=warnings)
    st.append(gate)
    _number(st)
110-  }
111-  S.gotoPanel = gotoPanel;
112:  function gotoFirstPending() {
113-    closeDialogs();
114-    const node = document.querySelector('[data-testid="queue"] [data-item-id][data-review="pending"]') || document.querySelector('[data-item-id][data-review="pending"]') || document.querySelector('[data-testid="queue"]');
115-    if (!node) return false;
116-    reveal(node); return true;
117-  }
118-  function gotoTray() {
119-    closeDialogs();
120-    const node = document.querySelector('[data-testid="rejected-tray"]') || document.querySelector('[data-testid="queue"]');
121-    if (!node) return false;
122-    reveal(node); return true;
123-  }
124-  async function rerun(confirm, msgNode) {
125-    const s = ZL.state.get();
126-    try { msgNode.textContent = ""; await ZL.api.run(s.token, confirm); ZL.pollRun(); } catch (e) { msgNode.textContent = "The AI steps could not be started: " + e.message; }
--
217-  function gotoItem(id) {
218-    if (S.goto(id)) return true;
219:    return /^ns\d/.test(String(id)) ? gotoPanel("narrative") : gotoFirstPending();
220-  }
221-  // Opens the edit box of an item (the same path as pressing e on its row). Used by every "Edit your wording" action.
222-  S.editItem = function (id) {
223-    if (!gotoItem(id)) return false;
224-    const n = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
225-    if (n) n.dispatchEvent(new KeyboardEvent("keydown", { key: "e", bubbles: true }));
226-    return true;
227-  };
228-  // T-104: the first failing check is on the quote (next_action EDIT_QUOTE): the action is the quote picker (Change quote on the row), or the record itself when the row has no picker.
229-  S.changeQuote = function (id) {
230-    if (!gotoItem(id)) return false;
231-    if (ZL.openQuoteEditor && ZL.openQuoteEditor(id)) return true;
232-    openRecord(id, null); return true;
233-  };
--
235-    judges: ["Open the AI checks", () => gotoPanel("judges")],
236-    amounts: ["Go to the charges", () => gotoPanel("charges")],
237:    queue: ["Go to the first pending item", () => gotoFirstPending()],
238-    tray: ["Go to the could-not-verify items", () => gotoTray()],
239-    narrative: ["Go to the draft paragraph", () => gotoPanel("narrative")],
240-  };
241-  // Case-level steps say what to do with counts ("Review the 3 items the AI objected to"), not the item-level sentence.
242-  function caseCopy(st) {
243-    const c = st.counts || {};
244-    switch (st.id) {
245-      case "judges": {
246-        const obj = c.unsupported || 0, unsure = c.unsure || 0, un = c.unavailable || 0, cant = unsure + un;
247-        if (!obj && !cant) return null;
248-        const bits = [];
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:34.674Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && grep -n \"def edit_warning\" -A6 app/backend/*.py; sed -n 1018,1030p app/backend/trace.py; grep -n \"\\\"review\\\"\" app/frontend/stepper.js | head; grep -n \"step.reason\\|st.reason\\|reason_code\" app/frontend/stepper.js | head -20"
}
````

### User / tool · 2026-11-02T12:33:34.792Z

**tool result**
````
app/backend/trace.py:1072:def edit_warning(n: int) -> str:
app/backend/trace.py-1073-    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
app/backend/trace.py-1074-            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")
app/backend/trace.py-1075-
app/backend/trace.py-1076-
app/backend/trace.py-1077-def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
app/backend/trace.py-1078-    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    else:
        st.append(step("totals", "Billed-charges total", "code", PASS, "The total is added up by code from the accepted charges.", rule="row 8", counts=tcounts))
    # 9 review
    rc = {k: rv["counts"][k] for k in ("pending", "accepted", "edited", "dismissed", "edit_to_check")}
    if rc["pending"]:
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{rc['pending']} item{'s are' if rc['pending'] != 1 else ' is'} waiting for your decision.", reason="PENDING_DECISION",
                       rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    elif rc["edit_to_check"]:           # T-134: her reworded entry is still marked Needs review; it is not decided until she accepts it
        n = rc["edit_to_check"]
        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PENDING, f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm "
                       f"{'them' if n != 1 else 'it'}). Compare {'them' if n != 1 else 'it'} with the quote and accept, or the {'entries stay' if n != 1 else 'entry stays'} out of the letter.",
                       reason="EDIT_NOT_CONFIRMED", rule="row 17", counts=rc, next_action=na("DECIDE", {"view": "queue"}, ["accept", "edit", "dismiss"])))
    else:
258:      case "review": {
158:  const jnrBlockers = (g) => ((g && g.blockers) || []).filter((b) => b.reason_code === "JUDGE_NOT_RUN");
333:    if (st._notNeeded) { delete ev.judge_verdict; delete ev.rationale; delete ev.judge_reason_code; }   // "Not needed" must not also print "The second AI check said: Unavailable"
353:    tech.push(kv("reason code", st.reason_code), kv("rule", st.rule), kv("judge reason code", ev.judge_reason_code && ev.judge_reason_code !== "NONE" ? ev.judge_reason_code : null));
413:    const gated = !!gate && ((gate.blockers || []).some((b) => b.reason_code === "JUDGE_NOT_RUN" && b.item_id === tr.item_id));
418:      steps = steps.map((x) => (x.status === "skipped" && needsRerun(x) ? Object.assign({}, x, { _notNeeded: true, next_action: null, reason_code: null, why: HUMAN_NOTE }) : x));
477:    return el("li", { class: "zs-blocker", "data-testid": "gate-blocker", "data-blocker-code": b.reason_code, "data-jump-item": b.item_id || null },
495:    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
531:    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
566:    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
571:    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").length))));
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:36.271Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136/app/frontend && sed -n 250,275p stepper.js; sed -n 520,545p stepper.js; sed -n 95,111p stepper.js"
}
````

### User / tool · 2026-11-02T12:33:36.378Z

**tool result**
````
        if (unsure) bits.push("The AI could not decide " + plural(unsure, "item", "items") + "; read " + (unsure === 1 ? "it" : "them") + " yourself.");
        if (un) bits.push("The second AI check did not run on " + plural(un, "item", "items") + ". Run it again; accepted items it never checked cannot go in the letter.");
        return { text: bits.join(" "), label: obj ? "Review the " + plural(obj, "item", "items") + " the AI objected to" : "Show the " + plural(cant, "item", "items") + " the AI could not check", go: () => gotoPanel("judges"), rerun: un > 0 };
      }
      case "totals": {
        const n = c.pending_charges || 0;
        return { text: "Decide the " + plural(n, "detected charge", "detected charges") + ": accept the ones that are billed charges, dismiss the rest. The total counts accepted charges only.", label: "Go to the totals", go: () => gotoPanel("charges") };
      }
      case "review": {
        const n = c.pending || 0;
        return { text: "Decide the " + plural(n, "pending item", "pending items") + ": accept, edit or dismiss each one.", label: "Go to the first pending item", go: () => gotoFirstPending() };
      }
      case "export_gate": {
        const bl = st.blockers || [], n = c.blocking || bl.length, jnr = jnrBlockers(st);
        if (!bl.length) return null;
        const b = firstBlocker(bl);
        if (!b && !jnr.length) return null;     // only whole-case blockers (nothing accepted, run state): the step's own action (go to the queue) says it
        const text = jnr.length ? plural(jnr.length, "accepted item", "accepted items") + " never got the second AI check, so the export is blocked. Run the second check again; if it still cannot answer, dismiss " + (jnr.length === 1 ? "that item" : "those items") + "."
          : "Settle the " + plural(n, "blocker", "blockers") + " listed here and the export opens.";
        return { text, label: "Go to the first blocking item", go: b ? () => gotoItem(b.item_id) : null, rerun: jnr.length > 0 };
      }
      default: return null;
    }
  }
  // The first blocker in QUEUE order, so "Go to the first blocking item" lands where "Go to the first pending item" would.
  const queueIds = () => Array.from(document.querySelectorAll('[data-testid="queue"] [data-item-id]')).map((n) => n.getAttribute("data-item-id"));
      el("ol", { class: "zs-rail", "aria-label": "Case checks, from reading the paste to the export gate" }, steps.map((s, i) => stepNode(s, i === act, ctx))),
      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet, or waiting for you. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “AI” steps by a model, “You” steps are your decisions."));
  }
  // The one-line summary: how many checks passed, how many need the human, and what the export is waiting for.
  function summaryBits(steps) {
    const passed = steps.filter((s) => s.status === "pass").length, need = steps.filter((s) => s.status === "fail" || s.status === "pending").length;
    const gate = steps.find((s) => s.id === "export_gate"), bl = (gate && gate.blockers) || [];
    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
    let gateText = "";
    const warned = ((gate && gate.warnings) || []).reduce((t, w) => t + (w.count || 0), 0);
    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
    else if (gate) gateText = "Export blocked by " + (n || 1);
    return { passed, need, gateText, total: steps.length };
  }
  function paintCase(host, tr) {
    clear(host);
    const steps = tr ? tr.steps || [] : [], sb = summaryBits(steps);
    const toggle = el("span", { class: "zs-toggle", "aria-hidden": "true" }, "Show");
    const sum = el("summary", { "data-testid": "case-summary" }, el("span", { class: "zs-case-title" }, "Case checks"),
      tr ? [el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, sb.passed + "/" + sb.total + " checks passed"),
        sb.gateText === "Ready to export" ? (sb.total - sb.passed ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, (sb.total - sb.passed) + (sb.total - sb.passed === 1 ? " check was not run" : " checks were not run")) : null)
          : sb.need ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, sb.need + " need you") : null,
        sb.gateText ? el("span", { class: "zs-sumv zs-sumgate", "data-testid": "case-summary-gate" }, sb.gateText) : null] : el("span", { class: "zs-progress", "data-testid": "case-summary-progress" }, "loading…"), toggle);
    const det = el("details", { class: "zs-case-det" }, sum, tr ? caseRail(tr) : el("p", { class: "muted", role: "status" }, "Loading the case checks…"));
    det.open = !!openPref;
    if (!node) return false;
    reveal(node); return true;
  };
  function gotoDates(recordId) {
    closeDialogs();
    const node = (recordId && document.querySelector('[data-testid="date-to-confirm-item"][data-record-id="' + recordId + '"]')) ||
      (recordId && document.querySelector('[data-record-id="' + recordId + '"]')) || document.querySelector('[data-testid="dates-to-confirm"]');
    if (node) reveal(node);
  }
  function gotoPanel(name) {
    closeDialogs();
    const node = document.querySelector('[data-panel="' + name + '"]:not([hidden])') || document.querySelector('[data-testid="queue"]');
    if (!node) return false;
    node.querySelectorAll("details[data-open-on-jump]").forEach((d) => { d.open = true; });
    reveal(node); return true;
  }
  S.gotoPanel = gotoPanel;
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:39.879Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136/app/frontend && grep -n \"warningNode\\|gateNode\\|S.gateBlock\\|gate-warnings\" *.js | head -20; sed -n 546,600p stepper.js; grep -n \"gate-warning\\|gate-warnings\" ../../tests/e2e/*.py | head"
}
````

### User / tool · 2026-11-02T12:33:39.984Z

**tool result**
````
stepper.js:492:  function warningNode(st) {
stepper.js:495:    return el("div", { class: "zs-gate-warns", "data-testid": "gate-warnings" }, ws.map((w) => el("div", { class: "zs-warnbox", "data-testid": "gate-warning", "data-warning-code": w.reason_code },
stepper.js:500:  function gateNode(st) {
stepper.js:502:    const a = bl.length ? blockerList(bl) : null, w = warningNode(st), said = rerunNote && rerunNote.token === (ZL.state.get() || {}).token;
stepper.js:506:    if (st.id === "export_gate") return gateNode(st);
    toggle.textContent = det.open ? "Hide" : "Show";
    det.addEventListener("toggle", () => { openPref = det.open; toggle.textContent = det.open ? "Hide" : "Show"; });
    host.append(det); curDet = det;
    // "What you need to do", visible without opening the checks: the next step that waits on the human, in the words the rail uses (T-060, paralegal F2).
    const i = tr ? activeIndex(steps) : -1, st = i >= 0 ? steps[i] : null, na = st && st.next_action;
    if (st && na) {
      const cc = caseCopy(st), text = (cc && cc.text) || na.text || "";
      if (text) host.append(el("div", { class: "zs-nextline", "data-testid": "case-next-action" },
        el("p", {}, el("strong", {}, "What you need to do: "), text),
        el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-show-next-step", onclick: () => { det.open = true; const n = det.querySelector('[data-step-id="' + st.id + '"]') || det; n.scrollIntoView({ block: "center" }); flash(n); } }, "Show this step")));
    }
  }
  // ---- the message beside the Export button. A refused export (422 judge_not_run / export_blocked) is shown right under the toolbar, scrolled into view and
  // focused, with the same Go to item list as the gate and the rerun button; never in the Export view 12,000 px further down.
  let blocked = null, curNotice = null;   // blocked: {token, message, blockers[], cleared}
  function paintNotice(host) {
    clear(host);
    const s = ZL.state.get();
    if (!blocked || blocked.token !== s.token) { host.hidden = true; return; }
    host.hidden = false;
    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
    host.className = "zs-exnote" + (blocked.cleared ? " zs-exnote-ok" : "");
    host.append(el("p", { class: "zs-exnote-msg", role: blocked.cleared ? "status" : "alert", "data-testid": "export-blocked-msg" }, el("strong", {}, blocked.cleared ? "Nothing blocks the export now. " : "The export is blocked. "), (blocked.message || "").replace(/\s*The export is blocked\.?\s*$/i, "")));
    // The rerun button and its Running… / result sentence sit together right under the lead sentence, above the (possibly long) blocker list, so the answer is
    // where the pressed button is. The same status node serves the cleared message.
    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").length))));
    host.append(rerunStatus());
    // the lead sentence already says it when it carries the blockers' own wording: say it once (T-060 r3, paralegal F8)
    const said = (blocked.message || "").replace(/\s+/g, " ");
    const dup = bl.length > 0 && bl.every((b) => b.why && said.includes(String(b.why).replace(/\s+/g, " ").trim()) && !isCodeBlocker(b));
    if (!blocked.cleared && bl.length) host.append(blockerList(bl, null, dup));
    host.append(el("div", { class: "zs-todo-btns" }, el("button", { type: "button", class: "btn", "data-testid": "btn-export-blocked-close", onclick: () => { blocked = null; paintNotice(host); const b = ZL.$('[data-testid="btn-export"]'); if (b) b.focus(); } }, "Close this message")));
  }
  S.exportNotice = function () {
    const host = el("section", { "data-testid": "export-blocked", tabindex: "-1", "aria-label": "Why the export is blocked" });
    curNotice = host; paintNotice(host); return host;
  };
  S.showExportBlocked = function (err, reveal_) {
    const s = ZL.state.get();
    const d = (err && err.detail) || {};
    blocked = { token: s.token, message: (err && err.message) || "The export could not be built.", blockers: d.blockers || [] };
    if (!curNotice || !curNotice.isConnected) return false;
    paintNotice(curNotice);
    if (reveal_ !== false) {
      reveal(curNotice);
      const b = ZL.$('[data-testid="btn-export"]'), r = b && b.getBoundingClientRect();   // the button this message explains stays in view with it, so Export can be pressed again
      if (r && (r.top < 0 || r.bottom > window.innerHeight)) b.scrollIntoView({ block: "start" });
    }
    return true;
  };
  // The message must not outlive its cause: after any decision, ask the server again (GET /export has no side effects). Blockers gone -> "Nothing blocks the export now";
  // still blocked -> the current list.
  let reTimer = null;
  ZL.state.subscribe((st) => {
    if (!blocked || blocked.cleared || !st.case) return;
../../tests/e2e/conftest.py:23:  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
../../tests/e2e/test_rerun_judge.py:39:    w = gate.get_by_test_id("gate-warning"); expect(w).to_have_attribute("data-warning-code", "ITEMS_NOT_REVIEWED")
../../tests/e2e/test_rerun_judge.py:43:    w.get_by_test_id("btn-gate-warning-jump").click()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:44.946Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && sed -n 1,60p tests/e2e/test_rerun_judge.py; sed -n 60,70p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T12:33:45.036Z

**tool result**
````
"""T-081 / T-082 round 3 (D-044, D-045): 'Run the second check again', the refused export shown beside the Export button, and pending items as a gate warning.
The fixture backend cannot leave an accepted recorded item without a judge answer, so those states are produced by the JudgeNotRun route-rewriting stub (conftest);
the pending-warning tests use the real backend."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, JudgeNotRun, WordingFails
from tests.e2e.test_stepper import open_rail, open_judges, active_in


def _accept(tok, n=3):
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] != "rejected" and e["date"]][:n]
    assert len(ids) == n
    for i in ids:
        assert api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "accept"})[0] == 200
    return ids


@pytest.fixture
def unrun(page, sample_case):
    """Three accepted entries whose second check 'never ran'; rejudge clears them."""
    ids = _accept(sample_case)
    return JudgeNotRun(page, sample_case, ids)


def in_view(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + min(b["height"], 40) <= vh


# ---- D-045: pending items are a warning, not a blocker
def test_pending_items_are_a_warning_not_a_blocker(page, sample_case):
    _accept(sample_case)
    open_case(page, sample_case); cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]')
    expect(gate).to_have_attribute("data-status", "pass")
    assert gate.get_by_test_id("gate-blocker").count() == 0
    w = gate.get_by_test_id("gate-warning"); expect(w).to_have_attribute("data-warning-code", "ITEMS_NOT_REVIEWED")
    txt = w.inner_text().lower()
    assert "not reviewed" in txt and "will not be in the letter" in txt and "disclosure" in txt and "does not block" in txt
    assert re.search(r"Ready to export, \d+ not reviewed", cs.get_by_test_id("case-summary-gate").inner_text())
    w.get_by_test_id("btn-gate-warning-jump").click()
    assert page.evaluate("document.activeElement.getAttribute('data-review')") == "pending"
    page.get_by_test_id("btn-export").click()                      # the export opens even though items are pending
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    assert page.get_by_test_id("export-blocked").is_hidden()


def test_export_with_nothing_accepted_says_so_beside_the_button(page, sample_case):
    """422 export_blocked (nothing accepted): the message sits right under the toolbar, in view, focused; the rail stays as the human left it."""
    open_case(page, sample_case)
    page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-blocked"); expect(box).to_be_visible()
    assert "nothing is accepted" in box.get_by_test_id("export-blocked-msg").inner_text().lower()
    assert in_view(page, box) and active_in(page, '[data-testid="export-blocked"]')
    assert page.get_by_test_id("btn-export").is_visible() and in_view(page, page.get_by_test_id("btn-export"))
    assert page.locator("#view-export").is_hidden()
    assert page.get_by_test_id("case-stepper").locator("details.zs-case-det").evaluate("d => d.open") is False
    box.get_by_test_id("btn-export-blocked-close").click(); expect(box).to_be_hidden()
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
  edit-check-hint (a reworded entry that is still marked Needs review: its btn-accept reads 'I compared it with the quote'; the row carries data-edit-check; it counts as open in the header, todo-list ('1 edit to check') and the copy-confirm),
  letter-style (fieldset in the export panel) with letter-style-standard / letter-style-oneline radios (T-121: ?style=oneline), tray-filtered (collapsed <details> 'Filtered by rule (n)', D-057) with tray-filtered-summary,
  tray-filtered-rule (one per rule, data-rule) and tray-filtered-item; data-group = the list a row sits in (flag kind on the flag sections, 'charges' / 'unclear-amounts' on the amount tables): a / d move only inside it.
  A dismissed flag / amount / entry has NO btn-accept and no btn-edit (state word 'Dismissed' + btn-reset 'Undo'); entry-date is a <time datetime="YYYY-MM-DD"> showing the long date.
"""
import json, os, urllib.request, urllib.error
import pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:53.793Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && sed -n 1,40p tests/e2e/test_code_check_refusal.py | head -50; sed -n 14,30p tests/e2e/test_stepper.py; grep -n \"def open_rail\" -A8 tests/e2e/test_stepper.py"
}
````

### User / tool · 2026-11-02T12:33:53.905Z

**tool result**
````
"""T-097 round 3 (D-051, T-098 r2): Accept (single and batch) can be refused with 422 CODE_CHECK_FAILED. The UI shows the server's plain reason next to the item's Accept button
with an Edit action, and for a batch lists the items it refused; nothing is accepted. Each test runs twice: against the REAL backend (needs ZLAYT_DB, the SQLite file of the server
under test, to put a failing summary into the store the way a stale or imported state would) and against a route stub that answers exactly as memory/contracts/api.md says."""
import json
import os
import re
import sys
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REASON = "The summary has a number that is not in the quote: 5. Edit the summary to match the quote."
NEXT = {"code": "EDIT_SUMMARY", "text": "Edit the summary to match the quote"}


def _entry(tok, eid):
    c = api("GET", f"/api/cases/{tok}")[1]
    return next(e for e in c["entries"] + c["undated_entries"] if e["id"] == eid)


def _break(tok, eid):
    """Real backend: put 'Pain 5/10' (a figure the quote does not carry) into the stored summary, like a stale or imported state."""
    path = os.environ.get("ZLAYT_DB")
    if not path:
        pytest.skip("the real-backend variant needs ZLAYT_DB (the SQLite file of the server under test)")
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        assert "5/10" not in (_entry(tok, eid)["excerpt"] or "")
        DB.update_item(conn, eid, now=9e9, case=tok, summary="Pain 5/10")
    finally:
        conn.close()


class Refuse:
    """Stub: POST .../review (accept) and POST .../review/batch (accept) answer 422 CODE_CHECK_FAILED while the item's summary is unchanged (an edit through the real route lifts it)."""
    def __init__(self, tok, eid):
        self.tok, self.eid = tok, eid
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def judged_case():
    """Library L6: three judge objections (two amounts, one flag) and several code-vs-AI disagreements. Local mode only."""
    st, c = api("POST", "/api/cases", {"library": "case_lib06_lop_billed_vs_adjusted"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")

32:def open_rail(page):
33-    """The case checks are collapsed to one line by default; open them like a user does."""
34-    cs = page.get_by_test_id("case-stepper"); cs.get_by_test_id("case-summary").wait_for()
35-    if not cs.locator("details.zs-case-det").evaluate("d => d.open"):
36-        cs.get_by_test_id("case-summary").click()
37-    cs.get_by_test_id("case-step").first.wait_for()
38-    return cs
39-
40-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:33:55.237Z

Now the tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:34:16.197Z

**tool call — Write**
````
{
 "command": "/Users/arsis/zlayt-pm-project/tests/e2e/test_edit_to_check.py",
 "file_text": "\"\"\"T-136 (frontend; backend T-134, D-045b, D-051): the UI reads the item's own `edit_to_check` and the review's `counts.edit_to_check`, not a summary-only guess.\nAn edit made with the quote picker (excerpt only, no edited summary) on an entry that is still Needs review is open: its Accept reads \"I compared it with the quote\", the header,\nthe Open-decisions strip and the copy-confirm count it, the export stepper shows the gate warning EDIT_NOT_CONFIRMED in its plain reason, and the Accept clears all of it.\nReal backend; needs ZLAYT_DB (the SQLite file of the server under test) to put the entry into Needs review the way a missing second check does (the fixture set verifies every entry).\nNo new test ids: btn-edit-excerpt, excerpt-unit, btn-save-excerpt, btn-accept, edit-check-hint, todo-list, copy-confirm, gate-warning, btn-gate-warning-jump (all declared in conftest).\"\"\"\nimport os\nimport re\nimport sys\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case\nfrom tests.e2e.test_stepper import open_rail\n\nROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"..\"))\nRAW_CODE = re.compile(r\"\\b[A-Z]{3,}(?:_[A-Z]+)+\\b\")\n\n\ndef _case(tok):\n    return api(\"GET\", f\"/api/cases/{tok}\")[1]\n\n\ndef _needs_review_entry_with_picker(tok):\n    \"\"\"Put a dated, pending entry whose record has several sentences into Needs review (store write) and return it with its record.\"\"\"\n    path = os.environ.get(\"ZLAYT_DB\")\n    if not path:\n        pytest.skip(\"needs ZLAYT_DB (the SQLite file of the server under test)\")\n    c = _case(tok); recs = {r[\"id\"]: r for r in c[\"records\"]}\n    e = next(x for x in c[\"entries\"] if x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\" and len(x[\"record_ids\"]) == 1 and len(recs[x[\"record_ids\"][0]][\"sentences\"]) >= 3)\n    sys.path.insert(0, ROOT)\n    from app.db import db as DB\n    conn = DB.connect(path)\n    try:\n        DB.update_item(conn, e[\"id\"], now=9e9, case=tok, state=\"needs_review\")\n    finally:\n        conn.close()\n    return e, recs[e[\"record_ids\"][0]]\n\n\ndef _progress(page):\n    t = page.locator(\"#progress-text\").inner_text()\n    m = re.match(r\"(\\d+) of (\\d+) decided(?: · (\\d+) items? needs? review(?:, including (\\d+) edits? to check)?)?\", t)\n    assert m, t\n    return int(m.group(1)), int(m.group(2)), int(m.group(3) or 0), int(m.group(4) or 0)\n\n\ndef _quote_edit(page, row):\n    \"\"\"Use the quote picker the way a paralegal does: open Change quote, drop the last sentence, Use these sentences. No summary is edited.\"\"\"\n    row.get_by_test_id(\"btn-edit-excerpt\").click()\n    ed = row.get_by_test_id(\"excerpt-editor\"); expect(ed).to_be_visible()\n    units = ed.get_by_test_id(\"excerpt-unit\")\n    last = max(i for i in range(units.count()) if units.nth(i).is_checked())\n    units.nth(last).click()\n    ed.get_by_test_id(\"btn-save-excerpt\").click()\n\n\n@pytest.fixture\ndef edited_quote(page, sample_case):\n    e, rec = _needs_review_entry_with_picker(sample_case)\n    open_case(page, sample_case)\n    row = page.locator(f'[data-testid=queue] [data-item-id=\"{e[\"id\"]}\"], [data-testid=timeline] [data-item-id=\"{e[\"id\"]}\"]').first\n    row.scroll_into_view_if_needed()\n    before = _progress(page)\n    _quote_edit(page, row)\n    expect(row).to_have_attribute(\"data-review\", \"edited\")\n    return {\"tok\": sample_case, \"id\": e[\"id\"], \"row\": row, \"before\": before, \"orig\": e[\"excerpt\"]}\n\n\ndef test_a_quote_only_edit_is_open_and_offers_the_compare_accept(page, edited_quote):\n    t = edited_quote; row = t[\"row\"]\n    got = next(x for x in _case(t[\"tok\"])[\"entries\"] if x[\"id\"] == t[\"id\"])\n    assert got[\"excerpt\"] != t[\"orig\"] and got[\"edit_to_check\"] is True and not (got.get(\"edited\") or {}).get(\"summary\"), \"the setup is a quote-only edit\"\n    assert row.get_attribute(\"data-edit-check\") is not None\n    ok = row.get_by_test_id(\"btn-accept\"); expect(ok).to_contain_text(\"I compared it with the quote\"); assert \"btn--primary\" in ok.get_attribute(\"class\")\n    hint = row.get_by_test_id(\"edit-check-hint\"); expect(hint).to_be_visible()\n    assert \"quote\" in hint.inner_text().lower() and not RAW_CODE.search(hint.inner_text())\n\n\ndef test_header_strip_and_server_count_agree_on_a_quote_only_edit(page, edited_quote):\n    t = edited_quote\n    server = _case(t[\"tok\"])[\"review\"][\"counts\"][\"edit_to_check\"]; assert server == 1\n    d0, total0, n0, _ = t[\"before\"]\n    d1, total1, n1, k1 = _progress(page)\n    assert d1 == d0, \"an edit that is still Needs review was counted as decided\"\n    assert k1 == server and n1 >= 1, (n1, k1)\n    strip = page.get_by_test_id(\"todo-list\").inner_text()\n    assert re.search(rf\"{server} edit to check\", strip), strip\n    assert page.get_by_test_id(\"need-review-count\").inner_text().startswith(str(n1))\n\n\ndef test_the_server_count_is_the_one_the_ui_shows(page, sample_case):\n    \"\"\"The UI shows review.counts.edit_to_check as sent: a stubbed count of 2 over a case with one open edit reads 2 in the header and the strip (the UI adds nothing of its own).\"\"\"\n    e, rec = _needs_review_entry_with_picker(sample_case)\n    assert api(\"POST\", f\"/api/cases/{sample_case}/items/{e['id']}/review\", {\"action\": \"edit\", \"edits\": {\"excerpt\": \" \".join(s[\"text\"] for s in rec[\"sentences\"][:2] if s[\"start\"] >= e[\"excerpt_start\"] and s[\"end\"] <= e[\"excerpt_end\"]) or e[\"excerpt\"]}})[0] in (200, 422)\n    c = _case(sample_case)\n    if c[\"review\"][\"counts\"][\"edit_to_check\"] != 1:\n        pytest.skip(\"the edit did not leave an open edit on this backend\")\n    open_case(page, sample_case)\n    assert _progress(page)[3] == 1\n    assert re.search(r\"1 edit to check\", page.get_by_test_id(\"todo-list\").inner_text())\n\n\ndef test_the_export_stepper_shows_the_gate_warning_in_plain_words(page, edited_quote):\n    t = edited_quote\n    api(\"POST\", f\"/api/cases/{t['tok']}/items/e1/review\", {\"action\": \"accept\"})      # something is in the letter, so the gate is ready with a warning\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    cs = open_rail(page)\n    gate = cs.locator('[data-step-id=\"export_gate\"]'); expect(gate).to_have_attribute(\"data-status\", \"pass\")\n    w = gate.locator('[data-warning-code=\"EDIT_NOT_CONFIRMED\"]'); expect(w).to_have_count(1)\n    txt = w.inner_text()\n    assert \"1\" in txt and \"not in the letter\" in txt.lower() and \"quote\" in txt.lower() and \"does not block\" in txt.lower(), txt\n    assert not RAW_CODE.search(txt), txt\n    assert gate.locator('[data-warning-code=\"ITEMS_NOT_REVIEWED\"]').count() in (0, 1)\n    review = cs.locator('[data-step-id=\"review\"]')\n    assert \"pending item\" not in review.inner_text().lower() or \"0 pending\" not in review.inner_text().lower()\n    w.get_by_test_id(\"btn-gate-warning-jump\").click()\n    assert page.evaluate(\"document.activeElement.closest('[data-item-id]') && document.activeElement.closest('[data-item-id]').hasAttribute('data-edit-check')\"), \"the jump lands on the edit to check\"\n    assert \"edit\" in w.get_by_test_id(\"btn-gate-warning-jump\").inner_text().lower()\n\n\ndef test_case_checks_next_step_names_the_edit_not_a_pending_item(page, edited_quote):\n    t = edited_quote\n    for i in [e[\"id\"] for e in _case(t[\"tok\"])[\"entries\"] + _case(t[\"tok\"])[\"amounts\"] + _case(t[\"tok\"])[\"flags\"] if e[\"review_status\"] == \"pending\" and e[\"state\"] != \"rejected\"]:\n        api(\"POST\", f\"/api/cases/{t['tok']}/items/{i}/review\", {\"action\": \"dismiss\"})\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    nxt = page.get_by_test_id(\"case-next-action\"); expect(nxt).to_be_visible()\n    txt = nxt.inner_text().lower()\n    assert \"0 pending\" not in txt and \"edit\" in txt and \"quote\" in txt, txt\n\n\ndef test_the_edit_is_named_before_the_letter_is_copied(page, edited_quote):\n    t = edited_quote\n    api(\"POST\", f\"/api/cases/{t['tok']}/items/e1/review\", {\"action\": \"accept\"})\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    page.get_by_test_id(\"btn-export\").click(); page.get_by_test_id(\"btn-copy-letter\").click()\n    expect(page.get_by_test_id(\"copy-confirm\")).to_contain_text(\"1 edited entry still marked Needs review\")\n\n\ndef test_comparing_it_with_the_quote_closes_everything(page, edited_quote):\n    t = edited_quote; row = t[\"row\"]\n    api(\"POST\", f\"/api/cases/{t['tok']}/items/e1/review\", {\"action\": \"accept\"})\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    row = page.locator(f'[data-testid=queue] [data-item-id=\"{t[\"id\"]}\"], [data-testid=timeline] [data-item-id=\"{t[\"id\"]}\"]').first\n    d0, _, n0, k0 = _progress(page); assert k0 == 1\n    row.get_by_test_id(\"btn-accept\").click()\n    expect(row).to_have_attribute(\"data-review\", \"accepted\"); assert row.get_attribute(\"data-edit-check\") is None\n    d1, _, n1, k1 = _progress(page)\n    assert d1 == d0 + 1 and k1 == 0 and n1 == n0 - 1, ((d0, n0, k0), (d1, n1, k1))\n    assert _case(t[\"tok\"])[\"review\"][\"counts\"][\"edit_to_check\"] == 0\n    assert \"edit to check\" not in page.get_by_test_id(\"todo-list\").inner_text()\n    cs = open_rail(page)\n    assert cs.locator('[data-warning-code=\"EDIT_NOT_CONFIRMED\"]').count() == 0\n"
}
````

### User / tool · 2026-11-02T12:34:16.199Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Write failed due to the following issues:
The required parameter `file_path` is missing
The required parameter `content` is missing
An unexpected parameter `command` was provided
An unexpected parameter `file_text` was provided</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:34:33.815Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/e2e/test_edit_to_check.py",
 "content": "\"\"\"T-136 (frontend; backend T-134, D-045b, D-051): the UI reads the item's own `edit_to_check` and the review's `counts.edit_to_check`, not a summary-only guess.\nAn edit made with the quote picker (excerpt only, no edited summary) on an entry that is still Needs review is open: its Accept reads \"I compared it with the quote\", the header,\nthe Open-decisions strip and the copy-confirm count it, the export stepper shows the gate warning EDIT_NOT_CONFIRMED in its plain reason, and the Accept clears all of it.\nReal backend; needs ZLAYT_DB (the SQLite file of the server under test) to put the entry into Needs review the way a missing second check does (the fixture set verifies every entry).\nNo new test ids: btn-edit-excerpt, excerpt-unit, btn-save-excerpt, btn-accept, edit-check-hint, todo-list, need-review-count, case-next-action, copy-confirm, gate-warning,\nbtn-gate-warning-jump (all declared in conftest).\"\"\"\nimport os\nimport re\nimport sys\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case\nfrom tests.e2e.test_stepper import open_rail\n\nROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\", \"..\"))\nRAW_CODE = re.compile(r\"\\b[A-Z]{3,}(?:_[A-Z]+)+\\b\")\n\n\ndef _case(tok):\n    return api(\"GET\", f\"/api/cases/{tok}\")[1]\n\n\ndef _needs_review_entry_with_picker(tok):\n    \"\"\"Put a dated, pending entry whose record has several sentences into Needs review (store write, like a missing second check) and return it.\"\"\"\n    path = os.environ.get(\"ZLAYT_DB\")\n    if not path:\n        pytest.skip(\"needs ZLAYT_DB (the SQLite file of the server under test)\")\n    c = _case(tok); recs = {r[\"id\"]: r for r in c[\"records\"]}\n    e = next(x for x in c[\"entries\"] if x[\"id\"] != \"e1\" and x[\"state\"] == \"verified\" and x[\"date\"] and x[\"review_status\"] == \"pending\" and len(x[\"record_ids\"]) == 1\n             and len([s for s in recs[x[\"record_ids\"][0]][\"sentences\"] if s[\"start\"] >= x[\"excerpt_start\"] and s[\"end\"] <= x[\"excerpt_end\"]]) >= 2)\n    sys.path.insert(0, ROOT)\n    from app.db import db as DB\n    conn = DB.connect(path)\n    try:\n        DB.update_item(conn, e[\"id\"], now=9e9, case=tok, state=\"needs_review\")\n    finally:\n        conn.close()\n    return e\n\n\ndef _progress(page):\n    t = page.locator(\"#progress-text\").inner_text()\n    m = re.match(r\"(\\d+) of (\\d+) decided(?: · (\\d+) items? needs? review(?:, including (\\d+) edits? to check)?)?\", t)\n    assert m, t\n    return int(m.group(1)), int(m.group(2)), int(m.group(3) or 0), int(m.group(4) or 0)\n\n\ndef _row(page, eid):\n    return page.locator(f'[data-testid=queue] [data-item-id=\"{eid}\"], [data-testid=timeline] [data-item-id=\"{eid}\"]').first\n\n\ndef _quote_edit(row):\n    \"\"\"Use the quote picker the way a paralegal does: Change quote, drop the last chosen sentence, Use these sentences. No summary is edited.\"\"\"\n    row.get_by_test_id(\"btn-edit-excerpt\").click()\n    ed = row.get_by_test_id(\"excerpt-editor\"); expect(ed).to_be_visible()\n    units = ed.get_by_test_id(\"excerpt-unit\")\n    last = max(i for i in range(units.count()) if units.nth(i).is_checked())\n    units.nth(last).click()\n    ed.get_by_test_id(\"btn-save-excerpt\").click()\n\n\n@pytest.fixture\ndef edited_quote(page, sample_case):\n    e = _needs_review_entry_with_picker(sample_case)\n    open_case(page, sample_case)\n    row = _row(page, e[\"id\"]); row.scroll_into_view_if_needed()\n    before = _progress(page)\n    _quote_edit(row)\n    expect(row).to_have_attribute(\"data-review\", \"edited\")\n    return {\"tok\": sample_case, \"id\": e[\"id\"], \"before\": before, \"orig\": e[\"excerpt\"]}\n\n\ndef _accept_something_else(t):\n    assert api(\"POST\", f\"/api/cases/{t['tok']}/items/e1/review\", {\"action\": \"accept\"})[0] == 200      # the letter has one entry, so the gate is ready with a warning\n\n\ndef test_a_quote_only_edit_is_open_and_offers_the_compare_accept(page, edited_quote):\n    t = edited_quote; row = _row(page, t[\"id\"])\n    got = next(x for x in _case(t[\"tok\"])[\"entries\"] if x[\"id\"] == t[\"id\"])\n    assert got[\"excerpt\"] != t[\"orig\"] and got[\"edit_to_check\"] is True and not (got.get(\"edited\") or {}).get(\"summary\"), \"the setup is a quote-only edit\"\n    assert row.get_attribute(\"data-edit-check\") is not None\n    ok = row.get_by_test_id(\"btn-accept\"); expect(ok).to_contain_text(\"I compared it with the quote\"); assert \"btn--primary\" in ok.get_attribute(\"class\")\n    hint = row.get_by_test_id(\"edit-check-hint\"); expect(hint).to_be_visible()\n    assert \"quote\" in hint.inner_text().lower() and not RAW_CODE.search(hint.inner_text())\n\n\ndef test_header_and_strip_use_the_servers_edit_count(page, edited_quote):\n    t = edited_quote\n    server = _case(t[\"tok\"])[\"review\"][\"counts\"][\"edit_to_check\"]; assert server == 1\n    d0, _, n0, _ = t[\"before\"]\n    d1, _, n1, k1 = _progress(page)\n    assert d1 == d0, \"an edit that is still Needs review was counted as decided\"\n    assert k1 == server and n1 >= 1, (n1, k1)\n    assert re.search(rf\"{server} edit to check\", page.get_by_test_id(\"todo-list\").inner_text())\n    assert page.get_by_test_id(\"need-review-count\").inner_text().startswith(str(n1))\n\n\ndef test_the_export_stepper_shows_the_gate_warning_in_plain_words(page, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    cs = open_rail(page)\n    gate = cs.locator('[data-step-id=\"export_gate\"]'); expect(gate).to_have_attribute(\"data-status\", \"pass\")\n    w = gate.locator('[data-warning-code=\"EDIT_NOT_CONFIRMED\"]'); expect(w).to_have_count(1)\n    txt = w.inner_text().lower()\n    assert \"not in the letter\" in txt and \"quote\" in txt and \"does not block\" in txt, txt\n    assert not RAW_CODE.search(w.inner_text()), txt\n    w.get_by_test_id(\"btn-gate-warning-jump\").click()\n    assert page.evaluate(\"(() => { const r = document.activeElement.closest('[data-item-id]'); return !!r && r.hasAttribute('data-edit-check'); })()\"), \"the jump lands on the edit to check\"\n\n\ndef test_the_next_step_names_the_edit_not_a_pending_item(page, edited_quote):\n    t = edited_quote; c = _case(t[\"tok\"])\n    for it in c[\"entries\"] + c[\"amounts\"] + c[\"flags\"]:                        # decide everything else, so only the edit waits\n        if it[\"id\"] != t[\"id\"] and it[\"review_status\"] == \"pending\" and it[\"state\"] != \"rejected\":\n            api(\"POST\", f\"/api/cases/{t['tok']}/items/{it['id']}/review\", {\"action\": \"dismiss\"})\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    nxt = page.get_by_test_id(\"case-next-action\"); expect(nxt).to_be_visible()\n    txt = nxt.inner_text().lower()\n    assert \"0 pending\" not in txt and \"edit\" in txt and \"quote\" in txt, txt\n\n\ndef test_the_edit_is_named_before_the_letter_is_copied(page, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    page.get_by_test_id(\"btn-export\").click(); page.get_by_test_id(\"btn-copy-letter\").click()\n    expect(page.get_by_test_id(\"copy-confirm\")).to_contain_text(\"1 edited entry still marked Needs review\")\n\n\ndef test_comparing_it_with_the_quote_closes_everything(page, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    row = _row(page, t[\"id\"])\n    d0, _, n0, k0 = _progress(page); assert k0 == 1\n    row.get_by_test_id(\"btn-accept\").click()\n    expect(row).to_have_attribute(\"data-review\", \"accepted\"); assert row.get_attribute(\"data-edit-check\") is None\n    d1, _, n1, k1 = _progress(page)\n    assert d1 == d0 + 1 and k1 == 0 and n1 == n0 - 1, ((d0, n0, k0), (d1, n1, k1))\n    assert _case(t[\"tok\"])[\"review\"][\"counts\"][\"edit_to_check\"] == 0\n    assert \"edit to check\" not in page.get_by_test_id(\"todo-list\").inner_text()\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    assert open_rail(page).locator('[data-warning-code=\"EDIT_NOT_CONFIRMED\"]').count() == 0\n"
}
````

### User / tool · 2026-11-02T12:34:33.867Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/e2e/test_edit_to_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:34:36.714Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && cp /Users/arsis/zlayt-pm-project/tests/e2e/test_edit_to_check.py tests/e2e/ && ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 E2E_BASE_URL=http://localhost:7931 timeout 500 .venv/bin/python -m pytest tests/e2e/test_edit_to_check.py -x -q 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T12:34:36.819Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:34:39.527Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 E2E_BASE_URL=http://localhost:7931 .venv/bin/python -m pytest tests/e2e/test_edit_to_check.py -q 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T12:34:55.100Z

**tool result**
````
page = <Page url='http://localhost:7931/#/case/z0W-FFovG_gkKRx4mc5riA'>
edited_quote = {'tok': 'z0W-FFovG_gkKRx4mc5riA', 'id': 'e2', 'before': (0, 23, 4, 0), 'orig': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'}

    def test_comparing_it_with_the_quote_closes_everything(page, edited_quote):
        t = edited_quote; _accept_something_else(t)
        page.reload(); page.get_by_test_id("timeline").wait_for()
        row = _row(page, t["id"])
>       d0, _, n0, k0 = _progress(page); assert k0 == 1
                                         ^^^^^^^^^^^^^^
E       assert 0 == 1

tests/e2e/test_edit_to_check.py:133: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_edit_to_check.py::test_a_quote_only_edit_is_open_and_offers_the_compare_accept
FAILED tests/e2e/test_edit_to_check.py::test_header_and_strip_use_the_servers_edit_count
FAILED tests/e2e/test_edit_to_check.py::test_the_export_stepper_shows_the_gate_warning_in_plain_words
FAILED tests/e2e/test_edit_to_check.py::test_the_next_step_names_the_edit_not_a_pending_item
FAILED tests/e2e/test_edit_to_check.py::test_the_edit_is_named_before_the_letter_is_copied
FAILED tests/e2e/test_edit_to_check.py::test_comparing_it_with_the_quote_closes_everything
6 failed in 15.28s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:34:56.853Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-136 | tail -25; grep -n -i \"compared\\|dismissed (\\|collapse\\|single .a\\|press.*a\\b\" reviews/T-060-paralegal-pass5.md | head -40"
}
````

### User / tool · 2026-11-02T12:34:56.996Z

**tool result**
````
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T12:31:58Z"
updated_at: "2026-11-02T12:34:41Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T12:32:15Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "an excerpt-only edit shows as open with the compare-and-accept control; header/strip counts include review.counts.edit_to_check; e2e test", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T12:32:15Z frontend: claimed
- 2026-11-02T12:34:41Z orchestrator: Expanded from T-060 paralegal pass 5 (reviews/T-060-paralegal-pass5.md): (1) a single 'a' press on an edited row must not record the 'I compared it with the quote' confirmation or clear the copy warning - require an explicit confirm step (click or a second deliberate key with a visible prompt); (2) dismissed flags and amounts must collapse under Dismissed (n) like entries. A paralegal re-check is part of this card's review.

## Handoff (filled when moving to in_review)

5:The letter is still clean: every quote is verbatim and the $185 rate stays out of the total. The state is still the problem. The edited record 3 can be recorded as compared by one `a` keypress, the row keeps "Needs review" next to "Accepted", and after that the export bar, the header and the copy warning all stop saying anything is open. The dismissed-item rows are fixed except for their grouping.
11:| M1: dismissed flag or amount keeps Accept, `a` turns it into Accepted | Mostly fixed. A dismissed flag and a dismissed amount show only Dismissed and Undo (plus Audit and links); `a` on either leaves progress and the row unchanged. Not fixed: they are not collected under "Dismissed (n)" (F2). | `artifacts/review-evidence/T-060-paralegal-pass5/p5-06-m1-probe.out.txt`; `p5-06-m1-flag-f_r7_1-after-a.png` |
12:| M2: edited entry marked Needs review has no control, counts as decided, export says "Nothing left to decide" | Partly fixed, partly regressed. Mouse path: the header counts the edit as open and the copy warning names it. But "I compared it with the quote" leaves the Needs review chip on the row, and a single `a` (Start review selects this row first) records a comparison without the check and removes the warning (F1). | `p5-10-m2-compare.stdout.txt`; `p5-10-after-a-on-edited.png`; `p5-11-case2-m2-mouse.out.txt`; `p5-11-case2-e3-after-compare.png` |
38:7. M2 mouse path on a second pasted case (23 items, `case-RBKmvN...`): Edit, Save, Export, Copy letter (warning shown), Go back, "I compared it with the quote" (`p5-11-case2-m2-mouse.py`).
40:9. Keyboard on case 2: 40 presses of j from Start review, 40 of k, `o` then `a`, the batch button (`p5-12-case2-keys-batch.py`).
50:- **F1 (major): an edited row marked Needs review can be accepted by one `a` press, and the export then stops saying anything is open.** `Start review focus: e3`, then `a` gives `progress 23 of 23 decided`, the row reads "Needs review | Accepted", the header shows "0 items need review" and a banner "Everything is decided. Nothing is waiting on you." Copy goes straight through ("Copied the treatment section.", `p5-10-m2-compare.stdout.txt` lines 2, 4 and 7). On the mouse path the row still shows Needs review next to Accepted after "I compared it with the quote" (`p5-11-case2-m2-mouse.out.txt` line 10; `p5-11-case2-e3-after-compare.png`). The export bar says "0 items pending (0 flags)" while the header says "22 of 23 decided · 1 item needs review" (`p5-09-export-body.txt` line 538; `p5-09-after-copy-click.png`). When the copy warning does appear, it names the edit: "1 edited entry still marked Needs review (compare with the quote)" (`p5-11-case2-m2-mouse.out.txt` line 6). The export inclusion of the edited wording follows D-045b and I do not count it here; the cue is what fails.
51:- **F2 (major): dismissed flags and amounts are not collected under "Dismissed (n)".** Pass-4 M1's first fix item and its acceptance test require this. Entries get the group (`Dismissed (1)` in `p5-13-case1-dismiss-entry-oneline.out.txt` line 6), but no "Dismissed (" heading exists in the case body with the flag and amount dismissed (`p5-05-state-body.txt`: zero matches). The dismissed flag "Accident date source" and the dismissed amount "missing 3 days of work" stay in place (`p5-06-m1-flag-f_r7_1-after-a.png`).
83:  "M2 mouse path on a second pasted case: Edit, Save, Export, Copy letter (warning), Go back, I compared it with the quote, export, copy (p5-11)",
85:  "case 2 keyboard: 40 j presses from Start review, 40 k presses, o then a in the record dialog, batch button click (p5-12)",
95:  {"severity": "major", "title": "Edited entry marked Needs review is recorded as compared by one a press; the row keeps Needs review beside Accepted; the export bar, header and copy warning then say nothing is open",
96:   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-10-m2-compare.stdout.txt lines 2 (Start review focus: e3), 4 (a on edited e3 before compare: progress 23 of 23 decided) and 7 (copy warning texts include 'Copied the treatment section.' and 'Nothing left to decide. Export is next.'); p5-10-after-a-on-edited.png (header '23 of 23 decided', chip '0 items need review', banner 'Everything is decided'; row chips 'Needs review' and 'Accepted'); p5-11-case2-m2-mouse.out.txt line 10 and p5-11-case2-e3-after-compare.png (Needs review still beside Accepted after I compared); p5-09-export-body.txt line 538 ('0 items pending (0 flags)') against p5-09-after-copy-click.png header '22 of 23 decided · 1 item needs review'; warning that does work: p5-11-case2-m2-mouse.out.txt line 6 names '1 edited entry still marked Needs review (compare with the quote)'",
98:   "fix": "(1) a on an edited row whose reason is JUDGE_UNAVAILABLE does not record the comparison; it focuses 'I compared it with the quote' and says so. (2) After the comparison the Needs review chip clears and the reason becomes 'Compared by you; second AI check not available'. (3) The export bar counts an edit still marked Needs review as open ('1 edit to check'), never '0 items pending' while the header says 1. (4) The copy warning names the record ('Record 3, Dr. Alvarez, primary care').",
99:   "acceptance_test": "Start review on a case with one edited entry (judge unavailable), press a: progress stays at N-1 of 23, the row keeps a 'Compare with the quote' control and no Accepted chip, Copy letter shows the warning naming Record 3; after clicking the compare control the row has no Needs review chip and the export bar and header agree."},
100:  {"severity": "major", "title": "Dismissed flags and amounts are not collected under Dismissed (n); only entries are (pass-4 M1 residual)",
101:   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-05-state-body.txt has zero 'Dismissed (' headings with the flag f_r7_1 and the amount a3 dismissed; p5-13-case1-dismiss-entry-oneline.out.txt line 6 shows the only group, 'Dismissed (1)', for record 8 (an entry); p5-06-m1-flag-f_r7_1-after-a.png shows the dismissed flag in place among open flags; p5-05-a3-state.png shows the dismissed amount in place",
102:   "why_it_matters": "Pass-4 M1's acceptance test requires both kinds listed under Dismissed (n). The row states are now right (Dismissed and Undo only, a is a no-op), but a dismissed flag still sits in the open list where she is scanning for what needs her.",
103:   "fix": "Give dismissed flags and amounts the same collapsed Dismissed (n) group as entries, with the reason, and remove them from the open list.",
104:   "acceptance_test": "Dismiss one flag and one amount: both appear under a 'Dismissed (n)' group and not in the open list; a on either leaves progress unchanged; the group count matches the export's dismissed list."},
124:   "acceptance_test": "With the record dialog open, pressing a shows the message or accepts the selected item; the message text is in the DOM."},
131:   "evidence": "artifacts/review-evidence/T-060-paralegal-pass5/p5-09-export-body.txt lines 621-622 ('DAMAGES MENTIONS (not charges)' then '- none') while 'missing 3 days of work' is Dismissed (p5-05-a3-state.png)",
177:  "Should a on an edited row that still needs a second check record the comparison at all, or should only the named 'I compared it with the quote' control do that (F1)?",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:00.439Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 90,166p review.js; grep -n \"dismissed-group\\|dismissedOpen\" *.js | head -20"
}
````

### User / tool · 2026-11-02T12:35:00.535Z

**tool result**
````
  // item that still needs a decision, needs-review ones before verified ones.
  const NOT_QUEUE = "dialog, .sbs-pane";
  RV.itemRowOf = function (t) {   // the item row that holds focus, or null (focus on Export, the header, a dialog or the page body is not "in" the queue)
    const r = t && t.closest && t.closest("[data-item-id]");
    return r && !r.closest(NOT_QUEUE) ? r : null;
  };
  RV.domItems = () => Array.from(document.querySelectorAll("[data-item-id]")).filter((n) => !n.closest(NOT_QUEUE) && n.offsetParent !== null);
  const decidable = (n) => { const rs = n.getAttribute("data-review"); return (rs === "pending" || (rs === "edited" && n.hasAttribute("data-edit-check"))) && n.getAttribute("data-state") !== "rejected" && !n.hasAttribute("data-tray-kind"); };
  RV.nextPendingAfter = function (items, at) {   // items after `at` first, then wrapping. Order of preference: a needs-review entry in the timeline, then any needs-review item, then any item that still needs a decision
    const order = items.slice(at + 1).concat(items.slice(0, Math.max(at, 0) + (at < 0 ? 0 : 1)));
    const open = order.filter(decidable), needs = (n) => n.getAttribute("data-state") === "needs_review";
    return open.find((n) => needs(n) && n.closest('[data-testid="queue"]')) || open.find(needs) || open[0] || null;
  };
  // T-060 r5 (ux F3): after a / d the next row is the next row of the SAME list (the timeline, one flag kind, the charges table, the unclear table). It is never a row of another
  // kind: a run of `a a a` down the timeline can not accept a conflict flag. "The next item that needs a decision anywhere" is Start review's job only.
  const GROUP = '[data-group], [data-testid="queue"], [data-testid="dates-to-confirm"]';
  const groupKey = (g) => (g.hasAttribute("data-group") ? '[data-group="' + g.getAttribute("data-group") + '"]' : g.getAttribute("data-testid") ? '[data-testid="' + g.getAttribute("data-testid") + '"]' : null);
  const rowsIn = (g) => Array.from(g.querySelectorAll("[data-item-id]")).filter((n) => !n.closest(NOT_QUEUE) && n.offsetParent !== null);
  RV.planAdvance = function (id) {
    const ae = document.activeElement, mine = ae && ae.closest && ae.closest("[data-item-id]");
    const row = mine && mine.getAttribute("data-item-id") === id ? mine : document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]') || document.querySelector('[data-item-id="' + id + '"]');
    const g = row && row.closest(GROUP), key = g && groupKey(g);
    return key ? { key, ids: rowsIn(g).map((n) => n.getAttribute("data-item-id")), id } : { key: null, ids: [], id };
  };
  function focusNode(t) {
    if (!t) return false;
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
    t.focus({ preventScroll: true }); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
    return true;
  }
  function focusItem(id) {
    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
    return focusNode(q || document.querySelector('[data-item-id="' + id + '"]'));
  }
  RV.focusFirstPending = function () {   // "Start review": the first item that needs a decision, needs-review ones first
    const items = RV.domItems(); const t = items.filter(decidable).find((n) => n.getAttribute("data-state") === "needs_review") || items.find(decidable) || items[0];
    return focusNode(t);
  };
  function focusExport(msg) { const b = document.querySelector('[data-testid="btn-export"]'); if (b) { b.focus(); if (msg) RV.say(msg); } }
  function restoreFocus(pf) {
    if (!pf) return;
    requestAnimationFrame(() => {
      if (pf.nextFrom) {
        const plan = pf.plan || { key: null, ids: [], id: pf.nextFrom }, g = plan.key && document.querySelector(plan.key);
        const now = new Map((g ? rowsIn(g) : []).map((n) => [n.getAttribute("data-item-id"), n]));
        const at = plan.ids.indexOf(plan.id), order = plan.ids.slice(at + 1).concat(plan.ids.slice(0, Math.max(at, 0)));
        const t = order.map((i) => now.get(i)).filter(Boolean).find(decidable);
        if (t) { focusNode(t); return; }
        const c = RV.caseNow(), left = c ? ZL.progressOf(c).left : 0;
        if (!left) { focusExport("Nothing left to decide. Export is next."); return; }   // the last decision: the next control is the one that finishes the job, not the top of the page
        // this list is finished but other lists are not: stay where she is (or on the list's neighbour) and say so; never jump to an item of another kind
        const stay = now.get(plan.id) || order.map((i) => now.get(i)).filter(Boolean)[0];
        if (stay) focusNode(stay); else { const s = document.querySelector('[data-testid="btn-start-review"]'); if (s) s.focus(); }
        RV.say("Nothing more to decide in this list. " + left + (left === 1 ? " item is" : " items are") + " still open in other lists. Press Start review to go to the next one.");
        return;
      }
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) t.focus(); else focusItem(pf.id);
    });
  }

  // The server names a refused number the way it compares it ("9000"). Show it the way the paralegal typed it ("$9,000"): swap the first matching figure in the message for the
  // same figure as it appears in her own text. Display only; nothing is added or compared.
  RV.asTyped = function (msg, tokens, text) {
    let out = String(msg || "");
    (tokens || []).forEach((tok) => {
      if (!/^\d[\d.]*$/.test(String(tok))) return;
      const re = /\$?\s?\d[\d,]*(?:\.\d+)?/g; let m, typed = null;
      while ((m = re.exec(text || "")) && !typed) { const bare = m[0].replace(/[$,\s]/g, ""); if (bare === tok || bare.replace(/\.0+$/, "") === tok) typed = m[0].trim(); }
      if (!typed || typed === tok) return;
      out = out.replace(new RegExp("(^|[^\\d$,.])" + String(tok).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![\\d,]|\\.\\d)"), (_, pre) => pre + typed);
    });
    return out;
  };
  // What happened to an edit, in plain words, kept on the row until the next decision: the code re-checks the wording against the quote on every save, then a second AI check reads it.
  const rechecks = {};   // id -> sentence
review.js:240:      if (body.action === "dismiss" && found && found.kind === "entry") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo
timeline.js:66:  ZL.dismissedOpen = false;
timeline.js:69:    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group", open: ZL.dismissedOpen || null },
timeline.js:72:    d.addEventListener("toggle", () => { ZL.dismissedOpen = d.open; });
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:04.891Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"keydown\" review.js | head; grep -n \"case \\\"a\\\"\\|key === \\\"a\\\"\\|\\\"a\\\"\" review.js | head; sed -n 55,80p timeline.js; grep -n \"dismissed\" timeline.js flags.js charges.js | head -40"
}
````

### User / tool · 2026-11-02T12:35:05.000Z

**tool result**
````
329:      ta.addEventListener("keydown", (ev) => {
372:  document.addEventListener("keydown", (ev) => {
351:  const KEYS = [["j / k", "Next / previous item (dates to confirm, then entries, flags, charges)"], ["a", "Accept the selected item, then move to the next one that needs a decision"], ["d", "Dismiss the selected item, then move on"],
395:    if ((key === "a" || key === "d" || key === "e") && f.item.review_status === "dismissed") {   // T-060 r5 (paralegal M1): one key never undoes a dismissal; only Undo (or r) does
399:    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "entry-why", "aria-label": "Why this status: " + e.provider + (e.date ? ", " + ZL.fmtDate(e.date) : ""), onclick: () => openWhy(e.id) }, "Why this status"),
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": `Open record ${rec ? rec.seq : ""} for ${e.provider}`, onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"),
        )].filter(Boolean));
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    const ra = row.querySelector(":scope > .row-actions");
    if (ra) { ra.append(toggle); row.append(ra); }   // "More" is the last of the row's links; the links follow the decision buttons in the DOM, as they do on screen, so Tab order matches what is seen
    return row;
  }
  // T-060 r4: a dismissed entry leaves the queue and waits in a collapsed "Dismissed (n)" group right under it, each with Undo. It opens by itself for the entry the paralegal just
  // dismissed (so she sees where it went and can undo it), and stays as she leaves it. Dismissed entries are never in the letter.
  ZL.dismissedOpen = false;
  function dismissedGroup(c, rows) {
    if (!rows.length) return null;
    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group", open: ZL.dismissedOpen || null },
      el("summary", { "data-testid": "dismissed-summary" }, `Dismissed (${rows.length})`, el("span", { class: "muted small" }, " Not in the letter. Open to read them or press Undo.")),
      el("div", { class: "timeline", "data-testid": "dismissed-queue" }, rows.map((e) => entryRow(e, c))));
    d.addEventListener("toggle", () => { ZL.dismissedOpen = d.open; });
    return d;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => ZL.firstRank(e.id, e.state);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
flags.js:72:      f.state === "needs_review" && f.review_status !== "dismissed" && whyOnce(f) ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), whyOnce(f)) : null,   // the "quote found word for word..." sentence is in Why this status, not repeated on every card
flags.js:75:    if (note) a.append(el("p", { class: "rv-usernote", "data-testid": "flag-note-text" }, el("strong", {}, f.review_status === "dismissed" ? "Dismissed because: " : "Your note: "), note));
timeline.js:7:  const REVIEW_LABEL = { pending: "Not reviewed yet", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
timeline.js:20:  const DECISION = { accepted: ["ok", "check"], edited: ["ok", "pencil"], dismissed: ["muted", "dash"] };
timeline.js:38:    const reasonText_ = e.state === "needs_review" && e.review_status !== "dismissed" && (e.reasons.length || e.why) ? plainReason(e) : "";
timeline.js:64:  // T-060 r4: a dismissed entry leaves the queue and waits in a collapsed "Dismissed (n)" group right under it, each with Undo. It opens by itself for the entry the paralegal just
timeline.js:65:  // dismissed (so she sees where it went and can undo it), and stays as she leaves it. Dismissed entries are never in the letter.
timeline.js:66:  ZL.dismissedOpen = false;
timeline.js:67:  function dismissedGroup(c, rows) {
timeline.js:69:    const d = el("details", { class: "dismissed-group", "data-testid": "dismissed-group", open: ZL.dismissedOpen || null },
timeline.js:70:      el("summary", { "data-testid": "dismissed-summary" }, `Dismissed (${rows.length})`, el("span", { class: "muted small" }, " Not in the letter. Open to read them or press Undo.")),
timeline.js:71:      el("div", { class: "timeline", "data-testid": "dismissed-queue" }, rows.map((e) => entryRow(e, c))));
timeline.js:72:    d.addEventListener("toggle", () => { ZL.dismissedOpen = d.open; });
timeline.js:89:  // one is shown in plain words above the timeline (it stays until dismissed) and announced, so a figure never changes silently. Focus then moves to the
timeline.js:307:    const shown = c.entries.concat(c.undated_entries), nNeeds = ZL.progressOf(c).needs, nVer = shown.filter((e) => e.state === "verified").length; // T-060 r5: the SAME need-review number as the header and the strip (everything still open that is marked Needs review); falls when one is decided or dismissed
timeline.js:316:    const sorted = sortedEntries(c), liveRows = sorted.filter((e) => e.review_status !== "dismissed"), dismissedRows = sorted.filter((e) => e.review_status === "dismissed");
timeline.js:331:      dismissedGroup(c, dismissedRows),
charges.js:74:    const gone = rs === "dismissed";   // T-060 r5: a dismissed amount is decided; it keeps its quote, the word Dismissed and Undo, and no "Needs review" reason
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:06.672Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 370,420p review.js; sed -n 1,60p flags.js | head -5; grep -n \"function render\\|renderPanel\\|ZL.registerPanel\\|data-group\" flags.js charges.js | head -30"
}
````

### User / tool · 2026-11-02T12:35:06.772Z

**tool result**
````
  // From Export, the header, a dialog, a text field or the page body they do nothing, so a stray key can never change a decision.
  const typing = (t) => !!t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable);
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (typing(t)) return;
    if (document.querySelector("dialog[open]")) {   // a dialog swallows the letter keys; say so instead of doing nothing (T-060 r3, paralegal F11)
      if (ev.key.length === 1 && "jkadero".includes(ev.key.toLowerCase()) && !ev.shiftKey && ZL.state.get().case) RV.say("A window is open. Press Escape to close it first, then use the key again.");
      return;
    }
    const row = RV.itemRowOf(t);
    if (!row) return;
    const c = RV.caseNow(); if (!c) return;
    const key = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key, id = row.getAttribute("data-item-id");
    if (ev.key === "?") { ev.preventDefault(); if (RV.openShortcuts) RV.openShortcuts(); return; }
    if (ev.shiftKey) return;   // Shift+A is the batch key (batch.js); a capital letter never means the single-item key
    if (key === "j" || key === "k") {
      const items = RV.domItems(), at = items.indexOf(row), n = items[at + (key === "j" ? 1 : -1)];
      ev.preventDefault();
      if (n) focusNode(n); else RV.say(key === "j" ? "That is the last item." : "That is the first item.");
      return;
    }
    if (ev.key.length !== 1 || !"aedro".includes(key)) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    if ((key === "a" || key === "d" || key === "e") && f.item.review_status === "dismissed") {   // T-060 r5 (paralegal M1): one key never undoes a dismissal; only Undo (or r) does
      RV.say("This item is dismissed. Press r or Undo to bring it back first.");
      return;
    }
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.act(id, { action: "reset" }, { focus: "reset" }); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (c && mountEl) render(mountSection(mountEl, name), c); });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
/* Flags panel (T-043): four groups plus "Record warnings" (R-FL-6),
   unmerged conflicts shown side by side (D-017), reviewer note only (D-010), confirm_date control for ambiguous dates.
   All server text is inserted as text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
flags.js:83:  function render(root, c) {
flags.js:94:      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
charges.js:85:    return el("table", { class: "rv-table", "data-group": inTray ? "unclear-amounts" : "charges" }, el("caption", { class: "rv-sr" }, caption),
charges.js:95:  function render(root, c) {
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:15.953Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 83,140p flags.js; sed -n 60,140p charges.js"
}
````

### User / tool · 2026-11-02T12:35:16.037Z

**tool result**
````
  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "flags-panel");
    root.setAttribute("aria-labelledby", "rv-flags-h");
    root.append(el("h2", { id: "rv-flags-h" }, "Flags"),
      el("p", { class: "rv-help" }, "Flags point to things worth checking. Accepting one means you have seen it: it goes to the internal notes, never into the letter."));
    if (c.injection && c.injection.banner) root.append(el("p", { class: "rv-banner", role: "note" }, c.injection.banner));
    if (ZL.sg) root.append(ZL.sg.dismissalBox(c));
    const flags = c.flags || [];
    GROUPS.forEach(([type, title, empty]) => {
      const list = RV.needsReviewFirst(flags.filter((f) => f.type === type));
      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
        el("h3", { id: "rv-g-" + type }, title + " (" + list.length + ")"));
      if (type === "gap" && ZL.gapChanges) ZL.gapChanges.removed(c).forEach((t) => g.append(el("p", { class: "rv-gap-change", "data-testid": "gap-change-removed" }, t)));
      if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
      list.forEach((f) => g.append(card(c, f)));
      root.append(g);
    });
  }
  RV.registerPanel("flags", render);
  RV.renderFlags = render;
})();
  function row(c, a, inTray, boiler) {
    const isCharge = a.kind === "charge";
    const rs = a.review_status || "pending";
    const seq = recSeq(c, (a.record_ids || [])[0]);
    const tr = el("tr", { class: "rv-card rv-amount", tabindex: "0", "data-testid": "amount-" + a.text, "data-item-id": a.id, "data-amount-kind": a.kind,
      "data-state": a.state, "data-review": rs, "aria-label": "Amount " + a.text });
    const first = el("td", { class: "rv-c-amount", "data-label": "Amount" }, el("strong", { class: "rv-money", title: "As written in the record: " + a.text }, a.value_cents != null ? RV.money(a.value_cents) : a.text), el("span", { class: "rv-kind" }, KIND[a.kind] || a.kind));
    const src = el("td", { class: "rv-c-src", "data-label": "From the record" },
      snippet(a),
      el("div", { class: "rv-src-links" },
        el("button", { type: "button", class: "btn btn--link", "data-testid": "btn-source", "aria-label": "Open record " + seq + " for the amount " + a.text, onclick: () => RV.openSource(a, "amount") }, "Open record " + seq),
        ZL.stepper ? ZL.stepper.traceButton(a.id, "btn btn--link") : null));
    // one reason line (the code's). The server's longer sentence is shown only when it adds something and is not a notice every row repeats.
    const why = a.why && !boiler.has(a.why) ? a.why : null;
    const gone = rs === "dismissed";   // T-060 r5: a dismissed amount is decided; it keeps its quote, the word Dismissed and Undo, and no "Needs review" reason
    const status = el("td", { class: "rv-c-status", "data-label": "Status" }, RV.chips(a),
      inTray && !gone ? el("span", { class: "rv-unclear-note" }, STATUS_WORDS[a.kind] || STATUS_WORDS.unclear, ". ", unclearNote(c, a)) : null,
      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Kept in the internal notes only; not in the letter or the total.") : null,
      why && !gone ? el("p", { class: a.state === "needs_review" ? "rv-reason-line" : "rv-why" }, why) : null);
    const act = el("td", { class: "rv-c-act", "data-label": "Decision" }, RV.controls(a, "amount"));
    tr.append(first, src, status, act);
    return tr;
  }

  function table(c, list, caption, inTray, boiler) {
    return el("table", { class: "rv-table", "data-group": inTray ? "unclear-amounts" : "charges" }, el("caption", { class: "rv-sr" }, caption),
      el("thead", {}, el("tr", {}, ["Amount", "From the record", "Status", "Decision"].map((h) => el("th", { scope: "col" }, h)))),
      el("tbody", {}, RV.needsReviewFirst(list).map((a) => row(c, a, inTray, boiler))));
  }
  // A sentence that several rows carry (for example the Spanish-record notice) is shown once above the table and left out of the rows.
  function repeated(list) {
    const n = {}; list.forEach((a) => { if (a.why) n[a.why] = (n[a.why] || 0) + 1; });
    return new Set(Object.keys(n).filter((k) => n[k] > 1));
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "charges-panel");
    root.setAttribute("aria-labelledby", "rv-charges-h");
    const amounts = c.amounts || [], t = c.totals || {};
    const charges = amounts.filter((a) => a.kind === "charge"), unclear = amounts.filter((a) => a.kind !== "charge");
    const acc = (t.accepted && t.accepted.cents) != null ? t.accepted.cents : 0;
    const pendObj = t.pending || t.detected_not_a_total || { cents: 0 };
    root.append(el("h2", { id: "rv-charges-h" }, "Charges"),
      el("p", { class: "rv-help" }, "Only charges you accept are counted. Rates, estimates, damages and unreadable amounts are listed below and never added."),
      el("div", { class: "rv-totals" },
        el("p", { class: "rv-total rv-total-main", "data-testid": "accepted-total", "aria-live": "polite" }, el("span", { class: "rv-total-label" }, "Accepted charges: "), el("strong", {}, RV.money(acc))),
        el("p", { class: "rv-total rv-total-pending", "data-testid": "pending-total" }, "Detected, not yet accepted: " + RV.money(pendObj.cents || 0) + " (not a total)")));
    const overlap = ZL.sg ? ZL.sg.overlapBox(c) : null; if (overlap) root.append(overlap);
    root.append(el("h3", {}, "Detected charges (" + charges.length + ")"));
    const chBoil = repeated(charges), unBoil = repeated(unclear);
    if (charges.length) { chBoil.forEach((t) => root.append(el("p", { class: "rv-tray-note" }, t))); root.append(table(c, charges, "Detected charges", false, chBoil)); } else root.append(el("p", { class: "rv-empty" }, "No charges were found."));
    const tray = el("section", { class: "rv-tray", "data-testid": "unclear-tray", "aria-labelledby": "rv-unclear-h" },
      el("h3", { id: "rv-unclear-h" }, "Unclear — not totaled (" + unclear.length + ")"));
    if (unclear.length) { unBoil.forEach((t) => tray.append(el("p", { class: "rv-tray-note", "data-testid": "tray-notice" }, t))); tray.append(table(c, unclear, "Unclear amounts, not totaled", true, unBoil)); } else tray.append(el("p", { class: "rv-empty" }, "Nothing unclear."));
    root.append(tray);
  }
  RV.registerPanel("charges", render);
  RV.renderCharges = render;
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:42.126Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\nimport re\np='review.js'; s=open(p).read()\n\n# dismissed box helper + open-state map, before the \"ui\" registry; put right after RV.itemRowOf definition block\nanchor='  RV.domItems = () =>'\nadd='''  // T-136 (paralegal pass 5 F2): dismissed flags and amounts wait in a collapsed \"Dismissed (n)\" group inside their own panel, like dismissed entries do under the timeline. Not in the letter; each keeps Undo.\n  // The group opens for the item she just dismissed (so she sees where it went) and stays as she leaves it.\n  ZL.dismissedOpenBy = ZL.dismissedOpenBy || {};\n  RV.dismissedBox = function (kind, count, body) {\n    const d = el(\"details\", { class: \"dismissed-group\", \"data-testid\": \"dismissed-group-\" + kind, open: ZL.dismissedOpenBy[kind] || null },\n      el(\"summary\", { \"data-testid\": \"dismissed-summary-\" + kind }, \"Dismissed (\" + count + \")\", el(\"span\", { class: \"muted small\" }, \" Not in the letter. Open to read them or press Undo.\")), body);\n    d.addEventListener(\"toggle\", () => { ZL.dismissedOpenBy[kind] = d.open; });\n    return d;\n  };\n'''\nassert anchor in s; s=s.replace(anchor, add+anchor,1)\n\nold='''      if (body.action === \"dismiss\" && found && found.kind === \"entry\") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo'''\nnew='''      if (body.action === \"dismiss\" && found && found.kind === \"entry\") ZL.dismissedOpen = true;   // the entry moves to the Dismissed group: show it there, with its Undo\n      else if (body.action === \"dismiss\" && found) ZL.dismissedOpenBy[found.kind === \"amount\" ? \"amounts\" : \"flags\"] = true;   // a flag or amount does the same in its own panel'''\nassert old in s; s=s.replace(old,new,1)\n\n# 'a' on an edit to check: never records\nold='''    if (key === \"a\") RV.act(id, { action: \"accept\" }, { advance: true });\n    else if (key === \"d\")'''\nnew='''    if (key === \"a\" && ZL.editToCheck(f.item)) { askCompare(id); return; }   // T-136 (paralegal F1): one key press never records \"I compared it with the quote\"; the button (click, or Enter on it) does\n    if (key === \"a\") RV.act(id, { action: \"accept\" }, { advance: true });\n    else if (key === \"d\")'''\nassert old in s; s=s.replace(old,new,1)\n\n# prompt in controls + askCompare\nold='''    if (toCheck && !rechecks[id]) root.append(el(\"p\", { class: \"rv-help rv-recheck\", \"data-testid\": \"edit-check-hint\" }, \"Still marked Needs review. Compare your wording with the quote, then press the button to say you did. Until then it counts as open.\"));'''\nnew='''    if (toCheck && !rechecks[id]) root.append(el(\"p\", { class: \"rv-help rv-recheck\", \"data-testid\": \"edit-check-hint\" }, \"Still marked Needs review. Compare your \" + (item.edited && item.edited.summary != null ? \"wording\" : \"quote\") + \" with the original, then press the button to say you did. Until then it is not in the letter and counts as open.\"));\n    if (toCheck && comparePrompt.has(id)) root.append(el(\"p\", { class: \"rv-help rv-compare-prompt\", role: \"alert\", \"data-testid\": \"edit-compare-prompt\" }, COMPARE_PROMPT));'''\nassert old in s; s=s.replace(old,new,1)\n\nold='''  const rechecks = {};   // id -> sentence'''\nnew='''  const rechecks = {};   // id -> sentence\n  // T-136 (paralegal pass 5 F1): the confirmation \"I compared it with the quote\" is a statement by the paralegal. The a key (and Start review, which lands on this row) must not make it for her:\n  // a asks, in a visible line, and puts focus on the button; she records it by clicking the button or pressing Enter on it.\n  const comparePrompt = new Set();\n  const COMPARE_PROMPT = \"Not recorded yet. Read the quote against your edit. Then click \\\\u201cI compared it with the quote\\\\u201d, or press Enter on it, to say you did.\";\n  function askCompare(id) {\n    comparePrompt.add(id);\n    const root = document.querySelector('[data-controls-for=\"' + id + '\"]'); if (!root) return;\n    let p = root.querySelector('[data-testid=\"edit-compare-prompt\"]');\n    if (!p) { p = el(\"p\", { class: \"rv-help rv-compare-prompt\", role: \"alert\", \"data-testid\": \"edit-compare-prompt\" }, COMPARE_PROMPT); const h = root.querySelector('[data-testid=\"edit-check-hint\"]'); if (h) h.after(p); else root.append(p); }\n    const b = root.querySelector('[data-testid=\"btn-accept\"]'); if (b) b.focus();\n    RV.say(COMPARE_PROMPT);\n  }'''\nassert old in s; s=s.replace(old,new,1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"comparePrompt\\|COMPARE_PROMPT\" review.js | head; grep -n \"const { el\\|const el\\|RV.say =\" review.js | head -4"
}
````

### User / tool · 2026-11-02T12:35:42.247Z

**tool result**
````
178:  const comparePrompt = new Set();
179:  const COMPARE_PROMPT = "Not recorded yet. Read the quote against your edit. Then click \u201cI compared it with the quote\u201d, or press Enter on it, to say you did.";
181:    comparePrompt.add(id);
184:    if (!p) { p = el("p", { class: "rv-help rv-compare-prompt", role: "alert", "data-testid": "edit-compare-prompt" }, COMPARE_PROMPT); const h = root.querySelector('[data-testid="edit-check-hint"]'); if (h) h.after(p); else root.append(p); }
186:    RV.say(COMPARE_PROMPT);
322:    if (toCheck && comparePrompt.has(id)) root.append(el("p", { class: "rv-help rv-compare-prompt", role: "alert", "data-testid": "edit-compare-prompt" }, COMPARE_PROMPT));
9:  const el = (...a) => ZL.el(...a);
63:  RV.say = function (msg, isError) {
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:47.785Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='review.js'; s=open(p).read()\ns=s.replace('''\"Compare your \" + (item.edited && item.edited.summary != null ? \"wording\" : \"quote\") + \" with the original, then press the button''','''(item.edited && item.edited.summary != null ? \"Compare your wording with the quote\" : \"Compare the new quote with the record\") + \", then press the button''')\ns=s.replace('\"Still marked Needs review. \" + ','\"Still marked Needs review. \" + ')\ns=s.replace('\"Still marked Needs review. (item.edited','\"Still marked Needs review. \" + (item.edited')\ns=s.replace('el(\"p\", { class: \"rv-help rv-compare-prompt\", role: \"alert\", \"data-testid\"','el(\"p\", { class: \"rv-help rv-compare-prompt\", \"data-testid\"')\ns=s.replace('''      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }''','''      comparePrompt.delete(id);\n      if (refusals[id]) { delete refusals[id]; repaintRefusal(id); }''',1)\nopen(p,'w').write(s)\nEOF\nsed -n 316,322p review.js | cut -c1-330"
}
````

### User / tool · 2026-11-02T12:35:47.888Z

**tool result**
````
      onclick: (ev) => { if (st === "dismissed") { RV.say("Already dismissed. Use Undo to change it."); return; } RV.act(id, { action: "dismiss" }, ev.detail === 0 ? { advance: true } : { focus: "dismiss" }); } }));
    if (isFlag && st !== "dismissed") bar.append(btn("dismiss-reason", "Dismiss with reason…", "btn-dismiss-reason", { "aria-expanded": String(!!d.reasonOpen), "aria-controls": "dr-" + id, onclick: (ev) => { d.reasonOpen = !d.reasonOpen; reasonRow.hidden = !d.reasonOpen; ev.currentTarget.setAttribute("aria-expanded", String(d.
    if (st !== "pending") bar.append(btn("reset", "Undo", "btn-reset", { onclick: () => RV.act(id, { action: "reset" }, { focus: "reset" }) }));
    bar.append(btn("audit", "Audit", "btn-audit", { onclick: () => RV.openAudit && RV.openAudit(id, lbl) }));
    root.append(bar);
    root.append(el("div", { class: "rv-refused", role: "alert", hidden: true, "data-testid": "accept-refused" }));
    if (toCheck && !rechecks[id]) root.append(el("p", { class: "rv-help rv-recheck", "data-testid": "edit-check-hint" }, "Still marked Needs review. Compare your " + (item.edited && item.edited.summary != null ? "wording" : "quote") + " with the original, then press the button to say you did. Until then it is not in the letter a
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:48.871Z

The replace missed the exact string; fix directly.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:54.909Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='review.js'; s=open(p).read()\nold='\"Still marked Needs review. Compare your \" + (item.edited && item.edited.summary != null ? \"wording\" : \"quote\") + \" with the original, then press the button'\nnew='\"Still marked Needs review. \" + (item.edited && item.edited.summary != null ? \"Compare your wording with the quote\" : \"Compare the new quote with the record\") + \", then press the button'\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\n\n# dom.js: editToCheck from the item; ZL.editCount from the review counts\np='dom.js'; s=open(p).read()\nold=s[s.index('  ZL.editToCheck ='):s.index('\\n',s.index('  ZL.editToCheck ='))]\nnew='''  ZL.editToCheck = (i) => !!i && i.edit_to_check === true;   // T-136: the server's own flag (T-134): reworded summary OR quote, still Needs review, not yet accepted by her\n  // How many edits are waiting for her comparison: the review's own count when the server sent it, else a count of the items that say so (the mock API).\n  ZL.editCount = (c) => { const n = c && c.review && c.review.counts && c.review.counts.edit_to_check; return n != null ? n : [].concat(c.entries || [], c.undated_entries || []).filter(ZL.editToCheck).length; };'''\ns=s.replace(old,new,1); open(p,'w').write(s)\n\np='app.js'; s=open(p).read()\ns=s.replace('edits: all.filter(ZL.editToCheck).length };','edits: ZL.editCount(c) };')\ns=s.replace('''\" items need\") + \" review\" : \"\");''','''\" items need\") + \" review\" + (p.edits ? \", including \" + p.edits + (p.edits === 1 ? \" edit\" : \" edits\") + \" to check\" : \"\") : \"\");''')\nopen(p,'w').write(s)\n\np='export.js'; s=open(p).read()\ns=s.replace('const edits = (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length;','const edits = ZL.editCount(cs);')\ns=s.replace('const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? (cs.entries || []).concat(cs.undated_entries || []).filter(ZL.editToCheck).length : 0; };','const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? ZL.editCount(cs) : 0; };')\nopen(p,'w').write(s)\n\np='timeline.js'; s=open(p).read()\ns=s.replace('eEdits = eEntries.filter(ZL.editToCheck).length;','eEdits = Math.min(ZL.editCount(c), eEntries.length);   // the review\\'s own count (T-134), never more than the open entries listed')\nopen(p,'w').write(s)\nEOF\ngrep -n \"editCount\\|including\" app.js export.js timeline.js | cut -c1-200; grep -n \"editsToCheck\" export.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T12:35:55.054Z

**tool result**
````
app.js:23:    return { total: all.length, decided: all.length - open.length, left: open.length, needs: open.filter((i) => i.state === "needs_review").length, edits: ZL.editCount(c) };
app.js:32:    $("#progress-text").textContent = p.decided + " of " + p.total + " decided" + (p.needs ? " · " + p.needs + (p.needs === 1 ? " item needs" : " items need") + " review" + (p.edits ? ", in
export.js:28:    const edits = ZL.editCount(cs);   // T-060 r5 (paralegal M2): her reworded entries that are still marked Needs review
export.js:31:  const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? ZL.editCount(cs) : 0; };
timeline.js:264:    const eEntries = c.entries.filter((e) => open(e) && !dateless.has(e.id)), eEdits = Math.min(ZL.editCount(c), eEntries.length);   // the review's own count (T-134), never more than 
31:  const editsToCheck = () => { const cs = ZL.state.get().case; return cs ? ZL.editCount(cs) : 0; };
61:            el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-copy-letter", disabled: !data.letter_text, onclick: () => { const go = () => copy(data.letter_text, "treatm
62:            el("button", { type: "button", class: "btn", "data-testid": "btn-download-letter", disabled: !data.letter_text, onclick: () => { const go = () => download(data.letter_text, "treatment-s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:35:57.856Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 183,192p mock.js | cut -c1-260; sed -n 128,133p mock.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T12:35:57.944Z

**tool result**
````
      if (method === "POST" && (m = /^\/items\/([^/]+)\/review$/.exec(sub))) {
        const id = decodeURIComponent(m[1]); const it = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags].find((x) => x.id === id);
        if (!it) return err(404, "not_found", "That item was not found.");
        const a = body && body.action;
        if (a === "accept") it.review_status = "accepted"; else if (a === "dismiss") it.review_status = "dismissed"; else if (a === "reset") { it.review_status = "pending"; it.edited = null; }
        else if (a === "edit" && body.edits && typeof body.edits.summary === "string" && id[0] === "e") { it.edited = { summary: body.edits.summary, original_summary: it.summary, at: new Date().toISOString(), kept_my_wording: false }; it.summary = body.edits.s
        else if (a === "edit" && body.edits && typeof body.edits.note === "string" && id[0] === "f") { it.reviewer_note = body.edits.note; it.review_status = "edited"; }
        else return err(422, "invalid_edit", "That edit is not allowed.");
        recompute(c);
        return ok({ item: clone(it), totals: clone(c.totals), review: clone(c.review), warnings: [] });
      detected_not_a_total: { cents: sum(det), count: det.length, label: "Detected (not a total)" }, not_totaled: c.amounts.filter((a) => a.kind !== "charge").map((a) => ({ id: a.id, kind: a.kind, text: a.text })) };
    const items = [...c.entries, ...c.undated_entries, ...c.amounts, ...c.flags];
    const n = (f) => items.filter(f).length;
    c.review = { queue: c._queue, counts: { pending: n((i) => i.review_status === "pending"), accepted: n((i) => i.review_status === "accepted"), edited: n((i) => i.review_status === "edited"),
      dismissed: n((i) => i.review_status === "dismissed"), needs_review: n((i) => i.state === "needs_review"), verified: n((i) => i.state === "verified"), rejected: c.tray.length }, ready_to_export: false };
  }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:36:06.084Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='mock.js'; s=open(p).read()\ns=s.replace('''rejected: c.tray.length }, ready_to_export: false };''','''rejected: c.tray.length,\n      edit_to_check: n((i) => i.edit_to_check === true) }, ready_to_export: false };''',1)\ns=s.replace('''        recompute(c);\n        return ok({ item: clone(it), totals''','''        if (id[0] === \"e\") it.edit_to_check = it.review_status === \"edited\" && it.state === \"needs_review\";   // the server's flag (T-134)\n        recompute(c);\n        return ok({ item: clone(it), totals''',1)\nopen(p,'w').write(s)\n\n# flags\np='flags.js'; s=open(p).read()\nold='''    const flags = c.flags || [];\n    GROUPS.forEach'''\nnew='''    const flags = (c.flags || []).filter((f) => f.review_status !== \"dismissed\"), gone = (c.flags || []).filter((f) => f.review_status === \"dismissed\");\n    GROUPS.forEach'''\nassert old in s; s=s.replace(old,new,1)\nold='''      root.append(g);\n    });\n  }'''\nnew='''      root.append(g);\n    });\n    if (gone.length) root.append(RV.dismissedBox(\"flags\", gone.length, el(\"div\", { class: \"rv-dismissed-list\", \"data-testid\": \"dismissed-flags\" }, gone.map((f) => card(c, f)))));   // T-136 (pass 5 F2)\n  }'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\n\np='charges.js'; s=open(p).read()\nold='''    const charges = amounts.filter((a) => a.kind === \"charge\"), unclear = amounts.filter((a) => a.kind !== \"charge\");'''\nnew='''    const live = amounts.filter((a) => a.review_status !== \"dismissed\"), gone = amounts.filter((a) => a.review_status === \"dismissed\");   // T-136 (pass 5 F2): dismissed amounts wait under \"Dismissed (n)\"\n    const charges = live.filter((a) => a.kind === \"charge\"), unclear = live.filter((a) => a.kind !== \"charge\");'''\nassert old in s; s=s.replace(old,new,1)\nold='''    root.append(tray);\n  }'''\nnew='''    root.append(tray);\n    if (gone.length) {\n      const boil = repeated(gone);\n      root.append(RV.dismissedBox(\"amounts\", gone.length, el(\"table\", { class: \"rv-table\", \"data-testid\": \"dismissed-amounts\" }, el(\"caption\", { class: \"rv-sr\" }, \"Dismissed amounts\"),\n        el(\"thead\", {}, el(\"tr\", {}, [\"Amount\", \"From the record\", \"Status\", \"Decision\"].map((h) => el(\"th\", { scope: \"col\" }, h)))),\n        el(\"tbody\", {}, gone.map((a) => row(c, a, a.kind !== \"charge\", boil))))));\n    }\n  }'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nEOF\ngrep -n \"^  const RV\\|const RV\" flags.js charges.js | head -3; node --check flags.js charges.js review.js dom.js app.js export.js timeline.js mock.js && echo ok; grep -n \"dismissed-group\" *.css | head"
}
````

### User / tool · 2026-11-02T12:36:06.624Z

**tool result**
````
flags.js:6:  const RV = ZL.rv, el = (...a) => ZL.el(...a);
charges.js:5:  const RV = ZL.rv, el = (...a) => ZL.el(...a);
ok
styles.css:139:.dismissed-group { margin-top: var(--s-3); border: 1px solid var(--border); border-radius: var(--r-2); padding: 0 var(--s-3); background: var(--sunken); }
styles.css:140:.dismissed-group > summary { font-weight: var(--w-strong); }
styles.css:141:.dismissed-group[open] > summary { border-bottom: 1px solid var(--border); margin-bottom: var(--s-1); }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:36:18.860Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='stepper.js'; s=open(p).read()\nold='''  function gotoTray() {'''\nnew='''  // T-136: the first entry whose edit still waits for her comparison with the quote (the row carries data-edit-check).\n  function gotoFirstEdit() {\n    closeDialogs();\n    const node = document.querySelector('[data-testid=\"queue\"] [data-item-id][data-edit-check]') || document.querySelector('[data-item-id][data-edit-check]');\n    if (!node) return gotoFirstPending();\n    reveal(node); return true;\n  }\n  function gotoTray() {'''\nassert old in s; s=s.replace(old,new,1)\n\nold='''      case \"review\": {\n        const n = c.pending || 0;'''\nnew='''      case \"review\": {\n        const n = c.pending || 0, ed = c.edit_to_check || 0;\n        if (!n && ed) return { text: \"Compare \" + plural(ed, \"edit\", \"edits\") + \" with the quote, then click \\\\u201cI compared it with the quote\\\\u201d on \" + (ed === 1 ? \"it\" : \"each\") + \". Until you do, \" + (ed === 1 ? \"it stays\" : \"they stay\") + \" out of the letter.\", label: \"Go to the first edit to check\", go: () => gotoFirstEdit() };'''\nassert old in s; s=s.replace(old,new,1)\n\nold='''    return el(\"div\", { class: \"zs-gate-warns\", \"data-testid\": \"gate-warnings\" }, ws.map((w) => el(\"div\", { class: \"zs-warnbox\", \"data-testid\": \"gate-warning\", \"data-warning-code\": w.reason_code },\n      el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, \"Not reviewed (\" + (w.count != null ? w.count : \"\") + \"): \"), w.why || \"\"),\n      el(\"p\", { class: \"zs-ev\" }, \"This does not block the export.\"),\n      el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"btn-gate-warning-jump\", onclick: () => gotoFirstPending() }, \"Go to the first pending item\")))));'''\nnew='''    return el(\"div\", { class: \"zs-gate-warns\", \"data-testid\": \"gate-warnings\" }, ws.map((w) => {\n      const edit = w.reason_code === \"EDIT_NOT_CONFIRMED\";   // T-136 (T-134): her reworded entry is still marked Needs review; the server's own sentence says why it is not in the letter\n      return el(\"div\", { class: \"zs-warnbox\", \"data-testid\": \"gate-warning\", \"data-warning-code\": w.reason_code },\n        el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, (edit ? \"Edit to check (\" : \"Not reviewed (\") + (w.count != null ? w.count : \"\") + \"): \"), w.why || \"\"),\n        el(\"p\", { class: \"zs-ev\" }, \"This does not block the export.\"),\n        el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"btn\", \"data-testid\": \"btn-gate-warning-jump\", onclick: () => (edit ? gotoFirstEdit() : gotoFirstPending()) }, edit ? \"Go to the first edit to check\" : \"Go to the first pending item\")));\n    }));'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nEOF\nfor f in *.js; do node --check $f || echo BAD $f; done; grep -n \"const plural\\|plural =\" stepper.js | head -2"
}
````

### User / tool · 2026-11-02T12:36:20.053Z

**tool result**
````
223:  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:36:35.157Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_edit_to_check.py'; s=open(p).read()\ns=s.replace('''btn-gate-warning-jump (all declared in conftest).\"\"\"''','''btn-gate-warning-jump (all declared in conftest). New (declared in conftest): edit-compare-prompt, dismissed-group-flags / dismissed-group-amounts, dismissed-summary-flags / dismissed-summary-amounts,\ndismissed-flags, dismissed-amounts.\"\"\"''')\ns+='''\n\n# ---- paralegal pass 5 F1: one `a` never records the comparison\ndef test_one_a_press_does_not_record_the_comparison(page, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    row = _row(page, t[\"id\"]); d0, _, n0, k0 = _progress(page); assert k0 == 1\n    row.focus(); page.keyboard.press(\"a\"); page.wait_for_timeout(400)\n    assert row.get_attribute(\"data-review\") == \"edited\" and row.get_attribute(\"data-edit-check\") is not None, \"a recorded the comparison\"\n    assert next(x for x in _case(t[\"tok\"])[\"entries\"] if x[\"id\"] == t[\"id\"])[\"edit_to_check\"] is True\n    assert _progress(page) == (d0, _, n0, k0) or _progress(page)[0::2] == (d0, n0)\n    prompt = row.get_by_test_id(\"edit-compare-prompt\"); expect(prompt).to_be_visible()\n    assert \"not recorded\" in prompt.inner_text().lower() and \"i compared it with the quote\" in prompt.inner_text().lower()\n    assert page.evaluate(\"document.activeElement.getAttribute('data-testid')\") == \"btn-accept\", \"focus is on the confirm button\"\n    page.get_by_test_id(\"btn-export\").click(); page.get_by_test_id(\"btn-copy-letter\").click()\n    expect(page.get_by_test_id(\"copy-confirm\")).to_contain_text(\"1 edited entry still marked Needs review\")      # the copy warning is still there\n    page.get_by_test_id(\"btn-copy-cancel\").click(); page.go_back() if False else None\n\n\ndef test_enter_on_the_focused_confirm_button_records_it(page, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    row = _row(page, t[\"id\"]); row.focus(); page.keyboard.press(\"a\")\n    expect(row.get_by_test_id(\"edit-compare-prompt\")).to_be_visible()\n    page.keyboard.press(\"Enter\")\n    expect(row).to_have_attribute(\"data-review\", \"accepted\"); assert row.get_attribute(\"data-edit-check\") is None\n    assert _case(t[\"tok\"])[\"review\"][\"counts\"][\"edit_to_check\"] == 0\n\n\ndef test_start_review_then_a_does_not_confirm_either(page, edited_quote):\n    t = edited_quote\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    page.get_by_test_id(\"btn-start-review\").click()\n    page.keyboard.press(\"a\"); page.wait_for_timeout(400)\n    after = next(x for x in _case(t[\"tok\"])[\"entries\"] if x[\"id\"] == t[\"id\"])\n    assert after[\"edit_to_check\"] is True and after[\"review_status\"] == \"edited\", \"Start review then a confirmed the edit\"\n\n\n# ---- paralegal pass 5 F2: dismissed flags and amounts wait under Dismissed (n)\ndef test_dismissed_flags_and_amounts_wait_under_dismissed_n(page, sample_case):\n    c = _case(sample_case)\n    flag = next(f for f in c[\"flags\"] if f[\"state\"] != \"rejected\"); amt = next(a for a in c[\"amounts\"] if a[\"state\"] != \"rejected\")\n    open_case(page, sample_case)\n    fp, cp = page.get_by_test_id(\"flags-panel\"), page.get_by_test_id(\"charges-panel\")\n    n_open_flags = fp.locator(\"[data-item-id]\").count(); n_open_amts = cp.locator(\"[data-item-id]\").count()\n    fp.locator(f'[data-item-id=\"{flag[\"id\"]}\"]').get_by_test_id(\"btn-dismiss\").click()\n    cp.locator(f'[data-item-id=\"{amt[\"id\"]}\"]').get_by_test_id(\"btn-dismiss\").click()\n    g = fp.get_by_test_id(\"dismissed-group-flags\"); expect(g.get_by_test_id(\"dismissed-summary-flags\")).to_have_text(re.compile(r\"^Dismissed \\\\(1\\\\)\"))\n    a = cp.get_by_test_id(\"dismissed-group-amounts\"); expect(a.get_by_test_id(\"dismissed-summary-amounts\")).to_have_text(re.compile(r\"^Dismissed \\\\(1\\\\)\"))\n    assert g.locator(f'[data-item-id=\"{flag[\"id\"]}\"]').count() == 1 and fp.locator(f'[data-group] [data-item-id=\"{flag[\"id\"]}\"]').count() == 0, \"not in the open list\"\n    assert a.locator(f'[data-item-id=\"{amt[\"id\"]}\"]').count() == 1 and cp.locator(f'[data-group] [data-item-id=\"{amt[\"id\"]}\"]').count() == 0\n    assert fp.locator(\"[data-item-id]\").count() == n_open_flags and cp.locator(\"[data-item-id]\").count() == n_open_amts, \"rows moved, none lost\"\n    d0 = _progress(page)\n    for grp, iid in ((g, flag[\"id\"]), (a, amt[\"id\"])):\n        r = grp.locator(f'[data-item-id=\"{iid}\"]'); expect(r).to_have_attribute(\"data-review\", \"dismissed\")\n        assert r.get_by_test_id(\"btn-accept\").count() == 0\n        r.focus(); page.keyboard.press(\"a\"); page.wait_for_timeout(250)\n        expect(r).to_have_attribute(\"data-review\", \"dismissed\")\n    assert _progress(page) == d0\n    g.locator(f'[data-item-id=\"{flag[\"id\"]}\"]').get_by_test_id(\"btn-reset\").click()                     # Undo brings it back to the open list\n    expect(fp.locator(f'[data-group] [data-item-id=\"{flag[\"id\"]}\"]')).to_have_count(1)\n    expect(fp.get_by_test_id(\"dismissed-group-flags\")).to_have_count(0)\n'''\ns=s.replace('''    assert _progress(page) == (d0, _, n0, k0) or _progress(page)[0::2] == (d0, n0)\n''','''    d1, _, n1, k1 = _progress(page); assert (d1, n1, k1) == (d0, n0, k0), \"the header did not move\"\n''')\ns=s.replace('''; page.go_back() if False else None''','')\nopen(p,'w').write(s)\nEOF\ngrep -n \"dismissed-group\" tests/e2e/conftest.py | head -3; grep -rn \"dismissed-group\\|dismissed-summary\" tests/e2e/*.py | grep -v test_edit_to_check | head; grep -n \"def test\" tests/unit/test_e2e_contract.py | head"
}
````

### User / tool · 2026-11-02T12:36:35.289Z

**tool result**
````
59:  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
tests/e2e/conftest.py:59:  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
tests/e2e/test_polish_r4.py:3:New test ids (QA adds them to the tests/e2e/conftest.py docstring): gap-change-card, gap-change-removed, dismissed-group, dismissed-summary, dismissed-queue, edit-recheck-hint,
tests/e2e/test_polish_r4.py:111:    group = page.get_by_test_id("dismissed-group"); expect(group).to_have_count(1)
tests/e2e/test_polish_r4.py:112:    expect(page.get_by_test_id("dismissed-summary")).to_contain_text("Dismissed (1)")
tests/e2e/test_polish_r4.py:119:    expect(page.get_by_test_id("dismissed-group")).to_have_count(0)
tests/e2e/test_polish_r4.py:127:    expect(page.get_by_test_id("dismissed-summary")).to_contain_text("Dismissed (1)")
tests/e2e/test_polish_r4.py:128:    assert page.get_by_test_id("dismissed-group").get_attribute("open") is None
tests/e2e/test_polish_r4.py:130:    page.get_by_test_id("dismissed-summary").click()
13:def test_every_test_id_is_declared():
26:def test_data_attributes_declared():
33:def test_roles_and_inputs_and_keys_declared():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:36:41.714Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/conftest.py'; s=open(p).read()\nanchor=\"  A dismissed flag / amount / entry has NO btn-accept\"\nadd=\"\"\"  T-136: edit-compare-prompt (a visible line under the edit-check hint after the a key was pressed on an edit that still waits for her comparison: 'Not recorded yet ...'; a never records it, the btn-accept 'I compared it with the quote' does),\n  dismissed-group-flags / dismissed-group-amounts (a <details> at the end of the Flags / Charges panel, 'Dismissed (n)', rows keep Undo; opens for the item just dismissed) with dismissed-summary-flags / dismissed-summary-amounts, dismissed-flags (rows) and dismissed-amounts (table).\n\"\"\"\nassert anchor in s; s=s.replace(anchor, add+anchor,1); open(p,'w').write(s)\n\np='tests/e2e/test_polish_r5.py'; s=open(p).read()\nold='''    page.get_by_test_id(\"entry-3\").focus(); page.keyboard.press(\"a\")\n    expect(page.locator(\"#rv-live\")).to_contain_text(\"Nothing left to decide\")'''\nnew='''    page.get_by_test_id(\"entry-3\").focus(); page.keyboard.press(\"a\")                    # T-136: a only asks; the confirm button records it\n    expect(page.get_by_test_id(\"entry-3\").get_by_test_id(\"edit-compare-prompt\")).to_be_visible()\n    page.keyboard.press(\"Enter\")\n    expect(page.locator(\"#rv-live\")).to_contain_text(\"Nothing left to decide\")'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nEOF\ncd /private/tmp/claude-501/wt-t136 && for f in app/frontend/*.js; do :; done; rsync -a /Users/arsis/zlayt-pm-project/app/frontend/ app/frontend/ && cp /Users/arsis/zlayt-pm-project/tests/e2e/{test_edit_to_check,conftest,test_polish_r5}.py tests/e2e/ && ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 E2E_BASE_URL=http://localhost:7931 .venv/bin/python -m pytest tests/e2e/test_edit_to_check.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T12:37:00.292Z

**tool result**
````
...F......                                                               [100%]
=================================== FAILURES ===================================
_____________ test_the_next_step_names_the_edit_not_a_pending_item _____________

page = <Page url='http://localhost:7931/#/case/IPdbum94LvNn3EWTStM1TQ'>
edited_quote = {'tok': 'IPdbum94LvNn3EWTStM1TQ', 'id': 'e2', 'before': (0, 23, 4, 0), 'orig': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'}

    def test_the_next_step_names_the_edit_not_a_pending_item(page, edited_quote):
        t = edited_quote; c = _case(t["tok"])
        for it in c["entries"] + c["amounts"] + c["flags"]:                        # decide everything else, so only the edit waits
            if it["id"] != t["id"] and it["review_status"] == "pending" and it["state"] != "rejected":
                api("POST", f"/api/cases/{t['tok']}/items/{it['id']}/review", {"action": "dismiss"})
        page.reload(); page.get_by_test_id("timeline").wait_for()
        nxt = page.get_by_test_id("case-next-action"); expect(nxt).to_be_visible()
        txt = nxt.inner_text().lower()
>       assert "0 pending" not in txt and "edit" in txt and "quote" in txt, txt
E       AssertionError: what you need to do: the second ai check did not run on 1 item. run it again; accepted items it never checked cannot go in the letter.
E         
E         show this step
E       assert ('0 pending' not in 'what you ne...ow this step'
E         
E         '0 pending' is contained here:
E         ? ---
E           w this step and 'edit' in 'what you need to do: the second ai check did not run on 1 item. run it again; accepted items it never checked cannot go in the letter.\n\nshow this step')

tests/e2e/test_edit_to_check.py:120: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_edit_to_check.py::test_the_next_step_names_the_edit_not_a_pending_item
1 failed, 9 passed in 18.26s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:37:07.854Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_edit_to_check.py'; s=open(p).read()\nold='''    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    nxt = page.get_by_test_id(\"case-next-action\")'''\nnew='''    def settled_judges(route):      # the store write that put the entry into Needs review also leaves its second check unrun: show that step as passed so the review step is the one waiting on her\n        d = route.fetch().json()\n        for st in d.get(\"steps\", []):\n            if st[\"id\"] == \"judges\":\n                st.update(status=\"pass\", next_action=None, counts=dict(st.get(\"counts\") or {}, unavailable=0), reason_code=None)\n        route.fulfill(json=d)\n    page.route(re.compile(r\"/api/cases/[^/]+/trace$\"), settled_judges)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    nxt = page.get_by_test_id(\"case-next-action\")'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nEOF\ncp tests/e2e/test_edit_to_check.py /private/tmp/claude-501/wt-t136/tests/e2e/ && cd /private/tmp/claude-501/wt-t136 && ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 E2E_BASE_URL=http://localhost:7931 .venv/bin/python -m pytest tests/e2e/test_edit_to_check.py -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T12:37:26.700Z

**tool result**
````
..........                                                               [100%]
10 passed in 18.53s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:37:30.477Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && ZLAYT_DB=/private/tmp/claude-501/t136db/app.sqlite3 E2E_BASE_URL=http://localhost:7931 .venv/bin/python -m pytest tests/e2e -q -x -p no:cacheprovider 2>&1 | tail -30",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T12:42:48.720Z

**tool result**
````
........................................................................ [ 31%]
................s....................................................... [ 62%]
........................................................................ [ 93%]
................                                                         [100%]
231 passed, 1 skipped in 317.98s (0:05:17)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:42:54.507Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/wt-t136 && .venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -8",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T12:43:16.700Z

**tool result**
````
E       AssertionError: ['btn-edit-excerpt', 'btn-copy-cancel']
E       assert not ['btn-edit-excerpt', 'btn-copy-cancel']

tests/unit/test_e2e_contract.py:24: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 774 passed in 21.51s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:43:19.580Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/conftest.py'; s=open(p).read()\ns=s.replace(\"  T-136: edit-compare-prompt\",\"  T-136: btn-edit-excerpt ('Change quote' on an entry row; opens excerpt-editor), btn-copy-cancel ('Go back' in copy-confirm), edit-compare-prompt\",1)\nopen(p,'w').write(s)\nEOF\ncp tests/e2e/conftest.py /private/tmp/claude-501/wt-t136/tests/e2e/ && cd /private/tmp/claude-501/wt-t136 && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -5",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T12:46:29.935Z

**tool result**
````
........................................................................ [ 95%]
........................................................................ [ 97%]
........................................................................ [ 99%]
..........                                                               [100%]
3321 passed, 1 skipped in 188.86s (0:03:08)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:36.680Z

Now commit, board, memory, restart shared app, stop my server.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:37.923Z

**tool call — Bash**
````
{
 "command": "kill $(cat /private/tmp/claude-501/t136db/pid); git worktree remove --force /private/tmp/claude-501/wt-t136; git add app/frontend/review.js app/frontend/dom.js app/frontend/app.js app/frontend/export.js app/frontend/timeline.js app/frontend/stepper.js app/frontend/flags.js app/frontend/charges.js app/frontend/mock.js tests/e2e/test_edit_to_check.py tests/e2e/conftest.py tests/e2e/test_polish_r5.py && git status --short app/frontend tests/e2e | head"
}
````

### User / tool · 2026-11-02T12:46:38.344Z

**tool result**
````
M  app/frontend/app.js
M  app/frontend/charges.js
M  app/frontend/dom.js
M  app/frontend/export.js
M  app/frontend/flags.js
M  app/frontend/mock.js
M  app/frontend/review.js
M  app/frontend/stepper.js
M  app/frontend/timeline.js
M  tests/e2e/conftest.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:41.601Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/t136db/msg.txt <<'EOF'\nfeat(frontend): T-136 read item.edit_to_check and review.counts.edit_to_check; a never records the comparison; dismissed flags and amounts under Dismissed (n); EDIT_NOT_CONFIRMED gate warning\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\nEOF\nP=\"app/frontend/review.js app/frontend/dom.js app/frontend/app.js app/frontend/export.js app/frontend/timeline.js app/frontend/stepper.js app/frontend/flags.js app/frontend/charges.js app/frontend/mock.js tests/e2e/test_edit_to_check.py tests/e2e/conftest.py tests/e2e/test_polish_r5.py\"\ngit commit -F /private/tmp/claude-501/t136db/msg.txt -- $P 2>&1 | tail -3; git log --oneline | head -1"
}
````

### User / tool · 2026-11-02T12:46:42.485Z

**tool result**
````
[main 671f054] feat(frontend): T-136 read item.edit_to_check and review.counts.edit_to_check; a never records the comparison; dismissed flags and amounts under Dismissed (n); EDIT_NOT_CONFIRMED gate warning
 12 files changed, 279 insertions(+), 16 deletions(-)
 create mode 100644 tests/e2e/test_edit_to_check.py
671f054 feat(frontend): T-136 read item.edit_to_check and review.counts.edit_to_check; a never records the comparison; dismissed flags and amounts under Dismissed (n); EDIT_NOT_CONFIRMED gate warning
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:47.994Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-136 --check 1 --agent frontend --evidence \"tests/e2e/test_edit_to_check.py (10 pass, clean worktree HEAD+diff, own port); full e2e 231 pass/1 skip; unit 3321 pass\" && $B note T-136 --agent frontend --text \"Done: ZL.editToCheck = item.edit_to_check; ZL.editCount reads review.counts.edit_to_check (header 'including N edit to check', strip, copy-confirm); gate warning EDIT_NOT_CONFIRMED shows with the server's why and a jump to the first edit; case next step names the edit; a on an edit row only focuses the compare button with a visible prompt (Enter/click records); dismissed flags/amounts under Dismissed (n). Not done (not in scope list): paralegal F1 residuals - Needs review chip beside Accepted after compare, export bar '0 items pending' wording, copy warning naming the record.\" && $B handoff T-136 --agent frontend --text \"What changed: UI reads item.edit_to_check and review.counts.edit_to_check (header, strip, copy-confirm); quote-picker edit shows the 'I compared it with the quote' Accept; EDIT_NOT_CONFIRMED gate warning + next-step text; a never records the comparison (prompt + focus on button); Dismissed (n) groups for flags and amounts (testids dismissed-group-flags/-amounts). Commit 671f054. How verified: tests/e2e/test_edit_to_check.py written first (6 red before), 10 pass; full e2e 231 pass on clean worktree own port; unit 3321 pass. Left: F1 residuals (chip beside Accepted after compare, export bar pending wording, record name in copy warning) not in this card's list. Surprise: fixture set verifies every entry, so e2e puts an entry into Needs review via ZLAYT_DB (skips without it).\" && $B move T-136 in_review --agent frontend && $B commit T-136 --sha 671f054 --agent frontend; tools/serve_app.sh"
}
````

### User / tool · 2026-11-02T12:46:50.416Z

**tool result**
````
AC 1 checked: tests/e2e/test_edit_to_check.py (10 pass, clean worktree HEAD+diff, own port); full e2e 231 pass/1 skip; unit 3321 pass
noted on T-136
handoff written on T-136
T-136: in_progress -> in_review
T-136: commit 671f054 recorded
app http 200 on :7860
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:52.902Z

Memory note.

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:46:58.300Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/frontend && cat > project_t136_edit_to_check.md <<'EOF'\n---\nname: t136-edit-to-check\ndescription: T-136 hooks: item.edit_to_check source of truth, ZL.editCount, a-key prompt, Dismissed groups for flags/amounts, ZLAYT_DB test recipe\nmetadata:\n  type: project\n---\n`ZL.editToCheck(i)` is now `i.edit_to_check === true` (server flag, T-134); `ZL.editCount(c)` reads `c.review.counts.edit_to_check` (fallback: count of items) and feeds progressOf.edits, the strip (clamped to open entries), copy-confirm. Header: \"N items need review, including K edits to check\". Mock API sets edit_to_check too.\n`a` on an edit row never records \"I compared it with the quote\": `askCompare` (review.js) shows `edit-compare-prompt` and focuses btn-accept; Enter/click records. Start review then `a` is the same path.\nGate warning EDIT_NOT_CONFIRMED: stepper.js warningNode (heading \"Edit to check (n)\", jump `gotoFirstEdit`); caseCopy \"review\" step names the edit when counts.pending is 0.\nDismissed flags/amounts: `RV.dismissedBox(kind, n, body)` (kinds \"flags\"/\"amounts\", open state `ZL.dismissedOpenBy`), testids dismissed-group-flags/-amounts. Dismissed rows are outside `[data-group]`.\n**Test recipe:** the curated fixture verifies every entry, so e2e needs ZLAYT_DB and `DB.update_item(conn, id, case=tok, state=\"needs_review\")` to force Needs review (reasons cannot be written; the edit response adds JUDGE_UNAVAILABLE). That also makes the case-checks active step \"judges\"; stub /trace to pass it when testing the review step text.\nOpen residuals from paralegal pass 5 F1 (not done): Needs review chip stays beside Accepted after compare, export bar \"0 items pending\" wording, copy warning naming the record.\nEOF\necho \"- [T-136 edit_to_check](project_t136_edit_to_check.md) — server flag, a-key prompt, Dismissed groups, ZLAYT_DB test recipe, open F1 residuals\" >> MEMORY.md"
}
````

### User / tool · 2026-11-02T12:46:58.385Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T12:47:02.372Z

T-136 is in `in_review` (commit 671f054) and the shared app is restarted on :7860.
The UI now reads `item.edit_to_check` and `review.counts.edit_to_check`, so a quote-picker edit shows as open with "I compared it with the quote". It also shows the EDIT_NOT_CONFIRMED gate warning. The expanded scope is in: `a` no longer records the comparison, and dismissed flags and amounts collapse under "Dismissed (n)". I wrote `tests/e2e/test_edit_to_check.py` first, 6 of its tests failing before the change. Now all 10 of its tests pass, as do the full e2e run (231 passed, 1 skipped) and the unit suite (3321 passed), on a clean worktree and my own port.
Not done, since they were outside the list you gave: the Needs review chip still sits beside Accepted after the compare, the export bar's "0 items pending" wording, and the copy warning naming the record. The new e2e needs `ZLAYT_DB` and skips without it, because the fixture set verifies every entry.
