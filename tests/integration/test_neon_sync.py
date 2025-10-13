#!/usr/bin/env python3
"""
Tests for Neon Database Synchronization
=======================================

Comprehensive test suite for the neon_sync.py functionality.
"""

import os
import pytest
from unittest.mock import Mock, patch, mock_open
import psycopg2

from neon_sync import (
    get_neon_connection,
    check_existing_tables,
    execute_schema,
    verify_schema_integrity,
    main
)


class TestNeonSync:
    """Test suite for Neon database synchronization functionality."""

    def test_get_neon_connection_success(self):
        """Test successful Neon connection creation."""
        with patch.dict(os.environ, {'NEON_DATABASE_URL': 'postgresql://test:test@test.com/test'}):
            with patch('psycopg2.connect') as mock_connect:
                mock_conn = Mock()
                mock_connect.return_value = mock_conn
                
                conn = get_neon_connection()
                
                assert conn == mock_conn
                mock_connect.assert_called_once_with('postgresql://test:test@test.com/test')
                mock_conn.set_isolation_level.assert_called_once()

    def test_get_neon_connection_missing_env_var(self):
        """Test Neon connection with missing environment variable."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="NEON_DATABASE_URL"):
                get_neon_connection()

    def test_get_neon_connection_error(self):
        """Test Neon connection with connection error."""
        with patch.dict(os.environ, {'NEON_DATABASE_URL': 'invalid://url'}):
            with patch('psycopg2.connect', side_effect=psycopg2.Error("Connection failed")):
                with pytest.raises(ConnectionError, match="Failed to connect"):
                    get_neon_connection()

    def test_check_existing_tables_success(self):
        """Test successful table checking."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [('entities',), ('events',)]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        tables = check_existing_tables(mock_conn)
        
        assert tables == ['entities', 'events']
        mock_cursor.execute.assert_called_once()

    def test_check_existing_tables_error(self):
        """Test table checking with error."""
        mock_conn = Mock()
        mock_conn.cursor.side_effect = Exception("Database error")
        
        tables = check_existing_tables(mock_conn)
        
        assert tables == []

    def test_execute_schema_file_not_found(self):
        """Test schema execution when schema file doesn't exist."""
        mock_conn = Mock()
        
        with patch('os.path.exists', return_value=False):
            result = execute_schema(mock_conn, "nonexistent.sql")
            
            assert "error" in result
            assert "Schema file" in result["error"]

    def test_execute_schema_success(self):
        """Test successful schema execution."""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        schema_content = """
        CREATE TABLE entities (id TEXT PRIMARY KEY);
        CREATE INDEX idx_entities ON entities(id);
        -- This is a comment
        """
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=schema_content)):
                result = execute_schema(mock_conn, "schema.sql")
                
                assert result["status"] == "success"
                assert "executed_statements" in result
                # Should execute 2 statements (CREATE TABLE and CREATE INDEX)
                assert len(result["executed_statements"]) == 2
                assert mock_cursor.execute.call_count == 2

    def test_execute_schema_with_existing_relations(self):
        """Test schema execution with existing relations."""
        mock_conn = Mock()
        mock_cursor = Mock()
        
        # Simulate "already exists" error for first statement, success for second
        mock_cursor.execute.side_effect = [
            psycopg2.Error("relation already exists"),
            None  # Success
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        schema_content = """
        CREATE TABLE entities (id TEXT PRIMARY KEY);
        CREATE INDEX idx_entities ON entities(id);
        """
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=schema_content)):
                result = execute_schema(mock_conn, "schema.sql")
                
                assert result["status"] == "success"
                # Should have 1 successful execution (the index creation)
                assert len(result["executed_statements"]) == 1

    def test_verify_schema_integrity_success(self):
        """Test successful schema verification."""
        mock_conn = Mock()
        mock_cursor = Mock()
        
        # Mock responses for table and index existence checks
        # All tables and indexes exist
        mock_cursor.fetchone.side_effect = [(True,)] * 12  # 4 tables + 8 indexes
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        result = verify_schema_integrity(mock_conn)
        
        assert len(result["tables_verified"]) == 4
        assert len(result["indexes_verified"]) == 8
        assert len(result["missing_items"]) == 0

    def test_verify_schema_integrity_missing_items(self):
        """Test schema verification with missing items."""
        mock_conn = Mock()
        mock_cursor = Mock()
        
        # Mock responses: first table exists, second doesn't, first index exists, second doesn't, etc.
        mock_cursor.fetchone.side_effect = [
            (True,), (False,), (True,), (True,),  # Tables: entities exists, events missing, relationships exists, evidence exists
            (True,), (False,), (True,), (True,), (True,), (True,), (True,), (True,)  # Indexes: first missing, rest exist
        ]
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        result = verify_schema_integrity(mock_conn)
        
        assert len(result["tables_verified"]) == 3
        assert len(result["indexes_verified"]) == 7
        assert len(result["missing_items"]) == 2
        assert "table: events" in result["missing_items"]
        assert "index: idx_events_event_type" in result["missing_items"]

    def test_verify_schema_integrity_error(self):
        """Test schema verification with database error."""
        mock_conn = Mock()
        mock_conn.cursor.side_effect = Exception("Database error")
        
        result = verify_schema_integrity(mock_conn)
        
        assert "error" in result
        assert "Verification failed" in result["error"]

    @patch('neon_sync.verify_schema_integrity')
    @patch('neon_sync.execute_schema')
    @patch('neon_sync.check_existing_tables')
    @patch('neon_sync.get_neon_connection')
    def test_main_success(self, mock_get_conn, mock_check_tables, 
                         mock_execute_schema, mock_verify):
        """Test successful main execution."""
        # Setup mocks
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn
        mock_check_tables.return_value = ['existing_table']
        mock_execute_schema.return_value = {"status": "success", "executed_statements": ["CREATE TABLE..."]}
        mock_verify.return_value = {
            "tables_verified": ["entities", "events"],
            "indexes_verified": ["idx_entities", "idx_events"],
            "missing_items": []
        }
        
        result = main()
        
        assert result is True
        mock_get_conn.assert_called_once()
        mock_check_tables.assert_called_once_with(mock_conn)
        mock_execute_schema.assert_called_once_with(mock_conn, "database_schema_improved.sql")
        mock_verify.assert_called_once_with(mock_conn)
        mock_conn.close.assert_called_once()

    @patch('neon_sync.get_neon_connection')
    def test_main_connection_error(self, mock_get_conn):
        """Test main execution with connection error."""
        mock_get_conn.side_effect = ConnectionError("Failed to connect")
        
        result = main()
        
        assert result is False

    @patch('neon_sync.execute_schema')
    @patch('neon_sync.check_existing_tables')
    @patch('neon_sync.get_neon_connection')
    def test_main_schema_error(self, mock_get_conn, mock_check_tables, mock_execute_schema):
        """Test main execution with schema execution error."""
        mock_conn = Mock()
        mock_get_conn.return_value = mock_conn
        mock_check_tables.return_value = []
        mock_execute_schema.return_value = {"error": "Schema execution failed"}
        
        result = main()
        
        assert result is False
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
