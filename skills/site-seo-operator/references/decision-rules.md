# Prioritization, anti-spam, safety

## Decision order

1. Verified production defects that prevent intended public pages from being reachable/indexable (`P0/P1` from `$technical-seo-audit`). Review route policy first; a deliberate `noindex` is not a defect.
2. Known working pages with meaningful first-party GSC impressions and fixable intent/function/content gaps. An aggregate position of 8–20 suggests investigation, not an automatic rewrite.
3. Improving proven pages with weak task completion or uncovered subquestions, tested by `$helpful-value-audit` or equivalent functional review.
4. New indexable page intents only after first-party demand or competitor validated searches + distinct task + reusable capability + existing-page conflict check.
5. Cosmetic metadata polish and broad unvalidated content production last.

Within a tier, rank expected qualified-click/user-benefit opportunity, evidence quality, implementation hours, regression risk and reversibility. Do not use fake precision (e.g. a calculated "SEO score" from arbitrary numbers).

## Page decision gates

For each candidate, return exactly one `OPTIMIZE_EXISTING`, `BUILD`, `MERGE_REVIEW`, `HOLD`, `EXCLUDE`:

- `OPTIMIZE_EXISTING`: already serves canonical intent; evidence warrants a specific improvement. Keep its current URL unless an independent migration review approves otherwise.
- `BUILD`: distinct user task and query intent, enough documented demand, functional solution, verified facts, internal-link source and indexability gate.
- `MERGE_REVIEW`: overlapping URLs/keywords, needs SERP and canonical review before action.
- `HOLD`: unclear demand, low usefulness, source gap, non-core function, incomplete public release or not enough time since launch.
- `EXCLUDE`: intentionally non-public routes, unsafe/unsupported functions, or redundant keyword permutations with an accepted canonical target.

Keyword defaults such as Volume >= 1k and KD < 30 are opportunity research preferences, not automatic output gates. Prefer user task over mechanically multiplying pages, locales, extensions or parameter variants.

## Growth and monetization profiles

- `ads-tool`: qualified search demand, fully working tool, user experience, useful repeatable page model and measured advertising outcomes when available. Avoid ad layouts blocking the workbench, unsolicited popups and speculative revenue models.
- `saaS`: paid funnel and qualified conversion metrics when reliable. Do not apply SaaS "vs" and alternative-page factories to an ad-first tool by default.
- `hybrid`: classify at the URL/page level; public tools may index while authenticated app/transaction/system routes remain excluded.

Never turn planned future payments, ads, subscriptions or localization into production claims. No new feature or commercial claim without source-code/product confirmation.

## Anti-regression and link safeguards

- Never promise "rank in 30 days", mechanically resubmit unchanged pages, produce forced keyword density, generate fabricated reviews/FAQ schema or buy links.
- No automatic paid backlinks, mass directory submission, unsolicited outreach, social posting, email, account creation or hidden reciprocal linking.
- No automatic indexation flips, URL deletions/redirects, canonicals or hreflang edits without a migration plan with source evidence and reviewer signoff.
- Follow the destination repo `AGENTS.md` for tests and prohibited functionality. For multilingual properties, protect all language variants and hreflang reciprocity; for format references, protect authored fact/review/indexability gates.
- If the same repair fails twice, stop and report. Track a rollback before any code PR that could change a ranking page.

## Site review cadence

- New sites: baseline at launch; avoid treating a few zero-data weeks as failure. After roughly three months of GSC evidence, choose which existing site/page model to thicken and which to leave alone.
- Mature sites: weekly exceptions/opportunities and monthly outcome review.
- Cross-site comparison: choose a consistent date/window/country where possible; distinguish qualified traffic from platform-specific estimated traffic; never assume site age proves authority or indexing.
