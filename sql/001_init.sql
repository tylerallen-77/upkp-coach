create table if not exists users (
  id text primary key,
  username text not null,
  password_hash text not null,
  role text not null default 'user' check (role in ('user','admin')),
  disabled smallint not null default 0,
  created_at double precision not null
);
create unique index if not exists users_username_lower_uq on users(lower(username));
create table if not exists auth_sessions (
  token_hash text primary key,
  user_id text not null references users(id) on delete cascade,
  created_at double precision not null,
  expires_at double precision not null
);
create index if not exists auth_sessions_user_idx on auth_sessions(user_id);
create table if not exists learning_sessions (
  id text primary key,
  user_id text not null references users(id) on delete cascade,
  track text not null check (track in ('tpa','substansi')),
  kind text not null,
  title text not null,
  started double precision not null,
  ended double precision,
  meta text not null default '{}',
  summary text not null default '{}'
);
create index if not exists learning_sessions_user_idx on learning_sessions(user_id,started desc);
create table if not exists attempts (
  id bigserial primary key,
  user_id text not null references users(id) on delete cascade,
  attempt_key text unique,
  ts double precision not null,
  session_id text not null,
  question_id text not null,
  track text not null,
  skill text not null,
  item_signature text,
  payload text not null
);
create index if not exists attempts_user_track_idx on attempts(user_id,track,id);
create index if not exists attempts_item_signature_idx on attempts(item_signature);
create table if not exists question_tokens (
  token text primary key,
  user_id text not null references users(id) on delete cascade,
  session_id text not null,
  payload text not null,
  created double precision not null,
  used smallint not null default 0
);
create index if not exists question_tokens_user_idx on question_tokens(user_id,created);
create table if not exists auth_rate_limits (
  bucket text primary key,
  window_start double precision not null,
  count integer not null default 0
);

create table if not exists question_reports (
  id bigserial primary key,
  user_id text not null references users(id) on delete cascade,
  item_signature text not null,
  question_id text not null,
  reason text not null,
  detail text not null default '',
  created_at double precision not null,
  unique(user_id,item_signature)
);
create index if not exists question_reports_signature_idx on question_reports(item_signature,created_at desc);
create table if not exists content_quarantine (
  item_signature text primary key, reason text not null, report_count integer not null default 0,
  active smallint not null default 1, created_at double precision not null, updated_at double precision not null
);
create table if not exists population_item_stats (
  item_signature text primary key, skill text not null, authored_level integer not null,
  attempts integer not null default 0, correct integer not null default 0, skipped integer not null default 0,
  elapsed_sum_ms bigint not null default 0, answer_changes integer not null default 0,
  high_confidence_wrong integer not null default 0, updated_at double precision not null
);
