#!/usr/bin/env python3
"""Generate a Downloader Radar v3 core Intent Permutation Set.

Usage:
  python scripts/generate_keywords.py Threads
  python scripts/generate_keywords.py Threads --assets video,image,profile-picture,gif
  python scripts/generate_keywords.py Threads --format tsv

This script intentionally generates CORE permutations only. Secondary modifiers
like free/online/iPhone/HD belong to later SERP expansion.
"""

import argparse
import re

DEFAULT_ASSETS = [
    "video", "image", "photo", "carousel", "gif",
    "profile picture", "pfp", "dp", "avatar", "thumbnail",
]

ASSET_ALIASES = {
    "profile-picture": "profile picture",
    "profile_picture": "profile picture",
    "cover-art": "cover art",
    "cover_art": "cover art",
}


def normalize_asset(asset: str) -> str:
    asset = asset.strip().lower()
    return ASSET_ALIASES.get(asset, asset.replace("-", " "))


def canonical_asset(asset: str) -> str:
    if asset in {"profile picture", "pfp", "dp", "avatar"}:
        return "profile-picture"
    if asset in {"image", "photo"}:
        return "image"
    return re.sub(r"\s+", "-", asset.strip())


def add(rows, seen, keyword, canonical, asset, pattern):
    key = keyword.casefold().strip()
    if key in seen:
        return
    seen.add(key)
    rows.append({
        "keyword": keyword,
        "canonical_intent": canonical,
        "asset": asset or "platform",
        "pattern": pattern,
    })


parser = argparse.ArgumentParser()
parser.add_argument("platform", nargs="+", help="Platform name, e.g. Threads")
parser.add_argument(
    "--assets",
    default=",".join(DEFAULT_ASSETS),
    help="Comma-separated assets; default covers common media and identity assets",
)
parser.add_argument("--format", choices=["plain", "tsv"], default="plain")
args = parser.parse_args()

platform = " ".join(args.platform).strip()
assets = [normalize_asset(x) for x in args.assets.split(",") if x.strip()]

rows = []
seen = set()

# Platform head intent.
for kw, pattern in [
    (f"{platform} downloader", "platform_downloader"),
    (f"{platform} download", "platform_download"),
    (f"download {platform}", "download_platform"),
]:
    add(rows, seen, kw, "platform-download", "", pattern)

# Asset intent permutations.
for asset in assets:
    canon = f"{canonical_asset(asset)}-download"
    candidates = [
        (f"{platform} {asset} downloader", "platform_asset_downloader"),
        (f"{platform} {asset} download", "platform_asset_download"),
        (f"download {platform} {asset}", "download_platform_asset"),
        (f"download {asset} {platform}", "download_asset_platform"),
    ]
    for kw, pattern in candidates:
        add(rows, seen, kw, canon, asset, pattern)

if args.format == "tsv":
    print("keyword\tcanonical_intent\tasset\tpattern")
    for row in rows:
        print(f"{row['keyword']}\t{row['canonical_intent']}\t{row['asset']}\t{row['pattern']}")
else:
    for row in rows:
        print(row["keyword"])
