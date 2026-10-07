"""Adaptive question selection for UPKP Coach V2.1."""
from __future__ import annotations
import random, time
from . import engine
from .learning import chapter_for_skill, infer_skill, daily_prescription, profile_map, adaptive_level, personal_target_ms
from .skill_catalog import tag_question


def _tag_all(qs):
    return [tag_question(q) for q in qs]


def build_for_skill(skill: str, n: int, level: int = 0, seed: int | None = None,
                    attempts: list[dict] | None = None, target_seconds: int | None = None):
    bab = chapter_for_skill(skill)
    if not bab:
        return []
    prof = profile_map(attempts or []).get(skill) if attempts is not None else None
    lv = level or adaptive_level(prof)
    rng = random.Random(seed if seed is not None else time.time_ns())
    pool = _tag_all(engine.bangun(bab, max(n*6,n), lv, rng))
    exact = [q for q in pool if q.skill == skill]
    other = [q for q in pool if q.skill != skill]
    qs = (exact + other)[:n]
    if target_seconds is None and prof:
        target_seconds=max(18, round(personal_target_ms(prof, int(getattr(qs[0], 'waktu',45)*1000 if qs else 45000))/1000))
    if target_seconds:
        for q in qs: q.waktu=int(target_seconds)
    return qs


def build_mixed(n: int, level: int = 0, seed: int | None = None):
    rng = random.Random(seed if seed is not None else time.time_ns())
    plan=["padanan","kelompok","silogisme","analisis","operasi","persamaan","aritsos","banding","jarak","statistika","deret","deretfig","analogifig"]
    rng.shuffle(plan); result=[]; used=set(); i=0
    while len(result)<n and i<n*8:
        kode=plan[i%len(plan)]
        qs=engine.bangun(kode,1,level,rng,used)
        if qs:
            q=tag_question(qs[0]); result.append(q); used.add(q.id)
        i+=1
    return result[:n]


def build_prescription(attempts:list[dict],max_minutes:int=20,seed:int|None=None):
    rx=daily_prescription(attempts,max_minutes=max_minutes); questions=[]
    for idx,item in enumerate(rx["items"]):
        local_seed=None if seed is None else seed+idx
        if item["kind"]=="skill":
            qs=build_for_skill(item["skill"],item["questions"],level=item.get("level",0),seed=local_seed,attempts=attempts,target_seconds=item.get("target_seconds"))
        else:
            qs=build_mixed(item["questions"],level=item.get("level",0),seed=local_seed)
            for q in qs: q.waktu=int(item.get("target_seconds",q.waktu))
        for q in qs:
            d=q.to_dict(); d["prescription_item"]={k:v for k,v in item.items() if k!="reason"}; questions.append(d)
    return rx,questions


def build_speed_lab(kind:str="skip_or_solve", n:int=12, attempts:list[dict]|None=None, seed:int|None=None):
    """Generate focused speed sets. The exam behavior is handled by the client/API telemetry."""
    rng=random.Random(seed if seed is not None else time.time_ns())
    if kind=="arithmetic_blitz": plan=["operasi","persamaan","aritsos","banding"]
    elif kind=="logic_sprint": plan=["silogisme","analisis"]
    elif kind=="sequence_30": plan=["deret"]
    else: plan=["operasi","banding","deret","silogisme","analisis","padanan","kelompok"]
    result=[]; used=set(); i=0
    while len(result)<n and i<n*10:
        code=plan[i%len(plan)]; profs=profile_map(attempts or [])
        qs=engine.bangun(code,1,0,rng,used)
        if qs:
            q=tag_question(qs[0]); p=profs.get(q.skill)
            if p: q.waktu=max(18,round(personal_target_ms(p,q.waktu*1000)/1000))
            result.append(q); used.add(q.id)
        i+=1
    return result[:n]


def build_tryout(n:int=60, seed:int|None=None):
    """Configurable TPA simulation set; count is a product setting, not an official exam claim."""
    return build_mixed(n=n, level=0, seed=seed)
