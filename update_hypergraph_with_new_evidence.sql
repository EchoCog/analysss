-- Update Hypergraph Database with New Evidence
-- Bantjies Betrayal & 2025 Attack Pattern
-- Date: October 12, 2025

-- ============================================
-- 1. ADD NEW ENTITIES
-- ============================================

-- Add Danie Bantjies as critical entity
INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 7, 'Danie Bantjies', 'Person', 'Accountant (since 2013)'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Danie Bantjies' AND event_id = 7
);

-- Add "Strange People" collective entity
INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 25, 'Unknown Infiltrators', 'Group', 'Access attempt coordinators'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Unknown Infiltrators'
);

-- ============================================
-- 2. ADD NEW TIMELINE EVENTS (2024-2025 ATTACK PATTERN)
-- ============================================

-- Event 24: Secret Trustee Installation (July 2024)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number, 
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2024-07-01',
    'Bantjies secretly installed as trustee without Dan''s knowledge',
    'Danie Bantjies installed as third trustee alongside Peter and Jacqui. Dan deliberately excluded from notification. Email shows Rynette ("pp Peter") coordinating. Violates trust law requiring beneficiary notification.',
    'Conspiracy Preparation',
    5,
    true,
    'Email correspondence showing Bantjies trustee appointment',
    'case_2025_137857/02_evidence/emails/',
    'CRITICAL: Establishes Bantjies as double agent, enables all subsequent attacks'
) ON CONFLICT DO NOTHING;

-- Event 25: "Strange People" Access Attempts (July-Dec 2024)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2024-09-01',
    'Endless torrent of unknown individuals attempting company access',
    'Multiple unknown individuals systematically attempting to gain access to company systems and operations. Pattern suggests coordinated intelligence gathering operation with multiple vectors of attack.',
    'Conspiracy Preparation',
    5,
    true,
    'Security logs, access attempt records',
    'case_2025_137857/02_evidence/security/',
    'HIGH: Coordinated probing for weaknesses, intelligence gathering phase'
) ON CONFLICT DO NOTHING;

-- Event 26: False Incapacitation Report (Late 2024)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2024-11-01',
    'Dan falsely reported as "incapacitated" to bank',
    'Unknown party reports Dan as mentally incapacitated to bank. Bank restricts Dan''s access "for protection". Classic financial elder abuse tactic attempting to seize control through false incompetency claims.',
    'Conspiracy Preparation',
    5,
    true,
    'Bank correspondence, access restriction notices',
    'case_2025_137857/02_evidence/financial/',
    'CRITICAL: Attempted control seizure through false medical claims'
) ON CONFLICT DO NOTHING;

-- Event 27: Dan Reports Fraud to Bantjies (May 2025)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2025-05-16',
    'Dan unknowingly reports fraud discoveries to Bantjies',
    'Dan, unaware that Bantjies is now a trustee and potentially complicit, reports his fraud discoveries to Bantjies as trusted accountant. Bantjies gains intelligence on what Dan has discovered. Tragic irony proves Dan''s good faith while exposing conspiracy depth.',
    'Fraud Discovery and Cover-up',
    4,
    true,
    'Communication records between Dan and Bantjies',
    'case_2025_137857/02_evidence/emails/',
    'CRITICAL: Dan unknowingly reports to perpetrator, proves good faith, exposes conspiracy'
) ON CONFLICT DO NOTHING;

-- Event 28: "12-Hour Sign Here" Scam (2025)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2025-06-15',
    '12-hour signature scam - manufactured urgency',
    'Attempt to force Dan to sign documents within 12-hour deadline. Classic fraud tactic using manufactured urgency and exhaustion to obtain signatures on asset transfer documents without proper review.',
    'Active Attack Phase',
    6,
    true,
    'Document requests, correspondence',
    'case_2025_137857/02_evidence/legal/',
    'HIGH: Financial attack attempt #1 - Dan refused to sign under duress'
) ON CONFLICT DO NOTHING;

-- Event 29: "1000-Page Report" Scam (2025)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2025-07-01',
    '1000-page report demand - impossible compliance trap',
    'Demand for 1000-page report within one month. Impossible deliverable designed to create "evidence" of Dan''s incompetence when he cannot comply. Setup to justify taking control.',
    'Active Attack Phase',
    6,
    true,
    'Document requests, correspondence',
    'case_2025_137857/02_evidence/legal/',
    'HIGH: Financial attack attempt #2 - Dan recognized the setup'
) ON CONFLICT DO NOTHING;

-- Event 30: Account Redirection & Card Cancellation (April 2025)
-- This connects to existing Event 15 (April 14, 2025)
UPDATE timeline_events 
SET 
    description = 'Bank accounts redirected and cards cancelled secretly. Rynette bank letter change on April 14. Financial strangulation attempt to force capitulation through poverty.',
    significance = 'CRITICAL: Financial attack attempt #3 - connects to Rynette bank control'
WHERE event_date = '2025-04-15';

-- Event 31: Ex Parte Interdict (August 19, 2025)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2025-08-19',
    'Ex parte interdict - legal violence and asset stripping',
    'Peter Faucitt obtains ex parte interdict without notice to Dan or Jacqui. Supported by Bantjies. Court order used to freeze/empty accounts. "Legal" theft under court protection.',
    'Active Attack Phase',
    6,
    true,
    'Court documents, interdict application',
    'case_2025_137857/02_evidence/legal/',
    'CRITICAL: Legal attack attempt #4 - court-sanctioned theft, Bantjies support revealed'
) ON CONFLICT DO NOTHING;

-- Event 32: Forced Medical Experimentation Threat (August 2025)
INSERT INTO timeline_events (
    event_date, event_title, description, phase, phase_number,
    is_critical, evidence_source, evidence_location, significance
) VALUES (
    '2025-08-25',
    'Forced medical experimentation threat - escalation to physical violence',
    'Threat of forced "mediation" requiring "medical evaluation". Potential forced medication/institutionalization. Medical violence under legal cover. Escalation from financial fraud to attempted physical elimination.',
    'Active Attack Phase',
    6,
    true,
    'Mediation demands, medical evaluation requirements',
    'case_2025_137857/02_evidence/legal/',
    'CRITICAL: Physical attack attempt #5 - ATTEMPTED MURDER via medical violence'
) ON CONFLICT DO NOTHING;

-- ============================================
-- 3. ADD NEW ENTITY RELATIONSHIPS
-- ============================================

-- Bantjies relationships for Event 24 (Secret Trustee Installation)
INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Danie Bantjies', 'Person', 'Secret trustee'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Danie Bantjies' 
    AND role_in_event = 'Secret trustee'
);

INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Peter Faucitt', 'Person', 'Conspiracy coordinator'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Peter Faucitt' 
    AND role_in_event = 'Conspiracy coordinator'
);

INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Rynette Farrar', 'Person', 'Installation coordinator'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Rynette Farrar' 
    AND role_in_event = 'Installation coordinator'
);

INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Jacqui Faucitt', 'Person', 'Copied (aware)'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Jacqui Faucitt' 
    AND role_in_event = 'Copied (aware)'
);

INSERT INTO timeline_event_entities (event_id, entity_name, entity_type, role_in_event)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Daniel Faucitt', 'Person', 'Excluded victim'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_entities 
    WHERE entity_name = 'Daniel Faucitt' 
    AND role_in_event = 'Excluded victim'
);

-- ============================================
-- 4. ADD NEW TRANSACTION EDGES
-- ============================================

-- Conspiracy edge: Bantjies → Peter
INSERT INTO timeline_event_transactions (
    event_id, from_entity, to_entity, transaction_type, amount_zar, description
)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Bantjies secretly installed%'),
    'Danie Bantjies', 'Peter Faucitt', 'Criminal Conspiracy', 
    18600000.00,
    'Conspiracy to defraud Dan of R18.6M May 2026 payout via secret trustee installation'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_transactions 
    WHERE from_entity = 'Danie Bantjies' 
    AND to_entity = 'Peter Faucitt'
    AND transaction_type = 'Criminal Conspiracy'
);

-- Betrayal edge: Bantjies → Dan
INSERT INTO timeline_event_transactions (
    event_id, from_entity, to_entity, transaction_type, amount_zar, description
)
SELECT 
    (SELECT id FROM timeline_events WHERE event_title LIKE '%Dan unknowingly reports fraud%'),
    'Danie Bantjies', 'Daniel Faucitt', 'Fiduciary Breach', 
    0,
    'Bantjies receives Dan''s fraud reports while being complicit perpetrator and secret trustee'
WHERE NOT EXISTS (
    SELECT 1 FROM timeline_event_transactions 
    WHERE from_entity = 'Danie Bantjies' 
    AND to_entity = 'Daniel Faucitt'
    AND transaction_type = 'Fiduciary Breach'
);

-- ============================================
-- 5. UPDATE SUMMARY VIEW
-- ============================================

-- Refresh the summary view with new data
DROP VIEW IF EXISTS timeline_summary;
CREATE VIEW timeline_summary AS
SELECT 
    te.id,
    te.event_date,
    te.event_title,
    te.phase,
    te.phase_number,
    te.is_critical,
    COUNT(DISTINCT tee.entity_name) as entity_count,
    COUNT(DISTINCT tet.id) as transaction_count,
    COALESCE(SUM(tet.amount_zar), 0) as total_amount,
    te.evidence_source,
    te.evidence_location,
    te.description,
    te.significance
FROM timeline_events te
LEFT JOIN timeline_event_entities tee ON te.id = tee.event_id
LEFT JOIN timeline_event_transactions tet ON te.id = tet.event_id
GROUP BY te.id, te.event_date, te.event_title, te.phase, te.phase_number, 
         te.is_critical, te.evidence_source, te.evidence_location, 
         te.description, te.significance
ORDER BY te.event_date;

-- ============================================
-- 6. CREATE NEW PHASE DEFINITIONS
-- ============================================

-- Add new phases to the timeline
-- Phase 5: Conspiracy Preparation (July 2024 - April 2025)
-- Phase 6: Active Attack Phase (May 2025 - August 2025)

COMMENT ON COLUMN timeline_events.phase_number IS 
'Phase 1: Financial Structure Establishment (2019-2020)
Phase 2: Business Relationship Development (2017-2021)
Phase 3: Debt Accumulation and Manipulation (2022-2023)
Phase 4: Fraud Discovery and Cover-up (May 2025)
Phase 5: Conspiracy Preparation (July 2024 - April 2025)
Phase 6: Active Attack Phase (May 2025 - August 2025)';

-- ============================================
-- 7. VERIFICATION QUERIES
-- ============================================

-- Verify new events added
SELECT COUNT(*) as new_events_count 
FROM timeline_events 
WHERE event_date >= '2024-07-01';

-- Verify Bantjies entity relationships
SELECT COUNT(*) as bantjies_relationships
FROM timeline_event_entities
WHERE entity_name = 'Danie Bantjies';

-- Verify new conspiracy transactions
SELECT * FROM timeline_event_transactions
WHERE transaction_type IN ('Criminal Conspiracy', 'Fiduciary Breach');

-- Show updated timeline summary
SELECT * FROM timeline_summary
WHERE event_date >= '2024-07-01'
ORDER BY event_date;

