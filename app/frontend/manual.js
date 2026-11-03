/* Manual entry for a record in the could-not-verify tray (T-056 B1, D-031). The paralegal picks whole sentences of that record
   (the excerpt is cut from the record text by code, so it is verbatim) and writes her own summary: POST /records/{rid}/entry.
   Server refusals (422, D-047: the reason is shown inline and the typed text stays) are shown in plain words. Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  const draft = {};   // tray item id -> {open, picked:[sentence index], summary}
  const REASON = {
    EXCERPT_NOT_WHOLE_SENTENCE: "The quote must start and end at a sentence boundary.",
    EXCERPT_NOT_VERBATIM: "The quote is not word for word in the record.",
    EXCERPT_OMITS_QUALIFIER: "A hedge sentence in the record qualifies your quote; include it.",
  };

  // Quotable sentences of a record: header lines are not part of any excerpt, and the opening `Excerpt: "` / closing quote are not quoted text.
  function quotable(rec) {
    const out = [];
    (rec.sentences || []).forEach((s) => {
      let a = s.start, b = s.end, txt = rec.text.slice(a - rec.char_start, b - rec.char_start);
      if (/^(===|Date:|Source:)/.test(txt)) return;
      const m = /^Excerpt:\s*"?/.exec(txt); if (m) { a += m[0].length; txt = txt.slice(m[0].length); }
      if (/"\s*$/.test(txt) && !txt.slice(0, -1).includes('"')) { const k = txt.length - txt.replace(/"\s*$/, "").length; b -= k; txt = txt.slice(0, txt.length - k); }
      if (txt.trim()) out.push({ text: txt, start: a, end: b });
    });
    return out;
  }

  function control(c, t, rec) {
    const d = draft[t.id] || (draft[t.id] = { open: false, picked: [], summary: "" });
    const sents = quotable(rec);
    const msg = el("p", { class: "rv-error", role: "alert", "data-testid": "manual-error" });
    const sum = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: "summary", "data-testid": "manual-summary", "aria-label": "Your summary, written from the quote" });
    sum.value = d.summary; sum.addEventListener("input", () => { d.summary = sum.value; });
    const boxes = sents.map((s, i) => {
      const cb = el("input", { type: "checkbox", name: "sent", value: String(i), checked: d.picked.includes(i) || null, onchange: () => { d.picked = boxes.filter((b) => b.input.checked).map((b) => +b.input.value); } });
      return { input: cb, label: el("label", { class: "rv-radio" }, cb, s.text) };
    });
    async function submit() {
      msg.textContent = "";
      const idx = d.picked.slice().sort((a, b) => a - b);
      if (!idx.length) { msg.textContent = "Pick at least one sentence to quote."; return; }
      if (idx.some((v, k) => k && v !== idx[k - 1] + 1)) { msg.textContent = "Pick sentences that sit next to each other in the record."; return; }
      if (!d.summary.trim()) { msg.textContent = "Write your summary of the quote."; return; }
      const a = sents[idx[0]], b = sents[idx[idx.length - 1]];
      const body = { summary: d.summary.trim(), excerpt: rec.text.slice(a.start - rec.char_start, b.end - rec.char_start) };
      const r = await RV.http("POST", "/cases/" + encodeURIComponent(c.token) + "/records/" + encodeURIComponent(rec.id) + "/entry", body);
      if (r.status === 200 || r.status === 201) {
        delete draft[t.id]; ZL.state.set({ case: await ZL.api.getCase(c.token) }); RV.say("Entry added for record " + rec.seq + ". It is not reviewed yet."); return;
      }
      const err = (r.body && r.body.error) || {}, detail = err.detail || {};
      const why = (detail.reasons || []).map((x) => REASON[x]).filter(Boolean);
      msg.textContent = RV.asTyped((err.message || "That entry was refused.") + (why.length ? " " + why.join(" ") : ""), detail.tokens, d.summary);
      RV.say(msg.textContent, true);
    }
    const form = el("form", { class: "rv-edit rv-manual-form", hidden: !d.open, "data-testid": "manual-form", onsubmit: (ev) => { ev.preventDefault(); submit(); } },
      el("fieldset", { class: "rv-fieldset" }, el("legend", {}, "Pick the sentences to quote from Record " + rec.seq + " (whole sentences, next to each other)"),
        sents.length ? boxes.map((b) => b.label) : el("p", { class: "rv-empty", "data-testid": "manual-no-sentences" }, rec.sentences_reason || "This record has no sentences to pick from. Read the record text instead.")),
      el("label", { class: "rv-label" }, "Your summary (written from the quote; numbers and dates must be in the quote)", sum),
      el("div", { class: "rv-actions" }, el("button", { type: "submit", class: "btn btn--primary", "data-testid": "btn-save-manual" }, "Add entry"),
        el("button", { type: "button", class: "btn", onclick: () => toggle(false) }, "Cancel")), msg);
    const open = el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-manual-entry", "aria-expanded": String(d.open), onclick: () => toggle(!d.open) }, "Enter this record by hand");
    function toggle(v) { d.open = v; form.hidden = !v; open.setAttribute("aria-expanded", String(v)); if (v) { const f = form.querySelector("input,textarea"); if (f) f.focus(); } else open.focus(); }
    form.addEventListener("keydown", (ev) => { if (ev.key === "Escape") { ev.stopPropagation(); toggle(false); } });
    return el("div", { class: "rv-manual", "data-testid": "manual-entry", "data-record-id": rec.id }, el("div", { class: "rv-actions" }, open), form);
  }

  RV.registerPanel("manual", (root, c) => {
    ZL.clear(root); root.className = "rv-batchhost"; root.removeAttribute("data-testid");
    const wrap = root.closest('[data-testid="timeline"]'); if (!wrap) return;
    const inTray = {};
    wrap.querySelectorAll('[data-testid="tray-item"]').forEach((node) => {
      const t = (c.tray || []).find((x) => x.id === node.getAttribute("data-item-id"));
      const rec = t && (t.record_ids || []).length === 1 ? (c.records || []).find((r) => r.id === t.record_ids[0]) : null;
      if (!rec || (t.kind && t.kind !== "entry")) return;
      inTray[rec.id] = true;
      if (!node.querySelector(":scope > .rv-manual")) node.append(control(c, t, rec));
    });
    // Records that produced no entry and are not in the tray (for example the model call failed): same control.
    const has = {}; (c.entries || []).concat(c.undated_entries || [], c.tray || []).forEach((e) => (e.record_ids || []).forEach((id) => { has[id] = true; }));
    const toConfirm = {}; (c.dates_to_confirm || []).forEach((d) => { if ((d.candidates || []).length) toConfirm[d.record_id] = true; });  // listed once, under Dates to confirm
    const missing = (c.records || []).filter((r) => !has[r.id] && !inTray[r.id] && !toConfirm[r.id] && !r.duplicate_of);
    if (!missing.length || c.status !== "ready") return;
    root.className = "rv-panel"; root.setAttribute("data-testid", "records-without-entry");
    root.append(el("h2", {}, "Records without an entry (" + missing.length + ")"),
      el("p", { class: "rv-help" }, "These records did not produce an entry, so they are not in the timeline or the letter. Read the record, quote the sentences yourself and write the summary."));
    missing.forEach((r) => {
      const card = el("article", { class: "rv-card", "data-testid": "missing-entry", "data-record-id": r.id },
        el("div", { class: "rv-head" }, el("h3", { class: "rv-title" }, "Record " + r.seq + ": " + r.source_label), el("span", { class: "rv-chip" }, r.date_iso ? ZL.fmtDate(r.date_iso) : "undated")),
        r.date_status === "confirmed" ? el("p", { class: "rv-help", "data-testid": "missing-date-confirmed" }, `Date confirmed: ${ZL.fmtDate(r.date_iso)}. Not on the timeline yet: enter this record by hand below.`) : null,
        r.date_status === "confirmed" && ZL.recordExcerpt && ZL.recordExcerpt(r) ? el("blockquote", { class: "excerpt", "data-testid": "missing-entry-excerpt" }, ZL.recordExcerpt(r)) : null,
        el("div", { class: "rv-actions" }, el("button", { type: "button", class: "btn", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], "Record " + r.seq + ": " + r.source_label) }, "Open record " + r.seq)));
      card.append(control(c, { id: "rec:" + r.id }, r)); root.append(card);
    });
  });
})();
