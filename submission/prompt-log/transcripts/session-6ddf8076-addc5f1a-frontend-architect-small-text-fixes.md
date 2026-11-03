# Subagent: Frontend + architect small text fixes (Frontend + architect small text fixes)

Source: `agent-addc5f1a31dcb3174.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:26:01.580Z

You are a frontend worker in /Users/arsis/zlayt-pm-project. Your card is T-209, P1; claim it. Read the T-202 correction note (`python3 tools/board.py show T-202`) and the D-071 addendum.

In app/frontend/guided/step3.js, change `confirmNext` so it tells the user that the letter shows a blank "date of service [__________]", which they fill in from the highlighted words. Drop "type the date into your letter yourself". Update the matching e2e test assertion in tests/e2e/guided/test_t206.py.

Another frontend worker is editing guided app.js and classic judges.js on T-204; don't touch those files. Verify the guided suite from a fresh `git archive` (E2E_REQUIRE_DB=1). Commit through `git commit` with a temp index built from the current HEAD, move the card to in_review, and reply in 1 line.

### User / tool · 2026-11-03T01:26:01.585Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:26:04.509Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-209 --agent frontend; $B show T-202 | tail -40; $B show T-209; grep -n \"D-071\" -A15 memory/ORCHESTRATOR_DECISIONS.md | tail -40; grep -n \"confirmNext\" -B2 -A12 app/frontend/guided/step3.js; grep -n \"type the date\\|confirm\" tests/e2e/guided/test_t206.py"
}
````

### User / tool · 2026-11-03T01:26:04.775Z

**tool result**
````
T-209 claimed by frontend
    - [major] Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date — fix: Expose the D-071 service date or period on each charge in the case view (backend: dos_iso/dos_end_iso, or the T-200 'not stated' state). Show it on the Step 3 card exactly as the letter will print it, with the statement date labelled as such: 'Service J
    - [major] letter_check's date check accepts any service date the record states, not the line's own, so the wrong-date class passes; AC wording ('equals the service date in its quote') is not what it checks — fix: Pin the per-line expected date in the goldens: case_09, lib14 and lib10 expected letters, plus the T2/T3 probe shapes as SYNTHETIC cases. Make the check tie the date to the line's row
    - [minor] Some charge quotes name neither the service nor the date the line now prints (pre-existing quote span, unchanged by T-202) — fix: Quote the whole bill line from its code or description through the figure ('Rev 0120 room and board semi-private ... FL47 total charges $4,920.00.'; 'A0425 ground mileage, loaded, 8.7 miles ... charge $187.05.').
- 2026-11-02T23:48:15Z orchestrator: assigned: backend
- 2026-11-02T23:48:15Z orchestrator: Round 2 queued: starts when the staff r1 review lands (fold both). Paralegal blockers: ledger with Posted column before DOS prints the posting date; CMS-1500 with two service dates puts the first on every line; Step 3 still shows the statement date; letter_check passes the CMS-1500 mis-date.
- 2026-11-02T23:55:16Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-202-staff-engineer.md
- 2026-11-02T23:55:16Z orchestrator: Errata for reviews/T-202-staff-engineer.md: the 'two service dates' evidence is amounts.py:500 (non-row) and :493 (row), not :507.
- 2026-11-02T23:55:16Z orchestrator: Round 2 per the D-071 amendment (print a date only when certain; otherwise the not-stated form + Step 3 confirm note). Fold all paralegal and staff r1 blockers/majors; adversarial layout fixtures; independent per-line letter_check; Step 3 shows the same date as the letter (frontend may need a field: put it in the API and tell the orchestrator).
- 2026-11-02T23:55:32Z orchestrator: assigned: backend
- 2026-11-02T23:55:32Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:00:59Z backend: r2 started: adversarial fixtures tests/unit/test_t202_r2_service_date_layouts.py written first, RED on f0921e4 code: 33 failed, 15 passed. Rule I will implement: print a date only when exactly one unambiguous date/complete period is tied to the line by header/row; ambiguous numeric resolved only when one reading is after the record's own date (a service cannot follow its statement) else not-stated.
- 2026-11-03T00:16:07Z backend: r2 committed 986fc55 (unit/e2e from git archive running). New: app/backend/service_date.py; fixtures tests/unit/test_t202_r2_service_date_layouts.py (33 red on f0921e4 -> 0); letter_check rewritten (own scanner); API field amounts[].service_date. Corpus letters byte-identical to f0921e4 (84 charge lines diffed).
- 2026-11-03T00:16:38Z backend: AC 1 checked: r2 986fc55: tests/unit/test_t202_r2_service_date_layouts.py 48 cases (33 red on f0921e4 -> all pass); letter_check value 0 over 25 cases, mutants fail it (drop period end 16, record date 28, bare statement 20, record first date 6); unit + guided e2e from git archive 986fc55 (see handoff)
- 2026-11-03T00:19:45Z backend: moved in_progress -> in_review
- 2026-11-03T00:19:55Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-03T00:29:34Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r2.md; round 2; findings:
    - [blocker] A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date — fix: Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never 
    - [major] Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter — fix: Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of s
    - [minor] The not-stated string differs from the one quoted in the D-071 amendment — fix: Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.
    - [minor] A ledger column headed 'Trans Date' is read as the date of service — fix: Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.
    - [minor] A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill — fix: Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').
    - [minor] Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now) — fix: Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.
    - [minor] Carried from round 1: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T00:29:34Z orchestrator: assigned: backend
- 2026-11-03T00:29:34Z orchestrator: Round 3 queued until staff r2 lands. Paralegal r2 blocker: a date in prose (birth/injury/onset/referral/order) prints as DOS -> per D-071 amendment a date counts only if tied to a DOS column header, a DOS/service label ('DOS', 'date of service', 'service date', 'seen on', 'visit date') or the charge row's own date cell; any other date = not certain. Major: 'not stated' printed above quotes that do state one.
- 2026-11-03T00:30:26Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r2.md
- 2026-11-03T00:30:26Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read."
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:45:37Z backend: (correction: the two empty notes above were a shell slip; the exact LLM_VS_CODE text for the architect is in the note just above and on T-207.)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not stated)". Both are gone. Replace those two sentences with exactly: "Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it." Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date.
- 2026-11-03T01:25:40Z backend: AC 1 checked: r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)
- 2026-11-03T01:25:40Z backend: moved in_progress -> in_review
- 2026-11-03T01:25:49Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r3, 5703fc4 + 973b542): service_date.py is now an ALLOW-LIST: a date is the service date only if a column heading names service (DOS, date of service, from/to service, 24A ...), a service label ends its clause (DOS, date of service, seen on, visit date, visit of, run of; UB-04 'statement covers period'), it is the row cell under such a heading, or (coded bill line with no label) the bill's one period-labeled date. Birth/injury/onset/referral/order/entry/transaction/posted/statement/unlabeled dates are never read; a visit note keeps its own date. Unreadable-but-labeled dates (ambiguous, 2-digit year incl. 'Mar 5, 26', no year, invalid, several, after the statement or >5y before it) and no-label lines ALL print the D-071 addendum blank 'date of service [__________] (statement dated X)' (export.charge_when, store.charge_service_date; confirm_note names the date as written; notes get a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section). evals/letter_check.py: own allow-list scanner (string phrase list, own heading test), accepts the blank and nothing else for a not-certain line, fails a date no label ties, a blank above a certain labeled date, a wrong statement date. api.md updated. | Verified from git archive 973b542: unit 6121 passed/14 skipped, guided e2e 143 passed, letter_check 0 over 25 cases; corpus charge headers byte-identical to 986fc55 (84 lines). New test_t202_r3_allow_list.py: 144 cases, every paralegal/staff probe (B3,B7-B12,N5,N11,N12,N14,N16,N17,P10, Entry/Transaction/Issued/Printed headings, DOI/DOB/authorization, 1998/2031, Mar 5 26, all-vs-any), red first (74 failed on 986fc55 before the fix), 24 mutants (resolver, store, export, letter_check; all->any among them) all killed; production letter vs independent check agree on 45 layouts. | Left: Step 3 frontend text 'type the date into your letter yourself' still describes the old no-blank flow (frontend card); architect T-207 row 3 must be corrected to the blank wording (note on T-207); not done: quote-span minor (charge quotes naming neither service nor date) and a Step 3 control to enter a confirmed date. Crossings: edited tests/e2e/guided/test_round2.py + test_t205.py (one assertion each) and tests/unit test_t200/test_t202_charge (new blank text). | Surprise: a bare 'Date' column and unlabeled leading dates (03/13/2026 exam charge) are now not-certain by the allow-list; existing r2 fixtures needed DOS labels.

---
id: "T-209"
title: "Step 3 confirm note matches the letter's fillable date blank (not 'type the date into your letter yourself')"
milestone: "M3"
role: "frontend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T01:25:49Z"
updated_at: "2026-11-03T01:26:04Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T01:26:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "confirmNext in guided step3.js says the letter shows a blank 'date of service [____]' to fill from the highlighted words; e2e updated", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T01:26:04Z frontend: claimed

## Handoff (filled when moving to in_review)

84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
85-T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
86-
87:## D-071 amendment — when the service date is not certain, print none and ask the human
88-T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
89-
90-## D-072 — The prompt log is built and privacy-reviewed once, last
91-Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
34-  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
35-  /* T-206: the note says what to do next, with the buttons this card really has (it has no control to type a date, so the letter keeps "not stated" and she adds the date herself) */
36:  const confirmNext = () => h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "check the date in the highlighted words, then press ", h("b", {}, "Yes, count it"), " or ", h("b", {}, "No, don't count it"), ". If you count it, type the date into your letter yourself.");
37-
38-  function present(S, item) {
39-    const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
40-    const sd = sdOf(item), st = stmtDated(item, sd, rec);
41-    const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
42-    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r)) : null }));
43-    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, st) : "", nodes: srcNodes };
44-    const sub = rec ? [rec.source_label, rec.date_iso ? (st ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
45-    const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
46-    const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
47-    const flag = item.flag && item.confirm_required ? item.flag : null;
48-    const note = item.duplicate_note ? h("p", { class: "explain muted gap-top", "data-testid": "duplicate-note" }, R.plain(item.duplicate_note)) : null;
--
61-      return { tag: { cls: "ok", text: "Charge" }, sub, src,
62-        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
63:        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
64-        question: "Should this charge count toward the bill total?",
65-        yes: { label: "Yes, count it", disabled: () => (!!flag && !ticked("flag")) || (!!disp && !ticked("compare")),
66-          run: () => S.decide(item, "accept", { ...(flag ? { confirm: flag.confirm_with } : {}), ...(disp && ticked("compare") ? { compared: true } : {}) }) },
67-        no: { label: "No, don't count it", run: () => S.decide(item, "dismiss") }, third: null };
68-    }
69-
70-    if (kind === "count") {
71-      const cc = item.count_confirm, foot = [h("span", { "data-testid": "count-hint" }, "You can still count it if you checked the ledger yourself."), R.check(S, "separate", "I checked this is a separate charge for a service.")];
72-      if (cc) foot.push(h("p", { class: "foot-warn", "data-testid": "count-confirm-message" }, R.plain(cc.message)), R.check(S, "flag", flagBox(cc)));
73-      if (disp) foot.push(h("hr", { class: "foot-rule" }), h("strong", { "data-testid": "compare-reason" }, R.disputeText(disp, item)), compareBox());
74-      return { tag: { cls: "warn", text: "Not counted yet" }, sub, src,
75-        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), h("p", { class: "explain gap-top", "data-testid": "reason" }, R.plain(item.not_counted_reason || item.why)), note],
2:taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
29:        assert page.get_by_test_id("confirm-note").count() == 0
40:    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
41:                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
54:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="ambiguous_numeric", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("ambiguous_numeric", "04/05/2026"))
64:    nxt = page.get_by_test_id("confirm-next"); expect(nxt).to_be_visible()
66:    assert "check the date in the highlighted words" in t.lower() and "Yes, count it" in t and "No, don't count it" in t and "type the date into your letter yourself" in t, t
69:    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-next]").count() == 1
70:    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
78:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
88:    expect(phone.get_by_test_id("confirm-next")).to_be_visible()
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:26:07.189Z

**tool call — Bash**
````
{
 "command": "sed -n 1,6p tests/e2e/guided/test_t206.py; sed -n 60,70p tests/e2e/guided/test_t206.py; git status --short | head -20; cat .claude/agent-memory/frontend/feedback_verify_from_archive.md | head -40"
}
````

### User / tool · 2026-11-03T01:26:07.323Z

**tool result**
````
"""T-206 (D-071 follow-up to T-205, paralegal review minors): a Step 3 card shows a bare date only when it is a certain service date. An uncounted ledger line (lib11 a2-a4) and every other amount
taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
the words of the buttons the card has. Real browser, fixture backend, real API; the doubtful-date note is the backend's own sentence put into the case response (the fixture set has no such bill)."""
import re
from playwright.sync_api import expect
from tests.e2e.guided.test_shell_smoke import watch, go
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(page, tok, "a2", step="bills")
    nxt = page.get_by_test_id("confirm-next"); expect(nxt).to_be_visible()
    t = nxt.inner_text()
    assert "check the date in the highlighted words" in t.lower() and "Yes, count it" in t and "No, don't count it" in t and "type the date into your letter yourself" in t, t
    labels = [page.get_by_test_id("answer-yes").inner_text().strip(), page.get_by_test_id("answer-no").inner_text().strip()]
    assert labels == ["Yes, count it", "No, don't count it"], "the sentence names the buttons the card really has"
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-next]").count() == 1
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
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
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
---
name: verify-from-git-archive
description: Verify a frontend commit from a git archive of the commit tree, never the dirty tree; temp-index commit recipe and the confirm-dialog Escape race
metadata:
  type: feedback
---

Run e2e from `git archive <tree>` (tree from `GIT_INDEX_FILE=tmp git write-tree`) with `E2E_REQUIRE_DB=1`; a plain pytest there starts its own private server on a free port.

**Why:** T-154 r2 committed the a-key guard inside mountSection() (ReferenceError on every case load) while 12/12 passed on the dirty tree where other workers' hunks and the guard sat elsewhere. tests/e2e/test_no_console_errors.py now fails CI on any pageerror.

**How to apply:** build the commit with a temp index (`git read-tree HEAD`, `update-index --cacheinfo` for a file with others' hunks, `--add` for my own files); the check_stale_index hook blocks it if HEAD moved, so re-read-tree and recheck `git diff --stat OLD HEAD -- app/frontend tests/e2e`. The shared scratchpad has many dirs named arch/head0/etc; use a fresh name with mkdir -p.

Pitfall: ZL.confirmCharge (charges.js) must settle on the `cancel` event and ignore a stale `close` when the dialog is open again, else Escape then `a` is dropped (item still busy) or the reopened window is shut.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:26:10.372Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/frontend/guided/step3.js'\ns=open(p).read()\nold='''\". If you count it, type the date into your letter yourself.\");'''\nnew='''\". If you count it, the letter shows a blank \", h(\"b\", {}, \"date of service [__________]\"), \" for you to fill in from the highlighted words.\");'''\nassert s.count(old)==1\ns=s.replace(old,new)\ns=s.replace(\"(it has no control to type a date, so the letter keeps \\\"not stated\\\" and she adds the date herself)\",\"(it has no control to type a date: the letter shows the fillable blank \\\"date of service [__________]\\\" and she fills it from the highlighted words)\")\nopen(p,'w').write(s)\np='tests/e2e/guided/test_t206.py'\ns=open(p).read()\nold='\"type the date into your letter yourself\" in t, t'\nnew='\"date of service [__________]\" in t and \"fill in from the highlighted words\" in t and \"yourself\" not in t, t'\nassert s.count(old)==1\nopen(p,'w').write(s.replace(old,new))\nEOF\ngit diff --stat -- app/frontend/guided/step3.js tests/e2e/guided/test_t206.py; grep -rn \"type the date\" app tests | head"
}
````

### User / tool · 2026-11-03T01:26:10.535Z

**tool result**
````
 app/frontend/guided/step3.js  | 4 ++--
 tests/e2e/guided/test_t206.py | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:26:14.576Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/t209 && mkdir -p $S/t209/tree && export GIT_INDEX_FILE=$S/t209/idx && git read-tree HEAD && git update-index --add app/frontend/guided/step3.js tests/e2e/guided/test_t206.py && T=$(git write-tree) && unset GIT_INDEX_FILE && git archive $T | tar -x -C $S/t209/tree && cd $S/t209/tree && ln -sf /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/guided -q -x -p no:cacheprovider 2>&1 | tail -8; echo $T",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T01:29:27.032Z

**tool result**
````
........................................................................ [ 50%]
.......................................................................  [100%]
143 passed in 190.09s (0:03:10)
13bdb1e5b264c49893e337585615490e810cbe6c
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:29:32.341Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ngit diff --stat HEAD -- app/frontend/guided/step3.js tests/e2e/guided/test_t206.py | tail -1\nexport GIT_INDEX_FILE=$S/t209/idx2; git read-tree HEAD && git update-index --add app/frontend/guided/step3.js tests/e2e/guided/test_t206.py && T=$(git write-tree)\nC=$(git commit-tree $T -p HEAD -m \"fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"); unset GIT_INDEX_FILE\ngit update-ref refs/heads/$(git symbolic-ref --short HEAD) $C $(git rev-parse HEAD) && git reset -q -- app/frontend/guided/step3.js tests/e2e/guided/test_t206.py; git show --stat --oneline HEAD | head; \n$B ac T-209 --check 1 --agent frontend --evidence \"guided e2e from git archive $T: 143 passed (E2E_REQUIRE_DB=1); test_t206 asserts blank wording\"\n$B handoff T-209 --agent frontend --text \"What changed: step3.js confirmNext now says the letter shows a blank 'date of service [__________]' to fill in from the highlighted words; dropped 'type the date into your letter yourself'; test_t206.py assertion updated. Verified: guided e2e from git archive, 143 passed. Left: nothing. Surprise: none.\"\n$B commit T-209 --sha $(git rev-parse HEAD) --agent frontend; $B move T-209 in_review --agent frontend"
}
````

### User / tool · 2026-11-03T01:29:32.410Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: git symbolic-ref rewrites or prunes history; blocked | command: B="python3 tools/board.py"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scrat
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:29:35.774Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nexport GIT_INDEX_FILE=$S/t209/idx2; git read-tree HEAD && git update-index --add app/frontend/guided/step3.js tests/e2e/guided/test_t206.py && git commit -q -m \"fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"; unset GIT_INDEX_FILE\ngit show --stat --oneline HEAD | head -5; git status --short app/frontend/guided/step3.js tests/e2e/guided/test_t206.py"
}
````

### User / tool · 2026-11-03T01:30:03.862Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
88c73dd fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)
 app/frontend/guided/step3.js  | 4 ++--
 tests/e2e/guided/test_t206.py | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
MM app/frontend/guided/step3.js
MM tests/e2e/guided/test_t206.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:30:06.828Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; git reset -q -- app/frontend/guided/step3.js tests/e2e/guided/test_t206.py; git status --short app/frontend/guided/step3.js tests/e2e/guided/test_t206.py\n$B ac T-209 --check 1 --agent frontend --evidence \"guided e2e from git archive of tree 13bdb1e: 143 passed (E2E_REQUIRE_DB=1); test_t206 asserts the blank wording\"\n$B handoff T-209 --agent frontend --text \"What changed: step3.js confirmNext says the letter shows a blank 'date of service [__________]' to fill in from the highlighted words; dropped 'type the date into your letter yourself'; test_t206.py assertion updated. Verified: guided e2e from git archive, 143 passed. Left: nothing. Surprise: none.\"\n$B commit T-209 --sha 88c73dd --agent frontend; $B move T-209 in_review --agent frontend"
}
````

### User / tool · 2026-11-03T01:30:07.184Z

**tool result**
````
AC 1 checked: guided e2e from git archive of tree 13bdb1e: 143 passed (E2E_REQUIRE_DB=1); test_t206 asserts the blank wording
handoff written on T-209
T-209: commit 88c73dd recorded
T-209: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:30:08.333Z

T-209 is in review (commit 88c73dd): the Step 3 `confirmNext` now says the letter shows a blank "date of service [__________]" to fill in from the highlighted words, and the guided e2e suite passes (143 passed) from a fresh `git archive`.
