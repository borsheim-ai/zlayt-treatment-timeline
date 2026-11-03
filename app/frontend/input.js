/* Input view: paste or .txt upload -> POST /cases -> "N records found" BEFORE any model call -> Run. (R-IN-1, R-IN-2, R-IN-4) */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  const PDF_MSG = "PDF files can't be read here. Save the records as plain text (.txt) or paste them.";
  let busy = false, pending = null; // pending = {text} read from an uploaded file

  // T-174 F15: an error says what happened and offers the ONE next step as a button (btn-error-action). The box keeps its test id and its text; the button is inside it.
  // `extra` (T-174 r2) adds a second button and a one-line note, for the demo's "this is not a recorded case" refusal: { also: {label, testid, run}, note }.
  let refusing = false;   // T-204: the demo refusal is on screen, so it is rebuilt when the library list arrives late
  function showError(msg, action, extra) {
    refusing = !!(msg && extra && extra.refusal);
    const box = ZL.$("#input-error"); if (!box) return;
    clear(box);
    if (msg) box.append(el("span", { class: "error-text" }, msg));
    if (msg && action) box.append(" ", el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-error-action", onclick: action.run }, action.label));
    if (msg && extra && extra.also) box.append(" ", el("button", { type: "button", class: "btn btn--sm", "data-testid": extra.also.testid, onclick: extra.also.run }, extra.also.label));
    if (msg && extra && extra.note) box.append(el("span", { class: "error-note", "data-testid": "error-live-note" }, extra.note));
    box.hidden = !msg;
  }
  const toText = () => ({ label: "Edit the text", run: () => { const t = ZL.$("#paste"); if (t) { t.focus(); t.scrollIntoView({ block: "center" }); } } });
  const toFile = (label) => ({ label: label || "Choose a .txt file", run: () => { const f = ZL.$("#file"); if (f) f.click(); } });
  const useSample = () => ({ label: "Use the sample case", run: async () => { if (ZL.state.get().token) await startOver(); create({ sample: true }); } });
  // The sample preview is not a case she made: it exists only so she can see "9 records found" before any model call. If she leaves it without pressing Analyze it is removed, so the list
  // never shows a "Not analyzed yet" ghost (T-174 F14). Analyze (startRun) makes it hers.
  let previewToken = null;
  function discardPreview(tok) {
    previewToken = null;
    Promise.resolve().then(() => ZL.api.remove(tok)).catch(() => { /* already gone */ }).then(() => { if (ZL.cases && ZL.cases.refresh) ZL.cases.refresh(); });
  }
  ZL.state.subscribe((s) => { if (previewToken && s.token !== previewToken) discardPreview(previewToken); });
  // T-174 r2 F14: closing the tab, reloading or going Back out of the preview also removes it (keepalive lets the DELETE finish after the page is gone), and the address goes back to the empty form.
  let swept = false;
  window.addEventListener("pagehide", () => {
    if (!previewToken || ZL.API_MODE === "mock") return;
    const tok = previewToken; previewToken = null; swept = true;
    try { history.replaceState(null, "", location.pathname + location.search); fetch("/api/cases/" + encodeURIComponent(tok), { method: "DELETE", keepalive: true }).catch(() => {}); } catch (_) { /* leaving anyway */ }
  });
  window.addEventListener("pageshow", (ev) => { if (ev.persisted && swept) location.reload(); });   // restored from the back/forward cache: that preview is gone
  // T-174 r2 F15: the public demo runs only recorded cases (the sample, and in local mode the library). A paste is refused when the case is created. No edit can change that, so the box says
  // so plainly and offers what does work: open the sample, choose a library case (only where the library is on the page), and one line on running live on her own machine.
  const libraryOpen = () => { const sw = ZL.$("#case-switcher"); return sw && !sw.hidden && sw.querySelector("[data-testid=library-list] button") ? sw : null; };
  const chooseLibrary = () => { const sw = libraryOpen(); if (!sw) return; const d = sw.querySelector("details"); if (d) d.open = true; const b = sw.querySelector("[data-testid=library-list] button"); if (b) { b.scrollIntoView({ block: "center" }); b.focus(); } };
  function demoRefusal() {
    const lib = !!libraryOpen();
    showError(lib ? "This demo only runs the recorded sample and library cases, so it can\u2019t analyze other text. Nothing was started." : "This demo only runs the recorded sample case, so it can\u2019t analyze other text. Nothing was started.",
      { label: "Open the sample", run: useSample().run },
      { refusal: true, also: lib ? { label: "Choose a library case", testid: "btn-error-library", run: chooseLibrary } : null, note: " To run your own records, start the app on your own computer with ENABLE_LIVE=1 and a model key." });
  }
  // T-204: the library list loads after the page does (switcher.js announces it). A refusal painted before that said "sample only" and offered no library button; build it again so it matches the page.
  document.addEventListener("zl:switcher", () => { if (refusing) demoRefusal(); });
  async function create(payload, autoRun) {
    if (busy) return; busy = true; showError("");
    try {
      const nm = ZL.$("#case-title"), title = nm && nm.value.trim();
      const resp = await ZL.api.createCase(title ? Object.assign({}, payload, { title }) : payload);
      history.replaceState(null, "", "#/case/" + encodeURIComponent(resp.token));
      const c = await ZL.api.getCase(resp.token);
      previewToken = payload.sample && !autoRun ? resp.token : null;
      ZL.state.set({ token: resp.token, created: resp, case: c, status: null });
      if (autoRun) await startRun();
    } catch (e) {
      if (e.code === "demo_mode_unsupported_input") return demoRefusal();
      const down = !e.status || e.status >= 500;
      showError(e.status >= 500 ? "We couldn\u2019t start the analysis. Your text is still here." : e.message,
        down ? { label: "Try again", run: () => create(payload, autoRun) } : /name|title/i.test(e.message || "") ? { label: "Edit the name", run: () => { const t = ZL.$("#case-title"); if (t) t.focus(); } } : toText());
    } finally { busy = false; }
  }
  function submitText(autoRun) {
    const text = (pending && pending.text != null) ? pending.text : ZL.$("#paste").value;
    const max = ZL.state.get().health && ZL.state.get().health.limits.max_chars;
    if (!text.trim()) return showError("There is no text to read. Paste records or choose a .txt file.", useSample());
    if (max && text.length > max) return showError(`That is ${text.length.toLocaleString("en-US")} characters; the limit is ${max.toLocaleString("en-US")}. Nothing was sent.`, toText());
    create({ text }, autoRun);
  }
  function onFile(ev) {
    const f = ev.target.files && ev.target.files[0]; pending = null; showError("");
    if (!f) return;
    if (/\.pdf$/i.test(f.name) || f.type === "application/pdf") { ev.target.value = ""; return showError(PDF_MSG, toFile()); }
    if (!/\.txt$/i.test(f.name) && f.type && f.type !== "text/plain") { ev.target.value = ""; return showError("Only .txt files are accepted. Paste the text instead, or save the file as plain text.", toFile()); }
    const rd = new FileReader();
    rd.onerror = () => showError("That file could not be read.", toFile("Choose another file"));
    rd.onload = () => { pending = { text: String(rd.result) }; ZL.$("#file-name").textContent = f.name; submitText(); };
    rd.readAsText(f);
  }

  const recList = (c) => el("ul", { class: "reclist", "data-testid": "record-list" }, c.records.map((r) => el("li", {}, `Record ${r.seq}: ${r.source_label} — ${r.date_status === "parsed" || r.date_status === "confirmed" ? ZL.fmtDate(r.date_iso) : r.date_status === "ambiguous" ? "date to confirm" : "no readable date"}`)));
  ZL.renderInput = function (s) {
    const root = ZL.$("#input-body");
    const c = s.case, h = s.health;
    const limitTxt = "Limit: " + (h ? h.limits.max_chars.toLocaleString("en-US") : "—") + " characters. Plain text only; PDFs are not supported.";
    if (!c && root.dataset.mode === "form") { const l = ZL.$("#limit-note"); if (l) l.textContent = limitTxt; return; } // keep what she typed
    clear(root); root.dataset.mode = c ? "case" : "form";
    const hd = ZL.$("#h-input"); if (hd) hd.textContent = c ? "Records" : "New case";
    if (!c) {
      root.append(
        el("label", { for: "case-title", class: "lbl" }, "Case name (optional)"),
        el("input", { id: "case-title", type: "text", "data-testid": "input-title", maxlength: "120", autocomplete: "off", placeholder: "Client or matter" }),
        el("label", { for: "paste", class: "lbl" }, "Paste the records (each starts with a line like “=== Record 1 ===”)"),
        el("textarea", { id: "paste", "data-testid": "input-text", rows: "9", spellcheck: "false", placeholder: "=== Record 1 ===\nDate: 2026-01-09\nSource: ...\nExcerpt: \"...\"" }),
        el("div", { class: "row" },
          el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-analyze", onclick: () => { pending = null; submitText(true); } }, "Analyze"),
          el("label", { class: "btn", for: "file" }, "Upload .txt"),
          el("input", { id: "file", type: "file", accept: ".txt,text/plain", "data-testid": "file-input", class: "sr", onchange: onFile }),
          el("button", { type: "button", class: "btn", "data-testid": "btn-sample", onclick: () => create({ sample: true }) }, "Use the sample case"),
          el("span", { id: "file-name", class: "muted" })),
        el("p", { id: "input-error", class: "error", role: "alert", "data-testid": "error", hidden: true }),
        el("p", { id: "limit-note", class: "muted small" }, limitTxt));
      return;
    }
    const n = c.records ? c.records.length : 0;
    const running = c.status === "running" || (s.status && s.status.status === "running");
    const failed = s.status && s.status.status === "failed";
    if (running && !runStart) runStart = Date.now(); if (!running) runStart = 0;
    root.classList.toggle("input-done", c.status === "ready");   // a finished run folds the records card into one line above the work
    root.append(...[
      el("p", { class: "found", "data-testid": "record-count", role: "status" }, `${n} ${n === 1 ? "record" : "records"} found`),
      c.status === "ingested" && !running ? el("p", { class: "muted small" }, "Read by code only. No model has been called yet.") : null,
      c.status === "ready" ? el("details", { class: "reclist-wrap" }, el("summary", {}, `Records (${n})`), recList(c)) : recList(c),
      running ? runningNode(s) : null,
      el("div", { class: "row" },
        c.status === "ingested" && !running ? el("button", { type: "button", class: "btn btn--primary", "data-testid": "btn-analyze", onclick: startRun }, "Analyze") : null,
        el("button", { type: "button", class: running ? "btn btn--ghost" : "btn", "data-testid": "start-over", onclick: startOver }, "Start over")),
      failed ? el("div", { class: "notice notice--bad", role: "alert", "data-testid": "run-error" },
        el("div", { class: "notice-body" }, el("strong", {}, "The analysis did not finish. "), "Your records are kept and finished items are saved. ", (s.status.error && s.status.error.message) || ""),
        el("button", { type: "button", class: "btn", "data-testid": "btn-retry-run", onclick: startRun }, "Try again")) : null,
      el("p", { id: "input-error", class: "error", role: "alert", "data-testid": "error", hidden: true })].filter(Boolean));
  };
  // ---- processing state: a real progress element, the stage in plain words, elapsed seconds after a while, skeleton rows. No raw stage names.
  let runStart = 0;
  const STAGE = { ingest: "Splitting the records", split: "Splitting the records", dates: "Reading dates", extract: "Drafting summaries", verify: "Checking quotes against the records", grounding: "Checking quotes against the records",
    judge_entries: "Second check by another model", judge: "Second check by another model", amounts: "Reading amounts", conflicts: "Comparing records", flags: "Looking for gaps and flags", judge_flags: "Second check of the flags", finalize: "Finishing" };
  function stageOf(label) {
    const m = /Step\s+(\d+)\s+of\s+(\d+):\s*([A-Za-z_]+)/.exec(label || "");
    if (m) return { n: +m[1], of: +m[2], text: STAGE[m[3]] || "Working" };
    return { n: 0, of: 0, text: label && !/_/.test(label) ? label : "Working" };
  }
  function runningNode(s) {
    const st = stageOf(s.status && s.status.progress && s.status.progress.label), secs = Math.round((Date.now() - runStart) / 1000);
    return el("div", { class: "run-state", "aria-busy": "true", "data-testid": "run-state" },
      el("p", { class: "progress", "data-testid": "status-stage", role: "status" }, st.text + (st.of ? " (step " + st.n + " of " + st.of + ")" : "…") + (secs >= 15 ? " · still working, " + secs + " s" : "")),
      st.of ? el("progress", { max: String(st.of), value: String(Math.max(st.n - 1, 0)), "aria-label": "Analysis progress" }) : el("progress", { "aria-label": "Analysis progress" }),
      el("div", { class: "skeletons", "aria-hidden": "true" }, [1, 2, 3, 4, 5].map(() => el("div", { class: "skeleton" }))));
  }
  async function startRun() {
    const s = ZL.state.get(); showError(""); previewToken = null;   // Analyze: from here the case is hers
    ZL.state.set({ status: { status: "running", progress: { label: "Starting\u2026" } } });
    try { await ZL.api.run(s.token, false); ZL.pollRun(); }
    catch (e) {
      ZL.state.set({ status: null });   // not running after all: the records card shows its Analyze button again
      if (e.code === "demo_mode_unsupported_input") return demoRefusal();
      showError(!e.status || e.status >= 500 ? "The analysis did not start. Your records are kept." : e.message, { label: "Try again", run: startRun });   // the button says "Try again"; the sentence does not repeat it
    }
  }
  async function startOver() {
    const s = ZL.state.get(); try { if (s.token) await ZL.api.remove(s.token); } catch (_) { /* already gone */ }
    pending = null; history.replaceState(null, "", location.pathname + location.search);
    ZL.state.set({ token: null, created: null, case: null, status: null });
  }
  ZL.startOver = startOver;
})();
