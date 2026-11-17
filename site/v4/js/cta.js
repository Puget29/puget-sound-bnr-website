/* Quick form of the closing call to action (#contact). Uses the shared module (forms.js) for the messages and the sending.
   Chips are a native radio group (arrows move the choice, Space selects). ?service=<value> preselects a chip when the value is one of the Contact page options.
   Spam checks: a hidden "company" field that must stay empty, and a minimum time of 3 s on the page before a submit is accepted. Failures look like a success and send nothing. */
(function () {
  "use strict";
  var form = document.getElementById("quick");
  if (!form || !window.BNRForm) return;
  var $ = function (s) { return form.querySelector(s); };
  var t0 = performance.now();
  var btn = $(".cq__btn"), fail = $(".cq__fail"), ok = $(".cq__ok");
  var fields = [].slice.call(form.querySelectorAll("[data-req]"));

  var svc = (new URLSearchParams(location.search)).get("service") || form.getAttribute("data-service");
  if (svc) { var r = form.querySelector('input[name="service"][value="' + svc.replace(/[^a-z-]/g, "") + '"]'); if (r) r.checked = true; }

  function check(el) {
    var m = BNRForm.msg(el), err = document.getElementById(el.id + "-err");
    el.setAttribute("aria-invalid", m ? "true" : "false");
    if (err) err.textContent = m;
    return !m;
  }
  fields.forEach(function (el) {
    el.addEventListener("blur", function () { if (el.value || el.getAttribute("aria-invalid")) check(el); });
    el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") check(el); });
  });

  function success(demo) {
    form.classList.add("is-done");
    var demoLine = ok.querySelector(".cq__demo"); if (demoLine) demoLine.hidden = !demo;
    ok.hidden = false; ok.focus();
    form.reset();
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var hp = $('input[name="bot-field"], input[name="company"]');
    if (hp) hp.value = "";
    var bad = fields.filter(function (el) { return !check(el); });
    if (bad.length) { bad[0].focus(); return; }
    if (performance.now() - t0 < 3000) { success(false); return; }  /* far too fast for a person: looks like success, sends nothing */
    fail.hidden = true; btn.disabled = true;
    var data = { name: $("#q-name").value.trim(), phone: $("#q-phone").value.trim(), service: (form.querySelector('input[name="service"]:checked') || {}).value || "" };
    BNRForm.send(data, "landing-cta").then(function (res) { btn.disabled = false; success(res.demo); }, function () {
      btn.disabled = false; fail.textContent = BNRForm.error; fail.hidden = false; fail.focus();   /* what was typed stays */
    });
  });
})();
