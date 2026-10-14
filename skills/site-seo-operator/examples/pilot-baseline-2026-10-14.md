# Read-only pilot baseline — 2026-10-14

Scope: public response spot-check plus authorized repository read; **not** a complete crawl, GSC audit, Google indexation check, deploy or source SHA-to-production match. No product-code changes.

## WorkshopFetch

- `OBSERVED` Public home: https://workshopfetch.com/ — working Steam Workshop item lookup messaging; emphasizes no extra account and direct Steam URL only when Steam supplies one.
- `OBSERVED` Public robots: https://workshopfetch.com/robots.txt — `Allow: /`, points at production sitemap.
- `OBSERVED` Public sitemap: https://workshopfetch.com/sitemap.xml — extraction identifies **452 URLs** across locale, game, guide and static route families. This is **not** a Google index count.
- `OBSERVED` Public guide: https://workshopfetch.com/steam-workshop-download-not-working — already distinguishes stuck-at-zero, 100%, validation, subscription, and one-item failures; do not auto-create near-duplicate symptom pages.
- `REPO` `ai-ashao/steamworkshopdl`: `AGENTS.md`, `CURRENT_STATE.md` and `app/sitemap.ts` govern multilingual routes and `noindex` boundaries (dynamic results/base game pages excluded). The 2026-09-07 `CURRENT_STATE.md` mentions an older 438-URL sitemap; it is a dated reference, **not** evidence of a current defect.
- `UNASSESSED` GSC current period, query/page combinations, Google index status, production canonical/hreflang reciprocal audit for all locales, Ads revenue, JS tool behavior.

**Next read-only review:** obtain matching complete 28-day US/web `page` and `query` GSC exports; run `gsc_triage.py` on two adjacent windows; validate the leading candidates' canonical tasks and inspect multilingual technical audit results before proposing an SEO content PR. Do not add ads to dynamic result/error/loading views.

## FormatOdyssey

- `OBSERVED` Public home: https://formatodyssey.com/ — searchable file-format reference and two browser-local utilities.
- `OBSERVED` Public robots: https://formatodyssey.com/robots.txt — `Allow: /`, points at production sitemap.
- `OBSERVED` Public sitemap: https://formatodyssey.com/sitemap.xml — extraction identifies **50 URLs**, aligned with the authored 50-page launch pool. Count equality does not prove route HTTP/canonical/indexability correctness.
- `OBSERVED` Public example: https://formatodyssey.com/extension/pdf — a source-backed facts/opening guide with original utility link, rather than an empty extension template.
- `REPO` `ai-ashao/format-odyssey`: `AGENTS.md` and `content/release-matrix.json` require reviewed, effective-indexable pages. `docs/m5-launch-audit.md` describes an **older local-only** test; it did not prove production SEO on that date.
- `UNASSESSED` complete 50-URL production status/canonical/noindex audit, Google Page Indexing/GSC rankings, current deployed SHA, functional end-to-end browser tests, and monetization metrics.

**Next read-only review:** run bounded `$technical-seo-audit --profile toolsite --site --max-pages 100` against production from a network with public DNS resolution and verify GSC Page Indexing. Validate released vs draft/non-indexable route consistency before considering any extension pool expansion. Do not automatically release the 200 planned candidate formats or add advertising.

## Decision/status

| Site | Next decision | Source dependency | Production code changes |
| --- | --- | --- | --- |
| WorkshopFetch | `RESEARCH`: GSC-backed existing-page optimization | two comparable GSC Performance exports + tech audit | **None** |
| FormatOdyssey | `RESEARCH`: technical release gate and indexed page verification | full 50-URL audit + GSC Indexing/Performance | **None** |

The new Skill can propose a read-only backlog without these inputs; it **cannot** claim rankings, clicks, technical passing status, or indexing where none was measured.
