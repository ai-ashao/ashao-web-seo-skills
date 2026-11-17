# ashao-web-seo-skills

Web building and SEO Skills curated by [ashao](https://github.com/ai-ashao).

This repository keeps only workflows that benefit from fixed evidence contracts, deterministic validation, or a genuinely separate decision stage. More Skills are not inherently better; unnecessary Skills constrain normal model reasoning and create routing overlap.

## Active Skills (9)

| Skill | Core question |
|---|---|
| `pain-mining` | **PAIN** what recurring problems, workarounds, and product gaps are users actually reporting? |
| `site-opportunity-scorecard` | **WHERE** should the opportunity live: site, section, page, or nowhere yet? |
| `serp-siege` | **WHAT** Page Families and SEO MVP entrances should be built first? |
| `competitor-seo-page-pool` | **POOL** which canonical page intents from supplied competitor exports should be built, optimized, reviewed, or deferred, and in what reproducible order? |
| `reference-website-builder` | **HOW** should reference patterns be analyzed, prototyped, or adapted? |
| `ui-art-direction-loop` | **POLISH** which visible UI problems remain after independent screenshot review, fixes, and same-scene rechecks? |
| `technical-seo-audit` | **CRAWL** can search engines correctly discover/crawl/index the public surface? |
| `helpful-value-audit` | **VALUE** does the page genuinely complete the user's task? |
| `web-asset-pipeline` | **ASSETS** how should production visuals be prepared, tracked, and integrated? |

## Consolidated / retired

- `downloader-opportunity-radar` -> `site-opportunity-scorecard` downloader profile.
- `competitive-ui-reverse-engineering` -> `reference-website-builder` analyze mode.
- `adapt-reference-site` -> `reference-website-builder` adapt mode.
- `website-audit-scorecard` -> retired; use specialist audits and normal model synthesis instead of another aggregate score.
- `ai-citation-research` -> retired from the core set; run as ad-hoc research unless recurring measurement justifies a dedicated workflow.

## Default workflow

```text
Idea / problem -> pain-mining (when pain/workaround evidence is needed)
              -> site-opportunity-scorecard -> serp-siege
              -> competitor-seo-page-pool (when structured exports need a canonical instance pool)
              -> reference-website-builder
              -> ui-art-direction-loop (existing UI polish, when needed)
              -> technical-seo-audit -> helpful-value-audit -> launch/iterate
```

`pain-mining` is a pre-SEO evidence stage. It can surface user pain, workaround chains, feature gaps, and `PAGE_CANDIDATE`s, but it must not treat Reddit recurrence as keyword demand. Validate page candidates downstream with competitor exports, Ahrefs/Semrush, and SERP evidence.

`competitor-seo-page-pool` is the narrow structured-export path. Use it when Top Pages and Positions files already exist and repeated runs need a stable canonical intent pool. Use `serp-siege` for broader live research and product/SEO roadmaps; do not run both by default.

Use `web-asset-pipeline` only when production visual assets need processing or provenance.

Use `ui-art-direction-loop` to refine an existing site's UI with fixed screenshots and a screenshot-only art-director subagent. It preserves the site's product/brand scope, separates visual findings from functional verification, and does not grant release permission. Use `reference-website-builder` for reference analysis, prototypes, or adaptations instead.

## New-Skill gate

Prefer a profile/reference or normal reasoning unless at least two are true:

1. the model repeatedly makes the same high-impact mistake without the Skill;
2. the workflow needs deterministic scripts/validators/evidence contracts;
3. it is a genuinely separate decision stage rather than a niche variant.
