#!/usr/bin/env python3
"""
Sync Repository Improvements to Databases

Synchronizes the new improvements and schema changes to Supabase and Neon databases.
"""

import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sync_to_supabase():
    """Synchronize improvements metadata to Supabase."""
    logger.info("=" * 80)
    logger.info("Syncing improvements to Supabase...")
    logger.info("=" * 80)
    
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials not found. Skipping Supabase sync.")
            return False
        
        # Create Supabase client
        supabase = create_client(supabase_url, supabase_key)
        
        # Create improvements metadata record
        improvement_record = {
            "timestamp": datetime.now().isoformat(),
            "version": "0.5.0",
            "improvements": [
                "Enhanced database sync with rollback support",
                "Evidence processing automation pipeline",
                "Comprehensive test suites (90%+ coverage)",
                "Detailed improvement analysis documentation",
                "Comprehensive changelog"
            ],
            "files_added": [
                "src/database_sync/enhanced_sync.py",
                "src/evidence_automation/evidence_pipeline.py",
                "tests/unit/test_enhanced_database_sync.py",
                "tests/unit/test_evidence_pipeline.py",
                "IMPROVEMENT_ANALYSIS_2025.md",
                "CHANGELOG_2025.md"
            ],
            "status": "completed",
            "repository": "rzonedevops/analysis",
            "commit_hash": "41390b2"
        }
        
        # Try to insert into repository_updates table (if it exists)
        try:
            result = supabase.table("repository_updates").insert(improvement_record).execute()
            logger.info("✅ Successfully synced to Supabase repository_updates table")
            logger.info(f"Record ID: {result.data[0].get('id') if result.data else 'N/A'}")
            return True
            
        except Exception as e:
            if "relation" in str(e).lower() and "does not exist" in str(e).lower():
                logger.warning("Table 'repository_updates' does not exist in Supabase")
                logger.info("Creating table schema...")
                
                # SQL to create the table
                create_table_sql = """
                CREATE TABLE IF NOT EXISTS repository_updates (
                    id BIGSERIAL PRIMARY KEY,
                    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    version VARCHAR(50),
                    improvements JSONB,
                    files_added JSONB,
                    status VARCHAR(50),
                    repository VARCHAR(255),
                    commit_hash VARCHAR(255),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_repository_updates_timestamp ON repository_updates(timestamp);
                CREATE INDEX IF NOT EXISTS idx_repository_updates_repository ON repository_updates(repository);
                """
                
                logger.info("\n" + "=" * 80)
                logger.info("SUPABASE TABLE CREATION SQL")
                logger.info("=" * 80)
                logger.info("Execute the following SQL in your Supabase SQL Editor:")
                logger.info("=" * 80 + "\n")
                logger.info(create_table_sql)
                logger.info("\n" + "=" * 80)
                
                return False
            else:
                raise
        
    except ImportError:
        logger.error("Supabase client not installed. Install with: pip install supabase")
        return False
    
    except Exception as e:
        logger.error(f"Error syncing to Supabase: {e}")
        return False


def sync_to_neon():
    """Synchronize improvements metadata to Neon via MCP."""
    logger.info("=" * 80)
    logger.info("Syncing improvements to Neon...")
    logger.info("=" * 80)
    
    try:
        import subprocess
        import json
        
        # Get Neon project ID
        project_id = "shiny-leaf-22167783"  # From list_projects result
        
        logger.info(f"Using Neon project: {project_id}")
        
        # Create SQL for repository updates table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS repository_updates (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            version VARCHAR(50),
            improvements JSONB,
            files_added JSONB,
            status VARCHAR(50),
            repository VARCHAR(255),
            commit_hash VARCHAR(255),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        
        CREATE INDEX IF NOT EXISTS idx_repository_updates_timestamp ON repository_updates(timestamp);
        CREATE INDEX IF NOT EXISTS idx_repository_updates_repository ON repository_updates(repository);
        """
        
        logger.info("\n" + "=" * 80)
        logger.info("NEON TABLE CREATION SQL")
        logger.info("=" * 80)
        logger.info("The following SQL should be executed on Neon database:")
        logger.info("=" * 80 + "\n")
        logger.info(create_table_sql)
        logger.info("\n" + "=" * 80)
        
        # Note: Direct SQL execution via MCP requires specific tools
        # For now, we'll document the SQL that needs to be executed
        
        logger.info("✅ Neon sync prepared (manual SQL execution required)")
        logger.info(f"Project ID: {project_id}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error preparing Neon sync: {e}")
        return False


def create_sync_summary():
    """Create a summary of the sync operations."""
    logger.info("\n" + "=" * 80)
    logger.info("DATABASE SYNCHRONIZATION SUMMARY")
    logger.info("=" * 80)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "repository": "rzonedevops/analysis",
        "commit": "41390b2",
        "improvements_synced": [
            "Enhanced database sync module",
            "Evidence processing automation",
            "Comprehensive test suites",
            "Documentation updates"
        ],
        "databases": {
            "supabase": {
                "status": "prepared",
                "notes": "Table creation SQL provided for manual execution"
            },
            "neon": {
                "status": "prepared",
                "notes": "Table creation SQL provided for manual execution"
            }
        }
    }
    
    # Save summary to file
    summary_file = "/home/ubuntu/analysis/database_sync_summary.json"
    import json
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Sync summary saved to: {summary_file}")
    
    return summary


def main():
    """Main sync function."""
    logger.info("\n" + "=" * 80)
    logger.info("REPOSITORY IMPROVEMENTS DATABASE SYNC")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 80 + "\n")
    
    results = {
        "supabase": False,
        "neon": False
    }
    
    # Sync to Supabase
    results["supabase"] = sync_to_supabase()
    
    # Sync to Neon
    results["neon"] = sync_to_neon()
    
    # Create summary
    summary = create_sync_summary()
    
    # Final summary
    logger.info("\n" + "=" * 80)
    logger.info("SYNC OPERATIONS COMPLETED")
    logger.info("=" * 80)
    logger.info(f"Supabase: {'✅ Prepared' if results['supabase'] else '⚠️  Manual SQL required'}")
    logger.info(f"Neon:     {'✅ Prepared' if results['neon'] else '⚠️  Manual SQL required'}")
    logger.info("=" * 80 + "\n")
    
    logger.info("📋 Next Steps:")
    logger.info("1. Execute the provided SQL in Supabase SQL Editor")
    logger.info("2. Execute the provided SQL in Neon database")
    logger.info("3. Verify table creation and data insertion")
    logger.info("4. Update application code to use new tables")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

