# [Candidate Direction] Architecture Opportunity Assessment

## 1. Executive conclusion

- **Candidate:**
- **Decision Profile:** `seo_first_utility` / `product_led` / `content_site` / `downloader` / `generic`
- **Target market/language:**
- **Opportunity score:** /100
- **Separation risk:** /100
- **Evidence confidence:** High / Medium / Low
- **Recommended architecture:** INDEPENDENT_SITE / EXISTING_SITE_SECTION / EXISTING_SITE_PAGE / OBSERVE_OR_REJECT

Explain in 3–5 sentences why this architecture is preferred.

## 2. Decision basis

### Decisive opportunities
-

### Decisive constraints
-

### Hard gates
- Status: not triggered / triggered
- Scope: `SITE_ONLY` / `BLOCK_PRODUCT`

## 3. Score details

| Dimension | Criterion | Raw score (0–5) | Weighted score | Evidence | Evidence type | Confidence |
|---|---|---:|---:|---|---|---|
| Search opportunity | Independent primary cluster | | /12 | | | |
| Search opportunity | SERP breakability | | /15 | | | |
| Search opportunity | Expansion system | | /12 | | | |
| Product differentiation | User/use-case difference | | /12 | | | |
| Product differentiation | Homepage workflow difference | | /10 | | | |
| Product differentiation | Independent brand reason | | /10 | | | |
| Independent growth | Link/distribution potential | | /10 | | | |
| Independent growth | Independent content system | | /9 | | | |
| Site economics | Development/maintenance economics | | /5 | | | |
| Site economics | Monetization fit | | /5 | | | |

## 4. Separation risk

| Risk | Raw score (0–5) | Weighted risk | Notes |
|---|---:|---:|---|
| Keyword overlap with host | | /20 | |
| Search-intent overlap | | /20 | |
| Product-workflow overlap | | /15 | |
| Content/template overlap | | /15 | |
| Brand-positioning ambiguity | | /10 | |
| Link-authority fragmentation | | /10 | |
| Development/maintenance fragmentation | | /10 | |

## 5. Demand / Keyword System Summary

- **Core demand cluster:**
- **Important synonyms/input-output variants:**
- **Independent expansion classes:**
- **Mechanical false long-tails to exclude:**
- **Primary datasets and dates:**
- **Conflicts/missing evidence:**

Describe whether the demand system supports the selected architecture. Do not create the final URL/Page Family map here.

## 6. SERP entry evidence

- **Dominant intent:**
- **Main result types:**
- **Specific entry evidence:**
- **Authority/link dependency:**
- **SERP confidence:**

## 7. Positioning and separation logic

| Dimension | Host/competitors | Candidate |
|---|---|---|
| Core user | | |
| Primary job | | |
| Entry demand | | |
| Workflow | | |
| Core promise | | |
| Content/page system | | |
| Link/share reason | | |
| Monetization | | |
| Maintenance burden | | |

## 8. Distribution and independent-brand reason

Explain who would link/share, why, and whether a separate domain creates a genuinely clearer category position.

## 9. Monetization and maintenance

- Monetization route:
- Main traffic geographies:
- Return-use logic:
- API/server/database requirements:
- Platform dependencies:
- Support/maintenance burden:

## 10. Minimum validation plan

- **Assumption to test:**
- **Validation vehicle:**
- **Success signal:**
- **Failure signal:**
- **Re-evaluation trigger:**

## 11. Handoff to SERP Siege

```yaml
opportunity_context:
  source: site-opportunity-scorecard
  decision_profile: ...
  destination: ...
  primary_job: ...
  primary_cluster: ...
  market: ...
  evidence_datasets:
    - ...
  constraints:
    - ...
  exclusions:
    - ...
  unresolved_questions:
    - ...
```

Do not continue into an SEO Page Map or First Batch in this report.

## 12. Final decision

> Build [candidate direction] as [INDEPENDENT_SITE / EXISTING_SITE_SECTION / EXISTING_SITE_PAGE / OBSERVE_OR_REJECT]; hand downstream page planning to SERP Siege.
