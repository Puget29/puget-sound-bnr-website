# Minimal closing consultation section. Exec'd by v4-gen-pages.py.
# Dark site theme; the form stays on the Contact page.
def landing_cta_section():
    return f'''<section class="sec sec--dark cq" id="contact" aria-labelledby="cta-h">
  <div class="wrap cq__inner">
    <h2 class="h2 cq__h rv" id="cta-h">Let's talk about your project.</h2>
    <div class="cq__actions rv">
      <a class="btn btn--primary" href="{CONTACT}">Book your free consultation{BTN_ARROW}</a>
      <a class="cq__phone" href="tel:{PHONE_TEL}">Or call {PHONE_TXT}</a>
    </div>
  </div>
</section>
'''
