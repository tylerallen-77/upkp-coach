"""Export legacy V2.4 SQLite attempts/sessions for optional manual migration.
This never copies auth credentials because V2.4 had no multi-user identities.
Usage: python scripts/migrate_sqlite_export.py /path/to/coach.sqlite3 > legacy_export.json
"""
import sys,sqlite3,json
p=sys.argv[1]
c=sqlite3.connect(p)
out={'attempts':[],'sessions':[]}
for (payload,) in c.execute('select payload from attempts order by id'):
    try: out['attempts'].append(json.loads(payload))
    except Exception: pass
for r in c.execute('select id,started,ended,kind,title,meta,summary from sessions order by started'):
    out['sessions'].append({'id':r[0],'started':r[1],'ended':r[2],'kind':r[3],'title':r[4],'meta':json.loads(r[5] or '{}'),'summary':json.loads(r[6] or '{}')})
print(json.dumps(out,ensure_ascii=False,indent=2))
