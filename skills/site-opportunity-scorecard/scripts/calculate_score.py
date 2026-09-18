#!/usr/bin/env python3
"""Calculate opportunity and site-separation risk scores with decision profiles."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from typing import Any

OPPORTUNITY_WEIGHTS = {
    "independent_primary_keyword": 12,
    "serp_breakability": 15,
    "long_tail_expansion": 12,
    "user_use_case_difference": 12,
    "homepage_workflow_difference": 10,
    "independent_brand_reason": 10,
    "link_distribution_potential": 10,
    "independent_content_system": 9,
    "development_maintenance_economics": 5,
    "monetization_fit": 5,
}
RISK_WEIGHTS = {
    "keyword_overlap": 20,
    "search_intent_overlap": 20,
    "product_workflow_overlap": 15,
    "content_template_overlap": 15,
    "brand_positioning_ambiguity": 10,
    "link_authority_fragmentation": 10,
    "development_maintenance_fragmentation": 10,
}
SEARCH_KEYS = {"independent_primary_keyword", "serp_breakability", "long_tail_expansion"}
PRODUCT_KEYS = {"user_use_case_difference", "homepage_workflow_difference", "independent_brand_reason"}
VALID_CONFIDENCE = {"LOW", "MEDIUM", "HIGH"}
VALID_HARD_GATE_SCOPES = {"SITE_ONLY", "BLOCK_PRODUCT"}
VALID_PROFILES = {"generic", "seo_first_utility", "product_led", "content_site", "downloader"}

class InputError(ValueError):
    pass

def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    if not isinstance(data, dict):
        raise InputError("Top-level JSON value must be an object.")
    return data

def validate_scores(section: Any, weights: dict[str, int], name: str) -> dict[str, float]:
    if not isinstance(section, dict):
        raise InputError(f"'{name}' must be an object.")
    missing = [k for k in weights if k not in section]
    extra = [k for k in section if k not in weights]
    if missing: raise InputError(f"Missing {name} keys: {', '.join(missing)}")
    if extra: raise InputError(f"Unknown {name} keys: {', '.join(extra)}")
    out = {}
    for key in weights:
        value = section[key]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= float(value) <= 5:
            raise InputError(f"'{name}.{key}' must be a number from 0 to 5.")
        out[key] = float(value)
    return out

def validate_hard_gates(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise InputError("'hard_gates' must be an array.")
    gates = []
    for item in value:
        if isinstance(item, str):
            if item.strip(): gates.append({"reason": item.strip(), "scope": "SITE_ONLY"})
            continue
        if not isinstance(item, dict): raise InputError("Each hard gate must be a string or object.")
        reason, scope = item.get("reason"), str(item.get("scope", "")).upper()
        if not isinstance(reason, str) or not reason.strip(): raise InputError("Hard gate requires non-empty reason.")
        if scope not in VALID_HARD_GATE_SCOPES: raise InputError("Hard gate scope must be SITE_ONLY or BLOCK_PRODUCT.")
        gates.append({"reason": reason.strip(), "scope": scope})
    return gates

def exact_total(scores: dict[str, float], weights: dict[str, int]) -> float:
    return sum(scores[k] / 5.0 * weights[k] for k in weights)

def weighted_breakdown(scores: dict[str, float], weights: dict[str, int]) -> dict[str, float]:
    return {k: round(scores[k] / 5.0 * w, 1) for k, w in weights.items()}

def choose_recommendation(total: float, risk: float, scores: dict[str, float], gates: list[dict[str,str]], confidence: str, profile: str = "generic") -> tuple[str, list[str]]:
    reasons = []
    if any(g["scope"] == "BLOCK_PRODUCT" for g in gates):
        return "OBSERVE_OR_REJECT", ["A product-blocking hard gate is active."]
    if gates:
        reasons.append("A SITE_ONLY hard gate blocks a new domain until resolved.")
        if total >= 60: return "EXISTING_SITE_SECTION", reasons
        if total >= 40: return "EXISTING_SITE_PAGE", reasons
        return "OBSERVE_OR_REJECT", reasons

    search_subtotal = sum(scores[k] / 5 * OPPORTUNITY_WEIGHTS[k] for k in SEARCH_KEYS)
    product_subtotal = sum(scores[k] / 5 * OPPORTUNITY_WEIGHTS[k] for k in PRODUCT_KEYS)
    common = total >= 75 and risk <= 40 and search_subtotal >= 26 and scores["independent_primary_keyword"] >= 3 and confidence in {"MEDIUM","HIGH"}

    if profile in {"seo_first_utility", "downloader"}:
        independent = common and scores["long_tail_expansion"] >= 3 and scores["independent_content_system"] >= 3
        if independent:
            reasons.append("Independent demand, expansion depth, and separation risk support a standalone SEO utility; workflow novelty is not a hard gate for this profile.")
            return "INDEPENDENT_SITE", reasons
    elif profile == "content_site":
        independent = common and scores["independent_content_system"] >= 4 and scores["user_use_case_difference"] >= 2
        if independent:
            reasons.append("Independent demand and a distinct content system support a standalone content property.")
            return "INDEPENDENT_SITE", reasons
    else:  # generic / product_led
        independent = common and product_subtotal >= 22 and scores["homepage_workflow_difference"] >= 3
        if independent:
            reasons.append("Opportunity, product differentiation, and separation-risk gates support a new domain.")
            return "INDEPENDENT_SITE", reasons

    if total >= 60:
        if confidence == "LOW": reasons.append("Low confidence favors reversible validation on the existing domain.")
        if risk > 40: reasons.append("Separation risk favors authority concentration.")
        return "EXISTING_SITE_SECTION", reasons or ["The opportunity is substantial but does not clear the independent-site gate for this profile."]
    if total >= 40:
        return "EXISTING_SITE_PAGE", ["The opportunity supports a focused page but not a durable independent site system."]
    return "OBSERVE_OR_REJECT", ["The opportunity is below the default build threshold or lacks sufficient independent evidence."]

def calculate(data: dict[str, Any]) -> dict[str, Any]:
    scores = validate_scores(data.get("opportunity_scores"), OPPORTUNITY_WEIGHTS, "opportunity_scores")
    risks = validate_scores(data.get("risk_scores"), RISK_WEIGHTS, "risk_scores")
    gates = validate_hard_gates(data.get("hard_gates", []))
    confidence = str(data.get("overall_confidence", "LOW")).upper()
    if confidence not in VALID_CONFIDENCE: raise InputError("overall_confidence must be LOW, MEDIUM, or HIGH.")
    profile = str(data.get("decision_profile", "generic")).lower()
    if profile not in VALID_PROFILES: raise InputError(f"decision_profile must be one of: {', '.join(sorted(VALID_PROFILES))}")
    total, risk = round(exact_total(scores, OPPORTUNITY_WEIGHTS),1), round(exact_total(risks, RISK_WEIGHTS),1)
    recommendation, reasons = choose_recommendation(total, risk, scores, gates, confidence, profile)
    return {
        "decision_profile": profile,
        "opportunity_score": total,
        "separation_risk": risk,
        "overall_confidence": confidence,
        "recommendation": recommendation,
        "recommendation_reasons": reasons,
        "hard_gates": [gate["reason"] for gate in gates],
        "hard_gate_scopes": gates,
        "subtotals": {
            "search_opportunity": round(sum(weighted_breakdown(scores, OPPORTUNITY_WEIGHTS)[k] for k in SEARCH_KEYS), 1),
            "product_differentiation": round(sum(weighted_breakdown(scores, OPPORTUNITY_WEIGHTS)[k] for k in PRODUCT_KEYS), 1),
            "independent_growth": round(sum(weighted_breakdown(scores, OPPORTUNITY_WEIGHTS)[k] for k in ("link_distribution_potential", "independent_content_system")), 1),
            "site_economics": round(sum(weighted_breakdown(scores, OPPORTUNITY_WEIGHTS)[k] for k in ("development_maintenance_economics", "monetization_fit")), 1),
        },
        "opportunity_breakdown": weighted_breakdown(scores, OPPORTUNITY_WEIGHTS),
        "risk_breakdown": weighted_breakdown(risks, RISK_WEIGHTS),
    }

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument("input", type=Path); p.add_argument("--pretty", action="store_true"); args=p.parse_args()
    try: result=calculate(load_json(args.input))
    except InputError as exc: print(f"error: {exc}", file=sys.stderr); return 2
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty or sys.stdout.isatty() else None)); return 0
if __name__ == "__main__": raise SystemExit(main())
