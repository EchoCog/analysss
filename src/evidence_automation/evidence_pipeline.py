#!/usr/bin/env python3
"""
Automated Evidence Processing Pipeline

Provides automated evidence ingestion, entity extraction, and timeline integration.
"""

import json
import logging
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class EvidenceMetadata:
    """Metadata for evidence items."""

    evidence_id: str
    file_path: str
    file_type: str
    date_received: str
    date_created: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None
    entities_extracted: List[str] = None
    timeline_events: List[str] = None
    compliance_violations: List[str] = None
    processing_status: str = "pending"

    def __post_init__(self):
        if self.entities_extracted is None:
            self.entities_extracted = []
        if self.timeline_events is None:
            self.timeline_events = []
        if self.compliance_violations is None:
            self.compliance_violations = []


@dataclass
class ExtractedEntity:
    """Extracted entity from evidence."""

    entity_type: str  # person, organization, location, date, etc.
    entity_value: str
    confidence: float
    context: str
    source_evidence: str


@dataclass
class TimelineEvent:
    """Timeline event extracted from evidence."""

    event_date: str
    event_type: str
    description: str
    entities_involved: List[str]
    evidence_source: str
    confidence: float


class EvidenceProcessor:
    """
    Automated evidence processing with entity extraction and timeline integration.
    """

    def __init__(self, evidence_dir: str, output_dir: str):
        """
        Initialize evidence processor.

        Args:
            evidence_dir: Directory containing evidence files
            output_dir: Directory for processed output
        """
        self.evidence_dir = Path(evidence_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.processed_evidence: List[EvidenceMetadata] = []
        self.extracted_entities: List[ExtractedEntity] = []
        self.timeline_events: List[TimelineEvent] = []

    def process_evidence_file(
        self, file_path: str, evidence_type: str = "document"
    ) -> EvidenceMetadata:
        """
        Process a single evidence file.

        Args:
            file_path: Path to evidence file
            evidence_type: Type of evidence

        Returns:
            Evidence metadata
        """
        logger.info(f"Processing evidence file: {file_path}")

        file_path_obj = Path(file_path)

        # Create evidence metadata
        evidence_id = self._generate_evidence_id(file_path_obj)
        metadata = EvidenceMetadata(
            evidence_id=evidence_id,
            file_path=str(file_path_obj),
            file_type=file_path_obj.suffix,
            date_received=datetime.now().isoformat(),
            processing_status="processing",
        )

        try:
            # Extract text content
            text_content = self._extract_text(file_path_obj)

            # Extract entities
            entities = self._extract_entities(text_content, evidence_id)
            metadata.entities_extracted = [e.entity_value for e in entities]
            self.extracted_entities.extend(entities)

            # Extract timeline events
            events = self._extract_timeline_events(text_content, evidence_id)
            metadata.timeline_events = [e.description for e in events]
            self.timeline_events.extend(events)

            # Detect compliance violations
            violations = self._detect_compliance_violations(text_content)
            metadata.compliance_violations = violations

            # Update status
            metadata.processing_status = "completed"

            logger.info(f"Successfully processed evidence: {evidence_id}")
            logger.info(f"  - Entities: {len(entities)}")
            logger.info(f"  - Timeline events: {len(events)}")
            logger.info(f"  - Compliance violations: {len(violations)}")

        except Exception as e:
            logger.error(f"Error processing evidence {evidence_id}: {e}")
            metadata.processing_status = "failed"

        self.processed_evidence.append(metadata)
        return metadata

    def process_evidence_directory(self) -> List[EvidenceMetadata]:
        """
        Process all evidence files in directory.

        Returns:
            List of evidence metadata
        """
        logger.info(f"Processing evidence directory: {self.evidence_dir}")

        evidence_files = []

        # Find all evidence files
        for ext in [".pdf", ".txt", ".doc", ".docx", ".eml", ".msg"]:
            evidence_files.extend(self.evidence_dir.rglob(f"*{ext}"))

        logger.info(f"Found {len(evidence_files)} evidence files")

        for file_path in evidence_files:
            self.process_evidence_file(str(file_path))

        return self.processed_evidence

    def _generate_evidence_id(self, file_path: Path) -> str:
        """
        Generate unique evidence ID.

        Args:
            file_path: Path to evidence file

        Returns:
            Evidence ID
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = file_path.stem
        return f"EVD_{timestamp}_{file_name}"

    def _extract_text(self, file_path: Path) -> str:
        """
        Extract text content from file.

        Args:
            file_path: Path to file

        Returns:
            Extracted text
        """
        # Simple text extraction (would use proper libraries in production)
        if file_path.suffix == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

        elif file_path.suffix == ".pdf":
            # Would use PyPDF2 or pdfplumber in production
            logger.warning(f"PDF extraction not implemented: {file_path}")
            return ""

        elif file_path.suffix in [".doc", ".docx"]:
            # Would use python-docx in production
            logger.warning(f"Word document extraction not implemented: {file_path}")
            return ""

        else:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return ""

    def _extract_entities(self, text: str, evidence_id: str) -> List[ExtractedEntity]:
        """
        Extract entities from text.

        Args:
            text: Text content
            evidence_id: Evidence identifier

        Returns:
            List of extracted entities
        """
        entities = []

        # Extract dates (simple pattern matching)
        date_pattern = r"\b\d{4}-\d{2}-\d{2}\b|\b\d{2}/\d{2}/\d{4}\b"
        dates = re.findall(date_pattern, text)

        for date in dates:
            entities.append(
                ExtractedEntity(
                    entity_type="date",
                    entity_value=date,
                    confidence=0.9,
                    context=self._get_context(text, date),
                    source_evidence=evidence_id,
                )
            )

        # Extract email addresses
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        emails = re.findall(email_pattern, text)

        for email in emails:
            entities.append(
                ExtractedEntity(
                    entity_type="email",
                    entity_value=email,
                    confidence=0.95,
                    context=self._get_context(text, email),
                    source_evidence=evidence_id,
                )
            )

        # Extract names (simplified - would use NER in production)
        # Common South African names
        name_patterns = [
            r"\b(Daniel|Peter|Jacqui|Kent|Sage)\s+[A-Z][a-z]+\b",
            r"\b[A-Z][a-z]+\s+(Faucitt|RegimA)\b",
        ]

        for pattern in name_patterns:
            names = re.findall(pattern, text)
            for name in names:
                if isinstance(name, tuple):
                    name = " ".join(name)

                entities.append(
                    ExtractedEntity(
                        entity_type="person",
                        entity_value=name,
                        confidence=0.8,
                        context=self._get_context(text, name),
                        source_evidence=evidence_id,
                    )
                )

        # Extract organizations
        org_keywords = ["RegimA", "Sage", "Shopify", "RWD", "Rezonance"]
        for org in org_keywords:
            if org in text:
                entities.append(
                    ExtractedEntity(
                        entity_type="organization",
                        entity_value=org,
                        confidence=0.9,
                        context=self._get_context(text, org),
                        source_evidence=evidence_id,
                    )
                )

        return entities

    def _extract_timeline_events(
        self, text: str, evidence_id: str
    ) -> List[TimelineEvent]:
        """
        Extract timeline events from text.

        Args:
            text: Text content
            evidence_id: Evidence identifier

        Returns:
            List of timeline events
        """
        events = []

        # Look for date + action patterns
        event_patterns = [
            r"(\d{4}-\d{2}-\d{2})[:\s]+(.*?)(?:\n|$)",
            r"On\s+(\d{2}/\d{2}/\d{4})[,\s]+(.*?)(?:\.|$)",
        ]

        for pattern in event_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)

            for date, description in matches:
                # Extract entities from description
                entities = self._extract_entities(description, evidence_id)
                entity_values = [e.entity_value for e in entities]

                events.append(
                    TimelineEvent(
                        event_date=date,
                        event_type="extracted",
                        description=description.strip(),
                        entities_involved=entity_values,
                        evidence_source=evidence_id,
                        confidence=0.7,
                    )
                )

        return events

    def _detect_compliance_violations(self, text: str) -> List[str]:
        """
        Detect compliance violations in text.

        Args:
            text: Text content

        Returns:
            List of detected violations
        """
        violations = []

        # POPI Act violations
        popi_keywords = [
            "personal information",
            "data breach",
            "unauthorized access",
            "consent",
            "privacy violation",
        ]

        for keyword in popi_keywords:
            if keyword.lower() in text.lower():
                violations.append(f"POPI Act - {keyword}")

        # Fraud indicators
        fraud_keywords = [
            "fraudulent",
            "misrepresentation",
            "unauthorized transfer",
            "identity theft",
            "forgery",
        ]

        for keyword in fraud_keywords:
            if keyword.lower() in text.lower():
                violations.append(f"Fraud - {keyword}")

        return violations

    def _get_context(self, text: str, term: str, window: int = 50) -> str:
        """
        Get context around a term in text.

        Args:
            text: Full text
            term: Term to find context for
            window: Characters before/after term

        Returns:
            Context string
        """
        try:
            idx = text.find(term)
            if idx == -1:
                return ""

            start = max(0, idx - window)
            end = min(len(text), idx + len(term) + window)

            return text[start:end].strip()

        except Exception:
            return ""

    def export_results(self):
        """Export processing results to files."""

        # Export evidence metadata
        metadata_file = self.output_dir / "evidence_metadata.json"
        with open(metadata_file, "w") as f:
            json.dump([asdict(m) for m in self.processed_evidence], f, indent=2)
        logger.info(f"Evidence metadata exported to: {metadata_file}")

        # Export extracted entities
        entities_file = self.output_dir / "extracted_entities.json"
        with open(entities_file, "w") as f:
            json.dump([asdict(e) for e in self.extracted_entities], f, indent=2)
        logger.info(f"Extracted entities exported to: {entities_file}")

        # Export timeline events
        timeline_file = self.output_dir / "timeline_events.json"
        with open(timeline_file, "w") as f:
            json.dump([asdict(e) for e in self.timeline_events], f, indent=2)
        logger.info(f"Timeline events exported to: {timeline_file}")

        # Create summary report
        self._create_summary_report()

    def _create_summary_report(self):
        """Create summary report of processing results."""

        report_lines = [
            "# Evidence Processing Summary",
            f"\n**Generated:** {datetime.now().isoformat()}",
            f"\n## Overview\n",
            f"- **Total Evidence Files:** {len(self.processed_evidence)}",
            f"- **Successfully Processed:** {sum(1 for e in self.processed_evidence if e.processing_status == 'completed')}",
            f"- **Failed:** {sum(1 for e in self.processed_evidence if e.processing_status == 'failed')}",
            f"- **Total Entities Extracted:** {len(self.extracted_entities)}",
            f"- **Total Timeline Events:** {len(self.timeline_events)}",
            "\n## Entity Breakdown\n",
        ]

        # Count entities by type
        entity_counts = {}
        for entity in self.extracted_entities:
            entity_counts[entity.entity_type] = (
                entity_counts.get(entity.entity_type, 0) + 1
            )

        for entity_type, count in sorted(entity_counts.items()):
            report_lines.append(f"- **{entity_type.title()}:** {count}")

        report_lines.append("\n## Compliance Violations\n")

        # Count compliance violations
        all_violations = []
        for evidence in self.processed_evidence:
            all_violations.extend(evidence.compliance_violations)

        violation_counts = {}
        for violation in all_violations:
            violation_counts[violation] = violation_counts.get(violation, 0) + 1

        for violation, count in sorted(violation_counts.items()):
            report_lines.append(f"- **{violation}:** {count} occurrences")

        report_content = "\n".join(report_lines)

        report_file = self.output_dir / "processing_summary.md"
        with open(report_file, "w") as f:
            f.write(report_content)

        logger.info(f"Summary report created: {report_file}")


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.info("Evidence Processing Pipeline loaded")
