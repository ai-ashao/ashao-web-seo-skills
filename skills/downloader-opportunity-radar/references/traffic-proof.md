# Traffic Proof & Sanity Checks

## Do not collapse different metrics

`Monthly Visits` != `Organic Traffic` != `Target Cluster Traffic`.

Use this decomposition:

```text
Domain Monthly Visits
        x Search Share
≈ Implied Search Visits (directional)
        ↓
SEO Organic Traffic Estimate (if available)
        ↓
Top Keywords + Top Pages
        ↓
Target Cluster Attributable Traffic
```

## Strong pattern

A young competitor is strong demand proof when:

- search is a material source;
- multiple top keywords are direct target-cluster queries;
- multiple target pages rank or one core page dominates the cluster;
- top regions/locale data explain international demand;
- the target cluster accounts for a meaningful share of the observed search/organic traffic.

## Weak pattern

Do not overvalue:

- total visits dominated by Direct with no keyword proof;
- a multi-tool domain whose traffic comes from unrelated platforms;
- a 200K headline number with only hundreds of same-scope organic page traffic;
- one keyword with high estimated traffic but no corroborating cluster.

## Directional reconciliation

Useful calculations:

- `implied_search_visits = monthly_visits * search_share`
- `target_keyword_coverage = target_keyword_traffic / implied_search_visits`
- `target_page_share = target_page_traffic / organic_traffic_estimate`

These are sanity checks, not truth. Top-5 keyword samples can represent only a small fraction of total organic traffic.

## BREAKOUT examples

A candidate can qualify as BREAKOUT demand proof when, for example:

- <=6-month site receives six-figure monthly visits, search is a majority source, and its top keywords are overwhelmingly the target downloader cluster; or
- <=12-month site has >=10K/month attributable organic traffic across >=3 core query variants; or
- multi-region SEO databases show very large core query demand and the young site ranks strongly across those markets.

## Calibration lessons

### Threads-type case

If a <=6-month site has:

- hundreds of thousands of estimated monthly visits;
- majority Search share;
- top keywords such as `{platform} downloader`, `{platform} video downloader`, `{platform} download`, `download {platform}`;
- tens of thousands of traffic attributed to those core keywords;

then the niche can be `PROVEN BREAKOUT` even if one English head keyword alone looks only medium-sized.

### Suno-type conflict case

If a site is described as ~200K traffic but a same-scope organic top-pages report implies only hundreds or low thousands, do not call the target niche 200K. Flag `TRAFFIC_ESTIMATE_CONFLICT`, identify whether the 200K is total visits vs organic traffic, and keep the opportunity at ordinary ranking-proof status until attribution is reconciled.

Calibration examples are patterns, not reusable current facts.
