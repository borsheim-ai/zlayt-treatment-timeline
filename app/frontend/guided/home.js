/* Your cases (/). T-181, D-068, spec section 3. Builder A.
   Local mode: GET /api/cases lists every case. Public/demo mode: that route is 404 by design, so the list is the cases THIS BROWSER started (tokens kept in localStorage by G.cases,
   try/catch), each read with GET /api/cases/{token}. One definition of the Next line and the Continue target (spec 3.2) for both sources.
   Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, case-card (data-token, data-title), case-next, btn-continue, btn-rename, btn-delete, btn-delete-yes, btn-delete-keep,
   rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, cases-mode, page-error, btn-retry. Text only (textContent); no inline style attributes. */
(function () {
  const G = window.G, { h } = G;

  /* ---- the cases this browser started (public mode). Shared with step1.js. Never throws: storage can be blocked. ---- */
  const KEY = "zl.guided.cases";
  G.cases = {
    list() { try { const v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter((t) => typeof t === "string") : []; } catch (_) { return []; } },
    add(token) { try { const l = G.cases.list().filter((t) => t !== token); l.unshift(token); localStorage.setItem(KEY, JSON.stringify(l.slice(0, 100))); } catch (_) { /* not remembered */ } },
    remove(token) { try { localStorage.setItem(KEY, JSON.stringify(G.cases.list().filter((t) => t !== token))); } catch (_) { /* not remembered */ } },
  };

  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text "null"
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;
  const day = (iso) => { const d = new Date(iso); return isNaN(d) ? "" : d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); };
  const track = ["Add records", "Timeline", "Bills", "Letter"];

  /* ---- one view-model for a /api/cases row or a GET case JSON ---- */
  function fromRow(c) {
    const p = c.progress || {}, e = p.entries || { decided: 0, total: 0 }, f = p.flags || { decided: 0, total: 0 }, a = p.amounts || { decided: 0, total: 0 };
    const run = c.run || {};
    return { token: c.token, title: c.title || c.name || "Case", created: c.created_at, activity: c.last_activity_at || c.updated_at || c.created_at, records: c.record_count, status: c.status,
      stage: run.steps_done != null ? Math.min(run.steps_done + 1, run.steps_total || 8) : null, stages: run.steps_total || 8,
      err: !!c.status_error, errMsg: c.status_error_message || "We couldn't load this case's status",
      s2: { total: e.total + f.total, left: e.total + f.total - e.decided - f.decided }, s3: { total: a.total, left: a.total - a.decided },
      ready: !!c.export_ready, next: c.next_action, problems: c.hitl && c.hitl.gate_blockers ? c.hitl.gate_blockers.length : null, src: c };
  }
  function fromCase(c) {
    const n = G.steps.counts(c);
    return { token: c.token, title: G.titleOf(c), created: c.created_at, activity: c.updated_at || c.created_at, records: (c.records || []).length, status: c.status, stage: null, stages: 8,
      err: false, errMsg: "", s2: n.step2, s3: n.step3, ready: !!(c.review && c.review.ready_to_export), next: c.next_action, problems: null, src: c };
  }
  const finished = (v) => v.status === "ready" && v.s2.left === 0 && v.s3.left === 0 && v.ready;

  /* Spec 3.2: the Next line and where Continue goes */
  function nextStep(v) {
    const t = v.token;
    if (v.err) return { text: null, to: G.url.records(t), btn: "Open case" };
    if (v.status === "ingested") return { text: "Draft the timeline.", to: G.url.records(t) };
    if (v.status === "running") return { text: "Wait while the timeline is drafted" + (v.stage ? ` (stage ${v.stage} of ${v.stages}).` : "."), to: G.url.records(t) };
    if (v.status === "failed") return { text: "Drafting stopped. Run it again.", cls: "warn", to: G.url.records(t) };
    if (v.s2.left > 0) return { text: `Check the timeline. ${v.s2.left} of ${plural(v.s2.total, "item")} left.`, to: G.url.timeline(t) };
    if (v.s3.left > 0) return { text: `Check the bills. ${v.s3.left} of ${plural(v.s3.total, "amount")} left.`, to: G.url.bills(t) };
    if (finished(v)) return { text: null, done: true, to: G.url.letter(t), btn: "Open letter" };
    const na = v.next;
    if (!v.ready && na && na.item_id && (na.kind === "entry" || na.kind === "flag" || na.kind === "amount"))
      return { text: `Fix ${plural(v.problems || 1, "problem")} before the letter.`, reason: na.reason, cls: "warn", to: na.kind === "amount" ? G.url.bills(t, na.item_id) : G.url.timeline(t, na.item_id) };
    return { text: "Get your letter.", to: G.url.letter(t) };
  }
  function trackStates(v) {
    const st = G.steps.states(v.src, 0), done = finished(v);
    const mine = st.map((s, i) => (i === 3 && done ? "done" : s.state === "done" ? "done" : s.state === "attn" ? "attn" : "todo"));
    const cur = mine.findIndex((s) => s !== "done");
    return mine.map((s, i) => (s === "done" ? "done" : s === "attn" ? "attn" : i === cur ? "current" : ""));
  }

  /* ---- one card ---- */
  function card(v, hooks) {
    if (v.gone) return goneCard(v, hooks);
    const nx = nextStep(v);
    const nextEl = v.err ? h("p", { class: "next warn", "data-testid": "case-next" }, v.errMsg)
      : nx.done ? h("p", { class: "next ok", "data-testid": "case-next" }, h("b", {}, "Finished."), " Your letter is ready.")
        : h("p", { class: "next " + (nx.cls || ""), "data-testid": "case-next" }, h("b", {}, "Next:"), " " + nx.text, nx.reason ? " " + nx.reason : "");
    const states = trackStates(v);
    const track$ = v.err ? h("div", { class: "cc-meta" }, "") : h("ol", { class: "track", "aria-label": "Steps" }, track.map((l, i) => h("li", { class: states[i] }, h("i", {}), l, h("span", { class: "sr" }, ` (${states[i] === "done" ? "done" : states[i] === "current" ? "now" : states[i] === "attn" ? "needs a look" : "later"})`))));
    const meta = h("div", { class: "cc-meta", "data-slot": "meta" }, [v.created ? "Started " + day(v.created) : "", v.records != null ? plural(v.records, "record") : ""].filter(Boolean).join(" · "));
    const metaText = meta.textContent;
    const titleEl = h("h3", { title: v.title }, v.title);
    const renameBtn = h("button", { type: "button", class: "btn quiet", "data-testid": "btn-rename" }, "Rename");
    const top = h("div", { class: "cc-top" }, titleEl, renameBtn);
    const cont = h("a", { class: "btn lg " + (nx.done ? "go" : "primary"), href: nx.to, "data-testid": "btn-continue" }, nx.btn || "Continue");
    const del = h("button", { type: "button", class: "btn quiet danger", "data-testid": "btn-delete" }, "Delete");
    const row1 = h("div", { class: "cc-bottom" }, cont, del);
    const yes = h("button", { type: "button", class: "btn danger", "data-testid": "btn-delete-yes" }, "Yes, delete");
    const keep = h("button", { type: "button", class: "btn", "data-testid": "btn-delete-keep" }, "Keep it");
    const row2 = h("div", { class: "cc-bottom", hidden: true }, h("span", { class: "cc-ask", role: "alert" }, "Delete this case and all its answers?"), yes, keep);
    const el = h("article", { class: "ccard", "data-testid": "case-card", "data-token": v.token, "data-title": v.title, "data-finished": finished(v) ? "1" : "0" }, top, meta, track$, nextEl, row1, row2);

    del.addEventListener("click", () => { hooks.editing(+1); row1.hidden = true; row2.hidden = false; keep.focus(); });
    keep.addEventListener("click", () => { hooks.editing(-1); row2.hidden = true; row1.hidden = false; del.focus(); });
    yes.addEventListener("click", async () => {
      yes.disabled = true; keep.disabled = true;
      try { await G.api.remove(v.token); G.cases.remove(v.token); hooks.editing(-1); hooks.removed(v.token); }
      catch (e) { yes.disabled = false; keep.disabled = false; meta.textContent = e.message; meta.classList.add("bad"); }
    });
    renameBtn.addEventListener("click", () => {
      hooks.editing(+1);
      const input = h("input", { type: "text", class: "rename", value: v.title, maxlength: "120", "aria-label": "Case name", "data-testid": "rename-input" });
      const save = h("button", { type: "button", class: "btn", "data-testid": "btn-rename-save" }, "Save"), cancel = h("button", { type: "button", class: "btn quiet", "data-testid": "btn-rename-cancel" }, "Cancel");
      top.replaceChildren(input, save, cancel);
      const close = (title) => { hooks.editing(-1); titleEl.textContent = title; titleEl.title = title; el.setAttribute("data-title", title); v.title = title; top.replaceChildren(titleEl, renameBtn); meta.textContent = metaText; meta.classList.remove("bad"); renameBtn.focus(); };
      const doSave = async () => {
        save.disabled = true;
        try { const r = await G.api.rename(v.token, input.value); close(r.title || G.titleOf({ title: input.value })); }
        catch (e) { save.disabled = false; meta.textContent = e.message; meta.classList.add("bad"); input.focus(); }
      };
      save.addEventListener("click", doSave); cancel.addEventListener("click", () => close(v.title));
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") { e.preventDefault(); doSave(); } else if (e.key === "Escape") { e.preventDefault(); close(v.title); } });
      input.focus(); input.select();
    });
    return el;
  }
  function goneCard(v, hooks) {
    const hrs = G.store.health && G.store.health.retention_hours;
    const rm = h("button", { type: "button", class: "btn lg", "data-testid": "btn-remove-gone" }, "Remove from this list");
    rm.addEventListener("click", () => { G.cases.remove(v.token); hooks.removed(v.token); });
    return h("article", { class: "ccard gone", "data-testid": "case-card", "data-token": v.token, "data-title": "", "data-finished": "0" }, h("div", { class: "cc-top" }, h("h3", {}, "A case that is gone")),
      h("div", { class: "cc-meta" }, ""), h("p", { class: "next warn", "data-testid": "case-next" }, "This case is no longer here." + (hrs ? ` Cases are kept for ${hrs} hours.` : "")), h("span", {}), h("div", { class: "cc-bottom" }, rm));
  }
  const skeleton = () => h("article", { class: "ccard skeleton", "aria-hidden": "true" }, h("div", { class: "skel sk-title" }), h("div", { class: "skel sk-meta" }), h("div", { class: "skel sk-track" }), h("div", { class: "skel sk-next" }), h("div", { class: "skel sk-btn" }));

  /* ---- data: local list, or this browser's tokens ---- */
  async function load(signal) {
    const hl = await G.healthNow(signal);
    if (hl.local_mode !== false) try { return { mode: "local", views: ((await G.api.cases(signal)).cases || []).map(fromRow) }; }
    catch (e) {
      if (e.name === "AbortError") throw e;
      if (e.status !== 404) throw e;
    }
    const tokens = G.cases.list();
    const got = await Promise.allSettled(tokens.map((t) => G.api.getCase(t, signal)));
    if (signal && signal.aborted) throw new DOMException("aborted", "AbortError");
    return { mode: "public", views: got.map((r, i) => r.status === "fulfilled" ? fromCase(r.value) : (r.reason && r.reason.status === 404 ? { token: tokens[i], gone: true, activity: "" }
      : { token: tokens[i], title: "Case", err: true, errMsg: "We couldn't load this case's status", status: "failed", s2: { total: 0, left: 0 }, s3: { total: 0, left: 0 }, src: {}, activity: "" })) };
  }

  G.pages.home = async function (ctx) {
    const sampleOk = () => !G.store.health || G.store.health.sample_available !== false;
    const head = (...extra) => h("div", { class: "home-h" }, h("div", { class: "hh-main" }, h("h1", { "data-testid": "page-title", tabindex: "-1" }, "Your cases"), h("p", {}, "Each case goes through 4 steps. Pick up where you left off.")), ...extra);
    const newBtn = () => h("a", { class: "btn primary lg", href: G.url.new(), "data-testid": "btn-new-case" }, "+ Start a new case");
    const main = h("main", { class: "wrap wide", id: "main" }, head(newBtn()),
      h("p", { class: "sr", role: "status" }, "Loading your cases"), h("h2", { class: "sec-h" }, "Loading your cases…"), h("div", { class: "cases", "data-testid": "cases-loading" }, skeleton(), skeleton(), skeleton()));
    ctx.view.append(main);

    let data, timer = null, editing = 0, last = "";
    const sig = ctx.signal;
    try { data = await load(sig); }
    catch (e) {
      if (e.name === "AbortError") return;
      fill(main, head(), h("div", { class: "panel empty", role: "alert", "data-testid": "page-error" }, h("div", { class: "em-ic bad", "aria-hidden": "true" }, "!"), h("h2", {}, "We couldn't load your cases."),
        h("p", {}, e.message), h("div", { class: "row-actions" }, h("button", { type: "button", class: "btn primary lg", "data-testid": "btn-retry", "data-autofocus": "", onclick: () => ctx.go("/", { replace: true }) }, "Try again"))));
      return;
    }

    const lists = h("div", { class: "lists" });
    const searchBox = h("div", { class: "find", hidden: true }, h("label", { class: "sr", for: "find-case" }, "Find a case"), h("input", { id: "find-case", type: "search", placeholder: "Find a case by name", "data-testid": "find-case", autocomplete: "off" }));
    const finput = searchBox.querySelector("input");
    const hooks = { editing: (n) => { editing = Math.max(0, editing + n); }, removed: (t) => { data.views = data.views.filter((v) => v.token !== t); last = ""; draw(true); } };

    function applyFilter() {
      const q = finput.value.trim().toLowerCase();
      lists.querySelectorAll("[data-testid=case-card]").forEach((c) => { c.hidden = !!q && !(c.getAttribute("data-title") || "").toLowerCase().includes(q); });
      lists.querySelectorAll("section").forEach((s) => { const n = s.querySelectorAll("[data-testid=case-card]:not([hidden])").length; s.querySelector(".c").textContent = String(n); });
    }
    function draw(force) {
      const sig = JSON.stringify(data.views.map((v) => [v.token, v.title, v.status, v.stage, v.s2, v.s3, v.ready, v.gone, v.err, v.next]));
      if (!force && sig === last) return; last = sig;
      const views = data.views.slice().sort((a, b) => String(b.activity || "").localeCompare(String(a.activity || "")));
      const active = views.filter((v) => !finished(v)), done = views.filter(finished);
      searchBox.hidden = views.length < 6;
      if (!views.length) {
        lists.replaceChildren(h("div", { class: "panel empty", "data-testid": "cases-empty" }, h("div", { class: "em-ic", "aria-hidden": "true" }, "+"), h("h2", {}, "You don't have any cases yet."),
          h("p", {}, "A case is one client's medical records. We'll guide you through 4 steps: add the records, check the timeline, check the bills, and get your letter."),
          h("div", { class: "row-actions" }, newBtn(), sampleOk() ? h("button", { type: "button", class: "btn lg", "data-testid": "btn-sample-case", onclick: openSample }, "Open the sample case") : null),
          h("p", { class: "err-slot", role: "alert", "data-testid": "sample-error" })));
        return;
      }
      const sec = (label, items, testid) => items.length ? h("section", { "aria-label": label }, h("h2", { class: "sec-h" }, label, " ", h("span", { class: "c" }, String(items.length))),
        h("div", { class: "cases", "data-testid": testid }, items.map((v) => card(v, hooks)))) : null;
      fill(lists, sec("In progress", active, "cases-list"), sec("Finished", done, "cases-finished"));
      applyFilter();
    }
    async function openSample(ev) {
      const btn = ev.currentTarget, slot = lists.querySelector("[data-testid=sample-error]"); btn.disabled = true; btn.textContent = "Opening…"; slot.textContent = "";
      try { const r = await G.api.createCase({ sample: true }); G.cases.add(r.token); ctx.go(G.url.records(r.token)); }
      catch (e) { btn.disabled = false; btn.textContent = "Open the sample case"; slot.textContent = e.message; }
    }
    finput.addEventListener("input", applyFilter);

    fill(main, head(data.views.length ? newBtn() : null),
      data.mode === "public" ? h("p", { class: "muted", "data-testid": "cases-mode" }, "These are the cases started in this browser. Keep the case link to open it elsewhere.") : null, searchBox, lists);
    draw(true);

    /* a case that is being drafted shows its stage; follow it without moving anything (only text inside the cards changes) */
    async function tick() {
      timer = null;
      if (!sig.aborted && data.views.some((v) => v.status === "running")) {
        if (!editing) { try { const d = await load(sig); if (!sig.aborted && !editing) { data = d; draw(false); } } catch (e) { /* keep what is on screen */ } }
        if (!sig.aborted) timer = setTimeout(tick, 2000);
      }
    }
    if (data.views.some((v) => v.status === "running")) timer = setTimeout(tick, 2000);
    return () => { if (timer) clearTimeout(timer); };
  };
})();
