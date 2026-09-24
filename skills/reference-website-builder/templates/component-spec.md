# Component Specification — <name>

## Overview

- Product purpose:
- Target file:
- Page namespace: <site-key>/<page-key>
- Screenshot/evidence:
- Interaction model: static / click / hover / keyboard / scroll / intersection / time / drag / data-state

## Reference observations and evidence

| Observation | Evidence type | Viewport/state | Confidence |
|---|---|---|---|

Evidence type: observed / measured / inferred / unknown.

## Component structure

Describe the bounded DOM/component hierarchy and reusable sub-components.

## Content/data model

- Temporary reference copy:
- Product copy/data source:
- Required props/state:
- Real vs mocked behavior:

## Measured styles

### Container

- typography:
- size/constraints:
- spacing:
- layout:
- border/radius/shadow:
- position/z-index/overflow:
- background/filter:
- transition/motion:

### Material child elements

Record only the values required to implement the component without guessing. Reference the raw extraction artifact when the list is long.

## State differences

### <state / behavior>

- Trigger:
- State A:
- State B:
- Changed properties/content:
- Transition:
- Observed mechanism:
- Implementation decision:

Repeat for hover, focus, active, selected, disabled, loading, empty, error, success, scroll, and autoplay states that materially apply.

## Responsive behavior

### Desktop

### Tablet

### Mobile

- Observed breakpoint range:
- Order/stacking changes:
- Asset/control swaps:

## Assets

| Logical asset ID | Visual role | Current status | Source/temporary path | Replacement constraints |
|---|---|---|---|---|

Components must use the centralized asset map rather than scattered direct `__reference__` paths.

## Target-product adaptation

- KEEP:
- CHANGE:
- ADD:
- OMIT:

## Accessibility

- semantics:
- keyboard/focus:
- accessible name/label:
- reduced motion:
- contrast/alt policy:

## Integration points

- existing primitives/modules:
- shared-sensitive files touched:
- business-critical boundaries:
- dependencies:

## Acceptance criteria

- [ ] visual geometry matches the selected fidelity target
- [ ] material states behave as specified
- [ ] desktop/mobile rules are verified
- [ ] assets resolve through approved logical mapping
- [ ] project type/build check passes for this unit where applicable

## Pre-dispatch gate

- [ ] purpose and target file explicit
- [ ] screenshot/evidence path known
- [ ] interaction model identified
- [ ] material computed styles measured
- [ ] applicable state changes captured
- [ ] scroll trigger/before-after captured when applicable
- [ ] layered assets/logical IDs identified
- [ ] desktop/mobile behavior documented
- [ ] target-product differences explicit
- [ ] acceptance criteria testable
- [ ] component is a bounded implementation unit

If substantive implementation detail grows beyond roughly 150 lines, split the component before dispatch.

## Out of scope
