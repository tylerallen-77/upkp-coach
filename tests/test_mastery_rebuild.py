
import time
from upkp import mastery
from upkp.final_core import build_mastery_challenge

def a(skill, correct=True, level=3, day=0, elapsed=25000, target=40000, sid="s"):
    return {"skill":skill,"correct":correct,"level":level,"ts":time.time()+day*86400,
            "elapsed_ms":elapsed,"target_ms":target,"skipped":False,"session_id":sid}

def test_badge_not_farmable_with_easy_questions():
    rows=[]
    for sk in mastery.BADGE_SKILLS["verbal"]:
        rows += [a(sk,True,1,i) for i in range(10)]
    b=mastery.section_badge(rows,"verbal",[])
    assert not b["earned"]
    assert not b["challenge_unlocked"]

def test_challenge_contains_exam_or_hard():
    qs=build_mastery_challenge("numerical",seed=7)
    assert len(qs)==15
    assert all(int(q["lv"])>=3 for q in qs)
    assert any(int(q["lv"])>=4 for q in qs)

def test_mastery_challenge_gate():
    rows=[]
    for sk in mastery.BADGE_SKILLS["logical"]:
        rows += [a(sk,True,3,i%2,sid="challenge") for i in range(4)]
    v=mastery.evaluate_mastery_challenge("logical",rows,"challenge")
    assert v["mastery_passed"] is True
