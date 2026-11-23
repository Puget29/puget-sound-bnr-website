/* BNR PPC city pages. The three config lines below are injected by tools/ppc/build.py from ppc/config.json. Docs: docs/ppc-forms.md */
/* Microsoft UET tag 343288326 + CallRail DNI swap.js. Added 2026-11-23 for Microsoft Ads tracking. */
(function (w, d) { w.uetq = w.uetq || []; var u = d.createElement('script'); u.async = true; u.src = 'https://bat.bing.com/bat.js'; u.onload = function () { var o = { ti: '343288326', enableAutoSpaTracking: true }; o.q = w.uetq; w.uetq = new UET(o); w.uetq.push('pageLoad'); }; d.head.appendChild(u); var c = d.createElement('script'); c.async = true; c.src = 'https://cdn.callrail.com/companies/718739933/f764ddd9de3375a7dd16/12/swap.js'; d.body.appendChild(c); })(window, document);
(function () {
  'use strict';
  var FORM = {"provider":"","endpoint":"","accessKey":"","thankYou":"/ppc-assets/thank-you/"};
  var TRACKING = {"gtmId":"","gaId":"","adsConversion":""};
  var PHONE = (document.querySelector('.pill') || { textContent: '' }).textContent.replace('Call', '').trim();
  if (window.PPC_CONFIG) { // test hook, lets the audit set an endpoint without editing the file
    FORM = Object.assign({}, FORM, window.PPC_CONFIG.form); TRACKING = Object.assign({}, TRACKING, window.PPC_CONFIG.tracking);
  }
  var PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid', 'msclkid', 'fbclid'];
  var KEY = 'bnr_ppc_first_touch';
  var form = document.querySelector('.lead-form');
  var dl = window.dataLayer = window.dataLayer || [];
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- first-touch campaign data, kept for the browser session ---- */
  function store(op, val) {
    try { return op === 'get' ? JSON.parse(sessionStorage.getItem(KEY) || 'null') : sessionStorage.setItem(KEY, JSON.stringify(val)); } catch (e) { return null; }
  }
  var q = new URLSearchParams(location.search), now = { params: {}, count: 0, referrer: document.referrer.slice(0, 300), landing_page: location.origin + location.pathname, first_seen: new Date().toISOString() };
  PARAMS.forEach(function (k) { var v = q.get(k); if (v) { now.params[k] = v.slice(0, 200); now.count++; } });
  var touch = store('get');
  if (!touch || (!touch.count && now.count)) { touch = now; store('set', touch); }

  /* ---- events ---- */
  function track(name, extra) {
    var e = { event: name, ppc_city: form ? form.elements.origin_city.value : '', ppc_service: form && form.elements.origin_service ? form.elements.origin_service.value : '', ppc_page: location.pathname };
    PARAMS.forEach(function (k) { if (touch.params[k]) e[k] = touch.params[k]; });
    for (var k in extra) e[k] = extra[k];
    dl.push(e);
  }
  (function loadTags() { // nothing external loads while the ids are empty
    function s(src) { var t = document.createElement('script'); t.async = true; t.src = src; document.head.appendChild(t); }
    if (TRACKING.gtmId) { dl.push({ 'gtm.start': Date.now(), event: 'gtm.js' }); s('https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(TRACKING.gtmId)); return; }
    var id = TRACKING.gaId || (TRACKING.adsConversion || '').split('/')[0];
    if (!id) return;
    window.gtag = function () { dl.push(arguments); };
    s('https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id));
    gtag('js', new Date());
    if (TRACKING.gaId) gtag('config', TRACKING.gaId);
    if (TRACKING.adsConversion) gtag('config', TRACKING.adsConversion.split('/')[0]);
  })();
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href^="tel:"]');
    if (a) track('ppc_click_call', { ppc_link_location: a.closest('.callbar') ? 'callbar' : a.closest('header') ? 'header' : a.closest('footer') ? 'footer' : a.closest('.hero, .hero2') ? 'hero' : 'page' });
  });

  if (!form) { // shared thank-you page
    track('ppc_thank_you', { ppc_city: new URLSearchParams(location.search).get('c') || '' });
    if (window.gtag && TRACKING.adsConversion) gtag('event', 'conversion', { send_to: TRACKING.adsConversion });
    return;
  }
  track('ppc_view');
  document.addEventListener('ppc:profile', function (e) { track('ppc_click_profile', { ppc_platform: String(e.detail).slice(0, 40) }); });
  document.addEventListener('ppc:service', function (e) { track('ppc_service_card_click', { ppc_service: String(e.detail).slice(0, 60) }); });

  /* ---- hidden attribution fields ---- */
  form.elements.origin_page.value = location.origin + location.pathname;
  var hidden = { referrer: touch.referrer, landing_page: touch.landing_page, first_seen: touch.first_seen };
  PARAMS.forEach(function (k) { hidden[k] = touch.params[k] || ''; });
  Object.keys(hidden).forEach(function (k) {
    var i = form.querySelector('input[type=hidden][name="' + k + '"]'); if (!i) { i = document.createElement('input'); i.type = 'hidden'; i.name = k; form.appendChild(i); } i.value = hidden[k];
  });

  /* ---- jump to the form (service cards, final call to action, call bar) ---- */
  var card = document.getElementById('consultation');
  function toForm(chip, focusId) {
    if (chip !== null) {
      [].forEach.call(form.querySelectorAll('input[name=service]'), function (r) { r.checked = r.value === chip; });
    }
    var f = focusId && document.getElementById(focusId);
    if (f) f.focus({ preventScroll: true });
    card.scrollIntoView({ behavior: calm ? 'auto' : 'smooth', block: 'start' });
  }
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href="#consultation"]');
    if (!a) return;
    ev.preventDefault();
    var svcName = a.getAttribute('data-service'), os = form.elements.origin_service;
    if (svcName !== null) {
      if (!os) { os = document.createElement('input'); os.type = 'hidden'; os.name = 'origin_service'; os.setAttribute('data-dyn', '1'); form.appendChild(os); }
      os.value = svcName;
    } else if (os && os.hasAttribute('data-dyn')) os.parentNode.removeChild(os);
    toForm(a.getAttribute('data-chip'), a.getAttribute('data-focus') || (a.hasAttribute('data-chip') ? 'phone' : null));
  });
  var addBtn = form.querySelector('.addemail');
  if (addBtn) addBtn.addEventListener('click', function () {
    var f = form.querySelector('.field--email'); f.hidden = false; addBtn.hidden = true; f.querySelector('input').focus();
  });

  /* ---- sticky bar (under 1024px): always on, only hidden while a field has focus (on screen keyboard) ---- */
  var bar = document.getElementById('callbar');
  if (bar) {
    var typing = function (on) { bar.classList.toggle('is-off', on); };
    document.addEventListener('focusin', function (e) { typing(/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName) && matchMedia('(max-width:1023px)').matches); });
    document.addEventListener('focusout', function () { setTimeout(function () { if (!/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '')) typing(false); }, 60); });
  }

  /* ---- form ---- */
  var btn = form.querySelector('.submit'), slot = form.querySelector('.slot'), msg = form.querySelector('.msg');
  var label = btn.textContent, loadedAt = Date.now(), started = false, busy = false;
  var emailMode = form.getAttribute('data-email') || 'off';
  var zipEl = form.elements.zip; if (zipEl) zipEl.addEventListener('input', function () { var c = zipEl.value.replace(/\D/g, '').slice(0, 5); if (c !== zipEl.value) zipEl.value = c; });
  form.addEventListener('input', function () { if (!started) { started = true; track('ppc_form_start'); } });

  var RULES = {
    name: function (v) { return v.trim().length > 1 || 'Enter your name'; },
    phone: function (v) { return v.replace(/\D/g, '').length >= 10 || 'Enter a phone number with area code'; },
    zip: function (v) { return /^\d{5}$/.test(v.trim()) || 'Enter a 5 digit zip code'; },
    email: function (v) { return (!v.trim() && emailMode !== 'required' && !(form.elements.email && form.elements.email.required)) || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim()) || 'Enter a valid email'; }
  };
  function validate() {
    var first = null;
    Object.keys(RULES).forEach(function (n) {
      var el = form.elements[n]; if (!el) return;
      var err = document.getElementById(n + '-err'), r = RULES[n](el.value);
      err.textContent = r === true ? '' : r;
      if (r === true) { el.removeAttribute('aria-invalid'); el.removeAttribute('aria-describedby'); }
      else { el.setAttribute('aria-invalid', 'true'); el.setAttribute('aria-describedby', err.id); first = first || el; }
    });
    return first;
  }
  function say(text, isErr) {
    msg.textContent = text; msg.classList.toggle('is-error', !!isErr); slot.classList.toggle('is-msg', !!text);
    if (text && msg.scrollIntoView) msg.scrollIntoView({ block: 'center', behavior: calm ? 'auto' : 'smooth' }); /* keep the message above the fixed bar on phones */
  }
  function showOk(real) {
    form.style.visibility = 'hidden';
    card.querySelector('.ok').hidden = false;
    if (real) setTimeout(function () { location.assign(FORM.thankYou + '?c=' + encodeURIComponent(form.getAttribute('data-slug'))); }, 450);
  }
  form.addEventListener('submit', function (ev) {
    ev.preventDefault(); // personal data never goes into the URL
    if (busy) return;
    var bad = validate();
    if (bad) { bad.focus(); say(''); return; }
    var endpoint = '/'; /* Netlify Forms: the form named lead is posted to the site root */
    var data = {}; [].forEach.call(form.elements, function (el) {
      if (el.name && el.name !== 'website' && (el.type !== 'radio' || el.checked)) data[el.name] = el.value;
    });
    if (form.elements.website.value || Date.now() - loadedAt < 3000) return showOk(false); // spam: look done, send nothing, no event
    busy = true; btn.disabled = true; btn.textContent = 'Sending'; say('');
    data.elapsed = Date.now() - loadedAt;
    var body = FORM.provider === 'web3forms' ? Object.assign({ access_key: FORM.accessKey, subject: 'PPC lead: ' + data.origin_city, from_name: 'BNR PPC page' }, data) : data;
    var ctl = window.AbortController ? new AbortController() : null, t = setTimeout(function () { ctl && ctl.abort(); }, 10000);
    fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(body).toString(), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (!r.ok) throw new Error('bad'); })
      .then(function () { clearTimeout(t); track('ppc_form_submit_success', { ppc_service: data.service || data.origin_service || '' }); dl.push({ event: 'generate_lead', service: data.service || data.origin_service || '', city: data.origin_city || '' }); showOk(true); })
      .catch(function () {
        clearTimeout(t); busy = false; btn.disabled = false; btn.textContent = label;
        say('Your request was not sent. Please try again or call ' + PHONE + '.', true);
      });
  });
})();
(function () {
  var texts = [].slice.call(document.querySelectorAll('[data-review-text]'));
  if (!texts.length) return;
  function lineCount(text) {
    var range = document.createRange();
    range.selectNodeContents(text);
    return range.getClientRects().length;
  }
  function setExpanded(text, button, expanded) {
    text.dataset.reviewExpanded = expanded ? 'true' : 'false';
    text.classList.toggle('is-clamped', !expanded);
    button.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    button.textContent = expanded ? 'Show less' : 'Read more';
  }
  function update() {
    texts.forEach(function (text) {
      text.classList.remove('is-clamped');
      text.style.whiteSpace = 'normal'; /* collapsed text runs on without paragraph breaks, so the clamp never ends on a lone ellipsis line */
      var hasMore = lineCount(text) > (window.matchMedia && matchMedia('(min-width:900px)').matches ? 6 : 5);
      text.style.whiteSpace = '';
      var button = text._reviewMore;
      if (!hasMore) {
        if (button) button.remove();
        text._reviewMore = null;
        text.dataset.reviewExpanded = 'false';
        return;
      }
      if (!button) {
        button = document.createElement('button');
        button.type = 'button';
        button.className = 'g-review__more';
        button.setAttribute('aria-expanded', 'false');
        button.textContent = 'Read more';
        button.addEventListener('click', function () {
          setExpanded(text, button, text.dataset.reviewExpanded !== 'true');
        });
        text.parentNode.appendChild(button);
        text._reviewMore = button;
      }
      if (text.dataset.reviewExpanded === 'true') {
        button.setAttribute('aria-expanded', 'true');
        button.textContent = 'Show less';
      } else {
        text.classList.add('is-clamped');
        button.setAttribute('aria-expanded', 'false');
        button.textContent = 'Read more';
      }
    });
  }
  var frame = 0;
  window.addEventListener('resize', function () {
    if (frame) return;
    frame = requestAnimationFrame(function () { frame = 0; update(); });
  }, { passive: true });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(update);
  else requestAnimationFrame(update);
})();

/* ---- reveal on scroll: one observer, runs once per element, below-the-fold only (CSS in ppc.css, data-rv vocabulary: rise, words, stagger, scale, hair) ---- */
(function () {
  'use strict';
  var els = [].slice.call(document.querySelectorAll('[data-rv]'));
  if (!els.length || !('IntersectionObserver' in window) || location.hash || (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches)) return;
  document.documentElement.classList.add('js');
  var hidden = [], vh = innerHeight;
  var io = new IntersectionObserver(function (en) {
    show(en.filter(function (e) { return e.isIntersecting; }).map(function (e) { return e.target; }));
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  function show(list) {
    list.forEach(function (e) {
      io.unobserve(e); e.classList.add('rv-go'); e.classList.remove('rv-h');
      var k = hidden.indexOf(e); if (k > -1) hidden.splice(k, 1);
    });
    if (list.length) setTimeout(function () { list.forEach(function (e) { e.classList.remove('rv-go'); }); }, 1500);
  }
  function words(el) { // the heading keeps its text for screen readers; the visible words are aria-hidden spans
    var h = el.querySelector('h2'), t = h.textContent, sr = document.createElement('span');
    sr.className = 'sr'; sr.textContent = t; h.textContent = ''; h.appendChild(sr);
    t.trim().split(/\s+/).forEach(function (w, i) {
      var o = document.createElement('span'), n = document.createElement('i');
      o.className = 'w'; o.setAttribute('aria-hidden', 'true'); n.textContent = w; n.style.setProperty('--d', Math.min(80 + i * 40, 400) + 'ms');
      o.appendChild(n); h.appendChild(o); h.appendChild(document.createTextNode(' '));
    });
  }
  var tops = els.map(function (e) { return e.getBoundingClientRect().top; });
  els.forEach(function (e, i) {
    if (tops[i] < vh) return; // first screen is never hidden
    var kind = e.getAttribute('data-rv');
    if (kind === 'stagger') [].forEach.call(e.children, function (c, j) { c.style.setProperty('--d', Math.min(j * 60, 360) + 'ms'); });
    if (kind === 'words') words(e);
    e.classList.add('rv-h'); hidden.push(e); if (!window.__ppcNoIO) io.observe(e);
  });
  /* fail safe: anything hidden that is in the viewport for 1.2 s, or already scrolled past, is shown whatever the observer did. window.__ppcNoIO (test hook) simulates a dead observer. */
  var seenAt = new WeakMap();
  function sweep() {
    var now = Date.now(), vh2 = innerHeight;
    show(hidden.filter(function (e) {
      var r = e.getBoundingClientRect();
      if (r.bottom < 0) return true;
      if (r.top < vh2 * 0.95 && r.bottom > 0) { var t = seenAt.get(e); if (!t) { seenAt.set(e, now); return false; } return now - t >= 1200; }
      seenAt.delete(e); return false;
    }));
  }
  var tick = setInterval(function () { sweep(); }, 300);
  addEventListener('scroll', function () { sweep(); }, { passive: true });
  function all() { show(hidden.slice()); }
  addEventListener('hashchange', all); addEventListener('pageshow', all); addEventListener('resize', all); addEventListener('beforeprint', all);
})();

/* FAQ: one row open at a time, rows slide open and shut (native details stays the base, so no JS and reduced motion still work) */
(function () {
  var list = document.querySelector('.faq__list'); if (!list || !list.animate) return;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)');
  function done(d) {
    var p = d.querySelector('p'); if (!d._a) return;
    var opening = d._a.__o; d._a = null; p.style.overflow = '';
    if (!opening) { d.open = false; d.classList.remove('is-closing'); }
  }
  function settle(d) { if (d._a) { var a = d._a; a.onfinish = a.oncancel = null; a.cancel(); done(d); } }
  function run(d, opening) {
    var p = d.querySelector('p'), pad = getComputedStyle(p).paddingBottom, h;
    if (opening) { d.open = true; h = p.scrollHeight; } else { h = p.offsetHeight; d.classList.add('is-closing'); }
    p.style.overflow = 'hidden';
    var full = { height: h + 'px', paddingBottom: pad, opacity: 1 }, none = { height: '0px', paddingBottom: '0px', opacity: 0 };
    var a = p.animate(opening ? [none, { opacity: 1, offset: 0.6 }, full] : [full, { opacity: 0, offset: 0.5 }, none], { duration: opening ? 420 : 300, easing: 'cubic-bezier(.2,.7,.1,1)' });
    a.__o = opening; d._a = a;
    a.onfinish = function () { done(d); if (opening) d.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); };
  }
  list.addEventListener('click', function (e) {
    var s = e.target.closest && e.target.closest('summary'); if (!s || s.parentNode.tagName !== 'DETAILS') return;
    var d = s.parentNode, all = [].slice.call(list.querySelectorAll('details'));
    e.preventDefault();
    if (reduce.matches) { if (!d.open) all.forEach(function (o) { o.open = false; }); d.open = !d.open; return; }
    settle(d);
    var opening = !d.open;
    if (opening) all.forEach(function (o) { if (o !== d) { settle(o); if (o.open) run(o, false); } });
    run(d, opening);
  });
})();

/* logo sliders: one rAF loop glides each track by scrollLeft (36 px/s, float accumulator because iOS rounds offsets). Swipe is native scrolling, mouse drag is pointer events.
   The real set is in the HTML; aria-hidden clones (one before, the rest after, at least 2x the width) keep it seamless and are rebuilt on resize. */
(function () {
  var S = document.querySelectorAll('[data-sl]'); if (!S.length || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var L = [], raf = 0, last = 0, away = document.hidden;
  function active(o) { return o.vis && !away && !o.hov && !o.foc && !o.down && performance.now() > o.until; }
  function kick() { if (!raf && L.some(active)) { last = performance.now(); raf = requestAnimationFrame(tick); } }
  function tick(t) {
    var dt = Math.min(250, t - last), n = 0; last = t; raf = 0;
    L.forEach(function (o) {
      if (!active(o)) return; n++;
      var c = o.el.scrollLeft; if (Math.abs(c - o.pos) > 1.5) o.pos = c;
      o.pos += 0.036 * dt; if (o.pos >= 2 * o.w) o.pos -= o.w; else if (o.pos < o.w) o.pos += o.w;
      o.self = 1; o.el.scrollLeft = o.pos;
    });
    if (n) raf = requestAnimationFrame(tick);
  }
  function hold(o, ms) { o.until = performance.now() + ms; setTimeout(kick, ms + 30); }
  function build(o) {
    var el = o.el, set = o.set, w0 = o.w, ph = w0 ? ((el.scrollLeft - w0) % w0 + w0) % w0 : 0;
    [].forEach.call(el.querySelectorAll('[data-c]'), function (x) { el.removeChild(x); });
    var w = set.getBoundingClientRect().width; if (!w) return; o.w = w;
    for (var i = Math.ceil(2 * el.clientWidth / w) + 1; i--;) {
      var c = set.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.setAttribute('data-c', '');
      [].forEach.call(c.querySelectorAll('a'), function (a) { a.tabIndex = -1; });
      i ? el.appendChild(c) : el.insertBefore(c, set);
    }
    el.scrollLeft = o.pos = w + Math.min(ph, w - 1);
  }
  function settle(o) { var c = o.el.scrollLeft; if (o.foc) return; if (!o.down && c < o.w) o.el.scrollLeft = o.pos = c + o.w; else if (!o.down && c >= 2 * o.w) o.el.scrollLeft = o.pos = c - o.w; else o.pos = c; }
  S.forEach(function (el) {
    var o = { el: el, set: el.firstElementChild, w: 0, pos: 0, until: 0, vis: 1 }, sx, s0, st, mv = 0;
    L.push(o); el.tabIndex = 0; el.classList.add('is-live'); build(o);
    el.addEventListener('scroll', function () { if (o.self) { o.self = 0; return; } hold(o, 2000); clearTimeout(st); st = setTimeout(function () { settle(o); }, 140); }, { passive: true });
    el.addEventListener('touchstart', function () { o.down = 1; }, { passive: true });
    ['touchend', 'touchcancel'].forEach(function (n) { el.addEventListener(n, function () { o.down = 0; hold(o, 2000); }, { passive: true }); });
    el.addEventListener('pointerdown', function (e) { if (e.pointerType == 'mouse' && e.button == 0) { o.down = 1; sx = e.clientX; s0 = el.scrollLeft; mv = 0; } });
    el.addEventListener('pointermove', function (e) {
      if (e.pointerType != 'mouse' || !o.down) return; var d = e.clientX - sx;
      if (!mv && Math.abs(d) > 6) { mv = 1; el.classList.add('is-drag'); el.setPointerCapture(e.pointerId); }
      if (mv) el.scrollLeft = s0 - d;
    });
    ['pointerup', 'pointercancel'].forEach(function (n) { el.addEventListener(n, function (e) { if (e.pointerType != 'mouse') return; o.down = 0; el.classList.remove('is-drag'); if (mv) { hold(o, 2000); setTimeout(function () { mv = 0; }, 0); } else kick(); }); });
    el.addEventListener('dragstart', function (e) { e.preventDefault(); });
    el.addEventListener('click', function (e) { if (mv) { e.preventDefault(); e.stopPropagation(); return; } var a = e.target.closest && e.target.closest('a[data-p]'); if (a) document.dispatchEvent(new CustomEvent('ppc:profile', { detail: a.getAttribute('data-p') })); }, true);
    el.addEventListener('pointerenter', function (e) { if (e.pointerType == 'mouse') o.hov = 1; });
    el.addEventListener('pointerleave', function (e) { if (e.pointerType == 'mouse') { o.hov = 0; kick(); } });
    el.addEventListener('focusin', function (e) {
      try { o.foc = e.target.matches(':focus-visible'); } catch (x) { o.foc = 1; }
      if (e.target == el) return; var r = e.target.getBoundingClientRect(), q = el.getBoundingClientRect(); // keep the focused tile clear of the edge fades
      if (r.left < q.left + 24) el.scrollLeft -= q.left + 24 - r.left; else if (r.right > q.right - 24) el.scrollLeft += r.right - q.right + 24;
    });
    el.addEventListener('focusout', function () { o.foc = 0; kick(); });
    if (window.IntersectionObserver) new IntersectionObserver(function (e) { o.vis = e[0].isIntersecting; kick(); }).observe(el);
    if (window.ResizeObserver) { var rw = el.clientWidth, rt; new ResizeObserver(function () { if (el.clientWidth == rw) return; rw = el.clientWidth; clearTimeout(rt); rt = setTimeout(function () { build(o); kick(); }, 120); }).observe(el); }
  });
  document.addEventListener('visibilitychange', function () { away = document.hidden; kick(); });
  kick();
})();
/* service cards. Hover version (fine pointer, 900px and up): the whole card is the link and one card at a time is lit (the others dim, held across the gaps).
   Touch version: a tap opens the panel inside the photo, its button is the action. Dots follow the snapped card. Without this script the cards are plain links. */
(function () {
  var g = document.querySelector('.svc-photos'); if (!g) return;
  var cards = [].slice.call(g.children), hov = matchMedia('(hover:hover) and (pointer:fine) and (min-width:900px)'), open = null, hot = null, t, sx, sy, mv, at = 0;
  function fire(a) { document.dispatchEvent(new CustomEvent('ppc:service', { detail: a.getAttribute('data-svc') })); }
  function set(c, on) { c.classList.toggle('is-open', !!on); c.firstChild.setAttribute('aria-expanded', on ? 'true' : 'false'); open = on ? c : null; if (on) at = g.scrollLeft; }
  function spot(c) { if (hot === c) return; if (hot) hot.classList.remove('is-hot'); hot = c; g.classList.toggle('is-spot', !!c); if (c) c.classList.add('is-hot'); }
  function mode() {
    var tap = !hov.matches; g.classList.toggle('is-tap', tap); if (open) set(open, 0); spot(null);
    cards.forEach(function (c) {
      var a = c.firstChild, q = c.querySelector('.pc__cta'), n = a.getAttribute('data-svc');
      if (tap) { a.setAttribute('role', 'button'); a.setAttribute('aria-expanded', 'false'); a.setAttribute('aria-label', n); q.removeAttribute('tabindex'); q.removeAttribute('aria-hidden'); }
      else { a.removeAttribute('role'); a.removeAttribute('aria-expanded'); a.setAttribute('aria-label', n + ', get a free quote'); q.tabIndex = -1; q.setAttribute('aria-hidden', 'true'); }
    });
  }
  g.addEventListener('pointerdown', function (e) { sx = e.clientX; sy = e.clientY; mv = 0; });
  g.addEventListener('pointerup', function (e) { mv = Math.hypot(e.clientX - sx, e.clientY - sy) > 8; });
  g.addEventListener('click', function (e) {
    var q = e.target.closest('.pc__cta'), a = e.target.closest('.pc__a');
    if (q) { if (open) set(open, 0); fire(q); return; }
    if (!a) return;
    if (hov.matches) { fire(a); return; }
    e.preventDefault(); e.stopPropagation(); if (mv) return;
    var c = a.parentNode, was = c === open; if (open) set(open, 0); if (!was) set(c, 1);
  }, true);
  g.addEventListener('keydown', function (e) { if (e.key === ' ' && !hov.matches && e.target.classList.contains('pc__a')) { e.preventDefault(); e.target.click(); } });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && open) { var a = open.firstChild; set(open, 0); a.focus(); } });
  document.addEventListener('pointerdown', function (e) { if (open && !open.contains(e.target)) set(open, 0); }, true);
  g.addEventListener('scroll', function () { if (open && Math.abs(g.scrollLeft - at) > 4) set(open, 0); }, { passive: true });
  g.addEventListener('pointerover', function (e) { if (e.pointerType != 'mouse' || !hov.matches) return; var c = e.target.closest('.pc'); if (c) { clearTimeout(t); spot(c); } });
  g.addEventListener('pointerleave', function () { clearTimeout(t); t = setTimeout(function () { spot(null); }, 120); });
  g.addEventListener('focusin', function (e) { var c = e.target.closest('.pc'); if (c && hov.matches) { clearTimeout(t); spot(c); } });
  g.addEventListener('focusout', function (e) { if (!g.contains(e.relatedTarget)) spot(null); });
  /* the active card is the one sitting at the start of the row (the hairline follows it) */
  var raf = 0, cur = -1;
  function sync() {
    raf = 0; var gl = g.getBoundingClientRect().left + (parseFloat(getComputedStyle(g).paddingLeft) || 0), b = 0, bd = 1e9;
    cards.forEach(function (c, i) { var d = Math.abs(c.getBoundingClientRect().left - gl); if (d < bd) { bd = d; b = i; } });
    if (b === cur) return; cur = b;
    cards.forEach(function (c, i) { c.classList.toggle('is-act', i === b); });
  }
  g.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(sync); }, { passive: true });
  (hov.addEventListener ? hov.addEventListener('change', mode) : hov.addListener(mode)); mode(); requestAnimationFrame(sync);

  /* desktop: first 6 cards, the rest behind a quiet button (height animation, hidden while collapsed). Phones keep the whole swipe row. */
  if (cards.length > 6) {
    var wide = matchMedia('(min-width:900px)'), calm = matchMedia('(prefers-reduced-motion: reduce)'), sec = g.closest('section'), wrap = document.createElement('div'), btn = document.createElement('button'), busy = 0;
    wrap.className = 'svc-toggle';
    btn.type = 'button'; btn.className = 'svc-btn'; btn.setAttribute('aria-expanded', 'false'); btn.setAttribute('aria-controls', g.id);
    btn.innerHTML = '<span class="svc-btn__t">Show all services</span><span class="svc-btn__c">' + (cards.length - 6) + ' more</span><svg class="svc-btn__i" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 6l4.5 4.5L12.5 6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    wrap.appendChild(btn); g.parentNode.insertBefore(wrap, g.nextSibling);
    var label = function (on) { btn.setAttribute('aria-expanded', on ? 'true' : 'false'); btn.querySelector('.svc-btn__t').textContent = on ? 'Show fewer' : 'Show all services'; btn.querySelector('.svc-btn__c').hidden = on; wrap.classList.toggle('is-open', on); };
    var extra = cards.slice(6), clean = function () { g.style.height = g.style.overflow = g.style.transition = ''; g.classList.remove('is-anim', 'is-in'); busy = 0; };
    var done = function (cb2) { var f = 0, fin = function () { if (f) return; f = 1; g.removeEventListener('transitionend', te); cb2(); }, te = function (e) { if (e.target === g && e.propertyName === 'height') fin(); }; g.addEventListener('transitionend', te); setTimeout(fin, 520); };
    btn.addEventListener('click', function () {
      if (busy) return; var on = g.hasAttribute('data-collapsed'); label(on);
      if (on) {
        var h0 = g.offsetHeight; g.removeAttribute('data-collapsed');
        if (calm.matches) return;
        var h1 = g.offsetHeight; busy = 1; g.style.height = h0 + 'px'; g.style.overflow = 'hidden'; g.classList.add('is-anim'); g.offsetHeight;
        g.style.transition = 'height .4s cubic-bezier(.2,.7,.1,1)'; g.style.height = h1 + 'px'; g.classList.add('is-in'); done(clean);
      } else {
        if (sec.getBoundingClientRect().top < 0) sec.scrollIntoView({ behavior: calm.matches ? 'auto' : 'smooth', block: 'start' });
        if (document.activeElement && extra.some(function (c) { return c.contains(document.activeElement); })) btn.focus();
        if (calm.matches) { g.setAttribute('data-collapsed', ''); return; }
        var top = g.getBoundingClientRect().top, h2 = cards[5].getBoundingClientRect().bottom - top; busy = 1;
        g.style.height = g.offsetHeight + 'px'; g.style.overflow = 'hidden'; g.classList.add('is-anim', 'is-in'); g.offsetHeight;
        g.style.transition = 'height .4s cubic-bezier(.2,.7,.1,1)'; g.style.height = h2 + 'px'; g.classList.remove('is-in');
        done(function () { g.setAttribute('data-collapsed', ''); clean(); });
      }
    });
    var place = function () { wrap.hidden = !wide.matches; if (!wide.matches) { g.removeAttribute('data-collapsed'); label(true); wrap.classList.remove('is-open'); } else if (!wrap.classList.contains('is-open')) { g.setAttribute('data-collapsed', ''); label(false); } };
    (wide.addEventListener ? wide.addEventListener('change', place) : wide.addListener(place)); place();
  }
})();

/* reviews deck: stacked cards, swipe, arrows, dots, keys, auto cycle (pauses while the visitor hovers, focuses or touches it, a card is expanded, the tab is hidden or the deck is off screen; waits REVIEW_RESUME_MS after a manual change; no autoplay with reduced motion). No JS = plain list. */
(function () {
  var REVIEW_AUTOPLAY_MS = 3500, REVIEW_RESUME_MS = 10000;
  var deck = document.querySelector('.rdeck');
  if (!deck) return;
  var stage = deck.querySelector('.rdeck__stage'), cards = [].slice.call(stage.querySelectorAll('.g-review')), n = cards.length;
  if (n < 2) return;
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cur = 0, auto = 0, idleUntil = 0, held = false, seen = false, timers = [];
  deck.classList.add('is-deck');
  stage.tabIndex = 0; stage.setAttribute('role', 'group'); stage.setAttribute('aria-roledescription', 'carousel'); stage.setAttribute('aria-label', 'Client reviews');
  var ctl = document.createElement('div'); ctl.className = 'rdeck__ctl';
  var chev = function (d) { return '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="' + d + '" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'; };
  var prev = document.createElement('button'); prev.type = 'button'; prev.className = 'rdeck__nav'; prev.setAttribute('aria-label', 'Previous review'); prev.innerHTML = chev('M12 4l-6 6 6 6');
  var next = document.createElement('button'); next.type = 'button'; next.className = 'rdeck__nav'; next.setAttribute('aria-label', 'Next review'); next.innerHTML = chev('M8 4l6 6-6 6');
  var dotsBox = document.createElement('div'); dotsBox.className = 'rdeck__dots'; dotsBox.setAttribute('role', 'group'); dotsBox.setAttribute('aria-label', 'Choose a review');
  var live = document.createElement('p'); live.className = 'rdeck__live'; live.setAttribute('aria-live', 'off'); live.setAttribute('aria-atomic', 'true');
  var dots = cards.map(function (c, i) {
    var d = document.createElement('button'); d.type = 'button'; d.className = 'rdeck__dot'; d.setAttribute('aria-label', 'Show review ' + (i + 1));
    d.addEventListener('click', function () { user(); go(i, true); }); dotsBox.appendChild(d); return d;
  });
  ctl.appendChild(prev); ctl.appendChild(dotsBox); ctl.appendChild(next); deck.appendChild(ctl); deck.appendChild(live);
  cards.forEach(function (c, i) { c.setAttribute('role', 'group'); c.setAttribute('aria-roledescription', 'slide'); c.setAttribute('aria-label', 'Review ' + (i + 1) + ' of ' + n); });
  function later(fn, ms) { var t = setTimeout(function () { timers.splice(timers.indexOf(t), 1); fn(); }, ms); timers.push(t); }
  function collapse(c) { var b = c.querySelector('.g-review__more[aria-expanded="true"]'); if (b) b.click(); }
  function draw(from, dir) {
    cards.forEach(function (c, k) {
      var d = (k - cur + n) % n, pos = d < 3 ? String(d) : 'x';
      c.classList.toggle('is-top', d === 0);
      if (d === 0) { c.removeAttribute('aria-hidden'); c.removeAttribute('inert'); } else { c.setAttribute('aria-hidden', 'true'); c.setAttribute('inert', ''); }
      if (from === null || calm) { c.dataset.pos = pos; return; }
      if (dir < 0 && d === 0) { c.classList.add('no-anim'); c.dataset.pos = 'back'; void c.offsetWidth; requestAnimationFrame(function () { c.classList.remove('no-anim'); c.dataset.pos = '0'; }); }
      else if (dir > 0 && k === from) { c.dataset.pos = 'exit'; later(function () { c.classList.add('no-anim'); c.dataset.pos = pos; void c.offsetWidth; c.classList.remove('no-anim'); }, 520); }
      else c.dataset.pos = pos;
    });
    dots.forEach(function (d, k) { if (k === cur) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
  }
  function go(to, manual) {
    var t = ((to % n) + n) % n; if (t === cur) return;
    live.setAttribute('aria-live', manual ? 'polite' : 'off');
    var from = cur, dir = ((t - cur + n) % n) <= n / 2 ? 1 : -1; collapse(cards[from]); cur = t; draw(from, dir);
    var nm = cards[cur].querySelector('.g-review__name'); live.textContent = (nm ? nm.textContent : 'Review') + ', review ' + (cur + 1) + ' of ' + n;
  }
  function user() { idleUntil = Date.now() + REVIEW_RESUME_MS; }
  function expanded() { return !!stage.querySelector('.g-review__more[aria-expanded="true"]'); }
  function start() { if (!auto && !calm && n > 1) auto = setTimeout(tick, REVIEW_AUTOPLAY_MS); }
  function tick() {
    auto = 0;
    if (!calm && seen && !document.hidden && !held && !expanded() && Date.now() >= idleUntil) go(cur + 1);
    start();
  }
  prev.addEventListener('click', function () { user(); go(cur - 1, true); });
  next.addEventListener('click', function () { user(); go(cur + 1, true); });
  stage.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); user(); go(cur + 1, true); } else if (e.key === 'ArrowLeft') { e.preventDefault(); user(); go(cur - 1, true); } });
  stage.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') held = true; });
  stage.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') held = false; });
  stage.addEventListener('focusin', function () { held = true; });
  stage.addEventListener('focusout', function () { held = false; });
  /* swipe: the top card follows the finger, then flicks away or springs back */
  var x0 = null, y0 = 0, dx = 0, lock = '', top = null;
  stage.addEventListener('pointerdown', function (e) {
    if (e.target.closest('a,button')) return; if (e.pointerType === 'mouse' && e.button !== 0) return;
    x0 = e.clientX; y0 = e.clientY; dx = 0; lock = ''; top = cards[cur]; user();
  });
  stage.addEventListener('pointermove', function (e) {
    if (x0 === null) return; var mx = e.clientX - x0, my = e.clientY - y0;
    if (!lock) { if (Math.abs(mx) < 8 && Math.abs(my) < 8) return; lock = Math.abs(mx) > Math.abs(my) * 1.2 ? 'x' : 'y'; if (lock === 'x') { try { stage.setPointerCapture(e.pointerId); } catch (_) {} top.classList.add('is-drag'); } }
    if (lock !== 'x') return; dx = mx; top.style.transform = 'translate(' + (mx * 0.9) + 'px,0) rotate(' + (mx / 40) + 'deg)'; top.style.opacity = String(Math.max(0.35, 1 - Math.abs(mx) / 420));
  });
  function end(commit) {
    if (x0 === null) return; var t = top, d = dx, l = lock; x0 = null; top = null;
    if (l === 'x') { t.classList.remove('is-drag'); t.style.transform = ''; t.style.opacity = ''; }
    if (commit && l === 'x' && Math.abs(d) > 48) { user(); go(cur + (d < 0 ? 1 : -1), true); }
  }
  stage.addEventListener('pointerup', function () { end(true); });
  stage.addEventListener('pointercancel', function () { end(false); });
  stage.addEventListener('dragstart', function (e) { e.preventDefault(); });
  document.addEventListener('visibilitychange', function () { if (!document.hidden) user(); });
  draw(null, 0);
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { seen = es[0].isIntersecting; }, { threshold: 0.4 }).observe(deck); else seen = true;
  start();
})();

(function () {
  /* Videos (Who we are slot and the video row): the YouTube iframe only exists after a click, Enter or Space. No request to YouTube before that.
     Only one player is alive at a time: starting a video puts every other one back to its poster. */
  var boxes = [].slice.call(document.querySelectorAll('.vid__box[data-yt]'));
  function restore(box) { if (box._f && box._f.parentNode === box) { box.replaceChild(box._btn, box._f); box._f = null; } }
  boxes.forEach(function (box) {
    var a = box.querySelector('.vid__poster'); if (!a) return;
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'vid__btn'; btn.setAttribute('aria-label', 'Play video');
    while (a.firstChild) { if (a.firstChild.className === 'vid__nojs') a.removeChild(a.firstChild); else btn.appendChild(a.firstChild); }
    box.replaceChild(btn, a); box.parentNode.classList.add('is-js'); box._btn = btn;
    btn.addEventListener('click', function () {
      boxes.forEach(function (o) { if (o !== box) restore(o); });
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + box.getAttribute('data-yt') + '?autoplay=1&playsinline=1&rel=0';
      f.title = box.getAttribute('data-title') || 'Video';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.setAttribute('allowfullscreen', ''); f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin'); f.loading = 'lazy';
      box.replaceChild(f, btn); box._f = f; f.focus();
    });
  });
  /* video row: scroll snap rail, arrows only when the cards overflow, arrow keys while focus is inside */
  [].forEach.call(document.querySelectorAll('.vrow__rail'), function (rail) {
    var track = rail.querySelector('.vrow__track'), nav = rail.querySelector('.vrow__nav'), prev = rail.querySelector('.vrow__prev'), next = rail.querySelector('.vrow__next');
    if (!track || !nav) return;
    function step() { var c = track.querySelector('.vrow__item'); return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0) : track.clientWidth; }
    function paint() {
      var over = track.scrollWidth > track.clientWidth + 4;
      nav.hidden = !over; rail.classList.toggle('is-over', over);
      prev.disabled = track.scrollLeft < 4; next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 4;
    }
    function go(d) { track.scrollBy({ left: d * step() * (innerWidth >= 900 ? 2 : 1), behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); }
    prev.addEventListener('click', function () { go(-1); }); next.addEventListener('click', function () { go(1); });
    track.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') { e.preventDefault(); go(1); } else if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); } });
    track.addEventListener('scroll', function () { requestAnimationFrame(paint); }, { passive: true });
    addEventListener('resize', paint); paint(); if (document.fonts && document.fonts.ready) document.fonts.ready.then(paint);
  });
})();

(function () {
  /* Service page gallery: Show more (desktop, more than 6 photos) and a native dialog lightbox. Without JS the tiles are plain links to the large photo. */
  var gal = document.querySelector('[data-gal]'); if (!gal) return;
  var links = [].slice.call(gal.querySelectorAll('.gal__a')); if (!links.length) return;
  gal.classList.add('is-js');
  var more = gal.querySelector('.gal__more');
  if (more && links.length > 6) {
    more.hidden = false;
    more.addEventListener('click', function () {
      var open = gal.classList.toggle('is-open');
      more.setAttribute('aria-expanded', open ? 'true' : 'false');
      more.textContent = open ? 'Show less' : 'Show more';
    });
  }
  if (typeof HTMLDialogElement === 'undefined' || !document.createElement('dialog').showModal) return;
  var dlg, img, count, closeB, prevB, nextB, idx = 0, opener = null, tx = 0, ty = 0;
  var ico = function (d) { return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="' + d + '"/></svg>'; };
  function build() {
    dlg = document.createElement('dialog'); dlg.className = 'lb'; dlg.setAttribute('aria-label', 'Project photos');
    dlg.innerHTML = '<button type="button" class="lb__btn lb__close" aria-label="Close">' + ico('M6 6l12 12M18 6L6 18') + '</button>' +
      '<div class="lb__stage"><img class="lb__img" alt=""></div>' +
      '<button type="button" class="lb__btn lb__prev" aria-label="Previous photo">' + ico('M15 5l-7 7 7 7') + '</button>' +
      '<button type="button" class="lb__btn lb__next" aria-label="Next photo">' + ico('M9 5l7 7-7 7') + '</button>' +
      '<p class="lb__count" aria-live="polite"></p>';
    document.body.appendChild(dlg);
    img = dlg.querySelector('.lb__img'); count = dlg.querySelector('.lb__count');
    closeB = dlg.querySelector('.lb__close'); prevB = dlg.querySelector('.lb__prev'); nextB = dlg.querySelector('.lb__next');
    closeB.addEventListener('click', function () { dlg.close(); });
    prevB.addEventListener('click', function () { show(idx - 1); });
    nextB.addEventListener('click', function () { show(idx + 1); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.className === 'lb__stage') dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      else if (e.key === 'Tab') {
        var f = [closeB, prevB, nextB], i = f.indexOf(document.activeElement);
        e.preventDefault(); f[(i + (e.shiftKey ? f.length - 1 : 1)) % f.length].focus();
      }
    });
    dlg.addEventListener('touchstart', function (e) { var t = e.changedTouches[0]; tx = t.clientX; ty = t.clientY; }, { passive: true });
    dlg.addEventListener('touchend', function (e) {
      var t = e.changedTouches[0], dx = t.clientX - tx, dy = t.clientY - ty;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) show(idx + (dx < 0 ? 1 : -1));
    }, { passive: true });
    dlg.addEventListener('close', function () {
      document.documentElement.style.overflow = '';
      if (opener && opener.focus) opener.focus();
    });
  }
  function show(i) {
    idx = (i + links.length) % links.length;
    var a = links[idx], im = a.querySelector('img');
    img.sizes = '100vw'; img.srcset = a.getAttribute('data-srcset') || ''; img.src = a.getAttribute('href'); img.alt = im ? im.alt : '';
    count.textContent = (idx + 1) + ' of ' + links.length;
    [idx + 1, idx - 1].forEach(function (n) { var p = new Image(); p.src = links[(n + links.length) % links.length].getAttribute('href'); });
  }
  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); if (!dlg) build();
      opener = a; show(i); document.documentElement.style.overflow = 'hidden'; dlg.showModal(); closeB.focus();
    });
  });
})();
