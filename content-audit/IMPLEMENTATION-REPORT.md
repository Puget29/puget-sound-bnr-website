# Location Page Content Improvement — Implementation Report

All 81 `/service-areas/<city>/` pages rewritten with genuinely unique, researched, location-specific content. Build staged to `build/stage` (not deployed). Branch `gs-marketing-optimization`; nothing committed/pushed; the 43 pre-existing working-tree changes preserved.

## A. Summary

- **Pages updated: 81 / 81.** Each now has a unique hero, four substantive SEO sections with city-specific headings, distinct kitchen and bathroom copy, a unique local-homes passage, and six city-specific FAQs — generated from per-city research with recorded sources.
- **New content model:** `data/city-content.json` (per-city), consumed by `tools/city-gen.py` (`_city_page_v2`). Shared **factual** sections (services, reviews, process steps, CTA, maps, schema) are intentionally preserved; only editorial/local content changed.
- **Uniqueness (median across 81): unique-sentence ratio 8% -> 33%; boilerplate 86% -> 55%.**
- **Validation: 81/81 pages fully clean, 0 broken internal links, FAQPage schema matches visible FAQs on every page.**
- **Research flagged for human confirmation:** 79 cities carry one or more `needs_verification` notes (see `RESEARCH-PROVENANCE.md`); these are facts drawn from secondary sources, written qualitatively, never asserted as precise.
- **FAQ-answer de-duplication (completed in the final pass):** after the sample approval, the reused factual FAQ answers (permit/cost/bathroom/kitchen) were localized across the 68 affected cities using each city's already-researched facts. FAQ answers are now **473 / 486 unique (97%%)**, up from 66%%.

## B. Keyword coverage (all 81)

Primary `Home Remodeling in <City>` and secondary `Kitchen and Bathroom Remodeling in <City>` verified on every page:

| Signal | Pages |
|--------|-------|
| Exact primary in H1 (`Home Remodeling in <City>, WA`) | 81 / 81 |
| Primary phrase in hero description | 81 / 81 |
| Primary phrase in >=1 SEO H2 (planning section) | 81 / 81 |
| Secondary phrase as the Kitchen & Bath H2 | 81 / 81 |
| Distinct, substantive kitchen AND bathroom paragraphs | 81 / 81 |
| Links to both dedicated service pages (descriptive anchors) | 81 / 81 |
| Six visible FAQs + matching FAQPage schema | 81 / 81 |

No keyword stuffing introduced; primary phrase appears a handful of times per page in natural context.

## C. Uniqueness analysis (before -> after)

Measured by normalizing city names to a token and comparing sentence frequency across all 81 pages (same method as the original audit).

| Metric (median) | Before | After |
|-----------------|--------|-------|
| Unique-sentence ratio | 7.7% | **32.7%** |
| Boilerplate ratio (shared by >=40 pages) | 86.4% | **54.5%** |
| Hero descriptions unique across 81 | identical template | **81 / 81** |
| Local-homes prose unique across 81 | ~39 words, templated | **81 / 81**, 120-200 words |
| FAQ answers unique (of 486) | ~all identical sitewide | **473 (97%%)** |

After-build per-page unique ratio ranges 23%-44%. Residual boilerplate is the intentionally shared sections (Why-Choose-Us facts, Services carousel, reviews, work rail, Process steps, Service-Areas frame, CTA) plus the FAQ answers noted in A.

## D. Page-by-page quality (all 81)

`Uniq%` = after-build unique-sentence ratio. `KB` = distinct kitchen+bath. `FAQ dup` = how many of this page's 6 FAQ answers are shared with another city (0 is best). `Flags` = needs_verification count.

| # | City | Clean | Uniq% | Body words | KB | FAQ dup | Flags |
|---|------|-------|-------|------------|----|---------|-------|
| 1 | Algona | yes | 39% | 1944 | ok | 0 | 2 |
| 2 | Anacortes | yes | 41% | 1960 | ok | 0 | 2 |
| 3 | Arlington | yes | 39% | 1955 | ok | 0 | 2 |
| 4 | Auburn | yes | 40% | 1962 | ok | 0 | 2 |
| 5 | Bainbridge Island | yes | 42% | 1968 | ok | 0 | 2 |
| 6 | Bellevue | yes | 29% | 1845 | ok | 0 | 2 |
| 7 | Black Diamond | yes | 37% | 2015 | ok | 0 | 2 |
| 8 | Bonney Lake | yes | 37% | 2005 | ok | 0 | 2 |
| 9 | Bothell | yes | 33% | 1972 | ok | 0 | 2 |
| 10 | Bremerton | yes | 35% | 1959 | ok | 0 | 2 |
| 11 | Brier | yes | 31% | 1919 | ok | 0 | 2 |
| 12 | Buckley | yes | 31% | 1875 | ok | 0 | 2 |
| 13 | Burien | yes | 35% | 1883 | ok | 0 | 1 |
| 14 | Carnation | yes | 36% | 1831 | ok | 0 | 2 |
| 15 | Centralia | yes | 36% | 1846 | ok | 0 | 2 |
| 16 | Clyde Hill | yes | 39% | 1895 | ok | 0 | 2 |
| 17 | Covington | yes | 43% | 1886 | ok | 0 | 1 |
| 18 | Des Moines | yes | 38% | 1904 | ok | 0 | 1 |
| 19 | DuPont | yes | 42% | 1862 | ok | 0 | 0 |
| 20 | Duvall | yes | 42% | 1851 | ok | 0 | 0 |
| 21 | Edgewood | yes | 41% | 1909 | ok | 0 | 1 |
| 22 | Edmonds | yes | 30% | 1874 | ok | 0 | 2 |
| 23 | Enumclaw | yes | 30% | 1859 | ok | 0 | 2 |
| 24 | Everett | yes | 30% | 1884 | ok | 0 | 2 |
| 25 | Federal Way | yes | 32% | 1962 | ok | 0 | 2 |
| 26 | Fife | yes | 29% | 1864 | ok | 0 | 2 |
| 27 | Fircrest | yes | 33% | 1902 | ok | 0 | 2 |
| 28 | Gig Harbor | yes | 32% | 1923 | ok | 0 | 2 |
| 29 | Gold Bar | yes | 31% | 1919 | ok | 0 | 2 |
| 30 | Granite Falls | yes | 28% | 1917 | ok | 0 | 2 |
| 31 | Hunts Point | yes | 36% | 1848 | ok | 0 | 2 |
| 32 | Issaquah | yes | 35% | 1961 | ok | 0 | 2 |
| 33 | Kenmore | yes | 26% | 1922 | ok | 1 | 2 |
| 34 | Kent | yes | 33% | 1936 | ok | 0 | 2 |
| 35 | Kirkland | yes | 29% | 1933 | ok | 0 | 1 |
| 36 | Lacey | yes | 31% | 1920 | ok | 1 | 2 |
| 37 | Lake Forest Park | yes | 28% | 1958 | ok | 0 | 2 |
| 38 | Lake Stevens | yes | 23% | 1958 | ok | 0 | 2 |
| 39 | Lakewood | yes | 31% | 1877 | ok | 0 | 2 |
| 40 | Lynnwood | yes | 29% | 1905 | ok | 0 | 2 |
| 41 | Maple Valley | yes | 23% | 1956 | ok | 0 | 2 |
| 42 | Marysville | yes | 24% | 1937 | ok | 0 | 2 |
| 43 | Medina | yes | 34% | 1868 | ok | 0 | 2 |
| 44 | Mercer Island | yes | 29% | 1921 | ok | 0 | 2 |
| 45 | Mill Creek | yes | 30% | 1892 | ok | 1 | 2 |
| 46 | Monroe | yes | 26% | 1897 | ok | 1 | 2 |
| 47 | Mountlake Terrace | yes | 32% | 1933 | ok | 1 | 1 |
| 48 | Mount Vernon | yes | 32% | 1916 | ok | 0 | 1 |
| 49 | Mukilteo | yes | 34% | 1920 | ok | 1 | 2 |
| 50 | Newcastle | yes | 34% | 1935 | ok | 0 | 2 |
| 51 | Normandy Park | yes | 34% | 1955 | ok | 0 | 2 |
| 52 | North Bend | yes | 34% | 1971 | ok | 0 | 2 |
| 53 | Oak Harbor | yes | 33% | 1907 | ok | 0 | 2 |
| 54 | Olympia | yes | 37% | 1874 | ok | 0 | 2 |
| 55 | Orting | yes | 32% | 1862 | ok | 0 | 2 |
| 56 | Pacific | yes | 31% | 1873 | ok | 0 | 2 |
| 57 | Port Orchard | yes | 31% | 1917 | ok | 0 | 2 |
| 58 | Poulsbo | yes | 33% | 1851 | ok | 0 | 3 |
| 59 | Puyallup | yes | 38% | 1874 | ok | 0 | 2 |
| 60 | Redmond | yes | 33% | 1917 | ok | 0 | 2 |
| 61 | Renton | yes | 33% | 1854 | ok | 0 | 3 |
| 62 | Roy | yes | 43% | 1913 | ok | 0 | 2 |
| 63 | Ruston | yes | 42% | 1915 | ok | 0 | 2 |
| 64 | Sammamish | yes | 44% | 1910 | ok | 0 | 2 |
| 65 | SeaTac | yes | 36% | 1905 | ok | 0 | 2 |
| 66 | Seattle | yes | 40% | 1970 | ok | 0 | 2 |
| 67 | Shoreline | yes | 30% | 1872 | ok | 1 | 2 |
| 68 | Snohomish | yes | 32% | 1849 | ok | 0 | 1 |
| 69 | Snoqualmie Pass | yes | 43% | 1862 | ok | 0 | 2 |
| 70 | Snoqualmie | yes | 32% | 1860 | ok | 1 | 2 |
| 71 | Stanwood | yes | 31% | 1889 | ok | 0 | 2 |
| 72 | Steilacoom | yes | 26% | 1905 | ok | 1 | 2 |
| 73 | Sultan | yes | 34% | 1888 | ok | 0 | 2 |
| 74 | Sumner | yes | 26% | 1968 | ok | 1 | 2 |
| 75 | Tacoma | yes | 32% | 1927 | ok | 0 | 2 |
| 76 | Tenino | yes | 31% | 1904 | ok | 0 | 2 |
| 77 | Tukwila | yes | 34% | 1906 | ok | 1 | 2 |
| 78 | Tumwater | yes | 30% | 1855 | ok | 1 | 2 |
| 79 | University Place | yes | 35% | 1871 | ok | 1 | 2 |
| 80 | Woodinville | yes | 38% | 1871 | ok | 0 | 2 |
| 81 | Yarrow Point | yes | 38% | 1890 | ok | 0 | 2 |

## E. Validation

- **Build:** `npm run stage` succeeded; 81 city pages; sitemap 116 URLs (unchanged).
- **Pages fully clean:** 81 / 81 (correct H1, unique hero, primary+secondary coverage, distinct kitchen/bath, all 4 SEO sections + areas + POI present, 6 FAQs, canonical, `index,follow`).
- **Broken internal links:** 0 across all 81 (service-area + service-page targets all resolve).
- **FAQPage schema:** matches the 6 visible FAQs on every page.
- **Preserved / unchanged:** URL structure, canonical tags, `index,follow`, sitemap, Org + breadcrumb + City + FAQPage schema, maps (GBP + directions), review widget, forms, navigation, CSS/JS. No service pages or unrelated sections touched.
- **Build-lock handling:** released by stopping only the specific `http.server` PIDs bound to the preview ports (verified via netstat), never a blanket Python kill.
- **Files modified:** `tools/city-gen.py` (generator consumes the new content; fallback retained); `data/city-content.json` (new, 81 cities). Reports added under `content-audit/`. No other source files changed; the 43 pre-existing working-tree changes are untouched.
- **Visual note:** no in-session browser is available, so layout was verified structurally (markup + CSS classes unchanged, same section order/surfaces). A human spot-check on desktop + mobile is advised.

## F. Remaining recommendations

1. **Human-confirm the `needs_verification` items** in `RESEARCH-PROVENANCE.md` (mostly housing-era shares and neighborhood build-year ranges taken from real-estate/aggregator sources, written qualitatively). Confirm small-city permit administration where a city may contract to its county (e.g., Roy, Snoqualmie Pass).
2. **Optional:** add one city-specific editorial line to the Why-Choose-Us / Service-Areas intros where a verified local angle exists (the model supports `why_intro`/`areas_intro`; used on Bellevue).
