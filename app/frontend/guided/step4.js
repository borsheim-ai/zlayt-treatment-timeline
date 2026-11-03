/* Step 4: Get your letter (/case/<token>/letter). T-181, D-068, spec section 7. Builder A.
   GET /export: 200 = the letter and the notes for the attorney; 422 export_blocked / judge_not_run = one row per blocker with a button back to the step that fixes it.
   Copy and Download sit in the sticky action bar (always on screen). No drafted treatment paragraph (D-067). Letter text is inserted with textContent only.
   Test ids: letter-status, letter-text, notes-text, btn-copy-letter, btn-download-letter, btn-copy-notes, btn-download-notes, check-copy-anyway, btn-first-undecided, blockers, blocker (data-code),
   btn-blocker, btn-rejudge, cfg-exhibit, cfg-bates-prefix, cfg-bates-start, btn-save-cfg, cfg-error, prepared-badge, bar-msg, action-bar, page-error, btn-retry. */
(function () {
  const G = window.G, { h } = G;
  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text "null"
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;
  const slug = (t) => String(t || "case").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "case";

  G.pages.letter = async function (ctx) {
    const token = ctx.token, sig = ctx.signal;
    let c = ctx.case, exp = null, blockers = null, cfg = null, ack = null, flashTimer = null, bar0 = null;
    const main = h("main", { class: "wrap wide", id: "main" });
    ctx.view.append(main);

    const head = () => h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, "Step 4 of 4"), h("h1", { "data-testid": "page-title", tabindex: "-1" }, "Get your letter"),
      h("p", {}, "Copy the treatment section into your demand letter, or download it. The notes for the attorney are separate and are for the attorney only.")));

    /* ---- load ---- */
    async function load() {
      exp = null; blockers = null;
      /* the check trace first: its export gate says "ready" or lists the blockers without a refused request (a 422 would show as a console error); the export is read only when it will be 200 */
      try { const tr = await G.api.trace(token, sig), gate = (tr.steps || []).find((x) => x.id === "export_gate"); if (gate && !gate.ready && Array.isArray(gate.blockers) && gate.blockers.length) { blockers = gate.blockers; return; } }
      catch (e) { if (e.name === "AbortError") throw e; /* fall through: the export answers for itself */ }
      try { exp = await G.api.exportCase(token, sig); }
      catch (e) {
        if (e.name === "AbortError") throw e;
        if (e.status === 422 && e.detail && Array.isArray(e.detail.blockers)) blockers = e.detail.blockers;
        else throw e;
      }
      if (exp) { try { cfg = await G.api.call("GET", "/cases/" + encodeURIComponent(token) + "/export_config", null, sig); } catch (e) { if (e.name === "AbortError") throw e; cfg = null; } }
    }
    const undecidedCount = () => { const k = (c.review && c.review.counts) || {}; return (k.pending || 0) + (k.edit_to_check || 0); };
    function firstUndecidedUrl() {
      const s2 = [].concat(c.entries || [], c.undated_entries || [], c.flags || []).some(G.steps.undecided);
      return s2 ? G.url.timeline(token) : G.url.bills(token);
    }
    const itemUrl = (b) => !b.item_id ? G.url.timeline(token) : b.kind === "amount" ? G.url.bills(token, b.item_id) : G.url.timeline(token, b.item_id);
    const findItem = (id) => [].concat(c.entries || [], c.undated_entries || [], c.amounts || [], c.flags || []).find((i) => i.id === id);

    /* ---- downloads and copies (code, client side) ---- */
    function download(text, name) {
      const url = URL.createObjectURL(new Blob([text], { type: "text/plain;charset=utf-8" })), a = h("a", { href: url, download: name });
      document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
    function flash(btn, label) { const was = btn.getAttribute("data-label") || btn.textContent; btn.setAttribute("data-label", was); btn.textContent = label; clearTimeout(flashTimer); flashTimer = setTimeout(() => { btn.textContent = was; }, 2000); }
    async function copy(text, pre, btn, say) {
      try { await navigator.clipboard.writeText(text); flash(btn, "Copied"); say("Copied. Paste it into your demand letter."); return; } catch (_) { /* fall through */ }
      let ok = false;
      try { const r = document.createRange(); r.selectNodeContents(pre); const s = getSelection(); s.removeAllRanges(); s.addRange(r); ok = document.execCommand("copy"); } catch (_) { ok = false; }
      if (ok) { flash(btn, "Copied"); say("Copied. Paste it into your demand letter."); }
      else say("Your browser blocked copying. The text is selected: press Ctrl+C (Cmd+C on a Mac).");
    }

    /* ---- draw ---- */
    function draw(note) {
      ctx.layout("page"); if (bar0) bar0.el.remove();
      const title = G.titleOf(c), ready = !!exp, pending = ready ? undecidedCount() : 0;
      const letter = h("pre", { class: ready ? "doc" : "doc placeholder", id: "letter", tabindex: "0", "data-testid": "letter-text", "aria-label": "Your letter section" });
      const notes = h("pre", { class: ready ? "doc notes" : "doc notes placeholder", id: "notes", tabindex: "0", "data-testid": "notes-text", "aria-label": "Notes for the attorney" });
      if (ready) { letter.textContent = exp.letter_text; notes.textContent = exp.internal_notes_text; }
      else { letter.textContent = "Your letter will appear here once the problem above is fixed."; notes.textContent = "The notes appear with the letter."; }

      const copyL = h("button", { type: "button", class: "btn primary lg sbar-main", "data-testid": "btn-copy-letter", "data-autofocus": "" }, "Copy letter");
      const dlL = h("button", { type: "button", class: "btn lg", "data-testid": "btn-download-letter" }, "Download letter (.txt)");
      const copyN = h("button", { type: "button", class: "btn lg", "data-testid": "btn-copy-notes" }, "Copy notes");
      const dlN = h("button", { type: "button", class: "btn lg", "data-testid": "btn-download-notes" }, "Download notes (.txt)");
      const hasBlanks = (t) => /\[Ex\. __|Bates __/.test(t), hasDates = (t) => /date of service \[_+\]/.test(t);     // T-216: the date-of-service blanks are named beside the Ex/Bates ones, so "ready" never hides them
      const blanks = ready && (hasBlanks(exp.letter_text) || hasDates(exp.letter_text));
      const blankSay = () => { const a = hasBlanks(exp.letter_text), d = hasDates(exp.letter_text); return a && d ? " The [Ex. __ / Bates __] blanks and each “date of service [____]” blank are yours to fill in." : d ? " Each “date of service [____]” blank is yours to fill in." : a ? " The [Ex. __ / Bates __] blanks are yours to fill in." : ""; };
      const bar = G.sbar("", copyL, dlL); bar.el.classList.add("wide", "pair", "letter-bar"); bar0 = bar;
      const sayDefault = () => ready ? (pending && !ack.checked ? `Tick the box above to copy without ${plural(pending, "item")} that still need a decision.` : "Copy this into your demand letter." + (blanks ? blankSay() : "")) : "Fix the problem above first.";
      const gate = () => { const on = ready && (!pending || ack.checked); [copyL, dlL, copyN, dlN].forEach((b) => { b.disabled = !on; }); bar.say(sayDefault()); };
      copyL.addEventListener("click", () => copy(exp.letter_text, letter, copyL, (t) => bar.say(t)));
      copyN.addEventListener("click", () => copy(exp.internal_notes_text, notes, copyN, (t) => bar.say(t)));
      dlL.addEventListener("click", () => { download(exp.letter_text, `${slug(title)}-letter.txt`); bar.say("Downloaded your letter."); });
      dlN.addEventListener("click", () => { download(exp.internal_notes_text, `${slug(title)}-notes.txt`); bar.say("Downloaded the notes for the attorney."); });

      /* status row */
      let status, extra = null;
      if (!ready) {
        const n = blockers.length;
        status = h("div", { class: "note-box bad", role: "alert", "data-testid": "letter-status" }, h("span", { class: "nb-text" }, "The letter can't be made yet.", h("span", {}, "Fix the problem below, then come back here.")));
        extra = h("ul", { class: "blockers", "data-testid": "blockers" }, blockers.map(blockerRow));
        ctx.setStepStatus(4, plural(n, "problem"), "attn");
      } else if (pending) {
        ack = h("input", { type: "checkbox", "data-testid": "check-copy-anyway" }); ack.addEventListener("change", gate);
        status = h("div", { class: "note-box", "data-testid": "letter-status" }, h("span", { class: "nb-text" }, `${plural(pending, "item")} still ${pending === 1 ? "needs" : "need"} a decision.`, h("span", {}, "If you don't decide them, they stay out of the letter. The letter below is what would be sent now.")),
          h("a", { class: "btn primary lg", href: firstUndecidedUrl(), "data-testid": "btn-first-undecided" }, "Go to the first one"));
        extra = h("label", { class: "check anyway" }, ack, `Copy it anyway, without ${plural(pending, "item")}.`);
        ctx.setStepStatus(4, "Not yet", "todo");
      } else {
        const k = exp.counts || {}, parts = [plural(k.entries != null ? k.entries : 0, "timeline line")]; if (k.charges) parts.push(plural(k.charges, "charge"));
        status = h("div", { class: "note-box ok", "data-testid": "letter-status" }, h("span", { class: "nb-text" }, "Your letter is ready. Every item has an answer.", h("span", {}, `${parts.join(" and ")} ${parts.length === 1 && (k.entries || 0) === 1 ? "is" : "are"} in it. Nothing is left undecided.`)));
        ctx.setStepStatus(4, "Done", "done");
      }
      const prep = ready ? !!(exp.provenance && exp.provenance.generator_prepared) : !!(c.models && c.models.generator_prepared);
      const prov = prep ? h("p", { class: "prov" }, h("span", { class: "tag prep", title: G.provenance().note, "data-testid": "prepared-badge" }, "Prepared by our team"), " ", G.provenance().note) : null;

      const cfgBox = ready ? cfgPanel(letter, bar, (said) => { /* the letter text changed: the blanks sentence follows it */ if ((hasBlanks(exp.letter_text) || hasDates(exp.letter_text)) !== blanks) draw(said); else bar.say(said); }) : null;

      fill(main, head(), status, extra, prov,
        h("div", { class: "letter-grid" },
          h("section", {}, h("div", { class: "doc-h" }, h("h2", {}, "Your letter section"), h("span", { class: "muted" }, "Paste into the demand letter")), letter),
          h("section", {}, h("div", { class: "doc-h" }, h("h2", {}, "Notes for the attorney"), h("span", { class: "do-not-send" }, "Do not send")), notes, h("div", { class: "doc-actions" }, copyN, dlN))),
        cfgBox);
      ctx.view.append(bar.el);
      document.title = "Get your letter – Treatment Timeline";
      gate(); if (note) bar.say(note);
    }

    function blockerRow(b) {
      const code = (b.next_action && b.next_action.code) || "", id = b.item_id;
      let act;
      if (code === "DECIDE") act = h("a", { class: "btn primary", href: G.url.timeline(token), "data-testid": "btn-blocker" }, "Go to step 2");
      else if (code === "EDIT_SUMMARY" || code === "EDIT_QUOTE") act = h("a", { class: "btn primary", href: itemUrl(b), "data-testid": "btn-blocker" }, "Fix it");
      else if (code === "DISMISS_OR_ENTER_BY_HAND") act = h("a", { class: "btn primary", href: itemUrl(b), "data-testid": "btn-blocker" }, "Go to it");
      else if (code === "RERUN_JUDGE") {
        const it = id ? findItem(id) : null;
        if (it && it.rerun_available) act = h("button", { type: "button", class: "btn primary", "data-testid": "btn-rejudge", onclick: (ev) => rejudge(ev.currentTarget) }, "Run the second check again");
        else act = h("span", { class: "muted blk-note", "data-testid": "blocker-note" }, "The second check can't run here. Fix the wording in your own words, or leave the item out.");
      } else if (code === "CONFIRM_RERUN") act = h("a", { class: "btn primary", href: G.url.records(token), "data-testid": "btn-blocker" }, "Go to step 1");
      else if (code === "RUN_IN_PROGRESS") act = h("span", { class: "muted blk-note", "data-testid": "blocker-note" }, "Wait for drafting to finish.");
      else act = id ? h("a", { class: "btn primary", href: itemUrl(b), "data-testid": "btn-blocker" }, "Go to it") : h("a", { class: "btn primary", href: G.url.timeline(token), "data-testid": "btn-blocker" }, "Go to step 2");
      return h("li", { "data-testid": "blocker", "data-code": code || b.reason_code || "" }, h("span", { class: "blk-why" }, b.why || "This needs a look before the letter can be made."), act);
    }
    async function rejudge(btn) {
      btn.disabled = true; btn.textContent = "Checking…";
      try { await G.api.rejudge(token); } catch (e) { if (e.name === "AbortError") return; btn.disabled = false; btn.textContent = "Run the second check again"; btn.after(h("span", { class: "bad blk-note", role: "alert" }, e.message)); return; }
      try { c = await ctx.refresh(); await load(); draw(); } catch (e) { if (e.name === "AbortError") return; showError(e); }
    }

    /* ---- exhibit and page numbers (optional) ---- */
    function cfgPanel(letter, bar, changed) {
      const mk = (id, label, ph, val, mode) => ({ f: h("div", { class: "field" }, h("label", { for: id }, label), h("input", { id, "data-testid": "cfg-" + id.replace("cfg-", ""), placeholder: ph, value: val == null ? "" : String(val), maxlength: "20", inputmode: mode || null, autocomplete: "off" })) });
      const ex = mk("cfg-exhibit", "Exhibit", "e.g. 4", cfg && cfg.exhibit), bp = mk("cfg-bates-prefix", "Bates prefix", "e.g. RIV", cfg && cfg.bates_prefix), bs = mk("cfg-bates-start", "First number", "e.g. 1", cfg && cfg.bates_start, "numeric");
      const err = h("p", { class: "err-slot", role: "alert", "data-testid": "cfg-error" });
      const save = h("button", { type: "button", class: "btn lg", "data-testid": "btn-save-cfg" }, "Save numbers");
      const val = (x) => x.f.querySelector("input").value.trim();
      save.addEventListener("click", async () => {
        err.textContent = ""; const body = {}; if (val(ex)) body.exhibit = val(ex); if (val(bp)) body.bates_prefix = val(bp);
        if (val(bs)) { if (!/^\d{1,8}$/.test(val(bs))) { err.textContent = "The first number must be a whole number, like 1."; return; } body.bates_start = Number(val(bs)); }
        save.disabled = true;
        try { cfg = await G.api.call("PUT", "/cases/" + encodeURIComponent(token) + "/export_config", body); exp = await G.api.exportCase(token, sig); letter.textContent = exp.letter_text; changed("Saved. The numbers are in your letter."); }
        catch (e) { if (e.name === "AbortError") return; err.textContent = e.message; }
        finally { save.disabled = false; }
      });
      /* one Bates number per RECORD (the server counts record 1, record 2 ... in the order the records were read), and nothing in the records says how many pages each one is */
      const nRec = ((c && c.records) || []).length, pad = (n) => String(n).padStart(4, "0");
      const cite = (n) => { const st = val(bs) === "" || !/^\d{1,8}$/.test(val(bs)) ? 1 : Number(val(bs)); return `[Ex. ${val(ex) || "__"} / Bates ${val(bp) || val(bs) ? (val(bp) + pad(st + n - 1)) : "__"}]`; };
      const preview = h("p", { class: "cfg-preview", "data-testid": "cfg-preview", "aria-live": "polite" });
      const drawPreview = () => {
        if (!val(ex) && !val(bp) && !val(bs)) { preview.textContent = "Nothing filled in: every source line keeps “[Ex. __ / Bates __]” for you to fill in."; return; }
        preview.textContent = nRec > 1 ? `In your letter: record 1 reads ${cite(1)}, record 2 reads ${cite(2)}, and record ${nRec} reads ${cite(nRec)}.` : `In your letter: record 1 reads ${cite(1)}.`;
      };
      [ex, bp, bs].forEach((x) => x.f.querySelector("input").addEventListener("input", drawPreview));
      queueMicrotask(drawPreview);
      return h("div", { class: "panel cfg-panel", "data-testid": "cfg-panel" }, h("h2", {}, "Exhibit and Bates numbers (optional)"),
        h("p", { "data-testid": "cfg-rule" }, h("b", {}, "One Bates number per record, not per page. "), `Record 1 gets the first number you type, record 2 gets the next number, and so on in the order the records were read (${nRec} record${nRec === 1 ? "" : "s"} here). Use this only if each of your records is one Bates page in that order.`),
        h("p", { class: "muted" }, "If your records are longer, or in a different order, leave these blank and fill in the page numbers in Word. Filled in, the numbers replace “[Ex. __ / Bates __]” in every source line of the letter, and the letter then cites those pages."),
        h("div", { class: "cfg" }, ex.f, bp.f, bs.f, save), preview, err);
    }

    function showError(e) {
      ctx.layout("page"); main.replaceChildren(G.errorBlock(e, async () => { try { await load(); draw(); } catch (e2) { if (e2.name !== "AbortError") showError(e2); } }, "We couldn't make the letter"));
    }

    main.replaceChildren(head(), h("div", { class: "note-box", role: "status" }, h("span", { class: "nb-text" }, "Making your letter…")), h("div", { class: "letter-grid" }, h("section", {}, h("div", { class: "doc placeholder" }, "Making your letter…")), h("section", {}, h("div", { class: "doc notes placeholder" }, ""))));
    try { await load(); draw(); }
    catch (e) { if (e.name === "AbortError") return; showError(e); }
    return () => { clearTimeout(flashTimer); };
  };
})();
