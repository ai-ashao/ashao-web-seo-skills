#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
PROFILES={
"zh":{"headings":["执行结论","决策依据","评分明细","拆站风险","Demand / Keyword System 摘要","SERP 切入证据","定位与拆站逻辑","商业化与维护","最小验证方案","Handoff to SERP Siege","最终决策"],"terms":["机会评分","拆站风险","数据置信度","推荐架构"]},
"en":{"headings":["Executive conclusion","Decision basis","Score details","Separation risk","Demand / Keyword System Summary","SERP entry evidence","Positioning and separation logic","Monetization and maintenance","Minimum validation plan","Handoff to SERP Siege","Final decision"],"terms":["Opportunity score","Separation risk","Evidence confidence","Recommended architecture"]}}
VALID={"zh":["独立网站","现有站专区","现有站单页面","观察或放弃"],"en":["INDEPENDENT_SITE","EXISTING_SITE_SECTION","EXISTING_SITE_PAGE","OBSERVE_OR_REJECT"]}
def norm(line): return re.sub(r"^[#\s\d.、-]+","",line).strip()
def detect(text): return "zh" if sum(t in text for t in PROFILES["zh"]["terms"]) >= sum(t.lower() in text.lower() for t in PROFILES["en"]["terms"]) else "en"
def validate(text, lang="auto"):
    if lang=="auto": lang=detect(text)
    errors=[]; heads=[norm(l) for l in text.splitlines() if l.lstrip().startswith("#")]
    for h in PROFILES[lang]["headings"]:
        if not any(h.lower() in x.lower() for x in heads): errors.append(f"Missing required heading: {h}")
    for term in PROFILES[lang]["terms"]:
        if term.lower() not in text.lower(): errors.append(f"Missing required field: {term}")
    if not any(v in text for v in VALID[lang]): errors.append("No valid architecture recommendation found.")
    if "Page matrix" in text or "页面矩阵" in text: errors.append("Downstream page matrix belongs to SERP Siege, not Site Opportunity Scorecard.")
    if "opportunity_context:" not in text: errors.append("Missing SERP Siege handoff payload.")
    return errors
def main():
    p=argparse.ArgumentParser(); p.add_argument("report",type=Path); p.add_argument("--lang",choices=("auto","zh","en"),default="auto"); a=p.parse_args()
    try: text=a.report.read_text(encoding="utf-8")
    except OSError as exc: print(f"error: {exc}",file=sys.stderr); return 2
    e=validate(text,a.lang)
    if e:
        print("Report validation failed:"); [print(f"- {x}") for x in e]; return 1
    print("Report validation passed."); return 0
if __name__=="__main__": raise SystemExit(main())
