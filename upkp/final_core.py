from __future__ import annotations
import random, time
from . import engine, learning
from .skill_catalog import tag_question, BADGE_SKILLS, chapter
from .advanced_tpa import generate as generate_advanced, ADVANCED_SKILLS

TPA_CODES=["padanan","kelompok","silogisme","analisis","operasi","persamaan","geometri","aritsos","sudut","banding","jarak","peluang","statistika","deret","deretfig","analogifig"]
SUB_CODES=["etika","wawasan","nilai","kepegawaian","keuangan","struktur"]
TRACK_CODES={"tpa":TPA_CODES,"substansi":SUB_CODES}

def _qs_for_codes(codes,n,level=0,seed=None):
    rng=random.Random(seed if seed is not None else time.time_ns())
    codes=list(codes); rng.shuffle(codes); out=[]; used=set(); i=0
    while len(out)<n and i<n*14:
        code=codes[i%len(codes)]
        lv=min(3,level) if level else 0
        qs=engine.bangun(code,1,lv,rng,used)
        if qs:
            q=tag_question(qs[0]); out.append(q); used.add(q.id)
        i+=1
    return out[:n]

def build_mixed(track:str,n:int,level:int=0,seed=None):
    return _qs_for_codes(TRACK_CODES.get(track,TPA_CODES),n,level,seed)

def build_for_skill(skill:str,n:int,attempts:list[dict],level:int=0,seed=None,target_seconds:int|None=None):
    prof=learning.profile_map(attempts).get(skill)
    lv=level or learning.adaptive_level(prof)
    rng=random.Random(seed if seed is not None else time.time_ns())
    out=[]
    # Advanced transfer skills are deliberately L4 constructs. Once the coach
    # targets one of them, generate that construct directly instead of falling
    # back to a different legacy chapter skill.
    if skill in ADVANCED_SKILLS:
        for _ in range(n*4):
            q=generate_advanced(skill,max(4,lv),rng)
            if q: out.append(q)
            if len(out)>=n: break
    elif lv>=4:
        for _ in range(n*3):
            q=generate_advanced(skill,lv,rng)
            if q: out.append(q)
            if len(out)>=n: break
    ch=chapter(skill)
    if len(out)<n and ch:
        pool=[tag_question(q) for q in engine.bangun(ch,max((n-len(out))*6,n),min(3,lv),rng)]
        exact=[q for q in pool if q.skill==skill]; other=[q for q in pool if q.skill!=skill]
        out.extend((exact+other)[:n-len(out)])
    if target_seconds:
        for q in out:q.waktu=int(target_seconds)
    return out[:n]

def build_prescription(track:str,attempts:list[dict],max_minutes:int=18,seed=None):
    filtered=[a for a in attempts if a.get("track", track)==track]
    rx=learning.daily_prescription(filtered,max_minutes=max_minutes); qs=[]
    for i,item in enumerate(rx["items"]):
        local=None if seed is None else seed+i
        if item["kind"]=="skill":
            got=build_for_skill(item["skill"],item["questions"],filtered,item.get("level",0),local,item.get("target_seconds"))
        elif item["kind"]=="diagnostic" and track=="tpa":
            # Baseline must reveal a ceiling, not just prove that Foundation is easy.
            n=item["questions"]; cuts=[n//3,n//3,n-(2*(n//3))]
            got=[]
            for lv,count in zip((1,2,3),cuts):
                got.extend(build_mixed(track,count,lv,None if local is None else local+lv))
            random.Random(local if local is not None else time.time_ns()).shuffle(got)
            for q in got:q.waktu=int(item.get("target_seconds",q.waktu))
        else:
            got=build_mixed(track,item["questions"],item.get("level",0),local)
            for q in got:q.waktu=int(item.get("target_seconds",q.waktu))
        for q in got:
            d=q.to_dict(); d["track"]=track; d["prescription_item"]={k:v for k,v in item.items() if k!="reason"}; qs.append(d)
    # ~10% stretch exposure: original Hard archetypes from expanded TPA sources.
    # This prevents mastery from being based only on familiar/easy templates.
    if track=="tpa" and len(filtered)>=12:
        stretch=["verbal.critical_inference","logika.constraint_ordering","logika.assignment_constraints","numerik.multi_step_percent","numerik.data_interpretation","figural.matrix_transform"]
        counts={s:sum(1 for a in filtered if a.get("skill")==s) for s in stretch}
        chosen=sorted(stretch,key=lambda s:counts[s])[:2]
        for j,sk in enumerate(chosen):
            q=generate_advanced(sk,4,random.Random((seed or time.time_ns())+100+j))
            if q:
                d=q.to_dict();d["track"]="tpa";d["prescription_item"]={"kind":"stretch","label":"Stretch · "+sk.split(".")[-1].replace("_"," "),"level":4}
                qs.append(d)
        rx["items"].append({"kind":"stretch","label":"Hard transfer","questions":len(chosen),"minutes":2,"level":4,"reason":"10% stretch exposure"})
    return rx,qs

def build_tryout(track:str,n:int|None=None,seed=None):
    rng=random.Random(seed if seed is not None else time.time_ns())
    if n is None:
        package="potensi" if track=="tpa" else "tskkwk"
        return [q.to_dict()|{"track":track} for q in engine.bangun_tryout(package,0,rng)]
    return [q.to_dict()|{"track":track} for q in build_mixed(track,n,0,seed)]

def build_mastery_challenge(section:str,track:str="tpa",seed=None):
    """Section challenge. TPA uses Exam/Hard transfer; Substansi uses fresh Exam-level knowledge items."""
    if section not in BADGE_SKILLS: return []
    rng=random.Random(seed if seed is not None else time.time_ns())
    qs=[]
    if track=="substansi":
        skills=BADGE_SKILLS[section]
        i=0
        while len(qs)<15 and i<180:
            sk=skills[i%len(skills)]
            ch=chapter(sk)
            if ch:
                built=engine.bangun(ch,1,3,rng)
                if built:
                    q=tag_question(built[0]);qs.append(q.to_dict()|{"track":"substansi","challenge":True})
            i+=1
        rng.shuffle(qs)
        return qs[:15]
    advanced_by_section={
        "verbal":["verbal.critical_inference"],
        "numerical":["numerik.multi_step_percent","numerik.weighted_average","numerik.data_interpretation"],
        "logical":["logika.constraint_ordering","logika.assignment_constraints","logika.only_if"],
        "figural":["figural.matrix_transform"],
    }
    hard=advanced_by_section.get(section,[])
    for i in range(4):
        if not hard:break
        skill=hard[i%len(hard)]
        q=generate_advanced(skill,4,rng)
        if q:qs.append(q.to_dict()|{"track":"tpa","challenge":True})
    skills=BADGE_SKILLS[section]
    i=0
    while len(qs)<15 and i<150:
        sk=skills[i%len(skills)]
        ch=chapter(sk)
        if ch:
            built=engine.bangun(ch,1,3,rng)
            if built:
                q=tag_question(built[0]);qs.append(q.to_dict()|{"track":"tpa","challenge":True})
        i+=1
    rng.shuffle(qs)
    return qs[:15]
