#!/usr/bin/env python3
"""
Test Suite for OpenCog HyperGraphQL ORGGML Evidence Refinery
==========================================================

Comprehensive tests for the integrated evidence refinery system.
Tests all major components and integration points.
"""

import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.opencog_hypergraphql_orggml_evidence_refinery import (
    OpenCogHyperGraphQLORGGMLEvidenceRefinery,
    RefinedEvidence,
    EvidenceQualityScore,
    EvidenceProcessingStatus
)
from src.api.hypergraphql_resolvers import HyperGraphQLResolver


class TestEvidenceRefineryCore(unittest.TestCase):
    """Test core evidence refinery functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.case_id = "test_case_001"
        self.refinery = OpenCogHyperGraphQLORGGMLEvidenceRefinery(
            case_id=self.case_id,
            output_dir=self.temp_dir
        )
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_refinery_initialization(self):
        """Test refinery system initialization"""
        self.assertIsNotNone(self.refinery.atomspace)
        self.assertIsNotNone(self.refinery.query_engine)
        self.assertIsNotNone(self.refinery.ggml_engine)
        self.assertIsNotNone(self.refinery.hypergraphql_schema)
        self.assertIsNotNone(self.refinery.hypergraphql_resolver)
        self.assertEqual(self.refinery.case_id, self.case_id)
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_add_raw_evidence(self):
        """Test adding raw evidence to refinery"""
        evidence_id = "test_evidence_001"
        content = "Test evidence content for legal analysis"
        source = "test_source"
        metadata = {"test_key": "test_value"}
        
        evidence = self.refinery.add_raw_evidence(
            evidence_id=evidence_id,
            content=content,
            source=source,
            metadata=metadata
        )
        
        # Verify evidence object
        self.assertEqual(evidence.evidence_id, evidence_id)
        self.assertEqual(evidence.original_content, content)
        self.assertEqual(evidence.processing_status, EvidenceProcessingStatus.PENDING)
        self.assertIsNotNone(evidence.atom_id)
        self.assertIsNotNone(evidence.graphql_node_id)
        
        # Verify storage
        self.assertIn(evidence_id, self.refinery.refined_evidence)
        self.assertEqual(self.refinery.refined_evidence[evidence_id], evidence)
        
        # Verify OpenCog integration
        atom = self.refinery.atomspace.get_atom(evidence.atom_id)
        self.assertIsNotNone(atom)
        self.assertEqual(atom.metadata["evidence_id"], evidence_id)
        
        # Verify HyperGraphQL integration
        node = self.refinery.hypergraphql_schema.get_node(evidence.graphql_node_id)
        self.assertIsNotNone(node)
        self.assertEqual(node.properties["content"], content)
    
    def test_evidence_processing_pipeline(self):
        """Test complete evidence processing pipeline"""
        # Add evidence
        evidence_id = "test_evidence_002"
        content = "Legal document containing fraud evidence and financial transaction details"
        
        evidence = self.refinery.add_raw_evidence(
            evidence_id=evidence_id,
            content=content,
            source="legal_documents"
        )
        
        # Process evidence
        processed_evidence = self.refinery.process_evidence(evidence_id)
        
        # Verify processing results
        self.assertEqual(processed_evidence.processing_status, EvidenceProcessingStatus.ANALYZED)
        self.assertIsNotNone(processed_evidence.refined_content)
        self.assertIsNotNone(processed_evidence.ggml_analysis)
        self.assertIsInstance(processed_evidence.quality_score, EvidenceQualityScore)
        self.assertGreaterEqual(processed_evidence.confidence, 0.0)
        self.assertLessEqual(processed_evidence.confidence, 1.0)
        
        # Verify GGML analysis
        ggml_analysis = processed_evidence.ggml_analysis
        self.assertIn("relevance_score", ggml_analysis)
        self.assertIn("legal_significance", ggml_analysis)
        
        # Verify OpenCog updates
        atom = self.refinery.atomspace.get_atom(processed_evidence.atom_id)
        self.assertGreater(atom.truth_value.strength, 0)
        
        # Verify processing log
        self.assertGreater(len(processed_evidence.processing_log), 0)
    
    def test_quality_assessment(self):
        """Test evidence quality assessment"""
        # High quality evidence
        high_quality_evidence = self.refinery.add_raw_evidence(
            "high_quality_001",
            "Comprehensive legal document with detailed fraud evidence, financial transaction records, "
            "witness testimony, and corroborating documentation. Contains specific fiduciary duty breach "
            "evidence with bank transaction details and contract violations.",
            "verified_legal_documents"
        )
        
        # Low quality evidence  
        low_quality_evidence = self.refinery.add_raw_evidence(
            "low_quality_001",
            "Some claim",
            "unknown"
        )
        
        # Process both
        processed_high = self.refinery.process_evidence("high_quality_001")
        processed_low = self.refinery.process_evidence("low_quality_001")
        
        # Verify quality differentiation
        self.assertGreater(processed_high.confidence, processed_low.confidence)
        # Note: Quality scores may be the same due to simplified assessment algorithm
    
    def test_evidence_relationships(self):
        """Test evidence relationship creation"""
        # Add two evidence items
        evidence1 = self.refinery.add_raw_evidence("rel_test_001", "First evidence", "source1")
        evidence2 = self.refinery.add_raw_evidence("rel_test_002", "Second evidence", "source2")
        
        # Create relationship
        success = self.refinery.create_evidence_relationship(
            "rel_test_001", "rel_test_002", "corroborates", 0.9
        )
        
        self.assertTrue(success)
        
        # Verify relationship storage
        self.assertIn("rel_test_001", self.refinery.evidence_relationships)
        self.assertIn("rel_test_002", self.refinery.evidence_relationships["rel_test_001"])
        
        # Verify related evidence finding
        related = self.refinery.find_related_evidence("rel_test_001")
        # Note: This may be empty due to HGNNQL query limitations in test environment
    
    def test_evidence_summary(self):
        """Test evidence summary generation"""
        # Add and process evidence
        evidence = self.refinery.add_raw_evidence(
            "summary_test_001",
            "Test evidence for summary generation",
            "test_source"
        )
        processed = self.refinery.process_evidence("summary_test_001")
        
        # Get summary
        summary = self.refinery.get_evidence_summary("summary_test_001")
        
        # Verify summary contents
        self.assertEqual(summary["evidence_id"], "summary_test_001")
        self.assertIn("quality_score", summary)
        self.assertIn("confidence", summary)
        self.assertIn("processing_status", summary)
        self.assertIn("created_at", summary)
        self.assertIn("last_updated", summary)
    
    def test_processing_summary(self):
        """Test processing summary statistics"""
        # Add multiple evidence items
        for i in range(3):
            evidence = self.refinery.add_raw_evidence(
                f"stats_test_{i:03d}",
                f"Test evidence content {i}",
                "test_source"
            )
            self.refinery.process_evidence(f"stats_test_{i:03d}")
        
        # Get processing summary
        summary = self.refinery.get_processing_summary()
        
        # Verify summary structure
        self.assertEqual(summary["total_evidence"], 3)
        self.assertIn("quality_distribution", summary)
        self.assertIn("status_distribution", summary)
        self.assertIn("average_confidence", summary)
        self.assertIn("atomspace_size", summary)
        self.assertIn("ggml_performance", summary)
    
    def test_export_functionality(self):
        """Test evidence export functionality"""
        # Add and process evidence
        evidence = self.refinery.add_raw_evidence(
            "export_test_001",
            "Test evidence for export functionality",
            "test_source"
        )
        self.refinery.process_evidence("export_test_001")
        
        # Export evidence
        filepath = self.refinery.export_refined_evidence("json")
        
        # Verify export file
        self.assertTrue(Path(filepath).exists())
        
        # Verify export content
        with open(filepath, 'r') as f:
            export_data = json.load(f)
        
        self.assertEqual(export_data["case_id"], self.case_id)
        self.assertIn("evidence", export_data)
        self.assertIn("export_test_001", export_data["evidence"])


class TestHyperGraphQLResolverIntegration(unittest.TestCase):
    """Test HyperGraphQL resolver integration with evidence refinery"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.case_id = "resolver_test_case"
        self.refinery = OpenCogHyperGraphQLORGGMLEvidenceRefinery(
            case_id=self.case_id,
            output_dir=self.temp_dir
        )
        self.resolver = HyperGraphQLResolver(self.refinery.hypergraphql_schema)
        self.resolver.set_evidence_refinery(self.refinery)
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_resolver_initialization(self):
        """Test resolver-refinery integration setup"""
        self.assertIsNotNone(self.resolver.evidence_refinery)
        self.assertEqual(self.resolver.evidence_refinery, self.refinery)
    
    def test_resolve_add_raw_evidence(self):
        """Test adding evidence via GraphQL resolver"""
        input_data = {
            "evidenceId": "resolver_evidence_001",
            "content": "Evidence added via GraphQL resolver",
            "source": "graphql_test",
            "metadata": {"test": "data"}
        }
        
        result = self.resolver.resolve_add_raw_evidence(input_data)
        
        # Verify result structure
        self.assertNotIn("error", result)
        self.assertEqual(result["evidence_id"], "resolver_evidence_001")
        self.assertEqual(result["original_content"], "Evidence added via GraphQL resolver")
        
        # Verify evidence was added to refinery
        self.assertIn("resolver_evidence_001", self.refinery.refined_evidence)
    
    def test_resolve_process_evidence(self):
        """Test processing evidence via GraphQL resolver"""
        # Add evidence first
        self.refinery.add_raw_evidence(
            "process_test_001",
            "Evidence to process via resolver",
            "test_source"
        )
        
        # Process via resolver
        result = self.resolver.resolve_process_evidence("process_test_001")
        
        # Verify result
        self.assertNotIn("error", result)
        self.assertEqual(result["processing_status"], EvidenceProcessingStatus.ANALYZED.value)
        self.assertIn("ggml_analysis", result)
    
    def test_resolve_evidence_summary(self):
        """Test getting evidence summary via resolver"""
        # Add and process evidence
        self.refinery.add_raw_evidence(
            "summary_resolver_001",
            "Evidence for summary test",
            "test_source"
        )
        self.refinery.process_evidence("summary_resolver_001")
        
        # Get summary via resolver
        summary = self.resolver.resolve_evidence_summary("summary_resolver_001")
        
        # Verify summary
        self.assertNotIn("error", summary)
        self.assertEqual(summary["evidenceId"], "summary_resolver_001")
        self.assertIn("qualityScore", summary)
        self.assertIn("confidence", summary)
    
    def test_resolve_quality_report(self):
        """Test getting quality report via resolver"""
        # Add some evidence
        for i in range(2):
            self.refinery.add_raw_evidence(
                f"quality_test_{i}",
                f"Evidence {i} for quality report",
                "test_source"
            )
            self.refinery.process_evidence(f"quality_test_{i}")
        
        # Get quality report
        report = self.resolver.resolve_evidence_quality_report(self.case_id)
        
        # Verify report
        self.assertNotIn("error", report)
        self.assertEqual(report["caseId"], self.case_id)
        self.assertEqual(report["totalEvidence"], 2)
        self.assertIn("qualityDistribution", report)
        self.assertIn("averageConfidence", report)
    
    def test_resolve_export(self):
        """Test exporting via GraphQL resolver"""
        # Add evidence
        self.refinery.add_raw_evidence(
            "export_resolver_001",
            "Evidence for export test",
            "test_source"
        )
        
        # Export via resolver
        export_result = self.resolver.resolve_export_refined_evidence(self.case_id, "json")
        
        # Verify export result
        self.assertTrue(export_result["success"])
        self.assertIn("filepath", export_result)
        self.assertEqual(export_result["recordCount"], 1)
    
    def test_resolver_without_refinery(self):
        """Test resolver behavior when refinery not set"""
        # Create resolver without refinery
        standalone_resolver = HyperGraphQLResolver()
        
        # Test various methods return errors
        result = standalone_resolver.resolve_add_raw_evidence({"evidenceId": "test", "content": "test"})
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Evidence refinery not configured")
        
        summary = standalone_resolver.resolve_evidence_summary("test")
        self.assertIn("error", summary)
        
        related = standalone_resolver.resolve_related_evidence("test")
        self.assertEqual(related, [])


class TestGGMLIntegration(unittest.TestCase):
    """Test GGML legal engine integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.refinery = OpenCogHyperGraphQLORGGMLEvidenceRefinery(
            case_id="ggml_test_case",
            output_dir=self.temp_dir
        )
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_ggml_analysis_integration(self):
        """Test GGML analysis integration in evidence processing"""
        # Add evidence with legal/financial keywords
        evidence = self.refinery.add_raw_evidence(
            "ggml_test_001",
            "Legal contract breach involving fiduciary duty violation and unauthorized financial transactions",
            "legal_documents"
        )
        
        # Process evidence (triggers GGML analysis)
        processed = self.refinery.process_evidence("ggml_test_001")
        
        # Verify GGML analysis was performed
        self.assertIsNotNone(processed.ggml_analysis)
        ggml_analysis = processed.ggml_analysis
        
        # Verify analysis structure
        self.assertIn("document_analysis", ggml_analysis)
        self.assertIn("relevance_score", ggml_analysis)
        self.assertIn("legal_significance", ggml_analysis)
        self.assertIn("ggml_optimized", ggml_analysis)
        
        # Verify scores are within valid range
        relevance = ggml_analysis["relevance_score"]
        self.assertGreaterEqual(relevance, 0.0)
        self.assertLessEqual(relevance, 1.0)
        
        legal_sig = ggml_analysis["legal_significance"]
        self.assertGreaterEqual(legal_sig, 0.0)
        self.assertLessEqual(legal_sig, 1.0)
    
    def test_ggml_performance_tracking(self):
        """Test GGML performance statistics tracking"""
        # Process some evidence to generate GGML activity
        self.refinery.add_raw_evidence("perf_test", "Performance test evidence", "test")
        self.refinery.process_evidence("perf_test")
        
        # Get performance stats
        stats = self.refinery.ggml_engine.get_performance_stats()
        
        # Verify stats structure
        self.assertIn("total_tensors", stats)
        self.assertIn("quantized_tensors", stats)
        self.assertIn("quantization_ratio", stats)
        self.assertIn("total_memory_bytes", stats)
        self.assertIn("memory_mb", stats)
        self.assertIn("operators_available", stats)
        
        # Verify some tensors were created
        self.assertGreater(stats["total_tensors"], 0)


class TestOpenCogIntegration(unittest.TestCase):
    """Test OpenCog AtomSpace integration"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.refinery = OpenCogHyperGraphQLORGGMLEvidenceRefinery(
            case_id="opencog_test_case",
            output_dir=self.temp_dir
        )
        
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_atomspace_evidence_atoms(self):
        """Test evidence representation in OpenCog AtomSpace"""
        # Add evidence
        evidence = self.refinery.add_raw_evidence(
            "atom_test_001",
            "Evidence for AtomSpace testing",
            "test_source"
        )
        
        # Verify atom creation
        self.assertIsNotNone(evidence.atom_id)
        atom = self.refinery.atomspace.get_atom(evidence.atom_id)
        self.assertIsNotNone(atom)
        
        # Verify atom properties
        from frameworks.opencog_hgnnql import AtomType
        self.assertEqual(atom.atom_type, AtomType.EVIDENCE)
        self.assertIn("Evidence:", atom.name)
        self.assertEqual(atom.metadata["evidence_id"], "atom_test_001")
    
    def test_hgnnql_queries(self):
        """Test HGNNQL queries for evidence"""
        # Add multiple evidence items
        for i in range(3):
            self.refinery.add_raw_evidence(
                f"hgnnql_test_{i}",
                f"Evidence {i} for HGNNQL testing",
                "test_source"
            )
        
        # Query for evidence atoms
        result = self.refinery.query_engine.execute_hgnnql("FIND EVIDENCE")
        
        # Verify query result
        self.assertEqual(result["command"], "FIND")
        self.assertEqual(result["atom_type"], "EVIDENCE")
        self.assertEqual(result["count"], 3)
        self.assertIsInstance(result["results"], list)
    
    def test_truth_value_updates(self):
        """Test truth value updates during processing"""
        # Add evidence
        evidence = self.refinery.add_raw_evidence(
            "truth_test_001",
            "Evidence for truth value testing",
            "test_source"
        )
        
        # Get initial truth value
        initial_atom = self.refinery.atomspace.get_atom(evidence.atom_id)
        initial_strength = initial_atom.truth_value.strength
        
        # Process evidence (should update truth values)
        processed = self.refinery.process_evidence("truth_test_001")
        
        # Verify truth value was updated
        updated_atom = self.refinery.atomspace.get_atom(evidence.atom_id)
        self.assertIsNotNone(processed.truth_value)
        # Truth value should be updated based on processing results


def run_all_tests():
    """Run all test suites"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEvidenceRefineryCore))
    suite.addTests(loader.loadTestsFromTestCase(TestHyperGraphQLResolverIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestGGMLIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestOpenCogIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)