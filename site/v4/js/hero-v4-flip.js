/* Scroll-driven headline for hero v3 (FlipText effect). Copy of js/hero-flip.js with two changes (marked "v3"):
   1) The stage is chosen from the VIDEO's current time, not from the scroll position. The picture eases toward the scroll and
      can lag it (a lot in WebKit), so a scroll-based headline could show "Finished, down to the details." over a blueprint.
      Using the video time keeps the words and the frame together. Falls back to scroll progress until the video is ready.
   2) The hero gets an is-final class at the last stage, which reveals the proof line.
   The real <h1> stays in the page as the static heading; the animated text is an aria-hidden visual layer.
   Not run for reduced motion (the hero then shows the finished frame and the plain h1). */
(function () {
  "use strict";
  var hero = document.querySelector(".hero");
  var box = hero && hero.querySelector(".hero__flip");
  var h1 = hero && hero.querySelector("h1");
  var video = hero && hero.querySelector(".hero__video");
  if (!box || !h1) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) { hero.classList.add("is-final"); return; } /* v3: finished frame, so show the proof line too */

  var DURATION = 0.9;
  var HYST = 0.012;
  /* Desktop restores the original stage fractions. Phone fractions remain converted for the trimmed video and frame sequence. */
  var originalDesktop = !!(window.__hero && window.__hero.d);
  var STAGES = [             /* at = fraction of the video (current time / duration) */
    { at: 0.00, text: "Every home starts as a sketch." },       /* floor plan blueprint */
    { at: originalDesktop ? 0.20 : 0.137, text: "Planned around how you live." }, /* wireframe house */
    { at: originalDesktop ? 0.45 : 0.407, text: "Built with care." }, /* wireframe turns into real materials */
    { at: originalDesktop ? 0.66 : 0.633, text: "Finished, down to the details." }, /* nearly finished house */
    { at: originalDesktop ? 0.90 : 0.892, text: h1.textContent.replace(/\s+/g, " ").trim() } /* the final line, same text as the h1 */
  ];

  var current = null, idx = -1, started = false, raf = 0;

  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function scrollProgress() {
    var r = hero.getBoundingClientRect();
    var run = hero.offsetHeight - window.innerHeight;
    return run > 0 ? clamp(-r.top / run, 0, 1) : 0;
  }
  function progress() { /* v3: what the visitor actually sees (video time), else the scroll position */
    if (typeof window.__heroP === "number") return window.__heroP; /* phones: the frame sequence sets this */
    if (video && video.readyState >= 1 && video.duration > 0.1) {
      return clamp(video.currentTime / Math.max(0.1, video.duration - 0.05), 0, 1);
    }
    return scrollProgress();
  }
  function stageFor(p) {
    var i = 0;
    for (var k = 0; k < STAGES.length; k++) if (p >= STAGES[k].at) i = k;
    return i;
  }

  function buildLayer(text) {
    var layer = document.createElement("div");
    layer.className = "fl";
    var words = text.split(" "), total = text.length, n = 0;
    words.forEach(function (w, wi) {
      var word = document.createElement("span");
      word.className = "fw";
      for (var c = 0; c < w.length; c++) {
        var ch = document.createElement("span");
        ch.className = "fc";
        ch.textContent = w.charAt(c);
        ch.style.setProperty("--d", (Math.sin((n / total) * (Math.PI / 2)) * (DURATION * 0.25)).toFixed(3) + "s");
        word.appendChild(ch);
        n++;
      }
      n++;
      layer.appendChild(word);
      if (wi < words.length - 1) layer.appendChild(document.createTextNode(" "));
    });
    return layer;
  }

  function show(i, dir) {
    var next = buildLayer(STAGES[i].text);
    next.classList.add("is-in");
    next.style.setProperty("--dir", dir);
    box.appendChild(next);
    if (current) {
      var old = current;
      old.classList.remove("is-in");
      old.classList.add("is-out");
      old.style.setProperty("--dir", dir);
      setTimeout(function () { if (old.parentNode) old.parentNode.removeChild(old); }, 800);
    }
    while (box.children.length > 3) box.removeChild(box.firstChild);
    current = next;
    idx = i;
    hero.classList.toggle("is-final", i === STAGES.length - 1); /* v3 */
  }

  function update() {
    raf = 0;
    if (!started) return;
    var p = progress();
    var want = stageFor(p);
    if (want === idx) return;
    var boundary = STAGES[Math.max(want, idx)].at;
    if (Math.abs(p - boundary) < HYST) return;
    show(want, want > idx ? 1 : -1);
  }
  function queue() { if (!raf) raf = requestAnimationFrame(update); }

  hero.classList.add("has-flip"); /* hides the plain h1 right away, the box stays empty until start() */

  function start() {
    if (started) return;
    started = true;
    show(stageFor(progress()), 1);
  }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue);
  window.addEventListener("heroseq", queue);
  if (video) { /* v3: follow the picture as it seeks, not only the scroll events */
    video.addEventListener("seeked", queue);
    video.addEventListener("timeupdate", queue);
    video.addEventListener("loadedmetadata", queue);
  }

  start(); /* the page opens straight to the hero, nothing to wait for */
})();
