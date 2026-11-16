/* Projects page: service filter and photo lightbox. Does nothing when [data-pj] is absent.
   Without script all photos show and every tile is a plain link to the large photo. Filter moves use only opacity and transform (FLIP).
   Reduced motion: instant. The lightbox shows the service name only. */
(function () {
  "use strict";
  var grid = document.querySelector("[data-pj]"); if (!grid) return;
  var items = [].slice.call(grid.children), bar = document.querySelector(".pj__bar"), empty = document.querySelector(".pj__empty");
  var status = document.querySelector(".pj__status"), chips = [].slice.call(document.querySelectorAll("[data-f]"));
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches, cur = "all", token = 0;
  var can = typeof Element !== "undefined" && Element.prototype.animate;
  var NAMES = { all: "all", kitchen: "kitchen", bathroom: "bathroom", adu: "ADU", roofing: "roofing", deck: "deck" };
  if (bar) bar.hidden = false;

  /* bento layout: rows of three, a large tile in every second group, the last row stretched so no row is ragged (6 column grid, 2 columns on phones) */
  function layout() {
    var vis = items.filter(function (li) { return !li.hidden; }), n = vis.length, mob = matchMedia("(max-width: 699px)").matches, i, g = 0;
    items.forEach(function (li) { li.removeAttribute("data-l"); });
    if (mob) { if (n > 1 && n % 2 === 1) vis[n - 1].setAttribute("data-l", "w"); return; }
    var full = Math.floor(n / 3) * 3;
    for (i = 0; i < full; i += 3, g++) {
      if (n >= 9 && g % 2 === 1) vis[g % 4 === 1 ? i + 1 : i].setAttribute("data-l", "f");
    }
    if (n - full === 1) vis[n - 1].setAttribute("data-l", "w");
    else if (n - full === 2) { vis[n - 2].setAttribute("data-l", "h"); vis[n - 1].setAttribute("data-l", "h"); }
  }
  function match(li, f) { return f === "all" || li.getAttribute("data-svc") === f; }
  function settle(f) {
    var n = 0;
    items.forEach(function (li) { var m = match(li, f); li.hidden = !m; if (m) { n++; li.classList.add("sx-in"); } });
    layout(); ui(f, n);
  }
  function ui(f, n) {
    chips.forEach(function (c) { if (c.hasAttribute("aria-pressed")) c.setAttribute("aria-pressed", c.getAttribute("data-f") === f ? "true" : "false"); });
    if (empty) empty.hidden = n > 0;
    if (status) status.textContent = n ? "Showing " + n + (f === "all" ? " photos" : " " + NAMES[f] + " photos") + "." : "No photos in this category yet.";
  }
  function rects(list) { return list.map(function (li) { return li.getBoundingClientRect(); }); }

  function apply(f) {
    if (f === cur) return;
    var prev = cur; cur = f; var my = ++token;
    items.forEach(function (li) { if (li.getAnimations) li.getAnimations().forEach(function (a) { a.cancel(); }); });
    if (reduce || !can) { settle(f); return; }
    var vis = items.filter(function (li) { return !li.hidden; });
    var leaving = vis.filter(function (li) { return !match(li, f); });
    var staying = vis.filter(function (li) { return match(li, f); });
    var entering = items.filter(function (li) { return li.hidden && match(li, f); });
    ui(f, staying.length + entering.length);
    function swap() {
      if (my !== token) return;
      var first = rects(staying);
      leaving.forEach(function (li) { li.hidden = true; });
      entering.forEach(function (li) { li.hidden = false; li.classList.add("sx-in"); });
      layout();
      var last = rects(staying), eo = 0;
      staying.forEach(function (li, i) {
        var dx = first[i].left - last[i].left, dy = first[i].top - last[i].top;
        if (dx || dy) li.animate([{ transform: "translate(" + dx + "px," + dy + "px)" }, { transform: "none" }], { duration: 420, easing: "cubic-bezier(0.2,0.7,0.1,1)" });
      });
      entering.forEach(function (li) {
        li.animate([{ opacity: 0, transform: "translateY(14px) scale(0.96)" }, { opacity: 1, transform: "none" }], { duration: 480, delay: Math.min(eo++, 12) * 30, easing: "cubic-bezier(0.2,0.7,0.1,1)", fill: "backwards" });
      });
    }
    if (!leaving.length) { swap(); return; }
    var done = 0;
    leaving.forEach(function (li) {
      var a = li.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "scale(0.96)" }], { duration: 170, easing: "ease-out", fill: "forwards" });
      a.onfinish = a.oncancel = function () { if (++done === leaving.length) swap(); };
    });
  }

  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.getAttribute("data-f"); apply(f);
      try { history.replaceState(null, "", f === "all" ? location.pathname + location.search : "#" + f); } catch (e) {}
    });
  });
  var h = (location.hash || "").slice(1);
  if (NAMES[h] && h !== "all") { cur = "all"; settle(h); cur = h; } else { layout(); ui("all", items.length); }
  var mq = matchMedia("(max-width: 699px)"); (mq.addEventListener ? mq.addEventListener("change", layout) : mq.addListener(layout));

  /* ---------- lightbox over the photos that are visible ---------- */
  if (typeof HTMLDialogElement === "undefined" || !document.createElement("dialog").showModal) return;
  var dlg, img, count, cap, closeB, prevB, nextB, idx = 0, opener = null, tx = 0, ty = 0, links = [];
  var ico = function (d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; };
  function build() {
    dlg = document.createElement("dialog"); dlg.className = "lb"; dlg.setAttribute("aria-label", "Project photos");
    dlg.innerHTML = '<button type="button" class="lb__btn lb__close" aria-label="Close">' + ico("M6 6l12 12M18 6L6 18") + "</button>" +
      '<div class="lb__stage"><img class="lb__img" alt=""></div>' +
      '<button type="button" class="lb__btn lb__prev" aria-label="Previous photo">' + ico("M15 5l-7 7 7 7") + "</button>" +
      '<button type="button" class="lb__btn lb__next" aria-label="Next photo">' + ico("M9 5l7 7-7 7") + "</button>" +
      '<p class="lb__count" aria-live="polite"><span class="lb__cap"></span><span class="lb__num"></span></p>';
    document.body.appendChild(dlg);
    img = dlg.querySelector(".lb__img"); count = dlg.querySelector(".lb__num"); cap = dlg.querySelector(".lb__cap");
    closeB = dlg.querySelector(".lb__close"); prevB = dlg.querySelector(".lb__prev"); nextB = dlg.querySelector(".lb__next");
    closeB.addEventListener("click", function () { dlg.close(); });
    prevB.addEventListener("click", function () { show(idx - 1); });
    nextB.addEventListener("click", function () { show(idx + 1); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.className === "lb__stage") dlg.close(); });
    dlg.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); show(idx - 1); }
      else if (e.key === "ArrowRight") { e.preventDefault(); show(idx + 1); }
      else if (e.key === "Tab") { var f = [closeB, prevB, nextB], i = f.indexOf(document.activeElement); e.preventDefault(); f[(i + (e.shiftKey ? f.length - 1 : 1)) % f.length].focus(); }
    });
    dlg.addEventListener("touchstart", function (e) { var t = e.changedTouches[0]; tx = t.clientX; ty = t.clientY; }, { passive: true });
    dlg.addEventListener("touchend", function (e) {
      var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(idx + (dx < 0 ? 1 : -1));
    }, { passive: true });
    dlg.addEventListener("close", function () { document.documentElement.style.overflow = ""; if (opener && opener.focus) opener.focus(); });
  }
  function show(i) {
    idx = (i + links.length) % links.length;
    var a = links[idx], im = a.querySelector("img");
    img.sizes = "100vw"; img.srcset = a.getAttribute("data-srcset") || ""; img.src = a.getAttribute("href"); img.alt = im ? im.alt : "";
    cap.textContent = a.getAttribute("data-name") || ""; count.textContent = (idx + 1) + " of " + links.length;
    [idx + 1, idx - 1].forEach(function (n) { var p = new Image(); p.src = links[(n + links.length) % links.length].getAttribute("href"); });
  }
  grid.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".pj__a"); if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
    e.preventDefault(); if (!dlg) build();
    links = items.filter(function (li) { return !li.hidden; }).map(function (li) { return li.querySelector(".pj__a"); });
    opener = a; show(links.indexOf(a)); document.documentElement.style.overflow = "hidden"; dlg.showModal(); closeB.focus();
  });
})();
