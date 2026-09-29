# Output Contracts

Use these contracts to keep repeated runs comparable. Add project-specific fields only when they affect selection or implementation; do not rename the core fields between runs.

## Page Pool

One row per canonical intent. Preserve raw source evidence outside the canonical columns when needed.

| Field | Meaning |
|---|---|
| `intent_id` | Stable taxonomy key used for deduplication and diffs |
| `page_type` | Tool, Entity, Family, Generator, Converter, Guide, Template, Hub, or project-defined type |
| `suggested_url` | Proposed canonical path |
| `target_intent` | The search task owned by the page |
| `primary_keyword` | Representative query, not the page identity |
| `aliases` | Secondary queries and spelling variants that do not create pages |
| `market` | Country/language market used for evidence |
| `search_volume` | Demand metric from the named source |
| `keyword_difficulty` | Difficulty metric from the named source |
| `competitor_support` | Count and names of competitors validating the intent/model |
| `best_competitor_traffic` | Highest page-traffic estimate supporting the candidate |
| `low_kd_keyword_count` | Supporting low-difficulty query count when available |
| `source_urls` | Traceable competitor ranking/page URLs |
| `closest_existing_page` | Current Page ID/URL that may already own the task |
| `unique_page_value` | Independent data, output, or utility supplied by this page |
| `internal_link_sources` | Natural static links into the candidate |
| `data_readiness` | Ready, Partial, Blocked, or Review |
| `locale_behavior` | Initial release locales and canonical/hreflang behavior |
| `action` | BUILD, OPTIMIZE_EXISTING, MERGE_REVIEW, DEFER, or EXCLUDE |
| `tier` | P0, P1, P2, Review, or Excluded |
| `confidence` | High, Medium, Low, or Review |
| `decision_reason` | Concise evidence-based explanation |
| `priority_rank` | Deterministic development order within the assigned tier |
| `priority_reason` | Ordered factors used for the rank, including data readiness, competitor support, paired KD, page traffic, and paired volume |

`primary_keyword`, `search_volume`, and `keyword_difficulty` must describe the same representative evidence row. If minimum KD or maximum volume across aliases is useful, add separately named supporting fields rather than replacing the paired values.

### Page Pool summary

Report:

- input files and markets
- counts by page type, tier, action, and data readiness
- priority ordering and the representative-keyword KD distribution
- existing-page overlap and net-new P0 count
- aliases merged and Review items
- expected URL count by locale policy, kept separate from logical intent count
- important evidence gaps

## Page Model Analysis

For each competitor and model report:

| Page model | Page count | Estimated traffic | Traffic share | Average per page | Representative URLs |
|---|---:|---:|---:|---:|---|

Use the SEO provider's estimates as directional evidence, not verified analytics.

## Implementation Spec

The implementation specification must cover only the approved P0 pool and contain:

1. Product positioning and P0 boundary
2. Homepage intent
3. Information architecture
4. Route and stable Page ID structure
5. Page templates and unique-value contract per page model
6. Static/source-backed data and deterministic derived fields
7. Title, H1, description, canonical, and locale behavior
8. Internal linking and breadcrumb ownership
9. Structured data, only where visible content supports it
10. Sitemap and robots behavior
11. Redirect and migration map for changed public URLs
12. SSR/SSG and no-JavaScript content requirements
13. Data gates and manual review gates
14. SEO MVP acceptance criteria
15. Verification, release, production-readback, and GSC boundaries

Do not treat the Implementation Spec as authorization to modify code or publish.

## Delta Report

When a prior pool exists, compare by `intent_id` and report:

| Change | Required explanation |
|---|---|
| Added | New source evidence or policy rule |
| Removed | Evidence loss, deduplication, or explicit policy change |
| Merged | Canonical intent owner and aliases absorbed |
| Split | SERP/task evidence proving independent intents |
| Retiered | Metric, product-fit, or data-readiness change |
| URL changed | Canonical reason and migration requirement |

Also report the old/new totals and percentage of P0 changed. A material unexplained delta is a workflow failure, not a valid result.
