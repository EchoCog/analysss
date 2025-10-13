#!/usr/bin/env python3
"""
Enhanced Neon Database Synchronization Script
=============================================

This enhanced script provides robust database synchronization with Neon serverless Postgres,
featuring:
- MCP integration for Neon operations
- Comprehensive error handling and logging
- Schema validation and migration support
- Type hints and documentation for maintainability
- Connection pooling and retry mechanisms
"""

import json
import logging
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("neon_sync.log")],
)
logger = logging.getLogger(__name__)


@dataclass
class NeonSyncResult:
    """
    Result of a Neon synchronization operation

    Attributes:
        success: Whether the operation was successful
        message: Human-readable message about the operation
        details: Additional details about the operation
        errors: List of errors encountered
        execution_time: Time taken for the operation in seconds
        neon_response: Raw response from Neon MCP server
    """

    success: bool
    message: str
    details: Dict[str, Any]
    errors: List[str]
    execution_time: float
    neon_response: Optional[Dict[str, Any]] = None


class EnhancedNeonSync:
    """
    Enhanced Neon synchronization manager with MCP integration

    Provides robust database synchronization capabilities including:
    - MCP server integration for Neon operations
    - Project and branch management
    - SQL query execution with error handling
    - Schema validation and migration support
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0) -> None:
        """
        Initialize the enhanced Neon sync manager

        Args:
            max_retries: Maximum number of retry attempts for failed operations
            retry_delay: Delay between retry attempts in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.server_name = "neon"

        logger.info("Enhanced Neon sync manager initialized")

    def execute_mcp_command(
        self, command: str, input_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a command using the Neon MCP server

        Args:
            command: MCP command to execute
            input_data: Optional input data for the command

        Returns:
            Dictionary containing the command result

        Raises:
            subprocess.CalledProcessError: If MCP command fails
            json.JSONDecodeError: If response is not valid JSON
        """
        try:
            cmd_args = [
                "manus-mcp-cli",
                "tool",
                "call",
                command,
                "--server",
                self.server_name,
            ]

            if input_data:
                cmd_args.extend(["--input", json.dumps(input_data)])

            logger.debug(f"Executing MCP command: {' '.join(cmd_args)}")

            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,  # 60 second timeout
            )

            if result.stdout:
                response = json.loads(result.stdout)
                logger.debug(f"MCP command successful: {command}")
                return response
            else:
                logger.warning(f"MCP command returned empty response: {command}")
                return {"status": "empty_response"}

        except subprocess.CalledProcessError as e:
            error_msg = f"MCP command failed: {command} - {e.stderr}"
            logger.error(error_msg)
            raise
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON response from MCP command: {command} - {e}"
            logger.error(error_msg)
            raise
        except subprocess.TimeoutExpired:
            error_msg = f"MCP command timed out: {command}"
            logger.error(error_msg)
            raise

    def retry_operation(self, operation_func, *args, **kwargs) -> Any:
        """
        Retry an operation with exponential backoff

        Args:
            operation_func: Function to retry
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the operation function

        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                return operation_func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2**attempt)  # Exponential backoff
                    logger.warning(
                        f"Operation failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}"
                    )
                    logger.info(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(
                        f"Operation failed after {self.max_retries + 1} attempts"
                    )

        raise last_exception

    def list_projects(self) -> NeonSyncResult:
        """
        List all Neon projects

        Returns:
            NeonSyncResult containing project list or error information
        """
        start_time = time.time()

        try:
            response = self.retry_operation(self.execute_mcp_command, "list_projects")
            execution_time = time.time() - start_time

            return NeonSyncResult(
                success=True,
                message="Successfully retrieved project list",
                details={"project_count": len(response.get("projects", []))},
                errors=[],
                execution_time=execution_time,
                neon_response=response,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Failed to list projects: {e}"
            logger.error(error_msg)

            return NeonSyncResult(
                success=False,
                message="Failed to retrieve project list",
                details={"error": str(e)},
                errors=[error_msg],
                execution_time=execution_time,
            )

    def create_project(
        self, project_name: str, region: str = "us-east-1"
    ) -> NeonSyncResult:
        """
        Create a new Neon project

        Args:
            project_name: Name for the new project
            region: AWS region for the project

        Returns:
            NeonSyncResult containing creation result
        """
        start_time = time.time()

        try:
            input_data = {"name": project_name, "region": region}

            response = self.retry_operation(
                self.execute_mcp_command, "create_project", input_data
            )

            execution_time = time.time() - start_time

            return NeonSyncResult(
                success=True,
                message=f"Successfully created project: {project_name}",
                details={
                    "project_name": project_name,
                    "region": region,
                    "project_id": response.get("project", {}).get("id"),
                },
                errors=[],
                execution_time=execution_time,
                neon_response=response,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Failed to create project {project_name}: {e}"
            logger.error(error_msg)

            return NeonSyncResult(
                success=False,
                message=f"Failed to create project: {project_name}",
                details={"error": str(e)},
                errors=[error_msg],
                execution_time=execution_time,
            )

    def execute_sql_query(
        self, project_id: str, database_name: str, query: str
    ) -> NeonSyncResult:
        """
        Execute SQL query on a Neon database

        Args:
            project_id: Neon project ID
            database_name: Name of the database
            query: SQL query to execute

        Returns:
            NeonSyncResult containing query result
        """
        start_time = time.time()

        try:
            input_data = {
                "project_id": project_id,
                "database": database_name,
                "query": query,
            }

            response = self.retry_operation(
                self.execute_mcp_command, "execute_query", input_data
            )

            execution_time = time.time() - start_time

            return NeonSyncResult(
                success=True,
                message="SQL query executed successfully",
                details={
                    "project_id": project_id,
                    "database": database_name,
                    "query_length": len(query),
                    "rows_affected": response.get("rows_affected", 0),
                },
                errors=[],
                execution_time=execution_time,
                neon_response=response,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Failed to execute SQL query: {e}"
            logger.error(error_msg)

            return NeonSyncResult(
                success=False,
                message="SQL query execution failed",
                details={
                    "error": str(e),
                    "query": query[:100] + "..." if len(query) > 100 else query,
                },
                errors=[error_msg],
                execution_time=execution_time,
            )

    def create_database_schema(
        self, project_id: str, database_name: str
    ) -> NeonSyncResult:
        """
        Create the HyperGNN database schema in Neon

        Args:
            project_id: Neon project ID
            database_name: Name of the database

        Returns:
            NeonSyncResult containing schema creation result
        """
        start_time = time.time()
        all_errors = []

        # Define schema creation queries
        schema_queries = [
            """
            CREATE TABLE IF NOT EXISTS agents (
                agent_id VARCHAR(255) PRIMARY KEY,
                agent_type VARCHAR(50) NOT NULL,
                name VARCHAR(255) NOT NULL,
                professional_links TEXT[],
                social_links TEXT[],
                attributes JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS events (
                event_id VARCHAR(255) PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                event_type VARCHAR(50) NOT NULL,
                actors TEXT[] NOT NULL,
                description TEXT NOT NULL,
                implications TEXT[],
                evidence_refs TEXT[],
                motive_analysis TEXT,
                means_analysis TEXT,
                opportunity_analysis TEXT,
                hostility_assessment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS flows (
                flow_id VARCHAR(255) PRIMARY KEY,
                flow_type VARCHAR(50) NOT NULL,
                source VARCHAR(255) NOT NULL,
                target VARCHAR(255) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                magnitude FLOAT NOT NULL,
                description TEXT NOT NULL,
                evidence TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS timeline_tensors (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                tensor_type VARCHAR(50) NOT NULL,
                dimensions INTEGER[] NOT NULL,
                data BYTEA NOT NULL,
                metadata JSONB,
                confidence_score FLOAT DEFAULT 1.0,
                source_evidence TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(agent_type);
            CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
            CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type);
            CREATE INDEX IF NOT EXISTS idx_flows_timestamp ON flows(timestamp);
            CREATE INDEX IF NOT EXISTS idx_flows_type ON flows(flow_type);
            CREATE INDEX IF NOT EXISTS idx_timeline_tensors_timestamp ON timeline_tensors(timestamp);
            CREATE INDEX IF NOT EXISTS idx_timeline_tensors_type ON timeline_tensors(tensor_type);
            """,
        ]

        try:
            for i, query in enumerate(schema_queries):
                logger.info(f"Executing schema query {i + 1}/{len(schema_queries)}")
                result = self.execute_sql_query(project_id, database_name, query)

                if not result.success:
                    all_errors.extend(result.errors)
                    logger.error(f"Schema query {i + 1} failed: {result.message}")

            execution_time = time.time() - start_time

            if all_errors:
                return NeonSyncResult(
                    success=False,
                    message="Schema creation completed with errors",
                    details={
                        "queries_executed": len(schema_queries),
                        "errors_count": len(all_errors),
                    },
                    errors=all_errors,
                    execution_time=execution_time,
                )
            else:
                return NeonSyncResult(
                    success=True,
                    message="Database schema created successfully",
                    details={
                        "queries_executed": len(schema_queries),
                        "tables_created": [
                            "agents",
                            "events",
                            "flows",
                            "timeline_tensors",
                        ],
                    },
                    errors=[],
                    execution_time=execution_time,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Unexpected error during schema creation: {e}"
            logger.error(error_msg)
            all_errors.append(error_msg)

            return NeonSyncResult(
                success=False,
                message="Schema creation failed",
                details={"error": str(e)},
                errors=all_errors,
                execution_time=execution_time,
            )

    def sync_with_repository(
        self, project_id: str, database_name: str
    ) -> NeonSyncResult:
        """
        Synchronize Neon database with the repository structure

        Args:
            project_id: Neon project ID
            database_name: Name of the database

        Returns:
            NeonSyncResult containing synchronization result
        """
        start_time = time.time()
        all_errors = []

        logger.info("🔄 Starting Neon database synchronization with repository...")

        try:
            # Create schema
            schema_result = self.create_database_schema(project_id, database_name)
            if not schema_result.success:
                all_errors.extend(schema_result.errors)
                logger.error("Schema creation failed during synchronization")

            # Validate schema
            validation_result = self.validate_schema(project_id, database_name)
            if not validation_result.success:
                all_errors.extend(validation_result.errors)
                logger.warning("Schema validation failed")

            execution_time = time.time() - start_time

            success = len(all_errors) == 0
            message = (
                "Neon synchronization completed successfully"
                if success
                else "Neon synchronization completed with warnings"
            )

            return NeonSyncResult(
                success=success,
                message=message,
                details={
                    "schema_created": schema_result.success,
                    "schema_validated": validation_result.success,
                    "total_execution_time": execution_time,
                },
                errors=all_errors,
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Unexpected error during synchronization: {e}"
            logger.error(error_msg)
            all_errors.append(error_msg)

            return NeonSyncResult(
                success=False,
                message="Neon synchronization failed",
                details={"error": str(e)},
                errors=all_errors,
                execution_time=execution_time,
            )

    def validate_schema(self, project_id: str, database_name: str) -> NeonSyncResult:
        """
        Validate the database schema

        Args:
            project_id: Neon project ID
            database_name: Name of the database

        Returns:
            NeonSyncResult containing validation result
        """
        start_time = time.time()
        errors = []

        try:
            # Check for required tables
            validation_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('agents', 'events', 'flows', 'timeline_tensors');
            """

            result = self.execute_sql_query(project_id, database_name, validation_query)

            if result.success:
                tables = result.neon_response.get("rows", [])
                table_names = [row[0] for row in tables] if tables else []

                required_tables = ["agents", "events", "flows", "timeline_tensors"]
                missing_tables = [
                    table for table in required_tables if table not in table_names
                ]

                if missing_tables:
                    errors.extend(
                        [f"Missing table: {table}" for table in missing_tables]
                    )

                execution_time = time.time() - start_time

                if errors:
                    return NeonSyncResult(
                        success=False,
                        message="Schema validation failed",
                        details={"missing_tables": missing_tables},
                        errors=errors,
                        execution_time=execution_time,
                    )
                else:
                    return NeonSyncResult(
                        success=True,
                        message="Schema validation passed",
                        details={"validated_tables": table_names},
                        errors=[],
                        execution_time=execution_time,
                    )
            else:
                errors.extend(result.errors)
                execution_time = time.time() - start_time

                return NeonSyncResult(
                    success=False,
                    message="Schema validation query failed",
                    details={"query_error": result.message},
                    errors=errors,
                    execution_time=execution_time,
                )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Schema validation error: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

            return NeonSyncResult(
                success=False,
                message="Schema validation failed",
                details={"error": str(e)},
                errors=errors,
                execution_time=execution_time,
            )


def main() -> bool:
    """
    Main Neon synchronization function

    Returns:
        True if synchronization was successful, False otherwise
    """
    try:
        sync_manager = EnhancedNeonSync()

        # List projects to verify connection
        projects_result = sync_manager.list_projects()
        if not projects_result.success:
            logger.error("Failed to connect to Neon - cannot list projects")
            return False

        logger.info(
            f"Connected to Neon - found {projects_result.details.get('project_count', 0)} projects"
        )

        # For demonstration, we'll use the first available project
        # In a real scenario, you would specify the project ID
        projects = projects_result.neon_response.get("projects", [])
        if not projects:
            logger.error("No Neon projects found - please create a project first")
            return False

        project_id = projects[0].get("id")
        database_name = "postgres"  # Default database name

        logger.info(f"Using project: {project_id}")

        # Perform synchronization
        result = sync_manager.sync_with_repository(project_id, database_name)

        # Log results
        if result.success:
            logger.info("✅ Enhanced Neon synchronization completed successfully")
            logger.info(f"   - Execution time: {result.execution_time:.2f} seconds")
            logger.info(f"   - Details: {result.details}")
        else:
            logger.error("❌ Enhanced Neon synchronization failed")
            logger.error(f"   - Message: {result.message}")
            logger.error(f"   - Errors: {result.errors}")

        return result.success

    except Exception as e:
        logger.error(f"❌ Critical error in main Neon synchronization: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
