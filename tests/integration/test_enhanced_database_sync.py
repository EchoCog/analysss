#!/usr/bin/env python3
"""
Integration Tests for Enhanced Database Synchronization
=======================================================

This module contains comprehensive integration tests for the enhanced
Supabase and Neon synchronization scripts.

Tests cover:
- Connection establishment and validation
- Schema creation and validation
- Migration management
- Error handling and recovery
- Performance and reliability
"""

import unittest
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from supabase_sync_enhanced import EnhancedSupabaseSync, SyncResult
from neon_sync_enhanced import EnhancedNeonSync, NeonSyncResult


class TestEnhancedSupabaseSync(unittest.TestCase):
    """Test cases for Enhanced Supabase Synchronization"""

    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test_key_123'
        })
        self.env_patcher.start()
        
        self.sync_manager = EnhancedSupabaseSync(max_retries=1, retry_delay=0.1)

    def tearDown(self):
        """Clean up test environment"""
        self.env_patcher.stop()

    def test_initialization_with_valid_env(self):
        """Test successful initialization with valid environment variables"""
        self.assertEqual(self.sync_manager.supabase_url, 'https://test.supabase.co')
        self.assertEqual(self.sync_manager.supabase_key, 'test_key_123')
        self.assertEqual(self.sync_manager.max_retries, 1)
        self.assertEqual(self.sync_manager.retry_delay, 0.1)

    def test_initialization_without_env_variables(self):
        """Test initialization failure without required environment variables"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                EnhancedSupabaseSync()
            
            self.assertIn("SUPABASE_URL and SUPABASE_KEY", str(context.exception))

    @patch('supabase_sync_enhanced.create_client')
    def test_get_supabase_client_success(self, mock_create_client):
        """Test successful Supabase client creation"""
        mock_client = Mock()
        mock_table = Mock()
        mock_table.select.return_value.limit.return_value.execute.return_value = {}
        mock_client.table.return_value = mock_table
        mock_create_client.return_value = mock_client
        
        client = self.sync_manager.get_supabase_client()
        
        self.assertIsNotNone(client)
        mock_create_client.assert_called_once_with(
            'https://test.supabase.co', 
            'test_key_123'
        )

    @patch('supabase_sync_enhanced.create_client')
    def test_get_supabase_client_connection_error(self, mock_create_client):
        """Test Supabase client creation with connection error"""
        mock_create_client.side_effect = Exception("Connection failed")
        
        with self.assertRaises(ConnectionError) as context:
            self.sync_manager.get_supabase_client()
        
        self.assertIn("Unable to connect to Supabase", str(context.exception))

    @patch('supabase_sync_enhanced.create_engine')
    def test_get_sqlalchemy_engine_success(self, mock_create_engine):
        """Test successful SQLAlchemy engine creation"""
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_engine.connect.return_value.__exit__.return_value = None
        mock_create_engine.return_value = mock_engine
        
        engine = self.sync_manager.get_sqlalchemy_engine()
        
        self.assertIsNotNone(engine)
        mock_create_engine.assert_called_once()

    def test_retry_operation_success_on_first_attempt(self):
        """Test retry operation succeeding on first attempt"""
        mock_func = Mock(return_value="success")
        
        result = self.sync_manager.retry_operation(mock_func, "arg1", kwarg1="value1")
        
        self.assertEqual(result, "success")
        mock_func.assert_called_once_with("arg1", kwarg1="value1")

    def test_retry_operation_success_after_retry(self):
        """Test retry operation succeeding after initial failure"""
        mock_func = Mock(side_effect=[Exception("First failure"), "success"])
        
        result = self.sync_manager.retry_operation(mock_func)
        
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 2)

    def test_retry_operation_final_failure(self):
        """Test retry operation failing after all attempts"""
        mock_func = Mock(side_effect=Exception("Persistent failure"))
        
        with self.assertRaises(Exception) as context:
            self.sync_manager.retry_operation(mock_func)
        
        self.assertEqual(str(context.exception), "Persistent failure")
        self.assertEqual(mock_func.call_count, 2)  # max_retries + 1

    @patch('supabase_sync_enhanced.Config')
    @patch('os.path.exists')
    def test_setup_alembic_environment_success(self, mock_exists, mock_config):
        """Test successful Alembic environment setup"""
        mock_exists.return_value = True
        mock_alembic_cfg = Mock()
        mock_config.return_value = mock_alembic_cfg
        
        with patch.object(self.sync_manager, 'get_sqlalchemy_engine') as mock_get_engine:
            mock_engine = Mock()
            mock_engine.url = "postgresql://test"
            mock_get_engine.return_value = mock_engine
            
            config = self.sync_manager.setup_alembic_environment()
            
            self.assertIsNotNone(config)
            mock_alembic_cfg.set_main_option.assert_called_once_with(
                'sqlalchemy.url', 
                'postgresql://test'
            )

    @patch('os.path.exists')
    def test_setup_alembic_environment_missing_config(self, mock_exists):
        """Test Alembic environment setup with missing config file"""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError) as context:
            self.sync_manager.setup_alembic_environment()
        
        self.assertIn("alembic.ini not found", str(context.exception))

    def test_sync_result_dataclass(self):
        """Test SyncResult dataclass functionality"""
        result = SyncResult(
            success=True,
            message="Test message",
            details={"key": "value"},
            errors=[],
            execution_time=1.5
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Test message")
        self.assertEqual(result.details["key"], "value")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.execution_time, 1.5)


class TestEnhancedNeonSync(unittest.TestCase):
    """Test cases for Enhanced Neon Synchronization"""

    def setUp(self):
        """Set up test environment"""
        self.sync_manager = EnhancedNeonSync(max_retries=1, retry_delay=0.1)

    def test_initialization(self):
        """Test successful initialization"""
        self.assertEqual(self.sync_manager.max_retries, 1)
        self.assertEqual(self.sync_manager.retry_delay, 0.1)
        self.assertEqual(self.sync_manager.server_name, "neon")

    @patch('subprocess.run')
    def test_execute_mcp_command_success(self, mock_run):
        """Test successful MCP command execution"""
        mock_result = Mock()
        mock_result.stdout = '{"status": "success", "data": "test"}'
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.sync_manager.execute_mcp_command("test_command", {"param": "value"})
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"], "test")
        
        expected_args = [
            "manus-mcp-cli", "tool", "call", "test_command", 
            "--server", "neon", "--input", '{"param": "value"}'
        ]
        mock_run.assert_called_once_with(
            expected_args,
            capture_output=True,
            text=True,
            check=True,
            timeout=60
        )

    @patch('subprocess.run')
    def test_execute_mcp_command_failure(self, mock_run):
        """Test MCP command execution failure"""
        from subprocess import CalledProcessError
        mock_run.side_effect = CalledProcessError(1, "cmd", stderr="Command failed")
        
        with self.assertRaises(CalledProcessError):
            self.sync_manager.execute_mcp_command("test_command")

    @patch('subprocess.run')
    def test_execute_mcp_command_invalid_json(self, mock_run):
        """Test MCP command execution with invalid JSON response"""
        mock_result = Mock()
        mock_result.stdout = 'invalid json'
        mock_run.return_value = mock_result
        
        with self.assertRaises(json.JSONDecodeError):
            self.sync_manager.execute_mcp_command("test_command")

    @patch.object(EnhancedNeonSync, 'execute_mcp_command')
    def test_list_projects_success(self, mock_execute):
        """Test successful project listing"""
        mock_execute.return_value = {
            "projects": [
                {"id": "proj1", "name": "Project 1"},
                {"id": "proj2", "name": "Project 2"}
            ]
        }
        
        result = self.sync_manager.list_projects()
        
        self.assertTrue(result.success)
        self.assertEqual(result.details["project_count"], 2)
        self.assertIn("Successfully retrieved project list", result.message)

    @patch.object(EnhancedNeonSync, 'execute_mcp_command')
    def test_list_projects_failure(self, mock_execute):
        """Test project listing failure"""
        mock_execute.side_effect = Exception("API Error")
        
        result = self.sync_manager.list_projects()
        
        self.assertFalse(result.success)
        self.assertIn("Failed to retrieve project list", result.message)
        self.assertIn("API Error", result.errors[0])

    @patch.object(EnhancedNeonSync, 'execute_mcp_command')
    def test_create_project_success(self, mock_execute):
        """Test successful project creation"""
        mock_execute.return_value = {
            "project": {
                "id": "new_proj_123",
                "name": "Test Project"
            }
        }
        
        result = self.sync_manager.create_project("Test Project", "us-west-2")
        
        self.assertTrue(result.success)
        self.assertEqual(result.details["project_name"], "Test Project")
        self.assertEqual(result.details["region"], "us-west-2")
        self.assertEqual(result.details["project_id"], "new_proj_123")

    @patch.object(EnhancedNeonSync, 'execute_mcp_command')
    def test_execute_sql_query_success(self, mock_execute):
        """Test successful SQL query execution"""
        mock_execute.return_value = {
            "rows_affected": 5,
            "rows": [["col1", "col2"], ["val1", "val2"]]
        }
        
        result = self.sync_manager.execute_sql_query(
            "proj123", 
            "testdb", 
            "SELECT * FROM test_table"
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.details["rows_affected"], 5)
        self.assertEqual(result.details["project_id"], "proj123")
        self.assertEqual(result.details["database"], "testdb")

    def test_neon_sync_result_dataclass(self):
        """Test NeonSyncResult dataclass functionality"""
        result = NeonSyncResult(
            success=True,
            message="Test message",
            details={"key": "value"},
            errors=[],
            execution_time=2.0,
            neon_response={"data": "test"}
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Test message")
        self.assertEqual(result.details["key"], "value")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(result.execution_time, 2.0)
        self.assertEqual(result.neon_response["data"], "test")


class TestDatabaseSyncIntegration(unittest.TestCase):
    """Integration tests for database synchronization workflows"""

    def setUp(self):
        """Set up integration test environment"""
        # Mock environment variables for Supabase
        self.env_patcher = patch.dict(os.environ, {
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_KEY': 'test_key_123'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up integration test environment"""
        self.env_patcher.stop()

    @patch('supabase_sync_enhanced.create_client')
    @patch('supabase_sync_enhanced.create_engine')
    def test_supabase_sync_workflow(self, mock_create_engine, mock_create_client):
        """Test complete Supabase synchronization workflow"""
        # Mock Supabase client
        mock_client = Mock()
        mock_table = Mock()
        mock_table.select.return_value.limit.return_value.execute.return_value = {}
        mock_client.table.return_value = mock_table
        mock_create_client.return_value = mock_client
        
        # Mock SQLAlchemy engine
        mock_engine = Mock()
        mock_connection = Mock()
        mock_engine.connect.return_value.__enter__.return_value = mock_connection
        mock_engine.connect.return_value.__exit__.return_value = None
        mock_create_engine.return_value = mock_engine
        
        sync_manager = EnhancedSupabaseSync(max_retries=1, retry_delay=0.1)
        
        # Test client creation
        client = sync_manager.get_supabase_client()
        self.assertIsNotNone(client)
        
        # Test engine creation
        engine = sync_manager.get_sqlalchemy_engine()
        self.assertIsNotNone(engine)

    @patch.object(EnhancedNeonSync, 'execute_mcp_command')
    def test_neon_sync_workflow(self, mock_execute):
        """Test complete Neon synchronization workflow"""
        # Mock different MCP responses for different commands
        def mock_execute_side_effect(command, input_data=None):
            if command == "list_projects":
                return {
                    "projects": [
                        {"id": "test_proj_123", "name": "Test Project"}
                    ]
                }
            elif command == "execute_query":
                return {
                    "rows_affected": 1,
                    "rows": [["table_name"], ["agents"], ["events"]]
                }
            else:
                return {"status": "success"}
        
        mock_execute.side_effect = mock_execute_side_effect
        
        sync_manager = EnhancedNeonSync(max_retries=1, retry_delay=0.1)
        
        # Test project listing
        projects_result = sync_manager.list_projects()
        self.assertTrue(projects_result.success)
        
        # Test SQL execution
        sql_result = sync_manager.execute_sql_query(
            "test_proj_123", 
            "postgres", 
            "SELECT table_name FROM information_schema.tables"
        )
        self.assertTrue(sql_result.success)

    def test_error_handling_consistency(self):
        """Test that both sync managers handle errors consistently"""
        # Test Supabase error handling
        supabase_sync = EnhancedSupabaseSync(max_retries=1, retry_delay=0.1)
        
        # Test Neon error handling
        neon_sync = EnhancedNeonSync(max_retries=1, retry_delay=0.1)
        
        # Both should have similar retry mechanisms
        self.assertEqual(supabase_sync.max_retries, neon_sync.max_retries)
        self.assertEqual(supabase_sync.retry_delay, neon_sync.retry_delay)


if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestEnhancedSupabaseSync))
    suite.addTest(unittest.makeSuite(TestEnhancedNeonSync))
    suite.addTest(unittest.makeSuite(TestDatabaseSyncIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
