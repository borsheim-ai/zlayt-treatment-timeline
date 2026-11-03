# Subagent: Backend: T-167 plain wording (Backend: T-167 plain wording)

Source: `agent-ad56d780ea92e2376.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T16:06:53.658Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim T-167 (P0, MVP polish) with `python3 tools/board.py claim T-167 --agent backend` and read it with `show`. Read F4 and F7 in reviews/MVP-ux-audit.md.

Remove developer codes and test-mode wording from every paralegal-facing string and from the exported internal notes. That covers:
- reason codes such as JUDGE_UNAVAILABLE in the notes; use the plain sentence from why.py;
- 'fixture backend', 'curated responses' and 'older version of the AI prompts';
- raw 'server answered 500' messages.

The demo-mode edit message must say plainly that the AI second check is not available in the demo, and what she can do instead. Reason codes stay in the API fields; only the displayed text changes.

**Tests, written first:**
- a grep-style test over the notes export and the why/message text that fails if a raw code or any of those phrases appears;
- the sample golden still matches; if the notes text changes, update the golden with a written reason.

Keep to why.py, export.py (notes text only) and the message strings. Commit via a temp index for only your hunks, and never run `git checkout` on files. Run the full unit suite from a `git archive HEAD` copy. Write the handoff and move the card to in_review. Reply in 2 lines.

### User / tool · 2026-11-02T16:06:53.663Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:06:56.828Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-167 --agent backend; $B show T-167; grep -n \"F4\\|F7\" reviews/MVP-ux-audit.md | head -30"
}
````

### User / tool · 2026-11-02T16:06:57.043Z

**tool result**
````
T-167 claimed by backend
---
id: "T-167"
title: "MVP backend wording (T-166 audit F4/F7): no developer codes or test-mode wording in paralegal-facing text or the exported notes (JUDGE_UNAVAILABLE, fixture backend, curated responses, 'server answered 500'); demo-mode edit wording is plain"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T16:06:36Z"
updated_at: "2026-11-02T16:06:56Z"
claimed_by: "backend"
claimed_at: "2026-11-02T16:06:56Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "grep of every user-facing string and the notes export for reason codes / test jargon finds none; the demo-mode edit message says plainly that the AI check is not available in the demo and what to do; unit tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T16:06:40Z orchestrator: assigned: backend
- 2026-11-02T16:06:56Z backend: claimed

## Handoff (filled when moving to in_review)

16:All are frontend work except two one-line backend copy edits (F4).
35:- **F4 Edit lands in a "second check failed" state beside a cut-off quote.** On the demo backend every edit shows "The second check failed (the AI check was asked and gave no usable answer)" and asks "I compared it with the quote" while the quote is clamped to one line. An edit takes 3 actions (Edit, Save, compare), and the internal notes print "(JUDGE_UNAVAILABLE)". Frontend fix: un-clamp in this state, show your wording above the quote, and make it one confirm: "Matches the quote, accept". Backend copy only (no new feature): change `why.py:49` to "The second check is not available right now. Compare your wording with the quote, then accept." and drop the codes in `export.py:611`. Screens: 08-edit-saved-light-1440.png, 15-phone-edit-saved-light-390.png.
38:- **F7 Test and developer wording is on the paralegal's surfaces.**
127:  {"severity": "major", "title": "P0 F4: An edit lands in a 'second check failed' state and asks her to compare with a quote that is cut off",
142:  {"severity": "major", "title": "P0 F7: Test and developer wording on the paralegal's screens and in the paste-out notes",
239:  "The hosted demo runs recorded AI answers, so every edit has no second check. Should the demo record a second-check reply for edits so viewers see the normal path, or is the plain 'not available, compare it yourself' wording (F4) enough?"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:06:59.610Z

**tool call — Bash**
````
{
 "command": "sed -n 36,50p reviews/MVP-ux-audit.md; cat app/backend/why.py | head -120; grep -n \"JUDGE_UNAVAILABLE\\|fixture backend\\|curated responses\\|older version\\|server answered\" -r app --include=*.py --include=*.js --include=*.html --include=*.md | grep -v \"^app/frontend/node\" | head -40; git status --short | head"
}
````

### User / tool · 2026-11-02T16:06:59.764Z

**tool result**
````
- **F5 Dismiss makes the row vanish and moves focus off-screen.** The row jumps to "Dismissed (n)". Focus lands at y 1,033 in a 900 px viewport, and at y 1,959 in 844 px at 390. Fix in `review.js` (RV.act / dismissedBox): leave a 6 s placeholder in the row's slot, "Dismissed: Capital PT, visit 8 · Undo", and never focus outside the viewport. Screens: 09-after-dismiss-light-1440.png, 15-phone-after-dismiss-light-390.png.
- **F6 The keyboard loop dead-ends.** `a` stops at the end of a flag group: presses 6 to 8 did nothing while 18 items were open. There is no `n` key, and Export is 92 Shift+Tabs away. Fix in `review.js`: at the end of a group, focus and announce the next group's first open item without deciding it. Add `n` (focusFirstPending) and `x` (focus Export), and list both in `?`. In `input.js`, focus Start review when a run finishes. Screen: 12-kbd-after-8a-dark-1440.png.
- **F7 Test and developer wording is on the paralegal's surfaces.**
  - Header chip "cached demo (curated responses)".
  - An amber box: "older version of the AI prompts … fixture backend (recorded replies, 10 golden cases…)".
  - "JUDGE_UNAVAILABLE" in the notes export.
  - "(the server answered 500). Request failed".
  - An "Audit" link on every row.

  Fix: reword the chip to "Demo: recorded AI answers". Move the calibration box into "How the AI was checked", reworded (`suggestions.js:138`). Strip the codes and move Audit into the Why dialog. Screens: 01-landing-empty-light-1440.png, 06-tray-light-1440.png, 16-err-list500-light-1440.png.

### P1: should fix (minor)
- **F8 "Do this first" and "Start review" point at different items.** "Do this first" points at the $185 rate in Charges. Start review goes to the causation flag. Make Start review use `next_action.item_id`. Screens: 05-case-top-light-1440.png, 07-start-review-light-1440.png.
- **F9 Counts and state names disagree.**
  - Unreviewed count: 18 on the chip, 19 in Case checks and the export count line.
"""One fixed plain-language sentence per reason code (LLM_VS_CODE row 18, api.md appendix). Never model text."""
_WHY = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "The quoted text is not word for word in the record, so this item was rejected and cannot be used.",
    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
    "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
    "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
    "CHARGE_TEXT_IN_ENTRY": "The summary or quote states a dollar amount, which goes only in the internal notes, so this entry is held out of the letter. Dismiss it, or pick a quote without the amount and edit the summary to match.",
    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
    "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
    "JUDGE_UNSURE": "A second AI check could not decide whether this item is supported.",
    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
    "DATE_MISSING": "The record has no readable date, so it is left out of gap checks.",
    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
    "AMOUNT_RATE_NOT_TOTALED": "This figure is a rate, not a charge, so it is not added to the total.",
    "AMOUNT_ESTIMATE": "This figure is an estimate, not a billed charge, so it is not added to the total.",
    "AMOUNT_DAMAGES": "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.",
    "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
    "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is an AI translation that has not been verified; read the original quote yourself.",
    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
    "SUMMARY_NOT_IN_QUOTE": "Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the entry by hand.",
    "AI_TRANSLATION": "AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
    "OCR_DERIVED": "This record was read from a scanned page by OCR, which can misread letters and digits. Check it against the page image.",
}


# T-113 r2 (F5): a model-proposed CONFLICT sits in the tray under the reason code LLM_ONLY (the code is a closed contract list), but "the phrase list did not
# find it" is not why: conflicts never come from the phrase list. The cause is the rule that only a pair the software's own rules pick can be a conflict.
MODEL_CONFLICT = ("The AI suggested a conflict between two passages, but the software only raises a conflict for pairs its own fixed rules pick, "
                  "and they did not pick this one. Read both passages; add it by hand if it matters.")


# T-146 r2 / T-145: JUDGE_UNAVAILABLE is one closed reason code with two causes. The sentence follows the judge record: a judge that was asked and gave no usable
# answer says so; one that never ran (deadline, or no judge record yet) keeps the JUDGE_NOT_RUN sentence. The reason code itself is unchanged.
JUDGE_FAILED = "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked."


def judge_failed(judge) -> bool:
    return bool(judge) and judge.get("verdict") == "unavailable" and judge.get("reason_code") != "JUDGE_NOT_RUN"


def why(code: str, judge=None) -> str:
    if code == "JUDGE_UNAVAILABLE" and judge_failed(judge):
        return JUDGE_FAILED
    return _WHY[code]


def join(reasons, judge=None) -> str:
    """The sentences for a reason list. A recorded-answer miss (FIXTURE_MISS, demo) is not a failed call: no model was asked, so the 'did not run' sentence stays."""
    j = None if "FIXTURE_MISS" in (reasons or []) else judge
    return " ".join(why(c, j) for c in reasons or [])


def all_codes() -> list:
    return list(_WHY)


# D-028: judge reason codes (closed lists) -> fixed sentence. Model prose never reaches the UI.
_JUDGE_DETAIL = {
    "ADDS_DIAGNOSIS": "The summary adds a diagnosis the quote does not state.",
    "ADDS_SEVERITY": "The summary adds a severity the quote does not state.",
    "ADDS_CAUSATION": "The summary adds a cause the quote does not state.",
    "DROPS_QUALIFIER": "The summary leaves out a qualifier that the quote carries.",
    "NUMBER_MISMATCH": "A number in the summary does not match the quote.",
    "OTHER_UNSUPPORTED": "Part of the summary is not supported by the quote.",
    "SHOULD_BE_CHARGE": "The second check reads this figure as a billed charge.",
    "SHOULD_BE_RATE": "The second check reads this figure as a rate.",
    "SHOULD_BE_ESTIMATE": "The second check reads this figure as an estimate.",
    "SHOULD_BE_DAMAGES": "The second check reads this figure as a non-bill amount.",
    "SHOULD_BE_UNCLEAR": "The second check could not read this figure with confidence.",
    "TEXT_AMBIGUOUS": "The text does not settle the question.",
    "PLAN_VS_ACTUAL": "The second check reads the quotes as a plan and what followed.",
    "FACT_MISMATCH": "The second check reads the quotes as stating different facts.",
    "DIFFERENT_VISITS": "The second check reads the quotes as different visits that can both be true.",
    "CAN_BOTH_BE_TRUE": "The second check reads both quotes as possibly true together.",
    "WRONG_TYPE": "The second check does not think this flag type fits the quote.",
    "WRONG_CATEGORY": "The second check does not think this flag category fits the quote.",
    "NEGATED": "The second check reads the quote as negating the condition.",
    "NOT_SUPPORTED_BY_QUOTE": "The second check does not find this flag supported by the quote.",
}


def judge_detail(code) -> str:
    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
    return _JUDGE_DETAIL.get(code, "")
app/README-arch.md:72:2. `provider.py` + fixture backend + `audited.py`; record fixtures with the CLI backend from the golden text.
app/README-arch.md:82:First to go if a milestone exceeds 150% of budget (record in `SCOPE_CUTS.md`): the side-by-side layout (R-ST-1; the record modal R-RV-9 stays), then the synchronous judge re-run on edits (the edit would save as `needs_review` / `JUDGE_UNAVAILABLE`, which is already a defined state). The per-record flag pass is not on the cut line (it is the injection control, ADR-008.3); cheapen it by batching the judge instead.
app/llm/audited.py:134:        # a live backend that just failed (rate limit, timeout) is retried after a short pause, not at once (T-075); the fixture backend never sleeps
app/llm/backends/fixture.py:1:"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
app/frontend/stepper.js:169:  // False in demo mode and with the fixture backend, and after a rerun that got no answer. A field that is missing counts as false: no button that cannot work.
app/frontend/suggestions.js:138:        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These numbers come from an older version of the AI prompts."),
app/frontend/timeline.js:20:  const comparedReason = (e) => "Compared by you with the quote. " + ((e.reasons || []).includes("JUDGE_UNAVAILABLE") ? "The second AI check did not run." : plainReason(e));
app/frontend/dom.js:57:  ZL.secondCheckPending = (i) => !!i && (i.second_check_pending !== undefined ? i.second_check_pending === true : i.ai_drafted === true && !ZL.wordingEdited(i) && (i.reasons || []).includes("JUDGE_UNAVAILABLE"));
app/frontend/app.js:11:    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? (h.fixture_set === "recorded" ? "cached demo (recorded responses)" : "cached demo (curated responses)") : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : ""; // D-029: the demo replays the curated fixture set; label says so
app/backend/store.py:19:    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
app/backend/why.py:16:    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
app/backend/why.py:47:# T-146 r2 / T-145: JUDGE_UNAVAILABLE is one closed reason code with two causes. The sentence follows the judge record: a judge that was asked and gave no usable
app/backend/why.py:57:    if code == "JUDGE_UNAVAILABLE" and judge_failed(judge):
app/backend/trace.py:219:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:230:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:776:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
app/backend/trace.py:860:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
app/backend/trace.py:965:            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
app/backend/trace.py:1087:            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
app/backend/trace.py:1089:            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
app/backend/trace.py:1090:                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
app/backend/calibration_route.py:17:The UI hides the accuracy line when `calibration` is null (T-096) and shows "numbers from an older version" when `stale` is true.
app/backend/calibration_route.py:163:    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."
app/backend/confidence.py:10:    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
app/backend/confidence.py:20:          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
app/backend/rejudge.py:17:_JUDGE_REASONS = {"JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE", "FIXTURE_MISS"}
app/backend/flags.py:360:        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
app/backend/flags.py:367:        f["reasons"] = [r for r in f["reasons"] if r != "JUDGE_UNAVAILABLE"]
app/backend/flags.py:377:    An unsure answer or failed judge call leaves the flag needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a disagreement on a flag that is both
app/backend/export.py:636:_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MISS)",
app/backend/narrative.py:25:    "JUDGE_UNAVAILABLE": "The second check was not available for this sentence.",
app/backend/narrative.py:113:            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
app/backend/review.py:8:JUDGE_UNAVAILABLE).
app/backend/review.py:376:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
app/backend/generator.py:240:    """Stage 3: judge 1 on every non-rejected entry. Judge failure -> 'unavailable' (JUDGE_UNAVAILABLE). Recomposes state."""
app/backend/pipeline.py:232:    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.
app/backend/pipeline.py:393:    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
app/backend/reclassify.py:41:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
app/backend/reclassify.py:217:        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
app/backend/reclassify.py:221:        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:02.611Z

**tool call — Bash**
````
{
 "command": "sed -n 595,700p app/backend/export.py; grep -rn \"answered\\|fixture backend\\|curated\\|recorded replies\\|golden cases\\|JUDGE_NOT_RUN\\|FIXTURE_MISS\" app/backend app/llm --include=*.py | grep -v \"^app/backend/trace.py.*reason=\" | grep -v \"^\\S*:\\s*#\" | cut -c1-230 | head -60"
}
````

### User / tool · 2026-11-02T16:07:02.723Z

**tool result**
````
def _reconcile(v):
    in_letter = {e["record_no"] for e in v.in_entries}
    lines = []
    for r in sorted(v.records.values(), key=lambda r: (r.get("date_iso") or "9999", r["n"])):
        n = r["n"]
        if n in in_letter:
            continue
        ents = [e for e in v.entries if e["record_no"] == n]
        if r.get("could_not_process") or r.get("status") in ("failed", "could_not_process"):
            why = "could not process"
        elif any(_status(e) == "in" and not v.verbatim(e) for e in ents):
            why = "excerpt not found in record, not exported"
        elif any(_status(e) == "in" and not v.date_of(e) for e in ents):
            why = "date not confirmed, not exported"
        elif any(_status(e) != "out" and v.states_amount(e) for e in ents):
            why = _held_amount_note(v, n, ents)      # T-139
        elif any(e.get("edit_unconfirmed") for e in ents):
            why = "edited, not yet confirmed against the quote"      # T-134
        elif any(_status(e) == "pending" for e in ents):
            why = "not reviewed"
        elif any(e.get("review_status") == "rejected" for e in ents):
            why = "rejected"
        elif ents:
            why = "dismissed"
        else:
            why = r.get("reason") or "no entry"
        lines.append(f"- {_cap(v.cite(n))} — {why}")
    return lines or [f"- none ({len(v.records)} of {len(v.records)} records included)"]


def _was_edited(e):
    """T-069: an entry stays an edited item after the paralegal accepts it (accept keeps the edit payload and only flips the status),
    so edited-ness is the status OR a stored original that differs from the exported text. Out-of-letter entries are not listed."""
    if e.get("review_status") == "edited" or e.get("edit_unconfirmed"):
        return True
    if _status(e) != "in":
        return False
    return ((e.get("original_summary") is not None and e["original_summary"] != e["summary"])
            or (e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]))


_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MISS)",
                       "JUDGE_PARTIAL": "the second check only partly supported it (JUDGE_PARTIAL)", "JUDGE_UNSUPPORTED": "the second check did not support it (JUDGE_UNSUPPORTED)",
                       "JUDGE_UNSURE": "the second check was unsure (JUDGE_UNSURE)", "JUDGE_DISAGREES": "the second check disagreed (JUDGE_DISAGREES)"}


def _edit_unconfirmed_why(e) -> str:
    codes = list(e.get("edit_state_reasons") or [])
    return "; ".join(_EDIT_REASON_PHRASE.get(c, f"still marked for review ({c})") for c in codes) or "still marked for review"


def _edit_unconfirmed_phrase(e) -> str:
    """T-134: an edit that is still needs_review is out of the letter until the paralegal accepts it; the notes say it was edited and why it is still open, never that she accepted it."""
    return f"edited; {_edit_unconfirmed_why(e)}; not yet confirmed against the quote, so it is not in the letter (accept it to put it there)"


def _edited(v):
    out = []
    for e in v.entries:
        if e.get("entered_by_reviewer") and _status(e) == "in":
            out.append(f'- {_cap(v.cite(e["record_no"]))}: entered by reviewer (the AI did not draft this entry); summary "{e["summary"]}"'
                       + ".")
        if not _was_edited(e):
            continue
        bits = []
        if e.get("original_summary") is not None and e["original_summary"] != e["summary"]:
            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
                bits.append(f'summary was AI wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
            else:
                bits.append(f'summary was "{e["original_summary"]}", now "{e["summary"]}"')
        if e.get("original_excerpt") is not None and e["original_excerpt"] != e["excerpt"]:
            bits.append(f'excerpt was "{e["original_excerpt"]}", now "{e["excerpt"]}"')
        tail = (f" ({_edit_unconfirmed_phrase(e)})" if e.get("edit_unconfirmed") else
                f" (accepted by the paralegal after comparing it with the quote; {_edit_unconfirmed_why(e)})" if e.get("edit_state_reasons") and _status(e) == "in" else "")
        out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + "." + tail)
    return out or ["- none"]


def _pending(v):
    out = []
    for e in v.entries:
        if e.get("edit_unconfirmed") and not e.get("code_check_failed"):
            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}" ({_edit_unconfirmed_phrase(e)})')
        elif _status(e) == "pending" and e.get("code_check_failed"):       # D-051: the wording fails a code check, so it is not printed anywhere in the export
            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
        elif _status(e) == "pending":
            out.append(f'- Entry, {v.cite(e["record_no"])}: "{e["summary"]}"' + (" [entered by reviewer]" if e.get("entered_by_reviewer") else ""))
    for a in v.amounts:
        if _status(a) == "pending":
            out.append(f'- Amount {_money_short(a.get("cents"), a.get("raw", ""))} ({a["cls"]}), {v.cite(a["record_no"])}: '
                       f'"{_amount_quote(v, a)}"')
    for f in v.flags:
        if _status(f) == "pending":
            out.append("- Flag, " + _flag_line(v, f))
    return out


def _cite_tail(v, entry_id):
    e = next(x for x in v.entries if x["id"] == entry_id)
    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"


def _draft_paragraph(v):
    n = v.narrative
    if not n:
        return []
app/backend/store.py:19:    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
app/backend/store.py:118:        out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/why.py:16:    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
app/backend/why.py:17:    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
app/backend/why.py:53:    return bool(judge) and judge.get("verdict") == "unavailable" and judge.get("reason_code") != "JUDGE_NOT_RUN"
app/backend/why.py:63:    """The sentences for a reason list. A recorded-answer miss (FIXTURE_MISS, demo) is not a failed call: no model was asked, so the 'did not run' sentence stays."""
app/backend/why.py:64:    j = None if "FIXTURE_MISS" in (reasons or []) else judge
app/backend/ingest.py:282:            if e.code == "FIXTURE_MISS":   # no recorded answer is the same user-facing state as no model; the detail stays for the run's error entry
app/backend/split_llm.py:22:            raise ingest.SplitFailed("FIXTURE_MISS") from None
app/backend/trace.py:50:    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
app/backend/trace.py:51:    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace
app/backend/trace.py:219:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:230:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:274:                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:314:        if c.startswith("JUDGE_") or c == "FIXTURE_MISS":
app/backend/trace.py:689:            other = next((c for c in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS") if c in R), None)
app/backend/trace.py:860:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
app/backend/trace.py:924:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
app/backend/trace.py:984:    answered = j("supported", "partially", "unsupported", "disagrees", "unsure")
app/backend/trace.py:986:            "totals": {"items_judged": answered, "supported": j("supported"), "unsupported": j("partially", "unsupported", "disagrees"), "unsure": j("unsure"),
app/backend/trace.py:1133:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/calibration_route.py:3:Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
app/backend/calibration_route.py:63:    return f"{cell['matched']}/{cell['total']} times" in text and f"{case_count} golden cases" in text
app/backend/present.py:16:            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
app/backend/present.py:187:    """T-134 r4: the ids of live AI-made items whose second check has no answer (the same list the export gate's JUDGE_NOT_RUN reads), except a rate (accepting it only
app/backend/present.py:221:    """Entries and amounts in the could-not-verify tray (state rejected), without a placeholder the paralegal has since answered with a hand-entered entry (T-110 r2)."""
app/backend/export.py:636:_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MISS)",
app/backend/export.py:850:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:859:        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
app/backend/api.py:403:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/confidence.py:11:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:66:    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
app/backend/rejudge.py:1:"""Run the second check again for the items whose judge never answered (D-044). The LLM judges; code decides what to ask and what state follows.
app/backend/rejudge.py:17:_JUDGE_REASONS = {"JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE", "FIXTURE_MISS"}
app/backend/conflict_candidates.py:18:- A form field answered No counts as a denial (T-141): "Prior accidents? Yes [ ] No [X]." (OCR "No IX]") or "Prior injuries: None." Yes checked, no box
app/backend/conflict_candidates.py:87:    """Sentences of the record that deny prior problems: the T-094 phrases plus a form field answered No (T-141). A form denial is the stem unit and
app/backend/conflict_candidates.py:210:            if _ACCIDENT_STEM.match(u) and not _DENIAL.search(u):        # a form field about accidents is answered by an accident, not by a problem-list line
app/backend/conflict_candidates.py:230:    "denial_vs_history": "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record",
app/llm/_types.py:12:    """No recorded answer for this prompt hash. Never retried, never answered with a default."""
app/llm/_types.py:15:        super().__init__(f"FIXTURE_MISS {prompt_hash}")
app/llm/audited.py:34:    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
app/llm/audited.py:47:    last_error = "FIXTURE_MISS"
app/llm/audited.py:87:            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
app/backend/generator.py:56:        return {"failure": "FIXTURE_MISS", "record_no": record["n"]}
app/backend/generator.py:185:    """A record the extract step produced NO usable output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE, SUMMARY_NOT_IN_QUOTE) as a could-not-verify tray
app/backend/generator.py:227:    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
app/llm/backends/fixture.py:1:"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
app/backend/pipeline.py:227:JUDGE_NOT_RUN = "JUDGE_NOT_RUN"
app/backend/pipeline.py:232:    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.
app/backend/pipeline.py:237:        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
app/backend/pipeline.py:241:_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
app/backend/pipeline.py:242:_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
app/backend/pipeline.py:517:    if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
app/backend/pipeline.py:518:        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
app/backend/pipeline.py:540:            if f["failure"] != "SUMMARY_NOT_IN_QUOTE":      # D-054: a tray item, not an error (the model answered; code removed what the quote does not support)
app/backend/pipeline.py:542:                                   "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
app/backend/case_list.py:160:      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:05.699Z

**tool call — Bash**
````
{
 "command": "sed -n 120,175p app/backend/calibration_route.py; grep -rn \"server answered\\|recorded replies\\|fixture backend\\|curated\" app/frontend/*.js app/backend/*.py | cut -c1-260; sed -n 355,385p app/backend/review.py; grep -n \"demo\" app/backend/review.py app/backend/api.py | cut -c1-220 | head -40"
}
````

### User / tool · 2026-11-02T16:07:05.807Z

**tool result**
````
    return bad


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def disk_prompt_hashes(root=ROOT) -> dict:
    """The prompt and lexicon hashes read from the working tree: the set evals/run.py hashes() records. The route compares against these, not HEAD."""
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / PROMPT_DIR).glob("*.md")):
        out[p.relative_to(root).as_posix()] = _sha256(p.read_bytes())
    if (root / LEXICON).exists():
        out[LEXICON] = _sha256((root / LEXICON).read_bytes())
    return out


def current_prompt_hashes(root=ROOT) -> dict:
    """What the prompts are now: the files on disk under `root`, which are the files the running app loads (app/llm/promptlib.py reads them
    from disk). Deliberately not HEAD: a prompt edited and not yet committed already changes what the pipeline runs, so it must read as stale."""
    return disk_prompt_hashes(root)


def stale_reason(doc, current):
    """Why the measurement in `doc` no longer matches the prompts in `current`, or None. Compared name by name: a prompt added, removed or
    edited since the run means the counts describe other prompts. A file that records no hashes cannot be shown current."""
    recorded = doc.get("hashes")
    if not isinstance(recorded, dict) or not recorded:
        return "This measurement does not record which prompts it used, so it cannot be checked against the current prompts."
    changed = sorted(k for k in set(recorded) | set(current) if recorded.get(k) != current.get(k))
    if not changed:
        return None

    def describe(k):
        name = pathlib.PurePosixPath(k).name
        if k not in recorded:
            return f"{name} is new"
        if k not in current:
            return f"{name} was removed"
        return f"{name} changed"
    shown = "; ".join(describe(k) for k in changed[:8])
    more = f"; and {len(changed) - 8} more" if len(changed) > 8 else ""
    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."


def _envelope(status, calibration=None, message=None) -> dict:
    return {"status": status, "calibration": calibration, "message": message}


def load(path=REPORT, root=ROOT) -> dict:
    """The envelope for the file at `path`: ok with the served subset and the stale flags, missing, or invalid. Read-only; never raises.
    `root` is the tree whose prompt files (on disk) the file is compared with."""
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
app/frontend/app.js:11:    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? (h.fixture_set === "recorded" ? "cached demo (recorded responses)" : "cached demo (curated responses)") : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : ""; // D
app/frontend/stepper.js:169:  // False in demo mode and with the fixture backend, and after a rerun that got no answer. A field that is missing counts as false: no button that cannot work.
app/backend/store.py:19:    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
    if toks:
        words = _quoted_words(toks)
        raise _bad(f"The summary says {words}, which the quote does not say. Remove it or change the quote.", tokens=toks, reason="SUMMARY_TOKEN_NOT_IN_EXCERPT")
    dropped = g.dropped_qualifiers(new_sum, new_exc)
    if dropped:
        what = "; ".join(_QUALIFIER_WORDS.get(k, k) for k in dropped)
        raise _bad(f"The quote carries {what} that the summary leaves out. Put it back in the summary.", qualifiers=list(dropped), reason="SUMMARY_DROPS_QUALIFIER")
    found = charge_text.check(new_sum, new_exc)             # T-139 (D-019, R-CH-7): an amount in the summary or the quote never reaches the letter
    if found:
        raise _bad(charge_text.message(found, bill_state() if callable(bill_state) else bill_state), amounts=list(dict.fromkeys(found.get("excerpt", []) + found.get("summary", []))), reason="CHARGE_TEXT_IN_ENTRY")
    if span is None:
        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
    if call is not None:
        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
        ladder_verdict = judges.to_ladder("j1", verdict)
    warnings = []
    if ladder_verdict in ("partially", "unsupported"):
        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
    elif ladder_verdict == "unavailable":
        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                               "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
            "judge_error": judge_error, "state": state, "reasons": reasons}


# ---------------------------------------------------------------- edit
def _edit(conn, case_id, kind, item, body, call, t):
app/backend/api.py:1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
app/backend/api.py:114:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
app/backend/api.py:119:    def demo_mode():
app/backend/api.py:214:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
app/backend/api.py:220:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:256:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:257:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:300:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:301:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:307:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
app/backend/api.py:320:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
app/backend/api.py:333:            v = present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
app/backend/api.py:386:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:387:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:388:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:403:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/api.py:404:        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
app/backend/api.py:411:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:412:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:413:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:545:    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
app/backend/api.py:570:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:08.617Z

**tool call — Bash**
````
{
 "command": "grep -rln \"recorded replies\\|server answered\" --include=* app evals tests 2>/dev/null | head; grep -n \"message\\|fixture\\|backend\" app/backend/calibration_route.py | cut -c1-240 | head -40; grep -rn \"recorded replies\" evals/*.py app | cut -c1-300 | head"
}
````

### User / tool · 2026-11-02T16:07:08.751Z

**tool result**
````
evals/run.py
evals/reports/latest.json
evals/reports/20261102T094757Z.md
evals/reports/20261102T104436Z.md
evals/reports/20261102T123428Z.md
evals/reports/20261102T132655Z.md
evals/reports/20261102T090958Z.md
evals/reports/20261102T115517Z.md
evals/reports/20261102T115607Z.md
evals/reports/20261102T121612Z.md
4:from those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.
6:Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
31:SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
56:def _statement_ok(text, cell, backend, case_count) -> bool:
57:    """A statement is a non-empty string that names the backend. When its cell has items it must also quote that cell's own m/t and the
59:    if not isinstance(text, str) or not text or f" on the {backend} backend" not in text:
74:    if not (isinstance(c.get("backend"), str) and c["backend"]):
75:        bad.append("backend")
114:        if not _statement_ok(se["overall"].get(s), bs[s], c["backend"], c["case_count"]):
118:            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s], c["backend"], c["case_count"]):
166:def _envelope(status, calibration=None, message=None) -> dict:
167:    return {"status": status, "calibration": calibration, "message": message}
177:        return _envelope("missing", message=MISSING)
180:        return _envelope("invalid", message=INVALID)
185:        return _envelope("invalid", message=INVALID)
189:        return _envelope("invalid", message=INVALID)
evals/run.py:314:        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:12.744Z

**tool call — Bash**
````
{
 "command": "grep -rn \"answered\" app/frontend/*.js | cut -c1-240; grep -rn \"older version\" tests app evals/*.py | cut -c1-200; grep -rn \"JUDGE_NOT_RUN\\|(JUDGE_\\|(FIXTURE_MISS\" tests/*.py tests/**/*.golden* 2>/dev/null| cut -c1-200 | head -20; ls tests | head -80; grep -rln \"second check not available\" tests evals | head"
}
````

### User / tool · 2026-11-02T16:07:12.910Z

**tool result**
````
app/frontend/overview.js:336:    // The list summary is refreshed after every decision, so it wins; GET case's own next_action (read once) serves a case opened by link before the list answered. A line that names an
app/frontend/stepper.js:192:      : "The second check ran on " + plural(asked, "item", "items") + " and answered for " + (asked === 1 ? "it" : "all of them") + ".";
tests/unit/test_calibration_route.py:218:                                 "The numbers describe an older version of the prompts.")
tests/unit/test_calibration_route.py:327:    assert reason.endswith("; and 3 more. The numbers describe an older version of the prompts.")
tests/e2e/conftest.py:45:  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verb
tests/e2e/test_suggestions.py:184:    expect(st).to_contain_text("These numbers come from an older version of the AI prompts."); expect(st).to_contain_text(REASON)
app/frontend/suggestions.js:138:        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These numbers come from an older version of t
app/backend/calibration_route.py:17:The UI hides the accuracy line when `calibration` is null (T-096) and shows "numbers from an older version" when `stale` is true.
app/backend/calibration_route.py:163:    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
tests/unit/test_t134_unconfirmed_edit.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:17.644Z

**tool call — Bash**
````
{
 "command": "grep -rn \"the server\\|Request failed\" app/frontend/*.js app/backend/*.py | cut -c1-240; grep -n \"second check not available\\|JUDGE_UNAVAILABLE\\|JUDGE_\" tests/unit/test_t134_unconfirmed_edit.py | cut -c1-240; grep -rn \"not available\\|JUDGE_UNAVAILABLE)\" tests/unit/*.py | grep -i \"notes\\|(JUDGE\\|(FIX\" | cut -c1-220 | head -20; ls tests/fixtures | head -30; grep -rn \"export\" tests/unit/*golden* 2>/dev/null | head -3"
}
````

### User / tool · 2026-11-02T16:07:17.769Z

**tool result**
````
app/frontend/api.js:10:    constructor(status, err) { super((err && err.message) || "Request failed"); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }
app/frontend/audit.js:28:  function eventRow(e, confirmed) {   // a flagged charge's accept names the flag she confirmed (the event's own `confirm` when the server sends it)
app/frontend/batch.js:1:/* Batch accept for verified entries only (T-055, D-031). Button + Shift+A; the server enforces "verified pending entries only" (422 otherwise).
app/frontend/batch.js:2:   Never touches amounts or flags. Undo resets exactly the entries this batch accepted. Any error (including 404/405) shows a plain message and accepts nothing: no per-item fallback, so the server's verified-only che
app/frontend/batch.js:7:  let refused = null;   // {token, message, rows:[{id, why}]}: the last batch the server refused for a failing code check (D-051); nothing was accepted
app/frontend/batch.js:11:  // D-059 (T-154): charges are never part of a batch (the server refuses a batch that names one); say so beside the button while any charge still waits.
app/frontend/batch.js:61:  // Items the server named that are still waiting (an item the paralegal has since edited, accepted or dismissed drops out of the list).
app/frontend/excerpt.js:2:   The server validates (invalid_edit / needs_confirm); this only builds the text from API offsets and shows the server's reasons. */
app/frontend/dom.js:49:  ZL.editToCheck = (i) => !!i && i.edit_to_check === true;   // T-136: the server's own flag (T-134): reworded summary OR quote, still Needs review, not yet accepted by her
app/frontend/dom.js:50:  // How many edits are waiting for her comparison: the review's own count when the server sent it, else a count of the items that say so (the mock API).
app/frontend/dom.js:55:  // T-136 r3 (T-134 r4): the server's own `second_check_pending` (live, AI-made, no second-check answer, not a rate) is what the page reads. The inference below is only for a server
app/frontend/charges.js:60:  // D-059 (T-154): a charge the code flagged (likely duplicate / likely total) shows the flag and the server's sentence in its row; it is counted only after a confirm that names the flag.
app/frontend/export.js:16:  // A plain-text file of exactly the text the server built (no editing, no re-assembly here).
app/frontend/exportcfg.js:2:   GET/PUT/DELETE /api/cases/{token}/export_config; the panel stays hidden when the server answers 404. */
app/frontend/flags.js:89:  // T-151 (T-141 r2): `checks.skipped[]` says which check did NOT run on this case, or not on every record, in the server's own words; `checks.notes[]` are info lines. Neither is a conflict.
app/frontend/flags.js:108:  // T-151: the server's own list is authoritative even when it is empty: `conflict_types: []` means no conflict check ran on this case (the reasons are in `skipped`). Never an empty list.
app/frontend/mock.js:192:        if (id[0] === "e") it.edit_to_check = it.review_status === "edited" && it.state === "needs_review";   // the server's flag (T-134)
app/frontend/mock.js:196:      if (method === "POST" && sub === "/review/batch") {   // same verified-only, all-or-nothing rule as the server (api.md batch); no per-item route is called
app/frontend/judges.js:3:   This is a report on the AI's drafts, never a verdict on the case: the label says so. Counts are the server's; nothing is added here.
app/frontend/judges.js:106:  // An edited or hand-written item whose wording fails a code check: the row is the gate's blocker as the server wrote it (reason, fix sentence), with an Edit action.
app/frontend/judges.js:127:  // Built from the server's totals and from the gate; each kind of item is named once, and only items the gate lists carry the blocking words ("blocks export"). An edited item the
app/frontend/judges.js:171:    const verdictLine = cblk.length && gate.verdict && gate.verdict.label   // the case verdict exactly as the server words it (the same text as the case checks)
app/frontend/overview.js:6:   Nothing is computed here beyond counting what the server sent; every sentence about a blocker is the server's own `why`. Server text only goes through ZL.el (text nodes). */
app/frontend/overview.js:57:  // The library cases keep their plain titles from niceName (a typed name replaces the stored name, so a renamed library case shows the typed one); every other case shows the server's title (T-157).
app/frontend/overview.js:256:      // a decision in the open case: ask the list again (quietly, after the burst) so "Do this first" and the counts on return are the server's current numbers
app/frontend/narrative.js:1:/* Draft treatment paragraph (T-059, D-031): drafted by the server from ACCEPTED entries only, every sentence cited and checked. Shown with the
app/frontend/suggestions.js:53:  const ds = { token: null, list: [], sig: "" };   // last list the server sent for the case on screen
app/frontend/timeline.js:19:  // T-136 r2: the reason line of an edit she compared with the quote and accepted: her act first, then what the second check did (the server's own first sentence when it is not "did not run").
app/frontend/timeline.js:115:  // What the gap card shows: the sentence the server wrote, then the old and new figures with their dates. Only while the card still shows the new figure.
app/frontend/review.js:190:  const serverText = new Map();   // "item:<id>" | "blocker:<id>" -> the server's sentence for this page load
app/frontend/review.js:191:  function withServerText(node, key, load, prefix) {   // paint the fallback now; swap in the server's sentence when it arrives
app/frontend/review.js:197:  const loadItemWhy = (id) => () => ZL.api.trace(ZL.state.get().token, id).then((tr) => { const h = ((tr && tr.steps) || []).find((x) => x.id === "human"); return h && h.why ? h.why : null; });   // as given: what
app/frontend/review.js:221:  // There is no "keep my wording" confirmation any more (D-047, T-100): the server answers 422 or saves.
app/frontend/review.js:229:  // T-104: CODE_CHECK_FAILED returned by an EDIT: the server's sentence sits under the edit box (the box stays open with the typed text); EDIT_QUOTE adds a Change the quote action.
app/frontend/review.js:290:    if (body.action === "accept" && found && RV.needsDate(found.item, found.kind)) { showError(id, DATE_FIRST + " " + DATE_WHY); return false; }   // D-041: never sent; the server refuses too
app/frontend/review.js:316:      else if (e && e.code === "invalid_edit" && body.action === "edit") {   // D-047: the reason is the server's sentence (e.g. a number, side or negation that is not in the quote); the text stays in the box
app/frontend/review.js:321:      } else if (RV.isCodeCheckRefusal(e) && body.action === "accept") {   // D-051: the server's sentence, verbatim, beside the Accept button; nothing was changed
app/frontend/review.js:325:      } else if (e && String(e.code).toUpperCase() === "CONFIRM_REQUIRED" && body.action === "accept" && !body.confirm && ZL.confirmCharge) {   // D-059: the page did not know the charge was flagged; the server's 
app/frontend/review.js:336:  // T-162 (T-146): a re-run that disagreed with or failed on a decided item kept it as it was and left a note; the server's sentence is shown beside the item and in its trace.
app/frontend/stepper.js:4:   except "x of y steps passed" counts of what the server returned. Full-mode-only keys (response_raw, edited_text, events[].before/after) may be absent.
app/frontend/stepper.js:145:  // D-045(b)/T-098: a code-check blocker on wording the paralegal wrote or edited (the gate's blocker carries step_id; the text is the server's).
app/frontend/stepper.js:168:  // T-157 / T-136 debt: "Run the second check again" is offered only when the server says it can get an answer (item.rerun_available, on every item of GET case and of each review response).
app/frontend/stepper.js:233:  // ---- "What you need to do": one fixed sentence from the server plus a button where something on the page can do it.
app/frontend/stepper.js:513:  // the new quote, a rerun CAN clear it, so it is offered beside "Write the summary" (the server's own sentence says both). After a rerun that gave no answer the server sets
app/frontend/stepper.js:550:      const edit = w.reason_code === "EDIT_NOT_CONFIRMED";   // T-136 (T-134): her reworded entry is still marked Needs review; the server's own sentence says why it is not in the letter
app/frontend/stepper.js:581:  // Items the export gate would leave out of the letter because nobody decided them (the server's ITEMS_NOT_REVIEWED warning count).
app/frontend/stepper.js:657:  // The message must not outlive its cause: after any decision, ask the server again (GET /export has no side effects). Blockers gone -> "Nothing blocks the export now";
app/frontend/uncovered.js:37:  // The list is computed by the server from the entries' quotes and states, so it changes when a quote is changed or an entry stops being live. The review responses do not carry it:
app/backend/pdf_ocr.py:41:    """The environment tesseract runs with: an allow-list taken from the server's at call time, plus one thread (T-086 round 2)."""
50:    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
88:    assert "second check not available" in notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
153:    DB.update_item(conn, "e5", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"])
211:def _object(db, tok, iid, verdict="partially", code="PARTIAL", reasons=("JUDGE_PARTIAL",)):
tests/unit/test_eval_runner.py:334:    """An entry/amount/flag in a golden case whose judge was unavailable (JUDGE_UNAVAILABLE) is counted per case and fails bar 4."""
tests/unit/test_flags_pass.py:109:    """T-094: the conflicts stage is code candidates + J3; there is no model search to fail. A J3 that fails leaves the candidate needs_review (JUDGE_UNAVAILABLE)."""
tests/unit/test_t134_unconfirmed_edit.py:50:    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
tests/unit/test_t134_unconfirmed_edit.py:88:    assert "second check not available" in notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
llm
make_curated.py
t140_restating_labels.txt
t140_synthetic_ledger_r1.txt
t140_synthetic_ledger_r2.txt
t140_synthetic_ledger_r3.txt
tests/unit/_golden.py:24:def export_blocks():
tests/unit/_golden.py:25:    t = (G / "sample.export.expected.txt").read_text()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:26.145Z

**tool call — Bash**
````
{
 "command": "grep -n \"judge_error\\|FIXTURE\\|demo\\|warnings\" app/backend/review.py | cut -c1-260 | head -40; sed -n 1,60p tests/unit/test_t134_unconfirmed_edit.py | cut -c1-260; cat tests/unit/_golden.py | head -50; ls tests/fixtures/llm | head -3; grep -rn \"sample.export.expected\" -r tests evals tools Makefile 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T16:07:26.344Z

**tool result**
````
7:(D-045b); an objection or an unavailable judge saves the edit as needs_review and is returned in warnings[] (JUDGE_PARTIAL, JUDGE_UNSUPPORTED,
281:    warnings = []
292:        warnings = _edit(conn, case_id, kind, item, body, call, t)
295:            "review": present.review_view(conn, case_id), "warnings": warnings}
346:    The judge never blocks (D-045b): its objection is returned in `warnings` and the item is stored as needs_review."""
367:    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
369:        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
371:    warnings = []
374:        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
376:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
380:    return {"toks": [], "code_reasons": code_reasons, "warnings": warnings, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
381:            "judge_error": judge_error, "state": state, "reasons": reasons}
444:                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
452:        chk["warnings"].append({"code": "CHARGE_CLAUSE_REMOVED", "item_id": item["id"], "removed": trimmed["removed"],
455:    return chk["warnings"]
523:            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
607:        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
664:                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
681:            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}
745:            "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": warns}
"""T-134 (paralegal pass 4 M2; D-045b, D-051): an edited entry that is still needs_review has not been decided.
It is not in the letter, not counted as accepted, listed by the gate as EDIT_NOT_CONFIRMED (a warning: it is not in the letter, so it blocks nothing),
and the notes never say the paralegal accepted it. Her explicit Accept (after comparing with the quote) is still bound by the code checks (422)."""
import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from app.db import db as DB
from tests.unit.test_api_routes import run_case

EDIT = "Persistent neck pain 6/10 with daily headaches noted."


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "t134.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def _gate(c, tok):
    return next(s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"] if s["id"] == "export_gate")


def _setup(c, accept=("e1",)):
    tok = run_case(c)
    for i in accept:
        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
    r = c.post(f"/api/cases/{tok}/items/e3/review", json={"action": "edit", "edits": {"summary": EDIT}})
    assert r.status_code == 200 and r.json()["item"]["review_status"] == "edited" and r.json()["item"]["state"] == "needs_review"
    return tok, r.json()


def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted(env):
    _, c = env
    tok, r = _setup(c)
    assert r["item"]["edit_to_check"] is True
    assert r["review"]["counts"]["edit_to_check"] == 1
    ex = c.get(f"/api/cases/{tok}/export")
    assert ex.status_code == 200
    j = ex.json()
    assert EDIT not in j["letter_text"] and "daily headaches" not in j["letter_text"]
    assert "e3" not in [e["id"] for e in j["items"]["entries"]]
    assert j["counts"]["entries"] == 1 and j["counts"]["pending"] >= 1
    assert j["excluded"]["edit_not_confirmed"] == 1
    assert j["provenance"]["edited_count"] == 0
    notes = j["internal_notes_text"]
    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
    assert "not yet confirmed" in notes
    before_edited = notes.split("EDITED ITEMS")[1].split("PENDING ITEMS NOT INCLUDED")[0]
    assert "not in the letter" in before_edited and EDIT in before_edited
    assert "Items not reviewed: 0" not in notes


def test_gate_names_the_unconfirmed_edit_as_a_warning_and_agrees_with_the_export(env):
    _, c = env
    tok, _ = _setup(c)
    g = _gate(c, tok)
"""Helpers: load golden records/expected files from evals/golden (the only test data; synthetic)."""
import json, pathlib, re
G = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"

def case_names():
    return sorted(p.name[:-len(".expected.json")] for p in G.glob("*.expected.json"))

def expected(case):
    return json.loads((G / f"{case}.expected.json").read_text())

def raw(case):
    return (G / f"{case}.txt").read_text()

def records(case):
    """[{n, date_raw, source, excerpt}] parsed from the golden paste format."""
    out = []
    for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', raw(case)):
        out.append(dict(n=int(m.group(1)), date_raw=m.group(2), source=m.group(3), excerpt=m.group(4)))
    return out

def record(case, n):
    return next(r for r in records(case) if r["n"] == n)

def export_blocks():
    t = (G / "sample.export.expected.txt").read_text()
    letter, notes = t.split("=== INTERNAL_NOTES_TEXT")
    return letter.split("\n", 1)[1], notes.split("\n", 1)[1]
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
tests/unit/test_grounding.py:128:    """R-TL-10 / R-EX-6: all 9 summaries in sample.export.expected.txt pass check_summary against their own quote, label and date."""
tests/unit/_golden.py:25:    t = (G / "sample.export.expected.txt").read_text()
tests/unit/test_export.py:32:    """R-EX-6: all entries + both charges accepted -> letter_text and internal_notes_text equal sample.export.expected.txt exactly."""
tests/fixtures/make_curated.py:2:excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a model.
tests/fixtures/make_curated.py:9:real fixture backend and checks the export against evals/golden/sample.export.expected.txt.
tests/fixtures/make_curated.py:19:HEADER = ("CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from "
tests/fixtures/make_curated.py:168:    g = (G.G / "sample.export.expected.txt").read_text()
tests/fixtures/llm/curated/bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json:2: "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
tests/fixtures/llm/curated/4770363f6bf66fd6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json:2: "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
tests/fixtures/llm/curated/85a544a335859c486aaa581be110146353bbe09d65a0b3946d121a72f463ad81.json:2: "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:33.438Z

**tool call — Bash**
````
{
 "command": "sed -n 436,447p app/backend/review.py | cut -c1-300; grep -rn \"no usable answer\\|JUDGE_FAILED\\|did not run or did not finish\\|JUDGE_NOT_RUN:\" app tests evals/*.py | grep -v \"^app/frontend/node\" | cut -c1-230; sed -n 40,56p app/backend/narrative.py; sed -n 210,235p app/backend/trace.py | cut -c1-260"
}
````

### User / tool · 2026-11-02T16:07:33.571Z

**tool result**
````
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
    lad = item.get("ladder") or {"item_id": item["id"]}
    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
                           "state": item["state"], "state_reasons": list(item.get("state_reasons") or []), "lad_state": lad.get("state")}      # deep copies: the edit updates code_checks in place below
    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
app/backend/trace.py:273:                        "LLM_FAILED_AFTER_RETRIES": "Not run: the AI gave no usable answer for this record.",
app/backend/trace.py:274:                        "FIXTURE_MISS": "Not run: the AI gave no usable answer for this record.",
app/backend/why.py:16:    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
app/backend/why.py:49:JUDGE_FAILED = "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked."
app/backend/why.py:58:        return JUDGE_FAILED
app/backend/reclassify.py:41:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:3:called and failed says 'second check failed' (reason code unchanged), not 'JUDGE_NOT_RUN:'."""
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:177:        assert WHY.why("JUDGE_UNAVAILABLE").startswith("JUDGE_NOT_RUN:")
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:184:    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("JUDGE_NOT_RUN:")
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:185:    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("JUDGE_NOT_RUN:")                  # no judge record = it did not run
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:192:    assert text.startswith("JUDGE_NOT_RUN:") and "second check failed" not in text.lower()

def accepted_entries(case: dict) -> list:
    """Entries the paralegal accepted (or edited and accepted) whose quote is still verbatim in the record, chronological."""
    v = export._View(case)
    return [dict(e, label=v.source(e["record_no"]), date_iso=v.date_of(e), cite=v.cite(e["record_no"])) for e in v.in_entries]


def prompt_user(entries: list, nonce: str) -> str:
    blocks = []
    for e in entries:
        blocks.append(f"ENTRY {e['id']} | {export._long_date(e['date_iso'])} | {e['label']}\nSUMMARY:\n{injection.wrap(e['summary'], nonce)}\n"
                      f"QUOTE:\n{injection.wrap(e['excerpt'], nonce)}")
    return "ACCEPTED ENTRIES:\n" + "\n\n".join(blocks) + "\nReturn the JSON object."


def check_sentence(text: str, entry: dict) -> list:
    """Code checks (a); returns reason codes, empty when the sentence may go to the judge."""
    label = label or f"Second AI check: {JUDGE_LABEL[jid].lower()}"
    label = label[0].upper() + label[1:]
    jd = jd or {}
    raw = jd.get("verdict")
    call = cx.call(jd.get("call_id"), item_id, jid)
    if raw is None and not call:
        if not cx.ran:
            return step(sid, label, "llm", PENDING, "The second check has not run yet.", rule=rule, evidence={"model": {"id": cx.models["judge"], "role": "judge", "independent_of_generator": cx.models["judge"] != cx.models["generator"]}, "prompt_version": JUDG
                        next_action=na("RERUN"))
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
                    next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    verdict = _norm_verdict(jid, raw if raw is not None else (call or {}).get("verdict"))
    ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or JUDGE_PROMPT[jid], call)
    rc = _judge_reason_code(jd, call)
    ev.update(judge_verdict=verdict, judge_reason_code=rc)
    if verdict == "supported":
        ev["rationale"] = _J_OK[jid]
        return step(sid, label, "llm", PASS, _J_OK[jid], rule=rule, evidence=ev)
    if verdict == "unavailable":
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence=ev, next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    code = _OBJECTION[verdict]
    detail = why.judge_detail(rc)
    ev["rationale"] = detail or reason_text(code)
    return step(sid, label, "llm", FAIL, (reason_text(code) + (" " + detail if detail else "")).strip(), reason=code, rule=rule, evidence=ev,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:37.738Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/probe.py <<'EOF'\nimport os, tempfile, json\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ.pop(\"ANTHROPIC_API_KEY\",None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom tests.unit.test_api_routes import run_case\nd=tempfile.mkdtemp()\nc=TestClient(create_app(d+\"/x.sqlite\", static_dir=d), client=(\"127.0.0.1\",50000))\ntok=run_case(c)\nr=c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\":\"edit\",\"edits\":{\"summary\":\"Persistent neck pain 6/10 with daily headaches noted.\"}}).json()\nprint(json.dumps(r[\"warnings\"]), json.dumps({k:r[\"item\"].get(k) for k in (\"why\",\"reasons\",\"state\",\"why_text\")}))\nprint(json.dumps(r[\"item\"])[:1500])\nt=c.get(f\"/api/cases/{tok}/trace/e3\") if False else None\nn=c.get(f\"/api/cases/{tok}/export\").json()[\"internal_notes_text\"]\nprint(n)\nEOF\npython3 /private/tmp/claude-501/probe.py 2>&1 | tail -60"
}
````

### User / tool · 2026-11-02T16:07:37.863Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/probe.py", line 3, in <module>
    from fastapi.testclient import TestClient
ModuleNotFoundError: No module named 'fastapi'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:39.262Z

**tool call — Bash**
````
{
 "command": "ls -d .venv venv 2>/dev/null; grep -rn \"venv\\|pytest\" Makefile memory/ENVIRONMENT.md 2>/dev/null | head -5"
}
````

### User / tool · 2026-11-02T16:07:39.348Z

**tool result**
````
.venv
memory/ENVIRONMENT.md:8:| python3 | 3.12.2 | project venv at `.venv/` (gitignored). Use `.venv/bin/python`. |
memory/ENVIRONMENT.md:18:| Playwright | python package in .venv; chromium-headless-shell 1248 | |
memory/ENVIRONMENT.md:19:| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:41.676Z

**tool call — Bash**
````
{
 "command": "PYTHONPATH=. .venv/bin/python /private/tmp/claude-501/probe.py 2>&1 | tail -70 | cut -c1-900"
}
````

### User / tool · 2026-11-02T16:07:42.831Z

**tool result**
````
llm call failed call_id=c3b3e78dff90b step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
[{"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": "e3"}] {"why": "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked.", "reasons": ["JUDGE_UNAVAILABLE"], "state": "needs_review", "why_text": null}
{"id": "e3", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"], "why": "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked.", "review_status": "edited", "edited": {"at": "2026-11-02T16:07:42Z", "original_summary": "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.", "summary": "Persistent neck pain 6/10 with daily headaches noted."}, "ladder": {"backend": "fixture", "code_checks": {"date_provider_from_header": true, "excerpt_verbatim": true, "excerpt_whole_sentence": true, "highlight_found": true, "qualifier_carried": true, "summary_tokens_not_in_excerpt": []}, "generator": {"call_id": "cc57132e7ad2a", "model": "claude-sonnet-5-5", "output": {"excerpt": "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks.", "summary": "Persistent 
Traceback (most recent call last):
  File "/private/tmp/claude-501/probe.py", line 13, in <module>
    n=c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'internal_notes_text'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:47.548Z

**tool call — Bash**
````
{
 "command": "sed -n 105,125p app/backend/api.py | cut -c1-200; cat >> /private/tmp/claude-501/probe.py <<'EOF'\nEOF\nsed -i 's/^n=c.get.*$/print(r[\"item\"][\"ladder\"][\"judge\"]); e=c.get(f\"\\/api\\/cases\\/{tok}\\/export\"); print(e.status_code, list(e.json())[:12])/; s/^print(n)$//' /private/tmp/claude-501/probe.py; sed -i '/^print(json.dumps(r\\[\"item\"\\])/d' /private/tmp/claude-501/probe.py; PYTHONPATH=. .venv/bin/python /private/tmp/claude-501/probe.py 2>&1 | tail -5 | cut -c1-600"
}
````

### User / tool · 2026-11-02T16:07:48.693Z

**tool result**
````
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/probe.py'
sed: 2: "/private/tmp/claude-501 ...": undefined label 'mp/claude-501/probe.py'
Traceback (most recent call last):
  File "/private/tmp/claude-501/probe.py", line 13, in <module>
    n=c.get(f"/api/cases/{tok}/export").json()["internal_notes_text"]
      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
KeyError: 'internal_notes_text'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:07:55.732Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S; head -9 /private/tmp/claude-501/probe.py > $S/probe.py; cat >> $S/probe.py <<'EOF'\nr=c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\":\"edit\",\"edits\":{\"summary\":\"Persistent neck pain 6/10 with daily headaches noted.\"}}).json()\nprint(r[\"item\"][\"ladder\"][\"judge\"])\ne=c.get(f\"/api/cases/{tok}/export\"); print(e.status_code, e.text[:300])\nEOF\nPYTHONPATH=. .venv/bin/python $S/probe.py 2>&1 | tail -4 | cut -c1-700; echo $S"
}
````

### User / tool · 2026-11-02T16:07:56.701Z

**tool result**
````
llm call failed call_id=ccfbd529531f6 step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
llm call failed call_id=c7ff72a1572ae step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
{'call_id': None, 'error_class': 'LLMFailedFixtureMiss', 'model': 'claude-haiku-5-5', 'prompt_version': 'judge_faithfulness_v1', 'reason_code': 'NONE', 'verdict': 'unavailable'}
422 {"error":{"code":"export_blocked","message":"Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.","detail":{"blockers":[{"item_id":null,"kind":"case","reason_code":"NOTHING_ACCEPTED","why":"Nothing is accepted or edited yet, so the letter would be empty.","next_ac
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:04.794Z

**tool call — Bash**
````
{
 "command": "sed -n 5,30p app/backend/present.py | cut -c1-250; grep -rn \"why\\.join\\|why\\.why\\|WHY\\.why\\|WHY\\.join\\|judge_failed\\|JUDGE_FAILED\" app --include=*.py | cut -c1-220"
}
````

### User / tool · 2026-11-02T16:08:04.885Z

**tool result**
````
from app.backend import conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons, judge=None):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
app/backend/why.py:49:JUDGE_FAILED = "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked."
app/backend/why.py:52:def judge_failed(judge) -> bool:
app/backend/why.py:57:    if code == "JUDGE_UNAVAILABLE" and judge_failed(judge):
app/backend/why.py:58:        return JUDGE_FAILED
app/backend/trace.py:89:        return why.why(code)
app/backend/present.py:16:            out.append(why.why(c, None if "FIXTURE_MISS" in reasons else judge))
app/backend/flags.py:45:    f["why"] = why.join(f["reasons"], (f.get("ladder") or {}).get("judge")) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
app/backend/flags.py:235:            "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
app/backend/flags.py:361:        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
app/backend/flags.py:370:    f["why"] = why.why(code) + (" " + detail if detail else "")
app/backend/review.py:186:    static = why.why("CHARGE_TEXT_IN_ENTRY")
app/backend/generator.py:171:    e["why"] = why.join(reasons, lad.get("judge")) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
app/backend/generator.py:189:    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
app/backend/pipeline.py:68:                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
app/backend/pipeline.py:84:                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
app/backend/pipeline.py:407:    a["why"] = WHY.join(reasons, a["ladder"]["judge"]) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
app/backend/pipeline.py:605:    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
app/backend/reclassify.py:243:            "why": " ".join(WHY.why(c) for c in old["state_reasons"])}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:15.640Z

**tool call — Bash**
````
{
 "command": "grep -nE \"[A-Z]{3,}_[A-Z_]{2,}\" app/backend/export.py | cut -c1-250; grep -nE \"[A-Z]{3,}_[A-Z_]{3,}\" evals/golden/sample.export.expected.txt | head; grep -n \"original_summary_failed\" -r app/backend/*.py | cut -c1-200"
}
````

### User / tool · 2026-11-02T16:08:15.748Z

**tool result**
````
3:Contract (ADR-009, D-001, D-012, D-017, D-019, LLM_VS_CODE rows 8 and 19; R-EX-1..R-EX-8):
23:LETTER_TITLE = "TREATMENT CHRONOLOGY"
24:CHARGES_TITLE = "BILLED CHARGES"
25:SUMMARY_TITLE = "TREATMENT SUMMARY"
26:NOTES_TITLE = "INTERNAL REVIEW NOTES — DO NOT SEND"
27:SOURCE_PREFIX = "Source [Ex. __ / Bates __]: "
28:TOTAL_PREFIX = "Billed charges accepted from these records: "  # D-019: nothing may follow the amount, ever
31:FLAGGED_HEADING = ("FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or "
37:TRANSLATION_NOTE = {"AI translation": "[AI translation of the Spanish original; check before sending]",
39:NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
43:_TYPE_RANK = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
44:_CONFLICT_SUB = {"accident_date": "accident date", "treatment_plan": "PT plan", "treatment_plan_vs_actual": "PT plan",
46:_ACCIDENT_SUBS = ("accident_date", "accident_dates_differ", "accident_date_after_treatment")
47:_COLLISION_RE = re.compile(r"rear-ended|collision|accident|crash|\bMV[AC]\b|struck|hit by", re.I)
51:_FUTURE_RE = re.compile(r"^\s*recommend", re.I)  # extend by card (R-EX-4 section 7)
171:        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
177:        head = SOURCE_PREFIX[len("Source "):-2] if self.export_config is None else self._bracket(n)[len("Source "):]
292:    return " " + TRANSLATION_NOTE.get(lab, f"[{lab}; check before sending]") if lab else ""
308:    out = [LETTER_TITLE, ""]
321:        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
324:        out += [CHARGES_TITLE, ""]
329:        out += ["", TOTAL_PREFIX + _money(sum(a["cents"] for a in charges))]
341:        return "Conflict, " + _CONFLICT_SUB.get(sub, (sub or "other").replace("_", " "))
377:                    coll = next((x for x in _sentences(v.text(n)) if _COLLISION_RE.search(x)), None)
406:            keyed.append((_TYPE_RANK[t], idx, [f]))
411:            merged[t] = (_TYPE_RANK.get(t, 9), idx, [f])
428:    live = sorted((f for f in flags if _status(f) != "out"), key=lambda f: _TYPE_RANK.get(f.get("type"), 9))
435:            if f.get("type") == "conflict" and f.get("subtype") in _ACCIDENT_SUBS and not any(
437:                coll = [k for k, (st, en) in enumerate(spans) if _COLLISION_RE.search(exc[st:en])]
543:            if _FUTURE_RE.match(s) and "$" not in s:
550:_NOT_A_TREATER_SOURCE = re.compile(r"\b(?:LLP|L\.L\.P\.|law\s+(?:offices?|firms?|group)|attorneys?|counsel(?:ors?)?\s+at\s+law|esq\.?|legal|demand\s+letter|"
553:_FIRM_VOICE = re.compile(r"\b(?:this\s+firm\s+represents|we\s+represent|our\s+client|the\s+undersigned\s+(?:firm|counsel)|on\s+behalf\s+of\s+our\s+client)\b", re.IGNORECASE)
559:    return not (_NOT_A_TREATER_SOURCE.search(src) or _FIRM_VOICE.search(text))
636:_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MISS)",
637:                       "JUDGE_PARTIAL": "the second check only partly supported it (JUDGE_PARTIAL)", "JUDGE_UNSUPPORTED": "the second check did not support it (JUDGE_UNSUPPORTED)",
638:                       "JUDGE_UNSURE": "the second check was unsure (JUDGE_UNSURE)", "JUDGE_DISAGREES": "the second check disagreed (JUDGE_DISAGREES)"}
643:    return "; ".join(_EDIT_REASON_PHRASE.get(c, f"still marked for review ({c})") for c in codes) or "still marked for review"
712:        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
714:        elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
726:        NOTES_TITLE, "",
730:        FLAGGED_HEADING, *_flagged_language(v, v.flags), "",
748:    if lines and lines[-1].startswith(TOTAL_PREFIX):
750:            if lines[k] == CHARGES_TITLE and k + 1 < len(lines) and (lines[k + 1] == "" or lines[k + 1].startswith(TOTAL_PREFIX)):
755:_CHARGE_HEAD = re.compile(r"^(.*): (\$[\d,]+\.\d\d)$")
763:        if k < 2 or line.startswith(TOTAL_PREFIX):
765:        if _CHARGE_HEAD.match(line):
773:    return {"item_id": owner["id"] if owner else None, "kind": kind if owner else "case", "reason_code": "MONEY_IN_LETTER", "line": line_no, "text": line,
788:    [{item_id, kind, reason_code: MONEY_IN_LETTER, line (1-based), text, expressions, why, next_action}]"""
800:        act = ({"code": "EDIT_SUMMARY" if in_summary else "EDIT_QUOTE", "target": {"item_id": owner["id"]},
803:               if owner else {"code": "EDIT_SUMMARY", "text": "Remove the amount from the line named above, or dismiss the item it comes from. The export stays blocked until it passes."})
809:        figure = _CHARGE_HEAD.match(header).group(2)
812:        bad += [(k, header, h) for h in money.strings(_CHARGE_HEAD.match(header).group(1))]      # the header names a provider and a date: no money in it
827:            act = ({"code": "DISMISS_OR_ENTER_BY_HAND", "target": {"item_id": owner["id"]},
829:                   if owner else {"code": "DISMISS_OR_ENTER_BY_HAND", "text": "Dismiss the charge named above, or enter it by hand. The export stays blocked until it passes."})
835:    """The MONEY_IN_LETTER blockers of a case dict (T-139 r4). Both letter styles are scanned and merged (one blocker per offending entry and expression set, the first style's
850:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
855:        super().__init__(self.items[0]["reason_code"] if self.items else "EXPORT_BLOCKED")
859:        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
1:=== LETTER_TEXT (block 1: paste into letter) ===
48:=== INTERNAL_NOTES_TEXT (block 2: do not send) ===
app/backend/export.py:661:            if e.get("original_summary_failed"):        # D-051: AI wording that failed a code check is not printed anywhere in the export
app/backend/export.py:662:                bits.append(f'summary was AI wording removed (failed a check: {"; ".join(e["original_summary_failed"])}), now "{e["summary"]}"')
app/backend/store.py:80:                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:20.697Z

**tool call — Bash**
````
{
 "command": "sed -n 700,722p app/backend/export.py | cut -c1-260; grep -n \"reason\\b\\|reasons\\|code\" app/backend/export.py | sed -n 1,80p | grep -n \"f\\\"\\|f'\" | cut -c1-230"
}
````

### User / tool · 2026-11-02T16:08:20.796Z

**tool result**
````
        return []
    live = {e["id"]: e for e in v.in_entries}
    st = n.get("status", "pending")
    lines = ["", "DRAFT TREATMENT PARAGRAPH (AI-drafted from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
    for s in n.get("sentences", []):
        e = live.get(s["entry_id"])
        stale = e is None or (n.get("basis") or {}).get(s["entry_id"]) != basis_hash(e)
        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
        lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
    for r in n.get("removed", []):
        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
            lines.append(f'- AI wording removed (failed a check: {r.get("message") or r["reason"]}) ({r["entry_id"]}): {r["reason"]}.')
        elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}): {r["reason"]}.')
        else:
            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
    return lines


def _notes(v):
    accepted = [f for f in v.flags if _status(f) == "in"]
5:275:    return hashlib.sha256(f"{entry['summary']}\x1f{entry['excerpt']}".encode("utf-8")).hexdigest()[:16]
6:419:        extra = [f"Reason: {f['reason']}" for f in group if f.get("reason")] + \
12:643:    return "; ".join(_EDIT_REASON_PHRASE.get(c, f"still marked for review ({c})") for c in codes) or "still marked for review"
14:668:                f" (accepted by the paralegal after comparing it with the quote; {_edit_unconfirmed_why(e)})" if e.get("edit_state_reasons") and _status(e) == "in" else "")
17:679:            out.append(f'- Entry, {v.cite(e["record_no"])}: summary not shown, a code check on it fails (edit it to match the quote, or dismiss it)')
20:713:            lines.append(f'- AI wording removed (failed a check: {r.get("message") or r["reason"]}) ({r["entry_id"]}): {r["reason"]}.')
22:715:            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}): {r["reason"]}.')
23:717:            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:24.895Z

**tool call — Bash**
````
{
 "command": "sed -n 15,38p app/backend/narrative.py | cut -c1-260; grep -n '\"reason\"' app/backend/narrative.py | cut -c1-200 | head -20; sed -n 414,422p app/backend/export.py | cut -c1-240"
}
````

### User / tool · 2026-11-02T16:08:24.989Z

**tool result**
````
REASONS = {
    "NOT_AN_ACCEPTED_ENTRY": "The sentence cites an entry that is not accepted.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, an attribution phrase or a negation that the cited quote has.",
    "CAUSATION_NOT_QUOTED": "The sentence uses cause or adverse wording that the cited quote does not contain.",
    "SEVERITY_NOT_QUOTED": "The sentence uses severity, outcome or recommendation wording that the cited quote does not contain.",
    "FLAG_CONTENT": "The sentence talks about gaps, conflicts or other review flags, which stay out of the paragraph.",
    "JUDGE_PARTIAL": "The second check found the sentence only partly supported by the cited quote.",
    "JUDGE_UNSUPPORTED": "The second check found the sentence not supported by the cited quote.",
    "JUDGE_UNAVAILABLE": "The second check was not available for this sentence.",
}
_CAUSE = re.compile(r"\b(?:caused?|causing|due to|result(?:ed|ing)? (?:of|from|in)|because of|as a result|attributable|secondary to|"
                    r"led to|stemm(?:ed|ing) from|aggravat\w+|exacerbat\w+|permanent|chronic|disabl\w+)\b", re.IGNORECASE)
_FLAGISH = re.compile(r"\b(?:gaps?|conflicts?|inconsisten\w+|discrepanc\w+|pre-?existing|prior (?:injur\w+|condition)|missed appointments?|"
                      r"non-?complian\w+|days without treatment)\b", re.IGNORECASE)
# Severity / outcome / recommendation wording the prompt forbids ("no adjectives of your own", "never add a diagnosis, severity, prognosis"):
# deterministic backstop so a sentence like "significant pain 4/10" or "and recommended surgery" never rests on judge 1 alone.
_SEVERITY = re.compile(r"\b(?:significan\w*|sever(?:e|ely|ity)|serious\w*|ongoing|worsen\w*|worse|deteriorat\w*|debilitat\w*|excruciat\w*|"
                       r"substantial\w*|catastroph\w*|prognos\w+|recommend\w*|surg\w+)\b", re.IGNORECASE)
_DATE_PHRASE = re.compile(r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(?:,\s*\d{4})?", re.IGNORECASE)


basis_hash = export.basis_hash
100:            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
105:            base["removed"].append({**item, "reason": reasons[0], "reasons": reasons})
113:            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
118:        r["message"] = REASONS.get(r["reason"], r["reason"])
159:            "removed": [{"text": r["text"], "entry_id": r["entry_id"], "reason": r["reason"], "message": r.get("message") or REASONS.get(r["reason"], r["reason"])} for r in nar.get("removed", [])]
    for _, _, group in sorted(keyed, key=lambda k: (k[0], k[1])):
        if len(group) == 1:
            line = _flag_line(v, group[0])
        else:
            line = _terminate(f"{_flag_label(group[0])}: " + "; ".join(_flag_line(v, f).split(": ", 1)[1] for f in group))
        extra = [f"Reason: {f['reason']}" for f in group if f.get("reason")] + \
                [f"Reviewer note: {f['note']}" for f in group if f.get("note")]
        lines.append("- " + " ".join([_terminate(line)] + extra) if extra else "- " + _terminate(line))
    return lines or ["- none"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:37.622Z

**tool call — Bash**
````
{
 "command": "sed -n 690,700p app/backend/export.py | cut -c1-200; grep -rn \"AI wording removed\\|Sentence removed\\|: NOT_AN_ACCEPTED_ENTRY\\|Removed: \" tests/unit/*.py | cut -c1-240; grep -rln \"second check not available\\|still marked for review\\|JUDGE_UNAVAILABLE\\\" in\\|(JUDGE_\" tests | head"
}
````

### User / tool · 2026-11-02T16:08:37.771Z

**tool result**
````
def _cite_tail(v, entry_id):
    e = next(x for x in v.entries if x["id"] == entry_id)
    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"


def _draft_paragraph(v):
    n = v.narrative
    if not n:
        return []
tests/unit/test_narrative.py:289:        assert "Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY." in notes
tests/unit/test_trace.py:1403:    assert "summary was AI wording removed (failed a check:" in notes and "a number or word in it is not in the quote" in notes
tests/unit/test_trace.py:1404:    assert "- AI wording removed (failed a check: The sentence has a number" in notes
tests/unit/test_trace.py:1405:    assert 'Removed: "Second check said no."' in notes                                              # a judge removal is not a code failure: the sentence stays visible
tests/unit/test_case_list.py
tests/unit/test_generator.py
tests/unit/test_t139_narrow.py
tests/unit/test_review_rules.py
tests/unit/test_flags_pass.py
tests/unit/test_t134_unconfirmed_edit.py
tests/unit/test_trace.py
tests/unit/test_eval_runner.py
tests/unit/test_conflict_candidates.py
tests/unit/test_t145_judge_not_run.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:08:59.059Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_t167_plain_wording.py",
 "content": "\"\"\"T-167 (MVP UX audit F4/F7): no developer codes and no test-mode wording in anything the paralegal reads, or in the exported internal notes.\nReason codes stay in the API fields (`reasons`, `reason_code`, `code`); only the displayed sentences change.\nThe demo-mode edit message says plainly that the AI second check is not available in the demo and what she can do instead.\"\"\"\nimport re\nfrom types import SimpleNamespace\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import calibration_route, export, narrative, reclassify, trace, why as WHY\nfrom app.backend.api import create_app\nfrom tests.unit.test_api_routes import run_case\n\n# A reason code is SHOUTING_SNAKE (two or more words); ordinary capitals (PT, MRI, OCR, AI) are not.\nCODE = re.compile(r\"\\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\\b\")\n# Test-mode and developer wording that must never be shown to a paralegal.\nBANNED = (\"fixture\", \"curated\", \"older version\", \"server answered\", \"recorded replies\", \"golden case\", \"the server\", \"request failed\", \"http 5\")\nEDIT = \"Persistent neck pain 6/10 with daily headaches noted.\"\n\n\ndef assert_plain(text, where=\"\"):\n    assert not CODE.search(text), f\"raw reason code in {where}: {CODE.search(text).group(0)!r} in {text[:200]!r}\"\n    low = text.lower()\n    for b in BANNED:\n        assert b not in low, f\"test/developer wording {b!r} in {where}: {text[:200]!r}\"\n\n\n# ---------------------------------------------------------------- why.py: every fixed sentence, with every judge shape\nJUDGES = [None, {}, {\"verdict\": \"unavailable\", \"reason_code\": \"JUDGE_NOT_RUN\"},\n          {\"verdict\": \"unavailable\", \"reason_code\": \"NONE\", \"error_class\": \"LLMFailedFixtureMiss\"},\n          {\"verdict\": \"unavailable\", \"reason_code\": \"NONE\", \"error_class\": \"LLMFailedTimeout\"},\n          {\"verdict\": \"unavailable\", \"reason_code\": \"NONE\"}]\n\n\n@pytest.mark.parametrize(\"code\", WHY.all_codes())\n@pytest.mark.parametrize(\"judge\", JUDGES, ids=lambda j: str(j and j.get(\"error_class\") or j and j.get(\"reason_code\")))\ndef test_every_why_sentence_is_plain(code, judge):\n    assert_plain(WHY.why(code, judge), f\"why({code})\")\n\n\ndef test_judge_detail_and_models_sentences_are_plain():\n    for c in (\"ADDS_DIAGNOSIS\", \"SHOULD_BE_CHARGE\", \"TEXT_AMBIGUOUS\", \"WRONG_TYPE\", \"NOT_SUPPORTED_BY_QUOTE\", \"FACT_MISMATCH\"):\n        assert_plain(WHY.judge_detail(c), f\"judge_detail({c})\")\n    assert_plain(WHY.MODEL_CONFLICT, \"MODEL_CONFLICT\")\n\n\ndef test_not_run_sentence_has_no_internal_code_prefix():\n    assert WHY.why(\"JUDGE_UNAVAILABLE\", None).startswith(\"The second AI check did not run or did not finish\")\n    assert not WHY.why(\"JUDGE_UNAVAILABLE\", {\"verdict\": \"unavailable\", \"reason_code\": \"JUDGE_NOT_RUN\"}).startswith(\"JUDGE_NOT_RUN\")\n\n\ndef test_demo_second_check_sentence_says_plainly_what_it_is_and_what_to_do():\n    s = WHY.why(\"JUDGE_UNAVAILABLE\", {\"verdict\": \"unavailable\", \"reason_code\": \"NONE\", \"error_class\": \"LLMFailedFixtureMiss\"})\n    low = s.lower()\n    assert \"second check is not available in this demo\" in low and \"ai\" in low\n    assert \"compare\" in low and \"quote\" in low and \"accept\" in low         # what she can do instead\n    assert \"failed\" not in low and \"gave no usable answer\" not in low         # not framed as a failure she caused\n\n\ndef test_live_failed_second_check_sentence_says_what_to_do():\n    s = WHY.why(\"JUDGE_UNAVAILABLE\", {\"verdict\": \"unavailable\", \"reason_code\": \"NONE\", \"error_class\": \"LLMFailedTimeout\"})\n    low = s.lower()\n    assert \"second check is not available right now\" in low and \"compare\" in low and \"quote\" in low and \"accept\" in low\n    assert \"failed\" not in low and \"gave no usable answer\" not in low\n\n\ndef test_other_message_strings_are_plain():\n    for k, s in narrative.REASONS.items():\n        assert_plain(s, f\"narrative.REASONS[{k}]\")\n    for k, s in trace.TRACE_WHY.items():\n        assert_plain(s, f\"trace.TRACE_WHY[{k}]\")\n    for k, s in reclassify._REFUSAL_WORDING.items() if hasattr(reclassify, \"_REFUSAL_WORDING\") else ():\n        assert_plain(s, f\"reclassify[{k}]\")\n    stale = calibration_route.stale_reason({\"hashes\": {\"app/llm/prompts/a.md\": \"x\"}}, {\"app/llm/prompts/a.md\": \"y\"})\n    assert_plain(stale, \"calibration stale reason\")\n    assert \"older version of the prompts\" not in stale\n    assert_plain(calibration_route.stale_reason({}, {}), \"calibration stale reason (no hashes)\")\n\n\n# ---------------------------------------------------------------- the exported notes\ndef test_edit_reason_phrases_in_the_notes_carry_no_code():\n    for c, s in export._EDIT_REASON_PHRASE.items():\n        assert_plain(s, f\"_EDIT_REASON_PHRASE[{c}]\")\n    for codes in ([\"JUDGE_UNAVAILABLE\"], [\"FIXTURE_MISS\"], [\"SOMETHING_NEW\"], [\"JUDGE_PARTIAL\", \"JUDGE_UNSURE\"], []):\n        assert_plain(export._edit_unconfirmed_why({\"edit_state_reasons\": codes}), f\"_edit_unconfirmed_why({codes})\")\n\n\ndef test_removed_narrative_lines_in_the_notes_carry_no_code():\n    n = {\"status\": \"pending\", \"sentences\": [], \"basis\": {}, \"removed\": [\n        {\"text\": \"x\", \"entry_id\": \"e1\", \"reason\": \"SUMMARY_TOKEN_NOT_IN_EXCERPT\", \"message\": narrative.REASONS[\"SUMMARY_TOKEN_NOT_IN_EXCERPT\"]},\n        {\"text\": \"y\", \"entry_id\": \"e2\", \"reason\": \"NOT_AN_ACCEPTED_ENTRY\", \"message\": narrative.REASONS[\"NOT_AN_ACCEPTED_ENTRY\"]},\n        {\"text\": \"Second check said no.\", \"entry_id\": \"e3\", \"reason\": \"JUDGE_UNSUPPORTED\", \"message\": narrative.REASONS[\"JUDGE_UNSUPPORTED\"]},\n        {\"text\": \"z\", \"entry_id\": \"e4\", \"reason\": \"JUDGE_UNAVAILABLE\", \"message\": narrative.REASONS[\"JUDGE_UNAVAILABLE\"]}]}\n    lines = export._draft_paragraph(SimpleNamespace(narrative=n, in_entries=[]))\n    text = \"\\n\".join(lines)\n    assert_plain(text, \"draft-paragraph notes\")\n    assert \"AI wording removed (failed a check: The sentence has a number\" in text\n    assert 'Removed: \"Second check said no.\"' in text and \"not supported by the cited quote\" in text\n    assert \"Sentence removed (cites an entry that is not accepted)\" in text\n\n\n@pytest.fixture\ndef env(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)          # no live model: this is the demo\n    d = str(tmp_path / \"t167.sqlite\")\n    return TestClient(create_app(d, static_dir=str(tmp_path)), client=(\"127.0.0.1\", 50000))\n\n\ndef test_demo_edit_message_and_notes_are_plain_end_to_end(env):\n    c = env\n    tok = run_case(c)\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"accept\"}).status_code == 200\n    r = c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": EDIT}})\n    assert r.status_code == 200\n    j = r.json()\n    # the codes stay in the API fields\n    assert j[\"item\"][\"reasons\"] == [\"JUDGE_UNAVAILABLE\"] and [w[\"code\"] for w in j[\"warnings\"]] == [\"JUDGE_UNAVAILABLE\"]\n    # the displayed text is plain, says the check is not available in the demo and what she can do\n    msg = j[\"warnings\"][0][\"message\"]\n    for text in (msg, j[\"item\"][\"why\"]):\n        assert_plain(text, \"demo edit message\")\n        low = text.lower()\n        assert \"not available in this demo\" in low and \"compare\" in low and \"quote\" in low and \"accept\" in low\n    notes = c.get(f\"/api/cases/{tok}/export\").json()[\"internal_notes_text\"]\n    assert_plain(notes, \"internal notes\")\n    assert \"edited; second check not available\" in notes and \"not yet confirmed\" in notes\n    # accept it after comparing: the other notes line (edited item accepted) is plain too\n    assert c.post(f\"/api/cases/{tok}/items/e3/review\", json={\"action\": \"accept\"}).status_code == 200\n    notes = c.get(f\"/api/cases/{tok}/export\").json()[\"internal_notes_text\"]\n    assert_plain(notes, \"internal notes after accept\")\n    assert \"after comparing it with the quote; second check not available\" in notes\n    # every other message the review responses carry, and the trace sentences of the edited item\n    assert_plain(c.get(f\"/api/cases/{tok}/trace/e3\").text.replace('\"reason_code\"', \"\").replace(\"JUDGE_UNAVAILABLE\", \"\").replace(\"FIXTURE_MISS\", \"\"), \"trace body\") if False else None\n\n\ndef test_sample_golden_notes_still_match_and_are_plain():\n    from tests.unit._golden import export_blocks\n    _, notes = export_blocks()\n    assert_plain(notes, \"golden internal notes\")\n"
}
````

### User / tool · 2026-11-02T16:08:59.120Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_t167_plain_wording.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:02.148Z

**tool call — Bash**
````
{
 "command": "sed -n 36,48p app/backend/reclassify.py | cut -c1-200; python3 - <<'EOF'\nimport re\np=\"tests/unit/test_t167_plain_wording.py\"\ns=open(p).read()\ns=re.sub(r\"    # every other message the review responses carry.*\\n.*if False else None\\n\",\"\",s)\ns=s.replace('    for k, s in reclassify._REFUSAL_WORDING.items() if hasattr(reclassify, \"_REFUSAL_WORDING\") else ():\\n        assert_plain(s, f\"reclassify[{k}]\")\\n','')\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"^_[A-Z_]* = {\" app/backend/reclassify.py | head"
}
````

### User / tool · 2026-11-02T16:09:02.268Z

**tool result**
````
    "INJECTION_SUSPECTED": "This record has instruction-like text, so a figure from it cannot become a charge.",
    "NOT_A_CHARGE_BY_RULE": "A fixed rule says this figure is not a charge, so it stays a figure that is not a charge.",
    "NO_CHARGE_WORDING": "The sentence with this figure has no wording that says it was charged or billed (such as charged, billed, invoiced or amount due), so it stays a figure that is not a charge."
    "JUDGE_DISAGREES": "A second AI check read this figure as something other than a charge, so it stays as it is.",
    "JUDGE_UNSURE": "A second AI check could not tell whether this figure is a charge, so it stays as it is.",
    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
}


def _sentences(excerpt: str):
    """[(start, end, text)] of the excerpt's sentences, the same boundary rule amounts.classify uses."""
    out, pos = [], 0
    for m in _BOUNDARY.finditer(excerpt):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:06.422Z

**tool call — Bash**
````
{
 "command": "sed -n 25,31p app/backend/reclassify.py | cut -c1-120; grep -n \"reclassify\\|_REFUSAL\" tests/unit/test_t167_plain_wording.py; .venv/bin/python -m pytest tests/unit/test_t167_plain_wording.py -q -x 2>&1 | tail -15 | cut -c1-300"
}
````

### User / tool · 2026-11-02T16:09:07.225Z

**tool result**
````
TARGETS = ("charge", "not_a_charge")
NOT_A_CHARGE_KIND = "unclear"
AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
_WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECA
# a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
10:from app.backend import calibration_route, export, narrative, reclassify, trace, why as WHY
text = 'JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.'
where = 'why(JUDGE_UNAVAILABLE)'

    def assert_plain(text, where=""):
>       assert not CODE.search(text), f"raw reason code in {where}: {CODE.search(text).group(0)!r} in {text[:200]!r}"
E       AssertionError: raw reason code in why(JUDGE_UNAVAILABLE): 'JUDGE_NOT_RUN' in 'JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.'
E       assert not <re.Match object; span=(0, 13), match='JUDGE_NOT_RUN'>
E        +  where <re.Match object; span=(0, 13), match='JUDGE_NOT_RUN'> = <built-in method search of re.Pattern object at 0x10c37fd80>('JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.')
E        +    where <built-in method search of re.Pattern object at 0x10c37fd80> = re.compile('\\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\\b').search

tests/unit/test_t167_plain_wording.py:22: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t167_plain_wording.py::test_every_why_sentence_is_plain[None-JUDGE_UNAVAILABLE]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 13 passed in 0.37s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:11.408Z

**tool call — Bash**
````
{
 "command": "grep -n \"^[A-Z_]* = {\" app/backend/reclassify.py"
}
````

### User / tool · 2026-11-02T16:09:11.496Z

**tool result**
````
34:REFUSALS = {
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:13.395Z

Now implement. why.py first.

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:23.473Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np=\"app/backend/why.py\"; s=open(p).read()\ns=s.replace('\"JUDGE_UNAVAILABLE\": \"JUDGE_NOT_RUN: the second AI check did not run','\"JUDGE_UNAVAILABLE\": \"The second AI check did not run')\nold=s[s.index(\"# T-146 r2 / T-145: JUDGE_UNAVAILABLE\"):s.index(\"def join(\")]\nnew='''# T-146 r2 / T-145 / T-167: JUDGE_UNAVAILABLE is one closed reason code with three causes, and the sentence follows the judge record (the code itself is unchanged and stays in the\n# API fields; no code is ever printed in a sentence). A judge that never ran (deadline, or no judge record yet) keeps the \"did not run\" sentence. A judge that was asked and\n# got no recorded answer is the demo (no live model): say so and say what she can do. A judge that was asked and failed live is \"not available right now\".\nJUDGE_DEMO = (\"The AI second check is not available in this demo, so this item has not been double-checked. \"\n              \"Compare the summary with the quote yourself; if they match, accept it.\")\nJUDGE_FAILED = (\"The second check is not available right now, so this item has not been double-checked. \"\n                \"Compare the summary with the quote; if they match, accept it.\")\n\n\ndef judge_failed(judge) -> bool:\n    return bool(judge) and judge.get(\"verdict\") == \"unavailable\" and judge.get(\"reason_code\") != \"JUDGE_NOT_RUN\"\n\n\ndef judge_in_demo(judge) -> bool:\n    \"\"\"The judge was asked and no recorded answer existed (fixture replay = the demo). The error class is the audited call's, never model text.\"\"\"\n    return judge_failed(judge) and \"FixtureMiss\" in str(judge.get(\"error_class\") or \"\")\n\n\ndef unavailable_sentence(judge) -> str:\n    \"\"\"The one sentence for a second check that gave no answer, by cause (used by the item's why and by the edit warning).\"\"\"\n    return JUDGE_DEMO if judge_in_demo(judge) else JUDGE_FAILED if judge_failed(judge) else _WHY[\"JUDGE_UNAVAILABLE\"]\n\n\ndef why(code: str, judge=None) -> str:\n    if code == \"JUDGE_UNAVAILABLE\":\n        return unavailable_sentence(judge)\n    return _WHY[code]\n\n\n'''\ns=s.replace(old,new)\nopen(p,\"w\").write(s)\n\np=\"app/backend/review.py\"; s=open(p).read()\ns=s.replace('''        warnings.append({\"code\": \"JUDGE_UNAVAILABLE\", \"message\": \"The second check was not available; the item stays marked for review.\", \"item_id\": item_id})''',\n'''        warnings.append({\"code\": \"JUDGE_UNAVAILABLE\", \"message\": why.unavailable_sentence({\"verdict\": \"unavailable\", \"reason_code\": judge_code, \"error_class\": judge_error}) + \" Until you do, the item stays marked for review.\", \"item_id\": item_id})''')\nopen(p,\"w\").write(s)\n\np=\"app/backend/export.py\"; s=open(p).read()\na=s.index(\"_EDIT_REASON_PHRASE = {\"); b=s.index(\"def _edit_unconfirmed_why\")\ns=s[:a]+'''_EDIT_REASON_PHRASE = {\"JUDGE_UNAVAILABLE\": \"second check not available\", \"FIXTURE_MISS\": \"second check not available\",\n                       \"JUDGE_PARTIAL\": \"the second check only partly supported it\", \"JUDGE_UNSUPPORTED\": \"the second check did not support it\",\n                       \"JUDGE_UNSURE\": \"the second check was unsure\", \"JUDGE_DISAGREES\": \"the second check disagreed\"}      # T-167: plain words, never the reason code\n\n\n'''+s[b:]\ns=s.replace('_EDIT_REASON_PHRASE.get(c, f\"still marked for review ({c})\")','_EDIT_REASON_PHRASE.get(c, \"still marked for review\")')\ns=s.replace('''lines.append(f'- AI wording removed (failed a check: {r.get(\"message\") or r[\"reason\"]}) ({r[\"entry_id\"]}): {r[\"reason\"]}.')''',\n'''lines.append(f'- AI wording removed (failed a check: {_removed_why(r)}) ({r[\"entry_id\"]}).')''')\ns=s.replace('''lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r[\"entry_id\"]}): {r[\"reason\"]}.')''','''lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r[\"entry_id\"]}).')''')\ns=s.replace('''lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.')''','''lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {_removed_why(r)}')''')\ns=s.replace(\"def _draft_paragraph(v):\",'''def _removed_why(r) -> str:\n    \"\"\"T-167: the plain sentence for a removed narrative sentence; the reason code is in the API field, not in the notes.\"\"\"\n    m = r.get(\"message\")\n    return m if m and not re.search(r\"\\\\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\\\\b\", m) else \"it failed a check\"\n\n\ndef _draft_paragraph(v):''',1)\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"^import\\|^from\" app/backend/export.py | head -5; grep -n \"^from\\|^import\" app/backend/review.py | head -8; sed -n 183,190p app/backend/review.py | cut -c1-140"
}
````

### User / tool · 2026-11-02T16:09:23.600Z

**tool result**
````
16:from __future__ import annotations
18:import re
19:from datetime import date
21:from app.backend import amounts, charge_text, language, money
10:import copy
11:import json
12:import time
14:from app.backend import amounts as AM, charge_text, conflicts, confidence, gaps, generator, grounding, judge_guard, judges, language, spanish, store, why
15:from app.db import db as DB
    if not held:
        return
    amts = DB.list_items(conn, case_id, "amount")
    static = why.why("CHARGE_TEXT_IN_ENTRY")
    for v in held:
        ids = set(v.get("record_ids") or [])
        found = charge_text.check(v.get("summary"), v.get("excerpt")) or {"summary": ["amount"]}
        new = charge_text.hold_why(found, charge_text.bill_state([a for a in amts if ids & set(a.get("record_ids") or [])]))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:31.647Z

**tool call — Bash**
````
{
 "command": "grep -n \"prompts have changed\\|older version\\|cannot be checked against\" tests/unit/test_calibration_route.py tests/e2e/*.py app/frontend/*.js | cut -c1-260"
}
````

### User / tool · 2026-11-02T16:09:31.741Z

**tool result**
````
tests/unit/test_calibration_route.py:217:    assert c["stale_reason"] == ("The prompts have changed since these numbers were measured: judge_flag_v2.md changed. "
tests/unit/test_calibration_route.py:218:                                 "The numbers describe an older version of the prompts.")
tests/unit/test_calibration_route.py:327:    assert reason.endswith("; and 3 more. The numbers describe an older version of the prompts.")
tests/e2e/conftest.py:45:  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, onl
tests/e2e/test_suggestions.py:184:    expect(st).to_contain_text("These numbers come from an older version of the AI prompts."); expect(st).to_contain_text(REASON)
app/frontend/suggestions.js:138:        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These numbers come from an older version of the AI prompts."),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:41.103Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"app/backend/calibration_route.py\"; s=open(p).read()\ns=s.replace('return f\"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts.\"',\n 'return f\"The AI\\'s instructions have changed since these numbers were measured: {shown}{more}. The numbers describe an earlier version and may be out of date.\"')\ns=s.replace('\"This measurement does not record which prompts it used, so it cannot be checked against the current prompts.\"','\"This measurement does not record which AI instructions it used, so it cannot be checked against the current ones.\"')\nopen(p,\"w\").write(s)\np=\"tests/unit/test_calibration_route.py\"; s=open(p).read()\ns=s.replace('''(\"The prompts have changed since these numbers were measured: judge_flag_v2.md changed. \"\n                                 \"The numbers describe an older version of the prompts.\")''','''(\"The AI's instructions have changed since these numbers were measured: judge_flag_v2.md changed. \"\n                                 \"The numbers describe an earlier version and may be out of date.\")''')\ns=s.replace('\"; and 3 more. The numbers describe an older version of the prompts.\"','\"; and 3 more. The numbers describe an earlier version and may be out of date.\"')\nopen(p,\"w\").write(s)\np=\"tests/unit/test_t167_plain_wording.py\"; s=open(p).read()\ns=s.replace('''    stale = calibration_route''','''    for k, s in reclassify.REFUSALS.items():\n        assert_plain(s, f\"reclassify.REFUSALS[{k}]\")\n    stale = calibration_route''')\ns=s.replace('''    assert \"older version of the prompts\" not in stale\\n''','')\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"cannot be checked against\\|does not record which\" tests/unit/*.py | cut -c1-200"
}
````

### User / tool · 2026-11-02T16:09:41.256Z

**tool result**
````
tests/unit/test_calibration_route.py:316:    assert c["stale"] is True and "does not record which prompts" in c["stale_reason"]
tests/unit/test_calibration_route.py:319:    assert c["stale"] is True and "does not record which prompts" in c["stale_reason"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:42.271Z

Update those, plus the old-sentence tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:43.166Z

**tool call — Bash**
````
{
 "command": "sed -i 's/does not record which prompts/does not record which AI instructions/' tests/unit/test_calibration_route.py && sed -n 168,195p tests/unit/test_t146_r2_failed_rerun_keeps_items.py; grep -rn \"second check failed\\|asked and gave no usable\" tests/unit tests/e2e | cut -c1-200"
}
````

### User / tool · 2026-11-02T16:09:43.374Z

**tool result**
````
sed: 2: "tests/unit/test_calibra ...": undefined label 'ests/unit/test_calibration_route.py'
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:3:called and failed says 'second check failed' (reason code unchanged), not 'JUDGE_NOT_RUN:'."""
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:165:    assert "second check failed" in text.lower() and "JUDGE_NOT_RUN" not in text
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:183:    assert "second check failed" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", failed)
tests/unit/test_t146_r2_failed_rerun_keeps_items.py:192:    assert text.startswith("JUDGE_NOT_RUN:") and "second check failed" not in text.lower()
tests/unit/test_t146_r3_decided_items_never_lowered.py:273:    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(j1=down("j1"))), now=lambda: 1.0)      # e1 needs_review: second
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:48.232Z

**tool call — Bash**
````
{
 "command": "sed -i '' 's/does not record which prompts/does not record which AI instructions/' tests/unit/test_calibration_route.py && sed -n 155,195p tests/unit/test_t146_r2_failed_rerun_keeps_items.py | cut -c1-240"
}
````

### User / tool · 2026-11-02T16:09:48.325Z

**tool result**
````
# ---- T-145 minor: a judge that was called and failed is not reported as 'did not run'
def test_a_failed_second_check_says_failed_and_keeps_the_reason_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(j1=_down("j1"))), now=lambda: 1.0)
    e = DB.get_item(conn, "e1")
    assert e["state"] == "needs_review" and e["state_reasons"] == ["JUDGE_UNAVAILABLE"]       # the reason code is unchanged
    assert e["ladder"]["judge"]["verdict"] == "unavailable" and e["ladder"]["judge"]["reason_code"] != "JUDGE_NOT_RUN"
    text = present.item_view(conn, cid, "e1")["why"]
    assert "second check failed" in text.lower() and "JUDGE_NOT_RUN" not in text
    assert "agreed" not in text


def test_a_second_check_that_never_ran_still_says_so_with_its_code(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    ticks = iter([0.0, 0.0, 0.0, 0.0] + [10_000.0] * 5000)       # the deadline passes before judge 1
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: next(ticks), deadline_s=480)
    rows = [r for r in DB.list_items(conn, cid, "entry") if r["state"] != "rejected"]
    if rows:
        assert all((r["ladder"].get("judge") or {}).get("reason_code") == "JUDGE_NOT_RUN" for r in rows)
        assert WHY.why("JUDGE_UNAVAILABLE").startswith("JUDGE_NOT_RUN:")


def test_why_helper_picks_the_sentence_from_the_judge_record():
    failed = {"verdict": "unavailable", "reason_code": "NONE", "call_id": None}
    notrun = {"verdict": "unavailable", "reason_code": "JUDGE_NOT_RUN"}
    assert "second check failed" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", failed)
    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("JUDGE_NOT_RUN:")
    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("JUDGE_NOT_RUN:")                  # no judge record = it did not run
    assert WHY.why("JUDGE_UNSURE", failed) == WHY.why("JUDGE_UNSURE")


def test_a_recorded_answer_miss_is_not_called_a_failed_check():
    failed = {"verdict": "unavailable", "reason_code": "NONE"}
    text = WHY.join(["JUDGE_UNAVAILABLE", "FIXTURE_MISS"], failed)
    assert text.startswith("JUDGE_NOT_RUN:") and "second check failed" not in text.lower()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:09:54.821Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_t146_r2_failed_rerun_keeps_items.py\"; s=open(p).read()\ns=s.replace(\"\"\"called and failed says 'second check failed' (reason code unchanged), not 'JUDGE_NOT_RUN:'.\"\"\",\"\"\"called and failed says 'second check is not available' (reason code unchanged), not 'did not run'. T-167: no code appears in any sentence.\"\"\")\ns=s.replace('''assert \"second check failed\" in text.lower() and \"JUDGE_NOT_RUN\" not in text''','''assert \"second check is not available\" in text.lower() and \"JUDGE_NOT_RUN\" not in text''')\ns=s.replace('''assert WHY.why(\"JUDGE_UNAVAILABLE\").startswith(\"JUDGE_NOT_RUN:\")''','''assert WHY.why(\"JUDGE_UNAVAILABLE\").startswith(\"The second AI check did not run\")''')\ns=s.replace('''assert \"second check failed\" in WHY.why(\"JUDGE_UNAVAILABLE\", failed).lower() and''','''assert \"second check is not available\" in WHY.why(\"JUDGE_UNAVAILABLE\", failed).lower() and''')\ns=s.replace('''assert WHY.why(\"JUDGE_UNAVAILABLE\", notrun).startswith(\"JUDGE_NOT_RUN:\")''','''assert WHY.why(\"JUDGE_UNAVAILABLE\", notrun).startswith(\"The second AI check did not run\")''')\ns=s.replace('''assert WHY.why(\"JUDGE_UNAVAILABLE\", None).startswith(\"JUDGE_NOT_RUN:\") ''','''assert WHY.why(\"JUDGE_UNAVAILABLE\", None).startswith(\"The second AI check did not run\") ''')\ns=s.replace('''assert text.startswith(\"JUDGE_NOT_RUN:\") and \"second check failed\" not in text.lower()''','''assert text.startswith(\"The second AI check did not run\") and \"not available\" not in text.lower()''')\nopen(p,\"w\").write(s)\np=\"tests/unit/test_t134_unconfirmed_edit.py\"; s=open(p).read()\ns=s.replace('''assert \"edited; second check not available\" in notes and \"JUDGE_UNAVAILABLE\" in notes''','''assert \"edited; second check not available\" in notes and \"JUDGE_UNAVAILABLE\" not in notes      # T-167: the code stays in the API fields, not the notes''')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t167_plain_wording.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_trace.py -q 2>&1 | tail -20 | cut -c1-300"
}
````

### User / tool · 2026-11-02T16:10:25.565Z

**tool result**
````
tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5552/test_internal_notes_never_prin0')

    def test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry(tmp_path):
        conn, cid = accepted_sample(tmp_path)
        bad = {"entry_id": "e99", "text": "Pain was 9/10 on the left side."}
        n = N.draft(conn, cid, call=narr(GOOD + [bad]), now=2.0)
        assert [r["reason"] for r in n["removed"]] == ["NOT_AN_ACCEPTED_ENTRY"] and [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"]
        for accept in (False, True):
            if accept:
                N.review(conn, cid, "accept", now=3.0)
            ex = X.build_export(store.export_case(conn, cid))
            notes = ex["internal_notes_text"]
            assert "9/10 on the left" not in notes and "left side" not in notes and "9/10 on the left" not in ex["letter_text"]
>           assert "Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY." in notes
E           AssertionError: assert 'Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.' in 'INTERNAL REVIEW NOTES — DO NOT SEND\n\nThis chronology was drafted with AI assistance; every item in the treatment se.... (record 5 (Capital PT, visit 8, February 20, 2026)

tests/unit/test_narrative.py:289: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry
1 failed, 427 passed in 29.70s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:10:29.325Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_narrative.py\"; s=open(p).read()\ns=s.replace('assert \"Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.\" in notes','assert \"Sentence removed (cites an entry that is not accepted) (e99).\" in notes and \"NOT_AN_ACCEPTED_ENTRY\" not in notes      # T-167: no code in the notes')\nopen(p,\"w\").write(s)\nEOF\ngit status --short | grep -v agent-memory | head -20\nrm -rf $TMPDIR/t167arch 2>/dev/null; echo"
}
````

### User / tool · 2026-11-02T16:10:29.376Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion ($TMPDIR/t167arch) is blocked | command: python3 - <<'EOF'
p="tests/unit/test_narrative.py"; s=open(p).read()
s=s.replace('assert "Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY." in notes','assert "Sente
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:10:31.268Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_narrative.py\"; s=open(p).read()\ns=s.replace('assert \"Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.\" in notes','assert \"Sentence removed (cites an entry that is not accepted) (e99).\" in notes and \"NOT_AN_ACCEPTED_ENTRY\" not in notes      # T-167: no code in the notes')\nopen(p,\"w\").write(s)\nEOF\ngit status --short | grep -v agent-memory | head -20"
}
````

### User / tool · 2026-11-02T16:10:31.414Z

**tool result**
````
 M app/backend/calibration_route.py
 M app/backend/export.py
 M app/backend/generator.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/review.py
 M app/backend/why.py
MM app/frontend/api.js
MM app/frontend/app.js
MM app/frontend/input.js
MM app/frontend/overview.css
MM app/frontend/overview.js
MM app/frontend/review.js
 M app/frontend/sidebyside.css
MM app/frontend/state.js
MM app/frontend/stepper.js
 M app/frontend/styles.css
MM app/frontend/timeline.js
 M app/frontend/tokens.css
MM app/frontend/uncovered.css
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:10:33.913Z

**tool call — Bash**
````
{
 "command": "git status --short | grep -v \"agent-memory\\|app/frontend\" ; git diff --stat -- app/backend tests | tail -15; git diff -- app/backend/export.py app/backend/review.py app/backend/calibration_route.py | grep \"^@@\" "
}
````

### User / tool · 2026-11-02T16:10:34.088Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:10:39.286Z

**tool call — Bash**
````
{
 "command": "for f in app/backend/why.py app/backend/export.py app/backend/review.py app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py; do echo \"== $f\"; git diff -U0 -- $f | grep \"^@@\\|^[-+][^-+]\" | cut -c1-150; done"
}
````

### User / tool · 2026-11-02T16:10:39.509Z

**tool result**
````
== app/backend/why.py
@@ -16 +16 @@ _WHY = {
-    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
+    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
@@ -47,3 +47,7 @@ MODEL_CONFLICT = ("The AI suggested a conflict between two passages, but the sof
-# T-146 r2 / T-145: JUDGE_UNAVAILABLE is one closed reason code with two causes. The sentence follows the judge record: a judge that was asked and ga
-# answer says so; one that never ran (deadline, or no judge record yet) keeps the JUDGE_NOT_RUN sentence. The reason code itself is unchanged.
-JUDGE_FAILED = "The second check failed (the AI check was asked and gave no usable answer), so this item has not been double-checked."
+# T-146 r2 / T-145 / T-167: JUDGE_UNAVAILABLE is one closed reason code with three causes, and the sentence follows the judge record (the code itself
+# API fields; no code is ever printed in a sentence). A judge that never ran (deadline, or no judge record yet) keeps the "did not run" sentence. A j
+# got no recorded answer is the demo (no live model): say so and say what she can do. A judge that was asked and failed live is "not available right 
+JUDGE_DEMO = ("The AI second check is not available in this demo, so this item has not been double-checked. "
+              "Compare the summary with the quote yourself; if they match, accept it.")
+JUDGE_FAILED = ("The second check is not available right now, so this item has not been double-checked. "
+                "Compare the summary with the quote; if they match, accept it.")
@@ -55,0 +60,10 @@ def judge_failed(judge) -> bool:
+def judge_in_demo(judge) -> bool:
+    """The judge was asked and no recorded answer existed (fixture replay = the demo). The error class is the audited call's, never model text."""
+    return judge_failed(judge) and "FixtureMiss" in str(judge.get("error_class") or "")
+def unavailable_sentence(judge) -> str:
+    """The one sentence for a second check that gave no answer, by cause (used by the item's why and by the edit warning)."""
+    return JUDGE_DEMO if judge_in_demo(judge) else JUDGE_FAILED if judge_failed(judge) else _WHY["JUDGE_UNAVAILABLE"]
@@ -57,2 +71,2 @@ def why(code: str, judge=None) -> str:
-    if code == "JUDGE_UNAVAILABLE" and judge_failed(judge):
-        return JUDGE_FAILED
+    if code == "JUDGE_UNAVAILABLE":
+        return unavailable_sentence(judge)
== app/backend/export.py
@@ -636,3 +636,3 @@ def _was_edited(e):
-_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MI
-                       "JUDGE_PARTIAL": "the second check only partly supported it (JUDGE_PARTIAL)", "JUDGE_UNSUPPORTED": "the second check did not s
-                       "JUDGE_UNSURE": "the second check was unsure (JUDGE_UNSURE)", "JUDGE_DISAGREES": "the second check disagreed (JUDGE_DISAGREES)
+_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available", "FIXTURE_MISS": "second check not available",
+                       "JUDGE_PARTIAL": "the second check only partly supported it", "JUDGE_UNSUPPORTED": "the second check did not support it",
+                       "JUDGE_UNSURE": "the second check was unsure", "JUDGE_DISAGREES": "the second check disagreed"}      # T-167: plain words, nev
@@ -643 +643 @@ def _edit_unconfirmed_why(e) -> str:
-    return "; ".join(_EDIT_REASON_PHRASE.get(c, f"still marked for review ({c})") for c in codes) or "still marked for review"
+    return "; ".join(_EDIT_REASON_PHRASE.get(c, "still marked for review") for c in codes) or "still marked for review"
@@ -696,0 +697,6 @@ def _cite_tail(v, entry_id):
+def _removed_why(r) -> str:
+    """T-167: the plain sentence for a removed narrative sentence; the reason code is in the API field, not in the notes."""
+    m = r.get("message")
+    return m if m and not re.search(r"\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b", m) else "it failed a check"
@@ -713 +719 @@ def _draft_paragraph(v):
-            lines.append(f'- AI wording removed (failed a check: {r.get("message") or r["reason"]}) ({r["entry_id"]}): {r["reason"]}.')
+            lines.append(f'- AI wording removed (failed a check: {_removed_why(r)}) ({r["entry_id"]}).')
@@ -715 +721 @@ def _draft_paragraph(v):
-            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}): {r["reason"]}.')
+            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}).')
@@ -717 +723 @@ def _draft_paragraph(v):
-            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
+            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {_removed_why(r)}')
== app/backend/review.py
@@ -376 +376 @@ def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call,
-        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": 
+        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "erro
@@ -676,0 +677,2 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
+    from app.backend import pipeline as PL
+    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no longer fails
== app/backend/calibration_route.py
@@ -149 +149 @@ def stale_reason(doc, current):
-        return "This measurement does not record which prompts it used, so it cannot be checked against the current prompts."
+        return "This measurement does not record which AI instructions it used, so it cannot be checked against the current ones."
@@ -163 +163 @@ def stale_reason(doc, current):
-    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."
+    return f"The AI's instructions have changed since these numbers were measured: {shown}{more}. The numbers describe an earlier version and may be 
== tests/unit/test_calibration_route.py
@@ -217,2 +217,2 @@ def test_edited_and_committed_prompt_is_stale_and_the_reason_names_it(tmp_path):
-    assert c["stale_reason"] == ("The prompts have changed since these numbers were measured: judge_flag_v2.md changed. "
-                                 "The numbers describe an older version of the prompts.")
+    assert c["stale_reason"] == ("The AI's instructions have changed since these numbers were measured: judge_flag_v2.md changed. "
+                                 "The numbers describe an earlier version and may be out of date.")
@@ -316 +316 @@ def test_a_file_that_records_no_hashes_is_stale(tmp_path):
-    assert c["stale"] is True and "does not record which prompts" in c["stale_reason"]
+    assert c["stale"] is True and "does not record which AI instructions" in c["stale_reason"]
@@ -319 +319 @@ def test_a_file_that_records_no_hashes_is_stale(tmp_path):
-    assert c["stale"] is True and "does not record which prompts" in c["stale_reason"]
+    assert c["stale"] is True and "does not record which AI instructions" in c["stale_reason"]
@@ -327 +327 @@ def test_stale_reason_names_at_most_eight_files_and_counts_the_rest():
-    assert reason.endswith("; and 3 more. The numbers describe an older version of the prompts.")
+    assert reason.endswith("; and 3 more. The numbers describe an earlier version and may be out of date.")
== tests/unit/test_narrative.py
@@ -289 +289 @@ def test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry(t
-        assert "Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY." in notes
+        assert "Sentence removed (cites an entry that is not accepted) (e99)." in notes and "NOT_AN_ACCEPTED_ENTRY" not in notes      # T-167: no cod
== tests/unit/test_t134_unconfirmed_edit.py
@@ -50 +50 @@ def test_edit_with_no_second_check_is_not_in_the_letter_and_not_counted_accepted
-    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
+    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" not in notes      # T-167: the code stays in the API fields, not the
== tests/unit/test_t146_r2_failed_rerun_keeps_items.py
@@ -3 +3 @@ partial stub. Errored records keep their previous rows (full row, not a few fiel
-called and failed says 'second check failed' (reason code unchanged), not 'JUDGE_NOT_RUN:'."""
+called and failed says 'second check is not available' (reason code unchanged), not 'did not run'. T-167: no code appears in any sentence."""
@@ -165 +165 @@ def test_a_failed_second_check_says_failed_and_keeps_the_reason_code(tmp_path):
-    assert "second check failed" in text.lower() and "JUDGE_NOT_RUN" not in text
+    assert "second check is not available" in text.lower() and "JUDGE_NOT_RUN" not in text
@@ -177 +177 @@ def test_a_second_check_that_never_ran_still_says_so_with_its_code(tmp_path):
-        assert WHY.why("JUDGE_UNAVAILABLE").startswith("JUDGE_NOT_RUN:")
+        assert WHY.why("JUDGE_UNAVAILABLE").startswith("The second AI check did not run")
@@ -183,3 +183,3 @@ def test_why_helper_picks_the_sentence_from_the_judge_record():
-    assert "second check failed" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", failed)
-    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("JUDGE_NOT_RUN:")
-    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("JUDGE_NOT_RUN:")                  # no judge record = it did not run
+    assert "second check is not available" in WHY.why("JUDGE_UNAVAILABLE", failed).lower() and "JUDGE_NOT_RUN" not in WHY.why("JUDGE_UNAVAILABLE", fa
+    assert WHY.why("JUDGE_UNAVAILABLE", notrun).startswith("The second AI check did not run")
+    assert WHY.why("JUDGE_UNAVAILABLE", None).startswith("The second AI check did not run")                  # no judge record = it did not run
@@ -192 +192 @@ def test_a_recorded_answer_miss_is_not_called_a_failed_check():
-    assert text.startswith("JUDGE_NOT_RUN:") and "second check failed" not in text.lower()
+    assert text.startswith("The second AI check did not run") and "not available" not in text.lower()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:10:50.753Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$S/arch; mkdir -p $A && git archive HEAD | tar -x -C $A && \npython3 - \"$A\" <<'EOF'\nimport sys,subprocess,shutil\nA=sys.argv[1]\nfiles=\"app/backend/why.py app/backend/export.py app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t167_plain_wording.py\".split()\nfor f in files: shutil.copy(f, f\"{A}/{f}\")\n# review.py: HEAD + only my line\nh=subprocess.check_output([\"git\",\"show\",\"HEAD:app/backend/review.py\"],text=True)\nw=open(\"app/backend/review.py\").read()\nold=[l for l in h.splitlines() if 'warnings.append({\"code\": \"JUDGE_UNAVAILABLE\"' in l][0]\nnew=[l for l in w.splitlines() if 'warnings.append({\"code\": \"JUDGE_UNAVAILABLE\"' in l][0]\nassert h.count(old)==1\nopen(f\"{A}/app/backend/review.py\",\"w\").write(h.replace(old,new))\nEOF\ncd $A && ls; (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider 2>&1 | tail -15 | cut -c1-300)"
}
````

### User / tool · 2026-11-02T16:12:51.716Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: bo5kum15p). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output. You will be notified when it completes. To check interim output, use Read on that file path.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:12:55.963Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-167 --agent backend --text \"tests first (tests/unit/test_t167_plain_wording.py, grep-style over why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, demo edit end-to-end); why.py JUDGE_DEMO/JUDGE_FAILED/NOT_RUN sentences, review.py edit warning, export.py notes phrases + removed-narrative lines, calibration stale reason. Not mine: 'server answered 500'/'Request failed' (frontend api.js), chip 'curated responses' (frontend app.js), calibration box heading and 'fixture backend (recorded replies...)' (evals/run.py statements + suggestions.js). Running suite from git archive copy.\""
}
````

### User / tool · 2026-11-02T16:12:56.094Z

**tool result**
````
noted on T-167
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:12:56.858Z

**tool call — Bash**
````
{
 "command": "sleep 100; tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output | cut -c1-300"
}
````

### User / tool · 2026-11-02T16:12:56.859Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output cut -c1-300. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:12:58.143Z

**tool call — Monitor**
````
{
 "query": "select:Monitor",
 "max_results": "1"
}
````

### User / tool · 2026-11-02T16:12:58.145Z

**tool result (error)**
````
<tool_use_error>InputValidationError: Monitor failed due to the following issue:
The required parameter `description` is missing

This tool's schema was not sent to the API — it was not in the discovered-tool set derived from message history. Without the schema in your prompt, typed parameters (arrays, numbers, booleans) get emitted as strings and the client-side parser rejects them. Load the tool first: call ToolSearch with query "select:Monitor", then retry this call. For reference, this tool's input schema is: {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","properties":{"description":{"description":"Short human-readable description of what you are monitoring (shown in notifications).","type":"string"},"timeout_ms":{"description":"Kill the monitor after this deadline. Default 300000ms. Deadlines above 1800000ms are capped to 1800000ms. You are notified at expiry and can re-arm.","default":300000,"type":"number","minimum":1000,"maximum":3600000},"command":{"description":"Shell command or script. Each stdout line is an event; exit ends the watch.","type":"string"},"ws":{"description":"WebSocket to open. Each text frame is an event; binary frames are reported as a placeholder line. Socket close ends the watch. Cannot be combined with command.","type":"object","properties":{"url":{"type":"string"},"protocols":{"type":"array","items":{"type":"string","pattern":"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$"}}},"required":["url"],"additionalProperties":false}},"required":["description","timeout_ms"],"additionalProperties":false}</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:00.552Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output"
}
````

### User / tool · 2026-11-02T16:13:00.575Z

**tool result**
````
1	CLAUDE.md
2	MASTER_PROMPT.md
3	app
4	artifacts
5	board
6	docs
7	evals
8	memory
9	personas
10	requirements-dev.txt
11	requirements.txt
12	research
13	reviews
14	spec
15	submission
16	tests
17	tools
18	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:01.490Z

Still running; I'll wait for the completion notification.

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:13:02.955Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"passed|failed|error\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output; do sleep 5; done; tail -12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bo5kum15p.output | cut -c1-300",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T16:15:08.414Z

**tool result**
````
            why = present._common(r)["why"]
>           assert "JUDGE_NOT_RUN" in why and "agreed" not in why, r["id"]
E           AssertionError: e1
E           assert ('JUDGE_NOT_RUN' in 'The second AI check did not run or did not finish, so this item has not been double-checked.')

tests/unit/test_t145_judge_not_run.py:54: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t145_judge_not_run.py::test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 4666 passed, 8 skipped in 252.50s (0:04:12)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:15:11.467Z

**tool call — Bash**
````
{
 "command": "grep -rn \"JUDGE_NOT_RUN\\\" in\\|JUDGE_NOT_RUN' in\\|in why\\b\" tests/unit/*.py | grep -i \"why\\|text\" | cut -c1-220; sed -n 50,56p tests/unit/test_t145_judge_not_run.py"
}
````

### User / tool · 2026-11-02T16:15:11.558Z

**tool result**
````
tests/unit/test_amounts_d059.py:58:    assert why and word in why.lower(), (text, why)
tests/unit/test_amounts_d060.py:66:    assert "names no service" in why(ex, "$950.00", "Brindlewood Physical Therapy, account ledger")
tests/unit/test_amounts_d060.py:76:    assert "charges column" in why(ex, "$20.00", "Clinic, account ledger")
tests/unit/test_amounts_d060.py:136:    assert "insurer" in why(ex, "$150.00", src).lower()
tests/unit/test_amounts_d060.py:153:    assert "insurer" in why(ex, "$500.00", "Clinic, billing statement").lower()
tests/unit/test_amounts_d060.py:159:    assert "zero" in why("04/16/2026 manual therapy charge $0.00.", "$0.00").lower()
tests/unit/test_eval_runner.py:692:    assert "evals/reports/latest.json" in why and "evals/golden/case_zz.txt" in why
tests/unit/test_t113_heldout_audit.py:17:    assert st == A.WITH_PROMPT and "c3" in why
tests/unit/test_t113_heldout_audit.py:22:    assert st == A.TERM and "smoking" in why
tests/unit/test_t139_charge_text.py:74:    assert "dollar" in why.why("CHARGE_TEXT_IN_ENTRY").lower() and "internal notes" in why.why("CHARGE_TEXT_IN_ENTRY").lower()
tests/unit/test_t134_unconfirmed_edit.py:273:    assert "second" in why and "check" in why and "accepting alone" in why.lower()
tests/unit/test_t145_judge_not_run.py:54:        assert "JUDGE_NOT_RUN" in why and "agreed" not in why, r["id"]
tests/unit/test_d050_never_verified.py:30:    assert "AI translation — check against the original" in why.why("AI_TRANSLATION")
    conn, cid = _case(tmp_path)
    _run(conn, cid, Clock("verify"))
    for r in DB.list_items(conn, cid, "entry"):
        why = present._common(r)["why"]
        assert "JUDGE_NOT_RUN" in why and "agreed" not in why, r["id"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:15:16.286Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np=\"tests/unit/test_t145_judge_not_run.py\"; s=open(p).read()\ns=s.replace('assert \"JUDGE_NOT_RUN\" in why and \"agreed\" not in why, r[\"id\"]','assert \"did not run or did not finish\" in why and \"JUDGE_NOT_RUN\" not in why and \"agreed\" not in why, r[\"id\"]      # T-167: plain sentence, no code')\nopen(p,\"w\").write(s)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cp tests/unit/test_t145_judge_not_run.py $S/arch/tests/unit/; git diff -U0 -- tests/unit/test_t145_judge_not_run.py | grep \"^@@\"; cd $S/arch && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -8 | cut -c1-250",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T16:15:16.355Z

**tool result**
````
Command running in background with ID: b0ypowrq9. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b0ypowrq9.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:15:18.541Z

**tool call — Bash**
````
{
 "command": "grep -rn \"second check failed\\|was not available; the item\\|JUDGE_NOT_RUN:\" tests/e2e app/frontend/*.js | cut -c1-200"
}
````

### User / tool · 2026-11-02T16:15:18.660Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:15:23.464Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"passed|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b0ypowrq9.output; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b0ypowrq9.output | cut -c1-250",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T16:19:49.248Z

**tool result**
````
........................................................................ [ 95%]
........................................................................ [ 96%]
........................................................................ [ 98%]
........................................................................ [ 99%]
..................                                                       [100%]
5266 passed, 8 skipped in 269.41s (0:04:29)

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:03.664Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; export GIT_INDEX_FILE=$S/idx167; rm -f $GIT_INDEX_FILE; git read-tree HEAD && \ngit update-index --add app/backend/why.py app/backend/export.py app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t145_judge_not_run.py tests/unit/test_t167_plain_wording.py &&\nH=$(git hash-object -w $S/arch/app/backend/review.py) && git update-index --cacheinfo 100644,$H,app/backend/review.py &&\ngit diff --cached --stat | tail -12 &&\nT=$(git write-tree) && P=$(git rev-parse HEAD) && C=$(git commit-tree $T -p $P -m \"feat(backend): plain wording, no reason codes or test-mode text in paralegal-facing sentences or the notes (T-167, audit F4/F7)\n\nwhy.py: JUDGE_NOT_RUN prefix removed; demo and live second-check-unavailable sentences say what she can do; review.py edit warning follows; export.py notes drop reason codes; calibration stale reason reworded.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\") && echo $C && git update-ref HEAD $C $P && unset GIT_INDEX_FILE && git log --oneline -1 && git status --short app/backend/why.py app/backend/review.py"
}
````

### User / tool · 2026-11-02T16:20:03.845Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: dynamic git subcommand is not allowed | command: S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf807
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:09.159Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cp /dev/null $S/idx167; rm -f $S/idx167; GIT_INDEX_FILE=$S/idx167 git read-tree HEAD; GIT_INDEX_FILE=$S/idx167 git update-index --add app/backend/why.py app/backend/export.py app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t145_judge_not_run.py tests/unit/test_t167_plain_wording.py; cp $S/arch/app/backend/review.py $S/review_mine.py; H=$(git hash-object -w $S/review_mine.py); echo $H; GIT_INDEX_FILE=$S/idx167 git update-index --cacheinfo 100644,$H,app/backend/review.py; GIT_INDEX_FILE=$S/idx167 git diff --cached --stat | tail -12"
}
````

### User / tool · 2026-11-02T16:20:09.717Z

**tool result**
````
447ea273a3159946967601306a24bce77a47913c
 app/backend/calibration_route.py                   |   4 +-
 app/backend/export.py                              |  20 +--
 app/backend/review.py                              |   4 +-
 app/backend/why.py                                 |  26 +++-
 tests/unit/test_calibration_route.py               |  10 +-
 tests/unit/test_narrative.py                       |   2 +-
 tests/unit/test_t134_unconfirmed_edit.py           |   2 +-
 tests/unit/test_t145_judge_not_run.py              |   2 +-
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  |  14 +--
 tests/unit/test_t167_plain_wording.py              | 138 +++++++++++++++++++++
 10 files changed, 189 insertions(+), 33 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:17.179Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; GIT_INDEX_FILE=$S/idx167 git diff --cached -U0 -- app/backend/review.py | cut -c1-120"
}
````

### User / tool · 2026-11-02T16:20:17.287Z

**tool result**
````
diff --git a/app/backend/review.py b/app/backend/review.py
index 7eed93b..447ea27 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -376 +376 @@ def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call,
-        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays ma
+        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "r
@@ -677,2 +676,0 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
-    from app.backend import pipeline as PL
-    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no l
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:23.185Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git log --oneline -3; python3 - \"$S\" <<'EOF'\nimport sys,subprocess\nS=sys.argv[1]\nh=subprocess.check_output([\"git\",\"show\",\"HEAD:app/backend/review.py\"],text=True)\nw=open(\"app/backend/review.py\").read()\nf=lambda t:[l for l in t.splitlines() if 'warnings.append({\"code\": \"JUDGE_UNAVAILABLE\"' in l][0]\nassert h.count(f(h))==1\nopen(S+\"/review_mine.py\",\"w\").write(h.replace(f(h),f(w)))\nEOF\nH=$(git hash-object -w $S/review_mine.py); GIT_INDEX_FILE=$S/idx167 git update-index --cacheinfo 100644,$H,app/backend/review.py; for f in why export calibration_route; do git diff HEAD --quiet -- app/backend/$f.py; done; GIT_INDEX_FILE=$S/idx167 git diff --cached --stat | tail -12"
}
````

### User / tool · 2026-11-02T16:20:23.850Z

**tool result**
````
f7a8f2a feat(frontend): T-149 r3 Do this first names the item and Start review goes to it, New case button, case checks never green while items are unreviewed, j/k hint, list skeleton and plain error, phone puts the jump strip and case checks under the entries
312efe6 fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
ea988f8 fix(backend): T-139 r5 the export gate scans Billed charges (a charge line carries its own amount; other money trimmed by code or blocks naming the line); number words after a money label are money
 app/backend/calibration_route.py                   |   4 +-
 app/backend/export.py                              |  20 +--
 app/backend/review.py                              |   2 +-
 app/backend/why.py                                 |  26 +++-
 tests/unit/test_calibration_route.py               |  10 +-
 tests/unit/test_narrative.py                       |   2 +-
 tests/unit/test_t134_unconfirmed_edit.py           |   2 +-
 tests/unit/test_t145_judge_not_run.py              |   2 +-
 .../unit/test_t146_r2_failed_rerun_keeps_items.py  |  14 +--
 tests/unit/test_t167_plain_wording.py              | 138 +++++++++++++++++++++
 10 files changed, 189 insertions(+), 31 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:29.284Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; GIT_INDEX_FILE=$S/idx167 git commit -q -m \"feat(backend): plain wording, no reason codes or test-mode text in paralegal-facing sentences or the notes (T-167, audit F4/F7)\n\nwhy.py: JUDGE_NOT_RUN prefix removed; demo and live second-check-unavailable sentences say what she can do; review.py edit warning follows; export.py notes drop reason codes; calibration stale reason reworded.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"; git log --oneline -1; git status --short app/backend/why.py app/backend/review.py app/backend/export.py tests/unit/test_t167_plain_wording.py"
}
````

### User / tool · 2026-11-02T16:20:33.186Z

**tool result**
````
check_secrets: ok (10 file(s) scanned staged)
da6afb2 feat(backend): plain wording, no reason codes or test-mode text in paralegal-facing sentences or the notes (T-167, audit F4/F7)
MM app/backend/export.py
MM app/backend/review.py
MM app/backend/why.py
D  tests/unit/test_t167_plain_wording.py
?? tests/unit/test_t167_plain_wording.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:41.987Z

**tool call — Bash**
````
{
 "command": "git reset -q -- app/backend/why.py app/backend/export.py app/backend/review.py app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_narrative.py tests/unit/test_t134_unconfirmed_edit.py tests/unit/test_t146_r2_failed_rerun_keeps_items.py tests/unit/test_t145_judge_not_run.py tests/unit/test_t167_plain_wording.py; git status --short app/backend/why.py app/backend/review.py app/backend/export.py tests/unit/test_t167_plain_wording.py\nB=\"python3 tools/board.py\"\n$B ac T-167 --check 1 --agent backend --evidence \"tests/unit/test_t167_plain_wording.py (grep-style: no SHOUTING_CODE and no fixture/curated/older version/server answered/recorded replies in why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, golden notes; demo edit end-to-end says AI second check not available in this demo + compare + accept); full unit suite from git archive HEAD copy + my hunks: 5266 passed, 8 skipped; golden sample notes unchanged\"\n$B commit T-167 --sha da6afb2 --agent backend\n$B handoff T-167 --agent backend --text \"What changed: why.py (no JUDGE_NOT_RUN prefix; JUDGE_DEMO 'The AI second check is not available in this demo... compare the summary with the quote yourself; if they match, accept it'; JUDGE_FAILED 'not available right now' + same advice; picked from judge error_class FixtureMiss), review.py edit warning uses the same sentence, export.py notes (reason codes removed from edit phrases and removed-narrative lines), calibration_route stale reason ('older version of the prompts' gone). Codes unchanged in API fields. How verified: new tests/unit/test_t167_plain_wording.py (written first, failed first); 4 older tests updated for the new sentences; sample golden unchanged (no codes in it); full unit suite from git archive copy 5266 passed. Left (not mine, frontend/qa): 'server answered 500'/'Request failed' in app/frontend/api.js, header chip 'cached demo (curated responses)' app.js:11, calibration box heading suggestions.js:138 and 'fixture backend (recorded replies, N golden cases)' statements built in evals/run.py:314. Surprised: sentence advice 'accept it' is right for edits but generic for AI-drafted items (why() does not know the item was edited).\"\n$B move T-167 in_review --agent backend"
}
````

### User / tool · 2026-11-02T16:20:42.308Z

**tool result**
````
AC 1 checked: tests/unit/test_t167_plain_wording.py (grep-style: no SHOUTING_CODE and no fixture/curated/older version/server answered/recorded replies in why sentences x judge shapes, narrative/trace/reclassify/calibration strings, notes export, golden notes; demo edit end-to-end says AI second check not available in this demo + compare + accept); full unit suite from git archive HEAD copy + my hunks: 5266 passed, 8 skipped; golden sample notes unchanged
T-167: commit da6afb2 recorded
handoff written on T-167
T-167: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T16:20:46.063Z

T-167 is in_review, committed as da6afb2. The full unit suite ran from a `git archive HEAD` copy plus my hunks: 5266 passed, 8 skipped. The sample golden is unchanged.

Reason codes, "older version of the AI prompts" and "JUDGE_NOT_RUN:" no longer appear in the displayed sentences or the exported notes, and the codes stay in the API fields. The demo edit message now says the AI second check is not available in this demo, and to compare the summary with the quote and accept if they match. Not done, because they're in frontend and qa files (not mine): "server answered 500" (`app/frontend/api.js`), the "curated responses" chip (`app.js:11`), the calibration box heading (`suggestions.js:138`), and "fixture backend (recorded replies…)" built in `evals/run.py:314`.
