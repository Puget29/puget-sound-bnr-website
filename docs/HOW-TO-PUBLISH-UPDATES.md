# How to publish website updates

For the marketing manager. You need WordPress admin access and access to the hosting provider's file manager or SFTP. You do not need to write code. How the files are built is in [README.md](../README.md); this guide starts from the finished zip files in the folder `dist-live-home-zips/`.

Steps marked **To confirm** depend on the hosting panel or on settings that cannot be read from this repository. Check them once with the hosting provider and write the answer next to the step.

## 1. Before you publish

1. Take a fresh full backup with UpdraftPlus: Settings, UpdraftPlus Backups, Backup Now, tick both files and database, then Backup Now. Wait until it shows as finished and keep the backup until the new pages have been live for a few days.
2. Know the two things that sit in front of the site:
   - **WP Rocket** caches pages. After every change you must clear its cache (section 4).
   - **Wordfence** is the firewall. If it blocks an upload or a test form, look at Wordfence, All Options or Firewall, Blocking, and at Tools, Live Traffic for the blocked request. **To confirm:** whether Wordfence needs the lead form address `/wp-json/bnr/v1/lead` or the plugin upload allowed.

## 2. Upload the asset zips and install the plugins

Files to use from `dist-live-home-zips/`: `bnr-home-assets-video.zip`, `bnr-home-assets-1.zip`, `bnr-home-assets-2.zip`, `bnr-home-loader.zip` and `bnr-lead-handler.zip`. A file starting with `patch-` is a small update that holds only the files that changed since the last build. Use the patch for later updates (see below).

**Asset zips (images, video, CSS, JavaScript).** They must be unpacked into the site's web root, the folder that contains `wp-content` and `wp-admin`. They create the folder `bnr-home-assets/`.
- **To confirm:** how to do this on the hosting panel. What must happen: upload each asset zip into the web root, extract it there so that `bnr-home-assets` appears next to `wp-content`, and allow overwriting if asked. Use the provider's file manager or SFTP. Then delete the zips from the web root.
- Check: open `https://www.pugetsoundbnr.com/bnr-home-assets/css/site.min.css` in a browser. CSS text should appear.

**Plugins.** In WordPress admin:
1. Plugins, Add New Plugin, Upload Plugin, Choose File, select `bnr-home-loader.zip`, Install Now, then Activate Plugin. If an older version is installed, WordPress offers to replace it. Accept.
2. Repeat with `bnr-lead-handler.zip`.
3. Both plugins start safe. Nothing changes on the real addresses until you turn pages on (section 3).

**Previews.** After the upload every built page can be opened at a hidden address that search engines ignore and that carries no tracking:
`/home-new/`, `/home-new/about/`, `/home-new/contact/`, `/home-new/privacy/`, `/home-new/remodeling-projects/`, `/home-new/our-services/`, `/home-new/our-services/<service>/` (kitchen-remodeling, bathroom-remodeling, roofing, deck-building, adu-garage-conversion, siding, flooring, painting), `/home-new/blog/` and `/home-new/blog/<post-slug>/`. Review everything here first.

**Later updates.** Upload the `patch-<date>.zip` the same way as an asset zip (it holds web root paths, including the plugin's `pages/` folder, so it is extracted into the web root and overwrites). Then clear the cache (section 4).

## 3. Turning pages on, one at a time

Two settings at the top of the file `wp-content/plugins/bnr-home-loader/bnr-home-loader.php` decide what is live:

- `BNR_LIVE_PAGES` is a list of page names. A page in the list is served at its real address. It ships empty: `array()`.
- `BNR_HOME_LIVE` is `false` or `true`. `true` serves the new Home page at `/`, the same as adding `'home'` to the list.

Page names: `home`, `about`, `contact`, `services`, `projects`, `kitchen`, `bathroom`, `roofing`, `deck`, `adu`, `siding`, `flooring`, `painting`, `blog`, and one `blog-<post-slug>` per Blog post. `privacy` has a preview only and never replaces an address.

Example with two pages on: `define( 'BNR_LIVE_PAGES', array( 'about', 'contact' ) );`

How to edit it: **To confirm** which editor is available. Options are the Plugins, Plugin File Editor screen (it may be disabled for security), the hosting file manager, or SFTP. Change only the text inside `array()`, keep the quotes and commas, and save.

One page at a time:
1. Add one name, save, clear the WP Rocket cache (section 4).
2. Open the page's real address in a private window and run the checklist in section 4. The real addresses are listed in `tools/v4-links.json` (for example `/about/`, `/contact-us/`, `/remodeling-projects/`, `/kitchen-remodel-seattle/`).
3. Only when the page is correct, add the next name.
4. Check the address collisions in section 6 before adding `siding` or any Blog post.

A page that goes live takes over an address that may already exist in WordPress (for example the kitchen, bathroom, roofing, siding and flooring pages and the Blog posts). The old WordPress page is not deleted, it is just hidden while the new one is on. Pages with a new address (deck, ADU, painting) need no replacement. **To confirm:** whether WordPress already has pages at the three `/our-services/` addresses (deck-building, adu-garage-conversion, painting). If it does, they will be hidden when turned on.

When a page is live, its search engine tags and Google Tag Manager and Google Ads tags (from `data/tracking.json`) are included. Previews never have them.

## 4. After each change

1. Clear WP Rocket: in the admin bar choose WP Rocket, Clear cache, or go to Settings, WP Rocket, Dashboard, Clear and preload cache. If the host or a CDN adds its own cache, clear that too (**To confirm** what the host uses).
2. Checklist, in a private window:
   - The page loads at the real address with no error and the right content.
   - It looks right on a phone and on a desktop screen: header, buttons, photos, forms, footer.
   - Links in the menu and the footer open the right pages.
   - Fill in the contact form with a test lead (use your own name, a real email, a 5 digit zip code, wait a few seconds before sending). A success message must appear. Within a few minutes an email arrives at the lead address with the line "New lead from the website". Also check Tools, BNR leads in WordPress: the attempt shows as "sent".
   - No error message on the page and no broken images.
3. The form allows 5 attempts per visitor every 10 minutes. If a test is refused, wait 10 minutes.

## 5. If something goes wrong

**Turn the new pages off.** In the plugins folder (`wp-content/plugins/`, through the hosting file manager or SFTP, **To confirm** which) rename the folder `bnr-home-loader` to `bnr-home-loader-off`. WordPress deactivates the plugin, every address returns to the previous WordPress pages, and the hidden previews stop working. Clear the WP Rocket cache afterwards. To turn it back on, rename the folder back and activate the plugin in Plugins.

A gentler alternative is to remove the page name from `BNR_LIVE_PAGES` and clear the cache. That switches off one page and leaves the rest.

**See the old page while a new one is live.** Add `?bnr-old=1` to the address, for example `https://www.pugetsoundbnr.com/?bnr-old=1`. The plugin ignores addresses with that extra text, so WordPress shows its own previous page. It is for comparing only; visitors do not use it.

If the site is broken in a way you cannot undo, restore the UpdraftPlus backup taken in section 1.

## 6. Address collisions

Read from `tools/v4-links.json` (page addresses) and `data/blog/posts.json` (Blog post addresses):

| Address | Used by | What happens |
| --- | --- | --- |
| `/siding-replacement/` | The Siding service page (`siding`) and the Blog post "Siding Replacement" (`blog-siding-replacement`) | One address, two pages. |

No other page shares an address with another page or with a Blog post. The Flooring address `/flooring-replacement-in-seattle/` is different from every post. The `privacy` page has a preview only, because its real address `/ppc-assets/privacy/` is an existing static file that the plugin does not replace.

What the plugin does with the siding collision:
- If only one of the two names is in `BNR_LIVE_PAGES`, that page is served at `/siding-replacement/`.
- If both are listed, the plugin serves `siding` (the first in its page table) and the Blog post is never shown at that address.
- Previews do not collide: the service page is `/home-new/our-services/siding/` and the post is `/home-new/blog/siding-replacement/`.
- Links to the Blog post from the Blog index point to `/siding-replacement/` when live, so they show whichever of the two is on.

Decide before turning on `siding` or `blog-siding-replacement`:
1. Which page should own `/siding-replacement/`. The recommendation is the Siding service page.
2. A new address for the other page (for example the Blog post moved under `/blog/`), and a redirect from the old address if it has search traffic. **To confirm** who sets up the redirect and with which tool.
3. The Blog post's links from the Blog pages must then be updated to the new address (a change in `data/blog/posts.json` followed by a new build).

Turning on the other seven Blog posts and the Blog index (`/blog/`) is safe from collisions, but each replaces the existing WordPress post at the same address.

## 7. Lead emails

The lead form posts to `/wp-json/bnr/v1/lead`. The handler plugin builds the email and WordPress sends it through the WP Mail SMTP plugin. The recipient is set in `bnr-lead-handler.php` (`BNR_LEAD_TO`, currently Leads@pugetsoundbnr.com). The subject reads "New lead: <service> from <city or page>" and the first line says "New lead from the website" for forms on these pages.

**Sender address.** Mail that is sent from an address on a different domain than the site can land in Spam. In WP Mail SMTP, Settings, set the From Email to an address on the site's own domain (for example an address at pugetsoundbnr.com), tick Force From Email, and make sure the mailer is connected and sending. Use WP Mail SMTP, Tools, Email Test to check delivery. **To confirm:** which mailer is configured and whether the sending domain has SPF and DKIM records set up (the host or the DNS provider can say).

**First test lead.**
1. Send one test lead from the live Contact page (section 4).
2. Look in the Inbox. If it is not there, open Spam.
3. If it is in Spam, open it and click Not spam (Report not spam).
4. In Gmail create a filter so these emails are never sent to Spam: open the email, click the three dots, Filter messages like these, check that the From address matches, Create filter, tick Never send it to Spam, and optionally Apply the label and Mark as important, then Create filter.
5. Send a second test to confirm it reaches the Inbox.

If there is no email at all, open Tools, BNR leads. "sent" means WordPress handed the email to the mail system, so check WP Mail SMTP, Email Log (if enabled) next. Anything else in the Note column, such as "invalid zip" or "rate limit", explains why the form did not send.
