# Pain Mining Skill v0.3

A Codex/Skills-compatible workflow for mining evidence-backed user pains from public discussions, with a dedicated **tool-site mode** for SEO utilities.

## Typical prompts

- `Use pain-mining to research markdown to word converter in tool-site mode.`
- `Mine user pain for image compressor and classify findings as Feature vs SEO Page Candidate.`
- `Research image to STL. Extract workaround chains and page candidates.`
- `Research chart maker. If Reddit wording remains weak after one reframe, use bounded source widening.`
- `Research text case converter as a negative control; do not manufacture pains.`

## What changed in v0.3

v0.3 adds a second tool-site benchmark covering:

- Color Palette Generator
- Chart Maker
- Pinterest Board Downloader
- Background Remover
- JSON Formatter
- Word Counter
- Text Case Converter (true low-friction control)

Key changes:

1. **Evidence Shape** — every run ends as `BROAD`, `NARROW`, or `SPARSE`.
2. **Pain Density** — query relevance is separated from actual user-origin pain evidence.
3. **Source Widening Gate** — after one failed task-language reframe, switch evidence lane instead of endlessly rewriting Reddit queries.
4. **Ecosystem Reframe** — professional tools may be discussed via products/libraries (Flourish, Plotly, VS Code, jq) rather than generic category nouns.
5. **Negative-control behavior** — relevant search results with little pain are allowed to remain sparse.
6. Existing v0.2 guards remain: self-promo scores zero, workaround chains are explicit, and PAGE_CANDIDATE still requires downstream SEO validation.

## What it intentionally does not do

- keyword-volume validation
- revenue estimation
- SERP difficulty scoring
- automatic build/no-build verdicts

Use Ahrefs/Semrush/SERP/competitor Top Pages as downstream validation for any `PAGE_CANDIDATE`.
