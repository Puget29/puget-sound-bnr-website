/* Service pages: gallery Show more, dialog lightbox, review Read more. Each part does nothing when its markup is absent.
   Without script the gallery tiles are plain links to the large photo and the reviews show in full. */
(function () {
  "use strict";
  /* ---------- gallery: Show more (more than 6 photos) and a native dialog lightbox ---------- */
  (function () {
    var gal = document.querySelector("[data-gal]"); if (!gal) return;
    var links = [].slice.call(gal.querySelectorAll(".gal__a")); if (!links.length) return;
    gal.classList.add("is-js");
    var more = gal.querySelector(".gal__more");
    if (more && links.length > 6) {
      more.hidden = false;
      more.addEventListener("click", function () {
        var open = gal.classList.toggle("is-open");
        more.setAttribute("aria-expanded", open ? "true" : "false");
        more.textContent = open ? "Show less" : "Show more";
      });
    }
    if (typeof HTMLDialogElement === "undefined" || !document.createElement("dialog").showModal) return;
    var dlg, img, count, closeB, prevB, nextB, idx = 0, opener = null, tx = 0, ty = 0;
    var ico = function (d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; };
    function build() {
      dlg = document.createElement("dialog"); dlg.className = "lb"; dlg.setAttribute("aria-label", "Project photos");
      dlg.innerHTML = '<button type="button" class="lb__btn lb__close" aria-label="Close">' + ico("M6 6l12 12M18 6L6 18") + "</button>" +
        '<div class="lb__stage"><img class="lb__img" alt=""></div>' +
        '<button type="button" class="lb__btn lb__prev" aria-label="Previous photo">' + ico("M15 5l-7 7 7 7") + "</button>" +
        '<button type="button" class="lb__btn lb__next" aria-label="Next photo">' + ico("M9 5l7 7-7 7") + "</button>" +
        '<p class="lb__count" aria-live="polite"></p>';
      document.body.appendChild(dlg);
      img = dlg.querySelector(".lb__img"); count = dlg.querySelector(".lb__count");
      closeB = dlg.querySelector(".lb__close"); prevB = dlg.querySelector(".lb__prev"); nextB = dlg.querySelector(".lb__next");
      closeB.addEventListener("click", function () { dlg.close(); });
      prevB.addEventListener("click", function () { show(idx - 1); });
      nextB.addEventListener("click", function () { show(idx + 1); });
      dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.className === "lb__stage") dlg.close(); });
      dlg.addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { e.preventDefault(); show(idx - 1); }
        else if (e.key === "ArrowRight") { e.preventDefault(); show(idx + 1); }
        else if (e.key === "Tab") {
          var f = [closeB, prevB, nextB], i = f.indexOf(document.activeElement);
          e.preventDefault(); f[(i + (e.shiftKey ? f.length - 1 : 1)) % f.length].focus();
        }
      });
      dlg.addEventListener("touchstart", function (e) { var t = e.changedTouches[0]; tx = t.clientX; ty = t.clientY; }, { passive: true });
      dlg.addEventListener("touchend", function (e) {
        var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty;
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(idx + (dx < 0 ? 1 : -1));
      }, { passive: true });
      dlg.addEventListener("close", function () {
        document.documentElement.style.overflow = "";
        if (opener && opener.focus) opener.focus();
      });
    }
    function show(i) {
      idx = (i + links.length) % links.length;
      var a = links[idx], im = a.querySelector("img");
      img.sizes = "100vw"; img.srcset = a.getAttribute("data-srcset") || ""; img.src = a.getAttribute("href"); img.alt = im ? im.alt : "";
      count.textContent = (idx + 1) + " of " + links.length;
      [idx + 1, idx - 1].forEach(function (n) { var p = new Image(); p.src = links[(n + links.length) % links.length].getAttribute("href"); });
    }
    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey) return;
        e.preventDefault(); if (!dlg) build();
        opener = a; show(i); document.documentElement.style.overflow = "hidden"; dlg.showModal(); closeB.focus();
      });
    });
  })();

  /* ---------- reviews: long text is cut to a few lines, Read more shows all of it ---------- */
  [].slice.call(document.querySelectorAll(".sv-rev")).forEach(function (card) {
    var t = card.querySelector("[data-clamp]"), b = card.querySelector(".sv-rev__more"); if (!t || !b) return;
    t.classList.add("is-clamped");
    if (t.scrollHeight <= t.clientHeight + 2) { t.classList.remove("is-clamped"); return; }
    b.hidden = false;
    b.addEventListener("click", function () {
      var open = t.classList.toggle("is-clamped") === false;
      b.setAttribute("aria-expanded", open ? "true" : "false");
      b.textContent = open ? "Show less" : "Read more";
    });
  });
})();
