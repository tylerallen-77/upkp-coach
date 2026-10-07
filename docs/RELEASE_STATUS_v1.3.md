# UPKP Coach v1.3 — Public-Ready Release Candidate

Date: 2026-10-07

## Source release status
**PASS** — ready for deployment to a Vercel Preview environment backed by Supabase.

### Verified locally
- 34/34 automated tests PASS
- Python compile PASS
- TS/TSX syntax parse PASS (11 files)
- baseline content stress: 1,875 sampled, 0 hard validity issues
- advanced L4/L5 stress: 1,080 sampled, 0 hard validity issues, 23 archetypes
- answer-key secrecy tests PASS
- multi-user isolation tests PASS
- cross-site mutation rejection PASS
- rate-limited public actions implemented
- reserved-admin takeover blocked
- self-service account deletion PASS
- question reporting + 3-user auto-quarantine PASS
- population difficulty calibration PASS
- schema-aware health check PASS

### Public-facing product state
- 4 learner destinations only: Beranda / Belajar / Try Out / Progress
- TPA Mastery badges: Verbal / Numerical / Logical / Figural
- 4/4 -> internal `TPA Ready`
- first diagnostic spans Foundation / Standard / Exam
- guided sessions adapt to gaps, maintenance, and Hard transfer
- TPA material expanded beyond the uploaded baseline using external reasoning constructs; authored questions remain original
- Substansi remains visible but labelled Beta pending its own regulatory provenance audit

## External deployment gates still required
These cannot be truthfully passed without the user's real cloud project:
1. CI/Vercel `npm install`
2. `npm run typecheck`
3. `npm run build`
4. Supabase migrations applied
5. `/api/health` returns 200 against real Supabase
6. preview smoke on text/table/figural questions
7. progress persists after browser refresh
8. admin bootstrap/login verified
9. security response headers verified on Preview
10. promote Preview to Production

Do not call a production URL launched until all ten external gates pass.
