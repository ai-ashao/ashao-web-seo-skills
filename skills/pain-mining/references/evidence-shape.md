# Evidence Shape — v0.3

Evidence shape describes the **observed research corpus**. It is not market size, search volume, or commercial potential.

## Diagnostics

Calculate:

- `pain_density = unique user-origin pain threads / unique relevant fetched threads`
- `promotion_contamination = developer-promo items / all classified evidence items`

Do not compare these ratios across unrelated sources as if they were population statistics.

## BROAD

Use BROAD when evidence is distributed across several recurring user problems.

Default operational signal:

- at least 3 retained pain clusters each have >=2 independent user-origin threads; **or**
- >=8 user-origin threads span >=4 retained clusters and no single cluster contains >50% of user-origin threads.

BROAD means the category has multiple evidence-backed friction branches in the sampled corpus.

## NARROW

Use NARROW when real evidence exists but concentrates in one or two jobs/branches.

Default operational signal:

- at least one MEDIUM/HIGH cluster; **or**
- >=3 user-origin threads exist but BROAD criteria are not met; **or**
- a distinct subtask repeats while the generic/core task remains low-friction.

Example: generic Word Counter may be low-friction while `word count excluding citations` forms a narrow branch.

## SPARSE

Use SPARSE when neither BROAD nor NARROW criteria are met after:

- normal query batches,
- one task-language reframe when needed,
- and bounded source widening when searchability—not low pain density—is the problem.

SPARSE is a valid result.

## Interpretation guardrail

- BROAD does not mean "build it."
- NARROW can still hide an excellent SEO page opportunity.
- SPARSE does not prove zero demand; it only says this research method did not find enough user-origin pain evidence.
- High query yield + low pain density is evidence of a low-friction or already-solved task, not a reason to keep searching until pain appears.
