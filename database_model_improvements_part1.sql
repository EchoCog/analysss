-- Enhanced Entity Model Tables
CREATE TABLE IF NOT EXISTS enhanced_entities (
    entity_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    description TEXT,
    aliases JSONB DEFAULT '[]',
    tags JSONB DEFAULT '[]',
    behavioral_properties JSONB DEFAULT '{}',
    strategic_goals JSONB DEFAULT '[]',
    behavioral_rules JSONB DEFAULT '[]',
    current_state JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    archived_at TIMESTAMP,
    deleted_at TIMESTAMP,
    current_version INTEGER DEFAULT 1,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS entity_versions (
    version_id VARCHAR(255) PRIMARY KEY,
    entity_id VARCHAR(255) REFERENCES enhanced_entities(entity_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    properties JSONB NOT NULL,
    changed_by VARCHAR(255),
    change_reason TEXT,
    version_number INTEGER
);

CREATE TABLE IF NOT EXISTS entity_relationships (
    relationship_id VARCHAR(255) PRIMARY KEY,
    source_entity_id VARCHAR(255) REFERENCES enhanced_entities(entity_id),
    target_entity_id VARCHAR(255) REFERENCES enhanced_entities(entity_id),
    relationship_type VARCHAR(100) NOT NULL,
    strength FLOAT CHECK (strength >= 0.0 AND strength <= 1.0),
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    evidence_refs JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
