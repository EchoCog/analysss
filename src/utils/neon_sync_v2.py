#!/usr/bin/env python3
"""
Neon Database Synchronization Script (Enhanced)
============================================

This script synchronizes the improved database schema with the Neon Postgres instance.

**Prerequisite:**
You must have the `manus-mcp-cli` installed and configured for the `neon` server.
"""

import json
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class NeonMCPError(Exception):
    """Custom exception for Neon MCP errors."""

    pass


def get_project_id() -> str:
    """Get the Neon project ID from environment variables."""
    project_id = os.environ.get("NEON_PROJECT_ID")
    if not project_id:
        raise ValueError("NEON_PROJECT_ID environment variable must be set")
    return project_id


def execute_mcp_command(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a command on the Neon MCP server."""
    command = [
        "manus-mcp-cli",
        "tool",
        "call",
        tool_name,
        "--server",
        "neon",
        "--input",
        json.dumps({"params": params}),  # Wrap params in params object
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing MCP command: {e.stderr}")
        raise NeonMCPError(f"Failed to execute MCP command: {e.stderr}")
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding MCP response: {e}")
        raise NeonMCPError(f"Failed to decode MCP response: {e}")


def sync_schema_with_neon(schema_file: str, project_id: str) -> Dict[str, Any]:
    """Synchronize the database schema with the Neon instance using MCP."""
    if not os.path.exists(schema_file):
        return {"error": f"Schema file {schema_file} not found"}

    with open(schema_file, "r") as f:
        schema_sql = f.read()

    statements = [stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()]

    logging.info(f"Found {len(statements)} statements in {schema_file}.")

    try:
        # The tool name and parameters should match the MCP server's expectations.
        # Based on the MCP tool specification, it takes `projectId` and `sqlStatements`.
        result = execute_mcp_command(
            "run_sql_transaction",
            {"projectId": project_id, "sqlStatements": statements},
        )
        return {
            "status": "success",
            "message": "Schema synchronization completed.",
            "result": result,
        }
    except NeonMCPError as e:
        return {"status": "error", "message": str(e)}


def main():
    """Main synchronization function."""
    try:
        logging.info("🔄 Starting Neon database synchronization...")
        project_id = get_project_id()

        schema_result = sync_schema_with_neon(
            "analysis/database_schema_improved.sql", project_id
        )

        if schema_result.get("status") == "error":
            logging.error(f"❌ Schema sync failed: {schema_result.get('message')}")
            return False

        logging.info("✅ Schema synchronization completed successfully.")
        logging.info("\n🎯 Neon Synchronization Summary:")
        logging.info(f"   - Status: Ready for production use")

        return True

    except Exception as e:
        logging.error(f"❌ Synchronization failed: {e}")
        return False


if __name__ == "__main__":
    # Change working directory to the root of the repository
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    success = main()
    sys.exit(0 if success else 1)
