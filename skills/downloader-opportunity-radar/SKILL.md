---
name: downloader-opportunity-radar
description: Find and validate SEO opportunities for downloader/save/export utility sites by expanding the full download-intent keyword universe, verifying whether genuinely young domains rank across the intent cluster, attributing traffic to the target cluster instead of headline domain visits, and scoring technical/policy durability. Treat domains 6 months or less as strong evidence, 6–12 months as normal evidence, 12–18 months as weak supporting evidence, and older than 18 months as old. Use for downloader niche discovery, competitor validation, global/locale opportunity sizing, and TEST NOW / WATCH / REJECT / PROVEN BREAKOUT decisions.
---

# Downloader Opportunity Radar v3

## Purpose

Find downloader/save/export utility niches that are realistically attackable by a new SEO site.

The core question is not:

> Does `{platform} downloader` have traffic?

It is:

> Across the complete core download-intent cluster, can a genuinely young domain rank now, is the demand large enough after query-permutation and locale expansion, is the observed traffic actually attributable to this niche, and can we build the product with acceptable maintenance and policy risk?

v3 fixes two common false conclusions:

1. **Single-keyword undercounting** — `threads downloader` is not the whole Threads download market. `threads download`, `download threads`, `threads video downloader`, `download threads video`, etc. can be separate material queries and SERPs.
2. **Headline-traffic overclaiming** — a domain with 200K estimated visits does not prove a 200K niche. Traffic must be attributed to the target downloader cluster using top keywords/pages and search-source evidence.

Prioritize lightweight, low-support, ad-monetizable tools. Favor browser-side or light-backend implementations. Avoid opportunities that depend on DRM circumvention, paywall bypass, credential theft, private-content scraping, or clearly unauthorized access.

## Default assumptions

Unless the user overrides them:

- Primary discovery market: Google English, then expand to evidence-led locales.
- Domain-age bands:
  - `STRONG_FRESH`: <=6 months.
  - `FRESH`: >6 and <=12 months.
  - `WEAK_FRESH`: >12 and <=18 months.
  - `OLD`: >18 months.
- Primary ranking threshold: organic Top 10.
- Product shape: 10–30 useful SEO/product pages for initial validation.
- Monetization: ads first; optional affiliate/API later.
- Preferred maintenance: low.
- Preferred infrastructure: client-side first, stateless/light backend second.

Do not assume US-only demand for downloader tools. These utilities often behave as **global utility search** products. Locale priority must come from actual keyword/competitor evidence, not a fixed ES/PT/DE/FR template.

## Required inputs

The skill can run from any of these:

1. No seed: discover downloader niches from scratch.
2. Platform seed: e.g. `Threads`, `Bluesky`, `Kick`, `RedNote`.
3. Asset seed: e.g. `thumbnail`, `emoji`, `SVG`, `website images`.
4. Keyword seed: e.g. `threads video downloader`.
5. Competitor seed: a known downloader site.

Do not block on missing optional inputs. Use defaults and proceed.

# Workflow

## Step 1 — Discover 20–60 candidate niches

Search across three dimensions.

### A. Platform

Favor:

- emerging social networks;
- creator/video platforms;
- streaming platforms;
- community/chat platforms;
- AI music/video/image/voice platforms;
- ecommerce/CMS platforms;
- developer platforms;
- game/mod platforms;
- presentation/recording platforms;
- design/asset platforms.

Prefer platforms that are growing, recently changed product behavior, or have an immature third-party utility ecosystem.

### B. Asset

Generate plausible asset-specific intents:

- video;
- image / photo;
- carousel / album;
- GIF;
- audio;
- thumbnail;
- avatar / profile picture / PFP / DP;
- banner / cover;
- emoji;
- sticker;
- icon;
- clip;
- VOD;
- stream;
- artwork / cover art;
- SVG;
- file / folder / repository asset;
- metadata / captions / chat export where lawful and useful.

### C. Action

Use:

- downloader;
- download;
- save;
- export;
- extractor;
- grabber;
- fetcher;
- bulk downloader;
- batch downloader;
- download all;
- ZIP downloader.

Do not mechanically generate invalid Cartesian products.

## Step 2 — Build the full Intent Permutation Set BEFORE market sizing

This is a hard v3 requirement.

For every serious platform candidate, do not validate only one seed such as `{platform} downloader`.

Generate and inspect at least these **core action permutations**:

- `{platform} downloader`
- `{platform} download`
- `download {platform}`

For every plausible core asset, generate:

- `{platform} {asset} downloader`
- `{platform} {asset} download`
- `download {platform} {asset}`
- `download {asset} {platform}`

Add natural synonyms where users actually use them, e.g.:

- `profile picture` / `pfp` / `dp`;
- `image` / `photo`;
- `video` / `mp4` only when supported by evidence;
- `download` / `save` where query language makes sense.

Then discover additional variants from autocomplete, related searches, competitor top keywords, and SEO databases.

### Core vs secondary modifiers

Keep these separate.

**Core permutations** define market size and rankability:

- word order;
- download vs downloader;
- asset type;
- common asset synonym.

**Secondary modifiers** are phase-two expansion only unless they show independent volume/SERP intent:

- free;
- online;
- HD;
- MP4;
- no watermark;
- without login;
- iPhone;
- Android;
- Chrome.

Do not let secondary modifiers inflate the core market estimate.

Use `scripts/generate_keywords.py` as a deterministic starting point, then enrich with live evidence.

## Step 3 — Canonicalize the keyword universe

Create a table with:

- raw keyword;
- canonical intent;
- asset;
- action pattern;
- locale/market;
- volume if available;
- current ranking evidence;
- target page mapping.

Group close variants under one canonical intent, but **do not erase distinct material queries** merely because they mean the same thing.

For market sizing, report both:

1. `Observed Core Cluster Volume` — sum of material keyword volumes from a single consistent database/market, with a warning that SEO tools may cluster close variants differently.
2. `Conservative Demand Range` — a lower-confidence range after removing obviously duplicated/near-identical tool groupings when the provider appears to double-count.

Never use one keyword's volume as the niche size when 5+ material core permutations exist.

## Step 4 — Run live SERP validation across the cluster

For each serious candidate, inspect at least:

- the head query;
- the strongest alternate word-order query;
- the strongest asset-specific query.

For a downloader platform candidate this normally means >=3 SERPs before classification.

Capture organic Top 10 as accurately as available. Ignore ads, AI answer modules, shopping blocks, and unrelated results.

For each result record:

- query;
- rank;
- domain;
- URL;
- title;
- page type: dedicated tool / feature page / blog / extension / directory / official;
- apparent authority: low / medium / high;
- niche microsite vs giant multi-tool domain.

Do not call a niche OPEN because one young domain appears for one query. Look for **cluster-level rankability**.

## Step 5 — Verify domain freshness

Use exact age on the SERP observation date:

- `STRONG_FRESH`: <=6 months — strong new-site proof.
- `FRESH`: >6 to <=12 months — normal proof; stricter TEST NOW gate.
- `WEAK_FRESH`: >12 to <=18 months — supporting evidence only.
- `OLD`: >18 months — no fresh-site proof.

Evidence hierarchy:

1. RDAP / registrar / WHOIS creation date;
2. reputable domain-history service;
3. official launch evidence;
4. earliest trustworthy indexed/public evidence;
5. copyright/established claims only as weak fallback.

A new page on an old domain is not young-domain proof.

## Step 6 — Classify cluster-level SERP openness

Assign:

- `OPEN`: strong young-domain proof appears across >=2 core permutations, or one <=6-month domain ranks very strongly and neighboring SERPs are fragmented.
- `ATTACKABLE`: qualifying 6–12 month proof or <=6-month proof exists but is concentrated in one query.
- `MIXED`: only 12–18 month proof, inconsistent intent, or strong incumbents coexist with weak sites.
- `LOCKED`: old/high-authority/official domains dominate and no convincing <=12-month proof exists.

A single exact-match domain is not enough.

## Step 7 — Validate demand and traffic attribution

### A. Do not confuse these metrics

Keep separate:

- `Domain Monthly Visits` — Similarweb-like total visits across all channels.
- `Search Share` — percentage of visits attributed to search.
- `Organic Traffic Estimate` — Semrush/Ahrefs-like estimated organic visits.
- `Target Cluster Traffic` — traffic attributable to the specific downloader niche being evaluated.

### B. Traffic attribution table

For every high-potential competitor record:

- total domain visits;
- search share;
- implied search visits if calculable;
- organic traffic estimate if available;
- top 10–50 keywords;
- top 10–50 pages;
- target-cluster keyword traffic;
- target-cluster page traffic;
- other-topic traffic;
- attribution confidence.

### C. Sanity-check headline numbers

Flag `TRAFFIC_ESTIMATE_CONFLICT` when a headline claim cannot be directionally reconciled with top pages/keywords or when two tools differ by an extreme multiple without a clear scope explanation.

Examples:

- 200K monthly visits does **not** equal 200K Google organic traffic.
- A site with 200K headline traffic but only hundreds of organic page traffic in the same supposed scope must be treated as conflicting until explained.
- A 600K-visit site with ~60% search share plus multiple target-cluster keywords contributing tens of thousands is much stronger evidence that the niche itself drives traffic.

Use `scripts/traffic_sanity_check.py` when the numbers are available.

### D. Demand proof grades

Assign one:

- `BREAKOUT`: >=10K/month attributable target-cluster search/organic traffic OR similarly strong multi-region evidence, with >=3 material core keywords/pages and no unresolved traffic conflict.
- `STRONG`: 3K–10K attributable target-cluster traffic or multiple high-volume core queries with ranking proof.
- `MODERATE`: 1K–3K attributable traffic or credible cluster volume with several ranking keywords.
- `WEAK`: only one small keyword or indirect traffic evidence.
- `UNKNOWN`: no reliable demand data.

Absolute numbers are directional, not GSC truth. Prefer consistency across keyword, page, region, and search-source evidence.

## Step 8 — Check locale opportunity AFTER English/core validation

Downloader utilities are often global.

Do not automatically copy the same locales to every site.

Use:

- competitor top regions;
- country-specific keyword databases;
- language-specific SERPs;
- top keyword language patterns;
- platform adoption by country.

For the top 3–5 geographies, inspect local-language and English-query behavior.

Report:

- locale;
- evidence source;
- core query demand;
- fresh-site SERP proof;
- recommended phase: launch / phase 2 / skip.

## Step 9 — Evaluate product feasibility

Assess:

- client-side feasibility;
- backend/proxy requirement;
- API dependence;
- anti-bot/signature churn;
- media remux/transcoding;
- bandwidth/storage cost;
- platform breakage risk;
- abuse/support burden.

Preferred:

- public CDN URLs;
- public metadata/API;
- deterministic URL transforms;
- browser parsing;
- stateless server functions.

Penalize frequent reverse engineering.

For platform-dependent downloaders, recommend an **Extractor Spike** before full build when parsing stability is uncertain. Test 30–50 representative public URLs and require a clear success-rate threshold before committing.

## Step 10 — Policy-shock and durability screen

Check current platform rules, especially after product/ToS changes.

Apply `POLICY_SHOCK` when a recent platform change materially affects the downloader's core behavior.

Hard reject or heavily downgrade when the product depends on:

- DRM or technical-access-control circumvention;
- paid/private/authenticated content access without authorization;
- bypassing explicit download quotas through unauthorized acquisition;
- credential/token extraction;
- paywall bypass;
- private account access;
- mass scraping personal data.

A surge in demand caused by a new restriction is not automatically a good business opportunity if the only product path is prohibited or operationally fragile.

## Step 11 — Build the page cluster

A good opportunity must support useful intent, not doorway pages.

Build 10–30 initial pages from:

- parent downloader;
- asset-specific downloader;
- bulk/batch variant where real;
- format-specific tool where real;
- adjacent viewer/extractor;
- device/use-case variant only with distinct SERP intent;
- guides solving real usage problems;
- evidence-led locale pages after validation.

Separate:

- `Core SEO pages` — distinct tool intents;
- `Supporting pages` — guides/device/help;
- `Locale expansion` — only after locale evidence.

## Step 12 — Score using v3 model

Use `references/scoring.md` and `scripts/score_candidate.py`.

v3 scoring dimensions:

- Young-domain SERP proof: 25
- SERP weakness: 12
- Demand & attributable traffic proof: 18
- Keyword/page cluster depth: 12
- Product feasibility: 12
- Maintenance burden: 8
- Monetization: 5
- Platform growth/timing: 4
- Legal/policy durability: 4

### Decisions

- `PROVEN BREAKOUT`: not a separate score band; an upgrade label on a qualifying TEST NOW niche with `BREAKOUT` demand proof and consistent target-cluster attribution.
- `TEST NOW`: 78–100, age gate passed, confidence >= medium, no hard reject.
- `WATCH`: 65–77, weak age evidence, unresolved traffic conflict, or insufficiently strong 6–12 month proof.
- `REJECT`: <65 or hard-reject condition.

### Age gate

`TEST NOW` requires one of:

1. >=1 `STRONG_FRESH` <=6-month domain in current Top 10; or
2. qualifying `FRESH` 6–12 month evidence: >=1 domain Top 5, or >=2 domains Top 10 plus a weak/fragmented SERP.

12–18 month evidence can never independently trigger TEST NOW.

### PROVEN BREAKOUT gate

Requires all:

- base decision = TEST NOW;
- demand proof = `BREAKOUT`;
- target-cluster attribution confidence = medium/high;
- no unresolved `TRAFFIC_ESTIMATE_CONFLICT`;
- >=3 material core keywords with target-cluster ranking/traffic evidence OR >=2 target-cluster top pages;
- no policy hard reject.

## Step 13 — Cross-check top candidates

Before finalizing TEST NOW / PROVEN BREAKOUT:

- rerun >=3 core permutations;
- verify the young domain's rank is not a one-query anomaly;
- inspect at least one alternate market/locale when traffic is globally distributed;
- reconcile headline traffic with top keywords/pages;
- re-check current platform policy/technical feasibility.

## Step 14 — Produce a decision-ready report

Use `templates/report.md`.

Always include:

1. Executive shortlist.
2. Core Intent Permutation Set.
3. Core cluster demand table.
4. SERP evidence across >=3 queries.
5. Exact young-domain dates.
6. Traffic attribution / sanity check.
7. Locale opportunity where relevant.
8. Suggested MVP.
9. 10–30 page cluster.
10. Technical risk and Extractor Spike if needed.
11. Policy/legal durability.
12. Score and TEST NOW / WATCH / REJECT.
13. PROVEN BREAKOUT label only when the gate is satisfied.
14. “What would falsify this thesis?”

# Evidence discipline

Never write:

- “new sites can rank” without domain, creation date, query, and rank;
- “market is 13K” from one keyword when the core intent has multiple permutations;
- “site gets 200K organic” when the source is total monthly visits;
- “200K niche” from a 200K domain whose traffic is mostly another topic;
- “low competition” only because KD is low;
- “domain is new” from design/copyright year;
- precise traffic/volume/CPC/KD without a source.

If paid SEO data is unavailable, continue using live SERPs and label market size `not verified` rather than inventing numbers.

# Stop conditions

Stop or downgrade when:

- no <=18-month domain appears after two close query variants, and no <=12-month evidence appears after deeper validation for TEST NOW;
- the SERP is locked by official/high-authority domains;
- the niche only looks large because of unrelated domain traffic;
- `TRAFFIC_ESTIMATE_CONFLICT` remains unresolved and the thesis depends on the headline number;
- implementation depends on prohibited access-control circumvention;
- platform dependency is high and cluster depth is shallow;
- intent is informational rather than tool/download intent.

# Final QA checklist

Before returning:

- [ ] Generated full core Intent Permutation Set, not only one seed keyword.
- [ ] Checked >=3 material core permutations for serious candidates.
- [ ] Reported cluster demand rather than single-keyword demand.
- [ ] Separated Domain Visits, Search Share, Organic Traffic, and Target Cluster Traffic.
- [ ] Reconciled headline traffic with top pages/keywords or flagged `TRAFFIC_ESTIMATE_CONFLICT`.
- [ ] Every TEST NOW candidate has current Top 10 evidence.
- [ ] Every TEST NOW candidate has qualifying <=12-month domain evidence.
- [ ] <=6 months = STRONG_FRESH; 6–12 = FRESH; 12–18 = WEAK_FRESH; >18 = OLD.
- [ ] 12–18 month evidence never independently triggers TEST NOW.
- [ ] PROVEN BREAKOUT is based on attributable target-cluster demand, not total domain visits.
- [ ] Locale expansion is evidence-led, not copied blindly.
- [ ] At least 10 plausible pages exist without doorway spam.
- [ ] Product feasibility and maintenance are explicitly scored.
- [ ] Current policy/ToS shock is checked for platform-dependent tools.
- [ ] No fabricated SEO metrics appear.
- [ ] Each TEST NOW recommendation includes a falsification condition.
