"""Letter-level eval (T-139; D-019, R-CH-7, R-EX-8): no dollar amount reaches the carrier letter except in the BILLED CHARGES section.

For every golden case, the sample and every library packet, on the FIXTURE backend (recorded model answers; no network):
  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
  then a variant where every charge is dismissed.
Violations (all must be zero):
  - a currency string in the letter outside the BILLED CHARGES section (the treatment entries and the TREATMENT SUMMARY paragraph);
  - in the BILLED CHARGES section, a currency string that is not an accepted charge or the total line (R-EX-8: exactly 'Billed charges accepted from these records: $X');
  - after dismissing every charge: any currency string anywhere in the letter, or a provider whose charge was dismissed under BILLS TO REQUEST in the notes.
  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
D-071 / D-073 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every charge
line of every letter is checked (`charge_date_violations`, D-073 FALLBACK after round 6): the letter extracts no service date, so EVERY charge line must print the fillable blank in its exact
form, 'date of service [__________] (record dated X)', X the record's own date. A printed date, period or any other form is a violation.
Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.

    python -m evals.letter_check            prints one line per case and exits 1 on any violation
"""
import contextlib
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"
CHARGES, TOTAL = "BILLED CHARGES", "Billed charges accepted from these records: "
STYLES = (None, "oneline")

def dollar_figures(text: str) -> list:
    """Every '$'-marked figure (also 'N dollars', 'USD N') in `text`, in order of position (the shared detector, app/backend/money.py)."""
    from app.backend import money
    return money.of_kind(text, "dollar")


def other_currency(text: str) -> list:
    """Figures with another currency sign or code, amounts in words, and money in a patient's statement (the shared detector)."""
    from app.backend import money
    return money.of_kind(text, "sign", "spoken", "statement")


def unmarked_money(text: str) -> list:
    """Money written without a sign (a money word or claim-form field and its figure), outside any signed figure (the shared detector)."""
    from app.backend import money
    return money.of_kind(text, "unmarked")


def cases():
    """[(name, text)]: the sample, the golden cases and the library packets, in a fixed order."""
    names = [GOLD / "sample.txt"] + sorted(GOLD.glob("case_*.txt")) + sorted(LIB.glob("case_*.txt"))
    return [(p.stem, p.read_text()) for p in names]


def violations(letter: str, accepted_cents=(), expect_none: bool = False) -> list:
    """Currency strings the letter may not carry. `accepted_cents`: the accepted charges (the only amounts the BILLED CHARGES section may list).
    `expect_none`: nothing was accepted as a charge, so no currency string may appear anywhere."""
    from app.backend import amounts as AM, export
    out = []
    head_lines, tail_lines = export.split_letter(letter)               # by structure (the last BILLED CHARGES header line before the total line), never on the words in a quote
    head, tail = "\n".join(head_lines), "\n".join(tail_lines)
    out += [f"treatment text states {s}" for s in dollar_figures(head)]
    out += [f"treatment text states money in another form: {s}" for s in other_currency(head)]
    out += [f"treatment text states money without a $ sign: {s}" for s in unmarked_money(head)]
    if expect_none or not accepted_cents:
        out += [f"letter states {s} with no accepted charge" for s in dollar_figures(tail)]
        out += [f"letter states money without a $ sign: {s}" for s in unmarked_money(tail)]
        out += [f"letter states money in another form: {s}" for s in other_currency(tail)]
        return out
    allowed = {c for c in accepted_cents} | {sum(accepted_cents)}
    for line in tail.splitlines():
        for s in dollar_figures(line):
            cents = AM.to_cents(s.lstrip("$ ").strip())
            if cents is None or cents not in allowed:
                out.append(f"charges section states {s}, not an accepted charge or the total")
        out += [f"charges section states money without a $ sign: {s}" for s in unmarked_money(line)]
        out += [f"charges section states money in another form: {s}" for s in other_currency(line)]
    totals = [l for l in tail.splitlines() if l.startswith(TOTAL)]
    if len(totals) != 1 or not re.fullmatch(re.escape(TOTAL) + r"\$[\d,]+\.\d\d", totals[0]):
        out.append(f"total line is not exactly the template: {totals}")
    return out


# T-208 (T-201 review, D-065 / D-069): the carrier letter never names an AI or a model, whatever the case's provenance (prepared or live). One independent pattern, its own scan.
AI_WORDING = re.compile(r"\bAI\b|claude|sonnet|haiku|opus|\bmodel\b", re.I)
# The ONE allowed form (D-042 / D-050, T-121): the bracketed, removable translation label on an entry from a Spanish record whose English summary a model wrote. It is a safety label (check the
# original before sending), not provenance wording, and it is the only place the letter says 'AI'. Matched whole and verbatim (the string is copied here on purpose, not imported from the export).
# T-208 r2: the label is exempt ONLY where it belongs: the case must have a translated (non-English) source entry, and the label must sit directly with that entry's quote (standard style: alone on
# the line right under the quote line; one-line style: after the quote, on the same line). Anywhere else, in an English letter or away from the quote, it fails like any other 'AI'.
# If the product decides the letter must not say it at all, delete this one tuple entry.
ALLOWED_AI_LABELS = ("[AI translation of the Spanish original; check before sending]",)


def _oneline(s):
    return " ".join(str(s).split())


def _label_with_quote(letter: str, i: int, label: str, translated_quotes) -> bool:
    """True when the label starting at index i sits directly with the quote of a translated entry (see the comment on ALLOWED_AI_LABELS)."""
    before = letter[:i]
    line_start = before.rfind("\n") + 1
    after = letter[i + len(label):i + len(label) + 1]
    for q in translated_quotes:
        if not q:
            continue
        if line_start == i:      # standard style: the label is alone on its line, right under the quote line
            if after in ("", "\n") and before.endswith(f'"{q}"\n'):
                return True
        elif after in ("", "\n") and f'"{_oneline(q)}"' in before[line_start:]:      # one-line style: the quote is on this line, before the label
            return True
    return False


def ai_wording(letter: str, translated_quotes=()) -> list:
    """Every AI or model word in the letter ('AI', 'Claude', 'Sonnet', 'Haiku', 'Opus', 'model'), each with its line, so the audit shows where. The allowed translation label is not scanned when
    it sits directly with the quote of a translated entry (translated_quotes = that case's translated entries' quotes); with no translated quote given, nothing is exempt."""
    chars = list(letter)
    for ok in ALLOWED_AI_LABELS:
        for m in re.finditer(re.escape(ok), letter):
            if _label_with_quote(letter, m.start(), ok, translated_quotes):
                chars[m.start():m.end()] = [" "] * (m.end() - m.start())      # blank only the allowed occurrences (same length, so every other index stays valid)
    out = []
    for line, orig in zip("".join(chars).splitlines(), letter.splitlines()):
        out += [f"letter names AI or a model: {m.group(0)!r} in {orig.strip()[:80]!r}" for m in AI_WORDING.finditer(line)]
    return out


def _walk(conn, cid, dismiss_charges=False):
    """Accept (or dismiss) every item through the review code path. Returns (accepted charge cents, refused [(id, code)])."""
    from app.backend import review
    from app.db import db as DB
    refused, cents = [], []
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, cid, kind):
            if it["state"] == "rejected":
                continue
            dismiss = dismiss_charges and kind == "amount" and it["kind"] == "charge"
            try:
                review.apply_review(conn, cid, it["id"], {"action": "dismiss" if dismiss else "accept"})
            except review.ReviewError as e:
                refused.append((it["id"], e.code if e.code != "CODE_CHECK_FAILED" else (e.detail or {}).get("reason_code", e.code)))
                continue
            if kind == "amount" and it["kind"] == "charge" and not dismiss and it.get("value_cents") is not None:
                cents.append(it["value_cents"])
    return cents, refused


def _count_all(conn, cid):
    """D-064 count path: count every amount the code held back for a missing detail, naming the confirm (and the duplicate / total flag when the code asks for it); an uncountable one is
    skipped. Returns the cents of every accepted charge after that."""
    from app.backend import count_charge, review
    from app.db import db as DB
    for it in DB.list_items(conn, cid, "amount"):
        if it["state"] == "rejected" or it["kind"] == "charge":
            continue
        body = {"confirm": count_charge.CONFIRM}
        for _ in range(2):
            try:
                count_charge.count(conn, cid, it["id"], dict(body))
                break
            except review.ReviewError as e:
                want = (e.detail or {}).get("confirm_with")
                if e.code == "CONFIRM_REQUIRED" and want and want != count_charge.CONFIRM and "confirm_flag" not in body:
                    body["confirm_flag"] = want
                    continue
                break
    return [it["value_cents"] for it in DB.list_items(conn, cid, "amount")
            if it["kind"] == "charge" and it["review_status"] in ("accepted", "edited") and it.get("value_cents") is not None and it["state"] != "rejected"]


BLANK = "date of service [__________]"          # D-073 fallback: the ONLY printed form of a charge line's date


def charge_lines(letter: str) -> list:
    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
    from app.backend import export
    _, tail = export.split_letter(letter)
    out = []
    for i, line in enumerate(tail):
        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
            q = tail[i + 1]
            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
    return out


def charge_date_violations(letter: str, records) -> list:
    """D-073 FALLBACK (T-202 round 6): every charge line prints the fillable blank and nothing else for its date of service, in its exact form, anchored at both ends:
    '<source label>, date of service [__________] (record dated June 15, 2026)' (D-075: always "record dated", no bill/record classification), and no parenthesis when the
    record has no date. A printed service date, a period, a blank in any other form, or a statement date that is not the record's own is a violation. `records`: the case's
    [{n, source, date_iso, excerpt}]; a line's record is the one whose excerpt holds the line's quote."""
    from datetime import date
    norm = lambda t: " ".join(str(t).split())
    out = []
    for head, quote in charge_lines(letter):
        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
        if not recs:
            out.append(f"charge line's quote is in no record: {head}")
            continue
        got = norm(re.sub(r": \$[\d,]+\.\d\d$", "", head))
        wants = []
        for r in recs:
            rd = r.get("date_iso")
            d = date.fromisoformat(rd) if rd else None
            wants.append(f"{norm(r.get('source') or '')}, {BLANK}" + (f" (record dated {d.strftime('%B')} {d.day}, {d.year})" if d else ""))
        if got not in wants:
            out.append(f"charge line does not print the blank date of service in its exact form (source label, then '{BLANK}', then '(record dated X)', X the record's own date): {head}")
    return out


def letters_for(text: str, backend: str = "fixture") -> dict:
    """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
    from app.backend import export, ingest as IN, pipeline as PL, store
    from app.llm import provider as P
    out = {}
    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
        with PL._Backend(backend), tempfile.TemporaryDirectory() as tmp:
            conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
            with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
                PL.run_pipeline(conn, cid, text, call=call)
            cents, refused = _walk(conn, cid, dismiss)
            if variant == "counted":
                cents = _count_all(conn, cid)
            case = store.export_case(conn, cid)
            case["judge_not_run"] = []          # this check reads the letter text only; the second-check gate is a separate rule (D-044)
            built, gate = {}, {}
            for st in STYLES:
                key = st or "standard"
                try:
                    built[key] = export.build_export(case, st)
                except export.ExportBlocked as e:                  # T-139 r4: the export gate itself; a blocked letter is a violation, and the text is still audited below
                    gate[key] = [i["why"] for i in e.items]
                    built[key] = export.build_export(case, st, check_letter=False)
            src = {r["n"]: r["source"] for r in case["records"]}
            dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
            conn.close()
        out[variant] = {"letters": {k: v["letter_text"] for k, v in built.items()}, "notes": built["standard"]["internal_notes_text"],
                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate,
                        "prepared": bool(case.get("prepared")),
                        "translated_quotes": [e["excerpt"] for e in case["entries"] if e.get("translation_label") == "AI translation"]}      # T-208: the case kind, so a report can say how many prepared and live letters were scanned
    return out


def dismissed_in_bills(notes: str, providers) -> list:
    """Providers whose charge was dismissed that the notes still list under BILLS TO REQUEST."""
    sec = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0] if "BILLS TO REQUEST" in notes else ""
    listed = [re.sub(r"\s*\(itemized ledger\)$", "", x.strip().rstrip(".")) for x in sec.split("\n", 2)[-1].lstrip("- ").split(";")]
    return [p for p in providers if p in listed]


def measure(case_list=None, backend: str = "fixture") -> dict:
    """The report block: {'value': total violations (0 = pass), 'cases': n, 'per_case': {...}, 'held_out_entries': n, 'r_ids': [...]}."""
    per_case, held = {}, 0
    for name, text in (case_list if case_list is not None else cases()):
        got = letters_for(text, backend)
        bad = []
        for style, letter in got["all_accepted"]["letters"].items():
            bad += [f"{style}: {v}" for v in violations(letter, got["all_accepted"]["charge_cents"])]
        for style, letter in got["charges_dismissed"]["letters"].items():
            bad += [f"{style} (charges dismissed): {v}" for v in violations(letter, (), expect_none=True)]
        for style, letter in got["counted"]["letters"].items():
            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
        for variant in ("all_accepted", "charges_dismissed", "counted"):      # T-208: no AI or model wording in any letter, of any kind of case
            for style, letter in got[variant]["letters"].items():
                bad += [f"{style} ({variant}): {v}" for v in ai_wording(letter, got[variant].get("translated_quotes", ()))]
        for variant in ("all_accepted", "counted"):
            for style, letter in got[variant]["letters"].items():
                bad += [f"{style} ({variant}): {v}" for v in charge_date_violations(letter, got[variant]["records"])]
        for variant in ("all_accepted", "charges_dismissed", "counted"):
            bad += [f"{style} ({variant}): the export gate blocked this letter: {w}" for style, whys in got[variant]["gate"].items() for w in whys]
        bad += [f"dismissed charge's provider {p} is under BILLS TO REQUEST" for p in dismissed_in_bills(got["charges_dismissed"]["notes"], got["charges_dismissed"]["dismissed_providers"])]
        held += sum(1 for _, code in got["all_accepted"]["refused"] if code == "CHARGE_TEXT_IN_ENTRY")
        if bad:
            per_case[name] = sorted(set(bad))
    return {"value": sum(len(v) for v in per_case.values()), "cases": len(case_list if case_list is not None else cases()), "per_case": per_case,
            "held_out_entries": held, "backend": backend, "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}


def main(argv=None) -> int:
    m = measure()
    print(json.dumps({k: v for k, v in m.items() if k != "per_case"}))
    for name, v in m["per_case"].items():
        print(f"  {name}: {v}")
    return 0 if m["value"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
