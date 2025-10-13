# Testing Guide

This document provides instructions for running tests and validating the analysis framework codebase.

## Prerequisites

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

Or install testing tools individually:

```bash
pip install pytest pytest-cov black flake8 isort
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Verbosity

```bash
pytest tests/ -v
```

### Run Specific Test Categories

**Unit Tests Only:**
```bash
pytest tests/unit/ -v
```

**Integration Tests Only:**
```bash
pytest tests/integration/ -v
```

**Run Tests by Marker:**
```bash
# Run only fast tests (exclude slow ones)
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m integration
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

This generates a coverage report in `htmlcov/index.html` and displays a summary in the terminal.

### Run Specific Test Files

```bash
pytest tests/unit/test_citizenship_settlement_analyzer.py -v
```

### Run Specific Test Functions

```bash
pytest tests/unit/test_citizenship_settlement_analyzer.py::TestCitizenshipProfile::test_citizenship_profile_creation -v
```

## Code Quality Checks

### Linting with Flake8

Check for syntax errors and common issues:

```bash
# Check for critical errors only
flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Full linting check
flake8 src/ --count --statistics
```

### Code Formatting with Black

Check if code follows formatting standards:

```bash
black --check src/
```

Auto-format code:

```bash
black src/
```

### Import Sorting with isort

Check import order:

```bash
isort --check-only src/
```

Auto-fix imports:

```bash
isort src/
```

## Using the Validation Script

A helper script is provided to run all quality checks at once:

```bash
python3 scripts/validate_codebase.py
```

This script runs:
1. Linting checks (flake8)
2. Code formatting checks (black)
3. Import order checks (isort)
4. Unit tests
5. Integration tests (optional)

## Test Configuration

Test configuration is defined in:
- `pytest.ini` - Main pytest configuration
- `tests/conftest.py` - Shared fixtures and test setup
- `pyproject.toml` - Tool configurations for black, isort, flake8

## Common Test Patterns

### Using Fixtures

```python
def test_example(test_database, test_case_data):
    """Test using shared fixtures."""
    # test_database and test_case_data are automatically provided
    assert test_case_data['id'] == 'test_case_001'
```

### Mocking Dependencies

```python
from unittest.mock import Mock, patch

@patch('module.external_dependency')
def test_with_mock(mock_dependency):
    """Test with mocked external dependency."""
    mock_dependency.return_value = "mocked value"
    # Your test code here
```

### Skipping Tests

```python
import pytest

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(condition, reason="Requires specific environment")
def test_conditional():
    pass
```

## Troubleshooting

### Import Errors

If you encounter import errors when running tests:

1. Ensure you're running from the repository root
2. Check that the package is installed: `pip install -e .`
3. Verify PYTHONPATH includes the src directory

### Missing Dependencies

If tests fail due to missing dependencies:

```bash
pip install -e ".[dev,database,fraud-analysis]"
```

### Database Issues

Tests use temporary databases that are cleaned up automatically. If you encounter database lock issues:

1. Stop any running processes using the test database
2. Delete any `.db` files in the `tests/` directory
3. Re-run the tests

## Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branches
- Pre-commit hooks (if configured)

See `.pre-commit-config.yaml` and `.github/workflows/` for CI configuration.

## Writing New Tests

When adding new tests:

1. Place unit tests in `tests/unit/`
2. Place integration tests in `tests/integration/`
3. Use descriptive test names: `test_<feature>_<scenario>_<expected_result>`
4. Add docstrings explaining what the test validates
5. Use fixtures from `conftest.py` when possible
6. Mark slow tests with `@pytest.mark.slow`

Example:

```python
import pytest

def test_analysis_framework_initialization(test_database):
    """Test that the analysis framework initializes correctly with valid config."""
    from src.models.hypergnn_framework_improved import HyperGNNFramework
    from src.models.hypergnn_framework_improved import AnalysisConfiguration
    
    config = AnalysisConfiguration(case_id="test_case")
    framework = HyperGNNFramework(config)
    
    assert framework.config.case_id == "test_case"
    assert framework.component_factory is not None
```

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- Project README: [README.md](README.md)
- Technical Architecture: [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)
