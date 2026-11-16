# ADU and DADU band on the Home page. Exec'd by v4-gen-pages.py (shares esc, ARROW, BTN_ARROW, URLS, CONTACT, AS).
# One photo backed band (the earlier use case chooser with tabs is no longer part of the page):
# a real ADU job photo, the existing headline and line, the existing note about city rules, a button to the ADU service page.
# No prices, counts, timelines or city rules. Photo is a real job photo (data/projects.json, stock false), alt text empty (decoration behind the text).
_ADU_PHOTO = ("project-58", "50% 38%")

def adu_section():
    pid, pos = _ADU_PHOTO
    adu_url = URLS["servicePages"]["adu-garage-conversion"]
    return f'''<!-- Section order: hero, brand strip, #who, #services, #adu (photo band), #why, #work, #reviews, #faq, #contact. -->
<section class="sec adu" id="adu" aria-labelledby="adu-h">
  <picture class="adu__bg" aria-hidden="true">
    <source media="(max-width: 900px)" srcset="{AS}assets/projects/{pid}-960.webp">
    <img src="{AS}assets/projects/{pid}-1440.webp" width="1440" height="1920" alt="" loading="lazy" decoding="async" style="object-position:{pos}">
  </picture>
  <div class="adu__ov" aria-hidden="true"></div>
  <div class="wrap">
    <div class="adu__band">
      <h2 class="h2 rv" id="adu-h">Extra space, planned around your lot.</h2>
      <p class="lede rv" style="--d:.08s">A backyard cottage, a DADU or an ADU inside your home. Tell us how you want to use it and we plan the space around that.</p>
      <p class="adu__note rv" style="--d:.14s">ADU rules are different in every city. Ask us what applies to your lot.</p>
      <div class="row adu__row rv" style="--d:.2s"><a class="btn btn--primary" href="{adu_url}">See ADU and garage conversion{BTN_ARROW}</a><a class="btn btn--ghost" href="{CONTACT}" data-book>Plan my ADU</a></div>
    </div>
  </div>
</section>
'''
