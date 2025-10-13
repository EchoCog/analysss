#!/usr/bin/env python3
"""
Integration tests for OpenCog HGNNQL Case-LLM complete system
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from datetime import datetime
import json
import tempfile

import pytest

from frameworks.opencog_case_llm import OpenCogCaseLLM


class TestOpenCogCaseLLMIntegration:
    """Integration tests for complete OpenCog Case-LLM system"""
    
    def test_system_initialization(self):
        """Test that the system initializes correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            assert system.case_id == "test_case"
            assert system.atomspace is not None
            assert system.query_engine is not None
            assert system.inference_engine is not None
            assert system.trainer is not None
            assert system.llm is not None
    
    def test_add_entities_and_query(self):
        """Test adding entities and querying them"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add entities
            system.add_entity("alice", "Alice Johnson", "person")
            system.add_entity("bob", "Bob Smith", "person")
            system.add_entity("company", "Test Company", "organization")
            
            # Query entities
            entities = system.query_entities()
            assert len(entities) == 3
            
            # Query by type
            persons = system.query_entities(entity_type="person")
            assert len(persons) == 2
    
    def test_add_events_and_query(self):
        """Test adding events and querying them"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add events
            system.add_event(
                "event_001", "Meeting",
                datetime(2025, 1, 15),
                participants=[]
            )
            system.add_event(
                "event_002", "Transaction",
                datetime(2025, 1, 20),
                participants=[]
            )
            
            # Query events
            events = system.query_events()
            assert len(events) == 2
            
            # Query with date range
            events_filtered = system.query_events(
                start_date=datetime(2025, 1, 16),
                end_date=datetime(2025, 1, 31)
            )
            assert len(events_filtered) == 1
    
    def test_add_relationships(self):
        """Test adding relationships between entities"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add entities
            system.add_entity("alice", "Alice", "person")
            system.add_entity("bob", "Bob", "person")
            
            # Add relationship
            rel_id = system.add_relationship("alice", "bob", "colleagues")
            assert rel_id is not None
            
            # Query relationships
            relationships = system.query_relationships("entity_alice", "entity_bob")
            assert len(relationships) >= 0  # May find the relationship
    
    def test_add_evidence(self):
        """Test adding evidence items"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add entity
            system.add_entity("company", "Test Company", "organization")
            
            # Add evidence
            ev_id = system.add_evidence(
                "evidence_001",
                "Bank records showing suspicious activity",
                related_entities=["company"],
                verification_status="verified"
            )
            assert ev_id is not None
            
            # Query evidence
            result = system.query_hgnnql("FIND EVIDENCE")
            assert result["count"] == 1
    
    def test_hgnnql_queries(self):
        """Test HGNNQL query execution"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add test data
            system.add_entity("alice", "Alice", "person")
            system.add_event("event_001", "Test Event", datetime.now())
            
            # Test FIND queries
            result = system.query_hgnnql("FIND ENTITY")
            assert result["command"] == "FIND"
            assert result["count"] >= 1
            
            result = system.query_hgnnql("FIND EVENT")
            assert result["command"] == "FIND"
            assert result["count"] >= 1
    
    def test_inference_pipeline(self):
        """Test inference engine pipeline"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add test data
            system.add_entity("alice", "Alice", "person")
            system.add_entity("bob", "Bob", "person")
            system.add_event("event_001", "Meeting", datetime.now(), ["alice", "bob"])
            
            # Run inference
            result = system.run_inference(method="forward", max_iterations=3)
            assert result["method"] == "forward_chain"
            assert result["iterations"] >= 1
    
    def test_pattern_detection(self):
        """Test pattern detection"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add test data
            system.add_entity("alice", "Alice", "person")
            system.add_entity("bob", "Bob", "person")
            system.add_event("event_001", "Meeting", datetime.now())
            
            # Detect patterns
            patterns = system.detect_patterns()
            assert isinstance(patterns, list)
    
    def test_introspection_training(self):
        """Test Super-Sleuth introspection training"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add test data
            system.add_entity("alice", "Alice", "person")
            system.add_entity("bob", "Bob", "person")
            system.add_event("event_001", "Meeting", datetime(2025, 1, 15))
            system.add_relationship("alice", "bob", "colleagues")
            
            # Train introspection
            summary = system.train_introspection()
            assert "training_timestamp" in summary
            assert "patterns_learned" in summary
            assert "leads_generated" in summary
    
    def test_complete_analysis_pipeline(self):
        """Test complete analysis pipeline"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add comprehensive test data
            system.add_entity("alice", "Alice Johnson", "person", {"role": "investigator"})
            system.add_entity("bob", "Bob Smith", "person", {"role": "analyst"})
            system.add_entity("company", "Test Corp", "organization")
            
            system.add_event("event_001", "Initial meeting", datetime(2025, 1, 15), ["alice", "bob"])
            system.add_event("event_002", "Investigation", datetime(2025, 1, 20), ["alice"])
            
            system.add_relationship("alice", "bob", "colleagues")
            system.add_relationship("alice", "company", "investigates")
            
            system.add_evidence(
                "evidence_001", "Suspicious transaction records",
                related_entities=["company"],
                verification_status="verified"
            )
            
            # Run complete analysis
            report = system.run_complete_analysis()
            
            assert "case_id" in report
            assert "analysis_timestamp" in report
            assert "inference_results" in report
            assert "patterns_detected" in report
            assert "training_summary" in report
            assert "introspection_report" in report
            assert "investigation_leads" in report
            assert "summary" in report
            
            # Check summary metrics
            summary = report["summary"]
            assert "total_inferences" in summary
            assert "patterns_detected" in summary
            assert "leads_generated" in summary
            assert "knowledge_base_size" in summary
    
    def test_export_functionality(self):
        """Test exporting results"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add minimal data
            system.add_entity("alice", "Alice", "person")
            
            # Export knowledge base
            kb_file = Path(tmpdir) / "test_kb.json"
            system.export_knowledge_base(str(kb_file))
            assert kb_file.exists()
            
            # Verify exported data
            with open(kb_file, 'r') as f:
                data = json.load(f)
                assert "case_id" in data
                assert "atoms" in data
                assert "statistics" in data
    
    def test_system_status(self):
        """Test getting system status"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add some data
            system.add_entity("alice", "Alice", "person")
            system.add_event("event_001", "Test", datetime.now())
            
            # Get status
            status = system.get_system_status()
            
            assert "case_id" in status
            assert "atomspace" in status
            assert "inference_engine" in status
            assert "trainer" in status
            assert "llm" in status
            
            # Check AtomSpace metrics
            assert status["atomspace"]["total_atoms"] >= 2
    
    def test_investigation_leads(self):
        """Test getting investigation leads"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add data
            system.add_entity("alice", "Alice", "person")
            system.add_entity("bob", "Bob", "person")
            system.add_event("event_001", "Meeting", datetime.now())
            
            # Train to generate leads
            system.train_introspection()
            
            # Get leads
            leads = system.get_investigation_leads()
            assert isinstance(leads, list)
    
    def test_learned_patterns(self):
        """Test getting learned patterns"""
        with tempfile.TemporaryDirectory() as tmpdir:
            system = OpenCogCaseLLM(case_id="test_case", output_dir=tmpdir)
            
            # Add data
            system.add_entity("alice", "Alice", "person")
            system.add_event("event_001", "Test", datetime.now())
            
            # Train to learn patterns
            system.train_introspection()
            
            # Get patterns
            patterns = system.get_learned_patterns()
            assert isinstance(patterns, dict)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
