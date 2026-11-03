# T-157 review r2: staff-engineer-reviewer (commit 852b060)

Verdict: **changes** (0 blockers, 1 major, 5 minors, 1 nit). Verdict rule: no blocker, so not fail; one major, so changes.

Scope: commit 852b060, the r2 fix. HEAD has moved to 2ac96cf (a T-140 commit); I did not review 2ac96cf. Reviewed on a `git archive 852b060` copy with untracked `artifacts/review-evidence` overlaid (tests read it). Fixture backend, in-process TestClient, no live app URL, no UI.

What holds:
- Titles: control, zero-width and bidi characters are removed before the markup check. `<` or `>` and titles over 120 characters are `422 invalid_title`, nothing is stored, and the message never echoes the text. The PDF `?title` is checked before the file is read.
- next_action: blockers come first (NOTHING_ACCEPTED yields to a waiting item), then timeline order with an id tie-break. Six of the ordering and blocker mutants die.
- Live definition: `api.live_enabled` calls `store.live_enabled`, and `rerun_available` goes through `store.live_model_available`, which calls the same function. The baseline demo gate is correct.
- Full `tests/unit` on the clean archive: 4778 passed, 8 skipped, exit 0. This matches the card's evidence.

What does not hold:
- The unconfirmed-edit class drops out of next_action with no test failing (major, finding 1). The live-definition test compares the API with the store by identity and cannot fail for a definition change (minor, finding 6).
- An HTML-entity-encoded title is stored verbatim. It is inert today, but it is not refused (finding 2).

Mutants (scratch copy, one at a time, restored and confirmed; baseline 40 passed, restored 40 passed):
- killed: A waiting[-1]; B first=None; C seq/rank swap; D undated first; E markup check off; F derived tags kept; G NOTHING_ACCEPTED not yielded; H blockers lose to waiting; I length cap off; J bidi not stripped; L rerun ignores live model; N api.live_enabled diverges.
- survived: K unconfirmed edit not waiting (test_case_list.py: 40 passed); M store.live_enabled drops ENABLE_LIVE (40 passed).

Findings (detail in the JSON block):
1. major: next_action drops unconfirmed edits from the waiting set (mutant K survives; the reworded-entry case changes its pick from e1 to f_r2_1).
2. minor: entity-encoded titles stored verbatim (201).
3. minor: create silently ignores a non-text `title` (201), while PATCH returns 400.
4. minor: PATCH validates the title before the token lookup, so an unknown token with a bad title gets 422, not the 404 that api.md states.
5. minor: derived title drops all text after a stray `<` (api.md says brackets are dropped, not the text after them).
6. minor: the live-definition test is tautological for the demo flag; mutant M survives, and a probe shows the public demo gate flips (`demo_mode` False, non-recorded text 201).
7. nit: `Untitled case` fallback still in app/frontend/overview.js:51 (carry-over from r1, outside this commit).

Questions for Chris are in the JSON block.

```json
{"card": "T-157", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 852b060 (r2 fix): app/backend/api.py, case_list.py, store.py, memory/contracts/api.md, tests/unit/test_case_list.py. HEAD at review time was 2ac96cf (not reviewed). Reviewed on a git archive copy of 852b060 at /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-157-r2-852b060 with untracked artifacts/review-evidence overlaid (cp -Rn). Fixture backend, in-process TestClient, no app URL. Case under test: evals/library/case_lib02 (reworded entry), plus every library case for next_action.",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-157-staff-engineer.md (r1), .claude/agent-memory/staff-engineer-reviewer/project_t157_case_title_next_action_patterns.md",
  "python3 tools/board.py show T-157: status in_review, commits [926bf37, 852b060], rounds 1, AC 1 done with the r2 evidence text",
  "git rev-parse --short HEAD -> 2ac96cf; git log --oneline -5 (852b060 is the r2 commit, 2ac96cf is later and out of scope)",
  "git show 852b060 -- app/backend/api.py app/backend/case_list.py app/backend/store.py memory/contracts/api.md (full diff read) and git show --stat 852b060 (5 files, 321 insertions, 32 deletions)",
  "git archive 852b060 | tar -x into the scratchpad T-157-r2-852b060; cp -Rn artifacts/review-evidence overlay; five in-scope files diffed against git show 852b060:<path> (identical)",
  ".venv/bin/python -I -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider on the archive: '40 passed in 11.33s'",
  ".venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider on the archive: '4778 passed, 8 skipped in 286.67s (0:04:46)', exit 0 (output file T-157-r2-full-unit.out in the scratchpad)",
  "read tests/unit/test_case_list.py in full (lines 1-520 of the archive copy) and app/backend/case_list.py, store.py, present.py:37-47, api.py:112-122, api.py:240-350",
  "mutant run on a second archive copy T-157-r2-mut (no overlay, test_case_list only): script T-157-r2-mutate.py, output T-157-r2-mutants.out; 14 mutants: A waiting[-1] KILLED (2 failed); B first=None KILLED (2); C seq/rank swap KILLED (1); D undated first KILLED (3); E markup check off KILLED (4); F derived tags kept KILLED (2); G NOTHING_ACCEPTED not yielded KILLED (2); H blockers lose to waiting KILLED (2); I length cap off KILLED (2); J bidi not stripped KILLED (1); K unconfirmed edit not waiting SURVIVED (40 passed); L rerun ignores live model KILLED (17); M store.live_enabled drops ENABLE_LIVE SURVIVED (40 passed); N api.live_enabled diverges KILLED (6). Baseline and restored runs: 40 passed",
  "title probe T-157-r2-probe.py (python -I, fixture env, TestClient): ASCII <img onerror> -> 422 invalid_title; entity &lt;img -> 201 stored verbatim; double-encoded &amp;lt; -> 201 verbatim; fullwidth U+FF1C/FF1E, U+2039/203A, U+FE64/FE65 -> 201 stored verbatim (inert); NUL/BEL and ZWJ removed -> 201; 120 chars -> 201; 121 chars -> 422; 120 visible + 10 controls -> 201; int title on create -> 201 with name null; name=<b>x</b> -> 422; name of 200 chars -> 201 cut; PATCH <img> -> 422, PATCH entity -> 200 stored, PATCH fullwidth -> 200 stored, PATCH int/bool -> 400; stored name unchanged after refused PATCH; PATCH unknown token with valid title -> 404, with markup or 121 chars -> 422, with int title or no title -> 400",
  "bypass probe T-157-r2-probe4.py: '<' followed by U+200B, NUL, U+202E, VT, or '<' after U+2028 / U+0085 -> REFUSED; numeric entities &#60; and &#x3c; and \\u003c -> STORED verbatim; legacy stored markup via readable_name -> 'Smith records' (tags dropped at read)",
  "derived title probe T-157-r2-probe2.py (baseline): plain_title('<img ...>Marrowgate ED') -> 'Marrowgate ED'; plain_title('Marrowgate <img src=x onerror=alert(1) ED') -> 'Marrowgate'; plain_title(\"St. Mary's <3 Clinic\") -> \"St. Mary's\"; plain_title('&lt;b&gt;Clinic') -> stored as text",
  "demo gate probe T-157-r2-probe2.py with ANTHROPIC_API_KEY set, ENABLE_LIVE unset, LLM_BACKEND=anthropic-api: baseline GET /api/health demo_mode True, live_enabled False, backend fixture; POST /api/cases non-recorded text -> 409 demo_mode_unsupported_input. Under mutant M (store.py:15 ENABLE_LIVE check dropped): demo_mode False, live_enabled True, POST -> 201. Mutant file restored and diffed against git show 852b060",
  "next_action probe T-157-r2-probe3.py: all 15 library cases run on the fixture, reworded entry on case_lib02 (edit_to_check). Baseline: edit item e1 in waiting True, next_action e1 (output T-157-r2-probe3-base.out). Mutant K (case_list.py:147 drops edit_unconfirmed): e1 in waiting False, next_action f_r2_1 (output T-157-r2-probe3-K.out); diff shows only the case_lib02 line changes. Mutant restored and diffed",
  "grep -rn innerHTML app/frontend -> only a comment (app/frontend/sidebyside.js:5); grep -n Untitled case app/frontend/overview.js -> line 51; grep title readers in app/backend (none reach the export, the letter or a prompt)",
  "not exercised: a live app URL (none), the eval runner (not in the T-157 brief), the UI (no frontend change in this commit)"
 ],
 "verdict": "changes",
 "scores": {"card_acs_implemented": 4, "tests_prove_acs": 3, "title_input_validation": 4, "rerun_available_correct": 4, "next_action_determinism": 3, "contract_consistency": 3, "honest_failure": 3},
 "findings": [
  {"severity": "major",
   "title": "next_action drops unconfirmed edits from the waiting set; the mutant survives and changes the named item",
   "evidence": "app/backend/case_list.py:147 'if not (r[review_status] == pending or review.edit_unconfirmed(kind, r)):' (double quotes shown as single). Mutant: drop the edit_unconfirmed clause; pytest tests/unit/test_case_list.py -q on the mutant copy: '40 passed in 9.84s' (SURVIVED). Probe T-157-r2-probe3.py: baseline 'edit item id: e1 in waiting: True' and 'next_action second: e1'; under the mutant 'edit item id: e1 in waiting: False' and 'next_action second: f_r2_1'. Tests: tests/unit/test_case_list.py:247-251 checks the waiting list only when next_action is None; :258-261 checks membership only against the items next_action already named, so an omitted class is invisible.",
   "why_it_matters": "memory/contracts/api.md line 703 defines the queue as including 'an edit not yet confirmed'. Dropping that class points the paralegal at the next decided-looking item and never at the reworded entry. The gate still lists EDIT_NOT_CONFIRMED as a warning, so the loss is silent at the next_action level. The card's evidence says mutants turn tests red; this one does not, and the brief requires the mutants to die.",
   "fix": "Add a case where a reworded (edited, unconfirmed) entry is the earliest waiting item, and assert next_action names it. Also assert for every library case that the set of items next_action may name equals the GET case items with state needs_review and (review_status pending or edit_to_check), computed from the case JSON and not from needs_review_order.",
   "acceptance_test": "Scratch mutant of case_list.py:147 (drop edit_unconfirmed) must turn tests/unit/test_case_list.py red. For the case_lib02 reworded-entry scenario, next_action.item_id equals the edited entry e1 (T-157-r2-probe3.py output must not change to f_r2_1)."},
  {"severity": "minor",
   "title": "HTML-entity-encoded titles are stored verbatim (not refused)",
   "evidence": "Probe T-157-r2-probe.py: POST /api/cases title '&lt;img src=x onerror=alert(1)&gt;Rivera' -> 201, stored name '&lt;img src=x onerror=alert(1)&gt;Rivera'. Numeric '&#60;img&#62;' (validate_title) and double-encoded '&amp;lt;img' also stored verbatim. Code: app/backend/case_list.py:45 checks only literal '<' or '>'. No decode step anywhere; no innerHTML in app/frontend (grep).",
   "why_it_matters": "Inert today: nothing decodes the text and inserts it as markup. The contract says a title is never markup, and an entity-encoded title becomes markup at the first sink that decodes once before inserting. Rated minor, not major, because no current sink does this and the paralegal sees the literal entity text. The rule as written in the card (reject < and >) is met.",
   "fix": "Pick one and write it into api.md line 703: (a) refuse '&' followed by a named or numeric character reference, or (b) state that titles are literal text, entities are shown as typed, and no sink may decode them. Pin the choice in tests.",
   "acceptance_test": "Option (a): POST /api/cases with title '&lt;img&gt;' returns 422 invalid_title. Option (b): the stored value is '&lt;img&gt;' and a test asserts it is unchanged and that api.md documents it."},
  {"severity": "minor",
   "title": "Create silently ignores a non-text title; PATCH refuses the same body with 400",
   "evidence": "app/backend/api.py:248-249 'typed = isinstance(b.get(title), str)' / 'given = b.get(title) if typed else b.get(name)'. Probe T-157-r2-probe.py: POST /api/cases with text and title 5 -> 201, title 'Sablewood Market first-aid log, Mar 9, 2026', name null. PATCH with title 5 -> 400 bad_request (api.py:342-343).",
   "why_it_matters": "A typed value that is not text is dropped while the response says success. The create and PATCH routes disagree on the same input. The honest-failure rule says a refused input should say so.",
   "fix": "On create, if the key title is present and is neither a string nor null, return 400 bad_request, the same as PATCH.",
   "acceptance_test": "POST /api/cases with text and title 5 returns 400 bad_request and creates no case. Add this to tests/unit/test_case_list.py next to the PATCH non-text checks at lines 190-195."},
  {"severity": "minor",
   "title": "PATCH checks the title before the token lookup: unknown token with a bad title returns 422, not 404",
   "evidence": "app/backend/api.py:344 'name = valid_name(b[title])' runs before api.py:347 'get_case(c, token)'. Probe T-157-r2-probe.py: PATCH /api/cases/nope with title '<img ...>' -> 422 invalid_title; with a 121-character title -> 422; with title 'a' -> 404 not_found. memory/contracts/api.md (PATCH sentence, line 703) says 'an unknown token is 404 not_found'.",
   "why_it_matters": "The order is not written down and the doc says 404. No existence leak: a bad title gets 422 whatever the token. Minor, as the brief says.",
   "fix": "Look up the token first (api.py:347 before 344), or add 'checks run in this order: body, token, title' to api.md.",
   "acceptance_test": "A test PATCHes /api/cases/nope with a markup title and asserts the documented status (404 if the token check moves first)."},
  {"severity": "minor",
   "title": "Derived title drops all text after a stray '<' (the doc says brackets are dropped)",
   "evidence": "app/backend/case_list.py:26 _TAG = re.compile(r'<[^<>]*>?') used by plain_title at :54. Probe T-157-r2-probe2.py: plain_title(\"St. Mary's <3 Clinic\") -> \"St. Mary's\"; plain_title('Marrowgate <img src=x onerror=alert(1) ED') -> 'Marrowgate'. memory/contracts/api.md line 703, rule (2): 'its Source line with any tags or angle brackets dropped'.",
   "why_it_matters": "The header label loses words that were in the record. Not a safety issue (the record text is untouched and the title is inert), but the code does more than the documented rule.",
   "fix": "Remove complete <...> pairs only, and drop any remaining lone < or > character without deleting the text after it.",
   "acceptance_test": "plain_title(\"St. Mary's <3 Clinic\") == \"St. Mary's 3 Clinic\", and plain_title('<b>Clinic</b> & Co <') still == 'Clinic & Co' (the existing test at tests/unit/test_case_list.py:345 stays green)."},
  {"severity": "minor",
   "title": "The live-definition test compares the API with the store by identity; a change to the definition passes",
   "evidence": "tests/unit/test_case_list.py:381 'assert demo is (not store.live_enabled())' and :385 'assert got is (store.live_model_available() and not demo)'. The API side is api.py:117 'return store.live_enabled()'. Mutant M (app/backend/store.py:15, drop 'os.environ.get(ENABLE_LIVE) == 1 and'): pytest tests/unit/test_case_list.py -q -> '40 passed in 17.68s' (SURVIVED). Probe T-157-r2-probe2.py with ANTHROPIC_API_KEY set and ENABLE_LIVE unset: baseline health demo_mode True and POST non-recorded text 409 demo_mode_unsupported_input; under mutant M demo_mode False and POST 201. tests/unit/test_api_routes.py:43 and :316 pin demo_mode only with no key set.",
   "why_it_matters": "Sharing the definition holds by construction, which is what the AC asks for. But no test pins the value of the demo gate, so a change to the live definition flips the public demo gate (ADR-006, 'demo mode is the gate') and the suite stays green.",
   "fix": "Add absolute pins next to the parametrized test: ANTHROPIC_API_KEY=k, ENABLE_LIVE unset, LLM_BACKEND=anthropic-api, expecting health demo_mode True and POST of non-recorded text 409; and ENABLE_LIVE=1 with LLM_BACKEND=claude-cli, expecting demo_mode False.",
   "acceptance_test": "Mutant store.py:15 (drop the ENABLE_LIVE check) turns the new absolute-pin test red."},
  {"severity": "nit",
   "title": "Untitled case fallback still in the frontend (carry-over from r1)",
   "evidence": "app/frontend/overview.js:51 'const titleOf = (s) => (... : s.title || ZL.niceName(s.name) || Untitled case);' (double quotes shown as single). Unreachable while the backend always sends a title.",
   "why_it_matters": "Dead text, but it is the string the AC bans, and a future null from the backend would show it.",
   "fix": "Route to the frontend card: drop the fallback and use the backend title only.",
   "acceptance_test": "grep -rn 'Untitled case' app/frontend returns nothing."}
 ],
 "whats_right": [
  "Refusal happens before any write and before the PDF is read: a refused title leaves no case behind (probe T-157-r2-probe.py; the count assertion at tests/unit/test_case_list.py:306-308).",
  "Control, zero-width and bidi characters are removed before the markup check, so '<' followed by U+200B, NUL, U+202E or VT is still refused (probe T-157-r2-probe4.py).",
  "The blocker and timeline rules are now pinned: mutants waiting[-1], first=None, the seq/rank swap, undated-first, the NOTHING_ACCEPTED yield and blockers-behind-waiting all turn tests red (12 of 14 mutants killed; file T-157-r2-mutants.out)."
 ],
 "questions_for_chris": [
  "Entity-encoded titles (&lt;img&gt;): should they be refused with 422 like '<' and '>', or stored as literal text and documented in api.md as never decoded? Finding 2 waits on this choice.",
  "Create with a non-text title (title 5): 400 like PATCH, or ignored as today? Finding 3 waits on this choice."
 ]}
```
