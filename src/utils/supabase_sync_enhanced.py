#!/usr/bin/env python3
"""
Enhanced Supabase Database Synchronization Script
=================================================

This enhanced script provides robust database synchronization with the Supabase instance,
featuring:
- Alembic integration for proper migration management
- Comprehensive error handling and logging
- Connection pooling and retry mechanisms
- Schema validation and rollback capabilities
- Type hints and documentation for maintainability
"""

import logging
import os
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from supabase import Client, create_client

from alembic import command
from alembic.config import Config
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("supabase_sync.log")],
)
logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """
    Result of a synchronization operation

    Attributes:
        success: Whether the operation was successful
        message: Human-readable message about the operation
        details: Additional details about the operation
        errors: List of errors encountered
        execution_time: Time taken for the operation in seconds
    """

    success: bool
    message: str
    details: Dict[str, Any]
    errors: List[str]
    execution_time: float


class EnhancedSupabaseSync:
    """
    Enhanced Supabase synchronization manager with Alembic integration

    Provides robust database synchronization capabilities including:
    - Migration management with Alembic
    - Connection pooling and retry mechanisms
    - Comprehensive error handling and logging
    - Schema validation and rollback capabilities
    """

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0) -> None:
        """
        Initialize the enhanced Supabase sync manager

        Args:
            max_retries: Maximum number of retry attempts for failed operations
            retry_delay: Delay between retry attempts in seconds

        Raises:
            ValueError: If required environment variables are not set
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # Get environment variables
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
            )

        # Initialize clients
        self.supabase_client: Optional[Client] = None
        self.sqlalchemy_engine: Optional[Engine] = None

        logger.info("Enhanced Supabase sync manager initialized")

    def get_supabase_client(self) -> Client:
        """
        Get or create a Supabase client with connection validation

        Returns:
            Configured Supabase client

        Raises:
            ConnectionError: If unable to connect to Supabase
        """
        if self.supabase_client is None:
            try:
                self.supabase_client = create_client(
                    self.supabase_url, self.supabase_key
                )
                # Test connection
                self.supabase_client.table("_test_connection").select("*").limit(
                    1
                ).execute()
                logger.info("Supabase client connected successfully")
            except Exception as e:
                logger.error(f"Failed to connect to Supabase: {e}")
                raise ConnectionError(f"Unable to connect to Supabase: {e}")

        return self.supabase_client

    def get_sqlalchemy_engine(self) -> Engine:
        """
        Get or create a SQLAlchemy engine for direct database operations

        Returns:
            Configured SQLAlchemy engine

        Raises:
            ConnectionError: If unable to create database engine
        """
        if self.sqlalchemy_engine is None:
            try:
                # Extract database URL from Supabase URL
                db_url = self.supabase_url.replace("https://", "postgresql://postgres:")
                db_url = f"{db_url}@db.{self.supabase_url.split('//')[1].split('.')[0]}.supabase.co:5432/postgres"

                self.sqlalchemy_engine = create_engine(
                    db_url,
                    pool_size=5,
                    max_overflow=10,
                    pool_pre_ping=True,
                    pool_recycle=3600,
                )

                # Test connection
                with self.sqlalchemy_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))

                logger.info("SQLAlchemy engine created successfully")
            except Exception as e:
                logger.error(f"Failed to create SQLAlchemy engine: {e}")
                raise ConnectionError(f"Unable to create database engine: {e}")

        return self.sqlalchemy_engine

    @contextmanager
    def database_transaction(self):
        """
        Context manager for database transactions with automatic rollback on error

        Yields:
            SQLAlchemy connection object

        Raises:
            SQLAlchemyError: If database operation fails
        """
        engine = self.get_sqlalchemy_engine()
        connection = engine.connect()
        transaction = connection.begin()

        try:
            yield connection
            transaction.commit()
            logger.debug("Database transaction committed successfully")
        except Exception as e:
            transaction.rollback()
            logger.error(f"Database transaction rolled back due to error: {e}")
            raise
        finally:
            connection.close()

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

    def setup_alembic_environment(self) -> Config:
        """
        Set up Alembic configuration for database migrations

        Returns:
            Configured Alembic Config object

        Raises:
            FileNotFoundError: If alembic.ini is not found
        """
        alembic_cfg_path = os.path.join(os.getcwd(), "alembic.ini")

        if not os.path.exists(alembic_cfg_path):
            raise FileNotFoundError(
                "alembic.ini not found. Run 'alembic init alembic' first."
            )

        alembic_cfg = Config(alembic_cfg_path)

        # Set the database URL for Alembic
        engine = self.get_sqlalchemy_engine()
        alembic_cfg.set_main_option("sqlalchemy.url", str(engine.url))

        logger.info("Alembic environment configured")
        return alembic_cfg

    def create_migration(self, message: str, auto_generate: bool = True) -> SyncResult:
        """
        Create a new Alembic migration

        Args:
            message: Description of the migration
            auto_generate: Whether to auto-generate migration from model changes

        Returns:
            SyncResult indicating success or failure
        """
        start_time = time.time()
        errors = []

        try:
            alembic_cfg = self.setup_alembic_environment()

            if auto_generate:
                command.revision(alembic_cfg, message=message, autogenerate=True)
            else:
                command.revision(alembic_cfg, message=message)

            execution_time = time.time() - start_time

            return SyncResult(
                success=True,
                message=f"Migration '{message}' created successfully",
                details={"execution_time": execution_time},
                errors=[],
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Failed to create migration: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

            return SyncResult(
                success=False,
                message="Migration creation failed",
                details={"error": str(e)},
                errors=errors,
                execution_time=execution_time,
            )

    def apply_migrations(self, target_revision: Optional[str] = None) -> SyncResult:
        """
        Apply database migrations using Alembic

        Args:
            target_revision: Specific revision to migrate to (None for latest)

        Returns:
            SyncResult indicating success or failure
        """
        start_time = time.time()
        errors = []

        try:
            alembic_cfg = self.setup_alembic_environment()

            # Apply migrations
            if target_revision:
                command.upgrade(alembic_cfg, target_revision)
                message = f"Migrated to revision {target_revision}"
            else:
                command.upgrade(alembic_cfg, "head")
                message = "Migrated to latest revision"

            execution_time = time.time() - start_time

            return SyncResult(
                success=True,
                message=message,
                details={
                    "target_revision": target_revision,
                    "execution_time": execution_time,
                },
                errors=[],
                execution_time=execution_time,
            )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Failed to apply migrations: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

            return SyncResult(
                success=False,
                message="Migration application failed",
                details={"error": str(e)},
                errors=errors,
                execution_time=execution_time,
            )

    def get_migration_status(self) -> Dict[str, Any]:
        """
        Get current migration status

        Returns:
            Dictionary containing migration status information
        """
        try:
            alembic_cfg = self.setup_alembic_environment()
            engine = self.get_sqlalchemy_engine()

            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_revision = context.get_current_revision()

                # Get available revisions
                script_directory = alembic_cfg.get_main_option("script_location")

                return {
                    "current_revision": current_revision,
                    "script_directory": script_directory,
                    "status": "up_to_date" if current_revision else "needs_migration",
                }

        except Exception as e:
            logger.error(f"Failed to get migration status: {e}")
            return {"error": str(e)}

    def validate_schema(self) -> SyncResult:
        """
        Validate the current database schema

        Returns:
            SyncResult indicating validation success or failure
        """
        start_time = time.time()
        errors = []

        try:
            with self.database_transaction() as conn:
                # Check for required tables
                required_tables = ["agents", "events", "flows", "timeline_tensors"]

                for table in required_tables:
                    result = conn.execute(
                        text(
                            f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = '{table}'
                        );
                    """
                        )
                    )

                    if not result.scalar():
                        errors.append(f"Required table '{table}' not found")

                execution_time = time.time() - start_time

                if errors:
                    return SyncResult(
                        success=False,
                        message="Schema validation failed",
                        details={"missing_tables": errors},
                        errors=errors,
                        execution_time=execution_time,
                    )
                else:
                    return SyncResult(
                        success=True,
                        message="Schema validation passed",
                        details={"validated_tables": required_tables},
                        errors=[],
                        execution_time=execution_time,
                    )

        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Schema validation error: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

            return SyncResult(
                success=False,
                message="Schema validation failed",
                details={"error": str(e)},
                errors=errors,
                execution_time=execution_time,
            )

    def sync_database(self, validate_first: bool = True) -> SyncResult:
        """
        Perform complete database synchronization

        Args:
            validate_first: Whether to validate schema before syncing

        Returns:
            SyncResult indicating overall sync success or failure
        """
        start_time = time.time()
        all_errors = []

        logger.info("🔄 Starting enhanced database synchronization...")

        try:
            # Validate schema if requested
            if validate_first:
                validation_result = self.validate_schema()
                if not validation_result.success:
                    logger.warning(
                        "Schema validation failed, proceeding with migration"
                    )
                    all_errors.extend(validation_result.errors)

            # Apply migrations
            migration_result = self.apply_migrations()
            if not migration_result.success:
                all_errors.extend(migration_result.errors)
                return SyncResult(
                    success=False,
                    message="Database synchronization failed during migration",
                    details={"migration_errors": migration_result.errors},
                    errors=all_errors,
                    execution_time=time.time() - start_time,
                )

            # Final validation
            final_validation = self.validate_schema()
            if not final_validation.success:
                all_errors.extend(final_validation.errors)

            execution_time = time.time() - start_time

            success = len(all_errors) == 0
            message = (
                "Database synchronization completed successfully"
                if success
                else "Database synchronization completed with warnings"
            )

            return SyncResult(
                success=success,
                message=message,
                details={
                    "migration_applied": migration_result.success,
                    "schema_validated": final_validation.success,
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

            return SyncResult(
                success=False,
                message="Database synchronization failed",
                details={"error": str(e)},
                errors=all_errors,
                execution_time=execution_time,
            )


def main() -> bool:
    """
    Main synchronization function with enhanced error handling

    Returns:
        True if synchronization was successful, False otherwise
    """
    try:
        sync_manager = EnhancedSupabaseSync()

        # Perform synchronization
        result = sync_manager.sync_database()

        # Log results
        if result.success:
            logger.info("✅ Enhanced synchronization completed successfully")
            logger.info(f"   - Execution time: {result.execution_time:.2f} seconds")
            logger.info(f"   - Details: {result.details}")
        else:
            logger.error("❌ Enhanced synchronization failed")
            logger.error(f"   - Message: {result.message}")
            logger.error(f"   - Errors: {result.errors}")

        # Print migration status
        status = sync_manager.get_migration_status()
        logger.info(f"📊 Migration Status: {status}")

        return result.success

    except Exception as e:
        logger.error(f"❌ Critical error in main synchronization: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
