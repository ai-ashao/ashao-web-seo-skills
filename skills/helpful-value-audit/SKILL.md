---
name: helpful-value-audit
description: Audit a tool page, competitor page, or SERP for people-first helpful value, functional usefulness, reliability, relative differentiation, ranking moat, and attackability. Use for SEO tool sites and utility landing pages. Distinguish tested evidence from claims, verify external specifications against primary sources, and do not treat this as a hidden Google HCU score.
metadata:
  version: 1.1.0
---

# Helpful Value Audit

## Purpose

Evaluate whether a tool page deserves to exist for users and whether it offers enough value to compete in search.

This skill is designed for utility/tool websites. It does **not** attempt to infer Google's hidden Helpful Content score or reverse-engineer a proprietary ranking system.

The skill answers three separate questions:

1. **Helpful Strength** — How useful, reliable, and complete is this page for the target query?
2. **Ranking Moat** — How difficult is the competing page/domain to displace even if its page-level helpfulness is imperfect?
3. **Attackability** — Is there enough practical gap in function, reliability, UX, or differentiation to justify building or improving a page for this query?

The core principle is:

> For a tool page, functionality and successful task completion are usually more important than word count, generic explanatory content, or cosmetic SEO completeness.

---

# Modes

Support three modes.

## Mode A — Self Audit

Input:

- page URL, local preview, or deployed page
- target query or intended search intent
- optional competitor set

Goal:

- determine whether the page is ready to index / scale
- identify missing Helpful Value
- output prioritized fixes
- provide a SERP replacement reason

Invocation concept:

```text
/helpful-audit <url> [query]
```

## Mode B — Competitor Audit

Input:

- competitor URL
- target query

Goal:

- measure the competitor's real page-level strengths and weaknesses
- separate Helpful Strength from Ranking Moat
- identify exploitable gaps

Invocation concept:

```text
/helpful-competitor <url> <query>
```

## Mode C — SERP Audit

Input:

- target keyword/query
- optional locale/device constraints
- optional preferred competitor count

Default:

- inspect the top 5 meaningful organic tool results
- expand to top 10 when results are heterogeneous or the decision is unclear

Goal:

- establish SERP table stakes
- calculate relative feature gaps
- detect stale or inaccurate facts
- estimate Ranking Moat by competitor
- recommend ATTACK / CONDITIONAL / SKIP

Invocation concept:

```text
/helpful-serp <query>
```

---

# Non-Negotiable Rules

## Never claim a Google HCU score

Do not say:

```text
Google HCU score: 82/100
```

Say:

```text
Helpful Strength: 82/100
```

This is an analytical rubric, not a Google metric.

## Do not equate more text with more helpfulness

Never recommend content expansion only to increase word count.

Do not recommend:

- 1,500 words because competitors have 1,500 words
- generic definitions solely for SEO completeness
- boilerplate "What is X?" sections when the tool already solves the intent
- FAQ inflation

Supporting content exists to remove user uncertainty, explain limits, and improve task completion.

## AI generation is not automatically a violation

Do not treat AI-written content itself as a negative signal.

Evaluate the output instead:

- accuracy
- usefulness
- uniqueness
- evidence
- redundancy
- whether it exists only to capture search traffic

## Do not recommend fake expertise

Never recommend:

- fake author identities
- fake expert review
- invented credentials
- fabricated usage data
- fake testimonials

## Do not infer ranking causality from position alone

A page may rank because of:

- authority
- historical performance
- backlinks
- brand
- topical footprint
- domain age
- first-mover advantage

Therefore:

> Ranking position is evidence of SERP success, not proof of high Helpful Strength.

---

# Step 1 — Identify Query and Page Type

Before scoring, determine the user's actual task.

Extract:

```text
Primary query
Primary user task
Expected input
Expected output
Critical constraints
Implied intent modifiers
```

Examples of modifiers:

```text
free
online
no signup
no download
bulk
exact size
private
local
mobile
```

If the query contains them, treat them as part of Search Intent rather than optional marketing claims.

Example:

```text
Query: youtube thumbnail resizer free

Intent requirements:
- resize a thumbnail
- online use
- free access
- low friction
```

---

# Step 2 — Classify the Utility Type

Classify the page before evaluating reliability.

## Type 1 — Stable Utility

Examples:

```text
compress image
png to jpg
crop image
json formatter
word counter
```

Characteristics:

- task rules are mostly stable
- freshness has low importance
- reliability focuses on truthful claims and actual function

## Type 2 — External-Spec Utility

Examples:

```text
youtube thumbnail size
instagram image resizer
passport photo size
google ads image size
discord emoji resizer
marketplace upload requirements
```

Characteristics:

- task depends on an external platform, government, standard, or policy
- specifications can change

Mandatory behavior:

> Verify material specifications against the current primary source.

Examples:

```text
YouTube -> official YouTube / Google Help
US passport -> travel.state.gov
Meta / Instagram -> official Meta documentation
```

Do not rely on competitor consensus when a primary source exists.

## Type 3 — High-Trust / YMYL Utility

Examples may include tools materially affecting:

- health
- finance
- legal decisions
- regulated identity documents

Increase scrutiny for:

- source quality
- expertise
- accuracy
- limitation disclosure
- risk of misleading outputs

Do not apply the same trust standard to a color picker and a financial calculator.

---

# Step 3 — Functional Inspection

For tool pages, inspect the actual workflow before evaluating supporting content.

Whenever possible, test the tool rather than only reading the landing page.

Minimum workflow:

```text
Open page
-> identify tool without searching for it
-> provide valid input
-> configure expected target
-> run tool
-> inspect result
-> download/export/copy result
```

Test edge cases when material.

Examples for image compression:

- JPG
- PNG
- WebP
- large image
- small image
- target close to current size
- target dramatically below current size
- portrait / landscape
- multiple files if batch is claimed

Record:

```text
Does the tool load?
Does the user immediately know what to do?
Does the promised operation work?
Does the output satisfy the stated target?
Can the result be retrieved?
Are failures explained?
Does mobile remain usable?
Are there fake progress states?
Are there misleading download buttons?
```

---

# Step 3.5 — Evidence Confidence

Every scored observation must carry an evidence level. Do not score a claimed capability as if it was tested.

Use exactly these labels:

```text
TESTED
- the workflow or claim was directly verified in the current audit

OBSERVED
- the capability is visible in the UI, rendered page, source, or product behavior, but the full workflow was not executed

CLAIMED
- the site states the capability, but it was not independently observed or tested

UNKNOWN
- evidence is insufficient
```

Default Functional Completion ceilings when the evidence is incomplete:

```text
TESTED   -> eligible for 30/30
OBSERVED -> normally <= 24/30 unless equivalent runtime evidence exists
CLAIMED  -> normally <= 18/30
UNKNOWN  -> normally <= 12/30
```

These are evidence ceilings, not automatic scores. A tested tool can still score poorly if it fails.

For each important capability, record:

```text
Feature: Batch compression
Evidence: OBSERVED
Confidence: Medium
Notes: UI exposes multi-file upload, but no end-to-end batch run was performed.
```

At report level, return an overall confidence label:

```text
HIGH
MEDIUM
LOW
```

Use HIGH only when the core workflow and material claims are directly verified or strongly evidenced.

---

# Step 4 — Base Helpful Score

Score 0–100 using the following default weights for ordinary tool pages.

| Dimension | Weight |
|---|---:|
| Intent & Task Match | 20 |
| Functional Completion | 30 |
| Relative Information Gain | 15 |
| Reliability & Claim Accuracy | 15 |
| Task UX / Friction | 10 |
| Trust / Transparency | 5 |
| Supporting Content | 5 |
| **Total** | **100** |

Do not mechanically award points for the existence of a section. Score quality and relevance.

---

# Dimension 1 — Intent & Task Match (20)

Evaluate whether the page directly satisfies the target query.

### 17–20 — Strong

- page state closely matches query
- tool is visible immediately
- query modifiers are honored
- minimal interpretation required

Example:

```text
Query: compress image to 100kb
Page opens with Target = 100 KB
```

### 11–16 — Adequate

- page contains the correct tool
- user must configure the relevant setting manually
- some intent modifiers are not obvious

### 0–10 — Weak

- page is only textually related
- tool is buried
- wrong task is foregrounded
- major query constraint is missing

---

# Dimension 2 — Functional Completion (30)

This is normally the highest-weight dimension.

Evaluate:

- task success
- output correctness
- failure handling
- format/input coverage
- workflow completeness
- meaningful controls
- batch support when relevant
- preview / validation when relevant

### 25–30 — Strong

The user can reliably complete the intended task with few or no workarounds.

### 16–24 — Adequate

The core task works but important cases require compromise or external steps.

### 0–15 — Weak

The page promises more than the tool can complete, or the task frequently fails.

---

# Dimension 3 — Relative Information Gain (15)

This dimension must be scored **relative to the current SERP**.

Do not give points because a feature sounds good in isolation.

First build a SERP feature coverage table.

Example:

| Feature | Top 5 Coverage |
|---|---:|
| Exact target KB | 100% |
| Local processing | 80% |
| Batch | 80% |
| No signup | 80% |
| HEIC input | 40% |
| Failure explanation | 20% |
| Dimension fallback | 20% |
| Safe KB margin | 0% |

Classify feature coverage using these default bands:

### Table Stakes

```text
>= 70% SERP coverage
```

Expected capability. Match it, but do not treat it as meaningful differentiation.

### Common

```text
40%–69% coverage
```

Useful, but only modestly differentiating.

### Differentiator

```text
10%–39% coverage
```

Potentially meaningful if it materially improves the target task.

### Rare Gap

```text
< 10% coverage
```

Potentially strong Information Gain, subject to actual user value.

Coverage alone is not enough: a rare feature that does not help the query should receive little or no Information Gain credit.

Then score based on how much the page adds beyond table stakes.

Information Gain may come from:

- deeper function
- better automation
- unique controls
- failure handling
- first-party data
- real examples
- better explanations
- privacy advantage
- task-specific logic
- workflow integration

It does **not** require a long article.

## Prevent score inflation / double-counting

The same evidence may inform several dimensions, but it should have one primary score contribution.

Example:

```text
Feature: Safe upload margin
Primary contribution: Relative Information Gain
Secondary evidence: Reliability, UX
Do not award full points in all three dimensions for the same feature.
```

If one capability appears relevant to multiple dimensions, explicitly name the primary dimension and use the others only as context.

---

# Dimension 4 — Reliability & Claim Accuracy (15)

Check:

- factual accuracy
- truthful product claims
- output claims
- unsupported absolutes
- privacy claims
- external specifications when applicable

Watch for wording such as:

```text
always
exactly
without any quality loss
100% guaranteed
best
never fails
required
must
maximum
```

Absolute claims require strong evidence.

For External-Spec Utilities, verify current facts against the primary source.

Classify material reliability problems by severity:

### Critical

A false or unsupported claim is likely to make the user fail the core task, submit a non-compliant output, or make a materially wrong high-trust decision.

Examples:

- a passport tool outputs dimensions that the issuing authority does not accept
- a converter claims success but produces an invalid file
- a privacy claim says files never leave the device when network evidence shows upload is required

Default consequence:

```text
Helpful Strength <= 49
```

### Major

A material specification or product claim is clearly wrong or stale, but the tool may still complete the task in many cases.

Example:

```text
A platform page states an obsolete upload limit as a universal current requirement.
```

Default consequence:

```text
Helpful Strength <= 69
```

### Minor / Stale

The information is no longer the preferred or current recommendation, but it remains usable and does not normally make the core task fail.

Default consequence:

- no hard cap
- deduct within Reliability according to impact
- recommend updating the source-backed guidance

Do not label a page Critical merely because a recommendation is old if the old value remains accepted.

---

# Dimension 5 — Task UX / Friction (10)

Evaluate the cost of completing the task.

Check:

- tool visibility above the fold
- unnecessary signup
- unnecessary download
- forced account creation
- intrusive modal
- excessive ads
- fake buttons
- confusing settings
- task interruption
- mobile usability
- CLS / layout movement when observable

Core task path should remain clean:

```text
Input
-> Configure
-> Process
-> Result
-> Download / Export
```

Ads or promotions should not break this chain.

---

# Dimension 6 — Trust / Transparency (5)

For ordinary utility sites, basic trust is sufficient.

Check as relevant:

- About
- Contact
- Privacy
- Terms
- processing location
- upload / retention policy
- format/file limits
- known limitations
- company/person identity when appropriate

Do not over-penalize low-risk utilities for lacking an expert author bio.

Increase scrutiny for High-Trust / YMYL utilities.

---

# Dimension 7 — Supporting Content (5)

Supporting content should solve questions the interface cannot solve by itself.

Good examples:

```text
What happens if the file cannot reach 100KB?
Should dimensions or quality be reduced first?
What file type works best for this target?
What are the actual upload requirements?
What data is uploaded or retained?
Why did this output differ from the requested target?
```

Weak examples when added only for SEO bulk:

```text
What is image compression?
History of image compression
Why images are important
Benefits of technology
```

Do not reward generic filler.

---

# Step 5 — Hard Gates

Base score alone is insufficient.

Apply the following caps after scoring.

## Gate A — Core Task Failure

Condition:

- tool cannot reliably complete the query's core task

Cap:

```text
Helpful Strength <= 49
```

## Gate B1 — Critical Reliability Failure

Condition:

- a material false claim is likely to make the user fail the core task, create a non-compliant output, or make a materially wrong high-trust decision

Cap:

```text
Helpful Strength <= 49
```

## Gate B2 — Major Reliability Failure

Condition:

- an important product/specification claim is clearly false or materially stale
- the task may still work in many cases, but the guidance is meaningfully unreliable

Cap:

```text
Helpful Strength <= 69
```

Minor/stale issues do not trigger a hard gate; score them inside Reliability.

## Gate C — Deceptive Functionality

Condition includes:

- fake download buttons
- fake tool behavior
- deceptive redirects
- misleading ads presented as functionality

Cap:

```text
Helpful Strength <= 39
```

## Gate D — Demandless / Stateless Scaled Page

Do **not** penalize a page merely because it belongs to a programmatic family.

Trigger only when the page is substantially:

```text
Demandless
+
State-less
+
Value-less
```

Meaning:

- no credible independent query demand
- page state does not materially change
- user task is not made easier
- page exists mainly because the template can generate it

Cap:

```text
Helpful Strength <= 59
```

---

# Step 6 — Scaled Page Risk

Evaluate separately from Helpful Strength.

Programmatic pages are not automatically bad.

Example family:

```text
compress-image-to-20kb
compress-image-to-50kb
compress-image-to-100kb
compress-image-to-200kb
compress-image-to-500kb
```

Can be legitimate if:

1. independent demand exists
2. target state is preconfigured
3. user reaches the intended outcome faster
4. only meaningful variants are created

Risk rises when the site generates arbitrary variants such as:

```text
101kb
102kb
103kb
...
999kb
```

with no evidence of distinct demand or user value.

## Required sibling sampling

Do not judge a programmatic family from one page alone.

When sibling pages exist, sample at least 5 representative variants when practical, including:

- one low-value parameter
- one common/high-demand parameter
- one middle parameter
- one unusual parameter
- one different unit or scenario when available

Example:

```text
10KB
50KB
100KB
250KB
1MB
```

Compare:

```text
Query demand evidence
Tool state difference
Content overlap
FAQ overlap
Title / H1 difference
Unique task guidance
Internal linking
Independent user value
```

Return a compact sibling finding such as:

```text
Sibling differentiation:
- Functional: STRONG
- Intent: MEDIUM
- Content: WEAK

Scaled Page Risk: MEDIUM
```

Return:

```text
Scaled Page Risk: LOW / MEDIUM / HIGH
```

Explain the exact reason.

---

# Step 7 — Site-Level Cluster Coherence

Do not require an entire domain to cover one narrow topic.

Instead inspect whether the current page belongs to a coherent tool/content cluster.

Example acceptable structure:

```text
Tools
├── PDF
│   ├── Merge
│   ├── Compress
│   └── Edit
├── Image
│   ├── Resize
│   ├── Compress
│   └── Convert
└── Video
    ├── Compress
    └── Convert
```

A broad multi-tool site can still be coherent.

Return separately:

```text
Cluster Coherence: STRONG / ADEQUATE / WEAK
```

Do not fold this directly into the page score unless the information architecture materially harms intent or trust.

---

# Step 8 — Ranking Moat

Helpful Strength is not Ranking Strength.

Estimate Ranking Moat independently.

Use available evidence such as:

- domain authority proxies
- referring domains
- brand recognition
- domain/site age
- topical footprint
- indexed page footprint
- historical search visibility
- current organic traffic
- number of strong related pages
- first-mover / category ownership

Suggested qualitative scale:

```text
0–20   Very Low
21–40  Low
41–60  Medium
61–80  High
81–100 Very High
```

Do not invent precision when data is unavailable.

If only partial evidence exists, return a range or confidence label.

Example:

```text
Ranking Moat: 85/100 — High confidence
```

or:

```text
Ranking Moat: 55–70 — Medium confidence
```

---

# Step 9 — Attackability

Attackability answers:

> Is there enough practical opportunity to build a page that is meaningfully better and realistically competitive?

Base the judgment on:

```text
Helpful Weakness
+
Functional Gap
+
Reliability / Freshness Gap
+
UX Gap
+
Relative Information Gain Opportunity
-
Ranking Moat
```

Do not pretend this is a mathematically proven Google formula.

Do not output pseudo-precise values such as `Attackability: 73.4/100` unless the user explicitly supplies and asks to use a validated model. The default output is qualitative and evidence-backed.

Return one of:

```text
HIGH
MEDIUM-HIGH
MEDIUM
LOW
SKIP
```

### HIGH

Use when:

- SERP has clear task gaps
- several ranking pages are weak or stale
- small/medium domains already rank
- differentiation is practical

### MEDIUM-HIGH

Use when:

- strong domains exist
- but SERP still admits weaker specialist pages
- material functional or reliability gaps exist

### MEDIUM

Use when:

- opportunity exists
- but winning likely needs stronger authority, content cluster, or product depth

### LOW / SKIP

Use when:

- top results are both highly useful and heavily protected by moat
- no credible differentiation exists
- query demand is weak or redundant

---

# Step 10 — SERP Replacement Test

For every self audit and opportunity audit, answer:

> Why should Google replace one current SERP result with this page?

The answer must name concrete user value.

Good:

```text
This page reaches the requested <=100KB target automatically, explains when the target is physically impractical, supports HEIC input, offers a safe upload margin, and processes files locally without signup.
```

Weak:

```text
This page also lets users compress images to 100KB.
```

If a credible replacement reason cannot be produced, differentiation is insufficient.

---

# Self Audit Output Format

Use this structure.

```markdown
# Helpful Value Audit

URL: ...
Target Query: ...
Utility Type: Stable / External-Spec / High-Trust

## Verdict
Helpful Strength: 82/100
Status: PASS WITH IMPROVEMENTS
Evidence Confidence: HIGH / MEDIUM / LOW

## Evidence Summary
- Core workflow: TESTED / OBSERVED / CLAIMED / UNKNOWN
- Material claims: ...
- Primary-source verification: ...

## Hard Gates
- Core Task Failure: No
- Critical Reliability Failure: No
- Major Reliability Failure: No
- Deceptive Functionality: No
- Demandless Scaled Page: No

## Score Breakdown
- Intent & Task Match: 18/20
- Functional Completion: 26/30
- Relative Information Gain: 11/15
- Reliability & Claim Accuracy: 14/15
- Task UX / Friction: 8/10
- Trust / Transparency: 3/5
- Supporting Content: 2/5

## Strongest Areas
1. ...
2. ...
3. ...

## Critical Gaps
1. ...
2. ...
3. ...

## P0 — Fix Before Indexing / Scaling
- ...

## P1 — Improve Next
- ...

## Do Not Fix
List things that are already sufficient or where changes would add complexity without user value. Examples:
- Do not add generic 1,500-word filler.
- Do not create fake author expertise.
- Do not remove useful programmatic pages solely because they share a template.
- Do not change a correct claim merely to sound more differentiated.

## Scaled Page Risk
LOW
Reason: ...

## Cluster Coherence
STRONG
Reason: ...

## SERP Replacement Reason
...
```

Suggested status thresholds before gates:

```text
85–100  STRONG
75–84   PASS
65–74   IMPROVE BEFORE SCALING
<65     WEAK
```

Hard Gates override the threshold.

---

# Competitor Audit Output Format

```markdown
# Competitor Helpful Audit

Competitor: ...
Target Query: ...

Helpful Strength: 68/100
Evidence Confidence: MEDIUM
Ranking Moat: 88/100
Attackability: MEDIUM

## What This Competitor Does Well
- ...

## Functional Weaknesses
- ...

## Reliability / Freshness Weaknesses
- ...

## UX Friction
- ...

## Trust Gaps
- ...

## Table Stakes We Must Match
- ...

## Gaps We Can Exploit
- ...

## Required Differentiation
- ...

## Do Not Fix
- ...

## Recommendation
ATTACK / CONDITIONAL / SKIP

Reason: ...
```

---

# SERP Audit Output Format

```markdown
# Helpful SERP Audit

Query: ...
Locale: ...
Utility Type: ...

## SERP Summary
Helpful Strength: WEAK / MEDIUM / STRONG
Evidence Confidence: HIGH / MEDIUM / LOW
Ranking Moat: LOW / MEDIUM / HIGH
Attackability: ...

## Competitor Table
| Result | Helpful | Ranking Moat | Reliability | Functional Depth | Main Weakness |
|---|---:|---:|---|---|---|
| A | 78 | 90 | Strong | Strong | Signup friction |
| B | 64 | 35 | Weak | Strong | Stale specs |
| C | 71 | 20 | Strong | Medium | No batch |

## SERP Table Stakes
- ...

## Relative Feature Coverage
| Feature | Coverage | Classification |
|---|---:|---|
| Local processing | 80% | Table Stakes |
| Batch | 70% | Table Stakes |
| Failure explanation | 20% | Partial Gap |
| Safe target margin | 0% | Real Gap |

## Reliability / Fact Gaps
- ...

## Best Opportunity
...

## Minimum MVP Required
1. ...
2. ...
3. ...

## Optional Differentiators
1. ...
2. ...

## Do Not Fix
- ...

## Verdict
ATTACK / CONDITIONAL / SKIP

## Why
...
```

---

# Evidence Requirements

Distinguish evidence from interpretation, and attach an evidence level to material observations.

Evidence levels:

```text
TESTED
OBSERVED
CLAIMED
UNKNOWN
```

## Evidence

Examples:

- tool visibly supports batch
- page claims local processing
- official source states current specification
- competitor requires login
- target is preconfigured
- page provides format X

## Interpretation

Examples:

- signup creates meaningful friction
- feature appears to be table stakes
- current reliability gap creates an opportunity
- domain moat is likely high

Do not present interpretation as observed fact.

For External-Spec Utilities:

1. identify material claims
2. locate primary source
3. record current official specification
4. compare competitor claim
5. report exact mismatch

Use secondary sources only when no authoritative primary source exists or when they provide independent performance data such as traffic estimates.

---

# Traffic and SEO Metrics

Traffic estimates are validation labels, not Helpful Score inputs.

Never do:

```text
Traffic = 500K
Therefore Helpful = 90
```

Instead:

```text
Helpful Score -> based on page evidence
Traffic / authority -> Ranking Moat / external validation
```

When using third-party traffic estimates, label them as estimates.

---

# Relative Feature Extraction

When auditing a SERP, build a normalized feature matrix.

Possible tool features include:

```text
exact target
batch
local processing
no signup
no download
preview
before/after
format support
HEIC / AVIF
compression quality
resize dimensions
crop
fit / contain / cover
failure explanation
safe margin
metadata removal
history
presets
mobile support
privacy disclosure
```

Do not assume these features are universally important.

Select only features relevant to the query.

For each feature, record:

```text
Present
Absent
Unclear
```

Then calculate SERP coverage.

---

# Reliability Checks by Tool Category

## Image Compression

Check:

- target behavior
- <= target vs exact target distinction
- dimensions fallback
- quality degradation claims
- metadata handling
- format conversion behavior
- local/server processing claims

Beware claims such as:

```text
compress from 5MB to 100KB without any quality loss
```

unless meaningfully qualified.

## Platform Asset Resizers

Check current platform rules from primary sources:

- dimensions
- aspect ratio
- file-size limits
- formats
- mobile vs desktop differences
- safe areas

## File Converters

Check:

- whether conversion actually happens locally/server-side as claimed
- output validity
- format limitations
- retention policy
- lossy/lossless behavior when material

## Downloaders

Check:

- whether promised download is actually available
- fake redirect behavior
- platform/legal restrictions when relevant
- misleading ads/buttons

---

# Anti-Patterns to Flag

## Content-Heavy / Function-Light

Pattern:

- long article
- weak or broken tool
- task hidden below content

Flag:

```text
Content-heavy / Functional-light
```

## Template-Heavy / State-Light

Pattern:

- many keyword pages
- title/H1 changes
- tool state remains generic

Flag:

```text
Programmatic differentiation weak
```

## Fake Freshness

Pattern:

- recent "updated" date
- material specs remain outdated

Do not accuse intent without evidence.

Say:

```text
The stated update date is recent, but the material specification remains inconsistent with the current primary source.
```

## Unsupported Superlatives

Examples:

```text
best
perfect
lossless
no quality loss
always exact
```

Require evidence or qualification.

## Trust Theater

Examples:

- fake expert badges
- invented reviews
- fake author photos
- unverifiable claims

Flag as a trust problem rather than a positive EEAT signal.

---

# Decision Rules

## Self Page

Recommend indexing/scaling when:

- core task works
- Helpful >= 75
- no critical hard gate
- page has a credible SERP replacement reason

Recommend improvement before scaling when:

- Helpful 65–74
- major functional or reliability gaps remain
- scaled-page family would multiply the weakness

Recommend not scaling when:

- Helpful <65
- task failure exists
- differentiation is negligible
- page family is demandless/stateless

## New Keyword / New Page

Recommend ATTACK when:

- meaningful demand exists
- SERP has a measurable helpful/function/reliability gap
- required MVP is feasible
- ranking moat is not uniformly prohibitive

Recommend CONDITIONAL when:

- gap exists but requires significant authority or product investment

Recommend SKIP when:

- top results are both functionally excellent and heavily protected
- no practical differentiation exists
- page would be a redundant programmatic variant

---

# Required Final Questions

Before finishing any audit, answer all of these:

1. What exact task is the user trying to complete?
2. Can the page actually complete it?
3. What does the current SERP consider table stakes?
4. What value is genuinely rare in the SERP?
5. Are any material claims false, stale, or unsupported?
6. What friction prevents task completion?
7. Why does this page deserve to exist independently?
8. Why should Google replace one current result with it?
9. How strong is the ranking moat independently of page helpfulness?
10. Is the opportunity worth attacking?
11. Which conclusions are TESTED, OBSERVED, CLAIMED, or UNKNOWN?
12. What should explicitly NOT be changed?

If these questions cannot be answered from available evidence, explicitly mark the uncertainty instead of inventing a score.

---

# Example — `compress image to 100kb`

Illustrative only; always rescan the current SERP.

```text
Utility Type: Stable Utility

SERP Table Stakes:
- exact target KB
- no signup
- local/browser processing
- batch on many competitors

Potential Real Gaps:
- target failure explanation
- quality-first vs size-first strategy
- dimension fallback explanation
- KB/KiB ambiguity handling
- safe upload margin
- portal-safe result mode

Implication:
"Local processing" alone should not receive high Information Gain if most current competitors already provide it.
```

---

# Example — `youtube thumbnail resizer free`

Illustrative only; always verify the current official YouTube specification.

```text
Utility Type: External-Spec Utility

Mandatory:
- verify dimensions
- verify aspect ratio
- verify upload limits
- distinguish desktop/mobile where relevant

Possible Helpful Gap:
- competitor pages may rank despite stale specs

Implication:
A high-authority competitor with outdated specifications may have:

Helpful Strength: Medium
Ranking Moat: Very High

These are not contradictory.
```

---

# Version 1.1 Operational Notes

This version is intentionally conservative about evidence and scoring.

Key rules:

1. Never give full Functional Completion credit to an untested workflow solely because the page claims a feature.
2. Reliability severity must distinguish Critical, Major, and Minor/Stale issues.
3. Relative Information Gain is dynamic against the current SERP, not a static feature checklist.
4. Avoid double-counting the same feature across multiple score dimensions.
5. Programmatic-page risk requires sibling sampling when a family exists.
6. Attackability is qualitative by default; avoid pseudo-precise formulas.
7. Every report must include `Do Not Fix` so optimization does not make an already-good page heavier or less usable.

---

# Skill Design Principle

The skill should optimize for this hierarchy:

```text
Real demand
-> Task completion
-> Reliability
-> Relative differentiation
-> Low-friction UX
-> Trust
-> Supporting explanation
```

Not:

```text
Word count
-> FAQ count
-> author box
-> generic SEO sections
-> keyword repetition
```

The final objective is not to create pages that look "SEO complete."

The objective is to create pages for which there is a clear answer to both:

> Why does the user need this page?

and

> Why should this page replace an existing search result?
