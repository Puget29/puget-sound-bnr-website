/* Glass dock navigation (vanilla port of the glass-dock idea).
   - a capsule slides to the hovered item
   - the hovered word collapses and springs back (the icon "morph" timing, applied to text)
   - a tooltip follows, and its text swaps with a directional blur-slide
   Needs GSAP core (vendor/gsap.min.js). Does nothing on touch layouts or if GSAP is missing. */
(function () {
  "use strict";
  var dock = document.querySelector(".pill");
  var nav = dock && dock.querySelector(".nav");
  var glass = nav && nav.querySelector(".dock__glass");
  var tip = dock && dock.querySelector(".dock__tip");
  var tipText = tip && tip.querySelector(".dock__tipText");
  if (!nav || !glass || !tip || !window.gsap) return;

  var gsap = window.gsap;
  var items = [].slice.call(nav.querySelectorAll(".dock__item"));
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var cta = dock.querySelector(".pill__cta");
  var subtle = dock.getAttribute("data-motion") === "subtle"; /* quieter pop, tooltip and text swap; default is the full effect */
  var current = -1, tipShown = false, hideTimer = 0;

  function visibleItems() { return items.filter(function (el) { return el.offsetParent !== null; }); }
  function usable() { return nav.offsetParent !== null && getComputedStyle(nav).display !== "none"; }
  function dur(v) { return reduce.matches ? 0 : v; }

  /* the word collapses to a quarter, then springs back with the same elastic ease as the icon morph */
  function pop(label) {
    if (reduce.matches) return;
    gsap.killTweensOf(label);
    if (subtle) { /* a small dip and a smooth return, no bounce */
      gsap.timeline()
        .to(label, { scale: 0.95, opacity: 0.7, duration: 0.09, ease: "power1.out" })
        .to(label, { scale: 1, opacity: 1, duration: 0.35, ease: "power2.out" });
      return;
    }
    gsap.timeline()
      .to(label, { scale: 0.25, opacity: 0, duration: 0.1, ease: "power1.in" })
      .to(label, { scale: 1, opacity: 1, duration: 0.8, ease: "elastic.out(1, .9)" });
  }

  function tipWidthFor(text) {
    var probe = document.createElement("span");
    probe.textContent = text;
    probe.style.cssText = "position:absolute;visibility:hidden;white-space:nowrap;font-size:.8rem;font-weight:500;letter-spacing:.01em";
    tipText.appendChild(probe);
    var w = probe.offsetWidth; probe.remove();
    return Math.max(100, w + 40);
  }

  function setTipText(text, dir) {
    var old = tipText.querySelector("span:not(.is-leaving)");
    if (old && old.textContent === text) return;
    var sp = document.createElement("span");
    sp.textContent = text;
    tipText.appendChild(sp);
    var move = subtle ? 12 : 35, blur = subtle ? "blur(2px)" : "blur(6px)", t = subtle ? 0.22 : 0.3;
    var shift = dir === 0 ? 0 : (dir > 0 ? move : -move);
    gsap.fromTo(sp, { x: shift, opacity: 0, filter: blur }, { x: 0, opacity: 1, filter: "blur(0px)", duration: dur(t), ease: "power2.out" });
    if (old) {
      old.classList.add("is-leaving");
      gsap.to(old, { x: -shift, opacity: 0, filter: blur, duration: dur(t), ease: "power2.out", onComplete: function () { old.remove(); } });
    }
  }

  function geometry(el) {
    var navLeft = nav.offsetLeft;
    return { left: el.offsetLeft, width: el.offsetWidth, center: navLeft + el.offsetLeft + el.offsetWidth / 2 };
  }

  function enter(el) {
    clearTimeout(hideTimer);
    var list = visibleItems();
    var idx = list.indexOf(el);
    if (idx < 0) return;
    var dir = current < 0 ? 0 : (idx > current ? 1 : -1);
    if (idx === current && tipShown) return;
    var g = geometry(el);
    var text = el.getAttribute("data-tip") || "";
    var w = tipWidthFor(text);
    var x = g.center - w / 2;

    list.forEach(function (o) { o.classList.toggle("is-hover", o === el); });

    if (current < 0) { /* first entry: appear in place */
      gsap.set(glass, { x: g.left, width: g.width });
      gsap.to(glass, { opacity: 1, duration: dur(0.25) });
      gsap.set(tip, { x: x, width: w, y: subtle ? -4 : -8, scale: subtle ? 0.98 : 0.92, visibility: "visible" });
      gsap.to(tip, { opacity: 1, y: 0, scale: 1, duration: dur(subtle ? 0.25 : 0.4), ease: subtle ? "power2.out" : "back.out(1.6)", overwrite: "auto" });
      setTipText(text, 0);
    } else {
      gsap.to(glass, { x: g.left, width: g.width, opacity: 1, duration: dur(0.5), ease: "power3.out", overwrite: "auto" });
      gsap.to(tip, { x: x, width: w, opacity: 1, y: 0, scale: 1, duration: dur(subtle ? 0.35 : 0.55), ease: "power3.out", overwrite: "auto" });
      setTipText(text, dir);
    }
    tipShown = true;
    current = idx;
    pop(el.querySelector(".dock__label"));
  }

  function leave() {
    hideTimer = setTimeout(function () {
      var list = visibleItems();
      list.forEach(function (o) { o.classList.remove("is-hover"); });
      gsap.to(glass, { opacity: 0, duration: dur(0.2), overwrite: "auto" });
      gsap.to(tip, { opacity: 0, y: -8, scale: 0.92, duration: dur(0.2), overwrite: "auto", onComplete: function () { tip.style.visibility = "hidden"; } });
      current = -1; tipShown = false;
    }, 40);
  }

  items.forEach(function (el) {
    el.addEventListener("mouseenter", function () { if (usable()) enter(el); });
    el.addEventListener("focus", function () { if (usable()) enter(el); });
    el.addEventListener("blur", leave);
  });
  nav.addEventListener("mouseleave", leave);
  if (cta) cta.addEventListener("mouseenter", leave);
  window.addEventListener("resize", function () { if (tipShown && !usable()) leave(); });
})();
