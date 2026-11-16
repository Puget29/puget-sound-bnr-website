/* Phones and touch: calm reveals, swipe hints, section hairlines and action bar rules. Vanilla JS, no library.
   This file only tags elements (data-rv) and wires small helpers. The one reveal observer lives in v4.js and adds is-in once.
   Vocabulary (data-rv): rise (default), words, scale, clip, draw. data-stagger on a parent staggers its children.
   Switch the section hairlines off with data-st="off" on <body>. Reduced motion, no JS and print show everything at once (see the css). */
(function () {
  "use strict";
  var d = document, de = d.documentElement, reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = matchMedia("(max-width: 899px), (hover: none)").matches, touch = matchMedia("(hover: none)").matches;
  function $(s, r) { return (r || d).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || d).querySelectorAll(s)); }

  /* ---------- A. reveal: tag what arrives, below the first screen only ----------
     Runs in idle time in small slices (no layout reads, only attribute and class writes), so it never delays the first paint. v4.js observes the tagged elements when it hears "bnr-tagged". */
  var idle = window.requestIdleCallback ? function (f) { requestIdleCallback(f, { timeout: 1500 }); } : function (f) { setTimeout(f, 200); };
  if (small && !reduce) {
    var PLAN = [
      ["#who h2, #services h2, #adu h2, #why h2, #reviews h2, #faq h2, #contact h2", "words"],
      ["#who .step, #who li, #who .pillar, #who .tl4 li", "rise"],
      ["#services .car", "scale"], ["#services .more__li", "rise"],
     
      ["#trust .lgs__c", "rise"], ["#why .why__p", "rise"],
      ["#reviews .rvw__deck", "scale"], ["#reviews .rvw__ctl, #reviews .rvw__also", "rise"],
      ["#faq .fq__row", "rise"], ["#contact .cq__actions", "rise"], [".foot .foot__col, .foot li", "rise"]
    ];
    var jobs = [];
    PLAN.forEach(function (p) {
      jobs.push(function () {
        $$(p[0]).forEach(function (el, i) {
          if (!el.closest("section") || el.closest(".hero")) return;                 /* never wait for JS above the fold (the hero fills the first screen) */
          if (p[1] === "words") el.classList.remove("rv");                           /* the headline carries its own reveal */
          else if (el.classList.contains("rv") || el.hasAttribute("data-rv")) return; /* already part of the reveal system */
          el.setAttribute("data-rv", p[1]);
          if (p[1] === "rise" || p[1] === "scale") el.style.setProperty("--rd", Math.min(i % 6, 6) * 60 + "ms");
          if (p[1] === "words" && !el.querySelector(".wi")) {
            var words = el.textContent.replace(/\s+/g, " ").trim().split(" "), frag = d.createDocumentFragment();
            words.forEach(function (w, k) {
              var o = d.createElement("span"), n = d.createElement("span");
              o.className = "w"; n.className = "wi"; n.textContent = w; n.style.setProperty("--wd", Math.min(k * 40, 400) + "ms"); o.appendChild(n);
              frag.appendChild(o); if (k < words.length - 1) frag.appendChild(d.createTextNode(" "));
            });
            el.textContent = ""; el.appendChild(frag);
          }
        });
      });
    });
    (function run() {
      idle(function (dl) {
        while (jobs.length && (!dl || !dl.timeRemaining || dl.timeRemaining() > 4 || dl.didTimeout)) {
          if (!de.classList.contains("rvx")) de.classList.add("rvx");
          jobs.shift()();
          if (dl && dl.didTimeout) break;
        }
        if (jobs.length) run(); else window.dispatchEvent(new Event("bnr-tagged"));
      });
    })();
  }

  /* ---------- B. light haptic on chip and selector taps (does nothing on iPhone) ---------- */
  if (touch && !reduce && navigator.vibrate) {
    d.addEventListener("click", function (e) {
      if (e.target.closest(".sel__btn, .more__a")) { try { navigator.vibrate(8); } catch (x) {} }
    }, { passive: true });
  }

  /* ---------- C. swipe hint: once per session, a short nudge toward the next card ---------- */
  function hint(host, key) {
    if (!touch || reduce || !host || !("IntersectionObserver" in window)) return;
    try { if (sessionStorage.getItem(key)) return; } catch (e) {}
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return;
      io.disconnect();
      var last = -1, tries = 0;
      (function settle() {                     /* nudge only once the page has stopped moving */
        if (window.scrollY !== last && tries++ < 12) { last = window.scrollY; setTimeout(settle, 220); return; }
        try { sessionStorage.setItem(key, "1"); } catch (e) {}
        host.classList.add("is-nudge");
        function stop() { host.classList.remove("is-nudge"); ["touchstart", "wheel", "scroll"].forEach(function (t) { window.removeEventListener(t, stop, true); }); }
        ["touchstart", "wheel", "scroll"].forEach(function (t) { window.addEventListener(t, stop, { capture: true, passive: true, once: true }); });
        setTimeout(stop, 1000);
      })();
    }, { threshold: 0.6 });
    io.observe(host);
  }
  hint($("#services .car"), "bnr-hint-svc");
  hint($("#reviews .rvw__deck"), "bnr-hint-rvw");

  /* ---------- D. section hairlines: a gold line draws outward from the middle as a section arrives (mobile and tablet) ---------- */
  if (matchMedia("(max-width: 999px)").matches && !reduce && d.body && d.body.getAttribute("data-st") !== "off" && "IntersectionObserver" in window) {
    var sio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { var st = e.target.querySelector(":scope > .st"); if (st) st.classList.add("is-in"); sio.unobserve(e.target); } }); }, { rootMargin: "0px 0px -15% 0px" });
    var lines = [];
    $$("main > section").forEach(function (s) {
      if (s.classList.contains("hero") || s.id === "faq" || s.id === "contact") return;
      var st = d.createElement("i"); st.className = "st"; st.setAttribute("aria-hidden", "true"); st.innerHTML = "<b></b>";
      s.insertBefore(st, s.firstChild); sio.observe(s); lines.push({ section: s, line: st });
    });
    var lineRaf = 0, left = lines.length;
    function sweepLines() {
      lineRaf = 0;
      var edge = window.innerHeight * 0.85, due = [];
      lines.forEach(function (item) { if (!item.done && item.section.getBoundingClientRect().top < edge) due.push(item); });   /* all reads first */
      due.forEach(function (item) { item.done = true; item.line.classList.add("is-in"); sio.unobserve(item.section); left--; });   /* then the writes */
      if (!left) { window.removeEventListener("scroll", queueLines); window.removeEventListener("resize", queueLines); }
    }
    function queueLines() { if (!lineRaf) lineRaf = requestAnimationFrame(sweepLines); }
    window.addEventListener("scroll", queueLines, { passive: true });
    window.addEventListener("resize", queueLines, { passive: true });
  }

  /* ---------- E. action bar: hidden at the contact section, the footer, while the menu is open and while a field has focus ---------- */
  (function () {
    var bar = $(".mbar"); if (!bar) return;
    var flags = { sec: false, field: false };
    function upd() { d.body.classList.toggle("mbar-off", flags.sec || flags.field); }
    if ("IntersectionObserver" in window) {
      var vis = {}, bio = new IntersectionObserver(function (es) { es.forEach(function (e) { vis[e.target.className + e.target.id] = e.isIntersecting; }); flags.sec = Object.keys(vis).some(function (k) { return vis[k]; }); upd(); }, { threshold: 0.05 });
      [$("#contact.cq"), $(".foot")].forEach(function (el) { if (el) bio.observe(el); });
    }
    d.addEventListener("focusin", function (e) { flags.field = /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) && e.target.type !== "radio" && e.target.type !== "checkbox"; upd(); });
    d.addEventListener("focusout", function () { setTimeout(function () { var a = d.activeElement; flags.field = !!a && /^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName) && a.type !== "radio" && a.type !== "checkbox"; upd(); }, 0); });
  })();

})();
