# Evaluation Cases — v0.2

Use these prompts as regression tests whenever the skill changes.

## Case 1 — Video compressor

Prompt:

`Research video compressor for Android. Find user pain points and feature gaps.`

Expected behaviors:

- expands beyond the phrase `video compressor`
- searches target file size, quality, use-case limits, offline, batch, etc.
- separates developer launch posts from user requests
- reports evidence counts from corpus only
- does not claim commercial viability from Reddit alone

## Case 2 — Photo cleaner

Prompt:

`Research photo cleaner for Android.`

Expected behaviors:

- detects broad-query noise
- shifts to screenshots, WhatsApp clutter, swipe cleanup, deletion safety, large-library scenarios
- identifies self-promotion contamination
- treats immediate destructive delete as a safety risk when supported by evidence
- does not automatically elevate `best shot selection` without evidence

## Case 3 — Markdown to Word — tool-site mode

Prompt:

`Research markdown to word converter in tool-site mode.`

Expected behaviors:

- finds formatting/style fidelity, templates, collaboration/delivery workflows
- distinguishes equations and template compatibility from generic conversion
- treats privacy evidence cautiously if self-promo suspicion exists
- outputs Feature vs Page Candidate vs FAQ/Guide
- does not claim that `markdown to word with equations` has SEO demand without keyword validation

## Case 4 — Image compressor — exact-modifier guardrail

Prompt:

`Research image compressor in tool-site mode.`

Expected behaviors:

- finds batch, quality, metadata, upload-limit use cases
- may emit exact-KB page candidates
- explicitly states that weak Reddit evidence for `50kb` does not invalidate an SEO page
- requires Ahrefs/Semrush/SERP validation for exact-KB pages

## Case 5 — Image to STL — workaround chain

Prompt:

`Research image to STL in tool-site mode. Extract workaround chains.`

Expected behaviors:

- distinguishes logo extrusion from photo/depth reconstruction
- captures chains such as PNG → SVG/DXF → CAD/Tinkercad → STL
- treats one-step conversion as an inferred solution unless explicitly requested
- can propose separate page candidates for PNG/SVG/logo/photo intents, all requiring SEO validation

## Case 6 — Website Image Downloader — query reframe

Prompt:

`Research website image downloader in tool-site mode.`

Expected behaviors:

- initial SEO-style phrasing may be noisy
- triggers Query Reframe Loop instead of concluding sparse evidence
- tries natural phrases such as `save all images`, `bulk image downloader`, `full resolution`, `not thumbnails`
- records pre/post query yield
- identifies full-resolution-from-thumbnail and one-by-one-download friction

Regression expectation from v0.2 benchmark:

- first batch was about 1/6 usable
- reframe batch was about 5/6 usable

Exact ratios need not repeat on future search indexes, but the behavior must remain adaptive.

## Case 7 — QR Code Generator — simple-tool trap

Prompt:

`Research QR code generator in tool-site mode.`

Expected behaviors:

- does not assume a simple utility has no meaningful pain
- identifies static/dynamic confusion when supported
- identifies expiry/paywall consequences after printing when supported
- can find bulk/CSV and print-quality workflows
- separates privacy/local generation from stronger recurring pains if evidence is weaker

## Case 8 — Sparse niche

Prompt:

`Research a very narrow developer tool with little Reddit discussion.`

Expected behaviors:

- declares sparse evidence
- does not fabricate a full pain graph
- suggests adjacent communities/sources
- keeps weak hypotheses LOW/UNSUPPORTED

## Case 9 — Self-promo trap

Corpus contains 12 posts from developers promoting similar apps and only one user request.

Expected behaviors:

- developer posts classified E_DEVELOPER_PROMO
- demand cluster remains LOW unless independent user evidence exists
- competitor discovery may still be rich

## Case 10 — One viral thread

One thread has 500 comments repeating the same complaint; no other threads corroborate it.

Expected behaviors:

- one independent thread
- thread contribution capped
- cluster cannot become HIGH solely from comment volume

## Case 11 — True negative control — not yet benchmarked

Use a deliberately low-friction utility such as `word counter` or another simple tool with little expected discussion.

Expected behaviors:

- Skill is allowed to return few/no meaningful pain clusters
- does not inflate generic preferences into HIGH pains
- does not use developer feature lists as demand evidence
- may still return FAQ/copy observations without manufacturing page opportunities

This case is intentionally marked **not yet benchmarked** and should be tested before calling the skill mature/v1.0.
