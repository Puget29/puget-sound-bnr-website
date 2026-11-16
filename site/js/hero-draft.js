/* Hero draft only. Scroll cue: idle shimmer at the top, scroll progress once the visitor scrolls.
   Reads the same runway progress as hero.js but never touches its state. */
(function () {
  "use strict";
  var hero = document.querySelector(".hero");
  var cue = hero && hero.querySelector(".hero__cue");
  if (!cue) return;

  var raf = 0;
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  function update() {
    raf = 0;
    var r = hero.getBoundingClientRect();
    var run = hero.offsetHeight - window.innerHeight;
    var p = run > 0 ? clamp(-r.top / run, 0, 1) : 0;
    cue.style.setProperty("--p", p.toFixed(3));
    cue.classList.toggle("is-scrolling", p > 0.015);
  }
  function queue() { if (!raf) raf = requestAnimationFrame(update); }

  window.addEventListener("scroll", queue, { passive: true });
  window.addEventListener("resize", queue);
  update();
})();
