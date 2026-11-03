/* Guided UI core (T-181, D-068). Namespace G: safe DOM builder, URLs, the API wrapper, the case store and the step-state rules (spec 9.1-9.2).
   No innerHTML anywhere: record text, quotes and titles go in with textContent (spec section 0, "Untrusted text"; CSP stays script-src 'self').
   CSP also blocks inline style ATTRIBUTES: set sizes from code with el.style.width = ... (CSSOM is allowed) and never write style="..." in markup. */
(function () {
  const G = (window.G = window.G || {});
  G.pages = {};           // G.pages.home | new | records | timeline | bills | letter = async (ctx) => optional cleanup fn   (see app.js, "page contract")
  G.LABELS = [["Add records", "Records"], ["Check the timeline", "Timeline"], ["Check the bills", "Bills"], ["Get your letter", "Letter"]];

  /* h("button", { class: "btn", onclick: fn, "data-testid": "x" }, "text", node, ...) -> element. on* attributes are listeners; text becomes text nodes. */
  G.h = function (tag, attrs, ...kids) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v == null || v === false) continue;
      if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
      else if (k === "class") el.className = v;
      else if (k === "text") el.textContent = v;
      else el.setAttribute(k, v === true ? "" : String(v));
    }
    for (const kid of kids.flat(Infinity)) if (kid != null && kid !== false) el.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
    return el;
  };
  G.$ = (sel, root) => (root || document).querySelector(sel);
  G.$$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));

  const enc = encodeURIComponent;
  G.url = {
    home: () => "/", new: () => "/new",
    records: (t) => "/case/" + enc(t) + "/records",
    timeline: (t, item) => "/case/" + enc(t) + "/timeline" + (item ? "?item=" + enc(item) : ""),
    bills: (t, item) => "/case/" + enc(t) + "/bills" + (item ? "?item=" + enc(item) : ""),
    letter: (t) => "/case/" + enc(t) + "/letter",
    step: (t, n, item) => [null, G.url.records, G.url.timeline, G.url.bills, G.url.letter][n](t, item),
  };

  /* Tiny event bus: G.on("case", fn) fires when the store learns a case (token, json). */
  const subs = {};
  G.on = (ev, fn) => { (subs[ev] = subs[ev] || []).push(fn); return () => { subs[ev] = (subs[ev] || []).filter((f) => f !== fn); }; };
  G.emit = (ev, ...a) => (subs[ev] || []).slice().forEach((f) => { try { f(...a); } catch (e) { console.error(e); } });

  /* ---- API wrapper over the existing /api. Failures become G.ApiError with a message a first-time user can read: never an HTTP status, "Failed to fetch" or a stack. ---- */
  const FALLBACK = {
    0: "We couldn't reach the app. Check your connection and try again.",
    404: "We couldn't find that. It may have been deleted.",
    413: "That is too long for us to read in one go. Try a shorter piece.",
    429: "That was a lot at once. Wait a moment and try again.",
  };
  class ApiError extends Error {
    constructor(status, err) {
      const plain = err && typeof err.message === "string" && err.message && status < 500 ? err.message : null;     // server sentences are shown as given (spec section 0)
      super(plain || FALLBACK[status] || (status >= 500 ? "Something went wrong on our side. Try again in a moment." : "Something went wrong. Try again."));
      this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; this.raw = err || null;
    }
  }
  G.ApiError = ApiError;
  async function call(method, path, body, signal) {
    let res, data = null;
    try { res = await fetch("/api" + path, { method, signal, headers: body !== undefined && body !== null ? { "Content-Type": "application/json" } : {}, body: body !== undefined && body !== null ? JSON.stringify(body) : undefined }); }
    catch (e) { if (e && e.name === "AbortError") throw e; throw new ApiError(0, null); }
    try { data = await res.json(); } catch (_) { data = null; }
    if (res.status >= 400) throw new ApiError(res.status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + enc(token);
  G.api = {
    call,
    health: (s) => call("GET", "/health", null, s),
    cases: (s) => call("GET", "/cases", null, s),                                          // local mode only; 404 elsewhere (spec 3.3)
    createCase: (payload, s) => call("POST", "/cases", payload, s),                         // {text} or {sample:true}
    getCase: (token, s) => call("GET", t(token), null, s),
    rename: (token, title) => call("PATCH", t(token), { title }),
    remove: (token) => call("DELETE", t(token)),
    run: (token, confirmRerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirmRerun }),
    status: (token, s) => call("GET", t(token) + "/status", null, s),
    item: (token, id, s) => call("GET", t(token) + "/items/" + enc(id), null, s),
    review: (token, id, body) => call("POST", t(token) + "/items/" + enc(id) + "/review", body),
    addEntry: (token, rid, body) => call("POST", t(token) + "/records/" + enc(rid) + "/entry", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + enc(rid) + "/confirm_date", { date }),
    rejudge: (token) => call("POST", t(token) + "/rejudge"),
    trace: (token, s) => call("GET", t(token) + "/trace", null, s),
    itemTrace: (token, id, s) => call("GET", t(token) + "/items/" + enc(id) + "/trace", null, s),          // T-211: the per-item check trace ("How this was checked")
    exportCase: (token, s) => call("GET", t(token) + "/export", null, s),
  };

  /* ---- store: health and the cases this tab has loaded. Pages call ctx.refresh() after a write so the step bar and header follow. ---- */
  /* The server's health, once (shared with the shell's own request). `local_mode` (T-181 r2) says whether the list of cases and the test-case library exist: when it is false the page never asks for them,
     so a first paint makes no request that is going to fail. An older server without the field is asked (and a 404 there is expected). */
  G.healthNow = async function (signal) {
    if (G.store.health) return G.store.health;
    try { const hl = await (G.store.healthP || G.api.health(signal)); G.store.health = G.store.health || hl; return hl || {}; }
    catch (e) { if (e && e.name === "AbortError") throw e; return {}; }
  };
  G.store = {
    health: null, cases: {},
    async load(token, signal) { const c = await G.api.getCase(token, signal); return G.store.put(token, c); },
    put(token, c) { G.store.cases[token] = c; G.emit("case", token, c); return c; },
  };

  /* ---- step rules (spec 9.1, 9.2): one definition, used by the step bar and (via fromSummary) by Your cases ---- */
  const live = (i) => i && i.state !== "rejected";
  const undecided = (i) => live(i) && (i.review_status === "pending" || !!i.edit_to_check);       // 9.1
  const norm = {
    fromCase(c) {
      const s2 = [].concat(c.entries || [], c.undated_entries || [], c.flags || []).filter(live), s3 = (c.amounts || []).filter(live);
      return { status: c.status, hasItems: s2.length + s3.length + (c.tray || []).length > 0, stage: null, stages: 8,
        s2: { total: s2.length, left: s2.filter(undecided).length }, s3: { total: s3.length, left: s3.filter(undecided).length }, ready: !!(c.review && c.review.ready_to_export) };
    },
    fromSummary(c) {          // one row of GET /api/cases
      const p = c.progress || {}, e = p.entries || { decided: 0, total: 0 }, f = p.flags || { decided: 0, total: 0 }, a = p.amounts || { decided: 0, total: 0 };
      return { status: c.status, hasItems: e.total + f.total + a.total > 0, stage: c.run ? c.run.steps_done : null, stages: (c.run && c.run.steps_total) || 8,
        s2: { total: e.total + f.total, left: e.total + f.total - e.decided - f.decided }, s3: { total: a.total, left: a.total - a.decided }, ready: !!c.export_ready };
    },
  };
  /* G.steps.states(input, hereStep) -> [{ n, state: "done"|"todo"|"attn"|"locked", status }] for the four steps. `input` is GET case JSON or one /api/cases row (detected by `progress.entries`).
     Current-ness is the page's, not the data's: the caller marks hereStep. Step 4 reads "Ready" from the same flag the list uses; a page that knows more (a blocker count) overrides with setStepStatus. */
  G.steps = {
    undecided, live,
    states(input, here) {
      const x = input && input.progress && input.progress.entries ? norm.fromSummary(input) : norm.fromCase(input || {});
      const unlocked = x.status === "ready" || (x.status === "failed" && x.hasItems);
      const out = [];
      const s1 = x.status === "ready" ? { state: "done", status: "Done" } : x.status === "running" ? { state: "todo", status: x.stage != null ? `Drafting ${Math.min(x.stage + 1, x.stages)} of ${x.stages}` : "Drafting" }
        : x.status === "failed" ? { state: "attn", status: "Run again" } : { state: "todo", status: "Not started" };
      out.push(s1);
      const two = !unlocked ? { state: "locked", status: "After step 1" } : x.s2.left === 0 ? { state: "done", status: "Done" } : { state: "todo", status: `${x.s2.left} of ${x.s2.total} left` };
      const three = !unlocked ? { state: "locked", status: "After step 1" } : x.s3.total === 0 ? { state: "done", status: "None found" } : x.s3.left === 0 ? { state: "done", status: "Done" }
        : { state: "todo", status: x.s3.left === x.s3.total ? `${x.s3.total} amount${x.s3.total === 1 ? "" : "s"}` : `${x.s3.left} of ${x.s3.total} left` };
      out.push(two, three);
      const ok = unlocked && two.state === "done" && three.state === "done";
      out.push(!unlocked ? { state: "locked", status: "After step 1" } : ok && x.ready ? { state: "todo", status: "Ready" } : { state: "todo", status: "Not yet" });
      out.forEach((s, i) => { s.n = i + 1; if (here && s.state === "todo" && i + 1 < here && (i === 1 || i === 2)) s.state = "attn"; });      // a step she left with undecided items needs a look
      return out;
    },
    /* counts for the title row ("Item N of M", "3 answered - 16 to go"): { total, left } */
    counts(c) { const x = norm.fromCase(c); return { step2: x.s2, step3: x.s3 }; },
  };

  /* A plain error block: message + Try again (when `retry` is given) + a way home. Used by the shell and available to pages. */
  G.errorBlock = function (err, retry, title) {
    const msg = err instanceof ApiError ? err.message : "Something went wrong. Try again.";
    return G.h("div", { class: "errbox", role: "alert", "data-testid": "page-error" },
      G.h("h1", { "data-testid": "page-title" }, title || "Something went wrong"), G.h("p", {}, msg),
      G.h("div", { class: "row-actions" },
        retry ? G.h("button", { type: "button", class: "btn primary lg", "data-testid": "btn-retry", onclick: retry }, "Try again") : null,
        G.h("a", { class: "btn lg" + (retry ? "" : " primary"), href: "/", "data-testid": "link-home" }, "Back to your cases")));
  };
})();
