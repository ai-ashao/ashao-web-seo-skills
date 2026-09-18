# ashao-web-seo-skills

Web building and SEO Skills curated by [ashao](https://github.com/ai-ashao).

This repository keeps only workflows that benefit from fixed evidence contracts, deterministic validation, or a genuinely separate decision stage. More Skills are not inherently better; unnecessary Skills constrain normal model reasoning and create routing overlap.

## Active Skills (6)

| Skill | Core question |
|---|---|
| `site-opportunity-scorecard` | **WHERE** should the opportunity live: site, section, page, or nowhere yet? |
| `serp-siege` | **WHAT** Page Families and SEO MVP entrances should be built first? |
| `reference-website-builder` | **HOW** should reference patterns be analyzed, prototyped, or adapted? |
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
Idea -> site-opportunity-scorecard -> serp-siege -> reference-website-builder
     -> technical-seo-audit -> helpful-value-audit -> launch/iterate
```

Use `web-asset-pipeline` only when production visual assets need processing or provenance.

## New-Skill gate

Prefer a profile/reference or normal reasoning unless at least two are true:

1. the model repeatedly makes the same high-impact mistake without the Skill;
2. the workflow needs deterministic scripts/validators/evidence contracts;
3. it is a genuinely separate decision stage rather than a niche variant.
