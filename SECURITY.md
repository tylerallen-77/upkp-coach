# Security notes

UPKP Coach stores username/password credentials and learning telemetry.

- Passwords are hashed with Argon2id and are never stored as plaintext.
- Production sessions use Secure, HttpOnly, SameSite cookies.
- State-changing requests reject cross-site traffic using Origin / Sec-Fetch-Site checks.
- Login, registration, session creation, answering and reporting are rate-limited.
- The admin username is reserved; admin privilege is bootstrapped directly against the database.
- Answer keys and explanations stay server-side until practice feedback is allowed.
- Try Out and Mastery Challenge defer answer feedback.
- Security headers include CSP, HSTS, frame denial, content-type sniff protection and restrictive permissions policy.
- Never commit DATABASE_URL or production credentials.

If a learner account is compromised, disable it in Admin Console and reset its password. Password reset revokes existing sessions.
