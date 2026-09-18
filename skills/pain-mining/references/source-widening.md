# Source Widening Gate — v0.3

Use this only after one task-language Query Reframe still fails.

## Trigger

Widen when both are true:

1. post-reframe usable-query rate remains below 40%; and
2. fewer than 5 unique user-origin threads have surfaced.

Do **not** widen merely because pain density is low when query relevance is already good. That can be genuine negative evidence.

## Widening order

Choose the single most relevant next lane first:

1. **REDDIT_ECOSYSTEM** — specific competitors, libraries, host products, or specialist subreddits.
2. **GITHUB_ISSUES** — developer tools, libraries, extensions, local/open-source utilities.
3. **STACK_EXCHANGE** — technical workflows and repeated workaround questions.
4. **APP_REVIEW** — app stores, browser-extension stores, marketplace reviews.
5. **SPECIALIST_FORUM** — product/community forums, professional communities, Product Hunt discussions.

## Rules

- Run 4–8 targeted searches in the new lane.
- Record source type and yield separately.
- Do not merge Reddit comments, GitHub Issues, and store reviews into one fake frequency.
- Prefer firsthand problem reports over feature marketing.
- Stop after one lane produces enough user-origin evidence.
- If two additional lanes are both poor, classify SPARSE unless a major intent branch is still untested.

## Example: Chart Maker

Generic `chart maker` may have poor Reddit phrasing.

Try ecosystem language first:

- Flourish alternative
- Plotly cumbersome
- Excel chart export
- Google Sheets chart limitation
- ggplot workflow

If those still fail, specialist data-visualization communities or issue trackers are a better lane than a third round of generic Reddit rewrites.
