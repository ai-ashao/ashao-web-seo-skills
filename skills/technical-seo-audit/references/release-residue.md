# Public-facing release residue

This check exists for a common AI-assisted development failure mode: implementation-plan language, placeholders, deployment diagnostics, or backend terminology survives into the production UI even when the page is technically valid.

## Scope

Inspect static public-facing copy in:

- title and meta description;
- headings;
- CTA/control text;
- form labels and placeholders;
- links;
- alerts/status messages;
- list/table copy;
- visible body copy fallback.

Ignore script/style/template/noscript/SVG and code/preformatted blocks. Rendered-only copy remains unassessed until browser validation.

## Severity

### P0 - deterministic release blocker

Examples:

- TODO / FIXME / TBD;
- lorem placeholder text;
- raw runtime exceptions or stack-trace language;
- missing runtime/API configuration exposed to users;
- local development endpoints on ordinary public pages.

These are observable production-readiness defects. They are not claims about ranking impact.

### P1 - strong production-readiness review

Examples:

- MVP / minimum viable product;
- Phase 1 / Phase 2 implementation wording;
- internal notes and temporary-copy labels;
- mock/dummy output wording;
- staging/development/debug labels;
- explicit "not yet implemented" language.

A P1 match is not automatically wrong in every context. Confirm intended audience and whether the wording is deliberately public.

### P2 - contextual terminology review

Examples:

- R2 bucket / object storage;
- presigned URL;
- worker/job queue;
- job ID;
- process payload / invoke endpoint style action labels.

These may be correct in developer documentation. On a general tool/landing page, they often indicate implementation leakage or unnecessarily technical UX copy.

## Context handling

- DOCS, INTEGRATION, and SYSTEM routes suppress ordinary infrastructure-jargon rules.
- DOCS, INTEGRATION, CONTENT, and private/app routes downgrade development-process language where the terminology may be intentional.
- obvious deterministic residue remains reportable unless the rule itself is strongly context-dependent.
- path hints such as /docs, /api, /developers, /reference, and /changelog act as a technical-audience fallback.

## False-positive protocol

For every false positive, record:

1. rule code;
2. route class/page type;
3. exact observed text;
4. why the wording is appropriate for that audience;
5. whether to add a route exception, narrow the regex, or leave it as a P2 review.

Do not create broad allowlists from one example.

## False-negative protocol

When a human reviewer finds leaked development wording that the checker missed:

1. preserve a minimal anonymized HTML fixture;
2. add a regression test first;
3. add the narrowest rule that catches the fixture;
4. run the full test suite;
5. re-run the affected real sites to measure new noise.

## Calibration target

Use real production sites as the benchmark corpus.

- P0 should converge toward near-zero false positives.
- P1 should favor precision over exhaustive vocabulary coverage.
- P2 may remain broader because it is explicitly review-only.
- never turn release-residue matches into ranking, traffic, HCU, or keyword-demand claims.
