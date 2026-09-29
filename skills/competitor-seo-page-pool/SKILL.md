---
name: competitor-seo-page-pool
description: Convert competitor SEO CSV exports from Semrush, Ahrefs, or similar tools into a reproducible, deduplicated SEO MVP page pool and an implementation-ready specification. Use when deciding which SEO pages to build from competitor Top Pages, Organic Positions, or low-difficulty keyword exports; do not use for generic market reports or post-launch GSC expansion without competitor CSV inputs.
---

# Competitor SEO Page Pool

Produce a stable decision artifact from competitor exports. The same inputs, current-site inventory, and policy version should yield materially the same canonical intent pool.

Use this narrow workflow when structured competitor exports already exist and the required output is an auditable master page pool. Use `serp-siege` instead for broader live competitor/SERP research, product-feature coverage, or a bounded cross-source execution roadmap. Do not run both by default; this skill may consume an upstream roadmap, but its page-pool decisions must still be grounded in the supplied exports.

## Required outcome

Deliver two artifacts unless the user asks for only one:

1. **Page Pool** — which canonical page intents to build, defer, review, or exclude.
2. **Implementation Spec** — how the approved P0 pool should be implemented.

Read [references/output-contracts.md](references/output-contracts.md) before producing either artifact.

Analysis does not authorize code changes, document edits, commits, pushes, deployment, or GSC actions.

## Input contract

Prefer roughly three complementary, already validated competitors. For each competitor, use the available equivalents of:

- Top Pages / Organic Pages
- Organic Positions
- Low-difficulty Positions, when separately exported

Optional inputs:

- positions from a newer or smaller competitor
- referring domains
- an existing page pool for delta comparison

For an existing site, also require or derive a current URL/Page ID inventory and current product-capability inventory. Without them, mark cannibalization and implementation fit as unassessed rather than assuming the site is blank.

Record an input manifest: source tool, competitor, market/country, export date, filename, filters, and missing inputs. Do not mix markets or dates silently.

## Workflow

### 1. Analyze page models first

Classify competitor Top Pages by observable URL pattern and page task, such as Tool, Entity, Family, Generator, Converter, Guide, Template, or Programmatic collection.

For each model calculate, when the export supports it:

- page count
- estimated organic traffic and share
- average traffic per page
- representative high-traffic URLs

Do not generate the page pool from keywords before establishing which page models demonstrably attract traffic.

### 2. Normalize keyword opportunities

Merge Organic Positions and low-difficulty exports without double-counting the same competitor, keyword, market, and ranking URL.

Treat thresholds such as `Volume >= 1,000` and `KD < 30` as project-configurable defaults, not universal hard rules. Retain stronger page-model evidence even when a keyword misses one threshold, and record the reason.

Normalize case, whitespace, punctuation, singular/plural, locale spelling variants, trailing slashes, and known aliases. Preserve the raw keyword and raw URL for traceability.

Choose one representative keyword evidence row per intent with deterministic ordering: semantic fit to the canonical task first, then qualifying organic evidence, higher volume, lower KD, better competitor position, and lexical keyword. A ranking URL alone does not make an unrelated query representative. `search_volume` and `keyword_difficulty` in the Page Pool must come from that same row. Keep minimum KD or maximum volume across aliases only as separately labeled supporting metrics; never combine them into a synthetic opportunity pair.

### 3. Cluster to canonical intent

Use this chain:

`Keywords -> competitor ranking URLs -> search task/intent -> canonical page intent`

Never use `one keyword = one page`.

Assign every candidate a stable `intent_id`, such as `color:dark-gray`, `family:shades-of-blue`, or `tool:hex-to-rgb`. Variants and aliases attach to that intent and do not automatically create indexable pages.

When evidence cannot resolve whether two terms share one intent, place them in `Review`; do not guess or publish both.

### 4. Merge competitors and compare the current site

Combine candidate intents across competitors. Increase confidence when independent competitors validate the same intent or page model.

Map each candidate to the closest current Page ID/URL and choose one action:

- `BUILD`
- `OPTIMIZE_EXISTING`
- `MERGE_REVIEW`
- `DEFER`
- `EXCLUDE`

Protect existing public URLs. A weaker new score does not authorize deletion, redirect, noindex, or canonical changes.

### 5. Assign P0, P1, P2, or Review

Do not impose a universal fixed page count.

P0 candidates should have:

- a distinct canonical search intent
- competitor traffic or ranking evidence for the page model
- useful demand relative to the project market
- product fit and an implementable page task
- reusable implementation without thin-content substitution
- a natural static internal-link source
- sufficient factual or deterministic data to build the page safely

P1 has credible demand but lower priority or incomplete evidence. P2 is backlog/observe. `Review` is mandatory for unresolved alias, canonical, SERP-intent, data-source, or migration conflicts.

Do not pad P0 to a target number. A project-specific launch cap or taxonomy allocation may be supplied as policy, but it cannot override the page-quality gate.

Within each tier, assign an explicit `priority_rank`. Use this default ordering unless the project supplies another policy:

1. data readiness: Ready, then Partial, then Blocked/Review
2. stronger cross-competitor support
3. lower representative-keyword KD
4. higher best competitor page traffic
5. higher representative-keyword search volume
6. lexical `intent_id`

KD is therefore a real sequencing factor, not just an admission threshold, but it never overrides intent validity, product fit, or the data gate. Do not use an opaque weighted score when an ordered comparison is sufficient.

### 6. Apply the data gate

Before recommending development, identify the authoritative or reviewed data needed by each page model: entity values, classifications, aliases, formulas, recipes, sources, or canonical relationships.

Separate:

- authored or source-backed facts that require review
- deterministic values that code can compute
- unsupported values that remain blocked

Do not let implementation invent factual values, aliases, recipes, product capabilities, or source claims.

### 7. Produce stable deliverables and a delta

Follow the schemas in [references/output-contracts.md](references/output-contracts.md).

If a prior pool exists, report added, removed, merged, split, retiered, and URL-changed intents with a reason tied to changed input or policy. If the same inputs and policy produce unexplained material differences, stop and reconcile them before presenting the new pool.

## Stability rules

- Version the selection policy separately from the data snapshot.
- Use `intent_id` as the comparison key; do not diff only by title or URL.
- Apply the documented `priority_rank` ordering. Keep the representative keyword's volume and KD paired to the same evidence row.
- Keep disputed semantic judgments in `Review` so they do not change between runs through improvisation.
- Do not silently change thresholds, taxonomy definitions, canonical rules, market, or locale behavior.
- Never claim competitor estimates are the target site's traffic forecast.

## Completion check

Before handoff, confirm:

- page models were analyzed before candidate selection
- every P0 row has traceable competitor evidence
- aliases do not create duplicate pages
- the current site was checked for overlap
- data readiness is explicit
- every prioritized row has a reproducible `priority_rank` and paired representative-keyword Volume/KD
- Page Pool and Implementation Spec agree on counts, routes, and page models
- the delta is explained when a previous version exists
