"""CHARGE_TEXT_IN_ENTRY (T-139; D-019, R-CH-7, R-EX-8): a dollar amount never reaches the carrier letter through a treatment entry. CODE ONLY (no LLM, no network).

The only dollar figures the letter may print are the accepted-charge lines and the R-EX-8 total line, which export.py builds from amounts, not from entries.
Rates, estimates, unclear amounts and dismissed charges appear only in the internal notes. The extract prompt asks the model for sentences that carry the
treatment, findings, diagnosis, plan 'or charge', so a summary or a quote can state an amount ('Charge per visit $140', 'ED charge: $3,915').

    currency_strings(text) -> ['$3,915', ...]       every currency figure, in order of position (a '$' figure, OCR-noisy like '$1,2OO', 'N dollars', 'USD N')
    check(summary, excerpt) -> {} | {'summary': [...], 'excerpt': [...]}
    trim_summary(summary)  -> {text, removed, changed}     removes currency clauses from the END of a summary (D-054 suffix rule), never edits a kept clause
    narrow_excerpt(excerpt) -> {excerpt, dropped} | None    drops currency-bearing sentences at the START or END of a multi-sentence quote (whole sentences, contiguous run)

A quote is never rewritten: a quote that states an amount is replaced by the paralegal (the quote picker), not by code. A summary clause may be removed by
code under the D-054 suffix rule: only a run of trailing clauses that all state an amount is removed, the first clause is never removed, and the kept
prefix keeps at least 2 content words. When a rule says no, nothing is trimmed and the paralegal edits the summary."""
import re

from app.backend import money, sentences, summary_trim


def dollar_strings(text) -> list:
    """The signed figures (a '$' figure incl. OCR-noisy '$1,2OO', 'N dollars', 'USD N', other signs, amounts in words) as written, in order of position."""
    return money.dollar_strings(text)


def unmarked_strings(text) -> list:
    """Money written without a sign: a money word or claim-form field with its figure ('TOTAL CHARGE 49100', 'Patient responsibility 1,200.00', '24F 25500')."""
    return money.of_kind(text, "unmarked", "statement")


def currency_strings(text) -> list:
    """Every money expression in `text`, in order of position: the one shared detector (app/backend/money.py)."""
    return money.strings(text)


def has_currency(text) -> bool:
    return money.has_money(text)


def check(summary, excerpt) -> dict:
    """{} when neither the summary nor the quote states an amount; else {'summary': [...]} and/or {'excerpt': [...]}."""
    out = {}
    for key, text in (("summary", summary), ("excerpt", excerpt)):
        found = currency_strings(text)
        if found:
            out[key] = found
    return out


class BillState(str):
    """The state word ('listed' | 'pending' | 'dismissed' | 'not_totaled' | 'none'), carrying the text of the record's amount rows so a figure typed into a summary can be told
    from one that is on the record. It compares equal to its word."""
    texts = ""


def bill_state(amount_rows) -> str:
    """Where this record's figures are counted, from the amount items on the record(s) of a held entry (DB rows: kind, review_status, state, text, excerpt).
    'listed': a charge on it is accepted, so it is under Billed charges. 'pending': it has a charge not yet accepted. 'dismissed': its charge was dismissed, so nothing of it is
    counted. 'not_totaled': amounts were read from it (rates, unclear figures, estimates) but none is a charge, so none is totaled. 'none': no amount was read from it."""
    rows = [a for a in amount_rows or [] if a.get("state") != "rejected"]
    ch = [a for a in rows if a.get("kind") == "charge" and a.get("review_status") != "dismissed"]
    if any(a.get("review_status") in ("accepted", "edited") for a in ch):
        word = "listed"
    elif ch:
        word = "pending"
    elif any(a.get("kind") == "charge" for a in rows):
        word = "dismissed"
    else:
        word = "not_totaled" if rows else "none"
    out = BillState(word)
    out.texts = " ".join(f"{a.get('text') or ''} {a.get('excerpt') or ''}" for a in rows)
    return out


_BILL_SENTENCE = {
    "listed": "This record is a bill and its charges are already listed under Billed charges, so dismiss this entry unless it states treatment.",
    "pending": "This record has charges that go under Billed charges once you accept them, so dismiss this entry unless it states treatment.",
    "dismissed": "You dismissed this record's charge, so none of its figures is counted in Billed charges; dismiss this entry unless it states treatment.",
    "not_totaled": "Its amounts were read but not totaled (the internal notes say why), so none of them is in Billed charges; dismiss this entry unless it states treatment.",
    "none": "No amount was read from this record, so its figures are not counted in the Billed charges section; the internal notes name them so you can request the bill.",
}


def _squash(s) -> str:
    return re.sub(r"[^0-9a-z\u20ac\u00a3\u00a5]", "", str(s or "").lower())


def _typed_only(found, state) -> bool:
    """True when the amount is only in the SUMMARY and no amount row of the record carries it: a figure she typed (or the AI wrote) that the record does not state, so
    where the record's charges are counted has nothing to do with it."""
    if not found or found.get("excerpt") or not found.get("summary"):
        return False
    texts = _squash(getattr(state, "texts", ""))
    return not any(_squash(x) and _squash(x) in texts for x in found["summary"])


def bill_sentence(state, found=None) -> str:
    """The true sentence about where the figures of a held entry's record are counted ('' when unknown, or when the figure is only in the summary and not on the record).
    It never says a bill's charges are listed unless one is, and never says no charge was read when amounts were read."""
    if found is not None and _typed_only(found, state):
        return ""
    return _BILL_SENTENCE.get(state, "")


def hold_why(found: dict, state=None) -> str:
    """The item's `why` for CHARGE_TEXT_IN_ENTRY. `found` = check(...) of the current wording; `state` = bill_state(...) or None."""
    what = "quote" if found.get("excerpt") and not found.get("summary") else "summary" if found.get("summary") and not found.get("excerpt") else "summary or quote"
    fix = ("Dismiss it, or pick a quote without the amount and edit the summary to match." if found.get("excerpt")
           else "Dismiss it, or edit the summary to remove the amount.")
    return f"The {what} states a dollar amount, which goes only in the internal notes, so this entry is held out of the letter. {fix} {bill_sentence(state, found)}".strip()


def message(found: dict, state=None) -> str:
    """Plain words for a failed check (the first thing to fix, then the next step). Amounts go only in the internal notes. Every remedy named here is one the review
    code accepts: dismiss always clears the hold; a new quote needs the summary to match it in the same edit; a summary edit alone works only when the quote is clean.
    `state` (bill_state) adds the true sentence about where this record's figures are counted."""
    quote, summ = found.get("excerpt"), found.get("summary")
    tail = (" " + bill_sentence(state, found)) if bill_sentence(state, found) else ""
    if quote:
        return (f"The quote states a dollar amount ({', '.join(quote)}). Amounts go only in the internal notes, never in the letter. "
                "Change the quote to sentences that do not state it" + (" and edit the summary to match in the same edit" if summ else " (and make sure the summary matches the new quote)")
                + ", or dismiss this entry." + tail)
    return (f"The summary states a dollar amount ({', '.join(summ)}). Amounts go only in the internal notes, never in the letter. "
            "Edit the summary to remove it, or dismiss this entry." + tail)


def next_action_code(found: dict) -> str:
    return "EDIT_QUOTE" if found.get("excerpt") else "EDIT_SUMMARY"


def trim_summary(summary: str) -> dict:
    """Remove currency clauses from the end of `summary` (D-054 suffix rule). {'text', 'removed': [clause...], 'changed'}; unchanged (text == summary) when a rule says no."""
    s = summary or ""
    unchanged = {"text": s, "removed": [], "changed": False}
    clauses = summary_trim.split_clauses(s)
    drop = [has_currency(c[0]) for c in clauses]
    if not any(drop) or drop[0]:                                    # nothing to do; the first clause is never removed
        return unchanged
    cut = drop.index(True)
    if not all(drop[cut:]):                                         # suffix only: a kept clause can never follow a removed one
        return unchanged
    kept = clauses[:cut]
    if len(summary_trim.content_words(" ".join(c[0] for c in kept))) < 2:       # the kept prefix must be a summary, not a stub
        return unchanged
    out = ""
    for i, (text, sep) in enumerate(kept):
        piece = text.rstrip(" .;,")
        if i == len(kept) - 1:
            out += piece
        else:
            joiner = sep.strip()
            out += piece + (". " if joiner == "." else f"{joiner} " if joiner in (";", ",") else sep or " ")
    if s.rstrip().endswith("."):
        out += "."
    return {"text": out, "removed": [c[0].rstrip(" .;,") for c in clauses[cut:]], "changed": True}


def narrow_excerpt(excerpt: str):
    """Drop the currency-bearing sentences at the start and/or end of a multi-sentence quote. Returns {'excerpt', 'dropped': [sentence...]} or None when narrowing is impossible:
    a single sentence; every sentence states an amount; an amount in the MIDDLE (a contiguous run cannot skip it); or fewer than 2 content words would be left.
    The narrowed text is a verbatim substring of `excerpt` made of whole sentences (the shared sentence splitter, sentences.py). The caller re-runs every rung-1
    check on it (generator.verify) and keeps it only if nothing new fails; it never rewrites a word."""
    text = excerpt or ""
    spans = sentences.stripped_spans(text)
    if len(spans) < 2:
        return None
    bad = [has_currency(text[a:b]) for a, b in spans]
    if not any(bad) or all(bad):
        return None
    lo, hi = 0, len(spans) - 1
    while bad[lo]:
        lo += 1
    while bad[hi]:
        hi -= 1
    if any(bad[lo:hi + 1]):                                         # an amount in the middle
        return None
    kept = text[spans[lo][0]:spans[hi][1]]
    if len(summary_trim.content_words(kept)) < 2:
        return None
    if not kept.rstrip().endswith((".", "!", "?")):                  # adjuster r2: a line break splits a label from its figure ('... 12 visits. TOTAL' / 'CHARGE 49100.'); never keep half a sentence
        return None
    return {"excerpt": kept, "dropped": [text[a:b] for i, (a, b) in enumerate(spans) if bad[i]]}
