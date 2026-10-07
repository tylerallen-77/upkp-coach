# UX / Session Hotfix v1.3.1

Launch blockers fixed from first Vercel dogfood:

1. Mobile logout
   - `Keluar` is now visible in the mobile header.
   - Logout is blocked while a learning session is active to avoid silent data loss.

2. Start Diagnostic / session-launch responsiveness
   - Session launch shows `Menyiapkan sesi…`.
   - Backend/API errors are surfaced in a visible dismissible banner instead of being silently swallowed.
   - Local API regression confirms a fresh user can create the 15-question diagnostic.

3. Safe session exit
   - Every question session has a persistent `← Keluar sesi` action.
   - Exit asks for confirmation.
   - Already-submitted answers remain stored.
   - The session is closed with `abandoned=true`, so it appears in session history instead of vanishing.

4. Accidental navigation protection
   - Primary nav is blocked while a session is active; user is directed to `Keluar sesi`.
   - Browser unload/back gets a native unsaved-session warning where the browser supports it.

5. Resume protection
   - Active session bundle is stored locally.
   - Runner position/pass/deferred queue/selection/feedback/timer state are persisted per session.
   - Reopening the app can restore an unfinished active session rather than starting from zero.
   - Server remains source-of-truth for submitted attempts.

Verification:
- 35/35 Python/API tests PASS.
- Python compile PASS.
- Source assertions PASS for mobile logout, launch errors, session exit, resume state, and nav guard.
