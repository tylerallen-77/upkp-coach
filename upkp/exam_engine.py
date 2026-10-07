"""UPKP Coach V2.2 exam-intelligence layer.

Adds speed/ROI analysis, skip-or-solve recommendations, three-pass tryout
planning, structural item calibration, and exam post-mortems.
"""
from __future__ import annotations
from collections import defaultdict
import hashlib, re, statistics

BAD_ERRORS={"wrong","high_confidence_wrong","premature_guess","unstable_reasoning","skipped"}


def _median(xs):
    xs=list(xs); return statistics.median(xs) if xs else 0.0


def structural_signature(q:dict)->str:
    """Stable-ish template fingerprint for parametrically generated questions."""
    stem=str(q.get("stem","")).lower()
    stem=re.sub(r"\d+(?:[.,]\d+)*","#",stem)
    stem=re.sub(r"\s+"," ",stem).strip()
    raw="|".join([str(q.get("bab","")),str(q.get("skill","")),str(q.get("lv",1)),str(q.get("archetype") or stem)])
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def points_per_minute(correct:bool, elapsed_ms:int)->float:
    if not correct or elapsed_ms<=0:return 0.0
    return 60000.0/elapsed_ms


def skip_signal(profile:dict|None, question:dict, elapsed_ms:int=0)->dict:
    """Decision support, not an answer hint. Uses expected time/accuracy only."""
    target=int((profile or {}).get("personal_target_ms") or int(question.get("waktu",45))*1000)
    acc=float((profile or {}).get("accuracy",.75))
    lv=int(question.get("lv",1))
    cost_factor=1 + max(0,lv-1)*.18
    hard_stop=int(target*cost_factor*1.18)
    expected_ppm=(acc*60000)/max(target*cost_factor,1)
    if elapsed_ms and elapsed_ms>=hard_stop:
        decision="skip_to_next_pass"
        reason=f"Elapsed sudah melewati hard stop {round(hard_stop/1000)}s. Lindungi points/minute."
    elif acc<.62 and lv>=2:
        decision="consider_skip"
        reason="Historical accuracy rendah untuk kombinasi skill/difficulty ini."
    else:
        decision="solve"
        reason="Expected points/minute masih layak untuk pass ini."
    return {"decision":decision,"hard_stop_ms":hard_stop,"expected_ppm":expected_ppm,"reason":reason}


def calibrate_items(attempts:list[dict])->list[dict]:
    groups=defaultdict(list)
    for a in attempts:
        sig=a.get("item_signature")
        if sig:groups[sig].append(a)
    out=[]
    for sig,rows in groups.items():
        n=len(rows); acc=sum(bool(r.get("correct")) for r in rows)/n
        med=_median(r.get("elapsed_ms",0) for r in rows)
        target=_median(r.get("target_ms",45000) for r in rows) or 45000
        # Personal empirical difficulty; Bayesian shrink toward 0.5 prevents tiny-n extremes.
        shrunk_correct=(sum(bool(r.get("correct")) for r in rows)+2)/(n+4)
        difficulty=1-shrunk_correct
        time_pressure=med/target if target else 1
        out.append({"signature":sig,"n":n,"accuracy":acc,"difficulty":difficulty,"median_ms":med,"time_pressure":time_pressure,
                    "skill":rows[-1].get("skill",""),"level":rows[-1].get("level",1)})
    return sorted(out,key=lambda x:(-x["difficulty"],-x["time_pressure"]))


def speed_profile(attempts:list[dict])->dict:
    if not attempts:return {"n":0,"ppm":0,"wasted_ms":0,"overcheck_ms":0,"skip_efficiency":0}
    ppm=sum(points_per_minute(bool(a.get("correct")),int(a.get("elapsed_ms",0))) for a in attempts)/len(attempts)
    wasted=sum(max(0,int(a.get("elapsed_ms",0))-int(a.get("target_ms",0))) for a in attempts)
    overcheck=sum(max(0,int(a.get("elapsed_ms",0))-int(a.get("first_selection_ms") or a.get("elapsed_ms",0))) for a in attempts if a.get("correct"))
    skips=[a for a in attempts if a.get("skipped")]
    # skips in pass 1 are considered strategic when later answered correctly in same session/question.
    later={(a.get("session_id"),a.get("question_id")):a for a in attempts if a.get("correct") and int(a.get("pass_number",1))>1}
    strategic=sum(1 for a in skips if (a.get("session_id"),a.get("question_id")) in later)
    return {"n":len(attempts),"ppm":ppm,"wasted_ms":wasted,"overcheck_ms":overcheck,"skip_efficiency": strategic/len(skips) if skips else None}


def exam_postmortem(attempts:list[dict],session_id:str)->dict:
    rows=[a for a in attempts if a.get("session_id")==session_id]
    if not rows:return {"n":0,"session_id":session_id}
    unique={}
    for a in rows: # last attempt per question is final exam outcome
        unique[a.get("question_id")]=a
    finals=list(unique.values()); correct=sum(bool(a.get("correct")) for a in finals)
    total_ms=sum(int(a.get("elapsed_ms",0)) for a in rows)
    by_pass=defaultdict(list)
    for a in rows:by_pass[int(a.get("pass_number",1))].append(a)
    passes=[]
    for p,rs in sorted(by_pass.items()):
        passes.append({"pass":p,"attempts":len(rs),"correct":sum(bool(x.get("correct")) for x in rs),"time_ms":sum(int(x.get("elapsed_ms",0)) for x in rs),"skipped":sum(bool(x.get("skipped")) for x in rs)})
    speed=speed_profile(rows)
    expensive=sorted(rows,key=lambda a:(int(a.get("elapsed_ms",0))*(0 if a.get("correct") else 1.4)),reverse=True)[:5]
    return {"session_id":session_id,"n":len(finals),"correct":correct,"accuracy":correct/max(len(finals),1),"total_ms":total_ms,
            "points_per_minute":correct/(total_ms/60000) if total_ms else 0,"passes":passes,"speed":speed,
            "expensive_errors":[{"skill":a.get("skill"),"elapsed_ms":a.get("elapsed_ms"),"error_type":a.get("error_type"),"pass_number":a.get("pass_number")} for a in expensive if not a.get("correct")],
            "recommendation":_exam_recommendation(rows,speed)}


def _exam_recommendation(rows,speed):
    wrong=[a for a in rows if not a.get("correct") and not a.get("skipped")]
    p1_skips=[a for a in rows if a.get("skipped") and int(a.get("pass_number",1))==1]
    if speed.get("overcheck_ms",0)>60000:
        return "Prioritas: kurangi over-checking. Commit jawaban lebih cepat pada soal yang sudah terpecahkan."
    if wrong and _median(a.get("elapsed_ms",0) for a in wrong)>_median(a.get("target_ms",45000) for a in wrong)*1.2:
        return "Prioritas: hard-stop discipline. Soal salah juga menyerap waktu berlebih; parkir lebih cepat ke pass berikutnya."
    if not p1_skips:
        return "Prioritas: latih deliberate skipping di Pass 1 agar cheap points selesai lebih dulu."
    return "Strategi pass sudah sehat. Fokus berikutnya pada micro-skill dengan expected points/minute terendah."
