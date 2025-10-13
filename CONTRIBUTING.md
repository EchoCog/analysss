# Contributing to Analysis Repository

Thank you for your interest in contributing to the Analysis Repository! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Database Changes](#database-changes)

## Code of Conduct

This project adheres to professional standards of conduct. We expect all contributors to:

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize the project's goals and user needs
- Maintain confidentiality of sensitive case information

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of criminal case analysis workflows
- Familiarity with PostgreSQL (for database contributions)

### First-Time Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/analysis.git
   cd analysis
   ```

3. **Run the setup script**:
   ```bash
   ./scripts/setup_environment.sh
   ```

4. **Configure environment**:
   - Copy `.env.example` to `.env`
   - Add your database credentials (optional for most contributions)

5. **Verify installation**:
   ```bash
   source venv/bin/activate
   pytest tests/
   ```

## Development Setup

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev,database,fraud-analysis]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

### IDE Configuration

**VS Code**: Install Python extension and use the provided `.vscode/settings.json` (if available)

**PyCharm**: Configure Python interpreter to use `venv/bin/python`

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or improvements

### 2. Make Your Changes

- Write clear, self-documenting code
- Add docstrings to all functions and classes
- Update relevant documentation
- Add tests for new functionality

### 3. Run Quality Checks

```bash
# Format code
black src/ tests/

# Check code style
flake8 src/ tests/

# Sort imports
isort src/ tests/

# Run tests
pytest tests/ -v --cov=src

# Type checking (optional)
mypy src/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new timeline processing feature"
```

**Commit message format**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Test additions or changes
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Coding Standards

### Python Style Guide

We follow **PEP 8** with some modifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Organized with `isort`
- **Docstrings**: Google style
- **Type hints**: Encouraged for public APIs

### Example Code Style

```python
"""Module for processing timeline events."""

from datetime import datetime
from typing import List, Optional, Dict, Any


class TimelineProcessor:
    """
    Processes and validates timeline events for case analysis.
    
    Attributes:
        events: List of timeline events
        validation_rules: Dictionary of validation rules
    """
    
    def __init__(self, events: List[Dict[str, Any]]):
        """
        Initialize the timeline processor.
        
        Args:
            events: List of event dictionaries
        """
        self.events = events
        self.validation_rules = self._load_validation_rules()
    
    def process_events(self) -> List[Dict[str, Any]]:
        """
        Process and validate all timeline events.
        
        Returns:
            List of processed and validated events
            
        Raises:
            ValueError: If event validation fails
        """
        processed_events = []
        
        for event in self.events:
            if self._validate_event(event):
                processed_events.append(self._enrich_event(event))
        
        return processed_events
```

## Testing Guidelines

### Writing Tests

- **Unit tests**: Test individual functions/methods
- **Integration tests**: Test component interactions
- **API tests**: Test API endpoints

### Test Structure

```python
"""Tests for timeline processor."""

import pytest
from src.timeline_processor import TimelineProcessor


class TestTimelineProcessor:
    """Test suite for TimelineProcessor."""
    
    @pytest.fixture
    def sample_events(self):
        """Provide sample events for testing."""
        return [
            {"date": "2025-01-01", "description": "Event 1"},
            {"date": "2025-01-02", "description": "Event 2"},
        ]
    
    def test_process_events_success(self, sample_events):
        """Test successful event processing."""
        processor = TimelineProcessor(sample_events)
        result = processor.process_events()
        
        assert len(result) == 2
        assert result[0]["date"] == "2025-01-01"
    
    def test_process_events_invalid_date(self):
        """Test event processing with invalid date."""
        invalid_events = [{"date": "invalid", "description": "Event"}]
        processor = TimelineProcessor(invalid_events)
        
        with pytest.raises(ValueError):
            processor.process_events()
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/unit/test_timeline_processor.py

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_timeline_processor.py::TestTimelineProcessor::test_process_events_success
```

## Submitting Changes

### Pull Request Checklist

Before submitting a pull request, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with main branch
- [ ] Changes are focused and atomic

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass
- [ ] Documentation updated
```

## Database Changes

### Schema Modifications

If your changes affect the database schema:

1. **Create migration file**:
   ```bash
   alembic revision -m "add new table for evidence tracking"
   ```

2. **Write migration**:
   - Edit the generated file in `alembic/versions/`
   - Include both `upgrade()` and `downgrade()` functions

3. **Test migration**:
   ```bash
   python scripts/run_migrations.py --verify-only
   python scripts/run_migrations.py
   ```

4. **Update schema documentation**:
   - Update `database_schema_improved.sql`
   - Document changes in PR description

### Synchronization

Database changes must be synchronized to both:
- **Supabase**: For production use
- **Neon**: For development/testing

Use the synchronization tools:
```bash
python -m src.database_sync.real_time_sync
```

## Questions or Issues?

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create a GitHub Issue
- **Security**: Email security concerns to devops@rzone.dev

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Analysis Repository! 🎉

