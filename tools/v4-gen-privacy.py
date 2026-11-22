# Privacy page. Exec'd by v4-gen-pages.py (shares its helpers). The text is SAMPLE wording: have it checked before launch.

def privacy():
    items = [
        ("What we collect", "When you use a form on this site we collect what you type: your name, phone number, email address, ZIP code, a description of your project and, if you add them, photos of your space."),
        ("How we use it", "We use these details to reply to your request and to plan your project with you. We do not sell your details."),
        ("Who sees it", "The BNR office team sees your message. We share details only with the people who need them to do the work you asked for, or when the law requires it."),
        ("How long we keep it", "We keep your details for as long as we need them to answer you and to work on your project, then we delete them."),
        ("Cookies and tracking", "This site does not set tracking cookies."),
        ("Your choices", f"You can ask us to show, correct or delete the details you sent. Call {PHONE_TXT} or write to {EMAIL}."),
    ]
    prose = "".join(f"<h2>{esc(h)}</h2><p>{esc(t)}</p>" for h, t in items)
    body = (
        '<main id="main">\n<section class="page-hero page-hero--short" aria-labelledby="pv-h">\n  <div class="wrap page-hero__grid"><div>\n'
        '    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Privacy policy</span></nav>\n'
        '    <h1 id="pv-h">Privacy policy.</h1>\n    <p class="lede">How we handle the details you send us.</p>\n  </div></div>\n</section>\n'
        '<section class="sec sec--slab"><div class="wrap"><div class="prose prose--doc rv">' + prose + '</div></div></section></main>\n'
    )
    return (head("Privacy policy | Puget Sound Builders & Renovation",
                 "How Puget Sound Builders & Renovation handles the details you send through this website.",
                 "/privacy/", "../", "", [crumbs_ld("Privacy policy", "/privacy/")])
            + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("../", "privacy", False)
            + body + footer("../") + mbar("../") + scripts("../", False) + "</body>\n</html>\n")

w("privacy/index.html", privacy())


# Thank you page: where the forms land without JavaScript. Always noindex, also in the production build.
def thank_you():
    body = (
        '<main id="main">\n<section class="page-hero page-hero--short" aria-labelledby="ty-h">\n  <div class="wrap page-hero__grid"><div>\n'
        '    <h1 id="ty-h">Thank you.</h1>\n    <p class="lede">We have your details. Someone from the office will get back to you within one business day.</p>\n'
        f'    <p class="lede">Need us sooner? Call <a href="tel:{PHONE_TEL}">{PHONE_TXT}</a>.</p>\n'
        '    <p><a class="btn btn--primary" href="../">Back to the home page</a></p>\n  </div></div>\n</section></main>\n'
    )
    return (head("Thank you | Puget Sound Builders & Renovation", "Thank you for contacting Puget Sound Builders & Renovation. We will be in touch shortly.",
                 "/thank-you/", "../", "", [], None, '<meta name="robots" content="noindex, follow">')
            + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("../", "thank-you", False)
            + body + footer("../") + mbar("../") + scripts("../", False) + "</body>\n</html>\n")

w("thank-you/index.html", thank_you())
