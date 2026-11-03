/* T-144: "Also in this record, not in an entry (n)" under each entry. Shows records[].uncovered[] (T-143: every sentence of the record that no live entry quote overlaps, computed by code),
   each sentence verbatim, in a list that starts closed (a "Not in an entry (n)" link in the row's head line opens it). "Show in record" opens the source record with that sentence highlighted (ZL.openSource, by the API's offsets).
   Review aid only: it is never in the letter, the notes or the copy text, and `kinds` is a hint the UI does not use (nothing is filtered here). Plugs in through ZL.registerRowActions. */
(function () {
  const ZL = window.ZL, { el } = ZL;
  const opened = new Set();   // entry ids whose list she opened; the rows repaint on every decision, and a list she is reading must stay open

  const recordsOf = (entry) => {
    const c = ZL.state.get().case; if (!c) return [];
    return entry.record_ids.map((rid) => c.records.find((r) => r.id === rid)).filter((r) => r && r.uncovered && r.uncovered.length);
  };

  ZL.registerRowActions((entry, row) => {
    const recs = recordsOf(entry);
    const items = recs.flatMap((r) => r.uncovered.map((u) => ({ rec: r, u })));
    if (!items.length) return;
    const many = recs.length > 1, n = items.length, id = "unc-" + entry.id;
    const who = entry.provider + (entry.date ? ", " + ZL.fmtDate(entry.date) : "");
    const full = `Also in this record, not in an entry (${n})`;
    // The row budget is tight (T-060: a compact row), so the collapsed state costs no height: a short link in the row's head line opens the list below the row. The full wording heads the list.
    const panel = el("section", { class: "unc", id, hidden: !opened.has(entry.id) || null, "data-testid": "uncovered-list", "data-record-count": String(n), "aria-label": full + ": " + who },
      el("h4", { class: "unc-h", "data-testid": "uncovered-heading" }, full),
      el("p", { class: "muted small unc-note" }, "Sentences from this record that no entry quotes. They are not in the letter. To use one, add it by hand or change the quote."),
      el("ul", { class: "unc-list" }, items.map(({ rec, u }) => el("li", { class: "unc-item", "data-testid": "uncovered-item", "data-record-id": rec.id },
        el("span", { class: "unc-text", "data-testid": "uncovered-text" }, u.text),
        el("button", { type: "button", class: "btn btn--link unc-jump", "data-testid": "btn-uncovered-jump",
          "aria-label": `Show in record ${rec.seq}: ${u.text.length > 80 ? u.text.slice(0, 80) + "..." : u.text}`,
          onclick: () => ZL.openSource([{ record_id: rec.id, start: u.start, end: u.end }], `Record ${rec.seq}: ${rec.source_label || who}`) }, many ? `Show in record ${rec.seq}` : "Show in record")))));
    const toggle = el("button", { type: "button", class: "btn btn--link unc-toggle", "data-testid": "uncovered-summary", "aria-expanded": String(opened.has(entry.id)), "aria-controls": id, "aria-label": full + ": " + who,
      onclick: () => { const open = panel.hidden; panel.hidden = !open; toggle.setAttribute("aria-expanded", String(open)); if (open) opened.add(entry.id); else opened.delete(entry.id); } }, `Not in an entry (${n})`);
    // T-160: the link sits in the head line right after the record chip (or the provider), so it shares a line that already exists; at the end of the head it wrapped to a line of its own on a phone.
    const head = row.querySelector(":scope > .entry-head"), anchor = head && (head.querySelector(":scope > .chip--rec") || head.querySelector(":scope > .provider"));
    if (anchor) anchor.after(toggle); else if (head) head.append(toggle); else row.append(toggle);
    row.append(panel);
  });

  // The list is computed by the server from the entries' quotes and states, so it changes when a quote is changed or an entry stops being live. The review responses do not carry it:
  // when any entry's quote or state differs from the last paint, read the case again and take only the records' `uncovered` from it.
  let lastToken = null, lastSig = null, seq = 0;
  const sigOf = (c) => (c.entries || []).concat(c.undated_entries || []).map((e) => [e.id, e.state, e.excerpt_start, e.excerpt_end].join(":")).join("|");
  ZL.state.subscribe((s) => {
    const c = s.case; if (!c || !s.token) { lastToken = lastSig = null; return; }
    const sig = sigOf(c);
    if (s.token !== lastToken) { lastToken = s.token; lastSig = sig; return; }
    if (sig === lastSig) return;
    lastSig = sig;
    const mine = ++seq, token = s.token;
    ZL.api.getCase(token).then((fresh) => {
      const cur = ZL.state.get();
      if (mine !== seq || cur.token !== token || !cur.case || !fresh || !fresh.records) return;
      let changed = false;
      cur.case.records.forEach((r) => {
        const f = fresh.records.find((x) => x.id === r.id);
        if (f && f.uncovered && JSON.stringify(f.uncovered) !== JSON.stringify(r.uncovered)) { r.uncovered = f.uncovered; changed = true; }
      });
      if (changed) ZL.state.set({ case: cur.case });
    }).catch(() => {});   // the list stays as it was; nothing she decided depends on it
  });
})();
