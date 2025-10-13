#!/usr/bin/env python3
"""
OpenCog HGNNQL (HyperGraph Neural Network Query Language) Integration
====================================================================

This module implements OpenCog-inspired knowledge representation and reasoning
using HyperGraph Neural Networks (HGNN) as the underlying Case-LLM.

Key Components:
1. AtomSpace-like knowledge representation using hypergraphs
2. HGNNQL query interface for case analysis
3. Inference engine integration (Hyper-Holmes)
4. Introspection trainer integration (Super-Sleuth)

The system represents case knowledge as a hypergraph where:
- Nodes represent entities, events, and concepts
- Hyperedges represent relationships and patterns
- LLM embeddings enable semantic reasoning
- Inference rules enable automated deduction
"""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AtomType(Enum):
    """Types of atoms in the knowledge hypergraph"""
    CONCEPT = "concept"
    PREDICATE = "predicate"
    ENTITY = "entity"
    EVENT = "event"
    RELATIONSHIP = "relationship"
    PATTERN = "pattern"
    EVIDENCE = "evidence"
    INFERENCE = "inference"


class TruthValue:
    """
    Represents the truth value of an atom with confidence.
    Similar to OpenCog's probabilistic truth values.
    """
    def __init__(self, strength: float = 0.5, confidence: float = 0.5):
        """
        Initialize truth value.
        
        Args:
            strength: Probability that the atom is true (0.0 to 1.0)
            confidence: Confidence in the strength estimate (0.0 to 1.0)
        """
        self.strength = max(0.0, min(1.0, strength))
        self.confidence = max(0.0, min(1.0, confidence))
    
    def __repr__(self):
        return f"TV({self.strength:.3f}, {self.confidence:.3f})"
    
    def to_dict(self):
        return {"strength": self.strength, "confidence": self.confidence}


@dataclass
class Atom:
    """
    Basic unit of knowledge in the HGNNQL system.
    Represents concepts, entities, relationships, or patterns.
    """
    atom_id: str
    atom_type: AtomType
    name: str
    truth_value: TruthValue = field(default_factory=lambda: TruthValue())
    embedding: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    incoming: Set[str] = field(default_factory=set)  # Atoms pointing to this
    outgoing: Set[str] = field(default_factory=set)  # Atoms this points to
    
    def __hash__(self):
        return hash(self.atom_id)
    
    def to_dict(self):
        return {
            "atom_id": self.atom_id,
            "atom_type": self.atom_type.value,
            "name": self.name,
            "truth_value": self.truth_value.to_dict(),
            "metadata": self.metadata,
            "incoming": list(self.incoming),
            "outgoing": list(self.outgoing),
        }


@dataclass
class Link(Atom):
    """
    Represents a relationship between multiple atoms (hyperedge).
    """
    targets: List[str] = field(default_factory=list)  # Atom IDs in the relationship
    
    def to_dict(self):
        result = super().to_dict()
        result["targets"] = self.targets
        return result


class AtomSpace:
    """
    Knowledge base that stores atoms and links in a hypergraph structure.
    Inspired by OpenCog's AtomSpace but optimized for case analysis.
    """
    def __init__(self, case_id: str):
        self.case_id = case_id
        self.atoms: Dict[str, Atom] = {}
        self.index_by_type: Dict[AtomType, Set[str]] = {t: set() for t in AtomType}
        self.index_by_name: Dict[str, Set[str]] = {}
        logger.info(f"Initialized AtomSpace for case: {case_id}")
    
    def add_atom(self, atom: Atom) -> str:
        """Add an atom to the space"""
        self.atoms[atom.atom_id] = atom
        self.index_by_type[atom.atom_type].add(atom.atom_id)
        
        if atom.name not in self.index_by_name:
            self.index_by_name[atom.name] = set()
        self.index_by_name[atom.name].add(atom.atom_id)
        
        return atom.atom_id
    
    def get_atom(self, atom_id: str) -> Optional[Atom]:
        """Retrieve an atom by ID"""
        return self.atoms.get(atom_id)
    
    def get_atoms_by_type(self, atom_type: AtomType) -> List[Atom]:
        """Get all atoms of a specific type"""
        return [self.atoms[aid] for aid in self.index_by_type[atom_type]]
    
    def get_atoms_by_name(self, name: str) -> List[Atom]:
        """Get all atoms with a specific name"""
        atom_ids = self.index_by_name.get(name, set())
        return [self.atoms[aid] for aid in atom_ids]
    
    def add_link(self, link_type: AtomType, name: str, targets: List[str],
                 truth_value: Optional[TruthValue] = None) -> str:
        """Create a link between atoms"""
        link_id = f"link_{name}_{len(self.atoms)}"
        link = Link(
            atom_id=link_id,
            atom_type=link_type,
            name=name,
            truth_value=truth_value or TruthValue(),
            targets=targets
        )
        
        # Update incoming/outgoing references
        for target_id in targets:
            if target_id in self.atoms:
                self.atoms[target_id].incoming.add(link_id)
        
        self.add_atom(link)
        return link_id
    
    def query(self, pattern: Dict[str, Any]) -> List[Atom]:
        """
        Query atoms matching a pattern.
        
        Args:
            pattern: Dictionary with query criteria:
                - atom_type: AtomType to match
                - name_contains: Substring in name
                - min_strength: Minimum truth strength
                - min_confidence: Minimum confidence
        
        Returns:
            List of matching atoms
        """
        results = []
        candidates = self.atoms.values()
        
        if "atom_type" in pattern:
            candidates = self.get_atoms_by_type(pattern["atom_type"])
        
        for atom in candidates:
            if "name_contains" in pattern:
                if pattern["name_contains"] not in atom.name:
                    continue
            
            if "min_strength" in pattern:
                if atom.truth_value.strength < pattern["min_strength"]:
                    continue
            
            if "min_confidence" in pattern:
                if atom.truth_value.confidence < pattern["min_confidence"]:
                    continue
            
            results.append(atom)
        
        return results
    
    def export_to_json(self, filepath: str):
        """Export AtomSpace to JSON file"""
        data = {
            "case_id": self.case_id,
            "atoms": {aid: atom.to_dict() for aid, atom in self.atoms.items()},
            "statistics": {
                "total_atoms": len(self.atoms),
                "atoms_by_type": {
                    t.value: len(self.index_by_type[t]) for t in AtomType
                }
            }
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Exported AtomSpace to {filepath}")


class HGNNQLQueryEngine:
    """
    Query engine for HGNNQL (HyperGraph Neural Network Query Language).
    Provides high-level query interface for case analysis.
    """
    def __init__(self, atomspace: AtomSpace):
        self.atomspace = atomspace
        logger.info("Initialized HGNNQL Query Engine")
    
    def find_entities(self, entity_type: Optional[str] = None) -> List[Atom]:
        """Find all entity atoms, optionally filtered by type"""
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        if entity_type:
            entities = [e for e in entities if e.metadata.get("entity_type") == entity_type]
        return entities
    
    def find_events(self, start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Atom]:
        """Find event atoms within a date range"""
        events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        
        if start_date or end_date:
            filtered = []
            for event in events:
                event_date = event.metadata.get("timestamp")
                if isinstance(event_date, str):
                    event_date = datetime.fromisoformat(event_date)
                
                if start_date and event_date < start_date:
                    continue
                if end_date and event_date > end_date:
                    continue
                
                filtered.append(event)
            return filtered
        
        return events
    
    def find_relationships(self, source: str, target: str,
                          relationship_type: Optional[str] = None) -> List[Link]:
        """Find relationships between two entities"""
        relationships = []
        
        for atom in self.atomspace.get_atoms_by_type(AtomType.RELATIONSHIP):
            if not isinstance(atom, Link):
                continue
            
            if source in atom.targets and target in atom.targets:
                if relationship_type is None or atom.name == relationship_type:
                    relationships.append(atom)
        
        return relationships
    
    def find_patterns(self, pattern_type: Optional[str] = None,
                     min_confidence: float = 0.5) -> List[Atom]:
        """Find identified patterns with minimum confidence"""
        patterns = self.atomspace.get_atoms_by_type(AtomType.PATTERN)
        
        filtered = [p for p in patterns if p.truth_value.confidence >= min_confidence]
        
        if pattern_type:
            filtered = [p for p in filtered if p.metadata.get("pattern_type") == pattern_type]
        
        return filtered
    
    def find_evidence(self, entity_id: Optional[str] = None,
                     verified_only: bool = False) -> List[Atom]:
        """Find evidence atoms, optionally filtered by entity or verification status"""
        evidence = self.atomspace.get_atoms_by_type(AtomType.EVIDENCE)
        
        if entity_id:
            evidence = [e for e in evidence if entity_id in e.outgoing]
        
        if verified_only:
            evidence = [e for e in evidence 
                       if e.metadata.get("verification_status") == "verified"]
        
        return evidence
    
    def execute_hgnnql(self, query: str) -> Dict[str, Any]:
        """
        Execute a HGNNQL query string.
        
        Query format:
            FIND <atom_type> WHERE <conditions>
            LINK <source> TO <target> AS <relationship>
            INFER <pattern> FROM <evidence>
        
        Args:
            query: HGNNQL query string
        
        Returns:
            Query results as dictionary
        """
        original_query = query.strip()
        parts = original_query.split()
        
        if not parts:
            return {"error": "Empty query"}
        
        command = parts[0].upper()
        
        if command == "FIND":
            return self._execute_find(parts[1:])
        elif command == "LINK":
            return self._execute_link(parts[1:])
        elif command == "INFER":
            return self._execute_infer(parts[1:])
        elif command == "QUERY":
            return self._execute_query(parts[1:])
        elif command == "COUNT":
            return self._execute_count(parts[1:])
        else:
            return {"error": f"Unknown command: {command}"}
    
    def _execute_find(self, parts: List[str]) -> Dict[str, Any]:
        """Execute FIND query"""
        if not parts:
            return {"error": "FIND requires atom type"}
        
        atom_type_str = parts[0].upper()
        try:
            atom_type = AtomType[atom_type_str]
            atoms = self.atomspace.get_atoms_by_type(atom_type)
            return {
                "command": "FIND",
                "atom_type": atom_type_str,
                "count": len(atoms),
                "results": [a.to_dict() for a in atoms]
            }
        except KeyError:
            return {"error": f"Invalid atom type: {atom_type_str}"}
    
    def _execute_link(self, parts: List[str]) -> Dict[str, Any]:
        """
        Execute LINK query
        Syntax: LINK <source> TO <target> AS <relationship>
        """
        if len(parts) < 5:
            return {"error": "LINK requires: LINK <source> TO <target> AS <relationship>"}
        
        if parts[1].upper() != "TO" or parts[3].upper() != "AS":
            return {"error": "Invalid LINK syntax. Use: LINK <source> TO <target> AS <relationship>"}
        
        source_id = parts[0]
        target_id = parts[2]
        relationship_type = parts[4]
        
        # Find source and target atoms
        source_atom = self.atomspace.get_atom(source_id)
        target_atom = self.atomspace.get_atom(target_id)
        
        if not source_atom:
            return {"error": f"Source atom not found: {source_id}"}
        if not target_atom:
            return {"error": f"Target atom not found: {target_id}"}
        
        # Create relationship link
        link_id = f"link_{source_id}_{target_id}_{relationship_type}"
        link = Link(
            atom_id=link_id,
            atom_type=AtomType.RELATIONSHIP,
            name=f"{relationship_type}: {source_id} -> {target_id}",
            targets=[source_id, target_id],
            truth_value=TruthValue(strength=0.8, confidence=0.9),
            metadata={"created_by": "hgnnql_link", "timestamp": datetime.now().isoformat(), "relationship_type": relationship_type}
        )
        
        self.atomspace.add_atom(link)
        
        return {
            "command": "LINK",
            "status": "success",
            "link_id": link_id,
            "source": source_id,
            "target": target_id,
            "relationship": relationship_type
        }
    
    def _execute_infer(self, parts: List[str]) -> Dict[str, Any]:
        """
        Execute INFER query
        Syntax: INFER <pattern> FROM <evidence>
        """
        if len(parts) < 3:
            return {"error": "INFER requires: INFER <pattern> FROM <evidence>"}
        
        if "FROM" not in [p.upper() for p in parts]:
            return {"error": "Invalid INFER syntax. Use: INFER <pattern> FROM <evidence>"}
        
        from_index = next(i for i, p in enumerate(parts) if p.upper() == "FROM")
        pattern_parts = parts[:from_index]
        evidence_parts = parts[from_index+1:]
        
        pattern = " ".join(pattern_parts)
        evidence_ids = evidence_parts
        
        # Collect evidence atoms
        evidence_atoms = []
        for evidence_id in evidence_ids:
            atom = self.atomspace.get_atom(evidence_id)
            if atom:
                evidence_atoms.append(atom)
        
        if not evidence_atoms:
            return {"error": "No valid evidence atoms found"}
        
        # Simple inference: calculate average truth value from evidence
        total_strength = sum(atom.truth_value.strength for atom in evidence_atoms)
        total_confidence = sum(atom.truth_value.confidence for atom in evidence_atoms)
        avg_strength = total_strength / len(evidence_atoms)
        avg_confidence = total_confidence / len(evidence_atoms)
        
        # Create inferred atom
        inferred_id = f"inferred_{pattern.replace(' ', '_').lower()}"
        inferred_atom = Atom(
            atom_id=inferred_id,
            atom_type=AtomType.INFERENCE,
            name=f"Inferred: {pattern}",
            truth_value=TruthValue(strength=avg_strength * 0.8, confidence=avg_confidence * 0.9),  # Reduce confidence for inference
            metadata={
                "inferred_from": evidence_ids,
                "pattern": pattern,
                "inference_method": "simple_average",
                "timestamp": datetime.now().isoformat()
            }
        )
        
        self.atomspace.add_atom(inferred_atom)
        
        return {
            "command": "INFER",
            "status": "success",
            "inferred_id": inferred_id,
            "pattern": pattern,
            "evidence_count": len(evidence_atoms),
            "confidence": avg_confidence * 0.9,
            "strength": avg_strength * 0.8
        }
    
    def _execute_query(self, parts: List[str]) -> Dict[str, Any]:
        """
        Execute QUERY command - flexible graph traversal
        Syntax: QUERY CONNECTED TO <atom_id> [WITH <relationship_type>]
        """
        if len(parts) < 3:
            return {"error": "QUERY requires: QUERY CONNECTED TO <atom_id> [WITH <relationship_type>]"}
        
        if parts[0].upper() != "CONNECTED" or parts[1].upper() != "TO":
            return {"error": "Invalid QUERY syntax. Use: QUERY CONNECTED TO <atom_id>"}
        
        atom_id = parts[2]
        relationship_filter = None
        
        if len(parts) > 4 and parts[3].upper() == "WITH":
            relationship_filter = parts[4]
        
        # Find the atom
        atom = self.atomspace.get_atom(atom_id)
        if not atom:
            return {"error": f"Atom not found: {atom_id}"}
        
        # Find connected atoms through links
        connected_atoms = []
        for atom_obj in self.atomspace.atoms.values():
            if isinstance(atom_obj, Link) and atom_id in atom_obj.targets:
                # Check if relationship filter matches
                if relationship_filter and atom_obj.metadata.get("relationship_type") != relationship_filter:
                    continue
                
                # Add other atoms in the link
                for target_id in atom_obj.targets:
                    if target_id != atom_id:
                        target_atom = self.atomspace.get_atom(target_id)
                        if target_atom and target_atom not in connected_atoms:
                            connected_atoms.append(target_atom)
        
        return {
            "command": "QUERY",
            "query_type": "connected",
            "source_atom": atom_id,
            "relationship_filter": relationship_filter,
            "connected_count": len(connected_atoms),
            "connected_atoms": [a.to_dict() for a in connected_atoms]
        }
    
    def _execute_count(self, parts: List[str]) -> Dict[str, Any]:
        """
        Execute COUNT command
        Syntax: COUNT <atom_type> [WHERE <condition>]
        """
        if not parts:
            return {"error": "COUNT requires atom type"}
        
        atom_type_str = parts[0].upper()
        try:
            atom_type = AtomType[atom_type_str]
        except KeyError:
            return {"error": f"Invalid atom type: {atom_type_str}"}
        
        atoms = self.atomspace.get_atoms_by_type(atom_type)
        
        # Simple WHERE clause support
        if len(parts) > 2 and parts[1].upper() == "WHERE":
            condition = " ".join(parts[2:])
            # For now, just support name-based filtering
            if "NAME" in condition.upper():
                name_value = condition.split("=")[-1].strip().strip("'\"")
                atoms = [a for a in atoms if name_value.lower() in a.name.lower()]
        
        return {
            "command": "COUNT",
            "atom_type": atom_type_str,
            "count": len(atoms),
            "condition": " ".join(parts[1:]) if len(parts) > 1 else None
        }


class CaseLLM:
    """
    Case-LLM: LLM-based reasoning system for case analysis.
    Integrates with HyperGNN and HGNNQL for knowledge-enhanced inference.
    """
    def __init__(self, atomspace: AtomSpace, model_name: str = "case-llm"):
        self.atomspace = atomspace
        self.model_name = model_name
        self.embedding_dim = 768  # Standard LLM embedding dimension
        logger.info(f"Initialized Case-LLM: {model_name}")
    
    def embed_atom(self, atom: Atom) -> np.ndarray:
        """
        Generate LLM embedding for an atom.
        In a real implementation, this would use a transformer model.
        """
        # Simplified: create embedding from name and metadata
        text = f"{atom.name} {json.dumps(atom.metadata)}"
        # Mock embedding (in practice, use actual LLM)
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(self.embedding_dim)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding
    
    def compute_semantic_similarity(self, atom1: Atom, atom2: Atom) -> float:
        """Compute semantic similarity between two atoms"""
        if atom1.embedding is None:
            atom1.embedding = self.embed_atom(atom1)
        if atom2.embedding is None:
            atom2.embedding = self.embed_atom(atom2)
        
        similarity = np.dot(atom1.embedding, atom2.embedding)
        return float(similarity)
    
    def find_similar_atoms(self, query_atom: Atom, top_k: int = 5) -> List[Tuple[Atom, float]]:
        """Find atoms most similar to the query atom"""
        if query_atom.embedding is None:
            query_atom.embedding = self.embed_atom(query_atom)
        
        similarities = []
        for atom in self.atomspace.atoms.values():
            if atom.atom_id == query_atom.atom_id:
                continue
            
            sim = self.compute_semantic_similarity(query_atom, atom)
            similarities.append((atom, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def reason_about_case(self, question: str) -> Dict[str, Any]:
        """
        Use LLM reasoning to answer questions about the case.
        
        Args:
            question: Natural language question about the case
        
        Returns:
            Reasoning result with answer and supporting evidence
        """
        # Simplified reasoning
        # In practice, this would use an actual LLM with the case knowledge
        
        # Find relevant atoms
        relevant_entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        relevant_events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        
        return {
            "question": question,
            "model": self.model_name,
            "context": {
                "entities_count": len(relevant_entities),
                "events_count": len(relevant_events),
            },
            "answer": "Analysis requires integration with actual LLM backend",
            "confidence": 0.5,
            "supporting_atoms": []
        }


# Export key classes
__all__ = [
    "AtomType",
    "TruthValue", 
    "Atom",
    "Link",
    "AtomSpace",
    "HGNNQLQueryEngine",
    "CaseLLM",
]
