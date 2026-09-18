---
name: reference-website-builder
description: Analyze an explicit reference page or screenshot, build a lightweight prototype from its reusable structure, or adapt an approved reference pattern into an existing product. Use for competitor/reference UI analysis, static HTML prototypes, high-fidelity page reconstruction, and production integration. Default to the lightest mode that satisfies the request; do not force a full reconstruction workflow when analysis or a prototype is enough.
license: MIT
---

# Reference Website Builder v2

Use references to improve a target product without turning every visual task into a heavyweight migration project.

The default principle is:

> **Borrow structure and interaction logic; preserve product truth and target identity.**

## Modes

Choose exactly one mode from the request. Prefer the lightest adequate mode.

### `analyze`

Use when the user wants to understand a competitor/reference, compare screenshots, or extract patterns.

Output only what helps the decision:

- page/section map;
- important interaction patterns;
- responsive behavior;
- `KEEP / CHANGE / ADD / OMIT` decisions;
- implementation implications when requested.

Do not modify code unless asked. Do not create a document bundle by default.

### `prototype`

Use when the user wants a static HTML/React prototype, design exploration, or a first-pass recreation before production work.

Default deliverables:

- one compact `REFERENCE_PATTERN.md` or equivalent working note;
- prototype implementation;
- desktop + narrow-mobile visual check.

Do not require production auth, payments, analytics, persistence, or SEO infrastructure for a disposable prototype.

### `adapt`

Use when an approved reference pattern should be integrated into an existing project.

Preserve:

- framework and package manager;
- routes and i18n conventions;
- real product behavior;
- auth/payments/analytics/API boundaries;
- target design tokens unless the user explicitly chooses a reference-led visual language.

### `full`

Use only when the user explicitly requests high-fidelity reconstruction, an authorized migration, or a substantial multi-section/multi-state rebuild where provenance and release gates matter.

In `full` mode, use the existing templates/references for project context, design language, asset provenance, implementation plan, component specs, and QA.

## Reference scope

- Inspect only explicit URLs/screenshots unless the user asks to expand scope.
- Do not crawl the sitemap by default.
- Follow additional links only to understand an in-scope interaction or state.
- Separate observed facts from inference.
- Use desktop and mobile evidence when responsive behavior matters.

## What to extract

Focus on transferable product decisions:

1. information architecture;
2. section order and density;
3. grid/proportion/spacing rhythm;
4. primary workflow and CTA hierarchy;
5. progressive disclosure and result states;
6. responsive reordering/stacking;
7. trust and objection-handling patterns;
8. reusable component boundaries;
9. visual roles when relevant.

Do not treat every pixel as a requirement.

## Visual policy

Default order:

1. preserve an approved target design system;
2. otherwise derive a simple target-native visual system;
3. use a reference-led visual language only when explicitly requested;
4. use a staged reference-first skin only when explicitly requested.

A reference-led visual direction is permission to reuse general design roles—not logos, proprietary illustrations, copied copy, customer material, or other identity assets.

## Product truth

Reference screenshots may imply behavior that the target product does not have.

Never invent:

- AI capability;
- payment success;
- auth/account state;
- saved cloud data;
- external API results;
- calculation logic;
- production deployment.

For unavailable interactions, either omit them in an analysis/prototype or expose an honest deferred state when parity requires the visible control.

## Assets and rights

Use `$web-asset-pipeline` when production assets need optimization, provenance, resizing, or rights tracking.

For ordinary `analyze` or `prototype` work, do not create a full asset-provenance system unless third-party assets are actually being brought into the implementation.

For `full` reconstruction, use the existing temporary-asset isolation and release-gate resources. Never ship unapproved reference branding, testimonials, legal text, or proprietary media.

## Workflow

### 1. Frame

Record only what materially affects the result:

- target product/route;
- reference URL(s) or screenshots;
- selected mode;
- target user task;
- existing design system/stack if adapting;
- important non-goals.

### 2. Inspect evidence

For live references, inspect the current page rather than coding from memory. Capture enough states/viewports to support the requested fidelity.

For screenshots, explicitly mark cropped/unknown behavior instead of inventing it.

### 3. Build a compact pattern model

For each material pattern state:

- what is observed;
- why it may help the target task;
- `KEEP / CHANGE / ADD / OMIT`;
- responsive/interaction implications;
- any target-product difference.

This replaces a separate `competitive-ui-reverse-engineering` Skill.

### 4. Implement only if requested

- `prototype`: optimize for fast review and truthful interaction.
- `adapt`: use target-native components and real product behavior.
- `full`: follow the detailed reconstruction/provenance workflow.

Do not silently broaden scope from one page to a full site.

### 5. Verify proportionately

Minimum when implementation is requested:

- desktop visual check;
- narrow-mobile visual check;
- primary interaction states;
- keyboard/focus basics for interactive controls;
- no obvious overflow;
- project build/type/lint checks when working in a real repository.

Full reconstruction additionally uses the existing QA and asset-release gates.

## SEO boundary

This Skill may preserve route metadata and page semantics during production adaptation, but it does not perform keyword research or invent an SEO page system.

- Page/keyword planning -> `$serp-siege`
- Technical crawl/index checks -> `$technical-seo-audit`
- Page helpfulness/value -> `$helpful-value-audit`

## Output discipline

Do not generate paperwork that the user did not ask for.

Default outputs by mode:

| Mode | Default output |
|---|---|
| analyze | concise pattern analysis |
| prototype | pattern note + prototype + visual QA |
| adapt | implementation plan + code + QA |
| full | existing full evidence/provenance/QA artifact set |

This Skill absorbs the useful responsibilities of the former `competitive-ui-reverse-engineering` and `adapt-reference-site` Skills without copying their full workflow into every task.
