/* Audit drawer (T-058 AC1): per item (Audit button on every card/row) and for the whole case. Shows every model call: role, step, model, backend,
   prompt version and hash, verdict, latency. In local mode the API also returns prompts, responses and edit before/after; those appear
   in collapsed sections. Public mode: metadata only (whatever the API returns is shown, nothing is requested beyond GET /audit). Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  let dlg = null, body = null, title = null;

  function ensure() {
    if (dlg) return;
    title = el("h2", { id: "audit-title", class: "au-title" }, "Audit");
    body = el("div", { class: "au-body" });
    dlg = el("dialog", { id: "audit-drawer", class: "au-drawer", "data-testid": "audit-drawer", "aria-labelledby": "audit-title" },
      el("div", { class: "au-head" }, title, el("button", { type: "button", class: "btn", "data-testid": "btn-close-audit", onclick: () => dlg.close() }, "Close")), body);
    dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    document.body.append(dlg);
  }
  const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "au-kv" }, el("span", { class: "au-k" }, k + " "), String(v)));
  const pre = (label, text) => (text == null || text === "" ? null : el("details", { class: "au-more" }, el("summary", {}, label), el("pre", { class: "au-pre" }, typeof text === "string" ? text : JSON.stringify(text, null, 2))));

  function callRow(c) {
    const rf = c.prepared ? " (prepared answer, not model output)" : c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
    return el("li", { class: "au-call", "data-testid": "audit-call" },
      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.prepared ? el("span", { class: "rv-chip", "data-testid": "audit-prepared" }, "Prepared answer") : null, c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prepared ? null : c.prompt_version), kv("hash", c.prepared || !c.prompt_sha256 ? null : String(c.prompt_sha256).slice(0, 12)),      // D-065: no prompt made a prepared answer
        kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
      pre(c.prepared ? "System prompt (not sent: prepared answer)" : "System prompt (local mode)", c.system_text), pre(c.prepared ? "Record text (not sent: prepared answer)" : "Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
  }
  function eventRow(e, confirmed) {   // a flagged charge's accept names the flag she confirmed (the event's own `confirm` when the server sends it)
    const named = [e.confirm ? "confirmed " + (e.confirm.name || e.confirm.flag) : confirmed, e.compared ? "said she compared it with the quote" : null].filter(Boolean).join(", ");   // D-066
    return el("li", { class: "au-call", "data-testid": "audit-event" }, el("div", { class: "au-line" }, el("strong", {}, e.action + (named ? ", " + named : "")), el("span", { class: "au-k" }, e.at || "")),
      e.before || e.after ? pre("Before and after (local mode)", { before: e.before, after: e.after }) : null);
  }

  RV.openAudit = async function (itemId, label) {
    ensure(); const c = RV.caseNow(); if (!c) return;
    title.textContent = itemId ? "Audit: " + (label || itemId) : "Audit: whole case";
    clear(body); body.append(el("p", { role: "status" }, "Loading…"));
    if (!dlg.open) dlg.showModal();
    const r = await RV.http("GET", "/cases/" + encodeURIComponent(c.token) + "/audit");
    clear(body);
    if (r.status !== 200) { body.append(el("p", { class: "rv-error", role: "alert" }, RV.errMsg(r, "The audit could not be loaded."))); return; }
    const a = r.body, calls = (a.calls || []).filter((x) => !itemId || x.item_id === itemId), events = (a.events || []).filter((x) => !itemId || x.item_id === itemId);
    const s = a.summary || {}, prep = calls.some((x) => x.prepared) || !!(c.models && c.models.generator_prepared), noun = prep ? "call" : "model call";   // T-204 r2: a prepared answer is not a model call
    body.append(el("p", { class: "rv-help", "data-testid": "audit-summary" }, itemId ? `${calls.length} ${noun}${calls.length === 1 ? "" : "s"} for this item.` :
      `${s.calls != null ? s.calls : calls.length} ${noun}s, ${s.latency_ms_total != null ? s.latency_ms_total + " ms total latency" : ""}${s.cost_usd != null ? ", $" + s.cost_usd : ""}${s.by_backend ? ", by backend: " + Object.keys(s.by_backend).map((k) => k + " " + s.by_backend[k]).join(", ") : ""}.`));
    body.append(el("h3", {}, prep ? "Calls" : "Model calls"));
    if (calls.length) body.append(el("ol", { class: "au-list" }, calls.map(callRow)));
    else body.append(el("p", { class: "rv-empty" }, itemId ? "No " + noun + " was made for this item: code computed it." : "No " + noun + "s recorded."));
    body.append(el("h3", {}, "Your decisions"));
    const fn = itemId && ZL.chargeFlagNote ? ZL.chargeFlagNote(itemId, "audit-charge-flag") : null; if (fn) body.append(fn);
    const lastAccept = {}; events.forEach((e) => { if (e.action === "accept") lastAccept[e.item_id] = e; });   // her latest accept is the one the confirm belongs to
    if (events.length) body.append(el("ol", { class: "au-list" }, events.map((e) => eventRow(e, ZL.chargeConfirmWord && lastAccept[e.item_id] === e ? ZL.chargeConfirmWord(e.item_id) : null)))); else body.append(el("p", { class: "rv-empty" }, "No decisions recorded yet."));
  };

  RV.registerPanel("audit", (root, c) => {
    ZL.clear(root);
    root.append(el("h2", {}, "Audit"), el("p", { class: "rv-help" }, ((c && c.models && c.models.generator_prepared) ? "Every call behind this case, and every decision you made." : "Every model call behind this case, and every decision you made.")),
      el("button", { type: "button", class: "btn", "data-testid": "btn-audit-case", onclick: () => RV.openAudit(null) }, "Open full audit"));
  });
})();
