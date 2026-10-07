-- UPKP Coach public hardening migration
ALTER TABLE attempts ADD COLUMN IF NOT EXISTS item_signature text;
CREATE INDEX IF NOT EXISTS attempts_item_signature_idx ON attempts(item_signature);

CREATE TABLE IF NOT EXISTS question_reports (
  id bigserial PRIMARY KEY,
  user_id text NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  item_signature text NOT NULL,
  question_id text NOT NULL,
  reason text NOT NULL,
  detail text NOT NULL DEFAULT '',
  created_at double precision NOT NULL,
  UNIQUE(user_id,item_signature)
);
CREATE INDEX IF NOT EXISTS question_reports_signature_idx ON question_reports(item_signature,created_at DESC);

CREATE TABLE IF NOT EXISTS content_quarantine (
  item_signature text PRIMARY KEY,
  reason text NOT NULL,
  report_count integer NOT NULL DEFAULT 0,
  active smallint NOT NULL DEFAULT 1,
  created_at double precision NOT NULL,
  updated_at double precision NOT NULL
);

CREATE TABLE IF NOT EXISTS population_item_stats (
  item_signature text PRIMARY KEY,
  skill text NOT NULL,
  authored_level integer NOT NULL,
  attempts integer NOT NULL DEFAULT 0,
  correct integer NOT NULL DEFAULT 0,
  skipped integer NOT NULL DEFAULT 0,
  elapsed_sum_ms bigint NOT NULL DEFAULT 0,
  answer_changes integer NOT NULL DEFAULT 0,
  high_confidence_wrong integer NOT NULL DEFAULT 0,
  updated_at double precision NOT NULL
);
