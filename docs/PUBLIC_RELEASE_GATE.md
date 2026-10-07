# UPKP Coach v1.3 — Public Release Gate

A release may be called **public-ready** only when every blocking item below is green.

## Automated gates
- [x] Python compile
- [x] Full pytest suite
- [x] Baseline content QA: zero hard validity issues
- [x] Advanced L4/L5 content QA: zero hard validity issues
- [x] Mastery Challenge has Exam/Hard evidence
- [x] Cross-site mutation protection test
- [x] Reserved-admin takeover test
- [x] Terms gate test
- [x] Question report → auto-quarantine test
- [x] Population calibration test
- [x] Schema-aware health test
- [x] TS/TSX syntax parse
- [ ] `npm install && npm run typecheck && npm run build` on the actual CI/Vercel builder
- [ ] Preview deployment smoke test against real Supabase

The last two require an external Node/Vercel build environment and production-like database credentials. They are deployment gates, not source-code TODOs.

## Production configuration gates
- `DATABASE_URL`: Supabase Transaction Pooler URI, SSL required.
- `ADMIN_USERNAME`: reserved admin username; public registration cannot claim it.
- `REQUIRE_TERMS=1`
- `COOKIE_SECURE=1`
- Run `sql/001_init.sql` on a fresh database; `sql/002_public_hardening.sql` is idempotent upgrade support.
- Bootstrap admin with `python scripts/bootstrap_admin.py --username <ADMIN_USERNAME>`.
- `/api/health` must return HTTP 200 and `ok: true`.

## Public-product gates
- Main learner navigation remains only: Beranda / Belajar / Try Out / Progress.
- TPA Mastery has four badges: Verbal, Numerical, Logical, Figural.
- `TPA Ready` means 4/4 internal mastery badges, not an official pass guarantee.
- Substansi is visibly labelled **Beta** until regulatory content receives a separate provenance audit.
- Every answered practice item can be reported.
- Three independent reports on a structural item signature trigger quarantine.
- Admin can release/quarantine content and view empirical difficulty drift.
- Privacy and independent/unofficial disclaimer pages are public.
