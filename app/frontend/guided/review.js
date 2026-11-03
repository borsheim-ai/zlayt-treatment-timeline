/* Shared one-item review engine for the two review pages (step 2 timeline, step 3 bills). OWNER: the Step 2 + Step 3 builder (frontend-B). Spec 2.5-2.7, 5, 6; D-066, D-065, D-067, T-178.
   A step module calls G.review.run(ctx, cfg) and describes each item as a SCREEN (see "screen" below); this file owns the fixed frame (title row, two cards, action bar), the queue, every
   write (version + expected_status on each review POST, 409 -> reload, COMPARE_REQUIRED -> compare box), Undo, keyboard (A yes, D no, E third, arrows move) and focus.
   Nothing here touches the shell. No innerHTML anywhere: record text, quotes and titles go in with textContent. No style attributes (CSSOM only, for the progress bar).
   cfg = { step, title, unit ("Item"|"Amount"), chip (bool), buildQueue(c) -> [{id, optional?}], find(c, id), present(S, item, q) -> screen, empty(S) -> node, done(S) -> node,
           statusFor(S, item, q, resp, action) -> "kept in the letter", onResponse?(S, resp) }
   screen = { tag?: {cls, text, title}, tag2?, sub, body: [Node], foot: {cls, nodes}, question, yes: {label, sub?, key?, disabled?: fn, run}, no: {...}|null, third: {label, run, hint?}|null,
              later: {label?, run}|false, src: {head, nodes: () => [Node]}, counter?: string, focus?: "yes"|"field" } */
(function () {
  const G = window.G, { h } = G;
  const R = (G.review = G.review || {});

  /* ---------- words: server sentences get the plain vocabulary of spec section 10 (never the facts); text inside “curly quotes” is record text and is left alone ---------- */
  const WHY_OK = /^Quote found word for word, every number in the summary is in the quote, and the second check agreed\.?$/;
  R.plain = function (text) {
    if (text == null) return "";
    const s = String(text);
    if (WHY_OK.test(s.trim())) return "The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.";
    return s.split(/(“[^”]*”)/).map((part, i) => (i % 2 ? part : part
      .replace(/The quote carries (.+?) that the summary leaves out\. Put it back in the summary\./g, (m, what) => `Your line leaves out ${what.replace(/\bthe quote gives\b/, "the highlighted words give")} that the highlighted words have. Put it back in the line.`)
      .replace(/ \(the internal notes say why\), so none of them is in Billed charges; dismiss this (?:entry|line) unless it states treatment\./g, ". You decide in step 3, Check the bills, whether to count them. Dismiss this line unless it states treatment.")
      .replace(/\bpick a quote\b/g, "pick highlighted words").replace(/\ba quote\b/g, "highlighted words")
      .replace(/\b([Tt])he (?:AI )?second (?:AI )?check\b/g, (m, t) => (t === "T" ? "A second AI check" : "a second AI check"))
      .replace(/\bsecond check\b/g, "second AI check")
      .replace(/\bthe quoted text\b/g, "the highlighted words").replace(/\bquoted text\b/g, "highlighted words")
      .replace(/\b([Tt])he quote (does not|is not|is|has|says|contains|states|shows|carries|gives|labels)\b/g, (m, t, v) => `${t}he highlighted words ${v === "is" ? "are" : v === "has" ? "have" : v === "carries" ? "carry" : v === "gives" ? "give" : v === "labels" ? "label" : v === "does not" ? "do not" : v === "is not" ? "are not" : v === "says" ? "say" : v === "contains" ? "contain" : v === "states" ? "state" : "show"}`)
      .replace(/\bsummary or quote\b/g, "line or highlighted words").replace(/\bthe quotes?\b/g, "the highlighted words").replace(/\bQuote\b/g, "The highlighted words").replace(/\bquotes?\b/g, "highlighted words")
      .replace(/\bthe summary\b/g, "the line").replace(/\bThe summary\b/g, "The line").replace(/\bsummary\b/g, "line")
      .replace(/\ban itemized service line\b/g, "a single dated bill line").replace(/\bitemized service line\b/g, "single dated bill line").replace(/\ban itemized\b/g, "a line-by-line").replace(/\bitemized\b/g, "line-by-line")
      .replace(/\binternal notes\b/g, "notes for the attorney").replace(/\bthe model's\b/gi, G.provenance().kind === "prepared" ? "the prepared answer's" : "the AI's").replace(/\bmodel\b/g, G.provenance().kind === "prepared" ? "prepared answer" : "AI")
      .replace(/\bflags\b/g, "warnings").replace(/\bflag\b/g, "warning").replace(/\bthis entry\b/g, "this line"))).join("");
  };

  /* ---------- a refused edit that dropped a qualifier: name the words (UX review T-181 major). The server says which KIND (detail.qualifiers); the words are found in the quote by code. ---------- */
  const QUAL = {
    self_report: { re: /\b(?:complained of|complains of|complaint of|c\/o|reports?|reported|states?|stated|says?|said|denies|denied|per (?:the )?patient|according to)\b/gi, because: "which says whose account this is" },
    hedge: { re: /\b(?:may|might|possibly|possible|probable|probably|likely|appears?|suspected|suggests?|suggestive of|consistent with|cannot be excluded|rule out|r\/o)\b/gi, because: "which shows it is not certain" },
    negation: { re: /\b(?:no|not|denies|denied|without|negative|none|never)\b/gi, because: "which says something is not there" },
    laterality: { re: /\b(?:left|right|bilateral)\b/gi, because: "which says which side" },
    approx: { re: /\b(?:approx\.?|approximately|about|around|roughly|estimated)\b/gi, because: "which shows the figure is only close" },
  };
  const FALLBACK_WORDS = { self_report: "a phrase that says whose account this is", hedge: "a word that shows it is not certain", negation: "a word that says something is not there", laterality: "the side (left or right)", approx: "a word that shows the figure is only close" };
  R.droppedText = function (kinds, quote, summary, before) {
    const low = String(summary || "").toLowerCase(), out = [];
    (kinds || []).forEach((k) => {
      const q = QUAL[k]; if (!q) return;
      const gone = (text) => [...new Set((String(text || "").match(q.re) || []).map((w) => w.toLowerCase()))].filter((w) => !low.includes(w));
      const found = gone(before).length ? gone(before) : gone(quote);          // the words she took out of the line first, else the quote's own words
      out.push(found.length ? `“${found.slice(0, 3).join("”, “")}”, ${q.because}` : FALLBACK_WORDS[k]);
    });
    if (!out.length) return null;
    return `Your line leaves out ${out.join("; and ")}. Put ${out.length === 1 && /^“[^”]+”,/.test(out[0]) && !/”, “/.test(out[0]) ? "it" : "those words"} back in the line.`;
  };

  /* ---------- dates and money (code only) ---------- */
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  R.longDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1]} ${+m[3]}, ${m[1]}` : ""; };
  R.shortDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1].slice(0, 3)} ${+m[3]}, ${m[1]}` : "No date"; };
  R.money = (cents) => (cents < 0 ? "-" : "") + "$" + (Math.abs(cents) / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  /* ---------- provenance tags (D-065): a prepared answer says "Prepared answer", never "AI" ---------- */
  R.tagFor = function (item) {
    const p = G.provenance();
    if (item.entered_by_reviewer || (item.edited && item.edited.summary)) return { cls: "you", text: "Written by you" };
    if (item.prepared) return { cls: "prep", text: "Prepared answer", title: p.note };
    if (item.origin_label) return { cls: "never", text: item.origin_label, title: "Found by a program, not drafted by an AI." };      // T-214: a flag only code found says so; it is not a prepared answer
    if (item.ai_drafted === false || item.origin === "code") return null;
    return { cls: "ai", text: "AI draft", title: p.kind === "live" ? p.note : "Drafted by an AI. " + p.note };
  };
  // G.provenance() follows the open case: a case whose lines an AI wrote says so, never "not written by an AI model" (T-181 r2)
  R.aiNote = () => { const p = G.provenance(), hl = G.store.health; return p.kind === "live" && hl && hl.ai_banner ? hl.ai_banner : p.note; };

  /* ---------- the second check disputed this item (D-066; the same rule as review.judge_dispute) ---------- */
  const DISPUTE = { partially: "A second AI check found this only partly supported by the highlighted words.", unsupported: "A second AI check found this not supported by the highlighted words.",
    disagrees: "A second AI check disagreed with the first result for this item." };
  R.dispute = function (item) {
    const j = item && item.ladder && item.ladder.judge, vv = j && j.verdict, v = vv === "disagree" ? "disagrees" : vv;
    if (DISPUTE[v]) return v;
    const rs = (item && (item.state_reasons || item.reasons)) || [];
    return rs.includes("JUDGE_PARTIAL") ? "partially" : rs.includes("JUDGE_UNSUPPORTED") ? "unsupported" : rs.includes("JUDGE_DISAGREES") ? "disagrees" : null;
  };
  /* An amount's second check names the way it disagreed (judge reason_code): say which way, so the tick is not a formality (paralegal review T-181 minor). */
  const AMOUNT_WAY = { SHOULD_BE_CHARGE: "a billed charge", SHOULD_BE_RATE: "a rate", SHOULD_BE_ESTIMATE: "an estimate", SHOULD_BE_DAMAGES: "a damages figure (for example lost wages)" };
  R.disputeText = function (v, item) {
    const code = item && item.ladder && item.ladder.judge && item.ladder.judge.reason_code;
    if (v === "disagrees" && AMOUNT_WAY[code]) return `A second AI check thought this may be ${AMOUNT_WAY[code]}, not what it was first sorted as.`;
    if (v === "disagrees" && (code === "SHOULD_BE_UNCLEAR" || code === "TEXT_AMBIGUOUS")) return "A second AI check could not read this figure with confidence.";
    return DISPUTE[v];
  };

  /* ---------- T-211 (D-074): "How this was checked" on every item: three rows in plain words, from the item's own check trace (GET .../items/<id>/trace; metadata only, no prompts).
     1 Code check   what code verified (the passed steps with kind "code"), or what did not pass.
     2 Second AI check   a different model with a different prompt: verdict (agrees / disputes / could not check) and the fixed one-line reason the server wrote for its reason code.
                         A prepared demo answer (D-065) says so first: the team prepared it, then the second AI check read it against the quote.
     3 You   her decision, or "Waiting for you".
     The code and AI rows come from the trace (fetched once per item version); the You row is drawn at once from the item. A trace that cannot be read says so in the row, never a guess. ---------- */
  const CODE_PHRASE = [          // [trace step id, what passing it means], in the order they are said; two are shown
    ["excerpt_verbatim", "the highlighted words are in the record word for word"], ["summary_tokens", "the line's numbers and dates are in them"],
    ["found_in_text", "the amount appears in the record"], ["amount_class", "a rule sorted what kind of figure it is"],
    ["computed", "the dates and the number of days were worked out by code"], ["spans_match", "the words it points to are in the record"],
    ["record_warning_check", "the wording was found in the record by code"], ["date_confirmed", "the date comes from the record"],
  ];
  const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1);
  const isCodeStep = (x) => x.kind === "code" && (x.status === "pass" || x.status === "fail");
  R.howCode = function (tr) {
    const codes = ((tr && tr.steps) || []).filter(isCodeStep), bad = codes.filter((x) => x.status === "fail");
    if (!codes.length) return { state: "none", chip: "Code: none", text: "No code check applies to this item.", list: [] };
    const list = codes.map((x) => ({ ok: x.status === "pass", label: R.plain(x.label) }));
    if (bad.length) return { state: "bad", chip: "Code: not passed", text: "Did not pass: " + R.plain(bad[0].why || bad[0].label) + (bad.length > 1 ? ` (and ${bad.length - 1} more)` : ""), list };
    const ok = new Set(codes.map((x) => x.id)), say = CODE_PHRASE.filter(([id]) => ok.has(id)).slice(0, 2).map(([, t]) => t);
    return { state: "ok", chip: "Code: passed", text: "Passed: " + (say.length ? say.join(", and ") : `${codes.length} check${codes.length === 1 ? "" : "s"} by code`) + ".", list };
  };
  const VERDICT = { supported: ["Agrees", "ok", "AI: agrees"], agree: ["Agrees", "ok", "AI: agrees"], agrees: ["Agrees", "ok", "AI: agrees"],
    partially: ["Disputes", "bad", "AI: disputes"], unsupported: ["Disputes", "bad", "AI: disputes"], disagrees: ["Disputes", "bad", "AI: disputes"], disagree: ["Disputes", "bad", "AI: disputes"],
    unsure: ["Could not check", "warn", "AI: could not check"], unavailable: ["Could not check", "warn", "AI: could not check"] };
  /* One statement from the judge step's real state (T-211 r2). The "prepared by our team; the second AI then checked it" lead is said only when the second AI really returned a verdict;
     a step that was skipped says "Not run" when its reason starts "Not run" (the phrase list found it, so there is nothing to double-check) and "Not needed" when code made the item. */
  R.howJudge = function (tr, item) {
    const steps = (tr && tr.steps) || [], st = steps.find((x) => x.kind === "llm" && x.evidence && x.evidence.model && x.evidence.model.role === "judge") || steps.find((x) => /^judge/.test(x.id));
    const prep = !!(item && item.prepared), LEAD = "Prepared by our team; the second AI check then checked it against the quote.";
    if (!st) return { state: "none", word: "Not run", chip: "AI: not run", lead: "", text: "No second AI check applies to this item.", model: "" };
    const ev = st.evidence || {}, m = ev.model && ev.model.id && !ev.model.prepared ? ev.model.id + (ev.prompt_version ? ` · prompt ${ev.prompt_version}` : "") : "";
    const text = cap(R.plain(ev.rationale || st.why || "").replace(/^A second AI check (?:also )?/, ""));          // the row is already headed "Second AI check"
    if (st.status === "skipped" && !ev.judge_verdict) {
      if (/^not run\b/i.test(text)) return { state: "none", word: "Not run", chip: "AI: not run", lead: "", text: cap(text.replace(/^Not run:? ?/i, "")), model: "" };
      return { state: "none", word: "Not needed", chip: "AI: not needed", lead: "", text: cap(text.replace(/^Not needed: /, "")), model: "" };
    }
    if (st.status === "pending") return { state: "warn", word: "Not run yet", chip: "AI: not run yet", lead: "", text, model: m };
    const v = VERDICT[ev.judge_verdict] || (st.status === "fail" ? VERDICT.disagrees : VERDICT.supported);
    return { state: v[1], word: v[0], chip: v[2], lead: prep ? LEAD : "", text, model: m };
  };
  R.howYou = function (S, item) {
    const t = S.cfg.youText && S.cfg.youText(S, item);
    if (t) return { state: "ok", chip: "You: decided", text: t };
    return { state: "wait", chip: "You: waiting", text: item.edit_to_check ? "You changed the wording. Waiting for you to compare it with the highlighted words." : "Waiting for you." };
  };
  const TRACES = new Map();      // token|item|version -> Promise<trace>. A write changes the version, so the next look asks again. A failed read is forgotten.
  R.traceOf = function (S, item) {
    const key = S.token + "|" + item.id + "|" + item.version;
    if (!TRACES.has(key)) TRACES.set(key, G.api.itemTrace(S.token, item.id).catch((e) => { TRACES.delete(key); throw e; }));
    return TRACES.get(key);
  };
  R.howOpen = null;      // null until she toggles the panel; then it stays as she left it for the rest of the visit

  /* ---------- the record, with the highlighted words marked, or its sentences tappable ---------- */
  R.recBlock = function (rec, opt) {
    opt = opt || {};
    let text = rec.text || "", base = rec.char_start || 0;
    const pre = /^[\s\S]*?\nExcerpt: ?/.exec(text);
    let preEnd = pre ? pre[0].length : 0;
    const full = text.length, win = opt.win && opt.win[0] > 0 || opt.win && opt.win[1] < full ? opt.win : null;       // opt.win = [from, to] in the record's own offsets: show only that part (several records in one warning)
    if (win) { text = text.slice(win[0], win[1]); base += win[0]; preEnd = Math.max(0, preEnd - win[0]); }
    const n = text.length;
    const marks = (opt.marks || []).map(([a, b]) => [Math.max(0, a - base), Math.min(n, b - base)]).filter(([a, b]) => b > a).sort((x, y) => x[0] - y[0]);
    const cuts = new Set([0, n, preEnd]);
    marks.forEach(([a, b]) => { cuts.add(a); cuts.add(b); });
    const sents = (opt.sentences || []).map((s) => ({ ...s, a: s.start - base, b: s.end - base }));
    sents.forEach((s) => { cuts.add(s.a); cuts.add(s.b); });
    const pts = [...cuts].filter((x) => x >= 0 && x <= n).sort((x, y) => x - y), body = [];
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1], piece = text.slice(a, b); if (!piece) continue;
      const sent = sents.find((s) => a >= s.a && b <= s.b), marked = marks.some(([x, y]) => a >= x && b <= y);
      if (sent) {
        if (!sent.__el) {
          const el = h("span", { class: "sent" + (opt.picked && opt.picked.has(sent.start) ? " on" : ""), role: "button", tabindex: "0", "aria-pressed": opt.picked && opt.picked.has(sent.start) ? "true" : "false",
            "data-testid": "sentence", "data-start": sent.start, onclick: () => opt.onPick(sent), onkeydown: (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); opt.onPick(sent); } } });
          sent.__el = el; body.push(el);
        }
        sent.__el.append(document.createTextNode(piece));
      } else {
        const el = h(marked ? "mark" : "span", { class: a < preEnd ? "meta" : null }, piece);
        body.push(el);
      }
    }
    if (win && win[0] > 0) body.unshift(h("span", { class: "ell" }, "… "));
    if (win && win[1] < full) body.push(h("span", { class: "ell" }, " …"));
    const out = [];
    if (opt.head) out.push(h("div", { class: "rec-h" }, opt.head));
    out.push(h("div", { class: "rec", "data-testid": "record-text", "data-record": rec.id }, body));
    return out;
  };

  /* ---------- the engine ---------- */
  const undecided = (i) => !!i && G.steps.undecided(i);
  R.run = async function (ctx, cfg) {
    const token = ctx.token, body = document.body;
    const S = { ctx, cfg, token, c: ctx.case, queue: [], idx: -1, ui: {}, busy: false, alive: true, said: null, err: null, screen: null, forceCompare: new Map(), part2: new Set(), el: {} };
    const q$ = (id) => S.queue.find((q) => q.id === id);
    S.item = (id) => cfg.find(S.c, id);
    S.counted = () => S.queue.filter((q) => !q.optional && S.item(q.id));
    S.left = () => S.counted().filter((q) => undecided(S.item(q.id)));
    S.numberOf = (id) => { const i = S.counted().findIndex((q) => q.id === id); return i < 0 ? null : i + 1; };
    S.record = (rid) => (S.c.records || []).find((r) => r.id === rid);
    S.recOf = (pos) => (S.c.records || []).find((r) => pos >= r.char_start && pos < r.char_end);

    function say(text, undo) { S.said = text ? { text, undo } : null; drawStatus(); }
    S.say = say;
    S.fail = async function (e) {
      if (e && e.name === "AbortError") return;
      if (e instanceof G.ApiError && e.status === 409 && e.code === "stale_item") {
        let now = "";
        try { await S.reload(); const it = S.cur(); now = it && it.review_status === "dismissed" ? " It is now left out." : it && (it.review_status === "accepted" || it.review_status === "edited") ? " It is now kept." : ""; } catch (_) { /* the message below is enough */ }
        S.err = { text: `This item changed in another tab. We've loaded the latest.${now} Choose again if that is wrong.` };
      } else if (e instanceof G.ApiError && e.code === "COMPARE_REQUIRED") {
        const it = S.cur(); if (it) S.forceCompare.set(it.id, (e.detail && e.detail.verdict) || "disagrees");       // the page did not know: show the compare box (the server's reason is in it), never a raw error
        S.err = null;
      } else if (e instanceof G.ApiError && e.code === "invalid_edit" && e.detail && Array.isArray(e.detail.qualifiers) && R.droppedText(e.detail.qualifiers, S.lastEdit && S.lastEdit.excerpt, S.lastEdit && S.lastEdit.summary, S.lastEdit && S.lastEdit.before)) {
        S.err = { text: R.droppedText(e.detail.qualifiers, S.lastEdit.excerpt, S.lastEdit.summary, S.lastEdit.before) };
      } else if (e instanceof G.ApiError && e.status === 409 && e.code === "item_rejected") {
        S.err = { text: "We couldn't check this one, so it can't be answered here. We've loaded the latest." };
        try { await S.reload(); } catch (_) { /* keep the message */ }
      } else if (e instanceof G.ApiError && e.code === "CONFIRM_REQUIRED" && e.detail && e.detail.message) {
        S.err = { text: R.plain(e.detail.message) };
      } else S.err = { text: R.plain(e && e.message ? e.message : "Something went wrong. Try again.") };
      render(true);
    };
    S.cur = () => (S.idx >= 0 && S.queue[S.idx] ? S.item(S.queue[S.idx].id) : null);
    S.reload = async function () { S.c = await ctx.refresh(); updateTitlebar(); };
    S.act = async function (fn) {
      if (S.busy || !S.alive) return undefined;
      S.busy = true; S.err = null; syncButtons();
      try { return await fn(); } catch (e) { await S.fail(e); return undefined; } finally {
        S.busy = false;
        if (S.alive) { syncButtons(); drawStatus(); if (!S.ended && S.screen && (!document.activeElement || document.activeElement === document.body)) focusFirst(S.screen); }     // the click disabled the button that had focus: put it on the next item's first answer
      }
    };
    /* every review POST carries version + expected_status of the item on screen (T-178) */
    S.post = (item, action, extra) => G.api.review(token, item.id, { action, version: item.version, expected_status: item.review_status, ...(extra || {}) });
    S.go = (item) => { const i = S.queue.findIndex((q) => q.id === item.id); S.open(i < 0 ? S.idx : i); };

    /* ---- frame ---- */
    const E = S.el;
    E.eyebrow = h("div", { class: "eyebrow" }, `Step ${cfg.step} of 4`);
    E.toggle = h("button", { type: "button", class: "steps-toggle", "data-testid": "btn-steps", "aria-expanded": "false", "aria-controls": "step-list", onclick: () => toggleSteps() }, `Step ${cfg.step} of 4`, h("span", { "aria-hidden": "true" }, " ▾"));
    E.ai = h("div", { class: "t-ai", "data-testid": "ai-note" }, R.aiNote());
    E.count = h("span", { class: "num", "data-testid": "item-count" });
    E.prog = h("span", { class: "of num", "data-testid": "progress-text" });
    E.fill = h("i");
    E.bar = h("div", { class: "bar", role: "progressbar", "aria-label": "Progress in this step", "aria-valuemin": "0", "aria-valuemax": "100" }, E.fill);
    E.total = h("div", { class: "tc-v num", "data-testid": "total-value" }, "$0.00");
    E.titlebar = h("div", { class: "titlebar", "data-testid": "titlebar" },
      h("div", { class: "t-main" }, E.eyebrow, E.toggle, h("h1", { "data-testid": "page-title" }, cfg.title), E.ai),
      cfg.chip ? h("div", { class: "total-chip", "aria-live": "polite", "data-testid": "total-chip" }, h("div", { class: "tc-l" }, "Bill total so far"), E.total) : null,
      h("div", { class: "count-box", "data-testid": "count-box" }, h("div", { class: "count-line" }, E.count, E.prog), E.bar));
    E.srcHead = h("span", { class: "ch-sub", "data-testid": "src-head" });
    E.srcBody = h("div", { class: "card-b", "data-testid": "card-source", tabindex: "0", "aria-label": "The record" });
    E.lineHead = h("div", { class: "card-h", "data-testid": "line-head" });
    E.lineBody = h("div", { class: "card-b", "data-testid": "line-body" });
    E.foot = h("div", { class: "card-f plain", "data-testid": "card-foot", tabindex: "-1" });
    E.lineCard = h("section", { class: "card card-line", "aria-label": "To check", "data-testid": "card-line" }, E.lineHead, E.lineBody, E.foot);
    E.srcCard = h("section", { class: "card card-src", "aria-label": "From the record", "data-testid": "card-src" }, h("div", { class: "card-h" }, h("span", { class: "ch-title" }, "From the record"), E.srcHead), E.srcBody);
    E.work = h("main", { class: "work", id: "main", "data-testid": "work" }, E.srcCard, E.lineCard);
    /* T-211: "How this was checked" sits under the quote in the record card on a wide screen (it never takes room from the line), and on a phone as a one-line strip directly above the action bar (always in view; opened, its rows float above the bar and do not move anything) */
    E.how = h("details", { class: "how", "data-testid": "how-checked", hidden: true });
    const narrowMQ = matchMedia("(max-width: 760px)"), shortMQ = matchMedia("(max-width: 760px) and (max-height: 720px)");
    // T-216: a short phone (375x667) has no room for the strip in the bar: it follows the line card in the scrolling page instead
    const placeHow = () => { const to = shortMQ.matches ? E.work : narrowMQ.matches && E.actions ? E.actions : E.srcCard; if (to === E.actions) { if (E.how.parentNode !== E.actions || E.actions.firstChild !== E.how) E.actions.prepend(E.how); } else if (E.how.parentNode !== to || E.how !== to.lastChild) to.append(E.how); };
    narrowMQ.addEventListener("change", placeHow); shortMQ.addEventListener("change", placeHow);
    const btn = (cls, tid, key) => h("button", { type: "button", class: "btn " + cls, "data-testid": tid, "aria-keyshortcuts": key || null });
    E.question = h("p", { class: "question", id: "q", "data-testid": "question" });
    E.yes = btn("answer primary", "answer-yes", "a"); E.no = btn("answer", "answer-no", "d");
    E.yes.setAttribute("data-autofocus", "");
    E.back = btn("quiet", "btn-back", "ArrowLeft"); E.third = btn("quiet", "btn-third", "e"); E.later = btn("quiet", "btn-later", "ArrowRight");
    E.statusText = h("span", { class: "st-msg", "data-testid": "status-text" }); E.undo = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-undo", hidden: true }, "Undo");
    E.showBox = h("button", { type: "button", class: "btn quiet undo", "data-testid": "btn-show-box", hidden: true }, "Show box");
    E.status = h("p", { class: "status", role: "status", "aria-live": "polite", "data-testid": "status-slot" }, E.statusText, E.undo, E.showBox);
    E.actions = h("div", { class: "actions", "data-testid": "actions" }, h("div", { class: "actions-in" }, E.question,
      h("div", { class: "big", role: "group", "aria-labelledby": "q" }, E.yes, E.no), h("div", { class: "small" }, E.back, E.third, E.later), E.status));
    E.back.textContent = "‹ Back"; E.later.textContent = "Decide later";
    E.back.onclick = () => back();
    E.later.onclick = () => { const l = S.screen && S.screen.later; if (l === false) return; if (l && l.run) l.run(); else S.skip(); };
    placeHow();
    ctx.view.replaceChildren(E.titlebar, E.work, E.actions);
    ctx.layout("frame");

    function toggleSteps(force) {
      const open = force != null ? force : !body.classList.contains("steps-open");
      body.classList.toggle("steps-open", open); E.toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    const onDocClick = (e) => { if (body.classList.contains("steps-open") && !e.target.closest("#step-bar") && !e.target.closest("[data-testid=btn-steps]")) toggleSteps(false); };

    function drawStatus() {
      const s = S.said;
      const box = E.yes && E.yes.disabled && !S.busy && E.foot.querySelector("input[type=checkbox]:not(:checked)");      // Yes is greyed because a box is not ticked: say so beside it (on a 375x667 phone the box can sit below the bar)
      const tick = box ? (box.dataset.testid === "check-compare" ? "Tick the box to say you compared them." : "Tick the box first.") : "";      // no direction word: the box can be above the bar or below the screen
      const saved = s && !s.undo && /^Saved/.test(s.text);      // a "Saved" note must not hide the reason Yes is greyed: both stay until she ticks
      const why = box && (!s || saved);
      E.statusText.textContent = why ? (saved ? "Saved. " : "") + tick : s ? s.text : (matchMedia("(min-width: 761px)").matches ? `Keys: A says yes, D says no, ${S.screen && S.screen.third ? "E fixes or adds a note, " : ""}the arrow keys move between items.` : "");
      E.status.classList.toggle("hint", !s && !why);
      E.status.dataset.why = why ? "tick" : "";
      E.undo.hidden = !(s && s.undo);
      E.undo.onclick = s && s.undo ? () => S.act(s.undo) : null;
      const hidden = !!why && boxHidden(box);      // the box is under the bar or below the screen: one tap brings it into view
      E.showBox.hidden = !hidden;
      E.showBox.onclick = hidden ? () => revealBox(box) : null;
    }
    function boxHidden(box) {
      const r = box.getBoundingClientRect(), bar = E.actions.getBoundingClientRect();
      return r.bottom > bar.top - 4 || r.top < 0;
    }
    function revealBox(box) {
      const bar = E.actions.getBoundingClientRect();
      box.style.scrollMarginBottom = Math.ceil(window.innerHeight - bar.top + 12) + "px";
      try { box.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* nothing to scroll */ }
      box.focus({ preventScroll: true }); drawStatus();
    }

    function updateTitlebar() {
      const items = S.counted(), left = S.left().length, total = items.length, done = total - left;
      const q = S.queue[S.idx], n = q && !q.optional ? S.numberOf(q.id) : null;
      E.count.textContent = S.screen && S.screen.counter ? S.screen.counter : n ? `${cfg.unit} ${n} of ${total}` : q && q.optional ? "Optional" : `${total} ${cfg.unit.toLowerCase()}s`;
      E.prog.textContent = `${done} answered · ${left} to go`;
      const pct = total ? Math.round((done / total) * 100) : 100;
      E.fill.style.width = pct + "%"; E.bar.setAttribute("aria-valuenow", String(pct));
      if (cfg.chip) E.total.textContent = R.money(((S.c.totals || {}).accepted || {}).cents || 0);
    }

    /* ---- render one screen ---- */
    function fillTag(tag, extra) { return tag ? h("span", { class: "tag " + tag.cls, title: tag.title || null, "data-testid": extra || "line-tag" }, tag.text) : null; }
    function syncButtons() {
      const sc = S.screen; if (!sc) return;
      const set = (el, def) => {                                    // an absent answer keeps its place (invisible), so nothing else moves
        if (!def) { el.style.visibility = "hidden"; el.disabled = true; el.setAttribute("aria-hidden", "true"); el.tabIndex = -1; return; }
        el.disabled = S.busy || (typeof def.disabled === "function" ? def.disabled() : !!def.disabled);
        el.style.visibility = ""; el.removeAttribute("aria-hidden"); el.removeAttribute("tabindex");
      };
      set(E.yes, sc.yes); set(E.no, sc.no); set(E.third, sc.third);
      E.back.disabled = S.busy || sc.back === false; E.later.disabled = S.busy;
      E.later.style.visibility = sc.later === false ? "hidden" : ""; E.later.tabIndex = sc.later === false ? -1 : 0;
      E.third.classList.toggle("hint", !!(sc.third && sc.third.hint));
      E.undo.disabled = S.busy;
    }
    function drawBtn(el, def, keep) {
      if (!def) { el.replaceChildren(keep || ""); el.classList.remove("two"); el.onclick = null; return; }
      el.replaceChildren(...[def.label, def.sub ? h("span", { class: "sub" }, def.sub) : null].filter(Boolean));
      el.classList.toggle("two", !!def.sub); el.onclick = () => def.run();
      if (el === E.yes) el.classList.toggle("primary", !def.plain);
    }
    function render(keepScroll) {
      const item = S.cur(), q = S.queue[S.idx];
      if (!item) return finish();
      const sc = (S.screen = cfg.present(S, item, q));
      E.lineCard.dataset.itemId = item.id; E.lineCard.dataset.kind = item.kind || ""; E.lineCard.dataset.mode = S.ui.mode || "view";
      const head = [fillTag(sc.tag), fillTag(sc.tag2, "line-tag2"), sc.sub ? h("span", { class: "ch-sub", "data-testid": "line-sub" }, sc.sub) : null];
      E.lineHead.replaceChildren(...head.filter(Boolean));
      const bodyScroll = E.lineBody.scrollTop;
      E.lineBody.replaceChildren(...[].concat(sc.body || []).filter(Boolean));
      E.lineBody.scrollTop = keepScroll ? bodyScroll : 0;
      if (!keepScroll) E.lineCard.scrollTop = 0;
      const err = S.err ? { cls: "bad", nodes: [h("strong", {}, "Not saved. "), S.err.text] } : null;
      const foot = err || sc.foot || { cls: "plain", nodes: [] };
      E.foot.className = "card-f " + (foot.cls || "plain"); E.foot.replaceChildren(...[].concat(foot.nodes || []).filter(Boolean));
      if (err) E.foot.setAttribute("role", "alert"); else E.foot.removeAttribute("role");
      E.question.textContent = sc.question || "";
      drawHow(item, sc);
      drawBtn(E.yes, sc.yes, "Yes"); drawBtn(E.no, sc.no, "No"); drawBtn(E.third, sc.third, "Fix the wording");
      E.later.textContent = sc.later && sc.later.label ? sc.later.label : "Decide later";
      // a phone: when any item of this step needs a tick box the line card gets the room for the whole visit (so nothing moves between items), and the line and its box are on screen together
      S.sticky = S.sticky || S.queue.some((q) => { const it = S.item(q.id); return !!it && (!!R.dispute(it) || !!it.edit_to_check || (it.countable && it.kind !== "charge") || (it.flag && it.confirm_required)); }) || !!E.foot.querySelector("input[type=checkbox]");
      E.work.classList.toggle("needs-check", !!S.sticky);      // before the record is drawn: the window is its final size when the highlight is scrolled into it
      renderSource(false);
      fitHow();
      updateTitlebar(); syncButtons(); drawStatus();
      if (err) showRefusal();
      if (!keepScroll) focusFirst(sc);
    }
    /* ---- T-211: the three rows ---- */
    let howTicket = 0;
    function drawHow(item, sc) {
      const mine = ++howTicket;
      if (sc.how === false) { E.how.hidden = true; E.how.replaceChildren(); return; }
      E.how.hidden = false;
      const you = R.howYou(S, item);
      const row = (key, label, sub) => { const v = h("div", { class: "how-v", "data-testid": "how-" + key + "-text" }, "Checking…"), s = sub ? h("span", { class: "how-sub", "data-testid": "how-" + key + "-sub" }, sub) : null, r = h("div", { class: "how-r", "data-testid": "how-" + key }, h("div", { class: "how-l" }, h("b", {}, label), s), v); return [r, v, s]; };
      const [rCode, vCode] = row("code", "Code check", "no AI"), [rAi, vAi, sAi] = row("ai", "Second AI check", "own model and prompt"), [rYou, vYou] = row("you", "You");
      vYou.textContent = you.text; rYou.dataset.state = you.state;
      const chip = (key, text, state) => h("span", { class: "hchip " + (state || ""), "data-testid": "how-chip-" + key }, text);
      const cCode = chip("code", "Code: …"), cAi = chip("ai", "AI: …"), cYou = chip("you", you.chip, you.state);
      const sum = h("summary", { "data-testid": "how-summary" }, h("span", { class: "how-t" }, h("span", { class: "long" }, "How this was checked"), h("span", { class: "short", "aria-hidden": "true" }, "Checks")), h("span", { class: "how-chips" }, cCode, cAi, cYou));
      E.how.replaceChildren(sum, h("div", { class: "how-rows" }, rCode, rAi, rYou));
      E.how.dataset.item = item.id; E.how.setAttribute("aria-busy", "true");
      const want = R.howOpen == null ? !narrowMQ.matches && window.innerHeight >= 840 : R.howOpen;
      if (want !== E.how.open) { E.how._auto = true; E.how.open = want; }          // a change the page made is not her choice (the toggle event says which)          // closed (chips only) on a phone and on a short window until she opens it
      E.how.ontoggle = () => { if (E.how._auto) { E.how._auto = false; return; } R.howOpen = E.how.open; };
      R.traceOf(S, item).then((tr) => {
        if (mine !== howTicket || !S.alive) return;
        const c = R.howCode(tr), j = R.howJudge(tr, item);
        rCode.dataset.state = c.state; cCode.textContent = c.chip; cCode.className = "hchip " + c.state;
        const ul = h("ul", { class: "how-all", "data-testid": "how-all-list", hidden: true }, c.list.map((x) => h("li", { class: x.ok ? "ok" : "bad" }, h("span", { "aria-hidden": "true" }, x.ok ? "✓ " : "✗ "), h("span", { class: "sr" }, x.ok ? "Passed: " : "Did not pass: "), x.label)));
        const more = c.list.length ? h("button", { type: "button", class: "how-more", "data-testid": "how-all-checks", "aria-expanded": "false", onclick: () => { ul.hidden = !ul.hidden; more.setAttribute("aria-expanded", ul.hidden ? "false" : "true"); } }, `All ${c.list.length} check${c.list.length === 1 ? "" : "s"}`) : null;
        vCode.replaceChildren(...[c.text, " ", more, ul, !item.prepared && item.origin_label ? h("p", { class: "how-lead", "data-testid": "how-origin" }, item.origin_label + ".") : null].filter(Boolean));      // T-214: said once here and on the tag; the same words
        rAi.dataset.state = j.state; cAi.textContent = j.chip; cAi.className = "hchip " + j.state;
        vAi.replaceChildren(...[j.lead ? h("p", { class: "how-lead", "data-testid": "how-prepared" }, j.lead) : null, h("p", {}, h("b", { class: "how-verdict " + j.state, "data-testid": "how-verdict" }, j.word), j.text ? ". " + j.text : ""),
          ].filter(Boolean));
        if (j.model) { sAi.textContent = j.model.split(" · ")[0]; sAi.title = "Model and prompt: " + j.model; sAi.dataset.model = j.model; }
        E.how.removeAttribute("aria-busy");
        fitHow();
      }).catch((e) => {
        if (mine !== howTicket || !S.alive || (e && e.name === "AbortError")) return;
        for (const [v, c, k] of [[vCode, cCode, "Code"], [vAi, cAi, "AI"]]) { v.textContent = "We couldn't load this just now."; c.textContent = k + ": –"; }
        E.how.removeAttribute("aria-busy");
      });
    }
    /* The highlighted words come first: when the open panel would push any of them out of the record window (several records in one warning, a long quote), and she has not chosen to keep it open,
       it folds to its one-line chips. She can open it; her choice then stays for the rest of the visit. */
    function fitHow() {
      if (!E.how.open || R.howOpen != null || E.how.parentNode !== E.srcCard) { if (E.how.open && E.how.parentNode === E.srcCard && S.alignMark) S.alignMark(); return; }
      const box = E.srcBody.getBoundingClientRect(), cut = [...E.srcBody.querySelectorAll("mark")].some((m) => { const r = m.getBoundingClientRect(); return r.bottom > box.bottom + 1; });
      if (cut) { E.how._auto = true; E.how.open = false; if (S.alignMark) S.alignMark(); } else if (S.alignMark) S.alignMark();
    }
    function renderSource(keep) {
      const sc = S.screen; if (!sc || !sc.src) { E.srcHead.textContent = ""; E.srcBody.replaceChildren(); return; }
      const top = E.srcBody.scrollTop;
      E.srcHead.textContent = sc.src.head || ""; E.srcBody.replaceChildren(...sc.src.nodes().filter(Boolean));
      if (keep) E.srcBody.scrollTop = top;
      else alignMark();
    }
    /* the first highlighted word is in the record window: top-aligned with one line of the record above it on a phone (the window is small), a third down on a wide screen. Measured with rects, not offsetTop (the window is not the mark's offset parent). */
    function alignMark() {
      const box = E.srcBody, m = box.querySelector("mark, .sent.on");
      if (!m) { box.scrollTop = 0; return; }
      const narrow = matchMedia("(max-width: 760px)").matches, lead = narrow ? Math.min(30, box.clientHeight / 4) : box.clientHeight / 3;
      const at = m.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
      box.scrollTop = Math.max(0, at - lead);
    }
    S.alignMark = alignMark;
    /* a refused save: its words sit in the line card's foot, which on a phone can be below the visible part of the card (the card scrolls as one box) or under the action bar. Bring it into view, never under the bar. */
    function showRefusal() {
      const card = E.lineCard, f = E.foot;
      if (card.scrollHeight > card.clientHeight + 1) {
        const c = card.getBoundingClientRect(), r = f.getBoundingClientRect();
        if (r.bottom > c.bottom) card.scrollTop += r.bottom - c.bottom + 2;
      }
      try { f.scrollIntoView({ block: "nearest", inline: "nearest" }); } catch (_) { /* the card scroll above is enough */ }
    }
    S.renderSource = () => renderSource(true);
    S.render = (keep) => render(!!keep);
    S.sync = () => { syncButtons(); if (!S.said || (!S.said.undo && /^Saved/.test(S.said.text))) drawStatus(); };
    function focusFirst(sc) {
      const f = sc.focus === "field" ? E.lineBody.querySelector("textarea, input") : null;
      const target = f || (!E.yes.disabled ? E.yes : E.foot.querySelector("input[type=checkbox]") || (sc.yes && !S.busy ? E.foot : (!E.no.disabled ? E.no : null)));      // a refused Yes with no tick box: focus the reason, never a button that would answer
      if (target && document.activeElement !== target && !S.firstPaint) target.focus({ preventScroll: true });
    }

    /* ---- moving ---- */
    function writeUrl(id) { try { history.replaceState(history.state, "", id ? G.url.step(token, cfg.step, id) : G.url.step(token, cfg.step)); } catch (_) { /* the screen still works */ } }
    S.open = function (i) {
      if (i < 0 || i >= S.queue.length) return finish();
      S.idx = i; S.ui = {}; S.err = null; S.screen = null;
      writeUrl(S.queue[i].id); render(false);
    };
    function nextUndecided(from) { for (let i = from + 1; i < S.queue.length; i++) { const q = S.queue[i], it = S.item(q.id); if (it && !q.optional && undecided(it)) return i; } return -1; }
    S.next = function () { const i = nextUndecided(S.idx); if (i < 0) return finish(); S.open(i); };
    S.skip = function () {                                         // Decide later and the right arrow: the next item in the list, decided or not
      let i = S.idx + 1; while (i < S.queue.length && !S.item(S.queue[i].id)) i++;
      if (i >= S.queue.length) return finish(); S.open(i);
    };
    function back() {
      let i = S.idx - 1; while (i >= 0 && !S.item(S.queue[i].id)) i--;
      if (i < 0) { ctx.go(cfg.step === 2 ? G.url.records(token) : G.url.timeline(token)); return; }
      S.open(i);
    }
    S.firstUndecided = () => nextUndecided(-1);
    function finish() {
      writeUrl(null);
      const node = S.counted().length ? cfg.done(S) : cfg.empty(S);
      ctx.layout("page"); ctx.view.replaceChildren(node); window.scrollTo(0, 0);
      S.ended = true; document.title = cfg.title + " – Treatment Timeline"; const hh = G.$("h1", ctx.view); if (hh) { hh.tabIndex = -1; hh.focus({ preventScroll: true }); }
    }

    /* ---- the common write: POST, refresh, say what was saved, move on ---- */
    S.decide = async function (item, action, extra, opt) {
      opt = opt || {};
      return S.act(async () => {
        const resp = await S.post(item, action, extra);
        S.c = await ctx.refresh();
        const fresh = S.item(item.id) || resp.item, num = S.numberOf(item.id);
        const label = (num ? `${cfg.unit.toLowerCase()} ${num}` : "this item"), said = cfg.statusFor ? cfg.statusFor(S, fresh, resp, action, extra) : "saved";
        const undo = async () => {
          const cur = S.item(item.id) || fresh;
          await S.post(cur, "reset"); S.c = await ctx.refresh(); S.ui = {}; S.go(cur); say(`Undone: ${label} is back to not decided.`, null); render(false);
        };
        if (cfg.onResponse) cfg.onResponse(S, resp);
        updateTitlebar();
        if (opt.stay) { say(`Saved: ${label} ${said}.`, undo); render(false); return resp; }
        say(`Saved: ${label} ${said}.`, undo);
        S.next();
        return resp;
      });
    };

    /* ---- keyboard: A / D / E and the arrows (not while typing; not with a modifier) ---- */
    const onKey = (e) => {
      if (S.ended || e.ctrlKey || e.metaKey || e.altKey || e.defaultPrevented) return;
      const t = e.target, tag = t && t.tagName;
      if (tag === "TEXTAREA" || tag === "INPUT" && t.type !== "checkbox" || tag === "SELECT" || (t && t.isContentEditable)) return;
      const k = e.key.length === 1 ? e.key.toLowerCase() : e.key;
      const press = (el, def) => {
        if (!def) return; e.preventDefault();
        if (el.disabled) {
          const c = E.foot.querySelector("input[type=checkbox]:not(:checked)");
          if (c) c.focus();
          else if (!S.busy) say(`“${el.textContent}” is not available here.${def.why ? " " + def.why : ""}`, null);        // focus stays where it was: the next Space or Enter must never answer for her
          return;
        }
        el.click();
      };
      if (k === "a") press(E.yes, S.screen && S.screen.yes);
      else if (k === "d") press(E.no, S.screen && S.screen.no);
      else if (k === "e") press(E.third, S.screen && S.screen.third);
      else if (k === "ArrowRight") { if (!E.later.disabled && S.screen && S.screen.later !== false) { e.preventDefault(); E.later.click(); } }
      else if (k === "ArrowLeft") { if (!E.back.disabled) { e.preventDefault(); E.back.click(); } }
      else if (k === "Escape" && body.classList.contains("steps-open")) toggleSteps(false);
    };
    document.addEventListener("keydown", onKey); document.addEventListener("click", onDocClick);

    /* ---- start ---- */
    S.queue = cfg.buildQueue(S.c);
    S.firstPaint = true;
    updateTitlebar();
    const want = ctx.query.get("item"), wi = want ? S.queue.findIndex((q) => q.id === want && S.item(q.id)) : -1;
    if (wi >= 0) S.open(wi);
    else { const f = S.firstUndecided(); if (f >= 0) S.open(f); else finish(); }
    S.firstPaint = false;
    return function cleanup() { narrowMQ.removeEventListener("change", placeHow); S.alive = false; document.removeEventListener("keydown", onKey); document.removeEventListener("click", onDocClick); body.classList.remove("steps-open"); };
  };

  /* ---------- pieces the step modules share ---------- */
  R.check = function (S, key, label, opt) {
    const box = h("input", { type: "checkbox", "data-testid": "check-" + key, "data-autofocus": opt && opt.focus ? "" : null });
    box.checked = !!S.ui["chk_" + key];
    box.addEventListener("change", () => { S.ui["chk_" + key] = box.checked; S.sync(); });
    return h("label", { class: "check" }, box, h("span", {}, label));
  };
  R.ticked = (S, key) => !!S.ui["chk_" + key];

  /* An answers row for a done screen: number, date, label, chip, Change. */
  R.answerRow = function (n, date, label, chip, chipCls, href) {
    return h("li", { "data-testid": "answer-row" }, h("span", { class: "n" }, String(n)), h("span", { class: "d" }, date), h("span", { class: "lbl", title: label }, label),
      h("span", { class: "ans" }, h("span", { class: "tag " + chipCls, "data-testid": "answer-chip" }, chip)), h("a", { class: "btn", href, "data-testid": "btn-change" }, "Change"));
  };
  R.doneFrame = function (step, title, ...kids) {
    return h("main", { class: "wrap", id: "main", "data-testid": "done-page" }, h("div", { class: "page-h" }, h("div", { class: "ph-main" }, h("div", { class: "eyebrow" }, `Step ${step} of 4`), h("h1", { "data-testid": "page-title" }, title))), ...kids);
  };
})();
