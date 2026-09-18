---
name: pain-mining
description: Mine evidence-backed user pain points, workarounds, feature gaps, emerging competitors, and tool-site page opportunities from Reddit and similar public discussions. Use when researching a product idea, app, SaaS, SEO tool site, feature, competitor, or market to understand what users actually struggle with. In tool-site mode, classify findings into Feature, SEO Page Candidate, Homepage Copy, or FAQ/Guide while keeping search-demand validation separate. Do not use as a substitute for keyword-volume, SERP, revenue, or market-size validation.
---

# Pain Mining

Version: 0.2

## Purpose

Turn a seed product or problem into an evidence-backed **Pain Graph** using real user discussions.

This skill is for questions such as:

- What do users hate about this product category?
- What unmet needs keep recurring?
- Why are users switching away from competitors?
- What manual workarounds are people using?
- Which feature requests are strong enough to influence an MVP?
- Are new competitors emerging around the same pain?

The skill discovers **pain evidence**. It does not decide by itself whether a product should be built.

## Core rules

1. **Short query bank > giant Boolean query.** Use many short, targeted searches instead of one complex query.
2. **Intent expansion > synonym expansion.** Expand from the product name into user jobs, situations, consequences, constraints, and workarounds.
3. **User evidence and developer promotion must be separated.** Never count self-promotion as user-demand evidence.
4. **Counts must come from the collected corpus.** Never invent frequencies, percentages, or evidence counts.
5. **Do not force a Pain Graph.** If evidence is sparse, say so and show the weak signals.
6. **Separate evidence from inference.** A user complaint is evidence; a proposed feature is an inference unless users explicitly request it.
7. **Deduplicate aggressively.** One Reddit thread with ten similar comments is not ten independent threads.
8. **Prefer recent evidence for fast-moving software markets.** Older evidence can establish persistence but must be labeled as older.
9. **Negative evidence matters.** If a suspected pain does not appear after targeted searches, mark it weak or unsupported.
10. **Pain evidence is one layer.** Recommend search-demand/SERP/store-review validation after Pain Mining when the user is evaluating a build opportunity.
11. **SEO phrasing is not user phrasing.** If product-keyword queries fail, reframe into natural task language before concluding evidence is sparse.
12. **Tool-site outputs need action classification.** In tool-site mode, separate Feature, SEO Page Candidate, Homepage Copy, and FAQ/Guide. A Page Candidate is never treated as keyword-demand proof.
13. **Workaround chains are high-value signals.** Multi-step user workflows (e.g. PNG → SVG → CAD → STL) should be extracted explicitly because collapsing them can define a useful tool.
14. **Simple tools still need negative controls.** Do not assume a simple utility has few pains; test that empirically and maintain at least one genuinely low-pain benchmark case.

## Inputs

Required:

- `seed`: product, problem, category, competitor, or job-to-be-done.

Optional:

- `mode`: `general` or `tool_site`. Infer `tool_site` when the user is researching an SEO-first web utility/converter/downloader/generator/compressor.
- `platform`: Android, iOS, web, desktop, Shopify, WordPress, etc.
- `audience`: photographers, students, developers, parents, etc.
- `competitors`: known products or brands.
- `time_window`: default 24 months for software; expand when evidence is sparse.
- `source_scope`: default Reddit-first; may include app-store reviews, forums, GitHub Issues, Product Hunt comments, or other public discussions.
- `geo/language`: when relevant.

If only a seed is supplied, proceed without blocking on clarification. Infer a reasonable initial scope and label the assumption.

## Workflow

### Phase 1 — Normalize the seed

Write a one-line research scope:

`[seed] | [platform if known] | [audience if known] | [time window]`

Identify the likely object being cleaned, converted, downloaded, organized, shared, generated, edited, stored, or purchased.

### Phase 2 — Intent expansion

Generate an **Intent Map** before searching. Expand into:

1. Core task
2. Failure/problem states
3. Consequences
4. Workarounds
5. Use cases / destinations
6. Constraints
7. Trust / privacy / permissions
8. Pricing / paywall / subscription
9. Migration / alternative / switching
10. Scale / performance
11. Safety / recoverability
12. Source-specific clutter or edge cases

When `mode=tool_site`, also expand these tool-specific dimensions:

13. Input/output fidelity — formatting, metadata, transparency, resolution, naming
14. Exact constraints — target KB/MB, dimensions, page count, file type, print size
15. Batch/scale — many files, folders, URLs, rows, pages
16. Destination constraints — email, forms, CMS, Discord, print, slicer, Office, etc.
17. Compatibility — browser, OS, file formats, legacy/new versions
18. Manual workaround chain — multiple tools, conversions, CLI steps, copy/paste
19. Extraction edge cases — thumbnails vs originals, lazy-loaded assets, redirects, embedded media
20. Export/hand-off — ZIP, SVG, DOCX styles, editable equations, filenames, folder structure

Do not assume all branches are real pains. They are search hypotheses only.

Example for `photo cleaner + Android`:

- clean gallery
- delete photos quickly
- screenshot cleanup
- WhatsApp media cleanup
- duplicate photos
- too many photos
- swipe delete / keep
- accidental deletion / recovery
- offline / on-device
- cleaner subscription / paywall
- 10k photos / large gallery

### Phase 3 — Build query batches

Read `references/query-bank.md`.

Generate 12–24 **short queries** in 2–3 batches. Prefer 3–8 meaningful terms per query.

Good:

- `site:reddit.com/r/androidapps screenshot cleanup app`
- `site:reddit.com/r/androidapps gallery cleaner undo delete`
- `site:reddit.com "video too large" Discord`
- `site:reddit.com "compress video" target file size`

Avoid as the default:

- long Boolean trees with many OR clauses
- vague product-name-only queries
- mixing too many pains in one search

Use exact phrases only when they represent natural user language.

### Phase 4 — Search and score query quality

For each query, record:

- results inspected
- relevant unique threads
- obvious noise
- self-promotion-heavy results
- framing: `PRODUCT_TERM`, `TASK_LANGUAGE`, `CONSTRAINT`, `WORKAROUND`, or `COMMUNITY_RESTRICTED`

Classify query yield:

- `GOOD`: >= 40% of inspected results are directly relevant
- `OK`: 20–39%
- `POOR`: < 20%

#### Query Reframe Loop

Do **not** conclude "no Reddit evidence" after a weak product-keyword batch.

Trigger one adaptive reframe when either:

- fewer than 40% of the batch is GOOD/OK, or
- two consecutive queries are POOR.

Reframe in this order:

1. Replace SEO/product nouns with natural task language: `download every image`, `save all images`, `turn logo into STL`.
2. Add the concrete failure or constraint: `full resolution`, `not thumbnails`, `without losing formatting`.
3. Add a user context/destination: `for Word`, `for 3D printing`, `for upload form`.
4. Restrict to a relevant community only after the task language is clear.

Run one 4–8 query reframe batch. Record pre/post yield separately. If the reframe also fails, declare sparse evidence or widen sources; do not endlessly query-spin.

### Phase 5 — Fetch primary evidence

Open/fetch the strongest relevant threads, not only search snippets.

Target for a normal run:

- 15–30 unique relevant threads, or
- 25–50 evidence items across posts/comments,

whichever comes first.

For small niches, use what exists and declare sparse evidence.

Extract only evidence that materially describes:

- a pain/problem
- a concrete consequence
- a workaround
- an unmet request
- switching behavior
- pricing friction
- privacy/trust concern
- workflow friction
- scale/performance problem
- safety/recovery concern

### Phase 6 — Classify evidence

Read `references/evidence-taxonomy.md`.

Assign each evidence item one primary type:

- `A_USER_REQUEST`
- `B_FIRSTHAND_COMPLAINT`
- `C_FEATURE_REQUEST`
- `D_RECOMMENDATION`
- `E_DEVELOPER_PROMO`
- `F_SECONDHAND_OR_AMBIGUOUS`

**E_DEVELOPER_PROMO cannot count as demand evidence.** It can only inform competitor/feature discovery.

Also tag:

- source URL
- date
- thread/community
- query that found it
- pain candidate
- workaround if present
- consequence if present
- competitor mention if present
- self-promo flag

### Phase 7 — Deduplicate

Deduplicate by:

1. canonical URL/thread
2. same author repeating the same claim
3. copied/reposted wording
4. developer repeatedly promoting the same product

Count independent threads separately from raw evidence items.

### Phase 8 — Cluster into Pain Graph

Cluster evidence by the **underlying user problem**, not by keyword wording.

Bad clustering:

- `delete photos`
- `remove pictures`
- `clean images`

Good clustering:

- `Safe Deletion`
  - fear of accidental deletion
  - review before delete
  - trash / undo / recovery

For each cluster calculate only corpus-derived counts:

- independent threads
- user-origin evidence items (`A/B/C`)
- recent user-origin items
- workaround mentions
- explicit switching/abandonment mentions

Then assign confidence using `references/scoring.md`.

### Phase 9 — Negative-evidence check

Choose the 2–5 most tempting but weak hypotheses and run targeted searches for them.

Example:

- `best shot selection`
- `metadata preservation`
- `one-time purchase`

If targeted searches still produce little user-origin evidence, list them as **Weak / Unsupported**, not as core pains.

### Phase 10 — Emerging competitor scan

Developer posts are useful here.

Extract:

- new product names
- launch dates when visible
- positioning
- features used as differentiators
- repeated product mentions across user threads

Keep this section separate from Pain Evidence.

### Phase 11 — Product implications

For every proposed feature, link it to one or more pain clusters.

Use three labels:

- `DIRECT`: users explicitly requested the mechanism/feature.
- `INFERRED`: proposed solution derived from a documented pain.
- `SPECULATIVE`: interesting idea with weak evidence.

Do not present an inferred feature as if users explicitly asked for it.

### Phase 11A — Tool-site action classification

When `mode=tool_site`, classify each useful finding into exactly one primary action:

- `FEATURE`: capability inside the existing tool, e.g. preserve EXIF, batch mode, full-resolution extraction.
- `PAGE_CANDIDATE`: a distinct job/use-case that may deserve a standalone SEO page, e.g. `PNG to STL`, `download all images from website`, `compress image for upload`. This is **only an intent candidate** until validated with Ahrefs/Semrush/SERP.
- `HOMEPAGE_COPY`: trust or positioning message that strengthens the core page, e.g. local processing, no expiry, no signup.
- `FAQ_GUIDE`: clarification, edge case, workflow, or conceptual confusion that is useful content but does not yet justify a separate tool page.

For every `PAGE_CANDIDATE`, include:

- candidate query wording
- supporting pain/use-case evidence
- why it appears distinct from the core task
- `seo_validation_status: REQUIRED`

Do **not** infer search volume from Reddit recurrence.

Also extract `workaround_chains` explicitly. Example:

`PNG → online SVG converter → Tinkercad → extrude → STL`

A repeated workaround chain can justify an inferred one-step feature even when users never name that feature directly.

### Phase 12 — Report

Use `templates/pain-mining-report.md`.

Required sections:

1. Research scope
2. Corpus summary
3. Query performance, including any reframe batch
4. Pain Graph
5. Evidence table
6. Workarounds and workaround chains
7. Feature implications
8. Tool-site actions (when `mode=tool_site`)
9. Competitor discoveries
10. Weak / unsupported hypotheses
11. Next validation

## Evidence minimums

A pain cluster should not be called "strong" from a single viral thread.

Default thresholds:

- **HIGH confidence**: >= 3 independent **user-origin** threads (`A/B/C`), >= 2 `A/B` items, evidence score >= 8
- **MEDIUM confidence**: >= 2 independent **user-origin** threads (`A/B/C`), evidence score >= 4
- **LOW confidence**: anything below MEDIUM

`E_DEVELOPER_PROMO` never contributes score or user-origin thread count. `F_SECONDHAND_OR_AMBIGUOUS` may provide context but cannot upgrade confidence by itself.

These are workflow thresholds, not population estimates.

## Stop conditions

Stop broad searching when either:

- target corpus size is reached, or
- two consecutive query batches each add < 20% new relevant unique threads.

Continue only if a major pain branch is still untested.

## Failure modes to avoid

- Treating self-promotional posts as demand validation.
- Treating a failed SEO-keyword query as evidence that users do not have the problem.
- Calling a `PAGE_CANDIDATE` an SEO opportunity before keyword/SERP validation.
- Turning every pain into a page; many pains belong in features, copy, or FAQs.
- Ignoring a multi-step workaround because no user explicitly names the one-step solution.
- Reporting search-result snippets without opening the strongest threads.
- Turning one user's edge case into a top pain.
- Using upvotes as the only measure of importance.
- Counting several comments from the same discussion as independent demand.
- Concluding "users want X" when the corpus only shows one developer advertising X.
- Confusing Reddit popularity with search demand or willingness to pay.
- Hiding sparse or contradictory evidence.
- Generating fake evidence counts.

## Tool behavior

Use available web/search/browser tools. Prefer:

1. search with domain/community restriction
2. fetch/open primary thread
3. extract only the relevant post/comment context

If Reddit blocks direct fetch, use a search index, cached result, or browser-capable fetch tool. Do not claim full-thread evidence when only a snippet was visible.

For app research, optionally expand to Google Play/App Store reviews after Reddit, but keep source types separate.

## Final decision boundary

Pain Mining answers:

> What are users struggling with, how are they coping, what product gaps may exist, and—when researching a tool site—which findings map to features, candidate pages, homepage positioning, or FAQs?

It does **not** answer by itself:

> Is this commercially worth building?

When evaluating an opportunity, follow with:

- keyword/search-demand validation
- SERP/competitor validation
- store/review validation
- pricing/revenue evidence when available
- implementation cost
