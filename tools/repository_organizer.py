#!/usr/bin/env python3
"""
Repository Organizer - Comprehensive File Organization Tool
==========================================================

Analyzes and organizes repository files into optimal structure with
separation of models, analysis, evidence, and documentation.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime


class RepositoryOrganizer:
    """Organizes repository files into optimal structure"""
    
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.analysis_result = {
            "timestamp": datetime.now().isoformat(),
            "categories": {},
            "structure": {},
            "recommendations": []
        }
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Analyze current repository structure"""
        print("=== ANALYZING REPOSITORY STRUCTURE ===\n")
        
        # Categorize files
        self._categorize_files()
        
        # Analyze directories
        self._analyze_directories()
        
        # Generate recommendations
        self._generate_recommendations()
        
        return self.analysis_result
    
    def _categorize_files(self):
        """Categorize all files in repository"""
        categories = {
            "models": [],
            "analysis": [],
            "evidence": [],
            "documentation": [],
            "scripts": [],
            "frameworks": [],
            "simulations": [],
            "tools": [],
            "tests": [],
            "case_files": [],
            "config": [],
            "root_python": [],
            "other": []
        }
        
        # Scan root directory
        for item in self.repo_root.iterdir():
            if item.is_file():
                self._categorize_file(item, categories)
        
        self.analysis_result["categories"] = categories
        
        # Print summary
        print("File Categories:")
        for cat, files in categories.items():
            if files:
                print(f"  {cat}: {len(files)} files")
    
    def _categorize_file(self, file_path: Path, categories: Dict[str, List]):
        """Categorize a single file"""
        name = file_path.name
        stem = file_path.stem
        
        # Skip hidden and system files
        if name.startswith('.') or name in ['LICENSE', 'alembic.ini']:
            return
        
        # Documentation
        if file_path.suffix == '.md':
            if any(keyword in stem.upper() for keyword in [
                'MODEL', 'HYPERGNN', 'TRANSFORMER', 'LLM', 'AGENT', 
                'DISCRETE', 'SYSTEM_DYNAMICS'
            ]):
                categories["models"].append(str(file_path.name))
            elif any(keyword in stem.upper() for keyword in [
                'ANALYSIS', 'FINDINGS', 'REPORT', 'SUMMARY', 'EVIDENCE',
                'CASE', 'INVESTIGATION'
            ]):
                categories["analysis"].append(str(file_path.name))
            elif any(keyword in stem.upper() for keyword in [
                'IMPLEMENTATION', 'API', 'TECHNICAL', 'ARCHITECTURE',
                'TESTING', 'GUIDE'
            ]):
                categories["documentation"].append(str(file_path.name))
            else:
                categories["documentation"].append(str(file_path.name))
        
        # Python files
        elif file_path.suffix == '.py':
            if any(keyword in stem for keyword in [
                'model', 'hypergnn', 'transformer', 'llm', 'agent_based',
                'discrete_event', 'system_dynamics'
            ]):
                categories["models"].append(str(file_path.name))
            elif any(keyword in stem for keyword in [
                'analysis', 'super_sleuth', 'hyper_holmes', 'evidence_based'
            ]):
                categories["analysis"].append(str(file_path.name))
            elif any(keyword in stem for keyword in [
                'case_', 'rezonance', 'integration', 'loader'
            ]):
                categories["case_files"].append(str(file_path.name))
            elif 'demo' in stem or 'test_' in stem:
                categories["scripts"].append(str(file_path.name))
            elif stem == 'backend_api':
                categories["frameworks"].append(str(file_path.name))
            else:
                categories["root_python"].append(str(file_path.name))
        
        # JSON files
        elif file_path.suffix == '.json':
            categories["case_files"].append(str(file_path.name))
        
        # Database files
        elif file_path.suffix == '.db':
            categories["config"].append(str(file_path.name))
        
        # SQL files
        elif file_path.suffix == '.sql':
            categories["config"].append(str(file_path.name))
        
        else:
            categories["other"].append(str(file_path.name))
    
    def _analyze_directories(self):
        """Analyze existing directory structure"""
        structure = {}
        
        for item in self.repo_root.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                structure[item.name] = self._count_files_recursive(item)
        
        self.analysis_result["structure"] = structure
        
        print("\nExisting Directories:")
        for dir_name, count in sorted(structure.items()):
            print(f"  {dir_name}: {count} files")
    
    def _count_files_recursive(self, directory: Path) -> int:
        """Count files recursively in directory"""
        count = 0
        try:
            for item in directory.rglob('*'):
                if item.is_file():
                    count += 1
        except PermissionError:
            pass
        return count
    
    def _generate_recommendations(self):
        """Generate organization recommendations"""
        recommendations = []
        
        categories = self.analysis_result["categories"]
        
        # Models recommendation
        if categories["models"]:
            recommendations.append({
                "category": "models",
                "action": "Create dedicated docs/models/ directory",
                "files": len(categories["models"]),
                "description": "Consolidate all model documentation and implementations"
            })
        
        # Analysis recommendation
        if categories["analysis"]:
            recommendations.append({
                "category": "analysis",
                "action": "Create dedicated docs/analysis/ directory", 
                "files": len(categories["analysis"]),
                "description": "Consolidate all analysis reports and findings"
            })
        
        # Evidence recommendation
        evidence_files = [f for f in categories["analysis"] if 'EVIDENCE' in f.upper()]
        if evidence_files:
            recommendations.append({
                "category": "evidence",
                "action": "Create dedicated docs/evidence/ directory",
                "files": len(evidence_files),
                "description": "Consolidate all evidence-related documentation"
            })
        
        # Root Python files
        if categories["root_python"]:
            recommendations.append({
                "category": "scripts",
                "action": "Move utility scripts to scripts/ or tools/",
                "files": len(categories["root_python"]),
                "description": "Clean up root directory by organizing scripts"
            })
        
        self.analysis_result["recommendations"] = recommendations
        
        print("\nRecommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec['action']}")
            print(f"     - {rec['description']}")
            print(f"     - Files affected: {rec['files']}")
    
    def generate_structure_documentation(self) -> str:
        """Generate comprehensive structure documentation"""
        doc = f"""# Repository Structure Documentation
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
"""
        
        # Add model files
        model_files = self.analysis_result["categories"]["models"]
        if model_files:
            doc += "\n" + "\n".join(f"- {f}" for f in sorted(model_files))
        
        doc += "\n\n### Analysis-Related Files\n"
        
        # Add analysis files
        analysis_files = self.analysis_result["categories"]["analysis"]
        if analysis_files:
            doc += "\n" + "\n".join(f"- {f}" for f in sorted(analysis_files))
        
        doc += "\n\n### Evidence-Related Files\n"
        
        # Add evidence files
        evidence_files = [f for f in analysis_files if 'EVIDENCE' in f.upper()]
        if evidence_files:
            doc += "\n" + "\n".join(f"- {f}" for f in sorted(evidence_files))
        
        doc += """

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
"""
        
        return doc
    
    def export_analysis(self, output_file: str):
        """Export analysis to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.analysis_result, f, indent=2)
        print(f"\nAnalysis exported to: {output_file}")


def main():
    """Main function"""
    repo_root = "/home/runner/work/analysis/analysis"
    
    organizer = RepositoryOrganizer(repo_root)
    
    # Analyze repository
    analysis = organizer.analyze_repository()
    
    # Generate structure documentation
    print("\n=== GENERATING STRUCTURE DOCUMENTATION ===\n")
    structure_doc = organizer.generate_structure_documentation()
    
    # Save documentation
    doc_path = Path(repo_root) / "REPOSITORY_STRUCTURE.md"
    with open(doc_path, 'w') as f:
        f.write(structure_doc)
    print(f"Structure documentation saved to: {doc_path}")
    
    # Export analysis
    analysis_path = Path(repo_root) / "repository_structure_analysis.json"
    organizer.export_analysis(str(analysis_path))
    
    print("\n=== ORGANIZATION COMPLETE ===")


if __name__ == "__main__":
    main()
