from __future__ import annotations
import os, json, time, uuid, sqlite3, hashlib, secrets
from pathlib import Path

DATABASE_URL=os.getenv('DATABASE_URL','').strip()
LOCAL_DB=Path(os.getenv('UPKP_LOCAL_DB',Path(__file__).resolve().parent.parent/'data'/'final_local.sqlite3'))


def _is_pg(): return DATABASE_URL.startswith('postgres')

def _pg():
    import psycopg
    return psycopg.connect(DATABASE_URL, autocommit=False, prepare_threshold=None)

def connect():
    if _is_pg(): return _pg()
    LOCAL_DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(LOCAL_DB,timeout=20,isolation_level=None)
    c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON'); c.execute('PRAGMA journal_mode=WAL')
    return c

def ph(sql:str)->str:
    return sql.replace('?', '%s') if _is_pg() else sql

def _json(v): return json.dumps(v,ensure_ascii=False,separators=(',',':'))
def _decode(v,default):
    if v is None:return default
    if isinstance(v,(dict,list)):return v
    try:return json.loads(v)
    except Exception:return default

def init_schema():
    if _is_pg():
        return
    with connect() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,username TEXT UNIQUE COLLATE NOCASE,password_hash TEXT NOT NULL,role TEXT NOT NULL DEFAULT 'user',disabled INTEGER NOT NULL DEFAULT 0,created_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS auth_sessions(token_hash TEXT PRIMARY KEY,user_id TEXT NOT NULL,created_at REAL NOT NULL,expires_at REAL NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS learning_sessions(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,track TEXT NOT NULL,kind TEXT NOT NULL,title TEXT NOT NULL,started REAL NOT NULL,ended REAL,meta TEXT NOT NULL DEFAULT '{}',summary TEXT NOT NULL DEFAULT '{}',FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id TEXT NOT NULL,attempt_key TEXT UNIQUE,ts REAL NOT NULL,session_id TEXT NOT NULL,question_id TEXT NOT NULL,track TEXT NOT NULL,skill TEXT NOT NULL,payload TEXT NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
        CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts(user_id,id);
        CREATE INDEX IF NOT EXISTS idx_attempts_user_track ON attempts(user_id,track,id);
        CREATE TABLE IF NOT EXISTS question_tokens(token TEXT PRIMARY KEY,user_id TEXT NOT NULL,session_id TEXT NOT NULL,payload TEXT NOT NULL,created REAL NOT NULL,used INTEGER NOT NULL DEFAULT 0,FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS question_reports(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id TEXT NOT NULL,item_signature TEXT NOT NULL,question_id TEXT NOT NULL,reason TEXT NOT NULL,detail TEXT NOT NULL DEFAULT '',created_at REAL NOT NULL,UNIQUE(user_id,item_signature),FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);
        CREATE TABLE IF NOT EXISTS content_quarantine(item_signature TEXT PRIMARY KEY,reason TEXT NOT NULL,report_count INTEGER NOT NULL DEFAULT 0,active INTEGER NOT NULL DEFAULT 1,created_at REAL NOT NULL,updated_at REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS population_item_stats(item_signature TEXT PRIMARY KEY,skill TEXT NOT NULL,authored_level INTEGER NOT NULL,attempts INTEGER NOT NULL DEFAULT 0,correct INTEGER NOT NULL DEFAULT 0,skipped INTEGER NOT NULL DEFAULT 0,elapsed_sum_ms INTEGER NOT NULL DEFAULT 0,answer_changes INTEGER NOT NULL DEFAULT 0,high_confidence_wrong INTEGER NOT NULL DEFAULT 0,updated_at REAL NOT NULL);
        ''')
        try:c.execute('ALTER TABLE attempts ADD COLUMN item_signature TEXT')
        except Exception:pass

def execute(c,sql,args=()): return c.execute(ph(sql),args)
def fetchone(c,sql,args=()): return execute(c,sql,args).fetchone()
def fetchall(c,sql,args=()): return execute(c,sql,args).fetchall()

def _row(row):
    if row is None:return None
    if hasattr(row,'keys'): return {k:row[k] for k in row.keys()}
    return row

def create_user(username,password_hash,role='user'):
    init_schema(); uid=uuid.uuid4().hex
    with connect() as c:
        try:
            execute(c,'INSERT INTO users(id,username,password_hash,role,disabled,created_at) VALUES(?,?,?,?,0,?)',(uid,username.lower(),password_hash,role,time.time()))
            if _is_pg(): c.commit()
        except Exception:
            if _is_pg(): c.rollback()
            raise
    return {'id':uid,'username':username.lower(),'role':role}

def get_user_by_username(username):
    init_schema()
    with connect() as c:
        r=fetchone(c,'SELECT id,username,password_hash,role,disabled,created_at FROM users WHERE lower(username)=lower(?)',(username,))
        if not r:return None
        if _is_pg():
            vals=['id','username','password_hash','role','disabled','created_at']; return dict(zip(vals,r))
        return dict(r)

def get_user(uid):
    init_schema()
    with connect() as c:
        r=fetchone(c,'SELECT id,username,role,disabled,created_at FROM users WHERE id=?',(uid,))
        if not r:return None
        vals=['id','username','role','disabled','created_at']; return dict(zip(vals,r)) if _is_pg() else dict(r)

def create_auth_session(uid,days=30):
    raw=secrets.token_urlsafe(32); h=hashlib.sha256(raw.encode()).hexdigest(); now=time.time()
    with connect() as c:
        execute(c,'DELETE FROM auth_sessions WHERE expires_at<?',(now,))
        execute(c,'INSERT INTO auth_sessions(token_hash,user_id,created_at,expires_at) VALUES(?,?,?,?)',(h,uid,now,now+days*86400))
        if _is_pg(): c.commit()
    return raw

def user_from_session(raw):
    if not raw:return None
    h=hashlib.sha256(raw.encode()).hexdigest(); now=time.time()
    with connect() as c:
        r=fetchone(c,'SELECT u.id,u.username,u.role,u.disabled,u.created_at FROM auth_sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?',(h,now))
        if not r:return None
        vals=['id','username','role','disabled','created_at']; d=dict(zip(vals,r)) if _is_pg() else dict(r)
        return None if d.get('disabled') else d

def delete_auth_session(raw):
    if not raw:return
    h=hashlib.sha256(raw.encode()).hexdigest()
    with connect() as c:
        execute(c,'DELETE FROM auth_sessions WHERE token_hash=?',(h,))
        if _is_pg():c.commit()

def new_learning_session(uid,track,kind,title,meta=None):
    sid=uuid.uuid4().hex[:20]; now=time.time(); meta=meta or {}
    with connect() as c:
        execute(c,'INSERT INTO learning_sessions(id,user_id,track,kind,title,started,meta,summary) VALUES(?,?,?,?,?,?,?,?)',(sid,uid,track,kind,title,now,_json(meta),_json({})))
        if _is_pg():c.commit()
    return {'id':sid,'user_id':uid,'track':track,'kind':kind,'title':title,'started':now,'meta':meta}

def get_learning_session(uid,sid):
    with connect() as c:
        r=fetchone(c,'SELECT id,track,kind,title,started,ended,meta,summary FROM learning_sessions WHERE id=? AND user_id=?',(sid,uid))
    if not r:return None
    return {'id':r[0],'track':r[1],'kind':r[2],'title':r[3],'started':r[4],'ended':r[5],
            'meta':_decode(r[6],{}),'summary':_decode(r[7],{})}

def close_learning_session(uid,sid,summary):
    with connect() as c:
        execute(c,'UPDATE learning_sessions SET ended=?,summary=? WHERE id=? AND user_id=?',(time.time(),_json(summary),sid,uid))
        if _is_pg():c.commit()

def attempts(uid,track=None):
    with connect() as c:
        if track:
            rows=fetchall(c,'SELECT payload FROM attempts WHERE user_id=? AND track=? ORDER BY id',(uid,track))
        else: rows=fetchall(c,'SELECT payload FROM attempts WHERE user_id=? ORDER BY id',(uid,))
    return [_decode(r[0],{}) for r in rows]

def recent_sessions(uid,limit=8):
    with connect() as c:
        rows=fetchall(c,'SELECT id,track,kind,title,started,ended,meta,summary FROM learning_sessions WHERE user_id=? AND ended IS NOT NULL ORDER BY started DESC LIMIT ?',(uid,limit))
    out=[]
    for r in rows:
        out.append({'id':r[0],'track':r[1],'kind':r[2],'title':r[3],'started':r[4],'ended':r[5],'meta':_decode(r[6],{}),'summary':_decode(r[7],{})})
    return out

def stash_question(uid,sid,q):
    token=secrets.token_urlsafe(24)
    with connect() as c:
        execute(c,'DELETE FROM question_tokens WHERE created<?',(time.time()-86400,))
        execute(c,'INSERT INTO question_tokens(token,user_id,session_id,payload,created,used) VALUES(?,?,?,?,?,0)',(token,uid,sid,_json(q),time.time()))
        if _is_pg():c.commit()
    return token

def read_question(uid,token):
    with connect() as c:
        r=fetchone(c,'SELECT payload,used,created,session_id FROM question_tokens WHERE token=? AND user_id=?',(token,uid))
    if not r or bool(r[1]) or time.time()-float(r[2])>86400:return None
    q=_decode(r[0],{});q['_session_id']=r[3];return q

def record_attempt_atomic(uid,attempt,question_token,consume,attempt_key):
    with connect() as c:
        try:
            if _is_pg():
                r=fetchone(c,'SELECT used,created FROM question_tokens WHERE token=? AND user_id=? FOR UPDATE',(question_token,uid))
            else:
                execute(c,'BEGIN IMMEDIATE'); r=fetchone(c,'SELECT used,created FROM question_tokens WHERE token=? AND user_id=?',(question_token,uid))
            if not r or time.time()-float(r[1])>86400:
                if _is_pg():c.rollback()
                return 'missing'
            if consume:
                cur=execute(c,'UPDATE question_tokens SET used=1 WHERE token=? AND user_id=? AND used=0',(question_token,uid))
                if cur.rowcount!=1:
                    if _is_pg():c.rollback()
                    return 'duplicate'
            try:
                execute(c,'INSERT INTO attempts(user_id,attempt_key,ts,session_id,question_id,track,skill,item_signature,payload) VALUES(?,?,?,?,?,?,?,?,?)',(uid,attempt_key,float(attempt.get('ts',time.time())),str(attempt.get('session_id','')),str(attempt.get('question_id','')),str(attempt.get('track','tpa')),str(attempt.get('skill','unknown')),str(attempt.get('item_signature','')),_json(attempt)))
                _update_population_stats(c,attempt)
            except Exception:
                if _is_pg():c.rollback()
                return 'duplicate'
            if _is_pg():c.commit()
            return 'recorded'
        except Exception:
            if _is_pg():c.rollback()
            raise

def list_users():
    with connect() as c:
        rows=fetchall(c,'SELECT u.id,u.username,u.role,u.disabled,u.created_at,COUNT(a.id) FROM users u LEFT JOIN attempts a ON a.user_id=u.id GROUP BY u.id,u.username,u.role,u.disabled,u.created_at ORDER BY u.created_at DESC')
    return [{'id':r[0],'username':r[1],'role':r[2],'disabled':bool(r[3]),'created_at':r[4],'attempts':r[5]} for r in rows]

def set_disabled(uid,disabled):
    with connect() as c:
        execute(c,'UPDATE users SET disabled=? WHERE id=?',(1 if disabled else 0,uid))
        if _is_pg():c.commit()

def set_role(uid,role):
    if role not in ('user','admin'):raise ValueError('invalid role')
    with connect() as c:
        execute(c,'UPDATE users SET role=? WHERE id=?',(role,uid))
        if _is_pg():c.commit()


def reset_password(uid,password_hash):
    with connect() as c:
        execute(c,'UPDATE users SET password_hash=? WHERE id=?',(password_hash,uid)); execute(c,'DELETE FROM auth_sessions WHERE user_id=?',(uid,))
        if _is_pg():c.commit()

def _update_population_stats(c,attempt):
    sig=str(attempt.get('item_signature') or '')
    if not sig:return
    skill=str(attempt.get('skill','unknown'));lv=int(attempt.get('level',1));now=time.time()
    correct=1 if attempt.get('correct') else 0;skipped=1 if attempt.get('skipped') else 0
    elapsed=int(attempt.get('elapsed_ms',0));changes=int(attempt.get('answer_changes',0))
    hcw=1 if attempt.get('error_type')=='high_confidence_wrong' else 0
    r=fetchone(c,'SELECT attempts,correct,skipped,elapsed_sum_ms,answer_changes,high_confidence_wrong FROM population_item_stats WHERE item_signature=?',(sig,))
    if r:
        execute(c,'UPDATE population_item_stats SET attempts=?,correct=?,skipped=?,elapsed_sum_ms=?,answer_changes=?,high_confidence_wrong=?,updated_at=? WHERE item_signature=?',
                (int(r[0])+1,int(r[1])+correct,int(r[2])+skipped,int(r[3])+elapsed,int(r[4])+changes,int(r[5])+hcw,now,sig))
    else:
        execute(c,'INSERT INTO population_item_stats(item_signature,skill,authored_level,attempts,correct,skipped,elapsed_sum_ms,answer_changes,high_confidence_wrong,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)',
                (sig,skill,lv,1,correct,skipped,elapsed,changes,hcw,now))

def population_stats(limit=200):
    with connect() as c:
        rows=fetchall(c,'SELECT item_signature,skill,authored_level,attempts,correct,skipped,elapsed_sum_ms,answer_changes,high_confidence_wrong,updated_at FROM population_item_stats ORDER BY attempts DESC LIMIT ?',(limit,))
    out=[]
    for r in rows:
        n=max(1,int(r[3])); answered=max(1,n-int(r[5])); acc=int(r[4])/answered
        # Bayesian shrink avoids tiny-n extremes. Map higher difficulty to 1..5.
        shrunk=(int(r[4])+2)/(answered+4); difficulty=1+(1-shrunk)*4
        out.append({'signature':r[0],'skill':r[1],'authored_level':int(r[2]),'attempts':n,'accuracy':acc,'skip_rate':int(r[5])/n,
                    'mean_ms':int(r[6])/n,'answer_changes':int(r[7])/n,'high_confidence_wrong':int(r[8]),'empirical_level':round(difficulty,2),'updated_at':r[9]})
    return out

def user_has_signature(uid,sig):
    with connect() as c:return fetchone(c,'SELECT 1 FROM attempts WHERE user_id=? AND item_signature=? LIMIT 1',(uid,sig)) is not None

def report_question(uid,sig,qid,reason,detail=''):
    if not user_has_signature(uid,sig):return {'ok':False,'error':'not_attempted'}
    now=time.time()
    with connect() as c:
        try:
            execute(c,'INSERT INTO question_reports(user_id,item_signature,question_id,reason,detail,created_at) VALUES(?,?,?,?,?,?)',(uid,sig,qid,reason,detail[:500],now))
        except Exception:
            if _is_pg():c.rollback()
            return {'ok':True,'duplicate':True,'quarantined':is_quarantined(sig)}
        count=fetchone(c,'SELECT COUNT(DISTINCT user_id) FROM question_reports WHERE item_signature=?',(sig,))[0]
        if int(count)>=3:
            r=fetchone(c,'SELECT item_signature FROM content_quarantine WHERE item_signature=?',(sig,))
            if r: execute(c,'UPDATE content_quarantine SET active=1,report_count=?,reason=?,updated_at=? WHERE item_signature=?',(count,'auto: 3+ independent reports',now,sig))
            else: execute(c,'INSERT INTO content_quarantine(item_signature,reason,report_count,active,created_at,updated_at) VALUES(?,?,?,1,?,?)',(sig,'auto: 3+ independent reports',count,now,now))
        if _is_pg():c.commit()
    return {'ok':True,'duplicate':False,'report_count':int(count),'quarantined':int(count)>=3}

def is_quarantined(sig):
    if not sig:return False
    with connect() as c:
        r=fetchone(c,'SELECT active FROM content_quarantine WHERE item_signature=?',(sig,))
    return bool(r and int(r[0]))

def report_list(limit=100):
    with connect() as c:
        rows=fetchall(c,'SELECT r.item_signature,r.question_id,r.reason,r.detail,r.created_at,u.username,q.active,q.report_count FROM question_reports r JOIN users u ON u.id=r.user_id LEFT JOIN content_quarantine q ON q.item_signature=r.item_signature ORDER BY r.created_at DESC LIMIT ?',(limit,))
    return [{'signature':r[0],'question_id':r[1],'reason':r[2],'detail':r[3],'created_at':r[4],'username':r[5],'quarantined':bool(r[6] or 0),'report_count':int(r[7] or 0)} for r in rows]

def set_quarantine(sig,active,reason='admin review'):
    now=time.time()
    with connect() as c:
        r=fetchone(c,'SELECT item_signature FROM content_quarantine WHERE item_signature=?',(sig,))
        if r: execute(c,'UPDATE content_quarantine SET active=?,reason=?,updated_at=? WHERE item_signature=?',(1 if active else 0,reason,now,sig))
        else: execute(c,'INSERT INTO content_quarantine(item_signature,reason,report_count,active,created_at,updated_at) VALUES(?,?,0,?,?,?)',(sig,reason,1 if active else 0,now,now))
        if _is_pg():c.commit()

def db_health():
    try:
        required=('users','auth_sessions','learning_sessions','attempts','question_tokens','auth_rate_limits','question_reports','content_quarantine','population_item_stats')
        with connect() as c:
            r=fetchone(c,'SELECT 1')
            if not (r and int(r[0])==1):return False
            for table in required:
                fetchone(c,f'SELECT COUNT(*) FROM {table} WHERE 1=0')
        return True
    except Exception:
        return False

def maintenance_cleanup():
    now=time.time(); stats={}
    with connect() as c:
        for table,where,args,key in [
            ('auth_sessions','expires_at<?',(now,),'expired_sessions'),
            ('question_tokens','created<?',(now-86400,),'old_question_tokens'),
            ('auth_rate_limits','window_start<?',(now-86400,),'old_rate_limits')]:
            cur=execute(c,f'DELETE FROM {table} WHERE {where}',args);stats[key]=max(0,int(cur.rowcount or 0))
        if _is_pg():c.commit()
    return stats


def delete_user(uid):
    with connect() as c:
        execute(c,'DELETE FROM users WHERE id=?',(uid,))
        if _is_pg():c.commit()

init_schema()

def hit_rate_limit(bucket:str,limit:int=10,window_seconds:int=300)->bool:
    """Return True when blocked. PostgreSQL-backed so it works across serverless instances."""
    now=time.time()
    with connect() as c:
        try:
            if _is_pg():
                r=fetchone(c,'SELECT window_start,count FROM auth_rate_limits WHERE bucket=? FOR UPDATE',(bucket,))
            else:
                execute(c,'CREATE TABLE IF NOT EXISTS auth_rate_limits(bucket TEXT PRIMARY KEY,window_start REAL NOT NULL,count INTEGER NOT NULL DEFAULT 0)')
                execute(c,'BEGIN IMMEDIATE');r=fetchone(c,'SELECT window_start,count FROM auth_rate_limits WHERE bucket=?',(bucket,))
            if not r or now-float(r[0])>=window_seconds:
                execute(c,'DELETE FROM auth_rate_limits WHERE bucket=?',(bucket,))
                execute(c,'INSERT INTO auth_rate_limits(bucket,window_start,count) VALUES(?,?,1)',(bucket,now))
                if _is_pg():c.commit()
                return False
            count=int(r[1])+1
            execute(c,'UPDATE auth_rate_limits SET count=? WHERE bucket=?',(count,bucket))
            if _is_pg():c.commit()
            return count>limit
        except Exception:
            if _is_pg():c.rollback()
            raise
