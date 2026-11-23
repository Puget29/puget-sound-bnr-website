# FAQ Report

Every page renders **exactly 6 FAQs** (meets the >=5 requirement). Structure is identical sitewide:

| # | FAQ | Source | Uniqueness across 81 pages |
|---|-----|--------|-----------------------------|
| 1 | `Do you work in <City>?` (or `...in my part of <City>?`) | `faq_local[0]` | **2 question templates, ~11 answer templates** — near-boilerplate |
| 2 | `Do I need a permit for my project in <City>?` | `faq_local[1]` | **1 question (identical on all 81), 3 answer templates** — boilerplate |
| 3 | `Do you do kitchen and bathroom remodeling in <City>?` | hardcoded | identical on all 81 |
| 4 | `Do you have an office in <City>?` | hardcoded | identical on all 81 |
| 5 | `What affects the cost of a home remodel in <City>?` | hardcoded | identical on all 81 |
| 6 | `How do I get an estimate for my <City> project?` | hardcoded | identical on all 81 |

## Findings

- **Count is fine** (6 >= 5 on every page). Questions are genuine homeowner concerns (service area, permits, kitchen/bath availability, office location, cost drivers, how to get an estimate).
- **Pricing answer is safe** — FAQ 5 explicitly declines to quote and explains cost *drivers* instead of inventing numbers. No fabricated prices, timelines, or guarantees anywhere.
- **Uniqueness is weak.** FAQ 2's question is word-for-word identical on all 81 pages; its answer uses only 3 templates. FAQs 3-6 are fully identical sitewide. Only FAQ 1 (and occasionally FAQ 2's answer) carries any per-city variation, and even that is drawn from a small template pool. **Effectively ~0.5-1 of the 6 FAQs is genuinely local.**
- **Missing opportunities:** no city-specific kitchen OR bathroom question (they are merged into one generic Q3); no question tied to the local housing stock, climate, or the specific neighborhoods named in `local_body`.

FAQ schema (`FAQPage`) is present and mirrors the 6 visible Q&As on every page.

