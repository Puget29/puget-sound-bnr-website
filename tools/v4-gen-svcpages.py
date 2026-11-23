# Services overview and one page per service (main site, v4 style). Executed from v4-gen-pages.py, shares its helpers.
# Data: service records (data/service-pages.json) and project photos (data/projects.json) are read only. Extra page copy lives in tools/v4-extra-services.json.
# Pages: our-services/index.html and our-services/<service slug>/index.html. Real addresses are in tools/v4-links.json (servicePages).
# Design: same tokens as the other v4 pages. Hero split, slab intro, dark gallery, stone process, slab reasons, dark reviews, stone FAQ, slab form.
# No dashes in written copy. Real job photos only in work galleries. Phone 4004, no WhatsApp, no place names.
import json as _j, re as _re, os as _os

_P = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
def _rj(n): return _j.load(io.open(_os.path.join(_P, "data", n), encoding="utf-8"))
_SP = _rj("service-pages.json")["pages"]
_EXTRA = _j.load(io.open(_os.path.join(_P, "tools", "v4-extra-services.json"), encoding="utf-8"))["pages"]
_ALL_SP = _SP + _EXTRA
_PJ = {q["id"]: q for q in _rj("projects.json")}
_RV = [r for r in _rj("reviews.json") if r.get("verified") and r.get("featured")]
_CH = _rj("services.json")["chips"]
_CARDS = {c["slug"]: c for c in _rj("service-photos.json")["cards"]}
_SPU = URLS["servicePages"]
_UP = "../../"

def _rel_of(url):
    # The folder a page is written to is its real public URL, not its slug. This lets the Seattle
    # service records keep their Seattle URLs while separate records own the /our-services/ pages.
    u = url.strip("/")
    return (u + "/index.html") if u else "index.html"
_GOOGLE = _TJ["google"]["url"] if "_TJ" in globals() else ""
_ASSET_PHOTOS = {
    "painting-card": {"widths": [640, 960], "w": 960, "h": 1200, "alt": "Painter rolling a fresh coat of paint on an interior wall", "objectPosition": "50% 42%"}
}

def _dash_free(s): return s.replace(chr(0x2014), ",").replace(chr(0x2013), ",")
def _t(s): return esc(_dash_free(s)).replace("{{PHONE}}", PHONE_TXT)

# Shared Google Business Profile map embed (same place as the location-page areas section). Defined here
# so the services hub (_overview, below), the service-areas hub (city-gen _build_hub) and the contact page
# (v4-gen-approved-pages) can all reuse it. Self-contained inline styles so it renders on non-.km pages.
GBP_MAP_SRC = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d10757.322140992934!2d-122.19868572399378"
               "!3d47.619705800000006!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x54905d4b2eab6f75"
               "%3A0x2ad4580dc612257!2sPuget%20Sound%20Builders%20%26%20Renovation%20-%20Kitchen%20%26%20"
               "Bathroom!5e0!3m2!1sen!2s!4v1795337633395!5m2!1sen!2s")

def map_embed(sec_id, surface, heading, lede, extra=""):
    return ('<section class="sec ' + surface + '" id="' + sec_id + '" aria-labelledby="' + sec_id + '-h">\n'
            '  <div class="wrap">\n'
            '    <div class="sec__head rv" style="display:block;text-align:center"><h2 class="h2" id="' + sec_id + '-h" style="max-width:none;margin-left:auto;margin-right:auto">' + esc(heading) + '</h2><p class="lede" style="margin-left:auto;margin-right:auto">' + esc(lede) + '</p></div>\n'
            '    <div style="border-radius:16px;overflow:hidden;max-width:960px;margin:22px auto 0;border:1px solid rgba(0,0,0,.12)">'
            '<iframe src="' + GBP_MAP_SRC + '" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen '
            'title="Puget Sound Builders and Renovation on Google Maps, Bellevue" style="width:100%;height:420px;border:0;display:block"></iframe></div>\n'
            + extra +
            '  </div>\n</section>\n')

def _abs_photo(pid):
    """Absolute URL to a representative width of a photo id, for a schema Service image."""
    q = _photo(pid); ws = [w for w in (q.get("widths") or (640, 960, 1440)) if w <= 1440]
    w = 960 if 960 in ws else max(ws)
    stem = pid.split(":", 1)[1] if pid.startswith("asset:") else pid
    return SITE + "/assets/projects/" + stem + "-" + str(w) + ".webp"

def _src(pid, w): return f"{_UP}assets/projects/{pid}-{w}.webp"

def _photo(pid):
    if pid.startswith("asset:"): return _ASSET_PHOTOS[pid.split(":", 1)[1]]
    return _PJ[pid]

def _photo_src(pid, w):
    if pid.startswith("asset:"): return f"{_UP}assets/projects/{pid.split(':', 1)[1]}-{w}.webp"
    return _src(pid, w)

def _img(pid, sizes, cls="", eager=False, focus=None):
    q = _photo(pid)
    ws = [w for w in (q.get("widths") or (640, 960, 1440)) if w <= 1440]
    mid = 960 if 960 in ws else max(ws)
    ss = ", ".join(f"{_photo_src(pid, w)} {w}w" for w in ws)
    fp = focus or q.get("objectPosition", "50% 50%")
    ld = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{_photo_src(pid, mid)}" srcset="{ss}" sizes="{sizes}" width="{q.get("w", 1440)}" height="{q.get("h", 960)}" '
            f'alt="{esc(q["alt"])}" {ld} style="object-position:{esc(fp)}">')

def _check_real(pid, svc=None):
    if pid.startswith("asset:"):
        key = pid.split(":", 1)[1]
        if key not in _ASSET_PHOTOS: raise SystemExit(f"service pages: missing site image {pid}")
        for width in _ASSET_PHOTOS[key]["widths"]:
            path = _os.path.join(_P, "site", "assets", "projects", f"{key}-{width}.webp")
            if not _os.path.isfile(path): raise SystemExit(f"service pages: image file missing: {path}")
        return
    q = _PJ.get(pid)
    if not q: raise SystemExit(f"service pages: photo {pid} is not in data/projects.json")
    if q.get("real") is False or q.get("stock") or q.get("job", "").startswith("render"):
        raise SystemExit(f"service pages: photo {pid} is not a real job photo")
    if svc and q.get("service") != svc:
        raise SystemExit(f"service pages: photo {pid} belongs to {q.get('service')}, not {svc}")

def _sv_bullet_item(content):
    return f'<li><span class="sv-list__dot" aria-hidden="true"></span><span>{content}</span></li>'

def _crumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(items)]}

def _stars(n=5):
    return '<span class="sv-stars" role="img" aria-label="5 out of 5 stars">' + "".join('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.8l2.4 5.2 5.6.6-4.2 3.8 1.2 5.5L10 14.1 5 16.9l1.2-5.5L2 7.6l5.6-.6z"/></svg>' for _ in range(n)) + "</span>"

def _reviews():
    cards = ""
    for i, r in enumerate(_RV):
        paras = "".join(f"<p>{esc(p)}</p>" for p in r["text"].split("\n\n") if p.strip())
        cards += (f'<article class="sv-rev rv" style="--d:{i * .08:.2f}s"><div class="sv-rev__top"><span class="sv-rev__av" aria-hidden="true">{esc(r["name"][:1])}</span>'
                  f'<div><strong>{esc(r["name"])}</strong>{_stars()}</div></div>'
                  f'<div class="sv-rev__t" data-clamp>{paras}</div>'
                  f'<button class="sv-rev__more" type="button" aria-expanded="false" hidden>Read more</button></article>')
    link = f'<a class="link-q" href="{esc(_GOOGLE)}" target="_blank" rel="noopener noreferrer">Read all our reviews on Google<span class="sr"> (opens in a new tab)</span></a>' if _GOOGLE else ""
    return f'''<section class="sec sec--dark" id="sv-reviews" aria-labelledby="sv-rv-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="sv-rv-h">What clients say.</h2><div><p class="lede">Real Google reviews, word for word.</p>{('<p style="margin-top:14px">' + link + '</p>') if link else ''}</div></div>
    <div class="sv-revs">{cards}</div>
  </div>
</section>
'''

def _form(sv, source="service-page"):
    chips = ""
    want = sv["chip"]
    for c in _CH:
        chk = " checked" if c["value"] == want else ""
        chips += f'<label><input type="radio" name="service" value="{esc(c["value"])}"{chk}><span>{esc(c["label"])}</span></label>'
    return f'''{form_open("form form--card", source, sv["formHeading"], "form")}
        {netlify_fields(source, sv["formService"])}
        <h3 class="h3" style="margin-bottom:4px">{esc(sv["formHeading"])}</h3>
        <div class="form__two">
          <div class="fld"><label for="sf-name">Name</label><input id="sf-name" name="name" type="text" autocomplete="name" data-req aria-describedby="sf-name-err"><p class="err" id="sf-name-err" role="alert"></p></div>
          <div class="fld"><label for="sf-phone">Phone</label><input id="sf-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" data-req data-kind="phone" aria-describedby="sf-phone-err"><p class="err" id="sf-phone-err" role="alert"></p></div>
        </div>
        <div class="form__two">
          <div class="fld"><label for="sf-zip">ZIP code</label><input id="sf-zip" name="zip" type="text" autocomplete="postal-code" inputmode="numeric" data-req data-kind="zip" aria-describedby="sf-zip-err"><p class="err" id="sf-zip-err" role="alert"></p></div>
          <div class="fld"><label for="sf-email">Email</label><input id="sf-email" name="email" type="email" autocomplete="email" data-req data-kind="email" aria-describedby="sf-email-err"><p class="err" id="sf-email-err" role="alert"></p></div>
        </div>
        <div class="fld"><fieldset><legend>What do you need?</legend><div class="opts">{chips}</div></fieldset></div>
        {honeypot()}
        <button class="btn btn--primary" type="submit">Book your free consultation{BTN_ARROW}</button>
        <p class="form__fine">We use your details only to reply about your project.</p>
        <p class="form__fail err" tabindex="-1" hidden role="alert">Something went wrong. Please call {PHONE_TXT}.</p>
        <div class="form__ok" role="status"><strong>Thank you.</strong><span class="form__ok-text"></span></div>
      </form>'''

def _page(sv):
    slug, name = sv["slug"], sv["h1Service"]
    path = _SPU[slug]
    a = sv["about"]
    _check_real(sv["heroPhoto"], sv["photoService"])
    for g in sv["gallery"]: _check_real(g, sv["photoService"])
    offer = "".join(_sv_bullet_item(_t(x)) for x in a.get("offer", []))
    hero = f'''<main id="main">
<section class="page-hero sv-hero" aria-labelledby="sv-h">
  <div class="wrap page-hero__grid">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb"><a href="{_SPU['overview']}">Services</a><span aria-hidden="true">/</span><span aria-current="page">{esc(name)}</span></nav>
      <h1 id="sv-h">{esc(sv["h1"])}</h1>
      <p class="lede" style="margin-bottom:30px">{_t(sv["heroParagraph"])}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(sv["heroPhoto"], "(min-width:901px) 46vw, 92vw", "", True, sv.get("heroFocal"))}</figure>
  </div>
</section>
'''
    intro = f'''<section class="sec sec--slab" aria-labelledby="sv-a-h">
  <div class="wrap sv-split">
    <div class="rv"><h2 class="h2" id="sv-a-h">What we offer.</h2><p class="lede" style="margin-top:24px">{_t(a["intro"])}</p></div>
    <div class="rv" style="--d:.08s"><h3 class="sv-k">Service options</h3><ul class="sv-offer">{offer}</ul></div>
  </div>
  <div class="wrap sv-two">
    <div class="sec__head rv sv-two__head"><h2 class="h2" id="sv-i-h">What is included?</h2></div>
    <div class="rv"><h3 class="sv-k">Materials and choices</h3><p class="prose-p">{_t(a.get("options", ""))}</p></div>
    <div class="rv" style="--d:.08s"><h3 class="sv-k">Scope and planning</h3><p class="prose-p">{_t(a.get("expect", ""))}</p></div>
  </div>
</section>
''' if a.get("offer") else ""
    tiles = ""
    for g in sv["gallery"]:
        q = _photo(g); ws = sorted(q["widths"]); big = max(ws); mid = 960 if 960 in ws else big
        lb = ", ".join(f"{_photo_src(g, w)} {w}w" for w in ws if w >= mid)
        fp = q.get("objectPosition", "50% 50%")
        sm = ", ".join(f"{_photo_src(g, w)} {w}w" for w in ws if w <= 1440)
        tiles += (f'<li><a class="gal__a" href="{_photo_src(g, big)}" data-srcset="{lb}"><img src="{_photo_src(g, mid)}" srcset="{sm}" sizes="(min-width:900px) 31vw, 46vw" '
                  f'width="{q.get("w", 960)}" height="{q.get("h", 640)}" alt="{esc(q["alt"])}" loading="lazy" decoding="async" style="object-position:{esc(fp)}"></a></li>')
    cap = " gal--cap" if len(sv["gallery"]) > 8 else ""
    gallery = f'''<section class="sec sec--dark" id="work" aria-labelledby="sv-w-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="sv-w-h">{esc(sv.get("galleryHeading", "Our " + sv["workName"] + " work."))}</h2><p class="lede">{esc(sv.get("galleryIntro", "Photos of our own jobs. Tap a photo to see it larger."))}</p></div>
    <div class="gal{cap} rv" data-gal><ul class="gal__list">{tiles}</ul><button class="gal__more" type="button" aria-expanded="false" hidden>Show more</button></div>
  </div>
</section>
'''
    steps = "".join(f'<li class="sv-step rv" style="--d:{i * .05:.2f}s"><span class="sv-step__n" aria-hidden="true">{i + 1:02d}</span><div><h3 class="h3">{esc(s["title"])}</h3><p>{_t(s["text"])}</p></div></li>' for i, s in enumerate(sv["process"]))
    process = f'''<section class="sec sec--stone" aria-labelledby="sv-p-h">
  <div class="wrap sv-split sv-split--steps">
    <div class="rv"><h2 class="h2" id="sv-p-h">How our process works.</h2><p class="lede" style="margin-top:24px">From the first free consultation to the final walkthrough.</p></div>
    <ol class="sv-steps">{steps}</ol>
  </div>
</section>
'''
    why = "".join(f'<li class="sv-why__i rv" style="--d:{i * .06:.2f}s"><h3 class="h3">{esc(w_["title"])}</h3><p>{_t(w_["text"])}</p></li>' for i, w_ in enumerate(sv["why"]))
    whys = f'''<section class="sec sec--slab" aria-labelledby="sv-y-h">
  <div class="wrap"><div class="sec__head rv"><h2 class="h2" id="sv-y-h">Why choose Puget Sound BNR?</h2></div><ul class="sv-why">{why}</ul></div>
</section>
'''
    faq = "".join(f'<details class="sv-faq__r rv" name="svfaq"{" open" if i == 0 else ""}><summary><span>{esc(q)}</span><span class="plus" aria-hidden="true"></span></summary><div class="sv-faq__a"><p>{_t(an)}</p></div></details>' for i, (q, an) in enumerate(sv["faq"]))
    faqs = f'''<section class="sec sec--stone" id="sv-faq-s" aria-labelledby="sv-f-h">
  <div class="wrap sv-split"><div class="rv"><h2 class="h2" id="sv-f-h">Questions, answered.</h2></div><div class="sv-faq">{faq}</div></div>
</section>
'''
    last_photo = sv["gallery"][-1]
    closing_photo = (_img(last_photo, "(min-width:901px) 40vw, 90vw") if last_photo.startswith("asset:")
                     else pimg(_UP, last_photo, "(min-width:901px) 40vw, 90vw", None, False, ""))
    cta = lead_block("contact", "sv-c-h", esc(sv["closingHeading"]), "Send a few details and we will take it from there. We reply within one business day.", _form(sv), closing_photo)
    # Service-page schema policy: Service + FAQPage + BreadcrumbList (no business entity; Service.provider
    # references the homepage LocalBusiness by @id rather than duplicating the entity).
    ld = [_crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), (name, path)]),
          {"@context": "https://schema.org", "@type": "Service", "@id": SITE + path + "#service", "name": name,
           "serviceType": name, "description": sv["description"], "url": SITE + path, "image": _abs_photo(sv["heroPhoto"]),
           "provider": {"@id": SITE + "/#localbusiness"}, "areaServed": ["Bellevue, WA", "The Eastside", "Greater Seattle area"]},
          faq_ld([(q, [_dash_free(an).replace("{{PHONE}}", PHONE_TXT)]) for q, an in sv["faq"]])]
    html_ = (head(sv["title"].replace(" | ", " | "), sv["description"], path, _UP, "", ld)
             + f"<body>\n<!-- Service page: {slug}. -->\n" + '<a class="skip" href="#main">Skip to content</a>\n'
             + banner() + header(_UP, "services", False) + hero + brand_strip(_UP, True) + intro + process + whys + gallery + _reviews() + faqs + cta + "</main>\n"
             + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")
    return html_.replace('href="../"', f'href="{_UP}"')

# ------------------------------------------------------------------ overview ----
def _overview():
    rows = ""
    _by = {sv["slug"]: sv for sv in _ALL_SP}
    _ordered = [_by[key] for _lbl, key in _SERVICE_ORDER if key in _by]
    for i, sv in enumerate(_ordered):
        pid = sv["heroPhoto"]; _check_real(pid, sv["photoService"])
        offer = sv["about"].get("offer", [])[:3]
        li = "".join(_sv_bullet_item(_t(x)) for x in offer)
        flip = " sv-row--flip" if i % 2 else ""
        rows += f'''<article class="sv-row{flip}">
  <a class="sv-row__ph rv" href="{_SPU[sv["slug"]]}" tabindex="-1" aria-hidden="true">{_img(pid, "(min-width:901px) 52vw, 92vw", "", i == 0, sv.get("heroFocal"))}</a>
  <div class="sv-row__t rv" style="--d:.08s">
    <span class="sv-row__n" aria-hidden="true">{i + 1:02d}</span>
    <h2 class="h2"><a href="{_SPU[sv["slug"]]}">{esc(sv["h1Service"])}</a></h2>
    <p class="lede">{_t(sv["about"]["intro"].split(". ")[0].rstrip(".") + ".")}</p>
    <ul class="sv-offer">{li}</ul>
    <a class="btn btn--primary" href="{_SPU[sv["slug"]]}">See {esc(sv["h1Service"].lower())}{BTN_ARROW}</a>
  </div>
</article>
'''
    pills = "".join(f'<li><a href="/contact-us/?service={esc(k)}#form">{esc(n)}</a></li>' for k, n in (
        ("full-house-remodeling", "Full house remodeling"),
        ("electrical-and-plumbing", "Electrical and plumbing"), ("hvac-and-insulation", "HVAC and insulation"), ("windows-installation", "Windows"),
        ("room-additions", "Room additions"), ("garage-remodel", "Garage remodel"), ("driveways-pavers-and-concrete", "Driveways and concrete"),
        ("landscaping-and-hardscaping", "Landscaping"), ("mold-remediation", "Mold remediation")))
    ov_hero = photo_hero(_UP, "project-43", "50% 55%", "sv-o-h", f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{_UP}">Home</a><span aria-hidden="true">/</span><span aria-current="page">Services</span></nav>', "What we build and renovate.", "One general contractor for kitchens, bathrooms, ADUs, decks, roofs and more. Choose a service to see how we work and what we have built.", f'<a class="btn btn--primary" href="{CONTACT}" data-book>Book your free consultation{BTN_ARROW}</a>', "short")
    _ov_lead = lead_block("contact", "sv-o-c", "Tell us what you want to change.", "Send a few details and we will take it from there. We reply within one business day.", _form({"chip": "", "formHeading": "Free consultation", "formService": "Services page"}, "services-page"), pimg(_UP, "project-45", "(min-width:901px) 40vw, 90vw", "50% 60%", False, ""))
    _areas_btn = '<div style="text-align:center;margin-top:24px"><a class="btn btn--primary" href="/service-areas/">See all service areas' + BTN_ARROW + '</a></div>\n'
    areas_sec = map_embed("sv-o-areas", "sec--slab", "Areas We Serve",
                          "Based in Bellevue, we serve Seattle, Bellevue and homeowners across the Puget Sound region. Find your city to see how we work in your area.", _areas_btn)
    body = f'''<main id="main">
{ov_hero}{brand_strip(_UP, True)}
<section class="sec sec--slab sv-rows" aria-label="Our services"><div class="wrap">{rows}</div></section>
<section class="sec sec--stone" aria-labelledby="sv-m-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="sv-m-h">More we do.</h2><p class="lede">Not on the list? Tell us what you have in mind.</p></div>
    <ul class="sv-pills rv">{pills}</ul>
  </div>
</section>
{areas_sec}{_ov_lead}</main>
'''
    ld = []  # Services overview (hub) is an "other" page: no schema
    return (head("Our Home Remodeling Services | Puget Sound Builders", "Explore kitchen, bathroom, roofing, flooring, siding, painting, ADU and deck services from Puget Sound Builders & Renovation in Bellevue. Book a consult.",
             _SPU["overview"], _UP, photo_preload(_UP, "project-43"), ld)
            + "<body>\n<!-- Services overview. Links go to the service pages (tools/v4-links.json servicePages). -->\n" + '<a class="skip" href="#main">Skip to content</a>\n'
            + banner() + header(_UP, "services", False) + body + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n").replace('href="../"', f'href="{_UP}"').replace('href="../contact/', f'href="{CONTACT}')

w(_rel_of(_SPU["overview"]), _overview())
for _sv in _ALL_SP:
    # Pages rendered by the long-form generators in v4-gen-kitchen.py are skipped by the short template:
    # kitchen-remodeling (the Seattle long page) plus every main /our-services/ page (the full reusable
    # long-form design rolled out sitewide).
    if _sv["slug"] in ("kitchen-remodeling", "kitchen-main", "bathroom-main", "roofing-main", "floor-main",
                       "deck-building", "adu-garage-conversion", "painting", "basement-remodeling",
                       "attic-remodeling", "home-addition"):
        continue
    _out = _page(_sv)
    if _re.search(r"whatsapp|wa\.me", _out, _re.I): raise SystemExit("service pages: WhatsApp found")
    w(_rel_of(_SPU[_sv["slug"]]), _out)

# Kitchen has its own long form page, still generated from the shared page system.
exec(open(os.path.join(os.path.dirname(__file__), "v4-gen-kitchen.py"), encoding="utf-8").read(), globals())
