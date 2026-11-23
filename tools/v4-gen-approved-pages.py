# Approved Contact, Projects and Home text, using the shared long page renderer.
def _approved_section(section, page, index, blocks=None):
    return _k_section(section['title'], f'{page}-copy-{index}',
                      'sec--slab' if index % 2 else 'sec--stone',
                      _k_blocks(section['lines']) if blocks is None else blocks, 'split')

def _approved_faq(section, page, count, blocks=None):
    faq, pairs = _k_faq(_k_blocks(section['lines']) if blocks is None else blocks,
                        page, section['title'], count)
    plain = lambda value: _kr.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', value).replace('**', '')
    return faq, faq_ld([(q, [plain(a)]) for q, a in pairs])

def _approved_contact():
    meta, sections = _k_parse_copy('contact.md', 'Contact', 8)
    intro = _k_blocks(sections[0]['lines'])
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Contact</span></nav>'
    hero = photo_hero('../', 'project-47', '60% 55%', 'ct-h', crumbs, esc(meta['H1']),
                      _k_inline(intro[0][1]), f'<a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>', 'short')
    old = contact()
    form = _kr.search(r'<section class="sec sec--slab" aria-label="Contact form">.*?</section>', old, _kr.S)
    if not form: raise SystemExit('Contact form section not found')
    parts = ['<main id="main" class="long-service-page">', hero, brand_strip('../', True), form.group()]
    parts.append(_approved_section(sections[0], 'contact', 1, intro[1:]))
    # Render sections[1:5] normally; replace the "Areas We Serve" section (sections[5]) with the GBP map embed.
    parts.extend(_approved_section(s, 'contact', i + 2) for i, s in enumerate(sections[1:5]))
    _c_areas = sections[5]
    _c_areas_lede = next((l for l in _c_areas['lines'] if l.strip()), '')
    parts.append(map_embed('contact-areas', 'sec--stone', _c_areas['title'], _c_areas_lede))
    faq, schema = _approved_faq(sections[6], 'contact', 6)
    parts.extend([faq, _approved_section(sections[7], 'contact', 8), '</main>'])
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], CONTACT, '../', photo_preload('../', 'project-47'), [])  # Other page: no schema
            + '<body><a class="skip" href="#main">Skip to content</a>' + banner() + header('../', 'contact', False)
            + ''.join(parts) + footer('../') + mbar('../') + scripts('../', False) + '</body></html>')

w('contact/index.html', _approved_contact())

def _approved_projects():
    meta, sections = _k_parse_copy('projects.md', 'Projects', 7)
    intro = _k_blocks(sections[0]['lines'])
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Projects</span></nav>'
    hero = photo_hero('../', 'kitchen-06', '50% 50%', 'pj-h', crumbs, esc(meta['H1']),
                      _k_inline(intro[0][1]), f'<a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>', 'short')
    old, _ = _projects_page()
    gallery = _kr.search(r'<section class="sec sec--slab pj".*?</section>', old, _kr.S)
    if not gallery: raise SystemExit('Projects gallery not found')
    sv = {'chip': '', 'formHeading': 'Free consultation', 'formService': 'Projects page'}
    form = lead_block('contact', 'pj-c-h', 'Have a project like these in mind?', 'Send a few details and we will take it from there. We reply within one business day.', _form(sv, 'projects-page'), pimg('../', 'project-45', '(min-width:901px) 40vw, 90vw', '50% 60%', False, ''))
    parts = ['<main id="main" class="long-service-page">', hero, brand_strip('../', True), gallery.group(), _approved_section(sections[0], 'projects', 1, intro[1:])]
    parts.extend(_approved_section(s, 'projects', i + 2) for i, s in enumerate(sections[1:5]))
    parts.append(wrf_reviews_section(False, 'What clients say.', 'Real Google reviews, in their own words.', find_us('../')))
    faq, schema = _approved_faq(sections[5], 'projects', 5)
    parts.extend([faq, _approved_section(sections[6], 'projects', 7), form, '</main>'])
    path = URLS['projects']
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], path, '../', photo_preload('../', 'kitchen-06'), [])  # Other page: no schema
            + '<body><a class="skip" href="#main">Skip to content</a>' + banner() + header('../', 'work', False)
            + ''.join(parts) + footer('../') + mbar('../') + scripts('../', False) + '</body></html>')

w('remodeling-projects/index.html', _approved_projects())

_HOME_CSS = ("<style>"
             "#reviews .rvw__head{justify-items:center;text-align:center;justify-self:center}"
             "#reviews .rvw__head .lede{margin-left:auto;margin-right:auto}"
             "#reviews .rvw__head h2,#reviews .rvw__head .h2{max-width:none;margin-left:auto;margin-right:auto}"
             "#home-areas .ha-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:26px;align-items:stretch;margin-top:28px}"
             "#home-areas .ha-map{border-radius:16px;overflow:hidden;min-height:360px;border:1px solid rgba(245,242,236,.16)}"
             "#home-areas .ha-map iframe{width:100%;height:100%;min-height:360px;border:0;display:block}"
             "#home-areas .ha-panel{align-self:center}"
             "#home-areas .ha-list{columns:2;column-gap:28px;list-style:none;margin:8px 0 22px;padding:0}"
             "#home-areas .ha-list li{margin:0 0 10px}"
             "#home-areas .ha-list a{opacity:.9}#home-areas .ha-list a:hover{opacity:1;text-decoration:underline}"
             "@media(max-width:820px){#home-areas .ha-grid{grid-template-columns:1fr}#home-areas .ha-map,#home-areas .ha-map iframe{min-height:300px}#home-areas .ha-list{columns:1}}"
             "</style>")

def _approved_home():
    meta, raw = _k_parse_copy('home-text.md', 'Home', 7, False)
    sections = []
    for source in raw:
        lines = list(source['lines'])
        titles = [i for i, line in enumerate(lines) if line.startswith('### ')]
        if not titles: raise SystemExit('Home block has no heading: ' + source['title'])
        i = titles[0]
        sections.append({'title': lines[i][4:].strip(), 'lines': lines[i + 1:]})
    intro = _approved_section(sections[0], 'home', 1).replace('id="home-copy-1"', 'id="who"')
    services_text = _approved_section(sections[1], 'home', 2)
    services_inner = services_text[services_text.index('>') + 1:services_text.rindex('</section>')]
    services = services_section()
    services, n = _kr.subn(r'<div class="wrap">\s*<div class="sec__head rv">.*?</div>\s*</div>\s*(?=<div class="car")', lambda m: services_inner, services, count=1, flags=_kr.S)
    if n != 1: raise SystemExit('Home services introduction not found')
    services = services.replace("</section>", '  <div class="wrap" style="text-align:center;margin-top:34px"><a class="btn btn--primary" href="' + URLS["services"] + '">View all services' + BTN_ARROW + "</a></div>\n</section>", 1)
    faq_blocks = _k_blocks([line[1:] if line.startswith('#### ') else line for line in sections[5]['lines']])
    faq, schema = _approved_faq(sections[5], 'home', 6, faq_blocks)
    _areas_lede = next((l for l in sections[4]['lines'] if l.strip()), '')
    # Two SEO content sections for the second half, Bellevue-optimized, using the location-page section styles.
    _plan_cards = [
        ("Name and rank your priorities", "List what is not working, from a dated kitchen to a leaking roof, then decide which issues the budget should solve first."),
        ("Think about the whole home", "A single update is often the moment to plan related work, so the house moves in one direction instead of in pieces."),
        ("Respect the home's era", "Bellevue homes range from mid-century houses to newer builds, so we check wiring, insulation and roof condition before planning finishes."),
        ("Plan permits and scope early", "Structural work, roofs, decks and ADUs go through the City of Bellevue, and a settled scope keeps surprises down."),
    ]
    seo_plan = _km_feature_section("home-planning", "sec--slab", "km-svc",
        "Custom Home Remodeling in Bellevue: Planning Your Project",
        "A custom home remodel in Bellevue goes best when a few things are settled before any finish is chosen. Start with these.",
        _plan_cards, _KM_SVC_ICONS)
    _kb_lines = ["Kitchens and bathrooms are the rooms Bellevue homeowners remodel most, and they are where good planning pays off. We give both meaningful attention as part of a home remodeling project, or as standalone updates.", "",
        "- **Kitchen remodeling in Bellevue.** New layouts, cabinets, countertops, backsplashes and lighting, planned around how you actually cook. See our [kitchen remodeling](/our-services/kitchen-remodeling/) page for the full scope.",
        "- **Bathroom remodeling in Bellevue.** Showers, tubs, vanities, tile and fixtures, built on proper waterproofing and ventilation. See our [bathroom remodeling](/our-services/bathroom-remodeling/) page for details.",
        "- **One coordinated project.** When a kitchen or bathroom connects to wider work, we plan it together so the result feels intentional, not assembled from separate jobs."]
    seo_kb = _k_section("Kitchen and Bathroom Remodeling in Bellevue", "home-kb", "sec--stone", _k_blocks(_kb_lines), "full")
    # Service-areas section: GBP map embed beside links to nearby location pages (within ~20 mi), plus a hub button.
    _nearby = ["kirkland", "redmond", "medina", "clyde-hill", "hunts-point", "yarrow-point", "mercer-island", "newcastle",
               "renton", "issaquah", "sammamish", "bothell", "kenmore", "woodinville", "lake-forest-park", "shoreline",
               "mountlake-terrace", "tukwila"]
    _cn = {c["slug"]: c["name"] for c in _CITY_LIST}
    _links = "".join('<li><a href="/service-areas/' + s + '/">' + esc(_cn[s]) + "</a></li>" for s in _nearby if s in _cn)
    areas = ('<section class="sec sec--slab" id="home-areas" aria-labelledby="home-areas-h">\n  <div class="wrap">\n'
             '    <div class="sec__head rv" style="display:block;text-align:left"><h2 class="h2" id="home-areas-h" style="max-width:none;margin:0">'
             + esc(sections[4]["title"]) + '</h2><p class="lede" style="margin:0">' + esc(_areas_lede) + "</p></div>\n"
             '    <div class="ha-grid">\n'
             '      <div class="ha-map"><iframe src="' + GBP_MAP_SRC + '" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen title="Puget Sound Builders and Renovation on Google Maps, Bellevue"></iframe></div>\n'
             '      <div class="ha-panel"><p class="lede" style="margin:0 0 6px;font-size:1rem">Nearby communities we serve:</p><ul class="ha-list">' + _links + "</ul>"
             '<a class="btn btn--primary" href="/service-areas/">See all service areas' + BTN_ARROW + "</a></div>\n"
             "    </div>\n  </div>\n</section>\n")
    parts = [hero().replace('<main id="main">', '<main id="main" class="long-service-page km">', 1), brand_strip(''), intro, services,
             _approved_section(sections[2], 'home', 3), work_section(),
             _approved_section(sections[3], 'home', 4), wrf_reviews_section(),
             seo_plan, seo_kb, areas,
             _approved_section(sections[6], 'home', 7), faq, landing_cta_section(), '</main>']
    body = ''.join(parts).replace('href="#form"', f'href="{CONTACT}"')
    gsc = '<meta name="google-site-verification" content="1rXgYukCh58P5gVZ0ANdIL9ES_GztLeMtfmEu6sRW6A">'
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], '/', '', gsc + loader_head + _KM_CSS + _HOME_CSS, [org_ld()])  # Homepage: LocalBusiness only
            + '<body><a class="skip" href="#main">Skip to content</a>' + banner() + header('', None, True)
            + body + footer('', True) + mbar('') + scripts('', True) + '</body></html>')

w('index.html', _approved_home())
