#!/usr/bin/env python3
"""Inspect observable on-page technical SEO signals from bounded static HTML."""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin, urlsplit

from profiles import ROUTE_CLASSES, decide_route
from url_safety import UnsafeUrlError, safe_fetch

ROBOTS_DIRECTIVE_NAMES = {
    "all", "follow", "index", "indexifembedded", "max-image-preview", "max-snippet",
    "max-video-preview", "noarchive", "nofollow", "noimageindex", "noindex", "none",
    "nosnippet", "notranslate", "unavailable_after",
}
# Google hreflang uses a two-letter language, optional ISO 15924 script, and optional
# two-letter region. Numeric macroregions such as es-419 are intentionally rejected.
LANGUAGE = re.compile(r"^[A-Za-z]{2}$")
SCRIPT = re.compile(r"^[A-Za-z]{4}$")
REGION = re.compile(r"^[A-Za-z]{2}$")


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _without_fragment(url: str) -> str:
    parsed = urlsplit(url)
    return parsed._replace(fragment="").geturl()


def _normalize_for_compare(url: str) -> str:
    parsed = urlsplit(_without_fragment(url))
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return parsed._replace(scheme=parsed.scheme.lower(), netloc=parsed.netloc.lower(), path=path).geturl()


def _directive_tokens(values: str | list[str] | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    tokens: list[str] = []
    for value in values:
        tokens.extend(token for segment in value.lower().split(",") for token in segment.strip().split() if token)
    return tokens


def parse_directives(
    meta_robots: str | list[str] | None,
    meta_googlebot: str | list[str] | None,
    x_robots_headers: str | None,
    target_agent: str = "googlebot",
) -> dict[str, object]:
    """Return effective directives for one crawler while preserving scope boundaries."""
    target_agent = target_agent.lower()
    effective = _directive_tokens(meta_robots)
    ignored_scopes: dict[str, list[str]] = {}
    if target_agent == "googlebot":
        effective.extend(_directive_tokens(meta_googlebot))
    elif meta_googlebot:
        ignored_scopes["googlebot"] = _directive_tokens(meta_googlebot)

    for header_value in (x_robots_headers or "").splitlines():
        current_scope: str | None = None
        for raw_segment in header_value.split(","):
            segment = raw_segment.strip()
            if not segment:
                continue
            scoped = re.match(r"^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$", segment)
            if scoped and scoped.group(1).lower() not in ROBOTS_DIRECTIVE_NAMES:
                current_scope = scoped.group(1).lower()
                segment = scoped.group(2).strip()
            tokens = _directive_tokens(segment)
            if current_scope is None or current_scope == target_agent:
                effective.extend(tokens)
            elif tokens:
                ignored_scopes.setdefault(current_scope, []).extend(tokens)
    return {
        "target_agent": target_agent,
        "directives": sorted(set(effective)),
        "ignored_scoped_directives": {scope: sorted(set(tokens)) for scope, tokens in sorted(ignored_scopes.items())},
    }


def hreflang_code_supported_format(code: str) -> bool:
    if code.lower() == "x-default":
        return True
    parts = code.split("-")
    if not parts or not LANGUAGE.fullmatch(parts[0]):
        return False
    if len(parts) == 1:
        return True
    if len(parts) == 2:
        return bool(SCRIPT.fullmatch(parts[1]) or REGION.fullmatch(parts[1]))
    if len(parts) == 3:
        return bool(SCRIPT.fullmatch(parts[1]) and REGION.fullmatch(parts[2]))
    return False


class PageParser(HTMLParser):
    def __init__(self, final_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.final_url = final_url
        self.html_lang: str | None = None
        self.title_parts: list[str] = []
        self.in_title = False
        self.current_heading: str | None = None
        self.current_heading_parts: list[str] = []
        self.headings: dict[str, list[str]] = {f"h{level}": [] for level in range(1, 7)}
        self.meta_descriptions: list[str] = []
        self.robots_tags: list[str] = []
        self.googlebot_tags: list[str] = []
        self.canonicals: list[str] = []
        self.hreflang_entries: list[dict[str, str]] = []
        self.images: list[dict[str, bool]] = []
        self.links: list[dict[str, str]] = []
        self.text_parts: list[str] = []
        self.script_count = 0
        self.ignored_depth = 0
        self.in_json_ld = False
        self.current_json_ld: list[str] = []
        self.json_ld_blocks: list[str] = []
        self.current_anchor_href: str | None = None
        self.current_anchor_rel = ""
        self.current_anchor_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "script":
            self.script_count += 1
            if attributes.get("type", "").split(";", 1)[0].strip().lower() == "application/ld+json":
                self.in_json_ld = True
                self.current_json_ld = []
            else:
                self.ignored_depth += 1
            return
        if tag in {"style", "noscript", "template"}:
            self.ignored_depth += 1
            return
        if self.ignored_depth:
            return
        if tag == "html":
            self.html_lang = attributes.get("lang") or None
        elif tag == "title":
            self.in_title = True
        elif tag in self.headings:
            self.current_heading = tag
            self.current_heading_parts = []
        elif tag == "meta":
            name = attributes.get("name", "").lower()
            content = attributes.get("content", "")
            if name == "description":
                self.meta_descriptions.append(content)
            elif name == "robots":
                self.robots_tags.append(content)
            elif name == "googlebot":
                self.googlebot_tags.append(content)
        elif tag == "link":
            rel_tokens = attributes.get("rel", "").lower().split()
            href = attributes.get("href")
            if "canonical" in rel_tokens and href:
                self.canonicals.append(urljoin(self.final_url, href))
            if "alternate" in rel_tokens and attributes.get("hreflang") and href:
                self.hreflang_entries.append({"hreflang": attributes["hreflang"], "href": urljoin(self.final_url, href)})
        elif tag == "img":
            self.images.append({"has_alt": "alt" in attributes, "empty_alt": attributes.get("alt", "") == ""})
        elif tag == "a" and attributes.get("href"):
            self.current_anchor_href = urljoin(self.final_url, attributes["href"])
            self.current_anchor_rel = attributes.get("rel", "")
            self.current_anchor_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "script":
            if self.in_json_ld:
                self.json_ld_blocks.append("".join(self.current_json_ld).strip())
                self.in_json_ld = False
                self.current_json_ld = []
            else:
                self.ignored_depth = max(0, self.ignored_depth - 1)
            return
        if tag in {"style", "noscript", "template"}:
            self.ignored_depth = max(0, self.ignored_depth - 1)
            return
        if self.ignored_depth:
            return
        if tag == "title":
            self.in_title = False
        if tag == self.current_heading:
            value = _clean(" ".join(self.current_heading_parts))
            if value:
                self.headings[tag].append(value)
            self.current_heading = None
            self.current_heading_parts = []
        if tag == "a" and self.current_anchor_href:
            parsed = urlsplit(self.current_anchor_href)
            if parsed.scheme in {"http", "https"}:
                self.links.append({
                    "href": _without_fragment(self.current_anchor_href),
                    "anchor": _clean(" ".join(self.current_anchor_parts)),
                    "rel": self.current_anchor_rel,
                })
            self.current_anchor_href = None
            self.current_anchor_rel = ""
            self.current_anchor_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_json_ld:
            self.current_json_ld.append(data)
            return
        if self.ignored_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        if self.current_heading:
            self.current_heading_parts.append(data)
        if self.current_anchor_href:
            self.current_anchor_parts.append(data)
        self.text_parts.append(data)


def analyze_delivery(http_status: int | None, headers: dict[str, str], expected_indexable: bool | None) -> dict[str, object]:
    content_type = next((value for key, value in headers.items() if key.lower() == "content-type"), "")
    if http_status == 200:
        status, detail = "pass", "Final response returned HTTP 200."
    elif http_status in {404, 410}:
        status = "fail" if expected_indexable is True else "review"
        detail = f"Final response returned HTTP {http_status}; confirm whether this route should exist and be indexable."
    elif http_status in {401, 403}:
        status, detail = "unassessed", f"Final response returned HTTP {http_status}; page signals cannot be fully assessed."
    elif http_status is not None and http_status >= 500:
        status, detail = "fail", f"Final response returned server error HTTP {http_status}."
    elif http_status is None:
        status, detail = "unassessed", "No final HTTP response was available."
    else:
        status, detail = "review", f"Final response returned HTTP {http_status}; review delivery behavior."
    if content_type and "html" not in content_type.lower() and "xhtml" not in content_type.lower():
        status = "review" if status == "pass" else status
        detail += f" Content-Type is {content_type!r}, not HTML."
    return {"status": status, "http_status": http_status, "content_type": content_type or None, "detail": detail}


def _json_ld_check(blocks: list[str]) -> dict[str, object]:
    errors: list[dict[str, object]] = []
    top_level_types: set[str] = set()
    all_nested_types: set[str] = set()
    contexts: set[str] = set()
    parsed_blocks = 0
    def add_types(value: Any, destination: set[str]) -> None:
        if isinstance(value, str): destination.add(value)
        elif isinstance(value, list): destination.update(str(item) for item in value)
    def visit_declared(value: Any) -> None:
        if isinstance(value, list):
            for item in value: visit_declared(item)
        elif isinstance(value, dict):
            if isinstance(value.get("@context"), str): contexts.add(value["@context"])
            add_types(value.get("@type"), top_level_types)
            if "@graph" in value: visit_declared(value["@graph"])
    def visit_all(value: Any) -> None:
        if isinstance(value, list):
            for item in value: visit_all(item)
        elif isinstance(value, dict):
            add_types(value.get("@type"), all_nested_types)
            for child in value.values(): visit_all(child)
    for index, raw in enumerate(blocks):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append({"block": index + 1, "line": exc.lineno, "column": exc.colno, "message": exc.msg})
            continue
        parsed_blocks += 1
        visit_declared(value)
        visit_all(value)
    return {
        "status": "warn" if errors else "info", "blocks_found": len(blocks), "parseable_blocks": parsed_blocks,
        "parse_errors": errors, "types": sorted(top_level_types), "top_level_types": sorted(top_level_types),
        "all_nested_types": sorted(all_nested_types), "contexts": sorted(contexts),
        "semantic_review_required": bool(all_nested_types),
        "detail": "JSON-LD syntax errors observed." if errors else "JSON-LD parsed; verify claims against visible content." if blocks else "No JSON-LD block observed; absence is not automatically a defect.",
    }


def _canonical_check(parser: PageParser, final_url: str, expected_indexable: bool | None) -> dict[str, object]:
    normalized = [_normalize_for_compare(url) for url in parser.canonicals]
    unique = sorted(set(normalized))
    if not parser.canonicals:
        return {"status": "review", "values": [], "value": None, "conflicting": False, "detail": "No canonical declared; review whether the route has duplicate URL variants."}
    if len(unique) > 1:
        return {"status": "fail" if expected_indexable is True else "warn", "values": parser.canonicals, "value": None, "conflicting": True, "detail": "Conflicting canonical targets observed in static HTML."}
    target = parser.canonicals[0]
    duplicate_tags = len(parser.canonicals) > 1
    self_canonical = _normalize_for_compare(target) == _normalize_for_compare(final_url)
    status = "review" if duplicate_tags or not self_canonical else "info"
    return {
        "status": status, "values": parser.canonicals, "value": target, "conflicting": False,
        "duplicate_identical_tags": duplicate_tags, "self_canonical": self_canonical,
        "detail": "Duplicate identical canonical tags observed; consolidate to one declaration." if duplicate_tags else "Canonical matches fetched final URL." if self_canonical else "Canonical differs from fetched final URL; confirm consolidation intent and validate the target.",
    }


def _hreflang_check(parser: PageParser, self_reference_url: str, expected_multilingual: bool) -> dict[str, object]:
    entries = parser.hreflang_entries
    codes = [entry["hreflang"] for entry in entries]
    comparable = [code.lower() for code in codes]
    invalid = sorted({code for code in codes if not hreflang_code_supported_format(code)})
    duplicates = sorted({code for code in comparable if comparable.count(code) > 1})
    self_entries = [entry for entry in entries if _normalize_for_compare(entry["href"]) == _normalize_for_compare(self_reference_url)]
    self_codes = sorted({entry["hreflang"] for entry in self_entries if entry["hreflang"].lower() != "x-default"})
    lang_matches_self = None
    if parser.html_lang and self_codes:
        html_primary = parser.html_lang.lower().split("-", 1)[0]
        lang_matches_self = any(code.lower().split("-", 1)[0] == html_primary for code in self_codes)
    issues, reviews = [], []
    if expected_multilingual and not parser.html_lang: issues.append("Missing html lang on a page expected to be multilingual.")
    if expected_multilingual and not entries: issues.append("No hreflang alternates on a page expected to be multilingual.")
    if entries and not self_entries: issues.append("Hreflang set has no self-reference for the canonical/final URL.")
    if invalid: issues.append("Unsupported hreflang format observed; use a two-letter language with optional script/region.")
    if duplicates: issues.append("Duplicate hreflang codes observed.")
    if lang_matches_self is False: reviews.append("html lang and self hreflang use different primary languages.")
    detail = " ".join([*issues, *reviews]) or ("Language declarations observed; x-default is optional." if parser.html_lang or entries else "No language declarations observed; multilingual delivery was not expected for this run.")
    return {
        "status": "warn" if issues else "review" if reviews else "info", "html_lang": parser.html_lang,
        "entries": entries, "self_reference_target": self_reference_url, "has_self_reference": bool(self_entries),
        "self_reference_codes": self_codes, "html_lang_matches_self_reference": lang_matches_self,
        "has_x_default": "x-default" in comparable, "invalid_codes": invalid, "duplicate_codes": duplicates,
        "validation": None, "detail": detail,
    }


def analyze_html(html: str, final_url: str, keyword: str | None, expected_indexable: bool | None,
                 response_headers: dict[str, str] | None = None, http_status: int | None = 200,
                 expected_multilingual: bool = False) -> dict[str, object]:
    parser = PageParser(final_url)
    parser.feed(html)
    parser.close()
    headers = response_headers or {}
    title = _clean(" ".join(parser.title_parts)) or None
    text = _clean(" ".join(parser.text_parts))
    word_count = len(re.findall(r"\b\w+[\w'-]*\b", text))
    canonical_check = _canonical_check(parser, final_url, expected_indexable)
    canonical_target = canonical_check.get("value") if isinstance(canonical_check.get("value"), str) else None
    x_robots = next((value for key, value in headers.items() if key.lower() == "x-robots-tag"), None)
    parsed_directives = parse_directives(parser.robots_tags, parser.googlebot_tags, x_robots, "googlebot")
    directives = parsed_directives["directives"]
    noindex = "noindex" in directives or "none" in directives
    internal_links = [link for link in parser.links if urlsplit(link["href"]).netloc == urlsplit(final_url).netloc]
    external_links = [link for link in parser.links if urlsplit(link["href"]).netloc != urlsplit(final_url).netloc]
    missing_alt = sum(1 for image in parser.images if not image["has_alt"])
    checks: dict[str, object] = {
        "delivery": analyze_delivery(http_status, headers, expected_indexable),
        "title": {"status": "warn" if not title else "pass", "value": title, "length": len(title) if title else 0, "detail": "No title element in static HTML." if not title else "Title found; assess clarity and intent, not a fixed character threshold."},
        "meta_description": {"status": "review" if len(parser.meta_descriptions) != 1 else "info", "values": parser.meta_descriptions, "value": parser.meta_descriptions[-1] if parser.meta_descriptions else None, "detail": "One meta description found." if len(parser.meta_descriptions) == 1 else "No meta description observed; review snippet control." if not parser.meta_descriptions else "Multiple meta descriptions observed; consolidate to one."},
        "headings": {"status": "warn" if not parser.headings["h1"] else "info", "h1": parser.headings["h1"], "counts": {tag: len(values) for tag, values in parser.headings.items()}, "detail": "No H1 found in static HTML." if not parser.headings["h1"] else "Heading structure observed; assess hierarchy against the page task rather than a fixed count."},
        "canonical": canonical_check,
        "indexability_directives": {"status": "fail" if noindex and expected_indexable is True else "warn" if (not noindex and expected_indexable is False) else "review" if noindex else "info", "target_agent": parsed_directives["target_agent"], "meta_robots": parser.robots_tags, "meta_googlebot": parser.googlebot_tags, "x_robots_tag": x_robots, "directives": directives, "ignored_scoped_directives": parsed_directives["ignored_scoped_directives"], "noindex": noindex, "detail": "noindex observed on a route expected to be indexable." if noindex and expected_indexable is True else "Route is expected excluded but no noindex was observed; confirm access/indexation strategy." if not noindex and expected_indexable is False else "noindex observed; confirm route intent." if noindex else "No noindex directive observed for Googlebot."},
        "images": {"status": "review" if missing_alt else "info", "count": len(parser.images), "missing_alt_attribute": missing_alt, "empty_alt": sum(1 for image in parser.images if image["empty_alt"]), "detail": "Some images lack alt; inspect only content-bearing images." if missing_alt else "No missing alt attributes observed; empty alt can be correct for decoration."},
        "static_links": {"status": "info", "internal": len(internal_links), "external": len(external_links), "links": parser.links, "internal_links": internal_links, "detail": "Static crawlable links inventoried. Site mode validates status, redirects, canonical targets, depth, and orphaning."},
        "content": {"status": "info", "word_count": word_count, "detail": "Word count is an observation, not a content-quality or ranking score."},
        "rendering": {"status": "unassessed" if parser.script_count else "info", "script_count": parser.script_count, "static_core_signals": {"title": bool(title), "h1": bool(parser.headings["h1"]), "internal_links": bool(internal_links), "visible_text": bool(text)}, "detail": "Scripts are present; rendered DOM remains unassessed. Do not infer parity from static word count." if parser.script_count else "No script tags observed; browser-rendered state was not required for this static evidence pass."},
        "json_ld": _json_ld_check(parser.json_ld_blocks),
        "hreflang": _hreflang_check(parser, canonical_target or final_url, expected_multilingual),
    }
    if keyword:
        haystack = " ".join([title or "", *parser.headings["h1"]]).lower()
        checks["target_query"] = {"status": "info" if keyword.lower() in haystack else "review", "value": keyword, "detail": "Query phrase appears in title/H1; still review search intent." if keyword.lower() in haystack else "Exact query phrase is absent from title/H1; review natural semantic alignment rather than treating this as an automatic defect."}
    else:
        checks["target_query"] = {"status": "unassessed", "value": None, "detail": "No user-supplied query; search-intent alignment is unassessed."}
    return checks


def validate_canonical_target(check: dict[str, object], expected_indexable: bool | None, timeout: int) -> dict[str, object] | None:
    target = check.get("value")
    if not isinstance(target, str) or check.get("conflicting"):
        return None
    try:
        result = safe_fetch(target, timeout=timeout)
    except UnsafeUrlError as exc:
        return {"status": "warn", "url": target, "error": str(exc), "detail": "Canonical target could not be safely validated."}
    if result.error:
        return {"status": "warn", "url": target, "error": result.error, "detail": "Canonical target fetch failed."}
    target_checks = analyze_html(result.body or "", result.url, None, None, result.headers, result.status_code, False)
    noindex = bool(target_checks["indexability_directives"].get("noindex"))
    broken = result.status_code != 200 or noindex
    redirected = bool(result.redirect_chain)
    status = "fail" if broken and expected_indexable is True else "warn" if broken or redirected else "info"
    return {
        "status": status, "url": target, "final_url": result.url, "http_status": result.status_code,
        "redirected": redirected, "noindex": noindex,
        "self_canonical": target_checks["canonical"].get("self_canonical"),
        "detail": "Canonical target is not a clean indexable HTTP 200 target." if broken else "Canonical target redirects; point directly at the final canonical URL where practical." if redirected else "Canonical target returned HTTP 200 without noindex.",
    }


def validate_hreflang_targets(entries: list[dict[str, str]], source_url: str, source_codes: set[str], timeout: int, max_entries: int) -> dict[str, object]:
    results = []
    unique_entries = list({(entry["hreflang"].lower(), entry["href"]): entry for entry in entries}.values())
    for entry in unique_entries[:max_entries]:
        try:
            result = safe_fetch(entry["href"], timeout=timeout)
        except UnsafeUrlError as exc:
            results.append({"hreflang": entry["hreflang"], "url": entry["href"], "final_url": None, "http_status": None, "error": str(exc), "reciprocal": None, "cluster_complete": None})
            continue
        reciprocal = cluster_complete = None
        target_noindex = None
        if not result.error and result.status_code == 200 and result.body is not None:
            target_parser = PageParser(result.url)
            target_parser.feed(result.body)
            target_parser.close()
            reciprocal = any(_normalize_for_compare(item["href"]) == _normalize_for_compare(source_url) for item in target_parser.hreflang_entries)
            target_codes = {item["hreflang"].lower() for item in target_parser.hreflang_entries}
            cluster_complete = source_codes.issubset(target_codes)
            target_directives = parse_directives(target_parser.robots_tags, target_parser.googlebot_tags, next((v for k, v in result.headers.items() if k.lower() == "x-robots-tag"), None))
            target_noindex = "noindex" in target_directives["directives"] or "none" in target_directives["directives"]
        results.append({"hreflang": entry["hreflang"], "url": entry["href"], "final_url": result.url, "http_status": result.status_code, "error": result.error, "reciprocal": reciprocal, "cluster_complete": cluster_complete, "noindex": target_noindex})
    failed = [item for item in results if item["error"] or item["http_status"] != 200 or item["reciprocal"] is False or item["cluster_complete"] is False or item.get("noindex") is True]
    return {"checked": len(results), "not_checked": max(0, len(unique_entries) - len(results)), "results": results, "status": "warn" if failed else "info", "detail": "Some hreflang targets were unreachable, noindex, non-reciprocal, or exposed an incomplete alternate cluster." if failed else "Checked hreflang targets were reachable, reciprocal, and cluster-complete within the configured bound."}


def audit_page(url: str, keyword: str | None = None, expected_indexable: bool | None = None,
               expected_multilingual: bool = False, validate_hreflang: bool = False,
               max_hreflang: int = 12, timeout: int = 15, validate_canonical: bool = True,
               profile: str = "generic", route_class: str | None = None) -> dict[str, object]:
    decision = decide_route(url, profile, route_class)
    if expected_indexable is None:
        expected_indexable = decision.expected_indexable
    try:
        result = safe_fetch(url, timeout=timeout)
    except UnsafeUrlError as exc:
        return {"url": url, "status": "error", "error": str(exc)}
    if result.error:
        return {"url": result.url, "status": "error", "error": result.error, "redirect_chain": result.redirect_chain}
    checks = analyze_html(result.body or "", result.url, keyword, expected_indexable, result.headers, result.status_code, expected_multilingual)
    if validate_canonical and isinstance(checks.get("canonical"), dict):
        checks["canonical"]["target_validation"] = validate_canonical_target(checks["canonical"], expected_indexable, timeout)
    hreflang = checks["hreflang"]
    if validate_hreflang and isinstance(hreflang, dict) and hreflang["entries"]:
        source_codes = {entry["hreflang"].lower() for entry in hreflang["entries"]}
        hreflang["validation"] = validate_hreflang_targets(hreflang["entries"], hreflang.get("self_reference_target") or result.url, source_codes, timeout, max_hreflang)
        if hreflang["validation"]["status"] == "warn":
            hreflang["status"] = "warn"
            hreflang["detail"] = f"{hreflang['detail']} {hreflang['validation']['detail']}"
    return {
        "url": url, "final_url": result.url, "http_status": result.status_code, "response_bytes": result.byte_length,
        "redirect_chain": result.redirect_chain, "profile": profile, "route_class": decision.route_class,
        "expected_indexable": expected_indexable, "expectation_reason": decision.reason, "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run bounded static-HTML technical SEO checks.")
    parser.add_argument("url")
    parser.add_argument("--keyword")
    parser.add_argument("--profile", choices=["generic", "toolsite", "saas", "hybrid"], default="generic")
    parser.add_argument("--route-class", choices=sorted(ROUTE_CLASSES))
    parser.add_argument("--indexability", choices=["auto", "expected", "excluded"], default="auto")
    parser.add_argument("--expected-multilingual", action="store_true")
    parser.add_argument("--validate-hreflang", action="store_true")
    parser.add_argument("--skip-canonical-validation", action="store_true")
    parser.add_argument("--max-hreflang", type=int, default=12)
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args()
    expected = None if args.indexability == "auto" else args.indexability == "expected"
    output = audit_page(args.url, args.keyword, expected, args.expected_multilingual, args.validate_hreflang, args.max_hreflang, args.timeout, not args.skip_canonical_validation, args.profile, args.route_class)
    print(json.dumps(output, indent=2, ensure_ascii=False))
    if output.get("status") == "error": return 1
    checks = output.get("checks", {})
    return 1 if any(isinstance(value, dict) and value.get("status") == "fail" for value in checks.values()) else 0

if __name__ == "__main__":
    sys.exit(main())
