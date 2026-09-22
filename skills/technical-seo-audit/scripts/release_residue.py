#!/usr/bin/env python3
"""Detect development-stage wording and internal terminology leaked into public-facing static copy."""
from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Rule:
    code: str
    severity: str
    pattern: re.Pattern[str]
    group: str
    detail: str
    suggestion: str
    confidence: str = "high"


def _rule(code: str, severity: str, pattern: str, group: str, detail: str, suggestion: str,
          confidence: str = "high", flags: int = re.IGNORECASE) -> Rule:
    return Rule(code, severity, re.compile(pattern, flags), group, detail, suggestion, confidence)


RULES = [
    _rule(
        "PLACEHOLDER_LOREM", "P0", r"\b(?:lorem ipsum|dolor sit amet)\b", "deterministic",
        "Placeholder copy is visible in production-facing text.",
        "Replace the placeholder with final user-facing copy.",
    ),
    _rule(
        "TODO_MARKER", "P0", r"\b(?:TODO|FIXME|TBD)\b", "deterministic",
        "An internal work marker is visible in production-facing text.",
        "Remove the work marker and ship final copy or intentionally hide the unfinished feature.",
        "high",
        0,
    ),
    _rule(
        "RAW_RUNTIME_ERROR", "P0",
        r"(?:\[object Object\]|\bUnhandled(?: Promise)? Rejection\b|\b(?:TypeError|ReferenceError|SyntaxError):|\bECONNREFUSED\b|\bstack trace\b)",
        "deterministic",
        "Raw runtime/debug output appears visible to users.",
        "Replace raw implementation errors with a concise user-facing error and keep diagnostics in logs.",
    ),
    _rule(
        "MISSING_RUNTIME_CONFIG", "P0",
        r"(?:(?:API key|environment variable|env var|configuration)\b.{0,40}\b(?:missing|not set|not configured|required)\b|\b(?:missing|unset)\b.{0,30}\b(?:API key|environment variable|env var)\b)",
        "deterministic",
        "Deployment/configuration language is visible to end users.",
        "Fix the deployment configuration and expose only a user-facing availability/error message.",
    ),
    _rule(
        "LOCAL_DEVELOPMENT_ENDPOINT", "P0",
        r"(?<![A-Za-z0-9.-])(?:https?://)?(?:localhost|127\.0\.0\.1|0\.0\.0\.0)(?::\d{2,5})?(?![A-Za-z0-9.-])",
        "environment",
        "A local-development endpoint is visible in production-facing copy.",
        "Replace the local endpoint with the production URL or remove the implementation detail.",
    ),
    _rule(
        "MVP_LANGUAGE", "P1", r"\b(?:MVP|minimum viable product)\b", "dev_process",
        "Development-stage product language may have leaked into copy intended for end users.",
        "Describe the user capability or limitation directly instead of the internal delivery stage.",
    ),
    _rule(
        "PHASE_LANGUAGE", "P1", r"\bphase\s+(?:[0-9]+|[ivx]+)\b", "dev_process",
        "Implementation-phase wording is visible in public-facing copy.",
        "Replace internal phase terminology with the current user-facing capability, status, or roadmap wording if intentionally public.",
    ),
    _rule(
        "DEV_PRIORITY_LANGUAGE", "P1",
        r"(?:\b(?:priority|issue|fix|task|release|launch|blocker)\s*[:=-]?\s*P[0-3]\b|\bP[0-3]\s+(?:priority|issue|fix|task|release|blocker)\b)",
        "dev_process",
        "Internal priority/severity notation appears in user-facing copy.",
        "Remove internal prioritization tokens from the public message.",
    ),
    _rule(
        "INTERNAL_NOTE", "P1",
        r"\b(?:internal use only|developer note|dev note|implementation note|temporary copy|temporary ui|placeholder copy)\b",
        "dev_process",
        "An internal implementation/editorial note appears visible to users.",
        "Remove the internal note and keep only final user-facing copy.",
    ),
    _rule(
        "MOCK_COPY", "P1", r"\b(?:mock|dummy)\s+(?:data|result|response|content|output)\b", "dev_process",
        "Mock/test language may indicate unfinished production behavior.",
        "Use real production behavior or clearly label an intentional demo/sample in user language.",
        "medium",
    ),
    _rule(
        "STAGING_LANGUAGE", "P1",
        r"\b(?:staging|development|dev)\s+(?:environment|build|server|mode|deployment)\b",
        "environment",
        "A non-production environment label is visible in public-facing copy.",
        "Remove the environment label or replace it with an intentional public beta/demo label.",
    ),
    _rule(
        "NOT_IMPLEMENTED_LANGUAGE", "P1",
        r"\b(?:not yet implemented|implementation pending|will be implemented|coming in phase|feature not implemented)\b",
        "dev_process",
        "Implementation-status language exposes unfinished internal state.",
        "State the current user-visible limitation and available alternative without implementation-plan wording.",
    ),
    _rule(
        "DEBUG_LANGUAGE", "P1", r"\b(?:debug mode|debug only|enable debug|debug build)\b", "environment",
        "Debug terminology is visible in production-facing copy.",
        "Remove debug controls/messages from ordinary public UI or restrict them to an authenticated developer context.",
    ),
    _rule(
        "INFRASTRUCTURE_JARGON", "P2",
        r"\b(?:Cloudflare\s+R2|R2\s+bucket|object storage|storage bucket)\b", "jargon",
        "Infrastructure terminology may be unnecessary for the target audience.",
        "Prefer the user outcome (for example, secure download or file storage) unless the infrastructure detail is intentionally relevant.",
        "medium",
    ),
    _rule(
        "PRESIGNED_URL_JARGON", "P2", r"\bpre[- ]?signed\s+URL\b", "jargon",
        "Backend delivery terminology may be exposed to non-technical users.",
        "Use user language such as download link or secure link unless this is developer documentation.",
        "medium",
    ),
    _rule(
        "QUEUE_JARGON", "P2", r"\b(?:worker queue|job queue|queue worker)\b", "jargon",
        "Backend queue terminology may not match the page audience.",
        "Describe the user-visible processing state rather than the queue implementation.",
        "medium",
    ),
    _rule(
        "JOB_ID_JARGON", "P2", r"\bjob\s+id\b", "jargon",
        "An internal processing identifier may be exposed without user need.",
        "Use a user-facing reference number only when users need it for support or tracking.",
        "medium",
    ),
    _rule(
        "PROCESS_PAYLOAD_JARGON", "P2",
        r"\b(?:trigger conversion|execute task|process payload|invoke endpoint)\b", "jargon",
        "Action wording reads like an internal API/process instruction rather than end-user UI.",
        "Use a direct task verb such as Convert, Generate, Download, Retry, or Start.",
        "medium",
    ),
]

CAPTURE_TAGS = {
    "title", "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "li", "button", "label", "a", "legend", "summary", "option", "td", "th", "caption",
}
IGNORED_TAGS = {"script", "style", "template", "noscript", "svg", "code", "pre"}
TECHNICAL_ROUTE_CLASSES = {"DOCS", "INTEGRATION", "SYSTEM"}
PRIVATE_ROUTE_CLASSES = {"AUTH", "APP", "ACCOUNT", "TRANSACTIONAL", "SYSTEM"}


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _technical_path(url: str) -> bool:
    path = (urlsplit(url).path or "/").lower()
    return any(marker in path for marker in (
        "/docs", "/doc/", "/api", "/developers", "/developer/", "/reference", "/changelog",
    ))


class CopyParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignored_depth = 0
        self.active: list[dict[str, object]] = []
        self.segments: list[dict[str, str]] = []
        self.body_parts: list[str] = []

    def _add_attr(self, element: str, attribute: str, value: str) -> None:
        value = _clean(value)
        if value:
            self.segments.append({"element": f"{element}[{attribute}]", "text": value})

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag in IGNORED_TAGS:
            self.ignored_depth += 1
            return
        if self.ignored_depth:
            return

        if tag == "meta" and attributes.get("name", "").lower() == "description":
            self._add_attr("meta", "description", attributes.get("content", ""))

        if tag in {"input", "textarea", "button", "select"}:
            for attribute in ("placeholder", "aria-label", "title"):
                self._add_attr(tag, attribute, attributes.get(attribute, ""))
        if tag == "input" and attributes.get("type", "").lower() in {"button", "submit", "reset"}:
            self._add_attr("input", "value", attributes.get("value", ""))

        should_capture = tag in CAPTURE_TAGS or attributes.get("role", "").lower() in {"alert", "status"}
        if should_capture:
            label = tag if tag in CAPTURE_TAGS else f'{tag}[role={attributes.get("role", "").lower()}]'
            self.active.append({"tag": tag, "element": label, "parts": []})

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in IGNORED_TAGS:
            self.ignored_depth = max(0, self.ignored_depth - 1)
            return
        if self.ignored_depth:
            return
        for index in range(len(self.active) - 1, -1, -1):
            item = self.active[index]
            if item["tag"] != tag:
                continue
            text = _clean(" ".join(str(part) for part in item["parts"]))
            if text:
                self.segments.append({"element": str(item["element"]), "text": text})
            del self.active[index]
            break

    def handle_data(self, data: str) -> None:
        if self.ignored_depth:
            return
        if not data.strip():
            return
        self.body_parts.append(data)
        for item in self.active:
            item["parts"].append(data)


def _snippet(text: str, match: re.Match[str], radius: int = 80) -> str:
    start = max(0, match.start() - radius)
    end = min(len(text), match.end() + radius)
    prefix = "..." if start else ""
    suffix = "..." if end < len(text) else ""
    return prefix + _clean(text[start:end]) + suffix


def _adjust_severity(rule: Rule, route_class: str | None, url: str) -> str | None:
    route = (route_class or "").upper()
    technical = route in TECHNICAL_ROUTE_CLASSES or _technical_path(url)
    private = route in PRIVATE_ROUTE_CLASSES

    if rule.group == "jargon":
        if technical or private:
            return None
        return "P2"

    if rule.group == "dev_process" and (technical or route == "CONTENT" or private):
        return "P2"

    if rule.group == "environment" and technical:
        return "P2" if rule.severity in {"P0", "P1"} else rule.severity

    if private and rule.severity == "P1":
        return "P2"

    return rule.severity


def analyze_release_residue(html: str, final_url: str, route_class: str | None = None,
                            max_findings: int = 25) -> dict[str, object]:
    parser = CopyParser()
    parser.feed(html)
    parser.close()

    body_text = _clean(" ".join(parser.body_parts))
    segments = [*parser.segments]
    if body_text:
        segments.append({"element": "visible_body", "text": body_text})

    findings: list[dict[str, object]] = []
    seen_rules_specific: set[str] = set()
    seen: set[tuple[str, str]] = set()
    truncated = False

    for segment in segments:
        text = segment["text"]
        element = segment["element"]
        for rule in RULES:
            if element == "visible_body" and rule.code in seen_rules_specific:
                continue
            match = rule.pattern.search(text)
            if not match:
                continue
            severity = _adjust_severity(rule, route_class, final_url)
            if severity is None:
                continue
            snippet = _snippet(text, match)
            key = (rule.code, snippet.lower())
            if key in seen:
                continue
            seen.add(key)
            if element != "visible_body":
                seen_rules_specific.add(rule.code)
            findings.append({
                "severity": severity,
                "base_severity": rule.severity,
                "code": rule.code,
                "element": element,
                "text": snippet,
                "match": match.group(0),
                "detail": rule.detail,
                "suggestion": rule.suggestion,
                "confidence": rule.confidence,
            })
            if len(findings) >= max_findings:
                truncated = True
                break
        if truncated:
            break

    priority = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    findings.sort(key=lambda item: (priority.get(str(item["severity"]), 9), str(item["code"]), str(item["element"])))
    summary = {
        level: sum(item["severity"] == level for item in findings)
        for level in ("P0", "P1", "P2", "P3")
    }
    status = "fail" if summary["P0"] else "review" if findings else "info"
    return {
        "status": status,
        "route_class": route_class,
        "technical_audience_hint": (route_class or "").upper() in TECHNICAL_ROUTE_CLASSES or _technical_path(final_url),
        "findings": findings,
        "summary": summary,
        "truncated": truncated,
        "detail": (
            "Deterministic production-copy residue found."
            if summary["P0"]
            else "Potential development-stage or audience-mismatched wording requires review."
            if findings
            else "No configured development-stage public-copy residue was observed in static HTML."
        ),
    }
