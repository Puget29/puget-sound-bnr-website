# Work rail (#work): "Check our last jobs". Exec'd by v4-gen-pages.py (shares esc, ARROW, URLS, AS).
# Only the client's real photos: ids come from data/last-jobs.json, each must be real true and stock false in data/projects.json.
# Alt text is generic (service only), no place names, the only caption is the service name. Files are the existing WebP files in site/assets/projects/.
_PROJ = {p["id"]: p for p in json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "projects.json"), encoding="utf-8"))}
_LAST = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "last-jobs.json"), encoding="utf-8"))["ids"]
WORK_NAMES = {"kitchen": "Kitchen", "bathroom": "Bathroom", "roofing": "Roofing", "deck": "Deck", "adu": "ADU", "siding": "Siding", "flooring": "Flooring", "painting": "Painting"}

def work_section():
    cards = ""
    for i, pid in enumerate(_LAST):
        p = _PROJ.get(pid)
        if not p or p.get("real") is not True or p.get("stock") is not False or p.get("service") not in WORK_NAMES:
            raise SystemExit(f"work rail: {pid} is not a real, non stock project photo")
        base = os.path.join(SITE_DIR, "assets", "projects", pid)
        ws = [w for w in (640, 960) if os.path.exists(f"{base}-{w}.webp")]
        if not ws:
            raise SystemExit(f"work rail: no files for {pid}")
        name = WORK_NAMES[p["service"]]
        srcset = ", ".join(f"{AS}assets/projects/{pid}-{w}.webp {w}w" for w in ws)
        pos = p.get("objectPosition", "50% 50%")
        cards += (f'<li class="work__c"><figure class="work__f"><span class="work__img"><img src="{AS}assets/projects/{pid}-{ws[-1]}.webp" srcset="{srcset}" sizes="(min-width: 900px) 340px, 78vw" '
                  f'width="{p["w"]}" height="{p["h"]}" alt="Completed {name.lower()} project" loading="lazy" decoding="async" style="object-position:{pos}"></span>'
                  f'<figcaption class="work__n">{esc(name)}</figcaption></figure></li>')
    chev_l = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    chev_r = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="M8 4l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'''<section class="sec sec--stone work" id="work" aria-labelledby="work-h">
  <div class="wrap work__top">
    <div class="work__head rv">
      <h2 class="h2" id="work-h">Check our last jobs</h2>
      <p class="lede">Photos from our own recent work.</p>
    </div>
    <div class="work__ctl rv" style="--d:.08s">
      <button class="work__nav work__prev" type="button" aria-label="Previous jobs">{chev_l}</button>
      <button class="work__nav work__next" type="button" aria-label="Next jobs">{chev_r}</button>
    </div>
  </div>
  <div class="work__rail rv" style="--d:.12s" role="region" aria-label="Recent jobs, scroll sideways" tabindex="0">
    <ul class="work__track">{cards}</ul>
  </div>
  <div class="wrap work__foot rv"><a class="fq__book work__all" href="{URLS['projects']}"><span>See all projects</span>{ARROW}</a></div>
</section>
'''
