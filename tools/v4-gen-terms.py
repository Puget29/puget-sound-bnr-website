# Terms & Conditions page. Exec'd by v4-gen-pages.py (shares its helpers). Plain informational text; no schema.

def terms():
    updated = "Last updated: November 23, 2026"
    items = [
        ("Introduction", "Welcome to Puget Sound Builders & Renovation (\"we\", \"our\" or \"us\"). These Terms and Conditions govern your use of our website at pugetsoundbnr.com. By accessing or using this site, you agree to these terms. If you do not agree, please do not use the site."),
        ("Use of the website", "You agree to use this website only for lawful purposes and in a way that does not infringe the rights of others or restrict their use of the site."),
        ("Intellectual property", "All content on this website, including text, images, logos and design, is owned by Puget Sound Builders & Renovation unless otherwise stated. You may not reproduce, distribute or reuse it without our permission."),
        ("Information you submit", "If you send us information through a form on this site, you are responsible for the accuracy of what you provide. We may decline or remove any content we consider inappropriate or unlawful."),
        ("Links to other websites", "Our site may link to third-party websites, such as our profiles on other platforms or an embedded map. We are not responsible for the content or practices of those sites, and you visit them at your own risk."),
        ("Limitation of liability", "This website and its content are provided on an \"as is\" basis. To the extent permitted by law, we are not liable for any direct, indirect or incidental damages arising from your use of, or inability to use, this site."),
        ("Changes to these terms", "We may update these terms from time to time. Continued use of the site after changes are posted means you accept the updated terms."),
        ("Governing law", "These terms are governed by the laws of the State of Washington, United States."),
        ("Contact", f"Questions about these terms? Contact Puget Sound Builders & Renovation at {EMAIL} or {PHONE_TXT}, 11170 NE 10th St, Bellevue, WA 98004."),
    ]
    prose = f"<p><em>{esc(updated)}</em></p>" + "".join(f"<h2>{esc(h)}</h2><p>{esc(t)}</p>" for h, t in items)
    body = (
        '<main id="main">\n<section class="page-hero page-hero--short" aria-labelledby="tc-h">\n  <div class="wrap page-hero__grid"><div>\n'
        '    <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Terms &amp; Conditions</span></nav>\n'
        '    <h1 id="tc-h">Terms &amp; Conditions.</h1>\n    <p class="lede">The terms for using this website.</p>\n  </div></div>\n</section>\n'
        '<section class="sec sec--slab"><div class="wrap"><div class="prose prose--doc rv">' + prose + '</div></div></section></main>\n'
    )
    return (head("Terms & Conditions | Puget Sound Builders & Renovation",
                 "Read the terms and conditions for using the Puget Sound Builders & Renovation website, including acceptable use, intellectual property and governing law.",
                 "/terms-and-conditions/", "../", "", [])  # Other page: no schema
            + "<body>\n" + '<a class="skip" href="#main">Skip to content</a>\n' + banner() + header("../", None, False)
            + body + footer("../") + mbar("../") + scripts("../", False) + "</body>\n</html>\n")

w("terms-and-conditions/index.html", terms())
