#!/usr/bin/env python3
"""Bounded static crawl and SEO-first site architecture analysis."""
from __future__ import annotations

from collections import defaultdict, deque
from urllib.parse import urlsplit

from check_page import analyze_html, _normalize_for_compare
from profiles import classify_route, detect_profile, expectation_for
from url_safety import UnsafeUrlError, safe_fetch


def _same_origin(a: str, b: str) -> bool:
    pa, pb = urlsplit(a), urlsplit(b)
    return (pa.scheme.lower(), pa.netloc.lower()) == (pb.scheme.lower(), pb.netloc.lower())


def _norm(url: str) -> str:
    parsed = urlsplit(url)
    return parsed._replace(fragment="").geturl()


def _query_variant_of_canonical(url: str, canonical: str) -> bool:
    parsed = urlsplit(url)
    if not parsed.query:
        return False
    without_query = parsed._replace(query="", fragment="").geturl()
    return _normalize_for_compare(without_query) == _normalize_for_compare(canonical)


def _extract_page_record(requested_url: str, result, depth: int | None, source: str, profile: str) -> dict[str, object]:
    route_class = classify_route(result.url, profile)
    expected = expectation_for(route_class, profile)
    checks = analyze_html(result.body or "", result.url, None, expected, result.headers, result.status_code, False, route_class)
    return {
        "requested_url": requested_url, "final_url": result.url, "http_status": result.status_code,
        "redirected": bool(result.redirect_chain), "redirect_chain": result.redirect_chain, "depth": depth, "source": source,
        "route_class": route_class, "expected_indexable": expected,
        "title": checks["title"].get("value"), "h1": checks["headings"].get("h1", []),
        "meta_description": checks["meta_description"].get("value"), "canonical": checks["canonical"].get("value"),
        "canonical_conflicting": checks["canonical"].get("conflicting", False),
        "noindex": checks["indexability_directives"].get("noindex", False),
        "internal_links": [item["href"] for item in checks["static_links"].get("internal_links", [])],
        "script_count": checks["rendering"].get("script_count", 0),
        "static_core_signals": checks["rendering"].get("static_core_signals", {}),
        "release_residue": checks.get("release_residue", {}),
    }


def crawl_site(root_url: str, sitemap_urls: list[str], profile: str, max_pages: int = 200, timeout: int = 15) -> dict[str, object]:
    # Prioritize the static internal-link graph over sitemap-only fetches. On large
    # sitemaps, a single mixed queue can consume max_pages before category/listing
    # pages are fetched and manufacture false orphan findings.
    crawl_queue: deque[tuple[str, int | None, str]] = deque([(root_url, 0, "crawl")])
    sitemap_queue: deque[tuple[str, int | None, str]] = deque()
    for url in sitemap_urls:
        if _same_origin(root_url, url): sitemap_queue.append((url, None, "sitemap"))
    seen_requested: set[str] = set()
    pages: dict[str, dict[str, object]] = {}
    errors: list[dict[str, object]] = []
    indegree: defaultdict[str, int] = defaultdict(int)
    discovered_depth: dict[str, int] = {_norm(root_url): 0}
    while (crawl_queue or sitemap_queue) and len(seen_requested) < max_pages:
        requested, depth, source = crawl_queue.popleft() if crawl_queue else sitemap_queue.popleft()
        requested = _norm(requested)
        if requested in seen_requested or not _same_origin(root_url, requested): continue
        seen_requested.add(requested)
        try:
            result = safe_fetch(requested, timeout=timeout)
        except UnsafeUrlError as exc:
            errors.append({"url": requested, "error": str(exc)})
            continue
        if result.error:
            errors.append({"url": requested, "error": result.error})
            continue
        record = _extract_page_record(requested, result, depth, source, profile)
        pages[requested] = record
        if result.status_code != 200: continue
        canonical = record.get("canonical")
        if isinstance(canonical, str) and _same_origin(root_url, canonical) and _norm(canonical) not in seen_requested:
            crawl_queue.append((_norm(canonical), None, "canonical"))
        for link in record["internal_links"]:
            target = _norm(link)
            indegree[target] += 1
            if not _same_origin(root_url, target): continue
            base_depth = depth if isinstance(depth, int) else discovered_depth.get(requested)
            next_depth = base_depth + 1 if isinstance(base_depth, int) else None
            if isinstance(next_depth, int):
                prior = discovered_depth.get(target)
                if prior is None or next_depth < prior: discovered_depth[target] = next_depth
            if target not in seen_requested:
                crawl_queue.append((target, discovered_depth.get(target), "crawl"))
    for requested, record in pages.items():
        if record.get("depth") is None and requested in discovered_depth: record["depth"] = discovered_depth[requested]
        record["indegree"] = indegree.get(requested, 0)
    return {
        "pages": list(pages.values()), "errors": errors, "max_pages": max_pages,
        "requested_checked": len(seen_requested), "queue_remaining": len(crawl_queue) + len(sitemap_queue),
    }


def _group_duplicates(pages: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    for page in pages:
        if page.get("expected_indexable") is not True: continue
        value = page.get(field)
        if field == "h1": value = " | ".join(value or [])
        if isinstance(value, str) and value.strip(): groups[value.strip()].append(str(page["requested_url"]))
    return [{"value": value, "urls": urls} for value, urls in groups.items() if len(urls) > 1]


def analyze_site(crawl: dict[str, object], sitemap_urls: list[str], profile: str, root_url: str) -> dict[str, object]:
    pages = crawl.get("pages", [])
    page_by_requested = {str(page["requested_url"]): page for page in pages}
    sitemap_set = {_norm(url) for url in sitemap_urls}
    findings: list[dict[str, object]] = []
    def add(priority: str, code: str, url: str, detail: str, evidence: dict[str, object] | None = None, evidence_label: str = "OBSERVED") -> None:
        findings.append({"priority": priority, "evidence_label": evidence_label, "code": code, "url": url, "detail": detail, "evidence": evidence or {}})

    for page in pages:
        url = str(page["requested_url"])
        expected = page.get("expected_indexable")
        release_residue = page.get("release_residue")
        if isinstance(release_residue, dict):
            for item in release_residue.get("findings", []):
                if not isinstance(item, dict):
                    continue
                severity = str(item.get("severity") or "P2")
                if severity not in {"P0", "P1", "P2", "P3"}:
                    severity = "P2"
                code = str(item.get("code") or "RELEASE_RESIDUE")
                add(
                    severity,
                    f"PUBLIC_COPY_{code}",
                    url,
                    str(item.get("detail") or "Potential development-stage wording is visible in public-facing copy."),
                    {
                        "element": item.get("element"),
                        "text": item.get("text"),
                        "match": item.get("match"),
                        "suggestion": item.get("suggestion"),
                        "confidence": item.get("confidence"),
                    },
                    "OBSERVED" if severity == "P0" else "REVIEW",
                )
        if expected is True and page.get("noindex"):
            add("P0", "EXPECTED_INDEXABLE_NOINDEX", url, "Public search landing route is noindex.", evidence_label="REVIEW")
        if expected is False and not page.get("noindex") and page.get("http_status") == 200:
            add("P1", "PRIVATE_ROUTE_INDEXABLE", url, "Private/app/transactional route returned 200 without noindex.", evidence_label="REVIEW")
        if page.get("canonical_conflicting"):
            add("P1", "CONFLICTING_CANONICAL", url, "Multiple conflicting canonical targets were observed.")
        canonical = page.get("canonical")
        if expected is True and isinstance(canonical, str) and _normalize_for_compare(canonical) != _normalize_for_compare(str(page.get("final_url") or url)) and not _query_variant_of_canonical(str(page.get("final_url") or url), canonical):
            add("P1", "NON_SELF_CANONICAL_PUBLIC", url, "Expected-indexable page canonicalizes elsewhere; confirm intentional consolidation.", {"canonical": canonical}, "REVIEW")
            canonical_page = page_by_requested.get(_norm(canonical))
            if canonical_page:
                if canonical_page.get("http_status") != 200:
                    add("P1", "CANONICAL_TARGET_NON_200", url, "Canonical target does not return HTTP 200.", {"canonical": canonical, "status": canonical_page.get("http_status")})
                if canonical_page.get("noindex"):
                    add("P1", "CANONICAL_TARGET_NOINDEX", url, "Canonical target is noindex.", {"canonical": canonical})
        if page.get("script_count") and expected is True:
            core = page.get("static_core_signals") or {}
            if not core.get("title") or not core.get("h1"):
                add("P1", "STATIC_CORE_SIGNAL_MISSING", url, "Expected-indexable scripted page lacks static title or H1; rendered parity must be verified.", core)
        if url in sitemap_set:
            if page.get("http_status") != 200:
                add("P1", "SITEMAP_NON_200", url, "Sitemap URL does not resolve to HTTP 200.", {"status": page.get("http_status")})
            if page.get("redirected"):
                add("P1", "SITEMAP_REDIRECT", url, "Sitemap contains a redirecting URL; list the final canonical URL instead.")
            if page.get("noindex"):
                add("P1", "SITEMAP_NOINDEX", url, "Sitemap contains a noindex URL.")
            if isinstance(canonical, str) and _normalize_for_compare(canonical) != _normalize_for_compare(str(page.get("final_url") or url)):
                add("P1", "SITEMAP_NONCANONICAL", url, "Sitemap URL canonicalizes to another URL.", {"canonical": canonical})
            if url != _norm(root_url) and int(page.get("indegree") or 0) == 0:
                if int(crawl.get("queue_remaining") or 0) > 0:
                    add(
                        "P2",
                        "ORPHAN_SITEMAP_CANDIDATE",
                        url,
                        "Sitemap URL has zero observed static internal-link indegree, but the bounded crawl ended with unchecked URLs; orphan status is not proven.",
                        {"queue_remaining": crawl.get("queue_remaining"), "max_pages": crawl.get("max_pages")},
                        "REVIEW",
                    )
                else:
                    add("P1", "ORPHAN_SITEMAP_PAGE", url, "Sitemap URL has zero static internal-link indegree after the bounded crawl completed.")

    for source in pages:
        for target in source.get("internal_links", []):
            target = _norm(target)
            target_page = page_by_requested.get(target)
            if not target_page: continue
            if target_page.get("http_status") in {404, 410} or (isinstance(target_page.get("http_status"), int) and target_page["http_status"] >= 500):
                add("P1", "BROKEN_INTERNAL_LINK", str(source["requested_url"]), "Internal link points to a broken/server-error target.", {"target": target, "status": target_page.get("http_status")})
            elif target_page.get("redirected"):
                add("P2", "REDIRECTING_INTERNAL_LINK", str(source["requested_url"]), "Internal link points to a redirect instead of the final URL.", {"target": target, "final": target_page.get("final_url")})
            canonical = target_page.get("canonical")
            if isinstance(canonical, str) and _normalize_for_compare(canonical) != _normalize_for_compare(str(target_page.get("final_url") or target)):
                if _query_variant_of_canonical(str(target_page.get("final_url") or target), canonical):
                    add("P2", "INTERNAL_LINK_TO_CANONICALIZED_QUERY", str(source["requested_url"]), "Internal link points to a query-state URL that canonicals to the base page; review crawl-efficiency intent.", {"target": target, "canonical": canonical}, "REVIEW")
                else:
                    add("P1", "INTERNAL_LINK_TO_NONCANONICAL", str(source["requested_url"]), "Internal link points to a URL that canonicalizes elsewhere.", {"target": target, "canonical": canonical})

    duplicate_titles = _group_duplicates(pages, "title")
    duplicate_h1 = _group_duplicates(pages, "h1")
    duplicate_descriptions = _group_duplicates(pages, "meta_description")
    for group in duplicate_titles:
        add("P2", "DUPLICATE_TITLE", group["urls"][0], "Multiple expected-indexable pages share the same title.", group)
    for group in duplicate_h1:
        add("P2", "DUPLICATE_H1", group["urls"][0], "Multiple expected-indexable pages share the same H1 set.", group)
    for group in duplicate_descriptions:
        add(
            "P2",
            "DUPLICATE_META_DESCRIPTION",
            group["urls"][0],
            "Multiple expected-indexable pages share the same meta description.",
            group,
        )

    canonical_groups: defaultdict[str, list[str]] = defaultdict(list)
    for page in pages:
        if page.get("expected_indexable") is True and isinstance(page.get("canonical"), str):
            page_url = str(page.get("final_url") or page["requested_url"])
            canonical = str(page["canonical"])
            if _query_variant_of_canonical(page_url, canonical):
                continue
            key = _normalize_for_compare(canonical)
            requested_url = str(page["requested_url"])
            requested_normalized = _normalize_for_compare(requested_url)
            if any(_normalize_for_compare(existing) == requested_normalized for existing in canonical_groups[key]):
                continue
            canonical_groups[key].append(requested_url)
    collisions = [{"canonical": key, "urls": urls} for key, urls in canonical_groups.items() if len(urls) > 1]
    for group in collisions:
        add("P1", "CANONICAL_COLLISION", group["urls"][0], "Multiple expected-indexable URLs converge on one canonical target; verify intentional consolidation.", group)

    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    findings.sort(key=lambda item: (priority_order.get(str(item["priority"]), 9), str(item["url"]), str(item["code"])))
    return {
        "profile": profile, "pages_checked": len(pages), "findings": findings,
        "summary": {"P0": sum(f["priority"] == "P0" for f in findings), "P1": sum(f["priority"] == "P1" for f in findings), "P2": sum(f["priority"] == "P2" for f in findings), "P3": sum(f["priority"] == "P3" for f in findings)},
        "duplicate_titles": duplicate_titles, "duplicate_h1": duplicate_h1,
        "duplicate_descriptions": duplicate_descriptions, "canonical_collisions": collisions,
        "depth": sorted(({"url": page["requested_url"], "depth": page.get("depth"), "route_class": page.get("route_class")} for page in pages), key=lambda x: (9999 if x["depth"] is None else int(x["depth"]), str(x["url"]))),
    }


def run_site_audit(root_url: str, sitemap_urls: list[str], profile: str, max_pages: int = 200, timeout: int = 15) -> dict[str, object]:
    initial_urls = [root_url, *sitemap_urls]
    detected = detect_profile(initial_urls) if profile == "auto" else {"profile": profile, "confidence": "explicit", "signals": {}}
    effective_profile = str(detected["profile"])
    crawl = crawl_site(root_url, sitemap_urls, effective_profile, max_pages, timeout)
    if profile == "auto":
        detected = detect_profile([str(page["requested_url"]) for page in crawl["pages"]])
        effective_profile = str(detected["profile"])
        # Reclassify records with the stronger site-wide profile; no second fetch required.
        for page in crawl["pages"]:
            page["route_class"] = classify_route(str(page["final_url"]), effective_profile)
            page["expected_indexable"] = expectation_for(str(page["route_class"]), effective_profile)
    analysis = analyze_site(crawl, sitemap_urls, effective_profile, root_url)
    return {"profile_detection": detected, "effective_profile": effective_profile, "crawl": crawl, "analysis": analysis}
