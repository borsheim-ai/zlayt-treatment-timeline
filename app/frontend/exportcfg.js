/* Per-case exhibit / Bates settings (T-058 AC2): fills "[Ex. __ / Bates __]" in the letter text. Leave empty = placeholders stay (default export unchanged).
   GET/PUT/DELETE /api/cases/{token}/export_config; the panel stays hidden when the server answers 404. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, el = ZL.el;
  const cache = {};        // token -> {cfg} | {na:true} | {loading:true}
  const draft = {};        // token -> {exhibit,bates_prefix,bates_start} typed but unsaved
  let hostRef = null;

  async function load(token) {
    cache[token] = { loading: true };
    try {
      const r = await RV.http("GET", "/cases/" + encodeURIComponent(token) + "/export_config");
      cache[token] = r.status === 200 ? { cfg: r.body || {} } : { na: true };
    } catch (_) { cache[token] = { na: true }; }
    const c = RV.caseNow(); if (hostRef && c && c.token === token) draw(hostRef, c);
  }
  const val = (v) => (v == null ? "" : String(v));

  function draw(root, c) {
    ZL.clear(root); const st = cache[c.token];
    if (!st || st.na || st.loading) { root.hidden = true; return; }
    root.hidden = false; root.setAttribute("data-testid", "export-settings");
    const d = draft[c.token] || (draft[c.token] = { exhibit: val(st.cfg.exhibit), bates_prefix: val(st.cfg.bates_prefix), bates_start: val(st.cfg.bates_start) });
    const msg = el("p", { class: "rv-error", role: "status", "data-testid": "export-settings-msg" });
    const field = (key, label, hint, attrs) => el("label", { class: "rv-label es-field" }, label,
      el("input", Object.assign({ type: "text", class: "rv-input", name: key, value: d[key], "data-testid": "cfg-" + key, onInput: null }, attrs || {}, { oninput: (ev) => { d[key] = ev.target.value; } })), el("span", { class: "rv-help" }, hint));
    const form = el("form", { class: "es-form", onsubmit: async (ev) => {
      ev.preventDefault(); msg.textContent = ""; msg.className = "rv-error";
      const body = {}; if (d.exhibit.trim()) body.exhibit = d.exhibit.trim(); if (d.bates_prefix.trim()) body.bates_prefix = d.bates_prefix.trim();
      if (d.bates_start.trim() !== "") { if (!/^\d{1,8}$/.test(d.bates_start.trim())) { msg.textContent = "The first Bates number must be digits only."; return; } body.bates_start = Number(d.bates_start.trim()); }
      const r = await RV.http("PUT", "/cases/" + encodeURIComponent(c.token) + "/export_config", body);
      if (r.status >= 400) { msg.textContent = RV.errMsg(r, "Those settings were refused."); RV.say(msg.textContent, true); return; }
      cache[c.token] = { cfg: r.body || body }; msg.className = "rv-help"; msg.textContent = "Saved. The next export fills the placeholders."; RV.say(msg.textContent);
    } },
      field("exhibit", "Exhibit label", "Replaces the Ex. blank, for example 7 or B-2."),
      field("bates_prefix", "Bates prefix", "For example RIV-"),
      field("bates_start", "First Bates number", "Numbers run in record order from this value.", { inputmode: "numeric" }),
      el("div", { class: "rv-actions" },
        el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-config" }, "Save settings"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-reset-config", onclick: async () => {
          const r = await RV.http("DELETE", "/cases/" + encodeURIComponent(c.token) + "/export_config");
          if (r.status >= 400 && r.status !== 404) { msg.textContent = RV.errMsg(r, "Could not restore the defaults."); return; }
          cache[c.token] = { cfg: {} }; draft[c.token] = { exhibit: "", bates_prefix: "", bates_start: "" }; draw(root, c); RV.say("Placeholders restored.");
        } }, "Use the blank placeholders")), msg);
    root.append(el("h2", {}, "Exhibit and Bates numbers"), el("p", { class: "rv-help" }, "Optional. Fills “Source [Ex. __ / Bates __]” in the letter text. Left empty, the blanks stay for you to fill in."), form);
  }
  RV.registerPanel("export-settings", (root, c) => {
    hostRef = root;
    if (!cache[c.token]) load(c.token); else draw(root, c);
  });
})();
