---
name: helpful-value-audit
description: Audit whether a tool page genuinely satisfies its target query through task fit, working functionality, useful differentiation, accurate claims, low-friction UX, trust, and supporting guidance. Use for self audits, competitor page audits, and SERP page-quality benchmarking. Do not decide whether the whole market should be attacked or skipped; hand market/architecture decisions to site-opportunity-scorecard or serp-siege.
metadata:
  version: 2.0.0
---

# Helpful Value Audit v2

Answer one question:

> **Does this page provide enough real user value for this query, and what page-level gap remains?**

This is not a Google HCU score and not a market-opportunity Skill.

## Modes

### Self audit

Audit the target page against a query/intended task and produce prioritized fixes.

### Competitor audit

Audit one competitor page to identify page-level strengths, weaknesses, and reusable table stakes.

### SERP benchmark

Compare the top meaningful results to establish page-level table stakes and gaps.

The output of SERP benchmark is a **Page Gap** (`NONE`, `WEAK`, `MODERATE`, `STRONG`)—not `ATTACK`, `CONDITIONAL`, or `SKIP`.

## Evidence labels

Use exactly:

- `TESTED` — directly executed/verified in the current audit;
- `OBSERVED` — visible in UI/HTML/source/current product behavior but not fully executed;
- `CLAIMED` — stated by the site but not independently verified;
- `UNKNOWN` — insufficient evidence.

Do not score a claimed feature as tested.

## Utility types

Classify before auditing:

- `STABLE_UTILITY` — task rules are mostly stable;
- `EXTERNAL_SPEC_UTILITY` — correctness depends on a platform/government/standard specification;
- `HIGH_TRUST_UTILITY` — errors can materially affect health, finance, legal, identity, or regulated decisions.

For external-spec/high-trust utilities, verify material facts against current primary sources when available.

## Workflow

### 1. Define the task

Record:

- primary query;
- primary user task;
- expected input/output;
- material modifiers (`free`, `bulk`, `100KB`, `no signup`, etc.);
- utility type.

### 2. Test the core workflow when possible

For an ordinary tool:

```text
Open -> Input -> Configure -> Process -> Inspect Result -> Export/Download/Copy
```

Test representative edge cases when they materially affect the task.

Record failures, misleading states, hidden friction, and whether the promised outcome is actually achieved.

### 3. Benchmark page-level table stakes

For competitor/SERP mode, compare only features that materially help the target task.

Classify observed coverage:

- `TABLE_STAKE` — common and expected;
- `COMMON` — useful but not distinctive;
- `DIFFERENTIATOR` — uncommon and materially useful;
- `RARE_GAP` — rarely covered and materially useful.

Do not reward novelty that does not help the query.

### 4. Score Helpful Strength

Use the deterministic calculator in `scripts/calculate_score.py`.

Dimensions:

| Dimension | Weight |
|---|---:|
| Intent & Task Match | 20 |
| Functional Completion | 30 |
| Relative Information Gain | 15 |
| Reliability & Claim Accuracy | 15 |
| Task UX / Friction | 10 |
| Trust / Transparency | 5 |
| Supporting Content | 5 |

Rate each dimension 0–4. Unknown evidence is not a neutral midpoint; mark the relevant evidence weak/unknown and lower report confidence.

Functional Completion is evidence-capped:

- `TESTED` -> eligible for rating 4;
- `OBSERVED` -> max 3;
- `CLAIMED` -> max 2;
- `UNKNOWN` -> max 1.

### 5. Apply reliability/task gates

Use gates only when directly evidenced:

- core task failure -> final score cap 49;
- critical reliability failure -> cap 49;
- major reliability failure -> cap 69;
- deceptive functionality -> cap 39.

Do not use a gate to punish cosmetic SEO incompleteness.

### 6. State Page Gap

After comparing the page with current relevant results:

- `STRONG` — repeated, material page-level weakness exists and a clearly better workflow/accuracy/usefulness can be delivered;
- `MODERATE` — meaningful improvement exists but is narrower or partially evidenced;
- `WEAK` — mostly parity/polish improvements;
- `NONE` — current results satisfy the task well and no material page-level gap is evidenced.

Page Gap is **not** a recommendation to build, buy a domain, or enter the market.

## External difficulty context

Authority, backlinks, domain age, traffic estimates, and brand strength may be mentioned as `LOW / MEDIUM / HIGH / UNKNOWN` external context when relevant, but do not convert them into a pseudo-precise `Ranking Moat: 85/100` score.

If the user needs a site/market decision, route to `$site-opportunity-scorecard`. If the direction is already selected and page planning is needed, route to `$serp-siege`.

## Output

Include:

- query/task and utility type;
- Helpful Strength /100;
- evidence confidence (`HIGH / MEDIUM / LOW`);
- Page Gap;
- strongest table stakes;
- material failures/limitations;
- 3–7 prioritized page-level improvements;
- `Do Not Fix` items when changes would add SEO filler or unnecessary complexity;
- evidence limits.

Avoid generic advice such as adding word count, FAQ volume, author bios, or “more content” unless it solves a specific task uncertainty.
