---
name: serp-siege
description: Turn a user-selected tool-site competitor, website, or keyword into evidence-labeled coverage maps, a bounded first batch, and an MVP/P1/P2 execution roadmap. Use direct competitors as the primary demand source; optionally use professional vertical aggregators for demand-distribution signals and a tightly bounded cross-vertical page-pattern benchmark for strategic page templates. Use after the user has decided to pursue the direction; do not use to judge whether the project is worth doing, choose site architecture, build the site, publish pages, or monitor GSC.
---

# SERP Siege

Convert a competitor domain, website, keyword, or combination into a bounded product-and-SEO execution roadmap. Treat the user's request as a decision to proceed. Treat direct competitors as the primary demand dataset, not a blueprint. Enumerate broadly, cluster by user intent, and recommend only pages backed by distinct tasks and reusable product capabilities. Use non-direct benchmark sources only for the specific research role defined below; do not let them inflate scope.

## Responsibility boundary

This skill improves how to execute an already-selected direction. It must not:

- decide whether the project is worth doing;
- output `GO`, `CONDITIONAL_GO`, or `NO_GO`;
- calculate opportunity or separation-risk scores;
- choose between an independent site, existing-site section, or existing-site page;
- invoke an opportunity-analysis skill automatically;
- stop the roadmap merely because competition is strong or evidence is incomplete.

It may reject a proposed page, merge duplicate clusters, defer a feature, narrow the First Batch, or require an implementation prerequisite. Those are execution decisions, not project-admission decisions.

## Inputs

Accept either `target.domain`, `target.keyword`, or both. Also use these when supplied:

- `market.country` and `market.language`;
- `business.monetization` and `business.maintenance_preference`;
- `existing_site.domain`;
- `execution.destination` when the user has already chosen a site, section, or page;
- structured competitor or first-party exports such as Top Pages, Organic Keywords, Keyword Gap, GSC, Bing, or equivalent datasets from Ahrefs, Semrush, or another supplied source;
- optional professional vertical aggregators or collection sites relevant to the tool family;
- optional page-type benchmark examples supplied by the user;
- optional `opportunity_context` supplied from an upstream analysis.

Do not block on missing optional context or a missing opportunity report. State bounded assumptions, mark missing execution evidence, and lower planning confidence. Never invent search volume, keyword difficulty, traffic, revenue, CPC, backlinks, or conversion rates.

When the user supplies structured exports, treat them as first-class execution evidence and process them before speculative keyword expansion. Normalize source, market, date, URL, query, position, traffic/volume semantics, and provenance using [references/export-evidence.md](references/export-evidence.md). Do not truncate a supplied export to the live-browsing page budget.

If upstream opportunity or architecture context is supplied, read [references/optional-handoff.md](references/optional-handoff.md). Consume it without rerunning or challenging the upstream decision.

## Workflow

1. **FRAME — set the filling.** Convert the user's selected direction into an execution frame: primary job, scope, destination if supplied, constraints, assumptions, and missing execution evidence.
2. **EXPAND — roll the wrappers.** Collect query and competitor dimensions with recall favored over precision. Start with direct competitors and supplied Top Pages / Organic Keywords evidence. Use professional vertical aggregators only for bounded demand-distribution signals. Follow [references/dumpling-sop.md](references/dumpling-sop.md).
3. **CLUSTER — portion the filling.** Group by intent, task, input/output, constraint, SERP similarity, and workflow. Read [references/clustering-rules.md](references/clustering-rules.md).
4. **MAP — draw coverage.** Build the Demand Evidence, Feature Coverage, and SERP Coverage views using [references/coverage-model.md](references/coverage-model.md). Map clusters to page decisions with [references/page-mapping-rules.md](references/page-mapping-rules.md). When repeated URLs share one scalable template, add a Page Family Map using [references/page-family-rules.md](references/page-family-rules.md) instead of treating every instance as a separate product decision. Only after the demand/page map is stable, conditionally run the bounded Page Pattern Enhancement in [references/page-type-benchmark.md](references/page-type-benchmark.md) for strategically important templates that still have a structural or UX question.
5. **PRIORITIZE — make the first batch.** Rank demand, SERP weakness, competitor validation, core reuse, expansion potential, build cost, and maintenance cost. Read [references/priority-rules.md](references/priority-rules.md).
6. **ROADMAP — write the menu.** Produce the applicable report from [references/report-template.md](references/report-template.md).

## Research-source roles

Keep the three source classes separate:

- **Direct competitors — WHAT to build.** Use supplied Top Pages / Organic Keywords exports first when available, then live landing pages, navigation, and SERP overlap to establish demand, cluster boundaries, and page evidence. Preserve URL-level proof instead of collapsing everything into generic competitor notes.
- **Professional vertical aggregators — WHICH tool families matter.** Use category prominence, tool-family coverage, and supplied traffic distributions as supporting evidence about demand concentration. Do not assume their conversion rate, traffic ceiling, or business economics transfer to the candidate.
- **Cross-vertical page-type leaders — HOW a page can be structured.** Use only when the Page Pattern Enhancement trigger fires. Extract reusable information architecture, modules, CTA mechanics, preview/state patterns, related-item discovery, or internal-link patterns. They are not keyword-demand evidence.

Do not add a page merely because an aggregator or page-type leader has it. Every proposed page must still bind to a retained cluster and shared product capability.

## Page Pattern Enhancement guardrails

This is an optional enhancement layer, not an SEO MVP gate.

- Trigger it only after the direct-competitor demand map and SEO Page Map exist.
- Use it only when a P0/high-leverage template has a meaningful unresolved structure, UX, conversion, discovery, or internal-link question; or when direct competitors are structurally weak or homogeneous.
- Skip it when direct competitors already provide a strong reusable pattern or when the research would delay the bounded First Batch without resolving a real design question.
- Benchmark at most **1–2 cross-vertical sites total** in a normal run.
- Apply it to at most **1–3 strategic page templates**.
- Extract at most **3 reusable patterns total**.
- A benchmark pattern may change module order, information architecture, CTA mechanics, preview/state handling, related-item discovery, or internal-link structure.
- A benchmark pattern must not create a new keyword cluster, create a new page by itself, promote a cluster to P0/P1, change the user-supplied destination, or substitute for missing demand evidence.

## Execution behavior

Continue through all six phases and produce an execution roadmap. When a serious platform, copyright, API, technical, or maintenance constraint appears:

- state which feature or page it affects;
- narrow, reorder, or condition the affected work;
- provide a safe or maintainable alternative where possible;
- identify the prerequisite or validation required before implementation;
- continue planning the unaffected scope.

Do not turn an execution constraint into a verdict on the whole project.

## Output rules

- Use exactly the evidence labels defined in the report template.
- One query is not one page. Reject thin number, country, wording, and format permutations unless intent or workflow evidence justifies a distinct page.
- Every proposed page must bind to a named cluster and shared capability.
- Direct-competitor/search evidence determines demand and page justification; cross-vertical benchmark evidence never does.
- Aggregator evidence may corroborate tool-family demand concentration, but must not be presented as the candidate's conversion rate or attainable traffic ceiling.
- Include the optional `Page Pattern Enhancement` report section only when the conditional benchmark actually ran; otherwise omit it.
- A supplied destination must remain a user or upstream decision and include a traceable `Destination Basis`; otherwise use `NOT_SUPPLIED` and do not infer site architecture.
- `SAME_PAGE` must name its canonical parent; `REJECT` may omit its proposed URL but must name its canonical parent and state the execution reason.
- Every P0 item must state why it belongs now.
- SERP weakness/gap is supporting evidence, not a universal admission gate. When both current SERP strength and gap are `MISSING`, a non-core First Batch item may still remain P0 only when the `Demand Evidence Map` records `STRONG` non-inferred demand evidence (for example repeated competitor-export proof or first-party query data). Without that proof, inferred `SUPPORTING` and `ADJACENT` entries move to `HOLD`.
- P1 and P2 may be `NONE`; never invent roadmap items to fill a section.
- Keep the default First Batch to one core tool, 3–5 supporting entries, and 2–5 adjacent capabilities, normally 8–15 effective search entrances. Explain deviations.
- Use `MISSING` for unverified candidate feature state. Reserve `EXISTING` for first-party or live-public evidence; do not use `PLANNED` as a substitute for an unknown current state.
- Product coverage and SEO coverage must describe one roadmap, not separate wish lists.
- When structured exports are supplied, include an `Evidence Dataset` and `Demand Evidence Map`; do not average conflicting third-party estimates into fake precision.
- For template-driven sites, separate Page Family/template decisions from scaled instances. The normal 8–15 First Batch target counts effective search entrances/decision units, not every mechanically generated detail instance.
- Match the user's language; default to Simplified Chinese for Chinese requests while preserving the template's canonical machine-readable headings.

Validate a saved Markdown report with the bundled script resolved relative to this `SKILL.md`:

```bash
python3 <serp-siege-root>/scripts/validate_output.py path/to/report.md
```

The script checks structural and contractual invariants only. It cannot prove that public observations are current or that a metric is truthful.
