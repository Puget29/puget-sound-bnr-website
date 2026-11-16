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
    parts.extend(_approved_section(s, 'contact', i + 2) for i, s in enumerate(sections[1:6]))
    faq, schema = _approved_faq(sections[6], 'contact', 6)
    parts.extend([faq, _approved_section(sections[7], 'contact', 8), '</main>'])
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], '/contact/', '../', photo_preload('../', 'project-47'), [org_ld(), crumbs_ld('Contact', '/contact/'), schema])
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
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], path, '../', photo_preload('../', 'kitchen-06'), [org_ld(), _crumb_ld([('Home', '/'), ('Projects', path)]), schema])
            + '<body><a class="skip" href="#main">Skip to content</a>' + banner() + header('../', 'work', False)
            + ''.join(parts) + footer('../') + mbar('../') + scripts('../', False) + '</body></html>')

w('remodeling-projects/index.html', _approved_projects())

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
    faq_blocks = _k_blocks([line[1:] if line.startswith('#### ') else line for line in sections[5]['lines']])
    faq, schema = _approved_faq(sections[5], 'home', 6, faq_blocks)
    parts = [hero().replace('<main id="main">', '<main id="main" class="long-service-page">', 1), brand_strip(''), intro, services,
             _approved_section(sections[2], 'home', 3), work_section(),
             _approved_section(sections[3], 'home', 4), wrf_reviews_section(),
             _approved_section(sections[4], 'home', 5), faq,
             _approved_section(sections[6], 'home', 7), landing_cta_section(), '</main>']
    body = ''.join(parts).replace('href="#form"', f'href="{CONTACT}"')
    return (head(meta['TITLE TAG'], meta['META DESCRIPTION'], '/', '', loader_head, [org_ld(), schema])
            + '<body><a class="skip" href="#main">Skip to content</a>' + banner() + header('', None, True)
            + body + footer('', True) + mbar('') + scripts('', True) + '</body></html>')

w('index.html', _approved_home())
