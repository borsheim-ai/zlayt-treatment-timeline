/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
  const mode = new URLSearchParams(location.search).get("api") || API_MODE;
  ZL.API_MODE = mode;

  class ApiError extends Error {
    constructor(status, err) { super((err && err.message) || "Something went wrong. Try again."); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }   // T-166 F7: never a raw "Request failed" or an HTTP status on screen
  }
  ZL.ApiError = ApiError;

  async function call(method, path, body) {
    let status, data;
    if (mode === "mock") {
      ({ status, body: data } = await ZL.mock.handle(method, path, body));
    } else {
      let res;
      try { res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined }); }
      catch (_) { throw new ApiError(0, { code: "network", message: "Could not reach the app. Check your connection and try again." }); }   // T-166 F7: not "Failed to fetch"
      status = res.status;
      try { data = await res.json(); } catch (_) { data = null; }
    }
    if (status >= 400) throw new ApiError(status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + encodeURIComponent(token);
  ZL.api = {
    health: () => call("GET", "/health"),
    createCase: (payload) => call("POST", "/cases", payload),          // {text} or {sample:true}
    cases: () => call("GET", "/cases"),                                  // T-148: the case list (local mode only; 404 otherwise)
    getCase: (token) => call("GET", t(token)),
    rename: (token, title) => call("PATCH", t(token), { title }),         // T-157: name a case; returns {token, title}
    run: (token, confirm_rerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirm_rerun }),
    status: (token) => call("GET", t(token) + "/status"),
    item: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id)),
    trace: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id) + "/trace"),
    caseTrace: (token) => call("GET", t(token) + "/trace"),
    judges: (token) => call("GET", t(token) + "/judges"),
    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + encodeURIComponent(rid) + "/confirm_date", { date }),
    rejudge: (token) => call("POST", t(token) + "/rejudge"),            // D-044: run the second AI check again for accepted items it never checked
    dismissalSuggestions: (token) => call("GET", t(token) + "/dismissal_suggestions"),                      // T-089: read-only list
    applyDismissal: (token, key) => call("POST", t(token) + "/dismissal_suggestions/apply", { key }),   // T-089: only ever called from the paralegal's click
    calibration: () => call("GET", "/calibration"),                                                      // T-099: {status, calibration, message}
    exportCase: (token, style) => call("GET", t(token) + "/export" + (style && style !== "standard" ? "?style=" + encodeURIComponent(style) : "")),   // T-121: style=oneline
    remove: (token) => call("DELETE", t(token)),
  };
})();
