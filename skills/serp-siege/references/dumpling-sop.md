# Dumpling Workflow SOP

Use this procedure after framing the input. It keeps exploration broad enough to find the opportunity while bounding research cost.

## 1. 定馅 / FRAME

Identify:

- the primary job-to-be-done and core tool intent;
- the primary keyword or domain-derived candidate cluster;
- target market and language, with assumptions marked;
- the destination or host chosen by the user, when supplied;
- visible SERP result types and recurring competitors;
- the candidate's product promise and likely workflow;
- legal, copyright, policy, API, technical, and maintenance constraints;
- whether meaningful adjacent clusters can share a product core;
- optional upstream context that should be preserved rather than reassessed.

Do not judge whether the project is worth doing, choose its architecture, or invoke an opportunity-analysis skill. The user has already decided to proceed.

## 2. 擀皮 / EXPAND

Collect candidates across:

- synonyms, spelling, word order, input/output formats, file types;
- target size or dimensions, constraints, use cases, audiences;
- devices, platforms, problems, solutions, privacy, signup, and pricing modifiers;
- comparisons, alternatives, specifications, localization, and adjacent tools;
- competitor tool pages, navigation, top landing pages, guides, FAQs, related tools, and URL patterns;
- recurring, weak, outdated, thin, mixed-intent, forum, video, and large-brand SERP results.

When the user supplies Top Pages, Organic Keywords, Keyword Gap, GSC, Bing, or equivalent exports, process that evidence before speculative expansion. Normalize it with `export-evidence.md`, preserve URL/query provenance, and use the observed high-traffic/high-ranking page set to seed clusters. A supplied export is a dataset, not a browsing sample: process all relevant rows after deduplication rather than truncating it to the live-browsing page budget. Expand speculatively only where a distinct intent or workflow remains uncovered.

Do not remove a query merely because supplied search volume is small. Preserve it until clustering and page mapping.

### Research source roles

Use each source class for a different question:

1. **Direct competitors — demand and page evidence.** Default source. Use their Top Pages, keywords, ranking URLs, live pages, navigation, and SERP overlap to answer what users search for and which intents already support separate landing pages.
2. **Professional vertical aggregators — demand distribution.** Optional. Use a relevant collection/tool platform to identify which tool families or categories receive disproportionate attention when reliable supplied or observable evidence exists. Do not transfer its conversion rate, traffic ceiling, RPM, or economics to the candidate.
3. **Cross-vertical page-type leaders — page structure.** Conditional and post-map only. Use them to answer how a strategically important page template can be structured when direct competitors do not provide a sufficiently strong pattern. Follow `page-type-benchmark.md`.

Do not use source class 2 or 3 to manufacture new clusters. New pages still require direct search/competitor evidence or a clearly distinct user task under the normal clustering and mapping rules.

## Research bounds and stopping

When live browsing is available, default to:

- the first 10 organic results for the primary query;
- 3–5 recurring or product-relevant direct competitors;
- for live/manual browsing only: the homepage, main tool page, navigation or sitemap surface, and up to 8 relevant pages per direct competitor;
- for supplied structured exports: no 8-page cap; process the relevant dataset after normalization/deduplication and report dataset coverage;
- up to 2 professional vertical aggregators only when they add a meaningful demand-distribution signal;
- one expansion pass per distinct dimension, followed by one deduplication pass.

Cross-vertical page-type research does **not** run during normal expansion. It is a conditional post-map step with its own tighter budget in `page-type-benchmark.md`.

Expand beyond the direct-competitor defaults only when a new distinct intent or workflow continues to appear. Stop after two consecutive passes add no distinct cluster, or when additional pages repeat known templates without new evidence. Report coverage limits.

When live browsing is unavailable, do not describe SERP or competitor claims as current. Use `MISSING` or supplied evidence, lower planning confidence, and continue with a bounded execution plan that makes the missing evidence and validation action explicit.

## 3. 分馅 / CLUSTER

Apply the intent-first rules in `clustering-rules.md`. Preserve rejected permutations in a short exclusion list so they do not reappear later. Build a `Demand Evidence Map` before priority assignment so each retained cluster keeps its strongest traceable proof instead of losing URL-level evidence during clustering.

## 4. 画饺子地图 / MAP

Build the Demand Evidence, Feature Coverage, and SERP Coverage views from `coverage-model.md`, then decide the page treatment for every retained cluster with `page-mapping-rules.md`.

If many retained URLs are instances of the same archetype, create a Page Family Map with `page-family-rules.md`. Make the template/family decision once, keep representative instances, and record the initial instance count/scaling rule instead of repeating the same product decision hundreds of times.

Only after the SEO Page Map and any Page Family Map are stable, ask whether a strategic page template still has an unresolved structure, UX, conversion, discovery, or internal-link question. If yes, run the conditional Page Pattern Enhancement from `page-type-benchmark.md`. If not, skip it and continue.

## 5. 包第一锅 / PRIORITIZE

Apply `priority-rules.md`. The First Batch is a coherent shared-core release, not the top rows of a keyword list. Page-pattern benchmark observations may refine how a selected page is composed, but they may not raise its demand priority.

## 6. 出菜单 / ROADMAP

Use `report-template.md`. Keep supplied, observed, inferred, and missing evidence visibly distinct. Include the optional Page Pattern Enhancement section only when that benchmark actually ran. End with a concrete next execution or pre-development validation action.
