#!/usr/bin/env python3
"""Deterministic helper for Pain Mining v0.2 evidence scoring.

Input: JSON file containing a list of evidence items.
Required fields per item:
  type, thread_id, pain_cluster
Optional booleans:
  concrete_consequence, workaround, recent_24m, payment_or_paid_switch

Important v0.2 rule:
- E_DEVELOPER_PROMO always scores 0, regardless of recency or other bonuses.
- Cluster confidence uses independent USER-ORIGIN threads (A/B/C), so promotion
  or ambiguous evidence cannot upgrade demand confidence by itself.

This script is intentionally small and auditable. It does not infer evidence types.
"""

import json
import sys
from collections import defaultdict

BASE = {
    "A_USER_REQUEST": 3.0,
    "B_FIRSTHAND_COMPLAINT": 3.0,
    "C_FEATURE_REQUEST": 2.0,
    "D_RECOMMENDATION": 1.0,
    "E_DEVELOPER_PROMO": 0.0,
    "F_SECONDHAND_OR_AMBIGUOUS": 0.5,
}

USER_ORIGIN = {"A_USER_REQUEST", "B_FIRSTHAND_COMPLAINT", "C_FEATURE_REQUEST"}
AB_TYPES = {"A_USER_REQUEST", "B_FIRSTHAND_COMPLAINT"}


def item_score(item):
    evidence_type = item.get("type")
    if evidence_type == "E_DEVELOPER_PROMO":
        return 0.0

    score = BASE.get(evidence_type, 0.0)
    score += 1.0 if item.get("concrete_consequence") else 0.0
    score += 1.0 if item.get("workaround") else 0.0
    score += 0.5 if item.get("recent_24m") else 0.0
    score += 0.5 if item.get("payment_or_paid_switch") else 0.0
    return min(score, 5.0)


def main(path):
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)

    clusters = defaultdict(list)
    for idx, item in enumerate(items, start=1):
        item = dict(item)
        item["_score"] = item_score(item)
        item["_id"] = item.get("id", f"E{idx:03d}")
        clusters[item.get("pain_cluster", "UNCLUSTERED")].append(item)

    output = []
    for cluster, rows in sorted(clusters.items()):
        per_thread = defaultdict(float)
        all_threads = set()
        user_origin_threads = set()
        user_origin_items = 0
        promo_items = 0

        for row in rows:
            thread = row.get("thread_id") or row["_id"]
            all_threads.add(thread)
            per_thread[thread] += row["_score"]
            if row.get("type") in USER_ORIGIN:
                user_origin_items += 1
                user_origin_threads.add(thread)
            if row.get("type") == "E_DEVELOPER_PROMO":
                promo_items += 1

        capped_score = sum(min(v, 4.0) for v in per_thread.values())
        ab_count = sum(1 for r in rows if r.get("type") in AB_TYPES)

        if len(user_origin_threads) >= 3 and ab_count >= 2 and capped_score >= 8:
            confidence = "HIGH"
        elif len(user_origin_threads) >= 2 and capped_score >= 4:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        output.append({
            "pain_cluster": cluster,
            "confidence": confidence,
            "independent_threads": len(all_threads),
            "user_origin_threads": len(user_origin_threads),
            "evidence_items": len(rows),
            "user_origin_items": user_origin_items,
            "developer_promo_items": promo_items,
            "evidence_score": round(capped_score, 2),
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: score_evidence.py evidence.json")
    main(sys.argv[1])
