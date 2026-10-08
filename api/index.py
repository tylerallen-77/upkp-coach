from __future__ import annotations
import os, re, time
from urllib.parse import urlparse
from fastapi import FastAPI, HTTPException, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from upkp import curriculum, materi, learning, engine, material_meta, course_materials, official_sources, lesson_cards, study_tools, regulation_deepdives
from upkp import final_core as core
from upkp import multi_store as store
from upkp import mastery
from upkp import tpa_enrichment
from upkp.exam_engine import structural_signature

app=FastAPI(title='UPKP Coach Final API',version='1.7.0',docs_url=None if os.getenv('VERCEL')=='1' else '/docs',redoc_url=None)
app.add_middleware(CORSMiddleware,allow_origins=[],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

class SameOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        if request.method not in ('GET','HEAD','OPTIONS'):
            origin=request.headers.get('origin')
            host=request.headers.get('host','')
            fetch_site=(request.headers.get('sec-fetch-site') or '').lower()
            if fetch_site=='cross-site':
                return JSONResponse({'error':'Cross-site mutation blocked'},status_code=403)
            if origin and host:
                origin_host=urlparse(origin).netloc
                if origin_host and origin_host!=host:
                    return JSONResponse({'error':'Cross-origin mutation blocked'},status_code=403)
        response=await call_next(request)
        response.headers['Cache-Control']='no-store' if request.url.path.startswith('/api/') else response.headers.get('Cache-Control','')
        return response
app.add_middleware(SameOriginMiddleware)
ph=PasswordHasher(time_cost=2,memory_cost=19456,parallelism=1)
COOKIE='upkp_session'
USERNAME_RE=re.compile(r'^[a-z0-9_]{3,24}$')
TRACKS={'tpa':'Tes Potensi','substansi':'TSKKWK'}
DIFFICULTY={1:'Foundation',2:'Standard',3:'Exam',4:'Hard',5:'Expert'}

class AuthIn(BaseModel):
    username:str=Field(min_length=3,max_length=24)
    password:str=Field(min_length=8,max_length=128)
    accept_terms:bool=False
class AttemptIn(BaseModel):
    question_token:str; selected:int|None=None; elapsed_ms:int=Field(ge=0,le=300000)
    first_selection_ms:int|None=Field(default=None,ge=0,le=300000); answer_changes:int=Field(default=0,ge=0,le=50)
    confidence:str=''; skipped:bool=False; pass_number:int=Field(default=1,ge=1,le=3); session_id:str; hint_level:int=Field(default=0,ge=0,le=3)
class CloseIn(BaseModel):
    session_id:str
    abandoned:bool=False
class AdminReset(BaseModel): password:str=Field(min_length=8,max_length=128)
class DeleteAccountIn(BaseModel): password:str=Field(min_length=8,max_length=128)
class ResetLearningIn(BaseModel): password:str=Field(min_length=8,max_length=128)
class ReportIn(BaseModel):
    item_signature:str=Field(min_length=8,max_length=64)
    question_id:str=Field(min_length=1,max_length=128)
    reason:str=Field(min_length=2,max_length=64)
    detail:str=Field(default='',max_length=500)


def current_user(req:Request):
    u=store.user_from_session(req.cookies.get(COOKIE,''))
    if not u: raise HTTPException(401,'Login required')
    return u

def admin_user(u=Depends(current_user)):
    if u.get('role')!='admin':raise HTTPException(403,'Admin only')
    return u

def throttle(uid:str,bucket:str,limit:int,window:int):
    if store.hit_rate_limit(f'user:{uid}:{bucket}',limit,window):
        raise HTTPException(429,'Terlalu banyak aktivitas. Coba lagi sebentar.')

def set_cookie(resp:Response,token:str):
    secure=os.getenv('VERCEL')=='1' or os.getenv('COOKIE_SECURE','1')=='1'
    resp.set_cookie(COOKIE,token,max_age=30*86400,httponly=True,secure=secure,samesite='lax',path='/')

@app.get('/api/health')
def health():
    ok=store.db_health()
    return JSONResponse({'ok':ok,'version':'1.7.0','database':'postgres' if store.DATABASE_URL else 'sqlite-local'},status_code=200 if ok else 503)

@app.post('/api/auth/register')
def register(body:AuthIn,response:Response,request:Request):
    username=body.username.strip().lower()
    ip=(request.headers.get('x-forwarded-for') or (request.client.host if request.client else 'unknown')).split(',')[0].strip()
    if store.hit_rate_limit('register:'+ip,6,600): raise HTTPException(429,'Terlalu banyak percobaan. Coba lagi nanti.')
    if os.getenv('REQUIRE_TERMS','0')=='1' and not body.accept_terms:raise HTTPException(422,'Persetujuan Ketentuan & Privasi diperlukan')
    if not USERNAME_RE.fullmatch(username):raise HTTPException(422,'Username: 3–24 karakter, hanya a-z, 0-9, underscore')
    reserved=os.getenv('ADMIN_USERNAME','').strip().lower()
    if reserved and username==reserved:raise HTTPException(409,'Username ini direservasi untuk administrator')
    if store.get_user_by_username(username):raise HTTPException(409,'Username sudah dipakai')
    try:u=store.create_user(username,ph.hash(body.password),'user')
    except Exception:raise HTTPException(409,'Username sudah dipakai')
    token=store.create_auth_session(u['id']);set_cookie(response,token)
    return {'user':u}

@app.post('/api/auth/login')
def login(body:AuthIn,response:Response,request:Request):
    ip=(request.headers.get('x-forwarded-for') or (request.client.host if request.client else 'unknown')).split(',')[0].strip()
    bucket='login:'+ip+':'+body.username.strip().lower()
    if store.hit_rate_limit(bucket,10,300): raise HTTPException(429,'Terlalu banyak percobaan login. Coba lagi nanti.')
    u=store.get_user_by_username(body.username.strip().lower())
    if not u or u.get('disabled'):raise HTTPException(401,'Username atau password salah')
    try:ph.verify(u['password_hash'],body.password)
    except VerifyMismatchError:raise HTTPException(401,'Username atau password salah')
    token=store.create_auth_session(u['id']);set_cookie(response,token)
    return {'user':{'id':u['id'],'username':u['username'],'role':u['role']}}

@app.post('/api/auth/logout')
def logout(req:Request,response:Response):
    store.delete_auth_session(req.cookies.get(COOKIE,''));response.delete_cookie(COOKIE,path='/');return {'ok':True}

@app.get('/api/auth/me')
def me(u=Depends(current_user)):return {'user':u}


def track_attempts(uid,track):return store.attempts(uid,track)
def public_q(q):
    item={k:v for k,v in q.items() if k not in ('ans','exp','trick','_exam_mode','_session_id')}
    lv=int(item.get('lv',1));item['difficulty_label']=DIFFICULTY.get(lv,'Standard')
    item['item_signature']=structural_signature(q)
    item['hints']=[x for x in study_tools.hints(str(q.get('bab',''))) if x]
    return item
def prep_questions(uid,sid,qs):
    # Batch quarantine lookup + token insert: one read and one write transaction for the whole session.
    pairs=[(q,structural_signature(q)) for q in qs]
    blocked=store.quarantined_signatures([sig for _,sig in pairs])
    allowed=[q for q,sig in pairs if sig not in blocked]
    if not allowed: raise HTTPException(503,'Konten sesi sedang ditinjau. Coba sesi lain.')
    tokens=store.stash_questions(uid,sid,allowed)
    out=[]
    for q,token in zip(allowed,tokens):
        item=public_q(q);item['token']=token;out.append(item)
    return out

def track_snapshot(uid,track):
    a=track_attempts(uid,track);m=learning.overall_metrics(a);p=learning.profile_attempts(a);rx=learning.daily_prescription(a,max_minutes=18)
    out={'track':track,'label':TRACKS[track],'metrics':m,'skills':p[:8],'prescription':rx,'review':learning.review_queue(a,6),'review_due':learning.spaced_review_queue(a,6),'teacher':learning.teacher_plan(a,track)}
    sessions=store.recent_sessions(uid,100)
    if track=='tpa':
        out['mastery']=mastery.tpa_badges(a,sessions)
    elif track=='substansi':
        out['mastery']=mastery.substansi_badges(a,sessions)
    return out

@app.get('/api/home')
def home(u=Depends(current_user)):
    return {
        'user':u,
        'tracks':[track_snapshot(u['id'],'tpa'),track_snapshot(u['id'],'substansi')],
        'sessions':store.recent_sessions(u['id'],6),
        'active_sessions':store.active_sessions(u['id'],5),
    }

@app.get('/api/progress')
def progress(track:str='tpa',u=Depends(current_user)):
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    a=track_attempts(u['id'],track)
    return {'snapshot':track_snapshot(u['id'],track),'skills':learning.profile_attempts(a),'sessions':[s for s in store.recent_sessions(u['id'],30) if s['track']==track]}

@app.get('/api/coach')
def coach(track:str='tpa',u=Depends(current_user)):
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    a=track_attempts(u['id'],track)
    return {'track':track,'teacher':learning.teacher_plan(a,track),'prescription':learning.daily_prescription(a,max_minutes=18)}


@app.get('/api/catalog')
def catalog(track:str='tpa',u=Depends(current_user)):
    bagian='Tes Potensi' if track=='tpa' else 'TSKKWK'
    chapters=[]
    for b in curriculum.BAB:
        if b.bagian!=bagian:continue
        source_note='Konsep, strategi, dan pola latihan Tes Potensi' if track=='tpa' else 'Materi TSKKWK divalidasi terhadap sumber resmi/current; enam domain adalah struktur belajar internal.'
        extra=tpa_enrichment.ENRICHMENT.get(b.kode,'') if track=='tpa' else ''
        material=materi.MATERI.get(b.kode,'')
        if extra: material=(material+'\n\n'+extra).strip()
        material=course_materials.expand(b.kode,material)
        deep=regulation_deepdives.get(b.kode) if track=='substansi' else ''
        if deep: material=(material+'\n\n'+deep).strip()
        meta=material_meta.metadata(b.kode,b.sumber)
        chapter_stats=learning.chapter_coaching(track_attempts(u['id'],track),b.kode,track)
        headings=[ln[4:].strip() for ln in material.splitlines() if ln.strip().startswith('### ')][:6]
        objectives=[f"Jelaskan dan terapkan {h.lower()}" for h in headings[:4]]
        checks=[f"Tanpa melihat catatan, bisakah kamu menjelaskan {h.lower()} dan memberi satu contoh?" for h in headings[:4]]
        source_refs=tpa_enrichment.SOURCES if track=='tpa' else official_sources.TSKKWK_SOURCES.get(b.kode,[])
        chapters.append({'code':b.kode,'title':b.judul,'subtest':b.subtes,'source_type':b.sumber,'source_note':source_note,'material':material,
                         'source_refs':source_refs,
                         'source_status':meta.get('status'),'source_status_label':meta.get('status_label'),
                         'verified_at':meta.get('verified'),'freshness_note':meta.get('note'),'page':b.halaman if track=='tpa' else '',
                         'learner':chapter_stats,'objectives':objectives,'self_checks':checks,
                         'official_scope_note':official_sources.VALIDATION.get('tskkwk_scope') if track=='substansi' else '',
                         'lesson_cards':lesson_cards.cards(b.kode),
                         'reading_lens':study_tools.reading_lens(b.kode),
                         'formulas':study_tools.formulas(b.kode),
                         'mnemonics':study_tools.mnemonics(b.kode)})
    return {'track':track,'chapters':chapters}

@app.post('/api/session/guided')
def guided(track:str='tpa',u=Depends(current_user)):
    throttle(u['id'],'session',30,3600)
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    a=track_attempts(u['id'],track);rx,qs=core.build_prescription(track,a,max_minutes=18)
    s=store.new_learning_session(u['id'],track,'guided',f"{TRACKS[track]} · Today's Plan",{'prescription':rx})
    return {'session':s,'prescription':rx,'questions':prep_questions(u['id'],s['id'],qs),'mode':'practice'}

@app.post('/api/session/chapter')
def chapter(code:str,n:int=10,level:int=0,u=Depends(current_user)):
    throttle(u['id'],'session',30,3600)
    b=curriculum.BAB_BY_KODE.get(code)
    if not b or b.bagian not in ('Tes Potensi','TSKKWK'):raise HTTPException(404,'Unknown chapter')
    track='tpa' if b.bagian=='Tes Potensi' else 'substansi';n=max(5,min(n,30));level=level if level in (0,1,2,3) else 0
    import random
    qs=[q.to_dict()|{'track':track} for q in engine.bangun(code,n,level,random.Random(time.time_ns()))]
    s=store.new_learning_session(u['id'],track,'chapter',f'{b.judul} · {n}',{'chapter':code,'level':level})
    return {'session':s,'questions':prep_questions(u['id'],s['id'],qs),'mode':'practice'}

@app.post('/api/session/tryout')
def tryout(track:str='tpa',u=Depends(current_user)):
    throttle(u['id'],'session',30,3600)
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    qs=core.build_tryout(track)
    s=store.new_learning_session(u['id'],track,'tryout',f'Try Out · {TRACKS[track]}',{'passes':3,'question_count':len(qs)})
    for q in qs:q['_exam_mode']=True
    return {'session':s,'questions':prep_questions(u['id'],s['id'],qs),'mode':'tryout','passes':3}


@app.get('/api/mastery')
def mastery_status(track:str='tpa',u=Depends(current_user)):
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    a=track_attempts(u['id'],track);sessions=store.recent_sessions(u['id'],100)
    return mastery.tpa_badges(a,sessions) if track=='tpa' else mastery.substansi_badges(a,sessions)

@app.post('/api/session/mastery')
def mastery_challenge(section:str,track:str='tpa',u=Depends(current_user)):
    throttle(u['id'],'session',30,3600)
    if track not in TRACKS:raise HTTPException(404,'Unknown track')
    attempts=track_attempts(u['id'],track);sessions=store.recent_sessions(u['id'],100)
    current=mastery.tpa_badges(attempts,sessions) if track=='tpa' else mastery.substansi_badges(attempts,sessions)
    badge=next((b for b in current['badges'] if b['section']==section),None)
    if not badge:raise HTTPException(404,'Unknown mastery section')
    if not badge['challenge_unlocked'] and not bool(int(os.getenv('UPKP_ALLOW_EARLY_MASTERY','0'))):
        gate='coverage, retention, dan Exam-level gate' if track=='substansi' else 'coverage dan Exam-level gate'
        raise HTTPException(409,f'Mastery Challenge belum terbuka. Selesaikan {gate} lebih dulu.')
    qs=core.build_mastery_challenge(section,track)
    if not qs:raise HTTPException(503,'Mastery Challenge belum dapat dibangun untuk section ini.')
    s=store.new_learning_session(u['id'],track,'mastery',f"{badge['label']} Challenge",{'section':section,'question_count':len(qs),'track':track})
    for q in qs:q['_exam_mode']=True
    return {'session':s,'questions':prep_questions(u['id'],s['id'],qs),'mode':'tryout','passes':1,'mastery_section':section,'mastery_track':track}

@app.post('/api/session/resume/{sid}')
def resume_session(sid:str,u=Depends(current_user)):
    sess=store.get_learning_session(u['id'],sid)
    if not sess:raise HTTPException(404,'Session not found')
    if sess.get('ended') is not None:raise HTTPException(409,'Sesi ini sudah selesai dan tidak dapat dilanjutkan.')
    rows=store.session_question_rows(u['id'],sid,unused_only=True)
    if not rows:raise HTTPException(409,'Tidak ada soal tersisa di sesi ini.')
    questions=[]
    for row in rows:
        q=row['payload']
        item=public_q(q);item['token']=row['token'];questions.append(item)
    mode='tryout' if sess.get('kind') in ('tryout','mastery') else 'practice'
    return {'session':sess,'questions':questions,'mode':mode,'resumed':True}

@app.post('/api/attempt')
def attempt(body:AttemptIn,u=Depends(current_user)):
    # Token-bound authenticated attempts are naturally capped by session creation.
    # Keep answer recording to one DB transaction instead of read + throttle + write connections.
    if not body.skipped and body.selected is None:raise HTTPException(422,'Answer required')
    consume=(not body.skipped) or body.pass_number>=3
    key=f"{u['id']}:{body.question_token}:p{body.pass_number}:{'skip' if body.skipped else 'answer'}"
    def build_attempt(q):
        if body.session_id!=q.get('_session_id'):raise HTTPException(403,'Token belongs to another session')
        correct=(body.selected==q.get('ans')) and not body.skipped
        a=learning.make_attempt(q,selected=body.selected,correct=correct,elapsed_ms=body.elapsed_ms,confidence=body.confidence,first_selection_ms=body.first_selection_ms,answer_changes=body.answer_changes,skipped=body.skipped,pass_number=body.pass_number,session_id=body.session_id)
        a['track']=q.get('track','tpa');a['hint_level']=body.hint_level
        return a
    status,q,a=store.record_from_question_atomic(u['id'],body.question_token,consume,key,build_attempt)
    if status=='missing':raise HTTPException(404,'Question expired')
    if status=='duplicate':raise HTTPException(409,'Already submitted')
    if q.get('_exam_mode'):return {'deferred_feedback':True,'recorded':True}
    return {'correct':bool(a.get('correct')),'answer':q['ans'],'explanation':q.get('exp',''),'shortcut':q.get('trick',''),'attempt':a,'skill':learning.skill_label(a['skill']),'teacher_feedback':learning.attempt_coach_note(a)}

@app.post('/api/session/close')
def close(body:CloseIn,u=Depends(current_user)):
    rows=store.attempts(u['id']);pm=learning.session_postmortem(rows,body.session_id)
    sess=store.get_learning_session(u['id'],body.session_id)
    if not sess: raise HTTPException(404,'Session not found')
    pm['abandoned']=bool(body.abandoned)
    if body.abandoned:
        pm['recommendation']='Sesi dihentikan. Jawaban yang sudah dikirim tetap tersimpan dan ikut memperbarui profil belajar.'
    if sess.get('kind')=='mastery' and not body.abandoned:
        verdict=mastery.evaluate_mastery_challenge(sess.get('meta',{}).get('section',''),rows,body.session_id,sess.get('track','tpa'))
        pm={**pm,**verdict}
    pm=learning.enrich_postmortem(pm)
    store.close_learning_session(u['id'],body.session_id,pm)
    return {'ok':True,'postmortem':pm}

@app.post('/api/report-question')
def report_question(body:ReportIn,u=Depends(current_user)):
    throttle(u['id'],'report',20,3600)
    if body.reason not in {'ambiguous','wrong_key','broken_figure','typo','too_easy','too_hard','other'}:
        raise HTTPException(422,'Unknown report reason')
    result=store.report_question(u['id'],body.item_signature,body.question_id,body.reason,body.detail)
    if result.get('error')=='not_attempted':raise HTTPException(403,'Hanya soal yang pernah dikerjakan yang dapat dilaporkan')
    return result

@app.post('/api/account/reset-learning')
def reset_learning(body:ResetLearningIn,u=Depends(current_user)):
    row=store.get_user_by_username(u['username'])
    try:ph.verify(row['password_hash'],body.password)
    except VerifyMismatchError:raise HTTPException(401,'Password salah')
    store.reset_learning_history(u['id'])
    return {'ok':True}

@app.post('/api/account/delete')
def delete_account(body:DeleteAccountIn,response:Response,u=Depends(current_user)):
    row=store.get_user_by_username(u['username'])
    try:ph.verify(row['password_hash'],body.password)
    except VerifyMismatchError:raise HTTPException(401,'Password salah')
    store.delete_user(u['id']);response.delete_cookie(COOKIE,path='/')
    return {'ok':True}

@app.get('/api/admin/reports')
def admin_reports(u=Depends(admin_user)):return {'reports':store.report_list(150)}

@app.get('/api/admin/calibration')
def admin_calibration(u=Depends(admin_user)):return {'items':store.population_stats(300)}

@app.post('/api/admin/quarantine/{signature}')
def admin_quarantine(signature:str,active:bool=True,u=Depends(admin_user)):
    store.set_quarantine(signature,active,'admin review')
    store.write_audit(u['id'],'set_quarantine','question',signature,{'active':active})
    return {'ok':True,'active':active}

@app.post('/api/admin/maintenance')
def admin_maintenance(u=Depends(admin_user)):
    cleanup=store.maintenance_cleanup()
    store.write_audit(u['id'],'maintenance_cleanup','system','database',cleanup)
    return {'ok':True,'cleanup':cleanup}

@app.get('/api/admin/users')
def admin_users(u=Depends(admin_user)):return {'users':store.list_users()}

@app.get('/api/admin/data/overview')
def admin_data_overview(u=Depends(admin_user)):return {'counts':store.admin_data_overview()}

@app.get('/api/admin/data/users/{uid}')
def admin_data_user(uid:str,u=Depends(admin_user)):
    d=store.admin_user_detail(uid)
    if not d:raise HTTPException(404,'User not found')
    return d

@app.get('/api/admin/audit')
def admin_audit(u=Depends(admin_user)):return {'items':store.audit_log(150)}

@app.post('/api/admin/users/{uid}/disable')
def admin_disable(uid:str,disabled:bool=True,u=Depends(admin_user)):
    if uid==u['id'] and disabled:raise HTTPException(409,'Admin tidak dapat menonaktifkan akun sendiri.')
    store.set_disabled(uid,disabled);store.write_audit(u['id'],'set_user_disabled','user',uid,{'disabled':disabled});return {'ok':True}

@app.post('/api/admin/users/{uid}/reset-password')
def admin_reset(uid:str,body:AdminReset,u=Depends(admin_user)):
    store.reset_password(uid,ph.hash(body.password));store.write_audit(u['id'],'reset_password','user',uid,{});return {'ok':True}

@app.post('/api/admin/users/{uid}/reset-learning')
def admin_reset_learning(uid:str,u=Depends(admin_user)):
    if not store.admin_user_detail(uid):raise HTTPException(404,'User not found')
    store.reset_learning_history(uid);store.write_audit(u['id'],'reset_learning_history','user',uid,{})
    return {'ok':True}
