# Repository Navigation Guide

**Last Updated:** 2025-10-11

## Overview

This guide helps you navigate the Analysis Repository efficiently, whether you're a legal practitioner, technical user, analyst, or contributor.

## Quick Navigation by Role

### 👨‍⚖️ Legal Practitioners

**Start Here:**
1. [Documentation Hub](docs/README.md) - Central documentation portal
2. [Legal Frameworks](docs/legal/frameworks/) - Case analysis methodologies
3. [Legal Templates](docs/legal/templates/) - Document templates
4. [Legal Procedures](docs/legal/procedures/) - Workflow procedures

**For Specific Tasks:**
- **Case Analysis** → [Criminal Case Timeline Framework](criminal-case-timeline-outline-sa.md)
- **Document Preparation** → [Legal Templates](docs/legal/templates/)
- **Evidence Management** → [Evidence Management Guide](FOLDER_STRUCTURE_IMPLEMENTATION.md)
- **Timeline Construction** → [Timeline Processing Guide](timeline-processor.md)

### 👨‍💻 Technical Users

**Start Here:**
1. [Technical Architecture](TECHNICAL_ARCHITECTURE.md) - System architecture
2. [API Documentation](docs/technical/api/) - API references
3. [Implementation Guides](docs/technical/guides/) - Development guides
4. [Repository Structure](REPOSITORY_STRUCTURE.md) - Code organization

**For Specific Tasks:**
- **API Integration** → [API Documentation](API_DOCUMENTATION.md)
- **Model Implementation** → [Model Documentation](docs/models/)
- **Development Setup** → [Implementation Guides](docs/technical/guides/)
- **Testing** → [Testing Guide](TESTING.md)

### 📊 Analysts

**Start Here:**
1. [Feature Index](docs/FEATURE_INDEX.md) - Capability overview
2. [Analysis Documentation](docs/analysis/) - Analysis workflows
3. [Evidence Documentation](docs/evidence/) - Evidence handling
4. [Model Documentation](docs/models/) - Analytical models

**For Specific Tasks:**
- **Case Analysis** → [Analysis Reports](docs/analysis/reports/)
- **Evidence Analysis** → [Evidence Reports](docs/evidence/reports/)
- **Timeline Analysis** → [Timeline Processing](timeline-processor.md)
- **Findings Documentation** → [Findings](docs/analysis/findings/)

### 🔧 Contributors

**Start Here:**
1. [Repository Structure](REPOSITORY_STRUCTURE.md) - Structure guide
2. [File Organization Map](FILE_ORGANIZATION_MAP.md) - Organization rules
3. [Technical Architecture](TECHNICAL_ARCHITECTURE.md) - System design
4. [Testing Guide](TESTING.md) - Testing requirements

**For Specific Tasks:**
- **Code Organization** → [File Organization Map](FILE_ORGANIZATION_MAP.md)
- **Documentation** → [Documentation Hub](docs/README.md)
- **Testing** → [Testing Guide](TESTING.md)
- **Style Guidelines** → [Professional Language Guide](PROFESSIONAL_LANGUAGE_STYLE_GUIDE.md)

## Navigation by Topic

### Models & Frameworks

#### HyperGNN Framework
- **Overview**: [HyperGNN Documentation](docs/models/hypergnn/)
- **Schema**: [HYPERGNN_COMPREHENSIVE_SCHEMA.md](HYPERGNN_COMPREHENSIVE_SCHEMA.md)
- **Implementation**: `frameworks/hypergnn_core_enhanced.py`
- **API**: `src/api/hypergnn_core.py`

#### LLM Transformers
- **Overview**: [LLM Documentation](docs/models/llm/)
- **Schema**: [LLM_TRANSFORMER_SCHEMA_DOCUMENTATION.md](LLM_TRANSFORMER_SCHEMA_DOCUMENTATION.md)
- **Implementation**: `frameworks/llm_transformer_schema.py`
- **Enhanced**: `src/models/enhanced_llm_transformer.py`

#### Discrete Event Models
- **Overview**: [Discrete Event Documentation](docs/models/discrete_event/)
- **Summary**: [DISCRETE_EVENT_MODEL_SUMMARY.md](DISCRETE_EVENT_MODEL_SUMMARY.md)
- **Implementation**: `src/models/discrete_event_model.py`
- **Scripts**: `scripts/run_discrete_event_simulation.py`

#### System Dynamics
- **Overview**: [System Dynamics Documentation](docs/models/system_dynamics/)
- **Implementation**: `frameworks/system_dynamics.py`
- **API**: `src/api/system_dynamics.py`
- **Scripts**: `scripts/run_system_dynamics_simulation.py`

### Evidence Management

#### Evidence System
- **Overview**: [Evidence Documentation](docs/evidence/)
- **Implementation Guide**: [FOLDER_STRUCTURE_IMPLEMENTATION.md](FOLDER_STRUCTURE_IMPLEMENTATION.md)
- **Core System**: `frameworks/evidence_management.py`
- **API**: `src/api/evidence_management.py`

#### Evidence Reports
- **Location**: [Evidence Reports](docs/evidence/reports/)
- **Examples**: 
  - [Evidence Based Report](EVIDENCE_BASED_REPORT.md)
  - [Material Evidence Report](MATERIAL_EVIDENCE_REPORT.md)
  - [Final Evidence Summary](FINAL_EVIDENCE_SUMMARY.md)

#### Evidence Verification
- **Location**: [Verification Documentation](docs/evidence/verification/)
- **Tools**: `tools/verification_tracker.py`

### Analysis & Reporting

#### Analysis Workflows
- **Overview**: [Analysis Documentation](docs/analysis/)
- **Findings**: [Analysis Findings](docs/analysis/findings/)
- **Reports**: [Analysis Reports](docs/analysis/reports/)
- **Summaries**: [Executive Summaries](docs/analysis/summaries/)

#### Timeline Analysis
- **Framework**: [Timeline Processing Guide](timeline-processor.md)
- **Validator**: `tools/timeline_validator.py`
- **Case Timeline**: [Criminal Case Timeline](criminal-case-timeline-outline-sa.md)

#### Report Generation
- **Scripts**: `scripts/generate_simulation_report.py`
- **Templates**: Available in [Analysis Reports](docs/analysis/reports/)

### API & Integration

#### REST API
- **Overview**: [API Documentation](API_DOCUMENTATION.md)
- **Detailed Guide**: [API Technical Docs](docs/technical/api/)
- **Implementation**: `backend_api.py`

#### GraphQL API
- **Overview**: [HyperGraphQL Documentation](HYPERGRAPHQL_API_DOCUMENTATION.md)
- **Schema**: `src/api/hypergraphql_schema.py`
- **Resolvers**: `src/api/hypergraphql_resolvers.py`
- **API**: `src/api/hypergraphql_api.py`

#### Integration Guides
- **Location**: [Implementation Guides](docs/technical/guides/)
- **Examples**: `examples/hypergraphql_hypergnn_integration.py`

### Legal Resources

#### Legal Frameworks
- **Location**: [Legal Frameworks](docs/legal/frameworks/)
- **Criminal Timeline**: [Criminal Case Timeline](criminal-case-timeline-outline-sa.md)
- **UK-SA Cooperation**: [UK_SA_LEGAL_COOPERATION_FRAMEWORK.md](UK_SA_LEGAL_COOPERATION_FRAMEWORK.md)

#### Legal Templates
- **Location**: [Legal Templates](docs/legal/templates/)
- **Examples in Root**:
  - Formal notices
  - Court order templates
  - Affidavit drafts

#### Legal Procedures
- **Location**: [Legal Procedures](docs/legal/procedures/)
- **Processing**: [Timeline Processing](timeline-processor.md)

### Tools & Utilities

#### Analysis Tools
- **Timeline Validator**: `tools/timeline_validator.py`
- **Knowledge Matrix**: `tools/knowledge_matrix.py`
- **OCR Analyzer**: `tools/ocr_analyzer.py`
- **Verification Tracker**: `tools/verification_tracker.py`

#### Organization Tools
- **Repository Organizer**: `tools/repository_organizer.py`
- **Documentation Generator**: `tools/documentation_generator.py`
- **Folder Structure Generator**: `tools/folder_structure_generator.py`

#### Automation Scripts
- **Location**: `scripts/`
- **Simulations**:
  - `run_agent_based_simulation.py`
  - `run_discrete_event_simulation.py`
  - `run_system_dynamics_simulation.py`
  - `run_integrated_simulation.py`
- **Utilities**:
  - `generate_simulation_report.py`
  - `validate_codebase.py`

## Navigation by File Type

### Python Source Code

#### Production Code
- **Location**: `src/`
- **Structure**:
  - `src/api/` - API implementations
  - `src/models/` - Model implementations
  - `src/simulations/` - Simulation engines
  - `src/utils/` - Utility functions
  - `src/data_processing/` - Data pipelines

#### Frameworks
- **Location**: `frameworks/`
- **Files**:
  - `hypergnn_core_enhanced.py`
  - `hypergraph_model.py`
  - `llm_transformer_schema.py`

#### Tools
- **Location**: `tools/`
- See Tools & Utilities section above

#### Scripts
- **Location**: `scripts/`
- See Tools & Utilities section above

### Documentation

#### Markdown Files

##### Root Documentation
- System-level docs in root directory
- See [File Organization Map](FILE_ORGANIZATION_MAP.md)

##### Organized Documentation
- **Main Hub**: `docs/README.md`
- **Categories**: `docs/{models,analysis,evidence,technical,legal}/`
- **Indexes**: `docs/FEATURE_INDEX.md`

#### Configuration Files
- `pyproject.toml` - Python configuration
- `pytest.ini` - Test configuration
- `alembic.ini` - Database configuration
- `.gitignore` - Git configuration

### Case Files

#### Active Cases
- **Location**: `cases/active/`
- **Example**: `case_2025_137857/`

#### Case Documentation
- **Professional Docs**: `case_2025_137857_professional_court_docs/`
- **Structure**:
  - Case summaries
  - Evidence indexes
  - Timelines
  - Court documents
  - Legal analysis

### Evidence Files

#### Evidence Storage
- **Location**: `evidence/`
- **Structure**:
  - `documents/`
  - `digital/`
  - `media/`
  - `metadata/`

#### Evidence Organization
- See [Evidence Management Guide](FOLDER_STRUCTURE_IMPLEMENTATION.md)

### Test Files

#### Test Structure
- **Location**: `tests/`
- **Categories**:
  - `tests/unit/` - Unit tests
  - `tests/integration/` - Integration tests
  - `tests/api/` - API tests

## Common Workflows

### Starting a New Case

1. **Setup**:
   - Review [Legal Frameworks](docs/legal/frameworks/)
   - Check [Case Templates](cases/templates/)
   - Review [Evidence Management](FOLDER_STRUCTURE_IMPLEMENTATION.md)

2. **Case Creation**:
   - Create case directory in `cases/active/`
   - Use case template structure
   - Initialize documentation

3. **Evidence Collection**:
   - Follow [Evidence Procedures](docs/evidence/)
   - Use Evidence Management System
   - Maintain chain of custody

4. **Analysis**:
   - Build timeline using [Timeline Guide](timeline-processor.md)
   - Run analysis using models
   - Document findings in [Findings](docs/analysis/findings/)

5. **Reporting**:
   - Create reports in [Analysis Reports](docs/analysis/reports/)
   - Generate summaries in [Summaries](docs/analysis/summaries/)
   - Prepare court documents using [Templates](docs/legal/templates/)

### Running Simulations

1. **Preparation**:
   - Review [Model Documentation](docs/models/)
   - Prepare case data
   - Configure parameters

2. **Execution**:
   - Choose appropriate simulation script from `scripts/`
   - Run simulation
   - Monitor progress

3. **Results**:
   - Review results in `sims/`
   - Generate report using `generate_simulation_report.py`
   - Document findings

### API Integration

1. **Setup**:
   - Review [API Documentation](docs/technical/api/)
   - Check [Implementation Guides](docs/technical/guides/)
   - Set up authentication

2. **Integration**:
   - Choose REST or GraphQL API
   - Follow integration examples
   - Test endpoints

3. **Development**:
   - Use [Technical Architecture](TECHNICAL_ARCHITECTURE.md)
   - Follow code organization guidelines
   - Write tests

## Search Tips

### Finding Documentation

1. **By Topic**: Use [Documentation Hub](docs/README.md)
2. **By Feature**: Use [Feature Index](docs/FEATURE_INDEX.md)
3. **By Type**: Use [File Organization Map](FILE_ORGANIZATION_MAP.md)
4. **By Structure**: Use [Repository Structure](REPOSITORY_STRUCTURE.md)

### Finding Code

1. **Source Code**: Check `src/` directory structure
2. **Frameworks**: Check `frameworks/` directory
3. **Tools**: Check `tools/` directory
4. **Scripts**: Check `scripts/` directory
5. **Examples**: Check `examples/` directory

### Finding Help

1. **Getting Started**: [Quick Start](#quick-navigation-by-role) section
2. **Implementation**: [Implementation Guides](docs/technical/guides/)
3. **API Help**: [API Documentation](docs/technical/api/)
4. **Troubleshooting**: Check relevant README files

## Maintenance

This navigation guide is maintained alongside the repository structure.

**Review Schedule**: Quarterly
**Update Trigger**: Structure changes, new features, user feedback
**Responsibility**: Documentation team

## Feedback

To provide feedback on navigation:
1. Identify navigation issues
2. Document the problem
3. Suggest improvements
4. Submit feedback through appropriate channels

---

**Quick Links:**
- [Main README](README.md)
- [Documentation Hub](docs/README.md)
- [Repository Structure](REPOSITORY_STRUCTURE.md)
- [File Organization Map](FILE_ORGANIZATION_MAP.md)
- [Feature Index](docs/FEATURE_INDEX.md)
