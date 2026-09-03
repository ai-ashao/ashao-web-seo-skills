#!/usr/bin/env python3
"""Directional traffic sanity check for Downloader Radar v3.

Example:
  python scripts/traffic_sanity_check.py \
    --monthly-visits 611660 --search-share-pct 61.15 \
    --target-keyword-traffic 47000

The output is diagnostic only. Third-party traffic tools use different scopes
and models; do not treat calculated values as analytics truth.
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--monthly-visits", type=float)
parser.add_argument("--search-share-pct", type=float)
parser.add_argument("--organic-traffic", type=float)
parser.add_argument("--target-keyword-traffic", type=float)
parser.add_argument("--target-page-traffic", type=float)
parser.add_argument("--same-scope", action="store_true", help="Metrics are from the same tool/market/time scope")
args = parser.parse_args()

implied_search = None
if args.monthly_visits is not None and args.search_share_pct is not None:
    implied_search = args.monthly_visits * args.search_share_pct / 100.0
    print(f"implied_search_visits: {implied_search:.0f}")

if implied_search and args.target_keyword_traffic is not None:
    print(f"target_keyword_share_of_implied_search: {args.target_keyword_traffic / implied_search:.2%}")

if args.organic_traffic and args.target_page_traffic is not None:
    print(f"target_page_share_of_organic: {args.target_page_traffic / args.organic_traffic:.2%}")

flags = []
if args.same_scope and implied_search and args.organic_traffic:
    hi = max(implied_search, args.organic_traffic)
    lo = max(1.0, min(implied_search, args.organic_traffic))
    ratio = hi / lo
    print(f"search_vs_organic_ratio: {ratio:.2f}x")
    if ratio > 5:
        flags.append("TRAFFIC_ESTIMATE_CONFLICT")

if args.monthly_visits is not None and args.organic_traffic is not None and args.same_scope:
    if args.organic_traffic > args.monthly_visits * 1.5:
        flags.append("SCOPE_OR_MODEL_CHECK_REQUIRED")

if flags:
    print("flags: " + ",".join(sorted(set(flags))))
else:
    print("flags: none_detected")

print("note: directional sanity check only; reconcile source, country, time period, and metric definitions before drawing conclusions")
