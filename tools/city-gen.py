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
    form_sv = {"chip": "", "formHeading": "Free consultation", "formService": f"{city} city page"}
    form = lead_block("contact", "city-form-h", esc(f"Tell us about your {city} project."), "Send a few details and we will take it from there. We reply within one business day.",
                      _form(form_sv, "city-page"), pimg(_UP, closing_photo_id, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    ld = [org_ld(), _crumb_ld([("Home", "/"), (city, path)]),
          {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "Puget Sound Builders & Renovation - Kitchen & Bathroom", "telephone": PHONE_TEL,
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
    facts = _j.load(io.open(_os.path.join(_P, "data", "city-facts.json"), encoding="utf-8"))
    local = _j.load(io.open(_os.path.join(_P, "data", "city-local.json"), encoding="utf-8"))
    cities = _j.load(io.open(_os.path.join(_P, "data", "city-list.json"), encoding="utf-8"))
    _content_path = _os.path.join(_P, "data", "city-content.json")
    content = _j.load(io.open(_content_path, encoding="utf-8")) if _os.path.exists(_content_path) else {}
    only = _os.environ.get("V4_CITY", "").strip().lower()
    for c in cities:
        if only and c["slug"] != only: continue
        if c["slug"] not in facts:
            print(f"city-gen: skipped {c['name']} (no entry in data/city-facts.json)")
            continue
        _city_page_v2(c["name"], c["slug"], facts[c["slug"]], local.get(c["slug"], {}), content.get(c["slug"], {}))

# _build_cities() is called further down, after _city_page_v2 is defined.

# ================================================================ Algona pilot ====
# Optimized Algona location page: reuses the finalized service-page (km) design + helpers, with
# verified Algona-specific local content and two distinct maps. Algona is skipped in _build_cities so
# this is the only renderer for /service-areas/algona/. Pilot only, no other city page is affected.
_ALGONA_CSS = """<style>
.km #services .sec__head{text-align:center;margin-left:auto;margin-right:auto}
.km #services .sec__head .lede{margin-left:auto;margin-right:auto}
.km #reviews .rvw__head{justify-items:center;text-align:center;justify-self:center}
.km #reviews .rvw__head .lede{margin-left:auto;margin-right:auto}
.km #reviews .rlg-review-cta{text-align:center !important}
.km .algona-dir{display:grid;grid-template-columns:1.05fr .95fr;gap:26px;align-items:stretch;margin-top:28px}
.km .algona-dir__poi{list-style:none;margin:0;padding:0;display:grid;gap:12px;align-content:start}
.km .algona-dir__poi li{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.km .algona-dir__poi h3{margin:0 0 4px;font-size:1rem}
.km .algona-dir__poi p{margin:0;font-size:.92rem;line-height:1.5}
.km .algona-map{border-radius:16px;overflow:hidden;min-height:360px;border:1px solid rgba(0,0,0,.12)}
.km .algona-map iframe{width:100%;height:100%;min-height:360px;border:0;display:block}
@media (max-width:820px){.km .algona-dir{grid-template-columns:1fr}.km .algona-map,.km .algona-map iframe{min-height:300px}}
</style>"""


_CITY_NAME = {c["slug"]: c["name"] for c in _j.load(io.open(_os.path.join(_P, "data", "city-list.json"), encoding="utf-8"))}


def _homes_paragraphs(body):
    """Break the local-homes prose into 2-3 short paragraphs (same words), so the section reads as
    chunks instead of one long block. Respects existing blank-line breaks, then splits any block of
    4+ sentences into balanced 2-3 sentence paragraphs."""
    paras = []
    for blk in [b.strip() for b in body.split("\n\n") if b.strip()]:
        sents = [s for s in _cr.split(r"(?<=[.!?])\s+", blk) if s.strip()]
        n = len(sents)
        if n <= 3:
            paras.append(" ".join(sents))
        else:
            k = 2 if n <= 5 else 3
            size = (n + k - 1) // k
            for i in range(0, n, size):
                paras.append(" ".join(sents[i:i + size]))
    return paras


def _city_page_v2(city, slug, facts, local, content=None):
    # Finalized location-page design (same as the Algona pilot), data driven for every city. Generic and
    # factual sections (services, reviews, work, process steps, CTA) are reused; the per-city unique content
    # (hero, the four SEO sections, kitchen/bath, local considerations, local prose, FAQs, optional section
    # intros and refined POI descriptions) comes from data/city-content.json when present, with a safe
    # fallback to the shared template (data/city-facts.json + data/city-local.json) so partial builds work.
    C = content or {}
    path = f"/service-areas/{slug}/"
    hero_photo = "location-pages-hero"  # client-supplied hero image shared by all location pages
    GBP_MAP = _KM_MAP_SRC  # business place embed (shows the business name), used sitewide
    DIR_MAP = ("https://maps.google.com/maps?saddr=Puget+Sound+Builders+%26+Renovation+-+Kitchen+%26+Bathroom,+11170+NE+10th+St,+Bellevue,+WA+98004"
               "&daddr=" + city.replace(" ", "+") + ",+WA&output=embed")

    hero_desc = C.get("hero_desc") or f"Home remodeling in {city} that plans kitchens, bathrooms and whole home updates around how your house is actually built, used and lived in."
    hero_lede = _k_inline(hero_desc)
    hero = f'''<main id="main" class="long-service-page km">
<section class="page-hero sv-hero" aria-labelledby="{slug}-h1">
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_UP}">Home</a><span aria-hidden="true">/</span><a href="/service-areas/">Service areas</a><span aria-hidden="true">/</span><span aria-current="page">{esc(city)}</span></nav>
      <h1 id="{slug}-h1">Home Remodeling in {esc(city)}, WA</h1>
      <p class="lede" style="margin-bottom:30px">{hero_lede}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(hero_photo, "(min-width:901px) 46vw, 92vw", "", True, None)}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
'''
    parts = [hero]

    why_cards = [
        ("Local and accountable", f"A general contractor serving {city} and the surrounding communities, licensed in Washington, fully insured and bonded."),
        ("Clear communication", "You know the plan, the scope and the next step at every stage, and you can reach us at " + PHONE_TXT + "."),
        ("Planned scope", f"We agree on the work and the materials before we begin, so your {city} project stays predictable."),
        ("Care with the details", "The small decisions, from trim to fixtures, get the same attention as the big ones."),
        ("A record you can check", "More than 5 years of work and five stars on Google from homeowners across the area."),
    ]
    why_lede = C.get("why_intro") or "A local team you can hold accountable, from the first consultation to the final walkthrough."
    parts.append(_km_feature_section(slug + "-why", "sec--slab", "km-svc", f"Why {city} Homeowners Choose Puget Sound BNR",
                 why_lede, why_cards, _KM_WHY_ICONS))

    parts.append(services_section()
                 .replace("What we build for Eastside homes.", "What We Build and Renovate")
                 .replace("We build across Bellevue and the Eastside, from kitchens and bathrooms to ADU and DADU additions.",
                          "We build and renovate across the Puget Sound region, from kitchens and bathrooms to ADU and DADU additions.")
                 .replace("Roofing for Eastside homes", "Roofing for homes across the region")
                 .replace("</section>", '  <div class="wrap" style="text-align:center;margin-top:34px"><a class="btn btn--primary" href="' + URLS["services"] + '">View all services' + BTN_ARROW + "</a></div>\n</section>", 1))

    if C.get("planning"):
        _pl = C["planning"]
        plan_cards = [(t, d) for t, d in _pl["cards"]]
        plan_h2, plan_lede = _pl["h2"], _pl["intro"]
    else:
        plan_cards = [
            ("Name and rank your priorities", "List what is not working, from a dated kitchen to a leaking roof, then decide which issues the budget should solve first."),
            ("Think about the whole home", "A single update is often the moment to plan related work, so the house moves in one direction instead of in pieces."),
            ("Check behind the walls", f"{city} homes range from older houses to newer builds, so we look at condition and systems before finalizing a plan."),
            ("Plan permits and scope early", "Structural work, roofs, decks and ADUs usually need a permit, and a settled scope keeps surprises down."),
        ]
        plan_h2 = f"Home Remodeling in {city}: Planning Your Project and Priorities"
        plan_lede = f"A home remodeling project in {city} goes best when a few things are settled before any finish is chosen. Start with these four."
    parts.append(_km_feature_section(slug + "-planning", "sec--slab", "km-svc", plan_h2, plan_lede, plan_cards, _KM_SVC_ICONS))

    parts.append(wrf_reviews_section())
    parts.append(work_section().replace("assets/projects/", _UP + "assets/projects/"))

    proc = [C.get("process_intro") or "We keep the process predictable so you always know the next step.", "",
            f"1. **Free consultation.** Tell us about your {city} home and what you want to change. We look at the space and talk through goals, priorities and budget range.",
            "2. **Design and material selection.** We turn your ideas into a plan for the layout and scope, then help you compare materials and finishes, agreed before work begins.",
            "3. **Construction.** Our team carries out the agreed work and keeps you informed as the project comes together.",
            "4. **Final walkthrough.** We review the finished work with you and confirm every detail before we call it done."]
    parts.append(_k_section("A Clear Remodeling Process From Start to Finish", slug + "-steps", "sec--slab", _k_blocks(proc), "split"))

    if C.get("kitchen_bath"):
        _kb = C["kitchen_bath"]
        kb_h2 = _kb["h2"]
        _coord = _kb.get("coordinated") or "When a kitchen or bathroom connects to wider work, we plan it together so the result feels intentional, not assembled from separate jobs."
        seo2 = [_kb["intro"], "",
                f"- **Kitchen remodeling in {city}.** " + _kb["kitchen"] + " See our [kitchen remodeling](/our-services/kitchen-remodeling/) page for the full scope.",
                f"- **Bathroom remodeling in {city}.** " + _kb["bathroom"] + " See our [bathroom remodeling](/our-services/bathroom-remodeling/) page for details.",
                "- **One coordinated project.** " + _coord]
    else:
        kb_h2 = f"Kitchen and Bathroom Remodeling for {city} Homes"
        seo2 = [f"Kitchens and bathrooms are the rooms {city} homeowners remodel most, and they are where good planning pays off. We give both meaningful attention as part of a home remodeling project, or as standalone updates.", "",
                f"- **Kitchen remodeling in {city}.** New layouts, cabinets, countertops, backsplashes and lighting, planned around how you actually cook. See our [kitchen remodeling](/our-services/kitchen-remodeling/) page for the full scope.",
                f"- **Bathroom remodeling in {city}.** Showers, tubs, vanities, tile and fixtures, built on proper waterproofing and ventilation. See our [bathroom remodeling](/our-services/bathroom-remodeling/) page for details.",
                "- **One coordinated project.** When a kitchen or bathroom connects to wider work, we plan it together so the result feels intentional, not assembled from separate jobs."]
    parts.append(_k_section(kb_h2, slug + "-kb", "sec--slab", _k_blocks(seo2), "full"))

    # SEO section: per-city local considerations (from city-content.json, else city-facts.json bullets).
    if C.get("considerations"):
        _co = C["considerations"]
        seo3 = [_co["intro"], ""] + [f"- **{t}.** {d}" for t, d in _co["bullets"]]
        cons_h2 = _co["h2"]
    else:
        seo3 = [f"A few local details are worth understanding before you start a home renovation in {city}. We work through each of these with you during planning so there are no surprises later.", ""] + ["- " + b for b in facts["local_bullets"]]
        cons_h2 = f"What {city} Homeowners Should Know Before a Home Renovation"
    parts.append(_k_section(cons_h2, slug + "-local", "sec--stone", _k_blocks(seo3), "full"))

    # SEO section: per-city local prose (from city-content.json, else city-facts.json local_body).
    # Two-column split layout, prose broken into 2-3 short paragraphs so it is not one long block.
    if C.get("homes"):
        _ho = C["homes"]
        homes_h2 = _ho["h2"]
        _hpar = _homes_paragraphs(_ho["body"])
    else:
        homes_h2 = f"Remodeling Homes in {city}"
        _hpar = _homes_paragraphs(facts["local_body"])
    _hlines = []
    for _p in _hpar:
        _hlines += [_p, ""]
    parts.append(_k_section(homes_h2, slug + "-homes", "sec--slab", _k_blocks(_hlines), "split"))

    nearby = [(s, _CITY_NAME[s]) for s in local.get("nearby", []) if s in _CITY_NAME and s != slug]
    area_links = "".join('<li><a href="/service-areas/' + s + '/">' + esc(n) + "</a></li>" for s, n in nearby)
    areas_lede = esc(C["areas_intro"]) if C.get("areas_intro") else ('We are based in Bellevue and serve ' + esc(city) + ' along with the surrounding communities. We come to you, there is no office to visit in ' + esc(city) + '.')
    parts.append('<section class="sec sec--slab km-areas" id="' + slug + '-areas" aria-labelledby="' + slug + '-areas-h">\n'
                 '  <div class="wrap">\n'
                 '    <div class="sec__head rv"><h2 class="h2" id="' + slug + '-areas-h">Serving ' + esc(city) + ' and Nearby Communities</h2>'
                 '<p class="lede">' + areas_lede + '</p></div>\n'
                 '    <div class="km-areas__grid">\n'
                 '      <div class="km-areas__map"><iframe src="' + GBP_MAP + '" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen title="Puget Sound Builders and Renovation on Google Maps, Bellevue"></iframe></div>\n'
                 '      <div class="km-areas__panel"><p class="lede" style="margin:0 0 2px;font-size:1rem">Nearby communities we also serve:</p><ul class="km-areas__list">' + area_links + "</ul>"
                 '<a class="btn btn--ghost km-areas__all" href="/service-areas/">See all service areas</a></div>\n'
                 "    </div>\n  </div>\n</section>\n")

    _pois = C.get("pois") or local.get("pois", [])
    poi_items = "".join("<li><h3>" + esc(t) + "</h3><p>" + esc(d) + "</p></li>" for t, d in _pois)
    parts.append('<section class="sec sec--stone km-poi" id="' + slug + '-poi" aria-labelledby="' + slug + '-poi-h">\n'
                 '  <div class="wrap">\n'
                 '    <div class="sec__head rv"><h2 class="h2" id="' + slug + '-poi-h">Around ' + esc(city) + ' and How We Get There</h2>'
                 '<p class="lede">A few local landmarks for reference, and the route our crews take from our Bellevue base to ' + esc(city) + '. We travel to you, so these are reference points, not project sites.</p></div>\n'
                 '    <div class="algona-dir">\n'
                 '      <ul class="algona-dir__poi">' + poi_items + "</ul>\n"
                 '      <div class="algona-map"><iframe src="' + DIR_MAP + '" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen title="Driving directions from our Bellevue base to ' + esc(city) + ', WA"></iframe></div>\n'
                 "    </div>\n  </div>\n</section>\n")

    if C.get("faqs"):
        faqs = [(f["q"], f["a"]) for f in C["faqs"]]
    else:
        faqs = [(f["q"], f["a"]) for f in facts["faq_local"]] + [
            (f"Do you do kitchen and bathroom remodeling in {city}?", "Yes. Kitchens and bathrooms are among the projects we do most. See our kitchen remodeling and bathroom remodeling pages, or tell us what you have in mind."),
            (f"Do you have an office in {city}?", f"No. We are based in Bellevue and come to you. We serve {city} homeowners on site, from the free consultation through the final walkthrough."),
            (f"What affects the cost of a home remodel in {city}?", "Cost depends on the scope, the materials you choose, how much the layout changes and the condition of the home. Because every project is different, we review these factors with you in a free consultation rather than quoting before we understand the work."),
            (f"How do I get an estimate for my {city} project?", "Send a few details through the form on this page or call " + PHONE_TXT + " to book a free consultation. We look at the project with you, talk through your goals and agree on a clear scope before any work begins."),
        ]
    faq_md = []
    for q, a in faqs:
        faq_md += ["### " + q, "", a, ""]
    faq_section, faq_pairs = _k_faq(_k_blocks(faq_md), slug, f"{city} Home Remodeling Questions", len(faqs))
    parts.append(faq_section)

    form_sv = {"chip": "", "formHeading": "Free consultation", "formService": f"{city} city page"}
    form = lead_block("contact", slug + "-form-h", f"Ready to talk about your {city} remodel?", "Send a few details and we will take it from there. We reply within one business day.",
                      _form(form_sv, "city-page"), pimg(_UP, "project-45", "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    # Location-page schema policy: FAQPage + BreadcrumbList only (no business/Service entity).
    ld = [_crumb_ld([("Home", "/"), ("Areas We Serve", "/service-areas/"), (city, path)]),
          faq_ld([(q, [a]) for q, a in faq_pairs])]
    title = f"Home Remodeling in {city} - Puget Sound Builders"
    desc = f"Need Home Remodeling in {city}? Puget Sound Builders & Renovation delivers Kitchen and Bathroom remodeling & full-home renovations. Book Now!"
    page = (head(title, desc, path, _UP, photo_preload(_UP, hero_photo) + _KM_CSS + _ALGONA_CSS, ld)
            + '<body class="long-service-page-body">\n<!-- Location page (' + slug + '): finalized km design, verified local content, two distinct maps. -->\n'
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "areas", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    shown = _cr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_cr.S)
    if "WhatsApp" in shown or "wa.me" in shown: raise SystemExit(f"city page {city}: must not include WhatsApp")
    for bad in (chr(0x2014), chr(0x2013)):
        if bad in shown: raise SystemExit(f"city page {city}: a dash in the page")
    w(f"service-areas/{slug}/index.html", page)


_build_cities()

# ---- Areas We Serve hub: service-areas/index.html (preview /home-new/service-areas/), links to every city page ----
def _build_hub():
    cities = _j.load(io.open(_os.path.join(_P, "data", "city-list.json"), encoding="utf-8"))
    template = io.open(_os.path.join(_P, "content", "city-template.md"), encoding="utf-8").read()
    svc_lines = [l for l in template.splitlines() if l.startswith("- **[") and "/our-services/" in l]
    if len(svc_lines) != 8: raise SystemExit("hub: expected 8 service lines in content/city-template.md")
    title = "Areas We Serve | Puget Sound Builders & Renovation"
    desc = "Puget Sound Builders & Renovation serves Seattle, Bellevue and cities across the Puget Sound region. Find your city or call (425) 696-7586 to get started."
    lede = ("Puget Sound BNR is a general contractor based in Bellevue, Washington. We remodel, repair and build for homeowners in Seattle, Bellevue and communities "
            "across the Puget Sound region. Find your city below to see how we work in your area.")
    ctas = "[Book your free consultation]   [Call (425) 696-7586]"
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
    # Services carousel, same as the location pages ("What We Build and Renovate" + View all services).
    svc_sec = (services_section()
               .replace("What we build for Eastside homes.", "What We Build and Renovate")
               .replace("We build across Bellevue and the Eastside, from kitchens and bathrooms to ADU and DADU additions.",
                        "We build and renovate across the Puget Sound region, from kitchens and bathrooms to ADU and DADU additions.")
               .replace("Roofing for Eastside homes", "Roofing for homes across the region")
               .replace("</section>", '  <div class="wrap" style="text-align:center;margin-top:34px"><a class="btn btn--primary" href="' + URLS["services"] + '">View all services' + BTN_ARROW + "</a></div>\n</section>", 1))
    areas_map_sec = map_embed("areas-map", "sec--slab", "Find Us on the Map",
                              "We are based in Bellevue, Washington, and serve homeowners across Seattle, Bellevue and the Puget Sound region.")
    dont_sec = _k_section(heads["dont"], ids["dont"], "sec--stone", _k_blocks(["Tell us where you are and we will let you know if we can take on your project.", "", ctas]), "split")
    close_lines = ["If you are thinking about a project, the first step is simple. [Book your free consultation] or call (425) 696-7586, and we will come to your home, look at the project and tell you honestly what it needs.",
                   "", "### Related pages", "", "Explore our [services](/our-services/), see our [projects](/remodeling-projects/), or read about [who we are](/about/)."]
    close_sec = _k_section(heads["close"], ids["close"], "sec--stone", _k_blocks(close_lines), "split")
    form_sv = {"chip": "", "formHeading": "Free consultation", "formService": "Areas we serve page"}
    form = lead_block("contact", "areas-form-h", "Tell us about your project.", "Send a few details and we will take it from there. We reply within one business day.",
                      _form(form_sv, "areas-page"), pimg(_UP, closing_photo_id, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    # Testimonials section removed from the hub by request. Services-section head is centered via _HUB_CSS.
    parts = [hero, grid_sec, svc_sec, areas_map_sec, dont_sec, close_sec, form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n"]
    _HUB_CSS = "<style>#services .sec__head{display:block;text-align:center}#services .sec__head .h2{max-width:none;margin-left:auto;margin-right:auto}#services .sec__head .lede{margin-left:auto;margin-right:auto}</style>\n"
    ld = []  # Service-areas hub is an "other" page: no schema
    page = (head(title, desc, path, _UP, preload + _HUB_CSS, ld)
            + '<body class="long-service-page-body">\n<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "areas", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    shown = _cr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_cr.S)
    if "WhatsApp" in shown or "wa.me" in shown: raise SystemExit("hub: must not include WhatsApp")
    for bad in (chr(0x2014), chr(0x2013)):
        if bad in shown: raise SystemExit("hub: a dash in the page")
    if grid_items.count("<li>") != len(cities): raise SystemExit("hub: city grid mismatch")
    w("service-areas/index.html", page)

if not _os.environ.get("V4_CITY", "").strip(): _build_hub()
