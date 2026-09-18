# Evidence Taxonomy

## A_USER_REQUEST

A user proactively asks for a solution, product, workflow, or capability.

Examples:

- "Is there an app that can..."
- "I need a tool to..."
- "How do I..."

Strength: high.

## B_FIRSTHAND_COMPLAINT

A user describes a problem they personally experienced.

Examples:

- lost data
- repeated manual work
- poor quality
- app crashed on a large library
- subscription caused them to uninstall

Strength: high.

## C_FEATURE_REQUEST

A user asks an existing product/developer to add or change a specific behavior.

Examples:

- add date filtering
- add batch selection
- preserve metadata
- let me set a target file size

Strength: medium-high.

## D_RECOMMENDATION

A user recommends a product or approach to another user.

Useful for solution and competitor discovery, but it does not prove that the recommender personally experienced the original pain.

Strength: low-medium for demand; useful for competitive context.

## E_DEVELOPER_PROMO

A developer/founder promotes a product they built.

Signals:

- "I built..."
- "I made..."
- "I'm the developer..."
- support email / launch link / repeated promotion

Strength: zero for user-demand validation. It always scores 0; recency, workaround, payment, or consequence bonuses must not increase it.

Use only for:

- competitor discovery
- feature inventory
- positioning language
- launch timing

## F_SECONDHAND_OR_AMBIGUOUS

Claims whose origin or firsthand status is unclear.

Examples:

- "people hate..."
- "everyone wants..."
- scraped summaries without primary thread context

Strength: low. It may add context but does not count as a user-origin thread for confidence.

## Additional tags

Each item may also carry:

- `consequence`: lost time, lost money, lost data, abandonment, inability to complete task
- `workaround`: manual steps, multiple apps, scripts, repeated exports, spreadsheets, DIY
- `switching`: moved from competitor A to B
- `pricing`: subscription/paywall/one-time/free concerns
- `privacy`: upload/permissions/on-device/offline concerns
- `scale`: large file/library/batch/performance
- `safety`: undo/trash/recovery/confirmation
- `source_clutter`: WhatsApp, screenshots, downloads, email attachments, etc.
