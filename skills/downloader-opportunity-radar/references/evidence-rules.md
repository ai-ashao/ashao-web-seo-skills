# Evidence Rules v3

## 1. Domain age

Measure age at SERP observation date.

- `STRONG_FRESH`: <=6 months.
- `FRESH`: >6 and <=12 months.
- `WEAK_FRESH`: >12 and <=18 months.
- `OLD`: >18 months.

Preferred domain evidence:

1. RDAP / registrar / WHOIS creation timestamp.
2. Reputable domain-history provider.
3. Official launch announcement.
4. Earliest trustworthy public/index evidence.
5. Copyright/"established" statement only as weak fallback.

Store domain, date, exact age, band, source, confidence.

A new page on an old domain is not new-domain proof.

## 2. Ranking evidence

For every serious candidate store:

- query;
- canonical intent;
- market/language;
- observation date;
- rank;
- domain;
- URL;
- result type;
- creation date;
- age band.

A TEST NOW candidate should normally have >=3 core-query SERP checks.

Do not treat snippets returned in arbitrary order as confirmed ranking.

## 3. Keyword demand evidence

Never treat one head keyword as the whole market if close core permutations exist.

Record:

- source/database;
- country/locale;
- keyword;
- volume;
- canonical intent;
- whether the provider may cluster close variants.

Use one consistent database when summing a market. If combining tools, report them separately.

## 4. Traffic evidence hierarchy

Strongest to weakest:

1. First-party GSC/analytics for the competitor if legitimately available.
2. SEO tool organic traffic + top pages + top keywords in consistent scope.
3. Similarweb-like visits + channel mix + target-keyword/page corroboration.
4. Third-party headline monthly visits without attribution.
5. Competitor self-claims.

A headline monthly-visit number alone cannot upgrade a niche to PROVEN BREAKOUT.

## 5. Traffic attribution

Separate:

- domain total visits;
- search-share estimate;
- organic traffic estimate;
- target-cluster keyword traffic;
- target-cluster page traffic;
- unrelated traffic.

Assign confidence:

- `HIGH`: top keyword/page evidence clearly shows the target niche drives material traffic and metrics are directionally consistent.
- `MEDIUM`: target niche clearly contributes, but tool scopes differ or only a partial top-keyword/page sample is available.
- `LOW`: only headline visits or indirect data.
- `CONFLICT`: headline traffic and organic/page/keyword evidence are materially inconsistent with no scope explanation.

## 6. Traffic estimate conflict

Flag `TRAFFIC_ESTIMATE_CONFLICT` when:

- total visits are described as organic traffic;
- worldwide visits are compared directly to one-country organic data without adjustment;
- a same-scope tool shows a very large domain estimate but top pages/keywords cannot directionally support it;
- two same-type estimates differ by >5x without a plausible time/market/source explanation.

Do not overreact to small inconsistencies; third-party traffic tools are estimates.

## 7. Authority evidence

If no DR/DA is available:

- low: niche microsite, limited brand footprint;
- medium: established niche tool/SaaS;
- high: major platform/publisher/giant multi-tool brand.

Do not invent DR/DA.

## 8. Policy evidence

For platform-dependent tools, check current official Terms/help/changelog when available.

Record:

- policy observation date;
- relevant restriction/change;
- whether the product depends on violating it;
- `POLICY_SHOCK`: yes/no;
- impact: none / maintenance / monetization / hard reject.

## 9. Evidence confidence

### High

Exact SERP order + exact domain creation date + consistent target-cluster traffic evidence.

### Medium

Rank/date are credible and target cluster clearly contributes, but traffic estimates are partial or scopes differ.

### Low

Ordering, age, or traffic is indirect/inferred.

TEST NOW normally requires medium/high confidence.
PROVEN BREAKOUT requires medium/high target-cluster attribution confidence.
