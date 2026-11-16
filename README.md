# Puget Sound BNR website

Source for the Puget Sound BNR website (pugetsoundbnr.com). The site is a set of static pages that are generated from page copy, data files and a few templates, then served on the company's WordPress site by a small plugin. The repository holds the generators, the page copy, the images, the scripts that bundle the CSS and JavaScript, and the two WordPress plugins.

Pages built: Home, About, Contact, Privacy, Projects, the Services overview, eight service pages (Kitchen, Bathroom, Roofing, Deck, ADU and garage conversion, Siding, Flooring, Painting) and the Blog with its 12 posts.

## Requirements

- Node.js 20 or newer (built and tested with Node 24)
- Python 3.10 or newer, standard library only (no packages to install)

## Folder map

| Folder | What it holds |
| --- | --- |
| `content/` | Page copy in Markdown, one file per page (`kitchen.md`, `about.md`, `home-text.md` and so on). Edit the words here. |
| `data/` | Structured data: project photo list, reviews, trust logos, tracking ids, service records, and `data/blog/` with the Blog posts. |
| `site/` | Front end sources: `css/`, `js/`, `v4/css/v4.css`, `v4/js/`, `vendor/` (GSAP), and `assets/` (images, fonts, logos, hero video files). |
| `tools/` | Page generators (`v4-gen*.py`), the link map (`v4-links.json`) and the WordPress build script (`home-live.py`). |
| `scripts/` | `stage.mjs` (full site build), `build-assets.mjs` (CSS and JS bundles), `version-assets.mjs` (cache hashes), `serve-home-live.mjs` (local preview server). |
| `wp-plugin/bnr-home-loader/` | Plugin that serves the built pages on WordPress. |
| `wp-plugin/bnr-lead-handler/` | Plugin that receives the contact and quote forms and emails each lead. |

## Build

```
npm install
npm run build
```

`npm run build` runs `python tools/home-live.py`. That script first runs `npm run stage` (`node scripts/stage.mjs`: bundle the CSS and JS, generate every page, add cache hashes, lay the files out in `build/stage/`), then writes:

- `dist-live-home/`: the web root tree (`bnr-home-assets/` plus `wp-content/plugins/bnr-home-loader/`)
- `dist-live-home-zips/`: ready to upload zips, each under 25 MB: `bnr-home-assets-video.zip`, `bnr-home-assets-1.zip`, `bnr-home-assets-2.zip`, `bnr-home-loader.zip` (the page plugin) and `bnr-lead-handler.zip` (the form plugin). Later builds also write a small `patch-<timestamp>.zip` with only the files that changed.

If `python` is not the right command on your machine, set `PYTHON=python3` for the stage step and run `python3 tools/home-live.py`.

Preview the build locally:

```
npm run preview
```

Then open `http://127.0.0.1:8830/home-new/` (Home) or `http://127.0.0.1:8830/home-new/our-services/kitchen-remodeling/` (Kitchen). Every page has a preview address under `/home-new/`. The preview server also stands in for the lead handler, so forms work locally and write to `build/lead-log.jsonl`. To use another port: `node scripts/serve-home-live.mjs 8831`.

## Editing

- Page words: edit the file in `content/` and rebuild. Each file keeps its `TITLE TAG`, `META DESCRIPTION` and `H1` lines at the top (Home has no H1), then a fixed number of `##` sections. The build stops with a clear message if a file does not match what the generator expects.
- Home page text (`content/home-text.md`) has seven blocks. They sit below the hero and the brand strip, in this order: Introduction (directly below the strip), Services (merged into the services area), How we work, Why homeowners choose us (near the reviews), Service area (after the reviews), FAQs (above the contact form), Closing call to action. The hero, its heading, the strip and the banner are not part of this file.
- Project photos: add the optimized WebP files to `site/assets/projects/` and list them in `data/projects.json`. The photos shown first (Projects page and the Home "last jobs" row) are the ids in `data/last-jobs.json`.
- Links and page addresses: `tools/v4-links.json`.
- Tracking (Google Tag Manager and Google Ads): `data/tracking.json`. Tags are added to the live pages only, never to the previews.

## How the site goes live

1. Extract the asset zips into the WordPress web root (the folder that contains `wp-content`). They create `bnr-home-assets/`.
2. Install `bnr-home-loader.zip` (Plugins, Add New, Upload Plugin) and activate it. Install and activate `bnr-lead-handler.zip` the same way, so the forms can send leads. The recipient address is the `BNR_LEAD_TO` line at the top of `bnr-lead-handler.php`.
3. Every built page is now available as a hidden preview (noindex, no tracking) under `/home-new/`.
4. A page takes over its real address only when its name is listed in `BNR_LIVE_PAGES` at the top of `bnr-home-loader.php`, for example `array( 'about', 'contact' )`. Names: `home`, `about`, `contact`, `services`, `projects`, `kitchen`, `bathroom`, `roofing`, `deck`, `adu`, `siding`, `flooring`, `painting`, `blog` and one `blog-<post-slug>` per post. The list ships empty, so nothing goes live until it is set. Privacy has a preview only.
5. After changing the list, clear the site cache. Adding `?bnr-old=1` to an address shows the previous WordPress version of that page.

## What the plugins serve

`bnr-home-loader` serves only the pages built from this repository, from its own `pages/` folder:

- Previews (always on, noindex, no tracking): `/home-new/`, `/home-new/about/`, `/home-new/contact/`, `/home-new/privacy/`, `/home-new/remodeling-projects/`, `/home-new/our-services/`, `/home-new/our-services/<service>/` for the eight services, `/home-new/blog/` and `/home-new/blog/<post-slug>/` for each of the 12 posts.
- Real addresses (index, tracking tags included, Google Tag Manager and Google Ads from `data/tracking.json`): only for pages named in `BNR_LIVE_PAGES`, or Home when `BNR_HOME_LIVE` is `true`. Both ship off (`false` and `array()`), so no real address changes until they are set.
- Everything else on the site (wp-admin, wp-json, other pages) is left to WordPress.

`bnr-lead-handler` provides the REST endpoint `POST /wp-json/bnr/v1/lead` used by every form, plus the Tools, BNR leads log. Lead emails say "New lead from the website" when the form sends a `source` value (all forms built here do) and "New lead from the PPC landing page" otherwise.

The Google Ads landing pages (city and service pages, `/ppc-assets/`) are separate static folders in the web root. They are not served by either plugin and are not part of this repository, so installing or replacing the plugins does not affect them.
