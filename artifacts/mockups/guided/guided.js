/* Guided UI mockup behaviour (T-180). Static demo only: no network, no backend. Every change swaps text inside boxes that keep their size. */
(function () {
  "use strict";
  var root = document.documentElement;

  // Theme: follow the OS unless the visitor picked one. Remembered when storage works; the page works without it.
  function applyTheme(t) { if (t === "light" || t === "dark") root.setAttribute("data-theme", t); else root.removeAttribute("data-theme"); }
  var saved = null; try { saved = localStorage.getItem("zl.guided.theme"); } catch (e) { saved = null; }
  applyTheme(saved);
  function isDark() { var t = root.getAttribute("data-theme"); return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; }
  function label(btn) { btn.textContent = isDark() ? "Light mode" : "Dark mode"; btn.setAttribute("aria-label", btn.textContent); }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-theme-btn]").forEach(function (b) {
      label(b);
      b.addEventListener("click", function () {
        var t = isDark() ? "light" : "dark"; applyTheme(t);
        try { localStorage.setItem("zl.guided.theme", t); } catch (e) { /* not remembered */ }
        document.querySelectorAll("[data-theme-btn]").forEach(label);
      });
    });

    // A checkbox that unlocks a button (compare confirm, named charge confirms, copy anyway). The button keeps its place and size.
    document.querySelectorAll("[data-unlocks]").forEach(function (box) {
      var ids = box.getAttribute("data-unlocks").split(" ");
      function sync() {
        var group = document.querySelectorAll('[data-unlocks="' + box.getAttribute("data-unlocks") + '"]');
        var all = Array.prototype.every.call(group, function (b) { return b.checked; });
        ids.forEach(function (id) { var t = document.getElementById(id); if (t) { t.setAttribute("aria-disabled", all ? "false" : "true"); t.tabIndex = all ? 0 : -1; } });
      }
      box.addEventListener("change", sync); sync();
    });

    // Tappable sentences (choose the highlighted words).
    document.querySelectorAll(".sent").forEach(function (s) {
      s.setAttribute("role", "checkbox"); s.tabIndex = 0;
      s.setAttribute("aria-checked", s.classList.contains("on") ? "true" : "false");
      function flip() { s.classList.toggle("on"); s.setAttribute("aria-checked", s.classList.contains("on") ? "true" : "false"); }
      s.addEventListener("click", flip);
      s.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } });
    });

    // Scroll the source card (not the page) so the first highlight is in view.
    document.querySelectorAll("[data-scroll-mark]").forEach(function (body) {
      var m = body.querySelector("mark"); if (m && m.offsetTop + m.offsetHeight > body.clientHeight - 16) body.scrollTop = Math.max(0, m.offsetTop - 72);
    });

    // Copy buttons: the label says "Copied" for 2 s at the same width.
    document.querySelectorAll("[data-copy]").forEach(function (b) {
      b.addEventListener("click", function () {
        var src = document.getElementById(b.getAttribute("data-copy")); if (!src) return;
        var done = function () { var old = b.getAttribute("data-label") || b.textContent; b.setAttribute("data-label", old); b.textContent = "Copied"; setTimeout(function () { b.textContent = old; }, 2000); };
        try { navigator.clipboard.writeText(src.textContent).then(done, done); } catch (e) { done(); }
      });
    });

    // Download buttons: a client-side text file (code, no server).
    document.querySelectorAll("[data-download]").forEach(function (b) {
      b.addEventListener("click", function () {
        var src = document.getElementById(b.getAttribute("data-download")); if (!src) return;
        var a = document.createElement("a");
        a.href = URL.createObjectURL(new Blob([src.textContent], { type: "text/plain" }));
        a.download = b.getAttribute("data-name") || "letter.txt"; a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      });
    });

    // Find a case (home): filters the cards as she types.
    var find = document.getElementById("find-case");
    if (find) find.addEventListener("input", function () {
      var q = find.value.trim().toLowerCase();
      document.querySelectorAll(".ccard").forEach(function (c) { c.hidden = q && c.getAttribute("data-title").toLowerCase().indexOf(q) < 0; });
    });

    // Delete confirm swaps the card's bottom row in place.
    document.querySelectorAll("[data-delete]").forEach(function (b) {
      b.addEventListener("click", function () {
        var row = b.closest(".cc-bottom"); var ask = row.nextElementSibling;
        row.hidden = true; ask.hidden = false; ask.querySelector("button").focus();
      });
    });
    document.querySelectorAll("[data-keep]").forEach(function (b) {
      b.addEventListener("click", function () { var ask = b.closest(".cc-bottom"); ask.hidden = true; ask.previousElementSibling.hidden = false; });
    });

    // Drafting: walk the fixed stage list, then show the done box in the same place.
    var stages = document.getElementById("stages");
    if (stages) {
      var items = stages.querySelectorAll("li"); var i = parseInt(stages.getAttribute("data-start") || "0", 10);
      var bar = document.getElementById("draft-bar"); var count = document.getElementById("draft-count");
      var running = document.getElementById("draft-running"); var finished = document.getElementById("draft-done");
      var tick = function () {
        items.forEach(function (li, k) { li.className = k < i ? "done" : (k === i ? "now" : ""); li.querySelector(".ic").textContent = k < i ? "✓" : ""; });
        if (bar) bar.style.width = Math.round((i / items.length) * 100) + "%";
        if (count) count.textContent = Math.min(i + 1, items.length) + " of " + items.length;
        if (i >= items.length) { if (running) running.hidden = true; if (finished) { finished.hidden = false; var go = finished.querySelector(".btn"); if (go) go.focus(); } return; }
        i += 1; setTimeout(tick, stages.hasAttribute("data-slow") ? 2600 : 900);
      };
      if (!stages.hasAttribute("data-hold")) tick();
    }
  });
})();
