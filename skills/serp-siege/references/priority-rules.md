# Priority and First Batch Rules

Prioritize with explicit judgment across:

- demand evidence;
- SERP weakness;
- competitor validation;
- core reuse potential;
- expansion potential;
- build cost;
- maintenance cost.

Do not invent a precise multiplication score when the inputs are qualitative. Explain the strongest positive and negative factors instead.

## Evidence roles in prioritization

- Direct search, direct-competitor, first-party, and supplied metric evidence may support demand and priority judgments. Structured Top Pages / Organic Keywords / GSC / Bing evidence should retain URL/query provenance in the Demand Evidence Map.
- Professional vertical aggregators may corroborate which tool families or categories appear important, but their conversion rate, traffic ceiling, RPM, or economics must not be transferred to the candidate.
- Cross-vertical page-type benchmarks are **structure evidence only**. They may improve how an already-selected page is built, but they must not create a page, promote a cluster, or compensate for missing demand evidence.

## Demand evidence strength

Record a demand-strength judgment per retained cluster in the `Demand Evidence Map`:

- `STRONG`: repeated URL/query evidence across multiple direct competitors, or meaningful first-party query/performance evidence, with traceable provenance.
- `MEDIUM`: one credible competitor export/page plus supporting live search evidence, or repeated live dedicated-page evidence without reliable traffic/query metrics.
- `WEAK`: one weak/ambiguous observation, adjacent evidence, or evidence whose market/date/scope materially mismatches the target.
- `MISSING`: no usable demand evidence.

Do not turn third-party traffic estimates into exact demand truth. Use them comparatively and preserve source/date/market context.

## Levels

- `P0`: required for the First Batch or MVP promise.
- `P1`: validated expansion with clear demand and strong core reuse.
- `P2`: plausible later expansion with higher cost or weaker evidence.
- `HOLD`: not now; specify a measurable or observable revisit trigger.
- `REJECT`: do not create this feature or page under the current execution plan; it is not a verdict on the project.

## First Batch

Default shape:

- one core tool;
- 3–5 supporting search entrances;
- 2–5 adjacent capabilities;
- normally 8–15 effective search entrances in total.

These are planning defaults, not quotas. Explain any smaller or larger batch. Never inflate the batch to meet a count.

Use the report's `First Batch Deviation` field when the total or group mix falls outside the default shape. A deviation is valid when it explains why the smaller or larger batch is more coherent; the validator must not treat the defaults as absolute quotas.

Each item must include:

- a proposed URL or product item;
- its group: `CORE`, `SUPPORTING`, or `ADJACENT`;
- target cluster;
- why it belongs now;
- shared capability;
- SEO role.

## Roadmap discipline

- MVP/P0 implements the smallest complete workflow and the shared core needed by the First Batch.
- SERP weakness is an accelerator, not a universal gate. A cluster with both `SERP Strength: MISSING` and `Gap: MISSING` may remain P0 when it is the single user-selected First Batch `CORE` **or** when its `Demand Evidence Map` row is `STRONG` and based on traceable non-inferred evidence. Otherwise inferred expansion must be `HOLD` until its named evidence gate passes.
- P1 adds only evidenced demand that reuses the core and expands coverage coherently.
- P2 records edge demand, higher complexity, or insufficient current evidence.
- P1 or P2 may be `NONE` when no item meets the bar; do not invent work to populate a section.
- `HOLD` and `REJECT` belong in `Do Not Build Yet`, not hidden at the end of P2.
- Serious execution constraints should narrow, reorder, or condition affected work while preserving a roadmap for the unaffected scope.
- Page Pattern Enhancement may refine implementation acceptance criteria for a selected page, but it must not change the cluster's priority or increase the First Batch size.
- For template-driven sites, First Batch counts planning/search-entrance units, not every scaled entity/detail instance. Track initial instance volume separately in the Page Family Map.
