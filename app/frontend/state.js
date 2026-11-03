/* Tiny store. ZL.state.get() -> {health, token, case, status, error}; subscribe(fn) re-renders on every set(). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  let s = { health: null, token: null, created: null, case: null, status: null };
  const subs = [];
  ZL.state = {
    get: () => s,
    set(patch) { s = Object.assign({}, s, patch); subs.forEach((f) => f(s)); },
    subscribe(f) { subs.push(f); },
    // Patch the local case from a POST .../review response (item + totals + review); T-043 calls this after each decision.
    applyReview(resp) {
      const c = s.case; if (!c || !resp || !resp.item) return;
      for (const k of ["entries", "undated_entries", "amounts", "flags"]) {
        const i = (c[k] || []).findIndex((x) => x.id === resp.item.id);
        if (i >= 0) { // the review response labels items with a generic kind ("amount"); an amount's own kind (charge / rate / ...) must survive
          const { kind, ...rest } = resp.item; c[k][i] = Object.assign({}, c[k][i], rest);
        }
      }
      if (resp.totals) c.totals = Object.assign({}, c.totals, resp.totals);
      if (resp.review) c.review = Object.assign({}, c.review, resp.review);
      ZL.state.set({ case: c });
    },
  };
  // Extension points for T-043 (frontend-2): register without editing T-042 files.
  ZL.hooks = { rowActions: [], panels: [] };           // rowActions: fn(entry, rowEl); panels: fn(case, mountEl) -> void
  ZL.registerRowActions = (fn) => ZL.hooks.rowActions.push(fn);
  ZL.registerPanel = (fn) => ZL.hooks.panels.push(fn);
  // A side panel that throws must not take the others down with it and must not fail silently: the error is re-raised as a window "error" event (so onerror, the console and the e2e
  // pageerror watcher all see it) and the panel's place shows a plain notice naming it. T-162 r3: a throw in one panel used to stop the forEach and hide the rest.
  ZL.panelFailed = (host, name, err) => {
    try { if (typeof reportError === "function") reportError(err); else setTimeout(() => { throw err; }); } catch (_) { /* reporting must never throw */ }
    if (!host) return;
    const note = document.createElement("p");
    note.className = "rv-error"; note.setAttribute("role", "alert"); note.setAttribute("data-testid", "panel-error"); note.setAttribute("data-panel-name", name);
    note.textContent = "This part of the page could not be drawn (" + name + "). The rest of the review still works. ";
    const again = document.createElement("button"); again.type = "button"; again.className = "btn btn--sm"; again.setAttribute("data-testid", "btn-error-action"); again.textContent = "Reload the page"; again.addEventListener("click", () => location.reload());   // T-174 F15
    note.append(again);
    if (host.getAttribute && host.getAttribute("data-panel")) { host.replaceChildren(note); } else host.append(note);
  };
})();
