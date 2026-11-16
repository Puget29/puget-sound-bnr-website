/* Trust strip: the logos are already in the HTML. This config adds a logo with one line, or fills in a logo file and a profile link that did not exist at build time.
   Add a brand:    brands: [{ name: "Brand", src: "assets/logos/brand.svg", href: "" }]
   Fill a profile: profiles: [{ name: "Google", src: "assets/logos/google.svg", href: "https://..." }] (the name must match the existing cell) */
(function () {
  "use strict";
  /* To link Google or BBB: set href below, for example { name: "Google", src: "assets/logos/google.svg", href: "https://..." } */
  var TRUST = { brands: [{ name: "The Home Depot", src: "", href: "" }, { name: "Lowe's", src: "", href: "" }, { name: "Floor and Decor", src: "", href: "" }, { name: "Sherwin-Williams", src: "", href: "" },
      { name: "GAF", src: "", href: "" }, { name: "Trex", src: "", href: "" }, { name: "James Hardie", src: "", href: "" }, { name: "Milgard", src: "", href: "" }],
    profiles: [{ name: "Google", src: "", href: "" }, { name: "BBB", src: "", href: "" }, { name: "Yelp", src: "", href: "" }, { name: "Angie", src: "", href: "" }] };
  function img(it) { var i = new Image(); i.src = it.src; i.alt = it.name; i.width = it.w || 120; i.height = it.h || 32; i.loading = "lazy"; i.decoding = "async"; return i; }
  [["brands", "lgs-brands"], ["profiles", "lgs-profiles"]].forEach(function (g) {
    var ul = document.getElementById(g[1]); if (!ul) return;
    TRUST[g[0]].forEach(function (it) {
      var li = [].slice.call(ul.children).filter(function (c) { var t = c.querySelector("img, .lgs__ph"); return t && (t.alt || t.textContent) === it.name; })[0];
      if (!li) { if (!it.src) return; li = document.createElement("li"); li.className = "lgs__c is-in"; ul.appendChild(li); }
      if (it.src && !li.querySelector("img")) { var ph = li.querySelector(".lgs__ph"); if (ph) ph.replaceWith(img(it)); else li.insertBefore(img(it), li.firstChild); }
      if (g[0] === "profiles" && it.href && !li.querySelector("a")) {
        var a = document.createElement("a"); a.className = "lgs__a"; a.href = it.href; a.target = "_blank"; a.rel = "noopener noreferrer";
        a.setAttribute("aria-label", "Puget Sound Builders and Renovation on " + it.name + " (opens in a new tab)");
        while (li.firstChild && li.firstChild.nodeName !== "SPAN") a.appendChild(li.firstChild); a.insertAdjacentHTML("beforeend", '<svg class="lgs__go" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M4 10L10 4M5 4h5v5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'); li.insertBefore(a, li.firstChild); li.removeAttribute("data-confirm");
      }
    });
  });
})();

/* The main site brand row uses the same slider behavior as the PPC logo band. */
(function () {
  var S = document.querySelectorAll('[data-sl]'); if (!S.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var L = [], raf = 0, last = 0, away = document.hidden;
  function active(o) { return o.vis && !away && !o.hov && !o.foc && !o.down && performance.now() > o.until; }
  function kick() { if (!raf && L.some(active)) { last = performance.now(); raf = requestAnimationFrame(tick); } }
  function tick(t) {
    var dt = Math.min(250, t - last), n = 0; last = t; raf = 0;
    L.forEach(function (o) {
      if (!active(o)) return; n++;
      var c = o.el.scrollLeft; if (Math.abs(c - o.pos) > 1.5) o.pos = c;
      o.pos += 0.036 * dt; if (o.pos >= 2 * o.w) o.pos -= o.w; else if (o.pos < o.w) o.pos += o.w;
      o.self = 1; o.el.scrollLeft = o.pos;
    });
    if (n) raf = requestAnimationFrame(tick);
  }
  function hold(o, ms) { o.until = performance.now() + ms; setTimeout(kick, ms + 30); }
  function build(o) {
    var el = o.el, set = o.set, w0 = o.w, ph = w0 ? ((el.scrollLeft - w0) % w0 + w0) % w0 : 0;
    [].forEach.call(el.querySelectorAll('[data-c]'), function (x) { el.removeChild(x); });
    var w = set.getBoundingClientRect().width; if (!w) return; o.w = w;
    for (var i = Math.ceil(2 * el.clientWidth / w) + 1; i--;) {
      var c = set.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.setAttribute('data-c', '');
      [].forEach.call(c.querySelectorAll('a'), function (a) { a.tabIndex = -1; });
      i ? el.appendChild(c) : el.insertBefore(c, set);
    }
    el.scrollLeft = o.pos = w + Math.min(ph, w - 1);
  }
  function settle(o) { var c = o.el.scrollLeft; if (o.foc) return; if (!o.down && c < o.w) o.el.scrollLeft = o.pos = c + o.w; else if (!o.down && c >= 2 * o.w) o.el.scrollLeft = o.pos = c - o.w; else o.pos = c; }
  S.forEach(function (el) {
    var o = { el: el, set: el.firstElementChild, w: 0, pos: 0, until: 0, vis: 1 }, sx, s0, st, mv = 0;
    L.push(o); el.tabIndex = 0; el.classList.add('is-live'); build(o);
    el.addEventListener('scroll', function () { if (o.self) { o.self = 0; return; } hold(o, 2000); clearTimeout(st); st = setTimeout(function () { settle(o); }, 140); }, { passive: true });
    el.addEventListener('touchstart', function () { o.down = 1; }, { passive: true });
    ['touchend', 'touchcancel'].forEach(function (n) { el.addEventListener(n, function () { o.down = 0; hold(o, 2000); }, { passive: true }); });
    el.addEventListener('pointerdown', function (e) { if (e.pointerType == 'mouse' && e.button == 0) { o.down = 1; sx = e.clientX; s0 = el.scrollLeft; mv = 0; } });
    el.addEventListener('pointermove', function (e) {
      if (e.pointerType != 'mouse' || !o.down) return; var d = e.clientX - sx;
      if (!mv && Math.abs(d) > 6) { mv = 1; el.classList.add('is-drag'); el.setPointerCapture(e.pointerId); }
      if (mv) el.scrollLeft = s0 - d;
    });
    ['pointerup', 'pointercancel'].forEach(function (n) { el.addEventListener(n, function (e) { if (e.pointerType != 'mouse') return; o.down = 0; el.classList.remove('is-drag'); if (mv) { hold(o, 2000); setTimeout(function () { mv = 0; }, 0); } else kick(); }); });
    el.addEventListener('dragstart', function (e) { e.preventDefault(); });
    el.addEventListener('click', function (e) { if (mv) { e.preventDefault(); e.stopPropagation(); return; } var a = e.target.closest && e.target.closest('a[data-p]'); if (a) document.dispatchEvent(new CustomEvent('ppc:profile', { detail: a.getAttribute('data-p') })); }, true);
    el.addEventListener('pointerenter', function (e) { if (e.pointerType == 'mouse') o.hov = 1; });
    el.addEventListener('pointerleave', function (e) { if (e.pointerType == 'mouse') { o.hov = 0; kick(); } });
    el.addEventListener('focusin', function (e) {
      try { o.foc = e.target.matches(':focus-visible'); } catch (x) { o.foc = 1; }
      if (e.target == el) return; var r = e.target.getBoundingClientRect(), q = el.getBoundingClientRect();
      if (r.left < q.left + 24) el.scrollLeft -= q.left + 24 - r.left; else if (r.right > q.right - 24) el.scrollLeft += r.right - q.right + 24;
    });
    el.addEventListener('focusout', function () { o.foc = 0; kick(); });
    if (window.IntersectionObserver) new IntersectionObserver(function (e) { o.vis = e[0].isIntersecting; kick(); }).observe(el);
    if (window.ResizeObserver) { var rw = el.clientWidth, rt; new ResizeObserver(function () { if (el.clientWidth == rw) return; rw = el.clientWidth; clearTimeout(rt); rt = setTimeout(function () { build(o); kick(); }, 120); }).observe(el); }
  });
  document.addEventListener('visibilitychange', function () { away = document.hidden; kick(); });
  kick();
})();
