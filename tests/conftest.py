"""
Test configuration and fixtures for the analysis framework.
"""

import pytest
import tempfile
import os
import sqlite3
from datetime import datetime
from pathlib import Path

# Import the main modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from frameworks.hypergnn_core_enhanced import HyperGNNFramework
except ImportError:
    # Fallback for test environments
    HyperGNNFramework = None

try:
    from backend_api import app
except ImportError:
    # Flask app may not be available in all test environments
    app = None


@pytest.fixture(scope="session")
def test_database():
    """Create a temporary test database."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
        db_path = tmp_file.name
    
    # Initialize the database with schema
    conn = sqlite3.connect(db_path)
    
    # Create basic tables for testing
    conn.execute('''
        CREATE TABLE cases (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.execute('''
        CREATE TABLE entities (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            properties JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    ''')
    
    conn.execute('''
        CREATE TABLE evidence (
            id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            file_path TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (case_id) REFERENCES cases (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield db_path
    
    # Cleanup
    os.unlink(db_path)


@pytest.fixture
def test_case_data():
    """Sample case data for testing."""
    return {
        'id': 'test_case_001',
        'title': 'Test Investigation',
        'description': 'A test case for unit testing',
        'status': 'active'
    }


@pytest.fixture
def test_entity_data():
    """Sample entity data for testing."""
    return {
        'id': 'test_entity_001',
        'case_id': 'test_case_001',
        'name': 'Test Person',
        'type': 'person',
        'properties': {
            'age': 30,
            'occupation': 'Developer'
        }
    }


@pytest.fixture
def test_evidence_data():
    """Sample evidence data for testing."""
    return {
        'id': 'test_evidence_001',
        'case_id': 'test_case_001',
        'name': 'Test Document',
        'type': 'document',
        'file_path': '/tmp/test_document.pdf',
        'status': 'pending'
    }


@pytest.fixture
def hypergnn_framework(test_database):
    """Initialize HyperGNN framework for testing."""
    if HyperGNNFramework is None:
        pytest.skip("HyperGNN framework not available")
    framework = HyperGNNFramework()
    framework.db_path = test_database
    return framework


@pytest.fixture
def flask_app():
    """Create Flask app for testing."""
    if app is None:
        pytest.skip("Flask app not available")
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(flask_app):
    """Create Flask test client."""
    return flask_app.test_client()


@pytest.fixture
def temp_directory():
    """Create a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def sample_image_file(temp_directory):
    """Create a sample image file for OCR testing."""
    from PIL import Image
    
    # Create a simple test image
    img = Image.new('RGB', (100, 50), color='white')
    file_path = os.path.join(temp_directory, 'test_image.png')
    img.save(file_path)
    
    return file_path


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response for testing."""
    return {
        'choices': [
            {
                'message': {
                    'content': 'This is a mock response from OpenAI API.'
                }
            }
        ]
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ['TESTING'] = 'true'
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    yield
    # Cleanup
    if 'TESTING' in os.environ:
        del os.environ['TESTING']
    if 'DATABASE_URL' in os.environ:
        del os.environ['DATABASE_URL']


@pytest.fixture
def sample_timeline_data():
    """Sample timeline data for testing."""
    return [
        {
            'date': '2025-01-01',
            'event': 'Initial contact',
            'description': 'First communication between parties',
            'entities': ['person_001', 'person_002']
        },
        {
            'date': '2025-01-05',
            'event': 'Meeting',
            'description': 'In-person meeting at location',
            'entities': ['person_001', 'person_002', 'location_001']
        }
    ]


@pytest.fixture
def sample_hypergraph_data():
    """Sample hypergraph data for testing."""
    return {
        'nodes': [
            {'id': 'node_001', 'type': 'person', 'data': {'name': 'John Doe'}},
            {'id': 'node_002', 'type': 'person', 'data': {'name': 'Jane Smith'}},
            {'id': 'node_003', 'type': 'location', 'data': {'name': 'Office Building'}}
        ],
        'edges': [
            {
                'id': 'edge_001',
                'type': 'communication',
                'nodes': ['node_001', 'node_002'],
                'weight': 0.8
            },
            {
                'id': 'edge_002',
                'type': 'meeting',
                'nodes': ['node_001', 'node_002', 'node_003'],
                'weight': 0.9
            }
        ]
    }


class MockDatabase:
    """Mock database for testing without actual database connections."""
    
    def __init__(self):
        self.data = {
            'cases': {},
            'entities': {},
            'evidence': {},
            'relationships': {}
        }
    
    def insert(self, table, data):
        """Insert data into mock table."""
        if table not in self.data:
            self.data[table] = {}
        self.data[table][data['id']] = data
        return data['id']
    
    def select(self, table, filters=None):
        """Select data from mock table."""
        if table not in self.data:
            return []
        
        results = list(self.data[table].values())
        
        if filters:
            for key, value in filters.items():
                results = [r for r in results if r.get(key) == value]
        
        return results
    
    def update(self, table, id, data):
        """Update data in mock table."""
        if table in self.data and id in self.data[table]:
            self.data[table][id].update(data)
            return True
        return False
    
    def delete(self, table, id):
        """Delete data from mock table."""
        if table in self.data and id in self.data[table]:
            del self.data[table][id]
            return True
        return False


@pytest.fixture
def mock_database():
    """Provide a mock database for testing."""
    return MockDatabase()


# Performance testing fixtures
@pytest.fixture
def performance_test_data():
    """Generate large dataset for performance testing."""
    import random
    import string
    
    def random_string(length=10):
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    cases = []
    entities = []
    
    # Generate test cases
    for i in range(100):
        case_id = f"perf_case_{i:03d}"
        cases.append({
            'id': case_id,
            'title': f"Performance Test Case {i}",
            'description': random_string(100),
            'status': random.choice(['active', 'completed', 'pending'])
        })
        
        # Generate entities for each case
        for j in range(random.randint(5, 20)):
            entities.append({
                'id': f"perf_entity_{i:03d}_{j:03d}",
                'case_id': case_id,
                'name': random_string(15),
                'type': random.choice(['person', 'organization', 'location']),
                'properties': {
                    'random_field': random_string(20)
                }
            })
    
    return {'cases': cases, 'entities': entities}


# Markers for different test types
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "api: marks tests as API tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )
