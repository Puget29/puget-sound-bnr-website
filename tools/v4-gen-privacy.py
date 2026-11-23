# Privacy page. Exec'd by v4-gen-pages.py (shares its helpers). The text is SAMPLE wording: have it checked before launch.

def privacy():
    updated = "Last updated: November 23, 2026"
    items = [
        ("Who we are", "This website, pugetsoundbnr.com, is operated by Puget Sound Builders & Renovation - Kitchen & Bathroom, a general contractor based at 11170 NE 10th St, Bellevue, WA 98004. This policy explains what information we collect through this website and how we use it."),
        ("What we collect and why", "When you submit a form on this site, we collect the details you enter: your name, phone number, email address, ZIP code and a description of your project. We also receive basic information about how you reached us, such as the page you arrived from and the search or ad that referred you. We use these details only to respond to your inquiry and to plan your project with you. We do not use them for marketing without your consent."),
        ("Contact forms", "Form submissions on this site are processed through Netlify, our website host and forms provider, which delivers your message to our office. A hidden anti-spam field helps us filter out automated submissions."),
        ("Cookies and tracking", "This site uses Google Tag Manager and Google Ads, which may set cookies and collect information such as your device type, approximate location and the pages you view, so we can measure website visits and the performance of our advertising. You can control cookies through your browser settings."),
        ("Embedded content", "Some pages include an embedded Google Map. Google may collect data and set cookies through that embed, the same as if you visited Google directly."),
        ("Who we share data with", "We share information only with the providers that help us run this site and respond to you: Netlify (website hosting and form delivery) and Google (Tag Manager, Google Ads and Maps). We do not sell or rent your personal information."),
        ("How long we keep it", "We keep the details you send us for as long as we need them to answer your inquiry and keep reasonable business records, and then we delete them."),
        ("Your rights and choices", f"You can ask us to show, correct or delete the information you sent us, subject to any records we must keep for legal or security reasons. Call {PHONE_TXT} or email {EMAIL}."),
        ("Contact", f"For any privacy question, contact Puget Sound Builders & Renovation at {EMAIL} or {PHONE_TXT}, 11170 NE 10th St, Bellevue, WA 98004."),
    ]
    prose = f"<p><em>{esc(updated)}</em></p>" + "".join(f"<h2>{esc(h)}</h2><p>{esc(t)}</p>" for h, t in items)
    body = (
        '<main id="main">\n<section class="page-hero page-hero--short" aria-labelledby="pv-h">\n  <div class="wrap page-hero__grid"><div>\n'
        '    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Privacy policy</span></nav>\n'
        '    <h1 id="pv-h">Privacy policy.</h1>\n    <p class="lede">How we handle the details you send us.</p>\n  </div></div>\n</section>\n'
        '<section class="sec sec--slab"><div class="wrap"><div class="prose prose--doc rv">' + prose + '</div></div></section></main>\n'
    )
    return (head("Privacy Policy | Puget Sound Builders & Renovation",
                 "Read the privacy policy for Puget Sound Builders & Renovation: what details we collect when you contact us, how we use them and how we keep them safe.",
                 "/privacy/", "../", "", [])  # Other page: no schema
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
