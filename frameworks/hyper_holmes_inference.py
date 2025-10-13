#!/usr/bin/env python3
"""
Hyper-Holmes Inference Engine
=============================

Advanced inference engine for automated reasoning about case knowledge.
Implements forward-chaining and backward-chaining inference with
probabilistic reasoning support.

Key Features:
1. Rule-based inference with truth value propagation
2. Pattern matching and recognition
3. Anomaly detection in case data
4. Causal reasoning and hypothesis generation
5. Integration with HGNNQL AtomSpace
"""

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, Link, TruthValue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RuleType(Enum):
    """Types of inference rules"""
    DEDUCTION = "deduction"  # A->B, B->C => A->C
    INDUCTION = "induction"  # Multiple instances => pattern
    ABDUCTION = "abduction"  # Effect observed => hypothesize cause
    ANALOGY = "analogy"  # A:B :: C:D
    TEMPORAL = "temporal"  # Before/after relationships
    CAUSAL = "causal"  # Cause-effect relationships


@dataclass
class InferenceRule:
    """
    Represents an inference rule for automated reasoning.
    """
    rule_id: str
    rule_type: RuleType
    name: str
    description: str
    premises: List[Dict[str, Any]]  # Conditions that must be met
    conclusion: Dict[str, Any]  # What to infer
    strength_formula: Optional[Callable] = None  # How to compute truth value
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def applies_to(self, atomspace: AtomSpace) -> bool:
        """Check if this rule can be applied to current atomspace"""
        # Check if all premises are satisfied
        for premise in self.premises:
            if not self._check_premise(premise, atomspace):
                return False
        return True
    
    def _check_premise(self, premise: Dict[str, Any], atomspace: AtomSpace) -> bool:
        """Check if a single premise is satisfied"""
        atom_type = premise.get("atom_type")
        if atom_type:
            matching_atoms = atomspace.query(premise)
            return len(matching_atoms) > 0
        return True
    
    def apply(self, atomspace: AtomSpace) -> List[str]:
        """Apply the rule and return IDs of newly inferred atoms"""
        if not self.applies_to(atomspace):
            return []
        
        inferred_atoms = []
        # Create inference atom
        inference_id = f"inference_{self.rule_id}_{len(atomspace.atoms)}"
        
        # Compute truth value for inference
        if self.strength_formula:
            truth_value = self.strength_formula(atomspace, self.premises)
        else:
            truth_value = TruthValue(strength=0.7, confidence=0.6)
        
        inference_atom = Atom(
            atom_id=inference_id,
            atom_type=AtomType.INFERENCE,
            name=f"inferred_{self.conclusion.get('name', 'unknown')}",
            truth_value=truth_value,
            metadata={
                "rule_id": self.rule_id,
                "rule_type": self.rule_type.value,
                "conclusion": self.conclusion,
            }
        )
        
        atomspace.add_atom(inference_atom)
        inferred_atoms.append(inference_id)
        
        logger.info(f"Applied rule {self.rule_id}: {self.name}")
        return inferred_atoms


class HyperHolmesInferenceEngine:
    """
    Main inference engine for automated reasoning about case knowledge.
    Named after Sherlock Holmes, enhanced with hypergraph reasoning.
    """
    def __init__(self, atomspace: AtomSpace):
        self.atomspace = atomspace
        self.rules: Dict[str, InferenceRule] = {}
        self.inference_history: List[Dict[str, Any]] = []
        self._initialize_default_rules()
        logger.info("Initialized Hyper-Holmes Inference Engine")
    
    def _initialize_default_rules(self):
        """Initialize default inference rules for case analysis"""
        
        # Rule 1: Co-occurrence pattern detection
        cooccurrence_rule = InferenceRule(
            rule_id="rule_cooccurrence",
            rule_type=RuleType.INDUCTION,
            name="Co-occurrence Pattern Detection",
            description="Detect patterns from co-occurring events",
            premises=[
                {"atom_type": AtomType.EVENT, "min_strength": 0.6},
            ],
            conclusion={"atom_type": AtomType.PATTERN, "name": "co_occurrence_pattern"}
        )
        self.add_rule(cooccurrence_rule)
        
        # Rule 2: Entity relationship inference
        relationship_rule = InferenceRule(
            rule_id="rule_entity_relationship",
            rule_type=RuleType.DEDUCTION,
            name="Entity Relationship Inference",
            description="Infer relationships from shared events",
            premises=[
                {"atom_type": AtomType.ENTITY},
                {"atom_type": AtomType.EVENT},
            ],
            conclusion={"atom_type": AtomType.RELATIONSHIP, "name": "inferred_relationship"}
        )
        self.add_rule(relationship_rule)
        
        # Rule 3: Temporal sequence inference
        temporal_rule = InferenceRule(
            rule_id="rule_temporal_sequence",
            rule_type=RuleType.TEMPORAL,
            name="Temporal Sequence Analysis",
            description="Identify temporal sequences and potential causation",
            premises=[
                {"atom_type": AtomType.EVENT},
            ],
            conclusion={"atom_type": AtomType.PATTERN, "name": "temporal_sequence"}
        )
        self.add_rule(temporal_rule)
        
        # Rule 4: Anomaly detection
        anomaly_rule = InferenceRule(
            rule_id="rule_anomaly_detection",
            rule_type=RuleType.ABDUCTION,
            name="Anomaly Detection",
            description="Detect anomalous patterns requiring explanation",
            premises=[
                {"atom_type": AtomType.EVENT, "min_strength": 0.5},
                {"atom_type": AtomType.ENTITY},
            ],
            conclusion={"atom_type": AtomType.PATTERN, "name": "anomaly"}
        )
        self.add_rule(anomaly_rule)
    
    def add_rule(self, rule: InferenceRule):
        """Add an inference rule to the engine"""
        self.rules[rule.rule_id] = rule
        logger.info(f"Added inference rule: {rule.name}")
    
    def forward_chain(self, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Forward chaining inference: apply rules to derive new knowledge.
        
        Args:
            max_iterations: Maximum number of inference iterations
        
        Returns:
            Summary of inference results
        """
        logger.info("Starting forward chaining inference...")
        
        total_inferences = 0
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            inferences_this_iteration = 0
            
            # Try to apply each rule
            for rule_id, rule in self.rules.items():
                try:
                    new_atoms = rule.apply(self.atomspace)
                    inferences_this_iteration += len(new_atoms)
                    
                    if new_atoms:
                        self.inference_history.append({
                            "iteration": iteration,
                            "rule_id": rule_id,
                            "rule_name": rule.name,
                            "inferred_atoms": new_atoms,
                        })
                except Exception as e:
                    logger.error(f"Error applying rule {rule_id}: {e}")
            
            total_inferences += inferences_this_iteration
            
            # Stop if no new inferences
            if inferences_this_iteration == 0:
                logger.info(f"Convergence reached at iteration {iteration}")
                break
        
        result = {
            "method": "forward_chain",
            "iterations": iteration,
            "total_inferences": total_inferences,
            "rules_applied": len(self.inference_history),
            "inference_history": self.inference_history,
        }
        
        logger.info(f"Forward chaining complete: {total_inferences} inferences")
        return result
    
    def backward_chain(self, goal_atom: Atom, max_depth: int = 5) -> Dict[str, Any]:
        """
        Backward chaining inference: work backwards from goal to find support.
        
        Args:
            goal_atom: The atom to prove or find support for
            max_depth: Maximum search depth
        
        Returns:
            Proof tree or evidence chain
        """
        logger.info(f"Starting backward chaining for goal: {goal_atom.name}")
        
        proof_chain = self._backward_chain_recursive(goal_atom, depth=0, max_depth=max_depth)
        
        result = {
            "method": "backward_chain",
            "goal": goal_atom.to_dict(),
            "proof_found": proof_chain is not None,
            "proof_chain": proof_chain,
        }
        
        return result
    
    def _backward_chain_recursive(self, goal: Atom, depth: int, max_depth: int) -> Optional[List[Dict[str, Any]]]:
        """Recursive backward chaining helper"""
        if depth >= max_depth:
            return None
        
        # Check if goal already exists in atomspace
        existing = self.atomspace.get_atom(goal.atom_id)
        if existing and existing.truth_value.strength > 0.5:
            return [{"atom": existing.to_dict(), "depth": depth, "status": "found"}]
        
        # Try to find rules that could prove this goal
        for rule_id, rule in self.rules.items():
            if self._rule_could_prove(rule, goal):
                # Try to prove premises
                premise_proofs = []
                for premise in rule.premises:
                    # Create atom for premise
                    premise_atom = self._premise_to_atom(premise)
                    sub_proof = self._backward_chain_recursive(premise_atom, depth + 1, max_depth)
                    if sub_proof:
                        premise_proofs.append(sub_proof)
                
                if len(premise_proofs) == len(rule.premises):
                    return [{
                        "atom": goal.to_dict(),
                        "rule": rule.rule_id,
                        "depth": depth,
                        "premises": premise_proofs,
                    }]
        
        return None
    
    def _rule_could_prove(self, rule: InferenceRule, goal: Atom) -> bool:
        """Check if a rule could potentially prove the goal"""
        conclusion_type = rule.conclusion.get("atom_type")
        if conclusion_type and conclusion_type != goal.atom_type:
            return False
        return True
    
    def _premise_to_atom(self, premise: Dict[str, Any]) -> Atom:
        """Convert premise dictionary to an atom"""
        atom_type = premise.get("atom_type", AtomType.CONCEPT)
        name = premise.get("name", "premise")
        return Atom(
            atom_id=f"premise_{name}",
            atom_type=atom_type,
            name=name,
        )
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """
        Detect patterns in the case data using inference.
        
        Returns:
            List of detected patterns with confidence scores
        """
        logger.info("Detecting patterns in case data...")
        
        patterns = []
        
        # Get all events
        events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        
        # Pattern 1: Frequent entity co-occurrence
        entity_cooccurrence = self._detect_entity_cooccurrence(events, entities)
        patterns.extend(entity_cooccurrence)
        
        # Pattern 2: Temporal clusters
        temporal_clusters = self._detect_temporal_clusters(events)
        patterns.extend(temporal_clusters)
        
        # Pattern 3: Anomalies
        anomalies = self._detect_anomalies(events)
        patterns.extend(anomalies)
        
        logger.info(f"Detected {len(patterns)} patterns")
        return patterns
    
    def _detect_entity_cooccurrence(self, events: List[Atom], entities: List[Atom]) -> List[Dict[str, Any]]:
        """Detect entities that frequently occur together in events"""
        cooccurrences = []
        
        # Count entity pairs in events
        entity_pairs: Dict[Tuple[str, str], int] = {}
        
        for event in events:
            event_entities = [e for e in event.outgoing if e.startswith("entity_")]
            for i, e1 in enumerate(event_entities):
                for e2 in event_entities[i+1:]:
                    pair = tuple(sorted([e1, e2]))
                    entity_pairs[pair] = entity_pairs.get(pair, 0) + 1
        
        # Identify significant co-occurrences
        for pair, count in entity_pairs.items():
            if count >= 2:  # Threshold
                cooccurrences.append({
                    "pattern_type": "entity_cooccurrence",
                    "entities": list(pair),
                    "frequency": count,
                    "confidence": min(0.9, count / len(events)),
                })
        
        return cooccurrences
    
    def _detect_temporal_clusters(self, events: List[Atom]) -> List[Dict[str, Any]]:
        """Detect temporal clusters of events"""
        clusters = []
        
        # Sort events by timestamp
        sorted_events = sorted(
            [e for e in events if "timestamp" in e.metadata],
            key=lambda e: e.metadata["timestamp"]
        )
        
        # Simple clustering: events within short time window
        if len(sorted_events) >= 2:
            clusters.append({
                "pattern_type": "temporal_cluster",
                "event_count": len(sorted_events),
                "time_span": {
                    "start": sorted_events[0].metadata.get("timestamp"),
                    "end": sorted_events[-1].metadata.get("timestamp"),
                },
                "confidence": 0.7,
            })
        
        return clusters
    
    def _detect_anomalies(self, events: List[Atom]) -> List[Dict[str, Any]]:
        """Detect anomalous events or patterns"""
        anomalies = []
        
        # Look for events with low confidence
        for event in events:
            if event.truth_value.confidence < 0.5:
                anomalies.append({
                    "pattern_type": "low_confidence_event",
                    "event_id": event.atom_id,
                    "event_name": event.name,
                    "confidence": event.truth_value.confidence,
                    "requires_investigation": True,
                })
        
        return anomalies
    
    def generate_hypotheses(self, evidence_atoms: List[str]) -> List[Dict[str, Any]]:
        """
        Generate hypotheses to explain observed evidence.
        
        Args:
            evidence_atoms: List of evidence atom IDs
        
        Returns:
            List of hypotheses with supporting reasoning
        """
        logger.info(f"Generating hypotheses from {len(evidence_atoms)} evidence atoms")
        
        hypotheses = []
        
        # Get evidence atoms
        evidence = [self.atomspace.get_atom(aid) for aid in evidence_atoms]
        evidence = [e for e in evidence if e is not None]
        
        if not evidence:
            return hypotheses
        
        # Hypothesis 1: Common cause
        hypotheses.append({
            "hypothesis_type": "common_cause",
            "description": "Evidence items may share a common cause",
            "supporting_evidence": [e.atom_id for e in evidence],
            "confidence": 0.6,
            "requires_investigation": True,
        })
        
        # Hypothesis 2: Causal chain
        if len(evidence) >= 2:
            hypotheses.append({
                "hypothesis_type": "causal_chain",
                "description": "Evidence items may form a causal sequence",
                "supporting_evidence": [e.atom_id for e in evidence],
                "confidence": 0.5,
                "requires_investigation": True,
            })
        
        return hypotheses
    
    def get_inference_statistics(self) -> Dict[str, Any]:
        """Get statistics about inference operations"""
        return {
            "total_rules": len(self.rules),
            "total_inferences": len(self.inference_history),
            "rules_breakdown": {
                rule_id: rule.rule_type.value 
                for rule_id, rule in self.rules.items()
            },
            "atomspace_size": len(self.atomspace.atoms),
        }


# Export key classes
__all__ = [
    "RuleType",
    "InferenceRule",
    "HyperHolmesInferenceEngine",
]
