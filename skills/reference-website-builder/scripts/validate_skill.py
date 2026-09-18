#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path

def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
    errors=[]; warnings=[]
    required=["SKILL.md","references/inspection-guide.md","references/integration-guide.md","references/qa-guide.md","references/rights-and-provenance.md","references/temporary-assets-guide.md","scripts/check-reference-assets.mjs"]
    for rel in required:
        if not (root/rel).exists(): errors.append(f"Missing required resource: {rel}")
    p=root/"SKILL.md"
    if p.exists():
        text=p.read_text(encoding="utf-8")
        for phrase in ("### `analyze`","### `prototype`","### `adapt`","### `full`","KEEP / CHANGE / ADD / OMIT","Do not crawl the sitemap"):
            if phrase not in text: errors.append(f"SKILL.md missing consolidation contract: {phrase}")
        if len(text.splitlines())>350: warnings.append("SKILL.md is longer than the lightweight consolidation target (350 lines).")
        if "default" not in text.lower(): errors.append("SKILL.md must define a lightweight default behavior.")
    gate=root/"scripts/check-reference-assets.mjs"
    if gate.exists():
        t=gate.read_text(encoding="utf-8")
        if "process.exit(1)" not in t: errors.append("Reference asset gate does not appear to fail on issues.")
        for pattern in (r"rmSync\(",r"unlinkSync\(",r"fetch\(",r"child_process"):
            if re.search(pattern,t): errors.append(f"Reference asset gate must remain read-only; found {pattern}")
    print(f"Validating: {root}")
    for w in warnings: print(f"warning: {w}")
    for e in errors: print(f"error: {e}")
    if errors: return 1
    print("Validation passed."); return 0
if __name__=="__main__": raise SystemExit(main())
