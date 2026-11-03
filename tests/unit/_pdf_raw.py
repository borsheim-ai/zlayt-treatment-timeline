"""Hand-built PDFs for the hidden-text and OCR tests (T-086/T-087): raw content streams, and an image-only 'scan' made by rendering a
text PDF with pypdfium2 and embedding the pixels as an image with no text layer. All text is SYNTHETIC."""
import zlib


def build(content: bytes, mediabox: str = "0 0 600 800", image: tuple = None) -> bytes:
    """One page. `image` = (gray_bytes, width, height): drawn full-page, no text layer unless `content` adds one."""
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            (f"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >>"
             + (" /XObject << /Im1 6 0 R >>" if image else "") + " >> >>").encode(),
            b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    if image:
        gray, w, h = image
        z = zlib.compress(gray)
        objs.append(f"<< /Type /XObject /Subtype /Image /Width {w} /Height {h} /ColorSpace /DeviceGray /BitsPerComponent 8 "
                    f"/Filter /FlateDecode /Length {len(z)} >>\nstream\n".encode() + z + b"\nendstream")
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


def text_page(lines, size=14, x=50, y=740, lead=22) -> bytes:
    parts = [b"BT /F1 %d Tf %d TL %d %d Td" % (size, lead, x, y)]
    for ln in lines:
        parts.append(b"(" + ln.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("latin-1") + b") Tj T*")
    parts.append(b"ET")
    return b"\n".join(parts)


def scanned_copy(pdf_bytes: bytes, scale: float = 2.0) -> bytes:
    """An image-only PDF that looks like `pdf_bytes` page 1 when shown (no text layer)."""
    import pypdfium2 as pdfium
    page = pdfium.PdfDocument(pdf_bytes)[0]
    bm = page.render(scale=scale)
    w, h, stride, ch = bm.width, bm.height, bm.stride, bm.n_channels
    buf = bytes(bm.buffer)
    gray = b"".join(buf[y * stride + 1: y * stride + w * ch: ch] for y in range(h))
    return build(b"q 600 0 0 800 0 0 cm /Im1 Do Q", image=(gray, w, h))


def build_pages(contents: list, mediabox: str = "0 0 600 800") -> bytes:
    """Several text pages: one content stream each (Helvetica as /F1)."""
    n = len(contents)
    kids = " ".join(f"{3 + 2 * i} 0 R" for i in range(n))
    objs = [b"<< /Type /Catalog /Pages 2 0 R >>", f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode()]
    for i, c in enumerate(contents):
        objs.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [{mediabox}] /Contents {4 + 2 * i} 0 R "
                    f"/Resources << /Font << /F1 {3 + 2 * n} 0 R >> >> >>".encode())
        objs.append(b"<< /Length %d >>\nstream\n" % len(c) + c + b"\nendstream")
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
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
