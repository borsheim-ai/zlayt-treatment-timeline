"""Advisory scan for instruction-like text in records (lexicon `injection`) and prompt delimiters. D-005, ADR-008.3, row 14.
A hit never strips or edits text; it tags the record. The scan is a floor, not a defence: the real controls are per-record
LLM passes, nonce delimiters and review."""
import re

from app.backend import lexicon


def scan(text: str) -> list:
    """[{id, phrase, start, end}] sorted by start; offsets index into `text`."""
    hits = []
    for e in lexicon.code_list("injection"):
        for m in e["regex"].finditer(text or ""):
            start, end = m.start(), m.end()
            while start < end and text[start] in ".\n \t":   # role_label includes its sentence/line lead-in
                start += 1
            hits.append({"id": e["id"], "phrase": text[start:end], "start": start, "end": end})
    return sorted(hits, key=lambda h: (h["start"], h["end"]))


_LOOKALIKE = re.compile(r"<(\s*/?\s*record-)", re.IGNORECASE)


def wrap(text: str, nonce: str) -> str:
    """Wrap record text in nonce delimiters; any `<record-` / `</record-` lookalike inside the text is neutralised in this prompt copy."""
    safe = _LOOKALIKE.sub(r"&lt;\1", text)
    return f"<record-{nonce}>\n{safe}\n</record-{nonce}>"
