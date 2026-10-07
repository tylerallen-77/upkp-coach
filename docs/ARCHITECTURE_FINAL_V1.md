# Architecture — Final v1

```text
Browser
  │
  ├─ Next.js / React UI (Vercel)
  │
  └─ /api/* → FastAPI Python Function (same Vercel project)
                    │
                    ├─ Python UPKP generator + adaptive engine
                    │
                    └─ Supabase Postgres via transaction pooler
```

## Why no Supabase Auth?
Product requirement is username + password without email/phone. Final v1 therefore uses Postgres only and implements a small server-side auth layer. Supabase credentials are never exposed to the browser.

## Why transaction pooler?
Vercel Functions are serverless and short-lived. Use Supabase's transaction-pooler connection string (port 6543), not a long-lived direct connection. `psycopg` has prepared statements disabled (`prepare_threshold=None`) to remain compatible with transaction pooling.

## Local mode
Without `DATABASE_URL`, the same API uses local SQLite for tests/development. Local mode is not the production persistence mechanism.
