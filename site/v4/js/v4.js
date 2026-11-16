/* BNR v4 behaviour. Vanilla JS, no dependencies. Loaded before hero-v4.js (it builds the announcement band that hero-v4.js then wires up).
   Everything degrades: without JS the content is all visible (the .js class on <html> gates every hidden-until-revealed state).
   CONFIG is the one place for things that change at launch. */
(function () {
  "use strict";

  var CONFIG = {
    maxFileMb: 10,
    fileTypes: ["image/jpeg", "image/png", "image/webp", "image/heic", "application/pdf"]
  };

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return [].slice.call((c || document).querySelectorAll(s)); }
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  /* ---------- announcement band: the offer text comes from data-offer on .banner. Remove the attribute value and the band goes away. ---------- */
  (function banner() {
    var b = $(".banner");
    if (!b) return;
    var offer = (b.getAttribute("data-offer") || "").trim();
    if (!offer) { b.remove(); document.documentElement.style.setProperty("--banner-h", "0px"); return; }
    var track = $(".banner__track", b);
    if (!track) return;
    function item() { var s = document.createElement("span"); s.className = "banner__item"; s.textContent = offer; return s; }
    track.textContent = "";
    for (var g = 0; g < 2; g++) {
      var grp = document.createElement("div");
      grp.className = "banner__group";
      if (g) grp.setAttribute("aria-hidden", "true");
      for (var i = 0; i < 6; i++) grp.appendChild(item());
      track.appendChild(grp);
    }
  })();

  /* ---------- reveal, line draw, count up ---------- */
  $$(".art").forEach(function (a) { $$("path, rect, line, circle, ellipse, polyline", a).forEach(function (el, i) { el.style.setProperty("--i", Math.min(i, 24)); el.setAttribute("pathLength", "1"); }); });
  var smallRv = matchMedia("(max-width: 899px), (hover: none)").matches;
  if ("IntersectionObserver" in window) {
    var secs = $$("main > section");
    var show = function (el) { if (el.classList.contains("is-in")) return; el.classList.add("is-in"); io.unobserve(el); if (el.hasAttribute("data-count")) countUp(el); if (el.hasAttribute("data-rv")) { el.style.willChange = "transform, opacity"; setTimeout(function () { el.style.willChange = ""; }, 1100); } };
    var rest = function (s) { return $$(".rv, .art, [data-rv]", s).filter(function (el) { return !el.classList.contains("is-in"); }); };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) show(e.target); });
    }, smallRv ? { threshold: 0, rootMargin: "0px 0px -12% 0px" } : { threshold: 0, rootMargin: "0px 0px -8% 0px" });
    $$(".rv, .art, [data-count], [data-rv]").forEach(function (el) { io.observe(el); });
    window.addEventListener("bnr-tagged", function () { $$("[data-rv]").forEach(function (el) { if (!el.classList.contains("is-in")) io.observe(el); }); });   /* motion.js tags in idle time */
    /* Keep below-fold content visible after a fast flick or a missed observer callback. Read first, then write classes. */
    if (smallRv) {
      var sweepTimer = 0;
      function sweep() {
        sweepTimer = 0;
        var visible = [], edge = window.innerHeight;
        secs.forEach(function (s) {
          var r = s.getBoundingClientRect();
          if (r.bottom < 0) {
            visible.push.apply(visible, rest(s));
          } else if (r.top < edge && r.bottom > 0) {
            rest(s).forEach(function (el) { if (el.getBoundingClientRect().top < edge) visible.push(el); });
          }
        });
        visible.forEach(show);
      }
      function queueSweep() { if (!sweepTimer) sweepTimer = setTimeout(sweep, 100); }
      window.addEventListener("scroll", queueSweep, { passive: true });
      window.addEventListener("resize", queueSweep);
      setTimeout(sweep, 2500);
    } else {
      setTimeout(function () { secs.forEach(function (s) { var r = s.getBoundingClientRect(); if (r.top < window.innerHeight && r.bottom > 0) rest(s).forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) show(el); }); }); }, 2500);
    }
    window.addEventListener("hashchange", function () { var t = document.getElementById(location.hash.slice(1)); if (t) $$(".rv, [data-rv], .art", t).forEach(show); });
  } else {
    $$(".rv, .art, [data-rv]").forEach(function (el) { el.classList.add("is-in"); });
  }
  function countUp(el) {
    var end = parseFloat(el.getAttribute("data-count")), suffix = el.getAttribute("data-suffix") || "";
    if (isNaN(end)) return;
    if (reduce.matches) { el.textContent = end + suffix; return; }
    var t0 = performance.now(), dur = 1300;
    (function step(now) {
      var p = clamp((now - t0) / dur, 0, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * eased) + suffix;
      if (p < 1) requestAnimationFrame(step);
    })(t0);
  }
  $$("[data-count]").forEach(function (el) { if (!reduce.matches) el.textContent = "0" + (el.getAttribute("data-suffix") || ""); });

  /* ---------- service area: the list and the pins light each other ---------- */
  (function area() {
    var lis = $$(".cities li[data-city]"), pins = $$(".map .pin[data-city]");
    if (!lis.length) return;
    function on(city, v) {
      lis.forEach(function (l) { if (l.getAttribute("data-city") === city) l.classList.toggle("is-on", v); });
      pins.forEach(function (p) { if (p.getAttribute("data-city") === city) p.classList.toggle("is-on", v); });
    }
    lis.forEach(function (l) { var c = l.getAttribute("data-city"); l.addEventListener("mouseenter", function () { on(c, true); }); l.addEventListener("mouseleave", function () { on(c, false); }); });
    pins.forEach(function (p) { var c = p.getAttribute("data-city"); p.addEventListener("mouseenter", function () { on(c, true); }); p.addEventListener("mouseleave", function () { on(c, false); }); });
  })();

  /* ---------- reviews: render from the data array if it has anything, else the "coming soon" block stays ---------- */
  (function reviews() {
    var host = $("#reviews-list"), dataEl = $("#reviews-data");
    if (!host || !dataEl) return;
    var items = []; try { items = JSON.parse(dataEl.textContent); } catch (e) { return; }
    if (!items.length) return;
    host.textContent = ""; host.className = "rev";
    var STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.6l2.5 5.4 5.9.7-4.4 4 1.2 5.8L10 14.6l-5.2 2.9 1.2-5.8-4.4-4 5.9-.7L10 1.6Z" fill="currentColor"/></svg>';
    items.slice(0, 3).forEach(function (r) { /* each review: { name, city, text, stars } */
      var c = document.createElement("figure"); c.className = "rcard"; c.style.margin = "0";
      var n = Math.max(1, Math.min(5, parseInt(r.stars, 10) || 5));
      var st = document.createElement("span"); st.className = "stars"; st.setAttribute("role", "img"); st.setAttribute("aria-label", n + " out of 5 stars");
      st.innerHTML = new Array(n + 1).join(STAR);
      var q = document.createElement("blockquote"); q.textContent = r.text;
      var ci = document.createElement("cite"); ci.textContent = r.name + (r.city ? ", " + r.city : "");
      c.appendChild(st); c.appendChild(q); c.appendChild(ci); host.appendChild(c);
    });
  })();

  /* ---------- forms ---------- */
  $$(".form[data-form]").forEach(function (form) {
    var fields = $$("[data-req], [data-kind]", form);
    var qs = new URLSearchParams(location.search), svc = qs.get("service"), sel = $('select[name="service"]', form);
    var alias = { deck: "deck-siding", siding: "deck-siding" }; /* the Contact page still has one Deck or siding choice */
    if (svc && sel) { var opt = $$("option", sel).filter(function (o) { return o.value === svc || o.value === alias[svc]; })[0]; if (opt) sel.value = opt.value; }
    function check(el) {
      var kind = el.getAttribute("data-kind"), msg = window.BNRForm ? BNRForm.msg(el) : "";
      if (msg) { /* the shared module found a problem */ }
      else if (kind === "file" && el.files && el.files[0]) {
        var f = el.files[0];
        if (CONFIG.fileTypes.indexOf(f.type) < 0) msg = "Use a JPG, PNG, WebP, HEIC or PDF file.";
        else if (f.size > CONFIG.maxFileMb * 1048576) msg = "The file is over " + CONFIG.maxFileMb + " MB.";
      }
      var err = el.id && $("#" + el.id + "-err", form);
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg;
      return !msg;
    }
    fields.forEach(function (el) { el.addEventListener("blur", function () { if (el.value || el.getAttribute("aria-invalid")) check(el); }); el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") check(el); }); el.addEventListener("change", function () { if (el.getAttribute("data-kind") === "file") check(el); }); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var hp = $('input[name="company"]', form); if (hp && hp.value) return; /* honeypot: bots fill it, people never see it */
      var bad = fields.filter(function (el) { return !check(el); });
      if (bad.length) { bad[0].focus(); return; }
      var ok = $(".form__ok", form), msg = $(".form__ok-text", form), btn = $('[type="submit"]', form);
      function done(demo) {
        if (msg) msg.textContent = "We have your details. Someone from the office will get back to you." + (demo ? " Demo only. Nothing was sent." : "");
        form.classList.add("is-done"); if (ok) { ok.setAttribute("tabindex", "-1"); ok.focus(); }
      }
      if (btn) btn.disabled = true;
      BNRForm.send(new FormData(form), form.getAttribute("data-source") || "contact-page", form)
        .then(function (r) { done(r.demo); })
        .catch(function () { if (btn) btn.disabled = false; var s = $(".form__fail", form); if (s) { s.hidden = false; s.textContent = BNRForm.error; s.focus(); } });
    });
  });

  /* ---------- phone action bar: appears once the hero is behind you (landing) or after a short scroll (other pages) ---------- */
  (function mbar() {
    var bar = $(".mbar"), hero = $(".hero"), menu = $("#menu");
    if (!bar) return;
    document.body.classList.add("has-mbar");
    function upd() { var on = hero ? hero.getBoundingClientRect().bottom <= 0 : window.scrollY > 240; bar.classList.toggle("is-on", on); }
    window.addEventListener("scroll", function () { requestAnimationFrame(upd); }, { passive: true });
    window.addEventListener("resize", upd); upd();
    if (menu && "MutationObserver" in window) new MutationObserver(function () { document.body.classList.toggle("menu-is-open", menu.classList.contains("is-open")); }).observe(menu, { attributes: true, attributeFilter: ["class"] });
  })();

  /* ---------- About hero: a small depth tilt (mouse only, no 3D library). Static for touch and reduced motion. ---------- */
  (function tilt() {
    var t = $(".tilt");
    if (!t || reduce.matches || !window.matchMedia("(hover: hover) and (min-width: 901px)").matches) return;
    var raf = 0, x = 0, y = 0;
    t.addEventListener("pointermove", function (e) { var r = t.getBoundingClientRect(); x = ((e.clientX - r.left) / r.width - 0.5) * 2; y = ((e.clientY - r.top) / r.height - 0.5) * 2; if (!raf) raf = requestAnimationFrame(function () { raf = 0; t.style.setProperty("--tx", x.toFixed(3)); t.style.setProperty("--ty", y.toFixed(3)); }); });
    t.addEventListener("pointerleave", function () { t.style.setProperty("--tx", 0); t.style.setProperty("--ty", 0); });
  })();
})();
