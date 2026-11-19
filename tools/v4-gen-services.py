# Services section: horizontal image carousel (one image per service, name on the image).
# Exec'd by v4-gen-pages.py.

# (name, slug, kicker, description, bullets, icon, link slug for the contact form)
SERVICES = [
    ("Additions: ADU and DADU", "adu", "Room to grow", "Design, permits and construction for ADUs and DADUs, attached or detached.",
     ["Design and permits", "Foundation, framing and finish", "Utilities and landscaping"], "adu", "adu"),
    ("Kitchens", "kitchen", "The heart of the house", "New layouts, cabinets, counters and lighting, planned around how you cook and live.",
     ["Layout and cabinetry", "Counters, backsplash and lighting", "Flooring, paint and finishes"], "kitchen", "kitchen"),
    ("Bathrooms", "bathroom", "Private spaces", "Showers, tubs, vanities and tile, built to last.",
     ["Tile and waterproof membranes", "Showers, tubs and vanities", "Lighting and ventilation"], "bathroom", "bathroom"),
    ("Roofing", "roofing", "Protection from above", "Roofing for Eastside homes, planned and installed by one team.",
     ["New roofs", "Roof replacement", "A clear plan and quote first"], "roofing", "roofing"),
    ("Decks", "deck", "Outdoor living", "New decks and deck rebuilds, built to last.",
     ["Deck framing and decking", "Railings and stairs", "Repairs and replacement"], "deck", "deck-siding"),
    ("Flooring", "flooring", "Under every step", "New floors that fit how you live, planned and installed by one team.",
     ["Floor installation and replacement", "Planned and installed by one team"], "flooring", "flooring-painting"),
    ("Painting", "painting", "Finishing touches", "Fresh paint that finishes the job, planned and done by one team.",
     ["Interior painting", "Exterior painting"], "painting", "flooring-painting"),
    ("Siding", "siding", "First line of defense", "Siding installed or replaced, with the details done right.",
     ["Replacement and new installation", "Repairs and trim", "Weather barriers and flashing"], "siding", "deck-siding"),
]

# "More we do": the rest of the client's service list. One line per chip. A chip links to the contact form option of the same slug when it exists, otherwise to "other"
# (the contact form has: kitchen, bathroom, adu, deck-siding, flooring-painting, roofing, other). Icons are small 24 px line drawings.
CONTACT_OPTIONS = {"kitchen", "bathroom", "adu", "deck-siding", "flooring-painting", "roofing", "other"}
MORE_SERVICES = [
    ("Fencing and gates", "fencing", '<path d="M5 20V8l2-2 2 2v12M11 20V8l2-2 2 2v12M17 20V8l2-2 2 2v12M3 12h18M3 17h18"/>'),
    ("Framing and drywall", "framing", '<path d="M4 20V4h16v16zM4 12h16M12 4v16M8 4v8M16 12v8"/>'),
    ("Plumbing", "plumbing", '<path d="M4 8h9a3 3 0 0 1 3 3v9M4 8V5M16 14h4M18 20v-2M12 8V5"/>'),
    ("Electrical", "electrical", '<path d="M13 3L5 13h6l-1 8 8-10h-6z"/>'),
    ("Landscaping", "landscaping", '<path d="M12 21v-8M12 13c-4 0-6-3-6-7 4 0 6 3 6 7zM12 15c3 0 5-2 5-5-3 0-5 2-5 5zM4 21h16"/>'),
    ("Insulation", "insulation", '<path d="M3 8h18v8H3zM6 8v8M9 8v8M12 8v8M15 8v8M18 8v8"/>'),
    ("General construction", "general", '<path d="M4 20h16M6 20V10l6-5 6 5v10M10 20v-6h4v6"/>'),
]

def more_html(c):
    out = ""
    for i, (name, slug, ico) in enumerate(MORE_SERVICES):
        form = slug if slug in CONTACT_OPTIONS else "other"
        out += (f'<li class="more__li rv" style="--d:{min(i * 0.05, 0.4):.2f}s"><a class="more__a" href="{c}" data-svc="{slug}">'
                f'<svg class="more__ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ico}</svg>'
                f'<span>{esc(name)}</span></a></li>')
    return out


def services_section():
    c = CONTACT
    n = len(SERVICES)
    items = ""
    for i, (name, slug, kick, desc, bullets, icon, form) in enumerate(SERVICES):
        href = {"adu": URLS["servicePages"]["adu-garage-conversion"], "kitchen": URLS["servicePages"]["kitchen-main"], "bathroom": URLS["servicePages"]["bathroom-main"],
                "roofing": URLS["servicePages"]["roofing-main"], "deck": URLS["servicePages"]["deck-building"], "siding": URLS["servicePages"]["siding"],
                "flooring": URLS["servicePages"]["floor-main"], "painting": URLS["servicePages"]["painting"]}.get(slug, URLS["services"])
        bl = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        items += f'''<div class="car__item" role="group" aria-roledescription="slide" aria-label="{esc(name)}, {i + 1} of {n}" data-svc="{slug}" data-page="/services/{slug}/" style="--tone:{i}">
        <a class="car__card" href="{href}">
          <figure class="pslot" data-slot="svc-{slug}" data-ratio="4:5"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i><span class="pslot__ico">{art(icon)}</span></figure>
          <span class="car__scrim" aria-hidden="true"></span>
          <span class="car__ico" aria-hidden="true">{art(icon)}</span>
          <span class="car__cap"><span class="car__k">{esc(kick)}</span><h3 class="car__h">{esc(name)}</h3><span class="car__d">{esc(desc)}</span><span class="car__view" aria-hidden="true">View{ARROW}</span></span>
          <span class="car__ov"><span class="car__ovh" aria-hidden="true">{esc(name)}</span><span class="car__ovd">{esc(desc)}</span><ul class="car__b">{bl}</ul><span class="car__go">View service{ARROW}</span></span>
        </a>
      </div>
      '''
    chev_l = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    chev_r = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M8 4l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'''<section class="sec sec--stone" id="services" aria-labelledby="svc-h">
  <div class="wrap">
    <div class="sec__head rv"><h2 class="h2" id="svc-h">What we build for Eastside homes.</h2>
    <p class="lede">Pick what you have in mind and book a free consultation. We build across Bellevue and the Eastside, from kitchens and bathrooms to ADU and DADU additions.</p></div>
  </div>
  <div class="car" role="region" aria-roledescription="carousel" aria-label="Our services">
    <button class="car__btn car__prev" type="button" aria-label="Previous service">{chev_l}</button>
    <div class="car__stage">
      <div class="car__track">
      {items}</div>
    </div>
    <button class="car__btn car__next" type="button" aria-label="Next service">{chev_r}</button>
    <div class="car__meta"><span class="car__bar" aria-hidden="true"><span class="car__fill"></span></span></div>
    <p class="car__live" aria-live="polite" aria-atomic="true"></p>
  </div>
  <div class="wrap more">
    <p class="more__l">More we do</p>
    <ul class="more__ul">{more_html(c)}</ul>
  </div>
</section>
'''
