#!/usr/bin/env python3
"""
HyperGraphQL GitHub Integration
=================================

Integrates HyperGraphQL with GitHub repository structures.
Provides org-aware repo management features:
- Projects entities & relations to/from repo folder structures
- Supports org-level aggregation across multiple repos
- Enables scaling (compression for storage, expansion for enterprise)
- Maps HyperGNN data to GitHub org/repo hierarchy
"""

import json
import logging
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

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


class GitHubRepoProjection:
    """
    Projects HyperGraphQL entities and relations onto GitHub repo folder structures.
    Creates/manages folder hierarchy for entities and relations.
    """

    def __init__(self, base_path: str):
        """
        Initialize with base path for repo projection.

        Args:
            base_path: Root directory for projected repo structure
        """
        self.base_path = Path(base_path)
        self.entities_path = self.base_path / "entities"
        self.relations_path = self.base_path / "relations"

    def initialize_repo_structure(self) -> None:
        """Create the base folder structure for entities and relations"""
        # Create entity type folders
        for entity_type in EntityTypeQL:
            entity_folder = self.entities_path / entity_type.value.lower()
            entity_folder.mkdir(parents=True, exist_ok=True)

            # Create README for each entity type
            readme_path = entity_folder / "README.md"
            if not readme_path.exists():
                self._create_entity_readme(entity_folder, entity_type)

        # Create relation type folders
        for relation_type in RelationTypeQL:
            relation_folder = self.relations_path / relation_type.value.lower()
            relation_folder.mkdir(parents=True, exist_ok=True)

            # Create README for each relation type
            readme_path = relation_folder / "README.md"
            if not readme_path.exists():
                self._create_relation_readme(relation_folder, relation_type)

        # Create main README
        main_readme = self.base_path / "README.md"
        if not main_readme.exists():
            self._create_main_readme()

        logger.info(f"Initialized repo structure at {self.base_path}")

    def _create_entity_readme(self, folder: Path, entity_type: EntityTypeQL) -> None:
        """Create README for an entity type folder"""
        content = f"""# {entity_type.value.title()} Entities

This folder contains entity data for {entity_type.value} type nodes in the HyperGraphQL structure.

## File Format

Each entity is stored as a JSON file with the following structure:

```json
{{
  "id": "unique_entity_id",
  "name": "Entity Name",
  "properties": {{
    "property1": "value1",
    "property2": "value2"
  }},
  "metadata": {{
    "created_at": "ISO timestamp",
    "updated_at": "ISO timestamp",
    "source": "data source"
  }}
}}
```

## Usage

Entity files are automatically loaded into the HyperGraphQL schema when querying.
They can be created, updated, or deleted via the GraphQL API.
"""
        with open(folder / "README.md", "w") as f:
            f.write(content)

    def _create_relation_readme(
        self, folder: Path, relation_type: RelationTypeQL
    ) -> None:
        """Create README for a relation type folder"""
        content = f"""# {relation_type.value.replace('_', ' ').title()} Relations

This folder contains relation data for {relation_type.value} type edges in the HyperGraphQL structure.

## File Format

Each relation is stored as a JSON file with the following structure:

```json
{{
  "id": "unique_relation_id",
  "type": "{relation_type.value}",
  "source": "source_entity_id",
  "targets": ["target_entity_id1", "target_entity_id2"],
  "strength": 0.8,
  "properties": {{
    "property1": "value1"
  }},
  "evidence_refs": ["evidence1", "evidence2"],
  "timestamp": "ISO timestamp",
  "metadata": {{}}
}}
```

## Usage

Relation files are automatically loaded into the HyperGraphQL schema.
They support hyperedges (multiple targets) for complex relationship modeling.
"""
        with open(folder / "README.md", "w") as f:
            f.write(content)

    def _create_main_readme(self) -> None:
        """Create main README for the repo"""
        content = """# HyperGraphQL Repository

This repository contains HyperGraphQL entity and relation data projected from the HyperGNN framework.

## Structure

```
.
├── entities/           # Entity nodes organized by type
│   ├── person/
│   ├── organization/
│   ├── event/
│   ├── evidence/
│   └── ...
├── relations/          # Relation edges organized by type
│   ├── participates_in/
│   ├── owns/
│   ├── communicates_with/
│   └── ...
└── README.md          # This file
```

## Usage

This repository is managed via the HyperGraphQL API. Entities and relations can be:
- Queried via GraphQL interface
- Loaded into HyperGNN framework for analysis
- Aggregated across multiple repos for org-level views
- Compressed for efficient storage
- Expanded for enterprise-level analysis

## Integration

The repo structure integrates with:
- HyperGNN Framework: Multi-layer network modeling
- GraphQL API: Query and mutation interface
- GitHub Organizations: Multi-repo aggregation
- Enterprise Scaling: Cross-org analysis capabilities
"""
        with open(self.base_path / "README.md", "w") as f:
            f.write(content)

    def project_node(self, node: HyperGraphQLNode) -> Path:
        """
        Project a node to the repo folder structure.
        Creates/updates the corresponding JSON file.

        Returns:
            Path to the created/updated file
        """
        folder = self.entities_path / node.node_type.value.lower()
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{node.id}.json"

        data = {
            "id": node.id,
            "name": node.name,
            "properties": node.properties,
            "metadata": {
                **node.metadata,
                "created_at": node.created_at.isoformat(),
                "updated_at": node.updated_at.isoformat(),
                "org_level": node.org_level.value,
            },
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        logger.debug(f"Projected node {node.id} to {file_path}")
        return file_path

    def project_edge(self, edge: HyperGraphQLEdge) -> Path:
        """
        Project an edge to the repo folder structure.
        Creates/updates the corresponding JSON file.

        Returns:
            Path to the created/updated file
        """
        folder = self.relations_path / edge.edge_type.value.lower()
        folder.mkdir(parents=True, exist_ok=True)

        file_path = folder / f"{edge.id}.json"

        data = {
            "id": edge.id,
            "type": edge.edge_type.value,
            "source": edge.source_id,
            "targets": edge.target_ids,
            "strength": edge.strength,
            "properties": edge.properties,
            "evidence_refs": edge.evidence_refs,
            "timestamp": edge.timestamp.isoformat() if edge.timestamp else None,
            "metadata": {**edge.metadata, "org_level": edge.org_level.value},
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        logger.debug(f"Projected edge {edge.id} to {file_path}")
        return file_path

    def project_schema(self, schema: HyperGraphQLSchema) -> None:
        """Project entire schema to repo structure"""
        self.initialize_repo_structure()

        # Project all nodes
        for node in schema.nodes.values():
            self.project_node(node)

        # Project all edges
        for edge in schema.edges.values():
            self.project_edge(edge)

        logger.info(
            f"Projected {len(schema.nodes)} nodes and {len(schema.edges)} edges"
        )

    def get_repo_stats(self) -> Dict[str, Any]:
        """Get statistics about the projected repo structure"""
        stats = {
            "entity_counts": {},
            "relation_counts": {},
            "total_entities": 0,
            "total_relations": 0,
            "last_updated": datetime.now().isoformat(),
        }

        # Count entities
        if self.entities_path.exists():
            for entity_type_folder in self.entities_path.iterdir():
                if entity_type_folder.is_dir():
                    count = len(list(entity_type_folder.glob("*.json")))
                    stats["entity_counts"][entity_type_folder.name] = count
                    stats["total_entities"] += count

        # Count relations
        if self.relations_path.exists():
            for relation_type_folder in self.relations_path.iterdir():
                if relation_type_folder.is_dir():
                    count = len(list(relation_type_folder.glob("*.json")))
                    stats["relation_counts"][relation_type_folder.name] = count
                    stats["total_relations"] += count

        return stats


class OrgAwareManager:
    """
    Manages org-aware operations across multiple repos.
    Handles aggregation, scaling, and compression.
    """

    def __init__(self, org_name: str, org_level: OrgLevel = OrgLevel.ORG):
        """
        Initialize org-aware manager.

        Args:
            org_name: Name of the GitHub organization
            org_level: Level of organization (REPO, ORG, ENTERPRISE)
        """
        self.org_name = org_name
        self.org_level = org_level
        self.repos: Dict[str, GitHubRepoProjection] = {}

    def register_repo(self, repo_name: str, repo_path: str) -> None:
        """Register a repository for org-level management"""
        projection = GitHubRepoProjection(repo_path)
        self.repos[repo_name] = projection
        logger.info(f"Registered repo {repo_name} at {repo_path}")

    def aggregate_schemas(self) -> HyperGraphQLSchema:
        """
        Aggregate schemas from all registered repos into a single org-level schema.
        Useful for cross-repo analysis and enterprise views.
        """
        aggregated_schema = HyperGraphQLSchema()

        for repo_name, projection in self.repos.items():
            # Load entities from repo
            if projection.entities_path.exists():
                for entity_type_folder in projection.entities_path.iterdir():
                    if not entity_type_folder.is_dir():
                        continue

                    for entity_file in entity_type_folder.glob("*.json"):
                        try:
                            with open(entity_file, "r") as f:
                                data = json.load(f)

                            # Determine entity type
                            entity_type = EntityTypeQL[
                                entity_type_folder.name.upper().rstrip("S")
                            ]

                            node = HyperGraphQLNode(
                                id=f"{repo_name}:{data['id']}",  # Prefix with repo name
                                node_type=entity_type,
                                name=data["name"],
                                properties=data.get("properties", {}),
                                org_level=self.org_level,
                                repo_path=str(projection.base_path),
                                folder_path=str(
                                    entity_file.relative_to(projection.base_path)
                                ),
                                metadata={
                                    **data.get("metadata", {}),
                                    "source_repo": repo_name,
                                    "org_name": self.org_name,
                                },
                            )
                            aggregated_schema.add_node(node)
                        except Exception as e:
                            logger.error(
                                f"Error loading entity from {entity_file}: {e}"
                            )

            # Load relations from repo
            if projection.relations_path.exists():
                for relation_type_folder in projection.relations_path.iterdir():
                    if not relation_type_folder.is_dir():
                        continue

                    for relation_file in relation_type_folder.glob("*.json"):
                        try:
                            with open(relation_file, "r") as f:
                                data = json.load(f)

                            # Determine relation type
                            try:
                                relation_type = RelationTypeQL[data["type"].upper()]
                            except KeyError:
                                relation_type = RelationTypeQL.RELATED_TO

                            # Prefix IDs with repo name
                            source_id = f"{repo_name}:{data['source']}"
                            target_ids = [
                                f"{repo_name}:{t}" for t in data.get("targets", [])
                            ]

                            edge = HyperGraphQLEdge(
                                id=f"{repo_name}:{data['id']}",
                                edge_type=relation_type,
                                source_id=source_id,
                                target_ids=target_ids,
                                strength=data.get("strength", 0.5),
                                properties=data.get("properties", {}),
                                org_level=self.org_level,
                                evidence_refs=data.get("evidence_refs", []),
                                timestamp=(
                                    datetime.fromisoformat(data["timestamp"])
                                    if data.get("timestamp")
                                    else None
                                ),
                                metadata={
                                    **data.get("metadata", {}),
                                    "source_repo": repo_name,
                                    "org_name": self.org_name,
                                },
                            )
                            aggregated_schema.add_edge(edge)
                        except Exception as e:
                            logger.error(
                                f"Error loading relation from {relation_file}: {e}"
                            )

        logger.info(
            f"Aggregated {len(aggregated_schema.nodes)} nodes and "
            f"{len(aggregated_schema.edges)} edges from {len(self.repos)} repos"
        )
        return aggregated_schema

    def compress_repo(self, repo_name: str, output_path: str) -> Path:
        """
        Compress a repo's entity/relation structure for storage.
        Useful for archiving or reducing storage footprint.

        Returns:
            Path to the compressed archive
        """
        if repo_name not in self.repos:
            raise ValueError(f"Repo {repo_name} not registered")

        projection = self.repos[repo_name]
        output_file = Path(output_path) / f"{repo_name}_compressed.zip"

        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add all entity files
            if projection.entities_path.exists():
                for file_path in projection.entities_path.rglob("*.json"):
                    arcname = file_path.relative_to(projection.base_path)
                    zipf.write(file_path, arcname)

            # Add all relation files
            if projection.relations_path.exists():
                for file_path in projection.relations_path.rglob("*.json"):
                    arcname = file_path.relative_to(projection.base_path)
                    zipf.write(file_path, arcname)

            # Add README files
            for readme in projection.base_path.rglob("README.md"):
                arcname = readme.relative_to(projection.base_path)
                zipf.write(readme, arcname)

        logger.info(f"Compressed repo {repo_name} to {output_file}")
        return output_file

    def decompress_repo(self, archive_path: str, extract_to: str) -> None:
        """
        Decompress a repo archive.
        Useful for restoring archived data or expanding for analysis.
        """
        archive = Path(archive_path)
        extract_path = Path(extract_to)

        with zipfile.ZipFile(archive, "r") as zipf:
            zipf.extractall(extract_path)

        logger.info(f"Decompressed archive to {extract_path}")

    def get_org_stats(self) -> Dict[str, Any]:
        """Get aggregate statistics across all repos in the org"""
        stats = {
            "org_name": self.org_name,
            "org_level": self.org_level.value,
            "repo_count": len(self.repos),
            "total_entities": 0,
            "total_relations": 0,
            "repos": {},
        }

        for repo_name, projection in self.repos.items():
            repo_stats = projection.get_repo_stats()
            stats["repos"][repo_name] = repo_stats
            stats["total_entities"] += repo_stats["total_entities"]
            stats["total_relations"] += repo_stats["total_relations"]

        return stats

    def scale_up_to_enterprise(
        self, other_orgs: List["OrgAwareManager"]
    ) -> HyperGraphQLSchema:
        """
        Scale up to enterprise level by aggregating multiple orgs.
        Creates a unified enterprise-level schema.
        """
        enterprise_schema = HyperGraphQLSchema()

        # Add this org's data
        org_schema = self.aggregate_schemas()
        for node in org_schema.nodes.values():
            node.org_level = OrgLevel.ENTERPRISE
            enterprise_schema.add_node(node)
        for edge in org_schema.edges.values():
            edge.org_level = OrgLevel.ENTERPRISE
            enterprise_schema.add_edge(edge)

        # Add other orgs' data
        for other_org in other_orgs:
            other_schema = other_org.aggregate_schemas()
            for node in other_schema.nodes.values():
                node.org_level = OrgLevel.ENTERPRISE
                node.id = f"{other_org.org_name}:{node.id}"  # Prefix with org name
                enterprise_schema.add_node(node)
            for edge in other_schema.edges.values():
                edge.org_level = OrgLevel.ENTERPRISE
                edge.id = f"{other_org.org_name}:{edge.id}"
                edge.source_id = f"{other_org.org_name}:{edge.source_id}"
                edge.target_ids = [f"{other_org.org_name}:{t}" for t in edge.target_ids]
                enterprise_schema.add_edge(edge)

        logger.info(f"Scaled up to enterprise level with {len(other_orgs) + 1} orgs")
        return enterprise_schema
