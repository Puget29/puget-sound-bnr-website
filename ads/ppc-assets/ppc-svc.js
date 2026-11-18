/* Services section style tests (S1 sticky, S2 list, S3 stack). Test pages only. Vanilla JS, IntersectionObserver and one passive scroll listener, no scroll hijacking.
   Without this script (or without JS) every service is a plain stacked photo card with its quote link. */
(function () {
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wide = matchMedia('(min-width:900px)');
  function on(mq, fn) { mq.addEventListener ? mq.addEventListener('change', fn) : mq.addListener(fn); }

  /* ---- S1: the row at the centre of the free area is active, its photo is shown on the pinned stage ---- */
  var s1 = document.querySelector('.sv1');
  if (s1) {
    var rows = [].slice.call(s1.querySelectorAll('.sv1__row')), imgs = [].slice.call(s1.querySelectorAll('.sv1__img')), stage = s1.querySelector('.sv1__stage'), io = null, cur = -1;
    var set = function (i) { if (i === cur) return; cur = i; rows.forEach(function (r, k) { r.classList.toggle('on', k === i); }); imgs.forEach(function (m, k) { m.classList.toggle('on', k === i); }); };
    var watch = function () {
      if (io) io.disconnect();
      var vh = window.innerHeight, top = wide.matches ? 0 : stage.getBoundingClientRect().height, yc = Math.round(top + (vh - top) / 2);
      io = new IntersectionObserver(function (en) { en.forEach(function (e) { if (e.isIntersecting) set(+e.target.getAttribute('data-i')); }); }, { rootMargin: '-' + yc + 'px 0px -' + Math.max(0, vh - yc - 1) + 'px 0px' });
      rows.forEach(function (r) { io.observe(r); });
    };
    s1.addEventListener('focusin', function (e) { var r = e.target.closest && e.target.closest('.sv1__row'); if (r) set(+r.getAttribute('data-i')); });
    on(wide, watch); window.addEventListener('resize', watch); watch(); set(0);
  }

  /* ---- S2: desktop hover or focus swaps the photo and opens the row, click or Enter pins it. Phone: accordion, one open, the first open ---- */
  var s2 = document.querySelector('.sv2');
  if (s2) {
    var r2 = [].slice.call(s2.querySelectorAll('.sv2__row')), im2 = [].slice.call(s2.querySelectorAll('.sv1__img')), pin = 0, act = -1;
    var show = function (i) {
      act = i;
      r2.forEach(function (r, k) { var o = k === i; r.classList.toggle('on', o); r.querySelector('.sv2__b').setAttribute('aria-expanded', o ? 'true' : 'false'); });
      im2.forEach(function (m, k) { m.classList.toggle('on', k === i); });
    };
    r2.forEach(function (r, i) {
      var b = r.querySelector('.sv2__b');
      b.addEventListener('click', function () {
        if (wide.matches) { pin = i; show(i); return; }
        var was = act === i; show(was ? -1 : i);
        if (!was) setTimeout(function () { var t = r.getBoundingClientRect(); if (t.top < 8 || t.bottom > innerHeight) r.scrollIntoView({ block: 'start', behavior: calm ? 'auto' : 'smooth' }); }, calm ? 0 : 420);
      });
      r.addEventListener('pointerenter', function (e) { if (wide.matches && e.pointerType === 'mouse') show(i); });
      r.addEventListener('focusin', function () { if (wide.matches) show(i); });
    });
    s2.querySelector('.sv2__list').addEventListener('pointerleave', function () { if (wide.matches) show(pin); });
    s2.querySelector('.sv2__list').addEventListener('focusout', function (e) { if (wide.matches && !s2.querySelector('.sv2__list').contains(e.relatedTarget)) show(pin); });
    on(wide, function () { pin = 0; show(0); }); show(0);
  }

  /* ---- S3: panels stick with a growing offset, a panel taller than the free height scrolls normally, the covered panel shrinks and dims ---- */
  var s3 = document.querySelector('.sv3');
  if (s3) {
    var ps = [].slice.call(s3.querySelectorAll('.sv3__p')), raf = 0, tops = [96, 108, 120];
    var fit = function () { ps.forEach(function (p, i) { p.classList.remove('is-free'); var h = p.offsetHeight; p.classList.toggle('is-free', h > innerHeight - tops[i] - 16); }); update(); };
    var update = function () {
      raf = 0;
      ps.forEach(function (p, i) {
        var n = ps[i + 1], t = 0;
        if (n && !calm && !p.classList.contains('is-free')) { var range = Math.min(p.offsetHeight, innerHeight), d = n.getBoundingClientRect().top - tops[i + 1]; t = Math.min(1, Math.max(0, 1 - d / range)); }
        p.style.setProperty('--t', t.toFixed(3));
      });
    };
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(update); }, { passive: true });
    window.addEventListener('resize', fit); fit();
  }
})();

/* ---- S4 hybrid: on desktop the row at the vertical centre is active and its photo is shown on the pinned stage. Phones use the plain 2 column grid, no JS needed. ---- */
(function () {
  var s4 = document.querySelector('.sv4'); if (!s4) return;
  var wide = matchMedia('(min-width:900px)'), rows = [].slice.call(s4.querySelectorAll('.sv4d__row')), imgs = [].slice.call(s4.querySelectorAll('.sv4d__img')), io = null, cur = -1;
  var set = function (i) { if (i === cur) return; cur = i; rows.forEach(function (r, k) { r.classList.toggle('on', k === i); }); imgs.forEach(function (m, k) { m.classList.toggle('on', k === i); }); };
  /* active row by hysteresis: the line sits a little below the middle of the visible area (under the 56px header); the current row stays until another row centre is at least 10vh closer to that line, so rows do not flicker while passing */
  var raf = 0, HH = 56, track = s4.classList.contains('sv4--city') ? s4.querySelector('.sv4t') : null;
  var pick = function () {
    raf = 0; if (!wide.matches || !rows.length) return;
    if (track) {
      /* city desktop: the track is pinned for (n - 1) steps; scroll progress through it picks the row, with a dead zone of 0.2 row so a row does not flicker at the border */
      var q = track.getBoundingClientRect(), span = Math.max(1, q.height - window.innerHeight), p = Math.min(1, Math.max(0, -q.top / span)), v = p * (rows.length - 1);
      if (cur < 0 || Math.abs(v - cur) >= 0.7) set(Math.round(v));
      return;
    }
    var vh = window.innerHeight, line = HH + (vh - HH) * 0.54, gap = vh * 0.1, best = 0, bd = 1e9, cd = 1e9;
    rows.forEach(function (r, k) { var q = r.getBoundingClientRect(), d = Math.abs(q.top + q.height / 2 - line); if (d < bd) { bd = d; best = k; } if (k === cur) cd = d; });
    if (cur < 0 || best === cur || bd + gap <= cd) set(best);
  };
  var tick = function () { if (!raf) raf = requestAnimationFrame(pick); };
  var watch = function () { tick(); };
  window.addEventListener('scroll', tick, { passive: true });
  s4.addEventListener('focusin', function (e) { var r = e.target.closest && e.target.closest('.sv4d__row'); if (r) set(+r.getAttribute('data-i')); });
  (wide.addEventListener ? wide.addEventListener('change', watch) : wide.addListener(watch)); window.addEventListener('resize', watch); watch(); set(0);
})();

/* ---- S4 phone: scroll progress drives 4 pages that slide up over each other inside one pinned stage. Native scroll only, one passive scroll listener with rAF. ---- */
(function () {
  var s4 = document.querySelector('.sv4'); if (!s4) return;
  var wrap = s4.querySelector('.sv4p'); if (!wrap) return;
  var stage = wrap.querySelector('.sv4p__stage'), pages = [].slice.call(wrap.querySelectorAll('.sv4p__pg')), N = pages.length;
  var mm = matchMedia('(max-width:899px)'), calm = matchMedia('(prefers-reduced-motion: reduce)');
  var pin = false, raf = 0, cur = -1, unit = 0, last = [];
  var cl = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
  var tabs = function () {
    pages.forEach(function (pg, i) { [].forEach.call(pg.querySelectorAll('a'), function (a) { if (pin && i !== cur) a.setAttribute('tabindex', '-1'); else a.removeAttribute('tabindex'); }); });
  };
  var update = function () {
    raf = 0; if (!pin) return;
    var r = wrap.getBoundingClientRect(), p = Math.max(0, Math.min(N - 1, -r.top / unit)), t = [1];
    for (var i = 1; i < N; i++) t.push(cl(p - (i - 1)));
    pages.forEach(function (pg, i) {
      var ti = i ? t[i] * t[i] * (3 - 2 * t[i]) : 1, c = i < N - 1 ? t[i + 1] * t[i + 1] * (3 - 2 * t[i + 1]) : 0, k = ti.toFixed(3) + '|' + c.toFixed(3);
      if (last[i] !== k) {
        last[i] = k; pg.style.setProperty('--t', ti.toFixed(3)); pg.style.setProperty('--c', c.toFixed(3));
        pg.classList.toggle('is-act', (ti > 0 && ti < 1) || (c > 0 && c < 1));
      }
      pg.classList.toggle('is-in', i === 0 ? r.bottom > 0 && r.top < innerHeight : t[i] > .35);
    });
    var now = 0; for (var j = 1; j < N; j++) if (t[j] > .5) now = j;
    if (now !== cur) { cur = now; stage.setAttribute('data-cur', now); pages.forEach(function (pg, i) { pg.classList.toggle('is-top', i === now); }); tabs(); }
    stage.style.setProperty('--pp', (p / (N - 1)).toFixed(3));
  };
  var ask = function () { if (!raf) raf = requestAnimationFrame(update); };
  var measure = function () { unit = stage.offsetHeight * .7; last = []; ask(); };
  var apply = function () {
    var want = mm.matches && !calm.matches;
    if (want === pin) { if (pin) measure(); return; }
    pin = want; s4.classList.toggle('is-pin', pin); cur = -1;
    if (!pin) { pages.forEach(function (pg) { pg.style.removeProperty('--t'); pg.style.removeProperty('--c'); pg.classList.remove('is-in', 'is-act', 'is-top'); }); stage.removeAttribute('data-cur'); stage.style.removeProperty('--pp'); }
    tabs(); if (pin) { unit = stage.offsetHeight * .7; last = []; update(); }
  };
  var goPage = function (i) { var r = wrap.getBoundingClientRect(); window.scrollTo(0, window.scrollY + r.top + i * unit + 1); };
  window.addEventListener('scroll', ask, { passive: true });
  window.addEventListener('resize', function () { if (pin) measure(); });
  [mm, calm].forEach(function (q) { q.addEventListener ? q.addEventListener('change', apply) : q.addListener(apply); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { s4.classList.toggle('is-play', en[0].isIntersecting && !document.hidden); }, { threshold: 0 }).observe(stage);
  document.addEventListener('visibilitychange', function () { s4.classList.toggle('is-hid', document.hidden); });
  wrap.addEventListener('focusin', function (e) {
    var c = e.target.closest && e.target.closest('.sv4p__c'); if (!pin || !c) return;
    var i = +c.closest('.sv4p__pg').getAttribute('data-p'); if (i !== cur) goPage(i);
  });
  wrap.addEventListener('keydown', function (e) {
    if (!pin || e.key !== 'Tab' || e.shiftKey) return;
    var c = e.target.closest && e.target.closest('.sv4p__c'); if (!c) return;
    var pg = c.closest('.sv4p__pg'), i = +pg.getAttribute('data-p'), cs = pg.querySelectorAll('.sv4p__c');
    if (c === cs[cs.length - 1] && i < N - 1) { e.preventDefault(); goPage(i + 1); var nx = pages[i + 1].querySelector('.sv4p__c'); nx.removeAttribute('tabindex'); nx.focus({ preventScroll: true }); }
  });
  wrap.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.sv4p__c'); if (!pin || !a || a.__go) return;
    e.preventDefault(); e.stopPropagation(); a.classList.add('is-tap');
    setTimeout(function () { a.__go = 1; a.click(); a.__go = 0; a.classList.remove('is-tap'); }, 150);
  }, true);
  apply();
})();

/* ---- S5 stack and S6 slide: phone swipe deck. Pointer events, touch-action pan-y, horizontal lock after 8px, one rAF layout while dragging, transform and opacity only. ---- */
(function () {
  var s4 = document.querySelector('.sv4'); if (!s4) return;
  var root = s4.querySelector('.sv5'); if (!root) return;
  var mode = root.getAttribute('data-mode'), deck = root.querySelector('.sv5__deck');
  var groups = [].slice.call(root.querySelectorAll('.sv5__grp')), bar = root.querySelector('.sv5__bar b'), live = root.querySelector('.sv5__sr');
  var btns = [].slice.call(root.querySelectorAll('.sv5__b')), again = root.querySelector('.sv5__again');
  var lists = groups.map(function (g) { return [].slice.call(g.children); });
  var mm = matchMedia('(max-width:899px)'), calm = matchMedia('(prefers-reduced-motion: reduce)');
  var on = false, busy = false, i = 0, f = 0, W = 300, raf = 0, nudged = false, firstSet = true;
  var labels = [].slice.call(root.querySelectorAll('.sv4p__c')).map(function (a) { return a.querySelector('.sv4p__n').textContent; });
  lists.forEach(function (ls) { ls.forEach(function (li) { if (li.querySelector('.sv4p__c') && !li.querySelector('.sv5__dim')) { var d = document.createElement('span'); d.className = 'sv5__dim'; d.setAttribute('aria-hidden', 'true'); li.querySelector('.sv4p__c').appendChild(d); } }); });
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var grp = function () { return i >> 2; }, pos = function () { return i === 16 ? 0 : i & 3; };

  var layout = function () {
    raf = 0; if (!on) return;
    var ls = lists[grp()], c = pos(), ff = f, extra = 0;
    if (c === 0 && ff < 0) { extra = -ff * W * .3; ff = 0; }
    ls.forEach(function (li, k) {
      var o = k - c - ff, tx = 0, ty = 0, rot = 0, sc = 1, op = 1, dim = 0;
      if (mode === 'stack') {
        if (o <= -1) { tx = -1.15 * W; rot = -8; op = 0; }
        else if (o < 0) { var a = -o; tx = -a * 1.15 * W; rot = -a * 8; op = 1 - a; }
        else { var d = Math.min(o, 2.4); sc = 1 - .05 * d; ty = 12 * d; op = o <= 2 ? 1 : Math.max(0, 3 - o); dim = .14 * Math.min(o, 2); }
        if (k === c && extra) { tx = extra; rot = extra / W * 8; }
        li.style.zIndex = 100 - k;
        li.style.transform = 'translate3d(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px,0) rotate(' + rot.toFixed(2) + 'deg) scale(' + sc.toFixed(3) + ')';
        var dm = li.querySelector('.sv5__dim'); if (dm) dm.style.opacity = dim.toFixed(3);
      } else {
        tx = o * (W - 14) + (k === c && extra ? extra : 0); op = Math.abs(o) > 2 ? 0 : 1;
        li.style.transform = 'translate3d(' + tx.toFixed(1) + 'px,0,0)';
      }
      li.style.opacity = op.toFixed(3);
    });
    bar.parentNode.style.setProperty('--pp', clamp((i + f) / 16, 0, 1).toFixed(3));
  };
  var ask = function () { if (!raf) raf = requestAnimationFrame(layout); };
  var eager = function (li) { if (li) [].forEach.call(li.querySelectorAll('img'), function (m) { m.loading = 'eager'; }); };
  var setActive = function () {
    var g = grp(), c = pos();
    groups.forEach(function (el, n) { el.hidden = n !== g; });
    lists[g].forEach(function (li, k) {
      var top = k === c; if (top) { li.removeAttribute('inert'); li.removeAttribute('aria-hidden'); } else { li.setAttribute('inert', ''); li.setAttribute('aria-hidden', 'true'); }
      li.classList.toggle('is-w', k === c || k === c + 1);
    });
    eager(lists[g][c + 1]); if (c >= 2 && lists[g + 1]) lists[g + 1].forEach(eager);
    if (deck.contains(document.activeElement) && document.activeElement.closest('[inert]')) deck.focus({ preventScroll: true });
    btns[0].disabled = i === 0; btns[1].disabled = i === 16;
    if (!firstSet) live.textContent = i === 16 ? 'End of services' : labels[i]; firstSet = false;
    f = 0; layout();
  };
  var tween = function (from, to, dur, done) {
    var t0 = performance.now(); busy = true;
    var step = function (t) {
      var p = clamp((t - t0) / dur, 0, 1); f = from + (to - from) * (1 - Math.pow(1 - p, 3)); layout();
      if (p < 1) requestAnimationFrame(step); else { busy = false; done && done(); }
    };
    requestAnimationFrame(step);
  };
  var rise = function (dir, ni) {
    var old = groups[grp()]; i = ni; var nw = groups[grp()], ls = lists[grp()];
    busy = true; nw.hidden = false; f = 0; nw.style.zIndex = 5; old.style.zIndex = 1;
    ls.forEach(function (li, k) { li.removeAttribute('inert'); });
    layout();
    var an = nw.animate([{ transform: 'translate3d(0,' + (dir > 0 ? '100%' : '-100%') + ',0)' }, { transform: 'translate3d(0,0,0)' }], { duration: 500, easing: 'cubic-bezier(.2,.7,.2,1)' });
    var fin = function () { busy = false; nw.style.zIndex = ''; old.style.zIndex = ''; setActive(); };
    an.onfinish = fin; an.oncancel = fin;
  };
  var go = function (dir, fromF) {
    if (busy || !on) return;
    if (dir > 0) {
      if (i >= 16) { tween(f, 0, 160); return; }
      var cross = ((i + 1) >> 2) !== (i >> 2) || i === 15;
      tween(fromF === undefined ? 0 : fromF, 1, cross ? 220 : 260, function () { if (cross) rise(1, i + 1); else { i++; setActive(); } });
    } else {
      if (i <= 0) { tween(f, 0, 160); return; }
      if (pos() === 0 && i !== 16) { f = 0; rise(-1, i - 1); return; }
      if (i === 16) { f = 0; rise(-1, 15); return; }
      tween(fromF === undefined ? 0 : fromF, -1, 260, function () { i--; setActive(); });
    }
  };
  var drag = null, moved = false;
  deck.addEventListener('pointerdown', function (e) {
    if (!on || busy || (e.pointerType === 'mouse' && e.button !== 0)) return;
    drag = { id: e.pointerId, x: e.clientX, y: e.clientY, lock: '', s: [[performance.now(), e.clientX]] }; moved = false;
  });
  deck.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.lock) {
      if (dx * dx + dy * dy < 64) return;
      drag.lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
      if (drag.lock === 'y') { drag = null; return; }
      try { deck.setPointerCapture(e.pointerId); } catch (x) { } moved = true;
    }
    drag.s.push([performance.now(), e.clientX]); if (drag.s.length > 6) drag.s.shift();
    f = clamp(-dx / W, -1, 1); if (i >= 16) f = Math.min(f, 0); ask();
  });
  var end = function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var d = drag; drag = null;
    if (d.lock === '' && e.type === 'pointerup') { var ta = e.target.closest && e.target.closest('.sv4p__c'); if (ta) { lastTap = performance.now(); tap(ta); } return; }
    if (d.lock !== 'x') return;
    setTimeout(function () { moved = false; }, 60);
    var dx = e.clientX - d.x, a = d.s[0], b = d.s[d.s.length - 1], v = b[0] > a[0] ? (b[1] - a[1]) / (b[0] - a[0]) : 0;
    if (e.type === 'pointercancel') { tween(f, 0, 180); return; }
    var fwd = (dx < -W * .28 || v < -.5) && dx < -10, back = (dx > W * .28 || v > .5) && dx > 10;
    if (fwd && i < 16) { busy = false; go(1, f); } else if (back && i > 0) { busy = false; go(-1, f); } else tween(f, 0, 200);
  };
  deck.addEventListener('pointerup', end); deck.addEventListener('pointercancel', end);
  deck.addEventListener('dragstart', function (e) { e.preventDefault(); });
  var lastTap = 0;
  var tap = function (a) {
    if (a.__tap) return; a.__tap = 1; a.classList.add('is-tap');
    setTimeout(function () { a.__go = 1; a.click(); a.__go = 0; a.__tap = 0; a.classList.remove('is-tap'); }, 150);
  };
  deck.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.sv4p__c'); if (!on || !a || a.__go) return;
    e.preventDefault(); e.stopPropagation(); if (moved || performance.now() - lastTap < 600) return;
    tap(a);
  }, true);
  deck.addEventListener('keydown', function (e) {
    if (!on || (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft')) return;
    e.preventDefault(); go(e.key === 'ArrowRight' ? 1 : -1);
  });
  btns.forEach(function (b) { b.addEventListener('click', function () { go(+b.getAttribute('data-d')); }); });
  if (again) again.addEventListener('click', function () { if (busy) return; rise(-1, 0); });
  var measure = function () { W = deck.clientWidth || 300; ask(); };
  var apply = function () {
    var want = mm.matches && !calm.matches; if (want === on) { if (on) measure(); return; }
    on = want; s4.classList.toggle('is-deck', on);
    if (on) { deck.setAttribute('tabindex', '0'); W = deck.clientWidth || 300; i = 0; f = 0; firstSet = true; setActive(); }
    else {
      deck.removeAttribute('tabindex');
      groups.forEach(function (g) { g.hidden = false; g.style.zIndex = ''; });
      lists.forEach(function (ls) { ls.forEach(function (li) { li.style.transform = li.style.opacity = li.style.zIndex = ''; li.removeAttribute('inert'); li.removeAttribute('aria-hidden'); li.classList.remove('is-w'); }); });
    }
  };
  window.addEventListener('resize', function () { if (on) measure(); });
  [mm, calm].forEach(function (q) { q.addEventListener ? q.addEventListener('change', apply) : q.addListener(apply); });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) {
      if (!en[0].isIntersecting || nudged || !on) return; nudged = true; io.disconnect();
      setTimeout(function () { if (i === 0 && !busy && !drag) tween(0, 24 / W, 260, function () { tween(24 / W, 0, 340); }); }, 400);
    }, { threshold: .6 });
    io.observe(deck);
  }
  apply();
})();

/* ---- S6 phone swipe deck. Normal page flow, horizontal swipe only. Pointer events, touch-action pan-y, direction lock after 8px, one rAF layout while dragging, transform and opacity only. ---- */
(function () {
  var s4 = document.querySelector('.sv4'); if (!s4) return;
  var root = s4.querySelector('.sv6'); if (!root) return;
  var deck = root.querySelector('.sv6__deck'), groups = [].slice.call(root.querySelectorAll('.sv6__grp')), lists = groups.map(function (g) { return [].slice.call(g.children); });
  var bar = root.querySelector('.sv6__bar'), live = root.querySelector('.sv6__sr'), again = root.querySelector('.sv5__again');
  var mm = matchMedia('(max-width:899px)'), calm = matchMedia('(prefers-reduced-motion: reduce)');
  var on = false, busy = false, rising = false, nudging = false, tok = 0, i = 0, f = 0, raf = 0, CW = 300, STEP = 260, swiped = false, firstSet = true, nudges = 0, nudgeT = 0, inview = false, last = {};
  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var sm = function (u) { u = clamp(u, 0, 1); return u * u * (3 - 2 * u); };
  var part = lists.map(function (ls) { return ls.map(function (li) { var a = li.querySelector('.sv4p__c'), im = li.querySelector('.sv4p__img'), d = null; if (a) { d = document.createElement('span'); d.className = 'sv6__dim'; d.setAttribute('aria-hidden', 'true'); a.appendChild(d); } return { img: im && im.firstElementChild, t: li.querySelector('.sv4p__t'), chip: li.querySelector('.sv4p__chip'), dim: d }; }); });
  var labels = [].slice.call(root.querySelectorAll('.sv4p__c')).map(function (a) { return a.querySelector('.sv4p__n').textContent; });
  var grp = function () { return i >> 2; }, pos = function () { return i === 16 ? 0 : i & 3; };
  var put = function (el, key, val, prop) { if (last[key] !== val) { last[key] = val; el.style[prop || 'transform'] = val; } };

  var lay = function (g, c, ff, extra) {
    lists[g].forEach(function (li, k) {
      var o = k - c - ff, x, sc, ty = 0, op = 1, dim = 0, pt = part[g][k], oc = clamp(o, -1, 1);
      if (o <= 0) { var ao = Math.min(-o, 1.2); x = o * STEP; sc = 1 - .06 * Math.min(ao, 1); op = ao > 1 ? 0 : 1 - .5 * ao; }
      else if (o <= 1) { x = o * STEP; sc = 1 - .06 * o; dim = .35 * o; }
      else if (o <= 2) { x = STEP; sc = .94 - .06 * (o - 1); ty = (o - 1) * 22; dim = .5; op = 1 - .4 * (o - 1); }
      else { x = STEP; sc = .88; ty = 22; op = 0; }
      if (k === c && extra) x += extra;
      var a = o >= 0 ? sm((1 - o - .7) / .3) : 1 - sm(-o / .4), ky = g + '_' + k;
      put(li, 'c' + ky, 'translate3d(' + x.toFixed(1) + 'px,' + ty.toFixed(1) + 'px,0) scale(' + sc.toFixed(3) + ')'); put(li, 'o' + ky, op.toFixed(3), 'opacity');
      li.style.zIndex = 100 - k;
      if (pt.dim) put(pt.dim, 'd' + ky, dim.toFixed(3), 'opacity');
      if (pt.img) put(pt.img, 'i' + ky, 'none');
      [pt.t, pt.chip].forEach(function (el, n) { if (el) { put(el, 't' + n + ky, 'translate3d(0,' + ((1 - a) * 10).toFixed(1) + 'px,0)'); put(el, 'u' + n + ky, (.25 + .75 * a).toFixed(3), 'opacity'); } });
    });
  };
  var layout = function () {
    raf = 0; if (!on) return;
    var g = grp(), c = pos(), ff = f, extra = 0;
    if (c === 0 && ff < 0) { extra = -ff * STEP * .3; ff = 0; }
    lay(g, c, ff, extra);
    var ng = groups[g + 1];
    if (ng && !rising) {
      var pf = clamp(c + ff - 2, 0, 1);
      if (pf > 0) { ng.hidden = false; lay(g + 1, 0, 0, 0); put(ng, 'pg', 'translate3d(0,calc(100% - ' + (16 * pf).toFixed(1) + 'px),0)'); put(ng, 'po', (.7 * pf).toFixed(3), 'opacity'); }
      else if (!ng.hidden) { ng.hidden = true; last.pg = last.po = ''; ng.style.transform = ng.style.opacity = ''; }
    }
    var pp = clamp((i + f) / 16, 0, 1).toFixed(4); if (last.pp !== pp) { last.pp = pp; bar.style.setProperty('--pp', pp); }
  };
  var ask = function () { if (!raf) raf = requestAnimationFrame(layout); };
  var eager = function (li) { if (li) [].forEach.call(li.querySelectorAll('img'), function (m) { m.loading = 'eager'; }); };
  var setActive = function () {
    var g = grp(), c = pos(); last = {};
    groups.forEach(function (el, n) { el.hidden = n !== g; el.style.transform = el.style.opacity = ''; });
    lists[g].forEach(function (li, k) {
      if (k === c) { li.removeAttribute('inert'); li.removeAttribute('aria-hidden'); } else { li.setAttribute('inert', ''); li.setAttribute('aria-hidden', 'true'); }
      li.classList.toggle('is-w', k === c || k === c + 1);
    });
    eager(lists[g][c + 1]); if (c >= 2 && lists[g + 1]) eager(lists[g + 1][0]);
    if (deck.contains(document.activeElement) && document.activeElement.closest('[inert]')) deck.focus({ preventScroll: true });
    deck.classList.toggle('is-end', i === 16);
    if (!firstSet) live.textContent = i === 16 ? 'End of services' : labels[i]; firstSet = false;
    f = 0; layout();
  };
  var tween = function (from, to, dur, done) {
    busy = true; if (calm.matches) dur = 0;
    var t0 = performance.now(), my = ++tok;
    var step = function (t) {
      if (my !== tok) return;
      var p = dur ? clamp((t - t0) / dur, 0, 1) : 1; f = from + (to - from) * (1 - Math.pow(1 - p, 3)); layout();
      if (p < 1) requestAnimationFrame(step); else { busy = false; done && done(); }
    };
    requestAnimationFrame(step);
  };
  var rise = function (dir, ni) {
    var old = groups[grp()]; var fromT, fromO = 1;
    var nwBefore = groups[ni >> 2];
    if (dir > 0 && !nwBefore.hidden && nwBefore.style.transform) { fromT = nwBefore.style.transform; fromO = parseFloat(nwBefore.style.opacity || '1'); } else fromT = 'translate3d(0,' + (dir > 0 ? '100%' : '-100%') + ',0)';
    i = ni; var nw = groups[grp()]; busy = true; rising = true; f = 0; last = {}; nw.hidden = false; nw.style.transform = nw.style.opacity = ''; nw.style.zIndex = 5; old.style.zIndex = 1;
    lists[grp()].forEach(function (li) { li.removeAttribute('inert'); }); lay(grp(), pos(), 0, 0);
    var fin = function () { busy = false; rising = false; nw.style.zIndex = ''; old.style.zIndex = ''; setActive(); };
    if (calm.matches || !nw.animate) { fin(); return; }
    var an = nw.animate([{ transform: fromT, opacity: fromO }, { transform: 'translate3d(0,0,0)', opacity: 1 }], { duration: 500, easing: 'cubic-bezier(.2,.7,.2,1)' });
    an.onfinish = fin; an.oncancel = fin;
  };
  var go = function (dir, fromF) {
    if (busy || !on) return;
    if (dir > 0) {
      if (i >= 16) { tween(f, 0, 160); return; }
      var cross = ((i + 1) >> 2) !== (i >> 2);
      tween(fromF === undefined ? 0 : fromF, 1, cross ? 220 : 260, function () { if (cross) rise(1, i + 1); else { i++; setActive(); } });
    } else {
      if (i <= 0) { tween(f, 0, 160); return; }
      if (pos() === 0) { f = 0; rise(-1, i - 1); return; }
      tween(fromF === undefined ? 0 : fromF, -1, 260, function () { i--; setActive(); });
    }
  };
  var markSwiped = function () { if (swiped) return; swiped = true; clearTimeout(nudgeT); deck.classList.add('has-swiped'); deck.classList.remove('is-hint'); };
  var drag = null, moved = false, lastTap = 0;
  var tap = function (a) {
    if (a.__tap) return; a.__tap = 1; a.classList.add('is-tap');
    setTimeout(function () { a.__go = 1; a.click(); a.__go = 0; a.__tap = 0; a.classList.remove('is-tap'); }, 150);
  };
  deck.addEventListener('pointerdown', function (e) {
    if (nudging) { nudging = false; tok++; busy = false; f = 0; ask(); }
    if (!on || busy || (e.pointerType === 'mouse' && e.button !== 0)) return;
    drag = { id: e.pointerId, x: e.clientX, y: e.clientY, lock: '', s: [[performance.now(), e.clientX]] }; moved = false;
  });
  deck.addEventListener('pointermove', function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (!drag.lock) {
      if (dx * dx + dy * dy < 64) return;
      drag.lock = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
      if (drag.lock === 'y') { drag = null; return; }
      try { deck.setPointerCapture(e.pointerId); } catch (x) { } moved = true; markSwiped();
    }
    drag.s.push([performance.now(), e.clientX]); if (drag.s.length > 6) drag.s.shift();
    f = clamp(-dx / STEP, -1, 1); if (i >= 16) f = Math.min(f, 0); ask();
  });
  var end = function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var d = drag; drag = null;
    if (d.lock === '' && e.type === 'pointerup') { var ta = e.target.closest && e.target.closest('.sv4p__c'); if (ta) { lastTap = performance.now(); tap(ta); } return; }
    if (d.lock !== 'x') return;
    setTimeout(function () { moved = false; }, 60);
    var dx = e.clientX - d.x, a = d.s[0], b = d.s[d.s.length - 1], v = b[0] > a[0] ? (b[1] - a[1]) / (b[0] - a[0]) : 0;
    if (e.type === 'pointercancel') { tween(f, 0, 180); return; }
    var fwd = (dx < -.22 * CW || v < -.5) && dx < -10, back = (dx > .22 * CW || v > .5) && dx > 10;
    if (fwd && i < 16) go(1, f); else if (back && i > 0) go(-1, f); else tween(f, 0, 200);
  };
  deck.addEventListener('pointerup', end); deck.addEventListener('pointercancel', end);
  deck.addEventListener('dragstart', function (e) { e.preventDefault(); });
  deck.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.sv4p__c'); if (!on || !a || a.__go) return;
    e.preventDefault(); e.stopPropagation(); if (moved || performance.now() - lastTap < 600) return; tap(a);
  }, true);
  deck.addEventListener('keydown', function (e) {
    if (!on || (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft')) return;
    e.preventDefault(); markSwiped(); go(e.key === 'ArrowRight' ? 1 : -1);
  });
  if (again) again.addEventListener('click', function () { if (!busy) rise(-1, 0); });
  var schedule = function () {
    clearTimeout(nudgeT); if (!on || calm.matches || swiped || nudges >= 3 || !inview) return;
    nudgeT = setTimeout(function () {
      if (swiped || !inview) return;
      if (busy || drag || i !== 0) { schedule(); return; }
      nudges++; nudging = true; tween(0, 36 / STEP, 260, function () { tween(36 / STEP, 0, 460, function () { nudging = false; schedule(); }); });
    }, nudges === 0 ? 1200 : 3500);
  };
  var measure = function () { CW = deck.clientWidth - 52 || 280; STEP = CW + 12; deck.style.height = deck.clientWidth > 52 ? Math.round(CW * 2 / 3) + 'px' : ''; last = {}; ask(); };
  var apply = function () {
    var want = !!mm.matches && !calm.matches; if (want === on) { if (on) measure(); return; }
    on = want; s4.classList.toggle('is-s6', on);
    if (on) { deck.setAttribute('tabindex', '0'); measure(); i = 0; f = 0; firstSet = true; setActive(); }
    else {
      clearTimeout(nudgeT); deck.removeAttribute('tabindex'); deck.style.height = '';
      groups.forEach(function (g) { g.hidden = false; g.style.transform = g.style.opacity = g.style.zIndex = ''; });
      lists.forEach(function (ls) { ls.forEach(function (li) { li.style.cssText = ''; li.removeAttribute('inert'); li.removeAttribute('aria-hidden'); li.classList.remove('is-w'); }); });
    }
  };
  window.addEventListener('resize', function () { if (on) measure(); });
  [mm, calm].forEach(function (q) { q.addEventListener ? q.addEventListener('change', apply) : q.addListener(apply); });
  if ('IntersectionObserver' in window) new IntersectionObserver(function (en) {
    inview = en[0].isIntersecting && on; deck.classList.toggle('is-hint', inview && !swiped && !calm.matches); if (inview) schedule(); else clearTimeout(nudgeT);
  }, { threshold: .5 }).observe(deck);
  apply();
})();
