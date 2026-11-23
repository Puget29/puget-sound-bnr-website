# Puget Sound BNR — Location Page Content Audit

Read-only content audit of all **81** `/service-areas/<city>/` location pages.
Date: 2026-11-22 · Branch: `gs-marketing-optimization` · Scope: on-page content + repository data.

## This is an audit, not an implementation

No website source files were modified. No content was rewritten, no templates, CSS, JS, metadata,
or schema were touched, and nothing was staged, committed, pushed, or deployed. The only files
created are the reports in this `content-audit/` folder (new, untracked — safe to delete). Pre-existing
uncommitted work on the branch was recorded before starting and left untouched.

## What was audited

The **rendered HTML** in `build/stage/service-areas/<slug>/index.html` (what visitors and search engines
receive), cross-referenced with the source of truth:
`tools/city-gen.py` (`_city_page_v2` renderer), `data/city-facts.json`, `data/city-local.json`,
`data/city-list.json`.

## Read the reports in this order

| File | Contents |
|------|----------|
| `00-executive-summary.md` | Headline findings, score distribution, the one structural issue that dominates |
| `01-master-scorecard.md` / `.csv` | All 81 pages scored /100 with status columns |
| `02-keyword-coverage.md` | Primary + secondary exact-match coverage |
| `03-seo-sections.md` | The four SEO sections: which are unique, which are generic |
| `04-duplication-and-similarity.md` | Sitewide duplication analysis with evidence |
| `05-secondary-keywords.md` | Kitchen / bathroom coverage and balance |
| `06-local-relevance.md` | POIs, nearby communities, geographic accuracy (with spot-verification) |
| `07-faq-report.md` | FAQ count, quality, duplication |
| `08-cannibalization.md` | Page-vs-page and page-vs-service-page overlap risk |
| `09-prioritized-plan.md` | Critical / High / Medium / Low recommendations (sitewide vs per-page) |
| `10-page-by-page.md` | Findings for each of the 81 pages |

## Methodology & honest limits

- **Programmatic extraction** (Python, stdlib): exact keyword counts against rendered `<main>` text,
  heading extraction, FAQ parsing, internal-link extraction, word counts, and **sentence-level
  cross-page similarity** (city names normalized to a token so templated sentences collide, then
  frequency-counted across all 81 pages). Scripts: `audit_extract.py`, `audit_score.py`, `audit_reports.py`
  in the session scratchpad.
- **Manual review** of the renderer and the per-city data fields.
- **Local-fact spot-verification** via web search on a sample of POIs (results in `06`).
- **Not available / not invented:** no Google Search Console, ranking, traffic, impression, conversion,
  search-volume, or keyword-difficulty data was used or fabricated. This audit evaluates on-page content
  and repository data only — not live ranking performance or search demand. Where a local claim could not
  be independently confirmed it is labelled **Needs verification**, not asserted false.
