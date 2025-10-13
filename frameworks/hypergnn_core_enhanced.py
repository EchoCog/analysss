#!/usr/bin/env python3
"""
Enhanced HyperGNN Framework Core
===============================

A comprehensive framework for multilayer network modeling, timeline tensor states,
and generalized case solving across any degree of complexity and dimensions.

This enhanced version includes:
- Comprehensive type hints for all functions and methods
- Detailed docstrings with parameter and return value descriptions
- Improved error handling and validation
- Performance optimizations

Focus: Professional investigative analysis with clarity and accuracy.
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TensorType(Enum):
    """Types of tensors in the HyperGNN framework"""
    ACTIVITY = "activity"
    KNOWLEDGE = "knowledge"
    INFLUENCE = "influence"
    RESOURCE = "resource"
    TEMPORAL = "temporal"
    RELATIONSHIP = "relationship"


class AgentType(Enum):
    """Types of agents in the multi-agent system"""
    INDIVIDUAL = "individual"
    GROUP = "group"
    ORGANIZATION = "organization"
    SYSTEM = "system"


class FlowType(Enum):
    """Types of flows in system dynamics model"""
    FINANCIAL = "financial"
    MATERIAL = "material"
    INFORMATION = "information"
    INFLUENCE = "influence"
    LEVERAGE = "leverage"
    DECEPTION = "deception"


class EventType(Enum):
    """Types of discrete events"""
    COMMUNICATION = "communication"
    TRANSACTION = "transaction"
    MEETING = "meeting"
    DECISION = "decision"
    ACTION = "action"
    EVIDENCE = "evidence"


@dataclass
class TimelineTensor:
    """
    Represents a tensor state at a specific point in time
    
    Attributes:
        timestamp: The time point for this tensor state
        tensor_type: The type of tensor (activity, knowledge, etc.)
        dimensions: Shape of the tensor data
        data: The actual tensor data as numpy array
        metadata: Additional metadata about the tensor
        confidence_score: Confidence level in the tensor data (0.0 to 1.0)
        source_evidence: List of evidence sources supporting this tensor
    """
    timestamp: datetime
    tensor_type: TensorType
    dimensions: Tuple[int, ...]
    data: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 1.0
    source_evidence: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate tensor data after initialization"""
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        if self.data.shape != self.dimensions:
            raise ValueError("Data shape does not match specified dimensions")


@dataclass
class Agent:
    """
    Represents an agent in the multi-agent system
    
    Attributes:
        agent_id: Unique identifier for the agent
        agent_type: Type of agent (individual, group, organization, system)
        name: Human-readable name for the agent
        activity_tensors: Timeline of activity tensors for this agent
        knowledge_tensors: Timeline of knowledge tensors for this agent
        professional_links: Set of professional connections to other agents
        social_links: Set of social connections to other agents
        attributes: Additional agent attributes
    """
    agent_id: str
    agent_type: AgentType
    name: str
    activity_tensors: Dict[datetime, TimelineTensor] = field(default_factory=dict)
    knowledge_tensors: Dict[datetime, TimelineTensor] = field(default_factory=dict)
    professional_links: Set[str] = field(default_factory=set)
    social_links: Set[str] = field(default_factory=set)
    attributes: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate agent data after initialization"""
        if not self.agent_id:
            raise ValueError("Agent ID cannot be empty")
        if not self.name:
            raise ValueError("Agent name cannot be empty")


@dataclass
class DiscreteEvent:
    """
    Represents a discrete event in the timeline
    
    Attributes:
        event_id: Unique identifier for the event
        timestamp: When the event occurred
        event_type: Type of event (communication, transaction, etc.)
        actors: List of agent IDs involved in the event
        description: Human-readable description of the event
        implications: List of implications or consequences
        evidence_refs: References to supporting evidence
        motive_analysis: Analysis of motives behind the event
        means_analysis: Analysis of means used in the event
        opportunity_analysis: Analysis of opportunities that enabled the event
        hostility_assessment: Assessment of hostility levels
    """
    event_id: str
    timestamp: datetime
    event_type: EventType
    actors: List[str]
    description: str
    implications: List[str] = field(default_factory=list)
    evidence_refs: List[str] = field(default_factory=list)
    motive_analysis: Optional[str] = None
    means_analysis: Optional[str] = None
    opportunity_analysis: Optional[str] = None
    hostility_assessment: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate event data after initialization"""
        if not self.event_id:
            raise ValueError("Event ID cannot be empty")
        if not self.actors:
            raise ValueError("Event must have at least one actor")


@dataclass
class SystemFlow:
    """
    Represents a flow in the system dynamics model
    
    Attributes:
        flow_id: Unique identifier for the flow
        flow_type: Type of flow (financial, material, information, etc.)
        source: Source agent ID
        target: Target agent ID
        timestamp: When the flow occurred
        magnitude: Magnitude or strength of the flow
        description: Human-readable description of the flow
        evidence: List of evidence supporting this flow
    """
    flow_id: str
    flow_type: FlowType
    source: str
    target: str
    timestamp: datetime
    magnitude: float
    description: str
    evidence: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate flow data after initialization"""
        if not self.flow_id:
            raise ValueError("Flow ID cannot be empty")
        if self.source == self.target:
            raise ValueError("Source and target cannot be the same")


class HyperGNNFramework:
    """
    Enhanced HyperGNN Framework for comprehensive case analysis

    Provides multilayer network modeling with timeline tensor states
    for generalized case solving across any complexity and dimensions.
    
    This enhanced version includes improved type safety, error handling,
    and performance optimizations.
    """

    def __init__(self, case_id: str) -> None:
        """
        Initialize the HyperGNN Framework
        
        Args:
            case_id: Unique identifier for the case being analyzed
            
        Raises:
            ValueError: If case_id is empty or invalid
        """
        if not case_id:
            raise ValueError("Case ID cannot be empty")
            
        self.case_id = case_id
        self.agents: Dict[str, Agent] = {}
        self.events: Dict[str, DiscreteEvent] = {}
        self.flows: Dict[str, SystemFlow] = {}
        self.hypergraph = nx.MultiDiGraph()
        self.timeline_tensors: Dict[datetime, Dict[str, TimelineTensor]] = {}
        self.evidence_repository: Dict[str, Dict[str, Any]] = {}
        
        logger.info(f"Initialized HyperGNN Framework for case: {case_id}")

    def add_agent(self, agent: Agent) -> None:
        """
        Add an agent to the framework
        
        Args:
            agent: The agent to add to the framework
            
        Raises:
            ValueError: If agent with same ID already exists
        """
        if agent.agent_id in self.agents:
            raise ValueError(f"Agent with ID {agent.agent_id} already exists")
            
        self.agents[agent.agent_id] = agent
        self.hypergraph.add_node(
            agent.agent_id,
            type="agent",
            agent_type=agent.agent_type.value,
            name=agent.name,
        )
        logger.debug(f"Added agent: {agent.name} ({agent.agent_id})")

    def add_event(self, event: DiscreteEvent) -> None:
        """
        Add a discrete event to the framework
        
        Args:
            event: The event to add to the framework
            
        Raises:
            ValueError: If event with same ID already exists
        """
        if event.event_id in self.events:
            raise ValueError(f"Event with ID {event.event_id} already exists")
            
        self.events[event.event_id] = event
        self.hypergraph.add_node(
            event.event_id,
            type="event",
            event_type=event.event_type.value,
            timestamp=event.timestamp.isoformat(),
        )

        # Connect event to actors
        for actor in event.actors:
            if actor in self.agents:
                self.hypergraph.add_edge(
                    actor, event.event_id, relationship="participates_in"
                )
            else:
                logger.warning(f"Actor {actor} not found in agents when adding event {event.event_id}")
                
        logger.debug(f"Added event: {event.description} ({event.event_id})")

    def add_flow(self, flow: SystemFlow) -> None:
        """
        Add a system flow to the framework
        
        Args:
            flow: The flow to add to the framework
            
        Raises:
            ValueError: If flow with same ID already exists
        """
        if flow.flow_id in self.flows:
            raise ValueError(f"Flow with ID {flow.flow_id} already exists")
            
        self.flows[flow.flow_id] = flow

        # Add flow as edge in hypergraph
        self.hypergraph.add_edge(
            flow.source,
            flow.target,
            key=flow.flow_id,
            flow_type=flow.flow_type.value,
            magnitude=flow.magnitude,
            timestamp=flow.timestamp.isoformat(),
            description=flow.description,
        )
        logger.debug(f"Added flow: {flow.description} ({flow.flow_id})")

    def create_timeline_tensor(
        self,
        timestamp: datetime,
        tensor_type: TensorType,
        data: np.ndarray,
        metadata: Optional[Dict[str, Any]] = None,
        confidence_score: float = 1.0,
        source_evidence: Optional[List[str]] = None
    ) -> TimelineTensor:
        """
        Create a timeline tensor for a specific timestamp
        
        Args:
            timestamp: The time point for this tensor
            tensor_type: Type of tensor to create
            data: The tensor data as numpy array
            metadata: Optional metadata dictionary
            confidence_score: Confidence level (0.0 to 1.0)
            source_evidence: Optional list of evidence sources
            
        Returns:
            The created TimelineTensor object
            
        Raises:
            ValueError: If confidence_score is not between 0.0 and 1.0
        """
        if metadata is None:
            metadata = {}
        if source_evidence is None:
            source_evidence = []

        tensor = TimelineTensor(
            timestamp=timestamp,
            tensor_type=tensor_type,
            dimensions=data.shape,
            data=data,
            metadata=metadata,
            confidence_score=confidence_score,
            source_evidence=source_evidence
        )

        if timestamp not in self.timeline_tensors:
            self.timeline_tensors[timestamp] = {}

        self.timeline_tensors[timestamp][tensor_type.value] = tensor
        logger.debug(f"Created timeline tensor: {tensor_type.value} at {timestamp}")
        return tensor

    def analyze_motive_means_opportunity(
        self, agent_id: str, event_id: str
    ) -> Dict[str, Any]:
        """
        Analyze motive, means, and opportunity for an agent regarding an event
        
        Args:
            agent_id: ID of the agent to analyze
            event_id: ID of the event to analyze
            
        Returns:
            Dictionary containing analysis results with motive, means, and opportunity factors
            
        Raises:
            ValueError: If agent or event not found
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not found")
        if event_id not in self.events:
            raise ValueError(f"Event {event_id} not found")

        agent = self.agents[agent_id]
        event = self.events[event_id]

        analysis = {
            "agent": agent.name,
            "event": event.description,
            "motive_indicators": self._analyze_motive_indicators(agent, event),
            "means_available": self._analyze_available_means(agent, event),
            "opportunity_factors": self._analyze_opportunity_factors(agent, event),
            "risk_assessment": self._assess_risk_level(agent, event),
        }

        return analysis

    def _analyze_motive_indicators(self, agent: Agent, event: DiscreteEvent) -> List[str]:
        """
        Analyze potential motive indicators for an agent regarding an event
        
        Args:
            agent: The agent to analyze
            event: The event to analyze
            
        Returns:
            List of motive indicators
        """
        indicators = []
        
        # Analyze based on agent's connections and attributes
        if len(agent.professional_links) > 5:
            indicators.append("High professional connectivity")
        
        if event.event_type == EventType.COMMUNICATION and agent.agent_id in event.actors:
            indicators.append("Direct involvement in communication")
            
        return indicators

    def _analyze_available_means(self, agent: Agent, event: DiscreteEvent) -> List[str]:
        """
        Analyze available means for an agent regarding an event
        
        Args:
            agent: The agent to analyze
            event: The event to analyze
            
        Returns:
            List of available means
        """
        means = []
        
        if agent.agent_type == AgentType.ORGANIZATION:
            means.append("Organizational resources")
            
        if len(agent.professional_links) > 0:
            means.append("Professional network access")
            
        return means

    def _analyze_opportunity_factors(self, agent: Agent, event: DiscreteEvent) -> List[str]:
        """
        Analyze opportunity factors for an agent regarding an event
        
        Args:
            agent: The agent to analyze
            event: The event to analyze
            
        Returns:
            List of opportunity factors
        """
        factors = []
        
        if agent.agent_id in event.actors:
            factors.append("Direct participation in event")
            
        # Check temporal proximity to other events
        related_events = [e for e in self.events.values() 
                         if agent.agent_id in e.actors and 
                         abs((e.timestamp - event.timestamp).total_seconds()) < 86400]
        
        if len(related_events) > 1:
            factors.append("Multiple related events in timeframe")
            
        return factors

    def _assess_risk_level(self, agent: Agent, event: DiscreteEvent) -> str:
        """
        Assess risk level for an agent regarding an event
        
        Args:
            agent: The agent to analyze
            event: The event to analyze
            
        Returns:
            Risk level assessment string
        """
        risk_factors = 0
        
        if agent.agent_id in event.actors:
            risk_factors += 2
            
        if len(agent.professional_links) > 3:
            risk_factors += 1
            
        if event.event_type in [EventType.TRANSACTION, EventType.DECISION]:
            risk_factors += 1
            
        if risk_factors >= 3:
            return "high"
        elif risk_factors >= 2:
            return "medium"
        else:
            return "low"

    def export_professional_report(self) -> Dict[str, Any]:
        """
        Export comprehensive professional analysis report
        
        Returns:
            Dictionary containing complete analysis report with facts, evidence, and relationships
        """
        try:
            return {
                "case_id": self.case_id,
                "analysis_timestamp": datetime.now().isoformat(),
                "agent_summary": {
                    "total_agents": len(self.agents),
                    "agent_types": {
                        t.value: len([a for a in self.agents.values() if a.agent_type == t])
                        for t in AgentType
                    },
                },
                "event_summary": {
                    "total_events": len(self.events),
                    "event_types": {
                        t.value: len([e for e in self.events.values() if e.event_type == t])
                        for t in EventType
                    },
                },
                "flow_analysis": {
                    "total_flows": len(self.flows),
                    "flow_types": {
                        t.value: len([f for f in self.flows.values() if f.flow_type == t])
                        for t in FlowType
                    },
                },
                "network_metrics": self._calculate_network_metrics(),
                "timeline_analysis": self._analyze_timeline_patterns(),
                "risk_assessment": self._generate_risk_assessment(),
            }
        except Exception as e:
            logger.error(f"Error generating professional report: {e}")
            return {"error": f"Report generation failed: {str(e)}"}

    def _calculate_network_metrics(self) -> Dict[str, Any]:
        """
        Calculate network metrics for the hypergraph
        
        Returns:
            Dictionary containing network metrics
        """
        if self.hypergraph.number_of_nodes() == 0:
            return {"nodes": 0, "edges": 0, "density": 0.0}
            
        return {
            "nodes": self.hypergraph.number_of_nodes(),
            "edges": self.hypergraph.number_of_edges(),
            "density": nx.density(self.hypergraph) if self.hypergraph.number_of_nodes() > 1 else 0.0,
            "connected_components": nx.number_weakly_connected_components(self.hypergraph),
        }

    def _analyze_timeline_patterns(self) -> Dict[str, Any]:
        """
        Analyze patterns in the timeline data
        
        Returns:
            Dictionary containing timeline pattern analysis
        """
        if not self.events:
            return {"total_events": 0, "time_span": "No events"}
            
        event_times = [event.timestamp for event in self.events.values()]
        time_span = max(event_times) - min(event_times)
        
        return {
            "total_events": len(self.events),
            "time_span": str(time_span),
            "earliest_event": min(event_times).isoformat(),
            "latest_event": max(event_times).isoformat(),
            "event_frequency": len(self.events) / max(1, time_span.days),
        }

    def _generate_risk_assessment(self) -> Dict[str, Any]:
        """
        Generate overall risk assessment for the case
        
        Returns:
            Dictionary containing risk assessment
        """
        high_risk_events = [
            event for event in self.events.values()
            if event.event_type in [EventType.TRANSACTION, EventType.DECISION]
        ]
        
        high_connectivity_agents = [
            agent for agent in self.agents.values()
            if len(agent.professional_links) + len(agent.social_links) > 5
        ]
        
        risk_level = "low"
        if len(high_risk_events) > 3 or len(high_connectivity_agents) > 2:
            risk_level = "high"
        elif len(high_risk_events) > 1 or len(high_connectivity_agents) > 0:
            risk_level = "medium"
            
        return {
            "overall_risk_level": risk_level,
            "high_risk_events": len(high_risk_events),
            "high_connectivity_agents": len(high_connectivity_agents),
            "risk_factors": self._identify_risk_factors(),
        }

    def _identify_risk_factors(self) -> List[str]:
        """
        Identify specific risk factors in the case
        
        Returns:
            List of identified risk factors
        """
        factors = []
        
        if len(self.flows) > 10:
            factors.append("High volume of system flows")
            
        if any(flow.flow_type == FlowType.DECEPTION for flow in self.flows.values()):
            factors.append("Deception patterns detected")
            
        if len(self.agents) > 20:
            factors.append("Large number of involved parties")
            
        return factors


def create_sample_framework() -> HyperGNNFramework:
    """
    Create a sample framework for testing and demonstration
    
    Returns:
        A configured HyperGNNFramework instance with sample data
    """
    framework = HyperGNNFramework("sample_case_001")

    # Add sample agents
    agent1 = Agent("agent_001", AgentType.INDIVIDUAL, "John Doe")
    agent2 = Agent("agent_002", AgentType.INDIVIDUAL, "Jane Smith")
    agent3 = Agent("agent_003", AgentType.ORGANIZATION, "ABC Corp")

    agent1.professional_links.add("agent_002")
    agent2.social_links.add("agent_001")

    framework.add_agent(agent1)
    framework.add_agent(agent2)
    framework.add_agent(agent3)

    # Add sample event
    event = DiscreteEvent(
        "event_001",
        datetime.now(),
        EventType.COMMUNICATION,
        ["agent_001", "agent_002"],
        "Professional correspondence regarding case matter",
    )
    framework.add_event(event)

    # Add sample flow
    flow = SystemFlow(
        "flow_001",
        FlowType.INFORMATION,
        "agent_001",
        "agent_002",
        datetime.now(),
        1.0,
        "Information transfer via professional channel",
    )
    framework.add_flow(flow)

    return framework


if __name__ == "__main__":
    # Demonstrate framework capabilities
    try:
        framework = create_sample_framework()
        report = framework.export_professional_report()
        print(json.dumps(report, indent=2, default=str))
    except Exception as e:
        logger.error(f"Error in demonstration: {e}")
        print(f"Error: {e}")
