#!/usr/bin/env python3
"""
Super-Sleuth Introspection Trainer
==================================

Advanced introspection and learning system for case analysis.
Trains on case patterns, learns from inference results, and improves
reasoning over time.

Key Features:
1. Pattern learning from case data
2. Introspective analysis of inference quality
3. Anomaly detection and lead generation
4. Confidence calibration
5. Knowledge base enhancement through learning
"""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from frameworks.opencog_hgnnql import Atom, AtomSpace, AtomType, TruthValue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatternCategory(Enum):
    """Categories of patterns for learning"""
    TEMPORAL = "temporal"
    FINANCIAL = "financial"
    BEHAVIORAL = "behavioral"
    RELATIONSHIP = "relationship"
    ANOMALY = "anomaly"
    CAUSAL = "causal"


@dataclass
class LearnedPattern:
    """
    Represents a pattern learned through introspection.
    """
    pattern_id: str
    category: PatternCategory
    name: str
    description: str
    frequency: int
    confidence: float
    examples: List[str] = field(default_factory=list)  # Example atom IDs
    features: Dict[str, Any] = field(default_factory=dict)
    learned_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "pattern_id": self.pattern_id,
            "category": self.category.value,
            "name": self.name,
            "description": self.description,
            "frequency": self.frequency,
            "confidence": self.confidence,
            "examples": self.examples,
            "features": self.features,
            "learned_at": self.learned_at.isoformat(),
        }


@dataclass
class InvestigationLead:
    """
    Represents a lead generated through introspection.
    """
    lead_id: str
    priority: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    description: str
    supporting_evidence: List[str]  # Atom IDs
    recommended_actions: List[str]
    confidence: float
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "lead_id": self.lead_id,
            "priority": self.priority,
            "description": self.description,
            "supporting_evidence": self.supporting_evidence,
            "recommended_actions": self.recommended_actions,
            "confidence": self.confidence,
            "generated_at": self.generated_at.isoformat(),
        }


class SuperSleuthTrainer:
    """
    Introspection trainer that learns from case data and improves reasoning.
    Named after the classic detective, enhanced with machine learning.
    """
    def __init__(self, atomspace: AtomSpace):
        self.atomspace = atomspace
        self.learned_patterns: Dict[str, LearnedPattern] = {}
        self.investigation_leads: List[InvestigationLead] = []
        self.training_history: List[Dict[str, Any]] = []
        self.pattern_statistics: Dict[str, Any] = defaultdict(int)
        logger.info("Initialized Super-Sleuth Introspection Trainer")
    
    def train_on_case_data(self) -> Dict[str, Any]:
        """
        Perform comprehensive training on case data.
        
        Returns:
            Training summary with learned patterns and statistics
        """
        logger.info("Starting Super-Sleuth training on case data...")
        
        training_start = datetime.now()
        
        # Phase 1: Analyze timing patterns
        timing_patterns = self._analyze_timing_patterns()
        
        # Phase 2: Analyze financial patterns
        financial_patterns = self._analyze_financial_patterns()
        
        # Phase 3: Analyze behavioral patterns
        behavioral_patterns = self._analyze_behavioral_patterns()
        
        # Phase 4: Analyze relationship patterns
        relationship_patterns = self._analyze_relationship_patterns()
        
        # Phase 5: Detect anomalies
        anomalies = self._detect_anomalies()
        
        # Phase 6: Generate investigation leads
        leads = self._generate_investigation_leads()
        
        training_duration = (datetime.now() - training_start).total_seconds()
        
        summary = {
            "training_timestamp": training_start.isoformat(),
            "duration_seconds": training_duration,
            "patterns_learned": len(self.learned_patterns),
            "leads_generated": len(self.investigation_leads),
            "pattern_breakdown": {
                "timing": len(timing_patterns),
                "financial": len(financial_patterns),
                "behavioral": len(behavioral_patterns),
                "relationship": len(relationship_patterns),
                "anomalies": len(anomalies),
            },
            "statistics": self.pattern_statistics,
        }
        
        self.training_history.append(summary)
        logger.info(f"Training complete: {len(self.learned_patterns)} patterns learned")
        
        return summary
    
    def _analyze_timing_patterns(self) -> List[LearnedPattern]:
        """Analyze temporal patterns in case data"""
        logger.info("Analyzing timing patterns...")
        
        patterns = []
        events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        
        if len(events) < 2:
            return patterns
        
        # Sort events by timestamp
        timestamped_events = [e for e in events if "timestamp" in e.metadata]
        timestamped_events.sort(key=lambda e: e.metadata["timestamp"])
        
        # Pattern 1: Event clusters
        if len(timestamped_events) >= 3:
            pattern = LearnedPattern(
                pattern_id=f"timing_cluster_{len(self.learned_patterns)}",
                category=PatternCategory.TEMPORAL,
                name="Event Clustering",
                description=f"Detected cluster of {len(timestamped_events)} events",
                frequency=len(timestamped_events),
                confidence=0.8,
                examples=[e.atom_id for e in timestamped_events[:5]],
                features={
                    "cluster_size": len(timestamped_events),
                    "time_span": {
                        "start": str(timestamped_events[0].metadata["timestamp"]),
                        "end": str(timestamped_events[-1].metadata["timestamp"]),
                    }
                }
            )
            patterns.append(pattern)
            self.learned_patterns[pattern.pattern_id] = pattern
            self.pattern_statistics["timing_patterns"] += 1
        
        # Pattern 2: Rapid succession
        for i in range(len(timestamped_events) - 1):
            # Check if events are close together (this is simplified)
            pattern = LearnedPattern(
                pattern_id=f"timing_succession_{i}",
                category=PatternCategory.TEMPORAL,
                name="Rapid Event Succession",
                description="Events occurring in quick succession",
                frequency=2,
                confidence=0.7,
                examples=[timestamped_events[i].atom_id, timestamped_events[i+1].atom_id],
                features={"succession_pair": True}
            )
            patterns.append(pattern)
        
        return patterns
    
    def _analyze_financial_patterns(self) -> List[LearnedPattern]:
        """Analyze financial transaction patterns"""
        logger.info("Analyzing financial patterns...")
        
        patterns = []
        
        # Find financial entities and events
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        financial_entities = [
            e for e in entities 
            if e.metadata.get("entity_type") in ["organization", "financial"]
        ]
        
        if len(financial_entities) >= 2:
            pattern = LearnedPattern(
                pattern_id=f"financial_network_{len(self.learned_patterns)}",
                category=PatternCategory.FINANCIAL,
                name="Financial Entity Network",
                description=f"Network of {len(financial_entities)} financial entities",
                frequency=len(financial_entities),
                confidence=0.75,
                examples=[e.atom_id for e in financial_entities[:5]],
                features={
                    "entity_count": len(financial_entities),
                    "network_density": len(financial_entities) * (len(financial_entities) - 1) / 2,
                }
            )
            patterns.append(pattern)
            self.learned_patterns[pattern.pattern_id] = pattern
            self.pattern_statistics["financial_patterns"] += 1
        
        return patterns
    
    def _analyze_behavioral_patterns(self) -> List[LearnedPattern]:
        """Analyze behavioral patterns of entities"""
        logger.info("Analyzing behavioral patterns...")
        
        patterns = []
        
        # Analyze entity behaviors through their events
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        
        # Count events per entity
        entity_event_counts: Dict[str, int] = defaultdict(int)
        for event in events:
            for entity_id in event.outgoing:
                if entity_id in [e.atom_id for e in entities]:
                    entity_event_counts[entity_id] += 1
        
        # Identify highly active entities
        for entity_id, count in entity_event_counts.items():
            if count >= 3:  # Threshold for high activity
                pattern = LearnedPattern(
                    pattern_id=f"behavioral_active_{entity_id}",
                    category=PatternCategory.BEHAVIORAL,
                    name="High Activity Entity",
                    description=f"Entity with {count} associated events",
                    frequency=count,
                    confidence=0.8,
                    examples=[entity_id],
                    features={
                        "activity_level": "high",
                        "event_count": count,
                    }
                )
                patterns.append(pattern)
                self.learned_patterns[pattern.pattern_id] = pattern
        
        self.pattern_statistics["behavioral_patterns"] += len(patterns)
        return patterns
    
    def _analyze_relationship_patterns(self) -> List[LearnedPattern]:
        """Analyze relationship patterns between entities"""
        logger.info("Analyzing relationship patterns...")
        
        patterns = []
        relationships = self.atomspace.get_atoms_by_type(AtomType.RELATIONSHIP)
        
        if len(relationships) >= 1:
            pattern = LearnedPattern(
                pattern_id=f"relationship_network_{len(self.learned_patterns)}",
                category=PatternCategory.RELATIONSHIP,
                name="Entity Relationship Network",
                description=f"Network with {len(relationships)} relationships",
                frequency=len(relationships),
                confidence=0.75,
                examples=[r.atom_id for r in relationships[:5]],
                features={
                    "relationship_count": len(relationships),
                }
            )
            patterns.append(pattern)
            self.learned_patterns[pattern.pattern_id] = pattern
            self.pattern_statistics["relationship_patterns"] += 1
        
        return patterns
    
    def _detect_anomalies(self) -> List[LearnedPattern]:
        """Detect anomalous patterns requiring investigation"""
        logger.info("Detecting anomalies...")
        
        anomalies = []
        
        # Anomaly 1: Low confidence atoms
        all_atoms = list(self.atomspace.atoms.values())
        low_confidence_atoms = [
            a for a in all_atoms 
            if a.truth_value.confidence < 0.5
        ]
        
        if low_confidence_atoms:
            anomaly = LearnedPattern(
                pattern_id=f"anomaly_low_confidence_{len(self.learned_patterns)}",
                category=PatternCategory.ANOMALY,
                name="Low Confidence Atoms",
                description=f"Found {len(low_confidence_atoms)} atoms with low confidence",
                frequency=len(low_confidence_atoms),
                confidence=0.9,
                examples=[a.atom_id for a in low_confidence_atoms[:5]],
                features={
                    "anomaly_type": "low_confidence",
                    "count": len(low_confidence_atoms),
                }
            )
            anomalies.append(anomaly)
            self.learned_patterns[anomaly.pattern_id] = anomaly
        
        # Anomaly 2: Isolated entities (no relationships)
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        isolated_entities = [
            e for e in entities 
            if len(e.incoming) == 0 and len(e.outgoing) == 0
        ]
        
        if isolated_entities:
            anomaly = LearnedPattern(
                pattern_id=f"anomaly_isolated_{len(self.learned_patterns)}",
                category=PatternCategory.ANOMALY,
                name="Isolated Entities",
                description=f"Found {len(isolated_entities)} entities with no relationships",
                frequency=len(isolated_entities),
                confidence=0.85,
                examples=[e.atom_id for e in isolated_entities[:5]],
                features={
                    "anomaly_type": "isolated_entity",
                    "count": len(isolated_entities),
                }
            )
            anomalies.append(anomaly)
            self.learned_patterns[anomaly.pattern_id] = anomaly
        
        self.pattern_statistics["anomalies"] += len(anomalies)
        return anomalies
    
    def _generate_investigation_leads(self) -> List[InvestigationLead]:
        """Generate investigation leads from learned patterns"""
        logger.info("Generating investigation leads...")
        
        leads = []
        
        # Lead 1: From high-priority patterns
        high_confidence_patterns = [
            p for p in self.learned_patterns.values() 
            if p.confidence >= 0.8
        ]
        
        if high_confidence_patterns:
            lead = InvestigationLead(
                lead_id=f"lead_high_confidence_{len(self.investigation_leads)}",
                priority="HIGH",
                description=f"Investigate {len(high_confidence_patterns)} high-confidence patterns",
                supporting_evidence=[
                    ex for p in high_confidence_patterns for ex in p.examples
                ],
                recommended_actions=[
                    "Review high-confidence patterns for case-breaking insights",
                    "Cross-reference patterns with external evidence",
                    "Validate pattern conclusions with expert analysis",
                ],
                confidence=0.85,
            )
            leads.append(lead)
            self.investigation_leads.append(lead)
        
        # Lead 2: From anomalies
        anomaly_patterns = [
            p for p in self.learned_patterns.values()
            if p.category == PatternCategory.ANOMALY
        ]
        
        if anomaly_patterns:
            lead = InvestigationLead(
                lead_id=f"lead_anomalies_{len(self.investigation_leads)}",
                priority="CRITICAL",
                description=f"Investigate {len(anomaly_patterns)} anomalous patterns",
                supporting_evidence=[
                    ex for p in anomaly_patterns for ex in p.examples
                ],
                recommended_actions=[
                    "Examine anomalous patterns for potential fraud indicators",
                    "Request additional documentation for low-confidence items",
                    "Investigate isolated entities for hidden connections",
                ],
                confidence=0.9,
            )
            leads.append(lead)
            self.investigation_leads.append(lead)
        
        # Lead 3: From temporal patterns
        temporal_patterns = [
            p for p in self.learned_patterns.values()
            if p.category == PatternCategory.TEMPORAL
        ]
        
        if temporal_patterns:
            lead = InvestigationLead(
                lead_id=f"lead_temporal_{len(self.investigation_leads)}",
                priority="MEDIUM",
                description=f"Investigate {len(temporal_patterns)} temporal patterns",
                supporting_evidence=[
                    ex for p in temporal_patterns for ex in p.examples
                ],
                recommended_actions=[
                    "Analyze timing of events for coordination patterns",
                    "Check for suspicious timing around key dates",
                    "Correlate temporal patterns with external events",
                ],
                confidence=0.75,
            )
            leads.append(lead)
            self.investigation_leads.append(lead)
        
        return leads
    
    def introspect(self) -> Dict[str, Any]:
        """
        Perform introspective analysis of the knowledge base.
        
        Returns:
            Introspection report with insights and recommendations
        """
        logger.info("Performing introspective analysis...")
        
        # Analyze knowledge completeness
        entities = self.atomspace.get_atoms_by_type(AtomType.ENTITY)
        events = self.atomspace.get_atoms_by_type(AtomType.EVENT)
        relationships = self.atomspace.get_atoms_by_type(AtomType.RELATIONSHIP)
        evidence = self.atomspace.get_atoms_by_type(AtomType.EVIDENCE)
        patterns = self.atomspace.get_atoms_by_type(AtomType.PATTERN)
        
        # Compute knowledge graph metrics
        total_atoms = len(self.atomspace.atoms)
        avg_confidence = np.mean([a.truth_value.confidence for a in self.atomspace.atoms.values()])
        avg_strength = np.mean([a.truth_value.strength for a in self.atomspace.atoms.values()])
        
        # Identify gaps
        gaps = []
        if len(evidence) < len(events) * 0.5:
            gaps.append({
                "type": "evidence_gap",
                "description": "Low evidence coverage for events",
                "severity": "HIGH",
            })
        
        if len(relationships) < len(entities) * 0.3:
            gaps.append({
                "type": "relationship_gap",
                "description": "Sparse relationship network",
                "severity": "MEDIUM",
            })
        
        report = {
            "introspection_timestamp": datetime.now().isoformat(),
            "knowledge_base_metrics": {
                "total_atoms": total_atoms,
                "entities": len(entities),
                "events": len(events),
                "relationships": len(relationships),
                "evidence": len(evidence),
                "patterns": len(patterns),
                "average_confidence": float(avg_confidence),
                "average_strength": float(avg_strength),
            },
            "learned_patterns_summary": {
                "total_patterns": len(self.learned_patterns),
                "by_category": {
                    cat.value: len([p for p in self.learned_patterns.values() if p.category == cat])
                    for cat in PatternCategory
                },
            },
            "investigation_leads": [lead.to_dict() for lead in self.investigation_leads],
            "knowledge_gaps": gaps,
            "recommendations": self._generate_recommendations(gaps),
        }
        
        return report
    
    def _generate_recommendations(self, gaps: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on identified gaps"""
        recommendations = []
        
        for gap in gaps:
            if gap["type"] == "evidence_gap":
                recommendations.append(
                    "Gather additional evidence to support events in the timeline"
                )
            elif gap["type"] == "relationship_gap":
                recommendations.append(
                    "Map additional relationships between entities to strengthen the network"
                )
        
        if len(self.investigation_leads) > 0:
            recommendations.append(
                f"Prioritize investigation of {len(self.investigation_leads)} generated leads"
            )
        
        return recommendations
    
    def export_training_results(self, filepath: str):
        """Export training results to JSON file"""
        data = {
            "case_id": self.atomspace.case_id,
            "training_timestamp": datetime.now().isoformat(),
            "learned_patterns": {
                pid: pattern.to_dict() 
                for pid, pattern in self.learned_patterns.items()
            },
            "investigation_leads": [lead.to_dict() for lead in self.investigation_leads],
            "training_history": self.training_history,
            "pattern_statistics": dict(self.pattern_statistics),
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"Exported training results to {filepath}")


# Export key classes
__all__ = [
    "PatternCategory",
    "LearnedPattern",
    "InvestigationLead",
    "SuperSleuthTrainer",
]
