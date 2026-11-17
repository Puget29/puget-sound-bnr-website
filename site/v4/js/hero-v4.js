/* v4 copy of js/hero-v3.js: only the video paths change (the page lives in /v4/), plus a null guard so About and Contact (no hero) run the menu only.
   Original header: Scroll-scrubbed hero + header behaviour for hero v3. Copy of js/hero.js with two changes (marked "v3"):
   1) Safari and iPhone (WebKit) always get the lighter 720 file. In the Playwright check the 1080 file lagged far behind the
      scroll in WebKit (scroll at 85 percent showed the video at 67 percent), so the headline and the picture drifted apart.
   2) The announcement band gets a pause button (WCAG 2.2.2: motion longer than 5 seconds needs a way to stop it).
   hero.js itself is untouched. No dependencies. */
(function () {
  "use strict";

  var hero = document.querySelector(".hero");
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  var menu = document.getElementById("menu");
  var scrim = document.querySelector(".menu-scrim");

  /* ---------- Mobile menu ---------- */
  var menuWasOpen = false;
  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.querySelector(".menu-toggle__label").textContent = open ? "Close" : "Menu";
    menu.classList.toggle("is-open", open);
    if (scrim) scrim.classList.toggle("is-open", open);
    header.classList.toggle("menu-open", open);
    document.documentElement.style.overflow = open ? "hidden" : "";
    /* v3 side panel: the Menu button stays in the header and turns into the cross, so it keeps focus; Escape and links hand it back */
    if (!open && menuWasOpen) toggle.focus({ preventScroll: true });
    menuWasOpen = open;
    if (menu.inert !== undefined) menu.inert = !open;
  }
  if (toggle && menu) {
    setMenu(false);
    toggle.addEventListener("click", function () { setMenu(toggle.getAttribute("aria-expanded") !== "true"); });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    if (scrim) scrim.addEventListener("click", function () { setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key !== "Escape") return;
      var openDrop = document.querySelector(".nav__drop.is-open");
      if (openDrop) { closeDrops(); return; }
      setMenu(false);
    });
    window.matchMedia("(min-width: 901px)").addEventListener("change", function (e) { if (e.matches) setMenu(false); });
  }

  /* ---------- v3: pause button for the announcement band ---------- */
  var banner = document.querySelector(".banner");
  var pause = banner && banner.querySelector(".banner__pause");
  if (pause) {
    pause.addEventListener("click", function () {
      var paused = banner.classList.toggle("is-paused");
      pause.setAttribute("aria-pressed", String(paused));
      pause.setAttribute("aria-label", paused ? "Play announcement" : "Pause announcement");
    });
  }

  function closeDrops() {
    [].forEach.call(document.querySelectorAll(".nav__drop.is-open"), function (drop) {
      drop.classList.remove("is-open");
      var btn = drop.querySelector(".nav__chev");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }
  [].forEach.call(document.querySelectorAll(".nav__chev"), function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var drop = btn.closest(".nav__drop");
      var open = !drop.classList.contains("is-open");
      closeDrops();
      drop.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__drop")) closeDrops(); });
  [].forEach.call(document.querySelectorAll(".menu__chev"), function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".menu__item");
      var open = !item.classList.contains("is-open");
      item.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  if (!hero) return;
  var video = hero.querySelector(".hero__video");
  var cue = hero.querySelector(".hero__cue");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* ---------- Which rendition: chosen once, before any video byte is requested ----------
     The inline script after the <video> (see tools/v4-gen-pages.py) set window.__hero = { d: true } for a wide screen on a decent connection.
     Phones, Save-Data and slow connections get the small file. Only one file is ever downloaded. */
  var HERO = window.__hero || {};
  var conn = navigator.connection || {};
  var wideScreen = HERO.d !== undefined ? HERO.d : (window.innerWidth > 900 && !conn.saveData);
  var FPS = wideScreen ? 30 : 20;                 /* desktop uses the original clip; phones keep the trimmed rendition */
  var SRC = video.getAttribute(wideScreen ? "data-src-d" : "data-src-m");
  var TRIM = wideScreen ? 0 : 1.3333, OLD_DURATION = 18.2333; /* desktop restores the original timeline; phone frames keep the trimmed timeline */
  var DBG = /[?&]perf=1/.test(location.search);
  var dbg = null;
  /* Phones: poster only (no frames, no video) on Save-Data, a slow connection (2g, 3g) or reduced motion. Otherwise the frames load in the background after the page is idle. */
  var posterOnly = !wideScreen && (!!conn.saveData || /(^|-)[23]g$/.test(conn.effectiveType || "") || reduce.matches);
  var useSeq = !wideScreen && !conn.saveData && !!video.getAttribute("data-seq") && !!video.getAttribute("data-seq-index") && "createImageBitmap" in window && "fetch" in window && !/[?&]video=1/.test(location.search);
  var seq = null;     /* phones: the frame sequence (see initSeq), set once it starts */

  var ready = false, target = 0, cur = 0, raf = 0, pending = false, pendAt = 0, inView = true, primed = false, started = false;
  var HOLD = 60;      /* svh of scroll at the end where the video sits on its last frame and the last line stays pinned */
  var vEnd = 0.76;    /* share of the runway used by the video, read from --runway */
  function readEnd() {
    var run = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--runway")) || 250;
    vEnd = Math.max(0.5, (run - HOLD) / run);
  }
  readEnd();
  window.addEventListener("resize", readEnd);
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  function paint(p) {
    if (cue) cue.classList.toggle("is-gone", p > 0.02);
  }

  function runwayProgress() {
    var r = hero.getBoundingClientRect();
    var run = hero.offsetHeight - window.innerHeight;
    return run > 0 ? clamp(-r.top / run, 0, 1) : 0;
  }

  function solidNav() {
    var r = hero.getBoundingClientRect();
    header.classList.toggle("is-solid", r.bottom <= header.offsetHeight + 1);
  }

  /* the end of the buffered range that holds the current time (scrubbing never asks for a frame that has not arrived) */
  function bufferedEnd() {
    var b = video.buffered, t = video.currentTime, end = 0;
    for (var i = 0; i < b.length; i++) { if (b.start(i) <= t + 0.6) end = Math.max(end, b.end(i)); }
    return end;
  }
  function wantedTime() {
    var t = Math.min(1, cur / vEnd) * (OLD_DURATION - 0.05) - TRIM;
    var last = Math.max(0, video.duration - 0.05);
    return clamp(t, 0, Math.min(last, Math.max(0, bufferedEnd() - 0.05)));
  }
  function seek(t) {
    pending = true; pendAt = performance.now();
    if (video.fastSeek) { try { video.fastSeek(t); return; } catch (e) { /* fall through */ } }
    video.currentTime = t;
  }

  var lastFt = 0, avgFt = 16;
  function frame(now) {
    raf = 0;
    if (DBG) { if (lastFt) avgFt += ((now - lastFt) - avgFt) * 0.05; lastFt = now; }
    var d = target - cur;
    cur = Math.abs(d) < 0.0006 ? target : cur + d * (seq ? 0.35 : 0.18); /* a light glide between the jumps a mouse wheel or a flick makes (a sequence can follow closer) */
    var t = 0;
    if (seq) { seq.step(cur); }
    else if (ready && video.readyState >= 2) {
      t = wantedTime();
      if (pending && performance.now() - pendAt > 600) pending = false;           /* a seek that never reported back must not freeze the picture */
      if (!pending && Math.abs(video.currentTime - t) > 1 / FPS) seek(t);          /* one seek at a time, always to the latest target */
    }
    paint(cur);
    if (DBG && dbg && !seq) dbg.update({ rendition: wideScreen ? "hero-d" : "hero-m", fps: FPS, buffered: video.duration ? bufferedEnd() / video.duration : 0, frame: video.currentTime * FPS, target: t * FPS, dt: avgFt });
    if (cur !== target || pending || (seq && seq.busy()) || (!seq && ready && Math.abs(video.currentTime - t) > 1 / FPS)) raf = requestAnimationFrame(frame);
    else lastFt = 0;
  }
  function wake() { if (!raf && inView) raf = requestAnimationFrame(frame); }

  function onScroll() {
    target = runwayProgress();
    solidNav();
    wake();
  }

  /* ---------- Reduced motion: no scrubbing, show the finished house ---------- */
  function applyMotionPreference() {
    var still = reduce.matches;
    hero.classList.toggle("is-static", still);
    if (still) {
      target = cur = 1;
      startVideo();
      if (ready) video.currentTime = Math.max(0, video.duration - 0.05);
      paint(1);
    } else {
      onScroll();
    }
  }

  /* ---------- Phones: a pre-extracted frame sequence drawn on a canvas, instead of seeking a video ----------
     The frames are WebP images packed in one file (assets/hero-seq.bin, coarse frames first) with a small index (hero-seq.json). They download in the background while the
     page is already usable. The picture shown is the loaded frame closest to the wanted one, so scrolling never waits for a seek and never freezes.
     Only a small window of frames is kept decoded in memory. If anything fails, the video path below is used instead. */
  var SEQ_DUR = OLD_DURATION - 0.05 - TRIM;     /* seconds of picture in the sequence, same timeline as the video */
  function initSeq() {
    var canvas = document.createElement("canvas"), ctx = null, attached = false;
    canvas.className = video.className; canvas.setAttribute("aria-hidden", "true");
    var ix = null, blobs = [], bmps = {}, decoding = {}, nb = 0, shown = -1, want = 0, loadedCount = 0, MAXBMP = 24;
    function dead() { seq = null; useSeq = false; started = false; startVideo(); }
    function nearest(list, i) { for (var d = 0; d < ix.n; d++) { if (list[i - d]) return i - d; if (list[i + d]) return i + d; } return -1; }
    function decode(i) {
      if (bmps[i] || decoding[i] || !blobs[i]) return;
      decoding[i] = true;
      createImageBitmap(blobs[i]).then(function (b) { bmps[i] = b; delete decoding[i]; evict(); wake(); }).catch(function () { delete decoding[i]; });
    }
    function evict() {
      var k = Object.keys(bmps); if (k.length <= MAXBMP) return;
      k.sort(function (a, b) { return Math.abs(b - want) - Math.abs(a - want); });
      for (var j = 0; j < k.length - MAXBMP; j++) { try { bmps[k[j]].close(); } catch (e) {} delete bmps[k[j]]; }
    }
    function paintFrame(i) {
      if (!attached) { canvas.width = ix.w; canvas.height = ix.h; video.parentNode.insertBefore(canvas, video.nextSibling); attached = true; }
      ctx.drawImage(bmps[i], 0, 0); shown = i;
      if (video.style.display !== "none") video.style.display = "none"; /* the poster gives way to the first drawn frame */
    }
    function draw() {
      if (!ix) return;
      var best = nearest(blobs, want);
      if (best < 0) return;
      decode(best);
      for (var k = 1; k <= 6; k++) { if (blobs[want + k]) decode(want + k); if (blobs[want - k]) decode(want - k); }   /* frames near the wanted one are decoded ahead of time */
      if (bmps[best]) { if (shown !== best) paintFrame(best); return; }
      var have = []; Object.keys(bmps).forEach(function (k) { have[k] = true; });
      var alt = nearest(have, want);
      if (alt >= 0 && shown !== alt) paintFrame(alt);
    }
    seq = {
      step: function (c) {
        var t = clamp(Math.min(1, c / vEnd) * (OLD_DURATION - 0.05) - TRIM, 0, SEQ_DUR), w = ix ? Math.round(t / SEQ_DUR * (ix.n - 1)) : 0;
        window.__heroP = t / SEQ_DUR;
        if (w !== want) { want = w; window.dispatchEvent(new Event("heroseq")); }
        draw();
        if (DBG) window.__heroState = { shown: shown, want: want, n: ix ? ix.n : 0, loaded: loadedCount };
        if (DBG && dbg) dbg.update({ rendition: "frames", fps: ix ? ix.fps : 0, buffered: ix ? loadedCount / ix.n : 0, frame: shown, target: want, dt: avgFt });
      },
      busy: function () { if (!ix) return false; var best = nearest(blobs, want); return best >= 0 && (!bmps[best] || shown !== best); }
    };
    fetch(video.getAttribute("data-seq-index")).then(function (r) { if (!r.ok) throw new Error("index"); return r.json(); }).then(function (j) {
      ix = j; ctx = canvas.getContext("2d", { alpha: false });
      var total = ix.sizes.reduce(function (a, b) { return a + b; }, 0), buf = new Uint8Array(total), got = 0, offs = [], o = 0;
      ix.sizes.forEach(function (s) { offs.push(o); o += s; });
      blobs = new Array(ix.n);
      function take() {
        while (nb < ix.n && got >= offs[nb] + ix.sizes[nb]) { blobs[ix.order[nb]] = new Blob([buf.slice(offs[nb], offs[nb] + ix.sizes[nb])], { type: "image/webp" }); nb++; loadedCount++; }
        wake();
      }
      return fetch(video.getAttribute("data-seq")).then(function (res) {
        if (!res.ok || !res.body) throw new Error("bin");
        var rd = res.body.getReader();
        return (function pump() { return rd.read().then(function (r) { if (r.done) { take(); return; } buf.set(r.value, got); got += r.value.length; take(); return pump(); }); })();
      });
    }).catch(function () { if (!ix || nb < 1) dead(); });
  }

  /* ---------- Start loading the video after the page has painted: the poster, fonts and CSS get the network first ---------- */
  function startVideo() {
    if (started) return;
    if (!wideScreen && (posterOnly || reduce.matches)) return;   /* the poster stays, nothing more is requested */
    if (useSeq) { started = true; initSeq(); return; }   /* phones: frames, no video file is requested */
    if (!SRC) return;
    started = true;
    video.preload = "auto";
    video.src = SRC;
    video.load();
  }
  if (wideScreen) {
    if (document.readyState === "complete") startVideo(); else window.addEventListener("load", startVideo);
    setTimeout(startVideo, 4000);
  } else if (!posterOnly) {
    /* phones: wait for load, then for an idle moment, then fetch the frames (the poster and headline are already on screen) */
    var kick = function () { if ("requestIdleCallback" in window) requestIdleCallback(startVideo, { timeout: 2500 }); else setTimeout(startVideo, 1500); };
    if (document.readyState === "complete") kick(); else window.addEventListener("load", kick);
  }

  /* some Safari versions draw nothing from seeks until a muted video has played once: start it and pause on the first frame, after the first touch or when ready */
  function prime() {
    if (primed || !ready) return;
    primed = true;
    try { var pr = video.play(); if (pr && pr.then) pr.then(function () { video.pause(); wake(); }).catch(function () {}); else video.pause(); } catch (e) {}
  }
  ["touchstart", "pointerdown", "keydown"].forEach(function (ev) { window.addEventListener(ev, prime, { once: true, passive: true }); });

  video.addEventListener("loadedmetadata", function () {
    ready = true;
    applyMotionPreference();
    wake();
  });
  video.addEventListener("canplay", function () { prime(); wake(); });
  video.addEventListener("progress", wake);        /* more of the file arrived: the picture can catch up */
  video.addEventListener("seeked", function () { pending = false; wake(); });
  video.addEventListener("error", function () { /* poster stays; copy still reads */ });

  /* work only while the hero is on screen */
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { inView = es[0].isIntersecting; if (inView) { onScroll(); } }, { threshold: 0 }).observe(hero);
  }

  window.addEventListener("scroll", function () { if (!reduce.matches) onScroll(); else solidNav(); }, { passive: true });
  window.addEventListener("resize", function () { if (!reduce.matches) onScroll(); else solidNav(); });
  if (reduce.addEventListener) reduce.addEventListener("change", applyMotionPreference);

  /* ---------- dev only: ?perf=1 loads a small overlay for testing on a real phone. Nothing exists in normal use. ---------- */
  if (DBG) {
    var hudSrc = video.getAttribute("data-hud");
    if (hudSrc) { var hs = document.createElement("script"); hs.src = hudSrc; hs.onload = function () { dbg = window.__heroHud && window.__heroHud(video); }; document.head.appendChild(hs); }
  }

  paint(0);
  applyMotionPreference();
  solidNav();

  /* ---------- v3: the header (and the announcement band with it) hides once the hero is behind us ----------
     It comes back when the visitor scrolls up, moves the cursor to the top of the page, tabs into it, or opens the menu. */
  var hdrBanner = document.querySelector(".banner");
  var lastY = window.scrollY, goingUp = false, atTop = false, focusIn = false, hdrRaf = 0;
  function hdrUpdate() {
    hdrRaf = 0;
    var y = window.scrollY, dy = y - lastY;
    if (dy < -2) goingUp = true; else if (dy > 2) goingUp = false;
    lastY = y;
    var pastHero = hero.getBoundingClientRect().bottom <= 0;
    var menuOpen = menu && menu.classList.contains("is-open");
    var show = !pastHero || goingUp || atTop || focusIn || menuOpen;
    header.classList.toggle("is-hidden", !show);
    if (hdrBanner) hdrBanner.classList.toggle("is-hidden", !show);
  }
  function hdrQueue() { if (!hdrRaf) hdrRaf = requestAnimationFrame(hdrUpdate); }
  window.addEventListener("scroll", hdrQueue, { passive: true });
  window.addEventListener("resize", hdrQueue);
  document.addEventListener("mousemove", function (e) { var t = e.clientY <= 90; if (t !== atTop) { atTop = t; hdrQueue(); } }, { passive: true });
  document.documentElement.addEventListener("mouseleave", function () { if (atTop) { atTop = false; hdrQueue(); } });
  header.addEventListener("focusin", function () { focusIn = true; hdrQueue(); });
  header.addEventListener("focusout", function (e) { if (!header.contains(e.relatedTarget)) { focusIn = false; hdrQueue(); } });
  if (toggle) toggle.addEventListener("click", hdrQueue);
  hdrQueue();
})();
