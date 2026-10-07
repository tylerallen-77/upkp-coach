import os, time
from fastapi.testclient import TestClient
from api import index as mod
from upkp import multi_store as store
from upkp.exam_engine import structural_signature


def _register(name, ip):
    c=TestClient(mod.app)
    r=c.post('/api/auth/register',json={'username':name,'password':'password123','accept_terms':True},headers={'x-forwarded-for':ip})
    assert r.status_code==200,r.text
    return c,r.json()['user']


def test_cross_site_mutation_blocked():
    c=TestClient(mod.app)
    r=c.post('/api/auth/register',json={'username':'evil_try','password':'password123'},headers={'Origin':'https://evil.example','Host':'testserver','x-forwarded-for':'10.0.0.10'})
    assert r.status_code==403


def test_admin_username_is_reserved(monkeypatch):
    monkeypatch.setenv('ADMIN_USERNAME','rio_admin_reserved')
    c=TestClient(mod.app)
    r=c.post('/api/auth/register',json={'username':'rio_admin_reserved','password':'password123'},headers={'x-forwarded-for':'10.0.0.11'})
    assert r.status_code==409


def test_terms_gate_can_be_required(monkeypatch):
    monkeypatch.setenv('REQUIRE_TERMS','1')
    c=TestClient(mod.app)
    r=c.post('/api/auth/register',json={'username':'terms_test','password':'password123','accept_terms':False},headers={'x-forwarded-for':'10.0.0.12'})
    assert r.status_code==422


def test_reports_auto_quarantine_after_three_independent_users():
    q={'id':'public-hardening-q','bab':'operasi','lv':3,'stem':'17 × 6 = ?','opts':['100','102','104','106','108'],'ans':1,'exp':'17×6=102','trick':'10×6 + 7×6','waktu':30,'skill':'numerik.operasi_bilangan','archetype':'qa_report_fixture','track':'tpa'}
    sig=structural_signature(q)
    for i in range(3):
        c,u=_register(f'reporter_{i}',f'10.0.1.{i+1}')
        sess=store.new_learning_session(u['id'],'tpa','chapter','QA report fixture',{})
        token=store.stash_question(u['id'],sess['id'],q)
        a=c.post('/api/attempt',json={'question_token':token,'selected':1,'elapsed_ms':12000,'session_id':sess['id']})
        assert a.status_code==200,a.text
        rr=c.post('/api/report-question',json={'item_signature':sig,'question_id':q['id'],'reason':'ambiguous','detail':'QA fixture'})
        assert rr.status_code==200,rr.text
    assert store.is_quarantined(sig) is True


def test_population_calibration_updates():
    rows=store.population_stats(500)
    fixture=[x for x in rows if x['skill']=='numerik.operasi_bilangan']
    assert fixture
    assert max(x['attempts'] for x in fixture)>=3
    assert all(1 <= x['empirical_level'] <= 5 for x in fixture)


def test_health_checks_real_database():
    c=TestClient(mod.app)
    r=c.get('/api/health')
    assert r.status_code==200
    assert r.json()['ok'] is True


def test_self_delete_revokes_account_and_session():
    c,u=_register('delete_me','10.0.2.1')
    bad=c.post('/api/account/delete',json={'password':'wrongpass'})
    assert bad.status_code==401
    ok=c.post('/api/account/delete',json={'password':'password123'})
    assert ok.status_code==200
    assert c.get('/api/auth/me').status_code==401
