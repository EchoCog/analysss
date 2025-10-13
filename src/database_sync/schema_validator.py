"""
Schema Validator

This module provides automated schema validation and migration tools
for Supabase and Neon databases.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from ..exceptions import DatabaseSchemaError

logger = logging.getLogger(__name__)


class ColumnType(Enum):
    """Database column types."""

    INTEGER = "integer"
    BIGINT = "bigint"
    TEXT = "text"
    VARCHAR = "varchar"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    TIMESTAMPTZ = "timestamptz"
    JSON = "json"
    JSONB = "jsonb"
    UUID = "uuid"
    FLOAT = "float"
    DOUBLE = "double precision"


@dataclass
class Column:
    """Represents a database column."""

    name: str
    type: ColumnType
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[Any] = None
    foreign_key: Optional[str] = None

    def to_sql(self) -> str:
        """Convert column definition to SQL."""
        parts = [f'"{self.name}"', self.type.value]

        if self.primary_key:
            parts.append("PRIMARY KEY")
        if not self.nullable:
            parts.append("NOT NULL")
        if self.unique and not self.primary_key:
            parts.append("UNIQUE")
        if self.default is not None:
            parts.append(f"DEFAULT {self.default}")
        if self.foreign_key:
            parts.append(f"REFERENCES {self.foreign_key}")

        return " ".join(parts)


@dataclass
class Table:
    """Represents a database table."""

    name: str
    columns: List[Column]
    indexes: List[str] = None
    constraints: List[str] = None

    def __post_init__(self):
        if self.indexes is None:
            self.indexes = []
        if self.constraints is None:
            self.constraints = []

    def to_create_sql(self) -> str:
        """Generate CREATE TABLE SQL."""
        column_defs = [col.to_sql() for col in self.columns]

        sql = f'CREATE TABLE IF NOT EXISTS "{self.name}" (\n'
        sql += ",\n".join(f"  {col_def}" for col_def in column_defs)

        if self.constraints:
            sql += ",\n" + ",\n".join(
                f"  {constraint}" for constraint in self.constraints
            )

        sql += "\n);"

        return sql

    def get_column_names(self) -> Set[str]:
        """Get set of column names."""
        return {col.name for col in self.columns}


class SchemaValidator:
    """
    Validates and manages database schemas for Supabase and Neon.
    """

    def __init__(self):
        self.expected_schemas = self._define_expected_schemas()

    def _define_expected_schemas(self) -> Dict[str, Table]:
        """
        Define expected database schemas.

        Returns:
            Dictionary mapping table names to Table definitions
        """
        return {
            "evidence": Table(
                name="evidence",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("case_id", ColumnType.TEXT, nullable=False),
                    Column("evidence_type", ColumnType.TEXT, nullable=False),
                    Column("description", ColumnType.TEXT),
                    Column("file_path", ColumnType.TEXT),
                    Column("hash", ColumnType.TEXT),
                    Column("collected_date", ColumnType.TIMESTAMPTZ),
                    Column("collected_by", ColumnType.TEXT),
                    Column("chain_of_custody", ColumnType.JSONB),
                    Column("metadata", ColumnType.JSONB),
                    Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
                    Column("updated_at", ColumnType.TIMESTAMPTZ, default="now()"),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_evidence_case_id ON "evidence"(case_id);',
                    'CREATE INDEX IF NOT EXISTS idx_evidence_type ON "evidence"(evidence_type);',
                    'CREATE INDEX IF NOT EXISTS idx_evidence_collected_date ON "evidence"(collected_date);',
                ],
            ),
            "timeline_events": Table(
                name="timeline_events",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("case_id", ColumnType.TEXT, nullable=False),
                    Column("event_date", ColumnType.TIMESTAMPTZ, nullable=False),
                    Column("event_type", ColumnType.TEXT, nullable=False),
                    Column("description", ColumnType.TEXT),
                    Column("actors", ColumnType.JSONB),
                    Column("evidence_ids", ColumnType.JSONB),
                    Column("location", ColumnType.TEXT),
                    Column("verified", ColumnType.BOOLEAN, default="false"),
                    Column("confidence_score", ColumnType.FLOAT),
                    Column("metadata", ColumnType.JSONB),
                    Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
                    Column("updated_at", ColumnType.TIMESTAMPTZ, default="now()"),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_timeline_case_id ON "timeline_events"(case_id);',
                    'CREATE INDEX IF NOT EXISTS idx_timeline_event_date ON "timeline_events"(event_date);',
                    'CREATE INDEX IF NOT EXISTS idx_timeline_event_type ON "timeline_events"(event_type);',
                ],
            ),
            "entities": Table(
                name="entities",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("case_id", ColumnType.TEXT, nullable=False),
                    Column("entity_type", ColumnType.TEXT, nullable=False),
                    Column("name", ColumnType.TEXT, nullable=False),
                    Column("role", ColumnType.TEXT),
                    Column("attributes", ColumnType.JSONB),
                    Column("relationships", ColumnType.JSONB),
                    Column("metadata", ColumnType.JSONB),
                    Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
                    Column("updated_at", ColumnType.TIMESTAMPTZ, default="now()"),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_entities_case_id ON "entities"(case_id);',
                    'CREATE INDEX IF NOT EXISTS idx_entities_type ON "entities"(entity_type);',
                    'CREATE INDEX IF NOT EXISTS idx_entities_name ON "entities"(name);',
                ],
            ),
            "hypergraph_nodes": Table(
                name="hypergraph_nodes",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("case_id", ColumnType.TEXT, nullable=False),
                    Column("node_type", ColumnType.TEXT, nullable=False),
                    Column("entity_id", ColumnType.UUID),
                    Column("properties", ColumnType.JSONB),
                    Column("embedding", ColumnType.JSONB),
                    Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
                    Column("updated_at", ColumnType.TIMESTAMPTZ, default="now()"),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_case_id ON "hypergraph_nodes"(case_id);',
                    'CREATE INDEX IF NOT EXISTS idx_hypergraph_nodes_type ON "hypergraph_nodes"(node_type);',
                ],
            ),
            "hypergraph_edges": Table(
                name="hypergraph_edges",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("case_id", ColumnType.TEXT, nullable=False),
                    Column("edge_type", ColumnType.TEXT, nullable=False),
                    Column("source_nodes", ColumnType.JSONB, nullable=False),
                    Column("target_nodes", ColumnType.JSONB, nullable=False),
                    Column("weight", ColumnType.FLOAT, default="1.0"),
                    Column("properties", ColumnType.JSONB),
                    Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
                    Column("updated_at", ColumnType.TIMESTAMPTZ, default="now()"),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_case_id ON "hypergraph_edges"(case_id);',
                    'CREATE INDEX IF NOT EXISTS idx_hypergraph_edges_type ON "hypergraph_edges"(edge_type);',
                ],
            ),
            "sync_log": Table(
                name="sync_log",
                columns=[
                    Column(
                        "id",
                        ColumnType.UUID,
                        nullable=False,
                        primary_key=True,
                        default="gen_random_uuid()",
                    ),
                    Column("sync_type", ColumnType.TEXT, nullable=False),
                    Column("source_db", ColumnType.TEXT, nullable=False),
                    Column("target_db", ColumnType.TEXT, nullable=False),
                    Column("status", ColumnType.TEXT, nullable=False),
                    Column("records_synced", ColumnType.INTEGER, default="0"),
                    Column("errors", ColumnType.JSONB),
                    Column("started_at", ColumnType.TIMESTAMPTZ, nullable=False),
                    Column("completed_at", ColumnType.TIMESTAMPTZ),
                    Column("metadata", ColumnType.JSONB),
                ],
                indexes=[
                    'CREATE INDEX IF NOT EXISTS idx_sync_log_type ON "sync_log"(sync_type);',
                    'CREATE INDEX IF NOT EXISTS idx_sync_log_status ON "sync_log"(status);',
                    'CREATE INDEX IF NOT EXISTS idx_sync_log_started_at ON "sync_log"(started_at);',
                ],
            ),
        }

    def validate_schema(self, table_name: str, actual_columns: Set[str]) -> List[str]:
        """
        Validate that actual schema matches expected schema.

        Args:
            table_name: Name of the table to validate
            actual_columns: Set of actual column names in the database

        Returns:
            List of validation errors (empty if valid)
        """
        if table_name not in self.expected_schemas:
            return [f"Unknown table: {table_name}"]

        expected_table = self.expected_schemas[table_name]
        expected_columns = expected_table.get_column_names()

        errors = []

        # Check for missing columns
        missing = expected_columns - actual_columns
        if missing:
            errors.append(f"Missing columns in {table_name}: {', '.join(missing)}")

        # Check for extra columns (warning, not error)
        extra = actual_columns - expected_columns
        if extra:
            logger.warning(f"Extra columns in {table_name}: {', '.join(extra)}")

        return errors

    def generate_migration_sql(self, table_name: str) -> List[str]:
        """
        Generate SQL statements to create or migrate a table.

        Args:
            table_name: Name of the table

        Returns:
            List of SQL statements
        """
        if table_name not in self.expected_schemas:
            raise DatabaseSchemaError(f"Unknown table: {table_name}")

        table = self.expected_schemas[table_name]
        sql_statements = [table.to_create_sql()]
        sql_statements.extend(table.indexes)

        return sql_statements

    def generate_all_migrations(self) -> Dict[str, List[str]]:
        """
        Generate migration SQL for all tables.

        Returns:
            Dictionary mapping table names to SQL statements
        """
        return {
            table_name: self.generate_migration_sql(table_name)
            for table_name in self.expected_schemas.keys()
        }
