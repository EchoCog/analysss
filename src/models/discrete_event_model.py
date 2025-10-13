#!/usr/bin/env python3
"""
Discrete Event-Driven Model and Knowledge Tensor Generator
========================================================

This module generates discrete event-driven models and knowledge tensors
from timeline data, integrating with agent-based model data and evidence tracking.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import networkx as nx
import numpy as np

from case_data_loader import InformationStatus
from frameworks.hypergnn_core import HyperGNNFramework
from src.models.hypergnn_framework_improved import (
    AnalysisConfiguration,
    AnalysisScope,
    ComplexityLevel,
)

# Import existing components
from src.simulations.enhanced_timeline_processor import (
    EnhancedTimelineProcessor,
    TimelineEntry,
    TimelineEntryType,
    VerificationLevel,
)


class EventState(Enum):
    """States for discrete events"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TensorDimension(Enum):
    """Dimensions for knowledge tensors"""

    TIME = "time"
    AGENT = "agent"
    ACTION = "action"
    EVIDENCE = "evidence"
    IMPACT = "impact"
    RELATION = "relation"


@dataclass
class DiscreteEvent:
    """Discrete event representation"""

    event_id: str
    timestamp: datetime
    event_type: TimelineEntryType
    state: EventState
    actors: List[str]
    preconditions: List[str] = field(default_factory=list)
    postconditions: List[str] = field(default_factory=list)
    evidence_required: List[str] = field(default_factory=list)
    evidence_submitted: List[str] = field(default_factory=list)
    impact_vector: np.ndarray = field(default_factory=lambda: np.zeros(5))
    knowledge_tensor: Optional[np.ndarray] = None


@dataclass
class KnowledgeTensor:
    """Multi-dimensional knowledge tensor"""

    tensor_id: str
    dimensions: Dict[TensorDimension, int]
    data: np.ndarray
    feature_names: Dict[TensorDimension, List[str]]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class EvidenceRequirement:
    """Evidence requirement specification"""

    event_id: str
    evidence_type: str
    description: str
    status: str  # required, submitted, verified, missing
    priority: str  # critical, high, medium, low
    legal_reference: Optional[str] = None
    deadline: Optional[datetime] = None


class DiscreteEventModel:
    """Discrete event-driven model generator with knowledge tensors"""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.events: Dict[str, DiscreteEvent] = {}
        self.event_graph = nx.DiGraph()
        self.knowledge_tensors: Dict[str, KnowledgeTensor] = {}
        self.evidence_requirements: Dict[str, List[EvidenceRequirement]] = {}
        self.agent_states: Dict[str, Dict[str, Any]] = {}

        # Initialize feature dimensions
        self.dimensions = {
            TensorDimension.TIME: 100,  # Time steps
            TensorDimension.AGENT: 20,  # Max agents
            TensorDimension.ACTION: 50,  # Action types
            TensorDimension.EVIDENCE: 30,  # Evidence types
            TensorDimension.IMPACT: 5,  # Impact dimensions
            TensorDimension.RELATION: 10,  # Relation types
        }

        # Feature mappings
        self.feature_maps = {
            TensorDimension.AGENT: {},
            TensorDimension.ACTION: {},
            TensorDimension.EVIDENCE: {},
            TensorDimension.RELATION: {},
        }

    def process_timeline(
        self, timeline_entries: Dict[str, TimelineEntry]
    ) -> Dict[str, Any]:
        """Process timeline entries into discrete events"""
        print("=== DISCRETE EVENT MODEL GENERATION ===")

        # Sort entries by date
        sorted_entries = sorted(timeline_entries.values(), key=lambda x: x.date)

        # Generate discrete events
        for entry in sorted_entries:
            event = self._create_discrete_event(entry)
            self.events[event.event_id] = event

            # Add to event graph
            self._add_to_event_graph(event, sorted_entries)

            # Generate evidence requirements
            self._generate_evidence_requirements(event, entry)

        # Generate knowledge tensors
        self._generate_knowledge_tensors()

        # Integrate with agent-based model
        self._integrate_agent_model()

        return {
            "total_events": len(self.events),
            "event_states": self._count_event_states(),
            "knowledge_tensors": len(self.knowledge_tensors),
            "evidence_requirements": sum(
                len(reqs) for reqs in self.evidence_requirements.values()
            ),
        }

    def _create_discrete_event(self, timeline_entry: TimelineEntry) -> DiscreteEvent:
        """Create discrete event from timeline entry"""
        # Map actors
        actors = timeline_entry.participants

        # Determine event state based on date
        if timeline_entry.date > datetime.now():
            state = EventState.PENDING
        elif timeline_entry.information_status == InformationStatus.SAVED:
            state = EventState.COMPLETED
        else:
            state = EventState.IN_PROGRESS

        # Calculate impact vector
        impact_vector = self._calculate_impact_vector(timeline_entry)

        # Map evidence
        evidence_submitted = timeline_entry.evidence_references
        evidence_required = self._determine_required_evidence(timeline_entry)

        # Create event
        event = DiscreteEvent(
            event_id=timeline_entry.entry_id,
            timestamp=timeline_entry.date,
            event_type=timeline_entry.entry_type,
            state=state,
            actors=actors,
            evidence_required=evidence_required,
            evidence_submitted=evidence_submitted,
            impact_vector=impact_vector,
        )

        # Set pre and post conditions
        event.preconditions = self._extract_preconditions(timeline_entry)
        event.postconditions = self._extract_postconditions(timeline_entry)

        return event

    def _calculate_impact_vector(self, entry: TimelineEntry) -> np.ndarray:
        """Calculate 5-dimensional impact vector"""
        impact = np.zeros(5)

        # Dimension 0: Legal impact
        if "murder" in entry.tags or "homicide" in entry.tags:
            impact[0] = 1.0
        elif "court" in entry.tags or "legal" in entry.tags:
            impact[0] = 0.8
        elif "crime" in entry.tags:
            impact[0] = 0.6

        # Dimension 1: Financial impact
        if entry.entry_type == TimelineEntryType.FINANCIAL_TRANSACTION:
            impact[1] = 0.9
        elif "theft" in entry.tags or "fraud" in entry.tags:
            impact[1] = 0.8

        # Dimension 2: Social impact (number of participants)
        impact[2] = min(1.0, len(entry.participants) / 5.0)

        # Dimension 3: Evidence strength
        impact[3] = entry.source_reliability

        # Dimension 4: Temporal criticality
        if entry.impact_assessment.startswith("CRITICAL"):
            impact[4] = 1.0
        elif entry.impact_assessment.startswith("HIGH"):
            impact[4] = 0.7
        elif entry.impact_assessment.startswith("MODERATE"):
            impact[4] = 0.4
        else:
            impact[4] = 0.2

        return impact

    def _determine_required_evidence(self, entry: TimelineEntry) -> List[str]:
        """Determine required evidence based on event type and legal significance"""
        required = []

        # Criminal events
        if entry.entry_type == TimelineEntryType.CRIMINAL_EVENT:
            required.extend(
                [
                    "police_report",
                    "witness_statements",
                    "forensic_evidence",
                    "scene_documentation",
                ]
            )

        # Legal actions
        elif entry.entry_type == TimelineEntryType.LEGAL_ACTION:
            required.extend(
                ["court_filing", "legal_representation", "supporting_affidavits"]
            )

        # Financial transactions
        elif entry.entry_type == TimelineEntryType.FINANCIAL_TRANSACTION:
            required.extend(
                ["transaction_records", "bank_statements", "authorization_documents"]
            )

        # Communications
        elif entry.entry_type == TimelineEntryType.COMMUNICATION:
            required.extend(["communication_logs", "metadata_records"])

        # Evidence discovery
        elif entry.entry_type == TimelineEntryType.EVIDENCE_DISCOVERY:
            required.extend(
                ["chain_of_custody", "discovery_documentation", "verification_records"]
            )

        return required

    def _extract_preconditions(self, entry: TimelineEntry) -> List[str]:
        """Extract preconditions from timeline entry"""
        preconditions = []

        # Murder events require victim to be alive
        if "murder" in entry.tags:
            preconditions.append("victim_alive")

        # Court orders require standing
        if "court_order" in entry.tags:
            preconditions.append("legal_standing")
            preconditions.append("court_jurisdiction")

        # Email hijacking requires access
        if "email_hijacking" in entry.tags:
            preconditions.append("system_access")
            preconditions.append("credential_knowledge")

        return preconditions

    def _extract_postconditions(self, entry: TimelineEntry) -> List[str]:
        """Extract postconditions from timeline entry"""
        postconditions = []

        # Murder changes victim state
        if "murder" in entry.tags:
            postconditions.append("victim_deceased")
            postconditions.append("investigation_triggered")

        # Court orders create legal obligations
        if "court_order" in entry.tags:
            postconditions.append("legal_obligation_created")
            postconditions.append("compliance_required")

        # Email hijacking changes control
        if "email_hijacking" in entry.tags:
            postconditions.append("unauthorized_access_gained")
            postconditions.append("information_interception_enabled")

        return postconditions

    def _add_to_event_graph(
        self, event: DiscreteEvent, all_entries: List[TimelineEntry]
    ):
        """Add event to causal graph"""
        self.event_graph.add_node(
            event.event_id, event=event, timestamp=event.timestamp, actors=event.actors
        )

        # Find dependencies based on preconditions
        for other_event_id, other_event in self.events.items():
            if other_event_id == event.event_id:
                continue

            # Check if other event satisfies preconditions
            for precond in event.preconditions:
                if precond in other_event.postconditions:
                    self.event_graph.add_edge(
                        other_event_id,
                        event.event_id,
                        relation="enables",
                        condition=precond,
                    )

            # Check temporal dependencies
            if other_event.timestamp < event.timestamp:
                time_diff = (event.timestamp - other_event.timestamp).days
                if time_diff < 30:  # Within 30 days
                    # Check if same actors involved
                    common_actors = set(event.actors) & set(other_event.actors)
                    if common_actors:
                        self.event_graph.add_edge(
                            other_event_id,
                            event.event_id,
                            relation="temporal_proximity",
                            actors=list(common_actors),
                            days_apart=time_diff,
                        )

    def _generate_evidence_requirements(
        self, event: DiscreteEvent, entry: TimelineEntry
    ):
        """Generate detailed evidence requirements for event"""
        requirements = []

        # Map general requirements to specific ones
        for req_type in event.evidence_required:
            if req_type == "police_report":
                requirements.append(
                    EvidenceRequirement(
                        event_id=event.event_id,
                        evidence_type="police_report",
                        description=f"Official police report for {entry.title}",
                        status=(
                            "required"
                            if req_type not in event.evidence_submitted
                            else "submitted"
                        ),
                        priority="critical" if "murder" in entry.tags else "high",
                        legal_reference="Criminal Procedure Act 51 of 1977, Section 3",
                    )
                )

            elif req_type == "court_filing":
                requirements.append(
                    EvidenceRequirement(
                        event_id=event.event_id,
                        evidence_type="court_filing",
                        description=f"Court filing documents for {entry.title}",
                        status=(
                            "submitted"
                            if "Court_Order" in event.evidence_submitted
                            else "required"
                        ),
                        priority="critical",
                        legal_reference="Rules of Court",
                        deadline=entry.date + timedelta(days=10),
                    )
                )

            elif req_type == "witness_statements":
                requirements.append(
                    EvidenceRequirement(
                        event_id=event.event_id,
                        evidence_type="witness_statements",
                        description=f"Witness statements regarding {entry.title}",
                        status="required",
                        priority="high",
                        legal_reference="Criminal Procedure Act, Section 212",
                    )
                )

            elif req_type == "transaction_records":
                requirements.append(
                    EvidenceRequirement(
                        event_id=event.event_id,
                        evidence_type="transaction_records",
                        description=f"Financial transaction records for {entry.title}",
                        status="required",
                        priority=(
                            "high"
                            if entry.entry_type
                            == TimelineEntryType.FINANCIAL_TRANSACTION
                            else "medium"
                        ),
                    )
                )

        # Check verification level for additional requirements
        if entry.verification_level == VerificationLevel.ALLEGED:
            requirements.append(
                EvidenceRequirement(
                    event_id=event.event_id,
                    evidence_type="corroboration",
                    description="Independent corroboration required for alleged event",
                    status="required",
                    priority="high",
                )
            )

        self.evidence_requirements[event.event_id] = requirements

    def _generate_knowledge_tensors(self):
        """Generate multi-dimensional knowledge tensors from events"""
        print("\n=== GENERATING KNOWLEDGE TENSORS ===")

        # Initialize tensors
        event_agent_tensor = np.zeros(
            (
                len(self.events),
                self.dimensions[TensorDimension.AGENT],
                self.dimensions[TensorDimension.ACTION],
            )
        )

        evidence_tensor = np.zeros(
            (
                len(self.events),
                self.dimensions[TensorDimension.EVIDENCE],
                self.dimensions[TensorDimension.IMPACT],
            )
        )

        temporal_relation_tensor = np.zeros(
            (
                len(self.events),
                len(self.events),
                self.dimensions[TensorDimension.RELATION],
            )
        )

        # Map features
        self._build_feature_maps()

        # Fill tensors
        event_list = list(self.events.values())
        for i, event in enumerate(event_list):
            # Event-Agent-Action tensor
            for actor in event.actors:
                if actor in self.feature_maps[TensorDimension.AGENT]:
                    agent_idx = self.feature_maps[TensorDimension.AGENT][actor]
                    action_idx = self._get_action_index(event.event_type)
                    event_agent_tensor[i, agent_idx, action_idx] = 1.0

            # Evidence-Impact tensor
            for j, evidence in enumerate(
                event.evidence_submitted[: self.dimensions[TensorDimension.EVIDENCE]]
            ):
                evidence_tensor[i, j, :] = event.impact_vector

            # Temporal relation tensor
            for j, other_event in enumerate(event_list):
                if i != j:
                    relation_strength = self._calculate_relation_strength(
                        event, other_event
                    )
                    temporal_relation_tensor[i, j, :] = relation_strength

            # Store individual event tensor
            event.knowledge_tensor = self._create_event_tensor(event, i)

        # Store tensors
        self.knowledge_tensors["event_agent_action"] = KnowledgeTensor(
            tensor_id="event_agent_action",
            dimensions={
                TensorDimension.TIME: len(self.events),
                TensorDimension.AGENT: self.dimensions[TensorDimension.AGENT],
                TensorDimension.ACTION: self.dimensions[TensorDimension.ACTION],
            },
            data=event_agent_tensor,
            feature_names={
                TensorDimension.AGENT: list(
                    self.feature_maps[TensorDimension.AGENT].keys()
                ),
                TensorDimension.ACTION: list(
                    self.feature_maps[TensorDimension.ACTION].keys()
                ),
            },
        )

        self.knowledge_tensors["evidence_impact"] = KnowledgeTensor(
            tensor_id="evidence_impact",
            dimensions={
                TensorDimension.TIME: len(self.events),
                TensorDimension.EVIDENCE: self.dimensions[TensorDimension.EVIDENCE],
                TensorDimension.IMPACT: self.dimensions[TensorDimension.IMPACT],
            },
            data=evidence_tensor,
            feature_names={
                TensorDimension.EVIDENCE: list(
                    self.feature_maps[TensorDimension.EVIDENCE].keys()
                ),
                TensorDimension.IMPACT: [
                    "legal",
                    "financial",
                    "social",
                    "evidence_strength",
                    "criticality",
                ],
            },
        )

        self.knowledge_tensors["temporal_relations"] = KnowledgeTensor(
            tensor_id="temporal_relations",
            dimensions={
                TensorDimension.TIME: len(self.events),
                TensorDimension.TIME: len(self.events),
                TensorDimension.RELATION: self.dimensions[TensorDimension.RELATION],
            },
            data=temporal_relation_tensor,
            feature_names={
                TensorDimension.RELATION: [
                    "enables",
                    "blocks",
                    "temporal_proximity",
                    "same_actors",
                    "evidence_link",
                    "causal",
                ]
            },
        )

        print(f"✅ Generated {len(self.knowledge_tensors)} knowledge tensors")

    def _build_feature_maps(self):
        """Build feature mappings for tensor dimensions"""
        # Agent mapping
        all_agents = set()
        for event in self.events.values():
            all_agents.update(event.actors)

        for i, agent in enumerate(
            sorted(all_agents)[: self.dimensions[TensorDimension.AGENT]]
        ):
            self.feature_maps[TensorDimension.AGENT][agent] = i

        # Action mapping (event types)
        action_types = set(event.event_type.value for event in self.events.values())
        for i, action in enumerate(sorted(action_types)):
            self.feature_maps[TensorDimension.ACTION][action] = i

        # Evidence mapping
        all_evidence = set()
        for event in self.events.values():
            all_evidence.update(event.evidence_submitted)
            all_evidence.update(event.evidence_required)

        for i, evidence in enumerate(
            sorted(all_evidence)[: self.dimensions[TensorDimension.EVIDENCE]]
        ):
            self.feature_maps[TensorDimension.EVIDENCE][evidence] = i

    def _get_action_index(self, event_type: TimelineEntryType) -> int:
        """Get action index for event type"""
        action_name = event_type.value
        return self.feature_maps[TensorDimension.ACTION].get(action_name, 0)

    def _calculate_relation_strength(
        self, event1: DiscreteEvent, event2: DiscreteEvent
    ) -> np.ndarray:
        """Calculate relation strength vector between events"""
        relation_vector = np.zeros(self.dimensions[TensorDimension.RELATION])

        # Check different relation types
        # 0: enables
        if any(pc in event1.postconditions for pc in event2.preconditions):
            relation_vector[0] = 1.0

        # 1: blocks
        if any(pc in event1.postconditions for pc in event2.preconditions):
            relation_vector[1] = 0.0  # Placeholder

        # 2: temporal proximity
        time_diff = abs((event1.timestamp - event2.timestamp).days)
        if time_diff < 30:
            relation_vector[2] = 1.0 - (time_diff / 30.0)

        # 3: same actors
        common_actors = set(event1.actors) & set(event2.actors)
        if common_actors:
            relation_vector[3] = len(common_actors) / max(
                len(event1.actors), len(event2.actors)
            )

        # 4: evidence link
        common_evidence = set(event1.evidence_submitted) & set(
            event2.evidence_submitted
        )
        if common_evidence:
            relation_vector[4] = len(common_evidence) / max(
                len(event1.evidence_submitted), len(event2.evidence_submitted)
            )

        # 5: causal (from graph)
        if self.event_graph.has_edge(event1.event_id, event2.event_id):
            relation_vector[5] = 1.0

        return relation_vector

    def _create_event_tensor(self, event: DiscreteEvent, event_idx: int) -> np.ndarray:
        """Create individual event knowledge tensor"""
        # 4D tensor: actors x actions x evidence x impact
        tensor_shape = (
            len(event.actors),
            1,  # Single action per event
            len(event.evidence_submitted) + len(event.evidence_required),
            5,  # Impact dimensions
        )

        event_tensor = np.zeros(tensor_shape)

        # Fill tensor
        for i, actor in enumerate(event.actors):
            # Action dimension (single action)
            event_tensor[i, 0, :, :] = np.outer(
                np.ones(tensor_shape[2]), event.impact_vector
            )

        return event_tensor

    def _integrate_agent_model(self):
        """Integrate discrete events with agent-based model"""
        print("\n=== INTEGRATING WITH AGENT-BASED MODEL ===")

        # Initialize agent states
        all_agents = set()
        for event in self.events.values():
            all_agents.update(event.actors)

        for agent in all_agents:
            self.agent_states[agent] = {
                "events_participated": [],
                "roles": set(),
                "evidence_submitted": set(),
                "evidence_required": set(),
                "impact_score": np.zeros(5),
                "state_transitions": [],
            }

        # Process events chronologically
        sorted_events = sorted(self.events.values(), key=lambda x: x.timestamp)

        for event in sorted_events:
            # Update agent states
            for actor in event.actors:
                agent_state = self.agent_states[actor]

                # Record participation
                agent_state["events_participated"].append(event.event_id)

                # Update roles based on event type and tags
                if event.event_type == TimelineEntryType.CRIMINAL_EVENT:
                    if "victim" in actor.lower():
                        agent_state["roles"].add("victim")
                    elif "perpetrator" in actor.lower() or "suspect" in actor.lower():
                        agent_state["roles"].add("perpetrator")

                # Track evidence
                agent_state["evidence_submitted"].update(event.evidence_submitted)
                agent_state["evidence_required"].update(event.evidence_required)

                # Accumulate impact
                agent_state["impact_score"] += event.impact_vector

                # Record state transitions
                if event.postconditions:
                    agent_state["state_transitions"].append(
                        {
                            "event_id": event.event_id,
                            "timestamp": event.timestamp,
                            "postconditions": event.postconditions,
                        }
                    )

        print(f"✅ Integrated {len(self.agent_states)} agents with event model")

    def integrate_case_entities(self, entities: Dict[str, Any]) -> None:
        """
        Integrate CaseEntity objects with agent models into the discrete event model.

        This method allows CaseEntity objects with initialized agent models to be used
        in the discrete event model, enabling agent-based decision making and behavioral
        modeling within the event processing framework.

        Args:
            entities: Dictionary mapping entity_id to CaseEntity objects with agent models
        """
        print("\n=== INTEGRATING CASE ENTITIES WITH AGENT MODELS ===")

        integrated_count = 0
        for entity_id, entity in entities.items():
            # Check if entity has agent model initialized
            if (
                hasattr(entity, "behavioral_properties")
                and entity.behavioral_properties
            ):
                # Update or create agent state with behavioral properties
                if entity_id not in self.agent_states:
                    self.agent_states[entity_id] = {
                        "events_participated": [],
                        "roles": (
                            set(entity.roles) if hasattr(entity, "roles") else set()
                        ),
                        "evidence_submitted": set(),
                        "evidence_required": set(),
                        "impact_score": np.zeros(5),
                        "state_transitions": [],
                    }

                # Add agent model specific data
                self.agent_states[entity_id][
                    "behavioral_properties"
                ] = entity.behavioral_properties
                self.agent_states[entity_id][
                    "behavioral_rules"
                ] = entity.behavioral_rules
                self.agent_states[entity_id]["strategic_goals"] = entity.strategic_goals
                self.agent_states[entity_id]["entity_name"] = entity.name

                integrated_count += 1

        print(
            f"✅ Integrated {integrated_count} CaseEntity agents with behavioral models"
        )

    def simulate_agent_decisions(
        self, event_id: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate agent decisions for a specific event using their behavioral models.

        Args:
            event_id: The event ID to simulate decisions for
            context: Context information for decision making

        Returns:
            Dictionary mapping entity_id to their decision for this event
        """
        if event_id not in self.events:
            return {}

        event = self.events[event_id]
        decisions = {}

        for actor in event.actors:
            if actor in self.agent_states:
                agent_state = self.agent_states[actor]

                # Check if agent has behavioral model
                if "behavioral_properties" in agent_state:
                    # Simulate decision based on behavioral properties
                    decision = {
                        "actor": actor,
                        "event_id": event_id,
                        "decision": None,
                        "reasoning": [],
                    }

                    # Check behavioral rules
                    if "behavioral_rules" in agent_state:
                        for rule in agent_state["behavioral_rules"]:
                            # Simple rule matching
                            if any(
                                cond in str(context)
                                for cond in rule.split("THEN")[0].split()
                            ):
                                action = (
                                    rule.split("THEN")[1].strip()
                                    if "THEN" in rule
                                    else "monitor"
                                )
                                decision["decision"] = action
                                decision["reasoning"].append(f"Applied rule: {rule}")
                                break

                    # Use behavioral properties if no rule matched
                    if not decision["decision"]:
                        props = agent_state["behavioral_properties"]
                        if props.get("legal_aggression", 0) > 0.7:
                            decision["decision"] = "escalate_legally"
                            decision["reasoning"].append("High legal aggression")
                        elif props.get("control_seeking", 0) > 0.7:
                            decision["decision"] = "seek_control"
                            decision["reasoning"].append("High control seeking")
                        else:
                            decision["decision"] = "monitor"
                            decision["reasoning"].append("Default action")

                    decisions[actor] = decision

        return decisions

    def _count_event_states(self) -> Dict[str, int]:
        """Count events by state"""
        state_counts = {}
        for event in self.events.values():
            state_name = event.state.value
            state_counts[state_name] = state_counts.get(state_name, 0) + 1
        return state_counts

    def generate_evidence_report(self) -> Dict[str, Any]:
        """Generate comprehensive evidence report"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "case_id": self.case_id,
            "summary": {
                "total_events": len(self.events),
                "total_evidence_required": 0,
                "total_evidence_submitted": 0,
                "evidence_gap": 0,
            },
            "by_event": {},
            "critical_missing": [],
            "verification_status": {},
        }

        # Process each event
        for event_id, event in self.events.items():
            requirements = self.evidence_requirements.get(event_id, [])

            event_report = {
                "event_type": event.event_type.value,
                "timestamp": event.timestamp.isoformat(),
                "actors": event.actors,
                "evidence_required": event.evidence_required,
                "evidence_submitted": event.evidence_submitted,
                "requirements_detail": [],
            }

            # Add detailed requirements
            for req in requirements:
                req_detail = {
                    "type": req.evidence_type,
                    "description": req.description,
                    "status": req.status,
                    "priority": req.priority,
                    "legal_reference": req.legal_reference,
                    "deadline": req.deadline.isoformat() if req.deadline else None,
                }
                event_report["requirements_detail"].append(req_detail)

                # Track critical missing evidence
                if req.status == "required" and req.priority == "critical":
                    report["critical_missing"].append(
                        {
                            "event_id": event_id,
                            "evidence_type": req.evidence_type,
                            "description": req.description,
                            "deadline": (
                                req.deadline.isoformat() if req.deadline else "ASAP"
                            ),
                        }
                    )

            report["by_event"][event_id] = event_report

            # Update summary
            report["summary"]["total_evidence_required"] += len(event.evidence_required)
            report["summary"]["total_evidence_submitted"] += len(
                event.evidence_submitted
            )

        # Calculate evidence gap
        report["summary"]["evidence_gap"] = (
            report["summary"]["total_evidence_required"]
            - report["summary"]["total_evidence_submitted"]
        )

        # Verification status summary
        for event_id, requirements in self.evidence_requirements.items():
            for req in requirements:
                status = req.status
                report["verification_status"][status] = (
                    report["verification_status"].get(status, 0) + 1
                )

        return report

    def export_model(self) -> Dict[str, Any]:
        """Export complete discrete event model"""
        return {
            "case_id": self.case_id,
            "export_timestamp": datetime.now().isoformat(),
            "events": {
                event_id: {
                    "event_id": event.event_id,
                    "timestamp": event.timestamp.isoformat(),
                    "event_type": event.event_type.value,
                    "state": event.state.value,
                    "actors": event.actors,
                    "preconditions": event.preconditions,
                    "postconditions": event.postconditions,
                    "evidence_required": event.evidence_required,
                    "evidence_submitted": event.evidence_submitted,
                    "impact_vector": event.impact_vector.tolist(),
                    "has_knowledge_tensor": event.knowledge_tensor is not None,
                }
                for event_id, event in self.events.items()
            },
            "knowledge_tensors": {
                tensor_id: {
                    "tensor_id": tensor.tensor_id,
                    "dimensions": {
                        dim.value: size for dim, size in tensor.dimensions.items()
                    },
                    "shape": tensor.data.shape,
                    "timestamp": tensor.timestamp.isoformat(),
                }
                for tensor_id, tensor in self.knowledge_tensors.items()
            },
            "agent_states": self.agent_states,
            "event_graph": {
                "nodes": list(self.event_graph.nodes()),
                "edges": [
                    {"source": u, "target": v, "attributes": data}
                    for u, v, data in self.event_graph.edges(data=True)
                ],
            },
            "evidence_report": self.generate_evidence_report(),
        }

    def simulate_event_cascade(
        self, trigger_event_id: str, time_horizon: int = 30
    ) -> Dict[str, Any]:
        """
        Simulate cascading effects of events with enhanced temporal dynamics
        """
        if trigger_event_id not in self.events:
            return {"error": "Trigger event not found"}

        trigger_event = self.events[trigger_event_id]
        simulation_results = {
            "trigger_event": trigger_event_id,
            "time_horizon_days": time_horizon,
            "cascade_sequence": [],
            "affected_agents": set(),
            "probability_tree": {},
            "critical_paths": [],
        }

        # Initialize event probabilities
        event_probabilities = self._calculate_event_probabilities()

        # Simulate cascade over time horizon
        current_time = trigger_event.timestamp
        active_events = [trigger_event]

        for day in range(time_horizon):
            simulation_time = current_time + timedelta(days=day)
            day_events = []

            # Process active events and generate consequences
            for event in active_events:
                consequences = self._generate_event_consequences(
                    event, event_probabilities, simulation_time
                )
                for consequence in consequences:
                    # Add to cascade sequence
                    cascade_entry = {
                        "day": day,
                        "timestamp": simulation_time.isoformat(),
                        "trigger": event.event_id,
                        "consequence": consequence,
                        "probability": consequence.get("probability", 0.5),
                        "impact_score": consequence.get("impact_score", 0.3),
                    }
                    simulation_results["cascade_sequence"].append(cascade_entry)

                    # Track affected agents
                    if "affected_agents" in consequence:
                        simulation_results["affected_agents"].update(
                            consequence["affected_agents"]
                        )

                    day_events.append(consequence)

            # Update active events (events with ongoing effects)
            active_events = [e for e in day_events if e.get("ongoing", False)]

        # Analyze critical paths
        simulation_results["critical_paths"] = self._identify_critical_paths(
            simulation_results["cascade_sequence"]
        )

        # Build probability tree
        simulation_results["probability_tree"] = self._build_probability_tree(
            simulation_results["cascade_sequence"]
        )

        return simulation_results

    def run_temporal_sensitivity_analysis(self) -> Dict[str, Any]:
        """
        Analyze sensitivity to temporal changes in event sequence
        """
        sensitivity_results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "event_count": len(self.events),
            "sensitivity_metrics": {},
            "critical_windows": [],
            "temporal_dependencies": [],
        }

        # Sort events by timestamp
        sorted_events = sorted(self.events.values(), key=lambda e: e.timestamp)

        # Analyze temporal windows
        for i, event in enumerate(sorted_events):
            window_analysis = self._analyze_temporal_window(event, sorted_events, i)
            sensitivity_results["sensitivity_metrics"][event.event_id] = window_analysis

            if window_analysis["criticality_score"] > 0.7:
                sensitivity_results["critical_windows"].append(
                    {
                        "event_id": event.event_id,
                        "window_start": event.timestamp.isoformat(),
                        "window_end": (event.timestamp + timedelta(days=7)).isoformat(),
                        "criticality": window_analysis["criticality_score"],
                        "risk_factors": window_analysis["risk_factors"],
                    }
                )

        # Analyze dependencies
        dependency_analysis = self._analyze_temporal_dependencies(sorted_events)
        sensitivity_results["temporal_dependencies"] = dependency_analysis

        return sensitivity_results

    def generate_predictive_insights(self, forecast_days: int = 60) -> Dict[str, Any]:
        """
        Generate predictive insights based on event patterns
        """
        forecast_results = {
            "forecast_horizon_days": forecast_days,
            "prediction_confidence": 0.0,
            "likely_events": [],
            "risk_indicators": [],
            "intervention_opportunities": [],
        }

        # Analyze historical patterns
        event_patterns = self._extract_event_patterns()

        # Generate forecasts based on patterns
        forecast_timeline = datetime.now()
        for day in range(forecast_days):
            prediction_date = forecast_timeline + timedelta(days=day)

            # Calculate event likelihood for this day
            daily_predictions = self._predict_daily_events(
                event_patterns, prediction_date
            )

            for prediction in daily_predictions:
                if prediction["probability"] > 0.3:  # Only include likely events
                    forecast_results["likely_events"].append(
                        {
                            "predicted_date": prediction_date.isoformat(),
                            "event_type": prediction["event_type"],
                            "probability": prediction["probability"],
                            "confidence": prediction["confidence"],
                            "triggering_factors": prediction["factors"],
                        }
                    )

        # Identify risk indicators
        risk_indicators = self._identify_risk_indicators(event_patterns)
        forecast_results["risk_indicators"] = risk_indicators

        # Find intervention opportunities
        interventions = self._identify_intervention_opportunities(
            forecast_results["likely_events"]
        )
        forecast_results["intervention_opportunities"] = interventions

        # Calculate overall confidence
        if forecast_results["likely_events"]:
            avg_confidence = np.mean(
                [e["confidence"] for e in forecast_results["likely_events"]]
            )
            forecast_results["prediction_confidence"] = avg_confidence

        return forecast_results

    def _calculate_event_probabilities(self) -> Dict[str, float]:
        """Calculate base probabilities for different event types"""
        event_counts = {}
        total_events = len(self.events)

        for event in self.events.values():
            event_type = getattr(event, "event_type", "unknown")
            if event_type not in event_counts:
                event_counts[event_type] = 0
            event_counts[event_type] += 1

        # Calculate probabilities based on historical frequency
        probabilities = {}
        for event_type, count in event_counts.items():
            probabilities[event_type] = count / max(1, total_events)

        return probabilities

    def _generate_event_consequences(
        self,
        event: DiscreteEvent,
        probabilities: Dict[str, float],
        simulation_time: datetime,
    ) -> List[Dict[str, Any]]:
        """Generate potential consequences of an event"""
        consequences = []

        # Base consequence generation based on event type
        event_type = getattr(event, "event_type", "unknown")
        base_probability = probabilities.get(event_type, 0.3)

        # Generate different types of consequences
        consequence_types = [
            ("communication_response", base_probability * 0.8),
            ("investigation_escalation", base_probability * 0.4),
            ("legal_action", base_probability * 0.2),
            ("evidence_discovery", base_probability * 0.6),
        ]

        for cons_type, probability in consequence_types:
            if np.random.random() < probability:
                consequence = {
                    "type": cons_type,
                    "probability": probability,
                    "impact_score": np.random.uniform(0.2, 0.8),
                    "affected_agents": getattr(event, "actors", []),
                    "ongoing": probability > 0.5,
                    "timestamp": simulation_time.isoformat(),
                }
                consequences.append(consequence)

        return consequences

    def _identify_critical_paths(
        self, cascade_sequence: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify critical paths in the cascade sequence"""
        critical_paths = []

        # Group events by impact score
        high_impact_events = [
            e for e in cascade_sequence if e.get("impact_score", 0) > 0.6
        ]

        # Find sequences of high-impact events
        current_path = []
        for event in sorted(high_impact_events, key=lambda x: x["day"]):
            if not current_path or event["day"] - current_path[-1]["day"] <= 3:
                current_path.append(event)
            else:
                if len(current_path) >= 2:
                    critical_paths.append(
                        {
                            "path_id": f"critical_path_{len(critical_paths)}",
                            "events": current_path.copy(),
                            "total_impact": sum(
                                e["impact_score"] for e in current_path
                            ),
                            "duration_days": current_path[-1]["day"]
                            - current_path[0]["day"],
                        }
                    )
                current_path = [event]

        # Add final path if exists
        if len(current_path) >= 2:
            critical_paths.append(
                {
                    "path_id": f"critical_path_{len(critical_paths)}",
                    "events": current_path.copy(),
                    "total_impact": sum(e["impact_score"] for e in current_path),
                    "duration_days": current_path[-1]["day"] - current_path[0]["day"],
                }
            )

        return critical_paths

    def _build_probability_tree(
        self, cascade_sequence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build probability tree for cascade analysis"""
        tree = {"root": "trigger_event", "branches": {}, "cumulative_probabilities": {}}

        # Group by trigger events
        trigger_groups = {}
        for event in cascade_sequence:
            trigger = event["trigger"]
            if trigger not in trigger_groups:
                trigger_groups[trigger] = []
            trigger_groups[trigger].append(event)

        # Build branches
        for trigger, events in trigger_groups.items():
            tree["branches"][trigger] = {
                "event_count": len(events),
                "average_probability": np.mean([e["probability"] for e in events]),
                "consequences": [
                    e["consequence"]["type"] for e in events if "consequence" in e
                ],
            }

            # Calculate cumulative probability for this branch
            cumulative_prob = 1.0
            for event in events:
                cumulative_prob *= event["probability"]
            tree["cumulative_probabilities"][trigger] = cumulative_prob

        return tree

    def _analyze_temporal_window(
        self, event: DiscreteEvent, all_events: List[DiscreteEvent], event_index: int
    ) -> Dict[str, Any]:
        """Analyze temporal sensitivity for a specific event"""
        window_size = 7  # days
        window_start = event.timestamp - timedelta(days=window_size)
        window_end = event.timestamp + timedelta(days=window_size)

        # Find events in window
        window_events = []
        for other_event in all_events:
            if (
                window_start <= other_event.timestamp <= window_end
                and other_event != event
            ):
                window_events.append(other_event)

        # Calculate criticality score
        criticality_factors = {
            "event_density": len(window_events) / (2 * window_size),  # events per day
            "temporal_clustering": self._calculate_clustering_coefficient(
                event, window_events
            ),
            "cascade_potential": len(
                [e for e in window_events if e.timestamp > event.timestamp]
            )
            / max(1, len(window_events)),
        }

        criticality_score = sum(criticality_factors.values()) / len(criticality_factors)

        return {
            "criticality_score": min(1.0, criticality_score),
            "window_event_count": len(window_events),
            "risk_factors": criticality_factors,
            "sensitive_period": {
                "start": window_start.isoformat(),
                "end": window_end.isoformat(),
            },
        }

    def _calculate_clustering_coefficient(
        self, center_event: DiscreteEvent, window_events: List[DiscreteEvent]
    ) -> float:
        """Calculate temporal clustering coefficient"""
        if len(window_events) < 2:
            return 0.0

        # Calculate average time distance
        time_distances = []
        for event in window_events:
            distance = (
                abs((event.timestamp - center_event.timestamp).total_seconds()) / 86400
            )  # days
            time_distances.append(distance)

        if not time_distances:
            return 0.0

        # Clustering is inverse of time spread
        avg_distance = np.mean(time_distances)
        clustering = 1.0 / (1.0 + avg_distance)

        return clustering

    def _analyze_temporal_dependencies(
        self, sorted_events: List[DiscreteEvent]
    ) -> List[Dict[str, Any]]:
        """Analyze temporal dependencies between events"""
        dependencies = []

        for i, event1 in enumerate(sorted_events):
            for j, event2 in enumerate(sorted_events[i + 1 :], start=i + 1):
                time_gap = (
                    event2.timestamp - event1.timestamp
                ).total_seconds() / 86400  # days

                if time_gap <= 30:  # Consider dependencies within 30 days
                    # Check for agent overlap
                    actors1 = set(getattr(event1, "actors", []))
                    actors2 = set(getattr(event2, "actors", []))
                    agent_overlap = len(actors1.intersection(actors2)) / max(
                        1, len(actors1.union(actors2))
                    )

                    if (
                        agent_overlap > 0.3 or time_gap <= 7
                    ):  # Strong temporal or agent connection
                        dependency = {
                            "predecessor": event1.event_id,
                            "successor": event2.event_id,
                            "time_gap_days": time_gap,
                            "agent_overlap": agent_overlap,
                            "dependency_strength": min(
                                1.0, agent_overlap + (1.0 / (1.0 + time_gap))
                            ),
                            "dependency_type": (
                                "sequential" if time_gap <= 1 else "cascading"
                            ),
                        }
                        dependencies.append(dependency)

        return dependencies

    def _extract_event_patterns(self) -> Dict[str, Any]:
        """Extract patterns from historical events"""
        patterns = {
            "temporal_patterns": {},
            "agent_patterns": {},
            "sequence_patterns": [],
        }

        # Analyze temporal patterns
        event_times = [event.timestamp for event in self.events.values()]
        if event_times:
            time_diffs = []
            sorted_times = sorted(event_times)
            for i in range(1, len(sorted_times)):
                diff = (
                    sorted_times[i] - sorted_times[i - 1]
                ).total_seconds() / 86400  # days
                time_diffs.append(diff)

            if time_diffs:
                patterns["temporal_patterns"] = {
                    "average_interval_days": np.mean(time_diffs),
                    "interval_std": np.std(time_diffs),
                    "typical_interval_range": [
                        np.percentile(time_diffs, 25),
                        np.percentile(time_diffs, 75),
                    ],
                }

        return patterns

    def _predict_daily_events(
        self, patterns: Dict[str, Any], prediction_date: datetime
    ) -> List[Dict[str, Any]]:
        """Predict events for a specific day based on patterns"""
        predictions = []

        # Use temporal patterns to estimate likelihood
        temporal_patterns = patterns.get("temporal_patterns", {})
        avg_interval = temporal_patterns.get("average_interval_days", 7)

        # Simple prediction based on average intervals
        last_event_time = max(
            [event.timestamp for event in self.events.values()], default=datetime.now()
        )
        days_since_last = (prediction_date - last_event_time).total_seconds() / 86400

        # Calculate probability based on typical intervals
        if avg_interval > 0:
            interval_probability = min(1.0, days_since_last / avg_interval)

            # Predict different event types
            for event_type in ["communication", "investigation", "legal_action"]:
                type_probability = interval_probability * np.random.uniform(0.3, 0.8)
                if type_probability > 0.1:
                    predictions.append(
                        {
                            "event_type": event_type,
                            "probability": type_probability,
                            "confidence": min(0.8, type_probability * 1.2),
                            "factors": ["temporal_pattern", "historical_frequency"],
                        }
                    )

        return predictions

    def _identify_risk_indicators(
        self, patterns: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify risk indicators from event patterns"""
        indicators = []

        # Temporal clustering risk
        temporal_patterns = patterns.get("temporal_patterns", {})
        if (
            temporal_patterns.get("interval_std", 0)
            > temporal_patterns.get("average_interval_days", 7) * 0.5
        ):
            indicators.append(
                {
                    "type": "temporal_instability",
                    "severity": "medium",
                    "description": "High variance in event timing suggests unpredictable pattern",
                    "recommendation": "Monitor for sudden event clusters",
                }
            )

        return indicators

    def _identify_intervention_opportunities(
        self, likely_events: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify opportunities for intervention"""
        opportunities = []

        # Look for high-probability negative events that could be prevented
        high_risk_events = [e for e in likely_events if e["probability"] > 0.6]

        for event in high_risk_events:
            if event["event_type"] in ["legal_action", "investigation"]:
                opportunities.append(
                    {
                        "target_event": event,
                        "intervention_type": "preventive",
                        "optimal_timing": "immediate",
                        "success_probability": 0.7,
                        "recommended_actions": [
                            "stakeholder_communication",
                            "proactive_disclosure",
                        ],
                    }
                )

        return opportunities


def main():
    """Main execution function"""
    print("=== DISCRETE EVENT-DRIVEN MODEL GENERATOR ===")

    # Load enhanced timeline
    timeline_file = "/tmp/enhanced_timeline_case_2025_137857.json"
    if not Path(timeline_file).exists():
        print("Enhanced timeline not found. Running timeline processor...")
        from enhanced_timeline_processor import EnhancedTimelineProcessor

        from case_data_loader import CaseDataLoader

        # Load case data
        loader = CaseDataLoader("case_2025_137857")
        loader.load_case_documents()
        case_data = loader.export_case_data()

        # Process timeline
        processor = EnhancedTimelineProcessor("case_2025_137857")
        processor.load_case_timeline(case_data)
        enhanced_timeline = processor.export_enhanced_timeline()

        # Save timeline
        with open(timeline_file, "w") as f:
            json.dump(enhanced_timeline, f, indent=2, default=str)
    else:
        with open(timeline_file, "r") as f:
            enhanced_timeline = json.load(f)

    # Generate discrete event model
    model = DiscreteEventModel("case_2025_137857")

    # Convert timeline entries back to TimelineEntry objects
    timeline_entries = {}
    for entry_id, entry_data in enhanced_timeline["timeline_entries"].items():
        # Create TimelineEntry from data
        entry = TimelineEntry(
            entry_id=entry_data["entry_id"],
            date=datetime.fromisoformat(entry_data["date"]),
            title=entry_data["title"],
            description=entry_data["description"],
            entry_type=TimelineEntryType(entry_data["entry_type"]),
            participants=entry_data["participants"],
            information_status=InformationStatus(entry_data["information_status"]),
            verification_level=VerificationLevel(entry_data["verification_level"]),
            evidence_references=entry_data["evidence_references"],
            source_reliability=entry_data["source_reliability"],
            impact_assessment=entry_data["impact_assessment"],
            legal_significance=entry_data["legal_significance"],
            tags=set(entry_data["tags"]),
        )
        timeline_entries[entry_id] = entry

    # Process timeline
    results = model.process_timeline(timeline_entries)

    print(f"\n=== MODEL GENERATION RESULTS ===")
    print(f"Total events: {results['total_events']}")
    print(f"Event states: {results['event_states']}")
    print(f"Knowledge tensors: {results['knowledge_tensors']}")
    print(f"Evidence requirements: {results['evidence_requirements']}")

    # Export model
    model_export = model.export_model()

    # Save outputs
    model_file = "/tmp/discrete_event_model_case_2025_137857.json"
    with open(model_file, "w") as f:
        json.dump(model_export, f, indent=2, default=str)

    # Generate evidence report
    evidence_report = model.generate_evidence_report()
    report_file = "/tmp/evidence_requirements_report_case_2025_137857.json"
    with open(report_file, "w") as f:
        json.dump(evidence_report, f, indent=2)

    # Save knowledge tensors (metadata only, tensors too large for JSON)
    tensor_metadata = {
        tensor_id: {
            "tensor_id": tensor.tensor_id,
            "dimensions": {dim.value: size for dim, size in tensor.dimensions.items()},
            "shape": tensor.data.shape,
            "feature_names": {
                dim.value: names for dim, names in tensor.feature_names.items()
            },
            "timestamp": tensor.timestamp.isoformat(),
        }
        for tensor_id, tensor in model.knowledge_tensors.items()
    }

    tensor_file = "/tmp/knowledge_tensors_metadata_case_2025_137857.json"
    with open(tensor_file, "w") as f:
        json.dump(tensor_metadata, f, indent=2)

    print(f"\n✅ Discrete event model saved to: {model_file}")
    print(f"✅ Evidence report saved to: {report_file}")
    print(f"✅ Knowledge tensor metadata saved to: {tensor_file}")

    # Print summary
    print("\n=== EVIDENCE SUMMARY ===")
    print(
        f"Total evidence required: {evidence_report['summary']['total_evidence_required']}"
    )
    print(
        f"Total evidence submitted: {evidence_report['summary']['total_evidence_submitted']}"
    )
    print(f"Evidence gap: {evidence_report['summary']['evidence_gap']}")
    print(f"Critical missing evidence: {len(evidence_report['critical_missing'])}")

    if evidence_report["critical_missing"]:
        print("\n⚠️  CRITICAL MISSING EVIDENCE:")
        for missing in evidence_report["critical_missing"][:5]:  # Show first 5
            print(f"  - {missing['evidence_type']}: {missing['description']}")
            print(f"    Deadline: {missing['deadline']}")

    return model


if __name__ == "__main__":
    main()
