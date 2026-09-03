# Calibration Notes

These notes summarize the empirical calibration that shaped v1.1. They are not Google ranking-factor claims.

## Benchmark round 1 — high-traffic utility sites

Observed across utility sites ranging from roughly 100K monthly visits to multi-million-visit properties:

- long-form content and author bios were not universal requirements;
- functional task completion was consistently more important for utility pages;
- broad multi-tool domains can succeed when tool clusters remain coherent;
- old-looking UI does not necessarily imply weak utility value;
- traffic/authority must not be used as Helpful Score inputs.

Resulting rule: separate **Helpful Strength** from **Ranking Moat**.

## Benchmark round 2 — `youtube thumbnail resizer free`

The SERP showed that high-authority pages may rank while carrying stale external-platform specifications.

Resulting rules:

- classify External-Spec Utilities;
- verify material specifications against current primary sources;
- distinguish reliability severity;
- do not infer Helpful Strength from ranking position.

## Benchmark round 3 — `compress image to 100kb`

The SERP showed that capabilities such as local processing, no signup, exact target presets, and batch support can become common table stakes.

Resulting rules:

- Information Gain must be relative to the current SERP;
- rare features only matter if they improve the actual task;
- programmatic target-size pages are not automatically low-value when demand and preconfigured state are real;
- failure handling, safe target margins, width/height constraints, format strategy, and honest target behavior can be more useful than generic SEO copy.

## Self-audit calibration — imgsizetokb.com

The first live self-audit exposed the need to distinguish `TESTED` from `OBSERVED` evidence and to avoid over-scoring functionality that could not be executed end-to-end in the audit environment. It also showed why a `Do Not Fix` section is useful: some pages need deeper functionality, not more words.

## Practical principle

For utility pages, optimize in this order:

```text
Real demand
-> Task completion
-> Reliability
-> Relative differentiation
-> Low-friction UX
-> Trust
-> Supporting explanation
```
