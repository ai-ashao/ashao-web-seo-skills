# downloader-opportunity-radar v3

A reusable Agent Skill for finding downloader/save/export SEO niches where genuinely young domains can rank **and** the full intent cluster shows attributable demand.

## What v3 fixes

### 1. Single-keyword undercounting

v2 could validate `{platform} downloader` without systematically expanding variants such as:

- `{platform} download`
- `download {platform}`
- `{platform} video downloader`
- `download {platform} video`
- `download video {platform}`

v3 requires a full **Intent Permutation Set** before sizing the niche.

### 2. Domain-traffic overclaiming

v3 separates:

- Domain Monthly Visits
- Search Share
- Organic Traffic Estimate
- Target Cluster Traffic

A 200K domain is not a 200K niche unless top keywords/pages attribute that traffic to the target cluster.

### 3. Global downloader demand

v3 no longer assumes US/English tells the whole story. Locale expansion is evidence-led from top regions and country keyword data.

### 4. PROVEN BREAKOUT

A TEST NOW niche can be upgraded to `PROVEN BREAKOUT` when a young domain has strong target-cluster traffic proof, not merely a high headline visit number.

### 5. Policy shock

Recent platform changes that make the downloader dependent on prohibited access/circumvention are explicitly screened.

## Domain-age standard

- **<=6 months:** STRONG_FRESH.
- **6–12 months:** FRESH.
- **12–18 months:** WEAK_FRESH, WATCH support only.
- **>18 months:** OLD, no new-site proof.

## Package

- `SKILL.md` — main workflow.
- `references/scoring.md` — v3 100-point scoring model.
- `references/evidence-rules.md` — age, SERP, traffic, policy evidence rules.
- `references/keyword-templates.md` — full intent-permutation framework.
- `references/traffic-proof.md` — traffic attribution/sanity-check guidance.
- `templates/report.md` — required v3 report.
- `scripts/generate_keywords.py` — deterministic intent-permutation generator.
- `scripts/traffic_sanity_check.py` — directional traffic reconciliation helper.
- `scripts/score_candidate.py` — v3 scorer with age/traffic/policy gates.
- `scripts/validate.py` — regression validator for permutations and decision gates.
- `fixtures/*.json` — deterministic calibration cases.
- `examples/example-report.md` — fictional format example.

## Suggested prompts

- `Run Downloader Opportunity Radar v3 from scratch. Find 30 candidates, expand the full core intent permutations, and deeply validate the best 10.`
- `Find PROVEN BREAKOUT downloader opportunities where a <=6 month domain already ranks and target-cluster traffic is >=10K/month.`
- `Do not size any niche from a single keyword. Report Core Intent Cluster demand and locale opportunities.`
- `Run the radar for Threads-like emerging platform downloaders and require traffic attribution sanity checks.`
