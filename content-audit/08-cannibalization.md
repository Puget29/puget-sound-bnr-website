# Cannibalization Report

## Summary

**Keyword cannibalization risk: LOW.** Duplicate-content dilution risk: **MODERATE–HIGH** (covered in `04`).
No action is recommended in this audit — only identification, per the brief (no deleting, redirecting,
noindexing, or consolidating).

## A. Location page vs location page

- **Evidence:** every page targets a **distinct** `Home Remodeling in <City>` phrase. H1s differ only by
  city. Bodies are 86% identical (see `04`).
- **Search-intent overlap:** different cities = different geo-intent. A user searching "home remodeling
  Auburn" and one searching "home remodeling Kent" want different pages. So the pages do **not** compete for
  the same query.
- **Confidence:** Strong that this is **not** classic cannibalization.
- **Caveat:** For *near-adjacent* micro-cities with overlapping populations (e.g. Hunts Point / Medina /
  Clyde Hill / Yarrow Point, or Ruston / Tacoma, or Fircrest / Tacoma), Google may struggle to pick which
  near-identical page to rank for a borderline query, and could fold them together. This is a **duplicate
  content** symptom, not keyword cannibalization — the fix is differentiation (`09`), not consolidation.

## B. Location page vs dedicated Kitchen Remodeling service page

- **`/our-services/kitchen-remodeling/`** targets `Kitchen Remodeling in Bellevue, WA`; location pages target
  `Home Remodeling in <City>` and mention kitchen remodeling only in one short sub-section that **links to**
  the service page.
- **Overlap:** minimal. Location pages use `kitchen remodeling in <City>` (geo-qualified) ×1; the service
  page owns the non-geo `kitchen remodeling` intent. They reinforce rather than compete.
- **Confidence:** Strong — **low risk.** The link equity flows correctly from location pages to the service
  page.

## C. Location page vs dedicated Bathroom Remodeling service page

- Same pattern as kitchen. `bathroom remodeling in <City>` ×2 on location pages vs the service page's
  ownership of `Bathroom Remodeling in Bellevue`. **Low risk.**

## D. Location page vs the Service-Areas hub (`/service-areas/`)

- The hub targets the broad "areas we serve" navigational intent and links to all 81 cities; it does not
  target any single `Home Remodeling in <City>`. **No overlap.**

## E. Location page vs homepage / `/our-services/` index

- Homepage H1 is brand/positioning ("From first sketch to finished home."); the services index is a hub.
  Neither targets a city-qualified remodeling phrase. **No overlap.**

## Potential issue register

| ID | Competing URLs | Topic | Intent overlap | Content overlap | Concern | Evidence |
|----|----------------|-------|----------------|-----------------|---------|----------|
| C-1 | All 81 `/service-areas/*` as a set | `Home Remodeling in <City>` | Low (distinct geo) | **High (86%)** | Duplicate-content dilution of the cluster | Strong |
| C-2 | Adjacent micro-cities (e.g. Hunts Point/Medina/Clyde Hill/Yarrow Point) | geo remodeling | Moderate | Very high | Google may fold near-identical neighbors | Moderate |
| C-3 | Location pages vs `/our-services/kitchen-remodeling/` | kitchen | Low | Low | None material | Strong (low) |
| C-4 | Location pages vs `/our-services/bathroom-remodeling/` | bathroom | Low | Low | None material | Strong (low) |

**Net:** there is no genuine keyword cannibalization to resolve. The thing that *looks* like a
cannibalization problem (C-1/C-2) is really the duplication problem from `04`, and its remedy is content
differentiation, not page consolidation.
