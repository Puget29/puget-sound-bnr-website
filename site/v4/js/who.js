/* "Who we are" (#who): fills the photo slot from one config and draws the slot corners when it comes into view. Vanilla JS, no library.
   TO ADD A PHOTO: fill the entry below (src is the minimum, alt is required). No markup edit.
     { slot: 'who-1', src: 'assets/who-1.webp', alt: 'Describe the photo', focus: '50% 40%' }
   Optional: srcset (webp widths), avif (avif srcset), width, height (the file's real size), caption. */
(function () {
  "use strict";
  var WHO_PHOTOS = [
    { slot: "who-1", src: "/assets/projects/project-01-960.webp", srcset: "/assets/projects/project-01-640.webp 640w, /assets/projects/project-01-960.webp 960w", avif: "", width: 960, height: 640, alt: "Kitchen with white cabinets, a butcher block island and wood floors", focus: "50% 50%", caption: "" }
  ];
  var SIZES = "(min-width: 901px) 40vw, 92vw";

  WHO_PHOTOS.forEach(function (e) {
    var fig = document.querySelector('.pslot[data-slot="' + e.slot + '"]');
    if (!fig || !e.src) return;
    if (!e.alt) console.warn("[who] slot " + e.slot + " has a photo but no alt text. Add alt in WHO_PHOTOS.");
    var pic = document.createElement("picture"), img = new Image();
    pic.className = "pslot__img";
    if (e.avif) { var s = document.createElement("source"); s.type = "image/avif"; s.srcset = e.avif; s.sizes = SIZES; pic.appendChild(s); }
    img.src = e.src; if (e.srcset) img.srcset = e.srcset;
    img.sizes = SIZES; img.alt = e.alt || ""; img.width = e.width; img.height = e.height;
    img.loading = "lazy"; img.decoding = "async"; img.style.objectPosition = e.focus || "50% 50%";
    pic.appendChild(img);
    if (e.caption) { var c = document.createElement("figcaption"); c.textContent = e.caption; pic.appendChild(c); }
    fig.appendChild(pic); fig.classList.add("is-filled");
    requestAnimationFrame(function () { pic.classList.add("is-on"); });
  });

  var slots = [].slice.call(document.querySelectorAll(".pslot"));
  if (!("IntersectionObserver" in window)) { slots.forEach(function (f) { f.classList.add("is-draw"); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-draw"); io.unobserve(en.target); } });
  }, { threshold: 0.2 });
  slots.forEach(function (f) { io.observe(f); });
})();
