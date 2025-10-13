#!/usr/bin/env python3
"""
Case Hypergraph Constructor
===========================

Constructs a comprehensive hypergraph representation of case data, capturing:
- Multi-way relationships between entities
- Temporal evolution of connections
- Evidence-based edge weights
- Verification status tracking
- Pattern detection and anomaly identification
"""

import json
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import networkx as nx
import numpy as np

# Import case data loader
from case_data_loader import (
    CaseDataLoader,
    CaseEntity,
    CaseEvent,
    CaseRelationship,
    InformationStatus,
)


class HyperedgeType(Enum):
    """Types of hyperedges in the case hypergraph"""

    COMMUNICATION = "communication"
    TRANSACTION = "transaction"
    LEGAL_PROCEEDING = "legal_proceeding"
    ORGANIZATIONAL = "organizational"
    TEMPORAL_CLUSTER = "temporal_cluster"
    EVIDENCE_LINK = "evidence_link"
    CONTROL_STRUCTURE = "control_structure"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    # OCR Revelation-specific hyperedge types
    CHANNEL_CONTROL = "channel_control"  # Who actually controls vs owns channels
    KNOWLEDGE_ATTRIBUTION = "knowledge_attribution"  # Who actually knows vs claims to know
    INFORMATION_INTERCEPTION = "information_interception"  # Email hijacking patterns
    VERIFICATION_STATUS = "verification_status"  # Confirmed vs impossible knowledge claims


@dataclass
class Hyperedge:
    """Represents a hyperedge connecting multiple nodes"""

    edge_id: str
    nodes: Set[str]  # Set of node IDs connected by this hyperedge
    edge_type: HyperedgeType
    weight: float = 1.0
    timestamp: Optional[datetime] = None
    duration: Optional[timedelta] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    evidence_refs: List[str] = field(default_factory=list)
    verification_status: InformationStatus = InformationStatus.PARTIAL

    def contains_node(self, node_id: str) -> bool:
        """Check if hyperedge contains a specific node"""
        return node_id in self.nodes

    def intersection_size(self, other_nodes: Set[str]) -> int:
        """Get size of intersection with another set of nodes"""
        return len(self.nodes.intersection(other_nodes))

    def to_dict(self) -> Dict[str, Any]:
        """Convert hyperedge to dictionary representation"""
        return {
            "edge_id": self.edge_id,
            "nodes": list(self.nodes),
            "edge_type": self.edge_type.value,
            "weight": self.weight,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "duration": str(self.duration) if self.duration else None,
            "attributes": self.attributes,
            "evidence_refs": self.evidence_refs,
            "verification_status": self.verification_status.value,
        }


@dataclass
class HypergraphNode:
    """Represents a node in the hypergraph"""

    node_id: str
    node_type: str  # person, organization, email, etc.
    label: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    hyperedges: Set[str] = field(
        default_factory=set
    )  # IDs of hyperedges containing this node
    degree: int = 0  # Number of hyperedges containing this node
    weighted_degree: float = 0.0  # Sum of weights of hyperedges containing this node

    def add_hyperedge(self, edge_id: str, weight: float = 1.0):
        """Add hyperedge to this node"""
        self.hyperedges.add(edge_id)
        self.degree = len(self.hyperedges)
        self.weighted_degree += weight

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary representation"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "label": self.label,
            "attributes": self.attributes,
            "hyperedges": list(self.hyperedges),
            "degree": self.degree,
            "weighted_degree": self.weighted_degree,
        }


class CaseHypergraph:
    """Main hypergraph structure for case analysis"""

    def __init__(self, case_id: str):
        self.case_id = case_id
        self.nodes: Dict[str, HypergraphNode] = {}
        self.hyperedges: Dict[str, Hyperedge] = {}
        self.incidence_matrix: Optional[np.ndarray] = None
        self.node_index_map: Dict[str, int] = {}
        self.edge_index_map: Dict[str, int] = {}
        self.temporal_index: Dict[datetime, List[str]] = defaultdict(list)

    def add_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> HypergraphNode:
        """Add node to hypergraph"""
        if node_id not in self.nodes:
            self.nodes[node_id] = HypergraphNode(
                node_id=node_id,
                node_type=node_type,
                label=label,
                attributes=attributes or {},
            )
        return self.nodes[node_id]

    def add_hyperedge(
        self,
        edge_id: str,
        node_ids: Set[str],
        edge_type: HyperedgeType,
        weight: float = 1.0,
        timestamp: Optional[datetime] = None,
        attributes: Optional[Dict[str, Any]] = None,
        evidence_refs: Optional[List[str]] = None,
        verification_status: InformationStatus = InformationStatus.PARTIAL,
    ) -> Hyperedge:
        """Add hyperedge to hypergraph"""
        # Filter out nodes that don't exist
        valid_node_ids = set()
        for node_id in node_ids:
            if node_id in self.nodes:
                valid_node_ids.add(node_id)

        # Skip if no valid nodes
        if len(valid_node_ids) < 2:
            return None

        # Create hyperedge
        hyperedge = Hyperedge(
            edge_id=edge_id,
            nodes=valid_node_ids,
            edge_type=edge_type,
            weight=weight,
            timestamp=timestamp,
            attributes=attributes or {},
            evidence_refs=evidence_refs or [],
            verification_status=verification_status,
        )

        self.hyperedges[edge_id] = hyperedge

        # Update node references
        for node_id in valid_node_ids:
            self.nodes[node_id].add_hyperedge(edge_id, weight)

        # Update temporal index
        if timestamp:
            self.temporal_index[timestamp].append(edge_id)

        # Mark incidence matrix as needing update
        self.incidence_matrix = None

        return hyperedge

    def build_incidence_matrix(self) -> np.ndarray:
        """Build incidence matrix representation of hypergraph"""
        if self.incidence_matrix is not None:
            return self.incidence_matrix

        # Create index mappings
        self.node_index_map = {
            node_id: i for i, node_id in enumerate(sorted(self.nodes.keys()))
        }
        self.edge_index_map = {
            edge_id: j for j, edge_id in enumerate(sorted(self.hyperedges.keys()))
        }

        # Initialize matrix
        n_nodes = len(self.nodes)
        n_edges = len(self.hyperedges)
        self.incidence_matrix = np.zeros((n_nodes, n_edges))

        # Fill matrix
        for edge_id, hyperedge in self.hyperedges.items():
            edge_idx = self.edge_index_map[edge_id]
            for node_id in hyperedge.nodes:
                node_idx = self.node_index_map[node_id]
                self.incidence_matrix[node_idx, edge_idx] = hyperedge.weight

        return self.incidence_matrix

    def get_node_similarity_matrix(self) -> np.ndarray:
        """Compute node similarity based on shared hyperedges"""
        H = self.build_incidence_matrix()
        # Node similarity = H * H^T
        similarity = np.dot(H, H.T)
        # Normalize by diagonal
        diag = np.diag(similarity)
        diag_sqrt = np.sqrt(diag)
        # Avoid division by zero
        diag_sqrt[diag_sqrt == 0] = 1
        similarity = similarity / np.outer(diag_sqrt, diag_sqrt)
        return similarity

    def get_hyperedge_similarity_matrix(self) -> np.ndarray:
        """Compute hyperedge similarity based on shared nodes"""
        H = self.build_incidence_matrix()
        # Hyperedge similarity = H^T * H
        similarity = np.dot(H.T, H)
        # Normalize
        diag = np.diag(similarity)
        diag_sqrt = np.sqrt(diag)
        diag_sqrt[diag_sqrt == 0] = 1
        similarity = similarity / np.outer(diag_sqrt, diag_sqrt)
        return similarity

    def find_overlapping_hyperedges(
        self, min_overlap: int = 2
    ) -> List[Tuple[str, str, int]]:
        """Find hyperedges with significant node overlap"""
        overlaps = []
        edge_ids = list(self.hyperedges.keys())

        for i in range(len(edge_ids)):
            for j in range(i + 1, len(edge_ids)):
                edge1 = self.hyperedges[edge_ids[i]]
                edge2 = self.hyperedges[edge_ids[j]]
                overlap = len(edge1.nodes.intersection(edge2.nodes))

                if overlap >= min_overlap:
                    overlaps.append((edge_ids[i], edge_ids[j], overlap))

        return sorted(overlaps, key=lambda x: x[2], reverse=True)

    def detect_communities(self, resolution: float = 1.0) -> Dict[str, int]:
        """Detect communities in the hypergraph using Louvain algorithm on projected graph"""
        # Project hypergraph to regular graph
        G = nx.Graph()

        # Add nodes
        for node_id in self.nodes:
            G.add_node(node_id)

        # Add edges based on hyperedge co-occurrence
        for hyperedge in self.hyperedges.values():
            nodes_list = list(hyperedge.nodes)
            # Create clique for all nodes in hyperedge
            for i in range(len(nodes_list)):
                for j in range(i + 1, len(nodes_list)):
                    if G.has_edge(nodes_list[i], nodes_list[j]):
                        G[nodes_list[i]][nodes_list[j]]["weight"] += hyperedge.weight
                    else:
                        G.add_edge(
                            nodes_list[i], nodes_list[j], weight=hyperedge.weight
                        )

        # Apply Louvain community detection
        try:
            import community as community_louvain

            partition = community_louvain.best_partition(G, resolution=resolution)
        except ImportError:
            # Fallback to connected components if python-louvain not available
            components = list(nx.connected_components(G))
            partition = {}
            for i, component in enumerate(components):
                for node in component:
                    partition[node] = i

        return partition

    def find_temporal_patterns(self, window_days: int = 7) -> List[Dict[str, Any]]:
        """Find temporal patterns in hyperedge creation"""
        patterns = []

        # Sort temporal index
        sorted_times = sorted(self.temporal_index.keys())

        if not sorted_times:
            return patterns

        # Sliding window analysis
        for i, start_time in enumerate(sorted_times):
            end_time = start_time + timedelta(days=window_days)

            # Collect hyperedges in window
            window_edges = []
            for t in sorted_times[i:]:
                if t > end_time:
                    break
                window_edges.extend(self.temporal_index[t])

            if len(window_edges) >= 3:  # Minimum edges for pattern
                # Analyze pattern
                edge_types = defaultdict(int)
                participants = set()

                for edge_id in window_edges:
                    edge = self.hyperedges[edge_id]
                    edge_types[edge.edge_type.value] += 1
                    participants.update(edge.nodes)

                patterns.append(
                    {
                        "start_time": start_time,
                        "end_time": end_time,
                        "edge_count": len(window_edges),
                        "edge_types": dict(edge_types),
                        "unique_participants": len(participants),
                        "edges": window_edges,
                    }
                )

        return patterns

    def compute_centrality_measures(self) -> Dict[str, Dict[str, float]]:
        """Compute various centrality measures for nodes"""
        centrality = {
            "degree": {},
            "weighted_degree": {},
            "eigenvector": {},
            "betweenness": {},
        }

        # Degree centrality (already computed)
        for node_id, node in self.nodes.items():
            centrality["degree"][node_id] = node.degree
            centrality["weighted_degree"][node_id] = node.weighted_degree

        # Eigenvector centrality on node similarity
        similarity = self.get_node_similarity_matrix()
        eigenvalues, eigenvectors = np.linalg.eig(similarity)
        # Get dominant eigenvector
        dominant_idx = np.argmax(eigenvalues)
        dominant_eigenvector = np.abs(eigenvectors[:, dominant_idx])

        for node_id, idx in self.node_index_map.items():
            centrality["eigenvector"][node_id] = dominant_eigenvector[idx]

        # Betweenness centrality (approximate using projected graph)
        G = self._project_to_graph()
        betweenness = nx.betweenness_centrality(G, weight="weight")
        centrality["betweenness"] = betweenness

        return centrality

    def _project_to_graph(self) -> nx.Graph:
        """Project hypergraph to weighted graph"""
        G = nx.Graph()

        for node_id in self.nodes:
            G.add_node(node_id)

        for hyperedge in self.hyperedges.values():
            nodes_list = list(hyperedge.nodes)
            for i in range(len(nodes_list)):
                for j in range(i + 1, len(nodes_list)):
                    if G.has_edge(nodes_list[i], nodes_list[j]):
                        G[nodes_list[i]][nodes_list[j]]["weight"] += hyperedge.weight
                    else:
                        G.add_edge(
                            nodes_list[i], nodes_list[j], weight=hyperedge.weight
                        )

        return G

    def export_to_dict(self) -> Dict[str, Any]:
        """Export hypergraph to dictionary format"""
        return {
            "case_id": self.case_id,
            "metadata": {
                "node_count": len(self.nodes),
                "hyperedge_count": len(self.hyperedges),
                "creation_time": datetime.now().isoformat(),
            },
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "hyperedges": {
                edge_id: edge.to_dict() for edge_id, edge in self.hyperedges.items()
            },
            "analysis": {
                "communities": self.detect_communities(),
                "centrality": self.compute_centrality_measures(),
                "temporal_patterns": self.find_temporal_patterns(),
                "overlapping_edges": self.find_overlapping_hyperedges(),
            },
        }

    def save_to_file(self, filepath: str):
        """Save hypergraph to JSON file"""
        data = self.export_to_dict()
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2, default=str)

    @classmethod
    def load_from_file(cls, filepath: str) -> "CaseHypergraph":
        """Load hypergraph from JSON file"""
        with open(filepath, "r") as f:
            data = json.load(f)

        hypergraph = cls(data["case_id"])

        # Load nodes
        for node_data in data["nodes"].values():
            hypergraph.add_node(
                node_id=node_data["node_id"],
                node_type=node_data["node_type"],
                label=node_data["label"],
                attributes=node_data["attributes"],
            )

        # Load hyperedges
        for edge_data in data["hyperedges"].values():
            timestamp = None
            if edge_data["timestamp"]:
                timestamp = datetime.fromisoformat(edge_data["timestamp"])

            hypergraph.add_hyperedge(
                edge_id=edge_data["edge_id"],
                node_ids=set(edge_data["nodes"]),
                edge_type=HyperedgeType(edge_data["edge_type"]),
                weight=edge_data["weight"],
                timestamp=timestamp,
                attributes=edge_data["attributes"],
                evidence_refs=edge_data["evidence_refs"],
                verification_status=InformationStatus(edge_data["verification_status"]),
            )

        return hypergraph


class CaseHypergraphBuilder:
    """Builds case hypergraph from case data"""

    def __init__(self, case_data_loader: CaseDataLoader):
        self.loader = case_data_loader
        self.hypergraph = CaseHypergraph(case_data_loader.case_id)

    def build(self) -> CaseHypergraph:
        """Build complete hypergraph from case data"""
        print("Building case hypergraph...")

        # Add all entities as nodes
        self._add_entity_nodes()

        # Create hyperedges from events
        self._create_event_hyperedges()

        # Create hyperedges from relationships
        self._create_relationship_hyperedges()

        # Create temporal clustering hyperedges
        self._create_temporal_hyperedges()

        # Create evidence-based hyperedges
        self._create_evidence_hyperedges()

        print(
            f"Hypergraph built with {len(self.hypergraph.nodes)} nodes and {len(self.hypergraph.hyperedges)} hyperedges"
        )

        return self.hypergraph

    def _add_entity_nodes(self):
        """Add all entities as nodes in the hypergraph"""
        for entity_id, entity in self.loader.entities.items():
            self.hypergraph.add_node(
                node_id=entity_id,
                node_type=entity.entity_type,
                label=entity.name,
                attributes={
                    "roles": entity.roles,
                    "verification_status": entity.verification_status.value,
                    "evidence_count": len(entity.evidence_references),
                    **entity.attributes,
                },
            )

    def _create_event_hyperedges(self):
        """Create hyperedges from events"""
        for event in self.loader.events:
            if (
                len(event.participants) >= 2
            ):  # Only create hyperedge if multiple participants
                # Determine edge type based on event type
                edge_type = self._map_event_type_to_hyperedge_type(event.event_type)

                # Calculate weight based on verification status
                weight = self._calculate_edge_weight(event.verification_status)

                self.hypergraph.add_hyperedge(
                    edge_id=f"event_{event.event_id}",
                    node_ids=set(event.participants),
                    edge_type=edge_type,
                    weight=weight,
                    timestamp=event.date,
                    attributes={
                        "description": event.description,
                        "event_type": event.event_type,
                    },
                    evidence_refs=event.evidence_references,
                    verification_status=event.verification_status,
                )

    def _create_relationship_hyperedges(self):
        """Create hyperedges from relationships"""
        # Group relationships by type and create hyperedges
        relationship_groups = defaultdict(list)

        for rel in self.loader.relationships:
            key = (rel.relationship_type, rel.source_entity)
            relationship_groups[key].append(rel)

        # Create hyperedges for relationship groups
        for (rel_type, source), rels in relationship_groups.items():
            if len(rels) >= 2:  # Multiple targets from same source
                nodes = {source}
                nodes.update([rel.target_entity for rel in rels])

                # Calculate average weight
                avg_weight = sum(
                    self._calculate_edge_weight(rel.verification_status) for rel in rels
                ) / len(rels)

                edge_type = self._map_relationship_type_to_hyperedge_type(rel_type)

                self.hypergraph.add_hyperedge(
                    edge_id=f"rel_group_{source}_{rel_type}",
                    node_ids=nodes,
                    edge_type=edge_type,
                    weight=avg_weight,
                    attributes={
                        "relationship_type": rel_type,
                        "relationship_count": len(rels),
                    },
                    evidence_refs=[
                        ref for rel in rels for ref in rel.evidence_references
                    ],
                    verification_status=InformationStatus.PARTIAL,
                )

    def _create_temporal_hyperedges(self):
        """Create hyperedges based on temporal clustering"""
        # Group events by time windows
        time_window = timedelta(days=1)  # 1-day window

        if not self.loader.events:
            return

        # Sort events by date
        sorted_events = sorted(
            [e for e in self.loader.events if e.date], key=lambda x: x.date
        )

        if not sorted_events:
            return

        current_window_start = sorted_events[0].date
        current_window_events = []

        for event in sorted_events:
            if event.date - current_window_start <= time_window:
                current_window_events.append(event)
            else:
                # Create hyperedge for current window if sufficient events
                if len(current_window_events) >= 3:
                    self._create_temporal_cluster_edge(
                        current_window_events, current_window_start
                    )

                # Start new window
                current_window_start = event.date
                current_window_events = [event]

        # Handle last window
        if len(current_window_events) >= 3:
            self._create_temporal_cluster_edge(
                current_window_events, current_window_start
            )

    def _create_temporal_cluster_edge(
        self, events: List[CaseEvent], window_start: datetime
    ):
        """Create temporal cluster hyperedge"""
        # Collect all unique participants
        participants = set()
        for event in events:
            participants.update(event.participants)

        if len(participants) >= 2:
            self.hypergraph.add_hyperedge(
                edge_id=f"temporal_cluster_{window_start.strftime('%Y%m%d')}",
                node_ids=participants,
                edge_type=HyperedgeType.TEMPORAL_CLUSTER,
                weight=len(events),  # Weight by number of events
                timestamp=window_start,
                attributes={
                    "event_count": len(events),
                    "event_ids": [e.event_id for e in events],
                    "window_days": 1,
                },
                verification_status=InformationStatus.PARTIAL,
            )

    def _create_evidence_hyperedges(self):
        """Create hyperedges based on shared evidence"""
        # Group entities by shared evidence references
        evidence_groups = defaultdict(set)

        for entity_id, entity in self.loader.entities.items():
            for evidence_ref in entity.evidence_references:
                evidence_groups[evidence_ref].add(entity_id)

        # Create hyperedges for entities sharing evidence
        for evidence_ref, entity_ids in evidence_groups.items():
            if len(entity_ids) >= 3:  # At least 3 entities share evidence
                self.hypergraph.add_hyperedge(
                    edge_id=f"evidence_link_{Path(evidence_ref).stem}",
                    node_ids=entity_ids,
                    edge_type=HyperedgeType.EVIDENCE_LINK,
                    weight=1.0,
                    attributes={
                        "evidence_source": evidence_ref,
                        "entity_count": len(entity_ids),
                    },
                    evidence_refs=[evidence_ref],
                    verification_status=InformationStatus.SAVED,
                )

    def _map_event_type_to_hyperedge_type(self, event_type: str) -> HyperedgeType:
        """Map event types to hyperedge types"""
        mapping = {
            "communication": HyperedgeType.COMMUNICATION,
            "legal_proceeding": HyperedgeType.LEGAL_PROCEEDING,
            "financial_crime": HyperedgeType.TRANSACTION,
            "criminal_homicide": HyperedgeType.EVIDENCE_LINK,
            "report": HyperedgeType.KNOWLEDGE_SHARING,
        }
        return mapping.get(event_type, HyperedgeType.EVIDENCE_LINK)

    def _map_relationship_type_to_hyperedge_type(self, rel_type: str) -> HyperedgeType:
        """Map relationship types to hyperedge types"""
        mapping = {
            "controls": HyperedgeType.CONTROL_STRUCTURE,
            "communicates_with": HyperedgeType.COMMUNICATION,
            "employed_by": HyperedgeType.ORGANIZATIONAL,
            "financial_transfer": HyperedgeType.TRANSACTION,
        }
        return mapping.get(rel_type, HyperedgeType.ORGANIZATIONAL)

    def _calculate_edge_weight(self, verification_status: InformationStatus) -> float:
        """Calculate edge weight based on verification status"""
        weights = {
            InformationStatus.VERIFIED: 1.0,
            InformationStatus.SAVED: 0.8,
            InformationStatus.PARTIAL: 0.6,
            InformationStatus.CIRCUMSTANTIAL: 0.4,
            InformationStatus.SPECULATIVE: 0.2,
            InformationStatus.MISSING: 0.1,
        }
        return weights.get(verification_status, 0.5)

    def add_ocr_channel_control_revelation(
        self,
        channel_address: str,
        nominal_owner: str,
        actual_controller: str,
        evidence_source: str,
        timestamp: Optional[datetime] = None
    ):
        """Add OCR revelation about channel control vs ownership
        
        Args:
            channel_address: The email/communication address (e.g., "Pete@regima.com")
            nominal_owner: Who the address appears to belong to (e.g., "Peter Faucitt")
            actual_controller: Who actually controls it (e.g., "Rynette Farrar")
            evidence_source: OCR screenshot or other evidence reference
            timestamp: When the revelation was discovered
        """
        # Add nodes if they don't exist
        channel_node_id = f"channel_{channel_address.replace('@', '_at_').replace('.', '_')}"
        self.add_node(channel_node_id, "communication_channel", channel_address, {
            "channel_type": "email",
            "address": channel_address,
            "ocr_verified": True
        })
        
        nominal_owner_id = f"person_{nominal_owner.replace(' ', '_').lower()}"
        self.add_node(nominal_owner_id, "person", nominal_owner, {
            "role": "nominal_owner"
        })
        
        actual_controller_id = f"person_{actual_controller.replace(' ', '_').lower()}"
        self.add_node(actual_controller_id, "person", actual_controller, {
            "role": "actual_controller"
        })

        # Add channel control hyperedge
        self.add_hyperedge(
            edge_id=f"channel_control_{channel_node_id}",
            node_ids={channel_node_id, nominal_owner_id, actual_controller_id},
            edge_type=HyperedgeType.CHANNEL_CONTROL,
            weight=1.0,  # High weight - OCR verified
            timestamp=timestamp,
            attributes={
                "control_type": "email_hijacking",
                "nominal_owner": nominal_owner,
                "actual_controller": actual_controller,
                "channel": channel_address,
                "ocr_verified": True,
                "legal_implications": ["identity_theft", "information_warfare", "perjury_evidence"]
            },
            evidence_refs=[evidence_source],
            verification_status=InformationStatus.VERIFIED
        )

    def add_knowledge_attribution_correction(
        self,
        person: str,
        claimed_knowledge: str,
        actual_source: str,
        event_id: str,
        impossibility_reason: str,
        evidence_source: str
    ):
        """Add correction for knowledge attribution based on OCR revelations
        
        Args:
            person: Person claiming direct knowledge
            claimed_knowledge: What they claim to know directly
            actual_source: Who actually provided the information
            event_id: Related event or communication
            impossibility_reason: Why direct knowledge is impossible
            evidence_source: OCR or other evidence supporting correction
        """
        person_id = f"person_{person.replace(' ', '_').lower()}"
        source_id = f"person_{actual_source.replace(' ', '_').lower()}"
        event_node_id = f"event_{event_id}"
        
        # Add nodes
        self.add_node(person_id, "person", person, {"knowledge_claim": "impossible"})
        self.add_node(source_id, "person", actual_source, {"knowledge_role": "information_controller"})
        self.add_node(event_node_id, "event", f"Knowledge Event: {claimed_knowledge}", {
            "knowledge_type": "claimed_vs_actual"
        })

        # Add knowledge attribution hyperedge
        self.add_hyperedge(
            edge_id=f"knowledge_attribution_{person_id}_{event_id}",
            node_ids={person_id, source_id, event_node_id},
            edge_type=HyperedgeType.KNOWLEDGE_ATTRIBUTION,
            weight=0.0,  # Zero weight - impossible claim
            attributes={
                "claimed_knowledge": claimed_knowledge,
                "actual_source": actual_source,
                "impossibility_reason": impossibility_reason,
                "perjury_evidence": True,
                "verification_status": "impossible"
            },
            evidence_refs=[evidence_source],
            verification_status=InformationStatus.VERIFIED  # Impossibility is verified
        )

    def add_information_interception_pattern(
        self,
        interceptor: str,
        target_channel: str,
        intended_recipient: str,
        communications: List[str],
        evidence_source: str
    ):
        """Add systematic information interception pattern
        
        Args:
            interceptor: Person controlling the interception
            target_channel: Communication channel being intercepted
            intended_recipient: Person who should receive communications
            communications: List of intercepted communications
            evidence_source: Evidence supporting the interception pattern
        """
        interceptor_id = f"person_{interceptor.replace(' ', '_').lower()}"
        recipient_id = f"person_{intended_recipient.replace(' ', '_').lower()}"
        channel_id = f"channel_{target_channel.replace('@', '_at_').replace('.', '_')}"
        
        # Add nodes
        self.add_node(interceptor_id, "person", interceptor, {
            "role": "information_interceptor",
            "intercept_capability": True
        })
        self.add_node(recipient_id, "person", intended_recipient, {
            "role": "intended_recipient",
            "information_dependency": interceptor
        })
        self.add_node(channel_id, "communication_channel", target_channel, {
            "interception_status": "compromised"
        })

        # Add interception pattern hyperedge
        self.add_hyperedge(
            edge_id=f"interception_pattern_{channel_id}",
            node_ids={interceptor_id, recipient_id, channel_id},
            edge_type=HyperedgeType.INFORMATION_INTERCEPTION,
            weight=1.0,
            attributes={
                "interception_method": "email_control",
                "communications_affected": communications,
                "pattern_type": "systematic_filtering",
                "legal_implications": ["criminal_conspiracy", "information_warfare"]
            },
            evidence_refs=[evidence_source],
            verification_status=InformationStatus.VERIFIED
        )

    def integrate_ocr_revelations(self, ocr_data: Dict[str, Any]):
        """Integrate all OCR revelations into the hypergraph
        
        Args:
            ocr_data: Dictionary containing OCR findings from tools/ocr_analyzer.py
        """
        timestamp = datetime.now()
        
        # Process Pete@regima.com revelation
        if "email_control" in ocr_data:
            pete_email_data = ocr_data["email_control"].get("Pete@regima.com", {})
            if pete_email_data:
                self.add_ocr_channel_control_revelation(
                    channel_address="Pete@regima.com",
                    nominal_owner="Peter Faucitt", 
                    actual_controller="Rynette Farrar",
                    evidence_source="OCR Screenshot 2025-06-20 Sage Account system",
                    timestamp=timestamp
                )
        
        # Process impossible knowledge claims
        if "impossible_knowledge_claims" in ocr_data:
            for claim in ocr_data["impossible_knowledge_claims"]:
                self.add_knowledge_attribution_correction(
                    person=claim.get("person", "Peter Faucitt"),
                    claimed_knowledge=claim.get("claimed_knowledge", "Direct email receipt"),
                    actual_source=claim.get("actual_source", "Rynette Farrar"),
                    event_id=claim.get("event_id", "email_receipt_claim"),
                    impossibility_reason=claim.get("reason", "Email controlled by different person"),
                    evidence_source=claim.get("evidence", "OCR system access verification")
                )
        
        # Process systematic interception patterns
        if "interception_patterns" in ocr_data:
            for pattern in ocr_data["interception_patterns"]:
                self.add_information_interception_pattern(
                    interceptor=pattern.get("interceptor", "Rynette Farrar"),
                    target_channel=pattern.get("channel", "Pete@regima.com"),
                    intended_recipient=pattern.get("intended_recipient", "Peter Faucitt"),
                    communications=pattern.get("communications", []),
                    evidence_source=pattern.get("evidence", "OCR system access analysis")
                )

    def export_ocr_verified_relationships(self) -> Dict[str, Any]:
        """Export OCR-verified relationships for legal evidence
        
        Returns:
            Dictionary containing verified relationships and evidence
        """
        ocr_relationships = {
            "channel_controls": [],
            "knowledge_impossibilities": [],
            "interception_patterns": [],
            "perjury_evidence": []
        }
        
        for edge_id, hyperedge in self.hyperedges.items():
            if hyperedge.verification_status == InformationStatus.VERIFIED:
                edge_data = hyperedge.to_dict()
                
                if hyperedge.edge_type == HyperedgeType.CHANNEL_CONTROL:
                    ocr_relationships["channel_controls"].append(edge_data)
                elif hyperedge.edge_type == HyperedgeType.KNOWLEDGE_ATTRIBUTION:
                    ocr_relationships["knowledge_impossibilities"].append(edge_data)
                elif hyperedge.edge_type == HyperedgeType.INFORMATION_INTERCEPTION:
                    ocr_relationships["interception_patterns"].append(edge_data)
                
                # Check for perjury evidence
                if hyperedge.attributes.get("perjury_evidence"):
                    ocr_relationships["perjury_evidence"].append({
                        "edge_id": edge_id,
                        "evidence_type": "impossible_knowledge_claim",
                        "legal_implications": hyperedge.attributes.get("legal_implications", []),
                        "evidence_sources": hyperedge.evidence_refs
                    })
        
        return ocr_relationships


def main():
    """Main function to demonstrate hypergraph construction"""
    print("=== CASE HYPERGRAPH CONSTRUCTION ===\n")

    # Load case data
    print("Loading case data...")
    loader = CaseDataLoader("case_2025_137857", base_directory="/workspace")
    loader.load_case_documents()

    # Build hypergraph
    builder = CaseHypergraphBuilder(loader)
    hypergraph = builder.build()

    # Perform analysis
    print("\n=== HYPERGRAPH ANALYSIS ===")

    # Basic statistics
    print(f"\nNodes: {len(hypergraph.nodes)}")
    print(f"Hyperedges: {len(hypergraph.hyperedges)}")

    # Node degree distribution
    degrees = [node.degree for node in hypergraph.nodes.values()]
    if degrees:
        print(f"\nNode degree statistics:")
        print(f"  Min: {min(degrees)}")
        print(f"  Max: {max(degrees)}")
        print(f"  Average: {sum(degrees) / len(degrees):.2f}")

    # Hyperedge size distribution
    edge_sizes = [len(edge.nodes) for edge in hypergraph.hyperedges.values()]
    if edge_sizes:
        print(f"\nHyperedge size statistics:")
        print(f"  Min: {min(edge_sizes)}")
        print(f"  Max: {max(edge_sizes)}")
        print(f"  Average: {sum(edge_sizes) / len(edge_sizes):.2f}")

    # Community detection
    print("\n=== COMMUNITY DETECTION ===")
    communities = hypergraph.detect_communities()
    community_counts = defaultdict(int)
    for node, community in communities.items():
        community_counts[community] += 1

    print(f"Number of communities: {len(community_counts)}")
    for comm_id, count in sorted(
        community_counts.items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"  Community {comm_id}: {count} nodes")

    # Centrality analysis
    print("\n=== CENTRALITY ANALYSIS ===")
    centrality = hypergraph.compute_centrality_measures()

    # Top nodes by degree centrality
    print("\nTop 5 nodes by degree centrality:")
    top_degree = sorted(centrality["degree"].items(), key=lambda x: x[1], reverse=True)[
        :5
    ]
    for node_id, degree in top_degree:
        node = hypergraph.nodes[node_id]
        print(f"  {node.label} ({node.node_type}): {degree}")

    # Top nodes by eigenvector centrality
    print("\nTop 5 nodes by eigenvector centrality:")
    top_eigen = sorted(
        centrality["eigenvector"].items(), key=lambda x: x[1], reverse=True
    )[:5]
    for node_id, eigen in top_eigen:
        node = hypergraph.nodes[node_id]
        print(f"  {node.label} ({node.node_type}): {eigen:.4f}")

    # Temporal patterns
    print("\n=== TEMPORAL PATTERNS ===")
    patterns = hypergraph.find_temporal_patterns(window_days=7)
    print(f"Found {len(patterns)} temporal patterns")

    if patterns:
        # Show most active time window
        most_active = max(patterns, key=lambda x: x["edge_count"])
        print(f"\nMost active period:")
        print(f"  Start: {most_active['start_time'].strftime('%Y-%m-%d')}")
        print(f"  Edges: {most_active['edge_count']}")
        print(f"  Participants: {most_active['unique_participants']}")
        print(f"  Edge types: {most_active['edge_types']}")

    # Overlapping hyperedges
    print("\n=== OVERLAPPING HYPEREDGES ===")
    overlaps = hypergraph.find_overlapping_hyperedges(min_overlap=2)
    print(f"Found {len(overlaps)} overlapping hyperedge pairs")

    if overlaps:
        print("\nTop 5 overlapping pairs:")
        for edge1_id, edge2_id, overlap in overlaps[:5]:
            edge1 = hypergraph.hyperedges[edge1_id]
            edge2 = hypergraph.hyperedges[edge2_id]
            print(f"  {edge1_id} & {edge2_id}: {overlap} shared nodes")

    # Save hypergraph
    output_file = "/workspace/case_hypergraph.json"
    hypergraph.save_to_file(output_file)
    print(f"\n✅ Hypergraph saved to: {output_file}")

    return hypergraph


if __name__ == "__main__":
    hypergraph = main()
