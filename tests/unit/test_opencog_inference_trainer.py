#!/usr/bin/env python3
"""
Unit tests for Hyper-Holmes Inference Engine and Super-Sleuth Trainer
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from datetime import datetime

import pytest

from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, TruthValue
from frameworks.hyper_holmes_inference import (
    HyperHolmesInferenceEngine,
    InferenceRule,
    RuleType,
)
from frameworks.super_sleuth_trainer import (
    SuperSleuthTrainer,
    PatternCategory,
    LearnedPattern,
    InvestigationLead,
)


class TestHyperHolmesInferenceEngine:
    """Tests for Hyper-Holmes Inference Engine"""
    
    def test_inference_engine_creation(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        assert engine.atomspace == atomspace
        assert len(engine.rules) > 0  # Should have default rules
    
    def test_add_rule(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        
        initial_rules = len(engine.rules)
        
        custom_rule = InferenceRule(
            rule_id="test_rule",
            rule_type=RuleType.DEDUCTION,
            name="Test Rule",
            description="Test inference rule",
            premises=[{"atom_type": AtomType.ENTITY}],
            conclusion={"atom_type": AtomType.PATTERN, "name": "test_pattern"}
        )
        
        engine.add_rule(custom_rule)
        assert len(engine.rules) == initial_rules + 1
    
    def test_forward_chain(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        
        # Add some data
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        event = Atom(atom_id="event_001", atom_type=AtomType.EVENT, name="Test Event")
        atomspace.add_atom(entity)
        atomspace.add_atom(event)
        
        # Run inference
        result = engine.forward_chain(max_iterations=3)
        
        assert result["method"] == "forward_chain"
        assert result["iterations"] > 0
        assert result["total_inferences"] >= 0
    
    def test_detect_patterns(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        
        # Add test data
        entity1 = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Entity 1")
        entity2 = Atom(atom_id="entity_002", atom_type=AtomType.ENTITY, name="Entity 2")
        event1 = Atom(
            atom_id="event_001",
            atom_type=AtomType.EVENT,
            name="Event 1",
            metadata={"timestamp": datetime.now().isoformat()}
        )
        
        atomspace.add_atom(entity1)
        atomspace.add_atom(entity2)
        atomspace.add_atom(event1)
        
        # Detect patterns
        patterns = engine.detect_patterns()
        assert isinstance(patterns, list)
    
    def test_generate_hypotheses(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        
        # Add evidence
        evidence1 = Atom(
            atom_id="evidence_001",
            atom_type=AtomType.EVIDENCE,
            name="Evidence 1"
        )
        evidence2 = Atom(
            atom_id="evidence_002",
            atom_type=AtomType.EVIDENCE,
            name="Evidence 2"
        )
        
        atomspace.add_atom(evidence1)
        atomspace.add_atom(evidence2)
        
        # Generate hypotheses
        hypotheses = engine.generate_hypotheses(["evidence_001", "evidence_002"])
        assert isinstance(hypotheses, list)
        assert len(hypotheses) > 0
    
    def test_get_inference_statistics(self):
        atomspace = AtomSpace("test_case")
        engine = HyperHolmesInferenceEngine(atomspace)
        
        stats = engine.get_inference_statistics()
        assert "total_rules" in stats
        assert "total_inferences" in stats
        assert "atomspace_size" in stats


class TestSuperSleuthTrainer:
    """Tests for Super-Sleuth Trainer"""
    
    def test_trainer_creation(self):
        atomspace = AtomSpace("test_case")
        trainer = SuperSleuthTrainer(atomspace)
        assert trainer.atomspace == atomspace
        assert len(trainer.learned_patterns) == 0
        assert len(trainer.investigation_leads) == 0
    
    def test_train_on_case_data(self):
        atomspace = AtomSpace("test_case")
        trainer = SuperSleuthTrainer(atomspace)
        
        # Add test data
        entity1 = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="Entity 1",
            metadata={"entity_type": "organization"}
        )
        entity2 = Atom(
            atom_id="entity_002",
            atom_type=AtomType.ENTITY,
            name="Entity 2",
            metadata={"entity_type": "person"}
        )
        event1 = Atom(
            atom_id="event_001",
            atom_type=AtomType.EVENT,
            name="Event 1",
            metadata={"timestamp": datetime(2025, 1, 15).isoformat()}
        )
        relationship = atomspace.add_link(
            link_type=AtomType.RELATIONSHIP,
            name="connected",
            targets=["entity_001", "entity_002"]
        )
        
        atomspace.add_atom(entity1)
        atomspace.add_atom(entity2)
        atomspace.add_atom(event1)
        
        # Train
        summary = trainer.train_on_case_data()
        
        assert "training_timestamp" in summary
        assert "patterns_learned" in summary
        assert "leads_generated" in summary
        assert summary["patterns_learned"] > 0
    
    def test_introspect(self):
        atomspace = AtomSpace("test_case")
        trainer = SuperSleuthTrainer(atomspace)
        
        # Add minimal data
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        atomspace.add_atom(entity)
        
        # Introspect
        report = trainer.introspect()
        
        assert "introspection_timestamp" in report
        assert "knowledge_base_metrics" in report
        assert "investigation_leads" in report
        assert "knowledge_gaps" in report
        assert "recommendations" in report
    
    def test_learned_pattern_creation(self):
        pattern = LearnedPattern(
            pattern_id="test_pattern",
            category=PatternCategory.TEMPORAL,
            name="Test Pattern",
            description="Test description",
            frequency=5,
            confidence=0.8
        )
        
        assert pattern.pattern_id == "test_pattern"
        assert pattern.category == PatternCategory.TEMPORAL
        assert pattern.confidence == 0.8
        
        # Test to_dict
        d = pattern.to_dict()
        assert d["pattern_id"] == "test_pattern"
        assert d["category"] == "temporal"
    
    def test_investigation_lead_creation(self):
        lead = InvestigationLead(
            lead_id="test_lead",
            priority="HIGH",
            description="Test lead description",
            supporting_evidence=["evidence_001", "evidence_002"],
            recommended_actions=["Action 1", "Action 2"],
            confidence=0.85
        )
        
        assert lead.lead_id == "test_lead"
        assert lead.priority == "HIGH"
        assert len(lead.supporting_evidence) == 2
        assert len(lead.recommended_actions) == 2
        
        # Test to_dict
        d = lead.to_dict()
        assert d["lead_id"] == "test_lead"
        assert d["priority"] == "HIGH"


class TestInferenceRule:
    """Tests for InferenceRule"""
    
    def test_rule_creation(self):
        rule = InferenceRule(
            rule_id="test_rule",
            rule_type=RuleType.DEDUCTION,
            name="Test Rule",
            description="Test description",
            premises=[{"atom_type": AtomType.ENTITY}],
            conclusion={"atom_type": AtomType.PATTERN}
        )
        
        assert rule.rule_id == "test_rule"
        assert rule.rule_type == RuleType.DEDUCTION
        assert len(rule.premises) == 1
    
    def test_rule_applies_to(self):
        atomspace = AtomSpace("test_case")
        
        # Add entity
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        atomspace.add_atom(entity)
        
        # Create rule that requires an entity
        rule = InferenceRule(
            rule_id="test_rule",
            rule_type=RuleType.DEDUCTION,
            name="Test Rule",
            description="Test",
            premises=[{"atom_type": AtomType.ENTITY}],
            conclusion={"atom_type": AtomType.PATTERN}
        )
        
        # Rule should apply
        assert rule.applies_to(atomspace) == True
    
    def test_rule_apply(self):
        atomspace = AtomSpace("test_case")
        
        # Add entity
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        atomspace.add_atom(entity)
        
        # Create and apply rule
        rule = InferenceRule(
            rule_id="test_rule",
            rule_type=RuleType.DEDUCTION,
            name="Test Rule",
            description="Test",
            premises=[{"atom_type": AtomType.ENTITY}],
            conclusion={"atom_type": AtomType.PATTERN, "name": "test_pattern"}
        )
        
        inferred_atoms = rule.apply(atomspace)
        assert len(inferred_atoms) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
