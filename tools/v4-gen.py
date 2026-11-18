# Builds site/v4/index.html, about/index.html, contact/index.html from shared partials.
# Dev-time helper only (not part of the site). The output is plain static HTML.
import html, json, io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "v4")
# V4_ROOT=1 builds the variant that is published at the site root (/, /about/, /contact/). It goes to site/v4/_root/ and uses the root layout of the repo
# (css/, js/, assets/ at the top, hero-v3.js). Without it the pages are built for /v4/ as before.
ROOT = os.environ.get("V4_ROOT") == "1"
if ROOT: OUT = os.path.join(OUT, "_root")
def shared(up): return up if ROOT else up + "../"      # where the shared css, js, vendor and assets live, seen from a page that is `up` deep
OG = "/assets/og.jpg" if ROOT else "/v4/assets/og.jpg"
SITE = "https://www.pugetsoundbnr.com"
URLS = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v4-links.json"), encoding="utf-8"))
CONTACT = URLS["contact"]
_CITY_LIST = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "city-list.json"), encoding="utf-8"))
_SERVICE_ORDER = [
    ("Kitchen remodeling", "kitchen-remodeling"),
    ("Bathroom remodeling", "bathroom-remodeling"),
    ("Roofing", "roofing"),
    ("Deck building", "deck-building"),
    ("ADU and garage conversion", "adu-garage-conversion"),
    ("Siding", "siding"),
    ("Flooring", "flooring"),
    ("Painting", "painting"),
]

PHONE_TXT, PHONE_TEL = "(425) 696-4004", "+14256964004"
WA = "https://wa.me/14252295663"
EMAIL = "Office@pugetsoundbnr.com"
ADDR = "11170 NE 10th St, Bellevue, WA 98004"
OFFER = "10% Off for New Clients"
LINKS = {
    "Instagram": "https://www.instagram.com/pugetsoundbnr/",
    "Facebook": "https://www.facebook.com/PugetSoundbnr",
    "Yelp": "https://m.yelp.com/biz/puget-sound-builders-and-renovation-bellevue-3",
    "Angi": "https://www.angi.com/companylist/us/wa/bellevue/puget-sound-builders-and-renovations-reviews-10974240.htm",
}
CITIES = [  # (name, lat, lon), the 27 cities from the client
    ("Bellevue", 47.61, -122.20), ("Kirkland", 47.68, -122.21), ("Redmond", 47.67, -122.12), ("Bothell", 47.76, -122.21),
    ("Seattle", 47.61, -122.33), ("Mercer Island", 47.57, -122.22), ("Newcastle", 47.53, -122.16), ("Renton", 47.48, -122.22),
    ("Kenmore", 47.76, -122.24), ("Everett", 47.98, -122.20), ("Lynnwood", 47.82, -122.31), ("Duvall", 47.74, -121.99),
    ("Issaquah", 47.53, -122.03), ("Sammamish", 47.61, -122.04), ("North Bend", 47.50, -121.78), ("Snohomish", 47.91, -122.10),
    ("Snoqualmie", 47.53, -121.83), ("SeaTac", 47.44, -122.30), ("Tukwila", 47.47, -122.26), ("Kent", 47.38, -122.23),
    ("Auburn", 47.31, -122.23), ("Bonney Lake", 47.18, -122.18), ("Federal Way", 47.32, -122.31), ("Tacoma", 47.25, -122.44),
    ("Marysville", 48.05, -122.18), ("Covington", 47.36, -122.10), ("Maple Valley", 47.39, -122.04),
]
assert len(CITIES) == 27

def esc(s): return html.escape(s, quote=True)

# ---------------------------------------------------------------- line art (viewBox 0 0 240 160) ----
def _lines_h(ys, x1, x2): return "".join(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>' for y in ys)
def _flooring():
    s = '<rect x="16" y="16" width="208" height="128"/>' + _lines_h([48, 80, 112], 16, 224)
    ys = [16, 48, 80, 112, 144]
    for i in range(4):
        xs = (56, 136, 216) if i % 2 else (96, 176)
        for xx in xs: s += f'<line x1="{xx}" y1="{ys[i]}" x2="{xx}" y2="{ys[i+1]}"/>'
    return s
ART = {
    "kitchen": '<rect x="16" y="16" width="208" height="128" rx="2"/><rect x="16" y="16" width="208" height="24"/><rect x="200" y="40" width="24" height="70"/><rect x="48" y="21" width="34" height="14" rx="3"/><circle cx="65" cy="28" r="2"/><circle cx="140" cy="28" r="6"/><circle cx="160" cy="28" r="6"/><rect x="72" y="76" width="96" height="30" rx="2"/><circle cx="88" cy="122" r="6"/><circle cx="120" cy="122" r="6"/><circle cx="152" cy="122" r="6"/><path d="M16 144 H56"/><path d="M56 144 A40 40 0 0 0 16 104"/>',
    "bathroom": '<rect x="16" y="16" width="208" height="128" rx="2"/><rect x="28" y="28" width="120" height="44" rx="14"/><rect x="38" y="37" width="100" height="26" rx="10"/><rect x="164" y="24" width="48" height="30"/><ellipse cx="188" cy="39" rx="14" ry="8"/><rect x="184" y="104" width="26" height="14" rx="3"/><ellipse cx="197" cy="128" rx="13" ry="11"/><rect x="28" y="92" width="60" height="44"/><circle cx="58" cy="114" r="4"/><path d="M110 144 H150"/><path d="M150 144 A40 40 0 0 0 110 104"/>',
    "adu": '<rect x="12" y="12" width="216" height="136"/><rect x="28" y="28" width="108" height="64"/><line x1="82" y1="28" x2="82" y2="92"/><rect x="150" y="84" width="62" height="44"/><line x1="150" y1="106" x2="212" y2="106"/><path d="M82 92 V110 H150"/><circle cx="44" cy="120" r="9"/><circle cx="70" cy="130" r="6"/>',
    "deck": '<rect x="28" y="30" width="184" height="92"/><line x1="28" y1="20" x2="212" y2="20"/>' + _lines_h([44, 58, 72, 86, 100, 114], 28, 212) + '<rect x="96" y="122" width="48" height="8"/><rect x="104" y="130" width="32" height="8"/><rect x="112" y="138" width="16" height="8"/>',
    "roofing": '<path d="M16 96 L120 26 L224 96"/><path d="M16 96 H224"/>' + _lines_h([112, 128], 28, 212) + '<path d="M60 96 V70 H80 V84"/><path d="M150 96 L170 82 L190 96"/>',
    "siding": '<path d="M28 140 V74 L120 22 L212 74 V140 Z"/>' + _lines_h([88, 100, 112, 124], 28, 212) + '<rect x="104" y="104" width="32" height="36"/><rect x="52" y="92" width="30" height="26"/><rect x="158" y="92" width="30" height="26"/>',
    "flooring": _flooring(),
    "painting": '<rect x="24" y="20" width="192" height="120" rx="2"/><rect x="48" y="40" width="120" height="28" rx="6"/><path d="M168 54 H190 V88 H120 V104"/><rect x="112" y="104" width="16" height="30" rx="4"/><path d="M44 120 H88"/>',
    "lot": '<rect x="12" y="12" width="216" height="130"/><rect x="28" y="28" width="108" height="62"/><line x1="82" y1="28" x2="82" y2="90"/><rect x="150" y="78" width="62" height="44"/><line x1="150" y1="100" x2="212" y2="100"/><path d="M82 90 V108 H150"/><circle cx="44" cy="118" r="9"/><circle cx="70" cy="128" r="6"/><line x1="12" y1="152" x2="228" y2="152"/><line x1="12" y1="147" x2="12" y2="157"/><line x1="228" y1="147" x2="228" y2="157"/><line x1="150" y1="134" x2="212" y2="134"/><line x1="150" y1="129" x2="150" y2="139"/><line x1="212" y1="129" x2="212" y2="139"/>',
    "call": '<rect x="90" y="18" width="60" height="124" rx="12"/><line x1="108" y1="32" x2="132" y2="32"/><circle cx="120" cy="126" r="4"/><path d="M168 54 q22 26 0 52"/><path d="M182 40 q34 40 0 80"/>',
    "visit": '<rect x="48" y="52" width="144" height="56" rx="8"/>' + "".join(f'<line x1="{x}" y1="52" x2="{x}" y2="{66 if i % 2 else 76}"/>' for i, x in enumerate(range(64, 192, 16))) + '<path d="M192 80 H214 V128 H174"/>',
    "quote": '<rect x="76" y="14" width="88" height="132" rx="4"/><line x1="92" y1="40" x2="148" y2="40"/><line x1="92" y1="60" x2="148" y2="60"/><line x1="92" y1="80" x2="132" y2="80"/><path d="M96 114 l12 12 l26 -28"/>',
}
def art(name, cls=""): return f'<svg class="art {cls}" viewBox="0 0 240 160" aria-hidden="true" focusable="false">{ART[name]}</svg>'

ARROW = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 10h13M11 5l5 5-5 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BTN_ARROW = '<svg class="btn__arrow" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 74 74" height="34" width="34" aria-hidden="true"><circle stroke-width="3" stroke="currentColor" r="35.5" cy="37" cx="37"/><path fill="currentColor" d="M25 35.5C24.1716 35.5 23.5 36.1716 23.5 37C23.5 37.8284 24.1716 38.5 25 38.5V35.5ZM49.0607 38.0607C49.6464 37.4749 49.6464 36.5251 49.0607 35.9393L39.5147 26.3934C38.9289 25.8076 37.9792 25.8076 37.3934 26.3934C36.8076 26.9792 36.8076 27.9289 37.3934 28.5147L45.8787 37L37.3934 45.4853C36.8076 46.0711 36.8076 47.0208 37.3934 47.6066C37.9792 48.1924 38.9289 48.1924 39.5147 47.6066L49.0607 38.0607ZM25 38.5L48 38.5V35.5L25 35.5V38.5Z"/></svg>'

DEV_SCRIPT = r'''<script>/* js class gates the reveal states. ?dark turns the stone sections dark. */(function(){var d=document.documentElement;d.classList.add("js");try{if(/[?&]dark(&|$)/.test(location.search))d.classList.add("v4-dark")}catch(e){}})();(function(){var w=window;try{history.scrollRestoration="manual"}catch(e){}function top(){if(!location.hash){try{w.scrollTo({top:0,left:0,behavior:"instant"})}catch(e){w.scrollTo(0,0)}}}w.addEventListener("DOMContentLoaded",top);w.addEventListener("pageshow",function(e){if(e.persisted)top()});w.addEventListener("load",function(){if(!location.hash)return;var el=null;try{el=document.getElementById(decodeURIComponent(location.hash.slice(1)))}catch(e){}if(el&&document.fonts&&document.fonts.ready)document.fonts.ready.then(function(){try{el.scrollIntoView({block:"start",behavior:"instant"})}catch(e){el.scrollIntoView()}})})})();</script>'''

# ---------------------------------------------------------------- partials ----
# Indexable by default. PREVIEW=1 (set when staging a preview) writes noindex instead.
PREVIEW = os.environ.get("PREVIEW") == "1"
ROBOTS_TAG = ('<!-- DEMO: remove this noindex line at launch. Canonical points at the planned live address. -->' + chr(10) + '<meta name="robots" content="noindex">' if PREVIEW
              else '<meta name="robots" content="index, follow">')


# ---- Netlify Forms: every lead form uses the same name and field set, written into the static HTML ----
NETLIFY_FORM = 'name="lead" method="post" action="/thank-you/" data-netlify="true" data-netlify-honeypot="bot-field"'
_TRACK = ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid")
def netlify_hidden(source, service="", city=""):
    hid = lambda n, v="": f'<input type="hidden" name="{n}" value="{esc(v)}">'
    return (hid("form-name", "lead") + hid("source", source) + hid("origin_service", service) + hid("origin_city", city) + hid("page_url")
            + "".join(hid(t) for t in _TRACK)
            + '<p class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="bot-field" tabindex="-1" autocomplete="off"></label></p>')

def head(title, desc, path, up, extra_head="", jsonld=None, depth_assets=None, robots=None):
    A = shared(up)      # shared v3 css, assets
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>\n' for j in (jsonld or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{ROBOTS_TAG}
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Puget Sound Builders &amp; Renovation">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}{OG}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{OG}">
<meta name="theme-color" content="#0c0c0c">
<link rel="preload" href="{A}assets/fonts/outfit-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{A}assets/fonts/hanken-grotesk-latin-wght.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{A}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{A}apple-touch-icon.png">
{css_links(A, up)}
{DEV_SCRIPT}
{extra_head}{ld}</head>
'''

def banner():
    return f'''<div class="banner" role="region" aria-label="Announcement" data-offer="{esc(OFFER)}">
  <div class="banner__track"><div class="banner__group"><span class="banner__item">{esc(OFFER)}</span></div></div>
  <button class="banner__pause" type="button" aria-pressed="false" aria-label="Pause announcement">
    <svg class="i-pause" viewBox="0 0 12 12" aria-hidden="true"><rect x="2" y="1.5" width="2.8" height="9" rx="0.6" fill="currentColor"/><rect x="7.2" y="1.5" width="2.8" height="9" rx="0.6" fill="currentColor"/></svg>
    <svg class="i-play" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1.8v8.4L10 6 3 1.8Z" fill="currentColor"/></svg>
  </button>
</div>
'''

def _service_links():
    pages = URLS["servicePages"]
    return [(label, pages[key]) for label, key in _SERVICE_ORDER]

def _area_links():
    return [(c["name"], f'/service-areas/{c["slug"]}/') for c in _CITY_LIST]

def _menu_links(links):
    return "".join(f'<a class="menu__sublink" href="{href}">{esc(label)}</a>' for label, href in links)

def _nav_links(links):
    return "".join(f'<a href="{href}">{esc(label)}</a>' for label, href in links)

def header(up, current, home):
    A = shared(up)
    L = {"about": URLS["about"], "contact": CONTACT, "services": URLS["services"], "areas": "/service-areas/", "work": URLS["projects"], "blog": URLS["blog"]}
    services, areas = _service_links(), _area_links()
    def a(key, label, tip):
        cur = ' aria-current="page"' if current == key else ""
        return f'<a class="dock__item" href="{L[key]}" data-tip="{tip}"{cur}><span class="dock__label">{label}</span></a>'
    def drop(key, label, tip, panel_id, links, wide=False):
        cur = ' aria-current="page"' if current == key else ""
        wide_cls = " nav__panel--wide" if wide else ""
        return f'''<div class="nav__drop">
        <a class="dock__item" href="{L[key]}" data-tip="{tip}"{cur}><span class="dock__label">{label}</span></a>
        <button class="nav__chev" type="button" aria-expanded="false" aria-controls="{panel_id}" aria-label="Show {esc(label.lower())}"><span aria-hidden="true"></span></button>
        <div class="nav__panel{wide_cls}" id="{panel_id}">{_nav_links(links)}</div>
      </div>'''
    def group(key, label, panel_id, links):
        return f'''<div class="menu__item">
      <div class="menu__row"><a class="menu__link" href="{L[key]}">{label}</a><button class="menu__chev" type="button" aria-expanded="false" aria-controls="{panel_id}" aria-label="Show {esc(label.lower())}"></button></div>
      <div class="menu__sub" id="{panel_id}">{_menu_links(links)}</div>
    </div>'''
    brand_href = "#top" if home else "../"
    solid = "" if home else " is-solid"
    phone = f'<a class="dock__item dock__phone" data-opt href="tel:{PHONE_TEL}" data-tip="Call the office"><span class="dock__label">{PHONE_TXT}</span></a>'
    return f'''<header class="site-header{solid}">
  <a class="brand" href="{brand_href}" aria-label="Puget Sound Builders &amp; Renovation">
    <img class="brand__mark" src="{A}assets/logo-mark.webp" width="55" height="48" alt="" decoding="async">
    <span class="brand__name"><b>Puget Sound</b><small>Builders &amp; Renovation</small></span>
  </a>
  <div class="pill" data-motion="subtle">
    <nav class="nav" aria-label="Main">
      <span class="dock__glass" aria-hidden="true"></span>
      {a("about", "About", "Who we are")}
      {drop("services", "Services", "Kitchens, ADUs, baths, decks", "nav-services", services)}
      {drop("areas", "Areas", "Cities we serve", "nav-areas", areas, True)}
      {a("work", "Projects", "Recent remodeling work")}
      {a("blog", "Blog", "Blog")}
      {a("contact", "Contact", "Talk to the office")}
      {phone}
    </nav>
    <a class="pill__cta" href="{L['contact']}" data-book>Free Consultation</a>
    <div class="dock__tip" aria-hidden="true"><div class="dock__tipText"></div></div>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu">
      <span class="menu-toggle__label">Menu</span><span class="menu-toggle__icon" aria-hidden="true"><i></i><i></i><i></i></span>
    </button>
  </div>
</header>

<div class="menu-scrim" aria-hidden="true"></div>
<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Site menu">
  <nav class="menu__links" aria-label="Menu">
    <div class="menu__item"><a class="menu__link" href="{L['about']}">About</a></div>
    {group("services", "Services", "menu-services", services)}
    {group("areas", "Service areas", "menu-areas", areas)}
    <div class="menu__item"><a class="menu__link" href="{L['work']}">Projects</a></div>
    <div class="menu__item"><a class="menu__link" href="{L['blog']}">Blog</a></div>
    <div class="menu__item"><a class="menu__link" href="{L['contact']}">Contact</a></div>
  </nav>
  <div class="menu__foot">
    <a class="btn btn--primary" href="{L['contact']}" data-book>Free Consultation{BTN_ARROW}</a>
  </div>
</div>
'''

PH_ICON = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 20l1.3-4.2A8 8 0 1 1 8.4 18.8L4 20Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8.5c0 3.5 3 6.5 6.5 6.5l1-1.5-2-1-1 .8c-1-.4-2-1.4-2.4-2.4l.8-1-1-2-1.9.6Z" fill="currentColor"/></svg>'
BK_ICON = '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="4" y="5" width="16" height="15" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 3v4M16 3v4M4 10h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

def mbar(up):
    c = CONTACT
    return f'''<nav class="mbar" aria-label="Quick contact">
  <a href="tel:{PHONE_TEL}">{PH_ICON}Call</a>
  <a class="mbar__book" href="{c}" data-book>{BK_ICON}Free consultation</a>
</nav>
'''

SVC_LINKS = [("Kitchens", "kitchen"), ("Bathrooms", "bathroom"), ("ADU and DADU", "adu"), ("Decks", "deck"),
             ("Siding", "siding"), ("Flooring and painting", "flooring-painting")]

def footer(up, home=False):
    c = CONTACT
    who = URLS["about"]
    privacy = URLS["privacy"]
    A = shared(up)
    return f'''<footer class="foot">
  <div class="foot__inner">
    <div class="foot__top">
      <div class="foot__brand">
        <a class="foot__logo" href="{'#top' if home else '../'}" aria-label="Puget Sound Builders &amp; Renovation home"><img src="{A}assets/logo-mark.webp" width="55" height="48" alt="" loading="lazy"><span class="lock"><b>Puget Sound</b><small>Builders &amp; Renovation</small></span></a>
        <p>General contractor in Bellevue, WA.</p>
      </div>
      <nav class="foot__group" aria-label="Explore"><h2>Explore</h2><ul><li><a href="{who}">About</a></li><li><a href="{URLS['services']}">Services</a></li><li><a href="/service-areas/">Service areas</a></li><li><a href="{URLS['projects']}">Projects</a></li><li><a href="{URLS['blog']}">Blog</a></li><li><a href="{c}">Contact</a></li></ul></nav>
      <nav class="foot__group" aria-label="Services"><h2>Services</h2><ul><li><a href="{URLS['services']}">Kitchen remodeling</a></li><li><a href="{URLS['services']}">Bathroom remodeling</a></li><li><a href="{URLS['services']}">ADUs &amp; DADUs</a></li></ul></nav>
      <div class="foot__group foot__contact"><h2>Contact</h2><ul><li><a href="tel:{PHONE_TEL}">{PHONE_TXT}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    </div>
    <div class="foot__base">
      <p>&copy; 2026 Puget Sound Builders &amp; Renovation</p>
      <p><a href="{privacy}">Privacy policy</a></p>
    </div>
  </div>
</footer>
'''

def faq_items(which):
    q = [
        ("Do you offer free consultations?", [f"Yes. You can book a free consultation to talk through your project. Use the button on this page, call {PHONE_TXT}."]),
        ("How long does a kitchen remodel take?", ["It depends on the size of the kitchen, the permits it needs and how long cabinets and materials take to arrive. We talk through a realistic schedule for your project at the consultation."]),
        ("Do you handle permits?", ["Many remodeling projects in Washington need a permit, and the rules differ by city. Ask us at your consultation which permits your project needs and how they are handled."]),
        ("What is an ADU or DADU?", ["An ADU is an accessory dwelling unit: a small, separate home on the same lot as a main house. A DADU is a detached one, built as its own small building. We build both."]),
        ("Are you licensed and insured?", ["Washington requires contractors to register with the state Department of Labor and Industries, and you can look up any contractor on the L&I website. Ask us for our registration number and proof of insurance at your consultation."]),
        ("How do quotes work?", ["We look at your project with you, then put together a scope and a price. Your consultation is where we explain how that works for the job you have in mind."]),
    ]
    return q if which == "all" else q[:3]

def faq_html(items):
    out = []
    for qn, ans in items:
        body = "".join(f"<p>{esc(p)}</p>" for p in ans)
        out.append(f'<details><summary>{esc(qn)}<span class="plus" aria-hidden="true"></span></summary><div class="ans">{body}</div></details>')
    return "".join(out)

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": qn, "acceptedAnswer": {"@type": "Answer", "text": " ".join(ans)}} for qn, ans in items]}

def org_ld():
    # only confirmed fields: no city list, no social profiles, no rating, no licence number
    return {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "Puget Sound Builders & Renovation",
            "url": SITE + "/", "telephone": PHONE_TEL, "email": EMAIL, "image": SITE + OG,
            "areaServed": ["Bellevue, WA", "The Eastside", "Greater Seattle area"]}

def crumbs_ld(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

# ---------------------------------------------------------------- reusable sections ----
def trust(count_years=True):
    return f'''<section class="trust" id="trust" aria-label="Why people trust us">
  <div class="trust__grid">
    <div class="trust__item rv"><div class="trust__val">General contractor</div><div class="trust__label">Based in Bellevue, WA</div></div>
    <div class="trust__item rv" style="--d:.06s"><div class="trust__val"><span data-count="5" data-suffix="+">5+</span> years</div><div class="trust__label">in business</div></div>
    <div class="trust__item rv" style="--d:.12s"><div class="trust__val">Free consultation</div><div class="trust__label">Tell us what you want to change</div></div>
    <div class="trust__item rv" style="--d:.18s"><div class="trust__val">Licensed in WA</div><div class="trust__label">Washington contractor</div></div>
    <div class="trust__item rv" style="--d:.24s"><div class="trust__val">Insured</div><div class="trust__label">and bonded</div></div>
    <div class="trust__item rv" style="--d:.3s"><div class="trust__val">4.9</div><div class="trust__label">Google rating</div></div>
  </div>
</section>
'''

def map_svg():
    W, H = 560, 600
    def px(lat, lon): return (round((lon + 122.52) / 0.86 * (W - 60) + 30, 1), round((48.12 - lat) / 1.06 * (H - 60) + 30, 1))
    coast = [(48.12, -122.30), (47.99, -122.25), (47.90, -122.32), (47.80, -122.38), (47.70, -122.40), (47.61, -122.385), (47.52, -122.40), (47.40, -122.345), (47.30, -122.365), (47.26, -122.43), (47.20, -122.455), (47.06, -122.50)]
    sea = "M0 0 H" + str(px(48.12, -122.30)[0]) + " " + " ".join(f"L{px(a, b)[0]} {px(a, b)[1]}" for a, b in coast) + f" L0 {H} Z"
    lakew = [(47.755, -122.26), (47.69, -122.285), (47.63, -122.275), (47.58, -122.285), (47.53, -122.25), (47.50, -122.20), (47.56, -122.205), (47.60, -122.215), (47.66, -122.215), (47.72, -122.235), (47.755, -122.25)]
    lakes = [(47.74, -122.10), (47.65, -122.105), (47.59, -122.10), (47.54, -122.085), (47.545, -122.06), (47.60, -122.07), (47.66, -122.08), (47.74, -122.085)]
    poly = lambda pts: "M" + " L".join(f"{px(a, b)[0]} {px(a, b)[1]}" for a, b in pts) + " Z"
    pins = ""
    for n, la, lo in CITIES:
        x, y = px(la, lo)
        if n == "Bellevue":
            pins += f'<circle class="ring" cx="{x}" cy="{y}" r="9"/><circle class="pin pin--home" data-city="{n}" cx="{x}" cy="{y}" r="7"/>'
        else:
            pins += f'<circle class="pin" data-city="{n}" cx="{x}" cy="{y}" r="5"><title>{n}</title></circle>'
    labels = ""
    for n, dx, dy, anc in (("Bellevue", 14, 5, "start"), ("Seattle", -12, -6, "end"), ("Everett", 12, -4, "start"), ("Tacoma", -12, 4, "end")):
        la, lo = [(c[1], c[2]) for c in CITIES if c[0] == n][0]; x, y = px(la, lo)
        labels += f'<text x="{x + dx}" y="{y + dy}" text-anchor="{anc}">{n}</text>'
    return f'''<svg viewBox="0 0 {W} {H}" role="img" aria-label="Schematic map of the Puget Sound area with the 27 cities BNR serves. Bellevue is highlighted.">
<rect class="land" width="{W}" height="{H}"/><path class="sea" d="{sea}"/><path class="sea" d="{poly(lakew)}"/><path class="sea" d="{poly(lakes)}"/>
<path class="coast" d="M{px(*coast[0][::1])[0]} {px(*coast[0])[1]} {' '.join('L%s %s' % px(a, b) for a, b in coast[1:])}"/>
<text class="water-label" x="60" y="330">Puget Sound</text>{pins}{labels}</svg>'''

def area_section(h2="27 cities around Puget Sound."):
    home = ' class="home"'
    lis = "".join(f'<li data-city="{n}"{home if n == "Bellevue" else ""}>{n}</li>' for n, *_ in CITIES)
    return f'''<section class="sec sec--dark" id="area" aria-labelledby="area-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="area-h">{h2}</h2><p class="lede">From our Bellevue office we work across the Eastside and Seattle, north to Everett and Marysville, and south to Tacoma. Hover a city to find it on the map.</p></div>
    <div class="area">
      <div class="map rv">{map_svg()}<p class="map__cap">Schematic map, not to scale.</p></div>
      <ul class="cities rv" aria-label="Cities we serve">{lis}</ul>
    </div>
  </div>
</section>
'''

def reviews_section(up):
    plats = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in LINKS.items())
    return f'''<section class="sec sec--slab" id="reviews" aria-labelledby="rev-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="rev-h">What clients say.</h2><p class="lede">We only show real, verified reviews.</p></div>
    <div id="reviews-list" class="rev__empty rv">
      <h3 class="h3">Reviews coming soon</h3>
      <p>We are collecting verified reviews to show here. In the meantime you can find us on these sites.</p>
      <div class="platforms">{plats}</div>
    </div>
    <script type="application/json" id="reviews-data">[]</script>
  </div>
</section>
'''

# Netlify Forms registers a form only when this markup is in the published HTML.
# Every page uses the same form name so the submissions land in one form.
def form_open(klass, source, label, id_attr=""):
    ident = f' id="{id_attr}"' if id_attr else ""
    return (f'<form class="{klass}"{ident} name="lead" method="POST" action="/" data-netlify="true" data-netlify-honeypot="bot-field" '
            f'data-form data-source="{esc(source)}" novalidate aria-label="{esc(label)}">')

def honeypot():
    return '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="bot-field" tabindex="-1" autocomplete="off"></label></div>'

def netlify_fields(source, origin_service=None, service=None):
    rows = [
        '<input type="hidden" name="form-name" value="lead">',
        f'<input type="hidden" name="source" value="{esc(source)}">',
        '<input type="hidden" name="origin_city" value="General">',
        '<input type="hidden" name="origin_page" value="">',
    ]
    if origin_service is not None:
        rows.append(f'<input type="hidden" name="origin_service" value="{esc(origin_service)}">')
    if service is not None:
        rows.append(f'<input type="hidden" name="service" value="{esc(service)}">')
    for key in ("utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "gbraid", "wbraid", "msclkid", "fbclid", "landing_page", "referrer"):
        rows.append(f'<input type="hidden" name="{key}" value="">')
    return "\n        ".join(rows)

def cta_section(up, mini=True):
    c = "contact-us/" if up == "" else "../contact-us/"
    bg = '<svg viewBox="0 0 1200 600" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="120" y="120" width="560" height="360" pathLength="1"/><path pathLength="1" d="M120 300 H680 M400 120 V480 M120 210 H300 M500 390 H680"/><path pathLength="1" d="M680 220 H900 V480 H680"/><path pathLength="1" d="M900 220 L790 140 L680 220"/><rect pathLength="1" x="740" y="330" width="60" height="150"/><line pathLength="1" x1="60" y1="480" x2="1140" y2="480"/><path pathLength="1" d="M120 90 H680 M120 80 V100 M680 80 V100"/></svg>'
    form = f'''{form_open("form form--card", "about-quick", "Request a consultation")}
        {netlify_fields("about-quick", "Free consultation", "")}
        <div class="fld"><label for="m-name">Name</label><input id="m-name" name="name" type="text" autocomplete="name" data-req aria-describedby="m-name-err"><p class="err" id="m-name-err" role="alert"></p></div>
        <div class="fld"><label for="m-phone">Phone</label><input id="m-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" data-req data-kind="phone" aria-describedby="m-phone-err"><p class="err" id="m-phone-err" role="alert"></p></div>
        <div class="form__two">
          <div class="fld"><label for="m-zip">ZIP code</label><input id="m-zip" name="zip" type="text" autocomplete="postal-code" inputmode="numeric" data-req data-kind="zip" aria-describedby="m-zip-err"><p class="err" id="m-zip-err" role="alert"></p></div>
          <div class="fld"><label for="m-email">Email</label><input id="m-email" name="email" type="email" autocomplete="email" data-req data-kind="email" aria-describedby="m-email-err"><p class="err" id="m-email-err" role="alert"></p></div>
        </div>
        {honeypot()}
        <button class="btn btn--primary" type="submit">Book your free consultation{BTN_ARROW}</button>
        <p class="form__fail err" tabindex="-1" hidden role="alert">Something went wrong. Please call (425) 696-4004.</p>
        <div class="form__ok" role="status"><strong>Thank you.</strong><span class="form__ok-text"></span></div>
      </form>''' if mini else ""
    return f'''<section class="sec fin" id="contact" aria-labelledby="cta-h">
  <div class="cta__bg" aria-hidden="true">{bg}</div>
  <div class="wrap cta__grid">
    <div class="rv">
      <h2 class="cta__big" id="cta-h">Ready when you are.</h2>
      <p class="lede">Tell us about your project and we will take it from there.</p>
      <div class="cta__lines"><a class="bigtel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a></div>
      <div class="row" style="margin-top:28px"><a class="btn btn--primary" href="{c}">Book your free consultation{BTN_ARROW}</a></div>
    </div>
    <div class="rv" style="--d:.1s">{form}</div>
  </div>
</section>
'''

def css_links(A, up):
    # published (root) pages load one minified stylesheet built by scripts/build-assets.mjs, the dev pages load the three source files
    if ROOT:
        return f'<link rel="stylesheet" href="{A}css/site.min.css">'
    return (f'<link rel="stylesheet" href="{A}css/site.css">\n<link rel="stylesheet" href="{A}css/hero-v3.css">\n<link rel="stylesheet" href="{up}css/v4.css">')

def scripts(up, home):
    # all scripts are deferred. The published (root) pages load one minified bundle of the site's own scripts, built by scripts/build-assets.mjs in this exact order.
    A = shared(up)
    if ROOT:
        return f'''<script>if(innerWidth>900)document.write('<script defer src="{A}vendor/gsap.min.js"><\\/script>')</script>
<script defer src="{A}js/site.min.js"></script>
'''
    return f'''<script>if(innerWidth>900)document.write('<script defer src="{A}vendor/gsap.min.js"><\\/script>')</script>
<script defer src="{up}js/forms.js"></script>
<script defer src="{up}js/motion.js"></script>
<script defer src="{up}js/svc.js"></script>
<script defer src="{up}js/sx.js"></script>
<script defer src="{up}js/pj.js"></script>
<script defer src="{up}js/v4.js"></script>
<script defer src="{up}js/hero-v4.js"></script>
{f'<script defer src="{A}js/hero-draft.js"></script>' if home else ''}
<script defer src="{A}js/dock.js"></script>
{f'<script defer src="{up}js/who.js"></script>' if home else ''}
{f'<script defer src="{up}js/services.js"></script>' if home else ''}
<script defer src="{up}js/trust.js"></script>
{f'<script defer src="{up}js/wrf.js"></script>' if home else ''}
{f'<script defer src="{up}js/hero-v4-flip.js"></script>' if home else ''}
'''

def w(rel, s):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("wrote", rel, len(s))

exec(open(os.path.join(os.path.dirname(__file__), "v4-gen-pages.py"), encoding="utf-8").read())
