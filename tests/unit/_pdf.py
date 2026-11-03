"""Minimal hand-built text PDFs for tests (no PDF library needed): one page per list entry, one text line per list item."""


def _esc(s: str) -> bytes:
    return s.encode("cp1252").replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def make_pdf(pages: list, image_only: bool = False) -> bytes:
    """pages: [[line, ...], ...]. image_only=True draws a rectangle instead of text (a stand-in for a scan: no text layer)."""
    objs = []
    n = len(pages)
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n))
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode())
    for i, lines in enumerate(pages):
        page_no, content_no = 3 + 2 * i, 4 + 2 * i
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 2000 800] /Contents {content_no} 0 R "
                    f"/Resources << /Font << /F1 {3 + 2 * n} 0 R >> >> >>".encode())
        if image_only:
            stream = b"0.5 g 50 50 400 300 re f"
        else:
            parts = [b"BT /F1 8 Tf 9 TL 20 780 Td"]
            for ln in lines:
                parts.append(b"(" + _esc(ln) + b") Tj T*")
            parts.append(b"ET")
            stream = b"\n".join(parts)
        objs.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    out, offs = bytearray(b"%PDF-1.4\n"), []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    x = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode() + b"0000000000 65535 f \n"
    for o in offs:
        out += f"{o:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{x}\n%%EOF\n".encode()
    return bytes(out)


def sample_pdf(raw: str, split_after_record: int = 5) -> bytes:
    """The golden sample as a 2-page text PDF: records up to `split_after_record` on page 1, the rest on page 2."""
    lines = raw.split("\n")
    cut = next(i for i, l in enumerate(lines) if l == f"=== Record {split_after_record + 1} ===")
    return make_pdf([lines[:cut], lines[cut:]])
