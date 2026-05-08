-- ECFE Digital Platform Database Schema and Seed Data

DROP TABLE IF EXISTS relief_distributions CASCADE;
DROP TABLE IF EXISTS volunteer_deployments CASCADE;
DROP TABLE IF EXISTS volunteers CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;
DROP TABLE IF EXISTS registration_photos CASCADE;
DROP TABLE IF EXISTS field_registrations CASCADE;
DROP TABLE IF EXISTS diaspora_partnerships CASCADE;
DROP TABLE IF EXISTS diaspora_communities CASCADE;
DROP TABLE IF EXISTS church_leaders CASCADE;
DROP TABLE IF EXISTS ministries CASCADE;
DROP TABLE IF EXISTS churches CASCADE;
DROP TABLE IF EXISTS kebeles CASCADE;
DROP TABLE IF EXISTS woredas CASCADE;
DROP TABLE IF EXISTS zones CASCADE;
DROP TABLE IF EXISTS regions CASCADE;
DROP TABLE IF EXISTS denominations CASCADE;
DROP TABLE IF EXISTS users CASCADE;

DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS registration_status CASCADE;
DROP TYPE IF EXISTS incident_severity CASCADE;
DROP TYPE IF EXISTS incident_status CASCADE;
DROP TYPE IF EXISTS volunteer_status CASCADE;

CREATE TYPE user_role AS ENUM (
    'SUPER_ADMIN', 'NATIONAL_ADMIN', 'REGIONAL_ADMIN',
    'FIELD_OFFICER', 'CHURCH_LEADER', 'DIASPORA_REP', 'VIEWER'
);

CREATE TYPE registration_status AS ENUM ('PENDING', 'VERIFIED', 'REJECTED');
CREATE TYPE incident_severity AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL');
CREATE TYPE incident_status AS ENUM ('REPORTED', 'ACTIVE', 'CONTAINED', 'RESOLVED');
CREATE TYPE volunteer_status AS ENUM ('AVAILABLE', 'DEPLOYED', 'UNAVAILABLE');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'VIEWER',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE zones (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    region_id INTEGER NOT NULL REFERENCES regions(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE woredas (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    zone_id INTEGER NOT NULL REFERENCES zones(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE kebeles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    woreda_id INTEGER NOT NULL REFERENCES woredas(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE denominations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    founded_year INTEGER,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE churches (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    denomination_id INTEGER NOT NULL REFERENCES denominations(id),
    woreda_id INTEGER NOT NULL REFERENCES woredas(id),
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    established_year INTEGER,
    member_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE ministries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    church_id INTEGER NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    leader_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE church_leaders (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(100),
    church_id INTEGER NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    phone VARCHAR(50),
    email VARCHAR(255),
    ordained_year INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE diaspora_communities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    contact_person VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    member_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE diaspora_partnerships (
    id SERIAL PRIMARY KEY,
    community_id INTEGER NOT NULL REFERENCES diaspora_communities(id) ON DELETE CASCADE,
    church_id INTEGER NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    partnership_type VARCHAR(100),
    description TEXT,
    start_date TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE field_registrations (
    id SERIAL PRIMARY KEY,
    church_id INTEGER NOT NULL REFERENCES churches(id) ON DELETE CASCADE,
    field_officer_id INTEGER NOT NULL REFERENCES users(id),
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    altitude DOUBLE PRECISION,
    accuracy DOUBLE PRECISION,
    address TEXT,
    notes TEXT,
    status registration_status NOT NULL DEFAULT 'PENDING',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE registration_photos (
    id SERIAL PRIMARY KEY,
    registration_id INTEGER NOT NULL REFERENCES field_registrations(id) ON DELETE CASCADE,
    s3_key VARCHAR(500) NOT NULL,
    caption VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity incident_severity NOT NULL DEFAULT 'MEDIUM',
    status incident_status NOT NULL DEFAULT 'REPORTED',
    location VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    reported_by INTEGER NOT NULL REFERENCES users(id),
    woreda_id INTEGER REFERENCES woredas(id),
    affected_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE volunteers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    email VARCHAR(255),
    skills TEXT,
    church_id INTEGER REFERENCES churches(id),
    status volunteer_status NOT NULL DEFAULT 'AVAILABLE',
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE volunteer_deployments (
    id SERIAL PRIMARY KEY,
    volunteer_id INTEGER NOT NULL REFERENCES volunteers(id) ON DELETE CASCADE,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    deployed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    released_at TIMESTAMP,
    notes TEXT
);

CREATE TABLE relief_distributions (
    id SERIAL PRIMARY KEY,
    incident_id INTEGER NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    item_name VARCHAR(255) NOT NULL,
    quantity DOUBLE PRECISION NOT NULL,
    unit VARCHAR(50),
    distributed_to VARCHAR(255),
    distributed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    distributed_by INTEGER REFERENCES users(id),
    notes TEXT
);

INSERT INTO users (username, email, hashed_password, role, is_active) VALUES
    ('admin', 'admin@ecfe.org', '$2b$12$Sx1.LZfMzolDoX5Y7bDqTe3QZesGtYLCqsoIrIwO3lizvr.Wq4Ts6', 'SUPER_ADMIN', TRUE),
    ('field.officer', 'field.officer@ecfe.org', '$2b$12$Sx1.LZfMzolDoX5Y7bDqTe3QZesGtYLCqsoIrIwO3lizvr.Wq4Ts6', 'FIELD_OFFICER', TRUE),
    ('diaspora.rep', 'diaspora.rep@ecfe.org', '$2b$12$Sx1.LZfMzolDoX5Y7bDqTe3QZesGtYLCqsoIrIwO3lizvr.Wq4Ts6', 'DIASPORA_REP', TRUE);

INSERT INTO denominations (name, code, founded_year, description) VALUES
    ('Ethiopian Kale Heywet Church', 'EKHC', 1927, 'One of the largest evangelical denominations in Ethiopia.'),
    ('Ethiopian Evangelical Church Mekane Yesus', 'EECMY', 1959, 'National Lutheran church body and ECFE member denomination.'),
    ('Ethiopian Baptist Church Fellowship', 'EBCF', 1994, 'Baptist fellowship serving congregations across Ethiopia.'),
    ('Ethiopian Full Gospel Believers Church', 'EFGBC', 1969, 'Pentecostal denomination with strong urban and diaspora presence.'),
    ('Assemblies of God Ethiopia', 'AGE', 1940, 'Assemblies of God churches in Ethiopia.')
ON CONFLICT (code) DO NOTHING;

INSERT INTO regions (name, code) VALUES
    ('Addis Ababa', 'AA'),
    ('Oromia', 'OR'),
    ('Amhara', 'AM'),
    ('Central Ethiopia', 'CE')
ON CONFLICT (code) DO NOTHING;

INSERT INTO zones (name, code, region_id) VALUES
    ('Addis Ababa Central', 'AA-C', (SELECT id FROM regions WHERE code = 'AA')),
    ('East Shewa', 'OR-ES', (SELECT id FROM regions WHERE code = 'OR')),
    ('North Shewa', 'AM-NS', (SELECT id FROM regions WHERE code = 'AM')),
    ('Gurage', 'CE-GU', (SELECT id FROM regions WHERE code = 'CE'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO woredas (name, code, zone_id) VALUES
    ('Bole', 'AA-C-BO', (SELECT id FROM zones WHERE code = 'AA-C')),
    ('Adama', 'OR-ES-AD', (SELECT id FROM zones WHERE code = 'OR-ES')),
    ('Debre Birhan', 'AM-NS-DB', (SELECT id FROM zones WHERE code = 'AM-NS')),
    ('Wolkite', 'CE-GU-WK', (SELECT id FROM zones WHERE code = 'CE-GU'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO kebeles (name, code, woreda_id) VALUES
    ('Bole Medhanialem', 'AA-C-BO-01', (SELECT id FROM woredas WHERE code = 'AA-C-BO')),
    ('Adama 01', 'OR-ES-AD-01', (SELECT id FROM woredas WHERE code = 'OR-ES-AD')),
    ('Debre Birhan 03', 'AM-NS-DB-03', (SELECT id FROM woredas WHERE code = 'AM-NS-DB')),
    ('Wolkite 02', 'CE-GU-WK-02', (SELECT id FROM woredas WHERE code = 'CE-GU-WK'))
ON CONFLICT (code) DO NOTHING;

INSERT INTO churches (name, denomination_id, woreda_id, address, phone, email, established_year, member_count, is_active) VALUES
    (
        'Addis Hope Church',
        (SELECT id FROM denominations WHERE code = 'EKHC'),
        (SELECT id FROM woredas WHERE code = 'AA-C-BO'),
        'Bole Medhanialem, Addis Ababa',
        '+251911000101',
        'addis.hope@ecfe.org',
        2005,
        850,
        TRUE
    ),
    (
        'Adama Gospel Center',
        (SELECT id FROM denominations WHERE code = 'EECMY'),
        (SELECT id FROM woredas WHERE code = 'OR-ES-AD'),
        'Adama, Oromia',
        '+251911000102',
        'adama.gospel@ecfe.org',
        1998,
        620,
        TRUE
    ),
    (
        'Debre Birhan Fellowship',
        (SELECT id FROM denominations WHERE code = 'EBCF'),
        (SELECT id FROM woredas WHERE code = 'AM-NS-DB'),
        'Debre Birhan, Amhara',
        '+251911000103',
        'debrebirhan@ecfe.org',
        2011,
        410,
        TRUE
    ),
    (
        'Wolkite Revival Church',
        (SELECT id FROM denominations WHERE code = 'EFGBC'),
        (SELECT id FROM woredas WHERE code = 'CE-GU-WK'),
        'Wolkite, Central Ethiopia',
        '+251911000104',
        'wolkite.revival@ecfe.org',
        2014,
        530,
        TRUE
    );

INSERT INTO ministries (name, description, church_id, leader_name) VALUES
    ('Youth Discipleship', 'Youth discipleship and leadership development program.', (SELECT id FROM churches WHERE name = 'Addis Hope Church'), 'Pastor Hana Bekele'),
    ('Women Empowerment', 'Women mentorship, prayer, and economic empowerment ministry.', (SELECT id FROM churches WHERE name = 'Adama Gospel Center'), 'Sister Mulu Alemu'),
    ('Children Outreach', 'Weekend children outreach and Sunday school support.', (SELECT id FROM churches WHERE name = 'Debre Birhan Fellowship'), 'Teacher Samuel Tadesse');

INSERT INTO church_leaders (full_name, title, church_id, phone, email, ordained_year, is_active) VALUES
    ('Rev. Hana Bekele', 'Senior Pastor', (SELECT id FROM churches WHERE name = 'Addis Hope Church'), '+251911200001', 'hana.bekele@ecfe.org', 2010, TRUE),
    ('Rev. Daniel Girma', 'Lead Pastor', (SELECT id FROM churches WHERE name = 'Adama Gospel Center'), '+251911200002', 'daniel.girma@ecfe.org', 2006, TRUE),
    ('Pastor Ruth Worku', 'Associate Pastor', (SELECT id FROM churches WHERE name = 'Wolkite Revival Church'), '+251911200003', 'ruth.worku@ecfe.org', 2016, TRUE);

INSERT INTO diaspora_communities (name, country, city, contact_person, contact_email, contact_phone, member_count, is_active) VALUES
    ('ECFE North America Network', 'United States', 'Washington, DC', 'Alemayehu Desta', 'na.network@ecfe.org', '+12025550101', 340, TRUE),
    ('ECFE Europe Fellowship', 'Germany', 'Frankfurt', 'Bethlehem Fikru', 'europe.fellowship@ecfe.org', '+49695550102', 180, TRUE);

INSERT INTO diaspora_partnerships (community_id, church_id, partnership_type, description, start_date, is_active) VALUES
    (
        (SELECT id FROM diaspora_communities WHERE name = 'ECFE North America Network'),
        (SELECT id FROM churches WHERE name = 'Addis Hope Church'),
        'Mission Support',
        'Supports leadership development, literature, and youth conferences.',
        '2023-01-15',
        TRUE
    ),
    (
        (SELECT id FROM diaspora_communities WHERE name = 'ECFE Europe Fellowship'),
        (SELECT id FROM churches WHERE name = 'Wolkite Revival Church'),
        'Relief Partnership',
        'Coordinates seasonal relief fundraising and volunteer mobilization.',
        '2024-03-01',
        TRUE
    );

INSERT INTO field_registrations (church_id, field_officer_id, latitude, longitude, altitude, accuracy, address, notes, status) VALUES
    (
        (SELECT id FROM churches WHERE name = 'Addis Hope Church'),
        (SELECT id FROM users WHERE username = 'field.officer'),
        8.9806,
        38.7578,
        2355,
        4.2,
        'Bole Medhanialem, Addis Ababa',
        'Verified compound and worship hall coordinates.',
        'VERIFIED'
    ),
    (
        (SELECT id FROM churches WHERE name = 'Adama Gospel Center'),
        (SELECT id FROM users WHERE username = 'field.officer'),
        8.5409,
        39.2716,
        1710,
        5.0,
        'Adama, Oromia',
        'Pending media upload and frontage photo.',
        'PENDING'
    );

INSERT INTO registration_photos (registration_id, s3_key, caption) VALUES
    ((SELECT id FROM field_registrations WHERE address = 'Bole Medhanialem, Addis Ababa'), 'registrations/addis-hope/front.jpg', 'Front entrance'),
    ((SELECT id FROM field_registrations WHERE address = 'Bole Medhanialem, Addis Ababa'), 'registrations/addis-hope/auditorium.jpg', 'Main auditorium');

INSERT INTO incidents (title, description, severity, status, location, latitude, longitude, reported_by, woreda_id, affected_count) VALUES
    (
        'Displacement Support Needed',
        'Recent displacement created urgent shelter and food needs for member households.',
        'HIGH',
        'ACTIVE',
        'Adama',
        8.5409,
        39.2716,
        (SELECT id FROM users WHERE username = 'admin'),
        (SELECT id FROM woredas WHERE code = 'OR-ES-AD'),
        95
    ),
    (
        'Flood Recovery Coordination',
        'Church compound damage and household recovery follow-up.',
        'MEDIUM',
        'CONTAINED',
        'Wolkite',
        8.2876,
        37.7801,
        (SELECT id FROM users WHERE username = 'admin'),
        (SELECT id FROM woredas WHERE code = 'CE-GU-WK'),
        44
    );

INSERT INTO volunteers (full_name, phone, email, skills, church_id, status, latitude, longitude, is_active) VALUES
    ('Abel Terefe', '+251911300001', 'abel.terefe@ecfe.org', 'Logistics, first aid', (SELECT id FROM churches WHERE name = 'Addis Hope Church'), 'DEPLOYED', 8.9800, 38.7600, TRUE),
    ('Saron Negash', '+251911300002', 'saron.negash@ecfe.org', 'Counselling, child support', (SELECT id FROM churches WHERE name = 'Adama Gospel Center'), 'AVAILABLE', 8.5410, 39.2710, TRUE),
    ('Mekonnen Bulti', '+251911300003', 'mekonnen.bulti@ecfe.org', 'Distribution management', (SELECT id FROM churches WHERE name = 'Wolkite Revival Church'), 'AVAILABLE', 8.2870, 37.7800, TRUE);

INSERT INTO volunteer_deployments (volunteer_id, incident_id, notes) VALUES
    (
        (SELECT id FROM volunteers WHERE email = 'abel.terefe@ecfe.org'),
        (SELECT id FROM incidents WHERE title = 'Displacement Support Needed'),
        'Assigned as field logistics coordinator.'
    );

INSERT INTO relief_distributions (incident_id, item_name, quantity, unit, distributed_to, distributed_by, notes) VALUES
    (
        (SELECT id FROM incidents WHERE title = 'Displacement Support Needed'),
        'Emergency Food Kit',
        120,
        'kits',
        '95 displaced households',
        (SELECT id FROM users WHERE username = 'admin'),
        'Distributed through church coordination center.'
    ),
    (
        (SELECT id FROM incidents WHERE title = 'Flood Recovery Coordination'),
        'Blankets',
        70,
        'pieces',
        'Flood-affected families',
        (SELECT id FROM users WHERE username = 'admin'),
        'Priority distribution for elderly households.'
    );
