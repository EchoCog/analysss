-- Sync Evidence Package 2025-05-23 to Database
-- This script adds new entities, events, and relationships

-- Add new entity types if not exists
INSERT INTO entity_types (type_name, description) VALUES
('service_provider', 'External service provider or platform'),
('software_system', 'Software system or application'),
('financial_instrument', 'Payment card, bank account, or other financial instrument'),
('e_commerce_store', 'Online store or e-commerce platform')
ON CONFLICT (type_name) DO NOTHING;

-- Add Shopify International Limited
INSERT INTO case_entities (entity_id, name, entity_type, roles, metadata) VALUES
('service_shopify_international', 'Shopify International Limited', 'service_provider', 
 ARRAY['cloud_platform', 'e_commerce_provider'],
 '{"vat_number": "4820289033", "address": "2nd Floor, 1-2 Victoria Buildings, Haddington Road, Dublin 4, D04 XN32, Ireland"}'::jsonb)
ON CONFLICT (entity_id) DO UPDATE SET
  name = EXCLUDED.name,
  metadata = EXCLUDED.metadata;

-- Add Pastel System
INSERT INTO case_entities (entity_id, name, entity_type, roles, metadata) VALUES
('system_pastel_local', 'Pastel Accounting System (Local)', 'software_system',
 ARRAY['accounting_system', 'criminal_infrastructure'],
 '{"access_control": "Exclusive Rynette access", "purpose": "Repository for diverted audit trails"}'::jsonb)
ON CONFLICT (entity_id) DO UPDATE SET
  name = EXCLUDED.name,
  metadata = EXCLUDED.metadata;

-- Add Payment Cards
INSERT INTO case_entities (entity_id, name, entity_type, roles, metadata) VALUES
('payment_card_5225', 'Visa ending in 5225', 'financial_instrument',
 ARRAY['business_payment_card'],
 '{"owner": "RegimA Zone (Pty) Ltd", "status": "Cancelled June 7, 2025"}'::jsonb),
('payment_card_3212', 'Visa ending in 3212', 'financial_instrument',
 ARRAY['personal_payment_card'],
 '{"owner": "Dan/Jax Personal", "status": "Active - used for business rescue"}'::jsonb)
ON CONFLICT (entity_id) DO UPDATE SET
  name = EXCLUDED.name,
  metadata = EXCLUDED.metadata;

-- Add Shopify Stores (RegimA Zone Network)
INSERT INTO case_entities (entity_id, name, entity_type, roles, metadata) VALUES
('store_regima_dst', 'RegimA DST', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_zone_sa', 'RegimA Zone SA', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_zone', 'RegimA Zone', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_za_gp_ne', 'RegimA ZA-GP-NE', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_za_ne', 'RegimA ZA-NE', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_europe', 'RegimA Europe', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb),
('store_regima_wwd', 'RegimA WWD', 'e_commerce_store', ARRAY['shopify_store', 'regima_zone_network'],
 '{"parent": "RegimA Zone W", "status": "Audit trail ceased May 22, 2025"}'::jsonb)
ON CONFLICT (entity_id) DO UPDATE SET
  name = EXCLUDED.name,
  metadata = EXCLUDED.metadata;

-- Add Shopify Stores (RegimA SA Network)
INSERT INTO case_entities (entity_id, name, entity_type, roles, metadata) VALUES
('store_regima_za_cpt', 'RegimA ZA-CPT', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_alma', 'RegimA ZA (Alma)', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_wc', 'RegimA ZA-WC', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_dbn', 'RegimA ZA-DBN', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_ec', 'RegimA ZA-EC', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_nl', 'RegimA ZA-NL', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_romy', 'RegimA ZA (Romy)', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb),
('store_regima_za_debbie', 'RegimA ZA (Debbie)', 'e_commerce_store', ARRAY['shopify_store', 'regima_sa_network'],
 '{"parent": "RegimA SA", "status": "Sales ceased June 2025"}'::jsonb)
ON CONFLICT (entity_id) DO UPDATE SET
  name = EXCLUDED.name,
  metadata = EXCLUDED.metadata;

-- Add timeline events
INSERT INTO case_events (event_id, event_date, event_type, title, description, importance, evidence_source) VALUES
('evt_20250522_audit_trail_diversion', '2025-05-22', 'revenue_diversion',
 'Shopify Audit Trail Disappears - Revenue Diversion',
 'Orders & payment records diverted from Shopify Cloud to local Pastel instance. 15 Shopify stores affected. R34.9M+ annual revenue at risk.',
 'CRITICAL', 'evidence_package_20250523'),
('evt_20250710_payment_failure_cascade', '2025-07-10', 'payment_sabotage',
 'Payment Failure Cascade - Shopify Bill',
 'Shopify invoice #388990813 created. 24 payment failures over 78 days using cancelled card (Visa 5225). One of 300+ similar defaulting bills.',
 'HIGH', 'evidence_package_20250523'),
('evt_20250929_alternative_payment', '2025-09-29', 'forced_personal_liability',
 'Shopify Bill Paid - Personal Card',
 'Bill finally paid using Dan/Jax personal card (Visa 3212) after 78 days and 24 failures. Demonstrates forced personal liability for business expenses.',
 'MEDIUM', 'evidence_package_20250523')
ON CONFLICT (event_id) DO UPDATE SET
  event_date = EXCLUDED.event_date,
  title = EXCLUDED.title,
  description = EXCLUDED.description;

-- Add event-entity relationships
INSERT INTO event_entity_relations (event_id, entity_id, relationship_type) VALUES
('evt_20250522_audit_trail_diversion', 'service_shopify_international', 'victim_platform'),
('evt_20250522_audit_trail_diversion', 'system_pastel_local', 'receiving_system'),
('evt_20250522_audit_trail_diversion', 'store_regima_dst', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_zone_sa', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_zone', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_gp_ne', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_ne', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_europe', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_wwd', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_cpt', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_alma', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_wc', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_dbn', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_ec', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_nl', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_romy', 'affected_store'),
('evt_20250522_audit_trail_diversion', 'store_regima_za_debbie', 'affected_store'),
('evt_20250710_payment_failure_cascade', 'payment_card_5225', 'failed_payment_method'),
('evt_20250710_payment_failure_cascade', 'service_shopify_international', 'service_provider'),
('evt_20250929_alternative_payment', 'payment_card_3212', 'alternative_payment_method'),
('evt_20250929_alternative_payment', 'service_shopify_international', 'service_provider')
ON CONFLICT (event_id, entity_id, relationship_type) DO NOTHING;

-- Summary
SELECT 'Database sync completed - Evidence Package 2025-05-23' AS status;
