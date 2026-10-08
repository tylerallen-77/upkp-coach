# v1.3.3 Structural Foundation

## User-facing information architecture
- Top-level navigation: Beranda, Belajar, Try Out, Progress, Account.
- Account owns profile/data actions; Progress contains only learning analytics/mastery.
- Reset Riwayat Pembelajaran preserves the account/password while clearing attempts, learning sessions, active question tokens, adaptive progress and mastery evidence.
- Delete Account remains a distinct destructive action.

## Symmetric UPKP mastery
TPA retains four badges: Verbal, Numerical, Logical, Figural.

Substansi now has six badges:
1. Etika PNS
2. Wawasan Kebangsaan
3. Nilai Kemenkeu
4. Kepegawaian
5. Keuangan Negara
6. Struktur Kemenkeu

TPA mastery includes a speed gate. Substansi intentionally does not: its gate prioritizes coverage, accuracy, Exam-level evidence, retention across multiple days, and a fresh Mastery Challenge.

UPKP Ready requires both TPA Ready and Substansi Ready.

## Admin data console
Admin Console is a guarded production data workspace, not a raw SQL editor. It supports:
- user inspect / disable-enable / password reset / learning-history reset
- session and recent-attempt inspection
- question report and quarantine management
- empirical difficulty calibration
- database table counts
- maintenance cleanup
- audit log for admin mutations

Credentials, password hashes, auth tokens, environment secrets and arbitrary SQL are never exposed in the UI.

## Audit schema
The app lazily creates admin_audit_log with CREATE TABLE IF NOT EXISTS when the admin audit path is first used. sql/003_admin_audit.sql is retained for explicit/reproducible migration workflows.
