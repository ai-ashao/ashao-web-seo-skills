# Query Bank — v0.3

Use this as a pattern library. Replace bracketed terms with natural language. Keep queries short.

## Core principle

Search the **job and failure state**, not only the SEO keyword.

Bad default:

- `site:reddit.com website image downloader original resolution lazy loaded webp svg batch zip`

Better as separate queries:

- `site:reddit.com "bulk image downloader" extension`
- `site:reddit.com "download full resolution images" website`
- `site:reddit.com "save all images" webpage`

## A. Core discovery

- `site:reddit.com [product/category] problem`
- `site:reddit.com [product/category] annoying`
- `site:reddit.com [product/category] alternative`
- `site:reddit.com [task] tool`
- `site:reddit.com [task] app`

## B. Natural task language

Use verbs a user would type in a forum:

- `site:reddit.com "save all [objects]" [context]`
- `site:reddit.com "download every [object]" [context]`
- `site:reddit.com "turn [input] into [output]"`
- `site:reddit.com "convert [input] to [output]"`
- `site:reddit.com "make [input] smaller"`
- `site:reddit.com "keep formatting" [conversion]`
- `site:reddit.com "full resolution" [task]`
- `site:reddit.com "not thumbnails" [task]`

## C. Fidelity / preservation

Useful for converters, compressors, exporters, and downloaders:

- `site:reddit.com [task] formatting issue`
- `site:reddit.com [task] preserve formatting`
- `site:reddit.com [task] images tables`
- `site:reddit.com [task] metadata exif`
- `site:reddit.com [task] transparency`
- `site:reddit.com [task] filenames folders`
- `site:reddit.com [task] original resolution`
- `site:reddit.com [task] editable equations`

## D. Exact constraints

Useful for SEO utilities because constraints often become separate user jobs:

- `site:reddit.com [task] target file size`
- `site:reddit.com [task] [50kb/100kb/etc]`
- `site:reddit.com [task] width height`
- `site:reddit.com [task] print size`
- `site:reddit.com [task] page limit`
- `site:reddit.com [task] [format]`

Do not treat a failed exact-number Reddit query as proof that the SEO query has no demand. Exact constraints may be search-engine-native behavior rather than discussion behavior.

## E. Batch / scale

- `site:reddit.com [task] batch`
- `site:reddit.com [task] bulk`
- `site:reddit.com [task] "one by one"`
- `site:reddit.com [task] "hundreds"`
- `site:reddit.com [task] "thousands"`
- `site:reddit.com [task] folder`
- `site:reddit.com [task] csv`

## F. Workaround discovery

- `site:reddit.com [task] manually`
- `site:reddit.com [problem] workaround`
- `site:reddit.com [problem] "had to"`
- `site:reddit.com [task] inkscape tinkercad`
- `site:reddit.com [task] script`
- `site:reddit.com [task] command line`
- `site:reddit.com [task] multiple tools`

When a thread describes a chain such as `PNG → SVG → Tinkercad → STL`, record the whole chain.

## G. Destination / use-case constraints

- `site:reddit.com [problem] Word`
- `site:reddit.com [problem] email`
- `site:reddit.com [problem] Discord`
- `site:reddit.com [problem] upload form`
- `site:reddit.com [problem] WordPress`
- `site:reddit.com [problem] 3D printing`
- `site:reddit.com [problem] Canva`
- `site:reddit.com [problem] print`

## H. Switching / abandonment

- `site:reddit.com "switched from" [competitor]`
- `site:reddit.com "alternative to" [competitor]`
- `site:reddit.com "stopped using" [competitor]`
- `site:reddit.com "returned" [product]`

## I. Pricing / paywall

- `site:reddit.com [product/category] subscription`
- `site:reddit.com [product/category] paywall`
- `site:reddit.com [product/category] expensive`
- `site:reddit.com [product/category] "one time"`
- `site:reddit.com [product/category] free alternative`
- `site:reddit.com [product/category] expired`

## J. Trust / privacy

- `site:reddit.com [product/category] privacy`
- `site:reddit.com [product/category] offline`
- `site:reddit.com [product/category] "on device"`
- `site:reddit.com [product/category] permission`
- `site:reddit.com [product/category] upload`
- `site:reddit.com [task] local processing`

## K. Safety / reversibility

- `site:reddit.com [task] accidentally deleted`
- `site:reddit.com [task] undo`
- `site:reddit.com [task] recover`
- `site:reddit.com [task] trash`
- `site:reddit.com [task] confirmation`

## L. Extraction edge cases

Useful for downloader/scraper tools:

- `site:reddit.com [task] thumbnails full resolution`
- `site:reddit.com [task] lazy loaded`
- `site:reddit.com [task] linked from thumbnails`
- `site:reddit.com [task] background images`
- `site:reddit.com [task] webp svg`
- `site:reddit.com [task] gallery`
- `site:reddit.com [task] multiple pages`

## M. Document-conversion edge cases

- `site:reddit.com markdown docx reference template`
- `site:reddit.com markdown docx bullet list styles`
- `site:reddit.com markdown docx equations`
- `site:reddit.com markdown docx tables images`
- `site:reddit.com markdown docx track changes`

## N. 2D → 3D edge cases

- `site:reddit.com png to stl easy`
- `site:reddit.com logo to stl extrude`
- `site:reddit.com photo to stl depth map`
- `site:reddit.com svg to stl`
- `site:reddit.com image to stl mac`
- `site:reddit.com image to stl printable`

## O. Community restriction

When broad Reddit search is noisy, restrict to communities that match the user job:

- software/tools: `r/software`, `r/selfhosted`, `r/techsupport`
- Android: `r/androidapps`
- documents/Markdown: `r/Markdown`, `r/pandoc`, `r/ObsidianMD`
- 3D: `r/3Dprinting`, `r/BambuLab`, `r/tinkercad`
- web extraction/archiving: `r/DataHoarder`, `r/webscraping`, `r/chrome_extensions`
- business/QR: `r/smallbusiness`, `r/DigitalMarketing`, `r/graphic_design`, `r/qrcode`

These are examples, not an allowlist.

## Query Reframe Loop

If fewer than 40% of a 4–8 query batch is GOOD/OK, reframe once.

### Step 1 — Remove the SEO noun phrase

`website image downloader` → `save all images`, `download every image`, `bulk image download`

### Step 2 — Add the concrete desired result

- full resolution
- preserve formatting
- exact file size
- printable STL
- editable Word equation

### Step 3 — Add the failure/workaround

- one by one
- thumbnails only
- CLI too hard
- multiple conversions
- upload too large

### Step 4 — Restrict community

Only after the task language is specific.

Record both pre-reframe and post-reframe yield. One successful reframe is a signal that the original wording was wrong, not that demand suddenly appeared.

## Query-generation rules

- Prefer 12–24 short queries total for a normal run.
- Use 4–8 queries per batch.
- Adapt after each batch.
- Use one pain hypothesis per query.
- Avoid more than two OR clauses in routine searches.
- Do not overuse quoted phrases.
- Prefer natural task verbs over SEO nouns.
- Use recent-date filters for fast-moving software, but expand when evidence is sparse.
- Do not endlessly reframe: one adaptive reframe batch, then widen sources or declare sparse evidence.


## P. Ecosystem reframe

Some tool categories are discussed through **specific ecosystems**, not the generic SEO noun.

Examples:

- `chart maker` may appear as `Flourish alternative`, `Plotly cumbersome`, `Excel chart export`, or `ggplot`.
- `JSON formatter` may appear as browser-extension trust, VS Code large-file handling, `jq`, or JSON diff.
- platform downloaders may be discussed in the platform subreddit rather than under `downloader`.

Patterns:

- `site:reddit.com "[competitor] alternative" [job]`
- `site:reddit.com [library/product] cumbersome [task]`
- `site:reddit.com/r/[community] "[natural task phrase]"`
- `site:reddit.com [host platform] [desired outcome]`

Use ecosystem reframing only when the generic task is semantically clear but the category noun is not how users discuss it.

## Query yield vs pain density

Do not confuse these:

- **Query yield**: how many inspected results are relevant to the task.
- **Pain density**: how many relevant fetched threads contain user-origin pain/request evidence.

A text case converter can have relevant results but very low pain density because the task is already simple and often solved by built-in shortcuts. That is valid negative evidence.

If query yield is good but pain density is low, stop broadening unless a major intent branch is untested.

## Source Widening Gate

After one failed task-language reframe, use `references/source-widening.md`.

Do not run repeated Reddit rewrites indefinitely.
