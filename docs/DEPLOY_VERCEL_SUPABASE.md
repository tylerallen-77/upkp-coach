# Deploy — Vercel + Supabase Free

## 1. Create Supabase project
Create a free project. Keep the generated database password safe.

Open **SQL Editor** and run the complete contents of:

`sql/001_init.sql`

No Supabase Auth setup is required.

## 2. Copy the serverless database URL
In Supabase use **Connect → Transaction pooler**. Copy the Postgres URI that uses port `6543` and SSL.

Save it locally as `DATABASE_URL`. Never put it in frontend code and never prefix it `NEXT_PUBLIC_`.

## 3. Push this folder to GitHub
Repository root must contain `package.json`, `app/`, `api/`, `upkp/`, `requirements.txt`, and `vercel.json`.

## 4. Import GitHub repository into Vercel
Create a new Vercel project from the repo. Framework should be detected as Next.js.

Add Production/Preview environment variables:

- `DATABASE_URL` = Supabase transaction-pooler URI
- `ADMIN_USERNAME` = the username that should receive admin role when first registered (example: `rio`)
- `COOKIE_SECURE` = `1`

Deploy.

## 5. Smoke test
Open:

`https://YOUR-PROJECT.vercel.app/api/health`

Expected: `{ "ok": true, "version": "1.0.0", "database": "postgres" }`

Then register the `ADMIN_USERNAME` account first. It should return `role=admin`.

Create a second normal account and verify that progress is isolated.

## 6. Persistence test
On account A, answer 2–3 questions. Redeploy Vercel. Sign in again. Progress must remain because learning data is stored in Supabase, not in the Vercel filesystem.

## 7. Migration from PythonAnywhere alpha (optional)
Download `/home/upkpcoach/upkp-coach/data/coach.sqlite3` from PythonAnywhere.

Locally:

```bash
python scripts/migrate_sqlite_export.py coach.sqlite3 > legacy.json
export DATABASE_URL='YOUR_SUPABASE_TRANSACTION_POOLER_URL'
python scripts/import_legacy_to_user.py legacy.json rio
```

Create the `rio` Final account first. Migration imports learning attempts only; it does not import old Basic Auth credentials.

## 8. Admin recovery
Final v1 intentionally has no email reset. Admin reset/disable endpoints exist under `/api/admin/...`. A small admin UI can be added later without changing schema.

## Production caution
Substansi regulations/organization facts can change. Update source-sensitive question content before each exam cycle rather than assuming old regulation facts remain current.
