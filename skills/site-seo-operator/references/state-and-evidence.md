# State, evidence and metrics contract

## 1. Evidence manifest

Every report states `checked_at` (ISO date), `site`, `repo` + SHA (if read), property/market/search type and the following independently:

| Source | Primary facts supported | Unsupported inference |
|---|---|---|
| Live HTML/HTTP/robots/sitemap | route response, visible headings, static links, directives | GSC index status, CTR, demand, field performance |
| Site repository | authored routing, release gates, copy, tests and code changes | deployed SHA unless proven |
| GSC Performance | clicks, impressions, CTR, mean position **by same dimension/window** | UV, sessions, revenue, index coverage |
| GSC Page Indexing / Inspection | Google-reported index status for inspected URL/property | total visits, rank guarantee |
| Bing Webmaster | Bing performance/index data | Google data or additive unique visitors |
| GA4 | measured events/sessions/users as defined by consent and tag deployment | all real visitors if consent or tagging is incomplete |
| Ad dashboard | measured revenue, page RPM by the specific platform/timezone | search clicks converting to revenue, future earnings |
| Ahrefs/Semrush | modeled third-party rankings, estimated volume, KD, traffic | exact actual site traffic |

Use confidence tags `OBSERVED` (verified in this run), `INFERRED` (explained assumption), `REVIEW` (human or task evaluation needed), `UNASSESSED` (not accessed). Do not relabel historical/reported facts as observed today.

## 2. GSC export input

The bundled CSV triage accepts two **non-overlapping, equal-length, fully completed** exported GSC tables (same property, market/search type, dimension, filters). The script is deterministic but cannot independently verify that two CSVs share filters; the source manifest must record those conditions.

Expected column names (English GSC exports):

- `Top pages` / `Pages` / `Page` / `URL` for page mode, or `Top queries` / `Queries` / `Query` for query mode;
- `Clicks`, `Impressions`, `CTR`, `Position` (or `Average position`).

Optional `CTR` is recomputed from clicks/impressions. Numeric values may use US-style thousands separators, and percentages may be `3.1%` or `0.031`. If a required column is missing or a dimension key is duplicated, fail rather than silently aggregate. Set `--dimension page|query`; never concatenate page and query tables, and never sum a position metric.

Treat average position as a **weighted/aggregated GSC number**, not a daily rank. Flags are candidate filters: `PAGE_2_REVIEW`, `CTR_DROP_REVIEW`, `CLICK_DROP_REVIEW`, `NEW_IMPRESSION_SIGNAL`; none establish cause or guarantee uplift. Country/query mix changes can produce aggregate CTR changes without title problems.

## 3. State files

`policy.json`: `site`, `repository`, `business_model`, `target_market`, `search_type`, `ship_mode`, `indexability_policy`, `forbidden_changes`, `tests`, `primary_kpis`, `source_refs`.

`page-inventory.csv`: `intent_id,url,locale,route_class,indexability_expected,source,checked_at`.

`backlog.md`: one section per item with:

```text
ID / date / status: RESEARCH | REVIEW | PR_READY | SHIPPED | MEASURING | CLOSED
Site, canonical intent, URL, query cluster and market
Evidence: GSC export date/window + supporting URL/commit
Diagnosis vs alternative hypotheses
Proposed change and customer benefit
Tests / rollback / 28-day remeasurement / owner approval
```

`changes.md`: dated PR URL, deploy confirmation (if later explicitly authorized), tests executed, counterfactual/measurement caveat and result.

Use repo links or summarized evidence; avoid raw account data in public repositories. Only store source excerpts and CSVs if safe and permitted.

## 4. Reporting discipline

- Compare GSC periods only when the site, filters, search type, country, time granularity and window completeness match.
- Daily sampling may show noisy changes. Do not diagnose a loss from one day or use Google data later than the completed reporting window.
- Do not sum query and page clicks (they are separate breakdowns of the same traffic) or claim `GSC + Bing` equals site UV.
- In GA4, account for consent, measurement/tag issues, attribution differences and bot filters before explaining any GSC/GA4 divergence.
- Ad RPM = ad revenue / eligible pageviews * 1000 only when the platform defines those terms consistently. Do not extrapolate revenue from search clicks alone.
- Use data movement to choose an experiment, not to claim causation. Record prior version, date, and a stable follow-up window.
