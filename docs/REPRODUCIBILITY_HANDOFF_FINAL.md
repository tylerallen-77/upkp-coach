# Reproducibility Handoff — Final v1.0

## Baseline provenance
Final v1 is a forward migration of `UPKP_Coach_V2_4_PRE_HOSTING_READY`, preserving its Python question generators and adaptive learning modules.

## Major deltas
1. SQLite single-user persistence replaced by a dual adapter: local SQLite / production Postgres.
2. Custom username/password multi-user auth added.
3. All tokens/sessions/attempts scoped to authenticated user.
4. Substansi exposed as a real adaptive track instead of an empty UI toggle.
5. Primary navigation reduced to four learner choices.
6. Next.js/React frontend replaces the alpha vanilla SPA.
7. Rich question renderer fixes SVG options and pipe-table display.
8. Vercel/Supabase deployment contract added.

## Reproduce
```bash
pip install -r requirements.txt
npm install
COOKIE_SECURE=0 pytest -q tests
npm run build
```

Then apply `sql/001_init.sql` to a blank Postgres database and run the API with `DATABASE_URL` configured.

## Required release gates
- Python compileall PASS
- content/generator tests PASS
- multi-user API tests PASS
- Next production build PASS
- two-user isolation smoke test PASS against Postgres
- Try Out response contains no answer/explanation before session completion
- figural question and option SVGs render
- table question renders as HTML table
