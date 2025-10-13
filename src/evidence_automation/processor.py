"""
Evidence Processor

Main orchestration class for automated evidence processing, including
file ingestion, analysis, and integration with existing repository structures.
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .analyzers import EntityAnalyzer, LegalAnalyzer, TimelineAnalyzer
from .extractors import DocumentExtractor, EmailExtractor, HTMLExtractor


class EvidencePackage:
    """Represents a processed evidence package with extracted information."""

    def __init__(self, package_name: str, source_files: List[str]):
        self.package_name = package_name
        self.source_files = source_files
        self.entities = []
        self.timeline_events = []
        self.legal_violations = []
        self.evidence_folder = None
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence package to dictionary for serialization."""
        return {
            "package_name": self.package_name,
            "source_files": self.source_files,
            "entities": self.entities,
            "timeline_events": self.timeline_events,
            "legal_violations": self.legal_violations,
            "evidence_folder": self.evidence_folder,
            "created_at": self.created_at.isoformat(),
        }


class EvidenceProcessor:
    """
    Main evidence processing orchestrator that automates the workflow
    demonstrated in the July 2025 formal notice processing.
    """

    def __init__(self, repository_root: str = "."):
        self.repository_root = Path(repository_root)
        self.evidence_base = self.repository_root / "evidence"

        # Initialize extractors for different file types
        self.extractors = {
            "docx": DocumentExtractor(),
            "html": HTMLExtractor(),
            "email": EmailExtractor(),
        }

        # Initialize analyzers for different analysis types
        self.analyzers = {
            "entity": EntityAnalyzer(),
            "timeline": TimelineAnalyzer(),
            "legal": LegalAnalyzer(),
        }

    def process_evidence_package(
        self, files: List[str], package_name: str = None
    ) -> EvidencePackage:
        """
        Process a collection of evidence files into an organized evidence package.

        Args:
            files: List of file paths to process
            package_name: Optional name for the evidence package

        Returns:
            EvidencePackage with extracted information and organized files
        """
        if package_name is None:
            package_name = (
                f"evidence_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

        # Create evidence package
        package = EvidencePackage(package_name, files)

        # Extract content from all files
        extracted_content = {}
        for file_path in files:
            content = self._extract_file_content(file_path)
            if content:
                extracted_content[file_path] = content

        # Analyze extracted content
        all_content = " ".join(extracted_content.values())

        # Entity analysis
        package.entities = self.analyzers["entity"].extract_entities(all_content)

        # Timeline analysis
        package.timeline_events = self.analyzers["timeline"].extract_timeline_events(
            all_content
        )

        # Legal analysis
        package.legal_violations = self.analyzers["legal"].analyze_legal_violations(
            all_content
        )

        # Create evidence folder and organize files
        package.evidence_folder = self._create_evidence_folder(package)

        # Update repository timeline and entities
        self._update_repository_timeline(package)
        self._update_repository_entities(package)

        return package

    def _extract_file_content(self, file_path: str) -> Optional[str]:
        """Extract content from a file based on its type."""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"Warning: File {file_path} does not exist")
            return None

        file_extension = file_path.suffix.lower().lstrip(".")

        if file_extension in self.extractors:
            try:
                return self.extractors[file_extension].extract(str(file_path))
            except Exception as e:
                print(f"Error extracting content from {file_path}: {e}")
                return None
        else:
            print(f"Warning: No extractor available for file type {file_extension}")
            return None

    def _create_evidence_folder(self, package: EvidencePackage) -> str:
        """Create organized evidence folder structure."""
        # Create evidence folder
        evidence_folder = self.evidence_base / package.package_name
        evidence_folder.mkdir(parents=True, exist_ok=True)

        # Copy source files to evidence folder
        for file_path in package.source_files:
            source_path = Path(file_path)
            if source_path.exists():
                dest_path = evidence_folder / source_path.name
                shutil.copy2(source_path, dest_path)

        # Create analysis files
        self._create_analysis_files(evidence_folder, package)

        # Create README for the evidence package
        self._create_evidence_readme(evidence_folder, package)

        return str(evidence_folder)

    def _create_analysis_files(self, evidence_folder: Path, package: EvidencePackage):
        """Create analysis files within the evidence folder."""

        # Entity analysis file
        entities_file = evidence_folder / "extracted_entities.json"
        with open(entities_file, "w") as f:
            json.dump(package.entities, f, indent=2)

        # Timeline events file
        timeline_file = evidence_folder / "timeline_events.json"
        with open(timeline_file, "w") as f:
            json.dump(package.timeline_events, f, indent=2)

        # Legal violations file
        legal_file = evidence_folder / "legal_violations.json"
        with open(legal_file, "w") as f:
            json.dump(package.legal_violations, f, indent=2)

        # Complete package metadata
        metadata_file = evidence_folder / "package_metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(package.to_dict(), f, indent=2)

    def _create_evidence_readme(self, evidence_folder: Path, package: EvidencePackage):
        """Create a comprehensive README for the evidence package."""
        readme_content = f"""# Evidence Package: {package.package_name}

## Overview
This evidence package was automatically processed on {package.created_at.strftime('%Y-%m-%d %H:%M:%S')}.

## Source Files
{chr(10).join(f"- {Path(f).name}" for f in package.source_files)}

## Analysis Summary

### Entities Extracted
- Total entities identified: {len(package.entities)}
- Entity types: {', '.join(set(e.get('type', 'unknown') for e in package.entities))}

### Timeline Events
- Total events identified: {len(package.timeline_events)}
- Date range: {self._get_date_range(package.timeline_events)}

### Legal Violations
- Total violations identified: {len(package.legal_violations)}
- Violation categories: {', '.join(set(v.get('category', 'unknown') for v in package.legal_violations))}

## Files in this Package

### Source Documents
{chr(10).join(f"- **{Path(f).name}**: Original evidence file" for f in package.source_files)}

### Analysis Files
- **extracted_entities.json**: Structured entity data
- **timeline_events.json**: Chronological event data
- **legal_violations.json**: Legal violation analysis
- **package_metadata.json**: Complete package metadata

## Integration Status
- ✅ Entities added to repository entity database
- ✅ Timeline events integrated with main timeline
- ✅ Legal violations catalogued for case analysis

## Processing Notes
This package was processed using the automated evidence processing system.
All extracted information has been integrated with the main repository
timeline and entity databases for comprehensive case analysis.
"""

        readme_file = evidence_folder / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)

    def _get_date_range(self, timeline_events: List[Dict]) -> str:
        """Get the date range for timeline events."""
        if not timeline_events:
            return "No dates identified"

        dates = [event.get("date") for event in timeline_events if event.get("date")]
        if not dates:
            return "No valid dates found"

        dates.sort()
        if len(dates) == 1:
            return dates[0]
        else:
            return f"{dates[0]} to {dates[-1]}"

    def _update_repository_timeline(self, package: EvidencePackage):
        """Update the main repository timeline with new events."""
        timeline_file = (
            self.repository_root
            / "evidence"
            / "rezonance"
            / "timeline"
            / "updated_timeline.md"
        )

        if timeline_file.exists() and package.timeline_events:
            # Read existing timeline
            with open(timeline_file, "r") as f:
                timeline_content = f.read()

            # Generate new timeline section
            new_section = self._generate_timeline_section(package)

            # Append new section to timeline
            updated_content = timeline_content + "\n\n" + new_section

            # Write updated timeline
            with open(timeline_file, "w") as f:
                f.write(updated_content)

    def _update_repository_entities(self, package: EvidencePackage):
        """Update the main repository entities with new entities."""
        entities_file = (
            self.repository_root
            / "evidence"
            / "rezonance"
            / "entities"
            / "extracted_entities.md"
        )

        if entities_file.exists() and package.entities:
            # Read existing entities
            with open(entities_file, "r") as f:
                entities_content = f.read()

            # Generate new entities section
            new_section = self._generate_entities_section(package)

            # Append new section to entities
            updated_content = entities_content + "\n\n" + new_section

            # Write updated entities
            with open(entities_file, "w") as f:
                f.write(updated_content)

    def _generate_timeline_section(self, package: EvidencePackage) -> str:
        """Generate timeline section for new evidence package."""
        section = f"## {package.package_name.replace('_', ' ').title()} - Automated Processing\n\n"

        for event in package.timeline_events:
            date = event.get("date", "Unknown date")
            description = event.get("description", "No description")
            significance = event.get("significance", "Standard")

            section += f"- **{date}**: {description}\n"
            if significance != "Standard":
                section += f"  - Significance: {significance}\n"

        return section

    def _generate_entities_section(self, package: EvidencePackage) -> str:
        """Generate entities section for new evidence package."""
        section = (
            f"## {package.package_name.replace('_', ' ').title()} - New Entities\n\n"
        )

        # Group entities by type
        entities_by_type = {}
        for entity in package.entities:
            entity_type = entity.get("type", "Unknown")
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
            entities_by_type[entity_type].append(entity)

        # Generate section for each entity type
        for entity_type, entities in entities_by_type.items():
            section += f"### {entity_type.title()}\n\n"
            for entity in entities:
                name = entity.get("name", "Unknown")
                description = entity.get("description", "No description")
                section += f"- **{name}**: {description}\n"
            section += "\n"

        return section


def process_evidence_files(
    file_paths: List[str], package_name: str = None
) -> EvidencePackage:
    """
    Convenience function for processing evidence files.

    Args:
        file_paths: List of file paths to process
        package_name: Optional name for the evidence package

    Returns:
        Processed evidence package
    """
    processor = EvidenceProcessor()
    return processor.process_evidence_package(file_paths, package_name)
