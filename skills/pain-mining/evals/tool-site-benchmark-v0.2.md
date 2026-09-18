# Tool-site Benchmark — v0.2

Date: 2026-09-18

Purpose: test whether Pain Mining generalizes to SEO-first web utilities and identify failure modes before treating the skill as mature.

## Seeds

1. Markdown to Word Converter
2. Image Compressor
3. Image to STL
4. Website Image Downloader
5. QR Code Generator

## Aggregate result

- Initial queries: 30
- Initial GOOD/OK queries: 22
- Initial usable-query rate: 73.3%
- Website Image Downloader adaptive reframe queries: 6
- Reframe GOOD/OK queries: 5
- Total queries including reframe: 36
- Primary threads fetched: 20
- User-origin primary threads: 17
- Developer-promo or ambiguous primary threads: 3

These are research-process diagnostics, not market statistics.

## Main findings

### Markdown to Word

The recurring problem is not generic conversion alone. User-origin evidence points to formatting/style fidelity, numbered headings, list indentation, corporate templates, cover pages/footers, equations, and collaboration workflows.

### Image Compressor

Useful clusters include batch compression, acceptable visual quality, metadata preservation, and destination upload limits. Exact-KB pages can still be SEO-native even when Reddit discussion for a literal number such as 50KB is sparse.

### Image to STL

This seed produced the strongest workaround-chain evidence. A common pattern is:

`PNG → SVG/DXF converter → Tinkercad/Fusion/Onshape → extrude → STL`

The chain is strong product-design evidence for collapsing multiple steps into one tool, but it is not search-volume proof.

### Website Image Downloader

The initial SEO-like wording performed badly: about 1/6 queries were useful. Reframing into natural user language such as `save all images`, `bulk image downloader`, `full resolution`, and `not thumbnails` recovered about 5/6 useful queries.

This seed directly motivated the Query Reframe Loop.

### QR Code Generator

This was intended as a simple-tool negative control, but it produced genuine pains: static/dynamic confusion, hosted-redirect expiry/paywall risk after printing, bulk generation, editable destinations, scan tracking, print quality, and privacy.

Therefore “simple utility” is not a valid proxy for “low-pain utility.”

## v0.2 changes derived from the benchmark

1. Add Query Reframe Loop.
2. Separate SEO/user phrasing.
3. Add tool-site action classification: FEATURE, PAGE_CANDIDATE, HOMEPAGE_COPY, FAQ_GUIDE.
4. Extract workaround chains explicitly.
5. Keep PAGE_CANDIDATE separate from keyword/SERP validation.
6. Make E_DEVELOPER_PROMO always score 0.
7. Compute confidence only from independent user-origin A/B/C threads.
8. Preserve a true negative-control case for later testing.

## Remaining maturity gap

v0.2 is a tool-site beta, not v1.0. A true negative-control utility and a second cross-category benchmark batch are still required before calling the skill mature.
