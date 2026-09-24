# 05 — Implementation Plan

## Scope summary

## Release target

- Requested mode:
- High-fidelity kernel active:
- Prototype-only acceptable:
- Production-ready required:

## Output plan

| Source URL | site-key | page-key | Destination route | Research root | Component namespace | Asset namespace |
|---|---|---|---|---|---|---|

## Collision and preservation checks

- Existing routes inspected:
- Existing clone/prototype namespaces inspected:
- Route collisions:
- Shared foundation locations approved:
- Existing pages/artifacts that must not be replaced:

## File plan

| Path | Action | Risk class | Reason | Validation |
|---|---|---|---|---|

Risk classes: safe-local / shared-sensitive / business-critical.

## Component boundaries

## Shared foundation sequence

Complete sequentially before any parallel builder:

1. output/route plan
2. page shell/topology contract
3. shared tokens/fonts
4. shared types
5. shared asset registry
6. genuinely shared site-level components

## Component delivery pipeline

For each independent component:

```text
extract -> write spec -> pre-dispatch gate -> build -> bounded validation -> merge/integrate
```

## Builder evidence packet

Each high-fidelity builder receives:

- complete component spec
- target file
- screenshot/evidence path
- measured styles/state diffs
- responsive rules
- logical asset IDs
- integration constraints
- acceptance criteria

## Routes and locales

## Existing modules to reuse

## Data and state contracts

## Asset isolation and mapping

- Raw archive:
- Temporary served directory:
- Asset map:
- Manifest:
- Replacement checklist:
- Production-gate script:

## Dependencies

| Dependency | Existing/new | Justification | Bundle/runtime impact |
|---|---|---|---|

## Parallelization decision

- Eligible components:
- Sequential dependencies:
- Worktree/agent strategy:
- Merge order:
- Per-unit validation:

## Adaptation and replacement sequence

## Rollback strategy

## Validation commands

## Risks

- Auth/session:
- Credits/quota:
- Payments:
- API/data:
- Analytics/consent:
- SEO/localization:
- Temporary assets:
- Route/output collision:
- Deployment: