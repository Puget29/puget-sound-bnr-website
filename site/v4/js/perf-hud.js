/* Dev only. Loaded by hero-v4.js when the address has ?perf=1, so it costs nothing in normal use (no markup, no script request).
   Shows which hero file was chosen, how much of it has arrived, the frame on screen against the frame wanted, the lag, and the average frame time.
   Use it on a real phone: open the page with ?perf=1 and scroll through the hero. */
(function () {
  "use strict";
  window.__heroHud = function (video) {
    var el = document.createElement("pre");
    el.setAttribute("aria-hidden", "true");
    el.style.cssText = "position:fixed;left:8px;bottom:8px;z-index:99999;margin:0;padding:8px 10px;background:rgba(0,0,0,.78);color:#e6cf86;font:12px/1.4 ui-monospace,Menlo,Consolas,monospace;border-radius:6px;pointer-events:none;white-space:pre";
    document.body.appendChild(el);
    var last = 0;
    return {
      update: function (s) {
        var now = performance.now(); if (now - last < 120) return; last = now;
        var lag = Math.abs(s.frame - s.target);
        el.textContent = "file     " + s.rendition + " (" + s.fps + " fps)\nbuffered " + Math.round(s.buffered * 100) + "%\nframe    " + s.frame.toFixed(1) + "\ntarget   " + s.target.toFixed(1) + "\nlag      " + lag.toFixed(1) + " frames\nframe ms " + s.dt.toFixed(1) + (video.seeking ? "\nseeking" : "");
      }
    };
  };
})();
