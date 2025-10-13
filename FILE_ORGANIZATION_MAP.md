# File Organization Map

Generated: 2025-10-11

## Overview

This document provides a comprehensive map of file organization in the repository,
showing where different types of files are located and how they are organized.

## Directory Structure Map

### Root Directory (`/`)

**Configuration Files:**
- `pyproject.toml` - Python project configuration
- `pytest.ini` - Test configuration
- `alembic.ini` - Database migration configuration
- `.gitignore` - Git ignore patterns
- `.pre-commit-config.yaml` - Pre-commit hooks
- `LICENSE` - Repository license

**Core Documentation:**
- `README.md` - Main repository documentation
- `TECHNICAL_ARCHITECTURE.md` - System architecture
- `API_DOCUMENTATION.md` - REST API reference
- `HYPERGRAPHQL_API_DOCUMENTATION.md` - GraphQL API reference
- `CHANGELOG.md` - Version history

**Management Documentation:**
- `REPOSITORY_STRUCTURE.md` - This structure documentation
- `FILE_ORGANIZATION_MAP.md` - File organization guide
- `repository_structure_analysis.json` - Structure analysis data

### Source Code (`/src/`)

**Purpose**: Production source code organized by functionality

```
src/
├── api/                  # API implementations
│   ├── evidence_management.py
│   ├── hypergnn_core.py
│   ├── hypergraphql_api.py
│   ├── hypergraphql_resolvers.py
│   ├── hypergraphql_schema.py
│   ├── hypergraphql_github.py
│   ├── professional_language.py
│   └── system_dynamics.py
├── models/              # Model implementations
│   ├── discrete_event_model.py
│   ├── enhanced_llm_transformer.py
│   ├── hypergnn_framework_improved.py
│   ├── comprehensive_model_demo.py
│   └── unified_model_framework.py
├── simulations/         # Simulation engines
│   └── hypergnn_case_integration.py
├── cases/               # Case-specific logic
├── data_processing/     # Data processing pipelines
├── fraud_analysis/      # Fraud detection
└── utils/              # Utility functions
    ├── neon_sync_enhanced.py
    ├── neon_sync_v2.py
    ├── supabase_sync_v2.py
    └── integrate_case_updates.py
```

**Organization Rules:**
- **API Layer** (`src/api/`): All API endpoints and GraphQL resolvers
- **Models** (`src/models/`): Core model implementations (HyperGNN, LLM, etc.)
- **Simulations** (`src/simulations/`): Simulation execution engines
- **Utils** (`src/utils/`): Shared utility functions and helpers

### Frameworks (`/frameworks/`)

**Purpose**: Core framework implementations that power the system

```
frameworks/
├── hypergnn_core_enhanced.py    # Enhanced HyperGNN framework
├── hypergraph_model.py           # Hypergraph modeling
└── llm_transformer_schema.py    # LLM transformer schema
```

**Organization Rules:**
- Stable, well-tested framework code
- Minimal dependencies between frameworks
- Comprehensive documentation in docstrings

### Tools (`/tools/`)

**Purpose**: Standalone utility tools for operations

```
tools/
├── timeline_validator.py           # Timeline validation
├── folder_structure_generator.py   # Folder structure creation
├── repository_organizer.py         # Repository organization (this tool)
├── documentation_generator.py      # Documentation generation
├── ocr_analyzer.py                # OCR processing
├── knowledge_matrix.py            # Knowledge tracking
└── verification_tracker.py        # Verification system
```

**Organization Rules:**
- Each tool should be independently executable
- Include CLI interface where appropriate
- Comprehensive help documentation

### Scripts (`/scripts/`)

**Purpose**: Automation and operational scripts

```
scripts/
├── run_agent_based_simulation.py    # Agent-based simulation runner
├── run_discrete_event_simulation.py # Discrete event simulation
├── run_system_dynamics_simulation.py # System dynamics simulation
├── run_integrated_simulation.py     # Integrated multi-model simulation
├── generate_simulation_report.py    # Report generation
└── validate_codebase.py            # Codebase validation
```

**Organization Rules:**
- Automation scripts for repetitive tasks
- Simulation runners
- Data processing scripts
- Deployment and maintenance scripts

### Documentation (`/docs/`)

**Purpose**: Comprehensive documentation organized by category

```
docs/
├── README.md                     # Documentation index
├── FEATURE_INDEX.md             # Feature catalog
├── models/                      # Model documentation
│   ├── README.md
│   ├── hypergnn/
│   ├── llm/
│   ├── discrete_event/
│   └── system_dynamics/
├── analysis/                    # Analysis documentation
│   ├── README.md
│   ├── findings/
│   ├── reports/
│   └── summaries/
├── evidence/                    # Evidence documentation
│   ├── README.md
│   ├── reports/
│   └── verification/
├── technical/                   # Technical documentation
│   ├── README.md
│   ├── architecture/
│   ├── api/
│   └── guides/
└── legal/                      # Legal documentation
    ├── README.md
    ├── frameworks/
    ├── templates/
    └── procedures/
```

**Organization Rules:**
- Organize by topic and audience
- Include README in each subdirectory
- Keep documentation close to code when possible
- Update documentation with code changes

### Case Files (`/cases/` and `/case_*/`)

**Purpose**: Case-specific data and documentation

```
cases/
├── active/                      # Active cases
├── closed/                      # Closed cases
└── templates/                   # Case templates

case_2025_137857/               # Specific case directory
├── 01_court_documents/
├── 02_evidence/
├── 03_analysis/
├── 05_medical_records/
├── 06_financial_fraud/
├── 07_legal_research/
└── 08_case_notes/
```

**Organization Rules:**
- Each case gets dedicated directory
- Follow consistent internal structure
- Separate by evidence type
- Maintain chain of custody documentation

### Evidence (`/evidence/`)

**Purpose**: Evidence file storage

```
evidence/
├── documents/                   # Document evidence
├── digital/                     # Digital evidence
├── media/                       # Media evidence
├── rezonance/                   # Rezonance-specific
├── trial_balances_2020/        # Financial data
└── metadata/                    # Evidence metadata
```

**Organization Rules:**
- Organize by evidence type
- Maintain metadata
- Follow chain of custody
- Apply appropriate classification

### Examples (`/examples/`)

**Purpose**: Example code and demonstrations

```
examples/
└── hypergraphql_hypergnn_integration.py
```

**Organization Rules:**
- Complete, working examples
- Well-documented code
- Demonstrate best practices
- Include sample data

### Tests (`/tests/`)

**Purpose**: Test suites for code validation

```
tests/
├── __init__.py
├── conftest.py                  # Test configuration
├── unit/                        # Unit tests
├── integration/                 # Integration tests
└── api/                         # API tests
```

**Organization Rules:**
- Mirror source code structure
- >80% code coverage target
- Fast unit tests
- Comprehensive integration tests

### Simulation Outputs (`/sims/`)

**Purpose**: Simulation result storage

```
sims/
├── agent_based/                 # Agent-based results
├── discrete_event/              # Discrete event results
├── system_dynamics/             # System dynamics results
└── integrated/                  # Integrated results
```

**Organization Rules:**
- Timestamped result files
- JSON format for data
- Include metadata
- Archive old results

### Database (`/alembic/`)

**Purpose**: Database migration management

```
alembic/
├── versions/                    # Migration versions
└── env.py                       # Alembic environment
```

**Organization Rules:**
- Version-controlled migrations
- Descriptive migration names
- Test migrations thoroughly
- Document breaking changes

### Frontend (`/analysis-frontend/`)

**Purpose**: React-based frontend application

```
analysis-frontend/
├── public/                      # Static assets
├── src/                         # React source code
└── package.json                 # Node dependencies
```

**Organization Rules:**
- Standard React project structure
- Component-based architecture
- Separate business logic
- Comprehensive tests

## File Type Guidelines

### Python Files (`.py`)

**Location by Purpose:**
- **Models**: `src/models/` or `frameworks/`
- **API**: `src/api/`
- **Tools**: `tools/`
- **Scripts**: `scripts/`
- **Tests**: `tests/`
- **Utils**: `src/utils/`

**Naming Convention:**
- Lowercase with underscores
- Descriptive names
- Module-level organization

### Documentation Files (`.md`)

**Location by Purpose:**
- **Root Docs**: Root directory (README, TECHNICAL_ARCHITECTURE, etc.)
- **Model Docs**: `docs/models/`
- **Analysis Docs**: `docs/analysis/`
- **Evidence Docs**: `docs/evidence/`
- **Technical Docs**: `docs/technical/`
- **Legal Docs**: `docs/legal/`

**Naming Convention:**
- UPPERCASE for root-level docs
- lowercase-with-hyphens for subdirectory docs
- Descriptive, consistent naming

### Configuration Files

**Location**: Root directory

**Files:**
- `pyproject.toml` - Python configuration
- `pytest.ini` - Test configuration
- `alembic.ini` - Database configuration
- `.gitignore` - Git configuration
- `.pre-commit-config.yaml` - Pre-commit hooks

### Data Files (`.json`, `.csv`, `.sql`)

**Location by Purpose:**
- **Case Data**: Case directories
- **Evidence Data**: `evidence/`
- **Simulation Results**: `sims/`
- **Configuration**: Root or relevant subdirectory
- **Database Schema**: Root directory

## Organization Best Practices

### 1. Keep Root Directory Clean
- Only essential files in root
- Move scripts to `scripts/` or `tools/`
- Move data files to appropriate directories
- Use subdirectories for organization

### 2. Use Consistent Naming
- Follow established patterns
- Use descriptive names
- Avoid abbreviations unless standard
- Be consistent across similar files

### 3. Document Everything
- README in each major directory
- Docstrings in all Python modules
- Comments for complex logic
- Keep documentation up to date

### 4. Separate Concerns
- Source code in `src/`
- Documentation in `docs/`
- Tests in `tests/`
- Tools in `tools/`
- Scripts in `scripts/`

### 5. Version Control
- Commit logically related changes together
- Write descriptive commit messages
- Use branches for features
- Tag releases

### 6. Testing
- Test at appropriate levels
- Maintain high coverage
- Keep tests fast
- Test edge cases

### 7. Dependencies
- Document all dependencies
- Pin versions for stability
- Regular security updates
- Minimize dependencies

## File Movement Guidelines

When reorganizing files:

1. **Plan the move**
   - Identify all affected files
   - Map current → new locations
   - Identify import dependencies

2. **Update imports**
   - Find all import statements
   - Update to new paths
   - Test imports work

3. **Update documentation**
   - Update file references
   - Update directory structures
   - Update examples

4. **Test thoroughly**
   - Run all tests
   - Check all functionality
   - Verify no broken imports

5. **Commit incrementally**
   - Small, logical commits
   - Clear commit messages
   - Test between commits

## Maintenance

This organization structure should be:
- Reviewed quarterly
- Updated as repository evolves
- Documented when changed
- Communicated to team

Tools available:
- `python tools/repository_organizer.py` - Analyze structure
- `python tools/documentation_generator.py` - Generate docs
- `python tools/folder_structure_generator.py` - Evidence folders

## Contact

For questions about file organization:
1. Check this document first
2. Review REPOSITORY_STRUCTURE.md
3. Consult technical lead
4. Update documentation as needed
