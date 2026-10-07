# UPKP Coach Final v1.0 — Product Spec

## Goal
A guided multi-user exam coach for UPKP V that minimizes learner choice overload while preserving advanced adaptive diagnostics behind the scenes.

## Learner navigation
1. **Beranda** — today's plan for TPA and Substansi, readiness, recent sessions.
2. **Belajar** — guided session by default; material and chapter drill are optional secondary controls.
3. **Try Out** — track-specific simulation with deferred feedback and 3-pass strategy.
4. **Progress** — detailed metrics, micro-skill map, review/error queue.

## Tracks
### TPA
Verbal, Numerical, Figural. Existing V2.4 adaptive micro-skill engine retained.

### Substansi Kemenkeu
Etika PNS, Wawasan Kebangsaan, Nilai-Nilai Kementerian Keuangan, Tata Aturan Kepegawaian, Pengelolaan Keuangan Negara, Struktur Kementerian Keuangan.

Substansi uses the same attempt telemetry, mastery, spaced review and guided prescription machinery as TPA.

## Auth
- username: lower-case canonical form, 3–24 chars, `[a-z0-9_]`
- password: min 8 chars
- Argon2id server-side hashing
- opaque random session token; SHA-256 token hash stored in DB
- 30-day session by default
- no email recovery in v1; admin-reset only

## Multi-user isolation
Every learning session, attempt and question token is scoped by `user_id`. API reads are always derived from authenticated user identity, never a client-provided user ID.

## Question rendering
Renderer supports:
- plain/rich multiline text
- pipe-style tables
- stem SVG
- option SVGs
- normal text options

This fixes the live-alpha figural and statistics-table rendering defects.

## Adaptive engine
Retained from V2.1–V2.4:
- clean/slow/hesitation/wrong/high-confidence-wrong classifications
- personal speed targets
- mastery states
- spaced review stages
- daily prescription
- session post-mortem
- 3-pass exam behavior

## Non-goals in v1
- public leaderboard
- email/phone identity
- social login
- payments
- chat/community
- pretending internal packet question counts are official exam counts
