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
    if label == "Call (425) 696-4004" or label == "call (425) 696-4004":
        href = "tel:" + PHONE_TEL
        kind = "ghost"
        arrow = False
    href = href or "#form"
    icon = BTN_ARROW if arrow and kind == "primary" else ""
    return f'<a class="btn btn--{kind}" href="{esc(href)}">{esc(label)}{icon}</a>'

_KCTA = r"\[(Book your free consultation|Call \(425\) 696-4004|Get your free estimate)\]"
_KCOMBO = _kr.compile(r"\[(Book your free consultation|Get your free estimate)\] or call \(425\) 696-4004")

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
        chunks.append(_k_cta_row([combo.group(1), "call (425) 696-4004"], "or"))
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

    ld = [org_ld(), _crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), ("Kitchen Remodeling", path)]),
          {"@context": "https://schema.org", "@type": "Service", "name": "Kitchen Remodeling",
           "provider": {"@type": "HomeAndConstructionBusiness", "name": "Puget Sound Builders & Renovation", "telephone": PHONE_TEL},
           "areaServed": [{"@type": "City", "name": "Seattle"}, {"@type": "City", "name": "Bellevue"}], "url": SITE + path},
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
    ld = [org_ld(), _crumb_ld([("Home", "/"), ("Services", _SPU["overview"]), (service_name, path)]),
          {"@context": "https://schema.org", "@type": "Service", "name": service_schema_name,
           "provider": {"@type": "HomeAndConstructionBusiness", "name": "Puget Sound Builders & Renovation", "telephone": PHONE_TEL},
           "areaServed": [{"@type": "City", "name": "Seattle"}, {"@type": "City", "name": "Bellevue"}], "url": SITE + path},
          faq_ld([(q, [a]) for q, a in faq_pairs])]
    page = (head(meta["TITLE TAG"], meta["META DESCRIPTION"], path, _UP, photo_preload(_UP, sv["heroPhoto"]), ld)
            + f'<body class="long-service-page-body">\n<!-- {esc(service_name)} page generated from its approved copy file. -->\n'
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header(_UP, "services", False) + "".join(parts))
    page = page.replace('href="../"', f'href="{_UP}"')
    visible_copy = _kr.sub(r'<article class="sv-rev.*?</article>', "", page, flags=_kr.S)
    if "WhatsApp" in visible_copy or "wa.me" in visible_copy:
        raise SystemExit(service_name + " page must not include WhatsApp")
    w(_rel_of(_SPU[sv['slug']]), page)

_long_only = _os.environ.get("V4_LONG_SERVICE", "").strip().lower()
if _long_only not in ("", "bathroom", "roofing", "deck", "adu", "siding", "flooring", "painting"):
    raise SystemExit("V4_LONG_SERVICE must name a supported long service page")
if _long_only in ("", "bathroom"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "bathroom-remodeling"),
                       "bathroom.md", "bathroom", ["project-15", "project-18"])
if _long_only in ("", "roofing"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "roofing"),
                       "roofing.md", "roofing", ["project-29", "project-61"])
if _long_only in ("", "deck"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "deck-building"),
                       "deck.md", "deck building", ["project-43", "project-44"])
if _long_only in ("", "adu"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "adu-garage-conversion"),
                       "adu.md", "ADU and garage conversion", ["project-58", "project-59"])
if _long_only in ("", "siding"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "siding"),
                       "siding.md", "siding", ["project-14", "project-14"])
if _long_only in ("", "flooring"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "flooring"),
                       "flooring.md", "flooring", ["project-12", "project-12"])
if _long_only in ("", "painting"):
    _long_service_page(next(page for page in _ALL_SP if page["slug"] == "painting"),
                       "painting.md", "painting", ["asset:painting-card", "asset:painting-card"])
