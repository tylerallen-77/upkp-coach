-- UPKP Coach v1.3.3 structural foundation
-- Optional explicit migration. The backend also creates this table lazily with IF NOT EXISTS.
CREATE TABLE IF NOT EXISTS admin_audit_log (
  id bigserial PRIMARY KEY,
  actor_user_id text NOT NULL,
  action text NOT NULL,
  target_type text NOT NULL,
  target_id text NOT NULL,
  detail text NOT NULL DEFAULT '{}',
  created_at double precision NOT NULL
);
CREATE INDEX IF NOT EXISTS admin_audit_created_idx ON admin_audit_log(created_at DESC);
