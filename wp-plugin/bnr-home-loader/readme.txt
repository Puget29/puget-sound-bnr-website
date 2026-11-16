=== BNR Home Loader ===
Contributors: bnr
Tags: static, home page
Requires at least: 5.8
Tested up to: 6.6
Requires PHP: 7.4
Stable tag: 2.2.0
License: GPLv2 or later

Serves the static BNR home page from the plugin folder.

== Description ==

* Every built page has a hidden preview: /home-new/ (home), /home-new/about/, /home-new/contact/, /home-new/privacy/, /home-new/our-services/ and /home-new/our-services/<service>/ for the eight service pages. HTTP 200, header X-Robots-Tag: noindex, nofollow, and a noindex meta tag. Links inside stay in the preview.
* A page takes over its real WordPress address only when it is named in BNR_LIVE_PAGES (for example array( 'about', 'contact' ); names: home, about, contact, services, kitchen, bathroom, roofing, deck, adu, siding, flooring, painting) at the top of bnr-home-loader.php. BNR_HOME_LIVE true also makes Home live. Both default to off.
* Everything else on the site is untouched: wp-admin, wp-json, feeds, previews, the Elementor editor and every other page.
* A live page is served only for the plain address. Tracking parameters (utm_*, gclid, fbclid and similar) and service are fine. Any other query string, for example ?bnr-old=1, goes to WordPress, so the old version can always be viewed with ?bnr-old=1.
* If a page file in pages/ is missing the plugin does nothing for that page.
* Cache-Control: public, max-age=300. After a switch change, clear WP Rocket.

The page files (css, js, images, video) live in the folder bnr-home-assets in the site root, not in this plugin.

== Changelog ==

= 2.2.0 =
Projects page (name projects, address /remodeling-projects/, exact path only).

= 2.1.0 =
Services overview and five service pages (nested addresses), each with its own preview and live switch.

= 2.0.0 =
Preview of every built page and a per page live list.

= 1.0.0 =
First version.
