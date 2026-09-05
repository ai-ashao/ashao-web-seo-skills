# Evidence and Interpretation

## Evidence labels

| Label | Meaning | Examples |
| --- | --- | --- |
| `OBSERVED` | Direct response/parser evidence. | HTTP 200, `noindex`, canonical target, orphan candidate within the bounded graph. |
| `REVIEW` | Needs product/SEO context. | Whether consolidation is intentional; whether docs should index; query intent. |
| `UNASSESSED` | Cannot be established from current evidence. | GSC index coverage, rendered parity, crawl frequency, field CWV. |

## Severity discipline

| Priority | Use only when | Examples |
| --- | --- | --- |
| `P0` | Confirmed unintended blocker affects a route expected to rank. | Public tool/landing page has `noindex`. |
| `P1` | Material discoverability/indexability/architecture defect. | Private app route indexability leak, orphan sitemap page, conflicting canonical, sitemap noindex, broken internal link. |
| `P2` | Meaningful cleanup/template risk. | Redirecting internal links, duplicate titles across public template pages. |
| `P3` | Optional polish or hypothesis. | Non-critical schema or wording cleanup. |

Priority requires route intent. Site profile alone is not enough.

## Interpretation rules

- Multiple robots/meta directives are aggregated; restrictive directives must not be overwritten by later tags.
- Conflicting canonical tags are defects to investigate; a single canonical target should be fetched and checked for clean delivery/noindex.
- Canonical absence is not automatically a failure, but SEO-first template pages should be reviewed for duplicate URL variants.
- Sitemap URLs should represent intended canonical public URLs. Redirect/noindex/noncanonical sitemap entries are architecture findings.
- Orphan status means “sitemap URL with zero observed static indegree in the bounded crawl,” not proof of zero links anywhere on the web or in rendered DOM.
- Crawl depth is an observation. Do not invent a universal maximum depth rule.
- Internal-link status/redirect/canonical checks outrank generic image-alt or schema polish in SEO-first release work.
- Hreflang validation covers supported structural form, self-reference, reachability, noindex, reciprocity, and bounded cluster completeness. It does not prove international targeting success.
- Script presence leaves rendered parity unassessed. If an expected-indexable scripted page lacks static title/H1, prioritize browser verification.
- Duplicate metadata is a template-risk signal, not automatic proof of duplicate content.
- Private/app routes without `noindex` are high priority under SaaS/hybrid policy, but access control and product intent still matter.
- Do not evaluate target-query alignment without a supplied query, live SERP evidence, or GSC evidence.
