#!/usr/bin/env python3
"""
Execute Neon Database Migrations via MCP

This script executes the database migrations on Neon using the MCP server.
"""

import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Neon project details
PROJECT_ID = "sweet-sea-69912135"
BRANCH_ID = "br-sweet-lab-a8q8jg5j"

# SQL migrations
MIGRATIONS = [
    # Evidence table
    """CREATE TABLE IF NOT EXISTS evidence (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        case_id text NOT NULL,
        evidence_type text NOT NULL,
        description text,
        file_path text,
        hash text,
        collected_date timestamptz,
        collected_by text,
        chain_of_custody jsonb,
        metadata jsonb,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON evidence(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_evidence_type ON evidence(evidence_type)",
    "CREATE INDEX IF NOT EXISTS idx_evidence_collected_date ON evidence(collected_date)",
    
    # Timeline events table
    """CREATE TABLE IF NOT EXISTS timeline_events (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        case_id text NOT NULL,
        event_date timestamptz NOT NULL,
        event_type text NOT NULL,
        description text,
        actors jsonb,
        evidence_ids jsonb,
        location text,
        verified boolean DEFAULT false,
        confidence_score float,
        metadata jsonb,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_timeline_case_id ON timeline_events(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_timeline_event_date ON timeline_events(event_date)",
    "CREATE INDEX IF NOT EXISTS idx_timeline_event_type ON timeline_events(event_type)",
    
    # Entities table
    """CREATE TABLE IF NOT EXISTS entities (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        case_id text NOT NULL,
        entity_type text NOT NULL,
        name text NOT NULL,
        role text,
        attributes jsonb,
        relationships jsonb,
        metadata jsonb,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_entities_case_id ON entities(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type)",
    "CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)",
    
    # Hypergraph nodes table
    """CREATE TABLE IF NOT EXISTS hypergraph_nodes (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        case_id text NOT NULL,
        node_type text NOT NULL,
        entity_id uuid,
        properties jsonb,
        embedding jsonb,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_case_id ON hypergraph_nodes(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_type ON hypergraph_nodes(node_type)",
    
    # Hypergraph edges table
    """CREATE TABLE IF NOT EXISTS hypergraph_edges (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        case_id text NOT NULL,
        edge_type text NOT NULL,
        source_nodes jsonb NOT NULL,
        target_nodes jsonb NOT NULL,
        weight float DEFAULT 1.0,
        properties jsonb,
        created_at timestamptz DEFAULT now(),
        updated_at timestamptz DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_case_id ON hypergraph_edges(case_id)",
    "CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_type ON hypergraph_edges(edge_type)",
    
    # Sync log table
    """CREATE TABLE IF NOT EXISTS sync_log (
        id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
        sync_type text NOT NULL,
        source_db text NOT NULL,
        target_db text NOT NULL,
        status text NOT NULL,
        records_synced integer DEFAULT 0,
        errors jsonb,
        started_at timestamptz NOT NULL,
        completed_at timestamptz,
        metadata jsonb
    )""",
    "CREATE INDEX IF NOT EXISTS idx_sync_log_type ON sync_log(sync_type)",
    "CREATE INDEX IF NOT EXISTS idx_sync_log_status ON sync_log(status)",
    "CREATE INDEX IF NOT EXISTS idx_sync_log_started_at ON sync_log(started_at)",
]


def execute_sql(sql: str) -> bool:
    """Execute SQL via Neon MCP server."""
    try:
        # Prepare the input
        input_data = {
            "params": {
                "projectId": PROJECT_ID,
                "branchId": BRANCH_ID,
                "sql": sql
            }
        }
        
        # Execute via MCP
        result = subprocess.run(
            [
                "manus-mcp-cli", "tool", "call", "run_sql",
                "--server", "neon",
                "--input", json.dumps(input_data)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            logger.info(f"✓ Executed: {sql[:80]}...")
            return True
        else:
            # Check if error is "already exists"
            if "already exists" in result.stderr.lower() or "already exists" in result.stdout.lower():
                logger.info(f"ℹ Already exists: {sql[:80]}...")
                return True
            else:
                logger.error(f"✗ Failed: {sql[:80]}...")
                logger.error(f"Error: {result.stderr}")
                return False
                
    except subprocess.TimeoutExpired:
        logger.error(f"✗ Timeout: {sql[:80]}...")
        return False
    except Exception as e:
        logger.error(f"✗ Exception: {sql[:80]}... - {e}")
        return False


def main():
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("NEON DATABASE MIGRATION")
    logger.info(f"Project: {PROJECT_ID}")
    logger.info(f"Branch: {BRANCH_ID}")
    logger.info("=" * 80)
    
    success_count = 0
    failed_count = 0
    
    for i, sql in enumerate(MIGRATIONS, 1):
        logger.info(f"\n[{i}/{len(MIGRATIONS)}] Executing migration...")
        if execute_sql(sql):
            success_count += 1
        else:
            failed_count += 1
    
    logger.info("\n" + "=" * 80)
    logger.info("MIGRATION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Total migrations: {len(MIGRATIONS)}")
    logger.info(f"Successful: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info("=" * 80)
    
    if failed_count == 0:
        logger.info("✅ All migrations completed successfully!")
    else:
        logger.warning(f"⚠️  {failed_count} migration(s) failed.")


if __name__ == "__main__":
    main()

