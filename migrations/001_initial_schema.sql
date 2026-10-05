-- ULPF PostgreSQL Schema — Migration 001
-- Run once on a fresh database. Safe to re-run (uses IF NOT EXISTS / CREATE EXTENSION IF NOT EXISTS).

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── raw_events ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS raw_events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    received_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_format   VARCHAR(32) NOT NULL,
    source_file     TEXT,
    raw_data        TEXT NOT NULL,
    sha256_hash     CHAR(64) NOT NULL,
    batch_id        UUID
);

CREATE INDEX IF NOT EXISTS idx_raw_events_batch_id    ON raw_events(batch_id);
CREATE INDEX IF NOT EXISTS idx_raw_events_received_at ON raw_events(received_at);
CREATE INDEX IF NOT EXISTS idx_raw_events_sha256      ON raw_events(sha256_hash);

-- ── normalized_events ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS normalized_events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    raw_event_id    UUID NOT NULL REFERENCES raw_events(id) ON DELETE CASCADE,
    normalized_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_format   VARCHAR(32) NOT NULL,
    ocsf_json       JSONB NOT NULL,
    severity_id     SMALLINT,
    activity_id     SMALLINT,
    src_ip          INET,
    dst_ip          INET,
    event_time      TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_norm_raw_event_id ON normalized_events(raw_event_id);
CREATE INDEX IF NOT EXISTS idx_norm_severity     ON normalized_events(severity_id);
CREATE INDEX IF NOT EXISTS idx_norm_activity     ON normalized_events(activity_id);
CREATE INDEX IF NOT EXISTS idx_norm_src_ip       ON normalized_events(src_ip);
CREATE INDEX IF NOT EXISTS idx_norm_event_time   ON normalized_events(event_time);

-- ── integrity_batches ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS integrity_batches (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_count             INTEGER NOT NULL,
    merkle_root             CHAR(64) NOT NULL,
    blockchain_block_index  BIGINT,
    blockchain_block_hash   CHAR(64)
);

-- ── raw_batch_payloads ────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS raw_batch_payloads (
    batch_id        UUID PRIMARY KEY REFERENCES integrity_batches(id) ON DELETE CASCADE,
    raw_payload     TEXT NOT NULL,
    sha256_hash     CHAR(64) NOT NULL
);

-- ── tamper_checks ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tamper_checks (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    checked_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    raw_event_id            UUID NOT NULL REFERENCES raw_events(id),
    stored_hash             CHAR(64) NOT NULL,
    recomputed_hash         CHAR(64) NOT NULL,
    batch_id                UUID,
    blockchain_block_index  BIGINT,
    is_tampered             BOOLEAN NOT NULL,
    detail                  TEXT
);

CREATE INDEX IF NOT EXISTS idx_tamper_raw_event_id ON tamper_checks(raw_event_id);
