#!/usr/bin/env python3
"""
Evidence Management System - Folder Structure Generator
======================================================

Utility script for generating, visualizing, and documenting
folder structures for evidence management systems.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frameworks.evidence_management import EvidenceManagementSystem


class FolderStructureGenerator:
    """Utility class for generating and managing evidence folder structures"""

    def __init__(self, base_directory: str = None):
        self.base_directory = base_directory or "/tmp/evidence_repository"
        self.ems = EvidenceManagementSystem(base_directory)

    def generate_all_structures(self) -> Dict[str, Any]:
        """Generate all types of folder structures"""
        return {
            "base_structure": self.ems.generate_folder_structure_report(),
            "visualization": self.ems.visualize_folder_structure(),
            "comprehensive_list": self.ems._generate_comprehensive_folder_structure(),
            "timestamp": datetime.now().isoformat(),
        }

    def create_template_structure(self, output_dir: str = None) -> Dict[str, Any]:
        """Create a template folder structure with documentation"""
        if output_dir:
            self.ems.base_directory = output_dir

        # Ensure directory structure exists
        self.ems._ensure_directory_structure()

        # Create documentation files
        self._create_documentation_files()

        return {
            "base_directory": self.ems.base_directory,
            "folders_created": len(self.ems._generate_comprehensive_folder_structure()),
            "documentation_files": self._get_documentation_files(),
            "created_timestamp": datetime.now().isoformat(),
        }

    def _create_documentation_files(self):
        """Create documentation files for the folder structure"""

        # Main README
        readme_content = self._generate_main_readme()
        with open(f"{self.ems.base_directory}/README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)

        # Structure documentation
        structure_doc = self._generate_structure_documentation()
        with open(
            f"{self.ems.base_directory}/FOLDER_STRUCTURE.md", "w", encoding="utf-8"
        ) as f:
            f.write(structure_doc)

        # Category-specific READMEs
        self._create_category_readmes()

        # .gitkeep files for empty directories
        self._create_gitkeep_files()

    def _generate_main_readme(self) -> str:
        """Generate main README content"""
        return f"""# Evidence Management System Repository

This repository contains a comprehensive folder structure for managing legal evidence and case documentation.

## Generated Information
- **Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Base Directory:** {self.ems.base_directory}
- **Total Folders:** {len(self.ems._generate_comprehensive_folder_structure())}

## Quick Navigation
- [`FOLDER_STRUCTURE.md`](FOLDER_STRUCTURE.md) - Detailed folder structure documentation
- [`documents/`](documents/) - Legal documents, contracts, and correspondence
- [`communications/`](communications/) - Email, phone records, and messages
- [`financial/`](financial/) - Bank statements and financial records
- [`technical/`](technical/) - Digital forensics and technical analysis
- [`media/`](media/) - Photographs, audio, and video evidence
- [`cases/`](cases/) - Case management and organization
- [`analysis/`](analysis/) - Analysis reports and findings
- [`classified/`](classified/) - Security-classified evidence

## Folder Structure Overview

{self.ems.visualize_folder_structure()}

## Usage Instructions

1. **Adding Evidence**: Place evidence files in appropriate category folders
2. **Case Management**: Use the `cases/` directory to organize by case
3. **Date Organization**: Evidence is organized by year/month within categories
4. **Classification**: Sensitive evidence goes in the `classified/` directory
5. **Working Files**: Use `working/` directory for temporary files

## Security Notes

- Classified evidence requires appropriate security clearance
- Maintain chain of custody documentation in `metadata/chain_of_custody/`
- Regular backups are stored in `backup/` with different frequencies
- Archive completed cases in `archive/completed_cases/`

For detailed folder descriptions and usage guidelines, see [FOLDER_STRUCTURE.md](FOLDER_STRUCTURE.md).
"""

    def _generate_structure_documentation(self) -> str:
        """Generate detailed structure documentation"""
        report = self.ems.generate_folder_structure_report()

        doc = f"""# Folder Structure Documentation

## Overview
This document provides detailed information about the evidence management system folder structure.

**Generated:** {report['created_timestamp']}  
**Total Folders:** {report['total_folders']}  
**Date-Based Organization:** {'Yes' if report['date_based_organization'] else 'No'}

## Main Categories

"""

        for category in report["main_categories"]:
            doc += f"### 📁 {category['name'].title()}\n"
            doc += f"**Path:** `{category['path']}`  \n"
            doc += f"**Description:** {category['description']}\n\n"

            if category["name"] in report["subcategories"]:
                subcats = report["subcategories"][category["name"]]
                if subcats:
                    doc += "**Subcategories:**\n"
                    for subcat in sorted(subcats):
                        doc += f"- `{subcat}`\n"
                    doc += "\n"

        doc += """## Organization Principles

### Date-Based Organization
Evidence is organized by collection date in YYYY/MM format within each category:
```
documents/
├── contracts/
│   ├── 2025/01/
│   ├── 2025/02/
│   └── ...
└── legal/
    ├── 2025/01/
    └── ...
```

### Classification Levels
Sensitive evidence is organized by security classification:
- `classified/public/` - Public access evidence
- `classified/confidential/` - Confidential evidence
- `classified/restricted/` - Restricted access evidence  
- `classified/privileged/` - Privileged/attorney-client evidence

### Case Management
Individual cases have dedicated folder structures:
```
cases/active/{case_id}/
├── evidence/
├── analysis/
├── reports/
└── working/
```

### File Naming Convention
Evidence files follow the pattern: `{evidence_id}_{date}_{title}`

Example: `EV001_20250101_Communication_Analysis_Report`

## Backup Strategy
- `backup/daily/` - Daily incremental backups
- `backup/weekly/` - Weekly full backups  
- `backup/monthly/` - Monthly archive backups

## Working Directories
- `working/staging/` - New evidence staging area
- `working/processing/` - Evidence under processing
- `working/review/` - Evidence under review
- `working/temp/` - Temporary files (auto-cleaned)

## Security Considerations
1. Classified folders require appropriate access controls
2. Chain of custody must be maintained for all evidence
3. Hash verification for file integrity
4. Audit trails in metadata folders
"""

        return doc

    def _create_category_readmes(self):
        """Create README files for main categories"""
        categories = {
            "documents": {
                "title": "Legal Documents",
                "description": "Repository for all legal documents, contracts, reports, and official correspondence.",
                "subcategories": [
                    "contracts",
                    "legal",
                    "reports",
                    "correspondence",
                    "forms",
                    "statements",
                ],
                "examples": [
                    "Contracts and agreements",
                    "Court filings",
                    "Analysis reports",
                    "Email correspondence",
                ],
            },
            "communications": {
                "title": "Communication Evidence",
                "description": "All forms of communication evidence including emails, phone records, and messages.",
                "subcategories": [
                    "emails",
                    "phone_records",
                    "text_messages",
                    "social_media",
                    "instant_messages",
                    "voicemails",
                ],
                "examples": [
                    "Email threads",
                    "Call logs",
                    "Text message exports",
                    "Social media posts",
                ],
            },
            "financial": {
                "title": "Financial Records",
                "description": "Financial evidence including bank statements, transactions, and monetary records.",
                "subcategories": [
                    "bank_statements",
                    "transaction_records",
                    "invoices",
                    "receipts",
                    "tax_documents",
                    "investment_records",
                ],
                "examples": [
                    "Bank account statements",
                    "Wire transfer records",
                    "Invoice copies",
                    "Receipt scans",
                ],
            },
            "technical": {
                "title": "Technical Evidence",
                "description": "Digital forensics, system logs, and technical analysis evidence.",
                "subcategories": [
                    "digital_forensics",
                    "network_logs",
                    "system_logs",
                    "database_exports",
                    "code_analysis",
                    "hardware_analysis",
                ],
                "examples": [
                    "Hard drive images",
                    "Network traffic logs",
                    "Server logs",
                    "Database dumps",
                ],
            },
            "media": {
                "title": "Media Evidence",
                "description": "Photographs, audio recordings, video files, and multimedia evidence.",
                "subcategories": [
                    "photographs/originals",
                    "photographs/processed",
                    "audio/recordings",
                    "audio/transcriptions",
                    "video/surveillance",
                    "video/interviews",
                ],
                "examples": [
                    "Crime scene photos",
                    "Audio recordings",
                    "Security camera footage",
                    "Interview videos",
                ],
            },
        }

        for category, info in categories.items():
            readme_path = f"{self.ems.base_directory}/{category}/README.md"
            os.makedirs(os.path.dirname(readme_path), exist_ok=True)

            content = f"""# {info['title']}

{info['description']}

## Organization Structure

This directory is organized by date (YYYY/MM) within each subcategory:

"""
            for subcat in info["subcategories"]:
                content += f"- `{subcat}/` - {subcat.replace('_', ' ').title()}\n"

            content += f"""
## Examples of Evidence Types

"""
            for example in info["examples"]:
                content += f"- {example}\n"

            content += f"""
## File Naming Convention

Files should follow the pattern: `{{evidence_id}}_{{date}}_{{descriptive_title}}`

## Security Notes

- Sensitive files should be placed in the classified directory structure
- Maintain chain of custody documentation
- Verify file integrity with hash values

---
*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

    def _create_gitkeep_files(self):
        """Create .gitkeep files to maintain directory structure in git"""
        folders = self.ems._generate_comprehensive_folder_structure()

        for folder in folders:
            gitkeep_path = f"{folder}/.gitkeep"
            os.makedirs(folder, exist_ok=True)

            # Only create .gitkeep if directory is empty
            if not os.listdir(folder):
                with open(gitkeep_path, "w") as f:
                    f.write(
                        f"# Keep this directory in version control\n# Created: {datetime.now().isoformat()}\n"
                    )

    def _get_documentation_files(self) -> List[str]:
        """Get list of created documentation files"""
        return [
            f"{self.ems.base_directory}/README.md",
            f"{self.ems.base_directory}/FOLDER_STRUCTURE.md",
            f"{self.ems.base_directory}/documents/README.md",
            f"{self.ems.base_directory}/communications/README.md",
            f"{self.ems.base_directory}/financial/README.md",
            f"{self.ems.base_directory}/technical/README.md",
            f"{self.ems.base_directory}/media/README.md",
        ]

    def export_structure_to_json(self, output_file: str = None) -> str:
        """Export folder structure to JSON file"""
        if not output_file:
            output_file = f"{self.ems.base_directory}/folder_structure.json"

        structure_data = self.generate_all_structures()

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(structure_data, f, indent=2, ensure_ascii=False)

        return output_file


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description="Evidence Management System Folder Structure Generator"
    )
    parser.add_argument(
        "--base-dir",
        "-b",
        default="/tmp/evidence_repository",
        help="Base directory for evidence repository",
    )
    parser.add_argument(
        "--output-dir", "-o", help="Output directory (if different from base-dir)"
    )
    parser.add_argument(
        "--visualize",
        "-v",
        action="store_true",
        help="Show folder structure visualization",
    )
    parser.add_argument(
        "--create-template",
        "-t",
        action="store_true",
        help="Create template folder structure with documentation",
    )
    parser.add_argument("--export-json", "-j", help="Export structure to JSON file")

    args = parser.parse_args()

    generator = FolderStructureGenerator(args.base_dir)

    if args.create_template:
        print("Creating template folder structure...")
        result = generator.create_template_structure(args.output_dir)
        print(f"✅ Template created successfully!")
        print(f"Base directory: {result['base_directory']}")
        print(f"Folders created: {result['folders_created']}")
        print(f"Documentation files: {len(result['documentation_files'])}")

    if args.visualize:
        print("\n📁 Folder Structure Visualization:")
        print("=" * 50)
        print(generator.ems.visualize_folder_structure())

    if args.export_json:
        print(f"\nExporting structure to {args.export_json}...")
        output_file = generator.export_structure_to_json(args.export_json)
        print(f"✅ Structure exported to: {output_file}")

    if not any([args.create_template, args.visualize, args.export_json]):
        # Default: show structure report
        print("📊 Folder Structure Report:")
        print("=" * 50)
        structure = generator.generate_all_structures()
        print(json.dumps(structure["base_structure"], indent=2))


if __name__ == "__main__":
    main()
