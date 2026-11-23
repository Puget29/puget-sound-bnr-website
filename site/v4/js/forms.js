/* Shared form module: Contact page form, service page forms and the About quick form.
   Netlify detects the form from the static HTML (name="lead", data-netlify="true", a hidden form-name field).
   Submit is sent as a URL-encoded POST to /, which is where Netlify stores the submission.
   The hidden company field is the Netlify honeypot. On success the page pushes generate_lead to dataLayer.
   Never put a private key or secret in this file. */
(function () {
  "use strict";
  var FORM = { endpoint: "/" };
  var ERR = "Your request was not sent. Please try again or call (425) 696-7586.";
  var busy = false;
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

  function setHidden(form, name, value) {
    if (!form) return;
    var el = form.querySelector('input[type="hidden"][name="' + name + '"]');
    if (el) el.value = String(value == null ? "" : value).slice(0, 300);
  }

  /* send(data, source, form): data is a FormData. Resolves { ok } or rejects.
     Netlify returns an HTML page, not JSON. A 2xx response means the submission was stored. */
  function send(data, source, form) {
    var svc = serviceName(form, data), attr = attribution();
    setHidden(form, "source", source || (form && form.getAttribute("data-source")) || "");
    setHidden(form, "origin_page", location.href.split("#")[0]);
    setHidden(form, "origin_city", "General");
    if (svc && form && !form.querySelector('select[name="service"], input[name="service"]')) setHidden(form, "service", svc);
    Object.keys(attr).forEach(function (k) { setHidden(form, k, attr[k]); });
    var fd = form ? new FormData(form) : data;
    var body = new URLSearchParams();
    fd.forEach(function (value, key) { body.append(key, value); });
    if (svc) { body.delete("service"); body.set("service", svc); }
    if (!body.get("form-name")) body.set("form-name", "lead");
    if (busy) return Promise.reject(new Error("busy"));
    busy = true;
    var ctl = "AbortController" in window ? new AbortController() : null, timer = setTimeout(function () { if (ctl) ctl.abort(); }, 10000);
    return fetch(FORM.endpoint, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body.toString(), signal: ctl ? ctl.signal : undefined })
      .then(function (r) {
        clearTimeout(timer); busy = false;
        if (!r.ok) throw new Error("bad");
        dl.push({ event: "generate_lead", service: svc || body.get("service") || "", city: "", source: body.get("source") || "" });
        return { ok: true, demo: false };
      }, function (e) { clearTimeout(timer); busy = false; throw e; });
  }

  window.BNRForm = { config: FORM, msg: msg, send: send, error: ERR };
})();
