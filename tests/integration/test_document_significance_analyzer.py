#!/usr/bin/env python3
"""
Test suite for Document Significance Analyzer

Validates document significance analysis functionality and integration
with the interdict verification system.
"""

import unittest
import json
from datetime import datetime
from pathlib import Path
import sys

# Add tools directory to path
sys.path.append(str(Path(__file__).parent / "tools"))

from document_significance_analyzer import (
    DocumentSignificanceAnalyzer,
    DocumentSignificance
)


class TestDocumentSignificanceAnalyzer(unittest.TestCase):
    """Test cases for the document significance analyzer"""

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = DocumentSignificanceAnalyzer("2025-137857")
        
    def test_analyzer_initialization(self):
        """Test analyzer initializes correctly"""
        self.assertEqual(self.analyzer.case_number, "2025-137857")
        self.assertTrue(self.analyzer.case_path.exists())
        self.assertTrue(self.analyzer.documents_path.exists())
        self.assertEqual(len(self.analyzer.significance_analyses), 0)
        
    def test_file_hash_calculation(self):
        """Test file hash calculation functionality"""
        # Test with existing file
        test_file = Path(__file__)
        hash_result = self.analyzer.calculate_file_hash(test_file)
        self.assertNotEqual(hash_result, "")
        self.assertNotIn("ERROR", hash_result)
        self.assertEqual(len(hash_result), 64)  # SHA256 length
        
        # Test with non-existent file
        fake_file = Path("/tmp/nonexistent_file.txt")
        hash_result = self.analyzer.calculate_file_hash(fake_file)
        self.assertIn("ERROR_CALCULATING_HASH", hash_result)

    def test_mat4719_analysis(self):
        """Test MAT4719 document analysis"""
        # Create a dummy file for testing
        test_file = self.analyzer.documents_path / "3. MAT4719 - 01.10.25 - WP Letter to KE.pdf"
        
        if test_file.exists():
            significance = self.analyzer.analyze_mat4719_wp_letter(test_file)
            
            self.assertEqual(significance.document_type, "procedural")
            self.assertEqual(significance.significance_level, "critical")
            self.assertIn("Withdrawal of legal representation", significance.legal_implications[0])
            self.assertIn("service requirements", significance.procedural_impact[0])
            self.assertIn("attorney-client relationship", significance.evidence_value[0])
            self.assertIn("01.10.25", significance.timeline_relevance)
            self.assertTrue(len(significance.verification_requirements) > 0)

    def test_draft_response_analysis(self):
        """Test draft response document analysis"""
        test_file = self.analyzer.documents_path / "DRAFT OF MAIN POINTS - RESPONSE.docx"
        
        if test_file.exists():
            significance = self.analyzer.analyze_draft_main_points_response(test_file)
            
            self.assertEqual(significance.document_type, "legal_strategy")
            self.assertEqual(significance.significance_level, "high")
            self.assertIn("legal strategy", significance.legal_implications[0])
            self.assertIn("Draft status", significance.procedural_impact[0])
            self.assertIn("respondent's position", significance.evidence_value[0])

    def test_kf0019_analysis(self):
        """Test KF0019 second application analysis"""
        test_file = self.analyzer.documents_path / "KF0019 - Second Application - 03.10.2025.pdf"
        
        if test_file.exists():
            significance = self.analyzer.analyze_kf0019_second_application(test_file)
            
            self.assertEqual(significance.document_type, "procedural")
            self.assertEqual(significance.significance_level, "critical")
            self.assertIn("Second application", significance.legal_implications[0])
            self.assertIn("Multiple applications", significance.procedural_impact[0])
            self.assertIn("multiple application attempts", significance.evidence_value[0])
            self.assertIn("03.10.2025", significance.timeline_relevance)

    def test_bank_records_analysis(self):
        """Test bank records series analysis"""
        # Find existing bank record files
        bank_files = list(self.analyzer.documents_path.glob("D_FAUCITT_PERSONAL_BANK_RECORDS*.pdf"))
        
        if bank_files:
            significance = self.analyzer.analyze_bank_records_series(bank_files)
            
            self.assertEqual(significance.document_type, "financial")
            self.assertEqual(significance.significance_level, "critical")
            self.assertIn("Personal bank records", significance.legal_implications[0])
            self.assertIn("Admissibility requirements", significance.procedural_impact[0])
            self.assertIn("Direct financial evidence", significance.evidence_value[0])
            self.assertIn("2025", significance.timeline_relevance)
            self.assertIn("R500K", significance.evidence_value[3])
            
            # Should have multiple file hashes separated by semicolons
            self.assertIn(";", significance.file_hash)

    def test_verification_usage_analysis(self):
        """Test interdict verification usage document analysis"""
        test_file = self.analyzer.documents_path / "interdict_verification_usage.md"
        
        if test_file.exists():
            significance = self.analyzer.analyze_interdict_verification_usage(test_file)
            
            self.assertEqual(significance.document_type, "procedural")
            self.assertEqual(significance.significance_level, "high")
            self.assertIn("systematic approach", significance.legal_implications[0])
            self.assertIn("framework", significance.procedural_impact[0])
            self.assertIn("verification system", significance.evidence_value[0])

    def test_document_significance_structure(self):
        """Test DocumentSignificance dataclass structure"""
        # Create a test significance object
        significance = DocumentSignificance(
            document_path="/test/path",
            document_type="test_type", 
            significance_level="high",
            legal_implications=["test implication"],
            procedural_impact=["test impact"],
            evidence_value=["test evidence"],
            timeline_relevance="test timeline",
            cross_references=["test ref"],
            verification_requirements=["test requirement"],
            analysis_date=datetime.now(),
            file_hash="test_hash"
        )
        
        # Verify all fields are accessible
        self.assertEqual(significance.document_path, "/test/path")
        self.assertEqual(significance.document_type, "test_type")
        self.assertEqual(significance.significance_level, "high")
        self.assertEqual(len(significance.legal_implications), 1)
        self.assertEqual(len(significance.procedural_impact), 1)
        self.assertEqual(len(significance.evidence_value), 1)

    def test_verification_system_integration(self):
        """Test integration with verification system"""
        # Create a mock significance analysis
        mock_significance = DocumentSignificance(
            document_path="/test/document.pdf",
            document_type="procedural",
            significance_level="critical", 
            legal_implications=["Test legal implication"],
            procedural_impact=["Test procedural impact"],
            evidence_value=["Test evidence value"],
            timeline_relevance="Test timeline",
            cross_references=["test_ref"],
            verification_requirements=["Test requirement"],
            analysis_date=datetime.now(),
            file_hash="test_hash_123"
        )
        
        # Add to analyzer
        self.analyzer.significance_analyses["test_document.pdf"] = mock_significance
        
        # Test integration
        self.analyzer.integrate_with_verification_system(
            {"test_document.pdf": mock_significance}
        )
        
        # Verify evidence was added to verification system
        evidence_items = self.analyzer.verification_system.evidence_repository
        self.assertGreater(len(evidence_items), 0)
        
        # Find our evidence item
        evidence_item = None
        for item in evidence_items.values():
            if "test_document.pdf" in item.source_document:
                evidence_item = item
                break
                
        self.assertIsNotNone(evidence_item)
        self.assertEqual(evidence_item.reliability_score, 0.95)
        self.assertIn("critical", evidence_item.content_summary)

    def test_report_generation(self):
        """Test comprehensive report generation"""
        # Add a test analysis
        mock_significance = DocumentSignificance(
            document_path="/test/document.pdf",
            document_type="financial",
            significance_level="high",
            legal_implications=["Financial implication"],
            procedural_impact=["Procedural impact"],
            evidence_value=["Evidence value"], 
            timeline_relevance="Test timeline",
            cross_references=["test_ref"],
            verification_requirements=["Test requirement"],
            analysis_date=datetime.now(),
            file_hash="test_hash_456"
        )
        
        self.analyzer.significance_analyses["test_doc.pdf"] = mock_significance
        
        # Generate report
        report = self.analyzer.generate_comprehensive_significance_report()
        
        # Verify report content
        self.assertIn("Document Significance Analysis Report", report)
        self.assertIn("2025-137857", report)
        self.assertIn("High Significance**: 1 documents", report)
        self.assertIn("Financial Evidence**: 1", report)
        self.assertIn("test_doc.pdf", report)
        self.assertIn("Financial implication", report)
        self.assertIn("test_hash_456", report)


class TestDocumentProcessingIntegration(unittest.TestCase):
    """Integration tests with actual case documents"""

    def setUp(self):
        """Set up integration test fixtures"""
        self.analyzer = DocumentSignificanceAnalyzer("2025-137857")

    def test_case_documents_exist(self):
        """Verify that target case documents exist"""
        target_documents = [
            "3. MAT4719 - 01.10.25 - WP Letter to KE.pdf",
            "DRAFT OF MAIN POINTS - RESPONSE.docx",
            "KF0019 - Second Application - 03.10.2025.pdf", 
            "interdict_verification_usage.md"
        ]
        
        existing_docs = []
        for doc in target_documents:
            doc_path = self.analyzer.documents_path / doc
            if doc_path.exists():
                existing_docs.append(doc)
                
        # At least some documents should exist
        self.assertGreater(len(existing_docs), 0, 
                          f"No target documents found in {self.analyzer.documents_path}")

    def test_bank_records_exist(self):
        """Test that bank record files exist"""
        bank_record_pattern = "D_FAUCITT_PERSONAL_BANK_RECORDS*.pdf"
        bank_files = list(self.analyzer.documents_path.glob(bank_record_pattern))
        
        self.assertGreater(len(bank_files), 0, 
                          f"No bank record files found matching {bank_record_pattern}")
        
        # Should have 5 files as specified in problem statement
        expected_files = 5
        self.assertEqual(len(bank_files), expected_files,
                        f"Expected {expected_files} bank record files, found {len(bank_files)}")

    def test_full_processing_workflow(self):
        """Test the complete document processing workflow"""
        # Define target documents
        target_documents = [
            "3. MAT4719 - 01.10.25 - WP Letter to KE.pdf",
            "DRAFT OF MAIN POINTS - RESPONSE.docx",
            "KF0019 - Second Application - 03.10.2025.pdf", 
            "interdict_verification_usage.md"
        ]
        
        # Add bank records
        bank_files = list(self.analyzer.documents_path.glob("D_FAUCITT_PERSONAL_BANK_RECORDS*.pdf"))
        target_documents.extend([f.name for f in bank_files])
        
        # Process documents (only test if documents exist)
        existing_docs = [
            doc for doc in target_documents 
            if (self.analyzer.documents_path / doc).exists()
        ]
        
        if existing_docs:
            # Run the processing
            significance_analyses = self.analyzer.process_document_significance(existing_docs)
            
            # Verify results
            self.assertGreater(len(significance_analyses), 0)
            
            # All analyses should be DocumentSignificance objects
            for analysis in significance_analyses.values():
                self.assertIsInstance(analysis, DocumentSignificance)
                self.assertIn(analysis.significance_level, ["critical", "high", "medium", "low"])
                self.assertIn(analysis.document_type, ["procedural", "financial", "legal_strategy", "evidence"])
                self.assertTrue(len(analysis.legal_implications) > 0)
                self.assertTrue(len(analysis.verification_requirements) > 0)

    def test_analysis_output_files(self):
        """Test that analysis output files are created correctly"""
        output_path = self.analyzer.case_path / "document_significance_analysis"
        
        # Check if analysis has been run (files exist)
        json_file = output_path / "significance_analysis.json"
        report_file = output_path / "significance_analysis_report.md"
        
        if json_file.exists() and report_file.exists():
            # Verify JSON structure
            with open(json_file) as f:
                json_data = json.load(f)
                
            self.assertIsInstance(json_data, dict)
            
            for doc_name, analysis_data in json_data.items():
                # Verify required fields
                required_fields = [
                    "document_path", "document_type", "significance_level",
                    "legal_implications", "procedural_impact", "evidence_value",
                    "timeline_relevance", "analysis_date", "file_hash"
                ]
                
                for field in required_fields:
                    self.assertIn(field, analysis_data, 
                                f"Missing field '{field}' in analysis for {doc_name}")
            
            # Verify report content
            with open(report_file) as f:
                report_content = f.read()
                
            self.assertIn("Document Significance Analysis Report", report_content)
            self.assertIn("2025-137857", report_content)
            self.assertIn("Executive Summary", report_content)
            self.assertIn("Integration Recommendations", report_content)


def run_tests():
    """Run all tests"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocumentSignificanceAnalyzer))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDocumentProcessingIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)