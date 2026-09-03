# Helpful Value Audit Skill v1.1

A Codex-ready skill for auditing SEO utility/tool pages.

## What it does

Supports three workflows:

- **Self Audit** — Is my page good enough to index or scale?
- **Competitor Audit** — Where is a specific competing page weak?
- **SERP Audit** — What are the current table stakes, real gaps, ranking moat, and attackability for a query?

The skill separates:

- Helpful Strength
- Ranking Moat
- Attackability

It does **not** claim to calculate a Google HCU score.

## Install

Unzip the package and install the `helpful-value-audit` folder as a Codex skill using your normal Codex skill installation workflow. Keep `SKILL.md` at the root of the skill directory.

Expected structure:

```text
helpful-value-audit/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    └── calibration-notes.md
```

## Typical prompts

```text
Use helpful-value-audit to audit https://example.com/tool for the query "compress image to 100kb".
```

```text
Use helpful-value-audit to compare the current SERP for "youtube thumbnail resizer free" and tell me whether to ATTACK, CONDITIONAL, or SKIP.
```

```text
Use helpful-value-audit on my local page before I add it to the sitemap. Treat this as a pre-index quality gate.
```

## Core scoring

```text
Intent & Task Match          20
Functional Completion       30
Relative Information Gain   15
Reliability & Claim Accuracy15
Task UX / Friction          10
Trust / Transparency         5
Supporting Content           5
Total                      100
```

## v1.1 additions

- Evidence levels: TESTED / OBSERVED / CLAIMED / UNKNOWN
- Reliability severity: Critical / Major / Minor-Stale
- Dynamic SERP table-stakes bands
- Score-inflation / double-count prevention
- Required sibling sampling for programmatic page families
- Qualitative Attackability by default
- Mandatory `Do Not Fix` section
