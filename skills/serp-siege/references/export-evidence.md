# Structured Export Evidence

Use this reference whenever the user supplies Ahrefs, Semrush, GSC, Bing Webmaster Tools, or another structured SEO dataset. The goal is to preserve the strongest evidence instead of flattening it into generic competitor notes.

## Export-first rule

When structured exports exist, process them before speculative keyword expansion or broad live browsing.

A supplied export is a dataset, not a browsing sample. Do not apply the normal “up to 8 pages per competitor” manual-browsing limit to it. Normalize, deduplicate, and process all rows relevant to the selected direction, then report what was included/excluded.

## Minimum normalized fields

Preserve when available:

- source/provider;
- dataset type (`TOP_PAGES`, `ORGANIC_KEYWORDS`, `KEYWORD_GAP`, `GSC_QUERY`, `GSC_PAGE`, `BING_QUERY`, or equivalent);
- competitor/site;
- market/country/language/database;
- extraction/data date;
- URL;
- query/keyword;
- position;
- traffic or traffic share;
- search volume;
- keyword difficulty;
- source-specific metric semantics;
- evidence provenance.

Never invent a missing metric.

## Evidence labels

- User-supplied Ahrefs/Semrush/third-party competitor exports: `USER_SUPPLIED_THIRD_PARTY`.
- User-supplied GSC/Bing data for the user's own verified property: `FIRST_PARTY`.
- Metrics read directly from a current public page: `LIVE_PUBLIC_OBSERVATION` only for what is actually observable; do not pretend private traffic estimates are public facts.
- Derived clustering or transfer judgments: `MODEL_INFERENCE`.

## Source conflict rules

Do not average conflicting tools into a synthetic number.

1. **Own-site performance:** prefer first-party GSC/Bing measurements for actual impressions/clicks/queries on that property over third-party traffic estimates.
2. **Competitor traffic:** Ahrefs/Semrush/etc. are estimates. Prefer relative ordering within the same provider, market, and date. If providers disagree materially, preserve both and lower metric confidence.
3. **Keyword volume/KD:** do not compare provider-specific scores as if they were identical scales. Pick one canonical provider for ranking within a run or keep source columns separate.
4. **Freshness:** newer comparable data normally wins over older data, unless the older snapshot is intentionally used for trend/history.
5. **Market match:** target-country/language data outranks mismatched global/other-market data for local prioritization.
6. **Scope match:** Exact URL evidence outranks domain-wide evidence when deciding whether one specific page/intent is proven.

## URL-level proof

For every retained cluster, keep enough provenance to answer:

- Which competitor URL(s) prove this page/task exists?
- Which query rows support it?
- Which provider, market, and date produced the estimate?
- Is the proof repeated across competitors or dependent on one site?

This rolls into the `Demand Evidence Map`.

## Demand-strength guidance

- `STRONG`: repeated across multiple direct competitors, or meaningful first-party query/page performance with target-market fit.
- `MEDIUM`: one credible competitor export plus supporting live/dedicated-page evidence, or repeated dedicated-page evidence without reliable metric depth.
- `WEAK`: one ambiguous/mismatched source or adjacent proxy.
- `MISSING`: no usable proof.

Demand strength is not a mathematical SEO score and must not be presented as one.
