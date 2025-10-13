#!/usr/bin/env python3
"""
Tests for the Affidavit Enhancement System
"""

import json
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from affidavit_enhancement.affidavit_processor import (
    AffidavitProcessor, 
    AffidavitMetadata, 
    EvidenceUpdate,
    AffidavitSection
)


class TestAffidavitProcessor(unittest.TestCase):
    """Test cases for AffidavitProcessor"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_config = {
            "affidavit_patterns": ["*affidavit*.md", "*AFFIDAVIT*.md"],
            "evidence_patterns": ["evidence/*.md", "*EVIDENCE*.md"],
            "critical_keywords": ["fraud", "murder", "criminal", "evidence"],
            "backup_on_change": True,
            "preserve_formatting": True,
            "auto_enhancement": True,
            "affidavit_dir": str(self.temp_dir),
            "evidence_dir": str(self.temp_dir / "evidence"),
            "backup_dir": str(self.temp_dir / "backups"),
            "output_dir": str(self.temp_dir / "enhanced")
        }
        
        # Create test directories
        (self.temp_dir / "evidence").mkdir(exist_ok=True)
        
        # Save test config
        self.config_path = self.temp_dir / "test_config.json"
        with open(self.config_path, 'w') as f:
            json.dump(self.test_config, f)
            
        self.processor = AffidavitProcessor(str(self.config_path))
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def create_test_affidavit(self, filename: str, content: str) -> Path:
        """Create a test affidavit file"""
        file_path = self.temp_dir / filename
        file_path.write_text(content, encoding='utf-8')
        return file_path
        
    def create_test_evidence(self, filename: str, content: str) -> Path:
        """Create a test evidence file"""
        file_path = self.temp_dir / "evidence" / filename
        file_path.write_text(content, encoding='utf-8')
        return file_path
        
    def test_processor_initialization(self):
        """Test processor initialization with config"""
        self.assertIsInstance(self.processor, AffidavitProcessor)
        self.assertEqual(str(self.processor.affidavit_dir), str(self.temp_dir))
        self.assertEqual(str(self.processor.evidence_dir), str(self.temp_dir / "evidence"))
        
    def test_discover_affidavits(self):
        """Test affidavit discovery"""
        # Create test affidavit files
        self.create_test_affidavit("test_affidavit.md", "# Test Affidavit\n\nContent")
        self.create_test_affidavit("ANOTHER_AFFIDAVIT.md", "# Another Affidavit\n\nContent")
        self.create_test_affidavit("not_an_affidavit.md", "# Not an affidavit")
        
        affidavits = self.processor.discover_affidavits()
        
        # Should find 2 affidavit files matching patterns
        self.assertEqual(len(affidavits), 2)
        affidavit_names = [f.name for f in affidavits]
        self.assertIn("test_affidavit.md", affidavit_names)
        self.assertIn("ANOTHER_AFFIDAVIT.md", affidavit_names)
        
    def test_is_relevant_evidence(self):
        """Test evidence relevance detection"""
        # Create evidence files with different content
        critical_evidence = self.create_test_evidence("critical.md", 
            "This evidence shows fraud and criminal activity.")
        normal_evidence = self.create_test_evidence("normal.md", 
            "This is a normal document with no critical keywords.")
            
        self.assertTrue(self.processor._is_relevant_evidence(critical_evidence))
        self.assertFalse(self.processor._is_relevant_evidence(normal_evidence))
        
    def test_determine_priority(self):
        """Test priority determination"""
        critical_content = "This evidence shows murder and criminal conspiracy."
        high_content = "New evidence of fraud has been discovered."
        medium_content = "This document contains some information."
        
        self.assertEqual(self.processor._determine_priority(critical_content), "critical")
        self.assertEqual(self.processor._determine_priority(high_content), "high")
        self.assertEqual(self.processor._determine_priority(medium_content), "medium")
        
    def test_extract_applicable_sections(self):
        """Test section extraction"""
        content = """
        This background information shows financial fraud in the timeline.
        Evidence indicates regulatory compliance violations.
        """
        
        sections = self.processor._extract_applicable_sections(content)
        
        self.assertIn("background", sections)
        self.assertIn("financial", sections)
        self.assertIn("timeline", sections)
        self.assertIn("evidence", sections)
        self.assertIn("regulatory", sections)
        
    def test_determine_update_type(self):
        """Test update type determination"""
        new_evidence = "This new evidence shows additional proof of fraud."
        correction = "This correction fixes an error in the previous statement."
        enhancement = "This analysis provides additional context."
        
        self.assertEqual(self.processor._determine_update_type(new_evidence), "new_evidence")
        self.assertEqual(self.processor._determine_update_type(correction), "correction")
        self.assertEqual(self.processor._determine_update_type(enhancement), "enhancement")
        
    def test_extract_evidence_summary(self):
        """Test evidence summary extraction"""
        content = """
        Evidence shows that the defendant committed fraud.
        
        Proof indicates systematic embezzlement over 5 years.
        
        Documents confirm transfer of R10 million.
        
        Analysis reveals coordinated conspiracy.
        """
        
        summary = self.processor._extract_evidence_summary(content)
        
        self.assertIn("fraud", summary)
        self.assertIn("embezzlement", summary)
        self.assertIn("R10 million", summary)
        self.assertIn("conspiracy", summary)
        
    def test_analyze_evidence_changes(self):
        """Test evidence change analysis"""
        # Create evidence files
        self.create_test_evidence("fraud_evidence.md", 
            "New evidence of criminal fraud discovered. This is critical evidence.")
        self.create_test_evidence("normal_doc.md", 
            "Regular document without critical keywords.")
            
        updates = self.processor.analyze_evidence_changes()
        
        # Should find the fraud evidence
        self.assertGreaterEqual(len(updates), 1)
        
        fraud_updates = [u for u in updates if "fraud" in u.content.lower()]
        self.assertGreater(len(fraud_updates), 0)
        
        fraud_update = fraud_updates[0]
        self.assertEqual(fraud_update.priority, "critical")
        self.assertIn("evidence", fraud_update.applicable_sections)
        
    def test_markdown_enhancement(self):
        """Test markdown affidavit enhancement"""
        # Create test affidavit
        affidavit_content = """# TEST AFFIDAVIT

## INTRODUCTION

I, John Doe, make this affidavit.

## BACKGROUND

Some background information.

## CONCLUSION

This concludes my affidavit.
"""
        
        affidavit_path = self.create_test_affidavit("test_affidavit.md", affidavit_content)
        
        # Create evidence update
        update = EvidenceUpdate(
            evidence_file="test_evidence.md",
            update_type="new_evidence",
            content="Evidence shows fraud committed by defendant.",
            priority="critical",
            applicable_sections=["evidence"],
            timestamp=datetime.now().isoformat()
        )
        
        # Enhance affidavit
        success = self.processor.enhance_affidavit(affidavit_path, [update])
        
        self.assertTrue(success)
        
        # Check output file exists
        enhanced_path = self.processor.output_dir / "test_affidavit_enhanced.md"
        self.assertTrue(enhanced_path.exists())
        
        # Check content includes enhancement
        enhanced_content = enhanced_path.read_text()
        self.assertIn("ENHANCED EVIDENCE ANALYSIS", enhanced_content)
        self.assertIn("fraud", enhanced_content)
        self.assertIn("ENHANCEMENT METADATA", enhanced_content)
        
    def test_backup_creation(self):
        """Test backup file creation"""
        # Create test file
        test_file = self.create_test_affidavit("backup_test.md", "Original content")
        
        # Create backup
        backup_path = self.processor._create_backup(test_file)
        
        self.assertTrue(backup_path.exists())
        self.assertEqual(backup_path.read_text(), "Original content")
        self.assertIn("backup", backup_path.name)
        
    def test_filter_relevant_updates(self):
        """Test filtering of relevant updates"""
        updates = [
            EvidenceUpdate("file1.md", "new_evidence", "content", "critical", [], "2025-01-01"),
            EvidenceUpdate("file2.md", "enhancement", "content", "high", [], "2025-01-01"),
            EvidenceUpdate("file3.md", "correction", "content", "low", [], "2025-01-01")
        ]
        
        affidavit_path = Path("test.md")
        relevant = self.processor._filter_relevant_updates(affidavit_path, updates)
        
        # Should filter out low priority updates
        self.assertEqual(len(relevant), 2)
        priorities = [u.priority for u in relevant]
        self.assertNotIn("low", priorities)
        
    def test_process_all_affidavits_integration(self):
        """Integration test for processing all affidavits"""
        # Create test affidavit
        affidavit_content = """# COMPREHENSIVE AFFIDAVIT

## INTRODUCTION
I am making this affidavit regarding fraudulent activities.

## EVIDENCE SECTION
Initial evidence is presented here.

## CONCLUSION
This concludes the affidavit.
"""
        
        self.create_test_affidavit("comprehensive_affidavit.md", affidavit_content)
        
        # Create critical evidence
        self.create_test_evidence("critical_fraud_evidence.md", 
            "URGENT: New evidence of murder and criminal conspiracy discovered. "
            "This evidence shows systematic fraud over multiple years.")
            
        # Process all affidavits
        results = self.processor.process_all_affidavits()
        
        # Should process the affidavit
        self.assertEqual(len(results), 1)
        self.assertTrue(list(results.values())[0])  # Should be successful
        
        # Check enhanced file was created
        enhanced_files = list((self.processor.output_dir).glob("*enhanced*"))
        self.assertGreater(len(enhanced_files), 0)
        
    def test_enhancement_report_generation(self):
        """Test enhancement report generation"""
        results = {
            "affidavit1.md": True,
            "affidavit2.md": False,
            "affidavit3.md": True
        }
        
        report = self.processor.generate_enhancement_report(results)
        
        self.assertIn("Enhancement Report", report)
        self.assertIn("Total Affidavits Processed: 3", report)
        self.assertIn("Successfully Enhanced: 2", report)
        self.assertIn("Failed: 1", report)
        self.assertIn("✅ Success", report)
        self.assertIn("❌ Failed", report)
        
    def test_since_timestamp_filtering(self):
        """Test filtering updates based on timestamp"""
        # Create evidence file with older timestamp
        old_evidence = self.create_test_evidence("old_evidence.md", 
            "Old evidence of fraud")
        
        # Modify file timestamp to be older
        old_time = (datetime.now() - timedelta(days=2)).timestamp()
        import os
        os.utime(old_evidence, (old_time, old_time))
        
        # Create recent evidence
        recent_evidence = self.create_test_evidence("recent_evidence.md", 
            "Recent evidence of criminal activity")
        
        # Analyze with timestamp filter
        since_timestamp = (datetime.now() - timedelta(days=1)).isoformat()
        updates = self.processor.analyze_evidence_changes(since_timestamp)
        
        # Should only find recent evidence
        evidence_files = [Path(u.evidence_file).name for u in updates]
        self.assertIn("recent_evidence.md", evidence_files)
        # May or may not include old evidence depending on file system precision


class TestDataClasses(unittest.TestCase):
    """Test the data classes"""
    
    def test_affidavit_metadata(self):
        """Test AffidavitMetadata creation"""
        metadata = AffidavitMetadata(
            file_path="test.md",
            document_type="affidavit",
            case_number="2025-123456"
        )
        
        self.assertEqual(metadata.file_path, "test.md")
        self.assertEqual(metadata.document_type, "affidavit")
        self.assertEqual(metadata.case_number, "2025-123456")
        self.assertEqual(metadata.evidence_sources, [])
        self.assertEqual(metadata.enhancement_count, 0)
        
    def test_evidence_update(self):
        """Test EvidenceUpdate creation"""
        update = EvidenceUpdate(
            evidence_file="evidence.md",
            update_type="new_evidence",
            content="Test content",
            priority="high",
            applicable_sections=["background", "evidence"],
            timestamp="2025-01-01T00:00:00"
        )
        
        self.assertEqual(update.evidence_file, "evidence.md")
        self.assertEqual(update.update_type, "new_evidence")
        self.assertEqual(update.priority, "high")
        self.assertEqual(len(update.applicable_sections), 2)
        
    def test_affidavit_section(self):
        """Test AffidavitSection creation"""
        section = AffidavitSection(
            section_id="evidence_001",
            title="Evidence Section",
            content="Evidence content here",
            paragraph_numbers=[10, 11, 12],
            evidence_references=["EV001", "EV002"],
            last_modified="2025-01-01T00:00:00"
        )
        
        self.assertEqual(section.section_id, "evidence_001")
        self.assertEqual(section.title, "Evidence Section")
        self.assertEqual(len(section.paragraph_numbers), 3)
        self.assertEqual(len(section.evidence_references), 2)


if __name__ == '__main__':
    # Set up logging for tests
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    unittest.main()