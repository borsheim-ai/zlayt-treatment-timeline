# Subagent: Backend: T-083 billing ledgers (Backend: T-083 billing ledgers)

Source: `agent-ac26b498a80d3ff30.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:16:13.601Z

You own board card T-083 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-083` and read D-042 in memory/ORCHESTRATOR_DECISIONS.md, research/record-formats.md (itemized ledger, CMS-1500, UB-04 and EOB traps: no-decimal amounts, a rate on the charge line), app/backend/amounts.py and app/backend/totals.py.

Build billing analysis on itemized ledgers, in code only. Each ledger line parses to billed, adjustment, paid and balance amounts, and every figure is cited to its line (a verbatim excerpt). Total by provider; list LOP and lien amounts separately; total nothing that isn't stated (D-019). Rates are never charges. Put it in a new module (e.g. app/backend/billing.py) and add an API route. Add the contract to memory/contracts/api.md, and write unit tests on synthetic ledgers that include the research traps. Note on the card what the UI needs, so a frontend card can follow.

**Shared rules (8 workers are running in parallel):**
- Put the logic in new modules. In shared files (api.py, pipeline.py, api.md), make the smallest possible edit, re-read the file right before editing, and never reformat.
- Don't touch flags.py or judges.py (T-094 is in them), evals/library, or evals/run.py.
- Commit only your own hunks. Use a temp index (`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD`, then add your paths or patches) when a shared file has other workers' edits; otherwise `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".
- Run `.venv/bin/python -m pytest -q tests/unit`. If a failure is in someone else's area, name it and move on.
- Then `board.py ac`, the handoff, and `move <card> in_review --agent backend`. Reply in 2 lines.

### User / tool · 2026-11-02T04:16:13.606Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:31.545Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-083 && grep -n \"D-042\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60 && grep -n \"D-019\" -A12 memory/ORCHESTRATOR_DECISIONS.md | head -30"
}
````

### User / tool · 2026-11-02T04:16:31.699Z

**tool result**
````
---
id: "T-083"
title: "Billing analysis on itemized ledgers: billed, adjusted, paid, LOP/lien (code only, cited)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:16:04Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Itemized ledger lines parse to billed/adjustment/paid/balance with each figure cited to its line; totals by provider; LOP/lien amounts listed separately; nothing totaled that is not stated; unit tests on synthetic ledgers", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed

## Handoff (filled when moving to in_review)

50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
52-| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
53-| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
27:| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28-| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29-| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30-| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31-| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
32-| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
33-| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
34-| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
35-| D-027 | Two-digit years are never guessed: `03-17-98` is `date_ambiguous` with candidates (1998, 2098) and excluded from gap math until confirmed. Text outside recognised record blocks is never dropped: it becomes an 'unsplit text' record flagged for the paralegal. | 'Say so instead of guessing' (spec); silent drops lose facts. | T-032 staff review |
36-| D-028 | Judges return a verdict enum plus a `reason_code` from a closed list (e.g. ADDS_DIAGNOSIS, ADDS_SEVERITY, ADDS_CAUSATION, DROPS_QUALIFIER, NUMBER_MISMATCH, OTHER_UNSUPPORTED); no free-text reason. The UI's Why? renders the code through a code template. | Model prose must not reach the attorney or the UI (consistent with D-007); ADR-008.5 enum-only. | T-035 staff review (Chris Q answered by orchestrator) |
37-| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
38-| D-030 | Flag evidence is the **verbatim phrase span** that triggered the flag (lexicon match or LLM-returned span), e.g. "Findings may represent degenerative change", "New onset pain" — not the whole sentence. Entry excerpts stay whole sentences (D-021). Internal notes quote flag spans; the golden notes block is the authority. | Precise flag quotes; matches the hand-written golden; entries keep context. | T-051/backend-4 |
39-| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:32.355Z

**tool call — Bash**
````
{
 "command": "wc -l research/record-formats.md app/backend/amounts.py app/backend/totals.py app/backend/api.py memory/contracts/api.md && cat app/backend/amounts.py app/backend/totals.py"
}
````

### User / tool · 2026-11-02T04:16:32.445Z

**tool result**
````
    1080 research/record-formats.md
     155 app/backend/amounts.py
      32 app/backend/totals.py
     569 app/backend/api.py
     606 memory/contracts/api.md
    2442 total
"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import re

from app.backend import injection, lexicon

# '$' + a whole numeric token (extra decimals are kept so to_cents can refuse them: never truncated).
# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


def find_amounts(excerpt: str) -> list:
    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
    out = []
    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
    for m in _AMT.finditer(excerpt or ""):
        figure = m.group(1)
        if not any(c.isdigit() for c in figure):
            continue
        injected = any(s <= m.start() and m.end() <= e for s, e in spans)   # a figure inside instruction-like text has no trusted value (D-005)
        out.append({"raw": m.group(0), "cents": None if injected else to_cents(figure), "start": m.start(), "end": m.end()})
    return out


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
    return " ".join((clauses[-1] if clauses else "").split()[-6:])


def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
    needs it to be a billing document."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
        return "damages"
    if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
        return "charge"
    if _CHARGE_END.search(label):
        return "charge"
    return "unclear"


def _is_billing_source(source: str) -> bool:
    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))


def damages_mentions(excerpt: str) -> list:
    """Work-loss and similar mentions with no dollar value (lexicon `damages`): [{raw, cents: None, cls: 'damages', start, end}]."""
    out = []
    for e in lexicon.code_list("damages"):
        for m in e["regex"].finditer(excerpt or ""):
            end = m.end()
            t = _WORK_TAIL.match(excerpt, end)
            if t:
                end = t.end()
            if not any(o["start"] < end and m.start() < o["end"] for o in out):
                out.append({"raw": excerpt[m.start():end], "cents": None, "cls": "damages", "start": m.start(), "end": end})
    return sorted(out, key=lambda o: o["start"])


def _norm(s):
    return " ".join((s or "").split()).casefold()


def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
    """Same date + normalised provider + record text (when given) + class + value merges into one amount citing every record (R-CH-6). Unreadable values never merge."""
    out, index = [], {}
    for a in amounts:
        nos = sorted(a.get("record_nos") or [a["record_no"]])
        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
        if set(nos) & set(separate):        # records the paralegal declared not-a-duplicate never merge (D-031)
            key = None
        if key in index:
            m = out[index[key]]
            m["record_nos"] = sorted(set(m["record_nos"]) | set(nos))
            m["duplicate_note"] = "Same amount, date and provider appears in records " + ", ".join(str(n) for n in m["record_nos"]) + "."
            continue
        row = {**a, "record_nos": nos, "duplicate_note": None}
        if key is not None:
            index[key] = len(out)
        out.append(row)
    return out


def extract_amounts(records: list, separate=frozenset()) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
    `separate` = record numbers the paralegal said are not duplicates: their amounts never merge with another record's and get ids ax<n>_<k>."""
    rows = []
    for r in records:
        if r.get("duplicate_of"):
            continue
        base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
                 for a in find_amounts(r["excerpt"])] + damages_mentions(r["excerpt"])
        for a in sorted(found, key=lambda x: x["start"]):
            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                         "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "injection": bool(r.get("injection_tag"))})
    out = dedupe_amounts(rows, separate)
    i, k = 0, {}
    for a in out:
        if a["record_no"] in separate:         # stable ids that do not shift the other amounts: a rerun lands on the same rows
            k[a["record_no"]] = k.get(a["record_no"], 0) + 1
            a["id"] = f"ax{a['record_no']}_{k[a['record_no']]}"
        else:
            i += 1
            a["id"] = f"a{i}"
    return out


_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
_VISIT = re.compile(r"\bvisit\s+(\d+)\b", re.IGNORECASE)


def _prefix(source):
    return _norm((source or "").split(",")[0])


def rate_note(records: list, record_no: int) -> dict:
    """Numbers for the rate note, code-derived (T-033 AC7): planned N from 'Plan of care: N visits' in a record with the same provider
    prefix (header label before the first comma); last_visit M = highest 'visit M' in such a header label. None when not found."""
    me = next(r for r in records if r["n"] == record_no)
    same = [r for r in records if _prefix(r.get("source")) == _prefix(me.get("source"))]
    planned = next((int(m.group(1)) for r in same for m in [_PLAN.search(r.get("excerpt") or "")] if m), None)
    visits = [int(m.group(1)) for r in same for m in [_VISIT.search(r.get("source") or "")] if m]
    return {"planned": planned, "last_visit": max(visits) if visits else None}
"""Running total of ACCEPTED charges, computed on read and never stored (R-CH-3, D-004, D-019, ADR-011). Integer cents only.
Only class `charge` with review_status accepted/edited adds. Pending charges are 'detected, not a total'. No PT total is ever derived from a rate."""

COUNTED = ("accepted", "edited")
LETTER_PREFIX = "Billed charges stated in these records: "
UI_PREFIX = "Accepted charges: "
DETECTED_LABEL = "Detected, not yet accepted (not a total)"


def usd(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


def totals(amounts: list) -> dict:
    accepted = pending = 0
    unclear, found = [], 0
    for a in amounts:
        cls, cents, st = a.get("cls"), a.get("cents"), a.get("review_status", "pending")
        if cls != "damages":
            found += 1
        if cls == "charge" and cents is not None:
            if st in COUNTED:
                accepted += cents
            elif st == "pending":
                pending += cents
        elif st != "dismissed" and cls != "damages":
            unclear.append(a)
    status = "none_found" if not found else ("partial_unclear" if unclear else "complete")
    return {"accepted_cents": accepted, "detected_pending_cents": pending, "detected_label": DETECTED_LABEL,
            "unclear_items": unclear, "amounts_found": found, "status": status,
            "letter_line": LETTER_PREFIX + usd(accepted) if accepted else None,
            "ui_line": UI_PREFIX + usd(accepted) if accepted else "No accepted charges yet."}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:35.006Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"ledger\\|CMS-1500\\|UB-04\\|EOB\\|lien\\|LOP\" research/record-formats.md | head -80"
}
````

### User / tool · 2026-11-02T04:16:35.097Z

**tool result**
````
27:| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter "Re:" line, intake form, narrative letter "Re:" line | It is the accident date, not a visit. Treating it as an encounter creates a phantom visit and hides the real first-treatment gap. |
28:| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line (unverified convention, see section 23), radiology "Signed", op-note "D:/T:" dictation and transcription stamps |
30:| Statement / print / fax date | Ledger "Statement date", pharmacy "Printed on", fax header line at the top of every page | Same date on every page of a records production; a naive extractor dates every entry to the production date. |
34:| Date ranges | CMS-1500 24A From/To with 24G units, UB-04 FL 6 statement period, PT "Visits 1 to 12" summary | One line can stand for many consecutive days (NUCC allows grouping only on consecutive days with identical code, charge and provider; days must equal units). |
44:| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
49:| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |
51:**Number formats.** CMS-1500 boxes use no dollar sign, no comma and no decimal point, with cents in a separate box to the right of a vertical
52:line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
62:An ED visit produces a facility bill (UB-04), an emergency-physician bill (CMS-1500), and a radiologist bill (CMS-1500 with modifier 26) for
80:the UB-04 and CMS-1500.
109:MDM: Strain vs radiculopathy. Toradol 30 mg IM. Reassessed 01:40, pain 5/10.
127:on the note; they appear on the CMS-1500 or ledger as units times a fee.
205:Visits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,
262:**Typical wording.** "PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy secondary to C5-6 disc protrusion." "PROCEDURE: C5-6 anterior cervical
283:PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy, C5-6 disc protrusion.
337:## 8. CMS-1500 (02/12) professional claim
399:## 9. UB-04 (CMS-1450) institutional claim
426:- Rhode Island EOHHS, *UB-04 Instructions*: https://eohhs.ri.gov/sites/g/files/xkgbur226/files/2021-03/ub04_instructions.pdf — **opened** (text extracted). Takeaways: FL 4 four-digit with leading zero; FL 6 MMDDYY; FL 42 enter "0001" after last revenue code for the total in column 47 (paper only); FL 47 per-line total plus grand total; FL 48 amount not covered by primary payer.
427:- NUBC, *Official UB-04 Data Specifications Manual 2024* (table of contents; FL 47 p.180, FL 48 p.181): https://www.nubc.org/system/files/media/file/2024/04/TOC%20FOR%20NUBC%20SITE%202024%20UB04%20Manual.pdf — search summary; the full manual is licensed.
434:SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
452:SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
473:## 10. Itemized provider ledger / statement
477:payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").
480:and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
501:Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
513:(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
514:CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
519:## 11. Explanation of Benefits (EOB) / remittance
530:- The EOB's "amount billed" restates the provider's charge; counting both the bill and the EOB double counts.
534:- Health-plan EOBs in a PI file often signal a subrogation lien by the health plan.
537:- Noridian JF-A, *MSP Calculation Examples on EOBs*: https://med.noridianmedicare.com/web/jfa/topics/msp/calculation-examples-eob — **opened**. Takeaway: billed minus total CARC amount equals allowed; allowed minus paid equals patient responsibility; examples with CARC CO-16 and a network discount.
556:## 12. Letter of protection (LOP) and lien letters
558:**Fields.** Law-firm letterhead; letter date; addressee (provider billing office); "Re:" block with client name, DOB, date of injury, sometimes
560:settlement or judgment; statement that the client remains responsible if the recovery is insufficient; request for records, itemized bill
561:and §18.001 affidavit; attorney signature; client acknowledgement and signature. Related documents: provider-side lien notice or
562:"Assignment and Authorization" signed by the patient at intake; hospital lien notice; reduction letters ("accept $X in full satisfaction").
565:from any recovery." "This letter does not relieve our client of responsibility for the balance." "Please forward complete records and an
566:itemized statement of charges." Provider intake LOPs add: the provider will not send the account to collections while the claim is pending,
567:a continuing lien on any recovery, a direction to pay, and duties to notify the provider before funds are disbursed.
570:- The LOP is not a medical record: its accident narrative is the attorney's, and its dates (letter date, injury date) are not encounters.
571:- Amounts in an LOP or lien notice ("current balance $4,860.00") are asserted totals without dates of service; never charges (D-019).
573:- Sources disagree on whether "LOP" and "lien" are interchangeable; the tool should keep the document's own words.
576:- Jotform HIPAA intake packet with an embedded LOP (chiropractic, auto/slip-and-fall): https://hipaa.jotform.com/221364153684052 — **opened**. Takeaway: patient signs; provider defers payment and collections; direction to pay from settlement after fees and costs; continuing lien; patient remains responsible for any shortfall; notice duties before disbursement.
577:- ChartRequest, *Letters of Protection and Medical Liens*: https://www.chartrequest.com/articles/letters-of-protection-medical-records — search summary; argues LOP and lien are distinct.
578:- D Law Group, *What is a Letter of Protection or Personal Injury Lien?*: https://dlawgroup.com/letter-of-protection-personal-injury-lien/ — search summary; LOP can operate as a contract; patient owes the balance if the case is lost.
579:- Miller & Zois forms library (sample assignment/LOP and hold-harmless letters): https://www.millerandzois.com/professional-attorney-information-center/forms-and-letters-for-personal-injury-lawyers/ — search result, not opened.
580:- Assumption: Texas hospital liens (Property Code ch. 55) produce a separate filed notice; I did not open the statute for this card.
588:Re: Our client Delphine Okonkwo-Vale (SYNTHETIC); Date of injury 05/14/2026
589:This firm represents the above client for injuries from a motor vehicle collision. We ask
592:relieve our client of responsibility for the balance. Please send complete records and an
656:health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).
667:| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
852:(The figures match the ledger in section 10: charges 445.00, adjustment 45.00, payments 0.00, balance 400.00. Page 3 is a duplicate of the
892:on 05/14/2026 and developed neck pain and right hand tingling the same night.
893:Diagnoses: cervical sprain (S13.4XXA); cervical radiculopathy (M54.12).
901:a charge. July 20, 2026 is the letter date. The diagnoses match the CMS-1500 in section 8.)
912:HPI." "MRI C-spine 06/18/2026 reviewed: C5-6 protrusion with R foraminal narrowing." "A/P: 1. Cervical radiculopathy, R C6. Discussed
940:A/P: Cervical radiculopathy, R C6. Recommend C5-6 ACDF. Estimated surgeon fee $14,500.00.
1006:| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts as implied cents; line sum vs Item 28 compared; days = units checked |
1007:| UB-04 | 0001 total; FL 44 rate on the charge line; creation date; occurrence codes 01-06 | Total line not summed; rate not a charge (D-042 guard); any accident code = accident date |
1008:| Ledger | Running balance; voids; balance forward; fee schedule | Only dated charge lines counted; voids netted in code |
1009:| EOB | Double count of billed; CO/PR; mismatch with ledger | EOB amounts to notes, never added to charges; mismatch flagged |
1010:| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |
1022:1. *ER-only then gap*: EMS report + ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + ambulance invoice + fax headers.
1023:2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR
1024:   versions) + ledger with a void and a courtesy adjustment + narrative letter + §18.001 affidavit with a duplicate attached statement.
1025:3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate
1026:   ledger-vs-EOB mismatch.
1028:   assistant/anesthesia/facility bills on one date + inpatient UB-04 with a room-rate line.
1029:5. *Spanish-speaking client*: Spanish clinic note with a day-first date whose parts are both 12 or less + rate and charge on the same page +
1040:| 3 | PT "Visit 7 of 24" on 06/10 but the ledger shows only the eval and 06/10 | Fixed: Visit 2 of 12 | None |
1041:| 4 | Ledger shows no payments; EOB for the same DOS shows plan paid 16.00 and CO reductions | DELIBERATE | Billing analysis cites both and flags the mismatch; never picks paid vs incurred |
1044:| 7 | CMS-1500 line grouped 06/01-06/05 (5 days) with 3 units; travel card had non-consecutive dates | Fixed: grouped lines 06/01-06/03 = 3 days = 3 units; travel card marks match | Code checks days = units |
1047:| 10 | §18.001 affidavit totals vs ledger (new in round 2) | Consistent: 445.00 / 0.00 / 400.00 | Attached statement deduped against section 10 |
1048:| 11 | Narrative letter "since 05/29/2026" and diagnoses vs chiro records and CMS-1500 (new in round 2) | Consistent | Letter cited as the letter; no new encounter |
1057:  NUCC 1500 manual, RI UB-04 instructions, HL7 NUBC occurrence-code list, Noridian chiro, EOB and ambulance-mileage pages, CMS bill guide,
1059:  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.
1061:- **UB-04 specifics.** FL 44 accommodation-rate use and the creation date on line 23 are prior knowledge that the T-078 reviewer also
1065:- **Payer variation.** CMS-1500, UB-04 and ambulance rules here are NUCC/NUBC, CMS and one Medicaid guide; commercial and auto carriers vary.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:35.488Z

**tool call — Bash**
````
{
 "command": "grep -n \"^@app\\|^def \\|^from\\|^import\\|router\\|APIRouter\" app/backend/api.py | head -80; tail -40 memory/contracts/api.md; ls tests/unit | head -50; ls tests/fixtures | head"
}
````

### User / tool · 2026-11-02T04:16:35.586Z

**tool result**
````
6:import hashlib
7:import ipaddress
8:import asyncio
9:import json
10:import logging
11:import os
12:import pathlib
13:import threading
14:import time
16:from fastapi import FastAPI, Request
17:from fastapi.exceptions import RequestValidationError
18:from fastapi.responses import JSONResponse, Response
19:from starlette.exceptions import HTTPException as StarletteHTTPException
21:from starlette.concurrency import run_in_threadpool
23:from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
24:from app.db import db as DB
52:def digest(text: str) -> str:
56:def recorded_hashes() -> set:
60:def library_cases() -> list:
77:def local_mode() -> bool:
81:def is_loopback_peer(request) -> bool:
91:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
```
`verdict` is the ladder vocabulary (`supported|partially|unsupported|disagrees|unsure|unavailable`). Frontend: after the call, refetch `/trace` (and the case view, since `state` can change).

## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## DELETE /api/cases/{token}
`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).

---

## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
| Code | State | Meaning |
|---|---|---|
| `GROUNDING_EXCERPT_NOT_VERBATIM` | rejected | model's excerpt is not word for word in the record |
| `GROUNDING_AMOUNT_NOT_IN_TEXT` | rejected | model reported an amount the record does not contain |
| `SCHEMA_INVALID` | rejected | model output failed schema validation after retries |
| `SUMMARY_TOKEN_NOT_IN_EXCERPT` | needs_review | a number, date, dollar figure or left/right/no/not/without in the summary (or an edit) is not in the quote |
| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
| `EXCERPT_OMITS_QUALIFIER` | needs_review | the record has a hedge sentence the excerpt leaves out |
| `EXCERPT_NOT_WHOLE_SENTENCE` | needs_review | the excerpt starts or ends mid-sentence |
| `HIGHLIGHT_NOT_FOUND` | needs_review | the quote cannot be located in the raw text for highlighting |
| `JUDGE_PARTIAL` / `JUDGE_UNSUPPORTED` | needs_review | judge 1 found the summary partly or not supported |
| `JUDGE_DISAGREES` / `JUDGE_UNSURE` | needs_review | judge 2, 3 or 4 disagreed or could not decide |
| `JUDGE_UNAVAILABLE` | needs_review | the judge call failed or timed out, or (always in demo mode) an edit has no recorded judge answer |
| `FIXTURE_MISS` | needs_review | the demo has no recorded model answer for this call; never retried |
| `DATE_AMBIGUOUS` / `DATE_MISSING` | needs_review | date has two readings or is absent; excluded from gap math until confirmed |
| `ENDPOINT_NOT_VERIFIED` | needs_review | a gap's span could contain an unconfirmed date |
| `AMOUNT_RATE_NOT_TOTALED` | needs_review | a rate, not a charge |
| `AMOUNT_ESTIMATE` / `AMOUNT_DAMAGES` / `AMOUNT_UNCLEAR` | needs_review | estimate, non-bill figure, or unreadable/unlabelled value |
| `LEXICON_ONLY` / `LLM_ONLY` | needs_review | phrase list and model disagree on a flag |
| `SPLIT_AMBIGUOUS` | needs_review | record boundaries uncertain |
| `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |
| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_backend_no_speaker_label.py
test_boundaries.py
test_case_extras.py
test_confidence.py
test_conflict_candidates.py
test_conflicts.py
test_date_unconfirmed.py
test_dates.py
test_db.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_frontend_no_speaker_label.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_ingest.py
test_injection.py
test_judges.py
test_library_denylist.py
test_manual_and_split.py
test_multicase.py
test_narrative.py
test_pdf_upload.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_split_llm.py
test_t033_backend.py
test_t037_backend.py
llm
make_curated.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:37.789Z

**tool call — Bash**
````
{
 "command": "sed -n 337,400p research/record-formats.md; sed -n 473,555p research/record-formats.md; sed -n 655,680p research/record-formats.md"
}
````

### User / tool · 2026-11-02T04:16:37.884Z

**tool result**
````
## 8. CMS-1500 (02/12) professional claim

**Fields (NUCC numbering).** 1a insured ID; 2 patient name; 3 DOB (8-digit) and sex; 10a-c condition related to employment / **auto accident
(with state)** / other accident; 11 insured's policy; 14 date of current illness or injury with qualifier (431 onset); 17 referring provider;
21 ICD indicator (0 = ICD-10) and diagnoses A-L; 24A dates of service From/To; 24B place of service; 24D CPT/HCPCS with up to four modifiers;
24E diagnosis pointer (letters); 24F $charges; 24G days or units; 24J rendering provider NPI; 25 federal tax ID; 28 total charge; 29 amount
paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.

**Typical wording and number format.** 24F "is the total billed amount for each service line": dollars right-justified left of a vertical
line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.

**Extraction traps.**
- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
- 24A From/To with 24G = 10 means ten consecutive days on one line; one line is not one visit (NUCC: days must equal units).
- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
- Item 14 is the injury/onset date and Item 31 is the signature date: neither is a service date.
- Item 28 can disagree with the sum of lines (data entry), or a claim may run to a second page with its own lines; sum lines in code and
  compare to Item 28 rather than trusting either.
- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.

**Sources.**
- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf — **opened** (text extracted locally). Takeaways: Items 14, 24A, 24F, 24G, 28, 29, 30 as stated above. Newer manual versions may exist (NUCC updates each July); field layout of the 02/12 form is unchanged.
- CMS MLN web-based training on the 1500 (lesson 5): https://cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson05/02/index.html — search result, not opened.

**Specimen (SYNTHETIC), clean boxed form** (as printed; money boxes have no decimal point, cents sit right of the bar):
```
SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
2. PATIENT'S NAME  OKONKWO-VALE, DELPHINE (SYNTHETIC)     3. DOB 03 | 09 | 1991  F
10b. AUTO ACCIDENT?  [X] YES  [ ] NO   PLACE (State) TX
14. DATE OF CURRENT ILLNESS  05 | 14 | 26   QUAL 431
21. ICD Ind 0   A. S13.4XXA   B. M54.12
24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
31. SIGNATURE  Dr. Corvin Ashdown, DC (SYNTHETIC)  DATE 06/30/26
33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142
```
(Lines 4-5 group 06/01 to 06/03: three consecutive days, 3 units, each matching the travel card's ES and H/C marks on all three days in
section 4; $30.00 and $15.00 per day. Lines 1-3 bill the same code one line per day, which NUCC also allows. MOD is blank; AB and A are
diagnosis pointers in 24E. Line sum 85 + 85 + 85 + 90 + 45 = 390 = Item 28. Item 14 is the injury date and Item 31 the signature date;
neither is a visit.)

**Specimen (SYNTHETIC), the same claim as OCR text** (what a scanned copy returns; truth beside each money string):
```
SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001         <- truth 85.00 (not 8,500.00)
    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001        <- truth 85.00 (bar dropped, space kept)
    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001        <- truth 85.00; O for 0 in the date
    060126 060326 11 97014 A 9000 3 SYN-NPI-0001          <- truth 90.00 (not 9,000.00)
    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001         <- truth 45.00; O for 0 in the cents
28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00             <- truth 390.00 and 0.00
```
(Expected tool behavior: money in 24F and Items 28-29 is parsed as implied-cents in code; the line sum is compared with Item 28 in code;
every OCR-derived amount and date goes to review with the page image. A parser that reads `8500` as dollars bills $8,500 per adjustment.)

---

## 9. UB-04 (CMS-1450) institutional claim

## 10. Itemized provider ledger / statement

**Fields.** Provider name and address; patient and account number; statement date; prior balance / balance forward; per line: date of
service, posting date, CPT or internal code, description, charge, payment, adjustment, running balance; totals block (total charges, total
payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").

**Typical wording.** CMS's consumer guide names the parts as total charges, allowed amount, adjustments, insurance payment, patient payment,
and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
parentheses or with a trailing minus, "Pmt - Ck #SYN-1043". Hospital consumer statements often show only a total; the itemized version must be
requested.

**Extraction traps.**
- Running balance is cumulative; summing it multiplies the bill.
- Balance forward from a prior statement re-counts earlier charges if two statements are both in the packet.
- Posting date versus date of service: a charge posted 06/30 for a 06/03 visit.
- Reversals ("Void", "Reverse chg") paired with a re-bill on a later line.
- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
- An attorney reduction recorded as an adjustment after settlement talks is a negotiated number, not a billed charge.

**Sources.**
- CMS, *How to read your medical bill*: https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/medical-bill-guides-resources/how-read-your-medical-bill — **opened**. Takeaway: standard parts are total charges, allowed amount, adjustments, insurance payment, patient payment, balance due.
- Resolve Medical Bills, *Itemized Hospital Bills*: https://www.resolvemedicalbills.com/guides/itemized-hospital-bill — search summary; itemized bill is sent only on request and lists dates, codes and per-service prices.
- Texas CPRC §18.001 (affidavit must include an itemized statement of the service and charge): https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm — search summary; see also research/texas-pi-notes.md.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.
```
(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
review; the tool never picks paid or incurred. The $65.00 fee-schedule line has no date of service: a rate, not a charge.)

---

## 11. Explanation of Benefits (EOB) / remittance

**Fields.** "THIS IS NOT A BILL"; member name and ID; claim number; provider; processed date; per service: date of service, service
description or code, amount billed, network discount / not covered, allowed amount, deductible, copay, coinsurance, plan paid, patient
responsibility ("You may owe"); CARC/RARC codes with group code (CO contractual obligation, PR patient responsibility, OA other).

**Typical wording.** "Amount billed $410.00 - Network discount $162.40 = Allowed $247.60." "Deductible applied $100.00; Coinsurance 20%
$29.52; Plan paid $118.08; You may owe $129.52." "CO-45: charge exceeds fee schedule/maximum allowable." "PR-1 deductible, PR-2 coinsurance,
PR-3 copay."

**Extraction traps.**
- The EOB's "amount billed" restates the provider's charge; counting both the bill and the EOB double counts.
- The processed/paid date is not a service date.
- "You may owe" is not what the patient paid; for Texas paid-or-incurred analysis (out of scope for the tool) the numbers matter, so keep them in notes with citations.
- Group code decides who owes: CO amounts are written off by a contracted provider, PR amounts are the patient's.
- Health-plan EOBs in a PI file often signal a subrogation lien by the health plan.

**Sources.**
- Noridian JF-A, *MSP Calculation Examples on EOBs*: https://med.noridianmedicare.com/web/jfa/topics/msp/calculation-examples-eob — **opened**. Takeaway: billed minus total CARC amount equals allowed; allowed minus paid equals patient responsibility; examples with CARC CO-16 and a network discount.
- D3RX glossary, *CO (Contractual Obligation)*: https://d3rx.com/glossary/co-contractual-obligation — search summary; billed minus allowed is a contractual write-off the participating provider cannot balance-bill.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - THIS IS NOT A BILL
Quoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
CO-97: payment included in allowance for another service.
```

---

explanation lines; current medications; employer and work status; "Who referred you?" (often an attorney); attorney name; insurance (auto,
health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).

**Typical wording.** Handwriting, abbreviations and the patient's own words: "rear ended at light, neck + back hurt", "no prior", "Dr. told
me to come", "pain 7-8". Stamps: "RECEIVED", "SCANNED", Bates numbers; fax header on every page.

**OCR failure modes to reproduce.**
| Failure | Example (truth → OCR) | Consequence |
|---|---|---|
| Checkbox read as character or dropped | `[X] No` → `IX] No` or `No`; `[ ] Yes [X] No` → `Yes No` | Prior-injury answer lost or flipped - high stakes for pre-existing flags |
| Glyph confusion | `0/O`, `1/l/I/7`, `5/S`, `8/B`, `2/Z` | `05/14/26` → `O5/l4/26`; `$150` → `$I50` |
| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
| Circled number | Pain scale `0 1 2 3 4 5 6 7 8 9 10` with 7 circled → all digits | Pain score lost |
| Strike-through and correction | `6/12` struck, `6/15` written above | Both dates extracted |
| Two-column / form-grid reading order | Left and right columns interleaved | Answers attached to the wrong question |
| Fax header and stamps | `11/03/2026 09:14 FROM: 555-0199 P.3/14` | Fax date read as a record date |
| Skew, blur, shadow, bleed-through | Phone photo of a form | Character error rate rises; Tesseract was weakest on blur and shadow in one study |
| Hidden or layered text in PDFs | Searchable PDF with an invisible text layer that differs from the image | Extracted text not visible to the human reviewer (D-042 hidden-text detection) |

**Sources.**
- *Compact Multimodal Language Models as Robust OCR Alternatives for Noisy Textual Clinical Reports* (arXiv 2511.13523): https://arxiv.org/html/2511.13523v1 — **opened**. Takeaway: on smartphone photos of printed clinical reports, Tesseract scored CER 0.189, WER 0.276 and numeric accuracy 0.756, worse than neural pipelines and small multimodal models; Tesseract struggled most with blur and shadows. (Cite by arXiv number; authors not recorded here.)
- Tesseract OCR mailing list, thread on reading "X" checkboxes: https://groups.google.com/g/tesseract-ocr/c/r9mVUg76iE0 — search summary; out-of-the-box quality is medium; form jargon needs training; one user got better results at 150 dpi than 600 dpi.
- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel — search summary (vendor); generic OCR has no character for a tick and skips or garbles it.
- Assumption: glyph confusions in the table are the standard OCR confusion set; I found no Tesseract-specific measurement of them.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:38.113Z

**tool call — Bash**
````
{
 "command": "grep -n \"narrative\\|case_extras\\|@app\\.\\(get\\|post\\)\" app/backend/api.py | head -60; sed -n 1,60p app/backend/case_extras.py"
}
````

### User / tool · 2026-11-02T04:16:38.209Z

**tool result**
````
23:from app.backend import case_extras, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
210:    @app.get("/api/health")
216:    @app.get("/api/cases")
226:    @app.get("/api/library")
232:    @app.post("/api/cases", status_code=201)
248:    @app.post("/api/cases/pdf", status_code=201)
304:    @app.get("/api/cases/{token}")
337:    @app.post("/api/cases/{token}/run", status_code=202)
360:    @app.post("/api/cases/{token}/rejudge")
382:    @app.get("/api/cases/{token}/status")
401:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
413:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
424:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
437:    @app.get("/api/cases/{token}/narrative")
438:    def narrative_get(token: str):
442:            return {"narrative": narrative.get(c, token)}
446:    @app.post("/api/cases/{token}/narrative")
447:    def narrative_draft(token: str):
452:            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
455:            return {"narrative": nar}
459:    @app.post("/api/cases/{token}/narrative/review")
460:    async def narrative_review(token: str, request: Request):
466:                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
474:    @app.get("/api/cases/{token}/items/{item_id}")
486:    @app.post("/api/cases/{token}/items/{item_id}/review")
496:    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
498:    @app.get("/api/cases/{token}/export")
525:    @app.get("/api/cases/{token}/items/{item_id}/trace")
538:    @app.get("/api/cases/{token}/trace")
547:    @app.get("/api/cases/{token}/judges")
556:    @app.get("/api/cases/{token}/audit")
"""Batch accept of verified entries and per-case export config (D-031). Routes are added by api.create_app via add_routes().
Code only: nothing here asks a model anything, and the only review_status writer used is DB.apply_review (one event per item)."""
import re
import threading

from fastapi import Request

from app.backend import present, review
from app.db import db as DB

MAX_BATCH = 200
_LOCK = threading.Lock()
_LABEL = re.compile(r"[A-Za-z0-9 ._-]{1,20}")
EXPORT_KEYS = ("exhibit", "bates_prefix", "bates_start")


# ------------------------------------------------------------------ batch review
class BatchRefused(Exception):
    def __init__(self, rejected):
        super().__init__("invalid_batch")
        self.rejected = rejected


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad = []
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad


def apply_batch(conn, case_id, body, now):
    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("bad_request")
    with _LOCK:
        bad = _check(conn, case_id, ids, action)
        if bad:
            raise BatchRefused(bad)
        done = []
        try:
            for i in ids:
                review.batch_apply(conn, case_id, i, action, now)
                done.append(i)
        except Exception:
            for i in reversed(done):          # compensate: each undo is itself an audited event
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:40.249Z

**tool call — Bash**
````
{
 "command": "sed -n 150,210p app/backend/api.py; sed -n 434,475p app/backend/api.py; sed -n 60,130p app/backend/case_extras.py; grep -n \"def \" app/db/db.py | head -60; git status --short | head -30"
}
````

### User / tool · 2026-11-02T04:16:40.376Z

**tool result**
````
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)

    @app.exception_handler(RequestValidationError)
    async def _validation(_, e):
        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)

    @app.middleware("http")
    async def _headers(request, call_next):
        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
            purged["at"] = time.time()
            c = conn()
            try:
                DB.purge_expired(c, time.time())
            finally:
                c.close()
        try:
            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
            else:
                resp = await call_next(request)
        except Exception as e:                                                          # last line of defence: standard JSON, no detail
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp

    async def body_of(request: Request) -> dict:
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > MAX_BODY_BYTES:
            raise ApiError(413, "input_too_large", "Input is too large.")
        raw = b""
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > MAX_BODY_BYTES:
                raise ApiError(413, "input_too_large", "Input is too large.")
        if not raw:
            return {}
        try:
            b = json.loads(raw)
        except ValueError:
            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
        if not isinstance(b, dict):
            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
        return b

    # -------------------------------------------------- routes
    @app.get("/api/health")
        finally:
            c.close()

    @app.get("/api/cases/{token}/narrative")
    def narrative_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return {"narrative": narrative.get(c, token)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/narrative")
    def narrative_draft(token: str):
        """D-031: draft the firm-voice paragraph from ACCEPTED entries (each sentence code-checked and judged; failures removed with a reason)."""
        c = conn()
        try:
            get_case(c, token)
            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
            if nar.get("error") == "NO_ACCEPTED_ENTRIES":
                raise ApiError(400, "bad_request", "Accept at least one entry first; the paragraph is written from accepted entries only.")
            return {"narrative": nar}
        finally:
            c.close()

    @app.post("/api/cases/{token}/narrative/review")
    async def narrative_review(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return {"narrative": narrative.review(c, token, b.get("action"), now=time.time())}
            except KeyError:
                raise ApiError(404, "not_found", "No draft paragraph yet.") from None
            except ValueError:
                raise ApiError(422, "invalid_edit", "That action is not allowed.") from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}")
    def item(token: str, item_id: str):
            for i in reversed(done):          # compensate: each undo is itself an audited event
                review.batch_apply(conn, case_id, i, "reset", now)
            raise
    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}


# ------------------------------------------------------------------ export config
def validate_config(b):
    """Returns the normalised config or raises ValueError. All keys optional; unknown keys refused."""
    if not isinstance(b, dict) or set(b) - set(EXPORT_KEYS):
        raise ValueError("invalid_edit")
    out = {}
    for k in ("exhibit", "bates_prefix"):
        v = b.get(k)
        if v is None or v == "":
            out[k] = None
        elif isinstance(v, str) and _LABEL.fullmatch(v):
            out[k] = v
        else:
            raise ValueError("invalid_edit")
    s = b.get("bates_start")
    if s is None:
        out["bates_start"] = None
    elif isinstance(s, int) and not isinstance(s, bool) and 0 <= s <= 99999999:
        out["bates_start"] = s
    else:
        raise ValueError("invalid_edit")
    return out


def get_config(conn, case_id) -> dict:
    cfg = (DB.get_case(conn, case_id).get("config") or {}).get("export") or {}
    return {k: cfg.get(k) for k in EXPORT_KEYS}


def put_config(conn, case_id, cfg):
    case = DB.get_case(conn, case_id)
    config = dict(case.get("config") or {})
    if cfg is None or not any(v is not None for v in cfg.values()):
        config.pop("export", None)
    else:
        config["export"] = cfg
    DB.update_case(conn, case_id, config_json=config or None)


def add_routes(app, *, conn, get_case, body_of, ApiError, now):
    @app.post("/api/cases/{token}/review/batch")
    async def review_batch(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return apply_batch(c, token, b, now())
            except ValueError:
                raise ApiError(400, "bad_request", "Send an action (accept or reset) and a list of entry ids.") from None
            except BatchRefused as e:
                if any(r["reason"] == "date_unconfirmed" for r in e.rejected):     # D-041: same code as a single accept
                    raise ApiError(422, "DATE_UNCONFIRMED", "Confirm the date of every undated entry first (Dates to confirm); nothing was changed.", {"rejected": e.rejected}) from None
                raise ApiError(422, "invalid_batch", "Only verified entries can be accepted together; nothing was changed.", {"rejected": e.rejected}) from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/export_config")
    def export_config_get(token: str):
        c = conn()
        try:
            get_case(c, token)
            return get_config(c, token)
        finally:
28:def init(path: str = ":memory:"):
36:def connect(path: str):
62:def _tok(prefix: str) -> str:
66:def _enc(v):
70:def _cols(conn, table):
74:def sha256(text: str) -> str:
78:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
86:def update_case(conn, case_id: str, **fields) -> None:
95:def get_case(conn, case_id: str):
100:def _insert(conn, table, row):
108:def add_record(conn, case_id: str, **fields) -> str:
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
127:def _find(conn, item_id, case=None):
144:def _decode(row) -> dict:
155:def get_item(conn, item_id: str, case: str = None) -> dict:
159:def list_items(conn, case_id: str, kind: str) -> list:
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
204:def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
211:def list_events(conn, case_id: str, item_id: str = None) -> list:
218:def add_llm_call(conn, case_id: str, prompt: str, response: str, now: float = 0, system: str = None, **fields) -> str:
227:def get_llm_call(conn, call_id: str):
232:def list_llm_calls(conn, case_id: str, item_id: str = None) -> list:
239:def delete_case(conn, case_id: str) -> None:
251:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
258:def table_counts(conn, case_id: str) -> dict:
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/frontend/api.js
 M app/frontend/export.js
 M app/frontend/judges.js
 M app/frontend/stepper.css
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:45.563Z

**tool call — Bash**
````
{
 "command": "sed -n 1,50p memory/contracts/api.md | cut -c1-220; grep -n \"records\" app/db/schema.sql | head; grep -n \"def list_records\\|def get_records\\|records\" app/backend/store.py | head -20; grep -rli \"itemized\\|ledger\" evals/library evals/golden 2>/dev/null | head; grep -n \"total\\|^## \" memory/contracts/api.md | head -60"
}
````

### User / tool · 2026-11-02T04:16:45.699Z

**tool result**
````
# API contract — DRAFT — backend owns from M2

Status: drafted by the architect (T-014, round 2). From M2 the backend worker is the sole writer; changes after that go through a card. Frontend may start against the examples below. They use the Appendix A sample case (

## Conventions
- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
- `{token}` is the case id: a random 128-bit URL-safe string. It is the only credential. **There is no case-list endpoint.** An unknown token is `404 not_found`.
- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run
- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4
- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
- Untrusted strings (record text, excerpts, summaries) are plain text; clients must insert them with `textContent`.

## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 in
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other record
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquot
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also 
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous 
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export 
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |

---

## GET /api/health
```json
{ "ok": true, "version": "0.1.0", "synthetic_only": true,
  "banner": "Synthetic data only — never paste real records",
  "backend": "fixture", "demo_mode": true, "live_enabled": false,
  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "limits": {"max_chars": 60000, "max_records": 40},
  "retention_hours": 24,
  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
  "sample_available": true }
```
9:  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
11:CREATE TABLE IF NOT EXISTS records (
60:CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
14:def load_records(conn, case_id: str, raw: str = None) -> list:
15:    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
19:    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
23:            body = ingest.split_records(block)[0]["excerpt"]
31:def _by_id(records):
32:    return {r["id"]: r for r in records}
39:    recs = load_records(conn, case_id, case["raw_text"])
73:    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
76:    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
evals/library/case_lib11_priors_and_ledger.txt
evals/library/case_lib12_records_review_credibility.txt
evals/library/case_lib15_conclusory_letter_mist.txt
evals/library/case_lib10_eob_ub04_cms1500.txt
evals/library/case_lib10_eob_ub04_cms1500.expected.json
evals/library/case_lib15_conclusory_letter_mist.expected.json
evals/golden/check_golden.py
evals/library/case_lib11_priors_and_ledger.expected.json
evals/library/case_lib12_records_review_credibility.expected.json
evals/golden/sample.export.expected.txt
5:## Conventions
14:## Endpoint index
24:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
25:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
34:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
40:## GET /api/health
53:## POST /api/cases
73:## POST /api/cases/pdf (D-031)
77:## POST /api/cases/{token}/review/batch (D-031)
78:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
80:## /api/cases/{token}/export_config (D-031)
83:## POST /api/cases/{token}/run
90:## GET /api/cases/{token}/status
94:  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
100:## GET /api/cases/{token}
146:      "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
152:  "totals": {
155:    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
156:    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}]
218:## POST /api/cases/{token}/records/{rid}/confirm_date
233:## GET /api/cases/{token}/items/{item_id}  — "Why?"
251:## POST /api/cases/{token}/items/{item_id}/review
278:  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
285:## GET /api/cases/{token}/export
373:        "counted_in_total": true,
380:        "counted_in_total": true,
400:  "totals": {
409:    "records_total": 9
434:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte.
436:## GET /api/cases/{token}/audit
446:  "summary": { "calls": 30, "cost_usd": 0.19, "latency_ms_total": 71200, "by_backend": {"fixture": 30} } }
456:## Check traces (D-042): per-item stepper, case stepper, judge summary
487:  "progress": { "done": 10, "total": 11, "label": "10 of 11 steps settled" },
505:- **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm; `skipped` for damages, which are not judged), `total_inclusion` (code: pass when it is an accepted charge counted in the total, pending when a charge is undecided, skipped when it is not a charge or was dismissed), `human`.
517:  "progress": { "done": 8, "total": 10, "label": "8 of 10 steps settled" },
529:    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
530:    { "id": "totals", "kind": "code", "counts": {"accepted_cents": 0, "pending_cents": 839000, "pending_charges": 2, "not_totaled": 1} },
539:Each case step has the shared step keys plus `counts` (object, may be `{}`); `export_gate` also has `ready` and `blockers[]`. Step order is fixed: `ingest, split, dates, extract, grounding, judges, flags, totals, review, export_gate`. Before the AI run (`status: "ingested"`) `extract`, `grounding`, `judges` and `flags` (AI part) are `pending`; the code-made flags and amounts already count.
548:  "totals": { "items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1, "human_overrides": 1 },
559:`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
561:## POST /api/cases/{token}/rejudge  (D-044)
571:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
577:## DELETE /api/cases/{token}
582:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:47.765Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p app/backend/store.py; grep -n -i -B3 -A25 \"itemized\\|ledger\" evals/library/case_lib11_priors_and_ledger.txt | head -90; grep -n \"def split_records\" -A40 app/backend/ingest.py | head -80"
}
````

### User / tool · 2026-11-02T04:16:47.871Z

**tool result**
````
"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.

Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
"""
from app.backend import ingest, pdf_text
from app.db import db as DB


def iso(t) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_records(conn, case_id: str, raw: str = None) -> list:
    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
    if raw is None:
        raw = DB.get_case(conn, case_id)["raw_text"]
    out = []
    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        d = DB._decode(r)
        block = raw[d["char_start"]:d["char_end"]]
        try:
            body = ingest.split_records(block)[0]["excerpt"]
        except Exception:
            body = block
        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
    return out


def _by_id(records):
    return {r["id"]: r for r in records}


# ---------------------------------------------------------------- unit dicts for export / totals
def export_case(conn, case_id: str) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
18-=== Record 4 ===
19-Date: 2026-03-26
20-Source: Pellingham and Rook PLLC, correspondence (letter of protection)
21:Excerpt: "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement."
22-
23-=== Record 5 ===
24-Date: 2026-03-27
25-Source: Fennimoor Spine Clinic, new patient
26-Excerpt: "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."
27-
28-=== Record 6 ===
29-Date: 3/27/26
30-Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
31-Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."
32-
33-=== Record 7 ===
34-Date: 2026-04-24
35-Source: Fennimoor Spine Clinic, visit 8
36-Excerpt: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
37-
38-=== Record 8 ===
39-Date: 2026-05-29
40-Source: Fennimoor Spine Clinic, visit 14
41-Excerpt: "Neck pain 4/10, low back pain 5/10. Care continues."
42-
43-=== Record 9 ===
44-Date: 2026-06-15
45:Source: Fennimoor Spine Clinic, itemized ledger
46:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
206:def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
207-    text = check_limits(raw_text, max_chars)
208-    recs, _ = _split(text)
209-    if len(recs) > max_records:
210-        raise IngestError("input_too_large")
211-    return recs
212-
213-
214-def record_kind(source: str, excerpt: str = "") -> str:
215-    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
216-    if not (source or "").strip():
217-        return "unsplit_text"
218-    for e in lexicon.code_list("non_encounter"):
219-        if e["regex"].search(source or ""):
220-            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
221-    return "encounter"
222-
223-
224-def _norm(s: str) -> str:
225-    return " ".join((s or "").split()).casefold()
226-
227-
228-def dedupe(records: list) -> list:
229-    """Groups of record numbers (in file order): same date + same normalised provider label + same normalised text merge (R-TL-7)."""
230-    groups, order = {}, []
231-    for r in records:
232-        p = dates.parse_date(r["date_raw"])
233-        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
234-        if key not in groups:
235-            groups[key] = []
236-            order.append(key)
237-        groups[key].append(r["n"])
238-    return [sorted(groups[k]) for k in order]
239-
240-
241-_PHI = [re.compile(p, re.IGNORECASE) for p in (
242-    r"\b\d{3}-\d{2}-\d{4}\b",                                  # SSN
243-    r"(?<!\d)(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}\b",  # phone
244-    r"\bMRN\s*[:#]?\s*[A-Z0-9-]{5,}")]                         # MRN
245-
246-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:16:51.092Z

**tool call — Bash**
````
{
 "command": "sed -n 90,205p app/backend/ingest.py; cat app/backend/lexicon.py | head -40; ls tests/fixtures/llm | head; ls .venv/bin/python"
}
````

### User / tool · 2026-11-02T04:16:51.195Z

**tool result**
````
    e = _F_EXC.search(block)
    if e:
        exc, used = _excerpt_extent(block[e.end():])
        f["excerpt"] = exc
        cov.append((a + e.start(), a + e.end() + used))
        found += 1
    f["complete"] = found == 3
    return (f if found else None), cov


def _leftovers(text: str, cov: list):
    """Non-blank segments of `text` not inside any covered span, as (start, end); an exact golden banner line (BANNERS) on line 1 is exempt."""
    out, pos = [], 0
    for s, e in sorted(cov) + [(len(text), len(text))]:
        if s > pos:
            seg = text[pos:s]
            if seg.strip():
                lead = len(seg) - len(seg.lstrip())
                out.append((pos + lead, pos + len(seg.rstrip())))
        pos = max(pos, e)
    return [(s, e) for s, e in out if not (s == 0 and text[s:e] in BANNERS)]


def _split(text: str):
    """(records, method). Every non-blank character of the input ends up inside some record; text outside a recognised block becomes
    an `unsplit` record (D-027) and the split is reported ambiguous."""
    spans = _spans(text)
    if not spans:
        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
    items, method = [], "code"
    cov_all = [] if _HEADER.search(text) else [(m.start(), m.end()) for m in _SEP.finditer(text)]   # separator lines carry no content
    for a, b in spans:
        f, cov = _scan_block(text, a, b)
        cov_all += cov
        if f is None:
            continue
        if not f["complete"]:
            method = "ambiguous"
        end = max(e for _, e in cov)
        items.append((a, end, f))
    for s, e in _leftovers(text, cov_all):
        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
        method = "ambiguous"
    items.sort(key=lambda t: t[0])
    return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method


def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}


class SplitFailed(Exception):
    """The model could not give a split (call failed, no recorded answer, unusable output). `code` is a reason code; never model text."""
    def __init__(self, code: str, replayed: bool = False):
        super().__init__(code)
        self.code = code
        self.replayed = replayed           # True: the reason was stored by an earlier run; no call was made, so it is not a new failure


def validate_split(text: str, spans, max_records: int = None) -> list:
    """Code check on the model's record boundaries (D-031). `spans` = [(start, end)]. Valid only if they cover `text` exactly
    (first start 0, each end == next start, last end == len(text)), every start falls on a line start, and there are at least two.
    Returns the list of (start, end) or raises ValueError; the caller then keeps the single unsplit record."""
    sp = [(int(a), int(b)) for a, b in spans]
    if max_records is not None and len(sp) > max_records:
        raise ValueError("SPLIT_TOO_MANY")
    if len(sp) < 2 or sp[0][0] != 0 or sp[-1][1] != len(text):
        raise ValueError("SPLIT_NOT_COVERING")
    for i, (a, b) in enumerate(sp):
        if not a < b or (i and a != sp[i - 1][1]):
            raise ValueError("SPLIT_NOT_CONTIGUOUS")
        if a and text[a - 1] != "\n":
            raise ValueError("SPLIT_NOT_ON_LINE_START")
        if not text[a:b].strip():
            raise ValueError("SPLIT_EMPTY_RECORD")
    return sp


def numbered(text: str) -> str:
    """The text with an '@OFFSET| ' label on every line, so the model can name boundaries without counting characters."""
    out, pos = [], 0
    for line in text.split("\n"):
        out.append(f"@{pos}| {line}")
        pos += len(line) + 1
    return "\n".join(out)


def _llm_records(text: str, spans: list) -> list:
    """Records from validated spans. Fields come from code only (labelled lines, or a first line that parses as a date)."""
    out = []
    for a, b in spans:
        s0 = a + (len(text[a:b]) - len(text[a:b].lstrip()))
        first_line = text[s0:b].split("\n", 1)[0].rstrip()
        if s0 == 0 and first_line in BANNERS:       # the golden banner line belongs to no record
            s0 += len(first_line)
            s0 += len(text[s0:b]) - len(text[s0:b].lstrip())
        e0 = a + len(text[a:b].rstrip())
        if s0 >= e0:
            continue
        f, _cov = _scan_block(text, s0, e0)
        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
        if not f["excerpt"]:
            f["excerpt"] = text[s0:e0].strip()
        if not f["date_raw"]:
            first = text[s0:e0].split("\n", 1)[0].strip()
            left, _, right = re.split(r"(\s+[\u2014\u2013|-]\s+)", first, maxsplit=1)[:3] if re.search(r"\s+[\u2014\u2013|-]\s+", first) else (first, "", "")
            if dates.parse_date(left.strip())["status"] == "parsed":     # 'May 4, 2026 - Pottsworth Emergency Department' or a bare date line
                f["date_raw"] = left.strip()
                if right.strip() and not f["source"]:
                    f["source"] = right.strip()
                    f["excerpt"] = text[s0:e0].split("\n", 1)[1].strip() if "\n" in text[s0:e0] else f["excerpt"]
        out.append(_record(len(out) + 1, text[s0:e0], s0, e0, f))
    return out


"""Loader for app/llm/lexicon.yaml (read as a data file; no app.llm import, so deterministic modules stay LLM-free)."""
import functools
import pathlib
import re

import yaml

LEXICON_PATH = pathlib.Path(__file__).resolve().parents[1] / "llm" / "lexicon.yaml"


@functools.lru_cache(maxsize=1)
def load() -> dict:
    return yaml.safe_load(LEXICON_PATH.read_text(encoding="utf-8"))


def code_list(name: str) -> list:
    """Entries of a `code_lists` category as [{id, regex}] (compiled IGNORECASE)."""
    return list(_compiled(name))


@functools.lru_cache(maxsize=None)
def _compiled(name: str) -> tuple:
    entries = load()["code_lists"][name]["entries"]
    return tuple({"id": e["id"], "regex": re.compile(e["pattern"], re.IGNORECASE)} for e in entries)
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
00e8d38a3d50d7d1d7a9b7431c6c2c1970b32930a2583c8a3acd58fdced43d2f.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
0115c20756060b7547d09ea7174734c62c4d2c54f0cc9840da3f4be1c00e19bb.json
03b065e9490648fde69d807c3f2719201ad149f6e41700f46c81c4258230b20a.json
03dca54059c1c53788cc6e6b66442c557959bc4443f86f86120412b8a7cf4b29.json
03f7de3945171cd4ccf7eed0a80ad8642913484686561e412ec1b8ee9a064d66.json
045838e062f32a8011ad9b74cb5cb6d55f3557d26fd6e1186e3f0fd4e2e6ac86.json
.venv/bin/python
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:17:28.476Z

**tool call — Bash**
````
{
 "command": "sed -n 399,424p research/record-formats.md; sed -n 430,472p research/record-formats.md; grep -n -i \"lop\\|lien\\|reduc\" app/llm/lexicon.yaml | head -20; sed -n 40,50p research/record-formats.md"
}
````

### User / tool · 2026-11-02T04:17:28.579Z

**tool result**
````
## 9. UB-04 (CMS-1450) institutional claim

**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
e.g. 0131 hospital outpatient); **FL 6 statement covers period** From/Through; 8-11 patient name and demographics; 12-13 admission date/hour;
14 admission type; 15 source; 17 discharge status; 31-36 occurrence codes and dates (accident codes 01-06, see traps); 39-41 value codes; **FL 42
revenue code** (4-digit, e.g. 0450 emergency room, 0320 x-ray, 0350 CT, 0610 MRI, 0250 pharmacy, 0636 drugs requiring detailed coding);
43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
line, plus the total after the last line); **48 non-covered charges**; 50 payer; 67 principal diagnosis and 67A-Q other diagnoses; 72
external cause of injury codes; 74 principal procedure; 76 attending provider; 80 remarks.

**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line
(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
outpatient lines.

**Extraction traps.**
- Summing every amount in FL 47 includes the 0001 total line and doubles the bill.
- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
- FL 45 on the total line is the claim creation date (unverified convention), not a service date.
- Occurrence codes 01-06 all carry an accident date: 01 auto accident (current NUBC wording reported as accident/medical coverage), 02
  no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim. A PI claim may
  carry any of them (01 or 03 most often). Extraction treats every one as the accident date, never a service date; packets vary the code.
- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.
- On multi-page claims the total appears only on the last page.
- FL 48 non-covered is not an adjustment by the provider; it is still a charge the payer did not cover.
- Payer guides disagree on whether Medicare's FL 47 total excludes non-covered charges; compute from lines and keep both.

- Assumption: FL 44 title "HCPCS/Rate/HIPPS code" and the creation-date-on-line-23 convention are from prior knowledge, confirmed only by the T-078 reviewer's working knowledge; verify against the NUBC manual before quoting.

**Specimen 1 (SYNTHETIC), outpatient ED claim.**
```
SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Quillfeather Regional Medical Center (SYNTHETIC)   3a SYN-PCN-5521  3b SYN-ED-40417  4 0131
6 STATEMENT COVERS PERIOD  FROM 051426  THROUGH 051526
8 OKONKWO-VALE, DELPHINE (SYNTHETIC)   12 ADMISSION 051426  13 HR 23
31 OCCURRENCE  CODE 01  DATE 051426
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00
0350    CT CERVICAL SPINE W/O         72125          051526        1          3,185.00
0636    KETOROLAC INJ 15MG            J1885          051526        2             96.00
0250    PHARMACY GENERAL                             051526        1             38.50           38.50
0001    TOTAL                                        051826                   5,729.50           38.50
67 S16.1XXA   72 ECI V43.52XA   76 ATTENDING Dr. Ilario Fenwick (SYNTHETIC)
PAGE 1 OF 1
```
(The 0001 line repeats the sum; 051826 on that line is the creation date, an unverified convention. Occurrence code 01.)

**Specimen 2 (SYNTHETIC), inpatient claim with a room rate on the charge line** (a different synthetic patient):
```
SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
6 STATEMENT COVERS PERIOD  FROM 091526  THROUGH 091826
8 TELFAIR-NKEMELU, AMBROSE (SYNTHETIC)   12 ADMISSION 091526  13 HR 02  14 TYPE 1  17 STAT 01
31 OCCURRENCE  CODE 03  DATE 091426
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
0450    EMERGENCY ROOM                               091526        1          1,975.00
0250    PHARMACY                                     091526       14            412.75
0300    LABORATORY                                   091526        6            688.00
0320    DX X-RAY                                     091526        2            540.00
0001    TOTAL                                        092226                   9,165.75
67 S42.201A   72 ECI V43.52XA   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)
PAGE 1 OF 1
```
(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money
figure adds the rate and the 0001 line and reports 20,181.50 instead of 9,165.75. Admitted 09/15, discharged 09/18 = 3 room days.
Occurrence code 03, not 01: 09/14/2026 is the accident date, not a service date. 092226 on the 0001 line is the creation date.)

---

133:    hit: ['History of migraines.', 'past medical history of cervical radiculopathy', 'No LOC, history of migraines.', 'No neck complaints before the accident, history of lumbar strain.', 'Prior history of neck pain 2019, resolved.']
167:    hit: ['PMH significant for lumbar strain.', 'Past medical history significant for cervical radiculopathy.']
220:  pattern: '\b(?:prior|previous|earlier|old|remote|past)\s+(?!to\b)(?:[\w/.-]+\s+){0,2}?(?:injur(?:y|ies)|accidents?|MVAs?|MVCs?|collisions?|wrecks?|claims?|fractures?|episodes?|pain|problems?|symptoms?|complaints?|conditions?|issues?|strains?|sprains?|herniations?|bulges?|protrusions?|radiculopath(?:y|ies)|stenosis|sciatica|whiplash|concussions?|dislocations?|diagnos[ei]s|disc\s+\w+)\b'
489:  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|notes|endorses|admits|recalls)\s+(?:(?:a|an|some)\s+)?(?:prior|previous|past|old|earlier|history)\b'
638:    hit: ['possible radiculopathy', 'could represent post-traumatic change', 'questionable relationship to MVA']
739:  pattern: '(?:\b(?:patient|pt\.?|he|she|client)\s+(?:states|stated|reports|reported|believes|attributes|relates|related|feels|claims|says|said|thinks)\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bcomplain(?:s|ing)?\s+of\b|\bc/o\b)[^.;]{0,80}?\b(?:after|since|from|due\s+to|because\s+of|caused\s+by|following|began\s+with)\b[^.;]{0,40}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:attributes?|relates?|links?|ascribes?|connects?|associates?|blames?)\b[^.;]{0,80}?\b(?:to|on|with)\s+(?:the\s+|this\s+|that\s+|a\s+)?(?:\w+\s+){0,2}(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:believes|feels|thinks|states|claims|says|reports)\s+(?:that\s+)?(?:the\s+|this\s+)?(?:\w+\s+)?(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\s+(?:caused|led\s+to|resulted\s+in|is\s+(?:the\s+)?(?:cause|reason|why|responsible)|triggered|brought\s+on)\b|\b(?:after|since|from|due\s+to|following)\b[^.;]{0,60}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b[^.;]{0,40}?,?\s*per\s+(?:the\s+)?(?:patient|pt)\b'
755:  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|endorses|complains|c/o|describes|relates|notes|admits|recalls)\b|\bc/o\b|\bcomplain(?:s|ing)?\s+of\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bpatient-?\s?reported\b'
768:    miss: ['Cervical range of motion reduced approx. 40%.']
771:  pattern: '\bper\s+(?:the\s+)?(?:intake(?:\s+form)?|patient\s+intake(?:\s+form)?|registration(?:\s+form)?|questionnaire|patient\s+paperwork)\b|\b(?:date\s+of\s+(?:accident|injury|loss)|accident\s+date|DOA|DOI)\s+(?:per|according\s+to|as\s+reported\s+by)\s+(?:the\s+)?(?:patient|pt|intake|form|client)\b'
787:  pattern: '\bnew(?:ly)?[-\s]+(?:onset|developed|complaints?|symptoms?|pain)\b'
799:    hit: ['New onset pain radiating to right arm', 'newly developed numbness']
804:  pattern: '\b(?:delayed\s+onset|(?:began|started|developed|appeared|noticed)\s+(?:\w+\s+){0,3}(?:days?|weeks?|months?)\s+(?:after|later|post)|(?:days?|weeks?|months?)\s+(?:after|following)\s+the\s+(?:accident|collision|MVA|MVC|crash)|did\s+not\s+(?:seek|report)\s+(?:\w+\s+){0,2}(?:care|treatment|injury)\s+until)\b'
866:    miss: ['Objective: ROM reduced 40%.']
882:    miss: ['Cervical range of motion reduced approx. 40%.']
901:  pattern: '\breferred\b[^.;]{0,40}?\bby\s+(?:his|her|their|the\s+patient''s|the)?\s*(?:attorney|lawyer|counsel|law\s+firm)\b|\battorney[-\s]referr\w*|\bletter\s+of\s+protection\b|\bLOP\b|\blien\s+basis\b|\btreating\s+on\s+(?:a\s+)?lien\b'
908:  rationale: 'Attorney-referred or LOP-funded care is attacked as litigation-driven, and its charges as unreasonable (K&L Auto Crushers made negotiated rates discoverable). D-018 makes it a causation flag.'
910:  false_positive: '"LOP" can be an unrelated abbreviation; the LLM confirms.'
943:  false_positive: 'Round 2 narrowed "did not show" to "did not show up/for" and "did not present" to "did not present for <appointment>": "did not show signs of radiculopathy" and "did not present with LOC" are clinical negatives.'
947:    miss: ['showed improvement', 'Did not present with loss of consciousness.', 'Patient did not show signs of radiculopathy.']
998:  pattern: '\bagainst\s+medical\s+advice\b|\bleft\s+(?:AMA|without\s+being\s+seen)\b|\bLWBS\b|\beloped\b|\bsigned\s+out\s+AMA\b'
### 1.2 Money: charges, rates, adjustments, estimates
| Wording | Meaning | Counted as a billed charge? (D-019, D-042) |
|---|---|---|
| "Charges", "Total charges", "$Charges", "Amount billed", "Gross charges" | A stated charge for a dated service | Yes, when tied to a date of service and accepted |
| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
| "Payment", "Ins pmt", "Pt pmt", "Plan paid", "Amount paid" (Item 29) | Money received | No |
| "Balance", "Balance due", "Amount due", "You owe", "Patient responsibility" | Remaining amount | No (it is a derived figure) |
| "Estimate", "Anticipated", "Quote", "Future care" | Not yet incurred | No |
| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:25.286Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_case_extras.py; .venv/bin/python - <<'E'\nfrom app.backend import dates\nprint(dates.parse_date(\"05/27/26\"), dates.parse_date(\"2026-05-27\"), dates.parse_date(\"05/27/2026\"))\nE"
}
````

### User / tool · 2026-11-02T04:18:25.394Z

**tool result**
````
"""Batch accept of verified entries (atomic, entries only) and per-case export config (D-031; T-055, T-058)."""
import time
import pytest
from fastapi.testclient import TestClient
from app.backend import export as X
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_api_routes import wait_ready, run_case
from tests.unit.test_export import build_case


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "x.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def items(c, tok):
    v = c.get(f"/api/cases/{tok}").json()
    return v


def statuses(db, tok):
    conn = DB.connect(db)
    out = {k: {i["id"]: (i["review_status"], i["state"]) for i in DB.list_items(conn, tok, k)} for k in ("entry", "amount", "flag")}
    conn.close()
    return out


def test_batch_accepts_verified_entries_only_and_logs_one_event_each(env):
    db, c = env
    tok = run_case(c)
    st = statuses(db, tok)
    ver = [i for i, (rs, s) in st["entry"].items() if s == "verified" and rs == "pending"]
    assert len(ver) >= 7
    r = c.post(f"/api/cases/{tok}/review/batch", json={"action": "accept", "item_ids": ver})
{'raw': '05/27/26', 'status': 'parsed', 'iso': '2026-05-27', 'candidates': []} {'raw': '2026-05-27', 'status': 'parsed', 'iso': '2026-05-27', 'candidates': []} {'raw': '05/27/2026', 'status': 'parsed', 'iso': '2026-05-27', 'candidates': []}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:18:29.752Z

**tool call — Bash**
````
{
 "command": "mkdir -p /tmp/x 2>/dev/null; .venv/bin/python - <<'E'\nimport re\nL='''DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00\n06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00\n07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00'''.split(\"\\n\")\nfor m in re.finditer(r\"[A-Z]+\",L[0]): print(m.group(),m.start(),m.end())\nfor l in L[1:]:\n    for m in re.finditer(r\"\\S*\\d+\\.\\d\\d\\S*\",l): print(m.group(),m.start(),m.end())\nE"
}
````

### User / tool · 2026-11-02T04:18:29.860Z

**tool result**
````
DOS 0 3
POSTED 10 16
CODE 20 24
DESCRIPTION 27 38
CHARGES 56 63
PAYMENTS 66 74
ADJ 77 80
BALANCE 88 95
210.00 57 63
210.00 88 94
(70.00) 57 64
375.00 88 94
45.00- 77 83
400.00 88 94
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:19:47.072Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport re\nL='''42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED\n0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00\n0250    PHARMACY GENERAL                             051526        1             38.50           38.50\n0001    TOTAL                                        051826                   5,729.50           38.50\n0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00'''.split(\"\\n\")\nfor k in (\"RATE\",\"TOTAL CHARGES\",\"NON-COVERED\"):\n    m=re.search(k,L[0]); print(k,m.start(),m.end())\nfor l in L[1:]:\n    print([ (m.group(),m.start(),m.end()) for m in re.finditer(r\"[\\d,]+\\.\\d\\d\",l)])\nE"
}
````

### User / tool · 2026-11-02T04:19:47.172Z

**tool result**
````
RATE 45 49
TOTAL CHARGES 78 91
NON-COVERED 96 107
[('2,410.00', 78, 86)]
[('38.50', 81, 86), ('38.50', 97, 102)]
[('5,729.50', 78, 86), ('38.50', 97, 102)]
[('1,850.00', 38, 46), ('5,550.00', 78, 86)]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:21:14.383Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "content": "\"\"\"Billing analysis on itemized ledgers, claim forms and EOBs (T-083, D-042). CODE ONLY: no model is asked anything here.\n\nWhat it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the\nrecord). Totals are per provider. LOP and lien amounts are listed separately and never added. Nothing is totaled that the records do not\nstate (D-019): a rate is never a charge, a running balance is never summed, a claim-form total (UB-04 line 0001, CMS-1500 Item 28) is\ncompared with the line sum and never added to it, an EOB's \"amount billed\" restates the bill and is never added, and a figure that cannot\nbe read cleanly (OCR letters, odd decimals, a column that cannot be told apart) is LISTED with cents None and kept out of every total.\nThe analysis is computed on read, never stored, and never reaches the letter: the letter's total line is still only accepted charges (D-019).\nDisagreements (ledger total vs line sum, ledger paid vs EOB paid, ...) are raised as `checks`; the code never picks a side.\nMoney is whole cents (int); integer arithmetic only.\n\"\"\"\nimport re\n\nfrom app.backend import amounts as A, dates, lexicon\n\n# ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)\nCHECKS = {\n    \"LEDGER_TOTAL_MISMATCH\": \"The statement's own total does not match the sum of its lines. Both figures are shown; check the original.\",\n    \"LEDGER_BALANCE_MISMATCH\": \"The stated balance does not equal the charges minus payments and adjustments on the parsed lines.\",\n    \"BALANCE_STEP_MISMATCH\": \"This line's running balance does not follow from the line before it, so a column may have been read wrongly.\",\n    \"LINE_UNCLEAR\": \"A figure on this line could not be read cleanly. It is listed but not totaled.\",\n    \"CLAIM_TOTAL_MISMATCH\": \"The claim form's printed total does not match the sum of its lines. Both figures are shown.\",\n    \"CLAIM_LEDGER_BILLED_MISMATCH\": \"The claim form and the itemized ledger for this provider show different billed totals. The ledger is used; check both.\",\n    \"LEDGER_EOB_PAID_MISMATCH\": \"The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.\",\n    \"LEDGER_EOB_BILLED_MISMATCH\": \"The ledger's billed amount for this date and service differs from the amount billed on the EOB.\",\n    \"NO_DATE_OF_SERVICE\": \"Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.\",\n}\nRULES = [\n    \"Only figures stated in the records are totaled; nothing is derived or estimated.\",\n    \"A rate (per visit, per unit, fee schedule, UB-04 line 44) is never a charge.\",\n    \"A running balance, a claim-form total and an EOB's amount billed are never added to the charges.\",\n    \"LOP, lien and attorney-reduction amounts are listed separately and never totaled with charges.\",\n    \"A figure that cannot be read cleanly is listed with no value and left out of every total.\",\n    \"This analysis is for review only. The letter's total line is still accepted charges only.\",\n]\n\n# ------------------------------------------------------------------ money tokens\n_FIG = r\"\\(?-?\\$?(?:\\d{1,3}(?:,\\d{3})+|\\d+)\\.\\d+\\)?-?\"\n_NUM = re.compile(rf\"(?<![\\w/.]){_FIG}(?![\\w/]|\\.\\d)\")\n_DATE = r\"(?:\\d{1,2}/\\d{1,2}/\\d{2,4}|\\d{4}-\\d{2}-\\d{2})\"\n_ROW = re.compile(rf\"^\\s*({_DATE})\\s+(?:({_DATE})\\s+)?(.*)$\")\n_VOID = re.compile(r\"\\b(?:void(?:ed)?|reverse[ds]?|reversal|rev\\.?\\s+chg)\\b\", re.IGNORECASE)\n_NEGOTIATED = re.compile(r\"\\b(?:atty|attorney|lawyer)\\s+(?:reduction|adj\\w*|discount)|\\breduced\\s+to\\b|\\bsettlement\\s+(?:reduction|discount)\\b|\\bin\\s+full\\s+satisfaction\\b\", re.IGNORECASE)\n_BALFWD = re.compile(r\"\\bbal(?:ance)?\\.?\\s*(?:fwd|forward|brought\\s+forward)\\b|\\bprevious\\s+balance\\b|\\bprior\\s+balance\\b\", re.IGNORECASE)\n_COLS = {\"billed\": re.compile(r\"\\b(?:CHARGES?|BILLED)\\b\", re.IGNORECASE), \"paid\": re.compile(r\"\\b(?:PAYMENTS?|PMTS?|PAID)\\b\", re.IGNORECASE),\n         \"adjustment\": re.compile(r\"\\b(?:ADJ(?:USTMENTS?|S)?)\\b\", re.IGNORECASE), \"balance\": re.compile(r\"\\b(?:BALANCE|BAL)\\b\", re.IGNORECASE)}\nTOL = 8        # characters a figure may sit away from its column header (left or right aligned) before the column is called unclear\n\n\ndef fmt(cents):\n    if cents is None:\n        return None\n    return (\"-\" if cents < 0 else \"\") + f\"${abs(cents) // 100:,}.{abs(cents) % 100:02d}\"\n\n\ndef parse_figure(token: str) -> dict:\n    \"\"\"'(70.00)' -> {cents: -7000}, '45.00-' -> -4500, '1,234.50' -> 123450. Credit notation (parentheses, trailing or leading minus) makes it\n    negative. Exactly two decimals are required: '95.5' or '9.999' keep their text and cents None, never rounded.\"\"\"\n    neg = token.startswith(\"(\") or token.startswith(\"-\") or token.endswith(\"-\") or token.endswith(\")\")\n    digits = re.sub(r\"[()\\-$]\", \"\", token)\n    cents = A.to_cents(digits) if re.search(r\"\\.\\d\\d\\Z\", digits) else None\n    return {\"text\": token, \"cents\": None if cents is None else (-cents if neg else cents), \"usd\": None if cents is None else fmt(-cents if neg else cents)}\n\n\ndef _mag(f):\n    \"\"\"Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept. The running\n    balance step check is what catches a column that was read the wrong way.\"\"\"\n    return {**f, \"cents\": None if f[\"cents\"] is None else abs(f[\"cents\"]), \"usd\": None if f[\"cents\"] is None else fmt(abs(f[\"cents\"]))}\n\n\ndef _norm(s):\n    return \" \".join(re.sub(r\"[^a-z0-9]+\", \" \", (s or \"\").casefold().replace(\"(synthetic)\", \"\")).split())\n\n\ndef _provider(rec: dict) -> str:\n    src = (rec.get(\"source\") or \"\").strip()\n    name = re.split(r\",|\\s[-–—]\\s\", src, maxsplit=1)[0].strip()\n    name = re.sub(r\"\\s+(?:itemized\\s+)?(?:ledger|statement|billing|bill|claim|eob)\\s*$\", \"\", name, flags=re.IGNORECASE).strip()\n    return name or \"Unknown provider\"\n\n\ndef _dos(raw):\n    p = dates.parse_date(raw or \"\")\n    return p[\"iso\"] if p.get(\"status\") == \"parsed\" else None\n\n\ndef _cite(rec, line):\n    return {\"record_no\": rec[\"n\"], \"excerpt\": line.strip()}\n\n\n# ------------------------------------------------------------------ record forms\ndef form_of(rec: dict) -> str:\n    \"\"\"ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words.\"\"\"\n    body = (rec.get(\"excerpt\") or rec.get(\"text\") or \"\")\n    src = rec.get(\"source\") or \"\"\n    up = body.upper()\n    if \"EXPLANATION OF BENEFITS\" in up or \"THIS IS NOT A BILL\" in up or re.search(r\"\\bEOB\\b\", src, re.IGNORECASE) or (\"PLAN PAID\" in up and \"BILLED\" in up):\n        return \"eob\"\n    if \"UB-04\" in up or \"UB04\" in up or \"CMS-1450\" in up or \"47 TOTAL CHARGES\" in up or re.search(r\"\\bUB-?04\\b\", src, re.IGNORECASE):\n        return \"ub04\"\n    if \"TOTAL CHARGE\" in up and \"AMOUNT PAID\" in up or \"1500\" in src or \"HEALTH INSURANCE CLAIM FORM\" in up:\n        return \"cms1500\"\n    if _header(body.split(\"\\n\"))[0] is not None:\n        return \"ledger_table\"\n    if \"$\" in body and (A._is_billing_source(src) or re.search(r\"\\bitemized\\s+(?:ledger|statement)\\b|\\bledger\\b\", body, re.IGNORECASE)):\n        return \"ledger_text\"\n    return None\n\n\ndef _header(lines):\n    \"\"\"(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column.\"\"\"\n    for i, ln in enumerate(lines):\n        if _ROW.match(ln) or re.match(r\"\\s*TOTAL\\b\", ln, re.IGNORECASE):\n            continue\n        cols = {}\n        for kind, rx in _COLS.items():\n            m = rx.search(ln)\n            if m:\n                cols[kind] = (m.start(), m.end())\n        if \"billed\" in cols and \"balance\" in cols and len(cols) >= 3:\n            return i, cols\n    return None, None\n\n\ndef _column(token_span, cols):\n    \"\"\"The column whose header the figure sits under (left- or right-aligned), or None when two are equally near or none within TOL.\"\"\"\n    s, e = token_span\n    d = sorted((min(abs(s - hs), abs(e - he)), kind) for kind, (hs, he) in cols.items())\n    if d[0][0] > TOL or (len(d) > 1 and d[1][0] == d[0][0]):\n        return None\n    return d[0][1]\n\n\n# ------------------------------------------------------------------ itemized ledger table\ndef _ledger_table(rec, lines):\n    hi, cols = _header(lines)\n    out, stated, balfwd = [], {}, None\n    for ln in lines[hi + 1:]:\n        if re.match(r\"\\s*TOTAL\\b\", ln, re.IGNORECASE) or re.search(r\"\\bBALANCE\\s+DUE\\b\", ln, re.IGNORECASE):\n            stated.update(_stated(rec, ln))\n            continue\n        if _BALFWD.search(ln):\n            figs = [m for m in _NUM.finditer(ln)]\n            if figs:\n                balfwd = {**parse_figure(figs[-1].group(0)), \"cite\": _cite(rec, ln)}\n            continue\n        m = _ROW.match(ln)\n        if not m:\n            continue\n        figs = list(_NUM.finditer(ln))\n        head = ln[:figs[0].start()] if figs else ln\n        row_m = _ROW.match(head + \" \")\n        parts = (row_m.group(3) if row_m else \"\").split(None, 1)\n        code = parts[0] if parts and re.fullmatch(r\"[A-Za-z0-9]{2,7}\", parts[0]) and (len(parts) > 1 or not figs) else None\n        desc = (parts[1] if code and len(parts) > 1 else \" \".join(parts)).strip() if parts else \"\"\n        line = {\"record_no\": rec[\"n\"], \"form\": \"ledger\", \"dos\": m.group(1), \"dos_iso\": _dos(m.group(1)), \"posted\": m.group(2), \"code\": code,\n                \"description\": desc, \"billed\": None, \"adjustment\": None, \"paid\": None, \"balance\": None, \"unclear\": [], \"excerpt\": ln.strip()}\n        for fm in figs:\n            kind = _column(fm.span(), cols)\n            f = parse_figure(fm.group(0))\n            if kind is None or f[\"cents\"] is None:\n                line[\"unclear\"].append(f[\"text\"])\n            elif line[kind] is not None:\n                line[\"unclear\"].append(f[\"text\"])            # two figures in one column: not guessed\n            else:\n                line[kind] = _mag(f) if kind in (\"paid\", \"adjustment\") else f\n        out.append(line)\n    stated.update({k: v for k, v in _stated(rec, \"\\n\".join(lines[hi + 1:])).items() if k not in stated})\n    return out, stated, balfwd\n\n\n_STATED = {\"billed\": re.compile(rf\"TOTAL\\s+CHARGES?\\s*[:=]?\\s*({_FIG})\", re.IGNORECASE),\n           \"paid\": re.compile(rf\"TOTAL\\s+(?:PMTS?|PAYMENTS?)\\s*[:=]?\\s*({_FIG})\", re.IGNORECASE),\n           \"adjustment\": re.compile(rf\"TOTAL\\s+ADJ\\w*\\s*[:=]?\\s*({_FIG})\", re.IGNORECASE),\n           \"balance\": re.compile(rf\"(?:BALANCE\\s+DUE|AMOUNT\\s+DUE|TOTAL\\s+BALANCE)\\s*[:=]?\\s*({_FIG})\", re.IGNORECASE)}\n\n\ndef _stated(rec, text):\n    \"\"\"Totals the statement prints itself. Returned with the line they were read from; compared with the parsed lines, never used instead.\"\"\"\n    out = {}\n    for kind, rx in _STATED.items():\n        m = rx.search(text)\n        if m:\n            f = parse_figure(m.group(1))\n            f = _mag(f) if kind in (\"paid\", \"adjustment\") else f\n            ln = next((x for x in text.split(\"\\n\") if m.group(0) in x), m.group(0))\n            out[kind] = {**f, \"cite\": _cite(rec, ln)}\n    return out\n\n\n# ------------------------------------------------------------------ ledger written as a sentence (\"New patient exam charge $250.00; ...\")\n_PROSE = ((\"billed_total\", re.compile(r\"\\btotal\\s+(?:billed\\s+)?charges?\\b|\\btotal\\s+billed\\b\", re.IGNORECASE)),\n          (\"paid\", re.compile(r\"\\bpayments?\\b|\\bpaid\\b|\\bpmts?\\b\", re.IGNORECASE)),\n          (\"adjustment\", re.compile(r\"\\badjust\\w*|\\bdiscount\\b|\\bwrite-?off\\b|\\bcontractual\\b|\\bcourtesy\\b|\\bW/O\\b\", re.IGNORECASE)),\n          (\"balance\", re.compile(r\"\\bbalance\\b|\\bamount\\s+due\\b\", re.IGNORECASE)))\n_SEG = re.compile(r\"[^.;!?\\n]+(?:\\.\\d+[^.;!?\\n]*)*[.;!?]?\")\n\n\ndef _segments(text):\n    \"\"\"[(start, end)] of clauses: split at ; ! ? newline and a period that ends a sentence (not the decimal point of a figure).\"\"\"\n    out, pos = [], 0\n    for m in re.finditer(r\"(?<=[;!?])\\s+|\\n|(?<=[a-zA-Z)\\d])\\.(?=\\s+[A-Z])\\s*\", text):\n        out.append((pos, m.start() + (1 if text[m.start()] == \".\" else 0)))\n        pos = m.end()\n    out.append((pos, len(text)))\n    return [(s, e) for s, e in out if text[s:e].strip()]\n\n\ndef _ledger_text(rec, body):\n    lines, stated = [], {}\n    for s, e in _segments(body):\n        seg = body[s:e]\n        for a in A.find_amounts(seg):\n            if a[\"cents\"] is None:\n                continue\n            label = A._label(seg, a[\"start\"])\n            neg = seg[max(0, a[\"start\"] - 1):a[\"start\"]] == \"-\" or label.endswith(\"-\")\n            raw = (\"-\" if neg else \"\") + a[\"raw\"]\n            fig = {\"text\": raw, \"cents\": -a[\"cents\"] if neg else a[\"cents\"], \"usd\": fmt(-a[\"cents\"] if neg else a[\"cents\"])}\n            kind = next((k for k, rx in _PROSE if rx.search(label)), None)\n            cite = _cite(rec, seg)\n            if kind == \"billed_total\":\n                stated[\"billed\"] = {**fig, \"cite\": cite}\n            elif kind in (\"paid\", \"adjustment\"):\n                lines.append(_pline(rec, seg, kind, _mag(fig), _NEGOTIATED.search(seg) is not None))\n            elif kind == \"balance\":\n                stated[\"balance\"] = {**fig, \"cite\": cite}\n            elif A.classify(seg, a, source=rec.get(\"source\")) == \"charge\":\n                lines.append(_pline(rec, seg, \"billed\", fig))\n    return lines, stated\n\n\ndef _pline(rec, seg, kind, fig, negotiated=False):\n    line = {\"record_no\": rec[\"n\"], \"form\": \"ledger\", \"dos\": None, \"dos_iso\": None, \"posted\": None, \"code\": None, \"description\": seg.strip(),\n            \"billed\": None, \"adjustment\": None, \"paid\": None, \"balance\": None, \"unclear\": [], \"excerpt\": seg.strip()}\n    line[kind] = fig\n    return line\n\n\n# ------------------------------------------------------------------ CMS-1500 service lines (24F is implied-cents)\n_AMT = r\"[0-9O]+(?:\\s*\\|\\s*[0-9O]{2}|[ ][0-9O]{2}(?![\\d.O]))?\"\n_CMS = re.compile(rf\"^\\s*(?:24\\.\\s*)?([0-9O]{{6}})\\s+([0-9O]{{6}})\\s+(\\d{{2}})\\s+([A-Z0-9]{{5}})(?:\\s+[A-Z0-9]{{1,4}})*?\\s+({_AMT})\\s+(\\d+)(?:\\s+(\\S+))?\\s*$\")\n_CMS_TOTAL = re.compile(rf\"\\bTOTAL\\s+CHARGE\\s+({_AMT}|{_FIG})\")\n_CMS_PAID = re.compile(rf\"\\bAMOUNT\\s+PAID\\s+({_AMT}|{_FIG})\")\n\n\ndef box_amount(raw: str) -> dict:\n    \"\"\"A CMS-1500 money box has no decimal point: '85 | 00', '85 00' and '8500' are all $85.00. A printed decimal point is honoured.\n    OCR letters (O for 0) keep the text, cents None.\"\"\"\n    raw = raw.strip()\n    if \"O\" in raw.upper().replace(\"|\", \"\"):\n        return {\"text\": raw, \"cents\": None, \"usd\": None, \"implied_decimal\": True}\n    if re.fullmatch(_FIG, raw):\n        return {**parse_figure(raw), \"implied_decimal\": False}\n    if \"|\" in raw:\n        d, c = [x.strip() for x in raw.split(\"|\")]\n        cents = int(d) * 100 + int(c)\n    elif re.fullmatch(r\"\\d+ \\d\\d\", raw):\n        d, c = raw.split(\" \")\n        cents = int(d) * 100 + int(c)\n    elif re.fullmatch(r\"\\d{3,}\", raw):\n        cents = int(raw)\n    else:\n        return {\"text\": raw, \"cents\": None, \"usd\": None, \"implied_decimal\": True}\n    return {\"text\": raw, \"cents\": cents, \"usd\": fmt(cents), \"implied_decimal\": True}\n\n\ndef _cms1500(rec, lines):\n    out, stated = [], {}\n    for ln in lines:\n        m = _CMS.match(ln)\n        if m:\n            fig = box_amount(m.group(5))\n            line = {\"record_no\": rec[\"n\"], \"form\": \"cms1500\", \"dos\": m.group(1) if m.group(1) == m.group(2) else f\"{m.group(1)}-{m.group(2)}\", \"dos_iso\": None,\n                    \"posted\": None, \"code\": m.group(4), \"description\": f\"units {m.group(6)}\", \"billed\": None, \"adjustment\": None, \"paid\": None,\n                    \"balance\": None, \"unclear\": [], \"excerpt\": ln.strip(), \"units\": int(m.group(6))}\n            if fig[\"cents\"] is None:\n                line[\"unclear\"].append(fig[\"text\"])\n            else:\n                line[\"billed\"] = fig\n            out.append(line)\n        else:\n            for kind, rx in ((\"billed\", _CMS_TOTAL), (\"paid\", _CMS_PAID)):\n                t = rx.search(ln)\n                if t:\n                    f = box_amount(t.group(1))\n                    if f[\"cents\"] is not None:\n                        stated[kind] = {**f, \"cite\": _cite(rec, ln)}\n    return out, stated\n\n\n# ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)\n_UBROW = re.compile(r\"^\\s*(\\d{4})\\s+(\\S.*?)(?:\\s{2,}|$)\")\n\n\ndef _ub04(rec, lines):\n    hi = next((i for i, ln in enumerate(lines) if re.search(r\"TOTAL\\s+CHARGES\", ln, re.IGNORECASE) and re.search(r\"\\bREV\\b|SERV\", ln)), None)\n    if hi is None:\n        return [], {}, []\n    h = lines[hi]\n    cols = {}\n    for kind, rx in ((\"rate\", r\"HCPCS/RATE|RATE\"), (\"billed\", r\"TOTAL\\s+CHARGES\"), (\"noncovered\", r\"NON-COVERED\")):\n        m = re.search(rx, h)\n        if m:\n            cols[kind] = (m.start(), m.end())\n    out, rates, stated = [], [], {}\n    for ln in lines[hi + 1:]:\n        m = _UBROW.match(ln)\n        if not m:\n            continue\n        figs = [(f, _column(f.span(), cols)) for f in _NUM.finditer(ln)]\n        if m.group(1) == \"0001\":\n            for f, k in figs:\n                if k == \"billed\":\n                    stated[\"billed\"] = {**parse_figure(f.group(0)), \"cite\": _cite(rec, ln)}\n            continue\n        line = {\"record_no\": rec[\"n\"], \"form\": \"ub04\", \"dos\": None, \"dos_iso\": None, \"posted\": None, \"code\": m.group(1), \"description\": m.group(2).strip(),\n                \"billed\": None, \"adjustment\": None, \"paid\": None, \"balance\": None, \"unclear\": [], \"excerpt\": ln.strip(), \"non_covered\": None}\n        sd = re.search(r\"\\b(\\d{6})\\b\", ln[:figs[0][0].start()] if figs else ln)\n        line[\"dos\"] = sd.group(1) if sd else None\n        for f, k in figs:\n            p = parse_figure(f.group(0))\n            if p[\"cents\"] is None or k is None:\n                line[\"unclear\"].append(p[\"text\"])\n            elif k == \"rate\":\n                rates.append({\"record_no\": rec[\"n\"], \"kind\": \"rate\", \"why\": \"UB-04 line 44 is a rate, not a charge.\", \"figure\": p, \"excerpt\": ln.strip()})\n            elif k == \"noncovered\":\n                line[\"non_covered\"] = p\n            elif line[\"billed\"] is None:\n                line[\"billed\"] = p\n            else:\n                line[\"unclear\"].append(p[\"text\"])\n        out.append(line)\n    return out, stated, rates\n\n\n# ------------------------------------------------------------------ EOB (payer figures; never added to charges)\n_EOBCOLS = ((\"billed\", r\"BILLED\"), (\"discount\", r\"DISCOUNT|NOT\\s+COVERED\"), (\"allowed\", r\"ALLOWED\"), (\"deductible\", r\"DEDUCT\\w*\"), (\"copay\", r\"COPAY\"),\n            (\"coinsurance\", r\"COINS\\w*\"), (\"plan_paid\", r\"PLAN\\s+PAID\"), (\"patient_owes\", r\"YOU\\s+MAY\\s+OWE|PATIENT\\s+RESP\\w*\"))\n\n\ndef _eob(rec, lines):\n    hi = next((i for i, ln in enumerate(lines) if re.search(r\"\\bBILLED\\b\", ln) and re.search(r\"PLAN\\s+PAID\", ln, re.IGNORECASE)), None)\n    prov = next((re.sub(r\"\\s+\", \" \", m.group(1)).strip() for ln in lines for m in [re.match(r\"\\s*Provider\\s*:\\s*(.+?)\\s*$\", ln, re.IGNORECASE)] if m), None)\n    if hi is None:\n        return {\"record_no\": rec[\"n\"], \"provider\": prov or _provider(rec), \"lines\": []}\n    order = sorted(((m.start(), k) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m))\n    names = [k for _, k in order]\n    out = []\n    for ln in lines[hi + 1:]:\n        m = re.match(rf\"^\\s*({_DATE})\\s+(\\S+)\\s+\", ln)\n        if not m:\n            continue\n        figs = [parse_figure(f.group(0)) for f in _NUM.finditer(ln)]\n        row = {\"record_no\": rec[\"n\"], \"dos\": m.group(1), \"dos_iso\": _dos(m.group(1)), \"service\": m.group(2), \"excerpt\": ln.strip(), \"unclear\": [],\n               \"codes\": (ln[list(_NUM.finditer(ln))[-1].end():].strip() or None) if figs else None}\n        if len(figs) == len(names) and all(f[\"cents\"] is not None for f in figs):\n            row.update({k: _mag(f) for k, f in zip(names, figs)})\n        else:\n            row[\"unclear\"] = [f[\"text\"] for f in figs]\n        out.append(row)\n    return {\"record_no\": rec[\"n\"], \"provider\": prov or _provider(rec), \"lines\": out}\n\n\n# ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)\n_LOP_SOURCE = re.compile(r\"letter\\s+of\\s+protection|\\bLOP\\b|\\blien\\b|reduction\\s+letter|assignment\", re.IGNORECASE)\n_LOP_LABEL = re.compile(r\"\\b(?:LOP|lien)\\b[^,;]{0,25}\\b(?:balance|amount)|\\b(?:balance|amount)\\b[^,;]{0,25}\\b(?:LOP|lien)\\b|\\breduced\\s+to\\b|\\baccept\\w*\\b[^.;]{0,50}\\bsatisf\\w+|\"\n                        r\"\\b(?:atty|attorney)\\s+reduction\\b|\\bcurrent\\s+balance\\b|\\bin\\s+full\\s+satisfaction\\b\", re.IGNORECASE)\n\n\ndef _lop_lien(rec):\n    body = rec.get(\"excerpt\") or rec.get(\"text\") or \"\"\n    doc = bool(_LOP_SOURCE.search(rec.get(\"source\") or \"\"))\n    out = []\n    for s, e in _segments(body):\n        seg = body[s:e]\n        for a in A.find_amounts(seg):\n            if a[\"cents\"] is None:\n                continue\n            label = A._label(seg, a[\"start\"])\n            if not (doc or _LOP_LABEL.search(label) or _LOP_LABEL.search(seg)):\n                continue\n            kind = \"reduction\" if re.search(r\"reduc|satisf\", seg, re.IGNORECASE) else (\"lien_amount\" if re.search(r\"\\blien\\b\", seg, re.IGNORECASE) else \"asserted_balance\")\n            out.append({\"record_no\": rec[\"n\"], \"provider\": _provider(rec), \"kind\": kind, \"label\": \" \".join(label.split()) or None,\n                        \"figure\": {\"text\": a[\"raw\"], \"cents\": a[\"cents\"], \"usd\": fmt(a[\"cents\"])}, \"excerpt\": seg.strip(), \"in_totals\": False})\n    return out\n\n\n# ------------------------------------------------------------------ assembling\ndef _checks_for_line(line, prev_balance):\n    codes = []\n    if line[\"unclear\"]:\n        codes.append(\"LINE_UNCLEAR\")\n    bal = line[\"balance\"][\"cents\"] if line.get(\"balance\") else None\n    if bal is not None and prev_balance is not None:\n        delta = sum(v[\"cents\"] for k, v in ((k, line[k]) for k in (\"billed\",)) if v and v[\"cents\"] is not None)\n        delta -= sum(line[k][\"cents\"] for k in (\"paid\", \"adjustment\") if line[k] and line[k][\"cents\"] is not None)\n        if bal - prev_balance != delta:\n            codes.append(\"BALANCE_STEP_MISMATCH\")\n    return codes\n\n\ndef _line_key(l):\n    g = lambda k: (l[k] or {}).get(\"cents\") if l.get(k) else None\n    return (_norm(l.get(\"dos\")), _norm(l.get(\"posted\")), _norm(l.get(\"code\")), _norm(l.get(\"description\")), g(\"billed\"), g(\"paid\"), g(\"adjustment\"), l.get(\"form\"))\n\n\ndef _merge_duplicates(lines):\n    \"\"\"A line repeated in a later record (a re-sent statement, an attached copy) counts once and cites both. Repeats inside ONE record are real.\"\"\"\n    out, seen = [], {}\n    for l in lines:\n        key = _line_key(l)\n        hit = next((o for o in seen.get(key, []) if l[\"record_no\"] not in o[\"record_nos\"] and l[\"record_no\"] not in o[\"_taken\"]), None)\n        if hit and key[4:7] != (None, None, None):\n            hit[\"record_nos\"].append(l[\"record_no\"])\n            hit[\"cites\"].append({\"record_no\": l[\"record_no\"], \"excerpt\": l[\"excerpt\"]})\n            hit[\"_taken\"].add(l[\"record_no\"])\n            continue\n        l = {**l, \"record_nos\": [l[\"record_no\"]], \"cites\": [{\"record_no\": l[\"record_no\"], \"excerpt\": l[\"excerpt\"]}], \"_taken\": set()}\n        seen.setdefault(key, []).append(l)\n        out.append(l)\n    for l in out:\n        l.pop(\"_taken\")\n    return out\n\n\ndef _sum(lines, kind):\n    vals = [l[kind][\"cents\"] for l in lines if l.get(kind) and l[kind][\"cents\"] is not None]\n    return sum(vals) if vals else None\n\n\ndef _tot(cents):\n    return {\"cents\": cents, \"usd\": fmt(cents)}\n\n\ndef analyze(records: list) -> dict:\n    \"\"\"The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O.\"\"\"\n    recs = [r for r in records if not r.get(\"duplicate_of\")]\n    lines, stated_by_rec, eobs, lop, excluded, balfwds, rec_form, checks = [], {}, [], [], [], {}, {}, []\n    for r in recs:\n        body = r.get(\"excerpt\") or r.get(\"text\") or \"\"\n        ls = body.split(\"\\n\")\n        form = form_of(r)\n        rec_form[r[\"n\"]] = form\n        if form == \"ledger_table\":\n            got, st, bf = _ledger_table(r, ls)\n            lines += got\n            stated_by_rec[r[\"n\"]], balfwds[r[\"n\"]] = st, bf\n        elif form == \"ledger_text\":\n            got, st = _ledger_text(r, body)\n            lines += got\n            stated_by_rec[r[\"n\"]] = st\n        elif form == \"cms1500\":\n            got, st = _cms1500(r, ls)\n            lines += got\n            stated_by_rec[r[\"n\"]] = st\n        elif form == \"ub04\":\n            got, st, rates = _ub04(r, ls)\n            lines += got\n            excluded += rates\n            stated_by_rec[r[\"n\"]] = st\n        elif form == \"eob\":\n            eobs.append(_eob(r, ls))\n        if form in (\"ledger_table\", \"ledger_text\"):     # a statement's fee-schedule line is a rate and carries no date of service\n            for a in A.find_amounts(body):\n                if a[\"cents\"] is not None and A.classify(body, a, source=r.get(\"source\")) == \"rate\":\n                    excluded.append({\"record_no\": r[\"n\"], \"kind\": \"rate\", \"why\": \"A rate (per visit, per unit) is a price, not a charge.\",\n                                     \"figure\": {\"text\": a[\"raw\"], \"cents\": a[\"cents\"], \"usd\": fmt(a[\"cents\"])}, \"excerpt\": body[max(body.rfind(\"\\n\", 0, a[\"start\"]) + 1, 0):(body.find(\"\\n\", a[\"end\"]) if body.find(\"\\n\", a[\"end\"]) >= 0 else len(body))].strip()})\n        lop += _lop_lien(r)\n    for e in eobs:\n        pass\n    # statements without a table that mention a rate in prose: classify each remaining sentence (ledger_text handled above)\n    for ln in lines:\n        ln[\"provider\"] = _provider(next(r for r in recs if r[\"n\"] == ln[\"record_no\"]))\n    for ex in excluded:\n        ex[\"provider\"] = _provider(next(r for r in recs if r[\"n\"] == ex[\"record_no\"]))\n    lines = _merge_duplicates(lines)\n    # per-line checks (running-balance steps follow the order printed within each record)\n    prev = {}\n    for l in lines:\n        n = l[\"record_no\"]\n        bf = balfwds.get(n)\n        if n not in prev:\n            prev[n] = bf[\"cents\"] if bf else None\n        l[\"checks\"] = _checks_for_line(l, prev[n])\n        prev[n] = l[\"balance\"][\"cents\"] if l.get(\"balance\") and l[\"balance\"][\"cents\"] is not None else prev[n]\n    for i, l in enumerate(lines, 1):\n        l[\"id\"] = f\"b{i}\"\n        l[\"kind\"] = (\"reversal\" if (l[\"billed\"] and (l[\"billed\"][\"cents\"] or 0) < 0) or (l[\"billed\"] and _VOID.search(l[\"description\"] or \"\")) else\n                     \"charge\" if l[\"billed\"] else\n                     \"payment\" if l[\"paid\"] else\n                     \"adjustment\" if l[\"adjustment\"] else\n                     \"balance_only\" if l[\"balance\"] else \"unclear\")\n        l[\"negotiated\"] = bool(l[\"adjustment\"] and _NEGOTIATED.search(l[\"description\"] or \"\"))\n        if l[\"form\"] == \"ledger\" and l[\"billed\"] and not l[\"dos\"] and rec_form.get(l[\"record_no\"]) == \"ledger_table\":\n            l[\"checks\"].append(\"NO_DATE_OF_SERVICE\")\n    # providers\n    by_prov = {}\n    for l in lines:\n        by_prov.setdefault(_norm(l[\"provider\"]), {\"provider\": l[\"provider\"], \"lines\": []})[\"lines\"].append(l)\n    providers = []\n    for key, p in by_prov.items():\n        ls = p[\"lines\"]\n        ledger = [l for l in ls if l[\"form\"] == \"ledger\"]\n        claim = [l for l in ls if l[\"form\"] != \"ledger\"]\n        basis = ledger or claim\n        pchecks = []\n        nego = [l for l in basis if l[\"negotiated\"]]\n        adj_lines = [l for l in basis if not l[\"negotiated\"]]\n        rec_nos = sorted({n for l in ls for n in l[\"record_nos\"]})\n        stated = {}\n        for n in rec_nos:\n            for k, v in (stated_by_rec.get(n) or {}).items():\n                stated.setdefault(k, []).append(v)\n        # one stated figure per kind is compared; with several statements the latest-in-file one is shown and all are listed\n        comp = {}\n        for kind in (\"billed\", \"paid\", \"adjustment\", \"balance\"):\n            comp[kind] = stated.get(kind, [None])[-1] if stated.get(kind) else None\n        billed, paid, adj = _sum(basis, \"billed\"), _sum(basis, \"paid\"), _sum(adj_lines, \"adjustment\")\n        unclear = [l for l in basis if l[\"unclear\"]]\n        if comp[\"billed\"] and billed is not None and comp[\"billed\"][\"cents\"] is not None and comp[\"billed\"][\"cents\"] != billed:\n            pchecks.append({\"code\": \"LEDGER_TOTAL_MISMATCH\" if basis is ledger else \"CLAIM_TOTAL_MISMATCH\", \"field\": \"billed\", \"stated\": comp[\"billed\"], \"computed\": _tot(billed)})\n        if comp[\"paid\"] and paid is not None and basis is ledger and comp[\"paid\"][\"cents\"] is not None and comp[\"paid\"][\"cents\"] != paid:\n            pchecks.append({\"code\": \"LEDGER_TOTAL_MISMATCH\", \"field\": \"paid\", \"stated\": comp[\"paid\"], \"computed\": _tot(paid)})\n        if comp[\"adjustment\"] and basis is ledger and comp[\"adjustment\"][\"cents\"] is not None and comp[\"adjustment\"][\"cents\"] != (adj or 0) + (_sum(nego, \"adjustment\") or 0):\n            pchecks.append({\"code\": \"LEDGER_TOTAL_MISMATCH\", \"field\": \"adjustment\", \"stated\": comp[\"adjustment\"], \"computed\": _tot((adj or 0) + (_sum(nego, \"adjustment\") or 0))})\n        if comp[\"balance\"] and comp[\"balance\"][\"cents\"] is not None and billed is not None and basis is ledger and not unclear:\n            derived = billed - (paid or 0) - ((adj or 0) + (_sum(nego, \"adjustment\") or 0))\n            if derived != comp[\"balance\"][\"cents\"]:\n                pchecks.append({\"code\": \"LEDGER_BALANCE_MISMATCH\", \"field\": \"balance\", \"stated\": comp[\"balance\"], \"computed\": _tot(derived)})\n        if ledger and claim:\n            cb = _sum(claim, \"billed\")\n            if cb is not None and billed is not None and cb != billed:\n                pchecks.append({\"code\": \"CLAIM_LEDGER_BILLED_MISMATCH\", \"field\": \"billed\", \"stated\": _tot(cb), \"computed\": _tot(billed)})\n        for c in pchecks:\n            c[\"message\"] = CHECKS[c[\"code\"]]\n        providers.append({\n            \"provider\": p[\"provider\"], \"record_nos\": rec_nos,\n            \"basis\": \"itemized_ledger\" if ledger else \"claim_form\",\n            \"billed\": _tot(billed), \"adjustment\": _tot(adj), \"paid\": _tot(paid),\n            \"negotiated_reductions\": _tot(_sum(nego, \"adjustment\")),\n            \"balance\": comp[\"balance\"], \"stated_totals\": {k: v for k, v in comp.items() if v},\n            \"complete\": not unclear, \"unclear_lines\": len(unclear),\n            \"line_count\": len(basis), \"claim_lines_not_totaled\": len(claim) if ledger else 0,\n            \"checks\": pchecks, \"lines\": ls})\n    # EOB cross-checks against the matching provider's ledger lines\n    payer = []\n    for e in eobs:\n        ledger_p = next((p for p in providers if p[\"basis\"] == \"itemized_ledger\" and (_norm(p[\"provider\"]) in _norm(e[\"provider\"]) or _norm(e[\"provider\"]) in _norm(p[\"provider\"]))), None)\n        e[\"matched_provider\"] = ledger_p[\"provider\"] if ledger_p else None\n        e[\"not_added_note\"] = \"The EOB restates the provider's charge; its amounts are never added to the charges.\"\n        e[\"checks\"] = []\n        if ledger_p:\n            for el in e[\"lines\"]:\n                led = [l for l in ledger_p[\"lines\"] if l[\"form\"] == \"ledger\" and _norm(l[\"code\"]) == _norm(el[\"service\"]) and\n                       ((l[\"dos_iso\"] and l[\"dos_iso\"] == el[\"dos_iso\"]) or _norm(l[\"dos\"]) == _norm(el[\"dos\"]))]\n                if not led or not el.get(\"billed\"):\n                    continue\n                lb, lp = _sum(led, \"billed\"), _sum(led, \"paid\") or 0\n                cites = [{\"record_no\": el[\"record_no\"], \"excerpt\": el[\"excerpt\"]}] + [c for l in led for c in l[\"cites\"]]\n                if lb is not None and lb != el[\"billed\"][\"cents\"]:\n                    e[\"checks\"].append({\"code\": \"LEDGER_EOB_BILLED_MISMATCH\", \"dos\": el[\"dos\"], \"service\": el[\"service\"], \"ledger\": _tot(lb), \"eob\": el[\"billed\"], \"cites\": cites})\n                if el.get(\"plan_paid\") and lp != el[\"plan_paid\"][\"cents\"]:\n                    e[\"checks\"].append({\"code\": \"LEDGER_EOB_PAID_MISMATCH\", \"dos\": el[\"dos\"], \"service\": el[\"service\"], \"ledger\": _tot(lp), \"eob\": el[\"plan_paid\"], \"cites\": cites})\n        for c in e[\"checks\"]:\n            c[\"message\"] = CHECKS[c[\"code\"]]\n        payer.append(e)\n    for i, x in enumerate(lop, 1):\n        x[\"id\"] = f\"l{i}\"\n    for i, x in enumerate(excluded, 1):\n        x[\"id\"] = f\"x{i}\"\n    allc = [c for p in providers for c in p[\"checks\"]] + [c for e in payer for c in e[\"checks\"]]\n    line_flags = [{\"code\": c, \"line_id\": l[\"id\"], \"provider\": l[\"provider\"], \"message\": CHECKS[c], \"excerpt\": l[\"excerpt\"]} for p in providers for l in p[\"lines\"] for c in l[\"checks\"]]\n    for p in providers:\n        for l in p[\"lines\"]:\n            l.pop(\"provider\", None)\n    found = bool(providers or payer or lop)\n    return {\n        \"status\": \"none_found\" if not found else (\"partial_unclear\" if any(not p[\"complete\"] for p in providers) else \"analyzed\"),\n        \"providers\": providers, \"payer_reports\": payer, \"lop_lien\": lop, \"excluded\": excluded,\n        \"checks\": allc, \"line_flags\": line_flags,\n        \"totals\": {\"billed\": _tot(sum(p[\"billed\"][\"cents\"] or 0 for p in providers)) if providers else _tot(None),\n                   \"adjustment\": _tot(sum(p[\"adjustment\"][\"cents\"] or 0 for p in providers)) if providers else _tot(None),\n                   \"paid\": _tot(sum(p[\"paid\"][\"cents\"] or 0 for p in providers)) if providers else _tot(None),\n                   \"provider_count\": len(providers), \"not_for_letter\": True},\n        \"rules\": RULES}\n\n\ndef verify_citations(analysis: dict, records: list) -> list:\n    \"\"\"[] when every line's excerpt is a verbatim substring of a cited record and every figure text appears in its excerpt; else the failures.\n    Run in tests and by the API before a response leaves: a line that fails is dropped from the response, never shown uncited.\"\"\"\n    text_of = {r[\"n\"]: (r.get(\"text\") or \"\") + \"\\n\" + (r.get(\"excerpt\") or \"\") for r in records}\n    bad = []\n    for p in analysis[\"providers\"]:\n        for l in p[\"lines\"]:\n            for c in l[\"cites\"]:\n                if c[\"excerpt\"] not in text_of.get(c[\"record_no\"], \"\"):\n                    bad.append({\"line\": l[\"id\"], \"reason\": \"excerpt_not_verbatim\"})\n            for k in (\"billed\", \"adjustment\", \"paid\", \"balance\"):\n                if l.get(k) and l[k][\"text\"].lstrip(\"-\") not in l[\"excerpt\"] and l[k][\"text\"] not in l[\"excerpt\"]:\n                    bad.append({\"line\": l[\"id\"], \"reason\": f\"{k}_not_in_excerpt\"})\n    for x in analysis[\"lop_lien\"] + analysis[\"excluded\"]:\n        if x[\"excerpt\"] not in text_of.get(x[\"record_no\"], \"\") or x[\"figure\"][\"text\"] not in x[\"excerpt\"]:\n            bad.append({\"line\": x[\"id\"], \"reason\": \"excerpt_not_verbatim\"})\n    return bad\n\n\ndef for_case(conn, case_id: str) -> dict:\n    from app.backend import store      # imported here so unit tests of the pure functions need no database\n    recs = store.load_records(conn, case_id)\n    out = analyze(recs)\n    failures = verify_citations(out, recs)\n    if failures:                       # fail closed: an uncited figure is never shown\n        bad = {f[\"line\"] for f in failures}\n        for p in out[\"providers\"]:\n            p[\"lines\"] = [l for l in p[\"lines\"] if l[\"id\"] not in bad]\n        out[\"lop_lien\"] = [x for x in out[\"lop_lien\"] if x[\"id\"] not in bad]\n        out[\"excluded\"] = [x for x in out[\"excluded\"] if x[\"id\"] not in bad]\n        out[\"status\"] = \"partial_unclear\"\n    return out\n\n\ndef add_routes(app, *, conn, get_case):\n    @app.get(\"/api/cases/{token}/billing\")\n    def billing_get(token: str):\n        c = conn()\n        try:\n            get_case(c, token)\n            return {\"billing\": for_case(c, token)}\n        finally:\n            c.close()\n"
}
````

### User / tool · 2026-11-02T04:21:14.442Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/billing.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:00.144Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_billing.py",
 "content": "\"\"\"Billing analysis (T-083, D-042): code-only, every figure cited, nothing totaled that is not stated. SYNTHETIC ledgers from research/record-formats.md.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import billing as B\nfrom app.backend.api import create_app\n\nLEDGER = \"\"\"SYNTHETIC RECORD\nLarkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026\nPatient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP\nDOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00\n06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00\n06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00\n06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00\n06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00\n06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00\n07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00\n                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00\nFee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.\"\"\"\n\nEOB = \"\"\"SYNTHETIC RECORD - THIS IS NOT A BILL\nQuoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026\nMember: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091\nProvider: Larkspur Hollow Physical Therapy (SYNTHETIC)\nDOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES\n06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45\n06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45\n06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97\nTOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00\nCO-97: payment included in allowance for another service.\"\"\"\n\nCMS_CLEAN = \"\"\"SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS\n24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI\n    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001\n    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001\n    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001\n25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00\n33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142\"\"\"\n\nCMS_OCR = \"\"\"SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS\n24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001\n    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001\n    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001\n    060126 060326 11 97014 A 9000 3 SYN-NPI-0001\n    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001\n28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00\"\"\"\n\nUB_ROOM = \"\"\"SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS\n1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111\n42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED\n0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00\n0450    EMERGENCY ROOM                               091526        1          1,975.00\n0250    PHARMACY                                     091526       14            412.75\n0300    LABORATORY                                   091526        6            688.00\n0320    DX X-RAY                                     091526        2            540.00\n0001    TOTAL                                        092226                   9,165.75\n67 S42.201A   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)\"\"\"\n\nPROSE = (\"Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; \"\n         \"total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.\")\n\nLOP = (\"Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction \"\n       \"of the account. Please send an itemized statement.\")\n\n\ndef rec(n, source, text, **kw):\n    return {\"n\": n, \"source\": source, \"excerpt\": text, \"text\": text, **kw}\n\n\ndef one(records):\n    out = B.analyze(records)\n    assert B.verify_citations(out, records) == []\n    return out\n\n\ndef provider(out, name):\n    return next(p for p in out[\"providers\"] if p[\"provider\"].startswith(name))\n\n\n# ------------------------------------------------------------------ itemized ledger\ndef test_ledger_lines_parse_to_four_figures_each_cited():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy (SYNTHETIC), itemized statement\", LEDGER)]\n    p = provider(one(r), \"Larkspur\")\n    ls = p[\"lines\"]\n    assert [l[\"code\"] for l in ls] == [\"97162\", \"97110\", \"97140\", \"97014\", \"97140\", \"97140\", \"ADJ\"]\n    first = ls[0]\n    assert (first[\"billed\"][\"cents\"], first[\"balance\"][\"cents\"], first[\"paid\"], first[\"adjustment\"]) == (21000, 21000, None, None)\n    assert first[\"dos\"] == \"05/27/26\" and first[\"dos_iso\"] == \"2026-05-27\" and first[\"posted\"] == \"05/28/26\"\n    assert first[\"cites\"] == [{\"record_no\": 1, \"excerpt\": first[\"excerpt\"]}] and first[\"excerpt\"] in LEDGER\n    adj = ls[-1]\n    assert adj[\"adjustment\"][\"cents\"] == 4500 and adj[\"adjustment\"][\"text\"] == \"45.00-\" and adj[\"balance\"][\"cents\"] == 40000 and adj[\"kind\"] == \"adjustment\"\n\n\ndef test_void_nets_and_running_balance_is_never_summed():\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER)]), \"Larkspur\")\n    void = next(l for l in p[\"lines\"] if \"VOID\" in l[\"description\"])\n    assert void[\"billed\"][\"cents\"] == -7000 and void[\"kind\"] == \"reversal\"\n    assert p[\"billed\"][\"cents\"] == 44500           # 210+130+70+35-70+70, not the sum of the running balances\n    assert p[\"adjustment\"][\"cents\"] == 4500 and p[\"paid\"][\"cents\"] is None\n    assert p[\"balance\"][\"cents\"] == 40000          # the statement's own BALANCE DUE\n    assert p[\"checks\"] == [] and p[\"complete\"] and not any(f[\"code\"] == \"BALANCE_STEP_MISMATCH\" for f in one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER)])[\"line_flags\"])\n\n\ndef test_fee_schedule_rate_is_listed_and_never_a_charge():\n    out = one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER)])\n    assert [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in out[\"excluded\"]] == [(6500, \"rate\")]\n    assert \"Fee schedule\" in out[\"excluded\"][0][\"excerpt\"]\n    assert 6500 not in [l[\"billed\"][\"cents\"] for l in provider(out, \"Larkspur\")[\"lines\"] if l[\"billed\"]]\n\n\ndef test_stated_total_mismatch_is_flagged_not_corrected():\n    bad = LEDGER.replace(\"TOTAL CHARGES 445.00\", \"TOTAL CHARGES 455.00\")\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", bad)]), \"Larkspur\")\n    assert p[\"billed\"][\"cents\"] == 44500           # the lines, not the printed total\n    c = p[\"checks\"][0]\n    assert c[\"code\"] == \"LEDGER_TOTAL_MISMATCH\" and c[\"stated\"][\"cents\"] == 45500 and c[\"computed\"][\"cents\"] == 44500\n\n\ndef test_running_balance_step_mismatch_is_flagged_on_the_line():\n    bad = LEDGER.replace(\"410.00\\n\", \"415.00\\n\", 1)\n    out = one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", bad)])\n    assert [f[\"code\"] for f in out[\"line_flags\"] if f[\"code\"] == \"BALANCE_STEP_MISMATCH\"] != []\n\n\ndef test_unreadable_figure_is_listed_with_no_value_and_left_out_of_totals():\n    txt = LEDGER.replace(\"130.00    \", \"13O.00    \", 1).replace(\"TOTAL CHARGES 445.00  \", \"\")\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", txt)]), \"Larkspur\")\n    bad = next(l for l in p[\"lines\"] if l[\"code\"] == \"97110\")\n    assert bad[\"billed\"] is None and bad[\"unclear\"] and \"LINE_UNCLEAR\" in bad[\"checks\"]\n    assert p[\"billed\"][\"cents\"] == 31500 and p[\"complete\"] is False and p[\"unclear_lines\"] == 1\n\n\ndef test_extra_decimals_are_never_rounded():\n    txt = LEDGER.replace(\"130.00\", \"130.005\")\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", txt)]), \"Larkspur\")\n    assert next(l for l in p[\"lines\"] if l[\"code\"] == \"97110\")[\"billed\"] is None\n\n\ndef test_duplicate_statement_counts_once_and_cites_both_records():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, \"Larkspur Hollow Physical Therapy, statement (copy)\", LEDGER)]\n    p = provider(one(r), \"Larkspur\")\n    assert p[\"billed\"][\"cents\"] == 44500\n    assert all(l[\"record_nos\"] == [1, 2] for l in p[\"lines\"]) and p[\"lines\"][0][\"cites\"][1][\"record_no\"] == 2\n\n\ndef test_two_identical_lines_inside_one_record_both_count():\n    twice = LEDGER.replace(\"06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00\",\n                           \"06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00\\n\"\n                           \"06/10/26  06/11/26  97014  E-stim unattended              35.00                         480.00\")\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", twice)]), \"Larkspur\")\n    assert sum(1 for l in p[\"lines\"] if l[\"code\"] == \"97014\") == 2\n\n\ndef test_balance_forward_is_not_a_charge():\n    txt = LEDGER.replace(\"05/27/26  05/28/26  97162\", \"Bal fwd                                                                          100.00\\n05/27/26  05/28/26  97162\", 1) \\\n                .replace(\"PT eval moderate complexity   210.00                         210.00\", \"PT eval moderate complexity   210.00                         310.00\")\n    p = provider(one([rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", txt)]), \"Larkspur\")\n    assert p[\"billed\"][\"cents\"] == 44500 and all(\"Bal\" not in (l[\"description\"] or \"\") for l in p[\"lines\"])\n\n\ndef test_payments_adjustments_in_their_own_columns_by_position():\n    txt = \"\"\"DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n03/01/26  03/02/26  99213  Office visit                  150.00                         150.00\n03/15/26  03/15/26  PMT    Ins pmt - Ck #SYN-1043                    100.00             50.00\n03/15/26  03/15/26  CO45   Contractual adj                                   20.00-      30.00\n04/20/26  04/20/26  ATY    Atty reduction                                    10.00-      20.00\n                     TOTAL CHARGES 150.00  TOTAL PMTS 100.00  TOTAL ADJ (30.00)  BALANCE DUE 20.00\"\"\"\n    p = provider(one([rec(1, \"Medlark Clinic, statement\", txt)]), \"Medlark\")\n    assert (p[\"billed\"][\"cents\"], p[\"paid\"][\"cents\"], p[\"adjustment\"][\"cents\"], p[\"negotiated_reductions\"][\"cents\"]) == (15000, 10000, 2000, 1000)\n    assert p[\"checks\"] == []                       # stated adjustments 30.00 = contractual 20.00 + attorney reduction 10.00; balance 150-100-30 = 20\n\n\ndef test_ledger_prose_statement_parses_and_checks_its_own_total():\n    out = one([rec(9, \"Fennimoor Spine Clinic, itemized ledger\", PROSE)])\n    p = provider(out, \"Fennimoor\")\n    assert [l[\"billed\"][\"cents\"] for l in p[\"lines\"] if l[\"billed\"]] == [25000, 18000, 231000]\n    assert p[\"billed\"][\"cents\"] == 274000 and p[\"paid\"][\"cents\"] == 30000 and p[\"adjustment\"][\"cents\"] == 27400\n    assert p[\"balance\"][\"cents\"] == 216600 and p[\"checks\"] == []\n    assert out[\"lop_lien\"] == []                   # \"held under letter of protection\" has no amount\n\n\n# ------------------------------------------------------------------ totals by provider\ndef test_totals_are_per_provider_and_only_of_stated_figures():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, \"Fennimoor Spine Clinic, itemized ledger\", PROSE)]\n    out = one(r)\n    assert sorted((p[\"provider\"], p[\"billed\"][\"cents\"]) for p in out[\"providers\"]) == [(\"Fennimoor Spine Clinic\", 274000), (\"Larkspur Hollow Physical Therapy\", 44500)]\n    assert out[\"totals\"][\"billed\"][\"cents\"] == 318500 and out[\"totals\"][\"not_for_letter\"] is True\n\n\ndef test_nothing_found_for_a_clinical_record():\n    out = one([rec(1, \"Dr. Lee, progress note\", \"Neck pain 5/10 after the collision. Plan: continue therapy.\")])\n    assert out[\"status\"] == \"none_found\" and out[\"providers\"] == [] and out[\"totals\"][\"billed\"][\"cents\"] is None\n\n\n# ------------------------------------------------------------------ LOP / lien amounts are separate\ndef test_lop_and_lien_amounts_are_listed_separately_and_never_totaled():\n    r = [rec(1, \"Fennimoor Spine Clinic, itemized ledger\", PROSE), rec(2, \"Pellingham and Rook PLLC, correspondence (letter of protection)\", LOP)]\n    out = one(r)\n    assert [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in out[\"lop_lien\"]] == [(486000, \"asserted_balance\"), (310000, \"reduction\")]\n    assert all(x[\"in_totals\"] is False for x in out[\"lop_lien\"])\n    assert provider(out, \"Fennimoor\")[\"billed\"][\"cents\"] == 274000\n\n\ndef test_atty_reduction_on_a_ledger_is_not_a_plain_adjustment():\n    txt = \"Itemized ledger. Therapy charge $1,000.00. Balance reduced to $600.00 in full satisfaction. Balance due $1,000.00.\"\n    out = one([rec(1, \"Medlark Clinic, itemized ledger\", txt)])\n    assert [x[\"figure\"][\"cents\"] for x in out[\"lop_lien\"]] == [60000]\n    assert provider(out, \"Medlark\")[\"billed\"][\"cents\"] == 100000\n\n\n# ------------------------------------------------------------------ CMS-1500 (implied decimals), UB-04 (rate on the charge line), EOB\ndef test_cms1500_boxes_are_implied_cents_and_checked_against_item_28():\n    p = provider(one([rec(1, \"Brightwater Spine & Wellness, CMS-1500\", CMS_CLEAN)]), \"Brightwater\")\n    assert [l[\"billed\"][\"cents\"] for l in p[\"lines\"]] == [8500, 8500, 8500, 9000, 4500]\n    assert p[\"billed\"][\"cents\"] == 39000 and p[\"stated_totals\"][\"billed\"][\"cents\"] == 39000 and p[\"checks\"] == []\n    assert p[\"stated_totals\"][\"paid\"][\"cents\"] == 0 and p[\"basis\"] == \"claim_form\"\n\n\ndef test_cms1500_ocr_text_never_reads_8500_as_dollars():\n    p = provider(one([rec(1, \"Brightwater Spine & Wellness, CMS-1500 (OCR)\", CMS_OCR)]), \"Brightwater\")\n    cents = [l[\"billed\"][\"cents\"] if l[\"billed\"] else None for l in p[\"lines\"]]\n    assert cents[:2] == [8500, 8500] and cents[3] == 9000          # 8500 -> $85.00, 9000 -> $90.00\n    assert cents[4] is None and \"45 OO\" in p[\"lines\"][4][\"unclear\"]    # OCR letters: listed, not totaled\n    assert p[\"lines\"][2][\"billed\"][\"cents\"] == 8500                # O in the date does not matter\n    assert p[\"billed\"][\"cents\"] == 8500 * 3 + 9000 - 0 and p[\"complete\"] is False\n    assert p[\"checks\"][0][\"code\"] == \"CLAIM_TOTAL_MISMATCH\"        # 39000 stated vs the lines that could be read\n\n\ndef test_ub04_rate_on_the_charge_line_is_not_a_charge_and_0001_is_not_added():\n    out = one([rec(1, \"Saltmarrow General Hospital, UB-04\", UB_ROOM)])\n    p = provider(out, \"Saltmarrow\")\n    assert p[\"billed\"][\"cents\"] == 916575          # 5550.00 + 1975.00 + 412.75 + 688.00 + 540.00, not 20,181.50\n    assert p[\"stated_totals\"][\"billed\"][\"cents\"] == 916575 and p[\"checks\"] == []\n    assert [(x[\"figure\"][\"cents\"], x[\"kind\"]) for x in out[\"excluded\"]] == [(185000, \"rate\")]\n    assert all(l[\"code\"] != \"0001\" for l in p[\"lines\"])\n    assert next(l for l in p[\"lines\"] if l[\"code\"] == \"0120\")[\"billed\"][\"cents\"] == 555000\n\n\ndef test_eob_is_never_added_and_a_ledger_eob_paid_mismatch_is_raised():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)]\n    out = one(r)\n    assert provider(out, \"Larkspur\")[\"billed\"][\"cents\"] == 44500          # EOB's 235.00 billed is not added\n    assert len(out[\"providers\"]) == 1\n    e = out[\"payer_reports\"][0]\n    assert e[\"matched_provider\"].startswith(\"Larkspur\") and len(e[\"lines\"]) == 3\n    l140 = next(x for x in e[\"lines\"] if x[\"service\"] == \"97140\")\n    assert l140[\"plan_paid\"][\"cents\"] == 1600 and l140[\"codes\"] == \"PR-1, PR-2, CO-45\"\n    mism = [(c[\"code\"], c[\"service\"], c[\"ledger\"][\"cents\"], c[\"eob\"][\"cents\"]) for c in e[\"checks\"]]\n    assert mism == [(\"LEDGER_EOB_PAID_MISMATCH\", \"97140\", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment\n    assert len(e[\"checks\"][0][\"cites\"]) >= 3 and e[\"checks\"][0][\"cites\"][0][\"record_no\"] == 2\n\n\ndef test_claim_form_and_ledger_for_the_same_provider_are_not_double_counted():\n    claim = CMS_CLEAN\n    r = [rec(1, \"Brightwater Spine & Wellness, itemized ledger\", \"Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00.\"),\n         rec(2, \"Brightwater Spine & Wellness, CMS-1500\", claim)]\n    p = provider(one(r), \"Brightwater\")\n    assert p[\"basis\"] == \"itemized_ledger\" and p[\"billed\"][\"cents\"] == 39000 and p[\"claim_lines_not_totaled\"] == 5 and p[\"checks\"] == []\n\n\n# ------------------------------------------------------------------ citations, API\ndef test_verify_citations_catches_an_uncited_line():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER)]\n    out = B.analyze(r)\n    out[\"providers\"][0][\"lines\"][0][\"cites\"][0][\"excerpt\"] = \"not in the record\"\n    assert B.verify_citations(out, r)[0][\"reason\"] == \"excerpt_not_verbatim\"\n\n\n@pytest.fixture\ndef client(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    return TestClient(create_app(str(tmp_path / \"x.sqlite\"), static_dir=str(tmp_path)))\n\n\ndef test_billing_route_for_a_pasted_case(client):\n    text = (\"=== Record 1 ===\\nDate: 2026-06-15\\nSource: Fennimoor Spine Clinic, itemized ledger\\nExcerpt: \\\"\" + PROSE + \"\\\"\\n\\n\"\n            \"=== Record 2 ===\\nDate: 2026-03-26\\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\\nExcerpt: \\\"\" + LOP + \"\\\"\\n\")\n    tok = client.post(\"/api/cases\", json={\"text\": text}).json()[\"token\"]\n    r = client.get(f\"/api/cases/{tok}/billing\")\n    assert r.status_code == 200\n    b = r.json()[\"billing\"]\n    assert b[\"providers\"][0][\"billed\"][\"cents\"] == 274000\n    assert [x[\"figure\"][\"cents\"] for x in b[\"lop_lien\"]] == [486000, 310000]\n    assert client.get(\"/api/cases/nope/billing\").status_code == 404\n"
}
````

### User / tool · 2026-11-02T04:22:00.214Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_billing.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:00.625Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_billing.py -x 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:01.311Z

**tool result**
````
.....F
=================================== FAILURES ===================================
____ test_unreadable_figure_is_listed_with_no_value_and_left_out_of_totals _____

    def test_unreadable_figure_is_listed_with_no_value_and_left_out_of_totals():
        txt = LEDGER.replace("130.00    ", "13O.00    ", 1).replace("TOTAL CHARGES 445.00  ", "")
        p = provider(one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", txt)]), "Larkspur")
        bad = next(l for l in p["lines"] if l["code"] == "97110")
>       assert bad["billed"] is None and bad["unclear"] and "LINE_UNCLEAR" in bad["checks"]
E       assert (None is None and [])

tests/unit/test_billing.py:132: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_unreadable_figure_is_listed_with_no_value_and_left_out_of_totals
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 5 passed in 0.32s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:09.164Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport re\np=\"app/backend/billing.py\"\ns=open(p).read()\ns=s.replace('''_FIG = r\"\\\\(?-?\\\\$?(?:\\\\d{1,3}(?:,\\\\d{3})+|\\\\d+)\\\\.\\\\d+\\\\)?-?\"\n_NUM = re.compile(rf\"(?<![\\\\w/.]){_FIG}(?![\\\\w/]|\\\\.\\\\d)\")''','''_D = r\"[0-9OolISB]\"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped\n_FIG = rf\"\\\\(?-?\\\\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\\\\.{_D}+\\\\)?-?\"\n_NUM = re.compile(rf\"(?<![\\\\w/.])(?=[^\\\\s]*[0-9]){_FIG}(?![\\\\w/]|\\\\.\\\\d)\")''')\ns=s.replace('digits = re.sub(r\"[()\\\\-$]\", \"\", token)\\n    cents = A.to_cents(digits) if re.search(r\"\\\\.\\\\d\\\\d\\\\Z\", digits) else None','digits = re.sub(r\"[()\\\\-$]\", \"\", token)\\n    cents = A.to_cents(digits) if re.fullmatch(r\"[\\\\d,]+\\\\.\\\\d\\\\d\", digits) else None')\nopen(p,\"w\").write(s)\nE\ngrep -n \"_D = \\|^_FIG\\|^_NUM\\|fullmatch(r\\\"\\[\" app/backend/billing.py; .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T04:22:09.929Z

**tool result**
````
38:_D = r"[0-9OolISB]"           # letters OCR confuses with digits are tolerated so a noisy figure is LISTED (cents None), never silently skipped
39:_FIG = rf"\(?-?\$?(?:{_D}{{1,3}}(?:,{_D}{{3}})+|{_D}+)\.{_D}+\)?-?"
40:_NUM = re.compile(rf"(?<![\w/.])(?=[^\s]*[0-9]){_FIG}(?![\w/]|\.\d)")
62:    cents = A.to_cents(digits) if re.fullmatch(r"[\d,]+\.\d\d", digits) else None
155:        code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
______ test_lop_and_lien_amounts_are_listed_separately_and_never_totaled _______

    def test_lop_and_lien_amounts_are_listed_separately_and_never_totaled():
        r = [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE), rec(2, "Pellingham and Rook PLLC, correspondence (letter of protection)", LOP)]
        out = one(r)
        assert [(x["figure"]["cents"], x["kind"]) for x in out["lop_lien"]] == [(486000, "asserted_balance"), (310000, "reduction")]
        assert all(x["in_totals"] is False for x in out["lop_lien"])
>       assert provider(out, "Fennimoor")["billed"]["cents"] == 274000
               ^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/unit/test_billing.py:204: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

out = {'status': 'analyzed', 'providers': [], 'payer_reports': [], 'lop_lien': [{'record_no': 2, 'provider': 'Pellingham and..._no': 2, 'provider': 'Pellingham and Rook PLLC', 'kind': 'reduction', 'label': 'Provider agrees to accept', ...}], ...}
name = 'Fennimoor'

    def provider(out, name):
>       return next(p for p in out["providers"] if p["provider"].startswith(name))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       StopIteration

tests/unit/test_billing.py:80: StopIteration
_____________________ test_billing_route_for_a_pasted_case _____________________

client = <starlette.testclient.TestClient object at 0x109844830>

    def test_billing_route_for_a_pasted_case(client):
        text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
                "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
>       tok = client.post("/api/cases", json={"text": text}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_billing.py:284: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_ledger_prose_statement_parses_and_checks_its_own_total
FAILED tests/unit/test_billing.py::test_totals_are_per_provider_and_only_of_stated_figures
FAILED tests/unit/test_billing.py::test_lop_and_lien_amounts_are_listed_separately_and_never_totaled
FAILED tests/unit/test_billing.py::test_billing_route_for_a_pasted_case - Key...
4 failed, 19 passed in 0.36s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:12.378Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nfrom tests.unit.test_billing import *\nr=rec(9,\"Fennimoor Spine Clinic, itemized ledger\",PROSE)\nprint(B.form_of(r))\nprint([PROSE[s:e] for s,e in B._segments(PROSE)])\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | grep -B5 \"KeyError\" | head; grep -n \"POST.*api/cases\\\"\" -A12 app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T04:22:13.444Z

**tool result**
````
ledger_table
['Itemized ledger, statement date 06/15/2026.', 'New patient exam charge $250.00;', 'x-ray charge $180.00;', 'treatment visits 1 through 14 charge $2,310.00;', 'total charges $2,740.00.', 'Payment received $300.00.', 'Adjustment (courtesy discount) -$274.00.', 'Balance due $2,166.00.', 'Account held under letter of protection.']
    def test_billing_route_for_a_pasted_case(client):
        text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
                "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
>       tok = client.post("/api/cases", json={"text": text}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_billing.py:284: KeyError
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:19.390Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"app/backend/billing.py\"\ns=open(p).read()\ns=s.replace('''        if _ROW.match(ln) or re.match(r\"\\\\s*TOTAL\\\\b\", ln, re.IGNORECASE):\n            continue\n        cols = {}''','''        if _ROW.match(ln) or re.match(r\"\\\\s*TOTAL\\\\b\", ln, re.IGNORECASE) or \"$\" in ln or not re.search(r\"\\\\S\\\\s{2,}\\\\S\", ln):\n            continue          # a header is a spaced-out row of column names: a sentence with a '$' figure is prose\n        cols = {}''')\nopen(p,\"w\").write(s)\nE\n.venv/bin/python - <<'E'\nfrom fastapi.testclient import TestClient\nimport os\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ[\"ZLAYT_MODE\"]=\"local\"\nfrom app.backend.api import create_app\nimport tempfile\nc=TestClient(create_app(tempfile.mktemp()))\nr=c.post(\"/api/cases\",json={\"text\":\"=== Record 1 ===\\nDate: 2026-06-15\\nSource: Fennimoor Spine Clinic, itemized ledger\\nExcerpt: \\\"Itemized ledger. Charge $5.00.\\\"\\n\"})\nprint(r.status_code,r.text[:300])\nE\nsed -n 53,72p memory/contracts/api.md | cut -c1-300"
}
````

### User / tool · 2026-11-02T04:22:19.781Z

**tool result**
````
403 {"error":{"code":"forbidden","message":"Local mode accepts loopback clients only.","detail":{}}}
`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view

## POST /api/cases
Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`.
```json
{ "name": "Rivera sample", "text": "SYNTHETIC — ...\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, ...\"\n...", "sample": false }
```
Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020).
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ingested", "source": "paste",
  "demo_mode": true, "record_count": 9, "split_method": "code",
  "records": [
    { "id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09",
      "date_status": "parsed", "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true,
      "char_start": 106, "char_end": 313,
      "text": "=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"" } ],
  "dates_to_confirm": [],
  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
  "warnings": [] }
```
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:21.561Z

**tool call — Bash**
````
{
 "command": "grep -n \"TestClient\\|client=\" tests/unit/test_multicase.py | head -5; grep -n \"def is_loopback_peer\" -A9 app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:22:21.659Z

**tool result**
````
81:def is_loopback_peer(request) -> bool:
82-    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
83-    host = request.client.host if request.client else None
84-    try:
85-        ip = ipaddress.ip_address(host)
86-    except (TypeError, ValueError):
87-        return False
88-    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback
89-
90-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:22.890Z

I don't need local mode; the billing route works in any mode. Drop ZLAYT_MODE; check demo-mode create restrictions though.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:24.516Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_multicase.py | head -40; .venv/bin/python - <<'E'\nfrom fastapi.testclient import TestClient\nimport os\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ[\"ZLAYT_MODE\"]=\"local\"\nfrom app.backend.api import create_app\nimport tempfile\nc=TestClient(create_app(tempfile.mktemp()),client=(\"127.0.0.1\",5000))\nr=c.post(\"/api/cases\",json={\"text\":\"=== Record 1 ===\\nDate: 2026-06-15\\nSource: Fennimoor Spine Clinic, itemized ledger\\nExcerpt: \\\"Itemized ledger. Charge $5.00.\\\"\\n\"})\nprint(r.status_code,r.text[:200])\nE"
}
````

### User / tool · 2026-11-02T04:22:24.894Z

**tool result**
````
"""T-050: many cases share one sqlite file; ids are short per case and never collide; delete_case touches only its own rows."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record


def seeded(conn, case, text):
    cid = DB.create_case(conn, text, now=1.0)
    PL.ingest_case(conn, cid, text, 1.0)
    return cid


def test_two_golden_cases_back_to_back_in_one_file(tmp_path):
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    a = seeded(conn, "sample", G.raw("sample"))
    b = seeded(conn, "case_01", G.raw("case_01_date_formats"))
    c = seeded(conn, "sample again", G.raw("sample"))
    ids = lambda cid: sorted(r["id"] for r in DB.list_items(conn, cid, "flag"))   # noqa: E731
    assert ids(a) == ids(c) and ids(a)                                              # same short ids in two cases
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (a,)).fetchone()[0] == 9
    assert conn.execute("SELECT count(*) FROM records WHERE case_id=?", (b,)).fetchone()[0] >= 8


def test_full_pipeline_twice_in_one_file(tmp_path):
    sums = golden_summaries()
    script = {"extract": lambda u: dict(summary=sums[which_record(u)[0]][0], excerpt=sums[which_record(u)[0]][1]),
              "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"}, "j3": {"verdict": "conflict", "reason_code": "NONE"},
              "j4": {"verdict": "agree", "reason_code": "NONE"}, "conflicts": {"flags": []}, "flags": {"flags": []}}
    conn = DB.connect(str(tmp_path / "m.sqlite"))
    outs = []
    for _ in range(2):
        cid = DB.create_case(conn, G.raw("sample"), now=1.0)
        outs.append((cid, PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(script), now=lambda: 1.0)))
    (a, oa), (b, ob) = outs
    assert [e["id"] for e in oa["entries"]] == [e["id"] for e in ob["entries"]] and len(oa["entries"]) == 9
    eid = oa["entries"][0]["id"]
    with pytest.raises(ValueError):                      # a bare id is ambiguous once two cases hold it
        DB.get_item(conn, eid)
409 {"error":{"code":"demo_mode_unsupported_input","message":"This demo only runs the recorded sample cases.","detail":{}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:27.301Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"tests/unit/test_billing.py\"\ns=open(p).read()\ns=s.replace('static_dir=str(tmp_path)))\\n\\n\\ndef test_billing_route','static_dir=str(tmp_path)), client=(\"127.0.0.1\", 5000))\\n\\n\\ndef test_billing_route')\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:28.047Z

**tool result**
````
......................F                                                  [100%]
=================================== FAILURES ===================================
_____________________ test_billing_route_for_a_pasted_case _____________________

client = <starlette.testclient.TestClient object at 0x10bacafc0>

    def test_billing_route_for_a_pasted_case(client):
        text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
                "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
>       tok = client.post("/api/cases", json={"text": text}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_billing.py:284: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_billing_route_for_a_pasted_case - Key...
1 failed, 22 passed in 0.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:30.879Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nfrom fastapi.testclient import TestClient\nimport os,tempfile\nos.environ[\"LLM_BACKEND\"]=\"fixture\"; os.environ[\"ZLAYT_MODE\"]=\"local\"\nfrom app.backend.api import create_app\nfrom tests.unit.test_billing import *\nc=TestClient(create_app(tempfile.mktemp()),client=(\"127.0.0.1\",5000))\ntext = (\"=== Record 1 ===\\nDate: 2026-06-15\\nSource: Fennimoor Spine Clinic, itemized ledger\\nExcerpt: \\\"\" + PROSE + \"\\\"\\n\\n\"\n            \"=== Record 2 ===\\nDate: 2026-03-26\\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\\nExcerpt: \\\"\" + LOP + \"\\\"\\n\")\nr=c.post(\"/api/cases\",json={\"text\":text}); print(r.status_code,r.text[:300])\nE"
}
````

### User / tool · 2026-11-02T04:22:31.312Z

**tool result**
````
409 {"error":{"code":"demo_mode_unsupported_input","message":"This demo only runs the recorded sample cases.","detail":{}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:33.147Z

**tool call — Bash**
````
{
 "command": "sed -n 60,80p app/backend/api.py; grep -n \"demo_mode\\b\" app/backend/api.py | head; grep -n \"ZLAYT_DEMO\\|DEMO\" tests/unit/test_multicase.py tests/unit/test_api_routes.py | head"
}
````

### User / tool · 2026-11-02T04:22:33.267Z

**tool result**
````
def library_cases() -> list:
    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
    evals/golden until the library exists. [{id, name, description, path}]"""
    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
    out = []
    for p in sorted(base.glob("*.txt")):
        meta = {}
        ej = p.with_name(p.stem + ".expected.json")
        if ej.exists():
            try:
                meta = json.loads(ej.read_text())
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


117:    def demo_mode():
212:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
251:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
275:        if demo_mode() and digest(text) not in allowed_hashes():
283:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
296:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
309:            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
345:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
347:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
370:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:34.765Z

**tool call — Bash**
````
{
 "command": "sed -n 112,125p app/backend/api.py; grep -rn \"ZLAYT_DEMO\\|DEMO_MODE\" tests/unit/*.py | head -5"
}
````

### User / tool · 2026-11-02T04:22:34.914Z

**tool result**
````
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:38.149Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"tests/unit/test_billing.py\"\ns=open(p).read()\ns=s.replace('''    tok = client.post(\"/api/cases\", json={\"text\": text}).json()[\"token\"]\n''','''    conn = DB.connect(client.app.state.db_path)             # demo mode refuses unrecorded text over HTTP, so the case is seeded directly (code-only ingest)\n    tok = DB.create_case(conn, text, now=1.0)\n    PL.ingest_case(conn, tok, text, 1.0)\n    conn.close()\n''')\ns=s.replace(\"from app.backend.api import create_app\\n\",\"from app.backend import pipeline as PL\\nfrom app.backend.api import create_app\\nfrom app.db import db as DB\\n\")\nopen(p,\"w\").write(s)\nE\nsed -n 494,498p app/backend/api.py; grep -n \"^from app.backend import\" app/backend/api.py"
}
````

### User / tool · 2026-11-02T04:22:38.289Z

**tool result**
````
            c.close()

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
    from app.backend import reclassify
    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:39.782Z

Others are adding hooks the same way. Smallest edit: one line after case_extras.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:40.991Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/api.py",
 "old_string": "    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\n",
 "new_string": "    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\n    from app.backend import billing\n    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\n"
}
````

### User / tool · 2026-11-02T04:22:41.077Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/api.py has been updated successfully.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:41.412Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:42.222Z

**tool result**
````
......................F                                                  [100%]
=================================== FAILURES ===================================
_____________________ test_billing_route_for_a_pasted_case _____________________

client = <starlette.testclient.TestClient object at 0x109b00590>

    def test_billing_route_for_a_pasted_case(client):
        text = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n\n"
                "=== Record 2 ===\nDate: 2026-03-26\nSource: Pellingham and Rook PLLC, correspondence (letter of protection)\nExcerpt: \"" + LOP + "\"\n")
        conn = DB.connect(client.app.state.db_path)             # demo mode refuses unrecorded text over HTTP, so the case is seeded directly (code-only ingest)
        tok = DB.create_case(conn, text, now=1.0)
        PL.ingest_case(conn, tok, text, 1.0)
        conn.close()
        r = client.get(f"/api/cases/{tok}/billing")
>       assert r.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404 Not Found]>.status_code

tests/unit/test_billing.py:291: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_billing.py::test_billing_route_for_a_pasted_case - ass...
1 failed, 22 passed in 0.38s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:51.718Z

**tool call — Bash**
````
{
 "command": "sed -n 128,150p app/backend/api.py; grep -n \"def get_case\" -A14 app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T04:22:51.858Z

**tool result**
````
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL

    def get_case(c, token):
        case = DB.get_case(c, token)
        if case is None:
            raise ApiError(404, "not_found", "No such case.")
        return case

    # -------------------------------------------------- errors / headers
    @app.exception_handler(ApiError)
    async def _api_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
138:    def get_case(c, token):
139-        case = DB.get_case(c, token)
140-        if case is None:
141-            raise ApiError(404, "not_found", "No such case.")
142-        return case
143-
144-    # -------------------------------------------------- errors / headers
145-    @app.exception_handler(ApiError)
146-    async def _api_error(_, e):
147-        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
148-
149-    @app.exception_handler(review.ReviewError)
150-    async def _review_error(_, e):
151-        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)
152-
--
305:    def get_case_view(token: str):
306-        c = conn()
307-        try:
308-            get_case(c, token)
309-            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
310-        finally:
311-            c.close()
312-
313-    @app.delete("/api/cases/{token}", status_code=204)
314-    def delete_case(token: str):
315-        c = conn()
316-        try:
317-            get_case(c, token)
318-            DB.delete_case(c, token)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:54.097Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nfrom tests.unit.test_billing import *\nimport tempfile,os\nos.environ[\"LLM_BACKEND\"]=\"fixture\"\nfrom fastapi.testclient import TestClient\napp=create_app(tempfile.mktemp())\nprint([r.path for r in app.routes if 'billing' in r.path], hasattr(app.state,'db_path'))\nc=TestClient(app,client=(\"127.0.0.1\",5000))\nconn=DB.connect(app.state.db_path); tok=DB.create_case(conn,\"x\",now=1.0); print(tok)\nprint(c.get(f\"/api/cases/{tok}/billing\").text)\nE"
}
````

### User / tool · 2026-11-02T04:22:54.548Z

**tool result**
````
['/api/cases/{token}/billing'] True
szCPXkv_llZyv7dn1A9YPw
{"error":{"code":"not_found","message":"No such case.","detail":{}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:22:57.897Z

**tool call — Bash**
````
{
 "command": "sed -i 's/tok = DB.create_case(conn, text, now=1.0)/tok = DB.create_case(conn, text, now=time.time())/; s/PL.ingest_case(conn, tok, text, 1.0)/PL.ingest_case(conn, tok, text, time.time())/; s/^import pytest$/import time\\n\\nimport pytest/' tests/unit/test_billing.py && .venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:22:58.010Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/unit/test_billing ...": undefined label 'ests/unit/test_billing.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:00.028Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"tests/unit/test_billing.py\"\ns=open(p).read()\ns=s.replace(\"tok = DB.create_case(conn, text, now=1.0)\",\"tok = DB.create_case(conn, text, now=time.time())\").replace(\"PL.ingest_case(conn, tok, text, 1.0)\",\"PL.ingest_case(conn, tok, text, time.time())\").replace(\"\\nimport pytest\\n\",\"\\nimport time\\n\\nimport pytest\\n\",1)\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T04:23:00.883Z

**tool result**
````
.......................                                                  [100%]
23 passed in 0.40s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:06.972Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\nimport time,tempfile\nfrom tests.unit.test_billing import *\nfrom app.backend import billing as B, store\ntext = \"=== Record 1 ===\\nDate: 2026-07-31\\nSource: Larkspur Hollow Physical Therapy, itemized statement\\nExcerpt: \\\"\\n\"+\"\\n\".join(LEDGER.split(\"\\n\")[3:])+\"\\n\\\"\\n\"\ntext2 = \"=== Record 1 ===\\nDate: 2026-07-31\\nSource: Larkspur Hollow Physical Therapy, itemized statement\\nExcerpt: \\\"\"+LEDGER.split(\"\\n\",3)[3]+\"\\\"\\n\"\nfor t in (text,text2):\n    conn=DB.connect(tempfile.mktemp()); tok=DB.create_case(conn,t,now=time.time()); PL.ingest_case(conn,tok,t,time.time())\n    recs=store.load_records(conn,tok)\n    print(repr(recs[0][\"excerpt\"][:120]))\n    o=B.for_case(conn,tok); print(o[\"status\"], [(p[\"provider\"],p[\"billed\"],p[\"lines\"].__len__(),p[\"checks\"]) for p in o[\"providers\"]], o[\"line_flags\"][:2])\nE"
}
````

### User / tool · 2026-11-02T04:23:07.470Z

**tool result**
````
'\nDOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n05/27/26  05/28/26  971'
analyzed [('Larkspur Hollow Physical Therapy', {'cents': 44500, 'usd': '$445.00'}, 7, [])] []
'DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE\n05/27/26  05/28/26  9716'
analyzed [('Larkspur Hollow Physical Therapy', {'cents': 44500, 'usd': '$445.00'}, 7, [])] []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:22.284Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"app/backend/billing.py\"\ns=open(p).read()\ndef rep(a,b,cnt=1):\n    global s\n    assert s.count(a)==cnt,(a,s.count(a))\n    s=s.replace(a,b)\nrep(\"from app.backend import amounts as A, dates, lexicon\",\"from app.backend import amounts as A, dates\")\nrep('''_SEG = re.compile(r\"[^.;!?\\\\n]+(?:\\\\.\\\\d+[^.;!?\\\\n]*)*[.;!?]?\")\\n''','')\nrep('''    for e in eobs:\n        pass\n    # statements without a table that mention a rate in prose: classify each remaining sentence (ledger_text handled above)\n''','')\nrep('''def _checks_for_line(line, prev_balance):\n    codes = []\n    if line[\"unclear\"]:\n        codes.append(\"LINE_UNCLEAR\")\n    bal = line[\"balance\"][\"cents\"] if line.get(\"balance\") else None\n    if bal is not None and prev_balance is not None:\n        delta = sum(v[\"cents\"] for k, v in ((k, line[k]) for k in (\"billed\",)) if v and v[\"cents\"] is not None)\n        delta -= sum(line[k][\"cents\"] for k in (\"paid\", \"adjustment\") if line[k] and line[k][\"cents\"] is not None)\n        if bal - prev_balance != delta:\n            codes.append(\"BALANCE_STEP_MISMATCH\")\n    return codes\n''','''def _cents(fig):\n    return fig[\"cents\"] if fig and fig[\"cents\"] is not None else None\n\n\ndef _checks_for_line(line, prev_balance):\n    \"\"\"LINE_UNCLEAR when a figure could not be read; BALANCE_STEP_MISMATCH when this line's balance is not the previous balance plus its\n    charge minus its payment and adjustment (only checked when every figure on the line was read).\"\"\"\n    codes = []\n    if line[\"unclear\"]:\n        codes.append(\"LINE_UNCLEAR\")\n    elif _cents(line.get(\"balance\")) is not None and prev_balance is not None:\n        delta = (_cents(line[\"billed\"]) or 0) - (_cents(line[\"paid\"]) or 0) - (_cents(line[\"adjustment\"]) or 0)\n        if line[\"balance\"][\"cents\"] - prev_balance != delta:\n            codes.append(\"BALANCE_STEP_MISMATCH\")\n    return codes\n''')\nrep('''\"excerpt\": body[max(body.rfind(\"\\\\n\", 0, a[\"start\"]) + 1, 0):(body.find(\"\\\\n\", a[\"end\"]) if body.find(\"\\\\n\", a[\"end\"]) >= 0 else len(body))].strip()})''','''\"excerpt\": _line_around(body, a[\"start\"], a[\"end\"])})''')\nrep('''# ------------------------------------------------------------------ assembling\n''','''# ------------------------------------------------------------------ assembling\ndef _line_around(body, start, end):\n    \"\"\"The whole printed line a figure sits on (a verbatim excerpt); a single-line paragraph gives the clause around it.\"\"\"\n    a, b = body.rfind(\"\\\\n\", 0, start) + 1, body.find(\"\\\\n\", end)\n    line = body[a:(b if b >= 0 else len(body))]\n    if len(line) > 240:\n        for s, e in _segments(body):\n            if s <= start < e:\n                return body[s:e].strip()\n    return line.strip()\n\n\n''')\n# injection skip + uncited guard\nrep('''    for r in recs:\n        body = r.get(\"excerpt\") or r.get(\"text\") or \"\"\n        ls = body.split(\"\\\\n\")\n        form = form_of(r)\n''','''    skipped = []\n    for r in recs:\n        body = r.get(\"excerpt\") or r.get(\"text\") or \"\"\n        ls = body.split(\"\\\\n\")\n        form = form_of(r)\n        if r.get(\"injection_tag\") and (form or _lop_lien(r)):      # a figure inside instruction-like text has no trusted value (D-005)\n            skipped.append({\"record_no\": r[\"n\"], \"reason_code\": \"INJECTION_SUSPECTED\"})\n            continue\n        before = len(lines)\n''')\nrep('''        if form in (\"ledger_table\", \"ledger_text\"):     # a statement's fee-schedule''','''        text = (r.get(\"text\") or \"\") + \"\\\\n\" + body\n        for l in lines[before:]:                       # fail closed: a line that is not a verbatim excerpt of its record shows no figures\n            if l[\"excerpt\"] not in text:\n                l.update(billed=None, adjustment=None, paid=None, balance=None, unclear=[\"(not verbatim)\"])\n        if form in (\"ledger_table\", \"ledger_text\"):     # a statement's fee-schedule''')\nrep('''        \"providers\": providers, \"payer_reports\": payer, \"lop_lien\": lop, \"excluded\": excluded,''','''        \"providers\": providers, \"payer_reports\": payer, \"lop_lien\": lop, \"excluded\": excluded, \"skipped_records\": skipped,''')\n# for_case simplify\ni=s.index(\"def for_case\")\nj=s.index(\"def add_routes\")\ns=s[:i]+'''def for_case(conn, case_id: str) -> dict:\n    from app.backend import store      # imported here so unit tests of the pure functions need no database\n    return analyze(store.load_records(conn, case_id))\n\n\n'''+s[j:]\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:23:23.368Z

**tool result**
````
.......................                                                  [100%]
23 passed in 0.46s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:33.282Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'E'\np=\"app/backend/billing.py\"\ns=open(p).read()\na='rec_form.get(l[\"record_no\"]) == \"ledger_table\":'\nassert a in s\ns=s.replace(a,'rec_form.get(l[\"record_no\"]) == \"ledger_text\":')\nopen(p,\"w\").write(s)\np=\"tests/unit/test_billing.py\"\ns=open(p).read()\ns+='''\n\ndef test_table_survives_ingest_with_the_quote_on_its_own_line_or_the_first_line(client):\n    from app.backend import store\n    body = LEDGER.split(\"\\\\n\", 3)[3]\n    for quoted in ('Excerpt: \"' + body + '\"', 'Excerpt: \"\\\\n' + body + '\\\\n\"'):\n        text = \"=== Record 1 ===\\\\nDate: 2026-07-31\\\\nSource: Larkspur Hollow Physical Therapy, itemized statement\\\\n\" + quoted + \"\\\\n\"\n        conn = DB.connect(client.app.state.db_path)\n        tok = DB.create_case(conn, text, now=time.time())\n        PL.ingest_case(conn, tok, text, time.time())\n        out = B.for_case(conn, tok)\n        assert B.verify_citations(out, store.load_records(conn, tok)) == []\n        conn.close()\n        p = out[\"providers\"][0]\n        assert p[\"billed\"][\"cents\"] == 44500 and p[\"adjustment\"][\"cents\"] == 4500 and p[\"checks\"] == [] and len(p[\"lines\"]) == 7\n\n\ndef test_prose_charges_without_a_date_of_service_are_counted_as_stated_and_flagged():\n    out = one([rec(9, \"Fennimoor Spine Clinic, itemized ledger\", PROSE)])\n    assert {f[\"code\"] for f in out[\"line_flags\"]} == {\"NO_DATE_OF_SERVICE\"}\n\n\ndef test_injection_tagged_record_is_skipped_not_totaled():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER, injection_tag=True)]\n    out = one(r)\n    assert out[\"providers\"] == [] and out[\"skipped_records\"] == [{\"record_no\": 1, \"reason_code\": \"INJECTION_SUSPECTED\"}]\n\n\ndef test_duplicate_records_are_ignored_and_no_model_is_imported():\n    r = [rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER), rec(2, \"Larkspur Hollow Physical Therapy, itemized statement\", LEDGER, duplicate_of=1)]\n    assert provider(one(r), \"Larkspur\")[\"lines\"][0][\"record_nos\"] == [1]\n    import app.backend.billing as mod, inspect\n    assert \"app.llm\" not in inspect.getsource(mod) and \"call(\" not in inspect.getsource(mod)\n'''\nopen(p,\"w\").write(s)\nE\n.venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T04:23:34.170Z

**tool result**
````
...........................                                              [100%]
27 passed in 0.44s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:36.382Z

**tool call — Bash**
````
{
 "command": "grep -n \"^| GET | \\`/api/cases/{token}/judges\\`\\|^## DELETE\\|^## Appendix\\|CONFLICT_CHECK_INCOMPLETE\" memory/contracts/api.md | cut -c1-120"
}
````

### User / tool · 2026-11-02T04:23:36.447Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:37.894Z

**tool call — Bash**
````
{
 "command": "grep -n -e '/judges' -e '^## DELETE' -e '^## Appendix' -e 'CONFLICT_CHECK_INCOMPLETE' memory/contracts/api.md | cut -c1-110"
}
````

### User / tool · 2026-11-02T04:23:38.025Z

**tool result**
````
37:| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rat
218:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt sh
572:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blo
574:### GET /api/cases/{token}/judges
606:## DELETE /api/cases/{token}
611:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
636:| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded a
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:23:39.550Z

**tool call — Bash**
````
{
 "command": "sed -n 36,40p memory/contracts/api.md | cut -c1-90; sed -n 600,611p memory/contracts/api.md | cut -c1-120; tail -3 memory/contracts/api.md | cut -c1-120"
}
````

### User / tool · 2026-11-02T04:23:39.659Z

**tool result**
````
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extra
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections wi
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=l

---
/bin/bash: child setpgid (98586 to 98586): Operation not permitted
## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted"
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a libr

## DELETE /api/cases/{token}
`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from 

---

## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
| `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by cod
| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from 
| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflic
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:01.051Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/billing_contract.md <<'EOF'\n## GET /api/cases/{token}/billing  (T-083, D-042)\nCode-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.\n```json\n{ \"billing\": {\n  \"status\": \"analyzed\",                         // analyzed | partial_unclear (some figure could not be read) | none_found\n  \"providers\": [ {\n    \"provider\": \"Larkspur Hollow Physical Therapy\", \"record_nos\": [1], \"basis\": \"itemized_ledger\",   // or \"claim_form\" when the provider has no ledger\n    \"billed\": {\"cents\": 44500, \"usd\": \"$445.00\"}, \"adjustment\": {\"cents\": 4500, \"usd\": \"$45.00\"}, \"paid\": {\"cents\": null, \"usd\": null},\n    \"negotiated_reductions\": {\"cents\": null, \"usd\": null},        // attorney reductions on the ledger, kept out of `adjustment`\n    \"balance\": {\"text\": \"400.00\", \"cents\": 40000, \"usd\": \"$400.00\", \"cite\": {\"record_no\": 1, \"excerpt\": \"TOTAL CHARGES 445.00 ...\"}},   // the statement's own figure, null when none; never derived\n    \"stated_totals\": {\"billed\": {...}, \"paid\": {...}, \"adjustment\": {...}, \"balance\": {...}},        // each with a cite; only those the document prints\n    \"complete\": true, \"unclear_lines\": 0, \"line_count\": 7, \"claim_lines_not_totaled\": 0,\n    \"checks\": [ {\"code\": \"LEDGER_TOTAL_MISMATCH\", \"field\": \"billed\", \"stated\": {\"cents\": 45500, \"usd\": \"$455.00\", ...}, \"computed\": {\"cents\": 44500, \"usd\": \"$445.00\"}, \"message\": \"...\"} ],\n    \"lines\": [ {\n      \"id\": \"b3\", \"kind\": \"charge\",                              // charge | reversal | payment | adjustment | balance_only | unclear\n      \"form\": \"ledger\",                                          // ledger | cms1500 | ub04\n      \"dos\": \"06/10/26\", \"dos_iso\": \"2026-06-10\", \"posted\": \"06/11/26\", \"code\": \"97140\", \"description\": \"Manual therapy x1\",\n      \"billed\": {\"text\": \"70.00\", \"cents\": 7000, \"usd\": \"$70.00\"}, \"adjustment\": null, \"paid\": null, \"balance\": {\"text\": \"410.00\", \"cents\": 41000, \"usd\": \"$410.00\"},\n      \"unclear\": [], \"negotiated\": false, \"checks\": [],           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE\n      \"excerpt\": \"06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00\",   // the printed line, verbatim\n      \"record_nos\": [1], \"cites\": [ {\"record_no\": 1, \"excerpt\": \"<same line>\"} ] } ] } ],\n  \"payer_reports\": [ { \"record_no\": 2, \"provider\": \"Larkspur Hollow Physical Therapy\", \"matched_provider\": \"Larkspur Hollow Physical Therapy\",\n    \"lines\": [ {\"dos\": \"06/10/26\", \"service\": \"97140\", \"billed\": {...}, \"discount\": {...}, \"allowed\": {...}, \"deductible\": {...}, \"coinsurance\": {...}, \"plan_paid\": {...}, \"patient_owes\": {...}, \"codes\": \"PR-1, PR-2, CO-45\", \"excerpt\": \"...\", \"unclear\": []} ],\n    \"checks\": [ {\"code\": \"LEDGER_EOB_PAID_MISMATCH\", \"dos\": \"06/10/26\", \"service\": \"97140\", \"ledger\": {\"cents\": 0, \"usd\": \"$0.00\"}, \"eob\": {\"cents\": 1600, ...}, \"cites\": [ {\"record_no\": 2, \"excerpt\": \"...\"}, {\"record_no\": 1, \"excerpt\": \"...\"} ], \"message\": \"...\"} ],\n    \"not_added_note\": \"The EOB restates the provider's charge; its amounts are never added to the charges.\" } ],\n  \"lop_lien\": [ {\"id\": \"l1\", \"record_no\": 2, \"provider\": \"Pellingham and Rook PLLC\", \"kind\": \"asserted_balance\", \"label\": \"...\", \"figure\": {\"text\": \"$4,860.00\", \"cents\": 486000, \"usd\": \"$4,860.00\"}, \"excerpt\": \"...\", \"in_totals\": false} ],   // kind: asserted_balance | lien_amount | reduction\n  \"excluded\": [ {\"id\": \"x1\", \"record_no\": 1, \"provider\": \"...\", \"kind\": \"rate\", \"why\": \"...\", \"figure\": {...}, \"excerpt\": \"Fee schedule: Therapeutic exercise $65.00 per unit.\"} ],\n  \"skipped_records\": [ {\"record_no\": 4, \"reason_code\": \"INJECTION_SUSPECTED\"} ],\n  \"checks\": [ /* every provider and payer check, flat */ ], \"line_flags\": [ {\"code\": \"BALANCE_STEP_MISMATCH\", \"line_id\": \"b3\", \"provider\": \"...\", \"message\": \"...\", \"excerpt\": \"...\"} ],\n  \"totals\": { \"billed\": {\"cents\": 318500, \"usd\": \"$3,185.00\"}, \"adjustment\": {...}, \"paid\": {...}, \"provider_count\": 2, \"not_for_letter\": true },\n  \"rules\": [ \"Only figures stated in the records are totaled; ...\", \"...\" ] } }\n```\n**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (a void nets out) and is read as a reduction in the payment and adjustment columns (magnitude kept; `BALANCE_STEP_MISMATCH` catches a wrongly read column). Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. A running balance is never summed; `Bal fwd` is not a charge; a re-sent statement or attached copy counts once and cites both records (`record_nos`, `cites`), while a repeated line inside one record counts twice. CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00 (the `Item 28` total is parsed the same way and compared with the line sum). UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a rate (listed in `excluded`) and the `0001` line is the printed total (compared, never added). A fee-schedule or per-unit figure is a rate, listed in `excluded`. EOB amounts (`billed`, `plan_paid`, ...) are never added to charges; a ledger-versus-EOB difference for the same date and service is raised as a check and neither side is picked. When a provider has both a ledger and a claim form, the ledger is the basis and the claim form is compared (`CLAIM_LEDGER_BILLED_MISMATCH`). LOP, lien, \"reduced to\" and attorney-reduction amounts are only in `lop_lien` (`in_totals: false`, always). A figure with OCR letters, other than two decimals, or inside an injection-tagged record has `cents: null` / the record is `skipped_records`, and is left out of every total. Every `excerpt` is a verbatim substring of its record (`verify_citations`); a line that is not verbatim shows no figures.\n**Check codes (closed list, fixed message each):** `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, `NO_DATE_OF_SERVICE`.\n**Ladder.** All steps are code (parse, cite, compare); there is no model step, so no judge. The human step is reading the view; none of it is exportable.\n\nEOF\n.venv/bin/python - <<'E'\np=\"memory/contracts/api.md\"\ns=open(p).read()\nsec=open(\"/private/tmp/claude-501/billing_contract.md\").read()\nrow=\"| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |\\n\"\nanchor=\"| GET | `/api/cases`, `/api/library` |\"\nassert s.count(anchor)==1 and s.count(\"\\n## DELETE /api/cases/{token}\\n\")==1 and \"/billing\" not in s\ns=s.replace(anchor,row+anchor,1)\ns=s.replace(\"\\n## DELETE /api/cases/{token}\\n\",\"\\n\"+sec.rstrip(\"\\n\")+\"\\n\\n## DELETE /api/cases/{token}\\n\",1)\nopen(p,\"w\").write(s)\nE\ngrep -c \"billing\" memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T04:24:01.182Z

**tool result**
````
5
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:03.556Z

**tool call — Bash**
````
{
 "command": "grep -n \"billing\" app/backend/api.py; .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -12"
}
````

### User / tool · 2026-11-02T04:24:44.373Z

**tool result**
````
507:    from app.backend import billing
508:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
>           assert not re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M), p
E           AssertionError: PosixPath('/Users/arsis/zlayt-pm-project/app/backend/pdf_ocr.py')
E           assert not <re.Match object; span=(1070, 1087), match='import subprocess'>
E            +  where <re.Match object; span=(1070, 1087), match='import subprocess'> = <function search at 0x10462c7c0>('^\\s*(import|from)\\s+(anthropic|subprocess)\\b', '"""Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page...der the page\n        raise OcrFailed(type(e).__name__) from None\n    finally:\n        pdf.close()\n    return out\n', re.MULTILINE)
E            +    where <function search at 0x10462c7c0> = re.search
E            +    and   re.MULTILINE = re.M

tests/unit/test_provider_backends.py:159: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
2 failed, 1260 passed in 39.39s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:47.488Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -3 && git diff HEAD --stat -- app/backend/api.py memory/contracts/api.md | tail -3; git show HEAD:app/backend/api.py | grep -n \"billing\" | head -2"
}
````

### User / tool · 2026-11-02T04:24:47.745Z

**tool result**
````
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
 app/backend/api.py      | 38 +++++++++++++++++++++---------
 memory/contracts/api.md | 62 ++++++++++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 88 insertions(+), 12 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:53.550Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u) && git read-tree HEAD && \ngit show HEAD:app/backend/api.py > /private/tmp/claude-501/api_head.py &&\n.venv/bin/python - <<'E'\ns=open(\"/private/tmp/claude-501/api_head.py\").read()\na=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(a)==1\ns=s.replace(a,a+\"    from app.backend import billing\\n    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\\n\")\nopen(\"/private/tmp/claude-501/api_new.py\",\"w\").write(s)\nm=open(\"memory/contracts/api.md\").read()\nsec=open(\"/private/tmp/claude-501/billing_contract.md\").read()\nh=__import__(\"subprocess\").check_output([\"git\",\"show\",\"HEAD:memory/contracts/api.md\"]).decode()\nrow=\"| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |\\n\"\nanchor=\"| GET | `/api/cases`, `/api/library` |\"\nh=h.replace(anchor,row+anchor,1).replace(\"\\n## DELETE /api/cases/{token}\\n\",\"\\n\"+sec.rstrip(\"\\n\")+\"\\n\\n## DELETE /api/cases/{token}\\n\",1)\nopen(\"/private/tmp/claude-501/api_md_new.md\",\"w\").write(h)\nE\nfor pair in \"app/backend/api.py:/private/tmp/claude-501/api_new.py\" \"memory/contracts/api.md:/private/tmp/claude-501/api_md_new.md\"; do f=${pair%%:*}; src=${pair#*:}; sha=$(git hash-object -w \"$src\"); git update-index --cacheinfo 100644,$sha,$f; done\ngit add app/backend/billing.py tests/unit/test_billing.py && git diff --cached --stat && git commit -q -m \"feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)\n\nCode-only: ledger lines parse to billed/adjustment/paid/balance, each cited verbatim; totals by provider; LOP and lien amounts listed separately; rates, running balances, claim totals and EOB billed are never totaled. GET /api/cases/{token}/billing.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD; unset GIT_INDEX_FILE"
}
````

### User / tool · 2026-11-02T04:24:53.701Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u) && git read-tree HEAD && 
git show HEAD:app/backend/api.py > /private/tmp/claude-501/api_head.py &&
.venv/bin/python - <<'E'
s=open("/private/tmp/claude-501/api_head
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:24:58.782Z

**tool call — Bash**
````
{
 "command": "rm -f /private/tmp/claude-501/idx_t083 && export GIT_INDEX_FILE=/private/tmp/claude-501/idx_t083 && git read-tree HEAD && git show HEAD:app/backend/api.py > /private/tmp/claude-501/api_head.py && .venv/bin/python - <<'E'\nimport subprocess\ns=open(\"/private/tmp/claude-501/api_head.py\").read()\na=\"    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)\\n\"\nassert s.count(a)==1\ns=s.replace(a,a+\"    from app.backend import billing\\n    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083\\n\")\nopen(\"/private/tmp/claude-501/api_new.py\",\"w\").write(s)\nsec=open(\"/private/tmp/claude-501/billing_contract.md\").read()\nh=subprocess.check_output([\"git\",\"show\",\"HEAD:memory/contracts/api.md\"]).decode()\nrow=\"| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |\\n\"\nanchor=\"| GET | `/api/cases`, `/api/library` |\"\nassert h.count(anchor)==1\nh=h.replace(anchor,row+anchor,1).replace(\"\\n## DELETE /api/cases/{token}\\n\",\"\\n\"+sec.rstrip(\"\\n\")+\"\\n\\n## DELETE /api/cases/{token}\\n\",1)\nopen(\"/private/tmp/claude-501/api_md_new.md\",\"w\").write(h)\nE\ngit update-index --cacheinfo 100644,$(git hash-object -w /private/tmp/claude-501/api_new.py),app/backend/api.py && git update-index --cacheinfo 100644,$(git hash-object -w /private/tmp/claude-501/api_md_new.md),memory/contracts/api.md && git add app/backend/billing.py tests/unit/test_billing.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T04:24:59.374Z

**tool result**
````
 app/backend/api.py         |   2 +
 app/backend/billing.py     | 642 +++++++++++++++++++++++++++++++++++++++++++++
 memory/contracts/api.md    |  37 +++
 tests/unit/test_billing.py | 330 +++++++++++++++++++++++
 4 files changed, 1011 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:02.003Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/billing.py tests/unit/test_billing.py; GIT_INDEX_FILE=/private/tmp/claude-501/idx_t083 git commit -q -m \"feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)\n\nCode-only: ledger lines parse to billed/adjustment/paid/balance, each cited verbatim; totals by provider; LOP and lien amounts listed separately; rates, running balances, claim totals and EOB billed are never totaled. GET /api/cases/{token}/billing.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" && git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T04:25:02.535Z

**tool result**
````
     642 app/backend/billing.py
     330 tests/unit/test_billing.py
     972 total
check_secrets: ok (4 file(s) scanned staged)
f218263
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:10.440Z

**tool call — Bash**
````
{
 "command": "grep -c \"^def \" app/backend/billing.py; grep -n \"^def analyze\" app/backend/billing.py; B=\"python3 tools/board.py\"; $B ac T-083 --check 1 --agent backend --evidence \"tests/unit/test_billing.py: 27 passed (ledger table+prose, void netting, rate excluded, CMS-1500 implied decimals, UB-04 FL44 rate, EOB mismatch, LOP/lien separate, citations verbatim, route)\"; $B commit T-083 --sha f218263 --agent backend; $B note T-083 --agent backend --text \"UI needs (for a frontend card): GET /api/cases/{token}/billing (contract in api.md). A Billing panel per case: per-provider cards (billed, adjustment, paid, stated balance, 'complete' badge), expandable line table with the verbatim excerpt per line + highlight of the figure, line_flags/checks as stepper-style rows (code check pass/fail with both figures and cites; ledger-vs-EOB mismatch shows both documents' lines, no picking), separate 'LOP and lien amounts (not totaled)' list, separate 'Rates and excluded' list, skipped_records notice, and an 'internal view, not in the letter' label. Unclear figures show text with no value. All code-made: label 'checked by code', no judge step.\" ; $B handoff T-083 --agent backend --text \"What changed: app/backend/billing.py (new, code only) + GET /api/cases/{token}/billing + api.md section; 2-line hook in api.py. Ledger tables (position-assigned columns), sentence ledgers, CMS-1500 (implied cents), UB-04 (FL44 rate excluded, 0001 compared), EOBs (never added; ledger-vs-EOB paid/billed checks), LOP/lien list. How verified: .venv/bin/python -m pytest -q tests/unit/test_billing.py (27 pass); full unit run 1260 pass, 2 unrelated fails (test_single_call_path in test_provider*.py: app/backend/pdf_ocr.py imports subprocess, T-086's file). Left: frontend panel (see note); no LLM step so no eval impact. Surprised: ADJ amounts are left-aligned under header while charges are right-aligned, so column match uses min(start,end) distance; demo mode refuses unrecorded text over HTTP so route test seeds via ingest_case.\" ; $B move T-083 in_review --agent backend"
}
````

### User / tool · 2026-11-02T04:25:10.816Z

**tool result**
````
31
451:def analyze(records: list) -> dict:
AC 1 checked: tests/unit/test_billing.py: 27 passed (ledger table+prose, void netting, rate excluded, CMS-1500 implied decimals, UB-04 FL44 rate, EOB mismatch, LOP/lien separate, citations verbatim, route)
T-083: commit f218263 recorded
noted on T-083
handoff written on T-083
T-083: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:25:13.265Z

T-083 is in review: billing analysis is built, code only, with a new `GET /api/cases/{token}/billing` route, committed as f218263 (contract in `memory/contracts/api.md`, 2-line hook in `api.py`).

The 27 new tests in `tests/unit/test_billing.py` pass. The full unit run is 1260 pass, 2 fail: both `test_single_call_path` tests, because T-086's `app/backend/pdf_ocr.py` imports `subprocess`. I left the frontend-panel notes on the card for a follow-up card.
