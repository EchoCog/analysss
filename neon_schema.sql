-- Neon Schema Extensions for Hypergraph Analysis and Legal Compliance

-- Hypergraph optimization for legal analysis
CREATE TABLE legal_relationships (
    id SERIAL PRIMARY KEY,
    source_entity_id INTEGER,
    target_entity_id INTEGER,
    relationship_type TEXT,
    legal_basis TEXT,
    compliance_impact TEXT,
    temporal_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE compliance_monitoring (
    id SERIAL PRIMARY KEY,
    entity_id INTEGER,
    legislation_id INTEGER,
    compliance_status TEXT,
    last_assessment DATE,
    next_review DATE,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

