#!/usr/bin/env python3
"""
Integration tests for HyperGraphQL system
==========================================
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.api.hypergraphql_github import GitHubRepoProjection, OrgAwareManager
from src.api.hypergraphql_resolvers import HyperGraphQLResolver
from src.api.hypergraphql_schema import (
    EntityTypeQL,
    HyperGraphQLEdge,
    HyperGraphQLNode,
    HyperGraphQLOrgMapping,
    HyperGraphQLSchema,
    OrgLevel,
    RelationTypeQL,
)


class TestGitHubRepoProjection:
    """Test GitHub repository projection functionality"""
    
    @pytest.fixture
    def temp_repo(self):
        """Create a temporary repo directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
            
    def test_initialize_repo_structure(self, temp_repo):
        """Test initializing repo structure"""
        projection = GitHubRepoProjection(str(temp_repo))
        projection.initialize_repo_structure()
        
        # Check entities folder structure
        entities_path = temp_repo / "entities"
        assert entities_path.exists()
        assert (entities_path / "person").exists()
        assert (entities_path / "organization").exists()
        assert (entities_path / "event").exists()
        
        # Check relations folder structure
        relations_path = temp_repo / "relations"
        assert relations_path.exists()
        assert (relations_path / "owns").exists()
        assert (relations_path / "participates_in").exists()
        
        # Check README files
        assert (temp_repo / "README.md").exists()
        assert (entities_path / "person" / "README.md").exists()
        
    def test_project_node(self, temp_repo):
        """Test projecting a node to repo"""
        projection = GitHubRepoProjection(str(temp_repo))
        projection.initialize_repo_structure()
        
        node = HyperGraphQLNode(
            id="person_test_1",
            node_type=EntityTypeQL.PERSON,
            name="Test Person",
            properties={"age": 30, "role": "analyst"},
            org_level=OrgLevel.REPO
        )
        
        file_path = projection.project_node(node)
        
        assert file_path.exists()
        assert file_path.name == "person_test_1.json"
        
        # Verify file content
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        assert data["id"] == "person_test_1"
        assert data["name"] == "Test Person"
        assert data["properties"]["age"] == 30
        
    def test_project_edge(self, temp_repo):
        """Test projecting an edge to repo"""
        projection = GitHubRepoProjection(str(temp_repo))
        projection.initialize_repo_structure()
        
        edge = HyperGraphQLEdge(
            id="edge_test_1",
            edge_type=RelationTypeQL.OWNS,
            source_id="person_1",
            target_ids=["org_1"],
            strength=0.9,
            evidence_refs=["evidence_1"]
        )
        
        file_path = projection.project_edge(edge)
        
        assert file_path.exists()
        assert file_path.name == "edge_test_1.json"
        
        # Verify file content
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        assert data["id"] == "edge_test_1"
        assert data["type"] == "owns"
        assert data["source"] == "person_1"
        assert data["targets"] == ["org_1"]
        assert data["strength"] == 0.9
        
    def test_project_schema(self, temp_repo):
        """Test projecting entire schema to repo"""
        projection = GitHubRepoProjection(str(temp_repo))
        schema = HyperGraphQLSchema()
        
        # Add nodes
        schema.add_node(HyperGraphQLNode(
            id="node_1",
            node_type=EntityTypeQL.PERSON,
            name="Person 1",
            org_level=OrgLevel.REPO
        ))
        schema.add_node(HyperGraphQLNode(
            id="node_2",
            node_type=EntityTypeQL.ORGANIZATION,
            name="Org 1",
            org_level=OrgLevel.REPO
        ))
        
        # Add edge
        schema.add_edge(HyperGraphQLEdge(
            id="edge_1",
            edge_type=RelationTypeQL.MEMBER_OF,
            source_id="node_1",
            target_ids=["node_2"]
        ))
        
        projection.project_schema(schema)
        
        # Verify files exist
        assert (temp_repo / "entities" / "person" / "node_1.json").exists()
        assert (temp_repo / "entities" / "organization" / "node_2.json").exists()
        assert (temp_repo / "relations" / "member_of" / "edge_1.json").exists()
        
    def test_get_repo_stats(self, temp_repo):
        """Test getting repo statistics"""
        projection = GitHubRepoProjection(str(temp_repo))
        schema = HyperGraphQLSchema()
        
        # Add test data
        for i in range(3):
            schema.add_node(HyperGraphQLNode(
                id=f"person_{i}",
                node_type=EntityTypeQL.PERSON,
                name=f"Person {i}",
                org_level=OrgLevel.REPO
            ))
            
        projection.project_schema(schema)
        stats = projection.get_repo_stats()
        
        assert stats["total_entities"] == 3
        assert stats["entity_counts"]["person"] == 3


class TestOrgAwareManager:
    """Test organization-aware management functionality"""
    
    @pytest.fixture
    def temp_repos(self):
        """Create temporary repo directories"""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            repo1 = base / "repo1"
            repo2 = base / "repo2"
            repo1.mkdir()
            repo2.mkdir()
            yield {"base": base, "repo1": repo1, "repo2": repo2}
            
    def test_register_repo(self, temp_repos):
        """Test registering repos to org manager"""
        manager = OrgAwareManager("test-org", OrgLevel.ORG)
        
        manager.register_repo("repo1", str(temp_repos["repo1"]))
        manager.register_repo("repo2", str(temp_repos["repo2"]))
        
        assert len(manager.repos) == 2
        assert "repo1" in manager.repos
        assert "repo2" in manager.repos
        
    def test_aggregate_schemas(self, temp_repos):
        """Test aggregating schemas from multiple repos"""
        manager = OrgAwareManager("test-org", OrgLevel.ORG)
        
        # Setup repo1
        projection1 = GitHubRepoProjection(str(temp_repos["repo1"]))
        schema1 = HyperGraphQLSchema()
        schema1.add_node(HyperGraphQLNode(
            id="person_1",
            node_type=EntityTypeQL.PERSON,
            name="Person 1",
            org_level=OrgLevel.REPO
        ))
        projection1.project_schema(schema1)
        manager.register_repo("repo1", str(temp_repos["repo1"]))
        
        # Setup repo2
        projection2 = GitHubRepoProjection(str(temp_repos["repo2"]))
        schema2 = HyperGraphQLSchema()
        schema2.add_node(HyperGraphQLNode(
            id="person_2",
            node_type=EntityTypeQL.PERSON,
            name="Person 2",
            org_level=OrgLevel.REPO
        ))
        projection2.project_schema(schema2)
        manager.register_repo("repo2", str(temp_repos["repo2"]))
        
        # Aggregate
        aggregated = manager.aggregate_schemas()
        
        assert len(aggregated.nodes) == 2
        assert "repo1:person_1" in aggregated.nodes
        assert "repo2:person_2" in aggregated.nodes
        
    def test_get_org_stats(self, temp_repos):
        """Test getting org-level statistics"""
        manager = OrgAwareManager("test-org", OrgLevel.ORG)
        
        # Setup repos with data
        for repo_name, repo_path in [("repo1", temp_repos["repo1"]), ("repo2", temp_repos["repo2"])]:
            projection = GitHubRepoProjection(str(repo_path))
            schema = HyperGraphQLSchema()
            schema.add_node(HyperGraphQLNode(
                id=f"person_1",
                node_type=EntityTypeQL.PERSON,
                name=f"Person in {repo_name}",
                org_level=OrgLevel.REPO
            ))
            projection.project_schema(schema)
            manager.register_repo(repo_name, str(repo_path))
            
        stats = manager.get_org_stats()
        
        assert stats["org_name"] == "test-org"
        assert stats["repo_count"] == 2
        assert stats["total_entities"] == 2


class TestHyperGraphQLResolver:
    """Test HyperGraphQL resolver functionality"""
    
    @pytest.fixture
    def resolver(self):
        """Create a resolver with test data"""
        schema = HyperGraphQLSchema()
        resolver = HyperGraphQLResolver(schema)
        
        # Add test nodes
        schema.add_node(HyperGraphQLNode(
            id="person_1",
            node_type=EntityTypeQL.PERSON,
            name="Alice",
            org_level=OrgLevel.REPO
        ))
        schema.add_node(HyperGraphQLNode(
            id="person_2",
            node_type=EntityTypeQL.PERSON,
            name="Bob",
            org_level=OrgLevel.REPO
        ))
        
        # Add test edge
        schema.add_edge(HyperGraphQLEdge(
            id="edge_1",
            edge_type=RelationTypeQL.COMMUNICATES_WITH,
            source_id="person_1",
            target_ids=["person_2"],
            strength=0.8
        ))
        
        return resolver
        
    def test_resolve_node(self, resolver):
        """Test resolving a single node"""
        result = resolver.resolve_node("person_1")
        
        assert result is not None
        assert result["id"] == "person_1"
        assert result["name"] == "Alice"
        assert result["nodeType"] == "person"
        
    def test_resolve_nodes_with_filters(self, resolver):
        """Test resolving nodes with filters"""
        results = resolver.resolve_nodes(node_type="person", org_level="repo")
        
        assert len(results) == 2
        assert all(r["nodeType"] == "person" for r in results)
        
    def test_resolve_edge(self, resolver):
        """Test resolving a single edge"""
        result = resolver.resolve_edge("edge_1")
        
        assert result is not None
        assert result["id"] == "edge_1"
        assert result["edgeType"] == "communicates_with"
        assert result["sourceId"] == "person_1"
        
    def test_resolve_connected_nodes(self, resolver):
        """Test resolving connected nodes"""
        connected = resolver.resolve_connected_nodes("person_1")
        
        assert len(connected) == 1
        assert connected[0]["id"] == "person_2"
        
    def test_resolve_add_node(self, resolver):
        """Test adding a node via resolver"""
        input_data = {
            "nodeType": "organization",
            "name": "Test Org",
            "properties": {"size": "large"},
            "orgLevel": "org"
        }
        
        result = resolver.resolve_add_node(input_data)
        
        assert result["nodeType"] == "organization"
        assert result["name"] == "Test Org"
        assert result["properties"]["size"] == "large"
        
    def test_resolve_export_schema(self, resolver):
        """Test exporting schema via resolver"""
        result = resolver.resolve_export_schema()
        
        assert "nodes" in result
        assert "edges" in result
        assert "metadata" in result
        assert result["metadata"]["nodeCount"] == 2
        assert result["metadata"]["edgeCount"] == 1
        
    def test_load_from_repo_structure(self, resolver):
        """Test loading from repo structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Create repo structure
            projection = GitHubRepoProjection(str(repo_path))
            test_schema = HyperGraphQLSchema()
            test_schema.add_node(HyperGraphQLNode(
                id="loaded_person",
                node_type=EntityTypeQL.PERSON,
                name="Loaded Person",
                org_level=OrgLevel.REPO
            ))
            projection.project_schema(test_schema)
            
            # Load via resolver
            resolver.load_from_repo_structure(str(repo_path), "test-org")
            
            # Verify loaded
            node = resolver.schema.get_node("loaded_person")
            assert node is not None
            assert node.name == "Loaded Person"
