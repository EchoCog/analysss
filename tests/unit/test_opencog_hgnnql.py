#!/usr/bin/env python3
"""
Unit tests for OpenCog HGNNQL Case-LLM components
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from datetime import datetime

import pytest

from frameworks.opencog_hgnnql import (
    Atom,
    AtomSpace,
    AtomType,
    CaseLLM,
    HGNNQLQueryEngine,
    Link,
    TruthValue,
)


class TestTruthValue:
    """Tests for TruthValue class"""
    
    def test_truth_value_creation(self):
        tv = TruthValue(strength=0.8, confidence=0.9)
        assert tv.strength == 0.8
        assert tv.confidence == 0.9
    
    def test_truth_value_bounds(self):
        # Test that values are bounded to [0, 1]
        tv = TruthValue(strength=1.5, confidence=-0.5)
        assert tv.strength == 1.0
        assert tv.confidence == 0.0
    
    def test_truth_value_to_dict(self):
        tv = TruthValue(strength=0.7, confidence=0.6)
        d = tv.to_dict()
        assert d["strength"] == 0.7
        assert d["confidence"] == 0.6


class TestAtom:
    """Tests for Atom class"""
    
    def test_atom_creation(self):
        atom = Atom(
            atom_id="test_001",
            atom_type=AtomType.ENTITY,
            name="Test Entity",
        )
        assert atom.atom_id == "test_001"
        assert atom.atom_type == AtomType.ENTITY
        assert atom.name == "Test Entity"
        assert isinstance(atom.truth_value, TruthValue)
    
    def test_atom_with_metadata(self):
        atom = Atom(
            atom_id="test_002",
            atom_type=AtomType.EVENT,
            name="Test Event",
            metadata={"timestamp": "2025-01-01", "type": "meeting"}
        )
        assert atom.metadata["timestamp"] == "2025-01-01"
        assert atom.metadata["type"] == "meeting"
    
    def test_atom_to_dict(self):
        atom = Atom(
            atom_id="test_003",
            atom_type=AtomType.CONCEPT,
            name="Test Concept",
        )
        d = atom.to_dict()
        assert d["atom_id"] == "test_003"
        assert d["atom_type"] == "concept"
        assert d["name"] == "Test Concept"


class TestAtomSpace:
    """Tests for AtomSpace class"""
    
    def test_atomspace_creation(self):
        atomspace = AtomSpace("test_case")
        assert atomspace.case_id == "test_case"
        assert len(atomspace.atoms) == 0
    
    def test_add_atom(self):
        atomspace = AtomSpace("test_case")
        atom = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="Test Entity",
        )
        atom_id = atomspace.add_atom(atom)
        assert atom_id == "entity_001"
        assert len(atomspace.atoms) == 1
    
    def test_get_atom(self):
        atomspace = AtomSpace("test_case")
        atom = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="Test Entity",
        )
        atomspace.add_atom(atom)
        retrieved = atomspace.get_atom("entity_001")
        assert retrieved is not None
        assert retrieved.name == "Test Entity"
    
    def test_get_atoms_by_type(self):
        atomspace = AtomSpace("test_case")
        
        # Add multiple atoms of different types
        entity1 = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Entity 1")
        entity2 = Atom(atom_id="entity_002", atom_type=AtomType.ENTITY, name="Entity 2")
        event1 = Atom(atom_id="event_001", atom_type=AtomType.EVENT, name="Event 1")
        
        atomspace.add_atom(entity1)
        atomspace.add_atom(entity2)
        atomspace.add_atom(event1)
        
        # Get entities
        entities = atomspace.get_atoms_by_type(AtomType.ENTITY)
        assert len(entities) == 2
        
        # Get events
        events = atomspace.get_atoms_by_type(AtomType.EVENT)
        assert len(events) == 1
    
    def test_add_link(self):
        atomspace = AtomSpace("test_case")
        
        # Add entities
        entity1 = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Entity 1")
        entity2 = Atom(atom_id="entity_002", atom_type=AtomType.ENTITY, name="Entity 2")
        atomspace.add_atom(entity1)
        atomspace.add_atom(entity2)
        
        # Add link
        link_id = atomspace.add_link(
            link_type=AtomType.RELATIONSHIP,
            name="connected_to",
            targets=["entity_001", "entity_002"]
        )
        
        assert link_id is not None
        link = atomspace.get_atom(link_id)
        assert isinstance(link, Link)
        assert len(link.targets) == 2
    
    def test_query(self):
        atomspace = AtomSpace("test_case")
        
        # Add atoms with different properties
        atom1 = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="High Confidence Entity",
            truth_value=TruthValue(strength=0.9, confidence=0.9)
        )
        atom2 = Atom(
            atom_id="entity_002",
            atom_type=AtomType.ENTITY,
            name="Low Confidence Entity",
            truth_value=TruthValue(strength=0.3, confidence=0.3)
        )
        
        atomspace.add_atom(atom1)
        atomspace.add_atom(atom2)
        
        # Query by type and confidence
        results = atomspace.query({
            "atom_type": AtomType.ENTITY,
            "min_confidence": 0.5
        })
        
        assert len(results) == 1
        assert results[0].name == "High Confidence Entity"


class TestHGNNQLQueryEngine:
    """Tests for HGNNQL Query Engine"""
    
    def test_query_engine_creation(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        assert engine.atomspace == atomspace
    
    def test_find_entities(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add entities
        entity = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="Test Entity",
            metadata={"entity_type": "person"}
        )
        atomspace.add_atom(entity)
        
        # Find all entities
        entities = engine.find_entities()
        assert len(entities) == 1
        
        # Find by type
        persons = engine.find_entities(entity_type="person")
        assert len(persons) == 1
    
    def test_execute_hgnnql_find(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add entities
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        atomspace.add_atom(entity)
        
        # Execute FIND query
        result = engine.execute_hgnnql("FIND ENTITY")
        assert result["command"] == "FIND"
        assert result["count"] == 1


class TestCaseLLM:
    """Tests for Case-LLM"""
    
    def test_case_llm_creation(self):
        atomspace = AtomSpace("test_case")
        llm = CaseLLM(atomspace)
        assert llm.atomspace == atomspace
        assert llm.embedding_dim == 768
    
    def test_embed_atom(self):
        atomspace = AtomSpace("test_case")
        llm = CaseLLM(atomspace)
        
        atom = Atom(
            atom_id="entity_001",
            atom_type=AtomType.ENTITY,
            name="Test Entity"
        )
        
        embedding = llm.embed_atom(atom)
        assert embedding is not None
        assert len(embedding) == 768
    
    def test_compute_similarity(self):
        atomspace = AtomSpace("test_case")
        llm = CaseLLM(atomspace)
        
        atom1 = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test 1")
        atom2 = Atom(atom_id="entity_002", atom_type=AtomType.ENTITY, name="Test 2")
        
        similarity = llm.compute_semantic_similarity(atom1, atom2)
        assert isinstance(similarity, float)
        assert -1.0 <= similarity <= 1.0
    
    def test_reason_about_case(self):
        atomspace = AtomSpace("test_case")
        llm = CaseLLM(atomspace)
        
        # Add some data
        entity = Atom(atom_id="entity_001", atom_type=AtomType.ENTITY, name="Test")
        atomspace.add_atom(entity)
        
        # Ask a question
        result = llm.reason_about_case("What entities are involved?")
        assert result["question"] == "What entities are involved?"
        assert "answer" in result
        assert "confidence" in result


class TestEnhancedHGNNQLOperations:
    """Tests for enhanced HGNNQL operations (LINK, INFER, QUERY, COUNT)"""
    
    def test_execute_hgnnql_link(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add test atoms
        atom1 = Atom(atom_id="alice", atom_type=AtomType.ENTITY, name="Alice")
        atom2 = Atom(atom_id="bob", atom_type=AtomType.ENTITY, name="Bob")
        atomspace.add_atom(atom1)
        atomspace.add_atom(atom2)
        
        result = engine.execute_hgnnql("LINK alice TO bob AS knows")
        assert result["command"] == "LINK"
        assert result["status"] == "success"
        assert result["relationship"] == "knows"
    
    def test_execute_hgnnql_count(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add test atoms
        atom1 = Atom(atom_id="entity1", atom_type=AtomType.ENTITY, name="Entity 1")
        atom2 = Atom(atom_id="entity2", atom_type=AtomType.ENTITY, name="Entity 2")
        atomspace.add_atom(atom1)
        atomspace.add_atom(atom2)
        
        result = engine.execute_hgnnql("COUNT ENTITY")
        assert result["command"] == "COUNT"
        assert result["count"] == 2
    
    def test_execute_hgnnql_infer(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add evidence atoms
        evidence1 = Atom(atom_id="evidence1", atom_type=AtomType.EVIDENCE, name="Evidence 1")
        evidence2 = Atom(atom_id="evidence2", atom_type=AtomType.EVIDENCE, name="Evidence 2")
        atomspace.add_atom(evidence1)
        atomspace.add_atom(evidence2)
        
        result = engine.execute_hgnnql("INFER fraud FROM evidence1 evidence2")
        assert result["command"] == "INFER"
        assert result["status"] == "success"
        assert result["pattern"] == "fraud"
    
    def test_execute_hgnnql_query_connected(self):
        atomspace = AtomSpace("test_case")
        engine = HGNNQLQueryEngine(atomspace)
        
        # Add atoms and create a link
        atom1 = Atom(atom_id="alice", atom_type=AtomType.ENTITY, name="Alice")
        atom2 = Atom(atom_id="bob", atom_type=AtomType.ENTITY, name="Bob")
        atomspace.add_atom(atom1)
        atomspace.add_atom(atom2)
        
        # Create link first
        engine.execute_hgnnql("LINK alice TO bob AS knows")
        
        # Query connected entities
        result = engine.execute_hgnnql("QUERY CONNECTED TO alice")
        assert result["command"] == "QUERY"
        assert result["query_type"] == "connected"
        assert result["connected_count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
