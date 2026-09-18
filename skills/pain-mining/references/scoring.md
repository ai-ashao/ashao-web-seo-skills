# Evidence Scoring — v0.2

Scoring prioritizes the collected corpus; it does not estimate market prevalence.

## Item score

Base score:

- A_USER_REQUEST: 3
- B_FIRSTHAND_COMPLAINT: 3
- C_FEATURE_REQUEST: 2
- D_RECOMMENDATION: 1
- E_DEVELOPER_PROMO: 0
- F_SECONDHAND_OR_AMBIGUOUS: 0.5

Add:

- +1 concrete consequence (lost data, paid money, abandoned product, repeated work)
- +1 concrete workaround or multi-step coping behavior
- +0.5 recent <= 24 months
- +0.5 explicit willingness to pay / actual payment / paid switching behavior

Cap each evidence item at 5.

## Thread cap

Multiple similar comments in one thread are correlated. Cap the total contribution from one thread to a pain cluster at 4 points.

## Cluster confidence

HIGH:

- >= 3 independent **user-origin threads** (`A/B/C`)
- >= 2 A/B user-origin items
- >= 8 points after thread caps

MEDIUM:

- >= 2 independent **user-origin threads** (`A/B/C`)
- >= 4 points

LOW:

- below MEDIUM

## Workaround-chain strength

Track separately; do not add extra score beyond the normal workaround bonus.

Record:

- number of independent threads showing a multi-step workaround
- number of distinct tools/steps in the chain
- whether users explicitly complain about complexity/time

A repeated multi-step workaround is strong **solution-design evidence**, but not search-demand proof.

## Query quality metrics

For each query:

- GOOD: >=40% inspected results directly relevant
- OK: 20–39%
- POOR: <20%

For each batch also record:

- usable-query rate = (GOOD + OK queries) / queries run
- reframe recovery = post-reframe usable-query rate minus pre-reframe usable-query rate

These are research-process diagnostics, not market metrics.

## Promotion contamination

Report separately:

- number of E_DEVELOPER_PROMO items
- number of F_SECONDHAND_OR_AMBIGUOUS items
- products repeatedly self-promoted

`E_DEVELOPER_PROMO` always scores 0, including recency/payment/workaround bonuses.

A cluster supported only by developer promotion remains LOW/UNSUPPORTED regardless of raw mentions. `F_SECONDHAND_OR_AMBIGUOUS` can add context but does not count as a user-origin thread for confidence.

## Tool-site action evidence

Action classification does not change pain confidence.

- `FEATURE`: can be DIRECT or INFERRED.
- `PAGE_CANDIDATE`: must have a distinct job/constraint and at least LOW user-origin support; always mark SEO validation REQUIRED.
- `HOMEPAGE_COPY`: can be supported by trust/friction evidence.
- `FAQ_GUIDE`: appropriate for conceptual confusion, edge cases, or workflows.

Never promote a candidate page to a validated SEO opportunity using Reddit evidence alone.
