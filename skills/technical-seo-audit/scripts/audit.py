#!/usr/bin/env python3
"""Unified technical SEO audit with optional SEO-first bounded site mode."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from check_page import audit_page
from check_site import audit_site
from profiles import PROFILES, ROUTE_CLASSES, detect_profile
from site_audit import run_site_audit


def _safe_cell(value: object) -> str:
    return str(value if value is not None else "—").replace("|", "\\|").replace("\n", " ")


def _display_origin(url: str | None) -> str | None:
    if not url: return None
    parsed = urlsplit(url if "://" in url else f"https://{url}")
    if not parsed.scheme or not parsed.netloc: return None
    return f"{parsed.scheme.lower()}://{parsed.netloc.lower()}"


def _rows(evidence: dict[str, object]) -> list[tuple[str, str, str]]:
    rows = []
    site = evidence.get("site", {})
    if isinstance(site, dict) and site.get("status") != "error":
        for name in ("robots", "sitemap"):
            check = site.get(name, {})
            if isinstance(check, dict): rows.append((name, str(check.get("status", "unassessed")), str(check.get("detail", ""))))
    page = evidence.get("page", {})
    if isinstance(page, dict) and page.get("status") != "error":
        for name, check in page.get("checks", {}).items():
            if isinstance(check, dict): rows.append((name, str(check.get("status", "unassessed")), str(check.get("detail", ""))))
    return rows


def render_markdown(evidence: dict[str, object], evidence_path: Path) -> str:
    page = evidence.get("page", {}) if isinstance(evidence.get("page"), dict) else {}
    rows = _rows(evidence)
    lines = [
        f"# Technical SEO Audit: {evidence['target_url']}", "", "## Scope and profile", "",
        f"- Requested profile: `{evidence.get('requested_profile')}`",
        f"- Effective page profile: `{page.get('profile', 'unassessed')}`",
        f"- Route class: `{page.get('route_class', 'unassessed')}`",
        f"- Expected indexable: `{page.get('expected_indexable', 'unassessed')}`",
        f"- Expected multilingual: `{str(evidence.get('expected_multilingual')).lower()}`",
        f"- Target query supplied: `{evidence.get('keyword') or 'none'}`",
        f"- Requested origin: `{evidence.get('requested_origin') or 'unavailable'}`",
        f"- Final origin: `{evidence.get('final_origin') or 'unavailable'}`",
        f"- Site mode: `{str(evidence.get('site_mode')).lower()}`",
        f"- Raw evidence: `{evidence_path.name}`", "",
        "## Deterministic evidence", "", "| Check | Status | Observation |", "| --- | --- | --- |",
    ]
    lines.extend(f"| `{_safe_cell(name)}` | `{_safe_cell(status)}` | {_safe_cell(detail)} |" for name, status, detail in rows)
    site_mode = evidence.get("site_audit")
    if isinstance(site_mode, dict):
        detection = site_mode.get("profile_detection", {})
        analysis = site_mode.get("analysis", {})
        lines.extend(["", "## SEO-first site audit", "",
                      f"- Effective site profile: `{site_mode.get('effective_profile')}`",
                      f"- Profile confidence: `{detection.get('confidence', 'unassessed')}`",
                      f"- Pages checked: `{analysis.get('pages_checked', 0)}`", ""])
        findings = analysis.get("findings", []) if isinstance(analysis, dict) else []
        if findings:
            lines.extend(["| Priority | Code | URL | Finding |", "| --- | --- | --- | --- |"])
            for finding in findings:
                lines.append(f"| `{_safe_cell(finding.get('priority'))}` | `{_safe_cell(finding.get('code'))}` | {_safe_cell(finding.get('url'))} | {_safe_cell(finding.get('detail'))} |")
        else:
            lines.append("No P0–P2 site-architecture findings were produced within the crawl bound.")
    lines.extend(["", "## Evidence limits", "",
                  "- Public fetches do not prove Google indexation, rankings, traffic, crawl frequency, or GSC status.",
                  "- Static HTML checks do not prove rendered DOM parity; scripted pages remain browser-review candidates.",
                  "- Bounded crawl results do not prove the absence of orphan pages outside the checked inventory.",
                  "- Route classification is a policy aid. Explicit product intent overrides automatic classification.", "",
                  "## Re-check", "", "Re-run the same command after remediation. For scripted public landing pages, compare rendered DOM with static HTML separately."])
    return "\n".join(lines) + "\n"


def default_report_path(url: str) -> Path:
    parsed = urlsplit(url if "://" in url else f"https://{url}")
    slug = re.sub(r"[^a-z0-9]+", "-", f"{parsed.netloc}{parsed.path}".lower()).strip("-") or "site"
    return Path("reports") / f"{slug}-technical-seo-audit.md"


def collect_evidence(url: str, keyword: str | None, requested_profile: str, route_class: str | None,
                     indexability: str, expected_multilingual: bool, validate_hreflang: bool,
                     validate_canonical: bool, site_mode: bool, max_pages: int, max_hreflang: int,
                     max_sitemaps: int, timeout: int) -> dict[str, object]:
    page_profile = requested_profile
    if requested_profile == "auto":
        page_profile = str(detect_profile([url])["profile"])
    expected = None if indexability == "auto" else indexability == "expected"
    page = audit_page(url, keyword, expected, expected_multilingual, validate_hreflang, max_hreflang,
                      timeout, validate_canonical, page_profile, route_class)
    final_url = page.get("final_url") if isinstance(page.get("final_url"), str) else None
    site_target = final_url or url
    site = audit_site(site_target, timeout, max_sitemaps)
    requested_origin = _display_origin(url)
    final_origin = _display_origin(final_url)
    site_audit_origin = site.get("origin") if isinstance(site.get("origin"), str) else _display_origin(site_target)
    if isinstance(site_audit_origin, str): site_audit_origin = site_audit_origin.rstrip("/")
    evidence: dict[str, object] = {
        "target_url": url, "requested_profile": requested_profile, "requested_origin": requested_origin,
        "final_url": final_url, "final_origin": final_origin, "site_audit_origin": site_audit_origin,
        "origin_changed": requested_origin != final_origin if requested_origin and final_origin else None,
        "expected_multilingual": expected_multilingual, "keyword": keyword, "site_mode": site_mode,
        "site": site, "page": page,
    }
    if site_mode and isinstance(site, dict) and site.get("status") != "error":
        sitemap_urls = site.get("sitemap", {}).get("page_urls", []) if isinstance(site.get("sitemap"), dict) else []
        root = str(site.get("origin") or site_target)
        evidence["site_audit"] = run_site_audit(root, sitemap_urls, requested_profile, max_pages, timeout)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an evidence-led technical SEO audit with optional SEO-first site mode.")
    parser.add_argument("url")
    parser.add_argument("--keyword")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="auto")
    parser.add_argument("--route-class", choices=sorted(ROUTE_CLASSES))
    parser.add_argument("--indexability", choices=["auto", "expected", "excluded"], default="auto")
    parser.add_argument("--site", action="store_true", help="Run bounded crawl/site-architecture checks.")
    parser.add_argument("--multilingual", action="store_true")
    parser.add_argument("--validate-hreflang", action="store_true")
    parser.add_argument("--skip-canonical-validation", action="store_true")
    parser.add_argument("--max-pages", type=int, default=200)
    parser.add_argument("--max-hreflang", type=int, default=12)
    parser.add_argument("--max-sitemaps", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    evidence = collect_evidence(args.url, args.keyword, args.profile, args.route_class, args.indexability,
                                args.multilingual, args.validate_hreflang, not args.skip_canonical_validation,
                                args.site, args.max_pages, args.max_hreflang, args.max_sitemaps, args.timeout)
    report_path = args.output or default_report_path(args.url)
    evidence_path = report_path.with_suffix(".json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report_path.write_text(render_markdown(evidence, evidence_path), encoding="utf-8")
    print(json.dumps({"report": str(report_path), "evidence": str(evidence_path)}, ensure_ascii=False))
    has_error = any(isinstance(evidence.get(key), dict) and evidence[key].get("status") == "error" for key in ("site", "page"))
    has_failure = any(status == "fail" for _, status, _ in _rows(evidence))
    site_findings = evidence.get("site_audit", {}).get("analysis", {}).get("findings", []) if isinstance(evidence.get("site_audit"), dict) else []
    release_block = any(item.get("priority") in {"P0", "P1"} for item in site_findings)
    return 1 if has_error or has_failure or release_block else 0

if __name__ == "__main__":
    sys.exit(main())
