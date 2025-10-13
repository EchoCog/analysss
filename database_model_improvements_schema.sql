-- Database Schema for Model Improvements
-- =========================================
-- Supports: Entities, Relations, Events, Timelines, Dynamics, HGNN, Case-LLM

-- Enhanced Entity Model Tables
-- ============================

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

-- Relationship Inference Tables
-- =============================

CREATE TABLE IF NOT EXISTS inferred_relationships (
    relationship_id VARCHAR(255) PRIMARY KEY,
    source_entity_id VARCHAR(255),
    target_entity_id VARCHAR(255),
    relationship_type VARCHAR(100) NOT NULL,
    inference_method VARCHAR(100) NOT NULL,
    confidence_score FLOAT CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    supporting_evidence JSONB DEFAULT '[]',
    inference_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    first_observed TIMESTAMP,
    last_observed TIMESTAMP,
    observation_count INTEGER DEFAULT 0,
    validated BOOLEAN DEFAULT FALSE,
    validation_timestamp TIMESTAMP,
    validation_notes TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS relationship_patterns (
    pattern_id VARCHAR(255) PRIMARY KEY,
    pattern_type VARCHAR(100) NOT NULL,
    entities_involved JSONB NOT NULL,
    relationships JSONB NOT NULL,
    pattern_strength FLOAT CHECK (pattern_strength >= 0.0 AND pattern_strength <= 1.0),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    metadata JSONB DEFAULT '{}'
);

-- Event Causality Tables
-- ======================

CREATE TABLE IF NOT EXISTS causal_relationships (
    relationship_id VARCHAR(255) PRIMARY KEY,
    cause_event_id VARCHAR(255),
    effect_event_id VARCHAR(255),
    causality_type VARCHAR(100) NOT NULL,
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    time_lag_seconds BIGINT,
    evidence JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_impacts (
    event_id VARCHAR(255) PRIMARY KEY,
    impact_level VARCHAR(50) NOT NULL,
    affected_entities JSONB DEFAULT '[]',
    affected_events JSONB DEFAULT '[]',
    impact_description TEXT,
    propagation_path JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS event_sequences (
    sequence_id VARCHAR(255) PRIMARY KEY,
    sequence_type VARCHAR(100) NOT NULL,
    events JSONB NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    pattern_strength FLOAT CHECK (pattern_strength >= 0.0 AND pattern_strength <= 1.0),
    description TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS event_anomalies (
    anomaly_id VARCHAR(255) PRIMARY KEY,
    event_id VARCHAR(255),
    anomaly_type VARCHAR(100) NOT NULL,
    anomaly_score FLOAT CHECK (anomaly_score >= 0.0 AND anomaly_score <= 1.0),
    expected_pattern TEXT,
    actual_pattern TEXT,
    detection_method VARCHAR(100),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS event_predictions (
    prediction_id VARCHAR(255) PRIMARY KEY,
    predicted_event_type VARCHAR(100) NOT NULL,
    predicted_time TIMESTAMP NOT NULL,
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    based_on_events JSONB DEFAULT '[]',
    prediction_method VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Enhanced Timeline Tables
-- ========================

CREATE TABLE IF NOT EXISTS timeline_gaps (
    gap_id VARCHAR(255) PRIMARY KEY,
    gap_type VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_hours FLOAT,
    severity FLOAT CHECK (severity >= 0.0 AND severity <= 1.0),
    description TEXT,
    surrounding_events JSONB DEFAULT '[]',
    suggested_investigation TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS timeline_conflicts (
    conflict_id VARCHAR(255) PRIMARY KEY,
    conflict_type VARCHAR(100) NOT NULL,
    conflicting_events JSONB NOT NULL,
    description TEXT,
    resolution_strategy TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    resolution_notes TEXT,
    confidence_in_resolution FLOAT CHECK (confidence_in_resolution >= 0.0 AND confidence_in_resolution <= 1.0),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS uncertainty_measures (
    uncertainty_id VARCHAR(255) PRIMARY KEY,
    event_id VARCHAR(255),
    uncertainty_type VARCHAR(100) NOT NULL,
    uncertainty_score FLOAT CHECK (uncertainty_score >= 0.0 AND uncertainty_score <= 1.0),
    lower_bound TIMESTAMP,
    upper_bound TIMESTAMP,
    confidence_interval JSONB,
    description TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS timeline_reconstructions (
    reconstruction_id VARCHAR(255) PRIMARY KEY,
    original_events JSONB NOT NULL,
    reconstructed_events JSONB NOT NULL,
    reconstruction_method VARCHAR(100),
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    assumptions JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}'
);

-- HGNN Training Tables
-- ====================

CREATE TABLE IF NOT EXISTS hypergraph_embeddings (
    embedding_id VARCHAR(255) PRIMARY KEY,
    node_embeddings JSONB NOT NULL,
    embedding_dim INTEGER NOT NULL,
    embedding_method VARCHAR(100) NOT NULL,
    training_params JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS attention_weights (
    attention_id VARCHAR(255) PRIMARY KEY,
    node_attention JSONB DEFAULT '{}',
    hyperedge_attention JSONB DEFAULT '{}',
    attention_mechanism VARCHAR(100),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS pooling_results (
    pooling_id VARCHAR(255) PRIMARY KEY,
    original_nodes JSONB NOT NULL,
    pooled_nodes JSONB NOT NULL,
    pooling_method VARCHAR(100) NOT NULL,
    pooling_scores JSONB DEFAULT '{}',
    reduction_ratio FLOAT,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS training_metrics (
    metric_id SERIAL PRIMARY KEY,
    embedding_id VARCHAR(255) REFERENCES hypergraph_embeddings(embedding_id),
    epoch INTEGER NOT NULL,
    train_loss FLOAT,
    val_loss FLOAT,
    train_accuracy FLOAT,
    val_accuracy FLOAT,
    learning_rate FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS explainability_results (
    explanation_id VARCHAR(255) PRIMARY KEY,
    prediction_id VARCHAR(255),
    important_nodes JSONB DEFAULT '[]',
    important_hyperedges JSONB DEFAULT '[]',
    explanation_method VARCHAR(100),
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    metadata JSONB DEFAULT '{}'
);

-- Agent-Based Modeling Tables
-- ===========================

CREATE TABLE IF NOT EXISTS agents (
    agent_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    behavior_type VARCHAR(100) DEFAULT 'neutral',
    goals JSONB DEFAULT '[]',
    behavior_rules JSONB DEFAULT '[]',
    current_state JSONB DEFAULT '{}',
    state_history JSONB DEFAULT '[]',
    capabilities JSONB DEFAULT '[]',
    constraints JSONB DEFAULT '{}',
    learning_rate FLOAT DEFAULT 0.1,
    experience JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS agent_interactions (
    interaction_id VARCHAR(255) PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_agent_id VARCHAR(255) REFERENCES agents(agent_id),
    target_agent_id VARCHAR(255) REFERENCES agents(agent_id),
    interaction_type VARCHAR(100) NOT NULL,
    content JSONB DEFAULT '{}',
    outcome VARCHAR(255),
    impact_on_source JSONB DEFAULT '{}',
    impact_on_target JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS emergent_patterns (
    pattern_id VARCHAR(255) PRIMARY KEY,
    pattern_type VARCHAR(100) NOT NULL,
    agents_involved JSONB NOT NULL,
    description TEXT,
    emergence_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    strength FLOAT CHECK (strength >= 0.0 AND strength <= 1.0),
    stability FLOAT CHECK (stability >= 0.0 AND stability <= 1.0),
    metadata JSONB DEFAULT '{}'
);

-- Case-LLM AAR Core Tables
-- ========================

CREATE TABLE IF NOT EXISTS aar_cores (
    case_id VARCHAR(255) PRIMARY KEY,
    agent_state JSONB DEFAULT '{}',
    agent_goals JSONB DEFAULT '[]',
    agent_capabilities JSONB DEFAULT '[]',
    arena_state JSONB DEFAULT '{}',
    arena_constraints JSONB DEFAULT '{}',
    arena_context JSONB DEFAULT '{}',
    self_representation JSONB DEFAULT '{}',
    self_beliefs JSONB DEFAULT '{}',
    self_confidence FLOAT CHECK (self_confidence >= 0.0 AND self_confidence <= 1.0),
    feedback_history JSONB DEFAULT '[]',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pattern_dynamics (
    pattern_id VARCHAR(255) PRIMARY KEY,
    case_id VARCHAR(255),
    pattern_order VARCHAR(50) NOT NULL,
    pattern_description TEXT,
    first_order_elements JSONB DEFAULT '[]',
    second_order_links JSONB DEFAULT '{}',
    third_order_influences JSONB DEFAULT '{}',
    pattern_strength FLOAT CHECK (pattern_strength >= 0.0 AND pattern_strength <= 1.0),
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS hypotheses (
    hypothesis_id VARCHAR(255) PRIMARY KEY,
    case_id VARCHAR(255),
    description TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'proposed',
    confidence FLOAT CHECK (confidence >= 0.0 AND confidence <= 1.0),
    supporting_evidence JSONB DEFAULT '[]',
    contradicting_evidence JSONB DEFAULT '[]',
    reasoning_mode VARCHAR(100) NOT NULL,
    reasoning_chain JSONB DEFAULT '[]',
    testable_predictions JSONB DEFAULT '[]',
    test_results JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS counterfactual_scenarios (
    scenario_id VARCHAR(255) PRIMARY KEY,
    case_id VARCHAR(255),
    description TEXT,
    original_events JSONB DEFAULT '[]',
    counterfactual_events JSONB DEFAULT '[]',
    key_differences JSONB DEFAULT '[]',
    predicted_outcomes JSONB DEFAULT '[]',
    outcome_probabilities JSONB DEFAULT '{}',
    insights JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS introspection_reports (
    report_id VARCHAR(255) PRIMARY KEY,
    case_id VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    self_confidence FLOAT CHECK (self_confidence >= 0.0 AND self_confidence <= 1.0),
    knowledge_gaps JSONB DEFAULT '[]',
    reasoning_quality FLOAT CHECK (reasoning_quality >= 0.0 AND reasoning_quality <= 1.0),
    detected_patterns JSONB DEFAULT '[]',
    pattern_coherence FLOAT CHECK (pattern_coherence >= 0.0 AND pattern_coherence <= 1.0),
    active_hypotheses INTEGER,
    validated_hypotheses INTEGER,
    refuted_hypotheses INTEGER,
    investigation_priorities JSONB DEFAULT '[]',
    suggested_actions JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}'
);

-- Indexes for Performance
-- =======================

CREATE INDEX idx_entities_type ON enhanced_entities(entity_type);
CREATE INDEX idx_entities_status ON enhanced_entities(status);
CREATE INDEX idx_entities_created ON enhanced_entities(created_at);

CREATE INDEX idx_relationships_source ON entity_relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON entity_relationships(target_entity_id);
CREATE INDEX idx_relationships_type ON entity_relationships(relationship_type);

CREATE INDEX idx_inferred_rel_source ON inferred_relationships(source_entity_id);
CREATE INDEX idx_inferred_rel_target ON inferred_relationships(target_entity_id);
CREATE INDEX idx_inferred_rel_method ON inferred_relationships(inference_method);

CREATE INDEX idx_causal_cause ON causal_relationships(cause_event_id);
CREATE INDEX idx_causal_effect ON causal_relationships(effect_event_id);

CREATE INDEX idx_timeline_gaps_time ON timeline_gaps(start_time, end_time);
CREATE INDEX idx_timeline_conflicts_type ON timeline_conflicts(conflict_type);

CREATE INDEX idx_agents_type ON agents(agent_type);
CREATE INDEX idx_agent_interactions_time ON agent_interactions(timestamp);

CREATE INDEX idx_hypotheses_case ON hypotheses(case_id);
CREATE INDEX idx_hypotheses_status ON hypotheses(status);

CREATE INDEX idx_patterns_case ON pattern_dynamics(case_id);
CREATE INDEX idx_patterns_order ON pattern_dynamics(pattern_order);

-- Views for Common Queries
-- ========================

CREATE OR REPLACE VIEW active_entities AS
SELECT * FROM enhanced_entities
WHERE status = 'active' AND deleted_at IS NULL;

CREATE OR REPLACE VIEW validated_hypotheses AS
SELECT * FROM hypotheses
WHERE status = 'validated';

CREATE OR REPLACE VIEW high_confidence_relationships AS
SELECT * FROM inferred_relationships
WHERE confidence_score >= 0.7 AND validated = TRUE;

CREATE OR REPLACE VIEW critical_timeline_gaps AS
SELECT * FROM timeline_gaps
WHERE severity >= 0.7;

CREATE OR REPLACE VIEW emergent_coalitions AS
SELECT * FROM emergent_patterns
WHERE pattern_type = 'coalition' AND strength >= 0.6;

