"""
Integration Tests for Database Synchronization

Tests for Supabase and Neon database synchronization functionality.
"""

import pytest
import os
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock

from src.database_sync.enhanced_client import EnhancedSupabaseClient, EnhancedNeonClient
from src.database_sync.schema_validator import SchemaValidator, Column, ColumnType, Table
from src.exceptions import DatabaseConnectionError, DatabaseQueryError, DatabaseSchemaError


class TestEnhancedSupabaseClient:
    """Tests for EnhancedSupabaseClient."""
    
    @pytest.fixture
    def mock_supabase_client(self):
        """Create a mock Supabase client."""
        mock_client = Mock()
        mock_table = Mock()
        mock_client.table.return_value = mock_table
        return mock_client
    
    @pytest.fixture
    def client(self, mock_supabase_client):
        """Create an EnhancedSupabaseClient with mock."""
        return EnhancedSupabaseClient(supabase_client=mock_supabase_client)
    
    def test_execute_query_select(self, client, mock_supabase_client):
        """Test execute_query with SELECT operation."""
        # Setup mock
        mock_result = Mock()
        mock_result.data = [{"id": 1, "name": "test"}]
        
        mock_table = Mock()
        mock_table.select.return_value = mock_table
        mock_table.eq.return_value = mock_table
        mock_table.execute.return_value = mock_result
        
        mock_supabase_client.table.return_value = mock_table
        
        # Execute
        result = client.execute_query(
            table="evidence",
            operation="select",
            filters={"case_id": "case_001"}
        )
        
        # Verify
        assert result == mock_result
        mock_supabase_client.table.assert_called_once_with("evidence")
        mock_table.select.assert_called_once_with("*")
        mock_table.eq.assert_called_once_with("case_id", "case_001")
    
    def test_execute_query_insert(self, client, mock_supabase_client):
        """Test execute_query with INSERT operation."""
        # Setup mock
        mock_result = Mock()
        mock_table = Mock()
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = mock_result
        
        mock_supabase_client.table.return_value = mock_table
        
        # Execute
        data = {"case_id": "case_001", "evidence_type": "document"}
        result = client.execute_query(
            table="evidence",
            operation="insert",
            data=data
        )
        
        # Verify
        assert result == mock_result
        mock_table.insert.assert_called_once_with(data)
    
    def test_execute_query_update(self, client, mock_supabase_client):
        """Test execute_query with UPDATE operation."""
        # Setup mock
        mock_result = Mock()
        mock_table = Mock()
        mock_table.eq.return_value = mock_table
        mock_table.update.return_value = mock_table
        mock_table.execute.return_value = mock_result
        
        mock_supabase_client.table.return_value = mock_table
        
        # Execute
        data = {"verified": True}
        result = client.execute_query(
            table="evidence",
            operation="update",
            data=data,
            filters={"id": "123"}
        )
        
        # Verify
        assert result == mock_result
        mock_table.update.assert_called_once_with(data)
    
    def test_execute_query_invalid_operation(self, client):
        """Test execute_query with invalid operation."""
        with pytest.raises(DatabaseQueryError) as exc_info:
            client.execute_query(
                table="evidence",
                operation="invalid_op"
            )
        
        assert "Unsupported operation" in str(exc_info.value)
    
    def test_bulk_insert(self, client, mock_supabase_client):
        """Test bulk_insert with batching."""
        # Setup mock
        mock_result = Mock()
        mock_table = Mock()
        mock_table.insert.return_value = mock_table
        mock_table.execute.return_value = mock_result
        
        mock_supabase_client.table.return_value = mock_table
        
        # Create test records
        records = [{"id": i, "name": f"test_{i}"} for i in range(250)]
        
        # Execute
        with patch('src.config.get_config') as mock_config:
            mock_config.return_value.system.batch_size = 100
            results = client.bulk_insert("evidence", records)
        
        # Verify - should be split into 3 batches (100, 100, 50)
        assert len(results) == 3
        assert mock_table.insert.call_count == 3


class TestEnhancedNeonClient:
    """Tests for EnhancedNeonClient."""
    
    @pytest.fixture
    def mock_engine(self):
        """Create a mock SQLAlchemy engine."""
        mock_engine = Mock()
        return mock_engine
    
    @pytest.fixture
    def client(self):
        """Create an EnhancedNeonClient."""
        return EnhancedNeonClient(connection_string="postgresql://user:pass@localhost/db")
    
    def test_session_context_manager_success(self, client):
        """Test session context manager with successful operation."""
        with patch('src.database_sync.enhanced_client.sessionmaker') as mock_sessionmaker:
            mock_session = Mock()
            mock_sessionmaker.return_value.return_value = mock_session
            
            with patch.object(client, '_create_engine'):
                with client.session() as session:
                    session.execute("SELECT 1")
                
                # Verify commit was called
                mock_session.commit.assert_called_once()
                mock_session.close.assert_called_once()
    
    def test_session_context_manager_error(self, client):
        """Test session context manager with error and rollback."""
        with patch('src.database_sync.enhanced_client.sessionmaker') as mock_sessionmaker:
            mock_session = Mock()
            mock_session.execute.side_effect = Exception("Database error")
            mock_sessionmaker.return_value.return_value = mock_session
            
            with patch.object(client, '_create_engine'):
                with pytest.raises(DatabaseQueryError):
                    with client.session() as session:
                        session.execute("SELECT 1")
                
                # Verify rollback was called
                mock_session.rollback.assert_called_once()
                mock_session.close.assert_called_once()
    
    def test_execute_sql(self, client):
        """Test execute_sql with parameters."""
        mock_result = Mock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [("test",)]
        
        with patch.object(client, 'session') as mock_session_ctx:
            mock_session = Mock()
            mock_session.execute.return_value = mock_result
            mock_session_ctx.return_value.__enter__.return_value = mock_session
            mock_session_ctx.return_value.__exit__.return_value = False
            
            result = client.execute_sql("SELECT * FROM evidence WHERE id = :id", {"id": "123"})
            
            assert result == [("test",)]
            mock_session.execute.assert_called_once()


class TestSchemaValidator:
    """Tests for SchemaValidator."""
    
    @pytest.fixture
    def validator(self):
        """Create a SchemaValidator instance."""
        return SchemaValidator()
    
    def test_validate_schema_valid(self, validator):
        """Test schema validation with valid schema."""
        actual_columns = {
            "id", "case_id", "evidence_type", "description", "file_path",
            "hash", "collected_date", "collected_by", "chain_of_custody",
            "metadata", "created_at", "updated_at"
        }
        
        errors = validator.validate_schema("evidence", actual_columns)
        assert len(errors) == 0
    
    def test_validate_schema_missing_columns(self, validator):
        """Test schema validation with missing columns."""
        actual_columns = {"id", "case_id", "evidence_type"}
        
        errors = validator.validate_schema("evidence", actual_columns)
        assert len(errors) > 0
        assert "Missing columns" in errors[0]
    
    def test_validate_schema_unknown_table(self, validator):
        """Test schema validation with unknown table."""
        errors = validator.validate_schema("unknown_table", set())
        assert len(errors) == 1
        assert "Unknown table" in errors[0]
    
    def test_generate_migration_sql(self, validator):
        """Test migration SQL generation."""
        sql_statements = validator.generate_migration_sql("evidence")
        
        assert len(sql_statements) > 0
        assert "CREATE TABLE" in sql_statements[0]
        assert "evidence" in sql_statements[0]
        
        # Check that indexes are included
        index_statements = [s for s in sql_statements if "CREATE INDEX" in s]
        assert len(index_statements) > 0
    
    def test_generate_migration_sql_unknown_table(self, validator):
        """Test migration SQL generation for unknown table."""
        with pytest.raises(DatabaseSchemaError) as exc_info:
            validator.generate_migration_sql("unknown_table")
        
        assert "Unknown table" in str(exc_info.value)
    
    def test_generate_all_migrations(self, validator):
        """Test generation of all migration SQL."""
        all_migrations = validator.generate_all_migrations()
        
        assert isinstance(all_migrations, dict)
        assert len(all_migrations) > 0
        
        # Check that all expected tables are present
        expected_tables = ["evidence", "timeline_events", "entities", "hypergraph_nodes", "hypergraph_edges", "sync_log"]
        for table in expected_tables:
            assert table in all_migrations
            assert len(all_migrations[table]) > 0


class TestColumn:
    """Tests for Column class."""
    
    def test_column_to_sql_basic(self):
        """Test basic column SQL generation."""
        col = Column("name", ColumnType.TEXT)
        sql = col.to_sql()
        
        assert '"name"' in sql
        assert "text" in sql
    
    def test_column_to_sql_primary_key(self):
        """Test primary key column SQL generation."""
        col = Column("id", ColumnType.UUID, nullable=False, primary_key=True)
        sql = col.to_sql()
        
        assert "PRIMARY KEY" in sql
        assert "NOT NULL" in sql
    
    def test_column_to_sql_with_default(self):
        """Test column with default value SQL generation."""
        col = Column("created_at", ColumnType.TIMESTAMPTZ, default="now()")
        sql = col.to_sql()
        
        assert "DEFAULT now()" in sql
    
    def test_column_to_sql_foreign_key(self):
        """Test foreign key column SQL generation."""
        col = Column("entity_id", ColumnType.UUID, foreign_key="entities(id)")
        sql = col.to_sql()
        
        assert "REFERENCES entities(id)" in sql


class TestTable:
    """Tests for Table class."""
    
    def test_table_to_create_sql(self):
        """Test CREATE TABLE SQL generation."""
        table = Table(
            name="test_table",
            columns=[
                Column("id", ColumnType.UUID, nullable=False, primary_key=True),
                Column("name", ColumnType.TEXT, nullable=False),
                Column("created_at", ColumnType.TIMESTAMPTZ, default="now()"),
            ]
        )
        
        sql = table.to_create_sql()
        
        assert "CREATE TABLE IF NOT EXISTS" in sql
        assert "test_table" in sql
        assert '"id"' in sql
        assert '"name"' in sql
        assert '"created_at"' in sql
    
    def test_table_get_column_names(self):
        """Test getting column names from table."""
        table = Table(
            name="test_table",
            columns=[
                Column("id", ColumnType.UUID),
                Column("name", ColumnType.TEXT),
                Column("email", ColumnType.TEXT),
            ]
        )
        
        column_names = table.get_column_names()
        
        assert column_names == {"id", "name", "email"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

