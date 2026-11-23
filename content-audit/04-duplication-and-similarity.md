# Duplication & Similarity Report

This is the most important section of the audit. All 81 pages were compared against one another, not
reviewed in isolation.

## Method

Rendered `<main>` text was split into sentences (≥6 words). In each sentence the page's own city name,
its nearby-city names, and "Bellevue" were replaced with a `CITY` token, so that a templated sentence
written for two different cities becomes identical and collides. Sentence frequency was then counted
across all 81 pages.

## Headline numbers

| Measure | Value |
|---------|-------|
| Distinct (city-normalized) sentences across all 81 pages | 645 |
| Sentences appearing on **≥70 of 81 pages** | **74** |
| Sentences appearing on exactly **1** page | 538 (≈6.6 per page) |
| Median **unique-sentence ratio** per page | **8%** (range 4–15%) |
| Median **boilerplate ratio** (sentences shared by ≥40 pages) | **86%** |
| Unique sentences per page | median 7 (range 4–14) |

Interpretation: the 74 near-universal sentences make up the **bulk of each page's text volume** (the Why,
Services, Planning, Kitchen-&-Bath, Process, reviews, areas, CTA and FAQs 3–6). The ~7 unique sentences per
page are the POIs and the single `local_body` paragraph. So each page is **~86% identical** to the others.

## Exact-duplication evidence (verbatim on all 81 pages, city aside)

Representative sentences that render identically on **81/81** pages:

- *"We work through each of these with you during planning so there are no surprises later."*
- *"Local and accountable — A general contractor serving CITY and the surrounding communities, licensed in Washington, fully insured and bonded."*
- *"Planned scope — We agree on the work and the materials before we begin, so your CITY project stays predictable."*
- *"Think about the whole home — A single update is often the moment to plan related work…"*
- *"We come to you, there is no office to visit in CITY."*
- *"We review the finished work with you and confirm every detail before we call it done."*
- *"See our kitchen remodeling page for the full scope."*
- *"What We Build and Renovate — Pick what you have in mind and book a free consultation."*

Entire **sections** are duplicated verbatim across all 81 pages:

| Section | Duplication |
|---------|-------------|
| Why `<City>` Homeowners Choose Puget Sound BNR (5 cards) | 100% identical (3 cards city-stamped) |
| What We Build and Renovate (services carousel) | 100% identical |
| Planning Your Project and Priorities (4 cards) | 100% identical (heading + 1 card city-stamped) |
| What clients say (review deck) | 100% identical |
| Check our last jobs (gallery) | 100% identical |
| A Clear Remodeling Process… (4 steps) | 100% identical (step 1 city-stamped) |
| Kitchen and Bathroom Remodeling for `<City>` Homes | 100% identical |
| FAQs 3–6 | 100% identical |
| Form / CTA | 100% identical |

## Near-duplication evidence (the "unique" fields are half-templated)

Even the five per-city data fields are substantially boilerplate:

| Field | Distinct templates (city-normalized) | Verdict |
|-------|--------------------------------------|---------|
| `local_bullets[0]` — Permits | **4 of 81** (75 share one) | Boilerplate |
| `local_bullets[1]` — home age / climate | 3 of 81 | Boilerplate pool |
| `local_bullets[2]` — local access/variety | **78 of 81** | Genuinely varied ✅ |
| `local_bullets[3]` — ADUs | 3 of 81 | Boilerplate pool |
| `faq_local[0]` question / answer | 2 / ~11 templates | Near-boilerplate |
| `faq_local[1]` question / answer | **1** / 3 templates | Boilerplate (identical Q on all 81) |
| `local_body` prose | **81 of 81** | Genuinely unique ✅ (but 32–77 words) |
| POI names + descriptions | unique per city | Genuinely unique ✅ (3–5 per page) |

So the genuinely distinct content per page = `local_body` (median 39 words) + one local bullet (~25 words)
+ 3–5 POI blurbs (~70 words) ≈ **130–150 words of ~1,640**.

## Most repetitive page pairs

Because the template is shared, *every* pair of pages is ~86% identical; there is no single "worst pair" —
the duplication is uniform and sitewide. Pairs that share even their *local* content (same nearby cluster,
same boilerplate bullets, similar short `local_body`) include the small Points/Eastside cities whose local
prose is briefest, e.g. Medina ↔ Clyde Hill ↔ Yarrow Point ↔ Hunts Point, and the south-King cluster
Algona ↔ Pacific ↔ Edgewood ↔ Milton. These differ almost only in POIs and city name.

## What is *legitimately* shared (not a defect)

Shared business facts are expected and fine: company name, phone, license/insured/bonded status, the
4-step process, the service list, the real review set, "we come to you / no local office," and the
consultation CTA. The problem is **not** that these are shared — it is that **almost nothing else is not.**

## Risk

81 pages that are 86% identical is the canonical thin/doorway-content pattern. Likely consequences:
Google indexes a subset, treats the rest as duplicates, or discounts the cluster's quality signals. The
pages are honest and useful at the *business* level, but at the *page* level they do not yet earn 81
separate rankings. Remedy in `09`.
