#!/usr/bin/env python3
"""
HyperGraphQL Resolvers
=======================

Implements GraphQL resolvers for HyperGNN entities and relations.
Provides org-aware query resolution with support for:
- Entity navigation and filtering
- Relation traversal and hypergraph queries
- Org-level aggregation and scaling
- GitHub repo structure integration
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .hypergraphql_schema import (
    EntityTypeQL,
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLOrgMapping,
    HyperGraphQLSchema,
    OrgLevel,
    RelationTypeQL,
)

# Import HyperGNN framework if available
try:
    from .hypergnn_core import Agent, DiscreteEvent, HyperGNNFramework

    HYPERGNN_AVAILABLE = True
except ImportError:
    HYPERGNN_AVAILABLE = False

logger = logging.getLogger(__name__)


class HyperGraphQLResolver:
    """
    Main resolver class for HyperGraphQL queries.
    Bridges HyperGNN framework with GraphQL interface.
    """

    def __init__(self, schema: Optional[HyperGraphQLSchema] = None):
        """
        Initialize resolver with optional schema.
        If no schema provided, creates a new one.
        """
        self.schema = schema or HyperGraphQLSchema()
        self.hypergnn_frameworks: Dict[str, Any] = {}
        # Evidence refinery integration - will be set by external code
        self.evidence_refinery = None

    def set_hypergnn_framework(self, case_id: str, framework: Any) -> None:
        """Register a HyperGNN framework instance for a case"""
        self.hypergnn_frameworks[case_id] = framework

    def load_from_hypergnn(self, case_id: str) -> None:
        """
        Load entities and relations from HyperGNN framework into GraphQL schema.
        Maps HyperGNN agents, events, and flows to GraphQL nodes and edges.
        """
        if case_id not in self.hypergnn_frameworks:
            logger.warning(f"No HyperGNN framework found for case {case_id}")
            return

        framework = self.hypergnn_frameworks[case_id]

        # Load agents as nodes
        if hasattr(framework, "agents"):
            for agent_id, agent in framework.agents.items():
                node = HyperGraphQLNode(
                    id=agent_id,
                    node_type=EntityTypeQL.AGENT,
                    name=getattr(agent, "name", agent_id),
                    properties={
                        "agent_type": (
                            getattr(agent, "agent_type", None).value
                            if getattr(agent, "agent_type", None)
                            else None
                        ),
                        "attributes": getattr(agent, "attributes", {}),
                    },
                    org_level=OrgLevel.REPO,
                    metadata={"source": "hypergnn", "case_id": case_id},
                )
                self.schema.add_node(node)

        # Load events as nodes
        if hasattr(framework, "events"):
            for event_id, event in framework.events.items():
                node = HyperGraphQLNode(
                    id=event_id,
                    node_type=EntityTypeQL.EVENT,
                    name=getattr(event, "description", event_id),
                    properties={
                        "event_type": (
                            getattr(event, "event_type", None).value
                            if getattr(event, "event_type", None)
                            else None
                        ),
                        "timestamp": (
                            getattr(event, "timestamp", None).isoformat()
                            if getattr(event, "timestamp", None)
                            else None
                        ),
                    },
                    org_level=OrgLevel.REPO,
                    metadata={"source": "hypergnn", "case_id": case_id},
                )
                self.schema.add_node(node)

        # Load flows/relations as edges
        if hasattr(framework, "flows"):
            for flow_id, flow in framework.flows.items():
                edge = HyperGraphQLEdge(
                    id=flow_id,
                    edge_type=RelationTypeQL.RELATED_TO,
                    source_id=getattr(flow, "source", ""),
                    target_ids=[getattr(flow, "target", "")],
                    strength=getattr(flow, "magnitude", 0.5),
                    properties={
                        "flow_type": (
                            getattr(flow, "flow_type", None).value
                            if getattr(flow, "flow_type", None)
                            else None
                        ),
                        "description": getattr(flow, "description", ""),
                    },
                    timestamp=getattr(flow, "timestamp", None),
                    org_level=OrgLevel.REPO,
                    metadata={"source": "hypergnn", "case_id": case_id},
                )
                self.schema.add_edge(edge)

    def load_from_repo_structure(self, repo_path: str, org_name: str) -> None:
        """
        Load entities and relations from GitHub repo folder structure.
        Expects folders like:
        - entities/persons/
        - entities/organizations/
        - relations/ownership/
        - relations/transactions/
        """
        repo_path_obj = Path(repo_path)

        if not repo_path_obj.exists():
            logger.warning(f"Repo path does not exist: {repo_path}")
            return

        # Load entity folders
        entities_path = repo_path_obj / "entities"
        if entities_path.exists():
            self._load_entities_from_folder(entities_path, org_name, repo_path)

        # Load relation folders
        relations_path = repo_path_obj / "relations"
        if relations_path.exists():
            self._load_relations_from_folder(relations_path, org_name, repo_path)

    def _load_entities_from_folder(
        self, entities_path: Path, org_name: str, repo_path: str
    ) -> None:
        """Load entity JSON files from folder structure"""
        for entity_type_folder in entities_path.iterdir():
            if not entity_type_folder.is_dir():
                continue

            entity_type = entity_type_folder.name.upper()
            try:
                entity_type_enum = EntityTypeQL[entity_type.rstrip("S")]
            except KeyError:
                entity_type_enum = EntityTypeQL.AGENT

            for entity_file in entity_type_folder.glob("*.json"):
                try:
                    with open(entity_file, "r") as f:
                        entity_data = json.load(f)

                    node = HyperGraphQLNode(
                        id=entity_data.get("id", entity_file.stem),
                        node_type=entity_type_enum,
                        name=entity_data.get("name", entity_file.stem),
                        properties=entity_data.get("properties", {}),
                        org_level=OrgLevel.REPO,
                        repo_path=repo_path,
                        folder_path=str(entity_file.relative_to(repo_path)),
                        metadata={"source": "repo_structure", "org_name": org_name},
                    )
                    self.schema.add_node(node)
                except Exception as e:
                    logger.error(f"Error loading entity from {entity_file}: {e}")

    def _load_relations_from_folder(
        self, relations_path: Path, org_name: str, repo_path: str
    ) -> None:
        """Load relation JSON files from folder structure"""
        for relation_type_folder in relations_path.iterdir():
            if not relation_type_folder.is_dir():
                continue

            for relation_file in relation_type_folder.glob("*.json"):
                try:
                    with open(relation_file, "r") as f:
                        relation_data = json.load(f)

                    # Determine relation type
                    edge_type_str = relation_data.get("type", "RELATED_TO").upper()
                    try:
                        edge_type = RelationTypeQL[edge_type_str]
                    except KeyError:
                        edge_type = RelationTypeQL.RELATED_TO

                    edge = HyperGraphQLEdge(
                        id=relation_data.get("id", relation_file.stem),
                        edge_type=edge_type,
                        source_id=relation_data.get("source", ""),
                        target_ids=relation_data.get("targets", []),
                        strength=relation_data.get("strength", 0.5),
                        properties=relation_data.get("properties", {}),
                        org_level=OrgLevel.REPO,
                        evidence_refs=relation_data.get("evidence_refs", []),
                        metadata={
                            "source": "repo_structure",
                            "org_name": org_name,
                            "file_path": str(relation_file.relative_to(repo_path)),
                        },
                    )
                    self.schema.add_edge(edge)
                except Exception as e:
                    logger.error(f"Error loading relation from {relation_file}: {e}")

    # Query Resolvers

    def resolve_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Resolve a single node by ID"""
        node = self.schema.get_node(node_id)
        return node.to_graphql_type() if node else None

    def resolve_nodes(
        self, node_type: Optional[str] = None, org_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Resolve multiple nodes with optional filtering"""
        nodes = list(self.schema.nodes.values())

        if node_type:
            try:
                type_enum = EntityTypeQL[node_type.upper()]
                nodes = [n for n in nodes if n.node_type == type_enum]
            except KeyError:
                logger.warning(f"Invalid node type: {node_type}")

        if org_level:
            try:
                level_enum = OrgLevel[org_level.upper()]
                nodes = [n for n in nodes if n.org_level == level_enum]
            except KeyError:
                logger.warning(f"Invalid org level: {org_level}")

        return [n.to_graphql_type() for n in nodes]

    def resolve_edge(self, edge_id: str) -> Optional[Dict[str, Any]]:
        """Resolve a single edge by ID"""
        edge = self.schema.get_edge(edge_id)
        if not edge:
            return None

        result = edge.to_graphql_type()

        # Enhance with source and target node data
        source_node = self.schema.get_node(edge.source_id)
        if source_node:
            result["sourceNode"] = source_node.to_graphql_type()

        target_nodes = []
        for target_id in edge.target_ids:
            target_node = self.schema.get_node(target_id)
            if target_node:
                target_nodes.append(target_node.to_graphql_type())
        result["targetNodes"] = target_nodes

        return result

    def resolve_edges(
        self, edge_type: Optional[str] = None, org_level: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Resolve multiple edges with optional filtering"""
        edges = list(self.schema.edges.values())

        if edge_type:
            try:
                type_enum = RelationTypeQL[edge_type.upper()]
                edges = [e for e in edges if e.edge_type == type_enum]
            except KeyError:
                logger.warning(f"Invalid edge type: {edge_type}")

        if org_level:
            try:
                level_enum = OrgLevel[org_level.upper()]
                edges = [e for e in edges if e.org_level == level_enum]
            except KeyError:
                logger.warning(f"Invalid org level: {org_level}")

        return [e.to_graphql_type() for e in edges]

    def resolve_connected_nodes(self, node_id: str) -> List[Dict[str, Any]]:
        """Resolve all nodes connected to a given node"""
        connected = self.schema.get_connected_nodes(node_id)
        return [n.to_graphql_type() for n in connected]

    def resolve_org_mapping(self, org_name: str) -> Optional[Dict[str, Any]]:
        """Resolve organization mapping configuration"""
        mapping = self.schema.org_mappings.get(org_name)
        return mapping.to_graphql_type() if mapping else None

    def resolve_export_schema(self, org_level: Optional[str] = None) -> Dict[str, Any]:
        """Resolve schema export with optional org level filtering"""
        level_enum = None
        if org_level:
            try:
                level_enum = OrgLevel[org_level.upper()]
            except KeyError:
                logger.warning(f"Invalid org level: {org_level}")

        return self.schema.export_schema(level_enum)

    # Mutation Resolvers

    def resolve_add_node(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new node to the schema"""
        node_type = EntityTypeQL[input_data["nodeType"].upper()]
        org_level = OrgLevel[input_data.get("orgLevel", "REPO").upper()]

        node = HyperGraphQLNode(
            id=input_data.get("id", f"node_{datetime.now().timestamp()}"),
            node_type=node_type,
            name=input_data["name"],
            properties=input_data.get("properties", {}),
            org_level=org_level,
            repo_path=input_data.get("repoPath"),
            folder_path=input_data.get("folderPath"),
            metadata=input_data.get("metadata", {}),
        )

        self.schema.add_node(node)
        return node.to_graphql_type()

    def resolve_update_node(
        self, node_id: str, input_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing node"""
        node = self.schema.get_node(node_id)
        if not node:
            return None

        # Update fields
        if "name" in input_data:
            node.name = input_data["name"]
        if "properties" in input_data:
            node.properties.update(input_data["properties"])
        if "metadata" in input_data:
            node.metadata.update(input_data["metadata"])

        node.updated_at = datetime.now()

        return node.to_graphql_type()

    def resolve_delete_node(self, node_id: str) -> bool:
        """Delete a node from the schema"""
        if node_id in self.schema.nodes:
            del self.schema.nodes[node_id]
            return True
        return False

    def resolve_add_edge(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new edge to the schema"""
        edge_type = RelationTypeQL[input_data["edgeType"].upper()]
        org_level = OrgLevel[input_data.get("orgLevel", "REPO").upper()]

        timestamp = None
        if "timestamp" in input_data and input_data["timestamp"]:
            timestamp = datetime.fromisoformat(input_data["timestamp"])

        edge = HyperGraphQLEdge(
            id=input_data.get("id", f"edge_{datetime.now().timestamp()}"),
            edge_type=edge_type,
            source_id=input_data["sourceId"],
            target_ids=input_data["targetIds"],
            strength=input_data.get("strength", 0.5),
            properties=input_data.get("properties", {}),
            org_level=org_level,
            evidence_refs=input_data.get("evidenceRefs", []),
            timestamp=timestamp,
            metadata=input_data.get("metadata", {}),
        )

        self.schema.add_edge(edge)
        return edge.to_graphql_type()

    def resolve_update_edge(
        self, edge_id: str, input_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an existing edge"""
        edge = self.schema.get_edge(edge_id)
        if not edge:
            return None

        # Update fields
        if "strength" in input_data:
            edge.strength = input_data["strength"]
        if "properties" in input_data:
            edge.properties.update(input_data["properties"])
        if "metadata" in input_data:
            edge.metadata.update(input_data["metadata"])
        if "evidenceRefs" in input_data:
            edge.evidence_refs = input_data["evidenceRefs"]

        return edge.to_graphql_type()

    def resolve_delete_edge(self, edge_id: str) -> bool:
        """Delete an edge from the schema"""
        if edge_id in self.schema.edges:
            del self.schema.edges[edge_id]
            return True
        return False

    def resolve_add_org_mapping(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add organization mapping configuration"""
        org_level = OrgLevel[input_data["orgLevel"].upper()]

        mapping = HyperGraphQLOrgMapping(
            org_name=input_data["orgName"],
            org_level=org_level,
            repos=input_data.get("repos", []),
            entity_folders=input_data.get("entityFolders", []),
            relation_folders=input_data.get("relationFolders", []),
            compression_enabled=input_data.get("compressionEnabled", False),
            aggregation_rules=input_data.get("aggregationRules", {}),
        )

        self.schema.add_org_mapping(mapping)
        return mapping.to_graphql_type()

    # Evidence Refinery Resolvers
    
    def set_evidence_refinery(self, evidence_refinery) -> None:
        """Set the evidence refinery instance for resolver integration"""
        self.evidence_refinery = evidence_refinery
    
    def resolve_add_raw_evidence(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add raw evidence to the refinery"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        try:
            evidence = self.evidence_refinery.add_raw_evidence(
                evidence_id=input_data["evidenceId"],
                content=input_data["content"],
                source=input_data.get("source", "unknown"),
                metadata=input_data.get("metadata")
            )
            return evidence.to_dict()
        except Exception as e:
            logger.error(f"Failed to add raw evidence: {str(e)}")
            return {"error": str(e)}
    
    def resolve_process_evidence(self, evidence_id: str) -> Dict[str, Any]:
        """Process evidence through the refinery pipeline"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        try:
            evidence = self.evidence_refinery.process_evidence(evidence_id)
            return evidence.to_dict()
        except Exception as e:
            logger.error(f"Failed to process evidence {evidence_id}: {str(e)}")
            return {"error": str(e)}
    
    def resolve_refined_evidence(self, evidence_id: str) -> Dict[str, Any]:
        """Get refined evidence by ID"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        if evidence_id not in self.evidence_refinery.refined_evidence:
            return {"error": f"Evidence not found: {evidence_id}"}
        
        evidence = self.evidence_refinery.refined_evidence[evidence_id]
        return evidence.to_dict()
    
    def resolve_evidence_summary(self, evidence_id: str) -> Dict[str, Any]:
        """Get evidence summary"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        return self.evidence_refinery.get_evidence_summary_graphql(evidence_id)
    
    def resolve_related_evidence(self, evidence_id: str, threshold: float = 0.7) -> List[str]:
        """Find related evidence"""
        if not self.evidence_refinery:
            return []
        
        return self.evidence_refinery.find_related_evidence(evidence_id, threshold)
    
    def resolve_create_evidence_relationship(self, input_data: Dict[str, Any]) -> bool:
        """Create relationship between evidence items"""
        if not self.evidence_refinery:
            return False
        
        try:
            return self.evidence_refinery.create_evidence_relationship(
                source_id=input_data["sourceId"],
                target_id=input_data["targetId"],
                relationship_type=input_data.get("relationshipType", "related_to"),
                strength=input_data.get("strength", 0.8)
            )
        except Exception as e:
            logger.error(f"Failed to create evidence relationship: {str(e)}")
            return False
    
    def resolve_update_evidence_quality(self, evidence_id: str, 
                                       quality_score: str, confidence: float) -> Dict[str, Any]:
        """Update evidence quality assessment"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        if evidence_id not in self.evidence_refinery.refined_evidence:
            return {"error": f"Evidence not found: {evidence_id}"}
        
        try:
            from src.api.opencog_hypergraphql_orggml_evidence_refinery import EvidenceQualityScore
            
            evidence = self.evidence_refinery.refined_evidence[evidence_id]
            evidence.quality_score = EvidenceQualityScore(quality_score)
            evidence.confidence = confidence
            evidence.last_updated = datetime.now()
            
            # Update processing log
            evidence.processing_log.append({
                "timestamp": datetime.now().isoformat(),
                "action": "quality_updated",
                "quality_score": quality_score,
                "confidence": confidence
            })
            
            return evidence.to_dict()
        except Exception as e:
            logger.error(f"Failed to update evidence quality: {str(e)}")
            return {"error": str(e)}
    
    def resolve_evidence_quality_report(self, case_id: str) -> Dict[str, Any]:
        """Get evidence quality report for case"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        if self.evidence_refinery.case_id != case_id:
            return {"error": f"Case ID mismatch: {case_id}"}
        
        summary = self.evidence_refinery.get_processing_summary()
        return {
            "caseId": case_id,
            "totalEvidence": summary["total_evidence"],
            "qualityDistribution": summary["quality_distribution"],
            "statusDistribution": summary["status_distribution"],
            "averageConfidence": summary["average_confidence"],
            "totalRelationships": summary["total_relationships"],
            "reportTimestamp": datetime.now().isoformat()
        }
    
    def resolve_processing_status(self, case_id: str) -> Dict[str, Any]:
        """Get processing status report"""
        if not self.evidence_refinery:
            return {"error": "Evidence refinery not configured"}
        
        if self.evidence_refinery.case_id != case_id:
            return {"error": f"Case ID mismatch: {case_id}"}
        
        summary = self.evidence_refinery.get_processing_summary()
        return {
            "caseId": case_id,
            "totalEvidence": summary["total_evidence"],
            "atomSpaceSize": summary["atomspace_size"],
            "hyperGraphQLNodes": summary["hypergraphql_nodes"],
            "hyperGraphQLEdges": summary["hypergraphql_edges"],
            "ggmlPerformance": summary["ggml_performance"],
            "reportTimestamp": datetime.now().isoformat()
        }
    
    def resolve_export_refined_evidence(self, case_id: str, format: str = "json") -> Dict[str, Any]:
        """Export refined evidence"""
        if not self.evidence_refinery:
            return {
                "success": False,
                "message": "Evidence refinery not configured",
                "recordCount": 0
            }
        
        if self.evidence_refinery.case_id != case_id:
            return {
                "success": False,
                "message": f"Case ID mismatch: {case_id}",
                "recordCount": 0
            }
        
        try:
            filepath = self.evidence_refinery.export_refined_evidence(format)
            record_count = len(self.evidence_refinery.refined_evidence)
            
            return {
                "success": True,
                "filepath": filepath,
                "message": f"Exported {record_count} evidence records",
                "recordCount": record_count
            }
        except Exception as e:
            logger.error(f"Failed to export evidence: {str(e)}")
            return {
                "success": False,
                "message": f"Export failed: {str(e)}",
                "recordCount": 0
            }
