"""Import a V2.4 legacy export into one Final-v1 user.

1) Create/login to the target user once in Final.
2) python scripts/migrate_sqlite_export.py /path/coach.sqlite3 > legacy.json
3) Set DATABASE_URL (Supabase transaction-pooler URL).
4) python scripts/import_legacy_to_user.py legacy.json rio

Idempotency: legacy attempts use deterministic attempt_key prefixes, so reruns are skipped.
"""
from __future__ import annotations
import sys,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from upkp import multi_store as store
from upkp.curriculum import BAB_BY_KODE

def track_for(a):
    b=BAB_BY_KODE.get(str(a.get('bab','')))
    return 'substansi' if b and b.bagian=='TSKKWK' else 'tpa'

def main(path,username):
    u=store.get_user_by_username(username)
    if not u: raise SystemExit(f'User {username!r} belum ada di Final.')
    d=json.loads(Path(path).read_text(encoding='utf-8'))
    imported=0
    with store.connect() as c:
        for i,a in enumerate(d.get('attempts',[])):
            a=dict(a);a['track']=track_for(a)
            key=f"legacy:{u['id']}:{i}:{a.get('question_id','')}:{int(float(a.get('ts',0)))}"
            try:
                store.execute(c,'INSERT INTO attempts(user_id,attempt_key,ts,session_id,question_id,track,skill,payload) VALUES(?,?,?,?,?,?,?,?)',
                    (u['id'],key,float(a.get('ts',time.time())),str(a.get('session_id','legacy')),str(a.get('question_id','')),a['track'],str(a.get('skill','unknown')),store._json(a)))
                imported+=1
            except Exception:
                if store._is_pg(): c.rollback()
                continue
        if store._is_pg():c.commit()
    print(f'Imported {imported} attempts to @{u["username"]}.')
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: import_legacy_to_user.py legacy.json username')
    main(sys.argv[1],sys.argv[2])
