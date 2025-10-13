"""
Enhanced Database Client

This module provides enhanced database clients for Supabase and Neon
with connection pooling, retry logic, and transaction support.
"""

import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

from ..config import get_config
from ..exceptions import (
    DatabaseConnectionError,
    DatabaseQueryError,
    DatabaseSyncError,
    RetryableError,
)
from ..utils.retry import RetryContext, exponential_backoff

logger = logging.getLogger(__name__)


class EnhancedSupabaseClient:
    """
    Enhanced Supabase client with retry logic and connection management.
    """

    def __init__(self, supabase_client=None):
        """
        Initialize the enhanced Supabase client.

        Args:
            supabase_client: Optional pre-configured Supabase client
        """
        self.config = get_config()
        self._client = supabase_client
        self._connected = False

    @property
    def client(self):
        """Get or create the Supabase client."""
        if self._client is None:
            self._connect()
        return self._client

    def _connect(self):
        """Establish connection to Supabase."""
        try:
            from supabase import create_client

            if (
                not self.config.database.supabase_url
                or not self.config.database.supabase_key
            ):
                raise DatabaseConnectionError(
                    "Supabase credentials not configured",
                    details={
                        "url_present": bool(self.config.database.supabase_url),
                        "key_present": bool(self.config.database.supabase_key),
                    },
                )

            self._client = create_client(
                self.config.database.supabase_url, self.config.database.supabase_key
            )
            self._connected = True
            logger.info("Successfully connected to Supabase")

        except ImportError:
            raise DatabaseConnectionError(
                "Supabase client not installed. Install with: pip install supabase"
            )
        except Exception as e:
            raise DatabaseConnectionError(
                f"Failed to connect to Supabase: {str(e)}",
                details={"error_type": type(e).__name__},
            )

    @exponential_backoff(
        max_retries=3,
        initial_delay=1.0,
        exceptions=(DatabaseQueryError, RetryableError),
    )
    def execute_query(
        self, table: str, operation: str, data: Dict = None, filters: Dict = None
    ) -> Any:
        """
        Execute a database query with retry logic.

        Args:
            table: Table name
            operation: Operation type ('select', 'insert', 'update', 'delete', 'upsert')
            data: Data for insert/update/upsert operations
            filters: Filters for select/update/delete operations

        Returns:
            Query result

        Raises:
            DatabaseQueryError: If query execution fails
        """
        try:
            query = self.client.table(table)

            if operation == "select":
                query = query.select("*")
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.execute()

            elif operation == "insert":
                if not data:
                    raise DatabaseQueryError("Insert operation requires data")
                result = query.insert(data).execute()

            elif operation == "update":
                if not data:
                    raise DatabaseQueryError("Update operation requires data")
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.update(data).execute()

            elif operation == "delete":
                if filters:
                    for key, value in filters.items():
                        query = query.eq(key, value)
                result = query.delete().execute()

            elif operation == "upsert":
                if not data:
                    raise DatabaseQueryError("Upsert operation requires data")
                result = query.upsert(data).execute()

            else:
                raise DatabaseQueryError(f"Unsupported operation: {operation}")

            logger.debug(f"Successfully executed {operation} on {table}")
            return result

        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise DatabaseQueryError(
                f"Failed to execute {operation} on {table}: {str(e)}",
                details={"table": table, "operation": operation},
            )

    def bulk_insert(self, table: str, records: List[Dict]) -> Any:
        """
        Bulk insert records with batching.

        Args:
            table: Table name
            records: List of records to insert

        Returns:
            Insert result
        """
        batch_size = self.config.system.batch_size
        results = []

        for i in range(0, len(records), batch_size):
            batch = records[i : i + batch_size]
            result = self.execute_query(table, "insert", data=batch)
            results.append(result)
            logger.info(f"Inserted batch {i // batch_size + 1} ({len(batch)} records)")

        return results

    def health_check(self) -> bool:
        """
        Check if the database connection is healthy.

        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            # Try a simple query to check connection
            self.client.table("_health_check").select("*").limit(1).execute()
            return True
        except:
            return False


class EnhancedNeonClient:
    """
    Enhanced Neon client with connection pooling and retry logic.
    """

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the enhanced Neon client.

        Args:
            connection_string: Optional PostgreSQL connection string
        """
        self.config = get_config()
        self.connection_string = (
            connection_string or self.config.database.neon_connection_string
        )
        self._engine = None
        self._session_factory = None

    def _create_engine(self):
        """Create SQLAlchemy engine with connection pooling."""
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker

            if not self.connection_string:
                raise DatabaseConnectionError("Neon connection string not configured")

            self._engine = create_engine(
                self.connection_string,
                pool_size=self.config.database.pool_size,
                max_overflow=self.config.database.max_overflow,
                pool_timeout=self.config.database.pool_timeout,
                pool_recycle=self.config.database.pool_recycle,
                echo=self.config.system.debug,
            )

            self._session_factory = sessionmaker(bind=self._engine)
            logger.info("Successfully created Neon engine with connection pooling")

        except ImportError:
            raise DatabaseConnectionError(
                "SQLAlchemy not installed. Install with: pip install sqlalchemy psycopg2-binary"
            )
        except Exception as e:
            raise DatabaseConnectionError(
                f"Failed to create Neon engine: {str(e)}",
                details={"error_type": type(e).__name__},
            )

    @property
    def engine(self):
        """Get or create the SQLAlchemy engine."""
        if self._engine is None:
            self._create_engine()
        return self._engine

    @contextmanager
    def session(self):
        """
        Context manager for database sessions with automatic commit/rollback.

        Yields:
            SQLAlchemy session

        Example:
            with client.session() as session:
                session.execute("SELECT * FROM table")
        """
        if self._session_factory is None:
            self._create_engine()

        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session error, rolling back: {str(e)}")
            raise DatabaseQueryError(f"Database operation failed: {str(e)}")
        finally:
            session.close()

    @exponential_backoff(
        max_retries=3,
        initial_delay=1.0,
        exceptions=(DatabaseQueryError, RetryableError),
    )
    def execute_sql(self, sql: str, params: Dict = None) -> Any:
        """
        Execute raw SQL with retry logic.

        Args:
            sql: SQL query string
            params: Query parameters

        Returns:
            Query result
        """
        try:
            with self.session() as session:
                result = session.execute(sql, params or {})
                return result.fetchall() if result.returns_rows else result

        except Exception as e:
            logger.error(f"SQL execution failed: {str(e)}")
            raise DatabaseQueryError(
                f"Failed to execute SQL: {str(e)}",
                details={"sql": sql[:100]},  # Log first 100 chars of SQL
            )

    def health_check(self) -> bool:
        """
        Check if the database connection is healthy.

        Returns:
            bool: True if connection is healthy, False otherwise
        """
        try:
            with self.session() as session:
                session.execute("SELECT 1")
            return True
        except:
            return False

    def close(self):
        """Close the database engine and all connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Closed Neon database connections")
