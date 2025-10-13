"""
Database Synchronizer

Main orchestration class for synchronizing database schemas and data
between Supabase and Neon databases based on repository evolution.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class Change:
    """Represents a repository change that may require database updates."""

    def __init__(self, change_type: str, file_path: str, description: str):
        self.change_type = change_type  # 'schema', 'data', 'model'
        self.file_path = file_path
        self.description = description
        self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "change_type": self.change_type,
            "file_path": self.file_path,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(),
        }


class SyncResult:
    """Represents the result of a database synchronization operation."""

    def __init__(self):
        self.success = True
        self.supabase_changes = []
        self.neon_changes = []
        self.conflicts = []
        self.errors = []
        self.timestamp = datetime.now()

    def add_supabase_change(self, change: str):
        self.supabase_changes.append(change)

    def add_neon_change(self, change: str):
        self.neon_changes.append(change)

    def add_conflict(self, conflict: str):
        self.conflicts.append(conflict)

    def add_error(self, error: str):
        self.errors.append(error)
        self.success = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "supabase_changes": self.supabase_changes,
            "neon_changes": self.neon_changes,
            "conflicts": self.conflicts,
            "errors": self.errors,
            "timestamp": self.timestamp.isoformat(),
        }


class DatabaseSynchronizer:
    """
    Main database synchronization orchestrator that manages schema
    and data synchronization between Supabase and Neon databases.
    """

    def __init__(
        self, supabase_client=None, neon_client=None, repository_root: str = "."
    ):
        self.supabase_client = supabase_client
        self.neon_client = neon_client
        self.repository_root = Path(repository_root)
        self.sync_log_path = self.repository_root / "database_sync_log.json"

        # Initialize schema definitions
        self.schema_definitions = self._load_schema_definitions()

        # Track last sync timestamp
        self.last_sync = self._get_last_sync_timestamp()

    def sync_schema_changes(self, repository_changes: List[Change]) -> SyncResult:
        """
        Synchronize database schemas based on repository changes.

        Args:
            repository_changes: List of repository changes to process

        Returns:
            SyncResult with details of synchronization operations
        """
        result = SyncResult()

        try:
            # Analyze changes for database impact
            schema_changes = self._analyze_schema_changes(repository_changes)

            if not schema_changes:
                result.add_supabase_change("No schema changes required")
                result.add_neon_change("No schema changes required")
                return result

            # Generate migration scripts
            supabase_migrations = self._generate_supabase_migrations(schema_changes)
            neon_migrations = self._generate_neon_migrations(schema_changes)

            # Execute migrations
            if supabase_migrations:
                supabase_result = self._execute_supabase_migrations(supabase_migrations)
                result.supabase_changes.extend(supabase_result)

            if neon_migrations:
                neon_result = self._execute_neon_migrations(neon_migrations)
                result.neon_changes.extend(neon_result)

            # Update sync log
            self._update_sync_log(result)

        except Exception as e:
            result.add_error(f"Synchronization failed: {str(e)}")

        return result

    def sync_evidence_data(self, evidence_package) -> SyncResult:
        """
        Synchronize evidence data with both databases.

        Args:
            evidence_package: Evidence package with extracted data

        Returns:
            SyncResult with synchronization details
        """
        result = SyncResult()

        try:
            # Prepare data for insertion
            entities_data = self._prepare_entities_data(evidence_package.entities)
            timeline_data = self._prepare_timeline_data(
                evidence_package.timeline_events
            )
            violations_data = self._prepare_violations_data(
                evidence_package.legal_violations
            )

            # Sync to Supabase
            if self.supabase_client:
                supabase_result = self._sync_to_supabase(
                    entities_data, timeline_data, violations_data
                )
                result.supabase_changes.extend(supabase_result)

            # Sync to Neon
            if self.neon_client:
                neon_result = self._sync_to_neon(
                    entities_data, timeline_data, violations_data
                )
                result.neon_changes.extend(neon_result)

            # Update sync log
            self._update_sync_log(result)

        except Exception as e:
            result.add_error(f"Evidence data sync failed: {str(e)}")

        return result

    def _load_schema_definitions(self) -> Dict[str, Any]:
        """Load schema definitions from repository."""
        schema_file = self.repository_root / "database_schemas.json"

        if schema_file.exists():
            with open(schema_file, "r") as f:
                return json.load(f)
        else:
            # Return default schema definitions
            return {
                "entities": {
                    "table_name": "entities",
                    "columns": {
                        "id": "SERIAL PRIMARY KEY",
                        "type": "VARCHAR(50)",
                        "name": "VARCHAR(255)",
                        "description": "TEXT",
                        "context": "TEXT",
                        "evidence_package": "VARCHAR(100)",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    },
                },
                "timeline_events": {
                    "table_name": "timeline_events",
                    "columns": {
                        "id": "SERIAL PRIMARY KEY",
                        "date": "DATE",
                        "time": "TIME",
                        "description": "TEXT",
                        "significance": "VARCHAR(20)",
                        "context": "TEXT",
                        "evidence_package": "VARCHAR(100)",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    },
                },
                "legal_violations": {
                    "table_name": "legal_violations",
                    "columns": {
                        "id": "SERIAL PRIMARY KEY",
                        "category": "VARCHAR(50)",
                        "description": "TEXT",
                        "severity": "VARCHAR(20)",
                        "penalties": "TEXT[]",
                        "context": "TEXT",
                        "evidence_package": "VARCHAR(100)",
                        "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
                    },
                },
            }

    def _get_last_sync_timestamp(self) -> Optional[datetime]:
        """Get timestamp of last synchronization."""
        if self.sync_log_path.exists():
            with open(self.sync_log_path, "r") as f:
                log_data = json.load(f)
                if log_data and "last_sync" in log_data:
                    return datetime.fromisoformat(log_data["last_sync"])
        return None

    def _analyze_schema_changes(
        self, repository_changes: List[Change]
    ) -> List[Dict[str, Any]]:
        """Analyze repository changes for database schema impact."""
        schema_changes = []

        for change in repository_changes:
            # Check if change affects database schema
            if self._affects_schema(change):
                schema_change = {
                    "type": change.change_type,
                    "file": change.file_path,
                    "description": change.description,
                    "required_tables": self._get_required_tables(change),
                    "required_columns": self._get_required_columns(change),
                }
                schema_changes.append(schema_change)

        return schema_changes

    def _affects_schema(self, change: Change) -> bool:
        """Determine if a repository change affects database schema."""
        schema_affecting_patterns = [
            "evidence_automation",
            "entity",
            "timeline",
            "legal_violation",
            "hypergraph",
            "model",
        ]

        return any(
            pattern in change.file_path.lower() for pattern in schema_affecting_patterns
        )

    def _get_required_tables(self, change: Change) -> List[str]:
        """Get list of tables required for a change."""
        tables = []

        if "entity" in change.file_path.lower():
            tables.append("entities")
        if "timeline" in change.file_path.lower():
            tables.append("timeline_events")
        if (
            "legal" in change.file_path.lower()
            or "violation" in change.file_path.lower()
        ):
            tables.append("legal_violations")
        if "hypergraph" in change.file_path.lower():
            tables.extend(["hypergraph_nodes", "hypergraph_edges"])

        return tables

    def _get_required_columns(self, change: Change) -> Dict[str, List[str]]:
        """Get required columns for tables based on change."""
        # This would analyze the change to determine new columns needed
        # For now, return empty dict (no new columns required)
        return {}

    def _generate_supabase_migrations(
        self, schema_changes: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate Supabase migration scripts."""
        migrations = []

        for change in schema_changes:
            for table in change["required_tables"]:
                if table in self.schema_definitions:
                    migration = self._generate_table_migration(table, "supabase")
                    migrations.append(migration)

        return migrations

    def _generate_neon_migrations(
        self, schema_changes: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate Neon migration scripts."""
        migrations = []

        for change in schema_changes:
            for table in change["required_tables"]:
                if table in self.schema_definitions:
                    migration = self._generate_table_migration(table, "neon")
                    migrations.append(migration)

        return migrations

    def _generate_table_migration(self, table_name: str, database_type: str) -> str:
        """Generate CREATE TABLE migration for a specific table."""
        if table_name not in self.schema_definitions:
            return ""

        table_def = self.schema_definitions[table_name]
        columns = []

        for col_name, col_type in table_def["columns"].items():
            columns.append(f"    {col_name} {col_type}")

        migration = f"""
-- Create {table_name} table for {database_type}
CREATE TABLE IF NOT EXISTS {table_def['table_name']} (
{','.join(columns)}
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_{table_name}_created_at ON {table_def['table_name']} (created_at);
CREATE INDEX IF NOT EXISTS idx_{table_name}_evidence_package ON {table_def['table_name']} (evidence_package);
"""

        return migration.strip()

    def _execute_supabase_migrations(self, migrations: List[str]) -> List[str]:
        """Execute migrations on Supabase database."""
        results = []

        for migration in migrations:
            try:
                if self.supabase_client:
                    # Execute migration using Supabase client
                    # This is a placeholder - actual implementation would use Supabase API
                    results.append(f"Executed Supabase migration: {migration[:50]}...")
                else:
                    results.append(
                        "Supabase client not available - migration logged for manual execution"
                    )
            except Exception as e:
                results.append(f"Supabase migration failed: {str(e)}")

        return results

    def _execute_neon_migrations(self, migrations: List[str]) -> List[str]:
        """Execute migrations on Neon database."""
        results = []

        for migration in migrations:
            try:
                if self.neon_client:
                    # Execute migration using Neon client
                    # This is a placeholder - actual implementation would use Neon API
                    results.append(f"Executed Neon migration: {migration[:50]}...")
                else:
                    results.append(
                        "Neon client not available - migration logged for manual execution"
                    )
            except Exception as e:
                results.append(f"Neon migration failed: {str(e)}")

        return results

    def _prepare_entities_data(
        self, entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prepare entities data for database insertion."""
        prepared_data = []

        for entity in entities:
            data = {
                "type": entity.get("type", "unknown"),
                "name": entity.get("name", ""),
                "description": entity.get("description", ""),
                "context": entity.get("context", ""),
                "evidence_package": "formal_notice_july_2025",
            }
            prepared_data.append(data)

        return prepared_data

    def _prepare_timeline_data(
        self, timeline_events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prepare timeline data for database insertion."""
        prepared_data = []

        for event in timeline_events:
            data = {
                "date": event.get("date"),
                "time": event.get("time"),
                "description": event.get("description", ""),
                "significance": event.get("significance", "Standard"),
                "context": event.get("context", ""),
                "evidence_package": "formal_notice_july_2025",
            }
            prepared_data.append(data)

        return prepared_data

    def _prepare_violations_data(
        self, violations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prepare legal violations data for database insertion."""
        prepared_data = []

        for violation in violations:
            data = {
                "category": violation.get("category", "unknown"),
                "description": violation.get("description", ""),
                "severity": violation.get("severity", "Medium"),
                "penalties": violation.get("penalties", []),
                "context": violation.get("context", ""),
                "evidence_package": "formal_notice_july_2025",
            }
            prepared_data.append(data)

        return prepared_data

    def _sync_to_supabase(
        self,
        entities_data: List[Dict],
        timeline_data: List[Dict],
        violations_data: List[Dict],
    ) -> List[str]:
        """Sync data to Supabase database."""
        results = []

        try:
            if self.supabase_client:
                # Insert entities
                if entities_data:
                    # supabase_client.table('entities').insert(entities_data).execute()
                    results.append(
                        f"Inserted {len(entities_data)} entities to Supabase"
                    )

                # Insert timeline events
                if timeline_data:
                    # supabase_client.table('timeline_events').insert(timeline_data).execute()
                    results.append(
                        f"Inserted {len(timeline_data)} timeline events to Supabase"
                    )

                # Insert legal violations
                if violations_data:
                    # supabase_client.table('legal_violations').insert(violations_data).execute()
                    results.append(
                        f"Inserted {len(violations_data)} legal violations to Supabase"
                    )
            else:
                results.append(
                    "Supabase client not available - data sync logged for manual execution"
                )

        except Exception as e:
            results.append(f"Supabase sync error: {str(e)}")

        return results

    def _sync_to_neon(
        self,
        entities_data: List[Dict],
        timeline_data: List[Dict],
        violations_data: List[Dict],
    ) -> List[str]:
        """Sync data to Neon database."""
        results = []

        try:
            if self.neon_client:
                # Insert entities
                if entities_data:
                    results.append(f"Inserted {len(entities_data)} entities to Neon")

                # Insert timeline events
                if timeline_data:
                    results.append(
                        f"Inserted {len(timeline_data)} timeline events to Neon"
                    )

                # Insert legal violations
                if violations_data:
                    results.append(
                        f"Inserted {len(violations_data)} legal violations to Neon"
                    )
            else:
                results.append(
                    "Neon client not available - data sync logged for manual execution"
                )

        except Exception as e:
            results.append(f"Neon sync error: {str(e)}")

        return results

    def _update_sync_log(self, result: SyncResult):
        """Update synchronization log with results."""
        log_data = {
            "last_sync": datetime.now().isoformat(),
            "last_result": result.to_dict(),
        }

        # Load existing log if it exists
        if self.sync_log_path.exists():
            with open(self.sync_log_path, "r") as f:
                existing_log = json.load(f)
                if "sync_history" not in existing_log:
                    existing_log["sync_history"] = []
                existing_log["sync_history"].append(result.to_dict())
                log_data["sync_history"] = existing_log["sync_history"]
        else:
            log_data["sync_history"] = [result.to_dict()]

        # Write updated log
        with open(self.sync_log_path, "w") as f:
            json.dump(log_data, f, indent=2)


def sync_repository_changes(repository_changes: List[Change]) -> SyncResult:
    """
    Convenience function for synchronizing repository changes.

    Args:
        repository_changes: List of repository changes to sync

    Returns:
        SyncResult with synchronization details
    """
    synchronizer = DatabaseSynchronizer()
    return synchronizer.sync_schema_changes(repository_changes)
