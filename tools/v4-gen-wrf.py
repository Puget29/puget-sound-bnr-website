# Three landing sections: Why homeowners hire BNR (#why), What clients say (#reviews), Questions homeowners ask (#faq).
# Exec'd by v4-gen-pages.py (shares esc, art, ARROW, BTN_ARROW, LINKS, PHONE_TXT, PHONE_TEL).
# No reviews, ratings, counts, licence or insurance claims are written here. No numbering anywhere.

WRF_FAQ = [
    ("How do I get started?", "Book a free consultation. We talk through your project and plan the next steps together."),
    ("Where do you work?", "We are based in Bellevue, WA and work on homes across the Eastside."),
    ("What kinds of projects do you take on?", "ADUs and DADUs, kitchens, bathrooms, roofing, decks and outdoor living, flooring, painting and siding. We also do fencing and gates, framing and drywall, plumbing, electrical, landscaping, insulation and general construction."),
    ("Do you do roofing?", "Yes, roofing is one of our services. Book a free consultation and we will talk through your roof and the next steps."),
    ("Do you build ADUs and DADUs?", "Yes. We handle ADU and DADU design, permits and construction. Rules are different in every city, so ask us what applies to your lot."),
    ("How much will my project cost?", "Every home and every project is different. After the free consultation we put together a quote for your project."),
    ("How long will it take?", "It depends on the size and type of project. We talk through the schedule with you as part of the plan."),
]
# shown only after the client supplies the answers
WRF_FAQ_EXTRA = [("Are you licensed and insured?", "Yes. We are licensed in Washington, fully insured and bonded.")]   # shown on the page, not added to the FAQ JSON-LD (kept as is)

def _svg(vb, body, extra=""):
    return f'<svg class="art why__art" viewBox="{vb}" aria-hidden="true" focusable="false">{body}</svg>{extra}'

# three line drawings, one 4:3 box (320 x 240), one stroke width (the .art rule keeps it at 1.6 px on screen)
WHY_ART1 = _svg("0 0 320 240",
    '<path d="M50 206 H270"/><circle cx="50" cy="206" r="7"/><circle cx="160" cy="206" r="7"/><circle cx="270" cy="206" r="7"/>'
    '<path d="M160 64 L240 104 L160 144 L80 104 Z"/><path d="M80 104 V154 L160 194"/><path d="M240 104 V154 L160 194"/><path d="M160 144 V194"/>'
    '<path d="M160 24 L240 64 L160 104 L80 64 Z" stroke-dasharray="3 6"/><path d="M80 64 V104 M240 64 V104 M160 104 V144" stroke-dasharray="3 6"/>'
    '<path d="M104 128 V158 M128 140 V170 M192 140 V170 M216 128 V158"/>'
    '<text x="50" y="232" text-anchor="middle">Plan</text><text x="160" y="232" text-anchor="middle">Build</text><text x="270" y="232" text-anchor="middle">Walkthrough</text>',
    '<svg class="why__dot" viewBox="0 0 320 240" style="--dx:220px" aria-hidden="true" focusable="false"><circle cx="50" cy="206" r="4"/></svg>')
WHY_ART2 = _svg("0 0 320 240",
    '<path d="M160 188 L272 150 L160 112 L48 150 Z"/><path d="M80 140 V100 L128 84 V124"/><path d="M128 84 L214 112 V148"/><path d="M214 112 L252 100 V134"/><path d="M80 100 L48 110"/>'
    '<path d="M48 210 H272 M48 202 V218 M272 202 V218"/><path d="M296 150 V188 M290 150 H302 M290 188 H302"/>')
WHY_ART3 = _svg("0 0 320 240",
    '<path d="M70 200 H250"/><path d="M110 200 V110 A50 50 0 0 1 210 110 V200"/><path d="M136 200 V116 A24 24 0 0 1 184 116 V200"/><path d="M146 156 L160 170 L186 138"/>')

def why_section():
    ps = [
        ("One team from first sketch to walkthrough", "The people who plan your project are the people who build it. You deal with one team at every step.", WHY_ART1),
        ("A plan you understand before work starts", "We go through the plan with you first, so you know what is being built and why.", WHY_ART2),
        ("A walkthrough at the end", "When the work is done we go through it with you together, room by room.", WHY_ART3),
    ]
    out = ""
    for i, (t, txt, art_svg) in enumerate(ps):
        out += (f'<article class="why__p why__p--{i + 1} rv" data-spot style="--i:{i}"><div class="why__art-w">{art_svg}</div>'
                f'<h3 class="h3">{esc(t)}</h3><p>{esc(txt)}</p></article>\n      ')
    return f'''<!-- Intended final order of the landing sections: hero, who, services, adu, trust, why, work, reviews, faq, contact. Move the why, reviews and faq blocks when "From drawing to doorstep", Recent work and the contact form are added. -->
<section class="sec sec--dark why" id="why" aria-labelledby="why-h" data-fx="stagger draw glow spot">
  <div class="wrap">
    <div class="why__head rv"><h2 class="h2" id="why-h">Why homeowners hire BNR</h2><p class="lede">Three reasons, in plain words.</p></div>
    <div class="why__grid">
      {out}</div>
  </div>
</section>
'''

def wrf_reviews_section(also=True, head="What clients say", sub="In their own words.", extra=""):
    pills = ""
    LINKS_ALL = dict(LINKS, Google=_TJ["google"]["url"])
    for name, key in (("Google", "Google"), ("Yelp", "Yelp"), ("Angi", "Angi")):   # profile links already used in the trust strip (LINKS), nothing new. A platform without a URL gets no pill.
        if LINKS_ALL.get(key):
            pills += f'<a class="rvw__b" href="{esc(LINKS_ALL[key])}" target="_blank" rel="noopener noreferrer" aria-label="Read our reviews on {name} (opens in a new tab)"><span>{name}</span>{ARROW}</a>'
    chev_l = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="M12 4l-6 6 6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    chev_r = '<svg viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false"><path d="M8 4l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    return f'''<section class="sec sec--card rvw" id="reviews" aria-labelledby="rv-h" data-fx="stagger morph glow spot">
  <div class="wrap rvw__w">
    <div class="rvw__head">
      <h2 class="h2 rv" id="rv-h">{head}</h2>
      <p class="lede rv" style="--d:.08s">{sub}</p>
    </div>
    <div class="rvw__stage rv" style="--d:.12s">
      <div class="rvw__deck" role="region" aria-roledescription="carousel" aria-label="Client reviews" tabindex="0" data-spot></div>
      <div class="rvw__ctl">
        <button class="rvw__nav rvw__prev" type="button" aria-label="Previous review">{chev_l}</button>
        <div class="rvw__dots" role="group" aria-label="Choose a review"></div>
        <button class="rvw__nav rvw__next" type="button" aria-label="Next review">{chev_r}</button>
      </div>
      <p class="rvw__live" aria-live="polite" aria-atomic="true"></p>
    </div>
    {('<div class="rvw__also rv" style="--d:.2s"><span class="rvw__al">Also on</span>' + pills + '</div>') if also else ''}{extra}
  </div>
</section>
'''

def faq3_section():
    rows = ""
    for i, (q, a) in enumerate(WRF_FAQ):
        op = " open" if i == 0 else ""
        rows += (f'<details class="fq__row rv" name="faq" style="--i:{i}"{op}><summary><span class="fq__q">{esc(q)}</span><span class="fq__ico" aria-hidden="true"></span></summary>'
                 f'<div class="fq__a"><p>{esc(a)}</p></div></details>\n        ')
    for q, a2 in WRF_FAQ_EXTRA:
        rows += (f'<details class="fq__row rv" name="faq" style="--i:{len(WRF_FAQ)}"><summary><span class="fq__q">{esc(q)}</span><span class="fq__ico" aria-hidden="true"></span></summary>'
                 f'<div class="fq__a"><p>{esc(a2)}</p></div></details>')
    return f'''<section class="sec fq" id="faq" aria-labelledby="fq-h" data-fx="stagger spot">
  <span class="fq__glow" aria-hidden="true"></span>
  <div class="wrap fq__grid">
    <div class="fq__side">
      <h2 class="h2 rv" id="fq-h">Questions homeowners ask</h2>
      <p class="lede rv" style="--d:.08s">Short answers. Ask us anything else at your free consultation.</p>
      <div class="fq__card rv" style="--d:.16s"><h3 class="h3">Still have a question?</h3><a class="fq__tel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a><a class="fq__book" href="{CONTACT}" data-book><span>Book a free consultation</span>{ARROW}</a></div>
    </div>
    <div class="fq__list" data-spot>
        {rows}</div>
  </div>
</section>
'''

def wrf_ld():
    return faq_ld([(q, [a]) for q, a in WRF_FAQ])
