-- Supabase Schema Extensions for SA AI Legislation Compliance

-- SA AI Legislation Compliance Tables
CREATE TABLE sa_legislation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    full_name TEXT,
    year INTEGER,
    type TEXT,
    significance TEXT,
    key_requirements JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE compliance_deadlines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    legislation TEXT NOT NULL,
    severity TEXT NOT NULL,
    last_checked TIMESTAMP,
    next_due TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE ai_fraud_threats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    threat_name TEXT NOT NULL,
    threat_type TEXT NOT NULL,
    description TEXT,
    severity TEXT,
    legal_implications JSONB,
    detection_methods JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enhanced Entity Tables
CREATE TABLE entity_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID REFERENCES entities(id),
    version_date DATE NOT NULL,
    entity_data JSONB NOT NULL,
    compliance_status JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

