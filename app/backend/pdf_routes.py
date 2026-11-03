"""GET /api/cases/{token}/pages/{n}/image (T-086): the scanned page beside its OCR text. The PNG was rendered at upload from the
user's own PDF and is stored with the case (config.page_images, base64), so it goes away with the case (DELETE or retention purge).
`add_routes(app, conn=..., get_case=..., ApiError=...)`, the same shape as the other route modules."""
import base64
import binascii

from fastapi import Response


def add_routes(app, *, conn, get_case, ApiError):
    @app.get("/api/cases/{token}/pages/{n}/image")
    def page_image(token: str, n: int):
        c = conn()
        try:
            case = get_case(c, token)
        finally:
            c.close()
        b64 = ((case.get("config") or {}).get("page_images") or {}).get(str(n))
        if not b64:
            raise ApiError(404, "not_found", "No page image for that page.")
        try:
            png = base64.b64decode(b64, validate=True)
        except (binascii.Error, ValueError):
            raise ApiError(404, "not_found", "No page image for that page.") from None
        return Response(content=png, media_type="image/png", headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"})
