# SERP Siege

SERP Siege is a post-decision execution-planning orchestrator for tool-site SEO. Given a user-selected website, competitor domain, keyword, or combination, it produces competitor and keyword maps, feature and SERP coverage matrices, an SEO page map, a bounded First Batch, and an MVP/P1/P2 roadmap.

The user decides whether to pursue the project. SERP Siege improves how to execute it. It does not score the opportunity, output GO/NO_GO, choose site architecture, build or publish the site, generate bulk SEO copy, submit pages for indexing, or monitor rankings.

## Research model

SERP Siege is export-first when structured evidence is available, then uses three research roles so the workflow stays bounded. Supplied Top Pages / Organic Keywords / GSC / Bing datasets are normalized before speculative expansion and are not truncated to the manual-browsing page budget.

SERP Siege keeps three research roles separate:

1. **Direct competitors — WHAT to build.** Top Pages, Organic Keywords, ranking URLs, live pages, and SERP overlap are the primary demand/page evidence.
2. **Professional vertical aggregators — WHICH tool families matter.** Optional supporting signal for demand distribution; their conversion rate or traffic ceiling is not assumed to transfer.
3. **Cross-vertical page-type leaders — HOW to structure a strategic page.** Conditional post-map enhancement only. A normal run benchmarks no more than 1–2 sites, applies the research to no more than 1–3 strategic templates, and keeps no more than 3 reusable patterns.

The third layer is deliberately optional: it may improve information architecture, CTA mechanics, preview/state handling, related-item discovery, or internal linking, but it cannot create pages, promote priority, or expand the First Batch.

## V2 evidence and scaling model

- **Demand Evidence Map:** keeps URL/query-level proof attached to each retained cluster. Strong competitor-export or first-party evidence can support a P0 supporting page even when SERP-gap research is not yet complete.
- **Page Family Map:** separates a reusable template decision from scaled instances such as font details, asset details, converter pairs, or directory items. The 8–15 First Batch default counts effective search/planning entrances, not every repeated instance.
- **Source conflicts:** third-party estimates are not averaged into fake precision. Keep source/date/market/metric semantics visible and prefer same-source relative comparisons.

## Optional upstream context

SERP Siege has no opportunity-analysis dependency. If the user already has an opportunity or architecture report, it may be supplied as `opportunity_context`; SERP Siege consumes the chosen destination and constraints without rerunning or challenging the upstream decision.

## Example

```text
Use $serp-siege with:

target:
  keyword: image compressor
market:
  country: US
  language: en
business:
  monetization: adsense
  maintenance_preference: low
execution:
  destination: independent_site
competitor_exports:
  - source: ahrefs
    type: top_pages
    file: competitor-a-top-pages.csv
  - source: semrush
    type: organic_keywords
    file: competitor-b-keywords.csv
```

## Validation

```bash
python3 -B skills/serp-siege/scripts/validate_output.py path/to/report.md
python3 -B -m unittest discover -s skills/serp-siege/tests -v
```

Validation confirms execution-report structure, destination provenance, evidence traceability, enum values, cross-map cluster consistency, unique page URLs, First Batch shape or deviation, and P0-to-First-Batch coverage. The optional Page Pattern Enhancement is intentionally not a required report heading. Live SERP accuracy, benchmark transfer quality, and evidence truthfulness still require review.
