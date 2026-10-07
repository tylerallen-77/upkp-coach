from __future__ import annotations
from collections import defaultdict
import statistics, time
from .skill_catalog import BADGE_SKILLS, SECTION_LABELS, label

SECTION_ORDER=["verbal","numerical","logical","figural"]

def _median(xs): return statistics.median(xs) if xs else 0

def _skill_rows(attempts,skill): return [a for a in attempts if a.get("skill")==skill and not a.get("skipped")]

def _skill_gate(rows):
    if not rows:
        return {"attempts":0,"accuracy":0,"median_ms":0,"exam_accuracy":0,"retention":False,"pass":False}
    recent=rows[-20:]
    acc=sum(bool(x.get("correct")) for x in recent)/len(recent)
    med=_median([x.get("elapsed_ms",0) for x in recent])
    targets=_median([x.get("target_ms",45000) for x in recent]) or 45000
    exam=[x for x in rows if int(x.get("level",1))>=3]
    exam_acc=sum(bool(x.get("correct")) for x in exam[-12:])/len(exam[-12:]) if exam else 0
    days={int(float(x.get("ts",0))//86400) for x in rows if x.get("correct")}
    retention=len(days)>=2
    passed=len(rows)>=5 and acc>=.82 and med<=targets*1.08 and len(exam)>=2 and exam_acc>=.75 and retention
    return {"attempts":len(rows),"accuracy":acc,"median_ms":med,"target_ms":targets,
            "exam_attempts":len(exam),"exam_accuracy":exam_acc,"retention":retention,"pass":passed}

def section_badge(attempts, section, sessions=None):
    skills=BADGE_SKILLS.get(section,[])
    details=[]
    for s in skills:
        g=_skill_gate(_skill_rows(attempts,s));g["skill"]=s;g["label"]=label(s);details.append(g)
    covered=sum(1 for x in details if x["attempts"]>=3)
    passed=sum(1 for x in details if x["pass"])
    coverage=covered/max(1,len(skills))
    gate_ratio=passed/max(1,len(skills))
    exam_rows=[a for a in attempts if a.get("skill") in skills and int(a.get("level",1))>=3 and not a.get("skipped")]
    hard_rows=[a for a in attempts if a.get("skill") in skills and int(a.get("level",1))>=4 and not a.get("skipped")]
    exam_acc=sum(bool(a.get("correct")) for a in exam_rows[-30:])/len(exam_rows[-30:]) if exam_rows else 0
    hard_acc=sum(bool(a.get("correct")) for a in hard_rows[-15:])/len(hard_rows[-15:]) if hard_rows else None
    challenge=False
    for s in sessions or []:
        if s.get("kind")=="mastery" and s.get("meta",{}).get("section")==section:
            sm=s.get("summary") or {}
            if sm.get("mastery_passed"):challenge=True;break
    prereq = coverage>=.9 and gate_ratio>=.8 and len(exam_rows)>=max(6,len(skills)) and exam_acc>=.82
    readiness_progress=min(100,round(35*coverage+35*gate_ratio+20*min(1,len(exam_rows)/max(8,len(skills)*2))+10*(1 if challenge else 0)))
    earned=bool(prereq and challenge)
    return {
        "section":section,"label":SECTION_LABELS.get(section,section.title()+" Mastery"),"earned":earned,
        "progress":100 if earned else readiness_progress,"coverage":coverage,"skill_gate_ratio":gate_ratio,
        "exam_attempts":len(exam_rows),"exam_accuracy":exam_acc,"hard_attempts":len(hard_rows),
        "hard_accuracy":hard_acc,"challenge_passed":challenge,"challenge_unlocked":prereq,
        "skills":details,
    }

def tpa_badges(attempts,sessions=None):
    badges=[section_badge(attempts,s,sessions) for s in SECTION_ORDER]
    return {"badges":badges,"earned":sum(x["earned"] for x in badges),"total":len(badges),
            "tpa_ready":all(x["earned"] for x in badges)}

def evaluate_mastery_challenge(section, attempts, session_id):
    rows=[a for a in attempts if a.get("session_id")==session_id and not a.get("skipped")]
    if not rows:return {"mastery_passed":False,"reason":"No answered items"}
    acc=sum(bool(a.get("correct")) for a in rows)/len(rows)
    med=_median([a.get("elapsed_ms",0) for a in rows])
    target=_median([a.get("target_ms",45000) for a in rows]) or 45000
    skill_acc={}
    for sk in set(a.get("skill") for a in rows):
        sr=[a for a in rows if a.get("skill")==sk]
        skill_acc[sk]=sum(bool(a.get("correct")) for a in sr)/len(sr)
    critical_ok=all(v>=.60 for v in skill_acc.values())
    # Challenge deliberately includes L3/L4; Expert L5 is optional.
    passed=len(rows)>=10 and acc>=.85 and med<=target*1.08 and critical_ok
    return {"mastery_passed":passed,"accuracy":acc,"median_ms":med,"target_ms":target,
            "skill_accuracy":skill_acc,"critical_ok":critical_ok,"section":section}
