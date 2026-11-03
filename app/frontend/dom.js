/* Shared DOM helpers (frontend-1 / T-042; also used by T-043). Data is only ever written with textContent / text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  // el("button", {class:"x", type:"button", onclick:fn, "data-testid":"y"}, "label", childNode, ...)
  ZL.el = function (tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat(Infinity)) {   // any nesting of arrays: a list of [dt, dd] pairs must never print as [object HTMLElement]
      if (c == null || c === false) continue;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return e;
  };
  // Rank "needs review first" by the state an item had when this case was first shown, so rows do not jump when a decision changes the state
  // (keeps the row under the cursor still and nth-button order stable).
  const ranks = {};
  ZL.firstRank = (id, state) => { const k = (ZL.state && ZL.state.get().token) + ":" + id; if (!(k in ranks)) ranks[k] = state === "needs_review" ? 0 : 1; return ranks[k]; };
  ZL.clear = (n) => { while (n.firstChild) n.removeChild(n.firstChild); return n; };
  ZL.$ = (s, r) => (r || document).querySelector(s);
  ZL.fmtDate = (iso) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return iso || "undated";
    const mon = ["January","February","March","April","May","June","July","August","September","October","November","December"][+m[2] - 1];
    return `${mon} ${+m[3]}, ${m[1]}`;
  };
  // Library cases arrive named after their file ("case lib09 spanish interpreter espalda"). Show a plain title instead; any other name (a pasted case, a sample) is left alone.
  // Display only: the case id and the stored name never change.
  const LIB_TITLE = { 1: "ER visit, then a treatment gap", 2: "Slip and fall, prior knee surgery", 3: "Truck rear-end, chiropractic plan", 4: "Dog bite, scar revision", 5: "Pedestrian struck, hardware (ORIF)",
    6: "Letter of protection, billed vs. adjusted", 7: "Parking-lot fall, outside records", 8: "Second crash, MRI after", 9: "Spanish-language records, back pain", 10: "Hospital bill and EOB forms (UB-04, CMS-1500)",
    11: "Prior conditions and charge ledger", 12: "Records review, credibility wording", 13: "Copied-forward notes across providers", 14: "Handwritten chiropractic scans", 15: "Conflicting accounts, narrative letter" };
  ZL.niceName = (name) => {
    const m = /^case[ _]lib(\d+)\b\s*(.*)$/i.exec(String(name || ""));
    if (!m) return name;
    if (LIB_TITLE[+m[1]]) return LIB_TITLE[+m[1]];
    const t = m[2].replace(/_/g, " ").trim();
    return t ? t.charAt(0).toUpperCase() + t.slice(1) : name;
  };
  // ---- T-060 r5: ONE definition of "still waiting on the paralegal", used by the header, the Open-decisions strip, the Timeline chip, the keyboard flow and the export question.
  // An item is undecided when it is pending, or when she reworded it and it is still marked Needs review (the second check did not agree or did not run: her wording is in the
  // letter, but she has not yet compared it with the quote). A dismissed item is decided and is never counted as needing review.
  ZL.undecided = (i) => { const rs = (i && i.review_status) || "pending"; return rs === "pending" || ZL.editToCheck(i); };
  ZL.needsReview = (i) => !!i && i.state === "needs_review" && ZL.undecided(i);
  ZL.editToCheck = (i) => !!i && i.edit_to_check === true;   // T-136: the server's own flag (T-134): reworded summary OR quote, still Needs review, not yet accepted by her
  // How many edits are waiting for her comparison: the review's own count when the server sent it, else a count of the items that say so (the mock API).
  ZL.editCount = (c) => { const n = c && c.review && c.review.counts && c.review.counts.edit_to_check; return n != null ? n : [].concat(c.entries || [], c.undated_entries || []).filter(ZL.editToCheck).length; };
  // T-136 r2 (paralegal F-1, F-2). Her own summary wording is exempt from the second AI check (D-045b); a re-picked quote on an AI draft is not. When that check never ran on the entry,
  // the export gate (D-044) blocks it as soon as she accepts, until the check runs. One place for the rule, so a server flag can replace it.
  ZL.wordingEdited = (i) => !!i && !!i.edited && i.edited.summary != null;
  // T-136 r3 (T-134 r4): the server's own `second_check_pending` (live, AI-made, no second-check answer, not a rate) is what the page reads. The inference below is only for a server
  // (the mock API) that does not send the field.
  ZL.secondCheckPending = (i) => !!i && (i.second_check_pending !== undefined ? i.second_check_pending === true : i.ai_drafted === true && !ZL.wordingEdited(i) && (i.reasons || []).includes("JUDGE_UNAVAILABLE"));
  // T-179 / D-066: the second check disputed this item (verdict partially | unsupported | disagrees, or a JUDGE_PARTIAL / JUDGE_UNSUPPORTED / JUDGE_DISAGREES reason). Accepting it needs her explicit
  // "I compared it with the quote" (the server answers 422 COMPARE_REQUIRED without it). ZL.judgeDispute returns the verdict word or null; ZL.needsCompare is true while the item is still open.
  const DISPUTE_REASON = { JUDGE_PARTIAL: "partially", JUDGE_UNSUPPORTED: "unsupported", JUDGE_DISAGREES: "disagrees" };
  ZL.judgeDispute = (i) => {
    const j = i && i.ladder && i.ladder.judge, v0 = j && typeof j === "object" ? j.verdict : null, v = v0 === "disagree" ? "disagrees" : v0;
    if (v === "partially" || v === "unsupported" || v === "disagrees") return v;
    const hit = ((i && i.reasons) || []).find((r) => DISPUTE_REASON[r]);
    return hit ? DISPUTE_REASON[hit] : null;
  };
  ZL.needsCompare = (i) => !!i && ((i.review_status || "pending") === "pending") && i.state !== "rejected" && !!ZL.judgeDispute(i);
  ZL.DISPUTE_SENTENCE = { partially: "The second AI check found this only partly supported by the quote.", unsupported: "The second AI check found this not supported by the quote.", disagrees: "The second AI check disagreed with the first result for this item." };
  // She compared the edit with the quote and accepted it: the row says that, not "Needs review" (which would contradict her decision).
  ZL.comparedEdit = (i) => !!i && i.review_status === "accepted" && i.state === "needs_review" && !!i.edited && !ZL.editToCheck(i);
  // A date for a row: <time datetime="2026-01-09">January 9, 2026</time>. The machine date stays in the attribute (tests and assistive tech read it); the person reads the long form.
  ZL.timeEl = (iso, attrs) => ZL.el("time", Object.assign({ datetime: iso }, attrs || {}), ZL.fmtDate(iso));
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
})();
