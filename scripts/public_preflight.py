from __future__ import annotations
import json, os, subprocess, sys
from pathlib import Path
from upkp.content_qa import audit, audit_advanced

ROOT=Path(__file__).resolve().parents[1]

def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    return p.returncode,p.stdout+p.stderr

def main():
    checks=[]
    rc,out=run([sys.executable,'-m','pytest','-q'])
    checks.append(('pytest',rc==0,out.strip().splitlines()[-1] if out.strip() else ''))
    rc2,out2=run([sys.executable,'-m','compileall','-q','api','upkp','scripts'])
    checks.append(('python_compile',rc2==0,out2.strip()))
    b=audit(sample_per_level=15,seed=20261007)
    a=audit_advanced(samples_per_skill=60,seed=20261008)
    checks.append(('content_baseline',b['ok'],f"sampled={b['sampled']} issues={b['issue_count']}"))
    checks.append(('content_advanced',a['ok'],f"sampled={a['sampled']} issues={a['issue_count']} archetypes={a['archetype_total']}"))
    cfg=(ROOT/'next.config.mjs').read_text()
    for key in ['Content-Security-Policy','Strict-Transport-Security','X-Content-Type-Options','X-Frame-Options']:
        checks.append((f'header_{key}',key in cfg,''))
    checks.append(('admin_bootstrap',(ROOT/'scripts/bootstrap_admin.py').exists(),''))
    checks.append(('migration_002',(ROOT/'sql/002_public_hardening.sql').exists(),''))
    checks.append(('privacy',(ROOT/'app/privacy/page.tsx').exists(),''))
    checks.append(('disclaimer',(ROOT/'app/about/page.tsx').exists(),''))
    pkg=json.loads((ROOT/'package.json').read_text())
    exact=all(not str(v).startswith(('^','~')) for block in ('dependencies','devDependencies') for v in pkg.get(block,{}).values())
    checks.append(('exact_top_level_dependencies',exact,''))
    failed=[x for x in checks if not x[1]]
    for name,ok,detail in checks:print(('PASS' if ok else 'FAIL').ljust(5),name,detail)
    print(f'\n{len(checks)-len(failed)}/{len(checks)} source preflight checks passed')
    if not (ROOT/'node_modules/next').exists():
        print('EXTERNAL GATE: node_modules unavailable here; CI/Vercel must run npm install + typecheck + next build.')
    return 1 if failed else 0

if __name__=='__main__':raise SystemExit(main())
