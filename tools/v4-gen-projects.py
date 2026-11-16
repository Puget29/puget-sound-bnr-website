# Projects page (main site, v4 style). Executed from v4-gen-pages.py after the service pages, shares their helpers (_reviews, _form, _crumb_ld, _PJ, _dash_free).
# Real job photos only: real true, stock false in data/projects.json, a service we sell, no lowres flag. The 14 photos of data/last-jobs.json come first.
# Only caption is the service name, alt text is generic (service only), no place names, dates or claims. Real address: tools/v4-links.json "projects".
# Output: remodeling-projects/index.html. Filter and lightbox: site/v4/js/pj.js. No dashes in written copy, phone 4004, no WhatsApp.
_PJ_NAMES = [("kitchen", "Kitchen"), ("bathroom", "Bathroom"), ("adu", "ADU"), ("roofing", "Roofing"), ("deck", "Deck")]
_PJ_LABEL = dict(_PJ_NAMES)
_PJ_UP = "../"
_PJ_LAST = _j.load(io.open(_os.path.join(_P, "data", "last-jobs.json"), encoding="utf-8"))["ids"]

def _pj_ok(q):
    if q.get("real") is not True or q.get("stock") is not False or q.get("lowres") or q.get("service") not in _PJ_LABEL: return False
    ws = q.get("widths") or []
    return all(_os.path.exists(_os.path.join(SITE_DIR, "assets", "projects", f'{q["id"]}-{w}.webp')) for w in ws) and bool(ws)

def _pj_list():
    ok = [q for q in _PJ.values() if _pj_ok(q)]
    for pid in _PJ_LAST:
        if pid not in {q["id"] for q in ok}: raise SystemExit(f"projects page: last job photo {pid} is not a real photo")
    first = [_PJ[i] for i in _PJ_LAST]
    rest = {s: [q for q in ok if q["service"] == s and q["id"] not in _PJ_LAST] for s, _n in _PJ_NAMES}
    out = list(first)
    while any(rest.values()):                      # round robin so neighbours come from different services
        for s, _n in _PJ_NAMES:
            if rest[s]: out.append(rest[s].pop(0))
    return out

def _pj_tile(q, i):
    ws = sorted(w for w in q["widths"] if w <= 1440)
    big = max(ws); thumbs = [w for w in ws if w <= 960] or ws[:1]; mid = 960 if 960 in thumbs else max(thumbs)
    sm = ", ".join(f"{_src(q['id'], w).replace('../../', _PJ_UP)} {w}w" for w in thumbs)
    lb = ", ".join(f"{_src(q['id'], w).replace('../../', _PJ_UP)} {w}w" for w in ws if w >= 960)
    name = _PJ_LABEL[q["service"]]
    fp = q.get("objectPosition", "50% 50%")
    ld = 'fetchpriority="high" decoding="async"' if i < 3 else 'loading="lazy" decoding="async"'
    return (f'<li data-svc="{q["service"]}"><a class="pj__a" href="{_src(q["id"], big).replace("../../", _PJ_UP)}" data-srcset="{lb}" data-name="{name}">'
            f'<img src="{_src(q["id"], mid).replace("../../", _PJ_UP)}" srcset="{sm}" sizes="(min-width:900px) 31vw, 47vw" width="960" height="640" '
            f'alt="{name} remodeling project photo" {ld} style="object-position:{esc(fp)}"></a></li>')

def _projects_page():
    items = _pj_list()
    path = URLS["projects"]
    counts = {s: sum(1 for q in items if q["service"] == s) for s, _n in _PJ_NAMES}
    chips = '<button class="pj__chip" type="button" data-f="all" aria-pressed="true">All</button>'
    chips += "".join(f'<button class="pj__chip" type="button" data-f="{s}" aria-pressed="false">{n}</button>' for s, n in _PJ_NAMES)
    tiles = "".join(_pj_tile(q, i) for i, q in enumerate(items))
    hero = '<main id="main">\n' + photo_hero(_PJ_UP, "kitchen-06", "50% 50%", "pj-h", f'<nav class="crumbs" aria-label="Breadcrumb"><a href="{_PJ_UP}">Home</a><span aria-hidden="true">/</span><span aria-current="page">Projects</span></nav>',
        "Our remodeling projects.", "Photos from our own jobs: kitchens, bathrooms, ADUs, roofs and decks. Pick a service to filter, tap a photo to see it larger.",
        f'<a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>', "short") + brand_strip(_PJ_UP, True)
    grid = f'''<section class="sec sec--slab pj" id="pj" aria-labelledby="pj-g-h">
  <div class="wrap">
    <h2 class="sr" id="pj-g-h">Project photos</h2>
    <div class="pj__bar" role="group" aria-label="Filter photos by service" hidden>{chips}</div>
    <p class="pj__status sr" role="status" aria-live="polite"></p>
    <ul class="pj__grid" data-pj>{tiles}</ul>
    <div class="pj__empty" hidden><p>No photos in this category yet.</p><button class="pj__chip" type="button" data-f="all">Show all projects</button></div>
  </div>
</section>
'''
    sv = {"chip": "", "formHeading": "Free consultation", "formService": "Projects page"}
    cta = lead_block("contact", "pj-c-h", "Have a project like these in mind?", "Send a few details and we will take it from there. We reply within one business day.", _form(sv, "projects-page"), pimg(_PJ_UP, "project-45", "(min-width:901px) 40vw, 90vw", "50% 60%", False, ""))
    ld = [org_ld(), _crumb_ld([("Home", "/"), ("Projects", path)])]
    html_ = (head("Remodeling projects | Puget Sound Builders & Renovation", "Photos of real kitchen, bathroom, ADU, roofing and deck jobs by Puget Sound Builders & Renovation in Bellevue, WA.", path, _PJ_UP, photo_preload(_PJ_UP, "kitchen-06"), ld)
             + "<body>\n<!-- Projects page. -->\n" + '<a class="skip" href="#main">Skip to content</a>\n'
             + banner() + header(_PJ_UP, "work", False) + hero + grid + wrf_reviews_section(False, "What clients say.", "Real Google reviews, in their own words.", find_us(_PJ_UP)) + cta + "</main>\n"
             + footer(_PJ_UP) + mbar(_PJ_UP) + scripts(_PJ_UP, False) + "</body>\n</html>\n")
    return html_.replace('href="../"', f'href="{_PJ_UP}"'), len(items)

_pj_out, _pj_n = _projects_page()
if _re.search(r"whatsapp|wa\.me", _pj_out, _re.I): raise SystemExit("projects page: WhatsApp found")
w("remodeling-projects/index.html", _pj_out)
print("projects page photos:", _pj_n)
