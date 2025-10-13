-- Database Migration SQL for rzonedevops/analysis
-- Generated: October 11, 2025
-- Purpose: Schema synchronization for Supabase and Neon databases

-- ============================================================================
-- Table: evidence
-- ============================================================================

CREATE TABLE IF NOT EXISTS "evidence" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "case_id" text NOT NULL,
  "evidence_type" text NOT NULL,
  "description" text,
  "file_path" text,
  "hash" text,
  "collected_date" timestamptz,
  "collected_by" text,
  "chain_of_custody" jsonb,
  "metadata" jsonb,
  "created_at" timestamptz DEFAULT now(),
  "updated_at" timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON "evidence"(case_id);
CREATE INDEX IF NOT EXISTS idx_evidence_type ON "evidence"(evidence_type);
CREATE INDEX IF NOT EXISTS idx_evidence_collected_date ON "evidence"(collected_date);

-- ============================================================================
-- Table: timeline_events
-- ============================================================================

CREATE TABLE IF NOT EXISTS "timeline_events" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "case_id" text NOT NULL,
  "event_date" timestamptz NOT NULL,
  "event_type" text NOT NULL,
  "description" text,
  "actors" jsonb,
  "evidence_ids" jsonb,
  "location" text,
  "verified" boolean DEFAULT false,
  "confidence_score" float,
  "metadata" jsonb,
  "created_at" timestamptz DEFAULT now(),
  "updated_at" timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_timeline_case_id ON "timeline_events"(case_id);
CREATE INDEX IF NOT EXISTS idx_timeline_event_date ON "timeline_events"(event_date);
CREATE INDEX IF NOT EXISTS idx_timeline_event_type ON "timeline_events"(event_type);

-- ============================================================================
-- Table: entities
-- ============================================================================

CREATE TABLE IF NOT EXISTS "entities" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "case_id" text NOT NULL,
  "entity_type" text NOT NULL,
  "name" text NOT NULL,
  "role" text,
  "attributes" jsonb,
  "relationships" jsonb,
  "metadata" jsonb,
  "created_at" timestamptz DEFAULT now(),
  "updated_at" timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_entities_case_id ON "entities"(case_id);
CREATE INDEX IF NOT EXISTS idx_entities_type ON "entities"(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_name ON "entities"(name);

-- ============================================================================
-- Table: hypergraph_nodes
-- ============================================================================

CREATE TABLE IF NOT EXISTS "hypergraph_nodes" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "case_id" text NOT NULL,
  "node_type" text NOT NULL,
  "entity_id" uuid,
  "properties" jsonb,
  "embedding" jsonb,
  "created_at" timestamptz DEFAULT now(),
  "updated_at" timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_case_id ON "hypergraph_nodes"(case_id);
CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_type ON "hypergraph_nodes"(node_type);

-- ============================================================================
-- Table: hypergraph_edges
-- ============================================================================

CREATE TABLE IF NOT EXISTS "hypergraph_edges" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "case_id" text NOT NULL,
  "edge_type" text NOT NULL,
  "source_nodes" jsonb NOT NULL,
  "target_nodes" jsonb NOT NULL,
  "weight" float DEFAULT 1.0,
  "properties" jsonb,
  "created_at" timestamptz DEFAULT now(),
  "updated_at" timestamptz DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_case_id ON "hypergraph_edges"(case_id);
CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_type ON "hypergraph_edges"(edge_type);

-- ============================================================================
-- Table: sync_log
-- ============================================================================

CREATE TABLE IF NOT EXISTS "sync_log" (
  "id" uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  "sync_type" text NOT NULL,
  "source_db" text NOT NULL,
  "target_db" text NOT NULL,
  "status" text NOT NULL,
  "records_synced" integer DEFAULT 0,
  "errors" jsonb,
  "started_at" timestamptz NOT NULL,
  "completed_at" timestamptz,
  "metadata" jsonb
);

CREATE INDEX IF NOT EXISTS idx_sync_log_type ON "sync_log"(sync_type);
CREATE INDEX IF NOT EXISTS idx_sync_log_status ON "sync_log"(status);
CREATE INDEX IF NOT EXISTS idx_sync_log_started_at ON "sync_log"(started_at);

-- ============================================================================
-- End of migrations
-- ============================================================================

