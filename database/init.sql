-- Ethio-Council ECFE Digital Platform Database Initialization

-- Extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Roles enum
CREATE TYPE user_role AS ENUM (
    'SUPER_ADMIN',
    'NATIONAL_ADMIN',
    'REGIONAL_ADMIN',
    'ZONAL_ADMIN',
    'LOCAL_ADMIN',
    'DENOMINATION_ADMIN',
    'VIEWER'
);

CREATE TYPE member_status AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'PENDING');
CREATE TYPE crisis_severity AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE crisis_status AS ENUM ('OPEN', 'ACKNOWLEDGED', 'RESPONDING', 'RESOLVED', 'CLOSED');

-- Denominations (ECFE member organizations)
CREATE TABLE IF NOT EXISTS denominations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL UNIQUE,
    name_am VARCHAR(200),
    abbreviation VARCHAR(20),
    founded_year INTEGER,
    headquarters_city VARCHAR(100),
    website VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Administrative Regions (Ethiopia's 12 regions + 2 city administrations)
CREATE TABLE IF NOT EXISTS regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    name_am VARCHAR(100),
    code VARCHAR(10) UNIQUE,
    boundary GEOMETRY(MULTIPOLYGON, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region_id UUID NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    name_am VARCHAR(100),
    code VARCHAR(10),
    boundary GEOMETRY(MULTIPOLYGON, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(region_id, name)
);

CREATE TABLE IF NOT EXISTS woredas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    name_am VARCHAR(100),
    code VARCHAR(10),
    boundary GEOMETRY(MULTIPOLYGON, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(zone_id, name)
);

-- Users (platform users with role-based access)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(200) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'VIEWER',
    denomination_id UUID REFERENCES denominations(id) ON DELETE SET NULL,
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Churches (local congregations)
CREATE TABLE IF NOT EXISTS churches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    denomination_id UUID NOT NULL REFERENCES denominations(id) ON DELETE CASCADE,
    woreda_id UUID REFERENCES woredas(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    name_am VARCHAR(200),
    pastor_name VARCHAR(200),
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    location GEOMETRY(POINT, 4326),
    member_count INTEGER DEFAULT 0,
    established_year INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Members
CREATE TABLE IF NOT EXISTS members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    church_id UUID NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    denomination_id UUID REFERENCES denominations(id) ON DELETE SET NULL,
    full_name VARCHAR(200) NOT NULL,
    full_name_am VARCHAR(200),
    gender VARCHAR(10),
    date_of_birth DATE,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    location GEOMETRY(POINT, 4326),
    status member_status DEFAULT 'ACTIVE',
    baptism_date DATE,
    membership_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Crisis Reports
CREATE TABLE IF NOT EXISTS crisis_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reporter_id UUID REFERENCES users(id) ON DELETE SET NULL,
    church_id UUID REFERENCES churches(id) ON DELETE SET NULL,
    region_id UUID REFERENCES regions(id) ON DELETE SET NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    severity crisis_severity NOT NULL DEFAULT 'MEDIUM',
    status crisis_status NOT NULL DEFAULT 'OPEN',
    location GEOMETRY(POINT, 4326),
    affected_count INTEGER DEFAULT 0,
    response_notes TEXT,
    resolved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for spatial and foreign key lookups
CREATE INDEX IF NOT EXISTS idx_churches_location ON churches USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_members_location ON members USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_crisis_location ON crisis_reports USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_churches_denomination ON churches(denomination_id);
CREATE INDEX IF NOT EXISTS idx_members_church ON members(church_id);
CREATE INDEX IF NOT EXISTS idx_crisis_region ON crisis_reports(region_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- ============================================================
-- SEED DATA
-- ============================================================

-- ECFE Member Denominations
INSERT INTO denominations (name, name_am, abbreviation, founded_year, headquarters_city, is_active) VALUES
    ('Ethiopian Kale Heywet Church', 'ኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን', 'EKHC', 1952, 'Addis Ababa', TRUE),
    ('Ethiopian Evangelical Church Mekane Yesus', 'ኢትዮጵያ ወንጌላዊት ቤተ ክርስቲያን መካነ ኢየሱስ', 'EECMY', 1959, 'Addis Ababa', TRUE),
    ('Ethiopian Full Gospel Believers Church', 'ሙሉ ወንጌል አማኞች ቤተ ክርስቲያን', 'FGBC', 1967, 'Addis Ababa', TRUE),
    ('Ethiopian Apostolic Church', 'ኢትዮጵያ አፖስቶሊክ ቤተ ክርስቲያን', 'EAC', 1960, 'Addis Ababa', TRUE),
    ('Assemblies of God Ethiopia', 'አሰምብሊ ኦፍ ጎድ ኢትዮጵያ', 'AGE', 1960, 'Addis Ababa', TRUE),
    ('Ethiopian Pentecostal Church', 'ኢትዮጵያ ጴንጤቆስጤ ቤተ ክርስቲያን', 'EPC', 1970, 'Addis Ababa', TRUE),
    ('Seventh-day Adventist Church Ethiopia', 'ሰንበት አድቬንቲስት ቤተ ክርስቲያን', 'SDACE', 1907, 'Addis Ababa', TRUE),
    ('Ethiopian Baptist Church', 'ኢትዮጵያ ባፕቲስት ቤተ ክርስቲያን', 'EBC', 1972, 'Addis Ababa', TRUE)
ON CONFLICT (name) DO NOTHING;

-- Administrative Regions of Ethiopia
INSERT INTO regions (name, name_am, code) VALUES
    ('Addis Ababa City Administration', 'አዲስ አበባ ከተማ አስተዳደር', 'AA'),
    ('Oromia', 'ኦሮሚያ', 'OR'),
    ('Amhara', 'አማራ', 'AM'),
    ('Tigray', 'ትግራይ', 'TI'),
    ('Sidama', 'ሲዳማ', 'SI'),
    ('Southern Ethiopia', 'ደቡብ ኢትዮጵያ', 'SE'),
    ('SNNPR', 'ደቡብ ብሔሮች ብሔረሰቦችና ህዝቦች ክልል', 'SN'),
    ('Somali', 'ሶማሌ', 'SO'),
    ('Afar', 'አፋር', 'AF'),
    ('Harari', 'ሐረሪ', 'HA'),
    ('Dire Dawa City Administration', 'ድሬ ዳዋ ከተማ አስተዳደር', 'DD'),
    ('Benishangul-Gumuz', 'ቤኒሻንጉል ጉሙዝ', 'BG'),
    ('Gambela', 'ጋምቤላ', 'GA'),
    ('Central Ethiopia', 'መካከለኛ ኢትዮጵያ', 'CE')
ON CONFLICT (name) DO NOTHING;

-- Default SUPER_ADMIN user (password: Admin@2024!)
INSERT INTO users (email, full_name, hashed_password, role, is_active, is_verified) VALUES
    (
        'superadmin@ecfe.et',
        'ECFE Super Administrator',
        '$2b$12$5dNEeBq2d8ZPZnvN/53G2.glN8EflfL.2U5B0Xem3b23fhAvsOaHK',
        'SUPER_ADMIN',
        TRUE,
        TRUE
    )
ON CONFLICT (email) DO NOTHING;
