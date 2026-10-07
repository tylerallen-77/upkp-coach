"""Transactional SQLite storage for UPKP Coach.

V2.4 stores attempts and sessions as independent rows instead of rewriting one
large profile document. It transparently imports the older JSON/blob storage.
"""
from __future__ import annotations
import json, os, time, uuid, sqlite3, threading
from pathlib import Path

DATA_DIR = Path(os.environ.get("UPKP_DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
LEGACY_FILE = DATA_DIR / "coach_v2.json"
FILE = LEGACY_FILE  # backward-compatible alias used by older tests/tools
DB = Path(os.environ.get("UPKP_DB_PATH", str(DATA_DIR / "coach.sqlite3")))
VERSION = 4
_DB_LOCK = threading.RLock()


def connect():
    DB.parent.mkdir(parents=True, exist_ok=True)
    c=sqlite3.connect(DB,timeout=20,isolation_level=None)
    c.row_factory=sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=NORMAL")
    c.execute("PRAGMA foreign_keys=ON")
    c.execute("PRAGMA busy_timeout=20000")
    c.executescript("""
    CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS attempts(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      token TEXT UNIQUE,
      ts REAL NOT NULL,
      session_id TEXT NOT NULL,
      question_id TEXT NOT NULL,
      skill TEXT NOT NULL,
      payload TEXT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_attempts_ts ON attempts(ts);
    CREATE INDEX IF NOT EXISTS idx_attempts_session ON attempts(session_id,id);
    CREATE INDEX IF NOT EXISTS idx_attempts_skill ON attempts(skill,id);
    CREATE TABLE IF NOT EXISTS sessions(
      id TEXT PRIMARY KEY,
      started REAL NOT NULL,
      ended REAL,
      kind TEXT NOT NULL,
      title TEXT NOT NULL,
      meta TEXT NOT NULL DEFAULT '{}',
      summary TEXT NOT NULL DEFAULT '{}'
    );
    CREATE INDEX IF NOT EXISTS idx_sessions_started ON sessions(started DESC);
    CREATE TABLE IF NOT EXISTS question_tokens(
      token TEXT PRIMARY KEY,
      payload TEXT NOT NULL,
      created REAL NOT NULL,
      used INTEGER NOT NULL DEFAULT 0,
      session_id TEXT NOT NULL
    );
    """)
    return c


def _json(v): return json.dumps(v,ensure_ascii=False,separators=(",",":"))
def _parse(v,default):
    try: return json.loads(v)
    except Exception: return default


def _import_legacy_once(con):
    row=con.execute("SELECT value FROM meta WHERE key='legacy_import_done'").fetchone()
    if row: return
    legacy=None
    # Old relational-blob profile DB, if present next to the new DB.
    old_db=DATA_DIR/"profile.sqlite3"
    if old_db.exists() and old_db.resolve()!=DB.resolve():
        try:
            oc=sqlite3.connect(old_db)
            r=oc.execute("SELECT value FROM profile WHERE id=1").fetchone(); oc.close()
            if r: legacy=json.loads(r[0])
        except Exception: pass
    if legacy is None and LEGACY_FILE.exists():
        try: legacy=json.loads(LEGACY_FILE.read_text(encoding="utf-8"))
        except Exception: legacy=None
    if isinstance(legacy,dict):
        for a in legacy.get("attempts",[]):
            try:
                con.execute("INSERT INTO attempts(token,ts,session_id,question_id,skill,payload) VALUES(NULL,?,?,?,?,?)",
                            (float(a.get("ts",time.time())),str(a.get("session_id","")),str(a.get("question_id","")),str(a.get("skill","unknown")),_json(a)))
            except Exception: pass
        for s in legacy.get("sessions",[]):
            try:
                con.execute("INSERT OR IGNORE INTO sessions(id,started,ended,kind,title,meta,summary) VALUES(?,?,?,?,?,?,?)",
                            (str(s.get("id") or uuid.uuid4().hex[:16]),float(s.get("started",time.time())),s.get("ended"),str(s.get("kind","legacy")),str(s.get("title","Legacy session")),_json(s.get("meta",{})),_json(s.get("summary",{}))))
            except Exception: pass
        for k,v in (legacy.get("settings") or {"track":"TPA"}).items():
            con.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",(str(k),_json(v)))
    con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('legacy_import_done',?)",(str(time.time()),))
    con.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('schema_version',?)",(str(VERSION),))


def ensure_schema():
    with _DB_LOCK, connect() as con:
        con.execute("BEGIN IMMEDIATE"); _import_legacy_once(con); con.commit()


def load() -> dict:
    ensure_schema()
    with _DB_LOCK, connect() as con:
        attempts=[_parse(r[0],{}) for r in con.execute("SELECT payload FROM attempts ORDER BY id").fetchall()]
        sessions=[]
        for r in con.execute("SELECT id,started,ended,kind,title,meta,summary FROM sessions WHERE ended IS NOT NULL ORDER BY started DESC LIMIT 200"):
            sessions.append({"id":r[0],"started":r[1],"ended":r[2],"kind":r[3],"title":r[4],"meta":_parse(r[5],{}),"summary":_parse(r[6],{})})
        settings={r[0]:_parse(r[1],r[1]) for r in con.execute("SELECT key,value FROM settings")}
    if "track" not in settings: settings["track"]="TPA"
    return {"version":VERSION,"attempts":attempts,"sessions":sessions,"settings":settings}


def save(d: dict) -> None:
    """Compatibility method. Only settings are mutable through whole-state save.

    Attempts/sessions are persisted transactionally by their dedicated methods.
    """
    ensure_schema()
    with _DB_LOCK, connect() as con:
        con.execute("BEGIN IMMEDIATE")
        for k,v in (d.get("settings") or {}).items():
            con.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)",(str(k),_json(v)))
        con.commit()


def new_session(kind: str, title: str, meta: dict | None = None) -> dict:
    ensure_schema(); s={"id":uuid.uuid4().hex[:16],"started":time.time(),"ended":None,"kind":kind,"title":title,"meta":meta or {}}
    with _DB_LOCK, connect() as con:
        con.execute("INSERT INTO sessions(id,started,ended,kind,title,meta,summary) VALUES(?,?,?,?,?,?,?)",
                    (s["id"],s["started"],None,kind,title,_json(s["meta"]),"{}"))
    return s


def record_attempt(d: dict, attempt: dict, token: str | None = None) -> None:
    """Persist one attempt atomically. token makes client retries idempotent."""
    ensure_schema()
    with _DB_LOCK, connect() as con:
        try:
            con.execute("INSERT INTO attempts(token,ts,session_id,question_id,skill,payload) VALUES(?,?,?,?,?,?)",
                        (token,float(attempt.get("ts",time.time())),str(attempt.get("session_id","")),str(attempt.get("question_id","")),str(attempt.get("skill","unknown")),_json(attempt)))
        except sqlite3.IntegrityError:
            # Same token already recorded: idempotent retry.
            return
    d.setdefault("attempts",[]).append(attempt)


def close_session(d: dict, session: dict, summary: dict | None = None) -> None:
    ensure_schema(); ended=time.time(); sid=str(session.get("id","")); summary=summary or {}
    with _DB_LOCK, connect() as con:
        con.execute("UPDATE sessions SET ended=?,meta=?,summary=? WHERE id=?",
                    (ended,_json(session.get("meta",{})),_json(summary),sid))
    session=dict(session);session["ended"]=ended;session["summary"]=summary
    d.setdefault("sessions",[]).insert(0,session)


def export_snapshot() -> dict:
    """Portable, non-secret user learning snapshot; question tokens excluded."""
    d=load(); d["exported_at"]=time.time(); d["schema_version"]=VERSION; return d


def stats() -> dict:
    ensure_schema()
    with _DB_LOCK, connect() as con:
        return {
            "attempts":con.execute("SELECT COUNT(*) FROM attempts").fetchone()[0],
            "sessions":con.execute("SELECT COUNT(*) FROM sessions WHERE ended IS NOT NULL").fetchone()[0],
            "open_sessions":con.execute("SELECT COUNT(*) FROM sessions WHERE ended IS NULL").fetchone()[0],
            "live_tokens":con.execute("SELECT COUNT(*) FROM question_tokens WHERE used=0 AND created>=?",(time.time()-86400,)).fetchone()[0],
            "db_bytes":DB.stat().st_size if DB.exists() else 0,
        }

ensure_schema()


def record_with_question_token(attempt: dict, question_token: str, *, consume: bool, attempt_key: str) -> str:
    """Atomically persist an attempt and optionally consume its question token.

    Returns ``recorded`` or ``duplicate``. If consume=True, the token transition
    and attempt insert occur in one SQLite transaction, preventing double-submit
    races across threads/processes sharing the same database.
    """
    ensure_schema()
    with _DB_LOCK, connect() as con:
        con.execute("BEGIN IMMEDIATE")
        try:
            row=con.execute("SELECT used,created FROM question_tokens WHERE token=?",(question_token,)).fetchone()
            if row is None or time.time()-float(row[1])>86400:
                con.rollback(); return "missing"
            if consume:
                changed=con.execute("UPDATE question_tokens SET used=1 WHERE token=? AND used=0",(question_token,)).rowcount
                if changed!=1:
                    con.rollback(); return "duplicate"
            try:
                con.execute("INSERT INTO attempts(token,ts,session_id,question_id,skill,payload) VALUES(?,?,?,?,?,?)",
                            (attempt_key,float(attempt.get("ts",time.time())),str(attempt.get("session_id","")),str(attempt.get("question_id","")),str(attempt.get("skill","unknown")),_json(attempt)))
            except sqlite3.IntegrityError:
                con.rollback(); return "duplicate"
            con.commit(); return "recorded"
        except Exception:
            con.rollback(); raise
