/* Why (#why), Reviews (#reviews) and FAQ (#faq). Vanilla JS, no library. Reviews cycle every 3.5 s. Each effect is switched by a word in the section's data-fx.
   HOW TO ADD A REAL REVIEW: add one object to REVIEWS (name, rating, source and text are needed). Keep the text verbatim.
     { name: "Maria S.", city: "Bellevue", service: "Kitchen", text: "Their words.", source: "google", url: "https://...", date: "2026-10" }
   With REVIEWS empty and DEMO_PLACEHOLDERS true the deck shows clearly marked sample cards. Set DEMO_PLACEHOLDERS to false for launch with no reviews. */
(function () {
  "use strict";
  var DEMO_PLACEHOLDERS = false;
  var REVIEWS = [
    /* the real Google reviews, verbatim from data/reviews.json (featured and verified). No count, no average. */
    {"name": "Paris Goettel", "rating": 5, "source": "google", "text": "I had the pleasure of working with Puget Sound B&R while I was in town for a year visiting my mother-in-law and her husband, and I was able to be involved every step of the way throughout their backyard landscaping and remodeling project, including the addition of a new deck. I was genuinely impressed.\n\nFrom the very beginning, the company operated with professionalism, organization, and clear communication. Every detail was explained thoroughly, timelines were respected, and any questions were addressed promptly. It’s clear that Puget Sound B&R is very well run — the coordination between the team members, scheduling, and execution of the work was seamless.\n\nThe quality of the craftsmanship truly stood out. The landscaping completely transformed the yard, and the new deck was beautifully built and thoughtfully designed to complement the space. Watching the project unfold from start to finish, I could see the care and pride they take in their work.\n\nIt’s not often you come across a company that delivers both exceptional results and an excellent customer experience, but Puget Sound B&R absolutely does. I would highly recommend them to anyone looking for a professional, well-managed team that delivers outstanding work."},
    {"name": "Hong Shi", "rating": 5, "source": "google", "text": "Matt and his crew did my two level deck in the winter of 2024/2025. The deck turned out beautifully with top notch Trex material. Mauro is the master deck builder and very communicative. His helper Jimmy is also very nice. The deck took longer to build as the weather was not great and the day light  was shorter. It’s also partially because Mauro and Jimmy paid attention to every detail. Thank you for a job well done! I look forward to warmer days when I can enjoy the deck.  I highly recommend Matt and his crew."},
    {"name": "Sho Yeh", "rating": 5, "source": "google", "text": "Matt was referred by a friend of mine at work for our remodeling project. Our schedule was very tight for the scope of work due to our rental property end day. Him and his team completed the entire project  with a few unexpected minor issues, they repaired the unexpected and stay on the original schedule. The workmanship is good and Matt/his team always reach out to confirm what we want before they starts. We enjoy the newly remodeled home and appreciate what his team has done for us."}
  ];
  var RATINGS = { google: { score: "", count: "", url: "" }, yelp: { score: "", count: "", url: "" }, angi: { score: "", count: "", url: "" } };
  var EASE = "cubic-bezier(0.2, 0.7, 0.1, 1)";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches, fine = matchMedia("(hover: hover) and (pointer: fine)").matches;
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  function has(sec, k) { return (" " + (sec.getAttribute("data-fx") || "") + " ").indexOf(" " + k + " ") > -1; }
  var why = $("#why"), rv = $("#reviews"), fq = $("#faq");

  /* why: a drawing is dim until its panel crosses the middle of the screen, then it draws and brightens */
  if (why && has(why, "draw") && "IntersectionObserver" in window) {
    var lo = new IntersectionObserver(function (es) {
      es.forEach(function (e) { e.target.classList.toggle("is-lit", e.isIntersecting); if (e.isIntersecting) e.target.classList.add("is-drawn"); });
    }, { rootMargin: "-42% 0px -42% 0px" });
    $$(".why__p", why).forEach(function (p) { lo.observe(p); });
  }

  /* a faint glow follows a fine pointer inside a card or list. Nothing that is clickable moves. */
  if (fine && !reduce) {
    var host = null, mx = 0, my = 0, sraf = 0;
    [why, rv, fq].forEach(function (sec) {
      if (!sec || !has(sec, "spot")) return;
      sec.addEventListener("pointermove", function (e) {
        var h = e.target.closest && e.target.closest("[data-spot]");
        if (host && host !== h) host.classList.remove("is-spot");
        host = h; if (!h) return; mx = e.clientX; my = e.clientY; h.classList.add("is-spot");
        if (!sraf) sraf = requestAnimationFrame(function () { sraf = 0; if (!host) return; var r = host.getBoundingClientRect(); host.style.setProperty("--mx", (mx - r.left) + "px"); host.style.setProperty("--my", (my - r.top) + "px"); });
      });
      sec.addEventListener("pointerleave", function () { if (host) host.classList.remove("is-spot"); host = null; });
    });
  }

  /* reviews: a layered deck. Real cards come only from REVIEWS. */
  if (rv) (function () {
    var deck = $(".rvw__deck", rv), dotsBox = $(".rvw__dots", rv), ctl = $(".rvw__ctl", rv), live = $(".rvw__live", rv), lede = $(".lede", rv);
    if (!deck || !dotsBox) return;   /* a page without the deck markup (About) has nothing to build */
    var data = [], ph = false, cur = 0, cards = [], dots = [];
    REVIEWS.forEach(function (r, i) {
      var miss = ["name", "source", "text"].filter(function (k) { return !r || !r[k]; });
      if (miss.length) console.warn("[reviews] review " + (i + 1) + " is missing: " + miss.join(", "));
      if (r && r.name && r.source && r.text) data.push(r);
    });
    if (!data.length) {
      if (DEMO_PLACEHOLDERS) { ph = true; for (var k = 0; k < 4; k++) data.push({ name: "Client name", city: "City", service: "Service", text: "Your client's words will appear here, in their own voice.", source: "" }); }
      else { rv.classList.add("is-compact"); if (lede) lede.textContent = "Read what homeowners say about us."; return; }
    }
    var n = data.length;
    var GMARK = '<svg class="g-review__google" width="28" height="28" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.09-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.1c-.22-.66-.35-1.36-.35-2.1s.13-1.44.35-2.1V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.27c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 1.99 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>';
    var names = { google: "Google", yelp: "Yelp", angi: "Angi", direct: "Direct" };
    data.forEach(function (r, i) {
      var c = document.createElement("div"); c.className = "rvw__card"; c.setAttribute("role", "group"); c.setAttribute("aria-roledescription", "slide"); c.setAttribute("aria-label", "Review " + (i + 1) + " of " + n);
      c.className = "rvw__card g-review";
      var pal = ["#D2E3FC", "#FCE8E6", "#E6F4EA", "#FEF7E0", "#EDE7F6"], ci = 0, ini = "?", k2;
      for (k2 = 0; k2 < r.name.length; k2++) { ci += (k2 + 1) * r.name.charCodeAt(k2); if (ini === "?" && /[A-Za-z]/.test(r.name.charAt(k2))) ini = r.name.charAt(k2); }
      var rate = Math.max(0, Math.min(5, parseInt(r.rating, 10) || 5)), stars = "";
      for (k2 = 1; k2 <= 5; k2++) stars += k2 <= rate ? "★" : "☆";
      c.innerHTML = '<div class="g-review__head"><div class="g-review__person"><span class="g-review__avatar" aria-hidden="true"></span><div class="g-review__identity"><span class="g-review__name"></span><span class="g-review__src"></span></div></div>' + GMARK + '</div>' +
        '<div class="g-review__stars" role="img" aria-label="' + rate + ' out of 5 stars"></div><div class="g-review__copy"><p class="g-review__text"></p></div>';
      var av = c.querySelector(".g-review__avatar"); av.textContent = ini; av.style.setProperty("--avatar-color", pal[ci % pal.length]);
      c.querySelector(".g-review__name").textContent = r.name; c.querySelector(".g-review__src").textContent = names[r.source] ? "Review on " + names[r.source] : "";
      c.querySelector(".g-review__stars").textContent = stars; c.querySelector(".g-review__text").textContent = r.text;
      deck.appendChild(c); cards.push(c);
      var d = document.createElement("button"); d.type = "button"; d.className = "rvw__dot";
      if (ph) { d.setAttribute("aria-hidden", "true"); d.tabIndex = -1; } else d.setAttribute("aria-label", "Show review " + (i + 1));
      d.addEventListener("click", function () { go(i); }); dotsBox.appendChild(d); dots.push(d);
    });
    if (ph) { deck.setAttribute("aria-hidden", "true"); deck.removeAttribute("tabindex"); dotsBox.setAttribute("aria-hidden", "true"); }

    function draw(prev, dir) {
      cards.forEach(function (c, k) {
        var d = (k - cur + n) % n, pos = d < 3 ? String(d) : "x";
        c.classList.toggle("is-top", d === 0);
        if (!ph) { c.setAttribute("aria-hidden", d === 0 ? "false" : "true"); c.inert = d !== 0; }
        if (prev === null) { c.dataset.pos = pos; return; }
        if (dir < 0 && d === 0 && !reduce) { c.classList.add("no-anim"); c.dataset.pos = "exit"; void c.offsetWidth; requestAnimationFrame(function () { c.classList.remove("no-anim"); c.dataset.pos = "0"; }); }
        else if (dir > 0 && k === prev && !reduce) { c.dataset.pos = "exit"; setTimeout(function () { c.classList.add("no-anim"); c.dataset.pos = pos; void c.offsetWidth; c.classList.remove("no-anim"); }, 640); }
        else c.dataset.pos = pos;
      });
      dots.forEach(function (d, k) { if (k === cur) d.setAttribute("aria-current", "true"); else d.removeAttribute("aria-current"); });
    }
    function go(to) {
      var t = ((to % n) + n) % n; if (t === cur || n < 2) return;
      if (typeof collapseAll === "function") collapseAll();
      var prev = cur, dir = ((t - cur + n) % n) <= n / 2 ? 1 : -1; cur = t; draw(prev, dir);
      if (live && !ph) live.textContent = data[cur].name + ", review " + (cur + 1) + " of " + n;
    }
    /* Read more: a long review is clamped, the button opens the whole text (same behaviour as the PPC cards). The stage height follows the tallest card so the arrows stay centred. */
    var expandedAny = false, stage = $(".rvw__stage", rv);
    function lines(t) { var rg = document.createRange(); rg.selectNodeContents(t); return rg.getClientRects().length; }
    function fit() {
      cards.forEach(function (c) {
        var t = c.querySelector(".g-review__text"), btn = c._more; if (!t) return;
        var open = t.dataset.open === "1";
        t.classList.remove("is-clamped"); t.style.whiteSpace = "normal";
        var long = lines(t) > (matchMedia("(min-width: 700px)").matches ? 6 : 8);
        t.style.whiteSpace = "";
        if (!long) { if (btn) { btn.remove(); c._more = null; } return; }
        if (!btn) {
          btn = document.createElement("button"); btn.type = "button"; btn.className = "g-review__more"; btn.setAttribute("aria-expanded", "false"); btn.textContent = "Read more";
          btn.addEventListener("click", function () {
            var o = t.dataset.open === "1"; t.dataset.open = o ? "0" : "1"; t.classList.toggle("is-clamped", o);
            btn.setAttribute("aria-expanded", o ? "false" : "true"); btn.textContent = o ? "Read more" : "Show less";
            expandedAny = cards.some(function (x) { var y = x.querySelector(".g-review__text"); return y && y.dataset.open === "1"; }); sizeStage();
          });
          c.querySelector(".g-review__copy").appendChild(btn); c._more = btn;
        }
        t.classList.toggle("is-clamped", !open);
      });
      sizeStage();
    }
    function sizeStage() { if (stage) stage.style.setProperty("--dh", deck.offsetHeight + "px"); }
    var rz = 0; window.addEventListener("resize", function () { if (!rz) rz = requestAnimationFrame(function () { rz = 0; fit(); }); }, { passive: true });
    fit(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
    function collapseAll() { cards.forEach(function (c) { var t = c.querySelector(".g-review__text"); if (t && t.dataset.open === "1" && c._more) c._more.click(); }); }
    draw(null, 0);
    if (n < 2 && ctl) ctl.hidden = true;
    $(".rvw__prev", rv).addEventListener("click", function () { go(cur - 1); });
    $(".rvw__next", rv).addEventListener("click", function () { go(cur + 1); });
    deck.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { e.preventDefault(); go(cur + 1); } else if (e.key === "ArrowLeft") { e.preventDefault(); go(cur - 1); } });
    var x0 = null, y0 = 0;
    deck.addEventListener("pointerdown", function (e) { x0 = e.clientX; y0 = e.clientY; });
    deck.addEventListener("pointerup", function (e) { if (x0 === null) return; var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null; if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) go(cur + (dx < 0 ? 1 : -1)); });
    deck.addEventListener("pointercancel", function () { x0 = null; });
    /* auto cycle every 3.5 s (same as the PPC pages): only with real reviews, paused while touched, hovered, focused, expanded, hidden or off screen; a manual move waits 10 s */
    if (!ph && n > 1 && !reduce) {
      var held = false, seen = false, idle = 0, bump = function () { idle = Date.now() + 10000; };
      ["pointerdown", "keydown"].forEach(function (ev) { deck.addEventListener(ev, bump); });
      ctl.addEventListener("click", bump);
      deck.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") held = true; });
      deck.addEventListener("pointerleave", function (e) { if (e.pointerType === "mouse") held = false; });
      deck.addEventListener("focusin", function () { held = true; });
      deck.addEventListener("focusout", function () { held = false; });
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { seen = es[0].isIntersecting; }, { threshold: 0.4 }).observe(deck); else seen = true;
      ["touchstart", "touchend"].forEach(function (ev) { deck.addEventListener(ev, bump, { passive: true }); });
      setInterval(function () { if (seen && !held && !expandedAny && !document.hidden && Date.now() >= idle) go(cur + 1); }, 3500);
    }
  })();

  /* faq: native details, one row open at a time, opened and closed with a FLIP animation.
     The new layout is applied at once, then every row slides from where it was to where it is (transform only), the new answer is revealed with a clip, and the answer that is closing
     is kept as a clipped copy until it has gone. Only transform, clip-path and opacity change while it runs, so it stays smooth on a phone (no layout or paint work per frame). */
  if (fq) {
    var rows = $$("details.fq__row", fq).filter(function (r) { return !r.hidden; });
    var list = $(".fq__list", fq), DUR = 440, EASE2 = "cubic-bezier(0.4, 0, 0.2, 1)", ghosts = [];
    rows.forEach(function (r) { r.removeAttribute("name"); r._w = r.open; });
    var cancelAll = function () {
      ghosts.forEach(function (g) { if (g.parentNode) g.parentNode.removeChild(g); }); ghosts = [];
      rows.forEach(function (x) { x.getAnimations({ subtree: true }).forEach(function (a) { if (a.effect && a.effect.target && !(a instanceof CSSTransition)) a.cancel(); }); });
    };
    var toggle = function (r) {
      var opening = !r._w;
      var closing = rows.filter(function (x) { return x._w && (opening ? x !== r : x === r); });
      if (reduce) { closing.forEach(function (x) { x._w = false; x.open = false; }); if (opening) { r._w = true; r.open = true; } return; }
      /* where everything is right now, as the visitor sees it (a running animation counts) */
      var old = rows.map(function (x) { return x.getBoundingClientRect().top; });
      var lr = list.getBoundingClientRect();
      var gone = closing.map(function (x) { var a = $(".fq__a", x), ar = a.getBoundingClientRect(); return { html: a.innerHTML, top: ar.top - lr.top, h: ar.height }; });
      cancelAll();
      closing.forEach(function (x) { x._w = false; x.open = false; });
      if (opening) { r._w = true; r.open = true; }
      var nw = rows.map(function (x) { return x.getBoundingClientRect().top; });
      rows.forEach(function (x, i) {
        var d = old[i] - nw[i];
        if (Math.abs(d) > 0.5) x.animate([{ transform: "translateY(" + d + "px)" }, { transform: "none" }], { duration: DUR, easing: EASE2 });
      });
      gone.forEach(function (g) {
        var el = document.createElement("div"); el.className = "fq__a fq__ghost"; el.setAttribute("aria-hidden", "true"); el.innerHTML = g.html;
        el.style.cssText = "position:absolute;left:0;right:0;z-index:1;pointer-events:none;top:" + g.top + "px;height:" + g.h + "px";
        list.appendChild(el); ghosts.push(el);
        el.animate([{ clipPath: "inset(0 0 0 0)", opacity: 1 }, { clipPath: "inset(0 0 " + g.h + "px 0)", opacity: 0 }], { duration: DUR, easing: EASE2 }).onfinish = function () { if (el.parentNode) el.parentNode.removeChild(el); };
      });
      if (opening) {
        var a = $(".fq__a", r), h = a.getBoundingClientRect().height;
        r.animate([{ clipPath: "inset(0 0 " + h + "px 0)" }, { clipPath: "inset(0 0 0 0)" }], { duration: DUR, easing: EASE2 });
        a.firstElementChild.animate([{ opacity: 0 }, { opacity: 1 }], { duration: DUR * 0.7, delay: DUR * 0.2, easing: EASE2, fill: "backwards" });
        r.classList.remove("is-sheen"); void r.offsetWidth; r.classList.add("is-sheen"); /* one quick sheen across the hairline */
        setTimeout(function () { r.classList.remove("is-sheen"); }, 700);
      }
    };
    rows.forEach(function (r) {
      $("summary", r).addEventListener("click", function (e) { e.preventDefault(); toggle(r); });
    });
  }
  /* work rail (#work): sideways scroll with snap, arrows on desktop. Photos only, no autoplay. */
  var wk = $("#work");
  if (wk) (function () {
    var rail = $(".work__rail", wk), prev = $(".work__prev", wk), next = $(".work__next", wk), first = rail && $(".work__c", rail);
    if (!rail || !first) return;
    function step() { return (first.getBoundingClientRect().width + 18) * 2; }
    function upd() { var max = rail.scrollWidth - rail.clientWidth - 2; if (prev) prev.disabled = rail.scrollLeft <= 2; if (next) next.disabled = rail.scrollLeft >= max; }
    if (prev) prev.addEventListener("click", function () { rail.scrollBy({ left: -step(), behavior: reduce ? "auto" : "smooth" }); });
    if (next) next.addEventListener("click", function () { rail.scrollBy({ left: step(), behavior: reduce ? "auto" : "smooth" }); });
    rail.addEventListener("scroll", function () { requestAnimationFrame(upd); }, { passive: true });
    rail.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") { e.preventDefault(); rail.scrollBy({ left: step() / 2, behavior: "auto" }); } else if (e.key === "ArrowLeft") { e.preventDefault(); rail.scrollBy({ left: -step() / 2, behavior: "auto" }); } });
    window.addEventListener("resize", upd, { passive: true }); upd();
  })();
})();
