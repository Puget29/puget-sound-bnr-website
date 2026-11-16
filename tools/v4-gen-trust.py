import re
# Trust strip: brands and profile logos. Exec'd by v4-gen-pages.py (shares esc, AS).
# Logo files are not supplied yet. A cell shows the brand name as plain text until assets/logos/<slug>.svg (or .png) exists, then the build picks the file up.
# Honesty: group A makes no partnership, certification or authorization claim. Group B links only when a real profile URL is set.

SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
# Supplier brands: Trex, GAF, James Hardie, Milgard, Floor and Decor, The Home Depot and Sherwin-Williams.
# Logos: files in site/assets/logos/ppc/, sizes from data/trust.json. Trex and Milgard have no logo file, so they are not shown (no text tiles).
_TJ = {i["slug"]: i for i in json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "trust.json"), encoding="utf-8"))["items"]}
_PPC_LOGOS = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "logos.generated.json"), encoding="utf-8"))
TRUST_BRANDS = [("Trex", "trex"), ("GAF", "gaf"), ("James Hardie", "james-hardie"), ("Milgard", "milgard"), ("Floor & Decor", "floor-and-decor"), ("The Home Depot", "home-depot"), ("Sherwin-Williams", "sherwin-williams")]
# profile links: Google and BBB are the verified links (data/trust.json), Yelp and Angi come from the links on the company's own site (LINKS)
TRUST_PROFILES = [("Google", "google", _TJ["google"]["url"]), ("BBB", "bbb", _TJ["bbb"]["url"]), ("Yelp", "yelp", LINKS["Yelp"]), ("Angi", "angi", LINKS["Angi"])]

ARROWUR = '<svg class="lgs__go" viewBox="0 0 14 14" fill="none" aria-hidden="true" focusable="false"><path d="M4 10L10 4M5 4h5v5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def _dims(path):
    # the logo's real size, so the browser reserves the right box (width and height attributes)
    try:
        if path.endswith(".svg"):
            head = io.open(path, encoding="utf-8").read(600)
            w = re.search(r'\swidth="([\d.]+)', head); h = re.search(r'\sheight="([\d.]+)', head)
            if w and h: return int(float(w.group(1))), int(float(h.group(1)))
            vb = re.search(r'viewBox="[\d.\- ]*?([\d.]+)[ ,]+([\d.]+)"', head)
            if vb: return int(float(vb.group(1))), int(float(vb.group(2)))
        else:
            from PIL import Image
            return Image.open(path).size
    except Exception:
        pass
    return 120, 32

def _logo(slug):
    for sub in ("ppc/", ""):
        for ext in ("svg", "webp", "png"):
            p = os.path.join(SITE_DIR, "assets", "logos", sub + slug + "." + ext)
            if os.path.exists(p):
                return f"{AS}assets/logos/{sub}{slug}.{ext}", _dims(p)
    return "", (0, 0)

def _cell(i, name, slug, href=None):
    src, (iw, ih) = _logo(slug)
    inner = (f'<img src="{src}" alt="{esc(name)}" width="{iw}" height="{ih}" loading="lazy" decoding="async">' if src
             else f'<span class="lgs__ph">{esc(name)}</span>')
    t = _TJ.get(slug, {})
    sc = float(t.get("scale", 1) or 1)
    cls = "lgs__c rv" + (" lgs__c--inv" if t.get("invert") else "")
    d = f' style="--d:{min(i * 0.07, 0.4):.2f}s;--ls:{sc}"'
    if not href:                                       # group A (brands): not a link
        return f'<li class="{cls}" data-slug="{slug}"{d}>{inner}</li>'
    label = f"Puget Sound Builders and Renovation on {name} (opens in a new tab)"
    return (f'<li class="{cls}" data-slug="{slug}"{d}><a class="lgs__a" href="{esc(href)}" target="_blank" rel="noopener noreferrer" aria-label="{esc(label)}">{inner}{ARROWUR}</a></li>')

def trust_section():
    a = "".join(_cell(i, n, s) for i, (n, s) in enumerate(TRUST_BRANDS))
    b = "".join(_cell(i + len(TRUST_BRANDS), n, s, h) for i, (n, s, h) in enumerate(TRUST_PROFILES))
    return f'''<!-- Intended final position: after Why homeowners hire BNR, before Reviews. Move when those sections exist. -->
<section class="sec sec--stone lgs" id="trust" aria-labelledby="lgs-h">
  <div class="wrap">
    <h2 class="lgs__vh" id="lgs-h">Brands we work with and where to find us</h2>
    <div class="lgs__grid">
      <div class="lgs__grp">
        <p class="lgs__l" id="lgs-a">Brands we work with</p>
        <ul class="lgs__ul" id="lgs-brands" aria-labelledby="lgs-a">{a}</ul>
      </div>
      <div class="lgs__grp">
        <p class="lgs__l" id="lgs-b">Find us on</p>
        <ul class="lgs__ul" id="lgs-profiles" aria-labelledby="lgs-b">{b}</ul>
      </div>
    </div>
    <p class="lgs__fine">All logos are trademarks of their respective owners.</p>
  </div>
</section>
'''


# ---------------------------------------------------------------------------------------------------------------
# Main site brand strip. Markup and logo data follow the PPC brand band.
def _blogo(slug, up):
    logo = _PPC_LOGOS.get(slug)
    if logo:
        return f"{shared(up)}{logo['file'].lstrip('/')}", (logo["w"], logo["h"])
    return "", (0, 0)

def brand_strip(up, small=False):
    items = []
    for name, slug in TRUST_BRANDS:
        src, (iw, ih) = _blogo(slug, up)
        if src:
            inner = f'<img src="{src}" alt="{esc(name)}" width="{iw}" height="{ih}" loading="eager" decoding="async">'
        else:
            inner = esc(name)
        items.append(f'<li><span class="tile">{inner}</span></li>')
    return f'''<section class="band band--brands" aria-label="Brands we work with">
  <div class="band__in">
    <div class="sl" data-sl role="group" aria-label="Brands we work with"><ul class="sl__set">{"".join(items)}</ul></div>
  </div>
</section>
'''
