#!/usr/bin/env python3
"""
Hypergraph Model for Complex Relationship Analysis
================================================

This module implements a comprehensive hypergraph model that can represent 
complex multi-way relationships between entities, events, and evidence.
Unlike traditional graphs where edges connect only two nodes, hyperedges
can connect multiple nodes simultaneously, making it ideal for legal case
analysis where multiple entities may be involved in single events.

Key Features:
- Multi-way relationships via hyperedges
- Temporal hypergraphs with time-aware analysis
- Integration with existing HyperGNN framework
- Evidence-based relationship weighting
- Complex pattern detection across multiple entities
"""

import numpy as np
import networkx as nx
from typing import Dict, List, Set, Tuple, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
from collections import defaultdict

from .hypergnn_core import Agent, AgentType, DiscreteEvent, EventType


class HyperedgeType(Enum):
    """Types of hyperedges in the hypergraph"""
    
    COMMUNICATION = "communication"  # Multi-party communications
    TRANSACTION = "transaction"      # Financial or resource transactions
    MEETING = "meeting"             # Physical or virtual meetings
    COLLABORATION = "collaboration"  # Working relationships
    EVIDENCE_CHAIN = "evidence_chain" # Evidence linking multiple entities
    TEMPORAL_SEQUENCE = "temporal_sequence" # Time-based connections
    CAUSAL_RELATIONSHIP = "causal_relationship" # Cause-effect relationships
    CONSPIRACY = "conspiracy"        # Coordinated activities
    CONFLICT = "conflict"           # Adversarial relationships


class RelationshipStrength(Enum):
    """Strength of relationships in hyperedges"""
    
    VERY_WEAK = 0.1
    WEAK = 0.3
    MODERATE = 0.5
    STRONG = 0.7
    VERY_STRONG = 0.9


@dataclass
class Hyperedge:
    """Represents a hyperedge connecting multiple nodes"""
    
    edge_id: str
    node_ids: Set[str]
    edge_type: HyperedgeType
    timestamp: datetime
    strength: float = 0.5
    description: str = ""
    evidence_refs: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate hyperedge after creation"""
        if len(self.node_ids) < 2:
            raise ValueError("Hyperedge must connect at least 2 nodes")
        if not 0 <= self.strength <= 1:
            raise ValueError("Strength must be between 0 and 1")


@dataclass
class HypergraphNode:
    """Represents a node in the hypergraph"""
    
    node_id: str
    node_type: str  # "agent", "event", "evidence", "resource"
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    creation_time: datetime = field(default_factory=datetime.now)


class HypergraphModel:
    """
    Comprehensive Hypergraph Model for Complex Relationship Analysis
    
    This model can represent and analyze complex multi-way relationships
    that are common in legal and investigative contexts.
    """
    
    def __init__(self, case_id: str):
        self.case_id = case_id
        self.nodes: Dict[str, HypergraphNode] = {}
        self.hyperedges: Dict[str, Hyperedge] = {}
        self.adjacency_matrix: Optional[np.ndarray] = None
        self.incidence_matrix: Optional[np.ndarray] = None
        self._node_index: Dict[str, int] = {}
        self._edge_index: Dict[str, int] = {}
        
    def add_node(self, node: HypergraphNode) -> None:
        """Add a node to the hypergraph"""
        self.nodes[node.node_id] = node
        self._rebuild_indices()
        
    def add_hyperedge(self, hyperedge: Hyperedge) -> None:
        """Add a hyperedge to the hypergraph"""
        # Validate that all nodes in the hyperedge exist
        for node_id in hyperedge.node_ids:
            if node_id not in self.nodes:
                raise ValueError(f"Node {node_id} not found in hypergraph")
        
        self.hyperedges[hyperedge.edge_id] = hyperedge
        self._rebuild_indices()
        
    def _rebuild_indices(self):
        """Rebuild node and edge indices for matrix operations"""
        self._node_index = {node_id: i for i, node_id in enumerate(self.nodes.keys())}
        self._edge_index = {edge_id: i for i, edge_id in enumerate(self.hyperedges.keys())}
        
    def build_incidence_matrix(self) -> np.ndarray:
        """Build the hypergraph incidence matrix"""
        n_nodes = len(self.nodes)
        n_edges = len(self.hyperedges)
        
        if n_nodes == 0 or n_edges == 0:
            return np.array([])
        
        # Initialize incidence matrix
        incidence = np.zeros((n_nodes, n_edges))
        
        for edge_id, hyperedge in self.hyperedges.items():
            edge_idx = self._edge_index[edge_id]
            for node_id in hyperedge.node_ids:
                node_idx = self._node_index[node_id]
                incidence[node_idx, edge_idx] = hyperedge.strength
                
        self.incidence_matrix = incidence
        return incidence
        
    def build_adjacency_matrix(self) -> np.ndarray:
        """Build adjacency matrix from hypergraph structure"""
        n_nodes = len(self.nodes)
        
        if n_nodes == 0:
            return np.array([])
        
        # Initialize adjacency matrix
        adjacency = np.zeros((n_nodes, n_nodes))
        
        # For each hyperedge, connect all pairs of nodes
        for hyperedge in self.hyperedges.values():
            node_indices = [self._node_index[node_id] for node_id in hyperedge.node_ids]
            
            # Connect all pairs of nodes in this hyperedge
            for i, idx_i in enumerate(node_indices):
                for j, idx_j in enumerate(node_indices):
                    if i != j:
                        # Weight by hyperedge strength and number of connections
                        weight = hyperedge.strength / len(node_indices)
                        adjacency[idx_i, idx_j] += weight
                        
        self.adjacency_matrix = adjacency
        return adjacency
        
    def find_cliques(self, min_size: int = 3) -> List[Set[str]]:
        """Find cliques (fully connected subsets) in the hypergraph"""
        # Convert to networkx graph for clique analysis
        G = nx.Graph()
        
        # Add nodes
        for node_id in self.nodes.keys():
            G.add_node(node_id)
            
        # Add edges based on hyperedge connections
        for hyperedge in self.hyperedges.values():
            node_list = list(hyperedge.node_ids)
            # Add edges between all pairs in the hyperedge
            for i in range(len(node_list)):
                for j in range(i + 1, len(node_list)):
                    if not G.has_edge(node_list[i], node_list[j]):
                        G.add_edge(node_list[i], node_list[j], weight=hyperedge.strength)
                    else:
                        # Increase weight for multiple connections
                        G[node_list[i]][node_list[j]]['weight'] += hyperedge.strength
                        
        # Find cliques
        cliques = []
        for clique in nx.find_cliques(G):
            if len(clique) >= min_size:
                cliques.append(set(clique))
                
        return cliques
        
    def find_communities(self) -> List[Set[str]]:
        """Find communities using modularity-based community detection"""
        G = nx.Graph()
        
        # Add nodes
        for node_id in self.nodes.keys():
            G.add_node(node_id)
            
        # Add weighted edges
        for hyperedge in self.hyperedges.values():
            node_list = list(hyperedge.node_ids)
            for i in range(len(node_list)):
                for j in range(i + 1, len(node_list)):
                    if not G.has_edge(node_list[i], node_list[j]):
                        G.add_edge(node_list[i], node_list[j], weight=hyperedge.strength)
                    else:
                        G[node_list[i]][node_list[j]]['weight'] += hyperedge.strength
        
        # Use Louvain community detection
        try:
            import community as community_louvain
            partition = community_louvain.best_partition(G)
            
            # Group nodes by community
            communities = defaultdict(set)
            for node, community_id in partition.items():
                communities[community_id].add(node)
                
            return list(communities.values())
        except ImportError:
            # Fallback to connected components
            return [set(component) for component in nx.connected_components(G)]
            
    def analyze_centrality(self) -> Dict[str, Dict[str, float]]:
        """Calculate various centrality measures for nodes"""
        if self.adjacency_matrix is None:
            self.build_adjacency_matrix()
            
        n_nodes = len(self.nodes)
        if n_nodes == 0:
            return {}
            
        centrality_measures = {}
        
        # Degree centrality (based on hyperedge participation)
        degree_centrality = {}
        for node_id, node_idx in self._node_index.items():
            # Count hyperedges this node participates in
            degree = sum(1 for hyperedge in self.hyperedges.values() 
                        if node_id in hyperedge.node_ids)
            degree_centrality[node_id] = degree / len(self.hyperedges) if self.hyperedges else 0
            
        # Eigenvector centrality (if adjacency matrix is available)
        eigenvector_centrality = {}
        if self.adjacency_matrix.size > 0:
            try:
                eigenvalues, eigenvectors = np.linalg.eig(self.adjacency_matrix)
                principal_eigenvector = np.abs(eigenvectors[:, np.argmax(eigenvalues)])
                
                for node_id, node_idx in self._node_index.items():
                    eigenvector_centrality[node_id] = principal_eigenvector[node_idx]
            except:
                # Fallback if eigenvector calculation fails
                eigenvector_centrality = {node_id: 0.0 for node_id in self.nodes.keys()}
                
        # Hyperedge centrality (unique to hypergraphs)
        hyperedge_centrality = {}
        for node_id in self.nodes.keys():
            # Calculate based on the sum of strengths of connected hyperedges
            total_strength = sum(hyperedge.strength for hyperedge in self.hyperedges.values() 
                               if node_id in hyperedge.node_ids)
            hyperedge_centrality[node_id] = total_strength
            
        # Compile results
        for node_id in self.nodes.keys():
            centrality_measures[node_id] = {
                "degree_centrality": degree_centrality.get(node_id, 0),
                "eigenvector_centrality": eigenvector_centrality.get(node_id, 0),
                "hyperedge_centrality": hyperedge_centrality.get(node_id, 0)
            }
            
        return centrality_measures
        
    def find_temporal_patterns(self) -> Dict[str, List[Tuple[datetime, str]]]:
        """Analyze temporal patterns in hyperedge formation"""
        temporal_patterns = defaultdict(list)
        
        # Sort hyperedges by timestamp
        sorted_edges = sorted(self.hyperedges.values(), key=lambda x: x.timestamp)
        
        for hyperedge in sorted_edges:
            # Track each node's participation over time
            for node_id in hyperedge.node_ids:
                temporal_patterns[node_id].append((hyperedge.timestamp, hyperedge.edge_id))
                
        return dict(temporal_patterns)
        
    def detect_suspicious_patterns(self) -> Dict[str, Any]:
        """Detect potentially suspicious patterns in the hypergraph"""
        suspicious_patterns = {
            "high_centrality_nodes": [],
            "dense_clusters": [],
            "temporal_anomalies": [],
            "isolated_groups": []
        }
        
        # High centrality nodes
        centrality = self.analyze_centrality()
        for node_id, measures in centrality.items():
            if (measures["degree_centrality"] > 0.7 or 
                measures["hyperedge_centrality"] > np.mean(list(m["hyperedge_centrality"] for m in centrality.values())) * 2):
                suspicious_patterns["high_centrality_nodes"].append(node_id)
                
        # Dense clusters
        cliques = self.find_cliques(min_size=3)
        for clique in cliques:
            if len(clique) >= 4:  # Groups of 4+ are worth investigating
                suspicious_patterns["dense_clusters"].append(list(clique))
                
        # Temporal anomalies (bursts of activity)
        temporal_patterns = self.find_temporal_patterns()
        for node_id, events in temporal_patterns.items():
            if len(events) >= 3:
                # Check for clusters of activity in short time periods
                time_diffs = []
                for i in range(1, len(events)):
                    diff = (events[i][0] - events[i-1][0]).total_seconds() / 3600  # hours
                    time_diffs.append(diff)
                
                # If multiple events happen within 24 hours, flag as suspicious
                if any(diff < 24 for diff in time_diffs):
                    suspicious_patterns["temporal_anomalies"].append(node_id)
                    
        # Isolated groups (potential conspiracies)
        communities = self.find_communities()
        for community in communities:
            if len(community) >= 3:
                # Check if this community is isolated from others
                external_connections = 0
                for hyperedge in self.hyperedges.values():
                    overlap_with_community = len(hyperedge.node_ids.intersection(community))
                    overlap_with_others = len(hyperedge.node_ids - community)
                    if overlap_with_community > 0 and overlap_with_others > 0:
                        external_connections += 1
                        
                if external_connections == 0:  # No external connections
                    suspicious_patterns["isolated_groups"].append(list(community))
                    
        return suspicious_patterns
        
    def export_model(self) -> Dict[str, Any]:
        """Export the complete hypergraph model"""
        # Build matrices if not already built
        if self.incidence_matrix is None:
            self.build_incidence_matrix()
        if self.adjacency_matrix is None:
            self.build_adjacency_matrix()
            
        return {
            "case_id": self.case_id,
            "export_timestamp": datetime.now().isoformat(),
            "nodes": {
                node_id: {
                    "node_type": node.node_type,
                    "name": node.name,
                    "properties": node.properties,
                    "creation_time": node.creation_time.isoformat()
                }
                for node_id, node in self.nodes.items()
            },
            "hyperedges": {
                edge_id: {
                    "node_ids": list(hyperedge.node_ids),
                    "edge_type": hyperedge.edge_type.value,
                    "timestamp": hyperedge.timestamp.isoformat(),
                    "strength": hyperedge.strength,
                    "description": hyperedge.description,
                    "evidence_refs": hyperedge.evidence_refs,
                    "metadata": hyperedge.metadata
                }
                for edge_id, hyperedge in self.hyperedges.items()
            },
            "analysis": {
                "centrality_measures": self.analyze_centrality(),
                "communities": [list(community) for community in self.find_communities()],
                "cliques": [list(clique) for clique in self.find_cliques()],
                "suspicious_patterns": self.detect_suspicious_patterns(),
                "temporal_patterns": {
                    node_id: [(t.isoformat(), edge_id) for t, edge_id in events]
                    for node_id, events in self.find_temporal_patterns().items()
                }
            },
            "matrices": {
                "incidence_matrix_shape": self.incidence_matrix.shape if self.incidence_matrix is not None else None,
                "adjacency_matrix_shape": self.adjacency_matrix.shape if self.adjacency_matrix is not None else None,
                "node_index": self._node_index,
                "edge_index": self._edge_index
            }
        }
        
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the hypergraph model"""
        return {
            "case_id": self.case_id,
            "total_nodes": len(self.nodes),
            "total_hyperedges": len(self.hyperedges),
            "node_types": list(set(node.node_type for node in self.nodes.values())),
            "hyperedge_types": list(set(edge.edge_type.value for edge in self.hyperedges.values())),
            "average_hyperedge_size": np.mean([len(edge.node_ids) for edge in self.hyperedges.values()]) if self.hyperedges else 0,
            "total_communities": len(self.find_communities()),
            "total_cliques": len(self.find_cliques())
        }


def create_sample_hypergraph() -> HypergraphModel:
    """Create a sample hypergraph for testing and demonstration"""
    model = HypergraphModel("sample_case_hypergraph")
    
    # Add nodes
    nodes = [
        HypergraphNode("agent_001", "agent", "Alice Johnson"),
        HypergraphNode("agent_002", "agent", "Bob Smith"),
        HypergraphNode("agent_003", "agent", "Carol Davis"),
        HypergraphNode("agent_004", "agent", "David Wilson"),
        HypergraphNode("event_001", "event", "Board Meeting"),
        HypergraphNode("event_002", "event", "Financial Transaction"),
        HypergraphNode("evidence_001", "evidence", "Email Chain"),
        HypergraphNode("evidence_002", "evidence", "Bank Records")
    ]
    
    for node in nodes:
        model.add_node(node)
    
    # Add hyperedges
    hyperedges = [
        Hyperedge(
            "meeting_001",
            {"agent_001", "agent_002", "agent_003", "event_001"},
            HyperedgeType.MEETING,
            datetime.now() - timedelta(days=10),
            strength=0.8,
            description="Three-party meeting about financial matters",
            evidence_refs=["evidence_001"]
        ),
        Hyperedge(
            "transaction_001",
            {"agent_002", "agent_004", "event_002", "evidence_002"},
            HyperedgeType.TRANSACTION,
            datetime.now() - timedelta(days=5),
            strength=0.9,
            description="Large financial transaction between parties",
            evidence_refs=["evidence_002"]
        ),
        Hyperedge(
            "communication_001",
            {"agent_001", "agent_003", "evidence_001"},
            HyperedgeType.COMMUNICATION,
            datetime.now() - timedelta(days=7),
            strength=0.6,
            description="Email communication regarding meeting",
            evidence_refs=["evidence_001"]
        )
    ]
    
    for hyperedge in hyperedges:
        model.add_hyperedge(hyperedge)
        
    return model


if __name__ == "__main__":
    # Create and test sample hypergraph
    print("=== HYPERGRAPH MODEL DEMONSTRATION ===")
    
    model = create_sample_hypergraph()
    
    print(f"\nCreated hypergraph for case: {model.case_id}")
    print(f"Nodes: {len(model.nodes)}")
    print(f"Hyperedges: {len(model.hyperedges)}")
    
    # Build matrices
    model.build_incidence_matrix()
    model.build_adjacency_matrix()
    
    print(f"\nIncidence matrix shape: {model.incidence_matrix.shape}")
    print(f"Adjacency matrix shape: {model.adjacency_matrix.shape}")
    
    # Analyze centrality
    centrality = model.analyze_centrality()
    print(f"\nCentrality measures for top nodes:")
    for node_id in list(centrality.keys())[:3]:
        measures = centrality[node_id]
        print(f"  {node_id}: degree={measures['degree_centrality']:.3f}, "
              f"hyperedge={measures['hyperedge_centrality']:.3f}")
    
    # Find communities
    communities = model.find_communities()
    print(f"\nFound {len(communities)} communities:")
    for i, community in enumerate(communities):
        print(f"  Community {i+1}: {list(community)}")
    
    # Detect suspicious patterns
    suspicious = model.detect_suspicious_patterns()
    print(f"\nSuspicious patterns detected:")
    for pattern_type, items in suspicious.items():
        if items:
            print(f"  {pattern_type}: {items}")
    
    print("\n✅ Hypergraph model demonstration complete!")