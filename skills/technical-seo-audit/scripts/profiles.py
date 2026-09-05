"""Site profiles and conservative route classification for SEO expectations."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

PROFILES = {"generic", "toolsite", "saas", "hybrid", "auto"}
ROUTE_CLASSES = {
    "PUBLIC_TOOL", "MARKETING", "SEO_LANDING", "CONTENT", "INTEGRATION", "DOCS",
    "AUTH", "APP", "ACCOUNT", "TRANSACTIONAL", "SYSTEM", "UNKNOWN",
}
PUBLIC_CLASSES = {"PUBLIC_TOOL", "MARKETING", "SEO_LANDING", "CONTENT", "INTEGRATION", "DOCS"}
PRIVATE_CLASSES = {"AUTH", "APP", "ACCOUNT", "TRANSACTIONAL", "SYSTEM"}

@dataclass(frozen=True)
class RouteDecision:
    route_class: str
    expected_indexable: bool | None
    reason: str

_PATTERNS = [
    ("SYSTEM", ("/api/", "/webhook", "/oauth/", "/auth/callback", "/callback")),
    ("TRANSACTIONAL", ("/checkout", "/payment", "/success", "/thank-you", "/purchase")),
    ("ACCOUNT", ("/account", "/settings", "/billing", "/profile")),
    ("AUTH", ("/login", "/signin", "/sign-in", "/signup", "/sign-up", "/register", "/forgot-password", "/reset-password")),
    ("APP", ("/dashboard", "/app/", "/workspace", "/console")),
    ("INTEGRATION", ("/integrations", "/integration/")),
    ("SEO_LANDING", ("/solutions", "/use-cases", "/use-case/", "/compare", "/alternatives", "/alternative/")),
    ("CONTENT", ("/guides", "/guide/", "/blog", "/articles", "/article/", "/resources")),
    ("DOCS", ("/docs", "/documentation", "/help/")),
    ("PUBLIC_TOOL", ("/tools", "/tool/", "/converter", "/downloader", "/generator", "/compressor", "/resizer", "/viewer", "/calculator")),
    ("MARKETING", ("/pricing", "/features", "/feature/", "/product", "/about", "/contact", "/enterprise", "/security")),
]

def _match(path: str, needles: tuple[str, ...]) -> bool:
    for needle in needles:
        base = needle.rstrip("/")
        if path == base or path.startswith(base + "/"):
            return True
    return False

def classify_route(url: str, profile: str = "generic") -> str:
    path = urlsplit(url).path.lower() or "/"
    if path == "/":
        if profile == "toolsite":
            return "PUBLIC_TOOL"
        if profile in {"saas", "hybrid"}:
            return "MARKETING"
        return "UNKNOWN"
    for route_class, needles in _PATTERNS:
        if _match(path, needles):
            return route_class
    return "UNKNOWN"

def expectation_for(route_class: str, profile: str) -> bool | None:
    if route_class in PUBLIC_CLASSES:
        return True
    # Login/signup intent varies by product. Treat AUTH as review by default, not a hidden noindex mandate.
    if route_class == "AUTH":
        return None
    if route_class in PRIVATE_CLASSES:
        return False
    if route_class == "UNKNOWN" and profile == "toolsite":
        return None
    return None

def decide_route(url: str, profile: str = "generic", route_override: str | None = None) -> RouteDecision:
    route_class = route_override or classify_route(url, profile)
    expected = expectation_for(route_class, profile)
    if expected is True:
        reason = f"{route_class} is a public search landing class under the {profile} profile."
    elif expected is False:
        reason = f"{route_class} is a private/transactional application class under the {profile} profile."
    else:
        reason = "Route intent is not safe to infer; keep indexability expectation unassessed unless explicitly supplied."
    return RouteDecision(route_class, expected, reason)

def detect_profile(urls: list[str]) -> dict[str, object]:
    classes = [classify_route(url, "generic") for url in urls]
    tool = sum(item == "PUBLIC_TOOL" for item in classes)
    saas_public = sum(item in {"MARKETING", "SEO_LANDING", "INTEGRATION"} for item in classes)
    saas_private = sum(item in {"AUTH", "APP", "ACCOUNT", "TRANSACTIONAL", "SYSTEM"} for item in classes)
    saas = saas_public + saas_private
    if tool and saas:
        profile = "hybrid"
        confidence = "high" if tool >= 2 and saas >= 2 else "medium"
    elif tool:
        profile = "toolsite"
        confidence = "high" if tool >= 2 else "medium"
    elif saas:
        profile = "saas"
        confidence = "high" if saas >= 3 else "medium"
    else:
        profile = "generic"
        confidence = "low"
    return {
        "profile": profile,
        "confidence": confidence,
        "signals": {"public_tool": tool, "saas_public": saas_public, "saas_private": saas_private},
    }
