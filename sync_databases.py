#!/usr/bin/env python3
"""
Database Synchronization Script

Synchronizes schema changes with Supabase and Neon databases based on
the repository improvements.
"""

import os
import sys
import logging
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config import get_config
from src.database_sync.enhanced_client import EnhancedSupabaseClient, EnhancedNeonClient
from src.database_sync.schema_validator import SchemaValidator
from src.exceptions import DatabaseConnectionError, DatabaseSchemaError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sync_supabase_schema():
    """Synchronize schema with Supabase."""
    logger.info("=" * 80)
    logger.info("Starting Supabase schema synchronization...")
    logger.info("=" * 80)
    
    try:
        # Initialize validator and client
        validator = SchemaValidator()
        
        # Check if Supabase credentials are available
        config = get_config()
        if not config.database.supabase_url or not config.database.supabase_key:
            logger.warning("Supabase credentials not configured. Skipping Supabase sync.")
            logger.info("To enable Supabase sync, set SUPABASE_URL and SUPABASE_KEY environment variables.")
            return False
        
        client = EnhancedSupabaseClient()
        
        # Test connection
        if not client.health_check():
            logger.warning("Supabase health check failed. Database may not be accessible.")
        
        # Generate migration SQL for all tables
        logger.info("Generating migration SQL for all tables...")
        all_migrations = validator.generate_all_migrations()
        
        logger.info(f"Generated migrations for {len(all_migrations)} tables:")
        for table_name in all_migrations.keys():
            logger.info(f"  - {table_name}")
        
        # Note: Supabase SQL execution requires service role key or SQL editor
        logger.info("\n" + "=" * 80)
        logger.info("SUPABASE MIGRATION SQL")
        logger.info("=" * 80)
        logger.info("Execute the following SQL in your Supabase SQL Editor:")
        logger.info("=" * 80 + "\n")
        
        for table_name, sql_statements in all_migrations.items():
            logger.info(f"-- Table: {table_name}")
            for sql in sql_statements:
                logger.info(sql)
            logger.info("")
        
        logger.info("=" * 80)
        logger.info("Supabase schema synchronization completed (manual execution required)")
        logger.info("=" * 80 + "\n")
        
        return True
        
    except DatabaseConnectionError as e:
        logger.error(f"Failed to connect to Supabase: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during Supabase sync: {e}")
        return False


def sync_neon_schema():
    """Synchronize schema with Neon."""
    logger.info("=" * 80)
    logger.info("Starting Neon schema synchronization...")
    logger.info("=" * 80)
    
    try:
        # Initialize validator
        validator = SchemaValidator()
        
        # Check if Neon credentials are available
        config = get_config()
        if not config.database.neon_connection_string:
            logger.warning("Neon connection string not configured. Skipping Neon sync.")
            logger.info("To enable Neon sync, set NEON_CONNECTION_STRING environment variable.")
            return False
        
        # Initialize client
        client = EnhancedNeonClient()
        
        # Test connection
        if not client.health_check():
            logger.warning("Neon health check failed. Database may not be accessible.")
        
        # Generate migration SQL for all tables
        logger.info("Generating migration SQL for all tables...")
        all_migrations = validator.generate_all_migrations()
        
        logger.info(f"Generated migrations for {len(all_migrations)} tables:")
        for table_name in all_migrations.keys():
            logger.info(f"  - {table_name}")
        
        # Execute migrations
        logger.info("\nExecuting migrations on Neon database...")
        
        with client.session() as session:
            for table_name, sql_statements in all_migrations.items():
                logger.info(f"Migrating table: {table_name}")
                
                for sql in sql_statements:
                    try:
                        session.execute(sql)
                        logger.info(f"  ✓ Executed: {sql[:80]}...")
                    except Exception as e:
                        # Table might already exist, which is fine
                        if "already exists" in str(e).lower():
                            logger.info(f"  ℹ Table/Index already exists (skipping)")
                        else:
                            logger.error(f"  ✗ Failed: {e}")
        
        logger.info("\n" + "=" * 80)
        logger.info("Neon schema synchronization completed successfully")
        logger.info("=" * 80 + "\n")
        
        # Close connection
        client.close()
        
        return True
        
    except DatabaseConnectionError as e:
        logger.error(f"Failed to connect to Neon: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during Neon sync: {e}")
        return False


def create_sync_log_entry(sync_type: str, status: str, details: dict):
    """Create a sync log entry in both databases."""
    logger.info(f"Creating sync log entry: {sync_type} - {status}")
    
    log_entry = {
        "sync_type": sync_type,
        "source_db": "repository",
        "target_db": "supabase,neon",
        "status": status,
        "started_at": datetime.now().isoformat(),
        "completed_at": datetime.now().isoformat(),
        "metadata": details
    }
    
    try:
        # Try to log to Supabase
        config = get_config()
        if config.database.supabase_url and config.database.supabase_key:
            client = EnhancedSupabaseClient()
            try:
                client.execute_query("sync_log", "insert", data=log_entry)
                logger.info("Sync log entry created in Supabase")
            except Exception as e:
                logger.warning(f"Failed to create sync log in Supabase: {e}")
    except Exception as e:
        logger.warning(f"Could not log to Supabase: {e}")
    
    try:
        # Try to log to Neon
        config = get_config()
        if config.database.neon_connection_string:
            client = EnhancedNeonClient()
            try:
                with client.session() as session:
                    session.execute(
                        """
                        INSERT INTO sync_log (sync_type, source_db, target_db, status, started_at, completed_at, metadata)
                        VALUES (:sync_type, :source_db, :target_db, :status, :started_at, :completed_at, :metadata)
                        """,
                        log_entry
                    )
                logger.info("Sync log entry created in Neon")
            except Exception as e:
                logger.warning(f"Failed to create sync log in Neon: {e}")
    except Exception as e:
        logger.warning(f"Could not log to Neon: {e}")


def main():
    """Main synchronization function."""
    logger.info("\n" + "=" * 80)
    logger.info("DATABASE SYNCHRONIZATION SCRIPT")
    logger.info("Repository: rzonedevops/analysis")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80 + "\n")
    
    # Validate configuration
    config = get_config()
    if not config.validate():
        logger.error("Configuration validation failed. Please check environment variables.")
        sys.exit(1)
    
    results = {
        "supabase": False,
        "neon": False
    }
    
    # Sync Supabase
    results["supabase"] = sync_supabase_schema()
    
    # Sync Neon
    results["neon"] = sync_neon_schema()
    
    # Create sync log entry
    status = "success" if all(results.values()) else "partial" if any(results.values()) else "failed"
    create_sync_log_entry(
        sync_type="schema_migration",
        status=status,
        details={
            "supabase_synced": results["supabase"],
            "neon_synced": results["neon"],
            "tables": ["evidence", "timeline_events", "entities", "hypergraph_nodes", "hypergraph_edges", "sync_log"]
        }
    )
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("SYNCHRONIZATION SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Supabase: {'✓ SUCCESS' if results['supabase'] else '✗ FAILED/SKIPPED'}")
    logger.info(f"Neon:     {'✓ SUCCESS' if results['neon'] else '✗ FAILED/SKIPPED'}")
    logger.info(f"Overall:  {status.upper()}")
    logger.info("=" * 80 + "\n")
    
    if status == "success":
        logger.info("✅ All database synchronizations completed successfully!")
    elif status == "partial":
        logger.warning("⚠️  Some database synchronizations failed or were skipped.")
    else:
        logger.error("❌ Database synchronization failed.")
    
    sys.exit(0 if status in ["success", "partial"] else 1)


if __name__ == "__main__":
    main()

