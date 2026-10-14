# Site SEO Operator (v0.1)

A **post-launch coordinator**, not another technical SEO crawler or generic content-generation Skill. Extracted from the broad idea of [Illyism/seo-skills](https://github.com/Illyism/seo-skills), but adapted to an evidence-first tool-site portfolio, existing specialist Skills, and PR-only delivery.

## Install

```bash
# Run from this skill collection's root:
mkdir -p ~/.codex/skills
cp -R skills/site-seo-operator ~/.codex/skills/site-seo-operator
```

Read `SKILL.md` and configure a site-specific `seo-ops/policy.json` in **each target site's repo** with reviewed values from `examples/`. The reusable Skill and actual site operational state are separate.

## Bootstrap prompt

```text
Use $site-seo-operator in baseline/read-only mode for https://workshopfetch.com.
Read AGENTS.md and sitemap policy from ai-ashao/steamworkshopdl,
run the existing technical-seo-audit where possible, inspect GSC if connected,
and propose no more than five evidence-backed items. Do not change product code,
indexability, ads or deploy. If ready, put seo-ops/ bootstrap files in a PR for review.
```

Swap URL/repo for the FormatOdyssey example. Use its **authored release/indexability gate**; the 200-page backlog is not authorization to ship 200 pages.

## GSC CSV review (no API required)

Export the same Search Console Performance dimension for two *equal completed nonoverlapping periods* (e.g. two adjacent 28-day windows), same property, search type and filters.

```bash
python3 scripts/gsc_triage.py --dimension page --current current-pages.csv \
  --previous previous-pages.csv --output /tmp/gsc-page-review.md
python3 -B -m unittest discover -s tests -v
```

`gsc_triage.py` only produces **review flags**; it does not fetch GSC, modify a site, predict ranking movement or fill missing values. Never treat flags as proved diagnoses.

## Boundaries

- No automatic outreach/backlinks, publishing, merge, deployment or sitewide title churn.
- No replacement of technical-seo-audit, helpful-value-audit or serp-siege.
- Do not use code/report dates as evidence of today's production behavior.
- Errors, missing GSC or inaccessible URLs remain explicitly `UNASSESSED`.
- Add production integrations, scheduler and authenticated GSC adapter only through separate reviewed changes. This initial Skill runs when invoked; it does **not** independently schedule itself.
