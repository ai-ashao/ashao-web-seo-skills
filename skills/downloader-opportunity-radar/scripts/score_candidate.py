#!/usr/bin/env python3
"""Score a Downloader Opportunity Radar v3 candidate and enforce gates.

Positional dimensions (max):
  young_domain_serp 25
  serp_weakness 12
  demand_traffic 18
  cluster_depth 12
  product_feasibility 12
  maintenance 8
  monetization 5
  timing 4
  durability 4

Example:
  python scripts/score_candidate.py 23 10 16 10 9 6 4 4 3 \
    --age-proof strong --demand-grade breakout \
    --attribution-confidence high --target-keyword-count 5 \
    --attributable-search-visits 47000
"""

import argparse

LABELS = [
    ("young_domain_serp", 25),
    ("serp_weakness", 12),
    ("demand_traffic", 18),
    ("cluster_depth", 12),
    ("product_feasibility", 12),
    ("maintenance", 8),
    ("monetization", 5),
    ("timing", 4),
    ("durability", 4),
]

parser = argparse.ArgumentParser()
for name, maxv in LABELS:
    parser.add_argument(name, type=int, help=f"0-{maxv}")

parser.add_argument("--age-proof", choices=["strong", "general", "weak", "old", "none"], required=True)
parser.add_argument("--general-top5", action="store_true")
parser.add_argument("--general-count", type=int, default=0)
parser.add_argument("--serp-fragmented", action="store_true")
parser.add_argument("--demand-grade", choices=["breakout", "strong", "moderate", "weak", "unknown"], default="unknown")
parser.add_argument("--attribution-confidence", choices=["high", "medium", "low", "conflict"], default="low")
parser.add_argument("--target-keyword-count", type=int, default=0)
parser.add_argument("--target-page-count", type=int, default=0)
parser.add_argument("--attributable-search-visits", type=float, default=0)
parser.add_argument("--traffic-conflict", action="store_true")
parser.add_argument("--policy-hard-reject", action="store_true")
parser.add_argument("--policy-shock", action="store_true")
args = parser.parse_args()

values = [getattr(args, name) for name, _ in LABELS]
for (name, maxv), value in zip(LABELS, values):
    if value < 0 or value > maxv:
        parser.error(f"{name} must be between 0 and {maxv}")

total = sum(values)

# Generic hard caps.
if args.age_proof in {"old", "none"}:
    total = min(total, 59)
if values[3] <= 5:  # shallow cluster
    total = min(total, 64)
if values[4] <= 5:  # fragile product feasibility
    total = min(total, 64)

# Unresolved traffic conflict caps demand dimension effect and breakout label.
traffic_conflict = args.traffic_conflict or args.attribution_confidence == "conflict"
if traffic_conflict and values[2] > 9:
    total -= values[2] - 9

# Age gate.
age_gate = False
if args.age_proof == "strong":
    age_gate = True
    age_note = "<=6-month Top 10 proof: age gate passed"
elif args.age_proof == "general":
    age_gate = args.general_top5 or (args.general_count >= 2 and args.serp_fragmented)
    age_note = "6–12-month proof: age gate passed" if age_gate else "6–12-month proof insufficient for TEST NOW"
elif args.age_proof == "weak":
    total = min(total, 77)
    age_note = "12–18-month proof only: WATCH ceiling"
elif args.age_proof == "old":
    age_note = ">18-month domains are old: no fresh-site proof"
else:
    age_note = "No usable domain-age proof"

hard_reject = args.policy_hard_reject or values[8] == 0

if hard_reject:
    decision = "REJECT"
elif total >= 78 and age_gate:
    decision = "TEST NOW"
elif total >= 65:
    decision = "WATCH"
else:
    decision = "REJECT"

breakout_gate = (
    decision == "TEST NOW"
    and args.demand_grade == "breakout"
    and args.attribution_confidence in {"high", "medium"}
    and not traffic_conflict
    and args.attributable_search_visits >= 10000
    and (args.target_keyword_count >= 3 or args.target_page_count >= 2)
    and not hard_reject
)

tier = "PROVEN BREAKOUT" if breakout_gate else decision

for (name, _), value in zip(LABELS, values):
    print(f"{name}: {value}")
print(f"age_proof: {args.age_proof}")
print(f"age_gate: {'PASS' if age_gate else 'FAIL'}")
print(f"age_note: {age_note}")
print(f"demand_grade: {args.demand_grade}")
print(f"attribution_confidence: {args.attribution_confidence}")
print(f"traffic_conflict: {'YES' if traffic_conflict else 'NO'}")
print(f"policy_shock: {'YES' if args.policy_shock else 'NO'}")
print(f"total: {total}")
print(f"decision: {decision}")
print(f"tier: {tier}")
