#!/usr/bin/env python3
"""
Supabase Database Synchronization Script (Enhanced)
===================================================

This script synchronizes the improved database schema with the Supabase instance.

**Prerequisite:**
You must first create the `execute_sql` RPC function in your Supabase SQL editor.
This function is necessary for the script to execute raw SQL statements.

SQL to create the function:
CREATE OR REPLACE FUNCTION execute_sql(sql_statement TEXT)
RETURNS VOID AS $$
BEGIN
    EXECUTE sql_statement;
END;
$$ LANGUAGE plpgsql;
"""

import logging
import os
import sys
from typing import Any, Dict

from supabase import Client, create_client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_supabase_client() -> Client:
    """Initialize and return a Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
        )

    return create_client(url, key)


def verify_rpc_function(supabase: Client):
    """Verify that the RPC function 'execute_sql' exists."""
    logging.info("Verifying the existence of RPC function 'execute_sql'...")
    try:
        # A simple select to check if the function exists and is callable
        supabase.rpc("execute_sql", {"sql_statement": "SELECT 1"}).execute()
        logging.info("RPC function 'execute_sql' is available.")
        return True
    except Exception as e:
        logging.error("RPC function 'execute_sql' not found or not callable.")
        logging.error(
            "Please create it using the SQL provided in the script's docstring."
        )
        logging.error(f"Error details: {e}")
        return False


def execute_schema_from_file(supabase: Client, schema_file: str) -> Dict[str, Any]:
    """Execute the database schema from a file against Supabase."""
    if not os.path.exists(schema_file):
        return {"error": f"Schema file {schema_file} not found"}

    with open(schema_file, "r") as f:
        schema_sql = f.read()

    statements = [stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()]
    executed_statements = []
    errors = []

    logging.info(f"Found {len(statements)} statements in {schema_file}.")

    for statement in statements:
        if statement and not statement.startswith("--"):
            try:
                logging.info(f"Executing: {statement[:80]}...")
                supabase.rpc("execute_sql", {"sql_statement": statement}).execute()
                executed_statements.append(statement)
            except Exception as e:
                error_message = str(e)
                logging.error(
                    f"Error executing statement: {statement[:80]}... - {error_message}"
                )
                errors.append({"statement": statement, "error": error_message})

    if errors:
        return {
            "status": "error",
            "message": "Schema synchronization failed with errors.",
            "errors": errors,
        }

    return {
        "status": "success",
        "message": f"Schema synchronization completed. Executed {len(executed_statements)} statements.",
        "executed_statements": executed_statements,
    }


def main():
    """Main synchronization function."""
    try:
        logging.info("🔄 Starting Supabase synchronization...")
        supabase = get_supabase_client()
        logging.info("✅ Supabase client initialized successfully")

        if not verify_rpc_function(supabase):
            return False

        schema_result = execute_schema_from_file(
            supabase, "analysis/database_schema_improved.sql"
        )

        if schema_result.get("status") == "error":
            logging.error(f"❌ Schema sync failed: {schema_result.get('message')}")
            for error in schema_result.get("errors", []):
                logging.error(f"  - Statement: {error['statement']}")
                logging.error(f"    Error: {error['error']}")
            return False

        logging.info("✅ Schema synchronization completed successfully.")
        logging.info("\n🎯 Synchronization Summary:")
        logging.info(
            f"   - Statements executed: {len(schema_result.get('executed_statements', []))}"
        )
        logging.info("   - Status: Ready for production use")

        return True

    except Exception as e:
        logging.error(f"❌ Synchronization failed: {e}")
        return False


if __name__ == "__main__":
    # Change working directory to the root of the repository
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    success = main()
    sys.exit(0 if success else 1)
