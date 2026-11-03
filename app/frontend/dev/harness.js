/* Dev harness: renders a minimal queue + entries + the T-043 panels against the mock store. Not part of the product. */
(function () {
  const ZL = window.ZL, el = ZL.el;
  const c = ZL.devCase(new URLSearchParams(location.search).get("case") || "sample");
  ZL.openSource = (spans, title) => {   // stand-in with the same signature as source.js: (spans, title)
    const m = document.getElementById("modal"); ZL.clear(m); m.hidden = false; m.append(el("h3", {}, title));
    m.append(el("button", { "data-testid": "btn-close-modal", onclick: () => { m.hidden = true; } }, "Close"));
    spans.forEach((s) => { const r = ZL.state.get().case.records.find((x) => x.id === s.record_id); m.append(el("pre", {}, "Record " + r.seq + "\n" + r.text));
      m.append(el("mark", { "data-testid": "record-highlight" }, r.text.slice(s.start - r.char_start, s.end - r.char_start))); });
  };
  function render(s) {
    const cs = s.case; if (!cs) return;
    const q = document.getElementById("queue"); ZL.clear(q);
    (cs.review.queue || []).forEach((id) => { const f = ZL.rv.find(cs, id); if (f) q.append(el("li", { tabindex: "0", "data-item-id": id, "data-state": f.item.state }, id + " " + ZL.rv.label(f.item))); });
    const en = document.getElementById("entries"); ZL.clear(en);
    cs.entries.forEach((e) => { const row = el("div", { class: "ent", "data-testid": "entry-" + e.seq, "data-review": e.review_status, "data-item-id": e.id },
      el("div", { "data-testid": "entry-summary" }, e.summary), el("div", {}, ZL.rv.chips(e)));
      ZL.hooks.rowActions.forEach((f) => f(e, row)); en.append(row); });
    const mount = document.getElementById("side-panels"); ZL.hooks.panels.forEach((f) => f(cs, mount));
  }
  ZL.state.subscribe(render);
  ZL.state.set({ token: c.token, case: c });
})();
