/* Scroll experience for phones and tablets, every page. One small module, no library. Only transform and opacity move.
   Vocabulary (data-sx): rise, left (steps), scale (tiles), pop (icons and numerals), draw (a gold line then the content), mask (curtain lifts, photo settles), words (headings).
   data-px marks a big photo that drifts a little against the scroll. A gold progress line sits at the top edge.
   Off for desktop (GSAP and the existing reveals do that), reduced motion and Save-Data (html.sx-calm: all content simply visible). Without JS nothing is hidden:
   the hiding rules need html.sxm, which this file adds. Runs in idle slices, never touches the hero or the first screen. */
(function () {
  "use strict";
  var d = document, de = d.documentElement;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var conn = navigator.connection || {}, saveData = !!conn.saveData;
  if (saveData) { de.classList.add("sx-calm"); return; }
  if (reduce) return;
  var active = matchMedia("(max-width: 1023px), (hover: none)").matches;
  if (!active || !("IntersectionObserver" in window)) return;
  function $$(s) { return [].slice.call(d.querySelectorAll(s)); }

  /* selector, kind, stagger group (children of the same parent get 70 ms steps) */
  var PLAN = [
    ["main h2.h2, main .cta__big, main .rvw__head h2, main .fq h2", "words"],
    [".sv-row__ph", "mask"],
    [".sv-row__t > *", "rise"],
    [".sv-more__i", "scale"], [".sv-pills li", "rise"],
    [".gal__list li", "scale"], [".pj__grid li", "rise"],
    [".sv-offer li", "left"], [".sv-offer .ic", "pop"],
    [".sv-step", "left"], [".sv-step__n", "pop"],
    [".sv-why__i", "draw"],
    [".sv-rev", "rise"], [".sv-faq__r", "rise"],
    [".sv-cta .form--card, .contact .form--card, .cq .form--card", "scale"],
    [".side > div", "rise"], [".next3 li", "rise"], [".commit__item", "rise"], [".team .tm", "rise"], [".golist li", "rise"],
    [".trust__item", "pop"], [".proof__tile", "pop"], [".bst__ul:not(.bst__dup) li", "pop"],
    [".bst__l", "rise"]
  ];
  var PX = [".sv-hero__ph", ".sv-row__ph", ".tilt"];
  var idle = window.requestIdleCallback ? function (f) { requestIdleCallback(f, { timeout: 1500 }); } : function (f) { setTimeout(f, 200); };

  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("sx-in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -9% 0px", threshold: 0.1 });

  function split(el) {
    if (el.querySelector(".sxw")) return;
    var words = el.textContent.replace(/\s+/g, " ").trim().split(" "), frag = d.createDocumentFragment();
    words.forEach(function (w, k) {
      var o = d.createElement("span"), n = d.createElement("span");
      o.className = "sxw"; n.className = "sxi"; n.textContent = w; n.style.setProperty("--wd", Math.min(k * 45, 420) + "ms"); o.appendChild(n);
      frag.appendChild(o); if (k < words.length - 1) frag.appendChild(d.createTextNode(" "));
    });
    el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
    el.textContent = ""; el.appendChild(frag);
    [].forEach.call(el.children, function (c) { c.setAttribute("aria-hidden", "true"); });
  }

  var home = !!d.querySelector(".hero");
  var jobs = [], tagged = [];
  PLAN.forEach(function (p) {
    jobs.push(function () {
      var seen = new Map();
      $$(p[0]).forEach(function (el) {
        if (el.closest(".hero, .page-hero, .banner, .site-header, .menu, .foot") || el.hasAttribute("data-sx")) return;
        if (p[1] === "words" && home && el.closest("#who, #services, #adu, #why, #reviews, #faq, #contact")) return;   /* motion.js already splits these on Home */
        var par = el.parentNode, i = seen.get(par) || 0; seen.set(par, i + 1);
        el.classList.remove("rv"); el.removeAttribute("data-rv");       /* this element carries its own reveal now */
        el.setAttribute("data-sx", p[1]);
        el.style.setProperty("--sd", Math.min(i, 6) * 70 + "ms");
        if (p[1] === "words") split(el);
        tagged.push(el);
      });
    });
  });
  jobs.push(function () {
    PX.forEach(function (s) { $$(s).forEach(function (el) { if (!el.closest(".banner, .site-header")) el.setAttribute("data-px", ""); }); });
  });

  (function run() {
    idle(function (dl) {
      while (jobs.length && (!dl || !dl.timeRemaining || dl.timeRemaining() > 4 || dl.didTimeout)) {
        if (!de.classList.contains("sxm")) de.classList.add("sxm");
        jobs.shift()();
        if (dl && dl.didTimeout) break;
      }
      if (jobs.length) run(); else { tagged.forEach(function (el) { io.observe(el); }); parallax(); }
    });
  })();

  /* ---------- depth: photos marked data-px drift a little while they are on screen ---------- */
  function parallax() {
    var els = $$("[data-px]"), vis = new Set(), raf = 0, vh = innerHeight;
    if (!els.length) return;
    var pio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) vis.add(e.target); else vis.delete(e.target); }); queue(); }, { rootMargin: "20% 0px" });
    els.forEach(function (el) { pio.observe(el); });
    function frame() {
      raf = 0; var rects = [];
      vis.forEach(function (el) { rects.push([el, el.getBoundingClientRect()]); });            /* all reads first */
      rects.forEach(function (r) {
        var c = (r[1].top + r[1].height / 2 - vh / 2) / vh;                                     /* about -1 above, 0 centred, 1 below */
        r[0].style.setProperty("--py", (Math.max(-1, Math.min(1, c)) * -22).toFixed(1));       /* then the writes */
      });
    }
    function queue() { if (!raf) raf = requestAnimationFrame(frame); }
    addEventListener("scroll", queue, { passive: true });
    addEventListener("resize", function () { vh = innerHeight; queue(); }, { passive: true });
    queue();
  }

  /* ---------- progress cue ---------- */
  (function () {
    var bar = d.createElement("i"), raf = 0;
    bar.className = "sx-prog"; bar.setAttribute("aria-hidden", "true"); d.body.appendChild(bar);
    function frame() {
      raf = 0;
      var h = de.scrollHeight - innerHeight, p = h > 0 ? Math.min(1, Math.max(0, scrollY / h)) : 0;
      bar.style.transform = "scaleX(" + p.toFixed(4) + ")";
    }
    function queue() { if (!raf) raf = requestAnimationFrame(frame); }
    addEventListener("scroll", queue, { passive: true }); addEventListener("resize", queue, { passive: true }); queue();
  })();
})();
