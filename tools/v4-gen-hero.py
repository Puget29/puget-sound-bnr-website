# Photo hero shared by About, Contact, Services overview and Projects. Exec'd from v4-gen-pages.py before the pages are built.
# One real job photo (stock false), full width, dark overlay stronger on the text side, 1440 and 960 WebP, preloaded as the LCP image.
# Alt text is empty on purpose: the picture is decoration behind the headline. No place names anywhere.
import json as _hj, os as _hos
_HP = _hos.path.dirname(_hos.path.dirname(_hos.path.abspath(__file__)))
_HPJ = {q["id"]: q for q in _hj.load(io.open(_hos.path.join(_HP, "data", "projects.json"), encoding="utf-8"))}

def _hero_ok(pid):
    if pid.startswith("asset:"):
        key = pid.split(":", 1)[1]
        if key != "painting-card":
            raise SystemExit(f"photo hero: unsupported supplied image {pid}")
        base = _hos.path.join(_HP, "site", "assets", "projects", key)
        if not all(_hos.path.isfile(f"{base}-{w}.webp") for w in (640, 960)):
            raise SystemExit(f"photo hero: supplied image files missing for {pid}")
        return {"w": 960, "h": 1200}
    q = _HPJ.get(pid)
    if not q or q.get("real") is False or q.get("stock") or q.get("lowres"):
        raise SystemExit(f"photo hero: {pid} is not a real, sharp job photo")
    return q

def photo_preload(up, pid):
    q = _hero_ok(pid)
    if pid.startswith("asset:"):
        name = pid.split(":", 1)[1]
        return f'<link rel="preload" as="image" href="{up}assets/projects/{name}-960.webp" type="image/webp" fetchpriority="high">\n'
    widths = q.get("widths", [640, 960, 1440])
    desktop = 1440 if 1440 in widths else max(widths)
    mobile = 960 if 960 in widths else max(widths)
    return (f'<link rel="preload" as="image" href="{up}assets/projects/{pid}-{mobile}.webp" type="image/webp" media="(max-width: 900px)" fetchpriority="high">\n'
            f'<link rel="preload" as="image" href="{up}assets/projects/{pid}-{desktop}.webp" type="image/webp" media="(min-width: 901px)" fetchpriority="high">\n')

def photo_hero(up, pid, pos, hid, crumbs, h1, lede, buttons, size="tall"):
    q = _hero_ok(pid)
    return f'''<section class="page-hero page-hero--photo phero phero--{size}" aria-labelledby="{hid}">
  <picture class="phero__bg" aria-hidden="true">
    <source media="(max-width: 900px)" srcset="{up}assets/projects/{pid}-960.webp">
    <img src="{up}assets/projects/{pid}-1440.webp" width="1440" height="{round(1440 * q.get("h", 960) / q.get("w", 1440))}" alt="" fetchpriority="high" decoding="async" style="object-position:{pos}">
  </picture>
  <div class="phero__ov" aria-hidden="true"></div>
  <div class="wrap page-hero__grid"><div class="phero__t">
    {crumbs}
    <h1 id="{hid}">{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="row phero__row">{buttons}</div>
  </div></div>
</section>
'''

# ---------------------------------------------------------------- icons (24px line, gold via CSS currentColor)
_ICO = {
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6l8-3z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 10h8M8 13h5"/>',
    "clip": '<rect x="6" y="4" width="12" height="17" rx="2"/><path d="M9 4h6v3H9zM9 12h6M9 16h4"/>',
    "headset": '<path d="M4 14v-2a8 8 0 0116 0v2"/><rect x="3" y="13" width="4" height="6" rx="1.5"/><rect x="17" y="13" width="4" height="6" rx="1.5"/><path d="M19 19c0 1.5-2 2-5 2"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "tag": '<path d="M3 12V4h8l10 10-8 8L3 12z"/><circle cx="8" cy="8.5" r="1.5"/>',
    "hammer": '<path d="M14 4l6 6-3 3-6-6 3-3z"/><path d="M11 9L3 17l4 4 8-8"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.4l2.7 2.7L16 9.6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a2 2 0 01-2 2A16 16 0 013 6a2 2 0 012-2z"/>',
    "insta": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="0.7"/>',
}
def ico(name): return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{_ICO[name]}</svg>'

# ---------------------------------------------------------------- lead block: one headline per page, form on the right
def lead_block(sid, hid, h2, line, form_html, ph_img="", bg_img="", pts=None, htag="h2"):
    pts = pts or ["Free consultation", "Licensed, bonded and insured in Washington", "We reply within one business day"]
    li = "".join(f'<li>{ico("check")}<span>{esc(p)}</span></li>' for p in pts)
    bg = f'<div class="lead__bg" aria-hidden="true">{bg_img}</div><div class="lead__ov" aria-hidden="true"></div>' if bg_img else ""
    ph = f'<figure class="lead__ph">{ph_img}</figure>' if ph_img else ""
    return f'''<section class="sec sec--slab lead" id="{sid}" aria-labelledby="{hid}">
  {bg}
  <div class="wrap lead__grid">
    <div class="lead__l rv"><{htag} class="h2" id="{hid}">{h2}</{htag}><p class="lede">{line}</p>
      <a class="lead__tel" href="tel:{PHONE_TEL}">{ico("phone")}<span>{PHONE_TXT}</span></a>
      <ul class="lead__pts">{li}</ul>{ph}</div>
    <div class="rv" style="--d:.1s">{form_html}</div>
  </div>
</section>
'''

def pimg(up, pid, sizes, pos=None, eager=False, alt="", cls=""):
    q = _hero_ok(pid)
    ws = sorted(w for w in (q.get("widths") or (640, 960, 1440)) if w <= 1440)
    mid = 960 if 960 in ws else max(ws)
    ss = ", ".join(up + "assets/projects/" + pid + "-" + str(w) + ".webp " + str(w) + "w" for w in ws)
    fp = pos or q.get("objectPosition", "50% 50%")
    ld = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    c = ('class="' + cls + '" ') if cls else ""
    return ("<img " + c + 'src="' + up + "assets/projects/" + pid + "-" + str(mid) + '.webp" srcset="' + ss + '" sizes="' + sizes + '" width="' + str(q.get("w", 1440)) + '" height="' + str(q.get("h", 960)) + '" alt="' + esc(alt) + '" ' + ld + ' style="object-position:' + esc(fp) + '">')

def find_us(up):
    L = dict(LINKS)
    def logo(src, w, h, name): return f'<img src="{src}" alt="{name}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    base = f"{up}assets/logos/ppc/"
    items = [("Instagram", L["Instagram"], ico("insta") + "<span>Instagram</span>"),
             ("Facebook", L["Facebook"], logo(base + "facebook.webp", 24, 24, "Facebook")),
             ("Yelp", L["Yelp"], logo(base + "yelp.svg", 60, 24, "Yelp")),
             ("Angi", L["Angi"], logo(base + "angi.webp", 60, 24, "Angi"))]
    a = "".join(f'<a class="fus__b" href="{esc(u)}" target="_blank" rel="noopener noreferrer" aria-label="{n} (opens in a new tab)">{h}</a>' for n, u, h in items)
    g = _TJ["google"]["url"]
    return (f'<div class="fus rv"><p class="fus__l">Find us on</p>{a}</div>'
            f'<div class="fus__all rv"><a class="rvw__b" href="{esc(g)}" target="_blank" rel="noopener noreferrer" aria-label="Read all our reviews on Google (opens in a new tab)"><span>Read all our reviews on Google</span>{ARROW}</a></div>')

