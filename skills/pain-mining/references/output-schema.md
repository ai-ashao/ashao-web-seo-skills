# Structured Output Schema — v0.2

Use this structure internally when possible.

```json
{
  "scope": {
    "seed": "",
    "mode": "general|tool_site",
    "platform": "",
    "audience": "",
    "time_window": "",
    "sources": []
  },
  "corpus": {
    "queries_run": 0,
    "query_reframes": 0,
    "unique_threads": 0,
    "evidence_items": 0,
    "user_origin_items": 0,
    "developer_promo_items": 0,
    "ambiguous_items": 0
  },
  "query_performance": [
    {
      "query": "",
      "batch": 1,
      "framing": "PRODUCT_TERM|TASK_LANGUAGE|CONSTRAINT|WORKAROUND|COMMUNITY_RESTRICTED",
      "relevant_results": 0,
      "inspected_results": 0,
      "yield": "GOOD|OK|POOR",
      "reframe_of": null
    }
  ],
  "pain_clusters": [
    {
      "name": "",
      "confidence": "HIGH|MEDIUM|LOW",
      "independent_threads": 0,
      "user_origin_threads": 0,
      "evidence_score": 0,
      "user_origin_items": 0,
      "recent_items": 0,
      "workaround_mentions": 0,
      "switching_mentions": 0,
      "evidence_ids": []
    }
  ],
  "evidence": [
    {
      "id": "E001",
      "type": "A_USER_REQUEST",
      "date": "",
      "source": "Reddit",
      "community": "",
      "url": "",
      "query": "",
      "summary": "",
      "excerpt": "",
      "pain_cluster": "",
      "consequence": "",
      "workaround": "",
      "competitor": "",
      "self_promo": false
    }
  ],
  "workaround_chains": [
    {
      "job": "",
      "steps": [""],
      "independent_threads": 0,
      "opportunity_inference": ""
    }
  ],
  "feature_implications": [
    {
      "feature": "",
      "evidence_level": "DIRECT|INFERRED|SPECULATIVE",
      "pain_clusters": [],
      "rationale": ""
    }
  ],
  "tool_site_actions": [
    {
      "finding": "",
      "action_type": "FEATURE|PAGE_CANDIDATE|HOMEPAGE_COPY|FAQ_GUIDE",
      "candidate_query": "",
      "evidence_level": "DIRECT|INFERRED|SPECULATIVE",
      "supporting_clusters": [],
      "why_distinct": "",
      "seo_validation_status": "REQUIRED|NOT_APPLICABLE"
    }
  ],
  "competitors": [],
  "weak_hypotheses": [],
  "next_validation": []
}
```

## Tool-site guardrail

`PAGE_CANDIDATE` means only:

> The corpus shows a distinct user job or constraint that could plausibly map to a standalone page.

It does **not** mean:

- meaningful search volume exists
- the SERP is weak
- the page should be built
- the keyword is commercially valuable

Those require downstream keyword/SERP validation.
