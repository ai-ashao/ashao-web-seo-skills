#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors: list[str] = []
    warnings: list[str] = []

    required = [
        "SKILL.md",
        "references/inspection-guide.md",
        "references/extraction-recipes.md",
        "references/integration-guide.md",
        "references/qa-guide.md",
        "references/rights-and-provenance.md",
        "references/temporary-assets-guide.md",
        "templates/component-spec.md",
        "templates/project-context.md",
        "templates/implementation-plan.md",
        "templates/asset-manifest.json",
        "scripts/check-reference-assets.mjs",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append(f"Missing required resource: {rel}")

    skill = root / "SKILL.md"
    if skill.exists():
        text = skill.read_text(encoding="utf-8")
        phrases = (
            "# Reference Website Builder v2.1",
            "### `analyze`",
            "### `prototype`",
            "### `adapt`",
            "### `full`",
            "KEEP / CHANGE / ADD / OMIT",
            "Do not crawl the sitemap",
            "## Output isolation contract",
            "## Deterministic reconstruction kernel",
            "## Foreman pipeline",
            "## Pre-dispatch gate",
            "site-key",
            "page-key",
        )
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"SKILL.md missing v2.1 contract: {phrase}")
        if len(text.splitlines()) > 350:
            warnings.append("SKILL.md is longer than the lightweight target (350 lines).")
        if "lightest" not in text.lower():
            errors.append("SKILL.md must preserve lightweight mode selection.")

    extraction = root / "references/extraction-recipes.md"
    if extraction.exists():
        text = extraction.read_text(encoding="utf-8")
        for phrase in ("getComputedStyle", "Page asset discovery", "Interaction-state capture", "Builder evidence packet"):
            if phrase not in text:
                errors.append(f"Extraction recipes missing contract: {phrase}")

    component = root / "templates/component-spec.md"
    if component.exists():
        text = component.read_text(encoding="utf-8")
        for phrase in ("## Pre-dispatch gate", "Interaction model", "Measured styles", "Responsive behavior"):
            if phrase not in text:
                errors.append(f"Component spec missing v2.1 section: {phrase}")

    manifest = root / "templates/asset-manifest.json"
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if data.get("schemaVersion", 0) < 2:
                errors.append("Asset manifest schemaVersion must be >= 2.")
            for key in ("siteKey", "pageKey"):
                if not data.get(key):
                    errors.append(f"Asset manifest missing {key}.")
        except json.JSONDecodeError as exc:
            errors.append(f"Asset manifest is not valid JSON: {exc}")

    gate = root / "scripts/check-reference-assets.mjs"
    if gate.exists():
        text = gate.read_text(encoding="utf-8")
        if "process.exit(1)" not in text:
            errors.append("Reference asset gate does not appear to fail on issues.")
        for pattern in (r"rmSync\(", r"unlinkSync\(", r"fetch\(", r"child_process"):
            if re.search(pattern, text):
                errors.append(f"Reference asset gate must remain read-only; found {pattern}")

    print(f"Validating: {root}")
    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")
    if errors:
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())