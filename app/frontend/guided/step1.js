/* Step 1: Add records. T-181, D-068, spec section 4. Builder A.
   /new (before the case exists): name, how to add (paste / upload / sample / test case), Read the records. /case/<token>/records: records found, drafting, done, stopped.
   The primary action lives in a sticky action bar (G.sbar, also used by step 4), so it is on screen at 1440x900 and 390x844 without scrolling (T-180 review, major 1).
   Test ids: input-name, name-error, tile-paste, tile-file, tile-sample, tile-library, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar,
   btn-use-sample, btn-retry-read, btn-ocr, btn-hidden-anyway, check-hidden, records-list, records-notes, stage-list (li data-stage), draft-bar, draft-done, btn-next-step, draft-failed, btn-run-again, btn-run-yes, btn-run-cancel,
   prepared-badge, demo-note. Text only (textContent); no inline style attributes. */
(function () {
  const G = window.G, { h } = G;
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;
  const longDate = (iso) => { const d = /^\d{4}-\d{2}-\d{2}$/.test(iso || "") ? new Date(iso + "T00:00:00") : null; return d && !isNaN(d) ? d.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" }) : null; };
  const nice = (name) => { const s = String(name || "").replace(/^case[ _]?lib\d+[ _]/i, "").replace(/[_-]+/g, " ").trim(); return s ? s[0].toUpperCase() + s.slice(1) : "Test case"; };

  /* ---- the sticky action bar (shared with step 4): one instruction/error line, the primary button, and a slot for follow-up buttons that never moves the primary ---- */
  G.sbar = function (msgText, primary, ...statics) {
    const msg = h("p", { class: "sbar-msg", "aria-live": "polite", "data-testid": "bar-msg" }, msgText);
    const slot = h("span", { class: "sbar-alt" });                         // follow-up buttons (an error's action): grows to the LEFT of the primary on desktop, below it on phones, so the primary never moves
    const el = h("div", { class: "sbar", "data-testid": "action-bar" }, h("div", { class: "sbar-in" }, msg, h("div", { class: "sbar-btns" }, slot, primary, ...statics)));
    return { el, slot, say(text, kind) { msg.textContent = text; msg.className = "sbar-msg" + (kind ? " " + kind : ""); }, alts(...a) { slot.replaceChildren(...a); } };
  };
  G.longDate = longDate;

  /* ---------------------------------------------------------------- /new */
  G.pages.new = async function (ctx) {
    let hl;
    try { hl = await G.healthNow(ctx.signal); } catch (e) { if (e.name === "AbortError") return; hl = {}; }
    const demo = !!hl.demo_mode, lim = hl.limits || { max_chars: 60000, max_records: 40 }, sampleOk = hl.sample_available !== false;
    let lib = null;
    if (hl.local_mode !== false) try { lib = ((await G.api.call("GET", "/library", null, ctx.signal)).cases || []).map((x) => ({ id: x.id, name: nice(x.name) })); } catch (e) { if (e.name === "AbortError") return; lib = null; }
    if (lib && !lib.length) lib = null;
    const ONLY = () => (lib ? "This demo can only read the sample case and our test cases." : "This demo can only read the sample case.");
    const st = { how: demo ? (sampleOk ? "sample" : lib ? "library" : "sample") : "paste", text: "", file: null, lib: null, reading: false, again: null };

    /* name */
    const nameInput = h("input", { id: "case-name", type: "text", maxlength: "120", autocomplete: "off", "data-testid": "input-name", "aria-describedby": "name-hint name-error" });
    const nameErr = h("span", { class: "hint bad", id: "name-error", role: "alert", "data-testid": "name-error" });
    nameInput.addEventListener("input", () => { nameErr.textContent = ""; });

    /* tiles */
    const tiles = [
      { key: "paste", head: "Paste text", sub: "Copy the records and paste them here.", off: demo },
      { key: "file", head: "Upload a file", sub: "A .txt or .pdf file, up to 5 MB.", off: demo },
      sampleOk ? { key: "sample", head: "Use the sample case", sub: "A short made-up case to try it out." } : null,
      lib ? { key: "library", head: "Choose a test case", sub: "One of our made-up cases, ready to read." } : null,
    ].filter(Boolean);
    const tileEls = tiles.map((t) => {
      const input = h("input", { type: "radio", name: "how", value: t.key, disabled: t.off, "data-testid": "radio-" + t.key });
      if (st.how === t.key) input.checked = true;
      input.addEventListener("change", () => { st.how = t.key; clearMsg(); drawBox(); sync(); });
      return h("label", { class: "tile" + (t.off ? " off" : ""), "aria-disabled": t.off ? "true" : null, "data-testid": "tile-" + t.key }, input, h("span", { class: "tl-h" }, t.head), h("p", {}, t.sub), t.off ? h("p", { class: "tile-why" }, "Not available in this demo.") : null);
    });

    /* the one input box: fixed height, shows what was chosen */
    const box = h("div", { class: "input-box solid", "data-testid": "input-box" });
    const fileInput = h("input", { type: "file", class: "sr-file", accept: ".txt,.pdf,text/plain,application/pdf", "data-testid": "file-input", tabindex: "-1", "aria-hidden": "true" });
    fileInput.addEventListener("change", () => { setFile(fileInput.files && fileInput.files[0]); fileInput.value = ""; });
    function setFile(f) {
      clearMsg(); st.file = null; if (!f) { drawBox(); sync(); return; }
      const ext = (f.name.split(".").pop() || "").toLowerCase();
      if (ext !== "txt" && ext !== "pdf") fail({ msg: "We can read .txt and .pdf files. Choose another file." });
      else if (f.size > 5 * 1024 * 1024) fail({ msg: "That file is bigger than 5 MB. Choose a smaller one." });
      else st.file = f;
      drawBox(); sync();
    }
    function drawBox() {
      if (st.how === "paste") {
        const ta = h("textarea", { "aria-label": "Paste the records here", placeholder: "Paste the records here", "data-testid": "input-text", spellcheck: "false" }); ta.value = st.text;
        ta.addEventListener("input", () => { st.text = ta.value; clearMsg(); sync(); });
        box.className = "input-box solid"; box.replaceChildren(h("div", { class: "box-col" }, ta, h("p", { class: "hint" }, `Up to ${lim.max_chars.toLocaleString("en-US")} characters or ${lim.max_records} records.`)));
      } else if (st.how === "file") {
        const choose = h("button", { type: "button", class: "btn lg", "data-testid": "btn-choose-file", onclick: () => fileInput.click() }, st.file ? "Choose another file" : "Choose a file");
        box.className = "input-box" + (st.file ? " solid" : "");
        box.replaceChildren(h("div", { class: "box-col center" }, st.file ? [h("b", { class: "big-name", "data-testid": "file-name" }, st.file.name), h("span", { class: "muted" }, `${(st.file.size / 1024).toFixed(0)} KB`)]
          : [h("b", {}, "Drop a .txt or .pdf file here"), h("span", { class: "muted" }, "or")], choose));
      } else if (st.how === "library") {
        box.className = "input-box solid";
        box.replaceChildren(h("fieldset", { class: "libs" }, h("legend", { class: "sr" }, "Choose a test case"), lib.map((x) => {
          const r = h("input", { type: "radio", name: "lib", value: x.id, "data-testid": "library-" + x.id }); if (st.lib === x.id) r.checked = true;
          r.addEventListener("change", () => { st.lib = x.id; clearMsg(); sync(); });
          return h("label", { class: "lib-row" }, r, h("span", {}, x.name));
        })));
      } else {
        box.className = "input-box solid";
        box.replaceChildren(h("div", { class: "box-col center" }, h("b", { class: "big-name" }, "The sample case"), h("span", { class: "muted" }, "9 short records from a made-up car-accident case. Every name and date in it is invented.")));
      }
    }
    ["dragover", "dragenter"].forEach((ev) => box.addEventListener(ev, (e) => { if (st.how === "file") { e.preventDefault(); box.classList.add("over"); } }));
    box.addEventListener("dragleave", () => box.classList.remove("over"));
    box.addEventListener("drop", (e) => { if (st.how !== "file") return; e.preventDefault(); box.classList.remove("over"); setFile(e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]); });

    /* the action bar */
    const read = h("button", { type: "button", class: "btn primary lg sbar-main", "data-testid": "btn-read", "data-autofocus": "" }, "Read the records");
    const bar = G.sbar("", read);
    const hint = () => st.how === "paste" ? "Paste the records, then press Read the records." : st.how === "file" ? "Choose a file, then press Read the records." : st.how === "library" ? "Pick a test case, then press Read the records." : "Press Read the records to open the sample case.";
    function canRead() { return !st.reading && (st.how === "sample" || (st.how === "paste" && st.text.trim() !== "") || (st.how === "file" && !!st.file) || (st.how === "library" && !!st.lib)); }
    function sync() { read.disabled = !canRead(); read.textContent = st.reading ? "Reading…" : "Read the records"; if (!bar.err) bar.say(hint()); }
    function clearMsg() { bar.err = false; bar.alts(); bar.say(hint()); }
    function fail(f) {
      bar.err = true; bar.say(f.msg, "bad");
      bar.alts(...(f.alts || []).map((a) => a.node || h("button", { type: "button", class: "btn", "data-testid": a.id, onclick: a.fn }, a.label)));
    }

    function plain(e, pdf) {
      const reason = e.detail && e.detail.reason, code = e.code, s = e.status;
      const again = { id: "btn-retry-read", label: "Try again", fn: () => submit(st.again || {}) };
      if (s === 0 || s >= 500) return { msg: "We couldn't reach the server. Your text is still here.", alts: [again] };
      if (s === 422 && code === "invalid_title") return { field: e.message };
      if (s === 413) return { msg: pdf ? "That file is bigger than 5 MB. Choose a smaller one." : `That's more than we can read at once (${lim.max_chars.toLocaleString("en-US")} characters or ${lim.max_records} records). Split it into two cases.` };
      if (s === 409 && code === "demo_mode_unsupported_input") return { msg: ONLY(), alts: sampleOk ? [{ id: "btn-use-sample", label: "Use the sample case", fn: () => { st.how = "sample"; setRadio(); drawBox(); clearMsg(); sync(); } }] : [] };
      if (s === 429) return { msg: reason === "demo_full" || reason === "demo_busy" ? e.message : "We're reading other files right now. Try again in a moment.", alts: [again] };
      if (reason === "pdf_no_text_layer") {
        const ocr = e.detail && e.detail.ocr && e.detail.ocr.status && e.detail.ocr.status.available;
        return { msg: "This PDF looks scanned, so it has no text we can read.", alts: ocr ? [{ id: "btn-ocr", label: "Read the scanned pages", fn: () => submit({ ocr: true }) }] : [] };
      }
      if (reason === "pdf_only_hidden_text") {
        const ok = h("input", { type: "checkbox", "data-testid": "check-hidden" }), go = h("button", { type: "button", class: "btn", disabled: true, "data-testid": "btn-hidden-anyway", onclick: () => submit({ includeHidden: "all" }) }, "Use these pages anyway");
        ok.addEventListener("change", () => { go.disabled = !ok.checked; });
        return { msg: "Everything on these pages is hidden text, so we kept it out.", alts: [{ node: h("label", { class: "check inline" }, ok, "I looked at these pages myself") }, { node: go }] };
      }
      if (reason && /^pdf_|^ocr_/.test(reason)) return { msg: e.message, alts: [{ id: "btn-choose-other", label: "Choose another file", fn: () => { st.how = "file"; setRadio(); drawBox(); clearMsg(); sync(); fileInput.click(); } }] };
      if (s === 400 && /empty/i.test(e.message)) return { msg: "There's nothing to read yet. Paste the records or choose a file." };
      return { msg: e.message };
    }
    function setRadio() { tileEls.forEach((t) => { const r = t.querySelector("input"); r.checked = r.value === st.how; }); }

    async function postPdf(file, title, extra) {
      const q = new URLSearchParams(); if (title) q.set("title", title); if (extra.ocr) q.set("ocr", "true"); if (extra.includeHidden) q.set("include_hidden", extra.includeHidden);
      let res, data = null;
      try { res = await fetch("/api/cases/pdf" + (q.toString() ? "?" + q : ""), { method: "POST", headers: { "Content-Type": "application/pdf" }, body: file, signal: ctx.signal }); }
      catch (e) { if (e && e.name === "AbortError") throw e; throw new G.ApiError(0, null); }
      try { data = await res.json(); } catch (_) { data = null; }
      if (res.status >= 400) throw new G.ApiError(res.status, data && data.error);
      return data;
    }
    async function submit(extra) {
      if (st.reading) return; st.again = extra || {}; st.reading = true; clearMsg(); nameErr.textContent = ""; sync();
      const title = nameInput.value.trim(), pdf = st.how === "file" && st.file && /\.pdf$/i.test(st.file.name);
      try {
        let r;
        if (st.how === "paste") r = await G.api.createCase({ text: st.text, ...(title ? { title } : {}) });
        else if (st.how === "sample") r = await G.api.createCase({ sample: true, ...(title ? { title } : {}) });
        else if (st.how === "library") r = await G.api.createCase({ library: st.lib, ...(title ? { title } : {}) });
        else if (pdf) r = await postPdf(st.file, title, extra || {});
        else r = await G.api.createCase({ text: await st.file.text(), ...(title ? { title } : {}) });
        G.cases.add(r.token); ctx.go(G.url.records(r.token));
      } catch (e) {
        if (e && e.name === "AbortError") return;
        st.reading = false; const f = plain(e, pdf);
        if (f.field) { nameErr.textContent = f.field; nameInput.focus(); bar.err = true; bar.say("Fix the case name, then press Read the records.", "bad"); }
        else fail(f);
        sync();
      }
    }
    read.addEventListener("click", () => submit({}));

    drawBox();
    const main = h("main", { class: "wrap", id: "main" },
      h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, "Step 1 of 4"), h("h1", { "data-testid": "page-title", tabindex: "-1" }, "Add records"),
        h("p", {}, "Add the medical records for this case. We'll read them and draft a timeline for you to check."))),
      h("div", { class: "panel" },
        demo ? h("div", { class: "note-box demo-note", "data-testid": "demo-note" }, h("span", { class: "nb-text" }, ONLY(), h("span", {}, "Pasting your own records or uploading a file isn't available here."))) : null,
        h("div", { class: "field" }, h("label", { for: "case-name" }, "Name this case (optional)"), nameInput, h("span", { class: "hint", id: "name-hint" }, "For example the client's name. You can change it later."), nameErr),
        h("fieldset", { class: "how" }, h("legend", { class: "sr" }, "How do you want to add the records?"), h("div", { class: "tiles" + (tiles.length > 3 ? " four" : "") }, tileEls)),
        box, fileInput));
    ctx.view.append(main, bar.el);
    sync();
  };

  /* ---------------------------------------------------------------- /case/<token>/records */
  const STAGES = [["ingest", "Reading the records"], ["extract", "Writing one line for each record", "Getting the line our team prepared for each record"], ["verify", "Checking every line word for word against the record"],
    ["judge_entries", "A second AI check of each line"], ["amounts", "Finding the bill amounts"], ["conflicts", "Comparing the records with each other"],
    ["flags", "Looking for things the attorney should know"], ["finalize", "Putting it all together"]];

  G.pages.records = async function (ctx) {
    const token = ctx.token; let c = ctx.case, dead = false, timer = null, bar = null;
    G.cases.add(token);
    const prepared = () => G.provenance().kind === "prepared";
    const counts = () => { const n = G.steps.counts(c); return { lines: n.step2.total, bills: n.step3.total }; };
    const nextTarget = () => { const n = counts(); return n.lines > 0 ? ["Go to step 2: Check the timeline", G.url.timeline(token)] : n.bills > 0 ? ["Go to step 3: Check the bills", G.url.bills(token)] : ["Go to step 4: Get your letter", G.url.letter(token)]; };
    const main = h("main", { class: "wrap", id: "main" });
    ctx.view.append(main);
    const put = (newBar, ...kids) => { main.replaceChildren(...kids.filter(Boolean)); if (bar) bar.el.remove(); bar = newBar; if (bar) ctx.view.append(bar.el); };
    const heading = (title, sub) => h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, "Step 1 of 4"), h("h1", { "data-testid": "page-title", tabindex: "-1" }, title), sub ? h("p", {}, sub) : null));
    let moved = false;      // a screen change after load moves focus to the new heading (a first paint is left to the shell)
    const focusTitle = () => { if (!moved) return; const t = main.querySelector("h1"); if (t) t.focus({ preventScroll: true }); };

    const recList = (id) => h("ol", { class: "list", "data-testid": id || "records-list" }, (c.records || []).map((r) => {
      const d = longDate(r.date_iso); return h("li", {}, h("span", { class: "n" }, String(r.seq)), h("span", { class: "num" + (d ? "" : " muted") }, d || "Date unclear"), h("span", { class: "src" }, r.source_label || "Record " + r.seq));
    }));
    function notes() {
      const out = [], w = new Set((c.warnings || []).map((x) => x.code)), n = (c.dates_to_confirm || []).length;
      if (n) out.push(h("div", { class: "note-box" }, h("span", { class: "nb-text" }, `${n === 1 ? "1 record has a date" : n + " records have dates"} we need you to check. You'll do that in step 2.`)));
      if (w.has("PHI_PATTERN")) out.push(h("div", { class: "note-box bad" }, h("span", { class: "nb-text" }, "Some text looks like real personal details (a phone, SSN or record number). Only use synthetic records.")));
      if (w.has("SPLIT_AMBIGUOUS") || w.has("UNSPLIT_TEXT")) out.push(h("div", { class: "note-box" }, h("span", { class: "nb-text" }, "Some text didn't look like a record. We kept it as its own record so nothing is lost.")));
      if (c.injection && c.injection.banner) out.push(h("div", { class: "note-box bad" }, h("span", { class: "nb-text" }, c.injection.banner)));
      if (!n && (c.records || []).length && c.records.every((r) => r.date_status === "parsed")) out.push(h("div", { class: "note-box ok" }, h("span", { class: "nb-text" }, "Every record has a date we could read.")));
      return h("div", { class: "notes", "data-testid": "records-notes" }, out);
    }

    /* ---- records found ---- */
    function drawFound() {
      ctx.layout("page"); ctx.setStepStatus(1, "Not started", "todo");
      const msg = h("span", {}, "Next, we'll draft one timeline line for each record.");
      const draft = h("button", { type: "button", class: "btn primary lg sbar-main", "data-testid": "btn-draft", "data-autofocus": "" }, "Draft the timeline");
      const over = h("a", { class: "btn quiet", href: G.url.new(), "data-testid": "btn-start-over" }, "Start over with other records");
      const b = G.sbar("", draft, over); b.say(msg.textContent);
      draft.addEventListener("click", () => run(false, draft, b));
      put(b, heading(`We found ${plural((c.records || []).length, "record")}`, "Check that these are the records you meant to add. Next, we'll draft a one-line timeline entry for each one."),
        h("div", { class: "panel" }, notes(), recList()));
    }
    async function run(confirm, btn, b) {
      btn.disabled = true; const label = btn.textContent; btn.textContent = "Starting…";
      try { await G.api.run(token, confirm); }
      catch (e) {
        if (e.code === "run_in_progress") { /* already going: show it */ }
        else if (e.status === 409 && e.code === "needs_confirm") { btn.disabled = false; btn.textContent = label; return askRerun(b); }
        else { btn.disabled = false; btn.textContent = label; b.say(e.code === "demo_mode_unsupported_input" ? ONLY() : e.message, "bad"); return; }
      }
      c = { ...c, status: "running" }; moved = true; drawRunning(); poll();
    }
    function askRerun(b) {
      b.say("Run it again? Your answers so far are kept.", "bad");
      const yes = h("button", { type: "button", class: "btn primary", "data-testid": "btn-run-yes", onclick: () => run(true, yes, b) }, "Yes, run it again"), no = h("button", { type: "button", class: "btn", "data-testid": "btn-run-cancel", onclick: () => { b.say(""); b.alts(); } }, "Cancel");
      b.alts(yes, no); yes.focus();
    }

    /* ---- drafting ---- */
    let live = null;
    function drawRunning() {
      ctx.layout("page");
      const items = STAGES.map(([id, a, b2]) => h("li", { "data-stage": id }, h("span", { class: "ic", "aria-hidden": "true" }), prepared() && b2 ? b2 : a));
      const barFill = h("i", { "data-testid": "draft-bar" }), count = h("span", { class: "num", "data-testid": "draft-count" }, "");
      live = { items, barFill, count };
      const main1 = h("button", { type: "button", class: "btn primary lg sbar-main", disabled: true }, "Drafting…");
      const b = G.sbar("This usually takes under a minute. You can leave this page; we'll keep going.", main1);
      put(b, heading("Drafting the timeline", "This usually takes under a minute. You can leave this page; we'll keep going."),
        h("div", { class: "panel fixed-box" }, h("div", { class: "count-line" }, h("span", {}, "Working on it"), count),
          h("div", { class: "bar", role: "progressbar", "aria-label": "Drafting progress", "aria-valuemin": "0", "aria-valuemax": String(STAGES.length) }, barFill), h("ol", { class: "stages", "data-testid": "stage-list", "aria-live": "polite" }, items)));
      showStage(0, STAGES.length);
      focusTitle();
    }
    function showStage(idx, total) {
      if (!live) return;
      live.items.forEach((li, i) => { li.className = i < idx ? "done" : i === idx ? "now" : ""; li.firstChild.textContent = i < idx ? "✓" : ""; });
      live.barFill.style.width = Math.round((idx / total) * 100) + "%"; live.count.textContent = `${Math.min(idx + 1, total)} of ${total}`;
      live.barFill.parentNode.setAttribute("aria-valuenow", String(idx));
      ctx.setStepStatus(1, `Drafting ${Math.min(idx + 1, total)} of ${total}`, "todo");
    }
    async function poll() {
      if (dead) return;
      let s;
      try { s = await G.api.status(token, ctx.signal); }
      catch (e) { if (e.name === "AbortError" || dead) return; timer = setTimeout(poll, 2000); return; }
      if (dead) return;
      if (s.status === "ready" || s.status === "failed") {
        try { c = await ctx.refresh(); } catch (e) { if (e.name === "AbortError" || dead) return; c = { ...c, status: s.status, error: s.error }; }
        moved = true; return s.status === "ready" ? drawDone() : drawFailed();
      }
      const stages = s.stages && s.stages.length ? s.stages : STAGES.map((x) => x[0]); const i = Math.max(0, stages.indexOf(s.stage));
      showStage(i, stages.length); timer = setTimeout(poll, 1000);
    }

    /* ---- done ---- */
    function drawDone() {
      ctx.layout("page"); ctx.setStepStatus(1, "Done", "done");
      const n = counts(), hl = G.store.health || {}, [label, href] = nextTarget();
      const msg = `${plural(n.lines, "timeline item")} and ${n.bills ? plural(n.bills, "bill amount") : "no bill amounts"} ${n.lines + n.bills === 1 ? "is" : "are"} ready for you to check.`;
      const go = h("a", { class: "btn primary lg sbar-main", href, "data-testid": "btn-next-step", "data-autofocus": "" }, label);
      const b = G.sbar("Step 1 is done.", go);
      const prep = (c.models && c.models.generator_prepared) || prepared();
      put(b, heading("Records added"), h("div", { class: "panel", "data-testid": "draft-done" },
        h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-title" }, "All set."), h("p", { "data-testid": "done-counts" }, msg))),
        hl.ai_banner ? h("p", { class: "muted ai-line", "data-testid": "ai-banner" }, hl.ai_banner) : null,
        prep ? h("p", { class: "prov" }, h("span", { class: "tag prep", title: G.provenance().note, "data-testid": "prepared-badge" }, "Prepared by our team"), " ", G.provenance().note) : null),
        h("div", { class: "panel" }, h("h2", {}, `${plural((c.records || []).length, "record")} added`), recList(), h("p", { class: "muted after-list" }, "To add more records, start a new case. ", h("a", { href: G.url.new() }, "Start a new case"))));
      focusTitle();
    }

    /* ---- stopped ---- */
    function drawFailed() {
      ctx.layout("page"); ctx.setStepStatus(1, "Run again", "attn");
      const err = c.error || {}, recs = (err.records || []).map(Number).filter(Boolean);
      const list = recs.length ? (recs.length === 1 ? `record ${recs[0]}` : `records ${recs.slice(0, -1).join(", ")} and ${recs[recs.length - 1]}`) : "";
      const again = h("button", { type: "button", class: "btn primary lg sbar-main", "data-testid": "btn-run-again", "data-autofocus": "" }, "Run it again");
      const home = h("a", { class: "btn quiet", href: "/", "data-testid": "link-home" }, "Back to your cases");
      const b = G.sbar("Some of the work finished. Nothing you decided is lost.", again, home);
      again.addEventListener("click", () => run(false, again, b));
      const hasItems = counts().lines + counts().bills > 0;
      put(b, heading("Drafting stopped", "Some of the work finished. You can run it again; nothing you decided is lost."),
        h("div", { class: "panel fixed-box", "data-testid": "draft-failed" }, h("div", { class: "done-hero" }, h("div", { class: "big-warn", "aria-hidden": "true" }, "!"),
          h("div", {}, h("h2", {}, "Drafting stopped before it finished."), err.message ? h("p", { "data-testid": "failed-message" }, err.message) : null)),
          list ? h("p", { class: "muted" }, `No line was written for ${list}. You can write ${recs.length === 1 ? "it" : "them"} yourself in step 2.`) : null,
          hasItems ? h("p", { class: "muted" }, "The items that did finish can be checked now in steps 2 and 3.") : null,
          h("h3", { class: "sub-h" }, "Your records"), recList()));
      focusTitle();
    }

    if (c.status === "ingested") drawFound();
    else if (c.status === "running") { drawRunning(); poll(); }
    else if (c.status === "failed") drawFailed();
    else drawDone();
    return () => { dead = true; if (timer) clearTimeout(timer); };
  };
})();
