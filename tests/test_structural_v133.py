import os, tempfile, time

def _substansi_attempt(skill, correct=True, level=3, day=0, session_id='s'):
    return {
        'skill':skill,'correct':correct,'skipped':False,'level':level,
        'elapsed_ms':20000,'target_ms':45000,'ts':time.time()+day*86400,
        'session_id':session_id,'track':'substansi'
    }

def test_substansi_mastery_has_six_domains_and_knowledge_gate():
    from upkp import mastery
    skills=[
        ('substansi_etika','substansi.etika'),
        ('substansi_wawasan','substansi.wawasan'),
        ('substansi_nilai','substansi.nilai_kemenkeu'),
        ('substansi_kepegawaian','substansi.kepegawaian'),
        ('substansi_keuangan','substansi.keuangan_negara'),
        ('substansi_struktur','substansi.struktur_kemenkeu'),
    ]
    attempts=[]
    sessions=[]
    for section,skill in skills:
        for i in range(10):
            attempts.append(_substansi_attempt(skill,True,3,0 if i<5 else 2))
        sessions.append({'track':'substansi','kind':'mastery','meta':{'section':section},'summary':{'mastery_passed':True}})
    status=mastery.substansi_badges(attempts,sessions)
    assert status['total']==6
    assert status['earned']==6
    assert status['substansi_ready'] is True

def test_reset_learning_history_keeps_account():
    db=tempfile.mktemp(suffix='.sqlite3')
    os.environ['UPKP_LOCAL_DB']=db
    from upkp import multi_store as store
    u=store.create_user('resetcase','hash','user')
    sess=store.new_learning_session(u['id'],'tpa','guided','x',{})
    q={'id':'q1','bab':'operasi','skill':'numerik.operasi_bilangan','track':'tpa','ans':0}
    token=store.stash_question(u['id'],sess['id'],q)
    attempt={'ts':time.time(),'session_id':sess['id'],'question_id':'q1','track':'tpa','skill':'numerik.operasi_bilangan','item_signature':'sig','correct':True}
    assert store.record_attempt_atomic(u['id'],attempt,token,True,'k1')=='recorded'
    store.reset_learning_history(u['id'])
    assert store.get_user_by_username('resetcase') is not None
    assert store.attempts(u['id'])==[]
    assert store.active_sessions(u['id'])==[]
    assert store.recent_sessions(u['id'])==[]
