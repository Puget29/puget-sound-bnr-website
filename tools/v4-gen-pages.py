# Page bodies. Exec'd by v4-gen.py (shares its helpers).
# LANDING (restructured 2026-10-18): hero, who we are, what we build, drawing to doorstep, specialty, why BNR, recent work,
# what clients say, questions, get started (form), footer. About and Contact below are unchanged.

# ---------------------------------------------------------------- Who we are (Option B: pillars, optional proof strip, slim timeline)
# Copy comes from the About page of the previous site, shortened to plain words. Confirm it with the client.
def who_section():
    pillars = [
        ("Close support", "A dedicated project manager oversees every part of your project, and our office team manager is there for any concern that comes up."),
        ("Clear and reliable", "We keep you well informed and involved in every decision, and we price fairly."),
        ("Skilled craftsmen", "A team of highly skilled professionals delivers work that meets the highest standards of quality."),
    ]
    cards = "".join(f'<div class="pillar rv" style="--d:{i * 0.08:.2f}s"><h3 class="h3">{esc(t)}</h3><p>{esc(p)}</p></div>' for i, (t, p) in enumerate(pillars))
    # Years, licence, insurance and the Google rating are shown. The 4.9 rating is sample data until the client gives the real verified rating.
    proof = ('<div class="proof__tile rv"><div class="proof__v">Licensed</div><div class="proof__l">in Washington</div></div>'
             '<div class="proof__tile rv" style="--d:.04s"><div class="proof__v"><span data-count="5" data-suffix="+">5+</span> years</div><div class="proof__l">in business</div></div>'
             '<div class="proof__tile rv" style="--d:.08s"><div class="proof__v">Insured</div><div class="proof__l">and bonded</div></div>'
             '<div class="proof__tile rv" style="--d:.16s"><div class="proof__v">Free</div><div class="proof__l">consultation</div></div>')
    steps = [("call", "Free consultation", "We talk through what you want to change and look at the space with you."),
             ("quote", "Design and quote", "We turn your ideas into a plan, a scope and a price you can read."),
             ("siding", "Build", "We do the work and keep you updated. If something needs to change, we talk it through with you."),
             ("visit", "Walkthrough", "We walk through the finished project with you, room by room.")]
    li = "".join(f'<li class="rv" style="--d:{i * 0.12:.2f}s">{art(a, "tl4__art")}<h4>{n}</h4><p>{esc(t)}</p></li>' for i, (a, n, t) in enumerate(steps))
    return f'''<section class="sec sec--slab" id="who" aria-labelledby="who-h">
  <div class="wrap">
    <div class="whotop">
      <div class="rv">
        <h2 class="h2" id="who-h">Architects of your dream home.</h2>
        <div class="prose" style="margin-top:28px">
          <p>Puget Sound Builders &amp; Renovation is a remodeling company in Bellevue, WA. Our team of designers and craftsmen is dedicated to bringing your vision to life with superior service.</p>
          <p>We specialize in kitchen, bathroom and full-home renovations. We pride ourselves on meticulous planning, craftsmanship and customer satisfaction.</p>
          <a class="link-q" href="{URLS['about']}">Our full story</a>
        </div>
      </div>
      <figure class="pslot rv" data-slot="who-1" data-ratio="3:4" style="--d:.1s"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i></figure>
    </div>
    <div class="pillars">{cards}</div>
    <div class="proof">{proof}</div>
    <div class="how rv"><h3>How a project runs</h3><p>Four steps, from the first conversation to the final walkthrough.</p></div>
    <ol class="tl4 rv" aria-label="How a project runs">{li}</ol>
  </div>
</section>
'''

def faq_section(which="all", up="", h2="Questions we hear a lot."):
    items = faq_items(which)
    return f'''<section class="sec {"sec--slab" if which == "all" else "sec--stone"}" id="faq" aria-labelledby="faq-h">
  <div class="wrap faqgrid">
    <div class="faqhead rv"><h2 class="h2" id="faq-h">{h2}</h2><p class="lede" style="margin-top:20px">Short answers. Your consultation covers the rest.</p></div>
    <div class="faq rv">{faq_html(items)}</div>
  </div>
</section>
''', items

# ================================================================= LANDING ====
def hero():
    return f'''<main id="main">
  <section class="hero" id="top" aria-label="Introduction">
    <div class="hero__stick">
      <video class="hero__video" muted playsinline preload="metadata" width="1920" height="1080" poster="{AS}assets/poster-m.webp" data-poster-d="{AS}assets/poster-desktop-original.jpg" data-src-m="{AS}assets/hero-m.mp4" data-src-d="{AS}assets/hero-desktop-original.mp4" data-seq="{AS}assets/hero-seq.bin" data-seq-index="{AS}assets/hero-seq.json" data-hud="js/perf-hud.js" aria-hidden="true" tabindex="-1" disablepictureinpicture></video>
      <script>/* one rendition per device, decided before any video byte is asked for: wide screens on a good connection get the desktop file and poster, everything else the small ones */(function(){{var v=document.querySelector(".hero__video"),c=navigator.connection||{{}},d=innerWidth>900&&!c.saveData&&!/(^|-)(2g|3g)$/.test(c.effectiveType||"");window.__hero={{d:d}};if(d)v.poster=v.getAttribute("data-poster-d")}})();</script>
      <div class="hero__scrim"></div>
      <div class="hero__copy">
        <h1>From first sketch to finished home.</h1>
        <div class="hero__flip" aria-hidden="true"></div>
        <p class="hero__proof">Bellevue, WA</p>
        <div class="hero__cta">
          <a class="btn btn--primary" href="{CONTACT}" data-book>Book your free consultation{BTN_ARROW}</a>
          <a class="btn btn--explore" href="#who">Explore our craft</a>
        </div>
      </div>
      <a class="hero__cue" href="#who" aria-label="Skip the intro and go to the next section"><span class="hero__cue-bar"><span class="hero__cue-fill"></span></span><span class="hero__cue-label" aria-hidden="true">Skip intro</span></a>
    </div>
  </section>
'''

AS = "" if ROOT else "../"   # shared assets, seen from the landing page
loader_head = '''<link rel="preload" as="image" href="@@AS@@assets/poster-m.webp" type="image/webp" media="(max-width: 900px)" fetchpriority="high">
<link rel="preload" as="image" href="@@AS@@assets/poster-desktop-original.jpg" type="image/jpeg" media="(min-width: 901px)" fetchpriority="high">
<script>/* first frame is the video poster, in the HTML. js-flip lets the headline flip in (not for reduced motion). */(function(){var r=document.documentElement;try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches)r.classList.add("js-flip")}catch(e){r.classList.add("js-flip")}})();</script>
'''
loader_head = loader_head.replace('@@AS@@', AS)
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-hero.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-services.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-adu.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-trust.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-wrf.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-work.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-cta.py'), encoding='utf-8').read())
landing = (head("Kitchen, bathroom and ADU remodeling in Bellevue, WA | Puget Sound Builders & Renovation",
                "General contractor in Bellevue, WA. Kitchen and bathroom remodeling, ADU and DADU construction, decks, siding, flooring and painting for Eastside homes.",
                "/", "", loader_head, [org_ld(), wrf_ld()])
           + "<body>\n<!-- Landing page. -->\n"
           + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("", None, True)
           + hero() + brand_strip("") + who_section() + services_section() + adu_section() + why_section() + work_section() + wrf_reviews_section() + faq3_section() + landing_cta_section() + "</main>\n" + footer("", True) + mbar("")
           + scripts("", True) + "</body>\n</html>\n")
# the sections are inside <main>; the footer sits after it
w("index.html", landing)

# ================================================================= CONTACT ====
def contact():
    sec, items = faq_section("short")
    plats = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in LINKS.items())
    steps = f'''<section class="sec sec--stone" aria-labelledby="nx-h">
  <div class="wrap"><div class="sec__head rv"><h2 class="h2" id="nx-h">What happens next.</h2><p class="lede">Three steps, from your message to a plan.</p></div>
    <ol class="next3">
      <li class="rv">{art("call")}<h3 class="h3">We call you</h3><p>We talk through your project and answer your first questions.</p></li>
      <li class="rv" style="--d:.06s">{art("visit")}<h3 class="h3">We visit and measure</h3><p>We look at the space with you and take the details we need.</p></li>
      <li class="rv" style="--d:.12s">{art("quote")}<h3 class="h3">You get a quote</h3><p>A clear scope and price, ready for you to read.</p><p>Written, before any work starts.</p></li>
    </ol></div>
</section>
'''
    form = f'''{form_open("form form--card rv", "contact-page", "Book your free consultation", "form")}
        {netlify_fields("contact-page", "Free consultation")}
        <h2 class="h3">Book your free consultation</h2><p class="form__sub">We reply within one business day.</p>
        <div class="form__two">
          <div class="fld"><label for="f-name">Name</label><input id="f-name" name="name" type="text" autocomplete="name" data-req aria-describedby="f-name-err"><p class="err" id="f-name-err" role="alert"></p></div>
          <div class="fld"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" data-req data-kind="phone" aria-describedby="f-phone-err"><p class="err" id="f-phone-err" role="alert"></p></div>
        </div>
        <div class="form__two">
          <div class="fld"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" data-req data-kind="email" aria-describedby="f-email-err"><p class="err" id="f-email-err" role="alert"></p></div>
          <div class="fld"><label for="f-zip">ZIP code</label><input id="f-zip" name="zip" type="text" autocomplete="postal-code" inputmode="numeric" data-req data-kind="zip" aria-describedby="f-zip-err"><p class="err" id="f-zip-err" role="alert"></p></div>
        </div>
        <div class="fld"><label for="f-service">Project type</label>
          <select id="f-service" name="service" data-req aria-describedby="f-service-err"><option value="">Choose one</option><option value="kitchen">Kitchen remodeling</option><option value="bathroom">Bathroom remodeling</option><option value="adu">ADU or DADU</option><option value="deck-siding">Deck or siding</option><option value="flooring-painting">Flooring or painting</option><option value="roofing">Roofing</option><option value="other">Not sure</option></select>
          <p class="err" id="f-service-err" role="alert"></p></div>
        <div class="hp" aria-hidden="true"><label>Company<input type="text" name="company" tabindex="-1" autocomplete="off"></label></div>
        <button class="btn btn--primary" type="submit">Book your free consultation{BTN_ARROW}</button>
        <p class="form__fine">We use your details only to reply about your project.</p>
        <p class="form__fail err" tabindex="-1" hidden role="alert">Something went wrong. Please call (425) 696-4004.</p>
        <div class="form__ok" role="status"><strong>Thank you.</strong><span class="form__ok-text"></span></div>
      </form>'''
    side = f'''<aside class="side rv" style="--d:.08s" aria-label="Contact details">
        <div><h2>Call the office</h2><a class="bigtel" href="tel:{PHONE_TEL}">{PHONE_TXT}</a></div>
        <div><h2>Email</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
        <div><h2>Office</h2><p>{ADDR}</p></div>
        <div><h2>Hours</h2><p>Mon to Fri, 8 am to 6 pm</p></div>
        <div><h2>License</h2><p>Licensed, bonded and insured in Washington</p></div>
        <div><h2>Find us online</h2><div class="platforms">{plats}</div></div>
      </aside>'''
    ct_hero = photo_hero("../", "project-47", "60% 55%", "ct-h", '<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Contact</span></nav>', "Let&rsquo;s talk about your project.", f"Send a few details and we will take it from there. Prefer to talk? Call {PHONE_TXT}. We reply within one business day.", f'<a class="btn btn--primary" href="#form">Book your free consultation{BTN_ARROW}</a><a class="btn btn--ghost" href="tel:{PHONE_TEL}">Call {PHONE_TXT}</a>', "short")
    body = f'''<main id="main">
{ct_hero}
{brand_strip("../", True)}
<section class="sec sec--slab" aria-label="Contact form">
  <div class="wrap contact"><div>{form}</div><div class="contact__side">{side}</div></div>
</section>
{steps}{area_section("Where we work.")}{sec}</main>
'''
    return (head("Contact Puget Sound Builders & Renovation | Book your free consultation in Bellevue, WA",
                 "Book your free consultation with Puget Sound Builders & Renovation in Bellevue, WA. Call (425) 696-4004 or send the form.",
                 CONTACT, "../", photo_preload("../", "project-47"), [org_ld(), crumbs_ld("Contact", CONTACT), faq_ld(items)])
            + "<body>\n<!-- Contact page v4. The form is a Netlify Form named lead. js/forms.js posts it. -->\n"
            + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("../", "contact", False)
            + body + footer("../") + mbar("../") + scripts("../", False) + "</body>\n</html>\n")
w("contact/index.html", contact())

def not_found():
    body = f'''<main id="main">
<section class="page-hero page-hero--short" aria-labelledby="nf-h">
  <div class="wrap page-hero__grid"><div>
    <p class="crumbs">404</p>
    <h1 id="nf-h">Page not found.</h1>
    <p class="lede">That address is not on this site. It may have moved, or it may have been typed wrong.</p>
    <div class="row"><a class="btn btn--primary" href="/">Back to the home page{BTN_ARROW}</a><a class="btn btn--ghost" href="{CONTACT}">Contact the office</a></div>
  </div></div>
</section>
</main>
'''
    html = (head("Page not found | Puget Sound Builders & Renovation",
                 "This page is not on the Puget Sound Builders & Renovation website.",
                 "/404.html", "", "")
            + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("", None, False)
            + body + footer("") + mbar("") + scripts("", False) + "</body>\n</html>\n")
    return html.replace('href="../"', 'href="/"')

w("404.html", not_found())

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-privacy.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-svcpages.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-projects.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-about.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-blog.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v4-gen-approved-pages.py'), encoding='utf-8').read())
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'city-gen.py'), encoding='utf-8').read())
