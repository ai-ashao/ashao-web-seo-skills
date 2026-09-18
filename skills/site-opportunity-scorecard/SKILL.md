---
name: site-opportunity-scorecard
description: Decide whether an SEO/product opportunity should live as an independent site, an existing-site section, an existing-site page, or be observed/rejected. Use before implementation when site architecture is genuinely undecided. Supports decision profiles such as seo_first_utility, product_led, content_site, and downloader. Do not design the SEO page matrix; hand the selected architecture and evidence to serp-siege.
---

# Site Opportunity Scorecard v2

Answer one question only:

> **Where should this opportunity live?**

Valid outcomes:

- `INDEPENDENT_SITE`
- `EXISTING_SITE_SECTION`
- `EXISTING_SITE_PAGE`
- `OBSERVE_OR_REJECT`

This skill is an architecture/admission decision layer. It does **not** build the site, design the final homepage, produce an SEO MVP page matrix, or decide every URL. Once architecture is selected, hand the evidence to `$serp-siege`.

## Decision profiles

Choose the profile that best matches the opportunity. Do not create a new Skill for every niche.

- `seo_first_utility` — converters, viewers, generators, calculators, download-like utilities, file tools, small ad-first tools.
- `product_led` — SaaS or products where workflow differentiation, activation, retention, or paid conversion is central.
- `content_site` — content/wiki/directory opportunities where the content system is the product surface.
- `downloader` — use `seo_first_utility` decision behavior plus the downloader-specific evidence checks in `references/profiles/downloader.md`.
- `generic` — use only when no profile above fits.

A profile changes **how evidence is interpreted**, not the evidence labels or the scoring scale.

## Responsibility boundary

This skill may:

- decide site / section / page / reject;
- evaluate independent demand, SERP entry, differentiation, distribution, economics, maintenance, and separation risk;
- use user-supplied Ahrefs/Semrush/GSC/Bing data as first-class evidence;
- state hard gates and minimum validation requirements;
- produce a compact handoff to SERP Siege.

This skill must not:

- generate a final keyword-to-URL map;
- produce an 8–15 page First Batch;
- invent Page Families or scaled instances as an execution plan;
- prescribe detailed Title/H1/CTA copy for the final site;
- rerun the downstream SERP Siege workflow inside this report.

## Inputs

Use whatever evidence is available. Typical inputs:

- candidate idea or keyword cluster;
- `decision_profile`;
- target market/language;
- possible host site;
- business model and maintenance constraints;
- direct competitors;
- user-supplied Ahrefs/Semrush Top Pages / Organic Keywords exports;
- GSC/Bing/analytics data when the opportunity extends an existing site;
- live SERP and competitor observations.

Never fabricate volume, traffic, KD, backlinks, revenue, or conversion.

## Evidence labels

Use:

- `FIRST_PARTY`
- `USER_SUPPLIED_THIRD_PARTY`
- `LIVE_PUBLIC_OBSERVATION`
- `HISTORICAL_PUBLIC_SOURCE`
- `MODEL_INFERENCE`
- `MISSING`

Missing evidence is not negative evidence. Lower confidence and name the validation required.

## Workflow

### 1. Frame the candidate

Define the primary job, candidate cluster, market, possible host, business model, maintenance constraints, and decision profile.

### 2. Establish independent demand

Determine whether the opportunity has a coherent discoverable demand system independent of the host.

Prefer, in order:

1. first-party query/completion data;
2. user-supplied Top Pages / Organic Keywords / traffic exports;
3. current SERP and competitor observations;
4. historical public evidence;
5. model inference.

For SEO-first utilities, repeated competitor Top Pages and keyword clusters are valid demand evidence even when product workflows look similar.

### 3. Inspect SERP entry and competitive proof

Evaluate:

- dominant page type and intent;
- whether dedicated tools, suites, homepages, forums, docs, or content pages rank;
- evidence that newer/smaller sites can enter, when available;
- whether weak or mismatched results exist;
- whether the candidate needs authority/link proof beyond product fit.

Do not use KD alone as SERP breakability.

### 4. Compare candidate vs host

Assess:

- keyword overlap;
- search-intent overlap;
- product/workflow overlap;
- content/template overlap;
- brand-positioning ambiguity;
- link-authority fragmentation;
- maintenance fragmentation.

Code reuse is not a reason by itself to merge or split sites.

### 5. Score opportunity and separation risk

Use the existing 0–5 scoring rubric and deterministic calculator.

Profiles alter the independent-site gate:

- `product_led` / `generic`: workflow differentiation remains decision-critical.
- `seo_first_utility` / `downloader`: **workflow difference is not a hard gate**. Independent demand, coherent expansion, low host overlap, and viable economics may justify a separate site even when the core interaction resembles other tools.
- `content_site`: content-system independence and search-intent separation matter more than homepage workflow novelty.

Do not raise or lower a raw criterion score merely to force the preferred architecture.

### 6. Apply hard gates

Use scoped hard gates:

- `SITE_ONLY` — blocks a new domain but may permit a section/page.
- `BLOCK_PRODUCT` — blocks every architecture until resolved.

Examples of `BLOCK_PRODUCT` include unacceptable legal/policy dependency or a maintenance requirement that directly violates the user's operating constraints.

### 7. Choose exactly one architecture

Use the deterministic result as a guardrail, then explain the decisive evidence and uncertainty.

When confidence is low, do not pretend the score is final. Prefer a reversible validation surface.

### 8. Produce a SERP Siege handoff

End with a compact handoff containing only:

```yaml
opportunity_context:
  source: site-opportunity-scorecard
  decision_profile: seo_first_utility
  destination: INDEPENDENT_SITE
  primary_job: ...
  primary_cluster: ...
  market: ...
  evidence_datasets:
    - ...
  constraints:
    - ...
  exclusions:
    - ...
  unresolved_questions:
    - ...
```

Do not include a final page matrix. SERP Siege owns Page Families, SEO Page Map, and First Batch.

## Profile-specific rules

### SEO-first utility

A separate site can be justified without a novel workflow when there is strong evidence for:

- a coherent independent query cluster;
- enough non-duplicate expansion to sustain a site;
- low-to-moderate overlap with the proposed host;
- clear topical/category positioning;
- viable low-maintenance economics;
- a plausible distribution/link or recurring-use reason.

Do not require product novelty for its own sake.

### Downloader

Read `references/profiles/downloader.md`. Keep downloader-specific keyword permutations, traffic attribution, fresh-domain proof, extractor/platform durability, and policy checks here as a profile—not as a separate Skill.

## Minimum validation

When decision confidence is medium/low, define the cheapest reversible test. Examples:

- an existing-site landing page;
- a small section;
- a lightweight prototype;
- a bounded SERP/Top Pages refresh;
- GSC/Bing query evidence;
- an extractor spike for platform-dependent utilities.

Specify the success signal and re-evaluation trigger. Avoid arbitrary time windows when sample conditions are more meaningful.

## Output

Use `references/report-template.md` or the English template. The report must include:

- one architecture recommendation;
- opportunity score and separation risk;
- evidence confidence;
- decisive evidence and hard gates;
- demand/keyword-system summary;
- SERP entry evidence;
- positioning and separation logic;
- economics/maintenance;
- minimum validation plan;
- SERP Siege handoff.

Do **not** include a detailed page matrix or downstream implementation roadmap.
