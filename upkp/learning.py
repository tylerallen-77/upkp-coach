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
        weights=[_recency_weight(float(r.get("ts",now)),now)*(1.0 if int(r.get("hint_level",0) or 0)==0 else 0.75 if int(r.get("hint_level",0) or 0)==1 else 0.45 if int(r.get("hint_level",0) or 0)==2 else 0.20) for r in rows]; wsum=sum(weights) or 1
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

ERROR_LABELS = {
    "high_confidence_wrong":"Miskonsepsi",
    "wrong":"Salah konsep / langkah",
    "premature_guess":"Terlalu cepat menebak",
    "unstable_reasoning":"Reasoning belum stabil",
    "skipped":"Dilewati",
    "slow_correct":"Benar tapi terlalu lambat",
    "hesitation":"Ragu-ragu",
    "clean_correct":"Benar & efisien",
}

def _teaching_action(p: dict, track: str) -> dict:
    """Convert learner evidence into a concrete teacher action."""
    skill=p.get("skill",""); ch=chapter_for_skill(skill)
    if p.get("high_confidence_wrong",0)>0:
        issue="Ada jawaban salah dengan confidence tinggi — tanda miskonsepsi, bukan sekadar kurang teliti."
        action="Pelajari ulang konsep inti, jelaskan kembali dengan kata sendiri, lalu mulai dari soal Standard sebelum naik level."
        mode="relearn"
    elif p.get("accuracy",0)<.68:
        issue="Akurasi belum stabil. Menambah kecepatan sekarang justru berisiko memperkuat pola salah."
        action="Fokus pada pola penyelesaian yang benar. Kerjakan perlahan sampai 3 jawaban bersih berturut-turut."
        mode="concept"
    elif track=="tpa" and p.get("speed_ratio",0)>1.15:
        issue="Konsep cukup dipahami, tetapi waktu penyelesaian masih di atas target."
        action="Jangan baca ulang semuanya. Fokus shortcut/cara cepat, lalu drill bertimer dengan metode yang sama."
        mode="speed"
    elif p.get("overdue_days",0)>0:
        issue="Skill ini sudah jatuh tempo untuk review. Kita perlu memastikan ingatan masih kuat."
        action="Coba recall tanpa catatan lebih dulu, lalu kerjakan beberapa soal transfer."
        mode="retention"
    else:
        issue="Skill sudah berkembang tetapi belum stabil di kondisi ujian."
        action="Naikkan sedikit difficulty dan uji pada soal campuran agar kemampuan tidak bergantung pada template."
        mode="transfer"
    return {"skill":skill,"label":p.get("label",skill),"chapter":ch,"issue":issue,"action":action,
            "mode":mode,"state":p.get("state"),"accuracy":p.get("accuracy",0),
            "median_ms":p.get("median_ms",0),"target_ms":p.get("personal_target_ms",p.get("target_median_ms",45000)),
            "level":p.get("recommended_level",1)}

def teacher_plan(attempts:list[dict], track:str)->dict:
    prof=profile_attempts(attempts)
    errors=defaultdict(int)
    for a in attempts[-40:]:
        errors[a.get("error_type","unknown")]+=1
    error_mix=[{"type":k,"label":ERROR_LABELS.get(k,k),"count":v} for k,v in sorted(errors.items(),key=lambda x:-x[1]) if k!="clean_correct" and v]
    if not prof:
        return {
            "phase":"diagnose",
            "headline":"Saya belum cukup mengenal pola kemampuanmu.",
            "message":"Kita mulai dengan diagnostic mixed. Jangan mengejar skor; saya ingin melihat cara kamu salah, bagian yang lambat, dan level yang masih nyaman.",
            "focus":None,"priorities":[],"error_mix":[],
            "success_criteria":"Selesaikan diagnostic dengan confidence yang jujur. Setelah itu saya akan memilih apa yang perlu dipelajari dan apa yang cukup dilatih.",
        }
    gaps=[p for p in prof if p.get("state")!="Mastered"]
    ranked=sorted(gaps or prof,key=lambda p:-p.get("priority",0))
    priorities=[_teaching_action(p,track) for p in ranked[:3]]
    focus=priorities[0] if priorities else None
    if focus:
        headline=f"Fokus utama sekarang: {focus['label']}."
        message=focus["issue"]+" "+focus["action"]
    else:
        headline="Fondasi sudah kuat."
        message="Sekarang tugas kita menjaga retention dan memindahkan kemampuan ke kondisi campuran/ujian."
    if track=="tpa":
        criteria="Saya anggap sesi efektif bila akurasi stabil, median mendekati target, dan kesalahan yang sama tidak berulang."
    else:
        criteria="Saya anggap sesi efektif bila fakta/konsep bisa diingat tanpa melihat catatan, akurasi stabil, dan tetap benar saat pertanyaan diubah konteksnya."
    return {"phase":"teach","headline":headline,"message":message,"focus":focus,"priorities":priorities,
            "error_mix":error_mix[:4],"success_criteria":criteria}

def chapter_coaching(attempts:list[dict], code:str, track:str)->dict:
    rows=[a for a in attempts if a.get("bab")==code and not a.get("skipped")]
    if not rows:
        return {"n":0,"accuracy":0,"median_ms":0,"status":"unseen",
                "teacher_note":"Belum ada evidence. Baca konsep inti secukupnya, lalu langsung cek pemahaman dengan 5 soal pemanasan.",
                "recommended":"warmup"}
    recent=rows[-20:];acc=sum(bool(a.get("correct")) for a in recent)/len(recent);med=_median(a.get("elapsed_ms",0) for a in recent)
    wrong=sum(1 for a in recent if not a.get("correct"));hc=sum(1 for a in recent if a.get("error_type")=="high_confidence_wrong")
    tgt=_median(a.get("target_ms",45000) for a in recent) or 45000
    if hc:
        note="Ada miskonsepsi terdeteksi. Jangan langsung menambah volume soal; baca ulang konsep dan cocokkan dengan penjelasan dari jawaban yang salah."
        rec="relearn"
    elif acc<.7:
        note="Akurasi menunjukkan konsep belum stabil. Prioritaskan memahami langkah/pola sebelum latihan bertimer."
        rec="concept"
    elif track=="tpa" and med>tgt*1.15:
        note="Akurasi sudah cukup, tetapi masih lambat. Fokus bagian 'Cara cepat' lalu lakukan drill bertimer."
        rec="speed"
    elif wrong:
        note="Dasar cukup baik. Gunakan materi hanya untuk menutup celah spesifik, lalu uji lagi dengan soal transfer."
        rec="transfer"
    else:
        note="Evidence terakhir bersih. Tidak perlu reread panjang; lakukan recall singkat lalu naik ke drill yang lebih menantang."
        rec="challenge"
    return {"n":len(rows),"accuracy":acc,"median_ms":med,"target_ms":tgt,"status":"practiced",
            "teacher_note":note,"recommended":rec,"high_confidence_wrong":hc}

def enrich_postmortem(pm:dict)->dict:
    """Teacher-language interpretation of one completed session."""
    if not pm or not pm.get("n"): return pm
    acc=float(pm.get("accuracy",0)); errors=pm.get("errors") or {}
    if errors.get("high_confidence_wrong",0):
        diagnosis="Ada miskonsepsi: setidaknya satu jawaban salah diberikan dengan confidence tinggi."
        next_action="Buka materi skill terlemah, pahami alasan jawaban benar, lalu ulangi drill pendek sebelum mixed practice."
    elif acc<.6:
        diagnosis="Konsep belum cukup stabil untuk dikejar dengan speed."
        next_action="Turunkan beban: pelajari pola inti, kerjakan 5 soal tanpa tekanan waktu, baru ulangi sesi."
    elif errors.get("premature_guess",0):
        diagnosis="Sebagian kehilangan poin berasal dari keputusan terlalu cepat, bukan semata-mata kurang pengetahuan."
        next_action="Gunakan checkpoint singkat sebelum memilih: apa yang ditanya, syarat kunci, lalu eliminasi opsi."
    elif errors.get("slow_correct",0):
        diagnosis="Akurasi cukup, tetapi metode masih terlalu mahal secara waktu."
        next_action="Bandingkan solusi dengan shortcut/cara cepat, lalu ulangi tipe yang sama dengan target waktu."
    elif acc>=.85:
        diagnosis="Pemahaman sesi ini sudah kuat."
        next_action="Jangan over-practice topik yang sama. Pindahkan kemampuan ke mixed transfer atau level lebih tinggi."
    else:
        diagnosis="Dasar sudah terbentuk, tetapi konsistensi masih perlu diperkuat."
        next_action="Review hanya kesalahan yang terjadi, lalu ulangi targeted drill singkat."
    pm["teacher_diagnosis"]=diagnosis
    pm["teacher_next_action"]=next_action
    pm["clean_correct"]=pm.get("n",0)-sum(int(v) for k,v in errors.items() if k!="clean_correct")
    return pm


def attempt_coach_note(a:dict)->dict:
    e=a.get("error_type")
    notes={
        "clean_correct":("Bagus. Metodenya sudah benar dan efisien.","Jangan overthink; lanjutkan."),
        "slow_correct":("Benar, tetapi waktunya terlalu mahal.","Bandingkan dengan shortcut/cara cepat dan cari langkah yang bisa dipangkas."),
        "hesitation":("Jawaban benar, tapi reasoning belum mantap.","Sebelum lanjut, sebutkan satu alasan kenapa pilihan ini benar."),
        "high_confidence_wrong":("Ini miskonsepsi, bukan sekadar miss.","Jangan hafal kunci. Baca penjelasan sampai tahu aturan mana yang tadi keliru."),
        "premature_guess":("Kamu memutuskan terlalu cepat.","Ulangi proses: identifikasi yang ditanya → syarat kunci → eliminasi."),
        "unstable_reasoning":("Perubahan jawaban menunjukkan reasoning belum stabil.","Tulis/ingat aturan utama dulu sebelum memilih opsi."),
        "wrong":("Jawaban belum tepat.","Cari langkah pertama yang salah, bukan hanya melihat jawaban akhir."),
        "skipped":("Soal dilewati.","Pastikan ini keputusan strategi, bukan karena konsepnya belum dikenali."),
    }
    title,action=notes.get(e,("Catat pola jawabanmu.","Gunakan feedback ini untuk percobaan berikutnya."))
    return {"title":title,"action":action,"error_type":e}

