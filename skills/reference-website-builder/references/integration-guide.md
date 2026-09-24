# Existing-project integration guide

## Repository discovery order

Read in this order when present:

1. root `AGENTS.md`, `CLAUDE.md`, `README.md`, contributing guides, and architecture docs
2. workspace/monorepo configuration
3. package manifests and lockfiles
4. route and app entry points
5. global styling and design tokens
6. shared components and page examples
7. i18n configuration and locale dictionaries
8. auth, payments, credits, API clients, analytics, consent, SEO, and deployment files
9. test and CI configuration

## Package manager

Infer from lockfiles and workspace configuration. Do not switch package managers.

- `pnpm-lock.yaml` -> pnpm
- `yarn.lock` -> yarn
- `package-lock.json` -> npm
- `bun.lock` or `bun.lockb` -> bun

Use existing scripts from the relevant package. In a monorepo, run commands from the correct workspace.

## Output isolation preflight

Before high-fidelity implementation:

1. inventory existing routes/pages;
2. inventory existing research, screenshot, component, and asset namespaces;
3. derive the page's `site-key` and `page-key`;
4. plan unique research/screenshot/temporary-asset roots;
5. identify the destination route;
6. identify any shared foundation files that may change;
7. detect collisions before writing.

A new reference page is not permission to replace a previous clone, prototype, user-authored route, or unrelated artifact directory.

If multiple pages share a true site-level foundation, make that sharing explicit. Otherwise keep page assets and components isolated.

## Package and dependency policy

Before adding a dependency:

1. Search for an existing equivalent.
2. Check whether native platform or current UI primitives can handle it.
3. Verify compatibility with current framework and runtime.
4. Record why the dependency is needed.
5. Avoid framework upgrades or broad lockfile churn.

Do not copy package manifests from a reference implementation.

## Design-system policy

Prefer existing:

- tokens and CSS variables
- button, card, input, dialog, tab, accordion, tooltip, and navigation primitives
- icon packages
- breakpoints and containers
- animation utilities
- typography system

Introduce page-scoped tokens before changing shared global tokens. Shared-token changes require impact review across existing pages.

For a reference-led high-fidelity reconstruction, isolate page-specific tokens first. Promote a token to shared only when the target project intentionally adopts it.

## Foundation before parallel builders

The following work should be sequential when shared:

- output/route plan;
- page shell and layout contract;
- shared tokens/fonts;
- shared types;
- shared asset registry;
- shared site-level components.

Only after that foundation is stable should independent component builders run concurrently.

## Business-module protection

Treat these as high risk:

- authentication and session middleware
- billing, checkout, webhooks, and payment provider code
- credit or quota calculation
- database schema and migrations
- API signing and secret handling
- analytics identity and consent
- locale middleware and redirects
- sitemap, robots, canonical, and structured-data generation

Use their existing public interfaces. A visual redesign should not cause a rewrite of these modules.

## Validation cadence

For implementation work:

- record baseline validation before edits;
- run the cheapest relevant type/build check after meaningful bounded units;
- run the repository's normal full validation before QA completion;
- re-check existing routes that share modified foundation files.

## Git safety

- Check status before edits.
- Never reset, clean, checkout, or delete user changes without explicit instruction.
- If the working tree is dirty, isolate new files and avoid automated worktree orchestration.
- Create a baseline report of existing build/test failures.
- Keep changes small enough to review and revert.
- Use worktrees only when supported and the working tree is safe.

## Empty or incompatible repositories

If no usable web application exists:

- do not silently scaffold a new project,
- document the missing foundation,
- provide a recommended stack only when asked,
- produce design and implementation artifacts that can be handed to a later project-creation step.
