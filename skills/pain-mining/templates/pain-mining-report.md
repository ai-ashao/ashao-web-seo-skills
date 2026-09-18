# Pain Mining Report — [Seed]

## 1. Research scope

- Seed:
- Mode: general / tool_site
- Platform:
- Audience:
- Time window:
- Sources:
- Assumptions:

## 2. Corpus summary

- Queries run:
- Query reframes:
- Unique relevant threads:
- Evidence items:
- User-origin evidence (A/B/C):
- Developer-promo items:
- Ambiguous items:
- Pain density:
- Promotion contamination:
- Evidence shape: BROAD / NARROW / SPARSE
- Source widening used: Yes/No

## 3. Query performance

| Batch | Query | Framing | Relevant / Inspected | Yield | Notes |
|---:|---|---|---:|---|---|

If a reframe was triggered, show **before vs after**. A successful reframe means the original wording was poor; it does not create new demand.

If source widening ran, list each source lane separately.

## 4. Evidence shape

- Shape: BROAD / NARROW / SPARSE
- Why:
- Pain density:
- Promotion contamination:
- What this shape does **not** prove:

Use `references/evidence-shape.md`. Shape describes the observed corpus, not market size or SEO demand.

## 5. Pain Graph

```text
[Seed]
├── Pain cluster 1
│   ├── sub-pain
│   └── sub-pain
├── Pain cluster 2
└── Pain cluster 3
```

## 6. Pain clusters

| Pain | Confidence | Independent Threads | Evidence Score | Workarounds | Consequences |
|---|---|---:|---:|---:|---:|

For each HIGH/MEDIUM cluster, summarize:

- What users are trying to do
- What fails
- Consequence
- Current workaround
- What evidence does **not** establish

## 7. Representative evidence

| ID | Type | Date | User signal | Cluster | Source |
|---|---|---|---|---|---|

Prefer paraphrase + URL. Use short excerpts only when useful.

## 8. Workarounds and workaround chains

List recurring manual or multi-product workarounds.

Example:

`PNG → SVG converter → Tinkercad → extrude → STL`

For each chain, state what a one-step tool could collapse. Do not call the inferred solution a user request unless it was explicitly requested.

## 9. Product implications

| Possible feature / mechanism | Evidence level | Supported pain | Notes |
|---|---|---|---|

Labels:

- DIRECT
- INFERRED
- SPECULATIVE

## 10. Tool-site actions

Use this section when `mode=tool_site`.

| Finding | Action | Candidate query / copy | Evidence | SEO validation |
|---|---|---|---|---|

Action labels:

- `FEATURE`
- `PAGE_CANDIDATE`
- `HOMEPAGE_COPY`
- `FAQ_GUIDE`

Every `PAGE_CANDIDATE` must say `REQUIRED` under SEO validation.

## 11. Competitor discoveries

Separate developer promotion from user recommendations.

| Product | How discovered | Positioning / differentiator | Evidence type |
|---|---|---|---|

## 12. Weak / unsupported hypotheses

List tempting ideas that did not receive enough user-origin evidence.

## 13. Next validation

Pain evidence alone is insufficient for a build/page decision. Choose relevant follow-ups:

- Ahrefs / Semrush keyword demand
- Google SERP
- competitor Top Pages
- Google Play / App Store reviews
- pricing/revenue evidence
- implementation complexity
