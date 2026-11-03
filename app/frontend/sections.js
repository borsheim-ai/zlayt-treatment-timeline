/* Section navigation (T-174 F13). One sticky bar under the case header: Overview, Timeline, Flags, Charges, Export. Each button takes her to that section's heading from any scroll position and
   shows how many items in it are still open (a plain count of undecided items; nothing is computed beyond counting). The current section carries aria-current="location".
   Also the way back from Export: ZL.sections.back() closes the Export view and puts focus on the row she left. Text goes through ZL.el only. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  const OPEN = (list) => (list || []).filter((i) => i.state !== "rejected" && ZL.undecided(i)).length;
  const SECTIONS = [
    ["overview", "Overview", "#co-h", null],
    ["timeline", "Timeline", "#h-timeline", (c) => OPEN((c.entries || []).concat(c.undated_entries || []))],
    ["flags", "Flags", "#rv-flags-h", (c) => OPEN(c.flags)],
    ["charges", "Charges", "#rv-charges-h", (c) => OPEN(c.amounts)],
    ["export", "Export", "#h-export", null],
  ];
  let nav = null, row = null, built = false, forced = null, forcedUntil = 0, lastItem = null, raf = 0;
  const target = (id) => document.querySelector(SECTIONS.find((s) => s[0] === id)[2]);
  const exportOpen = () => { const v = document.getElementById("view-export"); return !!(v && !v.hidden); };
  const present = (id) => (id === "export" ? true : !!target(id));

  function go(id) {
    forced = id; forcedUntil = Date.now() + 1200;
    if (id === "export" && !exportOpen()) { const b = document.getElementById("btn-export"); if (b) b.click(); return; }   // the same path as the header button (the gate, the notice, the scroll)
    const h = target(id); if (!h) return;
    if (!h.hasAttribute("tabindex")) h.setAttribute("tabindex", "-1");
    h.scrollIntoView({ block: "start" }); h.focus({ preventScroll: true });
    mark();
  }
  function build() {
    clear(row);
    SECTIONS.forEach(([id, label]) => row.append(el("button", { type: "button", class: "nav-btn", "data-testid": "nav-" + id, onclick: () => go(id) },
      id === "overview" ? [el("span", { class: "nav-long" }, label), el("span", { class: "nav-short", "aria-hidden": "true" }, "Top")] : label, el("span", { class: "nav-n", hidden: true }))));   // on a phone "Overview" is "Top": five buttons and their counts must fit 360 px
    built = true;
  }
  // The current section: the last one whose heading has reached the bottom edge of the sticky chrome (plus a little), unless she just pressed one.
  function mark() {
    if (!nav || nav.hidden) return;
    nav.classList.toggle("is-on", window.scrollY > 120);
    const edge = nav.getBoundingClientRect().bottom + 48; let cur = SECTIONS[0][0];
    SECTIONS.forEach(([id]) => { if (!present(id) || (id === "export" && !exportOpen())) return; const t = target(id); if (t && t.getBoundingClientRect().top <= edge) cur = id; });
    if (forced && Date.now() < forcedUntil) cur = forced;
    row.querySelectorAll(".nav-btn").forEach((b) => { if (b.getAttribute("data-testid") === "nav-" + cur) b.setAttribute("aria-current", "location"); else b.removeAttribute("aria-current"); });
  }
  function paint() {
    const s = ZL.state.get(), c = s.case, show = !!(c && c.status === "ready");
    if (!nav) { nav = document.getElementById("section-nav"); row = document.getElementById("section-nav-row"); }
    if (!nav) return;
    const was = nav.hidden; nav.hidden = !show;
    if (!show) { if (!was && ZL.measureChrome) ZL.measureChrome(); return; }
    if (!built) build();
    row.querySelectorAll(".nav-btn").forEach((b, i) => {
      const [id, label, , count] = SECTIONS[i], n = count ? count(c) : 0, chip = b.querySelector(".nav-n");
      b.hidden = !present(id);
      chip.hidden = !n; chip.textContent = n ? String(n) : "";
      b.setAttribute("aria-label", label + (n ? ", " + n + (n === 1 ? " item" : " items") + " open" : ""));
    });
    mark();
    if (was && ZL.measureChrome) ZL.measureChrome();
  }
  const later = () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; paint(); }); };
  window.addEventListener("scroll", () => { if (!raf) raf = requestAnimationFrame(() => { raf = 0; mark(); }); }, { passive: true });
  document.addEventListener("zl:panels", later);
  document.addEventListener("DOMContentLoaded", () => { ZL.state.subscribe(later); later(); });

  // ---- the way back from Export: the row she left (the last item row that held focus), else the first item to decide.
  document.addEventListener("focusin", (ev) => { const r = ZL.rv && ZL.rv.itemRowOf ? ZL.rv.itemRowOf(ev.target) : null; if (r) lastItem = r.getAttribute("data-item-id"); });
  ZL.sections = {
    back: function () {
      if (ZL.closeExport) ZL.closeExport();
      const ok = lastItem && ZL.stepper && ZL.stepper.goto ? ZL.stepper.goto(lastItem) : false;   // closing is synchronous, so the row is where it was before Export opened
      if (!ok && ZL.skipTo) ZL.skipTo("review");
      mark();
    },
  };
})();
