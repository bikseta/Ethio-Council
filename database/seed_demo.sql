-- ============================================================
-- ETHIO-COUNCIL DEMO SEED DATA
-- ============================================================

-- Short-hand CTEs for existing IDs
DO $$ DECLARE
  -- Regions
  r_aa UUID := '1d9132a2-c392-49e9-b344-83f60886572d';
  r_am UUID := '8c3d44f1-2cf9-4f3c-9274-29e16b44981a';
  r_or UUID := 'ea406280-754e-4a43-aa85-ff2ca8fbecd3';
  r_sn UUID := '9308aaef-569d-4ac0-bda1-4e09865f1178';
  -- Zones
  z_aa UUID := '10047092-9221-4d57-ae4c-adeed5bf55cb';
  z_am UUID := 'e118d4a0-d302-4a8b-aadc-1dcd8cc16ab5';
  z_or UUID := '01ef66a1-0091-4e21-93c9-a3faa732497a';
  z_sn UUID := 'b291ae63-ebb2-457d-9091-3cf80c2a13f2';
  -- Woredas
  w_aa UUID := '7bb3b659-3c20-48b9-bc63-8b5b473f1e64';
  w_am UUID := 'ecb11774-46e2-4d60-afaa-10310c2c4b73';
  w_or UUID := '291077db-a134-4aab-90cc-77411a244d8a';
  w_sn UUID := 'fed3331d-d73d-4005-9739-d0d7f308d30d';
  -- Denominations
  d_age  UUID := '3b57c1ce-cfa6-4a6a-8d58-6d3c088c8acc';
  d_ebcf UUID := 'a946c509-d24c-4a38-90b3-f85b0e4c568a';
  d_eecmy UUID := '0aa09ac6-56c3-4f34-b405-42b9301f0d03';
  d_efgbc UUID := '5425bfc7-143b-49b6-bc99-9bc04dcf44bc';
  d_ekhc UUID := 'aaaf9d82-6d36-4009-ab86-52ffb7717e77';
  -- Admin user
  u_admin UUID := 'b6e34b0e-7d08-469a-a235-841fb06b9a00';
  -- Church IDs (pre-generated)
  c1 UUID := uuid_generate_v4();
  c2 UUID := uuid_generate_v4();
  c3 UUID := uuid_generate_v4();
  c4 UUID := uuid_generate_v4();
  c5 UUID := uuid_generate_v4();
  c6 UUID := uuid_generate_v4();
  c7 UUID := uuid_generate_v4();
  c8 UUID := uuid_generate_v4();
  c9 UUID := uuid_generate_v4();
  c10 UUID := uuid_generate_v4();
  c11 UUID := uuid_generate_v4();
  c12 UUID := uuid_generate_v4();
  c13 UUID := uuid_generate_v4();
  c14 UUID := uuid_generate_v4();
  c15 UUID := uuid_generate_v4();

BEGIN

-- ============================================================
-- ADDITIONAL ZONES
-- ============================================================
INSERT INTO zones (id, name, code, region_id) VALUES
  (uuid_generate_v4(), 'Yeka Sub-City',       'AA-YK', r_aa),
  (uuid_generate_v4(), 'Bole Sub-City',        'AA-BO', r_aa),
  (uuid_generate_v4(), 'Kirkos Sub-City',      'AA-KK', r_aa),
  (uuid_generate_v4(), 'South Gondar Zone',    'AM-SG', r_am),
  (uuid_generate_v4(), 'West Hararghe Zone',   'OR-WH', r_or),
  (uuid_generate_v4(), 'Sidama Zone',          'SN-SI', r_sn)
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- ADDITIONAL WOREDAS
-- ============================================================
INSERT INTO woredas (id, name, code, zone_id) VALUES
  (uuid_generate_v4(), 'Yeka Woreda 1',        'AA-YK-01', (SELECT id FROM zones WHERE code='AA-YK')),
  (uuid_generate_v4(), 'Bole Woreda 1',        'AA-BO-01', (SELECT id FROM zones WHERE code='AA-BO')),
  (uuid_generate_v4(), 'Kirkos Woreda 1',      'AA-KK-01', (SELECT id FROM zones WHERE code='AA-KK')),
  (uuid_generate_v4(), 'Debre Tabor Woreda',   'AM-SG-01', (SELECT id FROM zones WHERE code='AM-SG')),
  (uuid_generate_v4(), 'Chiro Woreda',         'OR-WH-01', (SELECT id FROM zones WHERE code='OR-WH')),
  (uuid_generate_v4(), 'Hawassa Woreda 1',     'SN-SI-01', (SELECT id FROM zones WHERE code='SN-SI'))
ON CONFLICT (code) DO NOTHING;

-- ============================================================
-- CHURCHES (15 sample churches)
-- ============================================================
INSERT INTO churches (id, name, denomination_id, region_id, zone_id, woreda_id, community, address,
  year_established, membership_size, languages_used, service_schedules, phone, email, is_verified, verification_status)
VALUES
  -- Addis Ababa churches
  (c1,  'Kale Heywet Church - Addis Ababa Central',  d_ekhc,  r_aa, z_aa, w_aa, 'Piassa',        'Ras Desta Damtew St, Addis Ababa',        1958, 2400, ARRAY['am','en'],   '[{"day":"Sunday","time":"8:00 AM"},{"day":"Sunday","time":"10:30 AM"}]', '+251-11-551-2200', 'central@kaleheywet.org',  TRUE,  'approved'),
  (c2,  'EECMY Addis Ababa Synod - Bole Parish',     d_eecmy, r_aa, z_aa, w_aa, 'Bole',          'Bole Road, Near Bole Airport, AA',        1972, 1800, ARRAY['am','en','ti'],'[{"day":"Sunday","time":"9:00 AM"}]',                               '+251-11-661-8900', 'bole@eecmy.org',          TRUE,  'approved'),
  (c3,  'Full Gospel Church - Megenagna',             d_efgbc, r_aa, z_aa, w_aa, 'Megenagna',     'Megenagna Roundabout, Addis Ababa',       1985, 3200, ARRAY['am','en'],   '[{"day":"Sunday","time":"7:00 AM"},{"day":"Sunday","time":"10:00 AM"},{"day":"Wednesday","time":"6:00 PM"}]', '+251-11-467-3300', 'megenagna@fgc.org',       TRUE,  'approved'),
  (c4,  'Assemblies of God - Gerji Congregation',    d_age,   r_aa, z_aa, w_aa, 'Gerji',         'Gerji Area, Addis Ababa',                 1993, 950,  ARRAY['am'],        '[{"day":"Sunday","time":"9:30 AM"}]',                               '+251-11-462-7788', 'gerji@aoge.org',          TRUE,  'approved'),
  (c5,  'Ethiopian Baptist Church - Kazanchis',       d_ebcf,  r_aa, z_aa, w_aa, 'Kazanchis',     'Kazanchis, Near UN ECA, Addis Ababa',     1969, 720,  ARRAY['am','en'],   '[{"day":"Sunday","time":"10:00 AM"}]',                              '+251-11-551-6644', 'kazanchis@ebcf.org',      TRUE,  'approved'),

  -- Amhara region churches
  (c6,  'Kale Heywet Church - Bahir Dar',            d_ekhc,  r_am, z_am, w_am, 'Bahir Dar City','King George VI St, Bahir Dar',           1965, 1650, ARRAY['am'],        '[{"day":"Sunday","time":"8:00 AM"},{"day":"Sunday","time":"10:00 AM"}]','+251-58-220-5500', 'bahirdar@kaleheywet.org', TRUE,  'approved'),
  (c7,  'EECMY Gondar Parish',                       d_eecmy, r_am, z_am, w_am, 'Gondar City',   'Fasil Area, Gondar',                      1960, 1120, ARRAY['am'],        '[{"day":"Sunday","time":"9:00 AM"}]',                               '+251-58-111-2233', 'gondar@eecmy.org',        TRUE,  'approved'),
  (c8,  'Full Gospel - Dessie Congregation',         d_efgbc, r_am, z_am, w_am, 'Dessie',        'Dessie Town, South Wollo Zone',           1988, 830,  ARRAY['am'],        '[{"day":"Sunday","time":"9:00 AM"},{"day":"Friday","time":"5:00 PM"}]', '+251-33-111-4455', 'dessie@fgc.org',          FALSE, 'pending'),

  -- Oromia region churches
  (c9,  'Kale Heywet Church - Adama',                d_ekhc,  r_or, z_or, w_or, 'Adama City',    'Adama (Nazret), East Shewa',              1970, 1380, ARRAY['am','or'],   '[{"day":"Sunday","time":"8:30 AM"},{"day":"Sunday","time":"11:00 AM"}]','+251-22-111-3344', 'adama@kaleheywet.org',    TRUE,  'approved'),
  (c10, 'Assemblies of God - Jimma Central',         d_age,   r_or, z_or, w_or, 'Jimma City',    'Jimma Town Center, Jimma Zone',           1981, 1050, ARRAY['am','or'],   '[{"day":"Sunday","time":"9:00 AM"}]',                               '+251-47-111-6677', 'jimma@aoge.org',          TRUE,  'approved'),
  (c11, 'EECMY Nekemte Parish',                      d_eecmy, r_or, z_or, w_or, 'Nekemte',       'Nekemte Town, East Welega Zone',          1955, 2100, ARRAY['or','am'],   '[{"day":"Sunday","time":"8:00 AM"},{"day":"Sunday","time":"10:30 AM"}]','+251-57-661-2200', 'nekemte@eecmy.org',       TRUE,  'approved'),
  (c12, 'Ethiopian Baptist - Shashemene',             d_ebcf,  r_or, z_or, w_or, 'Shashemene',    'Shashemene, West Arsi Zone',              1977, 640,  ARRAY['am','or'],   '[{"day":"Sunday","time":"10:00 AM"}]',                              '+251-46-110-8899', 'shashemene@ebcf.org',     FALSE, 'under_review'),

  -- SNNPR region churches
  (c13, 'Kale Heywet Church - Hawassa Central',      d_ekhc,  r_sn, z_sn, w_sn, 'Hawassa City',  'Hawassa, Sidama Zone',                    1963, 3100, ARRAY['am','sid'],  '[{"day":"Sunday","time":"7:30 AM"},{"day":"Sunday","time":"10:00 AM"},{"day":"Sunday","time":"5:00 PM"}]','+251-46-220-4455', 'hawassa@kaleheywet.org',  TRUE,  'approved'),
  (c14, 'Full Gospel - Wolaita Sodo',                d_efgbc, r_sn, z_sn, w_sn, 'Wolaita Sodo',  'Sodo Town, Wolaita Zone',                 1990, 780,  ARRAY['am','wal'],  '[{"day":"Sunday","time":"9:30 AM"}]',                               '+251-46-551-2211', 'sodo@fgc.org',            TRUE,  'approved'),
  (c15, 'Assemblies of God - Arba Minch',            d_age,   r_sn, z_sn, w_sn, 'Arba Minch',    'Arba Minch, Gamo Zone',                   1986, 560,  ARRAY['am','gam'],  '[{"day":"Sunday","time":"9:00 AM"}]',                               '+251-46-881-3322', 'arba@aoge.org',           FALSE, 'pending')
;

-- ============================================================
-- CHURCH LEADERS
-- ============================================================
INSERT INTO church_leaders (church_id, full_name, role, phone, email, bio, is_primary, is_active) VALUES
  (c1,  'Ato Tesfaye Gebre',       'Senior Pastor',     '+251-91-123-4567', 'tesfaye@kaleheywet.org',  'Served EKHC for 22 years. Graduate of Addis Ababa Bible College.',      TRUE,  TRUE),
  (c1,  'Weizero Marta Haile',     'Associate Pastor',  '+251-91-234-5678', 'marta@kaleheywet.org',    'Women ministry leader with 12 years of service.',                         FALSE, TRUE),
  (c2,  'Rev. Daniel Bekele',      'Parish Pastor',     '+251-91-345-6789', 'daniel@eecmy.org',        'Ordained minister in EECMY for 18 years. Theology degree from EGST.',     TRUE,  TRUE),
  (c3,  'Pastor Solomon Tadesse',  'Senior Pastor',     '+251-91-456-7890', 'solomon@fgc.org',         'Founder of Megenagna congregation. 30 years in ministry.',                TRUE,  TRUE),
  (c6,  'Rev. Abebe Worku',        'Parish Pastor',     '+251-91-567-8901', 'abebe@kaleheywet.org',    'Regional church coordinator for Amhara. Author of several Amharic devotionals.', TRUE, TRUE),
  (c9,  'Ato Girma Lemma',         'Senior Pastor',     '+251-91-678-9012', 'girma@kaleheywet.org',    'Bilingual pastor serving Oromo and Amhara communities in Adama.',        TRUE,  TRUE),
  (c13, 'Pastor Yohannes Alemu',   'Senior Pastor',     '+251-91-789-0123', 'yohannes@kaleheywet.org', 'Pioneer of evangelical work in Sidama Zone. Led church plant in 3 woredas.', TRUE, TRUE),
  (c13, 'Weizero Tigist Kebede',   'Youth Pastor',      '+251-91-890-1234', 'tigist@kaleheywet.org',   'Youth ministry director with 400+ youth members under her care.',         FALSE, TRUE),
  (c10, 'Pastor Wakjira Gobena',   'Lead Pastor',       '+251-91-901-2345', 'wakjira@aoge.org',        'Serves Jimma congregation since 2005. Active in rural church planting.',  TRUE,  TRUE),
  (c4,  'Elder Habtamu Seifu',     'Elder/Deacon',      '+251-91-012-3456', 'habtamu@aoge.org',        'Lay leader and businessman supporting church operations in Gerji.',       FALSE, TRUE)
;

-- ============================================================
-- MINISTRIES
-- ============================================================
INSERT INTO ministries (name, church_id, denomination_id, ministry_type, description, contact_name, contact_phone, region_id, zone_id, woreda_id, is_active) VALUES
  ('Kale Heywet Youth Ministry - National',    NULL,  d_ekhc,  'Youth',              'National youth ministry coordinating youth programs across all EKHC congregations.',  'Ato Biruk Alemu',      '+251-91-111-2222', r_aa, z_aa, w_aa, TRUE),
  ('EECMY Women Fellowship',                   NULL,  d_eecmy, 'Women',              'National womens fellowship promoting leadership, health and spiritual growth.',         'Weizero Hiwot Girma',  '+251-91-222-3333', r_aa, z_aa, w_aa, TRUE),
  ('Addis Ababa City Outreach',                c1,    d_ekhc,  'Evangelism',         'Urban evangelism targeting street communities and informal settlements in Addis.',     'Ato Dawit Mulugeta',   '+251-91-333-4444', r_aa, z_aa, w_aa, TRUE),
  ('Bahir Dar Prison Ministry',                c6,    d_ekhc,  'Prison Ministry',    'Weekly services and counselling at Bahir Dar Federal Prison.',                        'Rev. Abebe Worku',     '+251-91-567-8901', r_am, z_am, w_am, TRUE),
  ('Oromia Rural Church Planting',             NULL,  d_eecmy, 'Church Planting',    'Establishing new congregations in underserved kebeles across Oromia region.',         'Ato Lemma Negash',     '+251-91-444-5555', r_or, z_or, w_or, TRUE),
  ('Hawassa HIV/AIDS Care Ministry',           c13,   d_ekhc,  'Healthcare',         'Community health support for HIV/AIDS patients in Sidama Zone.',                      'Nurse Selam Tadesse',  '+251-91-555-6666', r_sn, z_sn, w_sn, TRUE),
  ('National Disaster Response Network',       NULL,  NULL,    'Humanitarian',       'Coordinating church-based emergency response across all ECFE member denominations.',  'Ato Firew Bekele',     '+251-91-666-7777', r_aa, z_aa, w_aa, TRUE),
  ('Children Bible Education Program',         c3,    d_efgbc, 'Children',           'Sunday school and vacation Bible school serving 600+ children in Addis Ababa.',       'Weizero Azeb Hailu',   '+251-91-777-8888', r_aa, z_aa, w_aa, TRUE),
  ('EECMY Theological Education',              NULL,  d_eecmy, 'Leadership Training','Equipping church leaders through certificate and diploma theological programs.',       'Dr. Mulugeta Zewdie',  '+251-91-888-9999', r_aa, z_aa, w_aa, TRUE),
  ('Jimma Community Development',              c10,   d_age,   'Community Dev',      'Integrated community development: clean water, literacy and vocational training.',    'Ato Wakjira Gobena',   '+251-91-901-2345', r_or, z_or, w_or, TRUE),
  ('Wolaita Bible Translation Project',        c14,   d_efgbc, 'Bible Translation',  'Translating scripture and devotional materials into Wolaita language.',              'Ato Dawit Wolde',      '+251-91-112-2233', r_sn, z_sn, w_sn, TRUE),
  ('Gondar Orphan & Vulnerable Children',      c7,    d_eecmy, 'Social Services',    'Care and support for orphaned children in Gondar and surrounding areas.',            'Weizero Ruth Asrat',   '+251-91-223-3344', r_am, z_am, w_am, TRUE)
;

-- ============================================================
-- DIASPORA COMMUNITIES
-- ============================================================
INSERT INTO diaspora_communities (name, country, city, contact_person, contact_email, contact_phone, membership_count, denomination_id, is_active) VALUES
  ('Ethiopian Evangelical Fellowship - Washington DC',  'United States',    'Washington DC',  'Dr. Samuel Tadesse',      'dc@eef-usa.org',          '+1-202-555-0101', 320, d_ekhc,  TRUE),
  ('Ethiopian Kale Heywet Church - Minnesota',          'United States',    'Minneapolis',    'Rev. Yonas Bekele',        'mn@ekhc-usa.org',         '+1-612-555-0102', 210, d_ekhc,  TRUE),
  ('EECMY Fellowship - Toronto',                        'Canada',           'Toronto',        'Ato Tesfaye Alemu',        'toronto@eecmy-canada.org', '+1-416-555-0103', 185, d_eecmy, TRUE),
  ('Ethiopian Full Gospel Church - London',             'United Kingdom',   'London',         'Pastor Daniel Haile',      'london@efgc-uk.org',      '+44-20-5550-0104', 240, d_efgbc, TRUE),
  ('Ethiopian Evangelical Church - Stockholm',          'Sweden',           'Stockholm',      'Rev. Miriam Getachew',     'stockholm@eec-sweden.org','+46-8-5550-0105', 95,  d_eecmy, TRUE),
  ('Ethiopian Christian Fellowship - Melbourne',        'Australia',        'Melbourne',      'Ato Girma Woldemichael',   'mel@ecf-aus.org',         '+61-3-5550-0106', 130, d_ekhc,  TRUE),
  ('Ethiopian Baptist Community - Frankfurt',           'Germany',          'Frankfurt',      'Pastor Hana Tesfaye',      'frankfurt@ebc-de.org',    '+49-69-5550-0107', 88,  d_ebcf,  TRUE),
  ('Assemblies of God Ethiopia - Nairobi',              'Kenya',            'Nairobi',        'Pastor Joseph Alemu',      'nairobi@age-kenya.org',   '+254-20-5550-0108', 145, d_age,  TRUE),
  ('ECFE Community - Dubai',                            'UAE',              'Dubai',          'Ato Henok Gebre',          'dubai@ecfe-uae.org',      '+971-4-5550-0109', 175, NULL,    TRUE),
  ('Ethiopian Evangelical Fellowship - Oslo',           'Norway',           'Oslo',           'Rev. Sara Mulugeta',       'oslo@eef-norway.org',     '+47-22-5550-0110', 70,  d_eecmy, TRUE)
;

-- ============================================================
-- DIASPORA PARTNERSHIPS
-- ============================================================
INSERT INTO diaspora_partnerships (diaspora_community_id, church_id, partnership_type, description, start_date, status) VALUES
  ((SELECT id FROM diaspora_communities WHERE city='Washington DC'),  c1,  'Financial Support',      'Annual support for the Central Church building renovation project.',                '2023-01-15', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Washington DC'),  c13, 'Mission Collaboration',  'Joint youth exchange program between DC fellowship and Hawassa central church.',     '2022-06-01', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Minneapolis'),    c6,  'Financial Support',      'Monthly support for the Bahir Dar childrens education program.',                    '2021-09-01', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Toronto'),        c9,  'Prayer Partnership',     'Monthly prayer calls and annual mission team visits to Adama congregation.',         '2023-03-10', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='London'),         c3,  'Mission Collaboration',  'Leadership training program — UK team visits Megenagna annually.',                  '2022-11-20', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Melbourne'),      c13, 'Financial Support',      'Funding the Hawassa HIV/AIDS care ministry medical supplies.',                       '2023-07-01', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Frankfurt'),      c7,  'Prayer Partnership',     'Sister-church relationship with Gondar Parish established in 2020.',                '2020-05-01', 'active'),
  ((SELECT id FROM diaspora_communities WHERE city='Nairobi'),        c10, 'Mission Collaboration',  'Cross-border evangelism and community development in Jimma.',                       '2024-01-01', 'active')
;

-- ============================================================
-- FIELD REGISTRATIONS (GPS verified)
-- ============================================================
INSERT INTO field_registrations (church_id, field_officer_id, gps_lat, gps_lng, gps_accuracy, location, device_metadata, registration_status, notes) VALUES
  (c1,  u_admin, 9.0192,  38.7525, 3.5, ST_SetSRID(ST_MakePoint(38.7525, 9.0192), 4326),  '{"device":"Samsung Galaxy A53","os":"Android 13","app_version":"1.2.0"}', 'verified', 'Main building verified. Large compound with parking.'),
  (c2,  u_admin, 9.0054,  38.7890, 4.2, ST_SetSRID(ST_MakePoint(38.7890, 9.0054), 4326),  '{"device":"iPhone 14","os":"iOS 16","app_version":"1.2.0"}',             'verified', 'Bole parish building. Adjacent to commercial area.'),
  (c3,  u_admin, 9.0204,  38.7980, 2.8, ST_SetSRID(ST_MakePoint(38.7980, 9.0204), 4326),  '{"device":"Samsung Galaxy A53","os":"Android 13","app_version":"1.2.0"}', 'verified', 'Large sanctuary capacity 1500+. New hall under construction.'),
  (c6,  u_admin, 11.5936, 37.3906, 5.1, ST_SetSRID(ST_MakePoint(37.3906, 11.5936), 4326), '{"device":"Tecno Camon 19","os":"Android 12","app_version":"1.1.5"}',    'verified', 'Historic building established 1965. Near Lake Tana.'),
  (c9,  u_admin, 8.5500,  39.2700, 3.9, ST_SetSRID(ST_MakePoint(39.2700, 8.5500), 4326),  '{"device":"Samsung Galaxy A33","os":"Android 12","app_version":"1.2.0"}', 'verified', 'Adama central church. Well-equipped facility.'),
  (c13, u_admin, 7.0621,  38.4769, 2.5, ST_SetSRID(ST_MakePoint(38.4769, 7.0621), 4326),  '{"device":"iPhone 13","os":"iOS 16","app_version":"1.2.0"}',             'verified', 'Hawassa central — largest evangelical church in Sidama Zone.'),
  (c10, u_admin, 7.6700,  36.8300, 6.0, ST_SetSRID(ST_MakePoint(36.8300, 7.6700), 4326),  '{"device":"Itel A56","os":"Android 11","app_version":"1.1.5"}',          'pending',  'Jimma congregation. Registration pending secondary review.'),
  (c15, u_admin, 6.0333,  37.5500, 7.2, ST_SetSRID(ST_MakePoint(37.5500, 6.0333), 4326),  '{"device":"Samsung Galaxy A13","os":"Android 12","app_version":"1.1.5"}', 'pending',  'Arba Minch registration. GPS accuracy marginal — re-verification recommended.')
;

-- ============================================================
-- CRISIS INCIDENTS
-- ============================================================
INSERT INTO incidents (title, description, incident_type, severity, status, location, gps_lat, gps_lng, region_id, zone_id, woreda_id, affected_population, reported_by) VALUES
  ('Flooding in Hawassa - Displacement Crisis',
   'Severe flooding has displaced approximately 1,200 families in Hawassa city outskirts. Churches coordinating emergency shelter and food distribution.',
   'Natural Disaster', 'critical', 'active',
   ST_SetSRID(ST_MakePoint(38.4769, 7.0621), 4326), 7.0621, 38.4769,
   r_sn, z_sn, w_sn, 6000, u_admin),

  ('Drought Relief - Arba Minch Zone',
   'Prolonged drought affecting pastoralist communities near Arba Minch. Church networks distributing food aid and clean water.',
   'Drought', 'high', 'responding',
   ST_SetSRID(ST_MakePoint(37.5500, 6.0333), 4326), 6.0333, 37.5500,
   r_sn, z_sn, w_sn, 4500, u_admin),

  ('Community Violence - Intercommunal Tension',
   'Intercommunal tension reported in West Hararghe. ECFE peace-building teams deployed. Churches providing safe spaces for reconciliation.',
   'Conflict', 'high', 'responding',
   ST_SetSRID(ST_MakePoint(40.1500, 8.9500), 4326), 8.9500, 40.1500,
   r_or, z_or, w_or, 2800, u_admin),

  ('Fire - Church Building Destroyed in Jimma',
   'Fire destroyed the main sanctuary of Jimma Assemblies of God church. Congregation displaced. Reconstruction support needed.',
   'Fire', 'medium', 'recovering',
   ST_SetSRID(ST_MakePoint(36.8300, 7.6700), 4326), 7.6700, 36.8300,
   r_or, z_or, w_or, 800, u_admin),

  ('Cholera Outbreak - Gondar Area',
   'Cholera cases reported near Gondar. EECMY health ministry and volunteers mobilized for sanitation and community education.',
   'Health Emergency', 'high', 'responding',
   ST_SetSRID(ST_MakePoint(37.3906, 12.6000), 4326), 12.6000, 37.3906,
   r_am, z_am, w_am, 3200, u_admin),

  ('Food Insecurity - Rural Amhara',
   'Seasonal food insecurity affecting rural communities in North Shewa. Church food banks mobilizing emergency distributions.',
   'Food Insecurity', 'medium', 'active',
   ST_SetSRID(ST_MakePoint(38.5000, 10.5000), 4326), 10.5000, 38.5000,
   r_am, z_am, w_am, 5500, u_admin)
;

-- ============================================================
-- VOLUNTEERS
-- ============================================================
INSERT INTO volunteers (full_name, phone, email, skills, availability, region_id, is_active) VALUES
  ('Ato Biruk Mengistu',    '+251-91-100-1001', 'biruk.m@ecfe.org',   ARRAY['First Aid','Logistics','Driving'],              'Full-time',   r_aa, TRUE),
  ('Weizero Hana Solomon',  '+251-91-100-1002', 'hana.s@ecfe.org',    ARRAY['Counselling','Social Work','Translation-Amharic'],'Weekends',  r_aa, TRUE),
  ('Ato Elias Haile',       '+251-91-100-1003', 'elias.h@ecfe.org',   ARRAY['Medical','Nursing','Health Education'],         'Part-time',   r_aa, TRUE),
  ('Weizero Selamawit Ato', '+251-91-100-1004', 'selam.a@ecfe.org',   ARRAY['Teaching','Childrens Ministry','Counselling'],  'Weekends',    r_am, TRUE),
  ('Ato Mebratu Kassaye',   '+251-91-100-1005', 'meb.k@ecfe.org',     ARRAY['Construction','Engineering','Project Mgmt'],    'Full-time',   r_am, TRUE),
  ('Ato Dereje Wolde',      '+251-91-100-1006', 'der.w@ecfe.org',     ARRAY['Driving','Logistics','Relief Distribution'],    'Full-time',   r_or, TRUE),
  ('Weizero Mahlet Girma',  '+251-91-100-1007', 'mah.g@ecfe.org',     ARRAY['Translation-Oromo','Community Org','Teaching'], 'Part-time',   r_or, TRUE),
  ('Ato Tamiru Belayneh',   '+251-91-100-1008', 'tam.b@ecfe.org',     ARRAY['Medical','Pharmacy','Health Education'],        'Weekends',    r_or, TRUE),
  ('Ato Fikadu Tesfaye',    '+251-91-100-1009', 'fik.t@ecfe.org',     ARRAY['Counselling','Trauma Support','Translation-Sidama'],'Full-time',r_sn,TRUE),
  ('Weizero Liya Bekele',   '+251-91-100-1010', 'liya.b@ecfe.org',    ARRAY['Social Work','Womens Ministry','Child Protection'],'Part-time', r_sn, TRUE),
  ('Ato Tadesse Alemu',     '+251-91-100-1011', 'tad.a@ecfe.org',     ARRAY['First Aid','Logistics','Food Distribution'],   'Full-time',   r_sn, TRUE),
  ('Rev. Yared Mulugeta',   '+251-91-100-1012', 'yared.m@ecfe.org',   ARRAY['Pastoral Care','Counselling','Preaching'],     'Weekends',    r_aa, TRUE)
;

-- ============================================================
-- ADDITIONAL USERS (demo accounts)
-- ============================================================
INSERT INTO users (email, username, password_hash, full_name, phone, role, language_preference, region_id, is_active, is_verified) VALUES
  ('regional.admin@ecfe.org', 'regional_admin',
   '$2b$12$9dPWeMmShRj6iOjA2sfscugAse09og9JI1wTjRAK.T1opeCUwMWNm',
   'Ato Dawit Kebede', '+251-91-200-0001', 'REGIONAL_ADMIN', 'am', r_aa, TRUE, TRUE),
  ('field.officer@ecfe.org', 'field_officer',
   '$2b$12$9dPWeMmShRj6iOjA2sfscugAse09og9JI1wTjRAK.T1opeCUwMWNm',
   'Weizero Sara Haile', '+251-91-200-0002', 'FIELD_OFFICER', 'am', r_or, TRUE, TRUE),
  ('church.leader@ecfe.org', 'church_leader',
   '$2b$12$9dPWeMmShRj6iOjA2sfscugAse09og9JI1wTjRAK.T1opeCUwMWNm',
   'Pastor Solomon Tadesse', '+251-91-456-7890', 'CHURCH_LEADER', 'en', r_aa, TRUE, TRUE),
  ('diaspora.rep@ecfe.org', 'diaspora_rep',
   '$2b$12$9dPWeMmShRj6iOjA2sfscugAse09og9JI1wTjRAK.T1opeCUwMWNm',
   'Dr. Samuel Tadesse', '+1-202-555-0101', 'DIASPORA_REP', 'en', NULL, TRUE, TRUE)
ON CONFLICT (email) DO NOTHING;

END $$;
