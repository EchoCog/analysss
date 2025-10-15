#!/usr/bin/env python3
"""
AD Hypergraph Repository Mapper
===============================

Maps the AD (Affidavit/Analysis Document) hypergraph across multiple GitHub repositories
to enable comprehensive cross-repository analysis and evidence correlation.

Supports the following target repositories:
- cogpy/ad-res-j7 (Primary evidence source)
- EchoCog/analysss (Comprehensive analysis hub) 
- rzonedevops/analysis
- rzonedevops/avtomaatoctory
- rzonedevops/analyticase
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from urllib.parse import urlparse

from .hypergraphql_github import GitHubRepoProjection, OrgAwareManager
from .hypergraphql_schema import (
    EntityTypeQL,
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLOrgMapping,
    HyperGraphQLSchema,
    OrgLevel,
    RelationTypeQL,
)

logger = logging.getLogger(__name__)


class RepositoryConfig:
    """Configuration for a target repository in the AD hypergraph mapping."""
    
    def __init__(
        self,
        url: str,
        name: str,
        org_name: str,
        evidence_level: str,
        entity_folders: Optional[List[str]] = None,
        relation_folders: Optional[List[str]] = None,
        evidence_folders: Optional[List[str]] = None,
        local_path: Optional[str] = None,
    ):
        self.url = url
        self.name = name
        self.org_name = org_name
        self.evidence_level = evidence_level  # "primary", "comprehensive", "limited", "none"
        self.entity_folders = entity_folders or []
        self.relation_folders = relation_folders or []
        self.evidence_folders = evidence_folders or []
        self.local_path = local_path
        
        # Parse URL to extract owner and repo name
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            self.github_owner = path_parts[0]
            self.github_repo = path_parts[1]
        else:
            self.github_owner = org_name
            self.github_repo = name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "url": self.url,
            "name": self.name,
            "org_name": self.org_name,
            "evidence_level": self.evidence_level,
            "entity_folders": self.entity_folders,
            "relation_folders": self.relation_folders,
            "evidence_folders": self.evidence_folders,
            "local_path": self.local_path,
            "github_owner": self.github_owner,
            "github_repo": self.github_repo,
        }


class ADHypergraphRepositoryMapper:
    """
    Maps AD hypergraph across multiple GitHub repositories.
    
    Provides cross-repository entity linking, evidence correlation,
    and unified hypergraph views across all target repositories.
    """

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the AD hypergraph repository mapper.
        
        Args:
            base_path: Base directory for repository operations
        """
        self.base_path = Path(base_path or "/home/runner/work/analysss/analysss")
        self.repositories: Dict[str, RepositoryConfig] = {}
        self.schema = HyperGraphQLSchema()
        self.org_managers: Dict[str, OrgAwareManager] = {}
        
        # Initialize with known target repositories
        self._initialize_target_repositories()

    def _initialize_target_repositories(self) -> None:
        """Initialize the known target repositories for AD hypergraph mapping."""
        
        # Primary evidence source
        self.add_repository(RepositoryConfig(
            url="https://github.com/cogpy/ad-res-j7",
            name="ad-res-j7",
            org_name="cogpy",
            evidence_level="primary",
            evidence_folders=[
                "evidence/bank_records",
                "evidence/director_loan_accounts",
                "evidence/correspondence",
                "evidence/invoices",
                "evidence/shopify_reports",
                "jax-response",
                "case_2025_137857"
            ],
            entity_folders=["entities", "jax-response/AD", "analysis-output"],
            relation_folders=["relations", "financial-flows"]
        ))
        
        # Comprehensive analysis hub (current repository)
        self.add_repository(RepositoryConfig(
            url="https://github.com/EchoCog/analysss",
            name="analysss",
            org_name="EchoCog",
            evidence_level="comprehensive",
            evidence_folders=[
                "jax-response",
                "murder-theft",
                "case_2025_137857",
                "evidence"
            ],
            entity_folders=["entities", "jax-response", "murder-theft/entities"],
            relation_folders=["relations", "jax-response/financial-flows"],
            local_path=str(self.base_path)
        ))
        
        # Analysis repository (limited)
        self.add_repository(RepositoryConfig(
            url="https://github.com/rzonedevops/analysis",
            name="analysis",
            org_name="rzonedevops",
            evidence_level="limited",
            entity_folders=["workflows", "analysis"],
            relation_folders=["dependencies"]
        ))
        
        # Automation factory repository 
        self.add_repository(RepositoryConfig(
            url="https://github.com/rzonedevops/avtomaatoctory",
            name="avtomaatoctory", 
            org_name="rzonedevops",
            evidence_level="none",
            entity_folders=["automation"],
            relation_folders=["processes"]
        ))
        
        # Legal case management repository
        self.add_repository(RepositoryConfig(
            url="https://github.com/rzonedevops/analyticase",
            name="analyticase",
            org_name="rzonedevops", 
            evidence_level="limited",
            evidence_folders=["legal", "case_management"],
            entity_folders=["legal/entities"],
            relation_folders=["legal/relations"]
        ))

    def add_repository(self, repo_config: RepositoryConfig) -> None:
        """Add a repository to the AD hypergraph mapping."""
        self.repositories[repo_config.name] = repo_config
        
        # Create or get org manager for this repository's organization
        if repo_config.org_name not in self.org_managers:
            self.org_managers[repo_config.org_name] = OrgAwareManager(
                org_name=repo_config.org_name,
                org_level=OrgLevel.ORG
            )
        
        logger.info(f"Added repository {repo_config.name} to AD hypergraph mapping")

    def create_org_mapping(self, repo_name: str) -> HyperGraphQLOrgMapping:
        """Create a HyperGraphQL organization mapping for a repository."""
        if repo_name not in self.repositories:
            raise ValueError(f"Repository {repo_name} not found")
        
        repo_config = self.repositories[repo_name]
        
        mapping = HyperGraphQLOrgMapping(
            org_name=repo_config.org_name,
            org_level=OrgLevel.ORG,
            repos=[repo_config.url],
            entity_folders=repo_config.entity_folders,
            relation_folders=repo_config.relation_folders,
            compression_enabled=False,
            aggregation_rules={
                "evidence_level": repo_config.evidence_level,
                "cross_repo_linking": True,
                "entity_prefixing": True
            }
        )
        
        self.schema.add_org_mapping(mapping)
        return mapping

    def scan_local_repository(self, repo_name: str) -> Dict[str, Any]:
        """
        Scan a local repository for entities, relations, and evidence.
        
        Returns:
            Dictionary containing scan results
        """
        if repo_name not in self.repositories:
            raise ValueError(f"Repository {repo_name} not found")
        
        repo_config = self.repositories[repo_name]
        if not repo_config.local_path:
            raise ValueError(f"No local path configured for repository {repo_name}")
        
        repo_path = Path(repo_config.local_path)
        if not repo_path.exists():
            raise FileNotFoundError(f"Local repository path does not exist: {repo_path}")
        
        scan_results = {
            "repository": repo_name,
            "path": str(repo_path),
            "entities": {},
            "relations": {},
            "evidence_files": [],
            "entity_count": 0,
            "relation_count": 0,
            "evidence_count": 0,
            "scan_timestamp": datetime.now().isoformat()
        }
        
        # Scan entity folders
        for entity_folder in repo_config.entity_folders:
            entity_path = repo_path / entity_folder
            if entity_path.exists():
                entity_files = self._scan_entity_folder(entity_path)
                scan_results["entities"][entity_folder] = entity_files
                scan_results["entity_count"] += len(entity_files)
        
        # Scan relation folders
        for relation_folder in repo_config.relation_folders:
            relation_path = repo_path / relation_folder
            if relation_path.exists():
                relation_files = self._scan_relation_folder(relation_path)
                scan_results["relations"][relation_folder] = relation_files
                scan_results["relation_count"] += len(relation_files)
        
        # Scan evidence folders
        for evidence_folder in repo_config.evidence_folders:
            evidence_path = repo_path / evidence_folder
            if evidence_path.exists():
                evidence_files = self._scan_evidence_folder(evidence_path)
                scan_results["evidence_files"].extend(evidence_files)
                scan_results["evidence_count"] += len(evidence_files)
        
        return scan_results

    def _scan_entity_folder(self, folder_path: Path) -> List[Dict[str, Any]]:
        """Scan a folder for entity files."""
        entities = []
        
        # Look for JSON files
        for json_file in folder_path.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                entities.append({
                    "file": str(json_file.relative_to(folder_path.parent)),
                    "id": data.get("id", json_file.stem),
                    "type": self._determine_entity_type(json_file, data),
                    "size": json_file.stat().st_size
                })
            except Exception as e:
                logger.warning(f"Error reading entity file {json_file}: {e}")
        
        # Look for Markdown files that might contain entity data
        for md_file in folder_path.rglob("*.md"):
            entities.append({
                "file": str(md_file.relative_to(folder_path.parent)),
                "id": md_file.stem,
                "type": "document",
                "size": md_file.stat().st_size
            })
        
        return entities

    def _scan_relation_folder(self, folder_path: Path) -> List[Dict[str, Any]]:
        """Scan a folder for relation files."""
        relations = []
        
        for json_file in folder_path.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                relations.append({
                    "file": str(json_file.relative_to(folder_path.parent)),
                    "id": data.get("id", json_file.stem),
                    "type": data.get("type", "related_to"),
                    "source": data.get("source"),
                    "targets": data.get("targets", []),
                    "size": json_file.stat().st_size
                })
            except Exception as e:
                logger.warning(f"Error reading relation file {json_file}: {e}")
        
        return relations

    def _scan_evidence_folder(self, folder_path: Path) -> List[Dict[str, Any]]:
        """Scan a folder for evidence files."""
        evidence_files = []
        
        # Common evidence file extensions
        evidence_extensions = {'.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.csv', 
                             '.xlsx', '.json', '.md', '.txt', '.eml', '.msg'}
        
        for file_path in folder_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in evidence_extensions:
                evidence_files.append({
                    "file": str(file_path.relative_to(folder_path.parent)),
                    "name": file_path.name,
                    "type": file_path.suffix.lower(),
                    "size": file_path.stat().st_size,
                    "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
        
        return evidence_files

    def _determine_entity_type(self, file_path: Path, data: Dict[str, Any]) -> str:
        """Determine entity type from file path and data."""
        # Check if type is explicitly specified in data
        if "type" in data:
            return data["type"]
        
        # Infer from file path
        path_parts = file_path.parts
        for part in path_parts:
            part_lower = part.lower()
            if "person" in part_lower or "people" in part_lower:
                return "person"
            elif "organization" in part_lower or "company" in part_lower:
                return "organization"
            elif "event" in part_lower:
                return "event"
            elif "evidence" in part_lower:
                return "evidence"
            elif "transaction" in part_lower:
                return "transaction"
            elif "document" in part_lower:
                return "document"
        
        return "agent"  # Default fallback

    def load_repository_into_schema(self, repo_name: str) -> int:
        """
        Load a repository's entities and relations into the unified schema.
        
        Returns:
            Number of items loaded (entities + relations)
        """
        if repo_name not in self.repositories:
            raise ValueError(f"Repository {repo_name} not found")
        
        repo_config = self.repositories[repo_name]
        if not repo_config.local_path:
            logger.warning(f"No local path for repository {repo_name}, skipping load")
            return 0
        
        repo_path = Path(repo_config.local_path)
        items_loaded = 0
        
        # Load entities
        for entity_folder in repo_config.entity_folders:
            entity_path = repo_path / entity_folder
            if entity_path.exists():
                items_loaded += self._load_entities_from_path(
                    entity_path, repo_name, repo_config
                )
        
        # Load relations
        for relation_folder in repo_config.relation_folders:
            relation_path = repo_path / relation_folder
            if relation_path.exists():
                items_loaded += self._load_relations_from_path(
                    relation_path, repo_name, repo_config
                )
        
        logger.info(f"Loaded {items_loaded} items from repository {repo_name}")
        return items_loaded

    def _load_entities_from_path(
        self, path: Path, repo_name: str, repo_config: RepositoryConfig
    ) -> int:
        """Load entities from a specific path."""
        entities_loaded = 0
        
        for json_file in path.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                entity_type_str = self._determine_entity_type(json_file, data)
                try:
                    entity_type = EntityTypeQL[entity_type_str.upper()]
                except KeyError:
                    entity_type = EntityTypeQL.AGENT
                
                node = HyperGraphQLNode(
                    id=f"{repo_name}:{data.get('id', json_file.stem)}",
                    node_type=entity_type,
                    name=data.get("name", json_file.stem),
                    properties=data.get("properties", {}),
                    org_level=OrgLevel.ORG,
                    repo_path=repo_config.local_path,
                    folder_path=str(json_file.relative_to(path)),
                    metadata={
                        **data.get("metadata", {}),
                        "source_repo": repo_name,
                        "source_org": repo_config.org_name,
                        "evidence_level": repo_config.evidence_level,
                        "ad_hypergraph_mapping": True
                    }
                )
                
                self.schema.add_node(node)
                entities_loaded += 1
                
            except Exception as e:
                logger.error(f"Error loading entity from {json_file}: {e}")
        
        return entities_loaded

    def _load_relations_from_path(
        self, path: Path, repo_name: str, repo_config: RepositoryConfig
    ) -> int:
        """Load relations from a specific path."""
        relations_loaded = 0
        
        for json_file in path.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                relation_type_str = data.get("type", "related_to")
                try:
                    relation_type = RelationTypeQL[relation_type_str.upper()]
                except KeyError:
                    relation_type = RelationTypeQL.RELATED_TO
                
                # Prefix source and target IDs with repository name
                source_id = data.get("source")
                if source_id and not source_id.startswith(f"{repo_name}:"):
                    source_id = f"{repo_name}:{source_id}"
                
                target_ids = data.get("targets", [])
                prefixed_targets = []
                for target_id in target_ids:
                    if not target_id.startswith(f"{repo_name}:"):
                        prefixed_targets.append(f"{repo_name}:{target_id}")
                    else:
                        prefixed_targets.append(target_id)
                
                edge = HyperGraphQLEdge(
                    id=f"{repo_name}:{data.get('id', json_file.stem)}",
                    edge_type=relation_type,
                    source_id=source_id,
                    target_ids=prefixed_targets,
                    strength=data.get("strength", 0.5),
                    properties=data.get("properties", {}),
                    org_level=OrgLevel.ORG,
                    evidence_refs=data.get("evidence_refs", []),
                    timestamp=(
                        datetime.fromisoformat(data["timestamp"])
                        if data.get("timestamp")
                        else None
                    ),
                    metadata={
                        **data.get("metadata", {}),
                        "source_repo": repo_name,
                        "source_org": repo_config.org_name,
                        "evidence_level": repo_config.evidence_level,
                        "ad_hypergraph_mapping": True
                    }
                )
                
                self.schema.add_edge(edge)
                relations_loaded += 1
                
            except Exception as e:
                logger.error(f"Error loading relation from {json_file}: {e}")
        
        return relations_loaded

    def generate_cross_repository_links(self) -> List[HyperGraphQLEdge]:
        """
        Generate cross-repository links based on entity similarity and evidence correlation.
        
        Returns:
            List of cross-repository edges created
        """
        cross_links = []
        
        # Group nodes by repository
        repo_nodes = {}
        for node in self.schema.nodes.values():
            repo_prefix = node.id.split(':')[0] if ':' in node.id else 'unknown'
            if repo_prefix not in repo_nodes:
                repo_nodes[repo_prefix] = []
            repo_nodes[repo_prefix].append(node)
        
        # Find potential cross-repository links
        for repo1, nodes1 in repo_nodes.items():
            for repo2, nodes2 in repo_nodes.items():
                if repo1 >= repo2:  # Avoid duplicate comparisons
                    continue
                
                for node1 in nodes1:
                    for node2 in nodes2:
                        if self._should_link_cross_repository(node1, node2):
                            cross_link = self._create_cross_repository_link(node1, node2)
                            if cross_link:
                                self.schema.add_edge(cross_link)
                                cross_links.append(cross_link)
        
        logger.info(f"Generated {len(cross_links)} cross-repository links")
        return cross_links

    def _should_link_cross_repository(
        self, node1: HyperGraphQLNode, node2: HyperGraphQLNode
    ) -> bool:
        """Determine if two nodes from different repositories should be linked."""
        
        # Same entity type
        if node1.node_type != node2.node_type:
            return False
        
        # Similar names
        name1 = node1.name.lower()
        name2 = node2.name.lower()
        
        # Simple similarity checks
        if name1 == name2:
            return True
        
        # Check for common keywords in properties
        props1 = set(str(v).lower() for v in node1.properties.values())
        props2 = set(str(v).lower() for v in node2.properties.values())
        
        common_props = props1.intersection(props2)
        if len(common_props) > 0:
            return True
        
        return False

    def _create_cross_repository_link(
        self, node1: HyperGraphQLNode, node2: HyperGraphQLNode
    ) -> Optional[HyperGraphQLEdge]:
        """Create a cross-repository link between two nodes."""
        
        link_id = f"cross_link:{node1.id}:{node2.id}"
        
        # Determine link strength based on similarity
        strength = 0.3  # Base strength for cross-repository links
        if node1.name.lower() == node2.name.lower():
            strength = 0.8
        
        return HyperGraphQLEdge(
            id=link_id,
            edge_type=RelationTypeQL.RELATED_TO,
            source_id=node1.id,
            target_ids=[node2.id],
            strength=strength,
            properties={
                "link_type": "cross_repository",
                "similarity_basis": "name_and_properties"
            },
            org_level=OrgLevel.ENTERPRISE,
            metadata={
                "created_by": "ad_hypergraph_mapper",
                "link_timestamp": datetime.now().isoformat(),
                "source_repos": [
                    node1.metadata.get("source_repo"),
                    node2.metadata.get("source_repo")
                ]
            }
        )

    def export_unified_hypergraph(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Export the unified AD hypergraph across all repositories.
        
        Returns:
            Dictionary containing the unified hypergraph data
        """
        export_data = self.schema.export_schema(org_level=None)
        
        # Add AD hypergraph specific metadata
        export_data["metadata"]["ad_hypergraph"] = {
            "repositories": [repo.to_dict() for repo in self.repositories.values()],
            "cross_repository_links": len([
                e for e in self.schema.edges.values() 
                if e.properties.get("link_type") == "cross_repository"
            ]),
            "evidence_levels": {
                repo.name: repo.evidence_level 
                for repo in self.repositories.values()
            },
            "export_timestamp": datetime.now().isoformat()
        }
        
        if output_path:
            output_file = Path(output_path)
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            logger.info(f"Exported unified AD hypergraph to {output_file}")
        
        return export_data

    def get_repository_summary(self) -> Dict[str, Any]:
        """Get a summary of all repositories in the AD hypergraph mapping."""
        summary = {
            "total_repositories": len(self.repositories),
            "repositories": {},
            "evidence_distribution": {},
            "organization_distribution": {},
            "total_entities": len(self.schema.nodes),
            "total_relations": len(self.schema.edges),
            "summary_timestamp": datetime.now().isoformat()
        }
        
        # Analyze evidence levels
        for repo in self.repositories.values():
            if repo.evidence_level not in summary["evidence_distribution"]:
                summary["evidence_distribution"][repo.evidence_level] = 0
            summary["evidence_distribution"][repo.evidence_level] += 1
            
            if repo.org_name not in summary["organization_distribution"]:
                summary["organization_distribution"][repo.org_name] = 0
            summary["organization_distribution"][repo.org_name] += 1
            
            summary["repositories"][repo.name] = {
                "url": repo.url,
                "org": repo.org_name,
                "evidence_level": repo.evidence_level,
                "local_available": repo.local_path is not None,
                "entity_folders": len(repo.entity_folders),
                "relation_folders": len(repo.relation_folders),
                "evidence_folders": len(repo.evidence_folders)
            }
        
        return summary