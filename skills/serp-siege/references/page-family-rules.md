# Page Family and Template Rules

Use a Page Family Map when many indexable URLs are instances of one reusable page archetype. This prevents SERP Siege from treating hundreds of near-identical implementation decisions as hundreds of independent product decisions.

## When to create a family

Create a family when pages share substantially the same:

- user task and completion state;
- information architecture and controls;
- product/data pipeline;
- metadata schema;
- internal-link behavior;
- implementation template.

Examples include:

- `/font/{slug}` font detail pages;
- `/sprite/{slug}` asset/detail pages;
- `/convert/{input}-to-{output}` converter-pair pages when the workflow is templated;
- `/calculator/{slug}` detail pages from a common calculator framework;
- directory/item pages backed by one entity schema.

## Family types

Use:

- `SINGLE`: one non-scaled page/template decision;
- `TEMPLATE`: many indexable instances generated from one reusable template/data model;
- `CATEGORY`: repeated category/collection pages sharing a collection template;
- `CONTENT`: repeated guide/reference pages sharing a content template.

## Cluster versus instance

A keyword/query still becomes a distinct cluster when intent, input/output, controls, SERP, or workflow materially differs.

An entity/name variation may remain an instance within one family when the task and page behavior are the same and the differentiation is primarily entity data. Do not create one product decision per entity merely because every entity has its own searchable name.

Converter pairs can be separate clusters **and** belong to one `TEMPLATE` family: cluster separation captures distinct search intent/input-output; the family captures shared implementation.

## Required family record

For each family record:

- stable family name;
- family type;
- URL pattern;
- bound cluster(s);
- 1–5 representative instances;
- initial indexable instance count;
- scaling/inclusion rule;
- shared product/data core;
- priority and evidence.

## First Batch counting

The default 8–15 First Batch target counts effective search/planning entrances, not raw repeated entity instances.

For a scaled family, record instance volume separately. Example:

- First Batch planning unit: `font-detail` family;
- representative instances: Inter, Roboto, Lato;
- initial instances: 150;
- scaling rule: only fonts with complete metadata/license/download asset.

Do not claim that 150 instances represent 150 independently validated intents unless the evidence actually supports that claim.

## Scaling safety

A scalable family must define an inclusion rule that prevents empty/thin instances. Require the data or workflow needed to make each instance useful. If instances differ only by a swapped token with no meaningful entity-specific value, hold or reject scaling.
