CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;

DO $$ BEGIN
    CREATE TYPE user_role AS ENUM ('SUPER_ADMIN', 'NATIONAL_ADMIN', 'REGIONAL_ADMIN', 'FIELD_OFFICER', 'CHURCH_LEADER', 'DIASPORA_REP', 'VIEWER');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS woredas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    zone_id UUID NOT NULL REFERENCES zones(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS kebeles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    woreda_id UUID NOT NULL REFERENCES woredas(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    phone VARCHAR(50),
    role user_role NOT NULL DEFAULT 'VIEWER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT TRUE,
    language_preference VARCHAR(8) NOT NULL DEFAULT 'en',
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    zone_id UUID REFERENCES zones(id) ON DELETE SET NULL,
    woreda_id UUID REFERENCES woredas(id) ON DELETE SET NULL,
    kebele_id UUID REFERENCES kebeles(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS denominations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    abbreviation VARCHAR(50),
    founded_year INTEGER,
    headquarters_region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    description TEXT,
    website VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS churches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    denomination_id UUID NOT NULL REFERENCES denominations(id) ON DELETE RESTRICT,
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    zone_id UUID REFERENCES zones(id) ON DELETE SET NULL,
    woreda_id UUID REFERENCES woredas(id) ON DELETE SET NULL,
    kebele_id UUID REFERENCES kebeles(id) ON DELETE SET NULL,
    community VARCHAR(255),
    address TEXT,
    year_established INTEGER,
    membership_size INTEGER,
    languages_used TEXT[] DEFAULT ARRAY[]::TEXT[],
    service_schedules JSONB NOT NULL DEFAULT '[]'::jsonb,
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verification_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ministries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    church_id UUID REFERENCES churches(id) ON DELETE CASCADE,
    denomination_id UUID REFERENCES denominations(id) ON DELETE SET NULL,
    ministry_type VARCHAR(100) NOT NULL,
    description TEXT,
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    zone_id UUID REFERENCES zones(id) ON DELETE SET NULL,
    woreda_id UUID REFERENCES woredas(id) ON DELETE SET NULL,
    kebele_id UUID REFERENCES kebeles(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS church_leaders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    church_id UUID NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    bio TEXT,
    profile_image_url VARCHAR(500),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diaspora_communities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    membership_count INTEGER NOT NULL DEFAULT 0,
    denomination_id UUID REFERENCES denominations(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS diaspora_partnerships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    diaspora_community_id UUID NOT NULL REFERENCES diaspora_communities(id) ON DELETE CASCADE,
    church_id UUID NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    partnership_type VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS field_registrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    church_id UUID NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    field_officer_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    gps_lat DOUBLE PRECISION NOT NULL,
    gps_lng DOUBLE PRECISION NOT NULL,
    gps_accuracy DOUBLE PRECISION,
    gps_timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    location geometry(Point, 4326),
    device_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    photos JSONB NOT NULL DEFAULT '[]'::jsonb,
    registration_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    incident_type VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'reported',
    location geometry(Point, 4326),
    gps_lat DOUBLE PRECISION,
    gps_lng DOUBLE PRECISION,
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    zone_id UUID REFERENCES zones(id) ON DELETE SET NULL,
    woreda_id UUID REFERENCES woredas(id) ON DELETE SET NULL,
    affected_population INTEGER,
    reported_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS volunteers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    skills TEXT[] DEFAULT ARRAY[]::TEXT[],
    availability VARCHAR(100),
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS relief_distributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    quantity NUMERIC(12,2) NOT NULL,
    unit VARCHAR(50) NOT NULL,
    distribution_date DATE NOT NULL,
    location VARCHAR(255),
    status VARCHAR(50) NOT NULL DEFAULT 'planned',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS volunteer_deployments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    volunteer_id UUID NOT NULL REFERENCES volunteers(id) ON DELETE CASCADE,
    role VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'assigned',
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO regions (name, code) VALUES
    ('Addis Ababa', 'AA'),
    ('Oromia', 'OR'),
    ('Amhara', 'AM'),
    ('SNNPR', 'SN')
ON CONFLICT (code) DO NOTHING;

INSERT INTO zones (name, code, region_id) VALUES
    ('Addis Ketema Zone', 'AA-AK', (SELECT id FROM regions WHERE code = 'AA')),
    ('Arsi Zone', 'OR-AR', (SELECT id FROM regions WHERE code = 'OR')),
    ('North Shewa', 'AM-NS', (SELECT id FROM regions WHERE code = 'AM')),
    ('Gamo Zone', 'SN-GA', (SELECT id FROM regions WHERE code = 'SN'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO woredas (name, code, zone_id) VALUES
    ('Addis Ketema', 'AA-AK-01', (SELECT id FROM zones WHERE code = 'AA-AK')),
    ('Asella', 'OR-AR-01', (SELECT id FROM zones WHERE code = 'OR-AR')),
    ('Debre Birhan', 'AM-NS-01', (SELECT id FROM zones WHERE code = 'AM-NS')),
    ('Arba Minch Zuria', 'SN-GA-01', (SELECT id FROM zones WHERE code = 'SN-GA'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO kebeles (name, code, woreda_id) VALUES
    ('Kebele 01', 'AA-AK-01-01', (SELECT id FROM woredas WHERE code = 'AA-AK-01')),
    ('Kebele 02', 'OR-AR-01-02', (SELECT id FROM woredas WHERE code = 'OR-AR-01')),
    ('Kebele 03', 'AM-NS-01-03', (SELECT id FROM woredas WHERE code = 'AM-NS-01')),
    ('Kebele 04', 'SN-GA-01-04', (SELECT id FROM woredas WHERE code = 'SN-GA-01'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO denominations (name, abbreviation, founded_year, headquarters_region_id, description, website) VALUES
    ('Ethiopian Kale Heywet Church', 'EKHC', 1927, (SELECT id FROM regions WHERE code = 'AA'), 'Nationwide evangelical denomination.', 'https://www.ekhc.org'),
    ('Ethiopian Evangelical Church Mekane Yesus', 'EECMY', 1959, (SELECT id FROM regions WHERE code = 'AA'), 'Lutheran evangelical denomination.', 'https://www.eecmy.org'),
    ('Ethiopian Baptist Church Fellowship', 'EBCF', 1973, (SELECT id FROM regions WHERE code = 'AA'), 'Baptist fellowship serving churches across Ethiopia.', NULL),
    ('Ethiopian Full Gospel Believers Church', 'EFGBC', 1967, (SELECT id FROM regions WHERE code = 'AA'), 'Pentecostal denomination with national presence.', NULL),
    ('Assemblies of God Ethiopia', 'AGE', 1950, (SELECT id FROM regions WHERE code = 'AA'), 'Assemblies of God movement in Ethiopia.', NULL)
ON CONFLICT (name) DO NOTHING;

INSERT INTO users (email, username, password_hash, full_name, role, is_active, is_verified, language_preference)
VALUES ('admin@ecfe.org', 'admin', '$2b$12$y5Cd5/Dydt.KL.f33vS8ieekBVRzEtCXFtHz4Bzdk1uDt0p6VS4/S', 'ECFE Platform Administrator', 'SUPER_ADMIN', TRUE, TRUE, 'en')
ON CONFLICT (email) DO NOTHING;
