---
name: reference-website-builder
description: Analyze an explicit reference page or screenshot, build a lightweight prototype from reusable structure, or adapt an approved reference pattern into an existing product. Use for competitor/reference UI analysis, static prototypes, high-fidelity page reconstruction, and production integration. Default to the lightest mode that satisfies the request; when high fidelity is requested, use deterministic inspection, isolated page outputs, component specifications, bounded parallel builders, and visual QA rather than guessing.
license: MIT
---

# Reference Website Builder v2.1

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

If the user explicitly asks for close/high-fidelity recreation, activate the deterministic reconstruction kernel below. Otherwise keep prototype work lightweight.

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

In `full` mode, use the detailed project-context, inspection, component-spec, provenance, implementation-plan, QA, and release-gate resources.

## High-fidelity kernel activation

Activate the deterministic reconstruction kernel only when one of these is true:

- mode is `full`;
- the user explicitly asks for high fidelity, close recreation, or visual parity;
- the page has substantial stateful interaction where a loose prototype would be misleading;
- the implementation will become the basis of a production adaptation and fidelity must be verified first.

Do not activate it merely because a URL was provided.

## Reference scope

- Inspect only explicit URLs/screenshots unless the user asks to expand scope.
- Do not crawl the sitemap by default.
- Follow additional links only to understand an in-scope interaction or state.
- Separate observed facts from inference.
- Use desktop and mobile evidence when responsive behavior matters.
- Treat each explicit page as durable output; never let a later page silently overwrite an earlier page.

## Output isolation contract

For high-fidelity work, assign every page a collision-resistant namespace before extraction.

Use:

- `site-key`: readable normalized origin/host slug + first 8 lowercase hex chars of SHA-256 over the normalized origin;
- `page-key`: readable pathname slug + first 8 lowercase hex chars of SHA-256 over normalized pathname plus any query/fragment that materially selects page state.

Recommended research paths:

```text
docs/reference-build/<site-key>/<page-key>/
  00-project-context.md
  01-reference-matrix.md
  02-page-topology.md
  03-behaviors.md
  04-design-language.md
  05-implementation-plan.md
  06-qa-report.md
  components/
  references/
```

Recommended temporary asset paths:

```text
.reference-assets/<site-key>/<page-key>/raw/
public/__reference__/<site-key>/<page-key>/
```

Choose implementation component/route paths according to the existing project. Do not force a Next.js namespace into another stack.

Before editing:

1. inventory existing routes and page/component namespaces;
2. verify the destination route is not an unintended collision;
3. preserve existing user-authored pages and research artifacts;
4. record any approved shared location explicitly.

If a destination route already exists and the request did not clearly authorize replacing it, preserve it and choose an additive adaptation plan.

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

Do not treat every pixel as a requirement in lightweight modes. In high-fidelity mode, measure the pixels that materially define the component instead of estimating them.

## Deterministic reconstruction kernel

Read `references/extraction-recipes.md` together with `references/inspection-guide.md`.

For each explicit page:

1. capture equivalent desktop/tablet/mobile evidence when practical;
2. perform scroll before click, then click, hover, keyboard, time/autoplay, drag/swipe, and responsive sweeps as relevant;
3. identify the interaction model before implementation;
4. use the standard computed-style recipe for representative component roots and meaningful descendants;
5. use the standard asset-discovery recipe to inventory layered media;
6. capture before/after styles for stateful or scroll-driven behavior;
7. write component specs from measured evidence, not visual guesses.

Do not dump the entire DOM merely because automation can. Extract the bounded evidence needed to build the in-scope component.

## Foreman pipeline

For high-fidelity `prototype` or `full` work, use a bounded extract -> specify -> dispatch pipeline.

Foundation work is sequential:

1. repository/output plan;
2. page topology;
3. shared tokens/layout rules;
4. shared types/assets needed by multiple sections.

Then process page sections top-to-bottom:

```text
extract section
-> write component spec
-> pass pre-dispatch gate
-> dispatch bounded builder
-> continue extracting the next independent section
```

Parallel builders are optional, not mandatory. Use them only when:

- runtime supports parallel agents/worktrees;
- Git state is safe;
- at least three components are genuinely independent;
- shared foundation is already fixed;
- every builder receives a complete self-contained specification.

Builder prompts should include the complete relevant spec inline or otherwise guarantee the worker receives the full contract. Do not rely on a worker guessing which external notes matter.

## Pre-dispatch gate

Do not dispatch a high-fidelity component builder until all applicable checks pass:

- [ ] component purpose and target file are explicit;
- [ ] screenshot/evidence path is known;
- [ ] interaction model is identified;
- [ ] measured typography, spacing, layout, borders/radius/shadow, positioning, and motion values are captured where material;
- [ ] hover/focus/active/state changes are captured;
- [ ] scroll-driven trigger and before/after states are captured when applicable;
- [ ] layered assets and logical asset IDs are identified;
- [ ] desktop and mobile behavior are documented;
- [ ] target-product differences are explicit;
- [ ] acceptance criteria are testable;
- [ ] the unit is small enough to implement without guessing.

If the spec becomes too large for one bounded implementation unit (roughly >150 lines of substantive component detail), split it before dispatch.

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

For ordinary `analyze` or lightweight `prototype` work, do not create a full asset-provenance system unless third-party assets are actually being brought into the implementation.

For high-fidelity reconstruction, temporary target assets may be used only through the existing isolated asset workflow. Register them by logical ID and page namespace. Never ship unapproved reference branding, testimonials, legal text, proprietary media, or hotlinks.

## Workflow

### 1. Frame

Record only what materially affects the result:

- target product/route;
- reference URL(s) or screenshots;
- selected mode;
- target user task;
- existing design system/stack if adapting;
- important non-goals.

For high-fidelity work, also record `site-key`, `page-key`, destination route, artifact roots, and collision checks.

### 2. Inspect evidence

For live references, inspect the current page rather than coding from memory. Capture enough states/viewports to support the requested fidelity.

For screenshots, explicitly mark cropped/unknown behavior instead of inventing it.

### 3. Build a compact pattern model

For each material pattern/state:

- what is observed;
- why it may help the target task;
- `KEEP / CHANGE / ADD / OMIT`;
- responsive/interaction implications;
- any target-product difference.

This replaces a separate `competitive-ui-reverse-engineering` Skill.

### 4. Implement only if requested

- `prototype`: optimize for fast review and truthful interaction; use the deterministic kernel only when high fidelity is requested.
- `adapt`: use target-native components and real product behavior.
- `full`: use isolated outputs, component specs, provenance, bounded parallelization, and release gates.

Do not silently broaden scope from one page to a full site.

### 5. Verify proportionately

Minimum when implementation is requested:

- desktop visual check;
- narrow-mobile visual check;
- primary interaction states;
- keyboard/focus basics for interactive controls;
- no obvious overflow;
- project build/type/lint checks when working in a real repository.

High-fidelity reconstruction additionally requires equivalent-viewport visual comparison, state-by-state interaction verification, route-preservation checks, and the existing asset-release gates.

## SEO boundary

This Skill may preserve route metadata and page semantics during production adaptation, but it does not perform keyword research or invent an SEO page system.

- Page/keyword planning -> `$serp-siege`
- Technical crawl/index checks -> `$technical-seo-audit`
- Page helpfulness/value -> `$helpful-value-audit`

## Output discipline

Do not generate paperwork that the user did not ask for.

| Mode | Default output |
|---|---|
| analyze | concise pattern analysis |
| prototype | pattern note + prototype + proportional visual QA |
| adapt | implementation plan + code + QA |
| full | isolated evidence/spec/provenance/QA artifact set |

This Skill absorbs the useful responsibilities of the former `competitive-ui-reverse-engineering` and `adapt-reference-site` Skills while keeping heavyweight reconstruction opt-in.
