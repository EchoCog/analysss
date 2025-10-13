#!/usr/bin/env python3
"""
Unit tests for evidence processing pipeline.
"""

import pytest
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from evidence_automation.evidence_pipeline import (
    EvidenceProcessor,
    EvidenceMetadata,
    ExtractedEntity,
    TimelineEvent
)


class TestEvidenceMetadata:
    """Test cases for EvidenceMetadata dataclass."""
    
    def test_initialization(self):
        """Test metadata initialization."""
        metadata = EvidenceMetadata(
            evidence_id="EVD_001",
            file_path="/path/to/file.pdf",
            file_type=".pdf",
            date_received="2025-10-12"
        )
        
        assert metadata.evidence_id == "EVD_001"
        assert metadata.file_path == "/path/to/file.pdf"
        assert metadata.entities_extracted == []
        assert metadata.timeline_events == []
        assert metadata.compliance_violations == []
    
    def test_initialization_with_lists(self):
        """Test metadata initialization with provided lists."""
        metadata = EvidenceMetadata(
            evidence_id="EVD_002",
            file_path="/path/to/file.txt",
            file_type=".txt",
            date_received="2025-10-12",
            entities_extracted=["Entity1", "Entity2"],
            timeline_events=["Event1"],
            compliance_violations=["Violation1"]
        )
        
        assert len(metadata.entities_extracted) == 2
        assert len(metadata.timeline_events) == 1
        assert len(metadata.compliance_violations) == 1


class TestExtractedEntity:
    """Test cases for ExtractedEntity dataclass."""
    
    def test_initialization(self):
        """Test entity initialization."""
        entity = ExtractedEntity(
            entity_type="person",
            entity_value="John Doe",
            confidence=0.95,
            context="John Doe signed the document",
            source_evidence="EVD_001"
        )
        
        assert entity.entity_type == "person"
        assert entity.entity_value == "John Doe"
        assert entity.confidence == 0.95


class TestTimelineEvent:
    """Test cases for TimelineEvent dataclass."""
    
    def test_initialization(self):
        """Test timeline event initialization."""
        event = TimelineEvent(
            event_date="2025-10-12",
            event_type="document_signed",
            description="Contract signed by parties",
            entities_involved=["John Doe", "Jane Smith"],
            evidence_source="EVD_001",
            confidence=0.9
        )
        
        assert event.event_date == "2025-10-12"
        assert len(event.entities_involved) == 2


class TestEvidenceProcessor:
    """Test cases for EvidenceProcessor class."""
    
    @pytest.fixture
    def temp_evidence_dir(self, tmp_path):
        """Create temporary evidence directory."""
        evidence_dir = tmp_path / "evidence"
        evidence_dir.mkdir()
        return evidence_dir
    
    @pytest.fixture
    def temp_output_dir(self, tmp_path):
        """Create temporary output directory."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        return output_dir
    
    @pytest.fixture
    def processor(self, temp_evidence_dir, temp_output_dir):
        """Create evidence processor instance."""
        return EvidenceProcessor(
            str(temp_evidence_dir),
            str(temp_output_dir)
        )
    
    def test_initialization(self, processor, temp_evidence_dir, temp_output_dir):
        """Test processor initialization."""
        assert processor.evidence_dir == Path(temp_evidence_dir)
        assert processor.output_dir == Path(temp_output_dir)
        assert processor.processed_evidence == []
        assert processor.extracted_entities == []
        assert processor.timeline_events == []
    
    def test_generate_evidence_id(self, processor):
        """Test evidence ID generation."""
        file_path = Path("/path/to/document.pdf")
        evidence_id = processor._generate_evidence_id(file_path)
        
        assert "EVD_" in evidence_id
        assert "document" in evidence_id
    
    def test_extract_text_from_txt(self, processor, temp_evidence_dir):
        """Test text extraction from .txt file."""
        # Create test file
        test_file = temp_evidence_dir / "test.txt"
        test_content = "This is a test document with some content."
        test_file.write_text(test_content)
        
        extracted = processor._extract_text(test_file)
        
        assert extracted == test_content
    
    def test_extract_entities_dates(self, processor):
        """Test date entity extraction."""
        text = "The event occurred on 2025-10-12 and was followed by another on 01/15/2025."
        entities = processor._extract_entities(text, "EVD_TEST")
        
        date_entities = [e for e in entities if e.entity_type == "date"]
        assert len(date_entities) >= 1
        assert any("2025-10-12" in e.entity_value for e in date_entities)
    
    def test_extract_entities_emails(self, processor):
        """Test email entity extraction."""
        text = "Contact john.doe@example.com or jane.smith@company.org for more info."
        entities = processor._extract_entities(text, "EVD_TEST")
        
        email_entities = [e for e in entities if e.entity_type == "email"]
        assert len(email_entities) == 2
        assert any("john.doe@example.com" in e.entity_value for e in email_entities)
    
    def test_extract_entities_persons(self, processor):
        """Test person entity extraction."""
        text = "Daniel Faucitt and Peter Faucitt were involved in the transaction."
        entities = processor._extract_entities(text, "EVD_TEST")
        
        person_entities = [e for e in entities if e.entity_type == "person"]
        assert len(person_entities) >= 1
    
    def test_extract_entities_organizations(self, processor):
        """Test organization entity extraction."""
        text = "RegimA and Sage were the primary vendors. Shopify handled payments."
        entities = processor._extract_entities(text, "EVD_TEST")
        
        org_entities = [e for e in entities if e.entity_type == "organization"]
        assert len(org_entities) >= 2
        assert any("RegimA" in e.entity_value for e in org_entities)
        assert any("Sage" in e.entity_value for e in org_entities)
    
    def test_extract_timeline_events(self, processor):
        """Test timeline event extraction."""
        text = """
        2025-10-12: Contract signed by all parties
        On 01/15/2025, the payment was processed
        """
        events = processor._extract_timeline_events(text, "EVD_TEST")
        
        assert len(events) >= 1
        assert any("2025-10-12" in e.event_date for e in events)
    
    def test_detect_compliance_violations_popi(self, processor):
        """Test POPI Act violation detection."""
        text = "There was unauthorized access to personal information without consent."
        violations = processor._detect_compliance_violations(text)
        
        popi_violations = [v for v in violations if "POPI" in v]
        assert len(popi_violations) >= 1
    
    def test_detect_compliance_violations_fraud(self, processor):
        """Test fraud violation detection."""
        text = "The transaction involved fraudulent misrepresentation and identity theft."
        violations = processor._detect_compliance_violations(text)
        
        fraud_violations = [v for v in violations if "Fraud" in v]
        assert len(fraud_violations) >= 1
    
    def test_get_context(self, processor):
        """Test context extraction around term."""
        text = "This is a long document. The important term is here. More text follows."
        context = processor._get_context(text, "important term", window=20)
        
        assert "important term" in context
        assert len(context) <= 60  # term + 2*window
    
    def test_process_evidence_file(self, processor, temp_evidence_dir):
        """Test processing a single evidence file."""
        # Create test file
        test_file = temp_evidence_dir / "evidence.txt"
        test_content = """
        Evidence Document
        Date: 2025-10-12
        Contact: john.doe@example.com
        
        RegimA was involved in unauthorized access to personal information.
        Daniel Faucitt signed the agreement on 01/15/2025.
        """
        test_file.write_text(test_content)
        
        metadata = processor.process_evidence_file(str(test_file))
        
        assert metadata.processing_status == "completed"
        assert len(metadata.entities_extracted) > 0
        assert len(metadata.compliance_violations) > 0
    
    def test_process_evidence_directory(self, processor, temp_evidence_dir):
        """Test processing entire evidence directory."""
        # Create multiple test files
        for i in range(3):
            test_file = temp_evidence_dir / f"evidence_{i}.txt"
            test_file.write_text(f"Evidence document {i} with date 2025-10-{12+i}")
        
        results = processor.process_evidence_directory()
        
        assert len(results) == 3
        assert all(m.processing_status == "completed" for m in results)
    
    def test_export_results(self, processor, temp_output_dir):
        """Test exporting processing results."""
        # Add some test data
        processor.processed_evidence.append(
            EvidenceMetadata(
                evidence_id="EVD_TEST",
                file_path="/test/file.txt",
                file_type=".txt",
                date_received="2025-10-12",
                processing_status="completed"
            )
        )
        
        processor.extracted_entities.append(
            ExtractedEntity(
                entity_type="person",
                entity_value="Test Person",
                confidence=0.9,
                context="Test context",
                source_evidence="EVD_TEST"
            )
        )
        
        processor.export_results()
        
        # Check that files were created
        assert (temp_output_dir / "evidence_metadata.json").exists()
        assert (temp_output_dir / "extracted_entities.json").exists()
        assert (temp_output_dir / "timeline_events.json").exists()
        assert (temp_output_dir / "processing_summary.md").exists()
    
    def test_create_summary_report(self, processor, temp_output_dir):
        """Test summary report creation."""
        # Add test data
        processor.processed_evidence.append(
            EvidenceMetadata(
                evidence_id="EVD_001",
                file_path="/test/file.txt",
                file_type=".txt",
                date_received="2025-10-12",
                processing_status="completed",
                compliance_violations=["POPI Act - unauthorized access"]
            )
        )
        
        processor.extracted_entities.extend([
            ExtractedEntity("person", "John Doe", 0.9, "context", "EVD_001"),
            ExtractedEntity("email", "john@example.com", 0.95, "context", "EVD_001")
        ])
        
        processor._create_summary_report()
        
        report_file = temp_output_dir / "processing_summary.md"
        assert report_file.exists()
        
        content = report_file.read_text()
        assert "Evidence Processing Summary" in content
        assert "Total Evidence Files" in content
        assert "Entity Breakdown" in content
        assert "Compliance Violations" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

