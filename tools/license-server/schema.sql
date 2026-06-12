-- License Activation System — PostgreSQL Schema

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    name        TEXT,
    created_at  TIMESTAMPTZ DEFAULT now(),
    updated_at  TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE licenses (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_key   TEXT UNIQUE NOT NULL,          -- e.g. MEM-PRO-XXXX-XXXX
    user_id       UUID REFERENCES users(id),
    tier          TEXT NOT NULL CHECK (tier IN ('trial', 'pro', 'enterprise')),
    max_machines  INT DEFAULT 1,                 -- 1 for trial, 3 for pro, unlimited for enterprise
    issued_at     TIMESTAMPTZ DEFAULT now(),
    expires_at    TIMESTAMPTZ,                   -- NULL for pro/enterprise (never expires)
    revoked       BOOLEAN DEFAULT false,
    metadata      JSONB DEFAULT '{}'
);

CREATE TABLE machines (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fingerprint     TEXT NOT NULL,               -- SHA-256 of machine ID
    hostname        TEXT,
    platform        TEXT,
    first_seen      TIMESTAMPTZ DEFAULT now(),
    last_seen       TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE activations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    license_id      UUID REFERENCES licenses(id) ON DELETE CASCADE,
    machine_id      UUID REFERENCES machines(id) ON DELETE CASCADE,
    token           TEXT NOT NULL,               -- signed JWT
    activated_at    TIMESTAMPTZ DEFAULT now(),
    last_verified   TIMESTAMPTZ DEFAULT now(),
    active          BOOLEAN DEFAULT true,
    UNIQUE(license_id, machine_id)
);

CREATE INDEX idx_licenses_key ON licenses(license_key);
CREATE INDEX idx_licenses_user ON licenses(user_id);
CREATE INDEX idx_activations_license ON activations(license_id);
CREATE INDEX idx_activations_machine ON activations(machine_id);
CREATE INDEX idx_machines_fingerprint ON machines(fingerprint);

-- Helper: generate a license key
CREATE OR REPLACE FUNCTION generate_license_key(prefix TEXT DEFAULT 'MEM')
RETURNS TEXT AS $$
DECLARE
    part1 TEXT;
    part2 TEXT;
    part3 TEXT;
BEGIN
    part1 := upper(substr(md5(random()::text), 1, 4));
    part2 := upper(substr(md5(random()::text), 1, 4));
    part3 := upper(substr(md5(random()::text), 1, 4));
    RETURN prefix || '-TRIAL-' || part1 || '-' || part2 || '-' || part3;
END;
$$ LANGUAGE plpgsql;
