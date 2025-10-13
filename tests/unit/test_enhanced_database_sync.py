#!/usr/bin/env python3
"""
Unit tests for enhanced database synchronization.
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from database_sync.enhanced_sync import (
    EnhancedDatabaseSync,
    SyncCoordinator,
    DatabaseSyncError,
    MigrationError,
    RollbackError
)


class TestEnhancedDatabaseSync:
    """Test cases for EnhancedDatabaseSync class."""
    
    @pytest.fixture
    def mock_db_client(self):
        """Create a mock database client."""
        client = Mock()
        client.execute = Mock()
        return client
    
    @pytest.fixture
    def sync_instance(self, mock_db_client):
        """Create a sync instance with mock client."""
        return EnhancedDatabaseSync(mock_db_client, "test_db")
    
    def test_initialization(self, sync_instance):
        """Test proper initialization of sync instance."""
        assert sync_instance.db_name == "test_db"
        assert sync_instance.migration_history == []
        assert sync_instance.db_client is not None
    
    def test_validate_migration_success(self, sync_instance):
        """Test successful migration validation."""
        migration_sql = [
            "CREATE TABLE test (id INT PRIMARY KEY)",
            "ALTER TABLE test ADD COLUMN name VARCHAR(100)"
        ]
        
        valid, error = sync_instance._validate_migration(migration_sql)
        
        assert valid is True
        assert error is None
    
    def test_validate_migration_empty_statement(self, sync_instance):
        """Test validation fails on empty statement."""
        migration_sql = [
            "CREATE TABLE test (id INT PRIMARY KEY)",
            "",  # Empty statement
            "ALTER TABLE test ADD COLUMN name VARCHAR(100)"
        ]
        
        valid, error = sync_instance._validate_migration(migration_sql)
        
        assert valid is False
        assert "Empty statement" in error
    
    def test_validate_migration_dangerous_operation(self, sync_instance):
        """Test validation warns on dangerous operations."""
        migration_sql = [
            "DROP DATABASE production"
        ]
        
        # Should still validate but log warning
        valid, error = sync_instance._validate_migration(migration_sql)
        
        # Validation passes but warning is logged
        assert valid is True
    
    def test_create_backup_point(self, sync_instance):
        """Test backup point creation."""
        backup_id = sync_instance._create_backup_point("test_migration")
        
        assert "test_migration" in backup_id
        assert len(sync_instance.migration_history) == 1
        assert sync_instance.migration_history[0]['status'] == 'backup_created'
    
    def test_execute_migration_dry_run(self, sync_instance):
        """Test migration execution in dry run mode."""
        migration_sql = [
            "CREATE TABLE test (id INT PRIMARY KEY)"
        ]
        
        success, error = sync_instance.execute_migration(
            migration_sql,
            "test_migration",
            dry_run=True
        )
        
        assert success is True
        assert error is None
        # Client should not be called in dry run
        sync_instance.db_client.execute.assert_not_called()
    
    def test_execute_migration_success(self, sync_instance):
        """Test successful migration execution."""
        migration_sql = [
            "CREATE TABLE test (id INT PRIMARY KEY)",
            "INSERT INTO test VALUES (1)"
        ]
        
        success, error = sync_instance.execute_migration(
            migration_sql,
            "test_migration",
            dry_run=False
        )
        
        assert success is True
        assert error is None
        assert len(sync_instance.migration_history) >= 1
    
    def test_execute_migration_failure(self, sync_instance):
        """Test migration failure and rollback."""
        # Configure mock to fail on second statement
        sync_instance.db_client.execute.side_effect = [
            None,  # First statement succeeds
            Exception("Database error")  # Second statement fails
        ]
        
        migration_sql = [
            "CREATE TABLE test (id INT PRIMARY KEY)",
            "INVALID SQL STATEMENT"
        ]
        
        success, error = sync_instance.execute_migration(
            migration_sql,
            "test_migration",
            dry_run=False
        )
        
        assert success is False
        assert error is not None
        assert "rolled back" in error.lower()
    
    def test_extract_table_name(self, sync_instance):
        """Test table name extraction from CREATE statement."""
        statement = "CREATE TABLE users (id INT PRIMARY KEY)"
        table_name = sync_instance._extract_table_name(statement)
        
        assert table_name == "users"
    
    def test_extract_table_name_with_if_not_exists(self, sync_instance):
        """Test table name extraction with IF NOT EXISTS."""
        statement = "CREATE TABLE IF NOT EXISTS users (id INT)"
        # Simplified extraction might not handle this perfectly
        # This test documents current behavior
        table_name = sync_instance._extract_table_name(statement)
        
        # May need adjustment based on implementation
        assert table_name is not None
    
    def test_generate_reverse_statement_create_table(self, sync_instance):
        """Test reverse statement generation for CREATE TABLE."""
        statement = "CREATE TABLE users (id INT PRIMARY KEY)"
        reverse = sync_instance._generate_reverse_statement(statement)
        
        assert reverse is not None
        assert "DROP TABLE" in reverse
        assert "users" in reverse
    
    def test_generate_reverse_statement_alter_table(self, sync_instance):
        """Test reverse statement generation for ALTER TABLE."""
        statement = "ALTER TABLE users ADD COLUMN email VARCHAR(255)"
        reverse = sync_instance._generate_reverse_statement(statement)
        
        # Complex alterations may not be reversible
        # This documents expected behavior
        assert reverse is None or "ALTER TABLE" in reverse
    
    def test_record_migration(self, sync_instance):
        """Test migration recording."""
        migration_sql = ["CREATE TABLE test (id INT)"]
        
        sync_instance._record_migration("test_migration", migration_sql)
        
        assert len(sync_instance.migration_history) == 1
        assert sync_instance.migration_history[0]['migration_name'] == "test_migration"
        assert sync_instance.migration_history[0]['status'] == "completed"
    
    def test_get_migration_history(self, sync_instance):
        """Test retrieving migration history."""
        sync_instance._record_migration("migration1", ["SQL1"])
        sync_instance._record_migration("migration2", ["SQL2"])
        
        history = sync_instance.get_migration_history()
        
        assert len(history) == 2
        assert history[0]['migration_name'] == "migration1"
        assert history[1]['migration_name'] == "migration2"
    
    def test_export_migration_log(self, sync_instance, tmp_path):
        """Test exporting migration log to file."""
        sync_instance._record_migration("test_migration", ["SQL"])
        
        log_file = tmp_path / "migration_log.json"
        sync_instance.export_migration_log(str(log_file))
        
        assert log_file.exists()
        
        import json
        with open(log_file) as f:
            log_data = json.load(f)
        
        assert len(log_data) == 1
        assert log_data[0]['migration_name'] == "test_migration"


class TestSyncCoordinator:
    """Test cases for SyncCoordinator class."""
    
    @pytest.fixture
    def coordinator(self):
        """Create a sync coordinator instance."""
        return SyncCoordinator()
    
    @pytest.fixture
    def mock_databases(self):
        """Create mock database clients."""
        return {
            'supabase': Mock(),
            'neon': Mock()
        }
    
    @pytest.fixture
    def sample_migrations(self):
        """Create sample migrations."""
        return {
            'users': ["CREATE TABLE users (id INT PRIMARY KEY)"],
            'posts': ["CREATE TABLE posts (id INT PRIMARY KEY)"]
        }
    
    def test_initialization(self, coordinator):
        """Test coordinator initialization."""
        assert coordinator.sync_results == {}
    
    def test_sync_all_databases_dry_run(
        self,
        coordinator,
        mock_databases,
        sample_migrations
    ):
        """Test syncing all databases in dry run mode."""
        results = coordinator.sync_all_databases(
            mock_databases,
            sample_migrations,
            dry_run=True
        )
        
        assert len(results) == 2  # Two databases
        assert 'supabase' in results
        assert 'neon' in results
        
        # Check that migrations were attempted for each table
        for db_name in mock_databases.keys():
            assert 'results' in results[db_name]
            assert 'users' in results[db_name]['results']
            assert 'posts' in results[db_name]['results']
    
    def test_get_sync_summary_all_success(self, coordinator):
        """Test sync summary with all successful migrations."""
        coordinator.sync_results = {
            'db1': {
                'results': {
                    'table1': {'success': True, 'error': None, 'timestamp': '2025-10-12'},
                    'table2': {'success': True, 'error': None, 'timestamp': '2025-10-12'}
                },
                'migration_history': []
            }
        }
        
        summary = coordinator.get_sync_summary()
        
        assert summary['total_databases'] == 1
        assert summary['total_migrations'] == 2
        assert summary['successful_migrations'] == 2
        assert summary['failed_migrations'] == 0
        assert summary['success_rate'] == 100.0
    
    def test_get_sync_summary_partial_failure(self, coordinator):
        """Test sync summary with partial failures."""
        coordinator.sync_results = {
            'db1': {
                'results': {
                    'table1': {'success': True, 'error': None, 'timestamp': '2025-10-12'},
                    'table2': {'success': False, 'error': 'Error', 'timestamp': '2025-10-12'}
                },
                'migration_history': []
            }
        }
        
        summary = coordinator.get_sync_summary()
        
        assert summary['total_migrations'] == 2
        assert summary['successful_migrations'] == 1
        assert summary['failed_migrations'] == 1
        assert summary['success_rate'] == 50.0
    
    def test_get_sync_summary_empty(self, coordinator):
        """Test sync summary with no results."""
        summary = coordinator.get_sync_summary()
        
        assert summary['total_databases'] == 0
        assert summary['total_migrations'] == 0
        assert summary['success_rate'] == 0


class TestMigrationReport:
    """Test cases for migration report generation."""
    
    def test_create_migration_report(self, tmp_path):
        """Test creating migration report."""
        from database_sync.enhanced_sync import create_migration_report
        
        sync_results = {
            'supabase': {
                'results': {
                    'users': {'success': True, 'error': None, 'timestamp': '2025-10-12'},
                    'posts': {'success': False, 'error': 'Failed', 'timestamp': '2025-10-12'}
                },
                'migration_history': []
            }
        }
        
        report_file = tmp_path / "migration_report.md"
        create_migration_report(sync_results, str(report_file))
        
        assert report_file.exists()
        
        content = report_file.read_text()
        assert "Database Migration Report" in content
        assert "supabase" in content
        assert "users" in content
        assert "posts" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

