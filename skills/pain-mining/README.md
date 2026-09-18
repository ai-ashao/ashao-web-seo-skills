# Pain Mining Skill v0.2

A Codex/Skills-compatible workflow for mining evidence-backed user pains from Reddit and similar public discussions, with a dedicated **tool-site mode** for SEO utilities.

## Typical prompts

- `Use pain-mining to research markdown to word converter in tool-site mode.`
- `Mine user pain for image compressor and classify findings as Feature vs SEO Page Candidate.`
- `Research image to STL. Extract workaround chains and page candidates.`
- `Research website image downloader. If initial queries are noisy, reframe them into natural user language.`

## What changed in v0.2

v0.2 is based on a five-seed tool-site benchmark:

- Markdown to Word
- Image Compressor
- Image to STL
- Website Image Downloader
- QR Code Generator

Key changes:

1. **Query Reframe Loop** — weak SEO/product-term queries are rewritten into natural task language before declaring sparse evidence.
2. **Tool-site action classification** — findings are mapped to `FEATURE`, `PAGE_CANDIDATE`, `HOMEPAGE_COPY`, or `FAQ_GUIDE`.
3. **Workaround chains** — multi-tool/manual workflows are extracted explicitly.
4. **SEO guardrail** — Reddit can generate page candidates but cannot validate keyword volume or SERP opportunity.
5. **Tool-specific intent expansion** — fidelity, exact constraints, batch, destination limits, compatibility, extraction edge cases, and export hand-off.
6. **Benchmark metrics** — query yield and reframe recovery are tracked.

## What it intentionally does not do

- keyword-volume validation
- revenue estimation
- SERP difficulty scoring
- automatic build/no-build verdicts

Use Ahrefs/Semrush/SERP/competitor Top Pages as downstream validation for any `PAGE_CANDIDATE`.
