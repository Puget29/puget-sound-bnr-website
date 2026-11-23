# Prioritized Improvement Plan

Recommendations only — **no changes were made.** Grouped by priority, and split into **sitewide patterns**
(fix once in the template/data strategy, applies to all 81) vs **per-page** work. Each item says *what*
topic/section to improve and *why*, not just "add content."

---

## CRITICAL (fix first — they cap the whole strategy)

### CR-1 · [Sitewide] Break the 86% duplication — raise genuine per-city content to a meaningful share
**What:** The template produces ~1,640-word pages with only ~130–150 unique words. Shift the ratio so each
page carries **meaningfully more city-specific substance** than boilerplate. Concretely, the per-city data
needs to grow where it is thinnest:
- Expand `local_body` from a median of 39 words to a **substantive 120–200-word** passage that names real
  neighborhoods/districts, typical housing stock, and a local remodeling consideration — the way Bellevue
  and Seattle already begin to.
- Make at least **two of the four `local_bullets` genuinely city-specific** (today only bullet 3 reliably is).
- Add **one city-specific kitchen OR bathroom consideration** tied to the local housing stock (also helps
  secondary intent — see HIGH-2).

**Why:** 81 pages that are 86% identical read as thin/doorway content; Google may index a subset or discount
the cluster. This is the one issue most likely to suppress location-page performance. Everything else is
secondary to it.

### CR-2 · [Per-page] Fix the thinnest pages first
**What:** Prioritize the pages whose only unique content is a <40-word `local_body` **and** boilerplate
bullets — they are the most exposed as thin duplicates. From the scorecard, start with the 60–65 band:
Covington (63); the 65s (Medina, Olympia, Roy, Steilacoom, and peers); then the rest of the "Weak" 69.
**Why:** highest duplication risk and lowest current differentiation — biggest marginal gain per edit.

---

## HIGH (materially improve quality / coverage)

### H-1 · [Sitewide] Make 2 of the 4 "SEO sections" city-specific
**What:** Today only `Remodeling Homes in <City>` is unique (and it's the shortest). The *Planning* and
*Kitchen-&-Bath* sections are 100% generic. Give each a short city-specific lead sentence (local housing
stock, permit jurisdiction specifics that actually differ, common local project types) instead of a
city-swapped template.
**Why:** three of four "substantive" sections currently add no differentiation; search engines and readers
get one unique section out of four.

### H-2 · [Sitewide] Deepen secondary (kitchen/bathroom) coverage with local specificity
**What:** Keep the dedicated-page links (they're good). Extend the kitchen and bathroom bullets with **one
locally-grounded clause each** (e.g. "older <City> homes often need the kitchen layout opened up…").
**Why:** secondary coverage is Partial and identical on all 81; this converts a generic mention into useful,
differentiated secondary-intent content without competing with the service pages.

### H-3 · [Sitewide] De-duplicate the FAQs
**What:** FAQ 2's question is identical on all 81 pages and FAQs 3–6 never change. Replace 2–3 of the generic
FAQs with **city-specific questions** drawn from local facts (housing age, climate exposure, a named
neighborhood, local permit nuance). Keep the safe cost FAQ.
**Why:** effectively <1 of 6 FAQs is local; FAQPage schema is duplicated across the set too.

### H-4 · [Sitewide] Replace the templated permit bullet & permit FAQ with real local nuance, or cut them
**What:** The "City of `<City>`" permit bullet (75/81 identical) and the permit FAQ (identical question on
all 81) imply local specificity they don't deliver. Either populate them with jurisdiction-specific detail
or drop them in favor of genuinely local content.
**Why:** they inflate word count and city-name density without adding unique value — the opposite of what the
duplication problem needs.

---

## MEDIUM (quality, not page-defining)

### M-1 · [Sitewide] Differentiate meta descriptions beyond the city token
Current meta descriptions are one template with the city swapped. Vary structure / lead with a local hook so
SERP snippets aren't near-identical across the set.

### M-2 · [Sitewide] Add body internal links to related **location** pages and relevant blog posts
The nearby-cities block links to neighbors (good), but the **body prose** links only to kitchen/bathroom
service pages. Add contextual links from the local prose to 1–2 nearby city pages and any relevant blog
content — with purpose, not for link count.

### M-3 · [Per-page] Verify POI names/spellings before heavy reliance
Spot-checks passed, but ~360 POIs weren't all verified. Do a one-pass stakeholder review; normalize official
names (e.g. "Fairweather Nature Preserve" vs "…Park and Nature Preserve").

### M-4 · [Per-page] Give micro-cities a distinct angle
For near-adjacent micro-cities (Hunts Point / Medina / Clyde Hill / Yarrow Point; Ruston / Fircrest vs
Tacoma), ensure each `local_body` leads with something the neighbor's does **not** say, so Google can tell
them apart (addresses C-2 in `08`).

---

## LOW (refinements)

- **L-1** Vary heading wording slightly across pages where natural (today every page has the same 13 H2s in
  the same order).
- **L-2** Diversify internal anchor text (kitchen/bathroom anchors are the same everywhere).
- **L-3** Trim city-name density where it borders on over-insertion (median 39 mentions/page).
- **L-4** Consider a 7th, genuinely local FAQ on the strongest pages (optional).

---

## Sitewide vs per-page at a glance

| Fix once (template/data strategy) | Per-page attention |
|-----------------------------------|--------------------|
| CR-1, H-1, H-2, H-3, H-4, M-1, M-2, L-1, L-2, L-3 | CR-2, M-3, M-4 (and the longer `local_body`/FAQ/bullets *content* for each city) |

Most of the leverage is **sitewide**: the template and the per-city data model decide 86% of every page.
The per-page work is writing richer, verified local content into `local_body`, the local bullets, and the
FAQs for each city — especially the thin "Weak" pages first.

> Reminder: this plan is for your approval. No edits have been made. Await your go-ahead before any revision.
