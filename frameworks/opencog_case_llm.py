#!/usr/bin/env python3
"""
OpenCog HGNNQL Case-LLM - Unified Integration
=============================================

This module provides a unified interface integrating:
1. OpenCog-inspired HGNNQL knowledge representation
2. Hyper-Holmes inference engine for automated reasoning
3. Super-Sleuth introspection trainer for pattern learning
4. Case-LLM for semantic understanding and natural language interaction

This creates a complete AI-powered case analysis system combining
symbolic reasoning, neural networks, and knowledge graphs.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from frameworks.opencog_hgnnql import (
    Atom,
    AtomSpace,
    AtomType,
    CaseLLM,
    HGNNQLQueryEngine,
    TruthValue,
)
from frameworks.hyper_holmes_inference import HyperHolmesInferenceEngine
from frameworks.super_sleuth_trainer import SuperSleuthTrainer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenCogCaseLLM:
    """
    Unified OpenCog HGNNQL Case-LLM system.
    
    Integrates multiple AI components for comprehensive case analysis:
    - Knowledge representation via AtomSpace
    - Query interface via HGNNQL
    - Automated reasoning via Hyper-Holmes
    - Pattern learning via Super-Sleuth
    - Semantic understanding via Case-LLM
    """
    
    def __init__(self, case_id: str, output_dir: str = "./output"):
        """
        Initialize the OpenCog Case-LLM system.
        
        Args:
            case_id: Unique identifier for the case
            output_dir: Directory for output files
        """
        self.case_id = case_id
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize core components
        self.atomspace = AtomSpace(case_id)
        self.query_engine = HGNNQLQueryEngine(self.atomspace)
        self.inference_engine = HyperHolmesInferenceEngine(self.atomspace)
        self.trainer = SuperSleuthTrainer(self.atomspace)
        self.llm = CaseLLM(self.atomspace)
        
        logger.info(f"Initialized OpenCog Case-LLM for case: {case_id}")
    
    def load_case_from_hypergnn(self, hypergnn_framework) -> Dict[str, Any]:
        """
        Load case data from HyperGNN framework into AtomSpace.
        
        Args:
            hypergnn_framework: HyperGNN framework instance with case data
        
        Returns:
            Loading summary
        """
        logger.info("Loading case data from HyperGNN framework...")
        
        stats = {
            "entities_added": 0,
            "events_added": 0,
            "relationships_added": 0,
        }
        
        # Import agents as entities
        if hasattr(hypergnn_framework, 'agents'):
            for agent_id, agent in hypergnn_framework.agents.items():
                entity_atom = Atom(
                    atom_id=f"entity_{agent_id}",
                    atom_type=AtomType.ENTITY,
                    name=agent.name if hasattr(agent, 'name') else agent_id,
                    truth_value=TruthValue(strength=0.9, confidence=0.8),
                    metadata={
                        "agent_id": agent_id,
                        "entity_type": agent.agent_type.value if hasattr(agent, 'agent_type') else "unknown",
                        "attributes": agent.attributes if hasattr(agent, 'attributes') else {},
                    }
                )
                self.atomspace.add_atom(entity_atom)
                stats["entities_added"] += 1
        
        # Import events
        if hasattr(hypergnn_framework, 'events'):
            for event_id, event in hypergnn_framework.events.items():
                event_atom = Atom(
                    atom_id=f"event_{event_id}",
                    atom_type=AtomType.EVENT,
                    name=event.description if hasattr(event, 'description') else event_id,
                    truth_value=TruthValue(strength=0.85, confidence=0.75),
                    metadata={
                        "event_id": event_id,
                        "timestamp": event.timestamp if hasattr(event, 'timestamp') else None,
                        "event_type": event.event_type.value if hasattr(event, 'event_type') else "unknown",
                    }
                )
                self.atomspace.add_atom(event_atom)
                stats["events_added"] += 1
        
        # Import flows as relationships
        if hasattr(hypergnn_framework, 'flows'):
            for flow_id, flow in hypergnn_framework.flows.items():
                if hasattr(flow, 'source') and hasattr(flow, 'target'):
                    self.atomspace.add_link(
                        link_type=AtomType.RELATIONSHIP,
                        name=flow.flow_type.value if hasattr(flow, 'flow_type') else "flow",
                        targets=[f"entity_{flow.source}", f"entity_{flow.target}"],
                        truth_value=TruthValue(strength=0.8, confidence=0.7)
                    )
                    stats["relationships_added"] += 1
        
        logger.info(f"Loaded case data: {stats}")
        return stats
    
    def add_entity(self, entity_id: str, name: str, entity_type: str,
                   attributes: Optional[Dict[str, Any]] = None) -> str:
        """Add an entity to the knowledge base"""
        atom = Atom(
            atom_id=f"entity_{entity_id}",
            atom_type=AtomType.ENTITY,
            name=name,
            truth_value=TruthValue(strength=0.9, confidence=0.8),
            metadata={
                "entity_id": entity_id,
                "entity_type": entity_type,
                "attributes": attributes or {},
            }
        )
        return self.atomspace.add_atom(atom)
    
    def add_event(self, event_id: str, description: str, timestamp: datetime,
                  participants: Optional[List[str]] = None) -> str:
        """Add an event to the knowledge base"""
        atom = Atom(
            atom_id=f"event_{event_id}",
            atom_type=AtomType.EVENT,
            name=description,
            truth_value=TruthValue(strength=0.85, confidence=0.75),
            metadata={
                "event_id": event_id,
                "timestamp": timestamp.isoformat(),
                "participants": participants or [],
            }
        )
        atom_id = self.atomspace.add_atom(atom)
        
        # Link to participants
        if participants:
            for participant in participants:
                atom.outgoing.add(f"entity_{participant}")
        
        return atom_id
    
    def add_relationship(self, source_id: str, target_id: str, 
                        relationship_type: str, strength: float = 0.8) -> str:
        """Add a relationship between entities"""
        return self.atomspace.add_link(
            link_type=AtomType.RELATIONSHIP,
            name=relationship_type,
            targets=[f"entity_{source_id}", f"entity_{target_id}"],
            truth_value=TruthValue(strength=strength, confidence=0.7)
        )
    
    def add_evidence(self, evidence_id: str, description: str,
                    related_entities: Optional[List[str]] = None,
                    verification_status: str = "unverified") -> str:
        """Add evidence to the knowledge base"""
        atom = Atom(
            atom_id=f"evidence_{evidence_id}",
            atom_type=AtomType.EVIDENCE,
            name=description,
            truth_value=TruthValue(
                strength=0.9 if verification_status == "verified" else 0.6,
                confidence=0.8 if verification_status == "verified" else 0.5
            ),
            metadata={
                "evidence_id": evidence_id,
                "verification_status": verification_status,
            }
        )
        atom_id = self.atomspace.add_atom(atom)
        
        # Link to related entities
        if related_entities:
            for entity_id in related_entities:
                atom.outgoing.add(f"entity_{entity_id}")
        
        return atom_id
    
    def query_hgnnql(self, query: str) -> Dict[str, Any]:
        """
        Execute an HGNNQL query.
        
        Args:
            query: HGNNQL query string
        
        Returns:
            Query results
        """
        return self.query_engine.execute_hgnnql(query)
    
    def query_entities(self, entity_type: Optional[str] = None) -> List[Atom]:
        """Query entities, optionally filtered by type"""
        return self.query_engine.find_entities(entity_type)
    
    def query_events(self, start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None) -> List[Atom]:
        """Query events within a date range"""
        return self.query_engine.find_events(start_date, end_date)
    
    def query_relationships(self, source: str, target: str,
                           relationship_type: Optional[str] = None) -> List:
        """Query relationships between entities"""
        return self.query_engine.find_relationships(source, target, relationship_type)
    
    def run_inference(self, method: str = "forward", max_iterations: int = 10) -> Dict[str, Any]:
        """
        Run inference to derive new knowledge.
        
        Args:
            method: "forward" or "backward"
            max_iterations: Maximum inference iterations
        
        Returns:
            Inference results
        """
        logger.info(f"Running {method} inference...")
        
        if method == "forward":
            return self.inference_engine.forward_chain(max_iterations)
        else:
            # For backward chaining, need a goal
            return {"error": "Backward chaining requires a goal atom"}
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns in the case data"""
        return self.inference_engine.detect_patterns()
    
    def generate_hypotheses(self, evidence_ids: List[str]) -> List[Dict[str, Any]]:
        """Generate hypotheses from evidence"""
        return self.inference_engine.generate_hypotheses(evidence_ids)
    
    def train_introspection(self) -> Dict[str, Any]:
        """
        Train the Super-Sleuth introspection system.
        
        Returns:
            Training summary
        """
        return self.trainer.train_on_case_data()
    
    def introspect(self) -> Dict[str, Any]:
        """
        Perform introspective analysis of the knowledge base.
        
        Returns:
            Introspection report
        """
        return self.trainer.introspect()
    
    def get_investigation_leads(self) -> List[Dict[str, Any]]:
        """Get generated investigation leads"""
        return [lead.to_dict() for lead in self.trainer.investigation_leads]
    
    def get_learned_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get patterns learned by Super-Sleuth"""
        return {
            pid: pattern.to_dict() 
            for pid, pattern in self.trainer.learned_patterns.items()
        }
    
    def ask_llm(self, question: str) -> Dict[str, Any]:
        """
        Ask a natural language question about the case.
        
        Args:
            question: Question in natural language
        
        Returns:
            LLM response with answer and supporting evidence
        """
        return self.llm.reason_about_case(question)
    
    def find_similar_concepts(self, concept: str, top_k: int = 5) -> List[Tuple[Atom, float]]:
        """
        Find concepts similar to the given concept using LLM embeddings.
        
        Args:
            concept: Concept to search for
            top_k: Number of similar concepts to return
        
        Returns:
            List of (atom, similarity_score) tuples
        """
        # Create a query atom
        query_atom = Atom(
            atom_id="query_temp",
            atom_type=AtomType.CONCEPT,
            name=concept,
        )
        
        return self.llm.find_similar_atoms(query_atom, top_k)
    
    def run_complete_analysis(self) -> Dict[str, Any]:
        """
        Run a complete analysis pipeline:
        1. Forward chaining inference
        2. Pattern detection
        3. Introspection training
        4. Lead generation
        
        Returns:
            Complete analysis report
        """
        logger.info("Running complete OpenCog Case-LLM analysis...")
        
        analysis_start = datetime.now()
        
        # Step 1: Inference
        inference_results = self.run_inference(method="forward", max_iterations=10)
        
        # Step 2: Pattern detection
        patterns = self.detect_patterns()
        
        # Step 3: Introspection training
        training_summary = self.train_introspection()
        
        # Step 4: Introspection
        introspection_report = self.introspect()
        
        # Step 5: Get leads
        leads = self.get_investigation_leads()
        
        analysis_duration = (datetime.now() - analysis_start).total_seconds()
        
        report = {
            "case_id": self.case_id,
            "analysis_timestamp": analysis_start.isoformat(),
            "duration_seconds": analysis_duration,
            "inference_results": inference_results,
            "patterns_detected": patterns,
            "training_summary": training_summary,
            "introspection_report": introspection_report,
            "investigation_leads": leads,
            "summary": {
                "total_inferences": inference_results.get("total_inferences", 0),
                "patterns_detected": len(patterns),
                "leads_generated": len(leads),
                "knowledge_base_size": len(self.atomspace.atoms),
            }
        }
        
        # Export results
        output_file = self.output_dir / f"opencog_case_llm_analysis_{self.case_id}.json"
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Complete analysis finished. Report saved to {output_file}")
        
        return report
    
    def export_knowledge_base(self, filepath: Optional[str] = None):
        """Export the complete knowledge base to JSON"""
        if filepath is None:
            filepath = str(self.output_dir / f"knowledge_base_{self.case_id}.json")
        
        self.atomspace.export_to_json(filepath)
    
    def export_training_results(self, filepath: Optional[str] = None):
        """Export training results"""
        if filepath is None:
            filepath = str(self.output_dir / f"training_results_{self.case_id}.json")
        
        self.trainer.export_training_results(filepath)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all system components"""
        return {
            "case_id": self.case_id,
            "atomspace": {
                "total_atoms": len(self.atomspace.atoms),
                "atoms_by_type": {
                    atom_type.value: len(self.atomspace.index_by_type[atom_type])
                    for atom_type in AtomType
                }
            },
            "inference_engine": self.inference_engine.get_inference_statistics(),
            "trainer": {
                "patterns_learned": len(self.trainer.learned_patterns),
                "leads_generated": len(self.trainer.investigation_leads),
            },
            "llm": {
                "model_name": self.llm.model_name,
                "embedding_dim": self.llm.embedding_dim,
            }
        }


# Export key class
__all__ = ["OpenCogCaseLLM"]
