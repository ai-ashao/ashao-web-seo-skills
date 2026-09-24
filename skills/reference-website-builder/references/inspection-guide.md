# Live-page inspection guide

Use this guide only after exact page scope and repository context are recorded.

## Tool requirement

Use browser automation such as Chrome, Playwright, Puppeteer, or Browserbase. A normal HTTP fetch is not a substitute for interaction inspection. Do not bypass login, paywalls, CAPTCHAs, geo restrictions, or anti-bot controls.

For high-fidelity work, also read `extraction-recipes.md` and use its bounded computed-style and asset-discovery recipes.

## Scope discipline

- Open only the explicit URL by default.
- Do not crawl the sitemap or clone navigation destinations automatically.
- Follow another URL only to observe an in-scope interaction or asset, and record why.
- When multiple URLs are supplied, inspect each independently.
- In high-fidelity work, assign `site-key` and `page-key` before capture so screenshots, specs, and assets cannot collide.

## Capture sequence

1. Open the exact URL.
2. Record final URL, redirects, locale, cookie/consent state, and viewport.
3. Capture full-page screenshots at desktop, tablet, and mobile widths when practical.
4. Map sections and fixed overlays.
5. Scroll slowly from top to bottom before clicking controls.
6. Click each meaningful tab, accordion, dropdown, carousel control, modal trigger, and safe CTA.
7. Hover buttons, links, cards, images, and navigation items.
8. Test keyboard tab order, focus styles, Escape behavior, and Enter/Space activation.
9. Resize between representative widths and identify actual layout changes.
10. Inspect computed styles for representative elements and unique component variants.
11. Inventory layered media and state-specific media.
12. For high-fidelity stateful components, capture the same component before and after each material state change.

## Interaction model

For every interactive area, state one or more drivers:

- click
- hover
- keyboard
- scroll position
- viewport intersection
- time/autoplay
- drag/swipe
- form/input state
- server/data state

Do not implement a click-based substitute for a scroll-driven interaction without documenting the adaptation.

For scroll-dependent UI, record the observed trigger position/range and the before/after visual state. When the exact implementation mechanism is not observable, label it as inferred rather than claiming source-code knowledge.

## Computed-style sampling

In lightweight modes, sample only what supports the requested decision.

In high-fidelity modes, use the standard recipe from `extraction-recipes.md` for each non-trivial component root and record at least the material properties affecting:

- typography: family, size, weight, line height, letter spacing
- geometry: width, max width, height, padding, margin, gap
- layout: display, grid columns, flex direction, alignment, order
- visual: colors, borders, radius, shadow, filter, backdrop filter
- positioning: position, inset, z-index, overflow, sticky offset
- media: dimensions, object fit, aspect ratio, masking, clipping, layering
- motion: transition properties, duration, easing, transform, opacity, delay

Do not hand-estimate values that can be measured. Do not dump the entire DOM without a component purpose.

## Layered media inventory

Use the standard asset-discovery recipe for high-fidelity work, then inspect visually important sections for:

- `<img>`, `<picture>`, `<source>`, `<video>`, poster, and inline SVG
- CSS background images and masks
- absolutely positioned overlays
- multiple images in the same parent
- desktop/mobile asset swaps
- animated or autoplay media
- source dimensions and rendered dimensions
- position and z-index relationships

Assign each production-relevant or temporary media item a stable logical ID before downloading it.

## Responsive evidence

Do not infer responsive behavior from desktop alone.

For each material component, capture:

- what disappears or appears;
- order changes;
- stack/column changes;
- width and container changes;
- mobile-specific controls or assets;
- sticky/fixed behavior differences;
- approximate breakpoint range when it can be observed.

## Content handling

Visible text may be recorded during reconstruction to reproduce hierarchy, line length, and state geometry. Mark it as temporary reference copy. Before production release it must be replaced or authorized.

## Evidence quality

Distinguish:

- directly observed
- measured from computed style
- inferred from behavior
- inferred from DOM naming or public metadata
- unknown

Do not state an inference as confirmed source-code behavior.
