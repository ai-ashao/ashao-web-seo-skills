---
name: ai-citation-research
description: Research how a website appears in AI/web-search source sets. Use when comparing a site against sources surfaced for natural-language user questions, finding repeated competitor pages, and turning the gaps into a small SEO/GEO action plan.
---

# AI Citation Research

Run a lightweight source-gap study for one website. This is research, not a ranking guarantee and not a productized GEO tool.

## Input

Require only:

- target domain;
- primary market/language;
- short description of what the site helps users do.

Use existing site pages and prior research when available. Do not require the user to manually prepare keywords first.

## Workflow

### 1. Build the query set

Create 30 natural-language questions by default. Use 50 only when the topic clearly needs broader coverage.

Cover several real user intents, such as:

- how-to;
- troubleshooting;
- tool/recommendation;
- comparison or alternative;
- safety/legality/compatibility when relevant;
- product/category-specific questions.

Write questions the way a person would ask an AI assistant, not as a list of SEO keywords.

Save the query set before testing. Reuse the exact same set for later before/after comparisons.

### 2. Test the questions

Use current web/AI search capabilities available in the environment. For each query, record the surfaced source pages without filtering out competitors or weak results.

Capture:

- query;
- intent category;
- engine/surface used;
- cited/surfaced domain;
- source URL;
- source title;
- whether the target domain appeared;
- test date.

Do not claim that a web-search source set is the same as the final citations shown to every ChatGPT, Gemini, Claude, or other AI user.

### 3. Build the source graph

Summarize:

- target-domain appearance count;
- appearance rate across the tested query set;
- most frequent competing domains;
- most frequently repeated competing URLs;
- intent categories where the target site appears often;
- intent categories where it is absent or weak.

Call the main metric **source appearance rate** or **search-source appearance rate** unless the environment truly measured final AI citations. Do not label it "ChatGPT citation rate" by default.

### 4. Diagnose gaps

For missing or weak queries, compare the likely intent with the target site's existing pages.

Classify each opportunity as one of:

1. **Expand existing page** — the site already has the right page but intent coverage is incomplete.
2. **Create new page** — the intent is distinct enough to deserve its own durable page.
3. **Add FAQ/section only** — the query is useful but too narrow for a standalone page.
4. **No action** — low-value, off-topic, redundant, or unsupported by evidence.

Prefer expanding an existing relevant page over creating a new page.

Also note technical mismatches when visible, especially:

- wrong locale surfacing for an English query;
- canonical/hreflang ambiguity;
- unclear page title/H1 intent;
- useful content hidden behind JavaScript or weak crawlable HTML;
- orphaned or weakly linked supporting pages.

### 5. Produce a small action plan

Prioritize only the clearest actions. Default to 3–7 recommendations, not a large backlog.

For each recommendation include:

- affected query/intention cluster;
- evidence from the source study;
- existing page if one exists;
- action type: expand / new page / FAQ / technical fix;
- priority: P0 / P1 / P2.

Do not recommend mass content creation just because many queries exist.

### 6. Save the research

Produce three files:

`YYYY-MM-DD-queries.csv`

```text
query,category,market,language,tested_at
```

`YYYY-MM-DD-sources.csv`

```text
query,category,engine,cited_domain,cited_url,cited_title,target_site_appeared,tested_at
```

`YYYY-MM-DD-report.md`

The report should contain:

- scope and method;
- query coverage summary;
- source appearance rate;
- top competing domains and repeated URLs;
- strongest intent clusters;
- weakest/missing intent clusters;
- content/technical gaps;
- prioritized action plan;
- methodology caveat.

When the user's Google Drive project folder is available, save under:

```text
<site>/Research/AI-Citation/
```

Do not create extra folders unless needed.

## Guardrails

- Do not invent search volume, KD, traffic, or citation statistics.
- Do not treat one test run as a stable ranking measurement.
- Do not infer hidden chain-of-thought from AI systems; analyze only observable queries, answers, sources, and pages.
- Do not create a dashboard, database, crawler, scheduled monitor, or API integration unless the user explicitly asks for tooling.
- Do not modify the target website during this research Skill. End with an action plan for review or handoff to the implementation agent.
- Preserve the original query set so later retests are comparable.

## Finish

Report the three saved artifacts and the 3–5 most important findings. Keep the conclusion decision-oriented: what to change now, what not to change, and what should be retested after deployment.
