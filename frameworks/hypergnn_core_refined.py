#!/usr/bin/env python3
"""
Refined HyperGNN Framework Core
===============================

A truthful and accurate framework for network-based case analysis with evidence-based
methods and transparent limitations.

Key Improvements:
- Evidence-based risk assessment with configurable weights
- Transparent confidence scoring for all analyses
- Proper validation and error handling
- Clear documentation of actual capabilities
- No exaggerated claims or mock functionality
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Set, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from pathlib import Path

# Configure logging with proper formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AnalysisConfidence(Enum):
    """Confidence levels for analysis results"""
    HIGH = "high"  # Based on strong evidence with multiple sources
    MEDIUM = "medium"  # Based on partial evidence or single sources
    LOW = "low"  # Based on inference or limited data
    INSUFFICIENT = "insufficient"  # Not enough data for meaningful analysis


class ValidationError(Exception):
    """Raised when data validation fails"""
    pass


class DataIntegrityError(Exception):
    """Raised when data integrity checks fail"""
    pass


@dataclass
class RiskFactor:
    """
    Represents a specific risk factor with evidence-based scoring
    
    Attributes:
        name: Descriptive name of the risk factor
        weight: Importance weight (0.0 to 1.0)
        score: Current score for this factor (0.0 to 1.0)
        evidence: List of evidence supporting the score
        confidence: Confidence level in the assessment
    """
    name: str
    weight: float
    score: float
    evidence: List[str]
    confidence: AnalysisConfidence
    
    def __post_init__(self):
        if not 0.0 <= self.weight <= 1.0:
            raise ValidationError(f"Weight must be between 0.0 and 1.0, got {self.weight}")
        if not 0.0 <= self.score <= 1.0:
            raise ValidationError(f"Score must be between 0.0 and 1.0, got {self.score}")


@dataclass
class AnalysisResult:
    """
    Standardized result format for all analyses
    
    Attributes:
        analysis_type: Type of analysis performed
        results: Dictionary of analysis results
        confidence: Overall confidence level
        evidence_used: List of evidence items used
        limitations: Known limitations of this analysis
        timestamp: When analysis was performed
    """
    analysis_type: str
    results: Dict[str, Any]
    confidence: AnalysisConfidence
    evidence_used: List[str]
    limitations: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


class TensorType(Enum):
    """Types of tensors in the framework - limited to what we actually implement"""
    ADJACENCY = "adjacency"  # Network connections
    TEMPORAL = "temporal"  # Time-based relationships
    ATTRIBUTE = "attribute"  # Entity attributes


@dataclass
class NetworkTensor:
    """
    Simplified tensor representation for network analysis
    
    Note: This is a basic implementation using numpy arrays, not advanced tensor operations
    """
    tensor_type: TensorType
    data: np.ndarray
    labels: List[str]  # Entity labels for tensor dimensions
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if len(self.labels) != self.data.shape[0]:
            raise ValidationError("Number of labels must match tensor dimensions")


class AgentType(Enum):
    """Types of agents in the system"""
    INDIVIDUAL = "individual"
    ORGANIZATION = "organization"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class Agent:
    """
    Represents an entity in the case network
    
    Simplified from original - focuses on verifiable attributes only
    """
    agent_id: str
    agent_type: AgentType
    name: str
    verified_attributes: Dict[str, Any] = field(default_factory=dict)
    connections: Set[str] = field(default_factory=set)
    evidence_refs: List[str] = field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.agent_id or not self.agent_id.strip():
            raise ValidationError("Agent ID cannot be empty")
        if not self.name or not self.name.strip():
            raise ValidationError("Agent name cannot be empty")


@dataclass
class Event:
    """
    Represents a verified event in the timeline
    
    Simplified to focus on factual, evidence-based information
    """
    event_id: str
    timestamp: datetime
    event_type: str  # Free-form to allow domain-specific types
    actors: List[str]
    description: str
    evidence_refs: List[str]
    confidence: AnalysisConfidence
    verified: bool = False
    
    def __post_init__(self):
        if not self.event_id:
            raise ValidationError("Event ID cannot be empty")
        if not self.actors:
            raise ValidationError("Event must have at least one actor")
        if not self.evidence_refs:
            logger.warning(f"Event {self.event_id} has no evidence references")


class RefinedHyperGNNFramework:
    """
    Refined framework for network-based case analysis
    
    This version focuses on:
    - Accurate, evidence-based analysis
    - Transparent confidence scoring
    - Clear documentation of limitations
    - Proper validation and error handling
    """
    
    def __init__(self, case_id: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the framework
        
        Args:
            case_id: Unique identifier for the case
            config: Optional configuration dictionary
        """
        if not case_id or not case_id.strip():
            raise ValidationError("Case ID cannot be empty")
            
        self.case_id = case_id
        self.config = config or self._default_config()
        self.agents: Dict[str, Agent] = {}
        self.events: Dict[str, Event] = {}
        self.graph = nx.DiGraph()  # Simple directed graph, not hypergraph
        self.analysis_cache: Dict[str, AnalysisResult] = {}
        
        logger.info(f"Initialized Refined HyperGNN Framework for case: {case_id}")
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration with transparent settings"""
        return {
            "risk_weights": {
                "high_connectivity": 0.3,
                "temporal_clustering": 0.2,
                "evidence_quality": 0.5
            },
            "confidence_thresholds": {
                "high": 0.8,
                "medium": 0.5,
                "low": 0.2
            },
            "analysis_limits": {
                "max_network_size": 10000,
                "max_events": 50000,
                "max_time_range_days": 3650  # 10 years
            }
        }
    
    def add_agent(self, agent: Agent) -> None:
        """
        Add a verified agent to the framework
        
        Args:
            agent: Agent to add
            
        Raises:
            ValidationError: If agent data is invalid
            DataIntegrityError: If agent ID already exists
        """
        if agent.agent_id in self.agents:
            raise DataIntegrityError(f"Agent {agent.agent_id} already exists")
        
        # Validate agent data
        if agent.first_seen and agent.last_seen:
            if agent.first_seen > agent.last_seen:
                raise ValidationError("First seen date cannot be after last seen date")
        
        self.agents[agent.agent_id] = agent
        self.graph.add_node(
            agent.agent_id,
            type=agent.agent_type.value,
            name=agent.name,
            **agent.verified_attributes
        )
        
        # Clear affected analyses from cache
        self._invalidate_cache(['network', 'risk'])
        
        logger.debug(f"Added agent: {agent.name} ({agent.agent_id})")
    
    def add_event(self, event: Event) -> None:
        """
        Add a verified event to the framework
        
        Args:
            event: Event to add
            
        Raises:
            ValidationError: If event data is invalid
            DataIntegrityError: If event ID already exists
        """
        if event.event_id in self.events:
            raise DataIntegrityError(f"Event {event.event_id} already exists")
        
        # Validate all actors exist
        missing_actors = [a for a in event.actors if a not in self.agents]
        if missing_actors:
            logger.warning(f"Event references unknown actors: {missing_actors}")
        
        self.events[event.event_id] = event
        
        # Update agent connections based on event participation
        for i, actor1 in enumerate(event.actors):
            for actor2 in event.actors[i+1:]:
                if actor1 in self.agents and actor2 in self.agents:
                    self.agents[actor1].connections.add(actor2)
                    self.agents[actor2].connections.add(actor1)
                    
                    # Add edge if not exists
                    if not self.graph.has_edge(actor1, actor2):
                        self.graph.add_edge(actor1, actor2, events=[event.event_id])
                    else:
                        self.graph[actor1][actor2]['events'].append(event.event_id)
        
        # Clear affected analyses from cache
        self._invalidate_cache(['timeline', 'risk'])
        
        logger.debug(f"Added event: {event.event_id}")
    
    def analyze_risk(self, agent_id: str) -> AnalysisResult:
        """
        Perform evidence-based risk analysis for an agent
        
        Args:
            agent_id: ID of agent to analyze
            
        Returns:
            AnalysisResult with risk assessment
        """
        # Check cache first
        cache_key = f"risk_{agent_id}"
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]
        
        if agent_id not in self.agents:
            raise ValidationError(f"Agent {agent_id} not found")
        
        agent = self.agents[agent_id]
        risk_factors = []
        evidence_used = []
        
        # Factor 1: Network connectivity (evidence-based)
        connectivity_score = self._assess_connectivity_risk(agent)
        risk_factors.append(connectivity_score)
        evidence_used.extend(connectivity_score.evidence)
        
        # Factor 2: Temporal clustering of events
        temporal_score = self._assess_temporal_risk(agent)
        risk_factors.append(temporal_score)
        evidence_used.extend(temporal_score.evidence)
        
        # Factor 3: Evidence quality and quantity
        evidence_score = self._assess_evidence_quality(agent)
        risk_factors.append(evidence_score)
        evidence_used.extend(evidence_score.evidence)
        
        # Calculate weighted risk score
        total_weight = sum(rf.weight for rf in risk_factors)
        if total_weight > 0:
            risk_score = sum(rf.weight * rf.score for rf in risk_factors) / total_weight
        else:
            risk_score = 0.0
        
        # Determine overall confidence
        confidence = self._determine_confidence(risk_factors)
        
        # Determine risk level based on score
        if risk_score >= 0.7:
            risk_level = "high"
        elif risk_score >= 0.4:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        result = AnalysisResult(
            analysis_type="risk_assessment",
            results={
                "agent_id": agent_id,
                "agent_name": agent.name,
                "risk_score": round(risk_score, 3),
                "risk_level": risk_level,
                "risk_factors": [
                    {
                        "name": rf.name,
                        "score": round(rf.score, 3),
                        "weight": rf.weight,
                        "confidence": rf.confidence.value
                    }
                    for rf in risk_factors
                ]
            },
            confidence=confidence,
            evidence_used=list(set(evidence_used)),
            limitations=[
                "Risk assessment based on available network data only",
                "Does not include external factors or context",
                "Weights are configurable and may need domain-specific adjustment"
            ]
        )
        
        # Cache the result
        self.analysis_cache[cache_key] = result
        
        return result
    
    def _assess_connectivity_risk(self, agent: Agent) -> RiskFactor:
        """Assess risk based on network connectivity patterns"""
        degree = self.graph.degree(agent.agent_id) if agent.agent_id in self.graph else 0
        total_agents = len(self.agents)
        
        if total_agents <= 1:
            connectivity_ratio = 0.0
        else:
            connectivity_ratio = degree / (total_agents - 1)
        
        # Evidence-based scoring
        evidence = []
        if degree > 0:
            evidence.append(f"Connected to {degree} other agents")
        
        # Check for connection patterns
        if agent.agent_id in self.graph:
            neighbors = list(self.graph.neighbors(agent.agent_id))
            high_risk_connections = [
                n for n in neighbors 
                if self.agents.get(n) and len(self.agents[n].connections) > 5
            ]
            if high_risk_connections:
                evidence.append(f"Connected to {len(high_risk_connections)} highly connected agents")
        
        # Determine score and confidence
        if degree == 0:
            score = 0.0
            confidence = AnalysisConfidence.HIGH
        elif degree < 3:
            score = 0.2
            confidence = AnalysisConfidence.HIGH
        elif degree < 10:
            score = 0.5
            confidence = AnalysisConfidence.MEDIUM
        else:
            score = min(0.9, connectivity_ratio * 2)
            confidence = AnalysisConfidence.HIGH
        
        return RiskFactor(
            name="Network Connectivity",
            weight=self.config["risk_weights"]["high_connectivity"],
            score=score,
            evidence=evidence,
            confidence=confidence
        )
    
    def _assess_temporal_risk(self, agent: Agent) -> RiskFactor:
        """Assess risk based on temporal event patterns"""
        # Find all events involving this agent
        agent_events = [
            e for e in self.events.values()
            if agent.agent_id in e.actors
        ]
        
        evidence = []
        
        if not agent_events:
            return RiskFactor(
                name="Temporal Clustering",
                weight=self.config["risk_weights"]["temporal_clustering"],
                score=0.0,
                evidence=["No events found for agent"],
                confidence=AnalysisConfidence.HIGH
            )
        
        evidence.append(f"Involved in {len(agent_events)} events")
        
        # Sort events by timestamp
        agent_events.sort(key=lambda e: e.timestamp)
        
        # Calculate clustering score
        if len(agent_events) < 2:
            clustering_score = 0.1
            confidence = AnalysisConfidence.LOW
        else:
            # Calculate time gaps between consecutive events
            gaps = []
            for i in range(1, len(agent_events)):
                gap = (agent_events[i].timestamp - agent_events[i-1].timestamp).days
                gaps.append(gap)
            
            avg_gap = sum(gaps) / len(gaps)
            
            # Identify clusters (events within 7 days of each other)
            clusters = 0
            current_cluster_size = 1
            
            for gap in gaps:
                if gap <= 7:
                    current_cluster_size += 1
                else:
                    if current_cluster_size > 2:
                        clusters += 1
                        evidence.append(f"Cluster of {current_cluster_size} events detected")
                    current_cluster_size = 1
            
            if current_cluster_size > 2:
                clusters += 1
                evidence.append(f"Cluster of {current_cluster_size} events detected")
            
            # Score based on clustering
            if clusters == 0:
                clustering_score = 0.2
            elif clusters == 1:
                clustering_score = 0.5
            else:
                clustering_score = min(0.9, clusters * 0.3)
            
            confidence = AnalysisConfidence.MEDIUM if len(agent_events) > 5 else AnalysisConfidence.LOW
        
        return RiskFactor(
            name="Temporal Clustering",
            weight=self.config["risk_weights"]["temporal_clustering"],
            score=clustering_score,
            evidence=evidence,
            confidence=confidence
        )
    
    def _assess_evidence_quality(self, agent: Agent) -> RiskFactor:
        """Assess risk based on evidence quality and quantity"""
        evidence = []
        
        # Check direct evidence
        direct_evidence_count = len(agent.evidence_refs)
        evidence.append(f"{direct_evidence_count} direct evidence items")
        
        # Check event evidence
        event_evidence = set()
        for event in self.events.values():
            if agent.agent_id in event.actors:
                event_evidence.update(event.evidence_refs)
        
        evidence.append(f"{len(event_evidence)} event-related evidence items")
        
        # Calculate evidence score
        total_evidence = direct_evidence_count + len(event_evidence)
        
        if total_evidence == 0:
            score = 0.0
            confidence = AnalysisConfidence.INSUFFICIENT
        elif total_evidence < 3:
            score = 0.3
            confidence = AnalysisConfidence.LOW
        elif total_evidence < 10:
            score = 0.6
            confidence = AnalysisConfidence.MEDIUM
        else:
            score = min(0.9, total_evidence / 20)
            confidence = AnalysisConfidence.HIGH
        
        # Check for verified events
        verified_events = sum(1 for e in self.events.values() 
                            if agent.agent_id in e.actors and e.verified)
        if verified_events > 0:
            evidence.append(f"{verified_events} verified events")
            score = min(1.0, score + 0.1)
        
        return RiskFactor(
            name="Evidence Quality",
            weight=self.config["risk_weights"]["evidence_quality"],
            score=score,
            evidence=evidence,
            confidence=confidence
        )
    
    def _determine_confidence(self, risk_factors: List[RiskFactor]) -> AnalysisConfidence:
        """Determine overall confidence based on individual factor confidence"""
        if not risk_factors:
            return AnalysisConfidence.INSUFFICIENT
        
        # Use weighted average of confidence scores
        confidence_scores = {
            AnalysisConfidence.HIGH: 1.0,
            AnalysisConfidence.MEDIUM: 0.6,
            AnalysisConfidence.LOW: 0.3,
            AnalysisConfidence.INSUFFICIENT: 0.0
        }
        
        total_weight = sum(rf.weight for rf in risk_factors)
        if total_weight == 0:
            return AnalysisConfidence.INSUFFICIENT
        
        weighted_confidence = sum(
            rf.weight * confidence_scores[rf.confidence] 
            for rf in risk_factors
        ) / total_weight
        
        # Map back to confidence level
        if weighted_confidence >= self.config["confidence_thresholds"]["high"]:
            return AnalysisConfidence.HIGH
        elif weighted_confidence >= self.config["confidence_thresholds"]["medium"]:
            return AnalysisConfidence.MEDIUM
        elif weighted_confidence >= self.config["confidence_thresholds"]["low"]:
            return AnalysisConfidence.LOW
        else:
            return AnalysisConfidence.INSUFFICIENT
    
    def _invalidate_cache(self, analysis_types: List[str]) -> None:
        """Invalidate cached analyses of specified types"""
        keys_to_remove = []
        for key in self.analysis_cache:
            if any(atype in key for atype in analysis_types):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.analysis_cache[key]
    
    def generate_network_tensor(self) -> NetworkTensor:
        """
        Generate adjacency matrix representation of the network
        
        Returns:
            NetworkTensor with adjacency matrix
        """
        if not self.agents:
            raise ValidationError("No agents in framework")
        
        # Create ordered list of agent IDs
        agent_ids = sorted(self.agents.keys())
        n = len(agent_ids)
        
        # Create adjacency matrix
        adj_matrix = np.zeros((n, n), dtype=np.float32)
        
        for i, agent1 in enumerate(agent_ids):
            for j, agent2 in enumerate(agent_ids):
                if i != j and self.graph.has_edge(agent1, agent2):
                    # Weight by number of shared events
                    edge_data = self.graph[agent1][agent2]
                    weight = len(edge_data.get('events', []))
                    adj_matrix[i, j] = min(1.0, weight / 10.0)  # Normalize
        
        return NetworkTensor(
            tensor_type=TensorType.ADJACENCY,
            data=adj_matrix,
            labels=agent_ids,
            timestamp=datetime.now(),
            metadata={
                "normalization": "events/10",
                "directed": True
            }
        )
    
    def export_analysis_report(self) -> Dict[str, Any]:
        """
        Export comprehensive analysis report with transparent methodology
        
        Returns:
            Dictionary containing analysis results and metadata
        """
        report = {
            "case_id": self.case_id,
            "generated_at": datetime.now().isoformat(),
            "framework_version": "1.0.0-refined",
            "data_summary": {
                "total_agents": len(self.agents),
                "total_events": len(self.events),
                "graph_nodes": self.graph.number_of_nodes(),
                "graph_edges": self.graph.number_of_edges()
            },
            "methodology": {
                "risk_assessment": "Evidence-based scoring with configurable weights",
                "confidence_scoring": "Weighted average of factor confidence",
                "limitations": [
                    "Analysis limited to network structure and temporal patterns",
                    "Does not include external context or domain knowledge",
                    "Risk weights may need adjustment for specific domains"
                ]
            },
            "configuration": self.config,
            "analyses_performed": list(set(
                result.analysis_type for result in self.analysis_cache.values()
            ))
        }
        
        # Add sample risk analyses for top connected agents
        if self.agents:
            top_agents = sorted(
                self.agents.keys(),
                key=lambda a: len(self.agents[a].connections),
                reverse=True
            )[:5]
            
            report["sample_risk_analyses"] = []
            for agent_id in top_agents:
                try:
                    risk_result = self.analyze_risk(agent_id)
                    report["sample_risk_analyses"].append(risk_result.results)
                except Exception as e:
                    logger.error(f"Failed to analyze risk for {agent_id}: {e}")
        
        return report


# Example usage demonstrating the refined framework
if __name__ == "__main__":
    # Create framework with transparent configuration
    framework = RefinedHyperGNNFramework("example_case_001")
    
    # Add verified agents
    agent1 = Agent(
        agent_id="person_001",
        agent_type=AgentType.INDIVIDUAL,
        name="John Doe",
        verified_attributes={"role": "witness", "verified": True},
        evidence_refs=["doc_001", "doc_002"]
    )
    
    agent2 = Agent(
        agent_id="org_001",
        agent_type=AgentType.ORGANIZATION,
        name="ABC Corporation",
        verified_attributes={"type": "financial_institution"},
        evidence_refs=["doc_003"]
    )
    
    framework.add_agent(agent1)
    framework.add_agent(agent2)
    
    # Add verified event
    event = Event(
        event_id="evt_001",
        timestamp=datetime.now() - timedelta(days=30),
        event_type="financial_transaction",
        actors=["person_001", "org_001"],
        description="Verified transaction between parties",
        evidence_refs=["doc_004", "doc_005"],
        confidence=AnalysisConfidence.HIGH,
        verified=True
    )
    
    framework.add_event(event)
    
    # Perform risk analysis
    risk_analysis = framework.analyze_risk("person_001")
    
    # Export report
    report = framework.export_analysis_report()
    
    print(json.dumps(report, indent=2, default=str))