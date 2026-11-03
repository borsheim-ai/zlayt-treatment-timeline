-- T-050: item/record ids are short per-case ids (r1, e5, f_gap_r6_r7); uniqueness is (case_id, id), so many cases share one file.
-- ADR-002: seven tables, one SQLite file. All offsets are absolute into cases.raw_text. Money is integer cents.
-- *_json columns hold JSON text. Times are epoch seconds (REAL) supplied by the caller's injectable now().
CREATE TABLE IF NOT EXISTS cases (
  id TEXT PRIMARY KEY, name TEXT, source TEXT CHECK (source IN ('paste','sample')) DEFAULT 'paste',
  raw_text TEXT NOT NULL, text_sha256 TEXT,
  status TEXT NOT NULL DEFAULT 'ingested' CHECK (status IN ('ingested','running','ready','failed')),
  stage TEXT, error TEXT, backend TEXT, demo_mode INTEGER DEFAULT 0, config_json TEXT,
  injection_records_json TEXT, created_at REAL NOT NULL, run_started_at REAL, run_finished_at REAL
);
CREATE TABLE IF NOT EXISTS records (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), seq INTEGER, char_start INTEGER, char_end INTEGER,
  date_header_start INTEGER, date_header_end INTEGER, source_header_start INTEGER, source_header_end INTEGER,
  source_label TEXT, date_raw TEXT, date_iso TEXT,
  date_status TEXT CHECK (date_status IN ('parsed','ambiguous','missing','confirmed')),
  date_candidates_json TEXT, duplicate_of TEXT, injection_tag INTEGER DEFAULT 0, encounter INTEGER DEFAULT 1,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS entries (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, seq INTEGER, date_iso TEXT,
  provider TEXT, summary TEXT, excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS amounts (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id), record_ids_json TEXT, entry_id TEXT,
  text TEXT, value_cents INTEGER, kind TEXT CHECK (kind IN ('charge','rate','estimate','damages','unclear')),
  excerpt TEXT, excerpt_start INTEGER, excerpt_end INTEGER, duplicate_note TEXT,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
CREATE TABLE IF NOT EXISTS flags (
  id TEXT NOT NULL, case_id TEXT NOT NULL REFERENCES cases(id),
  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
  state TEXT, state_reasons_json TEXT,
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
  edited_json TEXT, ladder_json TEXT, updated_at REAL,
  PRIMARY KEY (case_id, id)
);
-- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
CREATE TABLE IF NOT EXISTS llm_calls (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  role TEXT CHECK (role IN ('generator','judge')), step TEXT, backend TEXT, model TEXT,
  prompt_version TEXT, prompt_sha256 TEXT, system_text TEXT, user_text TEXT, response_raw TEXT,
  parsed_ok INTEGER, verdict TEXT, attempt INTEGER DEFAULT 1, latency_ms INTEGER, cost_usd REAL,
  tokens_in INTEGER, tokens_out INTEGER, recorded_from_json TEXT, error TEXT, created_at REAL
);
CREATE TABLE IF NOT EXISTS review_events (
  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry','reclassify','rejudge')),
  before_json TEXT, after_json TEXT, at REAL
);
CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
