-- Database Schema Improvements for rzonedevops/analysis
-- Simplified version without dollar-quoted strings

-- Synchronization log table
CREATE TABLE IF NOT EXISTS sync_operations (
    sync_id SERIAL PRIMARY KEY,
    operation_type TEXT NOT NULL,
    target_database TEXT NOT NULL,
    status TEXT NOT NULL,
    files_processed INTEGER DEFAULT 0,
    records_synced INTEGER DEFAULT 0,
    error_message TEXT,
    sync_metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_sync_operations_created_at ON sync_operations(created_at);
CREATE INDEX IF NOT EXISTS idx_sync_operations_status ON sync_operations(status);
CREATE INDEX IF NOT EXISTS idx_sync_operations_type ON sync_operations(operation_type);

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

CREATE INDEX IF NOT EXISTS idx_migrations_name ON database_migrations(migration_name);
CREATE INDEX IF NOT EXISTS idx_migrations_applied_at ON database_migrations(applied_at);

-- Repository changes tracking
CREATE TABLE IF NOT EXISTS repository_changes (
    change_id SERIAL PRIMARY KEY,
    commit_hash TEXT,
    change_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    change_description TEXT,
    requires_sync BOOLEAN DEFAULT FALSE,
    sync_completed BOOLEAN DEFAULT FALSE,
    sync_operation_id INTEGER,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    synced_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX IF NOT EXISTS idx_repo_changes_type ON repository_changes(change_type);
CREATE INDEX IF NOT EXISTS idx_repo_changes_sync_status ON repository_changes(sync_completed);
CREATE INDEX IF NOT EXISTS idx_repo_changes_detected_at ON repository_changes(detected_at);

-- CI/CD workflow runs tracking
CREATE TABLE IF NOT EXISTS workflow_runs (
    run_id SERIAL PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    trigger_event TEXT,
    branch_name TEXT,
    commit_hash TEXT,
    status TEXT NOT NULL,
    run_metadata JSONB,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER
);

CREATE INDEX IF NOT EXISTS idx_workflow_runs_name ON workflow_runs(workflow_name);
CREATE INDEX IF NOT EXISTS idx_workflow_runs_status ON workflow_runs(status);
CREATE INDEX IF NOT EXISTS idx_workflow_runs_started_at ON workflow_runs(started_at);

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

CREATE INDEX IF NOT EXISTS idx_quality_metrics_commit ON code_quality_metrics(commit_hash);
CREATE INDEX IF NOT EXISTS idx_quality_metrics_measured_at ON code_quality_metrics(measured_at);

