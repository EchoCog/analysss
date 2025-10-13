-- Database Schema Improvements for rzonedevops/analysis
-- Date: 2025-10-12
-- Purpose: Add tables to track synchronization, migrations, and repository changes

-- Synchronization log table
CREATE TABLE IF NOT EXISTS sync_operations (
    sync_id SERIAL PRIMARY KEY,
    operation_type TEXT NOT NULL,  -- 'schema', 'data', 'repository'
    target_database TEXT NOT NULL,  -- 'supabase', 'neon', 'both'
    status TEXT NOT NULL,  -- 'success', 'failed', 'partial'
    files_processed INTEGER DEFAULT 0,
    records_synced INTEGER DEFAULT 0,
    error_message TEXT,
    sync_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_sync_operations_created_at ON sync_operations(created_at);
CREATE INDEX idx_sync_operations_status ON sync_operations(status);
CREATE INDEX idx_sync_operations_type ON sync_operations(operation_type);

-- Migration tracking table
CREATE TABLE IF NOT EXISTS database_migrations (
    migration_id SERIAL PRIMARY KEY,
    migration_name TEXT NOT NULL,
    migration_file TEXT,
    migration_sql TEXT,
    applied_to_supabase BOOLEAN DEFAULT FALSE,
    applied_to_neon BOOLEAN DEFAULT FALSE,
    supabase_result TEXT,
    neon_result TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    applied_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_migrations_name ON database_migrations(migration_name);
CREATE INDEX idx_migrations_applied_at ON database_migrations(applied_at);

-- Repository changes tracking
CREATE TABLE IF NOT EXISTS repository_changes (
    change_id SERIAL PRIMARY KEY,
    commit_hash TEXT,
    change_type TEXT NOT NULL,  -- 'evidence', 'entities', 'timeline', 'schema', 'other'
    file_path TEXT NOT NULL,
    change_description TEXT,
    requires_sync BOOLEAN DEFAULT FALSE,
    sync_completed BOOLEAN DEFAULT FALSE,
    sync_operation_id INTEGER REFERENCES sync_operations(sync_id),
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    synced_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_repo_changes_type ON repository_changes(change_type);
CREATE INDEX idx_repo_changes_sync_status ON repository_changes(sync_completed);
CREATE INDEX idx_repo_changes_detected_at ON repository_changes(detected_at);

-- CI/CD workflow runs tracking
CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id SERIAL PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    workflow_type TEXT NOT NULL,  -- 'test', 'sync', 'deploy', 'scan'
    trigger_event TEXT,  -- 'push', 'pull_request', 'workflow_dispatch'
    branch_name TEXT,
    commit_hash TEXT,
    status TEXT NOT NULL,  -- 'running', 'success', 'failed', 'cancelled'
    run_metadata JSONB,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER
);

CREATE INDEX idx_workflow_runs_name ON workflow_runs(workflow_name);
CREATE INDEX idx_workflow_runs_status ON workflow_runs(status);
CREATE INDEX idx_workflow_runs_started_at ON workflow_runs(started_at);

-- Code quality metrics tracking
CREATE TABLE IF NOT EXISTS code_quality_metrics (
    metric_id SERIAL PRIMARY KEY,
    commit_hash TEXT NOT NULL,
    test_coverage_percent DECIMAL(5,2),
    total_tests INTEGER,
    passed_tests INTEGER,
    failed_tests INTEGER,
    code_quality_score DECIMAL(5,2),
    security_issues INTEGER,
    type_check_errors INTEGER,
    linting_errors INTEGER,
    measured_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_quality_metrics_commit ON code_quality_metrics(commit_hash);
CREATE INDEX idx_quality_metrics_measured_at ON code_quality_metrics(measured_at);

-- Add metadata columns to existing evidence table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'evidence' AND column_name = 'sync_status'
    ) THEN
        ALTER TABLE evidence ADD COLUMN sync_status TEXT DEFAULT 'pending';
        ALTER TABLE evidence ADD COLUMN last_synced_at TIMESTAMP WITH TIME ZONE;
        ALTER TABLE evidence ADD COLUMN sync_error TEXT;
    END IF;
END $$;

-- Add metadata columns to existing entities table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'entities' AND column_name = 'sync_status'
    ) THEN
        ALTER TABLE entities ADD COLUMN sync_status TEXT DEFAULT 'pending';
        ALTER TABLE entities ADD COLUMN last_synced_at TIMESTAMP WITH TIME ZONE;
        ALTER TABLE entities ADD COLUMN sync_error TEXT;
    END IF;
END $$;

-- Add metadata columns to existing events table (if not exists)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'events' AND column_name = 'sync_status'
    ) THEN
        ALTER TABLE events ADD COLUMN sync_status TEXT DEFAULT 'pending';
        ALTER TABLE events ADD COLUMN last_synced_at TIMESTAMP WITH TIME ZONE;
        ALTER TABLE events ADD COLUMN sync_error TEXT;
    END IF;
END $$;

-- Create view for sync operation summary
CREATE OR REPLACE VIEW sync_operation_summary AS
SELECT 
    operation_type,
    target_database,
    status,
    COUNT(*) as total_operations,
    SUM(files_processed) as total_files,
    SUM(records_synced) as total_records,
    MAX(created_at) as last_sync_time
FROM sync_operations
GROUP BY operation_type, target_database, status;

-- Create view for migration status
CREATE OR REPLACE VIEW migration_status AS
SELECT 
    migration_name,
    CASE 
        WHEN applied_to_supabase AND applied_to_neon THEN 'fully_applied'
        WHEN applied_to_supabase OR applied_to_neon THEN 'partially_applied'
        ELSE 'pending'
    END as status,
    applied_at
FROM database_migrations
ORDER BY applied_at DESC NULLS LAST;

-- Create view for recent workflow runs
CREATE OR REPLACE VIEW recent_workflow_runs AS
SELECT 
    workflow_name,
    workflow_type,
    status,
    branch_name,
    started_at,
    duration_seconds
FROM workflow_runs
WHERE started_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
ORDER BY started_at DESC;

-- Grant permissions (adjust as needed for your setup)
-- GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- Add comments for documentation
COMMENT ON TABLE sync_operations IS 'Tracks all database synchronization operations between repository and databases';
COMMENT ON TABLE database_migrations IS 'Records all database migrations and their application status';
COMMENT ON TABLE repository_changes IS 'Logs repository changes that may require database synchronization';
COMMENT ON TABLE workflow_runs IS 'Tracks CI/CD workflow execution and results';
COMMENT ON TABLE code_quality_metrics IS 'Stores code quality metrics from automated testing';

COMMENT ON VIEW sync_operation_summary IS 'Summary view of synchronization operations grouped by type and status';
COMMENT ON VIEW migration_status IS 'Current status of all database migrations';
COMMENT ON VIEW recent_workflow_runs IS 'Recent workflow runs from the last 7 days';

