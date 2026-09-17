#!/usr/bin/env python3
"""Validate the structural contract of a SERP Siege execution report."""
from __future__ import annotations
import argparse, re, sys
from pathlib import Path

EVIDENCE_LABELS={"FIRST_PARTY","USER_SUPPLIED_THIRD_PARTY","LIVE_PUBLIC_OBSERVATION","MODEL_INFERENCE","MISSING"}
DEPRECATED_EVIDENCE_LABELS={"VERIFIED","SUPPLIED_DATA","PUBLIC_OBSERVATION","INFERENCE"}
PAGE_DECISIONS={"SAME_PAGE","NEW_LANDING_PAGE","NEW_TOOL_PAGE","CATEGORY_PAGE","CONTENT_SUPPORT","REJECT"}
NEW_PAGE_DECISIONS=PAGE_DECISIONS-{"SAME_PAGE","REJECT"}
CLUSTER_TYPES={"CORE","FORMAT","CONSTRAINT","USE_CASE","AUDIENCE","PLATFORM","ADJACENT_TOOL","CONTENT_SUPPORT"}
PRIORITIES={"P0","P1","P2","HOLD","REJECT"}
FIRST_BATCH_GROUPS={"CORE","SUPPORTING","ADJACENT"}
COMPETITOR_FEATURE_STATES={"YES","PARTIAL","NO","MISSING"}
CANDIDATE_FEATURE_STATES={"EXISTING","PLANNED","OPTIONAL","REJECTED","MISSING"}
SERP_STRENGTHS={"LOW","MEDIUM","HIGH","VERY_HIGH","MISSING"}
GAPS={"HIGH","MEDIUM","LOW","MISSING"}
REUSE_POTENTIALS={"HIGH","MEDIUM","LOW"}
DEMAND_STRENGTHS={"STRONG","MEDIUM","WEAK","MISSING"}
PAGE_FAMILY_TYPES={"SINGLE","TEMPLATE","CATEGORY","CONTENT"}
TRANSFER_DECISIONS={"ADOPT","ADAPT","REJECT"}
REQUIRED_HEADINGS={"Execution Frame","Assumptions","Search Landscape Summary","Competitor Map","Keyword Cluster Map","Feature Coverage Map","SERP Coverage Map","SEO Page Map","First Batch","Product Roadmap","MVP / P0","P1","P2","Do Not Build Yet","Execution Constraints & Missing Evidence","Next Execution"}
REQUIRED_NONEMPTY_TABLES={"Assumptions","Competitor Map","Keyword Cluster Map","Feature Coverage Map","SERP Coverage Map","SEO Page Map","First Batch","MVP / P0","Execution Constraints & Missing Evidence"}
FORBIDDEN_FIELDS={"Decision","Architecture","Opportunity Score","Separation Risk","Hard Gates"}

def normalize_heading(line): return re.sub(r"^#+\s*","",line.strip()).strip()
def headings(text): return {normalize_heading(l) for l in text.splitlines() if re.match(r"^#{2,3}\s+",l.strip())}
def extract_field(text,label):
    m=re.search(rf"\*\*{re.escape(label)}:\*\*\s*([^\n]+)",text,flags=re.MULTILINE)
    return m.group(1).strip().strip("`") if m else None

def section_text(text,heading):
    m=re.search(rf"^#{{2,3}}\s+{re.escape(heading)}\s*$",text,flags=re.MULTILINE)
    if not m:return ""
    start=m.end(); n=re.search(r"^#{2,3}\s+",text[start:],flags=re.MULTILINE)
    return text[start:start+n.start() if n else len(text)]

def table_rows(section):
    rows=[]
    for line in section.splitlines():
        s=line.strip()
        if not(s.startswith("|") and s.endswith("|")):continue
        cells=[c.strip().strip("`") for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?",c) for c in cells):continue
        rows.append(cells)
    return rows

def data_rows(text,heading):
    rows=table_rows(section_text(text,heading)); return rows[1:] if rows else []
def evidence_labels(value):
    return {p.strip().strip("`") for p in value.split(":",1)[0].split("+")}

def validate_evidence_cell(value,context,errors,require_detail=False):
    labels=evidence_labels(value); invalid=labels-EVIDENCE_LABELS
    if invalid: errors.append(f"{context} has invalid evidence labels: "+", ".join(sorted(invalid))+".")
    if require_detail and labels and labels!={"MISSING"}:
        _,sep,detail=value.partition(":")
        if not sep or not detail.strip(): errors.append(f"{context} requires a traceable source or observation.")

def validate_evidence(text,errors):
    for d in sorted(DEPRECATED_EVIDENCE_LABELS):
        if re.search(rf"(?<![A-Z_]){d}(?![A-Z_])",text): errors.append(f"Deprecated evidence label found: {d}.")
    specs=(("Assumptions",1,5,False),("Competitor Map",6,7,True),("Keyword Cluster Map",7,8,True),("SERP Coverage Map",3,9,True),("Execution Constraints & Missing Evidence",3,6,False),("Evidence Dataset",6,7,True),("Demand Evidence Map",5,6,True),("Page Family Map",8,9,True),("Page Pattern Enhancement",5,6,True))
    for heading,idx,minc,detail in specs:
        for i,row in enumerate(data_rows(text,heading),1):
            if len(row)<minc: errors.append(f"{heading} row {i} has fewer than {minc} columns."); continue
            validate_evidence_cell(row[idx],f"{heading} row {i}",errors,detail)

def validate_keyword_map(text,errors):
    seen=set()
    for i,row in enumerate(data_rows(text,"Keyword Cluster Map"),1):
        if len(row)<8: continue
        cluster,ctype,_,_,_,decision,priority,_=row[:8]
        if not cluster or cluster in {"-","MISSING"}: errors.append(f"Keyword Cluster Map row {i} requires Cluster.")
        elif cluster in seen: errors.append(f"Keyword Cluster Map row {i} duplicates Cluster: {cluster}.")
        else: seen.add(cluster)
        if ctype not in CLUSTER_TYPES: errors.append(f"Keyword Cluster Map row {i} has invalid Type.")
        if decision not in PAGE_DECISIONS: errors.append(f"Keyword Cluster Map row {i} has invalid Page Decision.")
        if priority not in PRIORITIES: errors.append(f"Keyword Cluster Map row {i} has invalid Priority.")

def validate_demand_map(text,errors):
    seen=set()
    for i,row in enumerate(data_rows(text,"Demand Evidence Map"),1):
        if len(row)<6: continue
        cluster,_,_,_,strength,evidence=row[:6]
        if not cluster or cluster in {"-","MISSING"}: errors.append(f"Demand Evidence Map row {i} requires Cluster.")
        elif cluster in seen: errors.append(f"Demand Evidence Map row {i} duplicates Cluster: {cluster}.")
        else: seen.add(cluster)
        if strength not in DEMAND_STRENGTHS: errors.append(f"Demand Evidence Map row {i} has invalid Strength.")
        if strength=="STRONG" and evidence_labels(evidence)<={"MODEL_INFERENCE","MISSING"}:
            errors.append(f"Demand Evidence Map row {i} marks STRONG demand without non-inferred evidence.")

def validate_feature_map(text,errors):
    rows=table_rows(section_text(text,"Feature Coverage Map"))
    if not rows:return
    header=rows[0]
    if len(header)<5: errors.append("Feature Coverage Map must include Feature, at least one competitor, Candidate, Priority, and Evidence."); return
    for i,row in enumerate(rows[1:],1):
        if len(row)!=len(header): errors.append(f"Feature Coverage Map row {i} does not match header column count."); continue
        competitor_states=row[1:-3]; candidate,priority,evidence=row[-3:]
        if not competitor_states: errors.append(f"Feature Coverage Map row {i} requires at least one competitor state.")
        for state in competitor_states:
            if state not in COMPETITOR_FEATURE_STATES: errors.append(f"Feature Coverage Map row {i} has invalid competitor state."); break
        if candidate not in CANDIDATE_FEATURE_STATES: errors.append(f"Feature Coverage Map row {i} has invalid Candidate state.")
        if priority not in PRIORITIES: errors.append(f"Feature Coverage Map row {i} has invalid Priority.")
        validate_evidence_cell(evidence,f"Feature Coverage Map row {i}",errors,True)
        if candidate=="EXISTING" and not(evidence_labels(evidence)&{"FIRST_PARTY","LIVE_PUBLIC_OBSERVATION"}):
            errors.append(f"Feature Coverage Map row {i} marks Candidate EXISTING without first-party or live-public evidence.")

def validate_serp_map(text,errors):
    seen=set()
    for i,row in enumerate(data_rows(text,"SERP Coverage Map"),1):
        if len(row)<9: continue
        cluster,_,_,_,strength,gap,reuse,_,priority=row[:9]
        if not cluster or cluster in {"-","MISSING"}: errors.append(f"SERP Coverage Map row {i} requires Cluster.")
        elif cluster in seen: errors.append(f"SERP Coverage Map row {i} duplicates Cluster: {cluster}.")
        else: seen.add(cluster)
        if strength not in SERP_STRENGTHS: errors.append(f"SERP Coverage Map row {i} has invalid SERP Strength.")
        if gap not in GAPS: errors.append(f"SERP Coverage Map row {i} has invalid Gap.")
        if reuse not in REUSE_POTENTIALS: errors.append(f"SERP Coverage Map row {i} has invalid Reuse Potential.")
        if priority not in PRIORITIES: errors.append(f"SERP Coverage Map row {i} has invalid Priority.")

def validate_page_map(text,errors):
    seen_clusters=set(); seen_urls=set()
    for i,row in enumerate(data_rows(text,"SEO Page Map"),1):
        if len(row)<9: errors.append(f"SEO Page Map row {i} has fewer than 9 columns."); continue
        decision,url,parent,cluster,_,_,shared,priority,reason=row[:9]
        if decision not in PAGE_DECISIONS: errors.append(f"SEO Page Map row {i} has invalid Page Decision.")
        if not cluster or cluster in {"-","MISSING"}: errors.append(f"SEO Page Map row {i} is not bound to a target cluster.")
        elif cluster in seen_clusters: errors.append(f"SEO Page Map row {i} duplicates Target Cluster: {cluster}.")
        else: seen_clusters.add(cluster)
        if decision in NEW_PAGE_DECISIONS and (not url or url in {"-","MISSING"}): errors.append(f"SEO Page Map row {i} requires Proposed URL.")
        if decision in NEW_PAGE_DECISIONS and parent not in {"","-","MISSING"}: errors.append(f"SEO Page Map new-page row {i} must not set Canonical Parent.")
        if url and url not in {"-","MISSING"}:
            if url in seen_urls: errors.append(f"SEO Page Map row {i} duplicates Proposed URL: {url}.")
            else: seen_urls.add(url)
        if decision=="SAME_PAGE" and (not parent or parent in {"-","MISSING"}): errors.append(f"SEO Page Map SAME_PAGE row {i} requires Canonical Parent.")
        if decision=="REJECT" and (not reason or reason in {"-","MISSING"}): errors.append(f"SEO Page Map REJECT row {i} requires Reason.")
        if decision=="REJECT" and (not parent or parent in {"-","MISSING"}): errors.append(f"SEO Page Map REJECT row {i} requires Canonical Parent.")
        if priority=="P0":
            if not shared or shared in {"-","MISSING"}: errors.append(f"SEO Page Map P0 row {i} is missing Shared Core.")
            if not reason or reason in {"-","MISSING"}: errors.append(f"SEO Page Map P0 row {i} is missing Reason.")
        if priority not in PRIORITIES: errors.append(f"SEO Page Map row {i} has invalid Priority.")

def validate_first_batch(text,errors):
    groups=[]; seen=set()
    for i,row in enumerate(data_rows(text,"First Batch"),1):
        if len(row)<6: errors.append(f"First Batch row {i} has fewer than 6 columns."); continue
        _,group,cluster,why,shared,role=row[:6]; groups.append(group)
        if group not in FIRST_BATCH_GROUPS: errors.append(f"First Batch row {i} has invalid Group.")
        if not cluster or cluster in {"-","MISSING"}: errors.append(f"First Batch row {i} is not bound to a target cluster.")
        elif cluster in seen: errors.append(f"First Batch row {i} duplicates Target Cluster: {cluster}.")
        else: seen.add(cluster)
        if not why or why in {"-","MISSING"}: errors.append(f"First Batch row {i} is missing Why Now.")
        if not shared or shared in {"-","MISSING"}: errors.append(f"First Batch row {i} is missing Shared Capability.")
        if not role or role in {"-","MISSING"}: errors.append(f"First Batch row {i} is missing SEO Role.")
    if groups.count("CORE")!=1: errors.append("First Batch must contain exactly one CORE item.")
    total=len(groups); shape=8<=total<=15 and 3<=groups.count("SUPPORTING")<=5 and 2<=groups.count("ADJACENT")<=5
    dev=extract_field(section_text(text,"First Batch"),"First Batch Deviation")
    if not shape and (not dev or dev.upper()=="NONE"): errors.append("First Batch outside the default shape requires First Batch Deviation.")

def validate_page_family(text,errors):
    seen=set(); keyword={r[0] for r in data_rows(text,"Keyword Cluster Map") if r}
    for i,row in enumerate(data_rows(text,"Page Family Map"),1):
        if len(row)<9: continue
        family,ftype,pattern,bound,reps,count,shared,priority,_=row[:9]
        if not family or family in seen: errors.append(f"Page Family Map row {i} requires a unique Family.")
        else: seen.add(family)
        if ftype not in PAGE_FAMILY_TYPES: errors.append(f"Page Family Map row {i} has invalid Type.")
        if not pattern or pattern in {"-","MISSING"}: errors.append(f"Page Family Map row {i} requires URL Pattern.")
        if not shared or shared in {"-","MISSING"}: errors.append(f"Page Family Map row {i} requires Shared Core.")
        if priority not in PRIORITIES: errors.append(f"Page Family Map row {i} has invalid Priority.")
        if ftype=="TEMPLATE":
            try:
                if int(count)<1: raise ValueError
            except ValueError: errors.append(f"Page Family Map row {i} TEMPLATE requires positive Initial Instances.")
            if not reps or reps in {"-","MISSING"}: errors.append(f"Page Family Map row {i} TEMPLATE requires Representative Instances.")
        for cluster in [x.strip() for x in bound.split(";") if x.strip()]:
            if cluster not in keyword: errors.append(f"Page Family Map row {i} references unknown cluster: {cluster}.")

def validate_pattern_enhancement(text,errors):
    rows=data_rows(text,"Page Pattern Enhancement")
    if len(rows)>3: errors.append("Page Pattern Enhancement may keep at most 3 reusable patterns.")
    for i,row in enumerate(rows,1):
        if len(row)<6: continue
        decision=row[3]
        if decision not in TRANSFER_DECISIONS: errors.append(f"Page Pattern Enhancement row {i} has invalid Transfer Decision.")

def rows_by_cluster(text,heading,idx): return {r[idx]:r for r in data_rows(text,heading) if len(r)>idx and r[idx]}

def validate_cross_map_consistency(text,errors):
    keyword=rows_by_cluster(text,"Keyword Cluster Map",0); demand=rows_by_cluster(text,"Demand Evidence Map",0); serp=rows_by_cluster(text,"SERP Coverage Map",0); seo=rows_by_cluster(text,"SEO Page Map",3); batch=rows_by_cluster(text,"First Batch",2)
    for cluster,row in keyword.items():
        s=seo.get(cluster)
        if not s: errors.append(f"Keyword cluster {cluster} is missing from SEO Page Map."); continue
        if len(row)>=7 and len(s)>=8:
            if row[5]!=s[0]: errors.append(f"Cluster {cluster} has inconsistent Page Decision.")
            if row[6]!=s[7]: errors.append(f"Cluster {cluster} has inconsistent Priority.")
    for cluster in demand:
        if cluster not in keyword: errors.append(f"Demand cluster {cluster} is missing from Keyword Cluster Map.")
    for cluster,row in serp.items():
        if cluster not in keyword: errors.append(f"SERP cluster {cluster} is missing from Keyword Cluster Map.")
        s=seo.get(cluster)
        if not s: errors.append(f"SERP cluster {cluster} is missing from SEO Page Map."); continue
        if len(row)>=9 and len(s)>=8 and row[8]!=s[7]: errors.append(f"Cluster {cluster} has inconsistent SERP/SEO Priority.")
        if len(row)>=8 and len(s)>=2 and row[7] and s[1] and row[7]!=s[1]: errors.append(f"Cluster {cluster} has inconsistent Proposed Page.")
    for cluster,row in seo.items():
        if row and row[0]!="REJECT" and cluster not in keyword: errors.append(f"SEO cluster {cluster} is missing from Keyword Cluster Map.")
    for cluster,row in batch.items():
        s=seo.get(cluster)
        if not s: errors.append(f"First Batch cluster {cluster} is missing from SEO Page Map."); continue
        if s[7]!="P0": errors.append(f"First Batch cluster {cluster} must be P0 in SEO Page Map.")
        if row[0].startswith("/") and s[1] and row[0]!=s[1]: errors.append(f"First Batch cluster {cluster} has inconsistent URL.")
    for cluster,row in seo.items():
        if len(row)>=8 and row[7]=="P0" and row[0] in NEW_PAGE_DECISIONS and cluster not in batch: errors.append(f"SEO P0 cluster {cluster} is missing from First Batch.")
    for cluster,row in serp.items():
        if len(row)<9 or row[8]!="P0" or not(row[4]=="MISSING" and row[5]=="MISSING"): continue
        b=batch.get(cluster)
        if b and b[1]!="CORE":
            d=demand.get(cluster); strong=bool(d and len(d)>=5 and d[4]=="STRONG")
            if not strong: errors.append(f"SERP-missing P0 cluster {cluster} must be the First Batch CORE or move to HOLD.")

def validate_next_execution(text,errors):
    s=section_text(text,"Next Execution").lower(); fields={"First action":("first action","第一项动作","第一项开发前动作"),"Required evidence or prerequisite":("required evidence","prerequisite","所需证据","前置条件"),"Success condition":("success condition","成功条件"),"If it fails":("if it fails","失败时"),"First Batch re-evaluation trigger":("re-evaluation trigger","重新调整","重新评估触发")}
    for label,variants in fields.items():
        if not any(v in s for v in variants): errors.append(f"Next Execution is missing {label}.")

def validate(text):
    errors=[]; present=headings(text)
    for req in sorted(REQUIRED_HEADINGS-present): errors.append(f"Missing required heading: {req}.")
    for h in sorted(REQUIRED_NONEMPTY_TABLES):
        if h in present and not data_rows(text,h): errors.append(f"{h} must contain at least one data row.")
    for f in sorted(FORBIDDEN_FIELDS):
        if re.search(rf"\*\*{re.escape(f)}:\*\*",text): errors.append(f"Execution report must not contain field: {f}.")
    if re.search(r"(?<![A-Z_])(GO|CONDITIONAL_GO|NO_GO)(?![A-Z_])",text): errors.append("Execution report must not contain GO/NO_GO decisions.")
    conf=extract_field(text,"Planning Confidence")
    if conf not in {"HIGH","MEDIUM","LOW"}: errors.append("Missing or invalid Planning Confidence.")
    for label in ("Selected direction","Primary job","Target scope","Destination","Destination Basis"):
        if not extract_field(text,label): errors.append(f"Missing Execution Frame field: {label}.")
    dest=extract_field(text,"Destination"); basis=extract_field(text,"Destination Basis")
    if basis:
        validate_evidence_cell(basis,"Destination Basis",errors,require_detail=dest!="NOT_SUPPLIED"); labels=evidence_labels(basis)
        if dest=="NOT_SUPPLIED" and labels!={"MISSING"}: errors.append("NOT_SUPPLIED Destination requires MISSING Destination Basis.")
        if dest!="NOT_SUPPLIED" and not(labels&{"FIRST_PARTY","USER_SUPPLIED_THIRD_PARTY"}): errors.append("Supplied Destination requires FIRST_PARTY or USER_SUPPLIED_THIRD_PARTY basis.")
    validate_evidence(text,errors); validate_keyword_map(text,errors); validate_demand_map(text,errors); validate_feature_map(text,errors); validate_serp_map(text,errors); validate_page_map(text,errors); validate_first_batch(text,errors); validate_page_family(text,errors); validate_pattern_enhancement(text,errors); validate_cross_map_consistency(text,errors)
    for i,row in enumerate(data_rows(text,"MVP / P0"),1):
        if len(row)<4 or not row[3] or row[3] in {"-","MISSING"}: errors.append(f"MVP / P0 row {i} is missing Reason.")
    validate_next_execution(text,errors); return errors

def parse_args():
    p=argparse.ArgumentParser(description="Validate the structural contract of a SERP Siege execution report."); p.add_argument("report",type=Path); return p.parse_args()
def main():
    a=parse_args()
    try:text=a.report.read_text(encoding="utf-8")
    except FileNotFoundError: print(f"error: report not found: {a.report}",file=sys.stderr); return 2
    except UnicodeDecodeError as e: print(f"error: report is not valid UTF-8: {e}",file=sys.stderr); return 2
    errors=validate(text)
    if errors:
        print("SERP Siege execution report validation failed:"); [print(f"- {e}") for e in errors]; return 1
    print("SERP Siege execution report validation passed."); return 0
if __name__=="__main__": raise SystemExit(main())
