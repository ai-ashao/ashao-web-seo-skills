# Tool-site Benchmark — v0.3

Date: 2026-09-18

Purpose: extend the v0.2 benchmark across more SEO-first tool types, test low-friction controls, and identify when Reddit should stop being the only evidence lane.

## Seeds

1. Color Palette Generator
2. Chart Maker
3. Pinterest Board Downloader
4. Background Remover
5. JSON Formatter
6. Word Counter
7. Text Case Converter — true low-friction control

## Search work

- Initial queries: 34
- Adaptive reframe queries: 10
- Total search queries: 44
- Representative primary Reddit threads fetched: 20
- User-origin primary threads in fetched sample: 19
- Developer-promo primary threads in fetched sample: 1

Query-yield ratios are search-index dependent and should be treated as process diagnostics, not market statistics.

## Seed findings

### Color Palette Generator

The generic category is discussable on Reddit, but evidence is fragmented across several jobs:

- lock existing primary/secondary colors while generating semantic system colors
- improve a client's imperfect seed colors without replacing them entirely
- extract dominant colors from an image
- build accessible sequential palettes
- export/developer workflow appears frequently in developer posts but needs stronger user-origin evidence

Observed shape: **NARROW** in the benchmark sample. Multiple real jobs exist, but recurrence by pain cluster was limited.

### Chart Maker

Generic `chart maker` phrasing performed poorly. Reframing to `make a chart`, CSV, export, and embed language improved discovery only partially.

The strongest user-origin evidence appeared through **ecosystem language**, not the generic category:

- Flourish: easy and customizable, but image download moved behind a premium tier
- Plotly: simple charts become cumbersome when real customization is required

Observed shape on Reddit alone: **SPARSE**.

This seed directly motivated the **Source Widening Gate** and **Ecosystem Reframe**. Further work should use data-visualization communities, product-specific discussions, GitHub Issues, or other professional workflow sources rather than a third round of generic Reddit queries.

### Pinterest Board Downloader

SEO-style `Pinterest board downloader` phrasing was weak. Platform-native language was much better:

- `mass download pins`
- `download boards quickly`
- `save pins offline`
- `high resolution`

Strong user-origin jobs included:

- backing up thousands of references because users fear account/pin loss
- avoiding one-by-one downloads
- obtaining original/high-resolution images
- avoiding free-tool download caps
- preserving board organization/folders

Observed shape: **NARROW**, concentrated around bulk backup/download plus quality/limit subproblems.

### Background Remover

This category produced consistently strong task evidence:

- hair/fingers/small-gap edge failures
- ghost halos and accidentally removed foreground details
- batch processing for 100+ images
- local/offline processing to avoid server/subscription dependency
- retaining natural product shadows while removing the background
- users using GIMP/manual masking as workarounds

The benchmark confirmed that quality/fidelity and batch workflow are more useful research branches than generic `free background remover` wording.

Observed shape in the fetched sample: **NARROW**, with several distinct high-value branches that warrant deeper sampling before calling the category BROAD.

### JSON Formatter

Generic `JSON formatter problem` was poor, but job-specific queries worked:

- open/browse 500MB–1GB JSON that VS Code cannot handle
- compare 100k-line JSON outputs where normal diff is unreadable
- trust/privacy concerns around browser extensions after a popular formatter went closed-source and added tracking-related behavior
- local/offline processing appears often in developer positioning, so it must remain separate from user-origin evidence

Observed shape: **NARROW**.

The seed also showed that developer tools often need **ecosystem terms** such as VS Code, jq, browser extension, diff, and large-file viewer.

### Word Counter

The generic task is low-friction. Most users already have counters built into writing tools.

However, a narrower branch exists:

- keeping word/character limits visible without breaking writing flow
- assignment-specific rules for in-text citations/references/bibliography
- users searching for tools that exclude citations when their institution requires it

A developer-built citation counter appeared in the corpus and was correctly treated as promotion, not demand proof.

Observed shape: **NARROW**, because the generic tool is simple but an academic subtask has real evidence.

This invalidated Word Counter as a pure negative control.

### Text Case Converter

This seed served as the true low-friction control.

Search results were often relevant to text-case conversion, but many were:

- simple built-in shortcut answers
- one-off how-to questions
- developer/tool promotion
- already-solved uppercase/lowercase transformations

A few narrow edge cases exist (sentence/title case, definable title-case exceptions), but the benchmark did not surface a recurring multi-thread pain graph.

Observed shape: **SPARSE**.

This seed proved why **query yield must be separated from pain density**: relevant results can exist without meaningful repeated pain.

## v0.3 changes derived from the benchmark

1. Add **Evidence Shape**: BROAD / NARROW / SPARSE.
2. Add **Pain Density** as a separate corpus diagnostic from query relevance.
3. Add **Source Widening Gate** after one failed task-language reframe.
4. Add **Ecosystem Reframe** for professional/developer tools discussed through products/libraries rather than generic nouns.
5. Treat high query yield + low pain density as valid negative evidence.
6. Keep a tested true negative control: Text Case Converter.
7. Preserve all v0.2 guards: self-promo score zero, user-origin confidence only, workaround chains explicit, PAGE_CANDIDATE requires downstream SEO validation.

## Maturity assessment

v0.3 has now been exercised across:

- compressors
- cleaners
- document converters
- 2D→3D converters
- generic downloaders
- platform-specific downloaders
- QR generators
- color utilities
- chart/data-viz tools
- AI image tools
- developer tools
- word/text utilities
- a genuine low-friction negative control

It is suitable for regular tool-site research as a **beta/stable workflow**, but v1.0 should still require regression runs against all benchmark cases plus at least one non-Reddit source-widening case end to end.
