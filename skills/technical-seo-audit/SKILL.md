---
name: technical-seo-audit
description: Run an evidence-led technical SEO audit of public URLs and bounded site inventories. Supports generic, toolsite, SaaS, hybrid, and auto profiles with page-level route classification. Checks HTTP delivery, robots directives, robots.txt, sitemaps, canonical URLs and targets, metadata, headings, static crawlable links, internal-link architecture, orphan candidates, crawl depth, sitemap/indexability/canonical consistency, duplicate template signals, JSON-LD syntax, html lang, and hreflang reachability/reciprocity. Use for technical SEO audits, SEO-first release gates, multilingual checks, crawlability/indexability reviews, and mixed tool+SaaS sites. Do not use it to claim rankings, traffic, keyword demand, HCU/helpfulness, product quality, or conversion quality without separate evidence.
---

# Technical SEO Audit

Use deterministic checks for observable facts. Keep search-intent, content quality, product value, and ranking claims outside this skill unless independently evidenced.

## Operating model

This skill has two layers:

1. **Technical SEO kernel** — rules that apply across public websites.
2. **Policy profile + route class** — determines the expected indexability of each page without forcing an entire mixed site into one behavior.

Profiles:

- `generic`: conservative; does not infer indexability for unknown routes.
- `toolsite`: SEO-first public tools and landing pages; private/system routes still excluded.
- `saas`: marketing/content/integration pages are public; auth/app/account/transactional/system routes are expected excluded.
- `hybrid`: first-class mode for free SEO tools + SaaS marketing + authenticated app routes.
- `auto`: detect a bounded site profile from route evidence; report confidence and never hide the inference.

Route classes:

`PUBLIC_TOOL`, `MARKETING`, `SEO_LANDING`, `CONTENT`, `INTEGRATION`, `DOCS`, `AUTH`, `APP`, `ACCOUNT`, `TRANSACTIONAL`, `SYSTEM`, `UNKNOWN`.

**Site profile is only a default strategy. Route class controls page-level SEO expectation.** Explicit user/product intent overrides automatic classification.

## Core evidence rules

- Audit requested URL, final redirect URL, static HTML, final-origin robots.txt, and bounded sitemaps.
- Aggregate multiple `robots` and `googlebot` meta tags; do not let later tags erase earlier restrictive directives.
- Preserve crawler-scoped `X-Robots-Tag` boundaries.
- Detect zero, duplicate-identical, and conflicting canonical declarations. Validate a single canonical target for HTTP delivery and `noindex` unless explicitly skipped.
- Do not use fixed title length, meta-description length, H1 count, heading count, or word-count thresholds as ranking pass/fail rules.
- Word count is inventory only. It does not prove thin content, helpfulness, or ranking strength.
- Script presence means rendered-DOM parity is unassessed. Do not infer parity from static word count.
- Validate hreflang using Google-compatible language/script/region structure, self-reference, bounded target reachability, `noindex`, reciprocity, and cluster completeness. `x-default` remains optional.
- Treat JSON-LD syntax as observable; schema truthfulness/eligibility remains review work.
- Never claim Google indexation, GSC coverage, rankings, traffic, crawl frequency, field CWV, or demand from public HTML fetches.

## SEO-first site mode

Use site mode for release audits, tool sites, SaaS marketing sites, or hybrid sites:

```bash
python3 -B scripts/audit.py https://example.com \
  --profile hybrid \
  --site \
  --max-pages 200
```

For a known toolsite:

```bash
python3 -B scripts/audit.py https://example.com \
  --profile toolsite \
  --site
```

For a known SaaS:

```bash
python3 -B scripts/audit.py https://example.com \
  --profile saas \
  --site
```

When the site type is unknown or mixed:

```bash
python3 -B scripts/audit.py https://example.com \
  --profile auto \
  --site
```

Site mode combines sitemap inventory with a bounded same-origin static crawl. It reports:

- route class and expected indexability per checked URL;
- orphan candidates (`sitemap URL + zero observed static indegree`) with explicit bounded-crawl limits;
- crawl depth from the root for discoverable URLs;
- broken and redirecting internal links;
- internal links to URLs that canonicalize elsewhere;
- sitemap URLs that redirect, return non-200, are `noindex`, or canonicalize elsewhere;
- conflicting canonical declarations and canonical collisions;
- duplicate titles/H1/meta descriptions across expected-indexable pages;
- expected-indexable scripted pages missing static title/H1 as rendered-parity review candidates;
- public routes accidentally `noindex` and private/app routes returning 200 without `noindex`.

## Page mode and explicit overrides

For one route:

```bash
python3 -B scripts/audit.py https://example.com/tools/pdf \
  --profile hybrid \
  --route-class PUBLIC_TOOL \
  --indexability expected
```

`--indexability` accepts `auto`, `expected`, or `excluded`. Avoid a hidden boolean default: if route intent cannot be safely inferred, keep it unassessed.

Use `--multilingual --validate-hreflang` only when multilingual delivery is expected. Multilingual is not assumed merely because the portfolio often uses it.

## Priority model

Keep evidence labels separate from business impact.

- `OBSERVED`: directly fetched/parsed evidence.
- `REVIEW`: requires intent or semantic judgement.
- `UNASSESSED`: unavailable from current evidence.

SEO-first site findings use:

- `P0`: confirmed release blocker for a route expected to rank, e.g. unintended `noindex`.
- `P1`: material discoverability/indexability/architecture defect, e.g. private route indexability leak, orphan sitemap page, sitemap noindex, conflicting canonical, broken internal link, internal noncanonical link.
- `P2`: meaningful cleanup or template risk, e.g. redirecting internal links or duplicate metadata.
- `P3`: optional polish/hypothesis.

Do not promote schema polish, generic image-alt advice, or arbitrary metadata-length edits above crawl/index/canonical/internal-link defects.

## Mixed SaaS + tool sites

Do not classify the whole site as either “SEO site” or “app.” Example:

```text
/                         MARKETING      -> expected indexable
/tools/image-downloader   PUBLIC_TOOL    -> expected indexable
/features/bulk-download   MARKETING      -> expected indexable
/solutions/ecommerce      SEO_LANDING    -> expected indexable
/guides/...               CONTENT        -> expected indexable
/pricing                  MARKETING      -> expected indexable
/login                    AUTH           -> review / explicit policy
/dashboard/...            APP            -> expected excluded
/settings                 ACCOUNT        -> expected excluded
/api/...                  SYSTEM         -> expected excluded
```

This route-level model is the default for `hybrid` and the preferred architecture for mixed acquisition + SaaS products.

## Safe retrieval boundary

The bundled fetcher allows only public HTTP(S) URLs on ports 80/443, rejects private/loopback/link-local/multicast/reserved destinations, revalidates redirects, caps response bytes, and never sends credentials. This reduces SSRF risk but is not a complete network-security boundary; run untrusted audits with outbound controls.

## Adjacent work

Route separately:

- Search demand, SERP competition, keyword mapping -> SERP/keyword evidence workflow.
- HCU/helpfulness/user value -> helpful-value audit.
- Product UX, trust, monetization, conversion -> product/site scorecard.
- Image optimization and asset rights -> web asset pipeline.
- Rendered DOM, interaction, visual validation, CWV -> browser/performance tooling.
- GSC index coverage and query performance -> Search Console evidence.

## Completion standard

A complete report states target, requested/effective profile, route class, expected indexability, deterministic evidence, site-mode findings when requested, evidence limits, and exact re-check method. Automatic profile/route inference must be visible in the report, never silently treated as product truth.
