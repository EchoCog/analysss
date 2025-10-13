#!/usr/bin/env python3
"""
HyperGraphQL Schema Module
============================

Defines GraphQL schema for HyperGNN entities, relations, and hypergraph structures.
Provides org-aware schema definitions that support multi-level scaling:
- Repo-level: entities & relations in folder structures
- Org-level: aggregated views across repos
- Enterprise-level: cross-org analysis with compression/storage optimization
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union


class OrgLevel(Enum):
    """Organization hierarchy levels"""

    REPO = "repo"
    ORG = "org"
    ENTERPRISE = "enterprise"


class EntityTypeQL(Enum):
    """GraphQL-compatible entity types"""

    PERSON = "person"
    ORGANIZATION = "organization"
    EVENT = "event"
    EVIDENCE = "evidence"
    LOCATION = "location"
    DOCUMENT = "document"
    TRANSACTION = "transaction"
    AGENT = "agent"


class RelationTypeQL(Enum):
    """GraphQL-compatible relation types"""

    PARTICIPATES_IN = "participates_in"
    OWNS = "owns"
    CONTROLS = "controls"
    COMMUNICATES_WITH = "communicates_with"
    TRANSACTS_WITH = "transacts_with"
    LOCATED_AT = "located_at"
    EVIDENCES = "evidences"
    RELATED_TO = "related_to"
    PARENT_OF = "parent_of"
    MEMBER_OF = "member_of"


@dataclass
class HyperGraphQLNode:
    """
    GraphQL representation of a hypergraph node.
    Maps to HyperGNN entities and supports GitHub repo projection.
    """

    id: str
    node_type: EntityTypeQL
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)
    org_level: OrgLevel = OrgLevel.REPO
    repo_path: Optional[str] = None  # GitHub repo path
    folder_path: Optional[str] = None  # Folder path within repo
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_graphql_type(self) -> Dict[str, Any]:
        """Convert to GraphQL type representation"""
        return {
            "id": self.id,
            "nodeType": self.node_type.value,
            "name": self.name,
            "properties": self.properties,
            "orgLevel": self.org_level.value,
            "repoPath": self.repo_path,
            "folderPath": self.folder_path,
            "createdAt": self.created_at.isoformat(),
            "updatedAt": self.updated_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class HyperGraphQLEdge:
    """
    GraphQL representation of a hypergraph edge (relation).
    Supports multi-node connections and org-aware filtering.
    """

    id: str
    edge_type: RelationTypeQL
    source_id: str
    target_ids: List[str]  # Support hyperedges (multi-target)
    strength: float = 0.5
    properties: Dict[str, Any] = field(default_factory=dict)
    org_level: OrgLevel = OrgLevel.REPO
    evidence_refs: List[str] = field(default_factory=list)
    timestamp: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_graphql_type(self) -> Dict[str, Any]:
        """Convert to GraphQL type representation"""
        return {
            "id": self.id,
            "edgeType": self.edge_type.value,
            "sourceId": self.source_id,
            "targetIds": self.target_ids,
            "strength": self.strength,
            "properties": self.properties,
            "orgLevel": self.org_level.value,
            "evidenceRefs": self.evidence_refs,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "metadata": self.metadata,
        }


@dataclass
class HyperGraphQLOrgMapping:
    """
    Organization-aware mapping configuration.
    Defines how entities and relations map across GitHub org structure.
    """

    org_name: str
    org_level: OrgLevel
    repos: List[str] = field(default_factory=list)
    entity_folders: List[str] = field(default_factory=list)
    relation_folders: List[str] = field(default_factory=list)
    compression_enabled: bool = False
    aggregation_rules: Dict[str, Any] = field(default_factory=dict)

    def to_graphql_type(self) -> Dict[str, Any]:
        """Convert to GraphQL type representation"""
        return {
            "orgName": self.org_name,
            "orgLevel": self.org_level.value,
            "repos": self.repos,
            "entityFolders": self.entity_folders,
            "relationFolders": self.relation_folders,
            "compressionEnabled": self.compression_enabled,
            "aggregationRules": self.aggregation_rules,
        }


class HyperGraphQLSchema:
    """
    Main HyperGraphQL Schema manager.
    Handles schema definition, validation, and org-aware transformations.
    """

    def __init__(self):
        self.nodes: Dict[str, HyperGraphQLNode] = {}
        self.edges: Dict[str, HyperGraphQLEdge] = {}
        self.org_mappings: Dict[str, HyperGraphQLOrgMapping] = {}

    def add_node(self, node: HyperGraphQLNode) -> None:
        """Add a node to the schema"""
        self.nodes[node.id] = node

    def add_edge(self, edge: HyperGraphQLEdge) -> None:
        """Add an edge to the schema"""
        self.edges[edge.id] = edge

    def add_org_mapping(self, mapping: HyperGraphQLOrgMapping) -> None:
        """Add an organization mapping configuration"""
        self.org_mappings[mapping.org_name] = mapping

    def get_node(self, node_id: str) -> Optional[HyperGraphQLNode]:
        """Retrieve a node by ID"""
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: str) -> Optional[HyperGraphQLEdge]:
        """Retrieve an edge by ID"""
        return self.edges.get(edge_id)

    def get_nodes_by_type(
        self, node_type: EntityTypeQL, org_level: Optional[OrgLevel] = None
    ) -> List[HyperGraphQLNode]:
        """Get all nodes of a specific type, optionally filtered by org level"""
        nodes = [n for n in self.nodes.values() if n.node_type == node_type]
        if org_level:
            nodes = [n for n in nodes if n.org_level == org_level]
        return nodes

    def get_edges_by_type(
        self, edge_type: RelationTypeQL, org_level: Optional[OrgLevel] = None
    ) -> List[HyperGraphQLEdge]:
        """Get all edges of a specific type, optionally filtered by org level"""
        edges = [e for e in self.edges.values() if e.edge_type == edge_type]
        if org_level:
            edges = [e for e in edges if e.org_level == org_level]
        return edges

    def get_connected_nodes(self, node_id: str) -> List[HyperGraphQLNode]:
        """Get all nodes connected to a given node"""
        connected_ids = set()

        # Find edges where node is source
        for edge in self.edges.values():
            if edge.source_id == node_id:
                connected_ids.update(edge.target_ids)

        # Find edges where node is target
        for edge in self.edges.values():
            if node_id in edge.target_ids:
                connected_ids.add(edge.source_id)

        return [self.nodes[nid] for nid in connected_ids if nid in self.nodes]

    def export_schema(self, org_level: Optional[OrgLevel] = None) -> Dict[str, Any]:
        """Export the schema as a dictionary, optionally filtered by org level"""
        nodes = list(self.nodes.values())
        edges = list(self.edges.values())

        if org_level:
            nodes = [n for n in nodes if n.org_level == org_level]
            edges = [e for e in edges if e.org_level == org_level]

        return {
            "nodes": [n.to_graphql_type() for n in nodes],
            "edges": [e.to_graphql_type() for e in edges],
            "orgMappings": [m.to_graphql_type() for m in self.org_mappings.values()],
            "metadata": {
                "nodeCount": len(nodes),
                "edgeCount": len(edges),
                "orgMappingCount": len(self.org_mappings),
                "exportedAt": datetime.now().isoformat(),
            },
        }

    def get_graphql_schema_definition(self) -> str:
        """Generate GraphQL schema definition string"""
        return """
type HyperGraphQLNode {
  id: ID!
  nodeType: String!
  name: String!
  properties: JSON
  orgLevel: String!
  repoPath: String
  folderPath: String
  createdAt: DateTime!
  updatedAt: DateTime!
  metadata: JSON
  connectedNodes: [HyperGraphQLNode!]
}

type HyperGraphQLEdge {
  id: ID!
  edgeType: String!
  sourceId: ID!
  targetIds: [ID!]!
  strength: Float!
  properties: JSON
  orgLevel: String!
  evidenceRefs: [String!]
  timestamp: DateTime
  metadata: JSON
  sourceNode: HyperGraphQLNode
  targetNodes: [HyperGraphQLNode!]
}

type HyperGraphQLOrgMapping {
  orgName: String!
  orgLevel: String!
  repos: [String!]
  entityFolders: [String!]
  relationFolders: [String!]
  compressionEnabled: Boolean!
  aggregationRules: JSON
}

type Query {
  node(id: ID!): HyperGraphQLNode
  nodes(nodeType: String, orgLevel: String): [HyperGraphQLNode!]
  edge(id: ID!): HyperGraphQLEdge
  edges(edgeType: String, orgLevel: String): [HyperGraphQLEdge!]
  connectedNodes(nodeId: ID!): [HyperGraphQLNode!]
  orgMapping(orgName: String!): HyperGraphQLOrgMapping
  exportSchema(orgLevel: String): JSON
  
  # Evidence Refinery Queries
  refinedEvidence(evidenceId: String!): RefinedEvidenceResult
  evidenceSummary(evidenceId: String!): EvidenceSummary
  relatedEvidence(evidenceId: String!, threshold: Float = 0.7): [String!]!
  evidenceQualityReport(caseId: String!): EvidenceQualityReport
  processingStatus(caseId: String!): ProcessingStatusReport
}

type Mutation {
  addNode(input: HyperGraphQLNodeInput!): HyperGraphQLNode
  updateNode(id: ID!, input: HyperGraphQLNodeInput!): HyperGraphQLNode
  deleteNode(id: ID!): Boolean
  addEdge(input: HyperGraphQLEdgeInput!): HyperGraphQLEdge
  updateEdge(id: ID!, input: HyperGraphQLEdgeInput!): HyperGraphQLEdge
  deleteEdge(id: ID!): Boolean
  addOrgMapping(input: HyperGraphQLOrgMappingInput!): HyperGraphQLOrgMapping
  
  # Evidence Refinery Mutations
  addRawEvidence(input: RawEvidenceInput!): RefinedEvidenceResult
  processEvidence(evidenceId: String!): RefinedEvidenceResult
  createEvidenceRelationship(input: EvidenceRelationshipInput!): Boolean
  updateEvidenceQuality(evidenceId: String!, qualityScore: String!, confidence: Float!): RefinedEvidenceResult
  exportRefinedEvidence(caseId: String!, format: String = "json"): ExportResult
}

input HyperGraphQLNodeInput {
  nodeType: String!
  name: String!
  properties: JSON
  orgLevel: String
  repoPath: String
  folderPath: String
  metadata: JSON
}

input HyperGraphQLEdgeInput {
  edgeType: String!
  sourceId: ID!
  targetIds: [ID!]!
  strength: Float
  properties: JSON
  orgLevel: String
  evidenceRefs: [String]
  timestamp: DateTime
  metadata: JSON
}

input HyperGraphQLOrgMappingInput {
  orgName: String!
  orgLevel: String!
  repos: [String!]
  entityFolders: [String!]
  relationFolders: [String!]
  compressionEnabled: Boolean
  aggregationRules: JSON
}

scalar JSON
scalar DateTime

# Evidence Refinery Types
type RefinedEvidenceResult {
  evidenceId: String!
  originalContent: String!
  refinedContent: String
  qualityScore: String!
  confidence: Float!
  verificationStatus: String!
  sourceReliability: Float!
  corroborationCount: Int!
  processingStatus: String!
  atomId: String
  graphqlNodeId: String
  relatedEntities: [String!]
  ggmlAnalysis: JSON
  createdAt: DateTime!
  lastUpdated: DateTime!
  processingLog: [ProcessingLogEntry!]
}

type ProcessingLogEntry {
  timestamp: DateTime!
  action: String!
  metadata: JSON
}

type EvidenceSummary {
  evidenceId: String!
  qualityScore: String!
  confidence: Float!
  processingStatus: String!
  verificationStatus: String!
  sourceReliability: Float!
  originalContentLength: Int!
  refinedContentAvailable: Boolean!
  relatedEvidenceCount: Int!
  relatedEvidence: [String!]
  openCogAtomId: String
  hyperGraphQLNodeId: String
  ggmlAnalysisAvailable: Boolean!
  createdAt: DateTime!
  lastUpdated: DateTime!
  processingSteps: Int!
}

type EvidenceQualityReport {
  caseId: String!
  totalEvidence: Int!
  qualityDistribution: JSON!
  statusDistribution: JSON!
  averageConfidence: Float!
  totalRelationships: Int!
  reportTimestamp: DateTime!
}

type ProcessingStatusReport {
  caseId: String!
  totalEvidence: Int!
  atomSpaceSize: Int!
  hyperGraphQLNodes: Int!
  hyperGraphQLEdges: Int!
  ggmlPerformance: JSON!
  reportTimestamp: DateTime!
}

type ExportResult {
  success: Boolean!
  filepath: String
  message: String
  recordCount: Int
}

input RawEvidenceInput {
  evidenceId: String!
  content: String!
  source: String = "unknown"
  metadata: JSON
}

input EvidenceRelationshipInput {
  sourceId: String!
  targetId: String!
  relationshipType: String = "related_to"
  strength: Float = 0.8
}
"""
