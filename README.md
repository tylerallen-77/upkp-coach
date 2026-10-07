# UPKP Coach v1.3 — Public-Ready Release Candidate

**Status:** source hardening complete; deploy to Vercel Preview and pass the external release gates before Production promotion.

Core product: adaptive UPKP learning with multi-user accounts, four TPA Mastery badges, meaningful difficulty, content reporting/quarantine, empirical difficulty calibration, and guided learning.

Start here:
- `docs/PUBLIC_RELEASE_GATE.md`
- `docs/DEPLOY_PUBLIC_VERCEL_SUPABASE.md`
- `docs/RELEASE_STATUS_v1.3.md`
- `SECURITY.md`

# UPKP Coach — Final Rebuild Candidate

This rebuild centers the product on guided learning and credible Mastery Badges.

**Primary UX:** Beranda → Belajar → Try Out → Progress.

**TPA goal:** earn Verbal, Numerical, Logical, and Figural Mastery badges; all four produce a `TPA Ready` state.

Difficulty is now expressed as `Foundation / Standard / Exam / Hard / Expert`; Mastery cannot be earned by farming easy items.

See:
- `docs/FINAL_REBUILD_SPEC.md`
- `docs/MASTERY_BADGES.md`
- `docs/TPA_CONTENT_EXPANSION.md`
- `docs/REBUILD_CHANGELOG.md`

# UPKP Coach Final v1.0

Multi-user adaptive UPKP learning app built from the V2.4 trainer engine.

## Final product decisions

- **4 primary learner surfaces only:** Beranda, Belajar, Try Out, Progress.
- **2 learning tracks:** TPA and Substansi Kemenkeu.
- **Simple auth:** username + password. No email, OTP, or social login.
- Passwords are **Argon2id hashes**. Browser receives only an HttpOnly session cookie.
- Frontend: Next.js/React/TypeScript.
- Backend: FastAPI Python on Vercel Functions.
- Durable multi-user storage: Supabase Postgres.
- Existing Python question generators, verifier, adaptive learning, spaced review, exam telemetry, and 3-pass logic are preserved.

## UX principle

Complexity stays in the engine. The learner should normally do this:

`Login → Beranda → Today's Plan → Kerjakan → Post-mortem → Next plan`

Material, chapter drills, error review and detailed metrics are secondary surfaces inside Belajar/Progress instead of competing primary menu items.

## Local development

Python API uses SQLite locally when `DATABASE_URL` is absent.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
npm install
# Terminal 1
COOKIE_SECURE=0 uvicorn api.index:app --reload --port 8000

# Terminal 2
npm run dev
```

For API-only tests:

```bash
COOKIE_SECURE=0 pytest -q tests
```

## Production

Read `docs/DEPLOY_VERCEL_SUPABASE.md` from top to bottom. The SQL in `sql/001_init.sql` must be applied once before first registration.

## Security notes

- `DATABASE_URL` is server-only. Never prefix it with `NEXT_PUBLIC_`.
- Custom auth is intentionally username/password only.
- Login/register attempts have a Postgres-backed rate limit so it works across serverless instances.
- Mutating API calls reject foreign `Origin` headers.
- Question answers/explanations are never shipped before submission; Try Out feedback is deferred.
- Admin can disable an account or reset a password but cannot recover/view an existing password.

## Source/provenance note

TPA material/generators were inherited from the supplied trainer baseline. Substansi content in the inherited baseline explicitly labels itself as general/official-source-based content rather than pages from the supplied book. Treat regulation/organization content as update-sensitive and verify it before a high-stakes exam cycle.
