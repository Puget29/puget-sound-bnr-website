# Keyword Coverage Report

Exact-match counts measured against the rendered `<main>` text of each page. Because every page is produced by one template (`tools/city-gen.py` -> `_city_page_v2`), the counts are **identical on all 81 pages** except for the city token. The table below therefore reports the single shared profile, then flags the few per-page variations.

## Primary keyword: `Home Remodeling in <City>`

| Placement | Present | Occurrences | Evidence |
|-----------|---------|-------------|----------|
| H1 | 81 / 81 | 1 | `<h1>Home Remodeling in <City>, WA</h1>` |
| Hero description | 81 / 81 | 1 | `Home remodeling in <City> that plans kitchens, bathrooms and whole home updates...` |
| SEO content H2 | 81 / 81 | 1 | `Home Remodeling in <City>: Planning Your Project and Priorities` |
| Body total (exact phrase) | 81 / 81 | **3** | H1 + hero + planning H2 |
| `home remodeling` (any) | 81 / 81 | 6 | plus generic 'home remodeling project/services' mentions |
| `home renovation in <City>` | 81 / 81 | 1 | intro to the 'Before a Home Renovation' section |

**Assessment:** Primary-keyword placement is textbook and complete on every page (exact match in H1, hero, one SEO H2, ~3x in body). This is the strongest dimension sitewide. The weakness is that it is *mechanical and identical* everywhere, so it adds no differentiation. No keyword stuffing was detected (density is low and natural).

## Secondary keywords: `Kitchen Remodeling in <City>` / `Bathroom Remodeling in <City>`

| Signal | Present | Occurrences | Notes |
|--------|---------|-------------|-------|
| `kitchen remodeling in <City>` exact | 81 / 81 | 1 | single bullet in the Kitchen & Bath SEO section |
| `bathroom remodeling in <City>` exact | 81 / 81 | 2 | KB bullet + FAQ |
| `kitchen remodeling` (any) | 81 / 81 | 3 | KB section + FAQ + nav |
| `bathroom remodeling` (any) | 81 / 81 | 5 | |
| Dedicated H2 | 81 / 81 | 1 | `Kitchen and Bathroom Remodeling for <City> Homes` |
| Link to `/our-services/kitchen-remodeling/` | 81 / 81 | yes | descriptive anchor 'kitchen remodeling' |
| Link to `/our-services/bathroom-remodeling/` | 81 / 81 | yes | descriptive anchor 'bathroom remodeling' |

**Assessment:** Both secondary topics are *present and balanced* (one shared ~116-word section covering both, a contextual link each, and a combined FAQ). But coverage is **thin and 100% templated** — the exact same sentences on all 81 pages with only the city swapped. It satisfies the minimum but offers no city-specific kitchen/bathroom substance. Scored **Partial** on every page.

## City mentions

`<City>` appears a median of **39 times** per page (range 35-50). This is high but mostly from mechanical template substitution rather than meaningful local context — a density that borders on over-insertion given how little of it carries unique information.

