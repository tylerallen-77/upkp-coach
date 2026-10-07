# Public deployment — Vercel + Supabase

## 1. Create Supabase database
Create a Supabase project. In **Connect**, copy the **Transaction pooler** URI (port 6543) for serverless workloads. Keep it server-side only.

Run `sql/001_init.sql` in the Supabase SQL editor. For upgrades from an older UPKP Coach schema, also run `sql/002_public_hardening.sql`.

## 2. Bootstrap the admin safely
Do **not** create the reserved admin username through public registration. Public signup rejects it by design.

Set `DATABASE_URL` locally, then run:

```bash
python scripts/bootstrap_admin.py --username rio
```

The script prompts for the password without echoing it and creates/promotes the account directly in the database.

## 3. Vercel environment variables
Set for Production and Preview as appropriate:

```text
DATABASE_URL=<Supabase Transaction Pooler URI with sslmode=require>
ADMIN_USERNAME=rio
REQUIRE_TERMS=1
COOKIE_SECURE=1
```

Never prefix the database variable with `NEXT_PUBLIC_`.

## 4. Deploy preview first
Push to GitHub and import the repository into Vercel. Do not promote the first deployment immediately.

Required preview smoke:
1. `/api/health` -> 200 / `ok:true`
2. register a normal learner account
3. login/logout/login
4. start first TPA diagnostic; verify Foundation/Standard/Exam appear
5. answer a text question
6. answer a table question
7. answer a figural SVG question
8. refresh browser and confirm progress persists
9. inspect Progress -> four Mastery badges visible
10. verify `/about` and `/privacy`
11. login as admin and open `/admin`
12. submit a test question report; confirm it appears in Admin Console

## 5. Security before promotion
- Keep Vercel Build Logs / Source Protection enabled.
- Review Vercel Firewall / WAF settings; platform DDoS protection remains enabled.
- Keep HTTPS only.
- Confirm security headers on the preview response.
- Do not log request bodies, passwords, cookies, or database URLs.

## 6. Promote
Only after CI and preview smoke are green, promote the deployment to Production.

## 7. Early public operations
During the first cohort, check:
- question reports daily,
- empirical-vs-authored difficulty drift,
- database size,
- Vercel function errors/latency,
- registration/login abuse,
- mastery badge attainability.

Run Admin Console cleanup periodically to remove expired sessions, old question tokens and stale rate-limit buckets.
