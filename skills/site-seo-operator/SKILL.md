---
name: site-seo-operator
description: Operate a live SEO-first tool site after launch using evidence-backed GSC/analytics triage, technical audit handoffs, intent-safe optimization backlog, reviewed pull requests, and weekly/monthly learning loops. Use for recurring SEO operations, post-launch optimization, GSC performance changes, and multi-site portfolio reviews. Orchestrates existing specialist Skills; does not invent demand, promise rankings, buy links, or auto-deploy.
metadata:
  version: 0.1.0
---

# Site SEO Operator — post-launch orchestration

The owner chooses the market, product, domain and shipping policy. This Skill turns **verified production and search evidence** into a bounded backlog and reviewed, testable code changes. It is a coordinator, not another crawler, page-pool planner or article factory.

Read [state and evidence contract](references/state-and-evidence.md) and [decision rules](references/decision-rules.md) before the first run. For a new project copy an [example policy](examples/workshopfetch.json) and edit the values against the actual repository; never blindly transplant an example's project details.

## Trigger and handoff

- Trigger for **post-launch** daily/weekly/monthly SEO operations, GSC opportunity triage, indexation issues, and portfolio optimization review.
- Invoke `$technical-seo-audit` to establish technical crawl/indexability evidence. Do **not** recreate its checks or interpret its `P0/P1` as Google ranking factors.
- Invoke `$helpful-value-audit` when a real page/task or quality discrepancy is suspected; do not invent a helpfulness score.
- Invoke `$serp-siege` for fresh broad SERP research, and `$competitor-seo-page-pool` only when structured competitor exports justify a reproducible intent pool. Neither is invoked every day.
- Use existing product `AGENTS.md`, current release matrix, indexability gates, test commands and manual approvals. A repo policy overrides defaults here.
- The operator does not choose new verticals/domains, reverse an existing page-pool decision, or substitute SEO activity for product task completion.

## Input and preflight

Require a verified production domain and source repository. Attempt to collect, labeling each independently:

1. `PUBLIC`: bounded live homepage, `robots.txt`, `sitemap.xml`, representative indexable and noindex URLs, redirects, and crawl links.
2. `REPO`: current `AGENTS.md`, route/content registry, metadata/canonical/robots/sitemap implementation, release criteria, latest commit and tests.
3. `SEARCH`: first-party GSC performance, segmented by property, date, search type, country, page and/or query. Export or read source through an authorized connector. A screenshot is not an API export.
4. `OPTIONAL`: Bing Webmaster, GA4, ad dashboard or revenue, Ahrefs/Semrush and dated competitor observations. Keep channels and metric definitions separate.

Never replace missing source data with estimates or attribute traffic changes to a recent commit without a causal method. Mark each observation `OBSERVED`, `INFERRED`, `REVIEW`, or `UNASSESSED`; record its URL/file/date. Use source-system language such as "GSC clicks", not "UV".

If an input is unavailable, do not block all work. Produce a **coverage manifest** and do the supported tasks. In particular, never claim Google indexation, exact ranking, organic visitors, ad revenue or AI citations without corresponding evidence.

## Repo-local operating state

Store state **in the target site's repository** under `seo-ops/` (not inside this reusable Skill), but only via a reviewed PR:

```text
seo-ops/
  policy.json              # approved site-specific constraints, target market, ship mode
  sources.md               # source manifest, dates, granularity, unavailable inputs
  page-inventory.csv       # canonical intent ID, URL, route class, locale, index policy
  backlog.md               # prioritized proposed changes and review gates
  changes.md               # dated shipped PRs/commits, rollback and validation outcome
  snapshots/               # small dated source references; exclude credentials/raw PII
  reports/YYYY-MM-DD.md    # read-only/PR reports and evidence links
```

Read existing state before each run. Do not overwrite files owned by other operators. In a new repo, propose the initial `seo-ops/` structure as a PR and stop short of production mutations. Credentials and GSC tokens must **never** be committed.

## Cycle

### First run — baseline only

1. Read repo policy and compare production with authored routes. Determine which routes are **expected** to be indexable (including multilingual and legal/system routes).
2. Run the bounded specialist technical audit and test representative user tasks where authorized. Distinguish sitemap URL count, valid indexable pages, and **GSC indexed pages**.
3. Record a query-to-canonical-URL inventory if GSC data exists. Prevent keyword/page cannibalization; variants are not automatically pages.
4. Record the baseline and a maximum of five ranked action items. Do not alter existing public URLs, ads, the payment/product flow or the route policy.

### Daily or on-demand — exception handling

- Detect verified new P0/P1 technical defects, production outages, important code/content fact changes and regressions. Do **not** recrawl the full portfolio and rewrite titles every day by default.
- Create a bugfix PR only for clearly evidenced non-destructive P0/P1 issues. Respect repository-specific tests, build and reviewer constraints.
- If no actionable evidence or changes exist: log `NO_ACTION`, not invented work.

### Weekly — growth opportunity triage

1. Compare complete, non-overlapping GSC windows (prefer 28-day comparisons when low volume; do not use an incomplete latest day). Preserve property/market/search type/dimension.
2. Use `python3 scripts/gsc_triage.py --current <CSV> --previous <CSV> --dimension page --output <report.md>` where matching exported tables exist. Its flags are **review candidates, not automatic SEO diagnoses**.
3. Examine impression-bearing queries/pages in positions 8–20, meaningful click/CTR changes, and verified indexability problems. Inspect top SERP results **only for the exact market/query** before proposing content changes.
4. Select **at most three** work items. Default to improving a proven URL before making a new one; new URL requires independent intent, verified demand and working functionality.
5. For every work item, attach baseline, expected user benefit, PR diff, test results, measurement window and rollback conditions. Recheck the metric after data has had time to stabilize.

### Monthly — portfolio allocation

- Review **site-level** 28/90-day trends with GSC and revenue/ad data where available; do not sum Google/Bing clicks as unique people or GA4 users.
- Decide per site: `THICKEN`, `MAINTAIN`, `RESEARCH`, or `PAUSE` with cited evidence and effort estimate. A 3-month-old site with no signal is a review candidate, not an automatic deletion.
- Rebuild/extend page intent maps only when new demand evidence supports it. One query does not imply one page. Do not pad page counts.
- Report work hours, shipped improvements, outcomes, and unresolved data gaps; prefer small verified gains to content volume.

## PR and publication safety

Default `ship_mode=pr-only`. Read-only audit and report do not imply authorization to modify product code. When code changes are authorized, make a branch and PR; **never merge, deploy, publish, submit links, buy links, edit DNS, change billing or ads, or email third parties without explicit approval**. A PR cannot bypass local permission requirements.

Before any PR: verify source files and actual page behavior, run existing repository checks and tests, and report the ones not executed. Destructive operations (URL removal/redirect, `noindex`, canonicals, hreflang, legal copy, user-data handling) require a separately reviewed migration plan even if a script recommends them. Never alter unknown release gates, invent data, inflate reviews or add fake schema.

For an advertising-first tool, optimize qualified GSC clicks and functional page utility; use GA4 engagement, AdSense/RPM only when real first-party data exists. For a SaaS, use relevant qualified conversions where measured. Never make ads more intrusive solely to maximize short-term revenue.

## Required output

Every run returns:

- **Scope**: project, checked site/repo SHA, run date and mode, market/search type.
- **Evidence coverage**: named sources and dates; observed vs missing, and relevant limits.
- **Findings**: factual observations separated from hypotheses and risk.
- **Ranked backlog**: at most five items, each with `intent_id / URL / why now / proof / fix / verification / approval gate`.
- **Shipped**: PR URLs/commit IDs and actual tests, or explicitly `none`.
- **Next decision**: continue, measure, ask owner for a source export, or no action.

Do not present a draft as a deployed fix, a live URL as indexed, or a GSC click as a unique visitor.
