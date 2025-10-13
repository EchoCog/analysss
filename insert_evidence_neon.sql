-- Insert new evidence into Neon database
INSERT INTO evidence (
    id, 
    title, 
    description, 
    date_created, 
    category, 
    file_path, 
    hash, 
    entities_involved,
    metadata
) VALUES (
    'evidence_compliance_directive_2025_07_08',
    'URGENT: MANDATORY COMPLIANCE DIRECTIVE - PERSONAL CRIMINAL LIABILITY WARNING',
    'Daniel Faucitt (CIO) issues urgent compliance directive regarding illegal instructions to employees about customer data processing',
    '2025-07-08',
    'legal_compliance_directive',
    'evidence/email_compliance_directive_2025-07-08.md',
    'compliance_directive_hash',
    ARRAY['Daniel Faucitt', 'Kent', 'RegimA Distribution companies', 'RegimA Skin Treatments', 'Shopify'],
    '{"sender": "Daniel Faucitt", "recipient": "Kent", "urgency": "critical", "legal_framework": "POPI Act"}'::jsonb
);

-- Insert new event into events table
INSERT INTO events (
    id,
    event_date,
    event_type,
    title,
    description,
    entities_involved,
    evidence_id,
    metadata
) VALUES (
    'event_compliance_directive_2025_07_08',
    '2025-07-08',
    'legal_compliance_directive',
    'Compliance Directive Issued',
    'Daniel Faucitt issues urgent compliance directive warning of personal criminal liability for POPI violations',
    ARRAY['Daniel Faucitt', 'Kent', 'RegimA Distribution companies', 'RegimA Skin Treatments'],
    'evidence_compliance_directive_2025_07_08',
    '{"severity": "critical", "legal_act": "POPI", "penalties": {"unauthorized_access": "10 years imprisonment", "processing_violations": "R10 million fine"}}'::jsonb
);

-- Insert new entities
INSERT INTO entities (id, name, type, description, metadata) VALUES 
('entity_daniel_faucitt', 'Daniel Faucitt', 'person', 'Chief Information Officer (CIO) at RegimA', '{"role": "CIO", "email": "dan@regima.com", "authority_level": "executive"}'::jsonb),
('entity_kent_recipient', 'Kent', 'person', 'Employee at RegimA', '{"email": "kent@regima.zone", "authority_level": "employee"}'::jsonb),
('entity_regima_distribution', 'RegimA Distribution companies', 'organization', 'Legal owner of customer data', '{"data_ownership": "customer_data_owner", "legal_status": "authorized"}'::jsonb),
('entity_regima_skin_treatments', 'RegimA Skin Treatments', 'organization', 'Unauthorized third party to customer data', '{"data_ownership": "unauthorized_third_party", "legal_status": "unauthorized", "risk_level": "high"}'::jsonb),
('entity_shopify', 'Shopify', 'technology_platform', 'Authorized system for customer data processing', '{"authorization_status": "authorized", "function": "customer_data_processing"}'::jsonb)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    type = EXCLUDED.type,
    description = EXCLUDED.description,
    metadata = EXCLUDED.metadata;

-- Insert relationships
INSERT INTO relationships (id, from_entity_id, to_entity_id, relationship_type, description, metadata) VALUES
('rel_faucitt_regima', 'entity_daniel_faucitt', 'entity_regima_distribution', 'employment', 'Daniel Faucitt is CIO at RegimA Distribution', '{"authority": "high", "relationship": "executive_employee"}'::jsonb),
('rel_kent_regima', 'entity_kent_recipient', 'entity_regima_distribution', 'employment', 'Kent is employee at RegimA Distribution', '{"authority": "low", "relationship": "employee"}'::jsonb),
('rel_regima_shopify', 'entity_regima_distribution', 'entity_shopify', 'data_processing_authorization', 'RegimA Distribution authorizes Shopify for customer data processing', '{"status": "compliant", "relationship": "authorized_processor"}'::jsonb),
('rel_skin_treatments_risk', 'entity_regima_skin_treatments', 'entity_regima_distribution', 'unauthorized_access_risk', 'RegimA Skin Treatments poses unauthorized access risk to customer data', '{"status": "violation_risk", "relationship": "unauthorized_third_party"}'::jsonb)
ON CONFLICT (id) DO UPDATE SET
    from_entity_id = EXCLUDED.from_entity_id,
    to_entity_id = EXCLUDED.to_entity_id,
    relationship_type = EXCLUDED.relationship_type,
    description = EXCLUDED.description,
    metadata = EXCLUDED.metadata;
