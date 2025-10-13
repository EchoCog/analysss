-- Database schema for the HyperGNN analysis framework

-- Entities table
CREATE TABLE entities (
    entity_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    roles TEXT[],
    attributes JSONB,
    evidence_references TEXT[],
    verification_status TEXT
);

CREATE INDEX idx_entities_entity_type ON entities(entity_type);

-- Events table
CREATE TABLE events (
    event_id TEXT PRIMARY KEY,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    description TEXT,
    participants TEXT[],
    evidence_references TEXT[],
    verification_status TEXT,
    event_type TEXT
);

CREATE INDEX idx_events_event_type ON events(event_type);
CREATE INDEX idx_events_date ON events(date);

-- Relationships table
CREATE TABLE relationships (
    relationship_id TEXT PRIMARY KEY,
    source_entity TEXT REFERENCES entities(entity_id),
    target_entity TEXT REFERENCES entities(entity_id),
    relationship_type TEXT NOT NULL,
    strength REAL,
    evidence_references TEXT[],
    verification_status TEXT
);

CREATE INDEX idx_relationships_source_entity ON relationships(source_entity);
CREATE INDEX idx_relationships_target_entity ON relationships(target_entity);
CREATE INDEX idx_relationships_relationship_type ON relationships(relationship_type);

-- Evidence table
CREATE TABLE evidence (
    evidence_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    evidence_type TEXT,
    classification_level TEXT,
    verification_status TEXT,
    source_file TEXT,
    content_length INTEGER,
    creation_date TIMESTAMP WITH TIME ZONE,
    keywords TEXT[]
);

CREATE INDEX idx_evidence_evidence_type ON evidence(evidence_type);
CREATE INDEX idx_evidence_classification_level ON evidence(classification_level);

