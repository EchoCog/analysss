#!/usr/bin/env python3
"""
Improved Tests for Supabase Synchronization
===========================================

Comprehensive test suite for the enhanced supabase_sync.py functionality.
"""

import os
import pytest
from unittest.mock import Mock, patch, mock_open
from supabase_sync import (
    get_supabase_client,
    check_existing_tables,
    create_tables_if_not_exist,
    sync_data_structure,
    main
)


class TestSupabaseSync:
    """Test suite for Supabase synchronization functionality."""

    def test_get_supabase_client_success(self):
        """Test successful Supabase client creation."""
        with patch.dict(os.environ, {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test-key'
        }):
            with patch('supabase_sync.create_client') as mock_create:
                mock_client = Mock()
                mock_create.return_value = mock_client
                
                client = get_supabase_client()
                
                assert client == mock_client
                mock_create.assert_called_once_with(
                    'https://test.supabase.co', 
                    'test-key'
                )

    def test_get_supabase_client_missing_env_vars(self):
        """Test Supabase client creation with missing environment variables."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="SUPABASE_URL and SUPABASE_KEY"):
                get_supabase_client()

    def test_check_existing_tables_success(self):
        """Test successful table checking."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            {'table_name': 'entities'},
            {'table_name': 'events'}
        ]
        mock_client.rpc.return_value.execute.return_value = mock_response
        
        tables = check_existing_tables(mock_client)
        
        assert tables == ['entities', 'events']
        mock_client.rpc.assert_called_once_with("get_table_names")

    def test_check_existing_tables_error(self):
        """Test table checking with error."""
        mock_client = Mock()
        mock_client.rpc.side_effect = Exception("Connection error")
        
        tables = check_existing_tables(mock_client)
        
        assert tables == []

    def test_create_tables_schema_file_not_found(self):
        """Test schema creation when schema file doesn't exist."""
        mock_client = Mock()
        
        with patch('os.path.exists', return_value=False):
            result = create_tables_if_not_exist(mock_client)
            
            assert "error" in result
            assert "Schema file" in result["error"]

    def test_create_tables_success(self):
        """Test successful schema creation."""
        mock_client = Mock()
        mock_response = Mock()
        mock_client.rpc.return_value.execute.return_value = mock_response
        
        schema_content = """
        CREATE TABLE entities (id TEXT PRIMARY KEY);
        CREATE INDEX idx_entities ON entities(id);
        -- This is a comment
        """
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=schema_content)):
                result = create_tables_if_not_exist(mock_client)
                
                assert result["status"] == "success"
                assert "executed_statements" in result
                # Should execute 2 statements (CREATE TABLE and CREATE INDEX)
                assert len(result["executed_statements"]) == 2

    def test_create_tables_with_statement_errors(self):
        """Test schema creation with some statement errors."""
        mock_client = Mock()
        
        # First statement succeeds, second fails
        mock_client.rpc.side_effect = [
            Mock(execute=Mock(return_value=Mock())),  # Success
            Exception("Table already exists")         # Error
        ]
        
        schema_content = """
        CREATE TABLE entities (id TEXT PRIMARY KEY);
        CREATE TABLE events (id TEXT PRIMARY KEY);
        """
        
        with patch('os.path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=schema_content)):
                result = create_tables_if_not_exist(mock_client)
                
                assert result["status"] == "success"
                # Should have 1 successful execution
                assert len(result["executed_statements"]) == 1

    def test_sync_data_structure(self):
        """Test data structure synchronization."""
        mock_client = Mock()
        
        result = sync_data_structure(mock_client)
        
        assert result["sync_status"] == "completed"
        assert "tables_checked" in result
        assert "indexes_created" in result
        assert len(result["tables_checked"]) == 4  # entities, events, relationships, evidence
        assert len(result["indexes_created"]) == 8  # All expected indexes

    @patch('supabase_sync.sync_data_structure')
    @patch('supabase_sync.create_tables_if_not_exist')
    @patch('supabase_sync.check_existing_tables')
    @patch('supabase_sync.get_supabase_client')
    def test_main_success(self, mock_get_client, mock_check_tables, 
                         mock_create_tables, mock_sync_data):
        """Test successful main execution."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_check_tables.return_value = ['existing_table']
        mock_create_tables.return_value = {"status": "success", "executed_statements": []}
        mock_sync_data.return_value = {"sync_status": "completed", "tables_checked": [], "indexes_created": []}
        
        result = main()
        
        assert result is True
        mock_get_client.assert_called_once()
        mock_check_tables.assert_called_once_with(mock_client)
        mock_create_tables.assert_called_once_with(mock_client)
        mock_sync_data.assert_called_once_with(mock_client)

    @patch('supabase_sync.get_supabase_client')
    def test_main_client_error(self, mock_get_client):
        """Test main execution with client initialization error."""
        mock_get_client.side_effect = ValueError("Missing credentials")
        
        result = main()
        
        assert result is False

    @patch('supabase_sync.create_tables_if_not_exist')
    @patch('supabase_sync.check_existing_tables')
    @patch('supabase_sync.get_supabase_client')
    def test_main_schema_error(self, mock_get_client, mock_check_tables, mock_create_tables):
        """Test main execution with schema creation error."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_check_tables.return_value = []
        mock_create_tables.return_value = {"error": "Schema creation failed"}
        
        result = main()
        
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
