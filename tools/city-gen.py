# City pages (hidden preview). Exec'd from v4-gen-pages.py after the service pages, so it shares their helpers
# (_k_blocks, _k_section, _k_faq, _k_gallery, _reviews, _form, lead_block, head, header, footer, ...).
#
# Inputs:  content/city-template.md  shared copy with {{city}} and the local placeholders
#          data/city-facts.json      local facts per city slug (meta_description, intro_local, local_body, local_bullets, faq_local)
#          data/city-list.json       every city: name, slug, path
# Output:  service-areas/<slug>/index.html  (preview address /home-new/service-areas/<slug>/)
# A city with no entry in city-facts.json is skipped and its name is printed. There is no generic fallback text.
# Set V4_CITY=<slug> to build one city only.
import re as _cr

_CITY_KEYS = ("meta_description", "intro_local", "local_body", "local_bullets", "faq_local")

def _c_expand(template, city, facts):
    """Fill the template. Local bullets and FAQs expand into markdown lists and question blocks."""
    bullets = "\n".join("- " + b for b in facts["local_bullets"])
    faqs = "\n\n".join(f"### {f['q']}\n\n{f['a']}" for f in facts["faq_local"])
    text = template
    for key, val in (("meta_description", facts["meta_description"]), ("intro_local", facts["intro_local"]),
                     ("local_body", facts["local_body"]), ("local_bullets", bullets), ("faq_local", faqs)):
        text = text.replace("{{" + key + "}}", val)
    text = text.replace("{{city}}", city)
    if "{{" in text: raise SystemExit(f"city page {city}: unfilled placeholder in the template")
    return text

def _c_parse(text, city, expected_sections=8):
    meta = {}
    for key in ("TITLE TAG", "META DESCRIPTION", "H1"):
        m = _cr.search(r"(?m)^" + _cr.escape(key) + r":\s*(.+)$", text)
        if not m: raise SystemExit(f"city page {city}: template is missing {key}")
        meta[key] = m.group(1).strip()
    start = text.find("## ")
    sections, cur = [], None
    for line in text[start:].splitlines():
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "lines": []}; sections.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    if len(sections) != expected_sections: raise SystemExit(f"city page {city}: {len(sections)} sections, expected {expected_sections}")
    return meta, sections

def _city_page(city, slug, facts, template):
    for k in _CITY_KEYS:
        if k not in facts: raise SystemExit(f"city page {city}: data/city-facts.json is missing {k}")
    meta, sections = _c_parse(_c_expand(template, city, facts), city)
    intro = _k_blocks(sections[0]["lines"])
    if not intro or intro[0][0] != "paragraph": raise SystemExit(f"city page {city}: introduction must begin with a paragraph")
    hero_lede = _k_inline(intro[0][1])

    keys = ("intro", "services", "local", "process", "why", "faq", "areas", "closing")
    ids = {s["title"]: f"city-{keys[i]}" for i, s in enumerate(sections)}
    nav = '<nav class="kitchen-jump" aria-label="On this page"><div class="wrap"><strong>On this page</strong><ul>' + "".join(
        f'<li><a href="#{ids[s["title"]]}">{esc(s["title"])}</a></li>' for s in sections) + "</ul></div></nav>"

    path = f"/service-areas/{slug}/"
    hero_photo, closing_photo_id = "project-43", "project-45"
    # Desktop hero background photo, the same for every city. "solo" drops the side photo card on desktop (phones keep the card).
    bg_photo, hero_variant = "project-47", _os.environ.get("CITY_HERO", "solo")
    _check_real(bg_photo)
    bq = _PJ[bg_photo]
    bg_img = (f'<img src="{_src(bg_photo, 1440)}" srcset="{_src(bg_photo, 960)} 960w, {_src(bg_photo, 1440)} 1440w" sizes="100vw" width="{bq["w"]}" height="{bq["h"]}" alt="" '
              f'loading="lazy" decoding="async" style="object-position:{esc(bq.get("objectPosition", "50% 50%"))}">')
    preload = (f'<link rel="preload" as="image" href="{_src(hero_photo, 960)}" type="image/webp" media="(max-width: 900px)" fetchpriority="high">\n'
               f'<link rel="preload" as="image" href="{_src(bg_photo, 1440)}" type="image/webp" media="(min-width: 901px)" fetchpriority="high">\n')
    jobs = [pid for pid in _LAST if _PJ.get(pid, {}).get("real") is True and _PJ[pid].get("stock") is False]
    sv = {"gallery": jobs, "galleryHeading": "Check our last jobs", "galleryIntro": "Photos from our own recent work. Tap a photo to see it larger.", "workName": "recent"}

    hero = f'''<main id="main" class="long-service-page">
<section class="page-hero sv-hero city-hero city-hero--{hero_variant}" aria-labelledby="city-h1">
  <div class="city-hero__bg" aria-hidden="true">{bg_img}</div>
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_UP}">Home</a><span aria-hidden="true">/</span><span aria-current="page">{esc(city)}</span></nav>
      <h1 id="city-h1">{esc(meta["H1"])}</h1>
      <p class="lede" style="margin-bottom:30px">{hero_lede}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(hero_photo, "(min-width:901px) 46vw, 92vw", "", hero_variant != "solo", None)}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
{nav}
'''
    S = lambda i, surf, layout, cls="kitchen-list": _k_section(sections[i]["title"], ids[sections[i]["title"]], surf, _k_blocks(sections[i]["lines"]), layout, cls)
    parts = [hero,
             _k_section(sections[0]["title"], ids[sections[0]["title"]], "sec--stone", intro[1:], "split"),
             S(1, "sec--slab", "split", "sv-offer kitchen-check-list"),
             S(2, "sec--stone", "split", "sv-offer kitchen-check-list"),
             S(3, "sec--slab", "split"),  # the numbered steps are styled for a dark surface
             _k_gallery(sv, "city"),
             S(4, "sec--slab", "full", "kitchen-list kitchen-why-list"),
             _reviews()]
    faq_section, faq_pairs = _k_faq(_k_blocks(sections[5]["lines"]), "cityfaq", sections[5]["title"], 6)
    parts.append(faq_section.replace('id="cityfaq-faq"', f'id="{ids[sections[5]["title"]]}"').replace('aria-labelledby="cityfaq-faq-h"', 'aria-labelledby="cityfaq-faq-h"'))
    area = S(6, "sec--slab", "split").replace('class="sec sec--slab kitchen-section"', 'class="sec sec--slab kitchen-section long-service-area"', 1)
    parts.append(area)
    parts.append(S(7, "sec--stone", "split"))
    form_sv = {"chip": "", "formHeading": "Free consultation", "formService": f"{city} city page", "city": city}
    form = lead_block("contact", "city-form-h", esc(f"Tell us about your {city} project."), "Send a few details and we will take it from there. We reply within one business day.",
                      _form(form_sv, "city-page"), pimg(_UP, closing_photo_id, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    ld = [org_ld(), _crumb_ld([("Home", "/"), (city, path)]),
          {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "Puget Sound Builders & Renovation", "telephone": PHONE_TEL,
           "areaServed": {"@type": "City", "name": city}, "url": SITE + path},
          faq_ld([(q, [a]) for q, a in faq_pairs])]
    page = (head(meta["TITLE TAG"], meta["META DESCRIPTION"], path, _UP, preload, ld)
            + '<body class="long-service-page-body">\n<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "areas", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    shown = _cr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_cr.S)
    if "WhatsApp" in shown or "wa.me" in shown: raise SystemExit(f"city page {city}: must not include WhatsApp")
    for bad in (chr(0x2014), chr(0x2013)):
        if bad in shown: raise SystemExit(f"city page {city}: a dash in the page")
    w(f"service-areas/{slug}/index.html", page)

def _build_cities():
    template = io.open(_os.path.join(_P, "content", "city-template.md"), encoding="utf-8").read()
    facts = _j.load(io.open(_os.path.join(_P, "data", "city-facts.json"), encoding="utf-8"))
    cities = _j.load(io.open(_os.path.join(_P, "data", "city-list.json"), encoding="utf-8"))
    only = _os.environ.get("V4_CITY", "").strip().lower()
    for c in cities:
        if only and c["slug"] != only: continue
        if c["slug"] not in facts:
            print(f"city-gen: skipped {c['name']} (no entry in data/city-facts.json)")
            continue
        _city_page(c["name"], c["slug"], facts[c["slug"]], template)

_build_cities()

# ---- Areas We Serve hub: service-areas/index.html (preview /home-new/service-areas/), links to every city page ----
def _build_hub():
    cities = _j.load(io.open(_os.path.join(_P, "data", "city-list.json"), encoding="utf-8"))
    template = io.open(_os.path.join(_P, "content", "city-template.md"), encoding="utf-8").read()
    svc_lines = [l for l in template.splitlines() if l.startswith("- **[") and "/our-services/" in l]
    if len(svc_lines) != 8: raise SystemExit("hub: expected 8 service lines in content/city-template.md")
    title = "Areas We Serve | Seattle, Bellevue and Puget Sound | Puget Sound BNR"
    desc = "Puget Sound BNR is a Bellevue general contractor serving more than 80 cities across the Puget Sound region. Find your city and call (425) 696-4004."
    lede = ("Puget Sound BNR is a general contractor based in Bellevue, Washington. We remodel, repair and build for homeowners in Seattle, Bellevue and communities "
            "across the Puget Sound region. Find your city below to see how we work in your area.")
    ctas = "[Book your free consultation]   [Call (425) 696-4004]"
    path = "/service-areas/"
    hero_photo, closing_photo_id, bg_photo = "project-43", "project-45", "project-47"
    _check_real(bg_photo); bq = _PJ[bg_photo]
    bg_img = (f'<img src="{_src(bg_photo, 1440)}" srcset="{_src(bg_photo, 960)} 960w, {_src(bg_photo, 1440)} 1440w" sizes="100vw" width="{bq["w"]}" height="{bq["h"]}" alt="" '
              f'loading="lazy" decoding="async" style="object-position:{esc(bq.get("objectPosition", "50% 50%"))}">')
    preload = (f'<link rel="preload" as="image" href="{_src(hero_photo, 960)}" type="image/webp" media="(max-width: 900px)" fetchpriority="high">\n'
               f'<link rel="preload" as="image" href="{_src(bg_photo, 1440)}" type="image/webp" media="(min-width: 901px)" fetchpriority="high">\n')
    ids = {"grid": "areas-find", "svc": "areas-services", "dont": "areas-missing", "close": "areas-closing"}
    heads = {"grid": "Find Your City", "svc": "Services in Every City", "dont": "Don't See Your City?", "close": "Let's Build Something Exceptional"}
    nav = '<nav class="kitchen-jump" aria-label="On this page"><div class="wrap"><strong>On this page</strong><ul>' + "".join(
        f'<li><a href="#{ids[k]}">{esc(heads[k])}</a></li>' for k in ("grid", "svc", "dont", "close")) + "</ul></div></nav>"
    hero = f"""<main id="main" class="long-service-page">
<section class="page-hero sv-hero city-hero city-hero--solo" aria-labelledby="areas-h1">
  <div class="city-hero__bg" aria-hidden="true">{bg_img}</div>
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_UP}">Home</a><span aria-hidden="true">/</span><span aria-current="page">Areas We Serve</span></nav>
      <h1 id="areas-h1">Areas We Serve</h1>
      <p class="lede" style="margin-bottom:30px">{esc(lede)}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(hero_photo, "(min-width:901px) 46vw, 92vw", "", False, None)}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
{nav}
"""
    names = sorted(cities, key=lambda c: c["name"].lower())
    grid_items = "".join(f'<li><a href="/service-areas/{c["slug"]}/">{esc(c["name"])}</a></li>' for c in names)
    grid_sec = (f'<section class="sec sec--stone kitchen-section area-sec" id="{ids["grid"]}" aria-labelledby="{ids["grid"]}-h">'
                f'<div class="wrap kitchen-layout"><div class="kitchen-layout__head"><h2 class="h2" id="{ids["grid"]}-h">{heads["grid"]}</h2></div>'
                f'<div class="kitchen-copy"><ul class="area-grid">{grid_items}</ul></div></div></section>\n')
    svc_sec = _k_section(heads["svc"], ids["svc"], "sec--slab", _k_blocks(svc_lines), "split", "sv-offer kitchen-check-list")
    dont_sec = _k_section(heads["dont"], ids["dont"], "sec--stone", _k_blocks(["Tell us where you are and we will let you know if we can take on your project.", "", ctas]), "split")
    close_lines = ["If you are thinking about a project, the first step is simple. [Book your free consultation] or call (425) 696-4004, and we will come to your home, look at the project and tell you honestly what it needs.",
                   "", "### Related pages", "", "Explore our [services](/our-services/), see our [projects](/remodeling-projects/), or read about [who we are](/about/)."]
    close_sec = _k_section(heads["close"], ids["close"], "sec--stone", _k_blocks(close_lines), "split")
    form_sv = {"chip": "", "formHeading": "Free consultation", "formService": "Areas we serve page"}
    form = lead_block("contact", "areas-form-h", "Tell us about your project.", "Send a few details and we will take it from there. We reply within one business day.",
                      _form(form_sv, "areas-page"), pimg(_UP, closing_photo_id, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts = [hero, grid_sec, svc_sec, dont_sec, _reviews(), close_sec, form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n"]
    ld = [org_ld(), _crumb_ld([("Home", "/"), ("Areas We Serve", path)])]
    page = (head(title, desc, path, _UP, preload, ld)
            + '<body class="long-service-page-body">\n<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "areas", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    shown = _cr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_cr.S)
    if "WhatsApp" in shown or "wa.me" in shown: raise SystemExit("hub: must not include WhatsApp")
    for bad in (chr(0x2014), chr(0x2013)):
        if bad in shown: raise SystemExit("hub: a dash in the page")
    if grid_items.count("<li>") != len(cities): raise SystemExit("hub: city grid mismatch")
    w("service-areas/index.html", page)

if not _os.environ.get("V4_CITY", "").strip(): _build_hub()
