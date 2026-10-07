
import os, tempfile

def test_partial_close_records_abandoned():
    os.environ["UPKP_LOCAL_DB"]=tempfile.mktemp(suffix=".sqlite3")
    os.environ["COOKIE_SECURE"]="0"
    from fastapi.testclient import TestClient
    import importlib, api.index as mod
    c=TestClient(mod.app)
    r=c.post("/api/auth/register",json={"username":"partialux","password":"password123","accept_terms":True})
    assert r.status_code==200
    d=c.post("/api/session/guided?track=tpa").json()
    sid=d["session"]["id"]
    q=d["questions"][0]
    a=c.post("/api/attempt",json={
        "question_token":q["token"],"selected":0,"elapsed_ms":12000,
        "first_selection_ms":8000,"answer_changes":0,"confidence":"50:50",
        "skipped":False,"pass_number":1,"session_id":sid
    })
    assert a.status_code==200
    x=c.post("/api/session/close",json={"session_id":sid,"abandoned":True})
    assert x.status_code==200
    pm=x.json()["postmortem"]
    assert pm["abandoned"] is True and pm["n"]==1
    h=c.get("/api/home").json()
    assert any(s["id"]==sid and s["summary"].get("abandoned") for s in h["sessions"])
