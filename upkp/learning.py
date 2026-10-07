"""UPKP Coach V2.1 adaptive learning engine.

Pure learning logic: micro-skill profiles, mastery, personalized speed targets,
spaced review, adaptive difficulty, prescriptions, and session post-mortems.
"""
from __future__ import annotations
from collections import defaultdict
from math import exp
import statistics
import time
from typing import Iterable

from .skill_catalog import label as skill_label, chapter as chapter_for_skill, classify_legacy
from .exam_engine import structural_signature

MASTERY_STATES = ("Unseen", "Learning", "Weak", "Improving", "Stable", "Mastered")
CONFIDENCE_VALUES = ("yakin", "50:50", "tebak", "")
REVIEW_INTERVAL_DAYS = (0, 1, 3, 7, 14, 30)


def infer_skill(q: dict) -> str:
    """Compatibility helper. V2.1 prefers explicit stored ``skill`` tags."""
    return str(q.get("skill") or classify_legacy(q))


def classify_error(correct: bool, elapsed_ms: int, target_ms: int, confidence: str = "", skipped: bool = False, answer_changes: int = 0) -> str:
    if skipped: return "skipped"
    slow = elapsed_ms > target_ms * 1.15
    if correct:
        if answer_changes >= 2: return "hesitation"
        if slow: return "slow_correct"
        return "clean_correct"
    if confidence == "yakin": return "high_confidence_wrong"
    if elapsed_ms < target_ms * .45: return "premature_guess"
    if answer_changes >= 2: return "unstable_reasoning"
    return "wrong"


def make_attempt(q: dict, *, selected: int | None, correct: bool, elapsed_ms: int,
                 confidence: str = "", first_selection_ms: int | None = None,
                 answer_changes: int = 0, skipped: bool = False, pass_number: int = 1,
                 session_id: str = "", now: float | None = None) -> dict:
    target_ms = int(q.get("waktu", 45) * 1000)
    confidence = confidence if confidence in CONFIDENCE_VALUES else ""
    skill = infer_skill(q)
    return {
        "ts": float(now if now is not None else time.time()), "session_id": session_id,
        "question_id": q.get("id", ""), "item_signature": structural_signature(q), "bab": q.get("bab", ""), "skill": skill,
        "level": int(q.get("lv", 1)), "selected": selected, "answer": q.get("ans"),
        "correct": bool(correct), "elapsed_ms": max(0,min(int(elapsed_ms),300_000)),
        "target_ms": max(1_000,target_ms),
        "first_selection_ms": None if first_selection_ms is None else max(0,int(first_selection_ms)),
        "answer_changes": max(0,int(answer_changes)), "confidence": confidence,
        "skipped": bool(skipped), "pass_number": max(1,int(pass_number)),
        "error_type": classify_error(correct, elapsed_ms, target_ms, confidence, skipped, answer_changes),
    }


def _median(values):
    vals=list(values)
    return statistics.median(vals) if vals else 0.0


def _recency_weight(ts: float, now: float) -> float:
    age_days=max(0.0,(now-ts)/86400)
    return .18+.82*exp(-age_days/20.2)


def _review_stage(rows: list[dict]) -> int:
    """Skill-level spaced repetition stage.

    A clean/near-target correct answer promotes one stage. Any substantive error
    resets to stage 0. Slow-correct/hesitation hold the stage instead of promoting.
    """
    stage=0
    for r in sorted(rows,key=lambda x:x.get("ts",0)):
        e=r.get("error_type")
        if e in ("wrong","high_confidence_wrong","premature_guess","unstable_reasoning","skipped"):
            stage=0
        elif e == "clean_correct":
            stage=min(stage+1,len(REVIEW_INTERVAL_DAYS)-1)
    return stage


def _due_at(rows: list[dict]) -> float:
    if not rows: return 0
    stage=_review_stage(rows)
    last=float(sorted(rows,key=lambda x:x.get("ts",0))[-1].get("ts",0))
    return last + REVIEW_INTERVAL_DAYS[stage]*86400


def personal_target_ms(profile: dict | None, base_ms: int = 45_000) -> int:
    """Shrink the target only after demonstrated accuracy and evidence.

    Never chases a single fast outlier. Floor is 55% of chapter baseline.
    """
    if not profile or profile.get("n",0)<3:
        return int(base_ms)
    acc=profile["accuracy"]; n=profile["n"]; med=profile["median_ms"] or base_ms
    floor=base_ms*.55
    if acc < .70:
        desired=max(base_ms,med*.95)
    elif acc < .82:
        desired=min(base_ms, max(floor, med*.95))
    elif acc < .90 or n < 8:
        desired=min(base_ms*.92, max(floor, med*.90))
    elif profile.get("state") == "Mastered":
        desired=min(base_ms*.75, max(floor, med*.85))
    else:
        desired=min(base_ms*.84, max(floor, med*.88))
    return int(round(desired/1000)*1000)


def adaptive_level(profile: dict | None) -> int:
    if not profile or profile.get("n",0)<3: return 1
    if profile["accuracy"] < .68 or profile.get("state") == "Weak": return 1
    if profile.get("state") in ("Learning","Improving") or profile["accuracy"] < .84: return 2
    if profile["accuracy"] < .92 or profile.get("n",0) < 14: return 3
    return 4


def profile_attempts(attempts: Iterable[dict], now: float | None = None) -> list[dict]:
    now=float(now if now is not None else time.time())
    groups=defaultdict(list)
    for a in attempts: groups[a.get("skill") or "unknown"].append(a)
    out=[]
    for skill,rows in groups.items():
        rows=sorted(rows,key=lambda x:x.get("ts",0)); n=len(rows)
        weights=[_recency_weight(float(r.get("ts",now)),now) for r in rows]; wsum=sum(weights) or 1
        acc=sum(w*(1 if r.get("correct") else 0) for w,r in zip(weights,rows))/wsum
        med=_median(float(r.get("elapsed_ms",0)) for r in rows)
        base_target=_median(float(r.get("target_ms",45_000)) for r in rows) or 45_000
        speed_ratio=med/base_target
        confident=[r for r in rows if r.get("confidence")=="yakin"]
        conf_acc=sum(1 for r in confident if r.get("correct"))/len(confident) if confident else None
        clean_recent=0
        for r in reversed(rows):
            if r.get("error_type")=="clean_correct": clean_recent+=1
            else: break
        evidence=min(1.0,n/12); speed_score=max(0,min(1,1.35-speed_ratio))
        mastery=max(0,min(1,.62*acc+.23*speed_score+.15*evidence))
        if n<3: state="Learning"
        elif acc<.62: state="Weak"
        elif mastery<.76 or clean_recent<2: state="Improving"
        elif mastery<.9 or n<10 or clean_recent<3: state="Stable"
        else: state="Mastered"
        hc=sum(1 for r in rows[-12:] if r.get("error_type")=="high_confidence_wrong")
        slow=sum(1 for r in rows[-12:] if r.get("error_type")=="slow_correct")
        last=float(rows[-1].get("ts",now)); days=max(0,(now-last)/86400)
        stage=_review_stage(rows); due=_due_at(rows); overdue=max(0,(now-due)/86400) if due else 0
        priority=(1-acc)*1.7+max(0,speed_ratio-1)*.8+hc*.10+slow*.04+min(days,14)*.012+min(overdue,7)*.08
        p={"skill":skill,"label":skill_label(skill),"n":n,"accuracy":acc,"median_ms":med,
           "target_median_ms":base_target,"speed_ratio":speed_ratio,"confidence_accuracy":conf_acc,
           "mastery":mastery,"state":state,"clean_streak":clean_recent,"high_confidence_wrong":hc,
           "slow_correct":slow,"last_ts":last,"priority":priority,"review_stage":stage,"due_at":due,
           "overdue_days":overdue}
        p["personal_target_ms"]=personal_target_ms(p,int(base_target)); p["recommended_level"]=adaptive_level(p)
        out.append(p)
    return sorted(out,key=lambda x:(-x["priority"],x["label"]))


def profile_map(attempts:list[dict], now:float|None=None)->dict[str,dict]:
    return {p["skill"]:p for p in profile_attempts(attempts,now)}


def overall_metrics(attempts:list[dict])->dict:
    if not attempts: return {"n":0,"accuracy":0.0,"median_ms":0,"mastered":0,"skills":0,"readiness":0}
    recent=attempts[-50:]; acc=sum(1 for a in recent if a.get("correct"))/len(recent); med=_median(a.get("elapsed_ms",0) for a in recent)
    prof=profile_attempts(attempts); mastered=sum(1 for p in prof if p["state"]=="Mastered"); stable=sum(1 for p in prof if p["state"] in ("Stable","Mastered")); avg=sum(p["mastery"] for p in prof)/max(len(prof),1)
    readiness=round(100*(.48*acc+.38*avg+.14*(stable/max(len(prof),1))))
    return {"n":len(attempts),"accuracy":acc,"median_ms":med,"mastered":mastered,"skills":len(prof),"readiness":readiness}


def review_queue(attempts:list[dict],limit:int=12,now:float|None=None)->list[dict]:
    """Error notebook queue (attempt-level)."""
    now=float(now if now is not None else time.time()); latest={}; counts=defaultdict(int)
    for a in attempts:
        if a.get("error_type")!="clean_correct": latest[a.get("question_id","")]=a; counts[a.get("question_id","")]+=1
    rows=[]
    sev={"high_confidence_wrong":5,"wrong":4,"premature_guess":4,"unstable_reasoning":3.5,"skipped":3,"slow_correct":2,"hesitation":1.5}
    for qid,a in latest.items():
        age_h=max(0,(now-a.get("ts",now))/3600); due=sev.get(a.get("error_type"),1)+min(age_h/24,7)*.15+min(counts[qid],5)*.2
        rows.append({**a,"repeat_count":counts[qid],"due_score":due,"skill_label":skill_label(a.get("skill",""))})
    return sorted(rows,key=lambda x:(-x["due_score"],-x.get("ts",0)))[:limit]


def spaced_review_queue(attempts:list[dict],limit:int=12,now:float|None=None)->list[dict]:
    now=float(now if now is not None else time.time()); rows=[]
    for p in profile_attempts(attempts,now):
        if p["due_at"]<=now and p["state"]!="Mastered":
            rows.append({"skill":p["skill"],"label":p["label"],"state":p["state"],"review_stage":p["review_stage"],"due_at":p["due_at"],"overdue_days":p["overdue_days"],"priority":p["priority"]})
    return sorted(rows,key=lambda x:(-x["overdue_days"],-x["priority"]))[:limit]


def _reason(p):
    if p["high_confidence_wrong"]: return "Ada high-confidence wrong; misconception risk diprioritaskan."
    if p["accuracy"]<.70: return "Akurasi belum aman; pattern recognition dulu sebelum speed-up."
    if p["speed_ratio"]>1.15: return "Akurasi cukup, tetapi median waktu masih di atas target."
    if p["overdue_days"]>0: return "Spaced review sudah jatuh tempo."
    return "Belum melewati mastery gate secara stabil."


def daily_prescription(attempts:list[dict],max_minutes:int=20)->dict:
    prof=profile_attempts(attempts)
    if not prof:
        return {"minutes":15,"summary":"Belum ada baseline. Mulai diagnostic mixed untuk membangun peta kemampuan.","allocation":{"gap":0,"maintenance":0,"stretch":0},"items":[{"kind":"diagnostic","skill":"mixed","label":"Diagnostic Mixed","questions":15,"target_seconds":45,"minutes":15,"level":1,"role":"diagnostic"}]}
    due={x["skill"] for x in spaced_review_queue(attempts,limit=99)}
    gaps=sorted([p for p in prof if p["state"]!="Mastered"] or prof,key=lambda p:((p["skill"] not in due),-p["priority"]))
    strong=sorted([p for p in prof if p["state"] in ("Stable","Mastered")],key=lambda p:(-p["mastery"],p["speed_ratio"]))
    items=[];budget=max_minutes
    # Roughly 70% of useful work: current gaps and review-due material.
    for p in gaps[:2]:
        if budget<4:break
        qn=5;target=max(18,round(p["personal_target_ms"]/1000));mins=min(max(4,round(qn*target/60+1)),budget)
        items.append({"kind":"skill","skill":p["skill"],"label":p["label"],"questions":qn,"target_seconds":target,"minutes":mins,"reason":_reason(p),"level":p["recommended_level"],"review_due":p["skill"] in due,"role":"gap"})
        budget-=mins
    # ~20% maintenance: prove that a strength remains fast and retained.
    if strong and budget>=3:
        p=strong[0];qn=3;target=max(18,round(p["personal_target_ms"]/1000));mins=min(3,budget)
        items.append({"kind":"skill","skill":p["skill"],"label":"Maintenance · "+p["label"],"questions":qn,"target_seconds":target,"minutes":mins,"reason":"Jaga mastery dan speed tanpa over-practice.","level":max(2,p["recommended_level"]),"review_due":False,"role":"maintenance"});budget-=mins
    # Short mixed transfer block keeps breadth. Hard stretch is injected by final_core after baseline evidence.
    if budget>=3:
        items.append({"kind":"mixed","skill":"mixed","label":"Mixed Transfer","questions":5,"target_seconds":35,"minutes":min(4,budget),"reason":"Transfer skill ke kondisi campuran.","level":2,"role":"transfer"})
    total=sum(i["questions"] for i in items) or 1
    gap_q=sum(i["questions"] for i in items if i.get("role")=="gap")
    maint_q=sum(i["questions"] for i in items if i.get("role")=="maintenance")
    return {"minutes":sum(i["minutes"] for i in items),"summary":"Coach memprioritaskan gap/review, menjaga strength, lalu menguji transfer.","allocation":{"gap":gap_q/total,"maintenance":maint_q/total,"transfer":1-(gap_q+maint_q)/total},"items":items}


def session_postmortem(attempts:list[dict],session_id:str)->dict:
    rows=[a for a in attempts if a.get("session_id")==session_id]
    if not rows: return {"n":0,"session_id":session_id}
    correct=sum(1 for a in rows if a.get("correct")); med=_median(a.get("elapsed_ms",0) for a in rows)
    by=defaultdict(list)
    for a in rows: by[a.get("skill","unknown")].append(a)
    skills=[]
    for skill,rs in by.items():
        c=sum(1 for a in rs if a.get("correct")); m=_median(a.get("elapsed_ms",0) for a in rs); tgt=_median(a.get("target_ms",45_000) for a in rs)
        skills.append({"skill":skill,"label":skill_label(skill),"n":len(rs),"accuracy":c/len(rs),"median_ms":m,"target_ms":tgt,"excess_ms":max(0,m-tgt)})
    skills.sort(key=lambda x:(x["accuracy"],-x["excess_ms"]))
    errors=defaultdict(int)
    for a in rows:
        if a.get("error_type")!="clean_correct": errors[a.get("error_type","unknown")]+=1
    weakest=skills[0] if skills else None
    recommendation=(f"Next drill: {weakest['label']} — accuracy {round(weakest['accuracy']*100)}%, median {round(weakest['median_ms']/1000)}s." if weakest else "Lanjut mixed drill.")
    return {"session_id":session_id,"n":len(rows),"correct":correct,"accuracy":correct/len(rows),"median_ms":med,"errors":dict(errors),"skills":skills,"recommendation":recommendation}
