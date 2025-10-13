#!/usr/bin/env python3
"""
Integration Script for Codebase Refinements
==========================================

This script helps integrate the refined components into the existing codebase,
ensuring a smooth transition from mock/speculative code to accurate implementations.
"""

import os
import sys
import shutil
import sqlite3
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import get_config, Config
from utils.validators import ValidationError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RefinementIntegrator:
    """Handles integration of refined components"""
    
    def __init__(self, config: Config, dry_run: bool = False):
        self.config = config
        self.dry_run = dry_run
        self.backup_dir = Path("backups") / datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def integrate_all(self):
        """Run all integration steps"""
        logger.info("Starting codebase refinement integration...")
        
        # Create backup directory
        if not self.dry_run:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created backup directory: {self.backup_dir}")
        
        # Integration steps
        self.backup_original_files()
        self.update_imports()
        self.migrate_database()
        self.update_configuration()
        self.validate_integration()
        
        logger.info("Integration complete!")
        
    def backup_original_files(self):
        """Backup original files before modification"""
        files_to_backup = [
            "backend_api.py",
            "frameworks/hypergnn_core.py",
            "analysis_framework.db"
        ]
        
        for file_path in files_to_backup:
            src = Path(file_path)
            if src.exists():
                if self.dry_run:
                    logger.info(f"[DRY RUN] Would backup: {file_path}")
                else:
                    dst = self.backup_dir / file_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    logger.info(f"Backed up: {file_path}")
                    
    def update_imports(self):
        """Update import statements to use refined modules"""
        replacements = [
            ("from frameworks.hypergnn_core import", 
             "from frameworks.hypergnn_core_refined import"),
            ("from backend_api import",
             "from backend_api_refined import"),
        ]
        
        # Find Python files to update
        python_files = list(Path(".").rglob("*.py"))
        
        for py_file in python_files:
            # Skip refined files and this script
            if "refined" in py_file.name or py_file.name == "integrate_refinements.py":
                continue
                
            try:
                content = py_file.read_text()
                original_content = content
                
                for old_import, new_import in replacements:
                    if old_import in content:
                        content = content.replace(old_import, new_import)
                
                if content != original_content:
                    if self.dry_run:
                        logger.info(f"[DRY RUN] Would update imports in: {py_file}")
                    else:
                        py_file.write_text(content)
                        logger.info(f"Updated imports in: {py_file}")
                        
            except Exception as e:
                logger.error(f"Error updating {py_file}: {e}")
                
    def migrate_database(self):
        """Migrate database schema to refined version"""
        if self.dry_run:
            logger.info("[DRY RUN] Would migrate database schema")
            return
            
        db_path = self.config.DATABASE_PATH
        
        if not os.path.exists(db_path):
            logger.info("No existing database found, will be created on first run")
            return
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if migration is needed
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'agents' not in tables:
                logger.info("Migrating entities table to agents...")
                
                # Create new agents table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agents (
                        id TEXT PRIMARY KEY,
                        case_id TEXT NOT NULL,
                        name TEXT NOT NULL,
                        agent_type TEXT NOT NULL CHECK(agent_type IN ('individual', 'organization', 'system', 'unknown')),
                        verified_attributes TEXT,
                        first_seen TIMESTAMP,
                        last_seen TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (case_id) REFERENCES cases (id) ON DELETE CASCADE
                    )
                """)
                
                # Migrate data if entities table exists
                if 'entities' in tables:
                    cursor.execute("""
                        INSERT INTO agents (id, case_id, name, agent_type, verified_attributes, created_at)
                        SELECT id, case_id, name, 
                               CASE type 
                                   WHEN 'Person' THEN 'individual'
                                   WHEN 'Organization' THEN 'organization'
                                   ELSE 'unknown'
                               END,
                               properties,
                               created_at
                        FROM entities
                    """)
                    
                    # Drop old table
                    cursor.execute("DROP TABLE entities")
                    logger.info("Migrated entities to agents table")
            
            # Add new tables if they don't exist
            new_tables = [
                """CREATE TABLE IF NOT EXISTS event_actors (
                    event_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    role TEXT,
                    PRIMARY KEY (event_id, agent_id),
                    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
                    FOREIGN KEY (agent_id) REFERENCES agents (id) ON DELETE CASCADE
                )""",
                
                """CREATE TABLE IF NOT EXISTS evidence_refs (
                    entity_type TEXT NOT NULL CHECK(entity_type IN ('agent', 'event')),
                    entity_id TEXT NOT NULL,
                    evidence_id TEXT NOT NULL,
                    PRIMARY KEY (entity_type, entity_id, evidence_id),
                    FOREIGN KEY (evidence_id) REFERENCES evidence (id) ON DELETE CASCADE
                )"""
            ]
            
            for create_sql in new_tables:
                cursor.execute(create_sql)
                
            # Add indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_agents_case ON agents(case_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
            
            conn.commit()
            logger.info("Database migration completed")
            
        except Exception as e:
            logger.error(f"Database migration failed: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()
            
    def update_configuration(self):
        """Update configuration files"""
        config_updates = {
            ".env.example": [
                "# Refined configuration",
                "FLASK_ENV=development",
                "DATABASE_PATH=analysis_framework.db",
                "SECRET_KEY=change-this-in-production",
                "LOG_LEVEL=INFO",
                "REQUIRE_AUTH=false"
            ],
            "requirements.txt": [
                "# Core dependencies",
                "flask>=2.3.0",
                "flask-cors>=4.0.0",
                "numpy>=1.24.0",
                "networkx>=3.0.0",
                "python-dateutil>=2.8.0",
                "",
                "# Validation and security",
                "werkzeug>=2.3.0",
                "python-dotenv>=1.0.0",
                "",
                "# Development dependencies", 
                "pytest>=7.0.0",
                "pytest-cov>=4.0.0",
                "black>=23.0.0",
                "flake8>=6.0.0"
            ]
        }
        
        for filename, content in config_updates.items():
            file_path = Path(filename)
            
            if self.dry_run:
                logger.info(f"[DRY RUN] Would create/update: {filename}")
            else:
                file_path.write_text('\n'.join(content) + '\n')
                logger.info(f"Updated: {filename}")
                
    def validate_integration(self):
        """Validate that integration was successful"""
        logger.info("Validating integration...")
        
        checks = []
        
        # Check refined modules exist
        refined_modules = [
            "frameworks/hypergnn_core_refined.py",
            "backend_api_refined.py",
            "config/settings.py",
            "utils/validators.py"
        ]
        
        for module in refined_modules:
            exists = Path(module).exists()
            checks.append((f"Module {module} exists", exists))
            
        # Check database structure
        if not self.dry_run and os.path.exists(self.config.DATABASE_PATH):
            conn = sqlite3.connect(self.config.DATABASE_PATH)
            cursor = conn.cursor()
            
            required_tables = ['cases', 'agents', 'events', 'evidence']
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            for table in required_tables:
                checks.append((f"Table {table} exists", table in existing_tables))
                
            conn.close()
        
        # Report validation results
        all_passed = all(passed for _, passed in checks)
        
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            logger.info(f"{status} {check_name}")
            
        if all_passed:
            logger.info("All validation checks passed!")
        else:
            logger.warning("Some validation checks failed")
            
        return all_passed


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Integrate refined components into codebase"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--env",
        choices=['development', 'testing', 'production'],
        default='development',
        help="Environment to use for configuration"
    )
    
    args = parser.parse_args()
    
    # Get configuration
    config = get_config(args.env)
    
    # Run integration
    integrator = RefinementIntegrator(config, dry_run=args.dry_run)
    
    try:
        integrator.integrate_all()
    except Exception as e:
        logger.error(f"Integration failed: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())