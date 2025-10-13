# Repository Structure Documentation
Generated: 2025-10-11 01:34:14

## Overview

This document describes the optimal organization structure for the analysis repository,
separating concerns between models, analysis, evidence, and supporting infrastructure.

## Directory Structure

```
analysis/
├── docs/                          # All documentation
│   ├── models/                    # Model documentation
│   │   ├── hypergnn/             # HyperGNN framework docs
│   │   ├── llm/                  # LLM transformer docs
│   │   ├── discrete_event/       # Discrete event model docs
│   │   └── system_dynamics/      # System dynamics docs
│   ├── analysis/                  # Analysis reports
│   │   ├── findings/             # Investigation findings
│   │   ├── reports/              # Comprehensive reports
│   │   └── summaries/            # Executive summaries
│   ├── evidence/                  # Evidence documentation
│   │   ├── reports/              # Evidence reports
│   │   ├── verification/         # Verification docs
│   │   └── chain_of_custody/     # Chain of custody
│   ├── technical/                 # Technical documentation
│   │   ├── architecture/         # System architecture
│   │   ├── api/                  # API documentation
│   │   └── guides/               # Implementation guides
│   └── legal/                     # Legal documentation
│       ├── frameworks/           # Legal frameworks
│       ├── templates/            # Legal templates
│       └── procedures/           # Legal procedures
│
├── src/                          # Source code
│   ├── models/                   # Model implementations
│   │   ├── hypergnn/            # HyperGNN core
│   │   ├── llm/                 # LLM transformers
│   │   ├── discrete_event/      # Discrete event models
│   │   └── system_dynamics/     # System dynamics models
│   ├── analysis/                # Analysis engines
│   │   ├── evidence/           # Evidence analysis
│   │   ├── timeline/           # Timeline analysis
│   │   └── relationship/       # Relationship analysis
│   ├── api/                     # API implementations
│   ├── utils/                   # Utility functions
│   └── data_processing/         # Data processing
│
├── frameworks/                   # Core frameworks
│   ├── hypergnn_core.py         # HyperGNN framework
│   ├── evidence_management.py   # Evidence management
│   ├── system_dynamics.py       # System dynamics
│   └── professional_language.py # Language processing
│
├── tools/                        # Utility tools
│   ├── timeline_validator.py    # Timeline validation
│   ├── folder_structure_generator.py
│   ├── repository_organizer.py  # This tool
│   └── ocr_analyzer.py          # OCR processing
│
├── scripts/                      # Automation scripts
│   ├── run_simulations/         # Simulation runners
│   ├── data_processing/         # Data processing
│   └── utilities/               # General utilities
│
├── tests/                        # Test suites
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── api/                     # API tests
│
├── cases/                        # Case management
│   ├── active/                  # Active cases
│   ├── closed/                  # Closed cases
│   └── templates/               # Case templates
│
├── evidence/                     # Evidence storage
│   ├── documents/               # Document evidence
│   ├── digital/                 # Digital evidence
│   ├── media/                   # Media evidence
│   └── metadata/                # Evidence metadata
│
├── sims/                         # Simulation outputs
│   ├── agent_based/             # Agent-based results
│   ├── discrete_event/          # Discrete event results
│   ├── system_dynamics/         # System dynamics results
│   └── integrated/              # Integrated results
│
├── examples/                     # Example code
├── alembic/                      # Database migrations
└── analysis-frontend/            # Frontend application
```

## Category Descriptions

### Documentation (`docs/`)

All documentation organized by topic:
- **models/**: Model architecture and implementation docs
- **analysis/**: Analysis reports and findings
- **evidence/**: Evidence documentation and tracking
- **technical/**: Technical architecture and guides
- **legal/**: Legal frameworks and procedures

### Source Code (`src/`)

Production code organized by functionality:
- **models/**: All model implementations
- **analysis/**: Analysis engine implementations
- **api/**: API endpoint implementations
- **utils/**: Shared utility functions
- **data_processing/**: Data processing pipelines

### Frameworks (`frameworks/`)

Core framework implementations that power the system:
- HyperGNN framework
- Evidence management system
- System dynamics modeling
- Professional language processing

### Tools (`tools/`)

Standalone utility tools for operations:
- Timeline validation
- Folder structure generation
- Repository organization
- OCR analysis

### Scripts (`scripts/`)

Automation and operational scripts:
- Simulation runners
- Data processing scripts
- Utility scripts

### Cases (`cases/`)

Case file management:
- Active case tracking
- Closed case archives
- Case templates

### Evidence (`evidence/`)

Evidence file storage:
- Document evidence
- Digital evidence
- Media evidence
- Evidence metadata

## File Categories

### Model-Related Files

- AGENT_MODEL_FOR_ENTITIES.md
- COMPREHENSIVE_MODEL_SUITE_DOCUMENTATION.md
- DISCRETE_EVENT_MODEL_SUMMARY.md
- HYPERGNN_COMPREHENSIVE_SCHEMA.md
- IMPLEMENTATION_COMPLETE_AGENT_MODEL.md
- LLM_TRANSFORMER_IMPLEMENTATION_GUIDE.md
- LLM_TRANSFORMER_SCHEMA_DOCUMENTATION.md
- README_AGENT_MODEL.md
- demo_agent_model_entities.py

### Analysis-Related Files

- BANTJIES_DEBT_ANALYSIS.md
- CASE_HYPERGRAPH_DOCUMENTATION.md
- CODEBASE_ANALYSIS_AND_IMPROVEMENTS.md
- CORPORATE_AUTHORITY_ANALYSIS.md
- CORRECTED_EVIDENCE_ANALYSIS.md
- DATABASE_SYNCHRONIZATION_SUMMARY.md
- DOCUMENT_SIGNIFICANCE_PROCESSING_SUMMARY.md
- ENHANCED_SIMULATION_SUMMARY.md
- EVIDENCE_BASED_REPORT.md
- FINAL_EVIDENCE_SUMMARY.md
- FINAL_REPORT.md
- FINANCIAL_FACTS_SUMMARY.md
- HYPERGRAPHQL_IMPLEMENTATION_SUMMARY.md
- IMPLEMENTATION_SUMMARY.md
- IMPROVEMENT_IMPLEMENTATION_SUMMARY.md
- INTEGRATION_COMPLETION_REPORT.md
- JURISDICTION_STRATEGY_SUMMARY.md
- MATERIAL_EVIDENCE_REPORT.md
- OCR_INTEGRATION_COMPLETE_SUMMARY.md
- OPTIMIZATION_SUMMARY.md
- RECONNAISSANCE_FINDINGS.md
- REFACTORING_COMPLETE_SUMMARY.md
- REVISED_CASE_STATUS_COMPLETE.md
- REZONANCE_CASE_INTEGRATION.md
- REZONANCE_CASE_INTEGRATION_UPDATE.md
- SUPER_SLEUTH_ANALYSIS_FINDINGS.md
- SUPER_SLEUTH_INITIAL_FINDINGS.md
- TIMELINE_PROCESSING_SUMMARY.md
- UNAUTHORIZED_CONTROL_EVIDENCE.md
- UPDATE_COMPLETION_SUMMARY.md
- case_analysis_and_strategy.md
- comprehensive_vulnerability_report_case_2025_137857_20251008_074206.md
- criminal-case-timeline-outline-sa.md
- document_integration_report.md
- enhanced_trial_balance_analysis.py
- enhancement_summary.md
- entities_dates_summary.md
- evidence_based_analysis.py
- hyper_holmes_turbo_solve.py
- repository_analysis_report.md
- settlement_vulnerability_report_case_2025_137857_20251008_073926.md
- super_sleuth_analysis.py

### Evidence-Related Files

- CORRECTED_EVIDENCE_ANALYSIS.md
- EVIDENCE_BASED_REPORT.md
- FINAL_EVIDENCE_SUMMARY.md
- MATERIAL_EVIDENCE_REPORT.md
- UNAUTHORIZED_CONTROL_EVIDENCE.md
- evidence_based_analysis.py

## Organization Principles

1. **Separation of Concerns**: Models, analysis, evidence, and docs are clearly separated
2. **Discoverability**: Logical hierarchy makes files easy to find
3. **Scalability**: Structure supports growth and new features
4. **Maintainability**: Clear organization simplifies maintenance
5. **Consistency**: Similar files are grouped together

## Migration Notes

When reorganizing:
1. Move files to new locations
2. Update all import statements
3. Update documentation references
4. Test all functionality
5. Update CI/CD pipelines
6. Commit changes incrementally

## Best Practices

- Keep root directory clean with only essential files
- Use descriptive directory names
- Maintain README files in each major directory
- Document file purposes in docstrings
- Follow naming conventions consistently

## Maintenance

This structure should be reviewed and updated as the repository evolves.
Run `python tools/repository_organizer.py` to analyze current state.
