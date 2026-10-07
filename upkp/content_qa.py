"""Automated content-quality gate for generated TPA questions."""
from __future__ import annotations
from collections import Counter, defaultdict
import random, re
from . import engine
from .skill_catalog import SKILLS
from .exam_engine import structural_signature
from .advanced_tpa import ADVANCED_SKILLS, generate as generate_advanced


def validate_question(q) -> list[str]:
    d=q.to_dict() if hasattr(q,"to_dict") else dict(q)
    issues=[]
    opts=d.get("opts") or []
    if not str(d.get("stem","")).strip(): issues.append("empty_stem")
    if len(opts)!=5: issues.append("option_count")
    if len({str(x).strip() for x in opts})!=len(opts): issues.append("duplicate_options")
    ans=d.get("ans")
    if not isinstance(ans,int) or not 0<=ans<len(opts): issues.append("invalid_answer_index")
    if not str(d.get("exp","")).strip(): issues.append("missing_explanation")
    if not str(d.get("trick","")).strip(): issues.append("missing_shortcut")
    if not d.get("skill"): issues.append("missing_skill")
    elif d.get("skill") not in SKILLS and not str(d.get("skill")).startswith("bab."): issues.append("unknown_skill")
    if not 10<=int(d.get("waktu",45))<=180: issues.append("target_time_outlier")
    if int(d.get("lv",0)) not in (1,2,3,4,5): issues.append("invalid_level")
    if int(d.get("lv",0))>=4 and not str(d.get("archetype","")).strip(): issues.append("missing_archetype")
    return issues


def audit(sample_per_level:int=12, seed:int=20261007) -> dict:
    rng=random.Random(seed); issues=[]; signatures=Counter(); families=defaultdict(lambda:{"n":0,"issues":0,"skills":Counter()})
    for code in sorted(engine.BAB_BY_KODE):
        levels=engine.level_tersedia(code)
        for lv in levels:
            for _ in range(sample_per_level):
                try:
                    qs=engine.bangun(code,1,lv,rng)
                    if not qs:
                        issues.append({"chapter":code,"level":lv,"issues":["no_question"]});continue
                    q=qs[0]; d=q.to_dict(); bad=validate_question(q); sig=structural_signature(d); signatures[sig]+=1
                    f=families[code];f["n"]+=1;f["skills"][d.get("skill","")]+=1
                    if bad: f["issues"]+=1;issues.append({"chapter":code,"level":lv,"id":d.get("id"),"issues":bad})
                except Exception as e:
                    families[code]["issues"]+=1;issues.append({"chapter":code,"level":lv,"issues":["generator_exception"],"detail":repr(e)[:240]})
    total=sum(x["n"] for x in families.values()); dup=sum(c-1 for c in signatures.values() if c>1)
    return {"ok":not issues,"sampled":total,"issue_count":len(issues),"structural_duplicate_rate":dup/max(total,1),
            "families":{k:{"n":v["n"],"issues":v["issues"],"skills":dict(v["skills"])} for k,v in families.items()},"issues":issues[:200]}


def audit_advanced(samples_per_skill:int=30, seed:int=20261008) -> dict:
    rng=random.Random(seed); issues=[]; signatures=Counter(); by_skill={}
    for skill in ADVANCED_SKILLS:
        row={"n":0,"issues":0,"levels":Counter(),"archetypes":Counter()}
        for i in range(samples_per_skill):
            lv=4 if i%4 else 5
            try:
                q=generate_advanced(skill,lv,rng)
                if q is None:
                    row["issues"]+=1;issues.append({"skill":skill,"level":lv,"issues":["no_question"]});continue
                bad=validate_question(q);d=q.to_dict();signatures[structural_signature(d)]+=1;row["n"]+=1;row["levels"][lv]+=1;row["archetypes"][d.get("archetype","")]+=1
                if d.get("waktu",0)<35: bad.append("hard_target_too_short")
                if d.get("skill")!=skill and not (skill=="numerik.rate_change_table" and d.get("skill")=="numerik.data_interpretation"):
                    bad.append("skill_mismatch")
                if bad:
                    row["issues"]+=1;issues.append({"skill":skill,"level":lv,"id":d.get("id"),"issues":bad})
            except Exception as e:
                row["issues"]+=1;issues.append({"skill":skill,"level":lv,"issues":["generator_exception"],"detail":repr(e)[:240]})
        # Hard content should expose at least two distinct reasoning archetypes per skill.
        if len(row["archetypes"])<2:
            row["issues"]+=1;issues.append({"skill":skill,"issues":["insufficient_archetype_diversity"],"archetypes":dict(row["archetypes"])})
        row["levels"]=dict(row["levels"]);row["archetypes"]=dict(row["archetypes"]);by_skill[skill]=row
    total=sum(x["n"] for x in by_skill.values());dup=sum(c-1 for c in signatures.values() if c>1)
    return {"ok":not issues,"sampled":total,"issue_count":len(issues),"template_repetition_rate":dup/max(total,1),
            "archetype_total":sum(len(x["archetypes"]) for x in by_skill.values()),"skills":by_skill,"issues":issues[:200]}
