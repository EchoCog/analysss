"""
Real-time Database Synchronization

Enhanced synchronization module with actual database operations
for Supabase and Neon databases.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    NEON_AVAILABLE = True
except ImportError:
    NEON_AVAILABLE = False


class RealTimeDatabaseSync:
    """
    Real-time database synchronization with actual implementations
    for Supabase and Neon PostgreSQL databases.
    """

    def __init__(self, config: Optional[Dict[str, str]] = None):
        """
        Initialize database connections.

        Args:
            config: Configuration dictionary with database credentials
        """
        self.config = config or self._load_config()
        self.supabase_client = None
        self.neon_connection = None
        self.sync_log_path = Path("database_sync_log.json")

        # Initialize connections
        self._init_supabase()
        self._init_neon()

    def _load_config(self) -> Dict[str, str]:
        """Load configuration from environment variables."""
        return {
            "supabase_url": os.getenv("SUPABASE_URL", ""),
            "supabase_key": os.getenv("SUPABASE_KEY", ""),
            "neon_connection_string": os.getenv("NEON_CONNECTION_STRING", ""),
            "neon_host": os.getenv("NEON_HOST", ""),
            "neon_database": os.getenv("NEON_DATABASE", ""),
            "neon_user": os.getenv("NEON_USER", ""),
            "neon_password": os.getenv("NEON_PASSWORD", ""),
        }

    def _init_supabase(self):
        """Initialize Supabase client."""
        if not SUPABASE_AVAILABLE:
            print("Warning: Supabase library not installed. Install with: pip install supabase")
            return

        url = self.config.get("supabase_url")
        key = self.config.get("supabase_key")

        if url and key:
            try:
                self.supabase_client = create_client(url, key)
                print("✓ Supabase client initialized successfully")
            except Exception as e:
                print(f"✗ Failed to initialize Supabase client: {e}")
        else:
            print("⚠ Supabase credentials not configured")

    def _init_neon(self):
        """Initialize Neon PostgreSQL connection."""
        if not NEON_AVAILABLE:
            print("Warning: psycopg2 library not installed. Install with: pip install psycopg2-binary")
            return

        conn_string = self.config.get("neon_connection_string")

        if not conn_string:
            # Build connection string from components
            host = self.config.get("neon_host")
            database = self.config.get("neon_database")
            user = self.config.get("neon_user")
            password = self.config.get("neon_password")

            if all([host, database, user, password]):
                conn_string = f"postgresql://{user}:{password}@{host}/{database}?sslmode=require"

        if conn_string:
            try:
                self.neon_connection = psycopg2.connect(conn_string)
                print("✓ Neon PostgreSQL connection established")
            except Exception as e:
                print(f"✗ Failed to connect to Neon: {e}")
        else:
            print("⚠ Neon credentials not configured")

    def sync_schema(self, schema_sql: str) -> Dict[str, Any]:
        """
        Synchronize database schema to both Supabase and Neon.

        Args:
            schema_sql: SQL schema definition

        Returns:
            Dictionary with sync results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "supabase": {"success": False, "message": ""},
            "neon": {"success": False, "message": ""},
        }

        # Sync to Supabase
        if self.supabase_client:
            try:
                # Execute schema via Supabase RPC or direct SQL
                self.supabase_client.postgrest.rpc("exec_sql", {"sql": schema_sql}).execute()
                results["supabase"]["success"] = True
                results["supabase"]["message"] = "Schema synchronized successfully"
            except Exception as e:
                results["supabase"]["message"] = f"Schema sync failed: {str(e)}"

        # Sync to Neon
        if self.neon_connection:
            try:
                cursor = self.neon_connection.cursor()
                cursor.execute(schema_sql)
                self.neon_connection.commit()
                cursor.close()
                results["neon"]["success"] = True
                results["neon"]["message"] = "Schema synchronized successfully"
            except Exception as e:
                results["neon"]["message"] = f"Schema sync failed: {str(e)}"
                self.neon_connection.rollback()

        self._log_sync(results)
        return results

    def sync_data(self, table_name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronize data to both databases.

        Args:
            table_name: Name of the table to sync
            data: List of data records to insert/update

        Returns:
            Dictionary with sync results
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "table": table_name,
            "records": len(data),
            "supabase": {"success": False, "message": "", "inserted": 0},
            "neon": {"success": False, "message": "", "inserted": 0},
        }

        # Sync to Supabase
        if self.supabase_client and data:
            try:
                response = self.supabase_client.table(table_name).upsert(data).execute()
                results["supabase"]["success"] = True
                results["supabase"]["inserted"] = len(data)
                results["supabase"]["message"] = f"Inserted {len(data)} records"
            except Exception as e:
                results["supabase"]["message"] = f"Data sync failed: {str(e)}"

        # Sync to Neon
        if self.neon_connection and data:
            try:
                cursor = self.neon_connection.cursor()

                # Build upsert query
                if data:
                    columns = list(data[0].keys())
                    placeholders = ", ".join(["%s"] * len(columns))
                    columns_str = ", ".join(columns)

                    # Assuming first column is primary key for conflict resolution
                    pk_column = columns[0]
                    update_cols = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns[1:]])

                    query = f"""
                        INSERT INTO {table_name} ({columns_str})
                        VALUES ({placeholders})
                        ON CONFLICT ({pk_column}) DO UPDATE SET {update_cols}
                    """

                    for record in data:
                        values = tuple(record[col] for col in columns)
                        cursor.execute(query, values)

                    self.neon_connection.commit()
                    cursor.close()
                    results["neon"]["success"] = True
                    results["neon"]["inserted"] = len(data)
                    results["neon"]["message"] = f"Inserted {len(data)} records"
            except Exception as e:
                results["neon"]["message"] = f"Data sync failed: {str(e)}"
                self.neon_connection.rollback()

        self._log_sync(results)
        return results

    def sync_repository_changes(self, repository_path: str = ".") -> Dict[str, Any]:
        """
        Scan repository for changes and sync relevant data.

        Args:
            repository_path: Path to the repository root

        Returns:
            Dictionary with sync results
        """
        repo_path = Path(repository_path)
        results = {
            "timestamp": datetime.now().isoformat(),
            "changes_detected": [],
            "syncs_performed": [],
        }

        # Check for new evidence files
        evidence_path = repo_path / "evidence"
        if evidence_path.exists():
            for evidence_file in evidence_path.rglob("*.json"):
                try:
                    with open(evidence_file, "r") as f:
                        evidence_data = json.load(f)

                    # Sync evidence data
                    if isinstance(evidence_data, list):
                        sync_result = self.sync_data("evidence", evidence_data)
                        results["syncs_performed"].append(sync_result)
                        results["changes_detected"].append(str(evidence_file))
                except Exception as e:
                    print(f"Error processing {evidence_file}: {e}")

        # Check for entity files
        entities_path = repo_path / "entities"
        if entities_path.exists():
            for entity_file in entities_path.rglob("*.json"):
                try:
                    with open(entity_file, "r") as f:
                        entity_data = json.load(f)

                    if isinstance(entity_data, list):
                        sync_result = self.sync_data("entities", entity_data)
                        results["syncs_performed"].append(sync_result)
                        results["changes_detected"].append(str(entity_file))
                except Exception as e:
                    print(f"Error processing {entity_file}: {e}")

        return results

    def _log_sync(self, sync_result: Dict[str, Any]):
        """Log synchronization results."""
        log_data = []

        if self.sync_log_path.exists():
            with open(self.sync_log_path, "r") as f:
                log_data = json.load(f)

        log_data.append(sync_result)

        # Keep only last 100 entries
        log_data = log_data[-100:]

        with open(self.sync_log_path, "w") as f:
            json.dump(log_data, f, indent=2)

    def close(self):
        """Close database connections."""
        if self.neon_connection:
            self.neon_connection.close()
            print("✓ Neon connection closed")


def main():
    """Main function for testing sync functionality."""
    sync = RealTimeDatabaseSync()

    # Test schema sync
    test_schema = """
    CREATE TABLE IF NOT EXISTS test_sync (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    print("\n=== Testing Schema Sync ===")
    schema_result = sync.sync_schema(test_schema)
    print(json.dumps(schema_result, indent=2))

    # Test data sync
    test_data = [
        {"id": 1, "name": "Test Record 1"},
        {"id": 2, "name": "Test Record 2"},
    ]

    print("\n=== Testing Data Sync ===")
    data_result = sync.sync_data("test_sync", test_data)
    print(json.dumps(data_result, indent=2))

    sync.close()


if __name__ == "__main__":
    main()

