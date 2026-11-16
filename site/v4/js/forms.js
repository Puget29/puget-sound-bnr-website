/* Shared form module: Contact page form, service page forms and the About quick form. Every form posts to the same lead handler as the PPC pages:
   POST /wp-json/bnr/v1/lead (plugin bnr-lead-handler), JSON, fields name, phone, zip, email, service, origin_service, origin_city, origin_page, elapsed,
   website (honeypot, always empty from people), plus the campaign parameters that came with the visit. On success the page pushes the generate_lead event
   to dataLayer. The route is on the same site, so it works on the hidden preview addresses too.
   Never put a private key or secret in this file. */
(function () {
  "use strict";
  var FORM = { endpoint: "/wp-json/bnr/v1/lead" };
  var ERR = "Your request was not sent. Please try again or call (425) 696-4004.";
  var busy = false, loadedAt = Date.now();
  var dl = window.dataLayer = window.dataLayer || [];
  var PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "msclkid", "fbclid"];

  /* one set of messages for every form: required, phone, email, ZIP */
  function msg(el) {
    var v = (el.value || "").trim(), kind = el.getAttribute("data-kind");
    if (el.hasAttribute("data-req") && !v) return "Please fill this in.";
    if (v && kind === "phone" && v.replace(/\D/g, "").length < 10) return "Enter a phone number with area code.";
    if (v && kind === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return "Enter a valid email address.";
    if (v && kind === "zip" && !/^\d{5}$/.test(v)) return "Enter a 5 digit ZIP code.";
    return "";
  }

  /* the visible name of the chosen service (chip label or select text), the handler wants words, not slugs */
  function serviceName(form, fd) {
    var sel = form && form.querySelector('select[name="service"]');
    if (sel && sel.selectedOptions && sel.selectedOptions[0] && sel.value) return sel.selectedOptions[0].textContent.trim();
    var chip = form && form.querySelector('input[name="service"]:checked');
    if (chip) { var sp = chip.parentNode.querySelector("span"); return (sp ? sp.textContent : chip.value).trim(); }
    return (fd && fd.get && fd.get("service")) || "";
  }

  function attribution() {
    var o = {}, q = new URLSearchParams(location.search), keep = null;
    try { keep = JSON.parse(sessionStorage.getItem("bnr-attr") || "null"); } catch (e) {}
    keep = keep || { first_seen: new Date().toISOString(), landing_page: location.pathname, referrer: (document.referrer || "").slice(0, 200) };
    PARAMS.forEach(function (k) { if (q.get(k)) keep[k] = q.get(k).slice(0, 200); });
    try { sessionStorage.setItem("bnr-attr", JSON.stringify(keep)); } catch (e) {}
    Object.keys(keep).forEach(function (k) { o[k] = keep[k]; });
    return o;
  }
  attribution();

  /* send(data, source, form): data is a FormData. Resolves { ok } or rejects. */
  function send(data, source, form) {
    var svc = serviceName(form, data), o = attribution();
    o.name = (data.get("name") || "").toString().trim(); o.phone = (data.get("phone") || "").toString().trim();
    o.zip = (data.get("zip") || "").toString().trim(); o.email = (data.get("email") || "").toString().trim();
    o.service = svc || (data.get("origin_service") || "").toString();
    o.origin_service = (data.get("origin_service") || svc || "").toString();
    o.origin_city = "General";                                  /* the main site has no city pages, the handler shows the page address instead */
    o.origin_page = location.href.split("#")[0];
    o.website = "";                                             /* honeypot: the visible Company trap is checked by the page and never reaches here */
    o.elapsed = Date.now() - loadedAt;
    o.source = source || "";
    if (busy) return Promise.reject(new Error("busy"));
    busy = true;
    var ctl = "AbortController" in window ? new AbortController() : null, timer = setTimeout(function () { if (ctl) ctl.abort(); }, 10000);
    return fetch(FORM.endpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(o), signal: ctl ? ctl.signal : undefined })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || j.ok === false || j.success === false) throw new Error("bad"); return j; }); })
      .then(function () { clearTimeout(timer); busy = false; dl.push({ event: "generate_lead", service: o.service, city: "", source: o.source }); return { ok: true, demo: false }; },
            function (e) { clearTimeout(timer); busy = false; throw e; });
  }

  window.BNRForm = { config: FORM, msg: msg, send: send, error: ERR };
})();
