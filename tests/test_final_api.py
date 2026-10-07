import os, tempfile, importlib, sys
from pathlib import Path

os.environ['UPKP_LOCAL_DB']=str(Path(tempfile.gettempdir())/'upkp-final-test.sqlite3')
os.environ['COOKIE_SECURE']='0'
os.environ.pop('DATABASE_URL',None)
try: Path(os.environ['UPKP_LOCAL_DB']).unlink()
except FileNotFoundError: pass
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
mod=importlib.import_module('api.index')
client=TestClient(mod.app)

def test_register_home_and_both_tracks():
    r=client.post('/api/auth/register',json={'username':'rio_test','password':'password123'})
    assert r.status_code==200,r.text
    assert client.get('/api/auth/me').status_code==200
    h=client.get('/api/home'); assert h.status_code==200
    assert {x['track'] for x in h.json()['tracks']}=={'tpa','substansi'}

def test_substance_catalog_and_guided():
    c=client.get('/api/catalog?track=substansi').json()['chapters']
    assert len(c)==6
    assert any(x['code']=='keuangan' for x in c)
    s=client.post('/api/session/guided?track=substansi')
    assert s.status_code==200,s.text
    q=s.json()['questions']; assert q
    assert all('ans' not in x and 'exp' not in x for x in q)

def test_tpa_question_and_attempt():
    s=client.post('/api/session/chapter?code=operasi&n=5&level=1').json()
    q=s['questions'][0]
    r=client.post('/api/attempt',json={'question_token':q['token'],'selected':0,'elapsed_ms':1000,'session_id':s['session']['id']})
    assert r.status_code==200,r.text
    assert 'answer' in r.json()

def test_tryout_hides_feedback():
    s=client.post('/api/session/tryout?track=tpa').json();q=s['questions'][0]
    r=client.post('/api/attempt',json={'question_token':q['token'],'selected':0,'elapsed_ms':1000,'session_id':s['session']['id'],'pass_number':1})
    assert r.status_code==200
    assert r.json().get('deferred_feedback') is True
    assert 'answer' not in r.json()

def test_two_user_isolation():
    # current client is rio_test and has attempts
    before=client.get('/api/progress?track=tpa').json()['snapshot']['metrics']['n']
    assert before>=1
    c2=TestClient(mod.app)
    r=c2.post('/api/auth/register',json={'username':'friend_1','password':'password123'})
    assert r.status_code==200,r.text
    other=c2.get('/api/progress?track=tpa').json()['snapshot']['metrics']['n']
    assert other==0

def test_figural_payload_keeps_svg_but_not_answer():
    # chapter endpoint must carry figure payloads to React renderer.
    s=client.post('/api/session/chapter?code=deretfig&n=5&level=1').json()
    assert any(q.get('svg') or q.get('opt_svgs') for q in s['questions'])
    assert all('ans' not in q for q in s['questions'])
