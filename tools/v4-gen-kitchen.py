# Kitchen service page and the shared long page renderer. Page copy is read from content/*.md.
# This file is exec'd by v4-gen-svcpages.py and shares that generator's helpers.
import re as _kr

def _k_parse_copy(copy_file="kitchen.md", service_name="Kitchen", expected_sections=9, require_h1=True):
    source = io.open(_os.path.join(_P, "content", copy_file), encoding="utf-8").read()
    meta = {}
    for key in (("TITLE TAG", "META DESCRIPTION", "H1") if require_h1 else ("TITLE TAG", "META DESCRIPTION")):
        match = _kr.search(r"(?m)^" + _kr.escape(key) + r"(?:\s*\([^\n]*?\))?:\s*(.+)$", source)
        if not match: raise SystemExit(service_name + " copy is missing " + key)
        meta[key] = match.group(1).strip()
    start = source.find("## ")
    if start < 0: raise SystemExit(service_name + " copy has no sections")
    sections = []
    current = None
    for line in source[start:].splitlines():
        if line.startswith("## "):
            current = {"title": line[3:].strip(), "lines": []}
            sections.append(current)
        elif current is not None:
            current["lines"].append(line)
    if len(sections) != expected_sections: raise SystemExit(f"{service_name} copy has {len(sections)} main sections, expected {expected_sections}")
    return meta, sections

def _k_inline(value):
    pattern = _kr.compile(r"\*\*([^*]+)\*\*|\[([^\]]+)\]\(([^)]+)\)")
    out, pos = [], 0
    for match in pattern.finditer(value):
        plain = esc(value[pos:match.start()])
        plain = _kr.sub(_kr.escape(PHONE_TXT), lambda _m: f'<a href="tel:{PHONE_TEL}">{esc(PHONE_TXT)}</a>', plain)
        out.append(plain)
        if match.group(1) is not None:
            out.append("<strong>" + _k_inline(match.group(1)) + "</strong>")
        else:
            label = match.group(2).strip().lower()
            routes = {
                "kitchen remodeling": _SPU["kitchen-main"],
                "bathroom remodeling": _SPU["bathroom-main"],
                "roofing": _SPU["roofing-main"],
                "siding": _SPU["siding"],
                "deck building": _SPU["deck-building"],
                "adu and garage conversion": _SPU["adu-garage-conversion"],
                "flooring": _SPU["floor-main"],
                "painting": _SPU["painting"],
                "blog": URLS["blog"],
                "services": URLS["services"],
                "services page": URLS["services"],
                "projects": URLS["projects"],
                "projects page": URLS["projects"],
            }
            out.append(f'<a class="kitchen-inline-link" href="{esc(routes.get(label, match.group(3)))}">{esc(match.group(2))}</a>')
        pos = match.end()
    plain = esc(value[pos:])
    plain = _kr.sub(_kr.escape(PHONE_TXT), lambda _m: f'<a href="tel:{PHONE_TEL}">{esc(PHONE_TXT)}</a>', plain)
    out.append(plain)
    return "".join(out)

def _k_button(label, kind="primary", href=None, arrow=True):
    if label == "Call (425) 696-7586" or label == "call (425) 696-7586":
        href = "tel:" + PHONE_TEL
        kind = "ghost"
        arrow = False
    href = href or "#form"
    icon = BTN_ARROW if arrow and kind == "primary" else ""
    return f'<a class="btn btn--{kind}" href="{esc(href)}">{esc(label)}{icon}</a>'

_KCTA = r"\[(Book your free consultation|Call \(425\) 696-7586|Get your free estimate)\]"
_KCOMBO = _kr.compile(r"\[(Book your free consultation|Get your free estimate)\] or call \(425\) 696-7586")

def _k_cta_row(labels, separator=""):
    parts = []
    for i, label in enumerate(labels):
        if i and separator: parts.append(f'<span class="kitchen-cta__or">{esc(separator)}</span>')
        parts.append(_k_button(label))
    return '<div class="row kitchen-cta">' + "".join(parts) + "</div>"

def _k_paragraph(value):
    stripped = value.strip()
    labels = _kr.findall(_KCTA, stripped)
    if labels and _kr.sub(_KCTA + r"\s*", "", stripped).strip() == "":
        return _k_cta_row(labels)
    combo = _KCOMBO.search(value)
    if combo:
        before = value[:combo.start()].strip()
        after = value[combo.end():].strip()
        if after.startswith(", and ") and before.endswith("."):
            before = before[:-1] + "," + after[1:]
            after = ""
        elif after == ".":
            after = ""
        chunks = ([f'<p class="kitchen-copy__p">{_k_inline(before)}</p>'] if before else [])
        chunks.append(_k_cta_row([combo.group(1), "call (425) 696-7586"], "or"))
        if after: chunks.append(f'<p class="kitchen-copy__p">{_k_inline(after)}</p>')
        return "".join(chunks)
    matches = list(_kr.finditer(_KCTA, value))
    if not matches: return f'<p class="kitchen-copy__p">{_k_inline(value)}</p>'
    chunks, pos = [], 0
    for match in matches:
        before = value[pos:match.start()].strip()
        after = value[match.end():].strip()
        if after.startswith("and ") and before.endswith("."):
            before = before[:-1] + ", " + after
            after = ""
        if before: chunks.append(f'<p class="kitchen-copy__p">{_k_inline(before)}</p>')
        chunks.append(_k_cta_row([match.group(1)]))
        pos = match.end()
        if not after:
            pos = len(value)
    after = value[pos:].strip()
    if after: chunks.append(f'<p class="kitchen-copy__p">{_k_inline(after)}</p>')
    return "".join(chunks)

def _k_blocks(lines):
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == "---":
            i += 1
            continue
        if line.startswith("### "):
            blocks.append(("heading", line[4:].strip())); i += 1; continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [cell.strip() for cell in lines[i].strip().strip("|").split("|")]
                if not all(_kr.fullmatch(r"[-: ]+", cell or " ") for cell in cells): rows.append(cells)
                i += 1
            if rows: blocks.append(("table", rows))
            continue
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:]); i += 1
            blocks.append(("list", items)); continue
        if _kr.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and _kr.match(r"^\d+\. ", lines[i].strip()):
                items.append(_kr.sub(r"^\d+\. ", "", lines[i].strip(), count=1)); i += 1
            blocks.append(("steps", items)); continue
        paragraph = [line]; i += 1
        while i < len(lines) and lines[i].strip() and lines[i].strip() != "---" and not lines[i].strip().startswith(("### ", "- ", "|")) and not _kr.match(r"^\d+\. ", lines[i].strip()):
            paragraph.append(lines[i].strip()); i += 1
        blocks.append(("paragraph", " ".join(paragraph)))
    return blocks

def _k_render_blocks(blocks, list_class="kitchen-list"):
    out = []
    for kind, value in blocks:
        if kind == "heading":
            heading_class = " kitchen-copy__h--related" if value.strip().lower() == "related services" else ""
            out.append(f'<h3 class="h3 kitchen-copy__h{heading_class}">{_k_inline(value)}</h3>')
        elif kind == "paragraph":
            out.append(_k_paragraph(value))
        elif kind == "list":
            if "kitchen-why-list" in list_class:
                items = "".join(f'<li>{_k_inline(item)}</li>' for item in value)
            else:
                items = "".join(_sv_bullet_item(_k_inline(item)) for item in value)
            bullet_class = "" if "kitchen-why-list" in list_class else "sv-bullets "
            out.append('<ul class="' + bullet_class + list_class + '">' + items + '</ul>')
        elif kind == "steps":
            step_rows = []
            for n, item in enumerate(value, 1):
                match = _kr.match(r"\*\*(.+?)\*\*\s*(.*)$", item)
                title, text = (match.group(1), match.group(2)) if match else ("", item)
                heading = f'<h3 class="h3">{_k_inline(title)}</h3>' if title else ""
                step_rows.append(f'<li class="sv-step"><span class="sv-step__n" aria-hidden="true">{n:02d}</span><div>{heading}<p>{_k_inline(text)}</p></div></li>')
            out.append('<ol class="sv-steps kitchen-steps">' + "".join(step_rows) + '</ol>')
        elif kind == "table":
            rows = value
            head = "".join(f'<th scope="col">{_k_inline(cell)}</th>' for cell in rows[0])
            body = "".join('<tr>' + "".join(f'<td>{_k_inline(cell)}</td>' for cell in row) + '</tr>' for row in rows[1:])
            out.append(f'<div class="kitchen-table"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
    return "".join(out)

def _k_section(title, section_id, surface, blocks, layout="full", list_class="kitchen-list"):
    content = _k_render_blocks(blocks, list_class)
    structured = " kitchen-section--steps" if any(kind == "steps" for kind, _ in blocks) else (" kitchen-section--list" if any(kind == "list" for kind, _ in blocks) else "")
    heading = f'<h2 class="h2" id="{section_id}-h">{esc(title)}</h2>'
    if layout == "split":
        inner = f'<div class="wrap kitchen-layout kitchen-layout--split"><div>{heading}</div><div class="kitchen-copy">{content}</div></div>'
    else:
        inner = f'<div class="wrap kitchen-layout"><div class="kitchen-layout__head">{heading}</div><div class="kitchen-copy">{content}</div></div>'
    return f'<section class="sec {surface} kitchen-section{structured}" id="{section_id}" aria-labelledby="{section_id}-h">{inner}</section>\n'

def _k_gallery(sv, page_key="kitchen"):
    tiles = ""
    for pid in sv["gallery"]:
        q = _photo(pid); widths = sorted(q["widths"]); big = max(widths); mid = 960 if 960 in widths else big
        large = ", ".join(f"{_photo_src(pid, w)} {w}w" for w in widths if w >= mid)
        all_src = ", ".join(f"{_photo_src(pid, w)} {w}w" for w in widths if w <= 1440)
        tiles += (f'<li><a class="gal__a" href="{_photo_src(pid, big)}" data-srcset="{large}"><img src="{_photo_src(pid, mid)}" srcset="{all_src}" sizes="(min-width:900px) 31vw, 46vw" '
                  f'width="{q.get("w", 960)}" height="{q.get("h", 640)}" alt="{esc(q["alt"])}" loading="lazy" decoding="async" style="object-position:{esc(q.get("objectPosition", "50% 50%"))}"></a></li>')
    cap = " gal--cap" if len(sv["gallery"]) > 8 else ""
    return f'''<section class="sec sec--dark kitchen-section" id="{page_key}-gallery" aria-labelledby="{page_key}-gallery-h">
  <div class="wrap"><div class="sec__head rv"><h2 class="h2" id="{page_key}-gallery-h">{esc(sv.get("galleryHeading", "Our " + sv["workName"] + " work."))}</h2><p class="lede">{esc(sv.get("galleryIntro", "Photos of our own jobs. Tap a photo to see it larger."))}</p></div>
    <div class="gal{cap} rv" data-gal><ul class="gal__list">{tiles}</ul><button class="gal__more" type="button" aria-expanded="false" hidden>Show more</button></div>
  </div>
</section>
'''

def _k_photo_break(ids, page_key="kitchen"):
    figures = "".join(f'<figure class="kitchen-photo-break__figure">{_img(pid, "(min-width:901px) 42vw, 92vw", "kitchen-photo-break__img")}</figure>' for pid in ids)
    return f'<div class="kitchen-photo-break" data-service="{page_key}"><div class="wrap kitchen-photo-break__grid">{figures}</div></div>\n'

def _k_faq(blocks, page_key="kitchen", faq_title="Kitchen Remodeling FAQs", expected_count=8):
    pairs = []
    i = 0
    while i < len(blocks):
        if blocks[i][0] != "heading" or i + 1 >= len(blocks) or blocks[i + 1][0] != "paragraph":
            raise SystemExit(f"{page_key} FAQ source must have a question heading followed by its answer")
        pairs.append((blocks[i][1], blocks[i + 1][1]))
        i += 2
    if len(pairs) != expected_count: raise SystemExit(f"{page_key} FAQ has {len(pairs)} entries, expected {expected_count}")
    items = "".join(f'<details class="sv-faq__r" name="{page_key}faq"{" open" if i == 0 else ""}><summary><span>{esc(q)}</span><span class="plus" aria-hidden="true"></span></summary><div class="sv-faq__a"><p>{_k_inline(a)}</p></div></details>' for i, (q, a) in enumerate(pairs))
    section = f'''<section class="sec sec--stone kitchen-section" id="{page_key}-faq" aria-labelledby="{page_key}-faq-h">
  <div class="wrap kitchen-layout kitchen-layout--split"><div><h2 class="h2" id="{page_key}-faq-h">{esc(faq_title)}</h2></div><div class="sv-faq">{items}</div></div>
</section>
'''
    return section, pairs

def _kitchen_page(sv):
    meta, sections = _k_parse_copy()
    by_title = {s["title"]: s for s in sections}
    intro = _k_blocks(by_title["Kitchen Remodeling in Seattle, WA"]["lines"])
    if not intro or intro[0][0] != "paragraph": raise SystemExit("Kitchen introduction must begin with a paragraph")
    hero_lede = _k_inline(intro[0][1])
    intro_blocks = intro[1:]

    ids = {
        "Kitchen Remodeling in Seattle, WA": "kitchen-intro",
        "Kitchen Remodeling Services We Offer": "kitchen-services",
        "A Seamless Experience From Start to Finish": "kitchen-process",
        "Planning Your Kitchen Remodel: Layout and Budget Basics": "kitchen-planning",
        "Cabinets, Countertops and Where Quality Actually Matters": "kitchen-cabinets",
        "Living Through a Kitchen Renovation": "kitchen-living",
        "Why Homeowners Choose Puget Sound BNR for Kitchen Remodeling": "kitchen-why",
        "Kitchen Remodeling FAQs": "kitchen-faq",
        "Kitchen Remodeling in Seattle, Bellevue and Surrounding Areas": "kitchen-area",
    }
    menu = [(title, ids[title]) for title in ids]
    nav = '<nav class="kitchen-jump" aria-label="On this page"><div class="wrap"><strong>On this page</strong><ul>' + "".join(f'<li><a href="#{anchor}">{esc(label)}</a></li>' for label, anchor in menu) + '</ul></div></nav>'

    path = _SPU[sv["slug"]]
    hero = f'''<main id="main" class="long-service-page">
<section class="page-hero sv-hero" aria-labelledby="kitchen-h1">
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_SPU["overview"]}">Services</a><span aria-hidden="true">/</span><span aria-current="page">Kitchen Remodeling</span></nav>
      <h1 id="kitchen-h1">{esc(meta["H1"])}</h1>
      <p class="lede" style="margin-bottom:30px">{hero_lede}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(sv["heroPhoto"], "(min-width:901px) 46vw, 92vw", "", True, sv.get("heroFocal"))}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
{nav}
'''

    html_parts = [hero]
    html_parts.append(_k_section(sections[0]["title"], ids[sections[0]["title"]], "sec--slab", intro_blocks, "split"))
    html_parts.append(_k_section(sections[1]["title"], ids[sections[1]["title"]], "sec--stone", _k_blocks(sections[1]["lines"]), "split", "sv-offer kitchen-check-list"))
    html_parts.append(_k_section(sections[2]["title"], ids[sections[2]["title"]], "sec--slab", _k_blocks(sections[2]["lines"]), "split"))
    html_parts.append(_k_gallery(sv))
    html_parts.append(_k_section(sections[3]["title"], ids[sections[3]["title"]], "sec--stone", _k_blocks(sections[3]["lines"]), "full"))
    html_parts.append(_k_section(sections[4]["title"], ids[sections[4]["title"]], "sec--slab", _k_blocks(sections[4]["lines"]), "full"))
    html_parts.append(_k_photo_break(["kitchen-02", "kitchen-06"]))
    html_parts.append(_k_section(sections[5]["title"], ids[sections[5]["title"]], "sec--stone", _k_blocks(sections[5]["lines"]), "split"))
    html_parts.append(_k_section(sections[6]["title"], ids[sections[6]["title"]], "sec--slab", _k_blocks(sections[6]["lines"]), "full", "kitchen-list kitchen-why-list"))
    html_parts.append(_reviews())
    faq_section, faq_pairs = _k_faq(_k_blocks(sections[7]["lines"]), "kitchen", sections[7]["title"])
    html_parts.append(faq_section)
    html_parts.append(_k_section(sections[8]["title"], ids[sections[8]["title"]], "sec--slab", _k_blocks(sections[8]["lines"]), "split"))
    last_photo = sv["gallery"][-1]
    closing_photo = (_img(last_photo, "(min-width:901px) 40vw, 90vw") if last_photo.startswith("asset:")
                     else pimg(_UP, last_photo, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = lead_block("contact", "kitchen-form-h", esc(sv["closingHeading"]), "Send a few details and we will take it from there. We reply within one business day.", _form(sv), closing_photo)
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    html_parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    ld = [_crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), ("Kitchen Remodeling", path)]),
          {"@context": "https://schema.org", "@type": "Service", "@id": SITE + path + "#service", "name": "Kitchen Remodeling",
           "serviceType": "Kitchen Remodeling", "description": meta["META DESCRIPTION"], "url": SITE + path,
           "image": _abs_photo(sv["heroPhoto"]), "provider": {"@id": SITE + "/#localbusiness"},
           "areaServed": [{"@type": "City", "name": "Seattle"}, {"@type": "City", "name": "Bellevue"}]},
          faq_ld([(q, [a]) for q, a in faq_pairs])]
    page = (head(meta["TITLE TAG"], meta["META DESCRIPTION"], path, _UP, photo_preload(_UP, sv["heroPhoto"]), ld)
            + "<body class=\"long-service-page-body\">\n<!-- Kitchen page generated from the approved Kitchen copy file. -->\n"
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "services", False)
            + "".join(html_parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    visible_copy = _kr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_kr.S)
    if "WhatsApp" in visible_copy or "wa.me" in visible_copy: raise SystemExit("Kitchen page must not include WhatsApp")
    w(_rel_of(_SPU["kitchen-remodeling"]), page)

_kitchen_page(next(page for page in _ALL_SP if page["slug"] == "kitchen-remodeling"))

def _long_service_page(sv, copy_file, page_key, photo_break_ids):
    service_name = sv["h1Service"]
    meta, sections = _k_parse_copy(copy_file, service_name)
    intro = _k_blocks(sections[0]["lines"])
    if not intro or intro[0][0] != "paragraph":
        raise SystemExit(service_name + " introduction must begin with a paragraph")
    hero_lede = _k_inline(intro[0][1])
    suffixes = ("intro", "services", "process", "planning", "details", "living", "why", "faq", "area")
    ids = {section["title"]: f"{page_key}-{suffixes[i]}" for i, section in enumerate(sections)}
    menu = [(section["title"], ids[section["title"]]) for section in sections]
    nav = '<nav class="kitchen-jump" aria-label="On this page"><div class="wrap"><strong>On this page</strong><ul>' + "".join(
        f'<li><a href="#{anchor}">{esc(label)}</a></li>' for label, anchor in menu) + "</ul></div></nav>"
    path = _SPU[sv["slug"]]
    hero = f'''<main id="main" class="long-service-page">
<section class="page-hero sv-hero" aria-labelledby="{page_key}-h1">
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_SPU["overview"]}">Services</a><span aria-hidden="true">/</span><span aria-current="page">{esc(service_name)}</span></nav>
      <h1 id="{page_key}-h1">{esc(meta["H1"])}</h1>
      <p class="lede" style="margin-bottom:30px">{hero_lede}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(sv["heroPhoto"], "(min-width:901px) 46vw, 92vw", "", True, sv.get("heroFocal"))}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
{nav}
'''
    parts = [hero]
    parts.append(_k_section(sections[0]["title"], ids[sections[0]["title"]], "sec--slab", intro[1:], "split"))
    parts.append(_k_section(sections[1]["title"], ids[sections[1]["title"]], "sec--stone", _k_blocks(sections[1]["lines"]), "split", "sv-offer kitchen-check-list"))
    parts.append(_k_section(sections[2]["title"], ids[sections[2]["title"]], "sec--slab", _k_blocks(sections[2]["lines"]), "split"))
    # siding has no real, service-specific client project photos yet, so its "work" gallery is skipped.
    if sv["slug"] != "siding":
        parts.append(_k_gallery(sv, page_key))
    parts.append(_k_section(sections[3]["title"], ids[sections[3]["title"]], "sec--stone", _k_blocks(sections[3]["lines"]), "full"))
    parts.append(_k_section(sections[4]["title"], ids[sections[4]["title"]], "sec--slab", _k_blocks(sections[4]["lines"]), "full"))
    for pid in photo_break_ids:
        _check_real(pid, sv["photoService"])
    parts.append(_k_photo_break(photo_break_ids, page_key))
    parts.append(_k_section(sections[5]["title"], ids[sections[5]["title"]], "sec--stone", _k_blocks(sections[5]["lines"]), "split"))
    parts.append(_k_section(sections[6]["title"], ids[sections[6]["title"]], "sec--slab", _k_blocks(sections[6]["lines"]), "full", "kitchen-list kitchen-why-list"))
    parts.append(_reviews())
    faq_section, faq_pairs = _k_faq(_k_blocks(sections[7]["lines"]), page_key, sections[7]["title"])
    parts.append(faq_section)
    area = _k_section(sections[8]["title"], ids[sections[8]["title"]], "sec--slab", _k_blocks(sections[8]["lines"]), "split")
    area = area.replace('class="sec sec--slab kitchen-section"', 'class="sec sec--slab kitchen-section long-service-area"', 1)
    parts.append(area)
    last_photo = sv["gallery"][-1]
    closing_photo = (_img(last_photo, "(min-width:901px) 40vw, 90vw") if last_photo.startswith("asset:")
                     else pimg(_UP, last_photo, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = lead_block("contact", f"{page_key}-form-h", esc(sv["closingHeading"]), "Send a few details and we will take it from there. We reply within one business day.", _form(sv), closing_photo)
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    service_schema_name = meta["H1"].removesuffix(" in Seattle, WA")
    ld = [_crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), (service_name, path)]),
          {"@context": "https://schema.org", "@type": "Service", "@id": SITE + path + "#service", "name": service_schema_name,
           "serviceType": service_schema_name, "description": meta["META DESCRIPTION"], "url": SITE + path,
           "image": _abs_photo(sv["heroPhoto"]), "provider": {"@id": SITE + "/#localbusiness"},
           "areaServed": [{"@type": "City", "name": "Seattle"}, {"@type": "City", "name": "Bellevue"}]},
          faq_ld([(q, [a]) for q, a in faq_pairs])]
    page = (head(meta["TITLE TAG"], meta["META DESCRIPTION"], path, _UP, photo_preload(_UP, sv["heroPhoto"]), ld)
            + f'<body class="long-service-page-body">\n<!-- {esc(service_name)} page generated from its approved copy file. -->\n'
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "services", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    visible_copy = _kr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_kr.S)
    if "WhatsApp" in visible_copy or "wa.me" in visible_copy:
        raise SystemExit(service_name + " page must not include WhatsApp")
    w(_rel_of(_SPU[sv['slug']]), page)

# Long pages are generated only for services that keep a dedicated Seattle (or standalone) URL.
# deck-building, adu-garage-conversion and painting are NOT here on purpose: their real addresses are
# the main /our-services/ pages, which must stay general and Bellevue focused, so they are served by the
# short _page() template from their service records (same as the other /our-services/ pages). The old
# Seattle copy in content/deck.md, content/adu.md and content/painting.md is retained but no longer rendered.
_long_only = _os.environ.get("V4_LONG_SERVICE", "").strip().lower()
if _long_only not in ("", "bathroom", "roofing", "siding", "flooring"):
    raise SystemExit("V4_LONG_SERVICE must name a supported long service page")
if _long_only in ("", "bathroom"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "bathroom-remodeling"),
                       "bathroom.md", "bathroom", ["project-15", "project-18"])
if _long_only in ("", "roofing"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "roofing"),
                       "roofing.md", "roofing", ["project-29", "project-61"])
if _long_only in ("", "siding"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "siding"),
                       "siding.md", "siding", ["project-14", "project-14"])
if _long_only in ("", "flooring"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "flooring"),
                       "flooring.md", "flooring", ["project-12", "project-12"])


# ---- Kitchen (Bellevue) pilot design refinement. Everything below is scoped to this one page. ----
# Line icons (24px, same stroke style as the homepage "More we do" icons).
_KM_WHY_ICONS = [
    '<path d="M12 21s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
    '<path d="M4 5h16v11H9l-4 3z"/>',
    '<path d="M9 4h6v3H9z"/><path d="M7 5H5v15h14V5h-2"/><path d="M8.5 12.5l2 2 4-4"/>',
    '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    '<path d="M12 3l2.6 5.6 6.2.7-4.6 4.2 1.3 6.1L12 16.9 6.5 19.6l1.3-6.1L3.2 9.3l6.2-.7z"/>',
]
_KM_SVC_ICONS = [
    '<path d="M4 4h16v16H4z"/><path d="M4 9h16M9 9v11"/>',
    '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M4 12h16"/>',
    '<path d="M5 4h14v16H5z"/><path d="M5 12h14M9 8h2M9 16h2"/>',
    '<path d="M3 10l2-4h14l2 4M3 10h18v3H3zM6 13v6M18 13v6"/>',
    '<path d="M3 11h18v7H3zM3 15h18M7 11V7h10v4"/>',
    '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 1 4 10c-1 1-1 2-1 3H9c0-1 0-2-1-3a6 6 0 0 1 4-10z"/>',
]
_KM_EASTSIDE = ["bellevue", "kirkland", "redmond", "sammamish", "issaquah", "bothell", "woodinville",
                "newcastle", "mercer-island", "renton", "kenmore", "medina", "clyde-hill", "hunts-point",
                "yarrow-point", "snoqualmie", "north-bend", "duvall", "carnation"]
_KM_MAP_SRC = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d10757.322140992934!2d-122.19868572399378"
               "!3d47.619705800000006!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x54905d4b2eab6f75"
               "%3A0x2ad4580dc612257!2sPuget%20Sound%20Builders%20%26%20Renovation%20-%20Kitchen%20%26%20"
               "Bathroom!5e0!3m2!1sen!2s!4v1795337633395!5m2!1sen!2s")

# Services image gallery for the "Remodeling and Building Services" section: (name, url, photo id,
# focal point). Same photos the homepage services carousel uses (services.js SERVICE_PHOTOS). Kitchen
# has an empty url so it is not a self-link. Links point at the Bellevue main service pages.
_KM_BUILD = [
    ("Kitchen remodeling", "", "project-01", "50% 50%"),
    ("Bathroom remodeling", "/our-services/bathroom-remodeling/", "project-07", "50% 55%"),
    ("Roofing", "/our-services/roofing/", "project-05", "50% 50%"),
    ("Deck building", "/our-services/deck-building/", "project-10", "50% 62%"),
    ("ADU and garage conversion", "/our-services/adu-garage-conversion/", "project-13", "50% 50%"),
    ("Siding", "/siding-replacement/", "project-14", "80% 50%"),
    ("Flooring", "/our-services/floor-replacement/", "project-12", "50% 50%"),
    ("Painting", "/our-services/painting/", "asset:painting-card", "50% 50%"),
]

_KM_CSS = """<style>
/* Kitchen Remodeling (Bellevue) pilot: page-scoped design refinements. Scoped under .km so no other
   page, shared component or global style is affected. */
.km .sec{padding-block:clamp(52px,7vw,104px)}
.km .sec__head{max-width:780px}
.km .sec__head .lede{margin-top:14px}
/* Tighten the gap between an H2 and its description in the stacked (full, non-split) sections:
   Process, Planning, Living, Signs. The shared .kitchen-layout gap is up to 64px, too airy here. */
.km .kitchen-layout:not(.kitchen-layout--split){gap:12px}
.km .kitchen-layout:not(.kitchen-layout--split) .kitchen-layout__head{margin-bottom:8px}
.km .km-why__grid,.km .km-svc__grid{list-style:none;margin:36px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:16px}
.km .km-why__card,.km .km-svc__card{flex:1 1 180px;min-width:0;border-radius:16px;padding:24px 22px}
@media (min-width:980px){.km .km-why__grid,.km .km-svc__grid{flex-wrap:nowrap}}
@media (max-width:560px){.km .km-why__card,.km .km-svc__card{flex:1 1 100%}}
.km .km-why__ico,.km .km-svc__ico{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:12px;margin-bottom:15px}
.km .km-why__ico svg,.km .km-svc__ico svg{width:24px;height:24px}
.km .km-why__t,.km .km-svc__t{font-size:1.05rem;margin:0 0 7px}
.km .km-why__card p,.km .km-svc__card p{margin:0;font-size:.94rem;line-height:1.55}
/* Why: light (stone) surface */
.km .km-why__card{background:#fff;border:1px solid rgba(0,0,0,.08);box-shadow:0 1px 2px rgba(0,0,0,.05)}
.km .km-why__ico{background:rgba(212,175,55,.16);color:var(--gold-d,#765217)}
/* Our Services: dark (slab) surface */
.km .km-svc__card{background:rgba(255,255,255,.04);border:1px solid var(--line-dark);transition:transform .2s ease,border-color .2s ease}
.km .km-svc__card:hover{transform:translateY(-3px);border-color:rgba(212,175,55,.5)}
.km .km-svc__ico{background:rgba(212,175,55,.15);color:var(--gold-l)}
.km .km-svc__card p{color:var(--text-2)}
.km .km-svc__note{margin:26px 0 0;font-size:.98rem;color:var(--text-2)}
.km .km-svc__note a{color:var(--gold-l);text-decoration:underline;text-underline-offset:3px}
/* Remodeling and Building Services: image gallery of services (like the homepage showcase) */
.km .km-gal__grid{display:grid;gap:14px;grid-template-columns:repeat(4,1fr);margin-top:30px}
.km .km-gal__card{position:relative;display:block;border-radius:14px;overflow:hidden;aspect-ratio:4/3;text-decoration:none}
.km .km-gal__ph{margin:0;height:100%}
.km .km-gal__img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .45s ease}
.km a.km-gal__card:hover .km-gal__img{transform:scale(1.05)}
.km .km-gal__cap{position:absolute;left:0;right:0;bottom:0;padding:28px 16px 14px;color:#fff;font-weight:600;font-size:.98rem;line-height:1.25;background:linear-gradient(to top,rgba(0,0,0,.74),rgba(0,0,0,0))}
@media (max-width:900px){.km .km-gal__grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:520px){.km .km-gal__grid{grid-template-columns:1fr}}
/* Process keeps the shared sv-steps design; only override colours so the step number and description
   stay legible on this light (stone) surface. The long-service-page defaults set .sv-step p and
   .sv-step__n light for dark pages, which would be invisible here. */
.km [id$="-process"] .sv-step p{color:var(--ink-text-2)}
.km [id$="-process"] .sv-step__n{color:var(--gold-d)}
/* SEO 1 Planning: two-column checklist with check marks (dark slab) */
.km [id$="-planning"] .sv-bullets{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px 34px;margin-top:6px}
.km [id$="-planning"] .sv-bullets li{align-items:flex-start}
.km [id$="-planning"] .sv-list__dot{width:20px;height:20px;margin-top:.1em;border-radius:6px;background:rgba(212,175,55,.16);position:relative;flex:0 0 auto}
.km [id$="-planning"] .sv-list__dot::after{content:"";position:absolute;left:6px;top:3px;width:5px;height:10px;border:solid var(--gold-l);border-width:0 2px 2px 0;transform:rotate(45deg)}
/* SEO 2 Living: vertical numbered timeline (dark slab) */
.km [id$="-living"] .sv-steps{list-style:none;margin:26px 0 0;padding:0}
.km [id$="-living"] .sv-step{border:0;padding:0 0 24px 0;grid-template-columns:48px minmax(0,1fr);align-items:start}
.km [id$="-living"] .sv-step:last-child{padding-bottom:0}
.km [id$="-living"] .sv-step__n{position:static;width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;border-radius:50%;background:rgba(212,175,55,.15);color:var(--gold-l);font-size:.9rem;font-weight:700}
.km [id$="-living"] .sv-step h3{margin:0 0 5px;font-size:1.02rem}
.km [id$="-living"] .sv-step p{margin:0;font-size:.92rem;line-height:1.5}
/* SEO 3 Signs: scannable cards in one row (light stone) */
.km [id$="-signs"] .sv-bullets{display:flex;flex-wrap:wrap;gap:14px;margin-top:10px}
.km [id$="-signs"] .sv-bullets li{flex:1 1 180px;min-width:0;background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:12px;padding:16px 18px;box-shadow:0 1px 2px rgba(0,0,0,.05)}
.km [id$="-signs"] .sv-list__dot{width:10px;height:10px;background:var(--gold);margin-top:.45em}
@media (min-width:980px){.km [id$="-signs"] .sv-bullets{flex-wrap:nowrap}}
@media (max-width:560px){.km [id$="-signs"] .sv-bullets li{flex:1 1 100%}}
/* Service Areas: two-column map + list (dark slab) */
.km .km-areas__grid{display:grid;grid-template-columns:1.05fr .95fr;gap:26px;align-items:stretch;margin-top:30px}
.km .km-areas__map{border-radius:16px;overflow:hidden;min-height:380px;border:1px solid var(--line-dark)}
.km .km-areas__map iframe{width:100%;height:100%;min-height:380px;border:0;display:block}
.km .km-areas__panel{display:flex;flex-direction:column;gap:18px}
.km .km-areas__list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:8px}
.km .km-areas__list a{display:block;padding:9px 12px;border:1px solid var(--line-dark);border-radius:9px;font-size:.9rem;color:var(--text);text-decoration:none;transition:border-color .2s,background .2s,color .2s}
.km .km-areas__list a:hover{border-color:rgba(212,175,55,.5);background:rgba(212,175,55,.08);color:var(--gold-l)}
.km .km-areas__all{align-self:flex-start}
/* Review button aligned left (overrides the shared injector's inline text-align:center) */
.km .rlg-review-cta{text-align:left !important;margin-top:28px}
@media (max-width:820px){
  .km .km-areas__grid{grid-template-columns:1fr}
  .km .km-areas__map,.km .km-areas__map iframe{min-height:300px}
}
</style>"""


def _km_svg(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + paths + "</svg>")


def _km_list_items(blocks):
    for kind, value in blocks:
        if kind == "list":
            return value
    return []


def _km_paras(blocks):
    return [value for kind, value in blocks if kind == "paragraph"]


def _km_cards(items):
    out = []
    for it in items:
        m = _kr.match(r"\s*\*\*(.+?)\*\*\s*(.*)$", it)
        out.append((m.group(1).strip().rstrip("."), m.group(2).strip()) if m else ("", it.strip()))
    return out


def _km_feature_section(sec_id, surface, base, title, lede, cards, icons, note=""):
    tiles = []
    for i, (t, d) in enumerate(cards):
        ico = ('<span class="' + base + '__ico">' + _km_svg(icons[i % len(icons)]) + "</span>") if icons else ""
        tiles.append('<li class="' + base + '__card rv" style="--d:' + format(min(i * 0.06, 0.4), ".2f") + 's">'
                     + ico + '<h3 class="' + base + '__t">' + esc(t) + "</h3><p>" + _k_inline(d) + "</p></li>")
    lede_html = ('<p class="lede">' + _k_inline(lede) + "</p>") if lede else ""
    note_html = ('<p class="' + base + '__note">' + _k_inline(note) + "</p>") if note else ""
    return ('<section class="sec ' + surface + " " + base + '" id="' + sec_id + '" aria-labelledby="' + sec_id + '-h">\n'
            '  <div class="wrap">\n'
            '    <div class="sec__head rv"><h2 class="h2" id="' + sec_id + '-h">' + esc(title) + "</h2>" + lede_html + "</div>\n"
            '    <ul class="' + base + '__grid">' + "".join(tiles) + "</ul>" + note_html + "\n"
            "  </div>\n</section>\n")


def _km_areas_section(page_key, title, intro):
    sid = page_key + "-area"
    links = "".join('<li><a href="/service-areas/' + s + '/">' + esc(_km_city_names[s]) + "</a></li>"
                    for s in _KM_EASTSIDE if s in _km_city_names)
    map_html = ('<iframe src="' + _KM_MAP_SRC + '" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" '
                'allowfullscreen title="Puget Sound Builders & Renovation on Google Maps"></iframe>')
    return ('<section class="sec sec--slab km-areas" id="' + sid + '" aria-labelledby="' + sid + '-h">\n'
            '  <div class="wrap">\n'
            '    <div class="sec__head rv"><h2 class="h2" id="' + sid + '-h">' + esc(title) + '</h2><p class="lede">' + _k_inline(intro) + "</p></div>\n"
            '    <div class="km-areas__grid">\n'
            '      <div class="km-areas__map">' + map_html + "</div>\n"
            '      <div class="km-areas__panel"><ul class="km-areas__list">' + links + "</ul>"
            '<a class="btn btn--ghost km-areas__all" href="/service-areas/">See all service areas</a></div>\n'
            "    </div>\n  </div>\n</section>\n")


def _km_build_section(page_key, title, intro):
    sid = page_key + "-build"
    tiles = []
    for name, url, pid, focus in _KM_BUILD:
        inner = ('<figure class="km-gal__ph">' + _img(pid, "(min-width:901px) 22vw, 46vw", "km-gal__img", False, focus)
                 + '</figure><span class="km-gal__cap">' + esc(name) + "</span>")
        if url:
            tiles.append('<a class="km-gal__card" href="' + url + '">' + inner + "</a>")
        else:
            tiles.append('<div class="km-gal__card km-gal__card--static">' + inner + "</div>")
    return ('<section class="sec sec--stone km-build" id="' + sid + '" aria-labelledby="' + sid + '-h">\n'
            '  <div class="wrap">\n'
            '    <div class="sec__head rv"><h2 class="h2" id="' + sid + '-h">' + esc(title) + '</h2><p class="lede">' + _k_inline(intro) + "</p></div>\n"
            '    <div class="km-gal__grid">' + "".join(tiles) + "</div>\n"
            '    <div style="text-align:center;margin-top:34px"><a class="btn btn--primary" href="' + URLS["services"] + '">View all services' + BTN_ARROW + "</a></div>\n"
            "  </div>\n</section>\n")


_km_city_names = {c["slug"]: c["name"] for c in _CITY_LIST}


def _km_main_page(sv, copy_file):
    # Reusable long-form renderer for the Bellevue main /our-services/ pages, built from a per-service
    # content file (content/<copy_file>). Reuses the shared section helpers, adds page-scoped custom
    # sections (Why / Our Services / services image gallery / Service Areas) and a page-scoped <style>
    # block, and emits NO JSON-LD schema (the list passed to head() is empty). It does not call
    # _long_service_page, so that shared renderer is untouched for every other page. Section ids are
    # keyed by the record slug so one page-scoped stylesheet (attribute selectors) styles every page.
    meta, sections = _k_parse_copy(copy_file, sv["h1Service"], expected_sections=11 if sv["slug"] == "home-addition" else 10)
    by = {"intro": sections[0], "services": sections[1], "build": sections[2], "process": sections[3],
          "planning": sections[4], "living": sections[5], "signs": sections[6], "why": sections[7],
          "faq": sections[8], "area": sections[9]}
    intro = _k_blocks(by["intro"]["lines"])
    if not intro or intro[0][0] != "paragraph":
        raise SystemExit(copy_file + " introduction must begin with a paragraph")
    hero_lede = _k_inline(intro[0][1])
    page_key = sv["slug"]
    path = _SPU[sv["slug"]]
    service_name = sv["h1Service"]

    # Hero (jump nav removed per request).
    hero = f'''<main id="main" class="long-service-page km">
<section class="page-hero sv-hero" aria-labelledby="{page_key}-h1">
  <div class="wrap page-hero__grid">
    <div><nav class="crumbs" aria-label="Breadcrumb"><a href="{_SPU["overview"]}">Services</a><span aria-hidden="true">/</span><span aria-current="page">{esc(service_name)}</span></nav>
      <h1 id="{page_key}-h1">{esc(meta["H1"])}</h1>
      <p class="lede" style="margin-bottom:30px">{hero_lede}</p>
      <div class="row"><a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a></div>
    </div>
    <figure class="sv-hero__ph rv">{_img(sv["heroPhoto"], "(min-width:901px) 46vw, 92vw", "", True, sv.get("heroFocal"))}</figure>
  </div>
</section>
{brand_strip(_UP, True)}
'''

    svc_blocks = _k_blocks(by["services"]["lines"])
    svc_paras = _km_paras(svc_blocks)

    parts = [hero]
    # ---- First half: Why -> Our Services -> Testimonials -> Gallery ----
    parts.append(_km_feature_section(page_key + "-why", "sec--stone", "km-why", by["why"]["title"],
                 "A local team you can hold accountable, from the first consultation to the final walkthrough.",
                 _km_cards(_km_list_items(_k_blocks(by["why"]["lines"]))), _KM_WHY_ICONS))
    parts.append(_km_feature_section(page_key + "-services", "sec--slab", "km-svc", by["services"]["title"],
                 svc_paras[0] if svc_paras else "",
                 _km_cards(_km_list_items(svc_blocks)), _KM_SVC_ICONS,
                 svc_paras[-1] if len(svc_paras) > 1 else ""))
    # "Remodeling and Building Services": an image gallery of services, like the homepage showcase.
    parts.append(_km_build_section(page_key, by["build"]["title"], _km_paras(_k_blocks(by["build"]["lines"]))[0]))
    parts.append(_reviews())
    # The "Our <service> work" gallery is shown only when the record has real project photos for this
    # service. Services without client-supplied photos skip it (no borrowed or misleading imagery).
    if sv["slug"] not in _KM_NO_GALLERY:
        parts.append(_k_gallery(sv, page_key))
    # ---- Second half: Process -> 3 SEO sections -> Service Areas -> FAQ -> CTA ----
    parts.append(_k_section(by["process"]["title"], page_key + "-process", "sec--stone", _k_blocks(by["process"]["lines"]), "full"))
    parts.append(_k_section(by["planning"]["title"], page_key + "-planning", "sec--slab", _k_blocks(by["planning"]["lines"]), "full"))
    parts.append(_k_section(by["living"]["title"], page_key + "-living", "sec--slab", _k_blocks(by["living"]["lines"]), "full"))
    parts.append(_k_section(by["signs"]["title"], page_key + "-signs", "sec--stone", _k_blocks(by["signs"]["lines"]), "full"))
    # home-addition carries one extra section (sections[10]) targeting the "room additions" keyword.
    if sv["slug"] == "home-addition":
        parts.append(_k_section(sections[10]["title"], page_key + "-rooms", "sec--slab", _k_blocks(sections[10]["lines"]), "full"))
    parts.append(_km_areas_section(page_key, by["area"]["title"], _km_paras(_k_blocks(by["area"]["lines"]))[0]))
    faq_section, faq_pairs = _k_faq(_k_blocks(by["faq"]["lines"]), page_key, by["faq"]["title"], expected_count=8)
    parts.append(faq_section)
    last_photo = sv["gallery"][-1]
    closing_photo = (_img(last_photo, "(min-width:901px) 40vw, 90vw") if last_photo.startswith("asset:")
                     else pimg(_UP, last_photo, "(min-width:901px) 40vw, 90vw", None, False, ""))
    form = lead_block("contact", f"{page_key}-form-h", esc(sv["closingHeading"]), "Send a few details and we will take it from there. We reply within one business day.", _form(sv), closing_photo)
    form = form.replace('<section class="sec sec--slab lead"', '<section class="sec sec--slab lead kitchen-section long-service-form"')
    parts.append(form + "</main>\n" + footer(_UP) + mbar(_UP) + scripts(_UP, False) + "</body>\n</html>\n")

    # Service-page schema policy: Service + FAQPage + BreadcrumbList (no business entity; Service.provider
    # references the homepage LocalBusiness by @id). FAQPage mirrors the visible on-page FAQs (faq_pairs).
    _km_ld = [
        {"@context": "https://schema.org", "@type": "Service", "@id": SITE + path + "#service", "name": sv["h1Service"],
         "serviceType": sv["h1Service"], "description": meta["META DESCRIPTION"], "url": SITE + path,
         "image": _abs_photo(sv["heroPhoto"]), "provider": {"@id": SITE + "/#localbusiness"},
         "areaServed": ["Bellevue, WA", "The Eastside", "Greater Seattle area"]},
        faq_ld([(q, [a]) for q, a in faq_pairs]),
        _crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), (sv["h1Service"], path)]),
    ]
    page = (head(meta["TITLE TAG"], meta["META DESCRIPTION"], path, _UP, photo_preload(_UP, sv["heroPhoto"]) + _KM_CSS, _km_ld)
            + '<body class="long-service-page-body">\n<!-- Main /our-services/ page (' + page_key + '): Service + FAQPage + BreadcrumbList schema. -->\n'
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "services", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    visible_copy = _kr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_kr.S)
    if "WhatsApp" in visible_copy or "wa.me" in visible_copy:
        raise SystemExit(page_key + " page must not include WhatsApp")
    w(_rel_of(_SPU[sv["slug"]]), page)


# Pages that have no real, service-specific client project photos yet: their "Our <service> work"
# gallery is skipped so the page never shows borrowed or misleading imagery. (siding is handled in
# _long_service_page below.)
_KM_NO_GALLERY = {"floor-main", "painting", "basement-remodeling", "attic-remodeling", "home-addition"}

# The main /our-services/ pages, each (record slug, content file). This full long-form design is
# rolled out across all of them. Each record lives in data/service-pages.json or tools/v4-extra-services.json.
_KM_PAGES = [
    ("kitchen-main", "kitchen-main.md"),
    ("bathroom-main", "bathroom-main.md"),
    ("roofing-main", "roofing-main.md"),
    ("floor-main", "floor-main.md"),
    ("deck-building", "deck-building-main.md"),
    ("adu-garage-conversion", "adu-garage-conversion-main.md"),
    ("painting", "painting-main.md"),
    ("basement-remodeling", "basement-remodeling-main.md"),
    ("attic-remodeling", "attic-remodeling-main.md"),
    ("home-addition", "home-addition-main.md"),
]
for _km_slug, _km_copy in _KM_PAGES:
    _km_main_page(next(page for page in _ALL_SP if page["slug"] == _km_slug), _km_copy)
