# Executive Summary

## Verdict

All 81 location pages are **technically well-built and keyword-perfect, but content-thin and nearly
identical to one another.** Every page nails the on-page SEO fundamentals — exact primary keyword in
the H1, hero, and an SEO H2; kitchen and bathroom service links; six FAQs; valid canonical, `index,follow`,
and full schema. But a single structural fact dominates the entire audit:

> **~86% of every page is shared boilerplate.** After normalizing the city name to a token, the median
> page shares **74 substantial sentences verbatim with 70+ of the other 80 pages**, and only **~7
> sentences per page are genuinely unique** (the local landmarks and one short local-prose paragraph).
> The median page has a **unique-sentence ratio of just 8%** (range 4–15%).

This is because all 81 pages are produced by one template (`tools/city-gen.py` → `_city_page_v2`) in which
only `{city}` is substituted into otherwise-fixed copy. The genuinely unique content per page is confined
to five data fields — and two of those (the permit bullet and the permit FAQ) are themselves near-identical
templates. The real differentiated prose is roughly **130–150 words out of ~1,640 per page.**

## Scores at a glance

| Metric | Value |
|--------|-------|
| Pages audited | 81 / 81 |
| Average score | **67.9 / 100** |
| Median score | 68 / 100 |
| Range | 63 (Covington) – 76 (Bellevue) |
| Excellent (90–100) | 0 |
| Good (80–89) | 0 |
| **Needs improvement (70–79)** | **12** |
| **Weak (60–69)** | **69** |
| Poor (<60) | 0 |
| Pages with serious *accuracy/relevance* errors | 0 |

No page is broken, misleading, or mis-targeted — so nothing is "Poor." But no page clears 80 either,
because the uniqueness, SEO-depth, and FAQ dimensions are capped sitewide by the shared template.

## What is genuinely working (all 81 pages)

1. **Primary keyword targeting — excellent.** Exact `Home Remodeling in <City>, WA` in H1, hero, and a
   planning H2; ~3× in body; natural, no stuffing. This is the strongest dimension.
2. **Correct intent framing.** Every page is unmistakably about home remodeling for homeowners in its city,
   with kitchen and bathroom called out as sub-topics and linked to their dedicated service pages.
3. **Technical SEO is clean.** Unique (city-stamped) titles and meta descriptions, canonical, `index,follow`,
   breadcrumb + `HomeAndConstructionBusiness` + `FAQPage` schema, two maps, consistent heading hierarchy.
4. **No fabrication.** No invented prices, timelines, or guarantees (the cost FAQ deliberately declines to
   quote). Reviews are the shared real set. POIs spot-check as accurate (see `06`).
5. **Local landmarks are a real asset.** 3–5 researched, specific, verifiable POIs per city plus 5–8
   relevant nearby-community links — the best-differentiated part of each page.

## The core problems (ranked)

1. **[CRITICAL — sitewide] Near-duplicate pages at scale.** 86% boilerplate across 81 pages is a classic
   doorway/thin-content pattern. Google may index few of them, fold them together, or discount the set.
   This is the single issue most likely to hold back the whole location-page strategy.
2. **[HIGH — sitewide] Only one of four "SEO sections" is unique, and it's the thinnest** (median 43 words;
   `Remodeling Homes in <City>`). The Planning and Kitchen-&-Bath sections are 100% generic.
3. **[HIGH — sitewide] Secondary keywords are present but shallow and templated** — one shared 116-word
   section covers both kitchen and bathroom identically on all 81 pages.
4. **[HIGH — sitewide] FAQs are ~5 of 6 generic.** FAQ 2's question is identical on all 81 pages; FAQs 3–6
   never change. Effectively <1 of 6 FAQs is local.
5. **[MEDIUM — sitewide] "Unique" data fields are half-boilerplate.** The permit bullet (75/81 identical),
   the ADU bullet (3 templates), and both local FAQs are city-swapped templates, not local content.
6. **[MEDIUM] Meta descriptions and the on-page local prose are thin/templated;** no blog or deep
   cross-service internal links from the body.

## Cannibalization

**Low risk, with one caveat.** The 81 pages target distinct geographic keywords, so they do not cannibalize
*each other* in the normal sense, and they correctly defer to the dedicated kitchen/bathroom service pages
(linking out rather than competing). The real risk is not keyword cannibalization but **duplicate-content
dilution**: 81 near-identical pages competing for Google's attention as a *set*. See `08`.

## Bottom line for the client's questions

- **Is every page targeting `Home Remodeling in <City>`?** Yes — perfectly, on all 81.
- **Are kitchen & bathroom covered as secondary topics?** Yes, but thinly and identically everywhere.
- **Does every page have enough useful, substantive content?** Structurally yes; *substantively no* — the
  unique, city-specific content is ~130–150 words per page.
- **Are the four SEO sections genuinely helpful and distinct?** Two are generic, one is half-generic, one is
  unique but very short.
- **Are the pages meaningfully unique?** **No** — they are ~86% the same page with a different city name.
- **Is the local information relevant and accurate?** Yes — POIs and nearby lists are the strongest, most
  trustworthy differentiator (spot-verified accurate).
- **Are FAQs useful and location-specific?** Useful yes; location-specific mostly no.
- **Cannibalization risk?** Low between pages; the concern is duplicate-content dilution of the set.
- **Strongest pages:** Bellevue (76), Anacortes, Auburn, Bainbridge Island, Black Diamond (70–71) — those
  with the longest, most place-named local prose and 5 POIs.
- **Weakest / fix first:** the 69 "Weak" pages, led by those with <40-word local prose and/or boilerplate
  local bullets — Covington (63), and the cluster at 65 (Medina, Olympia, Roy, Steilacoom, and others).
  See `09` for the fix order.

The single highest-leverage move is **not** per-page keyword tweaking (keywords are already excellent) — it
is **raising the volume and uniqueness of genuinely local content** so each page stops being a city-name
variant of the same template. Specifics in `09-prioritized-plan.md`.
