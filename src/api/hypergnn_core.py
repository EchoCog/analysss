#!/usr/bin/env python3
"""
HyperGNN Framework Core
======================

A comprehensive framework for multilayer network modeling, timeline tensor states,
and generalized case solving across any degree of complexity and dimensions.

This framework integrates:
1. Multi-agent models with individual and group activity tensors
2. Discrete event models for timeline-to-action mapping
3. System dynamics models for tracking stocks and flows
4. Professional evidence management system

Focus: Professional investigative analysis with clarity and accuracy.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
import numpy as np


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
    """Represents a tensor state at a specific point in time"""

    timestamp: datetime
    tensor_type: TensorType
    dimensions: Tuple[int, ...]
    data: np.ndarray
    metadata: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 1.0
    source_evidence: List[str] = field(default_factory=list)


@dataclass
class Agent:
    """Represents an agent in the multi-agent system"""

    agent_id: str
    agent_type: AgentType
    name: str
    activity_tensors: Dict[datetime, TimelineTensor] = field(default_factory=dict)
    knowledge_tensors: Dict[datetime, TimelineTensor] = field(default_factory=dict)
    professional_links: Set[str] = field(default_factory=set)
    social_links: Set[str] = field(default_factory=set)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiscreteEvent:
    """Represents a discrete event in the timeline"""

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

    # Enhanced properties for legal analysis
    criminal_significance: float = 0.0
    commercial_significance: float = 0.0
    legal_categories: List[str] = field(default_factory=list)
    causal_predecessors: List[str] = field(
        default_factory=list
    )  # Events that caused this
    causal_successors: List[str] = field(default_factory=list)  # Events this caused
    timeline_criticality: float = (
        0.0  # How critical this event is to the overall timeline
    )

    def analyze_legal_significance(self) -> Dict[str, float]:
        """
        Analyze the legal significance of this event for criminal and commercial law.

        Returns:
            Dictionary with significance scores for different legal domains
        """
        criminal_keywords = {
            "murder": 0.9,
            "killed": 0.8,
            "violence": 0.7,
            "assault": 0.7,
            "police": 0.6,
            "investigation": 0.5,
            "forensic": 0.6,
            "evidence tampering": 0.8,
            "witness": 0.4,
            "testimony": 0.5,
            "criminal charge": 0.7,
            "victim": 0.6,
        }

        commercial_keywords = {
            "fraud": 0.8,
            "contract": 0.6,
            "breach": 0.7,
            "debt": 0.5,
            "payment": 0.4,
            "financial": 0.5,
            "misrepresentation": 0.8,
            "fiduciary": 0.7,
            "settlement": 0.6,
            "damages": 0.6,
            "business": 0.4,
            "transaction": 0.5,
        }

        description_lower = self.description.lower()

        # Calculate weighted criminal significance
        criminal_score = 0.0
        for keyword, weight in criminal_keywords.items():
            if keyword in description_lower:
                criminal_score += weight
        self.criminal_significance = min(1.0, criminal_score)

        # Calculate weighted commercial significance
        commercial_score = 0.0
        for keyword, weight in commercial_keywords.items():
            if keyword in description_lower:
                commercial_score += weight
        self.commercial_significance = min(1.0, commercial_score)

        # Determine legal categories
        self.legal_categories = []
        if self.criminal_significance > 0.4:
            self.legal_categories.append("criminal")
        if self.commercial_significance > 0.4:
            self.legal_categories.append("commercial")
        if not self.legal_categories:
            self.legal_categories.append("procedural")

        return {
            "criminal": self.criminal_significance,
            "commercial": self.commercial_significance,
        }

    def calculate_timeline_criticality(
        self, all_events: List["DiscreteEvent"]
    ) -> float:
        """
        Calculate how critical this event is to the overall timeline.

        Args:
            all_events: All events in the timeline for context

        Returns:
            Criticality score from 0.0 to 1.0
        """
        criticality_score = 0.0

        # High-impact event types get base score
        if self.criminal_significance > 0.6:
            criticality_score += 0.4
        if self.commercial_significance > 0.6:
            criticality_score += 0.3

        # Events with many actors are more critical
        if len(self.actors) > 2:
            criticality_score += 0.2

        # Events that cause many other events are critical
        causal_impact = len(self.causal_successors) * 0.1
        criticality_score += min(0.3, causal_impact)

        # Events with strong evidence are more critical
        if len(self.evidence_refs) > 2:
            criticality_score += 0.1

        self.timeline_criticality = min(1.0, criticality_score)
        return self.timeline_criticality


@dataclass
class SystemFlow:
    """Represents a flow in the system dynamics model"""

    flow_id: str
    flow_type: FlowType
    source: str
    target: str
    timestamp: datetime
    magnitude: float
    description: str
    evidence: List[str] = field(default_factory=list)

    # Enhanced properties for resource tracking
    resource_category: str = "general"  # financial, material, information, legal_power
    legal_significance: float = 0.0  # Legal importance of this flow
    flow_legitimacy: float = 0.5  # 0.0 = illegitimate, 1.0 = fully legitimate
    impact_assessment: Dict[str, float] = field(
        default_factory=dict
    )  # Impact on different dimensions

    def categorize_flow_type(self) -> str:
        """
        Categorize the flow type based on description and flow_type.

        Returns:
            Detailed resource category
        """
        description_lower = self.description.lower()

        financial_indicators = [
            "payment",
            "money",
            "debt",
            "loan",
            "invoice",
            "fund",
            "financial",
        ]
        material_indicators = ["property", "asset", "equipment", "document", "physical"]
        information_indicators = [
            "data",
            "information",
            "knowledge",
            "intelligence",
            "communication",
        ]
        legal_indicators = [
            "power",
            "authority",
            "control",
            "legal",
            "court order",
            "jurisdiction",
        ]

        if any(indicator in description_lower for indicator in financial_indicators):
            self.resource_category = "financial"
        elif any(indicator in description_lower for indicator in material_indicators):
            self.resource_category = "material"
        elif any(
            indicator in description_lower for indicator in information_indicators
        ):
            self.resource_category = "information"
        elif any(indicator in description_lower for indicator in legal_indicators):
            self.resource_category = "legal_power"
        else:
            self.resource_category = "general"

        return self.resource_category

    def assess_legal_significance(self) -> float:
        """
        Assess the legal significance of this resource flow.

        Returns:
            Legal significance score from 0.0 to 1.0
        """
        description_lower = self.description.lower()

        high_significance_terms = [
            "court order",
            "legal action",
            "settlement",
            "fraud",
            "evidence",
        ]
        medium_significance_terms = [
            "contract",
            "agreement",
            "payment",
            "debt",
            "business",
        ]

        if any(term in description_lower for term in high_significance_terms):
            self.legal_significance = 0.8
        elif any(term in description_lower for term in medium_significance_terms):
            self.legal_significance = 0.5
        else:
            self.legal_significance = 0.2

        return self.legal_significance

    def evaluate_legitimacy(self) -> float:
        """
        Evaluate the legitimacy of this flow based on context indicators.

        Returns:
            Legitimacy score from 0.0 (illegitimate) to 1.0 (fully legitimate)
        """
        description_lower = self.description.lower()

        illegitimate_indicators = [
            "fraud",
            "embezzlement",
            "theft",
            "unauthorized",
            "illegal",
        ]
        questionable_indicators = ["coercion", "pressure", "forced", "manipulation"]
        legitimate_indicators = [
            "contract",
            "agreement",
            "authorized",
            "legal",
            "proper",
        ]

        if any(indicator in description_lower for indicator in illegitimate_indicators):
            self.flow_legitimacy = 0.1
        elif any(
            indicator in description_lower for indicator in questionable_indicators
        ):
            self.flow_legitimacy = 0.3
        elif any(indicator in description_lower for indicator in legitimate_indicators):
            self.flow_legitimacy = 0.9
        else:
            self.flow_legitimacy = 0.5  # Neutral/unknown

        return self.flow_legitimacy

    def calculate_impact_assessment(self) -> Dict[str, float]:
        """
        Calculate the impact of this flow on different dimensions.

        Returns:
            Dictionary with impact scores on various dimensions
        """
        self.impact_assessment = {
            "financial": 0.0,
            "legal": 0.0,
            "operational": 0.0,
            "reputational": 0.0,
            "strategic": 0.0,
        }

        # Financial impact based on magnitude and type
        if self.flow_type == FlowType.FINANCIAL:
            self.impact_assessment["financial"] = min(
                1.0, self.magnitude / 100000
            )  # Normalize to reasonable scale

        # Legal impact based on legal significance
        self.impact_assessment["legal"] = self.legal_significance

        # Operational impact based on resource category
        if self.resource_category in ["material", "information", "legal_power"]:
            self.impact_assessment["operational"] = 0.6

        # Reputational impact based on legitimacy
        self.impact_assessment["reputational"] = 1.0 - self.flow_legitimacy

        # Strategic impact based on actors and type
        if self.flow_type in [FlowType.INFLUENCE, FlowType.LEVERAGE]:
            self.impact_assessment["strategic"] = 0.7

        return self.impact_assessment


class HyperGNNFramework:
    """
    Main HyperGNN Framework for comprehensive case analysis

    Provides multilayer network modeling with timeline tensor states
    for generalized case solving across any complexity and dimensions.
    """

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.agents: Dict[str, Agent] = {}
        self.events: Dict[str, DiscreteEvent] = {}
        self.flows: Dict[str, SystemFlow] = {}
        self.hypergraph = nx.MultiDiGraph()
        self.timeline_tensors: Dict[datetime, Dict[str, TimelineTensor]] = {}
        self.evidence_repository: Dict[str, Dict[str, Any]] = {}

    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the framework"""
        self.agents[agent.agent_id] = agent
        self.hypergraph.add_node(
            agent.agent_id,
            type="agent",
            agent_type=agent.agent_type.value,
            name=agent.name,
        )

    def add_event(self, event: DiscreteEvent) -> None:
        """Add a discrete event to the framework"""
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

    def add_flow(self, flow: SystemFlow) -> None:
        """Add a system flow to the framework"""
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

    def create_timeline_tensor(
        self,
        timestamp: datetime,
        tensor_type: TensorType,
        data: np.ndarray,
        metadata: Dict[str, Any] = None,
    ) -> TimelineTensor:
        """Create a timeline tensor for a specific timestamp"""
        if metadata is None:
            metadata = {}

        tensor = TimelineTensor(
            timestamp=timestamp,
            tensor_type=tensor_type,
            dimensions=data.shape,
            data=data,
            metadata=metadata,
        )

        if timestamp not in self.timeline_tensors:
            self.timeline_tensors[timestamp] = {}

        self.timeline_tensors[timestamp][tensor_type.value] = tensor
        return tensor

    def analyze_comprehensive_legal_framework(self) -> Dict[str, Any]:
        """
        Analyze the comprehensive legal framework including criminal and commercial aspects.

        Returns:
            Comprehensive legal analysis including roles, relations, events, timelines,
            resource flows, and legal highlights
        """
        analysis = {
            "agent_roles": {},
            "event_analysis": {},
            "resource_flows": {},
            "timeline_analysis": {},
            "legal_highlights": {"criminal": [], "commercial": []},
            "causal_chains": [],
            "risk_assessment": {},
        }

        # Analyze agent roles
        for agent_id, agent in self.agents.items():
            agent_analysis = {
                "criminal_roles": {},
                "commercial_roles": {},
                "behavioral_profile": agent.attributes.get("behavioral_properties", {}),
                "network_position": self._calculate_network_position(agent),
                "influence_score": len(agent.professional_links)
                + len(agent.social_links),
            }

            # Extract role indicators from agent attributes
            legal_role_indicators = agent.attributes.get("legal_role_indicators", {})
            for role, score in legal_role_indicators.items():
                if role.startswith("criminal_"):
                    agent_analysis["criminal_roles"][
                        role.replace("criminal_", "")
                    ] = score
                elif role.startswith("commercial_"):
                    agent_analysis["commercial_roles"][
                        role.replace("commercial_", "")
                    ] = score

            analysis["agent_roles"][agent_id] = agent_analysis

        # Analyze events
        for event_id, event in self.events.items():
            event_significance = event.analyze_legal_significance()
            event_analysis = {
                "criminal_significance": event_significance.get("criminal", 0.0),
                "commercial_significance": event_significance.get("commercial", 0.0),
                "legal_categories": event.legal_categories,
                "timeline_criticality": event.timeline_criticality,
                "causal_predecessors": event.causal_predecessors,
                "causal_successors": event.causal_successors,
                "actors_involved": event.actors,
            }
            analysis["event_analysis"][event_id] = event_analysis

            # Add to legal highlights if significant
            if event_significance.get("criminal", 0.0) > 0.5:
                analysis["legal_highlights"]["criminal"].append(
                    {
                        "event_id": event_id,
                        "description": event.description[:200],
                        "significance": event_significance["criminal"],
                        "timestamp": event.timestamp.isoformat(),
                    }
                )
            if event_significance.get("commercial", 0.0) > 0.5:
                analysis["legal_highlights"]["commercial"].append(
                    {
                        "event_id": event_id,
                        "description": event.description[:200],
                        "significance": event_significance["commercial"],
                        "timestamp": event.timestamp.isoformat(),
                    }
                )

        # Analyze resource flows
        flow_categories = {
            "financial": [],
            "material": [],
            "information": [],
            "legal_power": [],
        }
        for flow_id, flow in self.flows.items():
            category = flow.categorize_flow_type()
            legitimacy = flow.evaluate_legitimacy()
            legal_sig = flow.assess_legal_significance()
            impact = flow.calculate_impact_assessment()

            flow_analysis = {
                "flow_id": flow_id,
                "source": flow.source,
                "target": flow.target,
                "magnitude": flow.magnitude,
                "legitimacy": legitimacy,
                "legal_significance": legal_sig,
                "impact_assessment": impact,
                "timestamp": flow.timestamp.isoformat(),
            }
            flow_categories[category].append(flow_analysis)

        analysis["resource_flows"] = flow_categories

        # Timeline analysis
        analysis["timeline_analysis"] = self._analyze_timeline_patterns()

        # Build causal chains
        analysis["causal_chains"] = self._build_causal_chains()

        # Risk assessment
        analysis["risk_assessment"] = self._assess_legal_risks()

        return analysis

    def _analyze_timeline_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in the timeline of events."""
        if not self.events:
            return {}

        sorted_events = sorted(self.events.values(), key=lambda x: x.timestamp)

        patterns = {
            "total_events": len(sorted_events),
            "timeline_span_days": 0,
            "event_clusters": [],
            "critical_periods": [],
            "escalation_patterns": [],
        }

        if len(sorted_events) >= 2:
            start_date = sorted_events[0].timestamp
            end_date = sorted_events[-1].timestamp
            patterns["timeline_span_days"] = (end_date - start_date).days

            # Identify event clusters (events within 7 days of each other)
            current_cluster = [sorted_events[0]]
            for event in sorted_events[1:]:
                if (event.timestamp - current_cluster[-1].timestamp).days <= 7:
                    current_cluster.append(event)
                else:
                    if len(current_cluster) > 1:
                        patterns["event_clusters"].append(
                            {
                                "start_date": current_cluster[0].timestamp.isoformat(),
                                "end_date": current_cluster[-1].timestamp.isoformat(),
                                "event_count": len(current_cluster),
                                "events": [e.event_id for e in current_cluster],
                            }
                        )
                    current_cluster = [event]

            # Add final cluster if exists
            if len(current_cluster) > 1:
                patterns["event_clusters"].append(
                    {
                        "start_date": current_cluster[0].timestamp.isoformat(),
                        "end_date": current_cluster[-1].timestamp.isoformat(),
                        "event_count": len(current_cluster),
                        "events": [e.event_id for e in current_cluster],
                    }
                )

        return patterns

    def _build_causal_chains(self) -> List[Dict[str, Any]]:
        """Build causal chains from event relationships."""
        causal_chains = []

        # Find events that start causal chains (no predecessors)
        chain_starters = [e for e in self.events.values() if not e.causal_predecessors]

        for starter in chain_starters:
            chain = self._trace_causal_chain(starter, set())
            if len(chain) > 1:  # Only include chains with multiple events
                causal_chains.append(
                    {
                        "chain_id": f"chain_{len(causal_chains)}",
                        "starter_event": starter.event_id,
                        "chain_length": len(chain),
                        "events": [
                            {"event_id": e.event_id, "description": e.description[:100]}
                            for e in chain
                        ],
                        "legal_significance": sum(
                            e.criminal_significance + e.commercial_significance
                            for e in chain
                        )
                        / len(chain),
                    }
                )

        return causal_chains

    def _trace_causal_chain(
        self, event: DiscreteEvent, visited: Set[str]
    ) -> List[DiscreteEvent]:
        """Recursively trace a causal chain from an event."""
        if event.event_id in visited:
            return []

        visited.add(event.event_id)
        chain = [event]

        # Add all successor events
        for successor_id in event.causal_successors:
            if successor_id in self.events:
                successor_chain = self._trace_causal_chain(
                    self.events[successor_id], visited.copy()
                )
                chain.extend(successor_chain)

        return chain

    def _assess_legal_risks(self) -> Dict[str, Any]:
        """Assess legal risks based on the current state of the case."""
        risks = {
            "criminal_risks": [],
            "commercial_risks": [],
            "procedural_risks": [],
            "overall_risk_level": "medium",
        }

        # Assess criminal risks
        high_criminal_events = [
            e for e in self.events.values() if e.criminal_significance > 0.6
        ]
        if high_criminal_events:
            risks["criminal_risks"].append(
                {
                    "risk_type": "serious_criminal_activity",
                    "severity": "high",
                    "indicators": len(high_criminal_events),
                    "description": f"{len(high_criminal_events)} high-significance criminal events identified",
                }
            )

        # Assess commercial risks
        high_commercial_events = [
            e for e in self.events.values() if e.commercial_significance > 0.6
        ]
        if high_commercial_events:
            risks["commercial_risks"].append(
                {
                    "risk_type": "commercial_fraud_indicators",
                    "severity": "medium",
                    "indicators": len(high_commercial_events),
                    "description": f"{len(high_commercial_events)} high-significance commercial events identified",
                }
            )

        # Assess flow legitimacy risks
        illegitimate_flows = [f for f in self.flows.values() if f.flow_legitimacy < 0.4]
        if illegitimate_flows:
            risks["procedural_risks"].append(
                {
                    "risk_type": "questionable_resource_flows",
                    "severity": "medium",
                    "indicators": len(illegitimate_flows),
                    "description": f"{len(illegitimate_flows)} flows with questionable legitimacy",
                }
            )

        # Determine overall risk level
        total_risks = (
            len(risks["criminal_risks"])
            + len(risks["commercial_risks"])
            + len(risks["procedural_risks"])
        )
        if total_risks >= 3:
            risks["overall_risk_level"] = "high"
        elif total_risks >= 1:
            risks["overall_risk_level"] = "medium"
        else:
            risks["overall_risk_level"] = "low"

        return risks

    def analyze_motive_means_opportunity(
        self, agent_id: str, event_id: str
    ) -> Dict[str, str]:
        """
        Analyze motive, means, and opportunity for an agent regarding an event
        Returns professional analysis without subjective assessments
        """
        if agent_id not in self.agents or event_id not in self.events:
            return {"error": "Agent or event not found"}

        agent = self.agents[agent_id]
        event = self.events[event_id]

        analysis = {
            "agent": agent.name,
            "event": event.description,
            "motive_indicators": [],
            "means_available": [],
            "opportunity_factors": [],
            "risk_assessment": "pending_analysis",
        }

        # Enhanced analysis with behavioral properties
        behavioral_props = agent.attributes.get("behavioral_properties", {})

        # Motive analysis based on behavioral properties and strategic goals
        if behavioral_props.get("control_seeking", 0) > 0.7:
            analysis["motive_indicators"].append("High control-seeking behavior")
        if behavioral_props.get("legal_aggression", 0) > 0.7:
            analysis["motive_indicators"].append("High legal aggression tendency")

        strategic_goals = agent.attributes.get("strategic_goals", [])
        for goal in strategic_goals:
            analysis["motive_indicators"].append(f"Strategic goal: {goal}")

        # Means analysis based on network connections and resources
        professional_connections = len(agent.professional_links)
        social_connections = len(agent.social_links)

        if professional_connections > 3:
            analysis["means_available"].append("Extensive professional network")
        if social_connections > 2:
            analysis["means_available"].append("Strong social connections")

        # Opportunity analysis based on event timing and actor involvement
        if agent_id in event.actors:
            analysis["opportunity_factors"].append("Direct involvement in event")

        # Calculate risk assessment
        risk_factors = (
            len(analysis["motive_indicators"])
            + len(analysis["means_available"])
            + len(analysis["opportunity_factors"])
        )
        if risk_factors >= 6:
            analysis["risk_assessment"] = "high_risk"
        elif risk_factors >= 3:
            analysis["risk_assessment"] = "medium_risk"
        else:
            analysis["risk_assessment"] = "low_risk"

        return analysis

    def simulate_agent_behavior(
        self, agent_id: str, time_steps: int = 10
    ) -> Dict[str, Any]:
        """
        Simulate agent behavior over multiple time steps with dynamic interactions
        Enhanced simulation with behavioral patterns and adaptation
        """
        if agent_id not in self.agents:
            return {"error": "Agent not found"}

        agent = self.agents[agent_id]
        simulation_results = {
            "agent_id": agent_id,
            "time_steps": time_steps,
            "behavioral_trajectory": [],
            "interaction_patterns": [],
            "decision_points": [],
            "adaptation_metrics": [],
        }

        # Initialize agent state
        current_state = {
            "influence": 0.5,
            "knowledge": 0.3,
            "resource_access": len(agent.professional_links) * 0.1,
            "stress_level": 0.2,
            "decision_threshold": 0.6,
        }

        for step in range(time_steps):
            timestamp = datetime.now() + timedelta(days=step)

            # Simulate environmental influences
            environmental_factor = np.random.normal(0, 0.1)

            # Update agent state based on network effects
            network_influence = self._calculate_network_influence(agent)

            # Behavioral adaptation
            current_state["influence"] += network_influence * 0.1 + environmental_factor
            current_state["knowledge"] += np.random.normal(
                0.05, 0.02
            )  # Gradual learning
            current_state["stress_level"] += abs(environmental_factor) * 0.5

            # Normalize states
            for key in current_state:
                if key != "decision_threshold":
                    current_state[key] = max(0, min(1, current_state[key]))

            # Record behavioral snapshot
            behavior_snapshot = {
                "timestamp": timestamp.isoformat(),
                "state": current_state.copy(),
                "network_position": self._calculate_network_position(agent),
                "decision_probability": self._calculate_decision_probability(
                    current_state
                ),
            }
            simulation_results["behavioral_trajectory"].append(behavior_snapshot)

            # Simulate interactions with other agents
            if step % 3 == 0:  # Every 3rd step, simulate interactions
                interaction = self._simulate_agent_interaction(
                    agent, current_state, timestamp
                )
                if interaction:
                    simulation_results["interaction_patterns"].append(interaction)

            # Decision point analysis
            if current_state["influence"] > current_state["decision_threshold"]:
                decision = self._simulate_decision_making(
                    agent, current_state, timestamp
                )
                simulation_results["decision_points"].append(decision)
                # Decision impacts reduce immediate influence but may increase knowledge
                current_state["influence"] *= 0.8
                current_state["knowledge"] += 0.1

        # Calculate adaptation metrics
        adaptation_metrics = self._calculate_adaptation_metrics(
            simulation_results["behavioral_trajectory"]
        )
        simulation_results["adaptation_metrics"] = adaptation_metrics

        return simulation_results

    def run_multi_agent_simulation(self, duration_days: int = 30) -> Dict[str, Any]:
        """
        Run comprehensive multi-agent simulation with emergent behaviors
        """
        simulation_start = datetime.now()
        simulation_results = {
            "simulation_id": f"multi_agent_sim_{simulation_start.strftime('%Y%m%d_%H%M%S')}",
            "duration_days": duration_days,
            "agent_simulations": {},
            "emergent_patterns": [],
            "system_dynamics": [],
            "interaction_network_evolution": [],
        }

        # Run individual agent simulations
        for agent_id in self.agents:
            agent_sim = self.simulate_agent_behavior(agent_id, duration_days)
            simulation_results["agent_simulations"][agent_id] = agent_sim

        # Analyze emergent patterns
        emergent_patterns = self._analyze_emergent_patterns(
            simulation_results["agent_simulations"]
        )
        simulation_results["emergent_patterns"] = emergent_patterns

        # Track system-level dynamics
        system_dynamics = self._track_system_dynamics(
            simulation_results["agent_simulations"], duration_days
        )
        simulation_results["system_dynamics"] = system_dynamics

        # Network evolution analysis
        network_evolution = self._analyze_network_evolution(
            simulation_results["agent_simulations"]
        )
        simulation_results["interaction_network_evolution"] = network_evolution

        return simulation_results

    def generate_relationship_matrix(self) -> np.ndarray:
        """Generate relationship matrix for all agents"""
        agent_ids = list(self.agents.keys())
        n_agents = len(agent_ids)

        if n_agents == 0:
            return np.array([])

        matrix = np.zeros((n_agents, n_agents))

        for i, agent1 in enumerate(agent_ids):
            for j, agent2 in enumerate(agent_ids):
                if i != j:
                    # Calculate relationship strength based on connections
                    strength = self._calculate_relationship_strength(agent1, agent2)
                    matrix[i, j] = strength

        return matrix

    def _calculate_relationship_strength(self, agent1_id: str, agent2_id: str) -> float:
        """Calculate relationship strength between two agents"""
        agent1 = self.agents[agent1_id]

        strength = 0.0

        # Professional link connections
        if agent2_id in agent1.professional_links:
            strength += 0.7

        # Social link connections
        if agent2_id in agent1.social_links:
            strength += 0.3

        # Shared events
        shared_events = 0
        for event in self.events.values():
            if agent1_id in event.actors and agent2_id in event.actors:
                shared_events += 1

        strength += min(shared_events * 0.1, 0.5)

        return min(strength, 1.0)

    def track_deception_patterns(self) -> List[Dict[str, Any]]:
        """
        Identify potential deception patterns based on communication flows
        and knowledge discrepancies. Returns objective analysis.
        """
        patterns = []

        for agent_id, agent in self.agents.items():
            # Analyze knowledge tensor consistency over time
            knowledge_timeline = sorted(agent.knowledge_tensors.items())

            for i in range(len(knowledge_timeline) - 1):
                curr_time, curr_tensor = knowledge_timeline[i]
                next_time, next_tensor = knowledge_timeline[i + 1]

                # Look for sudden knowledge changes without evidence
                if self._detect_knowledge_anomaly(curr_tensor, next_tensor):
                    patterns.append(
                        {
                            "agent": agent.name,
                            "timeframe": f"{curr_time} to {next_time}",
                            "pattern_type": "knowledge_inconsistency",
                            "description": "Knowledge state change without supporting evidence",
                            "confidence": 0.7,
                        }
                    )

        return patterns

    def _detect_knowledge_anomaly(
        self, tensor1: TimelineTensor, tensor2: TimelineTensor
    ) -> bool:
        """Detect anomalies in knowledge tensor transitions"""
        if tensor1.data.shape != tensor2.data.shape:
            return True

        # Calculate change magnitude
        change = np.linalg.norm(tensor2.data - tensor1.data)

        # Threshold for significant change
        return change > 0.5

    def export_professional_report(self) -> Dict[str, Any]:
        """
        Export comprehensive professional analysis report
        Focus on facts, evidence, and logical relationships
        """
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
            "network_metrics": {
                "nodes": self.hypergraph.number_of_nodes(),
                "edges": self.hypergraph.number_of_edges(),
                "density": (
                    nx.density(self.hypergraph)
                    if self.hypergraph.number_of_nodes() > 1
                    else 0
                ),
            },
            "deception_patterns": self.track_deception_patterns(),
            "relationship_analysis": self._generate_relationship_analysis(),
        }

    def _generate_relationship_analysis(self) -> Dict[str, Any]:
        """Generate professional relationship analysis"""
        matrix = self.generate_relationship_matrix()

        if matrix.size == 0:
            return {"status": "insufficient_data"}

        return {
            "strongest_connections": self._identify_strong_connections(matrix),
            "isolated_agents": self._identify_isolated_agents(matrix),
            "network_centrality": self._calculate_centrality_measures(),
        }

    def _identify_strong_connections(self, matrix: np.ndarray) -> List[Dict[str, Any]]:
        """Identify strongest agent connections"""
        agent_ids = list(self.agents.keys())
        connections = []

        for i in range(len(agent_ids)):
            for j in range(i + 1, len(agent_ids)):
                strength = (matrix[i, j] + matrix[j, i]) / 2
                if strength > 0.5:
                    connections.append(
                        {
                            "agent1": self.agents[agent_ids[i]].name,
                            "agent2": self.agents[agent_ids[j]].name,
                            "strength": strength,
                            "connection_type": (
                                "professional" if strength > 0.7 else "social"
                            ),
                        }
                    )

        return sorted(connections, key=lambda x: x["strength"], reverse=True)

    def _identify_isolated_agents(self, matrix: np.ndarray) -> List[str]:
        """Identify agents with minimal connections"""
        agent_ids = list(self.agents.keys())
        isolated = []

        for i, agent_id in enumerate(agent_ids):
            total_connections = np.sum(matrix[i, :]) + np.sum(matrix[:, i])
            if total_connections < 0.1:
                isolated.append(self.agents[agent_id].name)

        return isolated

    def _calculate_centrality_measures(self) -> Dict[str, Dict[str, float]]:
        """Calculate network centrality measures"""
        if self.hypergraph.number_of_nodes() < 2:
            return {}

        try:
            centrality = {
                "degree": nx.degree_centrality(self.hypergraph),
                "betweenness": nx.betweenness_centrality(self.hypergraph),
                "closeness": nx.closeness_centrality(self.hypergraph),
            }

            # Convert to agent names
            result = {}
            for measure, values in centrality.items():
                result[measure] = {
                    self.agents.get(node_id, {"name": node_id}).get(
                        "name", node_id
                    ): score
                    for node_id, score in values.items()
                    if node_id in self.agents
                }

            return result
        except:
            return {"error": "centrality_calculation_failed"}

    def _calculate_network_influence(self, agent: Agent) -> float:
        """Calculate network influence for an agent"""
        professional_influence = len(agent.professional_links) * 0.3
        social_influence = len(agent.social_links) * 0.1
        return min(1.0, professional_influence + social_influence)

    def _calculate_network_position(self, agent: Agent) -> Dict[str, float]:
        """Calculate agent's position in the network"""
        return {
            "centrality": self._calculate_network_influence(agent),
            "connectivity": (len(agent.professional_links) + len(agent.social_links))
            / max(1, len(self.agents) - 1),
            "influence_potential": min(1.0, len(agent.professional_links) * 0.4),
        }

    def _calculate_decision_probability(self, state: Dict[str, float]) -> float:
        """Calculate probability of agent making a decision"""
        influence_factor = state["influence"] * 0.4
        knowledge_factor = state["knowledge"] * 0.3
        stress_factor = (1 - state["stress_level"]) * 0.3
        return min(1.0, influence_factor + knowledge_factor + stress_factor)

    def _simulate_agent_interaction(
        self, agent: Agent, state: Dict[str, float], timestamp: datetime
    ) -> Optional[Dict[str, Any]]:
        """Simulate interaction between agents"""
        # Select a random connected agent
        all_connections = list(agent.professional_links.union(agent.social_links))
        if not all_connections:
            return None

        target_agent_id = np.random.choice(all_connections) if all_connections else None
        if not target_agent_id or target_agent_id not in self.agents:
            return None

        interaction_strength = np.random.uniform(0.1, state["influence"])
        interaction_type = (
            "professional" if target_agent_id in agent.professional_links else "social"
        )

        return {
            "timestamp": timestamp.isoformat(),
            "initiator": agent.agent_id,
            "target": target_agent_id,
            "interaction_type": interaction_type,
            "strength": interaction_strength,
            "outcome": (
                "information_exchange"
                if interaction_strength > 0.5
                else "social_contact"
            ),
        }

    def _simulate_decision_making(
        self, agent: Agent, state: Dict[str, float], timestamp: datetime
    ) -> Dict[str, Any]:
        """Simulate agent decision-making process"""
        decision_factors = {
            "influence_level": state["influence"],
            "knowledge_confidence": state["knowledge"],
            "network_support": self._calculate_network_influence(agent),
            "environmental_pressure": state["stress_level"],
        }

        decision_weight = sum(decision_factors.values()) / len(decision_factors)
        decision_type = "major" if decision_weight > 0.7 else "minor"

        return {
            "timestamp": timestamp.isoformat(),
            "agent": agent.agent_id,
            "decision_type": decision_type,
            "decision_weight": decision_weight,
            "factors": decision_factors,
            "confidence": min(1.0, decision_weight * 1.2),
        }

    def _calculate_adaptation_metrics(
        self, trajectory: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate adaptation metrics from behavioral trajectory"""
        if len(trajectory) < 2:
            return {"adaptation_rate": 0.0, "stability": 1.0, "learning_rate": 0.0}

        # Calculate changes in key metrics
        influence_changes = []
        knowledge_changes = []

        for i in range(1, len(trajectory)):
            prev_state = trajectory[i - 1]["state"]
            curr_state = trajectory[i]["state"]

            influence_changes.append(
                abs(curr_state["influence"] - prev_state["influence"])
            )
            knowledge_changes.append(curr_state["knowledge"] - prev_state["knowledge"])

        adaptation_rate = np.mean(influence_changes) if influence_changes else 0.0
        learning_rate = (
            np.mean([k for k in knowledge_changes if k > 0])
            if knowledge_changes
            else 0.0
        )
        stability = 1.0 - np.std(influence_changes) if influence_changes else 1.0

        return {
            "adaptation_rate": adaptation_rate,
            "stability": max(0.0, stability),
            "learning_rate": learning_rate,
            "volatility": np.std(influence_changes) if influence_changes else 0.0,
        }

    def _analyze_emergent_patterns(
        self, agent_simulations: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze emergent patterns across all agents"""
        patterns = []

        # Analyze synchronization patterns
        decision_times = {}
        for agent_id, sim_data in agent_simulations.items():
            decision_times[agent_id] = [
                dp["timestamp"] for dp in sim_data.get("decision_points", [])
            ]

        # Find synchronized decision-making
        for agent1, times1 in decision_times.items():
            for agent2, times2 in decision_times.items():
                if agent1 >= agent2:  # Avoid duplicates
                    continue

                # Check for temporal proximity in decisions
                synchronized_count = 0
                for t1 in times1:
                    for t2 in times2:
                        time_diff = abs(
                            (
                                datetime.fromisoformat(t1) - datetime.fromisoformat(t2)
                            ).total_seconds()
                        )
                        if time_diff < 86400:  # Within 1 day
                            synchronized_count += 1

                if synchronized_count > 0:
                    patterns.append(
                        {
                            "pattern_type": "synchronized_decision_making",
                            "agents": [agent1, agent2],
                            "synchronization_count": synchronized_count,
                            "confidence": min(1.0, synchronized_count * 0.3),
                        }
                    )

        return patterns

    def _track_system_dynamics(
        self, agent_simulations: Dict[str, Dict[str, Any]], duration_days: int
    ) -> List[Dict[str, Any]]:
        """Track system-level dynamics over time"""
        system_states = []

        for day in range(duration_days):
            day_timestamp = datetime.now() + timedelta(days=day)

            # Aggregate system state for this day
            total_influence = 0
            total_knowledge = 0
            total_stress = 0
            agent_count = 0

            for agent_id, sim_data in agent_simulations.items():
                trajectory = sim_data.get("behavioral_trajectory", [])
                if day < len(trajectory):
                    state = trajectory[day]["state"]
                    total_influence += state["influence"]
                    total_knowledge += state["knowledge"]
                    total_stress += state["stress_level"]
                    agent_count += 1

            if agent_count > 0:
                system_state = {
                    "timestamp": day_timestamp.isoformat(),
                    "day": day,
                    "average_influence": total_influence / agent_count,
                    "average_knowledge": total_knowledge / agent_count,
                    "average_stress": total_stress / agent_count,
                    "system_stability": 1.0 - (total_stress / agent_count),
                    "collective_capacity": (total_influence + total_knowledge)
                    / (2 * agent_count),
                }
                system_states.append(system_state)

        return system_states

    def _analyze_network_evolution(
        self, agent_simulations: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyze how the interaction network evolves over time"""
        network_snapshots = []

        # Extract interaction patterns over time
        all_interactions = []
        for agent_id, sim_data in agent_simulations.items():
            interactions = sim_data.get("interaction_patterns", [])
            for interaction in interactions:
                interaction["source_agent"] = agent_id
                all_interactions.append(interaction)

        # Sort by timestamp
        all_interactions.sort(key=lambda x: x["timestamp"])

        # Group by time periods (e.g., weekly)
        current_week = 0
        current_interactions = []

        for interaction in all_interactions:
            interaction_time = datetime.fromisoformat(interaction["timestamp"])
            week = interaction_time.day // 7

            if week != current_week:
                if current_interactions:
                    network_snapshot = self._create_network_snapshot(
                        current_interactions, current_week
                    )
                    network_snapshots.append(network_snapshot)
                current_week = week
                current_interactions = []

            current_interactions.append(interaction)

        # Add final week
        if current_interactions:
            network_snapshot = self._create_network_snapshot(
                current_interactions, current_week
            )
            network_snapshots.append(network_snapshot)

        return network_snapshots

    def _create_network_snapshot(
        self, interactions: List[Dict[str, Any]], week: int
    ) -> Dict[str, Any]:
        """Create a network snapshot for a given time period"""
        # Count interaction frequencies
        interaction_counts = {}
        total_interactions = len(interactions)

        for interaction in interactions:
            source = interaction["source_agent"]
            target = interaction["target"]
            pair = tuple(sorted([source, target]))

            if pair not in interaction_counts:
                interaction_counts[pair] = 0
            interaction_counts[pair] += 1

        # Calculate network metrics
        unique_agents = set()
        for interaction in interactions:
            unique_agents.add(interaction["source_agent"])
            unique_agents.add(interaction["target"])

        network_density = len(interaction_counts) / max(
            1, len(unique_agents) * (len(unique_agents) - 1) / 2
        )

        return {
            "week": week,
            "total_interactions": total_interactions,
            "unique_agents": len(unique_agents),
            "interaction_pairs": len(interaction_counts),
            "network_density": network_density,
            "most_active_pairs": sorted(
                interaction_counts.items(), key=lambda x: x[1], reverse=True
            )[:3],
        }


def create_sample_framework() -> HyperGNNFramework:
    """Create a sample framework for testing and demonstration"""
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
    framework = create_sample_framework()
    report = framework.export_professional_report()
    print(json.dumps(report, indent=2, default=str))
