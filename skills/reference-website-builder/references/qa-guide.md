# QA guide

## Baseline first

Record validation status before edits so pre-existing failures are separated from introduced regressions.

For high-fidelity work, also record the source URL -> destination route -> <site-key>/<page-key> mapping so QA cannot accidentally compare or overwrite the wrong page.

## Two QA milestones

### Reconstruction QA

Goal: determine whether the local page accurately reproduces the selected page's visible design and behavior at the requested fidelity.

Compare equivalent source/local viewports and states:

- topology and section geometry
- typography, spacing, radius, borders, shadows, and backgrounds
- layered media, crop, focal point, masking, and z-index
- responsive breakpoints and reflow
- click, hover, keyboard, scroll, sticky, autoplay, drag, and state transitions

At minimum for high fidelity, compare desktop and mobile screenshots section-by-section. When practical, use the same viewport dimensions and equivalent page state.

A reconstruction can pass visual QA while temporary assets or adaptation work remain; record them in the QA report.

### Production QA

Goal: determine whether the adapted page is safe and ready to ship.

Production QA includes all reconstruction checks plus identity, content, provenance, business regression, SEO, accessibility, performance, and release-gate checks.

## Required QA layers

### 1. Build integrity

Run project-provided formatting, lint, typecheck, tests, and production build commands as applicable.

Confirm that previously existing routes affected by shared foundation changes still resolve/build.

### 2. Visual QA

Capture screenshots at the same representative widths used during research. Compare section boundaries, containers, wrapping, vertical rhythm, alignment, media crop, overlays, sticky elements, and overflow.

For every discrepancy, classify it as:

- extraction/spec defect;
- implementation defect;
- intentional adaptation;
- inaccessible/unknown source behavior;
- out of scope.

Fix extraction/spec defects at the specification source rather than patching the implementation blindly.

### 3. State and interaction QA

Test:

- default, hover, focus, active, selected, disabled
- loading, empty, error, success
- tabs, accordions, modals, drawers, dropdowns, and carousels
- uploads and generation states where relevant
- scroll-activated and sticky behavior
- autoplay, pause, drag, and swipe
- long text, translations, and missing media
- back/forward navigation and deep links

For high-fidelity components, validate the interaction model itself: click-driven UI must not replace observed scroll-driven behavior without an intentional adaptation record.

### 4. Responsive QA

Interact at mobile, tablet when materially different, and desktop. Do not only shrink a desktop screenshot.

### 5. Accessibility

Check semantics, heading order, keyboard reachability, visible focus, labels, accessible names, Escape/focus return, contrast, reduced motion, and alt-text policy.

### 6. Performance

Check local optimized media, sensible dimensions and formats, no target hotlinks, no unnecessary client rendering, dependency impact, and layout shift.

### 7. SEO and localization

Before production release, verify unique title, description, H1, body copy, canonical, locale alternates, indexability, sitemap, structured data, internal links, translated metadata, and no target brand or claims left behind.

### 8. Business regression

Verify existing auth/session, pricing/checkout, credits/quota, analytics/consent, APIs, feature flags, and deployment behavior.

### 9. Output isolation and route preservation

Verify:

- every explicit page has a unique page namespace;
- later work did not delete or replace an earlier page unintentionally;
- destination routes match the approved plan;
- page-specific assets/components are not leaking into unrelated routes;
- intentionally shared foundation changes were regression-tested.

### 10. Temporary asset and optional release review

Verify:

- every temporary asset exists in the manifest
- components use the centralized asset map
- `.reference-assets/` is not served
- `public/__reference__/` is used only during development
- replacements preserve visual constraints
- manifest states are accurate
- run `scripts/check-reference-assets.mjs` when the project owner requests a release review
- record the review result and any follow-up work

## Reporting

Every issue should include severity, viewport/state, expected result, observed result, evidence, likely cause, and disposition.

Report temporary assets and any requested release review explicitly:

```text
Temporary assets:
Release review: requested / not requested
Open issues:
```
