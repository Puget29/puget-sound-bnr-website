/* Services (#services): image carousel. Vanilla JS, no library, no autoplay.
   TO ADD A PHOTO: fill the entry in SERVICE_PHOTOS (src and alt are required, focus is the crop point). No markup edit.
   TO LINK A CARD TO A REAL SERVICE PAGE: change its line in SERVICE_LINKS (each card also carries its future route in data-page). */
(function () {
  "use strict";
  var P = { src: "", srcset: "", avif: "", width: 1200, height: 1500, alt: "", focus: "50% 50%" };
  var SERVICE_PHOTOS = {
    adu: { src: "/assets/projects/project-13-960.webp", srcset: "/assets/projects/project-13-640.webp 640w, /assets/projects/project-13-960.webp 960w", avif: "", width: 960, height: 538, alt: "Two story house with wood framing at a construction site", focus: "50% 50%" },
    kitchen: { src: "/assets/projects/project-01-960.webp", srcset: "/assets/projects/project-01-640.webp 640w, /assets/projects/project-01-960.webp 960w", avif: "", width: 960, height: 640, alt: "Kitchen with white cabinets, a butcher block island and wood floors", focus: "50% 50%" },
    bathroom: { src: "/assets/projects/project-07-960.webp", srcset: "/assets/projects/project-07-640.webp 640w, /assets/projects/project-07-960.webp 960w", avif: "", width: 960, height: 1440, alt: "Bathroom with a tiled glass shower and a white vanity", focus: "50% 55%" },
    roofing: { src: "/assets/projects/project-05-960.webp", srcset: "/assets/projects/project-05-640.webp 640w, /assets/projects/project-05-960.webp 960w", avif: "", width: 960, height: 720, alt: "Roof and upper windows of a two story home seen from above", focus: "50% 50%" },
    deck: { src: "/assets/projects/project-10-960.webp", srcset: "/assets/projects/project-10-640.webp 640w, /assets/projects/project-10-960.webp 960w", avif: "", width: 960, height: 960, alt: "Deck with two black rocking chairs and a metal railing overlooking hills", focus: "50% 62%" },
    flooring: { src: "/assets/projects/project-12-960.webp", srcset: "/assets/projects/project-12-640.webp 640w, /assets/projects/project-12-960.webp 960w", avif: "", width: 960, height: 540, alt: "Close up of light wood flooring planks", focus: "50% 50%" },
    painting: { src: "/assets/projects/painting-card-960.webp", srcset: "/assets/projects/painting-card-640.webp 640w, /assets/projects/painting-card-960.webp 960w", avif: "", width: 960, height: 1200, alt: "Painter rolling a fresh coat of paint on an interior wall", focus: "50% 50%" },
    siding: { src: "/assets/projects/project-14-960.webp", srcset: "/assets/projects/project-14-612.webp 612w, /assets/projects/project-14-960.webp 960w", avif: "", width: 612, height: 459, alt: "Blue house siding with a white corner post", focus: "80% 50%" }
  };
  var SERVICE_LINKS = { roofing: "/our-services/roofing/", kitchen: "/our-services/kitchen-remodeling/", bathroom: "/our-services/bathroom-remodeling/", adu: "/our-services/adu-garage-conversion/", deck: "/our-services/deck-building/", siding: "/siding-replacement/", flooring: "/our-services/floor-replacement/", painting: "/our-services/painting/" };
  var sec = document.getElementById("services");
  if (!sec) return;
  var car = sec.querySelector(".car"), track = sec.querySelector(".car__track");
  var items = [].slice.call(sec.querySelectorAll(".car__item")), n = items.length;
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches, wide = matchMedia("(min-width: 900px)");
  var i = 0, stage = false, dragged = false, live = sec.querySelector(".car__live");
  if (/[?&]contrast=1/.test(location.search)) car.classList.add("car--contrast");

  items.forEach(function (li) {
    var k = li.getAttribute("data-svc"), a = li.querySelector(".car__card");
    if (SERVICE_LINKS[k]) a.setAttribute("href", SERVICE_LINKS[k]);
    var e = SERVICE_PHOTOS[k], fig = li.querySelector(".pslot");
    if (!e || !e.src) return;
    if (!e.alt) console.warn("[services] slot svc-" + k + " has a photo but no alt text. Add alt in SERVICE_PHOTOS.");
    var pic = document.createElement("picture"), img = new Image(), sz = "(min-width: 900px) 27vw, 78vw";
    pic.className = "pslot__img";
    if (e.avif) { var s = document.createElement("source"); s.type = "image/avif"; s.srcset = e.avif; s.sizes = sz; pic.appendChild(s); }
    img.src = e.src; if (e.srcset) img.srcset = e.srcset;
    img.sizes = sz; img.alt = e.alt || ""; img.width = e.width; img.height = e.height; img.loading = "lazy"; img.decoding = "async"; img.draggable = false;
    img.style.objectPosition = e.focus || "50% 50%";
    pic.appendChild(img); fig.appendChild(pic); fig.classList.add("is-filled");
    requestAnimationFrame(function () { pic.classList.add("is-on"); });
  });

  function meta(say) {
    car.querySelector(".car__fill").style.transform = "scaleX(" + ((i + 1) / n) + ")";
    if (say && live) live.textContent = items[i].getAttribute("aria-label");
  }
  function draw(say) {
    items.forEach(function (li, k) {
      var d = ((k - i) % n + n) % n; if (d > 3) d -= n;
      var c = Math.max(-2, Math.min(2, d)), old = +li.getAttribute("data-pos") || 0, a = li.querySelector(".car__card");
      if (!stage) return;
      if (Math.abs(c - old) >= 4 && !reduce) {
        li.classList.add("no-anim"); li.setAttribute("data-pos", c); void li.offsetWidth;
        requestAnimationFrame(function () { li.classList.remove("no-anim"); });
      } else li.setAttribute("data-pos", c);
      var far = Math.abs(c) === 2;
      a.tabIndex = far ? -1 : 0;
      if (far) li.setAttribute("aria-hidden", "true"); else li.removeAttribute("aria-hidden");
    });
    meta(say);
  }
  function setIndex(k, say) { i = (k % n + n) % n; draw(say !== false); }
  function center(k, smooth) { /* scroll the row only, never the page (scrollIntoView also moved the page down to this section) */
    var it = items[k];
    track.scrollTo({ left: it.getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft - (track.clientWidth - it.offsetWidth) / 2, behavior: smooth && !reduce ? "smooth" : "auto" });
  }
  function go(k) { center(Math.max(0, Math.min(n - 1, k)), true); }
  car.querySelector(".car__prev").addEventListener("click", function () { if (stage) setIndex(i - 1); else go(i - 1); });
  car.querySelector(".car__next").addEventListener("click", function () { if (stage) setIndex(i + 1); else go(i + 1); });
  car.addEventListener("keydown", function (e) {
    if (!stage || (e.key !== "ArrowLeft" && e.key !== "ArrowRight")) return;
    e.preventDefault(); setIndex(i + (e.key === "ArrowRight" ? 1 : -1));
  });
  track.addEventListener("focusin", function (e) {
    var li = e.target.closest(".car__item"), k = items.indexOf(li);
    if (stage && li && li.getAttribute("data-pos") !== "0" && e.target.matches(":focus-visible")) setIndex(k); /* keyboard only: a mouse press must not move the card before the click is handled */
  });
  track.addEventListener("click", function (e) {
    var li = e.target.closest(".car__item"); if (!li) return;
    var k = items.indexOf(li);
    if (dragged) { e.preventDefault(); return; }
    if (stage) { if (li.getAttribute("data-pos") !== "0") { e.preventDefault(); setIndex(k); } return; }
    if (!li.classList.contains("is-active")) { e.preventDefault(); go(k); }
  });
  var x0 = null;
  track.addEventListener("pointerdown", function (e) { if (stage) { x0 = e.clientX; dragged = false; } });
  track.addEventListener("pointermove", function (e) { if (x0 !== null && Math.abs(e.clientX - x0) > 8) dragged = true; });
  function up(e) {
    if (x0 === null) return;
    var dx = e.clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) setIndex(i + (dx < 0 ? 1 : -1));
    setTimeout(function () { dragged = false; }, 0);
  }
  track.addEventListener("pointerup", up); track.addEventListener("pointercancel", up);
  track.addEventListener("dragstart", function (e) { e.preventDefault(); });

  /* phone and tablet: native scroll, an observer finds the centered card */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function () {
    if (stage) return;
    var m = track.getBoundingClientRect(), mid = m.left + m.width / 2, best = 0, bd = 1e9;
    items.forEach(function (li, k) { var r = li.getBoundingClientRect(), d = Math.abs(r.left + r.width / 2 - mid); if (d < bd) { bd = d; best = k; } });
    items.forEach(function (li, k) { li.classList.toggle("is-active", k === best); });
    if (best !== i) { i = best; meta(false); }
  }, { root: track, threshold: [0.5, 0.75, 1] }) : null;
  function mode() {
    stage = wide.matches; sec.classList.toggle("is-stage", stage);
    items.forEach(function (li) { if (io) { if (stage) io.unobserve(li); else io.observe(li); } li.classList.remove("is-active", "no-anim"); li.removeAttribute("data-pos"); li.removeAttribute("aria-hidden"); li.querySelector(".car__card").removeAttribute("tabindex"); });
    if (stage) { track.scrollLeft = 0; draw(false); } else { requestAnimationFrame(function () { center(i, false); }); }
  }
  (wide.addEventListener ? wide.addEventListener("change", mode) : wide.addListener(mode));
  if (wide.matches && !reduce) sec.classList.add("is-pre");
  mode();

  /* first reveal: the cards fan out from the center, 90 ms apart */
  function reveal() {
    items.forEach(function (li) { li.classList.add("is-in"); });
    if (!sec.classList.contains("is-pre")) return;
    items.forEach(function (li) { li.style.transitionDelay = Math.abs(+li.getAttribute("data-pos") || 0) * 90 + "ms"; });
    sec.classList.remove("is-pre");
    setTimeout(function () { items.forEach(function (li) { li.style.transitionDelay = ""; }); }, 1200);
  }
  if ("IntersectionObserver" in window) {
    var vo = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { reveal(); vo.disconnect(); } }, { threshold: 0.25 });
    vo.observe(car);
  } else reveal();
})();
