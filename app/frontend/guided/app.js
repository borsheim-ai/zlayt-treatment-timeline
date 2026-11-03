/* Guided UI shell (T-181, D-068; spec 2 "Global frame"). Owns: banner, header, demo label (D-065), step bar, footer, theme, router, case loading.
   Page modules (home.js, step1-4.js, review.js) plug in through G.pages and never touch the chrome except through ctx.

   ROUTES (real paths, history.pushState; the server returns index.html for them):
     /                         G.pages.home      layout page
     /new                      G.pages.new       layout page   (step 1, no case yet; step bar shows 1 current, 2-4 locked)
     /case/<token>/records     G.pages.records   layout page   (step 1)
     /case/<token>/timeline    G.pages.timeline  layout frame  (step 2; ?item=<id>; the done screen calls ctx.layout("page"))
     /case/<token>/bills       G.pages.bills     layout frame  (step 3; ?item=<id>; the done screen calls ctx.layout("page"))
     /case/<token>/letter      G.pages.letter    layout page   (step 4)
     /how-it-works             G.pages.how       layout page   (T-211: "How each answer is checked"; linked from the header on every screen; no step bar)
   PAGE CONTRACT: G.pages.<name> = async (ctx) => optional cleanup function. Render into ctx.view (cleared; its children become children of <body> because .view is display:contents,
   so a frame page appends .titlebar, .work and .actions, a page-layout page appends one <main class="wrap">). Resolve when the first paint is done; the shell then sets data-ready on #view.
   ctx = { route, token, step, query (URLSearchParams), case (GET case JSON, null on home and /new), health, signal (aborts on navigation: pass it to fetch),
           view, layout("frame"|"page"), go(path, {replace}), refresh() -> re-GET case, redraw step bar and header, returns the JSON,
           setStepStatus(n, text, state?) override one step-bar status line (e.g. "Drafting 4 of 8", "1 problem"), setCaseTitle(text), setTitle(text) document title }.
   Anything the page throws becomes the plain error block with Try again. Links: any <a href="/..."> is routed without a reload (modifier-clicks and target=_blank are left alone). */
(function () {
  const G = window.G, { h, $ } = G;
  const root = document.documentElement, body = document.body, view = $("#view"), bar = $("#step-bar"), list = $("#step-list"), headerEl = $("#header");
  const TITLE = "Treatment Timeline";
  const ROUTES = [
    [/^\/$/, "home", 0], [/^\/new$/, "new", 1], [/^\/how-it-works$/, "how", 0],
    [/^\/case\/([^/]+)\/records$/, "records", 1], [/^\/case\/([^/]+)\/timeline$/, "timeline", 2], [/^\/case\/([^/]+)\/bills$/, "bills", 3], [/^\/case\/([^/]+)\/letter$/, "letter", 4],
  ];
  const FRAME = { timeline: true, bills: true };

  /* ---- theme (spec 2.2): follows the OS until she picks; remembered in localStorage inside try/catch ---- */
  const isDark = () => { const t = root.getAttribute("data-theme"); return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; };
  try { const t = localStorage.getItem("zl.guided.theme"); if (t === "light" || t === "dark") root.setAttribute("data-theme", t); } catch (_) { /* follows the OS */ }
  function themeLabel() { const b = $("[data-theme-btn]"); if (b) { b.textContent = isDark() ? "Light mode" : "Dark mode"; b.setAttribute("aria-label", b.textContent); } }
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", themeLabel);
  function themeButton() {
    return h("button", { type: "button", class: "theme-btn", "data-theme-btn": "", "data-testid": "btn-theme", onclick: () => {
      const next = isDark() ? "light" : "dark"; root.setAttribute("data-theme", next);
      try { localStorage.setItem("zl.guided.theme", next); } catch (_) { /* not remembered */ }
      themeLabel();
    } }, "Dark mode");
  }

  /* ---- banner, demo label and footer (spec 2.1, 2.3, 2.8; D-065): wording by health.answers, never softened ---- */
  // D-065 as amended in T-177 r2: the prepared-answers sentence is the amended one (the spec 2.3 sentence about the evaluation report is superseded)
  const DEMO = { prepared: ["Demo: sample answers prepared by our team", "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."],
    recorded: ["Demo: recorded AI answers", "These are real AI answers recorded earlier; nothing new is sent to an AI."] };
  // A case whose lines were written by a model (models.generator_prepared === false) is never described as prepared by the team, even when the server's curated set is on (T-181 r2, paralegal minor).
  G.provenance = function (c) {
    const hl = G.store.health, cur = c === undefined ? G.store.current : c, notPrepared = !!(cur && cur.models && cur.models.generator_prepared === false);
    const kind = hl && hl.demo_mode ? (hl.answers === "prepared" && !notPrepared ? "prepared" : "recorded") : "live";
    // T-204 r3: until /api/health says whose answers these are, the footer makes no claim about who wrote them (a prepared sample must never flash "drafted by AI", and a failed health call leaves the neutral line)
    return { kind, pending: !hl, label: DEMO[kind] ? DEMO[kind][0] : "", note: DEMO[kind] ? DEMO[kind][1] : hl ? "Summaries and warnings are drafted by AI and checked by code; you decide every item." : "Checked by code; you decide every item.",
      hours: hl && !hl.demo_mode ? hl.retention_hours : null };
  };
  function drawBanner() {
    const hl = G.store.health, p = G.provenance();
    $("#banner-text").textContent = (hl && hl.banner) || "Synthetic data only — never paste real records";
    $("#banner-demo").textContent = p.label;
    const f = $("#footer"); f.replaceChildren(...[h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
      p.hours ? h("span", { class: "f-live" }, `Pasted text is deleted after ${p.hours} hours.`) : null].filter(Boolean));     // replaceChildren(null) would print the text "null"
  }
  let headerState = { title: null, sub: null };
  function drawHeader() {
    const p = G.provenance(), t = headerState.title;
    const left = t == null
      ? h("a", { class: "brand", href: "/", "data-testid": "brand" }, h("span", { class: "brand-mark", "aria-hidden": "true" }, "TT"), h("span", {}, "Treatment Timeline"))
      : [h("a", { class: "back-cases", href: "/", "data-testid": "btn-your-cases" }, h("span", { "aria-hidden": "true" }, "‹"), h("span", { class: "long" }, "Your cases"), h("span", { class: "short" }, "Cases")),
         h("div", { class: "hd-case" }, h("span", { class: "case-title", "data-testid": "case-title", title: t }, t), headerState.sub ? h("span", { class: "case-sub" }, headerState.sub) : null)];
    const how = h("a", { class: "how-link", href: "/how-it-works", "data-testid": "link-how", "aria-current": now && now.name === "how" ? "page" : null },
      h("span", { class: "long" }, "How each answer is checked"), h("span", { class: "short" }, "How it's checked"));      // T-211, D-074: on every screen
    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), how, themeButton());
    themeLabel();
  }
  G.store.healthP = G.api.health();
  G.store.healthP.then((hl) => { G.store.health = hl; drawBanner(); drawHeader(); G.emit("health", hl); }).catch(() => { /* the static banner stays; pages that need health read G.store.health and cope with null */ });

  /* ---- step bar (spec 2.4): same four steps in the same place; only classes, statuses and links change ---- */
  const overrides = {};      // token -> { n: [text, state?] }
  function drawBar(route, token, c, step) {
    const show = route === "new" || (token && step);
    bar.hidden = !show; if (!show) return;
    const ov = (token && overrides[token]) || {};
    const st = route === "new" ? [{ state: "todo", status: "Now" }, ...[2, 3, 4].map(() => ({ state: "locked", status: "After step 1" }))] : c ? G.steps.states(c, step) : [1, 2, 3, 4].map(() => ({ state: "locked", status: "" }));
    list.replaceChildren(...st.map((s, i) => {
      const n = i + 1, o = ov[n]; if (o) { s = { ...s, status: o[0], state: o[1] || s.state }; }
      const cur = n === step, locked = s.state === "locked", mark = s.state === "done" ? "✓" : s.state === "attn" && !cur ? "!" : String(n);
      const inner = [h("span", { class: "dot", "aria-hidden": "true" }, mark), h("span", { class: "st-text" },
        h("span", { class: "st-label" }, h("span", { class: "long" }, `${n} ${G.LABELS[i][0]}`), h("span", { class: "short" }, G.LABELS[i][1])), h("span", { class: "st-status" }, s.status)),
        h("span", { class: "sr" }, ` (step ${n} of 4)`)];
      const a = { class: "step " + s.state + (cur ? " current" : ""), "data-testid": "step-" + n, "data-state": s.state };
      if (cur) a["aria-current"] = "step";
      return h("li", {}, locked || !token ? h("span", { ...a, "aria-disabled": locked ? "true" : null }, inner) : h("a", { ...a, href: G.url.step(token, n) }, inner));
    }));
  }

  /* ---- router ---- */
  let ctrl = null, cleanup = null, ticket = 0, first = true, now = null;
  function parse() {
    const path = location.pathname.replace(/\/+$/, "") || "/";
    for (const [re, name, step] of ROUTES) { const m = path.match(re); if (m) return { name, step, token: m[1] ? decodeURIComponent(m[1]) : null, query: new URLSearchParams(location.search) }; }
    if (/^\/case\/[^/]+$/.test(path)) return { name: "redirect", token: decodeURIComponent(path.split("/")[2]) };
    return { name: "missing", step: 0, query: new URLSearchParams() };
  }
  G.go = function (path, opts) { G.navigated = true; (opts && opts.replace ? history.replaceState : history.pushState).call(history, null, "", path); return render(); };
  G.route = () => now;
  function setLayout(mode) { body.classList.toggle("frame", mode === "frame"); body.classList.toggle("page", mode !== "frame"); }

  async function render() {
    const r = parse(), mine = ++ticket;
    if (r.name === "redirect") { history.replaceState(null, "", G.url.records(r.token)); return render(); }          // a bare case link opens step 1
    if (ctrl) ctrl.abort();
    if (typeof cleanup === "function") { try { cleanup(); } catch (_) { /* a page's cleanup must not stop navigation */ } }
    cleanup = null; ctrl = new AbortController(); now = r;
    const stale = () => ticket !== mine;
    view.replaceChildren(); view.removeAttribute("data-ready"); view.dataset.route = r.name;
    setLayout(FRAME[r.name] ? "frame" : "page"); document.title = TITLE; window.scrollTo(0, 0);
    G.store.current = null; headerState = { title: r.name === "new" ? "New case" : null, sub: null }; drawHeader(); drawBanner();
    let c = null;
    const ctx = {
      route: r.name, token: r.token, step: r.step, query: r.query, case: null, signal: ctrl.signal, view, get health() { return G.store.health; },
      layout: (m) => setLayout(m), go: G.go,
      setStepStatus: (n, text, state) => { (overrides[r.token] = overrides[r.token] || {})[n] = [text, state]; if (!stale()) drawBar(r.name, r.token, ctx.case, r.step); },
      setCaseTitle: (t) => { if (!stale()) { headerState.title = t; drawHeader(); } },
      setTitle: (t) => { if (!stale()) document.title = t + " – " + TITLE; },
      refresh: async () => { const j = await G.store.load(r.token, ctrl.signal); if (!stale()) { ctx.case = j; paintCase(j); } return j; },
    };
    function paintCase(j) { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, r.token, j, r.step); }
    drawBar(r.name, r.token, G.store.cases[r.token] || null, r.step);
    try {
      if (r.token) {
        try { c = await G.store.load(r.token, ctrl.signal); }
        catch (e) {
          if (e && e.name === "AbortError") return; if (stale()) return;
          setLayout("page"); drawBar(r.name, r.token, null, r.step);
          view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, e.status === 404 ? null : () => render(), e.status === 404 ? "This case is no longer here" : "We couldn't open this case")));
          return done();
        }
        if (stale()) return; ctx.case = c; paintCase(c);
      }
      const page = G.pages[r.name];
      if (!page) { setLayout("page"); view.append(h("main", { class: "wrap" }, h("div", { class: "errbox" }, h("h1", { "data-testid": "page-title" }, "We couldn't find that page"), h("p", {}, "The link may be old or mistyped."),
        h("div", { class: "row-actions" }, h("a", { class: "btn primary lg", href: "/", "data-testid": "link-home" }, "Back to your cases"))))); return done(); }
      const out = await page(ctx);
      if (stale()) { if (typeof out === "function") out(); return; }
      cleanup = out;
    } catch (e) {
      if (e && e.name === "AbortError") return; if (stale()) return;
      setLayout("page"); view.replaceChildren(h("main", { class: "wrap" }, G.errorBlock(e, () => render(), "Something went wrong")));
    }
    done();
    function done() {
      if (stale()) return;
      view.setAttribute("data-ready", "1");
      const t = $("h1", view); if (t && document.title === TITLE) document.title = t.textContent + " – " + TITLE;
      if (!first) { const f = $("[data-autofocus]", view) || t; if (f) { if (!f.matches("a,button,input,textarea,select,[tabindex]")) f.tabIndex = -1; f.focus({ preventScroll: true }); } }
      first = false;
    }
  }
  /* The case title everywhere is the API title (spec 2.2); until it has one, the first record's source line is no use here, so a plain "Case". */
  G.titleOf = (c) => (c && (c.title || c.name)) || "Case";

  /* ---- links: same-origin absolute paths are routed without a reload ---- */
  document.addEventListener("click", (e) => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest && e.target.closest("a[href]"); if (!a || a.target || a.hasAttribute("download")) return;
    const u = new URL(a.href, location.href);
    if (u.origin !== location.origin || /^\/(api|classic)(\/|$)/.test(u.pathname) || !ROUTES.concat([[/^\/case\//]]).some(([re]) => re.test(u.pathname.replace(/\/+$/, "") || "/"))) return;
    e.preventDefault(); G.go(u.pathname + u.search);
  });
  window.addEventListener("popstate", render);
  window.addEventListener("pageshow", (e) => { if (e.persisted) render(); });
  G.on("case", (token, j) => { const r = now; if (r && r.token === token && r.name !== "redirect") { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, token, j, r.step); } });
  drawBanner(); drawHeader();
  render();
})();
