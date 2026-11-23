# Local Relevance & Geographic Content Report

## What carries local relevance on each page

| Element | Source | Per-city? | Quality |
|---------|--------|-----------|---------|
| Points of interest (3–5) | `city-local.json` → POI section | **Unique** | **Strong — specific, verifiable** |
| Nearby communities (5–8 links) | `city-local.json` → areas section | **Unique** | **Strong — geographically sensible** |
| `local_body` prose (32–77 words) | `city-facts.json` | **Unique** | Good but **thin** |
| Local bullet 3 of 4 | `city-facts.json` | Usually unique | Moderate |
| Driving-directions map | generated from city name | Per-city | Functional |
| Permit bullet / permit FAQ | `city-facts.json` | **Templated** (city-swapped) | Weak as *local* content |

POI count: **41 pages have 5 POIs, 39 have 4, 1 has 3** (Hunts Point). All pages have a working GBP map +
a city-specific driving-directions map.

## Geographic accuracy — spot-verified

POIs read as genuinely researched and specific rather than generic. A sample was independently verified
via web search:

- **North Bend:** Mount Si, Rattlesnake Lake, Twede's Cafe (the "Double R Diner" from *Twin Peaks*), Olallie
  State Park, Tanner Landing Park — all real and correctly located. ✅
- **Snoqualmie Pass:** The Summit at Snoqualmie (ski area), Gold Creek Pond, WA State Ski & Snowboard Museum,
  Alpine Lakes Wilderness — all real and correctly located. ✅
- **Gig Harbor:** Skansie Brothers Park/Netshed, Crescent Creek Park, Eddon Boat Park, Harbor History Museum
  — all real. ✅
- **Medina:** *Fairweather Nature Preserve* — verified real, in north Medina (city lists it as
  "Fairweather Park and Nature Preserve"; the official name drops "Park"). ✅ (minor naming nuance)
- **Hunts Point:** *Points Loop Trail* — verified: a real urban loop connecting Hunts Point, Medina,
  Clyde Hill and Yarrow Point. ✅

**Conclusion:** the sampled POIs are accurate and well-matched to their cities. No incorrect or
mislocated landmark was found in the sample.

### Scope limit (honest)

~360 POIs across 80 cities were **not** exhaustively verified — only a sample. The remainder are
**researched but not independently re-verified** and are labelled *Needs verification* rather than asserted
correct. Recommended: a one-pass human/stakeholder check of POI names and spellings before relying on them
in any citation context. Minor naming normalizations (e.g. official park names) may surface.

## Nearby communities

Nearby-city clusters are geographically correct and useful for internal linking and relevance, e.g.:

- North Bend → Snoqualmie, Issaquah, Sammamish, Snoqualmie Pass, Carnation, Duvall, Maple Valley ✅
- Gig Harbor → Tacoma, Port Orchard, Bremerton, University Place, Fircrest, Ruston, Steilacoom ✅
- Medina → Bellevue, Clyde Hill, Hunts Point, Yarrow Point, Kirkland, Mercer Island ✅

All nearby links resolve to existing location pages (0 broken links sitewide).

## Weaknesses

1. **`local_body` is thin** (median 39 words). The strongest local prose names real neighborhoods —
   Bellevue cites Crossroads, Newport Hills, Somerset, Wilburton; Seattle cites craftsman bungalows /
   mid-century homes. But many smaller cities get only 1–2 generic sentences ("a mix of established homes
   and newer subdivisions") with **no named neighborhood, street, or landmark** in the prose itself (POIs
   live in a separate section).
2. **Permit bullet and permit FAQ are not real local content** — they say "the City of `<City>`" but the
   surrounding sentence is identical everywhere; they imply local specificity without delivering it.
3. **"No office to visit in `<City>`"** is stated clearly and repeatedly — good, avoids a false local-office
   claim. No page implies a physical presence or completed local projects without evidence. ✅
4. **POIs are framed carefully** ("reference points, not project sites") — avoids implying work was done at
   those landmarks. ✅

## Pages with strong vs weak local context

- **Strongest:** Bellevue, Seattle, Anacortes, Bainbridge Island, Gig Harbor, North Bend, Snoqualmie Pass —
  longer place-named prose and/or 5 distinctive POIs.
- **Weakest (thin prose, generic bullets):** the small-city cluster with <40-word `local_body` and no named
  neighborhood — e.g. Covington, Roy, Steilacoom, Milton, Pacific, Edgewood, Ruston, Fircrest, Medina,
  Yarrow Point. These lean almost entirely on their POIs for differentiation. See `10` for the per-page list.
