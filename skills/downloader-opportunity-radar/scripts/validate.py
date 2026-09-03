#!/usr/bin/env python3
"""Run deterministic validation for Downloader Opportunity Radar v3."""

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PY = sys.executable


def run(cmd):
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(f"Command failed: {' '.join(map(str, cmd))}\n{result.stdout}\n{result.stderr}")
    return result.stdout


# Keyword permutation regression: the Threads calibration must include word-order variants.
out = run([PY, "scripts/generate_keywords.py", "Threads", "--assets", "video"])
required = {
    "Threads downloader",
    "Threads download",
    "download Threads",
    "Threads video downloader",
    "Threads video download",
    "download Threads video",
    "download video Threads",
}
missing = [kw for kw in required if kw not in out.splitlines()]
if missing:
    raise AssertionError(f"Missing required core permutations: {missing}")

# Score fixtures.
for fixture_path in sorted((ROOT / "fixtures").glob("*.json")):
    data = json.loads(fixture_path.read_text())
    cmd = [PY, "scripts/score_candidate.py", *map(str, data["scores"]), *data["args"]]
    output = run(cmd)
    tier_line = next((line for line in output.splitlines() if line.startswith("tier: ")), None)
    if tier_line is None:
        raise AssertionError(f"No tier emitted for {fixture_path.name}")
    actual = tier_line.split(": ", 1)[1]
    if actual != data["expected_tier"]:
        raise AssertionError(
            f"{fixture_path.name}: expected {data['expected_tier']}, got {actual}\n{output}"
        )

print("PASS: keyword permutations and scoring fixtures")
