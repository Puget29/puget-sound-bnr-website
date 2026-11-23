# About page from the approved copy, using the long service page renderer.
_AB_UP = "../"
_AB_HERO = ("kitchen-04", "50% 55%")

def _about():
    meta, sections = _k_parse_copy("about.md", "About", 8)
    intro = _k_blocks(sections[0]["lines"])
    if not intro or intro[0][0] != "paragraph":
        raise SystemExit("About introduction must begin with a paragraph")
    crumbs = '<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">About</span></nav>'
    hero = photo_hero(_AB_UP, _AB_HERO[0], _AB_HERO[1], "ab-h", crumbs, esc(meta["H1"]),
                      _k_inline(intro[0][1]), f'<a class="btn btn--primary" href="{CONTACT}" data-book>Book your free consultation{BTN_ARROW}</a>')
    parts = ['<main id="main" class="long-service-page">\n', hero, brand_strip(_AB_UP, True)]
    for i, section in enumerate(sections[:6]):
        blocks = intro[1:] if i == 0 else _k_blocks(section["lines"])
        parts.append(_k_section(section["title"], f"about-section-{i + 1}",
                                "sec--slab" if i % 2 == 0 else "sec--stone", blocks, "split"))
    # Testimonials section removed from the About page by request.
    faq, pairs = _k_faq(_k_blocks(sections[6]["lines"]), "about", sections[6]["title"], 6)
    parts.append(faq)
    # Keep the sentence around the final CTA intact while linking its action.
    final_blocks = _k_blocks(sections[7]["lines"])
    final_html = []
    for kind, value in final_blocks:
        if kind == "paragraph" and "[Book your free consultation]" in value:
            before, after = value.split("[Book your free consultation]", 1)
            final_html.append('<p class="kitchen-copy__p about-inline-cta">' + _k_inline(before) +
                              f'<a class="btn btn--primary" href="{esc(CONTACT)}">Book your free consultation{BTN_ARROW}</a>' + _k_inline(after) + '</p>')
            final_html.append('<div class="about-desktop-cta" hidden>' + _k_paragraph(value) + '</div>')
        else:
            final_html.append(_k_render_blocks([(kind, value)]))
    parts.append(f'<section class="sec sec--slab kitchen-section" id="about-contact" aria-labelledby="about-contact-h"><div class="wrap kitchen-layout kitchen-layout--split"><div><h2 class="h2" id="about-contact-h">{esc(sections[7]["title"])}</h2></div><div class="kitchen-copy">{"".join(final_html)}</div></div></section>')
    parts.append("</main>\n")
    plain = lambda text: _kr.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text).replace('**', '')
    ld = []  # Other page: no schema
    return (head(meta["TITLE TAG"], meta["META DESCRIPTION"], "/about/", _AB_UP, photo_preload(_AB_UP, _AB_HERO[0]), ld)
            + '<body class="long-service-page-body">\n<!-- About page generated from approved copy. -->\n'
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_AB_UP, "about", False)
            + ''.join(parts).replace('href="#form"', f'href="{CONTACT}"') + footer(_AB_UP) + mbar(_AB_UP) + scripts(_AB_UP, False) + '</body>\n</html>\n')

w("about/index.html", _about())
