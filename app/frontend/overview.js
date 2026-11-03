/* Multi-case management (T-149). Two things in one file because they share the call-out chips and the progress bars:
   1. the case OVERVIEW: the home screen when GET /api/cases answers 200 (local mode). A row per case: readable title, dates, run stage, a decided/total bar per kind, plain call-out chips
      (needs review, edits to check, could not verify, export blocked with its reasons, "Can export, N not reviewed" in amber, green only for "Everything decided"). Filter (all / needs attention / everything decided), title search,
      sort, open by click, Enter or link; j / k / arrows move between rows. Loading and error states are drawn in the list's own place.
   2. the case OVERVIEW BLOCK that starts the detail view (ZL.caseHead): progress, ONE "Do this first" line (server next_action), the call-outs, the Open-decisions buttons and the Case checks, in one block (T-149 r2).
   Nothing is computed here beyond counting what the server sent; every sentence about a blocker is the server's own `why`. Server text only goes through ZL.el (text nodes). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  const KINDS = [["entries", "Entries"], ["flags", "Flags"], ["amounts", "Amounts"]];
  const STAGE = { ingest: "Reading the records", extract: "Drafting summaries", verify: "Checking quotes against the records", judge_entries: "Second check by another model", amounts: "Reading amounts",
    conflicts: "Comparing records", flags: "Looking for gaps and flags", finalize: "Finishing" };
  const plural = (n, one, many) => n + " " + (n === 1 ? one : many);
  ZL.caseTitles = ZL.caseTitles || {};       // token -> the title the overview showed, so the header names the case the same way

  const when = (iso) => { const d = iso ? new Date(iso) : null; return d && !isNaN(d) ? d.toLocaleString("en-US", { month: "short", day: "numeric", year: "numeric", hour: "numeric", minute: "2-digit" }) : ""; };
  const timeEl = (iso) => el("time", { datetime: iso }, when(iso));
  const chip = (id, tone, icon, text) => el("span", { class: "chip chip--" + tone, "data-icon": icon, "data-testid": id }, text);

  // ---- shared: a decided/total bar per kind
  function bars(prefix, progress, notStarted) {
    return el("ul", { class: "cv-bars", "aria-label": "Items decided, by kind" }, KINDS.map(([k, label]) => {
      const p = (progress && progress[k]) || { decided: 0, total: 0 };
      return el("li", { class: "cv-bar" },
        el("span", { class: "cv-bar-label" }, label),
        el("progress", { max: Math.max(p.total, 1), value: p.decided, "aria-label": label + " decided: " + (notStarted ? "not started" : p.total ? p.decided + " of " + p.total : "none found"), "data-testid": prefix + "-progress-" + k }),
        el("span", { class: "cv-bar-n", "data-testid": prefix + "-progress-text-" + k }, notStarted ? "Not started" : p.total ? p.decided + " of " + p.total : "None"));
    }));
  }
  // ---- shared: plain chips for what is left for the human. o = {needs, edits, tray, notReviewed, blockers:[{why}], warnings:[{why}], done:true|false|null, ready:true|false|null, needsId}
  // Green is only for "Everything decided". A gate that passes while items are undecided is amber and says what stays out of the letter.
  function callouts(prefix, o) {
    const chips = [];
    if (o.needs) chips.push(chip(o.needsId || prefix + "-chip-needs-review", "warn", "alert", o.needs + (o.needs === 1 ? " needs review" : " need review")));
    if (o.edits) chips.push(chip(prefix + "-chip-edits", "warn", "pencil", plural(o.edits, "edit", "edits") + " to check"));
    if (o.tray) chips.push(chip(prefix + "-chip-tray", "muted", "info", o.tray + " could not be verified"));
    const bl = o.blockers || [];
    if (bl.length) chips.push(chip(prefix + "-chip-blocked", "bad", "x", "Export blocked (" + bl.length + ")"));
    else if (o.ready && o.done) chips.push(chip(prefix + "-chip-ready", "ok", "check", "Everything decided"));
    else if (o.ready && o.done === false) chips.push(chip(prefix + "-chip-can-export", "warn", "info", "Can export \u2014 " + o.notReviewed + " not reviewed (they stay out of the letter)"));
    const why = [];
    bl.forEach((b) => { if (b.why && !why.includes(b.why)) why.push(b.why); });
    const warns = [];
    if (!bl.length && o.ready) (o.warnings || []).forEach((w) => { if (w.reason_code !== "ITEMS_NOT_REVIEWED" && w.why && !warns.includes(w.why)) warns.push(w.why); });
    return el("div", { class: "cv-callouts" },
      el("div", { class: "cv-chips" }, chips),
      why.length ? el("ul", { class: "cv-reasons" }, why.slice(0, 2).map((w) => el("li", { "data-testid": prefix + "-blocker-reason" }, w)), why.length > 2 ? el("li", { class: "muted" }, "and " + (why.length - 2) + " more") : null) : null,
      warns.length ? el("ul", { class: "cv-reasons cv-reasons--soft" }, warns.slice(0, 2).map((w) => el("li", { "data-testid": prefix + "-warning" }, w))) : null);
  }

  // ======== 1. the overview (home) ========================================================================================================================
  let host = null, list = null, countEl = null, emptyEl = null, filterBtns = {}, sortSel = null, searchEl = null, loadingEl = null, errEl = null, openErrEl = null;
  let cases = [], available = null, loadErr = "", openErr = "", filter = "all", sort = "recent", query = "", timer = null, wasShown = false, pendingFocus = null, sig = "", btnAll = null;
  let openErrTok = null, openErrGone = false;
  let newBtn = null, toolsEl = null, skelEl = null, retryFocus = false, headEl = null;
  let settled = false, loading = false, showLoading = false, loadTimer = null, paintSig = "", detailTimer = null;

  // The library cases keep their plain titles from niceName (a typed name replaces the stored name, so a renamed library case shows the typed one); every other case shows the server's title (T-157).
  const titleOf = (s) => (/^case[ _]lib\d+/i.test(s.name || "") ? ZL.niceName(s.name) : s.title || ZL.niceName(s.name) || "Untitled case");
  ZL.titleOf = titleOf;
  const hitl = (s) => s.hitl || {};
  const blockersOf = (s) => hitl(s).gate_blockers || [];
  const undecidedOf = (s) => (hitl(s).pending || 0) + (hitl(s).edits_to_check || 0);
  // Items marked Needs review that are STILL undecided. The server's own open count when it sends one (hitl.needs_review_open); until then the state-based count capped by what is
  // undecided, so a case with nothing left to decide never keeps a stale "need review" call-out.
  const needsOpen = (s) => { const h = hitl(s); return h.needs_review_open != null ? h.needs_review_open : Math.min(h.needs_review || 0, undecidedOf(s)); };
  const analyzed = (s) => s.status !== "ingested";
  // Done: the export gate passes AND nothing is waiting (no undecided item, no edit to check). Only then is a case green.
  const isDone = (s) => s.status === "ready" && !!s.export_ready && undecidedOf(s) === 0;
  // Something is waiting for the paralegal: a failed run, an unanalyzed case, items to decide, edits to check or an export blocker. A running case waits for the AI, not for her.
  const needsAttention = (s) => s.status_error === true || s.status === "failed" || s.status === "ingested" || (s.status !== "running" && !isDone(s) && (undecidedOf(s) > 0 || blockersOf(s).length > 0));
  const share = (s) => { const p = s.progress || {}; let d = 0, t = 0; KINDS.forEach(([k]) => { d += (p[k] && p[k].decided) || 0; t += (p[k] && p[k].total) || 0; }); return d / Math.max(1, t); };
  const totals = (s) => { const p = s.progress || {}; let d = 0, t = 0; KINDS.forEach(([k]) => { d += (p[k] && p[k].decided) || 0; t += (p[k] && p[k].total) || 0; }); return [d, t]; };
  const rank = (s) => (s.status === "failed" ? 0 : s.status === "ready" && !s.export_ready ? 1 : s.status === "ingested" ? 2 : s.status === "ready" && !isDone(s) ? 3 : s.status === "running" ? 4 : 5);
  const recent = (a, b) => String(b.last_activity_at || b.created_at || "").localeCompare(String(a.last_activity_at || a.created_at || ""));
  const SORTS = {
    recent: ["Latest activity", recent],
    attention: ["Needs attention first", (a, b) => rank(a) - rank(b) || undecidedOf(b) - undecidedOf(a) || recent(a, b)],
    least_done: ["Least decided first", (a, b) => share(a) - share(b) || recent(a, b)],
    title: ["Title A to Z", (a, b) => { const x = titleOf(a).toLowerCase(), y = titleOf(b).toLowerCase(); return x < y ? -1 : x > y ? 1 : 0; }],
  };
  // Two states that never overlap: waiting for her, or everything decided.
  const FILTERS = { all: ["All cases", () => true], attention: ["Needs attention", needsAttention], ready: ["Everything decided", isDone] };   // T-174 F9: the same words as the chip of a finished case
  const EMPTY = { all: "No cases yet. Paste records below, or add a synthetic case.", attention: "No case needs attention.", ready: "No case has everything decided yet. A case is done when its export passes and every item is decided." };

  function stageChip(s) {
    const r = s.run || {};
    if (s.status === "running") return chip("cases-stage", "info", "info", "Analyzing: " + (STAGE[r.stage] || "working") + (r.steps_total ? " (step " + Math.min((r.steps_done || 0) + 1, r.steps_total) + " of " + r.steps_total + ")" : ""));
    if (s.status === "failed") return chip("cases-stage", "bad", "x", "Analysis failed");
    if (s.status === "ingested") return chip("cases-stage", "muted", "dash", "Not analyzed yet");
    return chip("cases-stage", "muted", "check", "Analysis done");
  }
  // The call-out column: ONE status pill first, then either the one thing to do (not analyzed, failed) or the chips.
  // T-174 / T-175 r2: a row the server could not read (status_error: true, every figure null) says so and offers Try again. It never shows a zero, a progress bar, or "Can export".
  const STATUS_ERR = "We couldn\u2019t load this case\u2019s status";
  function calloutColumn(s) {
    const h = hitl(s), pill = el("p", { class: "cv-stage" }, stageChip(s));
    if (s.status_error === true) return el("div", { class: "cv-callouts" }, el("p", { class: "cv-next rv-error", role: "alert", "data-testid": "cases-status-error" }, s.status_error_message || STATUS_ERR, " ",
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "cases-status-retry", onclick: (ev) => { ev.stopPropagation(); load(); } }, "Try again")));
    if (s.status === "ingested") return el("div", { class: "cv-callouts" }, pill, el("p", { class: "cv-next", "data-testid": "cases-next" }, "Not analyzed: open the case and press Analyze."));
    if (s.status === "failed") return el("div", { class: "cv-callouts" }, pill, el("p", { class: "cv-next", "data-testid": "cases-next" }, "The analysis stopped before it finished. Open the case to run it again."));
    if (s.status === "running") return el("div", { class: "cv-callouts" }, pill);
    const co = callouts("cases", { needs: needsOpen(s), edits: h.edits_to_check, tray: h.could_not_verify, blockers: blockersOf(s), warnings: h.gate_warnings, ready: !!s.export_ready, done: isDone(s), notReviewed: undecidedOf(s) });   // T-174 F9: the same open total as the header (pending + edits to check), not the gate's warning count, which leaves an edit to check out
    return el("div", { class: "cv-callouts" }, pill, co);
  }
  function rowNode(s) {
    const title = titleOf(s), [d, t] = totals(s);
    ZL.caseTitles[s.token] = title;
    const a = el("a", { class: "cv-open", href: "#/case/" + encodeURIComponent(s.token), "data-testid": "cases-open", onclick: (ev) => {
      if (ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.button) return;
      ev.preventDefault(); ev.stopPropagation(); openCase(s.token, true);
    } }, title);
    return el("li", { class: "cv-row", "data-testid": "cases-row", "data-token": s.token, onclick: (ev) => { if (!ev.target.closest("a, button, select, input, summary")) openCase(s.token, true); } },
      el("div", { class: "cv-main" },
        el("h3", { class: "cv-title", "data-testid": "cases-title" }, a),
        el("p", { class: "cv-dates muted small", "data-testid": "cases-dates", title: "Created " + when(s.created_at) }, "Last activity ", timeEl(s.last_activity_at || s.updated_at || s.created_at),
          s.record_count != null ? " \u00b7 " + plural(s.record_count, "record", "records") : "")),
      el("div", { class: "cv-prog" },
        s.status_error === true ? null : analyzed(s) && t ? el("p", { class: "cv-decided small", "data-testid": "cases-decided" }, d + " of " + t + " decided") : null,
        s.status_error === true ? null : bars("cases", s.progress, !analyzed(s))),
      calloutColumn(s));
  }

  // Space is held for the list while it loads: as many placeholder rows as the last list had (so the paste box below does not jump on a slow answer).
  function skelRows() { try { return Math.max(2, Math.min(8, parseInt(sessionStorage.getItem("zl.caseRows") || "3", 10) || 3)); } catch (e) { return 3; } }
  // New case: the create form lives under the list; this brings its heading to the top and puts the cursor in the name field.
  function goNew() {
    const f = ZL.$("#view-input"), t = ZL.$("#case-title"); if (!f || !t) return;
    const calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    f.scrollIntoView({ block: "start", behavior: calm ? "auto" : "smooth" });
    t.focus({ preventScroll: true });
  }
  function buildToolbar() {
    const g = el("div", { class: "cv-filters", role: "group", "aria-label": "Show" });
    Object.keys(FILTERS).forEach((k) => {
      const b = el("button", { type: "button", class: "btn cv-filter", "data-testid": "cases-filter-" + k, "aria-pressed": "false", onclick: () => { filter = k; paint(); } });
      filterBtns[k] = b; g.append(b);
    });
    sortSel = el("select", { id: "cv-sort", "data-testid": "cases-sort", onchange: (ev) => { sort = ev.target.value; paint(); } },
      Object.keys(SORTS).map((k) => el("option", { value: k }, SORTS[k][0])));
    searchEl = el("input", { type: "search", id: "cv-search", "data-testid": "cases-search", autocomplete: "off", placeholder: "Title", oninput: (ev) => { query = ev.target.value; paint(); } });
    countEl = el("p", { class: "cv-count muted small", role: "status", "data-testid": "cases-count" });
    loadingEl = el("p", { class: "cv-loading muted", role: "status", "data-testid": "cases-loading" }, "Loading cases\u2026");
    errEl = el("div", { class: "cv-msg rv-error", role: "alert", "data-testid": "cases-load-error" },
      el("span", { class: "cv-err-text" }), " ", el("button", { type: "button", class: "btn btn--sm", "data-testid": "cases-retry", onclick: () => { retryFocus = true; loadErr = ""; paint(); load(); } }, "Try again"));
    skelEl = el("ul", { class: "cv-skel", "aria-hidden": "true", "data-testid": "cases-skeleton" }, Array.from({ length: skelRows() }, () => el("li", { class: "cv-skel-row" })));
    openErrEl = el("p", { class: "cv-msg rv-error", role: "alert", "data-testid": "cases-open-error" });
    emptyEl = el("p", { class: "cv-empty", "data-testid": "cases-empty" });
    list = el("ul", { class: "cv-list", "aria-label": "Cases", "data-testid": "cases-list" });
    headEl = el("h2", { id: "cv-h", tabindex: "-1" }, "Cases");
    toolsEl = el("div", { class: "cv-tools" }, g, el("label", { class: "cv-sort", for: "cv-search" }, "Search ", searchEl), el("label", { class: "cv-sort", for: "cv-sort" }, "Sort ", sortSel));
    newBtn = el("button", { type: "button", class: "btn btn--primary cv-new", "data-testid": "btn-new-case", onclick: goNew }, "New case");
    host.append(el("div", { class: "cv-head" }, headEl, el("div", { class: "cv-head-r" }, countEl, newBtn)), toolsEl,
      el("p", { class: "cv-keys muted small", "data-testid": "cases-keys" }, "Keys: ", el("kbd", {}, "j"), " / ", el("kbd", {}, "k"), " move between cases, ", el("kbd", {}, "Enter"), " opens the one you are on."),
      loadingEl, skelEl, errEl, openErrEl, emptyEl, list);
  }
  // Keys are bound once on the document in DOMContentLoaded, before the first paint. Arrow keys, Home, End, j and k move between the rows' links; j / k also start at the first row from nowhere.
  function overviewShown() { const sec = host && host.closest("section"); return !!(sec && !sec.hidden && list); }
  function onDocKey(ev) {
    if (ev.metaKey || ev.ctrlKey || ev.altKey || !overviewShown()) return;
    const t = ev.target, tag = t && t.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || (t && t.isContentEditable) || document.querySelector("dialog[open]")) return;
    const links = Array.from(list.querySelectorAll(".cv-open")); if (!links.length) return;
    const onRow = t && t.classList && t.classList.contains("cv-open"), at = links.indexOf(t);
    let to = null;
    if (onRow) to = ev.key === "ArrowDown" || ev.key === "j" ? links[Math.min(at + 1, links.length - 1)] : ev.key === "ArrowUp" || ev.key === "k" ? links[Math.max(at - 1, 0)] : ev.key === "Home" ? links[0] : ev.key === "End" ? links[links.length - 1] : null;
    else if ((t === document.body || t === document.documentElement) && (ev.key === "j" || ev.key === "k")) to = links[0];
    if (to) { ev.preventDefault(); to.focus(); to.scrollIntoView({ block: "nearest" }); }
  }
  function paint() {
    if (!host) return;
    const s = ZL.state.get(), show = !s.case && (available === true || !!loadErr || showLoading);
    const sec = host.closest("section") || host; sec.hidden = !show;
    if (!show) return;
    if (!list) buildToolbar();
    const ready = available === true;
    loadingEl.hidden = !(loading && !settled); skelEl.hidden = loadingEl.hidden; errEl.hidden = !loadErr; toolsEl.hidden = !!loadErr && !ready; errEl.querySelector(".cv-err-text").textContent = loadErr;
    clear(openErrEl); openErrEl.hidden = !openErr;
    if (openErr) openErrEl.append(openErr, " ", el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-error-action", onclick: () => { if (openErrGone || !openErrTok) { openErr = ""; paint(); load(); } else openCase(openErrTok, true); } }, openErrGone || !openErrTok ? "Refresh the list" : "Try again"));   // T-174 F15
    Object.keys(FILTERS).forEach((k) => {
      const n = cases.filter(FILTERS[k][1]).length;
      clear(filterBtns[k]); filterBtns[k].append(FILTERS[k][0] + (ready ? " (" + n + ")" : ""));
      filterBtns[k].setAttribute("aria-pressed", k === filter ? "true" : "false");
    });
    sortSel.value = sort;
    const q = query.trim().toLowerCase();
    const shown = ready ? cases.filter(FILTERS[filter][1]).filter((c) => !q || titleOf(c).toLowerCase().includes(q)).sort(SORTS[sort][1]) : [];
    countEl.textContent = ready ? "Showing " + shown.length + " of " + cases.length + (cases.length === 1 ? " case" : " cases") : "";
    emptyEl.textContent = !ready || shown.length ? "" : q ? "No case matches \u201c" + query.trim() + "\u201d." : EMPTY[filter]; emptyEl.hidden = !emptyEl.textContent;
    // Rebuild the rows only when what they show changed: a poll or a state change must not drop the focus a key was just sent to (T-149 r2).
    const nsig = JSON.stringify([shown.map((c) => [c, titleOf(c)]), q]) + "|" + (pendingFocus || "");
    if (nsig !== paintSig || pendingFocus) {
      paintSig = nsig;
      const ae = document.activeElement, keepTok = ae && ae.classList && ae.classList.contains("cv-open") ? ae.closest("[data-token]").getAttribute("data-token") : pendingFocus;
      clear(list); shown.forEach((c) => list.append(rowNode(c)));
      if (keepTok) {
        const link = list.querySelector('[data-token="' + keepTok + '"] .cv-open');
        if (link) { link.focus({ preventScroll: !pendingFocus }); if (pendingFocus) link.scrollIntoView({ block: "nearest" }); }
        pendingFocus = null;
      }
    }
    list.setAttribute("data-ready", settled && ready ? "true" : "false");
  }
  async function load() {
    clearTimeout(loadTimer);
    if (!settled) { loading = true; loadTimer = setTimeout(() => { showLoading = true; paint(); }, 250); }   // a quick answer (or "not available") never flashes the section
    try {
      const r = await ZL.api.cases();
      available = true; loadErr = "";
      const next = r.cases || [];
      try { sessionStorage.setItem("zl.caseRows", String(next.length)); } catch (e) { /* storage is a convenience */ } nsig = JSON.stringify(next);
      if (nsig !== sig) { sig = nsig; cases = next; document.dispatchEvent(new CustomEvent("zl:cases")); }
    } catch (e) {
      if (e && e.status === 404) available = false;
      else loadErr = "We could not load your cases. Check the connection and try again.";   // T-166 F7: plain words and one action (Try again); never an HTTP status
    }
    settled = true; loading = false; clearTimeout(loadTimer); showLoading = false;
    syncButton(); paint(); schedule();
    if (retryFocus && settled) { retryFocus = false; if (!loadErr && headEl && host.closest("section") && !host.closest("section").hidden) headEl.focus({ preventScroll: true }); }
  }
  function schedule() {          // a case that is still being analyzed changes by itself: look again every 3 seconds while the overview is on screen
    clearTimeout(timer);
    if (available === true && !ZL.state.get().case && cases.some((c) => c.status === "running")) timer = setTimeout(load, 3000);
  }
  function syncButton() {
    if (!btnAll) return;
    btnAll.hidden = !(available === true && ZL.state.get().case); renameSync(ZL.state.get());
  }

  // ---- opening and leaving a case. A push on open, so the browser's Back button returns to the overview.
  async function openCase(token, push) {
    openErr = ""; paint();
    try {
      const c = await ZL.api.getCase(token);
      if (push) history.pushState(null, "", "#/case/" + encodeURIComponent(token));
      pendingHeadingFocus = true;
      ZL.state.set({ token, created: c.status === "ingested" ? Object.assign({}, c, { record_count: (c.records || []).length }) : null, case: c,
        status: c.status === "failed" ? { status: "failed", error: c.error || null } : null });
      if (c.status === "running") ZL.pollRun();
      window.scrollTo(0, 0);
    } catch (e) {
      openErrTok = token; openErrGone = !!(e && e.status === 404);
      openErr = openErrGone ? "That case no longer exists." : "That case could not be opened. " + ((e && e.message) || "Check the connection.");
      paint(); load();
    }
  }
  function goHome(push) {
    pendingFocus = ZL.state.get().token;
    if (push) history.pushState(null, "", location.pathname + location.search);
    ZL.state.set({ token: null, created: null, case: null, status: null });
    window.scrollTo(0, 0);
  }
  function fromHash() {
    const m = /#\/case\/([^&/]+)/.exec(location.hash), s = ZL.state.get();
    if (m) { const tok = decodeURIComponent(m[1]); if (tok !== s.token) openCase(tok, false); }
    else if (s.case || s.token) goHome(false);
  }
  const summaryOf = (token) => cases.find((c) => c.token === token) || null;
  ZL.cases = { open: (t) => openCase(t, true), home: () => goHome(true), available: () => available === true, refresh: load, summary: summaryOf };

  document.addEventListener("DOMContentLoaded", () => {
    host = ZL.$("#cases-body");
    btnAll = ZL.$("#btn-all-cases");
    if (btnAll) btnAll.addEventListener("click", () => goHome(true));
    window.addEventListener("popstate", fromHash);
    document.addEventListener("keydown", onDocKey, true);     // capture: bound before the rows paint, and before any other handler can swallow the key
    document.addEventListener("visibilitychange", () => { if (!document.hidden && wasShown) load(); });
    ZL.state.subscribe((s) => {
      syncButton();
      renameSync(s);
      // a decision in the open case: ask the list again (quietly, after the burst) so "Do this first" and the counts on return are the server's current numbers
      if (s.case && available === true) { clearTimeout(detailTimer); detailTimer = setTimeout(load, 700); }
      const show = available !== false && !s.case;
      if (show === wasShown) { if (show) paint(); return; }
      wasShown = show;
      if (show) { paint(); load(); } else { clearTimeout(timer); paint(); }
    });
    load();
  });

  // ---- naming a case (T-157 PATCH /api/cases/{token} {title}): a Rename button beside the name in the header; Enter saves, Escape leaves the old name.
  let caseNameEl = null, renameBtn = null, renameBox = null;
  function renameSync(s) {
    if (!renameBtn) return;
    renameBtn.hidden = !(available === true && s.case) || !!renameBox;
    if (renameBox && !s.case) endRename(false);
  }
  function endRename(focusBtn) {
    if (renameBox) { renameBox.remove(); renameBox = null; }
    if (caseNameEl) caseNameEl.hidden = !ZL.state.get().case;
    renameSync(ZL.state.get());
    if (focusBtn && renameBtn && !renameBtn.hidden) renameBtn.focus();
  }
  function startRename() {
    const s = ZL.state.get(); if (!s.case || renameBox) return;
    const cur = (ZL.caseTitles || {})[s.token] || caseNameEl.textContent || "";
    const input = el("input", { type: "text", class: "cv-rename-input", "data-testid": "case-rename-input", maxlength: "120", value: cur, "aria-label": "Case name", autocomplete: "off" });
    const err = el("span", { class: "rv-error small", role: "alert", "data-testid": "case-rename-error" });
    const save = async () => {
      const title = input.value.trim();
      if (!title) { err.textContent = "Type a name for the case."; return; }
      if (title === cur) return endRename(true);
      save.busy = true; err.textContent = "";
      try {
        const r = await ZL.api.rename(s.token, title), shown = (r && r.title) || title;
        ZL.caseTitles[s.token] = shown; caseNameEl.textContent = shown;
        if (ZL.state.get().case) document.title = "Treatment timeline \u00b7 " + shown;
        const sm = summaryOf(s.token); if (sm) { sm.title = shown; sm.name = (r && r.name) || shown; }
        if (ZL.state.get().case) { ZL.state.get().case.title = shown; ZL.state.get().case.name = (r && r.name) || shown; }
        const h2 = document.querySelector('[data-testid="case-heading"]'); if (h2) h2.setAttribute("aria-label", "Case overview: " + shown);
        endRename(true); load();
      } catch (e) { err.textContent = (e && e.message) || "The name could not be saved."; input.focus(); }
    };
    input.addEventListener("keydown", (ev) => { if (ev.key === "Enter") { ev.preventDefault(); save(); } else if (ev.key === "Escape") { ev.preventDefault(); ev.stopPropagation(); endRename(true); } });
    renameBox = el("span", { class: "cv-rename" }, input, el("button", { type: "button", class: "btn btn--sm btn--primary", "data-testid": "btn-save-rename", onclick: save }, "Save"),
      el("button", { type: "button", class: "btn btn--sm", onclick: () => endRename(true) }, "Cancel"), err);
    caseNameEl.hidden = true; renameBtn.hidden = true; caseNameEl.after(renameBox);
    input.focus(); input.select();
  }
  document.addEventListener("DOMContentLoaded", () => {
    caseNameEl = ZL.$("#case-name"); if (!caseNameEl) return;
    renameBtn = el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-rename-case", "aria-label": "Rename this case", hidden: true, onclick: startRename }, "Rename");
    caseNameEl.after(renameBtn);
  });

  // ======== 2. the case overview block that starts the detail view ====================================================================================
  // ONE block (T-149 r2): the progress bars, one "Do this first" line, the call-outs, then (in the slot, filled by timeline.js) the Open-decisions buttons and the Case checks.
  // Nothing in it is said twice: the need-review number is the chip, the export state is one chip, the steps are the Case checks rail.
  // What the do-first item is, in the words a paralegal uses: the entry's date and record, the flag's title and records, the amount and its record.
  const day = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? new Date(+m[1], +m[2] - 1, +m[3]).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : ""; };
  function itemLabel(c, id) {
    const recNo = (rid) => { const r = (c.records || []).find((x) => x.id === rid); return r ? r.seq : null; };
    const recs = (ids) => { const n = (ids || []).map(recNo).filter((x) => x != null); return n.length ? " (" + (n.length === 1 ? "record " : "records ") + n.join(", ") + ")" : ""; };
    const e = [].concat(c.entries || [], c.undated_entries || []).find((i) => i.id === id);
    if (e) return (e.date ? day(e.date) + " entry" : "Undated entry") + recs(e.record_ids);
    const f = (c.flags || []).find((i) => i.id === id);
    if (f) { const ns = (f.computed && f.computed.record_nos) || []; return (f.title || "Flag") + (ns.length ? " (" + (ns.length === 1 ? "record " : "records ") + ns.join(", ") + ")" : ""); }
    const a = (c.amounts || []).find((i) => i.id === id);
    if (a) return (a.text || "Amount") + recs(a.record_ids);
    return "";
  }
  let headFocusUntil = 0, pendingHeadingFocus = false;
  function paintHead(box, c, tr) {
    const main = box.querySelector(".co-main"); if (!main) return;
    const ae = document.activeElement, keep = ae && main.contains(ae) ? ae.getAttribute("data-testid") : null;
    clear(main);
    const s = ZL.state.get(), p = ZL.progressOf(c), live = (a) => (a || []).filter((i) => i.state !== "rejected");
    const dec = (a) => ({ decided: a.length - a.filter(ZL.undecided).length, total: a.length });
    const prog = { entries: dec(live(c.entries).concat(live(c.undated_entries))), flags: dec(live(c.flags)), amounts: dec(live(c.amounts)) };
    const gate = gateOf(tr), title = titleOf(c);
    // The list summary is refreshed after every decision, so it wins; GET case's own next_action (read once) serves a case opened by link before the list answered. A line that names an
    // item she has just decided waits for the refreshed answer instead of pointing at a finished item.
    const sm = ZL.cases && ZL.cases.summary ? ZL.cases.summary(s.token) : null, na0 = sm ? sm.next_action : c.next_action;
    const named = na0 && na0.item_id ? [].concat(c.entries || [], c.undated_entries || [], c.flags || [], c.amounts || []).find((i) => i.id === na0.item_id) : null;
    let na = na0 && na0.reason && !(named && !ZL.undecided(named)) ? na0 : null;
    // The server names nothing (or the item she just decided) while items still wait: say so and point at the review, so a case with pending work always has one line. A case-check step that already says what to do (an edit to compare) says it itself.
    if (!na && p.left > 0 && !((tr && tr.steps) || []).some((st) => st.next_action && st.status !== "pass")) na = { reason: "Review the remaining " + plural(p.left, "item", "items") + ".", item_id: null };
    const label = na && na.item_id ? itemLabel(c, na.item_id) : "";
    box.toggleAttribute("data-do-first", !!na);
    if (na && na.item_id) box.setAttribute("data-do-first-item", na.item_id); else box.removeAttribute("data-do-first-item");
    box.toggleAttribute("data-done", p.left === 0 && !p.edits);
    const first = na ? el("div", { class: "co-first", "data-testid": "do-first" },
      el("p", { class: "co-first-text" }, el("strong", {}, "Do this first: "), label ? [el("strong", { class: "co-first-item", "data-testid": "do-first-item" }, label), " \u2014 "] : null, na.reason),
      el("button", { type: "button", class: "btn btn--sm btn--primary", "data-testid": "btn-do-first", onclick: () => {
        const ok = na.item_id && ZL.stepper && ZL.stepper.goto ? ZL.stepper.goto(na.item_id) : false;
        if (!ok && ZL.skipTo) ZL.skipTo("review");
      } }, "Go to it")) : null;
    main.append(...[
      el("div", { class: "co-top" }, el("h2", { id: "co-h", tabindex: "-1", "data-testid": "case-heading", "aria-label": "Case overview" + (title ? ": " + title : "") }, "Case overview"), bars("co", prog)),
      first,
      callouts("co", { needs: p.needs, needsId: "need-review-count", edits: p.edits, tray: (c.tray || []).length, blockers: gate ? gate.blockers || [] : [], warnings: gate ? gate.warnings || [] : [],
        ready: gate ? !!gate.ready : null, done: p.left === 0 && !p.edits, notReviewed: p.left })].filter(Boolean));
    if (keep) { const t = main.querySelector('[data-testid="' + keep + '"]'); if (t) t.focus({ preventScroll: true }); }
  }
  // "Start review" and "Do this first" are one first step: while the block names an item (next_action.item_id), Start review goes to that same item, not to the top of the list.
  document.addEventListener("click", (ev) => {
    const b = ev.target.closest && ev.target.closest('[data-testid="btn-start-review"]'); if (!b) return;
    const box = b.closest('[data-testid="case-overview"]'), id = box && box.getAttribute("data-do-first-item");
    if (!id || !ZL.stepper || !ZL.stepper.goto) return;
    if (ZL.stepper.goto(id)) { ev.preventDefault(); ev.stopImmediatePropagation(); }
  }, true);
  ZL.caseHead = function (c) {
    const s = ZL.state.get();
    const box = el("section", { class: "co", "data-testid": "case-overview", "aria-labelledby": "co-h" }, el("div", { class: "co-main" }), el("div", { class: "co-slot" }));
    paintHead(box, c, ZL.stepper && ZL.stepper.cachedTrace ? ZL.stepper.cachedTrace(s.token) : null);
    if (pendingHeadingFocus) { pendingHeadingFocus = false; headFocusUntil = Date.now() + 1500; }
    if (Date.now() < headFocusUntil) {          // opened from the list: land on the case heading, which names the case; a re-render in the next moments keeps it there
      const h = box.querySelector("#co-h");
      setTimeout(() => { const ae = document.activeElement; if (h.isConnected && (!ae || ae === document.body || ae.id === "co-h" || !ae.isConnected || ae.getClientRects().length === 0)) h.focus({ preventScroll: true }); }, 0);
    }
    return box;
  };
  const repaintHead = (tr, error) => {
    const box = document.querySelector('[data-testid="case-overview"]'), s = ZL.state.get();
    if (!box || !s.case) return;
    paintHead(box, s.case, tr !== undefined ? tr : ZL.stepper && ZL.stepper.cachedTrace ? ZL.stepper.cachedTrace(s.token) : null);
  };
  // A fresh trace arrived (after a decision, a rerun, or the first load), or a fresh case list: repaint the block's own part in place.
  document.addEventListener("zl:trace", (ev) => { const s = ZL.state.get(); if (ev.detail && ev.detail.token === s.token) repaintHead(ev.detail.data); });
  document.addEventListener("zl:cases", () => repaintHead());
  const gateOf = (tr) => ((tr && tr.steps) || []).find((x) => x.id === "export_gate") || null;
})();
