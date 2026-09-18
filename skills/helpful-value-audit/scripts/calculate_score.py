#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
WEIGHTS={
"intent_task_match":20,"functional_completion":30,"relative_information_gain":15,"reliability_accuracy":15,"task_ux":10,"trust_transparency":5,"supporting_content":5}
EVIDENCE_CAP={"TESTED":4,"OBSERVED":3,"CLAIMED":2,"UNKNOWN":1}
GATE_CAPS={"core_task_failure":49.0,"critical_reliability_failure":49.0,"major_reliability_failure":69.0,"deceptive_functionality":39.0}
class InputError(ValueError): pass

def calculate(data):
    ratings=data.get("ratings");
    if not isinstance(ratings,dict): raise InputError("ratings must be an object")
    total=0.0; breakdown={}
    for key,w in WEIGHTS.items():
        item=ratings.get(key)
        if not isinstance(item,dict): raise InputError(f"missing rating: {key}")
        r=item.get("rating"); ev=str(item.get("evidence","UNKNOWN")).upper()
        if isinstance(r,bool) or not isinstance(r,int) or not 0<=r<=4: raise InputError(f"{key}.rating must be integer 0-4")
        if ev not in EVIDENCE_CAP: raise InputError(f"{key}.evidence invalid")
        if key=="functional_completion" and r>EVIDENCE_CAP[ev]: raise InputError(f"functional_completion rating {r} exceeds {ev} evidence cap {EVIDENCE_CAP[ev]}")
        pts=r/4*w; total+=pts; breakdown[key]={"rating":r,"evidence":ev,"points":round(pts,1),"max":w}
    raw=round(total,1)
    gates=data.get("gates",[])
    if not isinstance(gates,list): raise InputError("gates must be an array")
    caps=[]; triggered=[]
    for g in gates:
        if not isinstance(g,dict): raise InputError("gate must be object")
        gid=g.get("id"); on=g.get("triggered")
        if gid not in GATE_CAPS: raise InputError(f"unknown gate: {gid}")
        if not isinstance(on,bool): raise InputError(f"{gid}.triggered must be boolean")
        if on: caps.append(GATE_CAPS[gid]); triggered.append({"id":gid,"cap":GATE_CAPS[gid],"note":g.get("note","")})
    final=round(min([raw,*caps]) if caps else raw,1)
    return {"raw_score":raw,"helpful_strength":final,"triggered_gates":triggered,"breakdown":breakdown}

def main():
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); a=p.parse_args()
    try: data=json.loads(a.input.read_text(encoding="utf-8")); result=calculate(data)
    except (OSError,json.JSONDecodeError,InputError) as exc: print(f"error: {exc}",file=sys.stderr); return 2
    print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
